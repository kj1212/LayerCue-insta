#!/usr/bin/env python3
"""18편 연출표 — shotlist2.json · regions.json.   python3 ep18/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(= peek-s × 2.4, y + 60), 영역은 창 px(= peek-s × 2.4).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
k = lambda x0, y0, x1, y1: [round(x0 * 2.4), round(y0 * 2.4), round((x1 - x0) * 2.4), round((y1 - y0) * 2.4)]
R = {
 "toolsrow": k(645, 300, 1100, 330), "toolsbtn": k(490, 381, 630, 401), "upd": k(948, 300, 1006, 324),
 "filesbtn": k(490, 351, 630, 373), "importrow": k(645, 340, 1097, 386),
 "card3": k(538, 343, 703, 436), "locate": k(660, 386, 826, 407), "relinked": k(769, 793, 831, 821),
 "lockrow": k(645, 268, 1100, 310), "lockicon": k(1440, 848, 1457, 868), "card1": k(188, 343, 1053, 436),
 "chip": k(195, 848, 372, 869), "toast": k(643, 793, 958, 821), "notconn": k(590, 40, 770, 54),
 "clear": k(463, 40, 510, 56), "power": k(430, 40, 790, 55), "quitdlg": k(645, 404, 955, 497),
 "z_set": k(484, 217, 1116, 684), "z_cards": k(180, 300, 1420, 470), "z_tiles": k(180, 30, 800, 465), "z_bar": k(170, 690, 1600, 875),
}
c = lambda x, y: ["click", x, y]
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
P = lambda x, y: [round(x * 2.4), round(y * 2.4 + 60)]
C = lambda x, y: ["click", *P(x, y)]
GEAR, TOOLS, CHECK, FILES, STAGEPG, LOCKSW, CLOSE = C(1575, 858), C(532, 391), C(923, 312), C(557, 361), C(533, 301), C(913, 294), C(1098, 234)
BD = lambda on: 'betterdisplaycli set -name="Stage Monitor" -connected=%s >/dev/null 2>&1 &' % ("on" if on else "off")
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}]}, {"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 2.0, "cap": "The day before", "capdur": 2.4},
   {"line": 2, "at": 0.4, "mouse": GEAR},
   {"line": 2, "at": 1.4, "mouse": TOOLS},
   {"line": 2, "at": 2.0, **Z("z_set", 1.5)},
   {"line": 2, "at": 2.5, "mouse": CHECK},
   hl(2, 4.2, "toolsrow", "0.9.13 available", "", 2.4, "below"),
   hl(3, 0.4, "upd", "Not on show day", "it closes LayerCue", 3.6, "below"),
   {"line": 4, "at": 0.2, "mouse": FILES},
   hl(4, 1.2, "importrow", "Import external files", "every file inside", 4.2, "below"),
   {"line": 4, "at": 6.4, "mouse": C(1098, 234)},
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, "rest": True},
   {"line": 1, "at": 0.6, "mouse": C(270, 390)},
   {"line": 1, "at": 1.8, **Z("z_cards", 1.35)},
   hl(1, 3.2, "card3", "File missing", "the file was renamed", 3.8),
   {"line": 2, "at": 0.3, "mouse": ["rclick", *P(660, 380)]},
   hl(2, 1.1, "locate", "Locate file", "", 1.4, "right"),
   {"line": 2, "at": 2.6, "mouse": C(718, 396)},
   {"line": 2, "at": 4.6, "mouse": ["dbl", *P(812, 352)]},
   hl(2, 5.4, "card3", "Relinked", "", 2.4),
   {"line": 3, "at": 0.4, "cap": "Listen to each video and song once, at show volume", "capdur": 3.0},
  ]},
 "s3": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}, {"op": "output", "on": False}]}, {"sleep": 1.5}, {"mcp": [{"op": "output", "on": True}]}, {"sleep": 2.0}, {"mouse": ["jump", 2600, 1700]}],      # 잠금은 화면을 켠 뒤 「처음」 보낼 때 — s2 에서 이미 보냈으니 껐다 켠다
  "events": [
   {"line": 1, "at": 0.0, "rest": True},
   {"line": 1, "at": 0.2, "mouse": GEAR},
   {"line": 1, "at": 1.1, "mouse": STAGEPG},
   {"line": 1, "at": 1.6, **Z("z_set", 1.5)},
   {"line": 1, "at": 2.4, "mouse": LOCKSW},
   hl(1, 2.9, "lockrow", "Lock editing while live", "", 2.4, "below"),
   {"line": 2, "at": 0.0, "rest": True},
   {"line": 2, "at": 0.2, "mouse": CLOSE},
   {"line": 2, "at": 1.4, "mouse": C(445, 390)},
   hl(2, 2.4, "lockicon", "Editing locked", "", 3.2, "above"),
   {"line": 3, "at": 0.2, "mouse": C(620, 390)},
   {"line": 3, "at": 1.6, "mouse": ["drag", *P(795, 390), *P(1150, 390)]},
   hl(3, 3.6, "card1", "Order unchanged", "slides still go out", 2.6, "below"),
   {"line": 4, "at": 0.2, "cap": "Unlocks when every screen is off · a lock set by hand stays", "capdur": 4.0},
  ]},
 "s4": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, "sh": BD(False)},
   hl(1, 0.6, "toast", "Output screen disconnected", "", 2.0, "above"),
   hl(1, 4.6, "chip", "On air 1/2", "a ring", 2.0, "right"),
   {"line": 2, "at": 0.0, "sh": BD(True)},
   hl(2, 2.2, "chip", "On air 2/2", "back by itself", 2.0, "right"),
  ]},
 "s5": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.4, "mouse": C(486, 47)},
   hl(1, 0.8, "clear", "Clear", "", 1.4, "below"),
   {"line": 1, "at": 2.0, "mouse": C(441, 47)},
   {"line": 1, "at": 2.6, "mouse": C(774, 47)},
   hl(1, 3.0, "power", "Power off", "every screen", 1.8, "below"),
   {"line": 2, "at": 0.3, "cap": "With a screen on, Quit warns: “You are on air — quitting will black out the screen.”", "capdur": 5.4},
   {"line": 2, "at": 1.2, "key": [12, True]},
   hl(2, 2.0, "quitdlg", "Quit LayerCue?", "your work is saved", 3.0, "right"),
   {"line": 3, "at": 2.4, "mouse": C(870, 473)},      # 영상에선 Cancel(끝내면 녹화할 창이 사라진다)
  ]},
}
SL = {"_note": "18편 연출표 — Tools Check(0.9.13 available) · Import · File missing → 메뉴 Locate file(카드 위 단추는 이슈 #10) · 편집 잠금 · 케이블 뽑기 · 정리 순서 · 끝내기. (옛 17편: — NDI(Stage Lyrics, 투명, B 끔) → OBS(Camera = 무대 사진) · Syphon(OBS 연결만 — 그림은 뒤집혀 보여 이슈 #9, 화면에 안 넣음) · fill & key(UltraStudio Mini Replay 12G). (옛 16편: — 무대 모니터(BetterDisplay 가상 디스플레이 Stage Monitor) · Add screen · Send to · 이름 · Layers shown(B 끔) · Foreground 칩 · 온에어 목록 · Layout · 뽑기/꽂기. LG 녹화. (옛 15편 메모: — Files & YouTube · Import external files(USB 의 sponsor-reel) · Open → Finder(아이콘 보기, LG) · Backups · Reset 창 Cancel · 좁은 창 · Music 따로 창 · AI apps 화면 · Copy as HTML for AI → 답 붙여 넣기. LG 녹화.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
