#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""화면 녹화(가변 프레임률 .mov)를 30 fps 고정으로 다시 담는다 — AVFoundation 으로(ffmpeg 는 이 파일들의 시각을 잘못 읽어 늘어났다).

    ep01/cfr_av.py [s4 s8 …]      → ep01/rec/cfr/<name>.mp4  (H.264 최고 화질 프리셋, 3840×2160, 30 fps, 소리 없음)

AVMutableVideoComposition 의 frameDuration 을 1/30 로 두면 내보내기가 그 간격으로 프레임을 채워 쓴다. 길이는 원본과 같다.
"""
import sys, time, pathlib
import AVFoundation, Foundation, CoreMedia
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "rec" / "cfr"; OUT.mkdir(parents=True, exist_ok=True)
names = sys.argv[1:] or [p.stem for p in sorted((HERE / "rec").glob("*.mov")) if p.stem != "calib"]
for n in names:
    src = HERE / "rec" / f"{n}.mov"; dst = OUT / f"{n}.mp4"; dst.unlink(missing_ok=True)
    asset = AVFoundation.AVURLAsset.alloc().initWithURL_options_(Foundation.NSURL.fileURLWithPath_(str(src)), None)
    track = asset.tracksWithMediaType_(AVFoundation.AVMediaTypeVideo)[0]
    comp = AVFoundation.AVMutableVideoComposition.videoCompositionWithPropertiesOfAsset_(asset)
    comp.setFrameDuration_(CoreMedia.CMTimeMake(1, 30))
    comp.setRenderSize_(track.naturalSize())
    ex = AVFoundation.AVAssetExportSession.alloc().initWithAsset_presetName_(asset, AVFoundation.AVAssetExportPresetHighestQuality)
    ex.setVideoComposition_(comp)
    ex.setOutputURL_(Foundation.NSURL.fileURLWithPath_(str(dst)))
    ex.setOutputFileType_("public.mpeg-4")
    done = {"v": False}
    ex.exportAsynchronouslyWithCompletionHandler_(lambda: done.__setitem__("v", True))
    t0 = time.time()
    while not done["v"] and time.time() - t0 < 900: time.sleep(0.5)
    secs = CoreMedia.CMTimeGetSeconds(asset.duration())
    print(f"{n}: status {ex.status()} error {ex.error()} | src {secs:.2f}s → {dst.name} {dst.stat().st_size/1e6:.1f} MB in {time.time()-t0:.0f}s")
