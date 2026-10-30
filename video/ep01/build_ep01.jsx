// 1편 조립 엔진 — ep01/timeline.js (var TL) 를 읽어 AE 에서 3840×2160 · 30 fps 컴프를 짓고 렌더 대기열에 넣는다.
//   OUT_NAME=layercue-ep01 ./ae.sh ep01/build_ep01        (ae.sh 가 ROOT · OUT_DIR · OUT_NAME 을 앞에 붙인다)
// TL 의 구조는 ep01/assemble.py 가 만든다:
//   clips      창 녹화(LG 화면 캡처 3840×2160) — [t0, t1) 에 file 을 in 초부터. 위 60 px(메뉴 막대)는 마스크로 가린다
//   zoomKeys   Screen 층의 [시각, 배율, [x, y]] 키프레임 — 창 영역을 화면 가운데로 키운다
//   highlights 창 픽셀 영역에 둥근 테(색) + 바깥을 어둡게(dim)
//   captions   아래쪽 자막 PNG · full  전체 화면 소스(콜드 오픈 무대 영상 · 카드) · clicks 클릭 링 · voice 줄별 음성 · music 패드
// ★ 테·링·어둡게 층은 Screen 층의 자식이라(parent) 줌을 따라간다 — 자식의 위치는 Screen 좌표(창 px, y+60).

var P, comp, S;
var BG = [12 / 255, 13 / 255, 17 / 255];
var COLORS = { indigo: [123 / 255, 124 / 255, 246 / 255], amber: [232 / 255, 163 / 255, 58 / 255],
               green: [76 / 255, 192 / 255, 107 / 255], white: [242 / 255, 238 / 255, 228 / 255], orange: [255 / 255, 74 / 255, 26 / 255] };
$.evalFile(ROOT + "/ep01/timeline.js");

function imp(path) { return P.importFile(new ImportOptions(new File(path))); }
function easeAll(prop) {
    var n = 1, t = prop.propertyValueType;
    if (t === PropertyValueType.TwoD) n = 2;
    if (t === PropertyValueType.ThreeD) n = 3;
    var e = []; for (var i = 0; i < n; i++) e.push(new KeyframeEase(0, 70));
    for (var k = 1; k <= prop.numKeys; k++) {
        prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER);
        prop.setTemporalEaseAtKey(k, e, e);
    }
}
function keys(prop, list) { for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]); easeAll(prop); }
function T(L) { return L.property("ADBE Transform Group"); }
function fade(L, t0, t1, fin, fout, max) {
    var m = (max === undefined) ? 100 : max, list = [];
    if (fin > 0) { list.push([t0, 0]); list.push([t0 + fin, m]); } else list.push([t0, m]);
    if (fout > 0) { list.push([t1 - fout, m]); list.push([t1, 0]); }
    keys(T(L).property("ADBE Opacity"), list);
}
function rectMask(L, x0, y0, x1, y1, inverted, feather) {
    var sh = new Shape(); sh.vertices = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]; sh.closed = true;
    var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    m.property("ADBE Mask Shape").setValue(sh); m.inverted = !!inverted;
    if (feather) m.property("ADBE Mask Feather").setValue([feather, feather]);
}
function roundMask(L, x, y, w, h, r, inverted) {
    var k = r * 0.5523, sh = new Shape();
    sh.vertices = [[x + r, y], [x + w - r, y], [x + w, y + r], [x + w, y + h - r], [x + w - r, y + h], [x + r, y + h], [x, y + h - r], [x, y + r]];
    sh.inTangents = [[-k, 0], [0, 0], [0, -k], [0, 0], [k, 0], [0, 0], [0, k], [0, 0]];
    sh.outTangents = [[0, 0], [k, 0], [0, 0], [0, k], [0, 0], [-k, 0], [0, 0], [0, -k]];
    sh.closed = true;
    var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    m.property("ADBE Mask Shape").setValue(sh); m.inverted = !!inverted;
}
// Screen 층의 자식으로 붙인다 — parent= 는 세계 위치를 지키므로 쉬는 상태의 컴프 좌표(창 px 의 y 에 30)를 준다
function childAt(L, x, y) { T(L).property("ADBE Position").setValue([x, y]); L.parent = S; }

app.beginSuppressDialogs();
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.newProject();
P = app.project;
comp = P.items.addComp(TL.name, 3840, 2160, 1, TL.duration, TL.fps);
comp.bgColor = BG;
var bgSolid = comp.layers.addSolid(BG, "backdrop", 3840, 2160, 1, TL.duration);

