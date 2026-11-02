#!/usr/bin/env python3
"""편마다 숏츠 장면 후보 — 하이라이트 박스(hl) 사건을 녹화 파일·녹화 안 시각·창 영역과 함께 뽑는다.
    python3 shorts/beats.py 05        → 표
    python3 shorts/beats.py 05 --json → 기계용
녹화 안 시각 v = (사건 시각 − 구간 시작) + PRE + rec_t0  (assemble2 와 같은 식)
"""
import json, sys, pathlib
V = pathlib.Path(__file__).resolve().parent.parent
def beats(ep):
    E = V / f"ep{ep}"; SL = json.load(open(E / "shotlist2.json")); RG = json.load(open(E / "regions.json"))
    T = json.load(open(E / "times2.json")); PRE, R0 = SL["pre"], SL["rec_t0"]; out = []
    for seg in T:
        sl = SL["segments"].get(seg["id"], {}); rec = E / "rec" / "v2" / f"{seg['id']}.mp4"
        for ev in sl.get("events", []):
            ln = next((l for l in seg["lines"] if l["n"] == ev.get("line", 1)), None)
            if not ln: continue
            t = ln["t"] + ev.get("at", 0.0); v = round(t - seg["start"] + PRE + R0, 2)
            if "hl" in ev and rec.exists():
                r = ev["hl"]; r = RG.get(r, r) if isinstance(r, str) else r
                out.append({"seg": seg["id"], "chapter": seg["chapter"], "rec": str(rec.relative_to(V)), "v": v,
                            "dur": ev.get("dur", 0), "region": r, "lbl": ev.get("lbl", ["", ""]), "line": ln["text"]})
    return out
if __name__ == "__main__":
    b = beats(sys.argv[1])
    if "--json" in sys.argv: print(json.dumps(b, ensure_ascii=False, indent=1)); sys.exit()
    for i, x in enumerate(b):
        print(f"{i:2d} {x['seg']} v{x['v']:6.2f} {str(x['region']):26s} {' / '.join(x['lbl'])[:44]:44s} | {x['line'][:70]}")
