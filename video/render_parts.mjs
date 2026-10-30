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
// ★ 글자가 비어 있으면 글꼴을 아예 안 불러 fonts.ready 가 바로 끝난다 → 대체 글꼴로 찍혔다(2026-10-30). 쓰는 모양을 미리 불러 둔다.
await page.evaluate(async () => { for (const f of ['400 60px Archivo', '600 60px Archivo', '700 60px Archivo', '800 60px Archivo', '900 60px Archivo', '400 40px "DM Mono"', '500 40px "DM Mono"']) await document.fonts.load(f); await document.fonts.ready; });
const FN = { lbl: 'setLbl', cap: 'setCap', tag: 'setTag', prog: 'setProg', sub: 'setSub' }, sizes = {};
for (const it of list) {
  await page.evaluate((fn, args, kind) => { for (const w of document.querySelectorAll('.wrap')) w.style.display = (w.id === kind) ? 'inline-block' : 'none'; window[fn](...args); }, FN[it.kind], it.args, it.kind);   // 다른 조각의 그림자가 끼지 않게
  const el = await page.$('#' + it.kind);
  const bb = await el.boundingBox();
  await el.screenshot({ path: path.join(outDir, it.file), omitBackground: true });
  sizes[it.file] = [Math.round(bb.width), Math.round(bb.height)];
}
writeFileSync(path.join(outDir, 'sizes.json'), JSON.stringify(sizes, null, 1));
await browser.close(); console.log('parts:', list.length, '→', outDir);
