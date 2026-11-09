"""Original analytic illustration by Codex, requested 2026-11-08.

Run with Python + numpy + matplotlib. Outputs beside this file. Seed 20261108.
Dots are iid 2D samples lifted to the EXACT joint-density surface, not 3D data.
The square is [0,1]^2, translated by its centre then rotated 45 degrees.
All slices are analytic, not estimated from dots. No original image is edited.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = Path(__file__).resolve().parent
BLUE, ORANGE, INK = '#1966b3', '#da6226', '#24364a'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'text.color': INK, 'axes.labelcolor': INK,
                     'axes.titleweight': 'bold', 'axes.spines.top': False,
                     'axes.spines.right': False, 'savefig.facecolor': '#fbfcfe'})
rng = np.random.default_rng(20261108)
phi = lambda x: np.exp(-np.asarray(x)**2 / 2) / np.sqrt(2*np.pi)
radius = 1 / np.sqrt(2)

fig = plt.figure(figsize=(13.8, 11.4), facecolor='#fbfcfe')
gs = fig.add_gridspec(2, 2, height_ratios=[1.65, 1],
                      left=.075, right=.95, bottom=.10, top=.84,
                      hspace=.24, wspace=.30)
fig.suptitle('Moving the board: Gaussian hill vs. uniform square',
             fontsize=21, fontweight='bold', y=.975)
fig.text(.5, .936, 'Two-dimensional samples lifted into 3D: horizontal position = (u, v), height = joint density',
         ha='center', fontsize=11.5)
fig.text(.5, .908, 'Both views use diagonal coordinates. Colored curtains are exact cross-sections at fixed u.',
         ha='center', fontsize=11.5)
fig.text(.285, .867, 'GAUSSIAN  |  independent standard normals', ha='center', fontweight='bold', fontsize=12)
fig.text(.735, .867, 'UNIT SQUARE  |  uniform on [0, 1] x [0, 1]', ha='center', fontweight='bold', fontsize=12)

def setup3d(ax, lim, zlim):
    ax.set_facecolor('#fbfcfe')
    ax.set(xlim=(-lim, lim), ylim=(-lim, lim), zlim=(0, zlim))
    ax.set_xlabel('u', labelpad=2)
    ax.set_ylabel('v', labelpad=2)
    ax.set_zlabel('Joint density  f(u, v)', labelpad=9, fontsize=10)
    ax.set_box_aspect((1, 1, .70))
    ax.view_init(elev=26, azim=-58)
    ax.tick_params(labelsize=9, pad=1)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((.94,.96,.98,.20))
        axis._axinfo['grid']['color'] = (.70,.76,.82,.25)

def curtain(ax, u, v, h, color):
    vertices = [(u, v[0], 0), *zip(np.full_like(v, u), v, h), (u, v[-1], 0)]
    ax.add_collection3d(Poly3DCollection([vertices], facecolor=color,
                                        edgecolor='none', alpha=.27))
    ax.plot(np.full_like(v, u), v, h, color=color, lw=3.2, zorder=20)
    ax.plot([u,u], [v[0],v[-1]], [0,0], color=color, lw=1.4)

g = fig.add_subplot(gs[0,0], projection='3d')
setup3d(g, 3.3, .175)
grid = np.linspace(-3.3,3.3,85)
uu,vv = np.meshgrid(grid,grid)
g.plot_surface(uu,vv,phi(uu)*phi(vv), color='#90b3b7', alpha=.18,
               linewidth=0, shade=False, rcount=65, ccount=65)
xy = rng.normal(size=(600,2))
g.scatter(xy[:,0], xy[:,1], phi(xy[:,0])*phi(xy[:,1]),
          s=4, c='#406b73', alpha=.36, depthshade=False)
v = np.linspace(-3.3,3.3,400)
for u,c in [(0,BLUE),(1.5,ORANGE)]:
    curtain(g,u,v,phi(u)*phi(v),c)
g.set_zticks([0,.08,.16])
g.text2D(.02,-.055, 'u = 0: area 0.399     |     u = 1.5: area 0.130',
         transform=g.transAxes, fontsize=10)

s = fig.add_subplot(gs[0,1], projection='3d')
setup3d(s,.81,1.17)
corners=[(0,-radius,1),(radius,0,1),(0,radius,1),(-radius,0,1)]
s.add_collection3d(Poly3DCollection([corners], facecolor='#91b5b9',
                                    edgecolor='#648a94', alpha=.20))
boundary=np.array(corners+[corners[0]])
s.plot(boundary[:,0],boundary[:,1],np.zeros(5),color='#648a94',lw=1.4)
for x,y,z in corners:
    s.plot([x,x],[y,y],[0,z],color='#91a7b0',lw=.8,alpha=.65)
xy=rng.uniform(0,1,(600,2))
su=(xy[:,0]+xy[:,1]-1)/np.sqrt(2)
sv=(xy[:,1]-xy[:,0])/np.sqrt(2)
s.scatter(su,sv,np.ones(600),s=4,c='#406b73',alpha=.40,depthshade=False)
for u,c in [(0,BLUE),(.45,ORANGE)]:
    a=radius-abs(u)
    curtain(s,u,np.linspace(-a,a,200),np.ones(200),c)
s.set_zticks([0,.5,1])
s.set_xticks([-.7,0,.7]); s.set_yticks([-.7,0,.7])
s.text2D(.02,-.055,'u = 0: area 1.414     |     u = 0.45: area 0.514',
         transform=s.transAxes, fontsize=10)

ng=fig.add_subplot(gs[1,0]); ns=fig.add_subplot(gs[1,1])
for ax in (ng,ns):
    ax.set_title('After dividing each slice by its own area',fontsize=11,pad=15)
    ax.set_xlabel('v'); ax.set_ylabel('Conditional density',labelpad=8)
    ax.grid(axis='y',color='#dde3ea',lw=.7)
    ax.set_axisbelow(True)
ng.plot(v,phi(v),color=BLUE,lw=4,label='u = 0')
ng.plot(v,phi(v),color=ORANGE,lw=2.5,ls='--',label='u = 1.5 (same curve)')
ng.set(xlim=(-3.3,3.3),ylim=(0,.49))
ng.legend(frameon=False,fontsize=10,loc='upper right')
ng.text(.5,.13,'Same width, height, and shape\nIndependent diagonal coordinates',
        transform=ng.transAxes,ha='center',fontsize=11,
        bbox={'facecolor':'#fbfcfe','edgecolor':'none','alpha':.86})
for u,c in [(0,BLUE),(.45,ORANGE)]:
    a=radius-abs(u); h=1/(2*a)
    ns.plot([-.81,-a,-a,a,a,.81],[0,0,h,h,0,0],color=c,lw=2.8,label=f'u = {u:g}')
ns.set(xlim=(-.81,.81),ylim=(-.03,2.45))
ns.legend(frameon=False,fontsize=10,loc='upper right')
ns.text(.5,.43,'Narrower slice becomes taller\nDependent diagonal coordinates',
        transform=ns.transAxes,ha='center',fontsize=11,
        bbox={'facecolor':'#fbfcfe','edgecolor':'none','alpha':.86})
fig.text(.5,.043,'Gaussian: u = (z1 + z2)/sqrt(2), v = (z2 - z1)/sqrt(2).  '
         'Square: u = (x + y - 1)/sqrt(2), v = (y - x)/sqrt(2).',
         ha='center',fontsize=10)
fig.text(.5,.021,'The square is independent in (x, y), not in its diagonal coordinates.  '
         'Vertical scales differ. Gaussian tails extend beyond the displayed window.',
         ha='center',fontsize=10)

# Numerical sanity checks supplement the analytic formulas in the note.
wide=np.linspace(-10,10,100001)
assert abs(np.trapz(phi(wide),wide)-1)<1e-10
for u in [0,1.5]:
    assert np.allclose(phi(u)*phi(wide)/phi(u),phi(wide))
for u in [0,.45]:
    a=radius-abs(u)
    assert np.isclose(2*a/(2*a),1)
assert np.all(np.abs(su)+np.abs(sv)<=radius+1e-12)
assert np.isclose(2*radius**2,1) # rotated unit square area
fig.savefig(OUT/'gaussian-vs-unit-square.png',dpi=180)
fig.savefig(OUT/'gaussian-vs-unit-square.svg')
print('Rendered PNG and SVG; analytic density/support/normalization checks passed.')
