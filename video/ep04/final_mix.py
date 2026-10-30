#!/usr/bin/env python3
"""최종 소리 — 목소리(줄별 wav)를 times2 시각에 놓고, 음악은 본편에서 크게 낮춘다(타이틀·엔드 카드만 앞으로).
    ~/Documents/AIvoice/.venv/bin/python ep04/final_mix.py [body_db=-11] [edge_db=-4]  → ep04/qa/v2-mix.wav
"""
import sys, json, numpy as np, soundfile as sf, scipy.signal as ss
body_db = float(sys.argv[1]) if len(sys.argv) > 1 else -11.0; edge_db = float(sys.argv[2]) if len(sys.argv) > 2 else -4.0
segs = json.load(open("ep04/times2.json")); SR = 48000
m, _ = sf.read("ep04/audio/music-ep04.wav"); N = len(m); t = np.arange(N) / SR
title_end = segs[0]["start"]; last_voice = segs[-1]["lines"][-1]["t"] + segs[-1]["lines"][-1]["dur"]
g = np.full(N, body_db)
g[t < title_end] = edge_db; g[t > last_voice + 0.3] = edge_db
k = int(1.0 * SR); g = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]   # 1 s 로 부드럽게 넘어간다
# 말하는 동안 더 낮춘다(사용자: 말이 나올 때 음악이 크다) — 들어갈 때 0.1 s, 나올 때 0.6 s
duck_db = float(sys.argv[3]) if len(sys.argv) > 3 else -9.0
d = np.zeros(N)
for s_ in segs:
    for l in s_["lines"]:
        d[int(max(0, l["t"] - 0.1) * SR): int((l["t"] + l["dur"] + 0.2) * SR)] = duck_db
sm = np.copy(d); a, rl = 0.1 * SR, 0.6 * SR
for i in range(1, N):
    x = d[i] - sm[i - 1]; sm[i] = sm[i - 1] + x / (a if x < 0 else rl)
g = g + sm
mix = m * (10 ** (g / 20))[:, None]
for s in segs:
    for l in s["lines"]:
        v, vsr = sf.read(f"ep04/audio/vo-heart/e04-{l['key']}.wav"); v = v if v.ndim == 1 else v.mean(1)
        v = ss.resample_poly(v, SR // 1000, vsr // 1000); i = int(l["t"] * SR); j = min(N, i + len(v)); mix[i:j] += v[: j - i, None]
sf.write("ep04/qa/v2-mix.wav", mix.astype(np.float32), SR)
r = lambda a, b: 20 * np.log10(np.sqrt(np.mean(m[int(a*SR):int(b*SR)] ** 2 * 10 ** (g[int(a*SR):int(b*SR)] / 10)[:, None])) + 1e-9)
print(f"music in mix: title {r(0, title_end):.1f} | body {r(title_end, last_voice):.1f} | end {r(last_voice + 1, N / SR):.1f} dBFS")
