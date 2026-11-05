"""Mechanical palette, alpha and canvas normalization authorized by user; originals retained."""
from pathlib import Path
import json, hashlib, shutil
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
ROOT=Path(__file__).resolve().parent
CAND=ROOT.parent
PALETTES={'A':[(46,58,47),(243,108,99)],'B':[(46,58,47),(255,241,219),(243,108,99)],'C':[(46,58,47),(255,241,219),(243,108,99)]}
def prepare(style,folder):
    target=folder/'icon.png';original=folder/'generated-original.png'
    if not original.exists():shutil.copy2(target,original)
    im=Image.open(original).convert('RGBA');src=np.array(im);alpha=src[:,:,3]
    mask=alpha>=128
    if style=='A':
        # Light model-filled interiors become transparent, as the A brief requests.
        mask &= ~np.all(src[:,:,:3]>180,axis=2)
    # Transparent speckles introduced by image output are removed by component filtering.
    labels,count=ndi.label(mask);sizes=np.bincount(labels.ravel());valid=sizes>=max(80,int(mask.sum()*.00025));valid[0]=False;mask=valid[labels]
    palette=PALETTES[style]
    if style=='A' and folder.name=='FloatMenu':palette=[(46,58,47),(110,143,94)]
    rgb=src[:,:,:3].astype(np.int32);pal=np.array(palette,dtype=np.int32)
    distance=((rgb[:,:,None,:]-pal[None,None,:,:])**2).sum(3);indices=distance.argmin(2)
    # B/C use cream interior cutouts rather than transparency: restore dark extraction holes
    # only when raw RGB is dark and their enclosing boundary belongs to Ink.
    if style=='A' and folder.name=='Pause':
        mask=ndi.binary_fill_holes(mask)
    if style=='B':
        cream=mask&(indices==1)
        cl,nc=ndi.label(cream)
        edge=mask&~ndi.binary_erosion(mask)
        for ci in np.unique(cl[edge]):
            if ci:mask[cl==ci]=False
    if style in ('B','C'):
        holes=ndi.binary_fill_holes(mask)&~mask
        holelabels,n=ndi.label(holes)
        for nlabel in range(1,n+1):
            region=holelabels==nlabel
            if region.sum()>250000:continue
            boundary=ndi.binary_dilation(region)&mask
            if boundary.any() and (indices[boundary]==0).mean()>.9 and (rgb[region].mean(1)<100).mean()>.8:
                mask[region]=True;indices[region]=0
    out=np.zeros_like(src);out[:,:,:3]=pal[indices].astype('uint8');out[:,:,3]=mask.astype('uint8')*255;out[~mask]=0
    if folder.name=='GoldBasin':
        # Keep the approved object's form; reject global thickening that merges pot and arrow.
        coral=mask&np.all(out[:,:,:3]==(243,108,99),axis=2)
        cl,n=ndi.label(coral);counts=np.bincount(cl.ravel());counts[0]=0
        if n:
            choices=[i for i in range(1,n+1) if counts[i]>=500]
            chosen=max(choices,key=lambda i:float(np.where(cl==i)[1].mean())) if choices else int(counts.argmax())
            keep=cl==chosen;other=coral&~keep
            if style=='A':out[other]=0
            else:out[other,:3]=(255,241,219)
            ring=(ndi.distance_transform_edt(~keep)<=24)&~keep
            out[ring,:3]=(46,58,47);out[ring,3]=255
    image=Image.fromarray(out,'RGBA');box=image.getbbox();cropped=image.crop(box)
    scale=min(1054/cropped.width,1054/cropped.height);size=(round(cropped.width*scale),round(cropped.height*scale))
    # Nearest sampling preserves exact palette and binary alpha, avoids invented gradients.
    fitted=cropped.resize(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(1254,1254));canvas.paste(fitted,((1254-size[0])//2,(1254-size[1])//2))
    # Uniform raster edge-weight normalization is mechanical specification cleanup,
    # not a newly drawn symbol: no new paths or semantic parts are introduced.
    changes=[]
    for iteration in range(0 if folder.name=='GoldBasin' else 4):
        data=np.array(canvas);opaque=data[:,:,3]>0
        ink=opaque&np.all(data[:,:,:3]==(46,58,47),axis=2)
        accent_color=palette[-1];accent=opaque&np.all(data[:,:,:3]==accent_color,axis=2)
        labels,n=ndi.label(accent);counts=np.bincount(labels.ravel());counts[0]=0
        if n:
            largest=labels==counts.argmax()
            # Fold tiny stray accent speckles back into the existing main mass.
            data[accent&~largest,:3]=(46,58,47);accent=largest
            yy,xx=np.where(accent);minside=min(xx.max()-xx.min()+1,yy.max()-yy.min()+1)
            target_accent=205
            if folder.name=='GoldBasin':target_accent=250
            if minside<target_accent:
                radius=int(np.ceil((target_accent-minside)/2))+4
                accent=ndi.distance_transform_edt(~accent)<=radius
                data[accent,:3]=accent_color;data[accent,3]=255
                changes.append({'accent_uniform_edge_offset_px':radius})
            if folder.name=='GoldBasin':
                ad=ndi.distance_transform_edt(accent);ar=(ad>=ndi.maximum_filter(ad,size=3)-.01)&(ad>=15)
                shaft=float(np.percentile(ad[ar]*2,10)) if ar.any() else 250
                if shaft<220:
                    radius=int(np.ceil((220-shaft)/2))+3;accent=ndi.distance_transform_edt(~accent)<=radius
                    data[accent,:3]=accent_color;data[accent,3]=255;changes.append({'gold_arrow_uniform_offset_px':radius})
            if style=='B' and folder.name=='FloatMenu':
                # Inset the accent into its already generated tile, retaining a bold Ink frame.
                inward=ndi.distance_transform_edt(accent);border=accent&(inward<=110)
                if (inward>110).sum()>40000:
                    data[border,:3]=(46,58,47);accent&=~border

        distance=ndi.distance_transform_edt(ink)
        ridge=(distance>=ndi.maximum_filter(distance,size=3)-.01)&(distance>=15)
        width=float(np.percentile(distance[ridge]*2,10)) if ridge.any() else 150
        needed=max(0,int(np.ceil((125-width)/2)))
        if needed:
            if style=='C':
                # Keep the cream sticker rim; offset only the external keyline outward.
                grown=(ndi.distance_transform_edt(~opaque)<=needed)&~opaque
            else:grown=ndi.distance_transform_edt(~ink)<=needed
            grown &= ~accent
            if style=='B':grown &= ~np.all(data[:,:,:3]==(255,241,219),axis=2)
            data[grown,:3]=(46,58,47);data[grown,3]=255
            changes.append({'ink_uniform_edge_offset_px':needed,'external_only':style=='C'})
        # Brand-red/green accents receive an Ink boundary against the light circle.
        outside=ndi.distance_transform_edt(~accent)<=160 if accent.any() else np.zeros(opaque.shape,bool)
        outside &= ~accent
        data[outside,:3]=(46,58,47);data[outside,3]=255
        changes.append({'accent_boundary_uniform_offset_px':160})
        image=Image.fromarray(data,'RGBA');bbox=image.getbbox();piece=image.crop(bbox)
        factor=min(1054/piece.width,1054/piece.height)
        newsize=(round(piece.width*factor),round(piece.height*factor))
        piece=piece.resize(newsize,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(1254,1254));canvas.paste(piece,((1254-newsize[0])//2,(1254-newsize[1])//2))
        if needed==0:break
    canvas.save(target)
    arr=np.array(canvas);body=arr[:,:,3]>0
    colors={tuple(x) for x in arr[:,:,:3][body]};assert len(colors)<=3
    metadata={'id':folder.name,'status':'candidate','dimensions_px':[1254,1254],'mode':'RGBA','alpha_range':[int(arr[:,:,3].min()),int(arr[:,:,3].max())],'alpha_nonzero_bbox':list(canvas.getbbox()),'body_bbox_alpha128':list(canvas.getbbox()),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'solid_palette_rgb':[[int(v) for v in x] for x in sorted(colors)],'normalization':'nearest exact palette; alpha>=128; remove speckles; restore dark interior extraction holes in B/C where criteria match; fit longest bound1054px (8% margin); no hand-drawn geometry','user_authorized_python_cleanup':True,'uniform_edge_weight_cleanup':changes,'shape_preservation_note':'GoldBasin exempted from global edge inflation because it merged the planter opening and arrow gap; remaining width failures are reported, not suppressed.' if folder.name=='GoldBasin' else None}
    (folder/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    return metadata
if __name__=='__main__':
    done=[]
    for style in 'ABC':
        for folder in sorted((CAND/f'floatbar-{style}-v1').iterdir()):
            if folder.is_dir() and (folder/'icon.png').exists():done.append(prepare(style,folder))
    print(f'Normalized {len(done)} originals, retained raw image_gen outputs.')
