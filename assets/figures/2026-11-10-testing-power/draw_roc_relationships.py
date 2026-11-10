"""Coordinated ROC/type-I/type-II/precision illustration (original).
Run with Python, NumPy, SciPy, Matplotlib. All outputs are beside this script.
Illustrative normal score distributions, not empirical observations.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent
TP, TN, FP, FN = '#168575', '#376eae', '#cc4455', '#c68117'
INK, MUTED, LIGHT = '#162b40', '#566778', '#edf2f6'
alpha, power, prevalence, cases = .05, .8, .1, 1000
cutoff = norm.ppf(1-alpha)
delta = cutoff + norm.ppf(power)
fpr, tpr = norm.sf(cutoff), norm.sf(cutoff-delta)
specificity, type_ii = 1-fpr, 1-tpr
counts = dict(TP=cases*prevalence*tpr, FN=cases*prevalence*type_ii,
              FP=cases*(1-prevalence)*fpr, TN=cases*(1-prevalence)*specificity)
precision = counts['TP']/(counts['TP']+counts['FP'])
assert np.allclose([fpr,tpr,specificity,type_ii,precision],[.05,.8,.95,.2,.64])
assert np.allclose([counts[k] for k in ['TP','FN','FP','TN']],[80,20,45,855])
assert abs(sum(counts.values())-cases)<1e-10
thresholds=np.linspace(8,-5,2001)
rx,ry=norm.sf(thresholds),norm.sf(thresholds-delta)
assert np.all(np.diff(rx)>=0) and np.all(np.diff(ry)>=0)
assert np.all(ry>=rx-1e-12)
# Bayes calculation uses class proportions; the ROC uses only conditional laws.
other_prevalence=.01
other_precision=other_prevalence*tpr/(other_prevalence*tpr+(1-other_prevalence)*fpr)
assert other_precision<precision

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,
 'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED,
 'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#aab7c2',
 'svg.fonttype':'none','savefig.facecolor':'white'})
fig=plt.figure(figsize=(16,11),facecolor='white')
fig.text(.05,.965,'ONE TEST, FOUR VIEWS',fontsize=26,weight='bold')
fig.text(.05,.925,'Reject when score S > c.  Same operating point everywhere: Type I = 5%  |  power = 80%.',fontsize=15)
fig.text(.05,.885,'1  A cutoff splits each sampling distribution',fontsize=17,weight='bold')
fig.text(.55,.885,'2  The operating point on an ROC curve',fontsize=17,weight='bold')

xs=np.sort(np.r_[np.linspace(-3.7,6.2,1400),cutoff])
for y,mean,curve,left,right,name,leftlabel,rightlabel in [
 (.71,0,TN,TN,FP,'H₀ true: actually negative','Specificity = 95%','Type I error = 5%'),
 (.535,delta,TP,FN,TP,'H₁ true: actually positive','Type II error = 20%','Sensitivity / power = 80%')]:
 ax=fig.add_axes([.06,y,.37,.115])
 density=norm.pdf(xs-mean)
 ax.fill_between(xs,0,density,where=xs<=cutoff,color=left,alpha=.28)
 ax.fill_between(xs,0,density,where=xs>=cutoff,color=right,alpha=.40)
 ax.plot(xs,density,color=curve,lw=2.4)
 ax.axvline(cutoff,color=INK,lw=1.4,ls='--')
 ax.set(xlim=(-3.7,6.2),ylim=(0,.44),yticks=[],xticks=[0,cutoff,5])
 ax.set_xticklabels(['0','c = 1.645','5'],fontsize=9)
 ax.spines['left'].set_visible(False)
 ax.text(0,1.14,name,transform=ax.transAxes,fontsize=12,weight='bold',color=curve)
 if mean==0:
  ax.text(-2.8,.22,leftlabel,color=left,fontsize=11,weight='bold')
  ax.annotate(rightlabel,xy=(2.1,norm.pdf(2.1)/2),xytext=(2.6,.22),
              color=right,fontsize=11,weight='bold',arrowprops=dict(arrowstyle='->',color=right))
 else:
  ax.annotate(leftlabel,xy=(1.2,norm.pdf(1.2-mean)/2),xytext=(-3.4,.23),
              color=left,fontsize=11,weight='bold',arrowprops=dict(arrowstyle='->',color=left))
  ax.text(2.3,.25,'Sensitivity / power\n= 80%',color=right,fontsize=11,weight='bold')
  ax.set_xlabel('Score S  →  larger scores favor H₁',fontsize=11)

ax=fig.add_axes([.575,.555,.365,.28])
ax.plot(rx,ry,color=INK,lw=2.7,label='Threshold ROC')
ax.plot([0,1],[0,1],color='#bac5ce',ls='--',lw=1.1)
ax.text(.54,.43,'Chance diagonal',color=MUTED,fontsize=10,rotation=29)
ax.axvspan(0,alpha,color=TP,alpha=.08)
ax.axvline(alpha,color=FP,lw=1.3,ls=':')
ax.axhline(tpr,color=TP,lw=.8,ls=':',alpha=.5)
ax.scatter([fpr],[tpr],s=100,color=INK,zorder=10)
ax.annotate('Chosen cutoff\n(FPR, TPR) = (.05, .80)',xy=(fpr,tpr),xytext=(.29,.67),
            fontsize=12,weight='bold',arrowprops=dict(arrowstyle='->',color=INK))
ax.annotate('',xy=(fpr,tpr),xytext=(fpr,0),arrowprops=dict(arrowstyle='<->',color=TP,lw=2))
ax.text(.09,.34,'Sensitivity / recall\n= power = 1 − Type II\n= 80%',color=TP,fontsize=12,weight='bold')
ax.annotate('',xy=(fpr,1),xytext=(fpr,tpr),arrowprops=dict(arrowstyle='<->',color=FN,lw=2))
ax.text(.25,.88,'Type II error\n= 1 − sensitivity = 20%',color=FN,fontsize=11,weight='bold')
ax.annotate('Type I = 5%',xy=(fpr,0),xytext=(.25,.10),fontsize=11,color=FP,
            arrowprops=dict(arrowstyle='->',color=FP))
# A horizontal complement has length 1-FPR, independent of the curve height.
ax.annotate('',xy=(1,-.16),xytext=(fpr,-.16),xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle='<->',color=TN,lw=2),annotation_clip=False)
ax.text(.53,-.245,'Specificity = 1 − FPR = 95%',transform=ax.transAxes,
        ha='center',color=TN,fontsize=11,weight='bold')
ax.set(xlim=(0,1),ylim=(0,1.02),xticks=np.arange(0,1.01,.2),yticks=np.arange(0,1.01,.2))
ax.set_xlabel('False-positive rate = Type I error rate',labelpad=50,fontsize=11)
ax.set_ylabel('True-positive rate = sensitivity = power',fontsize=11)

fig.text(.05,.405,'3  Add a base rate to get expected counts',fontsize=17,weight='bold')
fig.text(.05,.373,'1,000 cases: 100 true alternatives + 900 true nulls (prevalence = 10%).',fontsize=11)
tabax=fig.add_axes([.05,.14,.43,.205]);tabax.axis('off')
table=tabax.table(cellText=[['Reject / positive','TP = 80','FP = 45'],
                          ['Do not reject / negative','FN = 20','TN = 855']],
 colLabels=['Decision','True alternative (100)','True null (900)'],
 cellLoc='center',loc='center',colWidths=[.38,.31,.31])
table.auto_set_font_size(False);table.set_fontsize(11);table.scale(1,2.7)
for (r,c),cell in table.get_celld().items():
 cell.set_edgecolor('white');cell.set_linewidth(3)
 cell.set_facecolor(LIGHT)
 if r==0:cell.set_text_props(weight='bold')
for key,col in [((1,1),TP),((1,2),FP),((2,1),FN),((2,2),TN)]:
 table[key].set_facecolor(col);table[key].set_text_props(color='white',weight='bold',fontsize=15)
fig.text(.06,.115,'Read within TRUE classes:',fontsize=11,weight='bold')
fig.text(.06,.087,'Sensitivity: 80 / 100 = 80%     Specificity: 855 / 900 = 95%',fontsize=11)

fig.text(.55,.405,'4  Precision uses a different denominator',fontsize=17,weight='bold')
fig.text(.55,.369,'Among predicted positives: 80 true positives + 45 false positives = 125',fontsize=11)
barax=fig.add_axes([.55,.265,.39,.070]);barax.axis('off');barax.set(xlim=(0,1),ylim=(0,1))
barax.add_patch(Rectangle((0,0),precision,1,color=TP))
barax.add_patch(Rectangle((precision,0),1-precision,1,color=FP))
barax.text(precision/2,.5,'80 TP',color='white',ha='center',va='center',weight='bold',fontsize=17)
barax.text((1+precision)/2,.5,'45 FP',color='white',ha='center',va='center',weight='bold',fontsize=17)
fig.text(.55,.222,'Precision = TP / (TP + FP) = 80 / 125 = 64%',fontsize=16,weight='bold',color=TP)
fig.text(.55,.175,'Power: P(reject | H₁)        Precision: P(H₁ | reject)',fontsize=12)
fig.text(.55,.125,'Changing prevalence changes precision, not this ROC curve,\nwhen both class-conditional score distributions stay fixed.',fontsize=11,color=MUTED,linespacing=1.6)
fig.text(.05,.032,'Illustrative model: S | H₀ ~ N(0, 1), S | H₁ ~ N(2.486, 1).  Here FPR = α; in general a level-α test only requires FPR ≤ α.',fontsize=10,color=MUTED)

fig.savefig(OUT/'roc-error-rates.svg')
fig.savefig(OUT/'roc-error-rates.png',dpi=125)
plt.close(fig)
ET.parse(OUT/'roc-error-rates.svg')
report=dict(model='Normal scores; common variance 1; simple hypotheses',
 cutoff=float(cutoff),alternative_mean=float(delta),alpha=alpha,
 FPR=float(fpr),TPR=float(tpr),specificity=float(specificity),type_II=float(type_ii),
 prevalence=prevalence,expected_counts=counts,precision=float(precision),
 precision_if_prevalence_001=float(other_precision),
 checks='PASS: complements, Bayes, counts, monotone ROC, above chance, SVG XML')
(OUT/'roc-error-rates-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
