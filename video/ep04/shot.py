#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""촬영용 LayerCue 의 창 그림 — ep01/shots/<name>.png (3840×2100, 창만). 보기용 작은 판도 같이(_s.png, 1600 너비).

    ep01/shot.py <name>            창을 찍는다
    ep01/shot.py <name> x,y,w,h    창 그림의 그 부분(픽셀)을 잘라 2배로 키워 _z.png 로도 둔다
"""
import subprocess, sys, pathlib
import Quartz

OUT = pathlib.Path(__file__).resolve().parent / "shots"
OUT.mkdir(exist_ok=True)


def win_id():
    for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID):
        if "LayerCue" in (w.get("kCGWindowOwnerName") or "") and w.get("kCGWindowName") == "LayerCue" and w["kCGWindowLayer"] == 0:
            return w["kCGWindowNumber"]
    raise SystemExit("LayerCue window not found")


def grab(name, crop=None):
    f = OUT / f"{name}.png"
    subprocess.run(["screencapture", "-x", "-o", "-l", str(win_id()), str(f)], check=True)
    subprocess.run(["sips", "-Z", "1600", str(f), "--out", str(OUT / f"{name}_s.png")], check=True, capture_output=True)
    if crop:
        x, y, w, h = crop
        z = OUT / f"{name}_z.png"
        subprocess.run(["sips", "-c", str(h), str(w), "--cropOffset", str(y), str(x), str(f), "--out", str(z)], check=True, capture_output=True)
    return f


if __name__ == "__main__":
    crop = tuple(int(v) for v in sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    print(grab(sys.argv[1], crop))
