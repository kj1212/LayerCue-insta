#!/usr/bin/env python3
"""16편 연출표 — shotlist2.json · regions.json.   python3 ep16/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(= peek-s × 2.4, y + 60), 영역은 창 px(= peek-s × 2.4).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
k = lambda x0, y0, x1, y1: [round(x0 * 2.4), round(y0 * 2.4), round((x1 - x0) * 2.4), round((y1 - y0) * 2.4)]
R = {
 "tile1": k(186, 38, 455, 227), "tile2": k(519, 38, 788, 227), "layercol": k(463, 64, 489, 209),
 "cells1": k(186, 210, 455, 227), "cells2": k(519, 210, 788, 227), "bcell2": k(520, 209, 558, 227),
 "sliders": k(387, 265, 409, 287), "addscreen": k(1407, 35, 1494, 58), "row2": k(1176, 296, 1591, 373),
 "switch2": k(1522, 301, 1586, 320), "card3chip": k(673, 346, 702, 365),
 "chip": k(195, 848, 372, 869), "airlist": k(195, 757, 463, 840), "layout": k(1176, 86, 1591, 233),
 "z_tiles": k(180, 30, 800, 465), "z_win": k(1168, 0, 1598, 380), "z_bar": k(170, 690, 720, 875),
}
c = lambda x, y: ["click", x, y]
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
P = lambda x, y: [round(x * 2.4), round(y * 2.4 + 60)]          # peek-s(1600 폭) → LG 캡처 px
CARD1, CARD2, CARD3, CHIP3 = c(*P(270, 390)), c(*P(445, 390)), c(*P(620, 390)), c(*P(690, 356))
SLIDERS, ADD, SENDTO, MONITOR, PENCIL, SWITCH2 = c(*P(398, 276)), c(*P(1450, 46)), c(*P(1410, 354)), c(3220, 620), c(*P(1271, 310)), c(*P(1571, 310))
CLOSE, BCELL2, AIRCHIP, LIST_STAGE, LIST_OPEN = c(*P(1180, 13)), c(*P(539, 218)), c(*P(270, 858)), c(*P(444, 800)), c(*P(250, 826))
BD = lambda on: 'betterdisplaycli set -name="Stage Monitor" -connected=%s >/dev/null 2>&1 &' % ("on" if on else "off")
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}]}, {"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 2.2, "mouse": CARD1},
   hl(1, 3.2, "tile1", "01 Audience", "video and words", 2.8, "right"),
   {"line": 2, "at": 0.2, **Z("z_tiles", 1.35)},
   hl(2, 1.2, "layercol", "One stage", "seven layers", 2.6, "right"),
   hl(2, 4.2, "cells1", "Layers shown", "what this screen shows", 2.6),
   {"line": 3, "at": 0.3, "cap": "One stage → every screen shows the same slides", "capdur": 3.6},
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, "rest": True},
   hl(1, 2.6, "sliders", "Stage output", "", 1.4, "right"),
   {"line": 1, "at": 4.2, "mouse": SLIDERS},
   {"line": 1, "at": 5.2, **Z("z_win", 1.55)},
   {"line": 2, "at": 1.2, "mouse": ADD},
   hl(2, 2.2, "row2", "Screen 2", "a free screen", 2.2, "below"),
   hl(3, 1.2, "switch2", "Off", "LayerCue's own screen", 3.6, "below"),
   {"line": 4, "at": 0.4, "mouse": SENDTO},
   {"line": 4, "at": 1.5, "mouse": MONITOR},
   {"line": 4, "at": 2.9, "mouse": PENCIL},
   {"line": 4, "at": 3.4, "key": [0, True]},
   {"line": 4, "at": 3.6, "type": "Stage", "gap": 0.09},
   {"line": 4, "at": 4.6, "key": [36]},
   {"line": 5, "at": 0.4, "mouse": SWITCH2},
   hl(5, 1.4, "row2", "02 Stage", "on air", 2.2, "below"),
   {"line": 5, "at": 1.6, "cap": "Audience here is a virtual screen: it only shows in its tile", "capdur": 2.6},
  ]},
 "s3": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, "rest": True},
   {"line": 1, "at": 0.3, "mouse": CLOSE},
   {"line": 1, "at": 1.1, **Z("z_tiles", 1.35)},
   hl(1, 1.8, "tile2", "02 Stage", "Stage Monitor", 2.0, "right"),
   hl(1, 4.0, "cells2", "Layers shown", "B F 1 2 3 4 5", 2.4),
   {"line": 2, "at": 0.8, "mouse": BCELL2},
   {"line": 2, "at": 1.25, "mouse": ["move", *P(660, 560)]},      # 칸 위에 두면 「다시 켜면」 미리보기(주황)로 차 B off 가 켜진 듯 보였다
   hl(2, 1.5, "bcell2", "B off", "", 1.6),
   {"line": 3, "at": 0.3, "mouse": CARD2},
   hl(3, 1.7, "tile1", "Audience", "video and words", 2.0, "below"),
   hl(3, 3.9, "tile2", "Stage", "words on black", 2.6, "below"),
   hl(4, 0.4, "layercol", "B is still up", "", 2.4, "right"),
   {"line": 5, "at": 0.3, "mouse": CARD3},
   hl(5, 2.0, "tile2", "Stage", "the picture is back", 2.6, "below"),
   {"line": 6, "at": 0.6, "mouse": CHIP3},
   hl(6, 1.2, "card3chip", "FG → BG", "", 1.6, "right"),
   {"line": 6, "at": 3.2, "mouse": CARD3},
   hl(6, 4.4, "tile2", "Stage", "words only", 2.4, "below"),
   {"line": 6, "at": 5.0, "cap": "Episode 8: lock a whole list to one layer", "capdur": 2.8},
  ]},
 "s4": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_bar", 1.6)},
   hl(1, 0.6, "chip", "On air 2/2", "Audience · Stage", 2.4, "right"),
   {"line": 2, "at": 0.3, "mouse": AIRCHIP},
   hl(2, 1.3, "airlist", "Every screen", "its own power switch", 4.0, "right"),
   {"line": 3, "at": 0.3, "mouse": LIST_STAGE},
   {"line": 3, "at": 1.8, "mouse": LIST_STAGE},
  ]},
 "s5": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.2, "mouse": LIST_OPEN},
   {"line": 1, "at": 0.4, "rest": True},
   {"line": 1, "at": 1.2, **Z("z_win", 1.55)},
   hl(1, 1.8, "layout", "Layout", "a picture of your room", 2.4, "below"),
   {"line": 1, "at": 4.6, "mouse": ["drag", *P(1430, 117), *P(1525, 185)]},
   hl(2, 0.4, "layout", "Solid · on air", "dashed · on, nothing out", 4.6, "below"),
   {"line": 3, "at": 0.0, "sh": BD(False)},
   {"line": 3, "at": 0.0, "rest": True},
   hl(3, 1.8, "row2", "not connected", "", 2.4, "below"),
   hl(3, 4.6, "chip", "A ring", "only some are showing", 2.8, "right"),
   {"line": 4, "at": 0.0, "sh": BD(True)},
   hl(4, 2.0, "row2", "On air", "again", 2.2, "below"),
   {"line": 5, "at": 0.3, "cap": "Kept on this computer — not in cue sheets or presentations", "capdur": 3.8},
  ]},
}
SL = {"_note": "16편 연출표 — 무대 모니터(BetterDisplay 가상 디스플레이 Stage Monitor) · Add screen · Send to · 이름 · Layers shown(B 끔) · Foreground 칩 · 온에어 목록 · Layout · 뽑기/꽂기. LG 녹화. (옛 15편 메모: — Files & YouTube · Import external files(USB 의 sponsor-reel) · Open → Finder(아이콘 보기, LG) · Backups · Reset 창 Cancel · 좁은 창 · Music 따로 창 · AI apps 화면 · Copy as HTML for AI → 답 붙여 넣기. LG 녹화.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
