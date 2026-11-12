"""Original, reproducible L2 geometry and a synthetic electricity-demand example.

Run this file with Python 3, numpy and matplotlib; outputs go beside this file.
No user source image is read, changed or reconstructed as purported handwriting.
SVGs are deterministic (fixed hash salt, no timestamp); PNGs are inspection previews.
Exact Fraction checks enumerate finite probability spaces, not Monte Carlo draws.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

OUT = Path(__file__).resolve().parent
BG, FG, MUTED = "#111c2b", "#f1f5fa", "#afbed0"
NOISE, BIAS, VAR, TOTAL = "#65c9ff", "#df9bf3", "#ffc078", "#91e3ad"
PLANE = "#497e96"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13,
    "figure.facecolor": BG, "axes.facecolor": BG,
    "text.color": FG, "axes.labelcolor": FG, "axes.edgecolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "svg.fonttype": "path", "svg.hashsalt": "bias-variance-2026-11-12",
    "savefig.facecolor": BG,
})


def average(values):
    return sum(values, F(0)) / len(values)


def verify():
    # Orthonormal basis {1, U, V}; U and V are independent fair signs.
    # D=U in this constructed example, so H_D = span{1,U} exactly.
    outcomes = list(product((-1, 1), repeat=2))
    estimator = [F(2 + 4*u) for u, v in outcomes]
    response = [F(5 + 3*v) for u, v in outcomes]
    pieces = [[F(3*v), F(3), F(-4*u)] for u, v in outcomes]
    assert average(estimator) == 2 and average(response) == 5
    assert all(average([y for y, (uu, v) in zip(response, outcomes) if uu == u]) == 5
               for u in (-1, 1))
    cross = [average([p[a]*p[b] for p in pieces])
             for a, b in ((0, 1), (0, 2), (1, 2))]
    assert cross == [0, 0, 0]
    lengths2 = [average([p[j]**2 for p in pieces]) for j in range(3)]
    mse = average([(y-h)**2 for y, h in zip(response, estimator)])
    assert lengths2 == [9, 9, 16] and mse == sum(lengths2) == 34
    vertices = {"origin": [0, 0, 0], "mean_estimator": [2, 0, 0],
                "truth": [5, 0, 0], "estimator": [2, 4, 0], "response": [5, 0, 3]}
    a, m, f, y = [np.array(vertices[k], dtype=float)
                  for k in ("estimator", "mean_estimator", "truth", "response")]
    displacements = [m-a, f-m, y-f]
    assert np.array_equal(sum(displacements), y-a)
    assert all(np.dot(displacements[i], displacements[j]) == 0
               for i, j in ((0, 1), (0, 2), (1, 2)))
    assert np.dot(y-a, y-a) == 34

    # Fixed temperatures. Training responses and the new response have
    # independent +/-4 kWh noise. Enumerate all 2**10 equiprobable outcomes.
    temperatures = list(range(16, 25))
    truth = [F(50) + F((t-20)**2, 2) for t in temperatures]
    ranked = sorted(range(9), key=lambda i: (abs(temperatures[i]-20), temperatures[i]))
    rows = []
    samples = list(product((-4, 4), repeat=10))
    for k in (1, 3, 5, 7, 9):
        neighbors = ranked[:k]
        mu = average([truth[i] for i in neighbors])
        bias = F(50) - mu  # The note's sign convention, not the usual opposite sign.
        variance = F(16, k)
        expected_mse = F(16) + bias*bias + variance
        predictions = [average([truth[i] + s[i] for i in neighbors]) for s in samples]
        empirical_mu = average(predictions)
        empirical_var = average([(p-empirical_mu)**2 for p in predictions])
        empirical_mse = average([(F(50)+s[9]-p)**2 for s, p in zip(samples, predictions)])
        assert empirical_mu == mu and empirical_var == variance and empirical_mse == expected_mse
        assert average([F(s[9])*(mu-p) for s, p in zip(samples, predictions)]) == 0
        rows.append({"k": k, "neighbors_C": [temperatures[i] for i in neighbors],
                     "mean_prediction": str(mu), "signed_bias": str(bias),
                     "bias_squared": str(bias*bias), "variance": str(variance),
                     "noise": "16", "test_mse": str(expected_mse)})
    assert [r["test_mse"] for r in rows if r["k"] in (1, 5, 9)] == ["32", "101/5", "260/9"]
    return {
        "geometry": {"basis": ["constant 1", "independent fair sign U", "independent fair sign V"],
                     "D": "U", "estimator": "2+4U", "Y": "5+3V", "vertices": vertices,
                     "screen_basis": [[1, 0], [0.48, -0.62], [0, 1]],
                     "cross_inner_products_exact": [str(x) for x in cross],
                     "noise_bias_variance_squared_exact": [str(x) for x in lengths2],
                     "prediction_mse_exact": str(mse), "outcomes": len(outcomes),
                     "scope": "3D L2 slice; oblique screen projection does not preserve angles or lengths"},
        "application": {"scope": "Invented building electricity-demand model; not measured data",
                        "temperatures_C": temperatures, "mean_kWh": [str(x) for x in truth],
                        "target_C": 20, "truth_at_target_kWh": 50, "noise_variance_kWh2": 16,
                        "conditional_on_fixed_training_temperatures": True,
                        "exact_enumerated_noise_outcomes_per_k": len(samples), "rows": rows,
                        "max_exact_moment_or_mse_error": "0"},
        "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                    "matplotlib": matplotlib.__version__},
    }


def save(fig, stem, description):
    fig.savefig(OUT / f"{stem}.svg", metadata={"Date": None, "Description": description})
    fig.savefig(OUT / f"{stem}.png", dpi=140)
    plt.close(fig)
    root = ET.parse(OUT / f"{stem}.svg").getroot()
    assert root.tag.endswith("svg")


def draw_projection():
    fig = plt.figure(figsize=(16, 9))
    fig.text(.045, .945, "Bias–variance is two orthogonal projections", fontsize=25, weight="bold")
    fig.text(.045, .898, "Fixed input x  ·  Each endpoint is a whole random variable, not one observed value.",
             fontsize=14, color=MUTED)
    ax = fig.add_axes([.025, .205, .61, .65])
    ax.set(xlim=(-.65, 9.4), ylim=(-4.25, 3.95), aspect="equal")
    ax.axis("off")
    basis = np.array([[1, 0], [.48, -.62], [0, 1]])

    def project(p):
        return np.asarray(p) @ basis

    def line(a, b, color, width=2, style="-", arrow=False, zorder=4):
        a, b = project(a), project(b)
        if arrow:
            ax.annotate("", xy=b, xytext=a,
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=width,
                                        linestyle=style, mutation_scale=18, shrinkA=0, shrinkB=0),
                        zorder=zorder)
        else:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=width, ls=style, zorder=zorder)

    def label(p, text, color=FG, dx=0, dy=0, size=16, **kw):
        q = project(p)
        ax.text(q[0]+dx, q[1]+dy, text, color=color, fontsize=size, **kw)

    o = np.array([0., 0., 0.])
    m, f = np.array([2., 0., 0.]), np.array([5., 0., 0.])
    h, y = np.array([2., 4., 0.]), np.array([5., 0., 3.])
    corners = [(-.45, -1.15, 0), (6.5, -1.15, 0), (6.5, 5.3, 0), (-.45, 5.3, 0)]
    ax.add_patch(Polygon([project(p) for p in corners], facecolor=PLANE, alpha=.20,
                         edgecolor="#83b4c8", lw=1.5, zorder=0))
    line((-.5, 0, 0), (7, 0, 0), MUTED, 1.5, arrow=True, zorder=1)
    line(o, h, MUTED, 1.1, style=":", zorder=1)
    line(o, y, MUTED, 1.1, style=":", zorder=1)
    line(h, f, MUTED, 1.6, style="--", zorder=2)
    line(h, m, VAR, 3, arrow=True)
    line(m, f, BIAS, 3, arrow=True)
    line(f, y, NOISE, 3, arrow=True)
    line(h, y, TOTAL, 2.7, style="--", arrow=True, zorder=3)
    # Right-angle markers are constructed in the true orthonormal coordinates.
    for p, u, v in [(m, np.array([1., 0, 0]), np.array([0., 1, 0])),
                    (f, (h-f)/np.linalg.norm(h-f), np.array([0., 0, 1]))]:
        s = .25
        line(p+s*u, p+s*(u+v), FG, 1.3)
        line(p+s*(u+v), p+s*v, FG, 1.3)
    for p, col in [(o, MUTED), (m, VAR), (f, BIAS), (h, VAR), (y, NOISE)]:
        ax.scatter(*project(p), s=45, color=col, zorder=6)
    label(o, "$0$", dx=-.18, dy=.18, size=13)
    label(m, r"$\mu=\mathbb{E}_D\hat f$", dx=-.9, dy=.3, size=17)
    label(f, "$f(x)$", dx=.19, dy=-.42, size=17)
    label(h, r"$\hat f(x;D)$", dx=-.75, dy=-.49, size=18)
    label(y, r"$Y=f(x)+\varepsilon$", dx=-1.8, dy=.32, size=19)
    label((3.25, 0, 0), r"$|\mathrm{Bias}|$", BIAS, dx=-.08, dy=.28, size=16)
    label((2, 2, 0), r"$\sqrt{\mathrm{Var}}$", VAR, dx=-1.55, dy=-.03, size=16)
    label((5, 0, 1.4), r"$\|\varepsilon\|=\sigma$", NOISE, dx=.30, dy=.05, size=16)
    ax.annotate(r"$\sqrt{\mathrm{MSE}}$", xy=project(h+.6*(y-h)), xytext=(2.65, 1.2),
                color=TOTAL, fontsize=16, arrowprops=dict(arrowstyle="-", color=TOTAL, lw=1))
    label((6.4, 0, 0), r"$\mathrm{span}\{\mathbf{1}\}$", dx=-.15, dy=.3, size=14)
    label((-.4, 5.2, 0), r"$\mathcal{H}_D$: functions of training data", MUTED, dy=-.35, size=14)
    fig.text(.045, .18, "Perspective sketch: right angles are in L², not measured on the screen.",
             fontsize=12, color=MUTED)

    fig.text(.665, .805, "1   Project the estimator onto constants", fontsize=15, weight="bold", color=VAR)
    fig.text(.665, .747, r"$P_{\mathrm{span}\{\mathbf{1}\}}\hat f=\mu\,\mathbf{1}$", fontsize=20)
    fig.text(.665, .683, "The centered fluctuation is perpendicular\nto every constant, including the bias.",
             fontsize=13, linespacing=1.6, color=MUTED)
    fig.text(.665, .604, r"$\|f-\hat f\|^2=\mathrm{Bias}^2+\mathrm{Var}$", fontsize=17)
    fig.text(.665, .502, "2   Project the response onto training data", fontsize=15, weight="bold", color=NOISE)
    fig.text(.665, .443, r"$P_{\mathcal{H}_D}Y=f(x)\,\mathbf{1}$", fontsize=20)
    fig.text(.665, .377, "Independent, centered test noise is\nperpendicular to the entire data space.",
             fontsize=13, linespacing=1.6, color=MUTED)
    fig.text(.665, .297, r"$\|Y-\hat f\|^2=\sigma^2+\|f-\hat f\|^2$", fontsize=17)
    fig.text(.665, .216, "A 3D slice of L² is drawn; in general\nH_D has more than two dimensions.",
             fontsize=12, color=MUTED, linespacing=1.6)
    fig.text(.5, .085, r"$Y-\hat f=(\mu-\hat f)+(f-\mu)+(Y-f)$", ha="center", fontsize=23)
    fig.text(.5, .035, "Error = fluctuation + bias + noise; the three pieces are mutually orthogonal.",
             ha="center", fontsize=13, color=MUTED)
    save(fig, "01-l2-projections",
         "Original reconstruction inspired by the user's handwritten L2 diagram. "
         "A 3D slice with two orthogonal projections; perspective is not an isometry.")


def draw_application(checks):
    rows = {r["k"]: r for r in checks["application"]["rows"]}
    fig = plt.figure(figsize=(15, 6.4))
    fig.text(.05, .93, "Electricity-demand prediction: how many nearby days should we average?",
             fontsize=21, weight="bold")
    fig.text(.05, .875, "Synthetic fixed-temperature example  ·  Target: 20°C  ·  Noise variance: 16 kWh²",
             fontsize=13, color=MUTED)
    ax = fig.add_axes([.065, .20, .42, .59])
    x = np.linspace(16, 24, 241)
    t = np.arange(16, 25)
    ax.plot(x, 50+.5*(x-20)**2, color=FG, lw=2, label=r"True mean $f(t)$")
    ax.scatter(t, 50+.5*(t-20)**2, color=FG, s=35, zorder=4)
    ax.axvspan(17.9, 22.1, color=VAR, alpha=.10)
    ax.plot([18, 22], [51, 51], color=VAR, lw=2.5, label=r"Mean prediction for $k=5$")
    ax.plot([20, 20], [50, 51], color=BIAS, lw=4)
    ax.scatter([20], [50], color=FG, s=75, zorder=5)
    ax.scatter([20], [51], color=VAR, s=75, zorder=5)
    ax.annotate("Bias magnitude = 1 kWh", (20, 50.5), (16.2, 48.85),
                color=BIAS, fontsize=11, arrowprops=dict(arrowstyle="->", color=BIAS))
    ax.text(20, 55, "5 nearest temperatures\n18, 19, 20, 21, 22°C", ha="center",
            fontsize=11, color=VAR, linespacing=1.5)
    ax.set(xlim=(15.7, 24.3), ylim=(48, 60.5), xlabel="Temperature (°C)", ylabel="Mean daily electricity (kWh)")
    ax.set_xticks([16, 18, 20, 22, 24])
    ax.grid(alpha=.1)
    ax.legend(loc="upper center", frameon=False, fontsize=10, labelcolor=FG)
    ax.set_title("Averaging farther away shifts the mean", fontsize=14, pad=15)
    ax = fig.add_axes([.58, .20, .36, .59])
    ks = [1, 5, 9]
    b2 = np.array([float(F(rows[k]["bias_squared"])) for k in ks])
    v = np.array([float(F(rows[k]["variance"])) for k in ks])
    n = np.full(3, 16.)
    ix = np.arange(3)
    ax.bar(ix, n, color=NOISE, width=.60, label="Noise")
    ax.bar(ix, b2, bottom=n, color=BIAS, width=.60, label="Bias²")
    ax.bar(ix, v, bottom=n+b2, color=VAR, width=.60, label="Variance")
    for j, total in enumerate(n+b2+v):
        ax.text(j, total+.7, f"{total:.2f}", ha="center", fontsize=13, color=TOTAL, weight="bold")
    ax.set(ylim=(0, 39), ylabel="Expected test MSE (kWh²)")
    ax.set_xticks(ix, ["k = 1\nToo local", "k = 5\nBalanced here", "k = 9\nToo broad"])
    ax.set_title("The shortest variance leg need not win", fontsize=14, pad=15)
    ax.legend(loc="upper right", ncol=3, frameon=False, fontsize=10, labelcolor=FG)
    ax.grid(axis="y", alpha=.1)
    fig.text(.5, .065, "Left: true means, not observed readings.   Right: exact expectations, not one test sample or a fitted U-curve.",
             ha="center", fontsize=12, color=MUTED)
    save(fig, "02-electricity-knn-tradeoff",
         "Invented electricity-demand example; true mean is 50+0.5(t-20)^2, fixed design 16,...,24 C, "
         "independent noise variance 16. Exact test risks for k=1,5,9 are 32,101/5,260/9.")


if __name__ == "__main__":
    report = verify()
    draw_projection()
    draw_application(report)
    report["svg_xml_parse"] = "PASS: both SVG roots parsed"
    report["generated_artifact_sha256"] = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(OUT.iterdir()) if p.suffix in (".svg", ".png", ".py")
    }
    (OUT / "checks.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({"exact_checks": "PASS", "application_rows": report["application"]["rows"],
                      "svg_xml_parse": report["svg_xml_parse"]}, indent=2))
