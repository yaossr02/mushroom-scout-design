// Local-only browser check. No approvals, App changes or network writes.
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
(async()=>{
 const repo=path.resolve(__dirname,'../../../../..');
 const server=http.createServer((req,res)=>{
  const f=path.resolve(repo,decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(1));
  if(!f.startsWith(repo+path.sep)){res.writeHead(403);return res.end()}
  fs.readFile(f,(e,data)=>{
   if(e){res.writeHead(404);return res.end()}
   res.setHeader('Content-Type',f.endsWith('.png')?'image/png':f.endsWith('.json')?'application/json':'text/html; charset=utf-8');res.end(data)
  });
 });
 await new Promise(ok=>server.listen(0,'127.0.0.1',ok));let browser;
 try{
  browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});
  const page=await browser.newPage({viewport:{width:1500,height:1000},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/brand/ui/illustrated-v1/review/batch2-batch3-v1/index.html');
  await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
  await page.evaluate(()=>document.fonts.ready);
  const result=await page.evaluate(()=>({
   imageCount:document.images.length,
   broken:[...document.images].filter(i=>!i.naturalWidth).length,
   circles:[...new Set([...document.querySelectorAll('.circle')].map(i=>i.getBoundingClientRect().width))],
   floatbarCounts:[...document.querySelectorAll('.floatrow')].map(i=>i.querySelectorAll('.circle').length),
   floatIconSizes:[...new Set([...document.querySelectorAll('.floatrow img')].map(i=>i.width))],
   mapRightCounts:[...document.querySelectorAll('.mapbuttons')].map(i=>i.querySelectorAll('.circle').length),
   mapTopCounts:[...document.querySelectorAll('.topbuttons')].map(i=>i.querySelectorAll('.circle').length),
   mapMoreCounts:[...document.querySelectorAll('.morebutton')].map(i=>i.querySelectorAll('.circle').length),
   mapIconSizes:[...new Set([...document.querySelectorAll('.mapscene img')].map(i=>i.width))],
   blindCount:document.querySelectorAll('.blind img').length,
   blindHasNoAltText:[...document.querySelectorAll('.blind img')].every(i=>i.alt===''),
   answersClosed:!document.querySelector('details').open
  }));
  assert.equal(result.broken,0);assert.deepEqual(errors,[]);assert.deepEqual(result.circles,[40]);
  assert.deepEqual(result.floatbarCounts,[16,16]);assert.deepEqual(result.floatIconSizes,[24,28]);
  assert.deepEqual(result.mapRightCounts,[9,9]);assert.deepEqual(result.mapTopCounts,[2,2]);assert.deepEqual(result.mapMoreCounts,[1,1]);assert.deepEqual(result.mapIconSizes,[32]);
  assert.equal(result.blindCount,44);assert(result.blindHasNoAltText);assert(result.answersClosed);
  for(let i=0;i<2;i++){
   await page.locator('.floatrow').nth(i).screenshot({path:path.join(__dirname,`browser-floatbar-${[24,28][i]}dp-1x.png`)});
   await page.locator('.mapscene').nth(i).screenshot({path:path.join(__dirname,`browser-map-${['A','B'][i]}-32dp-1x.png`)});
  }
  await page.selectOption('select[data-choice="Collapse"]','B');
  assert(await page.locator('img[data-icon="Expand"]').evaluateAll(nodes=>nodes.every(i=>i.src.includes('Expand-B-v1'))));
  await page.selectOption('select[data-choice="ReturnToApp"]','B');
  assert(await page.locator('img[data-icon="ReturnToApp"]').evaluateAll(nodes=>nodes.every(i=>i.src.includes('ReturnToApp-B-v1'))));
  result.collapseExpandLinkedSwitch='passed';result.returnToAppSwitch='passed';result.pageErrors=errors;result.date='2026-11-05';result.status='passed';
  fs.writeFileSync(path.join(__dirname,'browser-layout-check.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result));
 }finally{if(browser)await browser.close();await new Promise(ok=>server.close(ok))}
})().catch(e=>{console.error(e);process.exit(1)});
