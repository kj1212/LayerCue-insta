#!/usr/bin/env python3
"""배경음악 스타일(120 BPM Apple Loops) — 편 · 숏츠의 music_full 이 이름으로 골라 쓴다. 2026-11-02 사용자: 「새 배경음악을 더」.
    ~/Documents/AIvoice/.venv/bin/python music/styles.py        → music/styles/<이름>.wav (40 s 맛보기)
D = 드럼(인트로 · 바닥 A · 바닥 B · 올림 · 끝) · BASS RG(리듬) PAD STAB LEAD = 같은 곡 묶음(키가 같다)
"""
import json, subprocess, pathlib, numpy as np, soundfile as sf
V = pathlib.Path(__file__).resolve().parent.parent
LOOPS = {r["name"]: r for r in json.load(open(V / "ep10" / "audio" / "loops.json"))}
SR, BPM = 48000, 120; BAR = SR * 2
STYLES = {
 # 이미 쓴 것(디스코 펑크) — 1–15편
 "julian-disco":   dict(D=["Julian - Intro", "Julian - Verse", "Julian - Bridge", "Julian - Chorus", "Julian - Outro"],
                        BASS="Disco Fever Bass", RG="Disco Fever Guitar", PAD="Crystal Ball Electric Piano", STAB="Crystal Ball Clav", LEAD="Crystal Ball Wah Guitar"),
 # 새것 — 칠웨이브 · 인디 디스코 · 어쿠스틱
 "landing-chill":  dict(D=["Minimal Backbeat 01", "Minimal Backbeat 01", "Minimal Backbeat 02", "Disco Swagger Beat 01", "Minimal Backbeat 02"],
                        BASS="Landing in LA Bass 01", RG="Landing in LA Guitar", PAD="Landing in LA Synth 01", STAB="Landing in LA Synth 02", LEAD="Landing in LA Synth 03"),
 "road-trip":      dict(D=["Disco Swagger Beat 02", "Disco Swagger Beat 01", "Disco Swagger Beat 02", "Doubledown Beat 01", "Disco Swagger Beat 02"],
                        BASS="Road Trip Summer Bass", RG="Road Trip Summer Guitar", PAD="Road Trip Summer Synth", STAB="Road Trip Summer Synth", LEAD="Road Trip Summer Guitar"),
 "camden-indie":   dict(D=["Duncan - Intro", "Duncan - Verse", "Duncan - Bridge", "Duncan - Chorus", "Duncan - Outro"],
                        BASS="Camden Lock Bass", RG="Camden Lock Rhythm Guitar", PAD="Camden Lock Rhythm Guitar", STAB="Camden Lock Lead Guitar", LEAD="Camden Lock Lead Guitar"),
 "disco-pop":      dict(D=["Julian - Intro", "Julian - Verse", "Julian - Bridge", "Julian - Chorus", "Julian - Outro"],
                        BASS="Disco Pop Bass", RG="Disco Pop Rhythm Guitar", PAD="Disco Pop Synth Pad", STAB="Disco Pop Synth Stabs", LEAD="Disco Pop Lead Guitar"),
 "simple-melody":  dict(D=["Doubledown Beat 02", "Doubledown Beat 01", "Doubledown Beat 02", "Disco Swagger Beat 01", "Doubledown Beat 02"],
                        BASS="Simple Melody Bass", RG="Simple Melody Guitar", PAD="Simple Melody Synth", STAB="Simple Melody Synth", LEAD="Simple Melody Guitar"),
 "hyperlapse":     dict(D=["Go Time Beat 01", "Go Time Beat 01", "Go Time Beat 02", "Hot Stuff Beat 01", "Go Time Beat 02"],
                        BASS="Hyperlapse Bass", RG="Hyperlapse Guitar", PAD="Hyperlapse Synth", STAB="Hyperlapse Synth", LEAD="Hyperlapse Guitar"),
 "summers-end":    dict(D=["Simple Steady Break", "Minimal Backbeat 01", "Minimal Backbeat 02", "Doubledown Beat 01", "Simple Steady Break"],
                        BASS="Summers End Bass", RG="Summers End Acoustic Guitar", PAD="Summers End Acoustic Guitar", STAB="Summers End Acoustic Guitar", LEAD="Summers End Acoustic Guitar"),
}
def loop(name):
    r = LOOPS[name]; out = V / "ep10" / "audio" / "loops" / f"{name}.wav"
    if not out.exists(): subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEF32@48000", "-c", "2", r["path"], str(out)], check=True)
    a, _ = sf.read(out, dtype="float32"); a = np.stack([a, a], 1) if a.ndim == 1 else a
    n = int(round(int(r["u_beat count"]) * 60 / BPM * SR))
    return a[:n] if len(a) >= n else np.vstack([a, np.zeros((n - len(a), 2), np.float32)])
def plan(st, bars, title_bars=3, end_bars=4, chap=()):
    """music_full 과 같은 짜임: 인트로 → 바닥(8 마디마다 A/B) · 챕터 첫 마디 올림 → 끝 코러스"""
    D = st["D"]; P = {}
    for b in range(bars):
        if b < title_bars: P[b] = {D[0] if b < title_bars - 1 else D[3]: -5, st["STAB"]: -7, st["BASS"]: -4, st["PAD"]: -9}
        elif b >= bars - end_bars: P[b] = {D[3] if b < bars - 2 else D[4]: -5, st["BASS"]: -4, st["RG"]: -7, st["STAB"]: -8, st["PAD"]: -9, st["LEAD"]: -9}
        elif b in chap: P[b] = {D[3]: -9, st["BASS"]: -6, st["STAB"]: -8, st["PAD"]: -10, st["RG"]: -10}
        else:
            k = ((b - title_bars) // 8) % 2
            P[b] = {D[1]: -13, st["BASS"]: -7, st["RG"]: -10, st["PAD"]: -12} if k == 0 else {D[2]: -14, st["BASS"]: -7, st["STAB"]: -13, st["PAD"]: -11}
    return P
def render(P, bars):
    mix = np.zeros((bars * BAR, 2), np.float32); cache = {}
    for b, stems in P.items():
        s0, s1 = b * BAR, (b + 1) * BAR
        for name, db in stems.items():
            if name not in cache: cache[name] = loop(name)
            L = cache[name]; seg = L[np.arange(s0, s1) % len(L)] * (10 ** (db / 20))
            f = 240; r = np.linspace(0, 1, f, dtype=np.float32)[:, None]
            if name not in P.get(b - 1, {}): seg[:f] *= r
            if name not in P.get(b + 1, {}): seg[-f:] *= r[::-1]
            mix[s0:s1] += seg
    mix = np.tanh(mix * 1.05) / 1.05
    return mix
if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent / "styles"
    for name, st in STYLES.items():
        missing = [v for k, v in st.items() if k != "D" and v not in LOOPS] + [d for d in st["D"] if d not in LOOPS]
        if missing: print("skip", name, missing); continue
        m = render(plan(st, 20, chap=(11,)), 20); f = 2 * BAR; m[-f:] *= np.linspace(1, 0, f)[:, None]
        m = m / (np.abs(m).max() + 1e-9) * 0.85; sf.write(out / f"{name}.wav", m, SR); print("style", name)
