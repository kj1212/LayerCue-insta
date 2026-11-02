#!/usr/bin/env python3
"""숏츠 표지 — 훅 두 줄을 가운데에(유튜브 숏츠 목록은 가운데만 보인다). 위 · 아래는 그 숏츠 2박의 창 · 확대 칸을 흐리게.
    python3 shorts/make_covers.py   → shorts/<id>/out/<id>-cover.jpg · short03/out/…-cover.jpg"""
import json, subprocess, pathlib
H = pathlib.Path(__file__).resolve().parent; V = H.parent; args = []
items = [("short03", "YOUR WHOLE SHOW.", "ONE WINDOW.", "01", V / "short03/out/short03-pick-click-watch-adjust.mp4", 10.5, V / "short03/out/short03-pick-click-watch-adjust-cover.jpg")]
for d in sorted(p for p in H.glob("s[0-9]*") if p.is_dir()):
    sp = json.load(open(d / "spec.json")); cfg = json.loads((d / "cfg.js").read_text()[10:].rstrip().rstrip(";"))
    items.append((sp["id"], sp["hook"][0], sp["hook"][1], f"{int(sp['ep']):02d}", d / "out" / f"{sp['id']}.mp4", cfg["beats"][1]["t"] + 1.6, d / "out" / f"{sp['id']}-cover.jpg"))
fr = H / "cover-src"; fr.mkdir(exist_ok=True)
for sid, a, b, ep, mp4, t, out in items:
    top, bot = fr / f"{sid}-top.png", fr / f"{sid}-bot.png"
    for crop, f in (("1000:547:40:347", top), ("1000:700:40:950", bot)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(mp4), "-frames:v", "1", "-vf", f"crop={crop}", str(f)], check=True)
    args += [sid, a, b, ep, str(top), str(bot), str(out)]
subprocess.run(["node", str(H / "covers.mjs"), *args], check=True, cwd=V)
