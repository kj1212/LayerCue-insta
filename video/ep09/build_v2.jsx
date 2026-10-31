// 1편 2판 조립 엔진 — ep09/timeline2.js (var TL) 를 읽어 3840×2160 · 30 fps 컴프를 짓고 렌더 대기열에 넣는다.
//   OUT_NAME=layercue-ep01-v2 ./ae.sh ep09/build_v2
// 짜임: 바탕(그리드) · 타이틀(프레임 묶음) · 무대 카드(무대 녹화) · 창 카드(Card 프리컴프 = 구간별 녹화) · 테/어둡게/클릭 링(카드의 자식) ·
//       이름표/선/자막/챕터 태그(화면 좌표) · 엔드 카드(프레임 묶음) · 목소리 · 음악(덕킹까지 끝낸 한 줄)
// ★ 자식은 parent 를 먼저 걸고 위치를 준다 — 그러면 위치가 부모의 원본 px(창 px · 무대 px)로 읽힌다.

var P, comp, card, stage;
var VOID = [11 / 255, 11 / 255, 13 / 255];
var COL = { panel: [35 / 255, 35 / 255, 36 / 255], indigo: [139 / 255, 149 / 255, 245 / 255], amber: [217 / 255, 138 / 255, 43 / 255], green: [63 / 255, 178 / 255, 127 / 255],
            hot: [255 / 255, 74 / 255, 26 / 255], white: [242 / 255, 238 / 255, 228 / 255] };
$.evalFile(ROOT + "/ep09/timeline2.js");
app.purge(PurgeTarget.ALL_CACHES);     // 프레임을 다시 그린 뒤라면 AE 가 예전(덜 그려진) 묶음을 기억하고 있을 수 있다

function imp(path, seq) {
    var io = new ImportOptions(new File(path));
    if (seq) { io.sequence = true; io.forceAlphabetical = true; }
    var it = P.importFile(io);
    if (seq) it.mainSource.conformFrameRate = 30;
    return it;
}
function easeAll(prop, infl) {
    var n = 1, t = prop.propertyValueType;
    if (t === PropertyValueType.TwoD) n = 2;
    if (t === PropertyValueType.ThreeD) n = 3;
    var e = []; for (var i = 0; i < n; i++) e.push(new KeyframeEase(0, infl || 75));
    for (var k = 1; k <= prop.numKeys; k++) { prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER); prop.setTemporalEaseAtKey(k, e, e); }
}
function keys(prop, list, infl) { for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]); easeAll(prop, infl); }
function T(L) { return L.property("ADBE Transform Group"); }
function adopt(L, par, pos) { L.parent = par; T(L).property("ADBE Scale").setValue([100, 100]); T(L).property("ADBE Rotate Z").setValue(0); T(L).property("ADBE Position").setValue(pos); }
function fade(L, t0, t1, fin, fout, max) {
    var m = (max === undefined) ? 100 : max, l = [];
    if (fin > 0) { l.push([t0, 0]); l.push([t0 + fin, m]); } else l.push([t0, m]);
    if (fout > 0) { l.push([t1 - fout, m]); l.push([t1, 0]); }
    keys(T(L).property("ADBE Opacity"), l, 60);
}
function roundMask(L, x, y, w, h, r, inverted, name) {
    var k = r * 0.5523, sh = new Shape();
    sh.vertices = [[x + r, y], [x + w - r, y], [x + w, y + r], [x + w, y + h - r], [x + w - r, y + h], [x + r, y + h], [x, y + h - r], [x, y + r]];
    sh.inTangents = [[-k, 0], [0, 0], [0, -k], [0, 0], [k, 0], [0, 0], [0, k], [0, 0]];
    sh.outTangents = [[0, 0], [k, 0], [0, 0], [0, k], [0, 0], [-k, 0], [0, 0], [0, -k]];
    sh.closed = true;
    var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    m.property("ADBE Mask Shape").setValue(sh); m.inverted = !!inverted;
    return m;
}
function shadow(L, opacity, dist, soft, color) {
    var fx = L.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
    if (color) fx.property(1).setValue(color);
    fx.property(2).setValue(opacity); fx.property(3).setValue(180); fx.property(4).setValue(dist); fx.property(5).setValue(soft);
    return fx;
}
function rectShape(L, w, h, r, strokeCol, strokeW, strokeOp) {
    var g = L.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"), v = g.property("ADBE Vectors Group");
    var rc = v.addProperty("ADBE Vector Shape - Rect");
    rc.property("ADBE Vector Rect Size").setValue([w, h]); rc.property("ADBE Vector Rect Roundness").setValue(r);
    var st = v.addProperty("ADBE Vector Graphic - Stroke");
    st.property("ADBE Vector Stroke Color").setValue(strokeCol); st.property("ADBE Vector Stroke Width").setValue(strokeW);
    if (strokeOp !== undefined) st.property("ADBE Vector Stroke Opacity").setValue(strokeOp);
}
function holdLast(dir, t0, t1, fin) {     // 프레임 묶음 + 마지막 장을 이어 붙여 머문다
    var seq = imp(dir + "/00000.png", true), L = comp.layers.add(seq);
    L.startTime = t0; var d = seq.duration;
    var f = new Folder(dir).getFiles("*.png"); f.sort();
    var last = comp.layers.add(imp(f[f.length - 1].fsName)); last.startTime = 0; last.inPoint = t0 + d - 1 / 30; last.outPoint = t1;
    return [L, last, t0 + d];
}

