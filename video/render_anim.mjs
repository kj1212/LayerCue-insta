// 움직이는 HTML 한 판을 프레임 묶음으로 — window.render(t) · window.DUR · window.__ready 를 갖춘 페이지.
//   node render_anim.mjs <html> <selector> <fps> <outdir> [scale=1] [width=3840] [height=2160]
import puppeteer from 'puppeteer-core';
import { mkdirSync, rmSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const [html, sel, fpsArg, out, scaleArg, wArg, hArg] = process.argv.slice(2);
const fps = +fpsArg, scale = +(scaleArg || 1), W = +(wArg || 3840), H = +(hArg || 2160);
rmSync(out, { recursive: true, force: true }); mkdirSync(out, { recursive: true });
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files', '--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: scale });
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.waitForFunction('window.__ready === true');
const n = Math.round((await page.evaluate('window.DUR')) * fps), el = await page.$(sel);
for (let i = 0; i < n; i++) {
  await page.evaluate(t => window.render(t), i / fps);
  await el.screenshot({ path: path.join(out, String(i).padStart(5, '0') + '.png') });
}
await browser.close(); console.log(`${n} frames @ ${fps} → ${out}`);
