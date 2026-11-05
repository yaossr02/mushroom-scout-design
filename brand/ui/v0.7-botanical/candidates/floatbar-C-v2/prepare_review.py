"""Gentle palette/alpha/canvas cleanup and review of the C-GoldBasin-based redesign."""
from pathlib import Path
import json, hashlib, shutil, html
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT=Path(__file__).resolve().parent
CAND=ROOT.parent
PAL=np.array([(46,58,47),(255,241,219),(243,108,99)],dtype=np.int32)
JOBS=json.loads((ROOT/'generation-jobs.json').read_text())
IDS=['HideFloat','GoldBasin','Ticket','Dispatch','Feed','LightSpeed','ReturnToApp','Close','FloatMenu','Play','Pause','SkipBack','SkipForward','Stop','GameReturn','Check']
LABEL={j['id']:j['label'] for j in JOBS};LABEL['GoldBasin']='金盆（沿用基準）'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(id):
 p=ROOT/id/'icon.png'
 if (ROOT/'approval.json').exists():
  a=json.loads((ROOT/'approval.json').read_text());expected=next(i['sha256'] for i in a['assets'] if i['id']==id)
  assert digest(p)==expected,'Approved pixels changed: '+id
  meta=json.loads((ROOT/id/'metadata.json').read_text());assert meta['status']=='approved'
  return meta
 if id!='GoldBasin':
  original=ROOT/id/'generated-original.png';im=Image.open(original).convert('RGBA');a=np.array(im);mask=a[:,:,3]>=128
  labs,n=ndi.label(mask);sizes=np.bincount(labs.ravel());valid=sizes>=150;valid[0]=False;mask=valid[labs]
  rgb=a[:,:,:3].astype(np.int32);dist=((rgb[:,:,None,:]-PAL[None,None,:,:])**2).sum(3);idx=dist.argmin(2)
  # Restore fully enclosed near-black extraction holes, retaining colored cutouts.
  holes=ndi.binary_fill_holes(mask)&~mask;hl,nh=ndi.label(holes)
  for label,sl in enumerate(ndi.find_objects(hl),1):
   if sl is None:continue
   region=hl[sl]==label
   if region.sum()<250000 and (rgb[sl][region].mean(1)<100).mean()>.85:
    whole=(hl==label);boundary=ndi.binary_dilation(whole)&mask
    vote=np.bincount(idx[boundary],minlength=3)
    if not vote.sum() or vote.max()/vote.sum()<.8:continue
    color=int(vote.argmax());yy,xx=np.where(region);mask[yy+sl[0].start,xx+sl[1].start]=True;idx[yy+sl[0].start,xx+sl[1].start]=color
  out=np.zeros_like(a);out[:,:,:3]=PAL[idx].astype('uint8');out[:,:,3]=mask.astype('uint8')*255;out[~mask]=0
  im=Image.fromarray(out,'RGBA');box=im.getbbox();im=im.crop(box);scale=min(1054/im.width,1054/im.height);size=(round(im.width*scale),round(im.height*scale));im=im.resize(size,Image.Resampling.NEAREST)
  canvas=Image.new('RGBA',(1254,1254));canvas.paste(im,((1254-size[0])//2,(1254-size[1])//2));canvas.save(p)
 im=Image.open(p).convert('RGBA');a=np.array(im);mask=a[:,:,3]>127;colors=im.getcolors(5)
 if colors is None:raise ValueError('Palette not flat: '+id)
 ink=mask&np.all(a[:,:,:3]==PAL[0],axis=2);red=mask&np.all(a[:,:,:3]==PAL[2],axis=2)
 d=ndi.distance_transform_edt(ink);ridge=(d>=ndi.maximum_filter(d,size=3)-.01)&(d>=15);width=float(np.percentile(2*d[ridge],10))/62.7 if ridge.any() else None
 rl,n=ndi.label(red);sizes=np.bincount(rl.ravel());sizes[0]=0;minimum=None
 if n:
  yy,xx=np.where(rl==sizes.argmax());minimum=min(xx.max()-xx.min()+1,yy.max()-yy.min()+1)/62.7
 flags=[]
 if width is not None and width<1.75:flags.append('ink_width_p10_estimate_below_1.75dp')
 if minimum is None:flags.append('coral_accent_missing')
 elif minimum<3:flags.append('accent_bbox_min_edge_below_3dp')
 components=[int(v) for v in sizes[1:] if v>=500] if n else []
 if len(components)>1:flags.append('multiple_coral_components_review_required')
 if id=='GoldBasin':flags.append('reused_reference_retains_prior_geometry_limits')
 meta=dict(date='2026-11-04',id=id,label=LABEL[id],status='candidate',dimensions_px=list(im.size),mode=im.mode,alpha_range=list(im.getchannel('A').getextrema()),bbox=list(im.getbbox()),sha256=digest(p),palette_rgb=[list(rgba[:3]) for count,rgba in colors if rgba[3]>0],ink_width_p10_dp20_estimate=round(width,3) if width else None,ink_width_p10_dp24_estimate=round(width*1.2,3) if width else None,accent_min_bbox_edge_dp20=round(minimum,3) if minimum else None,coral_component_count=len(components),qc_flags=flags,cleanup='Exact palette, alpha threshold/speckle cleanup, enclosed dark alpha-hole repair, 8% canvas fit only. No contour inflation or shape redesign by code.',measurement_limit='Ridge percentile is screening, not certified minimum stroke width.',reused_unchanged=id=='GoldBasin')
 if id!='GoldBasin':meta['original_sha256']=digest(ROOT/id/'generated-original.png')
 else:assert digest(p)==digest(CAND/'floatbar-C-v1/GoldBasin/icon.png')
 (ROOT/id/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');pre=ROOT/id/'previews';pre.mkdir(exist_ok=True)
 for n in [20,24,32,48,64,80,96]:im.resize((n,n),Image.Resampling.LANCZOS).save(pre/f'{n}px.png')
 return meta
CSS='''*{box-sizing:border-box}body{margin:0;padding:32px;width:1440px;background:#f5f3eb;color:#2e3a2f;font-family:"Noto Sans CJK TC",sans-serif}h1{font-size:34px;margin:0 0 12px}h2{font-size:24px;margin:24px 0 14px}p{font-size:17px;line-height:1.6}.note{background:#fff1db;border-radius:16px;padding:16px}.scene{background:#69ad48 url('../floatbar-review-v1/simulated-game-background.png') center/cover;border-radius:22px;padding:18px;margin:16px 0}.bar{display:flex;gap:10px;padding:12px 0}.cell{width:40px;display:flex;flex-direction:column;align-items:center;gap:3px;flex:none}.circle{width:40px;height:40px;background:#fffcf6;border-radius:50%;display:flex;align-items:center;justify-content:center}.circle img{width:20px;height:20px;object-fit:contain}.large img{width:24px;height:24px}.pill{font-size:8px;line-height:13px;background:#2e3a2f;color:#fffcf6;border-radius:9px;padding:0 5px;white-space:nowrap}.tag{background:#2e3a2f;color:#fffcf6;padding:4px 12px;border-radius:8px;font-size:14px;display:inline-block}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.card{background:#fffcf6;border:1px solid #d8dfd2;border-radius:18px;padding:16px;text-align:center}.card h3{font-size:19px;margin:5px}.hero{width:125px;height:125px;object-fit:contain;margin:10px auto}.samples{display:flex;align-items:end;justify-content:center;gap:18px;min-height:86px}.samples span{display:flex;flex-direction:column;align-items:center;font-size:11px}.compare{display:flex;justify-content:center;gap:18px;margin-top:14px}.compare>span{font-size:12px;display:flex;flex-direction:column;align-items:center}.compare img{width:48px;height:48px;object-fit:contain}.flags{font-size:11px;color:#8b4432;line-height:1.5;word-break:break-word}.ref{display:flex;align-items:center;gap:24px}.ref img{width:160px;height:160px;object-fit:contain}a{color:#4a6650}'''
def bar(ids,dp=20):
 s='<div class="bar">'
 for id in ids:s+=f'<span class="cell"><span class="circle {"large" if dp==24 else ""}"><img src="{id}/icon.png" alt="{id}"></span><span class="pill">{"金盆" if id=="GoldBasin" else LABEL[id]}</span></span>'
 return s+'</div>'
def build():
 records=[prepare(id) for id in IDS]
 (ROOT/'validation.json').write_text(json.dumps(dict(status='approved' if (ROOT/'approval.json').exists() else 'candidate',new_generated=15,reused_reference=1,all_hard_geometry_certified=False,records=records),ensure_ascii=False,indent=2)+'\n')
 s='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>C金盆風格 · 全套重新設計</title><style>'+CSS+'</style><h1>C 金盆風格 · 懸浮功能列全套重設計 v2</h1><p class="note">15 個圖示全部重新用 image_gen 製作；金盆沿用 C-v1 原檔，沒有更動。全套均為 candidate，沒有核准或修改 App。<br>沿用墨綠實心、連續奶油貼紙邊、墨綠外輪廓與珊瑚紅點綴。背景為模擬遊戲場景，非實機附件。珊瑚紅2.87:1是已接受的色票例外。幾何警示逐張公開，未宣稱全數通過硬門檻。</p><div class="ref"><img src="GoldBasin/icon.png" alt="C金盆風格基準"><p>本輪唯一風格基準：C-v1 金盆<br>保留其圓潤、實心與貼紙邊的語彙；其餘15項不再沿用舊稿。</p></div>'
 for dp in [20,24]:s+=f'<h2>40dp暖白圓／{dp}dp圖示 · 原比例</h2><div class="scene scene-{dp}"><span class="tag">模擬遊戲場景｜{dp}dp</span>'+bar(IDS[:9],dp)+bar(IDS[9:],dp)+'</div>'
 s+='<h2>全套原圖、尺寸預覽與改稿比較</h2><div class="grid">'
 for r in records:
  id=r['id'];s+=f'<article class="card"><h3>{LABEL[id]}</h3><div style="font-size:12px">{id} · candidate</div><img class="hero" src="{id}/icon.png" alt="{id}"><div class="samples">'
  for n in [32,48,64]:s+=f'<span><img src="{id}/previews/{n}px.png" width="{n}" height="{n}" alt="{n}px">{n}px</span>'
  s+=f'</div><div class="compare"><span><img src="../floatbar-C-v1/{id}/icon.png" alt="舊C">舊C</span><span><img src="{id}/previews/80px.png" alt="新C">{"沿用基準" if id=="GoldBasin" else "新C"}</span><span><img src="../floatbar-review-v1/phosphor-reference/{id}.svg" alt="Phosphor">Phosphor參考</span></div><div class="flags">'+html.escape(', '.join(r['qc_flags']) or '篩檢未見旗標；仍待視覺審核')+f'</div><p style="font-size:12px"><a href="{id}/PROMPT.json">完整提示詞</a> · <a href="{id}/metadata.json">尺寸／alpha／hash／量測</a></p></article>'
 s+='</div><p>每張皆為1254×1254透明RGBA PNG，並有20／24dp與32／48／64px預覽。80／96px檔對應xxxhdpi的20／24dp。Phosphor為官方語意參考，未讀App資源。線寬估值不是最細筆畫認證；所有警示保留。<a href="validation.json">完整檢查資料</a></p></html>'
 if (ROOT/'approval.json').exists():
  s=s.replace('全套均為 candidate，沒有核准或修改 App。','全套已獲使用者核准，尚未修改 App。').replace(' · candidate',' · approved')
 (ROOT/'index.html').write_text(s)
 # Short contact sheet for choosing the coherent direction without scrolling a whole report.
 compact=s.split('<h2>全套原圖、尺寸預覽與改稿比較</h2>')[0]+'<h2>全套一覽</h2><div class="grid" style="grid-template-columns:repeat(8,1fr)">'
 for id in IDS:compact+=f'<div class="card"><img src="{id}/icon.png" width="88" height="88" style="object-fit:contain" alt="{id}"><div style="font-size:15px">{LABEL[id]}</div></div>'
 (ROOT/'overview.html').write_text(compact+'</div><p>完整提示詞、尺寸與改稿對照請見 index.html；本輪狀態與固定交付來源見正式manifest；核准PNG不經重新處理。</p></html>')
 print('C-v2:15 newly generated icons + unchanged GoldBasin; review and measurements built.')
if __name__=='__main__':build()
