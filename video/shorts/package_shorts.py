#!/usr/bin/env python3
"""숏츠 묶음 — 표지 · 자막(en/ko/ja) · 업로드 글 → shorts/<id>/out/ 과 OneDrive shorts/<id>/   python3 shorts/package_shorts.py [id …]"""
import sys, json, pathlib, subprocess, shutil
H = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(H)); import i18n
OD = pathlib.Path.home() / "OneDrive" / "LayerCue from Zero" / "shorts"
YT = {1: "55dioOOzick", 2: "TN-k9CZu6HM", 3: "7n3y090k32o", 4: "tMJCwayL_Ac", 5: "spZ9ot7IEtY", 6: "PxVnaJuqgvg", 7: "ir3SPZcCopI",
      8: "VYMQO1RbnFc", 9: "o2KG20shVno", 10: "SYOk30VlKHk", 11: "u0sWDknjsJQ"}
PL = "https://www.youtube.com/playlist?list=PLbN0h6kQZtT8"
EPT = json.load(open(H.parent / "ep14" / "out" / "meta.json"))   # 형식 참고용
def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round((x-int(x))*1000)):03d}"
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
def one(d):
    sp = json.load(open(d / "spec.json")); sid = sp["id"]; ep = int(sp["ep"]); out = d / "out"
    if not (out / f"{sid}.mp4").exists(): print("no video", sid); return
    cfg = json.loads((d / "cfg.js").read_text()[len("var CFG = "):].rstrip().rstrip(";"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(cfg["beats"][1]["t"] + 1.6), "-i", str(out / f"{sid}.mp4"), "-frames:v", "1", "-q:v", "2", str(out / f"{sid}-cover.jpg")], check=True)
    T = [(sp["vo_at"][i], sp["vo_at"][i] + dur(d / "audio" / f"{i:02d}.wav")) for i in range(7)]
    for lang, L in (("en", sp["lines"]), ("ko", i18n.KO[sp["ep"]]), ("ja", i18n.JA[sp["ep"]])):
        (out / "subtitles" / f"{sid}-{lang}.srt").write_text("\n".join(f"{i+1}\n{ts(a)} --> {ts(b + .2)}\n{t}\n" for i, ((a, b), t) in enumerate(zip(T, L))))
    meta = json.load(open(H.parent / f"ep{sp['ep']}" / "out" / "meta.json")) if (H.parent / f"ep{sp['ep']}" / "out" / "meta.json").exists() else {}
    eptitle = meta.get("title", "").split(" | ")[0] or f"Episode {ep}"
    eplink = f"https://www.youtube.com/watch?v={YT[ep]}" if ep in YT else PL
    words = " ".join(b["w"].capitalize() + "." for b in sp["beats"])
    ko_t = meta.get("title_ko", "").split(" | ")[0]; ja_t = meta.get("title_ja", "").split(" | ")[0]
    txt = f"""YOUTUBE SHORT — upload the vertical video; YouTube makes it a Short (under 3 min, 9:16).

TITLE
{sp['title']}: {words} #Shorts

DESCRIPTION
{sp['hook_vo']} {' '.join(b['vo'] for b in sp['beats'])}

Free while it's in beta, on Mac and Windows: https://layercue.com
Full tutorial — LayerCue from Zero, Episode {ep} ({eptitle}): {eplink}

The narration and music were made with AI running on a Mac. The event in the demo is made up.

#LayerCue #LiveProduction #EventProduction

TAGS
LayerCue, LayerCue tutorial, presentation software, live production, event production, projection software, Mac, Windows

PLAYLIST
LayerCue Shorts (optional)

SUBTITLES
subtitles/{sid}-en.srt, -ko.srt, -ja.srt as 'With timing'.

INSTAGRAM CAPTION
{sp['hook_vo']} {words}
Free on Mac & Windows while it's in beta.
🎬 Full episode → link in bio (LayerCue from Zero, Ep {ep})

Narration and music made with AI on a Mac.
#LayerCue #LiveProduction #EventProduction

========================================
한국어 (KOREAN)
========================================

TITLE
{i18n.KO[sp['ep']][5]} #Shorts

DESCRIPTION
{' '.join(i18n.KO[sp['ep']][:5])}

베타 기간 무료, Mac과 Windows: https://layercue.com
전체 강좌 — LayerCue 처음부터, {ep}편({ko_t}): {eplink}

========================================
日本語 (JAPANESE)
========================================

TITLE
{i18n.JA[sp['ep']][5]} #Shorts

DESCRIPTION
{''.join(i18n.JA[sp['ep']][:5])}

ベータ期間は無料、Mac と Windows: https://layercue.com
フル講座 — ゼロから LayerCue 第{ep}回({ja_t}): {eplink}
"""
    (out / f"{sid}-upload.txt").write_text(txt)
    on = "short" + sid[1:]                       # OneDrive 는 short01–03 과 같은 이름(shortNN-…)
    dst = OD / on; (dst / "subtitles").mkdir(parents=True, exist_ok=True)
    for f in (".mp4", "-cover.jpg"): shutil.copy(out / f"{sid}{f}", dst / f"{on}{f}")
    (dst / f"{on}-upload.txt").write_text(txt.replace(f"subtitles/{sid}-", f"subtitles/{on}-"))
    for f in (out / "subtitles").glob("*.srt"): shutil.copy(f, dst / "subtitles" / ("short" + f.name[1:]))
    print("packaged", sid)
if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(p.name for p in H.glob("s[0-9]*") if p.is_dir())
    for i in ids: one(H / i)
