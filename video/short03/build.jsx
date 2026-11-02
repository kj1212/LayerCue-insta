// 숏츠 03 「Pick. Click. Watch. Adjust.」(1편 메인 창) 29.2 s 1080×1920 — ./ae.sh short03/build  (OUT_NAME=short03)
// 위: 낱말 카드 · 가운데 위: 창 전체(미니맵)와 지금 구역의 테 · 가운데 아래: 그 구역을 크게 · 아래: 자막. 녹화는 LG 4K(short03/rec/v1/main-en.mp4).
// 녹화 시계 c 의 일 = 이 컴프의 시각 c (녹화의 0 초가 시계 −1.0 s — 잰 값)
var P, comp, R = ROOT + "/short03";
var VOID = [11 / 255, 11 / 255, 13 / 255], HOT = [1, 74 / 255, 26 / 255], CREAM = [242 / 255, 238 / 255, 228 / 255];
var DUR = 29.2, K = 1000 / 3840, MY = 620, ZY = 1300;
function imp(path, seq) { var io = new ImportOptions(new File(path)); if (seq) { io.sequence = true; io.forceAlphabetical = true; }
    var it = P.importFile(io); if (seq) it.mainSource.conformFrameRate = 30; return it; }
function easeAll(prop) { var n = 1, t = prop.propertyValueType; if (t === PropertyValueType.TwoD) n = 2; if (t === PropertyValueType.ThreeD) n = 3;
    var e = []; for (var i = 0; i < n; i++) e.push(new KeyframeEase(0, 75));
    for (var k = 1; k <= prop.numKeys; k++) { prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER); prop.setTemporalEaseAtKey(k, e, e); } }
function keys(prop, list) { for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]); easeAll(prop); }
function T(L) { return L.property("ADBE Transform Group"); }
function put(c, item, tin, tout, x, y) { var L = c.layers.add(item); L.startTime = 0; L.inPoint = tin; L.outPoint = tout; T(L).property("ADBE Position").setValue([x, y]); return L; }
function fadeIn(L, t, d) { keys(T(L).property("ADBE Opacity"), [[t, 0], [t + (d || .25), 100]]); }
function fadeOut(L, t, d) { var o = T(L).property("ADBE Opacity"); o.setValueAtTime(t - (d || .25), 100); o.setValueAtTime(t, 0); easeAll(o); }
function rectLayer(c, name, w, h, color, stroke, tin, tout) {
    var L = c.layers.addShape(); L.name = name; L.inPoint = tin; L.outPoint = tout;
    var g = L.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group").property("ADBE Vectors Group");
    var r = g.addProperty("ADBE Vector Shape - Rect"); r.property("ADBE Vector Rect Size").setValue([w, h]); r.property("ADBE Vector Rect Roundness").setValue(10);
    var s = g.addProperty("ADBE Vector Graphic - Stroke"); s.property("ADBE Vector Stroke Color").setValue(color); s.property("ADBE Vector Stroke Width").setValue(stroke);
    r = L.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group").property("ADBE Vector Shape - Rect");   // 획을 더하면 앞의 참조가 끊긴다
    return [L, r];
}

app.beginSuppressDialogs();
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.newProject(); P = app.project;

// 창 그림(3840×2100) — 녹화 위 60 px 메뉴 막대는 잘라낸다. 녹화가 끝난 뒤는 마지막 장면으로 버틴다
var rec = imp(R + "/rec/v1/main-en.mp4"), last = imp(R + "/rec/v1/last.png");
var win = P.items.addComp("win", 3840, 2100, 1, DUR, 30);
var RL = win.layers.add(rec); RL.startTime = -1.0; T(RL).property("ADBE Position").setValue([1920, 1020]);
var endRec = RL.outPoint;
var LL = win.layers.add(last); LL.inPoint = endRec - 0.05; LL.outPoint = DUR; T(LL).property("ADBE Position").setValue([1920, 1020]); LL.moveToEnd();

