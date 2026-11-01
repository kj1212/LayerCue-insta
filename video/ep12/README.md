# Episode 12 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep12.wav`(`music_full.py`, 타이틀·엔드 카드만) · 앱 소리 `rec/v2/sN.wav` · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep12.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 12` → `youtube/ep12/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep12/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep12/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1280(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 12편 메모(2026-11-01)
- 흐름: 11편 끝 상태(Prize Night · 음악 목록)에서 시작. 오디오 장치는 없는 장치(ini 의 audioOutputId)라 Not connected · 주황 스피커 → System default 로. 미터 읽기 · 마스터 +3 dB → 더블클릭 0 dB · MUTE(흐리게 계속 움직임) vs 마스터 −∞ · 무음 점검 두 사례: ① 음악 목록 아래 스피커가 꺼져 있다(미터는 움직임, 녹화 setup 에서 끔) ② 환영 영상의 Slide settings 볼륨이 0%(base 에 저장) → 100% 로 올리고 컨트롤 줄 ▶ 로 다시 · SOLO(왼쪽 = 전체, 오른쪽 = 앞 층).
- 장치를 이름으로 고르는 장면은 찍지 않았다 — 고르면 LayerCue 가 맥의 기본 출력도 바꾼다(사용자 컴퓨터). 목록만 보여 준다(기기 이름은 macOS 언어라 "MacBook Pro 스피커").
- 사운드 슬라이드 팡파르는 쓰지 않았다(11편의 끝 동작 물려받기 버그). 마스터 +3 dB 에서 Lobby Light 는 빨강까지 차지만 맨 위 클립 선은 잘 보이지 않아 자막으로 설명.
- 마스터를 −∞ 까지: (1284,305) → (1284,624). 598 이면 −54 dB 에서 멈추고, 더 내리면 MUTE 위에서 놓아 MUTE 가 눌린다.
- s3 · s6 은 다시 찍었다(`RESHOOT=1 python3 ep12/plan/make_shot.py` 가 앞 구간 끝 상태를 setup 으로 만든다). 첫 판은 rec/v2/first/.
- 본편 배경음악은 앱 소리가 없는 s1 에만 낮게(−12 dB).
- rec_t0 1.0.
