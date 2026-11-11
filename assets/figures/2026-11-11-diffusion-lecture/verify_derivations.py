"""Independent numerical checks of algebra expanded from the supplied lecture.
Run with Python + NumPy + SciPy. The examples here are verification fixtures,
not additional learning sources or claims that these numbers appear in the PDF.
"""
from pathlib import Path
from itertools import product
import json
import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.stats import norm
from scipy.integrate import quad

OUT = Path(__file__).resolve().parent
report = {}

# The exact schedule specified on slide 20.
b = np.linspace(1e-4, .02, 1000)
a = 1-b
ab = np.cumprod(a)
v = 0.
max_forward_error = 0.
for t in range(1000):
    v = a[t]*v+b[t]
    max_forward_error = max(max_forward_error, abs(v-(1-ab[t])))
assert max_forward_error < 1e-13
report['slide20_schedule'] = {'alpha_bar_T': float(ab[-1]),
    'signal_coefficient': float(np.sqrt(ab[-1])), 'noise_coefficient': float(np.sqrt(1-ab[-1])),
    'maximum_variance_recursion_error': max_forward_error}

# Check the raw trajectory objective and local-KL decomposition with
# independent Gaussian quadratures. Nonlinear reverse means are deliberate.
b = np.array([.1,.2,.3]); a = 1-b; ab = np.cumprod(a)
x0 = .7
def mean_model(z,t):
    return .6*z + .1*z*z + .03*t
def bridge(z,t):
    prev = ab[t-1]
    vv = (1-prev)*b[t]/(1-ab[t])
    mm = (np.sqrt(a[t])*(1-prev)*z + np.sqrt(prev)*b[t]*x0)/(1-ab[t])
    return mm,vv
def gkl(mq,vq,mp,vp):
    return .5*(np.log(vp/vq)-1+(vq+(mq-mp)**2)/vp)
nodes,weights = hermgauss(14)
nodes = np.sqrt(2)*nodes; weights = weights/np.sqrt(np.pi)
raw_loss = 0.
factor_error = 0.
for inds in product(range(len(nodes)), repeat=3):
    xs = [x0]; w = 1.
    log_forward = 0.; log_reverse = 0.
    for t,i in enumerate(inds):
        w *= weights[i]
        z = np.sqrt(a[t])*xs[-1]+np.sqrt(b[t])*nodes[i]
        log_forward += norm.logpdf(z,np.sqrt(a[t])*xs[-1],np.sqrt(b[t]))
        log_reverse += norm.logpdf(xs[-1],mean_model(z,t),np.sqrt(b[t]))
        xs.append(z)
    raw_loss += w*(log_forward-log_reverse-norm.logpdf(xs[-1]))
    reverse_factored_q = norm.logpdf(xs[-1],np.sqrt(ab[-1])*x0,np.sqrt(1-ab[-1]))
    for t in range(1,3):
        mm,vv = bridge(xs[t+1],t)
        reverse_factored_q += norm.logpdf(xs[t],mm,np.sqrt(vv))
    factor_error = max(factor_error,abs(log_forward-reverse_factored_q))
terminal = gkl(np.sqrt(ab[-1])*x0,1-ab[-1],0.,1.)
reconstruction = sum(
    -w*norm.logpdf(x0,mean_model(np.sqrt(ab[0])*x0+np.sqrt(1-ab[0])*z,0),np.sqrt(b[0]))
    for z,w in zip(nodes,weights))
locals_ = []
for t in range(1,3):
    value = 0.
    for z,w in zip(nodes,weights):
        xt = np.sqrt(ab[t])*x0+np.sqrt(1-ab[t])*z
        mm,vv = bridge(xt,t)
        value += w*gkl(mm,vv,mean_model(xt,t),b[t])
    locals_.append(float(value))
decomposed = terminal+reconstruction+sum(locals_)
assert abs(raw_loss-decomposed) < 1e-11
assert factor_error < 1e-10
report['elbo'] = {'path_loss':float(raw_loss),'decomposed_loss':float(decomposed),
    'difference':float(abs(raw_loss-decomposed)),'maximum_q_factorization_error':factor_error,
    'terminal_kl':float(terminal),'reconstruction':float(reconstruction),'local_kls':locals_}

