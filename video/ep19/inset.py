#!/usr/bin/env python3
"""19편: 관객 화면(Stage Monitor) 정지 사진(rec/v2/aud/<take>-<k>.png)을 녹화 오른쪽 위 작은 창으로 굽는다.
   사진이 찍힌 시각 = 연출표의 SNAP 시각(take2 의 sh) + rec_t0. 원본은 rec/v2/orig/ 에 남긴다.
    ../.venv/bin/python inset.py s1 s2"""
import json, re, subprocess, sys, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H = pathlib.Path(__file__).resolve().parent; R = H / "rec" / "v2"
R0 = json.load(open(H / "shotlist2.json"))["rec_t0"]
X, Y, W = 3060, 96, 720; Hh = W * 9 // 16; RAD = 22
FONT = ImageFont.truetype("/Users/kj1212/projects/LayerCue/qml/assets/fonts/DMMono-Medium.ttf", 26)
def plate(img_path, out):
    fr = Image.new("RGBA", (3840, 2160), (0, 0, 0, 0))
    sh = Image.new("RGBA", (3840, 2160), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([X - 4, Y + 10, X + W + 4, Y + Hh + 18], RAD, fill=(0, 0, 0, 150))
    fr = Image.alpha_composite(fr, sh.filter(ImageFilter.GaussianBlur(18)))
    pic = Image.open(img_path).convert("RGB").resize((W, Hh), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (W, Hh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, W - 1, Hh - 1], RAD, fill=255)
    fr.paste(pic, (X, Y), m)
    d = ImageDraw.Draw(fr); d.rounded_rectangle([X, Y, X + W - 1, Y + Hh - 1], RAD, outline=(242, 238, 228, 230), width=3)
    t = "AUDIENCE SCREEN"; tw = d.textlength(t, font=FONT)
    chip = Image.new("RGBA", (int(tw) + 36, 46), 0); cg = Image.new("RGBA", chip.size)
    for x in range(chip.size[0]):
        f = x / max(1, chip.size[0] - 1); c = (int(255), int(201 + (94 - 201) * f), int(77 + (138 - 77) * f), 255)
        ImageDraw.Draw(cg).line([(x, 0), (x, chip.size[1])], fill=c)
    cm = Image.new("L", chip.size, 0); ImageDraw.Draw(cm).rounded_rectangle([0, 0, chip.size[0] - 1, chip.size[1] - 1], 10, fill=255)
    fr.paste(cg, (X + 18, Y + 16), cm); d.text((X + 36, Y + 25), t, font=FONT, fill=(20, 20, 20, 255))
    fr.save(out)
for take in sys.argv[1:]:
    acts = json.load(open(H / "take2" / f"{take}.json"))["actions"]
    snaps = sorted((a["t"] + R0, re.search(r"rec/v2/aud/(\S+)\.png", a["sh"]).group(1)) for a in acts if "sh" in a and "rec/v2/aud/" in a["sh"])
    (R / "orig").mkdir(exist_ok=True); src = R / "orig" / f"{take}.mp4"
    if not src.exists(): (R / f"{take}.mp4").replace(src)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
    ins, fl, last = ["-i", str(src)], [], "[0:v]"
    for i, (t, name) in enumerate(snaps):
        p = R / "aud" / f"plate-{name}.png"; plate(R / "aud" / f"{name}.png", p); ins += ["-loop", "1", "-i", str(p)]
        t0 = 0 if i == 0 else round(t, 3); t1 = round(snaps[i + 1][0], 3) if i + 1 < len(snaps) else dur
        fl.append(f"{last}[{i + 1}:v]overlay=0:0:enable='between(t,{t0},{t1})':shortest=1[v{i}]"); last = f"[v{i}]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", last, "-c:v", "h264_videotoolbox", "-b:v", "50M",
                    "-pix_fmt", "yuv420p", "-r", "30", str(R / f"{take}.mp4")], check=True)
    print("inset", take, [(round(t, 2), n) for t, n in snaps])
