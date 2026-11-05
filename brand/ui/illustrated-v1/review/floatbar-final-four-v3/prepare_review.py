from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib,os,random
R=Path(__file__).resolve().parent;S=R.parents[1];REPO=S.parents[2];P=json.loads((R/'PLAN.json').read_text());FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def txt(d,xy,t,z=19):d.text(xy,t,font=ImageFont.truetype(FONT,z),fill='#2E3A2F')
def load(p):return Image.open(p).convert('RGBA')
def paste(b,im,xy,z):b.alpha_composite(im.resize((z,z),Image.Resampling.LANCZOS),xy)
def savejson(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def rel(p):return os.path.relpath(REPO/p,R)
def stat(p):
 im=Image.open(p);a=im.convert('RGBA').getchannel('A');return dict(path=str(p.relative_to(REPO)),dimensions_px=list(im.size),mode=im.mode,alpha_extrema=list(a.getextrema()),bbox_alpha_nonzero=list(a.getbbox() or []),bbox_alpha128=list(a.point(lambda v:255 if v>=128 else 0).getbbox() or []),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assets=[]
for a in P['assets']:
 folder=S/a['directory'];raw=folder/'generated-original.png';im=load(raw);box=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();scale=min(1254/im.width,1254/im.height,1054/max(box[2]-box[0],box[3]-box[1]));offset=[round(627-(box[0]+box[2])*scale/2),round(627-(box[1]+box[3])*scale/2)];b=Image.new('RGBA',(1254,1254));b.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),tuple(offset));b.save(folder/'icon.png');m={k:v for k,v in a.items() if k!='prompt'};m.update(original=stat(raw),final=stat(folder/'icon.png'),mechanical_operations=[dict(operation='uniform scale/transparent canvas translation only',scale=scale,offset_px=offset)]);savejson(folder/'METADATA.json',m);assets.append(m)
savejson(R/'catalog.json',dict(date=P['date'],status='candidate',assets=assets,original_count=8,derived_count=0))
by={(a['id'],a['concept']):a for a in assets};newids=['Feed','ReturnToApp','GameReturn','HideFloat'];labels={a['id']:a['label'] for a in assets};approved={}
for f in ['batch2-floatbar','batch3-map']:
 m=json.loads((S/'approved'/f/('current-manifest.json' if f=='batch3-map' else 'manifest.json')).read_text());approved.update({a['id']:a for a in m['assets']})
core=json.loads((S/'approved/current-manifest.json').read_text());approved.update({a['id']:a for a in core['assets']});approved['GoldBasin']=core['existing_approved_reference']
def path(id,c):return by[id,c]['final']['path'] if (id,c) in by else approved[id]['path']
def image(id,c):return load(REPO/path(id,c))
# A/B concept sheet, identical canvas size for all14 new icons.
b=Image.new('RGBA',(1600,410),'#FFFCF6');d=ImageDraw.Draw(b);txt(d,(24,16),'四項重畫 v3 · 8張新候選',30);txt(d,(24,65),'已核准圖全部維持；以下全為candidate，尚未核准或推送',18)
for i,id in enumerate(newids):
 x=10+i%4*400;y=116+i//4*290;txt(d,(x+12,y),id+' · '+labels[id],21)
 for j,c in enumerate(['A','B']):paste(b,image(id,c),(x+15+j*190,y+34),170);txt(d,(x+75+j*190,y+216),c,19)
