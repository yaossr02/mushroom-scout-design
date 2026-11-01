"""Record original model-generated FX layers and arrange them with unmodified bases."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'brand/effects/v0.9-orbit-bold'
LABELS={'fire':'火焰菇','water':'水菇','electric':'電菇','poison':'毒菇','crystal':'水晶菇'}
CSS='''*{box-sizing:border-box}body{margin:0;width:2000px;padding:50px;background:#f6f2e9;color:#374d3d;font-family:"Noto Sans CJK TC",sans-serif}h1{font-size:51px;margin:0 0 15px}h2{font-size:34px;margin:30px 0 18px}p{font-size:23px;line-height:1.6}.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:18px}.card{border:1px solid #deded0;border-radius:20px;padding:18px;background:#fffdf8;text-align:center}.name{font-size:27px;font-weight:700}.id,.hint{font-size:17px;color:#6e7b69}.composition{position:relative;display:inline-block;width:var(--size,300px);height:var(--size,300px);isolation:isolate;vertical-align:bottom}.composition img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.back{z-index:1;clip-path:inset(0 0 46% 0)}.base{z-index:2}.front{z-index:3;clip-path:inset(54% 0 0 0)}.effects-off .fx{visibility:hidden}.mini{display:flex;justify-content:center;gap:24px;margin-top:12px}.mini img{width:110px;height:110px;object-fit:contain}.mini span{font-size:16px}.sizes{display:flex;justify-content:center;gap:24px;align-items:end}.sizes span{font-size:16px}.dark{background:#253c33;color:#fff1db}.checker{background:repeating-conic-gradient(#ecece5 0% 25%,#fffdf8 0% 50%) 0/18px 18px;border-radius:12px}.pair{display:flex;justify-content:center;gap:12px;margin-top:15px}.map{display:flex;justify-content:space-around;align-items:center;padding:24px;background:#e5ebd8;border:2px dashed #9eb673;border-radius:20px}.control{font-size:23px;padding:15px 20px;background:#fff1db;border:1px solid #9eb673;border-radius:12px;display:inline-block;margin:6px 0 24px}.capture .control{display:none}.export{background:transparent;padding:0;width:1254px}.export .composition{display:block}'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def composition(a,size=300):
 return f'<span class="composition" data-element="{a["id"]}" style="--size:{size}px"><img class="fx back" src="/{a["layer"]}" alt=""><img class="base" src="/{a["base"]}" alt="{a["label"]}"><img class="fx front" src="/{a["layer"]}" alt=""></span>'
def main():
 registry=json.loads((ROOT/'brand/catalog.json').read_text());bases={a['id']:a for a in registry['assets'] if a.get('active_reference')}
 sources=json.loads((PACK/'GENERATION-SOURCES.json').read_text())
 approval=json.loads((PACK/'approval.json').read_text())
 assets=[]
 for id,label in LABELS.items():
  original=bases[id+'-mushroom'];base=ROOT/original['path'];assert original['status']=='approved' and sha(base)==original['sha256'],id
  p=PACK/f'layers/{id}.png'
  assert sha(p)==approval['layers'][id],f'{id}: approved FX bytes changed'
  with Image.open(p) as im:
   assert im.mode=='RGBA',id
   alpha=im.getchannel('A');lo,hi=alpha.getextrema();assert lo==0 and hi>0,id
   probes={name:alpha.getpixel((int(im.width*x),int(im.height*y))) for name,x,y in [('upper_cap',.5,.2),('orbit_hole',.5,.54),('stem',.5,.85)]}
   assert max(probes.values())<=16,f'{id}: effect-only transparent center check: {probes}'
   bbox=alpha.point(lambda v:255 if v>=16 else 0).getbbox();assert bbox,id
   assets.append({'id':id,'label':label,'version':'v0.9-orbit-bold','status':'approved','approval_record':approval['record'],'base':original['path'],'base_sha256':sha(base),'base_status':'approved','layer':str(p.relative_to(ROOT)),'layer_sha256':sha(p),'dimensions_px':list(im.size),'mode':im.mode,'alpha_range':[lo,hi],'bbox_alpha16':list(bbox),'body_bbox_alpha128':alpha.point(lambda v:255 if v>=128 else 0).getbbox(),'transparent_probes':probes,'original_generation':sources[id],'date':'2026-11-01','tool':'image_gen','composite_preview':f'brand/effects/v0.9-orbit-bold/composites/{id}.png','composition':{'frame_px':[1254,1254],'base_scale':1,'effect_scale':1,'effect_translate':[0,0],'split_y':.54,'back_clip':'inset(0 0 46% 0)','front_clip':'inset(54% 0 0 0)','order':['effect upper partition','original mushroom','effect lower partition'],'opacity':1}})
 c={'approval_record':approval['record'],'version':'v0.9-orbit-bold','direction':'B 環繞流動','direction_selected':True,'status':'approved','independent_effect_layers_generated':True,'base_files_modified':False,'effect_count':5,'assets':assets,'composition_note':'Same unmodified FX PNG used twice with complementary CSS depth clips; original base PNG between them. No base redraw, no programmatic effect painting.','runtime_animation_generated':False,'app_runtime_tested':False}
 (PACK/'catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
 s='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>元素菇 B 環繞流動</title><style>'+CSS+'</style><h1>元素菇 · B 環繞流動強化版</h1><p>v0.9 · 5 種強化獨立特效 × 原始 v0.5 核准蘑菇｜五種特效已核准<br>原始蘑菇直接引用，未重畫或覆蓋；環繞感由前後分層呈現。以下為靜態視覺，尚非執行中的動畫。</p><label class="control"><input id="showfx" type="checkbox" checked> 顯示環繞特效（取消可對照原稿）</label><div class="grid">'
 for a in assets:
  s+=f'<article class="card"><div class="name">{a["label"]}</div><div class="id">{a["id"]} · 已核准</div><div class="hero">{composition(a)}</div><div class="mini"><span><img src="/{a["base"]}" alt="原稿"><br>原始蘑菇</span><span class="checker"><img src="/{a["layer"]}" alt="獨立特效層"><br>獨立特效層</span></div></article>'
 s+='</div><h2>32／48／64 px · 原圖分層預覽</h2><div class="grid">'
 for a in assets:s+=f'<div class="card"><div class="name">{a["label"]}</div><div class="sizes">'+''.join(f'<span>{composition(a,n)}<br>{n}px</span>' for n in (32,48,64))+'</div></div>'
 s+='</div><h2>深色與棋盤底</h2><div class="grid">'
 for a in assets:s+=f'<div class="card dark"><div class="name">{a["label"]}</div><div class="pair"><span>{composition(a,145)}</span><span class="checker">{composition(a,145)}</span></div></div>'
 s+='</div><h2>地圖定位示意</h2><div class="map">'+''.join(composition(a,145) for a in assets)+'</div><p class="hint">地圖擺放示意，非 App 實機畫面。特效與原稿均為 PNG；透明合成匯出是瀏覽器渲染結果，不是重新生成的蘑菇。五種元素特效與合成配置已經使用者明確核准。</p><script>document.querySelector("#showfx").onchange=e=>document.body.classList.toggle("effects-off",!e.target.checked)</script></html>'
 # Present the independent effect at full review size, with immutable approved bases.
 standalone='<h2>01　強化獨立特效層</h2><div class="grid">'
 for a in assets:
  standalone+=f'<div class="card"><div class="name">{a["label"]}</div><div style="background:#253c33;border-radius:18px;margin:12px auto;width:300px;height:300px"><img src="/{a["layer"]}" style="width:300px;height:300px;object-fit:contain" alt="{a["label"]}獨立強化特效"></div><div class="hint">獨立透明 PNG · 示意底色</div></div>'
 standalone+='</div><h2>02　強化特效與原稿合成</h2>'
 s=s.replace('<div class="grid">',standalone+'<div class="grid">',1)
 (PACK/'review/index.html').write_text(s)
 export='<!doctype html><meta charset="utf-8"><style>'+CSS+'</style><body class="export">'+''.join(f'<div id="export-{a["id"]}">{composition(a,1254)}</div>' for a in assets)+'</body>'
 (PACK/'review/export.html').write_text(export)
 print('Verified five original base hashes; five RGBA FX layers with transparent cap/hole/stem probes; built review and full-resolution export layouts.')
if __name__=='__main__':main()
