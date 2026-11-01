#!/usr/bin/env python3
"""11편 데모 곡 — GarageBand Apple Loops(로열티 없음)로 가상 제목의 연주곡 4개와 수상 팡파르 1개를 만든다.

    ~/Documents/AIvoice/.venv/bin/python ep11/media/make_tracks.py   → ep11/media/tracks/*.mp3 · award-fanfare.wav

Open Doors 는 앞에 말소리 인트로(약 5 s)와 끝에 긴 페이드가 있다 — In point · Out point 데모용.
"""
import json, subprocess, pathlib, numpy as np, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "tracks"; OUT.mkdir(exist_ok=True)
CACHE = HERE.parent.parent / "ep10" / "audio" / "loops"
IDX = {r["name"]: r for r in json.load(open(HERE.parent.parent / "ep10" / "audio" / "loops.json"))}
SR = 48000

def loop(name, bpm):
    r = IDX[name]; out = CACHE / f"{name}.wav"
    if not out.exists(): subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEF32@48000", "-c", "2", r["path"], str(out)], check=True)
    a, _ = sf.read(out, dtype="float32")
    if a.ndim == 1: a = np.stack([a, a], 1)
    n = int(round(int(r["u_beat count"]) * 60 / bpm * SR))
    return a[:n] if len(a) >= n else np.vstack([a, np.zeros((n - len(a), 2), np.float32)])

def song(bpm, sections):
    """sections = [(마디 수, {루프: dB}), …] — 0 마디 기준 위상으로 이어 붙인다."""
    BAR = int(round(SR * 240 / bpm)); total = sum(n for n, _ in sections)
    mix = np.zeros((total * BAR, 2), np.float32); cache = {}; b = 0
    for i, (n, stems) in enumerate(sections):
        s0, s1 = b * BAR, (b + n) * BAR
        prev = sections[i - 1][1] if i else {}; nxt = sections[i + 1][1] if i + 1 < len(sections) else {}
        for name, db in stems.items():
            if name not in cache: cache[name] = loop(name, bpm)
            L = cache[name]; seg = L[np.arange(s0, s1) % len(L)] * (10 ** (db / 20))
            f = 480; r = np.linspace(0, 1, f, dtype=np.float32)[:, None]
            if name not in prev: seg[:f] *= r
            if name not in nxt: seg[-f:] *= r[::-1]
            mix[s0:s1] += seg
        b += n
    return np.tanh(mix * 1.1) / 1.1

def norm(a, peak_db=-3.0, rms_db=-18.0):
    rms = np.sqrt(np.mean(a ** 2)) + 1e-9; a = a * (10 ** (rms_db / 20) / rms)
    pk = np.max(np.abs(a)); lim = 10 ** (peak_db / 20)
    return np.tanh(a / lim) * lim if pk > lim else a

def fade(a, sec_in, sec_out):
    a = a.copy(); ni, no = int(sec_in * SR), int(sec_out * SR)
    if ni: a[:ni] *= np.linspace(0, 1, ni, dtype=np.float32)[:, None]
    if no: a[-no:] *= (np.linspace(1, 0, no, dtype=np.float32) ** 2)[:, None]
    return a

def mp3(a, name, title):
    w = OUT / f"{name}.wav"; sf.write(w, a, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(w), "-c:a", "libmp3lame", "-b:a", "320k", "-ar", "44100",
                    "-metadata", f"title={title}", "-metadata", "artist=Northfield Sessions", str(OUT / f"{name}.mp3")], check=True)
    w.unlink(); print(name, f"{len(a) / SR:.1f}s")

# ── Open Doors (120 BPM, G) — 말 인트로 + 긴 페이드
D = "Duncan - "
od = song(120, [(2, {"Moving Pictures Synth": -8}),
                (8, {"Moving Pictures Synth": -9, "Moving Pictures Bass": -6, D + "Intro": -10}),
                (16, {"Moving Pictures Rhythm Guitar": -9, "Moving Pictures Bass": -6, "Moving Pictures Synth": -11, D + "Verse": -9}),
                (16, {"Moving Pictures Acoustic Guitar": -8, "Moving Pictures Rhythm Guitar": -11, "Moving Pictures Bass": -6, "Moving Pictures Synth": -10, D + "Chorus": -8}),
                (16, {"Moving Pictures Rhythm Guitar": -9, "Moving Pictures Bass": -6, "Moving Pictures Synth": -11, D + "Verse": -9}),
                (8, {"Moving Pictures Synth": -8, "Moving Pictures Bass": -7, D + "Outro": -10})])
