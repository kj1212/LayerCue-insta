#!/bin/zsh
# 기기 이름 패치 뒤 본편 다시 렌더 — 녹화만 바뀌었으니 타임라인·믹스는 그대로
cd "${0:a:h}/.." || exit 1
for E in "$@"; do
  RENDER_NOW=1 OUT_NAME=layercue-$E ./ae.sh $E/build_v2 > $E/qa/render.log 2>&1
  osascript -e 'tell application "Adobe After Effects 2026" to quit'; sleep 3
  mv render/layercue-$E.aep $E/ae/$E.aep && mv render/layercue-$E.mp4 $E/render/ae-out.mp4
  (cd $E && ffmpeg -v error -y -i render/ae-out.mp4 -i qa/v2-mix.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 256k -shortest -movflags +faststart render/final.mp4)
  python3 package.py ${E#ep} | tail -1
  echo "done $E"
done
