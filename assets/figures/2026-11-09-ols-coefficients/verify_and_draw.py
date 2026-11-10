"""Reproduce the OLS example, independent algebra checks, and original figure.

Run with Python + numpy, sympy, matplotlib. No original source file is edited.
The right panel is an isometric coordinate view of the centered observation
plane, with basis u=x_c/||x_c||, v=e/||e||. It is not the x-y data plot.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
X = sp.Matrix([[1, 1], [1, 2], [1, 3]])
y = sp.Matrix([1, 2, 2])
G = X.T * X
b = G.inv() * X.T * y
H = X * G.inv() * X.T
e = y - X*b
assert b == sp.Matrix([sp.Rational(2, 3), sp.Rational(1, 2)])
assert e == sp.Matrix([-1, 2, -1])/6
assert e.dot(e) == sp.Rational(1, 6)
assert X.T*e == sp.zeros(2, 1)
assert H == H.T and H*H == H
assert (sp.eye(3)-H)*y == e
a, d = sp.symbols("a d", real=True)
v = sp.Matrix([a, d])
loss = (y-X*v).dot(y-X*v)
assert sp.Matrix([sp.diff(loss, z) for z in (a,d)]) == 2*G*v-2*X.T*y
assert sp.simplify(loss-e.dot(e)-(v-b).dot(G*(v-b))) == 0
C = sp.eye(3)-sp.ones(3)/3
xc, yc = C*X[:,1], C*y
assert xc.dot(xc) == 2 and xc.dot(yc) == 1
assert yc.dot(yc) == sp.Rational(2,3)
assert (X[:,1].dot(X[:,1])*3 - sum(X[:,1])**2) == 3*xc.dot(xc)

rng = np.random.default_rng(9012026)
Z = rng.normal(size=(24,3)) + np.array([2., -1., 4.])
XX = np.column_stack([np.ones(len(Z)), Z])
yy = rng.normal(size=len(Z))
bb, _, _, _ = np.linalg.lstsq(XX, yy, rcond=None)
Q, R = np.linalg.qr(XX, mode="reduced")
U, singular, Vt = np.linalg.svd(XX, full_matrices=False)
alternatives = {
    "normal_equations": np.linalg.solve(XX.T@XX, XX.T@yy),
    "QR": np.linalg.solve(R, Q.T@yy),
    "SVD": Vt.T @ ((U.T@yy)/singular),
}
Zc, yyc = Z-Z.mean(axis=0), yy-yy.mean()
S = Zc.T@Zc/(len(Z)-1)
s = Zc.T@yyc/(len(Z)-1)
slopes = np.linalg.solve(S,s)
alternatives["covariance"] = np.r_[yy.mean()-Z.mean(axis=0)@slopes,slopes]
fwl = []
for j in range(XX.shape[1]):
    W = np.delete(XX,j,axis=1)
    M = np.eye(len(XX))-W@np.linalg.solve(W.T@W,W.T)
    r, ry = M@XX[:,j], M@yy
    fwl.append(r@ry/(r@r))
alternatives["FWL"] = np.array(fwl)
candidate = rng.normal(size=XX.shape[1])
alternatives["Newton_one_step"] = candidate - np.linalg.solve(XX.T@XX, XX.T@(XX@candidate-yy))
gd = np.zeros(XX.shape[1])
eta = 1/np.linalg.eigvalsh(XX.T@XX)[-1]
for iteration in range(30000):
    gd -= eta * (XX.T@(XX@gd-yy))
    if np.linalg.norm(gd-bb) < 1e-10:
        break
alternatives["gradient_descent"] = gd
errors = {name: float(np.max(np.abs(value-bb))) for name,value in alternatives.items()}
assert max(errors.values()) < 1e-9, errors
G_reconstructed = np.block([[np.array([[len(Z)]]),len(Z)*Z.mean(axis=0)[None,:]],
                            [len(Z)*Z.mean(axis=0)[:,None],(len(Z)-1)*S+len(Z)*np.outer(Z.mean(axis=0),Z.mean(axis=0))]])
assert np.allclose(G_reconstructed,XX.T@XX)
Hn = XX @ np.linalg.solve(XX.T@XX,XX.T)
assert np.allclose(Hn@Hn,Hn) and np.allclose(Hn,Hn.T)
assert np.allclose(Hn,Q@Q.T) and np.allclose(Hn,U@U.T)
assert np.allclose(np.linalg.cond(XX.T@XX),np.linalg.cond(XX)**2)
Xd = np.array([[1,1,1],[1,2,2],[1,3,3]],dtype=float)
yd = np.array([1,2,2],dtype=float)
bd = np.linalg.pinv(Xd)@yd
assert np.allclose(bd,[2/3,1/4,1/4])
null = np.array([0.,1.,-1.])
assert np.allclose(Xd@null,0) and abs(bd@null)<1e-12
assert np.allclose(Xd@(bd+2*null),Xd@bd)
assert np.linalg.norm(bd+2*null)>np.linalg.norm(bd)

plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.fonttype":"path",
                     "axes.spines.top":False,"axes.spines.right":False})
blue, orange, ink = "#2166ac", "#c46b22", "#253746"
fig,(ax,geo)=plt.subplots(1,2,figsize=(12.6,4.8),gridspec_kw={"width_ratios":[1,1.1]})
fig.subplots_adjust(left=.065,right=.97,bottom=.19,top=.83,wspace=.32)
xx=np.array([1.,2.,3.]); obs=np.array([1.,2.,2.]); fitted=2/3+xx/2
t=np.linspace(.55,3.45,200)
ax.plot(t,2/3+t/2,color=blue,lw=2,label=r"$\hat y=2/3+x/2$")
ax.scatter(xx,obs,color=ink,s=48,zorder=5,label="observations")
for x0,y0,h0,label in zip(xx,obs,fitted,[r"$e_1=-1/6$",r"$e_2=1/3$",r"$e_3=-1/6$"]):
    ax.plot([x0,x0],[y0,h0],color=orange,lw=2.5)
    ax.scatter([x0],[h0],color=blue,s=24,zorder=4)
    ax.annotate(label,(x0,(y0+h0)/2),xytext=((-10,0) if x0==2 else (9,-5)),ha=("right" if x0==2 else "left"),textcoords="offset points",color=orange,fontsize=10)
ax.set(xlim=(.55,3.6),ylim=(.8,2.55),xlabel="predictor x",ylabel="response y",xticks=[1,2,3])
ax.set_title("Data space: three vertical residuals",loc="left",fontsize=12,fontweight="bold",pad=14)
ax.legend(loc="upper left",frameon=False,fontsize=10)
ax.grid(alpha=.14)
fit_len,res_len=1/np.sqrt(2),1/np.sqrt(6)
geo.set_aspect("equal")
geo.axhline(0,color="#a4b2be",lw=1.2)
geo.annotate("",xy=(1.12,0),xytext=(0,0),arrowprops={"arrowstyle":"->","color":"#a4b2be"})
geo.annotate("",xy=(fit_len,res_len),xytext=(0,0),arrowprops={"arrowstyle":"->","color":ink,"lw":2.2})
geo.annotate("",xy=(fit_len,0),xytext=(0,0),arrowprops={"arrowstyle":"->","color":blue,"lw":3})
geo.annotate("",xy=(fit_len,res_len),xytext=(fit_len,0),arrowprops={"arrowstyle":"->","color":orange,"lw":2.5})
mark=.04
geo.plot([fit_len-mark,fit_len-mark,fit_len],[0,mark,mark],color=orange,lw=1.2)
geo.text(.31,.24,r"$y_c=(-2/3,1/3,1/3)^\top$",rotation=29,ha="center",fontsize=10,color=ink)
geo.text(fit_len/2,-.08,r"$\hat y_c=\frac{1}{2}x_c$",ha="center",color=blue)
geo.text(.78,.24,r"$e=(-1,2,-1)^\top/6$",color=orange,fontsize=10)
geo.text(.78,.16,r"$\|e\|=1/\sqrt{6}$",color=orange,fontsize=10)
geo.text(1.11,-.07,r"$u=x_c/\sqrt{2}$",ha="right",fontsize=10,color="#657582")
geo.text(.34,-.17,r"$\|\hat y_c\|=1/\sqrt{2}$",ha="center",fontsize=10,color=blue)
geo.text(.02,.52,r"$x_c=(-1,0,1)^\top$",fontsize=10,color=blue)
geo.set(xlim=(-.06,1.55),ylim=(-.22,.59))
geo.set_title("Observation space: one residual vector",loc="left",fontsize=12,fontweight="bold",pad=14)
geo.axis("off")
fig.text(.065,.055,"Original illustration. Right: centered vectors in orthonormal coordinates; lengths and the right angle are exact.",fontsize=10,color="#566575")
fig.savefig(OUT/"ols-data-and-projection.svg")
fig.savefig(OUT/"ols-data-and-projection.png",dpi=170)
plt.close(fig)
result={"example":{"beta":[str(z) for z in b],"fitted":[str(z) for z in X*b],"residual":[str(z) for z in e],"SSE":str(e.dot(e)),"sigma2_MLE":"1/18","unbiased_sigma2":"1/6"},
        "symbolic_checks":["normal equations","symmetric/idempotent projection","gradient","completed square","centering/determinant"],
        "multiple_regression_max_abs_errors":errors,"gradient_descent_iterations":iteration+1,
        "rank_deficient_minimum_norm_beta":bd.tolist(),
        "figure_basis":{"u":(np.array(xc,dtype=float).ravel()/np.sqrt(2)).tolist(),"v":(np.array(e,dtype=float).ravel()*np.sqrt(6)).tolist()},
        "note":"Numerical checks support the written proofs; they do not prove the general statements."}
(OUT/"checks.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
