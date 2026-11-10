"""Original area diagram: joint population mass versus ROC area.
Same normal-score model and operating point as draw_roc_relationships.py.
Run with Python + numpy + scipy + matplotlib. Outputs beside this script.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import numpy as np
from scipy.stats import norm
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT=Path(__file__).resolve().parent
TP,TN,FP,FN='#168575','#376eae','#cc4455','#c68117'
INK,MUTED='#162b40','#566778'
AUC_COLOR='#7658a3'
pi,alpha,power=.1,.05,.8
c=norm.ppf(.95);delta=c+norm.ppf(.8)
areas=dict(TP=pi*power,FN=pi*(1-power),FP=(1-pi)*alpha,TN=(1-pi)*(1-alpha))
precision=areas['TP']/(areas['TP']+areas['FP'])
npv=areas['TN']/(areas['TN']+areas['FN'])
accuracy=areas['TP']+areas['TN']
auc=norm.cdf(delta/np.sqrt(2))
def roc(u):
    if u<=0:return 0.
    if u>=1:return 1.
    return float(norm.sf(norm.isf(u)-delta))
auc_quad,err=quad(roc,0,1,epsabs=1e-11,epsrel=1e-11)
partial,_=quad(roc,0,alpha,epsabs=1e-11)
weighted_tails=[quad(lambda s:pi*norm.pdf(s-delta),c,np.inf)[0],
                quad(lambda s:(1-pi)*norm.pdf(s),c,np.inf)[0]]
assert np.allclose([areas[k] for k in ['TP','FN','FP','TN']],[.08,.02,.045,.855])
assert abs(sum(areas.values())-1)<1e-12
assert np.allclose(weighted_tails,[areas['TP'],areas['FP']])
assert abs(precision-.64)<1e-12 and abs(accuracy-.935)<1e-12
assert abs(auc-auc_quad)<1e-10
assert partial<alpha*power

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':INK,
 'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED,
 'svg.fonttype':'none','savefig.facecolor':'white'})
fig=plt.figure(figsize=(15,10),facecolor='white')
fig.text(.05,.955,'TWO KINDS OF AREA — TWO DIFFERENT QUESTIONS',fontsize=23,weight='bold')
fig.text(.05,.915,'Same classifier: FPR = 5%, power = 80%.  Population prevalence = 10%.',fontsize=14)
fig.text(.05,.858,'A  Population area: precision is a ratio',fontsize=17,weight='bold')
fig.text(.55,.858,'B  ROC area: AUC measures ranking',fontsize=17,weight='bold')

# Mosaic: width is prior class mass; height is a class-conditional decision rate.
ax=fig.add_axes([.075,.445,.385,.34])
ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
for xy,w,h,color in [((0,0),pi,power,TP),((0,power),pi,1-power,FN),
                     ((pi,0),1-pi,alpha,FP),((pi,alpha),1-pi,1-alpha,TN)]:
 ax.add_patch(Rectangle(xy,w,h,facecolor=color,edgecolor='white',lw=2))
ax.add_patch(Rectangle((0,0),1,1,fill=False,edgecolor=INK,lw=1.3))
ax.text(pi/2,power/2,'TP = 8%',color='white',ha='center',va='center',rotation=90,weight='bold',fontsize=12)
ax.text(pi/2,.9,'FN\n2%',color='white',ha='center',va='center',weight='bold',fontsize=10)
ax.text(.55,.55,'TN = 85.5%\ncorrect negatives',color='white',ha='center',va='center',fontsize=18,weight='bold')
ax.text(.55,.025,'FP = 4.5%',color='white',ha='center',va='center',fontsize=8,weight='bold')
ax.annotate('True alternatives: 10%',xy=(.05,1),xytext=(.06,1.12),
            fontsize=11,ha='center',arrowprops=dict(arrowstyle='-',color=INK),annotation_clip=False)
ax.text(.55,1.12,'True nulls: 90%',ha='center',fontsize=11)
ax.annotate('',xy=(-.025,.8),xytext=(-.025,0),xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle='<->',color=TP,lw=1.4),annotation_clip=False)
ax.text(-.075,.4,'80% of positives',transform=ax.transAxes,rotation=90,ha='center',va='center',fontsize=10,color=TP)
ax.text(.5,-.09,'Whole rectangle = 100% of the population',transform=ax.transAxes,ha='center',fontsize=11)

# Condition on predicted positive: remove TN and FN; rescale remaining mass.
fig.text(.05,.365,'Keep only the green + red areas (all rejections):',fontsize=12,weight='bold')
bar=fig.add_axes([.075,.287,.385,.052]);bar.axis('off')
bar.add_patch(Rectangle((0,0),precision,1,color=TP))
bar.add_patch(Rectangle((precision,0),1-precision,1,color=FP))
bar.text(precision/2,.5,'TP: 64%',color='white',ha='center',va='center',weight='bold')
bar.text((1+precision)/2,.5,'FP: 36%',color='white',ha='center',va='center',weight='bold')
fig.text(.05,.243,'Precision = green / (green + red)',color=TP,fontsize=15,weight='bold')
fig.text(.05,.207,'= 0.080 / (0.080 + 0.045) = 64%',fontsize=14)
fig.text(.05,.170,'The bar renormalizes the 12.5% rejected to 100%.',fontsize=10,color=MUTED)

rx=np.unique(np.r_[np.linspace(0,1,1001),np.geomspace(1e-7,.1,500),alpha])
ry=np.array([roc(x) for x in rx])
ax=fig.add_axes([.585,.445,.36,.34])
ax.fill_between(rx,0,ry,color=AUC_COLOR,alpha=.23)
ax.fill_between(rx,ry,1,color='#aebbc5',alpha=.12)
ax.plot(rx,ry,color=INK,lw=2.5)
ax.plot([0,1],[0,1],ls='--',color='#aebbc5',lw=1)
ax.plot([alpha,alpha,0],[0,power,power],ls=':',color=INK,lw=1)
ax.scatter([alpha],[power],s=70,color=INK,zorder=5)
ax.annotate('One cutoff: (.05, .80)',xy=(alpha,power),xytext=(.25,.70),fontsize=11,
            arrowprops=dict(arrowstyle='->',color=INK))
ax.text(.54,.42,f'Shaded ROC area\nAUC = {auc:.4f}',ha='center',va='center',color=AUC_COLOR,fontsize=18,weight='bold')
ax.set(xlim=(0,1),ylim=(0,1),xlabel='False-positive rate',ylabel='True-positive rate / power',
       xticks=np.arange(0,1.01,.2),yticks=np.arange(0,1.01,.2))
ax.spines[['top','right']].set_visible(False)
fig.text(.55,.365,'Randomly draw one positive and one negative:',fontsize=12,weight='bold')
fig.text(.55,.320,f'AUC = P(score⁺ > score⁻) = {auc*100:.2f}%',fontsize=15,color=AUC_COLOR,weight='bold')
fig.text(.55,.270,'This summarizes the entire threshold curve.',fontsize=12)
fig.text(.55,.230,'It is NOT precision, accuracy, or power at one cutoff.',fontsize=11,weight='bold')
fig.text(.55,.185,'The small area above the ROC is ranking error,\nnot Type I or Type II error at the selected cutoff.',fontsize=11,color=MUTED,linespacing=1.5)

fig.text(.05,.105,'Other population-area readouts',fontsize=12,weight='bold')
fig.text(.05,.068,'Accuracy = TP + TN = 93.5%     |     Negative predictive value = TN / (TN + FN) = 97.71%',fontsize=12)
fig.text(.05,.025,'Class-conditional densities each integrate to 1. Weight them by prevalence first: green tail = π·TPR; red tail = (1−π)·FPR.',fontsize=10,color=MUTED)
fig.savefig(OUT/'precision-population-area-vs-auc.svg')
fig.savefig(OUT/'precision-population-area-vs-auc.png',dpi=125)
plt.close(fig)
ET.parse(OUT/'precision-population-area-vs-auc.svg')
report=dict(prevalence=pi,cutoff=float(c),alternative_mean=float(delta),
 population_areas=areas,precision=precision,accuracy=accuracy,NPV=npv,
 AUC_analytic=float(auc),AUC_quadrature=auc_quad,AUC_abs_error=abs(auc-auc_quad),
 partial_AUC_0_to_alpha=partial,weighted_tail_integrals=weighted_tails,
 checks='PASS: mosaic areas sum to 1; class weighting; precision; accuracy; NPV; normal-score AUC vs quadrature; SVG XML')
(OUT/'precision-areas-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
