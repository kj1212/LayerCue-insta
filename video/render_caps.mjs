// 자막 PNG 묶음 — JSON [{ "file": "cap-01.png", "text": "...", "keys": "⌘1 · Ctrl+1", "color": "amber" }, …] 를 받아
//   node render_caps.mjs <captions.html> <list.json> <outdir>
import puppeteer from 'puppeteer-core';
import { readFileSync, mkdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const [html, listFile, outDir] = process.argv.slice(2);
const list = JSON.parse(readFileSync(listFile, 'utf8'));
mkdirSync(outDir, { recursive: true });
const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true, args: ['--allow-file-access-from-files', '--hide-scrollbars'],
});
const page = await browser.newPage();
await page.setViewport({ width: 3840, height: 600, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.evaluate(() => document.fonts.ready);
for (const c of list) {
  await page.evaluate((t, k, col) => window.setCap(t, k, col), c.text, c.keys || '', c.color || '');
  const el = await page.$('#cap');
  await el.screenshot({ path: path.join(outDir, c.file), omitBackground: true });
}
await browser.close();
console.log('captions:', list.length, '→', outDir);
