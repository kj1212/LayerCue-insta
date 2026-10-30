# Episode 4 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep04.wav`(`music_full.py`, GarageBand 루프 pop) · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep04.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 4` → `youtube/ep04/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep04/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep04/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1080(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 4편 메모
- 조작 창은 맥북(3편과 같은 녹화 꼴). 촬영용 자료는 `sandbox-ep04.base/`(시작 상태)에서 되돌린다: 앱을 끄고 docs·settings 를 복사한 뒤 `LC_APP_ARGS="-AppleLanguages (en)"` 로 켠다.
- 녹화 순서 s2 → s7, 마지막에 s1(완성된 사이드바). s1 의 테는 녹화본을 OCR 로 재서 넣었다.
- 찾기(Return)로 결과에 가면 Library 서랍이 크게 올라간다 → s1 준비에서 서랍 버튼(350,570)을 눌러 내린다.
- 우클릭 메뉴는 누른 자리에서 열린다 — 항목 위치는 누른 점 기준(Rename +118 px, Delete +263 px 등).
