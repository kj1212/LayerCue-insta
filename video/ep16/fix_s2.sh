#!/bin/zsh
# 16편 s2: Add screen 을 누르는 순간 맥이 화면 배치를 다시 잡으며 캡처가 0.4 s 작게 찍혔다(12.13–12.50 s) — 바로 앞 프레임으로 덮는다
cd "${0:a:h}"
[ -f rec/v2/s2-glitch.mp4 ] || cp rec/v2/s2.mp4 rec/v2/s2-glitch.mp4
ffmpeg -v error -y -ss 12.08 -i rec/v2/s2-glitch.mp4 -frames:v 1 qa/s2hold.png
ffmpeg -v error -y -i rec/v2/s2-glitch.mp4 -loop 1 -i qa/s2hold.png -filter_complex "[0:v][1:v]overlay=0:0:enable='between(t,12.11,12.58)':shortest=1" \
  -c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30 rec/v2/s2.mp4
