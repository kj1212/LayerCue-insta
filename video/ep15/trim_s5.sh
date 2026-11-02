#!/bin/zsh
# 15편 s5: Claude 가 일하는 13.85 s 를 잘라 낸다(v 33.14 → 46.99, 0.3 s 디졸브) · 대화 첫 화면의 이름과 한국어 고지를 바탕색(23)으로 덮는다(v 17.9–28.9)
cd "${0:a:h}"
S=rec/v2/old/s5-full.mp4; A=33.14; B=46.99; X=0.3
ffmpeg -v error -y -i $S -filter_complex "\
[0:v]drawbox=x=806:y=462:w=394:h=94:color=0x171717:t=fill:enable='between(t,17.9,28.9)',drawbox=x=90:y=1995:w=1260:h=120:color=0x171717:t=fill:enable='between(t,17.9,28.9)',split[a][b];\
[a]trim=0:$A,setpts=PTS-STARTPTS[p];[b]trim=start=$((B-X)),setpts=PTS-STARTPTS[q];[p][q]xfade=transition=fade:duration=$X:offset=$((A-X))" \
 -c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p -r 30 rec/v2/s5.mp4
~/Documents/AIvoice/.venv/bin/python -c "
import soundfile as sf, numpy as np
a,sr=sf.read('rec/v2/old/s5-full.wav'); sf.write('rec/v2/s5.wav', np.zeros((int(len(a)-13.85*sr),2)), sr)"
echo trimmed
