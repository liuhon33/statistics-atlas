"""Original SVD illustration and numerical checks for the accompanying reference note.

Run with Python, NumPy and Matplotlib. The handwritten PDF is never modified.
The checks illustrate identities whose general justifications are in the note.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np

OUT = Path(__file__).resolve().parent
TOL = 1e-11
checks = {}


def check(name, actual, expected):
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    assert error < TOL, (name, error)
    checks[name] = error


def rotation(degrees):
    t = np.deg2rad(degrees)
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


# The fully specified two-dimensional example in the original illustration.
U, V = rotation(35), rotation(-25)
S = np.diag([2.0, 0.75])
A = U @ S @ V.T
check("figure_singular_values", np.linalg.svd(A, compute_uv=False), [2, .75])
check("figure_paired_directions", A @ V, U @ S)

theta = np.linspace(0, 2 * np.pi, 501)
circle = np.stack([np.cos(theta), np.sin(theta)])
x = V @ np.array([np.cos(np.deg2rad(50)), np.sin(np.deg2rad(50))])
transforms = [np.eye(2), V.T, S @ V.T, A]
curve_points = [M @ circle for M in transforms]
basis_points = [M @ V for M in transforms]
tracked_points = [M @ x for M in transforms]
check("first_orthogonal_stage_preserves_lengths", np.linalg.norm(curve_points[1], axis=0), 1)
check("last_orthogonal_stage_preserves_lengths", np.linalg.norm(curve_points[3], axis=0), np.linalg.norm(curve_points[2], axis=0))
check("ellipse_axis_lengths", np.linalg.norm(basis_points[3], axis=0), [2, .75])

# Exact example introduced on p. 2 of the supplied notes, including paired signs.
An = np.array([[4., 4.], [-3., 3.]])
Un = np.diag([1., -1.])
Sn = np.diag([4 * np.sqrt(2), 3 * np.sqrt(2)])
Vn = np.array([[1., 1.], [1., -1.]]) / np.sqrt(2)
check("notes_example_reconstruction", Un @ Sn @ Vn.T, An)
check("notes_example_pairing", An @ Vn, Un @ Sn)
check("notes_example_gram", An.T @ An, [[25, 7], [7, 25]])

# A nonsquare rank-deficient case checks dimensions and all four subspaces.
B = np.array([[1., 2., 3., 4.], [2., 4., 6., 8.], [0., 1., 0., 1.]])
Ub, sb, Vbt = np.linalg.svd(B, full_matrices=True)
rb = int(np.linalg.matrix_rank(B))
Sfull = np.zeros(B.shape)
np.fill_diagonal(Sfull, sb)
Ur, Sr, Vr = Ub[:, :rb], np.diag(sb[:rb]), Vbt.T[:, :rb]
check("rectangular_full_svd", Ub @ Sfull @ Vbt, B)
check("rectangular_compact_svd", Ur @ Sr @ Vr.T, B)
check("rectangular_AtA", Vbt.T @ Sfull.T @ Sfull @ Vbt, B.T @ B)
check("rectangular_AAt", Ub @ Sfull @ Sfull.T @ Ub.T, B @ B.T)
check("right_null_basis", B @ Vbt.T[:, rb:], 0)
check("left_null_basis", B.T @ Ub[:, rb:], 0)
check("constructed_left_vectors", B @ Vr @ np.linalg.inv(Sr), Ur)
check("left_vectors_orthonormal", Ur.T @ Ur, np.eye(rb))
P, Q = Ur @ Ur.T, Vr @ Vr.T
check("column_projector_idempotent", P @ P, P)
check("row_projector_idempotent", Q @ Q, Q)
Bplus = Vr @ np.linalg.inv(Sr) @ Ur.T
check("pseudoinverse", Bplus, np.linalg.pinv(B))
check("fitted_projection", B @ Bplus, P)

# The diagonal truncation example in the notes (p. 12).
D, D2 = np.diag([4., 3., 2., 1.]), np.diag([4., 3., 0., 0.])
check("rank_two_spectral_error", np.linalg.norm(D - D2, 2), 2)
check("rank_two_frobenius_error", np.linalg.norm(D - D2, "fro"), np.sqrt(5))
check("rank_two_nuclear_error", np.linalg.norm(D - D2, "nuc"), 3)
check("frobenius_from_singular_values", np.linalg.norm(B, "fro"), np.linalg.norm(sb))

# A counterexample to the handwritten normal => U=V implication.
N = np.diag([2., -1.])
check("normal_counterexample_commutes", N.T @ N, N @ N.T)
assert np.linalg.eigvalsh(N).min() < 0  # U Sigma U^T would be positive semidefinite.
check("determinant_absolute_value", np.prod(np.linalg.svd(N, compute_uv=False)), abs(np.linalg.det(N)))
Qpolar = Un @ Vn.T
Hleft = Un @ Sn @ Un.T
check("square_left_polar", Hleft @ Qpolar, An)
check("square_polar_orthogonal", Qpolar.T @ Qpolar, np.eye(2))
check("square_polar_positive_factor", Hleft @ Hleft, An @ An.T)

# PCA in both storage orientations, with centering and sample denominator explicit.
X0 = np.array([[1., 4., 3.], [2., 1., 5.], [4., 6., 2.], [5., 2., 7.], [8., 9., 1.]])
X = X0 - X0.mean(axis=0)
Ux, sx, Vxt = np.linalg.svd(X, full_matrices=False)
Vx = Vxt.T
scores = X @ Vx
check("pca_scores", scores, Ux @ np.diag(sx))
C = X.T @ X / (len(X) - 1)
check("pca_covariance_eigenpairs", C @ Vx, Vx @ np.diag(sx ** 2 / (len(X) - 1)))
check("pca_score_variances", scores.T @ scores / (len(X) - 1), np.diag(sx ** 2 / (len(X) - 1)))
check("pca_rank_two_reconstruction", X @ Vx[:, :2] @ Vx[:, :2].T, Ux[:, :2] @ np.diag(sx[:2]) @ Vxt[:2, :])
Y = X.T
Uy, sy, Vyt = np.linalg.svd(Y, full_matrices=False)
Cy = Y @ Y.T / (Y.shape[1] - 1)
check("column_sample_covariance", Cy, C)
check("column_sample_left_eigenvectors", Cy @ Uy, Uy @ np.diag(sy ** 2 / (Y.shape[1] - 1)))
check("column_sample_scores", Uy.T @ Y, np.diag(sy) @ Vyt)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "svg.fonttype": "path"})
fig, axes = plt.subplots(1, 4, figsize=(13.6, 4.8))
fig.subplots_adjust(left=.035, right=.985, bottom=.15, top=.77, wspace=.27)
fig.suptitle("SVD: choose coordinates, scale, choose output directions", fontsize=18, y=.97, color="#142e43")
fig.text(.5, .86, r"$A=U\Sigma V^T$,  $\sigma_1=2$,  $\sigma_2=0.75$  |  same coordinate scale in every panel", ha="center", color="#526471", fontsize=11)
titles = [r"$x$", r"$V^T x$", r"$\Sigma V^T x$", r"$U\Sigma V^T x=Ax$"]
labels = [(r"$v_1$", r"$v_2$"), (r"$e_1$", r"$e_2$"), (r"$\sigma_1 e_1$", r"$\sigma_2 e_2$"), (r"$\sigma_1 u_1$", r"$\sigma_2 u_2$")]
colors = ["#2079a7", "#d48b18"]
for ax, curve, basis, point, title, pair in zip(axes, curve_points, basis_points, tracked_points, titles, labels):
    ax.set_aspect("equal")
    ax.set_xlim(-2.65, 2.65)
    ax.set_ylim(-2.65, 2.65)
    ax.axhline(0, color="#d6dfe5", lw=.8, zorder=0)
    ax.axvline(0, color="#d6dfe5", lw=.8, zorder=0)
    ax.plot(curve[0], curve[1], color="#8d9da7", lw=2, zorder=1)
    for j, color in enumerate(colors):
        end = basis[:, j]
        ax.annotate("", xy=end, xytext=(0, 0), arrowprops={"arrowstyle": "-|>", "color": color, "lw": 2.4}, zorder=3)
        # Vector 1 labels below, vector 2 labels above: separate them from the tracked point.
        ax.annotate(pair[j], end, xytext=(4, -19 if j == 0 else 9), textcoords="offset points", color=color, fontsize=12, zorder=5)
    ax.plot(*point, "o", ms=6, color="#ab447e", zorder=4)
    ax.set_title(title, pad=13, fontsize=15)
    ax.set_xticks([-2, 0, 2])
    ax.set_yticks([-2, 0, 2])
    ax.tick_params(labelsize=8, colors="#73828c", length=2)
    for spine in ax.spines.values():
        spine.set_visible(False)

for i, label in enumerate([r"$V^T$", r"$\Sigma$", r"$U$"]):
    a, b = axes[i].get_position(), axes[i+1].get_position()
    start, end = (a.x1+.006, .48), (b.x0-.006, .48)
    fig.add_artist(FancyArrowPatch(start, end, transform=fig.transFigure, arrowstyle="-|>", mutation_scale=13, color="#243d50", lw=1.3))
    fig.text((start[0]+end[0])/2, .535, label, ha="center", color="#243d50", fontsize=13)

fig.text(.5, .055, "Blue and gold track paired singular directions. The magenta dot tracks one input through all three operations.", ha="center", color="#526471", fontsize=10)
fig.savefig(OUT / "svd_geometry.png", dpi=180, facecolor="white")
fig.savefig(OUT / "svd_geometry.svg", facecolor="white")
plt.close(fig)
(OUT / "checks.json").write_text(json.dumps({"tolerance": TOL, "maximum_error": max(checks.values()), "checks": checks}, indent=2) + "\n", encoding="utf-8")
print(f"Saved one SVG/PNG figure; {len(checks)} numerical checks passed, maximum error {max(checks.values()):.3g}.")
