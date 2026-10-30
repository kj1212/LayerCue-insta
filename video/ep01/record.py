#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""구간 하나를 녹화한다 — LG 화면(3840×2160) 을 screencapture 로 찍는 동안 정해진 시각에 마우스·MCP 동작을 보낸다.

    LC_SANDBOX=sandbox-ep01 ep01/record.py ep01/take/s03.json

take 파일:
  { "name": "s03", "sec": 42,
    "setup": [ {"mcp": [ {...commands...} ]}, {"mouse": ["click", x, y]} ],      # 녹화 전에 맞춰 둘 상태
    "actions": [ {"t": 2.0, "mouse": ["click", x, y]}, {"t": 5.5, "mcp": [ {...} ]}, {"t": 7, "mouse": ["hover", x, y]},
                 {"t": 9, "mouse": ["move", x, y]}, {"t": 11, "mouse": ["drag", x1, y1, x2, y2]}, {"t": 12, "key": [53]} ] }
좌표는 LG 화면 캡처 픽셀(3840×2160, 메뉴 막대 포함). 창 캡처 픽셀이면 y 에 60 을 더한다.
결과: ep01/rec/<name>.mov 와 ep01/rec/<name>.mouse.json (t=0 이 녹화 시작).
"""
import json, os, subprocess, sys, time, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import lc
from mouse import M

PRE = 1.2   # screencapture 가 실제로 찍기 시작하기까지의 여유 — 이 뒤를 t=0 으로 잡는다


def do(m, a):
    if "mouse" in a:
        op, *xy = a["mouse"]
        if op == "click": m.click(*xy)
        elif op == "dbl": m.double_click(*xy)
        elif op == "rclick": m.right_click(*xy)
        elif op == "hover": m.hover(*xy, stay=0)
        elif op == "move": m.move(*xy)
        elif op == "drag": m.drag(*xy)
        elif op == "jump": m.jump(*xy)
    if "mcp" in a:
        lc.call("run_commands", {"commands": a["mcp"]})
    if "key" in a:
        m.key(*a["key"])
    if "sleep" in a:
        time.sleep(a["sleep"])


def main(path):
    take = json.load(open(path))
    out = HERE / "rec"; out.mkdir(exist_ok=True)
    sub = out / os.environ.get("REC_SUB", "v2"); sub.mkdir(exist_ok=True)
    mov = sub / f"{take['name']}.mp4"; mov.unlink(missing_ok=True)
    m = M()
    for a in take.get("setup", []):
        do(m, a)
    time.sleep(0.8)
    # ffmpeg 로 LG 화면(Capture screen 1)을 처음부터 30 fps 고정으로 — screencapture 는 가변 프레임률이라 AE 가 시각을 잘못 읽었다
    rec = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "avfoundation", "-capture_cursor", os.environ.get("REC_CURSOR", "1"),
                            "-capture_mouse_clicks", "0", "-framerate", "30", "-pixel_format", "nv12", "-i", os.environ.get("REC_DEV", "3:none"),
                            "-t", str(take["sec"]), "-c:v", "h264_videotoolbox", "-b:v", "50M", "-pix_fmt", "yuv420p", "-r", "30", str(mov)],
                           stdin=subprocess.DEVNULL)
    time.sleep(PRE)
    t0 = time.time(); m.t0 = t0; m.mark("rec")
    for a in sorted(take.get("actions", []), key=lambda a: a["t"]):
        time.sleep(max(0, a["t"] - (time.time() - t0)))
        do(m, a)
    rec.wait()
    m.save(sub / f"{take['name']}.mouse.json")
    print("rec", mov.name, round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main(sys.argv[1])
