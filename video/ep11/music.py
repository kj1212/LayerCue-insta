#!/usr/bin/env python3
"""배경음악 — 이 맥의 GarageBand Apple Loops(사용권: 자기 영상의 배경음으로 로열티 없이 사용 가능)를 마디에 맞춰 쌓는다.

    ~/Documents/AIvoice/.venv/bin/python ep01/music.py demo            → ep01/audio/samples/music-*.wav (32 s 맛보기 셋)
    ~/Documents/AIvoice/.venv/bin/python ep01/music.py full <style>    → ep01/audio/music-full.wav (ep01/times.json 의 구간에 맞춘 전곡)

루프는 같은 「곡 묶음」(템포·키가 같다)에서 고르고, 120 BPM 이라 한 마디 = 2 s. 루프는 0 마디 기준으로 위상을 맞춰 이어 붙여
구간이 바뀌어도 박자가 어긋나지 않는다. 구간마다 루프별 음량(dB)을 정한다.
"""
import sys, json, subprocess, pathlib, numpy as np, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent
LOOPDIR = pathlib.Path("/Library/Audio/Apple Loops/Apple")
CACHE = HERE / "audio" / "loops"; CACHE.mkdir(parents=True, exist_ok=True)
SR = 48000; BPM = 120; BAR = int(SR * 60 / BPM * 4)        # 96000 샘플 = 2 s
IDX = {r["name"]: r for r in json.load(open(HERE / "audio" / "loops.json"))}

def loop(name):
    """루프를 48 kHz 스테레오로 풀고, 박자 수에 맞춰 길이를 정확히 자른다."""
    r = IDX[name]; out = CACHE / f"{name}.wav"
    if not out.exists():
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEF32@48000", "-c", "2", r["path"], str(out)], check=True)
    a, sr = sf.read(out, dtype="float32")
    if a.ndim == 1: a = np.stack([a, a], 1)
    n = int(round(int(r["u_beat count"]) * 60 / BPM * SR))
    a = a[:n] if len(a) >= n else np.vstack([a, np.zeros((n - len(a), 2), np.float32)])
    return a

def render(sections, total_bars, fade_bars_out=2):
    """sections = [(bar0, bar1, {loop: dB}), …] → 스테레오 float32"""
    N = total_bars * BAR; mix = np.zeros((N, 2), np.float32); cache = {}
    for b0, b1, stems in sections:
        s0, s1 = b0 * BAR, min(b1, total_bars) * BAR
        for name, db in stems.items():
            if name not in cache: cache[name] = loop(name)
            L = cache[name]; n = len(L); g = 10 ** (db / 20)
            idx = (np.arange(s0, s1) % n)                      # 0 마디 기준 위상
            seg = L[idx] * g
            f = min(480, len(seg) // 2)                         # 10 ms 들고 나기 — 딸깍 소리 방지
            ramp = np.linspace(0, 1, f, dtype=np.float32)[:, None]
            seg[:f] *= ramp; seg[-f:] *= ramp[::-1]
            mix[s0:s1] += seg
    # 마무리: 부드러운 포화 + 끝 페이드 + RMS 맞춤
    mix = np.tanh(mix * 1.1) / 1.1
    fo = fade_bars_out * BAR; mix[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
    rms = np.sqrt(np.mean(mix ** 2)) + 1e-9; mix *= 10 ** (-18 / 20) / rms
    peak = np.abs(mix).max()
    if peak > 0.95: mix *= 0.95 / peak
    return mix

STYLES = {
  # 밝은 팝 — 신스 스탭·리듬 기타·패드·베이스 + 전자 드럼
  "pop": {"drums_full": "Duncan - Verse", "drums_intro": "Duncan - Intro", "drums_out": "Duncan - Outro",
          "full": {"Disco Pop Bass": -4, "Disco Pop Rhythm Guitar": -6, "Disco Pop Synth Stabs": -7, "Disco Pop Synth Pad": -9},
          "bed":  {"Disco Pop Synth Pad": -8, "Disco Pop Rhythm Guitar": -9, "Disco Pop Bass": -9},
          "lift": {"Disco Pop Lead Guitar": -8}},
  # 따뜻한 건반 — 일렉트릭 피아노·피아노·리듬 기타·베이스 + 전자 드럼
  "keys": {"drums_full": "Julian - Verse", "drums_intro": "Julian - Intro", "drums_out": "Julian - Outro",
           "full": {"Disco Delight Electric Piano 01": -5, "Disco Delight Piano": -8, "Disco Delight Rhythm Guitar": -9, "Disco Delight Bass": -5},
           "bed":  {"Disco Delight Electric Piano 01": -8, "Disco Delight Bass": -10},
           "lift": {"Disco Delight Clav": -10}},
  # 햇살 어쿠스틱 — 통기타·일렉 리듬·신스·베이스 + 전자 드럼
  "acoustic": {"drums_full": "Duncan - Verse", "drums_intro": "Duncan - Intro", "drums_out": "Duncan - Outro",
               "full": {"Moving Pictures Acoustic Guitar": -4, "Moving Pictures Rhythm Guitar": -9, "Moving Pictures Synth": -9, "Moving Pictures Bass": -5},
               "bed":  {"Moving Pictures Acoustic Guitar": -7, "Moving Pictures Bass": -10, "Moving Pictures Synth": -12},
               "lift": {}},
}

def demo(style):
    S = STYLES[style]
    secs = [(0, 2, {S["drums_intro"]: -8, **{k: v - 3 for k, v in S["full"].items() if "Pad" in k or "Synth" in k}}),
            (2, 8, {S["drums_full"]: -6, **S["full"], **S["lift"]}),
            (8, 14, {S["drums_full"]: -16, **S["bed"]}),
            (14, 16, {S["drums_out"]: -7, **S["full"]})]
    return render(secs, 16)

if __name__ == "__main__":
    if sys.argv[1] == "demo":
        out = HERE / "audio" / "samples"; out.mkdir(parents=True, exist_ok=True)
        for st in STYLES:
            sf.write(out / f"music-{st}.wav", demo(st), SR); print("music", st)
