#!/bin/zsh
# 화면 녹화(screencapture -v)는 가변 프레임률이라 — 바뀐 프레임만 담겨 정지 화면 구간은 6 fps 정도 — AE 가 시각을 어긋나게 읽는다
# (포인터·툴팁이 엉뚱한 시각에 나오거나 안 나온다). 30 fps 고정 프레임률로 다시 담는다. 타임스탬프는 그대로라 in/out 은 안 바뀐다.
#   ep01/cfr.sh            → ep01/rec/cfr/*.mp4 (모든 .mov)
#   ep01/cfr.sh s4 s8      → 그 것만
cd "${0:a:h}" || exit 1
mkdir -p rec/cfr
FILES=("$@"); [ $# -eq 0 ] && FILES=($(ls rec/*.mov | xargs -n1 basename | sed 's/\.mov$//'))
for n in $FILES; do
  [ "$n" = "calib" ] && continue
  echo "── $n"
  ffmpeg -y -hide_banner -loglevel error -i "rec/$n.mov" -vf "fps=30" -c:v libx264 -preset medium -crf 14 -pix_fmt yuv420p -movflags +faststart -an "rec/cfr/$n.mp4" || exit 1
done
ls -la rec/cfr | awk 'NR>1{print $5, $9}'
