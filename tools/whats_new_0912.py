#!/usr/bin/env python3
"""8월 소개 게시물 뒤로 새로 생긴 것(0.9.4 → 0.9.12) — 6장 캐러셀.

    python3 tools/whats_new_0912.py   → posts/2026-10-29-whats-new/1.jpg … 6.jpg

판·글꼴·색은 make-cards.py(사이트 make-ig.py 사본)의 것을 그대로 쓴다 — 8월 소개 다섯 장과
넘겨 봤을 때 한 묶음으로 읽혀야 한다. 인스타 API 는 JPEG 만 받으므로 jpg 로 쓴다.
"""
import importlib.util
import os

from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cards", os.path.join(HERE, "make-cards.py"))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
W, H = c.W, c.H
OUT = os.path.join(os.path.dirname(HERE), "posts", "2026-10-29-whats-new")


def headline(d, top, bottom, bottom_color=c.CREAM, y=168):
    # 장마다 글자 크기가 다르면 넘길 때 덜컹거린다 — 가장 긴 제목(EVERY SCREEN)에 맞춘 한 크기
    size = c.fit_size("EVERY SCREEN", W * 0.80, 900, 84)
    c.tracked(d, top, c.font(size, 900, 84), W // 2, y, c.CREAM, track=c.TRACK * size)
    c.tracked(d, bottom, c.font(size, 900, 84), W // 2, y + size * 0.92, bottom_color, track=c.TRACK * size)


def items(d, rows, y=500, step=118):
    for head, body in rows:
        d.rectangle([78, y + 6, 92, y + 20], fill=c.HOT)
        d.text((116, y - 4), head, font=c.font(30, 800, 96), fill=c.CREAM)
        d.text((116, y + 40), body, font=c.font(22, 400), fill=c.MUTE)
        y += step


def table(d, rows, y):
    for k, v in rows:
        d.text((160, y), k, font=c.font(20, 700), fill=c.FAINT)
        tw = d.textlength(v, font=c.font(24, 500))
        d.text((W - 160 - tw, y - 2), v, font=c.font(24, 500), fill=c.CREAM)
        d.line([(160, y + 40), (W - 160, y + 40)], fill=(30, 30, 34), width=1)
        y += 62


def footnote(d, strong, soft):
    c.tracked(d, strong, c.font(30, 700, 96), W // 2, H - 210, c.CREAM, track=1.4)
    c.tracked(d, soft, c.font(22, 500), W // 2, H - 165, c.MUTE, track=1.6)


# ── 1. 표지 — 소개 게시물의 어긋난 층 글자를 「NEW」에 다시 쓴다 ──────────────────
def s1():
    img, d = c.base()
    c.tracked(d, "[ 0.9.4 → 0.9.12 ]", c.font(22, 500), W // 2, 150, c.FAINT, track=2.6)
    c.tracked(d, "WHAT’S", c.font(64, 900, 100), W // 2, 330, c.MUTE, track=c.TRACK * 64)

    size = c.fit_size("NEW", W * 0.70)
    cy = 560
    layers = Image.new("RGB", (W, H), (0, 0, 0))
    for color, fx, fy in c.GHOSTS:
        layers = ImageChops.screen(layers, c.word_layer("NEW", size, color, cy, fx * W, fy * H))
    img.paste(ImageChops.screen(img, layers))
    real = c.word_layer("NEW", size, c.CREAM, cy)
    img.paste(real, (0, 0), real.convert("L"))

    d = ImageDraw.Draw(img)
    c.tracked(d, "SINCE AUGUST, IN LAYERCUE", c.font(40, 800, 96), W // 2, 800, c.CREAM, track=1.0)
    c.tracked(d, "WINDOWS · EVERY SCREEN · NDI® · SDI · POWERPOINT · AI",
              c.font(20, 500), W // 2, 900, c.MUTE, track=1.6)
    return img


# ── 2. 윈도우 ─────────────────────────────────────────────────────────────────
def s2():
    img, d = c.base()
    c.tracked(d, "[ 01 — WINDOWS ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    headline(d, "NOW ON", "WINDOWS.", c.HOT)
    table(d, [("WINDOWS", "Microsoft Store · Windows 10 & 11"),
              ("MAC", "macOS 13+ · Apple silicon & Intel"),
              ("UPDATES", "the Store keeps it current"),
              ("PRICE", "free on both during the beta")], 560)
    footnote(d, "SAME LAYERS. SAME ONE-CLICK CUES.", "NOW ON THE PC IN THE BOOTH, TOO.")
    return img


# ── 3. 출력 ───────────────────────────────────────────────────────────────────
def s3():
    img, d = c.base()
    c.tracked(d, "[ 02 — OUTPUT ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    headline(d, "EVERY SCREEN", "IN THE ROOM.")
    items(d, [("MULTI-OUTPUT", "One stage on as many monitors as you have."),
              ("NDI® & SYPHON", "Send the stage to other computers and apps."),
              ("BLACKMAGIC SDI", "Straight out of DeckLink and UltraStudio (Mac)."),
              ("FILL & KEY", "Graphics over a switcher, frame-locked.")])
    footnote(d, "AND NOW WITH SOUND.", "MUSIC AND VIDEO RIDE ALONG OVER NDI® AND SDI.")
    return img


# ── 4. 가져오기 ───────────────────────────────────────────────────────────────
def s4():
    img, d = c.base()
    c.tracked(d, "[ 03 — BRING IT IN ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    headline(d, "BRING WHAT", "YOU HAVE.")
    items(d, [("POWERPOINT, STILL EDITABLE", "Text comes in as text. Pictures as pictures."),
              ("PDF IN AND OUT", "Pages in as 4K pictures. Text out as text."),
              ("FIND INSIDE THE LYRICS", "Search every song without opening one."),
              ("CUE SHEETS", "Fix a slide once. It’s fixed everywhere.")])
    footnote(d, "LIBRARIES FOR THE SONGS.", "CUE SHEETS FOR THE NIGHT.")
    return img


# ── 5. AI ─────────────────────────────────────────────────────────────────────
def s5():
    img, d = c.base()
    c.tracked(d, "[ 04 — AI ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    headline(d, "ASK FOR", "THE SLIDES.", c.HOT)

    # 말풍선 둘 — 실제로 하는 말 그대로
    asks = ["“Make slides from these lyrics.”",
            "“Darken the background and make the title bigger.”"]
    y = 520
    for a in asks:
        f = c.font(26, 600, 96)
        tw = d.textlength(a, font=f)
        x1 = W - 78
        x0 = max(78, x1 - tw - 64)
        d.rounded_rectangle([x0, y, x1, y + 84], radius=18, fill=(22, 22, 26))
        d.text((x0 + 32, y + 26), a, font=f, fill=c.CREAM)
        y += 112
    d.text((78, y + 20), "LayerCue checks what it drew — overflow, contrast, overlaps —",
           font=c.font(22, 400), fill=c.MUTE)
    d.text((78, y + 54), "and the AI fixes its own work. Every edit undoes.", font=c.font(22, 400), fill=c.MUTE)

    footnote(d, "CLAUDE · LM STUDIO · CURSOR", "ONE BUTTON IN SETTINGS › AI APPS.")
    return img


# ── 6. 받기 ───────────────────────────────────────────────────────────────────
def s6():
    img, d = c.base(footer_left="MADE BY CASTPAD", footer_right="MAC & WINDOWS")
    c.tracked(d, "[ 0.9.12 — BETA ]", c.font(22, 500), W // 2, 118, c.FAINT, track=2.6)
    size = c.fit_size("WHILE IT’S", W * 0.74, 900, 84)
    c.tracked(d, "FREE", c.font(size, 900, 84), W // 2, 300, c.CREAM, track=c.TRACK * size)
    c.tracked(d, "WHILE IT’S", c.font(size, 900, 84), W // 2, 300 + size * 0.92, c.CREAM, track=c.TRACK * size)
    c.tracked(d, "BETA.", c.font(size, 900, 84), W // 2, 300 + size * 1.84, c.HOT, track=c.TRACK * size)
    d.line([(W * 0.30, 800), (W * 0.70, 800)], fill=(46, 46, 50), width=1)
    table(d, [("VERSION", "0.9.12"),
              ("MAC", "macOS 13+ · Apple silicon & Intel"),
              ("WINDOWS", "Microsoft Store"),
              ("PRICE", "free during the beta")], 850)
    size2 = c.fit_size("LAYERCUE.COM", W * 0.62, 900, 100)
    c.tracked(d, "LAYERCUE.COM", c.font(size2, 900, 100), W // 2, H - 215, c.CREAM, track=c.TRACK * size2)
    return img


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = []
    for i, fn in enumerate([s1, s2, s3, s4, s5, s6], 1):
        p = os.path.join(OUT, f"{i}.jpg")
        fn().convert("RGB").save(p, quality=95, subsampling=0)
        names.append(f"{i}.jpg")
        print("썼다:", p)
