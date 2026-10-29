#!/bin/bash
# AE 스크립트 돌리기 — ./ae.sh build_short
# LayerCue/tools/design-lab/ae/run.sh 와 같은 길: 앞에 ROOT·OUT_DIR·logTo 를 붙여 임시 파일로 만들고 osascript 로 AE 에 보낸다.
# ★ AE 에 열린 프로젝트를 저장하지 않고 닫는다 — 작업 중이면 먼저 저장할 것.
cd "$(dirname "$0")" || exit 1
HERE="$PWD"; OUT="$HERE/render"; mkdir -p "$OUT"
APP="${AE_APP:-Adobe After Effects 2026}"
TMP="$OUT/.run-$1.jsx"
{
  echo "var ROOT = \"$HERE\"; var OUT_DIR = \"$OUT\"; var AUDIO_DIR = \"${AUDIO_DIR:-audio}\"; var OUT_NAME = \"${OUT_NAME:-layercue-ask-short}\"; var MUSIC_FILE = \"${MUSIC_FILE:-}\";"
  echo 'function logTo(p, s) { var f = new File(p); f.encoding = "UTF-8"; f.open("a"); f.writeln(s); f.close(); }'
  echo "try {"; cat "$HERE/$1.jsx"
  echo "} catch (err) { logTo(OUT_DIR + \"/build.log\", \"오류: \" + err.toString() + \" (줄 \" + err.line + \")\"); }"
} > "$TMP"
rm -f "$OUT/build.log"
osascript -e "tell application \"$APP\" to DoScriptFile \"$TMP\""
tr '\r' '\n' < "$OUT/build.log" 2>/dev/null
