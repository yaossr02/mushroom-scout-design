from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib,os
R=Path(__file__).resolve().parent;S=R.parents[1];REPO=S.parents[2];P=json.loads((R/'PLAN.json').read_text());FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def txt(d,xy,t,z=19,color='#2E3A2F'):d.text(xy,t,font=ImageFont.truetype(FONT,z),fill=color)
def load(p):return Image.open(p).convert('RGBA')
def paste(b,im,xy,z):b.alpha_composite(im.resize((z,z),Image.Resampling.LANCZOS),xy)
def rel(p):return os.path.relpath(REPO/p,R)
def stat(p):
 im=Image.open(p);a=im.convert('RGBA').getchannel('A');return dict(path=str(p.relative_to(REPO)),dimensions_px=list(im.size),mode=im.mode,alpha_extrema=list(a.getextrema()),bbox_alpha_nonzero=list(a.getbbox() or []),bbox_alpha128=list(a.point(lambda v:255 if v>=128 else 0).getbbox() or []),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
if (S/'approved/batch2-floatbar/completion-v4/manifest.json').exists():raise SystemExit('Final v4 is approved and frozen. Create a new version for further changes.')
assets=[]
for a in P['assets']:
 folder=S/a['directory'];raw=folder/'generated-original.png';im=load(raw);box=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();scale=min(1254/im.width,1254/im.height,1054/max(box[2]-box[0],box[3]-box[1]));off=[round(627-(box[0]+box[2])*scale/2),round(627-(box[1]+box[3])*scale/2)];b=Image.new('RGBA',(1254,1254));b.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),tuple(off));b.save(folder/'icon.png');m={k:v for k,v in a.items() if k!='prompt'};m.update(original=stat(raw),final=stat(folder/'icon.png'),mechanical_operations=[dict(operation='Uniform scale/transparent canvas translation only; no drawing or shape edits',scale=scale,offset_px=off)]);(folder/'METADATA.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');assets.append(m)
