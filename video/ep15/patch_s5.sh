#!/bin/zsh
# 15편 s5(태양계):
#  1) 새 대화 첫 화면의 이름(TAEHOON)과 아래 한국어 고지를, 바로 위 빈 바탕을 복사해 덮는다 — 화면에 보이는 18.1–29.4 s
#  2) 상태 막대의 한국어 기기 이름을 영어 패치로(shorts/patch_status.py, 자리 x 1272)
#  3) Edit 화면(38.77–48.83 s)에선 기기 이름 상자가 282 px 오른쪽 — 2) 가 잘못 덮은 자리를 되살리고 x 1554 에 덮는다
cd "${0:a:h}"
R=rec/v2/s5-raw.mp4; C=rec/v2/s5-cover.mp4; S=rec/v2/s5.mp4; P=../ep12/patch/status.png; E="between(t,38.75,48.85)"
[ -f $R ] || cp $S $R
ffmpeg -v error -y -i $R -filter_complex "[0:v]split=3[m][a][b];[a]crop=390:90:706:375[na];[b]crop=1340:172:60:1816[nf];\
[m][na]overlay=706:470:enable='between(t,17.9,29.6)'[m2];[m2][nf]overlay=60:1988:enable='between(t,17.9,29.6)'" \
  -c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30 $C
cp $C $S
~/Documents/AIvoice/.venv/bin/python ../shorts/patch_status.py ep15/$S 2>&1 | tail -1
mv $S rec/v2/s5-st.mp4
ffmpeg -v error -y -i rec/v2/s5-st.mp4 -i $C -loop 1 -i $P -filter_complex "[1:v]crop=72:36:1272:2104[o];[0:v][o]overlay=1272:2104:enable='$E'[v1];[v1][2:v]overlay=1554:2104:enable='$E':shortest=1" \
  -c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30 $S
rm rec/v2/s5-st.mp4
echo patched
