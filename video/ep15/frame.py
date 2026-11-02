#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""영상에서 정지 그림 한 장 — ffmpeg 없이 AVFoundation 으로.

    ep01/frame.py <mov> <sec> <out.png> [maxWidth]
"""
import sys
import AVFoundation, CoreMedia, Quartz, Foundation

mov, sec, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
maxw = int(sys.argv[4]) if len(sys.argv) > 4 else 0
asset = AVFoundation.AVURLAsset.alloc().initWithURL_options_(Foundation.NSURL.fileURLWithPath_(mov), None)
gen = AVFoundation.AVAssetImageGenerator.alloc().initWithAsset_(asset)
gen.setRequestedTimeToleranceBefore_(CoreMedia.kCMTimeZero); gen.setRequestedTimeToleranceAfter_(CoreMedia.kCMTimeZero)
gen.setAppliesPreferredTrackTransform_(True)
if maxw: gen.setMaximumSize_(Foundation.NSMakeSize(maxw, maxw))
res = gen.copyCGImageAtTime_actualTime_error_(CoreMedia.CMTimeMakeWithSeconds(sec, 600), None, None)
img = res[0] if isinstance(res, tuple) else res
actual = CoreMedia.CMTimeMakeWithSeconds(sec, 600)
if img is None:
    raise SystemExit("no frame: %s" % (res,))
dest = Quartz.CGImageDestinationCreateWithURL(Foundation.NSURL.fileURLWithPath_(out), "public.png", 1, None)
Quartz.CGImageDestinationAddImage(dest, img, None); Quartz.CGImageDestinationFinalize(dest)
print(out, "at", round(CoreMedia.CMTimeGetSeconds(actual), 3), "s; duration", round(CoreMedia.CMTimeGetSeconds(asset.duration()), 2), "s")
