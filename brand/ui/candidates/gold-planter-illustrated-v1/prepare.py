from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, hashlib, shutil
import numpy as np
R=Path(__file__).resolve().parent
repo=R.parents[3]
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def txt(d,xy,s,n=20,fill='#2E3A2F'): d.text(xy,s,font=ImageFont.truetype(font,n),fill=fill)
def stats(p):
 im=Image.open(p); a=im.convert('RGBA').getchannel('A'); return dict(path=str(p.relative_to(R)),dimensions_px=list(im.size),mode=im.mode,alpha_extrema=list(a.getextrema()),bbox_alpha_nonzero=list(a.getbbox() or []),bbox_alpha128=list(a.point(lambda x:255 if x>=128 else 0).getbbox() or []),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
refs={'v6':'brand/ui/v0.7-botanical/candidates/gold-planter-swipe-down-v6/icon.png','red-mushroom':'brand/approved/v0.5/red-mushroom.png','fire-mushroom':'brand/approved/v0.5/fire-mushroom.png','C-v2':'brand/ui/v0.7-botanical/approved/floatbar-C-v2/GoldBasin.png','grass':'brand/ui/v0.7-botanical/approved/floatbar-C-v2/review-assets/simulated-game-background.png'}
(R/'references').mkdir(exist_ok=True)
for name,p in refs.items(): shutil.copyfile(repo/p,R/'references'/f'{name}.png')
variants=sorted(p.parent for p in R.glob('*/PROMPT.json'))
manifest={'date':'2026-11-05','status':'candidate','scope':'illustrated gold planter exploration; no App integration or approval','references':[],'variants':[]}
for name,p in refs.items(): manifest['references'].append({'source':p,**stats(R/'references'/f'{name}.png')})
for v in variants:
 src=v/'generated-original.png'; im=Image.open(src).convert('RGBA')
 # Mechanical canvas resize only. Retain all shading and every alpha value; no morphological changes.
 operations=[]
 if im.size!=(1254,1254):
  im=ImageOps.contain(im,(1254,1254),Image.Resampling.LANCZOS); canvas=Image.new('RGBA',(1254,1254)); canvas.alpha_composite(im,((1254-im.width)//2,(1254-im.height)//2)); im=canvas; operations.append('uniform LANCZOS resize and transparent centered canvas to 1254x1254')
 im.save(v/'icon.png')
 m={'id':v.name,'status':'candidate','original':stats(src),'final':stats(v/'icon.png'),'mechanical_operations':operations,'limitations':['Soft shaded illustration; visual selection pending.','Model alpha edges retained, including faint edge pixels. No shape correction or outline added.']}
 (v/'METADATA.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n'); manifest['variants'].append(m)
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
items=[(v.name[0],Image.open(v/'icon.png').convert('RGBA'),v.name+'/icon.png') for v in variants]
red=Image.open(R/'references/red-mushroom.png').convert('RGBA')
allitems=items+[(n,Image.open(R/'references'/f'{n}.png').convert('RGBA'),'references/'+n+'.png') for n in ['red-mushroom','v6','C-v2']]
W=1280; board=Image.new('RGBA',(W,1950),'#FFFCF6'); d=ImageDraw.Draw(board)
txt(d,(32,18),'拉金盆 · 蘑菇插圖畫法 v1 / 4 個候選',30)
txt(d,(32,65),'2026-11-05 · candidate，尚未核准 · 原圖並排；下方為尺寸模擬，非實機測試',17)
labels=['A 單葉・圓腹','B 雙葉・圓腹','C 單葉・扁圓腹','D 雙葉・粗箭頭']
for i,(id,im,path) in enumerate(items):
 x=20+i*315
 txt(d,(x+5,108),labels[i],21)
 board.alpha_composite(im.resize((150,150),Image.Resampling.LANCZOS),(x,155)); board.alpha_composite(red.resize((150,150),Image.Resampling.LANCZOS),(x+155,155))
 txt(d,(x+20,310),id+' 候選',16); txt(d,(x+175,310),'v0.5 原紅菇',16)
 for j,size in enumerate([32,48,64]):
  sx=x+22+j*91; board.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(sx,360+(64-size)//2)); txt(d,(sx,432),f'{size}px',15)
 txt(d,(x+6,475),'80 / 96 px（20 / 24 dp @4x）',15)
 board.alpha_composite(im.resize((80,80),Image.Resampling.LANCZOS),(x+32,510)); board.alpha_composite(im.resize((96,96),Image.Resampling.LANCZOS),(x+155,502))
# DPR4 scene exports: each circle 160px (=40dp), icons80/96; overview embeds at 2x for visibility.
grass=Image.open(R/'references/grass.png').convert('RGBA')
for bi,bg in enumerate(['map','grass']):
 for si,size in enumerate([80,96]):
  scene=Image.new('RGBA',(1400,248),'#EFEBE3') if bg=='map' else ImageOps.fit(grass,(1400,248))
  sd=ImageDraw.Draw(scene)
  for i,(id,im,path) in enumerate(allitems):
   cx=i*200+100; sd.ellipse((cx-80,12,cx+79,171),fill='#FFFCF6'); scene.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(cx-size//2,92-size//2)); sd.rounded_rectangle((cx-83,185,cx+83,237),radius=23,fill='#2E3A2F'); txt(sd,(cx-65,190),id,20,fill='#FFFCF6')
  scene.save(R/f'{bg}-{size//4}dp-xxxhdpi.png')
  y=640+bi*410+si*190
  txt(d,(32,y),f'{"奶油地圖 #EFEBE3" if bg=="map" else "高飽和草地（模擬背景）"} · 40 dp 圓 / {size//4} dp 圖示 · 此圖板放大 2 倍',18)
  board.alpha_composite(scene.resize((700,124),Image.Resampling.LANCZOS),(35,y+30))
txt(d,(32,1500),'舊版對照（同畫布尺寸）',23)
for i,(id,im,path) in enumerate(allitems[4:]):
 board.alpha_composite(im.resize((190,190),Image.Resampling.LANCZOS),(45+i*300,1550)); txt(d,(50+i*300,1750),id,19)
txt(d,(32,1870),'透明原圖保留柔和明暗；未限色、未程式加粗或描邊。HTML 提供 1:1 CSS 尺寸與明暗底檢閱。',18)
board.convert('RGB').save(R/'review-board.png')
css='body{font:16px sans-serif;background:#FFFCF6;color:#2E3A2F;margin:24px} img{object-fit:contain} .row{display:flex;gap:20px;align-items:center;margin:16px 0}.card{padding:16px;background:#EFEBE3;border-radius:12px}.scene{padding:20px;display:flex;gap:18px;background:#EFEBE3;margin:10px 0}.grass{background-image:url(references/grass.png);background-size:cover}.cell{text-align:center;width:100px}.circle{display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:#FFFCF6;margin:auto}.pill{display:inline-block;background:#2E3A2F;color:#FFFCF6;border-radius:12px;padding:3px 9px;font-size:11px;margin-top:6px}.dark{background:#25362E}.checker{background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 0/16px 16px}'
html=['<!doctype html><meta charset="utf-8"><title>金盆插圖 v1 · candidate</title><style>'+css+'</style><h1>拉金盆 · illustrated v1 · candidate</h1><p>2026-11-05；未核准，未接 App。草地為既有 image_gen 模擬背景；顯示尺寸不代表實機驗證。每次生成均附 v6、紅菇、火菇三原圖。</p>']
for i,(id,im,path) in enumerate(items):
 html.append(f'<section class="card"><h2>{labels[i]}</h2><div class="row"><img src="{path}" width="220" height="220"><img src="references/red-mushroom.png" width="220" height="220"></div><p>候選與原紅菇：相同 220 px 畫布。</p><div class="row">'+''.join(f'<span><img src="{path}" width="{s}" height="{s}"> {s}px</span>' for s in [32,48,64,80,96])+'</div>'+''.join(f'<div class="row {cl}"><img src="{path}" width="96" height="96"></div>' for cl in ['dark','checker'])+f'<a href="{id if False else variants[i].name}/PROMPT.json">完整提示詞</a> · <a href="{variants[i].name}/METADATA.json">實測 metadata</a></section>')
for bg in ['map','grass']:
 for dp in [20,24]:
  html.append(f'<h2>{bg} · 40 dp 圓 / {dp} dp 圖示（1 CSS px = 1 dp）</h2><div class="scene {bg}">'+''.join(f'<div class="cell"><div class="circle"><img src="{p}" width="{dp}" height="{dp}"></div><div class="pill">{id}</div></div>' for id,im,p in allitems)+'</div>')
html.append('<h2>既有原圖對照</h2><div class="row">'+''.join(f'<span><img src="{p}" width="180" height="180">{id}</span>' for id,im,p in allitems[4:])+'</div><p><a href="review-board.png">總覽 PNG</a> · <a href="manifest.json">尺寸、alpha、bbox、SHA-256</a></p>')
(R/'index.html').write_text('\n'.join(html))
print(json.dumps([(m['id'],m['final']['dimensions_px'],m['final']['bbox_alpha128']) for m in manifest['variants']]))
