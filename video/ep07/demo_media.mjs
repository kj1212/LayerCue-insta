import puppeteer from 'puppeteer-core'; import path from 'node:path'; import {mkdirSync} from 'node:fs';
const here=path.resolve('ep07'); const out=path.join(here,'media/Summit media 2');
for (const d of ['kf1','kf2']) mkdirSync(path.join(here,'media',d),{recursive:true});
const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
const p=await b.newPage(); await p.goto('file://'+path.join(here,'demo-media.html')); await p.waitForFunction('window.__ready===true');
const show=id=>p.evaluate(i=>document.querySelectorAll('.f').forEach(e=>e.style.display=e.id===i?'block':'none'),id);
await show('pt'); await p.setViewport({width:1600,height:1200}); await (await p.$('#pt')).screenshot({path:path.join(here,'media/dana.png')});
await show('hl'); await p.setViewport({width:1920,height:1080});
for(let i=0;i<450;i++){await p.evaluate(t=>window.hl(t),i/30); await (await p.$('#hl')).screenshot({path:path.join(here,'media/kf1',String(i).padStart(4,'0')+'.png')});}
await show('vt'); await p.setViewport({width:1080,height:1920});
for(let i=0;i<240;i++){await p.evaluate(t=>window.vt(t),i/30); await (await p.$('#vt')).screenshot({path:path.join(here,'media/kf2',String(i).padStart(4,'0')+'.png')});}
await b.close(); console.log('ok');
