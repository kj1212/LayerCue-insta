#!/usr/bin/env python3
"""숏츠 03 배경음악 29.2 s — Apple Loops(Electric Funk + Duncan, 120 BPM). 끝 카드(24.8–)에서 크게, 나머지는 목소리 밑.
    ~/Documents/AIvoice/.venv/bin/python short03/music.py → short03/audio/music.wav
"""
import sys, pathlib, numpy as np, soundfile as sf
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "ep11" / "media"))
import make_tracks as MT            # song(bpm, sections), SR — 11편 데모 곡 도구
SR = MT.SR; D = "Duncan - "
secs = [(2, {"Electric Funk Synth Stabs": -7, "Electric Funk Guitar 01": -9, D + "Intro": -8}),
        (10, {"Electric Funk Guitar 01": -9, "Glitter Nights Funk Bass 01": -6, "Electric Funk Synth Stabs": -12, D + "Verse": -9}),
        (3, {"Electric Funk Guitar 02": -8, "Glitter Nights Funk Bass 01": -6, "Electric Funk Synth Stabs": -7, "Electric Funk Gliding Lead": -9, D + "Chorus": -7})]
a = MT.song(120, secs)
n = int(29.2 * SR); a = a[:n] if len(a) >= n else np.vstack([a, np.zeros((n - len(a), 2), np.float32)])
t = np.arange(n) / SR
g = np.where(t < 24.6, -10.0, -1.0); k = int(.6 * SR); g = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
a = a * (10 ** (g / 20))[:, None]; f = int(1.4 * SR); a[-f:] *= np.linspace(1, 0, f)[:, None]
a = a / (np.abs(a).max() + 1e-9) * 0.8
sf.write(H / "audio" / "music.wav", a.astype(np.float32), SR); print("music", n / SR)
