// 쇼츠·릴스 「Ask → LayerCue → Live」 21.4 s 1080×1920 — AE 에서 조립하고 렌더 대기열(H.264)에 넣는다.
//   ./ae.sh build_short   →  render/<OUT_NAME>.aep · render/check-*.png · aerender 로 render/<OUT_NAME>.mp4
//   목소리 바꾸기: AUDIO_DIR=audio-fenrir OUT_NAME=layercue-ask-short-fenrir ./ae.sh build_short
// 재료: frames/open(0–8.6 s) · frames/end(4.4 s) — motion.html · shots/*.png — shoot.py(촬영용 LayerCue) ·
//       audio/01–09.wav — Kokoro af_bella · overlays/*.png — overlays.py
// 시간표(초): 질문 0 · 입력 3.4 · 만드는 중 6.5 | 앱 8.6 라이브러리 → 11.3 큐시트 → 12.15 첫 카드 → 12.4 클릭 | 무대 13.0 · 몽타주 14.3 | 끝 17.0
// ★ 화면 좌표(앱 창 그림 2950×1784): 라이브러리 (200,1200) · 큐시트 Tour (200,380) · 첫 카드 (645,935)

var P, comp;
var VOID = [11 / 255, 11 / 255, 13 / 255];

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
function keys(prop, list) {               // list = [[t, v], …]
    for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]);
    easeAll(prop);
}
function layer(item, tin, tout) {
    var L = comp.layers.add(item);
    L.startTime = 0; L.inPoint = tin; L.outPoint = tout;
    return L;
}
function seqLayer(item, start) {          // 이미지 시퀀스는 start 에서 시작
    var L = comp.layers.add(item);
    L.startTime = start;
    return L;
}
function T(L) { return L.property("ADBE Transform Group"); }

app.beginSuppressDialogs();
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.newProject();
P = app.project;
comp = P.items.addComp("LayerCue-ask-short", 1080, 1920, 1, 21.4, 30);
comp.bgColor = VOID;

var R = ROOT;
var openSeq = imp(R + "/frames/open/00000.png", true);
var endSeq = imp(R + "/frames/end/00000.png", true);
var app2 = imp(R + "/shots/main-02-cuesheet.png");
var app3 = imp(R + "/shots/main-03-live.png");
var ov = {}, names = ["cap-libraries", "cap-cuesheets", "cap-click", "cap-live", "live", "ripple"];
for (var i = 0; i < names.length; i++) ov[names[i]] = imp(R + "/overlays/" + names[i] + ".png");
var montage = ["start-here-1", "start-here-2", "start-here-3", "bring-it-in-2", "make-it-with-ai-2",
               "stage-output-2", "libraries-and-cue-sheets-3", "working-with-slides-5"];
var st = [];
for (var m = 0; m < montage.length; m++) st.push(imp(R + "/shots/stage-" + montage[m] + ".png"));

// ── 0 – 8.6  질문 · 입력 · 만드는 중 (HTML 프레임) ──
seqLayer(openSeq, 0);

// ── 8.6 – 12.4  앱: 라이브러리 → 큐시트 → 첫 카드 ──
var A = layer(app2, 8.6, 12.5);
A.threeDLayer = true;
T(A).property("ADBE Position").setValue([540, 860, 0]);
keys(T(A).property("ADBE Anchor Point"), [[8.6, [230, 1130, 0]], [11.0, [230, 1250, 0]], [11.35, [230, 400, 0]],
                                          [11.8, [230, 350, 0]], [12.15, [645, 935, 0]], [12.5, [650, 935, 0]]]);
keys(T(A).property("ADBE Scale"), [[8.6, [165, 165, 165]], [11.0, [185, 185, 185]], [11.8, [200, 200, 200]],
                                   [12.15, [235, 235, 235]], [12.5, [245, 245, 245]]]);
keys(T(A).property("ADBE Rotate Y"), [[8.6, -28], [9.4, -8], [12.5, -4]]);
keys(T(A).property("ADBE Opacity"), [[8.6, 0], [8.85, 100]]);

// 클릭 — 같은 자리에서 「고른 카드」 → 「송출 중인 카드」로 바뀐다
var B = layer(app3, 12.5, 13.1);
B.threeDLayer = true;
T(B).property("ADBE Position").setValue([540, 860, 0]);
T(B).property("ADBE Anchor Point").setValue([650, 935, 0]);
keys(T(B).property("ADBE Scale"), [[12.5, [245, 245, 245]], [12.8, [250, 250, 250]], [13.1, [90, 90, 90]]]);
T(B).property("ADBE Rotate Y").setValue(-4);
keys(T(B).property("ADBE Opacity"), [[12.9, 100], [13.1, 0]]);

var RP = layer(ov["ripple"], 12.4, 12.9);
T(RP).property("ADBE Position").setValue([540, 860]);
keys(T(RP).property("ADBE Scale"), [[12.4, [30, 30]], [12.9, [170, 170]]]);
keys(T(RP).property("ADBE Opacity"), [[12.4, 100], [12.9, 0]]);

