// Local-only browser verification for directly referenced candidate PNGs.
const { chromium }=require('playwright');
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
(async()=>{
 const root=path.resolve(__dirname,'../../..');
 const server=http.createServer((req,res)=>{
  const file=path.resolve(root,decodeURIComponent(new URL(req.url,'http://localhost').pathname).slice(1));
  if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end()}
  fs.readFile(file,(e,data)=>{if(e){res.writeHead(404);return res.end()}res.setHeader('Content-Type',file.endsWith('.png')?'image/png':file.endsWith('.json')?'application/json':'text/html; charset=utf-8');res.end(data)})
 });
 await new Promise(ok=>server.listen(0,'127.0.0.1',ok));let browser;
 try{
  browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});
  const page=await browser.newPage({viewport:{width:1500,height:1000},deviceScaleFactor:1});
  const pageErrors=[];page.on('pageerror',e=>pageErrors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/brand/ui/illustrated-v1/review/index.html');
  await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await page.evaluate(()=>document.fonts.ready);
  const sizes=await page.evaluate(()=>({images:document.images.length,broken:[...document.images].filter(i=>!i.naturalWidth).length,circleWidths:[...new Set([...document.querySelectorAll('.circle')].map(i=>i.getBoundingClientRect().width))],iconWidths:[...new Set([...document.querySelectorAll('.circle img')].map(i=>i.getBoundingClientRect().width))],circleCounts:[...document.querySelectorAll('.scene')].map(i=>i.querySelectorAll('.circle').length),sceneSizes:[...document.querySelectorAll('.scene')].map(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),blindImages:document.querySelectorAll('.blind img').length,answersHidden:!document.querySelector('details').open}));
  assert.equal(sizes.broken,0);assert.deepEqual(sizes.circleWidths,[40]);assert.deepEqual(sizes.iconWidths.sort(),[20,24]);assert(sizes.circleCounts.every(n=>n===5));assert.equal(sizes.blindImages,10);assert(sizes.answersHidden);assert.deepEqual(pageErrors,[]);
  for(let i=0;i<4;i++)await page.locator('.scene').nth(i).screenshot({path:path.join(__dirname,'review','browser-scene-A-'+i+'-1x.png')});
  await page.locator('select[data-choice]').evaluateAll(nodes=>{nodes.forEach(s=>s.value='B');update()});
  await page.evaluate(()=>Promise.all([...document.querySelectorAll('.scene img')].map(i=>i.decode())));
  assert(await page.locator('.scene img').evaluateAll(nodes=>nodes.every(i=>i.src.includes('-B-v1/'))));
  await page.locator('select[data-choice="Scan"]').selectOption('A');
  assert(await page.locator('.scene img[data-id="Scan"]').evaluateAll(nodes=>nodes.every(i=>i.src.includes('-A-v1/'))));
  fs.writeFileSync(path.join(__dirname,'review','browser-layout-check.json'),JSON.stringify({date:'2026-11-05',status:'passed',...sizes,switchAllB:'passed',switchIndividualA:'passed',pageErrors},null,2)+'\n');
  console.log(JSON.stringify({status:'passed',...sizes}));
 }finally{if(browser)await browser.close();await new Promise(ok=>server.close(ok))}
})().catch(e=>{console.error(e);process.exit(1)});
