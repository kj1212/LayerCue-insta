#!/usr/bin/env python3
"""11편 연출표 — shotlist2.json · regions.json 을 만든다(줄 길이에 맞춰 '줄 끝 기준' 시각을 계산).
    python3 ep11/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(위 60 포함), 영역은 창 px(= peek-s × 2.4).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)

R = {   # 창 px [x, y, w, h]
 "musiccol": [1344, 91, 797, 605], "musiclist": [1351, 152, 782, 352], "transport": [1349, 626, 792, 70],
 "stopbtn": [1432, 632, 70, 62], "clearbtn": [1110, 94, 118, 42], "stage": [447, 141, 646, 400],
 "bar1": [1356, 157, 772, 56], "bar2": [1356, 227, 772, 56], "barbreak3": [1356, 418, 772, 56],
 "rows3": [1356, 222, 772, 186], "row1": [1356, 222, 772, 60], "row2": [1356, 284, 772, 60], "row3": [1356, 346, 772, 60],
 "rowint": [1356, 292, 772, 60], "endbtns": [2058, 222, 70, 186], "endint": [2058, 292, 70, 60],
 "len2": [1960, 284, 104, 60],
 "slider2": [1932, 290, 60, 48], "tspanel": [2172, 91, 972, 330], "tsprev": [2184, 626, 960, 70],
 "inout": [2860, 634, 290, 62],
 "gear": [3752, 2036, 56, 56], "setmusic": [1536, 904, 1112, 560], "lowerrow": [1544, 1352, 1100, 230],
 "card3": [1294, 822, 400, 238], "card4": [1712, 822, 400, 238], "card5": [2132, 822, 400, 238],
 "card6": [2552, 822, 400, 238], "card7": [2972, 822, 400, 238],
 "finder": [1300, 1240, 1280, 556], "f3": [1536, 1330, 670, 210], "f1": [1340, 1330, 160, 210],
 "musicbg": [1340, 88, 800, 620],
 # 확대(창 px)
 "z_music": [1300, 60, 900, 680], "z_stagemusic": [430, 60, 1720, 680], "z_track": [1300, 60, 1860, 680],
 "z_drop": [1200, 60, 1500, 1800], "z_settings": [1180, 520, 1520, 1180], "z_cards": [430, 60, 3000, 1080],
 "stagearea": [0, 0, 1, 1],
}
c = lambda x, y: ["click", x, y]
FIN3 = [{"mouse": ["drag", 2232, 1632, 1536, 1404]}, {"mouse": ["slowdrag", 1874, 1476, 1740, 420, 0.6]}]
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}, {"op": "music", "action": "stop"}]}, {"mouse": ["jump", 2600, 1950]}],
  "events": [
   {"line": 2, "at": 0.0, "zoom": "z_music", "scale": 2.0, "center": [1920, 1080]},
   {"line": 2, "at": 0.3, "hl": "musiccol", "lbl": ["Music", "its own channel · sky blue"], "lblSide": "below", "dur": 3.4, "exact": True},
   {"line": 3, "at": 0.0, "rest": True},
   {"line": 3, "at": 0.1, "finder": 1},
   {"line": 3, "at": 0.4, "mouse": ["drag", 2232, 1632, 1536, 1404]},
   {"line": 3, "at": 1.6, "mouse": ["slowdrag", 1874, 1476, 1740, 420, 0.6]},
   {"line": 3, "at": 2.0, "hl": "f3", "lbl": ["Three tracks", "dragged onto the list"], "lblSide": "below", "dur": 1.6, "exact": True},
   {"line": 4, "at": 0.0, "zoom": "z_music", "scale": 2.0, "center": [1920, 1080]},
   {"line": 4, "at": 0.4, "hl": "bar1", "lbl": ["Default", "made for the first tracks"], "lblSide": "below", "dur": 3.6, "exact": True},
   {"line": 5, "at": 0.1, "mouse": c(1502, 312)},
   {"line": 5, "at": 1.0, "hl": "row1", "lbl": ["Playing", "sound bars · sky-blue title"], "lblSide": "below", "dur": 2.4, "exact": True},
   {"line": 6, "at": 0.0, "zoom": "z_stagemusic", "scale": 1.7, "center": [1920, 1080]},
   {"line": 6, "at": 0.2, "mouse": c(648, 996)},
   {"line": 6, "at": 1.9, "mouse": c(1166, 175)},
   {"line": 6, "at": 2.6, "hl": "musiclist", "lbl": ["Still playing", "Clear All leaves the music"], "lblSide": "below", "dur": 2.4, "exact": True},
   {"line": 7, "at": 0.4, "mouse": c(1466, 722)},
   {"line": 7, "at": 0.9, "hl": "stopbtn", "lbl": ["Stop", "fades out"], "lblSide": "below", "dur": 2.0, "exact": True},
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1950]}],
  "events": [
   {"line": 1, "at": 0.0, "zoom": "z_music", "scale": 2.0, "center": [1920, 1080]},
   {"line": 1, "at": 0.2, "mouse": ["rclick", 1742, 245]},
   {"line": 1, "at": 1.2, "mouse": c(1867, 348)},
   {"line": 1, "at": 2.0, "type": "Walk-in"},
   {"line": 1, "at": 2.7, "key": [36]},
   {"line": 2, "at": 0.3, "mouse": c(2045, 173)},
   {"line": 2, "at": 1.4, "type": "Break"},
   {"line": 2, "at": 2.2, "key": [36]},
   {"line": 2, "at": 2.6, "hl": "barbreak3", "lbl": ["Break", "a new folder"], "lblSide": "below", "dur": 1.6, "exact": True},
   {"line": 3, "at": 1.4, "mouse": c(1440, 502)},
   {"line": 3, "at": 2.5, "rest": True},
   {"line": 3, "at": 2.6, "finder": 1},
   {"line": 3, "at": 2.9, "mouse": ["drag", 1536, 1692, 1344, 1404]},
   {"line": 3, "at": 4.1, "mouse": ["slowdrag", 1418, 1476, 1740, 420, 0.6]},
   {"line": 4, "at": 0.4, "zoom": "z_music", "scale": 2.0, "center": [1920, 1080]},
   {"line": 4, "at": 0.6, "hl": "rowint", "lbl": ["Into the open folder", ""], "lblSide": "below", "dur": 2.0, "exact": True},
   {"line": 4, "at": 2.8, "hl": "bar1", "lbl": ["Closed folder", "tracks · total length"], "lblSide": "below", "dur": 2.4, "exact": True},
   {"line": 5, "at": 0.2, "cap": "Nothing in the music list can be undone — don't tidy it during a show", "capdur": 4.8},
  ]},
 "s3": {"setup": [{"mouse": ["jump", 2600, 1950]}],
  "events": [
   {"line": 1, "at": 0.0, "zoom": "z_music", "scale": 2.0, "center": [1920, 1080]},
   {"line": 1, "at": 0.2, "mouse": c(1500, 245)},
   {"line": 1, "at": 1.6, "hl": "endbtns", "lbl": ["End action", "what happens when it ends"], "lblSide": "below", "dur": 3.0, "exact": True},
   {"line": 2, "at": 1.6, "mouse": c(2093, 312)},
   {"line": 2, "at": 2.3, "mouse": c(2093, 374)},
   {"line": 2, "at": 3.0, "mouse": c(2093, 437)},
   {"line": 2, "at": 3.7, "hl": "endbtns", "lbl": ["Play next", "one click each"], "lblSide": "below", "dur": 1.4, "exact": True},
   {"line": 3, "at": 0.1, "mouse": c(1480, 437)},
   {"line": 3, "at": 1.3, "mouse": c(2028, 660)},
   {"line": 3, "at": 2.0, "hl": "transport", "lbl": ["Near the end", "of Walk-up"], "lblSide": "below", "dur": 2.0, "exact": True},
   {"line": 3, "at": end("s3", 3, -1.4), "hl": "row1", "lbl": ["Back to the first", "Lobby Light comes in"], "lblSide": "below", "dur": 2.2, "exact": True},
   {"line": 4, "at": 0.4, "mouse": c(1440, 502)},
   {"line": 4, "at": 1.6, "mouse": c(2093, 382)},
   {"line": 4, "at": 2.3, "mouse": c(2093, 382)},
   {"line": 4, "at": 3.0, "hl": "endint", "lbl": ["Repeat one", "loops until you stop it"], "lblSide": "below", "dur": 2.0, "exact": True},
  ]},
 "s4": {"setup": [{"mouse": ["jump", 2600, 1950]}],
  "events": [
   {"line": 1, "at": 0.0, "zoom": "z_track", "scale": 1.75, "center": [1920, 1080]},
   {"line": 1, "at": 2.6, "mouse": c(1466, 722)},
   {"line": 1, "at": 3.8, "mouse": c(1500, 245)},
   {"line": 2, "at": 0.0, "mouse": ["move", 1700, 374]},
   {"line": 2, "at": 0.8, "mouse": c(1963, 374)},
   {"line": 2, "at": 1.6, "hl": "tspanel", "lbl": ["Track settings", "what this track keeps"], "lblSide": "below", "dur": 2.0, "exact": True},
   {"line": 2, "at": end("s2", 1, 0) and end("s4", 2, 0.9), "mouse": c(2218, 722)},
   {"line": 3, "at": -0.8, "mouse": c(3025, 723)},
   {"line": 3, "at": 0.6, "hl": "inout", "lbl": ["In point", "after the spoken intro"], "lblSide": "below", "dur": 1.8, "exact": True},
   {"line": 4, "at": 0.8, "mouse": c(2196 + round(936 * 124 / 136.2), 662)},
   {"line": 4, "at": 1.9, "mouse": c(3026, 723)},
   {"line": 4, "at": 2.6, "hl": "inout", "lbl": ["Out point", "before the long fade"], "lblSide": "below", "dur": 1.4, "exact": True},
   {"line": 5, "at": 0.0, "mouse": c(2218, 722)},
   {"line": 5, "at": 0.8, "hl": "len2", "lbl": ["Trimmed length", "in sky blue"], "lblSide": "below", "dur": 3.4, "exact": True},
  ]},
 "s5": {"setup": [{"mouse": ["jump", 2600, 1950]}],
  "events": [
   {"line": 1, "at": 1.8, "mouse": c(3780, 2119)},
   {"line": 1, "at": 2.6, "zoom": "z_settings", "scale": 1.45, "center": [1920, 1080]},
   {"line": 1, "at": 2.9, "mouse": c(1280, 783)},
   {"line": 1, "at": 4.2, "mouse": ["scroll", 2100, 1300, -150]},
   {"line": 2, "at": 0.3, "hl": "setmusic", "lbl": ["Settings › Stage › Music", ""], "lblSide": "right", "dur": 1.6, "exact": True},
   {"line": 2, "at": 1.9, "mouse": c(2302, 1471)},
   {"line": 2, "at": 2.6, "hl": "lowerrow", "lbl": ["Lower", "music drops under video"], "lblSide": "right", "dur": 1.6, "exact": True},
   {"line": 2, "at": end("s5", 2, -0.5), "mouse": c(2635, 622)},
   {"line": 3, "at": 0.0, "zoom": "z_stagemusic", "scale": 1.7, "center": [1920, 1080]},
   {"line": 3, "at": 0.2, "mouse": c(1502, 312)},
   {"line": 3, "at": end("s5", 3, -1.0), "mouse": c(1488, 996)},
   {"line": 3, "at": end("s5", 3, -2.6), "hl": "musicbg", "lbl": ["Music lowered", "while the video speaks"], "lblSide": "below", "dur": 6.0, "exact": True},
   {"line": 4, "at": end("s5", 4, 1.6), "mouse": c(1166, 175)},
   {"line": 4, "at": end("s5", 4, 0.8), "hl": "musiclist", "lbl": ["Back up", "the video is gone"], "lblSide": "below", "dur": 1.8, "exact": True},
  ]},
 "s6": {"setup": [{"mouse": c(1500, 245)}, {"sleep": 0.6}, {"mouse": ["jump", 2600, 1950]}],      # Walk-in 을 닫아 둔다 — 열린 폴더가 있으면 팡파르가 끝난 뒤 그 폴더 첫 곡이 이어진다(사운드 슬라이드가 앞 곡의 끝 동작을 물려받음)
  "events": [
   {"line": 1, "at": 0.0, "zoom": "z_cards", "scale": 1.2, "center": [1920, 1080]},
   {"line": 1, "at": 1.4, "hl": "card5", "lbl": ["Sound slide", "Music chip · nothing on screen"], "lblSide": "below", "dur": 3.4, "exact": True},
   {"line": 2, "at": 0.1, "mouse": c(1908, 996)},
   {"line": 2, "at": 1.5, "mouse": c(2328, 996)},
   {"line": 2, "at": 2.4, "hl": "stage", "lbl": ["Screen stays", "the fanfare takes the music's place"], "lblSide": "below", "dur": 4.0, "exact": True},
   {"line": 3, "at": end("s6", 3, 1.6), "mouse": c(2748, 996)},
   {"line": 4, "at": 0.1, "mouse": c(3168, 996)},
   {"line": 4, "at": 1.3, "mouse": c(1440, 314)},
   {"line": 4, "at": 2.4, "mouse": c(1500, 382)},
   {"line": 4, "at": 3.2, "hl": "rowint", "lbl": ["Interval", "Repeat one"], "lblSide": "below", "dur": 2.4, "exact": True},
  ]},
}
SL = {"_note": "11편 연출표 — Prize Night 음악: 끌어 넣기 → 폴더 → 끝 동작 → In/Out → 영상 아래 Lower → 팡파르 사운드 슬라이드. LG 녹화 + 앱 소리(tools/appaudio).",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 0.95, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
