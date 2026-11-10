"""Original level-2/3 Rao-Blackwell figures. Requires Pillow; no random draws.

Run with Python; outputs are beside this script. Exact Fraction arithmetic checks
the 4-outcome conditional-expectation operator for every p=k/20, 1<=k<=19.
Geometry is a schematic affine 2-D slice of L2, not a sample scatterplot.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
INK, BLUE, TEAL, ORANGE = "#182c43", "#285ea8", "#087e82", "#bc6729"
BG = "#f8fafc"
seqs = list(product((0, 1), repeat=2))
groups = [[j for j, x in enumerate(seqs) if sum(x) == t] for t in range(3)]
P = [[F(int(sum(x) == sum(y)), len(groups[sum(x)])) for y in seqs] for x in seqs]

def apply(A, v):
    return [sum(a*x for a, x in zip(row, v)) for row in A]

for i in range(4):
    for j in range(4):
        assert sum(P[i][k]*P[k][j] for k in range(4)) == P[i][j]
U = [F(x[0]) for x in seqs]
V = apply(P, U)
assert V == [F(sum(x), 2) for x in seqs]
for p in [F(k, 20) for k in range(1, 20)]:
    weights = [p**sum(x)*(1-p)**(2-sum(x)) for x in seqs]
    mean = lambda v: sum(w*x for w, x in zip(weights, v))
    assert mean(U) == mean(V) == p
    assert mean([(u-p)**2 for u in U]) == p*(1-p)
    assert mean([(v-p)**2 for v in V]) == p*(1-p)/2
    for i in range(4):
        for j in range(4):
            assert weights[i]*P[i][j] == weights[j]*P[j][i]
    for start in (U, [2*u for u in U]):  # unbiased and biased starting rules
        proj = apply(P, start)
        residual = [u-v for u, v in zip(start, proj)]
        assert mean(start) == mean(proj)
        for group in groups:
            assert sum(weights[i]*residual[i] for i in group) == 0
        assert mean([(u-p)**2 for u in start]) == (
            mean([r*r for r in residual]) + mean([(v-p)**2 for v in proj]))
        assert apply(P, proj) == proj

def canvas(h):
    im = Image.new("RGB", (1600, h), BG)
    return im, ImageDraw.Draw(im)

def text(d, x, y, s, size=30, color=INK, bold=False, anchor="la"):
    font = ImageFont.truetype("C:/Windows/Fonts/" + ("segoeuib.ttf" if bold else "segoeui.ttf"), size)
    d.text((x, y), s, font=font, fill=color, anchor=anchor)

def arrow(d, start, end, color=TEAL, width=5):
    from math import atan2, cos, sin
    a = atan2(end[1]-start[1], end[0]-start[0])
    d.line((start, end), fill=color, width=width)
    d.polygon([end, (end[0]-22*cos(a)+10*sin(a), end[1]-22*sin(a)-10*cos(a)),
               (end[0]-22*cos(a)-10*sin(a), end[1]-22*sin(a)+10*cos(a))], fill=color)

im, d = canvas(820)
text(d, 55, 30, "Two observations: average within each heads-count group", 43, bold=True)
text(d, 55, 105, "X1 and X2 are independent Bernoulli(p). Old rule: U = X1. Summary: T = X1 + X2.", 29)
for left, t in zip((55, 565, 1075), range(3)):
    right = left+470
    d.rounded_rectangle((left, 200, right, 650), 22, fill="#edf3fa", outline=BLUE, width=2)
    text(d, (left+right)/2, 240, f"T = {t}", 38, BLUE, True, "mm")
    if t == 1:
        text(d, left+35, 300, "(X1, X2)       Old U", 28, bold=True)
        text(d, left+45, 352, "(0, 1)              0", 34)
        text(d, left+45, 410, "(1, 0)              1", 34)
        text(d, (left+right)/2, 475, "Each has conditional chance 1/2", 25, anchor="mm")
        result = "U* = (0 + 1) / 2 = 1/2"
    else:
        val = t//2
        text(d, (left+right)/2, 350, f"Only ({val}, {val}) is possible", 32, anchor="mm")
        text(d, (left+right)/2, 415, f"Old U = {val}", 34, BLUE, anchor="mm")
        result = f"U* = {val}"
    arrow(d, ((left+right)/2, 510), ((left+right)/2, 553))
    text(d, (left+right)/2, 600, result, 32, TEAL, True, "mm")
text(d, 800, 705, "One formula covers all three groups: U* = T / 2", 38, TEAL, True, "mm")
text(d, 800, 765, "MSE: p(1 - p)  →  p(1 - p) / 2        Same data, half the mean squared error.", 29, anchor="mm")
im.save(OUT / "two-bernoulli.png")

im, d = canvas(900)
text(d, 55, 30, "Project once: remove the perpendicular error", 44, bold=True)
text(d, 55, 105, "A schematic L² slice for the two-toss example at p = 1/2; points represent random variables.", 28)
# The horizontal line is the intersection of H_T with this affine slice.
d.rounded_rectangle((60, 510, 870, 600), 16, fill="#e3f4f1")
d.line((70, 555, 850, 555), fill=TEAL, width=3)
A, B, C = (315, 555), (640, 555), (640, 230)
arrow(d, A, C, BLUE)
arrow(d, A, B, TEAL)
arrow(d, C, B, ORANGE)
d.line((610, 555, 610, 525, 640, 525), fill=INK, width=3)
for point, color in ((A, INK), (B, TEAL), (C, BLUE)):
    d.ellipse((point[0]-9, point[1]-9, point[0]+9, point[1]+9), fill=color)
text(d, 640, 187, "U = X1", 36, BLUE, True, "mm")
text(d, 315, 625, "p (constant)", 29, anchor="mm")
text(d, 640, 625, "U* = T / 2", 32, TEAL, True, "mm")
text(d, 80, 565, "Slice through H_T", 24, TEAL)
text(d, 170, 315, "Original error", 28, BLUE)
text(d, 180, 355, "MSE = 1/4", 28, BLUE)
text(d, 670, 345, "Removed", 28, ORANGE)
text(d, 670, 385, "MSE = 1/8", 28, ORANGE)
text(d, 360, 565, "Remaining MSE = 1/8", 24, TEAL)
d.rounded_rectangle((950, 220, 1535, 655), 24, fill="#edf3fa", outline=BLUE, width=2)
text(d, 1242, 278, "Project onto H_T again?", 33, BLUE, True, "mm")
text(d, 1242, 355, "U* is already in H_T.", 32, anchor="mm")
text(d, 1242, 430, "E[U* | T] = U*", 40, TEAL, True, "mm")
text(d, 1242, 505, "P_T² = P_T", 40, TEAL, True, "mm")
text(d, 1242, 585, "Same subspace, no further change.", 28, anchor="mm")
text(d, 800, 735, "Pythagoras: original MSE = removed MSE + remaining MSE", 34, bold=True, anchor="mm")
text(d, 800, 795, "H_T contains all square-integrable functions of T, including constants.", 29, anchor="mm")
text(d, 800, 847, "A different sufficient summary can define a different projection. This figure is schematic, not to scale.", 26, anchor="mm")
im.save(OUT / "projection-idempotence.png")

(OUT / "deeper-checks.json").write_text(json.dumps({
    "outcomes": seqs, "old_rule": [str(x) for x in U], "new_rule": [str(x) for x in V],
    "exact_checks": ["P squared equals P", "P is self-adjoint in probability-weighted inner product",
                     "Residual is orthogonal to each T-group indicator", "Bias preserved",
                     "MSE Pythagoras for unbiased U and biased 2U", "Two-toss MSE is halved"],
    "probability_grid": "k/20 for k=1,...,19; exact Fraction arithmetic",
    "scope": "Checks the finite example, not a proof of the general theorem"
}, indent=2) + "\n", encoding="utf-8")
print("PASS: exact conditional averaging, idempotence, weighted orthogonality and MSE checks; two figures generated")
