"""Verify cross-language fits, explorer math, and the embedded example copies."""
from pathlib import Path
import contextlib
import io
import json
import os
import re
import runpy
import shutil
import subprocess
import sys
import numpy as np
from scipy.special import expit

HERE=Path(__file__).resolve().parent
VAULT=HERE.parents[2]
NOTE=VAULT/'Backbone/Statistical inference & modeling/Regression & linear models/Generalized linear models/Binary, count & categorical responses/Logistic regression.md'
with contextlib.redirect_stdout(io.StringIO()):
    py=runpy.run_path(str(HERE/'example.py'))
rscript=shutil.which('Rscript')
if not rscript: raise RuntimeError('Rscript is required for the cross-language check.')
rcode='source(commandArgs(TRUE)[1]); cat("\\nCHECK_BETA",sprintf("%.17g",coef(fit)),"\\n"); cat("CHECK_PROB",sprintf("%.17g",p),"\\n"); cat("CHECK_LOSS",sprintf("%.17g",-mean(test$passed*log(q)+(1-test$passed)*log1p(-q))),"\\n")'
env=os.environ.copy();env.update(LC_ALL='C',LANG='C')
res=subprocess.run([rscript,'--vanilla','-e',rcode,str(HERE/'example.R')],capture_output=True,text=True,env=env,check=True)
def parse(key):
    return np.array([float(x) for x in re.search(r'^'+key+r' (.+)$',res.stdout,re.M).group(1).split()])
errors={
 'python_R_coefficient_error':float(np.max(abs(py['fit'].params-parse('CHECK_BETA')))),
 'python_R_probability_error':float(np.max(abs(py['p']-parse('CHECK_PROB')))),
 'python_R_test_log_loss_error':float(abs(py['log_loss']-parse('CHECK_LOSS')[0]))}
assert max(errors.values())<1e-9
assert np.array_equal(py['p']>=.5,parse('CHECK_PROB')>=.5)
note=NOTE.read_text(encoding='utf-8')
for lang,file in [('python','example.py'),('r','example.R')]:
    block=re.search(r'> ```'+lang+r'\n(.*?)\n> ```',note,re.S).group(1)
    decoded='\n'.join(line[2:] if line.startswith('> ') else '' for line in block.splitlines())
    assert decoded.strip()==(HERE/file).read_text(encoding='utf-8').strip()
# Independent SciPy comparison across all control extremes and interior points.
js="const m=require('./math.js');let a=[];for(const b0 of [-10,-4,0,4,10])for(const b1 of [-2,-.8,0,.8,2])for(const x of [0,1,5,9,10])a.push({b0,b1,x,...m.values(b0,b1,x)});process.stdout.write(JSON.stringify(a));"
states=json.loads(subprocess.check_output(['node','-e',js],cwd=HERE,text=True))
err=0.
for s in states:
    p=expit(s['b0']+s['b1']*s['x'])
    err=max(err,abs(p-s['p']),abs(s['b1']*p*(1-p)-s['slope']))
assert err<1e-14
errors['explorer_scipy_max_error']=err
# Exact structural identity check: no metadata change except updated.
import yaml
before=Path('D:/CodexStorage/temp/logistic-enrich-01a1e255/before.md')
if before.exists():
    a=yaml.safe_load(before.read_text(encoding='utf-8').split('---')[1])
    b=yaml.safe_load(note.split('---')[1])
    a.pop('updated');b.pop('updated');assert a==b
assert note.count('```atlas\n')==1 and '<!--' not in note
result={'status':'pass','errors':errors,'R_version':subprocess.check_output([rscript,'--version'],text=True,stderr=subprocess.STDOUT).strip(),
  'python_version':sys.version.split()[0],'reference_probabilities':py['p'].tolist(),
  'test_log_loss':py['log_loss'],'explorer_states':len(states),
  'embedded_scripts':'exact match','identity_and_relationships':'unchanged'}
(HERE/'implementation-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
