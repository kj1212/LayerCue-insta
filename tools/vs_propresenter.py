#!/usr/bin/env python3
"""「ProPresenter 값이 부담됐다면」 — 4장 캐러셀.

    python3 tools/vs_propresenter.py   → posts/2026-10-30-propresenter/1.jpg … 4.jpg

★ 남의 제품 이름을 건 글이다. 지키는 것 둘:
  - 값은 공식 페이지(renewedvision.com/propresenter/#pricing, 2026-10-29 확인)에 적힌 그대로.
    바뀌면 PRICE 와 캡션을 같이 고친다.
  - 깎아내리지 않는다. 「다 쓰면 그대로 쓰라」를 3장에 적는다 — 이 글의 신용이 거기서 나온다.
판은 whats_new_0912.py 의 것을 그대로 쓴다.
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wn", os.path.join(HERE, "whats_new_0912.py"))
wn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wn)
c, W, H = wn.c, wn.W, wn.H
OUT = os.path.join(os.path.dirname(HERE), "posts", "2026-10-30-propresenter")

PRICE = "$289"
SOURCE = "*PROPRESENTER STANDARD, PER SEAT, BILLED YEARLY — RENEWEDVISION.COM, OCT 2026"


# ── 1. 값 ─────────────────────────────────────────────────────────────────────
def s1():
    img, d = c.base()
    c.tracked(d, "[ FOR THE REST OF US ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    size = c.fit_size("PER COMPUTER.*", W * 0.84, 900, 84)     # 긴 줄에 맞춘다
    c.tracked(d, f"{PRICE} A YEAR,", c.font(size, 900, 84), W // 2, 300, c.CREAM, track=c.TRACK * size)
    c.tracked(d, "PER COMPUTER.*", c.font(size, 900, 84), W // 2, 300 + size * 0.92, c.HOT, track=c.TRACK * size)

    c.tracked(d, "THAT’S PROPRESENTER.", c.font(40, 800, 96), W // 2, 720, c.CREAM, track=1.0)
    c.tracked(d, "FOR A LOT OF ROOMS, THAT’S THE WHOLE MEDIA BUDGET.",
              c.font(22, 500), W // 2, 790, c.MUTE, track=1.6)
    c.tracked(d, SOURCE, c.font(15, 500), W // 2, H - 160, c.FAINT, track=1.2)
    return img


# ── 2. 실제로 쓰는 것 ──────────────────────────────────────────────────────────
def s2():
    img, d = c.base()
    c.tracked(d, "[ WHAT ROOMS ACTUALLY RUN ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    wn.headline(d, "MOST NIGHTS,", "IT’S THIS.")
    wn.items(d, [("A BACKGROUND THAT LOOPS", "Video or still, under everything else."),
                 ("THE WORDS", "Lyrics and slides, one click each."),
                 ("CAPTIONS & A LOGO", "Over the top, on their own layers."),
                 ("YOUTUBE & VIDEO", "Drop a link. It plays on the big screen."),
                 ("A SECOND SCREEN THAT BEHAVES", "Or five. Plus NDI® and SDI.")],
             y=480, step=104)
    wn.footnote(d, "LAYERCUE DOES THESE.", "FREE WHILE IT’S IN BETA.")
    return img


# ── 3. 정직하게 ───────────────────────────────────────────────────────────────
def s3():
    img, d = c.base()
    c.tracked(d, "[ HONESTLY ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    wn.headline(d, "KEEP IT.", "OR DON’T.", c.HOT)

    blocks = [("IF YOU USE ALL OF IT —", "keep ProPresenter. It’s good software,",
               "and it does far more than we do."),
              ("IF YOU MOSTLY CUE A BACKGROUND,", "the words and a logo — try LayerCue",
               "before you renew.")]
    y = 520
    for head, a, b in blocks:
        d.rectangle([78, y + 6, 92, y + 20], fill=c.HOT)
        d.text((116, y - 4), head, font=c.font(30, 800, 96), fill=c.CREAM)
        d.text((116, y + 44), a, font=c.font(24, 400), fill=c.MUTE)
        d.text((116, y + 80), b, font=c.font(24, 400), fill=c.MUTE)
        y += 180
    wn.footnote(d, "YOUR POWERPOINT COMES WITH YOU.", "IT OPENS AS SLIDES YOU CAN STILL EDIT.")
    return img


# ── 4. 받기 ───────────────────────────────────────────────────────────────────
def s4():
    img, d = c.base(footer_left="MADE BY CASTPAD", footer_right="MAC & WINDOWS")
    c.tracked(d, "[ 0.9.12 — BETA ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    size = c.fit_size("THIS SUNDAY.", W * 0.80, 900, 84)
    c.tracked(d, "TRY IT", c.font(size, 900, 84), W // 2, 330, c.CREAM, track=c.TRACK * size)
    c.tracked(d, "THIS SUNDAY.", c.font(size, 900, 84), W // 2, 330 + size * 0.92, c.HOT, track=c.TRACK * size)
    d.line([(W * 0.30, 800), (W * 0.70, 800)], fill=(46, 46, 50), width=1)
    wn.table(d, [("PRICE", "free during the beta"),
                 ("MAC", "macOS 13+ · Apple silicon & Intel"),
                 ("WINDOWS", "Microsoft Store"),
                 ("BRING", "PowerPoint · PDF · your videos")], 850)
    size2 = c.fit_size("LAYERCUE.COM", W * 0.62, 900, 100)
    c.tracked(d, "LAYERCUE.COM", c.font(size2, 900, 100), W // 2, H - 215, c.CREAM, track=c.TRACK * size2)
    return img


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([s1, s2, s3, s4], 1):
        p = os.path.join(OUT, f"{i}.jpg")
        fn().convert("RGB").save(p, quality=95, subsampling=0)
        print("썼다:", p)
