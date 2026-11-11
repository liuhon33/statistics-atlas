"""Build two offline explorers, static figures, and independent SciPy references.

Run with Python + numpy, scipy, matplotlib; then run `node check_math.cjs`.
"""
from pathlib import Path
import importlib.util
import json
import xml.etree.ElementTree as ET
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, ncx2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[2]
BUILDER = VAULT / '.agents/skills/animate-geometry/scripts/build_explorer.py'
spec = importlib.util.spec_from_file_location('explorer_builder', BUILDER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
C = dict(blue='#3975b7', orange='#cd7134', green='#16866c', purple='#8060b5')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelcolor': '#344640', 'text.color': '#344640',
                     'svg.hashsalt': 'ci-delta-20261111'})


def pack(name, title):
    parts = [HERE / f'{name}-body.html', HERE / 'explorer.css',
             HERE / 'math.js', HERE / 'plot.js', HERE / f'{name}.js']
    read = lambda p: p.read_text(encoding='utf-8-sig')
    content = builder.compile_html(title, read(parts[0]), [read(parts[1])],
                                   list(map(read, parts[2:])))
    builder.write_artifact(HERE / f'{name}-explorer.html', content,
                           [*parts, Path(__file__), BUILDER])


def style(ax):
    ax.grid(alpha=.18)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(HERE / f'{name}.svg', metadata={'Date': None}, facecolor='white')
    fig.savefig(HERE / f'{name}.png', dpi=145, facecolor='white')
    ET.parse(HERE / f'{name}.svg')
    plt.close(fig)


def ci_static():
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), layout='constrained')
    alpha, h = .05, .1 * norm.ppf(.975)
    for row, kind in enumerate(['normal', 'scale']):
        ax, pv = axes[row]
        if kind == 'normal':
            domain, x, b = (-.55, .55), .2, 0.
            grid = np.linspace(*domain, 700)
            lower, upper = grid-h, grid+h
            interval, acceptance = (x-h, x+h), (b-h, b+h)
            p = 2*norm.cdf(-np.abs(x-grid)/.1)
            p_here = 2*norm.cdf(-abs(x-b)/.1)
            title = 'Normal location: equal slice lengths'
        else:
            domain, x, b = (0, 2.2), 1., 1.
            grid = np.linspace(*domain, 700)
            L, U = .5+alpha/2, 1.5-alpha/2
            lower, upper = L*grid, U*grid
            interval, acceptance = (x/U, x/L), (L*b, U*b)
            f = np.clip(x/np.maximum(grid, 1e-30)-.5, 0, 1)
            p, p_here = 2*np.minimum(f, 1-f), 1.
            title = 'Uniform scale: unequal slice lengths'
        ax.fill_between(grid, lower, upper, color=C['blue'], alpha=.09)
        ax.plot(grid, lower, color=C['blue'], lw=1)
        ax.plot(grid, upper, color=C['blue'], lw=1)
        ax.axvline(b, color=C['blue'], ls=':', lw=1)
        ax.axhline(x, color=C['orange'], ls=':', lw=1)
        ax.plot([b, b], acceptance, color=C['blue'], lw=4, label='fix b: data slice')
        ax.plot(interval, [x, x], color=C['orange'], lw=4, label='fix x: CI')
        ax.scatter([b], [x], c=C['green'] if p_here >= alpha else '#b64f56', s=34, zorder=4)
        ax.set(xlim=domain, ylim=domain, xlabel='candidate parameter b',
               ylabel='possible observation x', title=title, aspect='equal')
        ax.legend(fontsize=8, loc='upper left')
        pv.plot(grid, p, c=C['green'], lw=2, label='p-value as b varies')
        pv.axhline(alpha, c=C['orange'], ls=':', label='α = 0.05')
        pv.plot(interval, [alpha, alpha], color=C['orange'], lw=4)
        pv.axvline(b, color=C['blue'], ls=':')
        pv.scatter([b], [p_here], c=C['green'] if p_here >= alpha else '#b64f56', s=34)
        pv.set(xlim=domain, ylim=(-.035, 1.1), xlabel='candidate parameter b',
               ylabel='p-value', title=f'Fix x = {x:g}: retain b where p(b) ≥ α')
        pv.text(.03, .93, f'CI = [{interval[0]:.4f}, {interval[1]:.4f}]\n'
                f'vertical length {acceptance[1]-acceptance[0]:.4f}\n'
                f'horizontal length {interval[1]-interval[0]:.4f}',
                transform=pv.transAxes, va='top', fontsize=9)
        style(ax)
        style(pv)
    fig.suptitle('Test inversion: one decision region, two slices', fontsize=16)
    save(fig, 'ci-overview')


