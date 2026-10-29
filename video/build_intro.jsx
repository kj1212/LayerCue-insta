// 기본 소개 쇼츠 「Seven layers. Every screen.」 2판 · 25.2 s · 1080×1920 — AE 에서 조립하고 렌더 대기열(H.264)에 넣는다.
//   AUDIO_DIR=audio-intro OUT_NAME=layercue-intro MUSIC_FILE=$PWD/music/bgm-25s.wav ./ae.sh build_intro
// 재료: frames/hook · frames/end-intro — motion.html | shots/rec/*.mov — record_seq.py · record_layers.py(8 s)
//       shots/layers/key-*.png — 검은 바탕을 지운 층 그림 | audio-intro/01–10.wav | music/bgm-25s.wav · sfx-*.wav — sfx.py
//       overlays/ — ic-*(자막) · tg-*(층 표) · sc-*(화면 이름표) · edge-*(판 테두리) · bezel · grid
//
// 시간표(초)
//   0    훅(HTML)
//   2.6  쌓기 — 녹화 그대로(배경 2.7 · 글 4.7 · 로고 6.5 · 이름 띠 7.7)
//   10.0 층 분리 — 쌓기 카드가 그 자리에서 판 넷으로 갈라졌다가
//   13.25 다시 붙은 판이 그대로 객석 화면이 되어 위로, 무대 모니터 · 로비가 아래에 — 신호선이 갈라진다
//   17.7 객석 화면이 다시 커져 「한 장만」 장면이 된다(18.3 에 글만 다음 장)
//   20.05 호박 · 보라 · 녹 와이프 → 20.6 끝(HTML)
// ★ 장면 사이를 자르지 않는다 — 앞 장면의 끝 모습(자리 · 크기 · 각도)과 다음 장면의 첫 모습을 같게 둔다.
// ★ 4K 녹화(3840×2160)를 세로 화면에 넣는다 — 28.125 % 면 폭 1080. 판·화면 모서리는 판 좌표 64 px(세로 화면 ~18 px).

var P, comp;
var VOID = [11 / 255, 11 / 255, 13 / 255];
var K = 28.125, KA = 25, KS = 12.24;          // 쌓기 카드 · 객석 화면 · 무대/로비 화면
var VO_AT = [];                                // 목소리 [시작, 끝] — 음악을 그 밑에서 낮춘다

function imp(path, seq) {
    var io = new ImportOptions(new File(path));
    if (seq) { io.sequence = true; io.forceAlphabetical = true; }
    var it = P.importFile(io);
    if (seq) it.mainSource.conformFrameRate = 30;
    return it;
}
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
function layer(item, tin, tout, start) {
    var L = comp.layers.add(item);
    L.startTime = (start === undefined) ? 0 : start;
    L.inPoint = tin; L.outPoint = tout;
    return L;
}
function s3(v) { return [v, v, v]; }

// 둥근 사각 마스크(판 좌표) — 꼭짓점 여덟, 모서리마다 베지어 손잡이 0.5523 r
function roundMask(L, w, h, r) {
    var k = r * 0.5523, sh = new Shape();
    sh.vertices = [[r, 0], [w - r, 0], [w, r], [w, h - r], [w - r, h], [r, h], [0, h - r], [0, r]];
    sh.inTangents = [[-k, 0], [0, 0], [0, -k], [0, 0], [k, 0], [0, 0], [0, k], [0, 0]];
    sh.outTangents = [[0, 0], [k, 0], [0, 0], [0, k], [0, 0], [-k, 0], [0, 0], [0, -k]];
    sh.closed = true;
    L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom").property("ADBE Mask Shape").setValue(sh);
}
function ellipseMask(L, cx, cy, rx, ry, feather, inverted) {
    var kx = rx * 0.5523, ky = ry * 0.5523, sh = new Shape();
    sh.vertices = [[cx, cy - ry], [cx + rx, cy], [cx, cy + ry], [cx - rx, cy]];
    sh.inTangents = [[-kx, 0], [0, -ky], [kx, 0], [0, ky]];
    sh.outTangents = [[kx, 0], [0, ky], [-kx, 0], [0, -ky]];
    sh.closed = true;
    var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    m.property("ADBE Mask Shape").setValue(sh); m.property("ADBE Mask Feather").setValue([feather, feather]);
    m.inverted = !!inverted;
}
function shadow(L) {
    var fx = L.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
    fx.property(2).setValue(180); fx.property(4).setValue(36); fx.property(5).setValue(110);
}
// 판 하나에 붙어 같이 움직이는 것 — parent = 은 배율을 거꾸로 보정하니 setParentWithJump 로(판보다 몇 배 크게 그려졌었다)
function attach(child, parent, scalePct) {
    child.threeDLayer = true; child.setParentWithJump(parent);
    T(child).property("ADBE Position").setValue([1920, 1080, 0]);
    T(child).property("ADBE Scale").setValue(s3(scalePct || 100));
}

