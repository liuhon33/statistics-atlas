"""Original coefficient examples, penalty geometry and MAP-prior illustrations.

Run with Python + NumPy, SciPy, Matplotlib and Pillow. All data are constructed.
No original lecture/source image is modified. The directory is resolved from
this script, not from the shell working directory. SVGs and PNGs are deterministic.
"""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.integrate import quad

OUT = Path(__file__).resolve().parent
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "svg.hashsalt": "l1-l2-elastic-net-2026-11-12",
                     "axes.spines.top": False, "axes.spines.right": False})
Z = np.array([3.0, 0.6])
SPECS = {
    "ridge": ("Ridge: shrink without a zero threshold", 0., 1., "#2563a6", "Gaussian prior"),
    "lasso": ("Lasso: shrink and set a small coefficient to zero", 1., 0., "#c96019", "Laplace prior"),
    "elastic-net": ("Elastic net: threshold, then shrink what remains", 1., 1., "#168477", "Product prior (not a mixture)"),
}


def soft(z, lam):
    return np.sign(z) * np.maximum(np.abs(z) - lam, 0.)


def solution(z, l1, l2):
    return soft(np.asarray(z), l1) / (1. + l2)


def penalty(b, l1, l2):
    return l1 * np.abs(b).sum(axis=-1) + l2 / 2 * (b * b).sum(axis=-1)


