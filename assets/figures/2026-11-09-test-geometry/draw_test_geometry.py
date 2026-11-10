"""Original analytic diagrams for the z/t/F learning notes.

Run with NumPy, SciPy and Matplotlib. Coordinates are illustrative, not
recovered video data. All 3D views use an orthographic camera; flat panels
use equal aspect where angles are measured. SVGs and PNG previews are paired.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc
from scipy import stats

OUT = Path(__file__).resolve().parent
BLUE, ORANGE, RED, GREEN, INK = '#2464a5', '#d18119', '#bb4751', '#348378', '#243447'
GRAY, PALE = '#758495', '#f2f5f8'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12,
                     'mathtext.fontset':'dejavusans', 'svg.fonttype':'none',
                     'axes.spines.top':False,'axes.spines.right':False,
                     'savefig.facecolor':'white'})
zcrit = stats.norm.ppf(.975)
tcrit = stats.t.ppf(.975,2)
fcrit = stats.f.ppf(.95,1,1)
angle_t = np.degrees(np.arctan(np.sqrt(2)/tcrit))
angle_f = np.degrees(np.arctan(1/np.sqrt(fcrit)))

# An orthographic camera for orthonormal coordinates (r1,r2,a).
# a is the all-ones direction in the z and t pictures.
az,el,roll=np.radians([35,24,-12])
cam_x=np.array([np.cos(az),-np.sin(az),0.])
cam_y=np.array([np.sin(el)*np.sin(az),np.sin(el)*np.cos(az),np.cos(el)])
CAM=np.array([[np.cos(roll),-np.sin(roll)],[np.sin(roll),np.cos(roll)]])@np.vstack([cam_x,cam_y])
def proj(p): return np.asarray(p)@CAM.T
def line3(ax, points, **kw):
    p=proj(points); ax.plot(p[:,0],p[:,1],**kw)
def poly3(ax,points,**kw): ax.add_patch(Polygon(proj(points),closed=True,**kw))
def arrow(ax,a,b,color=INK,lw=2.5,style='-|>',**kw):
    ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=color,lw=lw,shrinkA=0,shrinkB=0),**kw)
def arrow3(ax,a,b,**kw): arrow(ax,proj(a),proj(b),**kw)
def label3(ax,p,s,**kw): ax.text(*proj(p),s,**kw)
def dot3(ax,p,color=INK,**kw): ax.scatter(*proj(p),s=36,color=color,zorder=8,**kw)
def plain(ax,xlim,ylim):
    ax.set_aspect('equal'); ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis('off')
def title(fig,main,sub):
    fig.suptitle(main,fontsize=21,fontweight='bold',color=INK,y=.98)
    fig.text(.5,.91,sub,ha='center',fontsize=12,color=GRAY)
def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight')
    fig.savefig(OUT/(name+'.png'),dpi=155,bbox_inches='tight')
    plt.close(fig)

def z_slab():
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,6.8),gridspec_kw={'width_ratios':[1.15,1]})
    fig.subplots_adjust(top=.82,bottom=.18,wspace=.22)
    title(fig,'z test: a fixed-width slab','n = 3, known population SD = 1, two-sided significance level = 5%')
    plain(ax,(-3.5,3.6),(-3.7,3.7))
    size=2.2
    for a in [-zcrit,0,zcrit]:
        pts=[[-size,-size,a],[size,-size,a],[size,size,a],[-size,size,a]]
        poly3(ax,pts,facecolor=RED if a else BLUE,alpha=.10 if a else .05,edgecolor='none')
        line3(ax,pts+[pts[0]],color=RED if a else BLUE,lw=1.7,ls='-' if a else '--')
    arrow3(ax,[0,0,-3.1],[0,0,3.1],color=BLUE)
    label3(ax,[.1,0,3.3],r'$u=\mathbf{1}/\sqrt{3}$',color=BLUE,fontsize=13)
    dot3(ax,[0,0,0],BLUE)
    label3(ax,[-.1,0,-.35],r'$O=\mu_0\mathbf{1}$',ha='right',color=BLUE)
    for val,text in [(zcrit,r'$a=+1.96$'),(-zcrit,r'$a=-1.96$')]:
        label3(ax,[size+.05,-size,val],text,color=RED,fontsize=12)
    line3(ax,[[0,0,zcrit-.28],[.28,0,zcrit-.28],[.28,0,zcrit]],color=INK,lw=1.3)
    p=[1.1,.6,1.05]; q=[-.9,-.3,1.05]
    line3(ax,[p,q],color=GREEN,lw=2.4)
    dot3(ax,p,GREEN);dot3(ax,q,GREEN)
    ax.text(-3.35,-3.5,'All three planes have normal vector 1.\nThe middle plane has sample mean = null mean.',fontsize=11,color=GRAY)
    bx.axhspan(zcrit,3.1,color=RED,alpha=.14)
    bx.axhspan(-3.1,-zcrit,color=RED,alpha=.14)
    bx.axhspan(-zcrit,zcrit,color=BLUE,alpha=.05)
    for v in [-zcrit,zcrit]: bx.axhline(v,color=RED,lw=2)
    bx.axhline(0,color=BLUE,ls='--',lw=1)
    bx.scatter([-.8,1.15],[1.05,1.05],color=GREEN,zorder=5)
    arrow(bx,[-.68,1.05],[1.03,1.05],GREEN,lw=2,style='<->')
    bx.text(.2,1.3,'Same mean, different residual',ha='center',fontsize=10,color=GREEN)
    bx.text(0,2.52,'REJECT',ha='center',color=RED,fontweight='bold')
    bx.text(0,-2.65,'REJECT',ha='center',color=RED,fontweight='bold')
    bx.text(0,-.75,'DO NOT REJECT',ha='center',color=BLUE)
    bx.set(xlim=(-2.4,2.4),ylim=(-3.1,3.1),xlabel='One residual coordinate (the other is fixed)',ylabel=r'$a=\sqrt{3}(\bar{x}-\mu_0)$')
    bx.set_title('A flat cross-section',fontsize=14,pad=14)
    bx.set_yticks([-zcrit,0,zcrit],['-1.96','0','+1.96'])
    fig.text(.5,.035,'Moving parallel to a boundary changes sample spread, but leaves z and the decision unchanged.',ha='center',color=INK,fontsize=13)
    save(fig,'01-z-parallel-planes')

def t_cone():
    fig,ax=plt.subplots(figsize=(10.8,8))
    fig.subplots_adjust(top=.84,bottom=.13)
    title(fig,'t test: reject inside the double cone','The cone is centered at the null point; its axis is the all-ones line.')
    plain(ax,(-4.1,4.3),(-4.6,4.7))
    ratio=np.sqrt(2)/tcrit; h=3.5; ang=np.linspace(0,2*np.pi,181)
    for sign in [1,-1]:
        ring=np.c_[h*ratio*np.cos(ang),h*ratio*np.sin(ang),np.full_like(ang,sign*h)]
        for j in range(len(ang)-1): poly3(ax,[[0,0,0],ring[j],ring[j+1]],facecolor=RED,alpha=.08,edgecolor='none')
        line3(ax,ring,color=RED,lw=1.8)
        for phi in [0,np.pi]: line3(ax,[[0,0,0],[h*ratio*np.cos(phi),h*ratio*np.sin(phi),sign*h]],color=RED,lw=1.7)
    ring=np.c_[2.2*np.cos(ang),2.2*np.sin(ang),np.zeros_like(ang)]
    poly3(ax,ring,facecolor=GRAY,alpha=.08,edgecolor=GRAY,lw=1)
    arrow3(ax,[0,0,-4.05],[0,0,4.05],color=BLUE)
    label3(ax,[.1,0,4.25],r'$u=\mathbf{1}/\sqrt{3}$',color=BLUE,fontsize=14)
    dot3(ax,[0,0,0],INK); label3(ax,[-.2,0,.1],r'$O=\mu_0\mathbf{1}$',ha='right',fontsize=13)
    arrow3(ax,[0,0,0],[.48,.2,2.8],color=RED,lw=2)
    arrow3(ax,[0,0,0],[2.1,0,1.5],color=GREEN,lw=2)
    ax.text(-3.95,3.15,'REJECT\nnear either end\nof the mean line',color=RED,fontsize=13)
    ax.text(2.1,1.35,'DO NOT\nREJECT',color=GREEN,fontsize=13)
    fig.text(.5,.09,r'$|t|=\sqrt{2}\,|a|/\rho>4.303$'+'     '+r'$\theta<18.195^\circ$',ha='center',color=INK,fontsize=14)
    fig.text(.5,.035,'n = 3, two-sided alpha = 5%.  The cones extend indefinitely; the finite rims only crop the drawing.',ha='center',fontsize=11,color=GRAY)
    save(fig,'02-t-double-cone')

def t_lenience():
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,7))
    fig.subplots_adjust(top=.81,bottom=.18,wspace=.3)
    title(fig,'More residual spread needs a larger mean departure','The threshold for the statistic stays fixed; the required unstandardized mean departure grows.')
    k=tcrit/np.sqrt(2); xmax=2.1; ymax=5.9
    rho=np.linspace(0,xmax,300)
    ax.fill_between(rho,k*rho,ymax,where=k*rho<=ymax,color=RED,alpha=.12)
    ax.plot(rho,k*rho,color=RED,lw=2,label=r'$a=(4.303/\sqrt{2})\rho$')
    for r,c,l in [(.55,RED,'A'),(1.4,GREEN,'B')]:
        ax.plot([0,r],[0,3],color=c,lw=2.4)
        ax.scatter([r],[3],color=c,zorder=5)
        ax.text(r+.06,3.1,l,color=c,fontweight='bold')
    arrow(ax,[.6,3],[1.33,3],ORANGE,lw=2)
    ax.text(1.05,2.6,'Spread increases\nmean stays fixed',ha='center',fontsize=10,color=ORANGE)
    ax.text(.38,4.7,'REJECT',color=RED,fontweight='bold')
    ax.text(1.3,1.15,'DO NOT\nREJECT',color=GREEN)
    ax.set(xlim=(0,xmax),ylim=(0,ymax),xlabel=r'Residual length $\rho=\sqrt{2}\,s$',ylabel=r'Mean departure $a=\sqrt{3}(\bar{x}-\mu_0)$')
    ax.set_title('Fixed n and fixed significance level',fontsize=14)
    ax.text(.12,5.45,r'$a=(4.303/\sqrt{2})\rho$',color=RED,fontsize=11)
    # Equal scales: angle from vertical (mean axis) to data vector.
    bx.set_aspect('equal'); bx.set(xlim=(-.25,3.6),ylim=(-.35,4.1)); bx.axis('off')
    O=np.array([0.,0.]); foot=np.array([0.,3.]); tip=np.array([2.,3.])
    arrow(bx,O,foot,BLUE); arrow(bx,foot,tip,ORANGE); arrow(bx,O,tip,INK)
    bx.plot([0,.17,.17],[2.83,2.83,3.],color=GRAY,lw=1.2)
    theta=np.arctan2(2,3)
    arc=np.linspace(np.pi/2-theta,np.pi/2,60)
    bx.plot(.72*np.cos(arc),.72*np.sin(arc),color=INK)
    bx.text(.2,.9,r'$\theta$',fontsize=17)
    bx.text(-.12,1.6,r'$|a|$',ha='right',color=BLUE,fontsize=16)
    bx.text(1,3.15,r'$\rho=\sqrt{n-1}\,s$',ha='center',color=ORANGE,fontsize=15)
    bx.text(1.3,1.2,r'$\cot\theta=|a|/\rho$',fontsize=15)
    bx.text(.15,-.25,r'$|t|=\sqrt{n-1}\cot\theta$',fontsize=16)
    bx.set_title('Read the cotangent from this triangle',fontsize=14,pad=16)
    fig.text(.5,.025,'A: t = 7.71 (reject).   B: t = 3.03 (do not reject).   Scaling both legs equally leaves t unchanged.',ha='center',fontsize=12,color=INK)
    save(fig,'03-t-spread-and-angle')

def f_triangle():
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,6.8))
    fig.subplots_adjust(top=.81,bottom=.13,wspace=.18)
    title(fig,'F test: how much fit is gained by freeing the restriction?','A = data, C = full-model fit, D = reduced-model fit.  The angle belongs at D.')
    # Coordinates (added direction, nuisance direction, residual direction).
    plain(ax,(-3.7,4.5),(-1.7,4.8))
    poly3(ax,[[-2.8,-2.5,0],[3.2,-2.5,0],[3.2,2.5,0],[-2.8,2.5,0]],facecolor=BLUE,alpha=.10,edgecolor=BLUE,lw=1.1)
    line3(ax,[[0,-3,0],[0,3,0]],color=GREEN,lw=4)
    D=np.array([0,-.3,0]); C=D+[3,0,0]; A=C+[0,0,2.1]
    arrow3(ax,D,C,color=BLUE,lw=3); arrow3(ax,C,A,color=ORANGE,lw=3); arrow3(ax,D,A,color=INK,lw=2)
    for p,l,c,off in [(D,'D',GREEN,[-.25,0,-.35]),(C,'C',BLUE,[.15,0,-.35]),(A,'A',INK,[.15,0,.15])]:
        dot3(ax,p,c);label3(ax,p+off,l,color=c,fontsize=17,fontweight='bold')
    line3(ax,[C+[-.25,0,0],C+[-.25,0,.25],C+[0,0,.25]],color=INK,lw=1.2)
    ax.text(-3.5,-1.2,r'$\mathcal{M}_F=\mathrm{span}(\mathbf{1},x)$',color=BLUE,fontsize=13)
    ax.text(-3.5,1.65,r'$\mathcal{M}_R=\mathrm{span}(\mathbf{1})$',color=GREEN,fontsize=12)
    ax.text(-3.5,4.1,'Observation space (3D example)',fontsize=13,color=GRAY)
    # Exact face-on triangle, independent of camera projection.
    plain(bx,(-.65,4.9),(-1.0,3.9))
    D2=np.array([0.,0.]);C2=np.array([3.,0.]);A2=np.array([3.,2.1])
    arrow(bx,D2,C2,BLUE,lw=3);arrow(bx,C2,A2,ORANGE,lw=3);arrow(bx,D2,A2,INK,lw=2)
    bx.plot([2.8,2.8,3],[0,.2,.2],color=INK)
    for p,l in [(D2,'D'),(C2,'C'),(A2,'A')]:bx.text(p[0]-.1,p[1]-.37 if l!='A' else p[1]+.15,l,fontsize=16,fontweight='bold')
    arc=np.linspace(0,np.arctan2(2.1,3),50);bx.plot(.75*np.cos(arc),.75*np.sin(arc),color=INK);bx.text(.9,.22,r'$\phi$',fontsize=16)
    bx.text(1.4,-.68,r'$\|g\|=\|\hat y_F-\hat y_R\|$',color=BLUE,ha='center',fontsize=13)
    bx.text(3.15,1.02,r'$\|e_F\|$'+'\nremaining\nerror',color=ORANGE,fontsize=12)
    bx.text(.42,1.52,r'$\|e_R\|$'+'\nreduced error',fontsize=12,rotation=35)
    bx.text(0,3.15,r'$AD^2=DC^2+CA^2$',fontsize=18)
    fig.text(.5,.025,r'$\mathrm{SSE}_R-\mathrm{SSE}_F=\|g\|^2$'+'     and     '+r'$F=\dfrac{\|g\|^2/q}{\|e_F\|^2/\nu}=\dfrac{\nu}{q}\cot^2\phi$',ha='center',fontsize=17,color=INK)
    save(fig,'04-f-two-fits-and-sse')

def f_wedge():
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,6.6))
    fig.subplots_adjust(top=.81,bottom=.19,wspace=.25)
    title(fig,'The F wedge is a special three-dimensional case','n = 3, intercept plus slope, one restriction: numerator df = 1 and residual df = 1.')
    plain(ax,(-4,4),(-2.5,2.8))
    # A larger display angle makes the wedge visible; do not label it 5%.
    display_angle=18.; k=np.tan(np.radians(display_angle))
    for sign in [-1,1]:
        pts=[[-2.6,-2.6,sign*k*(-2.6)],[2.6,-2.6,sign*k*2.6],[2.6,2.6,sign*k*2.6],[-2.6,2.6,sign*k*(-2.6)]]
        poly3(ax,pts,facecolor=GREEN,alpha=.15,edgecolor=GREEN,lw=1.1)
    poly3(ax,[[-2.6,-2.6,0],[2.6,-2.6,0],[2.6,2.6,0],[-2.6,2.6,0]],facecolor=RED,alpha=.16,edgecolor=RED,lw=1.2)
    line3(ax,[[0,-3,0],[0,3,0]],color=BLUE,lw=3)
    label3(ax,[0,-3.15,0],r'$\mathcal{M}_R$',color=BLUE,fontsize=15)
    ax.text(-3.8,2.2,'Both boundaries intersect on the null line.',fontsize=11)
    ax.text(-3.8,-2.7,'3D angle enlarged to 18 degrees for visibility.\nIt corresponds to alpha = 20% for F(1,1).',fontsize=10,color=GRAY)
    # Exact alpha=5% cross section, preserving equal metric units.
    xx=np.linspace(-4,4,300); ktrue=1/np.sqrt(fcrit)
    bx.fill_between(xx,-ktrue*np.abs(xx),ktrue*np.abs(xx),color=RED,alpha=.20)
    bx.plot(xx,ktrue*xx,color=GREEN,lw=2);bx.plot(xx,-ktrue*xx,color=GREEN,lw=2)
    bx.axhline(0,color=RED,lw=1.5)
    bx.axvline(0,color=BLUE,ls=':',lw=1)
    bx.text(2.15,0,'REJECT',ha='center',va='center',fontsize=10,color=RED,fontweight='bold')
    bx.text(-2.15,0,'REJECT',ha='center',va='center',fontsize=10,color=RED,fontweight='bold')
    bx.text(0,1.1,'DO NOT REJECT',ha='center',color=GRAY)
    bx.text(0,-1.15,'DO NOT REJECT',ha='center',color=GRAY)
    bx.set_aspect('equal'); bx.set(xlim=(-4,4),ylim=(-2,2),xlabel='Signed coordinate in the added direction',ylabel='Signed full residual coordinate')
    bx.set_title('Exact 5% cross-section: half-angle = 4.5 degrees',fontsize=12,pad=14)
    fig.text(.5,.045,'Translate this cross-section along the null line to obtain the wedge.\nWith more residual or added dimensions, the boundary is a quadratic cone rather than two planes.',ha='center',fontsize=12,color=INK)
    save(fig,'05-f-wedge-and-cross-section')

def ci_inversion():
    nu=8;crit=stats.t.ppf(.975,nu);bhat=.8;se=.3
    bs=np.linspace(-.5,2.1,501); F=((bhat-bs)/se)**2
    fig,ax=plt.subplots(figsize=(11,5.8));fig.subplots_adjust(top=.78,bottom=.19)
    title(fig,'One restriction: t, F and the confidence interval agree','Move the hypothesized slope b; refit the intercept at each b.')
    ax.plot(bs,F,color=BLUE,lw=2.5,label=r'$F(b)=t(b)^2$')
    ax.axhline(crit**2,color=RED,lw=1.8,label=r'$F_{1,8;0.95}=t_{8;0.975}^2$')
    lo,hi=bhat-crit*se,bhat+crit*se
    ax.axvspan(lo,hi,color=GREEN,alpha=.12)
    ax.scatter([lo,hi],[crit**2]*2,color=GREEN,zorder=5)
    ax.text(bhat,9.1,'Null values not rejected\n= the 95% confidence interval',ha='center',color=GREEN,fontsize=13)
    ax.set(xlim=(-.5,2.1),ylim=(0,13),xlabel='Hypothesized slope b',ylabel='F statistic for this restriction')
    ax.legend(loc='upper right',fontsize=10,frameon=True,facecolor='white',framealpha=.97,edgecolor='none')
    fig.text(.5,.035,f'Illustrative full fit: slope = {bhat:.1f}, estimated SE = {se:.1f}, residual df = {nu}.  Interval: [{lo:.3f}, {hi:.3f}].',ha='center',fontsize=12)
    save(fig,'06-f-t-ci-inversion')

def checks():
    rng=np.random.default_rng(20261109); errs=[]
    for n in [3,5,12,30]:
        u=np.ones(n)/np.sqrt(n)
        for _ in range(20):
            x=rng.normal(size=n);mu0=.6;d=x-mu0;a=u@d;r=x-x.mean();rho=np.linalg.norm(r)
            t=np.sqrt(n)*(x.mean()-mu0)/x.std(ddof=1)
            errs += [abs(t-np.sqrt(n-1)*a/rho),abs(np.dot(u,r))]
            X=np.c_[np.ones(n),rng.normal(size=n)];y=rng.normal(size=n)
            bh=np.linalg.lstsq(X,y,rcond=None)[0];f=X@bh;e=y-f;g=f-y.mean()
            sse=e@e;sser=np.sum((y-y.mean())**2);sxx=np.sum((X[:,1]-X[:,1].mean())**2)
            stat=bh[1]/np.sqrt(sse/(n-2)/sxx)
            errs += [abs(sser-sse-g@g),abs(stat**2-(sser-sse)/(sse/(n-2)))]
            # General nonzero linear restriction, even in a multi-predictor model.
            if n>5:
                Xm=np.c_[X,rng.normal(size=n)];p=Xm.shape[1];Ginv=np.linalg.inv(Xm.T@Xm)
                bm=np.linalg.lstsq(Xm,y,rcond=None)[0];c=np.array([.3,1.,-.5]);b=.7;delta=c@bm-b
                br=bm-Ginv@c*delta/(c@Ginv@c)
                ef=y-Xm@bm;er=y-Xm@br
                fone=((er@er)-(ef@ef))/((ef@ef)/(n-p))
                tone=delta/np.sqrt((ef@ef)/(n-p)*(c@Ginv@c))
                errs += [abs(fone-tone**2),abs(c@br-b)]
    tail_errors=[]
    for nu in [1,2,8,25]:
        for val in [-12,-5,-2,-1,-.1,0,.1,1,2,5,12]:
            tail_errors.append(abs(stats.f.sf(val*val,1,nu)-2*stats.t.sf(abs(val),nu)))
    assert max(errs)<1e-9
    assert max(tail_errors)<1e-12
    assert abs(angle_t-18.1948723388)<1e-7
    assert abs(angle_f-4.5)<1e-10
    assert abs(1-np.cos(np.radians(angle_t))-.05)<1e-10
    assert abs(fcrit-np.tan(.95*np.pi/2)**2)<1e-8
    report={'z_critical':zcrit,'t_2_critical':tcrit,'t_cone_half_angle_degrees':angle_t,
            'F_1_1_critical':fcrit,'F_wedge_half_angle_degrees':angle_f,
            'max_identity_error':max(errs),'max_F_vs_two_sided_t_pvalue_error':max(tail_errors),
            'visual_conventions':'Orthographic 3D; exact equal-axis triangles; F 3D angle deliberately enlarged and labeled 20%, adjacent cross-section is exact 5%.',
            'source':'Independent algebra in the notes; numerical checks support those derivations.'}
    (OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    checks()
    for f in [z_slab,t_cone,t_lenience,f_triangle,f_wedge,ci_inversion]: f()
