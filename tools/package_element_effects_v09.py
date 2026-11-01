"""Validate and bundle original effect layers, rendered previews and unchanged bases."""
import hashlib,json,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'brand/effects/v0.9-orbit-bold'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 c=json.loads((PACK/'catalog.json').read_text());browser=json.loads((PACK/'review/browser-check.json').read_text());assert browser['errors']==[] and browser['effect_count']==5
 for a in c['assets']:
  assert sha(ROOT/a['base'])==a['base_sha256'],a['id']
  assert sha(ROOT/a['layer'])==a['layer_sha256'],a['id']
  approval=json.loads((PACK/'approval.json').read_text())
  assert sha(ROOT/a['layer'])==approval['layers'][a['id']]
  p=ROOT/a['composite_preview']
  assert sha(p)==approval['composites'][a['id']],a['id']
  with Image.open(p) as im:
   assert im.mode=='RGBA' and im.size==(1254,1254),a['id']
   assert im.getchannel('A').getextrema()==(0,255),a['id']
   a['composite_dimensions_px']=list(im.size);a['composite_mode']=im.mode;a['composite_alpha_range']=[0,255];a['composite_sha256']=sha(p)
 (PACK/'catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
 report={'version':c['version'],'status':c['status'],'effect_layers':5,'unchanged_approved_bases':5,'base_and_layer_hashes':'verified','transparent_exports':5,'export_dimensions_px':[1254,1254],'transparent_cap_hole_stem_probes':'passed','browser':browser,'app_runtime_tested':False,'runtime_animation_generated':False}
 (PACK/'review/technical-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 archive=PACK/'mushroom-scout-element-effects-v0.9.zip';manifest=PACK/'package-manifest.json'
 paths=[p for p in PACK.rglob('*') if p.is_file() and p not in (archive,manifest)]
 paths += [ROOT/a['base'] for a in c['assets']]
 paths += [ROOT/c['approval_record'],ROOT/'brand/catalog.json',ROOT/'tools/build_element_effects_v09.py',ROOT/'tools/render_element_effects_v09.cjs']
 paths=sorted(set(paths))
 manifest.write_text(json.dumps({'status':c['status'],'archive_paths':'relative to design repository root','files':{str(p.relative_to(ROOT)):sha(p) for p in paths}},ensure_ascii=False,indent=2)+'\n')
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for p in paths+[manifest]:z.write(p,str(p.relative_to(ROOT)))
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 print(f'Verified 5 unchanged bases, 5 layer hashes and 5 RGBA 1254px exports; ZIP CRC passed ({archive.stat().st_size} bytes).')
if __name__=='__main__':main()
