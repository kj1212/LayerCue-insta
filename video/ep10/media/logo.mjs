// 10편 데모용 가상 로고(투명 PNG) — node ep10/media/logo.mjs
import puppeteer from 'puppeteer-core';
import path from 'node:path';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const pg = await b.newPage(); await pg.setViewport({ width: 1400, height: 400, deviceScaleFactor: 2 });
await pg.goto('file://' + path.resolve('ep10/media/logo.html'));
await (await pg.$('#logo')).screenshot({ path: 'ep10/media/rts-logo.png', omitBackground: true });
await b.close(); console.log('logo ep10/media/rts-logo.png');
