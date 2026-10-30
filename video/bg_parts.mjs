// 움직이는 배경 조각을 epNN/parts2/ 에 — bg-grid.png(3840×2160) · bg-o/p/g.png(5760×3240, 투명)
import puppeteer from 'puppeteer-core'; import { pathToFileURL } from 'node:url'; import path from 'node:path';
const ep = process.argv[2]; const out = path.resolve(ep, 'parts2');
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 5760, height: 5600 });
await p.goto(pathToFileURL(path.resolve('bgparts.html')).href); await p.waitForFunction('window.__ready === true');
for (const [sel, f] of [['#grid', 'bg-grid.png'], ['#o', 'bg-o.png'], ['#p', 'bg-p.png'], ['#g', 'bg-g.png']]) {
  // 빛 번짐 캔버스는 서로 겹쳐 있다 — 찍을 것만 보이게(겹친 채 찍으면 셋이 다 들어간다)
  await p.evaluate(s => document.querySelectorAll('.cv').forEach(e => e.style.visibility = ('#' + e.id === s) ? 'visible' : 'hidden'), sel);
  await (await p.$(sel)).screenshot({ path: path.join(out, f), omitBackground: true });
}
await b.close(); console.log('bg parts →', out);
