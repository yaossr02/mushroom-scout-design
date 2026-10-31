// Render original SVGs to transparent PNGs and review boards. No source image editing.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert');

(async () => {
  const root = path.resolve(__dirname, '../brand/ui/v0.6');
  const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json')));
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox','--disable-dev-shm-usage']});
  const errors = [];
  try {
    const base = process.env.REVIEW_BASE_URL || 'http://127.0.0.1:8765';
    const page = await browser.newPage({viewport:{width:1536,height:1100},deviceScaleFactor:1});
    page.on('pageerror', e=>errors.push(e.message));
    page.on('response', r=>{if(r.status()>=400) errors.push(`${r.status()} ${r.url()}`)});
    await page.goto(base + '/brand/ui/v0.6/review/index.html', {waitUntil:'networkidle'});
    assert.strictEqual(await page.locator('article').count(),56);
    assert.strictEqual(await page.locator('article svg').count(),280);
    await page.fill('#search','相簿');
    assert.strictEqual(await page.locator('article:visible').count(),1);
    assert((await page.locator('article:visible code').textContent())==='Photo');
    await page.fill('#search','LightSpeed');
    assert.strictEqual(await page.locator('article:visible').count(),1);
    await page.fill('#search','');
    await page.evaluate(()=>document.fonts.ready);
    const names = ['01-map-main.png','02-actions-navigation.png','03-tools-status.png'];
    for(let i=1;i<=3;i++) {
      await page.evaluate(id=>{
        document.querySelector('header').style.display='none';
        document.querySelector('footer').style.display='none';
        document.querySelectorAll('section').forEach(s=>s.style.display=s.id===id?'block':'none');
        window.scrollTo(0,0);
      }, 'board-'+i);
      await page.locator('#board-'+i).screenshot({path:path.join(root,'review',names[i-1]),animations:'disabled'});
    }
    await page.evaluate(()=>{
      document.querySelector('header').style.display='';
      document.querySelector('footer').style.display='';
      document.querySelectorAll('section').forEach(s=>s.style.display='');
    });
    await page.click('#theme');
    assert(await page.locator('body').evaluate(e=>e.classList.contains('dark')));
    await page.locator('#board-1').screenshot({path:path.join(root,'review','04-dark-example.png')});
    await page.click('#theme');
    await page.setViewportSize({width:390,height:844});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.setViewportSize({width:1536,height:1100});
    const glyphPage = await browser.newPage({viewport:{width:64,height:64},deviceScaleFactor:1});
    await glyphPage.goto(base+'/brand/ui/v0.6/review/glyph-render.html',{waitUntil:'networkidle'});
    for(const g of catalog.glyphs){
      const svg=fs.readFileSync(path.join(root,g.svg),'utf8');
      g.png = {}; g.png_sha256 = {};
      for(const size of [24,48]){
        await glyphPage.evaluate(({svg,size})=>{const e=document.querySelector('#glyph');e.style.width=size+'px';e.style.height=size+'px';e.innerHTML=svg}, {svg,size});
        const relative=`png/${size}/${g.id}.png`;
        const file=path.join(root,relative);
        await glyphPage.locator('#glyph').screenshot({path:file,omitBackground:true});
        g.png[size]=relative;
        g.png_sha256[size]=crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
      }
    }
    assert.deepStrictEqual(errors,[]);
    fs.writeFileSync(path.join(root,'catalog.json'),JSON.stringify(catalog,null,2)+'\n');
    fs.writeFileSync(path.join(root,'review/browser-check.json'),JSON.stringify({
      version:'v0.6',browser:await browser.version(),viewport:[1536,1100],dpr:1,
      semantic_cards:56,inline_svg_previews:280,unique_glyphs:catalog.glyphs.length,
      png_exports:catalog.glyphs.length*2,export_sizes_px:[24,48],
      chinese_and_id_search:'passed',theme_toggle:'passed',mobile_overflow:'passed',
      errors,app_runtime_tested:false
    },null,2)+'\n');
    console.log(`${catalog.glyphs.length} glyphs -> ${catalog.glyphs.length*2} transparent PNGs; 56 semantics and review interactions verified.`);
  } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
