"""Original analytic illustrations, not recovered video frames.

Reproduce with Python, NumPy, SciPy, Matplotlib and statsmodels:
    python draw.py
Outputs are written beside this file. No sources or note files are changed.
"""
from pathlib import Path
import json
import hashlib
import xml.etree.ElementTree as ET
import numpy as np
from scipy.special import expit, logit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
BLUE, ORANGE, PURPLE = "#176b91", "#bc6429", "#7757a6"
INK, MUTED, GRID = "#203444", "#607382", "#dbe4ea"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": GRID,
    "xtick.color": MUTED, "ytick.color": MUTED, "svg.fonttype": "none",
    "svg.hashsalt": "logistic-regression-2026-11-15", "figure.facecolor": "white"})

def tidy(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=.55, color=GRID)
    ax.set_axisbelow(True)

def save(fig, stem):
    fig.savefig(HERE / (stem + ".svg"), bbox_inches="tight", metadata={"Date": None})
    fig.savefig(HERE / (stem + ".png"), dpi=145, bbox_inches="tight")
    plt.close(fig)
    ET.parse(HERE / (stem + ".svg"))

def practical():
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    x = np.linspace(0, 10, 500)
    ax.plot(x, expit(-4+.8*x), color=BLUE, lw=3, label="Model probability")
    # These points illustrate individual binary outcomes, not the fitting sample.
    obs_x = np.array([.6, 1.4, 2.3, 2.9, 3.6, 4.2, 4.9, 5.4, 6.1, 6.8, 7.4, 8.3, 9.2])
    obs_y = np.array([0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1])
    ax.scatter(obs_x, obs_y, c=MUTED, alpha=.72, s=38, label="Illustrative observed 0/1 outcomes")
    for h, color in [(3, ORANGE), (5, PURPLE), (7, BLUE)]:
        p = expit(-4+.8*h)
        ax.plot([h, h], [0, p], ls=":", color=color)
        ax.scatter([h], [p], color=color, s=70, zorder=5)
        ax.annotate(f"{h} hours → {p:.1%}", (h, p), xytext=(8, -30 if h == 7 else 14),
                    textcoords="offset points", color=color, fontsize=12)
    ax.set(xlim=(0, 10), ylim=(-.08, 1.25), xlabel="Study time x (hours)",
           ylabel="Outcome y / probability p(x)", yticks=[0, .25, .5, .75, 1])
    ax.set_title("Predict a probability, then choose an action", loc="left", weight="bold", pad=14)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    tidy(ax)
    fig.text(.13, -.01, "Illustrative model: p(x) = 1 / [1 + exp(4 − 0.8x)]. Each actual outcome is still 0 or 1.",
             fontsize=10, color=MUTED)
    save(fig, "01-use-it")

def scales():
    fig = plt.figure(figsize=(10.2, 6.8))
    grid = fig.add_gridspec(2, 2, height_ratios=[.95, 3], hspace=.27, wspace=.32)
    top = fig.add_subplot(grid[0, :]); top.axis("off"); top.set_xlim(-.03,1.03)
    top.set_title("The same probability on three coordinate scales", loc="left", weight="bold", pad=14)
    labels = [("Probability", r"$p\in(0,1)$", BLUE),
              ("Odds", r"$p/(1-p)\in(0,\infty)$", ORANGE),
              ("Log-odds", r"$\log[p/(1-p)]\in\mathbb{R}$", PURPLE)]
    for j, (name, eq, color) in enumerate(labels):
        left=.005+j*.35
        top.add_patch(FancyBboxPatch((left,.12),.285,.70,boxstyle="round,pad=.014",fc="white",ec=color,lw=1.5))
        top.text(left+.142,.60,name,ha="center",color=color,weight="bold")
        top.text(left+.142,.31,eq,ha="center",color=INK,fontsize=12)
        if j<2: top.annotate("",(left+.34,.47),(left+.30,.47),arrowprops={"arrowstyle":"->","color":MUTED})
    a, b = fig.add_subplot(grid[1,0]), fig.add_subplot(grid[1,1])
    p = np.linspace(.003,.997,1000)
    a.plot(p,p/(1-p),color=ORANGE,lw=2.6)
    b.plot(p,logit(p),color=PURPLE,lw=2.6)
    for q,c in [(.1,BLUE),(.5,MUTED),(.9,ORANGE)]:
        a.scatter(q,q/(1-q),color=c,s=60,zorder=4)
        b.scatter(q,logit(q),color=c,s=60,zorder=4)
    a.set(xlim=(0,1),ylim=(0,10),xlabel="Probability p",ylabel="Odds p/(1−p)",
          title="1. Remove the upper bound")
    b.set(xlim=(0,1),ylim=(-3.2,3.2),xlabel="Probability p",ylabel="Log-odds",title="2. Put equal odds at zero")
    a.annotate("→ +∞ as p → 1",(.95,9.7),ha="right",fontsize=10,color=MUTED)
    b.axhline(0,color=MUTED,lw=.8);b.axvline(.5,color=MUTED,lw=.8,ls=":")
    b.annotate("p = 0.1\nlog-odds = −2.20",(.1,logit(.1)),(.17,-2.6),fontsize=10,color=BLUE)
    b.annotate("p = 0.9\nlog-odds = +2.20",(.9,logit(.9)),(.51,2.35),fontsize=10,color=ORANGE)
    b.annotate("p = 0.5 → 0",(.5,0),(.58,-.6),fontsize=10,color=MUTED)
    for ax in [a,b]: tidy(ax)
    fig.text(.125,.015,"Axes show finite windows. Endpoints p = 0 and p = 1 map to infinite limits, not finite logits.",fontsize=10,color=MUTED)
    save(fig,"02-three-scales")

