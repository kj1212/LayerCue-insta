#!/bin/zsh
# 숏츠 전부 AE 렌더 → shorts/<id>/out/<id>.mp4 (loudnorm −14)
cd "${0:a:h}/.." || exit 1
for d in ${@:-shorts/s[0-9]*/}; do id=$(basename $d)
  RENDER_NOW=1 OUT_NAME=$id ./ae.sh shorts/build_short > shorts/$id/render.log 2>&1
  osascript -e 'tell application "Adobe After Effects 2026" to quit'; sleep 3
  mkdir -p shorts/$id/out && mv render/$id.mp4 shorts/$id/out/ae-out.mp4 && mv render/$id.aep shorts/$id/out/$id.aep
  ffmpeg -v error -y -i shorts/$id/out/ae-out.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 256k -movflags +faststart shorts/$id/out/$id.mp4
  echo "done $id $(ffprobe -v error -show_entries format=duration -of csv=p=0 shorts/$id/out/$id.mp4)"
done
