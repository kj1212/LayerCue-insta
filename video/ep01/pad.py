#!/usr/bin/env python3
"""튜토리얼용 배경 패드 — 받은 음원 없이 numpy 로 합성한다. 선율·박자 없이 천천히 바뀌는 화음 패드라 5분 내내 깔아도 귀에 안 걸린다.

    ~/Documents/AIvoice/.venv/bin/python ep01/pad.py 312   → ep01/audio/pad-312s.wav (48 kHz 스테레오, RMS −24 dBFS)

화음은 Ⅰ–Ⅵ–Ⅳ–Ⅴ 를 24초마다 아주 느린 크로스페이드로 — 각 음은 사인 3배음 + 아주 느린 비브라토, 위에 걸러 낸 잡음이 숨결처럼 얇게.
"""
import sys, numpy as np, soundfile as sf

SR = 48000
sec = float(sys.argv[1]) if len(sys.argv) > 1 else 312
n = int(sec * SR); t = np.arange(n) / SR
rng = np.random.default_rng(7)

# D major-ish pad, 저음역: D3 F#3 A3 / B2 D3 F#3 / G2 B2 D3 / A2 C#3 E3
CHORDS = [[146.83, 185.00, 220.00, 293.66], [123.47, 146.83, 185.00, 246.94],
          [98.00, 123.47, 146.83, 196.00], [110.00, 138.59, 164.81, 220.00]]
STEP = 24.0


def tone(f):
    v = 1 + 0.004 * np.sin(2 * np.pi * 0.11 * t + rng.uniform(0, 6.28))          # 아주 느린 비브라토
    ph = 2 * np.pi * np.cumsum(f * v) / SR
    return np.sin(ph) + 0.35 * np.sin(2 * ph + 0.3) + 0.12 * np.sin(3 * ph + 0.7)


mix = np.zeros(n)
for i, ch in enumerate(CHORDS):
    # 이 화음이 울리는 창: i*STEP 마다 돌아오며 6초 걸쳐 들어오고 나간다
    env = np.zeros(n)
    for k in range(int(sec // (STEP * len(CHORDS))) + 2):
        s = (k * len(CHORDS) + i) * STEP
        a = np.clip((t - s) / 6.0, 0, 1); b = np.clip((s + STEP + 6.0 - t) / 6.0, 0, 1)
        env = np.maximum(env, np.minimum(a, b))
    env = np.sin(env * np.pi / 2)
    for f in ch:
        mix += tone(f) * env * (0.9 if f < 160 else 0.6)

# 숨결 — 저역만 남긴 잡음, 느리게 숨쉬듯
noise = rng.standard_normal(n)
k = np.ones(400) / 400
for _ in range(3):                      # 상자 필터 세 번 — 한 번으로는 고역이 남아 쉭쉭거렸다
    noise = np.convolve(noise, k, mode="same")
breath = 0.5 + 0.5 * np.sin(2 * np.pi * t / 17.0)
mix += noise * breath * 40.0

# 들어오기·나가기 3초, RMS 맞추기
fade = np.minimum(np.clip(t / 3.0, 0, 1), np.clip((sec - t) / 3.0, 0, 1))
mix *= fade
mix /= np.sqrt(np.mean(mix ** 2)) + 1e-9
mix *= 10 ** (-24 / 20)
right = np.concatenate([np.zeros(int(0.011 * SR)), mix[: n - int(0.011 * SR)]])   # 살짝 넓게
out = np.stack([mix, right], axis=1).astype(np.float32)
import pathlib; pathlib.Path("ep01/audio").mkdir(parents=True, exist_ok=True)
sf.write(f"ep01/audio/pad-{int(sec)}s.wav", out, SR)
print("pad", sec, "s, peak", round(20 * np.log10(np.abs(out).max() + 1e-9), 1), "dBFS")
