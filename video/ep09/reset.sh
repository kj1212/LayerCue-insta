#!/bin/zsh
# 9편 촬영 시작 상태로 되돌린다 — 앱을 끄고 sandbox-ep09.base 를 다시 깔고 켠다(사진은 클립보드로 붙여 넣어 Finder 창은 쓰지 않는다)
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep09/docs sandbox-ep09/settings && cp -R sandbox-ep09.base/docs sandbox-ep09.base/settings sandbox-ep09/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep09 ./sb.sh launch sandbox-ep09 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
