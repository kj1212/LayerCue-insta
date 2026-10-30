#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""녹화 시각 보정 — record.py 의 t=0 이 영상 파일의 몇 초에 해당하는지 잰다.

    LC_SANDBOX=sandbox-ep01 ep01/calib.py
t=1.0 에 슬라이드를 송출하고(타일 미리보기가 검정에서 밝아진다), 영상의 0.6–2.4 s 를 0.05 s 마다 읽어 미리보기 밝기가 처음 오르는 시각을 찾는다.
"""
import json, subprocess, sys, pathlib
import AVFoundation, CoreMedia, Quartz, Foundation
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); import lc

take = {"name": "calib", "sec": 4, "setup": [{"mcp": [{"op": "clear", "layer": "all"}, {"op": "useCue", "name": "Summit Day 1"}, {"op": "openCue", "name": "Summit Day 1"}]}],
        "actions": [{"t": 1.0, "mcp": [{"op": "usePt", "name": "Welcome words"}, {"op": "present", "n": 1}]}]}
p = HERE / "take" / "calib.json"; p.parent.mkdir(exist_ok=True); json.dump(take, open(p, "w"))
subprocess.run([str(HERE / "record.py"), str(p)], check=True)
lc.call("run_commands", {"commands": [{"op": "clear", "layer": "all"}]})

mov = str(HERE / "rec" / "calib.mov")
asset = AVFoundation.AVURLAsset.alloc().initWithURL_options_(Foundation.NSURL.fileURLWithPath_(mov), None)
gen = AVFoundation.AVAssetImageGenerator.alloc().initWithAsset_(asset)
gen.setRequestedTimeToleranceBefore_(CoreMedia.kCMTimeZero); gen.setRequestedTimeToleranceAfter_(CoreMedia.kCMTimeZero)
gen.setMaximumSize_(Foundation.NSMakeSize(960, 960))      # 1/4 크기 — 미리보기 영역(창 px 445,138 642×365 → 화면 y+60) 은 4 로 나눈다
X0, Y0, X1, Y1 = 445 // 4, (138 + 60) // 4, (445 + 642) // 4, (138 + 60 + 365) // 4


def brightness(sec):
    res = gen.copyCGImageAtTime_actualTime_error_(CoreMedia.CMTimeMakeWithSeconds(sec, 600), None, None)
    img = res[0] if isinstance(res, tuple) else res
    actual = CoreMedia.CMTimeMakeWithSeconds(sec, 600)
    if img is None: return None, None
    w, h = Quartz.CGImageGetWidth(img), Quartz.CGImageGetHeight(img)
    bpr = Quartz.CGImageGetBytesPerRow(img)
    data = bytes(Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(img)))
    tot = n = 0
    for y in range(Y0, min(Y1, h), 4):
        row = y * bpr
        for x in range(X0, min(X1, w), 4):
            o = row + x * 4; tot += data[o] + data[o + 1] + data[o + 2]; n += 3
    return tot / n, CoreMedia.CMTimeGetSeconds(actual)


base = None; first = None
t = 0.4
while t <= 2.6:
    b, at = brightness(t)
    if b is None: break
    if base is None: base = b
    print(f"{t:4.2f}s  brightness {b:6.1f}")
    if first is None and b > base + 6: first = t
    t = round(t + 0.05, 2)
print("preview brightens at", first, "s in the file; action was sent at t=1.0 (+~0.1 s bridge) → file time of t=0 ≈", round(first - 1.1, 2) if first else None)
