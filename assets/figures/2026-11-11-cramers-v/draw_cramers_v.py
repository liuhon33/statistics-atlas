"""Original illustrations and checks for the learning note
"Categorical association and Cramér's V" (2026-11-11).

All tables are invented toy examples. Run with a Python that has numpy, scipy and
matplotlib (D:/anaconda/python.exe worked); outputs are written beside this file:
01-three-tables.svg/.png, 02-same-strength-more-data.svg/.png and checks.json.

The hand formulas below are checked against SciPy's independent implementations
(scipy.stats.chi2_contingency with correction=False and
scipy.stats.contingency.association(method='cramer')).
"""
from pathlib import Path
import json
import numpy as np
from scipy import stats
from scipy.stats.contingency import association
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.colors import to_rgb
from matplotlib import patheffects as pe

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- mathematics
def expected(O):
    O = np.asarray(O, float)
    return O.sum(1, keepdims=True) * O.sum(0, keepdims=True) / O.sum()

def pearson_x2(O):
    O = np.asarray(O, float); E = expected(O)
    return float(((O - E) ** 2 / E).sum())

def cramers_v(O):
    O = np.asarray(O, float); r, c = O.shape
    return float(np.sqrt(pearson_x2(O) / (O.sum() * (min(r, c) - 1))))

def phi_2x2(O):
    (a, b), (c, d) = np.asarray(O, float)
    return float((a * d - b * c) / np.sqrt((a + b) * (c + d) * (a + c) * (b + d)))

def residuals(O):
    O = np.asarray(O, float); E = expected(O)
    return (O - E) / np.sqrt(E)

