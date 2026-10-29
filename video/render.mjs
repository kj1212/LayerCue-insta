// motion.html 을 한 프레임씩 찍어 PNG 묶음으로 — AE 가 이미지 시퀀스로 불러간다.
//   node render.mjs open [fps]   → frames/open/00000.png …
//   node render.mjs end  [fps]   → frames/end/00000.png …
// 이 맥의 Chrome 을 그대로 쓴다(puppeteer-core). 화면 녹화가 아니라 시간을 넘기며 찍으므로 프레임이 튀지 않는다.
import puppeteer from 'puppeteer-core';
import { mkdirSync, rmSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const part = process.argv[2] || 'open';
const fps = Number(process.argv[3] || 30);
const out = path.join(here, 'frames', part);
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true, args: ['--allow-file-access-from-files', '--hide-scrollbars'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
await page.evaluateOnNewDocument(() => { window.__manual = true; });
await page.goto(pathToFileURL(path.join(here, 'motion.html')).href + `?part=${part}`);
await page.waitForFunction('window.__ready === true');
const dur = await page.evaluate('window.DUR');
const n = Math.round(dur * fps);
const stage = await page.$('#stage');
for (let i = 0; i < n; i++) {
  await page.evaluate(t => window.render(t), i / fps);
  await stage.screenshot({ path: path.join(out, String(i).padStart(5, '0') + '.png') });
}
await browser.close();
console.log(`${part}: ${n} frames @ ${fps}fps → ${out}`);
