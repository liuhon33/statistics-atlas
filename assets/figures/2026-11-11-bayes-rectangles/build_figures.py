"""Reproduce original Bayes/Monty/ELBO illustrations and offline explorers.

Run with Python + numpy + matplotlib from any directory. No network access.
The rectangle method and Steve inputs are attributed in the accompanying notes.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import json
import math
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[2]
BLUE, AMBER, GRAY, INK, PURPLE = '#307eae', '#d49b43', '#e6ebf0', '#172b40', '#8664b7'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'text.color': INK, 'axes.labelcolor': INK, 'axes.edgecolor': '#abb8c8',
                     'svg.fonttype': 'none', 'figure.facecolor': '#f7f8fa',
                     'axes.spines.top': False, 'axes.spines.right': False})

def save(fig, name):
    fig.savefig(HERE / (name+'.svg'), bbox_inches='tight')
    fig.savefig(HERE / (name+'.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    ET.parse(HERE / (name+'.svg'))

def bar(ax, probs, colors, y=.25, height=.25):
    left=0
    for p,c in zip(probs,colors):
        ax.add_patch(Rectangle((left,y),p,height,facecolor=c,edgecolor='white'))
        left+=p
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')

def rectangle(ax, prior, lh, colors):
    left=0
    for p,h,c in zip(prior,lh,colors):
        ax.add_patch(Rectangle((left,0),p,1,facecolor=GRAY,edgecolor='white'))
        ax.add_patch(Rectangle((left,0),p,h,facecolor=c,edgecolor='white'))
        left+=p
    ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set_yticks([0,.5,1]);ax.set_xticks([0,1])
    ax.set_ylabel('Fraction producing the evidence');ax.set_xlabel('Prior probability (column width)')

def make_figures():
    fig,ax=plt.subplots(figsize=(9,2.3))
    bar(ax,[1/6,5/6],[BLUE,AMBER],.25,.3)
    ax.text(0,.86,'Among 24 people matching the description',weight='bold',fontsize=17)
    ax.text(1/12,.40,'4',ha='center',va='center',color='white',weight='bold',fontsize=18)
    ax.text(7/12,.40,'20',ha='center',va='center',color=INK,weight='bold',fontsize=18)
    ax.text(0,.07,'Librarians: 4/24 = 1/6',color=BLUE)
    ax.text(.52,.07,'Farmers: 20/24 = 5/6',color='#906019')
    save(fig,'01-one-minute')

    fig=plt.figure(figsize=(9,6.5));gs=fig.add_gridspec(2,1,height_ratios=[3,1.2],hspace=.5)
    ax=fig.add_subplot(gs[0]);rectangle(ax,[1/21,20/21],[.4,.1],[BLUE,AMBER])
    ax.set_title('Steve: keep the evidence-producing part of each column',loc='left',pad=18,weight='bold')
    ax.annotate('Librarian area\n(1/21) × .4 = 2/105',xy=(1/42,.25),xytext=(.14,.65),arrowprops={'arrowstyle':'->','color':BLUE},color=BLUE)
    ax.annotate('Farmer area\n(20/21) × .1 = 2/21',xy=(.65,.05),xytext=(.48,.42),arrowprops={'arrowstyle':'->','color':AMBER},color='#906019')
    ax=fig.add_subplot(gs[1]);bar(ax,[1/6,5/6],[BLUE,AMBER],.28,.3)
    ax.text(0,.85,'Normalize by total retained area: 2/105 + 2/21 = 4/35',weight='bold')
    ax.text(0,.02,'Librarian 1/6',color=BLUE);ax.text(.5,.02,'Farmer 5/6',color='#906019')
    save(fig,'02-steve-rectangles')

    r=np.linspace(.00001,.99999,1001);a,b=2/105,2/21;loge=math.log(a+b)
    elbo=r*np.log(a/r)+(1-r)*np.log(b/(1-r))
    fig,axes=plt.subplots(2,1,figsize=(9,6.6),gridspec_kw={'height_ratios':[1,2.7]},layout='constrained')
    ax=axes[0];bar(ax,[1/6,5/6],[BLUE,AMBER],.50,.19);bar(ax,[.5,.5],[BLUE,AMBER],.05,.19)
    ax.text(0,.82,'Exact posterior: (1/6, 5/6)',weight='bold');ax.text(0,.31,'Trial q: (1/2, 1/2)')
    ax=axes[1];ax.plot(r,elbo,color=PURPLE,lw=2.5,label='ELBO(r)')
    ax.axhline(loge,color='#607086',ls='--',label='log evidence (fixed)')
    at_half=.5*math.log(a/.5)+.5*math.log(b/.5)
    ax.plot([.5,.5],[at_half,loge],color=BLUE,lw=3)
    ax.annotate('Posterior KL gap\nat r = 1/2',xy=(.5,(at_half+loge)/2),xytext=(.35,-3.15),arrowprops={'arrowstyle':'->','color':BLUE},color=BLUE)
    ax.scatter([1/6],[loge],color=INK,zorder=4);ax.text(.19,-2.06,'Maximum at r = 1/6')
    ax.set(xlim=(0,1),ylim=(-4.15,-1.9),xlabel='r = q(librarian)',ylabel='Natural log value (nats)')
    ax.legend(loc='lower left');save(fig,'03-elbo-shares')

    fig,axes=plt.subplots(2,1,figsize=(9,6.7),gridspec_kw={'height_ratios':[3,1.2]},layout='constrained')
    ax=axes[0];rectangle(ax,[1/3]*3,[.5,1,0],[BLUE,AMBER,'#9aa7b5'])
    ax.set_title('Monty opens door 3: the standard informed host',loc='left',weight='bold',pad=18)
    for x,h,label in [(1/6,.5,'Car at 1\nheight 1/2\narea 1/6'),(.5,1,'Car at 2\nheight 1\narea 1/3'),(5/6,0,'Car at 3\nheight 0\narea 0')]:
        ax.text(x,.72 if h<1 else .5,label,ha='center',va='center')
    ax=axes[1];bar(ax,[1/3,2/3],[BLUE,AMBER],.25,.32)
    ax.text(0,.82,'Retained area = 1/2. Divide each surviving area by 1/2.',weight='bold')
    ax.text(0,.02,'Stay: 1/3',color=BLUE);ax.text(.50,.02,'Switch: 2/3',color='#906019')
    save(fig,'04-monty-rectangles')

    fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
    for ax,lh,title in zip(axes,[[.5,1,0],[.5,.5,0]],['Knows: likelihoods (1/2, 1, 0)','Blind: likelihoods (1/2, 1/2, 0)']):
        rectangle(ax,[1/3]*3,lh,[BLUE,AMBER,'#9aa7b5']);ax.set_title(title,fontsize=13,pad=18)
        ax.set_xticks([1/6,.5,5/6],['Car at 1','Car at 2','Car at 3']);ax.set_xlabel('Equal prior widths = 1/3')
    fig.suptitle('Same observed goat; different mechanism → different posterior',fontsize=16)
    save(fig,'05-host-comparison')

    fig,ax=plt.subplots(figsize=(9,3.1));bar(ax,[.01,.99],[BLUE,AMBER],.35,.2)
    ax.text(0,.86,'100 doors: your original choice versus the other 99',weight='bold',fontsize=16)
    ax.annotate('Your door: 1%',xy=(.005,.45),xytext=(.08,.12),arrowprops={'arrowstyle':'->','color':BLUE},color=BLUE)
    ax.text(.53,.45,'Other 99 doors: 99%',ha='center',va='center')
    ax.text(0,.66,'An informed host opens 98 goats. Switch wins whenever your first pick was wrong.')
    save(fig,'06-hundred-doors')

def verify():
    evidence=F(1,21)*F(2,5)+F(20,21)*F(1,10)
    assert evidence==F(4,35)
    assert F(1,21)*F(2,5)/evidence==F(1,6)
    max_gap_error=0
    table=[]
    for r in np.linspace(0,1,1001):
        q=[r,1-r];post=[1/6,5/6];prior=[1/21,20/21];lh=[.4,.1]
        kl=lambda target:sum(x*math.log(x/y) for x,y in zip(q,target) if x)
        bound=sum(x*math.log(y) for x,y in zip(q,lh))-kl(prior)
        gap=kl(post);err=abs(math.log(float(evidence))-bound-gap)
        max_gap_error=max(max_gap_error,err);assert gap>=-1e-12 and err<1e-12
    for r in [1/21,.5,1/6]:
        q=[r,1-r];fit=sum(x*math.log(l) for x,l in zip(q,[.4,.1]));prior_kl=sum(x*math.log(x/y) for x,y in zip(q,[1/21,20/21]));gap=sum(x*math.log(x/y) for x,y in zip(q,[1/6,5/6]));table.append({'r':r,'fit':fit,'prior_kl':prior_kl,'elbo':fit-prior_kl,'gap':gap})
    # Enumerate the six equally likely (car, host fair coin) states independently.
    retained=[];wins=0
    for car in range(1,4):
        for coin in [0,1]:
            options=[d for d in [2,3] if d!=car]
            opened=options[coin] if len(options)==2 else options[0]
            switched=next(d for d in [2,3] if d!=opened)
            wins+=switched==car
            if opened==3:retained.append(car)
    assert retained.count(1)==1 and retained.count(2)==2 and len(retained)==3 and wins==4
    for n in range(3,101):
        # Fix a particular remaining unchosen door, e.g. 2. Ignore reveal order.
        joint_stay=F(1,n)*F(1,n-1);joint_switch=F(1,n)
        assert joint_stay/(joint_stay+joint_switch)==F(1,n)
    # A blind host chooses 2/3 regardless of the car; condition on 3 AND a goat.
    retained_blind=[car for car in range(1,4) for opened in [2,3] if opened==3 and car!=3]
    assert retained_blind==[1,2]
    # Exact biased-host mixture: before observing the named reveal, switch stays 2/3.
    for num in range(101):
        t=F(num,100); e3=(t+1)/3;e2=(2-t)/3
        assert e3/(1+t)+e2/(2-t)==F(2,3)
    # Finite-difference check of the score identity in a smooth Gaussian mixture.
    def component(x,mu,sd):return math.exp(-.5*((x-mu)/sd)**2)/(sd*math.sqrt(2*math.pi))
    def label_prob(x):
        a=.3*component(x,-1,1);b=.7*component(x,1.2,.8)
        return a/(a+b)
    score_err=0
    for x in np.linspace(-3,3,81):
        a=.3*component(x,-1,1);b=.7*component(x,1.2,.8)
        gu=(a*(-x-1)+b*(-(x-1.2)/.8**2))/(a+b)
        h=1e-5;dg=(math.log(label_prob(x+h))-math.log(label_prob(x-h)))/(2*h)
        score_err=max(score_err,abs((-x-1)-gu-dg))
    assert score_err<1e-8
    monty_gap=.5*math.log(9/8)
    assert abs((.5*math.log((1/6)/.5)+.5*math.log((1/3)/.5))-(math.log(.5)-monty_gap))<1e-12
    return {'steve_evidence':str(evidence),'steve_posterior':'1/6',
            'elbo_identity_max_error':max_gap_error,'elbo_table':table,
            'monty_retained_car_states':retained,'blind_retained_car_states':retained_blind,
            'n_door_cases':98,'biased_host_cases':101,'diffusion_score_max_error':score_err,
            'monty_elbo_gap':monty_gap,'svg_parse':'PASS'}

def build_explorers():
    builder=VAULT/'.agents/skills/animate-geometry/scripts/build_explorer.py'
    spec=importlib.util.spec_from_file_location('explorer_builder',builder);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    inputs=[HERE/'explorer.css',HERE/'math.js',HERE/'explorer.js',Path(__file__)]
    for mode in ['bayes','elbo','monty']:
        body=f'<main data-mode="{mode}"></main>'
        out=module.compile_html(f'{mode.title()} rectangles',body,[(HERE/'explorer.css').read_text(encoding='utf-8')],[(HERE/'math.js').read_text(encoding='utf-8'),(HERE/'explorer.js').read_text(encoding='utf-8')])
        module.write_artifact(HERE/(mode+'-explorer.html'),out,inputs)

if __name__=='__main__':
    result=verify();make_figures();build_explorers()
    (HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
