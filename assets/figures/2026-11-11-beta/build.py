"""Reproduce offline HTML, static SVG/PNG views and independent numerical checks.

Run with Python + numpy/scipy/matplotlib; Node must be on PATH.
Example: D:/anaconda/python.exe D:/obsidian_centre/stats_ML_rebuild/assets/figures/2026-11-11-beta/build.py
No originals, plugin files or other figures are modified.
"""
from pathlib import Path
import importlib.util
import json
import subprocess
import xml.etree.ElementTree as ET
import numpy as np
from scipy.special import betaln
from scipy.stats import beta
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUILDER = ROOT / '.agents/skills/animate-geometry/scripts/build_explorer.py'
spec = importlib.util.spec_from_file_location('packer', BUILDER)
packer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packer)

for mode in ['shapes', 'update']:
    files = [HERE / f'{mode}-body.html', HERE / 'explorer.css', HERE / 'math.js', HERE / 'explorer.js']
    body, css, math_js, ui_js = [p.read_text(encoding='utf-8') for p in files]
    html = packer.compile_html(f'Beta: {mode}', body, [css], [math_js, ui_js])
    packer.write_artifact(HERE / f'{mode}.html', html, [*files, BUILDER])

# Evaluate the actual browser math in Node, compare with independent SciPy implementations.
js = r"""
const m=require(process.argv[1]);
const shapes=[.25,.5,.75,1,1.25,2,5,10,20,50.25,70];
const xs=[1e-8,1e-5,.001,.01,.05,.1,.25,.5,.75,.9,.95,.99,.999,1-1e-5,1-1e-8];
const density=[],moments=[],updates=[];
for(const a of shapes)for(const b of shapes){
 moments.push([a,b,m.logBeta(a,b),m.mean(a,b),m.variance(a,b)]);
 for(const x of xs)density.push([x,a,b,m.pdf(x,a,b)]);
 for(const s of [0,1,3,30,50])for(const f of [0,1,10,50])updates.push([a,b,s,f,m.posterior(a,b,s,f)]);
}
if(m.pdf(0,.5,2)!==Infinity||m.pdf(1,2,.5)!==Infinity||m.pdf(0,1,3)!==3||m.pdf(1,3,1)!==3||m.pdf(0,2,2)!==0||m.pdf(1,2,2)!==0)throw Error('Endpoint failure');
console.log(JSON.stringify({density,moments,updates}));
"""
result = subprocess.run(['node', '-e', js, str(HERE / 'math.js')], check=True, capture_output=True, text=True)
data = json.loads(result.stdout)
pdf_err = max(abs(y-beta.pdf(x,a,b))/max(1,abs(beta.pdf(x,a,b))) for x,a,b,y in data['density'])
moment_err = max(max(abs(lb-betaln(a,b)),abs(m-beta.mean(a,b)),abs(v-beta.var(a,b))) for a,b,lb,m,v in data['moments'])
update_err=0.
for a,b,s,f,p in data['updates']:
    assert p['a']==a+s and p['b']==b+f
    update_err=max(update_err,abs(p['mean']-beta.mean(a+s,b+f)),abs(p['sd']-beta.std(a+s,b+f)))
    if s+f:
        assert abs(p['mean']-((a+b)/(a+b+s+f)*a/(a+b)+(s+f)/(a+b+s+f)*s/(s+f)))<1e-14
    assert abs(p['mean']-np.exp(betaln(a+s+1,b+f)-betaln(a+s,b+f)))<2e-12
    # Multiplication followed by normalization: test at a non-boundary p.
    x=.37
    lhs=np.log(beta.pdf(x,a,b))+s*np.log(x)+f*np.log1p(-x)-(betaln(a+s,b+f)-betaln(a,b))
    rhs=beta.logpdf(x,a+s,b+f)
    assert abs(lhs-rhs)<2e-11
assert pdf_err<1e-10 and moment_err<1e-10 and update_err<1e-12

