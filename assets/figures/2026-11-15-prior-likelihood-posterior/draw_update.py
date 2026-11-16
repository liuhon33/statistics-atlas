"""A compact original visual: prior shares, likelihood rates, posterior shares.

Run this file with Python + matplotlib; outputs are written beside the script.
All values are a hypothetical teaching model, not measured clinical test rates.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent
prior = [F(1,100), F(99,100)]
likelihood = [F(99,100), F(1,100)]
weights = [p*l for p,l in zip(prior,likelihood)]
evidence = sum(weights)
posterior = [w/evidence for w in weights]
assert sum(prior) == sum(posterior) == 1
assert weights == [F(99,10000)]*2
assert evidence == F(99,5000)
assert posterior == [F(1,2)]*2
assert posterior[0] > prior[0] and posterior[0] != likelihood[0]
assert prior[0]/prior[1] * likelihood[0]/likelihood[1] == posterior[0]/posterior[1]

GREEN, RED, GRAY = '#168575', '#cc4455', '#e9edf2'
INK, MUTED = '#162b40', '#566778'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12,
                     'text.color':INK, 'svg.fonttype':'none',
                     'svg.hashsalt':'prior-likelihood-posterior-2026-11-15',
                     'savefig.facecolor':'white'})
fig = plt.figure(figsize=(13, 4.8), facecolor='white')
fig.text(.035,.925,'PRIOR × LIKELIHOOD → POSTERIOR',fontsize=23,weight='bold')
fig.text(.035,.855,'Observed data: a positive test (+).  Two possibilities: disease or no disease.',
         fontsize=13,color=MUTED)
fig.text(.035,.745,'1  PRIOR',fontsize=17,weight='bold')
fig.text(.365,.745,'2  LIKELIHOOD',fontsize=17,weight='bold')
fig.text(.745,.745,'3  POSTERIOR',fontsize=17,weight='bold')
fig.text(.035,.685,'Before this test',fontsize=12,color=MUTED)
fig.text(.745,.685,'After a positive test',fontsize=12,color=MUTED)

def stacked_bar(position, shares, colors):
    ax = fig.add_axes(position)
    ax.set(xlim=(0,1),ylim=(0,1))
    ax.axis('off')
    offset = 0.
    for value, color in zip(shares, colors):
        patch=Rectangle((offset,0),float(value),1,facecolor=color,edgecolor='none')
        ax.add_patch(patch)
        assert abs(patch.get_width()-float(value)) < 1e-15
        offset += float(value)
    assert abs(offset-1) < 1e-15
    return ax

left=stacked_bar([.035,.47,.25,.12],prior,[GREEN,RED])
left.text(.505,.5,'99% no disease',ha='center',va='center',color='white',fontsize=13,weight='bold')
left.annotate('1% disease',xy=(.005,0),xytext=(0,-.68),color=GREEN,
              ha='left',fontsize=12,weight='bold',annotation_clip=False,
              arrowprops={'arrowstyle':'-','color':GREEN,'lw':1.2})

fig.text(.365,.655,'If disease: 99% test positive',fontsize=12,color=GREEN)
stacked_bar([.365,.575,.27,.045],[likelihood[0],1-likelihood[0]],[GREEN,GRAY])
fig.text(.365,.485,'If no disease: 1% test positive',fontsize=12,color=RED)
stacked_bar([.365,.405,.27,.045],[likelihood[1],1-likelihood[1]],[RED,GRAY])
fig.text(.365,.335,'Separate groups; gray = negative.',fontsize=10.5,color=MUTED)

right=stacked_bar([.745,.47,.22,.12],posterior,[GREEN,RED])
right.text(.25,.5,'50%',ha='center',va='center',color='white',fontsize=15,weight='bold')
right.text(.75,.5,'50%',ha='center',va='center',color='white',fontsize=15,weight='bold')
fig.text(.745,.35,'Disease       No disease',fontsize=11.5)
fig.text(.315,.51,'×',fontsize=27,ha='center')
fig.text(.69,.52,'→',fontsize=27,ha='center')
fig.text(.69,.39,'weight,\nnormalize',fontsize=10,ha='center',color=MUTED)

fig.text(.035,.205,'Disease weight: 0.01 × 0.99 = 0.0099',fontsize=12.5,color=GREEN,weight='bold')
fig.text(.535,.205,'No-disease weight: 0.99 × 0.01 = 0.0099',fontsize=12.5,color=RED,weight='bold')
fig.text(.035,.105,'Divide each weight by 0.0099 + 0.0099 = 0.0198.  The posterior shares sum to 100%.',
         fontsize=13,weight='bold')

fig.canvas.draw()
renderer=fig.canvas.get_renderer()
for label in fig.findobj(matplotlib.text.Text):
    if label.get_visible() and label.get_text():
        b=label.get_window_extent(renderer)
        assert b.x0 >= -1 and b.y0 >= -1 and b.x1 <= fig.bbox.x1+1 and b.y1 <= fig.bbox.y1+1, label.get_text()
fig.savefig(OUT/'prior-likelihood-posterior.svg',metadata={'Date':None})
fig.savefig(OUT/'prior-likelihood-posterior.png',dpi=130)
plt.close(fig)
ET.parse(OUT/'prior-likelihood-posterior.svg')
report={
    'status':'PASS', 'prior':[str(x) for x in prior],
    'likelihood':[str(x) for x in likelihood], 'joint_weights':[str(x) for x in weights],
    'evidence':str(evidence),'posterior':[str(x) for x in posterior],
    'checks':['Exact fractions and Bayes normalization',
              'Prior and posterior each sum to one',
              'Likelihood bars use separate class-conditional denominators',
              'Each bar segment width equals its stated probability',
              'Posterior is distinct from likelihood',
              'Posterior odds equal prior odds times likelihood ratio',
              'SVG XML parses; all text lies within figure bounds'],
    'sha256':{name:sha256((OUT/name).read_bytes()).hexdigest() for name in
              ['draw_update.py','prior-likelihood-posterior.svg','prior-likelihood-posterior.png']},
    'scope':'Static teaching model. Visual inspection is separate from live Obsidian rendering.'
}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
