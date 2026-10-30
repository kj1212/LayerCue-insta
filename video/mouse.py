#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""촬영용 마우스 — Quartz 로 진짜 포인터를 움직이고 누른다. 움직인 자취는 적어 두어(JSON) 편집에서 큰 포인터·클릭 링을 그린다.

    from mouse import M
    m = M()                      # 좌표는 LG 화면 캡처(3840×2160 px) 기준 — 창 캡처가 아니라 화면 캡처
    m.move(1200, 900, 0.8)       # 0.8 s 에 걸쳐 부드럽게(ease-in-out)
    m.click(1200, 900)           # 옮겨 가서 누른다
    m.save("rec/ep01-s03.mouse.json")

화면 캡처 픽셀 → 전역 포인트: LG 는 (-67, -1080) 에서 시작하고 2배 화소다.
"""
import json, math, os, time
import Quartz, AppKit

def lg_origin():
    """LG 화면의 왼쪽 위(전역 포인트, Quartz 좌표)와 화소 배율 — 배치·모드가 바뀌어도 그때그때 읽는다."""
    screens = AppKit.NSScreen.screens(); H = screens[0].frame().size.height
    for sc in screens:
        if "LG" in str(sc.localizedName()):
            f = sc.frame(); return (f.origin.x, H - (f.origin.y + f.size.height), float(sc.backingScaleFactor()))
    raise SystemExit("LG display not found")


LG_X, LG_Y, SCALE = lg_origin()
# MOUSE_WIN="x,y,w,h" (전역 포인트) — 창을 LG 가 아닌 곳(3편: 맥북)에 둘 때. 좌표는 그대로 "LG 캡처 px"(3840×2160, 위 60 px 는 메뉴 막대)로 쓰고
# 창 크기에 맞춰 늘려 읽는다 → 녹화본도 같은 꼴(3840×2100 + 위 60)로 맞추면 연출표·영역표를 그대로 쓴다.
WIN = [float(v) for v in os.environ["MOUSE_WIN"].split(",")] if os.environ.get("MOUSE_WIN") else None


class M:
    def __init__(self, log=True):
        # 송출 창이 LG 를 덮는 동안(무대 녹화)은 macOS 가 LG 를 원래 해상도(배율 1)로 바꾼다 — 그때는 마우스를 안 쓴다
        if SCALE != 2 and not os.environ.get("MOUSE_ANY_SCALE") and not WIN:
            raise SystemExit(f"LG display is not in HiDPI mode (scale {SCALE}) — set it to 1920×1080 first")
        self.events = []; self.t0 = time.time(); self.log = log

    # ── 좌표 ──
    @staticmethod
    def g(px, py):
        if WIN: return (WIN[0] + px * WIN[2] / 3840, WIN[1] + (py - 60) * WIN[3] / 2100)
        return (LG_X + px / SCALE, LG_Y + py / SCALE)

    def where(self):
        p = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
        if WIN: return ((p.x - WIN[0]) * 3840 / WIN[2], (p.y - WIN[1]) * 2100 / WIN[3] + 60)
        return ((p.x - LG_X) * SCALE, (p.y - LG_Y) * SCALE)

    # ── 기록 ──
    def _rec(self, kind, px, py):
        if self.log: self.events.append({"t": round(time.time() - self.t0, 3), "k": kind, "x": round(px), "y": round(py)})

    def mark(self, label):
        """녹화 시작 같은 기준점을 적어 둔다."""
        self._rec("mark:" + label, *self.where())

    def save(self, path):
        json.dump(self.events, open(path, "w"))

    # ── 동작 ──
    def _post(self, kind, px, py, button=Quartz.kCGMouseButtonLeft):
        e = Quartz.CGEventCreateMouseEvent(None, kind, self.g(px, py), button)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, e)

    def jump(self, px, py):
        self._post(Quartz.kCGEventMouseMoved, px, py); self._rec("move", px, py)

    def move(self, px, py, dur=0.7, fps=120):
        """ease-in-out 으로 옮긴다 — 사람 손처럼 처음과 끝이 느리다."""
        x0, y0 = self.where(); n = max(2, int(dur * fps))
        for i in range(1, n + 1):
            s = i / n; s = 0.5 - 0.5 * math.cos(math.pi * s)
            self._post(Quartz.kCGEventMouseMoved, x0 + (px - x0) * s, y0 + (py - y0) * s)
            time.sleep(dur / n)
        self._rec("move", px, py)

    def click(self, px, py, dur=0.7, hold=0.08):
        self.move(px, py, dur); time.sleep(0.12)
        self._post(Quartz.kCGEventLeftMouseDown, px, py); self._rec("down", px, py)
        time.sleep(hold)
        self._post(Quartz.kCGEventLeftMouseUp, px, py); self._rec("up", px, py)

    def cmd_click(self, px, py, dur=0.6):
        """⌘ 를 누른 채 클릭(여러 장 고르기) — ⌘ 키를 실제로 눌렀다 뗀다(마우스 이벤트 플래그만으로는 Qt 가 못 읽었다)."""
        self.move(px, py, dur); time.sleep(0.1)
        F = Quartz.kCGEventFlagMaskCommand
        k = Quartz.CGEventCreateKeyboardEvent(None, 55, True); Quartz.CGEventSetFlags(k, F); Quartz.CGEventPost(Quartz.kCGHIDEventTap, k); time.sleep(0.06)
        for kind in (Quartz.kCGEventLeftMouseDown, Quartz.kCGEventLeftMouseUp):
            e = Quartz.CGEventCreateMouseEvent(None, kind, self.g(px, py), Quartz.kCGMouseButtonLeft)
            Quartz.CGEventSetFlags(e, F); Quartz.CGEventPost(Quartz.kCGHIDEventTap, e); time.sleep(0.08)
        k = Quartz.CGEventCreateKeyboardEvent(None, 55, False); Quartz.CGEventSetFlags(k, 0); Quartz.CGEventPost(Quartz.kCGHIDEventTap, k)
        self._rec("down", px, py)

    def double_click(self, px, py, dur=0.7):
        self.move(px, py, dur); time.sleep(0.12)
        for n in (1, 2):
            e = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, self.g(px, py), Quartz.kCGMouseButtonLeft)
            Quartz.CGEventSetIntegerValueField(e, Quartz.kCGMouseEventClickState, n); Quartz.CGEventPost(Quartz.kCGHIDEventTap, e)
            e = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, self.g(px, py), Quartz.kCGMouseButtonLeft)
            Quartz.CGEventSetIntegerValueField(e, Quartz.kCGMouseEventClickState, n); Quartz.CGEventPost(Quartz.kCGHIDEventTap, e)
            time.sleep(0.06)
        self._rec("dbl", px, py)

    def right_click(self, px, py, dur=0.7):
        self.move(px, py, dur); time.sleep(0.12)
        self._post(Quartz.kCGEventRightMouseDown, px, py, Quartz.kCGMouseButtonRight); time.sleep(0.08)
        self._post(Quartz.kCGEventRightMouseUp, px, py, Quartz.kCGMouseButtonRight); self._rec("rclick", px, py)

    def drag(self, x1, y1, x2, y2, dur=1.0, fps=120):
        self.move(x1, y1, 0.6); time.sleep(0.15)
        self._post(Quartz.kCGEventLeftMouseDown, x1, y1); self._rec("down", x1, y1); time.sleep(0.2)
        n = max(2, int(dur * fps))
        for i in range(1, n + 1):
            s = i / n; s = 0.5 - 0.5 * math.cos(math.pi * s)
            self._post(Quartz.kCGEventLeftMouseDragged, x1 + (x2 - x1) * s, y1 + (y2 - y1) * s); time.sleep(dur / n)
        time.sleep(0.15); self._post(Quartz.kCGEventLeftMouseUp, x2, y2); self._rec("up", x2, y2)

    def slow_drag(self, x1, y1, x2, y2, hold=1.2, dur=1.0, fps=120):
        """끌어서 목표 위에 hold 초 머문 뒤 놓는다(카드 한가운데 교체 · Copy 배지를 보여 줄 때)."""
        self.move(x1, y1, 0.5); time.sleep(0.15)
        self._post(Quartz.kCGEventLeftMouseDown, x1, y1); self._rec("down", x1, y1); time.sleep(0.2)
        n = max(2, int(dur * fps))
        for i in range(1, n + 1):
            s = i / n; s = 0.5 - 0.5 * math.cos(math.pi * s)
            self._post(Quartz.kCGEventLeftMouseDragged, x1 + (x2 - x1) * s, y1 + (y2 - y1) * s); time.sleep(dur / n)
        for i in range(int(hold * 30)):
            self._post(Quartz.kCGEventLeftMouseDragged, x2 + (i % 2), y2); time.sleep(1 / 30)
        self._post(Quartz.kCGEventLeftMouseUp, x2, y2); self._rec("up", x2, y2)

    def hover(self, px, py, dur=0.7, stay=1.5):
        self.move(px, py, dur); self._rec("hover", px, py); time.sleep(stay)

    def type_text(self, text, gap=0.06):
        """글자를 사람처럼 한 자씩 친다 — System Events keystroke 를 **한 번의** osascript 안에서 돌린다.
        (예전엔 글자마다 osascript 를 새로 띄워 한 자 0.18 s — 4편에서 뒤 동작이 2 초씩 밀렸다)"""
        import subprocess
        esc = text.replace("\\", "\\\\").replace('"', '\\"')
        subprocess.run(["osascript", "-e", 'tell application "System Events"', "-e",
                        'repeat with c in characters of "%s"' % esc, "-e", "keystroke c", "-e", "delay %s" % gap, "-e", "end repeat", "-e", "end tell"])
        self._rec("type", *self.where())

    def lg_move(self, fx, fy, dur=0.9, click=False, fps=120):
        """LG 화면(송출 창이 덮고 있는 화면) 위 — 좌표는 LG 의 비율(0–1). 3편: 송출 위 둥근 ✕. 클릭 링은 그리지 않는다(창 밖)."""
        # ★ NSScreen 은 이벤트 루프 없는 프로세스에서 처음 값을 그대로 쥐고 있다 — 송출을 켜 LG 가 1:1 로 바뀐 뒤에도 옛 크기로 계산해
        #   ✕ 대신 엉뚱한 곳을 눌렀다. Quartz 의 CGDisplayBounds 는 늘 지금 값(전역, 왼쪽 위 기준)
        ids = Quartz.CGGetActiveDisplayList(8, None, None)[1]
        d = [i for i in ids if not Quartz.CGDisplayIsMain(i)][0]; b = Quartz.CGDisplayBounds(d)
        tx, ty = b.origin.x + fx * b.size.width, b.origin.y + fy * b.size.height
        p = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None)); n = max(2, int(dur * fps))
        for i in range(1, n + 1):
            k = 0.5 - 0.5 * math.cos(math.pi * i / n)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (p.x + (tx - p.x) * k, p.y + (ty - p.y) * k), 0))
            time.sleep(dur / n)
        if click:
            # ✕ 는 마우스가 움직일 때만 잠깐 뜬다 — 옆에서 다시 다가가 곧바로 누른다(가만히 기다리면 사라져 안 눌렸다)
            for k in range(1, 25):
                Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (tx - 40 + 40 * k / 24, ty + 30 - 30 * k / 24), 0)); time.sleep(0.012)
            time.sleep(0.15)
            for kind in (Quartz.kCGEventLeftMouseDown, Quartz.kCGEventLeftMouseUp):
                Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateMouseEvent(None, kind, (tx, ty), Quartz.kCGMouseButtonLeft)); time.sleep(0.08)
        if self.log: self.events.append({"t": round(time.time() - self.t0, 3), "k": "lg", "x": fx, "y": fy})

    def key(self, keycode, cmd=False, shift=False, alt=False):
        """키 하나 — Quartz 키코드(예: Esc 53, Return 36, 1 → 18)."""
        flags = 0
        if cmd: flags |= Quartz.kCGEventFlagMaskCommand
        if shift: flags |= Quartz.kCGEventFlagMaskShift
        if alt: flags |= Quartz.kCGEventFlagMaskAlternate
        for down in (True, False):
            e = Quartz.CGEventCreateKeyboardEvent(None, keycode, down)
            if flags: Quartz.CGEventSetFlags(e, flags)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, e); time.sleep(0.04)
        self._rec("key:%d" % keycode, *self.where())