// 구역(창 px: 가운데 x, 가운데 y, 폭) — 확대 칸 1000×700 에 맞는 비율. 테(미니맵)는 따로
var Z = [ { t: 3.6,  zx: 500,  zy: 1500, zw: 1000, ox: 200,  oy: 1050, ow: 400,  oh: 2060 },     // PICK  왼쪽 사이드바
          { t: 8.0,  zx: 930,  zy: 1110, zw: 1000, ox: 1900, oy: 1000, ow: 2960, oh: 560 },     // CLICK 가운데 카드
          { t: 12.5, zx: 880,  zy: 395,  zw: 900,  ox: 1290, oy: 390,  ow: 1720, oh: 640 },     // WATCH 위 무대 띠
          { t: 16.8, zx: 2650, zy: 420,  zw: 1000, ox: 2760, oy: 420,  ow: 1220, oh: 700 } ];   // ADJUST 오른쪽 Slide settings
var BEAT_END = 20.6, END0 = 24.8;

comp = P.items.addComp("short03-pick-click-watch-adjust", 1080, 1920, 1, DUR, 30); comp.bgColor = VOID;

// 확대 칸(1000×700)
var zc = P.items.addComp("zoom", 1000, 700, 1, DUR, 30);
var ZW = zc.layers.add(win); var zs = T(ZW).property("ADBE Scale"), za = T(ZW).property("ADBE Anchor Point");
T(ZW).property("ADBE Position").setValue([500, 350]);
for (var i = 0; i < Z.length; i++) {
    var s = 1000 / Z[i].zw * 100, t0 = Z[i].t;
    za.setValueAtTime(t0, [Z[i].zx, Z[i].zy]); zs.setValueAtTime(t0, [s, s]);
    if (i + 1 < Z.length) { za.setValueAtTime(Z[i + 1].t - 0.45, [Z[i].zx, Z[i].zy]); zs.setValueAtTime(Z[i + 1].t - 0.45, [s, s]); }
}
easeAll(za); easeAll(zs);
var ZL = put(comp, zc, 3.5, BEAT_END + 0.3, 540, ZY); fadeIn(ZL, 3.5, .35); fadeOut(ZL, BEAT_END + 0.3, .3);
keys(T(ZL).property("ADBE Scale"), [[3.5, [92, 92]], [3.9, [100, 100]]]);
var zb = rectLayer(comp, "zoom border", 1000, 700, HOT, 4, 3.5, BEAT_END + 0.3); T(zb[0]).property("ADBE Position").setValue([540, ZY]);
fadeIn(zb[0], 3.6, .3); fadeOut(zb[0], BEAT_END + 0.3, .3);

// 창 전체 — 처음엔 가운데 크게(훅), 3.4 s 에 위로 올라가 미니맵이 된다. 끝 카드 앞에서 사라진다
var W = put(comp, win, 0, END0 + 0.1, 540, 1040);
keys(T(W).property("ADBE Position"), [[0, [540, 1060]], [3.3, [540, 1040]], [3.85, [540, MY]]]);
keys(T(W).property("ADBE Scale"), [[0, [K * 100 * 1.04, K * 100 * 1.04]], [3.3, [K * 100, K * 100]]]);
fadeIn(W, 0, .3); fadeOut(W, END0 + 0.1, .35);
var wb = rectLayer(comp, "window border", 1000, 547, [CREAM[0], CREAM[1], CREAM[2]], 2, 0, END0 + 0.1);
keys(T(wb[0]).property("ADBE Position"), [[0, [540, 1060]], [3.3, [540, 1040]], [3.85, [540, MY]]]);
keys(T(wb[0]).property("ADBE Scale"), [[0, [104, 104]], [3.3, [100, 100]]]);
T(wb[0]).property("ADBE Opacity").setValue(25);

// 미니맵의 구역 테 — 박자마다 옮겨 간다
function mm(x, y) { return [540 + (x - 1920) * K, MY + (y - 1050) * K]; }
var ob = rectLayer(comp, "zone", 100, 100, HOT, 5, 3.6, BEAT_END + 0.2);
var op = T(ob[0]).property("ADBE Position"), os = ob[1].property("ADBE Vector Rect Size");
for (var j = 0; j < Z.length; j++) {
    op.setValueAtTime(Z[j].t, mm(Z[j].ox, Z[j].oy)); os.setValueAtTime(Z[j].t, [Z[j].ow * K, Z[j].oh * K]);
    if (j + 1 < Z.length) { op.setValueAtTime(Z[j + 1].t - 0.35, mm(Z[j].ox, Z[j].oy)); os.setValueAtTime(Z[j + 1].t - 0.35, [Z[j].ow * K, Z[j].oh * K]); }
}
easeAll(op); easeAll(os); fadeIn(ob[0], 3.7, .3);
// 다시 보기: 네 구역 테가 차례로 켜진다
for (var q = 0; q < Z.length; q++) {
    var rq = rectLayer(comp, "recap zone " + q, Z[q].ow * K, Z[q].oh * K, HOT, 5, BEAT_END + 0.2 + q * 0.42, END0 + 0.1);
    T(rq[0]).property("ADBE Position").setValue(mm(Z[q].ox, Z[q].oy)); fadeIn(rq[0], BEAT_END + 0.2 + q * 0.42, .15); fadeOut(rq[0], END0 + 0.1, .3);
}

