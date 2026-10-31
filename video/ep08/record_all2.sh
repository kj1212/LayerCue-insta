#!/bin/zsh
# 2판 창 녹화 — ep08/take2/sN.json 차례로(기본 s1–s8). ffmpeg 30 fps 고정 → ep08/rec/v2/sN.mp4
cd "${0:a:h}/.." || exit 1
export LC_SANDBOX=sandbox-ep08 REC_SUB=v2
# 창은 ./sb.sh place 로 LG 에 꽉 채운다
# 7편부터 다시 LG(1920×1080 HiDPI, 4K 그대로)에서 찍는다 — 맥북은 3360 px 를 3840 으로 늘려 덜 선명했다. 3편만 맥북+LG 두 화면이었다
export REC_DEV="3:none"
# 녹화 시작·끝을 알린다(맥북 화면 알림 + 소리) — 녹화 중에 마우스를 움직이면 화면에 그대로 찍힌다(2026-10-30 Dock 이 끼었다)
note() { osascript -e "display notification \"$2\" with title \"LayerCue 녹화\" subtitle \"$1\" sound name \"$3\"" 2>/dev/null; }
SEGS=("$@"); [ $# -eq 0 ] && SEGS=(s2 s3 s4 s5 s6 s7)
note "● 곧 녹화 시작" "8 초 뒤 시작해요. 끝날 때까지 마우스·키보드를 건드리지 마세요 (${#SEGS} 구간)" "Submarine"
ep08/clear_finder.sh; sleep 8     # 알림 배너가 맥북 화면(녹화되는 창 위)에서 사라질 때까지
for s in $SEGS; do echo "── $s"; ep08/record.py ep08/take2/$s.json || { echo "FAILED $s"; exit 1; }; sleep 1.5; done
python3 lc.py run_commands '{"commands":[{"op":"clear","layer":"all"}]}' >/dev/null; echo "all done"; note "■ 녹화 끝" "이제 마우스를 써도 됩니다" "Glass"
