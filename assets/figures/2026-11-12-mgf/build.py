"""Original MGF figures; Python + NumPy + Matplotlib + Pillow + SymPy.

Run with an absolute path, e.g. D:/anaconda/python.exe -X utf8 <this file>.
Outputs are written beside this file. Previously generated artifacts must still
match their saved hashes before regeneration; edited outputs are never replaced.
The GIF uses discrete held stages, not an interpolation between derivatives.
"""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import math
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from PIL import Image, ImageDraw
import sympy as sp

OUT = Path(__file__).resolve().parent
ARTIFACTS = [
    "mgf-use.svg", "mgf-use.png", "mgf-derivative-ladder.svg",
    "mgf-derivative-ladder.png", "mgf-derivative-ladder.gif",
    "decoded-stages.png", "checks.json",
]
MANIFEST = OUT / "artifact-manifest.json"
INK, MUTED, GRID = "#203542", "#647684", "#dbe3e8"
COLORS = ["#697782", "#087e8b", "#c26b0a", "#8b50a0", "#376cc2"]
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white", "svg.fonttype": "none",
    "svg.hashsalt": "mgf-2026-11-12",
})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_overwrites():
    old = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    for name in ARTIFACTS:
        p = OUT / name
        if p.exists() and old.get("sha256", {}).get(name) != sha(p):
            raise RuntimeError(f"Refusing to replace an unrecognized or edited artifact: {p}")


def save_pair(fig, stem):
    svg, png = BytesIO(), BytesIO()
    fig.savefig(svg, format="svg", metadata={"Date": None})
    fig.savefig(png, format="png", dpi=140)
    (OUT / f"{stem}.svg").write_bytes(svg.getvalue())
    (OUT / f"{stem}.png").write_bytes(png.getvalue())


def use_figure():
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.9), gridspec_kw={"width_ratios": [1, 1.6]})
    left, right = axes
    fig.suptitle("One fixed score distribution, one moment-generating function", fontsize=18, y=.97)
    left.vlines([0, 2], 0, [.5, .5], color=INK, linewidth=3)
    left.scatter([0, 2], [.5, .5], color=INK, s=90, zorder=4)
    for x in [0, 2]:
        left.text(x, .545, "1/2", ha="center", fontsize=16)
    left.set(xlim=(-.55, 2.55), ylim=(0, .69), xticks=[0, 1, 2], yticks=[0, .25, .5],
             xlabel=r"Possible score $x$", ylabel=r"Probability $P(X=x)$")
    left.set_title("Average over these two outcomes", fontsize=13, pad=15)
    left.spines[["top", "right"]].set_visible(False)
    left.grid(axis="y", color=GRID, alpha=.7)

    t = np.linspace(-.75, .75, 501)
    mgf = .5 + .5 * np.exp(2*t)
    right.plot(t, mgf, color=INK, lw=3, label=r"$M_X(t)=\frac{1}{2}+\frac{1}{2}e^{2t}$")
    right.plot(t, 1+t, color=COLORS[1], lw=2.2, ls="--", label=r"Tangent at 0: $1+t$")
    right.axvline(0, color=GRID, lw=1)
    right.scatter([0], [1], color=COLORS[1], s=55, zorder=5)
    right.annotate(r"$M_X(0)=1$", xy=(0, 1), xytext=(-.66, 1.8), fontsize=14,
                   arrowprops={"arrowstyle": "->", "color": MUTED})
    right.set(xlim=(-.75, .75), ylim=(0, 3.05), xticks=[-.5, 0, .5], yticks=[0, 1, 2, 3],
              xlabel=r"Chosen input $t$ (not a score)", ylabel=r"Value of $M_X(t)$")
    right.set_title("Differentiate the curve; then evaluate at zero", fontsize=13, pad=15)
    right.spines[["top", "right"]].set_visible(False)
    right.legend(loc="upper left", frameon=False, fontsize=12)
    right.grid(color=GRID, alpha=.5)
    fig.text(.27, .055, r"Mean: $M_X'(0)=1$", color=COLORS[1], ha="center", fontsize=16)
    fig.text(.74, .055, r"Second raw moment: $M_X''(0)=2$", color=COLORS[2], ha="center", fontsize=16)
    fig.subplots_adjust(left=.075, right=.98, bottom=.22, top=.80, wspace=.30)
    save_pair(fig, "mgf-use")
    plt.close(fig)


