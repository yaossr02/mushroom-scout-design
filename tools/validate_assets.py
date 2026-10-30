"""Validate recorded original candidates; no image mutation or visual approval."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'brand/catalog.json').read_text())
for asset in catalog['assets']:
    path = ROOT / asset['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == asset['sha256'], asset['id']
    with Image.open(path) as im:
        assert list(im.size) == asset['dimensions_px'], asset['id']
        if asset.get('alpha_policy') == 'opaque':
            assert im.mode in ('RGB', 'RGBA'), asset['id']
            if im.mode == 'RGBA':
                assert im.getchannel('A').getextrema() == (255, 255), asset['id']
        else:
            assert im.mode == 'RGBA', asset['id']
            alpha = im.getchannel('A')
            assert alpha.getextrema() == (0, 255), asset['id']
            bbox = alpha.point(lambda a: 255 if a >= 128 else 0).getbbox()
            assert list(bbox) == asset['body_bbox_alpha128'], asset['id']
            assert bbox[0] > 0 and bbox[1] > 0 and bbox[2] < im.width and bbox[3] < im.height
    assert asset['status'] in ('candidate', 'approved', 'rejected')
    if asset['status'] == 'approved':
        assert asset.get('approval_record'), 'Explicit user approval record required'
    print(f"OK {asset['id']}@{asset['version']} {asset['status']} active_reference={asset.get('active_reference', True)} {im.width}x{im.height}")
if catalog.get('current_direction_version') == 'v0.5':
    active = [a for a in catalog['assets'] if a.get('active_reference', False)]
    for asset in active:
        if asset['id'] not in ('leaf-sprout', 'flower-bud'):
            assert asset['version'] == 'v0.5', 'Legacy mushroom/brand reference is still active'
            assert asset.get('anthropomorphic_features_allowed') is False
    assert len([a for a in active if a.get('kind') == 'content']) == 15
    assert len([a for a in active if a.get('kind') not in (None, 'content')]) == 4
assert (ROOT / 'brand/reviews/v0.1/review.html').is_file()
print('Metadata checks passed. Visual style and clean alpha edges still require human review.')
