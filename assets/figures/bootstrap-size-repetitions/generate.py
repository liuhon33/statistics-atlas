"""Original Codex illustration, 2026-11-12; not the source chat's missing image.
Reproduce: python assets/figures/bootstrap-size-repetitions/generate.py

The fixed dataset comes from source assistant message
80005375-4e60-56c8-8548-613372080c8a. Exact distributions use integer
convolution of index counts. Histograms show probability per common bin,
never probability density; B=100 is a prefix of B=10,000 in each column.
"""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

OUT = Path(__file__).resolve().parent
DATA = np.array([1, 2, 2, 3, 4, 4, 4, 5, 7, 8], dtype=np.int64)
SEED = 20261112
MEAN = float(DATA.mean())
VAR = float(DATA.var(ddof=0))
BINS = np.arange(0.75, 8.26, 0.5)
assert len(DATA) == 10 and MEAN == 4 and math.isclose(VAR, 4.4)
rng = np.random.default_rng(SEED)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#243443", "text.color": "#243443",
    "xtick.color": "#243443", "ytick.color": "#243443",
    "svg.hashsalt": "bootstrap-size-repetitions-20261112",
})
fig, axes = plt.subplots(2, 2, figsize=(11.8, 7.7), sharex=True, sharey=True)
fig.subplots_adjust(left=.09, right=.98, bottom=.11, top=.76,
                    hspace=.34, wspace=.12)
fig.suptitle("Resample size changes the distribution; repetitions reveal it",
             fontsize=17, weight="bold", y=.98)
fig.text(.5, .92, "Fixed data: (1, 2, 2, 3, 4, 4, 4, 5, 7, 8)     |     n = 10, mean = 4",
         ha="center", fontsize=12)
fig.legend(handles=[
    Patch(facecolor="#4c9eab", alpha=.7, label="Simulated proportion in each bin"),
    Line2D([0], [0], color="#263844", lw=2, label="Exact probability in each bin"),
], loc="upper center", bbox_to_anchor=(.5, .895), ncol=2, frameon=False)
checks = {"seed": SEED, "data": DATA.tolist(), "mean": MEAN,
          "empirical_variance_denominator_n": VAR, "columns": {}}
for col, m in enumerate((1, 10)):
    counts = np.array([1], dtype=np.int64)
    one_draw_counts = np.bincount(DATA, minlength=9)
    for _ in range(m):
        counts = np.convolve(counts, one_draw_counts)
    assert int(counts.sum()) == len(DATA) ** m
    support = np.arange(len(counts)) / m
    pmf = counts.astype(float) / len(DATA) ** m
    exact_mean = float(pmf @ support)
    exact_var = float(pmf @ ((support - exact_mean) ** 2))
    assert math.isclose(exact_mean, MEAN, abs_tol=1e-12)
    assert math.isclose(exact_var, VAR / m, abs_tol=1e-12)
    binned_exact = np.histogram(support, bins=BINS, weights=pmf)[0]
    assert math.isclose(float(binned_exact.sum()), 1, abs_tol=1e-12)
    means = rng.choice(DATA, size=(10000, m), replace=True).mean(axis=1)
    info = {"exact_mean": exact_mean, "exact_variance": exact_var,
            "exact_sd": math.sqrt(exact_var), "simulations": {}}
    for row, reps in enumerate((100, 10000)):
        ax = axes[row, col]
        observed = means[:reps]
        masses = np.histogram(observed, bins=BINS)[0] / reps
        assert math.isclose(float(masses.sum()), 1, abs_tol=1e-12)
        ax.bar(BINS[:-1], masses, width=np.diff(BINS), align="edge",
               color="#4c9eab", alpha=.7, edgecolor="white", linewidth=.6)
        ax.stairs(binned_exact, BINS, color="#263844", linewidth=1.7)
        ax.axvline(MEAN, color="#8a9ba7", lw=1, ls=":", zorder=0)
        ax.set_title(f"B = {reps:,} repetitions", loc="left", fontsize=12, pad=8)
        ax.set_xlim(.5, 8.5)
        ax.set_ylim(0, .42)
        ax.set_xticks(range(1, 9))
        ax.set_yticks([0, .1, .2, .3, .4])
        ax.grid(axis="y", color="#e2e8ec", alpha=.8, zorder=0)
        ax.set_axisbelow(True)
        if col == 0:
            ax.set_ylabel("Probability per 0.5-wide bin")
        if row == 1:
            ax.set_xlabel("Mean of one resample")
        info["simulations"][str(reps)] = {
            "mean": float(observed.mean()),
            "sd_ddof_1": float(observed.std(ddof=1)),
            "max_bin_probability_error": float(np.max(np.abs(masses-binned_exact))),
        }
    axes[0, col].text(.5, 1.20,
        f"m = {m} draw{'s' if m != 1 else ''} per resample"
        + f"\nExact conditional SD = {math.sqrt(exact_var):.3f}",
        transform=axes[0, col].transAxes, ha="center", va="bottom",
        fontsize=12, weight="bold")
    checks["columns"][str(m)] = info
fig.text(.5, .025, "Same axes and bins throughout. Increasing B leaves the exact outline unchanged.",
         ha="center", fontsize=11)
fig.savefig(OUT / "bootstrap-size-repetitions.png", dpi=170,
            facecolor="white")
fig.savefig(OUT / "bootstrap-size-repetitions.svg", facecolor="white")
plt.close(fig)

rare = np.array([0] * 99 + [100])
assert rare.mean() == 1 and rare.var(ddof=0) == 99
checks["rare_value_example"] = {
    "mean": 1, "empirical_variance": 99,
    "probability_zero_mean": {str(m): .99 ** m for m in (20, 100, 1000)},
}
checks["se_ratio_m20_to_m100"] = math.sqrt(100 / 20)
checks["se_ratio_m10000_to_m100"] = math.sqrt(100 / 10000)
(OUT / "checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print(json.dumps(checks, indent=2))
