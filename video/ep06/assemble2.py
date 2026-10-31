#!/usr/bin/env python3
"""1편 2판 조립 — script.json(대본) + shotlist2.json(연출) + audio/vo-heart/lines.json(음성 길이) →
    times2.json(줄별 시각) · take2/sN.json(녹화 지시서) · timeline2.js(AE 타임라인, build_v2.jsx 가 읽는다)

    python3 ep01/assemble2.py times | takes | timeline
"""
import json, os, pathlib, subprocess, sys, math
HERE = pathlib.Path(__file__).resolve().parent
S = json.load(open(HERE / "script.json"))
SL = json.load(open(HERE / "shotlist2.json"))
RG = json.load(open(HERE / "regions.json"))
VO = HERE / "audio" / os.environ.get("VO_DIR", "vo-heart")
TITLE, LEAD, GAP, PRE, REC_T0 = SL["title_sec"], SL["lead"], SL["gap"], SL["pre"], SL["rec_t0"]
REST = (0.859375, 270.0, 150.0)                 # 창 px → 화면 px 배율, 창 (0,0) 의 화면 자리
STAGE = (0.859375, 270.0, 152.0)                # 무대 카드(3840×2160 → 3300×1856)
SPLIT = (0.52, 110.0, 574.0)                   # 3편: 조작 창(왼쪽)과 프로젝터(오른쪽)를 나란히 — 창 카드 자리
PROJ = (0.43, 2090.0, 656.0)                    # 프로젝터 카드(LG 녹화 3840×2160 → 1651×929)
M = 150                                         # 확대해도 가장자리 바탕은 이보다 넓게 비지 않는다


def region(name):
    return RG[name] if isinstance(name, str) else name


def voice():
    return json.load(open(VO / "lines.json"))


def times():
    vl = voice(); out = []; t = TITLE
    for g in S["segments"]:
        seg = {"id": g["id"], "chapter": g["chapter"], "start": round(t, 3), "lines": []}
        cur = t + LEAD
        for j, l in enumerate(g["lines"]):
            key = f"{g['id']}-l{j + 1:02d}"; dur = vl[key]["seconds"]
            seg["lines"].append({"key": key, "n": j + 1, "t": round(cur, 3), "dur": dur, "text": l["text"]})
            cur += dur + GAP + l.get("pause", 0)
        end = cur + 0.9 if g["id"] != "s9" else t + 15.0
        seg["end"] = round(end, 3); out.append(seg); t = end
    return out


def ev_time(seg, ev):
    ln = next(l for l in seg["lines"] if l["n"] == ev.get("line", 1))
    return ln["t"] + ev.get("at", 0.0)


def center_lg(name):
    x, y, w, h = region(name); return [round(x + w / 2), round(y + h / 2 + 60)]      # 창 px → LG 화면 캡처 px


def conv_mouse(m):
    op, *rest = m; xy = []
    for r in rest:
        if isinstance(r, str): xy += center_lg(r)
        else: xy.append(r)
    return [op, *xy]


