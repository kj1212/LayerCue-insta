# LayerCue from Zero: Run Your First Show — 튜토리얼 시리즈 최종 기획안 (0.9.12 기준)

> 뼈대: 우승안 "BEGINNER JOURNEY"(가르치기 전엔 쓰지 않는다, 매회 실제 화면에서 할 수 있는 일 하나 추가). 심사위원 지적대로 밀도가 높던 3회(구 Ep 7·13·14)를 각각 둘로 나눴고, 길이 검수에서 5분을 넘긴 구 Ep 16(More Screens)을 다시 둘로 나눠 **총 18편**으로 확정했다. 다른 안에서 콜드 오픈·로드맵 카드·Presentation settings 단독 회차·fill & key 실제 시연·Account/Reset·Import bundle·쇼 중 메시지·팩다운 순서·매뉴얼 대조표를 가져왔다. 사실·UI 이름은 모두 매뉴얼 노트 범위 안에서만 쓴다. 매뉴얼 경로는 `/Users/kj1212/projects/layercue-site/src/content/docs/docs/` 기준 상대 경로로 적는다(changelog만 `.../docs/changelog/index.md`).

---

## 1. 시리즈 개요

| 항목 | 내용 |
|---|---|
| 시리즈 제목 (EN) | **LayerCue from Zero: Run Your First Show** |
| 플레이리스트 | 같은 이름 1개(1→18 순서 고정) + 보조 플레이리스트 **"What's New in LayerCue"** |
| 대상 | LayerCue를 처음 켜는 운영자. 컨퍼런스·공연·학교 행사·예배·회의 어디든. 운영 경험 0 전제. |
| 톤 | 차분한 1인칭 시연("I send it. Watch the B cell."). 짧은 문장(15단어 이하)으로만 쓴다 → 한 줄씩 음성 생성. 약 140 wpm, 데모 멈춤을 빼면 **5분 회차 실발화 550–650단어**, 구간당 단어수 ≤ 구간초÷60×140×0.85. |
| 데모 세계관 | 가상 이벤트 3종으로 장소 편향 방지: **Riverside Tech Summit 2026**(컨퍼런스), **Northfield Academy — Prize Night 2026**(학교), **Harbor City Choir — Spring Concert**(합창 공연). 인물 가상: Dana Okafor, Priya Natarajan, Tomás Reyes. 경쟁사·가격 언급 없음. 숨긴 기능(name captions/titles) 언급·노출 없음. |
| 길이 규칙 | 3–5분. 대본 단어수가 상한을 넘으면 녹화 전에 자르거나 분할한다. 5분을 넘긴 편집본은 업로드하지 않는다. |

**에피소드 포맷 규약 (모든 회차 공통)**

1. **0:00 콜드 오픈(5–10초)**: 그 회차의 결과가 4K 무대 출력에 떠 있는 장면 → 타이틀 카드 `Episode N — <Title>` → 한 문장 목표 `By the end you will …`.
2. **본문 6–8구간**. 구간 시작 시각 = YouTube 챕터. 챕터 이름은 명사구(on-screen 요약 축약).
3. Mac 키·경로를 말하는 순간 **Windows 대응 자막**(Cmd/Ctrl, Option/Alt, Finder/File Explorer, Trash/Recycle Bin). 녹화는 macOS 영문 UI 1벌, Windows는 Ep 2 설치 B-roll만.
4. 안전 규칙은 **한 번만** 가르치고 이후엔 한 문장으로 상기한다(예: "Lock editing does not cover the sidebar or Presentation settings"는 Lock editing을 가르치는 Ep 6에서 가르치고 Ep 18 체크리스트에서만 상기).
5. **엔드 카드는 독립 구간**: 5:00 회차는 4:45–5:00, 4:30 회차는 4:15–4:30, 3:30 회차는 3:15–3:30. 이 구간엔 **새 조작·새 사실 없음**. 발화는 `You can now <one real thing>.` + `Next: Episode N+1 — <Title>` 두 문장만. 화면은 시리즈 로드맵 카드(18편 + "What's New" 슬롯, 현재 회차 하이라이트). 그 앞 구간에는 "Next:"를 넣지 않는다.
6. **설명란 고정 문구**: `Lost? Start with Episode 1.` / `Recorded on LayerCue 0.9.12.` / `No account is needed to run a show; Settings needs a one-time Google sign-in.` + 목표·선수 회차·챕터·참조 매뉴얼 공개 URL(`/docs/start/…` 형태).
7. 고정 자막 스타일: 하단 로어서드(인디고 바), 키 표기는 `⌘1 · Ctrl+1` 형태.

---

## 2. 전체 편성표

| # | Title (EN) | 분 | 목표 (KO) | 선수 회차 |
|---|---|---|---|---|
| 1 | Meet LayerCue: The Main Window | 5.0 | 메인 창 4영역의 이름·역할, 7개 레이어 개념(스크립트 데모) | 없음 |
| 2 | Install, First Launch and Settings | 5.0 | Mac/Windows 설치, 첫 실행 구성물, 1회 로그인, General/Tools, 안전한 종료 | 1 |
| 3 | Your First Show: Screen On, Slide Out, Clear | 5.0 | 화면 선택→전원 ON→슬라이드 송출→CLEAR/키→안전 종료. Esc·화면 덮임 대응 | 1–2 |
| 4 | Libraries, Presentations and Cue Sheets | 5.0 | 라이브러리/프레젠테이션/큐시트 생성·순서·이름·삭제·undo·Find | 1–3 |
| 5 | Adding Slides and Reading Cards | 5.0 | 파일/붙여넣기로 슬라이드 추가, 카드 읽기, 교체 함정, 복사/이동/삭제, File missing | 1–4 |
| 6 | Running the Slide List: Send, Select, Keys and Layers | 5.0 | 키보드 운용, 선택 vs 송출, 레이어 칩, 오버레이 규칙, 오렌지 표시 추적, 컨트롤 로우, Lock editing | 1–5 |
| 7 | Slide Settings: Fit, Trim, Loop and Volume | 4.5 | 송출 전 슬라이드 보정(저장되는 값) vs 무대 컨트롤(임시) | 1–6 |
| 8 | Presentation Settings: Fades, Auto-dismiss and Layer for This List | 3.5 | 프레젠테이션 단위 4값, 기본값 따름 vs 자기 값 | 1–7 |
| 9 | Text Slides in the Editor | 5.0 | 에디터 열기, 텍스트 박스·폰트·외곽선·맞춤·배경·분할/병합·라이브 전송 | 1–6 (7 권장) |
| 10 | Designing Slides: Shapes, Pictures, Styles | 5.0 | 타이틀 슬라이드·로어서드 제작, 정렬·순서·스타일 일괄 적용 | 9 |
| 11 | Music: Your Own Channel | 4.5 | 프리쇼/휴식 재생목록, 트랙 설정, 종료 동작, 영상 아래 덕킹, 사운드 슬라이드 | 3, 6 |
| 12 | Sound: Device, Meter, Master and the No-Sound Checklist | 4.5 | 장치 선택, 미터/마스터, MUTE/SOLO, 저장되는 볼륨 6곳, 무음 점검 | 6, 7, 11 |
| 13 | YouTube Slides: Streaming, Downloading, Captions | 5.0 | 링크 추가, 다운로드, 무대 커버/품질, 자막·더빙·챕터, yt-dlp 갱신 | 5, 7, 9, 12 |
| 14 | Bringing It In: PowerPoint, PDF and Export | 4.5 | PPTX 편집 가능 가져오기와 한계, PDF 그림 가져오기, PDF 내보내기 | 4, 5, 9, 10 |
| 15 | Your Files, Settings Pages and AI Helpers | 5.0 | 미디어 폴더·Import external files·백업/이동·Import bundle·Account/Reset·창 접힘·AI 연결/Copy as HTML | 2, 14 |
| 16 | More Screens: Stage Output Window and Layers Shown | 4.5 | 두 번째 화면(가사만), 가상 화면, 온에어 목록·Layout board, 분리/재연결 | 3, 6, 8 |
| 17 | Streaming Out: NDI, Syphon and Fill & Key (Advanced) | 5.0 | NDI/Syphon로 무대를 보내고, 스위처용 fill & key를 만든다 | 16 |
| 18 | Show Day: Defaults, Lock, Messages and the Checklist | 4.5 | 전날 점검, Lock editing while live, 기본값 사전 설정, 쇼 중 메시지, 6항목 체크리스트, 팩다운 | 전부(특히 3, 12, 13) |

합계 약 85분. 레이어·송출 안전(Ep 3)이 모든 제작 회차(Ep 4–10)보다 앞선다.

---

## 3. 편별 상세

표기: **구간표** 열 = 시각 | 화면 | 내레이션 비트(EN, 실제 발화의 핵심 문장; 비트 문장도 20단어 상한, 최종 대본은 이 비트를 15단어 이하 문장으로 풀어 쓴다) | 매뉴얼 참조. 마지막 행은 항상 엔드 카드(규약 5).

### Ep 1 — Meet LayerCue: The Main Window (5:00)

- **목표**: 메인 창 4영역의 이름과 역할을 말할 수 있고, "무대는 7개 레이어"라는 개념을 본다.
- **끝나면 할 수 있는 것**: 창의 어느 부분이 무엇인지 가리킬 수 있다. (아직 아무것도 송출하지 않는다.)
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 4K 무대에 루프 영상 + "Riverside Tech Summit 2026 — Welcome" + 좌상단 로고. 메인 창(영문 UI, Tour 큐시트·READ ME·My Stuff)으로 컷. 타이틀. | This is LayerCue. It sends a presentation to a screen, in layers. A video runs underneath. Words sit on top. A logo stays in a corner. Each one comes and goes on its own. Today we only look. Nothing goes on air yet. | `index.md`; `start/tour.md` |
| 0:35 | 네 영역 순서대로 하이라이트. 자막 "Pick on the left. Click in the middle. Watch the top. Adjust on the right." | The window has four areas. Pick on the left. Click in the middle. Watch the top. Adjust on the right. Remember that line. Every later episode hangs on it. | `start/tour.md` (Main window layout) |
| 1:05 | 사이드바 확대: Cue Sheets(Tour), Library drawer(READ ME, My Stuff). 더블 애로우로 드로어 올리고 내림. | Cue Sheets sit on top. A cue sheet is the running order for one event. The Library drawer is below. A library is a folder of presentations. A presentation is one set of slides. The number is the slide count. Press the double arrow to raise the drawer. Pointing at it does nothing. | `start/tour.md` (Sidebar); `start/install.md` (first time) |
| 1:45 | Tour 클릭 → 가운데에 5개 가이드. 타이틀 바 버튼 5개 툴팁: Add File, Link, Edit, Layer for this list, Presentation settings. 카드 설명(사진은 건드리지 않음). | Click a cue sheet and the middle shows every presentation in it. Each has a title bar with five buttons. Add File. Link. Edit. Layer for this list. Presentation settings. Under it are the slide cards. A click on a card's picture is a send. We do not click yet. That is Episode 3. | `start/tour.md` (Middle: title bar buttons) |
| 2:30 | 상단 밴드 확대: 모니터 타일(01 탭, 전원 스위치, 프리뷰, Layers shown 셀, 레이어 컬럼 CLEAR/1–5/F/B, 컨트롤 로우) → 미터 → Music → Slide settings. | The top band is where you watch. The tile is Screen 1. The power switch at the right end opens the output. Beside the preview is the layer column. CLEAR on top. Five overlays. F for foreground. B for background. Then the sound meter. Then Music, on its own channel. At the right end, Slide settings. That is where you adjust one slide before it goes out. | `start/tour.md`; `output/index.md` (The stage tile) |
| 3:20 | 상태 바 좌→우: Show/Edit, On air 칩 "No output", 스피커 박스, 무대 제목 점, Tell us what's wrong, 카드 크기 슬라이더, 연필(Lock editing), (빈 자리: Update 칩 위치), 렌치, 기어. | The status bar reads left to right. Show and Edit. The on-air chip counts live screens. The speaker box is your sound device. The dot and title say what is on stage. Tell us what's wrong. The slider sets card size. The pencil locks editing. When an update is waiting, an Update chip appears here. The wrench is the YouTube tool. The gear is Settings. | `start/tour.md` (Status bar) |
| 3:50 | 자막 "Scripted demo on a virtual screen — no projector is live." 영상→B(앰버), 텍스트→F(인디고), 로고→overlay 1(그린). 텍스트 슬라이드 3장 교체, 영상 멈추지 않음. ×(F)로 글자만 내림. | This part is a scripted demo on a virtual screen. Do not copy it on a live projector yet. A video goes to the background. The B cell turns amber. Words go on top. F turns indigo. A logo goes to overlay one. Green. I change the words. The video never stops. The small x beside F takes only the words down. That is the whole point of layers. | `index.md` (layers); `output/layers.md` (The seven layers) |
| 4:25 | Edit 누름 → 에디터. Show로 복귀. | Press Edit and the whole window becomes the slide editor. Press Show to come back. That is the main window. | `start/tour.md` (Edit) |
| 4:45 | 엔드 카드 + 로드맵 카드(1 하이라이트). 자막(내레이션 없음) "Not installed yet? Episode 2 walks you through it, on Mac and Windows." — 설치 없이 보는 편이라 따라 하려는 시청자를 2편으로 보내는 한 줄. 발화는 규약대로 두 문장만. | You can now point at every part of the window. Next: Episode 2 — Install, First Launch and Settings. | — |

- **데모 자료**: 라이브러리 "Summit 2026": `Welcome loop`(추상 루프 mp4, BG), `Welcome words`(텍스트 3장: Welcome / Doors open 9:00 / Keynote: Dana Okafor, 9:30), `Summit logo`(투명 PNG). 사이드바는 신규 설치 상태(Tour, READ ME, My Stuff) + Summit 2026. Screen 1 = Virtual screen 1920×1080(프로젝터 불필요). 상태 바는 최신 상태(Update 칩·렌치 점 없음) 그대로 — 내레이션이 "When an update is waiting…"으로 조건부 설명.
- **꼭 말할 주의점**: 카드 사진 클릭 = 즉시 송출, 확인창 없음. 3:50 데모는 스크립트/가상 화면임을 명시. 텍스트 애니메이션(줄이 하나씩 등장)은 앱에 없음. 드로어는 가리켜도 올라오지 않음.
- **제작 메모**: 이 회차는 **가장 마지막에 녹화**(완성된 데모 라이브러리가 Ep 4–10 녹화 후에만 존재). 공개는 첫 번째. 설치보다 앞에 두는 이유: 이 편은 "보기만 하는" 편이라 설치가 필요 없고, 2편이 여기서 붙인 이름(기어·상태 바·사이드바·Tour·READ ME)을 그대로 쓴다. 설명란 첫 줄에도 `Not installed yet? Episode 2 walks you through it.`를 넣는다.