(R/'catalog.json').write_text(json.dumps({'date':P['date'],'status':'candidate','assets':assets},ensure_ascii=False,indent=2)+'\n');by={a['id']:a for a in assets};ims={id:load(REPO/a['final']['path']) for id,a in by.items()};titles={'Feed':'自動＋咬一口蘋果','ReturnToApp':'B主體＋A黃色返回箭頭','GameReturn':'同款主體與返回箭頭＋手把'}
b=Image.new('RGBA',(1500,1130),'#FFFCF6');d=ImageDraw.Draw(b);txt(d,(25,15),'最後三項 v4 · 依指定修改 · 全部candidate',29)
for i,id in enumerate(['Feed','ReturnToApp','GameReturn']):
 x=15+i*500;paste(b,ims[id],(x+65,95),340);txt(d,(x+20,455),id+' · '+titles[id],20)
 for j,z in enumerate([32,48,64,96,112]):paste(b,ims[id],(x+12+j*95,530+(112-z)//2),z);txt(d,(x+12+j*95,654),str(z)+'px',16)
 txt(d,(x+15,700),'32 / 48 / 64px；96 / 112px = 24 / 28dp @4x',16)
grass=load(S/'references/simulated-grass.png')
for bi,bg in enumerate(['map','grass']):
 strip=Image.new('RGBA',(1460,130),'#EFEBE3') if bg=='map' else ImageOps.fit(grass,(1460,130));dd=ImageDraw.Draw(strip)
 for i,id in enumerate(['Feed','ReturnToApp','GameReturn']):
  for j,dp in enumerate([24,28]):
   x=i*500+75+j*180;dd.ellipse((x,10,x+79,89),fill='#FFFCF6');paste(strip,ims[id],(x+(80-dp*2)//2,10+(80-dp*2)//2),dp*2);dd.rounded_rectangle((x-3,94,x+83,129),radius=10,fill='#FFFCF6');txt(dd,(x+5,95),str(dp)+'dp',17)
 txt(d,(25,755+bi*180),('奶油底' if bg=='map' else '模擬草地')+' · 40dp圓／24、28dp圖示（本板放大2倍）',19);b.alpha_composite(strip,(20,790+bi*180))
b.convert('RGB').save(R/'comparison.png');b.crop((0,0,1500,505)).convert('RGB').save(R/'concepts.png')
base=json.loads((S/'approved/batch2-floatbar/current-manifest.json').read_text());paths={a['id']:a['path'] for a in base['assets']};paths['GoldBasin']=base['existing_approved_reference']['path'];paths.update({id:a['final']['path'] for id,a in by.items()});floatids=['GoldBasin','Feed','Dispatch','LightSpeed','Ticket','FloatMenu','ReturnToApp','GameReturn','HideFloat','Play','Pause','Stop','SkipBack','SkipForward','Check','Close']
for dp in [24,28]:
 b=ImageOps.fit(grass,(3136,336));dd=ImageDraw.Draw(b)
 for i,id in enumerate(floatids):
  x=32+i*192;dd.ellipse((x,32,x+159,191),fill='#FFFCF6');paste(b,load(REPO/paths[id]),(x+(160-dp*4)//2,32+(160-dp*4)//2),dp*4);dd.rounded_rectangle((x-8,216,x+168,296),radius=30,fill='#2E3A2F');txt(dd,(x+2,237),id,19,'#FFFCF6')
 b.convert('RGB').save(R/f'floatbar-{dp}dp-xxxhdpi.png')
auto='brand/ui/illustrated-v1/approved/auto-C-v2/icon.png';compare=[('Auto C（沿用）',load(REPO/auto)),('Feed v4',ims['Feed']),('GoldBasin D（沿用）',load(REPO/paths['GoldBasin'])),('ReturnToApp v4',ims['ReturnToApp']),('GameReturn v4',ims['GameReturn'])];b=Image.new('RGBA',(1500,400),'#FFFCF6');dd=ImageDraw.Draw(b);txt(dd,(24,15),'語意比較 · 完整蘋果／咬一口蘋果／金盆／蘑菇程式／遊戲',25)
for i,(name,im) in enumerate(compare):paste(b,im,(25+i*300,90),230);txt(dd,(25+i*300,335),name,18)
b.convert('RGB').save(R/'semantic-distinction.png')
b=Image.new('RGBA',(900,260),'#EFEBE3')
for i,id in enumerate(['GameReturn','Feed','ReturnToApp']):paste(b,ims[id],(40+i*300,20),220)
b.convert('RGB').save(R/'blind-test.png');(R/'blind-answers.md').write_text('# 無文字答案\n\n由左至右：GameReturn、Feed、ReturnToApp。\n')
css='''*{box-sizing:border-box}body{font:16px sans-serif;background:#FFFCF6;color:#2E3A2F;margin:24px}.scroller{overflow:auto}.floatrow{width:784px;height:84px;display:flex;gap:8px;padding:8px;background-image:url(GRASS);background-size:cover}.cell{width:40px;flex-shrink:0;text-align:center}.circle{width:40px;height:40px;border-radius:50%;background:#FFFCF6;display:flex;align-items:center;justify-content:center}.pill{margin-top:6px;font-size:7px;color:#FFFCF6;background:#2E3A2F;border-radius:8px;padding:3px}.samples{display:flex;gap:18px;align-items:center}.samples span{display:inline-flex;flex-direction:column;gap:6px}.dark{background:#25372C}.check{background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 0/16px 16px}img{object-fit:contain}'''.replace('GRASS',rel('brand/ui/illustrated-v1/references/simulated-grass.png'))
h=['<!doctype html><meta charset="utf-8"><title>最後三項 v4候選</title><style>'+css+'</style><h1>最後三項 v4 · 依指定修改</h1><p>三張新稿全部candidate。HideFloat A已核准並推送；其他核准圖不變。草地是模擬背景，未實機測試。</p><img src="concepts.png" width="1200"><p><a href="comparison.png">小尺寸比較</a> · <a href="semantic-distinction.png">Auto與Feed／回App與回遊戲比較</a> · <a href="blind-test.png">無文字圖</a> · <a href="blind-answers.md">答案</a> · <a href="catalog.json">實測與SHA-256</a></p>']
for dp in [24,28]:
 h.append(f'<h2>完整懸浮列 · 40dp圓／{dp}dp圖示</h2><div class="scroller"><div class="floatrow">')
 for id in floatids:h.append(f'<div class="cell"><div class="circle"><img src="{rel(paths[id])}" width="{dp}" height="{dp}" alt="{id}"></div><div class="pill">{id}</div></div>')
 h.append('</div></div>')
for id,a in by.items():
 p=rel(a['final']['path']);h.append(f'<h2>{id} · candidate</h2><div class="samples">'+''.join(f'<span><img src="{p}" width="{z}" height="{z}">{z}px</span>' for z in [32,48,64,96,112])+f'<span class="dark"><img src="{p}" width="80" height="80"></span><span class="check"><img src="{p}" width="80" height="80"></span></div><p><a href="{os.path.dirname(p)}/PROMPT.json">完整prompt與附圖</a> · <a href="{os.path.dirname(p)}/METADATA.json">metadata</a></p>')
(R/'index.html').write_text('\n'.join(h));print('Prepared3 v4 candidates, full floatbar, 32/48/64px and24/28dp previews, comparison and HTML.')
