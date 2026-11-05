"""Render original current assets into a single README contact sheet."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'brand/reviews/overview'
def src(path):return '/'+path
c=json.loads((ROOT/'brand/catalog.json').read_text());b=json.loads((ROOT/'brand/ui/v0.7-botanical/catalog.json').read_text())
assets=[a for a in c['assets'] if a.get('active_reference')];assets.sort(key=lambda a:0 if a['version']=='v0.5' else 1)
a={i['id']:i for i in b['icons']}
s='''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0;width:2400px;padding:65px;background:#f6f2e9;color:#374d3d;font-family:"Noto Sans CJK TC",sans-serif}h1{font-size:61px;margin:0 0 15px}h2{font-size:38px;margin:36px 0 18px}p{font-size:25px;line-height:1.6}.grid{display:grid;grid-template-columns:repeat(7,1fr);gap:17px}.card{border:1px solid #deded0;background:#fffdf8;border-radius:20px;padding:18px 12px;text-align:center}.brand{width:244px;height:244px;object-fit:contain}.name{font-size:26px;font-weight:700}.id{font-size:16px;color:#72806d;margin-top:5px}.pair{display:flex;justify-content:center;gap:14px;margin:16px 0}.sample{display:inline-flex;width:112px;height:112px;align-items:center;justify-content:center;position:relative;border:2px solid transparent;border-radius:19px}.sample img{width:96px;height:96px;object-fit:contain}.selected{background:#fff1db;border-color:#55735b}.selected:after{content:"";position:absolute;bottom:3px;width:6px;height:6px;border-radius:50%;background:#55735b}.state{font-size:16px;color:#72806d}.status{font-size:18px;color:#a16b20}.approved .status{color:#55735b}</style><h1>蘑菇偵察 · 全系列圖示總覽</h1><p>21 張蘑菇／植物／平台品牌 ＋ 57 項 B 植物線條功能用途 ＋ 1 個地圖入口 ＋ 16 張浮列專用已核准圖示<br>品牌、首批 6 張功能原圖與拉金盆向下滑動箭頭已核准；5 種元素特效已核准；49 張功能延伸新稿待審核（前稿僅留追溯）。2026-11-05；GoldBasin 最新採 D 蘑菇插圖版</p><h2>01　蘑菇、植物與平台品牌 · 已核准</h2><div class="grid">'''
for i in assets:s+=f'<div class="card"><img class="brand" src="{src(i["path"])}" alt="{html.escape(i["id"])}"><div class="name">{html.escape(i.get("label",i["id"]))}</div><div class="id">{i["id"]}</div></div>'
s+='</div><h2>02　App 功能圖示 · B 植物線條</h2><p>每格左：一般；右：選取。兩態共用原圖，選取另加奶油底、綠色外框與底部圓點。</p>'
rows=[]
for item in b['semantics']:
 if item.get('candidate_options'):
  for option in item['candidate_options']:rows.append(dict(item,id=('GoldBasin' if option.startswith('gold-planter-') else 'GoldBasin-'+('盆形'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-form-') else 'A'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-minimal-') else option[-1].upper())),label=('拉金盆' if option.startswith('gold-planter-') else '拉金盆 '+('盆形'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-form-') else 'A'+'123'['abc'.index(option[-1])] if option.startswith('gold-basin-minimal-') else option[-1].upper())),asset_id=option))
 else:rows.append(item)
rows+=[{'id':'Map','label':'地圖入口','group':'額外品牌入口','asset_id':'map','status':'approved','usage_status':'brand-entry'}]
for group in dict.fromkeys(i['group'] for i in rows):
 s+=f'<h2 style="font-size:29px">{html.escape(group)}</h2><div class="grid">'
 for i in rows:
  if i['group']!=group:continue
  source=src(a[i['asset_id']]['path']);status='已核准' if i['status']=='approved' else '新稿待審核';usage={'placeholder':' · 功能占位','reserved-unreferenced':' · 保留用途'}.get(i['usage_status'],'')
  s+=f'<div class="card {i["status"]}"><div class="name">{html.escape(i["label"])}</div><div class="pair"><span class="sample"><img src="{source}" alt="一般"></span><span class="sample selected"><img src="{source}" alt="選取"></span></div><div class="state">一般 ／ 選取</div><div class="id">{i["id"]}</div><div class="status">{status}{usage}</div></div>'
 s+='</div>'
orbit_file=ROOT/'brand/effects/v0.9-orbit-bold/catalog.json'
if orbit_file.exists():
 orbit=json.loads(orbit_file.read_text())
 s+='<h2>03　元素菇 · B 環繞流動強化版（已核准）</h2><p>原始 v0.5 蘑菇＋獨立透明特效層，以下為瀏覽器合成預覽。原稿未重畫或覆蓋；本輪為靜態視覺特效。</p><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:18px">'
 for effect in orbit['assets']:
  s+=f'<div class="card"><div class="name">{effect["label"]}</div><img src="/{effect["composite_preview"]}" style="width:340px;height:340px;object-fit:contain" alt="{effect["label"]}環繞特效"><div class="status" style="color:#55735b">已核准</div></div>'
 s+='</div>'
new_floatbar=ROOT/'brand/ui/illustrated-v1/approved/batch2-floatbar/manifest.json'
float_current=ROOT/'brand/ui/illustrated-v1/approved/batch2-floatbar/current-manifest.json'
if float_current.exists():new_floatbar=float_current
floatbar_manifest=new_floatbar if new_floatbar.exists() else ROOT/'brand/ui/v0.7-botanical/approved/floatbar-C-v2/manifest.json'
if floatbar_manifest.exists():
 floatbar=json.loads(floatbar_manifest.read_text())
 if new_floatbar.exists():
  s+='<h2>04　懸浮列插圖 · 12張新核准＋D金盆（尚缺3項）</h2><p>HideFloat已選睜眼＋斜線A；Feed、ReturnToApp、GameReturn仍待改稿核准。未與舊C-v2混搭；以下只列已核准來源，不代表全套已完成替換。</p><div class="grid">'
  icons=[dict(floatbar['existing_approved_reference'],label='拉金盆')]+floatbar['assets']
 else:
  s+='<h2>04　歷史遊戲懸浮功能列 · C-v2</h2><div class="grid">'
  icons=floatbar['assets']
 for icon in icons:
  image=src(icon['path'])
  s+=f'<div class="card approved"><div class="name">{html.escape(icon["label"])}</div><div class="pair"><span class="sample"><img src="{image}" alt="一般"></span><span class="sample selected"><img src="{image}" alt="選取示意"></span></div><div class="id">{icon["id"]}</div><div class="status">已核准 · 浮列專用</div></div>'
 s+='</div>'
illustrated_file=ROOT/'brand/ui/illustrated-v1/approved/batch1/manifest.json'
current_file=ROOT/'brand/ui/illustrated-v1/approved/current-manifest.json'
if current_file.exists():illustrated_file=current_file
if illustrated_file.exists():
 illustrated=json.loads(illustrated_file.read_text())
 s+='<h2>05　插圖風功能圖示 · 第一批5張已核准</h2><p>Auto現採C循環果實v2；Tasks A、Records A、Favorites B、Scan A。GoldBasin沿用D；未修改App。一般／選取只表示容器狀態示意。未選候選不列入此正式交接總覽。</p><div class="grid">'
 for icon in illustrated['assets']:
  image=src(icon['path'])
  s+=f'<div class="card approved"><div class="name">{html.escape(icon["label"])} {icon["concept"]}</div><div class="pair"><span class="sample"><img src="{image}" alt="一般示意"></span><span class="sample selected"><img src="{image}" alt="選取示意"></span></div><div class="id">{icon["id"]} · {html.escape(icon["title"])}</div><div class="status">已核准 · 插圖版</div></div>'
 s+='</div>'
map_extra=ROOT/'brand/ui/illustrated-v1/approved/batch3-map/manifest.json'
map_current=ROOT/'brand/ui/illustrated-v1/approved/batch3-map/current-manifest.json'
if map_current.exists():map_extra=map_current
if map_extra.exists():
 batch=json.loads(map_extra.read_text())
 s+='<h2>06　地圖其他圓鈕 · 7項全部已核准</h2><p>Collapse/Expand B綠色雙尖括號、Layers B剖面地塊；Locate B、Teleport A、Settings A、More A沿用核准。40dp圓／32dp插圖，未修改App。</p><div class="grid">'
 for item in batch['assets']:
  image=src(item['path'])
  s+=f'<div class="card approved"><div class="name">{html.escape(item["label"])} {item["concept"]}</div><div class="pair"><span class="sample"><img src="{image}" alt="一般示意"></span><span class="sample selected"><img src="{image}" alt="選取示意"></span></div><div class="id">{item["id"]}</div><div class="status">已核准 · 地圖32dp</div></div>'
 s+='</div>'
s+='<p>直接排列原始 PNG，供整體檢閱，非正式輸出尺寸。深色介面採奶油承托底。舊 v0.6 Phosphor 包保留供追溯，已不列入目前總覽。</p></html>'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'all-icons-overview.html').write_text(s)
print('Built current brand + complete Botanical Line overview.')
