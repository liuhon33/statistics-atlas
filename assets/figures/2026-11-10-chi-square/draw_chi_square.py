"""Original chi-square introduction. Requires Pillow; run this file from any cwd."""
from pathlib import Path
from math import exp, isclose, gamma, erfc, sqrt, pi
import json
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
S = 2
W, H = 1500, 1080
im = Image.new('RGB', (W*S, H*S), '#f5f8fc')
d = ImageDraw.Draw(im)
INK, BLUE, TEAL, ORANGE = '#19324a', '#2867ba', '#147d83', '#d46c20'
FONT = Path('C:/Windows/Fonts')

def text(x, y, value, size=26, color=INK, bold=False):
    font = ImageFont.truetype(str(FONT / ('segoeuib.ttf' if bold else 'segoeui.ttf')), size*S)
    d.text((x*S,y*S), value, font=font, fill=color)

def line(points, fill=INK, width=3):
    d.line([(round(x*S),round(y*S)) for x,y in points], fill=fill, width=width*S)

def box(x, y, w, h, fill='#ffffff'):
    d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S), radius=16*S, fill=fill, outline='#d7e1ec', width=2*S)

counts = {'A':[8,11,10,9,12,10], 'B':[4,6,8,10,12,20]}
scores = {name:sum((o-10)**2/10 for o in obs) for name,obs in counts.items()}
pdf = lambda q: q**1.5*exp(-q/2)/(2**2.5*gamma(2.5))
# Upper incomplete gamma recurrence for 5 degrees of freedom.
def sf(q):
    x=q/2
    return erfc(sqrt(x))+exp(-x)/sqrt(pi)*(2*sqrt(x)+4*x**1.5/3)
lo,hi=0,50
for _ in range(100):
    mid=(lo+hi)/2
    if sf(mid)>.05: lo=mid
    else: hi=mid
critical=(lo+hi)/2

text(55,28,'A fair die or a loaded die? Measure the mismatch.',40,bold=True)
text(55,88,'Roll each die 60 times. Fairness predicts 10 of each face — not exactly 10 every time.',25)
for x,name,color in [(55,'A',TEAL),(765,'B',ORANGE)]:
    box(x,145,680,390)
    text(x+30,162,f'Die {name}: Q = {scores[name]:g}',31,color,True)
    text(x+30,207,'Count',22)
    base=440
    for i,n in enumerate(counts[name]):
        cx=x+100+i*88
        d.rectangle(((cx-23)*S,(base-n*9)*S,(cx+23)*S,base*S),fill=color)
        text(cx-13,base-n*9-31,str(n),23,color,True)
        text(cx-7,base+10,str(i+1),24)
    for dx in range(45,635,18): line([(x+dx,350),(x+dx+10,350)],BLUE,2)
    text(x+300,207,'Dashed line = expected 10',22,BLUE)
    line([(x+45,base),(x+635,base)],INK,2)
    text(x+30,489,'Face →',22)
    text(x+180,489,'Consistent with fairness' if name=='A' else 'Evidence of bias',25,color,True)

box(55,565,1390,450)
text(90,584,'How large is too large? Compare Q with χ²₅ under fairness.',29,bold=True)
text(90,630,'Approximate reference: 6 faces − 1 fixed-total constraint = 5 degrees of freedom',24)
x0,y0,xw,yh=160,915,1130,220
xy=lambda q,f:(x0+xw*q/22,y0-yh*f/.16)
tail=[xy(critical,0)]+[xy(critical+i*(22-critical)/400,pdf(critical+i*(22-critical)/400)) for i in range(401)]+[xy(22,0)]
d.polygon([(round(x*S),round(y*S)) for x,y in tail],fill='#f4b986')
curve=[xy(i*22/700,pdf(i*22/700)) for i in range(701)]
line(curve,TEAL,4)
line([(x0,685),(x0,y0),(1310,y0)],INK,2)
text(90,662,'Density',21)
for f in [.05,.10,.15]:
    _,y=xy(0,f)
    text(100,y-15,f'{f:.2f}',20)
for q in [0,5,10,15,20]:
    x,_=xy(q,0)
    line([(x,y0),(x,y0+6)],INK,2)
    text(x-9,y0+10,str(q),22)
for q,label,color in [(1,'A: 1',TEAL),(16,'B: 16',ORANGE)]:
    x,y=xy(q,pdf(q))
    line([(x,y0),(x,y-25)],color,3)
    text(x-28,y-65,label,26,color,True)
x,_=xy(critical,0)
line([(x,y0),(x,780)],ORANGE,2)
text(x-45,738,'11.07',25,ORANGE,True)
text(960,685,'Upper 5%: flag the die',27,ORANGE,True)
text(970,965,'Mismatch score Q',24)
text(90,1030,'Invented counts. B is flagged; A is not. Neither conclusion proves cheating or fairness.',24)
im.resize((W,H),Image.Resampling.LANCZOS).save(OUT/'chi-square-intro.png')

step=.001
def integrate(a,b):
    return step*(sum(pdf(a+i*step) for i in range(1,round((b-a)/step)))+(pdf(a)+pdf(b))/2)
mass=integrate(0,80)
tail_numeric=integrate(16,80)
assert all(sum(obs)==60 for obs in counts.values())
assert isclose(scores['A'],1) and isclose(scores['B'],16)
assert isclose(mass,1,abs_tol=1e-8)
assert isclose(tail_numeric,sf(16),abs_tol=1e-9)
assert isclose(critical,11.070497693516,abs_tol=1e-10)
assert all(y0-yh <= y <= y0 for x,y in curve)
checks={'counts':counts,'scores':scores,'degrees_of_freedom':5,'expected_per_face':10,
        'right_tail_probabilities':{name:sf(q) for name,q in scores.items()},
        'critical_95_percent':critical,'density_integral_0_to_80':mass,
        'right_tail_numeric_16_to_80':tail_numeric,'figure_size':[W,H],
        'tail_beyond_plot_limit':sf(22),
        'scope':'Arithmetic and chi-square reference calculations; not an exact multinomial test or real experiment.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,indent=2))