// ── 13.0 – 17.0  무대: 4K 송출 화면 → 몽타주 ──
for (var s = 0; s < st.length; s++) {
    var tin = s === 0 ? 13.0 : 14.3 + (s - 1) * 0.38;
    var tout = s === st.length - 1 ? 17.0 : (s === 0 ? 14.3 + 0.12 : 14.3 + s * 0.38 + 0.12);
    var S = layer(st[s], tin, tout);
    S.threeDLayer = true;
    var fx = S.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
    fx.property(2).setValue(180);   // Opacity(0–255)
    fx.property(4).setValue(40);    // Distance
    fx.property(5).setValue(90);    // Softness
    if (s === 0) {
        keys(T(S).property("ADBE Position"), [[13.0, [540, 860, 0]]]);
        keys(T(S).property("ADBE Scale"), [[13.0, [62, 62, 62]], [13.45, [26.5, 26.5, 26.5]], [14.3, [27.5, 27.5, 27.5]]]);
        keys(T(S).property("ADBE Rotate X"), [[13.0, 14], [13.45, 0]]);
        keys(T(S).property("ADBE Opacity"), [[13.0, 0], [13.15, 100]]);
    } else {
        keys(T(S).property("ADBE Position"), [[tin, [1700, 860, 0]], [tin + 0.14, [540, 860, 0]]]);
        T(S).property("ADBE Scale").setValue([27.5, 27.5, 27.5]);
        keys(T(S).property("ADBE Rotate Y"), [[tin, -35], [tin + 0.14, 0]]);
        if (s === st.length - 1) keys(T(S).property("ADBE Scale"), [[tin, [27.5, 27.5, 27.5]], [17.0, [31, 31, 31]]]);
    }
}
var LV = layer(ov["live"], 13.2, 17.0);
T(LV).property("ADBE Position").setValue([540, 1265]);
keys(T(LV).property("ADBE Scale"), [[13.2, [0, 0]], [13.4, [112, 112]], [13.5, [100, 100]]]);

// ── 자막(소리 끄고 보는 사람) — 아래쪽, 어두운 띠 위 ──
// 띠: 검은 판에 위쪽을 넓게 흐린 마스크 — 앱 화면 위에서도 자막이 읽히게
var band = comp.layers.addSolid([0, 0, 0], "caption band", 1080, 760, 1, 21.4);
band.inPoint = 8.6; band.outPoint = 14.3;
T(band).property("ADBE Position").setValue([540, 1540]);
T(band).property("ADBE Opacity").setValue(85);
var mk = band.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
var shp = new Shape(); shp.vertices = [[-100, 260], [1180, 260], [1180, 860], [-100, 860]]; shp.closed = true;
mk.property("ADBE Mask Shape").setValue(shp);
mk.property("ADBE Mask Feather").setValue([0, 260]);
var caps = [["cap-libraries", 9.35, 11.25], ["cap-cuesheets", 11.3, 12.35], ["cap-click", 12.4, 13.05], ["cap-live", 13.1, 14.3]];
for (var c = 0; c < caps.length; c++) {
    var C = layer(ov[caps[c][0]], caps[c][1], caps[c][2]);
    T(C).property("ADBE Position").setValue([540, 1580]);
    keys(T(C).property("ADBE Opacity"), [[caps[c][1], 0], [caps[c][1] + 0.12, 100]]);
}

// ── 17.0 – 21.4  끝 (HTML 프레임) ──
seqLayer(endSeq, 17.0);

// ── 목소리 — 장면마다 한 줄씩. 목소리마다 줄 길이가 달라서, 앞 줄이 길면 다음 줄을 0.1 s 뒤로 민다 ──
var VO = [[1, 0.6], [2, 3.3], [3, 6.6], [4, 9.35], [5, 11.3], [6, 12.4], [7, 13.1], [8, 17.4], [9, 18.4]];
var prevEnd = 0;
for (var v = 0; v < VO.length; v++) {
    var a = imp(R + "/" + AUDIO_DIR + "/0" + VO[v][0] + ".wav");
    var at = Math.max(VO[v][1], prevEnd + 0.1);
    var AL = comp.layers.add(a); AL.startTime = at;
    prevEnd = at + a.duration;
}
// ── 배경음악 — 목소리 밑에 낮게. 처음 0.6 s 에 올라오고 끝 1.2 s 동안 내려간다 ──
if (MUSIC_FILE) {
    var mu = imp(MUSIC_FILE);
    var ML = comp.layers.add(mu); ML.startTime = 0; ML.outPoint = comp.duration;
    keys(ML.property("ADBE Audio Group").property("ADBE Audio Levels"),
         [[0, [-40, -40]], [0.6, [-22, -22]], [comp.duration - 1.2, [-22, -22]], [comp.duration, [-50, -50]]]);
}
if (prevEnd > comp.duration) logTo(OUT_DIR + "/build.log", "주의: 마지막 줄이 " + prevEnd.toFixed(2) + " s 에 끝난다(영상 " + comp.duration + " s)");

// 확인용 정지 장면
var checks = [1.5, 5.0, 7.2, 9.5, 11.3, 12.5, 13.6, 15.0, 19.5];
for (var q = 0; q < checks.length; q++)
    comp.saveFrameToPng(checks[q], new File(OUT_DIR + "/check-" + ("0" + Math.round(checks[q] * 10)).slice(-3) + ".png"));

// 렌더 대기열 — aerender 가 돈다
var rq = P.renderQueue.items.add(comp), om = rq.outputModule(1);
om.applyTemplate("H.264 - Match Render Settings - 15 Mbps");
om.file = new File(OUT_DIR + "/" + OUT_NAME);
P.save(new File(OUT_DIR + "/" + OUT_NAME + ".aep"));
logTo(OUT_DIR + "/build.log", "ok: " + comp.numLayers + " layers");
