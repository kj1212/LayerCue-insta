import puppeteer from 'puppeteer-core'; import path from 'node:path'; import {mkdirSync} from 'node:fs';
const here=path.resolve('ep06'); const out=path.join(here,'media/Prize media'); mkdirSync(path.join(here,'media/kf'),{recursive:true});
const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
const p=await b.newPage(); await p.setViewport({width:1920,height:1080});
await p.goto('file://'+path.join(here,'demo-media.html')); await p.waitForFunction('window.__ready===true');
for (const id of ['crest','mark']){ await p.evaluate(i=>{document.getElementById('wash').style.display='none';document.querySelectorAll('.logo').forEach(e=>e.style.display=e.id===i?'block':'none')},id);
  await (await p.$('#full')).screenshot({path:path.join(out,id==='crest'?'school-crest.png':'sponsor-mark.png'),omitBackground:true});}
await p.evaluate(()=>{document.getElementById('wash').style.display='block';document.querySelectorAll('.logo').forEach(e=>e.style.display='none')});
for(let i=0;i<300;i++){await p.evaluate(t=>window.frame(t),i/30); await p.screenshot({path:path.join(here,'media/kf',String(i).padStart(4,'0')+'.png')});}
await b.close(); console.log('ok');
