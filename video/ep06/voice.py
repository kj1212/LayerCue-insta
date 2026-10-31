#!/usr/bin/env python3
"""1편 내레이션 — script.json 의 줄마다 Chatterbox 로 음성을 만들고, Parakeet(STT) 로 받아 적어 빠진·뭉개진 줄을 찾는다.

    ~/Documents/AIvoice/.venv/bin/python ep01/voice.py gen  [--only s03-l02,s05-l01]   → ep01/audio/vo/e06-s03-l02.wav …
    ~/Documents/AIvoice/.venv/bin/python ep01/voice.py check                            → ep01/audio/vo/check.json (줄별 일치율)

말투: --exaggeration 0.45 --cfg_scale 0.3 (차분한 해설). 줄 이름 = 회차-구간-줄.
"""
import json, os, re, subprocess, sys, pathlib, difflib
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
PY = pathlib.Path.home() / "Documents/AIvoice/.venv/bin/python"
VO = HERE / "audio" / os.environ.get("VO_DIR", "vo"); RAW = VO / ".raw"     # VO_DIR=vo-george 처럼 목소리마다 폴더를 나눈다
TTS = os.environ.get("TTS_ARGS", "--model mlx-community/chatterbox-fp16 --exaggeration 0.45 --cfg_scale 0.3").split()
# Kokoro 예: TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice bm_george --speed 0.88"
STT_MODEL = "mlx-community/parakeet-tdt-0.6b-v3"


def lines():
    s = json.load(open(HERE / "script.json"))
    out = []
    for g in s["segments"]:
        for j, l in enumerate(g["lines"]):
            if l["text"].strip():     # "say" = 읽는 글(자막은 text) — 예: layercue.com → "layercue dot com"
                out.append((f"{g['id']}-l{j + 1:02d}", (l.get("say") or l["text"]).strip()))
    return out


def gen(only=None):
    VO.mkdir(parents=True, exist_ok=True); RAW.mkdir(exist_ok=True)
    marks = {}
    if (VO / "lines.json").exists():
        marks = json.load(open(VO / "lines.json"))
    for key, text in lines():
        f = VO / f"e06-{key}.wav"
        if only is not None and key not in only and f.exists():
            continue
        if only is None and f.exists() and marks.get(key, {}).get("text") == text:
            continue
        r = subprocess.run([str(PY), "-m", "mlx_audio.tts.generate", *TTS, "--text", text, "--output_path", str(RAW),
                            "--file_prefix", key, "--join_audio", "--audio_format", "wav"], capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-1500:] + r.stderr[-1500:])
        a, sr = sf.read(RAW / f"{key}.wav")
        if a.ndim > 1: a = a.mean(axis=1)
        nz = np.flatnonzero(np.abs(a) > 0.01)
        a = a[max(nz[0] - int(0.04 * sr), 0): nz[-1] + int(0.10 * sr)] if nz.size else a
        sf.write(f, a, sr)
        marks[key] = {"text": text, "seconds": round(len(a) / sr, 2)}
        print(key, round(len(a) / sr, 2), "s")
        json.dump(marks, open(VO / "lines.json", "w"), indent=1)
    print("total", round(sum(m["seconds"] for m in marks.values()), 1), "s")


def norm(s):
    s = s.lower().replace("layerq", "layercue").replace("layer cue", "layercue").replace("layer q", "layercue")
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return s.split()


def check():
    """줄들을 1.2 초 간격으로 이어 한 번에 받아 적고, 낱말 정렬로 줄마다 일치율을 낸다."""
    keys = [k for k, _ in lines()]
    marks = json.load(open(VO / "lines.json"))
    parts, bounds, pos = [], [], 0
    for k in keys:
        a, sr = sf.read(VO / f"e06-{k}.wav"); parts += [a, np.zeros(int(1.2 * sr))]
    joined = VO / "all-joined.wav"; sf.write(joined, np.concatenate(parts), sr)
    (VO / "stt").mkdir(exist_ok=True)
    # --output-path 는 폴더가 아니라 이름이다: <name>.txt 로 쓴다
    r = subprocess.run([str(PY), "-m", "mlx_audio.stt.generate", "--model", STT_MODEL, "--audio", str(joined),
                        "--output-path", str(VO / "stt" / "all"), "--format", "txt"], capture_output=True, text=True)
    txt = (VO / "stt" / "all.txt").read_text() if (VO / "stt" / "all.txt").exists() else ""
    heard = norm(txt); said = []
    for k in keys:
        w = norm(marks[k]["text"]); said.append((k, w, pos, pos + len(w))); pos += len(w)
    flat = [w for _, ws, _, _ in said for w in ws]
    sm = difflib.SequenceMatcher(a=flat, b=heard, autojunk=False)
    hit = [False] * len(flat)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i in range(i1, i2): hit[i] = True
    report = {}
    for k, ws, a, b in said:
        ok = sum(hit[a:b]); report[k] = {"match": round(ok / max(1, len(ws)), 2), "words": len(ws), "seconds": marks[k]["seconds"],
                                         "wps": round(len(ws) / max(0.1, marks[k]["seconds"]), 2)}
    json.dump({"transcript": txt, "lines": report}, open(VO / "check.json", "w"), indent=1)
    bad = {k: v for k, v in report.items() if v["match"] < 0.8 or v["wps"] > 3.4}
    print("checked", len(report), "lines; suspicious:", json.dumps(bad, indent=1) if bad else "none")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "gen":
        only = None
        if "--only" in sys.argv: only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
        gen(only)
    elif cmd == "check":
        check()
