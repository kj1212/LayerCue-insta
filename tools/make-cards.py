#!/usr/bin/env python3
"""인스타그램 게시물 그림 — 홈페이지와 같은 얼굴로.

    python3 tools/make-ig.py            → public/ig/01.png …

★ 왜 따로 만드나
  링크 미리보기용(og-v2.png)은 1200×630 가로다. 인스타 피드에서 가로 그림은 제일 작게
  잡힌다 — **세로 4:5(1080×1350)** 가 화면을 가장 많이 차지한다. 그리고 카톡에서는 그림
  옆에 링크와 제목이 붙지만 인스타에서는 **이 그림 하나가 전부**라, 이름만 크게 있으면
  "그래서 뭐하는 건데" 가 남는다. 그래서 판을 다시 짠다.

★ 무엇을 물려받나
  글꼴(Archivo)·색·어긋난 층 세 벌은 make-og.py 와 같은 값을 쓴다. 홈페이지·미리보기·
  인스타가 한 얼굴이라야 한다. 색은 Hero.astro 의 .g1/.g2/.g3 값 그대로다.
"""
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "/Users/kj1212/projects/LayerCue/qml/assets/fonts/Archivo.ttf"
# 한글은 Archivo 에 글리프가 없다 — 앱과 같은 Pretendard 로 떨어뜨린다
KFONT = os.path.expanduser("~/Library/Fonts/Pretendard-SemiBold.otf")

W, H = 1080, 1350          # 4:5 — 피드에서 가장 큰 비율
VOID = (11, 11, 13)
CREAM = (242, 238, 228)
MUTE = (156, 152, 142)
FAINT = (103, 100, 93)
HOT = (255, 74, 26)

# ★ 층이 **모여 붙은 뒤**의 미세한 어긋남만 남긴다(리소 인쇄가 조금 떠는 정도).
#   들어올 때의 큰 어긋남을 그대로 쓰면 글자가 안 읽히는 색수차 덩어리가 된다.
GHOSTS = [((255, 122, 0), -0.0028, -0.011),     # 배경 — 호박
          ((122, 43, 255), 0.0021, -0.005),     # 전경 — 보라
          ((0, 185, 108), 0.0031, 0.008)]       # 오버레이 — 녹

TRACK = -0.035      # 홈페이지와 같은 자간(음수)


def font(size, weight=600, width=100):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight, width])
    return f


def kfont(size):
    return ImageFont.truetype(KFONT, size)


def tracked(d, text, f, cx, y, fill, track=0.0, anchor_left=None):
    """자간을 손으로 벌려 그린다. PIL 에는 자간이 없다."""
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x = (cx - total / 2) if anchor_left is None else anchor_left
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill)
        x += cw + track
    return total