app.beginSuppressDialogs();
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.newProject();
P = app.project;
comp = P.items.addComp(TL.name, 3840, 2160, 1, TL.duration, TL.fps);
comp.bgColor = VOID;
var i, L, e;

// ── 바탕 ──
if (TL.bgm) {     // 4편부터: 격자 + 빛 번짐 셋이 천천히 떠다닌다
    L = comp.layers.add(imp(TL.bgm.grid)); L.outPoint = TL.duration; L.name = "bg grid";
    for (var gi2 = 0; gi2 < TL.bgm.glows.length; gi2++) {
        var gw = TL.bgm.glows[gi2], GL = comp.layers.add(imp(gw.file)); GL.outPoint = TL.duration; GL.name = "bg glow " + gi2;
        keys(T(GL).property("ADBE Position"), gw.keys, 33);      // 바탕이 컴프의 첫 레이어라 격자 위에 차례로 쌓인다
    }
} else { L = comp.layers.add(imp(TL.bg)); L.outPoint = TL.duration; L.name = "bg"; }

// ── 그래픽 장면(설치 등) ──
// ★ 프레임 묶음을 쓰는 동안 AE 가 폴더를 보면 앞 몇 초만 있는 묶음으로 기억한다 → 다시 읽히고 길이를 확인한다
var gShort = [];
for (i = 0; i < (TL.gfx || []).length; i++) {
    var gx = TL.gfx[i], gi = imp(gx.dir + "/00000.png", true);
    gi.mainSource.reload(); gi.mainSource.conformFrameRate = 30;
    if (gi.duration < gx.t1 - gx.t0 - 0.1) gShort.push("gfx " + i + " " + gi.duration.toFixed(2) + "/" + (gx.t1 - gx.t0).toFixed(2));
    var gs = comp.layers.add(gi); gs.startTime = gx.t0; gs.name = "gfx " + i;
}
if (gShort.length) { logTo(OUT_DIR + "/build.log", "오류: 그래픽 장면이 짧다 — " + gShort.join(", ")); throw new Error("gfx short"); }

// ── 무대 카드 ──
if (TL.stage) {
stage = comp.layers.add(imp(TL.stage.file)); stage.name = "stage";
stage.startTime = TL.stage.t0 - TL.stage["in"]; stage.inPoint = TL.stage.t0; stage.outPoint = TL.stage.t1;
T(stage).property("ADBE Anchor Point").setValue([0, 0]); T(stage).property("ADBE Position").setValue([270, 152]); T(stage).property("ADBE Scale").setValue([85.9375, 85.9375]);
roundMask(stage, 0, 0, 3840, 2160, 40); shadow(stage, 70, 40, 160);
fade(stage, TL.stage.t0, TL.stage.t1, 0.5, 0.5);
var sb = comp.layers.addShape(); sb.name = "stage border"; sb.inPoint = TL.stage.t0; sb.outPoint = TL.stage.t1;
adopt(sb, stage, [1920, 1080]); rectShape(sb, 3840, 2160, 40, COL.white, 3, 18); fade(sb, TL.stage.t0, TL.stage.t1, 0.5, 0.5);
}

