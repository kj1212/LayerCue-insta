#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""화면 녹화(가변 프레임률 .mov)를 30 fps 고정으로 — 애플의 AVAssetImageGenerator 가 읽는 시각이 맞다고 보고,
1/30 초마다 그 시각의 그림을 뽑아 ffmpeg 에 바로 흘려 넣는다(중간 파일 없음). ffmpeg 의 fps 필터와 AVAssetExportSession 은
이 파일들의 시각을 다르게 읽어 길이가 늘거나 줄었다(2026-10-30).

    ep01/cfr_gen.py [s4 s8 …]      → ep01/rec/cfr/<name>.mp4  (H.264 videotoolbox 60 Mbps, 3840×2160, 30 fps, 무음)
"""
import sys, subprocess, pathlib, time
import AVFoundation, Foundation, CoreMedia, Quartz
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "rec" / "cfr"; OUT.mkdir(parents=True, exist_ok=True)
FPS = 30
names = sys.argv[1:] or [p.stem for p in sorted((HERE / "rec").glob("*.mov")) if p.stem != "calib"]
for n in names:
    src = HERE / "rec" / f"{n}.mov"; dst = OUT / f"{n}.mp4"; dst.unlink(missing_ok=True)
    asset = AVFoundation.AVURLAsset.alloc().initWithURL_options_(Foundation.NSURL.fileURLWithPath_(str(src)), None)
    dur = CoreMedia.CMTimeGetSeconds(asset.duration())
    gen = AVFoundation.AVAssetImageGenerator.alloc().initWithAsset_(asset)
    gen.setRequestedTimeToleranceBefore_(CoreMedia.kCMTimeZero); gen.setRequestedTimeToleranceAfter_(CoreMedia.kCMTimeZero)
    nframes = int(round(dur * FPS))
    ff = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "3840x2160", "-r", str(FPS), "-i", "-",
                           "-c:v", "h264_videotoolbox", "-b:v", "60M", "-maxrate", "80M", "-bufsize", "120M", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)],
                          stdin=subprocess.PIPE)
    t0 = time.time(); last = None
    for i in range(nframes):
        res = gen.copyCGImageAtTime_actualTime_error_(CoreMedia.CMTimeMakeWithSeconds(i / FPS, 600), None, None)
        img = res[0] if isinstance(res, tuple) else res
        if img is not None:
            w, h, bpr = Quartz.CGImageGetWidth(img), Quartz.CGImageGetHeight(img), Quartz.CGImageGetBytesPerRow(img)
            data = bytes(Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(img)))
            if bpr != w * 4:        # 줄 끝 여백이 있으면 잘라 낸다
                data = b"".join(data[r * bpr: r * bpr + w * 4] for r in range(h))
            last = data
        if last is None: continue
        ff.stdin.write(last)
    ff.stdin.close(); ff.wait()
    print(f"{n}: {nframes} frames / {dur:.2f}s → {dst.name} {dst.stat().st_size/1e6:.1f} MB in {time.time()-t0:.0f}s")
