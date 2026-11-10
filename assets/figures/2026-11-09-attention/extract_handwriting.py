"""Extract labelled, unretouched regions from the preserved attention PDF.

Coordinates refer to Poppler's 150-dpi full-page raster. These PNGs are derived
PDF excerpts, not separately supplied original images. The source PDF stays
byte-identical. Run from any directory with pdftoppm and Pillow available.
"""
from pathlib import Path
import hashlib, json, subprocess, tempfile
from PIL import Image

out=Path(__file__).resolve().parent
vault=out.parents[2]
source=vault/'raw/notes/2026-11-09-attention.pdf'
regions=[
    ('p01-head-separation-and-output',1,(800,700,1275,1504)),
    ('p01-column-multiplication',1,(0,1530,330,1674)),
    ('p02-dot-and-outer-products',2,(0,0,325,140)),
    ('p02-mla-absorption',2,(0,325,480,1015)),
    ('p02-why-kv-and-latent-roles',2,(0,995,810,1330)),
]
manifest={'source':'raw/notes/2026-11-09-attention.pdf',
          'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'dpi':150,'coordinate_convention':'pixels, left/top/right/bottom; top-left origin',
          'excerpts':[]}
with tempfile.TemporaryDirectory(prefix='attention-pdf-') as tmp:
    prefix=str(Path(tmp)/'page')
    subprocess.run(['pdftoppm','-r','150','-png',str(source),prefix],check=True)
    for name,page,rect in regions:
        im=Image.open(f'{prefix}-{page}.png')
        assert 0<=rect[0]<rect[2]<=im.width and 0<=rect[1]<rect[3]<=im.height,(name,im.size)
        target=out/(name+'.png')
        im.crop(rect).save(target)
        manifest['excerpts'].append({'file':target.name,'page':page,'rectangle':rect,
                                    'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(out/'extraction-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,indent=2))
