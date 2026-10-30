#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
# 점검용: try.py click 547 190 | key 53 | move x y  (좌표 = 3편 녹화 꼴 px, 위 60 포함)
import os, sys, pathlib
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
