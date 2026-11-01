#!/usr/bin/env python3
"""13편 연출표 — shotlist2.json · regions.json.   python3 ep13/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(위 60 포함), 영역은 창 px(= peek-s × 2.4). 데모 영상은 사용자 채널의 1편(youtu.be/55dioOOzick).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
k = lambda x0, y0, x1, y1: [round(x0 * 2.4), round(y0 * 2.4), round((x1 - x0) * 2.4), round((y1 - y0) * 2.4)]   # peek-s 상자 → 창 px
R = {
 "linkbtn": k(1474, 311, 1496, 332), "addlink": k(629, 396, 971, 506), "card7": k(1238, 343, 1404, 457),
 "stage": [447, 141, 646, 400], "ctl": k(187, 266, 515, 288), "ticks": k(910, 240, 1312, 258),
 "caprow": k(1124, 96, 1282, 114), "capmenu": k(1236, 108, 1401, 244), "langdlg": k(645, 256, 955, 645),
 "setcap": k(645, 532, 1097, 665), "dlbtn": k(1126, 118, 1206, 138), "chips": k(1120, 121, 1312, 141),
 "scale4": k(1120, 145, 1248, 168), "badge": k(1238, 440, 1297, 456), "toolrow": k(645, 348, 1097, 396),
 "z_add": [1150, 600, 2600, 750], "z_stage_ss": [430, 60, 2780, 1020], "z_ss": [2150, 60, 1200, 1100],
 "z_dlg": [1300, 500, 1240, 1150], "z_setcap": [430, 100, 2300, 1600], "z_tools": [1150, 500, 1550, 700],
 "stagearea": [0, 0, 1, 1],
}
c = lambda x, y: ["click", x, y]
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
URL = "https://youtu.be/55dioOOzick"
CAPS, KO, JA, MANAGE = c(2964, 312), c(3088, 415), c(3088, 542), c(3150, 542)      # Japanese 등록 전엔 Manage 가 넷째 줄(542), 등록 뒤엔 Japanese 가 그 자리
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}]}, {"mouse": c(132, 1807)}, {"sleep": 0.8}, {"clip": URL}, {"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 2, "at": 1.6, "mouse": c(3562, 830)},
   hl(2, 2.5, "linkbtn", "Link", "on the title bar", 2.0),
   {"line": 3, "at": 0.0, **Z("z_add", 1.9)},
   {"line": 3, "at": 0.2, "key": [9, "cmd"]},
   hl(3, 0.5, "addlink", "Add Link", "YouTube / Web", 1.8),
   {"line": 3, "at": 1.5, "mouse": c(2258, 1219)},
   {"line": 4, "at": 0.0, "rest": True},
   hl(4, 0.6, "card7", "YouTube", "added at the end", 4.0),
   {"line": 5, "at": 0.3, "cap": "Or copy an address and press ⌘V on the slide list", "capdur": 4.2},
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, "mouse": c(3168, 996)},
   {"line": 1, "at": 1.0, **Z("z_stage_ss", 1.35)},
   hl(1, 1.4, "stage", "Streaming", "on stage", 2.6),
   hl(2, 1.8, "ctl", "LayerCue's controls", "under the preview", 3.0),
   {"line": 3, "at": 0.3, "cap": "One streaming YouTube on stage at a time · two together? download them", "capdur": 5.2},
   {"line": 4, "at": 0.2, "mouse": c(3168, 1133)},
   hl(4, 2.0, "ticks", "Chapters", "read from YouTube", 2.8),
  ]},
 "s3": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_stage_ss", 1.35)},
   {"line": 1, "at": 0.6, "mouse": CAPS},
   hl(1, 1.2, "capmenu", "Captions", "", 1.4),
   {"line": 1, "at": 2.8, "mouse": KO},
   hl(1, 4.0, "stage", "Korean captions", "on stage at once", 3.2),
   {"line": 2, "at": 1.6, "mouse": CAPS},
   {"line": 2, "at": 2.6, "mouse": MANAGE},
   {"line": 3, "at": 0.0, **Z("z_dlg", 1.6)},
   {"line": 3, "at": 0.1, "mouse": c(1918, 850)},
   {"line": 3, "at": 0.4, "type": "Japanese"},
   {"line": 3, "at": 1.7, "mouse": c(1704, 946)},
   hl(3, 2.3, "langdlg", "Caption languages", "tick, then OK", 1.2),
   {"line": 3, "at": 3.2, "mouse": c(2218, 1554)},
   {"line": 4, "at": 0.0, **Z("z_stage_ss", 1.35)},
   {"line": 4, "at": 0.2, "mouse": CAPS},
   {"line": 4, "at": 1.3, "mouse": JA},
   hl(4, 2.4, "stage", "Japanese", "", 2.0),
   {"line": 5, "at": 0.3, "cap": "Not saved with the slide · Settings › Files & YouTube › Default captions", "capdur": 5.2},
  ]},
 "s4": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 2.2, "mouse": c(3780, 2119)},
   {"line": 1, "at": 3.2, "mouse": c(1339, 926)},
   {"line": 1, "at": 4.0, "mouse": ["scroll", 2100, 1300, -150]},
   {"line": 1, "at": 4.8, **Z("z_setcap", 1.35)},
   {"line": 2, "at": 0.4, "mouse": c(2314, 1370)},
   hl(2, 1.0, "stage", "Top", "", 2.4),
   {"line": 3, "at": 0.3, "mouse": c(2213, 1615)},
   {"line": 3, "at": 0.9, "key": [0, "cmd"]},
   {"line": 3, "at": 1.1, "type": "160"},
   {"line": 3, "at": 1.6, "key": [36]},
   hl(3, 2.0, "stage", "160%", "", 3.0),
   {"line": 3, "at": end("s4", 3, -1.1), "key": [53]},
   {"line": 3, "at": end("s4", 3, -1.3), "mouse": c(2635, 622)},
  ]},
 "s5": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_ss", 1.6)},
   {"line": 1, "at": 2.6, "mouse": c(1166, 175)},
   {"line": 1, "at": 4.2, "mouse": c(2798, 367)},
   hl(1, 4.7, "dlbtn", "Download", "", 1.0),
   {"line": 3, "at": 0.0, "rest": True},
   hl(3, 0.3, "chips", "Downloaded", "", 1.6),
   hl(3, 2.1, "badge", "YouTube ↓", "", 1.6),
   {"line": 4, "at": 0.0, **Z("z_ss", 1.6)},
   hl(4, 1.0, "scale4", "All four Scale modes", "and crop", 3.6),
   hl(5, 0.3, "chips", "Streaming · Downloaded", "switch any time", 2.6),
   {"line": 5, "at": 3.2, "cap": "Download quality 1080p by default · Settings › Files & YouTube", "capdur": 3.4},
  ]},
 "s6": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 2, "at": 2.6, "mouse": c(3780, 2119)},
   {"line": 2, "at": 3.6, "mouse": c(1277, 998)},
   {"line": 2, "at": 4.4, **Z("z_tools", 1.9)},
   {"line": 3, "at": 0.2, "mouse": c(2215, 936)},
   hl(3, 1.6, "toolrow", "YouTube tool", "a newer version is available", 4.4),
   {"line": 1, "at": 0.3, "cap": "The YouTube tool is yt-dlp · ffmpeg converts", "capdur": 4.6},
   {"line": 4, "at": 0.3, "cap": "After Update: quit LayerCue and open it again", "capdur": 3.0},
   {"line": 4, "at": end("s6", 4, -0.4), "mouse": c(2635, 622)},
  ]},
}
SL = {"_note": "13편 연출표 — 1편 영상을 Day 1 에 링크로 · 스트리밍 송출 · 자막(한국어, 일본어 등록) · 자막 모양(위, 160%) · 다운로드 · YouTube tool Check. LG 녹화 + 앱 소리.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
