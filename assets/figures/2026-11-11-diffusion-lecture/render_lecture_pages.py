"""Preserve selected complete lecture-page renders, without cropping or annotation.
Run with Python + pypdfium2 + Pillow. Existing renders are never overwritten.
"""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / 'raw/notes/2026-11-10-Lec12-diffusion-models.pdf'
assert hashlib.sha256(PDF.read_bytes()).hexdigest() == '5ab40d7fc682f824c473203c3acdaa9d7d2858a87b23adaaf9e406abfb7ff789'
doc = pdfium.PdfDocument(str(PDF))
assert len(doc) == 32
pages = {5: 'processes', 28: 'guidance', 29: 'conditioning-applications', 30: 'tradeoffs'}
manifest = {'source': PDF.relative_to(ROOT).as_posix(), 'pages_in_source': len(doc),
            'scale': 2.0, 'method': 'Full-page PDFium render; no cropping, retouching, or relabeling', 'renders': []}
for number, label in pages.items():
    image = doc[number-1].render(scale=2.0).to_pil().convert('RGB')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    data = buffer.getvalue()
    target = ROOT / f'raw/assets/2026-11-11-Diffusion-lecture-P{number:02}-{label}.png'
    if target.exists():
        if target.read_bytes() != data:
            raise RuntimeError(f'Preserved render already exists with different bytes: {target}')
    else:
        target.write_bytes(data)
    manifest['renders'].append({'page': number, 'path': target.relative_to(ROOT).as_posix(),
                                'sha256': hashlib.sha256(data).hexdigest(), 'size': list(image.size)})
(Path(__file__).parent / 'page-render-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print(json.dumps(manifest, indent=2))
