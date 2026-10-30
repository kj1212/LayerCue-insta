// projparts.html 의 #off · #ctl · #prj 를 PNG 로(투명 바탕)
import puppeteer from 'puppeteer-core'; import { pathToFileURL } from 'node:url'; import path from 'node:path';
const here = path.resolve(process.argv[2] || 'ep03');     // node proj_parts.mjs ep03
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 3840, height: 2600 });
await p.goto(pathToFileURL(path.join(here, 'projparts.html')).href); await p.waitForFunction('window.__ready === true');
for (const [sel, out] of [['#off', 'proj-off.png'], ['#ctl', 'chip-ctl.png'], ['#prj', 'chip-proj.png']]) {
  const el = await p.$(sel); await el.screenshot({ path: path.join(here, out), omitBackground: true });
}
await b.close(); console.log('ok');