// 화면 카드 — 둥근 모서리 · 옅은 테 · 그림자 · 뒤로 번지는 화면 빛
// ★ 빛은 배경 영상만(1-bg.mov)으로 — 다 뜬 화면을 흐리면 흰 로고·글이 회색 얼룩으로 번졌다. glow = 배경 영상의 startTime
function card(item, tin, tout, start, glow) {
    var o = {};
    if (glow !== false && glow !== undefined) {
        o.g = layer(vBg, tin, tout, glow);
        var b = o.g.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur 2");
        // ★ Repeat Edge Pixels 를 켜면 흐린 판의 위아래가 칼같이 잘려 화면 밖까지 사각 띠가 졌다 — 끄면 가장자리가 스러진다
        b.property(1).setValue(260); b.property(3).setValue(0);
    }
    o.c = layer(item, tin, tout, start);
    o.c.threeDLayer = true; roundMask(o.c, 3840, 2160, 64); shadow(o.c);
    o.b = layer(BEZEL, tin, tout);
    attach(o.b, o.c);
    if (o.g) attach(o.g, o.c, 150);
    return o;
}
// 카드의 투명도 — 테와 번진 빛은 부모의 투명도를 물려받지 않아 같이 건다
function cardOpacity(o, list, glowMax) {
    keys(T(o.c).property("ADBE Opacity"), list);
    keys(T(o.b).property("ADBE Opacity"), list);
    if (o.g) {
        var gl = []; for (var i = 0; i < list.length; i++) gl.push([list[i][0], list[i][1] * (glowMax || 0.5)]);
        keys(T(o.g).property("ADBE Opacity"), gl);
    }
}
function pop(L, t, at) {    // 0 → 112 → 100 %
    keys(T(L).property("ADBE Scale"), [[t, [0, 0]], [t + 0.18, [112, 112]], [t + 0.3, [100, 100]]]);
    if (at) T(L).property("ADBE Position").setValue(at);
}
function line(x0, y0, x1, y1, tin, tout) {   // 신호선 — 위 끝을 축으로 아래로 그려진다
    var dx = x1 - x0, dy = y1 - y0, L = Math.sqrt(dx * dx + dy * dy);
    var S = comp.layers.addSolid([242 / 255, 238 / 255, 228 / 255], "signal", 3, Math.round(L), 1, comp.duration);
    S.inPoint = tin; S.outPoint = tout;
    T(S).property("ADBE Anchor Point").setValue([1.5, 0]);
    T(S).property("ADBE Position").setValue([x0, y0]);
    T(S).property("ADBE Rotate Z").setValue(-Math.asin(dx / L) * 180 / Math.PI);
    keys(T(S).property("ADBE Scale"), [[tin, [100, 0]], [tin + 0.3, [100, 100]]]);
    keys(T(S).property("ADBE Opacity"), [[tin, 40], [tout - 0.25, 40], [tout, 0]]);
    return S;
}

