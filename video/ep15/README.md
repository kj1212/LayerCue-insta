# Episode 15 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep15.wav`(`music_full.py`, 타이틀·엔드 카드만) · 앱 소리 `rec/v2/sN.wav` · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep15.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 15` → `youtube/ep15/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep15/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep15/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1580(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 15편 메모(2026-11-02)
- 흐름: Day 1 에 바깥(media/USB Stick) sponsor-reel 한 장 → Settings › Files & YouTube 「1 file(s) live outside」 → Import external files → Tools 를 거쳐 다시 들어오면 「Every file is inside」 → Open → Finder(finderwin.sh: LG 로 옮기고 아이콘 보기 — 목록 보기는 한국어 머리글 · 날짜) · Backups → Reset 창 Cancel → 창 오른쪽 끝을 끌어 좁히기 · Music 따로 창 · 넓히기 → AI apps 화면만(Connect 는 사용자의 Claude Desktop 설정을 바꾸고 앱을 껐다 켜야 해서 누르지 않는다 — 계정 쪽 Account 는 이메일이 보여 안 연다) → 3–5장 Copy as HTML for AI → media/answer.html 을 클립보드로 붙여 넣기(From HTML: updated 3).
- 녹화 도구: record.py `sh` 동작 · 클립보드 LANG=en_US.UTF-8(없으면 · 가 깨졌다).
- 기기 이름 패치: shorts/patch_status.py. rec_t0 1.0.
- 숏츠: shorts/s17-one-folder-ai-help(본편과 같이 만듦).
