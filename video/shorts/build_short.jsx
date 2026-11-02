// 편마다 숏츠(본편 4K 녹화를 잘라서) — shorts/<id>/cfg.js 를 읽는다.   RENDER_NOW=1 OUT_NAME=<id> ./ae.sh shorts/build_short
// 위: 낱말 · 가운데 위: 창 전체(미니맵)와 구역 테 · 가운데 아래: 그 구역 확대(박자 사이는 컷) · 아래: 자막 · 끝: 모션 카드
$.evalFile(new File(ROOT + "/shorts/" + OUT_NAME + "/cfg.js"));
var P, comp, C = CFG, R = C.root;
var VOID = [11 / 255, 11 / 255, 13 / 255], HOT = [1, 74 / 255, 26 / 255], CREAM = [242 / 255, 238 / 255, 228 / 255];
var DUR = C.DUR, K = 1000 / 3840, MY = 620, ZY = 1300, HK = C.H, RT = C.Rt, END0 = C.END0;
function imp(path, seq) { var io = new ImportOptions(new File(path)); if (seq) { io.sequence = true; io.forceAlphabetical = true; }
    var it = P.importFile(io); if (seq) it.mainSource.conformFrameRate = 30; return it; }
function easeAll(prop) { var n = 1, t = prop.propertyValueType; if (t === PropertyValueType.TwoD) n = 2; if (t === PropertyValueType.ThreeD) n = 3;
    var e = []; for (var i = 0; i < n; i++) e.push(new KeyframeEase(0, 75));
    for (var k = 1; k <= prop.numKeys; k++) { prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER); prop.setTemporalEaseAtKey(k, e, e); } }
function holdAll(prop) { for (var k = 1; k <= prop.numKeys; k++) prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.HOLD); }
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
    r = L.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group").property("ADBE Vector Shape - Rect");
    return [L, r];
}
function freeze(c, item, srcT, tin, tout) {     // 한 장면을 멈춘 채로
    var L = c.layers.add(item); L.startTime = 0; L.timeRemapEnabled = true;
    L.property("ADBE Time Remapping").expression = "" + srcT.toFixed(3);     // 키를 지우면 속성이 숨어 버린다 — 식으로 멈춘다
    L.inPoint = tin; L.outPoint = tout;          // 앞을 먼저 — 끝을 먼저 두면 앞을 옮길 때 길이째 밀려 끝이 늘어났다
    T(L).property("ADBE Position").setValue([1920, 1020]); return L;
}

app.beginSuppressDialogs();
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.newProject(); P = app.project;

// 창(3840×2100): 박자마다 녹화 한 조각. 1박 앞(훅)은 1박 녹화가 이어서 흐르고, 모자라면 첫 장면을 멈춰 둔다. 다시 보기 동안은 4박 끝 장면을 멈춘다
var win = P.items.addComp("win", 3840, 2100, 1, DUR, 30), recs = {};
for (var i = 0; i < 4; i++) {
    var b = C.beats[i]; if (!recs[b.rec]) recs[b.rec] = imp(b.rec);
    var it = recs[b.rec], tin = (i === 0) ? 0 : b.t, tout = (i === 3) ? RT : b.t + b.d;
    var L = win.layers.add(it); L.startTime = b.t - b.src; T(L).property("ADBE Position").setValue([1920, 1020]);
    var realIn = Math.max(tin, L.startTime); L.inPoint = realIn; L.outPoint = tout; L.moveToEnd();
    if (i === 0 && realIn > 0.01) freeze(win, it, 0, 0, realIn).moveToEnd();
    if (b.audio) { var au = imp(b.audio.file); var AL = win.layers.add(au); AL.startTime = L.startTime + b.audio.shift;
        AL.inPoint = Math.max(realIn, AL.startTime); AL.outPoint = tout;
        AL.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([b.audio.db, b.audio.db]); }
}
// 다시 보기: 박자마다 그 장면(테를 그린 순간)을 0.45 s 씩 멈춰 보여 준다 — 한 장면에 네 테를 다 그리면 다른 화면의 테가 엉뚱한 곳에 떴다(사용자, short11)
var SLOT = 0.45;
function recapT(r) { return RT + 0.15 + r * SLOT; }
for (var f = 0; f < 4; f++) {
    var bf = C.beats[f], itf = recs[bf.rec], ft = Math.min(bf.src + 1.4, bf.src + bf.d - 0.2, itf.duration - 0.1);
    freeze(win, itf, ft, f === 0 ? RT : recapT(f), f === 3 ? DUR : recapT(f + 1)).moveToEnd();
}

