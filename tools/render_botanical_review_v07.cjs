// Serve only this checkout to Chromium, preserve source PNGs, verify real interactions.
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
(async()=>{
 const root=path.resolve(__dirname,'..'),pack=path.join(root,'brand/ui/v0.7-botanical');
 const server=http.createServer((req,res)=>{try{const relative=decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(1),file=path.resolve(root,relative);if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end()}const data=fs.readFileSync(file);res.setHeader('Content-Type',file.endsWith('.png')?'image/png':file.endsWith('.svg')?'image/svg+xml':'text/html; charset=utf-8');res.end(data)}catch{res.writeHead(404);res.end()}});
 await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve)});
 let b;
 try{
  b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});
  const base='http://127.0.0.1:'+server.address().port,p=await b.newPage({viewport:{width:2100,height:1200},deviceScaleFactor:1});
  const catalog=JSON.parse(fs.readFileSync(path.join(pack,'catalog.json'))), basinCount=catalog.semantics.find(s=>s.id==='GoldBasin').candidate_options.length, count=catalog.semantics.reduce((n,s)=>n+(s.candidate_options?.length||1),1);
  const errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(`${r.status()} ${r.url()}`)});
  await p.goto(base+'/brand/ui/v0.7-botanical/review/index.html',{waitUntil:'networkidle'});
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await p.evaluate(()=>document.fonts.ready);
  assert.equal(await p.locator('article').count(),count);assert.equal(await p.locator('.hero').count(),count);assert.equal(await p.locator('.sizes img').count(),count*3);assert.equal(await p.locator('button').count(),count);
  for(const button of await p.locator('button').all()){await button.click();assert.equal(await button.getAttribute('aria-pressed'),'false');await button.click();assert.equal(await button.getAttribute('aria-pressed'),'true')}
  await p.fill('#search','相簿');assert.equal(await p.locator('article:visible').count(),1);await p.fill('#search','LightSpeed');assert.equal(await p.locator('article:visible').count(),1);await p.fill('#search','拉金盆');assert.equal(await p.locator('article:visible').count(),basinCount);await p.fill('#search','GoldBasin');assert.equal(await p.locator('article:visible').count(),basinCount);await p.fill('#search','');assert.equal(await p.locator('article:visible').count(),count);
  await p.evaluate(()=>document.body.classList.add('capture'));await p.screenshot({path:path.join(pack,'review/all-icons.png'),fullPage:true});
  await p.setViewportSize({width:2400,height:1200});await p.goto(base+'/brand/reviews/overview/all-icons-overview.html',{waitUntil:'networkidle'});await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:path.join(root,'brand/reviews/overview/all-icons-overview.png'),fullPage:true});
  assert.deepEqual(errors,[]);const report={source_images_decoded:true,functional_uses:catalog.semantics.length,additional_map_entry:1,hero_count:count,size_samples:count*3,state_toggles:count,chinese_and_id_search:'passed',errors,app_runtime_tested:false,browser:await b.version()};fs.writeFileSync(path.join(pack,'review/browser-check.json'),JSON.stringify(report,null,2)+'\n');console.log(report);
 }finally{if(b)await b.close();await new Promise(resolve=>server.close(resolve))}
})().catch(e=>{console.error(e);process.exit(1)});
