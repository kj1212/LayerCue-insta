#!/usr/bin/env python3
"""숏츠 만들기(본편 4K 녹화를 잘라서) — specs.py 한 편씩: 목소리 · 시간표 · 글판 · 끝 카드 · 음악 · AE 설정(cfg.js) · 자막 · 업로드 글.
    ~/Documents/AIvoice/.venv/bin/python shorts/make.py 02 05 …   (없으면 전부)
그다음 AE: RENDER_NOW=1 OUT_NAME=<id> ./ae.sh shorts/build_short   (id = s04-ready-in-a-minute …)
"""
import sys, json, subprocess, pathlib, re, html
import numpy as np, soundfile as sf
H = pathlib.Path(__file__).resolve().parent; V = H.parent
sys.path.insert(0, str(H))
import specs, beats as BT
PY = pathlib.Path.home() / "Documents/AIvoice/.venv/bin/python"
TTS = ["--model", "mlx-community/Kokoro-82M-bf16", "--voice", "af_heart", "--speed", "0.97"]
SCR = pathlib.Path("/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/949d2ea0-79bb-4103-a168-0f8598aa55e1/scratchpad/shortvo")
W, WH, PANEL_W, PANEL_H, ASPECT = 3840, 2100, 1000, 700, 1000 / 700
MUSIC = [  # 120 BPM 묶음 — 편마다 돌려 쓴다
 {"Electric Funk Guitar 01": -9, "Glitter Nights Funk Bass 01": -6, "Electric Funk Synth Stabs": -12, "Duncan - Verse": -9},
 {"Shining Star Electric Piano 01": -7, "Shining Star Bass 01": -6, "Shining Star Guitar 01": -12, "Julian - Verse": -11},
 {"Moving Pictures Rhythm Guitar": -9, "Moving Pictures Bass": -6, "Moving Pictures Synth": -11, "Duncan - Verse": -9},
 {"Drop the Funk Wah Guitar": -9, "Drop the Funk Bass 01": -6, "Drop the Funk Electric Piano": -10, "Duncan - Verse": -9},
 {"Slow Go Disco Rhythm Guitar": -9, "Slow Go Disco Bass 01": -6, "Slow Go Disco Synth Pad": -11, "Julian - Verse": -11},
 {"Polyester Boogie Guitar": -9, "Polyester Boogie Bass 01": -6, "Disco Delight Electric Piano 01": -10, "Julian - Verse": -11},
 {"Disco Fever Guitar": -9, "Disco Fever Bass": -6, "Crystal Ball Electric Piano": -10, "Julian - Verse": -11},
]

LOOPS = {r["name"]: r for r in json.load(open(V / "ep10" / "audio" / "loops.json"))}
def song(bpm, sections, SR=48000):
    """Apple Loops 를 0 마디 기준 위상으로 이어 붙인다(11편 make_tracks 와 같다)."""
    BAR = int(round(SR * 240 / bpm)); total = sum(n for n, _ in sections); mix = np.zeros((total * BAR, 2), np.float32); b = 0
    for n, stems in sections:
        for name, db in stems.items():
            out = V / "ep10" / "audio" / "loops" / f"{name}.wav"
            if not out.exists(): subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEF32@48000", "-c", "2", LOOPS[name]["path"], str(out)], check=True)
            L, _ = sf.read(out, dtype="float32"); L = np.stack([L, L], 1) if L.ndim == 1 else L
            m = int(round(int(LOOPS[name]["u_beat count"]) * 60 / bpm * SR)); L = L[:m] if len(L) >= m else np.vstack([L, np.zeros((m - len(L), 2), np.float32)])
            mix[b * BAR:(b + n) * BAR] += L[np.arange(b * BAR, (b + n) * BAR) % len(L)] * (10 ** (db / 20))
        b += n
    return np.tanh(mix * 1.1) / 1.1

