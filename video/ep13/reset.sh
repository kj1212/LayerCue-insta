#!/bin/zsh
# 13편 촬영 시작 상태로 되돌린다 — 앱을 끄고 sandbox-ep13.base(Summit 2026 › Day 1 · Prize Night · 음악 목록, 자막 위치 위)를 다시 깔고 켠다
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep13/docs sandbox-ep13/settings && cp -R sandbox-ep13.base/docs sandbox-ep13.base/settings sandbox-ep13/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep13 ./sb.sh launch sandbox-ep13 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
