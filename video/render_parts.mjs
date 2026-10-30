// 그래픽 조각 묶음 — JSON [{ "kind": "lbl"|"cap"|"tag"|"prog", "file": "...png", "args": [...] }, …] → 투명 PNG, 크기를 sizes.json 에
//   node render_parts.mjs <parts.html> <list.json> <outdir>
import puppeteer from 'puppeteer-core';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const [html, listFile, outDir] = process.argv.slice(2);
const list = JSON.parse(readFileSync(listFile, 'utf8')); mkdirSync(outDir, { recursive: true });
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files', '--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 3840, height: 1200, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.evaluate(() => document.fonts.ready);
const FN = { lbl: 'setLbl', cap: 'setCap', tag: 'setTag', prog: 'setProg' }, sizes = {};
for (const it of list) {
  await page.evaluate((fn, args) => window[fn](...args), FN[it.kind], it.args);
  const el = await page.$('#' + it.kind);
  const bb = await el.boundingBox();
  await el.screenshot({ path: path.join(outDir, it.file), omitBackground: true });
  sizes[it.file] = [Math.round(bb.width), Math.round(bb.height)];
}
writeFileSync(path.join(outDir, 'sizes.json'), JSON.stringify(sizes, null, 1));
await browser.close(); console.log('parts:', list.length, '→', outDir);