### Ep 2 — Install, First Launch and Settings (5:00)

- **목표**: Mac/Windows에 설치하고 열고, 1회 로그인으로 Settings를 열고, 언어·카드 크기·업데이트 확인·안전 종료를 안다.
- **끝나면 할 수 있는 것**: 자기 컴퓨터에 LayerCue가 설치돼 있고 Settings가 열린다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: Settings 창 01–07 페이지. 요구사항 카드: macOS 13+, Apple silicon/Intel 별도 빌드; Windows 10 1809+, 64-bit. | Check your computer first. Mac: macOS 13 or later. Separate builds for Apple silicon and Intel. Windows 10 version 1809 or later, 64-bit. A second screen is what LayerCue is for. You do not need one to start. | `start/install.md` (System requirements) |
| 0:30 | Mac B-roll: About This Mac 칩 확인 → 다운로드 페이지 두 빌드 → .dmg → Applications로 드래그 → 꺼내기 → Applications에서 열기 → 첫 실행 Open. | Open About This Mac. Note Apple silicon or Intel. Download the matching build. Drag LayerCue onto Applications. Eject the disk image. Open it from Applications, not from the image. macOS may check once. Choose Open. LayerCue is signed and notarized. | `start/install.md` (Installing on a Mac) |
| 1:15 | Windows B-roll: Store 목록(CastPad, free) → Start 메뉴 → 시작 창 "Preparing the screen…" + 버전 → 메인 창. 두 번째 실행 시 기존 창 앞으로. 자막 "Store shows 1.9.12.0 for 0.9.12" (녹화 전 Store 목록 캡처로 확인). | On Windows, LayerCue comes only from the Microsoft Store. Published by CastPad. Free. A small window shows what it is getting ready. The main window follows. LayerCue runs once at a time. Open it again and the existing window comes forward. The Store shows the version one higher. | `start/install.md` (Installing on Windows) |
| 1:55 | 새 사이드바. Tour 클릭 → 5개 가이드. Finder: Documents/LayerCue. 자막 `C:\Users\<name>\LayerCue`. READ ME 우클릭 Delete → Cmd+Z 복구. | You get three things. READ ME: five guides. Tour lines them up. My Stuff: one empty New Presentation. They are ordinary presentations. Click their names to look. A click on the picture would send it. Your files live in a LayerCue folder. Documents on a Mac. Your user folder on Windows. When done, right-click READ ME and Delete. Command Z brings it back. | `start/install.md` (first time); `help/files.md` |
| 2:40 | 기어 → "Sign in once to use the beta" → Sign in with Google → 브라우저 "You are signed in." → 패널 사라짐, 01–07. Never mind 버튼 표시. | Click the gear. A sign-in panel covers Settings. The beta is free. Everything you use during a show works without an account. Only Settings and Tell us what's wrong need it. Press Sign in with Google. Finish in the browser. Come back. If you closed the browser halfway, press Never mind and start again. | `start/install.md` (Sign in once); `settings/index.md` (signing in) |
| 3:25 | 01 General: Language English→한국어→English 즉시 반영. Slide card size S/M/L. Remember window layout On. Remember master volume Off 강조. | Values save as you change them. Language changes the menus at once. Card size: bigger cards mean fewer wrong clicks in a dark booth. Remember window layout keeps your windows. Remember master volume is off on purpose. The master starts at zero every launch. A show never opens silent. | `settings/index.md` (General) |
| 4:00 | 05 Tools: LayerCue row → Check. 상태 바 오렌지 Update 칩(스테이지드). 빨간 경고줄. 자막 "Windows: updates come from the Microsoft Store; the Update chip still appears (0.9.10+)." 자막 "Mac 0.9.12: menu bar — Settings ⌘,". | On Tools, press Check. On a Mac, LayerCue checks once a day on its own. Nothing installs until you press Update. Never update during a show. The screen would go dark. Your presentations are not inside the app. They stay. On a Mac, 0.9.12 adds a menu bar. Settings is Command comma. | `settings/index.md` (LayerCue updates; platform notes); `start/install.md` (Updates); `help/shortcuts.md` (Mac menu bar) |
| 4:30 | Cmd+Q → "Quit LayerCue?" → Cancel. 출력 ON 상태(스테이지드)에서 다시 → 빨간 "You are on air". Cancel. | Quitting always asks first. Your work is saved. If the output is on, it warns in red. Quitting would black out the screen. Press Cancel. | `start/install.md` (Quitting safely) |
| 4:45 | 엔드 카드 + 로드맵 카드(2). | You can now open Settings on your own computer. Next: Episode 3 — Your First Show: Screen On, Slide Out, Clear. | — |

- **데모 자료**: 깨끗한 macOS VM과 Windows VM(설치 B-roll만), 다운로드 페이지·Store 목록 캡처(버전 문자열 확인용), 테스트 Google 계정(주소 블러), 스테이지드 Update 칩 상태, 4:30용 출력 ON 스테이지 상태.
- **꼭 말할 주의점**: Apple silicon 빌드는 Intel Mac에서 안 돎, macOS 12 이하 불가. 디스크 이미지에서 실행 금지. Settings는 1회 로그인·인터넷 필요. 쇼 중 업데이트/종료는 관객 화면을 끈다. Windows 업데이트는 Store가 제공(Check는 "Updates come automatically from the Microsoft Store."); 0.9.10 이전 Windows는 업데이트를 스스로 찾지 않음.

### Ep 3 — Your First Show: Screen On, Slide Out, Clear (5:00)

- **목표**: 관객 화면을 고르고, 전원을 켜고, 슬라이드를 보내고, CLEAR/키로 내리고, 사고 없이 출력을 닫는다. **시리즈의 안전 회차.**
- **끝나면 할 수 있는 것**: 프로젝터에 슬라이드 한 장을 올리고 안전하게 내릴 수 있다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 프로젝터 피드에 READ ME "Start here" 슬라이드. 두 화면(제어창 + 프로젝터) 분할. 자막 "Goal: one slide on the projector, then down again, safely." | Today we go on air. One slide on the projector. Then down again, without a scare. We use the READ ME guides as slides. Plug in your second screen first. | `start/first-show.md`; `output/index.md` (stage tile) |
| 0:25 | 타일 해부: 01 탭, 헤더(이름·해상도·전원), 프리뷰, Layers shown 7셀, 레이어 컬럼 CLEAR, 컨트롤 로우. | Read the tile from the top. The tab says 01. The header shows the screen and the power switch. The preview shows what Screen 1 shows. Under it, seven small cells: Layers shown. To the right, the layer column headed CLEAR. At the bottom, the control row. | `output/index.md` (The stage tile) |
| 0:55 | 01 탭 클릭 → 이름 "Audience" → Screen 목록: 프로젝터, "— main display", 가는 선 아래 Virtual screen. 프로젝터 선택. 자막 "Until you choose a screen yourself, LayerCue follows the cable." | Click the 01 tab. Type a name: Audience. Open Screen. Plugged-in screens come first. The one marked main display is the screen you work on. Do not pick it. Below the line are virtual screens: a size, no window. Pick the projector. If a projector was plugged in at first launch, LayerCue already chose it. The output may already be open, black. | `output/index.md` (Choosing the screen; Virtual screens; First launch); `start/first-show.md` (monitor tile) |
| 1:50 | 전원 ON → 프로젝터 검정, 01 오렌지, "On air 1/1 · Audience". OFF → 데스크톱. 다시 ON. 툴팁 "Stop Output". 케이블 분리 컷: "not connected". 자막(내레이션 없음) "Mac: the projector's resolution may change while power is on. It returns when you switch off." | The power switch is the output window. On: the projector goes black, because the stage is empty. The 01 turns orange. On air one of one. Off: the desktop comes back. LayerCue remembers the switch. Unplugged? The header says not connected. The output appears the moment you plug in. | `output/index.md` (Turning a monitor on and off; Output resolution on a Mac) |
| 2:35 | "Start here" 사진 클릭 → 프리뷰·프로젝터. 오렌지 테두리, 사이드바 오렌지 바, F 셀 인디고, 상태 바 제목. → 키 두 번. 송출 중 카드 재클릭: 변화 없음. | Send a slide: click its picture once. It goes out that instant. No confirmation. See what lit up. Orange border on the card. Orange bar in the sidebar. The F cell turned indigo. The status bar names it. Press the right arrow for the next. Clicking the live slide again does nothing. It stays up. | `start/first-show.md` (Sending slides); `output/index.md` (live indicators) |
| 3:20 | CLEAR → 페이드 아웃, 프로젝터 검정. 다시 보내고 F 옆 × 클릭. 다시 보내고 Cmd+1. 자막 "F1 Clear All · F2 Foreground · F3 Background · F4 Overlays — or ⌘/Ctrl + 1–4". | CLEAR takes every layer down. The x beside a filled cell clears only that layer. Keys too: F1 everything, F2 foreground, F3 background, F4 overlays. On a Mac, F keys often change brightness. Use Command 1 to 4. Control on Windows. Clearing fades over the Fade out time. Clear All does not stop the music. | `start/first-show.md` (Layer column and CLEAR); `output/layers.md` (Taking things down); `help/shortcuts.md` (Clear keys) |
| 4:00 | 송출 중 Esc → 알림 "On air — to stop, use the power switch above the preview or ✕ on the output screen". CLEAR → 전원 OFF. 다시 ON 상태에서 Screen을 "— main display"로 → 전원이 꺼지며 메시지. 출력 위 마우스 → 둥근 ✕(B-roll). 마지막 5초 자막 카드: "not connected = the cable · Pick a screen = nothing chosen · Virtual screen = no window". | Your hand will reach for Escape. Press it and nothing goes dark. LayerCue shows a reminder instead. There is no panic key. Clear first. Then switch the power off. Pick the main display while power is on. LayerCue switches the power off and tells you. It never covers its own window by itself. If it is covered, move the mouse and click the round x. Closing the output clears nothing. If nothing reaches the audience, read the header. Choosing a screen sends nothing; only the power switch does. | `start/first-show.md` (Esc and closing); `help/shortcuts.md` (Esc); `output/index.md` (main display); `help/index.md` (Nothing reaches the audience screen) |
| 4:45 | 엔드 카드 + 로드맵 카드(3). | You can now put one slide on the projector and take it down safely. Next: Episode 4 — Libraries, Presentations and Cue Sheets. | — |

- **데모 자료**: 샌드박스에 외부 디스플레이로 등록된 "Projector 1920×1080" + "— main display" + 가상 화면이 목록에 함께 보이는 상태. Tour 큐시트. 제어창과 프로젝터 피드 동시 캡처. 케이블 분리는 샌드박스 디스플레이 분리 스크립트(불가하면 B-roll). 둥근 ✕는 B-roll.
- **꼭 말할 주의점**: Esc는 모니터를 끄지 않음. main display 선택 시 자동 전원 OFF + 메시지; 덮였으면 둥근 ✕. 모니터 OFF는 아무것도 내리지 않음. Mac은 Cmd+1–4(Control 아님). 가상 화면은 창이 열리지 않음. 첫 실행에 두 번째 화면이 있으면 Screen 1이 자동 선택되고 검정 출력이 바로 열림. Mac은 전원 ON 중 모니터 해상도가 1:1로 바뀜(자막만).

### Ep 4 — Libraries, Presentations and Cue Sheets (5:00)

- **목표**: 라이브러리·프레젠테이션·큐시트를 만들고, 순서를 짜고, 이름을 바꾸고, 안전하게 삭제·undo하고, Cmd+F로 찾는다.
- **끝나면 할 수 있는 것**: 한 이벤트의 러닝 오더(큐시트)를 처음부터 만든다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 완성된 "Summit Day 1" 큐시트. 아이콘 3종 카드: 두 장 카드=Presentation(.pplist), 폴더=Library, 리스트=Cue sheet(.ppcue). | Three words. A presentation is one set of slides. A library is where it lives: a real folder. A cue sheet is the running order for one event. It holds links, not copies. Edit once, every cue sheet shows the change. Delete a cue sheet: the presentations stay. Delete a library: its presentations go with it. | `library/index.md` (Presentation vs library vs cue sheet) |
| 0:40 | 사이드바 행 읽기: 폴더/인디고 리스트/슬라이드 수. Tour 안의 프레젠테이션 클릭 vs READ ME에서 클릭. 송출 중 오렌지 바. | A folder icon is a library. An indigo list is a cue sheet. Click a presentation inside a cue sheet: the whole running order, scrolled to it. Click it in the Library: that one alone. A short orange bar means something from it is on stage. | `library/index.md` (Reading the sidebar) |
| 1:20 | + beside Cue Sheets → New Cue Sheet "Summit Day 1". + in Library drawer → New Library "Summit 2026". 라이브러리 행의 + → New Presentation 대화상자: Name "Keynote — Dana Okafor", Which library, Add to cue sheet, Create. | Press the plus beside Cue Sheets: New Cue Sheet. Name it now. Press the plus in the drawer: New Library. Point at the library row and press its plus. The New Presentation dialog asks name, Which library, and Add to cue sheet. Press Create. It lands at the end of the cue sheet. | `library/index.md` (Creating); `start/first-show.md` (Make a presentation; Make a cue sheet) |
| 2:10 | 드로어에서 "Welcome loop"를 큐시트로 드래그(드로어 비켜남, 인디고 선). 우클릭 → Add to Cue Sheet. 행 드래그로 순서. 우클릭 → Remove from Cue Sheet. | Three ways in. Right-click: Add to Cue Sheet. Drag from the drawer up; the drawer drops out of the way. Or pick the cue sheet in the dialog. Drop between rows to place it. Drag rows to reorder. Remove from Cue Sheet changes only the order. The presentation stays in its library. | `library/index.md` (Building and reordering) |
| 3:00 | 라이브러리 행 우클릭 메뉴(Rename·Move to Library·Delete 포함) vs 큐시트 안 메뉴(Remove from Cue Sheet). Rename. My Stuff에서 Summit 2026으로 드래그 이동. | The menus differ by half. In the Library: Rename, Move to Library, Delete. Inside a cue sheet: Remove from Cue Sheet instead. Rename renames the file on disk too. Every presentation lives in exactly one library. | `library/index.md` (Organising; Right-click menus) |
| 3:30 | 큐시트 Delete → 프레젠테이션 남음 → Cmd+Z 알림. 슬라이드 있는 프레젠테이션 Delete → "Delete this presentation?" → Cmd+Z. | Delete a cue sheet and only the order goes. Delete a presentation and it leaves every cue sheet; its files stay. Delete a library and every presentation in it goes. Nothing is erased: it all goes to the Trash. Command Z brings any of it back, up to fifty steps. One rule for show day: do not delete in the sidebar during the show. | `library/index.md` (Deleting and undo); `help/index.md` (Undo after deleting) |
| 4:15 | Cmd+\ → 사이드바 숨김, 상태 바 피커. Cmd+F → "doors open" → 결과 → Return. 자막(내레이션 없음) "Drag a result straight onto a cue sheet." | Command backslash hides the sidebar; a picker appears in the status bar. Command F opens Find. There is no button for it. It searches names and slide text. Return jumps there; nothing goes out. | `library/index.md` (Hiding the sidebar); `library/find.md`; `help/shortcuts.md` (Find) |
| 4:45 | 엔드 카드 + 로드맵 카드(4). | You can now build a running order from scratch. Next: Episode 5 — Adding Slides and Reading Cards. | — |

