#!/bin/zsh
# 17편 촬영 시작 상태 — sandbox-ep17.base(16편 시작판: School Song · Screen 1 = Audience 가상 화면, 다른 화면 없음)
# NDI 받는 쪽 이름은 STAGE-MAC(sandbox-ep17/ndi) · OBS 는 장면 「Stream」(Camera = 무대 사진, LayerCue (NDI) 이름 비움, Syphon 숨김)
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep17/docs sandbox-ep17/settings && cp -R sandbox-ep17.base/docs sandbox-ep17.base/settings sandbox-ep17/
pgrep -f "OBS.app/Contents/MacOS/OBS" >/dev/null || { open -a OBS; sleep 10; }
.venv/bin/python ep17/obs_ctl.py reset; .venv/bin/python ep17/obs_ctl.py place
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep17 ./sb.sh launch sandbox-ep17 >/dev/null; sleep 9; ./sb.sh place >/dev/null
echo reset
