#!/usr/bin/env python3
"""17편 연출표 — shotlist2.json · regions.json.   python3 ep17/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(= peek-s × 2.4, y + 60), 영역은 창 px(= peek-s × 2.4).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
k = lambda x0, y0, x1, y1: [round(x0 * 2.4), round(y0 * 2.4), round((x1 - x0) * 2.4), round((y1 - y0) * 2.4)]
R = {
 "tile1": k(186, 38, 455, 227), "netgroup": k(1272, 236, 1555, 287), "resrow": k(1205, 397, 1530, 419),
 "alpharow": k(1205, 424, 1415, 443), "bcell2": k(1466, 321, 1484, 338), "state2": k(1460, 301, 1588, 320),
 "ndilist": k(984, 416, 1428, 440), "obsprev": k(994, 130, 1580, 460), "audiorow": k(1205, 449, 1590, 469),
 "syphonok": k(1205, 472, 1340, 488), "premult": k(1270, 449, 1395, 468),
 "fillrow": k(1205, 362, 1590, 383), "sdirow": k(1205, 389, 1392, 409), "keymix": k(1205, 414, 1590, 458),
 "alpha3": k(1205, 486, 1395, 506), "bcell3": k(1466, 339, 1484, 356),
 "z_win": k(1168, 0, 1598, 520), "z_obs": k(750, 0, 1600, 640),
}
c = lambda x, y: ["click", x, y]
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
P = lambda x, y: [round(x * 2.4), round(y * 2.4 + 60)]          # peek-s(1600 폭) → LG 캡처 px
C = lambda x, y: ["click", *P(x, y)]
FRONT = 'osascript -e \'tell application "System Events" to set frontmost of (first process whose unix id is \'$(pgrep -f "LayerCue-film-0912/build/LayerCue.app/Contents/MacOS/LayerCue( |$)" | head -1)\') to true\''
OBS = "../.venv/bin/python obs_ctl.py "
S = {
 "s1": {"setup": [{"mcp": [{"op": "clear", "layer": "all"}, {"op": "usePt", "name": "School Song"}, {"op": "present", "n": 1}]}, {"mouse": ["jump", 2600, 1700]}],
  "events": [
   hl(1, 3.4, "tile1", "01 Audience", "video and words", 2.6, "right"),
   {"line": 2, "at": 0.4, "mouse": C(398, 276)},
   {"line": 2, "at": 1.6, **Z("z_win", 1.6)},
   {"line": 2, "at": 2.0, "mouse": C(1450, 46)},
   {"line": 2, "at": 3.6, "mouse": C(1410, 354)},
   hl(2, 5.0, "netgroup", "Network · apps", "a video stream, no window", 3.6, "left"),
   hl(3, 0.4, "netgroup", "NDI · Syphon", "network · this Mac", 3.6, "left"),
  ]},
 "s2": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.2, "mouse": C(1358, 252)},
   {"line": 1, "at": 1.6, "mouse": C(1420, 381)},
   {"line": 1, "at": 2.0, "key": [0, True]},
   {"line": 1, "at": 2.2, "type": "Stage Lyrics", "gap": 0.07},
   {"line": 1, "at": 3.6, "key": [36]},
   hl(2, 0.6, "resrow", "1920×1080 · 29.97", "you choose", 3.0, "left"),
   {"line": 3, "at": 0.4, "mouse": C(1370, 433)},
   hl(3, 0.9, "alpharow", "On · transparent", "", 1.8, "left"),
   {"line": 3, "at": 2.9, "mouse": C(1475, 329)},
   {"line": 3, "at": 3.35, "mouse": ["move", *P(1300, 600)]},
   hl(3, 3.4, "bcell2", "B off", "", 1.8, "left"),
   {"line": 4, "at": 0.3, "mouse": C(1571, 310)},
   hl(4, 1.4, "state2", "On air", "0 receiving", 2.4, "left"),
  ]},
 "s3": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, "rest": True},
   {"line": 1, "at": 0.0, "sh": OBS + "front"},
   {"line": 1, "at": 0.6, **Z("z_obs", 1.35)},
   {"line": 1, "at": 1.0, "mouse": ["dbl", *P(811, 457)]},
   {"line": 1, "at": 3.0, "mouse": C(1418, 406)},
   hl(1, 4.0, "ndilist", "STAGE-MAC (Stage Lyrics)", "computer · stream", 3.0, "below"),
   {"line": 2, "at": 0.2, "mouse": C(1100, 428)},
   {"line": 2, "at": 1.1, "mouse": C(1428, 606)},
   {"line": 2, "at": 2.3, "mcp": [{"op": "present", "n": 2}]},
   hl(2, 3.0, "obsprev", "Over the camera", "OBS", 2.8, "below"),
   {"line": 3, "at": 0.2, "mcp": [{"op": "present", "n": 3}]},
   {"line": 4, "at": 0.0, "rest": True},
   {"line": 4, "at": 0.0, "sh": FRONT},
   {"line": 4, "at": 0.4, **Z("z_win", 1.6)},
   hl(4, 1.0, "state2", "On air", "1 receiving", 2.4, "left"),
   {"line": 5, "at": 0.3, "cap": "Renaming while it sends = a new stream · pick it again in each receiver", "capdur": 4.4},
   {"line": 5, "at": 5.4, "cap": "Mac: allow Local Network · Windows: allow LayerCue on Private networks", "capdur": 5.0},
   hl(6, 0.6, "audiorow", "Audio", "stage sound · off to begin with", 3.6, "below"),
  ]},
 "s4": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.2, "mouse": C(1400, 354)},
   {"line": 1, "at": 1.3, "mouse": C(1362, 275)},
   {"line": 1, "at": 2.6, "sh": OBS + "syphon &"},
   {"line": 1, "at": 3.0, "cap": "Syphon: Mac only · picture only, no sound", "capdur": 3.4},
   hl(2, 0.3, "syphonok", "A receiving app", "is connected", 2.4, "left"),
   hl(2, 3.2, "premult", "Premultiplied · Straight", "", 2.6, "left"),
  ]},
 "s5": {"setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 0.0, "rest": True},
   {"line": 1, "at": 0.4, "cap": "Fill = the picture · Key = white where it shows, black where the camera shows", "capdur": 5.4},
   {"line": 2, "at": 0.3, "mouse": C(1540, 46)},
   {"line": 2, "at": 1.2, **Z("z_win", 1.6)},
   hl(2, 2.0, "fillrow", "UltraStudio · SDI", "fill SDI A · key SDI B", 4.6, "left"),
   hl(3, 0.3, "sdirow", "SDI format", "match the switcher", 4.0, "left"),
   hl(4, 0.3, "keymix", "Keying · Mix", "External (usual)", 4.4, "left"),
   hl(5, 0.2, "alpha3", "Alpha", "the switcher's setting", 2.4, "left"),
   {"line": 6, "at": 0.6, "mouse": C(1475, 347)},
   {"line": 6, "at": 1.05, "mouse": ["move", *P(1300, 600)]},      # 칸 위에 두면 주황 미리보기로 B 가 켜진 듯 보였다(16편과 같다)
   hl(6, 1.2, "bcell3", "B off", "or the key is all white", 3.0, "left"),
  ]},
}
SL = {"_note": "17편 연출표 — NDI(Stage Lyrics, 투명, B 끔) → OBS(Camera = 무대 사진) · Syphon(OBS 연결만 — 그림은 뒤집혀 보여 이슈 #9, 화면에 안 넣음) · fill & key(UltraStudio Mini Replay 12G). (옛 16편: — 무대 모니터(BetterDisplay 가상 디스플레이 Stage Monitor) · Add screen · Send to · 이름 · Layers shown(B 끔) · Foreground 칩 · 온에어 목록 · Layout · 뽑기/꽂기. LG 녹화. (옛 15편 메모: — Files & YouTube · Import external files(USB 의 sponsor-reel) · Open → Finder(아이콘 보기, LG) · Backups · Reset 창 Cancel · 좁은 창 · Music 따로 창 · AI apps 화면 · Copy as HTML for AI → 답 붙여 넣기. LG 녹화.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
