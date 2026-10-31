# Episode 7 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep07.wav`(`music_full.py`, GarageBand 루프 pop) · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep07.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 7` → `youtube/ep07/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep07/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep07/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1080(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 7편 메모
- 다시 LG(4K)에서 녹화한다(1·2편과 같은 꼴, sb.sh place). 3–6편은 맥북에서 찍어 늘렸다.
- In point 를 찍으면 버튼 줄이 바뀐다: In(0:02) · Out · ✕(Clear) — Out 은 In 이 있던 자리(3026,723), 맨 오른쪽은 지우기 ✕.
- Scale 을 바꿔도 이미 나간 무대는 그대로 — 바뀐 모습은 Slide settings 미리보기에 보인다.
- 덕킹 덜 민감(2.5 s 보다 짧은 쉼은 낮춘 채)이 처음 들어간 편.
- 촬영 빌드에 2599bc4(그림 장 썸네일 = 자르기·채우기 그대로) 덧댐. 크롭 시트의 Anchor/Scale 칸은 peek(창 px)+60 이 클릭 좌표다.
- 음악 다시: Road Trip Summer + Duncan(처음 판 브라스 펑크는 이상하다는 말).
