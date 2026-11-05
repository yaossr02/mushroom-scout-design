const {chromium}=require('playwright');
const http=require('http'),fs=require('fs'),path=require('path'),assert=require('assert');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const server=http.createServer((req,res)=>{
  try{const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
   if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
   const type=file.endsWith('.png')?'image/png':file.endsWith('.svg')?'image/svg+xml':file.endsWith('.json')?'application/json':'text/html; charset=utf-8';
   res.setHeader('Content-Type',type);res.end(fs.readFileSync(file));
  }catch{res.writeHead(404);res.end();}
 });
 await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
 let browser;
 try{
  browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});
  const page=await browser.newPage({viewport:{width:1500,height:1200},deviceScaleFactor:1});
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url());});
  const base='http://127.0.0.1:'+server.address().port;
  const reports=[];
  for(const style of ['A','B','C']){
   const dir='floatbar-'+style+'-v1';await page.goto(base+'/'+dir+'/index.html',{waitUntil:'networkidle'});
   await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('article').count(),16);
   assert.equal(await page.locator('.native-scene .cell').count(),16);
   assert.equal(await page.locator('.samples img').count(),48);
   const measures=await page.locator('.native-scene .circle').first().evaluate(el=>({circle:el.getBoundingClientRect().width,icon:el.querySelector('img').getBoundingClientRect().width}));
   assert.equal(measures.circle,40);assert.equal(measures.icon,20);
   const size24=await page.locator('.circle.s24 img').first().evaluate(el=>el.getBoundingClientRect().width);assert.equal(size24,24);
   await page.screenshot({path:path.join(root,dir,'review.png'),fullPage:true});
   const hires=await browser.newPage({viewport:{width:1500,height:1200},deviceScaleFactor:4});
   await hires.goto(base+'/'+dir+'/index.html',{waitUntil:'networkidle'});await hires.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
   await hires.locator('.native-scene').evaluate(el=>el.style.width='560px');
   await hires.locator('.native-scene').screenshot({path:path.join(root,dir,'20dp-xxxhdpi-scene.png')});
   await hires.locator('.scene').nth(1).evaluate(el=>el.style.width='560px');
   await hires.locator('.scene').nth(1).screenshot({path:path.join(root,dir,'24dp-xxxhdpi-scene.png')});
   await hires.close();
   reports.push({style,cards:16,main_and_control_cells:16,thumbnail_samples:48,layout_circle_css_px:40,icon_css_px:[20,24],xxxhdpi_capture_dpr:4,images_decoded:true});
  }
  await page.goto(base+'/floatbar-review-v1/index.html',{waitUntil:'networkidle'});await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('.stylepanel').count(),3);assert.equal(await page.locator('.stylepanel .scene').count(),6);
  await page.screenshot({path:path.join(root,'floatbar-review-v1/overview.png'),fullPage:true});
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(__dirname,'browser-check.json'),JSON.stringify({status:'candidate',browser:await browser.version(),reviews:reports,overview_directions:3,http_or_script_errors:errors,game_background:'simulated; real screenshots1/2 not received',app_runtime_tested:false},null,2)+'\n');
  console.log('3 full reviews, 48 candidate cards, 144 thumbnail samples and DPR4 scene captures passed; no HTTP/script errors.');
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);process.exit(1);});
