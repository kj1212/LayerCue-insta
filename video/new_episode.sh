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
# 2편에서 복사하므로 ep02 → epNN(폴더·모래상자·음악·컴프 이름 모두). 3편 때 ep02 를 그대로 가리켜 2편을 덮어쓸 뻔했다
sed -i '' "s|ep02|$E|g" $E/assemble2.py $E/build_v2.jsx $E/music_full.py $E/final_mix.py $E/record_all2.sh $E/record_stage.sh
cp -n ep01/audio/loops.json $E/audio/ 2>/dev/null || true
echo "ready: video/$E"