comp = P.items.addComp(C.id, 1080, 1920, 1, DUR, 30); comp.bgColor = VOID;

// 확대 칸 — 박자 경계에서 컷(창 내용도 거기서 바뀐다), 박자 안에서는 천천히 4 % 다가간다
var zc = P.items.addComp("zoom", 1000, 700, 1, DUR, 30);
var ZW = zc.layers.add(win); var zs = T(ZW).property("ADBE Scale"), za = T(ZW).property("ADBE Anchor Point");
T(ZW).property("ADBE Position").setValue([500, 350]);
for (var j = 0; j < 4; j++) {
    var z = C.beats[j], s = 1000 / z.zw * 100, t0 = z.t, t1 = (j === 3) ? RT : z.t + z.d;
    za.setValueAtTime(t0, [z.zx, z.zy]); zs.setValueAtTime(t0, [s, s]);
    za.setValueAtTime(t1 - 0.04, [z.zx, z.zy]); zs.setValueAtTime(t1 - 0.04, [s * 1.04, s * 1.04]);
}
for (var q = 1; q <= za.numKeys; q++) za.setInterpolationTypeAtKey(q, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.HOLD);
for (var q2 = 1; q2 <= zs.numKeys; q2++) zs.setInterpolationTypeAtKey(q2, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.HOLD);
var B0 = C.beats[0].t, ZL = put(comp, zc, B0 - 0.1, RT + 0.3, 540, ZY); fadeIn(ZL, B0 - 0.1, .35); fadeOut(ZL, RT + 0.3, .3);
keys(T(ZL).property("ADBE Scale"), [[B0 - 0.1, [92, 92]], [B0 + 0.3, [100, 100]]]);
var zb = rectLayer(comp, "zoom border", 1000, 700, HOT, 4, B0 - 0.1, RT + 0.3); T(zb[0]).property("ADBE Position").setValue([540, ZY]);
fadeIn(zb[0], B0, .3); fadeOut(zb[0], RT + 0.3, .3);

// 창 전체 — 훅에서 가운데 크게, 1박 직전에 위로 올라가 미니맵
var Wl = put(comp, win, 0, END0 + 0.1, 540, 1040);
keys(T(Wl).property("ADBE Position"), [[0, [540, 1060]], [HK - 0.2, [540, 1040]], [HK + 0.35, [540, MY]]]);
keys(T(Wl).property("ADBE Scale"), [[0, [K * 104, K * 104]], [HK - 0.2, [K * 100, K * 100]]]);
fadeIn(Wl, 0, .3); fadeOut(Wl, END0 + 0.1, .35);
var wb = rectLayer(comp, "window border", 1000, 547, CREAM, 2, 0, END0 + 0.1);
keys(T(wb[0]).property("ADBE Position"), [[0, [540, 1060]], [HK - 0.2, [540, 1040]], [HK + 0.35, [540, MY]]]);
keys(T(wb[0]).property("ADBE Scale"), [[0, [104, 104]], [HK - 0.2, [100, 100]]]); T(wb[0]).property("ADBE Opacity").setValue(25);

