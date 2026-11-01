#!/bin/zsh
# 12편 촬영 시작 상태로 되돌린다 — 앱을 끄고 sandbox-ep12.base(11편 끝 상태: Prize Night · 음악 목록, 오디오 장치는 없는 장치 = Not connected)를 다시 깔고 켠다
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep12/docs sandbox-ep12/settings && cp -R sandbox-ep12.base/docs sandbox-ep12.base/settings sandbox-ep12/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep12 ./sb.sh launch sandbox-ep12 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
