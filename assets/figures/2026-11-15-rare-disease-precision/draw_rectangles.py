"""Original probability-area illustration for the rare-disease learning note.

Run: python <absolute path to this file>
Requires matplotlib. All outputs are written beside this generator.
The original ROC-note asset is read for preservation checks, never modified.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
TP, TN, FP, FN = '#168575', '#376eae', '#cc4455', '#c68117'
INK, MUTED = '#162b40', '#566778'
pi, tpr, fpr = F(1, 100), F(99, 100), F(1, 100)
mass = {'TP': pi*tpr, 'FN': pi*(1-tpr),
        'FP': (1-pi)*fpr, 'TN': (1-pi)*(1-fpr)}
counts = {k: v*10000 for k, v in mass.items()}
assert counts == {'TP': 99, 'FN': 1, 'FP': 99, 'TN': 9801}
assert sum(mass.values()) == 1
precision = mass['TP']/(mass['TP']+mass['FP'])
metrics = {
    'prevalence': (counts['TP']+counts['FN'])/10000,
    'sensitivity': counts['TP']/(counts['TP']+counts['FN']),
    'specificity': counts['TN']/(counts['TN']+counts['FP']),
    'FPR': counts['FP']/(counts['FP']+counts['TN']),
    'FNR': counts['FN']/(counts['FN']+counts['TP']),
    'precision': counts['TP']/(counts['TP']+counts['FP']),
    'NPV': counts['TN']/(counts['TN']+counts['FN']),
    'accuracy': (counts['TP']+counts['TN'])/10000,
}
assert metrics == dict(prevalence=pi, sensitivity=tpr, specificity=1-fpr,
                      FPR=fpr, FNR=1-tpr, precision=F(1, 2),
                      NPV=F(9801, 9802), accuracy=F(99, 100))
assert precision == F(1, 2)
assert mass['TP'] == mass['FP'] == F(99, 10000)
assert mass['TP']+mass['FP'] == F(99, 5000)
assert 1-precision == F(1, 2)  # Posterior null probability, not FPR.
assert F(1, 10)*F(4, 5)/(F(1, 10)*F(4, 5)+F(9, 10)*F(1, 20)) == F(16, 25)

original = ROOT/'assets/figures/2026-11-10-testing-power/precision-population-area-vs-auc.svg'
original_hash = sha256(original.read_bytes()).hexdigest()
assert original_hash == 'a95f8aa2cf71013da833099b6ec81dc646302230950799bcaace06db9cf34131'

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'text.color': INK, 'svg.fonttype': 'none',
                     'svg.hashsalt': 'rare-disease-precision-2026-11-15',
                     'savefig.facecolor': 'white'})
fig = plt.figure(figsize=(13, 7), facecolor='white')
fig.text(.04, .94, '99% ACCURACY DOES NOT MEAN 99% PRECISION',
         fontsize=23, weight='bold')
fig.text(.04, .89, 'Hypothetical population: 1% disease  |  Sensitivity 99%  |  Specificity 99%',
         fontsize=13, color=MUTED)
fig.text(.04, .81, '1  Whole population: 10,000 people', fontsize=16, weight='bold')
fig.text(.59, .81, '2  Keep only positive tests', fontsize=16, weight='bold')

ax = fig.add_axes([.10, .37, .40, .33])
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis('off')
specs = [((0, 0), pi, tpr, TP, 'TP'),
         ((0, tpr), pi, 1-tpr, FN, 'FN'),
         ((pi, 0), 1-pi, fpr, FP, 'FP'),
         ((pi, fpr), 1-pi, 1-fpr, TN, 'TN')]
for xy, width, height, color, key in specs:
    patch = Rectangle(tuple(map(float, xy)), float(width), float(height),
                      facecolor=color, edgecolor='none')
    ax.add_patch(patch)
    assert abs(patch.get_width()*patch.get_height()-float(mass[key])) < 1e-15
ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor=INK, lw=.7))
ax.text(.51, .56, 'TN = 9,801\ncorrect negatives', color='white', ha='center',
        va='center', fontsize=19, weight='bold', linespacing=1.6)
ax.annotate('Disease: 1%', xy=(.005, 1), xytext=(.04, 1.22),
            ha='center', fontsize=11, annotation_clip=False,
            arrowprops={'arrowstyle': '-', 'color': INK, 'lw': .9})
ax.text(.65, 1.22, 'No disease: 99%', ha='center', fontsize=11)
ax.annotate('TP = 99', xy=(.005, .52), xytext=(-.15, .52),
            color=TP, fontsize=12, weight='bold', ha='center', va='center',
            annotation_clip=False,
            arrowprops={'arrowstyle': '-', 'color': TP, 'lw': 1.2})
ax.annotate('FN = 1', xy=(.005, .995), xytext=(-.14, .90),
            color=FN, fontsize=10, ha='center', annotation_clip=False,
            arrowprops={'arrowstyle': '-', 'color': FN, 'lw': 1})
ax.annotate('FP = 99', xy=(.65, .005), xytext=(.65, -.17),
            color=FP, fontsize=12, weight='bold', ha='center',
            annotation_clip=False,
            arrowprops={'arrowstyle': '-', 'color': FP, 'lw': 1.2})

fig.text(.59, .71, 'Discard the blue and orange regions.', fontsize=12)
fig.text(.59, .66, 'Green + red = 99 + 99 = 198 positives.', fontsize=12)
bar = fig.add_axes([.59, .45, .36, .13])
bar.axis('off')
bar.add_patch(Rectangle((0, 0), float(precision), 1, facecolor=TP))
bar.add_patch(Rectangle((float(precision), 0), float(1-precision), 1, facecolor=FP))
bar.text(.25, .5, '99 with disease\n50%', color='white', ha='center', va='center',
         fontsize=13, weight='bold', linespacing=1.6)
bar.text(.75, .5, '99 without disease\n50%', color='white', ha='center', va='center',
         fontsize=13, weight='bold', linespacing=1.6)
fig.text(.59, .40, 'New denominator: all 198 positive tests = 100%',
         fontsize=11, color=MUTED)
fig.text(.59, .32, 'PRECISION = 99 / 198 = 50%', fontsize=17, color=TP, weight='bold')

fig.text(.04, .23, 'Width × retained height = joint probability area', fontsize=13, weight='bold')
fig.text(.04, .17, 'Green: 0.01 × 0.99 = 0.0099', fontsize=13, color=TP, weight='bold')
fig.text(.53, .17, 'Red: 0.99 × 0.01 = 0.0099', fontsize=13, color=FP, weight='bold')
fig.text(.04, .10, 'Bayes: posterior = green area / (green area + red area)',
         fontsize=16, weight='bold')
fig.text(.04, .045, 'Left areas are to probability scale. Right bar is renormalized: the retained 1.98% becomes 100%.',
         fontsize=11, color=MUTED)

# Check that all labels lie within the saved figure; inspect the PNG for overlaps.
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
bounds = fig.bbox
for text in fig.findobj(matplotlib.text.Text):
    if not text.get_visible() or not text.get_text():
        continue
    box = text.get_window_extent(renderer)
    assert box.x0 >= -1 and box.y0 >= -1 and box.x1 <= bounds.x1+1 and box.y1 <= bounds.y1+1, text.get_text()

fig.savefig(OUT/'rare-disease-rectangles.svg', metadata={'Date': None})
fig.savefig(OUT/'rare-disease-rectangles.png', dpi=130)
plt.close(fig)
ET.parse(OUT/'rare-disease-rectangles.svg')
assert sha256(original.read_bytes()).hexdigest() == original_hash
report = {
    'status': 'PASS', 'population_size': 10000,
    'counts': {k: int(v) for k, v in counts.items()},
    'exact_population_masses': {k: str(v) for k, v in mass.items()},
    'exact_metrics': {k: str(v) for k, v in metrics.items()},
    'positive_population_mass': str(mass['TP']+mass['FP']),
    'original_factory_precision': '16/25',
    'original_svg_sha256': original_hash,
    'generated_sha256': {
        name: sha256((OUT/name).read_bytes()).hexdigest()
        for name in ['draw_rectangles.py', 'rare-disease-rectangles.svg',
                     'rare-disease-rectangles.png']
    },
    'checks': ['Exact rational count and metric identities',
               'Four rectangle areas partition the unit population',
               'Rendered rectangle areas match joint probabilities',
               'Green and red have equal area; normalized shares sum to one',
               'Posterior null probability is distinct from Type I error',
               'Original factory example gives 64 percent precision',
               'Text remains within figure bounds', 'SVG XML parses',
               'Original ROC-note SVG is byte-unchanged'],
    'limits': 'Hypothetical population. Expected counts are not sample guarantees. '
              'PNG inspection is separate from live Obsidian rendering.'
}
(OUT/'checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2))
