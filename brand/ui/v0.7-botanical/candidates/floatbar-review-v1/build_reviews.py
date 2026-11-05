"""Read only this task's generated candidates, prepare measurements and review pages."""
from pathlib import Path
import json, html, hashlib
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE=Path(__file__).resolve().parent
CAND=HERE.parent
JOBS=json.loads((HERE/'jobs.json').read_text())
INK=(46,58,47);CORAL=(243,108,99);CREAM=(255,241,219)
def luminance(rgb):
    v=np.array(rgb)/255.;v=np.where(v<=.04045,v/12.92,((v+.055)/1.055)**2.4)
    return float(v@np.array([.2126,.7152,.0722]))
def contrast(rgb):return (luminance((255,252,246))+.05)/(luminance(rgb)+.05)
def strokes(mask):
    distance=ndi.distance_transform_edt(mask)
    ridge=(distance>=ndi.maximum_filter(distance,size=3)-.01)&(distance>=15)
    values=distance[ridge]*2
    if len(values)<10:return None
    return {f'p{p}':round(float(np.percentile(values,p))/62.7,3) for p in (10,50,90)}
def inspect(j):
    folder=CAND/f'floatbar-{j["style"]}-v1'/j['id'];im=Image.open(folder/'icon.png').convert('RGBA');arr=np.array(im);mask=arr[:,:,3]>127
    colors=im.getcolors(5)
    if colors is None:raise ValueError('Unexpected non-flat palette '+j['id'])
    palette=np.array([rgba[:3] for count,rgba in colors if rgba[3]>127],dtype=np.uint8)
    ink=mask&np.all(arr[:,:,:3]==INK,axis=2)
    red=mask&np.all(arr[:,:,:3]==CORAL,axis=2)
    accent=red if red.any() else mask&np.all(arr[:,:,:3]==(110,143,94),axis=2)
    labeled,n=ndi.label(accent);patches=[]
    for label,slices in enumerate(ndi.find_objects(labeled),1):
        if slices and (labeled[slices]==label).sum()>100:
            patches.append({'area_source_px':int((labeled[slices]==label).sum()),'bbox_source_px':[slices[1].start,slices[0].start,slices[1].stop,slices[0].stop],'bbox_min_edge_dp20':round(min(slices[0].stop-slices[0].start,slices[1].stop-slices[1].start)/62.7,3)})
    patches.sort(key=lambda p:-p['area_source_px'])
    boundary=mask&~ndi.binary_erosion(mask)
    exterior=~ndi.binary_fill_holes(mask)
    outer=boundary&ndi.binary_dilation(exterior)
    outer_ink=float(ink[outer].mean()) if outer.any() else 0
    # A local medial-ridge estimate detects likely underweight lines; not a proof of minimum width.
    estimate=strokes(ink);flags=[]
    if estimate and estimate['p10']<1.75:flags.append('ink_ridge_p10_below_1.75dp_review_required')
    if not patches:flags.append('accent_missing')
    elif patches[0]['bbox_min_edge_dp20']<3:flags.append('largest_accent_bbox_min_edge_below_3dp')
    if j['style']=='C' and outer_ink<.95:flags.append('cream_or_accent_exposed_on_outer_boundary')
    arrow=None
    if j['id']=='GoldBasin' and red.any():
        # Measure the dominant coral component through its central shaft, not the arrowhead.
        ids,counts=np.unique(labeled[red],return_counts=True);idx=int(ids[counts.argmax()]);ys,xs=np.where(labeled==idx)
        y0,y1=int(ys.min()),int(ys.max());widths=[]
        for y in range(y0+int((y1-y0)*.2),y0+int((y1-y0)*.6)+1):
            xx=np.where(labeled[y]==idx)[0]
            if len(xx):widths.append(int(xx.max()-xx.min()+1))
        if widths:arrow=round(float(np.percentile(widths,10))/62.7,3)
        if arrow is None or arrow<3:flags.append('gold_basin_arrow_shaft_below_3dp')
        component,ncomp=ndi.label(mask)
        connected=np.unique(component[red]);connected=connected[connected>0]
        if any((component==label).sum()>mask.sum()*.7 for label in connected):flags.append('gold_basin_arrow_gap_not_clear')
    bgcolors=[{'rgb':[int(x) for x in rgb],'contrast_on_warm_white':round(contrast(rgb),3),'role':'accent_exception_accepted' if tuple(rgb)==CORAL else 'internal_cream' if tuple(rgb)==CREAM else 'accent' if tuple(rgb)==(110,143,94) else 'main'} for rgb in palette]
    meta=json.loads((folder/'metadata.json').read_text())
    meta.update(style=j['style'],label=j['label'],occupied_canvas_fraction=round(float(mask.mean()),4),ink_ridge_width_dp20_estimate=estimate,ink_ridge_width_dp24_estimate={k:round(v*1.2,3) for k,v in estimate.items()} if estimate else None,accent_components=patches,outer_ink_fraction=round(outer_ink,4),gold_basin_arrow_shaft_dp20_estimate=arrow,color_contrast=bgcolors,qc_flags=flags,min_line_width_compliance='requires_shape_specific_review; ridge quantiles are diagnostic, not certified minima',status='candidate')
    previews=folder/'previews';previews.mkdir(exist_ok=True)
    for size in (20,24,32,48,64,80,96):im.resize((size,size),Image.Resampling.LANCZOS).save(previews/f'{size}px.png')
    meta['preview_notes']='80px=20dp@xxxhdpi;96px=24dp@xxxhdpi. Antialiased derived previews may contain blend colors; source icon.png has <=3 solid colors.'
    (folder/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    return meta

CSS='''*{box-sizing:border-box}body{margin:0;padding:32px;width:1500px;background:#f5f3eb;color:#2e3a2f;font-family:"Noto Sans CJK TC",sans-serif}h1{font-size:32px;margin:0 0 12px}h2{font-size:24px;margin:24px 0 14px}p{font-size:17px;line-height:1.6}a{color:#4a6650}.note{background:#fff1db;padding:14px 20px;border-radius:14px}.scene{background:#64b34a url('../floatbar-review-v1/simulated-game-background.png') center/cover;border-radius:22px;padding:20px;margin:16px 0;overflow:hidden}.phone{display:inline-block;padding:12px;background:rgba(255,255,255,.08)}.bar{display:flex;align-items:start;gap:8px;padding:12px 0}.cell{display:flex;flex-direction:column;align-items:center;width:40px;flex:none;gap:3px}.circle{width:40px;height:40px;border-radius:50%;background:#fffcf6;display:flex;align-items:center;justify-content:center}.circle img{width:20px;height:20px;object-fit:contain}.s24 img{width:24px;height:24px}.pill{font-size:8px;line-height:13px;max-width:52px;white-space:nowrap;background:#2e3a2f;color:#fffcf6;border-radius:9px;padding:0 5px}.scene-title{display:inline-block;background:#2e3a2f;color:#fffcf6;font-size:13px;padding:4px 10px;border-radius:8px}.zoom{transform:scale(2);transform-origin:top left;width:700px;height:180px}.zoom-frame{height:370px}.details{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{background:#fffcf6;border:1px solid #d6dfd2;border-radius:16px;padding:14px}.card h3{margin:4px 0 10px;font-size:18px}.hero{display:block;width:104px;height:104px;object-fit:contain;margin:8px auto}.samples{display:flex;align-items:end;gap:10px;justify-content:center;min-height:90px}.samples>span{display:flex;flex-direction:column;align-items:center;font-size:11px}.compare{display:flex;justify-content:center;gap:16px;margin:12px 0}.compare>div{text-align:center;font-size:12px}.compare .circle{margin:0 auto}.flags{font-size:11px;color:#8d3c2c;word-break:break-word;min-height:35px}.meta{font-size:12px;color:#596658}.overview .scene{background-image:url('simulated-game-background.png')}.overview .styles{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.overview .stylepanel{background:#fffcf6;border-radius:20px;padding:16px}.overview .stylepanel .scene{padding:8px}.overview .stylepanel .bar{gap:5px}.swatch{display:inline-block;width:16px;height:16px;vertical-align:middle;border:1px solid #2e3a2f}.control-note{font-size:12px}'''
TITLES={'A':'A 粗線雙色','B':'B 實心剪影','C':'C 圓角貼紙'}
MAIN=['HideFloat','GoldBasin','Ticket','Dispatch','Feed','LightSpeed','ReturnToApp','Close','FloatMenu']
CONTROL=['Play','Pause','SkipBack','SkipForward','Stop','GameReturn','Check']
def icon_path(style,id,overview=False):return f'../floatbar-{style}-v1/{id}/icon.png' if overview else f'{id}/icon.png'
def bar(style,ids,size=20,baseline=False,overview=False):
    lookup={j['id']:j for j in JOBS if j['style']==style};s='<div class="bar">'
    for id in ids:
        src=f'../floatbar-review-v1/phosphor-reference/{id}.svg' if baseline else icon_path(style,id,overview)
        label=lookup[id]['label'];s+=f'<div class="cell"><span class="circle {"s24" if size==24 else ""}"><img src="{src}" alt="{id}"></span><span class="pill">{label}</span></div>'
    return s+'</div>'
def page_header(title,overview=False):return '<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+title+'</title><style>'+CSS+'</style><body class="'+('overview' if overview else '')+'"><h1>'+title+'</h1>'
def build():
    records=[]
    for j in JOBS:
        if (CAND/f'floatbar-{j["style"]}-v1'/j['id']/'metadata.json').exists():records.append(inspect(j))
    if len(records)!=48:raise RuntimeError(f'Need48 candidates, found{len(records)}')
    allqc={'status':'candidate','count':48,'palette_exception':'Brand Coral #F36C63 has2.874:1 on#FFFCF6, retained by explicit user choice. Ink boundaries must still be visually checked.','dp_mapping':'CSS px represents layout dp, device/browser density is not a physical dp measurement.80px and96px derived previews correspond to xxxhdpi.','measurement_limit':'Line-width medial-ridge percentiles are screening diagnostics, not guaranteed shape-specific minimum measurements. Tapered tips/junctions and optical size require visual review.','records':records}
    (HERE/'validation.json').write_text(json.dumps(allqc,ensure_ascii=False,indent=2)+'\n')
    for style in 'ABC':
        subset=[r for r in records if r['style']==style];lookup={r['id']:r for r in subset}
        s=page_header(TITLES[style]+' · 懸浮功能列候選')
        s+='<p class="note">全套 16 張均為 candidate，未核准。背景為 image_gen 模擬遊戲場景，尚未取得附件1／2。每格40dp暖白圓、圖示20dp／24dp、深色膠囊標籤。珊瑚紅純色對比2.87:1為使用者接受的例外；其餘品質旗標見各卡與 validation.json。</p>'
        s+='<h2>遊戲背景 · 40dp圓／20dp圖示 · 原比例</h2><div class="scene native-scene"><span class="scene-title">模擬遊戲場景｜20dp</span><div class="phone">'+bar(style,MAIN)+bar(style,CONTROL)+'</div></div>'
        s+='<h2>同背景 · 24dp圖示</h2><div class="scene"><span class="scene-title">模擬遊戲場景｜24dp</span><div class="phone">'+bar(style,MAIN,24)+bar(style,CONTROL,24)+'</div></div>'
        s+='<h2>20dp配置放大2倍，方便比較形狀</h2><div class="scene zoom-frame"><div class="zoom">'+bar(style,MAIN)+bar(style,CONTROL)+'</div></div>'
        s+='<h2>Phosphor Bold 單色語意對照 · 同一場景／20dp</h2><p>官方2.1.1 Bold參考，未讀App資源，故不宣稱與目前App逐像素一致；GoldBasin對照暫用定位準星。</p><div class="scene">'+bar(style,MAIN,baseline=True)+bar(style,CONTROL,baseline=True)+'</div>'
        s+='<h2>獨立原圖、32／48／64px、20／24dp 與逐一對照</h2><div class="details">'
        for j in [j for j in JOBS if j['style']==style]:
            r=lookup[j['id']];id=j['id'];flags=', '.join(r['qc_flags']) or '幾何篩檢未發現旗標；不是人工核准'
            s+=f'<article class="card"><h3>{html.escape(j["label"])} · {id}</h3><div class="meta">candidate｜1254×1254 RGBA</div><img class="hero" src="{id}/icon.png" alt="{id}"><div class="samples">'
            for n in (32,48,64):s+=f'<span><img src="{id}/previews/{n}px.png" width="{n}" height="{n}" alt="{n}px">{n}px</span>'
            s+='</div><div class="compare"><div><span class="circle"><img src="../floatbar-review-v1/phosphor-reference/'+id+'.svg" alt="Phosphor '+id+'"></span>Phosphor20dp</div><div><span class="circle"><img src="'+id+'/previews/80px.png" alt="20dp"></span>候選20dp</div><div><span class="circle s24"><img src="'+id+'/previews/96px.png" alt="24dp"></span>候選24dp</div></div>'
            s+=f'<div class="flags">{html.escape(flags)}</div><div class="meta">Ink寬度p10估值：{r["ink_ridge_width_dp20_estimate"]["p10"] if r["ink_ridge_width_dp20_estimate"] else "—"}dp<br><a href="{id}/PROMPT.json">提示詞</a> · <a href="{id}/metadata.json">尺寸／alpha／hash／檢查</a></div></article>'
        s+='</div><p>來源 PNG 是限色原稿；80／96px 為抗鋸齒顯示預覽。未修改App、catalog、active_reference或既有核准檔。<a href="../floatbar-review-v1/index.html">三方向總覽</a></p></body></html>'
        (CAND/f'floatbar-{style}-v1/index.html').write_text(s)
        (CAND/f'floatbar-{style}-v1/validation.json').write_text(json.dumps({'status':'candidate','records':subset},ensure_ascii=False,indent=2)+'\n')
    s=page_header('懸浮功能列 · A／B／C 三方向比較',True)
    s+='<p class="note">48張獨立 image_gen 候選（每方向9項主功能＋7項控制）。只產候選，不改App或既有目錄。背景為模擬場景，非附件實機圖。保留品牌珊瑚紅；純紅2.87:1為已接受例外。各方向仍有需修正的幾何旗標，請一併查看完整檢閱與數值。</p><div class="styles">'
    for style in 'ABC':
        s+=f'<section class="stylepanel"><h2>{TITLES[style]}</h2><p><a href="../floatbar-{style}-v1/index.html">完整檢閱</a> · <a href="../floatbar-{style}-v1/review.png">完整PNG</a></p><div class="scene"><span class="scene-title">40dp圓／20dp圖示</span>'+bar(style,MAIN,overview=True)+bar(style,CONTROL,overview=True)+'</div><div class="scene"><span class="scene-title">40dp圓／24dp圖示</span>'+bar(style,MAIN,24,overview=True)+bar(style,CONTROL,24,overview=True)+'</div><div class="details" style="grid-template-columns:repeat(4,1fr)">'
        for j in [j for j in JOBS if j['style']==style]:s+=f'<div style="text-align:center;font-size:12px"><img src="{icon_path(style,j["id"],True)}" width="64" height="64" alt="{j["id"]}"><br>{j["label"]}</div>'
        s+='</div></section>'
    s+='</div><p>控制項：Play、Pause、SkipBack、SkipForward、Stop、GameReturn、Check。GoldBasin三款均以v6形狀作參考，只重繪風格，沒有手。<a href="validation.json">完整品質篩檢</a> · <a href="SOURCE-NOTES.json">來源與限制</a></p></body></html>'
    (HERE/'index.html').write_text(s)
    print(f'Built3 direction reviews and overview for{len(records)} candidates.')
if __name__=='__main__':build()