app.beginSuppressDialogs();
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.newProject();
P = app.project;
comp = P.items.addComp("LayerCue-intro", 1080, 1920, 1, 25.2, 30);
comp.bgColor = VOID;
var R = ROOT;

var hookSeq = imp(R + "/frames/hook/00000.png", true);
var endSeq = imp(R + "/frames/end-intro/00000.png", true);
var vStack = imp(R + "/shots/rec/seq-stack.mov"), vNext = imp(R + "/shots/rec/seq-next.mov");
var vAll = imp(R + "/shots/rec/4-all.mov"), vLobby = imp(R + "/shots/rec/lobby.mov"), vBg = imp(R + "/shots/rec/1-bg.mov");
var pFg = imp(R + "/shots/layers/only-fg.png");
var kFg = imp(R + "/shots/layers/key-fg.png"), kLogo = imp(R + "/shots/layers/key-logo.png"), kLt = imp(R + "/shots/layers/key-lt.png");
var ov = {};
var ON = ["ic-loops", "ic-slides", "ic-logo", "ic-own", "ic-every", "ic-needs", "ic-change",
          "tg-bg", "tg-fg", "tg-ov", "sc-audience", "sc-stage", "sc-lobby", "grid", "bezel", "edge-bg", "edge-fg", "edge-ov"];
for (var i = 0; i < ON.length; i++) ov[ON[i]] = imp(R + "/overlays/" + ON[i] + ".png");
var BEZEL = ov["bezel"];

// ── 바탕: 홈페이지와 같은 세로 격자(훅 · 끝 HTML 에도 있다) ──
var GR = layer(ov["grid"], 2.6, 20.6);

// ── 0 – 2.6  훅 ──
var H = comp.layers.add(hookSeq); H.startTime = 0;

// ── 2.6 – 10.0  쌓기 — LayerCue 의 실제 페이드가 녹화돼 있다 ──
var A = card(vStack, 2.6, 10.0, 2.3, 2.3);
T(A.c).property("ADBE Position").setValue([540, 820, 0]);
keys(T(A.c).property("ADBE Scale"), [[2.6, s3(K * 1.22)], [3.15, s3(K)], [9.4, s3(K * 1.04)], [10.0, s3(K)]]);
keys(T(A.c).property("ADBE Rotate Y"), [[2.6, -16], [3.15, -5], [9.4, 3], [10.0, 0]]);
cardOpacity(A, [[2.6, 0], [2.85, 100], [9.7, 100], [10.0, 100]]);
keys(T(A.g).property("ADBE Opacity"), [[2.6, 0], [3.0, 60], [9.6, 60], [10.0, 0]]);   // 판 장면 앞에서 빛을 거둔다
var TG = [["tg-bg", 2.75], ["tg-fg", 4.75], ["tg-ov", 6.55]];
for (var g = 0; g < TG.length; g++) {
    var Lt = layer(ov[TG[g][0]], TG[g][1], 10.0);
    pop(Lt, TG[g][1], [540 + (g - 1) * 330, 1205]);
    keys(T(Lt).property("ADBE Opacity"), [[9.7, 100], [10.0, 0]]);
}

