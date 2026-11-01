import puppeteer from 'puppeteer-core'; import path from 'node:path';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const p = await b.newPage(); await p.goto('file://' + path.resolve('programme.html'), { waitUntil: 'networkidle0' });
await p.pdf({ path: 'Summit-Programme.pdf', width: '1920px', height: '1080px', printBackground: true, pageRanges: '1-6' }); await b.close(); console.log('pdf ok');
