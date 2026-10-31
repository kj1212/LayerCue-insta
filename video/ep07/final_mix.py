#!/usr/bin/env python3
"""최종 소리 — 목소리(줄별 wav)를 times2 시각에 놓고, 음악은 본편에서 크게 낮춘다(타이틀·엔드 카드만 앞으로).
    ~/Documents/AIvoice/.venv/bin/python ep07/final_mix.py [body_db=-11] [edge_db=-4]  → ep07/qa/v2-mix.wav
"""
import sys, json, numpy as np, soundfile as sf, scipy.signal as ss
body_db = float(sys.argv[1]) if len(sys.argv) > 1 else -11.0; edge_db = float(sys.argv[2]) if len(sys.argv) > 2 else -4.0
segs = json.load(open("ep07/times2.json")); SR = 48000
m, _ = sf.read("ep07/audio/music-ep07.wav"); N = len(m); t = np.arange(N) / SR
title_end = segs[0]["start"]; last_voice = segs[-1]["lines"][-1]["t"] + segs[-1]["lines"][-1]["dur"]
g = np.full(N, body_db)
g[t < title_end] = edge_db; g[t > last_voice + 0.3] = edge_db
k = int(1.0 * SR); g = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]   # 1 s 로 부드럽게 넘어간다
# 말하는 동안 더 낮춘다(사용자: 말이 나올 때 음악이 크다) — 들어갈 때 0.1 s, 나올 때 0.6 s
duck_db = float(sys.argv[3]) if len(sys.argv) > 3 else -9.0
# 덕킹을 덜 민감하게(사용자, 7편부터): 말 사이 2.5 s 보다 짧게 쉬면 음악을 올리지 않고 낮춘 채 둔다. 올라올 때는 1.5 s 에 걸쳐 천천히
HOLD_GAP, REL = 2.5, 1.5
iv = sorted([(max(0, l["t"] - 0.1), l["t"] + l["dur"] + 0.2) for s_ in segs for l in s_["lines"]])
merged = []
for a0, b0 in iv:
    if merged and a0 - merged[-1][1] < HOLD_GAP: merged[-1][1] = max(merged[-1][1], b0)
    else: merged.append([a0, b0])
d = np.zeros(N)
for a0, b0 in merged: d[int(a0 * SR): int(b0 * SR)] = duck_db
sm = np.copy(d); a, rl = 0.1 * SR, REL * SR
for i in range(1, N):
    x = d[i] - sm[i - 1]; sm[i] = sm[i - 1] + x / (a if x < 0 else rl)
g = g + sm
mix = m * (10 ** (g / 20))[:, None]
for s in segs:
    for l in s["lines"]:
        v, vsr = sf.read(f"ep07/audio/vo-heart/e07-{l['key']}.wav"); v = v if v.ndim == 1 else v.mean(1)
        v = ss.resample_poly(v, SR // 1000, vsr // 1000); i = int(l["t"] * SR); j = min(N, i + len(v)); mix[i:j] += v[: j - i, None]
sf.write("ep07/qa/v2-mix.wav", mix.astype(np.float32), SR)
r = lambda a, b: 20 * np.log10(np.sqrt(np.mean(m[int(a*SR):int(b*SR)] ** 2 * 10 ** (g[int(a*SR):int(b*SR)] / 10)[:, None])) + 1e-9)
print(f"music in mix: title {r(0, title_end):.1f} | body {r(title_end, last_voice):.1f} | end {r(last_voice + 1, N / SR):.1f} dBFS")
