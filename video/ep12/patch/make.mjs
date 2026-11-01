// 12편: macOS 가 한국어로 붙인 오디오 기기 이름(MacBook Pro 스피커)을 영어로 덮는 패치 PNG — 앱 글꼴(Pretendard JP, 22 px, wght W)로
//   W=360 node make.mjs   (DOM 글자 + font-variation-settings — canvas 는 굵기가 100 단위로 뭉개졌다)
// 글꼴: cp ~/projects/LayerCue-film-0912/qml/assets/fonts/PretendardJPVariable.ttf ep12/patch/
import puppeteer from 'puppeteer-core'; import fs from 'node:fs';
const W = +(process.env.W || 360);
const P = [   // name, rect x,y,w,h (캡처 px), 배경, 글자색, 글자 시작 x, 기준선 y, 글
  ['status', 1272, 2104, 72, 36, 37, 248, 1276.5, 2128.6, 'Spe…'],
  ['row1', 1314, 1846, 130, 36, 30, 160, 1319.5, 1870.6, 'Speakers'],
  ['row1h', 1314, 1846, 130, 36, 38, 160, 1319.5, 1870.6, 'Speakers'],
  ['row2', 1150, 1924, 130, 34, 30, 248, 1155.5, 1948.6, 'Speakers'],
  ['row2h', 1150, 1924, 130, 34, 38, 248, 1155.5, 1948.6, 'Speakers'],
];
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 400, height: 100, deviceScaleFactor: 1 });
for (const [name, x, y, w, h, bg, fg, tx, by, text] of P) {
  // 기준선: Pretendard ascender 0.927 em → 22 px 에서 줄 머리부터 기준선까지 ≈ 20.4 px (line-height 1)
  await p.setContent(`<style>@font-face{font-family:PJ;src:url(file://${process.cwd()}/PretendardJPVariable.ttf)}
    body{margin:0;background:rgb(${bg},${bg},${bg})} #t{position:absolute;left:${tx - x}px;top:${by - y - 16.6}px;font:22px/1 PJ;font-variation-settings:'wght' ${W};-webkit-font-smoothing:antialiased;color:rgb(${fg},${fg},${fg});white-space:nowrap}</style><div id="t">${text}</div>`);
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: name + '.png', clip: { x: 0, y: 0, width: w, height: h } });
}
await b.close(); console.log('patches wght', W);
