"""Mechanical PNG normalization, provenance, and direct-original review layouts only."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json,hashlib,random,html
R=Path(__file__).resolve().parent
REPO=R.parents[2]
if (R/'approved/batch1/manifest.json').exists():
 raise SystemExit('Batch1 is frozen after approval. Create a new candidate version; do not regenerate this historical review/catalog.')
PLAN=json.loads((R/'generation-plan.json').read_text())
OUT=R/'review';OUT.mkdir(exist_ok=True)
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def text(d,xy,s,size=20,color='#2E3A2F'):d.text(xy,s,font=ImageFont.truetype(F,size),fill=color)
def load(p):return Image.open(p).convert('RGBA')
def paste(canvas,im,xy,size):canvas.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),xy)
def stats(p):
 im=Image.open(p);a=im.convert('RGBA').getchannel('A')
 return {'path':str(p.relative_to(R)),'dimensions_px':list(im.size),'mode':im.mode,'alpha_extrema':list(a.getextrema()),'bbox_alpha_nonzero':list(a.getbbox() or []),'bbox_alpha128':list(a.point(lambda n:255 if n>=128 else 0).getbbox() or []),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
assets=[]
for c in PLAN['concepts']:
 folder=R/c['directory'];raw=folder/'generated-original.png'
 if not raw.exists():raise RuntimeError('Missing generated asset: '+str(raw))
 im=load(raw);ops=[]
 if im.size!=(1254,1254):
  im=ImageOps.contain(im,(1254,1254),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(1254,1254));canvas.alpha_composite(im,((1254-im.width)//2,(1254-im.height)//2));im=canvas;ops=['Uniform LANCZOS resize and centered transparent canvas to 1254x1254; no shape editing.']
 # Uniform scale/translation is canvas preparation only: fit opaque body within ~8% margins.
 body=im.getchannel('A').point(lambda n:255 if n>=128 else 0).getbbox()
 if body:
  scale=min(1.0,1054/max(body[2]-body[0],body[3]-body[1]))
  newsize=(round(im.width*scale),round(im.height*scale))
  dx=round(627-(body[0]+body[2])*scale/2);dy=round(627-(body[1]+body[3])*scale/2)
  if scale<1 or dx or dy:
   scaled=im.resize(newsize,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(1254,1254));canvas.alpha_composite(scaled,(dx,dy));im=canvas
   ops.append({'operation':'Uniform scale and translate complete RGBA image to center alpha128 body with about 8% safe margin; no shape edits','scale':scale,'offset_px':[dx,dy]})
 im.save(folder/'icon.png')
 meta={**c,'status':'candidate','date':'2026-11-05','timezone':'Asia/Taipei','tool':'image_gen','reference':PLAN['references'],'original':stats(raw),'final':stats(folder/'icon.png'),'mechanical_operations':ops,'alpha_policy':'Original alpha retained; no shape edits, morphological filters, recoloring, thickening or outline added.','limitations':['Generated soft shading and edge alpha require visual review.','20dp/24dp browser mockups are not Android device tests.']}
 (folder/'METADATA.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 assets.append({**meta,'image':im})
refs=[('核准 D 金盆',load(R/'references/approved-gold.png'),'references/approved-gold.png'),('核准 v0.5 紅菇',load(R/'references/red-mushroom.png'),'references/red-mushroom.png')]
reference_meta=[]
for source,local in zip(PLAN['references'],['references/approved-gold.png','references/red-mushroom.png']):reference_meta.append({'source':source,**stats(R/local)})
catalog={'date':'2026-11-05','version':'illustrated-v1','status':'candidate','scope':'Map right-side five functions; each concept pending individual approval','references':reference_meta,'assets':[{k:v for k,v in a.items() if k!='image'} for a in assets]}
catalog['historical_attempts']=[]
for old in R.glob('candidates/*/attempts/*/generated-original.png'):
 attempt={'status':'candidate','include_in_review':False,'date':'2026-11-05','original':stats(old),'reason':'Earlier shape attempt retained for provenance; current candidate uses regenerated wooden box.'}
 (old.parent/'METADATA.json').write_text(json.dumps(attempt,ensure_ascii=False,indent=2)+'\n')
 catalog['historical_attempts'].append(attempt)
(R/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
by={(a['id'],a['concept']):a for a in assets};ids=list(dict.fromkeys(a['id'] for a in assets))
grass=load(R/'references/simulated-grass.png')
# 360x320dp viewport at xxxhdpi. Five 40dp circles at the right, 12dp gaps.
def scene(concept,dp,bg,overrides=None):
 im=Image.new('RGBA',(1440,1280),'#EFEBE3') if bg=='map' else ImageOps.fit(grass,(1440,1280),method=Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(im)
 for i,id in enumerate(ids):
  a=by[id,(overrides or {}).get(id,concept)];x=1216;y=96+i*208
  d.ellipse((x,y,x+159,y+159),fill='#FFFCF6');paste(im,a['image'],(x+(160-dp*4)//2,y+(160-dp*4)//2),dp*4)
 return im
for concept in ['A','B']:
 for dp in [20,24]:
  for bg in ['map','grass']:scene(concept,dp,bg).save(OUT/f'right-column-{concept}-{bg}-{dp}dp-xxxhdpi.png')
# Overview: all ten candidates plus approved gold/red at the same 170px canvas size.
board=Image.new('RGBA',(1500,2220),'#FFFCF6');d=ImageDraw.Draw(board)
text(d,(35,20),'插圖風功能圖示 · batch 1 · 10 張候選',32)
text(d,(35,70),'2026-11-05 · 全部 candidate，未核准 · PNG 直接排版；未改 App',19)
allcells=[(a['id']+' '+a['concept']+' · '+a['title'],a['image']) for a in assets]+[(n,im) for n,im,p in refs]
for i,(name,im) in enumerate(allcells):
 x=25+(i%6)*246;y=118+(i//6)*250
 paste(board,im,(x+34,y),170);text(d,(x+4,y+180),name,16)
text(d,(35,625),'32 / 48 / 64 px 原圖縮圖（每組從左至右）',23)
for i,a in enumerate(assets):
 x=35+(i%5)*292;y=675+(i//5)*140
 text(d,(x,y),a['id']+' '+a['concept'],17)
 for j,s in enumerate([32,48,64]):paste(board,a['image'],(x+15+j*82,y+40+(64-s)//2),s)
text(d,(35,970),'地圖右側 5 顆直排 · A 整套 / B 整套 · 每顆40dp（以下縮小示意，實際尺寸見HTML）',23)
for k,(bg,dp) in enumerate([('map',20),('map',24),('grass',20),('grass',24)]):
 for ci,concept in enumerate(['A','B']):
  col=k%2;row=k//2;x=35+col*730+ci*350;y=1040+row*550
  text(d,(x,y),f'{concept} · {"奶油地圖" if bg=="map" else "模擬草地"} · {dp}dp',18)
  im=Image.open(OUT/f'right-column-{concept}-{bg}-{dp}dp-xxxhdpi.png').convert('RGBA').resize((324,288),Image.Resampling.LANCZOS)
  board.alpha_composite(im,(x,y+38))
text(d,(35,2110),'原圖與參考圖皆同大小畫布；草地是既有 image_gen 模擬背景，非實機截圖。',19)
text(d,(35,2148),'1254×1254 RGBA · 每張完整prompt、原始輸出、alpha、bbox與SHA-256已保存。',19)
board.convert('RGB').save(OUT/'overview.png')
board.crop((0,0,1500,610)).convert('RGB').save(OUT/'concepts.png')
# One per-function board: A/B and both references, thumbnails, native xxxhdpi samples, backgrounds.
for id in ids:
 aa,bb=by[id,'A'],by[id,'B'];b=Image.new('RGBA',(1300,1390),'#FFFCF6');dd=ImageDraw.Draw(b)
 text(dd,(30,18),f'{id} · {aa["label"]} · A / B 候選',30)
 text(dd,(30,65),'四張圖同為230px畫布 · 參考圖已核准，新圖不繼承核准',18)
 for i,(name,im) in enumerate([(f'A {aa["title"]}',aa['image']),(f'B {bb["title"]}',bb['image'])]+[(n,im) for n,im,p in refs]):
  x=25+i*320;paste(b,im,(x+25,108),230);text(dd,(x+20,350),name,19)
 for ci,a in enumerate([aa,bb]):
  x=30+ci*640;text(dd,(x,415),a['concept']+' · 32 / 48 / 64 px',20)
  for j,s in enumerate([32,48,64]):paste(b,a['image'],(x+25+j*100,465+(64-s)//2),s)
  text(dd,(x,550),'80 / 96 px = 20 / 24 dp @4x',18)
  for j,s in enumerate([80,96]):paste(b,a['image'],(x+25+j*150,595+(96-s)//2),s)
 text(dd,(30,725),'40dp 圓鈕：以下放大2倍；地圖右側完整5顆直排見HTML／整套圖',20)
 for bi,bg in enumerate(['map','grass']):
  for ci,a in enumerate([aa,bb]):
   x=30+ci*640;y=780+bi*215
   strip=Image.new('RGBA',(600,180),'#EFEBE3') if bg=='map' else ImageOps.fit(grass,(600,180));sd=ImageDraw.Draw(strip)
   for j,dp in enumerate([20,24]):
    xx=60+j*300;sd.ellipse((xx,20,xx+79,99),fill='#FFFCF6');paste(strip,a['image'],(xx+(80-dp*2)//2,20+(80-dp*2)//2),dp*2);text(sd,(xx,115),f'{dp}dp',19)
   b.alpha_composite(strip,(x,y));text(dd,(x,y+183),f'{a["concept"]} · {"奶油地圖" if bg=="map" else "模擬草地"}',17)
 text(dd,(30,1250),'無文字辨識測試：見 blind-test.png；答案獨立放在 blind-answers.md。',19)
 text(dd,(30,1290),'透明邊與實機可讀性尚待檢閱；本圖只表示candidate，未核准。',18)
 b.convert('RGB').save(OUT/f'{id}.png')
# Truly unlabelled image board. Answers are a separate file; row/column identify positions.
order=assets.copy();random.Random(1105).shuffle(order)
blind=Image.new('RGBA',(1200,540),'#EFEBE3')
for i,a in enumerate(order):paste(blind,a['image'],(20+(i%5)*240,20+(i//5)*270),200)
blind.convert('RGB').save(OUT/'blind-test.png')
answers=['# 無文字辨識測試答案','先看 blind-test.png；從左至右、由上至下，按列／欄對照。','']
for i,a in enumerate(order):answers.append(f'- 第{i//5+1}列第{i%5+1}欄：{a["id"]} {a["concept"]} — {a["label"]}／{a["title"]}')
(OUT/'blind-answers.md').write_text('\n'.join(answers)+'\n')
# Portable HTML refers directly to final PNGs; interactive A/B switches change preview only.
css='''*{box-sizing:border-box}body{margin:24px;background:#FFFCF6;color:#2E3A2F;font:16px system-ui,sans-serif}h1{font-size:28px}h2{margin-top:32px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}.card{background:#EFEBE3;padding:16px;border-radius:14px}.hero{width:180px;height:180px;object-fit:contain}.samples{display:flex;align-items:center;gap:16px;margin:16px 0}.samples span{display:inline-flex;flex-direction:column;gap:8px;align-items:center}.refs{display:flex;gap:24px;align-items:center}.scenes{display:flex;flex-wrap:wrap;gap:24px}.scene{width:360px;height:320px;position:relative;background:#EFEBE3}.scene.grass{background-image:url(../references/simulated-grass.png);background-size:cover}.buttons{position:absolute;right:16px;top:24px;display:flex;flex-direction:column;gap:12px}.circle{display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:#FFFCF6}.scene img{object-fit:contain}.blind{display:grid;grid-template-columns:repeat(5,120px);gap:15px}.blind img{width:110px;height:110px}.dark{background:#26392D}.checker{background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 0/16px 16px}select,button{padding:8px;margin:6px}summary{cursor:pointer}'''
parts=['<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>插圖風功能圖示 batch1 · candidate</title><style>'+css+'</style><h1>插圖風功能圖示 · batch1 · candidate</h1><p>2026-11-05；10張均未核准。A/B切換只改預覽，不記錄核准。草地為既有image_gen模擬背景，未做Android實機驗證。</p><p><a href="../ILLUSTRATED-STYLE.md">風格規範</a> · <a href="overview.png">總覽PNG</a> · <a href="../catalog.json">規格／hash</a></p><h2>無文字辨識測試</h2><p>先看下方圖示，不看答案，試著分辨5種功能；答案按列／欄對照。</p><div class="blind">']
for a in order:parts.append(f'<img src="../{a["final"]["path"]}" alt="">')
parts.append('</div><details><summary>展開答案（先不看）</summary><ol>'+''.join(f'<li>第{i//5+1}列第{i%5+1}欄：{a["label"]}／{a["concept"]} {a["title"]}</li>' for i,a in enumerate(order))+'</ol></details><h2>核准參考（與候選同為180px畫布）</h2><div class="refs">')
for name,im,path in refs:parts.append(f'<figure><img class="hero" src="../{path}" alt="{name}"><figcaption>{name} · approved</figcaption></figure>')
parts.append('</div><h2>選擇概念做地圖預覽</h2><p>從上到下：Auto、Tasks、Records、Favorites、Scan。這裡不附按鈕文字，方便觀察辨識；對照答案在概念卡。</p>')
for id in ids:parts.append(f'<label>{id}<select data-choice="{id}"><option>A</option><option>B</option></select></label>')
parts.append('<button onclick="document.querySelectorAll(\'select[data-choice]\').forEach(s=>s.value=\'A\');update()">全A</button><button onclick="document.querySelectorAll(\'select[data-choice]\').forEach(s=>s.value=\'B\');update()">全B</button><div class="scenes">')
for bg in ['map','grass']:
 for dp in [20,24]:
  parts.append(f'<section><h3>{bg} · 40dp圓／{dp}dp圖示（1 CSS px = 1dp）</h3><div class="scene {bg}" data-size="{dp}"><div class="buttons">'+''.join(f'<div class="circle"><img data-id="{id}" src="../{by[id,"A"]["final"]["path"]}" width="{dp}" height="{dp}" alt=""></div>' for id in ids)+'</div></div></section>')
parts.append('</div><h2>A/B 全部候選（各自未核准）</h2><div class="grid">')
for a in assets:
 p='../'+a['final']['path'];folder='../'+a['directory'];parts.append(f'<article class="card"><h3>{a["id"]} {a["concept"]} · {a["title"]}</h3><img class="hero" src="{p}" alt="{a["label"]}"><p>{a["label"]} · candidate</p><div class="samples">'+''.join(f'<span><img src="{p}" width="{s}" height="{s}" alt="">{s}px</span>' for s in [32,48,64])+'</div><div class="samples">'+''.join(f'<span><img src="{p}" width="{s}" height="{s}" alt="">{s}px / {s//4}dp @4x</span>' for s in [80,96])+f'</div><div class="samples"><span class="dark"><img src="{p}" width="96" height="96" alt=""></span><span class="checker"><img src="{p}" width="96" height="96" alt=""></span></div><a href="{folder}/PROMPT.json">完整prompt</a> · <a href="{folder}/METADATA.json">metadata</a> · <a href="{a["id"]}.png">功能比較板</a></article>')
parts.append('</div><script>function update(){const c=Object.fromEntries([...document.querySelectorAll("select[data-choice]")].map(s=>[s.dataset.choice,s.value]));document.querySelectorAll(".scene img[data-id]").forEach(i=>i.src="../candidates/"+i.dataset.id+"-"+c[i.dataset.id]+"-v1/icon.png")}document.querySelectorAll("select[data-choice]").forEach(s=>s.addEventListener("change",update));</script></html>')
(OUT/'index.html').write_text('\n'.join(parts))
print('Built 10 candidates, catalog, overview, five function boards, blind test, 8 xxxhdpi scenes, and interactive HTML.')
