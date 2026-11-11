"""Build the offline explorer and a checked static SVG/PNG comparison.

Run: D:/anaconda/python.exe assets/figures/2026-11-11-joint-density/build.py
Requires NumPy, SciPy and Matplotlib for the static figure and quadrature only.
The delivered HTML has no runtime dependencies.
"""
from pathlib import Path
import importlib.util
import json
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, multivariate_normal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[2]
builder_path = VAULT / '.agents/skills/animate-geometry/scripts/build_explorer.py'
spec = importlib.util.spec_from_file_location('offline_explorer_builder', builder_path)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def build_html():
    files = [HERE/name for name in ('body.html', 'explorer.css', 'math.js', 'explorer.js')]
    read = lambda p: p.read_text(encoding='utf-8')
    content = builder.compile_html('Joint density — slice, normalize, average', read(files[0]),
                                   [read(files[1])], [read(p) for p in files[2:]])
    return builder.write_artifact(HERE/'joint-density.html', content, [*files, builder_path])


def check():
    worst_area = worst_mean = worst_variance = worst_ratio = 0.0
    cases = []
    for rho in [-.95, -.8, 0, .8, .95]:
        for mux in [-1.5, 0, 1.5]:
            model = multivariate_normal(mean=[mux,0], cov=[[1,rho],[rho,1]])
            for fixed in [-2.5, -1.3, 0, 1, 2.5]:
                for is_x in [True, False]:
                    marginal = norm.pdf(fixed, loc=0 if is_x else mux)
                    raw = lambda t: model.pdf([t,fixed] if is_x else [fixed,t])
                    mean = mux+rho*fixed if is_x else rho*(fixed-mux)
                    var = 1-rho*rho
                    area = quad(raw, -np.inf, np.inf, epsabs=1e-11)[0]
                    calc_mean = quad(lambda t:t*raw(t)/marginal, -np.inf, np.inf, epsabs=1e-10)[0]
                    calc_var = quad(lambda t:(t-mean)**2*raw(t)/marginal, -np.inf, np.inf, epsabs=1e-10)[0]
                    ratio_error = max(abs(raw(t)/marginal - norm.pdf(t,loc=mean,scale=np.sqrt(var))) for t in np.linspace(-5,5,35))
                    worst_area=max(worst_area,abs(area-marginal));worst_mean=max(worst_mean,abs(calc_mean-mean))
                    worst_variance=max(worst_variance,abs(calc_var-var));worst_ratio=max(worst_ratio,ratio_error)
            weighted=quad(lambda y:(mux+rho*y)*norm.pdf(y),-np.inf,np.inf)[0]
            assert abs(weighted-mux)<1e-10
            cases.append({'rho':rho,'mux':mux,'weighted_mean':weighted,'expected_mean':mux})
    assert max(worst_area,worst_mean,worst_variance,worst_ratio)<1e-8
    result={'method':'Independent scipy multivariate-normal density integration; full real-line integrals.',
            'parameter_cases':cases, 'slice_cases':150,
            'max_errors':dict(slice_area=worst_area,conditional_mean=worst_mean,conditional_variance=worst_variance,pointwise_density_ratio=worst_ratio),
            'screenshot_reference':dict(y0=-1.3,x0=1,rho=.8,mux=0,mean_x=-1.04,mean_y=.8,variance=.36,raw_x_area=float(norm.pdf(-1.3)),raw_y_area=float(norm.pdf(1))),
            'pass':True}
    (HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


def static_figure():
    green,orange,purple='#128768','#d35b34','#7563c5'
    plt.rcParams.update({'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,
                         'axes.labelcolor':'#33453d','text.color':'#23312e','axes.edgecolor':'#b9c7bf'})
    fig=plt.figure(figsize=(12,6.4),layout='constrained')
    grid=fig.add_gridspec(2,3,width_ratios=[1.4,1,1])
    surface=fig.add_subplot(grid[:,0],projection='3d');cx=fig.add_subplot(grid[0,1]);cy=fig.add_subplot(grid[1,1]);weights=fig.add_subplot(grid[:,2])
    rho,y0,x0=.8,-1.3,1.;model=multivariate_normal([0,0],[[1,rho],[rho,1]])
    x=np.linspace(-3.5,3.5,55);X,Y=np.meshgrid(x,x);Z=model.pdf(np.stack([X,Y],axis=-1))
    surface.plot_wireframe(X,Y,Z,rstride=3,cstride=3,color='#859189',alpha=.38,linewidth=.6)
    surface.plot(x,np.full_like(x,y0),model.pdf(np.column_stack([x,np.full_like(x,y0)])),color=green,lw=2.5)
    surface.plot(np.full_like(x,x0),x,model.pdf(np.column_stack([np.full_like(x,x0),x])),color=orange,lw=2.5)
    surface.plot(x,np.full_like(x,3.5),norm.pdf(x),color=purple,lw=1.6)
    surface.plot(np.full_like(x,-3.5),x,norm.pdf(x),color=purple,lw=1.6)
    surface.plot(rho*x,x,np.zeros_like(x),color=green,ls='--',lw=1.6)
    surface.set(xlabel='x',ylabel='y',zlabel='density',title='A joint surface and two raw slices',zlim=(0,.45))
    surface.view_init(elev=27,azim=-58);surface.set_box_aspect((1,1,.65))
    for ax,fixed,mean,color,is_x in [(cx,y0,rho*y0,green,True),(cy,x0,rho*x0,orange,False)]:
        t=np.linspace(-4,4,500);conditional=norm.pdf(t,loc=mean,scale=.6);raw=conditional*norm.pdf(fixed)
        ax.fill_between(t,conditional,color=color,alpha=.18);ax.plot(t,conditional,color=color,lw=2,label='conditional')
        ax.plot(t,raw,color=color,ls='--',lw=1.5,label='raw slice');ax.axvline(mean,color=color,ls=':',alpha=.8)
        ax.set(xlim=(-4,4),ylim=(0,.75),xlabel='x' if is_x else 'y',ylabel='density',title=f'{"X | Y" if is_x else "Y | X"} = {fixed:g}: N({mean:.2f}, 0.36)\nRaw area {norm.pdf(fixed):.3f} → conditional area 1')
        ax.title.set_fontsize(10)
        ax.grid(alpha=.13)
    yy=np.linspace(-3.5,3.5,200);weights.plot(yy,rho*yy,color=green,lw=2);yb=np.arange(-3,3.01,.5)
    weights.scatter(yb,rho*yb,s=norm.pdf(yb)*400,color=green,alpha=.4);weights.scatter([y0],[rho*y0],color=green,s=35,zorder=5)
    weights.axhline(0,color=purple,ls='--',lw=1.6);weights.set(xlabel='conditioning value y',ylabel='conditional mean m(y)',title='Weight the balance points',xlim=(-3.5,3.5),ylim=(-3.2,3.2))
    weights.text(.04,.96,'m(y) = 0.8y\n∫ m(y) pY(y) dy = 0',transform=weights.transAxes,va='top');weights.grid(alpha=.13)
    fig.suptitle('Slice → normalize → average   |   ρ = 0.8, μₓ = μᵧ = 0, variances = 1',fontsize=15)
    fig.get_layout_engine().set(rect=(0,.06,1,.93))
    fig.text(.5,.015,'Original analytic reconstruction. Dot areas show relative equal-width-bin weights. Finite plot windows; integrals are over the full support.',ha='center',fontsize=9,color='#63736e')
    for suffix in ('svg','png'):fig.savefig(HERE/f'overview.{suffix}',dpi=160)
    plt.close(fig)


if __name__=='__main__':
    build_html(); result=check();static_figure()
    print(json.dumps({'pass':result['pass'],'max_errors':result['max_errors'],'html':'joint-density.html'}))
