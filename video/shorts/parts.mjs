// 숏츠 글판 — <dir>/parts.html 의 .p 를 하나씩만 보이게 해서 <dir>/parts/<id>.png
import puppeteer from 'puppeteer-core'; import path from 'node:path'; import fs from 'node:fs';
const dirs = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1200, height: 1400 });
for (const d of dirs) {
  fs.mkdirSync(path.join(d, 'parts'), { recursive: true });
  await p.goto('file://' + path.resolve(d, 'parts.html')); await p.waitForFunction('window.__fit === true');
  const ids = await p.evaluate(() => [...document.querySelectorAll('.p')].map(e => e.id));
  for (const id of ids) {
    await p.evaluate(id => { document.querySelectorAll('.p').forEach(e => e.style.display = e.id === id ? 'inline-block' : 'none'); }, id);
    await (await p.$('#' + id)).screenshot({ path: path.join(d, 'parts', id + '.png'), omitBackground: true });
  }
  console.log('parts', d, ids.length);
}
await b.close();
