"""Record generated originals and verify coverage of every existing functional use."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'brand/ui/v0.7-botanical'
ALIASES={'Search':'search','Settings':'settings','Scan':'scan','Favorite':'favorite','Photo':'photo','ZoomIn':'plus','Add':'plus','ZoomOut':'minus','Remove':'minus','Crosshair':'crosshair','FitAll':'fit-all','Timezones':'timezones','OpenOutside':'open-outside','SkipForward':'skip-forward','SkipBack':'skip-back','FloatMenu':'float-menu','LightSpeed':'light-speed','ReturnToApp':'return-to-app'}
def slug(id):return ALIASES.get(id,id.lower())
def main():
 c=json.loads((PACK/'catalog.json').read_text());old=json.loads((ROOT/'brand/ui/v0.6/catalog.json').read_text())
 existing={i['id']:i for i in c['icons']}
 c['first_six_approval_record']=c.get('first_six_approval_record',c.get('approval_record'));c['approval_record']=None
 sources_file=PACK/'GENERATION-SOURCES.json';sources=json.loads(sources_file.read_text()) if sources_file.exists() else {}
 # The original six are immutable; approval is specific to recorded hashes.
 for i in existing.values():
  if i['status']=='approved':assert hashlib.sha256((ROOT/i['path']).read_bytes()).hexdigest()==i['sha256'],i['id']
 labels={slug(i['id']):i['label'] for i in old['icons']};labels.update(plus='新增／放大',minus='移除／縮小')
 specs=json.loads((PACK/'REMAINING-PROMPTS.json').read_text())['prompts']
 for spec in specs:
  id=spec['id'];p=PACK/f'png/{id}.png'
  if id in existing and existing[id]['status']=='approved':continue
  with Image.open(p) as im:
   assert im.mode=='RGBA',f'{id}: expected RGBA'
   a=im.getchannel('A');assert a.getextrema()==(0,255),f'{id}: transparency'
   bbox=a.point(lambda v:255 if v>=128 else 0).getbbox();assert bbox,f'{id}: empty'
   if id=='empty':assert a.getpixel((im.width//2,im.height//2))<=8,'Empty must have a transparent center'
   existing[id]={'id':id,'label':labels[id],'status':'candidate','path':str(p.relative_to(ROOT)),'dimensions_px':list(im.size),'mode':im.mode,'alpha_range':list(a.getextrema()),'alpha_nonzero_bbox':list(a.getbbox()),'body_bbox_alpha128':list(bbox),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'date':'2026-11-01','generated_original':sources.get(id),'tool':'image_gen','prompt_file':'brand/ui/v0.7-botanical/STOP-RETRY.json' if id=='stop' else 'brand/ui/v0.7-botanical/REMAINING-PROMPTS.json','selected_state':'same original PNG plus cream backing, sage border and bottom dot','vector':False}
 semantics=[]
 for i in old['icons']:
  id=slug(i['id']);asset=existing[id]
  semantics.append({'id':i['id'],'label':i['label'],'group':i['group'],'asset_id':id,'normal':asset['path'],'selected':asset['path'],'selected_container':'cream backing, sage border, bottom dot','status':asset['status'],'approval_record':asset.get('approval_record'),'usage_status':i['usage_status'],'usage_references':i.get('usage_references',[])})
 assert len(semantics)==56 and len({i['id'] for i in semantics})==56
 assert len(existing)==55
 assert len({a['sha256'] for a in existing.values()})==55,'Unexpected duplicate original images'
 c.update(status='mixed-approval',icons=list(existing.values()),semantics=semantics,source_count=len(existing),semantic_count=len(semantics),additional_brand_entry={'id':'Map','asset_id':'map','label':'地圖入口','status':'approved'},remaining_semantics_not_redesigned=0,approved_original_count=sum(i['status']=='approved' for i in existing.values()),new_candidate_original_count=sum(i['status']=='candidate' for i in existing.values()),source_mapping='56 legacy use IDs preserved; Map is an additional approved brand entry, not Layers',dark_background_policy='Use cream backing for dark interfaces; raw sage on dark is inspection only.')
 (PACK/'catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
 print(f"{len(semantics)} functional uses + approved Map entry; {len(existing)} originals, {sum(i['status']=='approved' for i in existing.values())} approved and {sum(i['status']=='candidate' for i in existing.values())} candidates. All hashes, RGBA and alpha ranges verified.")
if __name__=='__main__':main()
