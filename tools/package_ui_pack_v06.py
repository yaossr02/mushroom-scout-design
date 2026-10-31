"""Create and verify a ZIP delivery with a file-level hash manifest."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'brand/ui/v0.6'
archive = ROOT / 'mushroom-scout-ui-icons-v0.6.zip'
manifest = ROOT / 'package-manifest.json'
catalog = json.loads((ROOT / 'catalog.json').read_text())
files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p not in (archive, manifest))
data = dict(version='v0.6',status=catalog['status'],library='Phosphor Icons 2.1.1',license='MIT',semantic_count=56,unique_glyphs=92,
    files=[dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
prefix = 'mushroom-scout-ui-icons-v0.6/'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files + [manifest]:
        z.write(p,prefix+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for entry in data['files']:
        assert hashlib.sha256(z.read(prefix+entry['path'])).hexdigest()==entry['sha256']
print(f'ZIP verified: {len(files)+1} files, {archive.stat().st_size} bytes, SHA256 {hashlib.sha256(archive.read_bytes()).hexdigest()}')
