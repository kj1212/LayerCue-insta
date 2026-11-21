#!/bin/zsh
# 17편: Add screen 을 누르는 순간 맥이 화면 배치를 다시 잡아 캡처가 0.4 s 작게 찍혔다 — 바로 앞 프레임으로 덮는다.  fix_glitch.sh s1 13.65 14.12
cd "${0:a:h}"; S=$1; A=$2; B=$3
[ -f rec/v2/$S-glitch.mp4 ] || cp rec/v2/$S.mp4 rec/v2/$S-glitch.mp4
ffmpeg -v error -y -ss $((A-0.05)) -i rec/v2/$S-glitch.mp4 -frames:v 1 qa/$S-hold.png
ffmpeg -v error -y -i rec/v2/$S-glitch.mp4 -loop 1 -i qa/$S-hold.png -filter_complex "[0:v][1:v]overlay=0:0:enable='between(t,$A,$B)':shortest=1" \
  -c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30 rec/v2/$S.mp4
