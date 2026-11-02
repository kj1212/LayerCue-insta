#!/usr/bin/env python3
"""15편 s5: 리허설 때 Claude Desktop 이 실제로 만든 「Our Solar System」(media/solar/solar.html, 손대지 않음)을
   그대로 다시 넣는다 — 「짠」 하고 나오는 장면. Claude 가 고른 라이브러리 「Science Night」 에(미리 만들어 둔다).
   python3 solar_replay.py [이름] [라이브러리]"""
import sys, re, pathlib
H = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(H.parent)); import lc
html = (H / "media/solar/solar.html").read_text()
html = re.sub(r'\s*data-(id|rev)="[^"]*"', "", html)           # 원래 덱의 꼬리표만 뗀다 — 새 프레젠테이션으로 들어가게
name = sys.argv[1] if len(sys.argv) > 1 else "Our Solar System"
lib = sys.argv[2] if len(sys.argv) > 2 else "Science Night"
r = lc.call("set_slides_html", {"create": name, "library": lib, "html": html, "preview": False})
print("".join(c.get("text", "") for c in r.get("result", {}).get("content", []))[:400], r.get("error", ""))
