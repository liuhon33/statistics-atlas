"""Reproduce static norm geometry and independently check its mathematical claims.

Requires numpy and matplotlib. Generated assets only; never writes raw sources.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.size': 12, 'axes.spines.top': False,
                     'axes.spines.right': False, 'svg.fonttype': 'none'})
TEAL, ORANGE = '#087e8b', '#bf6019'

def boundary(p):
    if np.isinf(p):
        return np.array([[-1,-1],[1,-1],[1,1],[-1,1],[-1,-1]],float)
    # Cartesian-power parametrization, independent of the explorer's radial method.
    t = np.linspace(0, 2*np.pi, 2401)
    u = np.column_stack((np.cos(t),np.sin(t)))
    return np.sign(u)*np.abs(u)**(2/p)

def measure(v,p):
    if p == 0: return np.count_nonzero(v)
    return np.linalg.norm(v,ord=p)

def axes(ax):
    ax.set(xlim=(-1.35,1.35),ylim=(-1.35,1.35),aspect='equal',
           xticks=[-1,0,1],yticks=[-1,0,1],xlabel='$x_1$',ylabel='$x_2$')
    ax.axhline(0,color='#95a2ad',lw=.7,zorder=0)
    ax.axvline(0,color='#95a2ad',lw=.7,zorder=0)
    ax.grid(alpha=.15)

def ball(ax,p):
    a=boundary(p)
    ax.fill(a[:,0],a[:,1],color=TEAL,alpha=.12)
    ax.plot(a[:,0],a[:,1],color=TEAL,lw=2.2)

def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight')
    fig.savefig(OUT/(name+'.png'),dpi=150,bbox_inches='tight')
    plt.close(fig)
    ET.parse(OUT/(name+'.svg'))

fig,axs=plt.subplots(1,3,figsize=(11.8,4.2),layout='constrained')
for ax,p,title,eq in zip(axs,[1,2,np.inf],
        ['Sum of magnitudes · $\\ell_1$','Euclidean length · $\\ell_2$','Largest magnitude · $\\ell_\\infty$'],
        ['$|x_1|+|x_2|\\leq 1$','$x_1^2+x_2^2\\leq 1$','$\\max(|x_1|,|x_2|)\\leq 1$']):
    axes(ax); ball(ax,p); ax.set_title(title+'\n'+eq,pad=12)
fig.suptitle('A unit ball includes the boundary and the interior',fontsize=17)
save(fig,'01-three-unit-balls')

fig,axs=plt.subplots(1,2,figsize=(9,4.8),layout='constrained')
for ax in axs:
    axes(ax)
    ax.plot([1,0],[0,1],'--',color=ORANGE,lw=2)
    ax.scatter([1,0,.5],[0,1,.5],color=ORANGE,zorder=5)
    ax.annotate('$m=(1/2,1/2)$',(.5,.5),(.55,.87),fontsize=11,
                arrowprops={'arrowstyle':'-','color':ORANGE})
ball(axs[0],.5)
axs[0].set_title('$p=1/2$: triangle inequality fails\n$\\sqrt{|x_1|}+\\sqrt{|x_2|}\\leq 1$',pad=12)
axs[0].text(.5,-.27,'Midpoint size = 2 > 1',transform=axs[0].transAxes,ha='center',color=ORANGE)
for a,b in [((-1.28,0),(1.28,0)),((0,-1.28),(0,1.28))]:
    axs[1].annotate('',b,a,arrowprops={'arrowstyle':'<->','color':TEAL,'lw':3})
axs[1].scatter([0],[0],color=TEAL,zorder=6)
axs[1].set_title('$\\ell_0$: homogeneity fails\nAt most one nonzero coordinate',pad=12)
axs[1].text(.5,-.27,'Unbounded axes; origin included',transform=axs[1].transAxes,ha='center',fontsize=11,color=TEAL)
fig.suptitle('Both sets fail the midpoint test for convexity',fontsize=17)
save(fig,'02-non-norm-cases')

# Independent numeric support for the analytic reasoning in the note.
x=np.array([3.,-4.,0.]); e1=np.array([1.,0.]); e2=np.array([0.,1.])
assert [measure(x,p) for p in [1,2,np.inf,0]] == [7,5,4,2]
assert np.isclose(measure(x,.5),7+4*np.sqrt(3))
assert measure(e1+e2,.5)==4 and measure(e1,.5)+measure(e2,.5)==2
assert np.isclose(measure((e1+e2)/2,.5),2,rtol=0,atol=1e-14)
assert measure(2*e1,0)==1 and 2*measure(e1,0)==2
assert measure((e1+e2)/2,0)==2
errors=[]
for p in [.25,.5,.75,1,1.5,2,4,8,np.inf]:
    b=boundary(p)
    sizes=np.max(np.abs(b),axis=1) if np.isinf(p) else np.sum(np.abs(b)**p,axis=1)**(1/p)
    errors.append(float(np.max(np.abs(sizes-1))))
assert max(errors)<1e-12
rng=np.random.default_rng(20261112)
for n in [2,3,9]:
    for _ in range(100):
        a,b=rng.normal(size=(2,n))
        assert measure(a,np.inf)<=measure(a,2)+1e-12<=measure(a,1)+2e-12
        for p in [1,1.5,2,4,8,np.inf]:
            assert measure(a+b,p)<=measure(a,p)+measure(b,p)+1e-12
        assert measure(a+b,0)<=measure(a,0)+measure(b,0)
assert np.isclose(np.abs(x)**.001 @ np.ones(3),2,atol=.003)
result={'status':'PASS','example':{'l1':7,'l2':5,'linf':4,'l0':2,'p_half':float(measure(x,.5))},
        'max_boundary_error':max(errors),'random_triangle_checks':1800,
        'analytic_checks':['three norm axioms and convex-ball implication',
          'normalization proof of convex-ball converse under positivity and homogeneity',
          'p>=1 convexity proof via convex scalar powers',
          'p<1 triangle counterexample for dimension >=2',
          'l0 support union implies subadditivity; scaling violates homogeneity',
          'p to infinity via max <= lp <= n^(1/p) max',
          'p to zero: sum of powers tends to support count, root does not',
          'p to zero balls: bounded axis segments, not the unbounded l0 set'],
        'limits':'Numerical checks support the written algebra; they are not general proofs.'}
(OUT/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
