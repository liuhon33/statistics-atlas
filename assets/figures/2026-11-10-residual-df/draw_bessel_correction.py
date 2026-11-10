"""Deterministic expectation diagram + exact finite-distribution checks (Pillow)."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
support = [(0,0),(1,2),(2,1)]
variance, covariance = F(2,3), F(1,3)
ss_values, cp_values = [], []
for sample in product(support, repeat=3):
    x,y = zip(*sample)
    mx,my = F(sum(x),3),F(sum(y),3)
    ss = sum((a-mx)**2 for a in x)
    cp = sum((a-mx)*(b-my) for a,b in zip(x,y))
    assert ss == sum((a-1)**2 for a in x)-3*(mx-1)**2
    assert cp == sum((a-1)*(b-1) for a,b in zip(x,y))-3*(mx-1)*(my-1)
    ss_values.append(ss)
    cp_values.append(cp)
assert sum(ss_values)/27 == 2*variance
assert sum(cp_values)/27 == 2*covariance
assert sum(ss_values)/54 == variance
assert sum(cp_values)/54 == covariance

def mul(a,b):
    return [[sum(v*w for v,w in zip(row,col)) for col in zip(*b)] for row in a]
for n in range(2,9):
    c = [[F(int(i==j))-F(1,n) for j in range(n)] for i in range(n)]
    assert mul(c,c) == c
    assert all(sum(row)==0 for row in c)
    assert sum(c[i][i] for i in range(n)) == n-1
v,w = [-1,0,1],[-1,1,0]
assert sum(v)==sum(w)==0
assert sum(a*a for a in v)==2 and sum(a*b for a,b in zip(v,w))==1
assert sum(a*a for a in [1,2,3]) == 3*2**2+sum(a*a for a in v)

im = Image.new('RGB',(1450,760),'#f8fafc')
d = ImageDraw.Draw(im)
def text(x,y,t,size=27,color='#24364b',bold=False):
    f=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
    d.text((x,y),t,font=f,fill=color)
text(55,35,'Estimating the mean removes one variance-unit on average',36,bold=True)
text(55,95,'Three independent observations, each with variance σ²; their common mean is μ.',26)
text(55,168,'Expected squared deviation about the true mean',29,bold=True)
for i in range(3):
    a=65+i*400
    d.rounded_rectangle((a,220,a+375,312),radius=10,fill='#d7e8fb')
    text(a+145,241,'σ²',37,color='#246abd',bold=True)
text(1290,242,'3σ²',36,color='#246abd',bold=True)
text(55,355,'The same total splits into two parts',29,bold=True)
d.rounded_rectangle((65,410,440,502),radius=10,fill='#fff0c7')
d.rounded_rectangle((465,410,1240,502),radius=10,fill='#d2f0e8')
text(210,431,'σ²',37,color='#906500',bold=True)
text(815,431,'2σ²',37,color='#147a67',bold=True)
text(65,525,'Mean-estimation component',25,color='#906500',bold=True)
text(65,570,'E[3(X̄ − μ)²] = σ²',28,color='#906500')
text(490,525,'Remaining centered sum of squares',25,color='#147a67',bold=True)
text(490,570,'E[Σ(Xᵢ − X̄)²] = (3 − 1)σ²',28,color='#147a67')
text(55,652,'Divide the remaining sum by 2, not 3, to estimate σ² without bias.',30,bold=True)
text(55,710,'These are expectations over repeated samples—not fixed proportions in every observed sample.',24,color='#64748b')
im.save(OUT/'bessel-expectation.png')
(OUT/'bessel-checks.json').write_text(json.dumps({
    'finite_population':support,'sample_size':3,'equiprobable_samples_checked':27,
    'population_variance':str(variance),'population_covariance':str(covariance),
    'expected_centered_ss':str(sum(ss_values)/27),
    'expected_centered_cross_product':str(sum(cp_values)/27),
    'centering_matrix_idempotence_zero_row_sums_trace':'exact rational PASS for n=2,...,8',
    'example_centering_pythagoras_covariance':'PASS',
    'scope':'Exact illustration checks; general claims are established algebraically in the note.'
},indent=2)+'\n',encoding='utf-8')
print('PASS: 27 exact sample checks, covariance/variance expectations, centering matrices and example geometry.')
