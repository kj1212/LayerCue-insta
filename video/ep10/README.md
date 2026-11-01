# Episode 10 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep10.wav`(`music_full.py`, GarageBand 루프 pop) · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep10.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 10` → `youtube/ep10/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep10/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep10/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1080(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 10편 메모(2판, 2026-11-01 다시 만듦)
- 흐름: 밋밋한 타이틀 1장(Summit 2026 › Day 1)을 꾸민다 — 이름 옆 우클릭 → Insert icon(마이크) → Text color 주황 · 사각형 → "DAY 1" → Change shape 쉐브론 · 띠(Linear, 오른쪽 No fill) → 우클릭 Order › To back · 로고 붙여 넣기(media/rts-logo.png, 가상) → Duplicate slide 로 다음 연사 → 제목 Copy style → Show 모드에서 3–6장 고르고 Paste style.
- 1판은 별·아이콘을 넣었다 지우고, 띠(도형)에 Copy style 을 써서 다른 장에 안 넘어간 채 끝났다. **Copy style 은 텍스트 상자만**(매뉴얼 slides/text.md) — 도형·그림은 따라가지 않는다고 말한다.
- 시작 상태는 sandbox-ep10.base(plan/day1.html 을 set_slides_html 로 넣고 이름을 Day 1 로). Finder 없음.
- Show 모드 카드는 **이름표**를 눌러 고른다(그림을 누르면 송출된다). 끝 장은 Shift-클릭(mouse.shift_click).
- 우클릭 Order 하위 메뉴는 Order 위에 머물렀다가 옆으로 옮겨 가서 누른다(바로 가면 메뉴가 닫힌다).
- 이 날 녹화는 rec_t0 0.9(1.4 이면 화면 동작이 0.5 초 일찍 나왔다) — 녹화 뒤 한 번 재고 맞춘다.
