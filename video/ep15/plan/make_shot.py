#!/usr/bin/env python3
"""15편 연출표 — shotlist2.json · regions.json.   python3 ep15/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(= peek-s × 2.4, y + 60), 영역은 창 px(= peek-s × 2.4).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
k = lambda x0, y0, x1, y1: [round(x0 * 2.4), round(y0 * 2.4), round((x1 - x0) * 2.4), round((y1 - y0) * 2.4)]
R = {
 "filesrow": k(490, 351, 630, 373), "importrow": k(645, 340, 1097, 386), "card7": k(1237, 343, 1404, 457),
 "mediarow": k(645, 272, 1097, 322), "finder": k(301, 278, 1050, 658), "backups": k(325, 300, 1090, 662),
 "account": k(490, 441, 630, 463), "reset": k(490, 657, 630, 678), "resetdlg": k(707, 418, 893, 483),
 "folded": k(560, 37, 730, 290), "musicbtn": k(562, 217, 729, 240), "musicwin": k(970, 0, 1318, 297),
 "aipage": k(645, 228, 1097, 680), "aiapps": k(490, 411, 630, 433),
 "cards35": k(537, 343, 1054, 457), "copyhtml": k(797, 636, 960, 657), "notice": k(719, 794, 881, 821),
 "z_set": [1150, 500, 1550, 1200], "z_list": [430, 700, 3000, 900], "z_finder": [700, 600, 2000, 1050],
 "z_narrow": [430, 60, 2800, 1100], "stagearea": [0, 0, 1, 1],
}
c = lambda x, y: ["click", x, y]
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
GEAR, FILES, TOOLS, IMPORT, OPEN, AIAPPS, RESET, CANCEL, CLOSE = c(3780, 2119), c(1339, 926), c(1277, 998), c(2285, 934), c(2366, 773), c(1290, 1071), c(1344, 1661), c(1927, 1169), c(2635, 622)
FRONT = 'osascript -e \'tell application "System Events" to set frontmost of (first process whose unix id is \'$(pgrep -f "LayerCue-film-0912/build/LayerCue.app/Contents/MacOS/LayerCue( |$)" | head -1)\') to true\''
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}]}, {"mouse": c(132, 1807)}, {"sleep": 0.8}, {"mouse": ["jump", 2600, 1700]}],
  "events": [
   hl(1, 3.0, "card7", "sponsor-reel", "", 1.6),
   {"line": 2, "at": 0.2, "mouse": GEAR},
   {"line": 2, "at": 1.2, "mouse": FILES},
   {"line": 2, "at": 1.8, **Z("z_set", 1.6)},
   hl(2, 2.4, "filesrow", "04 Files & YouTube", "", 2.0, "right"),
   hl(3, 0.4, "importrow", "1 file outside", "a USB stick", 5.4),
   {"line": 4, "at": 0.4, "mouse": IMPORT},
   {"line": 4, "at": end("s1", 4, -0.3), "mouse": TOOLS},
   {"line": 5, "at": -0.6, "mouse": FILES},
   hl(5, 0.3, "importrow", "Every file is inside", "the media folder", 2.6),
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.1, "mouse": OPEN},
   {"line": 1, "at": 1.4, "sh": "./finderwin.sh"},
   {"line": 1, "at": 2.0, **Z("z_finder", 1.5)},
   hl(2, 0.2, "finder", "The LayerCue folder", "ordinary files", 4.8),
   {"line": 3, "at": 0.4, "cap": "Quit LayerCue first · settings are not in this folder", "capdur": 3.0},
   {"line": 4, "at": 0.3, "cap": "Mac: ~/Documents/LayerCue · Windows: C:\\Users\\<you>\\LayerCue", "capdur": 4.8},
   {"line": 5, "at": 0.1, "mouse": ["dbl", 840, 900]},
   hl(5, 1.0, "backups", "Backups", "one step back", 3.4),
   {"line": 5, "at": end("s2", 5, -0.5), "sh": "osascript -e 'tell application \"Finder\" to close every Finder window'; " + FRONT},
  ]},
 "s3": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_set", 1.6)},
   {"line": 2, "at": 0.1, "cap": "07 Account › Keep settings in my account — off by default", "capdur": 3.8},
   {"line": 3, "at": 0.2, "mouse": RESET},
   hl(3, 1.0, "resetdlg", "Reset every setting", "no undo", 2.4, "right"),
   {"line": 3, "at": 3.6, "mouse": CANCEL},
   {"line": 3, "at": end("s3", 3, -0.6), "mouse": CLOSE},
  ]},
 "s4": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.4, "mouse": ["drag", 3837, 1200, 2300, 1200]},
   {"line": 1, "at": 1.8, **Z("z_narrow", 1.3)},
   hl(1, 2.6, "folded", "Folded", "Slide settings · Music", 2.4, "right"),
   {"line": 2, "at": 1.6, "mouse": c(1548, 607)},
   hl(2, 2.6, "musicwin", "Music", "in its own window", 2.4, "below"),
   {"line": 3, "at": 0.0, "rest": True},
   {"line": 3, "at": 0.2, "mouse": ["drag", 2300, 1200, 3837, 1200]},
  ]},
 "s5": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.6, "mouse": GEAR},
   {"line": 1, "at": 1.6, "mouse": AIAPPS},
   {"line": 1, "at": 2.2, **Z("z_set", 1.6)},
   hl(2, 0.2, "aipage", "AI apps", "Claude Desktop · LM Studio · Cursor", 5.0, "right"),
   {"line": 3, "at": 0.3, "cap": "Quit the AI app completely (⌘Q) and reopen it · not ChatGPT, the Gemini app or claude.ai yet", "capdur": 6.4},
   {"line": 3, "at": end("s5", 3, -0.4), "mouse": CLOSE},
  ]},
 "s6": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, **Z("z_list", 1.25)},
   {"line": 1, "at": 0.2, "mouse": c(1512, 1133)},
   {"line": 1, "at": 1.2, "mouse": ["shiftclick", 2232, 1133]},
   {"line": 1, "at": 2.4, "mouse": ["rclick", 1908, 996]},
   hl(1, 3.4, "copyhtml", "Copy as HTML for AI", "", 1.6, "right"),
   {"line": 1, "at": end("s1", 1, 0) and end("s6", 1, -0.3), "mouse": c(2107, 1610)},
   {"line": 2, "at": 0.3, "cap": "Paste into any AI chat · ask · copy its answer   (the chat isn't shown)", "capdur": 6.0},
   {"line": 3, "at": 0.0, "clip": open(H / "media" / "answer.html").read()},
   {"line": 3, "at": 0.4, "mouse": c(2200, 1600)},
   {"line": 3, "at": 1.4, "key": [9, True]},
   hl(3, 1.8, "cards35", "Updated", "time on its own line, in amber", 4.6),
   {"line": 4, "at": 0.3, "cap": "From HTML: updated 3 · ⌘Z takes the whole paste back", "capdur": 4.0},
  ]},
}
SL = {"_note": "15편 연출표 — Files & YouTube · Import external files(USB 의 sponsor-reel) · Open → Finder(아이콘 보기, LG) · Backups · Reset 창 Cancel · 좁은 창 · Music 따로 창 · AI apps 화면 · Copy as HTML for AI → 답 붙여 넣기. LG 녹화.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
