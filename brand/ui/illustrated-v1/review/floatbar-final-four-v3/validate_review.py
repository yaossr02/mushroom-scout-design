from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
R=Path(__file__).resolve().parent
S=R.parents[1]
REPO=S.parents[2]
c=json.loads((R/'catalog.json').read_text())
assert len(c['assets'])==8
for a in c['assets']:
    p=REPO/a['final']['path']
    im=Image.open(p)
    assert im.size==(1254,1254) and im.mode=='RGBA'
    assert im.getchannel('A').getextrema()==(0,255)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==a['final']['sha256']
    assert a['status']=='candidate'
    b=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()
    assert min(b[0],b[1],1254-b[2],1254-b[3])>=95
    q=json.loads((p.parent/'PROMPT.json').read_text())
    assert len(q['reference'])==3 and all((REPO/x).exists() for x in q['reference'])
for p,h in json.loads((R/'protected-hashes.json').read_text()).items():
    assert hashlib.sha256((REPO/p).read_bytes()).hexdigest()==h,p
m=json.loads((S/'approved/batch3-map/current-manifest.json').read_text())
assert len(m['assets'])==7 and m['ready_for_full_replacement']
m=json.loads((S/'approved/batch2-floatbar/manifest.json').read_text())
assert len(m['assets'])==11 and not m['ready_for_full_replacement']
print('PASS 8 v3 candidate PNGs, dimensions/alpha/bbox/hash, 3 references each; all approved assets unchanged; map complete and floatbar still pending four.')