# Endpoint-aware quadrature, independent of log-gamma code.
quadrature=[]
for a,b in [(1,1),(.25,.25),(.25,20),(20,.25),(2,2),(4,2),(10,10),(31,11),(70,70)]:
    vals=[]
    for k in [0,1,2]:
        if min(a,b)<1:
            value,error=quad(lambda x:x**k,0,1,weight='alg',wvar=(a-1,b-1),epsabs=1e-12,epsrel=2e-11,limit=200)
            vals.append(value/np.exp(betaln(a,b)))
        else:
            value,error=quad(lambda x:x**k*np.exp((a-1)*np.log(x)+(b-1)*np.log1p(-x)-betaln(a,b)),0,1,epsabs=1e-12,epsrel=2e-11,limit=200)
            vals.append(value)
    err=max(abs(vals[0]-1),abs(vals[1]-beta.mean(a,b)),abs(vals[2]-beta.moment(2,a,b)))
    assert err<1e-9
    quadrature.append({'alpha':a,'beta':b,'maximum_error':err})
assert abs(quad(lambda p:20*p**3*(1-p),0,1)[0]-1)<1e-14
assert abs(quad(lambda p:p*20*p**3*(1-p),0,1)[0]-2/3)<1e-14

# Static original illustrations, deliberately not screenshots of controls.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'beta-2026-11-11'})
bg='#121c2d'; fg='#eaf0fa'; cyan='#55dbe2'; orange='#ffbf69'
x=np.linspace(0,1,1001)
def axes(title):
    fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
    fig.patch.set_facecolor(bg);ax.set_facecolor(bg)
    ax.tick_params(colors=fg)
    for spine in ax.spines.values():spine.set_color('#8da2bd')
    ax.set(xlim=(0,1),ylim=(0,4),xlabel='p — chance of heads',ylabel='Probability density',title=title)
    ax.xaxis.label.set_color(fg);ax.yaxis.label.set_color(fg);ax.title.set_color(fg)
    ax.grid(alpha=.16,color=fg)
    return fig,ax
fig,ax=axes('Start flat, then change the shape')
for a,b,color,label in [(1,1,cyan,'Beta(1, 1): uniform'),(2,2,'#c4a1ff','Beta(2, 2): middle'),(8,2,orange,'Beta(8, 2): high p')]:
    ax.plot(x,beta.pdf(x,a,b),color=color,lw=2.5,label=label)
ax.legend(facecolor=bg,labelcolor=fg,edgecolor='#536983',loc='upper left')
for ext in ['svg','png']:fig.savefig(HERE/f'shapes.{ext}',dpi=150)
plt.close(fig)
fig,ax=axes('3 heads + 1 tail: add counts to the prior parameters')
for a,b,color,label,style in [(1,1,cyan,'Prior: Beta(1, 1)','--'),(4,2,orange,'Posterior: Beta(4, 2)','-')]:
    ax.plot(x,beta.pdf(x,a,b),color=color,lw=2.5,label=label,linestyle=style)
    ax.axvline(a/(a+b),color=color,ls=':',lw=1.8)
ax.text(.49,3.05,'Prior mean\n0.5',color=cyan,ha='right')
ax.text(2/3+.012,2.6,'Posterior mean\n2/3',color=orange)
ax.legend(facecolor=bg,labelcolor=fg,edgecolor='#536983',loc='upper left')
for ext in ['svg','png']:fig.savefig(HERE/f'update.{ext}',dpi=150)
plt.close(fig)
for name in ['shapes','update']:ET.parse(HERE/f'{name}.svg')
report={'pass':True,'density_values_compared':len(data['density']),'density_max_scaled_error':pdf_err,'moment_parameter_pairs':len(data['moments']),'moments_max_absolute_error':moment_err,'posterior_cases':len(data['updates']),'posterior_max_absolute_error':update_err,'endpoint_limits':'PASS','normalization_and_moments_quadrature':quadrature,'coin_example_integrals':'PASS','svg_xml':'PASS','scope':'Independent numerical support; analytic proof is in the note. Browser/live-app checks recorded separately.'}
(HERE/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
# Normalize generated text for Git; Matplotlib emits trailing spaces in SVG paths.
# This changes whitespace only, not path commands, numerical values or HTML hashes.
for generated in [HERE/'shapes.svg', HERE/'update.svg', HERE/'checks.json', HERE/'shapes.build.json', HERE/'update.build.json']:
    generated.write_bytes(('\n'.join(line.rstrip() for line in generated.read_text(encoding='utf-8').splitlines())+'\n').encode('utf-8'))
print(json.dumps(report,indent=2))
