# 편마다 숏츠(본편 4K 녹화를 잘라서)

1편 숏츠(short03)의 틀을 일반화했다. 한 편 ≈ 28 s 1080×1920.

| 단계 | 명령 |
|---|---|
| 장면 후보 | `python3 shorts/beats.py 05` — 본편 하이라이트(hl) 사건의 녹화 파일 · 녹화 안 시각 · 창 영역 |
| 대본 | `shorts/specs.py`(훅 2줄 · 박자 넷 = beats 번호 · 낱말 · 작은 말 · 목소리 · 끝 카드 세 낱말) · 번역 `shorts/i18n.py` |
| 재료 | `~/Documents/AIvoice/.venv/bin/python shorts/make.py [05 …]` → 목소리 · cfg.js · parts.html · 음악 · spec.json |
| 글판 | `node shorts/parts.mjs shorts/<id> …`(글꼴을 먼저 불러온 뒤 넘치면 줄인다) |
| 끝 카드 | `node render.mjs end 30 'dur=4.4&tags=A.,B.,C.&beta=0' end-<id>` — 베타 · 버전 숫자는 영상에 넣지 않는다. 세 낱말이 18 글자를 넘으면 저절로 줄인다 |
| AE | `shorts/render_all.sh [shorts/<id>/ …]` → `shorts/<id>/out/<id>.mp4`(loudnorm −14) |
| 묶음 | `python3 shorts/package_shorts.py [id …]` → 표지 · 자막 en/ko/ja · 업로드 글 → OneDrive `shorts/shortNN-…` |

화면: 위 낱말 · 가운데 위 창 전체(미니맵)와 구역 테 · 가운데 아래 확대 칸(박자 경계에서 컷, 박자 안 4 % 다가감) · 아래 자막 · 다시 보기(네 테) · 끝 카드.
11 · 12편은 앱 소리(rec/v2/sN.wav)를 낮게 깐다. 13편은 앱 소리가 1편 내레이션이라 빼고, 14편은 앱 소리가 없다.
상태 막대 기기 이름은 `shorts/patch_status.py` 로 녹화에서 미리 영어로 바꿨다(11 · 13 · 14편, 2026-11-02 — 12편은 ep12/patch).
