#!/bin/zsh
# 무대(송출 창) 녹화 — 송출을 LG 화면으로 돌리고, 세 층을 띄워 4.5 초 기다린 뒤(자리 잡힘) 찍는다. 끝나면 가상 화면으로 되돌린다.
cd "${0:a:h}/.." || exit 1
export LC_SANDBOX=sandbox-ep07
INI=sandbox-ep07/settings/LayerCueFilm/LayerCueFilm.ini
./sb.sh quit >/dev/null; sleep 2
cp "$INI" "$INI.virtual"
sed -i '' 's|^outputScreenKey=.*|outputScreenKey=LG HDR 4K|; s|^winX=.*|winX=100|; s|^winY=.*|winY=120|; s|^winW=.*|winW=1600|; s|^winH=.*|winH=900|' "$INI"
./sb.sh launch sandbox-ep07 >/dev/null; sleep 9
python3 lc.py run_commands '{"commands":[{"op":"output","on":true},{"op":"clear","layer":"all"},{"op":"useCue","name":"Summit Day 1"},{"op":"openCue","name":"Summit Day 1"},{"op":"usePt","name":"Welcome loop"},{"op":"present","n":1},{"op":"usePt","name":"Welcome words"},{"op":"present","n":1},{"op":"usePt","name":"Summit logo"},{"op":"present","n":1}]}' >/dev/null
/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python -c 'import Quartz; Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (900, 600), 0))'   # 포인터를 맥북 화면으로 치운다
sleep 4.5
REC_CURSOR=0 MOUSE_ANY_SCALE=1 REC_SUB=v2 ep07/record.py ep07/take2/stage.json
python3 lc.py run_commands '{"commands":[{"op":"clear","layer":"all"},{"op":"output","on":false}]}' >/dev/null
./sb.sh quit >/dev/null; sleep 2
cp "$INI.virtual" "$INI"
./sb.sh launch sandbox-ep07 >/dev/null; sleep 9; ./sb.sh place >/dev/null
python3 lc.py run_commands '{"commands":[{"op":"output","on":true}]}' >/dev/null
echo "stage done; screen: $(python3 lc.py get_state | python3 -c 'import json,sys; print(json.load(sys.stdin)["outputs"][0]["screen"])')"
