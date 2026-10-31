"""Export existing MIT Phosphor vectors and actual app mappings; no new illustration generation."""
import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'brand/ui/v0.6'
parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, required=True, help='Read-only mushroom-scout checkout')
parser.add_argument('--phosphor', type=Path, required=True, help='Extracted @phosphor-icons/core@2.1.1 package')
args = parser.parse_args()
upstream = json.loads((args.phosphor / 'package.json').read_text())
assert upstream['name'] == '@phosphor-icons/core' and upstream['version'] == '2.1.1'
source = args.app / 'android/app/src/main/java/io/github/yaossr02/mushroomscout/ui/AppIcon.kt'
pairs = re.findall(r'^    (\w+)\(R.drawable\.(ph_\w+), R.drawable\.(ph_\w+)\)', source.read_text(), re.M)
assert len(pairs) == 52
groups = {
    '地圖與主要功能': 'Search Layers Filter Settings Crosshair Locate FitAll ZoomIn ZoomOut Auto Tasks Records Scan Teleport Route Reorder List Footprint Timezones Favorite Recent'.split(),
    '操作與導覽': 'Add Remove Undo Rotate Play Pause Stop Copy OpenOutside Share Delete Check Close More SkipForward SkipBack Back Previous Next Expand Collapse'.split(),
    '自動、懸浮與狀態': 'Feed Dispatch Lottery FloatMenu Ticket LightSpeed Backspace ReturnToApp Info Warning Photo Success Error Empty'.split(),
}
labels = dict(zip('Search Layers Filter Settings Crosshair Locate FitAll ZoomIn ZoomOut Auto Tasks Records Scan Feed Dispatch Lottery Teleport Route Reorder List Footprint Timezones Favorite Recent Add Remove Undo Rotate Play Pause Stop Copy OpenOutside Share Delete Check Close More SkipForward SkipBack FloatMenu Ticket LightSpeed Backspace ReturnToApp Back Previous Next Expand Collapse Info Warning Photo Success Error Empty'.split(),
    '搜尋 圖層 篩選 設定 準星 目前位置 顯示全部 放大 縮小 自動 任務 紀錄 掃描 餵果 派遣 抽獎 傳送 路線 拖曳排序 清單 足跡 時區 收藏 最近 新增 移除 復原 旋轉 開始 暫停 停止 複製 外部開啟 分享 刪除 確認 關閉 更多 下一步 上一步 功能選單 票券 光速移動 退格 回到App 返回 上一頁 下一頁 展開 收合 資訊 警告 相簿 成功 錯誤 空狀態'.split()))
extras = [('Photo', 'ph_image', 'ph_image_fill'), ('Success', 'ph_check_circle', 'ph_check_circle_fill'), ('Error', 'ph_warning_circle', 'ph_warning_circle_fill'), ('Empty', 'ph_circle', 'ph_circle')]
all_pairs = pairs + extras
assert len(labels) == len(all_pairs) == 56
assert set(i for group in groups.values() for i in group) == set(i for i, _, _ in all_pairs)
android = args.app / 'android/app/src/main/res/drawable'
ns = '{http://schemas.android.com/apk/res/android}'
glyphs = {}
for res in sorted({r for _, n, s in all_pairs for r in (n, s)}):
    weight = 'fill' if res.endswith('_fill') else 'bold'
    name = res[3:].removesuffix('_fill').replace('_', '-')
    src = args.phosphor / 'assets' / weight / f'{name}-{weight}.svg'
    raw = src.read_text()
    paths = [p.attrib['d'] for p in ET.fromstring(raw).findall('{http://www.w3.org/2000/svg}path')]
    assert paths and not re.search(r'<(circle|rect|line|polyline|polygon|g)\b|opacity|transform|fill-rule', raw), res
    if (android / (res + '.xml')).is_file():
        existing = ET.parse(android / (res + '.xml')).getroot()
        assert [p.attrib[ns + 'pathData'] for p in existing] == paths, f'Upstream/app geometry mismatch: {res}'
        xml = (android / (res + '.xml')).read_text()
    else:
        root = ET.Element('vector', {'xmlns:android': ns[1:-1], 'android:width':'24dp', 'android:height':'24dp', 'android:viewportWidth':'256', 'android:viewportHeight':'256'})
        for d in paths: ET.SubElement(root, 'path', {'android:fillColor':'#FF000000', 'android:pathData':d})
        xml = '<?xml version="1.0" encoding="utf-8"?>\n<!-- Phosphor Icons 2.1.1; MIT; see LICENSE-phosphor.txt -->\n' + ET.tostring(root, encoding='unicode') + '\n'
    glyphs[res] = {'svg':raw, 'xml':xml, 'paths':paths, 'weight':weight, 'name':name}

