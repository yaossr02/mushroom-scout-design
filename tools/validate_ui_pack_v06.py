"""Validate the licensed functional icon delivery, mappings and actual raster outputs."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'brand/ui/v0.6'
c = json.loads((PACK / 'catalog.json').read_text())
assert c['library_version'] == '2.1.1' and c['license'] == 'MIT'
assert len(c['icons']) == c['total_semantics'] == 56
assert len(c['glyphs']) == c['unique_glyphs'] == 92
assert len({i['id'] for i in c['icons']}) == 56
source_pairs = re.findall(r'^    (\w+)\(R.drawable\.(ph_\w+), R.drawable\.(ph_\w+)\)', (PACK / 'sources/AppIcon.kt').read_text(), re.M)
assert len(source_pairs) == 52
entries = {i['id']: i for i in c['icons']}
for ident, normal, selected in source_pairs:
    assert (entries[ident]['normal'], entries[ident]['selected']) == (normal, selected), ident
assert entries['Empty']['normal'] == entries['Empty']['selected'] == 'ph_circle'
assert entries['Dispatch']['usage_status'] == 'placeholder'
assert {i['id'] for i in c['icons'] if i['usage_status'] == 'reserved-unreferenced'} == {'Info','Rotate'}
wanted = {i[k] for i in c['icons'] for k in ('normal','selected')}
assert wanted == {g['id'] for g in c['glyphs']}
android_ns = '{http://schemas.android.com/apk/res/android}'
png_count = 0
for g in c['glyphs']:
    svg_path, xml_path = PACK / g['svg'], PACK / g['android']
    assert hashlib.sha256(svg_path.read_bytes()).hexdigest() == g['svg_sha256'], g['id']
    assert hashlib.sha256(xml_path.read_bytes()).hexdigest() == g['android_sha256'], g['id']
    svg, xml = ET.parse(svg_path).getroot(), ET.parse(xml_path).getroot()
    assert svg.attrib['viewBox'] == '0 0 256 256'
    assert xml.attrib[android_ns+'width'] == '24dp'
    assert xml.attrib[android_ns+'height'] == '24dp'
    assert xml.attrib[android_ns+'viewportWidth'] == '256'
    assert [p.attrib['d'] for p in svg] == [p.attrib[android_ns+'pathData'] for p in xml], g['id']
    for size in (24,48):
        p = PACK / g['png'][str(size)]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == g['png_sha256'][str(size)], g['id']
        with Image.open(p) as im:
            assert im.mode == 'RGBA' and im.size == (size,size), g['id']
            assert im.getchannel('A').getextrema() == (0,255), g['id']
            assert im.getchannel('A').getbbox(), g['id']
        png_count += 1
assert png_count == 184
sprite = ET.parse(PACK / 'sprite.svg').getroot()
assert {s.attrib['id'] for s in sprite} == wanted
assert 'MIT License' in (PACK / 'LICENSE-phosphor.txt').read_text()
browser = json.loads((PACK / 'review/browser-check.json').read_text())
assert browser['errors'] == [] and browser['png_exports'] == 184
report = {'version':'v0.6','status':'candidate','semantic_count':56,'android_mapping_count':52,'ios_supplement_count':4,'glyph_count':92,'svg_count':92,'android_xml_count':92,'transparent_png_count':184,'svg_android_geometry':'matched','source_mappings':'unchanged','license':'MIT retained','app_repo_modified':False,'app_runtime_tested':False}
(PACK / 'review/technical-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('56 semantics, 92 SVG/XML pairs, 184 transparent PNGs, sprite, source mappings and MIT license verified.')
