"""Rebuild the offline explorer and static overview. Python: numpy, matplotlib.

Example: python build.py --node <absolute-path-to-node.exe>
The source lecture PDF is not needed; no source screenshots are modified.
Original reconstruction inspired by Thibault Randrianarisoa, University of
Toronto, EM algorithm (2026-02-25), slide 13; not recovered lecture data/code.

math.js holds pure equations and the fixed LCG/Box-Muller seed 20261113.
export_states.cjs tests 36 initializations for 60 iterations. verify_math.py
checks the exported states independently with SciPy/NumPy and enumerates all
eight latent assignments for a three-point example. The delivered HTML has
no external libraries, fonts, servers, accounts or network dependencies.

Ordinary full-covariance ML updates, no added regularizer. Near-empty counts
(below 1e-7) or covariance eigenvalues (at/below 1e-7) stop rather than clip.
Playback stops at a relative likelihood gain of 1e-8 or 60 M-steps; neither
certifies a global optimum. E recolors points; M uses these frozen colors.

The source PDF is private/Git-ignored; selected screenshots stay publishable.
The separate full-slide-13 render was made with pypdfium2: zero-based page 12,
scale 2.8, no cropping. This builder never regenerates or modifies raw assets.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'em-gmm-mpl'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--node', default=shutil.which('node'))
    args = parser.parse_args()
    if not args.node:
        raise RuntimeError('Supply an absolute Node executable with --node.')
    node = str(Path(args.node).resolve())
    result = subprocess.run([node, str(HERE / 'export_states.cjs')], check=True, capture_output=True, text=True, encoding='utf-8')
    record = json.loads(result.stdout)
    (HERE / 'model-states.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    helper = ROOT / '.agents/skills/animate-geometry/scripts/build_explorer.py'
    spec = importlib.util.spec_from_file_location('explorer_builder', helper)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    files = [HERE / n for n in ['body.html', 'explorer.css', 'math.js', 'explorer.js']]
    text = [p.read_text(encoding='utf-8') for p in files]
    html = builder.compile_html('EM playground — two Gaussian components', text[0], [text[1]], text[2:])
    builder.write_artifact(HERE / 'explorer.html', html, files)
    plt.rcParams.update({'svg.hashsalt': 'em-gmm-20261113', 'font.family': 'DejaVu Sans', 'font.size': 11})
    fig, axs = plt.subplots(2, 2, figsize=(10, 10.8), facecolor='#111829')
    colors = np.array([[59,108,239],[239,91,82]]) / 255
    xs = np.asarray(record['data'])
    for ax, snap in zip(axs.flat, record['snapshots']):
        ax.set_facecolor('#1c263b')
        r = np.asarray(snap['r']) if snap['r'] else None
        cs = r @ colors if r is not None else '#73cf9b'
        ax.scatter(xs[:,0], xs[:,1], c=cs, s=11, alpha=.85, zorder=2)
        for k in range(2):
            mu = np.asarray(snap['p']['means'][k]); cov = np.asarray(snap['p']['covs'][k])
            t = np.linspace(0, 2*np.pi, 201); circle = np.array([np.cos(t),np.sin(t)])
            for radius in [1,2]:
                curve = mu[:,None] + radius*np.linalg.cholesky(cov)@circle
                ax.plot(*curve, c=colors[k], lw=2, ls='-' if radius==1 else '--')
            ax.plot(*mu, marker='+', markersize=13, color='white', mew=3)
            ax.plot(*mu, marker='+', markersize=11, color=colors[k], mew=2)
        ax.set(xlim=(-3.5,3.5),ylim=(-3.5,3.5),aspect='equal',xlabel='Observed feature x₁',ylabel='Observed feature x₂')
        ax.set_title(snap['label']+'\n'+f"log-likelihood = {snap['logLikelihood']:.2f}",color='#eef2fb',pad=10)
        ax.tick_params(colors='#b6c4dc');ax.xaxis.label.set_color('#b6c4dc');ax.yaxis.label.set_color('#b6c4dc')
        ax.grid(alpha=.13); ax.set_axisbelow(True)
        for spine in ax.spines.values():spine.set_color('#536886')
    fig.suptitle('Same data. Different responsibilities and fitted Gaussians.',color='#eef2fb',fontsize=17,y=.98)
    fig.text(.5,.025,'Original seeded example, inspired by Lecture 7 slide 13. Points never move.\nBlue/red = posterior weights; crosses = means; contours = Mahalanobis radii 1 and 2.\nAfter M, colors remain those used for that M-step until the next E-step.',ha='center',color='#b6c4dc',fontsize=10)
    fig.subplots_adjust(top=.91,bottom=.12,hspace=.34,wspace=.25)
    fig.savefig(HERE / 'overview.svg',metadata={'Date':None})
    fig.savefig(HERE / 'overview.png',dpi=140,metadata={'Software':'Matplotlib; original EM reconstruction'})
    plt.close(fig)
    print(json.dumps({'output':'explorer.html','static':'overview.svg','observations':len(xs),'jsChecks':record['jsChecks'],'stoppedRuns':sum(r['stop'] is not None for r in record['runs'])},indent=2))


if __name__ == '__main__':
    main()
