"""Original illustrative comparison, not lecture data.
Run: D:/anaconda/python.exe <absolute path to this script>
Requires NumPy and Matplotlib. Outputs are beside this script.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

OUT = Path(__file__).resolve().parent
t = np.arange(101)
beta, x0, seed = 0.1, 4.0, 1126
alpha = 1-beta
noise = np.random.default_rng(seed).standard_normal((100, 3))
walk = np.full((101, 3), x0)
diff = walk.copy()
for k in range(1, 101):
    walk[k] = walk[k-1] + np.sqrt(beta)*noise[k-1]
    diff[k] = np.sqrt(alpha)*diff[k-1] + np.sqrt(beta)*noise[k-1]
means = [np.full(101, x0), x0*alpha**(t/2)]
variances = [beta*t, 1-alpha**t]
v = 0.
errors = []
for k in range(1, 101):
    v = alpha*v+beta
    errors.append(abs(v-variances[1][k]))
assert max(errors) < 1e-13
assert np.allclose(np.diff(walk, axis=0), np.sqrt(beta)*noise)
assert np.allclose(diff[1:]-np.sqrt(alpha)*diff[:-1], np.sqrt(beta)*noise)
assert np.isclose(variances[0][-1], 10)
assert 0 < variances[1][-1] < 1

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'svg.fonttype': 'none', 'axes.spines.top': False,
                     'axes.spines.right': False})
fig = plt.figure(figsize=(12, 8.5), facecolor='#fafbfe')
gs = fig.add_gridspec(2, 2, height_ratios=[1.45, 1],
                      left=.075, right=.97, top=.76, bottom=.17,
                      hspace=.48, wspace=.18)
colors = ['#c86a20', '#167d9a']
titles = ['Random walk: add noise only', 'Diffusion: shrink, then add noise']
equations = [r'$x_t=x_{t-1}+\sqrt{0.1}\,\xi_t$',
             r'$x_t=\sqrt{0.9}\,x_{t-1}+\sqrt{0.1}\,\xi_t$']
for j in range(2):
    ax = fig.add_subplot(gs[0, j])
    ax.set_facecolor('#ffffff')
    m, v = means[j], variances[j]
    ax.fill_between(t, m-2*np.sqrt(v), m+2*np.sqrt(v),
                    color=colors[j], alpha=.16, linewidth=0)
    ax.plot(t, [walk, diff][j], color=colors[j], alpha=.35, lw=.9)
    ax.plot(t, m, color=colors[j], lw=3)
    ax.axhline(0, color='#536174', lw=.8, ls='--')
    ax.set(xlim=(0,100), ylim=(-4,11), xlabel='Forward step t',
           title=titles[j]+'\n'+equations[j])
    ax.set_yticks([-4,0,4,8])
    ax.grid(alpha=.12)
    if j == 0:
        ax.set_ylabel('One coordinate of the noisy state')
    ax.text(.035, .94, ['Mean stays at 4', 'Mean approaches 0'][j],
            transform=ax.transAxes, va='top', color=colors[j], weight='bold')

ax = fig.add_subplot(gs[1, :])
ax.set_facecolor('#ffffff')
ax.plot(t, variances[0], color=colors[0], lw=3,
        label=r'Random walk: $v_t=0.1t$')
ax.plot(t, variances[1], color=colors[1], lw=3,
        label=r'Diffusion: $v_t=1-0.9^t$')
ax.axhline(1, color='#536174', lw=.8, ls='--')
ax.set(xlim=(0,100), ylim=(0,11), xlabel='Forward step t',
       ylabel='Conditional variance', title='Spread across repeated runs from the same starting value')
ax.text(99, 10.25, '10 at step 100; keeps growing', color=colors[0], ha='right')
ax.text(99, 1.5, 'Levels off at 1, not 0', color=colors[1], ha='right')
ax.legend(loc='upper left', frameon=False)
ax.grid(alpha=.12)
fig.suptitle('Adding noise is not the same as an ever-spreading random walk',
             x=.52, y=.975, fontsize=17, weight='bold')
fig.text(.52, .926, r'Fixed start $x_0=4$  |  Constant $\beta=0.1$  |  Same noise draws in both panels',
         ha='center', color='#42516a', fontsize=12)
fig.legend(handles=[Line2D([0],[0],color='#42516a',lw=3,label='Exact conditional mean'),
                    Patch(facecolor='#a8b5c9',alpha=.4,label='Mean ± 2 standard deviations'),
                    Line2D([0],[0],color='#8291a8',lw=1,label='3 illustrative sample paths')],
           loc='upper center', bbox_to_anchor=(.52,.9), ncol=3, frameon=False, fontsize=10)
fig.text(.075,.046,'Shading covers about 95% at each fixed step; it is not a boundary for whole paths.\n'
         'Both top panels use identical scales. Zero mean does not mean zero samples.',
         fontsize=10, color='#42516a')
stem = OUT/'random-walk-vs-diffusion'
fig.savefig(stem.with_suffix('.svg'), facecolor=fig.get_facecolor())
fig.savefig(stem.with_suffix('.png'), dpi=130, facecolor=fig.get_facecolor())
plt.close(fig)
ET.parse(stem.with_suffix('.svg'))
np.savez(OUT/'random-walk-comparison-data.npz', t=t, noise=noise,
         random_walk=walk, diffusion=diff, means=np.array(means),
         variances=np.array(variances))
report = {'seed':seed, 'beta':beta, 'x0':x0, 'steps':100,
          'diffusion_mean_at_100':float(means[1][-1]),
          'random_walk_variance_at_100':float(variances[0][-1]),
          'diffusion_variance_at_100':float(variances[1][-1]),
          'maximum_variance_recursion_error':float(max(errors)),
          'svg_xml_parse':'PASS', 'paired_noise_checks':'PASS',
          'scope':'Exact conditional moments and three illustrative paths; not empirical proof.'}
(OUT/'random-walk-comparison-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