- **데모 자료**: 신규 사이드바 + My Stuff "Welcome words". 스크립트가 라이브러리 Summit 2026, 큐시트 Summit Day 1, 프레젠테이션 Keynote — Dana Okafor / Welcome loop / Sponsor thanks 생성. Find용 두 번째 라이브러리 "Northfield Academy" > "Prize Night 2026"(슬라이드 텍스트 "Doors open 18:30").
- **꼭 말할 주의점**: 라이브러리 삭제는 안의 모든 프레젠테이션을 Trash로. Rename/Move/Delete는 라이브러리 행에만. 큐시트엔 프레젠테이션만, 각 1회. Find는 단축키 전용, 80개까지. 사이드바 숨김 중엔 드롭 불가. (Lock editing은 Ep 6에서 가르친다 — 여기서 언급하지 않음.)

### Ep 5 — Adding Slides and Reading Cards (5:00)

- **목표**: 영상·사진·사운드·텍스트 붙여넣기로 슬라이드를 넣고, 카드를 읽고, 순서·복사·복제·삭제하고, File missing을 고친다.
- **끝나면 할 수 있는 것**: 프레젠테이션에 실제 미디어를 채우고 정리한다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 채워진 "Keynote — Dana Okafor". 영상·사진·mp3·텍스트 드롭, 배지 Video/Image/Music/Text. .txt 거부 알림. | A slide is one thing you put on the screen, or a sound you play. The file extension decides the kind. Each card wears a badge. Anything LayerCue cannot play is refused up front, with a notice, so it cannot fail on stage. PowerPoint and PDF import as many slides. That is Episode 14. | `slides/index.md` (What a slide is) |
| 0:40 | 타이틀 바 + (Add File) → 파일 선택기, Audio file 타입. 끝에 추가. "Copying" 진행 바. | The plus is Add File. Sound files hide under the Audio file type. LayerCue copies every file into its own media folder. The card says Copying while it works. It plays from the original until the copy is done. | `slides/index.md` (Adding slides); `start/tour.md` (title bar buttons) |
| 1:15 | Finder에서 사진 3장 드래그: 카드 사이 선. 의도적으로 카드 중앙에 1장 홀드 → 카드 하이라이트 → 드롭 → 미디어 교체. Cmd+Z. 같은 이름 대화상자 Use existing / Replace / Keep both. | Drag files from Finder. A line between cards means add here. Now watch. Hold one file over the middle of a card: the card lights up. Drop, and it swaps that slide's media. Handy on purpose, alarming by accident. Command Z puts it back. A same-name file asks: Use existing, Replace, or Keep both. Replace changes every slide using that file. | `slides/index.md` (Swapping media; duplicate names) |
| 2:05 | 텍스트 에디터에서 Harbor City Choir 프로그램 노트 복사 → 빈 곳 클릭 → Cmd+V → 텍스트 4장. 긴 카드 우클릭 → Split into slides. YouTube URL 붙이기 → YouTube 카드. | Paste works too. Copy text, click an empty spot, Command V. It splits at blank lines into text slides. Too long? Right-click the card, Split into slides. Paste a YouTube address and you get a YouTube slide. Paste a screenshot and you get a picture. The chain button, Link, also takes a YouTube address. More in Episode 13. | `slides/index.md` (Adding slides: paste; Text slides in the list); `help/shortcuts.md` (paste) |
| 2:40 | 카드 콜아웃: 번호(좌상), 레이어 칩(우상, FG는 호버 시만), 런타임(우하), 배지·이름. 오렌지(송출) vs 인디고(선택). 빨간 File missing → 우클릭 Locate file → Relinked. | Top left, its number. Top right, the layer chip. BG and overlay chips always show; FG shows only while you hover. Bottom right, run time. Orange is on air. Indigo is only selected. A red File missing card has lost its file. Right-click, Locate file. Pick the same name and every slide using it is relinked. | `slides/index.md` (Reading a card; missing file); `help/index.md` (Locate file) |
| 3:25 | 카드 드래그 재배치. Cmd-click 3장 → 다른 프레젠테이션 헤더로 드래그 "Copied 3". Option 홀드 → Move 배지. Cmd+D. Option+Cmd+→. | Drag a card to reorder. Command click or Shift click selects several. Drag from an empty spot to draw a box. Drag onto another presentation: copied. Hold Option as you let go to move. Command D duplicates. Option Command arrows move a slide by keyboard. Control Alt on Windows. | `slides/index.md` (Reordering, copying, moving; selecting several) |
| 4:05 | Delete → "Deleted 1" + Undo. 우클릭 Delete ▸ Slide only / Slide and file (to Trash), 공유 파일 경고. | Delete removes only the slides. The file stays. LayerCue asks first only when a slide is live, or ten or more. The notice offers Undo. Slide and file sends LayerCue's copy to the Trash and warns if another slide uses it. | `slides/index.md` (Deleting slides) |
| 4:30 | 상태 바 슬라이더 S→L. | The slider sets card size. Bigger cards, fewer wrong clicks. | `slides/index.md` (Card size) |
| 4:45 | 엔드 카드 + 로드맵 카드(5). | You can now fill a presentation with real media. Next: Episode 6 — Running the Slide List. | — |

- **데모 자료**: `keynote-intro.mp4`, `summit-hall.jpg`, `sponsor-wall.jpg`, `crowd.jpg`, `walk-on.mp3`, 거부용 `notes.txt`; Harbor City Choir 프로그램 노트 4단락 텍스트(한 단락은 길게 — Split into slides용); 외부에서 이름을 바꿔 File missing을 만든 파일 1개.
- **꼭 말할 주의점**: 카드 사이=추가, 카드 중앙=교체. PPTX/PDF는 교체되지 않고 뒤에 가져옴. 긴 텍스트는 여러 장으로 분리. Replace는 그 파일을 쓰는 모든 슬라이드 변경. 텍스트/YouTube 슬라이드는 File missing이 없음.

### Ep 6 — Running the Slide List: Send, Select, Keys and Layers (5:00)

- **목표**: 키보드로 라이브 운용, 보내지 않고 미리 보기, 칩으로 레이어 지정, 오버레이 규칙, 오렌지 표시 추적, 컨트롤 로우, Lock editing.
- **끝나면 할 수 있는 것**: 프레젠테이션 한 개를 처음부터 끝까지 레이어 포함해 실수 없이 돌린다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: Prize Night 무대(배경 루프 + 수상 부문 텍스트 + 교표 오버레이). 분할: 사진 클릭→출력 변경; 이름 클릭→출력 유지, Slide settings 로드; Option-클릭; 더블클릭→재시작. | One rule runs the show. A click on the picture is a send. Click the name instead, or Option click, and it only loads into Slide settings. Nothing goes out. Double click a picture to restart it. Sending never pulls Slide settings along. So you can set up the next slide while one is live. | `slides/index.md` (send vs select); `start/tour.md` (Clicking slides) |
| 0:40 | 이름 클릭으로 포커스. → 3번. Option+→ 2번(커서만). Return 송출. ↓ 한 줄. | Right arrow sends the next slide. Up and down jump a row, and they send too. Hold Option with the arrows to move without sending. Then Return. Shift widens the selection. Arrows carry on from the last sent slide and stay in one presentation. | `slides/index.md` (Keyboard); `help/shortcuts.md` (Moving through slides) |
| 1:30 | 7레이어 다이어그램(1–5 위, F, B, 그 아래 검정). 영상→B, 배경 없는 텍스트→F, 교표→overlay 1. | Seven layers stacked. Overlays one to five on top. Then F. Then B. Under all of it, black. Where a slide draws nothing you see the layers below. A text slide with no background colour is see-through around its words. A slide goes to the foreground unless you choose. A music slide goes on no layer. | `output/layers.md` (The seven layers) |
| 2:15 | 호버→FG 칩. 클릭→BG(앰버). 길게→1 Overlay(그린). 클릭→2. 우클릭 Layer ▸. 3장 선택 후 칩 → "Changed layer for 3". BG 칩 카드 송출: 그림은 B, 글자는 F. 로고를 overlay 1, 두 번째 로고를 overlay 1에 → 교체. 텍스트 띠를 overlay 3 → 둘 다 유지. | The chip colours match the layer column. Click: foreground to background. Press and hold: overlay one. Click again to step. Several selected? All change. Moving a slide to the background sets its sound to zero. A Background slide splits: its backdrop goes to B, its words to F. Changing a chip never moves what is already on stage. One slide per overlay. Send another to the same overlay and it replaces the first. A logo on one and a band on three both stay. | `slides/index.md` (The layer chip); `output/layers.md` (Putting a slide on a layer; Background slides; Overlays and naming them) |
| 3:10 | 오렌지 트레일: 카드 테두리→사이드바 바→타이틀 바→레이어 셀→01 탭→On air 칩→제목 점. 모니터 OFF → 점 회색. | Learn the orange trail. Card border. Sidebar bar. Filled cells. Orange tab number. The on-air chip counts live monitors. The title names the slide. The dot is orange on air, grey when something is up but no monitor is on, faint when clear. | `output/index.md` (live indicators) |
| 3:40 | B·F에 영상 둘. B 셀 클릭→흰 외곽선 이동, 컨트롤 로우 "Background". 일시정지·속도·볼륨. 빨간 ■ → 그 레이어만. 자막 "Stage controls: for now only. Not saved." Layers shown 셀은 숨김일 뿐. | The control row works on one layer: the cell with the white outline. Click another lit cell to switch. Pause, speed and volume here are for this moment only. Not saved. The red square takes down only that layer's video. The Layers shown cells under the preview hide a layer on this monitor. They clear nothing. | `output/layers.md` (control row); `start/tour.md` (Stage controls; Layers shown) |
| 4:20 | 연필→자물쇠. 드래그 시도 → "Editing is locked while presenting". 사진 클릭은 송출됨. 잠금 해제. 자막 "The lock does not cover the sidebar or Presentation settings." | Before a show, press the pencil. It becomes a padlock. The list cannot change. Sending still works. Undo is off while locked. The lock does not cover the sidebar or Presentation settings. Leave them alone during the show. Press the padlock to unlock. | `slides/index.md` (Lock editing); `output/index.md` (Locking editing); `library/index.md` (Deleting and undo) |
| 4:45 | 엔드 카드 + 로드맵 카드(6). | You can now run one presentation live, layers included. Next: Episode 7 — Slide Settings. | — |

- **데모 자료**: "Prize Night 2026"(Northfield Academy): `stage-wash.mp4`(루프 BG), 수상 부문 텍스트 8장(배경색 없음), `school-crest.png`, 두 번째 로고 `sponsor-mark.png`, 텍스트 띠 1장(overlay 3용), `highlights.mp4`. 샌드박스 프로젝터 ON(오렌지 표시가 진짜).
- **꼭 말할 주의점**: 클릭=송출, 두 번째 클릭은 내리지 않음. 맨 화살표는 관객 화면을 움직임(Option/Alt). BG 이동 시 볼륨 0. 컨트롤 로우 값은 다음 슬라이드에서 사라짐. Lock editing은 사이드바·Presentation settings를 덮지 않음(여기서 가르치고 Ep 18에서 상기). 오버레이 하나엔 슬라이드 하나, 같은 슬라이드는 두 오버레이에 동시에 못 올림. Mac에선 Cmd+1–4가 Stage 메뉴에도 있음(자막 또는 설명란).

### Ep 7 — Slide Settings: Fit, Trim, Loop and Volume (4:30)

- **목표**: 송출 전 한 슬라이드를 보정한다: Scale, Crop & fit, In/Out, 속도, Repeat, 볼륨(저장됨). To Screen으로 프레임 대기.
- **끝나면 할 수 있는 것**: 세로 영상·검은 머리 영상·과한 볼륨을 송출 전에 고친다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 세로 폰 영상이 Fit + blur bg로 와이드 무대에 꽉 찬 모습. 분할: 왼쪽 컨트롤 로우 / 오른쪽 Slide settings "Option + slide to load". 자막 "Left: for now. Right: saved on the slide." | Two places change how a slide plays. The control row changes what plays right now. Not saved. Slide settings, at the right end, is saved on that one slide. The heading tells you how to load: Option plus slide. Alt on Windows. | `slides/settings.md` (Loading); `start/first-show.md` (Slide settings) |
| 0:30 | 영상 라이브 중 Option-클릭 → 패널 로드, 무대 불변. 패널 프리뷰 무음. 우클릭 → Slide settings. | Load three ways: the name row, Option click, or right-click and Slide settings. The panel's preview stays silent while the stage has sound. That is not a fault. Set up the next slide while another is live. Then click its picture, or press Enter. | `slides/settings.md` (Loading); `output/sound.md` (Previews stay quiet) |
| 1:00 | 세로 영상: Fill / Stretch / Fit / Fit + blur bg 순회. 사진 5장 선택 → 우클릭 Crop & fit ▸ Fit → "Changed scale for 5". | A new slide starts on Fit, which can leave black bars. Fill cuts off what spills. Stretch ignores proportions. Fit plus blur background fills the space with a blurred copy. That is the one for a vertical phone video. For many slides at once: select, right-click, Crop and fit. | `slides/settings.md` (Scale) |
| 1:35 | 썸네일 기어 → Crop & fit 시트: 핸들, L T R B, Result, Anchor 3×3, Done. 연사 얼굴로 크롭, Anchor 상단. | The gear opens Crop and fit. Drag inside to move, handles to size. The numbers are percent trimmed. Anchor decides which side is cut with Fill, or where the space goes with Fit. Every change saves at once. Done just closes. On a text slide the gear is a pencil. | `slides/settings.md` (Crop & fit; Anchor) |
| 2:10 | `highlights.mp4`: 진행 바 클릭 → → 프레임 스텝 → In point. 크레딧 전 Out point. Clear In/Out. 속도 칩 1.25×. Repeat 버튼: Loop/Play once, Loop crossfade, Use default. | Drag to where it should start. Click the bar and tap the arrows for one frame. Shift for ten. Press In point. Then Out point. This speed chip is saved; the one in the control row is not. They look alike. Repeat: a background slide loops, everything else plays once, until you choose. Loop crossfade smooths the join on B. | `slides/settings.md` (In/Out; speed; Repeat); `help/shortcuts.md` (frame step) |
| 3:00 | 보라 Slide volume 60% → F로 송출: 레이어 볼륨 60. 칩 BG로 바꿔 송출: 0%. 올리면 무대 즉시 반영. | The purple bar is the slide's volume. Saved. When it goes out, the layer starts there. A slide keeps two values: one for F and overlays, one for B. The first time on the background it is zero percent. On purpose. Move it up and it stays. | `slides/settings.md` (Slide volume) |
| 3:35 | 패널 진행 바를 타이틀 프레임에 → To Screen → 무대에 정지 → 컨트롤 로우 ▶. 다른 슬라이드 로드 → Enter. Set as thumbnail 아이콘. | To Screen puts the slide on stage without playing it, held on this frame. Start it with play in the control row. Park a video on its title frame and roll it on cue. Enter sends the loaded slide from its in point. The picture icon sets the card thumbnail from this frame. | `slides/settings.md` (To Screen; Set as thumbnail) |
| 4:15 | 엔드 카드 + 로드맵 카드(7). | You can now fix a slide before it goes out. Next: Episode 8 — Presentation Settings. | — |

