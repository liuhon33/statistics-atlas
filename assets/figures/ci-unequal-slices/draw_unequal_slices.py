"""Exact 95% two-tail inversion for X ~ Uniform(theta/2, 3*theta/2).
Run with Python + NumPy + Matplotlib. Writes only adjacent generated artifacts.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
A, B = .525, 1.475
BLUE, ORANGE, GREEN, INK = '#2465ad', '#bf6014', '#218260', '#203347'

def main():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'svg.fonttype': 'none', 'axes.spines.top': False,
                         'axes.spines.right': False})
    fig = plt.figure(figsize=(12.8, 7.5))
    fig.suptitle('Two equal rejection tails, but UNEQUAL slice lengths',
                 fontsize=20, fontweight='bold', color=INK, y=.96)
    fig.text(.5, .895, r'$X\sim\mathrm{Uniform}(\theta/2,\,3\theta/2),\quad\theta>0$'
             '     |     95% non-rejection band: 0.525 b <= x <= 1.475 b',
             ha='center', fontsize=12, color=INK)
    ax = fig.add_axes([.07, .22, .43, .59])
    b = np.linspace(0, 2.4, 401)
    ax.fill_between(b, A*b, B*b, color=GREEN, alpha=.14)
    ax.plot(b, A*b, color=GREEN, lw=1.5)
    ax.plot(b, B*b, color=GREEN, lw=1.5)
    ax.plot(b, b, ':', color='#8b969e', lw=1)
    ax.axvline(1, color=BLUE, ls='--', lw=1)
    ax.axhline(1, color=ORANGE, ls='--', lw=1)
    ax.plot([1, 1], [A, B], color=BLUE, lw=6, solid_capstyle='butt')
    ax.plot([1/B, 1/A], [1, 1], color=ORANGE, lw=6, solid_capstyle='butt')
    ax.scatter([1], [1], s=85, facecolor=INK, edgecolor='white', zorder=5)
    ax.annotate('Fixed pair (b, x) = (1, 1)', xy=(1, 1), xytext=(.18, 2.13),
                arrowprops={'arrowstyle': '->', 'color': INK}, color=INK,
                bbox={'facecolor': 'white', 'alpha': .9, 'edgecolor': 'none'})
    ax.text(1.09, 1.52, '1.475', color=BLUE, fontsize=10)
    ax.text(.88, .44, '0.525', color=BLUE, ha='right', fontsize=10)
    ax.text(1/B-.04, .88, '0.678', color=ORANGE, ha='right', fontsize=10)
    ax.text(1/A+.03, 1.07, '1.905', color=ORANGE, fontsize=10)
    ax.text(1.75, .63, 'x = 0.525 b', color=GREEN, fontsize=10)
    ax.text(.15, 1.74, 'x = 1.475 b', color=GREEN, fontsize=10)
    ax.set(xlim=(0, 2.4), ylim=(0, 2.4), xlabel=r'Candidate parameter $b$',
           ylabel=r'Possible observed data $x$')
    ax.set_aspect('equal')
    ax.set_title('Widening band; equal axis scales', fontsize=13, pad=12)
    rx = fig.add_axes([.57, .32, .37, .37])
    for y, lo, hi, color in [(1, A, B, BLUE), (0, 1/B, 1/A, ORANGE)]:
        rx.plot([lo, hi], [y, y], lw=7, color=color, solid_capstyle='butt')
        rx.scatter([lo, hi], [y, y], s=35, color=color)
        rx.text(lo, y-.15, f'{lo:.3f}', ha='center', color=color)
        rx.text(hi, y-.15, f'{hi:.3f}', ha='center', color=color)
    rx.text(.04, 1.4, 'Vertical at b = 1: length 0.950', color=BLUE, fontsize=13)
    rx.text(.04, .4, 'Horizontal at x = 1: length 1.227', color=ORANGE, fontsize=13)
    rx.axvline(1, ls=':', color='#88929b', lw=1)
    rx.set(xlim=(0, 2.4), ylim=(-.45, 1.65), yticks=[], xlabel='Common numeric scale')
    rx.spines['left'].set_visible(False)
    rx.set_title('Compare lengths on one ruler', fontsize=13, pad=20)
    fig.text(.755, .22, 'Blue segment rotated for comparison, not rescaled.\nThe orange segment is about 29% longer.',
             ha='center', fontsize=11, color=INK)
    fig.text(.5, .105, 'Why? Under a larger candidate b, the sampling spread is larger: SD(X) = b / sqrt(12).',
             ha='center', fontsize=12, color=INK)
    fig.text(.5, .055, 'Unequal lengths do NOT break inversion: the same point is inside both slices, or outside both.',
             ha='center', fontsize=12, fontweight='bold', color=INK)
    svg = OUT / 'unequal-horizontal-vertical-slices.svg'
    fig.savefig(svg, facecolor='white')
    fig.savefig(OUT / 'unequal-horizontal-vertical-slices.png', dpi=150, facecolor='white')
    plt.close(fig)
    ET.parse(svg)
    # Proof is the algebra in the note; grid checks are supporting evidence.
    bs, xs = np.meshgrid(np.linspace(.08, 3.2, 337), np.linspace(.03, 4, 389))
    band = (A*bs <= xs) & (xs <= B*bs)
    ci = (xs/B <= bs) & (bs <= xs/A)
    cdf = np.clip(xs/bs - .5, 0, 1)
    p = 2*np.minimum(cdf, 1-cdf)
    away = np.abs(p-.05) > 1e-10
    assert np.array_equal(band[away], ci[away])
    assert np.array_equal(band[away], p[away] >= .05)
    assert abs((A-.5)-.025) < 1e-14
    assert abs((1.5-B)-.025) < 1e-14
    assert abs((B-A)-.95) < 1e-14
    assert 1/B < 1 < 1/A
    reject_x = 1.49
    reject_p = 2*(1.5-reject_x)
    assert reject_p < .05 and reject_x/B > 1
    report = {'model': 'X ~ Uniform(theta/2, 3*theta/2), theta>0',
              'alpha': .05, 'vertical_at_b1': [A, B], 'vertical_length': B-A,
              'horizontal_at_x1': [1/B, 1/A], 'horizontal_length': 1/A-1/B,
              'coverage': B-A, 'grid_pairs_checked_away_from_endpoints': int(away.sum()),
              'band_ci_pvalue_agreement': True, 'svg_xml_valid': True,
              'rejection_example': {'x': reject_x, 'b': 1, 'p': reject_p,
                                    'ci': [reject_x/B, reject_x/A]}}
    (OUT/'checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
