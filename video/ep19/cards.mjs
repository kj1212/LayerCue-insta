// 19편 기능 카드 PNG — node ep19/cards.mjs → ep19/media/card-s1.png …
import puppeteer from 'puppeteer-core'; import path from 'node:path'; import url from 'node:url';
const here = path.dirname(url.fileURLToPath(import.meta.url));
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1900, height: 860 });
for (const id of ['s1', 's2', 's3', 's4', 's5', 's6']) {
  await p.goto('file://' + path.join(here, 'cards.html') + '?id=' + id); await p.waitForFunction('window.__ok === true');
  await (await p.$('#c')).screenshot({ path: path.join(here, 'media', `card-${id}.png`), omitBackground: true });
}
await b.close(); console.log('cards ok');
