# 숏츠 03 — Pick. Click. Watch. Adjust. (본편 1편에서)

본편마다 숏츠 하나 — 핵심 한 가지 + 장점 한 줄, 29 s 1080×1920. 이 편이 틀(시범).

| 무엇 | 어디 |
|---|---|
| 녹화 | `take/main.json` → `record.py`(LG 4K, 22 s, sandbox-short03 = 13편 base) → `rec/v1/main.mp4` · 기기 이름 영어 패치 `main-en.mp4`(ep12/patch/status.png) |
| 목소리 | `lines.json` → Kokoro af_heart 0.97 → `audio/01–06.wav` |
| 음악 | `music.py`(Electric Funk + Duncan, ep11/media/make_tracks.song) |
| 글판 | `parts.html` → `node parts.mjs <id…>`(판 하나씩 — 모두 보이게 두고 찍으면 겹친다) |
| 끝 카드 | `node render.mjs end 30 'dur=4.4&tags=PICK.,CLICK.,LIVE.' end-s03` |
| AE | `RENDER_NOW=1 OUT_NAME=short03 ./ae.sh short03/build` → render/short03.mp4 → `out/` 로 옮기고 loudnorm −14 |

짜임: 훅(창 전체 + 큰 글) 0–3.5 → 박자 넷(위 낱말 · 가운데 위 미니맵에 구역 테 · 아래 확대 칸 · 자막) 3.6–20.6 → 다시 보기(네 테) → 끝 카드 24.8–29.2.
녹화 시계 = 컴프 시각(녹화 0 초가 −1.0 s).
