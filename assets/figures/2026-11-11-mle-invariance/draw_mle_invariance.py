"""Original static figure for the introductory MLE-invariance reference.

Reproduce with Python 3 + numpy, matplotlib, scipy, Pillow:
    python <absolute path to this file>
Outputs are always placed next to this script, independent of working directory.

Constructed example (not user data): two independent normal measurements,
x = [8, 12] cm, with KNOWN mean 10 cm and unknown variance v > 0.
The variance MLE is v_hat = mean((x - 10)**2) = 4 cm^2.
The SAME model is reparameterized by s = sqrt(v) > 0, so s_hat = 2 cm.
No observation is transformed; there is no parameter-density Jacobian.

Analytic check: L(v)/L(4) = (4/v) exp(1 - 4/v). For r = 4/v > 0,
log r <= r - 1 implies the relative likelihood <= 1, equality only at v=4.
L_s(s) = L_v(s**2), so its unique maximizer is s=2. Numerical checks below
support this analytic identity; grid agreement is not offered as a proof.

Theorem source, actually read 2026-11-11 (America/New_York):
UC Berkeley STAT 135, 'Functions of Estimators and the Delta Method',
'Estimating a function of Parameter with MLE', Theorem 1, standard-deviation
example and one-to-one proof:
https://stat135.berkeley.edu/fall-2026/Modules/11-DeltaMethod.html#estimating-a-function-of-parameter-with-mle
All plotting geometry and numerical values here are original synthesis.
"""

from pathlib import Path
import json
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from PIL import Image
from scipy.optimize import minimize_scalar


OUT = Path(__file__).resolve().parent
DATA_CM = np.array([8.0, 12.0])
KNOWN_MEAN_CM = 10.0
V_HAT = float(np.mean((DATA_CM - KNOWN_MEAN_CM) ** 2))
S_HAT = float(np.sqrt(V_HAT))


def log_likelihood_v(v):
    """Independent normal likelihood, parameterized by variance in cm^2."""
    v = np.asarray(v, dtype=float)
    return (-DATA_CM.size / 2 * np.log(2 * np.pi * v)
            - np.sum((DATA_CM - KNOWN_MEAN_CM) ** 2) / (2 * v))


def log_likelihood_s(s):
    """Same observations and model, independently evaluated using SD in cm."""
    s = np.asarray(s, dtype=float)
    z = (DATA_CM[:, None] - KNOWN_MEAN_CM) / np.atleast_1d(s)
    result = np.sum(-np.log(np.atleast_1d(s)) - .5 * np.log(2 * np.pi)
                    - .5 * z ** 2, axis=0)
    return result.item() if s.ndim == 0 else result


LOG_MAX = float(log_likelihood_v(V_HAT))


def relative_v(v):
    return np.exp(log_likelihood_v(v) - LOG_MAX)


def relative_s(s):
    return np.exp(log_likelihood_s(s) - LOG_MAX)


def checks():
    assert V_HAT == 4.0 and S_HAT == 2.0
    s = np.geomspace(.05, 100, 10001)
    v = np.geomspace(.0025, 10000, 10001)
    err = float(np.max(np.abs(relative_v(s ** 2) - relative_s(s))))
    assert err < 5e-15
    assert abs(float(relative_v(V_HAT)) - 1) < 1e-15
    assert abs(float(relative_s(S_HAT)) - 1) < 1e-15
    assert np.all(relative_v(v) <= 1 + 1e-14)
    assert np.all(relative_s(s) <= 1 + 1e-14)
    opt_v = minimize_scalar(lambda a: -log_likelihood_v(a),
                            bounds=(.01, 100), method='bounded',
                            options={'xatol': 1e-11})
    opt_s = minimize_scalar(lambda a: -log_likelihood_s(a),
                            bounds=(.1, 10), method='bounded',
                            options={'xatol': 1e-11})
    assert opt_v.success and opt_s.success
    assert abs(opt_v.x - V_HAT) < 1e-6
    assert abs(opt_s.x - S_HAT) < 1e-6
    return {
        'status': 'PASS',
        'data_cm': DATA_CM.tolist(),
        'model': 'Independent Normal(10 cm, v); known mean; v > 0',
        'variance_mle_cm2': V_HAT,
        'standard_deviation_mle_cm': S_HAT,
        'max_relative_likelihood_identity_error': err,
        'independent_numeric_variance_mle': float(opt_v.x),
        'independent_numeric_sd_mle': float(opt_s.x),
        'analytic_certificate': 'log(r) <= r - 1 for r > 0; r = 4/v',
        'axis_ranges': {'variance_cm2': [0, 16], 'sd_cm': [0, 4]},
        'matching_parameter_values': [[1, 1], [4, 2], [9, 3]],
        'likelihood_scale': 'Same likelihood divided by its common maximum; not a probability density over the parameter',
        'scope': 'Constructed example and coordinate identity, not empirical model validation',
    }


