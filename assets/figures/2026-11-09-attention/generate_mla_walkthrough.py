"""Expanded MLA matrix walkthrough, matching the standard-attention vector style.

Sources: the user's attention.pdf and 2026-11-09 comparison screenshot;
DeepSeek-V2 §§2.1.2-2.1.3 and Appendix C; Welch Labs 0VLAoVGf_74,
especially 7:35-10:44 and 13:36-16:14. Drawings are original.
Run with numpy and matplotlib. Existing standard-attention assets are untouched.
"""
from mla_vector_style import *

def product(ax,y,left,left_name,weight_name,right,right_name,
            left_cols,output_cols,left_color=BLUE,right_color=TEAL,rows='10',h=1.8):
    inds=(11,) if rows=='1' else (1,2,None,10)
    rowmat(ax,.8,y,3.5,h,left,left_name,rows=rows,cols=left_cols,color=left_color,inds=inds)
    eq(ax,5.35,y+h/2,r'\times',25)
    weight(ax,6.0,y,1.6,h,weight_name,left_cols,output_cols)
    eq(ax,8.9,y+h/2,'=',25)
    rowmat(ax,9.6,y,4.15,h,right,right_name,rows=rows,cols=output_cols,color=right_color,inds=inds)

def parens(ax,x,y,w,h,color=GREY):
    for xx,sgn in [(x,1),(x+w,-1)]:
        points=[(xx+sgn*.18,y),(xx-sgn*.26,y+h*.25),
                (xx-sgn*.26,y+h*.75),(xx+sgn*.18,y+h)]
        ax.add_patch(PathPatch(MPath(points,[MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4]),
                               fill=False,edgecolor=color,lw=1.35))

# 01: all four projection products are drawn, including the query branch.
fig,ax=page('MLA 01','Input rows become queries and a shared cache',
            'Notebook dimensions: 10 tokens, D = 12,288, r = 512, d_h = 128. One fixed head i; no bias or position yet.',17.2)
step(ax,1.65,'1','Compress the token rows once; every head uses the same C')
product(ax,3.05,'e','E',r'W^{DKV}','c','C','12,288','512')
txt(ax,9.65,5.22,'CACHE these latent rows',12,TEAL,weight='bold')
step(ax,5.9,'2','Project queries separately for this head')
product(ax,7.25,'e','E',r'W_i^Q','q','Q_i','12,288','128',right_color=BLUE)
step(ax,9.8,'3','The shared latent rows define this head’s keys')
product(ax,11.15,'c','C',r'U_{K,i}','k','K_i','512','128',left_color=TEAL,right_color=BLUE)
step(ax,13.6,'4','The same latent rows define this head’s values')
product(ax,14.95,'c','C',r'U_{V,i}','v','V_i','512','128',left_color=TEAL,right_color=ORANGE,h=1.35)
save(fig,'mla-01-projections')

# 02: show the absorbed query as actual rows, and draw both fixed-map factors.
fig,ax=page('MLA 02','Move the key map to the query side',
            'Associativity changes the parentheses. The transpose reverses the order of C and U_K.',20.6)
