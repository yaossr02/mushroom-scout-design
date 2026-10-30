"""Read-only technical validation for v0.5 platform candidates and review assets."""
import hashlib
import json
import math
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'brand/catalog.json').read_text())
assets = {a['id']: a for a in catalog['assets'] if a['version'] == 'v0.5'}
assert len(assets) == 19
platform = json.loads((ROOT / 'brand/systems/v0.5/platform-plan.json').read_text())
report = {'version': 'v0.5', 'status': 'candidate', 'device_runtime_tested': False, 'checks': {}}
for ident, scale in [('android-adaptive-foreground', platform['android_adaptive']['foreground_source_scale']), ('android-themed-monochrome', platform['android_themed']['source_scale'])]:
    with Image.open(ROOT / assets[ident]['path']) as im:
        alpha = im.getchannel('A')
        largest = 0.0
        outside = 0
        for idx, a in enumerate(alpha.get_flattened_data()):
            if a < 128:
                continue
            x, y = idx % im.width, idx // im.width
            radius = math.hypot((x + 0.5) / im.width - 0.5, (y + 0.5) / im.height - 0.5) * scale
            largest = max(largest, radius)
            outside += radius > 66 / 108 / 2
        assert outside == 0, ident
        report['checks'][ident] = {'source_scale': scale, 'alpha_threshold': 128, 'maximum_radius_normalized': largest, 'safe_radius_normalized': 66 / 108 / 2, 'outside_pixels': outside}
for ident in ['android-themed-monochrome', 'notification-mushroom']:
    with Image.open(ROOT / assets[ident]['path']) as im:
        min_rgb, max_rgb = 255, 0
        for r, g, b, a in im.get_flattened_data():
            if a >= 128:
                min_rgb = min(min_rgb, r, g, b)
                max_rgb = max(max_rgb, r, g, b)
        assert max_rgb <= 2, ident
        report['checks'].setdefault(ident, {})['opaque_rgb_range'] = [min_rgb, max_rgb]
with Image.open(ROOT / assets['ios-app-icon']['path']) as im:
    assert im.mode == 'RGB' or im.getchannel('A').getextrema() == (255, 255)
    report['checks']['ios-app-icon'] = {'mode': im.mode, 'dimensions': list(im.size), 'opaque': True}
report['screenshots'] = {}
for name in ['01-mushrooms.png', '02-marker-system.png', '03-brand-platforms.png']:
    p = ROOT / 'brand/reviews/v0.5' / name
    with Image.open(p) as im:
        report['screenshots'][name] = {'dimensions': list(im.size), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
(ROOT / 'brand/reviews/v0.5/technical-check.json').write_text(json.dumps(report, indent=2) + '\n')
print('v0.5 safe-circle checks, near-black masks, opaque iOS source and review screenshots passed.')