def save(fig, stem):
    fig.savefig(OUT / f"{stem}.svg", metadata={"Date": None}, facecolor="white")
    fig.savefig(OUT / f"{stem}.png", dpi=150, metadata={"Software": "Matplotlib"}, facecolor="white")
    plt.close(fig)
    p = OUT / f"{stem}.svg"
    p.write_text("\n".join(x.rstrip() for x in p.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    ET.parse(p)


def intro(key, title, l1, l2, color):
    b = solution(Z, l1, l2)
    fig, ax = plt.subplots(figsize=(8.6, 3.7))
    fig.subplots_adjust(left=.10, right=.98, bottom=.22, top=.77)
    x = np.arange(2)
    for offset, vals, col, label in [(-.17, Z, "#a8afb8", "No penalty"), (.17, b, color, "Penalized fit")]:
        bars = ax.bar(x + offset, vals, .30, color=col, label=label)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, val + .08, f"{val:g}", ha="center", weight="bold")
    ax.axhline(0, color="#555", lw=.8)
    ax.set(xticks=x, xticklabels=[r"Coefficient $\beta_1$", r"Coefficient $\beta_2$"],
           ylabel="Fitted coefficient", ylim=(0, 3.65), yticks=[0, 1, 2, 3])
    ax.legend(frameon=False, loc="upper right")
    fig.suptitle(title, fontsize=14, y=.97, weight="bold")
    fig.text(.5, .85, r"Toy loss: $\frac{1}{2}[(\beta_1-3)^2+(\beta_2-0.6)^2]$"
             + f"     |     weights: λ₁ = {l1:g}, λ₂ = {l2:g}", ha="center", fontsize=11)
    fig.text(.5, .035, "The same separable data-fit loss is used in all three examples; penalty weights are illustrative, not tuned.",
             ha="center", fontsize=9, color="#414b57")
    save(fig, f"{key}-intro")


def mechanics(key, title, l1, l2, color, prior_title):
    b = solution(Z, l1, l2)
    t = penalty(b, l1, l2)
    theta = np.linspace(0, 2*np.pi, 1441)
    directions = np.stack([np.cos(theta), np.sin(theta)], axis=-1)
    A = l1 * np.abs(directions).sum(axis=-1)
    radius = 2*t / (A + np.sqrt(A*A + 2*l2*t))
    boundary = radius[:, None] * directions
    boundary_error = np.max(np.abs(penalty(boundary, l1, l2) - t))
    assert boundary_error < 2e-14
    fig, (ax, pr) = plt.subplots(1, 2, figsize=(10.2, 4.5), gridspec_kw={"width_ratios": [1.12, 1]})
    fig.subplots_adjust(left=.07, right=.97, bottom=.23, top=.81, wspace=.33)
    ax.fill(boundary[:, 0], boundary[:, 1], color=color, alpha=.12)
    ax.plot(boundary[:, 0], boundary[:, 1], color=color, lw=2)
    circle = Z + np.linalg.norm(Z-b) * directions
    ax.plot(circle[:, 0], circle[:, 1], color="#88929e", ls="--", lw=1.5)
    ax.scatter(*Z, color="#535b66", marker="x", s=65, zorder=4)
    ax.scatter(*b, color=color, s=60, zorder=5)
    ax.annotate("No-penalty fit", Z, xytext=(-28, 30), textcoords="offset points", ha="center", fontsize=9)
    ax.annotate(f"Optimum ({b[0]:g}, {b[1]:g})", b, xytext=(5, -33), textcoords="offset points", color=color, fontsize=9)
    ax.axhline(0, lw=.7, color="#c5ccd5", zorder=0)
    ax.axvline(0, lw=.7, color="#c5ccd5", zorder=0)
    ax.set(xlim=(-2.25, 3.8), ylim=(-2.2, 2.3), xlabel=r"Coefficient $\beta_1$", ylabel=r"Coefficient $\beta_2$")
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Penalty budget meets a loss contour", fontsize=11, pad=12)
    u = np.linspace(-3.2, 3.2, 1601)
    scalar_penalty = lambda v: l1*abs(v) + .5*l2*v*v
    normalizer = quad(lambda v: np.exp(-scalar_penalty(v)), -np.inf, np.inf, epsabs=1e-12)[0]
    density = np.exp(-l1*np.abs(u) - .5*l2*u*u) / normalizer
    pr.plot(u, density, color=color, lw=2.5)
    pr.fill_between(u, density, color=color, alpha=.10)
    pr.axvline(0, color="#c5ccd5", lw=.8)
    pr.set(xlim=(-3.2, 3.2), ylim=(0, .96), xlabel=r"One coefficient $u$", ylabel="Prior density")
    pr.set_title(prior_title + "  (noise variance = 1)", fontsize=10.5, pad=12)
    pr.text(.5, .9, r"$p(u)\propto\exp[-\lambda_1|u|-\lambda_2u^2/2]$", transform=pr.transAxes, ha="center", fontsize=10)
    fig.suptitle({"ridge": "Ridge: a smooth boundary and a smooth log prior",
                  "lasso": "Lasso: an axis corner and a cusp in the log prior",
                  "elastic-net": "Elastic net: curved sides, retained corners"}[key], fontsize=14, weight="bold", y=.97)
    fig.text(.5, .075, "Left: coefficient space, not observations. Shading is P(β) ≤ P(optimum); dashed gray is equal data-fit loss.", ha="center", fontsize=9)
    fig.text(.5, .03, "Right: normalized continuous densities, not probabilities at zero. All panels use the same axes; prior variances differ.", ha="center", fontsize=9)
    save(fig, f"{key}-mechanics")
    return float(boundary_error), float(normalizer)


def checks():
    rng = np.random.default_rng(2701)
    expected = {"ridge": [1.5, .3], "lasso": [2., 0.], "elastic-net": [1., 0.]}
    max_kkt = 0.
    max_map_constant_error = 0.
    scalar_cases = 0
    for l1, l2 in [(0, 0), (0, 1), (1, 0), (1, 1), (.3, 2.4)]:
        z = np.r_[rng.normal(size=500), -l1, 0, l1]
        b = solution(z, l1, l2)
        grad = b-z+l2*b
        residual = np.where(b != 0, np.abs(grad + l1*np.sign(b)), np.maximum(np.abs(grad)-l1, 0))
        max_kkt = max(max_kkt, float(residual.max()))
        scalar_cases += len(z)
        sigma2 = 1.7
        v = rng.normal(size=1000)
        objective = .5*(v-.6)**2 + l1*np.abs(v) + l2*v*v/2
        neg_log_unnormalized_posterior = (v-.6)**2/(2*sigma2) + (l1*np.abs(v)+l2*v*v/2)/sigma2
        max_map_constant_error = max(max_map_constant_error, float(np.max(np.abs(objective-sigma2*neg_log_unnormalized_posterior))))
    assert max_kkt < 2e-14 and max_map_constant_error < 2e-14
    competitors = rng.uniform(-5, 5, size=(10000, 2))
    margins = {}
    for key, (_, l1, l2, _, _) in SPECS.items():
        b = solution(Z, l1, l2)
        np.testing.assert_allclose(b, expected[key], atol=1e-14)
        obj = lambda v: .5*((v-Z)**2).sum(axis=-1) + penalty(v, l1, l2)
        margins[key] = float(np.min(obj(competitors)-obj(b)))
        assert margins[key] >= -1e-14
    X = rng.normal(size=(9, 4)); X -= X.mean(axis=0)
    y = rng.normal(size=9); y -= y.mean()
    lam = .7
    ridge = np.linalg.solve(X.T@X + lam*np.eye(4), X.T@y)
    augmented = np.linalg.lstsq(np.vstack([X, np.sqrt(lam)*np.eye(4)]), np.r_[y, np.zeros(4)], rcond=None)[0]
    ridge_error = float(np.max(np.abs(ridge-augmented)))
    assert ridge_error < 1e-12
    # Identical columns: lasso has a continuum of nonnegative splits; EN picks equal shares.
    splits = np.linspace(0, 2, 201)
    lasso_obj = .5*(3-2)**2 + np.abs(splits) + np.abs(2-splits)
    np.testing.assert_allclose(lasso_obj, 2.5)
    identical_en = np.array([2/3, 2/3])
    identical_en_grad = np.repeat(identical_en.sum()-3, 2) + 1 + identical_en
    assert np.max(np.abs(identical_en_grad)) < 1e-14
    # Positive posterior mean despite a lasso MAP of exactly zero.
    post = lambda v: np.exp(-.5*(v-.6)**2-abs(v))
    norm = quad(post, -np.inf, np.inf)[0]
    mean = quad(lambda v: v*post(v), -np.inf, np.inf)[0]/norm
    assert soft(.6, 1) == 0 and mean > .05
    return {"status": "pass", "example_ols": Z.tolist(), "expected_fits": expected,
            "scalar_kkt_cases": scalar_cases, "max_kkt_residual": max_kkt,
            "max_map_objective_identity_error": max_map_constant_error,
            "random_competitors_per_method": len(competitors), "min_competitor_objective_gaps": margins,
            "ridge_vs_augmented_least_squares_max_error": ridge_error,
            "identical_columns_elastic_net_coefficients": identical_en.tolist(),
            "laplace_posterior_example": {"observation": .6, "noise_variance": 1., "laplace_scale": 1., "mode": 0., "mean": mean},
            "limits": "Numerical checks support the analytic derivations; no data-driven prediction guarantee or live Obsidian rendering is tested."}


def main():
    report = checks()
    report["geometry"] = {}
    for key, (title, l1, l2, color, prior_title) in SPECS.items():
        intro(key, title, l1, l2, color)
        err, normalizer = mechanics(key, title, l1, l2, color, prior_title)
        report["geometry"][key] = {"boundary_max_error": err, "prior_normalizer_sigma2_1": normalizer}
    for suffix in ["intro", "mechanics"]:
        images = [Image.open(OUT/f"{key}-{suffix}.png").convert("RGB") for key in SPECS]
        width = max(i.width for i in images)
        contact = Image.new("RGB", (width, sum(i.height for i in images)), "white")
        y0 = 0
        for im in images:
            contact.paste(im, ((width-im.width)//2, y0)); y0 += im.height
        contact.save(OUT/f"preview-{suffix}.png")
    report["artifact_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob("*.svg"))}
    (OUT/"checks.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
