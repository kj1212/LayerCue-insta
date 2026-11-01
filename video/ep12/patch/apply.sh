#!/bin/zsh
# 12편: 녹화(rec/v2/sN.mp4)에 영어 기기 이름 패치를 덮는다 — 원본은 rec/v2/orig/ 에 둔다.  ./patch/apply.sh
cd "${0:a:h}/.." || exit 1
mkdir -p rec/v2/orig
for s in s1 s2 s3 s4 s5 s6; do [ -f rec/v2/orig/$s.mp4 ] || cp rec/v2/$s.mp4 rec/v2/orig/$s.mp4; done
enc=(-c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30)
# s1: 목록(프레임 887–1105, 마우스가 지나는 줄은 밝은 배경), 그 뒤 상태 상자
ffmpeg -v error -y -i rec/v2/orig/s1.mp4 -i patch/row1.png -i patch/row1h.png -i patch/row2.png -i patch/row2h.png -i patch/status.png -filter_complex "\
[0][1]overlay=1314:1846:enable='between(n,887,1095)'[a];[a][2]overlay=1314:1846:enable='between(n,1096,1105)'[b];\
[b][3]overlay=1150:1924:enable='between(n,887,1089)+between(n,1096,1105)'[c];[c][4]overlay=1150:1924:enable='between(n,1090,1095)'[d];\
[d][5]overlay=1272:2104:enable='gte(n,1106)'" $enc rec/v2/s1.mp4
for s in s2 s3 s4 s5 s6; do
  ffmpeg -v error -y -i rec/v2/orig/$s.mp4 -i patch/status.png -filter_complex "[0][1]overlay=1272:2104" $enc rec/v2/$s.mp4
done
echo patched
