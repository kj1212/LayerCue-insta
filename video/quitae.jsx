// After Effects 를 끈다 — 열린 프로젝트는 저장하지 않고 닫는다(빌드한 프로젝트는 이미 저장돼 있다). 렌더는 aerender 가 따로 하니 GUI 는 필요 없다.
//   ./ae.sh quitae
if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
logTo(OUT_DIR + "/build.log", "quit");
app.quit();
