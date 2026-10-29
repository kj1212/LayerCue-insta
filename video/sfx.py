#!/usr/bin/env python3
"""효과음 셋을 합성한다 — 받은 음원을 쓰지 않아 쓸 권리를 따질 것이 없다.

    ~/Documents/AIvoice/.venv/bin/python sfx.py   → music/sfx-whoosh.wav · sfx-tick.wav · sfx-thump.wav (48 kHz 스테레오)

whoosh  장면 전환 — 걸러 낸 잡음이 0.45 s 동안 차오르다 빠진다. 대역이 위로 쓸려 올라가서 「휙」.
tick    표·화면이 뜰 때 — 아주 짧은 맑은 딸깍.
thump   판이 갈라지고 붙을 때 — 낮은 음이 아래로 미끄러지며 사라진다.
전부 낮게 둔다(정점 −14 ~ −18 dBFS). 목소리를 덮으면 안 된다.
"""
import numpy as np
import soundfile as sf

SR = 48000
rng = np.random.default_rng(3)


def stereo(x, width=0.0):
    # width: 왼쪽·오른쪽을 아주 조금 다르게 — 가운데서 한 점으로 들리지 않게
    d = int(width * SR)
    l = x; r = np.concatenate([np.zeros(d), x[: len(x) - d]]) if d else x
    return np.stack([l, r], axis=1)


def norm(x, peak_db):
    return x / (np.abs(x).max() + 1e-9) * 10 ** (peak_db / 20)


def bandsweep(noise, f0, f1, q=1.6):
    # 짧은 창마다 대역을 옮겨 가며 거른다(FFT) — 「쓸려 올라가는」 느낌
    n = len(noise); out = np.zeros(n); win = 1024; hop = 256
    w = np.hanning(win)
    for s in range(0, n - win, hop):
        fc = f0 * (f1 / f0) ** (s / n)
        spec = np.fft.rfft(noise[s:s + win] * w)
        f = np.fft.rfftfreq(win, 1 / SR)
        g = np.exp(-0.5 * (np.log(f / fc + 1e-9) * q) ** 2)
        out[s:s + win] += np.fft.irfft(spec * g) * w
    return out


def whoosh(sec=0.6):
    n = int(sec * SR); t = np.arange(n) / SR
    x = bandsweep(rng.standard_normal(n), 300, 4200)
    env = np.where(t < sec * 0.7, (t / (sec * 0.7)) ** 2.2, np.exp(-(t - sec * 0.7) * 22))
    return norm(x * env, -16)


def tick(sec=0.09):
    n = int(sec * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 2300 * t) * 0.6 + np.sin(2 * np.pi * 4600 * t) * 0.25 + rng.standard_normal(n) * 0.08
    env = np.exp(-t * 70)
    return norm(x * env, -18)


def thump(sec=0.4):
    n = int(sec * SR); t = np.arange(n) / SR
    f = 150 * (55 / 150) ** (t / sec)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    env = (1 - np.exp(-t * 400)) * np.exp(-t * 9)
    return norm(x * env, -14)


for name, sig, wd in [("whoosh", whoosh(), 0.004), ("tick", tick(), 0.0), ("thump", thump(), 0.0)]:
    sf.write(f"music/sfx-{name}.wav", stereo(sig, wd).astype(np.float32), SR)
    print(name, round(len(sig) / SR, 2), "s")
