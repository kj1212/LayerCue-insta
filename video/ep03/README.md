# Episode 3 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep03.wav`(`music_full.py`, GarageBand 루프 pop) · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep03.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 3` → `youtube/ep03/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep03/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep03/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1080(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 3편만의 것 — 두 화면
- 조작 창은 **맥북(주 화면)** 에서 녹화: 창 자리 `place.sh`(60,110 · 1680×919 pt), 녹화본은 `REC_CROP` 으로 잘라 3840×2100(+위 60)으로 늘린다 → 2편과 같은 연출표·영역표 꼴. 마우스는 `MOUSE_WIN` 으로 창 기준 좌표.
- **LG 는 프로젝터.** 출력을 켜면 macOS 가 LG 해상도를 1:1 로 바꾸는데, 그 순간 LG 실시간 녹화가 끊긴다(두 화면 동시 녹화도 멈춘다). 그래서 실제 송출을 한 장씩 찍은 `proj/*.png` 를 연출표의 `proj` 이벤트(클릭 + 0.9 s)에 맞춰 바꿔 보여 준다. `split` = 조작 창·프로젝터 나란히.
- 출력이 꺼진 동안 LG 에는 바탕화면(개인 창)이 보이므로 `proj/off.png`(OUTPUT OFF 그림)로 덮는다. 송출 사진 오른쪽 위의 보라 점(녹화 표시)은 지웠다.
- 주의: 출력을 끄면 LG 해상도가 돌아오며 LayerCue 가 "케이블을 새로 꽂았다"로 보고 Screen 1 을 LG 로 옮길 수 있다 → 녹화 전에 ini 의 `outputScreenKey=virtual:1920x1080`, `outputName0=` 로 되돌리고 다시 켠다.
- 이름 칸에 커서가 있으면 Esc 는 그 칸 것이라 팝업이 안 닫힌다 → 빈 곳 클릭으로 닫는다. Esc 안내는 선택이 없을 때만 뜬다(두 번 누른다).