// ── 10.0 – 13.3  층 분리 — 카드가 그 자리에서 판 넷으로 갈라진다 ──
// ★ 판에 수직으로 띄운다(위아래로만 올리면 기울어진 판끼리 맞부딪혀 글이 잘렸다). X −58° 의 판 앞쪽 = (0, −sin58, −cos58).
var PL = [[vBg, 9.6, "edge-bg"], [kFg, 0, "edge-fg"], [kLogo, 0, "edge-ov"], [kLt, 0, "edge-ov"]];
for (var p = 0; p < PL.length; p++) {
    var Lp = layer(PL[p][0], 10.0, 13.3, PL[p][1]);
    Lp.threeDLayer = true;
    if (p === 0) roundMask(Lp, 3840, 2160, 64);
    var d = 235 * p, dy = -0.848 * d, dz = -0.530 * d;
    keys(T(Lp).property("ADBE Position"), [[10.0, [540, 820, 0]], [10.7, [540, 1200 + dy, dz]], [12.55, [540, 1200 + dy, dz]], [13.25, [540, 820, 0]]]);
    keys(T(Lp).property("ADBE Scale"), [[10.0, s3(K)], [10.7, s3(K * 0.82)], [12.55, s3(K * 0.82)], [13.25, s3(K)]]);
    keys(T(Lp).property("ADBE Rotate X"), [[10.0, 0], [10.7, -58], [12.55, -58], [13.25, 0]]);
    keys(T(Lp).property("ADBE Rotate Z"), [[10.0, 0], [10.7, -32], [12.55, -26], [13.25, 0]]);   // 떠 있는 동안 아주 천천히 돈다
    var Ed = layer(ov[PL[p][2]], 10.0, 13.3);
    attach(Ed, Lp);
    keys(T(Ed).property("ADBE Opacity"), [[10.15, 0], [10.6, 100], [12.6, 100], [13.05, 0]]);
}

// ── 13.25 – 17.7  화면 셋 — 붙은 판이 그대로 객석 화면이 되어 위로, 아래에 무대 모니터 · 로비 ──
var AU = card(vAll, 13.25, 17.7, 13.0, 12.9);
keys(T(AU.c).property("ADBE Position"), [[13.25, [540, 820, 0]], [13.8, [540, 560, 0]], [17.2, [540, 560, 0]], [17.7, [540, 820, 0]]]);
keys(T(AU.c).property("ADBE Scale"), [[13.25, s3(K)], [13.8, s3(KA)], [17.2, s3(KA)], [17.7, s3(K)]]);
keys(T(AU.g).property("ADBE Opacity"), [[13.25, 0], [13.75, 60], [17.7, 60]]);
var SM = [[pFg, 0, 290, 13.55, "sc-stage", 253], [vLobby, 13.4, 790, 13.67, "sc-lobby", 736]];
for (var m = 0; m < SM.length; m++) {
    var t0 = SM[m][3];
    var o = card(SM[m][0], t0, 17.5, SM[m][1], false);
    keys(T(o.c).property("ADBE Position"), [[t0, [SM[m][2], 1180, 0]], [t0 + 0.32, [SM[m][2], 1150, 0]], [17.2, [SM[m][2], 1150, 0]], [17.5, [SM[m][2], 1215, 0]]]);
    keys(T(o.c).property("ADBE Scale"), [[t0, s3(KS * 0.86)], [t0 + 0.32, s3(KS)]]);
    cardOpacity(o, [[t0, 0], [t0 + 0.2, 100], [17.2, 100], [17.5, 0]]);
    var Lb = layer(ov[SM[m][4]], t0 + 0.35, 17.5);
    T(Lb).property("ADBE Position").setValue([SM[m][5], 992]);
    keys(T(Lb).property("ADBE Opacity"), [[t0 + 0.35, 0], [t0 + 0.55, 100], [17.2, 100], [17.45, 0]]);
    line(540, 832, SM[m][2], 1016, 13.45 + m * 0.08, 17.45);
}
var La = layer(ov["sc-audience"], 13.85, 17.45);
T(La).property("ADBE Position").setValue([271, 258]);
keys(T(La).property("ADBE Opacity"), [[13.85, 0], [14.05, 100], [17.2, 100], [17.45, 0]]);

