#!/usr/bin/env python3
"""19편: 상태 막대의 한국어 기기 이름(「MacBook Pro 스…」)을 영어 패치(ep12/patch/status.png)로 덮는다.
   0.9.14 는 보기(Show)·편집(Edit)에서 자리가 다르다 — 프레임마다 Edit 단추가 켜졌는지(파랑)로 고른다. 원본은 rec/v2/orig/.
    ../.venv/bin/python patch_dev.py s1 s2 …"""
import subprocess, sys, pathlib, numpy as np
H = pathlib.Path(__file__).resolve().parent; R = H / "rec" / "v2"; PATCH = H.parent / "ep12" / "patch" / "status.png"
SHOW_X, EDIT_X, Y = 1272, 1548, 2104
def edit_lit(src):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-vf", "crop=6:6:206:2114,scale=1:1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = np.frombuffer(r, np.uint8).reshape(-1, 3).astype(int); return (a[:, 2] > 150) & (a[:, 0] < 140)
def runs(mask):
    out, s = [], None
    for i, m in enumerate(list(mask) + [None]):
        if s is None and m is not None: s, v = i, m
        elif m != v or m is None:
            out.append((s, i - 1, v)); s, v = (i, m) if m is not None else (None, None)
    return out
for take in sys.argv[1:]:
    (R / "orig").mkdir(exist_ok=True); src = R / "orig" / f"{take}.mp4"
    if not src.exists(): (R / f"{take}.mp4").replace(src)
    lit = edit_lit(src)
    k = 5; sm = np.convolve(lit.astype(float), np.ones(k) / k, mode="same") > 0.5     # 몇 프레임 흔들림은 무시
    rs = runs(list(sm))
    en_show = "+".join(f"between(n,{a},{b})" for a, b, v in rs if not v) or "0"
    en_edit = "+".join(f"between(n,{a},{b})" for a, b, v in rs if v) or "0"
    fl = f"[1:v]split[p1][p2];[0:v][p1]overlay={SHOW_X}:{Y}:enable='{en_show}':shortest=1[a];[a][p2]overlay={EDIT_X}:{Y}:enable='{en_edit}'"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-loop", "1", "-i", str(PATCH), "-filter_complex", fl + ":shortest=1",
                    "-c:v", "h264_videotoolbox", "-b:v", "50M", "-pix_fmt", "yuv420p", "-r", "30", str(R / f"{take}.mp4")], check=True)
    print("patched", take, [(a, b, "edit" if v else "show") for a, b, v in rs])
