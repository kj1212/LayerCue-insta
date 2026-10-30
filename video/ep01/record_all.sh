#!/bin/zsh
# 구간별 창 녹화를 차례로 — ep01/record_all.sh [s1 s2 …]  (기본: s1–s8)
# 각 구간의 지시서(ep01/take/sNN.json) 대로 상태를 맞추고, 녹화하는 동안 마우스·MCP 동작을 보낸다.
cd "${0:a:h}/.." || exit 1
export LC_SANDBOX=${LC_SANDBOX:-sandbox-ep01}
SEGS=("$@"); [ $# -eq 0 ] && SEGS=(s1 s2 s3 s4 s5 s6 s7 s8)     # ${@:-…} 는 zsh 에서 한 덩어리가 된다
for s in $SEGS; do
  echo "── $s ──"
  ep01/record.py ep01/take/$s.json || { echo "FAILED $s"; exit 1; }
  sleep 1.5
done
python3 lc.py run_commands '{"commands":[{"op":"clear","layer":"all"}]}' >/dev/null
echo "all done"