step(ax,1.65,'1','Start from the same query-key scores')
eq(ax,.8,2.25,r'Q_iK_i^{\mathsf T}=Q_i(CU_{K,i})^{\mathsf T}=Q_iU_{K,i}^{\mathsf T}C^{\mathsf T}',23)
rowmat(ax,.8,3.75,3.1,1.8,'q','Q_i',cols='128')
eq(ax,4.95,4.65,r'\times',25)
weight(ax,5.65,3.75,1.8,1.8,r'U_{K,i}^{\mathsf T}','128','512')
eq(ax,8.6,4.65,r'\times',25)
colmat(ax,9.3,3.25,2.5,2.8,r'c_{k}^{\mathsf T}',r'C^{\mathsf T}',rows='512',cols='10',size=14)
brace(ax,.85,6.4,6.6,r'$\widehat Q_i=Q_iU_{K,i}^{\mathsf T}$',side=-1,color=BLUE)
step(ax,7.5,'2','The product is a new row for every query')
product(ax,8.85,'q','Q_i',r'U_{K,i}^{\mathsf T}',r'\widehat q_{k}',r'\widehat Q_i','128','512')
eq(ax,.8,11.27,r'\widehat q_1=q_1U_{K,i}^{\mathsf T},\quad \widehat q_2=q_2U_{K,i}^{\mathsf T},\quad\ldots,\quad \widehat q_{10}=q_{10}U_{K,i}^{\mathsf T}',20)
step(ax,12.15,'3','For the notebook’s linear query map, combine the fixed weights')
weight(ax,.8,13.35,3.0,1.6,r'W_i^Q','12,288','128')
eq(ax,5.2,14.15,r'\times',25)
weight(ax,5.9,13.35,2.3,1.6,r'U_{K,i}^{\mathsf T}','128','512')
eq(ax,9.3,14.15,'=',25)
weight(ax,10.0,13.35,3.3,1.6,r'B_i','12,288','512',color=ORANGE)
step(ax,15.75,'4','Apply the combined map directly to the input rows')
product(ax,17.1,'e','E','B_i',r'\widehat q_{k}',r'\widehat Q_i','12,288','512')
eq(ax,.8,19.55,r'\widehat Q_i=E(W_i^QU_{K,i}^{\mathsf T})=EB_i,\qquad Q_iK_i^{\mathsf T}=\widehat Q_iC^{\mathsf T}',20)
save(fig,'mla-02-key-absorption')

# 03: full causal weight staircase, then actual A C rows.
fig,ax=page('MLA 03','The weights average cached latent rows',
            'The score staircase becomes the same causal weight staircase as standard attention. Here it multiplies C.',17.8)
eq(ax,.8,1.85,r'\alpha_{ts}=\frac{\exp(\widehat q_t c_s^{\mathsf T}/\sqrt{128})}{\sum_{u=1}^{t}\exp(\widehat q_t c_u^{\mathsf T}/\sqrt{128})}\quad(s\leq t)',22)
eq(ax,10.6,1.85,r'\alpha_{ts}=0\quad(s>t)',18)
entries=[['1' if t==s==1 else (rf'\alpha_{{{t},{s}}}' if s<=t else '0')
          for s in range(1,11)] for t in range(1,11)]
grid(ax,1.15,3.6,13.15,5.0,entries,name=r'A_i=\mathrm{softmax}_{row}(S_i)',
     rowdim='10',coldim='10',colors=lambda i,j:PALE if j>i else GREEN,fontsize=13)
step(ax,9.05,'1','Multiply by the cache; each output row is a weighted latent vector')
weight(ax,.8,10.4,2.5,1.95,'A_i','10','10',color=BLUE)
eq(ax,4.45,11.37,r'\times',25)
rowmat(ax,5.15,10.4,3.5,1.95,'c','C',cols='512',color=TEAL)
eq(ax,9.8,11.37,'=',25)
rowmat(ax,10.4,10.4,3.7,1.95,'h','H_i',cols='512',color=TEAL)
step(ax,13.0,'2','Expand the first, second, and last rows')
eq(ax,.85,13.65,r'h_1=1c_1+0c_2+\cdots+0c_{10}=c_1',22)
eq(ax,.85,14.4,r'h_2=\alpha_{21}c_1+\alpha_{22}c_2',22)
eq(ax,.85,15.15,r'h_{10}=\alpha_{10,1}c_1+\alpha_{10,2}c_2+\cdots+\alpha_{10,10}c_{10}',22)
eq(ax,.85,16.0,r'h_t=\sum_{s=1}^{t}\alpha_{ts}c_s,\qquad \sum_{s=1}^{t}\alpha_{ts}=1',22)
txt(ax,.85,16.93,'C is shared across heads. H_i differs by head because each head has its own attention weights A_i.',12,TEAL)
save(fig,'mla-03-weights-and-latents')

# 04: expand every output product; keep the head sum explicit.
fig,ax=page('MLA 04','Map each latent average to the output',
            'All rows below refer to one head i. Its attention weights are held fixed while the matrix products are regrouped.',24.5)