# Rows = housing (Apartment, House); columns = pet (Cat, Dog). n = 100 each.
TABLES = {
    'A': np.array([[25, 25], [25, 25]]),
    'B': np.array([[35, 15], [15, 35]]),
    'C': np.array([[50, 0], [0, 50]]),
}
SCALED = {20: TABLES['B'] // 5, 100: TABLES['B'], 1000: TABLES['B'] * 10}
MAJORS = np.array([[18, 6, 6], [9, 15, 6], [3, 9, 18]])   # Stats/Bio/Art x Library/Cafe/Home
PERFECT3 = np.diag([30, 30, 30])
OVERSAMPLED = np.array([[35, 15], [60, 140]])              # House row of B multiplied by 4

# ---------------------------------------------------------------- checks
checks = {'tables': {}, 'scaled': {}, 'identities': {}}
max_err = 0.0

def record(err):
    global max_err
    max_err = max(max_err, float(abs(err)))

def summarize(O):
    O = np.asarray(O)
    x2 = pearson_x2(O); v = cramers_v(O)
    ref = stats.chi2_contingency(O, correction=False)
    record(x2 - ref.statistic); record(v - association(O, method='cramer'))
    record(np.max(np.abs(expected(O) - ref.expected_freq)))
    df = (O.shape[0] - 1) * (O.shape[1] - 1)
    assert df == ref.dof
    return {'counts': O.tolist(), 'n': int(O.sum()), 'expected': expected(O).tolist(),
            'X2': x2, 'df': df, 'p': float(stats.chi2.sf(x2, df)), 'V': v,
            'sqrt_X2_over_n': float(np.sqrt(x2 / O.sum()))}

for k, O in TABLES.items():
    checks['tables'][k] = summarize(O)
    checks['tables'][k]['phi'] = phi_2x2(O)
    checks['tables'][k]['odds_ratio'] = (float(O[0, 0] * O[1, 1] / (O[0, 1] * O[1, 0]))
                                         if O[0, 1] * O[1, 0] else None)
for n, O in SCALED.items():
    checks['scaled'][str(n)] = summarize(O)
checks['tables']['majors_3x3'] = summarize(MAJORS)
checks['tables']['perfect_3x3'] = summarize(PERFECT3)
checks['tables']['oversampled_houses'] = summarize(OVERSAMPLED)
checks['tables']['oversampled_houses']['odds_ratio'] = float(35 * 140 / (15 * 60))
checks['tables']['oversampled_houses']['phi'] = phi_2x2(OVERSAMPLED)

# Expected toy values (exact arithmetic done by hand in the note).
T = checks['tables']
for got, want in [(T['A']['X2'], 0), (T['A']['V'], 0), (T['B']['X2'], 16), (T['B']['V'], .4),
                  (T['C']['X2'], 100), (T['C']['V'], 1), (T['majors_3x3']['X2'], 25.2),
                  (T['majors_3x3']['V'], np.sqrt(.14)), (T['perfect_3x3']['V'], 1),
                  (T['perfect_3x3']['sqrt_X2_over_n'], np.sqrt(2)),
                  (checks['scaled']['20']['X2'], 3.2), (checks['scaled']['1000']['X2'], 160)]:
    record(got - want); assert abs(got - want) < 1e-12, (got, want)
for n in SCALED:
    assert abs(checks['scaled'][str(n)]['V'] - .4) < 1e-12

# Identity checks on random 2x2 and r x c tables (all margins positive).
rng = np.random.default_rng(20261111)
id_max = {'X2_eq_n_phi2': 0., 'abs_phi_eq_V': 0., 'phi_eq_pearson_r_of_indicators': 0.,
          'scale_invariance_V': 0., 'permutation_invariance_V': 0., 'transpose_invariance_V': 0.}
bound_ok = True
for _ in range(2000):
    O = rng.integers(1, 60, size=(2, 2))
    n = O.sum(); phi = phi_2x2(O)
    id_max['X2_eq_n_phi2'] = max(id_max['X2_eq_n_phi2'], abs(pearson_x2(O) - n * phi ** 2) / max(1, pearson_x2(O)))
    id_max['abs_phi_eq_V'] = max(id_max['abs_phi_eq_V'], abs(abs(phi) - cramers_v(O)))
    x = np.repeat([1, 1, 0, 0], O.ravel()); y = np.repeat([1, 0, 1, 0], O.ravel())
    id_max['phi_eq_pearson_r_of_indicators'] = max(id_max['phi_eq_pearson_r_of_indicators'],
                                                   abs(np.corrcoef(x, y)[0, 1] - phi))
for _ in range(2000):
    r, c = rng.integers(2, 6, size=2)
    O = rng.integers(0, 30, size=(r, c)); O[:, 0] += 1; O[0, :] += 1
    if (O.sum(0) == 0).any() or (O.sum(1) == 0).any():
        continue
    v = cramers_v(O)
    bound_ok &= -1e-12 <= v <= 1 + 1e-12
    id_max['scale_invariance_V'] = max(id_max['scale_invariance_V'], abs(cramers_v(7 * O) - v))
    id_max['permutation_invariance_V'] = max(id_max['permutation_invariance_V'],
        abs(cramers_v(O[rng.permutation(r)][:, rng.permutation(c)]) - v))
    id_max['transpose_invariance_V'] = max(id_max['transpose_invariance_V'], abs(cramers_v(O.T) - v))
assert bound_ok and max(id_max.values()) < 1e-10, id_max
checks['identities'] = {'random_tables': 4000, 'max_abs_error': id_max, 'V_within_0_1': bool(bound_ok)}

# Small-sample upward bias: truly independent variables, all four cells probability 1/4.
bias = {}
for n in (20, 100, 1000):
    tabs = rng.multinomial(n, [.25] * 4, size=20000).reshape(-1, 2, 2)
    ok = (tabs.sum(1) > 0).all(1) & (tabs.sum(2) > 0).all(1)
    vs = np.array([cramers_v(t) for t in tabs[ok]])
    bias[str(n)] = {'simulations': int(ok.sum()), 'mean_V': float(vs.mean()),
                    'median_V': float(np.median(vs)), 'sqrt_df_over_n': float(np.sqrt(1 / n))}
checks['independence_simulation'] = {'seed': 20261111, 'cells': '2x2, P(cell)=1/4', 'results': bias}
checks['max_abs_error_vs_scipy_and_hand_values'] = max_err

# ---------------------------------------------------------------- figures
for f in ('segoeui.ttf', 'segoeuib.ttf'):
    p = Path('C:/Windows/Fonts') / f
    if p.exists():
        font_manager.fontManager.addfont(str(p))
BG, CARD, EDGE = '#f5f8fc', '#ffffff', '#d7e1ec'
INK, MUTED, BLUE = '#19324a', '#5b6f84', '#2867ba'
POS, NEG, NEUTRAL = '#0093a3', '#d46c20', '#e4e9ef'   # validated teal/orange pair (dataviz validator)
plt.rcParams.update({'font.family': ['Segoe UI', 'DejaVu Sans'], 'font.size': 13,
                     'text.color': INK, 'axes.labelcolor': INK, 'axes.edgecolor': MUTED,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'figure.facecolor': BG,
                     'axes.facecolor': CARD, 'savefig.facecolor': BG, 'svg.fonttype': 'none'})

def mix(c1, c2, t):
    a, b = np.array(to_rgb(c1)), np.array(to_rgb(c2))
    return tuple((1 - t) * a + t * b)

def tile_color(res, cap=5.0):
    t = min(abs(res) / cap, 1.0)
    return mix(NEUTRAL, POS if res > 0 else NEG, 0.15 + 0.85 * t) if abs(res) > 1e-12 else NEUTRAL

def card(fig, x, y, w, h):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=0.012',
                                      transform=fig.transFigure, facecolor=CARD, edgecolor=EDGE,
                                      linewidth=1.4, zorder=-5))

