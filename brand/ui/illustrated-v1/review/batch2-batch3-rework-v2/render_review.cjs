const {chromium}=require('playwright'),http=require('http'),fs=require('fs'),path=require('path'),assert=require('assert');
(async()=>{
 const repo=path.resolve(__dirname,'../../../../..');
 const server=http.createServer((q,r)=>{const f=path.resolve(repo,decodeURIComponent(new URL(q.url,'http://localhost').pathname).slice(1));if(!f.startsWith(repo+path.sep))return r.writeHead(403).end();fs.readFile(f,(e,b)=>{if(e)return r.writeHead(404).end();r.setHeader('Content-Type',f.endsWith('.png')?'image/png':'text/html; charset=utf-8');r.end(b)})});
 await new Promise(ok=>server.listen(0,'127.0.0.1',ok));let browser;
 try{
  browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});const p=await browser.newPage({viewport:{width:1500,height:1000}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('http://127.0.0.1:'+server.address().port+'/brand/ui/illustrated-v1/review/batch2-batch3-rework-v2/index.html');await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
  const result=await p.evaluate(()=>({images:document.images.length,broken:[...document.images].filter(i=>!i.naturalWidth).length,circles:[...new Set([...document.querySelectorAll('.circle')].map(i=>i.getBoundingClientRect().width))],floatCounts:[...document.querySelectorAll('.floatrow')].map(i=>i.querySelectorAll('.circle').length),floatIcons:[...new Set([...document.querySelectorAll('.floatrow img')].map(i=>i.width))],mapRight:[...document.querySelectorAll('.right')].map(i=>i.querySelectorAll('.circle').length),mapIcons:[...new Set([...document.querySelectorAll('.mapscene img')].map(i=>i.width))]}));
  assert.deepEqual(errors,[]);assert.equal(result.broken,0);assert.deepEqual(result.circles,[40]);assert.deepEqual(result.floatCounts,[16,16]);assert.deepEqual(result.floatIcons,[24,28]);assert.deepEqual(result.mapRight,[9,9]);assert.deepEqual(result.mapIcons,[32]);
  await p.selectOption('[data-choice="Collapse"]','B');assert(await p.locator('img[data-id="Expand"]').evaluateAll(xs=>xs.every(i=>i.src.includes('Expand-B-v2'))));
  await p.selectOption('[data-choice="Feed"]','B');assert(await p.locator('img[data-id="Feed"]').evaluateAll(xs=>xs.every(i=>i.src.includes('Feed-B-v2'))));
  result.status='passed';result.date='2026-11-05';result.pageErrors=errors;result.collapseExpandLinked='passed';result.feedSwitch='passed';fs.writeFileSync(path.join(__dirname,'browser-layout-check.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
 }finally{if(browser)await browser.close();await new Promise(ok=>server.close(ok))}
})().catch(e=>{console.error(e);process.exit(1)});
