"""Original ELBO teaching figures. Run with Python + numpy + matplotlib.

Outputs are written beside this script, independent of working directory.
The binary model and all displayed quantities are checked by enumeration.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
TEAL, ORANGE, PURPLE, INK = '#087e8b', '#c76824', '#7856a6', '#23354b'
plt.rcParams.update({'font.size': 12, 'text.color': INK, 'axes.labelcolor': INK,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'svg.fonttype': 'none', 'savefig.facecolor': 'white'})
prior = np.array([.5, .5])
likelihood = np.array([.8, .2])
joint = prior * likelihood
evidence = joint.sum()
posterior = joint / evidence

def quantities(r):
    q = np.array([r, 1-r])
    fit = float(q @ np.log(likelihood))
    prior_kl = float(q @ np.log(q/prior))
    posterior_kl = float(q @ np.log(q/posterior))
    elbo = float(q @ np.log(joint/q))
    weights = joint/q
    assert np.isclose(elbo, fit-prior_kl, atol=1e-12)
    assert np.isclose(np.log(evidence)-elbo, posterior_kl, atol=1e-12)
    assert np.isclose(q @ weights, evidence, atol=1e-12)
    assert elbo <= np.log(evidence)+1e-12
    return dict(r=float(r), fit=fit, prior_kl=prior_kl,
                posterior_kl=posterior_kl, elbo=elbo, weights=weights.tolist())

grid = np.linspace(.001, .999, 999)
rows = [quantities(r) for r in grid]
examples = [quantities(r) for r in (.5,.7,.8)]
assert np.isclose(quantities(.8)['posterior_kl'], 0)
assert np.allclose(quantities(.8)['weights'], [.5,.5])

def save(fig, name):
    for ext in ('svg','png'):
        fig.savefig(OUT/f'{name}.{ext}', dpi=165, bbox_inches='tight')
    plt.close(fig)

fig, ax = plt.subplots(1,2,figsize=(11.5,4.5), gridspec_kw={'width_ratios':[1,1.2]})
fig.suptitle('A better distribution over hidden causes raises the ELBO', weight='bold', y=1.03)
x = np.arange(2)
for offset, vals, color, label in [(-.24, [.5,.5], TEAL, 'Candidate q: 50 / 50'),
                                  (0,[.7,.3], PURPLE,'Candidate q: 70 / 30'),
                                  (.24,[.8,.2],ORANGE,'Exact posterior: 80 / 20')]:
    bars=ax[0].bar(x+offset,vals,.23,color=color,label=label)
    ax[0].bar_label(bars,fmt='%.1f',padding=3,fontsize=10)
ax[0].set(xticks=x,xticklabels=['Rain','Sprinkler'],ylim=(0,1.05),ylabel='Probability after seeing wet ground')
ax[0].legend(fontsize=9,frameon=False,loc='upper right')
ax[0].set_title('Same observation, different q')
ax[1].axhline(np.log(.5),color=ORANGE,ls='--',label='Log evidence = −0.693')
scores=[r['elbo'] for r in examples]
ax[1].plot(range(3),scores,'o-',color=TEAL,lw=2,ms=9,label='ELBO (higher is better)')
for i,y in enumerate(scores):
    ax[1].text(i,y-.035,f'{y:.3f}',ha='center',va='top')
ax[1].annotate('',xy=(0,np.log(.5)),xytext=(0,scores[0]),arrowprops=dict(arrowstyle='<->',color=PURPLE))
ax[1].text(.12,-.79,'gap = 0.223',color=PURPLE,fontsize=11)
ax[1].set(xticks=range(3),xticklabels=['50 / 50','70 / 30','80 / 20'],ylim=(-1.03,-.56),xlim=(-.3,2.3),ylabel='Score (nats)',xlabel='Candidate probabilities: rain / sprinkler')
ax[1].legend(fontsize=9,frameon=False,loc='upper left')
fig.tight_layout()
save(fig,'bound-and-posterior')

fig, ax=plt.subplots(figsize=(10,4.8))
ax.plot(grid,[r['fit'] for r in rows],color=TEAL,lw=2,label='Expected log likelihood (data fit)')
ax.plot(grid,[-r['prior_kl'] for r in rows],color=PURPLE,lw=2,label='Negative prior KL')
ax.plot(grid,[r['elbo'] for r in rows],color=ORANGE,lw=3,label='Their sum: ELBO')
ax.axvline(.5,color=INK,ls=':',alpha=.5)
ax.axvline(.8,color=INK,ls=':',alpha=.5)
opt=quantities(.8)
ax.scatter([.8],[opt['elbo']],s=70,color=ORANGE,zorder=4)
ax.annotate('Best ELBO at r = 0.8\nPrior KL = 0.193, not zero',xy=(.8,opt['elbo']),xytext=(.57,-1.35),arrowprops=dict(arrowstyle='->',color=INK),fontsize=11)
ax.text(.49,-1.7,'q = prior',ha='right',fontsize=10)
ax.set(xlim=(0,1),ylim=(-2.35,.1),xlabel='r = q(rain | wet ground)',ylabel='Contribution (nats)',title='Fit and prior regularization must be optimized together')
ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=3,fontsize=9,frameon=False)
fig.tight_layout()
save(fig,'fit-versus-prior')

# Independently verify the reused path figure's row normalization and gap.
forward=np.array([[.36,.24,.08,.12],[.03,.02,.06,.09]])
reverse=np.array([[.212,.188,.212,.188],[.053,.047,.053,.047]])
assert np.allclose(forward.sum(axis=1),[.8,.2])
assert np.allclose(reverse.sum(axis=1),[.8,.2])
qa,pa=forward[0]/.8,reverse[0]/.8
path_gap=float(qa @ np.log(qa/pa))
assert np.isclose(path_gap,.146744026984539,atol=1e-6)
report={'model':{'prior':prior.tolist(),'likelihood':likelihood.tolist(),
                 'joint':joint.tolist(),'evidence':float(evidence),'posterior':posterior.tolist()},
        'examples':examples,'grid_points_checked':len(grid),
        'reused_path_A_posterior_KL':path_gap,
        'checks':'PASS: normalization, both ELBO identities, bound, importance weights, equality, reused path figure'}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
