"""Record and display original pull-basin candidates without modifying image pixels."""
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'brand/ui/v0.7-botanical'
OUT = PACK / 'candidates/gold-basin-pull-v2'
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
        assets.append(dict(id=f'gold-basin-pull-{letter}', label=variant['label'], status='candidate', active_reference=True,
            path=str(path.relative_to(ROOT)), dimensions_px=list(im.size), mode=im.mode,
            alpha_range=list(alpha.getextrema()), alpha_nonzero_bbox=list(alpha.getbbox()),
            body_bbox_alpha128=list(alpha.point(lambda x: 255 if x >= 128 else 0).getbbox()),
            sha256=hashlib.sha256(path.read_bytes()).hexdigest(), date=prompts['date'], tool='image_gen',
            prompt_file=str((OUT / 'PROMPTS.json').relative_to(ROOT)), vector=False,
            selected_state='same original PNG plus cream backing, sage border and bottom dot'))
catalog['icons'] = [i for i in catalog['icons'] if not i['id'].startswith('gold-basin-pull-')] + assets
old = next(i for i in catalog['icons'] if i['id'] == 'gold-basin')
old.update(status='rejected', active_reference=False, rejection_reason='User requested stronger pulling action and three alternatives, 2026-11-04')
for semantic in catalog['semantics']:
    if semantic['id'] == 'GoldBasin':
        semantic.update(candidate_options=[a['id'] for a in assets], selection_pending=True,
            status='candidate', note='Original static basin retired. A/B/C alternatives await selection; no App change.')
catalog.update(source_count=len(catalog['icons']), active_source_count=58, approved_original_count=6,
    new_candidate_original_count=52, rejected_original_count=1)
(PACK / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
(OUT / 'catalog.json').write_text(json.dumps(dict(status='candidate', selection_pending=True, assets=assets), ensure_ascii=False, indent=2) + '\n')
s = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>拉金盆 · 三種拉拔動作提案</title><style>
*{box-sizing:border-box}body{margin:0;padding:40px;width:1500px;background:#f6f2e9;color:#374d3d;font-family:sans-serif}h1{font-size:36px}p{font-size:20px;line-height:1.5}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}article{padding:22px;border-radius:24px;background:#fffdf8;border:1px solid #d9dfcf;text-align:center}h2{font-size:28px}.hero{width:310px;height:310px;object-fit:contain}.sample{display:inline-flex;align-items:center;justify-content:center;width:80px;height:80px;border-radius:18px}.sample img{width:64px;height:64px;object-fit:contain}.selected{background:#fff1db;border:2px solid #55735b}.sizes{display:flex;align-items:end;justify-content:center;gap:24px;margin:24px 0}.sizes img{display:block;object-fit:contain}.dark{background:#263a30;padding:12px;border-radius:16px}.dark img{background:#fff1db;border-radius:12px}.checker{background:repeating-conic-gradient(#ddd 0% 25%,white 0% 50%) 0/12px 12px;border-radius:12px}.status{color:#a16b20}</style><h1>拉金盆 · 三種拉拔動作提案</h1><p>比較示意：直接引用獨立透明原圖，沒有重畫或裁切。A／B／C 均待選擇與審核。舊靜態金盆已停用。<br>大圖供方向比較；下方 32／48／64 CSS px 才是小尺寸檢閱。未匯入 App。</p><div class="grid">'''
descriptions = ['向上箭頭＋離地間隙，強調拔起方向。', '拉環＋繃緊雙繩，強調受力與提拉。', '斜向箭頭＋拖曳線，強調拉出動勢。']
for a, description in zip(assets, descriptions):
    letter = a['id'][-1].upper()
    src = '/' + a['path']
    s += f'<article><h2>{letter}　{a["label"]}</h2><img class="hero" src="{src}" alt="{a["label"]}"><p>{description}</p><div class="status">candidate · 待審核</div><p><span class="sample"><img src="{src}" alt="一般"></span><span class="sample selected"><img src="{src}" alt="選取"></span></p><div class="sizes">'
    for n in (32, 48, 64):
        s += f'<span><img src="{src}" width="{n}" height="{n}" alt="{n}px">{n}px</span>'
    s += f'</div><div class="dark"><span class="sample"><img src="{src}" alt="深色承托底"></span><span class="sample checker"><img src="{src}" alt="棋盤底"></span></div></article>'
s += '</div><p>懸浮選單／地圖工具列示意（非 App 實機）：'
for a in assets:
    s += f'<span class="sample selected"><img src="/{a["path"]}" alt="{a["label"]}"></span> '
s += '</p></html>'
(OUT / 'index.html').write_text(s)
print('Recorded 3 original RGBA candidates and built comparison with 32/48/64px, states and backgrounds.')