- **데모 자료**: `highlights.mp4`(앞 2초 검정, 끝 크레딧), `backstage-vertical.mp4`(9:16), `dana-okafor-portrait.jpg`, 가로 사진 5장.
- **꼭 말할 주의점**: 사진 클릭은 송출. 스트리밍 YouTube엔 Fit + blur bg·크롭 없음. 속도 칩 둘 중 Slide settings만 저장. 배경 볼륨 0%는 설계. 더블클릭 이름은 에디터를 연다.

### Ep 8 — Presentation Settings: Fades, Auto-dismiss and Layer for This List (3:30)

- **목표**: 프레젠테이션 단위 4값을 설정하고, "기본값 따름"과 "자기 값"을 구분한다.
- **끝나면 할 수 있는 것**: 영상 프레젠테이션엔 느린 크로스페이드, 로어서드엔 Auto-dismiss, 루프 폴더엔 Background 고정.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 두 영상이 2초 겹쳐 넘어가는 무대. 타이틀 바 두 원 → 작은 패널(Crossfade·Fade out·Auto-dismiss). 겹친 시트 → 레이어 목록. 사이드바 우클릭 → 전체 창 + Done. | Every presentation carries four values. Crossfade, Fade out, Auto-dismiss, and Layer for this list. The two circles open the fades. The stacked sheets open the layer list. Right-click in the sidebar for all four. They belong to the presentation, not the cue sheet. | `library/presentation-settings.md` (Opening); `start/first-show.md` (Presentation settings) |
| 0:35 | "Welcome loop" Crossfade 2 s → 두 슬라이드 송출, 긴 겹침. "Welcome words" Fade out 0 → Cmd+2 즉시 컷. 다시 0.8. | Crossfade is how long a slide takes to come in. Fade out is how long it takes to go. Zero to five seconds. At zero it cuts. Each slide uses the values of its own presentation, so one cue sheet can mix slow videos and snappy words. | `library/presentation-settings.md` (Crossfade and Fade out) |
| 1:10 | "Sponsor thanks" Auto-dismiss 8 s. 오버레이 3에 송출. 화면에 카운트다운 오버레이(편집 그래픽). 스스로 내려감. | Auto-dismiss is for overlays. Set it above zero. This presentation's overlays then take themselves down after that many seconds. The clock starts when it actually shows. It does nothing for foreground or background slides. | `library/presentation-settings.md` (Auto-dismiss) |
| 1:45 | "Welcome loop" 겹친 시트 → Background. 자물쇠 칩, 카드 칩 흐려짐. "Sponsor thanks" → 3 Overlay. 칩 클릭 → Per slide. | Layer for this list puts every slide of a presentation on one layer. Background for loops. An overlay for lower thirds. A lock chip appears beside the title; card chips dim. Per slide releases them. It counts from the next send. Overlays that stop being overlays come down. | `library/presentation-settings.md` (Layer for this list); `output/layers.md` |
| 2:25 | 패널: 흐린 숫자 + "Following the defaults…". Settings › Stage › Default fades 변경 → 흐린 숫자가 함께 움직임. 슬라이더 직접 → 숫자 진해짐 + 둥근 화살표 Reset to default. 기본값 다시 바꿔도 불변. Reset. | A new presentation follows the defaults in Settings. The numbers are dim. Change the default and they move, including the presentation on stage. Move a slider and that value becomes this presentation's own: solid, with a reset arrow. Set defaults before the event, not during it. | `library/presentation-settings.md` (Following the defaults); `settings/index.md` (Default fades) |
| 3:05 | 네 값 요약 카드. | Four values. How slides come and go. Overlays that leave by themselves. A whole folder on one layer. | `library/presentation-settings.md` |
| 3:15 | 엔드 카드 + 로드맵 카드(8). | You can now set fades and a fixed layer per presentation. Next: Episode 9 — Text Slides in the Editor. | — |

- **데모 자료**: Summit 2026의 Welcome loop(영상 2개), Welcome words, Sponsor thanks(로어서드 2장, 오버레이 3). 카운트다운 그래픽은 후반 편집.
- **꼭 말할 주의점**: 기본값 변경은 진행 중인 쇼를 바꿈. Auto-dismiss는 오버레이만. Layer for this list엔 기본값이 없어 Reset이 건드리지 않음. Lock editing은 이 값을 얼리지 않음. Background loop crossfade는 별개 설정. 무대용 글자 띠는 "lower third"로만 부른다("caption"은 Ep 13 YouTube Captions에만).

### Ep 9 — Text Slides in the Editor (5:00)

- **목표**: 에디터를 열고, 텍스트 박스를 넣고 쓰고, 분할/병합, 폰트·크기·색·외곽선·그림자, 넘침 처리, 배경, 에디터에서 송출.
- **끝나면 할 수 있는 것**: 밝은 사진 위에서도 읽히는 가사/제목 슬라이드를 만든다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 합창단 사진 위 흰 글자+검은 외곽선 가사. 에디터 3가지로 열기(Show/Edit, 연필, 이름 더블클릭). 자막 "No Save button. Everything is saved as you go." | The editor opens three ways. Edit on the switch. The pencil on a title bar. Or double-click a slide's name. There is no Save button. Whatever you change is saved, however you leave. Press Show to come back. Escape backs out one step at a time. | `slides/text.md` (Opening and closing) |
| 0:35 | 리본 4행 줌: 1 Undo/Redo/Select/Text/Rectangle/Ellipse/Insert/Style, 2 Change/Box, 3 글자, 4 Align/Outline/Shadow/Fit. 사진 선택 시 3·4행 흐려짐. 체커보드. | Four rows. Row one: tools, Insert and Style. Row two: Change and Box. Row three is everything about letters. Row four: Align, Outline, Shadow, Fit. Hover any button for its name. Select a picture and rows three and four go dim. The checkerboard means transparent. | `slides/text.md` (ribbon layout) |
| 1:05 | 왼쪽 열: New Slide, Duplicate slide, 우클릭 Delete, Cmd+Z. 첫 줄 입력 시 슬라이드 이름 변경. Add text box, 더블클릭 편집, Esc. 긴 절 입력 중 Cmd+Return 분할 → 우클릭 Merge with previous. 자막 "Show mode: right-click several cards → Merge N into one". | Slides run down the left. New Slide adds one at the end. Duplicate slide puts a copy after. Delete does not ask; Command Z brings it back. A text slide names itself from its first line. Add text box lands in the middle. Double-click to edit. Escape ends typing. Command Return splits a slide at the cursor. Merge with previous joins it back. In the list, Merge N into one joins several. | `slides/text.md` (left column; Adding a text box; Typing; Splitting and merging); `slides/index.md` (Text slides in the list); `help/shortcuts.md` (Split and join) |
| 1:55 | 폰트 필드 "Search fonts…" → 호버 웨이트 → Bold. Font size 라벨 드래그, Shift 큰 단계. 제목 줄에 커서 → Line height. 한 단어 선택 → Tracking(0.9.12). | Search a font by any part of its name. Hover for its weights. The default is Pretendard JP. Font size is a percent of screen height, so it looks the same on 1080 and 4K. Drag any number's label. Shift for ten times bigger steps. Line height applies to the line with the cursor. Since 0.9.12, Tracking can apply to selected letters only. | `slides/text.md` (Choosing a font; size and spacing); `help/shortcuts.md` (Number fields); `changelog/index.md` (0.9.12) |
| 2:35 | 박스 선택 → Bold 전체. 단어 선택 → Bold 그 단어만. Text color 피커, Pick from screen으로 사진에서 색 추출. Clear formatting. | Where does a change land? Box selected: all its text. A word selected: that word only. Text color has an eyedropper, Pick from screen. It works over anything on your screen. Clear formatting resets the look; the text stays. | `slides/text.md` (where a change lands; Text colour); `help/shortcuts.md` (eyedropper) |
| 3:05 | 밝은 사진 위 흰 글자 → Outline ON(그룹 파랗게) → 읽힘. ▾ Width, Outline color. Text shadow. | White text over a bright photo disappears. Press Outline. The group turns blue and the text is readable. Open the arrow for width and colour. Text shadow works the same. Both scale with the font size. White with a black outline survives a bright sky and a dark stage alike. | `slides/text.md` (Outline and text shadow) |
| 3:35 | 긴 절 붙이기 → 파란 + 배지 → Expand box to fit text / Shrink text to fit. Shrink. Fit 그룹 Same text size across slides. 드래그 스냅 가이드, Shift 모서리. | When text does not fit, a blue plus badge appears. Expand the box, or shrink the text. Resizing a box never changes the font size. Same text size across slides keeps the size from jumping between verses. Look for this badge in rehearsal. Drag a box and guides snap it. Shift on a corner keeps proportions. | `slides/text.md` (Fit group; Same text size; moving and snapping) |
| 4:15 | Background row → Import image or video → Fit + blur bg → 카드 칩 BG. ✕로 지움. Show on output으로 송출 후 오타 수정 → 무대 따라옴. | The Background row lays a file under everything. The slide becomes a Background slide; its chip reads BG. The x clears it. Show on output sends the slide you are editing. If it is on stage, your edits follow live. Undo is kept per slide. | `slides/text.md` (Background row; Sending from the editor; Undo) |
| 4:45 | 엔드 카드 + 로드맵 카드(9). | You can now make a lyric slide that reads over any photo. Next: Episode 10 — Designing Slides. | — |

- **데모 자료**: "Spring Concert — Harbor City Choir": 빈 슬라이드, `choir-stage.jpg` 슬라이드, 넘침용 긴 프로그램 노트, 길이가 다른 가사 3장, Merge N into one 자막용 짧은 카드 3장.
- **꼭 말할 주의점**: Text 툴로 사진을 클릭하면 새 박스가 위에 생김. 마지막 줄만 Line height는 변화 없음. Word wrap OFF면 잘림. 스트리밍 YouTube엔 텍스트 불가(Make it a video box). Windows: Cloud fonts 불가 시 Font Cache Service. 앱 실행 중 설치한 폰트는 재시작 후.

### Ep 10 — Designing Slides: Shapes, Pictures, Styles (5:00)

- **목표**: 타이틀 슬라이드와 로어서드를 도형·아이콘·사진·그라디언트·테두리·그림자로 만들고, 정렬·순서·스타일 일괄 적용.
- **끝나면 할 수 있는 것**: 연사 이름 로어서드 1장을 만들고 20장에 스타일을 한 번에 입힌다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 완성 타이틀 "Riverside Tech Summit 2026" + 로어서드 "Dana Okafor — Keynote"(우측 투명 페이드). 빈 슬라이드로. Insert 그룹: Add text box·Insert shape·Insert icon·Add picture·Add video. 리본=중앙, 우클릭=포인터 위치. | Two things today: a title slide and a lower-third band. The Insert group adds things. From the ribbon they land in the middle, selected. From the right-click menu, where you clicked. One Command Z takes it away. A dim button says why in its tooltip. | `slides/design.md` (Insert group) |
| 0:40 | Rectangle 툴, Shift 정사각형, 힌트 줄. 더블클릭 "Day 1". Change shape → Chevron, 인디고 코너 포인트 드래그. Insert icon "microphone" → Return → Text color로 색, Solid. | Draw a rectangle. Shift keeps it square. Shapes hold text: double-click and type. Change shape turns it into one of fourteen shapes; drag the indigo corner points. Insert icon searches about fifteen hundred icons. Return places the first match. Its colour is the Text color. | `slides/design.md` (Shapes; Icons); `help/shortcuts.md` (drawing hints) |
| 1:25 | Add picture `summit-hall.jpg` → 비율 유지. Change: Fill/Fit/Stretch/Fill the slide/Set as background → 칩 BG. | Add picture keeps proportions. Fill covers the box, Fit shows it all, Fill the slide covers everything, Set as background drops it under the slide. LayerCue copies the file into its media folder, so moving the original breaks nothing. | `slides/design.md` (Pictures as boxes) |
| 2:00 | 하단 넓은 사각형. Style › Fill › Linear, 스톱 추가 → No fill → 우측 페이드. Radius, Border color, Box shadow. 이름 입력. | Open Fill, choose Linear. Click the band to add a stop. Set it to No fill: the band fades to transparent on the right. Radius rounds corners. Border color gives an edge. Box shadow falls behind the whole box; Text shadow only behind the letters. | `slides/design.md` (Fill and gradients; Border, corners, box shadow) |
| 2:40 | Box 그룹: Opacity 80, Rotation, Place X 5 Y 78 W 60 H 12. 사진 뒤 숨은 띠 → Cmd+], To front. Select overlapping. Align: 텍스트 정렬 vs Align across/Center on the slide, Distribute H. | Place sets X, Y, width and height as percent of the slide. Type numbers for a band that sits in the same spot on every slide. Picker opacity and box opacity multiply. Command right bracket brings a box forward. Select overlapping grabs a hidden one. In Align, the first buttons place text in its box; the rest place boxes on the slide. | `slides/design.md` (Box group; Stacking order); `slides/text.md` (Aligning) |
| 3:30 | 띠+이름 Cmd+C → 다음 슬라이드 Cmd+V. Cmd+D. 우클릭 Copy style → Paste style. Set as default style. Show 모드: 20장 선택 → Paste style "Style applied to 20 slides". | Copy boxes and paste them on another slide. Styles travel separately: Copy style, then Paste style on others. Position, size and words do not come along. Set as default style makes that look the start for new boxes. In Show mode, select twenty cards and Paste style once. That is the rehearsal fix. | `slides/text.md` (Copy/paste boxes; Passing a style along); `slides/index.md` (Text slides in the list) |
| 4:20 | 빠른 컷: Text inset, Add video ×2 + 스피커 뮤트, 화살표 넛지. | Text inset pads text from the edge. Add video puts a video in a box, up to four. Mute extras with the speaker button. Arrows nudge: Shift big, Option tiny. | `slides/text.md` (Text inset); `slides/design.md` (Video boxes); `help/shortcuts.md` (editor keys) |
| 4:45 | 엔드 카드 + 로드맵 카드(10). | You can now design a lower third and restyle twenty slides at once. Next: Episode 11 — Music: Your Own Channel. | — |