def word_layer(word, size, color, y, dx=0, dy=0):
    """낱말 한 벌을 검은 판에 그린다. screen 으로 겹치려면 바탕이 검어야 한다."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(size, 900, 118)
    track = TRACK * size
    widths = [d.textlength(c, font=f) for c in word]
    total = sum(widths) + track * (len(word) - 1)
    x = (W - total) / 2 + dx
    top, bottom = f.getbbox(word)[1], f.getbbox(word)[3]
    yy = y - (top + bottom) / 2 + dy
    for c, cw in zip(word, widths):
        d.text((x, yy), c, font=f, fill=color)
        x += cw + track
    return im


def fit_size(word, target_w, weight=900, width=118):
    """낱말이 target_w 를 채우는 크기를 찾는다.
    ★ vw 어림이 아니라 **실측 진폭으로 나눈 값**이다 — 홈페이지가 쓰는 그 방법.
      눈대중으로 잡으면 좁은 자리에서 반드시 넘친다."""
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    size = 100
    f = font(size, weight, width)
    w = probe.textlength(word, font=f) + TRACK * size * (len(word) - 1)
    return int(size * target_w / w)


def base(footer_left="LAYERCUE.COM", footer_right="FREE BETA · MAC & WINDOWS"):
    """모든 장이 같은 바닥을 쓴다 — 넘겨 봐도 한 묶음으로 읽힌다."""
    img = Image.new("RGB", (W, H), VOID)
    d = ImageDraw.Draw(img)
    d.line([(72, H - 118), (W - 72, H - 118)], fill=(46, 46, 50), width=1)
    f2 = font(19, 700)
    d.text((72, H - 92), footer_left, font=f2, fill=FAINT)
    tw = d.textlength(footer_right, font=f2)
    d.text((W - 72 - tw, H - 92), footer_right, font=f2, fill=FAINT)
    d.rectangle([W - 72 - tw - 30, H - 88, W - 72 - tw - 16, H - 74], fill=HOT)
    return img, d


# ── 01. 얼굴 ────────────────────────────────────────────────────────────────
def slide01(out):
    img, d = base()

    # 위 — 무엇인지 한 줄. 인스타에서는 이 그림이 전부라 이름만 두면 안 된다.
    tracked(d, "[ macOS — public beta ]", font(22, 500), W // 2, 150, FAINT, track=2.6)

    # 가운데 — 큰 낱말. 층 세 벌을 screen 으로 겹쳐 어긋남을 남긴다.
    size = fit_size("LAYERCUE", W * 0.88)
    cy = 560
    layers = Image.new("RGB", (W, H), (0, 0, 0))
    for color, fx, fy in GHOSTS:
        layers = ImageChops.screen(layers, word_layer("LAYERCUE", size, color, cy, fx * W, fy * H))
    img_ = ImageChops.screen(img, layers)
    img.paste(img_)
    real = word_layer("LAYERCUE", size, CREAM, cy)
    img.paste(real, (0, 0), real.convert("L"))

    d = ImageDraw.Draw(img)
    # 아래 — 하는 일. 두 줄로 끊는다(한 줄이면 글자가 너무 작아진다)
    tracked(d, "A LIVE MEDIA PLAYER", font(46, 800, 96), W // 2, 760, CREAM, track=1.0)
    tracked(d, "FOR THE BIG SCREEN", font(46, 800, 96), W // 2, 820, CREAM, track=1.0)

    tracked(d, "BACKGROUNDS · SLIDES · CAPTIONS · LOGOS · YOUTUBE",
            font(21, 500), W // 2, 930, MUTE, track=1.8)

    img.save(out)
    return out


# ── 02. 층 ──────────────────────────────────────────────────────────────────
# ★ 판의 꼭짓점은 앱 아이콘·상단 마크와 **같은 식**이다(Nav.astro 의 그 polygon).
#   각 38° · 평면비 8:5.5. 여기서 새로 지어내면 아이콘과 다른 물건이 된다.
PLATE_R = (5.72, 4.46)      # 오른쪽으로 가는 변
PLATE_L = (-8.32, 6.50)     # 왼쪽으로 가는 변
PLATE_GAP = 4.60            # 층 사이 간격(같은 단위)


def plate(d, cx, cy, k, fill=None, outline=None, wid=3):
    """등각 판 하나. k = 배율."""
    rx, ry = PLATE_R[0] * k, PLATE_R[1] * k
    lx, ly = PLATE_L[0] * k, PLATE_L[1] * k
    p0 = (cx - (rx + lx) / 2, cy - (ry + ly) / 2)
    pts = [p0, (p0[0] + rx, p0[1] + ry), (p0[0] + rx + lx, p0[1] + ry + ly), (p0[0] + lx, p0[1] + ly)]
    d.polygon(pts, fill=fill, outline=outline, width=wid)
    return pts


def slide02(out):
    img, d = base()
    tracked(d, "[ 02 — LAYERS ]", font(22, 500), W // 2, 118, FAINT, track=2.6)

    size = fit_size("SEVEN LAYERS.", W * 0.82, 900, 84)
    tracked(d, "ONE SCREEN.", font(size, 900, 84), W // 2, 168, CREAM, track=TRACK * size)
    tracked(d, "SEVEN LAYERS.", font(size, 900, 84), W // 2, 168 + size * 0.92, CREAM, track=TRACK * size)

    # ★ 판마다 **바탕색으로 채운다.** 처음엔 테두리만 그렸더니 일곱 장이 서로 뚫려
    #   그물처럼 보였다 — 쌓인 것으로 안 읽힌다. 채워야 위 판이 아래 판을 가린다.
    # ★ 그리는 차례도 중요하다. **화면 아래(=뒤쪽)부터** 그려야 위 판이 나중에 덮는다.
    k, cx, top_y = 17.0, W // 2 + 40, 545
    gap = 46
    rows = ([("#3FB27F", "OVERLAYS  ×5")] + [("#3FB27F", None)] * 4
            + [("#8B9BF0", "FOREGROUND"), ("#D98A2B", "BACKGROUND")])
    ys = [top_y + i * gap for i in range(len(rows))]

    for i in range(len(rows) - 1, -1, -1):        # 뒤에서 앞으로
        color, _ = rows[i]
        fill = "#2A1C0C" if i == len(rows) - 1 else VOID   # 배경 판만 살짝 물들여 '바탕' 임을 보인다
        plate(d, cx, ys[i], k, fill=fill, outline=color, wid=4)

    # 이름표 — 판과 같은 높이에 두고 가는 선으로 잇는다
    for i, (color, label) in enumerate(rows):
        if not label:
            continue
        y = ys[i]
        f = font(21, 700)
        tw = d.textlength(label, font=f)
        d.text((96, y - 12), label, font=f, fill=color)
        d.line([(96 + tw + 16, y), (cx - 8.32 * k / 2 - 14, y)], fill=(52, 52, 58), width=1)

    tracked(d, "EACH ONE CUES ON ITS OWN.", font(30, 700, 96), W // 2, H - 210, CREAM, track=1.4)
    tracked(d, "CHANGE ONE, THE REST DON\u2019T MOVE.", font(22, 500), W // 2, H - 165, MUTE, track=1.6)
    img.save(out); return out


# ── 03. 큐 ──────────────────────────────────────────────────────────────────
def slide03(out):
    img, d = base()
    tracked(d, "[ 03 — CUES ]", font(22, 500), W // 2, 118, FAINT, track=2.6)

    size = fit_size("CLICK A SLIDE.", W * 0.80, 900, 84)
    tracked(d, "CLICK A SLIDE.", font(size, 900, 84), W // 2, 168, CREAM, track=TRACK * size)
    tracked(d, "IT\u2019S LIVE.", font(size, 900, 84), W // 2, 168 + size * 0.92, HOT, track=TRACK * size)

    rows = [("Q1", "Corner logo",  "5 overlay · image",      "#3FB27F", True),
            ("Q2", "Speaker",      "1 overlay · lower third", "#3FB27F", True),
            ("Q3", "Title slide",  "foreground · text",      "#8B9BF0", False),
            ("Q4", "Background",   "video · loops",          "#D98A2B", True)]
    x0, y0, rw, rh = 78, 520, W - 156, 104
    for i, (no, name, sub, color, live) in enumerate(rows):
        y = y0 + i * (rh + 14)
        d.rectangle([x0, y, x0 + rw, y + rh], fill=(22, 22, 26))
        d.rectangle([x0, y, x0 + 8, y + rh], fill=color)          # 층 색 막대
        d.text((x0 + 34, y + 26), no, font=font(24, 700), fill=FAINT)
        d.text((x0 + 108, y + 20), name, font=font(30, 800, 96), fill=CREAM)
        d.text((x0 + 108, y + 60), sub, font=font(20, 400), fill=FAINT)
        if live:
            tw = d.textlength("LIVE", font=font(22, 800))
            d.ellipse([x0 + rw - 40 - tw - 26, y + rh / 2 - 7, x0 + rw - 40 - tw - 12, y + rh / 2 + 7], fill=HOT)
            d.text((x0 + rw - 34 - tw, y + rh / 2 - 13), "LIVE", font=font(22, 800), fill=CREAM)
        else:
            tw = d.textlength("OFF", font=font(22, 700))
            d.text((x0 + rw - 34 - tw, y + rh / 2 - 13), "OFF", font=font(22, 700), fill=FAINT)

    tracked(d, "ONE CLICK SENDS A LAYER LIVE.", font(30, 700, 96), W // 2, H - 210, CREAM, track=1.4)
    tracked(d, "CLICK IT AGAIN AND IT COMES DOWN.", font(22, 500), W // 2, H - 165, MUTE, track=1.6)
    img.save(out); return out


# ── 04. 자세히 ──────────────────────────────────────────────────────────────
def slide04(out):
    img, d = base()
    tracked(d, "[ 04 — DETAILS ]", font(22, 500), W // 2, 118, FAINT, track=2.6)

    size = fit_size("SMALL THINGS", W * 0.80, 900, 84)
    tracked(d, "SMALL THINGS", font(size, 900, 84), W // 2, 168, CREAM, track=TRACK * size)
    tracked(d, "THAT HOLD UP.", font(size, 900, 84), W // 2, 168 + size * 0.92, CREAM, track=TRACK * size)

    items = [("TRIM WITHOUT EDITING", "Set IN and OUT. The file never changes."),
             ("FIT WITHOUT PHOTOSHOP", "Scale and crop right where it sits."),
             ("YOUTUBE, AS A SLIDE", "Drop a link. Captions and speed included."),
             ("SCREENS YOU DON\u2019T HAVE YET", "Build against a virtual screen first.")]
    y = 500
    for head, body in items:
        d.rectangle([78, y + 6, 92, y + 20], fill=HOT)
        d.text((116, y - 4), head, font=font(30, 800, 96), fill=CREAM)
        d.text((116, y + 40), body, font=font(22, 400), fill=MUTE)
        y += 118

    tracked(d, "ON STAGE, THE SMALL THINGS ARE THE THING.",
            font(22, 500), W // 2, H - 165, MUTE, track=1.6)
    img.save(out); return out


# ── 05. 받기 ────────────────────────────────────────────────────────────────
def slide05(out):
    # 큰 글씨로 주소를 이미 외치므로 바닥 왼쪽은 만든 사람 자리로 넘긴다
    img, d = base(footer_left="MADE BY CASTPAD", footer_right="APPLE SILICON & INTEL")
    tracked(d, "[ 06 — BETA ]", font(22, 500), W // 2, 118, FAINT, track=2.6)

    size = fit_size("WHILE IT\u2019S", W * 0.74, 900, 84)
    tracked(d, "FREE", font(size, 900, 84), W // 2, 300, CREAM, track=TRACK * size)
    tracked(d, "WHILE IT\u2019S", font(size, 900, 84), W // 2, 300 + size * 0.92, CREAM, track=TRACK * size)
    tracked(d, "BETA.", font(size, 900, 84), W // 2, 300 + size * 1.84, HOT, track=TRACK * size)

    d.line([(W * 0.30, 800), (W * 0.70, 800)], fill=(46, 46, 50), width=1)

    lines = [("PLATFORM", "macOS 13 or later"),
             ("CHIP", "Apple silicon & Intel"),
             ("PRICE", "free during the beta"),
             ("WINDOWS", "in development")]
    y = 850
    for k, v in lines:
        d.text((160, y), k, font=font(20, 700), fill=FAINT)
        tw = d.textlength(v, font=font(24, 500))
        d.text((W - 160 - tw, y - 2), v, font=font(24, 500), fill=CREAM)
        d.line([(160, y + 40), (W - 160, y + 40)], fill=(30, 30, 34), width=1)
        y += 62

    size2 = fit_size("LAYERCUE.COM", W * 0.62, 900, 100)
    tracked(d, "LAYERCUE.COM", font(size2, 900, 100), W // 2, H - 215, CREAM, track=TRACK * size2)
    img.save(out); return out


if __name__ == "__main__":
    outdir = os.path.join(ROOT, "public", "ig")
    os.makedirs(outdir, exist_ok=True)
    for i, fn in enumerate([slide01, slide02, slide03, slide04, slide05], 1):
        p = fn(os.path.join(outdir, f"{i:02d}.png"))
        print(f"  썼다: {p}")
    print(f"({W}×{H}, 4:5)")
    sys.exit(0)
