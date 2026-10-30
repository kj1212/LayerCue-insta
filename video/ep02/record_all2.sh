#!/bin/zsh
# 2판 창 녹화 — ep02/take2/sN.json 차례로(기본 s1–s8). ffmpeg 30 fps 고정 → ep02/rec/v2/sN.mp4
cd "${0:a:h}/.." || exit 1
export LC_SANDBOX=sandbox-ep02 REC_SUB=v2
SEGS=("$@"); [ $# -eq 0 ] && SEGS=(s1 s2 s3 s4 s5 s6 s7 s8)
for s in $SEGS; do echo "── $s"; ep02/record.py ep02/take2/$s.json || { echo "FAILED $s"; exit 1; }; sleep 1.5; done
python3 lc.py run_commands '{"commands":[{"op":"clear","layer":"all"}]}' >/dev/null; echo "all done"
