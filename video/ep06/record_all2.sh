#!/bin/zsh
# 2판 창 녹화 — ep06/take2/sN.json 차례로(기본 s1–s8). ffmpeg 30 fps 고정 → ep06/rec/v2/sN.mp4
cd "${0:a:h}/.." || exit 1
export LC_SANDBOX=sandbox-ep06 REC_SUB=v2
# 3편: 조작 창은 맥북(주 화면) · 프로젝터는 LG — 둘 다 찍는다. 창 자리(포인트)와 자를 자리(px)는 ep06/place.sh 와 같아야 한다
export MOUSE_WIN="60,110,1680,919" REC_DEV="2:none" REC_CROP="3360:1838:120:220"
# 녹화 시작·끝을 알린다(맥북 화면 알림 + 소리) — 녹화 중에 마우스를 움직이면 화면에 그대로 찍힌다(2026-10-30 Dock 이 끼었다)
note() { osascript -e "display notification \"$2\" with title \"LayerCue 녹화\" subtitle \"$1\" sound name \"$3\"" 2>/dev/null; }
SEGS=("$@"); [ $# -eq 0 ] && SEGS=(s2 s3 s4 s5 s6 s7)
note "● 곧 녹화 시작" "8 초 뒤 시작해요. 끝날 때까지 마우스·키보드를 건드리지 마세요 (${#SEGS} 구간)" "Submarine"
ep06/clear_finder.sh; sleep 8     # 알림 배너가 맥북 화면(녹화되는 창 위)에서 사라질 때까지
for s in $SEGS; do echo "── $s"; ep06/record.py ep06/take2/$s.json || { echo "FAILED $s"; exit 1; }; sleep 1.5; done
python3 lc.py run_commands '{"commands":[{"op":"clear","layer":"all"}]}' >/dev/null; echo "all done"; note "■ 녹화 끝" "이제 마우스를 써도 됩니다" "Glass"
