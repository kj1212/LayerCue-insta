#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""촬영용 마우스 — Quartz 로 진짜 포인터를 움직이고 누른다. 움직인 자취는 적어 두어(JSON) 편집에서 큰 포인터·클릭 링을 그린다.

    from mouse import M
    m = M()                      # 좌표는 LG 화면 캡처(3840×2160 px) 기준 — 창 캡처가 아니라 화면 캡처
    m.move(1200, 900, 0.8)       # 0.8 s 에 걸쳐 부드럽게(ease-in-out)
    m.click(1200, 900)           # 옮겨 가서 누른다
    m.save("rec/ep01-s03.mouse.json")

화면 캡처 픽셀 → 전역 포인트: LG 는 (-67, -1080) 에서 시작하고 2배 화소다.
"""
import json, math, time
import Quartz, AppKit

def lg_origin():
    """LG 화면의 왼쪽 위(전역 포인트, Quartz 좌표)와 화소 배율 — 배치·모드가 바뀌어도 그때그때 읽는다."""
    screens = AppKit.NSScreen.screens(); H = screens[0].frame().size.height
    for sc in screens:
        if "LG" in str(sc.localizedName()):
            f = sc.frame(); return (f.origin.x, H - (f.origin.y + f.size.height), float(sc.backingScaleFactor()))
    raise SystemExit("LG display not found")


LG_X, LG_Y, SCALE = lg_origin()
if SCALE != 2:
    raise SystemExit(f"LG display is not in HiDPI mode (scale {SCALE}) — set it to 1920×1080 first")


class M:
    def __init__(self, log=True):
        self.events = []; self.t0 = time.time(); self.log = log

    # ── 좌표 ──
    @staticmethod
    def g(px, py):
        return (LG_X + px / SCALE, LG_Y + py / SCALE)

    def where(self):
        p = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
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

    def hover(self, px, py, dur=0.7, stay=1.5):
        self.move(px, py, dur); self._rec("hover", px, py); time.sleep(stay)

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
