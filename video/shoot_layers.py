#!/usr/bin/env python3
"""기본 소개 쇼츠 — 촬영용 LayerCue 의 4K 무대를 층 조합마다 찍는다.

    $VENV/bin/python shoot_layers.py   → shots/layers/*.png (3840×2160)

쌓기: 0 빈 무대 · 1 배경 · 2 +글 · 3 +로고 · 4 +이름 띠 · 5 글만 다음 장
떼어 보기(3D 분리용): only-bg · only-fg · only-logo · only-lt
화면별(멀티 스크린): audience=전부 · stage=글만 · lobby=배경+로고
"""
import sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lc, shoot

OUT = pathlib.Path(__file__).parent / "shots" / "layers"
OUT.mkdir(parents=True, exist_ok=True)
shoot.OUT = OUT


def c(*cmds):
    lc.call("run_commands", {"commands": list(cmds)}); time.sleep(1.3)


def pt(name, n=1):
    return [{"op": "usePt", "name": name}, {"op": "present", "n": n}]


lc.call("run_commands", {"commands": [{"op": "output", "on": True}]}); time.sleep(2.5)
main, stage = shoot.windows()
print("windows", main, stage)
g = lambda name: shoot.grab(stage, name)

c({"op": "clear", "layer": "all"}); g("0-empty")
c(*pt("Stage background")); g("1-bg")
c(*pt("Welcome")); g("2-bg-fg")
c(*pt("Event logo")); g("3-bg-fg-logo")
c(*pt("Lower third")); g("4-all")
shoot.grab(main, "app-all")
c(*pt("Welcome", 2)); g("5-all-next")

# 떼어 보기
for name, layer in [("only-bg", "Stage background"), ("only-fg", "Welcome"), ("only-logo", "Event logo"), ("only-lt", "Lower third")]:
    c({"op": "clear", "layer": "all"}); c(*pt(layer)); g(name)

# 화면별 — 객석은 4-all 과 같다
c({"op": "clear", "layer": "all"}); c(*pt("Stage background")); c(*pt("Event logo")); g("lobby")
c({"op": "clear", "layer": "all"}); c(*pt("Welcome")); g("stage-words")
c({"op": "clear", "layer": "all"})
print("done")
