#!/usr/bin/env python3
"""기본 소개 쇼츠 — 움직이는 배경(Stage loop)이 깔린 4K 무대를 층 조합마다 4초씩 녹화한다.

    python3 record_layers.py   → shots/rec/*.mov (3840×2160 · 60 fps · 8 s)

배경이 움직여서 그림 한 장으로는 모자란다. 송출 창이 4K 모니터(-D 2)를 가득 채운다.
글·로고·이름 띠만 따로 뜬 것(3D 분리용)과 「무대 모니터=글만」은 움직임이 없어 shoot_layers.py 의 그림을 쓴다.
"""
import subprocess, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lc

OUT = pathlib.Path(__file__).parent / "shots" / "rec"
OUT.mkdir(parents=True, exist_ok=True)
SEC = 8      # 장면이 4 s 를 넘는다 — 4 s 로 찍었더니 화면 셋 장면에서 양옆이 먼저 꺼졌다


def c(*cmds):
    lc.call("run_commands", {"commands": list(cmds)}); time.sleep(1.4)   # 크로스페이드가 끝난 뒤


def pt(name, n=1):
    return [{"op": "usePt", "name": name}, {"op": "present", "n": n}]


def rec(name):
    f = OUT / f"{name}.mov"; f.unlink(missing_ok=True)      # screencapture 는 있는 파일에 덮어쓰지 못한다
    subprocess.run(["screencapture", "-x", "-v", "-V", str(SEC), "-D", "2", str(f)], check=True)
    print("rec", name)


lc.call("run_commands", {"commands": [{"op": "output", "on": True}]}); time.sleep(2)
c({"op": "clear", "layer": "all"}); c(*pt("Stage loop")); rec("1-bg")
c(*pt("Welcome")); rec("2-bg-fg")
c(*pt("Event logo")); rec("3-bg-fg-logo")
c(*pt("Lower third")); rec("4-all")
c(*pt("Welcome", 2)); rec("5-all-next")
c({"op": "clear", "layer": "all"}); c(*pt("Stage loop")); c(*pt("Event logo")); rec("lobby")
c({"op": "clear", "layer": "all"})
print("done")