function mm(x, y) { return [540 + (x - 1920) * K, MY + (y - 1050) * K]; }
var ob = rectLayer(comp, "zone", 100, 100, HOT, 5, B0, RT + 0.2);
var op = T(ob[0]).property("ADBE Position"), os = ob[1].property("ADBE Vector Rect Size");
// 테는 박자 경계에서 컷(창 장면이 바뀌는 순간과 같이) — 미리 미끄러지면 앞 장면 위에서 엇나가 보였다(사용자, short16)
for (var m = 0; m < 4; m++) { var zz = C.beats[m]; op.setValueAtTime(zz.t, mm(zz.ox, zz.oy)); os.setValueAtTime(zz.t, [zz.ow * K, zz.oh * K]); }
holdAll(op); holdAll(os); fadeIn(ob[0], B0 + 0.1, .3);
for (var r = 0; r < 4; r++) { var zr = C.beats[r], te = (r === 3) ? END0 + 0.1 : recapT(r + 1), rq = rectLayer(comp, "recap zone " + r, zr.ow * K, zr.oh * K, HOT, 5, recapT(r), te);
    T(rq[0]).property("ADBE Position").setValue(mm(zr.ox, zr.oy)); fadeIn(rq[0], recapT(r), .1); if (r === 3) fadeOut(rq[0], END0 + 0.1, .3); }

// 글
var pn = ["hook", "w1", "w2", "w3", "w4", "recap", "tag", "s1", "s2", "s3", "s4", "s5", "s6"], parts = {};
for (var p = 0; p < pn.length; p++) parts[pn[p]] = imp(R + "/parts/" + pn[p] + ".png");
var Hl = put(comp, parts.hook, 0, HK + 0.05, 540, 380); fadeIn(Hl, 0.1, .3); fadeOut(Hl, HK + 0.05, .25);
keys(T(Hl).property("ADBE Scale"), [[0.1, [108, 108]], [0.6, [100, 100]]]);
for (var w = 0; w < 4; w++) { var bw = C.beats[w], t1w = (w === 3) ? RT : bw.t + bw.d;
    var WL = put(comp, parts["w" + (w + 1)], bw.t, t1w, 540, 205);
    keys(T(WL).property("ADBE Scale"), [[bw.t, [70, 70]], [bw.t + .22, [104, 104]], [bw.t + .34, [100, 100]]]); fadeIn(WL, bw.t, .12); }
var RC = put(comp, parts.recap, RT + 0.1, END0, 540, 1300);
keys(T(RC).property("ADBE Scale"), [[RT + 0.1, [86, 86]], [RT + 0.5, [100, 100]]]); fadeIn(RC, RT + 0.1, .3); fadeOut(RC, END0, .3);
for (var u = 0; u < 6; u++) { var su = C.subs[u], SLy = put(comp, parts["s" + (u + 1)], su[0], su[1], 540, 1770); fadeIn(SLy, su[0], .12); }
var E = comp.layers.add(imp(C.endframes, true)); E.startTime = END0;
var TG = put(comp, parts.tag, END0 + 1.6, DUR, 540, 1640); fadeIn(TG, END0 + 1.6, .3);

// 소리
for (var v = 0; v < C.vo.length; v++) { var AV = comp.layers.add(imp(C.vo[v].file)); AV.startTime = C.vo[v].t; }
var ML = comp.layers.add(imp(C.music)); ML.startTime = 0; ML.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([-6, -6]);

var checks = [1.5, C.beats[0].t + 1.5, C.beats[1].t + 1.5, C.beats[2].t + 1.5, C.beats[3].t + 1.5, RT + 1.5, END0 + 3.5];
for (var c = 0; c < checks.length; c++) comp.saveFrameToPng(checks[c], new File(R + "/qa-check-" + c + ".png"));
var rq2 = P.renderQueue.items.add(comp), om = rq2.outputModule(1);
om.applyTemplate("H.264 - Match Render Settings - 15 Mbps"); om.file = new File(OUT_DIR + "/" + OUT_NAME);
P.save(new File(OUT_DIR + "/" + OUT_NAME + ".aep"));
logTo(OUT_DIR + "/build.log", "ok: " + comp.numLayers + " layers");
if (typeof RENDER_NOW !== "undefined" && RENDER_NOW) P.renderQueue.render();
