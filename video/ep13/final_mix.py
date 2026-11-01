#!/usr/bin/env python3
"""13편 최종 소리 — 목소리 + 앱이 실제로 낸 소리(구간마다 rec/v2/sN.wav, tools/appaudio) + 배경음악(타이틀·엔드 카드만).
    ~/Documents/AIvoice/.venv/bin/python ep13/final_mix.py [edge_db=-4] [app_db=0] [app_duck_db=-13]  → ep13/qa/v2-mix.wav

앱 소리 자리: 녹화 시계 c(t0 부터) 의 일이 타임라인 seg.start − PRE + c 에 놓인다(영상과 같은 식, rec_t0 와 무관).
wav 의 a 초 = 시계 offset + a(offset = audio.json). 음악이 이 편의 주인공이라 본편 배경음악은 끄고,
내레이션이 나오는 동안만 앱 소리를 낮춘다 — 1.5 s 넘게 쉬면(말소리 인트로 · 환영 영상 · 팡파르) 제 크기로 올라온다.
"""
import sys, json, numpy as np, soundfile as sf, scipy.signal as ss
edge_db = float(sys.argv[1]) if len(sys.argv) > 1 else -4.0
app_db = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
app_duck = float(sys.argv[3]) if len(sys.argv) > 3 else -13.0
segs = json.load(open("ep13/times2.json")); SL = json.load(open("ep13/shotlist2.json")); PRE = SL["pre"]; SR = 48000
m, _ = sf.read("ep13/audio/music-ep13.wav"); N = len(m); t = np.arange(N) / SR
title_end = segs[0]["start"]; end_start = segs[-1]["start"]

def smooth(target, att, rel):
    sm = np.copy(target); a, r = att * SR, rel * SR
    for i in range(1, len(sm)):
        x = target[i] - sm[i - 1]; sm[i] = sm[i - 1] + x / (a if x < 0 else r)
    return sm

# 배경음악: 타이틀과 엔드 카드에서만(본편 −60 dB) — 1 s 로 넘어간다
g = np.full(N, -60.0); g[t < title_end] = edge_db; g[t > end_start] = edge_db
# 13편: 앱 소리가 없는 구간(s1 장치 고르기)에는 배경음악을 낮게 깐다
for s in segs:
    if s["id"] in ("s1", "s6"): g[(t >= s["start"]) & (t < s["end"] - 0.5)] = -12.0
k = int(1.0 * SR); g = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
# 배경음악도 내레이션 아래서 −9 dB(10편까지와 같다 — 엔드 카드의 다음 편 안내가 음악에 묻혔다). 2.5 s 보다 짧은 쉼은 낮춘 채, 1.5 s 에 걸쳐 올라온다
bv = sorted([(max(0, l["t"] - 0.1), l["t"] + l["dur"] + 0.2) for s_ in segs for l in s_["lines"]]); bm = []
for a0, b0 in bv:
    if bm and a0 - bm[-1][1] < 2.5: bm[-1][1] = max(bm[-1][1], b0)
    else: bm.append([a0, b0])
bd = np.zeros(N)
for a0, b0 in bm: bd[int(a0 * SR): int(b0 * SR)] = -9.0
mix = m * (10 ** ((g + smooth(bd, 0.1, 1.5)) / 20))[:, None]

# 앱 소리 — 구간마다 제자리에, 이음매 0.25 s 페이드
app = np.zeros((N, 2))
for s in segs:
    if s["id"] == "s9": continue
    w, wsr = sf.read(f"ep13/rec/v2/{s['id']}.wav"); off = json.load(open(f"ep13/rec/v2/{s['id']}.audio.json"))["offset"]
    if s["id"] == "s2":     # 13편: s2 는 스트리밍 소리가 녹음되지 않았다(재생이 녹음 뒤에 시작) — 무대에서 돈 1편 원본 소리를 s3 녹음과 맞춘 자리에(qa/s2fill.json)
        f2 = json.load(open("ep13/qa/s2fill.json")); ref, _ = sf.read("ep13/media/ep01-audio.wav")
        n0 = int(-f2["pos2"] * SR); w = np.zeros_like(w); w[n0:] = ref[: len(w) - n0] * f2["gain"]
    assert wsr == SR
    T0, T1 = s["start"] - 0.3, s["end"]
    i0, i1 = int(T0 * SR), min(N, int(T1 * SR))
    a0 = int((T0 - (s["start"] - PRE + off)) * SR)                # 이 구간 시작에 해당하는 wav 샘플
    seg = np.zeros((i1 - i0, 2)); lo = max(0, -a0); hi = min(i1 - i0, len(w) - a0)
    if hi > lo: seg[lo:hi] = w[a0 + lo: a0 + hi]
    f = int(0.25 * SR); r = np.linspace(0, 1, f)[:, None]; seg[:f] *= r; seg[-f:] *= r[::-1]
    app[i0:i1] += seg
# 내레이션 아래 덕킹(1.5 s 보다 짧은 쉼은 낮춘 채로)
iv = sorted([(max(0, l["t"] - 0.15), l["t"] + l["dur"] + 0.2) for s_ in segs for l in s_["lines"]]); mg = []
for a0, b0 in iv:
    if mg and a0 - mg[-1][1] < 1.5: mg[-1][1] = max(mg[-1][1], b0)
    else: mg.append([a0, b0])
d = np.full(N, app_db)
for a0, b0 in mg: d[int(a0 * SR): int(b0 * SR)] = app_db + app_duck
app *= (10 ** (smooth(d, 0.12, 0.5) / 20))[:, None]
mix += app
for s in segs:
    for l in s["lines"]:
        v, vsr = sf.read(f"ep13/audio/vo-heart/e13-{l['key']}.wav"); v = v if v.ndim == 1 else v.mean(1)
        v = ss.resample_poly(v, SR // 1000, vsr // 1000); i = int(l["t"] * SR); j = min(N, i + len(v)); mix[i:j] += v[: j - i, None]
pk = np.abs(mix).max()
if pk > 0.98: mix *= 0.98 / pk
sf.write("ep13/qa/v2-mix.wav", mix.astype(np.float32), SR)
db = lambda x: round(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9), 1)
print("app audio by segment:", {s["id"]: db(app[int(s["start"] * SR): int(s["end"] * SR)]) for s in segs if s["id"] != "s9"}, "| peak", round(20 * np.log10(pk), 1))
