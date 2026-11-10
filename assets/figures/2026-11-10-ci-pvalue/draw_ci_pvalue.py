"""Original test-inversion illustrations; run with NumPy, SciPy, Matplotlib, Pillow.

The normal mean example has KNOWN SE 0.1 and observed mean 0.2.
Animation changes only the candidate null mean, not the data or the true mean.
"""
from pathlib import Path
import json
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

OUT=Path(__file__).resolve().parent
BLUE='#2771b5'; GREEN='#247c64'; RED='#c34b51'; INK='#243447'; GRAY='#677789'
SE=.1; OBS=.2; ALPHA=.05; CRIT=stats.norm.ppf(1-ALPHA/2)
LOW=OBS-CRIT*SE; HIGH=OBS+CRIT*SE
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none',
 'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})

def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight')
    fig.savefig(OUT/(name+'.png'),dpi=150,bbox_inches='tight')

def belt():
    fig,axs=plt.subplots(1,2,figsize=(12,5.7))
    fig.subplots_adjust(top=.76,bottom=.22,wspace=.32)
    fig.suptitle('One acceptance band, two ways to read it',fontsize=20,color=INK,y=.97)
    fig.text(.5,.875,'Known-SE normal mean: keep pairs satisfying |observed mean - candidate mean| <= 1.96 x 0.1',ha='center',fontsize=11)
    b=np.linspace(-.4,.7,400)
    for ax in axs:
        ax.fill_between(b,b-CRIT*SE,b+CRIT*SE,color=GREEN,alpha=.15)
        ax.plot(b,b-CRIT*SE,color=GREEN,lw=1);ax.plot(b,b+CRIT*SE,color=GREEN,lw=1)
        ax.plot(b,b,color=GRAY,ls=':',lw=.8)
        ax.set(xlim=(-.35,.65),ylim=(-.35,.65),xlabel=r'Candidate null mean $b$',ylabel=r'Possible observed mean $m$')
        ax.set_aspect('equal')
    a=axs[0];a.set_title('TEST: fix a null, vary possible data',fontsize=12,pad=14)
    a.axvline(0,color=BLUE,ls='--',lw=1)
    a.plot([0,0],[-CRIT*SE,CRIT*SE],color=BLUE,lw=5,solid_capstyle='round')
    a.scatter([0],[OBS],color=RED,s=65,zorder=5)
    a.annotate('Observed 0.2\njust outside',xy=(0,OBS),xytext=(-.29,.40),arrowprops={'arrowstyle':'->','color':RED},color=RED)
    a.text(.08,-.20,'At b = 0:\n95% of null sample means\nfall on the blue segment.',fontsize=10,color=BLUE,bbox={'facecolor':'white','alpha':.85,'edgecolor':'none'})
    a=axs[1];a.set_title('INTERVAL: fix data, vary candidate nulls',fontsize=12,pad=14)
    a.axhline(OBS,color=BLUE,ls='--',lw=1)
    a.plot([LOW,HIGH],[OBS,OBS],color=BLUE,lw=5,solid_capstyle='round')
    for v in [LOW,HIGH]:a.plot([v,v],[OBS,-.35],ls=':',color=BLUE,lw=1)
    a.scatter([0],[OBS],color=RED,s=65,zorder=5)
    a.text(.15,-.15,'Keep these candidates:\n[0.0040, 0.3960]',ha='center',fontsize=11,color=BLUE,bbox={'facecolor':'white','alpha':.85,'edgecolor':'none'})
    fig.text(.5,.055,'Vertical slice: a sampling statement under one null.    Horizontal slice: the confidence interval for one dataset.\nThe shaded band is a set of non-rejected pairs, not a probability density over parameters.',ha='center',fontsize=11,color=INK)
    save(fig,'01-test-inversion-band');plt.close(fig)