def exact_cdf(v, mu, n, a):
    r = mu*mu + np.asarray(v)/a
    return ncx2.cdf(np.maximum(n*r, 0), df=1, nc=n*mu*mu)


def delta_static():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6), layout='constrained')
    x = np.linspace(-5.5, 7, 900)
    ax = axes[0]
    ax.plot(x, exact_cdf(x, 1, 25, 5), c=C['green'], lw=2, label='exact, n = 25')
    ax.plot(x, norm.cdf(x/2), c=C['blue'], ls='--', lw=2, label='first order: N(0, 4)')
    ax.set(title='μ = 1: linear term dominates', xlabel=r'$\sqrt{n}(\bar X^2-\mu^2)$')
    share = (4/25)/(4/25+2/25**2)
    ax.text(.03, .70, f'Linear variance share:\n{100*share:.1f}%',
            transform=ax.transAxes, fontsize=9)
    ax = axes[1]
    x = np.linspace(-.2, 4, 900)
    for n, color in [(5, C['purple']), (25, C['orange']), (500, C['green'])]:
        ax.plot(x, exact_cdf(x, 0, n, np.sqrt(n)), c=color, lw=2, label=f'exact, n = {n}')
    ax.plot([-.2, 0, 0, 4], [0, 0, 1, 1], c=C['blue'], ls='--', label='first order: mass at 0')
    ax.set(title='μ = 0: √n error collapses to 0', xlabel=r'$\sqrt{n}\,\bar X^2$')
    ax = axes[2]
    x = np.linspace(-.4, 8, 900)
    ax.plot(x, exact_cdf(x, 0, 25, 25), c=C['green'], lw=2, label='exact for every n: χ²₁')
    ax.plot([-.4, 0, 0, 8], [0, 0, 1, 1], c=C['blue'], ls='--', label='first order: mass at 0')
    ax.set(title='μ = 0: n scale preserves variation', xlabel=r'$n\,\bar X^2$')
    for ax in axes:
        ax.set(ylim=(-.03, 1.05), ylabel='cumulative probability')
        ax.legend(loc='lower right', fontsize=8)
        style(ax)
    fig.suptitle('Squaring a normal sample mean: exact distributions versus the delta approximation', fontsize=14)
    save(fig, 'delta-overview')


def references():
    cdf_rows = [[float(x), float(norm.cdf(x))] for x in np.linspace(-8, 8, 801)]
    probs = [.005, .01, .025, .05, .1, .25, .5, .75, .9, .95, .975, .99, .995]
    q_rows = [[p, float(norm.ppf(p))] for p in probs]
    delta_rows, moment_errors = [], []
    for mu in [-1.5, -.3, 0., .05, .8, 1.5]:
        for n in [1, 5, 25, 100, 500]:
            mean = quad(lambda z: ((mu+z/np.sqrt(n))**2-mu*mu)*norm.pdf(z), -10, 10)[0]
            var = quad(lambda z: (((mu+z/np.sqrt(n))**2-mu*mu)-1/n)**2*norm.pdf(z), -10, 10)[0]
            moment_errors += [abs(mean-1/n), abs(var-(4*mu*mu/n+2/n**2))]
            for mode, a in [('raw', 1), ('sqrt', np.sqrt(n)), ('n', n)]:
                rows = []
                for p in [.001, .01, .1, .5, .9, .99, .999]:
                    v = a*(ncx2.ppf(p, 1, n*mu*mu)/n-mu*mu)
                    rows.append([float(v), float(exact_cdf(v, mu, n, a))])
                delta_rows.append({'mu': mu, 'n': n, 'mode': mode, 'points': rows})
    assert max(moment_errors) < 1e-11
    record = {'normal_cdf': cdf_rows, 'normal_quantiles': q_rows,
              'delta_cdf': delta_rows,
              'scipy_checks': {'moment_cases': 30, 'max_moment_error': max(moment_errors),
                               'method': 'Full Gaussian moments by quadrature; exact CDF via independent noncentral chi-square distribution.'}}
    (HERE / 'reference-values.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    pack('ci', 'Confidence intervals and tests — three linked views')
    pack('delta', 'Delta method — local slope, curvature and distribution')
    ci_static()
    delta_static()
    references()
    print('Built two offline HTML figures, SVG/PNG fallbacks and independent SciPy reference values.')
