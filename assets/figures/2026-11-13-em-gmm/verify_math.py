"""Independent SciPy/NumPy checks against the JavaScript states produced by build.py."""
from pathlib import Path
import itertools
import json
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_normal

HERE = Path(__file__).resolve().parent
record = json.loads((HERE/'model-states.json').read_text(encoding='utf-8'))
xs = np.asarray(record['data'])


def log_joint(data, p):
    return np.column_stack([np.log(p['weights'][k])+multivariate_normal.logpdf(data,mean=p['means'][k],cov=p['covs'][k]) for k in range(2)])


errors = {'responsibilities':0.0,'weights':0.0,'means':0.0,'covariances':0.0,'likelihood':0.0,'elbo_tightness':0.0,'ellipse_radius':0.0,'mean_gradient':0.0}
finite_difference_errors = {'precision_gradient':0.0,'mixing_weight_gradient':0.0}
for trans in record['transitions']:
    p=trans['old'];new=trans['new'];r=np.asarray(trans['r']);logs=log_joint(xs,p)
    lse=logsumexp(logs,axis=1);expected_r=np.exp(logs-lse[:,None]);counts=r.sum(axis=0)
    mus=r.T@xs/counts[:,None]
    covs=np.array([((xs-mus[k])*r[:,k,None]).T@(xs-mus[k])/counts[k] for k in range(2)])
    for key,value in [('responsibilities',r-expected_r),('weights',np.asarray(new['weights'])-counts/len(xs)),('means',np.asarray(new['means'])-mus),('covariances',np.asarray(new['covs'])-covs)]:
        errors[key]=max(errors[key],float(np.abs(value).max()))
    entropy=-np.sum(r*np.log(np.maximum(r,1e-300)));q=np.sum(r*logs)
    errors['elbo_tightness']=max(errors['elbo_tightness'],float(abs(q+entropy-lse.sum())))
    # At the weighted optimum, each mean score vanishes (analytic first-order condition).
    for k in range(2):
        gradient=np.linalg.solve(np.asarray(new['covs'][k]),(r[:,k,None]*(xs-mus[k])).sum(axis=0))
        errors['mean_gradient']=max(errors['mean_gradient'],float(abs(gradient).max()))
        # Symmetric precision perturbations also check the off-diagonal factor of two.
        scatter=counts[k]*covs[k]
        precision=np.linalg.inv(covs[k]*1.15)
        matrix_gradient=counts[k]/2*np.linalg.inv(precision)-scatter/2
        def precision_objective(lam):
            return counts[k]/2*np.linalg.slogdet(lam)[1]-.5*np.trace(lam@scatter)
        for direction in [np.diag([1.,0.]),np.diag([0.,1.]),np.array([[0.,1.],[1.,0.]])]:
            h=1e-5
            fd=(precision_objective(precision+h*direction)-precision_objective(precision-h*direction))/(2*h)
            exact=float(np.sum(matrix_gradient*direction))
            finite_difference_errors['precision_gradient']=max(finite_difference_errors['precision_gradient'],abs(float(fd)-exact))
    w=.37;h=1e-5
    weight_objective=lambda w:counts[0]*np.log(w)+counts[1]*np.log(1-w)
    fd=(weight_objective(w+h)-weight_objective(w-h))/(2*h)
    exact=counts[0]/w-counts[1]/(1-w)
    finite_difference_errors['mixing_weight_gradient']=max(finite_difference_errors['mixing_weight_gradient'],abs(float(fd)-exact))
    assert abs(counts[0]/new['weights'][0]-counts[1]/new['weights'][1])<1e-10
    assert logsumexp(log_joint(xs,new),axis=1).sum() >= lse.sum()-1e-8
    assert np.sum(r*log_joint(xs,new))>=q-1e-8

for snap in record['snapshots']:
    p=snap['p'];ll=logsumexp(log_joint(xs,p),axis=1).sum()
    errors['likelihood']=max(errors['likelihood'],float(abs(ll-snap['logLikelihood'])))
    for cov in p['covs']:
        c=np.asarray(cov);t=np.linspace(0,2*np.pi,173)
        for radius in [1,2]:
            d=radius*np.linalg.cholesky(c)@np.array([np.cos(t),np.sin(t)])
            quadratic=np.einsum('in,ij,jn->n',d,np.linalg.inv(c),d)
            errors['ellipse_radius']=max(errors['ellipse_radius'],float(abs(quadratic-radius**2).max()))

# Enumerate all 2^3 assignments to check the general Q over whole Z against the n,k formula.
small=np.asarray(record['small']['data']);p=record['small']['p'];logs=log_joint(small,p)
assignments=list(itertools.product(range(2),repeat=3))
complete=np.array([sum(logs[n,k] for n,k in enumerate(z)) for z in assignments])
posterior=np.exp(complete-logsumexp(complete));r=np.exp(logs-logsumexp(logs,axis=1)[:,None])
general_q=float(posterior@complete);gmm_q=float(np.sum(r*logs))
errors['whole_assignment_Q']=abs(general_q-gmm_q)
errors['marginal_factorization']=float(abs(logsumexp(complete)-logsumexp(logs,axis=1).sum()))
assert max(errors.values())<1e-8,errors
assert max(finite_difference_errors.values())<1e-6,finite_difference_errors
assert len(record['runs'])==36
assert all(r['stop'] is None for r in record['runs']),record['runs']
report={'result':'PASS','independent_reference':'SciPy multivariate_normal and NumPy weighted moments; exhaustive 8-state latent sum; symmetric-precision and constrained-weight finite differences','max_absolute_errors':errors,'finite_difference_errors':finite_difference_errors,'finite_difference_tolerance':1e-6,'js_checks':record['jsChecks'],'initialization_grid_runs':36,'iterations_per_run':60,'source_boundary':'Original deterministic data; not recovered lecture data. Numerical checks support the analytic derivation.'}
(HERE/'math-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
