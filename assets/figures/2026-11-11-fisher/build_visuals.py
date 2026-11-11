"""Build self-contained offline HTML, original SVG/PNG figures, and numerical checks.
Run with Python + NumPy, SciPy, Matplotlib. No network dependencies or source images.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

HERE=Path(__file__).resolve().parent
BG='#101820'; PANEL='#15232e'; FG='#e6edf3'; MUTED='#adbfcd'
GREEN='#71d6ae'; BLUE='#75bfff'; RED='#f99b91'; GOLD='#f3cf78'
plt.rcParams.update({'figure.facecolor':BG,'axes.facecolor':PANEL,'axes.edgecolor':'#466276','text.color':FG,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED,'font.size':10,'svg.fonttype':'none'})

def html():
    css=(HERE/'explorer.css').read_text(encoding='utf-8')
    js=(HERE/'math.js').read_text(encoding='utf-8')+'\n'+(HERE/'explorer.js').read_text(encoding='utf-8')
    for mode in ('1d','2d'):
        content=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'"><title>Fisher information · {mode.upper()}</title><style>{css}</style></head><body data-mode="{mode}"><main></main><script>{js}</script></body></html>'''
        (HERE/f'fisher-{mode}.html').write_text(content,encoding='utf-8')

def style(ax):
    ax.grid(alpha=.15); ax.spines[['top','right']].set_visible(False)

def one_d():
    rng=np.random.default_rng(20261111); ys=5+rng.normal(size=512); mu=np.linspace(-6,16,400)
    fig,axs=plt.subplots(3,2,figsize=(11,8),gridspec_kw={'width_ratios':[1.25,1]},layout='constrained')
    fig.suptitle('One parameter, six views: normal mean, σ = 1, μ* = μ₀ = 5',fontsize=16)
    log=lambda y,m:-.5*np.log(2*np.pi)-.5*(y-m)**2
    for y in ys[::22]:
        axs[0,0].plot(mu,mu*0-1,color=RED,alpha=.25,lw=.8)
        axs[1,0].plot(mu,y-mu,color=BLUE,alpha=.35,lw=.8)
        axs[2,0].plot(mu,log(y,mu),color=GREEN,alpha=.4,lw=.8)
    for ax,title,lim in zip(axs[:,0],['1 · Curvature h = −1/σ²','3 · Score s = (y − μ)/σ²','5 · Log likelihood ℓ'],[(-1.8,.1),(-10,10),(-20,0)]):
        ax.axvline(5,color=GOLD,ls='--'); ax.set(title=title,xlabel='candidate mean μ',xlim=(-6,16),ylim=lim)
    axs[0,1].vlines(-1,0,1,color=RED,lw=3);axs[0,1].plot(-1,1,'o',color=RED)
    axs[0,1].set(title='2 · Point mass at h = −1',xlabel='curvature h',ylabel='probability mass',xlim=(-1.8,.1),ylim=(0,1.2))
    scores=ys-5;axs[1,1].hist(scores,bins=24,density=True,color=BLUE,alpha=.5)
    x=np.linspace(-4,4,200);axs[1,1].plot(x,np.exp(-x*x/2)/np.sqrt(2*np.pi),color=FG)
    axs[1,1].set(title='4 · Scores: variance = I = 1',xlabel='score s',ylabel='density',xlim=(-4,4))
    axs[2,1].hist(log(ys,5),bins=25,density=True,color=GREEN,alpha=.6)
    axs[2,1].set(title='6 · Log-likelihood values',xlabel='log likelihood ℓ',ylabel='density')
    for ax in axs.flat:style(ax)
    for ext in ('svg','png'):fig.savefig(HERE/f'six-panels.{ext}',dpi=150)
    plt.close(fig)

def two_d():
    S=np.array([[4.,3.],[3.,4.]]);I=np.linalg.inv(S);rng=np.random.default_rng(20261111)
    y=rng.multivariate_normal([0,0],S,240);scores=y@I;fig,axs=plt.subplots(1,3,figsize=(13,4.8),layout='constrained')
    fig.suptitle('Reciprocal geometry: data covariance Σ, score covariance I = Σ⁻¹, mean covariance Σ/n',fontsize=14)
    for p in y[:18]:axs[0].add_patch(Ellipse(p,2*np.sqrt(7),2,angle=45,facecolor='none',edgecolor=GREEN,alpha=.5,lw=.8))
    axs[0].scatter(y[:18,0],y[:18,1],s=10,color=GREEN)
    axs[0].quiver(np.zeros(18),np.zeros(18),scores[:18,0],scores[:18,1],color=BLUE,angles='xy',scale_units='xy',scale=2,width=.004)
    axs[0].set(title='Likelihood contours + 0.5 × score',xlabel='mean μ₁',ylabel='mean μ₂')
    axs[1].hist2d(scores[:,0],scores[:,1],bins=28,range=[[-4,4],[-4,4]],cmap='Blues',cmin=1)
    axs[1].add_patch(Ellipse((0,0),2/np.sqrt(7),2,angle=45,facecolor='none',edgecolor=BLUE,lw=2))
    axs[1].set(title='Score cloud is wide along (1, −1)',xlabel='score s₁',ylabel='score s₂')
    axs[2].add_patch(Ellipse((0,0),2*np.sqrt(7/10),2/np.sqrt(10),angle=45,facecolor='none',edgecolor=GOLD,lw=2))
    axs[2].set(title='Mean error is narrow along (1, −1)',xlabel='mean error δ₁',ylabel='mean error δ₂')
    for j,ax in enumerate(axs):
        lim=8 if j==0 else 4 if j==1 else 1.5
        ax.plot([-lim,lim],[lim,-lim],ls='--',color=GOLD,alpha=.7)
        ax.plot(0,0,'o',color=FG,ms=3);ax.set(xlim=(-lim,lim),ylim=(-lim,lim),aspect='equal');style(ax)
    fig.get_layout_engine().set(rect=(0,.09,1,.91))
    fig.text(.5,.015,'Unit Mahalanobis contours (not 95% regions). n = 10 in the last panel. Axes are equal within each panel; limits differ across panels.',ha='center',color=MUTED,fontsize=9)
    for ext in ('svg','png'):fig.savefig(HERE/f'two-dimensional.{ext}',dpi=150)
    plt.close(fig)

def checks():
    result={'normal':[],'logistic':[]}
    for sig in [1,2.5,5]:
        density=lambda y:np.exp(-.5*((y-5)/sig)**2)/(sig*np.sqrt(2*np.pi))
        score=lambda y:(y-5)/sig**2
        es=quad(lambda y:score(y)*density(y),-np.inf,np.inf)[0]
        es2=quad(lambda y:score(y)**2*density(y),-np.inf,np.inf)[0]
        expected=1/sig**2
        assert abs(es)<1e-10 and abs(es2-expected)<1e-9
        result['normal'].append({'sigma':sig,'E_score':es,'E_score_squared':es2,'negative_E_hessian':expected})
        # U = logistic CDF(Y) is uniform; this avoids tail overflow in quadrature.
        b=sig*np.sqrt(3)/np.pi
        es=quad(lambda u:(2*u-1)/b,0,1)[0]
        es2=quad(lambda u:((2*u-1)/b)**2,0,1)[0]
        neg_h=quad(lambda u:2*u*(1-u)/b**2,0,1)[0]
        assert abs(es)<1e-10 and abs(es2-1/(3*b*b))<1e-10 and abs(es2-neg_h)<1e-10
        result['logistic'].append({'sigma':sig,'scale':b,'E_score':es,'E_score_squared':es2,'negative_E_hessian':neg_h})
    S=np.array([[4.,3.],[3.,4.]]);I=np.linalg.inv(S)
    assert np.allclose(I@S@I,I) and np.allclose(np.linalg.eigvalsh(I),[1/7,1])
    for angle in np.linspace(0,np.pi,25):
        v=np.array([np.cos(angle),np.sin(angle)])
        radius=1/np.sqrt(10*v@I@v); assert abs((radius*v)@(10*I)@(radius*v)-1)<1e-12
    result['two_d']={'Sigma':S.tolist(),'I':I.tolist(),'score_covariance_error':float(np.max(abs(I@S@I-I))),'eigenvalues_I':np.linalg.eigvalsh(I).tolist()}
    result['off_truth_normal']={'mu_star':5,'mu0':6,'sigma':1,'mean_score':-1,'variance_score':1,'second_moment_score':2,'negative_expected_hessian':1}
    result['status']='PASS; quadrature supports the analytic proofs in the note.'
    (HERE/'checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(result['status'])

if __name__=='__main__':html();checks();one_d();two_d()
