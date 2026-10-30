#!/usr/bin/env python3
"""1편 조립 — 대본(script.json) + 연출표(shotlist.json) + 음성 길이(audio/vo/lines.json) 로
녹화 지시서(take/sNN.json) 와 AE 타임라인(timeline.js) 을 만든다.

    python3 ep01/assemble.py times      줄별 시각만 계산해 보여 준다(음성 길이가 있어야 한다)
    python3 ep01/assemble.py takes      ep01/take/sNN.json — record.py 가 읽는다
    python3 ep01/assemble.py timeline   ep01/timeline.js + 자막 PNG(ep01/caps/) — build_ep01.jsx 가 읽는다

연출표(shotlist.json):
  { "lead": 0.6, "gap": 0.45, "pre": 1.0,
    "full": [ {"file": "rec/coldopen-stage.mov", "t0": 0, "t1": 6.2, "in": 1.0, "fadeOut": 0.6}, {"file": "card-title.png", "t0": 5.8, "t1": 10.5, "fadeIn": 0.5, "fadeOut": 0.5} ],
    "segments": { "s01": { "setup": [ {"mcp": [...]}, {"mouse": ["jump", x, y]} ],
                          "events": [ {"line": 1, "at": 0.0, "zoom": "sidebar", "scale": 1.8},     # zoom 은 다음 zoom/rest 까지
                                      {"line": 2, "at": 0.3, "hl": "sidebar.cueSheets", "color": "indigo", "dim": true, "dur": 4},
                                      {"line": 3, "at": 0.0, "cap": "Pick on the left", "keys": "", "color": "", "dur": 3.5},
                                      {"line": 4, "at": 0.2, "mouse": ["click", "sidebar.tourRow"]},          # 영역 이름이면 그 가운데(창 px)
                                      {"line": 5, "at": 0.0, "mcp": [ {"op": "present", "n": 1} ]},
                                      {"line": 6, "at": 0.0, "rest": true} ] } } }
line 은 그 구간 안의 줄 번호(1부터, 빈 줄 제외하지 않음 — script 의 lines 순서). at 은 그 줄의 음성 시작에서 더하는 초.
창 픽셀 영역 → 녹화 지시서의 마우스 좌표는 y+60(LG 화면 캡처), 타임라인의 테·링은 창 px 그대로.
"""
import json, os, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
S = json.load(open(HERE / "script.json"))
SL = json.load(open(HERE / "shotlist.json"))
RG = json.load(open(HERE / "regions.json"))
LEAD, GAP, PRE = SL.get("lead", 0.6), SL.get("gap", 0.45), SL.get("pre", 1.0)
REC_T0 = SL.get("rec_t0", 1.1)     # record.py 의 t=0 이 영상 파일에서 몇 초인지 — calib.py 로 쟀다(2026-10-30: 1.1 s)


def region(name):
    if isinstance(name, list): return name
    return RG[name]


def center(name):
    x, y, w, h = region(name); return (x + w / 2, y + h / 2)


VO_DIR = os.environ.get("VO_DIR", "vo")      # 목소리 폴더(voice.py 와 같은 환경변수)


def voice_len():
    p = HERE / "audio" / VO_DIR / "lines.json"
    return json.load(open(p)) if p.exists() else {}


def times():
    """구간·줄의 실제 시각. 음성 길이가 없으면 낱말수로 어림(2.3 낱말/초)."""
    vl = voice_len(); out = []; t = 0.0
    for g in S["segments"]:
        planned = g["end"] - g["start"]
        seg = {"id": g["id"], "chapter": g["chapter"], "start": t, "lines": []}
        cur = t + LEAD
        for j, l in enumerate(g["lines"]):
            key = f"{g['id']}-l{j + 1:02d}"
            if not l["text"].strip():
                cur += l.get("pause", 0); continue
            dur = vl.get(key, {}).get("seconds") or len(l["text"].split()) / 2.3
            seg["lines"].append({"key": key, "n": j + 1, "t": round(cur, 3), "dur": round(dur, 3), "text": l["text"]})
            cur += dur + GAP + l.get("pause", 0)
        need = cur - t + 1.2      # 마지막 줄 뒤 숨 돌릴 틈 1.2 s(gap 포함)
        # 구간 길이는 실제 말한 만큼 — 계획표의 길이는 상한이 아니라 어림이었다. 엔드 카드만 15 s 고정
        seg["end"] = round(t + need, 3) if g["id"] != S["segments"][-1]["id"] else round(t + planned, 3)
        seg["planned"] = planned; seg["over"] = round(need - planned, 2) if need > planned else 0
        out.append(seg); t = seg["end"]
    return out


def event_time(seg, ev):
    ln = next((l for l in seg["lines"] if l["n"] == ev.get("line", 1)), None)
    base = ln["t"] if ln else seg["start"]
    return base + ev.get("at", 0.0)


