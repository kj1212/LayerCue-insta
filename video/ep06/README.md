# Episode 6 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep06.wav`(`music_full.py`, GarageBand 루프 pop) · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep06.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 6` → `youtube/ep06/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep06/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep06/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1080(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 6편 메모
- 시작 상태: `ep06/reset.sh`(sandbox-ep06.base: Prize Night 2026 = 배경 영상 · 글 4장 · 띠(아래 1/5, HTML) · 교표 · 스폰서 로고, 카드 2줄). 녹화는 s1→s8 한 번에(무대 상태가 이어진다).
- 칩: 클릭 = FG↔BG, 길게(1 s) = 오버레이 1, 오버레이에서 클릭 = 다음 번호. 녹화 도구 `hold` · `optkey`(⌥+화살표).
- 로고는 1920×1080 투명 PNG(오른쪽 위 같은 자리) — 오버레이 1 에서 바뀌는 게 보인다.