def takes():
    (HERE / "take2").mkdir(exist_ok=True)
    for seg in times():
        if seg["id"] == "s9" or SL["segments"].get(seg["id"], {}).get("gfx"): continue
        sl = SL["segments"][seg["id"]]; acts = []
        for ev in sl.get("events", []):
            t = round(ev_time(seg, ev) - seg["start"] + PRE, 2)
            if "mouse" in ev: acts.append({"t": t, "mouse": conv_mouse(ev["mouse"])})
            if "mcp" in ev: acts.append({"t": t, "mcp": ev["mcp"]})
            if "key" in ev: acts.append({"t": t, "key": ev["key"]})
            if "type" in ev: acts.append({"t": t, "type": ev["type"]})
            if "finder" in ev: acts.append({"t": t, "finder": 1})
            if "fclear" in ev: acts.append({"t": t, "fclear": 1})
            if "optkey" in ev: acts.append({"t": t, "optkey": ev["optkey"]})
            if "clip" in ev: acts.append({"t": t, "clip": ev["clip"]})
        setup = [{"front": 1}] + [({"mouse": conv_mouse(a["mouse"])} if "mouse" in a else a) for a in sl.get("setup", [])]     # 3편: 창을 먼저 맨 앞으로
        take = {"name": seg["id"], "sec": round(seg["end"] - seg["start"] + PRE + 1.5, 1), "setup": setup, "actions": acts}
        json.dump(take, open(HERE / "take2" / f"{seg['id']}.json", "w"), indent=1, ensure_ascii=False)
        print(seg["id"], take["sec"], "s,", len(acts), "actions")
    if "stage_until" not in SL["segments"]["s1"]: return
    # 무대 녹화 — 첫 구간 7번째 줄에서 글만 두 번 바뀐다
    s1 = times()[0]; l7 = next(l for l in s1["lines"] if l["n"] == 7)
    until = ev_time(s1, SL["segments"]["s1"]["stage_until"])
    st = {"name": "stage", "sec": round(until - s1["start"] + PRE + 2.0, 1),
          "actions": [{"t": round(l7["t"] - s1["start"] + PRE + 0.3, 2), "mcp": [{"op": "usePt", "name": "Welcome words"}, {"op": "present", "n": 2}]},
                      {"t": round(l7["t"] - s1["start"] + PRE + 1.9, 2), "mcp": [{"op": "usePt", "name": "Welcome words"}, {"op": "present", "n": 3}]}]}
    json.dump(st, open(HERE / "take2" / "stage.json", "w"), indent=1); print("stage", st["sec"], "s")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "times":
        for seg in times():
            print(f"{seg['id']} {seg['start']:7.2f}–{seg['end']:7.2f} ({seg['end'] - seg['start']:5.1f}s) {seg['chapter']}")
        print("total", times()[-1]["end"])
    elif cmd == "takes": takes()


# ───────────────────────── 타임라인 ─────────────────────────
MOVE = 0.6


def clamp_xy(s, X0, Y0):
    """확대해도 카드 가장자리 바깥(바탕)이 M px 를 넘게 보이지 않게."""
    if s <= REST[0] + 1e-6: return REST[1], REST[2]
    X0 = min(X0, M); X0 = max(X0, 3840 - M - 3840 * s)
    Y0 = min(Y0, M); Y0 = max(Y0, 2160 - M - 2100 * s)
    return X0, Y0


def zoom_state(ev):
    if ev.get("split"): return SPLIT
    x, y, w, h = region(ev["zoom"]); s = ev["scale"]
    cx, cy = ev.get("center", [1920, 1080])
    X0, Y0 = clamp_xy(s, cx - (x + w / 2) * s, cy - (y + h / 2) * s)
    return (s, round(X0, 1), round(Y0, 1))


def holds_for(segs):
    """[(t0, t1, (s, X0, Y0))] — 확대가 머무는 동안. 구간이 끝나기 전에 쉬는 자리로 돌아간다."""
    H = []
    for seg in segs:
        evs = sorted([(round(ev_time(seg, e), 3), e) for e in SL["segments"].get(seg["id"], {}).get("events", []) if "zoom" in e or e.get("split") or e.get("rest")], key=lambda p: p[0])
        for i, (t, e) in enumerate(evs):
            if "zoom" not in e and not e.get("split"): continue
            nxt = evs[i + 1][0] if i + 1 < len(evs) else seg["end"]
            H.append((t, round(nxt - MOVE, 3), zoom_state(e)))
    return H


def card_keys(H):
    R = REST; ks = [[0.0, *R]]
    for i, (t0, t1, st) in enumerate(H):
        prev = ks[-1]
        if t0 - MOVE > prev[0] + 1e-3: ks.append([round(t0 - MOVE, 3), *prev[1:]])
        ks.append([t0, *st]); ks.append([t1, *st])
        nxt = H[i + 1][0] if i + 1 < len(H) else None
        if nxt is None or nxt - MOVE > t1 + MOVE + 1e-3: ks.append([round(t1 + MOVE, 3), *R])
    out = []
    for k in ks:
        if out and k[0] <= out[-1][0] + 1e-6: out[-1] = k
        else: out.append(k)
    return out


def state_at(H, t):
    for t0, t1, st in H:
        if t0 - 1e-3 <= t <= t1 + 1e-3: return st
    return REST


def png_size(p):
    import struct
    b = open(p, "rb").read(24); return struct.unpack(">II", b[16:24])