def takes():
    (HERE / "take").mkdir(exist_ok=True)
    for seg in times():
        sl = SL["segments"].get(seg["id"], {})
        actions = []
        for ev in sl.get("events", []):
            t = event_time(seg, ev) - seg["start"] + PRE
            if "mouse" in ev:
                op, *rest = ev["mouse"]
                xy = []
                for r in rest:
                    if isinstance(r, str): cx, cy = center(r); xy += [round(cx), round(cy + 60)]
                    else: xy.append(r)
                actions.append({"t": round(t, 2), "mouse": [op, *xy]})
            if "mcp" in ev: actions.append({"t": round(t, 2), "mcp": ev["mcp"]})
            if "key" in ev: actions.append({"t": round(t, 2), "key": ev["key"]})
        setup = []
        for a in sl.get("setup", []):
            if "mouse" in a:
                op, *rest = a["mouse"]; xy = []
                for r in rest:
                    if isinstance(r, str): cx, cy = center(r); xy += [round(cx), round(cy + 60)]
                    else: xy.append(r)
                setup.append({"mouse": [op, *xy]})
            else: setup.append(a)
        take = {"name": seg["id"], "sec": round(seg["end"] - seg["start"] + PRE + 1.0, 1), "setup": setup, "actions": actions}
        json.dump(take, open(HERE / "take" / f"{seg['id']}.json", "w"), indent=1, ensure_ascii=False)
        print(seg["id"], take["sec"], "s,", len(actions), "actions")


def zoom_keys(zooms):
    """[(t0, t1, rect, scale)] → Screen 층의 [t, scale, [x, y]] 키프레임. 쉬는 자리는 (1, [1920, 1050]).
    줌 사이가 MOVE 안이면 바로 다음 줌으로 옮기고, 멀면 쉬는 자리로 돌아와 기다린다."""
    REST = (1.0, [1920, 1050]); MOVE = 0.6; ks = []
    def pos(rect, s):
        cx, cy = rect[0] + rect[2] / 2, rect[1] + 60 + rect[3] / 2
        x, y = 1920 - (cx - 1920) * s, 1080 - (cy - 1080) * s
        # 창 밖(검은 여백)이 화면에 들어오지 않게 — 창은 Screen 좌표 x 0–3840, y 60–2160. 아래는 120 px 여백을 둔다(상태 바 테가 잘리지 않게)
        x = min(max(x, 3840 - 1920 * s), 1920 * s)
        y = min(max(y, 2040 - 1080 * s), 1020 * s)
        return [round(x, 1), round(y, 1)]
    zs = sorted(zooms)
    for i, (t0, t1, rect, sc) in enumerate(zs):
        state = (sc, pos(rect, sc))
        prev = ks[-1] if ks else None
        if prev is None:
            ks.append([round(max(0, t0 - MOVE), 3), *REST])
        elif t0 - prev[0] > MOVE + 0.05:
            ks.append([round(t0 - MOVE, 3), prev[1], prev[2]])          # 이전 상태를 들고 있다가
        ks.append([round(t0, 3), *state]); ks.append([round(t1, 3), *state])
        nxt = zs[i + 1][0] if i + 1 < len(zs) else None
        if nxt is None or nxt - t1 > MOVE + 0.05:
            ks.append([round(t1 + MOVE, 3), *REST])
    out = []
    for k in ks:
        if out and k[0] <= out[-1][0] + 1e-6: out[-1] = k
        else: out.append(k)
    return out


def auto_scale(rect, want=0.8, cap=2.4):
    return round(min(cap, max(1.0, min(want * 3840 / rect[2], want * 2160 / rect[3]))), 3)