// ── 창 녹화 → Screen 프리컴프 ──
var scr = P.items.addComp("Screen", 3840, 2160, 1, TL.duration, TL.fps);
scr.bgColor = BG;
var i, L;
for (i = 0; i < TL.clips.length; i++) {
    var c = TL.clips[i];
    L = scr.layers.add(imp(c.file)); L.startTime = c.t0 - (c["in"] || 0); L.inPoint = c.t0; L.outPoint = c.t1;
    rectMask(L, 0, 60, 3840, 2160, false, 0);          // 메뉴 막대를 가린다
    if (c.fadeIn) fade(L, c.t0, c.t1, c.fadeIn, 0);
}
S = comp.layers.add(scr); S.startTime = 0; S.name = "Screen";
T(S).property("ADBE Position").setValue([1920, 1050]);   // 창(3840×2100)이 위아래 30 px 여백으로 가운데
if (TL.zoomKeys && TL.zoomKeys.length) {
    var sk = [], pk = [];
    for (i = 0; i < TL.zoomKeys.length; i++) { sk.push([TL.zoomKeys[i][0], [TL.zoomKeys[i][1] * 100, TL.zoomKeys[i][1] * 100]]); pk.push([TL.zoomKeys[i][0], TL.zoomKeys[i][2]]); }
    keys(T(S).property("ADBE Scale"), sk); keys(T(S).property("ADBE Position"), pk);
}

// ── 어둡게 + 둥근 테 ──
for (i = 0; i < TL.highlights.length; i++) {
    var h = TL.highlights[i], r = h.rect, col = COLORS[h.color || "indigo"];
    var compSpace = (h.space === "comp"), oy = compSpace ? 0 : 60;      // 마스크(층 좌표)는 Screen 안에서 y+60
    if (h.dim) {
        var D = comp.layers.addSolid([0, 0, 0], "dim", 3840, 2160, 1, TL.duration);
        D.inPoint = h.t0; D.outPoint = h.t1;
        roundMask(D, r[0] - 8, r[1] + oy - 8, r[2] + 16, r[3] + 16, Math.min(28, (r[3] + 16) / 3), true);
        if (compSpace) T(D).property("ADBE Position").setValue([1920, 1080]); else childAt(D, 1920, 1050);   // Screen 내용은 컴프에서 30 px 위에 있다
        fade(D, h.t0, h.t1, 0.3, 0.3, h.dim === true ? 55 : h.dim);
    }
    var H = comp.layers.addShape(); H.name = "hl " + (h.name || i); H.inPoint = h.t0; H.outPoint = h.t1;
    var g = H.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"), v = g.property("ADBE Vectors Group");
    var pad = (r[3] < 60) ? 5 : 8;                                  // 작은 셀은 여유를 줄여 옆 셀을 건드리지 않게
    var rc = v.addProperty("ADBE Vector Shape - Rect");
    rc.property("ADBE Vector Rect Size").setValue([r[2] + 2 * pad, r[3] + 2 * pad]);
    rc.property("ADBE Vector Rect Roundness").setValue(Math.min(28, (r[3] + 2 * pad) / 3));
    var st = v.addProperty("ADBE Vector Graphic - Stroke");
    st.property("ADBE Vector Stroke Color").setValue(col); st.property("ADBE Vector Stroke Width").setValue(h.width || 9);
    if (h.fill) { var fi = v.addProperty("ADBE Vector Graphic - Fill"); fi.property("ADBE Vector Fill Color").setValue(col); fi.property("ADBE Vector Fill Opacity").setValue(h.fill); }
    if (compSpace) T(H).property("ADBE Position").setValue([r[0] + r[2] / 2, r[1] + r[3] / 2]);
    else childAt(H, r[0] + r[2] / 2, r[1] + 30 + r[3] / 2);     // parent= 는 세계 위치를 지킨다 → 컴프 좌표(창 y+30)로
    fade(H, h.t0, h.t1, 0.25, 0.25);
}

// ── 클릭 링 ──
for (i = 0; i < TL.clicks.length; i++) {
    var k = TL.clicks[i], K = comp.layers.addShape(); K.name = "click"; K.inPoint = k.t; K.outPoint = k.t + 0.5;
    var kg = K.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"), kv = kg.property("ADBE Vectors Group");
    var el = kv.addProperty("ADBE Vector Shape - Ellipse");
    keys(el.property("ADBE Vector Ellipse Size"), [[k.t, [24, 24]], [k.t + 0.45, [190, 190]]]);
    var ks = kv.addProperty("ADBE Vector Graphic - Stroke");
    ks.property("ADBE Vector Stroke Color").setValue(COLORS.white); ks.property("ADBE Vector Stroke Width").setValue(8);
    childAt(K, k.x, k.y + 30); keys(T(K).property("ADBE Opacity"), [[k.t, 90], [k.t + 0.45, 0]]);
}

