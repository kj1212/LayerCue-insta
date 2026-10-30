#!/bin/zsh
# 녹화본 아래 띠에 macOS Dock 이 끼었는지 — ./dockscan.sh ep02/rec/v2/*.mp4  (색이 진한 아이콘 줄을 찾는다)
for f in "$@"; do
  ffmpeg -v error -i "$f" -vf "fps=4,crop=3840:110:0:2045,scale=480:14" -pix_fmt rgb24 -f rawvideo - 2>/dev/null | python3 -c "
import sys
d=sys.stdin.buffer.read(); fs=480*14*3; hits=[]
for i in range(len(d)//fs):
    f=d[i*fs:(i+1)*fs]; s=sum(max(f[j:j+3])-min(f[j:j+3]) for j in range(0,len(f),3))/(480*14)
    if s>18: hits.append(i/4)
print('$f', 'DOCK at %s s' % hits[:6] if hits else 'clean')"
done
