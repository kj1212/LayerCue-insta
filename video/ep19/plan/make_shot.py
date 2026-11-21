#!/usr/bin/env python3
"""19편 연출표 — shotlist2.json · regions.json.   python3 ep19/plan/make_shot.py
좌표: 클릭은 LG 캡처 px(= peek-s × 2.4, y + 60), 영역은 창 px(= peek-s × 2.4).
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
D = {k: v["seconds"] for k, v in json.load(open(H / "audio/vo-heart/lines.json")).items()}
def end(seg, n, back=0.0): return round(D[f"{seg}-l{n:02d}"] - back, 2)
k = lambda x0, y0, x1, y1: [round(x0 * 2.4), round(y0 * 2.4), round((x1 - x0) * 2.4), round((y1 - y0) * 2.4)]
R = {
 "inset": [3060, 36, 720, 405], "updbtn": k(8, 33, 135, 53), "bolt": k(136, 33, 158, 53), "title2": k(451, 390, 1315, 482),
 "picker": k(551, 130, 770, 525), "rect": k(895, 572, 1255, 705), "dot": k(905, 572, 921, 587),
 "link": k(962, 571, 979, 589), "bar": k(190, 344, 353, 352), "card1": k(188, 343, 353, 436),
 "strip": k(187, 210, 453, 227), "layercol": k(463, 64, 489, 209), "preview": k(186, 38, 455, 227),
}
c = lambda x, y: ["click", x, y]
Z = lambda r, s: {"zoom": r, "scale": s, "center": [1920, 1080]}
def hl(line, at, r, a, b, dur, side="below"): return {"line": line, "at": at, "hl": r, "lbl": [a, b], "lblSide": side, "dur": dur, "exact": True}
P = lambda x, y: [round(x * 2.4), round(y * 2.4 + 60)]
C = lambda x, y: ["click", *P(x, y)]
AUD = lambda name: {"sh": f"mkdir -p rec/v2/aud; screencapture -x -D 3 rec/v2/aud/{name}.png &"}      # 관객 화면 정지 사진(inset.py 가 오른쪽 위 작은 창으로)
SNAP = lambda line, at, name: {"line": line, "at": at, **AUD(name)}
# 기능 카드 = 장면 전환(타이틀처럼 화면 전체) — 구간 앞에 pre 초를 더 두고, 첫 줄 until 초까지 덮는다(card-anim.html)
CARD = lambda pre, at: {"pre": pre, "until": {"line": 1, "at": at}}
S = {
 "s1": {"card": CARD(0.8, 4.1), "setup": [{"mcp": [{"op": "clear", "layer": "all"}, {"op": "usePt", "name": "Prize Night 2026"}, {"op": "output", "on": True}, {"op": "present", "n": 2}]}, {"sleep": 1.5}, {"front": 1}, {"sleep": 0.4}, {"mouse": C(900, 700)}, {"sleep": 0.4}, {"mouse": ["jump", 2600, 1700]}],      # 송출 창이 뜨며 앞을 가져간다 — 빈 곳을 한 번 눌러 되찾는다
  "events": [
   SNAP(1, 0.0, "s1-0"),
   {"line": 1, "at": 2.4, "mouse": C(120, 858)},
   {"line": 1, "at": 3.6, "mouse": C(79, 195)},
   {"line": 2, "at": 0.3, "mouse": ["dbl", *P(940, 424)]},
   {"line": 2, "at": 1.0, "key": [124, True]},
   *[{"line": 2, "at": round(1.25 + i * 0.12, 2), "key": [51]} for i in range(5)],
   {"line": 2, "at": 2.0, "type": "19:00", "gap": 0.1},
   {"line": 2, "at": 3.1, "key": [53]},
   {"line": 2, "at": 3.5, "mouse": C(1340, 650)},
   SNAP(2, 3.9, "s1-1"),
   hl(3, 0.3, "inset", "Audience screen", "still 18:30", 2.8, "left"),
   hl(3, 3.6, "updbtn", "Update output", "", 2.2, "right"),
   {"line": 4, "at": 0.4, "mouse": C(63, 43)},
   SNAP(4, 0.9, "s1-2"),
   hl(4, 1.0, "inset", "Audience screen", "now 19:00", 2.0, "left"),
   {"line": 5, "at": 2.6, "mouse": C(146, 43)},
   hl(5, 3.0, "bolt", "Live updates", "", 2.4, "right"),
  ]},
 "s2": {"card": CARD(1.8, 1.45), "setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   SNAP(1, 0.0, "s2-0"),
   {"line": 1, "at": 1.8, "mouse": C(880, 424)},
   {"line": 1, "at": 2.6, "mouse": C(659, 108)},
   {"line": 1, "at": 3.6, "mouse": C(651, 144)},
   hl(1, 4.2, "picker", "Linear · Radial", "", 1.8, "right"),
   {"line": 2, "at": 0.1, "mouse": C(660, 439)},
   {"line": 2, "at": 0.4, "key": [0, True]},
   {"line": 2, "at": 0.6, "type": "FFC94D", "gap": 0.06},
   {"line": 2, "at": 1.2, "key": [36]},
   SNAP(2, 1.45, "s2-1"),
   {"line": 2, "at": 1.6, "mouse": C(760, 181)},
   {"line": 2, "at": 2.1, "mouse": C(660, 439)},
   {"line": 2, "at": 2.4, "key": [0, True]},
   {"line": 2, "at": 2.6, "type": "FF5E8A", "gap": 0.06},
   {"line": 2, "at": 3.2, "key": [36]},
   SNAP(2, 3.45, "s2-2"),
   {"line": 2, "at": 3.7, "mouse": C(679, 261)},
   SNAP(2, 4.2, "s2-3"),
   {"line": 3, "at": 0.3, "key": [53]},
   {"line": 3, "at": 0.7, "mouse": C(1340, 650)},
   hl(3, 1.0, "title2", "On the letters", "not the box", 2.4),
   hl(3, 3.6, "inset", "Audience screen", "already live", 2.2, "left"),
  ]},
 "s3": {"card": CARD(0.6, 3.6), "setup": [{"mcp": [{"op": "clear", "layer": "all"}]}, {"mouse": ["jump", 2600, 1700]}],
  "events": [      # 첫 줄은 카드 아래에서 사각형을 그린다 — 카드가 걷히면 손잡이가 달린 상자
   {"line": 1, "at": -0.4, "mouse": C(79, 372)},       # 클릭 한 번 ≈ 0.9 초 — 사각형은 첫 줄 +3.9 초쯤 다 그려진다(카드는 +3.6 부터 걷힌다)
   {"line": 1, "at": 0.2, "mouse": C(323, 45)},
   {"line": 1, "at": 0.6, "mouse": ["drag", *P(900, 580), *P(1250, 700)]},
   {**hl(2, 0.2, "dot", "Corner radius", "", 1.4, "left"), "nosync": True},      # 앞 동작이 늦어 테가 0.4 초만 떴다 — 계획 시각 그대로(사각형은 이미 다 그려졌다)
   {"line": 2, "at": 0.6, "mouse": ["drag", *P(913, 579), *P(955, 579)]},
   # 링크(손잡이 바로 오른쪽 고리)를 풀면 모서리마다 점 넷 — 오른쪽 위 · 왼쪽 아래를 0 으로(바깥쪽으로 끌면 줄어든다)
   # ★ 끌기 한 번 ≈ 2.1 초(down +0.75 · up +2.1) — 동작은 차례로 일어나니 2.2 초보다 좁게 두면 밀린다(첫 재녹화는 slowdrag 2.6 초씩 밀려 끝이 잘렸다)
   hl(3, 0.2, "link", "Link", "", 1.4, "above"),
   {"line": 3, "at": 0.8, "mouse": C(970, 580)},
   {"line": 3, "at": 2.0, "mouse": ["drag", *P(1193, 579), *P(1252, 579)]},
   {"line": 3, "at": 4.2, "mouse": ["drag", *P(956, 699), *P(898, 699)]},
   hl(3, 6.5, "rect", "Only the corners", "you pick", 1.8),
   # 기울이기: 좌우 = 아랫변 가운데 + 24 pt(창 20 px) · 위아래 = 오른쪽 변 가운데 **아래** 24 pt — 첫 녹화는 가운데(640)를 끌어 안 바뀌었다
   {"line": 4, "at": 0.6, "mouse": ["drag", *P(1095, 700), *P(1138, 700)]},
   {"line": 4, "at": 2.8, "mouse": ["drag", *P(1250, 660), *P(1250, 646)]},
   hl(4, 5.1, "rect", "Rounded and slanted", "", 2.0),
  ]},
 "s5": {"card": CARD(3.0, 0.0), "setup": [{"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 1.6, "mouse": C(45, 858)},
   {"line": 1, "at": 2.6, "mouse": C(80, 585)},
   {"line": 1, "at": 3.6, "mouse": C(270, 390)},
   hl(2, 0.3, "bar", "Time left", "Auto-dismiss 8 s", 3.4),
  ]},
 "s6": {"card": CARD(1.9, 1.35), "setup": [{"mcp": [{"op": "clear", "layer": "all"}]}, {"mouse": ["jump", 2600, 1700]}],
  "events": [
   {"line": 1, "at": 1.4, **Z("preview", 1.6)},
   hl(1, 2.6, "strip", "1 2 3 4 5 F B", "", 3.2),
   hl(1, 5.8, "layercol", "Same order", "as the layer column", 2.6, "right"),
  ]},
}
SL = {"_note": "19편 What\'s New 0.9.14 — Update output(관객 화면 = Stage Monitor 를 따로 찍어 오른쪽 위 작은 창으로) · 그라데이션 · 핸들(모서리 링크) · Auto-dismiss 막대 · 레이어 칸 순서. 가상 화면 Rec 4K 녹화. (옛 18편: — Tools Check(0.9.13 available) · Import · File missing → 메뉴 Locate file(카드 위 단추는 이슈 #10) · 편집 잠금 · 케이블 뽑기 · 정리 순서 · 끝내기. (옛 17편: — NDI(Stage Lyrics, 투명, B 끔) → OBS(Camera = 무대 사진) · Syphon(OBS 연결만 — 그림은 뒤집혀 보여 이슈 #9, 화면에 안 넣음) · fill & key(UltraStudio Mini Replay 12G). (옛 16편: — 무대 모니터(BetterDisplay 가상 디스플레이 Stage Monitor) · Add screen · Send to · 이름 · Layers shown(B 끔) · Foreground 칩 · 온에어 목록 · Layout · 뽑기/꽂기. LG 녹화. (옛 15편 메모: — Files & YouTube · Import external files(USB 의 sponsor-reel) · Open → Finder(아이콘 보기, LG) · Backups · Reset 창 Cancel · 좁은 창 · Music 따로 창 · AI apps 화면 · Copy as HTML for AI → 답 붙여 넣기. LG 녹화.",
      "title_sec": 6.0, "lead": 0.45, "gap": 0.42, "pre": 1.0, "rec_t0": 1.0, "segments": S}
json.dump(SL, open(H / "shotlist2.json", "w"), indent=1, ensure_ascii=False)
json.dump(R, open(H / "regions.json", "w"), indent=1)
print("ok")
