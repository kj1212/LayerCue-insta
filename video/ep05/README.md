# Episode 5 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep05.wav`(`music_full.py`, GarageBand 루프 pop) · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep05.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 5` → `youtube/ep05/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep05/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep05/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1080(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 5편 메모
- 시작 상태: `ep05/reset.sh`(sandbox-ep05.base 복원 + 데모 Finder 창 "Summit media" 를 앞에, 아이콘 자리 고정 · 선택 비움). 다른 Finder 창은 접는다.
- Finder 에서 끌 때마다 `finder`(앞으로) → `fclear`(선택 비움) → `drag`. 남은 선택이 있으면 여러 파일이 함께 끌린다. 끌어 놓은 뒤에는 LayerCue 가 앞으로 와 Finder 가 가려진다.
- 카드 고르기는 ⌘클릭(`cmdclick`: ⌘ 키를 실제로 눌렀다 뗀다). 이름 줄을 연달아 누르면 더블클릭으로 편집 화면이 열린다.
- Delete 키는 ⌘클릭으로 고른 뒤 0.8 s 이상 지나서 누른다(바로 누르면 먹지 않았다).
- 촬영 빌드: 0.9.12 + LayerCue 930199d(카드 영상 길이 바로 · ⌘Z 뒤 썸네일 되돌림)를 덧대 다시 지었다(2026-10-31).
- ⌘ 는 수식키 바뀜(FlagsChanged)으로 눌렀다 뗀다(mouse._cmd). 키 이벤트로 보내면 앱에 ⌘ 가 눌린 채 남아, 그 뒤 클릭이 송출 대신 선택만 되고 Delete 가 안 먹었다.
- 데모 창 말고 다른 Finder 창이 있으면 그 폴더로 파일이 옮겨진다 → record_all2.sh 가 clear_finder.sh 로 치운다(최소화).
