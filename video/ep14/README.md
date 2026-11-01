# Episode 14 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep14.wav`(`music_full.py`, 타이틀·엔드 카드만) · 앱 소리 `rec/v2/sN.wav` · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep14.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 14` → `youtube/ep14/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep14/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep14/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1480(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 14편 메모(2026-11-01)
- 흐름: Summit 2026 › Day 1(꾸민 판) · 데모 Finder 창 "Speaker files"(finder.sh) → New Presentation 의 From PowerPoint/From PDF 보여 주고 Cancel · Add File 가리키기 → Keynote-Okafor.pptx 를 1번 카드에 끌어 놓기(6장, 알림은 자막으로) · BG 칩 → 에디터: 표 칸 하나 고치기 · 글꼴 Default font(Segoe UI 없음) · 숨김(6) · 차트(5) 슬라이드 지우기 → Summit-Programme.pdf 를 마지막 카드에 · Range 2-3 · Import → 우클릭 Export to PDF · Range 1-10 · ⌘⇧G 로 media/export 에 저장.
- 데모 파일: media/make_deck.py(python-pptx, 스크래치 venv) · media/programme.html → pdf.mjs(Chrome PDF).
- 가져오기·내보내기 알림은 1.5 초쯤만 떠서 테두리 대신 자막으로 글을 보여 준다.
- 저장 창 경로와 Exported 알림에 사용자 홈 경로(/Users/…)가 잠깐 보인다.
- 앱 소리 없음 — 본편 전체에 배경음악을 낮게(final_mix 의 if True).
- rec_t0 1.0.