def figure_three_tables():
    fig = plt.figure(figsize=(15, 7.6))
    fig.text(.035, .935, 'Same row and column totals, three strengths of association',
             fontsize=24, weight='bold')
    fig.text(.035, .885, '100 households: housing type × preferred pet. Every row and every column '
             'totals 50, so independence predicts 25 per cell.', fontsize=15, color=MUTED)
    titles = {'A': 'A · No association', 'B': 'B · Moderate association', 'C': 'C · Perfect association'}
    gap = .025; w = (1 - 2 * .035 - 2 * gap) / 3
    for k, key in enumerate('ABC'):
        O = TABLES[key]; E = expected(O); R = residuals(O); s = checks['tables'][key]
        x0 = .035 + k * (w + gap)
        card(fig, x0, .2, w, .64)
        fig.text(x0 + .018, .79, titles[key], fontsize=18, weight='bold')
        ax = fig.add_axes([x0 + .075, .36, w - .095, .39])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        # Two horizontal strips (rows); each split left/right by the row's Cat share.
        for i, row in enumerate(['Apartment', 'House']):
            y_top = 1 - i * .5; h = .5 - .012
            left = 0
            for j, pet in enumerate(['Cat', 'Dog']):
                width = O[i, j] / O[i].sum()
                if width > 0:
                    gx = .006 if j == 1 and left > 0 else 0
                    ax.add_patch(Rectangle((left + gx, y_top - h), width - gx, h,
                                           facecolor=tile_color(R[i, j]), edgecolor='none'))
                    cx = left + width / 2
                    halo = [pe.withStroke(linewidth=3, foreground=tile_color(R[i, j]))]
                    ax.text(cx, y_top - h / 2 + .05, f'{pet} {O[i, j]}', ha='center', va='center',
                            fontsize=17, weight='bold', color=INK, zorder=6, path_effects=halo)
                    d = O[i, j] - E[i, j]
                    res_txt = ('0' if d == 0 else f'{d:+g}'.replace('-', '−'))
                    other = [q for q in range(2) if O[i, q] == 0]
                    if other:
                        res_txt += f"  ·  {['Cat', 'Dog'][other[0]]} 0"
                    ax.text(cx, y_top - h / 2 - .07, res_txt, ha='center', va='center',
                            fontsize=11.5, color=INK, zorder=6, path_effects=halo)
                left += width
            fig.text(x0 + .016, .36 + .39 * (y_top - h / 2), row, fontsize=13.5, color=INK,
                     va='center', rotation=90, ha='center')
        ax.plot([.5, .5], [-.02, 1.02], ls=(0, (5, 4)), color=BLUE, lw=1.6, clip_on=False, zorder=4)
        ax.text(.5, -.035, 'dashed: split if independent', color=INK, ha='center', va='top', fontsize=11)
        # V meter.
        mx = fig.add_axes([x0 + .075, .238, w - .095, .03]); mx.axis('off')
        mx.set_xlim(0, 1); mx.set_ylim(0, 1)
        mx.add_patch(Rectangle((0, .3), 1, .4, facecolor=NEUTRAL, edgecolor='none'))
        mx.add_patch(Rectangle((0, .3), s['V'], .4, facecolor=INK, edgecolor='none'))
        for t in (0, .5, 1):
            mx.text(t, -.35, f'{t:g}', ha='center', va='top', fontsize=10.5, color=MUTED)
        fig.text(x0 + .018, .29, f"χ² = {s['X2']:g}   ·   V = {s['V']:.2f}", fontsize=15, weight='bold')
    # Legend row.
    lx = .035
    for color, label in [(POS, 'more households than independence predicts'),
                         (NEG, 'fewer than independence predicts'),
                         (NEUTRAL, 'exactly as predicted')]:
        fig.patches.append(Rectangle((lx, .085), .016, .03, transform=fig.transFigure,
                                     facecolor=color, edgecolor=EDGE))
        fig.text(lx + .022, .1, label, va='center', fontsize=13)
        lx += .022 + .0072 * len(label) + .03
    fig.text(.035, .035, 'Tile area ∝ count. Second line: observed − expected count. Colour depth ∝ |O − E|/√E. '
             'Bar under each panel: V on its 0–1 scale. Invented counts.',
             fontsize=12, color=MUTED)
    return fig

