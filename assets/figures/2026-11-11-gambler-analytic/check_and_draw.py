"""Exact finite gambler certificates and original static teaching figures.

Run with Python + matplotlib + numpy + sympy. All input/output paths derive
from this script's absolute path; no originals or existing figures are edited.
The optimality certificate uses fractions, not convergence or a tolerance.
"""
from fractions import Fraction as F
from functools import reduce
from math import lcm
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import sympy as sy

OUT = Path(__file__).resolve().parent
P = F(2, 5)


def timid(n, p):
    if p == F(1, 2):
        return [F(s, n) for s in range(n + 1)]
    r = (1 - p) / p
    return [(1 - r ** s) / (1 - r ** n) for s in range(n + 1)]


def bold(n, p):
    """Solve affine cycles W(s)=c_s+d_s W(next_s) with exact fractions."""
    known = {0: F(0), n: F(1)}

    def edge(s):
        return (F(0), p, 2 * s) if 2 * s <= n else (p, 1 - p, 2 * s - n)

    for start in range(1, n):
        path, seen = [], {}
        s = start
        while s not in known and s not in seen:
            seen[s] = len(path)
            path.append(s)
            s = edge(s)[2]
        if s not in known:
            const, mult = F(0), F(1)
            for k in path[seen[s]:]:
                c, d, _ = edge(k)
                const += mult * c
                mult *= d
            assert mult < 1
            known[s] = const / (1 - mult)
        for k in reversed(path):
            c, d, nxt = edge(k)
            known[k] = c + d * known[nxt]
    return [known[s] for s in range(n + 1)]


def certificate(n, p, v, policy):
    assert v[0] == 0 and v[n] == 1
    assert all(0 <= x <= 1 for x in v)
    rows = []
    for s in range(1, n):
        gaps = {a: v[s] - p * v[s + a] - (1 - p) * v[s - a]
                for a in range(1, min(s, n - s) + 1)}
        assert min(gaps.values()) >= 0, (n, p, s, gaps)
        assert gaps[policy(s)] == 0
        rows.append({"capital": s, "value": str(v[s]), "decimal": float(v[s]),
                     "optimal_stakes": [a for a, g in gaps.items() if g == 0],
                     "gaps": {str(a): str(g) for a, g in gaps.items()}})
    return {"target": n, "p": str(p), "state_action_checks": sum(len(r["gaps"]) for r in rows),
            "all_inequalities_exact": True, "policy_equalities_exact": True, "rows": rows}


def independent_policy_values(n, p, policy):
    mat = np.eye(n - 1)
    rhs = np.zeros(n - 1)
    for s in range(1, n):
        a = policy(s)
        for t, prob in ((s + a, p), (s - a, 1 - p)):
            if t == n:
                rhs[s - 1] += float(prob)
            elif t != 0:
                mat[s - 1, t - 1] -= float(prob)
    return np.r_[0., np.linalg.solve(mat, rhs), 1.]


def run_checks():
    certificates = []
    max_error = 0.
    for n in (10, 100):
        for p in (F(2, 5), F(1, 2), F(3, 5)):
            u = timid(n, p)
            assert all(u[s] == p*u[s + 1] + (1-p)*u[s - 1] for s in range(1, n))
            v = bold(n, p) if p < F(1, 2) else u
            policy = (lambda s: min(s, n-s)) if p < F(1, 2) else (lambda s: 1)
            cert = certificate(n, p, v, policy)
            if p == F(1, 2):
                assert all(len(r["optimal_stakes"]) == len(r["gaps"]) for r in cert["rows"])
            if p > F(1, 2):
                assert all(r["optimal_stakes"] == [1] for r in cert["rows"])
            max_error = max(max_error, float(np.max(np.abs(np.array(list(map(float, v))) - independent_policy_values(n, p, policy)))))
            certificates.append(cert)
    b10, b100 = bold(10, P), bold(100, P)
    assert all(b10[s] == b100[10*s] for s in range(11))
    q = 1 - P
    assert b100[30] == P**2 * (1 + P*P*q)/(1 - P**2*q**2)
    assert b100[30] == P*b100[50] + q*b100[10]
    assert b100[30] == P*b100[60]
    assert b100[30] > P*b100[40] + q*b100[20]
    x, mu, sigma, target = sy.symbols("x mu sigma target", real=True, nonzero=True)
    h = (1 - sy.exp(-2*mu*x/sigma**2))/(1-sy.exp(-2*mu*target/sigma**2))
    assert sy.simplify(mu*sy.diff(h,x) + sigma**2*sy.diff(h,x,2)/2) == 0
    assert sy.simplify(h.subs(x,0)) == 0 and sy.simplify(h.subs(x,target)) == 1
    assert sy.simplify(sy.limit(h,mu,0) - x/target) == 0
    toy = certificates[0]
    den = reduce(lcm, [F(g).denominator for row in toy["rows"] for g in row["gaps"].values()])
    toy_gap_table = [{"capital": row["capital"], "scaled_gaps": [int(F(g)*den) for g in row["gaps"].values()]} for row in toy["rows"]]
    (OUT / "exact-certificates.json").write_text(json.dumps(certificates, indent=2) + "\n", encoding="utf-8")
    result = {"method": "exact rational cycle elimination and all-action verification inequalities",
              "certificates": [{k:v for k,v in c.items() if k != "rows"} for c in certificates],
              "N10_gap_common_denominator": den, "N10_scaled_gap_rows": toy_gap_table,
              "independent_float_policy_max_error": max_error,
              "Brownian_ODE_boundary_and_zero_drift_limit": "symbolic PASS",
              "scaled_bold_N10_N100_identity": "exact PASS",
              "examples": {"N10_s3_timid": str(timid(10,P)[3]), "N100_s30_timid": str(timid(100,P)[30]),
                           "N100_s30_timid_decimal": float(timid(100,P)[30]),
                           "N100_s30_bold": str(b100[30]), "N100_s30_bold_decimal": float(b100[30])}}
    return result


plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "svg.fonttype": "none", "figure.facecolor": "#fbfcff",
                     "axes.facecolor": "#fbfcff", "savefig.facecolor": "#fbfcff"})
BLUE, ORANGE, GRAY = "#156d9d", "#c86621", "#607183"


def save(fig, stem):
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    ET.parse(OUT / f"{stem}.svg")


def draw_values():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.7), layout="constrained")
    for ax, n in zip(axs, (10, 100)):
        s = np.arange(n+1)
        b, u = bold(n,P), timid(n,P)
        ax.plot(s, list(map(float,b)), color=BLUE, lw=2.4, marker="o" if n==10 else None, markersize=4, label="Bold: optimal success probability")
        ax.plot(s, list(map(float,u)), color=ORANGE, lw=2, label="Timid: always stake 1")
        ax.plot(s, s/n, "--", color=GRAY, lw=1.2, label="s/N: upper bound, not the answer")
        k = 3 if n == 10 else 30
        ax.scatter([k],[float(b[k])], color=BLUE, s=55, zorder=4)
        label = f"Start {k}: bold = {float(b[k]):.6f}\n" + (f"timid = {float(u[k]):.6f}" if n==10 else f"timid = {float(u[k]):.2e}")
        ax.text(.045,.80,label,transform=ax.transAxes,fontsize=11,bbox={"facecolor":"white","edgecolor":"#d5dce4","boxstyle":"round,pad=.45"})
        ax.set(xlabel="Starting capital s (units)",ylabel="Probability of reaching N before 0",title=f"Target N = {n}; win probability p = 0.4", xlim=(0,n), ylim=(0,1.03))
        ax.grid(alpha=.17)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="outside lower center",ncol=1,frameon=False,fontsize=10)
    save(fig,"01-fixed-versus-optimal")


def draw_cycle():
    fig, ax = plt.subplots(figsize=(12.6,4.5))
    ax.set(xlim=(-.7,9.3),ylim=(-1.8,2.5))
    ax.axis("off")
    states, xs = [30,60,20,40,80], [0,2,4,6,8]
    for s,x in zip(states,xs):
        a = min(s,100-s)
        ax.add_patch(FancyBboxPatch((x-.52,.30),1.04,1.02,boxstyle="round,pad=.08",facecolor="#e4f1fa",edgecolor=BLUE,lw=1.4))
        ax.text(x,.94,f"capital {s}",ha="center",va="center",weight="bold",fontsize=12)
        ax.text(x,.56,f"stake {a}",ha="center",va="center",fontsize=11)
        terminal, outcome, prob = (0,"lose",.6) if 2*s<100 else (100,"win",.4)
        ax.annotate("",xy=(x,-.53),xytext=(x,.18),arrowprops={"arrowstyle":"->","color":GRAY,"lw":1.4})
        ax.text(x,-.76,f"{outcome} ({prob})\nSTOP at {terminal}",ha="center",va="center",fontsize=10,color=GRAY)
    for i,label in enumerate(("win: 0.4","lose: 0.6","win: 0.4","win: 0.4")):
        ax.annotate("",xy=(xs[i+1]-.62,.81),xytext=(xs[i]+.62,.81),arrowprops={"arrowstyle":"->","color":BLUE,"lw":2})
        ax.text((xs[i]+xs[i+1])/2,1.03,label,ha="center",fontsize=10,color=BLUE)
    ax.plot([8,8,2],[1.44,2.0,2.0],color=ORANGE,lw=2)
    ax.annotate("",xy=(2,1.43),xytext=(2,2.0),arrowprops={"arrowstyle":"->","color":ORANGE,"lw":2})
    ax.text(5,2.34,"lose at 80: probability 0.6; return to 60",ha="center",fontsize=11,color=ORANGE)
    ax.text(4,-1.55,"Every unabsorbed path follows these arrows.  One loop 60 → 20 → 40 → 80 → 60 has probability 0.6 × 0.4 × 0.4 × 0.6.",ha="center",fontsize=10)
    fig.suptitle("Bold play turns the target-100 problem into an exactly solvable loop",fontsize=14,y=.99)
    fig.subplots_adjust(top=.88,bottom=.10,left=.04,right=.98)
    save(fig,"02-bold-cycle")


if __name__ == "__main__":
    result = run_checks()
    draw_values()
    draw_cycle()
    result["svg_XML_parsing"] = "PASS (2 figures)"
    (OUT / "checks.json").write_text(json.dumps(result, indent=2) + "\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
