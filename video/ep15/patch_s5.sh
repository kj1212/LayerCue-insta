#!/bin/zsh
# 15편 s5(태양계): 새 대화 첫 화면의 이름(TAEHOON)과 아래 한국어 고지를 바로 위 빈 바탕을 복사해 덮는다 — 화면에 보이는 18.1–29.4 s.
# 그다음 상태 막대의 한국어 기기 이름을 영어 패치로(shorts/patch_status.py — 원본은 rec/v2/orig/).
cd "${0:a:h}"
S=rec/v2/s5.mp4; R=rec/v2/s5-raw.mp4
[ -f $R ] || cp $S $R
ffmpeg -v error -y -i $R -filter_complex "[0:v]split=3[m][a][b];[a]crop=390:90:706:375[na];[b]crop=1340:172:60:1816[nf];\
[m][na]overlay=706:470:enable='between(t,17.9,29.6)'[m2];[m2][nf]overlay=60:1988:enable='between(t,17.9,29.6)'" \
  -c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30 $S
~/Documents/AIvoice/.venv/bin/python ../shorts/patch_status.py ep15/$S 2>&1 | tail -2
echo patched