def figure_scaling():
    ns = np.geomspace(10, 3000, 400)
    x2 = .16 * ns                       # X² = n·φ² with φ = 0.4, proportions held fixed
    p = stats.chi2.sf(x2, 1)
    crit = stats.chi2.isf(.05, 1)
    fig = plt.figure(figsize=(15, 6.4))
    fig.text(.035, .925, 'Same proportions, more households: the test sharpens, V stays put',
             fontsize=24, weight='bold')
    fig.text(.035, .87, 'Table B scaled to n = 20 (7, 3 / 3, 7), 100 (35, 15 / 15, 35) and 1000 '
             '(350, 150 / 150, 350). Cell proportions never change.', fontsize=15, color=MUTED)
    gap = .025; w = (1 - 2 * .035 - 2 * gap) / 3
    marks = [20, 100, 1000]
    specs = [('χ² grows in proportion to n', 'χ²'),
             ('p-value collapses toward 0', 'p-value (log scale)'),
             ("Cramér's V does not move", "Cramér's V")]
    for k, (title, ylabel) in enumerate(specs):
        x0 = .035 + k * (w + gap)
        card(fig, x0, .08, w, .72)
        fig.text(x0 + .018, .745, title, fontsize=17, weight='bold')
        ax = fig.add_axes([x0 + .065, .2, w - .09, .47])
        ax.set_xscale('log'); ax.set_xlim(10, 3000)
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        ax.grid(True, which='major', color='#e8edf3', lw=.8); ax.set_axisbelow(True)
        ax.set_xlabel('sample size n (log scale)', fontsize=12.5, color=INK)
        ax.set_ylabel(ylabel, fontsize=12.5, color=INK)
        ax.set_xticks([10, 20, 100, 1000, 3000]); ax.set_xticklabels(['10', '20', '100', '1000', '3000'])
        if k == 0:
            ax.set_yscale('log'); ax.set_ylim(1, 1000)
            ax.plot(ns, x2, color=INK, lw=2)
            ax.axhline(crit, color=NEG, lw=1.6, ls=(0, (5, 4)))
            ax.text(2800, crit * 1.18, f'5% critical value {crit:.2f}', color=INK, fontsize=11.5, ha='right')
            ys = [checks['scaled'][str(m)]['X2'] for m in marks]
            labels = ['3.2', '16', '160']
            ax.set_yticks([1, 10, 100, 1000]); ax.set_yticklabels(['1', '10', '100', '1000'])
        elif k == 1:
            ax.set_yscale('log'); ax.set_ylim(1e-40, 1)
            ax.plot(ns, p, color=INK, lw=2)
            ax.axhline(.05, color=NEG, lw=1.6, ls=(0, (5, 4)))
            ax.text(2800, .05 * 30, 'p = 0.05', color=INK, fontsize=11.5, ha='right')
            ys = [checks['scaled'][str(m)]['p'] for m in marks]
            labels = ['0.074', '6×10⁻⁵', '10⁻³⁶']
            ax.set_yticks([1, 1e-10, 1e-20, 1e-30, 1e-40])
            ax.set_yticklabels(['1', '10⁻¹⁰', '10⁻²⁰', '10⁻³⁰', '10⁻⁴⁰'])
        else:
            ax.set_ylim(0, 1)
            ax.plot(ns, np.full_like(ns, .4), color=INK, lw=2)
            ys = [checks['scaled'][str(m)]['V'] for m in marks]
            labels = ['0.40', '0.40', '0.40']
        for m, yv, lab in zip(marks, ys, labels):
            ax.scatter([m], [yv], s=70, color=POS, edgecolor=CARD, linewidth=2, zorder=5)
            if k == 2:
                off, ha = (0, 12), 'center'
            elif m == 20:
                off, ha = (2 if k == 1 else 9, -42 if k == 1 else -16), 'left'
            elif k == 0:
                off, ha = (-9, 6), 'right'
            else:
                off, ha = (9, 4), 'left'
            ax.annotate(f'n={m}: {lab}', (m, yv), textcoords='offset points', xytext=off,
                        ha=ha, fontsize=11.5, color=INK)
    fig.text(.035, .025, 'Curves treat n as continuous with fixed cell proportions 0.35, 0.15 / 0.15, 0.35; '
             'dots are the three integer toy tables. Uncorrected Pearson χ², df = 1.',
             fontsize=12, color=MUTED)
    return fig

def save(fig, stem):
    fig.savefig(OUT / f'{stem}.svg')
    fig.savefig(OUT / f'{stem}.png', dpi=100)
    plt.close(fig)

if __name__ == '__main__':
    save(figure_three_tables(), '01-three-tables')
    save(figure_scaling(), '02-same-strength-more-data')
    (OUT / 'checks.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in v.items()
                          if kk in ('X2', 'p', 'V', 'phi', 'odds_ratio', 'sqrt_X2_over_n')}
                      for k, v in {**checks['tables'], **{'n=' + a: b for a, b in checks['scaled'].items()}}.items()},
                     indent=1, ensure_ascii=False))
    print('identities', checks['identities'])
    print('bias', json.dumps(bias))
    print('max error vs scipy/hand', max_err)