// ── 17.7 – 20.6  한 장만 — 글만 다음 장(18.3), 나머지 층은 그대로 ──
var D = card(vNext, 17.7, 20.6, 16.8, 17.4);
T(D.c).property("ADBE Position").setValue([540, 820, 0]);
keys(T(D.c).property("ADBE Scale"), [[17.7, s3(K)], [20.3, s3(K * 1.05)]]);
keys(T(D.c).property("ADBE Rotate Y"), [[17.7, 0], [20.3, -3]]);
T(D.g).property("ADBE Opacity").setValue(60);
var TD = [["tg-bg", 45], ["tg-fg", 100], ["tg-ov", 45]];
for (var q = 0; q < TD.length; q++) {
    var Lq = layer(ov[TD[q][0]], 17.85, 20.6);
    T(Lq).property("ADBE Position").setValue([540 + (q - 1) * 330, 1205]);
    keys(T(Lq).property("ADBE Opacity"), [[17.85, 0], [18.05, TD[q][1]]]);
    if (q === 1) keys(T(Lq).property("ADBE Scale"), [[18.3, [100, 100]], [18.45, [122, 122]], [18.7, [100, 100]]]);   // 바뀐 층만 반짝
}

// ── 비네팅 — 가장자리를 눌러 가운데로 ──
var VG = comp.layers.addSolid([0, 0, 0], "vignette", 1080, 1920, 1, comp.duration);
VG.inPoint = 2.6; VG.outPoint = 20.6;
ellipseMask(VG, 540, 900, 760, 1180, 520, true);
T(VG).property("ADBE Opacity").setValue(55);

// ── 자막(소리 끄고 보는 사람) — 아래서 살짝 떠오른다 ──
var band = comp.layers.addSolid([0, 0, 0], "caption band", 1080, 700, 1, comp.duration);
band.inPoint = 2.6; band.outPoint = 20.6;
T(band).property("ADBE Position").setValue([540, 1650]);
T(band).property("ADBE Opacity").setValue(80);
var mk = band.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
var shp = new Shape(); shp.vertices = [[-100, 230], [1180, 230], [1180, 800], [-100, 800]]; shp.closed = true;
mk.property("ADBE Mask Shape").setValue(shp); mk.property("ADBE Mask Feather").setValue([0, 200]);
var CAP = [["ic-loops", 2.9, 4.7], ["ic-slides", 4.75, 6.55], ["ic-logo", 6.6, 9.95], ["ic-own", 10.3, 13.35],
           ["ic-every", 13.6, 15.15], ["ic-needs", 15.2, 17.6], ["ic-change", 17.8, 20.3]];
for (var c = 0; c < CAP.length; c++) {
    var C = layer(ov[CAP[c][0]], CAP[c][1], CAP[c][2]);
    keys(T(C).property("ADBE Position"), [[CAP[c][1], [540, 1712]], [CAP[c][1] + 0.22, [540, 1690]]]);
    keys(T(C).property("ADBE Opacity"), [[CAP[c][1], 0], [CAP[c][1] + 0.2, 100], [CAP[c][2] - 0.14, 100], [CAP[c][2], 0]]);
}

// ── 20.05 – 20.6  호박 · 보라 · 녹 와이프(AI 쇼츠와 같은 넘김) ──
var WC = [[[1, 122 / 255, 0], 20.05], [[122 / 255, 43 / 255, 1], 20.15], [[0, 185 / 255, 108 / 255], 20.25], [VOID, 20.35]];
for (var w = 0; w < WC.length; w++) {
    var Wl = comp.layers.addSolid(WC[w][0], "wipe", 1080, 1920, 1, comp.duration);
    Wl.inPoint = WC[w][1]; Wl.outPoint = 20.7;
    keys(T(Wl).property("ADBE Position"), [[WC[w][1], [540, 2880]], [WC[w][1] + 0.3, [540, 960]]]);
}

// ── 20.6 – 25.2  끝 ──
var E = comp.layers.add(endSeq); E.startTime = 20.6;

