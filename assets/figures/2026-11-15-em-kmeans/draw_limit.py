"""Original 1-D EM-to-K-means figure; no lecture data or artwork is copied.

Run this script with Python + NumPy, SciPy and Matplotlib. It writes outputs
beside itself. Only epsilon changes: means, weights, x-axis and y-axis stay
fixed. Numeric checks support the separate analytic small-variance proof.
"""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import expit
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
MEANS = np.array([-1.0, 1.0])
WEIGHTS = np.array([0.5, 0.5])
EPSILONS = [1.0, 0.25, 0.1, 0.05, 0.01]
EXAMPLE = -0.2
X = np.linspace(-2.2, 2.2, 2201)


def responsibilities(points, epsilon, weights=WEIGHTS):
    points = np.atleast_1d(points).astype(float)
    logs = np.log(weights)[None, :] - (points[:, None] - MEANS)**2 / (2*epsilon)
    scores = np.exp(logs-logs.max(axis=1, keepdims=True))
    return scores/scores.sum(axis=1, keepdims=True)


def check_math():
    normalization_error = direct_error = closed_form_error = 0.0
    table = []
    for epsilon in EPSILONS:
        r = responsibilities(X, epsilon)
        normalization_error = max(normalization_error, float(np.max(np.abs(r.sum(axis=1)-1))))
        direct = WEIGHTS * norm.pdf(X[:, None], loc=MEANS, scale=np.sqrt(epsilon))
        direct /= direct.sum(axis=1, keepdims=True)
        direct_error = max(direct_error, float(np.max(np.abs(r-direct))))
        closed_form_error = max(closed_form_error, float(np.max(np.abs(r[:, 0]-expit(-2*X/epsilon)))))
        assert np.all((r >= 0) & (r <= 1))
        assert np.all(np.diff(r[:, 0]) <= 1e-14)
        assert np.allclose(responsibilities([0], epsilon), [[0.5, 0.5]], atol=1e-14)
        assert np.allclose(responsibilities([0], epsilon, np.array([0.3, 0.7])), [[0.3, 0.7]], atol=1e-14)
        sample = responsibilities([EXAMPLE], epsilon)[0]
        # Keep the tiny losing responsibility: 1-r1 would round it to zero.
        table.append({'epsilon': epsilon, 'standard_deviation': float(np.sqrt(epsilon)),
                      'r1_float': float(sample[0]), 'r2': float(sample[1])})
    assert max(normalization_error, direct_error, closed_form_error) < 1e-12
    assert all(table[i]['r2'] > table[i+1]['r2'] for i in range(len(table)-1))
    assert 0 < table[-1]['r2'] < 5e-18
    probe = np.array([-1.7, -0.2, 0.2, 1.7])
    hard = np.column_stack((probe < 0, probe > 0)).astype(float)
    limit_error = float(np.max(np.abs(responsibilities(probe, 0.001)-hard)))
    assert limit_error < 1e-12
    points = np.array([-1.8, -1.2, -0.7, -0.2, 0.2, 0.7, 1.2, 1.8])
    soft = responsibilities(points, 0.001)
    soft_means = (soft.T @ points)/soft.sum(axis=0)
    hard_means = np.array([points[points < 0].mean(), points[points > 0].mean()])
    mean_error = float(np.max(np.abs(soft_means-hard_means)))
    assert mean_error < 1e-12
    q_error = 0.0
    candidate_means = np.array([-1.1, 0.9])
    for epsilon in EPSILONS:
        frozen_r = responsibilities(points, epsilon)
        log_joint = np.log(WEIGHTS) + norm.logpdf(points[:, None], loc=candidate_means, scale=np.sqrt(epsilon))
        direct_q = float((frozen_r*log_joint).sum())
        constant = -len(points)*np.log(2)-len(points)/2*np.log(2*np.pi*epsilon)
        expanded_q = constant - np.sum(frozen_r*(points[:, None]-candidate_means)**2)/(2*epsilon)
        q_error = max(q_error, abs(direct_q-expanded_q))
    assert q_error < 1e-10
    data = {'means': MEANS.tolist(), 'weights': WEIGHTS.tolist(),
            'x_range': [float(X[0]), float(X[-1])], 'grid_points': len(X),
            'example_point': EXAMPLE, 'squared_distances': [0.64, 1.44],
            'table': table, 'ties': 'x=0 stays (0.5,0.5) for every positive epsilon',
            'float_caveat': 'At epsilon=0.01 r1 rounds to 1 in float64, but r2 is positive; use r1=1-r2.'}
    (HERE/'example-values.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    return {'passed': True, 'grid_checks': len(X)*len(EPSILONS),
            'max_normalization_error': normalization_error,
            'max_direct_normal_pdf_error': direct_error,
            'max_closed_form_error': closed_form_error,
            'small_variance_hard_assignment_error': limit_error,
            'weighted_to_hard_mean_error': mean_error,
            'max_Q_coefficient_check_error': float(q_error),
            'tie_equal_and_unequal_weights': 'passed',
            'limits': 'Fixed centers and positive fixed weights; unique-nearest limit excludes ties. Static generated figure, not live Obsidian.'}