def bg_motion(total):
    """움직이는 배경(4편부터) — 빛 번짐 셋이 편마다 다른 자리에서 천천히 떠다닌다. 연출표 "bg" 로 정하고,
    없으면 4편부터는 편 번호로 자리를 정한다(3편까지는 None = 예전 한 장짜리 bg.png)."""
    ep = int(HERE.name[2:]); cfg = SL.get("bg")
    if cfg is None and ep < 4: return None
    if cfg is None:
        k = ep * 1.7
        cfg = {"o": [round(420 * math.sin(k)), round(300 * math.cos(k * 1.3))], "p": [round(-380 * math.cos(k * 0.9)), round(260 * math.sin(k * 1.1))],
               "g": [round(500 * math.sin(k * 0.7 + 1)), round(-220 * math.cos(k))], "drift": 170, "period": 26}
    pd = HERE / "parts2"
    if not (pd / "bg-o.png").exists():
        subprocess.run(["node", str(HERE.parent / "bg_parts.mjs"), HERE.name], check=True, cwd=HERE.parent)
    glows = []
    for i, n in enumerate(("o", "p", "g")):
        dx, dy = cfg.get(n, [0, 0]); D = cfg.get("drift", 170); T = cfg.get("period", 26) * (1 + 0.23 * i); ph = i * 2.1
        keys = [[round(t, 2), [1920 + dx + D * math.sin(ph + 2 * math.pi * t / T), 1080 + dy + 0.6 * D * math.cos(ph * 1.3 + 2 * math.pi * t / (T * 1.4))]]
                for t in [x * 4.0 for x in range(int(total / 4) + 2)]]
        glows.append({"file": str(pd / f"bg-{n}.png"), "keys": keys})
    return {"grid": str(pd / "bg-grid.png"), "glows": glows}



# ── 실제 동작 시각에 맞추기 ── 녹화 때 적어 둔 마우스·키 기록(rec/v2/sN.mouse.json)으로, 계획보다 늦어진 만큼 테·이름표를 민다.
#   (4편: 글자 입력이 느려 뒤 동작이 2–3 초 밀렸는데 테는 계획 시각에 떴다 사라져, 닫힌 창 자리에 빈 테가 남았다)
NOMINAL = {"click": 0.9, "rclick": 0.9, "dbl": 0.9, "drag": 0.8, "cmdclick": 0.8, "slowdrag": 0.7, "hold": 0.7}
def lags_for(seg):
    ml = HERE / "rec" / "v2" / f"{seg['id']}.mouse.json"; tk = HERE / "take2" / f"{seg['id']}.json"
    if not (ml.exists() and tk.exists()): return []
    log = json.load(open(ml)); i0 = next((i for i, e in enumerate(log) if e["k"] == "mark:rec"), None)
    if i0 is None: return []
    log = [e for e in log[i0 + 1:] if e["k"] in ("down", "rclick", "dbl", "type") or e["k"].startswith("key:")]
    out, j = [], 0
    for a in sorted(json.load(open(tk))["actions"], key=lambda a: a["t"]):
        if "mouse" in a:
            op = a["mouse"][0]
            if op not in NOMINAL: continue
            want, nom = ("down" if op in ("click", "drag", "cmdclick", "slowdrag", "hold") else op), NOMINAL[op]
        elif "key" in a: want, nom = "key:%d" % a["key"][0], 0.05
        elif "type" in a: want, nom = "type", 0.07 * len(a["type"])
        else: continue
        k = next((k for k in range(j, len(log)) if log[k]["k"] == want), None)
        if k is None: continue
        j = k + 1; out.append((a["t"], max(0.0, log[k]["t"] - (a["t"] + nom))))
    return out       # [(계획 시각(녹화 안), 늦어진 초)]

def shift(seg, t):
    """타임라인 시각 t(계획) → 실제로 화면에 일어난 시각. 그 앞의 마지막 동작이 늦어진 만큼 민다."""
    L = SHIFTS.setdefault(seg["id"], lags_for(seg)); rt = t - seg["start"] + PRE; d = 0.0
    for pt, lag in L:
        if pt <= rt + 1e-3: d = lag
    return round(t + d, 3)
SHIFTS = {}

