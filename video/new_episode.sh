#!/bin/zsh
# 새 편 폴더 — 1편의 파이프라인을 복사하고 편 번호만 바꾼다.  ./new_episode.sh 2
# (대본 script.json · 연출 shotlist2.json · 번역 i18n/ · 그래픽 gfx 는 편마다 새로 쓴다)
set -e
N=$1; P=$(printf "%02d" $N); E=ep$P; cd "${0:a:h}"
mkdir -p $E/{audio,rec,render,ae,out,i18n,parts2,frames,take2,qa}
for f in assemble2.py build_v2.jsx voice.py record.py record_all2.sh record_stage.sh music.py music_full.py final_mix.py \
         brand.css parts.html bg.html title-anim.html end-anim.html regions.json ocr.py frame.py shot.py; do
  [ -f $E/$f ] || cp ep02/$f $E/$f
done
sed -i "" "s/e02-/e$P-/g" $E/voice.py $E/assemble2.py $E/final_mix.py
sed -i '' "s|ep01/|$E/|g" $E/build_v2.jsx $E/record_all2.sh $E/record_stage.sh $E/final_mix.py
sed -i '' "s|LayerCue-ep01-v2|LayerCue-$E|; s|\"music-ep01.wav\"|\"music-$E.wav\"|" $E/assemble2.py
sed -i '' "s|music-ep01.wav|music-$E.wav|g" $E/music_full.py $E/final_mix.py
cp -n ep01/audio/loops.json $E/audio/ 2>/dev/null || true
echo "ready: video/$E"
