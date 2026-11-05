"""Prepare generated RGBA canvases and direct-original candidate review layouts.
Only uniform resize/translation and explicitly authorized vertical flip alter images.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib,os,random
R=Path(__file__).resolve().parent;S=R.parents[1];REPO=S.parents[2]
P=json.loads((R/'PLAN.json').read_text());FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONTS={}
def txt(d,xy,t,size=20,color='#2E3A2F'):
 if size not in FONTS:FONTS[size]=ImageFont.truetype(FONT,size)
 d.text(xy,t,font=FONTS[size],fill=color)
def read(p):return Image.open(p).convert('RGBA')
def paste(b,im,xy,size):b.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),xy)
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def stats(p):
 im=Image.open(p);a=im.convert('RGBA').getchannel('A');return dict(path=str(p.relative_to(REPO)),dimensions_px=list(im.size),mode=im.mode,alpha_extrema=list(a.getextrema()),bbox_alpha_nonzero=list(a.getbbox() or []),bbox_alpha128=list(a.point(lambda x:255 if x>=128 else 0).getbbox() or []),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def rel(p):return os.path.relpath(REPO/p,R)
assets=[]
for a in P['assets']:
 folder=S/a['directory'];raw=folder/'generated-original.png'
 if not raw.exists():raise RuntimeError('Missing '+str(raw))
 im=read(raw);bbox=im.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox()
 if not bbox:raise RuntimeError('Empty alpha '+str(raw))
 scale=min(1254/im.width,1254/im.height,1054/max(bbox[2]-bbox[0],bbox[3]-bbox[1]));offset=[round(627-(bbox[0]+bbox[2])*scale/2),round(627-(bbox[1]+bbox[3])*scale/2)]
 canvas=Image.new('RGBA',(1254,1254));canvas.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),tuple(offset));canvas.save(folder/'icon.png')
 meta={k:v for k,v in a.items() if k not in ['prompt','subject']};meta.update(original=stats(raw),final=stats(folder/'icon.png'),mechanical_operations=[dict(operation='uniform resize and translate complete image onto transparent 1254px canvas',scale=scale,offset_px=offset)],alpha_policy='Original alpha retained; no morphology, recoloring, thickening, stroke, added drawing or shape edits.',generation_record=str((folder/'generation.json').relative_to(REPO)))
 write(folder/'METADATA.json',meta);assets.append(meta)
# Expand is an EXACT vertical mirror of each finalized Collapse, never independently regenerated.
for concept in ['A','B']:
 source=S/f'candidates/Collapse-{concept}-v1';folder=S/f'candidates/Expand-{concept}-v1';folder.mkdir(exist_ok=True)
 srcmeta=next(a for a in assets if a['id']=='Collapse' and a['concept']==concept)
 prompt=json.loads((source/'PROMPT.json').read_text());prompt.update(id='Expand',label='展開',directory=f'candidates/Expand-{concept}-v1',tool='image_gen source + Pillow mechanical vertical flip',derivation={'source':'Collapse-'+concept+'-v1','operation':'FLIP_TOP_BOTTOM','authorization':P['flip_authorization']},source_model_prompt=prompt['prompt']);prompt['prompt']='Use the attached-reference image_gen source recorded in source_model_prompt. Mechanically flip the complete finalized Collapse PNG TOP TO BOTTOM, including its alpha channel. Do not redraw, recolor or alter any shape.'
 write(folder/'PROMPT.json',prompt)
 # Raw model bytes are retained unchanged with an explicit source provenance; this is not a second model output.
 (folder/'generated-original.png').write_bytes((source/'generated-original.png').read_bytes())
 im=read(source/'icon.png').transpose(Image.Transpose.FLIP_TOP_BOTTOM);im.save(folder/'icon.png')
 write(folder/'generation.json',dict(date=P['date'],tool='Pillow FLIP_TOP_BOTTOM; image_gen source inherited',source_model_generation=str((source/'generation.json').relative_to(REPO)),raw_original_policy='Byte-identical copy of source Collapse model output; not an independently generated Expand image.',authorization=P['flip_authorization']))
 meta={**srcmeta,'id':'Expand','label':'展開','directory':f'candidates/Expand-{concept}-v1','tool':'image_gen source + authorized mechanical vertical flip','original':stats(folder/'generated-original.png'),'final':stats(folder/'icon.png'),'derived_from':str((source/'icon.png').relative_to(REPO)),'mechanical_operations':[dict(operation='Exact FLIP_TOP_BOTTOM of finalized Collapse RGBA',authorization=P['flip_authorization'])],'generation_record':str((folder/'generation.json').relative_to(REPO))}
 write(folder/'METADATA.json',meta);assets.append(meta)
by={(a['id'],a['concept']):a for a in assets}
gold=dict(id='GoldBasin',label='拉金盆',concept='D',status='approved-reference',final=stats(REPO/P['gold_reference']),reused_without_modification=True)
for batch,name in [('floatbar','catalog.floatbar.json'),('map','catalog.map.json')]:write(R/name,dict(date=P['date'],status='candidate',assets=[a for a in assets if a['batch']==batch],approved_reference=gold if batch=='floatbar' else None))
write(R/'catalog.json',dict(date=P['date'],status='candidate',assets=assets,approved_reference=gold,source_generation_count=42,exact_derived_count=2))
images={(id,c):read(REPO/a['final']['path']) for (id,c),a in by.items()};goldim=read(REPO/P['gold_reference']);grass=read(S/'references/simulated-grass.png')
floatids=P['floatbar_ids'];mapids=P['map_ids']
labels={a['id']:a['label'] for a in assets};labels['GoldBasin']='拉金盆'
def image(id,c):return goldim if id=='GoldBasin' else images[id,c]
def imagepath(id,c):return P['gold_reference'] if id=='GoldBasin' else by[id,c]['final']['path']
# Pair contact sheets. A/B labels are outside image canvas; Gold is the same approved reference in both columns.
def contact(ids,name,title):
 rows=(len(ids)+3)//4;b=Image.new('RGBA',(1600,110+rows*300),'#FFFCF6');d=ImageDraw.Draw(b)
 txt(d,(25,15),title,30);txt(d,(25,62),'2026-11-05 · 新圖全部candidate；金盆D僅為既有核准參考 · 每格左右 A／B',18)
 for i,id in enumerate(ids):
  x=10+(i%4)*400;y=115+(i//4)*300;txt(d,(x+12,y),id+' · '+labels[id],21)
  for j,c in enumerate(['A','B']):paste(b,image(id,c),(x+15+j*190,y+37),170);txt(d,(x+70+j*190,y+218),c if id!='GoldBasin' else 'D沿用',18)
 b.convert('RGB').save(R/name)
contact(floatids,'floatbar-concepts.png','懸浮列 · 15組A/B新候選＋原金盆D')
contact(mapids,'map-concepts.png','地圖其他圓鈕 · 7組A/B新候選')
# Full single-row floatbar: native xxxhdpi; 16 circles40dp, icons24/28dp, gap8dp.
for c in ['A','B']:
 stripfiles=[]
 for dp in [24,28]:
  strip=ImageOps.fit(grass,(3136,336),method=Image.Resampling.LANCZOS);d=ImageDraw.Draw(strip)
  for i,id in enumerate(floatids):
   x=32+i*192;y=32;d.ellipse((x,y,x+159,y+159),fill='#FFFCF6');paste(strip,image(id,c),(x+(160-dp*4)//2,y+(160-dp*4)//2),dp*4)
   d.rounded_rectangle((x-8,216,x+168,296),radius=32,fill='#2E3A2F');txt(d,(x+2,237),id,19,'#FFFCF6')
  name=f'floatbar-{c}-{dp}dp-xxxhdpi.png';strip.convert('RGB').save(R/name);stripfiles.append(name)
 board=Image.new('RGBA',(1600,550),'#FFFCF6');d=ImageDraw.Draw(board);txt(d,(20,15),f'懸浮列 {c} 組 · 16顆單列 · 40dp圓',28)
 for i,name in enumerate(stripfiles):
  txt(d,(20,75+i*220),f'{[24,28][i]}dp圖示 · 草地模擬背景 · 本圖縮放示意，1:1請看HTML',19);im=read(R/name).resize((1568,168),Image.Resampling.LANCZOS);board.alpha_composite(im,(16,112+i*220))
 board.convert('RGB').save(R/f'floatbar-{c}.png')
# Map scene: 390x620dp at4x. Collapse+Expand both included, currentAuto C and approved four peers.
current=json.loads((S/'approved/current-manifest.json').read_text());approved={a['id']:a for a in current['assets']}
def map_source(id,c):return read(REPO/approved[id]['path']) if id in approved else image(id,c)
def map_path(id,c):return approved[id]['path'] if id in approved else imagepath(id,c)
for c in ['A','B']:
 b=Image.new('RGBA',(1560,2480),'#EFEBE3');d=ImageDraw.Draw(b)
 for i,id in enumerate(P['right_column']):
  x=1336;y=288+i*224;d.ellipse((x,y,x+159,y+159),fill='#FFFCF6');paste(b,map_source(id,c),(x+16,y+16),128)
 for id,x,y in [('Layers',64,64),('Settings',272,64),('More',64,2160)]:d.ellipse((x,y,x+159,y+159),fill='#FFFCF6');paste(b,image(id,c),(x+16,y+16),128)
 b.convert('RGB').save(R/f'map-{c}-32dp-xxxhdpi.png')
board=Image.new('RGBA',(1000,980),'#FFFCF6');d=ImageDraw.Draw(board);txt(d,(22,15),'地圖整體 · 40dp圓／32dp插圖',30);txt(d,(22,62),'右側9顆：收合、展開、自動、任務、紀錄、常用、掃描、定位、傳送；更多另放',18)
for i,c in enumerate(['A','B']):
 txt(d,(40+i*500,112),c+' 組（batch1與Auto C沿用）',22);im=read(R/f'map-{c}-32dp-xxxhdpi.png').resize((429,682),Image.Resampling.LANCZOS);board.alpha_composite(im,(30+i*500,160))
txt(d,(22,885),'A/B只是候選整套排列；可在HTML逐項切換，不代表整套核准。',19);board.convert('RGB').save(R/'map-comparison.png')
# Native32/48/64 thumbnail sheet of all44 new candidates.
b=Image.new('RGBA',(1600,120+11*150),'#FFFCF6');d=ImageDraw.Draw(b);txt(d,(22,15),'32／48／64 px · 全44張新候選',28)
for i,a in enumerate(assets):
 x=15+(i%4)*400;y=85+(i//4)*150;txt(d,(x+8,y),a['id']+' '+a['concept'],18)
 for j,size in enumerate([32,48,64]):paste(b,images[a['id'],a['concept']],(x+25+j*100,y+42+(64-size)//2),size)
b.convert('RGB').save(R/'thumbnails.png')
# Confusion check: Auto vs unchangedGoldBasin vs twoReturnToApp designs, same scale.
dist=[('Auto C',read(REPO/approved['Auto']['path'])),('GoldBasin D',goldim),('ReturnToApp A',image('ReturnToApp','A')),('ReturnToApp B',image('ReturnToApp','B'))]
b=Image.new('RGBA',(1400,760),'#FFFCF6');d=ImageDraw.Draw(b);txt(d,(22,15),'語意區分 · 自動／拉金盆／回到App',28)
for i,(name,im) in enumerate(dist):
 x=20+i*345;paste(b,im,(x+45,90),230);txt(d,(x+20,340),name,21)
 for j,dp in enumerate([24,28,32]):
  xx=x+15+j*105;d.ellipse((xx,400,xx+79,479),fill='#EFEBE3');paste(b,im,(xx+(80-dp*2)//2,400+(80-dp*2)//2),dp*2);txt(d,(xx,494),f'{dp}dp',17)
txt(d,(22,585),'Auto：果實＋循環箭頭；GoldBasin：原金盆＋向下箭頭。',20);txt(d,(22,630),'ReturnToApp：紅菇／小屋＋向左回頭箭頭；請確認小尺寸不會混淆。',20);b.convert('RGB').save(R/'semantic-distinction.png')
# Blind page: no letters/numbers/labels in the image, answers in a separate markdown.
order=assets.copy();random.Random(110523).shuffle(order);b=Image.new('RGBA',(1440,8*180),'#EFEBE3')
for i,a in enumerate(order):paste(b,images[a['id'],a['concept']],(25+(i%6)*240,15+(i//6)*180),150)
b.convert('RGB').save(R/'blind-test.png');answers=['# 無文字辨識答案','先看blind-test.png；由上到下、每列由左到右。','']
for i,a in enumerate(order):answers.append(f'- 第{i//6+1}列第{i%6+1}欄：{a["id"]} {a["concept"]} — {a["label"]}')
(R/'blind-answers.md').write_text('\n'.join(answers)+'\n')
# Direct-original HTML. Choices affect previews only, never approval or a remote service.
css='''*{box-sizing:border-box}body{font:16px system-ui,sans-serif;background:#FFFCF6;color:#2E3A2F;margin:24px}h1{font-size:29px}h2{margin-top:36px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.card{background:#EFEBE3;border-radius:12px;padding:16px}.pair{display:flex;align-items:center;gap:16px;flex-wrap:wrap}.samples{display:flex;gap:18px;align-items:center;margin:14px 0}.samples span{display:inline-flex;flex-direction:column;gap:6px}.hero{width:140px;height:140px;object-fit:contain}.dark{background:#25372C}.checker{background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 0/16px 16px}.scroller{overflow:auto;max-width:100%}.floatrow{width:784px;height:84px;background-image:url(REPLACE_GRASS);background-size:cover;display:flex;gap:8px;padding:8px;align-items:flex-start}.floatcell{width:40px;flex-shrink:0;text-align:center}.circle{width:40px;height:40px;border-radius:50%;background:#FFFCF6;display:flex;align-items:center;justify-content:center;flex-shrink:0}.circle img{object-fit:contain}.pill{margin-top:6px;background:#2E3A2F;color:#FFFCF6;border-radius:8px;font-size:7px;padding:3px 1px}.maps{display:flex;gap:24px;flex-wrap:wrap}.mapscene{position:relative;width:390px;height:620px;background:#EFEBE3;flex-shrink:0}.mapbuttons{position:absolute;right:16px;top:72px;display:flex;flex-direction:column;gap:16px}.topbuttons{position:absolute;left:16px;top:16px;display:flex;gap:12px}.morebutton{position:absolute;left:16px;top:540px}.blind{display:grid;grid-template-columns:repeat(6,120px);gap:15px}.blind img{width:110px;height:110px}select{padding:7px;margin:6px}summary{cursor:pointer}'''.replace('REPLACE_GRASS',rel('brand/ui/illustrated-v1/references/simulated-grass.png'))
h=['<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>插圖風batch2／batch3候選</title><style>'+css+'</style><h1>懸浮列＋地圖圓鈕 · illustrated-v1 候選</h1><p>2026-11-05。44張新PNG均candidate，金盆D為既有核准參考。沒有新增核准紀錄、approved目錄或App改動。草地為模擬背景；CSS尺寸檢查不等於實機驗證。</p><p><a href="floatbar-concepts.png">懸浮列A/B概念板</a> · <a href="map-concepts.png">地圖A/B概念板</a> · <a href="thumbnails.png">縮圖板</a> · <a href="semantic-distinction.png">Auto／金盆／回App比較</a> · <a href="catalog.json">實測與SHA-256</a></p><h2>無文字辨識測試</h2><p>先看圖，再對照獨立答案。圖示本身沒有用途文字。</p><div class="blind">']
for a in order:h.append(f'<img src="{rel(a["final"]["path"])}" alt="">')
h.append('</div><p><a href="blind-answers.md">另開答案</a></p><details><summary>展開答案</summary><ol>'+''.join(f'<li>第{i//6+1}列第{i%6+1}欄：{a["id"]} {a["concept"]} — {a["label"]}</li>' for i,a in enumerate(order))+'</ol></details>')
for batch,ids in [('floatbar',floatids),('map',mapids)]:
 h.append('<h2>'+('懸浮列：24／28dp圖示' if batch=='floatbar' else '地圖：32dp圖示；Collapse與Expand連動')+'</h2><div>')
 for id in ids:
  if id in ['GoldBasin','Expand']:continue
  h.append(f'<label>{id}<select data-choice="{id}"><option>A</option><option>B</option></select></label>')
 h.append('</div>')
 if batch=='floatbar':
  for dp in [24,28]:
   h.append(f'<h3>40dp圓／{dp}dp插圖 · 16顆單列，可橫向捲動</h3><div class="scroller"><div class="floatrow" data-batch="floatbar">')
   for id in floatids:h.append(f'<div class="floatcell"><div class="circle"><img data-icon="{id}" src="{rel(imagepath(id,"A"))}" width="{dp}" height="{dp}" alt=""></div><div class="pill">{id}</div></div>')
   h.append('</div></div>')
 else:
  h.append('<div class="maps">')
  for c in ['A','B']:
   h.append(f'<section><h3>{c}基準地圖 · 右側9顆／頂欄2顆／更多另放</h3><div class="mapscene" data-batch="map" data-base="{c}"><div class="mapbuttons">')
   for id in P['right_column']:h.append(f'<div class="circle"><img {"data-icon="+chr(34)+id+chr(34) if id not in approved else ""} src="{rel(map_path(id,c))}" width="32" height="32" alt="{id}"></div>')
   h.append('</div><div class="topbuttons">')
   for id in ['Layers','Settings']:h.append(f'<div class="circle"><img data-icon="{id}" src="{rel(imagepath(id,c))}" width="32" height="32" alt="{id}"></div>')
   h.append(f'</div><div class="morebutton"><div class="circle"><img data-icon="More" src="{rel(imagepath("More",c))}" width="32" height="32" alt="More"></div></div></div></section>')
  h.append('</div><p>兩張是全A／全B初始比較；切換任一選單後該功能在兩邊同步，方便比較混搭。</p>')
h.append('<h2>原圖與32／48／64px · 深底／棋盤底</h2><div class="grid">')
for a in assets:
 p=rel(a['final']['path']);folder=os.path.dirname(p);h.append(f'<article class="card"><h3>{a["id"]} {a["concept"]} · {a["label"]}</h3><img class="hero" src="{p}" alt="{a["id"]} {a["concept"]}"><p>candidate · {"精確翻轉來源Collapse" if a["id"]=="Expand" else "image_gen"}</p><div class="samples">'+''.join(f'<span><img src="{p}" width="{z}" height="{z}" alt="">{z}px</span>' for z in [32,48,64])+f'</div><div class="samples"><span class="dark"><img src="{p}" width="80" height="80" alt=""></span><span class="checker"><img src="{p}" width="80" height="80" alt=""></span></div><a href="{folder}/PROMPT.json">完整prompt</a> · <a href="{folder}/METADATA.json">metadata</a></article>')
h.append('</div>')
lookup={id:{c:rel(imagepath(id,c)) for c in ['A','B']} for id in floatids+mapids}
h.append('<script>const paths='+json.dumps(lookup)+';document.querySelectorAll("select[data-choice]").forEach(s=>s.addEventListener("change",()=>{const ids=s.dataset.choice==="Collapse"?["Collapse","Expand"]:[s.dataset.choice];document.querySelectorAll("img[data-icon]").forEach(i=>{if(ids.includes(i.dataset.icon))i.src=paths[i.dataset.icon][s.value];});}));'+'</script></html>')
(R/'index.html').write_text('\n'.join(h))
print('Prepared 44 candidate PNGs + unchanged gold reference; catalogs, floatbar A/B, map A/B, contact sheets, thumbnails, blind page and interactive HTML.')
