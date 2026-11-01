import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await b.newPage();
await p.goto('file://' + process.cwd() + '/blank.html');
const r = await p.evaluate(async () => {
  const f = new FontFace('PJ', 'url(PretendardJPVariable.ttf)', { weight: '100 900' }); await f.load(); document.fonts.add(f);
  const c = document.createElement('canvas').getContext('2d'); const out = [];
  for (const w of [400, 450, 500]) for (const s of [21, 21.5, 22, 22.5, 23]) {
    c.font = `${w} ${s}px PJ`; const m = c.measureText('MacBook'); const M = c.measureText('M');
    out.push([w, s, m.width.toFixed(1), (M.actualBoundingBoxAscent).toFixed(1), c.measureText('System default · MacBook Pro ').width.toFixed(1)]);
  }
  return out;
});
console.log(r.map(x => x.join(' ')).join('\n')); await b.close();