step(ax,1.65,'1','Turn each weighted latent row into a value-space output')
product(ax,3.0,'h','H_i',r'U_{V,i}','z','Z_i','512','128',left_color=TEAL,right_color=ORANGE)
step(ax,5.55,'2','Project those rows back to the model width')
product(ax,6.9,'z','Z_i',r'W_i^O',r'o_{k,i}','O_i','128','12,288',left_color=ORANGE,right_color=BLUE)
step(ax,9.45,'3','Group the two fixed maps, then apply the result to H_i')
weight(ax,.8,10.75,3.3,1.7,r'U_{V,i}','512','128',color=ORANGE)
eq(ax,5.2,11.6,r'\times',25)
weight(ax,5.9,10.75,2.3,1.7,r'W_i^O','128','12,288')
eq(ax,9.6,11.6,'=',25)
weight(ax,10.3,10.75,3.3,1.7,'T_i','512','12,288',color=BLUE)
product(ax,14.05,'h','H_i','T_i',r'o_{k,i}','O_i','512','12,288',left_color=TEAL,right_color=BLUE)
eq(ax,.8,16.48,r'o_{t,i}=\left(\sum_{s=1}^{t}\alpha_{ts}(c_sU_{V,i})\right)W_i^O'
   r'=\left(\sum_{s=1}^{t}\alpha_{ts}c_s\right)(U_{V,i}W_i^O)',20)
txt(ax,.85,17.22,'Averaging first avoids expanding every historical value. T_i may also be applied as its two factors.',12,TEAL)
step(ax,18.05,'4','Combine heads: concatenation and output projection equal a sum')
grid(ax,.85,19.9,5.4,1.7,[[r'Z_1',r'Z_2',r'\cdots',r'Z_H']],name=r'Z_{cat}',
     rowdim='10',coldim='H x 128',fontsize=20)
eq(ax,7.4,20.75,r'\times',25)
grid(ax,8.1,19.5,3.0,2.5,[[r'W_1^O'],[r'W_2^O'],[r'\vdots'],[r'W_H^O']],
     name='W^O',rowdim='H x 128',coldim='12,288',fontsize=17)
eq(ax,12.75,20.75,'=O',23)
eq(ax,.85,22.65,r'O=\sum_{i=1}^{H}O_i=\sum_{i=1}^{H}H_iT_i,\qquad o_t=\sum_{i=1}^{H}o_{t,i}',23)
txt(ax,.85,23.4,'O has 10 rows and 12,288 columns. In the notebook example H = 96; the surrounding block can add E + O.',12)
save(fig,'mla-04-value-and-output')

# 05: newest-query decoding, with n=11 and a single newly appended cache row.
fig,ax=page('MLA 05','Process token 11 with one query row',
            'Fix one head. The ten previous token states are unchanged; n = 11 includes the current token after appending c_11.',23.1)
step(ax,1.65,'1','Append one latent row to the shared cache')
rowmat(ax,.85,3.05,4,2.0,'c',r'C_{1:10}',rows='10',cols='512',color=TEAL)
eq(ax,6.1,3.9,r'\longrightarrow',27)
ax.add_patch(Rectangle((8.0,4.9),4.7,.55,facecolor=GOLD,edgecolor='none'))
rowmat(ax,8.0,2.8,4.7,2.65,'c',r'C_{1:11}',rows='11',cols='512',
       inds=(1,2,None,10,11),color=TEAL)
eq(ax,.85,5.95,r'c_{11}=e_{11}W^{DKV},\qquad \widehat q_{11}=q_{11}U_{K,i}^{\mathsf T}=e_{11}B_i',21)
step(ax,6.8,'2','One query times all cached columns gives the new score row')
rowmat(ax,.85,8.55,4.1,.7,r'\widehat q_{k}',r'\widehat q_{11}',rows='1',cols='512',inds=(11,))
eq(ax,6.0,8.9,r'\times',25)
colmat(ax,6.8,8.2,2.8,2.0,r'c_{k}^{\mathsf T}',r'C_{1:11}^{\mathsf T}',
       rows='512',cols='11',inds=(1,2,None,11),size=15)
eq(ax,10.8,8.9,r'\longrightarrow s_{11}',22)
grid(ax,.85,11.0,13.5,.85,[[r'\widehat q_{11}c_1^{\mathsf T}/\sqrt{128}',
     r'\widehat q_{11}c_2^{\mathsf T}/\sqrt{128}',r'\cdots',
     r'\widehat q_{11}c_{11}^{\mathsf T}/\sqrt{128}']],rowdim='1',coldim='11',fontsize=17)
