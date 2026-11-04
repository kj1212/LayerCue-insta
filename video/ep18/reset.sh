#!/bin/zsh
# 18편 촬영 시작 상태 — sandbox-ep18.base: Prize Night 2026(3번 영상 파일 이름이 바뀌어 File missing) · School Song ·
# Screen 1 Audience(가상 화면) + Screen 2 Stage(BetterDisplay 「Stage Monitor」, B 끔) — 둘 다 전원 켬 · 편집 잠금 끔 · 오버레이 이름 없음
cd "${0:a:h}/.." || exit 1
./sb.sh quit >/dev/null; sleep 2
betterdisplaycli set -name="Stage Monitor" -connected=on >/dev/null 2>&1; sleep 2
rm -rf sandbox-ep18/docs sandbox-ep18/settings && cp -R sandbox-ep18.base/docs sandbox-ep18.base/settings sandbox-ep18/
LC_APP_ARGS="-AppleLanguages (en)" LC_SANDBOX=sandbox-ep18 ./sb.sh launch sandbox-ep18 >/dev/null; sleep 9
# 켤 때 무대 모니터 송출 창이 먼저 떠서 sb.sh place 가 그 창을 LG 로 옮겼다(검은 화면) — 끄고 앉힌 뒤 다시 켠다
LC_SANDBOX=sandbox-ep18 python3 lc.py run_commands '{"commands":[{"op":"output","on":false}]}' >/dev/null; sleep 2
./sb.sh place >/dev/null; sleep 1
LC_SANDBOX=sandbox-ep18 python3 lc.py run_commands '{"commands":[{"op":"output","on":true}]}' >/dev/null; sleep 3
echo reset
