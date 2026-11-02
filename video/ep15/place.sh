#!/bin/zsh
# 3편: 촬영용 LayerCue 창을 맥북 화면(주 화면) 의 녹화 자리에 — 60,110 에 1680×919 pt(= 3360×1838 px, 3840×2100 으로 늘리면 2편과 같은 꼴)
osascript -l JavaScript -e 'var w=Application("System Events").processes.byName("LayerCue").windows[0]; w.position=[60,110]; w.size=[1680,919]; JSON.stringify([w.position(),w.size()])'