for directory in ['svg','android/drawable','png/24','png/48','sources','review']:
    (OUT / directory).mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, OUT / 'sources/AppIcon.kt')
shutil.copyfile(args.phosphor / 'LICENSE', OUT / 'LICENSE-phosphor.txt')
assets = []
symbols = []
for res, g in glyphs.items():
    svg = OUT / 'svg' / (res + '.svg')
    xml = OUT / 'android/drawable' / (res + '.xml')
    svg.write_text(g['svg']); xml.write_text(g['xml'])
    assets.append({'id':res,'phosphor_name':g['name'],'weight':g['weight'],'svg':svg.relative_to(OUT).as_posix(),'android':xml.relative_to(OUT).as_posix(),'svg_sha256':hashlib.sha256(svg.read_bytes()).hexdigest(),'android_sha256':hashlib.sha256(xml.read_bytes()).hexdigest()})
    symbols.append(f'<symbol id="{res}" viewBox="0 0 256 256" fill="currentColor">' + ''.join(f'<path d="{d}"/>' for d in g['paths']) + '</symbol>')
(OUT / 'sprite.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(symbols) + '</svg>\n')
usage = {}
for f in sorted((args.app / 'android/app/src/main/java').rglob('*.kt')):
    for line_no, line in enumerate(f.read_text().splitlines(), 1):
        for ident in re.findall(r'AppIcon\.(\w+)', line):
            if ident in labels: usage.setdefault(ident, []).append({'path':f.relative_to(args.app).as_posix(),'line':line_no})
entries = []
for ident, normal, selected in all_pairs:
    supplemental = ident in {x[0] for x in extras}
    state = 'ios-supplement' if supplemental else 'placeholder' if ident == 'Dispatch' else 'referenced' if usage.get(ident) else 'reserved-unreferenced'
    entries.append({'id':ident,'label':labels[ident],'normal':normal,'selected':selected,'has_fill_variant':normal != selected,'group':next(g for g, ids in groups.items() if ident in ids),'usage_status':state,'usage_references':usage.get(ident, []),'source':'iOS semantic gap; proposed Phosphor counterpart' if supplemental else 'Existing Android AppIcon mapping, unchanged'})
commit = subprocess.check_output(['git','-C',str(args.app),'rev-parse','HEAD'],text=True).strip()
catalog = {'version':'v0.6','status':'candidate','kind':'functional-ui-icon-delivery','library':'@phosphor-icons/core','library_version':'2.1.1','license':'MIT','design_origin':'Existing Phosphor geometry; assembled and exported, not newly drawn or AI-generated','source_app_commit':commit,'source_app_enum':'sources/AppIcon.kt','existing_android_semantics':52,'ios_supplemental_semantics':4,'total_semantics':56,'unique_glyphs':len(glyphs),'normal_sizes_dp':[16,18,20],'touch_target_dp':48,'selected_style':'Fill when available; action-only glyphs reuse Bold with selected tint','colors':{'normal':'#513A30','selected':'#55735B','selected_background':'#E1EACB','dark_normal':'#FFF1DB','dark_selected':'#DCE7CB'},'approval_record':None,'icons':entries,'glyphs':assets,'ios_mapping':{'gearshape':'Settings','scope':'Scan','photo':'Photo','square.and.arrow.up':'Share','checkmark.circle.fill':'Success','exclamationmark.circle.fill':'Error','circle':'Empty'},'notes':['Dispatch is referenced by a redesign placeholder, not a working dispatch feature.','Info and Rotate have no literal call sites in current checkout; retained as enum-reserved semantics.','Empty intentionally keeps an outline circle in both states so selection cannot imply non-empty.','Source Android geometry was checked against the pinned upstream package for every existing drawable.','PNG screenshots and SVGs are vector renders, not generated illustration concepts.','Existing botanical v0.5 approval is separate from this functional-icon pack.']}
(OUT / 'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')

def inline(res, size):
    raw=glyphs[res]['svg']
    return raw.replace('<svg ', f'<svg width="{size}" height="{size}" aria-hidden="true" ',1)

sections=[]
for index,(group,ids) in enumerate(groups.items(),1):
    cards=[]
    for ident in ids:
        item=next(e for e in entries if e['id']==ident)
        sizes=''.join(f'<span>{inline(item["normal"],s)}<small>{s}</small></span>' for s in [16,18,20])
        note={'placeholder':'派遣占位','reserved-unreferenced':'保留項目','ios-supplement':'iOS 補齊'}.get(item['usage_status'],'')
        cards.append(f'<article data-search="{ident.lower()} {item["label"]}"><h3>{item["label"]}</h3><code>{ident}</code><div class="states"><span>{inline(item["normal"],24)}<small>一般</small></span><span class="selected">{inline(item["selected"],24)}<small>選取</small></span></div><div class="sizes">{sizes}</div><p class="note">{note or ("Bold／Fill" if item["has_fill_variant"] else "同一圖形")}</p></article>')
    sections.append(f'<section id="board-{index}"><h2>{group} · {len(ids)} 個用途</h2><div class="grid">'+''.join(cards)+'</div></section>')
css='''*{box-sizing:border-box}body{margin:0;background:#fff8ed;color:#513a30;font:16px system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:24px}header,section{background:#fffdf8;border:1px solid #e5dacc;border-radius:22px;padding:24px;margin:0 0 24px}h1{font-size:30px}h2{font-size:24px;margin-top:0}h3{font-size:16px;margin:0 0 5px}.grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:12px}article{padding:14px;border:1px solid #e5dacc;border-radius:16px;background:#fff}code{font-size:11px;display:block;overflow-wrap:anywhere;color:#7d6f60}.states{display:flex;justify-content:space-around;align-items:center;margin:12px 0}.states span{padding:8px;border-radius:12px;text-align:center}.selected{color:#55735b;background:#e1eacb}small{display:block;font-size:10px;margin-top:5px}.sizes{display:flex;justify-content:space-around;align-items:end}.sizes>span{display:flex;flex-direction:column;align-items:center}.note{font-size:11px;margin:10px 0 0;color:#7d6f60}.controls{display:flex;gap:12px;flex-wrap:wrap}button,input{font:inherit;padding:8px 14px;border:1px solid #cabbac;border-radius:16px;background:white;color:#513a30}p{line-height:1.7}.dark{background:#172c25;color:#fff1db}.dark header,.dark section{background:#243d35;border-color:#657e4f}.dark article{background:#29443a;border-color:#657e4f}.dark .selected{color:#dce7cb;background:#355640}.dark code,.dark .note{color:#c4ceb4}article[hidden]{display:none}@media(max-width:1000px){.grid{grid-template-columns:repeat(4,minmax(0,1fr))}}@media(max-width:600px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}'''
page='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>App 功能圖示 v0.6</title><style>'+css+'</style><main><header><h1>App 功能圖示 · v0.6</h1><p>52 個 Android 用途＋4 個 iOS 補齊用途，採既定 Phosphor Bold／Fill。這批是現有向量的完整交付與配色規格，非新繪或 AI 生成。可與非擬人化 v0.5 蘑菇／品牌素材搭配。</p><p>每格顯示一般／選取及 16／18／20 CSS px 原圖。動作型圖示不另外發明 Fill；點擊區至少 48dp，不等同圖示尺寸。整批配色與補齊映射待確認。</p><div class="controls"><button id="theme">切換淺／深色</button><input id="search" type="search" placeholder="搜尋用途或 ID" aria-label="搜尋圖示"></div></header>'+''.join(sections)+'<footer><p>Phosphor Icons 2.1.1 · MIT。保留原始授權。用途與使用狀態以 catalog.json 為準；沒有修改 App repo。</p></footer></main><script>document.querySelector("#theme").onclick=()=>document.body.classList.toggle("dark");document.querySelector("#search").oninput=e=>{let q=e.target.value.toLowerCase();document.querySelectorAll("article").forEach(a=>a.hidden=!a.dataset.search.includes(q))}</script></html>'
(OUT / 'review/index.html').write_text(page)
(OUT / 'review/glyph-render.html').write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:transparent}#glyph{width:48px;height:48px;color:black}svg{display:block;width:100%;height:100%}</style><div id="glyph"></div>')
print(f'Exported {len(entries)} semantics, {len(glyphs)} unique SVG/Android vectors; geometry matches source App.')
