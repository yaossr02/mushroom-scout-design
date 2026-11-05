from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parent;S=R.parents[1];REPO=S.parents[2]
if (S/'approved/auto-C-v2/approval.json').exists():raise SystemExit('Auto C already approved; create a new candidate version instead.')
plan=json.loads((R/'plan.json').read_text());font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def text(d,xy,s,n=20):d.text(xy,s,font=ImageFont.truetype(font,n),fill='#2E3A2F')
def stats(p):
 im=Image.open(p);a=im.convert('RGBA').getchannel('A');return {'dimensions_px':list(im.size),'mode':im.mode,'alpha_extrema':list(a.getextrema()),'bbox_alpha_nonzero':list(a.getbbox() or []),'bbox_alpha128':list(a.point(lambda n:255 if n>=128 else 0).getbbox() or []),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):return Image.open(p).convert('RGBA')
def paste(b,im,xy,size):b.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),xy)
assets=[]
for c in plan['concepts']:
 p=S/c['path'];raw=p/'generated-original.png';im=load(raw);b=im.getchannel('A').point(lambda n:255 if n>=128 else 0).getbbox();scale=min(1254/im.width,1254/im.height,1054/max(b[2]-b[0],b[3]-b[1]));offset=[round(627-(b[0]+b[2])*scale/2),round(627-(b[1]+b[3])*scale/2)]
 canvas=Image.new('RGBA',(1254,1254));canvas.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),tuple(offset));canvas.save(p/'icon.png')
 meta={**c,'id':'Auto','status':'candidate','date':'2026-11-05','original':stats(raw),'final':stats(p/'icon.png'),'reference':plan['reference'],'mechanical_operations':{'uniform_scale':scale,'offset_px':offset,'note':'Canvas resize/centering only; original shading and alpha retained. No drawing, thickening, outlines or shape edits.'}}
 (p/'METADATA.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');assets.append(meta)
(R/'manifest.json').write_text(json.dumps({'date':'2026-11-05','status':'candidate','assets':assets},ensure_ascii=False,indent=2)+'\n')
current=S/'approved/batch1/Auto.png';cells=[(a['concept']+' '+a['title'],load(S/a['path']/'icon.png'),str((S/a['path']/'icon.png').relative_to(REPO))) for a in assets]+[('現行 Auto（已核准）',load(current),str(current.relative_to(REPO)))]
board=Image.new('RGBA',(1400,1200),'#FFFCF6');d=ImageDraw.Draw(board);text(d,(25,18),'Auto 重新設計 · 三個候選＋現行版',31);text(d,(25,63),'2026-11-05 · 新稿均candidate，尚未取代現行版',19)
for i,(name,im,path) in enumerate(cells):
 x=20+i*345;paste(board,im,(x+25,115),280);text(d,(x+15,410),name,22)
 for j,size in enumerate([32,48,64]):paste(board,im,(x+25+j*100,470+(64-size)//2),size)
 text(d,(x+12,550),'32 / 48 / 64 px',17)
 for j,size in enumerate([80,96]):paste(board,im,(x+40+j*150,600+(96-size)//2),size)
 text(d,(x+12,710),'80 / 96 px（20 / 24 dp @4x）',16)
grass=load(S/'references/simulated-grass.png')
for bi,bg in enumerate(['map','grass']):
 strip=Image.new('RGBA',(1360,150),'#EFEBE3') if bg=='map' else ImageOps.fit(grass,(1360,150));sd=ImageDraw.Draw(strip)
 for i,(name,im,path) in enumerate(cells):
  for j,dp in enumerate([20,24]):
   x=i*345+50+j*140;sd.ellipse((x,10,x+79,89),fill='#FFFCF6');paste(strip,im,(x+(80-dp*2)//2,10+(80-dp*2)//2),dp*2);sd.rounded_rectangle((x-4,96,x+83,140),radius=10,fill='#FFFCF6');text(sd,(x,100),f'{dp}dp',17)
 text(d,(25,770+bi*195),('奶油地圖' if bg=='map' else '模擬草地')+' · 40dp圓／20、24dp圖示（本板放大2倍）',19);board.alpha_composite(strip,(20,810+bi*195))
board.convert('RGB').save(R/'comparison.png');board.crop((0,0,1400,450)).convert('RGB').save(R/'concepts.png')
cohesion=Image.new('RGBA',(1500,330),'#FFFCF6');cd=ImageDraw.Draw(cohesion);text(cd,(20,10),'新Auto候選與已核准系列 · 同大小畫布',25)
peers=[(a['concept'],load(S/a['path']/'icon.png')) for a in assets]+[(id,load(S/'approved/batch1'/f'{id}.png')) for id in ['Tasks','Records','Favorites','Scan']]+[('GoldBasin',load(REPO/'brand/ui/approved/gold-planter-illustrated-v1/icon.png'))]
for i,(name,im) in enumerate(peers):paste(cohesion,im,(i*185+18,80),150);text(cd,(i*185+18,250),name,18)
cohesion.convert('RGB').save(R/'cohesion.png')
html=['<!doctype html><meta charset="utf-8"><title>Auto v2 三候選</title><style>body{background:#FFFCF6;color:#2E3A2F;font:16px sans-serif;margin:24px}.row{display:flex;gap:25px;flex-wrap:wrap}.scene{position:relative;width:360px;height:320px;background:#EFEBE3}.grass{background-image:url(/brand/ui/illustrated-v1/references/simulated-grass.png);background-size:cover}.buttons{position:absolute;right:16px;top:24px;display:flex;flex-direction:column;gap:12px}.circle{width:40px;height:40px;border-radius:50%;background:#FFFCF6;display:flex;align-items:center;justify-content:center}img{object-fit:contain}.dark{background:#28392E}.check{background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 0/16px 16px}</style><h1>Auto v2 · A芽苗齒輪／B芽苗沙漏／C循環果實</h1><p>全部candidate；現行Auto仍保留。草地為模擬背景，未做實機測試。以repo根目錄本機HTTP開啟。</p><img src="concepts.png" width="1200"><p><a href="comparison.png">小尺寸比較</a> · <a href="cohesion.png">與核准系列並排</a> · <a href="manifest.json">實測與SHA-256</a></p><label>預覽Auto<select id="choice">'+''.join(f'<option value="/{p}">{n}</option>' for n,im,p in cells)+'</select></label><div class="row">']
for bg in ['map','grass']:
 for dp in [20,24]:
  html.append(f'<section><h3>{bg} · 圓40dp／圖{dp}dp</h3><div class="scene {bg}"><div class="buttons">')
  for id in ['Auto','Tasks','Records','Favorites','Scan']:
   p=cells[0][2] if id=='Auto' else f'brand/ui/illustrated-v1/approved/batch1/{id}.png';html.append(f'<div class="circle"><img {"data-auto" if id=="Auto" else ""} src="/{p}" width="{dp}" height="{dp}" alt="{id}"></div>')
  html.append('</div></div></section>')
html.append('</div>')
for n,im,p in cells:
 html.append(f'<h2>{n}</h2><div class="row">'+''.join(f'<span><img src="/{p}" width="{z}" height="{z}">{z}px</span>' for z in [32,48,64,80,96])+f'<span class="dark"><img src="/{p}" width="96" height="96"></span><span class="check"><img src="/{p}" width="96" height="96"></span></div>')
html.append('<script>document.querySelector("#choice").addEventListener("change",e=>document.querySelectorAll("[data-auto]").forEach(i=>i.src=e.target.value))</script>')
(R/'index.html').write_text('\n'.join(html))
print('Prepared three candidate PNGs, metadata, comparison, cohesion and HTML.')
