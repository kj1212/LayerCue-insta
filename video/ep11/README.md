# Episode 11 — 제작 폴더

| 무엇 | 어디 |
|---|---|
| 대본(영어, 줄 단위) | `script.json` · 번역 `i18n/ko.json` `i18n/ja.json` |
| 연출(줌·테·이름표·자막·녹화 동작) | `shotlist2.json` · 영역 좌표 `regions.json`(OCR 로 잼: `ocr.py`) |
| 디자인 | `brand.css`(앱·홈페이지 값) · `title-anim.html` · `end-anim.html` · `parts.html` · `bg.html` · `design.html`(보드·썸네일) |
| 목소리 | `audio/vo-heart/`(Kokoro af_heart 0.95, `voice.py`) |
| 음악 | `audio/music-ep11.wav`(`music_full.py`, 타이틀·엔드 카드만) · 앱 소리 `rec/v2/sN.wav` · 최종 믹스 `final_mix.py` |
| 녹화 | `rec/v2/*.mp4`(ffmpeg 30 fps, `record_all2.sh` · 무대 `record_stage.sh`) |
| AE | `ae/ep11.aep`(엔진 `build_v2.jsx`, 타임라인 `timeline2.js` 는 `assemble2.py timeline` 이 만든다) |
| 렌더 | `render/ae-out.mp4`(AE) → `render/final.mp4`(최종 믹스를 붙인 것) |
| 업로드 묶음 | `python3 ../package.py 11` → `youtube/ep11/` |

## 고치기
- 대사 한 줄: `script.json` 수정 → `VO_DIR=vo-heart TTS_ARGS="--model mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.95" python ep11/voice.py gen` → `assemble2.py times/takes/timeline` → AE 빌드 → 렌더
- 테·이름표·자막 위치/글: `shotlist2.json` → `assemble2.py timeline` → `ae.sh ep11/build_v2` → `aerender`
- 음악 크기만: `final_mix.py <본편dB> <앞뒤dB> <말할때dB>` → ffmpeg 로 `render/ae-out.mp4` 에 다시 붙이기(재렌더 불필요)
- 녹화 다시: LG 를 1920×1180(HiDPI)로, `record_all2.sh s3 s5`(구간만) · 무대 `record_stage.sh`

## 11편 메모(2026-11-01)
- 흐름: Prize Night 2026(7장: 제목 · 입장 안내 · 교장 환영 영상 · 발표 · 팡파르 사운드 슬라이드 · 수상자 · 휴식)과 빈 음악 목록에서 시작 → Finder 창(media/Prize Night music)에서 3곡 끌어 넣기 → 재생 · 슬라이드 보내기 · CLEAR · Stop → 폴더 이름 Walk-in · 새 폴더 Break · Interval 넣기 → 끝 동작 Play next ×3 · 끝 근처로 건너뛰어 첫 곡으로 · Interval Repeat one → Open Doors 의 말소리 인트로를 In/Out 으로 자르기 → Settings › Stage › Music while video plays: Lower · 환영 영상 아래로 음악 낮춤 · CLEAR 로 복귀 → 팡파르 · 수상자 · Interval.
- 시작 상태: `reset.sh`(sandbox-ep11.base) + `finder.sh`(데모 Finder 창). 연출표는 `plan/make_shot.py` 가 shotlist2.json · regions.json 을 만든다.
- **앱 소리**: `../tools/appaudio`(ScreenCaptureKit, LayerCue 소리만, `swiftc -O tools/appaudio.swift -o tools/appaudio`). `REC_AUDIO=1` 이면 record.py 가 구간마다 rec/v2/sN.wav · sN.audio.json(offset) 을 남긴다. final_mix.py 가 타임라인 seg.start − PRE + offset + a 에 놓고 내레이션 아래서만 −13 dB. 본편 배경음악은 끈다.
- 데모 곡: `media/make_tracks.py`(Apple Loops, 가상 제목 · ID3 title) · Open Doors 앞 말소리는 Kokoro am_michael · 환영 영상 `media/welcome-message.mp4`(bf_emma) · 팡파르 `award-fanfare.wav`.
- Finder 끌기: 고무줄 선택(drag) 뒤에 slowdrag 해야 끌린다 — 아이콘을 클릭한 뒤 끌면 안 끌렸다.
- **앱 버그로 보이는 것**: 사운드 슬라이드가 그 전에 나오던 곡의 끝 동작을 물려받는다(Repeat one 곡 위에서 쏘면 팡파르가 반복, Play next 곡 위에서 쏘면 끝난 뒤 열린 폴더 첫 곡이 다시 나온다). 그래서 s6 시작 전에 Walk-in 을 닫아 둔다(열린 폴더가 없으면 멈춘다). 폴더 합계 길이는 범위를 바꿔도 폴더를 다시 열 때까지 그대로였다(5:55 → 5:41).
- rec_t0 0.95(이 날 다시 잼).
