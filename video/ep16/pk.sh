#!/bin/zsh
# 점검 한 장: LG 창 → qa/peek.png(원본) · qa/peek-s.png(1600 폭, 좌표 ×2.4, 캡처 y 는 +60)
cd "${0:a:h}"; ./peek.sh qa/peek.png && sips -Z 1600 qa/peek.png --out qa/peek-s.png >/dev/null