def tts(text, out):
    if out.exists() and out.with_suffix(".txt").exists() and out.with_suffix(".txt").read_text() == text: return
    SCR.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(PY), "-m", "mlx_audio.tts.generate", *TTS, "--text", text, "--output_path", str(SCR), "--file_prefix", "x", "--join_audio", "--audio_format", "wav"], capture_output=True, check=True)
    a, sr = sf.read(SCR / "x.wav"); a = a if a.ndim == 1 else a.mean(1)
    nz = np.flatnonzero(np.abs(a) > 0.01); a = a[max(nz[0] - int(.04 * sr), 0): nz[-1] + int(.1 * sr)]
    sf.write(out, a, sr); out.with_suffix(".txt").write_text(text)

def dur(p): return len(sf.read(p)[0]) / sf.info(p).samplerate

def zone(r):
    x, y, w, h = r; cx, cy = x + w / 2, y + h / 2
    ww = max(w * 1.35, h * 1.35 * ASPECT, 720.0); ww = min(ww, W); hh = ww / ASPECT
    if hh > WH: hh = WH; ww = hh * ASPECT
    cx = min(max(cx, ww / 2), W - ww / 2); cy = min(max(cy, hh / 2), WH - hh / 2)
    m = 10; fx, fy, fw, fh = x - m, y - m, max(w + 2 * m, 60), max(h + 2 * m, 50)
    return dict(zx=round(cx, 1), zy=round(cy, 1), zw=round(ww, 1), ox=round(fx + fw / 2, 1), oy=round(fy + fh / 2, 1), ow=round(fw, 1), oh=round(fh, 1))

def rec_dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)

