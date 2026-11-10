"""Original Codex SVG diagrams and independent numeric checks for attention.pdf.

Run with Python + numpy + matplotlib. PDF excerpts are produced separately by
extract_handwriting.py; this script never modifies a source PDF or image.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'svg.fonttype': 'none', 'mathtext.fontset': 'dejavusans'})
INK, BLUE, TEAL, ORANGE = '#243447', '#3568aa', '#167e78', '#b86b18'
PALE, GREEN, GOLD = '#eef4fc', '#e7f4f1', '#fff4df'

def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set(xlim=(0, w), ylim=(h, 0)); ax.axis('off')
    fig.patch.set_facecolor('white')
    return fig, ax

def label(ax, x, y, s, size=12, color=INK, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, va='center', **kw)

def box(ax, x, y, w, h, title, sub='', color=BLUE, fill=PALE):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.08',
                              linewidth=1.2, edgecolor=color, facecolor=fill))
    label(ax,x+w/2,y+h*(.35 if sub else .5),title,14,color,ha='center')
    if sub: label(ax,x+w/2,y+h*.75,sub,10,INK,ha='center')

def arrow(ax, x1,y1,x2,y2, color=INK):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),
                arrowprops=dict(arrowstyle='-|>',lw=1.3,color=color,shrinkA=4,shrinkB=4))

def save(fig, name):
    fig.savefig(OUT/(name+'.svg'),facecolor='white')
    fig.savefig(OUT/(name+'.png'),facecolor='white')
    plt.close(fig)

# Compact reference flow, used only on the backbone card.
fig,ax=canvas(10,1.6)
for x,t,s in [(0.25,'Score','query-key dot products'),(3.6,'Normalize','scale, mask, row softmax'),(6.95,'Mix','weighted value vectors')]:
    box(ax,x,.27,2.8,1.05,t,s)
arrow(ax,3.05,.8,3.6,.8); arrow(ax,6.4,.8,6.95,.8)
save(fig,'attention-reference')

# Explicit head axis; no summed-head attention matrix.
fig,ax=canvas(12,6.2)
label(ax,.35,.4,'STANDARD MULTI-HEAD SELF-ATTENTION',17,weight='bold')
label(ax,.35,.82,'Tokens are rows. The head index stays separate until the final output projection.',11)
box(ax,.4,1.5,1.65,1.1,r'$E$',r'$T\times D$')
box(ax,2.75,1.35,2.7,1.4,r'$Q_i,\ K_i,\ V_i$',r'each: $T\times d_h$')
arrow(ax,2.05,2.05,2.75,2.05)
label(ax,3.95,3.05,r'$i=1,\ldots,H$',12,ha='center')
box(ax,6.2,1.35,2.5,1.4,r'$A_i$',r'$T\times T$; causal softmax')
arrow(ax,5.45,2.05,6.2,2.05)
label(ax,6.1,1.02,r'$Q_iK_i^\mathsf{T}/\sqrt{d_h}$',12,ha='center')
box(ax,9.45,1.35,2.1,1.4,r'$Z_i=A_iV_i$',r'$T\times d_h$')
arrow(ax,8.7,2.05,9.45,2.05)
box(ax,.4,3.65,4.15,1.05,r'$[Z_1\ \cdots\ Z_H]$',r'$T\times(Hd_h)$')
box(ax,5.35,3.65,2.25,1.05,r'$W^O$',r'$(Hd_h)\times D$')
box(ax,8.45,3.65,3.1,1.05,r'$O=\sum_i Z_iW_i^O$',r'$T\times D$')
arrow(ax,4.55,4.18,5.35,4.18); arrow(ax,7.6,4.18,8.45,4.18)
label(ax,.4,5.18,r'Example: $T=10,\ H=96,\ d_h=128,\ D=12288$',12)
label(ax,.4,5.64,'Attention weights have shape 96 x 10 x 10: one 10 x 10 matrix per head.',12,TEAL)
save(fig,'standard-attention-shapes')

# Comparison requested by the user: regular attention above, MLA below.
fig,ax=canvas(12,8.4)
label(ax,.35,.4,'FROM FULL KEY / VALUE CACHES TO A SHARED LATENT CACHE',16,weight='bold')
label(ax,.4,.98,'STANDARD ATTENTION',13,BLUE,weight='bold')
box(ax,.4,1.5,2.25,1.1,r'$K_i,\ V_i$',r'cache for every head',TEAL,GREEN)
box(ax,3.5,1.5,2.2,1.1,r'$q_{t,i}K_i^\mathsf{T}$','scores over past tokens')
box(ax,6.55,1.5,1.75,1.1,r'$a_{t,i}$','scale + softmax')
box(ax,9.1,1.5,2.5,1.1,r'$(a_{t,i}V_i)W_i^O$','sum outputs over heads')
arrow(ax,2.65,2.05,3.5,2.05); arrow(ax,5.7,2.05,6.55,2.05); arrow(ax,8.3,2.05,9.1,2.05)
label(ax,.4,3.04,r'Per token, per layer: $H(d_k+d_v)$ cached scalars.',12,TEAL)
ax.plot([.4,11.6],[3.45,3.45],color='#d8dfe6',lw=1)
label(ax,.4,3.92,'MLA: CONTENT PATH',13,BLUE,weight='bold')
box(ax,.4,4.5,2.25,1.15,r'$C=EW^{DKV}$',r'one shared $n\times r$ cache',TEAL,GREEN)
box(ax,3.5,4.5,2.2,1.15,r'$\widehat q_{t,i}C^\mathsf{T}$',r'$\widehat q_{t,i}=q_{t,i}U_{K,i}^\mathsf{T}$')
box(ax,6.55,4.5,1.75,1.15,r'$a_{t,i}$','scale + softmax')
box(ax,9.1,4.5,2.5,1.15,r'$(a_{t,i}C)T_i$',r'$T_i=U_{V,i}W_i^O$')
arrow(ax,2.65,5.075,3.5,5.075); arrow(ax,5.7,5.075,6.55,5.075); arrow(ax,8.3,5.075,9.1,5.075)
label(ax,.4,6.02,'Keys are absorbed into the query; values are projected after averaging.',12)
box(ax,.4,6.55,4.65,1.05,r'Full MLA also caches $K^R$',r'add the positional score $q^R_{t,i}(K^R)^{\mathsf{T}}$',ORANGE,GOLD)
label(ax,5.5,6.85,r'Per token, per layer: $r+d_R$ scalars.',12,TEAL)
label(ax,5.5,7.32,r'Content scale $\sqrt{d_h}$; full MLA scale $\sqrt{d_h+d_R}$.',11)
label(ax,.4,8.03,'Original diagram. Bias-free algebra; one query shown. The causal mask is applied before softmax.',10)
save(fig,'mha-to-mla')

def matrix(ax, x, y, a, cell=.42, hi=None):
    a=np.atleast_2d(a); m,n=a.shape
    for i in range(m):
        for j in range(n):
            if hi and hi(i,j): ax.add_patch(Rectangle((x+j*cell,y+i*cell),cell,cell,fc=GREEN,ec='none'))
            label(ax,x+(j+.5)*cell,y+(i+.5)*cell,str(a[i,j]),12,ha='center')
    for xx,sgn in [(x,1),(x+n*cell,-1)]:
        ax.plot([xx+sgn*.07,xx,xx,xx+sgn*.07],[y,y,y+m*cell,y+m*cell],color=INK,lw=1.2)
    return n*cell,m*cell

A=np.array([[1,2,0],[0,1,3]]); B=np.array([[2,1],[1,0],[0,2]]); P=A@B
fig,ax=canvas(12,7.2)
label(ax,.35,.4,'THREE VIEWS OF THE SAME MATRIX PRODUCT',17,weight='bold')
label(ax,.4,1.03,'Shared example',11)
matrix(ax,2.1,.72,A); label(ax,3.7,1.13,'x',14)
matrix(ax,4.2,.52,B); label(ax,5.5,1.13,'=',17); matrix(ax,6.1,.72,P)
label(ax,7.65,1.12,r'$A:2\times3,\ B:3\times2,\ AB:2\times2$',12)
ax.plot([.4,11.6],[1.85,1.85],color='#d8dfe6')
label(ax,.4,2.3,'1  ROW x COLUMN',13,BLUE,weight='bold')
label(ax,4.3,2.3,r'$(AB)_{ij}=\sum_k A_{ik}B_{kj}$',17)
label(ax,.4,2.87,'One scalar at a time',11)
label(ax,4.3,2.87,r'$(AB)_{12}=1(1)+2(0)+0(2)=1$',13)
ax.plot([.4,11.6],[3.25,3.25],color='#d8dfe6')
label(ax,.4,3.7,'2  MATRIX x EACH COLUMN',13,BLUE,weight='bold')
label(ax,4.3,3.7,r'$AB=[Ab_1\ \ Ab_2]$',17)
label(ax,.4,4.27,'One output vector at a time',11)
label(ax,4.3,4.27,r'$Ab_1=2A_{:1}+1A_{:2}+0A_{:3}=(4,1)^\mathsf{T}$',13)
ax.plot([.4,11.6],[4.65,4.65],color='#d8dfe6')
label(ax,.4,5.1,'3  SUM OF OUTER PRODUCTS',13,BLUE,weight='bold')
label(ax,4.3,5.1,r'$AB=\sum_k A_{:k}B_{k:}$',17)
label(ax,.4,5.67,'One rank-at-most-one matrix at a time',11)
matrix(ax,4.3,5.65,[[2,1],[0,0]]); label(ax,5.45,6.06,'+',17)
matrix(ax,5.85,5.65,[[2,0],[1,0]]); label(ax,7,6.06,'+',17)
matrix(ax,7.4,5.65,[[0,0],[0,6]]); label(ax,8.55,6.06,'=',17)
matrix(ax,8.95,5.65,P)
label(ax,.4,6.9,'The same index sum is grouped into scalars, columns, or whole matrices. Original numeric example.',10)
save(fig,'three-matrix-products')

# Tests target mathematical identities and common mistakes, not rendering code.
rng=np.random.default_rng(20261109)
def softmax(x):
    z=np.exp(x-np.max(x,axis=-1,keepdims=True)); return z/z.sum(axis=-1,keepdims=True)
checks={}
def check(name,a,b):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    assert np.allclose(a,b,rtol=1e-11,atol=1e-11),(name,err)
    checks[name]=err
check('three_product_views',A@B,sum(np.outer(A[:,k],B[k,:]) for k in range(3)))
check('column_view',A@B,np.column_stack([A@B[:,j] for j in range(2)]))
n,D,H,dh,r=5,7,3,2,3
E=rng.normal(size=(n,D)); C=E@rng.normal(size=(D,r))
mask=np.where(np.arange(n)[None,:]<=np.arange(n)[:,None],0.,-np.inf)
out_expanded=np.zeros((n,D)); out_latent=np.zeros((n,D)); heads=[]; blocks=[]; scores=[]
for i in range(H):
    Q=E@rng.normal(size=(D,dh)); UK=rng.normal(size=(r,dh)); UV=rng.normal(size=(r,dh)); WO=rng.normal(size=(dh,D))
    K=C@UK; V=C@UV; score=Q@K.T
    check(f'key_absorption_{i}',score,(Q@UK.T)@C.T)
    weights=softmax(score/np.sqrt(dh)+mask)
    check(f'causal_weights_sum_{i}',weights.sum(axis=1),np.ones(n))
    assert np.count_nonzero(np.triu(weights,1))==0
    scol=K@Q.T/np.sqrt(dh)+mask.T
    ecol=np.exp(scol-np.max(scol,axis=0,keepdims=True))
    check(f'column_token_convention_{i}',weights.T,ecol/ecol.sum(axis=0,keepdims=True))
    check(f'value_absorption_{i}',(weights@V)@WO,(weights@C)@(UV@WO))
    heads.append(weights@V); blocks.append(WO); scores.append(score)
    out_expanded+=(weights@V)@WO; out_latent+=(weights@C)@(UV@WO)
check('all_head_mla_output',out_expanded,out_latent)
check('concat_equals_sum_of_blocks',np.concatenate(heads,axis=1)@np.concatenate(blocks,axis=0),out_expanded)
pooled=softmax(sum(scores)/np.sqrt(dh)+mask)
assert not np.allclose(pooled,softmax(scores[0]/np.sqrt(dh)+mask))
checks['pooled_heads_counterexample']=True
# Disjoint positional features: concatenated dot product equals two dot products.
qc=rng.normal(size=(1,dh)); kc=rng.normal(size=(n,dh))
qr=rng.normal(size=(1,2)); kr=rng.normal(size=(n,2))
check('decoupled_content_and_position',np.concatenate([qc,qr],axis=1)@np.concatenate([kc,kr],axis=1).T,qc@kc.T+qr@kr.T)
checks['cache_bytes_example']={name:int(61*2*width) for name,width in {
    'MHA_H128':2*128*128,'GQA_G16':2*16*128,'MQA':2*128,
    'MLA_content':512,'MLA_with_position':512+64,'identity_latent_D12288':12288}.items()}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,indent=2))
