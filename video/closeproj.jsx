// 열린 프로젝트를 저장하지 않고 닫는다 — 변환 중인 푸티지 파일을 AE 가 다시 읽으며 「damaged」 경고를 띄우지 않게.
//   ./ae.sh closeproj
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
logTo(OUT_DIR + "/build.log", "closed");
