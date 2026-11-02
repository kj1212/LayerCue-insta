#!/usr/bin/env python3
"""페이스북 페이지 커버 사진 — 인스타 카드(make-cards.py)와 같은 얼굴로.

    ~/.local/share/mflux-dev/bin/python3 tools/make-fb-cover.py   → brand/fb-cover.png

★ 크기와 안전 구역
  1640×624 로 만든다(데스크톱 표시 820×312 의 2배). 휴대폰은 같은 그림을 16:9 로
  보여 주느라 **양옆을 잘라** 가운데 약 1100 px 만 남는다. 데스크톱 새 페이지 화면은
  위아래를 조금 자른다. 그래서 글자는 전부 가운데 1040×520 안에 두고 양옆은 비운다.
  왼쪽 아래는 데스크톱에서 프로필 사진이 걸치는 자리이기도 하다.

★ 글자에 "beta"·"free"·버전 번호를 넣지 않는다 — 커버는 오래 걸려 있으니 지나가는 말은 뺀다.
"""
import os

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "video", "fonts", "Archivo.ttf")

W, H = 1640, 624
# 색·어긋남·자간은 make-cards.py 와 같은 값이다
VOID = (11, 11, 13)
CREAM = (242, 238, 228)
MUTE = (156, 152, 142)
FAINT = (103, 100, 93)
HOT = (255, 74, 26)
GHOSTS = [((255, 122, 0), -0.0028, -0.011),
          ((122, 43, 255), 0.0021, -0.005),
          ((0, 185, 108), 0.0031, 0.008)]
TRACK = -0.035

def font(size, weight=600, width=100):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight, width])
    return f


def tracked(d, text, f, cx, y, fill, track=0.0):
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x = cx - total / 2
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill)
        x += cw + track
    return total


def fit_size(word, target_w, weight=900, width=118):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = font(100, weight, width)
    w = probe.textlength(word, font=f) + TRACK * 100 * (len(word) - 1)
    return int(100 * target_w / w)


def word_layer(word, size, color, cy, dx=0, dy=0):
    im = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(size, 900, 118)
    track = TRACK * size
    widths = [d.textlength(c, font=f) for c in word]
    x = (W - sum(widths) - track * (len(word) - 1)) / 2 + dx
    top, bottom = f.getbbox(word)[1], f.getbbox(word)[3]
    y = cy - (top + bottom) / 2 + dy
    for c, cw in zip(word, widths):
        d.text((x, y), c, font=f, fill=color)
        x += cw + track
    return im


def main(out):
    img = Image.new("RGB", (W, H), VOID)
    d = ImageDraw.Draw(img)

    # 장식 없이 글자만 둔다 — 아이콘은 바로 아래 프로필 사진이 이미 보여 준다

    tracked(d, "[ A LIVE MEDIA PLAYER FOR THE BIG SCREEN ]", font(20, 500), W // 2, 118, FAINT, track=2.4)

    size = fit_size("LAYERCUE", 840)
    cy = 268
    # 어긋남은 카드(1080×1350)의 절반 — 가로 판에서는 같은 값이 두꺼운 색 띠로 보였다
    layers = Image.new("RGB", (W, H), (0, 0, 0))
    for color, fx, fy in GHOSTS:
        layers = ImageChops.screen(layers, word_layer("LAYERCUE", size, color, cy, fx * 540, fy * 675))
    img.paste(ImageChops.screen(img, layers))
    real = word_layer("LAYERCUE", size, CREAM, cy)
    img.paste(real, (0, 0), real.convert("L"))

    d = ImageDraw.Draw(img)
    f = font(40, 800, 96)
    a, b = "YOUR WHOLE SHOW IN ", "ONE WINDOW."
    wa = sum(d.textlength(c, font=f) for c in a) + 1.0 * (len(a) - 1)
    wb = sum(d.textlength(c, font=f) for c in b) + 1.0 * (len(b) - 1)
    x0 = W / 2 - (wa + 1.0 + wb) / 2
    tracked(d, a, f, x0 + wa / 2, 392, CREAM, track=1.0)
    tracked(d, b, f, x0 + wa + 1.0 + wb / 2, 392, HOT, track=1.0)

    tracked(d, "BACKGROUNDS · SLIDES · CAPTIONS · LOGOS · YOUTUBE", font(19, 500), W // 2, 470, MUTE, track=1.8)

    img.save(out)
    return out


if __name__ == "__main__":
    out = main(os.path.join(ROOT, "brand", "fb-cover.png"))
    print(f"  썼다: {out} ({W}×{H})")
