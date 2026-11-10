"""Reproducible original scientific figures; no source image is modified.
Run with Python + numpy + matplotlib + Pillow. Outputs beside this file.
Coordinates in every 3D scene are values for individuals 1, 2, 3.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent
BG, FG, MUTED = '#101823', '#eef3fb', '#adbdcf'
PLANE, MEAN = '#72baca', '#ffdb80'
COLORS = ['#42d9ef', '#ffad66', '#cc98ff', '#ff729d', '#9cda77', '#f2dd66', '#6ca7ff', '#db9cba']
NAMES = list('ABCDEFGH')
one = np.ones(3)
u = one / np.sqrt(3)
v1 = np.array([-1., 0., 1.]) / np.sqrt(2)
v2 = np.array([-1., 2., -1.]) / np.sqrt(6)
angles = np.deg2rad([0, 60, 110, 155, 205, 255, 300, 335])
radii = np.array([np.sqrt(2), np.sqrt(2), .65, 2., 2.8, 1.8, 1.15, 2.4])
means = np.array([2., .7, -.7, 1.1, -1.3, .3, 1.5, -.2])
Q = np.cos(angles)[:, None]*v1 + np.sin(angles)[:, None]*v2
C = radii[:, None]*Q
P = means[:, None]*one
X = P+C
S = radii/np.sqrt(2)
Z = C/S[:, None]
O = np.zeros(3)

plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':13,
    'text.color':FG, 'axes.labelcolor':FG, 'axes.edgecolor':MUTED,
    'xtick.color':MUTED, 'ytick.color':MUTED, 'figure.facecolor':BG,
    'axes.facecolor':BG, 'savefig.facecolor':BG, 'svg.fonttype':'none'})

def line(ax, a, b, **kw):
    pts=np.array([a,b]); ax.plot(*pts.T, **kw)

def arrow(ax, a, b, color, alpha=1, lw=2):
    ax.quiver(*a, *(b-a), color=color, alpha=alpha, linewidth=lw, arrow_length_ratio=.085)

def dot(ax, p, color, label=None, size=42, offset=.1):
    ax.scatter(*p, color=color, s=size, depthshade=False)
    if label: ax.text(*(p+offset), label, color=color, fontsize=12)

def scene(ax, limit=3.5, disk=2.9, sphere=False, axislabels=True, meanaxis=True):
    ax.set(xlim=(-limit,limit), ylim=(-limit,limit), zlim=(-limit,limit))
    ax.set_box_aspect((1,1,1), zoom=1.2); ax.view_init(elev=22, azim=-10)
    ax.set_axis_off()
    t=np.linspace(0,2*np.pi,100)
    rr=np.linspace(0,disk,2)
    surface=rr[:,None,None]*(np.cos(t)[None,:,None]*v1+np.sin(t)[None,:,None]*v2)
    ax.plot_surface(*surface.transpose(2,0,1), color=PLANE, alpha=.09, linewidth=0, shade=False)
    ring=disk*(np.cos(t)[:,None]*v1+np.sin(t)[:,None]*v2)
    ax.plot(*ring.T,color=PLANE,alpha=.26,lw=1)
    for k in range(3):
        b=np.eye(3)[k]*limit*.76
        line(ax,-b*.4,b,color=MUTED,alpha=.28,lw=.8)
        if axislabels: ax.text(*b, f'individual {k+1}', fontsize=10, color=MUTED)
    if meanaxis:
        line(ax,-u*limit*.92,u*limit*.92,color=MEAN,lw=1.8,alpha=.75)
        arrow(ax,O,u*limit*.92,MEAN,lw=1.4)
        ax.text(*(u*limit*1.06),r'$\mathbf{1}$ direction',color=MEAN,fontsize=12)
    dot(ax,O,FG,size=15)
    if sphere:
        for lat in np.linspace(-np.pi/2,np.pi/2,9)[1:-1]:
            pts=np.cos(lat)*(np.cos(t)[:,None]*v1+np.sin(t)[:,None]*v2)+np.sin(lat)*u
            ax.plot(*pts.T,color=MUTED,lw=.7,alpha=.27)
        for lng in np.linspace(0,2*np.pi,12,endpoint=False):
            pts=np.cos(t)[:,None]*(np.cos(lng)*v1+np.sin(lng)*v2)+np.sin(t)[:,None]*u
            ax.plot(*pts.T,color=MUTED,lw=.7,alpha=.23)
        ring=np.cos(t)[:,None]*v1+np.sin(t)[:,None]*v2
        ax.plot(*ring.T,color=FG,lw=2.4,alpha=.9)

def save(fig, name):
    fig.savefig(OUT/f'{name}.svg',bbox_inches='tight')
    fig.savefig(OUT/f'{name}.png',dpi=145,bbox_inches='tight')
    plt.close(fig)

def title(fig, heading, sub):
    fig.suptitle(heading,fontsize=23,fontweight='bold',y=.98)
    fig.text(.5,.905,sub,ha='center',fontsize=13,color=MUTED)

def coordinate_figure():
    fig=plt.figure(figsize=(15,6.7))
    title(fig,'First change the meaning of the axes','Same 3 individuals and 2 features. Rows become points on the left; columns become vectors on the right.')
    ax=fig.add_axes([.08,.2,.33,.59])
    for i,(a,b) in enumerate(X[:2].T):
        ax.scatter(a,b,s=100,color=FG); ax.annotate(f'individual {i+1}',(a,b),xytext=(9,8),textcoords='offset points')
    ax.set(xlim=(.5,3.6),ylim=(-.7,2.6),xlabel='feature A',ylabel='feature B')
    ax.grid(alpha=.12); ax.set_title('Usual scatterplot: 3 points',pad=17)
    ax=fig.add_axes([.49,.14,.47,.68],projection='3d')
    scene(ax,3.4,0,axislabels=True,meanaxis=False)
    # Hide mean-direction artists here: this panel introduces only observation space.
    for artist in list(ax.lines):
        if artist.get_color()==MEAN: artist.set_visible(False)
    for artist in list(ax.texts):
        if 'direction' in artist.get_text(): artist.set_visible(False)
    for j in range(2): arrow(ax,O,X[j],COLORS[j]); dot(ax,X[j],COLORS[j],NAMES[j])
    ax.set_title('Observation space: 2 feature vectors',pad=0)
    fig.text(.5,.07,'A = (1, 2, 3)    B = (−0.3, 1.7, 0.7)    Each 3D endpoint stores one entire feature.',ha='center',fontsize=14)
    save(fig,'01-coordinate-switch')

def centering_figure():
    fig=plt.figure(figsize=(19,7.7))
    title(fig,'Centering removes the component along the all-ones line','Eight illustrative features A–H. A fixed color follows the same feature throughout; the plane is H: x₁ + x₂ + x₃ = 0.')
    axs=[fig.add_subplot(1,3,k+1,projection='3d') for k in range(3)]
    for ax in axs: scene(ax,4.2,3.1)
    axs[0].set_title('1   Original vectors and mean projections',fontsize=15)
    for j in range(8):
        arrow(axs[0],O,X[j],COLORS[j],alpha=.75,lw=1.3); dot(axs[0],X[j],COLORS[j],NAMES[j])
        line(axs[0],P[j],X[j],color=COLORS[j],ls='--',lw=1.2,alpha=.55)
        dot(axs[0],P[j],COLORS[j],size=15)
    axs[1].set_title('2   Translate the residual arrow for A',fontsize=15)
    p,x,c=P[0],X[0],C[0]
    arrow(axs[1],O,p,MEAN); arrow(axs[1],O,x,COLORS[0],alpha=.25)
    for t in [0,.5,1]:
        a=(1-t)*p; b=a+c
        arrow(axs[1],a,b,COLORS[0],alpha=.35+.6*t,lw=2.5)
    line(axs[1],x,c,color=FG,ls=':',lw=1.5)
    arrow(axs[1],x,c,FG,alpha=.55,lw=1)
    dot(axs[1],p,MEAN,r'$p_A$')
    dot(axs[1],x,COLORS[0],r'$x_A$')
    dot(axs[1],c,COLORS[0],r'$c_A$')
    axs[2].set_title('3   All centered vectors start at the origin',fontsize=15)
    for j in range(8): arrow(axs[2],O,C[j],COLORS[j],lw=1.7); dot(axs[2],C[j],COLORS[j],NAMES[j])
    fig.subplots_adjust(left=0,right=1,bottom=.19,top=.82,wspace=0)
    notes=[r'$p_j=\bar{x}_j\mathbf{1}$'+'\nDashed segment: residual from projection foot to tip.',
           r'$p_A\to x_A\quad\longmapsto\quad 0\to c_A$'+'\nNo rotation; same arrow, translated by −p_A.',
           r'$c_j=x_j-\bar{x}_j\mathbf{1}\in H$'+'\nCentering also projects the original endpoint onto H.']
    for x,txt in zip([1/6,.5,5/6],notes): fig.text(x,.07,txt,ha='center',fontsize=13,linespacing=1.7)
    save(fig,'02-project-and-center')

def flat(ax,limit):
    ax.set_aspect('equal');ax.set(xlim=(-limit,limit),ylim=(-limit,limit))
    ax.axhline(0,color=MUTED,alpha=.3,lw=1);ax.axvline(0,color=MUTED,alpha=.3,lw=1)
    ax.set_xlabel(r'coordinate along $v_1$');ax.set_ylabel(r'coordinate along $v_2$')
    ax.spines[['top','right']].set_visible(False)

def circle(ax,r,**kw):
    t=np.linspace(0,2*np.pi,160); ax.plot(r*np.cos(t),r*np.sin(t),**kw)

def flat_arrow(ax,p,color,alpha=1):
    ax.annotate('',xy=p,xytext=(0,0),arrowprops={'arrowstyle':'->','color':color,'lw':2,'alpha':alpha})

def scaling_figure():
    fig,axs=plt.subplots(1,3,figsize=(18,7.5))
    title(fig,'Standard deviation is a length scale — not a point','Face-on views of the SAME zero-mean plane H. v₁ and v₂ are orthonormal directions within it, not individuals.')
    titles=['1   Centered lengths still differ','2   Divide by sample SD','3   Divide once more by √2']
    for ax,heading in zip(axs,titles): flat(ax,3.25 if ax is axs[0] else 1.9);ax.set_title(heading,fontsize=15,pad=15)
    for j in range(8):
        coords=np.array([np.cos(angles[j]),np.sin(angles[j])])
        for ax,scale in zip(axs,[radii[j],np.sqrt(2),1]):
            p=scale*coords;flat_arrow(ax,p,COLORS[j]);ax.scatter(*p,color=COLORS[j],s=48,zorder=3)
            ax.text(*(p+.10*coords+.03),NAMES[j],color=COLORS[j])
    circle(axs[0],1,color=FG,ls=':',alpha=.35)
    circle(axs[1],np.sqrt(2),color=FG,lw=1.5)
    circle(axs[2],np.sqrt(2),color=MUTED,ls='--',alpha=.4)
    circle(axs[2],1,color=FG,lw=2)
    # A's SD appears as a measured segment, separate from its feature endpoint.
    axs[0].annotate('',xy=(1,-.4),xytext=(0,-.4),arrowprops={'arrowstyle':'|-|','color':MEAN,'lw':2})
    axs[0].text(.5,-.72,r'$s_A=1$',color=MEAN,ha='center')
    fig.subplots_adjust(left=.055,right=.98,top=.78,bottom=.23,wspace=.26)
    notes=[r'$\|c_j\|=\sqrt{2}\,s_j$'+'\nA has length √2 and SD 1; C has length 0.65.',
           r'$z_j=c_j/s_j,\quad\|z_j\|=\sqrt{2}$'+'\nAll sample SDs are 1. This is NOT a unit circle.',
           r'$q_j=z_j/\sqrt{2}=c_j/\|c_j\|$'+'\nAll lengths are 1. Points encode direction, not SD.']
    for x,txt in zip([.18,.515,.85],notes): fig.text(x,.065,txt,ha='center',fontsize=13,linespacing=1.7)
    save(fig,'03-sd-and-normalization')

def sphere_figure():
    fig=plt.figure(figsize=(15,8.2))
    title(fig,'A unit sphere, a zero-mean plane, and their great circle','The white circle is S² ∩ H. Every centered unit feature vector ends on it; off-plane sphere points are not centered.')
    ax=fig.add_axes([.01,.14,.56,.69],projection='3d');scene(ax,1.65,1.3,sphere=True,axislabels=False)
    for j in range(8): arrow(ax,O,Q[j],COLORS[j],lw=1.7);dot(ax,Q[j],COLORS[j],NAMES[j],size=48,offset=.04)
    ax=fig.add_axes([.64,.25,.30,.53]);flat(ax,1.25);circle(ax,1,color=FG,lw=1.7)
    for j in [0,1]:
        p=np.array([np.cos(angles[j]),np.sin(angles[j])]);flat_arrow(ax,p,COLORS[j]);ax.scatter(*p,s=70,color=COLORS[j]);ax.text(*(1.08*p),f'q{NAMES[j]}',color=COLORS[j])
    t=np.linspace(0,np.pi/3,40);ax.plot(.36*np.cos(t),.36*np.sin(t),color=MEAN,lw=2)
    ax.text(.42,.18,'60°',color=MEAN);ax.set_title('Same circle, viewed face-on',pad=18,fontsize=15)
    fig.text(.29,.075,'Sphere surface: ||q|| = 1\nPlane: q₁ + q₂ + q₃ = 0\nIntersection: a 1-dimensional circle, S¹',ha='center',fontsize=13,linespacing=1.6)
    fig.text(.79,.075,r'$r_{AB}=q_A^\top q_B=\cos 60^\circ=0.5$'+'\nThe angle is between radius vectors from the origin.\nPerspective on the left does not preserve angles.',ha='center',fontsize=13,linespacing=1.6)
    save(fig,'04-sphere-and-correlation')

def animation():
    fig=plt.figure(figsize=(8,8));ax=fig.add_subplot(projection='3d')
    def frame(k):
        ax.clear()
        if k<8: t=0.; phase=0
        elif k<32: t=(k-8)/23;phase=0
        elif k<40: t=1.;phase=0
        elif k<64: t=(k-40)/23;phase=1
        else: t=1.;phase=1
        if phase==0:
            points=X-t*P;limit=4.2;disk=3.1
            header='CENTER: subtract the mean component'
            formula=r'$x_j(t)=x_j-t\bar{x}_j\mathbf{1},\quad 0\leq t\leq1$'
        else:
            points=((1-t)*radii+t)[:,None]*Q;limit=4.2*(1-t)+1.65*t;disk=3.1*(1-t)+1.3*t
            header='NORMALIZE: keep direction, change length'
            formula=r'$c_j\ \longrightarrow\ q_j=c_j/\|c_j\|$'
        scene(ax,limit,disk,sphere=True,axislabels=False)
        for j in range(8):
            arrow(ax,O,points[j],COLORS[j],lw=1.7);dot(ax,points[j],COLORS[j],NAMES[j],offset=.06)
            if phase==0: line(ax,X[j],C[j],color=COLORS[j],ls=':',lw=1,alpha=.35)
        ax.set_title(header+'\n'+formula,fontsize=16,pad=0)
        return []
    fig.text(.5,.05,'Same colors = same features. White circle = unit sphere ∩ zero-mean plane.\nCentering moves parallel to 1. Radial normalization can shrink OR expand.\nCamera scale zooms in only during normalization; this is not a sampling animation.',ha='center',fontsize=10,linespacing=1.6)
    fig.subplots_adjust(left=0,right=1,bottom=.12,top=.91)
    anim=FuncAnimation(fig,frame,frames=76,interval=90)
    anim.save(OUT/'05-center-then-normalize.gif',writer=PillowWriter(fps=11),dpi=90)
    plt.close(fig)

def checks():
    H=np.eye(3)-np.ones((3,3))/3
    errors={
        'means':float(np.max(np.abs(X.mean(axis=1)-means))),
        'centering':float(np.max(np.abs(X@H-C))),
        'plane_constraint':float(np.max(np.abs(C@one))),
        'sample_sd':float(np.max(np.abs(X.std(axis=1,ddof=1)-S))),
        'z_radius':float(np.max(np.abs(np.linalg.norm(Z,axis=1)-np.sqrt(2)))),
        'unit_radius':float(np.max(np.abs(np.linalg.norm(Q,axis=1)-1))),
        'correlation_gram':float(np.max(np.abs(np.corrcoef(X)-Q@Q.T))),
        'pythagoras':float(np.max(np.abs(np.sum(X*X,axis=1)-3*means**2-2*S**2))),
        'A_numeric':float(np.max(np.abs(X[0]-np.array([1,2,3])))),
        'AB_correlation':float(abs(Q[0]@Q[1]-.5))}
    rng=np.random.default_rng(20261109)
    for n in (2,3,5,20):
        Y=rng.normal(size=(n,12));c=Y-Y.mean(axis=0);s=Y.std(axis=0,ddof=1);q=c/np.linalg.norm(c,axis=0)
        errors[f'n{n}_gram']=float(np.max(np.abs(q.T@q-np.corrcoef(Y,rowvar=False))))
        errors[f'n{n}_sd_radius']=float(np.max(np.abs(np.linalg.norm(c/s,axis=0)-np.sqrt(n-1))))
    assert max(errors.values())<1e-12,errors
    manifest={'description':'Original Codex illustrations, deterministic constructed features; not measured data.',
        'n_individuals':3,'features':[{'name':NAMES[j],'color':COLORS[j],'x':X[j].tolist(),'mean':float(means[j]),'sample_sd':float(S[j]),'centered_length':float(radii[j]),'unit_direction':Q[j].tolist()} for j in range(8)],
        'plane_basis':[v1.tolist(),v2.tolist()],'maximum_absolute_errors':errors,
        'normalization':'Euclidean unit length q = c/||c||; sample z scores instead have radius sqrt(n-1).',
        'validation':'Analytic identities plus fixed-data and seeded numerical checks. No inference from simulation.'}
    (OUT/'checks.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('All numerical checks passed; max error',max(errors.values()))

if __name__=='__main__':
    checks();coordinate_figure();centering_figure();scaling_figure();sphere_figure();animation()
    print('Generated 4 SVGs, 4 PNG previews, 1 GIF, and checks.json in',OUT)
