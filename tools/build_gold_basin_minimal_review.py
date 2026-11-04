"""Record and display original pull-basin candidates without modifying image pixels."""
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'brand/ui/v0.7-botanical'
OUT = PACK / 'candidates/gold-basin-minimal-v3'
prompts = json.loads((OUT / 'PROMPTS.json').read_text())
catalog = json.loads((PACK / 'catalog.json').read_text())
if any(i['id']=='gold-planter-swipe-down-v6' and i['status']=='approved' for i in catalog['icons']):
    raise SystemExit('Historical revision helper: current v6 is approved; do not overwrite its catalog.')
assets = []
for variant in prompts['variants']:
    letter = variant['id'].lower()
    path = OUT / f'{letter}.png'
    with Image.open(path) as im:
        assert im.mode == 'RGBA'
        alpha = im.getchannel('A')
        assert alpha.getextrema() == (0, 255)
        assets.append(dict(id=f'gold-basin-minimal-{letter}', label=variant['label'], status='candidate', active_reference=True,
            path=str(path.relative_to(ROOT)), dimensions_px=list(im.size), mode=im.mode,
            alpha_range=list(alpha.getextrema()), alpha_nonzero_bbox=list(alpha.getbbox()),
            body_bbox_alpha128=list(alpha.point(lambda x: 255 if x >= 128 else 0).getbbox()),
            sha256=hashlib.sha256(path.read_bytes()).hexdigest(), date=prompts['date'], tool='image_gen',
            prompt_file=str((OUT / 'PROMPTS.json').relative_to(ROOT)), generated_original=variant.get('generated_original'), vector=False,
            selected_state='same original PNG plus cream backing, sage border and bottom dot'))
for previous in catalog['icons']:
    if previous['id'].startswith('gold-basin-pull-'):
        previous.update(active_reference=False, review_status='superseded-by-minimal-refinements')
        if previous['id']=='gold-basin-pull-a': previous['selected_for_refinement']=True
catalog['icons'] = [i for i in catalog['icons'] if not i['id'].startswith('gold-basin-minimal-')] + assets
old = next(i for i in catalog['icons'] if i['id'] == 'gold-basin')
old.update(status='rejected', active_reference=False, rejection_reason='User requested stronger pulling action and three alternatives, 2026-11-04')
for semantic in catalog['semantics']:
    if semantic['id'] == 'GoldBasin':
        semantic.update(candidate_options=[a['id'] for a in assets], selection_pending=True,
            status='candidate', note='User selected A upward-pull direction for refinement; A1/A2/A3 are new unapproved candidates. No App change.', selected_direction='gold-basin-pull-a')
catalog.update(source_count=len(catalog['icons']), active_source_count=58, approved_original_count=6,
    new_candidate_original_count=52, rejected_original_count=1, historical_candidate_original_count=3)
