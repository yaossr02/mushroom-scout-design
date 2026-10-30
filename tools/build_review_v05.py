"""Build the joint review from original images and candidate system tokens. No raster editing."""
import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'brand/reviews/v0.5/review.html'
catalog = json.loads((ROOT / 'brand/catalog.json').read_text())
system = json.loads((ROOT / 'brand/systems/v0.5/marker-system.json').read_text())
platform = json.loads((ROOT / 'brand/systems/v0.5/platform-plan.json').read_text())
assets = {a['id']: a for a in catalog['assets'] if a['status'] != 'rejected' and a.get('active_reference', True)}
new_ids = ['red-mushroom','yellow-mushroom','blue-mushroom','purple-mushroom','white-mushroom','gray-mushroom','pink-mushroom','ice-blue-mushroom','fire-mushroom','water-mushroom','electric-mushroom','poison-mushroom','crystal-mushroom','event-mushroom','unknown-mushroom']


def url(path):
    return os.path.relpath(ROOT / path, OUT.parent)


def picture(ident, size=160):
    a = assets[ident]
    return f'<img src="{url(a["path"])}" width="{size}" height="{size}" alt="{html.escape(a["label"])}">'


def marker(ident='red-mushroom', size='normal', state='normal', caption=''):
    a = assets[ident]
    ax, ay = a['anchor_normalized']
    s = system['states'][state]
    scale = system['size_scales'][size]
    style = f'--scale:{scale};--anchor-x:{ax};--anchor-y:{ay};--picture-opacity:{s["opacity"]};--state-color:{s.get("color", "#55735b")};--ring-style:{s["ring"]}'
    badge = f'<span class="marker-size">{system["badges"][size]}</span>' if size in system['badges'] else ''
    return f'<div class="marker-demo marker-{state}" style="{style}"><div class="marker-ground"><span class="marker-ring"></span><img class="marker-picture" src="{url(a["path"])}" alt="{a["label"]}">{badge}<span class="marker-state">{s["label"]}</span><span class="marker-anchor"></span></div><span class="marker-caption">{caption}</span></div>'


cards = []
for ident in new_ids:
    a = assets[ident]
    cards.append(f'<article><h3>{a["label"]}</h3><div class="art">{picture(ident, 220)}</div><p class="tag">{ident} · candidate</p><div class="small-row">' + ''.join(f'<figure>{picture(ident, s)}<figcaption>{s}px 畫布</figcaption></figure>' for s in [32, 48, 64]) + '</div></article>')