// ── 창 카드 ──
var cc = P.items.addComp("Card", 3840, 2100, 1, TL.duration, TL.fps); cc.bgColor = VOID;
for (i = 0; i < TL.clips.length; i++) {
    var c = TL.clips[i];
    L = cc.layers.add(imp(c.file)); L.startTime = c.t0 - c["in"]; L.inPoint = c.t0; L.outPoint = c.t1; L.name = "rec " + i;
    T(L).property("ADBE Position").setValue([1920, 1020]);          // 메뉴 막대(위 60 px)를 위로 밀어 낸다
    if (i > 0) keys(T(L).property("ADBE Opacity"), [[c.t0, 0], [c.t0 + 0.3, 100]], 50);
}
card = comp.layers.add(cc); card.name = "card"; card.inPoint = TL.card.t0; card.outPoint = TL.card.t1;
T(card).property("ADBE Anchor Point").setValue([0, 0]);
var pk = [], sk = [];
for (i = 0; i < TL.card.keys.length; i++) { var k = TL.card.keys[i]; pk.push([k[0], [k[2], k[3]]]); sk.push([k[0], [k[1] * 100, k[1] * 100]]); }
keys(T(card).property("ADBE Position"), pk, 80); keys(T(card).property("ADBE Scale"), sk, 80);
roundMask(card, 0, 0, 3840, 2100, 40); shadow(card, 70, 40, 160);
fade(card, TL.card.t0, TL.card.t1, 0.5, 0.5);
var cb = comp.layers.addShape(); cb.name = "card border"; cb.inPoint = TL.card.t0; cb.outPoint = TL.card.t1;
adopt(cb, card, [1920, 1050]); rectShape(cb, 3840, 2100, 40, COL.white, 3, 16); fade(cb, TL.card.t0, TL.card.t1, 0.5, 0.5);

// ── 3편: 프로젝터 카드(LG 동시 녹화) — 나란히 보기 동안만. 출력이 꺼진 동안은 바탕화면 대신 그림 ──
var projL = null;
if (TL.proj) {
    var pr = TL.proj, pc = P.items.addComp("Proj", 3840, 2160, 1, TL.duration, TL.fps); pc.bgColor = [0, 0, 0];
    for (i = 0; i < pr.shots.length; i++) {
        var q = pr.shots[i]; L = pc.layers.add(imp(q.file)); L.inPoint = q.t0; L.outPoint = q.t1; L.name = "proj " + i;
        T(L).property("ADBE Position").setValue([1920, 1080]);
        if (q.fade > 0) keys(T(L).property("ADBE Opacity"), [[q.t0, 0], [q.t0 + q.fade, 100]], 40);
    }
    projL = comp.layers.add(pc); projL.name = "proj";
    T(projL).property("ADBE Anchor Point").setValue([0, 0]); T(projL).property("ADBE Position").setValue([pr.state[1], pr.state[2]]);
    T(projL).property("ADBE Scale").setValue([pr.state[0] * 100, pr.state[0] * 100]);
    roundMask(projL, 0, 0, 3840, 2160, 40); shadow(projL, 70, 40, 160);
    var ok = [[0, 0]], sx = [[0, [pr.state[1] + 120, pr.state[2]]]];
    for (i = 0; i < pr.spans.length; i++) {
        var a = pr.spans[i][0], b = pr.spans[i][1], mv = pr.move;
        ok.push([a - mv, 0]); ok.push([a, 100]); ok.push([b, 100]); ok.push([b + mv, 0]);
        sx.push([a - mv, [pr.state[1] + 120, pr.state[2]]]); sx.push([a, [pr.state[1], pr.state[2]]]); sx.push([b, [pr.state[1], pr.state[2]]]); sx.push([b + mv, [pr.state[1] + 120, pr.state[2]]]);
    }
    keys(T(projL).property("ADBE Opacity"), ok, 70); keys(T(projL).property("ADBE Position"), sx, 80);
    var pb = comp.layers.addShape(); pb.name = "proj border"; adopt(pb, projL, [1920, 1080]); rectShape(pb, 3840, 2160, 40, COL.white, 3, 18);
    keys(T(pb).property("ADBE Opacity"), ok, 70);     // 부모의 불투명도는 물려받지 않는다 — 테두리만 남았었다
    // 이름표: 위에 "YOUR SCREEN" · "PROJECTOR"
    var chips = [[pr.chipCtl, pr.split[1], pr.split[2] - 26], [pr.chipProj, pr.state[1], pr.state[2] - 26]];
    for (var c2 = 0; c2 < chips.length; c2++) {
        var ci = imp(chips[c2][0]), CL = comp.layers.add(ci); CL.name = "chip " + c2;
        T(CL).property("ADBE Anchor Point").setValue([0, ci.height]); T(CL).property("ADBE Position").setValue([chips[c2][1], chips[c2][2]]);
        var ck2 = [[0, 0]];
        for (i = 0; i < pr.spans.length; i++) { ck2.push([pr.spans[i][0] - 0.1, 0]); ck2.push([pr.spans[i][0] + 0.3, 100]); ck2.push([pr.spans[i][1] - 0.2, 100]); ck2.push([pr.spans[i][1] + 0.2, 0]); }
        keys(T(CL).property("ADBE Opacity"), ck2, 60);
    }
}

