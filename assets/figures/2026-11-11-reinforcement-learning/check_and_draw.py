"""Run with D:/anaconda/python.exe; requires numpy, scipy, matplotlib.
Checks the JS implementation against independently evaluated policies and LP bounds.
Writes original analytic SVG/PNG figures and a reproducible verification record.
"""
from pathlib import Path
import itertools, json, subprocess
import numpy as np
from scipy.optimize import linprog
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
NODE=Path(r'C:\Program Files\nodejs\node.exe')
js="""const m=require('./math.js');let out=[];for(const n of [10,100])for(const p of [.4,.5,.6]){const h=m.valueHistory(n,p),z=m.policyHistory(n,p);out.push({n,p,h,pi:m.greedy(h.at(-1).v,p),policyHistory:z});}console.log(JSON.stringify(out));"""
cases=json.loads(subprocess.check_output([str(NODE),'-e',js],cwd=HERE,text=True))

def policy_value(n,p,pi):
    A=np.eye(n-1);b=np.zeros(n-1)
    for s in range(1,n):
        for target,weight in ((s+pi[s],p),(s-pi[s],1-p)):
            if target==n:b[s-1]+=weight
            elif target:A[s-1,target-1]-=weight
    return np.r_[0,np.linalg.solve(A,b),1]

def lp_value(n,p):
    rows=[];rhs=[]
    for s in range(1,n):
        for a in range(1,min(s,n-s)+1):
            r=np.zeros(n-1);r[s-1]-=1;b=0
            for target,w in ((s+a,p),(s-a,1-p)):
                if target==n:b-=w
                elif target:r[target-1]+=w
            rows.append(r);rhs.append(b)
    z=linprog(np.ones(n-1),A_ub=np.array(rows),b_ub=np.array(rhs),bounds=(0,1),method='highs',options={'dual_feasibility_tolerance':1e-10,'primal_feasibility_tolerance':1e-10,'presolve':False})
    assert z.success,z.message
    return np.r_[0,z.x,1]

checks=[]
for c in cases:
    n,p=c['n'],c['p'];v=np.array(c['h'][-1]['v']);pv=policy_value(n,p,c['pi']);lp=lp_value(n,p)
    history=np.array([f['v'] for f in c['h']]);assert np.min(np.diff(history,axis=0))>=-1e-12
    assert np.min(history)>=-1e-12 and np.max(history)<=1+1e-12
    pi_values=[np.array(f['v']) for f in c['policyHistory'] if f['phase']=='Evaluate current policy']
    assert all(np.min(b-a)>-1e-9 for a,b in zip(pi_values,pi_values[1:]))
    e_policy=float(np.max(abs(v-pv)));e_lp=float(np.max(abs(v-lp)));e_pi=float(np.max(abs(v-np.array(c['policyHistory'][-1]['v']))))
    assert max(e_policy,e_lp,e_pi)<2e-8,(n,p,e_policy,e_lp,e_pi)
    if p==.5:assert np.max(abs(v-np.arange(n+1)/n))<2e-9
    if p==.6:assert np.max(abs(v-policy_value(n,p,[0]+[1]*(n-1)+[0])))<2e-9
    checks.append(dict(goal=n,p=p,sweeps=len(c['h'])-1,policy_phases=len(c['policyHistory'])-1,policy_evaluation_error=e_policy,linear_program_error=e_lp,policy_iteration_error=e_pi))

# Exhaust every deterministic positive-stake policy for the small worked example.
c=next(c for c in cases if c['n']==10 and c['p']==.4)
best=np.zeros(11);count=0
for stakes in itertools.product(*(range(1,min(s,10-s)+1) for s in range(1,10))):
    best=np.maximum(best,policy_value(10,.4,[0,*stakes,0]));count+=1
