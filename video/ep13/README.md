# Episode 13 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep13.wav`(`music_full.py`, 타이틀·엔드 카드만) · 앱 소리 `rec/v2/sN.wav` · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep13.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 13` → `youtube/ep13/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep13/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep13/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1380(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 13편 메모(2026-11-01)
- 흐름: 10편에서 꾸민 Day 1(sandbox-ep10 의 것을 base 로) → Link 로 1편 영상(사용자 채널, youtu.be/55dioOOzick) 넣기 → 스트리밍 송출 → Slide settings 챕터 눈금 → 자막 Korean · Manage languages 로 Japanese 등록 → 일본어 → Settings › Files & YouTube 자막 위치 Top · 크기 160% → 무대 비우고 Download(이 맥에서 4 초) → Downloaded · YouTube ↓ · Scale 넷 → Settings › Tools › YouTube tool Check(2026.10.26 있음, Update 는 누르지 않는다).
- 출력 창이 없는 가상 화면이라 "YouTube is playing on the output screen" 덮개 · Quality · Bring to preview 는 못 찍는다(계획에서 뺐다). 에디터 글자 막힘도 시간상 뺐다.
- 자막 메뉴 줄 자리: Japanese 등록 전엔 넷째 줄(y 542)이 Manage languages, 등록 뒤엔 Japanese — 첫 판은 607 을 눌러 망가졌다(rec/v2/bad).
- **s2 의 YouTube 소리가 녹음되지 않았다**(appaudio 를 켠 뒤에 재생이 시작되면 WebEngine 소리를 못 잡는 듯). 1편 원본 소리(media/ep01-audio.wav)를 s3 녹음과 상관으로 맞춘 자리에 채운다(qa/s2fill.json, 상관 0.994, −3 dB). 다음에 스트리밍을 찍을 땐 녹음 전에 한 번 재생해 둘 것.
- 본편 앱 소리는 내레이션 아래 −20 dB(1편 내레이션과 겹친다). 앱 소리가 없는 s1 · s6 에는 배경음악을 낮게.
- rec_t0 1.0.