// ── 테 · 어둡게 (카드/무대의 자식, 원본 px) ──
for (i = 0; i < TL.hls.length; i++) {
    var h = TL.hls[i], par = (h.parent === "stage") ? stage : (h.parent === "proj") ? projL : card, r = h.rect, s = h.s, col = COL[h.color] || COL.indigo;
    var W = 3840, Hh = (h.parent === "stage" || h.parent === "proj") ? 2160 : 2100;
    var pad = h.fill ? 0 : 10 / s, rad = h.fill ? 6 / s : 14 / s;     // 가리개는 여백 없이 — 위 메뉴 이름을 덮지 않게
    if (h.dim) {
        var D = comp.layers.addSolid([0, 0, 0], "dim", W, Hh, 1, TL.duration); D.inPoint = h.t0; D.outPoint = h.t1;
        adopt(D, par, [W / 2, Hh / 2]);
        roundMask(D, r[0] - pad, r[1] - pad, r[2] + 2 * pad, r[3] + 2 * pad, Math.min(rad, (r[3] + 2 * pad) / 2), true);
        fade(D, h.t0, h.t1, 0.25, 0.25, 58);
    }
    var B = comp.layers.addShape(); B.name = "hl " + i; B.inPoint = h.t0; B.outPoint = h.t1;
    adopt(B, par, [r[0] + r[2] / 2, r[1] + r[3] / 2]);
    rectShape(B, r[2] + 2 * pad, r[3] + 2 * pad, Math.min(rad, (r[3] + 2 * pad) / 2), col, 7 / s);
    if (h.fill) { var fl = B.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Fill");
                  fl.property("ADBE Vector Fill Color").setValue(col); fl.property("ADBE Vector Fill Opacity").setValue(h.fill); }
    if (!h.fill) shadow(B, 85, 0, 36, col);
    fade(B, h.t0, h.t1, 0.2, 0.2);
}

// ── 그림 넣기(매뉴얼 화면 등) — 창 위에 뜨는 카드 ──
for (i = 0; i < (TL.imgs || []).length; i++) {
    var im = TL.imgs[i], it = imp(im.file); L = comp.layers.add(it); L.name = "img " + i; L.inPoint = im.t0; L.outPoint = im.t1;
    var sc = Math.min(2600 / it.width, 1700 / it.height) * 100;
    T(L).property("ADBE Position").setValue([1920, 1060]);
    keys(T(L).property("ADBE Scale"), [[im.t0, [sc * 0.94, sc * 0.94]], [im.t0 + 0.35, [sc, sc]]], 70);
    roundMask(L, 0, 0, it.width, it.height, 24); shadow(L, 80, 40, 160); fade(L, im.t0, im.t1, 0.3, 0.3);
    var dm = comp.layers.addSolid([0, 0, 0], "img dim", 3840, 2160, 1, TL.duration); dm.inPoint = im.t0; dm.outPoint = im.t1; dm.moveAfter(L);
    fade(dm, im.t0, im.t1, 0.3, 0.3, 55);
    if (im.chip) { var ch = comp.layers.add(imp(im.chip)); ch.inPoint = im.t0 + 0.2; ch.outPoint = im.t1; T(ch).property("ADBE Anchor Point").setValue([0, 0]);
                   T(ch).property("ADBE Position").setValue([1920 - it.width * sc / 200, 1060 - it.height * sc / 200 - 100]); fade(ch, im.t0 + 0.2, im.t1, 0.2, 0.3); }
}

