"""Original MLE/MAP comparison; run with Python + matplotlib, numpy, scipy, sympy.

No randomness or network access. Outputs stay beside this file. The likelihood
is for the exact ordered sequence, NOT the binomial count. Its raw vertical
scale is preserved; only prior and posterior are densities over theta.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.stats import beta
import sympy as sp


OUT = Path(__file__).resolve().parent
STEM = "mle-map-comparison"
SEQUENCE = "HHTHHHTHHH"
COLORS = {"prior": "#346ca9", "likelihood": "#c77810", "posterior": "#228467"}
INK = "#18304a"


def verify_math() -> dict:
    t = sp.Symbol("theta", real=True)
    heads, tails = SEQUENCE.count("H"), SEQUENCE.count("T")
    assert (heads, tails) == (8, 2)
    prior = 30 * t**2 * (1 - t)**2
    likelihood = t**heads * (1 - t)**tails
    evidence = sp.integrate(prior * likelihood, (t, 0, 1))
    posterior = sp.factor(prior * likelihood / evidence)
    assert evidence == sp.Rational(2, 1001)
    assert sp.expand(posterior - 15015 * t**10 * (1 - t)**4) == 0
    integrals = [sp.integrate(f, (t, 0, 1)) for f in (prior, likelihood, posterior)]
    assert integrals == [1, sp.Rational(1, 495), 1]
    modes = [sp.Rational(1, 2), sp.Rational(4, 5), sp.Rational(5, 7)]
    for f, mode in zip((prior, likelihood, posterior), modes):
        assert sp.diff(f, t).subs(t, mode) == 0
        assert sp.diff(f, t, 2).subs(t, mode) < 0
        assert f.subs(t, 0) == f.subs(t, 1) == 0
    # Analytic score/curvature checks, valid on the open unit interval.
    for f, a, b in ((likelihood, 8, 2), (posterior, 10, 4)):
        score = sp.diff(f, t) / f
        assert sp.simplify(score - (a / t - b / (1 - t))) == 0
        assert sp.simplify(sp.diff(score, t) + a / t**2 + b / (1 - t)**2) == 0
    assert sp.Rational(10, 14) * sp.Rational(4, 5) + sp.Rational(4, 14) / 2 == modes[2]

    grid = np.linspace(0, 1, 2001)
    funcs = [sp.lambdify(t, f, "numpy") for f in (prior, likelihood, posterior)]
    errors = {
        "prior_vs_scipy_beta_pdf": float(np.max(np.abs(funcs[0](grid) - beta.pdf(grid, 3, 3)))),
        "posterior_vs_scipy_beta_pdf": float(np.max(np.abs(funcs[2](grid) - beta.pdf(grid, 11, 5)))),
    }
    for i, (f, expected_area, mode) in enumerate(zip(funcs, integrals, modes)):
        area, _ = quad(f, 0, 1, epsabs=1e-12)
        optimum = minimize_scalar(lambda x: -f(x), bounds=(0, 1), method="bounded", options={"xatol": 1e-14})
        errors[f"panel_{i + 1}_area"] = abs(area - float(expected_area))
        errors[f"panel_{i + 1}_mode"] = abs(float(optimum.x) - float(mode))
        assert optimum.success
    assert max(errors.values()) < 5e-8, errors
    return {
        "assumptions": "Independent Bernoulli tosses conditional on fixed theta in [0,1]; Beta(3,3) prior.",
        "observation": {"ordered_sequence": SEQUENCE, "heads": heads, "tails": tails},
        "exact": {
            "prior_density": "30*theta^2*(1-theta)^2 = Beta(3,3) density",
            "likelihood": "theta^8*(1-theta)^2; probability of the exact observed sequence",
            "evidence": str(evidence),
            "posterior_density": "15015*theta^10*(1-theta)^4 = Beta(11,5) density",
            "integrals_over_theta": [str(x) for x in integrals],
            "prior_mode_MLE_MAP": [str(x) for x in modes],
            "scores_and_strictly_negative_curvatures": "symbolically verified on 0 < theta < 1",
            "boundary_values": "all three functions are zero at theta=0 and theta=1",
            "MAP_weighted_average": "(10/14)*(4/5) + (4/14)*(1/2) = 5/7",
        },
        "numerical_absolute_errors": errors,
    }


def draw() -> dict:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK,
        "ytick.color": INK, "axes.edgecolor": "#bac5ce",
        "svg.fonttype": "none", "svg.hashsalt": "mle-map-2026-11-15",
    })
    fig, axes = plt.subplots(1, 3, figsize=(16, 6.2), dpi=160)
    fig.patch.set_facecolor("#ffffff")
    fig.subplots_adjust(left=0.065, right=0.98, bottom=0.27, top=0.70, wspace=0.33)
    fig.suptitle("Same data, different question: MLE versus MAP", x=0.05, y=0.965, ha="left", fontsize=22, weight="bold")
    fig.text(0.05, 0.885, "Observed sequence: HHTHHHTHHH  (8 heads, 2 tails).  Tosses are independent given " + r"$\theta$" + ".", fontsize=13)

    theta = np.linspace(0, 1, 2001)
    curves = [30 * theta**2 * (1 - theta)**2, theta**8 * (1 - theta)**2, 15015 * theta**10 * (1 - theta)**4]
    titles = ["1  Prior: before these tosses", "2  Likelihood: fit to these tosses", "3  Posterior: after these tosses"]
    formulas = [r"$\pi(\theta)=30\theta^2(1-\theta)^2$", r"$L(\theta;x)=\theta^8(1-\theta)^2$", r"$p(\theta\mid x)=15015\theta^{10}(1-\theta)^4$"]
    modes = [0.5, 0.8, 5 / 7]
    ymax = [2.35, 0.0085, 4.05]
    density_names = ["Prior density", "Probability of this exact sequence", "Posterior density"]
    labels = ["Prior mode = 0.50", "MLE = 0.80", "MAP = 5/7 = 0.714..."]
    callout_positions = [(0.10, 0.95), (0.12, 0.95), (0.04, 0.95)]
    footers = ["Area over theta = 1\nA distribution for the unknown parameter", "Area over theta = 1/495, not 1\nNOT a distribution for the parameter", "Area over theta = 1\nLikelihood x prior, then normalize"]

    for ax, y, key, title, formula, mode, ytop, ylabel, label, pos, footer in zip(
        axes, curves, COLORS, titles, formulas, modes, ymax, density_names, labels, callout_positions, footers
    ):
        color = COLORS[key]
        ax.set_facecolor("#f9fbfd")
        ax.plot(theta, y, color=color, lw=2.6)
        ax.fill_between(theta, 0, y, color=color, alpha=0.13)
        height = float(np.interp(mode, theta, y))
        ax.vlines(mode, 0, height, colors=color, ls="--", lw=1.5)
        ax.scatter([mode], [height], color=color, s=38, zorder=5)
        ax.annotate(label, xy=(mode, height), xytext=pos, textcoords="axes fraction",
                    ha="left", va="top", fontsize=12.5, color=color, weight="bold",
                    arrowprops={"arrowstyle": "->", "color": color, "lw": 1.1},
                    bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92})
        ax.set_xlim(0, 1)
        ax.set_ylim(0, ytop)
        ax.set_xticks(np.linspace(0, 1, 6))
        ax.set_xlabel(r"$\theta$: probability of heads", labelpad=7)
        ax.set_ylabel(ylabel, labelpad=8, fontsize=11.5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.18)
        ax.set_axisbelow(True)
        ax.text(0, 1.22, title, transform=ax.transAxes, color=color, fontsize=13, weight="bold")
        ax.text(0, 1.07, formula, transform=ax.transAxes, fontsize=13)
        ax.text(0.5, -0.35, footer, transform=ax.transAxes, ha="center", va="top", fontsize=11, linespacing=1.5)

    axes[0].set_yticks([0, 0.5, 1, 1.5, 2])
    axes[1].set_yticks([0, 0.002, 0.004, 0.006, 0.008])
    axes[2].set_yticks([0, 1, 2, 3, 4])
    axes[2].axvline(0.8, color=COLORS["likelihood"], ls=":", lw=1.7)
    axes[2].text(0.81, 0.055, "MLE", transform=axes[2].get_xaxis_transform(), color=COLORS["likelihood"], fontsize=10.5)
    fig.text(0.05, 0.035, "Same horizontal scale; separate vertical scales.  Colors now identify functions, not disease groups.", fontsize=11.5, color="#4a5f72")

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = []
    for artist in fig.findobj(matplotlib.text.Text):
        if not artist.get_visible() or not artist.get_text():
            continue
        box = artist.get_window_extent(renderer)
        assert box.x0 >= -1 and box.y0 >= -1, artist.get_text()
        assert box.x1 <= fig.bbox.width + 1 and box.y1 <= fig.bbox.height + 1, artist.get_text()
        boxes.append(artist.get_text())
    svg, png = OUT / f"{STEM}.svg", OUT / f"{STEM}.png"
    fig.savefig(svg, metadata={"Date": None, "Creator": "Original deterministic MLE/MAP comparison"})
    fig.savefig(png, metadata={"Software": "Original deterministic MLE/MAP comparison"})
    plt.close(fig)
    # Matplotlib's path serializer leaves trailing spaces; remove only those.
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    root = ET.parse(svg).getroot()
    assert root.tag.endswith("svg")
    return {"svg_xml": "PASS", "visible_text_bounds": "PASS", "text_objects_checked": len(boxes),
            "shared_x_limits": [0, 1], "independent_y_limits": ymax,
            "raw_likelihood_scale_preserved": True, "animation": "Not needed: simultaneous three-function comparison"}


def main() -> None:
    report = {"math": verify_math(), "figure": draw()}
    files = [Path(__file__).resolve(), OUT / f"{STEM}.svg", OUT / f"{STEM}.png"]
    report["sha256"] = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    (OUT / "checks.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "figure": str(OUT / f"{STEM}.svg"), "checks": str(OUT / "checks.json")}, indent=2))


if __name__ == "__main__":
    main()
