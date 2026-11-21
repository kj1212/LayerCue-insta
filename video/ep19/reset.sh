#!/bin/zsh
# 19편(What's New 0.9.14) 시작 상태 — sandbox-ep19.base: Prize Night 2026 · Sponsor thanks(오버레이 1 · Auto-dismiss 8 s) ·
# Screen 1 Audience = BetterDisplay 「Stage Monitor」(2560×1440 — 따로 찍어 작은 창으로 넣는다), 전원 끔. 녹화 화면 = 가상 「Rec 4K」(1920×1080 HiDPI)
cd "${0:a:h}/.." || exit 1
export LC_BUILD=$HOME/projects/LayerCue/build REC_SCREEN="Rec 4K"
./sb.sh quit >/dev/null; sleep 2
betterdisplaycli set -name="Stage Monitor" -connected=on >/dev/null 2>&1; sleep 2
rm -rf sandbox-ep19/docs sandbox-ep19/settings && cp -R sandbox-ep19.base/docs sandbox-ep19.base/settings sandbox-ep19/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep19 ./sb.sh launch sandbox-ep19 >/dev/null; sleep 10; ./sb.sh place >/dev/null
echo reset
