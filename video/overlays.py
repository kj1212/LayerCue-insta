#!/usr/bin/env python3
"""AE 에 얹을 글자 그림 — 소리 끄고 보는 사람을 위한 자막과 「LIVE」 표. AE 에는 Archivo 가 없을 수 있어 그림으로 굽는다.

    $VENV/bin/python overlays.py   → overlays/*.png (1080 폭, 투명 바탕)
"""
import os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import importlib.util
spec = importlib.util.spec_from_file_location("cards", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "make-cards.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overlays")
os.makedirs(OUT, exist_ok=True)


def caption(name, text, hot=None):
    """아래쪽 자막 — 크게, 가운데. hot 은 주황으로 칠할 낱말."""
    im = Image.new("RGBA", (1080, 240), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = c.font(78, 900, 84)
    words = text.split(" ")
    widths = [d.textlength(w, font=f) for w in words]
    space = d.textlength(" ", font=f)
    x = (1080 - (sum(widths) + space * (len(words) - 1))) / 2
    for w, ww in zip(words, widths):
        d.text((x, 70), w, font=f, fill=c.HOT if hot and w.strip(".") == hot else c.CREAM)
        x += ww + space
    im.save(os.path.join(OUT, f"{name}.png"))


def live_tag():
    im = Image.new("RGBA", (360, 110), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 359, 109], radius=55, fill=(255, 74, 26, 255))
    d.ellipse([40, 37, 76, 73], fill=c.CREAM)
    d.text((100, 22), "LIVE", font=c.font(58, 900, 100), fill=c.CREAM)
    im.save(os.path.join(OUT, "live.png"))


def ripple():
    im = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([10, 10, 290, 290], outline=c.CREAM, width=10)
    d.ellipse([120, 120, 180, 180], fill=c.CREAM)
    im.save(os.path.join(OUT, "ripple.png"))


caption("cap-libraries", "Libraries for your slides.")
caption("cap-cuesheets", "Cue sheets for the night.")
caption("cap-click", "Click once.")
caption("cap-live", "It’s live.", hot="live")
live_tag(); ripple()
print("overlays →", OUT)
