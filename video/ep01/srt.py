#!/usr/bin/env python3
"""자막·챕터·설명란 — assemble.py 가 쓴 times.json(줄별 시각) 과 script.json 에서.

    python3 ep01/srt.py   → ep01/out/en.srt · ep01/out/chapters.txt · ep01/out/description.txt

한 문장 = 한 큐. 큐는 음성 시작 0.05 s 앞에서 시작해 음성 끝 + 0.3 s 까지(다음 큐와 겹치면 그 앞에서 끊는다).
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
segs = json.load(open(HERE / "times.json"))
script = json.load(open(HERE / "script.json"))


def ts(t):
    t = max(0.0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


cues = []
for seg in segs:
    for l in seg["lines"]:
        cues.append([l["t"] - 0.05, l["t"] + l["dur"] + 0.3, l["text"]])
for i in range(len(cues) - 1):
    if cues[i][1] > cues[i + 1][0] - 0.05: cues[i][1] = cues[i + 1][0] - 0.05
with open(OUT / "en.srt", "w") as f:
    for i, (a, b, text) in enumerate(cues, 1):
        f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n")

with open(OUT / "chapters.txt", "w") as f:
    for seg in segs:
        t = seg["start"]; name = "What's next" if seg["id"] == segs[-1]["id"] else seg["chapter"]
        f.write(f"{int(t // 60)}:{int(t % 60):02d} {name}\n")

with open(OUT / "description.txt", "w") as f:
    f.write("Episode 1 — Meet LayerCue: The Main Window\n\n")
    f.write(script["descriptionYouTube"].strip() + "\n\nChapters\n")
    for seg in segs:
        t = seg["start"]; name = "What's next" if seg["id"] == segs[-1]["id"] else seg["chapter"]
        f.write(f"{int(t // 60)}:{int(t % 60):02d} {name}\n")
print("srt cues", len(cues), "| chapters", len(segs), "→", OUT)
