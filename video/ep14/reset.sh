#!/bin/zsh
# 14편 촬영 시작 상태로 되돌린다 — 앱을 끄고 sandbox-ep14.base(13편 시작과 같음: Summit 2026 › Day 1 꾸민 판)를 다시 깔고 켠다
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep14/docs sandbox-ep14/settings && cp -R sandbox-ep14.base/docs sandbox-ep14.base/settings sandbox-ep14/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep14 ./sb.sh launch sandbox-ep14 >/dev/null; sleep 9; ./sb.sh place >/dev/null
ep14/finder.sh >/dev/null 2>&1      # 14편: 데모 Finder 창(Speaker files) — 녹화의 "front" 가 LayerCue 를 다시 앞으로
echo reset