def timeline():
    segs = times(); vl = voice_len()
    TL = {"name": "LayerCue-ep01", "duration": 300.0, "fps": 30, "clips": [], "full": [], "zoomKeys": [], "highlights": [],
          "captions": [], "clicks": [], "voice": [], "sfx": [], "music": None, "checks": [], "template": SL.get("template")}
    total = segs[-1]["end"]; TL["duration"] = round(max(300.0, total), 2)
    caps = []; zooms = []
    for seg in segs:
        sl = SL["segments"].get(seg["id"], {})
        rec = HERE / "rec" / "cfr" / f"{seg['id']}.mp4"          # 30 fps 고정 프레임률 판(cfr.sh) — 없으면 원본
        if not rec.exists(): rec = HERE / "rec" / f"{seg['id']}.mov"
        if rec.exists() or not sl.get("noclip"):
            TL["clips"].append({"file": str(rec), "t0": seg["start"], "t1": seg["end"], "in": round(REC_T0 + PRE, 3)})
        for l in seg["lines"]:
            TL["voice"].append({"key": l["key"], "t": l["t"], "file": str(HERE / "audio" / VO_DIR / f"e01-{l['key']}.wav"), "dur": l["dur"]})
        open_zoom = None
        for ev in sl.get("events", []):
            t = round(event_time(seg, ev), 3)
            if "zoom" in ev or ev.get("rest"):
                if open_zoom:
                    t_end = max(open_zoom[0] + 0.1, t - 0.6) if "zoom" in ev else t
                    zooms.append((open_zoom[0], t_end, open_zoom[1], open_zoom[2])); open_zoom = None
                if "zoom" in ev:
                    r = region(ev["zoom"]); open_zoom = (t, r, ev.get("scale") or auto_scale(r, ev.get("want", 0.8)))
            if "hl" in ev:
                r = region(ev["hl"])
                ln = next((l for l in seg["lines"] if l["n"] == ev.get("line", 1)), None)
                dur = max(ev.get("dur", 0), (ln["dur"] + 0.3) if ln else 3.0)
                TL["highlights"].append({"name": ev["hl"] if isinstance(ev["hl"], str) else "rect", "t0": t, "t1": round(t + dur, 3),
                                         "rect": r, "color": ev.get("color", "indigo"), "dim": ev.get("dim", False), "width": ev.get("width", 9), "fill": ev.get("fill", 0),
                                         "space": ev.get("space", "window")})
            if "cap" in ev:
                f = f"cap-{len(caps) + 1:02d}.png"
                caps.append({"file": f, "text": ev["cap"], "keys": ev.get("keys", ""), "color": ev.get("capcolor", "")})
                TL["captions"].append({"t0": t, "t1": round(t + ev.get("capdur", ev.get("dur", 3.5)), 3), "file": str(HERE / "caps" / f), "y": ev.get("y", 1930), "x": ev.get("x", 1920)})
        if open_zoom: zooms.append((open_zoom[0], seg["end"], open_zoom[1], open_zoom[2]))
        # 클릭 링 — 녹화 때 적은 마우스 자취에서
        ml = HERE / "rec" / f"{seg['id']}.mouse.json"
        if ml.exists():
            for e in json.load(open(ml)):
                if e["k"] == "down": TL["clicks"].append({"t": round(seg["start"] + e["t"] - PRE, 3), "x": e["x"], "y": e["y"] - 60})
        TL["checks"].append(round(seg["start"] + 2.0, 1))
    TL["zoomKeys"] = zoom_keys(zooms)
    TL["checks"] = sorted(set(TL["checks"] + [float(x) for x in SL.get("checks", [])]))
    bysid = {g["id"]: g for g in segs}
    def at(seg_id, spec):
        g = bysid[seg_id]; return round(event_time(g, {"line": spec["line"], "at": spec.get("at", 0.0)}), 3)
    for f in SL.get("full", []):
        src = HERE / f["file"]
        cfr = HERE / "rec" / "cfr" / (pathlib.Path(f["file"]).stem + ".mp4")
        if src.suffix == ".mov" and cfr.exists(): src = cfr
        ff = {"file": str(src), "in": f.get("in", 0), "fadeIn": f.get("fadeIn", 0), "fadeOut": f.get("fadeOut", 0)}
        ff["t0"] = at(f["seg"], f["from"]) if "from" in f else f["t0"]
        ff["t1"] = at(f["seg"], f["until"]) if "until" in f else f["t1"]
        TL["full"].append(ff)
    if SL.get("music"):
        TL["music"] = {"file": str(HERE / SL["music"]["file"]), "base": SL["music"].get("base", -20), "duck": SL["music"].get("duck", -26)}
    TL["sfx"] = [{"file": str(HERE.parent / x["file"]), "t": x["t"], "level": x.get("level", 0)} for x in SL.get("sfx", [])]
    (HERE / "caps").mkdir(exist_ok=True)
    json.dump(caps, open(HERE / "caps" / "list.json", "w"), ensure_ascii=False, indent=1)
    if caps:
        subprocess.run(["node", str(HERE.parent / "render_caps.mjs"), str(HERE / "captions.html"), str(HERE / "caps" / "list.json"), str(HERE / "caps")], check=True)
    (HERE / "timeline.js").write_text("var TL = " + json.dumps(TL, ensure_ascii=False, indent=1) + ";\n")
    json.dump(segs, open(HERE / "times.json", "w"), indent=1, ensure_ascii=False)
    print("timeline: total", total, "s;", len(TL["clips"]), "clips,", len(TL["voice"]), "voice,", len(TL["highlights"]), "hl,", len(TL["captions"]), "caps,", len(TL["clicks"]), "clicks,", len(zooms), "zooms")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "times":
        for seg in times():
            print(f"{seg['id']} {seg['start']:6.1f}–{seg['end']:6.1f}  planned {seg['planned']:3.0f}s  over {seg['over']}  {seg['chapter']}")
            for l in seg["lines"]: print(f"   {l['t']:6.1f} {l['dur']:4.1f}s  {l['text']}")
    elif cmd == "takes": takes()
    elif cmd == "timeline": timeline()