// ── 전체 화면 소스(콜드 오픈 무대 · 카드) — Screen 위에 ──
for (i = 0; i < TL.full.length; i++) {
    var f = TL.full[i];
    L = comp.layers.add(imp(f.file)); L.startTime = f.t0 - (f["in"] || 0); L.inPoint = f.t0; L.outPoint = f.t1; L.name = "full " + i;
    fade(L, f.t0, f.t1, f.fadeIn || 0, f.fadeOut || 0);
}

// ── 자막(아래쪽 PNG) ──
for (i = 0; i < TL.captions.length; i++) {
    var cp = TL.captions[i];
    L = comp.layers.add(imp(cp.file)); L.inPoint = cp.t0; L.outPoint = cp.t1; L.name = "cap " + i;
    var cx = cp.x || 1920;
    T(L).property("ADBE Position").setValue([cx, cp.y || 1080]);
    fade(L, cp.t0, cp.t1, 0.2, 0.2);
    keys(T(L).property("ADBE Position"), [[cp.t0, [cx, (cp.y || 1080) + 14]], [cp.t0 + 0.25, [cx, cp.y || 1080]]]);
}

// ── 목소리 ──
var VO_AT = [];
for (i = 0; i < TL.voice.length; i++) {
    var vo = TL.voice[i], A = comp.layers.add(imp(vo.file)); A.startTime = vo.t; A.name = "vo " + vo.key;
    VO_AT.push([vo.t, vo.t + vo.dur]);
}
if (TL.voice.length && VO_AT[VO_AT.length - 1][1] > comp.duration) logTo(OUT_DIR + "/build.log", "주의: 마지막 줄이 " + VO_AT[VO_AT.length - 1][1].toFixed(2) + " s 에 끝난다");

// ── 효과음 ──
for (i = 0; i < (TL.sfx || []).length; i++) {
    var sx = TL.sfx[i], SL = comp.layers.add(imp(sx.file)); SL.startTime = sx.t;
    SL.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([sx.level || 0, sx.level || 0]);
}

// ── 패드 — 목소리 아래에서 낮춘다 ──
if (TL.music && TL.music.file) {
    var ML = comp.layers.add(imp(TL.music.file)); ML.startTime = 0; ML.outPoint = comp.duration; ML.name = "pad";
    var BASE = TL.music.base, DUCK = TL.music.duck, lv = [[0, -40], [1.0, BASE]];
    for (var u = 0; u < VO_AT.length; u++) {
        var s0 = VO_AT[u][0], e0 = VO_AT[u][1];
        if (s0 - 0.25 > lv[lv.length - 1][0]) lv.push([s0 - 0.25, BASE]);
        lv.push([s0, DUCK]);
        var nxt = (u + 1 < VO_AT.length) ? VO_AT[u + 1][0] : 999;
        if (nxt - e0 > 1.2) { lv.push([e0 + 0.2, DUCK]); lv.push([e0 + 0.8, BASE]); }
    }
    lv.push([comp.duration - 2.0, lv[lv.length - 1][1]]); lv.push([comp.duration, -50]);
    var LV = []; for (var z = 0; z < lv.length; z++) if (z === 0 || lv[z][0] > LV[LV.length - 1][0]) LV.push([lv[z][0], [lv[z][1], lv[z][1]]]);
    keys(ML.property("ADBE Audio Group").property("ADBE Audio Levels"), LV);
}

// ── 확인용 정지 그림 ──
for (i = 0; i < (TL.checks || []).length; i++)
    comp.saveFrameToPng(TL.checks[i], new File(OUT_DIR + "/ep01-check-" + ("000" + Math.round(TL.checks[i] * 10)).slice(-4) + ".png"));

var rq = P.renderQueue.items.add(comp), om = rq.outputModule(1);
try { om.applyTemplate(TL.template || "H.264 - Match Render Settings - 40 Mbps"); }
catch (e1) { om.applyTemplate("H.264 - Match Render Settings - 15 Mbps"); logTo(OUT_DIR + "/build.log", "템플릿 대신 15 Mbps"); }
om.file = new File(OUT_DIR + "/" + OUT_NAME);
P.save(new File(OUT_DIR + "/" + OUT_NAME + ".aep"));
logTo(OUT_DIR + "/build.log", "ok: " + comp.numLayers + " layers, " + TL.clips.length + " clips, " + TL.voice.length + " voice lines");