// ── 클릭 링 ──
for (i = 0; i < TL.clicks.length; i++) {
    var ck = TL.clicks[i], K = comp.layers.addShape(); K.name = "click"; K.inPoint = ck.t; K.outPoint = ck.t + 0.5;
    adopt(K, card, [ck.x, ck.y]);
    var kg = K.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"), kv = kg.property("ADBE Vectors Group");
    var el = kv.addProperty("ADBE Vector Shape - Ellipse"), rr = 150 / (ck.s || 0.86);
    keys(el.property("ADBE Vector Ellipse Size"), [[ck.t, [rr * 0.15, rr * 0.15]], [ck.t + 0.45, [rr, rr]]], 30);
    var ks = kv.addProperty("ADBE Vector Graphic - Stroke");
    ks.property("ADBE Vector Stroke Color").setValue(COL.indigo); ks.property("ADBE Vector Stroke Width").setValue(7 / (ck.s || 0.86));
    keys(T(K).property("ADBE Opacity"), [[ck.t, 95], [ck.t + 0.45, 0]], 30);
}

// ── 이름표 + 선 (화면 좌표) ──
for (i = 0; i < TL.lbls.length; i++) {
    var lb = TL.lbls[i];
    if (lb.wire) {
        var w = lb.wire, horiz = (w[3] === null), len = horiz ? Math.abs(w[2] - w[0]) : Math.abs(w[3] - w[1]);
        if (len > 4) {
            var S = comp.layers.addSolid(COL.white, "wire", horiz ? Math.round(len) : 3, horiz ? 3 : Math.round(len), 1, TL.duration);
            S.inPoint = lb.t0 - 0.1; S.outPoint = lb.t1;
            if (horiz) {
                var x0 = Math.min(w[0], w[2]); T(S).property("ADBE Anchor Point").setValue([w[0] <= w[2] ? 0 : len, 1.5]);
                T(S).property("ADBE Position").setValue([w[0], w[1]]);
                keys(T(S).property("ADBE Scale"), [[lb.t0 - 0.1, [0, 100]], [lb.t0 + 0.12, [100, 100]]], 60);
            } else {
                T(S).property("ADBE Anchor Point").setValue([1.5, w[1] <= w[3] ? 0 : len]);
                T(S).property("ADBE Position").setValue([w[0], w[1]]);
                keys(T(S).property("ADBE Scale"), [[lb.t0 - 0.1, [100, 0]], [lb.t0 + 0.12, [100, 100]]], 60);
            }
            fade(S, lb.t0 - 0.1, lb.t1, 0, 0.2);
        }
    }
    L = comp.layers.add(imp(lb.file)); L.name = "lbl " + i; L.inPoint = lb.t0; L.outPoint = lb.t1;
    T(L).property("ADBE Anchor Point").setValue([0, 0]);
    var dx = lb.side === "right" ? -26 : lb.side === "left" ? 26 : 0, dy = lb.side === "below" ? -26 : lb.side === "above" ? 26 : 0;
    keys(T(L).property("ADBE Position"), [[lb.t0, [lb.x + dx, lb.y + dy]], [lb.t0 + 0.22, [lb.x, lb.y]]], 70);
    fade(L, lb.t0, lb.t1, 0.18, 0.2);
}

// ── 자막 ──
for (i = 0; i < TL.caps.length; i++) {
    var cp = TL.caps[i]; L = comp.layers.add(imp(cp.file)); L.name = "cap " + i; L.inPoint = cp.t0; L.outPoint = cp.t1;
    keys(T(L).property("ADBE Position"), [[cp.t0, [cp.x, cp.y + 16]], [cp.t0 + 0.25, [cp.x, cp.y]]], 70);
    fade(L, cp.t0, cp.t1, 0.2, 0.25);
}

