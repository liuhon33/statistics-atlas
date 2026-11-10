"""Original testing illustration and numerical checks; no supplied image is edited."""
from pathlib import Path
import json
import itertools
from fractions import Fraction
import numpy as np
from scipy.stats import norm, binom
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
# Exhaust all 16 deterministic tests. The note separately proves optimality
# over the entire continuous cube of randomized tests.
p0 = [Fraction(1,4)]*4
p1 = [Fraction(1,25),Fraction(4,25),Fraction(4,25),Fraction(16,25)]
tests=[]
for rule in itertools.product([0,1],repeat=4):
    size=sum(a*b for a,b in zip(p0,rule))
    power=sum(a*b for a,b in zip(p1,rule))
    tests.append((rule,size,power))
valid=[row for row in tests if row[1]<=Fraction(1,4)]
assert len(valid)==5
assert max(row[2] for row in valid)==Fraction(16,25)
assert [row[0] for row in valid if row[2]==Fraction(16,25)]==[(0,0,0,1)]
alpha, n, theta = .05, 100, .2
c = norm.ppf(1-alpha)
rows = []
for label, threshold in [('Liberal cutoff', norm.ppf(.9)), ('Level .05', c),
                         ('Conservative cutoff', norm.ppf(.975))]:
    rows.append(dict(rule=label, cutoff=float(threshold), size=float(norm.sf(threshold)),
                     power=float(norm.sf(threshold-n**.5*theta))))
first_power = float(norm.sf(c-theta))
assert abs(rows[1]['size']-.05)<1e-12
assert rows[0]['size']>.05 and rows[2]['size']<.05
assert rows[1]['power']>first_power
gamma = (.05-binom.sf(8,10,.5))/binom.pmf(8,10,.5)
assert abs(gamma-67/75)<1e-12
ps=np.linspace(0,.5,101)
sizes=binom.sf(8,10,ps)+gamma*binom.pmf(8,10,ps)
assert np.max(sizes)<=.05+1e-12
req=(norm.ppf(.95)+norm.ppf(.8))**2/.2**2
assert np.ceil(req)==155
assert norm.sf(c-np.sqrt(154)*.2)<.8<=norm.sf(c-np.sqrt(155)*.2)
z=2
p=float(2*norm.sf(z))
ci=[.2-norm.ppf(.975)/10,.2+norm.ppf(.975)/10]
assert p<.05 and ci[0]>0
# Deterministic comparison of test/CI inversion away from equality boundaries.
for xbar in np.linspace(-1,1,401):
    for null in [-.4,0,.4]:
        reject=abs(10*(xbar-null))>norm.ppf(.975)
        outside=not (xbar-norm.ppf(.975)/10<=null<=xbar+norm.ppf(.975)/10)
        assert reject==outside
out=dict(alpha=alpha,n=n,alternative=theta,threshold_comparison=rows,
         two_flip_tests=16,two_flip_valid_tests=5,two_flip_maximum=.64,
         first_observation_power=first_power,binomial_gamma=float(gamma),
         binomial_tail_gt8=float(binom.sf(8,10,.5)),binomial_tail_ge8=float(binom.sf(7,10,.5)),
         binomial_randomized_power_at_p07=float(binom.sf(8,10,.7)+gamma*binom.pmf(8,10,.7)),
         required_n_unrounded=float(req),required_n=155,two_sided_observed_p=p,ci=ci,
         checks='PASS: tail areas, binomial calibration, null grid, sample-size boundary, CI inversion')
(OUT/'checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
x=np.linspace(-4,6,1500)
axs[0].plot(x,norm.pdf(x),color='#3669aa',label='Null boundary: Z ~ N(0,1)')
axs[0].plot(x,norm.pdf(x-2),color='#c46a25',label='Alternative: Z ~ N(2,1)')
axs[0].fill_between(x,0,norm.pdf(x),where=x>=c,color='#3669aa',alpha=.35)
axs[0].fill_between(x,0,norm.pdf(x-2),where=x>=c,color='#c46a25',alpha=.22)
axs[0].axvline(c,color='#333',linestyle='--')
axs[0].set(title='Same rejection region, different sampling laws',xlabel='Z = 10 × sample mean',ylabel='Density',ylim=(0,.52))
axs[0].text(2.1,.45,'Reject for Z > 1.645\nNull area = .05; power = .639',fontsize=10)
axs[0].legend(loc='upper left',fontsize=9)
t=np.linspace(-.25,.55,500)
axs[1].axvspan(t.min(),0,color='#ddd',alpha=.5,label='Null: θ ≤ 0')
axs[1].plot(t,norm.sf(c-10*t),color='#c46a25',label='Use all 100 observations')
axs[1].plot(t,norm.sf(c-t),color='#3669aa',label='Use only the first observation')
axs[1].axhline(.05,color='#888',linestyle=':')
axs[1].scatter([.2,.2],[rows[1]['power'],first_power],color=['#c46a25','#3669aa'])
axs[1].set(title='Optimize the rule, not the true parameter',xlabel='True mean θ (evaluation point)',ylabel='Probability of rejection',ylim=(0,1.03))
axs[1].legend(loc='upper left',fontsize=9)
fig.savefig(OUT/'testing-power.png',dpi=170)
fig.savefig(OUT/'testing-power.svg')
plt.close(fig)
# The convex hull of deterministic points is the randomized-test feasible set
# in (null rejection probability, alternative rejection probability) space.
from scipy.spatial import ConvexHull
points=np.array([(float(s),float(p)) for _,s,p in tests])
hull=ConvexHull(points)
fig,ax=plt.subplots(figsize=(8,5),layout='constrained')
poly=points[hull.vertices]
ax.fill(poly[:,0],poly[:,1],color='#cdd8e8',alpha=.65,label='All randomized tests (convex hull)')
ax.axvspan(0,.25,color='#53a06e',alpha=.22,label='Allowed Type I error ≤ .25')
ax.scatter(points[:,0],points[:,1],s=28,color='#526078',label='16 deterministic rules (some overlap)')
ax.axvline(.25,color='#306446',linestyle='--')
for name,point,offset in [('A: HH only',(.25,.64),(15,10)),('B: TH only',(.25,.16),(15,-10)),
                          ('C: any head',(.75,.96),(-115,-25)),('Always reject',(1,1),(-115,12))]:
    ax.scatter(*point,s=70,color='#c46a25')
    ax.annotate(name,point,xytext=offset,textcoords='offset points',fontsize=10)
ax.set(xlabel='Type I error = E₀[φ(X)]',ylabel='Power = E₁[φ(X)]',
       title='Two flips: maximize height without crossing x = .25',xlim=(-.025,1.025),ylim=(-.03,1.09))
ax.legend(loc='lower right',fontsize=9)
fig.savefig(OUT/'coin-feasible-tests.png',dpi=170)
fig.savefig(OUT/'coin-feasible-tests.svg')
plt.close(fig)
print(json.dumps(out,indent=2))
