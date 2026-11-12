"""Original analytic figures. Run with Python + numpy, scipy, matplotlib, Pillow.

No external data or source-slide artwork is used. The HTML uses the vault's shared builder.
"""
from pathlib import Path
import importlib.util
import json
import math
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.stats import multivariate_normal, norm
from PIL import Image, ImageDraw

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
TEAL='#087f83'; GOLD='#b77418'; GRAY='#788793'; INK='#20313b'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':INK,'text.color':INK,'axes.titlecolor':INK,'svg.fonttype':'none'})
x=np.array([-1,0,.5,1.5,2.]);y=np.array([-1.2,.8,1.1,2.9,3.7]);sigma=.75
Phi=np.column_stack([np.ones(len(x)),x]);G=Phi.T@Phi;b=Phi.T@y

def posterior(tau):
    lam=0 if np.isinf(tau) else sigma**2/tau**2
    R=G+lam*np.eye(2)
    return np.linalg.solve(R,b),sigma**2*np.linalg.solve(R,np.eye(2)),lam

def ellipse(mu,V,r):
    d,Q=np.linalg.eigh(V);t=np.linspace(0,2*np.pi,151)
    return mu[:,None]+r*Q@np.diag(np.sqrt(d))@np.vstack([np.cos(t),np.sin(t)])

def save(fig,name):
    fig.savefig(OUT/f'{name}.svg',bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/f'{name}.png',dpi=145,bbox_inches='tight',facecolor='white')
    plt.close(fig)

def ridge_scene(tau,fig,axes):
    for ax in axes:ax.clear();ax.grid(alpha=.16)
    mu,V,lam=posterior(tau);mo,Vo,_=posterior(np.inf)
    ax=axes[0]
    for r in (1,2):
        q=ellipse(mo,Vo,r);ax.plot(*q,color=GRAY,ls='--',lw=1.1)
        q=ellipse(mu,V,r);ax.plot(*q,color=TEAL,lw=2)
    path=np.array([posterior(t)[0] for t in np.logspace(-2,3,160)])
    ax.plot(*path.T,color='#b8cbcc',lw=1,zorder=0)
    ax.scatter(*mo,marker='x',s=85,c=GRAY,label='OLS')
    ax.scatter(*mu,s=35,c=TEAL,label='posterior mean = ridge')
    ax.set(xlim=(-1.3,2.5),ylim=(-.4,3.4),xlabel='intercept $w_0$',ylabel='slope $w_1$',title='Parameter space');ax.set_aspect('equal');ax.legend(fontsize=8,loc='upper left')
    ax=axes[1];z=np.linspace(-2.5,4,750)
    if np.isfinite(tau):ax.plot(z,norm.pdf(z,scale=tau),color=GOLD,label='prior slope')
    ax.plot(z,norm.pdf(z,mo[1],np.sqrt(Vo[1,1])),color=GRAY,ls='--',label='flat-prior posterior')
    ax.plot(z,norm.pdf(z,mu[1],np.sqrt(V[1,1])),color=TEAL,label='posterior slope')
    ax.set(xlim=(-2.5,4),ylim=(0,4.3),xlabel='slope $w_1$',ylabel='density',title='The prior becomes locally flatter');ax.legend(fontsize=8,loc='upper right')
    ax=axes[2];xx=np.linspace(-2.3,3,150);F=np.column_stack([np.ones(len(xx)),xx]);m=F@mu;sd=np.sqrt(np.einsum('ij,jk,ik->i',F,V,F))
    ax.fill_between(xx,m-2*sd,m+2*sd,color=TEAL,alpha=.13,label='latent mean ± 2 SD')
    ax.plot(xx,F@mo,color=GRAY,ls='--',label='OLS');ax.plot(xx,m,color=TEAL,lw=2,label='posterior mean')
    ax.scatter(x,y,c=INK,zorder=3,s=25);ax.set(xlim=(-2.3,3),ylim=(-4.8,6.8),xlabel='input $x$',ylabel='$f(x)$',title='Fixed observations and noise SD = 0.75');ax.legend(fontsize=8,ncol=3,loc='upper left')
    ts='∞ (improper flat-prior limit)' if np.isinf(tau) else f'{tau:.3f}'
    fig.suptitle(f'Prior SD τ = {ts}     |     ridge penalty λ = {lam:.5f}',fontsize=14,y=.98)
    fig._ridge_footer.set_text(f'Posterior mean = ({mu[0]:.3f}, {mu[1]:.3f})    |    posterior slope SD = {np.sqrt(V[1,1]):.3f}\nBoth coefficients are penalized. Fixed axes; contours have squared Mahalanobis distances 1 and 4.')

