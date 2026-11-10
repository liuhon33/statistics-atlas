"""One rule, two sampling distributions. Run with Python + numpy + matplotlib."""
from pathlib import Path
from statistics import NormalDist
import json
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
alpha = 0.05
normal = NormalDist()
c = normal.inv_cdf(1-alpha)
power = 1-normal.cdf(c-2)
rows = []
for cutoff in [normal.inv_cdf(.975), c, normal.inv_cdf(.9)]:
    rows.append(dict(cutoff=cutoff, false_positive=1-normal.cdf(cutoff),
                     power=1-normal.cdf(cutoff-2)))
assert abs(rows[1]['false_positive']-alpha) < 1e-14
assert rows[0]['power'] < power < rows[2]['power']
assert rows[0]['false_positive'] < alpha < rows[2]['false_positive']
assert abs(power-0.6387600313) < 1e-9

plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12,
                     'svg.fonttype':'none', 'axes.spines.top':False,
                     'axes.spines.right':False})
ink, muted, null_color, alt_color = '#203247','#526477','#C65C25','#008576'
fig = plt.figure(figsize=(10,8.5), facecolor='#FFFFFF')
fig.text(.09,.958,'One decision rule. Two possible worlds.', fontsize=23,
         color=ink, weight='bold')
fig.text(.09,.920,'Illustrative model: X ~ N(θ, 1)     •     θ₀ = 0, θ₁ = 2     •     α = 0.05',
         color=muted, fontsize=12)

left, right = -3.4, 5.4
strip = fig.add_axes([.10,.785,.83,.095])
strip.set_xlim(left,right); strip.set_ylim(0,1); strip.axis('off')
strip.axvspan(left,c,facecolor='#E9EDF1')
strip.axvspan(c,right,facecolor='#D6EDE8')
strip.axvline(c,color=ink,lw=1.6,ls='--')
strip.text((left+c)/2,.64,'Fail to reject',ha='center',color=ink,weight='bold')
strip.text((left+c)/2,.24,'φ(x) = 0   for x ≤ c',ha='center',color=ink)
strip.text((c+right)/2,.64,'Reject',ha='center',color=ink,weight='bold')
strip.text((c+right)/2,.24,'φ(x) = 1   for x > c',ha='center',color=ink)

x = np.linspace(left,right,1200)
tail = np.linspace(c,right,600)
for y0,mu,color,title,area in [
    (.485,0,null_color,'If the null is true:  X ~ N(0, 1)', 'False-positive area = 0.050 = α'),
    (.190,2,alt_color,'If the alternative is true:  X ~ N(2, 1)',f'Power area = {power:.3f}')]:
    ax=fig.add_axes([.10,y0,.83,.205])
    ax.set_xlim(left,right); ax.set_ylim(0,.49)
    ax.axvspan(c,right,color='#F2F5F6',zorder=0)
    density=lambda z: np.exp(-.5*(z-mu)**2)/np.sqrt(2*np.pi)
    ax.fill_between(tail,0,density(tail),color=color,alpha=.32)
    ax.plot(x,density(x),color=color,lw=2.8)
    ax.axvline(c,color=ink,lw=1.5,ls='--')
    ax.set_title(title,loc='left',pad=13,color=ink,weight='bold',fontsize=13)
    ax.set_ylabel('Density',color=muted)
    ax.set_yticks([0,.2,.4]); ax.set_xticks([-2,0,c,4])
    ax.set_xticklabels(['−2','0','c = 1.645','4'])
    ax.tick_params(colors=muted,labelsize=11)
    ax.spines['left'].set_color('#B1BAC2'); ax.spines['bottom'].set_color('#B1BAC2')
    ax.text(.985,.84,area,ha='right',transform=ax.transAxes,color=ink,fontsize=12,
            bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=3))
    ax.text(1.01,-.01,'x',transform=ax.transAxes,color=ink)

fig.text(.10,.097,'Lower c → larger rejection region → more power AND more false positives.',
         fontsize=12,color=ink)
fig.text(.10,.054,'Best feasible cutoff among upper-tail rules: c = 1.645 (the 5% budget is used).',
         fontsize=12,color=ink,weight='bold')
fig.savefig(OUT/'decision-rule-two-worlds.png',dpi=170,facecolor=fig.get_facecolor())
fig.savefig(OUT/'decision-rule-two-worlds.svg',facecolor=fig.get_facecolor(),metadata={'Date':None})
plt.close(fig)
ET.parse(OUT/'decision-rule-two-worlds.svg')
(OUT/'decision-rule-checks.json').write_text(json.dumps({
    'model':'X ~ N(theta, 1); theta0=0, theta1=2; reject X>c',
    'alpha':alpha,'cutoff':c,'power':power,'cutoff_comparison':rows,
    'checks':'normal-tail calibration, monotone tradeoff, SVG XML: PASS'
},indent=2)+'\n',encoding='utf-8')
print(f'PASS: c={c:.9f}; null tail={alpha:.9f}; power={power:.9f}; SVG parses')
