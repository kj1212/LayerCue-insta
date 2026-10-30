#!/bin/zsh
# 촬영용 LayerCue(모래상자) 를 켜고 끄고 LG 화면에 앉힌다.
#   ./sb.sh launch [sandbox-dir]   켠다(기본 sandbox-ep01). 하루 안에 업데이트 확인을 한 것으로 적어 Update 칩이 안 뜨게 한다
#   ./sb.sh place                  LG 화면(1920×1080 HiDPI) 에 창을 꽉 채운다 — 메뉴 막대 아래 1920×1050
#   ./sb.sh quit                   끈다(사람이 쓰는 /Applications 의 LayerCue 는 건드리지 않는다)
set -e
HERE=${0:a:h}
SB=${2:-${LC_SANDBOX:-sandbox-ep01}}
F=$HERE/$SB
APP=${LC_BUILD:-$HOME/projects/LayerCue-film-0912/build}/LayerCue.app/Contents/MacOS/LayerCue      # 촬영용 0.9.12(win-0.9.12 가지를 따로 풀어 지은 것)
case "$1" in
  launch)
    mkdir -p "$F/settings/LayerCueFilm" "$F/docs" "$F/mcp"
    INI=$F/settings/LayerCueFilm/LayerCueFilm.ini
    [ -f "$INI" ] || printf '[General]\nlang=en\n' > "$INI"
    NOW=$(date +%Y-%m-%dT%H:%M:%S)
    if grep -q '^appUpdateLastCheck=' "$INI"; then
      sed -i '' "s|^appUpdateLastCheck=.*|appUpdateLastCheck=$NOW|" "$INI"
    else
      sed -i '' "s|^\[General\]|[General]\nappUpdateLastCheck=$NOW|" "$INI"
    fi
    LAYERCUE_ORG=LayerCueFilm LAYERCUE_SETTINGS_DIR=$F/settings LAYERCUE_DOCS_ROOT=$F/docs \
      LAYERCUE_MCP_DIR=$F/mcp LAYERCUE_MCP_JSON=$F/mcp/mcp-layercue-dev.json \
      nohup "$APP" > "$F/app.log" 2>&1 &
    echo "launched $SB (pid $!)"
    ;;
  place)
    # LG 의 자리를 그때그때 읽는다 — 배치가 바뀐 적이 있다(위 → 오른쪽 위)
    osascript -l JavaScript -e '
      ObjC.import("AppKit"); var s = $.NSScreen.screens; var H = s.objectAtIndex(0).frame.size.height; var lg = null;
      for (var i = 0; i < s.count; i++) { var sc = s.objectAtIndex(i); if (sc.localizedName.js.indexOf("LG") >= 0) lg = sc.frame; }
      var x = lg.origin.x, y = H - (lg.origin.y + lg.size.height);
      var w = Application("System Events").processes.byName("LayerCue").windows[0];
      w.position = [x, y]; w.size = [1920, 1050];     // 메뉴 막대 30 pt 아래로 1050 — 1080 을 주면 아래 30 pt 가 화면 밖으로 나간다
      JSON.stringify({ position: w.position(), size: w.size() })'
    ;;
  quit)
    pkill -f "$APP" && echo quit || echo "not running"
    ;;
  *) echo "usage: sb.sh launch|place|quit"; exit 1;;
esac
