#!/usr/bin/env python3
"""15편 s5: Claude 가 Day 1 에 슬라이드를 더할 때까지 기다렸다가(8 장), 잠시 뒤 되돌린다(MCP undo = ⌘Z 와 같은 한 단계).
   시각은 qa/s5-wait.json 에 남긴다(녹화를 자를 자리)."""
import sys, time, json, pathlib
H = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(H.parent)); import lc
t0 = time.time(); seen = None
while time.time() - t0 < 300:
    r = lc.call("get_slides", {"presentation": "Day 1"})
    try: n = json.loads(r["result"]["content"][0]["text"])["presentation"]["slides"]
    except Exception: n = 0
    if n >= 8: seen = time.time(); break
    time.sleep(0.5)
time.sleep(float(sys.argv[1]) if len(sys.argv) > 1 else 5.0)
undo = time.time(); lc.call("undo", {})
json.dump({"appear_epoch": seen, "undo_epoch": undo, "start_epoch": t0}, open(H / "qa" / "s5-wait.json", "w"))
