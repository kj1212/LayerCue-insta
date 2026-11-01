#!/bin/zsh
# 14편: 저장 창 Where 메뉴가 열린 동안(녹화 s5 14.85–16.45 s) 개인 항목(컴퓨터 이름 · 클라우드 · 위치 · 최근 폴더)을 흐리게. 원본은 rec/v2/orig/s5.mp4
cd "${0:a:h}"
ffmpeg -v error -y -i rec/v2/orig/s5.mp4 -filter_complex "\
[0]split=3[b][a1][a2];[a1]crop=514:554:1728:1162,boxblur=18:2[p1];[a2]crop=514:168:1728:1975,boxblur=18:2[p2];\
[b][p1]overlay=1728:1162:enable='between(t,14.85,16.45)'[c];[c][p2]overlay=1728:1975:enable='between(t,14.85,16.45)'" \
-c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30 rec/v2/s5.mp4 && echo patched