// 글
var parts = {}, pn = ["hook", "w1", "w2", "w3", "w4", "recap", "tag", "s1", "s2", "s3", "s4", "s5", "s6"];
for (var p = 0; p < pn.length; p++) parts[pn[p]] = imp(R + "/parts/" + pn[p] + ".png");
var H = put(comp, parts.hook, 0, 3.55, 540, 380); fadeIn(H, 0.1, .3); fadeOut(H, 3.55, .25);
keys(T(H).property("ADBE Scale"), [[0.1, [108, 108]], [0.6, [100, 100]]]);
var wt = [[3.6, 8.0], [8.0, 12.5], [12.5, 16.8], [16.8, BEAT_END]];
for (var w = 0; w < 4; w++) {
    var WL = put(comp, parts["w" + (w + 1)], wt[w][0], wt[w][1], 540, 205);
    keys(T(WL).property("ADBE Scale"), [[wt[w][0], [70, 70]], [wt[w][0] + .22, [104, 104]], [wt[w][0] + .34, [100, 100]]]);
    fadeIn(WL, wt[w][0], .12);
}
var RC = put(comp, parts.recap, BEAT_END + 0.1, END0, 540, 1300);
keys(T(RC).property("ADBE Scale"), [[BEAT_END + 0.1, [86, 86]], [BEAT_END + 0.5, [100, 100]]]); fadeIn(RC, BEAT_END + 0.1, .3); fadeOut(RC, END0, .3);
var subs = [["s1", 0.35, 3.5], ["s2", 3.7, 7.9], ["s3", 8.2, 12.4], ["s4", 12.6, 16.7], ["s5", 17.0, 20.5], ["s6", 22.6, END0]];
for (var u = 0; u < subs.length; u++) { var SL = put(comp, parts[subs[u][0]], subs[u][1], subs[u][2], 540, 1770); fadeIn(SL, subs[u][1], .12); }
// 끝 카드(모션) + 1편 안내
var endSeq = imp(ROOT + "/frames/end-s03/00000.png", true);
var E = comp.layers.add(endSeq); E.startTime = END0;
var TG = put(comp, parts.tag, END0 + 1.6, DUR, 540, 1640); fadeIn(TG, END0 + 1.2, .3);

// 소리 — 목소리 줄과 배경음악
var VO = [[1, 0.35], [2, 3.7], [3, 8.2], [4, 12.6], [5, 17.0], [6, 20.8]], prevEnd = 0;
for (var v = 0; v < VO.length; v++) { var a = imp(R + "/audio/0" + VO[v][0] + ".wav"); var at = Math.max(VO[v][1], prevEnd + 0.15);
    var AL = comp.layers.add(a); AL.startTime = at; prevEnd = at + a.duration; }
var mu = imp(R + "/audio/music.wav"); var ML = comp.layers.add(mu); ML.startTime = 0;
ML.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([-6, -6]);

var checks = [1.5, 5.0, 9.5, 14.0, 18.5, 22.5, 27.5];
for (var c = 0; c < checks.length; c++) comp.saveFrameToPng(checks[c], new File(R + "/qa/check-" + ("0" + Math.round(checks[c] * 10)).slice(-3) + ".png"));
var rq2 = P.renderQueue.items.add(comp), om = rq2.outputModule(1);
om.applyTemplate("H.264 - Match Render Settings - 15 Mbps");
om.file = new File(OUT_DIR + "/" + OUT_NAME);
P.save(new File(OUT_DIR + "/" + OUT_NAME + ".aep"));
logTo(OUT_DIR + "/build.log", "ok: " + comp.numLayers + " layers, voice ends " + prevEnd.toFixed(2));
if (typeof RENDER_NOW !== "undefined" && RENDER_NOW) P.renderQueue.render();
