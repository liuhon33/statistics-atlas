"""Tier-2 chi-square figures and checks. Requires NumPy and Pillow; no SciPy.
Run this file from any cwd. All outputs stay next to this source.
"""
from pathlib import Path
import math
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parent
S=2
INK='#19324a'; BLUE='#2867ba'; TEAL='#147d83'; ORANGE='#d46c20'
COLORS={1:'#aa4871',2:'#d46c20',5:'#147d83',10:'#2867ba',30:'#7656a3'}
FONTS=Path('C:/Windows/Fonts')

def pdf(q,k):
    q=np.asarray(q,dtype=float)
    out=np.zeros_like(q)
    ok=q>0
    out[ok]=np.exp((k/2-1)*np.log(q[ok])-q[ok]/2-(k/2)*math.log(2)-math.lgamma(k/2))
    if k==2: out[q==0]=.5
    return out

def sf5(q):
    x=q/2
    return math.erfc(math.sqrt(x))+math.exp(-x)/math.sqrt(math.pi)*(2*math.sqrt(x)+4*x**1.5/3)

class Canvas:
    def __init__(self,w,h):
        self.w,self.h=w,h
        self.im=Image.new('RGB',(w*S,h*S),'#f5f8fc')
        self.d=ImageDraw.Draw(self.im)
    def text(self,x,y,t,size=24,color=INK,bold=False):
        font=ImageFont.truetype(str(FONTS/('segoeuib.ttf' if bold else 'segoeui.ttf')),size*S)
        self.d.text((int(x*S),int(y*S)),t,font=font,fill=color)
    def line(self,points,color=INK,width=2):
        self.d.line([(round(x*S),round(y*S)) for x,y in points],fill=color,width=width*S)
    def box(self,x,y,w,h):
        self.d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S),radius=15*S,fill='white',outline='#d7e1ec',width=2*S)
    def save(self,name):
        self.im.resize((self.w,self.h),Image.Resampling.LANCZOS).save(OUT/name)

class Plot:
    def __init__(self,c,x,y,w,h,xlim,ylim,xticks,yticks):
        self.c,self.x,self.y,self.w,self.h=c,x,y,w,h
        self.xlim,self.ylim=xlim,ylim
        for v in yticks:
            px,py=self.xy(xlim[0],v)
            c.line([(px,py),(px+w,py)],'#e6ecf2',1)
            c.text(px-62,py-14,f'{v:g}',20)
        c.line([(x,y),(x,y+h),(x+w,y+h)])
        for v in xticks:
            px,py=self.xy(v,ylim[0]); c.line([(px,py),(px,py+6)])
            c.text(px-10,py+12,f'{v:g}',21)
    def xy(self,a,b):
        return self.x+self.w*(a-self.xlim[0])/(self.xlim[1]-self.xlim[0]), self.y+self.h-self.h*(b-self.ylim[0])/(self.ylim[1]-self.ylim[0])
    def curve(self,xs,ys,color,width=3,dash=False):
        points=[]
        for i,(a,b) in enumerate(zip(xs,ys)):
            if self.xlim[0]<=a<=self.xlim[1] and self.ylim[0]<=b<=self.ylim[1] and (not dash or i%18<11):
                points.append(self.xy(a,b))
            else:
                if len(points)>1: self.c.line(points,color,width)
                points=[]
        if len(points)>1: self.c.line(points,color,width)

# Shape: raw densities vs standardized densities on correctly transformed axes.
c=Canvas(1600,940)
c.text(55,28,'Degrees of freedom change location, spread and shape',40,bold=True)
c.text(55,88,'The raw sum moves right. Standardization reveals the approach to a bell shape.',26)
for x in [45,825]: c.box(x,145,730,700)
c.text(80,168,'Raw Q ~ χ²ₖ',30,bold=True)
c.text(860,168,'Standardized (Q − k) / √(2k)',30,bold=True)
p=Plot(c,120,300,615,400,(0,55),(0,.55),[0,10,20,30,40,50],[0,.1,.2,.3,.4,.5])
q=np.linspace(.001,55,5000)
for j,k in enumerate([1,2,5,10,30]):
    c.text(90+j*130,225,f'k = {k}',23,COLORS[k],True)
    p.curve(q,pdf(q,k),COLORS[k])
c.text(590,755,'Sum Q',24)
c.text(95,272,'Density',20)
c.text(90,790,'k = 1 rises without bound near 0 (clipped).',22)
p2=Plot(c,900,300,615,400,(-3,4),(0,.6),[-3,-2,-1,0,1,2,3,4],[0,.2,.4,.6])
z=np.linspace(-3,4,3000)
for j,k in enumerate([5,10,30]):
    c.text(860+j*130,225,f'k = {k}',23,COLORS[k],True)
    p2.curve(z,math.sqrt(2*k)*pdf(k+math.sqrt(2*k)*z,k),COLORS[k])
p2.curve(z,np.exp(-z*z/2)/math.sqrt(2*math.pi),INK,3,True)
c.text(1270,225,'Normal (dashed)',22,INK,True)
c.text(875,272,'Density',20)
c.text(1220,755,'Standardized value',23)
c.text(865,790,'All curves here have mean 0 and variance 1.',22)
c.text(75,875,'Mean = k     SD = √(2k)     Skewness = √(8/k) → 0     More symmetric does not mean exactly normal.',25)
c.save('chi-square-shapes.png')

