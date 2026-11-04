#!/bin/zsh
# 16편 촬영 시작 상태 — sandbox-ep16.base(School Song: 배경 영상 위 가사 석 장, 셋째는 일부러 Foreground · Screen 1 = Audience(가상 화면, 전원 켬) · 둘째 화면 없음)
# 무대 모니터는 BetterDisplay 가상 디스플레이 「Stage Monitor」(케이블 뽑기 = betterdisplaycli … -connected=off)
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
betterdisplaycli set -name="Stage Monitor" -connected=on >/dev/null 2>&1
rm -rf sandbox-ep16/docs sandbox-ep16/settings && cp -R sandbox-ep16.base/docs sandbox-ep16.base/settings sandbox-ep16/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep16 ./sb.sh launch sandbox-ep16 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
