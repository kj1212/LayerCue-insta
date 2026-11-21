import puppeteer from 'puppeteer-core'; import path from 'node:path'; import url from 'node:url';
const here = path.dirname(url.fileURLToPath(import.meta.url));
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
await p.goto('file://' + path.join(here, 'thumb.html')); await p.evaluate(() => document.fonts.ready);
await (await p.$('#t')).screenshot({ path: path.join(here, 'out', 'thumbnail.png') }); await b.close(); console.log('thumb ok');