def sweep_scene(b):
    fig,(ax,bx)=plt.subplots(1,2,figsize=(11,5.2),dpi=95)
    fig.subplots_adjust(top=.76,bottom=.25,wspace=.32)
    p=float(2*stats.norm.sf(abs(OBS-b)/SE));color=GREEN if p>=ALPHA else RED
    fig.suptitle('Hold the data fixed; test a different candidate mean',fontsize=18,color=INK,y=.96)
    fig.text(.5,.86,f'Observed mean = 0.200   |   known SE = 0.100   |   candidate b = {b:.3f}   |   p = {p:.4f}',ha='center',fontsize=11)
    x=np.linspace(-.9,1.3,2400);density=stats.norm.pdf(x,loc=b,scale=SE);distance=abs(OBS-b)
    ax.plot(x,density,color=BLUE,lw=2)
    ax.fill_between(x,0,density,where=np.abs(x-b)>=distance,color=color,alpha=.35,interpolate=True)
    ax.axvline(OBS,color=INK,lw=1.5);ax.axvline(b,color=BLUE,ls=':',lw=1)
    ax.set(xlim=(-.65,1.05),ylim=(0,4.5),xlabel=r'Hypothetical sample mean $M$',ylabel='Null sampling density')
    ax.set_title('Two tail areas add up to p(b)',fontsize=12,pad=12)
    ax.text(.5,.92,'The black data line does not move.',transform=ax.transAxes,ha='center',fontsize=9)
    bs=np.linspace(-.2,.6,700);ps=2*stats.norm.sf(np.abs(OBS-bs)/SE)
    bx.axvspan(LOW,HIGH,color=GREEN,alpha=.12)
    bx.plot(bs,ps,color=BLUE,lw=2);bx.axhline(ALPHA,color=RED,ls='--',lw=1.2)
    bx.plot([b,b],[0,p],color=color,ls=':',lw=1.5);bx.scatter([b],[p],s=70,color=color,zorder=6)
    bx.plot([LOW,HIGH],[0,0],color=GREEN,lw=6,clip_on=False)
    bx.set(xlim=(-.2,.6),ylim=(0,1.08),xlabel=r'Candidate null mean $b$',ylabel=r'$p(b)$')
    bx.set_title('The 95% CI keeps p(b) >= 0.05',fontsize=12,pad=12)
    bx.text(.98,.12,'alpha = 0.05',transform=bx.transAxes,ha='right',color=RED,fontsize=9)
    bx.text(.98,.90,'Current b:\n'+('KEEP' if p>=ALPHA else 'REJECT'),transform=bx.transAxes,ha='right',color=color,fontweight='bold',bbox={'facecolor':'white','alpha':.9,'edgecolor':'none'})
    fig.text(.5,.055,'Green interval stays fixed: [0.0040, 0.3960].  Sweeping b does not resample data or move the true parameter.\np(b) is NOT a posterior density; the vertical axis is a separate null-tail probability at each b.',ha='center',fontsize=10,color=INK)
    return fig

def sweep():
    fig=sweep_scene(0.);save(fig,'02-pvalue-and-interval');plt.close(fig)
    values=np.r_[np.full(8,-.12),np.linspace(-.12,.52,46),np.full(8,.52),np.linspace(.52,-.12,30)]
    frames=[]
    for b in values:
        fig=sweep_scene(float(b));fig.canvas.draw()
        frame=Image.fromarray(np.asarray(fig.canvas.buffer_rgba()).copy()).convert('RGB')
        frames.append(frame);plt.close(fig)
    frames[0].save(OUT/'03-sweep-null-values.gif',save_all=True,append_images=frames[1:],duration=105,loop=0,disposal=2,optimize=False)

def checks():
    # Algebraic inversion checked over a deterministic grid, avoiding only numerical boundary ambiguity.
    vals=np.linspace(-1,1,5001);p=2*stats.norm.sf(abs(vals-OBS)/SE)
    assert np.array_equal(p>=ALPHA,(vals>=LOW)&(vals<=HIGH))
    errors=[]
    for nu in [1,2,8,30,200]:
        c=stats.t.ppf(.975,nu)
        for v in [-4,-1,0,1,4]:
            errors.append(abs(stats.f.sf(v*v,1,nu)-2*stats.t.sf(abs(v),nu)))
        assert abs(2*stats.t.sf(c,nu)-ALPHA)<1e-10
    assert max(errors)<1e-10
    for endpoint in [LOW,HIGH]:assert abs(2*stats.norm.sf(abs(OBS-endpoint)/SE)-ALPHA)<1e-12
    report={'normal_example':{'observed_mean':OBS,'known_SE':SE,'alpha':ALPHA,'p_at_zero':float(2*stats.norm.sf(OBS/SE)),'CI':[LOW,HIGH]},
      'one_sided_example':{'z':1.8,'upper_tail_p':float(stats.norm.sf(1.8)),'two_sided_p':float(2*stats.norm.sf(1.8))},
      'grid_checks':len(vals),'max_F_t_tail_error':max(errors),
      'exact_normal_coverage':float(stats.norm.cdf(CRIT)-stats.norm.cdf(-CRIT)),
      'interpretation':'Numerical checks support algebra, not a proof of general coverage; p(b) is not a density.'}
    (OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    OUT.mkdir(exist_ok=True,parents=True);checks();belt();sweep()
