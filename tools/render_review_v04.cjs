// Requires Playwright and Chromium; run against a locally served design repository.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox', '--disable-dev-shm-usage']});
  try {
    const page = await browser.newPage({viewport: {width: 1536, height: 1100}, deviceScaleFactor: 1});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => {if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`)});
    const base = process.env.REVIEW_BASE_URL || 'http://127.0.0.1:8765';
    await page.goto(base + '/brand/reviews/v0.4/review.html', {waitUntil: 'networkidle'});
    await page.evaluate(() => Promise.all(Array.from(document.images).map(i => i.decode())));
    assert.strictEqual(await page.locator('#character-select option').count(), 15);
    const choices = await page.locator('#character-select option').evaluateAll(os => os.map(o => o.value));
    for (const id of choices) {
      await page.selectOption('#character-select', id);
      await page.evaluate(() => Promise.all(Array.from(document.querySelectorAll('.marker-picture')).map(i => i.decode())));
      assert(await page.locator('.marker-picture').first().getAttribute('src').then(s => s.endsWith(id + '.png')));
    }
    await page.selectOption('#character-select', 'red-mushroom');
    await page.evaluate(() => Promise.all(Array.from(document.querySelectorAll('.marker-picture')).map(i => i.decode())));
    await page.click('#background-toggle');
    assert(await page.locator('#content-review').evaluate(el => el.classList.contains('dark-content')));
    await page.click('#background-toggle');
    await page.click('#map-toggle');
    assert(await page.locator('.marker-area').first().evaluate(el => el.classList.contains('dark')));
    await page.click('#map-toggle');
    await page.click('#guide-toggle');
    assert.strictEqual(await page.locator('.safe-guide').first().evaluate(el => getComputedStyle(el).display), 'block');
    await page.click('#guide-toggle');
    assert.notStrictEqual(await page.locator('.theme-mask').first().evaluate(el => getComputedStyle(el).maskImage), 'none');
    const out = path.resolve(__dirname, '../brand/reviews/v0.4');
    for (const [id, filename] of [['content-review','01-mushrooms.png'],['marker-review','02-marker-system.png'],['brand-review','03-brand-platforms.png']]) {
      await page.locator('#' + id).screenshot({path: path.join(out, filename)});
    }
    // Second visual check of masks/labels on dark backgrounds, without changing the default review.
    await page.click('#background-toggle');
    await page.click('#map-toggle');
    await page.click('#guide-toggle');
    await page.locator('#brand-review').screenshot({path: '/tmp/design-v04-brand-guides.png'});
    await page.locator('#marker-review').screenshot({path: '/tmp/design-v04-marker-dark.png'});
    assert.deepStrictEqual(errors, []);
    fs.writeFileSync(path.join(out, 'browser-check.json'), JSON.stringify({
      review: 'v0.4', browser: await browser.version(), css_viewport: [1536,1100], dpr: 1,
      marker_choices_exercised: choices.length, background_toggles: 'passed', safety_guide_toggle: 'passed',
      source_images_decoded: 'passed', css_masks: 'configured and visually reviewed via screenshots',
      console_or_http_errors: errors, device_runtime_tested: false,
      screenshots: ['01-mushrooms.png','02-marker-system.png','03-brand-platforms.png']
    }, null, 2) + '\n');
    console.log('15 character choices, toggles, image decoding and page checks passed; three actual review screenshots saved.');
  } finally {
    await browser.close();
  }
})().catch(e => {console.error(e); process.exit(1)});
