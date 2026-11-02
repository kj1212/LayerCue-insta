// 숏츠 글판 — parts.html 의 #id 하나씩만 보이게 해서 투명 PNG 로
import puppeteer from 'puppeteer-core'; import path from 'node:path';
const ids = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1200, height: 1400 });
await p.goto('file://' + path.resolve('parts.html')); await p.evaluate(() => document.fonts.ready);
for (const id of ids) {
  await p.evaluate(id => { document.querySelectorAll('.p').forEach(e => e.style.display = e.id === id ? 'inline-block' : 'none'); }, id);
  await (await p.$('#' + id)).screenshot({ path: 'parts/' + id + '.png', omitBackground: true });
}
await b.close(); console.log('parts', ids.length);