// ── 대사 자막 ──
for (i = 0; i < (TL.subs || []).length; i++) {
    var sbt = TL.subs[i]; L = comp.layers.add(imp(sbt.file)); L.name = "sub"; L.inPoint = sbt.t0; L.outPoint = sbt.t1;
    T(L).property("ADBE Position").setValue([sbt.x, sbt.y]); fade(L, sbt.t0, sbt.t1, 0.08, 0.08);
}

// ── 위쪽 그늘 + 챕터 태그 · 진행 막대 ──
var scr = comp.layers.addSolid(VOID, "top scrim", 3840, 260, 1, TL.duration); T(scr).property("ADBE Position").setValue([1920, 130]);
scr.inPoint = TL.tags[0].t0; scr.outPoint = TL.tags[TL.tags.length - 1].t1;
var gr = scr.property("ADBE Effect Parade").addProperty("ADBE Linear Wipe"); gr.property(1).setValue(50); gr.property(2).setValue(0); gr.property(3).setValue(220);
keys(T(scr).property("ADBE Opacity"), [[scr.inPoint, 0], [scr.inPoint + 0.5, 82], [scr.outPoint - 0.5, 82], [scr.outPoint, 0]]);
for (i = 0; i < TL.tags.length; i++) {
    var tg = TL.tags[i]; L = comp.layers.add(imp(tg.file)); L.name = tg.prog ? "prog" : "tag"; L.inPoint = tg.t0; L.outPoint = tg.t1;
    T(L).property("ADBE Anchor Point").setValue([0, 0]);
    if (tg.prog) { T(L).property("ADBE Position").setValue([tg.x, tg.y]); fade(L, tg.t0, tg.t1, 0.3, 0.3); }
    else { keys(T(L).property("ADBE Position"), [[tg.t0, [tg.x - 46, tg.y]], [tg.t0 + 0.4, [tg.x, tg.y]]], 75); fade(L, tg.t0, tg.t1, 0.3, 0.3); }
}

// ── 타이틀 · 엔드 카드 (맨 위) ──
var ti = holdLast(TL.title.dir, 0, TL.title.t1);
fade(ti[1], ti[1].inPoint, TL.title.t1, 0, 0.6);
var en = holdLast(TL.end.dir, TL.end.t0, TL.duration);
fade(en[0], TL.end.t0, en[2], 0.5, 0);

// ── 소리 ──
for (i = 0; i < TL.voice.length; i++) { var vo = TL.voice[i]; L = comp.layers.add(imp(vo.file)); L.startTime = vo.t; L.name = "vo"; }
if (TL.music) { L = comp.layers.add(imp(TL.music)); L.startTime = 0; L.outPoint = TL.duration; L.name = "music"; }
for (i = 0; i < (TL.sfx || []).length; i++) { var sx = TL.sfx[i]; L = comp.layers.add(imp(sx.file)); L.startTime = sx.t; L.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([sx.level || 0, sx.level || 0]); }

for (i = 0; i < (TL.checks || []).length; i++)
    comp.saveFrameToPng(TL.checks[i], new File(OUT_DIR + "/v2-check-" + ("0000" + Math.round(TL.checks[i] * 10)).slice(-4) + ".png"));

var rq = P.renderQueue.items.add(comp), om = rq.outputModule(1);
try { om.applyTemplate("H.264 - Match Render Settings - 40 Mbps"); } catch (e1) { om.applyTemplate("H.264 - Match Render Settings - 15 Mbps"); }
om.file = new File(OUT_DIR + "/" + OUT_NAME);
P.save(new File(OUT_DIR + "/" + OUT_NAME + ".aep"));
// 에펙을 켠 채로 바로 렌더한다(끄고 aerender 로 다시 읽을 까닭이 없다) — RENDER_NOW 가 참이면
if (typeof RENDER_NOW !== "undefined" && RENDER_NOW) P.renderQueue.render();
logTo(OUT_DIR + "/build.log", "ok: " + comp.numLayers + " layers, " + TL.clips.length + " clips, " + TL.voice.length + " voice, " + TL.hls.length + " hl, " + TL.lbls.length + " lbl");
