#!/usr/bin/env python3
"""1편 데모 자료 「Summit 2026」 라이브러리 — 가상 행사 Riverside Tech Summit 2026 (이름·행사·인물은 지어낸 것).

    LC_SANDBOX=sandbox-ep01 python3 ep01/build_summit.py

  Welcome loop   추상 루프 영상 (pplist 로 미리 넣어 둠)   → Layer for this list = Background
  Welcome words  글 세 장(Welcome / Doors open 9:00 / Keynote) → 기본(foreground)
  Summit logo    왼쪽 위 로고 PNG                            → Layer for this list = Overlay 1
"""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import lc

LIB = "Summit 2026"


def text_of(r):
    return "\n".join(c.get("text", "") for c in r.get("result", {}).get("content", []) if c.get("type") == "text")


def pic(path):
    out = text_of(lc.call("add_picture", {"path": str(path)}))
    print("add_picture:", out[:160].replace("\n", " "))
    try:
        return json.loads(out)["name"]
    except Exception:
        m = re.search(r'"?name"?\s*[:=]\s*"([^"]+)"', out)
        return m.group(1) if m else pathlib.Path(path).name


def slides(name, html, layer=None):
    r = lc.call("set_slides_html", {"html": html, "create": name, "library": LIB, "preview": False})
    print(name, "→", text_of(r)[:240].replace("\n", " "))
    if layer:
        lc.call("run_commands", {"commands": [{"op": "usePt", "name": name}, {"op": "forcedLayer", "layer": layer}]})


BIG = ("color:#F4F1EA;font-family:'Archivo';font-weight:900;letter-spacing:-0.03em;line-height:1;"
       "text-align:center;align-content:center")
SUB = ("color:#5FD3C6;font-family:'Archivo';font-weight:600;letter-spacing:0.28em;line-height:1;"
       "text-align:center;align-content:center")


def page(big, sub, big_size="17cqh"):
    return ('<section style="background:transparent">'
            f'<div style="left:6%;top:38%;width:88%;height:24%;font-size:{big_size};{BIG}">{big}</div>'
            f'<div style="left:6%;top:65%;width:88%;height:8%;font-size:4cqh;{SUB}">{sub}</div>'
            '</section>')


slides("Welcome words",
       page("Welcome", "RIVERSIDE TECH SUMMIT 2026")
       + page("Doors open 9:00", "MAIN HALL · LEVEL 2", "14cqh")
       + page("Keynote", "DANA OKAFOR · 9:30", "15cqh"))

logo = pic(HERE / "summit-logo.png")
slides("Summit logo",
       f'<section style="background:transparent"><img src="{logo}" style="left:4%;top:6%;width:24%;height:10.67%"></section>',
       "overlay1")

st = json.loads(text_of(lc.call("get_state")))
print("libraries:", st["libraries"])
