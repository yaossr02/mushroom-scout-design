"""Build review pages from original PNGs, without mutating or redrawing icons."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'brand/ui/v0.7-botanical'
STYLE='''*{box-sizing:border-box}body{margin:0;padding:50px;background:#f6f2e9;color:#374d3d;font-family:"Noto Sans CJK TC",sans-serif;width:2100px}h1{font-size:51px;margin:0 0 14px}h2{font-size:34px;margin:34px 0 18px}p{font-size:23px;line-height:1.6;margin:10px 0 24px}.grid{display:grid;grid-template-columns:repeat(7,1fr);gap:16px}.card{background:#fffdf8;border:1px solid #d9dfcf;border-radius:20px;padding:18px 12px;text-align:center}.name{font-size:25px;font-weight:700}.id{font-size:16px;color:#6b796c;margin:6px 0}.hero{width:154px;height:154px;object-fit:contain;display:block;margin:8px auto}.states{display:flex;justify-content:center;gap:14px;margin:14px 0 6px}.sample,button{display:inline-flex;position:relative;align-items:center;justify-content:center;border:2px solid transparent;border-radius:17px;background:transparent;width:76px;height:76px}button{cursor:pointer}button img,.sample img{width:60px;height:60px;object-fit:contain}.selected{border-color:#55735b;background:#fff1db}.selected:after{content:"";position:absolute;bottom:3px;left:34px;width:5px;height:5px;background:#55735b;border-radius:50%}.status{font-size:16px;color:#a16b20}.approved .status{color:#55735b}.sizes{display:flex;justify-content:center;align-items:end;gap:16px;margin-top:15px}.sizes img{object-fit:contain;display:block}.sizes span{font-size:14px}.dark{background:#263a30;color:#fff1db}.dark .sample{background:#fff1db}.checker{background:repeating-conic-gradient(#ecece5 0% 25%,#fffdf8 0% 50%) 0/16px 16px!important}.hint{font-size:17px}.map{background:#e6ebd9;padding:22px;border:2px dashed #9eb673;border-radius:20px}#search{font:inherit;font-size:22px;padding:14px;border:1px solid #9eb673;border-radius:12px;width:500px}body.capture #search{display:none}.hidden{display:none}.asset-path{font-size:14px}'''
def source(path):return '/'+path
def items(c):
 a={i['id']:i for i in c['icons']}
 result=[]
 for s in c['semantics']:
  if s.get('candidate_options'):
   for option in s['candidate_options']:
    result.append(dict(s,id=('GoldBasin' if option.startswith('gold-planter-') else 'GoldBasin-'+('盆形'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-form-') else 'A'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-minimal-') else option[-1].upper())),label=('拉金盆' if option.startswith('gold-planter-') else '拉金盆 '+('盆形'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-form-') else 'A'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-minimal-') else option[-1].upper())),asset_id=option,asset=a[option]))
  else:result.append(dict(s,asset=a[s['asset_id']]))
 result.append({'id':'Map','label':'地圖入口','group':'額外品牌入口','status':'approved','asset_id':'map','asset':a['map'],'usage_status':'brand-entry'})
 return result
def card(i):
 a=i['asset'];src=source(a['path']);status='已核准' if i['status']=='approved' else '新稿待審核';usage={'placeholder':' · 功能占位','reserved-unreferenced':' · 保留未啟用'}.get(i['usage_status'],'')
 return f'''<article class="card {i['status']}" data-search="{html.escape(i['id']+' '+i['label'])}"><div class="name">{html.escape(i['label'])}</div><div class="id">{i['id']}</div><img class="hero" src="{src}" alt="{html.escape(i['label'])}"><div class="states"><span class="sample"><img src="{src}" alt="一般"></span><button class="selected" aria-pressed="true" aria-label="切換{i['label']}選取"><img src="{src}" alt=""></button></div><div class="hint">一般 ／ 選取</div><div class="status">{status}{usage}</div></article>'''
def main():
 c=json.loads((PACK/'catalog.json').read_text());rows=items(c)
 s='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>B 植物線條完整功能圖示</title><style>'+STYLE+'</style><h1>B 植物線條 · 完整功能圖示</h1><p>57 項功能用途 ＋ 1 個地圖品牌入口｜拉金盆：遊戲圓腹金盆＋向下滑動箭頭<br>首批 6 張與拉金盆下滑箭頭已核准；其餘 49 張延伸圖待審核；舊金盆稿僅保留追溯。原始 PNG 直接排列，一般／選取共用原圖。</p><input id="search" aria-label="搜尋圖示" placeholder="搜尋名稱或 ID…">'
 for group in dict.fromkeys(i['group'] for i in rows):
  s+=f'<section><h2>{group}</h2><div class="grid">'+''.join(card(i) for i in rows if i['group']==group)+'</div></section>'
 s+='<h2>32／48／64 px 原圖預覽</h2><p>此處為 CSS 顯示尺寸；原檔規格以 catalog 為準。新增／放大及移除／縮小共用符號。</p><div class="grid">'
 for i in rows:
  src=source(i['asset']['path']);s+=f'<div class="card"><div class="name">{i["label"]}</div><div class="sizes">'+''.join(f'<span><img src="{src}" width="{n}" height="{n}" alt="">{n}px</span>' for n in (32,48,64))+'</div></div>'
 s+='</div><h2>深色與棋盤底檢閱</h2><p>深色介面採奶油承托底，保留植物線條原色；右側棋盤底檢查透明邊緣。選取狀態另有外框與底部圓點。</p><div class="grid">'
 for i in rows:
  src=source(i['asset']['path']);s+=f'<div class="card dark"><div class="name">{i["label"]}</div><span class="sample"><img src="{src}" alt="深色承托"></span><span class="sample checker"><img src="{src}" alt="透明底"></span></div>'
 s+='</div><h2>地圖工具列示意</h2><div class="map"><div style="display:flex;gap:20px">'
 for id in ['Search','Layers','Filter','Locate','Scan']:
  i=next(x for x in rows if x['id']==id);s+=f'<div class="card"><img src="{source(i["asset"]["path"])}" width="48" height="48" alt="{i["label"]}"></div>'
 s+='</div><p>介面擺放示意，非 App 實機驗證。Dispatch 為占位；Info／Rotate 為保留用途。Empty 兩態維持空心，選取只改容器。</p></div><p class="hint">生成 PNG 原圖保留；非 SVG／VectorDrawable。新稿不繼承首批核准。各圖仍可能有線寬、色調與光學大小差異，正式平台輸出另行處理。</p><script>document.querySelectorAll("button").forEach(b=>b.onclick=()=>{const on=b.getAttribute("aria-pressed")!=="true";b.setAttribute("aria-pressed",String(on));b.classList.toggle("selected",on)});document.querySelector("#search").oninput=e=>{const q=e.target.value.toLowerCase();document.querySelectorAll("article").forEach(a=>a.classList.toggle("hidden",!a.dataset.search.toLowerCase().includes(q)))}</script></html>'
 (PACK/'review/index.html').write_text(s)
 print(f'Built {len(rows)} cards, {len(rows)*3} size samples, dark/checker pairs and map toolbar.')
if __name__=='__main__':main()