// ── 목소리 ──
var VO = [[1, 0.5], [2, 2.9], [3, 4.75], [4, 6.6], [5, 10.3], [6, 13.6], [7, 15.2], [8, 17.8], [9, 20.9], [10, 22.55]];
var prevEnd = 0;
for (var v = 0; v < VO.length; v++) {
    var a = imp(R + "/" + AUDIO_DIR + "/" + (VO[v][0] < 10 ? "0" : "") + VO[v][0] + ".wav");
    var at = Math.max(VO[v][1], prevEnd + 0.1);
    var AL = comp.layers.add(a); AL.startTime = at;
    prevEnd = at + a.duration; VO_AT.push([at, prevEnd]);
}
if (prevEnd > comp.duration) logTo(OUT_DIR + "/build.log", "주의: 마지막 줄이 " + prevEnd.toFixed(2) + " s 에 끝난다");

// ── 효과음 — 표·화면이 뜰 때 딸깍, 판이 갈라지고 붙을 때 둔탁, 휙은 색 와이프 한 번만 ──
// ★ 장면이 바뀔 때마다 휙을 넣었더니 너무 잦았다(사용자, 2026-10-30) — 굵은 색 띠가 지나가는 큰 넘김에만 쓴다
var SFX = { whoosh: imp(R + "/music/sfx-whoosh.wav"), tick: imp(R + "/music/sfx-tick.wav"), thump: imp(R + "/music/sfx-thump.wav") };
var HITS = [["whoosh", 19.9, 0],
            ["tick", 2.75, -3], ["tick", 4.75, -3], ["tick", 6.55, -3], ["tick", 13.55, -5], ["tick", 13.67, -5], ["tick", 18.3, -1],
            ["thump", 10.1, -3], ["thump", 13.05, -4]];
for (var x = 0; x < HITS.length; x++) {
    var SL = comp.layers.add(SFX[HITS[x][0]]); SL.startTime = HITS[x][1];
    SL.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([HITS[x][2], HITS[x][2]]);
}

// ── 배경음 — 목소리가 나오는 동안 6 dB 낮춘다 ──
if (MUSIC_FILE) {
    var mu = imp(MUSIC_FILE);
    var ML = comp.layers.add(mu); ML.startTime = 0; ML.outPoint = comp.duration;
    var BASE = -16, DUCK = -22, lv = [[0, -40], [0.6, BASE]];   // −19/−25 는 목소리보다 17 dB 낮아 음악이 거의 안 들렸다
    for (var u = 0; u < VO_AT.length; u++) {
        var s0 = VO_AT[u][0], e0 = VO_AT[u][1];
        if (s0 - 0.15 > lv[lv.length - 1][0]) lv.push([s0 - 0.15, BASE]);
        lv.push([s0, DUCK]);
        var nxt = (u + 1 < VO_AT.length) ? VO_AT[u + 1][0] : 99;
        if (nxt - e0 > 0.6) { lv.push([e0, DUCK]); lv.push([e0 + 0.3, BASE]); }
    }
    lv.push([comp.duration - 1.2, lv[lv.length - 1][1]]); lv.push([comp.duration, -50]);
    var LV = []; for (var z = 0; z < lv.length; z++) if (z === 0 || lv[z][0] > LV[LV.length - 1][0]) LV.push([lv[z][0], [lv[z][1], lv[z][1]]]);
    keys(ML.property("ADBE Audio Group").property("ADBE Audio Levels"), LV);
}

var checks = [1.8, 3.4, 5.4, 8.8, 10.0, 10.4, 11.6, 13.1, 13.5, 14.6, 16.0, 17.6, 18.5, 20.3, 22.8];
for (var qq = 0; qq < checks.length; qq++)
    comp.saveFrameToPng(checks[qq], new File(OUT_DIR + "/intro-check-" + ("00" + Math.round(checks[qq] * 10)).slice(-3) + ".png"));

var rq = P.renderQueue.items.add(comp), om = rq.outputModule(1);
om.applyTemplate("H.264 - Match Render Settings - 15 Mbps");
om.file = new File(OUT_DIR + "/" + OUT_NAME);
P.save(new File(OUT_DIR + "/" + OUT_NAME + ".aep"));
logTo(OUT_DIR + "/build.log", "ok: " + comp.numLayers + " layers");
