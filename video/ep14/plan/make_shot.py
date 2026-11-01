#!/usr/bin/env python3
"""14편 연출표 — shotlist2.json · regions.json.   python3 ep14/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(위 60 포함), 영역은 창 px(= peek-s × 2.4). 데모 파일은 Finder 창 "Speaker files"(finder.sh).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
k = lambda x0, y0, x1, y1: [round(x0 * 2.4), round(y0 * 2.4), round((x1 - x0) * 2.4), round((y1 - y0) * 2.4)]
R = {
 "newpres": k(645, 336, 955, 566), "frombtns": k(657, 532, 832, 554), "addfile": k(1446, 311, 1468, 332),
 "finder": k(500, 626, 900, 825), "card1": k(187, 343, 354, 457), "cards27": k(362, 343, 1404, 457), "notice": k(596, 790, 1004, 824),
 "bgchip": k(500, 346, 529, 364),
 "table": k(451, 355, 1315, 644), "cell30": k(451, 571, 739, 644), "fontfield": k(204, 98, 314, 119),
 "thumb5": k(8, 420, 152, 500), "thumb6": k(8, 509, 152, 589),
 "pdfdlg": k(487, 231, 1113, 671), "range": k(636, 544, 820, 566), "res": k(498, 585, 870, 607), "newcards": k(537, 469, 879, 583),
 "exportdlg": k(471, 270, 1129, 632), "exprange": k(619, 567, 805, 589), "savepanel": k(647, 365, 953, 512),
 "z_center": [1100, 650, 1700, 1000], "z_list": [430, 700, 3000, 900], "z_editor": [800, 380, 2600, 1500], "z_left": [0, 180, 1500, 1500],
 "z_pdf": [1150, 520, 1550, 1150], "z_exp": [1100, 620, 1650, 900], "stagearea": [0, 0, 1, 1],
}
c = lambda x, y: ["click", x, y]
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}]}, {"mouse": c(132, 1807)}, {"sleep": 0.8}, {"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 2, "at": 0.2, "mouse": c(360, 1675)},
   {"line": 2, "at": 0.8, **Z("z_center", 1.8)},
   hl(2, 1.3, "frombtns", "From PowerPoint · From PDF", "instead of Create", end("s2", 2, 0.3) if False else 4.2),
   {"line": 2, "at": end("s1", 2, -0.2), "mouse": c(2071, 1363)},
   {"line": 3, "at": 0.0, "rest": True},
   {"line": 3, "at": 0.2, "mouse": ["move", 3497, 830]},
   hl(3, 0.8, "addfile", "Add File", "to the end", 1.8),
   {"line": 3, "at": 2.6, "finder": 1},
   hl(3, 3.0, "finder", "Or drag it in", "", 2.0, "right"),
   {"line": 4, "at": 0.3, "cap": "Formats: .pptx and .pdf · old .ppt? save it as .pptx first", "capdur": 4.2},
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 0.0, "finder": 1},
   {"line": 1, "at": 0.2, "mouse": ["drag", 1730, 2000, 1490, 1750]},
   {"line": 1, "at": 1.4, "mouse": ["slowdrag", 1546, 1735, 648, 1000, 0.9]},
   hl(1, 2.2, "card1", "Drop on her title", "it goes in after it", 2.2),
   {"line": 1, "at": end("s1", 1, -0.4) if False else 4.4, "front": 1},
   hl(2, 0.2, "cards27", "6 slides", "", 1.6),
   {"line": 2, "at": 0.3, "cap": "Imported 6 slides from PowerPoint — May differ from the original: charts and SmartArt", "capdur": 4.8},
   {"line": 3, "at": 0.0, **Z("z_list", 1.25)},
   hl(3, 2.6, "bgchip", "BG", "background on B · words on F", 3.0),
  ]},
 "s3": {"setup": [{"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 0.2, "mouse": c(1907, 1133)},
   {"line": 1, "at": 0.9, "mouse": c(288, 2121)},
   {"line": 1, "at": 2.0, **Z("z_editor", 1.4)},
   hl(1, 2.4, "table", "One text box per cell", "", 2.0),
   {"line": 1, "at": 4.4, "mouse": ["dbl", 1171, 1478]},
   {"line": 1, "at": 5.1, "key": [0, True]},
   {"line": 1, "at": 5.4, "type": "30 m +"},
   {"line": 1, "at": 6.3, "key": [53]},
   {"line": 2, "at": 0.0, **Z("z_left", 1.4)},
   hl(2, 0.6, "fontfield", "Default font", "Segoe UI isn't here", 3.6),
   hl(3, 0.2, "thumb5", "The chart", "didn't come across", 1.8, "right"),
   {"line": 3, "at": 2.4, "mouse": ["rclick", 190, 1375]},
   {"line": 3, "at": 3.6, "mouse": c(336, 1604)},
   {"line": 3, "at": 4.6, "mouse": ["rclick", 190, 1164]},
   {"line": 3, "at": 5.7, "mouse": c(336, 1393)},
   {"line": 4, "at": 0.3, "cap": "⌘Z takes back the whole import · Undone — PowerPoint import", "capdur": 3.2},
   {"line": 4, "at": 3.2, "mouse": c(105, 2121)},
  ]},
 "s4": {"setup": [{"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 0.6, "finder": 1},
   {"line": 1, "at": 0.8, "mouse": ["drag", 1400, 2000, 1200, 1700]},
   {"line": 1, "at": 2.0, "mouse": ["slowdrag", 1320, 1735, 1068, 1296, 0.8]},
   {"line": 1, "at": 4.2, "front": 1},
   {"line": 1, "at": 4.4, **Z("z_pdf", 1.6)},
   hl(1, 4.8, "pdfdlg", "PDF import", "6 pages, all picked", 1.4),
   {"line": 2, "at": 1.2, "mouse": c(1745, 1393)},
   {"line": 2, "at": 1.8, "type": "2-3"},
   {"line": 2, "at": 2.5, "key": [36]},
   hl(2, 2.8, "range", "Range", "pages 2 and 3", 1.2),
   hl(3, 0.3, "res", "Resolution · Format", "4K · JPEG", 4.6),
   {"line": 3, "at": end("s4", 3, -0.3), "mouse": c(2580, 1615)},
   {"line": 4, "at": 0.4, **Z("z_list", 1.25)},
   hl(4, 0.8, "newcards", "Picture slides", "", 4.2),
  ]},
 "s5": {"setup": [{"mouse": ["jump", 2600, 1500]}],
  "events": [
   {"line": 1, "at": 2.6, "mouse": ["rclick", 132, 1807]},
   {"line": 1, "at": 3.8, "mouse": c(300, 2054)},
   {"line": 2, "at": 0.0, **Z("z_exp", 1.6)},
   hl(2, 0.2, "exportdlg", "Export to PDF", "every slide picked", 1.4),
   {"line": 2, "at": 1.6, "mouse": c(1702, 1447)},
   {"line": 2, "at": 2.0, "type": "1-10"},
   {"line": 2, "at": 2.6, "key": [36]},
   {"line": 2, "at": 3.4, "mouse": c(2574, 1520)},
   {"line": 3, "at": 0.4, "key": [5, True, True]},
   {"line": 3, "at": 1.1, "type": "~/projects/LayerCue-insta/video/ep14/media/export"},
   {"line": 3, "at": 4.4, "key": [36]},
   {"line": 3, "at": 5.4, "mouse": c(2174, 1228)},
   {"line": 4, "at": 0.0, "rest": True},
   {"line": 4, "at": 0.3, "cap": "Exported to PDF · streaming YouTube and audio slides give no picture — leave them unpicked", "capdur": 5.4},
  ]},
}
SL = {"_note": "14편 연출표 — 세 입구 · Keynote-Okafor.pptx 를 Day 1 첫 카드에 끌어 놓기 · 에디터 확인(표 · 글꼴 · 차트 · 숨김 삭제) · Summit-Programme.pdf 2–3쪽 · Export to PDF 1–10. LG 녹화.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
