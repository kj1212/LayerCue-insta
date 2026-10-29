#!/usr/bin/env python3
"""촬영용 LayerCue 에 기본 소개 쇼츠의 데모 장면을 짓는다 — 층마다 프레젠테이션 하나.

    python3 build_demo.py

  Stage background  배경 그림          → background 층에 고정
  Welcome           큰 글 두 장        → foreground
  Event logo        오른쪽 위 로고      → overlay1
  Lower third       왼쪽 아래 이름 띠   → overlay2
모두 라이브러리 「Demo」, 큐시트 「Opening Night」 에 담는다. 이름·행사는 지어낸 것이다.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lc

HERE = pathlib.Path(__file__).parent


def text_of(r):
    return "\n".join(c.get("text", "") for c in r.get("result", {}).get("content", []) if c.get("type") == "text")


def pic(path):
    out = text_of(lc.call("add_picture", {"path": str(path)}))
    print("add_picture:", out[:200])
    try:
        return json.loads(out)["name"]
    except Exception:
        import re
        m = re.search(r'"?name"?\s*[:=]\s*"([^"]+)"', out)
        return m.group(1) if m else pathlib.Path(path).name


def slides(name, html, layer):
    r = lc.call("set_slides_html", {"html": html, "create": name, "library": "Demo",
                                    "cue_sheet": "Opening Night", "preview": False})
    print(name, "→", text_of(r)[:300].replace("\n", " "))
    lc.call("run_commands", {"commands": [{"op": "usePt", "name": name}, {"op": "forcedLayer", "layer": layer}]})


bg = pic(HERE / "demo/stage-bg.jpg")
logo = pic(HERE / "demo/event-logo.png")

slides("Stage background",
       f'<section style="background:#0a0c1a"><img data-role="backdrop" src="{bg}" style="left:0;top:0;width:100%;height:100%;object-fit:cover"></section>',
       "background")

TXT = ("color:#F2EEE4;font-family:'Archivo';font-weight:900;font-size:12cqh;letter-spacing:-0.03em;"
       "line-height:1.0;text-align:center;align-content:center")
slides("Welcome",
       f'<section style="background:transparent"><div style="left:10%;top:28%;width:80%;height:44%;{TXT}">Welcome to<br>Opening Night</div></section>'
       f'<section style="background:transparent"><div style="left:10%;top:28%;width:80%;height:44%;{TXT}">Session two<br>The Keynote</div></section>',
       "foreground")

slides("Event logo",
       f'<section style="background:transparent"><img src="{logo}" style="left:66%;top:5%;width:28%;height:9.8%"></section>',
       "overlay1")

slides("Lower third",
       '<section style="background:transparent">'
       '<div data-shape="rect" style="left:6%;top:76%;width:30%;height:13%;background-color:rgba(11,11,13,0.82)"></div>'
       '<div data-shape="rect" style="left:6%;top:76%;width:0.6%;height:13%;background-color:#FF4A1A"></div>'
       "<div style=\"left:8%;top:77.5%;width:27%;height:6%;color:#F2EEE4;font-family:'Archivo';font-weight:800;font-size:4.6cqh\">Jane Park</div>"
       "<div style=\"left:8%;top:83.5%;width:27%;height:4.5%;color:#9C988E;font-family:'Archivo';font-weight:500;font-size:3cqh;letter-spacing:0.08em\">HOST</div>"
       '</section>',
       "overlay2")
print(lc.call("list_cue_sheets") and "ok")
