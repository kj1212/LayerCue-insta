#!/bin/zsh
# 맥북 화면의 LayerCue 창을 3편 녹화 꼴(3840×2100)로 한 장 찍는다 → $1 (기본 qa/peek.png)
cd "${0:a:h}" || exit 1
O=${1:-qa/peek.png}
ffmpeg -hide_banner -loglevel error -y -f avfoundation -capture_cursor 1 -framerate 30 -pixel_format nv12 -i "2:none" -t 0.4 -c:v h264_videotoolbox -b:v 20M /tmp/peek.mp4 2>&1 | grep -v objc
ffmpeg -v error -y -sseof -0.1 -i /tmp/peek.mp4 -frames:v 1 -vf "crop=3360:1838:120:220,scale=3840:2100" "$O"