(PACK / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
(OUT / 'catalog.json').write_text(json.dumps(dict(status='candidate', selection_pending=True, assets=assets), ensure_ascii=False, indent=2) + '\n')
s = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>拉金盆 · A 方向 · 三款精簡提案</title><style>
*{box-sizing:border-box}body{margin:0;padding:40px;width:1500px;background:#f6f2e9;color:#374d3d;font-family:sans-serif}h1{font-size:36px}p{font-size:20px;line-height:1.5}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}article{padding:22px;border-radius:24px;background:#fffdf8;border:1px solid #d9dfcf;text-align:center}h2{font-size:28px}.hero{width:310px;height:310px;object-fit:contain}.sample{display:inline-flex;align-items:center;justify-content:center;width:80px;height:80px;border-radius:18px}.sample img{width:64px;height:64px;object-fit:contain}.selected{background:#fff1db;border:2px solid #55735b}.sizes{display:flex;align-items:end;justify-content:center;gap:24px;margin:24px 0}.sizes img{display:block;object-fit:contain}.dark{background:#263a30;padding:12px;border-radius:16px}.dark img{background:#fff1db;border-radius:12px}.checker{background:repeating-conic-gradient(#ddd 0% 25%,white 0% 50%) 0/12px 12px;border-radius:12px}.status{color:#a16b20}</style><h1>拉金盆 · A 方向 · 三款精簡提案</h1><p>比較示意：直接引用獨立透明原圖，沒有重畫或裁切。A1／A2／A3 均為全新待審核候選。沿用選定的向上拉拔方向；舊稿僅供追溯。<br>大圖供方向比較；下方 32／48／64 CSS px 才是小尺寸檢閱。未匯入 App。</p><div class="grid">'''
descriptions = ['短珊瑚箭頭搭配淺盆，暖黃縮至盆緣。', '箭頭融入盆形，以留白降低色塊重量。', '上提箭頭移至右盆緣，試驗輪廓整合。']
for a, description in zip(assets, descriptions):
    letter = 'A'+str('abc'.index(a['id'][-1])+1)
    src = '/' + a['path']
    s += f'<article><h2>{letter}　{a["label"]}</h2><img class="hero" src="{src}" alt="{a["label"]}"><p>{description}</p><div class="status">candidate · 待審核</div><p><span class="sample"><img src="{src}" alt="一般"></span><span class="sample selected"><img src="{src}" alt="選取"></span></p><div class="sizes">'
    for n in (32, 48, 64):
        s += f'<span><img src="{src}" width="{n}" height="{n}" alt="{n}px">{n}px</span>'
    s += f'</div><div class="dark"><span class="sample"><img src="{src}" alt="深色承托底"></span><span class="sample checker"><img src="{src}" alt="棋盤底"></span></div></article>'
s += '</div><h2>放回同一組既有圖示比較 · 每張 48 px</h2><div class="grid">'
for a in assets:
    s += '<div class="context" style="display:grid;grid-template-columns:repeat(7,1fr);gap:8px;background:#fffdf8;padding:16px;border-radius:16px">'
    for ident in ['search','scan','favorite',a['id'],'settings','lottery','ticket']:
        item = next(i for i in catalog['icons'] if i['id']==ident)
        s += f'<div style="text-align:center;font-size:12px"><img src="/{item["path"]}" width="48" height="48" style="object-fit:contain" alt="{item["label"]}"><br>{item["label"]}</div>'
    s += '</div>'
s += '</div><p>懸浮選單／地圖工具列示意（非 App 實機）：'
for a in assets:
    s += f'<span class="sample selected"><img src="/{a["path"]}" alt="{a["label"]}"></span> '
s += '</p></html>'
# Align visible bounds only in browser layout; immutable PNG originals keep their pixels.
import re
by_path = {i['path']: i for i in catalog['icons']}
def align(match):
    tag = match.group(0)
    path_match = re.search(r'src="/([^"]+)"', tag)
    if not path_match or path_match.group(1) not in by_path: return tag
    item = by_path[path_match.group(1)]
    box = item['body_bbox_alpha128']
    width, height = item['dimensions_px']
    size_match = re.search(r'width="(\d+)"', tag)
    n = 310 if 'class="hero"' in tag else int(size_match.group(1)) if size_match else 64
    scale = .78 * n / max(box[2]-box[0], box[3]-box[1])
    left = n/2 - (box[0]+box[2])/2*scale
    top = n/2 - (box[1]+box[3])/2*scale
    tag = re.sub(r' style="[^"]*"', '', tag)
    tag = tag.replace('class="hero"', '')
    tag = tag[:-1] + f' style="position:absolute;max-width:none;width:{width*scale}px;height:{height*scale}px;left:{left}px;top:{top}px;object-fit:contain;background:transparent;border-radius:0">'
    return f'<span style="position:relative;display:inline-block;overflow:hidden;width:{n}px;height:{n}px;vertical-align:middle">{tag}</span>'
s = re.sub(r'<img\b[^>]*>', align, s)
s = s.replace('</style>', '.dark .sample{background:#fff1db}.dark .checker{background:repeating-conic-gradient(#ddd 0% 25%,white 0% 50%) 0/12px 12px}.sizes>span{display:flex;flex-direction:column;align-items:center}</style>')
s = s.replace('大圖供方向比較；下方 32／48／64 CSS px 才是小尺寸檢閱。', '比較圖已對齊可視大小，僅調整頁面中的透明留白；原圖保留。32／48／64 px 為容器尺寸。')
(OUT / 'index.html').write_text(s)
print('Recorded 3 original RGBA candidates and built comparison with 32/48/64px, states and backgrounds.')
