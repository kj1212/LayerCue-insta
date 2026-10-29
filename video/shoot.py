#!/usr/bin/env python3
"""촬영용 LayerCue 에서 장면 그림을 받는다 — 창 하나씩(screencapture -l), 메뉴 막대·다른 앱은 안 찍힌다.

    $VENV/bin/python shoot.py      (pyobjc Quartz 가 있는 파이썬)

shots/main-*.png  앱 창(레티나 2배)          shots/stage-*.png  4K 송출 창(3840×2160)
"""
import json, subprocess, sys, time, pathlib
import Quartz

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lc

OUT = pathlib.Path(__file__).parent / "shots"
OUT.mkdir(exist_ok=True)


def windows():
    main = stage = None
    for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID):
        if "LayerCue" not in (w.get("kCGWindowOwnerName") or ""):
            continue
        b = w["kCGWindowBounds"]
        if w.get("kCGWindowName") == "LayerCue" and w["kCGWindowLayer"] == 0:
            main = w["kCGWindowNumber"]
        elif b["Width"] == 3840 and b["Height"] == 2160:
            stage = w["kCGWindowNumber"]
    return main, stage


def grab(win, name):
    subprocess.run(["screencapture", "-x", "-o", "-l", str(win), str(OUT / f"{name}.png")], check=True)


def cmds(*c):
    lc.call("run_commands", {"commands": list(c)})
    time.sleep(1.2)          # 전환(크로스페이드)이 끝난 뒤에 찍는다


main, stage = windows()
print("windows", main, stage)

# 1) 처음 모습 — 라이브러리의 「Start here」, 아무것도 송출 안 함
cmds({"op": "clear", "layer": "all"})
grab(main, "main-01-library")

# 2) 큐시트 「Tour」를 연 모습
cmds({"op": "useCue", "name": "Tour"}, {"op": "usePt", "name": "Start here"}, {"op": "select", "n": 1})
grab(main, "main-02-cuesheet")

# 3) 첫 장을 송출 — 앱 창(LIVE 표시)과 4K 무대
cmds({"op": "present", "n": 1})
grab(main, "main-03-live")
grab(stage, "stage-start-here-1")

# 4) READ ME 의 장들을 무대에서 차례로 — 몽타주 재료
decks = json.loads(open(OUT.parent / "sandbox" / "decks.json").read())
for name, n in decks:
    for i in range(1, n + 1):
        cmds({"op": "usePt", "name": name}, {"op": "present", "n": i})
        grab(stage, f"stage-{name.lower().replace(' ', '-').replace('&', 'and')}-{i}")
    print("shot", name, n)

# 끝에 다시 첫 장으로 돌려 둔다
cmds({"op": "usePt", "name": "Start here"}, {"op": "present", "n": 1})
print("done")
