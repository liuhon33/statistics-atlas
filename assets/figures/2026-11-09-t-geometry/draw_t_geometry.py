"""Original vector illustration of the sample-mean t geometry; stdlib only.
Run this file to regenerate the SVG beside it. Coordinates are not sample data.
The sphere uses an orthographic projection; the triangle uses exact side lengths.
"""
from pathlib import Path
from html import escape
import math
import xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parent/'t-statistic-sphere-and-triangle.svg'
W,H=1800,1180
ink='#172c44'; muted='#566b80'; blue='#2563eb'; orange='#c77708'; red='#cf4655'
s=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">The t-statistic: a signed projection divided by residual length</title>
<desc id="desc">Left: a three-dimensional sphere schematic with the mean axis u, its perpendicular residual plane, and z = A u + r. Right: the exact plane triangle has signed horizontal coordinate A, vertical length square root Q, and angle theta from positive u. T equals square root nu times cotangent theta, with nu = n minus 1. Normality supplies independent normal and chi-square components; orthogonality alone does not imply independence.</desc>
<defs>
<radialGradient id="sphere" cx="32%" cy="24%" r="80%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#dce9f6"/></radialGradient>
<marker id="axis" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L10 5L0 10Z" fill="{muted}"/></marker>
''']
for name,col in [('blue',blue),('orange',orange),('red',red)]:
    s.append(f'<marker id="{name}" markerWidth="17" markerHeight="17" refX="14" refY="8.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L17 8.5L0 17Z" fill="{col}"/></marker>')
s.append('</defs><rect width="1800" height="1180" fill="#f5f8fc"/>')
def text(x,y,t,size=24,color=ink,weight=400,anchor='start',extra=''):
    s.append(f'<text x="{x}" y="{y}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" {extra}>{escape(t)}</text>')
def line(x1,y1,x2,y2,col=muted,width=2,dash='',arrow=''):
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{width}" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(f' marker-end="url(#{arrow})"' if arrow else '')+'/>')
def rect(x,y,w,h,fill,stroke='none',rx=20):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
def circle(x,y,r,fill,stroke='none',sw=1):
    s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def path(d,col,width=2,fill='none',extra=''):
    s.append(f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{width}" {extra}/>')
text(48,66,'The geometry of the t-statistic',46,weight=700)
text(50,112,'z = (X − μ1) / σ     ·     u = 1 / √n     ·     ν = n − 1     ·     iid N(μ, σ²) observations, σ > 0, n ≥ 2',26,muted)
rect(48,155,770,670,'#fff','#d6e0ec')
rect(842,155,910,670,'#fff','#d6e0ec')
text(80,202,'01   A direction in the Gaussian sphere',28,weight=650)
text(80,238,'3D illustration of an n-dimensional decomposition',22,muted)
text(874,202,'02   The exact triangle in span(u, r)',28,weight=650)
text(874,238,'Same vectors, enlarged in their own plane',22,muted)

# Orthographic camera: x-screen = sqrt(1-c²)*x + c*z; y-screen = -y.
# u is the x-axis, residual plane is x=0. All shown vectors have z-depth 0.
cx,cy,R,c=354,480,214,.29
k=math.sqrt(1-c*c); a,b=.6*R,.8*R
px,py=cx+k*a,cy-b
circle(cx,cy,R,'url(#sphere)','#a7bdd5',2)
s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{c*R}" ry="{R}" fill="#fff0d4" fill-opacity=".7" stroke="#d4a254" stroke-width="2"/>')
s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="44" fill="none" stroke="#b3c7dc" stroke-width="1.5" stroke-dasharray="7 7"/>')
line(95,cy,680,cy,'#899daf',2,arrow='axis')
text(681,cy+8,'+u',25,weight=600)
line(cx,cy,cx,py,orange,3,'6 7')
line(cx,py,px,py,orange,2,'6 7')
line(cx,cy,px,cy,blue,6,arrow='blue')
line(px,cy,px,py,orange,6,arrow='orange')
line(cx,cy,px,py,red,6,arrow='red')
path(f'M {px-19} {cy} L {px-19} {cy-19} L {px} {cy-19}',muted,2)
circle(cx,cy,5,ink);circle(px,py,6,red)
text(cx-24,cy+31,'0',23)
text(px+19,py-12,'z = Au + r',28,red,650)
text(px+21,(cy+py)/2+7,'r',30,orange,650)
text((cx+px)/2,cy+45,'Au',29,blue,650,'middle')
text(cx-22,py-14,'r',25,orange,600)
text(81,728,'Residual space u⊥',25,orange,650)
text(81,761,'Dimension n − 1; a residual plane is shown for n = 3.',21,muted)
line(268,714,322,653,orange,1.6)
text(81,797,'Sphere: fixed radius R = ‖z‖, not necessarily 1.',21,muted)
theta=math.atan2(b,a)
arc=[]
for i in range(41):
    t=theta*i/40
    arc.append(f'{cx+k*52*math.cos(t):.3f},{cy-52*math.sin(t):.3f}')
path('M'+' L'.join(arc),ink,2)
text(cx+68,cy-25,'θ',25,ink,600)

# Exact Euclidean triangle: the illustrated case A>0, sides 300 and 400.
ox,oy,fx,zy=980,690,1280,290
path(f'M{ox},{oy} L{fx},{oy} L{fx},{zy} Z','none',0,'#f4f8ff')
line(924,oy,1450,oy,'#91a3b5',2,arrow='axis')
line(ox,oy,fx,oy,blue,7,arrow='blue')
line(fx,oy,fx,zy,orange,7,arrow='orange')
line(ox,oy,fx,zy,red,7,arrow='red')
path(f'M{fx-27},{oy} L{fx-27},{oy-27} L{fx},{oy-27}',muted,2.5)
circle(ox,oy,6,ink);circle(fx,zy,6,red)
text(ox-27,oy+35,'0',25)
text(1455,oy+9,'+u',27,weight=600)
text(fx+21,zy-5,'z',32,red,650)
text((ox+fx)/2,oy+47,'A = uᵀz',31,blue,650,'middle')
text((ox+fx)/2,oy+79,'signed mean coordinate',22,blue,400,'middle')
text(1330,469,'‖r‖ = √Q',32,orange,650)
text(1330,503,'residual length',23,orange)
text(1330,538,'Q = ‖r‖²',25,orange)
text(1090,459,'R = ‖z‖',30,red,600,'middle',extra='transform="rotate(-53.1301 1090 459)"')
endx=ox+80*.6; endy=oy-80*.8
path(f'M{ox+80},{oy} A80,80 0 0 0 {endx},{endy}',ink,2.5)
text(ox+105,oy-43,'θ',32,weight=600)
text(1500,601,'uᵀr = 0',25,muted,600,'middle')
text(1500,638,'A > 0 shown',22,muted,400,'middle')

rect(48,853,1704,279,'#eaf1fb')
text(80,899,'THE RADIUS CANCELS — ONLY THE ANGLE REMAINS',22,muted,650)
def fraction(x,y,top,bottom,width,col=ink):
    text(x,y-16,top,35,col,500,'middle')
    line(x-width/2,y,x+width/2,y,col,2)
    text(x,y+42,bottom,35,col,500,'middle')
text(99,972,'T =',43,weight=650)
fraction(290,958,'A','√(Q/ν)',174)
text(405,972,'= √ν',42)
fraction(605,958,'A','‖r‖',112)
text(705,972,'= √ν cot θ',45,weight=650)
text(1180,949,'A = R cos θ',29,blue,600)
text(1180,991,'‖r‖ = R sin θ',29,orange,600)
text(80,1053,'A ~ N(0,1) and Q ~ χ² with ν degrees of freedom are independent  ⇒  T ~ Student t with ν degrees of freedom.',24)
text(80,1096,'θ < π/2: positive T     ·     θ = π/2: T = 0     ·     θ > π/2: negative T     ·     0 < θ < π',24,muted)
text(49,1162,'Orthogonality gives the triangle. Gaussianity gives independence. Left: schematic perspective; right: exact planar geometry.',22,muted)
s.append('</svg>')
svg='\n'.join(s)+'\n'
ET.fromstring(svg)
assert math.isclose(math.hypot(300,400),500)
assert math.isclose(math.atan2(400,300),theta)
assert math.isclose(a*a+b*b,R*R)
assert math.isclose(math.cos(theta)/math.sin(theta),.75)
OUT.write_text(svg,encoding='utf-8',newline='\n')
print(OUT)
