"""Execute the actual note examples and cross-check their numerical meaning."""
from pathlib import Path
import json
import re
import subprocess
import tempfile
import numpy as np

OUT = Path(__file__).parent
ROOT = OUT.parents[2]
note = ROOT / 'Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/Principal component analysis.md'
text = note.read_text(encoding='utf-8')
unquoted = '\n'.join('' if line == '>' else line[2:] if line.startswith('> ') else line for line in text.splitlines())
python_code = re.search(r'```python\n(.*?)\n```', unquoted, re.S).group(1)
r_code = re.search(r'```r\n(.*?)\n```', unquoted, re.S).group(1)
scope = {}
exec(compile(python_code, str(note), 'exec'), scope)
assert np.allclose(scope['pca'].explained_variance_ratio_, 91/97)
assert np.allclose(scope['pca'].explained_variance_, 182/11)
assert np.isclose(np.sum((scope['X']-scope['X_hat'])**2),12)

with tempfile.TemporaryDirectory(prefix='pca-note-', dir=r'D:\CodexStorage\temp') as td:
    rfile = Path(td)/'example.R'
    rfile.write_text(r_code + '\nstopifnot(abs(fit$sdev[1]^2 - 182/11) < 1e-10, abs(sum((X-X_hat)^2)-12)<1e-10)\ncat("R_EXAMPLE_PASS\\n")\n',encoding='utf-8')
    run = subprocess.run([r'D:\R-4.4.1\bin\Rscript.exe', str(rfile)],capture_output=True,text=True,check=True)
    assert 'R_EXAMPLE_PASS' in run.stdout
    print(run.stdout)

js = r"""
const m=require(process.argv[1]);
let max=0;
for(let angle=0;angle<=180;angle++){
 const s=m.project(angle), d=(angle-45)*Math.PI/180;
 const expected=(182*Math.cos(d)**2+12*Math.sin(d)**2)/11;
 max=Math.max(max,Math.abs(s.variance-expected),Math.abs(s.variance+s.error-194/11));
 if(!Number.isFinite(s.fraction)||s.fraction<0||s.fraction>1)throw Error('bad fraction');
}
if(max>1e-10)throw Error('projection mismatch');
console.log(JSON.stringify({angles:181,max_error:max}));
"""
js_run = subprocess.run(['node','-e',js,str(OUT/'math.js')],capture_output=True,text=True,check=True)
browser_math = json.loads(js_run.stdout)

# Independently compare eigen- and SVD reconstructions for rectangular and deficient data.
rng=np.random.default_rng(17)
errors=[]
for shape in [(9,3),(4,8),(12,2)]:
    A=rng.normal(size=shape); A-=A.mean(axis=0)
    if shape==(12,2): A[:,1]=2*A[:,0]
    U,s,Vt=np.linalg.svd(A,full_matrices=False)
    eig,Q=np.linalg.eigh(A.T@A/(shape[0]-1))
    errors.append(float(np.max(np.abs(eig[::-1][:len(s)]-s*s/(shape[0]-1)))))
    for k in range(1,min(shape)):
        reconstructed=(A@Vt[:k].T)@Vt[:k]
        errors.append(float(abs(np.sum((A-reconstructed)**2)-np.sum(s[k:]**2))))
assert max(errors)<1e-10

# Check normalization in the displayed t-SNE formulas (off-diagonal pairs only).
dist=np.array([[0,1,4],[1,0,9],[4,9,0]],float)
weights=np.exp(-dist/2); np.fill_diagonal(weights,0)
conditional=weights/weights.sum(axis=1,keepdims=True)
P=(conditional+conditional.T)/(2*len(dist))
Q=1/(1+dist);np.fill_diagonal(Q,0);Q/=Q.sum()
assert np.isclose(P.sum(),1) and np.isclose(Q.sum(),1)
assert np.allclose(P,P.T) and np.allclose(Q,Q.T)
assert np.sum(P[P>0]*np.log(P[P>0]/Q[P>0]))>=0
records={'python_note_example':'PASS (scikit-learn 1.4.2)',
         'R_note_example':'PASS (R 4.4.1)',
         'interactive_math':browser_math,
         'rectangular_rank_deficient_max_error':max(errors),
         'tSNE_pair_distribution_sums':[float(P.sum()),float(Q.sum())]}
(OUT/'example-checks.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,indent=2))