# Reproducible finite-sample illustrations under the fair-die null.
rng=np.random.default_rng(20261110)
M=150000
samples={}
simulation={}
for n in [6,60,600]:
    counts=rng.multinomial(n,[1/6]*6,size=M)
    scores=((counts-n/6)**2/(n/6)).sum(axis=1)
    samples[n]=np.sort(scores)
    simulation[n]={'replicates':M,'mean':float(scores.mean()),'variance':float(scores.var()),
                   'null_rejection_rate_at_11_0705':float(np.mean(scores>11.070497693516355))}
    assert abs(scores.mean()-5)<.05
    assert abs(scores.var()-10*(n-1)/n)<.22

c=Canvas(1500,1050)
c.text(55,25,'Why six face counts give five degrees of freedom',39,bold=True)
c.text(55,82,'Fair die, independent rolls, no fitted probabilities. The total n is fixed.',25)
for x,w in [(55,420),(540,420),(1025,420)]: c.box(x,140,w,165)
for x in [485,970]:
    c.line([(x,220),(x+43,220)],BLUE,4)
    c.line([(x+33,211),(x+43,220),(x+33,229)],BLUE,4)
c.text(80,162,'6 dependent residuals',29,BLUE,True)
c.text(80,208,'Their sum is exactly zero.',23)
c.text(80,250,'6 coordinates − 1 constraint',23)
c.text(565,162,'5 free directions',29,TEAL,True)
c.text(565,208,'Rotate within the subspace.',23)
c.text(565,250,'CLT → five independent N(0,1)',22)
c.text(1050,162,'Sum their squares',29,ORANGE,True)
c.text(1050,208,'Same squared length Q.',23)
c.text(1050,250,'Q → χ²₅ in distribution',25)
c.box(55,340,1390,625)
c.text(90,360,'More rolls improve the approximation, but df stays 5',30,bold=True)
for j,(n,color) in enumerate([(6,'#aa4871'),(60,ORANGE),(600,BLUE)]):
    c.text(100+j*265,412,f'n = {n} (simulated)',23,color,True)
c.text(1000,412,'χ²₅ reference (dashed)',23,INK,True)
p=Plot(c,160,500,1150,350,(0,20),(0,1),[0,5,10,15,20],[0,.25,.5,.75,1])
grid=np.linspace(0,20,1601)
for n,color in [(6,'#aa4871'),(60,ORANGE),(600,BLUE)]:
    cdf=np.searchsorted(samples[n],grid,side='right')/M
    p.curve(grid,cdf,color,3)
    err=float(np.max(np.abs(cdf-np.array([1-sf5(float(t)) for t in grid]))))
    simulation[n]['max_cdf_error_on_plot_grid']=err
    if n>=60: assert err<.04
p.curve(grid,[1-sf5(float(t)) for t in grid],INK,3,True)
c.text(100,465,'Cumulative probability P(Q ≤ q)',22)
c.text(1100,900,'Mismatch q',23)
c.text(90,980,'150,000 repetitions per n; fixed seed. At n = 6, expected counts are only 1: a deliberately poor case.',22)
c.save('dice-limit.png')

# Deterministic checks of normalization, moments and the covariance geometry.
# q=t² removes the k=1 singularity for numerical quadrature.
t=np.linspace(1e-8,math.sqrt(300),250001)
moments={}
for k in [1,2,5,10,30]:
    weight=pdf(t*t,k)*2*t
    vals=[float(np.trapezoid(weight*t**(2*m),t)) for m in [0,1,2]]
    assert abs(vals[0]-1)<1e-7
    assert abs(vals[1]-k)<1e-6
    assert abs(vals[2]-k*(k+2))<1e-5
    moments[k]={'mass':vals[0],'mean':vals[1],'second_moment':vals[2]}
H=np.zeros((6,5))
for j in range(1,6):
    H[:j,j-1]=1/math.sqrt(j*(j+1)); H[j,j-1]=-j/math.sqrt(j*(j+1))
u=np.ones(6)/math.sqrt(6); P=np.eye(6)-np.outer(u,u)
assert np.allclose(H.T@H,np.eye(5)) and np.allclose(H@H.T,P)
assert np.allclose(P@P,P) and np.allclose(P@u,0)
assert np.linalg.matrix_rank(P)==5
R=(np.array([4,6,8,10,12,20])-10)/math.sqrt(10)
assert np.isclose(R@R,16) and np.isclose((H.T@R)@(H.T@R),16)
assert np.allclose(H.T@P@H,np.eye(5))

# Numerical convolution check after x=q sin²(theta), including half-shapes.
theta=np.linspace(1e-8,math.pi/2-1e-8,200001)
convolution_errors=[]
for a,b,q0 in [(.5,.5,3),(.5,2,5),(2,3,7)]:
    x=q0*np.sin(theta)**2
    jac=2*q0*np.sin(theta)*np.cos(theta)
    integral=float(np.trapezoid(pdf(x,2*a)*pdf(q0-x,2*b)*jac,theta))
    expected=float(pdf(q0,2*(a+b)))
    error=abs(integral-expected)
    assert error<2e-6
    convolution_errors.append(error)
checks={'seed':20261110,'simulation':simulation,'quadrature_moments':moments,
        'projection_rank':int(np.linalg.matrix_rank(P)),
        'projection_eigenvalues':np.linalg.eigvalsh(P).tolist(),
        'orthonormal_basis_max_error':float(np.max(np.abs(H.T@H-np.eye(5)))),
        'example_squared_length':float(R@R),'rotated_squared_length':float((H.T@R)@(H.T@R)),
        'convolution_absolute_errors':convolution_errors,
        'scope':'Deterministic arithmetic/quadrature and seeded Monte Carlo illustration, not proof or exact finite-sample calibration.'}
(OUT/'tier2-checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,indent=2))