assert np.max(abs(best-np.array(c['h'][-1]['v'])))<1e-10
# Exact running mean and Bellman tower example, independent of the simulator.
returns=np.array([1.,0.,1.,1.,0.]);mean=0
for k,g in enumerate(returns,1):mean+=(g-mean)/k
assert abs(mean-returns.mean())<1e-15

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
BLUE='#236aad';GREEN='#23835a';ORANGE='#b95b19';GRAY='#526273'
def save(fig,name):
    fig.savefig(HERE/(name+'.svg'),bbox_inches='tight',facecolor='white')
    fig.savefig(HERE/(name+'.png'),dpi=150,bbox_inches='tight',facecolor='white');plt.close(fig)
    ET.parse(HERE/(name+'.svg'))

c100=next(c for c in cases if c['n']==100 and c['p']==.4)
fig,axs=plt.subplots(2,1,figsize=(10,6.5),layout='constrained')
for k,col in zip([1,2,3,len(c100['h'])-1],['#b9cddd','#7da8c8','#4e85b3',BLUE]):
    axs[0].plot(range(101),c100['h'][k]['v'],color=col,lw=2,label='Converged' if k==len(c100['h'])-1 else f'Sweep {k}')
axs[0].set(xlabel='Capital s',ylabel='Success probability V(s)',ylim=(0,1.04),xlim=(0,100),title='Value iteration sends the goal boundary backward through the state space')
axs[0].legend(ncol=4,frameon=False,loc='upper left');axs[0].grid(alpha=.18)
axs[1].bar(range(1,100),c100['pi'][1:100],color=GREEN,width=.82)
axs[1].set(xlabel='Capital s',ylabel='Stake a',ylim=(0,52),xlim=(0,100),title='One optimal policy: smallest stake among numerical ties')
axs[1].grid(axis='y',alpha=.18);fig.suptitle('Gambler: goal 100, win probability 0.4, no discount',fontsize=15)
save(fig,'01-gambler-values-policy')

# Random-policy gridworld: direct linear solution and independent fixed-policy sweeps.
active=list(range(1,15));A=np.eye(14);b=-np.ones(14)
def neighbors(s):
    r,c=divmod(s,4)
    return [max(0,r-1)*4+c,min(3,r+1)*4+c,r*4+max(0,c-1),r*4+min(3,c+1)]
for s in active:
    for t in neighbors(s):
        if t in active:A[s-1,t-1]-=.25
grid=np.r_[0,np.linalg.solve(A,b),0]
expected=np.array([0,-14,-20,-22,-14,-18,-20,-20,-20,-20,-18,-14,-22,-20,-14,0])
assert np.max(abs(grid-expected))<1e-10
g0=np.zeros(16);gh=[g0]
for k in range(2):gh.append(np.array([0 if s in (0,15) else -1+.25*sum(gh[-1][t] for t in neighbors(s)) for s in range(16)]))
assert gh[2][1]==-1.75
fig,axs=plt.subplots(1,4,figsize=(11,3.4),layout='constrained')
for ax,v,title in zip(axs,[*gh,grid],['Start: V₀','Sweep 1: V₁','Sweep 2: V₂','Converged Vπ']):
    ax.imshow(v.reshape(4,4),cmap='Blues_r',vmin=-22,vmax=0)
    for s,val in enumerate(v):
        grid_row,grid_col=divmod(s,4);txt='T\n0' if s in (0,15) else f'{val:g}'
        ax.text(grid_col,grid_row,txt,ha='center',va='center',color='white' if val<-12 else '#172739',fontsize=11)
    ax.set_title(title,fontsize=12);ax.set_xticks(np.arange(-.5,4,1),minor=True);ax.set_yticks(np.arange(-.5,4,1),minor=True);ax.grid(which='minor',color='#bccbd8');ax.tick_params(which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.suptitle('Same random policy throughout: four actions with probability ¼, reward −1 per move',fontsize=13)
save(fig,'05-gridworld-evaluation')

fig,ax=plt.subplots(figsize=(10,3.9),layout='constrained');ax.set(xlim=(0,10),ylim=(0,4));ax.axis('off')
def box(x,y,w,h,text,color):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.12',fc=color,ec='none',alpha=.12));ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=12)
def arrow(x1,y1,x2,y2,label='',dy=0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='->',mutation_scale=15,color=GRAY,lw=1.5));
    if label:ax.text((x1+x2)/2,(y1+y2)/2+dy,label,ha='center',va='center',fontsize=11,color=GRAY)
