#!/bin/zsh
# 데모 창("Summit media 4")이 아닌 Finder 창을 치운다 — 접고, 안 접히면 LG 화면 쪽으로 옮긴다(닫지는 않는다).
# 끌어 놓는 자리에 다른 Finder 창이 있으면 파일이 그 폴더로 옮겨진다(2026-10-31 실제로 youtube/ep01 로 옮겨졌다)
osascript <<'AS'
tell application "Finder"
  repeat with w in (every Finder window whose name is not "Summit media 4")
    try
      set collapsed of w to true
    on error
      try
        set nm to name of w
        tell application "System Events" to tell process "Finder" to set value of attribute "AXMinimized" of window nm to true
      end try
    end try
  end repeat
end tell
AS