step(ax,12.7,'3','Normalize this row and average the same cache')
eq(ax,.85,13.35,r'a_{11}=\mathrm{softmax}(s_{11})=[\alpha_{11,1}\ \alpha_{11,2}\ \cdots\ \alpha_{11,11}]',20)
weight(ax,.85,14.7,3.4,.7,r'a_{11}','1','11',color=BLUE)
eq(ax,5.3,15.05,r'\times',25)
rowmat(ax,6,14.1,3.4,1.9,'c',r'C_{1:11}',rows='11',cols='512',inds=(1,2,None,11),color=TEAL)
eq(ax,10.55,15.05,'=',25)
rowmat(ax,11.2,14.7,3.0,.7,'h',r'h_{11,i}',rows='1',cols='512',inds=(11,),color=TEAL)
eq(ax,.85,16.7,r'h_{11,i}=\alpha_{11,1}c_1+\alpha_{11,2}c_2+\cdots+\alpha_{11,11}c_{11}',22)
step(ax,17.6,'4','Project that one row; sum the head contributions')
product(ax,19.0,'h',r'h_{11,i}','T_i',r'o_{k,i}',r'o_{11,i}','512','12,288',
        left_color=TEAL,right_color=BLUE,rows='1',h=.85)
eq(ax,.85,21.0,r'o_{11}=\sum_{i=1}^{H}h_{11,i}T_i',24)
txt(ax,.85,21.9,'Only the current query is needed. Each decode step scores n cached tokens; a complete n-token sequence still sums many steps.',12,TEAL)
save(fig,'mla-05-single-query-decode')

# 06: faithful reconstruction of the supplied two-case before/after comparison.
fig,ax=page('MLA 06','Your comparison: reconstruct keys, or transform one query',
            'One current query q_11,i; n available cached tokens (n = 11 in the drawing). Bias-free, position-free algebra.',17.8,w=24)
step(ax,1.65,'A','MLA: cached token width r = 512')
txt(ax,.8,2.35,'EXPAND ALL n KEYS, THEN SCORE',14,BLUE,weight='bold')
txt(ax,12.6,2.35,'TRANSFORM ONE QUERY, THEN READ THE LATENT CACHE',14,TEAL,weight='bold')
def comparison(y,width,cache,cache_sym,keymap):
    rowmat(ax,.7,y+.55,1.35,.5,r'q_{k,i}',r'q_{11,i}',rows='1',cols='128',inds=(11,),size=14)
    eq(ax,2.95,y+.8,r'\times',24)
    rowmat(ax,3.7,y,2.3,1.6,cache_sym,cache,rows='n',cols=width,inds=(1,2,None,'n'),color=TEAL,size=16)
    eq(ax,7.1,y+.8,r'\times',24)
    weight(ax,7.7,y,1.35,1.6,keymap,width,'128')
    parens(ax,3.55,y-.2,6.8,2.0)
    eq(ax,10.55,y-.25,r'\mathsf{T}',17)
    eq(ax,11.2,y+.8,'=',26)
    rowmat(ax,12.3,y+.55,1.35,.5,r'q_{k,i}',r'q_{11,i}',rows='1',cols='128',inds=(11,),size=14)
    eq(ax,14.7,y+.8,r'\times',24)
    weight(ax,15.35,y+.15,2.6,1.3,'('+keymap+r')^{\mathsf T}','128',width)
    eq(ax,19.0,y+.8,r'\times',24)
    colmat(ax,19.7,y-.15,2.0,2.0,cache_sym+r'_{k}^{\mathsf T}',cache+r'^{\mathsf T}',
           rows=width,cols='n',inds=(1,2,None,'n'),size=15)
    brace(ax,12.3,y+2.15,5.65,'transformed query: 1 x '+width,side=-1,color=TEAL)
