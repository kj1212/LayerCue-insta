// 시리즈 썸네일 — node thumb.mjs <ep> <title(html)> <img.png> <word> <out.png> [top.png] [variant=A]
//   A 층 판(1편) · D 설치(2편: img = DMG 창, top = 앱 아이콘). 편마다 다른 그림을 쓴다.
import puppeteer from 'puppeteer-core';
import path from 'node:path';
const [ep, title, img, word, out, top, variant = 'A'] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const pg = await b.newPage(); await pg.setViewport({ width: 1400, height: 800, deviceScaleFactor: 2 });
const q = new URLSearchParams({ ep, title, img: 'file://' + path.resolve(img), word });
if (top && variant === 'A') q.set('top', 'file://' + path.resolve(top));
if (top) q.set('icon', 'file://' + path.resolve(top));
await pg.goto('file://' + path.resolve('thumbs.html') + '?' + q.toString());
await pg.evaluate(() => document.fonts.ready);
await (await pg.$('#' + variant)).screenshot({ path: out }); await b.close(); console.log('thumb', out);
