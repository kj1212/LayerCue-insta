#!/usr/bin/env python3
"""14편 데모 덱 — Dana Okafor 의 키노트(가상). 표 1, 차트 1(안 들어온다), 숨김 1, 윈도우 글꼴(Segoe UI) — 대체 글꼴로 바뀌는 것을 보여 준다.
    <venv with python-pptx>/bin/python ep14/media/make_deck.py  → ep14/media/Keynote-Okafor.pptx
"""
import pathlib
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.text import PP_ALIGN
H = pathlib.Path(__file__).resolve().parent
P = Presentation(); P.slide_width, P.slide_height = Emu(12192000), Emu(6858000)
W, Hh = P.slide_width, P.slide_height
BL = P.slide_layouts[6]
NAVY, AMBER, WHITE, MUTE = RGBColor(0x0B, 0x12, 0x30), RGBColor(0xF5, 0xB0, 0x3A), RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0xAE, 0xB8, 0xD0)
F = "Segoe UI"
def bg(s, pic=False):
    if pic: s.shapes.add_picture(str(H / "deck-bg.jpg"), 0, 0, W, Hh)
    else:
        f = s.background.fill; f.solid(); f.fore_color.rgb = NAVY
def text(s, x, y, w, h, lines, size, color=WHITE, bold=False, align=PP_ALIGN.LEFT):
    tb = s.shapes.add_textbox(Emu(int(W * x)), Emu(int(Hh * y)), Emu(int(W * w)), Emu(int(Hh * h))); tf = tb.text_frame; tf.word_wrap = True
    for i, l in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        r = p.add_run(); r.text = l; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = F
    return tb
# 1 제목
s = P.slides.add_slide(BL); bg(s, pic=True)
text(s, .08, .30, .84, .18, ["Designing for the Room"], 54, bold=True)
text(s, .08, .50, .84, .10, ["Dana Okafor · Riverside Tech Summit 2026"], 24, AMBER)
# 2 글머리
s = P.slides.add_slide(BL); bg(s)
text(s, .08, .10, .84, .12, ["What a screen in a hall needs"], 40, bold=True)
text(s, .08, .28, .84, .55, ["• Fewer words, larger type", "• Contrast that survives the house lights", "• One idea per slide, held long enough to read"], 28)
# 3 표
s = P.slides.add_slide(BL); bg(s)
text(s, .08, .08, .84, .12, ["Type size that reads from the back"], 40, bold=True)
rows = [("Room depth", "Smallest text", "Headline"), ("10 m", "28 pt", "48 pt"), ("20 m", "40 pt", "66 pt"), ("30 m", "54 pt", "88 pt")]
t = s.shapes.add_table(4, 3, Emu(int(W * .08)), Emu(int(Hh * .28)), Emu(int(W * .84)), Emu(int(Hh * .5))).table
for i, r in enumerate(rows):
    for j, v in enumerate(r):
        c = t.cell(i, j); c.text = v; c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0x1D, 0x3A, 0x8F) if i == 0 else RGBColor(0x14, 0x1D, 0x45)
        run = c.text_frame.paragraphs[0].runs[0]; run.font.size = Pt(24); run.font.name = F; run.font.color.rgb = AMBER if i == 0 else WHITE; run.font.bold = i == 0
# 4 차트(안 들어온다)
s = P.slides.add_slide(BL); bg(s)
text(s, .08, .08, .84, .12, ["What the audience told us"], 40, bold=True)
cd = CategoryChartData(); cd.categories = ["Too small", "Too dense", "Too fast", "Just right"]; cd.add_series("Votes", (38, 27, 19, 16))
s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(int(W * .12)), Emu(int(Hh * .26)), Emu(int(W * .76)), Emu(int(Hh * .62)), cd)
# 5 숨김
s = P.slides.add_slide(BL); bg(s)
text(s, .08, .10, .84, .12, ["Backup: Q&A notes"], 40, bold=True)
text(s, .08, .28, .84, .4, ["Only if time allows"], 28, MUTE)
s._element.set("show", "0")
# 6 마무리
s = P.slides.add_slide(BL); bg(s, pic=True)
text(s, .08, .38, .84, .18, ["Thank you"], 60, bold=True, align=PP_ALIGN.CENTER)
text(s, .08, .56, .84, .08, ["dana.okafor@example.com"], 22, MUTE, align=PP_ALIGN.CENTER)
P.save(H / "Keynote-Okafor.pptx"); print("deck", len(P.slides.__iter__.__self__._sldIdLst), "slides")
