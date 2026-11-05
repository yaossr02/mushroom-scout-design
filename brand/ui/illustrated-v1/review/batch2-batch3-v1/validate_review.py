from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image

R=Path(__file__).resolve().parent
S=R.parents[1]
REPO=S.parents[2]
data=json.loads((R/'catalog.json').read_text())
assert len(data['assets'])==44
assert sum(a['batch']=='floatbar' for a in data['assets'])==30
assert sum(a['batch']=='map' for a in data['assets'])==14
for a in data['assets']:
    p=REPO/a['final']['path']
    im=Image.open(p)
    assert im.size==(1254,1254) and im.mode=='RGBA',str(p)
    assert im.getchannel('A').getextrema()==(0,255),str(p)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==a['final']['sha256']
    assert a['status']=='candidate'
    box=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()
    assert min(box[0],box[1],1254-box[2],1254-box[3])>=95,(a['id'],a['concept'],box)
    prompt=json.loads((p.parent/'PROMPT.json').read_text())
    assert len(prompt['reference'])==3
    assert prompt['reference'][:2]==['brand/ui/approved/gold-planter-illustrated-v1/icon.png','brand/approved/v0.5/red-mushroom.png']
    assert prompt['reference'][2].startswith('brand/ui/illustrated-v1/approved/batch1/')
    assert all((REPO/ref).is_file() for ref in prompt['reference'])
    assert (p.parent/'generated-original.png').is_file()
    assert (p.parent/'generation.json').is_file()
for c in ['A','B']:
    up=np.array(Image.open(S/f'candidates/Collapse-{c}-v1/icon.png'))
    down=np.array(Image.open(S/f'candidates/Expand-{c}-v1/icon.png'))
    assert np.array_equal(up[::-1],down),c
    assert (S/f'candidates/Collapse-{c}-v1/generated-original.png').read_bytes()==(S/f'candidates/Expand-{c}-v1/generated-original.png').read_bytes()
for p,h in json.loads((R/'protected-hashes.json').read_text()).items():
    assert hashlib.sha256((REPO/p).read_bytes()).hexdigest()==h,p
assert not (S/'approved/batch2-floatbar').exists()
assert not (S/'approved/batch3-map').exists()
for c in ['A','B']:
    for dp in [24,28]:
        assert Image.open(R/f'floatbar-{c}-{dp}dp-xxxhdpi.png').size==(3136,336)
    assert Image.open(R/f'map-{c}-32dp-xxxhdpi.png').size==(1560,2480)
print('PASS: 44 candidate PNGs, dimensions/alpha/bbox/hash, 3 references each, exact Collapse/Expand RGBA flips, all pre-existing approved files unchanged, no batch2/3 approval dirs.')
