#!/usr/bin/env python3
"""녹화하는 동안 층을 차례로 올린다 — LayerCue 의 실제 페이드가 그대로 담기게.

    python3 record_seq.py   → shots/rec/seq-stack.mov (10 s) · shots/rec/seq-next.mov (5 s)

seq-stack: 0.4 s 배경 → 2.4 s 글 → 4.2 s 로고 → 5.4 s 이름 띠
seq-next : 전부 떠 있는 데서 1.5 s 에 글만 다음 장
"""
import subprocess, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lc

OUT = pathlib.Path(__file__).parent / "shots" / "rec"


def cmd(*c):
    lc.call("run_commands", {"commands": list(c)})


def pt(name, n=1):
    return [{"op": "usePt", "name": name}, {"op": "present", "n": n}]


def record(name, sec, plan):
    """plan = [(초, 명령들), …] — 녹화를 걸어 두고 그 시각마다 보낸다(다리 하나 부르는 데 ~0.1 s)."""
    f = OUT / f"{name}.mov"; f.unlink(missing_ok=True)      # screencapture 는 있는 파일에 덮어쓰지 못한다
    rec = subprocess.Popen(["screencapture", "-x", "-v", "-V", str(sec), "-D", "2", str(f)])
    t0 = time.time()
    for at, cmds in plan:
        time.sleep(max(0, at - (time.time() - t0)))
        cmd(*cmds)
    rec.wait()
    print("rec", name)


cmd({"op": "output", "on": True}, {"op": "clear", "layer": "all"}); time.sleep(2)
record("seq-stack", 10, [(0.4, pt("Stage loop")), (2.4, pt("Welcome")), (4.2, pt("Event logo")), (5.4, pt("Lower third"))])
time.sleep(0.5)
record("seq-next", 5, [(1.5, pt("Welcome", 2))])
cmd({"op": "clear", "layer": "all"})
print("done")