box(.3,1.4,1.7,1,'Capital s = 3\nChoose stake a = 2',BLUE)
box(4.3,2.6,1.9,.85,'Capital 5\nV(5) = 0.400000',GREEN)
box(4.3,.5,1.9,.85,'Capital 1\nV(1) = 0.043463',ORANGE)
arrow(2.15,2.1,4.1,3,'Win: 0.4',.28);arrow(2.15,1.6,4.1,.9,'Lose: 0.6',-.3)
box(7.2,1.2,2.3,1.4,'Q(3,2)\n= 0.4 V(5) + 0.6 V(1)\n= 0.186078',BLUE)
arrow(6.35,3,7.1,2.25);arrow(6.35,.95,7.1,1.6)
fig.suptitle('One action value is an average over the next states (goal 10)',fontsize=14);save(fig,'02-gambler-one-backup')

fig,ax=plt.subplots(figsize=(10,3.5),layout='constrained');ax.set(xlim=(0,10),ylim=(0,3.8));ax.axis('off')
box(.5,1.3,2.1,1.1,'Policy π\nChoose an action',GREEN);box(6.9,1.3,2.1,1.1,'Environment p\nNext state + reward',BLUE)
arrow(2.8,2.15,6.7,2.15,'Action Aₜ',.32);arrow(6.7,1.55,2.8,1.55,'Sₜ₊₁, Rₜ₊₁',-.32)
ax.text(5,.3,'Evaluate π → compute Vπ and Qπ → improve π → repeat',ha='center',fontsize=12)
fig.suptitle('Actions change the future states that generate later rewards',fontsize=15);save(fig,'03-agent-loop')

fig,ax=plt.subplots(figsize=(10,4.4),layout='constrained');ax.axis('off')
rows=[['Dynamic programming','Every possible next state','Exact expectation','Yes'],['Monte Carlo','One completed trajectory','Observed return Gₜ','No'],['TD(0)','One transition','Rₜ₊₁ + γV(Sₜ₊₁)','No'],['Q-learning','One transition','Rₜ₊₁ + γ maxₐ Q(Sₜ₊₁,a)','No']]
table=ax.table(cellText=rows,colLabels=['Method','What is used','Update target','Model?'],cellLoc='left',colLoc='left',colWidths=[.23,.27,.40,.10],loc='center')
table.auto_set_font_size(False);table.set_fontsize(10);table.scale(1,2.4)
for (r,k),cell in table.get_celld().items():cell.set_edgecolor('#d6dfe7');cell.set_facecolor('#eaf1f7' if r==0 else 'white')
ax.set_title('Same goal, different ways to construct the update target',fontsize=15,pad=12);save(fig,'04-update-targets')

(HERE/'checks.json').write_text(json.dumps({'status':'pass','cases':checks,'exhaustive_toy_policies':count,'exhaustive_max_error':float(np.max(abs(best-np.array(c['h'][-1]['v'])))),'gridworld_linear_system_error':float(np.max(abs(grid-expected))),'checks':['probability bounds','monotone synchronous value iteration','policy improvement is nondecreasing','independent linear policy evaluation','linear-program Bellman inequalities','fair-coin values s/goal','favorable-coin bet-1 policy','all 2880 toy deterministic policies','running-average identity','gridworld linear system and first two sweeps','SVG XML parsing'],'toy':{'values':c['h'][-1]['v'],'policy':c['pi'],'sweeps':[f['v'] for f in c['h'][:4]]}},indent=2),encoding='utf-8')
print(json.dumps({'status':'pass','exhaustive_policies':count,'max_lp_error':max(x['linear_program_error'] for x in checks),'max_policy_error':max(x['policy_evaluation_error'] for x in checks)}))
