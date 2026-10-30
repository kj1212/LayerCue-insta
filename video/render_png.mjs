// HTML 한 장을 투명 PNG 로 찍는다 — 로고·카드·자막판 같은 정지 그래픽용.
//   node render_png.mjs <html> <selector> <out.png> [scale=1]
// 이 맥의 Chrome 을 그대로 쓴다(puppeteer-core). 배경은 비워 둔다(omitBackground).
import puppeteer from 'puppeteer-core';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const [html, selector, out, scaleArg] = process.argv.slice(2);
const scale = Number(scaleArg || 1);
const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true, args: ['--allow-file-access-from-files', '--hide-scrollbars'],
});
const page = await browser.newPage();
await page.setViewport({ width: 4000, height: 3000, deviceScaleFactor: scale });
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.evaluate(() => document.fonts.ready);
const el = await page.$(selector);
await el.screenshot({ path: out, omitBackground: true });
await browser.close();
console.log('wrote', out);