- **데모 자료**: `summit-hall.jpg`, 짧은 클립 2개, 일괄 Paste style용 텍스트 20장. 이름: Dana Okafor, Priya Natarajan, Tomás Reyes.
- **꼭 말할 주의점**: 다각형엔 둥근 모서리·박스 그림자 없음. 비디오 박스는 fill/border/shadow 불가, YouTube 슬라이드엔 추가 불가. 추가 영상은 뮤트하지 않으면 모두 들림. Backdrop 박스는 클릭을 받지 않음. 박스는 에디터에서만 붙여짐. 0.9.12엔 선(line) 툴 없음. (advanced, 설명란/고정 댓글로만: SVG 코드 붙이기·재색은 64 KB 초과·viewBox 없음 거부; 우클릭 Role ▸ Slide text/Title/Decoration/Backdrop — Decoration 헤더는 Paste style이 건너뜀.)

### Ep 11 — Music: Your Own Channel (4:30)

- **목표**: 프리쇼/휴식 재생목록, 재생·정지, In/Out 트림, 종료 동작, 영상 아래 덕킹, 러닝 오더 속 사운드 슬라이드.
- **끝나면 할 수 있는 것**: 개장 음악을 깔고, 수상 팡파르를 큐에서 쏘고, 영상 땐 음악을 낮춘다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: Prize Night 개장, 음악 재생 중 슬라이드 교체·CLEAR·F1 → 음악 유지. ■ → 페이드 아웃. 스카이 블루. | Music runs on its own channel. Send slides, clear a layer, Clear All: the music keeps playing. Only the square Stop under the list stops it. Everything music is sky blue. There are no keyboard shortcuts for music. Hover the buttons for names. | `music/index.md` (basics); `start/first-show.md` (Music) |
| 0:35 | mp3 3개를 "Drop music here"에 드롭 → Default 폴더. +(Add music). 중복은 "name-1". | Add tracks with the plus or drop files. Nine formats, mp3 to flac. Videos and pictures are left out quietly. The first tracks go into a folder called Default. Each is copied into the Music folder. Add the same song twice and you get name dash one. | `music/index.md` (Adding tracks) |
| 1:05 | Add folder "Pre-show", "Break". 폴더 바 열기(하나만), 수·총 길이. 행 드래그 순서. 다른 폴더 바에 드롭=복사. | Add folder asks for a name. Only one folder is open at a time. Its right end shows count and total length. Drag rows to set the order Play next follows. Drop a track on another folder's bar to copy it there; the two copies are then set separately. | `music/index.md` (Folders and order) |
| 1:35 | 행 클릭 → 사운드 바. 두 번째 클릭 → 크로스페이드. 더블클릭 재시작. Pause vs ■. 리스트 아래 볼륨·속도 자막 "Not saved". | Click a row: it fades in. Click another: they crossfade. Double-click to start over. Pause holds the place. Stop fades out and puts it away. On stage, music off means Stop. The volume bar and speed chip under the list are not saved. | `music/index.md` (Playing, pausing, stopping) |
| 2:05 | 슬라이더 버튼 → Track settings(Music 배지, 포맷 줄). 말 인트로 뒤 In point, 롱 페이드 전 Out point → 길이 스카이 블루. 볼륨·속도 저장. Stop·Next·Repeat. | For lasting values, open Track settings. The right panel changes its heading. Press In point after the spoken intro, Out point before the fade. Volume and speed here are saved on the track. The preview is silent while music plays; pause it to hear. | `music/index.md` (Track settings) |
| 2:40 | 행 끝 버튼 순환 Stop at end › Play next › Repeat one. Play next 중 다른 폴더 열기 → 그 폴더 첫 곡으로. | Stop at end is the default. Play next follows the open folder. Repeat one loops. Careful: open another folder mid-track and Play next continues there. For a stretch that must not change, use Repeat one. | `music/index.md` (End actions) |
| 3:10 | 자막 "Settings › Stage › Music: fade in / fade out / crossfade · Music while video plays: Keep → Lower · Lower to 0.25". Lower로 바꾼 뒤 음악 중 `keynote-clip-speech.mp4` 송출 → 음악 내려가고 복귀. | Music while video plays is Keep by default. Set Lower and the music drops while a video with sound is on stage. It comes back by itself when the video ends. | `music/index.md` (fades; music under video); `settings/index.md` (Music) |
| 3:45 | Prize Night "Awards": `applause-sting.wav` 카드(Music 칩). 수상 발표 순간 클릭 → 재생목록과 크로스페이드, 화면 그대로. ■. 빨간 트랙 → Relink file. | The award fanfare belongs in the running order. A sound file in a presentation is a sound slide with a Music chip. Click it and it takes the place of the playing music; the screen stays. A red track lost its file: Relink file keeps its range and settings. Nothing in the music list can be undone. Do not tidy it during a show. | `music/index.md` (Sound slides; Relinking, renaming, deleting) |
| 4:15 | 엔드 카드 + 로드맵 카드(11). | You can now run music under a show and duck it for video. Next: Episode 12 — Sound. | — |

- **데모 자료**: 로열티프리 연주곡 6개(가상 제목 Open Doors, Lobby Light, Interval, Quiet Hall, Walk-up, Closing Theme; 하나는 말 인트로 포함), `applause-sting.wav`, `keynote-clip-speech.mp4`, 파일을 옮겨 빨갗게 만든 트랙 1개.
- **꼭 말할 주의점**: Clear All/F1–F4는 음악을 멈추지 않음. 폴더 바에 드롭해도 그 폴더가 열리지 않음. Play next는 열린 폴더를 따름. Pause≠Stop. 음악 목록엔 undo 없음. 음악 크로스페이드는 리허설에서 한 번 들어볼 것(자막/설명란).

### Ep 12 — Sound: Device, Meter, Master and the No-Sound Checklist (4:30)

- **목표**: 장치를 이름으로 고르고, 미터·마스터를 읽고, MUTE/SOLO, 저장되는 볼륨 6곳, 1분 안에 무음 해결.
- **끝나면 할 수 있는 것**: "소리가 안 나요"를 체크리스트 순서로 고친다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 미터가 움직이는 무대. 상태 바 스피커 박스 → 목록(System default + 이름 장치) → "USB Audio Interface". 분리 컷: "Not connected", 오렌지 아이콘. | Everything LayerCue plays goes to one device. Click the speaker box. System default follows the computer. For a show, pick the device by name, so headphones connecting cannot steal the sound. If it goes away, the box reads Not connected. Sound falls back to the system default. Streaming YouTube uses the computer's default output. So LayerCue makes your device the default while it runs. It puts the old one back when you quit. | `output/sound.md` (Choosing the audio device); `start/first-show.md` (Sound device) |
| 0:50 | 큰 클립. 미터: 그린/오렌지/레드, 평균선, 피크, 클립 라인. 마스터 핸들 0 dB 위로 → 클립. 더블클릭 → 0 dB. Settings › General › Remember master volume OFF: 마스터 내리고 재실행 → 0 dB 복귀. | The tall meter shows what leaves LayerCue. A red line across the top is clipping: bring the master or that layer down. The handle on the meter is the master fader. Double-click for zero dB. The whole meter is the fader, so a stray click moves it. Watch: I pull it down, relaunch, and it is back at zero, because Remember master volume is off. | `output/sound.md` (meter and master); `settings/index.md` (Remember master volume) |
| 1:40 | MUTE 빨강, 미터 흐려져도 움직임. SOLO → 4개 바, B 셀 클릭 → 우측 쌍 앰버 외곽선. | MUTE silences everything that goes out. The meter keeps moving, dimmed. MUTE does not silence the previews. SOLO changes only the meter: the left pair is the master, the right pair is the layer you are controlling. The room hears the same. | `output/sound.md` (MUTE and SOLO) |
| 2:15 | 6개 볼륨 다이어그램 saved/not saved: Master(Remember 시만), MUTE(no), 컨트롤 로우(no), Slide settings(yes), 음악 슬라이더(no) vs Track settings(yes), Music while video plays(setting). 같은 영상 두 곳에서 바꾸고 재송출. | Volumes multiply, and only some are saved. The control row is for now; the next slide starts from its own value. Slide settings is saved. The music slider under the list is for now; Track settings is saved. Music while video plays is a setting that stays. And a slide moved to the background starts at zero. | `output/sound.md` (Where each volume lives) |
| 2:55 | 무대에 영상 재생 중 다른 영상 Slide settings → 프리뷰 무음. MUTE → 들림. 귀로 In point. | Previews stay quiet while the stage has sound. Press MUTE, or stop the music, and the preview can be heard. Then set your in and out points by ear. | `output/sound.md` (Previews stay quiet) |
| 3:20 | 사보타주 3종 후 체크리스트 오버레이: 1 MUTE red? 2 Master −∞? 3 Meter moving? 4 Layer speaker in the control row 5 Slide volume / on background? 6 Music while video plays. 장치 박스. | When there is no sound, work down the list. Is MUTE red? Does the master read minus infinity? Double-click. Is the meter moving? If it moves and the room is silent, check the device. Click the layer's cell and check the speaker in the control row. Check the slide's volume, and whether it is on the background. Check Music while video plays. Sound does not depend on monitors. | `output/sound.md` (No sound? checklist); `help/index.md` (No sound) |
| 4:15 | 엔드 카드 + 로드맵 카드(12). | You can now fix a silent show in under a minute. Next: Episode 13 — YouTube Slides. | — |

- **데모 자료**: 가상 오디오 장치 "USB Audio Interface", `crowd-cheer.mp4`(클리핑용), `keynote-clip-speech.mp4`, Ep 11 재생목록. 사보타주 상태(MUTE ON, 마스터 −∞, B에 0% 슬라이드).
- **꼭 말할 주의점**: 미터 전체가 페이더. 흐린 YouTube 바로 레벨을 읽지 말 것. SOLO는 관객 소리를 바꾸지 않음. 프리뷰 무음은 정상. 컴퓨터 출력을 손으로 바꾸면 LayerCue는 그대로 둠.

### Ep 13 — YouTube Slides: Streaming, Downloading, Captions (5:00)

- **목표**: YouTube 추가, 다운로드로 인터넷 의존 제거, 무대 커버·품질, 자막 전환, yt-dlp 갱신.
- **끝나면 할 수 있는 것**: 행사 전날 YouTube 영상을 안전하게 준비한다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 스폰서 영상이 무대에. Link → Add Link 창 → URL → OK. ID 이름 → 제목 도착. 두 번째 URL은 리스트에 붙이기. | Two ways to add. Press the chain, Link, and paste. Or paste the address onto the slide list. The card is named by ID until the title arrives. A new YouTube slide streams. That means it needs internet on the day. | `slides/youtube.md` (Adding) |
| 0:35 | Option-클릭 → Download → "Downloading 42%" → "Converting" → Downloaded, 배지 "YouTube ↓". Streaming/Downloaded 칩 전환. Settings › Files & YouTube: Download quality 1080p, Convert to H.264 When needed. | If a video has to play, download it. Load the card and press Download. Keep that slide loaded until it says Downloaded; load another and the file is not attached. Now it plays like a file: no internet, all four Scale modes, crop, text on top. Quality defaults to 1080p. A 4K conversion can take twenty minutes. Delete download removes the file. | `slides/youtube.md` (Downloading); `settings/index.md` (YouTube quality, H.264) |
| 1:35 | 스트리밍 송출 → 타일 커버 "YouTube is playing on the output screen" + Bring to preview, Quality (Auto), Chapters. Quality 1080p. Bring to preview → 출력 비움 → Send back to output. | Only one streaming video can be on stage at a time. While it plays on an output, the player moves there and the tile shows a cover. YouTube picks quality by player size, so raise it under Quality right after it goes out. Bring to preview pulls it into the tile, and off the outputs meanwhile. Send back to output returns it. | `slides/youtube.md` (on stage; cover); `help/index.md` (YouTube on stage); `output/multi.md` (YouTube on several monitors) |
| 2:35 | 에디터에서 스트리밍 슬라이드: "Text can't go over full-screen YouTube streaming" → Make it a video box. 또는 Downloaded로 전환 후 텍스트. | Full-screen streaming takes no text. Press Make it a video box, and the video shrinks into a box you can design around. Or download it; a downloaded copy takes text, crop and Fit plus blur background. | `slides/text.md` (editor pitfalls); `slides/youtube.md` |
| 3:05 | Captions › Manage languages… → Korean, Spanish → OK → Korean 선택 → 무대 즉시 변경. Settings: Default captions, Caption position Top, font, size. | Captions work while streaming only. Register languages in Manage languages, then pick one. It changes at once on stage. The choice belongs to the app, not the slide: each launch starts from Default captions in Settings. Position, font and size live there too. | `slides/youtube.md` (Captions) |
| 3:45 | 재생 후 Audio 행(더빙 트랙). 진행 바 챕터 틱, Previous/Next chapter. | After playback starts, an Audio row offers dubbed tracks; that choice is saved with the slide. Chapters show as ticks on the bar; step with the two buttons. | `slides/youtube.md` (dubbed audio; chapters) |
| 4:10 | 렌치 칩 오렌지 점. Settings › Tools › YouTube tool: Check, Update, Revert, Check the tool daily. Update → "Installed". 자막 "Then quit LayerCue and open it again." 흐린 Download 툴팁 "Not found". | LayerCue downloads with a tool called yt-dlp. When a link that worked last month fails, the fix is usually a newer tool, not a newer LayerCue. Press Check, then Update. Then quit and reopen. A dimmed Download button means Not found. Do this the day before, not mid-show. Always have a downloaded copy or a local file ready. | `slides/youtube.md` (Updating the tool); `settings/index.md` (YouTube tool) |
| 4:45 | 엔드 카드 + 로드맵 카드(13). | You can now prepare YouTube videos the day before. Next: Episode 14 — PowerPoint, PDF and Export. | — |