ROW_TERMS = [
    [r"1", r"tX", r"\frac{X^2t^2}{2!}", r"\frac{X^3t^3}{3!}", r"\frac{X^4t^4}{4!}"],
    [r"1", r"m_1t", r"\frac{m_2t^2}{2!}", r"\frac{m_3t^3}{3!}", r"\frac{m_4t^4}{4!}"],
    [r"0", r"m_1", r"m_2t", r"\frac{m_3t^2}{2!}", r"\frac{m_4t^3}{3!}"],
    [r"0", r"0", r"m_2", r"m_3t", r"\frac{m_4t^2}{2!}"],
    [r"0", r"0", r"0", r"m_3", r"m_4t"],
]
ROW_LABELS = [r"e^{tX}", r"M_X(t)", r"M_X'(t)", r"M_X''(t)", r"M_X'''(t)"]
STAGES = [
    "1. Expand the exponential: the coefficients still contain the random X.",
    "2. Take expectation: each random power becomes its moment; t stays outside.",
    "3. Differentiate in t: the first moment becomes the constant term.",
    "4. Differentiate the full function again: the second moment is now constant.",
    "5. Differentiate once more: the third moment is now constant.",
]


def ladder_figure(stage=4, overview=False):
    fig, ax = plt.subplots(figsize=(13.6, 7.6))
    ax.set(xlim=(0, 1.18), ylim=(0, 1))
    ax.axis("off")
    fig.subplots_adjust(left=.025, right=.98, bottom=.11, top=.86)
    fig.suptitle("Expectation stores the moments; derivatives extract them", fontsize=20, y=.965)
    fig.text(.5, .905, r"$m_n=\mathbb{E}[X^n]$   |   A color follows the same original power of $X$", ha="center", fontsize=14)
    xs = [.27, .405, .54, .675, .81]
    ys = [.82, .66, .50, .34, .18]
    ax.text(.06, .97, "Operation", fontsize=12, color=MUTED)
    ax.text(.55, .97, "Terms of the full series (continues to the right)", ha="center", fontsize=12, color=MUTED)
    ax.text(1.07, .97, r"Read at $t=0$", ha="center", fontsize=12, color=MUTED)
    ax.plot([.98, .98], [.08, .93], color=GRID)
    for r, y in enumerate(ys):
        ax.axhline(y-.08, xmin=.01, xmax=.99, color=GRID, lw=.6)
        if r > stage and not overview:
            continue
        if not overview and r == stage:
            ax.add_patch(FancyBboxPatch((.005, y-.064), 1.16, .128,
                         boxstyle="round,pad=.008,rounding_size=.015", facecolor="#f1f6f9", edgecolor="none", zorder=-1))
        ax.text(.04, y, "$"+ROW_LABELS[r]+"$", va="center", fontsize=21)
        ax.text(.205, y, "=", va="center", ha="center", fontsize=18)
        for k, (x, term) in enumerate(zip(xs, ROW_TERMS[r])):
            is_zero = term == "0"
            ax.text(x, y, "$"+term+"$", va="center", ha="center", fontsize=22,
                    color="#bec8cf" if is_zero else COLORS[k])
            if k < 4:
                ax.text(x+.0675, y, "+", va="center", ha="center", color=MUTED, fontsize=13)
        ax.text(.919, y, r"$+\cdots$", va="center", ha="center", fontsize=19, color=MUTED)
        if r >= 1:
            result = "1" if r == 1 else f"m_{r-1}"
            ax.text(1.07, y, "$"+result+"$", va="center", ha="center", fontsize=24, color=COLORS[max(0,r-1)])
            k = r-1
            ax.add_patch(FancyBboxPatch((xs[k]-.047, y-.053), .094, .106,
                         boxstyle="round,pad=.004,rounding_size=.01", fill=False,
                         edgecolor=COLORS[k], linewidth=1.4))
        if r > 0:
            action = r"$\mathbb{E}[\,\cdot\,]$" if r == 1 else r"$d/dt$"
            ax.annotate("", xy=(.10,y+.046), xytext=(.10,ys[r-1]-.046),
                        arrowprops={"arrowstyle":"->", "color":MUTED, "lw":1})
            ax.text(.15, y+.079, action, color=MUTED, fontsize=10, va="center")
    footer = "Lower-degree terms disappear. Higher-degree terms vanish at t = 0. The matching moment survives." if overview else STAGES[stage]
    fig.text(.5, .07, footer, ha="center", fontsize=13)
    fig.text(.5, .025, "Differentiate the function in the middle, NOT the evaluated number in the right column.",
             ha="center", fontsize=12, color=MUTED)
    return fig


