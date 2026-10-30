#!/usr/bin/env python3
"""한 편을 업로드 폴더로 묶는다 — youtube/epNN/
    python3 package.py 1

  epNN/video.mp4          최종 영상(영어 자막 박힘)
  epNN/thumbnail.jpg      1280×720
  epNN/upload.txt         유튜브에 붙일 글(영어): 제목 · 설명(챕터 포함) · 태그 · 재생목록
  epNN/subtitles/ko.srt   한국어 자막   (유튜브 → 자막 → 언어 추가 → 파일 업로드 · 시간 포함)
  epNN/subtitles/ja.srt   일본어 자막
  epNN/subtitles/en.srt   영어(화면에 이미 박혀 있으니 올리지 않아도 된다 · 번역 기준용)
  epNN/SCRIPT.md          대본(영·한)
재료: video/epNN/ 의 times2.json · script.json · i18n/{ko,ja}.json · out/thumbnail.jpg · out/meta.json · render/final.mp4
"""
import json, shutil, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
n = int(sys.argv[1]); E = HERE / f"ep{n:02d}"; OUT = HERE.parent / "youtube" / f"ep{n:02d}"
(OUT / "subtitles").mkdir(parents=True, exist_ok=True)
segs = json.load(open(E / "times2.json")); S = json.load(open(E / "script.json")); meta = json.load(open(E / "out" / "meta.json"))

def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); x = t % 60; return f"{h:02d}:{m:02d}:{x:06.3f}".replace(".", ",")
lines = [l for g in segs for l in g["lines"]]
cues = [[l["t"] - 0.05, l["t"] + l["dur"] + 0.3, l["key"], l["text"]] for l in lines]
for i in range(len(cues) - 1):
    if cues[i][1] > cues[i + 1][0] - 0.05: cues[i][1] = cues[i + 1][0] - 0.05
for lang in ["en", "ko", "ja"]:
    tr = {c[2]: c[3] for c in cues} if lang == "en" else json.load(open(E / "i18n" / f"{lang}.json"))
    miss = [c[2] for c in cues if c[2] not in tr]
    if miss: sys.exit(f"{lang}: missing {miss}")
    (OUT / "subtitles" / f"{lang}.srt").write_text("".join(f"{i}\n{ts(a)} --> {ts(b)}\n{tr[k]}\n\n" for i, (a, b, k, _) in enumerate(cues, 1)), encoding="utf-8")

chap = ["0:00 Intro"] + [f"{int(g['start'] // 60)}:{int(g['start'] % 60):02d} {g['chapter']}" for g in segs]
up = [f"TITLE\n{meta['title']}\n", "DESCRIPTION", meta["description"].strip(), "", "Chapters", *chap, "",
      f"TAGS\n{', '.join(meta['tags'])}\n", f"PLAYLIST\n{meta['playlist']}\n",
      "SUBTITLES\nUpload subtitles/ko.srt (Korean) and subtitles/ja.srt (Japanese) as 'With timing'. English is burned in."]
(OUT / "upload.txt").write_text("\n".join(up) + "\n", encoding="utf-8")
ko = json.load(open(E / "i18n" / "ko.json"))
md = [f"# {meta['title']}", ""]
for g in segs:
    md += [f"## {g['chapter']}", ""] + [f"- {l['text']}  \n  {ko[l['key']]}" for l in g["lines"]] + [""]
(OUT / "SCRIPT.md").write_text("\n".join(md), encoding="utf-8")
shutil.copy(E / "render" / "final.mp4", OUT / "video.mp4"); shutil.copy(E / "out" / "thumbnail.jpg", OUT / "thumbnail.jpg")
for old in ["LayerCue-from-Zero-Ep01-Meet-LayerCue-The-Main-Window.mp4", "en.srt", "chapters.txt", "description.txt", "thumbnail.png"]:
    (OUT / old).unlink(missing_ok=True)
print("packaged →", OUT); [print("  ", p.relative_to(OUT)) for p in sorted(OUT.rglob("*")) if p.is_file()]