- **데모 자료**: 샌드박스 채널의 CC 영상 2개(챕터·다국어 자막 1개, 더빙 트랙 1개). **이 회차만 샌드박스 인터넷 허용**(제작 노트 참조). "Sponsor videos" 프레젠테이션. yt-dlp 업데이트 가능 상태 스테이징.
- **꼭 말할 주의점**: Downloaded까지 슬라이드를 로드 상태로. Bring to preview는 출력에서 영상을 뺌. 스트리밍 1개만. 자막은 슬라이드에 저장 안 됨. "Could not convert — check ffmpeg" → Convert to H.264 Never. 업데이트 후 종료·재실행(자막).

### Ep 14 — Bringing It In: PowerPoint, PDF and Export (4:30)

- **목표**: PPTX를 편집 가능한 슬라이드로, PDF를 그림으로 가져오고, 프레젠테이션을 PDF로 내보낸다.
- **끝나면 할 수 있는 것**: 연사가 보낸 덱을 10분 안에 큐시트에 넣는다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 가져온 키노트 덱이 무대에. 세 입구: New Presentation의 From PowerPoint…/From PDF…, 타이틀 바 +, 리스트에 .pptx 드래그. | Decks arrive three ways. In the New Presentation dialog, press From PowerPoint or From PDF instead of Create. Or Add File. Or drag the file onto the list. PowerPoint does not need to be on this computer. | `import/powerpoint.md`; `import/pdf.md` |
| 0:25 | Which library, Add to cue sheet → From PowerPoint… `Keynote-Okafor.pptx` → "Importing PowerPoint…" → "Imported 24 slides". 이름 더블클릭 → 오타 수정. BG 칩 → 클릭해 한 덩어리로. | Leave the name and it takes the file's name. LayerCue rebuilds every slide out of its own boxes. The text stays text. Imported cards carry a BG chip: background to B, text to F. Click the chip if the slide should go out as one piece. One Command Z takes back the whole import. Files import one at a time. Old dot ppt must be saved as pptx first. | `import/powerpoint.md` (Importing); `help/index.md` (import messages) |
| 1:20 | 알림 "May differ from the original: charts and SmartArt…". 표=셀별 박스, 차트 빠짐. 대체 폰트로 줄바꿈 변화 → 폰트 설치 후 재가져오기. | Read the notice. Text, shapes, pictures, tables and backgrounds come across. Charts, SmartArt, videos, sounds, animations and notes do not. Anything on the slide master is left out. Hidden slides are not skipped: delete the ones you do not need. A missing font is replaced, so lines can break differently. Install the deck's fonts first. For an exact look, save as PDF instead. | `import/powerpoint.md` (What comes across; Fonts) |
| 2:15 | From PDF… → PDF import 창: 썸네일, All/None/Range, Resolution FHD/2K/4K/6K, JPEG/PNG. Range "2-4" → Import → "Rendering…" → "Imported 3 pages". Cmd+F로 페이지 단어 검색. | A PDF comes in as pictures. The text cannot be edited. Every page starts picked. Click thumbnails or type a Range. Resolution is the long edge; 4K is the default. JPEG keeps files small. The words are kept for Find. A password-protected PDF is refused: remove the password first. | `import/pdf.md` (Importing a PDF) |
| 3:00 | 사이드바 우클릭 → Export to PDF… → All/None/Range → 저장 → "Exported to PDF —". PDF 리더에서 텍스트 선택·검색. | The other way round works too. Right-click a presentation and Export to PDF. The text stays text: selectable, searchable. One slide per 16 by 9 page. Streaming YouTube and audio slides give no picture, so leave them unpicked. Handy for a programme or a printout. | `import/pdf.md` (Exporting) |
| 3:35 | 가져온 덱 3장을 Ep 10 방식으로 빠르게 정리(Paste style 1회), 큐시트 순서에 끼움. | Now it is yours. Fix a title with Paste style. Drag it into the running order. | `slides/text.md` (Paste style); `library/index.md` |
| 4:15 | 엔드 카드 + 로드맵 카드(14). | You can now bring a speaker's deck into the running order. Next: Episode 15 — Your Files, Settings Pages and AI Helpers. | — |

- **데모 자료**: `Keynote-Okafor.pptx`(24장, 표 1, 차트 1, 숨김 1, Windows 전용 폰트 1), `Summit-Programme.pdf`(6쪽, 텍스트 기반).
- **꼭 말할 주의점**: Lock editing 중엔 가져오기 불가. 한 번에 한 파일. 차트·SmartArt·미디어·애니메이션은 안 들어옴. 스캔 PDF는 Find 불가.

### Ep 15 — Your Files, Settings Pages and AI Helpers (5:00)

- **목표**: 모든 미디어를 LayerCue 폴더 안에 두고 백업·이동하고, Import bundle·Account·Reset을 알고, 좁은 창 팝아웃을 쓰고, AI 앱을 연결하거나 Copy as HTML로 슬라이드를 다시 쓴다.
- **끝나면 할 수 있는 것**: 쇼 폴더를 다른 컴퓨터로 옮기고, AI로 가사 슬라이드를 만든다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: Finder의 LayerCue 폴더(Library, CueSheets, Videos, Images, Music, Backups). Settings › Files & YouTube › Media folder › Open. USB 영상 드롭 → "1 file lives outside the media folder" → Import external files → "Every file is inside the media folder." | Everything you make is ordinary files in one LayerCue folder. LayerCue copies every added file in and plays its own copy. Open Settings, Files and YouTube the day before. If it says files live outside the media folder, press Import external files. A disconnected disk breaks playback on stage. | `settings/index.md` (Media folder; Import external files); `help/files.md` |
| 0:45 | 종료 → 폴더를 외장 디스크로 복사. 두 번째 노트북: 같은 위치에 폴더 → 라이브러리 그대로, 화면은 재설정. Backups 폴더가 Library를 미러. | To back up, quit LayerCue and copy the whole folder. Settings are not in it. To move to another computer of the same kind, put the folder in the same place. Media is found by folder and name. Downloaded YouTube streams again, and screens must be set up again. Backups keeps the version before each save: one step back, not a history. | `help/files.md` (backing up; Backups; Moving) |
| 1:35 | Import bundle › Choose… → .pplistx → 사진 슬라이드 정상, 영상 슬라이드 File missing → Locate file. | A bundle, dot pplistx, carries one presentation to another computer. Pictures travel inside it. Videos and music do not: relink them with Locate file. | `settings/index.md` (Import bundle) |
| 2:00 | 07 Account: Keep settings in my account(Off), Sign out. 빨간 Reset → 대화상자 → Cancel. | Account can keep your settings in your account and bring them to another computer. Only settings travel; presentations and media never leave this computer. The red Reset puts every setting back. There is no undo. Card size, window positions and your monitor setup stay. Episode 16 covers that setup. | `settings/index.md` (Account; Reset) |
| 2:35 | 창을 좁힘: Slide settings 접힘 → Music 접힘. 헤딩 클릭 → 옆 창으로. 넓히면 복귀. Remember window layout. | On a laptop the window may be narrow. Slide settings folds first, then Music, then the sidebar. The heading of a folded part is a button: click it and the panel opens in its own window. Nothing pops out by itself. Remember window layout keeps all of this per set of monitors. | `start/tour.md` (Narrow window); `music/index.md` (narrow); `settings/index.md` (Remember window layout) |
| 3:10 | 06 AI apps → Connect on Claude Desktop → 앱 완전 종료(⌘Q) → 재실행 → 녹색 "Connected". 자막 "Also: LM Studio, Cursor. Not: ChatGPT, Gemini app, claude.ai". 새 채팅: "Make a cue sheet called Prize Night with …" → `[pause]` + 점프컷 → 슬라이드 생성. Cmd+Z → "Undone — AI command". | LayerCue has no AI of its own; an AI app on this computer can drive it. Press Connect on the app. Then quit that app completely and open it again. Closing its window is not enough. When the row turns green, ask in plain words. `[pause — AI works; jump cut]` Each AI action is one undo step. Lock editing holds for the AI too. Check web pictures yourself before they go on screen. | `ai/index.md` (Connect; What to ask; undo) |
| 4:00 | 텍스트 3장 우클릭 → Copy as HTML for AI → 브라우저 채팅에 붙이기 → `[pause]` → 답 복사 → 리스트에 Cmd+V → "From HTML: updated 3". Other AI apps: Copy command. | No connection? Right-click text slides and Copy as HTML for AI. Paste into any chat, say what you want, copy the answer, paste it back. The slides update. One Command Z takes the whole paste back. Other AI apps gives a command or config to copy. | `ai/index.md` (Copy as HTML; Other AI apps) |
| 4:45 | 엔드 카드 + 로드맵 카드(15). | You can now move a show folder and rewrite slides with an AI. Next: Episode 16 — More Screens: Stage Output Window and Layers Shown. | — |

- **데모 자료**: USB 경로의 `sponsor-reel.mp4`, 두 번째 VM, .pplistx 번들, 샌드박스용 AI 앱(계정 블러), 브라우저 채팅. AI 응답 대기는 편집에서 점프컷.
- **꼭 말할 주의점**: 미디어 폴더를 손으로 정리하지 말 것. 설정은 폴더에 없음. Connect 후 AI 앱 완전 종료. ChatGPT·Gemini 앱·claude.ai는 연결 불가(자막). Reset은 undo 없음, 언어는 시스템 언어로 돌아감.

### Ep 16 — More Screens: Stage Output Window and Layers Shown (4:30)

- **목표**: 두 번째 화면에 가사만 보내고, 가상 화면으로 모양을 준비하고, 온에어 목록·Layout board를 읽고, 분리/재연결을 안다.
- **끝나면 할 수 있는 것**: 관객 화면 + 무대 모니터를 한 무대에서 운용한다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 홀의 두 화면(관객: 영상+가사 / 무대 모니터: 검정 위 가사). 자막 "One stage. Each screen shows the layers you choose." Settings › Stage › Virtual screens: Portrait 1080 추가 → Screen 1에 선택 → 카드 세로 → 되돌림. | One stage, one set of seven layers. Monitors differ only in which layers they show. You cannot send different slides to different monitors. Virtual screens are sizes, not destinations. Add one and choose it for Screen 1 to prepare a portrait wall before you arrive. | `output/multi.md`; `output/index.md` (Virtual screens); `settings/index.md` |
| 0:35 | 컨트롤 로우 작은 슬라이더 버튼 → Stage output 창. + Add screen → Send to → 두 번째 모니터. ✎ "Stage". ON AIR 1/2. 휴지통 흐림 "On air — turn its power off first". | Screens are set up in the Stage output window. It is a window of its own; keep it open during the show. Press Add screen. Pick the second monitor under Send to. Click the pencil and name it Stage. New screens start with power on, so a plugged-in screen goes black at once. The trash is dimmed while on air. | `output/stage-window.md` (Opening; Adding, renaming, removing) |
| 1:30 | 상단 밴드에 02 "Stage" 타일. B OFF, 1–5 OFF. Background 슬라이드 송출: 관객=영상+가사, Stage=검정 위 가사. 전원 OFF 상태에서도 그림 표시. FG 슬라이드가 그림을 보이면 칩으로 Background. | A second tile appears. Only the stage tile has the layer column. Under each preview are the Layers shown cells. Turn B off on the Stage monitor, and the overlays. Send a slide with a video background: the audience sees everything, the stage sees words on black. The layer is still up; it is only hidden here. A tile shows its picture even while power is off. If a stage monitor still shows a picture, that slide is Foreground. Switch it to Background, or lock the whole presentation to Background, Episode 8. | `output/multi.md` (second tile; Layers shown); `help/index.md` (Layers shown and wrong-layer sends); `library/presentation-settings.md` (Layer for this list) |
| 2:25 | On air 칩 클릭 → 모니터 목록·전원 스위치·Stage output 버튼. 점(전부) vs 링(일부). 02 전원을 목록에서 OFF/ON. | The on-air chip lists every monitor with its power switch. A solid dot: every monitor you turned on is showing. A ring: only some, usually one unplugged. You can switch a monitor from this list, and open the Stage output window from its bottom. | `output/multi.md` (on-air list) |
| 3:15 | Layout board: 타일 배치, 리사이즈, Re-arrange. 선 상태(실선 오렌지/점선/희미한 점/회청). Stage 케이블 분리 → "not connected", 스위치 잠김 → 다시 연결 → 재개. | The Layout board is a picture for you; arrange it like your venue. It changes nothing about what goes out. Solid orange is on air. Dashed is power on with nothing out. Faint dots is off. Grey-blue is nowhere to go. Unplug a monitor: its row says not connected and the switch locks. Plug it back in and it resumes by itself. | `output/stage-window.md` (Layout board; nowhere to go) |
| 4:15 | 엔드 카드 + 로드맵 카드(16). | You can now run an audience screen and a stage monitor from one stage. Next: Episode 17 — Streaming Out: NDI, Syphon and Fill & Key. | — |

- **데모 자료**: 가상 디스플레이 2개("Projector", "Stage monitor"). Prize Night의 Background 슬라이드 + Foreground 슬라이드. 가사 프레젠테이션(배경 없음). 케이블 분리는 디스플레이 스크립트(불가하면 B-roll).
- **꼭 말할 주의점**: 새 화면 전원은 ON으로 시작. Layers shown OFF는 숨김, 지움 아님. 카드·에디터는 Screen 1 모양. 배경이 있는 Foreground 슬라이드는 B OFF여도 통째로 나감. 이 창의 설정은 이 컴퓨터에만 저장. Mac은 전원 ON 모니터를 1:1 해상도로 바꿈(Ep 3 자막 상기).

### Ep 17 — Streaming Out: NDI, Syphon and Fill & Key (Advanced) (5:00)