comparison(3.65,'512','C','c',r'U_{K,i}')
eq(ax,.8,6.55,r'q_{11,i}(CU_{K,i})^{\mathsf T}=(q_{11,i}U_{K,i}^{\mathsf T})C^{\mathsf T}\quad\in\mathbb{R}^{1\times n}',24)
txt(ax,.8,7.3,'Given cached C and q: n·512·128 + n·128 multiply-adds on the left; 128·512 + n·512 on the right.',14)
txt(ax,.8,7.9,'The regrouping avoids reconstructing n keys for this query. A conventional already-cached MHA key dot product is only width 128.',13,ORANGE)
ax.plot([.55,23.45],[8.45,8.45],lw=1,color=RULE)
step(ax,9.0,'B','Your proposal: cache X itself, so the token width is D = 12,288')
comparison(11.0,'12,288','X','x',r'W_i^K')
eq(ax,.8,13.9,r'q_{11,i}(XW_i^K)^{\mathsf T}=(q_{11,i}(W_i^K)^{\mathsf T})X^{\mathsf T}\quad\in\mathbb{R}^{1\times n}',24)
eq(ax,.8,14.75,r'\mathrm{value\ side:}\quad o_{11,i}=(a_{11,i}X)(W_i^VW_i^O)',24)
txt(ax,.8,15.5,'With D = H d_h = 12,288, caching X stores 12,288 scalars per token/layer instead of 2H d_h = 24,576: half.',14,TEAL)
txt(ax,.8,16.15,'The history-scoring dot product now has width 12,288. MLA uses a learned 512-coordinate cache to avoid that wide shared representation.',14)
txt(ax,.8,16.8,'Notation: X = E in this note. In the lower case U_K,i in the handwriting is the ordinary full-width key map W_i^K.',12,GREY)
save(fig,'mla-06-handwritten-comparison')

# 07: paper-specific branches, separated from the notebook's linear-only derivation.
fig,ax=page('MLA 07','Restore the separate positional score',
            'DeepSeek-V2 §§2.1.2-2.1.3, Appendix C. The 10-token matrices use r = 512, d_h = 128 and d_R = 64.',20.0)
step(ax,1.45,'1','Content score: transformed query rows read the latent cache')
rowmat(ax,.85,3.2,4.3,1.9,r'\widehat q_{k}',r'\widehat Q_i',cols='512')
eq(ax,6.3,4.15,r'\times',25)
colmat(ax,7.05,2.75,2.45,2.8,r'c_{k}^{\mathsf T}',r'C^{\mathsf T}',rows='512',cols='10',size=15)
eq(ax,10.65,4.15,r'\longrightarrow L_i^C',22)
step(ax,6.0,'2','Position score: position-encoded query rows read the shared positional keys')
rowmat(ax,.85,7.9,4.3,1.9,r'q^R_{k}',r'Q_i^R',cols='64',color=ORANGE)
eq(ax,6.3,8.85,r'\times',25)
colmat(ax,7.05,7.45,2.45,2.8,r'(k^R_{k})^{\mathsf T}',r'(K^R)^{\mathsf T}',rows='64',cols='10',size=14,color=ORANGE)
eq(ax,10.65,8.85,r'\longrightarrow L_i^R',22)
step(ax,11.1,'3','Add the two score matrices, then scale, mask, and normalize')
eq(ax,.85,11.8,r'S_i=\frac{L_i^C+L_i^R}{\sqrt{128+64}}+M'
   r'=\frac{\widehat Q_iC^{\mathsf T}+Q_i^R(K^R)^{\mathsf T}}{\sqrt{192}}+M',22)
eq(ax,.85,12.65,r'A_i=\mathrm{softmax}_{row}(S_i),\qquad O_i=(A_iC)(U_{V,i}W_i^O)',23)
txt(ax,.85,13.38,'Cache C (512 coordinates) and K^R (64 coordinates) per token: 576 shared scalars in each layer.',13,TEAL)
step(ax,14.25,'4','With a compressed query branch, absorb only the adjacent linear maps')
eq(ax,.85,14.95,r'C^Q:\ 10\times r_Q,\qquad Q_i=C^Q U_{Q,i},\quad U_{Q,i}:\ r_Q\times128',21)
eq(ax,.85,15.72,r'\widehat Q_i=C^Q(U_{Q,i}U_{K,i}^{\mathsf T})\quad(10\times r_Q)(r_Q\times512)',22)
eq(ax,.85,16.5,r'Q_i^R=\mathrm{RoPE}(C^QW_i^{QR}),\qquad K^R=\mathrm{RoPE}(EW^{KR})',21)
txt(ax,.85,17.27,'C^Q is the query latent; r_Q is its width. Each head has its own U_Q,i and W_i^QR. K^R is shared.',12)
txt(ax,.85,17.88,'Use the resulting C and C^Q after any latent normalization. Nonlinear normalization cannot be absorbed into a fixed matrix.',12,ORANGE)
txt(ax,.85,18.5,'Keeping RoPE on a separate branch lets the content-key map remain adjacent to the query map.',12)
save(fig,'mla-07-position-and-query')

