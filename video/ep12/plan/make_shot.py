#!/usr/bin/env python3
"""12편 연출표 — shotlist2.json · regions.json(줄 길이에 맞춰 '줄 끝 기준' 시각).   python3 ep12/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(위 60 포함), 영역은 창 px(= peek-s × 2.4).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
R = {
 "devbox": [908, 2030, 470, 58], "devlist": [958, 1764, 524, 276], "sysdef": [960, 1780, 520, 48],
 "meter": [1250, 94, 66, 474], "metercol": [1244, 88, 80, 604], "handle": [1248, 226, 72, 40],
 "mute": [1250, 568, 70, 38], "solo": [1250, 616, 70, 38], "dbval": [1242, 654, 86, 36],
 "musicspk": [1890, 640, 48, 46], "musiclist": [1351, 152, 782, 352], "fcell": [1112, 404, 56, 46],
 "ctlspk": [988, 640, 52, 46], "slidevol": [2392, 430, 420, 52], "stage": [447, 141, 646, 400],
 "z_status": [700, 1700, 1200, 420], "z_meter": [1150, 60, 1000, 680], "z_stagemusic": [430, 60, 1720, 680],
 "z_ctl": [430, 60, 2780, 700], "stagearea": [0, 0, 1, 1],
}
c = lambda x, y: ["click", x, y]
LOBBY, MUTE, SOLO, DBL, MSPK, VID, VIDLBL, SVOL, PLAY = c(1502, 312), c(1284, 646), c(1284, 693), ["dbl", 1284, 450], c(1914, 722), c(1488, 996), c(1488, 1133), c(2419, 514), c(483, 723)
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}, {"op": "music", "action": "stop"}]}, {"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 2, "at": 0.0, **Z("z_status", 2.0)},
   hl(2, 2.6, "devbox", "Audio device", "everything goes here", 2.4, "right"),
   hl(3, 2.2, "devbox", "Not connected", "the speaker turns orange", 4.4, "right"),
   {"line": 5, "at": 0.2, "mouse": c(1160, 2119)},
   hl(5, 1.0, "devlist", "System default", "or a device by name", 5.0, "right"),
   {"line": 6, "at": 0.1, "mouse": c(1197, 1863)},
   hl(6, 1.0, "devbox", "System default", "white speaker again", 1.6, "right"),
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_meter", 2.0)},
   {"line": 1, "at": 0.2, "mouse": LOBBY},
   hl(1, 1.8, "metercol", "The meter", "what LayerCue sends out", 3.2, "right"),
   hl(2, 0.2, "meter", "green · orange · red", "−20 · −9 dBFS", end("s2", 2, -0.2), "right"),
   hl(3, 0.2, "meter", "White line", "the average", end("s2", 3, -0.2), "right"),
   hl(4, 0.2, "handle", "Master", "starts at 0 dB", end("s2", 4, -0.2), "right"),
   {"line": 5, "at": 0.2, "mouse": ["drag", 1284, 305, 1284, 150]},
   hl(5, 1.3, "dbval", "+3.0 dB", "the top", 1.8, "right"),
   {"line": 5, "at": 2.0, "cap": "A red line across the very top = clipping · bring the master or that layer down", "capdur": 4.6},
   {"line": 6, "at": end("s2", 6, 1.1), "mouse": DBL},
   hl(6, end("s2", 6, 0.3), "dbval", "0.0 dB", "double-click", 1.4, "right"),
  ]},
 "s3": {"setup": [{"mouse": ["jump", 2600, 1500]}],    # 다시 찍을 때: ["dbl"], LOBBY 로 s2 끝 상태를 만든다(아래 RESHOOT)
  "events": [
   {"line": 1, "at": 0.0, **Z("z_meter", 2.0)},
   {"line": 1, "at": 0.3, "mouse": MUTE},
   hl(1, 1.1, "metercol", "MUTE", "still moving, dimmed", 4.6, "right"),
   {"line": 2, "at": 0.3, "mouse": MUTE},
   {"line": 3, "at": 0.3, "mouse": ["drag", 1284, 305, 1284, 624]},
   hl(3, 1.4, "metercol", "−∞ dB", "the meter drops", 2.6, "right"),
   {"line": 3, "at": end("s3", 3, 1.2), "mouse": DBL},
  ]},
 "s4": {"setup": [{"mcp": [{"op": "music", "action": "stop"}]}, {"sleep": 1.4}, {"mouse": MSPK}, {"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_meter", 2.0)},
   {"line": 1, "at": 0.8, "mouse": LOBBY},
   {"line": 2, "at": 0.3, "cap": "1 MUTE red? · 2 Master −∞? · 3 Meter moving? · 4 The layer · 5 The slide · 6 Music while video plays", "capdur": 15.0},
   hl(2, 1.6, "mute", "1 · MUTE red?", "no", 1.8, "right"),
   hl(2, 3.6, "dbval", "2 · −∞ dB?", "no, 0.0 dB", 2.2, "right"),
   hl(3, 0.2, "meter", "3 · Moving?", "yes", 2.4, "right"),
   hl(3, 2.9, "musicspk", "Music speaker", "off", 2.4, "below"),
   {"line": 4, "at": 0.4, "mouse": MSPK},
   hl(4, 1.1, "musicspk", "On", "the music is heard", 2.4, "below"),
   {"line": 5, "at": 0.0, "rest": True},
   hl(5, 0.6, "devbox", "The device", "Not connected?", 3.8, "right"),
  ]},
 "s5": {"setup": [{"mcp": [{"op": "music", "action": "stop"}]}, {"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 0.0, "rest": True},
   {"line": 1, "at": 0.2, "mouse": VID},
   {"line": 1, "at": 1.4, **Z("z_stagemusic", 1.7)},
   hl(1, 2.6, "meter", "Not moving", "", 2.0, "right"),
   hl(2, 3.2, "fcell", "4 · The layer", "F", 1.6, "right"),
   hl(2, 4.9, "ctlspk", "Speaker off", "control row", 2.0, "below"),
   {"line": 3, "at": 0.0, **Z("z_ctl", 1.3)},
   {"line": 3, "at": 0.1, "mouse": VIDLBL},
   hl(3, 1.6, "slidevol", "5 · Slide volume", "0%", 2.6, "below"),
   {"line": 4, "at": 0.2, "mouse": SVOL},
   hl(4, 0.9, "slidevol", "Saved", "with the slide", 3.4, "below"),
   {"line": 5, "at": 0.2, "mouse": PLAY},
   {"line": 5, "at": 0.8, **Z("z_stagemusic", 1.7)},
   hl(5, 1.4, "stage", "Heard", "the welcome speech", 5.6, "below"),
  ]},
 "s6": {"setup": [{"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_stagemusic", 1.7)},
   {"line": 1, "at": 0.1, "mouse": LOBBY},
   {"line": 1, "at": 1.3, "mouse": PLAY},
   {"line": 1, "at": 2.6, "mouse": SOLO},
   hl(2, 0.2, "meter", "Left: everything", "right: the foreground", end("s6", 2, -0.2), "right"),
   {"line": 3, "at": 1.6, "mouse": SOLO},
   {"line": 4, "at": 0.2, "cap": "Settings › General › Remember master volume — off: the master starts at 0 dB", "capdur": 6.0},
  ]},
}
# 다시 찍기(2026-11-01): s3 은 −∞ 까지 끌리지 않아서, s6 은 SOLO 설명 중 영상 목소리가 끝나서 — 따로 찍을 때 앞 구간 끝 상태를 setup 으로 만든다
import os
if os.environ.get("RESHOOT"):
    S["s3"]["setup"] = [{"mcp": [{"op": "music", "action": "stop"}, {"op": "clear", "layer": "all"}]}, {"mouse": DBL}, {"mouse": LOBBY}, {"sleep": 3.0}, {"mouse": ["jump", 2600, 1500]}]
    S["s6"]["setup"] = [{"mcp": [{"op": "music", "action": "stop"}]}, {"mouse": VID}, {"sleep": 12.0}, {"mouse": VIDLBL}, {"mouse": ["jump", 2600, 1500]}]
SL = {"_note": "12편 연출표 — 장치(Not connected → System default) · 미터와 마스터 · MUTE 와 −∞ · 무음 점검 두 사례(음악 스피커 · 슬라이드 볼륨 0) · SOLO. LG 녹화 + 앱 소리.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
