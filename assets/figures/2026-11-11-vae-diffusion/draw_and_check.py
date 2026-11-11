"""Original mathematical illustration and independent numeric checks.

Run: python draw_and_check.py (NumPy, SciPy, Matplotlib).
The binary example is a finite Markov-chain analogy, not Gaussian DDPM data.
All originals remain in raw/; this script creates only its own figure/checks.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.integrate import quad
from scipy.stats import norm, multivariate_normal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent
QCOLOR, PCOLOR, INK = "#147d92", "#b85f26", "#233347"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "text.color": INK, "axes.labelcolor": INK,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "svg.fonttype": "none", "figure.facecolor": "#ffffff"})

q0 = np.array([.8, .2])
f1 = np.array([[.75, .25], [.25, .75]])
f2 = np.array([[.6, .4], [.4, .6]])
q = q0[:, None, None] * f1[:, :, None] * f2[None, :, :]
q1, q2 = q.sum(axis=(0, 2)), q.sum(axis=(0, 1))
r1 = q.sum(axis=2) / q1[None, :]
r2 = q.sum(axis=0) / q2[None, :]
models = {
    "unfitted": q2[None, None, :] * np.full((2, 2, 1), .25),
    "images_match": q0[:, None, None] * np.full((1, 2, 1), .5) * q2[None, None, :],
    "exact_reverse": r1[:, :, None] * r2[None, :, :] * q2[None, None, :],
}


def kl(a, b):
    return float(np.sum(a * np.log(a / b)))


def numeric_checks():
    results = {}
    entropy = -float(np.sum(q0 * np.log(q0)))
    qcond = q / q0[:, None, None]
    assert np.allclose(q.reshape(2, 4), [[.36, .24, .08, .12], [.03, .02, .06, .09]])
    assert np.allclose(q1, [.65, .35]) and np.allclose(q2, [.53, .47])
    assert np.allclose(models["exact_reverse"], q)
    for name, p in models.items():
        p0 = p.sum(axis=(1, 2))
        pcond = p / p0[:, None, None]
        joint, marginal = kl(q, p), kl(q0, p0)
        gaps = np.array([kl(qcond[i], pcond[i]) for i in range(2)])
        elbos = np.sum(qcond * (np.log(p) - np.log(qcond)), axis=(1, 2))
        nll = -float(np.sum(q0 * np.log(p0)))
        assert abs(joint - marginal - q0 @ gaps) < 1e-13
        assert np.max(np.abs(np.log(p0) - elbos - gaps)) < 1e-13
        assert abs(-q0 @ elbos - entropy - joint) < 1e-13
        # Independently evaluate the endpoint + bridge-KL decomposition.
        terminal = sum(kl(qcond[i].sum(axis=0), q2) * q0[i] for i in range(2))
        p_r2 = p.sum(axis=0) / q2[None, :]
        p_r1 = p.sum(axis=2) / p.sum(axis=(0, 2))[None, :]
        recon = -float(np.sum(q.sum(axis=2) * np.log(p_r1)))
        bridge = 0.
        for i in range(2):
            for k in range(2):
                joint_ik = q[i, :, k].sum()
                bridge += joint_ik * kl(q[i, :, k] / joint_ik, p_r2[:, k])
        assert abs(terminal + bridge + recon + q0 @ elbos) < 1e-13
        true_step_kls = [sum(q1[j] * kl(r1[:,j], p_r1[:,j]) for j in range(2)),
                         sum(q2[k] * kl(r2[:,k], p_r2[:,k]) for k in range(2))]
        assert abs(joint - sum(true_step_kls)) < 1e-13
        results[name] = {"image_probabilities": p0.tolist(), "joint_kl": joint,
                         "image_kl": marginal, "posterior_kl_by_image": gaps.tolist(),
                         "average_posterior_kl": float(q0 @ gaps), "elbo_by_image": elbos.tolist(),
                         "average_nll": nll, "average_negative_elbo": float(-q0 @ elbos),
                         "decomposition": {"terminal_kl": terminal, "bridge_kl": bridge, "reconstruction": recon},
                         "true_reverse_step_kls": true_step_kls}
    # Closed-form Gaussian KL checked against direct integration.
    scalar = .5 * (np.log(1 / .25) - 1 + .25 + 1)
    integrated, _ = quad(lambda z: norm.pdf(z, 1, .5) *
                         (norm.logpdf(z, 1, .5) - norm.logpdf(z, 0, 1)), -np.inf, np.inf)
    assert abs(scalar - integrated) < 1e-11
    mq, mp = np.array([.7, -.3]), np.array([-.2, .5])
    sq, sp = np.array([[.7, .2], [.2, .5]]), np.array([[1.1, -.1], [-.1, .8]])
    delta = mq - mp
    general = .5 * (np.linalg.slogdet(sp)[1] - np.linalg.slogdet(sq)[1] - 2
                    + np.trace(np.linalg.solve(sp, sq)) + delta @ np.linalg.solve(sp, delta))
    nodes, weights = hermgauss(12)
    quadrature = 0.
    L = np.linalg.cholesky(sq)
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            z = mq + np.sqrt(2) * L @ np.array([a, b])
            quadrature += weights[i] * weights[j] / np.pi * (
                multivariate_normal.logpdf(z, mq, sq) - multivariate_normal.logpdf(z, mp, sp))
    assert abs(general - quadrature) < 1e-12
    # Continuous one-dimensional diffusion bridge, independent Bayes check.
    a1 = a2 = .5
    b2, abar2, x0, x2 = .5, .25, 1., .5
    bv = (1-a1) * b2 / (1-abar2)
    bm = (np.sqrt(a1)*b2*x0 + np.sqrt(a2)*(1-a1)*x2)/(1-abar2)
    denom = norm.pdf(x2, np.sqrt(abar2)*x0, np.sqrt(1-abar2))
    def bayes(x1):
        return (norm.pdf(x2, np.sqrt(a2)*x1, np.sqrt(b2))
                * norm.pdf(x1, np.sqrt(a1)*x0, np.sqrt(1-a1)) / denom)
    mass = quad(bayes, -np.inf, np.inf)[0]
    mean = quad(lambda z: z*bayes(z), -np.inf, np.inf)[0]
    variance = quad(lambda z: (z-mean)**2*bayes(z), -np.inf, np.inf)[0]
    grid = np.linspace(-3, 4, 101)
    assert np.max(np.abs([bayes(z)-norm.pdf(z, bm, np.sqrt(bv)) for z in grid])) < 1e-13
    assert max(abs(mass-1), abs(mean-bm), abs(variance-bv)) < 1e-11
    mu = .2
    local_kl = (bm-mu)**2 / (2*bv)
    local_integral = quad(lambda z: bayes(z) * (
        norm.logpdf(z, bm, np.sqrt(bv)) - norm.logpdf(z, mu, np.sqrt(bv))), -np.inf, np.inf)[0]
    assert abs(local_kl - local_integral) < 1e-10
    gradient = (mu-bm)/bv
    next_mu = mu - .1*gradient
    next_kl = (bm-next_mu)**2/(2*bv)
    eps = (x2 - np.sqrt(abar2)*x0)/np.sqrt(1-abar2)
    eps_theta = (x2 - np.sqrt(a2)*mu)*np.sqrt(1-abar2)/b2
    weight = b2*b2/(2*bv*a2*(1-abar2))
    assert abs(weight*(eps-eps_theta)**2 - local_kl) < 1e-13
    results["gaussian"] = {"scalar_kl": scalar, "scalar_quadrature": integrated,
        "matrix_kl": general, "matrix_quadrature": quadrature,
        "bridge_mean": bm, "bridge_variance": bv, "local_kl": local_kl,
        "local_quadrature": local_integral, "mean_gradient": gradient,
        "one_step_new_mean": next_mu, "one_step_new_kl": next_kl,
        "noise_weight": weight, "noise_target": eps, "noise_prediction": eps_theta}
    results["input"] = {"q0": q0.tolist(), "f1": f1.tolist(), "f2": f2.tolist(),
                        "q_joint": q.reshape(2,4).tolist(), "image_match_joint": models["images_match"].reshape(2,4).tolist()}
    results["verification"] = "PASS: normalizations, KL chain rule, both ELBO forms, Bayes bridge, Gaussian integration, noise parameterization."
    (OUT / "checks.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results


def joint_panel(ax, arr, heading, color):
    ax.axis("off")
    ax.set_xlim(-1.8, 4.8); ax.set_ylim(-.5, 2.9)
    ax.text(-1.7, 2.65, heading, fontsize=15, weight="bold", color=color)
    ax.text(1.55, 2.13, r"hidden path $Z=(x_1,x_2)$", ha="center", fontsize=12)
    for c, label in enumerate(["(0, 0)", "(0, 1)", "(1, 0)", "(1, 1)", "image total"]):
        ax.text(c, 1.69, label, ha="center", fontsize=11)
    for r, label in enumerate(["A = 0", "B = 1"]):
        y = .92 - r*.86
        ax.add_patch(Rectangle((-1.73, y-.12), .15, .22, facecolor="black" if r==0 else "white", edgecolor=INK, lw=1))
        ax.text(-.63, y, label, ha="right", va="center", fontsize=12)
        for c in range(4):
            ax.add_patch(Rectangle((c-.40, y-.31), .80, .62, facecolor=color, alpha=.08+arr[r,c]*.70, edgecolor="none"))
            ax.text(c, y, f"{arr[r,c]:.3f}", ha="center", va="center", fontsize=14)
        ax.text(4, y, f"{arr[r].sum():.3f}", ha="center", va="center", fontsize=16, weight="bold")
    ax.plot([3.5,3.5],[-.23,1.38], color="#abb7c3", lw=1)


def figure():
    p = models["images_match"]
    fig = plt.figure(figsize=(13,8.1))
    gs = fig.add_gridspec(2,2,height_ratios=[1.05,1],left=.055,right=.97,bottom=.13,top=.85,hspace=.48,wspace=.2)
    fig.suptitle("Matching image totals leaves room for different hidden paths", fontsize=20, weight="bold", y=.967)
    fig.text(.5,.908,"Every cell is one complete-path probability; adding a row gives the image probability.",ha="center",fontsize=12)
    joint_panel(fig.add_subplot(gs[0,0]), q.reshape(2,4), "Forward joint q", QCOLOR)
    joint_panel(fig.add_subplot(gs[0,1]), p.reshape(2,4), "Reverse-model joint p", PCOLOR)
    for i, name in enumerate(["A = 0", "B = 1"]):
        ax=fig.add_subplot(gs[1,i])
        qc=q[i].reshape(4)/q0[i]
        pc=p[i].reshape(4)/p[i].sum()
        xs=np.arange(4)
        a=ax.bar(xs-.18,qc,width=.34,color=QCOLOR,label="forward q(path | image)")
        b=ax.bar(xs+.18,pc,width=.34,color=PCOLOR,label="model p(path | image)")
        ax.bar_label(a,labels=[f"{x:.3f}" for x in qc],padding=4,fontsize=10)
        ax.bar_label(b,labels=[f"{x:.3f}" for x in pc],padding=4,fontsize=10)
        ax.set_xticks(xs,["(0, 0)","(0, 1)","(1, 0)","(1, 1)"])
        ax.set_ylim(0,.56); ax.set_yticks([0,.2,.4])
        ax.set_title(f"Given image {name}: divide its row by {q0[i]:.1f}",fontsize=12,pad=15)
        ax.set_xlabel(r"hidden path $(x_1,x_2)$")
        if i==0: ax.set_ylabel("conditional probability")
        ax.grid(axis="y",alpha=.14); ax.set_axisbelow(True)
    handles, labels=fig.axes[-1].get_legend_handles_labels()
    fig.legend(handles,labels,loc="lower center",bbox_to_anchor=(.5,.015),ncol=2,frameon=False,fontsize=12)
    fig.savefig(OUT/"binary-paths.svg")
    fig.savefig(OUT/"binary-paths.png",dpi=145)
    plt.close(fig)
    ET.parse(OUT/"binary-paths.svg")


if __name__ == "__main__":
    result=numeric_checks()
    figure()
    print(result["verification"])
    print(json.dumps(result["gaussian"],indent=2))