- **목표**: NDI/Syphon로 무대를 OBS나 스위처에 보내고, 스위처용 fill & key를 만든다.
- **끝나면 할 수 있는 것**: 스트리밍 PC나 스위처 위에 가사만 띄운다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: OBS 카메라 위에 가사가 떠 있음. Stage output 창. 자막 "A screen does not have to be a monitor." | A screen does not have to be a monitor. Under Network and apps, LayerCue sends the stage as a video stream. NDI goes over the network to OBS, vMix or a switcher. Syphon goes to an app on the same Mac. | `output/ndi-syphon.md` (Sending) |
| 0:30 | + Add screen › Send to › Network · apps › NDI®. Name "Summit Lyrics". Resolution 1920×1080, Frame rate 29.97. Alpha On · transparent. B OFF, 1–5 그대로. | Press Add screen. Under Network and apps, pick NDI. Name it; receivers see this name. Set the resolution and frame rate. Set Alpha to transparent. Turn B off. Now only words and overlays go out over the receiver's picture. | `output/ndi-syphon.md` (options) |
| 1:20 | 전원 ON → macOS Local Network 프롬프트 → Allow. 행 "On air · 1 receiving". 두 번째 VM의 OBS: NDI Source 목록에서 선택 → 카메라 위 가사. 자막 "Windows: allow LayerCue on Private networks." | Switch it on. The first time, allow the network permission. Decline it and other computers cannot find the stream. The row counts receivers. In OBS, pick the stream by name. The computer's name comes in front. | `output/ndi-syphon.md` (permissions); `help/index.md` (NDI) |
| 2:00 | Audio 행 Off → On, 슬라이더. 자막 "Audio over NDI: new in 0.9.12 — details in the What's New episode." Name 변경 → OBS에서 스트림 사라짐. | Audio, new in 0.9.12, puts the stage sound into the stream at its own level. Episode 19 goes through it. One warning: renaming while sending starts a new stream. Receivers must pick the new name again. | `output/ndi-syphon.md` (Audio; renaming); `output/sound.md` (Sound over NDI and SDI) |
| 2:30 | 같은 Mac의 OBS(Syphon Client). Send to › Syphon. 행 "A receiving app is connected". Alpha ▾ Premultiplied/Straight 전환. 자막 "Syphon: Mac only. Picture only." | On a Mac, Syphon hands the picture to an app on the same machine. It costs the CPU almost nothing. The row says when an app is connected. If letter edges look dark, switch between Premultiplied and Straight. | `output/ndi-syphon.md` (Syphon) |
| 3:05 | + Add fill & key. Fill=Virtual screen 1920×1080, Key=두 번째 가상 화면. Alpha. Fill/Key 타일: Key에 검정 위 흰 글자. 가사 송출, 페이드 중 두 타일 동기. | A switcher needs two signals. The fill is the picture. The key is a black-and-white matte. Press Add fill and key. Pick where the fill goes, then the key. Two virtual screens let you try it. The Key tile is white wherever something is drawn. Feed the switcher one resolution, or the key is drawn at the fill's shape. | `output/fill-key.md` (Adding; two outputs) |
| 4:05 | B ON → Key 전체 흰색 → B OFF → 글자만. | With B on, the background fills the frame: the key is all white. Turn B off and only the letters cut through the camera. | `output/fill-key.md` (key and the background layer) |
| 4:25 | Blackmagic 행 B-roll(매뉴얼 스크린샷): "· SDI" 선택 → Key 행 사라짐, SDI format, Keying External, Mix. 자막 "Blackmagic SDI: Mac only. Fill on SDI A, key on SDI B." | One Blackmagic SDI device can send fill and key together. Mac only. Set the SDI format before the show. | `output/fill-key.md` (Blackmagic); `help/index.md` (SDI) |
| 4:45 | 엔드 카드 + 로드맵 카드(17). | You can now put the stage over a camera in OBS or a switcher. Next: Episode 18 — Show Day. | — |

- **데모 자료**: 두 번째 VM의 NDI 수신기(OBS+NDI 또는 NDI Studio Monitor) → "1 receiving" 표시. 같은 Mac의 OBS(Syphon Client). 가상 디스플레이 2개(fill/key용). Blackmagic 행은 장비 없으면 매뉴얼 스크린샷 B-roll 20초. 가사 프레젠테이션(배경 없음) + Background 슬라이드 1장(B ON/OFF 대비용).
- **꼭 말할 주의점**: 네트워크 권한 거부 시 다른 컴퓨터가 스트림을 못 봄. 이름 변경은 새 스트림. NDI/SDI Audio는 마스터·MUTE·SOLO를 무시하고, YouTube 소리와 **Add video로 넣은 영상 박스의 소리는 포함되지 않음**(Ep 19에서 자세히). fill & key엔 NDI/Syphon 옵션 없음. 배경이 있는 Foreground 슬라이드는 B OFF여도 키를 채움. Blackmagic·Syphon은 Mac 전용; SDI format·Audio를 켜고 끄면 신호가 잠깐 끊김. 이 창의 설정은 이 컴퓨터에만 저장.

### Ep 18 — Show Day: Defaults, Lock, Messages and the Checklist (4:30)

