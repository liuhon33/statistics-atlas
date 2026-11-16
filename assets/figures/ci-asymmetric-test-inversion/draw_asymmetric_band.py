"""Reproduce the SVG/PNG with Python, NumPy and Matplotlib; no source-note edits.

Exact model: X = theta + E - 1, E ~ Exponential(rate=1), theta real.
Equal-tailed tests, reject p < alpha; closed inverted confidence intervals.
"""
from pathlib import Path
import json
import math
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
ALPHA = .05
L = -math.log(.975) - 1
U = -math.log(.025) - 1
BLUE = '#2465ad'
ORANGE = '#bd6417'
GREEN = '#167153'
RED = '#c33043'
INK = '#213449'

def pvalue(x, b):
    t = np.asarray(x) - np.asarray(b) + 1
    f = -np.expm1(-np.maximum(t, 0))
    return 2 * np.minimum(f, 1 - f)

def main():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'svg.fonttype': 'none', 'axes.spines.top': False,
                         'axes.spines.right': False})
    fig, axes = plt.subplots(1, 2, figsize=(13, 8))
    fig.subplots_adjust(left=.07, right=.97, top=.76, bottom=.25, wspace=.24)
    fig.suptitle('Different slices. Always the same decision at their intersection.',
                 fontsize=19, fontweight='bold', color=INK, y=.965)
    fig.text(.5, .905, r'An asymmetric, equal-tailed 95% band:  $b - 0.975 \leq x \leq b + 2.689$',
             ha='center', fontsize=14, color=INK)
    fig.text(.5, .855, 'Blue = vertical non-rejection region for b = 0     Orange = horizontal confidence interval',
             ha='center', fontsize=12)
    bs = np.linspace(-1.5, 4.5, 500)
    records = []
    for ax, x in zip(axes, [2., 3.]):
        lo, hi = x - U, x - L
        p = float(pvalue(x, 0))
        kept = lo <= 0 <= hi
        color = GREEN if kept else RED
        ax.fill_between(bs, bs + L, bs + U, color=GREEN, alpha=.13)
        ax.plot(bs, bs + L, color=GREEN, lw=1.2)
        ax.plot(bs, bs + U, color=GREEN, lw=1.2)
        ax.plot(bs, bs, ':', color='#88929b', lw=1)
        ax.axvline(0, color=BLUE, ls='--', lw=1.3)
        ax.plot([0, 0], [L, U], color=BLUE, lw=6, solid_capstyle='butt')
        ax.axhline(x, color=ORANGE, ls='--', lw=1.3)
        ax.plot([lo, hi], [x, x], color=ORANGE, lw=6, solid_capstyle='butt')
        ax.scatter([lo, hi], [x, x], color=ORANGE, s=35, zorder=5)
        ax.scatter([0], [x], s=125, color=color, edgecolor='white', linewidth=1.5, zorder=7)
        ax.annotate(f'SAME POINT (0, {x:g})\n' + ('inside the band' if kept else 'outside the band'),
                    xy=(0, x), xytext=(1.2, 3.85), color=color, fontsize=11,
                    arrowprops={'arrowstyle': '->', 'color': color},
                    bbox={'facecolor': 'white', 'alpha': .92, 'edgecolor': 'none'})
        ax.text(-.12, L - .17, '-0.975', ha='right', color=BLUE, fontsize=10)
        ax.text(-.12, U + .13, '2.689', ha='right', color=BLUE, fontsize=10)
        ax.text(2.2, -.8, f'95% CI = [{lo:.3f}, {hi:.3f}]', ha='center', color=ORANGE,
                bbox={'facecolor': 'white', 'alpha': .92, 'edgecolor': 'none'})
        ax.set(xlim=(-1.5, 4.5), ylim=(-1.5, 4.5),
               xlabel=r'Candidate parameter $b$', ylabel=r'Possible observed data $x$')
        ax.set_aspect('equal')
        ax.set_title(f'Observed x = {x:g}: ' + ('KEEP zero' if kept else 'REJECT zero'),
                     color=color, fontsize=14, pad=12)
        ax.text(.5, -.19, f'p(0) = {p:.4f} ' + ('>= 0.05   |   0 is IN the CI' if kept else '< 0.05   |   0 is OUT of the CI'),
                transform=ax.transAxes, ha='center', color=color, fontsize=12, fontweight='bold')
        records.append({'x': x, 'ci': [lo, hi], 'p_null_zero': p, 'zero_retained': kept})
    fig.text(.5, .105, 'Read vertically: is the dot on the blue segment?   Read horizontally: is it on the orange segment?',
             ha='center', fontsize=12, color=INK)
    fig.text(.5, .062, 'Both ask whether the SAME dot lies in the shaded band. No reflection or exchange of coordinates is needed.',
             ha='center', fontsize=12, color=INK, fontweight='bold')
    fig.text(.5, .018, r'Model: $X=\theta+E-1$, $E\sim\mathrm{Exponential}(1)$; $\theta\in\mathbb{R}$. Each null rejects 2.5% in each tail.',
             ha='center', fontsize=11, color=INK)
    svg = OUT / 'asymmetric-band-same-decision.svg'
    fig.savefig(svg, facecolor='white')
    fig.savefig(OUT / 'asymmetric-band-same-decision.png', dpi=150, facecolor='white')
    plt.close(fig)
    ET.parse(svg)
    # Analytic coverage: P(L <= E-1 <= U) = .975 - .025 = .95.
    coverage = math.exp(-(L + 1)) - math.exp(-(U + 1))
    assert abs(coverage - .95) < 1e-14
    b, x = np.meshgrid(np.linspace(-3, 5, 401), np.linspace(-3, 5, 401))
    band = (x >= b + L) & (x <= b + U)
    ci = (b >= x - U) & (b <= x - L)
    pkeep = pvalue(x, b) >= ALPHA
    assert np.array_equal(band, ci)
    assert np.array_equal(band, pkeep)
    assert L <= 2 <= U and not (2 + L <= 0 <= 2 + U)
    result = {'model': 'X=theta+Exp(1)-1', 'alpha': ALPHA, 'noise_quantiles': [L, U],
              'coverage': coverage, 'grid_pairs_checked': int(b.size),
              'band_ci_pvalue_agreement': True, 'swap_symmetry': False,
              'svg_xml_parsed': True, 'examples': records}
    (OUT / 'checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