od = fade(norm(od), 0.02, 14.0)
intro = HERE / "open-doors-intro.wav"
if not intro.exists():
    raise SystemExit("먼저 말소리 인트로를 만든다: open-doors-intro.wav")
v, vsr = sf.read(intro, dtype="float32"); v = v if v.ndim == 1 else v.mean(1)
import scipy.signal as ss
v = ss.resample_poly(v, SR // 1000, vsr // 1000); v = v / (np.max(np.abs(v)) + 1e-9) * 0.7
pad = int(0.3 * SR); lead = np.zeros((pad + len(v) + int(0.8 * SR), 2), np.float32); lead[pad:pad + len(v)] += v[:, None]
mp3(np.vstack([lead, od]), "open-doors", "Open Doors")

# ── Lobby Light (120 BPM, G) — 차분한 일렉트릭 피아노
J = "Julian - "
ll = song(120, [(4, {"Shining Star Electric Piano 01": -7, "Shining Star Bass 01": -8}),
                (16, {"Shining Star Electric Piano 01": -7, "Shining Star Bass 01": -6, "Shining Star Guitar 01": -12, J + "Verse": -12}),
                (16, {"Shining Star Electric Piano 02": -7, "Shining Star Bass 02": -6, "Shining Star Guitar 02": -11, J + "Chorus": -11}),
                (16, {"Shining Star Electric Piano 01": -7, "Shining Star Bass 01": -6, "Shining Star Guitar 01": -12, J + "Verse": -12}),
                (4, {"Shining Star Electric Piano 01": -7, J + "Outro": -13})])
mp3(fade(norm(ll), 0.02, 3.0), "lobby-light", "Lobby Light")

# ── Walk-up (125 BPM, C) — 힘찬 인디 디스코
Le = "Leah - "
wu = song(125, [(4, {"Ready to Go Rhythm Guitar": -8, Le + "Intro": -9}),
                (16, {"Ready to Go Rhythm Guitar": -8, "Ready to Go Bass 01": -6, Le + "Verse": -8}),
                (16, {"Ready to Go Lead Guitar": -8, "Ready to Go Rhythm Guitar": -10, "Ready to Go Bass 02": -6, Le + "Chorus": -7}),
                (16, {"Ready to Go Rhythm Guitar": -8, "Ready to Go Bass 01": -6, Le + "Verse": -8}),
                (4, {"Ready to Go Lead Guitar": -8, "Ready to Go Bass 01": -7, Le + "Outro": -8})])
mp3(fade(norm(wu), 0.02, 2.5), "walk-up", "Walk-up")

# ── Interval (110 BPM, B) — 휴식 시간, 느긋하게
K = "Kyle - "
iv = song(110, [(4, {"Contrails Synth": -8, "Contrails Acoustic Guitar": -9}),
                (16, {"Contrails Synth": -9, "Contrails Acoustic Guitar": -8, "Contrails Bass": -6, K + "Verse": -12}),
                (16, {"Contrails Synth": -9, "Contrails Lead Guitar": -9, "Contrails Bass": -6, K + "Chorus": -11}),
                (8, {"Contrails Synth": -8, "Contrails Acoustic Guitar": -8, K + "Outro": -13})])
mp3(fade(norm(iv), 0.02, 3.0), "interval", "Interval")

# ── 수상 팡파르(120 BPM) — 금관 두 마디 + 마지막 울림
fan = song(120, [(2, {"Throwback Funk Brass 01": -4, "Throwback Funk Beat 03": -9, "Throwback Funk Synth Bass": -8})])
tail = fan[-int(0.5 * SR):] * np.linspace(1, 0, int(0.5 * SR), dtype=np.float32)[:, None]
ring = np.vstack([fan, np.zeros((int(1.6 * SR), 2), np.float32)])
# 끝 울림: 마지막 박을 길게 끌어 잔향처럼(간단한 지수 감쇠 메아리)
for k, g in enumerate([0.45, 0.28, 0.16, 0.09]):
    s = len(fan) - int(0.5 * SR) + int((k + 1) * 0.3 * SR); ring[s:s + len(tail)] += tail * g
sf.write(OUT / "award-fanfare.wav", norm(fade(ring, 0.0, 1.2), rms_db=-16.0), SR); print("award-fanfare", f"{len(ring) / SR:.1f}s")
