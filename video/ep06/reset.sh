#!/bin/zsh
# 6편 촬영 시작 상태로 되돌린다 — 앱을 끄고 sandbox-ep06.base 를 다시 깔고 켠 뒤, 데모 Finder 창을 맨 앞에 둔다
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
rm -rf sandbox-ep06/docs sandbox-ep06/settings && cp -R sandbox-ep06.base/docs sandbox-ep06.base/settings sandbox-ep06/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep06 ./sb.sh launch sandbox-ep06 >/dev/null; sleep 9; ep06/place.sh >/dev/null
M="$PWD/ep06/media/Prize media"
osascript -e "tell application \"Finder\"" -e "repeat with w in (every Finder window whose name is not \"Prize media\")" -e "set collapsed of w to true" -e "end repeat" -e "end tell" 2>/dev/null
osascript -e "tell application \"Finder\" to set index of (first Finder window whose name is \"Prize media\") to 1" -e "tell application \"Finder\" to set bounds of (first Finder window whose name is \"Prize media\") to {1080, 640, 1700, 960}"
echo reset
# 아이콘 자리를 고정한다(정렬을 끄고 직접 놓는다) — 이름순 정렬이 켜지면 자리가 바뀌어 다른 파일을 집었다
osascript <<'AS'
tell application "Finder"
  set w to (first Finder window whose name is "Prize media")
  set arrangement of icon view options of w to not arranged
  set position of item "stage-wash.mp4" of w to {70, 60}
  set position of item "school-crest.png" of w to {180, 60}
  set position of item "sponsor-mark.png" of w to {290, 60}
  select {}
end tell
AS