def draw():
    ink = '#182b3a'
    muted = '#607583'
    curve = '#187b8b'
    gold = '#c67d11'
    bg = '#f7fafc'
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 12,
        'text.color': ink, 'axes.labelcolor': ink,
        'xtick.color': muted, 'ytick.color': muted,
        'svg.hashsalt': 'mle-invariance-initial-v1',
    })
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.7), sharey=True)
    fig.patch.set_facecolor(bg)
    fig.subplots_adjust(left=.085, right=.975, bottom=.22, top=.64, wspace=.30)
    fig.text(.5, .94, 'Same best fit, different parameter scale',
             ha='center', va='center', fontsize=19, weight='bold')
    fig.text(.285, .80, r'Variance MLE:  $4\ \mathrm{cm}^2$',
             ha='center', va='center', fontsize=16, weight='bold')
    fig.text(.745, .80, r'Standard-deviation MLE:  $2\ \mathrm{cm}$',
             ha='center', va='center', fontsize=16, weight='bold')
    arrow = FancyArrowPatch((.445, .80), (.54, .80), transform=fig.transFigure,
                            arrowstyle='-|>', mutation_scale=17,
                            linewidth=1.7, color=gold)
    fig.add_artist(arrow)
    fig.text(.493, .855, 'square root', color=muted, fontsize=10, ha='center')

    vv = np.unique(np.r_[np.linspace(.02, 16, 1601), V_HAT])
    ss = np.unique(np.r_[np.linspace(.02, 4, 1601), S_HAT])
    for ax, xx, yy, peak, other, lim, ticks, label in [
        (axes[0], vv, relative_v(vv), V_HAT, [1, 9], 16, [0, 4, 9, 16],
         r'Variance $v=\sigma^2$ (cm$^2$)'),
        (axes[1], ss, relative_s(ss), S_HAT, [1, 3], 4, [0, 1, 2, 3, 4],
         r'Standard deviation $\sigma$ (cm)'),
    ]:
        ax.set_facecolor('white')
        ax.plot(xx, yy, color=curve, linewidth=2.8)
        ax.fill_between(xx, 0, yy, color=curve, alpha=.055)
        ax.plot([peak, peak], [0, 1], linestyle='--', color=gold,
                linewidth=1.3, zorder=2)
        ax.scatter([peak], [1], s=76, color=gold, edgecolor='white',
                   linewidth=1.1, zorder=4)
        ax.annotate('maximum', xy=(peak, 1), xytext=(peak+.12*lim, 1.09),
                    fontsize=11, color=gold, ha='left', va='center',
                    arrowprops={'arrowstyle': '-', 'color': gold, 'lw': .8})
        values = relative_v(other) if ax is axes[0] else relative_s(other)
        ax.scatter(other, values, s=29, color=curve, edgecolor='white',
                   linewidth=.7, zorder=3)
        ax.set_xlim(0, lim)
        ax.set_ylim(0, 1.2)
        ax.set_xticks(ticks)
        ax.set_yticks([0, .5, 1])
        ax.set_xlabel(label, fontsize=12, labelpad=9)
        ax.grid(axis='y', color='#dfe7ec', linewidth=.7)
        ax.spines[['top', 'right']].set_visible(False)
        ax.spines[['left', 'bottom']].set_color('#c6d2da')
        ax.tick_params(length=3)
    axes[0].set_ylabel('Relative likelihood', fontsize=12, labelpad=9)
    axes[1].tick_params(labelleft=True)
    fig.text(.5, .075, 'Same data and likelihood values; only the horizontal scale changes.',
             ha='center', fontsize=12, color=muted)
    fig.text(.5, .025, 'Illustrative normal model  |  Likelihood maximum scaled to 1',
             ha='center', fontsize=9, color=muted)
    svg = OUT / 'mle-invariance.svg'
    png = OUT / 'mle-invariance.png'
    fig.savefig(svg, facecolor=bg, metadata={'Date': None})
    fig.savefig(png, facecolor=bg, dpi=160)
    plt.close(fig)
    root = ET.parse(svg).getroot()
    assert root.tag.endswith('svg')
    with Image.open(png) as im:
        im.verify()
    return {'svg_xml': 'PASS', 'png_integrity': 'PASS'}


if __name__ == '__main__':
    report = checks()
    report.update(draw())
    (OUT / 'checks.json').write_text(json.dumps(report, indent=2) + '\n',
                                   encoding='utf-8')
    print(json.dumps(report, indent=2))