def make(sp, idx):
    ep = int(sp["ep"]); sid = f"s{ep + 2:02d}-{sp['slug']}"; D = H / sid; (D / "audio").mkdir(parents=True, exist_ok=True)
    cand = BT.beats(sp["ep"]); SL = json.load(open(V / f"ep{sp['ep']}" / "shotlist2.json"))
    # ── 목소리
    words = [b["w"] for b in sp["beats"]]
    recap_vo = " ".join(w.capitalize() + "." for w in words)
    ep_vo = f"Episode {specs.NUM[ep]} walks you through it."
    lines = [sp["hook_vo"]] + [b["vo"] for b in sp["beats"]] + [recap_vo, ep_vo]
    for i, t in enumerate(lines): tts(t, D / "audio" / f"{i:02d}.wav")
    dv = [dur(D / "audio" / f"{i:02d}.wav") for i in range(len(lines))]
    # ── 시간표
    Hk = max(3.3, dv[0] + 0.75); S, Dd = [], []; t = Hk + 0.05
    for i in range(4):
        d = max(3.8, dv[i + 1] + 1.0); S.append(round(t, 2)); Dd.append(round(d, 2)); t += d
    Rt = round(t, 2); Rd = max(3.6, dv[5] + dv[6] + 0.9); END0 = round(Rt + Rd, 2); DUR = round(END0 + 4.4, 2)
    vo_at = [0.35] + [round(S[i] + 0.15, 2) for i in range(4)] + [round(Rt + 0.2, 2), round(Rt + 0.2 + dv[5] + 0.3, 2)]
    # ── 장면
    bl = []
    for i, b in enumerate(sp["beats"]):
        c = cand[b["b"]]; rp = V / c["rec"]; rd = rec_dur(rp)
        lead = 1.4; src = c["v"] - lead
        if i == 0: src = max(src, min(S[0], c["v"] - 0.6))      # 훅 동안 앞부분을 보여 줄 수 있게
        src = max(0.0, min(src, rd - Dd[i] - 0.2))
        z = zone(c["region"]); wav = rp.with_suffix(".wav"); aj = rp.with_suffix(".audio.json")
        aud = None
        if sp.get("app_audio") is not None and wav.exists() and aj.exists():
            aud = dict(file=str(wav), shift=round(SL["rec_t0"] + json.load(open(aj))["offset"], 3), db=sp["app_audio"])
        bl.append(dict(rec=str(rp), src=round(src, 3), t=S[i], d=Dd[i], audio=aud, **z, lbl=c["lbl"], line=c["line"]))
    cfg = dict(id=sid, ep=ep, DUR=DUR, H=round(Hk, 2), Rt=Rt, END0=END0, beats=bl,
               vo=[dict(file=str(D / "audio" / f"{i:02d}.wav"), t=vo_at[i]) for i in range(len(lines))],
               subs=[[0.35, round(Hk - 0.1, 2)]] + [[round(S[i] + 0.1, 2), round(S[i] + Dd[i] - 0.1, 2)] for i in range(4)] + [[vo_at[6] - 0.1, END0]],
               endframes=str(V / "frames" / f"end-{sid}" / "00000.png"), music=str(D / "audio" / "music.wav"), root=str(D))
    (D / "cfg.js").write_text("var CFG = " + json.dumps(cfg, indent=1) + ";\n")
    # ── 글판
    hook = f'<div class="p hook" id="hook"><div class="k">[ LAYERCUE ]</div><div class="a">{sp["hook"][0]}</div><div class="b">{sp["hook"][1]}</div></div>'
    ws = "".join(f'<div class="p word" id="w{i+1}"><div class="w">{b["w"]}</div><div class="s">{b["s"]}</div></div>' for i, b in enumerate(sp["beats"]))
    rc = '<div class="p recap" id="recap">' + "".join(f'<div class="{"h" if i % 2 else ""}">{w}.</div>' for i, w in enumerate(words)) + "</div>"
    tag = f'<div class="p tag" id="tag">FULL TUTORIAL · <b>LAYERCUE FROM ZERO · EP {ep:02d}</b></div>'
    subs = [sp["hook_vo"]] + [b["vo"] for b in sp["beats"]] + [ep_vo]
    sb = "".join(f'<div class="p sub" id="s{i+1}">{html.escape(t)}</div>' for i, t in enumerate(subs))
    (D / "parts.html").write_text((H / "parts.tmpl.html").read_text().replace("%BODY%", hook + ws + rc + tag + sb))
    # ── 음악
    bars = int(np.ceil(DUR / 2.0)) + 1; SR = 48000
    a = song(120, [(bars, MUSIC[idx % len(MUSIC)])]); n = int(DUR * SR); a = a[:n]
    tt = np.arange(n) / SR; g = np.where(tt < END0 - 0.2, -10.0, -1.0)
    k = int(.6 * SR); g = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
    a = a * (10 ** (g / 20))[:, None]; f = int(1.4 * SR); a[-f:] *= np.linspace(1, 0, f)[:, None]; fi = int(.4 * SR); a[:fi] *= np.linspace(0, 1, fi)[:, None]
    sf.write(D / "audio" / "music.wav", (a / (np.abs(a).max() + 1e-9) * 0.8).astype(np.float32), SR)
    # ── 자막(srt, 목소리 시각) · 업로드 글
    def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round((x-int(x))*1000)):03d}"
    srt_lines = [(vo_at[i], vo_at[i] + dv[i], lines[i]) for i in range(len(lines))]
    (D / "out" / "subtitles").mkdir(parents=True, exist_ok=True)
    (D / "out" / "subtitles" / f"{sid}-en.srt").write_text("\n".join(f"{i+1}\n{ts(a)} --> {ts(b + .2)}\n{t}\n" for i, (a, b, t) in enumerate(srt_lines)))
    (D / "spec.json").write_text(json.dumps(dict(sp, id=sid, lines=lines, vo_at=vo_at, dur=DUR), ensure_ascii=False, indent=1))
    return sid, DUR, [b["w"] for b in sp["beats"]]

if __name__ == "__main__":
    want = sys.argv[1:]
    for i, sp in enumerate(specs.S):
        if want and sp["ep"] not in want: continue
        print(*make(sp, i))
