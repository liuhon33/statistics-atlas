"""Original toy data and static figures. Run with Python, numpy, matplotlib, sklearn.
Outputs are restricted to this script's directory. No external data are used.
"""
from pathlib import Path
from itertools import product, combinations
import json
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.metrics import roc_auc_score, roc_curve

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.size': 12, 'svg.fonttype': 'none', 'figure.facecolor': '#fafbf d'.replace(' ', '')})
GREEN, ORANGE, BLUE = '#187a62', '#b44b24', '#3367a6'
def save(fig, name):
    fig.savefig(OUT / (name + '.svg'), bbox_inches='tight')
    fig.savefig(OUT / (name + '.png'), dpi=145, bbox_inches='tight')
    ET.parse(OUT / (name + '.svg'))
    plt.close(fig)

def binary_c(pos, neg):
    return np.mean([float(p > n) + .5 * float(p == n) for p in pos for n in neg])

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.set(xlim=(-1.4, 2.2), ylim=(-.55, 2.65))
ax.axis('off')
ax.text(.3, 2.4, 'Did the failed machine get the higher score?', ha='center', weight='bold')
for j, lab in enumerate(['C: no failure\nscore 0.6', 'D: no failure\nscore 0.2']):
    ax.text(j + .5, 2.03, lab, ha='center', va='bottom')
for i, (lab, p) in enumerate([('A: failed\nscore 0.9', .9), ('B: failed\nscore 0.4', .4)]):
    y = 1-i
    ax.text(-.12, y+.5, lab, ha='right', va='center')
    for j, n in enumerate([.6,.2]):
        win = p > n
        ax.add_patch(Rectangle((j,y),1,1,facecolor=GREEN if win else ORANGE,edgecolor='white',lw=3))
        ax.text(j+.5,y+.5,('Correct\n1' if win else 'Reversed\n0'),ha='center',va='center',color='white',weight='bold')
ax.text(1, -.32, 'C = (1 + 1 + 0 + 1) / 4 = 0.75', ha='center', weight='bold')
save(fig, '01-pair-grid')

fig, ax = plt.subplots(figsize=(9,4.4))
times, event, risk = [2,4,6,8], [True,False,True,True], [.9,.8,.3,.6]
for i,(t,e,r) in enumerate(zip(times,event,risk)):
    y = 3-i
    ax.plot([0,t],[y,y],color=BLUE,lw=3)
    if e:
        ax.scatter(t,y,color=BLUE,s=85,zorder=3)
        ax.text(t+.15,y+.16,'failure',fontsize=11)
    else:
        ax.scatter(t,y,marker='|',s=180,color=ORANGE)
        ax.annotate('',xy=(8.8,y),xytext=(t,y),arrowprops=dict(arrowstyle='->',color=ORANGE,lw=2,linestyle='--'))
        ax.text(4.3,y+.17,'not observed: failure time unknown',color=ORANGE,fontsize=10)
ax.set(yticks=[3,2,1,0],yticklabels=['A  risk 0.9','B  risk 0.8','C  risk 0.3','D  risk 0.6'],xlabel='Months from the common starting point',xlim=(0,9),ylim=(-.5,3.6))
ax.set_title('Censoring removes unknown comparisons, not incorrect ones',pad=14)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='x',alpha=.2)
save(fig,'02-survival-pairs')

y, score = [1,1,0,0], [.9,.4,.6,.2]
fpr,tpr,_ = roc_curve(y,score,drop_intermediate=False)
fig, ax = plt.subplots(figsize=(6.8,5.5))
ax.add_patch(Rectangle((0,0),.5,.5,facecolor=BLUE,alpha=.22))
ax.add_patch(Rectangle((.5,0),.5,1,facecolor=GREEN,alpha=.22))
ax.plot(fpr,tpr,'o-',color=BLUE,lw=2.5)
ax.text(.25,.25,'area = 1/4',ha='center')
ax.text(.75,.48,'area = 1/2',ha='center')
for x,z,lab,off in [(0,.5,'A enters',(12,10)),(.5,.5,'C enters',(10,-22)),(.5,1,'B enters',(-70,10)),(1,1,'D enters',(-53,-24))]:
    ax.annotate(lab,(x,z),xytext=off,textcoords='offset points',fontsize=10)
ax.set(xlim=(-.04,1.04),ylim=(-.04,1.1),xlabel='False-positive rate',ylabel='True-positive rate',xticks=[0,.5,1],yticks=[0,.5,1])
ax.set_title('Same four pairs, viewed as ROC area\nAUROC = 1/4 + 1/2 = 0.75',pad=14)
ax.spines[['top','right']].set_visible(False)
save(fig,'03-roc-area')

assert binary_c([.9,.4],[.6,.2]) == .75
assert binary_c([.9,.6],[.6,.2]) == .875
assert roc_auc_score(y,score) == .75
pairs = []
for i,j in combinations(range(4),2):
    if event[i] and times[i] < times[j]:
        pairs.append((i,j,float(risk[i]>risk[j]) + .5*float(risk[i]==risk[j])))
assert pairs == [(0,1,1.),(0,2,1.),(0,3,1.),(2,3,0.)]
assert sum(p[2] for p in pairs)/len(pairs) == .75
# Exhaustive score ties: 3 positive and 3 negative observations, each score in {0,1,2}.
max_error=0.
for s in product(range(3), repeat=6):
    c=binary_c(s[:3],s[3:])
    auc=roc_auc_score([1,1,1,0,0,0],s)
    block_area=0.
    for v in set(s):
        a=sum(x==v for x in s[:3]); b=sum(x==v for x in s[3:]); A=sum(x>v for x in s[:3])
        block_area += (A*b + .5*a*b)/9
    max_error=max(max_error,abs(c-auc),abs(c-block_area))
assert max_error < 1e-12
(OUT/'checks.json').write_text(json.dumps({'binary_C':.75,'tied_binary_C':.875,'survival_C':.75,'survival_comparable_pairs':pairs,'exhaustive_tie_cases':729,'max_auc_pair_block_error':max_error,'svg_parse':'PASS','scope':'Distinct survival times; no software survival API execution. Numerical checks support the analytic proof.'},indent=2)+'\n',encoding='utf-8')
print('PASS: toy examples, 729 tie cases, and three SVG parses')
