#!/usr/bin/env python3
"""목소리 후보 — 같은 다섯 줄을 목소리마다 만들어 0.55 s 쉼으로 잇는다.  ~/Documents/AIvoice/.venv/bin/python ep01/voice_samples.py"""
import subprocess, sys, pathlib, numpy as np, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE / "audio" / "samples"; RAW = OUT / ".raw"; RAW.mkdir(parents=True, exist_ok=True)
PY = pathlib.Path.home() / "Documents/AIvoice/.venv/bin/python"
LINES = [l.strip() for l in open(OUT / "lines.txt") if l.strip()]
VOICES = {
  "A-heart":    ["--model", "mlx-community/Kokoro-82M-bf16", "--voice", "af_heart", "--speed", "1.0"],
  "B-michael":  ["--model", "mlx-community/Kokoro-82M-bf16", "--voice", "am_michael", "--speed", "1.0"],
  "C-chatterbox": ["--model", "mlx-community/chatterbox-fp16", "--exaggeration", "0.6", "--cfg_scale", "0.3"],
}
for name, opts in VOICES.items():
    parts, sr = [], 24000
    for i, line in enumerate(LINES):
        pre = f"{name}-{i}"
        r = subprocess.run([str(PY), "-m", "mlx_audio.tts.generate", *opts, "--text", line, "--output_path", str(RAW), "--file_prefix", pre, "--join_audio", "--audio_format", "wav"], capture_output=True, text=True)
        if r.returncode: sys.exit(r.stderr[-800:])
        a, sr = sf.read(RAW / f"{pre}.wav"); a = a if a.ndim == 1 else a.mean(axis=1)
        nz = np.flatnonzero(np.abs(a) > 0.01); a = a[max(nz[0] - int(0.04 * sr), 0): nz[-1] + int(0.1 * sr)]
        parts += [a, np.zeros(int(0.55 * sr))]
    y = np.concatenate(parts); y = y / (np.abs(y).max() + 1e-9) * 0.7
    sf.write(OUT / f"voice-{name}.wav", y, sr); print(name, round(len(y) / sr, 1), "s")