# Independent Bayes-density check of the bridge and the noise parameterization.
xt = -.3; t=2; mm,vv = bridge(xt,t)
denom = norm.pdf(xt,np.sqrt(ab[t])*x0,np.sqrt(1-ab[t]))
def bayes(u):
    return norm.pdf(xt,np.sqrt(a[t])*u,np.sqrt(b[t]))*norm.pdf(u,np.sqrt(ab[t-1])*x0,np.sqrt(1-ab[t-1]))/denom
mass=quad(bayes,-np.inf,np.inf)[0]
numeric_mean=quad(lambda u:u*bayes(u),-np.inf,np.inf)[0]
numeric_var=quad(lambda u:(u-mm)**2*bayes(u),-np.inf,np.inf)[0]
kl_quad=quad(lambda u:bayes(u)*(norm.logpdf(u,mm,np.sqrt(vv))-norm.logpdf(u,mean_model(xt,t),np.sqrt(b[t]))),-np.inf,np.inf)[0]
kl_closed=gkl(mm,vv,mean_model(xt,t),b[t])
assert max(abs(mass-1),abs(numeric_mean-mm),abs(numeric_var-vv),abs(kl_quad-kl_closed))<1e-10
eps=(xt-np.sqrt(ab[t])*x0)/np.sqrt(1-ab[t])
mean_noise=(xt-b[t]*eps/np.sqrt(1-ab[t]))/np.sqrt(a[t])
eps_hat=.4
model_noise=(xt-b[t]*eps_hat/np.sqrt(1-ab[t]))/np.sqrt(a[t])
mean_error=(mm-model_noise)**2/(2*b[t])
noise_error=b[t]**2/(2*b[t]*a[t]*(1-ab[t]))*(eps-eps_hat)**2
assert abs(mean_noise-mm)<1e-13 and abs(mean_error-noise_error)<1e-13
report['bridge_and_noise']={'mass':mass,'mean':float(mm),'variance':float(vv),
    'kl_quadrature_error':abs(kl_quad-kl_closed),'mean_noise_equivalence_error':abs(mean_noise-mm),
    'weighted_loss_equivalence_error':abs(mean_error-noise_error)}

# Guidance: Bayes gradient with a nonuniform class prior; p(y) must be retained
# in the density equation even though its derivative with respect to x is zero.
prior=.3
def noisy_density(x): return prior*norm.pdf(x,1.,.8)+(1-prior)*norm.pdf(x,-.6,1.1)
def posterior_y(x): return prior*norm.pdf(x,1.,.8)/noisy_density(x)
def derivative(f,x,h=1e-5): return (f(x+h)-f(x-h))/(2*h)
max_bayes_gradient_error=0.
for x in np.linspace(-2.,2.,21):
    lhs=derivative(lambda u:np.log(posterior_y(u)),x)
    rhs=-(x-1.)/.8**2-derivative(lambda u:np.log(noisy_density(u)),x)
    max_bayes_gradient_error=max(max_bayes_gradient_error,abs(lhs-rhs))
assert max_bayes_gradient_error<1e-8

# A linear log-likelihood tilt has exactly the covariance-scaled mean shift.
mu=.2; var=.4; strength=1.7; gradient=.8
def tilted_unnormalized(u): return norm.pdf(u,mu,np.sqrt(var))*np.exp(strength*gradient*(u-mu))
normalizer=quad(tilted_unnormalized,-12,12)[0]
shifted=quad(lambda u:u*tilted_unnormalized(u),-12,12)[0]/normalizer
expected=mu+strength*var*gradient
assert abs(shifted-expected)<1e-10

# For Gaussian clean data, the optimal noise prediction / score relation can
# also be evaluated independently using a joint Gaussian conditional mean.
abar=.37; data_mu=.8; data_var=1.3; x=.25
noisy_var=abar*data_var+1-abar
noise_cond_mean=np.sqrt(1-abar)/noisy_var*(x-np.sqrt(abar)*data_mu)
score=-(x-np.sqrt(abar)*data_mu)/noisy_var
assert abs(score+noise_cond_mean/np.sqrt(1-abar))<1e-13
report['guidance']={'max_bayes_score_error':max_bayes_gradient_error,
    'tilted_mean_numeric':shifted,'tilted_mean_formula':expected,
    'noise_score_relation_error':float(abs(score+noise_cond_mean/np.sqrt(1-abar)))}
report['result']='PASS'
(OUT/'derivation-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
