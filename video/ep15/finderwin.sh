#!/bin/zsh
# 15편: Open 으로 열린 LayerCue 폴더 Finder 창을 LG 의 앱 위로(사이드바 · 도구 막대 숨김, 목록 보기)
osascript <<'AS'
tell application "Finder"
  set w to front Finder window
  set toolbar visible of w to false
  set sidebar width of w to 0
  set statusbar visible of w to false
  set current view of w to icon view
  set icon size of icon view options of w to 96
  set arrangement of icon view options of w to arranged by name
  set bounds of w to {2160, -720, 3060, -260}
  activate
end tell
AS