def timeline():
    segs = times(); H = holds_for(segs); total = segs[-1]["end"]
    parts, caps, lbls, hls, tags, clicks, voice_ = [], [], [], [], [], [], []
    # 1) 조각 목록 — 이름표 · 자막 · 태그 · 진행
    chapters = [s for s in segs if s["id"] != "s9"]
    for i, seg in enumerate(chapters):
        parts.append({"kind": "tag", "file": f"tag-{seg['id']}.png", "args": [f"{i + 1:02d}", seg["chapter"]]})
        parts.append({"kind": "prog", "file": f"prog-{seg['id']}.png", "args": [i, len(chapters)]})
    pending = []
    for seg in segs:
        for e in SL["segments"].get(seg["id"], {}).get("events", []):
            t = round(ev_time(seg, e), 3)
            ln = next(l for l in seg["lines"] if l["n"] == e.get("line", 1))
            if "lbl" in e:
                f = f"lbl-{len(parts):03d}.png"; parts.append({"kind": "lbl", "file": f, "args": [e["lbl"][0], e["lbl"][1], e.get("lblColor", "")]}); pending.append(("lbl", seg, e, t, ln, f))
            if "hl" in e: pending.append(("hl", seg, e, t, ln, None))
            if "cap" in e:
                f = f"cap-{len(parts):03d}.png"; parts.append({"kind": "cap", "file": f, "args": [e["cap"], e.get("keys", ""), e.get("color", "")]}); pending.append(("cap", seg, e, t, ln, f))
    subs = []
    for seg in segs:
        for l in seg["lines"]:
            f = f"sub-{l['key']}.png"; parts.append({"kind": "sub", "file": f, "args": [l["text"]]}); subs.append({"t0": round(l["t"] - 0.05, 3), "t1": round(l["t"] + l["dur"] + 0.3, 3), "file": f})
    for i in range(len(subs) - 1):
        if subs[i]["t1"] > subs[i + 1]["t0"] - 0.04: subs[i]["t1"] = round(subs[i + 1]["t0"] - 0.04, 3)
    pd = HERE / "parts2"; pd.mkdir(exist_ok=True)
    json.dump(parts, open(pd / "list.json", "w"), ensure_ascii=False, indent=1)
    subprocess.run(["node", str(HERE.parent / "render_parts.mjs"), str(HERE / "parts.html"), str(pd / "list.json"), str(pd)], check=True)
    sizes = json.load(open(pd / "sizes.json"))
    # 2) 배치
    for kind, seg, e, t, ln, f in pending:
        dur = e["dur"] if e.get("exact") else max(e.get("dur", 0), ln["dur"] + 0.35); t1 = round(t + dur, 3)     # exact: 앱 안내처럼 정해진 동안만
        if kind in ("hl", "lbl") and not e.get("nosync"):
            t = shift(seg, t); t1 = shift(seg, t1)
            if "end" in e:          # 메뉴·창을 닫는 동작의 (실제) 시각에 끝낸다 — end = {"line", "at"} (그 동작의 계획 시각) + "endpad"
                t1 = round(shift(seg, ev_time(seg, e["end"])) + e.get("endpad", 0.9), 3)
        space = e.get("space", "card")
        if kind == "hl" or kind == "lbl":
            x, y, w, h = region(e["hl"]) if "hl" in e else (0, 0, 0, 0)
            s, X0, Y0 = STAGE if space == "stage" else PROJ if space == "proj" else state_at(H, t)
            R = (X0 + x * s, Y0 + y * s, w * s, h * s)
        if kind == "hl":
            hls.append({"t0": t, "t1": t1, "parent": space, "rect": [x, y, w, h], "color": e.get("color", "indigo"), "dim": bool(e.get("dim")), "s": s, "fill": e.get("fill", 0)})
        elif kind == "lbl":
            lw, lh = sizes[f]; side = e.get("lblSide", "right"); P = 70
            pad = 8 * 1.0
            cands = {"right": (R[0] + R[2] + P, R[1] + R[3] / 2 - lh / 2), "left": (R[0] - P - lw, R[1] + R[3] / 2 - lh / 2),
                     "below": (R[0] + R[2] / 2 - lw / 2, R[1] + R[3] + P), "above": (R[0] + R[2] / 2 - lw / 2, R[1] - P - lh),
                     "inside": (R[0] + 60, R[1] + 60)}
            order = [side] + [k for k in ("right", "below", "left", "above") if k != side]
            def fits(p): return 40 <= p[0] and p[0] + lw <= 3800 and 40 <= p[1] and p[1] + lh <= 2120
            pick = next((k for k in order if fits(cands[k])), side); lx, ly = cands[pick]
            lx = min(max(lx, 40), 3800 - lw); ly = min(max(ly, 40), 2120 - lh)
            if pick == "right": wire = [R[0] + R[2] + 10, min(max(ly + lh / 2, R[1]), R[1] + R[3]), lx + 24, None]
            elif pick == "left": wire = [lx + lw - 24, min(max(ly + lh / 2, R[1]), R[1] + R[3]), R[0] - 10, None]
            elif pick == "below": wire = [min(max(lx + lw / 2, R[0]), R[0] + R[2]), R[1] + R[3] + 10, None, ly + 24]
            elif pick == "above": wire = [min(max(lx + lw / 2, R[0]), R[0] + R[2]), ly + lh - 24, None, R[1] - 10]
            else: wire = None
            lbls.append({"t0": round(t + 0.12, 3), "t1": t1, "file": str(pd / f), "x": round(lx, 1), "y": round(ly, 1), "w": lw, "h": lh, "side": pick, "wire": wire})
        elif kind == "cap":
            cw, ch = sizes[f]
            caps.append({"t0": t, "t1": round(t + e.get("capdur", dur), 3), "file": str(pd / f), "x": 1920, "y": round(2160 - 44 - ch / 2, 1)})
    capspans = [(c["t0"], c["t1"]) for c in caps]
    subs_out = []
    for sb in subs:
        if any(a < sb["t1"] and sb["t0"] < b for a, b in capspans): continue     # 강조 자막이 떠 있는 동안은 대사 자막을 빼다(같은 말이다)
        w, h = sizes[sb["file"]]; subs_out.append({"t0": sb["t0"], "t1": sb["t1"], "file": str(pd / sb["file"]), "x": 1920, "y": round(2160 - 40 - h / 2, 1)})
    for i, seg in enumerate(chapters):
        tw, th = sizes[f"tag-{seg['id']}.png"]; pw, ph = sizes[f"prog-{seg['id']}.png"]
        tags.append({"t0": seg["start"], "t1": seg["end"], "file": str(pd / f"tag-{seg['id']}.png"), "x": 270 - 24, "y": 40 - 24, "w": tw, "h": th})
        tags.append({"t0": seg["start"], "t1": seg["end"], "file": str(pd / f"prog-{seg['id']}.png"), "x": 3570 - pw + 24, "y": 70 - 24, "w": pw, "h": ph, "prog": True})
    # 3) 녹화 · 클릭 · 목소리
    rec = HERE / "rec" / "v2"; clips = []
    for seg in chapters:
        if SL["segments"].get(seg["id"], {}).get("gfx"):
            for l in seg["lines"]: voice_.append({"t": l["t"], "file": str(VO / f"e06-{l['key']}.wav"), "dur": l["dur"]})
            continue
        f = rec / f"{seg['id']}.mp4"
        clips.append({"file": str(f), "t0": round(seg["start"] - 0.3, 3), "t1": seg["end"], "in": round(REC_T0 + PRE - 0.3, 3)})
        ml = rec / f"{seg['id']}.mouse.json"
        if ml.exists():
            for e in json.load(open(ml)):
                if e["k"] == "down":
                    tc = round(seg["start"] + e["t"] - PRE, 3); clicks.append({"t": tc, "x": e["x"], "y": e["y"] - 60, "s": state_at(H, tc)[0]})
        for l in seg["lines"]: voice_.append({"t": l["t"], "file": str(VO / f"e06-{l['key']}.wav"), "dur": l["dur"]})
    for l in segs[-1]["lines"]: voice_.append({"t": l["t"], "file": str(VO / f"e06-{l['key']}.wav"), "dur": l["dur"]})
    # 무대 녹화(1편)는 선택 · 그래픽 장면(gfx) · 그림 넣기(img)
    s1 = segs[0]; st1 = SL["segments"]["s1"]
    until = round(ev_time(s1, st1["stage_until"]), 3) if "stage_until" in st1 else None
    gfx, imgs = [], []
    for seg in chapters:
        sc = SL["segments"].get(seg["id"], {}).get("gfx")
        if sc:
            beats = [round(l["t"] - seg["start"], 3) for l in seg["lines"]]; dur = round(seg["end"] - seg["start"] + 0.6, 2)
            d = HERE / "frames" / f"gfx-{seg['id']}"
            subprocess.run(["node", str(HERE.parent / "render_anim.mjs"), f"{HERE / 'gfx.html'}?scene={sc}&dur={dur}&beats={json.dumps(beats)}", "#g", "30", str(d), "1"], check=True)
            gfx.append({"dir": str(d), "t0": seg["start"], "t1": round(seg["start"] + dur, 3)})
        for e in SL["segments"].get(seg["id"], {}).get("events", []):
            if "img" in e:
                t0 = round(ev_time(seg, e), 3); t1 = round(ev_time(seg, e["until"]), 3)
                imgs.append({"file": str(HERE / e["img"]), "t0": t0, "t1": t1, "chip": str(HERE / e["chip"]) if e.get("chip") else ""})
    # 3편: 프로젝터 — 나란히 보기(split) 동안만. 실제 송출을 찍은 proj/<이름>.png 를 proj 이벤트 시각에 바꾼다(fade 초 동안 겹쳐 들어온다)
    shots = []
    for seg in segs:
        for e in SL["segments"].get(seg["id"], {}).get("events", []):
            if "proj" in e: shots.append([round(ev_time(seg, e), 3), e["proj"], e.get("fade", 0.3)])
    shots.sort()
    sh = [{"file": str(HERE / "proj" / f"{img}.png"), "t0": t, "t1": round((shots[i + 1][0] + shots[i + 1][2]) if i + 1 < len(shots) else total, 3), "fade": f}
          for i, (t, img, f) in enumerate(shots)]
    spans = [[t0, t1] for t0, t1, st in H if st == SPLIT]
    merged = []
    for a_, b_ in spans:
        if merged and a_ - MOVE <= merged[-1][1] + MOVE + 1e-3: merged[-1][1] = b_
        else: merged.append([a_, b_])
    proj = {"shots": sh, "spans": merged, "state": PROJ, "split": SPLIT, "move": MOVE,
            "chipProj": str(HERE / "chip-proj.png"), "chipCtl": str(HERE / "chip-ctl.png")} if sh else None
    first_win = next(s for s in chapters if not SL["segments"].get(s["id"], {}).get("gfx"))
    TL = {"name": "LayerCue-ep06", "duration": round(total, 3), "fps": 30,
          "title": {"dir": str(HERE / "frames" / "title2"), "t1": TITLE + 0.5},
          "end": {"dir": str(HERE / "frames" / "end2"), "t0": round(segs[-1]["start"] - 0.5, 3)},
          "bg": str(HERE / "parts2" / "bg.png"), "bgm": bg_motion(total),
          "stage": ({"file": str(rec / "stage.mp4"), "t0": round(s1["start"] - 0.5, 3), "t1": round(until + 0.5, 3), "in": round(REC_T0 + PRE - 0.5, 3), "xf": until} if until else None),
          "gfx": gfx, "imgs": imgs, "proj": proj,
          "card": {"t0": round((until - 0.1) if until else first_win["start"] - 0.3, 3), "t1": round(segs[-1]["start"] + 0.4, 3), "keys": card_keys(H)},
          "clips": clips, "hls": hls, "lbls": lbls, "caps": caps, "subs": subs_out, "tags": tags, "clicks": clicks, "voice": voice_,
          "music": str(HERE / "audio" / "music-ep06.wav"), "sfx": [], "checks": []}
    for seg in segs:
        for l in seg["lines"][:: max(1, len(seg["lines"]) // 3)]: TL["checks"].append(round(l["t"] + min(1.0, l["dur"] / 2), 2))
    (HERE / "timeline2.js").write_text("var TL = " + json.dumps(TL, ensure_ascii=False, indent=1) + ";\n")
    json.dump(segs, open(HERE / "times2.json", "w"), indent=1, ensure_ascii=False)
    print(f"timeline2: {total:.1f}s; clips {len(clips)} hls {len(hls)} lbls {len(lbls)} caps {len(caps)} tags {len(tags)} clicks {len(clicks)} voice {len(voice_)} zoomkeys {len(TL['card']['keys'])}")


if __name__ == "__main__" and sys.argv[1] == "timeline":
    timeline()
