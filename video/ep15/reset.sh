#!/bin/zsh
# 15편 촬영 시작 상태 — sandbox-ep15.base(Day 1 꾸민 판 + 바깥 USB 폴더의 sponsor-reel 영상 한 장)
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep15/docs sandbox-ep15/settings && cp -R sandbox-ep15.base/docs sandbox-ep15.base/settings sandbox-ep15/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep15 ./sb.sh launch sandbox-ep15 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
