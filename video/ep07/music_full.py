#!/usr/bin/env python3
"""1편 전곡 — GarageBand 루프(Disco Pop 묶음 + Duncan 드럼, 120 BPM)를 times2(줄별 시각)에 맞춰 쌓고, 목소리 밑에서 덕킹까지 끝낸다.

    ~/Documents/AIvoice/.venv/bin/python ep01/music_full.py   → ep01/audio/music-ep07.wav (48 kHz 스테레오)

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
D = {k: "Throwback Funk Beat 02" for k in ("intro", "verse", "bridge", "chorus", "outro")}     # 7편: Throwback/Electric Funk 브라스·신스
BASS, RG, PAD, STAB, LEAD = "Throwback Funk Synth Bass", "Electric Funk Guitar 01", "Disco Pop Synth Pad", "Electric Funk Synth Stabs", "Throwback Funk Brass 01"

def bar_of(t): return int(round(t / 2.0))
plan = {}                                   # 마디 → {루프: dB}
title_end = bar_of(A.TITLE)
for b in range(0, title_end): plan[b] = {D["intro"] if b < title_end - 1 else D["chorus"]: -5, STAB: -6, BASS: -4, PAD: -9}
chap_bars = {bar_of(s["start"]) for s in segs if s["id"] not in ("s1", "s9")}
end_b = bar_of(segs[-1]["start"])
for b in range(title_end, end_b):
    k = ((b - title_end) // 8) % 2
    bed = {D["verse"]: -13, BASS: -7, RG: -10, PAD: -12} if k == 0 else {D["bridge"]: -14, BASS: -7, STAB: -13, PAD: -11}
    if b in chap_bars: bed = {D["chorus"]: -9, BASS: -6, STAB: -8, PAD: -10, RG: -10}
    plan[b] = bed
for b in range(end_b, nb): plan[b] = {D["chorus"] if b < nb - 2 else D["outro"]: -5, BASS: -4, RG: -7, STAB: -7, PAD: -9, LEAD: -9}

# 마디마다 루프를 위상 맞춰 붙인다(0 마디 기준)
N = nb * BAR; mix = np.zeros((N, 2), np.float32); cache = {}
for b, stems in plan.items():
    s0, s1 = b * BAR, (b + 1) * BAR
    for name, db in stems.items():
        if name not in cache: cache[name] = MU.loop(name)
        Lp = cache[name]; seg = Lp[np.arange(s0, s1) % len(Lp)] * (10 ** (db / 20))
        f = 240; r = np.linspace(0, 1, f, dtype=np.float32)[:, None]
        prev = plan.get(b - 1, {}); nxt = plan.get(b + 1, {})
        if name not in prev: seg[:f] *= r                      # 새로 들어오는 줄만 살짝 연다(이어지는 줄은 이음매 없이)
        if name not in nxt: seg[-f:] *= r[::-1]
        mix[s0:s1] += seg
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
sf.write(HERE / "audio" / "music-ep07.wav", mix.astype(np.float32), SR)
def r(a, b): x = mix[int(a * SR): int(b * SR)]; return round(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9), 1)
print(f"music {total:.1f}s | title {r(0, A.TITLE)} dBFS | body {r(A.TITLE, segs[-1]['start'])} | end {r(segs[-1]['start'], total)} | peak {20*np.log10(np.abs(mix).max()):.1f}")
