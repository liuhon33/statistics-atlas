"""Original static teaching figure. Requires Pillow; run with any working directory."""
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
x = [150, 160, 170, 180, 190]
y = [47, 49, 60, 65, 79]
xbar, ybar = sum(x)/5, sum(y)/5
slope = sum((a-xbar)*(b-ybar) for a,b in zip(x,y))/sum((a-xbar)**2 for a in x)
fit = [ybar+slope*(a-xbar) for a in x]
e = [b-f for b,f in zip(y,fit)]
rss = sum(r*r for r in e)
assert slope == .8 and fit == [44,52,60,68,76]
assert e == [3,-3,0,-3,3] and rss == 36
assert sum(e) == 0 and sum((a-xbar)*r for a,r in zip(x,e)) == 0
# Two fitting constraints are independent because the heights are not constant.
assert sum((a-xbar)**2 for a in x) > 0
df = len(x)-2
assert df == 3 and rss/df == 12

im = Image.new('RGB', (1500,800), '#f8fafc')
d = ImageDraw.Draw(im)
fontdir = Path('C:/Windows/Fonts')
def font(size, bold=False):
    return ImageFont.truetype(str(fontdir/('arialbd.ttf' if bold else 'arial.ttf')), size)
def text(pos, s, size=25, fill='#22364b', bold=False):
    d.text(pos, s, font=font(size,bold), fill=fill)
def line(coords, fill='#dce3eb', width=2):
    d.line(coords, fill=fill, width=width)
def px(v): return 105+(v-145)/50*650
def py(v): return 610-(v-40)/45*450

text((55,35), 'Five residuals, but only three degrees of freedom', 39, bold=True)
text((55,95), 'Fit weight from height using a least-squares line with an intercept.', 27)
text((105,150), 'Weight (kg)', 24)
for t in [40,50,60,70,80]:
    line((105,py(t),755,py(t)))
    text((61,py(t)-14),str(t),23)
line((105,180,105,610), '#78899a')
line((105,610,755,610), '#78899a')
for t in x:
    text((px(t)-20,625),str(t),23)
text((335,665),'Height (cm)',25)
line((px(147),py(60+.8*(147-170)),px(193),py(60+.8*(193-170))), '#246abd', 5)
for a,b,f,r in zip(x,y,fit,e):
    line((px(a),py(b),px(a),py(f)),'#d56324',6)
    d.ellipse((px(a)-7,py(f)-7,px(a)+7,py(f)+7),fill='white',outline='#246abd',width=3)
    d.ellipse((px(a)-8,py(b)-8,px(a)+8,py(b)+8),fill='#22364b')
    label_y = py(b)-22 if r > 0 else py(b)+4
    text((px(a)+13,label_y),f'{r:+g}' if r else '0',24,'#ad4a12',True)
text((130,710),'Orange gaps: observed minus fitted weight (kg)',23,'#ad4a12')

d.rounded_rectangle((815,165,1445,685),radius=22,fill='white',outline='#dce3eb',width=2)
text((850,195),'Fitting uses two adjustable coefficients',27,bold=True)
text((850,250),'Intercept: sets the line\'s height',27)
text((850,297),'Slope: sets the line\'s tilt',27)
text((850,375),'5  −  2  =  3',58,'#246abd',True)
text((850,453),'observations − fitted coefficients = residual df',23)
text((850,510),'All five residuals are still present.',27,bold=True)
text((850,552),'Fitting imposes two relationships;',26)
text((850,590),'only three residual values can vary freely.',26)
text((850,713),'Squared gaps: 9 + 9 + 0 + 9 + 9 = 36 kg²',25)
text((55,765),'Original illustrative data, reused from the Linear regression introduction. Not a population weight formula.',21,'#63778c')
im.save(OUT/'residual-df.png')
(OUT/'checks.json').write_text(json.dumps({
    'height_cm':x,'weight_kg':y,'fitted_kg':fit,'residuals_kg':e,
    'slope_kg_per_cm':slope,'residual_sum':sum(e),
    'height_weighted_residual_sum':sum((a-xbar)*r for a,r in zip(x,e)),
    'rss_kg2':rss,'residual_df':df,'variance_kg2':rss/df,
    'residual_sd_kg':math.sqrt(rss/df),'assertions':'passed',
    'scope':'Exact checks of this constructed example, not a proof of general unbiasedness.'
},indent=2)+'\n',encoding='utf-8')
print('PASS: fit, residuals, two constraints, RSS, df and variance; figure generated.')
