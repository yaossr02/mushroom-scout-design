const {chromium}=require('playwright');
const fs=require('fs'),http=require('http'),path=require('path'),assert=require('assert');
(async()=>{
const root=path.resolve(__dirname,'..'),server=http.createServer((req,res)=>{try{const f=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);if(!f.startsWith(root+path.sep)){res.writeHead(403);return res.end();}res.setHeader('Content-Type',f.endsWith('.png')?'image/png':f.endsWith('.svg')?'image/svg+xml':'text/html; charset=utf-8');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
await new Promise((r,j)=>{server.once('error',j);server.listen(0,'127.0.0.1',r);});let browser;
try{browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});const p=await browser.newPage({viewport:{width:1440,height:1200},deviceScaleFactor:1}),errors=[];
p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url());});const base='http://127.0.0.1:'+server.address().port+'/floatbar-C-v2/';
await p.goto(base+'index.html',{waitUntil:'networkidle'});await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await p.evaluate(()=>document.fonts.ready);
assert.equal(await p.locator('article').count(),16);assert.equal(await p.locator('.samples img').count(),48);assert.equal(await p.locator('.scene-20 .cell').count(),16);assert.equal(await p.locator('.scene-24 .cell').count(),16);
const measures=await p.locator('.scene-20 .circle').first().evaluate(el=>({circle:el.getBoundingClientRect().width,icon:el.querySelector('img').getBoundingClientRect().width}));assert.equal(measures.circle,40);assert.equal(measures.icon,20);
assert.equal(await p.locator('.scene-24 .circle img').first().evaluate(el=>el.getBoundingClientRect().width),24);
await p.screenshot({path:path.join(__dirname,'review.png'),fullPage:true});
await p.goto(base+'overview.html',{waitUntil:'networkidle'});await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:path.join(__dirname,'overview.png'),fullPage:true});
const hires=await browser.newPage({viewport:{width:1440,height:1200},deviceScaleFactor:4});await hires.goto(base+'index.html',{waitUntil:'networkidle'});await hires.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
for(const size of [20,24]){const el=hires.locator('.scene-'+size);await el.evaluate(e=>e.style.width='560px');await el.screenshot({path:path.join(__dirname,size+'dp-xxxhdpi-scene.png')});}await hires.close();assert.deepEqual(errors,[]);
fs.writeFileSync(path.join(__dirname,'browser-check.json'),JSON.stringify({status:fs.existsSync(path.join(__dirname,'approval.json'))?'approved':'candidate',new_icons:15,reused_gold_basin:1,cards:16,thumbnail_samples:48,layout_circle_css_px:40,icon_css_px:[20,24],xxxhdpi_capture_dpr:4,images_decoded:true,errors,app_runtime_tested:false,game_background:'simulated; actual screenshots not received',browser:await browser.version()},null,2)+'\n');console.log('16 cards,48 size samples,20/24dp layouts and DPR4 scenes passed; no image/script errors.');
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exit(1);});
