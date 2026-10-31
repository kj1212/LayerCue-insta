#!/bin/zsh
# 6편 촬영 시작 상태로 되돌린다 — 앱을 끄고 sandbox-ep10.base 를 다시 깔고 켠 뒤, 데모 Finder 창을 맨 앞에 둔다
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep10/docs sandbox-ep10/settings && cp -R sandbox-ep10.base/docs sandbox-ep10.base/settings sandbox-ep10/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep10 ./sb.sh launch sandbox-ep10 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
