"""Reproducible, dependency-free SVGs; run this file with Python 3.

Original explanatory artwork, not a modification of the handwritten source.
Each SVG uses the same rectangular example as three-matrix-products.svg.
"""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).resolve().parent
INK, MUTED = '#243447', '#526279'
BLUE, TEAL, ORANGE = '#245eb2', '#087e78', '#ad5710'
PALE = '#f3f6fb'
A = [[1, 2, 0], [0, 1, 3]]
B = [[2, 1], [1, 0], [0, 2]]
P = [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
terms = [[[A[i][k]*B[k][j] for j in range(2)] for i in range(2)] for k in range(3)]
assert P == [[4, 1], [1, 6]]
assert [[sum(t[i][j] for t in terms) for j in range(2)] for i in range(2)] == P

class SVG:
    def __init__(self, height, title, description):
        self.height = height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
                      '<rect width="1100" height="100%" rx="18" fill="white"/>']
        self.text(36, 48, title, 29, weight='700')
    def text(self, x, y, s, size=23, color=INK, weight='400', anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(s))}</text>')
    def line(self, x1, y1, x2, y2, color='#d6dfeb', dash=''):
        self.parts.append(f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="{dash}"/>')
    def rect(self, x, y, w, h, fill, stroke='none', dash=''):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-dasharray="{dash}"/>')
    def matrix(self, x, y, data, cell=52, row=None, col=None, color=BLUE, dashed=False, label=None):
        nr, nc = len(data), len(data[0]); w, h = cell*nc, cell*nr
        if row is not None: self.rect(x+2,y+row*cell+2,w-4,cell-4,'#e8f0ff',color)
        if col is not None: self.rect(x+col*cell+2,y+2,cell-4,h-4,'#e4f4f0',color)
        if dashed:
            for j in range(nc): self.rect(x+j*cell+3,y+2,cell-6,h-4,'#f3f8fd',color if j==0 else TEAL,'6 5')
        for i,r in enumerate(data):
            for j,v in enumerate(r): self.text(x+(j+.5)*cell,y+(i+.5)*cell+9,v,27,anchor='middle')
        for xx,sgn in [(x-5,1),(x+w+5,-1)]:
            self.parts.append(f'<path d="M {xx+sgn*10} {y-3} H {xx} V {y+h+3} H {xx+sgn*10}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
        if label: self.text(x+w/2,y-20,label,22,color,anchor='middle',weight='600')
        return w,h
    def save(self, name):
        self.parts.append('</svg>')
        (OUT/(name+'.svg')).write_text('\n'.join(self.parts),encoding='utf-8')

s=SVG(690,'1 · ROW × COLUMN → ONE NUMBER','Highlight the first row of A and the first column of B, then pair their three entries and sum. Repeat for every output entry.')
s.text(36,88,'Choose row i of A and column j of B. Only entry (i, j) is produced.',22,MUTED)
s.matrix(80,150,A,row=0,label='A : 2 × 3')
s.text(275,218,'×',32)
s.matrix(340,124,B,col=0,color=TEAL,label='B : 3 × 2')
s.text(492,218,'=',32)
s.matrix(560,150,P,label='AB : 2 × 2')
s.rect(562,152,48,48,'none',ORANGE)
s.text(740,183,'First row, first column',23,ORANGE,weight='600')
s.text(740,220,'→ top-left entry = 4',24)
s.line(36,310,1064,310)
s.text(36,335,'Extract the two vectors',20,BLUE,weight='600')
s.matrix(70,408,[[1,2,0]],row=0,label='row 1 : 1 × 3')
s.text(267,444,'×',30)
s.matrix(335,365,[[2],[1],[0]],cell=44,col=0,color=TEAL,label='column 1 : 3 × 1')
s.text(415,444,'=  1·2 + 2·1 + 0·0  =  4',29)
s.text(70,538,'Pair matching positions; add the three scalar products.',22,MUTED)
s.line(36,560,1064,560)
s.text(36,600,'Repeat for the other entries:',22,weight='600')
s.text(36,640,'(1,2): 1·1 + 2·0 + 0·2 = 1',21)
s.text(390,640,'(2,1): 0·2 + 1·1 + 3·0 = 1',21)
s.text(743,640,'(2,2): 0·1 + 1·0 + 3·2 = 6',21)
s.save('matrix-detail-1-dot')

s=SVG(900,'2 · MATRIX × COLUMN → ONE OUTPUT COLUMN','Dashed outlines group complete column vectors. Compute Ab1 and Ab2 separately and place them side by side, without adding the output columns.')
s.text(36,88,'B = [ b₁ | b₂ ]     ⇒     AB = [ Ab₁ | Ab₂ ]',28,BLUE,weight='600')
s.text(36,125,'Dashed outlines mean “keep this whole column together.”',22,MUTED)
s.matrix(75,190,A,label='A : 2 × 3')
s.text(275,255,'×',32)
s.matrix(340,164,B,dashed=True,label='B = [ b₁ | b₂ ]')
s.text(495,255,'=',32)
s.matrix(565,190,P,dashed=True,label='AB = [ Ab₁ | Ab₂ ]')
s.text(750,220,'b₁ and b₂: 3 × 1',23)
s.text(750,259,'Ab₁ and Ab₂: 2 × 1',23)
s.text(750,298,'A changes vector length: 3 → 2',20,MUTED)
s.line(36,350,1064,350)
for j,y in [(0,410),(1,610)]:
    color = BLUE if j==0 else TEAL
    s.text(36,y-20,f'Output column {j+1}: use the entries of b{j+1} as weights on A’s columns.',22,color,weight='600')
    s.text(40,y+82,f'Ab{j+1} =',27,color)
    for k,x in enumerate([195,415,635]):
        s.text(x,y+82,str(B[k][j])+' ×',27,color)
        s.matrix(x+65,y+30,[[A[0][k]],[A[1][k]]],label=f'A column {k+1}')
        if k<2: s.text(x+155,y+82,'+',29)
    s.text(822,y+82,'=',30)
    s.matrix(885,y+30,[[P[0][j]],[P[1][j]]],dashed=True,color=color,label=f'Ab{j+1}')
s.rect(36,807,1028,60,PALE)
s.text(56,846,'Place the resulting columns SIDE BY SIDE — do not add Ab₁ and Ab₂.',24,weight='600')
s.save('matrix-detail-2-columns')

s=SVG(1100,'3 · COLUMN × ROW → ONE WHOLE MATRIX','Take column k of A and row k of B. Form their outer product, repeat for k equals 1, 2, 3, and add the three 2 by 2 matrices entry by entry.')
s.text(36,88,'AB = A[:,1] B[1,:] + A[:,2] B[2,:] + A[:,3] B[3,:]',27,ORANGE,weight='600')
s.text(36,125,'Match the same inner index k: column k of A with row k of B.',22,MUTED)
s.matrix(85,190,A,col=0,color=TEAL,label='A : choose column 1')
s.text(285,254,'×',30)
s.matrix(350,164,B,row=0,color=BLUE,label='B : choose row 1')
s.text(565,212,'(2 × 1) × (1 × 2) = 2 × 2',27)
s.text(565,254,'Every column entry multiplies EVERY row entry.',21)
s.text(565,290,'No sum inside an outer product: its inner dimension is 1.',19,MUTED)
s.line(36,350,1064,350)
for k,y in enumerate([392,552,712]):
    s.text(40,y+56,f'k = {k+1}',25,ORANGE,weight='600')
    s.matrix(165,y,[[A[0][k]],[A[1][k]]],col=0,color=TEAL)
    s.text(246,y+58,'×',29)
    s.matrix(300,y+26,[B[k]],row=0,color=BLUE)
    s.text(447,y+58,'=',30)
    symbolic=[[f'{A[i][k]}·{B[k][j]}' for j in range(2)] for i in range(2)]
    s.matrix(500,y,symbolic,cell=57)
    s.text(659,y+58,'=',30)
    s.matrix(715,y,terms[k])
    s.text(900,y+57,f'M{k+1} : 2 × 2',23,ORANGE)
s.line(36,850,1064,850)
s.text(36,890,'Now SUM the three full matrices entry by entry:',24,weight='600')
for x,k in [(75,0),(310,1),(545,2)]:
    s.matrix(x,930,terms[k])
    s.text(x+155,994,'+' if k<2 else '=',32)
s.matrix(805,930,P,label='AB')
s.text(36,1080,'Contrast: method 2 assembles columns; method 3 adds overlapping full-sized contributions.',21,MUTED)
s.save('matrix-detail-3-outer')

# Independent vector-assembly calculation, not a copied final matrix.
columns = [[sum(B[k][j]*A[i][k] for k in range(3)) for i in range(2)] for j in range(2)]
assert [list(row) for row in zip(*columns)] == P
(OUT/'matrix-vector-detail-checks.json').write_text(json.dumps({'A':A,'B':B,'AB':P,'output_columns':columns,'outer_products':terms,'checks':'dot products = assembled columns = sum of outer products'},indent=2)+'\n',encoding='utf-8')
print('Three SVGs generated; all displayed numerical products verified.')
