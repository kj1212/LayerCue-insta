#!/usr/bin/env python3
"""1편 전곡 — GarageBand 루프(Disco Pop 묶음 + Duncan 드럼, 120 BPM)를 times2(줄별 시각)에 맞춰 쌓고, 목소리 밑에서 덕킹까지 끝낸다.

    ~/Documents/AIvoice/.venv/bin/python ep01/music_full.py   → ep01/audio/music-ep17.wav (48 kHz 스테레오)

짜임(한 마디 = 2 s, 0 초부터 마디 격자):
  타이틀(0–6 s)  인트로 — 드럼 Intro · 스탭 · 베이스 · 패드, 크게
  본편           바닥(bed) — 드럼 Verse 를 작게 · 베이스 · 리듬 기타 · 패드. 8 마디마다 A/B 를 바꿔 지루하지 않게
  챕터 첫 마디    올림 — 스탭 · 드럼 Chorus
  엔드 카드       코러스 — 전부 + 리드 기타, 마지막 2 마디 페이드
"""
import sys, json, pathlib, numpy as np, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import music as MU                       # loop(), BAR, SR
import assemble2 as A

SR, BAR = MU.SR, MU.BAR
segs = A.times(); total = segs[-1]["end"]; nb = int(np.ceil(total / 2.0)) + 1
D = {"intro": "Disco Swagger Beat 02", "verse": "Disco Swagger Beat 01", "bridge": "Disco Swagger Beat 02", "chorus": "Doubledown Beat 01", "outro": "Disco Swagger Beat 02"}
BASS, RG, PAD, STAB, LEAD = "Road Trip Summer Bass", "Road Trip Summer Guitar", "Road Trip Summer Synth", "Road Trip Summer Synth", "Road Trip Summer Guitar"     # 17편: road-trip(music/styles.py) — 9~16편과 겹치지 않게

def bar_of(t): return int(round(t / 2.0))
# 2026-11-02 사용자: 「배경음악이 끊겼다 다시 재생되는 느낌」 — 마디마다 줄을 갈아 끼우지 않고, 줄마다 처음부터 끝까지 이어서 깔고
# 크기만 천천히(1 마디에 걸쳐) 바꾼다. 8 마디 A/B 교대 · 챕터 첫 마디 올림은 뺐다.
title_end = bar_of(A.TITLE); end_b = bar_of(segs[-1]["start"])
LEVEL = {   # 줄 → (타이틀, 본편, 엔드) dB · None = 그 구간엔 없음
 D["verse"]: (-6, -13, -6), BASS: (-4, -7, -4), RG: (None, -10, -7), PAD: (-9, -12, -9), STAB: (-6, -16, -7), LEAD: (None, None, -9)}
N = nb * BAR; mix = np.zeros((N, 2), np.float32)
idx = np.arange(N)
for name, (a, b_, c) in LEVEL.items():
    Lp = MU.loop(name); x = Lp[idx % len(Lp)]
    g = np.full(nb, -90.0)
    for bb in range(nb):
        v = a if bb < title_end else (b_ if bb < end_b else c)
        if v is not None: g[bb] = v
    gb = np.repeat(g, BAR)                                       # 마디 단위 계단 → 1 마디 이동 평균으로 매끈하게
    k = BAR; gb = np.convolve(np.pad(gb, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
    mix += x * (10 ** (gb / 20))[:, None].astype(np.float32)
fi = int(0.3 * SR); mix[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
mix = np.tanh(mix * 1.05) / 1.05

# 덕킹 — 목소리 구간에서 −8 dB (들어갈 때 0.12 s, 나올 때 0.45 s)
t = np.arange(N) / SR; g_db = np.zeros(N, np.float32)
# 덜 민감하게(7편부터): 2.5 s 보다 짧은 쉼은 낮춘 채로 잇는다
iv = sorted([(max(0, l["t"] - 0.08), l["t"] + l["dur"] + 0.15) for s in segs for l in s["lines"]]); mg = []
for a0, b0 in iv:
    if mg and a0 - mg[-1][1] < 2.5: mg[-1][1] = max(mg[-1][1], b0)
    else: mg.append([a0, b0])
for a0, b0 in mg: g_db[int(a0 * SR): int(b0 * SR)] = -8.0
k_att, k_rel = int(0.12 * SR), int(1.5 * SR)
sm = np.copy(g_db)
for i in range(1, N):                                          # 한쪽 방향 평활(빠르게 내려가고 천천히 올라온다)
    d = g_db[i] - sm[i - 1]
    sm[i] = sm[i - 1] + d / (k_att if d < 0 else k_rel)
mix *= (10 ** (sm / 20))[:, None]
# 끝 2 마디 페이드, 길이 맞춤, 크기(바닥 −21 dBFS 근처)
fo = 2 * BAR; mix[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
mix = mix[: int(total * SR)]
body = mix[int(A.TITLE * SR): int(segs[-1]["start"] * SR)]
cur = 20 * np.log10(np.sqrt(np.mean(body ** 2)) + 1e-9); mix *= 10 ** ((-25.0 - cur) / 20)
peak = np.abs(mix).max()
if peak > 0.89: mix *= 0.89 / peak
sf.write(HERE / "audio" / "music-ep17.wav", mix.astype(np.float32), SR)
def r(a, b): x = mix[int(a * SR): int(b * SR)]; return round(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9), 1)
print(f"music {total:.1f}s | title {r(0, A.TITLE)} dBFS | body {r(A.TITLE, segs[-1]['start'])} | end {r(segs[-1]['start'], total)} | peak {20*np.log10(np.abs(mix).max()):.1f}")