def ridge_figure():
    fig=plt.figure(figsize=(10,7.3));gs=fig.add_gridspec(2,2,height_ratios=[1.1,1]);axes=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1]),fig.add_subplot(gs[1,:])]
    fig.subplots_adjust(left=.08,right=.97,bottom=.13,top=.88,hspace=.48,wspace=.3)
    fig._ridge_footer=fig.text(.5,.035,'',ha='center',fontsize=9)
    return fig,axes

def ridge_outputs():
    for t,name in [(.1,'ridge-strong'),(1.,'ridge-moderate'),(np.inf,'ridge-limit')]:
        fig,axes=ridge_figure();ridge_scene(t,fig,axes);save(fig,name)
    fig,axes=ridge_figure();taus=[.1]*9+list(np.logspace(-1,1.5,55))+[np.inf]*14
    anim=FuncAnimation(fig,lambda i:ridge_scene(taus[i],fig,axes),frames=len(taus),interval=110)
    anim.save(OUT/'ridge-prior-to-ols.gif',writer=PillowWriter(fps=9),dpi=90);plt.close(fig)
    with Image.open(OUT/'ridge-prior-to-ols.gif') as im:
        indexes=sorted(set([0,im.n_frames//4,im.n_frames//2,3*im.n_frames//4,im.n_frames-1]));tiles=[]
        for i in indexes:
            im.seek(i);frame=im.convert('RGB');frame.thumbnail((650,500));tile=Image.new('RGB',(650,frame.height+25),'white');tile.paste(frame,(0,25));ImageDraw.Draw(tile).text((10,6),f'Decoded GIF frame {i}',fill='black');tiles.append(tile)
        sheet=Image.new('RGB',(1300,3*tiles[0].height),'#e8e8e8')
        for j,tile in enumerate(tiles):sheet.paste(tile,((j%2)*650,(j//2)*tile.height))
        sheet.save(OUT/'gif-review.jpg',quality=93)
        return {'decoded_frames':im.n_frames,'reviewed_frame_indices':indexes,'duration_ms':sum(_gif_durations(OUT/'ridge-prior-to-ols.gif'))}

def _gif_durations(path):
    with Image.open(path) as im:
        for i in range(im.n_frames):im.seek(i);yield im.info.get('duration',0)

def reference_figures():
    fig,axs=plt.subplots(1,2,figsize=(9,3.8),sharex=True,sharey=True)
    a=np.arange(-2,3)
    for ax,sign in zip(axs,[1,-1]):
        ax.scatter(a,sign*a,c=TEAL,s=50);ax.plot(a,sign*a,c=TEAL,alpha=.4)
        ax.set(xlabel='measurement A',ylabel='measurement B',title=f'Same marginal summaries\nSample covariance = {sign*2.5:g}')
        ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xticks(a);ax.set_yticks(a)
    fig.suptitle('Pairing is information: both means are 0; both sample variances are 2.5',fontsize=12)
    fig.tight_layout();save(fig,'multivariate-pairing')
    cov=np.array([[1,.8],[.8,1]])
    grid=np.linspace(-3,3,160);u,v=np.meshgrid(grid,grid);z=multivariate_normal.pdf(np.dstack([u,v]),cov=cov)
    fig,ax=plt.subplots(figsize=(6.4,4.3));ax.contour(u,v,z,levels=[.025,.07,.14,.22],colors=[TEAL]);ax.axvline(0,color=GRAY,lw=.6);ax.axhline(0,color=GRAY,lw=.6)
    ax.annotate('Positive covariance:\nhigh values tend to occur together',xy=(1.1,1.1),xytext=(-2.8,2.2),arrowprops={'arrowstyle':'->','color':GRAY},fontsize=10)
    ax.set(xlabel='$X_1$',ylabel='$X_2$',title='A joint normal law: unit variances, correlation 0.8');ax.set_aspect('equal');fig.tight_layout();save(fig,'mvn-contours')
    vals,Q=np.linalg.eigh(cov);L=Q@np.diag(np.sqrt(vals));theta=np.linspace(0,2*np.pi,200);circle=np.vstack([np.cos(theta),np.sin(theta)]);ell=L@circle
    fig,axs=plt.subplots(1,2,figsize=(9,4))
    axs[0].plot(*circle,color=GRAY);axs[1].plot(*ell,color=TEAL)
    for j in range(2):axs[0].arrow(0,0,*(np.eye(2)[:,j]),color=[GOLD,TEAL][j],width=.012,length_includes_head=True);axs[1].arrow(0,0,*L[:,j],color=[GOLD,TEAL][j],width=.012,length_includes_head=True)
    for ax,title in zip(axs,['Independent Z: covariance I','X = LZ: covariance LLᵀ = Σ']):
        ax.set(xlim=(-1.6,1.6),ylim=(-1.6,1.6),title=title,xlabel='coordinate 1',ylabel='coordinate 2');ax.set_aspect('equal');ax.grid(alpha=.2)
    fig.suptitle('Stretch along two perpendicular directions: lengths √0.2 and √1.8',fontsize=12);fig.tight_layout();save(fig,'mvn-transform')
    fig,axs=plt.subplots(1,2,figsize=(9.3,4))
    axs[0].contour(u,v,z,levels=[.025,.07,.14,.22],colors=[TEAL]);axs[0].axvline(1,color=GOLD);axs[0].scatter([1],[.8],c=GOLD,s=38);axs[0].set(xlabel='$X_1$',ylabel='$X_2$',title='Fix X₁ = 1');axs[0].set_aspect('equal')
    axs[1].plot(grid,norm.pdf(grid),color=GRAY,ls='--',label='marginal N(0, 1)');axs[1].plot(grid,norm.pdf(grid,.8,.6),color=TEAL,label='conditional N(0.8, 0.36)');axs[1].set(xlabel='$X_2$',ylabel='density',title='Normalize the vertical slice');axs[1].legend(fontsize=9);axs[1].grid(alpha=.2)
    fig.tight_layout();save(fig,'mvn-conditioning')
    xx=np.linspace(-2,2,300);anchor=.9
    fig,ax=plt.subplots(figsize=(7,3.8));ax.plot(xx,np.exp(-(xx-anchor)**2/2),color=INK,lw=3,label='exact Gaussian kernel')
    for count,color in [(1,GOLD),(3,'#a067a0'),(10,TEAL)]:
        approx=np.exp(-xx**2/2-anchor**2/2)*sum((xx*anchor)**j/math.factorial(j) for j in range(count))
        ax.plot(xx,approx,ls='--',c=color,label=f'first {count} features')
    ax.set(xlabel="second input x′ (first input fixed at 0.9)",ylabel="k(0.9, x′)",title='An infinite feature inner product, approached by finite sums');ax.legend(fontsize=8);ax.grid(alpha=.2);fig.tight_layout();save(fig,'kernel-series')
    tx=np.array([-1.6,-.4,.8,1.7]);ty=np.array([-.9,-.25,.85,.65]);px=np.linspace(-3,3,150);ell=.8;sn=.2
    kernel=lambda a,b:np.exp(-(a[:,None]-b[None,:])**2/(2*ell**2))
    C=kernel(tx,tx)+sn**2*np.eye(len(tx));cross=kernel(px,tx);mean=cross@np.linalg.solve(C,ty);V=kernel(px,px)-cross@np.linalg.solve(C,cross.T);sd=np.sqrt(np.diag(V))
    fig,axs=plt.subplots(1,2,figsize=(10,4))
    for ax,title,m,s in zip(axs,['Prior over function values','Posterior after four noisy observations'],[np.zeros(len(px)),mean],[np.ones(len(px)),sd]):
        ax.fill_between(px,m-2*s,m+2*s,color=TEAL,alpha=.16);ax.plot(px,m,c=TEAL,lw=2);ax.set(xlim=(-3,3),ylim=(-2.3,2.3),title=title,xlabel='input x',ylabel='latent function f(x)');ax.grid(alpha=.18)
    axs[1].scatter(tx,ty,c=INK,zorder=3);fig.suptitle('Same GP prior kernel: variance 1, length scale 0.8; noise SD 0.2',fontsize=12);fig.tight_layout();save(fig,'gp-conditioning')

def checks():
    rng=np.random.default_rng(20261112);errors={};refs=[]
    for tau in [.1,.2,1,3,10,10**1.5,np.inf]:
        mu,V,lam=posterior(tau)
        aug=np.vstack([Phi,np.sqrt(lam)*np.eye(2)]);target=np.r_[y,0,0]
        expected=np.linalg.lstsq(aug,target,rcond=None)[0]
        errors[f'ridge_augmented_ls_{tau}']=float(np.max(abs(mu-expected)))
        precision=G/sigma**2+(0 if np.isinf(tau) else 1/tau**2)*np.eye(2)
        errors[f'covariance_inverse_{tau}']=float(np.max(abs(precision@V-np.eye(2))))
        refs.append({'tau':None if np.isinf(tau) else tau,'lambda':lam,'mu':mu.tolist(),'V':V.ravel().tolist()})
    A=np.array([[3.,.7],[.7,1.8]]);bb=np.array([1.,-2.]);m=np.linalg.solve(A,bb);w=rng.normal(size=(50,2))
    before=np.einsum('ij,jk,ik->i',w,A,w)-2*w@bb
    after=np.einsum('ij,jk,ik->i',w-m,A,w-m)-bb@m
    errors['completing_square']=float(np.max(abs(before-after)))
    cov=np.array([[1,.8],[.8,1.]]);joint_precision=np.linalg.inv(cov)
    errors['conditional_mean']=abs(-joint_precision[1,0]/joint_precision[1,1]-.8)
    errors['conditional_variance']=abs(1/joint_precision[1,1]-.36)
    # Independent precision/block-conditioning routes and primal/dual GP predictions.
    S=np.array([[1.4,.2],[.2,.7]]);C=Phi@S@Phi.T+sigma**2*np.eye(len(x));p=np.array([1.,.7]);k=Phi@S@p;c=p@S@p+sigma**2
    mu=np.linalg.solve(G/sigma**2+np.linalg.inv(S),b/sigma**2);V=np.linalg.inv(G/sigma**2+np.linalg.inv(S))
    dmean=k@np.linalg.solve(C,y);dvar=c-k@np.linalg.solve(C,k)
    errors['primal_dual_mean']=abs(p@mu-dmean);errors['primal_dual_variance']=abs(p@V@p+sigma**2-dvar)
    J=np.block([[C,k[:,None]],[k[None,:],np.array([[c]])]]);P=np.linalg.inv(J)
    errors['block_precision_mean']=abs(-P[-1,:-1]@y/P[-1,-1]-dmean)
    errors['block_precision_variance']=abs(1/P[-1,-1]-dvar)
    # Covariance increases as prior precision decreases, for fixed data/noise.
    eigs=[]
    for a,big in zip(np.logspace(-1,1.5,30)[:-1],np.logspace(-1,1.5,30)[1:]):
        eigs.extend(np.linalg.eigvalsh(posterior(big)[1]-posterior(a)[1]))
    assert min(eigs)>-1e-12
    # Rank-deficient flat-prior caveat: null direction variance is tau².
    R=np.array([[1.,1.],[2.,2.]]);null=np.array([1.,-1.])/np.sqrt(2);tau=20
    Vr=np.linalg.inv(R.T@R+np.eye(2)/tau**2)
    errors['rank_deficient_null_variance']=abs(null@Vr@null-tau**2)
    aa=rng.normal(size=(8,2));features=np.column_stack([aa,np.sum(aa**2,axis=1)]);K=aa@aa.T+np.outer(np.sum(aa**2,axis=1),np.sum(aa**2,axis=1))
    errors['handwritten_custom_kernel']=float(np.max(abs(features@features.T-K)))
    u=.9;v=-1.2;features_u=np.array([np.exp(-u*u/2)*u**j/np.sqrt(float(math.factorial(j))) for j in range(35)]);features_v=np.array([np.exp(-v*v/2)*v**j/np.sqrt(float(math.factorial(j))) for j in range(35)])
    errors['gaussian_feature_series']=abs(features_u@features_v-np.exp(-(u-v)**2/2))
    assert max(errors.values())<1e-8,errors
    result={'description':'Analytic derivations plus independent numerical checks; original illustrative data.','data':{'x':x.tolist(),'y':y.tolist(),'sigma':sigma,'both_coefficients_penalized':True},'maximum_absolute_errors':errors,'covariance_increment_min_eigenvalue':float(min(eigs)),'reference_states':refs}
    (OUT/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result

def build_html():
    path=ROOT/'.agents/skills/animate-geometry/scripts/build_explorer.py'
    spec=importlib.util.spec_from_file_location('builder',path);builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    names=['body.html','explorer.css','math.js','explorer.js'];files=[OUT/n for n in names]
    txt=[p.read_text(encoding='utf-8') for p in files]
    page=builder.compile_html('Bayesian regression, ridge, and the flat-prior limit',txt[0],[txt[1]],txt[2:])
    builder.write_artifact(OUT/'explorer.html',page,files)

if __name__=='__main__':
    result=checks();reference_figures();build_html();result['gif']=ridge_outputs()
    for p in OUT.glob('*.svg'):ET.parse(p)
    (OUT/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Math checks PASS; static SVGs parsed; HTML and GIF generated.')