options = ''.join(f'<option value="{i}">{a["label"]}</option>' for i, a in assets.items() if a.get('kind', 'content') == 'content' and 'mushroom' in i)
size_row = ''.join(marker(size=size, caption=f'{system["size_labels"][size]} ×{scale}') for size, scale in system['size_scales'].items())
state_row = ''.join(marker(state=s, caption=s) for s in system['states'])
mix_row = ''.join(marker(size=size, state=state, caption=f'{system["size_labels"][size]}／{system["states"][state]["label"]}') for size, state in [('small', 'selected'), ('large', 'running'), ('giant', 'completed'), ('giant', 'stale')])
foreground = url(assets['android-adaptive-foreground']['path'])
mono = url(assets['android-themed-monochrome']['path'])
notification = url(assets['notification-mushroom']['path'])
ios = url(assets['ios-app-icon']['path'])
mask_tiles = ''.join(f'<figure><div class="adaptive {shape}"><img src="{foreground}" alt="Android 前景"><i class="safe-guide"></i></div><figcaption>{label}</figcaption></figure>' for shape, label in [('circle', '圓形遮罩'), ('rounded', '圓角方形'), ('squircle', 'Squircle 近似')])
theme_tiles = ''.join(f'<figure><div class="adaptive rounded themed" style="background:{bg};--tint:{fg}"><span class="theme-mask"></span></div><figcaption>{label}</figcaption></figure>' for bg, fg, label in [('#dce7cb', '#355640', '淺色主題'), ('#243d35', '#dce7cb', '深色主題')])
notifications = ''.join(f'<figure><span class="notification-mask" style="width:{s}px;height:{s}px"></span><figcaption>{s}px</figcaption></figure>' for s in [16, 24, 32])
css = '''
*{box-sizing:border-box}body{margin:0;background:#fff8ed;color:#513a30;font:16px system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:24px}h1{font-size:32px}h2{font-size:26px;margin:0 0 10px}h3{font-size:18px}p{line-height:1.7}.intro,section{padding:24px;margin-bottom:24px;background:#fffdf8;border:1px solid #e5dacc;border-radius:24px}nav a,button{display:inline-block;padding:8px 15px;margin:4px;border-radius:18px;border:1px solid #cabbac;background:#fff;color:#513a30;text-decoration:none;cursor:pointer}select{padding:10px;border-radius:12px}article{padding:14px;background:#fff;border:1px solid #eadfd2;border-radius:18px}.cards{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}.art{background:#f4ede3;border-radius:12px;display:grid;place-items:center}.art img{width:100%;height:auto}.small-row{display:flex;align-items:end;justify-content:space-around;gap:6px}figure{margin:0;text-align:center}figcaption{font-size:12px;margin-top:8px}.tag{font-size:11px;overflow-wrap:anywhere}.row{display:flex;flex-wrap:wrap;align-items:start;gap:16px}.marker-area{border-radius:18px;background:#e1eacb;margin:12px 0;display:flex;flex-wrap:wrap;justify-content:center}.marker-area.dark{background:#243d35;color:#fff}.note{background:#f2e9dc;padding:12px;border-radius:12px;font-size:13px}.brand-grid{display:grid;grid-template-columns:1fr 1.4fr 1fr;gap:24px}.brand-grid>article{min-width:0}.adaptive{position:relative;width:140px;height:140px;overflow:hidden;background:#55735b}.adaptive.circle{border-radius:50%}.adaptive.rounded{border-radius:24%}.adaptive.squircle{border-radius:36%}.adaptive img{position:absolute;width:150%;height:150%;max-width:none;left:-25%;top:-25%;transform:scale(.8)}.safe-guide{display:none;position:absolute;left:4.167%;top:4.167%;width:91.666%;height:91.666%;border:1px dashed #fff;border-radius:50%;pointer-events:none}.guides .safe-guide{display:block}.theme-mask{display:block;position:absolute;width:150%;height:150%;left:-25%;top:-25%;transform:scale(.65);background:var(--tint);mask-image:var(--theme-url);mask-size:100% 100%;mask-repeat:no-repeat;-webkit-mask-image:var(--theme-url);-webkit-mask-size:100% 100%;-webkit-mask-repeat:no-repeat}.notification-bar{padding:24px;background:#243d35;border-radius:14px;color:white}.notification-mask{display:inline-block;background:white;mask-image:var(--notification-url);mask-size:100% 100%;-webkit-mask-image:var(--notification-url);-webkit-mask-size:100% 100%}.ios-source{width:200px;height:200px}.ios-masked{width:100px;height:100px;border-radius:22%}.dark-content .art{background:#243d35}.dark-content .small-row{background:#243d35;color:white;border-radius:8px}.gallery{display:flex;flex-wrap:wrap;gap:15px}.badge-spec{display:inline-grid;place-items:center;width:28px;height:28px;border:2px solid #fff1db;background:#f4cf70;color:#513a30;border-radius:50%;font-weight:bold}@media(max-width:1000px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}.brand-grid{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){*{animation:none!important}}
'''
css += f'.adaptive img{{transform:scale({platform["android_adaptive"]["foreground_source_scale"]})}}.theme-mask{{transform:scale({platform["android_themed"]["source_scale"]})}}'
plant_html = '<h3>沿用已核准的非擬人化植物</h3><div class="row">' + ''.join('<figure>'+picture(i,96)+'<figcaption>'+assets[i]['label']+'</figcaption></figure>' for i in ['leaf-sprout','flower-bud']) + '</div>'
data = {i: {'src': url(a['path']), 'label': a['label'], 'anchor': a.get('anchor_normalized')} for i, a in assets.items() if 'mushroom' in i and a.get('kind', 'content') == 'content'}
page = f'''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>v0.5 三階段聯合審核</title><link rel="stylesheet" href="../../systems/v0.5/marker-system.css"><style>{css}</style><body style="--theme-url:url('{mono}');--notification-url:url('{notification}')"><main>
<div class="intro"><h1>Cream Gumdrop · v0.5 非擬人化全系列審核</h1><p>全套蘑菇已移除擬人化：沒有眼睛、嘴巴、腮紅、表情或人物身體。15 種蘑菇與品牌圖示皆為新版候選；舊擬人版僅供追溯，植物沿用核准原圖。</p><nav><a href="#content-review">1 蘑菇</a><a href="#marker-review">2 尺寸與狀態</a><a href="#brand-review">3 品牌圖示</a></nav><p>本頁引用原檔，圖板 PNG 是本頁的瀏覽器截圖。mask 需透過本機靜態 HTTP 檢閱；GitHub 不直接執行 HTML。</p></div>
<section id="content-review"><h2>1｜15 種非擬人化蘑菇</h2><p>自然柱狀菇柄、菌褶與低矮葉叢；用顏色、帽型與元素斑紋區分。活動種類改為星形斑紋，不穿戴派對帽。<button id="background-toggle">切換淺／深背景</button></p><div class="cards">{''.join(cards)}</div><p class="note">數字指包含留白的 CSS 畫布；所有尺寸都禁止五官，主要檢查帽型、菇柄與種類辨識。透明邊緣仍屬正式輸出整理項目。</p>{plant_html}</section>
<section id="marker-review"><h2>2｜尺寸與狀態系統</h2><p>直接重用新版自然蘑菇原圖，不重畫主體。切換所有 15 種蘑菇：<select id="character-select">{options}</select> <button id="map-toggle">切換地圖底色</button></p><h3>四級尺寸與大小徽章</h3><div class="marker-area">{size_row}</div><p>倍率：0.85／1／1.15／1.3；大 <span class="badge-spec">大</span> 與巨大 <span class="badge-spec">巨</span>。棕點固定在主體 bbox 底部中心估值，換尺寸不漂移腳底。</p><h3>六種狀態</h3><div class="marker-area">{state_row}</div><p>選取：實線；進行中：虛線＋文字；暫停：琥珀虛線＋文字；完成：雙線；過期：點線＋主體 55% 透明度，文字保持清楚。</p><h3>尺寸 × 狀態疊加</h3><div class="marker-area">{mix_row}</div><p class="note">這是可執行的視覺規格；CSS 與 tokens 已另存，尚非 App 程式碼。狀態同時用線型與文字表達，不能只靠顏色。</p></section>
<section id="brand-review"><h2>3｜App 與通知品牌圖示</h2><div class="brand-grid"><article><h3>iOS／品牌主圖示</h3><img class="ios-source" src="{ios}" alt="iOS 正方形原圖"><p>原檔完整方形、不透明，無內建圓角。</p><img class="ios-masked" src="{ios}" alt="iOS 圓角示意"><p class="tag">1254px 原稿；1024px 正式輸出與 AppIcon 集合留待第 4 階段。</p></article><article><h3>Android adaptive</h3><div class="row">{mask_tiles}</div><button id="guide-toggle">顯示／隱藏安全圈</button><p>前景與純色背景分離；foreground 以 source scale {platform["android_adaptive"]["foreground_source_scale"]} 呈現。108dp 設計格／72dp 可見視窗／66dp 安全圈。Squircle 為 CSS 近似，不等同各廠牌遮罩。</p><h3>單色主題</h3><div class="row">{theme_tiles}</div><p class="tag">黑色 alpha 原稿由系統著色；主題圖 source scale {platform["android_themed"]["source_scale"]}。</p></article><article><h3>通知圖示</h3><div class="notification-bar"><div class="row">{notifications}</div></div><p>簡化蘑菇剪影與兩個斑點孔，沒有五官或掃描框。</p><p class="note">黑色來源只提供 alpha，預覽著色為白色。不是黑底圖。正式密度輸出與 Android 資源尚未打包。</p></article></div><p class="note">平台原稿、背景色 XML、分層與縮放規格均已保存。安全圈數值檢查與瀏覽器預覽不能取代 Android／iOS 實機驗證。</p></section>
<p>審核時可分別回覆 1／2／3 的核准或修改項目。原 App repo 未變更；最新版品牌規範已依使用者明確要求改為非擬人化，候選仍須核准。</p></main>
<script>const characters={json.dumps(data, ensure_ascii=False)};document.querySelector('#character-select').onchange=e=>{{const a=characters[e.target.value];document.querySelectorAll('.marker-demo').forEach(m=>{{m.style.setProperty('--anchor-x',a.anchor[0]);m.style.setProperty('--anchor-y',a.anchor[1]);const i=m.querySelector('img');i.src=a.src;i.alt=a.label}})}};document.querySelector('#background-toggle').onclick=()=>document.querySelector('#content-review').classList.toggle('dark-content');document.querySelector('#map-toggle').onclick=()=>document.querySelectorAll('.marker-area').forEach(x=>x.classList.toggle('dark'));document.querySelector('#guide-toggle').onclick=()=>document.querySelector('#brand-review').classList.toggle('guides');</script></body></html>'''
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)
print(f'Built {OUT.relative_to(ROOT)}: {len(new_ids)} candidates; {len(data)} marker choices; three review sections')
