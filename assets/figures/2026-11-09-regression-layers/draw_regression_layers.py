"""Original illustrations for the three-level Linear regression backbone.

Run: python -X utf8 assets/figures/2026-11-09-regression-layers/draw_regression_layers.py
Requires numpy, matplotlib, scipy, Pillow. All measurements are constructed.
Figures 1--3 revisit the SAME five observations; figure 4 is a separate
population counterexample. No existing assets are modified.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Arc, Polygon
from PIL import Image
from scipy.stats import t, f

OUT = Path(__file__).resolve().parent
BLUE, ORANGE, INK, TEAL, MUTED = '#2268ad', '#ce771a', '#26384b', '#248677', '#6c7d8e'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelcolor': INK, 'text.color': INK,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'regression-three-levels'})
x = np.array([150., 160., 170., 180., 190.])
y = np.array([47., 49., 60., 65., 79.])
n = len(x)
xc, yc = x - x.mean(), y - y.mean()
X = np.column_stack([np.ones(n), xc])
coef = np.linalg.lstsq(X, y, rcond=None)[0]
yhat = X @ coef
e = y - yhat
g = yhat - y.mean()
Sxx, Sxy = xc @ xc, xc @ yc
sse, sst, gain = e @ e, yc @ yc, g @ g
nu = n - 2
Fvalue = gain / (sse / nu)
tvalue = coef[1] / np.sqrt((sse / nu) / Sxx)
gl, el = np.linalg.norm(g), np.linalg.norm(e)
phi = np.arctan2(el, gl)
critical = t.ppf(.975, nu)

def save(fig, name):
    fig.savefig(OUT / f'{name}.svg', metadata={'Date': None}, bbox_inches='tight')
    fig.savefig(OUT / f'{name}.png', dpi=145, bbox_inches='tight')
    plt.close(fig)

def arrow(ax, start, end, color, lw=2.8):
    ax.annotate('', xy=end, xytext=start,
                arrowprops={'arrowstyle': '->', 'color': color, 'lw': lw})

def intro_scene(ax, k):
    ax.clear()
    ax.set(xlim=(145, 195), ylim=(39, 85), xlabel='Height (cm)', ylabel='Weight (kg)')
    ax.grid(alpha=.13)
    ax.scatter(x, y, c=INK, s=55, zorder=5, label='Five invented observations')
    line_alpha = np.clip((k-7)/11, 0, 1)
    if line_alpha > 0:
        xx = np.linspace(148, 192, 100)
        ax.plot(xx, 60 + .8*(xx-170), c=BLUE, lw=2.7, alpha=line_alpha)
        ax.text(148, 82, 'Fitted line: predicted weight = 60 + 0.8 (height - 170)',
                color=BLUE, fontsize=10, alpha=line_alpha)
    if k >= 22:
        fraction = min((k-22)/12, 1)
        ax.plot([175, 175], [40, 40+24*fraction], c=TEAL, ls='--', lw=2)
        ax.text(175, 37.1, '175', ha='center', color=TEAL, weight='bold')
    if k >= 35:
        fraction = min((k-35)/12, 1)
        ax.plot([175-30*fraction, 175], [64, 64], c=TEAL, ls='--', lw=2)
        ax.scatter([175], [64], c=TEAL, s=85, zorder=6)
        ax.annotate('Predicted: 64 kg', (175, 64), (177, 58), color=TEAL,
                    arrowprops={'arrowstyle': '-', 'color': TEAL}, fontsize=11)
    phase = ('1. Record paired measurements' if k < 8 else
             '2. Fit a line to the observed trend' if k < 22 else
             '3. Enter height: 175 cm' if k < 35 else
             '4. Read the prediction: 64 kg')
    ax.set_title(phase, fontsize=16, loc='left', pad=16, weight='bold')

def intro():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.subplots_adjust(left=.11, right=.97, bottom=.16, top=.85)
    fig.text(.11, .025, 'Original illustrative data, not a population weight formula. '
             'Dots stay fixed; green guides show how to use the line.', fontsize=9, color=MUTED)
    intro_scene(ax, 59)
    fig.savefig(OUT/'01-predict-weight.svg', metadata={'Date': None})
    fig.savefig(OUT/'01-predict-weight.png', dpi=145)
    ani = FuncAnimation(fig, lambda k: intro_scene(ax, k), frames=64, interval=110)
    ani.save(OUT/'01-predict-weight.gif', writer=PillowWriter(fps=9), dpi=100)
    plt.close(fig)

def mechanics():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.6, 4.9), gridspec_kw={'width_ratios':[1,1.18]})
    fig.subplots_adjust(left=.08, right=.98, bottom=.29, top=.77, wspace=.30)
    fig.suptitle('One fitted line, two explanations', fontsize=18, weight='bold', y=.97)
    slopes = np.linspace(.3, 1.3, 240)
    a.plot(slopes, sse + Sxx*(slopes-.8)**2, c=BLUE, lw=2.6)
    a.scatter([.8], [sse], c=TEAL, s=65, zorder=5)
    a.annotate('Minimum: b = 0.8\nSSE = 36', (.8, sse), (.48, 100),
               arrowprops={'arrowstyle':'-', 'color':TEAL}, color=TEAL, fontsize=10)
    a.set(xlabel='Candidate slope b (kg per cm)', ylabel='Squared residuals, SSE (kg²)', ylim=(0,310))
    a.set_title('Calculus: minimize the loss', fontsize=12, pad=10)
    a.grid(alpha=.15)
    fig.text(.27, .105, 'Each candidate line passes through (170, 60).\n'
             r'$S(b)=36+1000(b-0.8)^2$', ha='center', fontsize=10)
    b.set(xlim=(-2, 35), ylim=(-6, 17), aspect='equal')
    b.axis('off')
    b.set_title('Geometry: the residual is perpendicular', fontsize=12, pad=10)
    b.plot([-1, 33], [0,0], c=MUTED, alpha=.5)
    arrow(b, (0,0), (gl,0), BLUE)
    arrow(b, (gl,0), (gl,el), ORANGE)
    arrow(b, (0,0), (gl,el), INK)
    b.plot([gl-1, gl-1, gl], [0,1,1], c=INK, lw=1.2)
    b.text(gl*.45, -2.3, r'$g=\hat y-\bar y\mathbf{1}$', ha='center', color=BLUE)
    b.text(gl+1.4, el/2, r'$e=y-\hat y$'+'\nlength = 6', va='center', color=ORANGE, fontsize=10)
    b.text(gl*.38, el*.65+1, r'$y_c=y-\bar y\mathbf{1}$', color=INK)
    b.text(0, 13.1, 'Each arrow represents all FIVE observations.', fontsize=10, color=MUTED)
    b.text(0, 10.4, 'The fitted part follows the centered-height direction.', fontsize=9.5, color=MUTED)
    fig.text(.08,.015,'Original illustration. Right: orthonormal coordinates in the plane of g and e; '
             'equal scales preserve the right angle and lengths.', fontsize=9, color=MUTED)
    save(fig, '02-loss-and-projection')

def inference():
    fig, (a,b) = plt.subplots(1,2,figsize=(10.7,4.9))
    fig.subplots_adjust(left=.06,right=.97,top=.80,bottom=.23,wspace=.30)
    fig.suptitle('The same triangle now compares two models', fontsize=18, weight='bold', y=.98)
    a.set(xlim=(-3,35),ylim=(-5,16),aspect='equal');a.axis('off')
    arrow(a,(0,0),(gl,0),BLUE);arrow(a,(gl,0),(gl,el),ORANGE);arrow(a,(0,0),(gl,el),INK)
    a.plot([gl-1,gl-1,gl],[0,1,1],c=INK,lw=1.2)
    a.add_patch(Arc((0,0),12,12,theta1=0,theta2=np.degrees(phi),color=INK))
    a.text(7,.6,r'$\phi$',fontsize=13)
    a.text(-1,-2.5,'Mean-only fit',ha='left',fontsize=10,color=TEAL)
    a.text(gl,-2.5,'Line fit',ha='center',fontsize=10,color=BLUE)
    a.text(gl+1.2,el+1,'Observed y',fontsize=10)
    a.text(gl*.42,el*.65+1.6,r'$\mathrm{SSE}_R=676$',fontsize=11)
    a.text(gl+1,el/2,r'$\mathrm{SSE}_F=36$',color=ORANGE,fontsize=10)
    a.text(gl*.40,-4.6,r'$\|g\|^2=640$',color=BLUE,fontsize=11)
    a.set_title('Squared lengths: 676 = 640 + 36',fontsize=12,pad=12)
    a.text(0,12,'F = (640 / 1) / (36 / 3) = 53.33',fontsize=12,weight='bold')
    aa=np.linspace(-33,33,501); boundary=np.sqrt(nu)/critical*np.abs(aa)
    b.fill_between(aa,0,boundary,color=ORANGE,alpha=.16)
    b.plot(aa,boundary,c=ORANGE,lw=1.7)
    b.scatter([gl],[el],c=INK,s=50,zorder=5)
    b.annotate('This example', (gl,el), (8,12),fontsize=10,
               arrowprops={'arrowstyle':'-', 'color':INK})
    b.text(0,23,'do not reject',ha='center',color=MUTED,fontsize=10)
    b.text(-21,3,'reject',ha='center',color=ORANGE,fontsize=10)
    b.set(xlim=(-33,33),ylim=(0,27),aspect='equal',xlabel='Signed added-fit coordinate c',
          ylabel='Residual length r = ||e||')
    b.set_title('Two-sided 5% slope test (3 residual df)',fontsize=12,pad=18)
    b.grid(alpha=.12)
    fig.text(.06,.08,r'$t=\sqrt{3}\,c/r,\quad F=t^2.\qquad '
             r'\mathrm{Reject\ when}\ |t|>3.182\ '
             r'\Longleftrightarrow\ r<\sqrt{3}|c|/3.182.$',fontsize=12)
    fig.text(.06,.025,'Original illustration. Right: a radial cross-section; residuals live in THREE dimensions. '
             'Both signs of the slope can reject.',fontsize=9,color=MUTED)
    save(fig,'03-fit-gain-and-test-region')

def conditional_mean():
    fig,ax=plt.subplots(figsize=(8.5,4.1))
    z=np.linspace(-1,1,301)
    ax.plot(z,z*z,c=TEAL,lw=2.8,label=r'Conditional mean: $E[Y\mid Z=z]=z^2$')
    ax.axhline(1/3,c=BLUE,lw=2.5,label=r'Best straight line: $1/3+0z$')
    ax.set(xlim=(-1.05,1.05),ylim=(-.05,1.15),xlabel='Predictor z',ylabel='Predicted response')
    ax.set_title('A zero linear slope can hide a strong curved relationship',fontsize=14,weight='bold',pad=14)
    ax.grid(alpha=.12);ax.legend(loc='upper center',fontsize=10,frameon=True)
    fig.subplots_adjust(left=.1,right=.98,bottom=.22,top=.83)
    fig.text(.1,.025,r'Original population example: $Z\sim\mathrm{Uniform}[-1,1]$, '
             r'$Y=Z^2+\varepsilon$, $E[\varepsilon\mid Z]=0$, finite variances.'+'\n'
             'The line uses only 1 and Z; conditional expectation can use every square-integrable function of Z.',
             fontsize=9,color=MUTED)
    save(fig,'04-linear-versus-conditional-mean')

def checks():
    errs={}
    def ck(name,a,b):
        err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        assert err < 1e-9,(name,err)
        errs[name]=err
    ck('centered_design_coefficients',coef,[60,.8])
    ck('original_intercept',coef[0]-coef[1]*x.mean(),-76)
    ck('prediction_175cm',coef[0]+coef[1]*5,64)
    ck('residuals',e,[3,-3,0,-3,3])
    ck('sum_residuals',e.sum(),0)
    ck('normal_equations',X.T@e,[0,0])
    ck('centered_gram_values',[Sxx,Sxy],[1000,800])
    ck('squared_lengths',[sse,gain,sst],[36,640,676])
    ck('pythagorean_decomposition',sse+gain,sst)
    ck('perpendicular_components',g@e,0)
    for b in [.3,.6,.8,1.1,1.3]:
        ck(f'profiled_loss_{b}',np.sum((y-(60+b*xc))**2),36+1000*(b-.8)**2)
    H=X@np.linalg.solve(X.T@X,X.T)
    ck('hat_matrix_symmetry',H,H.T)
    ck('hat_matrix_idempotence',H@H,H)
    ck('hat_matrix_rank',np.linalg.matrix_rank(H),2)
    ck('residual_rank',np.linalg.matrix_rank(np.eye(n)-H),nu)
    ck('F_equals_t_squared',Fvalue,tvalue*tvalue)
    ck('F_cotangent',Fvalue,nu/(np.tan(phi)**2))
    ck('R_squared_correlation',gain/sst,np.corrcoef(x,y)[0,1]**2)
    ck('matching_critical_values',critical**2,f.ppf(.95,1,nu))
    ck('matching_tail_probabilities',2*t.sf(abs(tvalue),nu),f.sf(Fvalue,1,nu))
    # Independently recover the population line by Gaussian quadrature.
    # Analytically, symmetry gives E[Z]=E[Z^3]=0 and E[Z^2]=1/3.
    nodes, weights = np.polynomial.legendre.leggauss(12)
    root_weights = np.sqrt(weights / 2)
    design = np.column_stack([np.ones_like(nodes), nodes])
    population_fit = np.linalg.lstsq(design * root_weights[:, None],
                                    nodes**2 * root_weights, rcond=None)[0]
    ck('population_best_linear_slope',population_fit[1],0)
    ck('population_best_linear_intercept',population_fit[0],1/3)
    animation=Image.open(OUT/'01-predict-weight.gif')
    durations=[]
    for j in range(animation.n_frames):
        animation.seek(j);durations.append(animation.info.get('duration',0))
    result={'data_kind':'constructed teaching example, not measurements',
            'height_cm':x.tolist(),'weight_kg':y.tolist(),
            'fitted_weight_kg':yhat.tolist(),'residuals_kg':e.tolist(),
            'slope':float(coef[1]),'intercept_at_170cm':float(coef[0]),
            'SSE_full':float(sse),'SSE_reduced':float(sst),'gain':float(gain),
            'q':1,'residual_df':nu,'F':float(Fvalue),'t':float(tvalue),
            'angle_degrees':float(np.degrees(phi)),
            'p_two_sided':float(2*t.sf(abs(tvalue),nu)),
            'critical_t_5_percent':float(critical),
            'animation':{'decoded_frames':animation.n_frames,'duration_ms':sum(durations),
                         'phases':'observations; fitted line; height guide; prediction guide; final hold'},
            'maximum_error':max(errs.values()),'checks':errs}
    (OUT/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(errs),'maximum_error':max(errs.values()),'gif_frames':animation.n_frames}))

if __name__=='__main__':
    intro();mechanics();inference();conditional_mean();checks()