def sensitivity():
    x=np.linspace(0,10,600);p=expit(-4+.8*x)
    fig, axes=plt.subplots(2,1,figsize=(9.4,6.8),sharex=True,gridspec_kw={"height_ratios":[1.5,1]},layout="constrained")
    a,b=axes
    a.plot(x,p,color=BLUE,lw=2.7)
    for start,col in [(1,ORANGE),(4.5,PURPLE),(8,ORANGE)]:
        end=start+1; p0,p1=expit(-4+.8*np.array([start,end]))
        a.plot([start,end],[p0,p1],color=col,lw=5,solid_capstyle="round")
        a.scatter([start,end],[p0,p1],color=col,zorder=4,s=35)
        a.annotate(f"+1 hour:\n+{100*(p1-p0):.1f} percentage points",((start+end)/2,(p0+p1)/2),
                   xytext=(0,52 if start==4.5 else (32 if start<6 else -48)),textcoords="offset points",ha="center",fontsize=11,color=col)
    a.set(ylabel="Pass probability p(x)",ylim=(-.03,1.06))
    a.set_title("Equal changes in x can produce very different probability changes",loc="left",weight="bold",pad=13)
    b.plot(x,.8*p*(1-p),color=PURPLE,lw=2.7)
    b.axvline(5,color=MUTED,lw=1,ls=":")
    b.scatter([5],[.2],color=PURPLE,zorder=4)
    b.annotate("Largest local slope at p = 0.5\n0.8 / 4 = 0.20 per hour",(5,.2),(6.1,.16),fontsize=11,color=PURPLE)
    b.set(xlim=(0,10),ylim=(0,.23),xlabel="Study time x (hours)",ylabel="Local slope dp/dx")
    for ax in axes: tidy(ax)
    save(fig,"03-sensitivity")

def checks():
    p=np.linspace(.0001,.9999,1000)
    h=1e-5;x=np.linspace(0,10,501);prob=expit(-4+.8*x)
    numerical=(expit(-4+.8*(x+h))-expit(-4+.8*(x-h)))/(2*h)
    errors={"inverse_max_error":float(np.max(abs(expit(logit(p))-p))),
      "symmetry_max_error":float(np.max(abs(logit(1-p)+logit(p)))),
      "slope_finite_difference_max_error":float(np.max(abs(numerical-.8*prob*(1-prob))))}
    assert errors["inverse_max_error"]<1e-14
    assert errors["symmetry_max_error"]<2e-12
    assert errors["slope_finite_difference_max_error"]<1e-9
    eta=-4+.8*x
    np.testing.assert_allclose(np.exp(eta+.8)/np.exp(eta),np.exp(.8))
    # Canonical-link gradient and Hessian checked against finite differences.
    X=np.column_stack([np.ones(9),np.arange(1,10)])
    k=np.array([4,8,17,31,50,69,83,92,96]);n=np.full(9,100)
    beta=np.array([-3.1,.61]);mu=expit(X@beta)
    loss=lambda z:float(np.sum(n*np.logaddexp(0,X@z)-k*(X@z)))
    grad=X.T@(n*mu-k); eps=1e-5
    numgrad=np.array([(loss(beta+eps*d)-loss(beta-eps*d))/(2*eps) for d in np.eye(2)])
    H=X.T@((n*mu*(1-mu))[:,None]*X)
    score=lambda z:X.T@(n*expit(X@z)-k)
    numH=np.column_stack([(score(beta+eps*d)-score(beta-eps*d))/(2*eps) for d in np.eye(2)])
    errors["gradient_max_error"]=float(np.max(abs(grad-numgrad)))
    errors["hessian_max_error"]=float(np.max(abs(H-numH)))
    assert errors["gradient_max_error"]<1e-5 and errors["hessian_max_error"]<1e-4
    assert min(np.linalg.eigvalsh(H))>0
    fit=sm.GLM(k/n,X,family=sm.families.Binomial(),freq_weights=n).fit()
    result={"description":"Original analytic examples; numerical checks support the derivations in the note.",
      "errors":errors,"fit_coefficients":fit.params.tolist(),
      "fit_probabilities_3_5_7":fit.predict(np.column_stack([np.ones(3),[3,5,7]])).tolist(),
      "illustrative_probabilities_3_5_7":expit(-4+.8*np.array([3,5,7])).tolist(),
      "equal_step_changes":{str(s):float(expit(-4+.8*(s+1))-expit(-4+.8*s)) for s in [1,4.5,8]},
      "svg_xml":"pass","sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*.svg')}}
    (HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    practical();scales();sensitivity();checks()
