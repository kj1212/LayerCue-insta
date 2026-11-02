// 숏츠 표지(1080×1920) — 가운데에 훅 두 줄(목록에서 가운데만 보여도 읽히게), 위·아래에 그 편 화면을 흐리게
//   node shorts/covers.mjs <id> <a> <b> <ep> <top.png> <bot.png> <out.jpg>  …(7개씩 반복)
import puppeteer from 'puppeteer-core'; import path from 'node:path';
const A = process.argv.slice(2);
const br = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
const p = await br.newPage(); await p.setViewport({ width: 1080, height: 1920 });
for (let i = 0; i < A.length; i += 7) {
  const [id, a, b, ep, top, bot, out] = A.slice(i, i + 7);
  const q = new URLSearchParams({ a, b, ep, top: 'file://' + path.resolve(top), bot: 'file://' + path.resolve(bot) });
  await p.goto('file://' + path.resolve('shorts/cover.html') + '?' + q); await p.waitForFunction('window.__ready === true');
  await (await p.$('#c')).screenshot({ path: out, type: 'jpeg', quality: 92 }); console.log('cover', id);
}
await br.close();
