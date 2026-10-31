#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
# 점검용: try.py click 547 190 | key 53 | move x y  (좌표 = 3편 녹화 꼴 px, 위 60 포함)
import os, sys, pathlib, time, math
os.environ.setdefault("MOUSE_WIN", "60,110,1680,919")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from mouse import M
m = M(log=False); op = sys.argv[1]; a = [float(v) for v in sys.argv[2:]] if op != "type" else []
if op == "click": m.click(*a)
elif op == "rclick": m.right_click(*a)
elif op == "move": m.move(*a)
elif op == "key": m.key(int(a[0]))
elif op == "cmdkey": m.key(int(a[0]), cmd=True)
elif op == "type": m.type_text(" ".join(sys.argv[2:]))
elif op == "drag": m.drag(*a)
elif op == "rclick2": m.right_click(*a)
elif op == "slowdrag":
    x1,y1,x2,y2,hold = a
    m.move(x1,y1,0.6); time.sleep(0.15)
    import Quartz
    m._post(Quartz.kCGEventLeftMouseDown,x1,y1); time.sleep(0.2)
    n=120
    for i in range(1,n+1):
        s=i/n; s=0.5-0.5*math.cos(math.pi*s)
        m._post(Quartz.kCGEventLeftMouseDragged,x1+(x2-x1)*s,y1+(y2-y1)*s); time.sleep(1.0/n)
    for i in range(int(hold*30)):
        m._post(Quartz.kCGEventLeftMouseDragged,x2+(i%2),y2); time.sleep(1/30)
    m._post(Quartz.kCGEventLeftMouseUp,x2,y2)
elif op == "cmdclick": m.cmd_click(*a)