def ladder_assets():
    full = ladder_figure(overview=True)
    save_pair(full, "mgf-derivative-ladder")
    plt.close(full)
    frames = []
    for stage in range(5):
        fig = ladder_figure(stage)
        bio = BytesIO()
        fig.savefig(bio, format="png", dpi=100)
        bio.seek(0)
        frames.append(Image.open(bio).convert("RGB"))
        plt.close(fig)
    frames[0].save(OUT / "mgf-derivative-ladder.gif", save_all=True, append_images=frames[1:],
                   loop=0, duration=[2200, 2800, 3400, 3400, 4200], disposal=2, optimize=False)
    # Inspect the saved GIF, not the pre-encoding frames.
    decoded = []
    durations = []
    with Image.open(OUT / "mgf-derivative-ladder.gif") as gif:
        for i in range(gif.n_frames):
            gif.seek(i)
            decoded.append(gif.convert("RGB"))
            durations.append(gif.info["duration"])
    assert len(decoded) == 5
    thumb_w, thumb_h = 816, 456
    sheet = Image.new("RGB", (2*thumb_w, 3*(thumb_h+30)), "#e4ebef")
    draw = ImageDraw.Draw(sheet)
    for i, pic in enumerate(decoded):
        x, y = (i%2)*thumb_w, (i//2)*(thumb_h+30)
        draw.text((x+12,y+8), f"Decoded stage {i+1} / {len(decoded)}", fill=INK)
        sheet.paste(pic.resize((thumb_w,thumb_h), Image.Resampling.LANCZOS), (x,y+30))
    sheet.save(OUT / "decoded-stages.png")
    return {"decoded_frames":len(decoded), "duration_ms":durations, "total_duration_ms":sum(durations),
            "stages":STAGES, "format":"Discrete symbolic steps; no interpolated derivative order or moving axes."}


def mathematical_checks():
    t, x = sp.symbols("t x", real=True)
    m = [sp.Integer(1)] + list(sp.symbols("m1:5"))
    M = sp.Rational(1,2) + sp.exp(2*t)/2
    records = []
    for n in range(13):
        direct = sp.Integer(1) if n == 0 else sp.Rational(1,2)*2**n
        derivative = sp.diff(M,t,n).subs(t,0)
        coefficient = sp.expand(sp.series(M,t,0,n+1).removeO()).coeff(t,n)
        assert sp.simplify(derivative-direct) == 0
        assert coefficient*sp.factorial(n) == direct
        records.append({"order":n,"moment":str(direct),"series_coefficient":str(coefficient)})
    assert sp.diff(M,t).subs(t,0) == 1
    assert sp.diff(M,t,2).subs(t,0)-sp.diff(M,t).subs(t,0)**2 == 1

    # Symbolic values of every displayed cell, checked against differentiation.
    displayed = [
        [1,t*x,x**2*t**2/2,x**3*t**3/6,x**4*t**4/24],
        [1,m[1]*t,m[2]*t**2/2,m[3]*t**3/6,m[4]*t**4/24],
        [0,m[1],m[2]*t,m[3]*t**2/2,m[4]*t**3/6],
        [0,0,m[2],m[3]*t,m[4]*t**2/2],
        [0,0,0,m[3],m[4]*t],
    ]
    for k in range(5):
        assert sp.simplify(sp.sympify(displayed[0][k])-x**k*t**k/sp.factorial(k)) == 0
        assert sp.simplify(sp.sympify(displayed[1][k])-m[k]*t**k/sp.factorial(k)) == 0
    for r in range(2,5):
        for k in range(5):
            assert sp.simplify(sp.diff(displayed[r-1][k],t)-displayed[r][k]) == 0
    for r in range(1,5):
        assert sp.simplify(sum(map(sp.sympify,displayed[r])).subs(t,0)-m[r-1]) == 0
    signed_x = [-2,0,3]
    signed_p = [sp.Rational(1,4),sp.Rational(1,2),sp.Rational(1,4)]
    Ms = sum(p*sp.exp(t*v) for v,p in zip(signed_x,signed_p))
    for n in range(9):
        weighted = sum(p*v**n*sp.exp(t*v) for v,p in zip(signed_x,signed_p))
        assert sp.simplify(sp.diff(Ms,t,n)-weighted) == 0
        assert sp.diff(Ms,t,n).subs(t,0) == sum(p*v**n for v,p in zip(signed_x,signed_p))

    grid = np.linspace(-.75,.75,501)
    series = np.ones_like(grid)
    for n in range(1,21):
        series += float(sp.Rational(1,2)*2**n/sp.factorial(n))*grid**n
    max_error = float(np.max(np.abs(series-(.5+.5*np.exp(2*grid)))))
    assert max_error < 5e-14
    # Supporting numerical check of the analytic domination bound in the note.
    a,b = 1., .4
    y = np.linspace(0.,30.,2001)
    ratios = [float(np.max(y**r*np.exp(-(a-b)*y)*(a-b)**r/math.factorial(r))) for r in range(9)]
    assert max(ratios) <= 1+1e-12
    return {
        "status":"PASS", "constructed_distribution":{"x":[0,2],"probabilities":[.5,.5]},
        "exact_moments_and_coefficients":records,
        "derivative_ladder":"25 symbolic cells and 4 evaluated row sums checked exactly",
        "signed_distribution":"Orders 0 through 8: full derivative and at-zero expectation checked symbolically",
        "mean":1,"second_raw_moment":2,"variance":1,
        "degree20_series_max_absolute_error":max_error,
        "domination_bound_sampled_max_ratios":ratios,
        "scope":"Exact symbolic identities for displayed finite examples; numerical support for figures. The general theorem is justified analytically in the note, not by these examples.",
    }


if __name__ == "__main__":
    check_overwrites()
    checks = mathematical_checks()
    use_figure()
    checks["animation"] = ladder_assets()
    for name in ["mgf-use.svg", "mgf-derivative-ladder.svg"]:
        ET.parse(OUT/name)
    checks["svg_parse"] = "PASS: both SVGs"
    (OUT/"checks.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="utf-8")
    manifest = {"description":"Original deterministic mathematical graphics; no external image or source original was edited.",
                "generator":"build.py", "sha256":{name:sha(OUT/name) for name in ARTIFACTS}}
    MANIFEST.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":checks["status"],"series_error":checks["degree20_series_max_absolute_error"],
                      "gif_frames":checks["animation"]["decoded_frames"],"output":str(OUT)}))
