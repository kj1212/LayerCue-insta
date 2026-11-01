#!/usr/bin/env python3
"""테 점검 — 완성 영상(render/final.mp4)에서 테마다 그 자리를 원래 해상도로 잘라 본다.
    python3 audit_hl.py ep09            → epNN/qa/hlcheck/NN-a.png(뜬 직후) · NN-b.png(사라지기 직전) · sheet*.png
테는 카드(창 녹화)의 자식이라, 카드의 확대 상태(TL.card.keys)로 화면 자리를 계산해 그 둘레를 자른다.
작은 썸네일로 보면 테가 엉뚱한 자리에 있어도 모른다(9편 Show/Edit) — 반드시 이걸로 본다.
"""
import json, subprocess, sys, pathlib
ep = sys.argv[1]; E = pathlib.Path(__file__).resolve().parent / ep
TL = json.loads((E / "timeline2.js").read_text()[8:-2])
keys = TL["card"]["keys"]
def state(t):
    if t <= keys[0][0]: return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / max(1e-6, b[0] - a[0])
            return [a[i] + (b[i] - a[i]) * f for i in (1, 2, 3)]
    return keys[-1][1:]
out = E / "qa" / "hlcheck"; out.mkdir(parents=True, exist_ok=True)
for p in out.glob("*.png"): p.unlink()
rows = []
for i, h in enumerate(TL["hls"]):
    if h["parent"] != "card": continue
    x, y, w, hh = h["rect"]
    for tag, t in (("a", min(h["t0"] + 0.75, (h["t0"] + h["t1"]) / 2)), ("b", h["t1"] - 0.3)):
        s, X, Y = state(t)
        cx, cy, cw, ch = X + x * s, Y + y * s, w * s, hh * s
        pad = 140
        x0 = max(0, int(cx - pad)); y0 = max(0, int(cy - pad)); x1 = min(3840, int(cx + cw + pad)); y1 = min(2160, int(cy + ch + pad))
        f = out / f"{i:02d}-{tag}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(E / "render" / "final.mp4"), "-frames:v", "1", "-update", "1",
                        "-vf", f"crop={x1-x0}:{y1-y0}:{x0}:{y0},scale=w=760:h=430:force_original_aspect_ratio=decrease,pad=760:430:0:0:color=0x303030", str(f)])
        rows.append((i, tag, round(t, 2), h["rect"]))
fs = sorted(out.glob("??-?.png"))
for part in range(0, len(fs), 8):
    sub = [str(f) for f in fs[part:part + 8]]
    while len(sub) % 2: sub.append(sub[-1])
    args = sum([["-i", f] for f in sub], [])
    fc = "".join(f"[{k}]" for k in range(len(sub))) + f"xstack=inputs={len(sub)}:layout=" + "|".join(f"{(k % 2) * 764}_{(k // 2) * 434}" for k in range(len(sub)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", fc, "-frames:v", "1", "-update", "1", str(out / f"sheet{part // 8}.png")])
for r in rows[::2]: print(r[0], r[2], r[3])
print("sheets:", len(fs) // 8 + (1 if len(fs) % 8 else 0))
