#!/bin/zsh
# 11편 데모 Finder 창 "Prize Night music" 을 LG 의 카드 아래 빈자리에 띄운다(사이드바·툴바 숨김, 아이콘 자리 고정).
# 다른 Finder 창은 접는다 — 끌어 놓는 자리에 다른 Finder 창이 있으면 파일이 그리로 옮겨진다(5편 교훈).
cd "${0:a:h}"
D="$PWD/media/Prize Night music"
osascript <<AS
tell application "Finder"
  repeat with w in (every Finder window whose name is not "Prize Night music")
    try
      set collapsed of w to true
    end try
  end repeat
  if not (exists (first Finder window whose name is "Prize Night music")) then open (POSIX file "$D" as alias)
  set w to (first Finder window whose name is "Prize Night music")
  set current view of w to icon view
  set toolbar visible of w to false
  set sidebar width of w to 0
  set statusbar visible of w to false
  set bounds of w to {${FB:-2450, -430, 3090, -150}}
  set icon size of icon view options of w to 96
  set arrangement of icon view options of w to not arranged
  set position of item "open-doors.mp3" of w to {90, 80}
  set position of item "lobby-light.mp3" of w to {230, 80}
  set position of item "walk-up.mp3" of w to {370, 80}
  set position of item "interval.mp3" of w to {530, 80}
  select {}
  set index of w to 1
end tell
AS
