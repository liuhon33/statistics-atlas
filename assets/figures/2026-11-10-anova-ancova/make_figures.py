"""Original introductory examples. Run with Python + NumPy, SciPy, Matplotlib.

Outputs go beside this script, independent of the working directory.
No external figure/data is copied. Numerical checks are illustration checks,
not evidence that model assumptions hold for real data.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'anova-ancova-initial'})
COLORS = ['#007C91', '#C36316', '#7955A2']

def save(fig, name):
    fig.savefig(OUT / (name + '.svg'), bbox_inches='tight', metadata={'Date': None})
    fig.savefig(OUT / (name + '.png'), dpi=160, bbox_inches='tight')
    ET.parse(OUT / (name + '.svg'))
    plt.close(fig)

# Three independently sampled groups, constructed for simple arithmetic.
groups = np.array([[8., 10., 12.], [12., 14., 16.], [16., 18., 20.]])
means = groups.mean(axis=1)
grand = groups.mean()
ss_between = 3 * np.sum((means - grand)**2)
ss_within = np.sum((groups - means[:, None])**2)
f_value = (ss_between / 2) / (ss_within / 6)
p_value = stats.f.sf(f_value, 2, 6)
assert np.allclose(means, [10, 14, 18])
assert np.isclose(ss_between, 96) and np.isclose(ss_within, 24)
assert np.isclose(f_value, 12) and np.isclose(p_value, .008)
assert np.allclose(stats.f_oneway(*groups), [f_value, p_value])

fig, ax = plt.subplots(figsize=(8.5, 4.4))
fig.suptitle('ANOVA: compare mean separation with within-group scatter',
             fontsize=15, weight='bold', y=1.02)
for i, (data, mean, color) in enumerate(zip(groups, means, COLORS)):
    ax.scatter(i + np.array([-.10, 0, .10]), data, c=color, s=70, zorder=4)
    ax.hlines(mean, i-.28, i+.28, color=color, lw=3)
    ax.text(i+.31, mean, f'mean {mean:.0f}', color=color, va='center',
            bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 1.5})
    ax.annotate('', (i-.22, mean+2), (i-.22, mean-2),
                arrowprops={'arrowstyle': '<->', 'color': color, 'lw': 1.4})
ax.axhline(grand, color='#677480', linestyle=':', lw=1.4, zorder=0)
ax.text(2.72, grand+.35, 'overall mean 14', ha='right', color='#53616E', fontsize=10)
ax.set(xlim=(-.5, 2.8), ylim=(6, 22), xticks=[0, 1, 2],
       xticklabels=['Fertilizer A', 'Fertilizer B', 'Fertilizer C'],
       ylabel='Plant height (cm)', yticks=range(6, 23, 2))
ax.grid(axis='y', alpha=.14)
fig.text(.13, -.16, 'Dots = plants   |   bars = group means   |   arrows = within-group spread\n'
         'Constructed data: A = 8, 10, 12; B = 12, 14, 16; C = 16, 18, 20 cm.\n'
         'One-way test: F(2, 6) = 12, p = 0.008. It does not identify which pairs differ.',
         fontsize=10, linespacing=1.6)
save(fig, 'anova-initial')

# Teaching methods A/B: x is a pre-course test and y is a final test, in points.
# Residuals are orthogonal to each group's intercept and x, so OLS is exact.
x_a = np.array([40., 45., 50., 55., 60.])
x_b = x_a + 10
e = np.array([1., -2., 2., -2., 1.])
y_a = 45 + .5*x_a + e
y_b = 50 + .5*x_b + e
x = np.r_[x_a, x_b]
y = np.r_[y_a, y_b]
g = np.r_[np.zeros(5), np.ones(5)]
design = np.column_stack([np.ones(10), g, x])
coef, *_ = np.linalg.lstsq(design, y, rcond=None)
common_x = x.mean()
adjusted = np.array([[1, 0, common_x], [1, 1, common_x]]) @ coef
raw = np.array([y_a.mean(), y_b.mean()])
assert np.allclose(coef, [45, 5, .5])
assert np.allclose(raw, [70, 80]) and np.isclose(common_x, 55)
assert np.allclose(adjusted, [72.5, 77.5])
assert np.allclose(raw - coef[2]*(np.array([x_a.mean(), x_b.mean()])-common_x), adjusted)
assert max(x_a.min(), x_b.min()) <= common_x <= min(x_a.max(), x_b.max())
residuals = y - design @ coef
assert np.allclose(design.T @ residuals, 0)

fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={'width_ratios': [1.5, 1]})
fig.suptitle('ANCOVA: compare groups at the same starting score',
             fontsize=15, weight='bold', y=1.02)
for i, (xx, yy, color) in enumerate(zip([x_a, x_b], [y_a, y_b], COLORS)):
    ax.scatter(xx, yy, color=color, s=40, alpha=.75)
    line_x = np.array([xx.min(), xx.max()])
    ax.plot(line_x, coef[0] + coef[1]*i + coef[2]*line_x, color=color, lw=2,
            label=f'Method {"AB"[i]}')
    ax.scatter(common_x, adjusted[i], s=85, marker='D', color=color, edgecolor='white', zorder=5)
    bx.plot([0, 1], [raw[i], adjusted[i]], color=color, lw=2, marker='o')
    bx.text(-.09, raw[i], f'{"AB"[i]}: {raw[i]:.0f}', ha='right', va='center', color=color)
    bx.text(1.09, adjusted[i], f'{adjusted[i]:.1f}', va='center', color=color)
ax.axvline(common_x, color='#677480', ls=':', zorder=0)
ax.annotate('', (common_x, adjusted[1]), (common_x, adjusted[0]),
            arrowprops={'arrowstyle': '<->', 'lw': 1.6, 'color': '#202C37'})
ax.text(56.3, 75, '5 points', va='center', fontsize=10)
ax.text(common_x, 62.8, 'compare at 55', ha='center', color='#53616E', fontsize=10)
ax.set(xlabel='Pre-course score (points)', ylabel='Final score (points)',
       xlim=(37, 73), ylim=(62, 88))
ax.legend(loc='upper left', frameon=False)
bx.set(xlim=(-.5, 1.55), ylim=(66, 84), xticks=[0, 1],
       xticklabels=['Raw means', 'Adjusted\nat x = 55'], ylabel='Final score (points)')
bx.set_title('10-point gap → 5-point gap', fontsize=12)
for a in [ax, bx]:
    a.grid(axis='y', alpha=.15)
fig.tight_layout(w_pad=2.3)
fig.text(.08, -.08, 'Constructed data. Common fitted slope = 0.5 final-score points per pre-course point.\n'
         'Diamonds = fitted means at x = 55; they are not new observations. Adjustment is not proof of causation.',
         fontsize=10, linespacing=1.6)
save(fig, 'ancova-initial')

checks = {'status': 'PASS', 'scope': 'Constructed examples, OLS arithmetic and SVG XML; not empirical assumption checks.',
          'anova': {'data_cm': groups.tolist(), 'means_cm': means.tolist(),
                    'ss_between': float(ss_between), 'ss_within': float(ss_within),
                    'df': [2, 6], 'F': float(f_value), 'p': float(p_value)},
          'ancova': {'x_A': x_a.tolist(), 'x_B': x_b.tolist(),
                     'y_A': y_a.tolist(), 'y_B': y_b.tolist(),
                     'OLS_intercept_groupB_slope': coef.tolist(),
                     'raw_means': raw.tolist(), 'common_x': float(common_x),
                     'adjusted_means': adjusted.tolist(), 'overlap_check': True,
                     'max_normal_equation_error': float(np.max(np.abs(design.T @ residuals)))}}
(OUT / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n', encoding='utf-8')
print(json.dumps(checks, indent=2))
