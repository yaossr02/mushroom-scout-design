from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
R=Path(__file__).resolve().parent
S=R.parents[1]
REPO=S.parents[2]
c=json.loads((R/'catalog.json').read_text())
assert len(c['assets'])==14
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
for concept in ['A','B']:
    a=np.array(Image.open(S/f'candidates/Collapse-{concept}-v2/icon.png'))
    b=np.array(Image.open(S/f'candidates/Expand-{concept}-v2/icon.png'))
    assert np.array_equal(a[::-1],b)
for p,h in json.loads((R/'protected-hashes.json').read_text()).items():
    assert hashlib.sha256((REPO/p).read_bytes()).hexdigest()==h,p
for name,n in [('batch2-floatbar',11),('batch3-map',4)]:
    m=json.loads((S/'approved'/name/'manifest.json').read_text())
    assert len(m['assets'])==n and m['ready_for_full_replacement']==False
print('PASS 14 new candidates, RGBA/size/alpha/bbox/hash, 3 references, exact flips, all approved files unchanged; 15 selected designs remain partial approved package.')