b.convert('RGB').save(R/'concepts.png')
b=Image.new('RGBA',(1600,420),'#FFFCF6');d=ImageDraw.Draw(b);txt(d,(24,15),'32／48／64px · 新候選縮圖',27)
for i,a in enumerate(assets):
 x=10+i%4*400;y=82+i//4*160;txt(d,(x+4,y),a['id']+' '+a['concept'],16)
 for j,z in enumerate([32,48,64]):paste(b,image(a['id'],a['concept']),(x+5+j*70,y+40+(64-z)//2),z)
b.convert('RGB').save(R/'thumbnails.png')
grass=load(S/'references/simulated-grass.png');floatids=['GoldBasin','Feed','Dispatch','LightSpeed','Ticket','FloatMenu','ReturnToApp','GameReturn','HideFloat','Play','Pause','Stop','SkipBack','SkipForward','Check','Close'];right=['Collapse','Expand','Auto','Tasks','Records','Favorites','Scan','Locate','Teleport']
for c in ['A','B']:
 for dp in [24,28]:
  b=ImageOps.fit(grass,(3136,336));d=ImageDraw.Draw(b)
  for i,id in enumerate(floatids):
   x=32+i*192;d.ellipse((x,32,x+159,191),fill='#FFFCF6');paste(b,image(id,c),(x+(160-dp*4)//2,32+(160-dp*4)//2),dp*4);d.rounded_rectangle((x-8,216,x+168,296),radius=30,fill='#2E3A2F');d.text((x+2,237),id,font=ImageFont.truetype(FONT,19),fill='#FFFCF6')
  b.convert('RGB').save(R/f'floatbar-{c}-{dp}dp-xxxhdpi.png')
 b=Image.new('RGBA',(1560,2480),'#EFEBE3');d=ImageDraw.Draw(b)
 for i,id in enumerate(right):
  x=1336;y=288+i*224;d.ellipse((x,y,x+159,y+159),fill='#FFFCF6');paste(b,image(id,c),(x+16,y+16),128)
 for id,x,y in [('Layers',64,64),('Settings',272,64),('More',64,2160)]:d.ellipse((x,y,x+159,y+159),fill='#FFFCF6');paste(b,image(id,c),(x+16,y+16),128)
 b.convert('RGB').save(R/f'map-{c}-32dp-xxxhdpi.png')
# Compare changed returns with fixed Auto/Gold.
ids=['Auto','GoldBasin','ReturnToApp','GameReturn','HideFloat'];b=Image.new('RGBA',(1500,680),'#FFFCF6');d=ImageDraw.Draw(b);txt(d,(20,15),'辨識比較 · 固定Auto C／金盆D＋新回App／回遊戲／隱藏',28)
for i,id in enumerate(ids):
 x=10+i*300;txt(d,(x+8,70),id,20)
 for j,c in enumerate(['A','B']):paste(b,image(id,c),(x+45,110+j*250),200);txt(d,(x+12,315+j*250),c if id in newids else '沿用已核准',17)
b.convert('RGB').save(R/'semantic-distinction.png')
order=assets.copy();random.Random(11052).shuffle(order);b=Image.new('RGBA',(1200,570),'#EFEBE3')
for i,a in enumerate(order):paste(b,image(a['id'],a['concept']),(20+i%4*300,20+i//4*270),150)
b.convert('RGB').save(R/'blind-test.png');(R/'blind-answers.md').write_text('# 無文字辨識答案\n\n'+'\n'.join(f'- 第{i//4+1}列第{i%4+1}欄：{a["id"]} {a["concept"]} — {a["label"]}' for i,a in enumerate(order))+'\n')
css='''*{box-sizing:border-box}body{background:#FFFCF6;color:#2E3A2F;font:16px sans-serif;margin:24px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.card{padding:15px;background:#EFEBE3;border-radius:12px}.samples{display:flex;align-items:center;gap:15px;margin:15px 0}.samples span{display:inline-flex;flex-direction:column;gap:6px}.scroller{overflow:auto}.floatrow{width:784px;height:84px;display:flex;gap:8px;padding:8px;background-image:url(GRASS);background-size:cover}.circle{width:40px;height:40px;border-radius:50%;background:#FFFCF6;display:flex;align-items:center;justify-content:center;flex-shrink:0}.floatcell{width:40px;flex-shrink:0;text-align:center}.pill{margin-top:6px;font-size:7px;background:#2E3A2F;color:#FFFCF6;padding:3px;border-radius:8px}.maps{display:flex;gap:24px;flex-wrap:wrap}.mapscene{width:390px;height:620px;background:#EFEBE3;position:relative}.right{position:absolute;right:16px;top:72px;display:flex;flex-direction:column;gap:16px}.top{position:absolute;left:16px;top:16px;display:flex;gap:12px}.more{position:absolute;left:16px;top:540px}.dark{background:#25372C}.check{background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 0/16px 16px}select{padding:7px;margin:6px}img{object-fit:contain}'''.replace('GRASS',rel('brand/ui/illustrated-v1/references/simulated-grass.png'))
h=['<!doctype html><meta charset="utf-8"><title>四項重畫v3候選</title><style>'+css+'</style><h1>四項重畫 v3 · 8張候選</h1><p>2026-11-05；地圖七項已核准；懸浮列僅剩四個ID待選。A/B切換只預覽，不記錄核准；草地為模擬背景，未實機測試。</p><img src="concepts.png" width="1200"><p><a href="thumbnails.png">縮圖</a> · <a href="blind-test.png">無文字辨識</a> · <a href="blind-answers.md">獨立答案</a> · <a href="semantic-distinction.png">與Auto／金盆比較</a> · <a href="catalog.json">實測規格</a></p>']
for id in ['Feed','ReturnToApp','GameReturn','HideFloat']:h.append(f'<label>{id}<select data-choice="{id}"><option>A</option><option>B</option></select></label>')
for dp in [24,28]:
 h.append(f'<h2>完整懸浮列 · 40dp圓／{dp}dp插圖</h2><div class="scroller"><div class="floatrow">')
 for id in floatids:h.append(f'<div class="floatcell"><div class="circle"><img data-id="{id}" src="{rel(path(id,"A"))}" width="{dp}" height="{dp}" alt=""></div><div class="pill">{id}</div></div>')
 h.append('</div></div>')
h.append('<h2>完整地圖 · 40dp圓／32dp插圖</h2><div class="maps">')
for c in ['A','B']:
 h.append(f'<section><h3>{c}基準組合</h3><div class="mapscene"><div class="right">')
 for id in right:h.append(f'<div class="circle"><img data-id="{id}" src="{rel(path(id,c))}" width="32" height="32" alt="{id}"></div>')
 h.append('</div><div class="top">')
 for id in ['Layers','Settings']:h.append(f'<div class="circle"><img data-id="{id}" src="{rel(path(id,c))}" width="32" height="32" alt="{id}"></div>')
 h.append(f'</div><div class="more"><div class="circle"><img src="{rel(path("More",c))}" width="32" height="32" alt="More"></div></div></div></section>')
h.append('</div><div class="grid">')
for a in assets:
 p=rel(a['final']['path']);h.append(f'<article class="card"><h3>{a["id"]} {a["concept"]} · {a["label"]}</h3><img src="{p}" width="160" height="160"><p>candidate</p><div class="samples">'+''.join(f'<span><img src="{p}" width="{z}" height="{z}">{z}px</span>' for z in [32,48,64])+f'</div><div class="samples"><span class="dark"><img src="{p}" width="80" height="80"></span><span class="check"><img src="{p}" width="80" height="80"></span></div><a href="{os.path.dirname(p)}/PROMPT.json">完整prompt</a> · <a href="{os.path.dirname(p)}/METADATA.json">規格</a></article>')
lookup={id:{c:rel(path(id,c)) for c in ['A','B']} for id in newids};js=';document.querySelectorAll("select[data-choice]").forEach(s=>s.addEventListener("change",()=>{const ids=s.dataset.choice==="Collapse"?["Collapse","Expand"]:[s.dataset.choice];document.querySelectorAll("img[data-id]").forEach(i=>{if(ids.includes(i.dataset.id))i.src=paths[i.dataset.id][s.value];});}));'
h.append('</div><script>const paths='+json.dumps(lookup)+js+'</script>');(R/'index.html').write_text('\n'.join(h));print('Prepared8 v3 candidate PNGs, comparison boards, full floatbar/map previews and HTML.')
