"""Deterministic original PCA illustrations and independent numerical checks."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sklearn.decomposition import PCA

OUT = Path(__file__).parent
BLUE, ORANGE, GREEN, INK = '#2864a0', '#d97724', '#158477', '#263447'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11, 'axes.spines.top':False,
                     'axes.spines.right':False, 'svg.fonttype':'none', 'axes.labelcolor':INK,
                     'text.color':INK, 'axes.titleweight':'bold'})
a = np.r_[np.arange(-6, 0), np.arange(1, 7)].astype(float)
b = np.array([1,-1,1,-1,1,-1,-1,1,-1,1,-1,1], dtype=float)
V = np.array([[1,1],[1,-1]]) / np.sqrt(2)
X = np.column_stack([a,b]) @ V.T
mu = np.array([10.,20.])
raw = X + mu
n = len(X)
C = X.T @ X / (n-1)
ev = np.array([182,12])/(n-1)
model = PCA(n_components=2, svd_solver='full').fit(raw)
scores = model.transform(raw)

def save(fig, name):
    fig.savefig(OUT / (name+'.svg'), bbox_inches='tight')
    fig.savefig(OUT / (name+'.png'), dpi=160, bbox_inches='tight')
    plt.close(fig)

def geometry(ax, angle=45):
    v = np.array([np.cos(np.deg2rad(angle)),np.sin(np.deg2rad(angle))])
    t = X @ v
    foot = t[:,None] * v
    ax.plot([-6*v[0],6*v[0]],[-6*v[1],6*v[1]], color=ORANGE,lw=2)
    for x, y in zip(X,foot):
        ax.plot([x[0],y[0]],[x[1],y[1]],color='#9ba5af',lw=.9)
    ax.scatter(*X.T,c=BLUE,s=35,label='Sample: two measurements',zorder=3)
    ax.scatter(*foot.T,c=ORANGE,s=23,label='Projection on PC1',zorder=4)
    ax.axhline(0,color='#d5dbe0',lw=.6); ax.axvline(0,color='#d5dbe0',lw=.6)
    ax.set(xlim=(-6,6),ylim=(-6,6),xlabel='Measurement A, centered',ylabel='Measurement B, centered')
    ax.set_aspect('equal'); return t,foot

fig, axes = plt.subplots(1,2,figsize=(10,4),gridspec_kw={'width_ratios':[1,1.2]},layout='constrained')
geometry(axes[0]); axes[0].set_title('Two readings per sample')
axes[0].legend(loc='upper left',fontsize=8)
axes[1].scatter(a,np.zeros(n),c=ORANGE,s=55)
axes[1].axhline(0,c=ORANGE,lw=1,zorder=0)
axes[1].set(xlim=(-6.7,6.7),ylim=(-1,1),yticks=[],xlabel='PC1 score: one coordinate per sample')
axes[1].set_title('Keep one number per sample')
axes[1].text(.5,.72,'93.8% of total sample variance retained',ha='center',transform=axes[1].transAxes)
axes[1].text(.5,.22,'Gray segments on the left are discarded.\nThe orange points reconstruct the samples.',ha='center',transform=axes[1].transAxes,fontsize=10)
for spine in ['left','bottom']: axes[1].spines[spine].set_visible(False)
save(fig,'01-projection')

angles=np.linspace(0,180,721)
vs=np.column_stack([np.cos(np.deg2rad(angles)),np.sin(np.deg2rad(angles))])
vars=np.einsum('ij,jk,ik->i',vs,C,vs)
errs=np.trace(C)-vars
fig,ax=plt.subplots(figsize=(9,3.7),layout='constrained')
ax.plot(angles,vars,color=ORANGE,lw=2.5,label='Retained score variance')
ax.plot(angles,errs,color=BLUE,lw=2.5,label='Squared error / (n - 1)')
ax.axhline(np.trace(C),color=INK,ls=':',label='Their sum stays fixed')
ax.axvline(45,color=GREEN,ls='--')
ax.text(48,8.5,'PC1: 45 degrees\nmaximum variance\nminimum error',color=GREEN)
ax.set(xlim=(0,180),xticks=[0,45,90,135,180],ylim=(0,20.5),xlabel='Projection-line angle (degrees)',ylabel='Squared measurement units')
ax.legend(loc='upper center',ncol=3,fontsize=9)
save(fig,'02-variance-error')

fig,axes=plt.subplots(1,3,figsize=(10,4.6),layout='constrained')
parts=[X,np.outer(a,V[:,0]),np.outer(b,V[:,1])]
titles=['Centered data Xc','PC1: d1 u1 v1 transpose','PC2: d2 u2 v2 transpose']
for ax, data, title in zip(axes,parts,titles):
    ax.imshow(data,cmap='RdBu_r',vmin=-5,vmax=5,aspect='auto')
    ax.set(title=title,xticks=[0,1],xticklabels=['A','B'],yticks=[0,5,11],yticklabels=['1','6','12'],ylabel='Sample')
axes[0].text(.5,-.15,'Xc = PC1 contribution + PC2 contribution',ha='center',transform=axes[0].transAxes,fontsize=9)
axes[1].text(.5,-.15,'d1² = 182  →  λ1 = 182/11\nKeep: 93.8% of variance',ha='center',transform=axes[1].transAxes,fontsize=10)
axes[2].text(.5,-.15,'d2² = 12  →  λ2 = 12/11\nDiscard: 6.2% of variance',ha='center',transform=axes[2].transAxes,fontsize=10)
save(fig,'03-svd-pieces')

fig,axes=plt.subplots(1,2,figsize=(9,3.5),layout='constrained')
axes[0].bar(['A','B'],V[:,0],color=GREEN,width=.5)
axes[0].set(ylim=(0,.9),ylabel='Weight',title='Loadings: one weight per feature')
for i,v in enumerate(V[:,0]): axes[0].text(i,v+.025,'1 / sqrt(2)',ha='center',fontsize=10)
axes[1].bar(np.arange(1,n+1),a,color=ORANGE)
axes[1].axhline(0,c=INK,lw=.8)
axes[1].set(xlabel='Sample',ylabel='PC1 coordinate',title='Scores: one value per sample',xticks=[1,3,6,9,12])
save(fig,'04-scores-loadings')

fig,ax=plt.subplots(figsize=(10,2.6),layout='constrained')
ax.axis('off')
for i,(title,body,color) in enumerate([
    ('PCA','Choose shared linear axes\nKeep variance; reconstruct data',BLUE),
    ('t-SNE','Match pair probabilities\nArrange nearby observations',ORANGE),
    ('UMAP','Match a weighted neighbor graph\nArrange connected observations',GREEN)]):
    x=.01+i*.335
    ax.add_patch(FancyBboxPatch((x,.2),.305,.63,boxstyle='round,pad=.01',facecolor='#f6f8fa',edgecolor=color,transform=ax.transAxes))
    ax.text(x+.1525,.67,title,color=color,ha='center',weight='bold',fontsize=14,transform=ax.transAxes)
    ax.text(x+.1525,.43,body,ha='center',va='center',fontsize=10,transform=ax.transAxes)
ax.text(.5,.04,'Same high-dimensional samples  →  fewer coordinates; different targets',ha='center',transform=ax.transAxes)
save(fig,'05-three-objectives')

checks={}
checks['center_error']=float(np.abs(X.mean(axis=0)).max())
checks['covariance_expected_error']=float(np.abs(C-np.array([[97,85],[85,97]])/11).max())
checks['eigen_equation_error']=float(np.abs(C@V-V*ev).max())
checks['sklearn_eigenvalue_error']=float(np.abs(model.explained_variance_-ev).max())
checks['singular_square_error']=float(np.abs(model.singular_values_**2-np.array([182,12])).max())
checks['score_covariance_error']=float(np.abs(np.cov(scores,rowvar=False)-np.diag(ev)).max())
checks['pythagorean_error']=max(float(abs(np.sum(X**2)-np.sum((X@v)**2)-np.sum((X-np.outer(X@v,v))**2))) for v in vs)
checks['rank_one_residual_ss']=float(np.sum((X-parts[1])**2))
checks['retained_fraction']=float(ev[0]/ev.sum())
checks['loading_feature_correlation']=float(np.corrcoef(X[:,0],a)[0,1])
checks['sklearn_version']=__import__('sklearn').__version__
assert max(v for k,v in checks.items() if k.endswith('_error'))<1e-10
assert abs(checks['rank_one_residual_ss']-12)<1e-10
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
(OUT/'toy-data.json').write_text(json.dumps({'centered':X.tolist(),'raw':raw.tolist(),'a':a.tolist(),'b':b.tolist(),'mean':mu.tolist()},indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,indent=2))
