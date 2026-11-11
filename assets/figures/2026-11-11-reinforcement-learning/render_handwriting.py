"""Create labeled presentation excerpts without altering the supplied PDF."""
from pathlib import Path
import subprocess,tempfile,shutil
from PIL import Image
here=Path(__file__).resolve().parent
vault=here.parents[2]
pdf=vault/'raw/notes/2026-11-11-Reinforcement-learning-handwritten-notes.pdf'
renderer=shutil.which('pdftoppm')
if not renderer:raise RuntimeError('Poppler pdftoppm is required')
with tempfile.TemporaryDirectory(prefix='rl-handwriting-') as work:
    prefix=Path(work)/'page'
    subprocess.run([renderer,'-scale-to','3500','-png',str(pdf),str(prefix)],check=True)
    Image.open(Path(work)/'page-1.png').crop((0,1000,2667,1960)).save(here/'handwriting-bellman.png')
    Image.open(Path(work)/'page-3.png').crop((0,0,1200,1600)).save(here/'handwriting-approximation.png')
print('Rendered two excerpts; original PDF unchanged.')
