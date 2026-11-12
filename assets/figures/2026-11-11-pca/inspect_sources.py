"""Read-only source rendering; run with the bundled Python (pypdfium2, Pillow)."""
from pathlib import Path
import base64
import json
import hashlib
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent / 'source-previews'
OUT.mkdir(exist_ok=True)
PDF = ROOT / 'raw/articles/2026-11-11-dimensionality-reduction-slides.pdf'
doc = pdfium.PdfDocument(PDF)
for start in range(0, len(doc), 12):
    sheet = Image.new('RGB', (1200, 1050), 'white')
    draw = ImageDraw.Draw(sheet)
    for j, index in enumerate(range(start, min(start + 12, len(doc)))):
        page = doc[index].render(scale=1).to_pil().convert('RGB')
        page.thumbnail((390, 225))
        x, y = (j % 3) * 400, (j // 3) * 260
        sheet.paste(page, (x, y + 25))
        draw.text((x + 8, y + 6), f'Slide {index + 1}', fill='black')
    sheet.save(OUT / f'slides-{start+1:02d}-{min(start+12,len(doc)):02d}.png')
for index in [6, 12, 13, 24, 25, 26, 27, 32, 33, 34]:
    doc[index].render(scale=1.6).to_pil().save(OUT / f'slide-{index+1:02d}.png')

nbpath = ROOT / 'raw/notebooks/2026-11-11-rna-seq-tsne/PCA_tSNE_UMAP.ipynb'
nb = json.loads(nbpath.read_text(encoding='utf-8'))
recovered = []
for i, cell in enumerate(nb['cells'], start=1):
    for j, output in enumerate(cell.get('outputs', []), start=1):
        data = output.get('data', {}).get('image/png')
        if not data:
            continue
        contents = base64.b64decode(''.join(data) if isinstance(data, list) else data)
        name = f'2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-{i:02d}-output-{j}.png'
        path = ROOT / 'raw/assets' / name
        if path.exists():
            assert path.read_bytes() == contents, 'Never overwrite a different original'
        else:
            path.write_bytes(contents)
        recovered.append({'cell': i, 'output': j, 'path': path.relative_to(ROOT).as_posix(),
                          'sha256': hashlib.sha256(contents).hexdigest()})
sheet = Image.new('RGB', (1200, 320 * ((len(recovered)+2)//3)), 'white')
draw = ImageDraw.Draw(sheet)
for j, rec in enumerate(recovered):
    image = Image.open(ROOT / rec['path']).convert('RGB')
    image.thumbnail((390, 285))
    x, y = (j % 3)*400, (j//3)*320
    sheet.paste(image, (x, y+25))
    draw.text((x+8, y+5), f"Notebook cell {rec['cell']}", fill='black')
sheet.save(OUT / 'notebook-outputs.png')
(OUT / 'recovered-assets.json').write_text(json.dumps(recovered, indent=2), encoding='utf-8')
print(json.dumps({'slides':len(doc), 'notebook_images':recovered},indent=2))