# Independent checks of the identities illustrated, including a new decoding row.
rng=np.random.default_rng(20261110)
T,D,r,d,H,dR=11,19,7,4,3,2
X=rng.normal(size=(T,D))/np.sqrt(D)
WD=rng.normal(size=(D,r))/np.sqrt(D)
C=X@WD
mask=np.triu(np.full((T,T),-np.inf),1)
def sm(s):
    ex=np.exp(s-s.max(axis=-1,keepdims=True))
    return ex/ex.sum(axis=-1,keepdims=True)
errs=[]
head_outputs=[]; head_z=[]; head_wo=[]
for _ in range(H):
    WQ=rng.normal(size=(D,d)); UK=rng.normal(size=(r,d))
    UV=rng.normal(size=(r,d)); WO=rng.normal(size=(d,D))
    Q=X@WQ; K=C@UK; V=C@UV; Qhat=Q@UK.T; B=WQ@UK.T
    A=sm(Q@K.T/np.sqrt(d)+mask)
    Alat=sm(Qhat@C.T/np.sqrt(d)+mask)
    expanded=A@V@WO; latent=(Alat@C)@(UV@WO)
    errs += [np.max(abs(Q@K.T-Qhat@C.T)),np.max(abs(Qhat-X@B)),np.max(abs(expanded-latent))]
    one=sm((Qhat[-1:]@C.T)/np.sqrt(d))
    errs += [np.max(abs(one-A[-1:])),np.max(abs((one@C)@(UV@WO)-expanded[-1:]))]
    WK=rng.normal(size=(D,d)); WV=rng.normal(size=(D,d))
    errs += [np.max(abs(Q[-1:]@(X@WK).T-(Q[-1:]@WK.T)@X.T)),
             np.max(abs((A@(X@WV))@WO-(A@X)@(WV@WO)))]
    QR=rng.normal(size=(T,dR)); KR=rng.normal(size=(T,dR))
    fullQ=np.concatenate([Q,QR],axis=1); fullK=np.concatenate([K,KR],axis=1)
    errs += [np.max(abs(fullQ@fullK.T-(Qhat@C.T+QR@KR.T)))]
    CQ=rng.normal(size=(T,9)); UQ=rng.normal(size=(9,d))
    errs += [np.max(abs((CQ@UQ)@UK.T-CQ@(UQ@UK.T)))]
    assert np.allclose(A.sum(axis=1),1) and np.all(A[np.triu_indices(T,1)]==0)
    head_outputs.append(expanded);head_z.append(A@V);head_wo.append(WO)
errs += [np.max(abs(np.concatenate(head_z,axis=1)@np.concatenate(head_wo,axis=0)-sum(head_outputs)))]
assert max(errs)<1e-11,max(errs)
assert np.allclose(C[:-1],X[:-1]@WD)
REPORT['checks']={'rectangular_dimensions':{'tokens':T,'input_width':D,'latent_width':r,'head_width':d,'heads':H,'position_width':dR},
                  'max_abs_error':float(max(errs)),'identities_checked':len(errs),
                  'mask_and_row_sums':True,'new_query_matches_full_last_row':True,
                  'new_cache_preserves_old_rows':True,
                  'checks_are_supporting_examples':'The displayed associativity and transpose identities give the general proof.'}
(OUT/'mla-walkthrough-checks.json').write_bytes((json.dumps(REPORT,indent=2)+'\n').encode())
print(json.dumps(REPORT['checks'],indent=2))
