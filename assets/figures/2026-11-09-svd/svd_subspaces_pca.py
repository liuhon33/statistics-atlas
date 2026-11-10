"""Reproduce the requested handwriting excerpt, subspace diagram, and PCA example.

The excerpt is rendered directly from PDF p. 6 by Poppler, without retouching.
The clean diagram is an original schematic; the numeric example is constructed.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, FancyBboxPatch
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SOURCE = ROOT / "raw/notes/2025-06-05-linear-algebra-29-svd.pdf"
SOURCE_HASH = "0399ad78b326ddff0e884d7ae9843222b521eb73f32b30e4ff17a2cdf0a5a67b"
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH

poppler = shutil.which("pdftoppm")
if not poppler:
    raise RuntimeError("pdftoppm is required to render the original PDF excerpt")
crop_args = [poppler, "-f", "6", "-l", "6", "-singlefile", "-scale-to", "1700",
             "-x", "130", "-y", "190", "-W", "1155", "-H", "850", "-png",
             str(SOURCE), str(OUT / "handwritten-p06-basis-goal")]
subprocess.run(crop_args, check=True)

checks = {}
def check(name, actual, expected):
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    assert error < 1e-11, (name, error)
    checks[name] = error

# Three centered observations and two features; v1 has the requested ratio 1:2.
X = np.array([[1., 7.], [-5., -5.], [4., -2.]])
v1, v2 = np.array([1., 2.]) / np.sqrt(5), np.array([-2., 1.]) / np.sqrt(5)
u1, u2 = np.array([1., -1., 0.]) / np.sqrt(2), np.array([1., 1., -2.]) / np.sqrt(6)
V = np.column_stack([v1, v2])
U = np.column_stack([u1, u2])
s = np.array([3 * np.sqrt(10), np.sqrt(30)])
S = np.diag(s)
T = X @ V
C = X.T @ X / (X.shape[0] - 1)
M1, M2 = s[0] * np.outer(u1, v1), s[1] * np.outer(u2, v2)
check("centered_feature_columns", X.mean(axis=0), 0)
check("unit_orthogonal_loadings", V.T @ V, np.eye(2))
check("unit_orthogonal_score_patterns", U.T @ U, np.eye(2))
check("covariance", C, [[21, 12], [12, 39]])
check("principal_eigenpairs", C @ V, V @ np.diag([45, 15]))
check("singular_values", np.linalg.svd(X, compute_uv=False), s)
check("unnormalized_one_to_two_combination", X @ [1., 2.], [15, -15, 0])
check("pc1_scores", X @ v1, [3 * np.sqrt(5), -3 * np.sqrt(5), 0])
check("pc2_scores", X @ v2, [np.sqrt(5), np.sqrt(5), -2 * np.sqrt(5)])
check("actual_scores_equal_U_Sigma", T, U @ S)
check("left_vectors_are_normalized_scores", T / s, U)
check("dual_observation_weights", X.T @ U, V @ S)
check("pc1_rank_one_contribution", M1, [[3, 6], [-3, -6], [0, 0]])
check("pc2_rank_one_contribution", M2, [[-2, 1], [-2, 1], [4, -2]])
check("two_component_reconstruction", M1 + M2, X)
check("pc1_extracts_only_first_outer_product", (M1 + M2) @ v1, s[0] * u1)
check("pc1_reconstruction_is_projection", X @ np.outer(v1, v1), M1)
check("sample_variances", np.var(T, axis=0, ddof=1), [45, 15])
check("variance_proportions", s ** 2 / np.sum(s ** 2), [.75, .25])
check("rank_one_squared_frobenius_error", np.linalg.norm(X-M1, "fro") ** 2, 30)
assert np.linalg.matrix_rank(M1) == 1 and np.linalg.matrix_rank(X) == 2

# A rectangular rank-2 map checks the diagram's arrows and both zero spaces.
A = np.array([[1., 2., 3., 4.], [2., 4., 6., 8.], [0., 1., 0., 1.]])
Ua, sa, Vat = np.linalg.svd(A, full_matrices=True)
Va = Vat.T
check("basis_goal_A_Vr_equals_Ur_Sigma", A @ Va[:, :2], Ua[:, :2] @ np.diag(sa[:2]))
check("null_A_maps_to_zero", A @ Va[:, 2:], 0)
check("left_null_maps_to_zero_under_transpose", A.T @ Ua[:, 2:], 0)
check("all_outputs_orthogonal_to_left_null", Ua[:, 2:].T @ A, 0)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "svg.fonttype": "path"})
fig, ax = plt.subplots(figsize=(12.8, 6.6))
fig.subplots_adjust(left=.02, right=.98, bottom=.02, top=.98)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6.4)
ax.set_aspect("equal")
ax.axis("off")
ink, blue, gold, red = "#16394d", "#2079a7", "#c78316", "#b24d62"
ax.text(6, 6.13, "The four subspaces: which directions survive the map?", ha="center", fontsize=18, color=ink)
ax.text(2.7, 5.62, r"Input space $\mathbb{R}^n$", ha="center", color=ink, fontsize=14)
ax.text(9.3, 5.62, r"Output space $\mathbb{R}^m$", ha="center", color=ink, fontsize=14)

def space_panel(x, left):
    # Perspective diagram: two basis directions, with no literal spatial dimension claim.
    o = np.array([x + .55, 3.45])
    a, b = np.array([.62, 1.12]), np.array([1.95, .30])
    verts = np.array([o, o+a, o+a+b, o+b])
    ax.add_patch(Polygon(verts, closed=True, facecolor="#e9f2f6", edgecolor="#789baa", lw=1.5))
    for idx, (direction, color) in enumerate([(a, blue), (b, gold)]):
        end=o+.77*direction
        ax.add_patch(FancyArrowPatch(o, end, arrowstyle="-|>", mutation_scale=16, lw=2.4, color=color))
        prefix="v" if left else "u"
        ax.text(end[0] + .09, end[1] + (.13 if idx==0 else -.20), rf"${prefix}_{idx+1}$", color=color, fontsize=15)
    ax.plot(o[0],o[1],"o",color=ink,ms=4)
    if left:
        ax.text(x+1.78,5.04,r"Row space: $\operatorname{col}(A^T)$",ha="center",color=ink,fontsize=12)
        ax.text(x+1.78,3.00,r"$\operatorname{span}(v_1,\ldots,v_r)$   |   dimension $r$",ha="center",color=ink,fontsize=11)
    else:
        ax.text(x+1.78,5.04,r"Column space: $\operatorname{col}(A)$",ha="center",color=ink,fontsize=12)
        ax.text(x+1.78,3.00,r"$\operatorname{span}(u_1,\ldots,u_r)$   |   dimension $r$",ha="center",color=ink,fontsize=11)
        ax.text(o[0]-.21,o[1]-.28,r"$0$",color=red,fontsize=13)
    ax.text(x+1.78,2.64,r"$\perp$",ha="center",color="#82939a",fontsize=19)
    box=FancyBboxPatch((x+.15,1.42),3.3,.89,boxstyle="round,pad=.12,rounding_size=.1",facecolor="#faf0f2",edgecolor="#d5aab3",lw=1.2)
    ax.add_patch(box)
    if left:
        ax.text(x+1.8,2.05,r"Null space $\ker A$",ha="center",color=ink,fontsize=12)
        ax.text(x+1.8,1.70,r"$\operatorname{span}(v_{r+1},\ldots,v_n)$;  dimension $n-r$",ha="center",color=ink,fontsize=10)
    else:
        ax.text(x+1.8,2.05,r"Left null space $\ker A^T$",ha="center",color=ink,fontsize=12)
        ax.text(x+1.8,1.70,r"$\operatorname{span}(u_{r+1},\ldots,u_m)$;  dimension $m-r$",ha="center",color=ink,fontsize=10)
    return o

lo=space_panel(.65,True)
ro=space_panel(7.25,False)
ax.add_patch(FancyArrowPatch((4.4,4.48),(7.45,4.48),arrowstyle="-|>",mutation_scale=17,lw=2,color=ink))
ax.text(5.92,4.77,r"$Av_i=\sigma_i u_i$",ha="center",fontsize=15,color=ink)
ax.text(5.92,4.07,r"$i=1,\ldots,r$",ha="center",fontsize=11,color=ink)
# This arrow deliberately terminates at the output origin, never at the left-null box.
ax.add_patch(FancyArrowPatch((4.1,1.9),ro,connectionstyle="arc3,rad=.28",arrowstyle="-|>",mutation_scale=16,lw=1.7,linestyle="--",color=red))
ax.text(5.9,2.08,r"$Az=0$",ha="center",color=red,fontsize=14,bbox={"facecolor":"white","edgecolor":"none","pad":3})
ax.text(5.9,1.75,r"$z\in\ker A$",ha="center",color=red,fontsize=11,bbox={"facecolor":"white","edgecolor":"none","pad":2})
ax.text(9.08,1.05,r"$A^T w=0$ for $w\in\ker A^T$",ha="center",color=red,fontsize=11)
ax.text(6,.57,r"Every output $Ax$ lies in $\operatorname{col}(A)$ and is orthogonal to $\ker A^T$.",ha="center",color=ink,fontsize=12)
ax.text(6,.17,"Schematic: two singular directions shown; perspective patches are not to scale.",ha="center",color="#657c87",fontsize=10)

fig.savefig(OUT/"svd_four_subspaces.svg",facecolor="white")
fig.savefig(OUT/"svd_four_subspaces.png",dpi=170,facecolor="white")
plt.close(fig)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_HASH
report={"source_pdf_sha256":SOURCE_HASH,"source_page":6,
        "crop_pixels_at_scale_to_1700":{"x":130,"y":190,"width":1155,"height":850},
        "excerpt_sha256":hashlib.sha256((OUT/"handwritten-p06-basis-goal.png").read_bytes()).hexdigest(),
        "toy_X":X.tolist(),"toy_covariance":C.tolist(),"toy_scores":T.tolist(),
        "checks":checks,"maximum_error":max(checks.values())}
(OUT/"subspaces-pca-checks.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(f"Excerpt and diagram saved; {len(checks)} checks passed; maximum error {max(checks.values()):.3g}.")
