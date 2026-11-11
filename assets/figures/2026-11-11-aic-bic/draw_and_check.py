"""Original deterministic teaching figures. Run with Python + numpy/matplotlib/scipy.
Outputs are written beside this script; no source-vault or raw files are touched.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import quad
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.size': 11, 'svg.fonttype': 'none', 'axes.spines.top': False,
                     'axes.spines.right': False, 'figure.facecolor': '#fafaf7',
                     'axes.facecolor': '#fafaf7'})
blue, orange, gray = '#236a9b', '#b85d22', '#64717a'

def save(fig, name):
    fig.savefig(OUT / (name + '.svg'), bbox_inches='tight')
    fig.savefig(OUT / (name + '.png'), dpi=145, bbox_inches='tight')
    ET.parse(OUT / (name + '.svg'))
    plt.close(fig)

n, h = 100, 60
p_hat = h/n
ll0 = n*np.log(.5)
ll1 = h*np.log(p_hat)+(n-h)*np.log1p(-p_hat)
gain = 2*(ll1-ll0)
assert np.isclose(gain, 4.027102710137775)
aic = np.array([-2*ll0, -2*ll1+2])
bic = np.array([-2*ll0, -2*ll1+np.log(n)])
assert aic.argmin() == 1 and bic.argmin() == 0
assert np.isclose((2/3)**2*(1-2/3), 4/27)

fig, axes = plt.subplots(1, 2, figsize=(11.4, 4), constrained_layout=True)
p = np.linspace(.25, .85, 801)
rel = np.exp(h*np.log(p)+(n-h)*np.log1p(-p)-ll1)
axes[0].plot(p, rel, color=blue, lw=2.5)
axes[0].scatter([.5,.6], [np.exp(ll0-ll1),1], color=[gray,blue], zorder=3)
axes[0].annotate('Fair: p = 0.5', (.5,np.exp(ll0-ll1)), (.29,.40), arrowprops={'arrowstyle':'->','color':gray})
axes[0].annotate('Best fit: p = 0.6', (.6,1), (.34,.91), arrowprops={'arrowstyle':'->','color':blue})
axes[0].set(xlabel='Assumed probability of heads p', ylabel='Likelihood / maximum likelihood',
            title='Same 100 flips: 60 heads, 40 tails', ylim=(0,1.13))
labels = ['Fit only', 'AIC', 'BIC']
free_change = np.array([-gain, -gain+2, -gain+np.log(n)])
axes[1].axhline(0, color=gray, lw=1)
axes[1].bar(labels, free_change, color=[blue, blue, orange], width=.55)
for i,v in enumerate(free_change):
    axes[1].text(i, v + (-.24 if v<0 else .15), f'{v:+.3f}', ha='center', va='top' if v<0 else 'bottom')
axes[1].set(ylabel='Free-p score minus fair-coin score', title='Extra fit versus the parameter penalty', ylim=(-5.1,1.6))
axes[1].text(.03,-.24,'Below zero: free p wins.\nAbove zero: fixed fair coin wins.', transform=axes[1].transAxes, fontsize=10)
save(fig,'01-coin-fit-and-selection')

fig, axes = plt.subplots(1,2,figsize=(11.4,4),constrained_layout=True)
axes[0].bar(['Training', 'Fresh sample'], [19,21], color=[blue,orange], width=.5)
axes[0].set(ylim=(0,25), ylabel='Expected squared-error sum', title='AIC: fitting one mean creates a gap of 2')
axes[0].text(0,19.5,'n − 1 = 19',ha='center')
axes[0].text(1,21.5,'n + 1 = 21',ha='center')
axes[0].text(.03,-.26,'20 independent N(μ, 1) observations.\nFresh data use the TRAINING fitted mean.', transform=axes[0].transAxes, fontsize=10)
t = np.linspace(-1,1,1001)
for nn,c in [(25,blue),(100,orange)]:
    axes[1].plot(t,np.exp(-nn*t*t/2),color=c,lw=2.5,label=f'n = {nn}, width ∝ 1/√{nn}')
axes[1].legend(frameon=False,fontsize=10)
axes[1].set(xlabel='Mean minus fitted mean',ylabel='Likelihood / maximum likelihood', title='BIC: evidence uses height AND width')
axes[1].text(.03,-.26,'Same peak height here; 4× the data\ngives half the area in one dimension.',transform=axes[1].transAxes,fontsize=10)
save(fig,'02-why-penalties-arise')

# Check exact AIC expectation using an orthogonal Gaussian coordinate system:
# n-1 residual coordinates plus the independent fitted-mean coordinate.
rng = np.random.default_rng(1111)
reps, nn = 160000, 20
train_residual_sum = rng.chisquare(nn-1,size=reps)
mean_error = rng.normal(0,1/np.sqrt(nn),size=reps)
expected_fresh_given_mean = nn + nn*mean_error**2
assert abs(train_residual_sum.mean()-(nn-1)) < .06
assert abs(expected_fresh_given_mean.mean()-(nn+1)) < .02
areas = [quad(lambda x: np.exp(-nn*x*x/2), -np.inf,np.inf)[0] for nn in [25,100]]
assert np.isclose(areas[0]/areas[1],2)
# Exact numerical integration against a proper N(0,tau^2) prior checks the
# n^(-1/2) scaling used by the optional BIC argument.
tau, muhat = 2., .3
errs=[]
for nn in [10,100,1000]:
    value=quad(lambda x: np.exp(-nn*(x-muhat)**2/2-x*x/(2*tau*tau))/(np.sqrt(2*np.pi)*tau),-np.inf,np.inf)[0]
    exact=np.exp(-nn*muhat*muhat/(2*(1+nn*tau*tau)))/np.sqrt(1+nn*tau*tau)
    errs.append(abs(value-exact))
assert max(errs)<1e-10
gain80=2*(80*np.log(.8)+20*np.log(.2)-ll0)
assert round(gain80,2)==38.55 and gain80>np.log(100)
report={'coin':{'n':n,'heads':h,'ll_fixed':ll0,'ll_free':ll1,'twice_loglik_gain':gain,'gain_80_heads':gain80,
                'AIC':aic.tolist(),'BIC':bic.tolist()},
        'normal_AIC':{'n':20,'replications':reps,
                      'mean_training_SSE':float(train_residual_sum.mean()),
                      'mean_conditional_fresh_SSE':float(expected_fresh_given_mean.mean()),
                      'exact_expectations':[19,21]},
        'BIC':{'area_ratio_n25_over_n100':areas[0]/areas[1],'max_prior_integral_error':max(errs)},
        'checks':'PASS: coin arithmetic/rankings, exact normal expectations (Monte Carlo support), Gaussian area and proper-prior quadrature, SVG XML',
        'limits':'Numerics support the written identities; they do not prove general asymptotic AIC/BIC validity.'}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
