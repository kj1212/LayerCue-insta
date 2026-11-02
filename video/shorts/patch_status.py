#!/usr/bin/env python3
"""상태 막대의 한국어 기기 이름(「System default · MacBook Pro 스…」)을 영어 패치로 덮는다 — 프레임마다 상자 바탕 밝기를 재서
   창이 어두워진 동안(설정 창 · 대화 상자)은 그만큼 어둡게 한 패치를, 상자가 안 보이면(바탕이 다르면) 덮지 않는다.
    ~/Documents/AIvoice/.venv/bin/python shorts/patch_status.py ep11/rec/v2/s1.mp4 …   (원본은 rec/v2/orig/ 에 남긴다)
패치: ep12/patch/status.png(배경 37, 글 248 — 12편 make.mjs). 자리: 캡처 (1272, 2104).
"""
import sys, subprocess, pathlib, shutil, numpy as np
V = pathlib.Path(__file__).resolve().parent.parent
PATCH = V / "ep12" / "patch" / "status.png"
X, Y, W, H = 1272, 2104, 72, 36
def frames_bg(path):
    # 상자 위쪽 여백(글 없는 곳) 2×2 의 평균 — 프레임마다
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "crop=4:4:1300:2100,format=gray,scale=1:1", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).astype(int)
def text_level(path):
    # 「MacBook Pro」 글자의 가장 밝은 값 — 어둡게 덮인 정도가 상자 바탕과 다를 수 있어 글은 글대로 잰다
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "crop=110:22:1150:2112,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).reshape(-1, 22, 110).max(axis=(1, 2)).astype(int)
def text_check(path, n):
    # 스… 가 있는지: 패치 자리 오른쪽 끝(1330–1344)에 밝은 글 픽셀이 있어야 한다
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"crop=60:24:{X+4}:{Y+6},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(r, np.uint8).reshape(-1, 24, 60)
    return a.max(axis=(1, 2))
def runs(mask):
    out, s = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and s is None: s = i
        if not m and s is not None: out.append((s, i - 1)); s = None
    return out
def main(p):
    p = (V / p) if not pathlib.Path(p).is_absolute() else pathlib.Path(p)
    orig = p.parent / "orig" / p.name; orig.parent.mkdir(exist_ok=True)
    src = p.parent / (p.stem + ".pre-status.mp4")
    if not orig.exists(): shutil.copy(p, orig)
    shutil.copy(p, src)
    bg = frames_bg(src); tx = text_check(src, len(bg)); tl = text_level(src)
    n = min(len(bg), len(tx), len(tl)); bg, tx, tl = bg[:n], tx[:n], tl[:n]
    # 바탕이 18–40 이고 글이 보이는 프레임만. 밝기 단계(2 단위)마다 패치 하나
    ok = (bg >= 5) & (bg <= 40) & (tx > bg + 15)
    levels = {}
    for i in np.flatnonzero(ok): levels.setdefault((max(6, int(round(bg[i] / 2) * 2)), int(round(tl[i] / 6) * 6)), []).append(i)
    if not levels: print("skip (no status box)", p); src.unlink(); return
    ins, chain, k = ["-i", str(src)], "", 0; last = "0:v"
    for (lb, lt), idx in sorted(levels.items()):
        k += 1; g = (lt - lb) / (248 - 37)        # 패치 37→바탕 lb, 248→글 lt
        ins += ["-i", str(PATCH)]
        m = np.zeros(n, bool); m[idx] = True
        en = "+".join(f"between(n,{a},{b})" for a, b in runs(m))
        chain += f"[{k}:v]format=rgb24,lutrgb=r={lb}+(val-37)*{g:.4f}:g={lb}+(val-37)*{g:.4f}:b={lb}+(val-37)*{g:.4f}[p{k}];[{last}][p{k}]overlay={X}:{Y}:enable='{en}'[o{k}];"
        last = f"o{k}"
    script = p.parent / (p.stem + ".fc.txt"); script.write_text(chain.rstrip(";"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", str(script), "-map", f"[{last}]", "-c:v", "h264_videotoolbox", "-b:v", "50M", "-pix_fmt", "yuv420p", "-r", "30", str(p)], check=True)
    script.unlink(); src.unlink()
    print("patched", p.relative_to(V), f"{ok.sum()}/{n} frames, levels {sorted(levels)}")
if __name__ == "__main__":
    for a in sys.argv[1:]: main(a)