def draw():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'em-kmeans-20261115',
                         'axes.spines.top': False, 'axes.spines.right': False})
    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    fig.subplots_adjust(left=0.10, right=0.97, top=0.79, bottom=0.25)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.axvspan(-2.2, 0, color='#dbeafe', alpha=0.5)
    ax.axvspan(0, 2.2, color='#fee2e2', alpha=0.45)
    colors = ['#93c5fd', '#3b82f6', '#2563eb', '#172554']
    shown = [1.0, 0.25, 0.1, 0.01]
    for e, color in zip(shown, colors):
        ax.plot(X, responsibilities(X, e)[:, 0], color=color, lw=2.5,
                label=rf'GMM: $\epsilon={e:g}$', zorder=3)
    ax.plot([-2.2, 0], [1, 1], color='#111827', ls='--', lw=2,
            label='K-means: hard assignment', zorder=4)
    ax.plot([0, 2.2], [0, 0], color='#111827', ls='--', lw=2, zorder=4)
    ax.scatter([0, 0], [0, 1], facecolors='white', edgecolors='#111827', s=46, zorder=7)
    ax.axvline(0, color='#64748b', ls=':', lw=1.1, zorder=1)
    ax.axvline(EXAMPLE, color='#475569', ls=':', lw=1.3, zorder=1)
    ax.scatter([0], [0.5], c='#9333ea', marker='D', s=55, zorder=8)
    ax.annotate('Exact tie: GMM stays 0.5\nK-means must break the tie',
                xy=(0, 0.5), xytext=(0.63, 0.58), fontsize=11,
                color='#6b21a8', va='center',
                arrowprops={'arrowstyle': '->', 'color': '#9333ea', 'lw': 1.2})
    ax.text(-1.0, 1.10, r'Center 1: $\mu_1=-1$', ha='center', color='#1d4ed8', fontsize=12)
    ax.text(1.0, 1.10, r'Center 2: $\mu_2=1$', ha='center', color='#b91c1c', fontsize=12)
    ax.text(EXAMPLE-0.06, 0.17, 'Example x = -0.2', rotation=90, va='bottom',
            ha='right', fontsize=10, color='#475569')
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-0.06, 1.04)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlabel('Observed position x (centers stay fixed)', labelpad=9)
    ax.set_ylabel(r'Responsibility for component 1, $r_1(x;\epsilon)$', labelpad=10)
    ax.grid(axis='y', color='#cbd5e1', alpha=0.5, lw=0.7)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.23), ncol=3,
              frameon=False, fontsize=10.5, handlelength=2.8, columnspacing=1.3)
    fig.suptitle('Soft GMM memberships approach hard K-means assignments',
                 fontsize=17, fontweight='bold', y=0.975, color='#0f172a')
    fig.text(0.5, 0.918, r'Shared covariance $\Sigma_k=\epsilon I$; equal weights. Same boundary at $x=0$, different softness.',
             ha='center', fontsize=12, color='#334155')
    fig.text(0.5, 0.025, r'Only $\epsilon$ changes. For any finite $\epsilon>0$, probabilities are not exactly 0 or 1; $r_2=1-r_1$.',
             ha='center', fontsize=10.5, color='#475569')
    fig.savefig(HERE/'responsibility-limit.svg', metadata={'Date': None})
    fig.savefig(HERE/'responsibility-limit.png', dpi=155)
    plt.close(fig)


if __name__ == '__main__':
    checks = check_math()
    draw()
    ET.parse(HERE/'responsibility-limit.svg')
    checks['svg_xml'] = 'passed'
    checks['sha256'] = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                        for name in ['draw_limit.py', 'example-values.json', 'responsibility-limit.svg', 'responsibility-limit.png']}
    (HERE/'checks.json').write_text(json.dumps(checks, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(checks, indent=2))
