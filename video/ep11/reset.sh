#!/bin/zsh
# 11편 촬영 시작 상태로 되돌린다 — 앱을 끄고 sandbox-ep11.base(Prize Night 7장, 빈 음악 목록)를 다시 깔고 켠 뒤, 데모 Finder 창을 놓는다
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep11/docs sandbox-ep11/settings && cp -R sandbox-ep11.base/docs sandbox-ep11.base/settings sandbox-ep11/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep11 ./sb.sh launch sandbox-ep11 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
ep11/finder.sh >/dev/null 2>&1      # 11편: 데모 Finder 창(Prize Night music)을 카드 아래 빈자리에 — 녹화의 "front" 가 LayerCue 를 다시 앞으로
