// 시리즈 썸네일(A안 · 층 판) — node thumb.mjs <ep> <title(html)> <plate.png> <word> <out.png>
import puppeteer from 'puppeteer-core';
import path from 'node:path';
const [ep, title, img, word, out, top] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const pg = await b.newPage(); await pg.setViewport({ width: 1400, height: 800, deviceScaleFactor: 2 });
const q = new URLSearchParams({ ep, title, img: 'file://' + path.resolve(img), word });
if (top) q.set('top', 'file://' + path.resolve(top));
await pg.goto('file://' + path.resolve('thumbs.html') + '?' + q.toString());
await pg.evaluate(() => document.fonts.ready);
await (await pg.$('#A')).screenshot({ path: out }); await b.close(); console.log('thumb', out);
