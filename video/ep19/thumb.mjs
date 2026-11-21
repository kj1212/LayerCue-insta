// 19편 썸네일 — node ep19/thumb.mjs [a b c] → ep19/out/thumb-<v>.png (첫째를 thumbnail.png 로도)
import puppeteer from 'puppeteer-core'; import path from 'node:path'; import url from 'node:url'; import fs from 'node:fs';
const here = path.dirname(url.fileURLToPath(import.meta.url)); const vs = process.argv.slice(2).length ? process.argv.slice(2) : ['a'];
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
for (const v of vs) { await p.goto('file://' + path.join(here, 'thumb.html') + '?v=' + v); await p.evaluate(() => document.fonts.ready);
  await (await p.$('#' + v)).screenshot({ path: path.join(here, 'out', `thumb-${v}.png`) }); }
fs.copyFileSync(path.join(here, 'out', `thumb-${vs[0]}.png`), path.join(here, 'out', 'thumbnail.png'));
await b.close(); console.log('thumbs', vs.join(' '));