- **목표**: 전날 점검 루틴, Lock editing while live, 기본값·오버레이 이름 사전 설정, 쇼 중 메시지 4종, 6항목 체크리스트, 팩다운.
- **끝나면 할 수 있는 것**: 반복 가능한 쇼 데이 루틴을 가진다.
- **구간표**

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | 콜드 오픈: 두 모니터 홀, "On air 2/2". 자막 "The day before". Settings › Files & YouTube › Import external files. Settings › Tools: LayerCue Check, YouTube tool Check. 상태 바 Update 칩 → 창 닫기(업데이트 안 함). | The day before. Press Import external files until every file is inside the media folder. Press Check on both Tools rows. If an update is out, read it, and leave it for after the event. Installing closes LayerCue and the audience screen goes dark. | `settings/index.md` (Import external files; updates); `start/install.md` (Updates) |
| 0:40 | 큐시트 전체를 실제 화면에서 한 번 돌림. 빨간 File missing → Locate file → Relinked. 빨간 트랙 → Relink file. YouTube 카드 "YouTube ↓" 확인. | Run the whole cue sheet once on the real screen. A red card: Locate file. A red track: Relink file. Confirm every YouTube card shows the arrow, or that the venue internet works. Listen to each video's level. | `start/first-show.md` (Before the event); `slides/index.md` (missing file); `music/index.md` |
| 1:25 | Settings › Stage: Lock editing while live ON → 송출 시 "Live — editing locked (unlock in the status bar)" → 드래그 거부 → 클릭은 송출. Default fades, Auto-dismiss. 03 Overlay names "Logo" → 칩 "1 Logo". | Turn on Lock editing while live. The first time you send with an output open, editing locks itself. Sending still works. It unlocks when every output is off; a lock you set by hand stays. Set Default fades and Auto-dismiss now, because changing them later changes the live show. Name your overlays: the number always comes first. | `settings/index.md` (Lock editing while live; Default fades; Overlay names); `slides/text.md` (When editing is locked); `output/layers.md` (naming overlays) |
| 2:15 | 카드 크기 L, Cmd+\ 사이드바 숨김, 피커. 창 배치 → Remember window layout. 연필로 수동 잠금. 자막 "Sidebar and Presentation settings are not covered by the lock." Tell us what's wrong: Question/Idea/Bug → Send. | Make the booth comfortable. Bigger cards. Hide the sidebar and jump with the picker. Arrange your windows; Remember window layout brings them back. Remember: the lock does not cover the sidebar or Presentation settings. Leave them alone. If LayerCue itself misbehaves, press Tell us what's wrong: Question, Idea or Bug, then Send. | `slides/index.md` (Card size); `library/index.md` (Hiding the sidebar); `settings/index.md`; `help/index.md` (Tell us what's wrong) |
| 2:45 | 메시지 카드 순서대로: "All monitors are off — turn one on with the power button above the preview" / "Foreground: can't play this —" / "Output screen disconnected — plug it back in and it comes right back". 자막만: "Several videos are playing — playback may stutter (more than three at once)". | Messages you may see. All monitors are off: you sent with no screen on. Can't play this: a file was dropped instead of freezing the screen. Output screen disconnected: a cable came out; it comes back by itself. A message tells you what happened and what to do. | `output/index.md` (Messages during a show) |
| 3:20 | 체크리스트 오버레이: 1 every monitor on, no "not connected", chip 2/2 · 2 Layers shown right · 3 no red cards · 4 YouTube downloaded or internet · 5 sound chain MUTE→master→device→layer→slide→music · 6 run the whole show once. | One more pass, in order. Every monitor on, no header says not connected. Each Layers shown strip lights the right layers. No red cards. YouTube downloaded, or internet checked. Sound, from MUTE down to the music. Then run the whole show once. Overlaps and music changes are caught only by eye and ear. | `help/index.md` (One more pass); `start/first-show.md` (checklist) |
| 3:55 | 팩다운: CLEAR → 음악 ■ → 전원 OFF → Cmd+Q → Quit. | After the closing slide: CLEAR. Stop the music. Switch the monitors off. Then quit. That order, every time. | `start/install.md` (Quitting); `output/index.md` |
| 4:15 | 시리즈 엔드 카드 + 로드맵(18 하이라이트) + What's New 슬롯. | You can now run a show from setup to packdown. Next: when a new version ships, a What's New episode joins this playlist. | `index.md` |

- **데모 자료**: 두 가상 디스플레이, USB 영상(Import external files 점등), 이름 바꾼 파일(File missing), 옮긴 음악 파일(빨간 트랙), 스테이지드 Update 칩, 스트리밍 YouTube 1장.
- **꼭 말할 주의점**: 쇼 중 업데이트 금지. 수동 잠금은 스스로 풀리지 않음. 카드 크기 키는 슬라이드 리스트 포커스 필요. 영상 4개 이상 동시 재생은 실제 컴퓨터에서 테스트(자막). 피드백은 일일 한도 있음.

---

## 4. 새 기능 편 템플릿 — "What's New in LayerCue 0.9.x"

**제목 형식**: `What's New in LayerCue 0.9.X: <feature in plain words>`. 한 릴리스당 1편, 큰 기능이 둘이면 2편(각 3–5분). 번호는 본편 뒤를 이어 19, 20… 두 플레이리스트에 모두 추가(본편 플레이리스트 끝 + "What's New in LayerCue").

**공통 규칙**: 본편과 같은 포맷·데모 라이브러리·140 wpm·짧은 문장(비트 20단어, 대본 15단어 상한)·4K·음악 베드·SRT·독립 엔드 카드 구간. 해당 릴리스에 실제로 출시된 기능만. 숨김/비활성 기능(name captions 등)은 절대 노출하지 않고, 재활성화되면 그때 자기 What's New 편을 받는다(본편에 소급 삽입 금지). **"name caption"/"title" 기능명 사용 금지** — 무대용 글자 띠는 항상 "lower third"/"overlay band", "caption"은 YouTube Captions(실제 UI 이름)에만. 새 컨트롤을 가리킬 땐 4영역 주문("Pick on the left… Adjust on the right")을 공간 앵커로 쓴다. 본편의 UI 이름/흐름이 바뀌면 재녹화 대신 **고정 댓글 "Since 0.9.X: <change>" + 엔드 스크린 카드**로 연결하고, 화면 흐름 자체가 달라졌을 때만 재녹화.

**필수 구간 (6–8 + 엔드 카드)**

| # | 시각 | 구간 | 내용 |
|---|---|---|---|
| 1 | 0:00 | Cold open | 결과가 무대에 떠 있는 장면 → 버전(Settings › Tools LayerCue 행 또는 시작 창). "LayerCue 0.9.X is out. Here is what changed." |
| 2 | ~0:20 | How to get it | Update 칩 → Get it(Mac: Open and quit / Windows: Store). "Never update mid-show." |
| 3 | ~0:40 | What changed, in one breath | changelog 한 줄을 쉬운 말로. 무엇을 대체/개선하는지, 무엇은 바뀌지 않았는지. |
| 4 | ~1:00 | Where to find it | 매뉴얼 영문 UI 이름으로 정확한 경로(Settings › page › row / 타이틀 바 버튼 / Stage output 행). 4영역 중 어디인지 한 문장. 툴팁 노출. Mac/Windows 차이 한 줄. |
| 5 | ~1:40 | Do it once, slowly | 가장 흔한 용례를 끝까지, 켜지는 표시 전부 보여주며. |
| 6 | ~2:50 | A second real case | 첫 사례가 컨퍼런스면 두 번째는 학교나 공연. |
| 7 | ~3:30 | What it does not change | 기본값, 저장 vs 임시, 컴퓨터별 vs 프레젠테이션별, Lock editing·undo 적용 여부. |
| 8 | ~3:55 | Pitfalls + which episode to rewatch | 매뉴얼에 적힌 함정만(플랫폼, 미저장, 온에어 민감, 종료-재실행 필요). "You met this panel in Episode N. From this version, …" 영향받은 본편 번호 → 고정 댓글 갱신 대상. 마무리 "Episode N stays correct except for …" 또는 "Nothing in the base series changes." |
| 9 | 마지막 15초 | End card | 규약 5와 동일: "You can now …" + 다음 편 또는 "Back to Episode 1 if you are new." |

**필드**: n, title, minutes, goal(한국어 한 문장: "<기능>을 실제 쇼에서 쓴다."), prerequisites(기반 본편 번호), segments(t, on_screen, narration, manual_refs = 갱신된 매뉴얼 페이지 + changelog 항목), demo_assets, pitfalls_to_mention. 영어 문장은 title·narration·on-screen·엔드 카드 문구("You can now …")에만. 오디오 파일 명명은 본편과 동일(`e19-s04-l03`).

**예시 — Episode 19: "What's New in LayerCue 0.9.12: Sound Over NDI and SDI, and Four Smaller Changes" (4:30)**
선수 회차: 9, 15, 17. 목표: NDI 스트림에 무대 소리를 함께 보내고, 작은 변경 4가지를 쓴다.

| 시각 | 화면 | 내레이션 비트 (EN) | 매뉴얼 |
|---|---|---|---|
| 0:00 | OBS에 가사+소리 도착. Settings › Tools에 0.9.12. | LayerCue 0.9.12 is out. The stage sound can now ride along with an NDI or SDI output. Here is what changed. | `changelog/index.md` |
| 0:20 | Update 칩 → Get it. 빨간 경고. | Press Update, then Get it. On a Mac, drag the new copy into Applications. Never update mid-show. | `start/install.md` (Updates) |
| 0:40 | changelog 줄 자막. | Before, an NDI stream carried only the picture. Now Audio can be On, with its own level. Monitors and Syphon still carry no sound. | `changelog/index.md`; `output/sound.md` |
| 1:00 | Stage output 창 → NDI 행 → Audio Off · On + 슬라이더(닫힌 행 "Audio 70%"). 자막 "Top band → Stage output window → the screen's row". | It lives in the Stage output window, in the NDI or Blackmagic screen's row. Audio is Off to begin with. Set it On and drag the volume. Watch the top. | `output/sound.md` (Sound over NDI and SDI) |
| 1:40 | Summit: NDI "Summit Lyrics" Audio On 70% → OBS 미터 움직임. MUTE 눌러도 스트림 소리 유지. Add video 박스 영상 송출 → OBS 미터 무반응. | Turn Audio on. OBS now shows level. Press MUTE: the room goes silent, the stream does not. This audio ignores the master, MUTE and SOLO. The slide's video and the music go in. YouTube sound and videos added with Add video do not, yet. | `output/sound.md` |
| 2:50 | Harbor City Choir: Blackmagic 행(B-roll) Audio On → SDI A. 자막 "Mac only". | On a Mac with a Blackmagic device, Audio rides SDI A, with the fill. Turning it on or off restarts the device output, so set it before the concert. | `output/fill-key.md`; `output/sound.md` |
| 3:30 | "What it does not change" 카드: 마스터/MUTE 무관, 미터에 안 보임, 이 컴퓨터에 저장, Lock editing 영향 없음. 이어서 4개 작은 변화 빠른 컷: Mac 메뉴 바(⌘, ⌘N ⌘W), 별도 창이 LayerCue가 있는 모니터에 열림/모니터 세트별 레이아웃, 선택 글자 Tracking, 커서 줄 Line height. | What it does not change: the meter, the master, MUTE. The level is saved on this computer, not in a cue sheet. Four smaller changes. The Mac gets a menu bar: Command comma for Settings. Separate windows open on LayerCue's monitor, and the layout is remembered per set of monitors. Tracking can apply to selected letters. Line height applies to the cursor's line. | `help/shortcuts.md` (Mac menu bar); `settings/index.md` (Remember window layout); `slides/text.md` |
| 3:55 | 함정 + 회차 매핑: Ep 17(NDI 행에 Audio 행 추가), Ep 2·6(메뉴 바), Ep 9(Tracking). | Pitfalls: a Blackmagic device drops the signal for a moment when Audio changes. Audio arrives some tens of milliseconds behind the picture. You met the NDI row in Episode 17; it now has an Audio row. Episode 9 stays correct; Tracking gained a per-letter case. Nothing else in the base series changes. | `output/sound.md`; `changelog/index.md` |
| 4:15 | 엔드 카드. | You can now send the stage sound with an NDI stream. New here? Back to Episode 1. | — |

(본편은 이미 0.9.12로 녹화되므로 이 예시는 템플릿 검증용. 실제 첫 What's New는 0.9.13부터.)

---

## 5. 제작 노트

**녹화 환경**
- 격리 샌드박스 macOS, 영문 UI, LayerCue 0.9.12 고정. 스크립트 드라이브(앱 상태를 코드로 세팅·조작) + 4K 무대 출력 녹화 + 앱 창 녹화(분할/PIP는 편집에서). 마우스 포인터 확대 + 클릭 링 효과.
- 샌드박스 디스플레이: "Projector 1920×1080"(외부로 등록) + "Stage monitor 1920×1080" + 메인 디스플레이 + 가상 화면. 케이블 분리/재연결은 디스플레이 스크립트로, 불가하면 B-roll.
- 가상 오디오 장치 "USB Audio Interface" 등록(Ep 12).
- **샌드박스 예외(격리 가정과 충돌하는 항목과 대책)**: Ep 2 설치 = 깨끗한 macOS/Windows VM에서 별도 B-roll 캡처 1회(Store 목록·버전 문자열·시작 창·작업표시줄 깜빡임 포함). Ep 2 Google 로그인 = 테스트 계정, 주소 블러, 가능하면 스테이지드 패널 상태. Ep 1 상태 바 = 최신 상태 그대로(Update 칩·렌치 점 없음), 내레이션이 조건부로 설명. Ep 13 = 샌드박스 인터넷 허용 **유일 회차**, 자체 CC 영상만 사용. Ep 15 AI 연결 = 샌드박스 전용 AI 앱·테스트 계정, 대화 내용 노출 없음, 응답 대기는 점프컷. Ep 17 NDI 수신 = 두 번째 VM의 OBS/NDI Studio Monitor; Syphon = 같은 Mac의 OBS; Blackmagic 행은 장비 없으면 매뉴얼 스크린샷 B-roll 20초. 모든 Update 칩/yt-dlp 업데이트 가능 상태는 스테이징(Ep 2·13·18만).
- 상태 저장: 블록마다 샌드박스 스냅샷을 찍어 다음 회차가 그 상태에서 시작(READ ME는 Ep 4 이후에도 삭제하지 않고 유지해 Block A/B 연속성 확보).

**녹화 블록과 순서** (공개 순서는 1→18 고정, 녹화 순서는 다름)
- Block A: Ep 2, 3 (신규 설치 상태, Tour 큐시트)
- Block B: Ep 4 → 5 → 6 → 7 → 8 (Summit 2026·Prize Night 라이브러리가 회차마다 자라므로 순서대로)
- Block C: Ep 9, 10 (에디터, Harbor City Choir + Summit 타이틀)
- Block D: Ep 11, 12 (재생목록·가상 오디오 장치 공유)
- Block E: Ep 13, 14, 15 (13만 인터넷; 15는 완성 폴더 필요)
- Block F: Ep 16, 17 (가상 디스플레이 2 + NDI 수신기 + Syphon OBS)
- Block G: Ep 18, **그리고 Ep 1 마지막**(완성된 데모 라이브러리로 콜드 오픈 촬영)

**데모 데이터셋(1회 제작, 전 회차 재사용)**
- 라이브러리 `Summit 2026`: Welcome loop(추상 루프 mp4 ×2), Welcome words(텍스트 3), Summit logo(PNG), Keynote — Dana Okafor(Keynote-Okafor.pptx 24장: 표1·차트1·숨김1·Windows 폰트1), Sponsor thanks(로어서드 2), Sponsor videos(YouTube 2), 사진 summit-hall/sponsor-wall/crowd/dana-okafor-portrait, keynote-intro.mp4, keynote-clip-speech.mp4, backstage-vertical.mp4(9:16), Summit-Programme.pdf(6쪽).
- 라이브러리 `Northfield Academy`: Prize Night 2026(stage-wash.mp4 루프 BG, 수상 부문 텍스트 8, school-crest.png, sponsor-mark.png, 오버레이 3용 텍스트 띠 1, highlights.mp4 앞 2초 검정+크레딧, applause-sting.wav), 슬라이드 텍스트 "Doors open 18:30".
- 라이브러리 `Harbor City Choir`: Spring Concert(choir-stage.jpg, 프로그램 노트 4단락 텍스트 — 한 단락은 Split into slides용으로 길게, 가사 길이 다른 3장, Merge N into one용 짧은 카드 3장, 일괄 스타일용 텍스트 20장).
- 음악: 가상 제목 6곡(Open Doors, Lobby Light, Interval, Quiet Hall, Walk-up, Closing Theme; 1곡은 말 인트로), 폴더 Pre-show/Break.
- 고장 유발 파일: 외부에서 이름 바꾼 영상 1(File missing), 옮긴 음악 1(빨간 트랙), USB 경로 sponsor-reel.mp4, 거부용 notes.txt.
- 큐시트: Summit Day 1, Prize Night.
- 인물/단체 전부 가상. 경쟁 제품·가격 금지. 모든 사진/영상은 자체 제작 또는 CC0.

**내레이션 워크플로**
1. 이 문서의 비트를 **15단어 이하 문장**으로 풀어 최종 대본 작성(한 줄 = 한 문장). **비트 문장도 20단어 상한** — 넘는 비트는 이 문서 단계에서 미리 쪼갠다. 매뉴얼 UI 이름은 그대로.
2. 단어수 게이트: 구간 단어수 ≤ 초÷60×140×0.85. 엔드 카드 구간은 두 문장만. 초과 시 자르거나 분할. 통과 전 녹음 금지.
3. 줄별 음성 생성, 파일명 `e07-s04-l03.wav`(회차-구간-줄). UI 이름이 바뀌면 그 줄만 재생성.
4. 녹화 전 **사실 검증 체크리스트**(심사 지적 반영): 버전 주장 3건은 매뉴얼 노트와 대조 완료 — "Mac 메뉴 바 = 0.9.12"(`help/shortcuts.md`, changelog), "선택 글자 Tracking = 0.9.12"(changelog), "0.9.10 이전 Windows는 업데이트 미확인"(`start/install.md`). 플랫폼 한정 주장: "once a day 자동 확인 = Mac"(`settings/index.md` platform notes). Store 버전 문자열 "1.9.12.0"은 녹화 전 Store 목록 캡처로 확인(매뉴얼 예시는 0.9.10 → 1.9.10.0). 그 외 Esc 알림 문구, "Clear All does not stop the music", undo 50단계, 배경 볼륨 0%, 첫 실행 Screen 1 자동 선택, Stage output 창 0.9.10 도입, NDI/SDI Audio 제외 항목(YouTube·Add video)도 매뉴얼 원문 재확인 후 녹음.
5. 데모 멈춤은 대본에 `[pause 2s]`로 명시(AI 응답 대기는 `[pause]` + 점프컷); 음악 베드는 내레이션 아래 −18 dB, 멈춤 구간에서 −12 dB.

**자막(SRT)**: 줄별 음성 타이밍에서 생성, 한 문장 = 한 큐, 최대 2줄, 데모 멈춤 뒤 300 ms 패딩. 영어 자막 기본; 한국어/일본어 번역 자막은 같은 큐 타이밍에 올림. "내레이션 없음, 자막만" 항목(Ep 3 Mac 해상도, Ep 4 Find 드래그, Ep 13 종료·재실행, Ep 15 AI 앱 이름, Ep 18 Several videos)은 하단 로어서드 자막으로만.

**썸네일**: 통일 템플릿 — 좌측 큰 회차 번호, 우측 그 회차의 무대 결과 스틸, 하단 짧은 제목(3–5단어, 예 "Screen On, Slide Out"). Advanced 회차(17)와 What's New는 코너 배지. 얼굴·과장 표정 없음.

**YouTube 설정**: 챕터 = 구간 시각 + 명사구(엔드 카드 구간은 "What's next"). 설명란 고정 문구(1장 참조) + 매뉴얼 URL(`/docs/start/…`, `/docs/library/…`, `/docs/slides/…`, `/docs/output/…`, `/docs/music/…`, `/docs/import/…`, `/docs/ai/…`, `/docs/settings/…`, `/docs/help/…`). Ep 1 = 플레이리스트 트레일러·채널 고정. 모든 설명에 "Lost? Start with Episode 1."

**공개 주기**: 주 1편, 고정 요일, 18주. Ep 1·2·3을 첫 주에 함께 공개하는 안도 허용(시청자가 즉시 첫 쇼까지 도달) — 그 경우 Ep 4부터 주 1편. 절대 순서 변경 금지(Ep 3이 안전 회차). What's New는 버전 출시 후 2주 안에, 매뉴얼 페이지와 changelog 갱신 뒤에 공개.

**유지보수**: 채널 노트에 아래 6장의 "매뉴얼 ↔ 회차" 표를 복제해 두고, 매뉴얼 페이지가 수정되면 해당 회차 대본·고정 댓글을 점검. UI 이름·흐름 변경 → 고정 댓글 "Since 0.9.X: …" + 카드. 구간의 1/3 이상이 틀려질 때만 재녹화.

---

## 6. 매뉴얼 대조표

경로 기준: `/Users/kj1212/projects/layercue-site/src/content/docs/docs/` (changelog는 `/Users/kj1212/projects/layercue-site/src/content/docs/changelog/index.md`). 굵은 숫자 = 주 담당 회차.

| 매뉴얼 페이지 | 다루는 회차 |
|---|---|
| `index.md` (LayerCue is, layers, Tell us what's wrong) | **1**, 6, 18 |
| `start/install.md` | **2**, 3(Quitting 상기), 18(Updates) |
| `start/tour.md` | **1**, 3, 5, 6, 9, 15(Narrow window) |
| `start/first-show.md` | **3**, 4, 7, 8, 11, 12, 18(checklist) |
| `library/index.md` | **4**, 6(Lock editing does not cover the sidebar), 14, 18(Hiding the sidebar) |
| `library/find.md` | **4** |
| `library/presentation-settings.md` | **8**, 16(Layer for this list 상기) |
| `slides/index.md` | **5**, **6**, 9(Text slides in the list: Merge N into one), 10(Paste style), 14, 18 |
| `slides/text.md` | **9**, 10, 13(editor pitfalls), 14, 18(When editing is locked) |
| `slides/design.md` | **10** |
| `slides/settings.md` | **7**, 13 |
| `slides/youtube.md` | **13**, 5(Link 언급) |
| `output/index.md` | **3**(Choosing the screen; First launch; Mac 1:1 자막), 6(live indicators; Locking), 16(Virtual screens), 18(Messages) |
| `output/layers.md` | 1, 3, **6**(The seven layers; chip; Overlays), 8, 18(Overlay names) |
| `output/stage-window.md` | **16** |
| `output/multi.md` | **16**, 13(YouTube on several monitors) |
| `output/sound.md` | 7, **12**, 17(Sound over NDI and SDI 소개), 19(예시) |
| `output/fill-key.md` | **17** |
| `output/ndi-syphon.md` | **17** |
| `music/index.md` | **11**, 15(narrow), 18(Relink) |
| `import/powerpoint.md` | **14** |
| `import/pdf.md` | **14** |
| `ai/index.md` | **15** |
| `settings/index.md` | 2(General, Tools, sign-in, Windows Store updates), 8(Default fades), 11(Music), 12(Remember master volume), 13(YouTube, Tools), **15**(Media folder, Import external files, Import bundle, Account, Reset, Remember window layout), 16(Virtual screens, Output monitors), **18**(Lock editing while live, Overlay names) |
| `help/index.md` | 3(Nothing reaches the audience; covered screen), 4(Undo), 5(Locate file), 12(No sound), 13(YouTube on stage), 14(import messages), 16(Layers shown), 17(NDI/SDI), **18**(One more pass; Tell us what's wrong) |
| `help/files.md` | 2(folder location), **15** |
| `help/shortcuts.md` | 2·6(Mac menu bar — 6은 설명란), 3(Clear keys, Esc), 4(Find), 5(paste), 6(Moving through slides), 7(frame step), 9(Number fields, Split/join, eyedropper), 10(editor keys, drawing hints) |
| `changelog/index.md` (0.9.8–0.9.12) | 2(menu bar), 9(Tracking on selection), 17(NDI Audio 소개), **19**(What's New 예시), 템플릿 |

의도적으로 제외: 숨김 기능(name captions/titles), 0.9.12에 없는 기능(선 툴 등), 경쟁사 비교. 설명란/고정 댓글로만 내린 advanced 항목: SVG 붙이기·Box roles(`slides/design.md`, Ep 10 주의점).
