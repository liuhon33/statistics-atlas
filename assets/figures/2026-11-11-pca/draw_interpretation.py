"""Original PCA interpretation figures; NumPy + Matplotlib, no downloaded data.

Run with Python 3.11+ and numpy/matplotlib. Outputs stay beside this script.
The two-feature data reproduce draw_pca.py without importing/rerunning it.
The four-feature spectrum is a separate constructed, sample-standardized toy.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = Path(__file__).resolve().parent
BLUE, ORANGE, GREEN, INK = "#2864a0", "#d97724", "#158477", "#263447"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "svg.hashsalt": "pca-interpretation",
    "axes.labelcolor": INK, "text.color": INK, "axes.titleweight": "bold",
})

a = np.r_[np.arange(-6, 0), np.arange(1, 7)].astype(float)
b = np.array([1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1.])
T = np.column_stack((a, b))
V = np.array([[1., 1.], [1., -1.]]) / np.sqrt(2)
X = T @ V.T
n = len(X)
C = X.T @ X / (n - 1)
lam = np.array([182., 12.]) / (n - 1)
sd = np.sqrt(np.diag(C))
L = V * np.sqrt(lam)[None, :] / sd[:, None]


def hadamard(order):
    h = np.ones((1, 1))
    while len(h) < order:
        h = np.block([[h, h], [h, -h]])
    return h


spectrum = np.array([2.4, 1.0, 0.4, 0.2])
q = hadamard(8)[:, 1:5] / np.sqrt(8)
v4 = hadamard(4) / 2
X4 = q @ np.diag(np.sqrt(7 * spectrum)) @ v4.T
pct = 100 * spectrum / spectrum.sum()
cum = np.cumsum(pct)


def save(fig, name):
    svg = OUT / f"{name}.svg"
    fig.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    fig.savefig(OUT / f"{name}.png", dpi=170, bbox_inches="tight")
    ET.parse(svg)
    plt.close(fig)


fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), layout="constrained")
pcs = np.arange(1, 5)
axes[0].plot(pcs, spectrum, "o-", color=BLUE, lw=2)
axes[0].set(ylabel="PC variance (eigenvalue)", ylim=(0, 2.8), title="Scree: spread per PC")
for j, val in zip(pcs, spectrum):
    axes[0].annotate(f"{val:g}", (j, val), xytext=(0, 9), textcoords="offset points", ha="center")
axes[1].bar(pcs, pct, color=[BLUE, ORANGE, "#a7bacb", "#ccd6df"], width=.65)
axes[1].set(ylabel="Share of total variance (%)", ylim=(0, 74), title="Explained variance: share")
for j, val in zip(pcs, pct):
    axes[1].text(j, val + 2, f"{val:g}%", ha="center")
axes[2].plot(pcs, cum, "o-", color=GREEN, lw=2)
axes[2].axhline(90, color=INK, ls="--", lw=1)
axes[2].text(1.05, 92, "90% example target", fontsize=9, va="bottom")
axes[2].set(ylabel="Variance kept through this PC (%)", ylim=(45, 109), title="Cumulative: running total")
for j, val in zip(pcs, cum):
    axes[2].annotate(f"{val:g}%", (j, val), xytext=(0, 8), textcoords="offset points", ha="center")
for ax in axes:
    ax.set(xticks=pcs, xticklabels=[f"PC{j}" for j in pcs])
    ax.grid(axis="y", alpha=.15)
fig.suptitle("Separate four-feature toy: 60% + 25% = 85%; three PCs reach 95%", fontsize=13)
save(fig, "06-variance-reading")


def score_axes(ax):
    ax.scatter(*T.T, s=37, color=BLUE, zorder=3)
    ax.scatter(*T[-1], s=65, color=GREEN, zorder=4)
    ax.annotate("S12 (6, 1)", T[-1], xytext=(-2, -19), textcoords="offset points", ha="right", color=GREEN)
    ax.annotate("S1", T[0], xytext=(0, 8), textcoords="offset points", ha="center")
    ax.axhline(0, color="#b8c1ca", lw=.8)
    ax.axvline(0, color="#b8c1ca", lw=.8)
    ax.set(xlim=(-7, 7), ylim=(-4.8, 4.8), xlabel="PC1 score (93.8% of variance)",
           ylabel="PC2 score (6.2% of variance)")
    ax.set_aspect("equal", adjustable="box")


fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), layout="constrained")
for ax in axes:
    score_axes(ax)
axes[0].set_title("Score plot: each dot is a sample")
axes[0].text(.5, .94, "Right = larger shared A + B pattern\nUp = more A relative to B", ha="center",
             va="top", transform=axes[0].transAxes, fontsize=10)
axes[1].set_title("Biplot: samples + feature arrows")
arrow_scale = 3.
for row, label, col in zip(V, ["A", "B"], [ORANGE, GREEN]):
    tip = arrow_scale * row
    axes[1].annotate("", xy=tip, xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=2.4, color=col))
    axes[1].text(tip[0] - .1, tip[1] + (.3 if tip[1] > 0 else -.5), label, color=col, fontsize=12)
direction = V[0]
foot = np.dot(T[-1], direction) * direction
axes[1].plot([0, 4.5], [0, 4.5], ls=":", lw=1, color=ORANGE)
axes[1].plot([T[-1, 0], foot[0]], [T[-1, 1], foot[1]], ls="--", color="#83909c", lw=1.2)
axes[1].scatter(*foot, marker="s", s=22, color=ORANGE)
axes[1].annotate("Read along A,\nnot distance to its tip", foot, xytext=(-52, 17),
                 textcoords="offset points", ha="center", fontsize=9)
fig.suptitle("Original twelve samples; both PCs shown, so no dimension is hidden", fontsize=13)
fig.supxlabel("Biplot convention: dots = raw scores T; arrows = 3 × coefficient loadings V (display scale only).", fontsize=10)
save(fig, "07-scores-biplot-reading")


fig, axes = plt.subplots(1, 2, figsize=(9.7, 4.9), layout="constrained")
for ax, data, title, xlabel, ylabel in zip(
    axes, [V, L], ["Coefficient loadings: recipe weights", "Correlation circle: feature–PC correlations"],
    ["Weight in PC1", "Correlation with PC1"], ["Weight in PC2", "Correlation with PC2"],
):
    ax.axhline(0, color="#b8c1ca", lw=.8)
    ax.axvline(0, color="#b8c1ca", lw=.8)
    for row, label, col in zip(data, ["A", "B"], [ORANGE, GREEN]):
        ax.annotate("", xy=row, xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=2.6, color=col))
        ax.text(row[0] + .045, row[1] + (.035 if row[1] > 0 else -.09), label, color=col, fontsize=12)
    ax.set(xlim=(-1.15, 1.22), ylim=(-1.15, 1.15), xlabel=xlabel, ylabel=ylabel, title=title)
    ax.set_aspect("equal")
axes[0].text(-1.02, .91, "A: (0.707, 0.707)\nB: (0.707, −0.707)", fontsize=10, va="top")
axes[0].text(-1.02, -1.03, "90° here does NOT mean zero correlation.", fontsize=9)
axes[1].add_patch(Circle((0, 0), 1, fill=False, color="#9daab7", ls="--", lw=1))
axes[1].text(-1.04, .91, "A: (0.969, 0.249)\nB: (0.969, −0.249)", fontsize=10, va="top")
axes[1].text(-1.02, -1.03, "Here cos(angle) = corr(A, B) = 0.876.", fontsize=9)
fig.suptitle("Same data, different arrow scaling: always check what 'loadings' means", fontsize=13)
save(fig, "08-loading-correlation-reading")

# Numerical support for the analytic explanations in the note.
errors = {}
def check(name, observed, expected, tol=1e-11):
    err = float(np.max(np.abs(np.asarray(observed) - np.asarray(expected))))
    errors[name] = err
    assert err < tol, (name, err)

check("centering", X.mean(0), 0)
check("scores_from_recipe", X @ V, T)
check("scores_sample_covariance", np.cov(T, rowvar=False), np.diag(lam))
check("reconstruction", T @ V.T, X)
check("feature_pc_correlations", np.corrcoef(X.T, T.T)[:2, 2:], L)
check("full_correlation_from_arrows", L @ L.T, np.corrcoef(X, rowvar=False))
check("correlation_circle_radius", np.sum(L**2, axis=1), 1)
check("raw_coefficient_arrow_dot", V[0] @ V[1], 0)
check("true_feature_correlation", L[0] @ L[1], 85 / 97)
check("single_pc_feature_cos2", L[:, 0]**2, 91 / 97)
check("coefficient_contributions_sum", np.sum(V**2, axis=0), 1)
check("biplot_display_scale_undone", (T @ (arrow_scale * V).T) / arrow_scale, X)
check("simple_scores", np.array([[2, 2], [-2, -2], [2, -2]]) @ V,
      np.array([[2*np.sqrt(2), 0], [-2*np.sqrt(2), 0], [0, 2*np.sqrt(2)]]))
check("separate_four_feature_centering", X4.mean(0), 0)
check("separate_four_feature_unit_variance", X4.var(0, ddof=1), 1)
check("separate_four_feature_spectrum", np.linalg.eigvalsh(np.cov(X4, rowvar=False))[::-1], spectrum)
check("separate_four_feature_cumulative", cum, [60, 85, 95, 100])
u, d, vt = np.linalg.svd(X, full_matrices=False)
check("svd_scores", X @ vt.T, u * d)
check("svd_eigenvalues", d*d/(n-1), lam)
check("rank_one_residual", np.sum((X - T[:, :1] @ V[:, :1].T)**2), 12)
# General rectangular/truncated check: dot products of correlation arrows need
# not equal correlations, but omitted-component Cauchy–Schwarz bounds the error.
u4, d4, vt4 = np.linalg.svd(X4, full_matrices=False)
lam4 = d4**2 / 7
l4 = vt4.T * np.sqrt(lam4)
quality = np.sum(l4[:, :2]**2, axis=1)
diff = np.abs(np.corrcoef(X4, rowvar=False) - l4[:, :2] @ l4[:, :2].T)
bound = np.sqrt((1-quality)[:, None] * (1-quality)[None, :])
assert np.all(diff <= bound + 1e-12)
pair_diff = X[:, None, :] - X[None, :, :]
score_diff = T[:, None, :] - T[None, :, :]
check("full_score_distances", np.sum(pair_diff**2, axis=2), np.sum(score_diff**2, axis=2))
assert np.all(score_diff[:, :, 0]**2 <= np.sum(pair_diff**2, axis=2) + 1e-12)

data = {"two_feature_centered": X.tolist(), "scores": T.tolist(), "coefficient_loadings": V.tolist(),
        "correlation_loadings": L.tolist(), "four_feature_sample_standardized": X4.tolist(),
        "four_feature_eigenvalues": spectrum.tolist()}
(OUT / "interpretation-data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
report = {"status": "PASS", "numerical_errors": errors,
          "truncated_correlation_error_bound": "PASS", "projection_distance_contraction": "PASS",
          "svg_xml_parse": "PASS (3 files)", "max_numerical_error": max(errors.values()),
          "scope": "Independent numerical support; not a proof or live Obsidian rendering check."}
(OUT / "interpretation-checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
