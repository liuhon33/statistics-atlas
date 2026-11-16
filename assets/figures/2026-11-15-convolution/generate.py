"""Original, deterministic convolution illustrations; never edits supplied images.

Run: D:/anaconda/python.exe assets/figures/2026-11-15-convolution/generate.py
Requires numpy, scipy, sympy, matplotlib and Pillow. Outputs beside this file.
All signal samples are constructed examples, not recorded EEG.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import xml.etree.ElementTree as ET

import numpy as np
import sympy as sp
from scipy.integrate import quad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
BLUE, ORANGE, GREEN = "#2877a8", "#d1772b", "#16836b"
INK, MUTED, BG = "#23354a", "#657589", "#fafbf9"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12, "text.color": INK,
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": "#bcc6ce", "figure.facecolor": BG,
    "axes.facecolor": BG, "savefig.facecolor": BG, "svg.fonttype": "none",
})


def clean(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.14)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


def density(t):
    t = np.asarray(t)
    return np.maximum(0, np.minimum(2, t) - np.maximum(0, t - 3)) / 6


def overlap(t):
    return max(0., t - 3), min(2., t)


def box(ax, left, right, height, color, label=None, fill=False):
    ax.plot([left, left, right, right], [0, height, height, 0],
            color=color, lw=2.5, label=label)
    if fill:
        ax.fill_between([left, right], 0, height, color=color, alpha=.16)


def dice():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.6, 4.6),
                                gridspec_kw={"width_ratios": [1, 1.35]})
    for a in range(1, 7):
        for b in range(1, 7):
            hit = a + b == 7
            ax.add_patch(Rectangle((a-.5, b-.5), 1, 1,
                         facecolor=GREEN if hit else "#eef2f4", edgecolor="white", lw=2))
            ax.text(a, b, str(a+b), ha="center", va="center",
                    color="white" if hit else MUTED, fontsize=12)
    ax.set(xlim=(.5, 6.5), ylim=(.5, 6.5), xticks=range(1, 7), yticks=range(1, 7),
           xlabel="First die", ylabel="Second die", title="36 equally likely pairs")
    ax.set_aspect("equal")
    for spine in ax.spines.values():
        spine.set_visible(False)
    sums = np.arange(2, 13)
    counts = np.array([sum(a+b == s for a in range(1, 7) for b in range(1, 7)) for s in sums])
    bx.bar(sums, counts/36, color=[GREEN if s == 7 else BLUE for s in sums], width=.8)
    for s, count in zip(sums, counts):
        bx.text(s, count/36+.006, str(count), ha="center", fontsize=11)
    bx.set(xticks=sums, ylim=(0, .21), yticks=[0, 1/36, 3/36, 6/36],
           yticklabels=["0", "1/36", "3/36", "6/36"], xlabel="Sum of the dice",
           ylabel="Probability", title="Count the pairs for each sum")
    clean(bx)
    fig.text(.5, .025, "Green: six ways to make 7. Numbers above bars count pairs; divide each by 36.",
             ha="center", fontsize=11)
    fig.subplots_adjust(left=.07, right=.98, top=.87, bottom=.19, wspace=.32)
    save(fig, "01-dice")


def input_axes(ax, t, compact=False):
    box(ax, 0, 2, .5, BLUE, r"$f_U(\tau)$", fill=True)
    box(ax, t-3, t, 1/3, ORANGE, r"$f_V(t-\tau)$", fill=True)
    lo, hi = overlap(t)
    if hi > lo:
        ax.axvspan(lo, hi, color=GREEN, alpha=.12, ymin=0, ymax=.54)
        ax.plot([lo, hi], [.022, .022], color=GREEN, lw=6, solid_capstyle="butt")
    ax.set(xlim=(-3.6, 5.8), ylim=(0, .63), yticks=[0, 1/3, .5],
           yticklabels=["0", "1/3", "1/2"], xlabel=r"Integration coordinate $\tau$",
           ylabel="Density", xticks=[-3, 0, 2, 3, 5])
    clean(ax)
    if not compact:
        ax.legend(loc="upper right", frameon=False, ncol=2)


def uniform_keyframes():
    fig = plt.figure(figsize=(12, 7))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.1], hspace=.60, wspace=.28)
    values = [1, 2.5, 4]
    for i, t in enumerate(values):
        ax = fig.add_subplot(gs[0, i])
        input_axes(ax, t, compact=True)
        lo, hi = overlap(t)
        ax.set_title(f"t = {t:g}: overlap [{lo:g}, {hi:g}]\nlength {hi-lo:g}; area {(hi-lo)/6:.3f}", fontsize=12)
        if i > 0:
            ax.set_ylabel("")
    ax = fig.add_subplot(gs[1, :])
    x = np.linspace(-.5, 5.5, 601)
    ax.plot(x, density(x), color=GREEN, lw=3)
    ax.fill_between(x, density(x), color=GREEN, alpha=.08)
    for t in values:
        ax.plot([t, t], [0, density(t)], ls=":", color=MUTED)
        ax.scatter(t, density(t), color=GREEN, s=55, zorder=4)
    ax.set(xlim=(-.5, 5.5), ylim=(0, .43), xticks=[0, 1, 2, 2.5, 3, 4, 5],
           yticks=[0, 1/6, 1/3], yticklabels=["0", "1/6", "1/3"],
           xlabel=r"Output coordinate $t$ (possible sum $U+V$)", ylabel=r"$f_{U+V}(t)$")
    ax.text(1, .37, "growing overlap", ha="center", fontsize=11)
    ax.text(2.5, .37, "full overlap", ha="center", fontsize=11)
    ax.text(4, .37, "shrinking overlap", ha="center", fontsize=11)
    clean(ax)
    fig.suptitle("Two uniform densities: product height 1/6 × overlap length", fontsize=17, y=.98)
    fig.text(.5, .918, "Blue: fixed [0, 2]     Orange: reflected and shifted [t − 3, t]     Green: overlap", ha="center", fontsize=12)
    fig.subplots_adjust(left=.08, right=.98, top=.80, bottom=.10)
    save(fig, "02-uniform-keyframes")


def uniform_animation():
    fig, axes = plt.subplots(3, 1, figsize=(10, 8.2), gridspec_kw={"height_ratios": [1, .85, 1]})
    fig.subplots_adjust(left=.10, right=.97, top=.86, bottom=.09, hspace=.57)
    # Holds retain the same exact coordinates; no interpolated or invented densities.
    ts = np.r_[np.repeat(-.5, 8), np.linspace(-.5, 0, 5),
               np.linspace(0, 2, 25), np.repeat(2, 7),
               np.linspace(2, 3, 15), np.repeat(3, 7),
               np.linspace(3, 5, 25), np.linspace(5, 5.5, 5), np.repeat(5.5, 9)]
    grid = np.linspace(-.5, 5.5, 601)
    def frame(i):
        t = float(ts[i])
        a, b, c = axes
        for ax in axes:
            ax.clear()
        input_axes(a, t)
        phase = "no overlap" if t <= 0 or t >= 5 else "growing overlap" if t < 2 else "full overlap" if t <= 3 else "shrinking overlap"
        fig.suptitle(f"Reflect, then slide: t = {t:.2f}  ·  {phase}", fontsize=17, y=.98)
        a.set_title(r"$f_V(\tau)\ \to\ f_V(-\tau)\ \to\ f_V(t-\tau)$; move horizontally as $t$ increases", fontsize=12, pad=13)
        lo, hi = overlap(t)
        length = max(0, hi-lo)
        if length > 0:
            box(b, lo, hi, 1/6, GREEN, fill=True)
        b.set(xlim=(-3.6, 5.8), ylim=(0, .25), xticks=[-3, 0, 2, 3, 5],
              yticks=[0, 1/6], yticklabels=["0", "1/6"], xlabel=r"Integration coordinate $\tau$",
              ylabel="Product", title=f"Multiply, then integrate: area = (1/6) × {length:.2f} = {length/6:.3f}")
        clean(b)
        past = grid <= t
        c.plot(grid, density(grid), color="#cbd4d8", lw=1.5, ls="--")
        c.plot(grid[past], density(grid[past]), color=GREEN, lw=3)
        c.scatter([t], [density(t)], color=GREEN, s=55, zorder=4)
        c.set(xlim=(-.65, 5.65), ylim=(0, .40), xticks=[0, 2, 3, 5],
              yticks=[0, 1/6, 1/3], yticklabels=["0", "1/6", "1/3"],
              xlabel=r"Output coordinate $t$", ylabel=r"$f_{U+V}(t)$")
        clean(c)
        return []
    animation = FuncAnimation(fig, frame, frames=len(ts), interval=90)
    animation.save(OUT / "03-uniform-slide.gif", writer=PillowWriter(fps=11), dpi=100)
    plt.close(fig)
    # Inspect decoded GIF data, including every interval and both zero-overlap states.
    with Image.open(OUT / "03-uniform-slide.gif") as gif:
        decoded_count = gif.n_frames
        picks = np.unique(np.linspace(0, decoded_count-1, 8, dtype=int))
        thumbs = []
        for idx in picks:
            gif.seek(int(idx))
            im = gif.convert("RGB")
            im.thumbnail((500, 410))
            thumb = Image.new("RGB", (500, 438), "white")
            thumb.paste(im, (0, 28))
            ImageDraw.Draw(thumb).text((12, 7), f"Decoded GIF frame {idx}", fill=INK)
            thumbs.append(thumb)
        sheet = Image.new("RGB", (2000, 876), "white")
        for n, im in enumerate(thumbs):
            sheet.paste(im, ((n % 4)*500, (n // 4)*438))
        sheet.save(OUT / "03-decoded-contact-sheet.png")
        for label, idx in zip(["start", "rise", "plateau", "fall", "end"],
                              [0, int(decoded_count*.27), int(decoded_count*.5), int(decoded_count*.75), decoded_count-1]):
            gif.seek(idx)
            gif.convert("RGB").save(OUT / f"03-inspect-{label}.png")
    return {"requested_frames": len(ts), "decoded_frames": decoded_count,
            "decoded_contact_indices": [int(x) for x in picks], "t_range": [-.5, 5.5]}


def kernel_products():
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    ax.axis("off")
    xs = [2, 4, 8]
    rows = [("Input patch (oldest → newest)", xs, BLUE, .77),
            ("Cross-correlation: stored weights", [1, 2, 3], ORANGE, .52),
            ("Convolution: reversed weights", [3, 2, 1], GREEN, .27)]
    for label, values, color, ypos in rows:
        ax.text(.015, ypos+.045, label, va="center", fontsize=12, transform=ax.transAxes)
        for j, value in enumerate(values):
            xpos = .40+j*.10
            ax.add_patch(Rectangle((xpos, ypos-.035), .08, .16, transform=ax.transAxes,
                         facecolor=color, alpha=.12, edgecolor=color, lw=1.5))
            ax.text(xpos+.04, ypos+.045, str(value), ha="center", va="center", fontsize=18,
                    color=color, transform=ax.transAxes)
    ax.text(.73, .565, "2×1 + 4×2 + 8×3\n= 34", transform=ax.transAxes, va="center", fontsize=15, color=ORANGE)
    ax.text(.73, .315, "2×3 + 4×2 + 8×1\n= 22", transform=ax.transAxes, va="center", fontsize=15, color=GREEN)
    ax.text(.015, .04, "Stored weights: h[0] = 1, h[1] = 2, h[2] = 3. Same patch; anchors differ: r[0] and y[2].",
            transform=ax.transAxes, fontsize=11)
    fig.suptitle("An asymmetric kernel makes the flip visible", fontsize=17, y=.98)
    fig.subplots_adjust(left=.02, right=.98, bottom=.05, top=.9)
    save(fig, "04-kernel-products")


def moving_average():
    # Small invented channel, in microvolts, at equally spaced sample times.
    x = np.array([2, 4, 8, 10, 6, 2, -2, -4, -1, 3, 8, 7, 3, 0, -3], dtype=float)
    n = np.arange(len(x))
    y = np.convolve(x, np.ones(3)/3, mode="valid")
    fig, (a, b) = plt.subplots(1, 2, figsize=(11.6, 4.5), gridspec_kw={"width_ratios": [1, 2]})
    a.stem([0, 1, 2], [1/3]*3, linefmt=GREEN, markerfmt="o", basefmt=" ")
    a.set(xlim=(-.6, 2.6), ylim=(0, .5), xticks=[0, 1, 2],
          yticks=[0, 1/3], yticklabels=["0", "1/3"], xlabel="Lag k (samples)",
          ylabel="Weight h[k]", title="Three-point boxcar")
    a.text(1, .42, "Weights sum to 1", ha="center", fontsize=12, color=GREEN)
    clean(a)
    b.plot(n, x, ".-", color=BLUE, alpha=.7, label="Constructed input x[n]", lw=1.4)
    b.plot(n[2:], y, "o-", color=GREEN, label="Trailing 3-sample mean y[n]", lw=2.3, markersize=4)
    b.axvspan(-.15, 2.15, color=GREEN, alpha=.07)
    b.annotate("y[2] = (2 + 4 + 8)/3", xy=(2, y[0]), xytext=(3.7, 10.5),
                fontsize=11, arrowprops={"arrowstyle": "->", "color": GREEN})
    b.set(xlim=(-.2, 14.4), ylim=(-5.5, 12.7), xlabel="Sample index n", ylabel="Amplitude (µV)",
          title="One illustrative EEG channel: average across time")
    b.legend(loc="lower left", frameon=False, fontsize=10)
    clean(b)
    fig.text(.5, .02, "Synthetic values, not recorded EEG. First output is at n = 2; no padding or future samples.", ha="center", fontsize=11)
    fig.subplots_adjust(left=.07, right=.98, bottom=.20, top=.86, wspace=.30)
    save(fig, "05-moving-average")
    return x, y


def checks(x, y, animation):
    counts = [sum(a+b == s for a in range(1, 7) for b in range(1, 7)) for s in range(2, 13)]
    assert counts == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    assert sum(Fraction(c, 36) for c in counts) == 1
    t = sp.symbols("t", real=True)
    pieces = [(t/6, 0, 2), (sp.Rational(1, 3), 2, 3), ((5-t)/6, 3, 5)]
    mass = sum(sp.integrate(f, (t, a, b)) for f, a, b in pieces)
    mean = sum(sp.integrate(t*f, (t, a, b)) for f, a, b in pieces)
    second = sum(sp.integrate(t*t*f, (t, a, b)) for f, a, b in pieces)
    variance = sp.simplify(second-mean**2)
    assert mass == 1 and mean == sp.Rational(5, 2) and variance == sp.Rational(13, 12)
    assert pieces[0][0].subs(t, 2) == pieces[1][0] == pieces[2][0].subs(t, 3)
    grid = np.linspace(-1, 6, 281)
    numerical = []
    for value in grid:
        pts = sorted({0., 2., *[p for p in [value-3, value] if 0 < p < 2]})
        integral = quad(lambda u: (1/6) if 0 <= value-u <= 3 else 0.,
                        0, 2, points=pts)[0]
        numerical.append(abs(integral-float(density(value))))
    assert max(numerical) < 1e-12
    assert np.allclose(y, [x[i-2:i+1].mean() for i in range(2, len(x))])
    assert np.allclose(y[:3], [14/3, 22/3, 8])
    recurrence = y[:-1] + (x[3:] - x[:-3])/3
    assert np.allclose(recurrence, y[1:])
    weights = np.array([1, 2, 3])
    assert np.correlate(x[:3], weights, "valid").item() == 34
    assert np.convolve(x[:3], weights, "valid").item() == 22
    assert np.allclose(np.convolve(np.ones(10)*7, np.ones(3)/3, "valid"), 7)
    # The causal box is coefficient-symmetric about lag 1, not about lag 0.
    assert np.allclose(np.correlate(x, np.ones(3)/3, "valid"), y)
    svgs = sorted(OUT.glob("*.svg"))
    for path in svgs:
        ET.parse(path)
    raw = ROOT / "raw/assets/2026-11-15-convolution-uniform-handwriting.png"
    report = {
        "status": "PASS", "date": "2026-11-15", "author": "Codex",
        "figures": "Original analytic illustrations and constructed samples; not recovered source figures or measured EEG.",
        "dice_counts": counts, "uniform_mass": str(mass), "uniform_mean": str(mean),
        "uniform_variance": str(variance), "uniform_quadrature_max_abs_error": max(numerical),
        "handwriting_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        "input_microvolts": x.tolist(), "moving_average_full_window_outputs": y.tolist(),
        "moving_average_anchor": "Newest sample n; n starts at 2 for M=3; no padding.",
        "asymmetric_patch": {"input": [2, 4, 8], "weights": [1, 2, 3], "cross_correlation_r0": 34, "convolution_y2": 22},
        "checks": ["exact dice enumeration", "symbolic normalization/moments/continuity",
                   "independent numerical integration across all support regimes", "moving mean/direct convolution/recurrence",
                   "constant-signal preservation", "asymmetric kernel orientation and index anchors", "SVG XML parsing"],
        "animation": animation,
        "figure_inspection": "See PNG previews and decoded GIF frames; live Obsidian rendering is a separate check.",
        "sources": [
            "https://www.probabilitycourse.com/chapter6/6_1_2_sums_random_variables.php (section 6.1.2)",
            "https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html (sections 7.2.1, 7.2.5)",
            "https://docs.pytorch.org/docs/2.15/generated/torch.nn.Conv1d.html (cross-correlation definition)",
            "https://www.dspguide.com/CH15.PDF (pp. 277–280, moving averages and frequency limitations)"
        ],
    }
    (OUT / "checks.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "uniform_mass": str(mass), "max_quadrature_error": max(numerical),
                      "svg_count": len(svgs), "gif_decoded_frames": animation["decoded_frames"]}))


if __name__ == "__main__":
    dice()
    uniform_keyframes()
    anim_info = uniform_animation()
    signal, mean = moving_average()
    kernel_products()
    checks(signal, mean, anim_info)
