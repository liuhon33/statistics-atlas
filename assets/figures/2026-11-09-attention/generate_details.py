"""Detailed, original vector reconstructions of every algebraic route in attention.pdf.

Run with numpy and matplotlib. Tokens are rows except in the explicitly labelled
column-convention figure. Matrix drawings are schematic, not to physical scale.
All mathematical text is exported as vector paths for portable SVG rendering.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MPath

OUT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,
                     'svg.fonttype':'path','mathtext.fontset':'dejavusans'})
INK='#25364a'; BLUE='#3269a5'; TEAL='#167e78'; ORANGE='#ae641c'
GREY='#68788b'; RULE='#d9e1e9'; PALE='#edf4fc'; GREEN='#e9f5f1'; GOLD='#fff3df'
REPORT={}

def txt(ax,x,y,s,size=13,color=INK,ha='left',**kw):
    return ax.text(x,y,s,fontsize=size,color=color,ha=ha,va='center',**kw)

def eq(ax,x,y,s,size=21,color=INK,ha='left'):
    return txt(ax,x,y,'$'+s.replace(r'\mathsf T',r'\mathsf{T}')+'$',size,color,ha)

def page(number,title,subtitle,h):
    fig,ax=plt.subplots(figsize=(16,h),dpi=140)
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    ax.set(xlim=(0,16),ylim=(h,0)); ax.axis('off')
    fig.patch.set_facecolor('white')
    code=f'{number:02d}' if isinstance(number,int) else str(number)
    txt(ax,.55,.48,f'{code}  {title}',23,BLUE,weight='bold')
    txt(ax,.55,1.03,subtitle,12)
    txt(ax,.55,h-.34,'Original Codex reconstruction from attention.pdf. Braces give dimensions; drawing proportions are schematic.',10,GREY)
    return fig,ax

def rule(ax,y):
    ax.plot([.55,15.45],[y,y],lw=1,color=RULE)

def step(ax,y,n,s):
    txt(ax,.55,y,f'{n}  {s}',16,BLUE,weight='bold')

def arrow(ax,x1,y1,x2,y2,color=GREY):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),
                arrowprops={'arrowstyle':'-|>','lw':1.5,'color':color,'shrinkA':4,'shrinkB':4})

def brace(ax,x,y,length,label,orient='h',color=GREY,side=1):
    # Two cusp-shaped halves, transformed into a horizontal or vertical brace.
    d=.14
    v=[(0,0),(.07*length,0),(.02*length,-d),(.20*length,-d),
       (.43*length,-d),(.47*length,-d),(.50*length,-2*d),
       (.53*length,-d),(.57*length,-d),(.80*length,-d),
       (.98*length,-d),(.93*length,0),(length,0)]
    if orient=='h': points=[(x+a,y+side*b) for a,b in v]
    else: points=[(x-side*b,y+a) for a,b in v]
    codes=[MPath.MOVETO]+[MPath.CURVE4]*12
    ax.add_patch(PathPatch(MPath(points,codes),fill=False,lw=1.1,edgecolor=color))
    if orient=='h': txt(ax,x+length/2,y-side*.45,label,12,color,ha='center')
    else: txt(ax,x+side*.42,y+length/2,label,12,color,ha='left' if side>0 else 'right')

def brackets(ax,x,y,w,h,color=INK):
    for xx,sgn in [(x,1),(x+w,-1)]:
        ax.plot([xx+sgn*.13,xx,xx,xx+sgn*.13],
                [y,y,y+h,y+h],lw=1.45,color=color)

def vector_label(sym,k):
    if '{k}' in sym: return sym.replace('{k}','{'+str(k)+'}')
    if ':' in sym: return sym
    return sym+'_{'+str(k)+'}'

def rowmat(ax,x,y,w,h,sym,name,rows='10',cols='128',inds=(1,2,None,10),color=BLUE,br=True,size=16):
    brackets(ax,x,y,w,h,color)
    if name: eq(ax,x+w/2,y-.93,name,19,color,ha='center')
    if br:
        brace(ax,x+.07,y-.18,w-.14,cols)
        brace(ax,x+w+.14,y+.03,h-.06,rows,orient='v')
    for j,k in enumerate(inds):
        yy=y+h*(j+.5)/len(inds)
        if k is None:
            eq(ax,x+w/2,yy,r'\vdots',size,ha='center',color=GREY)
        else:
            lab=vector_label(sym,k)
            mid=x+w/2; gap=min(.43,w*.24)
            ax.plot([x+.19,mid-gap],[yy,yy],color=color,lw=.9)
            ax.plot([mid+gap,x+w-.19],[yy,yy],color=color,lw=.9)
            eq(ax,mid,yy,lab,size,color,ha='center')
    return x+w,y+h

def colmat(ax,x,y,w,h,sym,name,rows='128',cols='10',inds=(1,2,None,10),color=TEAL,br=True,size=15):
    brackets(ax,x,y,w,h,color)
    if name: eq(ax,x+w/2,y-.93,name,19,color,ha='center')
    if br:
        brace(ax,x+.07,y-.18,w-.14,cols)
        brace(ax,x+w+.14,y+.03,h-.06,rows,orient='v')
    for j,k in enumerate(inds):
        xx=x+w*(j+.5)/len(inds)
        if k is None: eq(ax,xx,y+h/2,r'\cdots',size,ha='center',color=GREY)
        else:
            lab=vector_label(sym,k)
            mid=y+h/2
            ax.plot([xx,xx],[y+.16,mid-.34],color=color,lw=.9)
            ax.plot([xx,xx],[mid+.34,y+h-.16],color=color,lw=.9)
            eq(ax,xx,mid,lab,size,color,ha='center')
    return x+w,y+h

def weight(ax,x,y,w,h,name,rows,cols,color=GREY):
    brackets(ax,x,y,w,h,color)
    eq(ax,x+w/2,y+h/2,name,20,color,ha='center')
    brace(ax,x+.07,y-.18,w-.14,cols,color=color)
    brace(ax,x+w+.14,y+.03,h-.06,rows,orient='v',color=color)

def grid(ax,x,y,w,h,entries,name='',rowdim='',coldim='',colors=None,fontsize=15):
    m,n=len(entries),len(entries[0]); cw,ch=w/n,h/m
    if name: eq(ax,x+w/2,y-.96,name,21,ha='center')
    for i in range(m):
        for j in range(n):
            fill=colors(i,j) if colors else ('#f6f9fc' if (i+j)%2==0 else 'white')
            ax.add_patch(Rectangle((x+j*cw,y+i*ch),cw,ch,facecolor=fill,edgecolor='white',lw=2))
            eq(ax,x+(j+.5)*cw,y+(i+.5)*ch,entries[i][j],fontsize,ha='center')
    brackets(ax,x-.05,y-.03,w+.1,h+.06)
    if coldim: brace(ax,x,y-.18,w,coldim)
    if rowdim: brace(ax,x+w+.18,y,h,rowdim,orient='v')

def save(fig,name):
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    fw,fh=fig.canvas.get_width_height()
    outside=[]
    for ax in fig.axes:
        for t in ax.texts:
            b=t.get_window_extent(renderer)
            if b.x0 < -1 or b.y0 < -1 or b.x1 > fw+1 or b.y1 > fh+1:
                outside.append(t.get_text())
    assert not outside,(name,'clipped text',outside)
    fig.savefig(OUT/(name+'.svg'),facecolor='white')
    fig.savefig(OUT/(name+'.png'),facecolor='white')
    REPORT[name]={'canvas_inches':list(fig.get_size_inches()),'text_within_canvas':True}
    plt.close(fig)

# 1. The exact E-row picture, branching into Q, K and V.
fig,ax=page(1,'Token rows become queries, keys, and values',
            r'One fixed head i. T = 10 tokens, D = 12,288 features, $d_h=128$. Write $q_t$ for $q_{t,i}$.',16)
rowmat(ax,5.5,2.65,4,2,'e','E',cols='12,288')
txt(ax,10.4,3.1,'Each long row is one token.',13)
txt(ax,10.4,3.55,'The shared input feeds all three branches.',12)
for y,letter,color in [(6.1,'Q',BLUE),(9.65,'K',TEAL),(13.2,'V',ORANGE)]:
    rowmat(ax,.8,y,3.6,1.8,'e','E',cols='12,288')
    eq(ax,5.45,y+.9,r'\times',25)
    weight(ax,6.05,y,1.55,1.8,r'W_i^'+letter,'12,288','128')
    eq(ax,8.9,y+.9,'=',25)
    rowmat(ax,9.6,y,4.3,1.8,letter.lower(),letter+'_i',cols='128',color=color)
eq(ax,.65,15.25,r'q_t=e_tW_i^Q,\qquad k_t=e_tW_i^K,\qquad v_t=e_tW_i^V',18)
save(fig,'detail-01-token-projections')

# 2. Q horizontally, K^T vertically; every 10x10 masked score is shown.
fig,ax=page(2,'Dot products form the causal score staircase',
            'One head. Query t labels a row; key s labels a column. Future keys have s > t.',15.6)
rowmat(ax,.8,2.75,4.6,2.1,'q','Q_i',cols='128')
eq(ax,6.55,3.8,r'\times',28)
colmat(ax,7.35,2.35,2.45,3.2,r'k_{k}^{\mathsf T}',r'K_i^{\mathsf T}',rows='128',cols='10',size=14)
eq(ax,11.15,3.15,r'(Q_iK_i^{\mathsf T})_{ts}',19)
eq(ax,11.15,3.8,r'=q_tk_s^{\mathsf T}',22)
eq(ax,11.15,4.55,r'(10\times128)(128\times10)',14)
txt(ax,.8,5.85,'Scale by 1 / sqrt(128), then mask the strictly upper triangle.',14)
eq(ax,.8,6.4,r'S_i=\left(Q_iK_i^{\mathsf T}+M\right)/\sqrt{128}',21)
txt(ax,8.7,6.4,'M = 0 if s <= t; otherwise -infinity.',12)
entries=[[rf'q_{{{t}}}k_{{{s}}}^{{\mathsf T}}' if s<=t else r'-\infty'
          for s in range(1,11)] for t in range(1,11)]
grid(ax,1.15,7.65,13.15,5.4,entries,rowdim='10',coldim='10',
     colors=lambda i,j:GOLD if j>i else GREEN,fontsize=12)
txt(ax,1.15,13.48,'The displayed matrix is Q_i K_i^T + M. Divide the entire matrix by sqrt(128) to obtain S_i.',12)
eq(ax,.8,14.15,r'S_{i,1:}=[q_1k_1^{\mathsf T}/\sqrt{128},-\infty,\ldots,-\infty]',18)
eq(ax,.8,14.8,r'S_{i,10:}=[q_{10}k_1^{\mathsf T},q_{10}k_2^{\mathsf T},\ldots,q_{10}k_{10}^{\mathsf T}]/\sqrt{128}',18)
save(fig,'detail-02-causal-scores')

# 3. Weights and their application to all token values.
fig,ax=page(3,'Softmax weights mix value rows',
            'A_i is the normalized weight matrix. Its future-token entries are zero, and every row sums to one.',17.3)
eq(ax,.8,1.85,r'\alpha_{ts}=\frac{\exp(q_tk_s^{\mathsf T}/\sqrt{128})}{\sum_{u=1}^{t}\exp(q_tk_u^{\mathsf T}/\sqrt{128})}\quad(s\leq t)',22)
eq(ax,10.2,1.85,r'\alpha_{ts}=0\quad(s>t)',18)
entries=[['1' if t==s==1 else (rf'\alpha_{{{t},{s}}}' if s<=t else '0')
          for s in range(1,11)] for t in range(1,11)]
grid(ax,1.15,3.6,13.15,5.0,entries,name=r'A_i=\mathrm{softmax}_{row}(S_i)',rowdim='10',coldim='10',
     colors=lambda i,j:PALE if j>i else GREEN,fontsize=13)
step(ax,9.02,'1','Multiply the weights by V, keeping one output row per query')
weight(ax,.8,10.35,2.5,1.95,'A_i','10','10',color=TEAL)
eq(ax,4.45,11.3,r'\times',25)
rowmat(ax,5.15,10.35,3.5,1.95,'v','V_i',cols='128',color=ORANGE)
eq(ax,9.8,11.3,'=',25)
rowmat(ax,10.4,10.35,3.7,1.95,'z','Z_i',cols='128')
step(ax,12.95,'2','Read the first, second, and last output rows')
eq(ax,.85,13.55,r'z_1=1v_1+0v_2+\cdots+0v_{10}=v_1',21)
eq(ax,.85,14.25,r'z_2=\alpha_{21}v_1+\alpha_{22}v_2',21)
eq(ax,.85,15.0,r'z_{10}=\alpha_{10,1}v_1+\alpha_{10,2}v_2+\cdots+\alpha_{10,10}v_{10}',21)
eq(ax,.85,15.78,r'z_t=\sum_{s=1}^{t}\alpha_{ts}v_s,\qquad \sum_{s=1}^{t}\alpha_{ts}=1',21)
txt(ax,.85,16.5,'The score selects how much to read; the value vector supplies the content.',13,TEAL)
save(fig,'detail-03-weights-and-values')

# 4. Packed heads, concatenation, output map and value bottleneck.
fig,ax=page(4,'Keep heads separate, then project their outputs',
            'H = 96 heads; each head has width 128. The concatenated width is 96 x 128 = 12,288.',17.4)
step(ax,1.7,'1','Pack the learned query maps into one wide matrix')
rowmat(ax,.8,3.05,3.1,1.7,'e','E',cols='12,288')
eq(ax,4.95,3.9,r'\times',25)
grid(ax,5.65,3.05,5.6,1.7,[[r'W_1^Q',r'W_2^Q',r'\cdots',r'W_{96}^Q']],name='W^Q',rowdim='12,288',coldim='96 blocks, each 128 columns',fontsize=19)
eq(ax,12.7,3.9,'=',24)
eq(ax,13.45,3.9,'Q_{flat}',19)
eq(ax,.85,5.3,r'Q_{flat}=[Q_1\ Q_2\ \cdots\ Q_{96}]\in\mathbb{R}^{10\times12288}',21)
eq(ax,.85,5.95,r'(10,12288)\ \longrightarrow\ (10,96,128)\ \longrightarrow\ (96,10,128)',20)
txt(ax,.85,6.48,'Repeat for K and V. Each head computes its own 10 x 10 weights A_i.',13)
step(ax,7.05,'2','Keep this valid block identity distinct from multi-head attention')
eq(ax,.85,7.68,r'Q_{flat}K_{flat}^{\mathsf T}=\sum_{i=1}^{96}Q_iK_i^{\mathsf T}',23)
txt(ax,.85,8.25,'This pools scores. MHA instead applies softmax separately to every head before mixing values.',13,ORANGE)
step(ax,8.68,'3','Concatenate head outputs, then multiply by stacked output blocks')
grid(ax,.85,10.15,6.0,1.6,[[r'Z_1',r'Z_2',r'\cdots',r'Z_{96}']],name=r'Z_{cat}',rowdim='10',coldim='12,288',fontsize=20)
eq(ax,8.0,10.95,r'\times',25)
grid(ax,8.75,9.8,3.4,2.4,[[r'W_1^O'],[r'W_2^O'],[r'\vdots'],[r'W_{96}^O']],name=r'W^O',rowdim='12,288',coldim='12,288',fontsize=17)
eq(ax,13.6,10.95,'=O',22)
eq(ax,.85,12.75,r'O=\sum_{i=1}^{96}Z_iW_i^O=\sum_{i=1}^{96}A_iE\,W_i^VW_i^O',24)
step(ax,13.65,'4','For each head, expose the value bottleneck and its regrouping')
eq(ax,.85,14.28,r'E_{10\times12288}\ (W_i^V)_{12288\times128}\ (W_i^O)_{128\times12288}',20)
eq(ax,.85,15.0,r'O_i=A_i\left((EW_i^V)W_i^O\right)=(A_iE)(W_i^VW_i^O)',22)
eq(ax,.85,15.75,r'W_i^VW_i^O:\ 12288\times12288,\quad \mathrm{rank}\leq128',20)
txt(ax,.85,16.42,'Sum the head contributions to get O (10 x 12,288); the surrounding residual block can add E + O.',12)
save(fig,'detail-04-heads-and-output')

# 5. The left-hand, column-token convention from the handwritten page.
fig,ax=page(5,'The same calculation with tokens in columns',
            'This is the left-hand drawing in the notebook. Every row-convention object is transposed consistently.',14)
step(ax,1.7,'1','Transpose the input and the learned feature maps')
colmat(ax,.85,3.0,2.5,3.1,r'e_{k}^{\mathsf T}',r'X=E^{\mathsf T}',rows='12,288',cols='10')
eq(ax,5,3.0,r'Q_c=(W_i^Q)^{\mathsf T}X=Q_i^{\mathsf T}\quad(128\times10)',21)
eq(ax,5,4.0,r'K_c=(W_i^K)^{\mathsf T}X=K_i^{\mathsf T}\quad(128\times10)',21)
eq(ax,5,5.0,r'V_c=(W_i^V)^{\mathsf T}X=V_i^{\mathsf T}\quad(128\times10)',21)
step(ax,6.75,'2','Queries now index columns, so normalize down each column')
eq(ax,.85,7.4,r'K_c^{\mathsf T}Q_c=(Q_iK_i^{\mathsf T})^{\mathsf T}\quad(10\times10)',22)
eq(ax,.85,8.15,r'S_c=K_c^{\mathsf T}Q_c/\sqrt{128}+M^{\mathsf T}=S_i^{\mathsf T}',21)
txt(ax,.85,8.78,'Here M is the additive mask used in S_i = Q_i K_i^T / sqrt(128) + M.',12)
eq(ax,.85,9.4,r'A_c=\mathrm{softmax}_{col}(S_c)=A_i^{\mathsf T}',23)
step(ax,10.15,'3','The values multiply the attention weights from the left')
eq(ax,.85,10.83,r'Z_c=V_cA_c=(A_iV_i)^{\mathsf T}\quad(128\times10)',23)
eq(ax,.85,11.62,r'O_i^{\mathsf T}=(W_i^O)^{\mathsf T}(W_i^V)^{\mathsf T}X A_c',22)
eq(ax,.85,12.4,r'(12288\times128)(128\times12288)(12288\times10)(10\times10)',18)
txt(ax,.85,13.17,'Rows of A_c are keys, columns are queries. The causal allowed region is upper triangular in this convention.',12,TEAL)
save(fig,'detail-05-column-convention')

# 6. Shared compressed token rows with separate expansion branches.
fig,ax=page(6,'MLA starts with shared latent token rows',
            'Content-only derivation from the notebook: D = 12,288, r = 512, d_h = 128. No RoPE or bias here.',16.3)
rowmat(ax,.8,2.85,3.4,1.9,'e','E',cols='12,288')
eq(ax,5.25,3.8,r'\times',26)
weight(ax,5.95,2.85,1.65,1.9,r'W^{DKV}','12,288','512')
eq(ax,8.85,3.8,'=',26)
rowmat(ax,9.55,2.85,4.3,1.9,'c','C',cols='512',color=TEAL)
txt(ax,.85,5.35,'Cache one c_t for each token. Every head reads the same C, with its own learned maps.',13,TEAL)
for y,letter in [(7.2,'K'),(10.65,'V')]:
    rowmat(ax,.8,y,3.4,1.8,'c','C',cols='512',color=TEAL)
    eq(ax,5.25,y+.9,r'\times',26)
    weight(ax,5.95,y,1.65,1.8,'U_{'+letter+',i}','512','128')
    eq(ax,8.85,y+.9,'=',26)
    rowmat(ax,9.55,y,4.3,1.8,letter.lower(),letter+'_i',cols='128',color=BLUE if letter=='K' else ORANGE)
eq(ax,.85,13.25,r'Q_i=EW_i^Q\quad(10\times128)',22)
txt(ax,7.9,13.25,'The query branch stays separate in this simplified derivation.',12)
eq(ax,.85,14.1,r'[K_1\ \cdots\ K_H\ V_1\ \cdots\ V_H]=C[U_{K,1}\ \cdots\ U_{K,H}\ U_{V,1}\ \cdots\ U_{V,H}]',17)
txt(ax,.85,14.86,'Each 512 -> 128 map is one head block. Together they expand C into all heads, hence “up-projection”.',12)
txt(ax,.85,15.57,'Low-rank parameterization is a modeling choice; the following regroupings are exact for these chosen factors.',12,ORANGE)
save(fig,'detail-06-mla-projections')

# 7. Every key-absorption grouping, followed by the one-query comparison.
fig,ax=page(7,'MLA absorbs the key map into the query',
            'Follow the transpose, change only the parentheses, and preserve the score scale sqrt(128).',17.1)
step(ax,1.7,'1','Start with expanded keys')
eq(ax,.85,2.35,r'K_i=CU_{K,i}\qquad\Longrightarrow\qquad K_i^{\mathsf T}=U_{K,i}^{\mathsf T}C^{\mathsf T}',23)
eq(ax,.85,3.12,r'Q_iK_i^{\mathsf T}=Q_i(CU_{K,i})^{\mathsf T}=Q_iU_{K,i}^{\mathsf T}C^{\mathsf T}',24)
rowmat(ax,.8,4.65,3.1,1.9,'q','Q_i',cols='128')
eq(ax,4.95,5.6,r'\times',25)
weight(ax,5.65,4.65,2.0,1.9,r'U_{K,i}^{\mathsf T}','128','512')
eq(ax,8.9,5.6,r'\times',25)
colmat(ax,9.6,4.65,3.5,1.9,r'c_{k}^{\mathsf T}',r'C^{\mathsf T}',rows='512',cols='10',size=16)
brace(ax,.85,7.05,6.8,'absorb this product into the query',side=-1,color=BLUE)
step(ax,8.1,'2','Precompose the learned maps, or transform the current query directly')
eq(ax,.85,8.78,r'B_i=W_i^QU_{K,i}^{\mathsf T}\quad(12288\times128)(128\times512)=(12288\times512)',19)
eq(ax,.85,9.5,r'\widehat Q_i=EB_i=Q_iU_{K,i}^{\mathsf T}\quad(10\times512)',24)
eq(ax,.85,10.25,r'Q_iK_i^{\mathsf T}=\widehat Q_i C^{\mathsf T}\quad(10\times512)(512\times10)=(10\times10)',19)
eq(ax,.85,11.0,r'A_i=\mathrm{softmax}_{row}\!\left(\widehat Q_iC^{\mathsf T}/\sqrt{128}+M\right)',23)
step(ax,11.8,'3','For one current query, avoid expanding every cached token')
eq(ax,.85,12.48,r'q_{t,i}(CU_{K,i})^{\mathsf T}=(q_{t,i}U_{K,i}^{\mathsf T})C^{\mathsf T}',23)
eq(ax,.85,13.25,r'(1\times128)\ [(n\times512)(512\times128)]^{\mathsf T}',20)
eq(ax,.85,14.0,r'=[(1\times128)(128\times512)](512\times n)=(1\times n)',20)
txt(ax,.85,14.78,'Expanded route: create n x 128 keys for this head. Absorbed route: transform one query, then read C.',12)
txt(ax,.85,15.46,'A cached-MHA score has width 128; the absorbed latent score has width 512. Less cache is not automatically less arithmetic.',12,ORANGE)
txt(ax,.85,16.23,'The regrouping leaves scores unchanged. Dividing by sqrt(512) instead would change the attention weights.',12,TEAL)
save(fig,'detail-07-mla-key-absorption')

# 8. Values, output map, token-level sums, and why it is still a KV cache.
fig,ax=page(8,'MLA averages latent rows before the value map',
            'The same head-specific attention weights are used on both sides of every equality.',18)
step(ax,1.7,'1','Expose all three factors after the attention matrix')
eq(ax,.85,2.35,r'O_i=A_iV_iW_i^O=A_i(CU_{V,i})W_i^O=(A_iC)(U_{V,i}W_i^O)',23)
weight(ax,.8,3.8,2,1.6,'A_i','10','10',color=BLUE)
eq(ax,3.95,4.6,r'\times',25)
rowmat(ax,4.65,3.8,2.45,1.6,'c','C',cols='512',color=TEAL)
eq(ax,8.2,4.6,r'\times',25)
weight(ax,8.85,3.8,1.6,1.6,r'U_{V,i}','512','128',color=ORANGE)
eq(ax,11.55,4.6,r'\times',25)
weight(ax,12.2,3.8,2,1.6,r'W_i^O','128','12,288')
brace(ax,.85,5.9,6.2,r'$H_i=A_iC:\ 10\times512$',side=-1,color=TEAL)
brace(ax,8.9,5.9,5.2,r'$T_i=U_{V,i}W_i^O:\ 512\times12288$',side=-1,color=ORANGE)
step(ax,6.95,'2','Read the latent average as actual token rows')
rowmat(ax,.85,8.2,6.25,2.35,r'h_{k}',r'H_i=A_iC',cols='512',color=TEAL)
eq(ax,8.2,8.25,r'h_1=c_1',21)
eq(ax,8.2,9.0,r'h_2=\alpha_{21}c_1+\alpha_{22}c_2',19)
eq(ax,8.2,9.8,r'h_{10}=\sum_{s=1}^{10}\alpha_{10,s}c_s',20)
eq(ax,.85,11.1,r'O_i=H_iT_i\quad(10\times512)(512\times12288)=(10\times12288)',20)
step(ax,11.85,'3','Expand one output sum to see exactly what moved')
eq(ax,.85,12.55,r'v_s=c_sU_{V,i}',22)
eq(ax,.85,13.3,r'z_{t,i}=\alpha_{t1}(c_1U_{V,i})+\cdots+\alpha_{tt}(c_tU_{V,i})',23)
eq(ax,.85,14.05,r'=(\alpha_{t1}c_1+\cdots+\alpha_{tt}c_t)U_{V,i}=h_tU_{V,i}',23)
eq(ax,.85,14.8,r'o_{t,i}=z_{t,i}W_i^O=h_tT_i,\qquad O=\sum_{i=1}^{H}O_i',23)
rule(ax,15.38)
txt(ax,.85,15.88,'Why is it still a KV cache?',17,BLUE,weight='bold')
eq(ax,.85,16.48,r'\widehat Q_iC^{\mathsf T}=Q_iK_i^{\mathsf T}\quad\mathrm{(key\ role)}',19)
eq(ax,8.2,16.48,r'(A_iC)T_i=A_iV_iW_i^O\quad\mathrm{(value\ role)}',18)
txt(ax,.85,17.15,'C stores token representations; transformed queries score them; T_i maps their weighted average to the output.',12)
save(fig,'detail-08-mla-value-absorption')

# 9. Full-dimensional proposal and cache accounting from the notebook.
fig,ax=page(9,'The identity proposal and the cache comparison',
            'Bias-free, position-free attention: separate exact regrouping from the choice to compress.',18)
step(ax,1.7,'1','The notebook proposal: make the down-projection the identity')
eq(ax,.85,2.38,r'W^{DKV}=I_{12288},\qquad C=E,\qquad U_{K,i}=W_i^K,\quad U_{V,i}=W_i^V',22)
eq(ax,.85,3.13,r'Q_iK_i^{\mathsf T}=(Q_i(W_i^K)^{\mathsf T})E^{\mathsf T}',24)
eq(ax,.85,3.88,r'O_i=(A_iE)(W_i^VW_i^O)',24)
rowmat(ax,.85,5.35,4.25,1.9,'e',r'C=E',cols='12,288',color=TEAL)
arrow(ax,6.3,6.3,8.4,6.3)
rowmat(ax,9.1,5.35,4.25,1.9,'c',r'C=EW^{DKV}',cols='512',color=TEAL)
txt(ax,.85,7.83,'Both arrangements are valid. The learned latent bottleneck changes the cache width from D to r.',13)
step(ax,8.55,'2','Compare representations stored for one historical token in one layer')
table=[
 [r'\mathrm{method}',r'\mathrm{stored\ scalars}',r'\mathrm{score\ width}'],
 [r'\mathrm{MHA}',r'2Hd_h',r'd_h=128'],
 [r'\mathrm{GQA}',r'2Gd_h',r'd_h=128'],
 [r'\mathrm{MQA}',r'2d_h',r'd_h=128'],
 [r'\mathrm{identity\ cache}',r'D=12288',r'D=12288'],
 [r'\mathrm{MLA\ content}',r'r=512',r'r=512'],
]
grid(ax,.85,9.35,13.4,3.65,table,fontsize=17)
txt(ax,.85,13.48,'MHA stores separate KV for every head; GQA shares within G groups; MQA shares one KV pair.',12)
step(ax,14.14,'3','Put layers, tokens, and bytes back into the storage calculation')
eq(ax,.85,14.78,r'\mathrm{MHA\ bytes}=nL\,b(2Hd_h)',22)
txt(ax,8.55,14.78,'Example: H=128, d_h=128, L=61, b=2 bytes.',12)
eq(ax,.85,15.48,r'2(128)(128)(61)(2)=3,997,696\ \mathrm{bytes/token}',21)
txt(ax,.85,16.12,'At 100,000 tokens: 399.77 GB total. One more token adds about 4 MB, not 400 GB.',13,ORANGE)
txt(ax,.85,16.83,'Full DeepSeek MLA also caches a shared positional key: r + d_R scalars (512 + 64 in the cited example).',12,TEAL)
save(fig,'detail-09-identity-and-cache')

# 7b. Repeat exactly the row/column and staircase format in latent coordinates.
fig,ax=page('07b','The same score staircase in latent coordinates',
            'Fix one head. The absorbed query has 512 coordinates; each cached token is a row of C.',16.9)
eq(ax,.8,1.85,r'\widehat Q_i=E B_i=Q_iU_{K,i}^{\mathsf T},\qquad \widehat q_t=q_tU_{K,i}^{\mathsf T}',23)
rowmat(ax,.8,3.4,4.6,2.1,r'\widehat q_{k}',r'\widehat Q_i',cols='512')
eq(ax,6.55,4.45,r'\times',28)
colmat(ax,7.35,3.0,2.45,3.2,r'c_{k}^{\mathsf T}',r'C^{\mathsf T}',rows='512',cols='10',size=14)
eq(ax,11.15,3.8,r'\widehat q_t c_s^{\mathsf T}',23)
eq(ax,11.15,4.55,r'=q_tk_s^{\mathsf T}',22)
eq(ax,11.15,5.25,r'(10\times512)(512\times10)',14)
eq(ax,.8,6.75,r'S_i=(\widehat Q_iC^{\mathsf T}+M)/\sqrt{128}',23)
entries=[[rf'\widehat q_{{{t}}}c_{{{s}}}^{{\mathsf T}}' if s<=t else r'-\infty'
          for s in range(1,11)] for t in range(1,11)]
grid(ax,1.15,8.0,13.15,5.4,entries,rowdim='10',coldim='10',
     colors=lambda i,j:GOLD if j>i else GREEN,fontsize=12)
txt(ax,1.15,13.85,'Divide this displayed masked score matrix by sqrt(128), then apply softmax to each row.',12)
eq(ax,.85,14.55,r'A_{i,1:}=[1,0,\ldots,0]',23)
eq(ax,.85,15.35,r'\alpha_{10,s}=\frac{\exp(\widehat q_{10}c_s^{\mathsf T}/\sqrt{128})}{\sum_{u=1}^{10}\exp(\widehat q_{10}c_u^{\mathsf T}/\sqrt{128})}',23)
txt(ax,.85,16.17,'Causal structure and weights are unchanged. Only the coordinates used to compute each content score have changed.',12,TEAL)
save(fig,'detail-07b-mla-score-staircase')

# 9b. Stacked layer caches and all byte estimates from the handwritten comparison.
fig,ax=page('09b','Cache rows, shared heads, and layer stacks',
            'Cache comparison example: n historical tokens, H = 128, d_h = 128, L = 61 layers, b = 2 bytes/scalar.',17.7)
step(ax,1.7,'1','Ordinary MHA stores both keys and values for every head')
for x,name in [(1.1,'K_{cache}'),(8.4,'V_{cache}')]:
    for delta in [.27,.18,.09]:
        ax.add_patch(Rectangle((x+delta,3.2-delta),4.5,2.2,fill=False,lw=.8,edgecolor=RULE))
    grid(ax,x,3.2,4.5,2.2,[[r'K_1' if name[0]=='K' else r'V_1',
                            r'K_2' if name[0]=='K' else r'V_2',r'\cdots',
                            r'K_H' if name[0]=='K' else r'V_H']],
         name=name,rowdim='n',coldim='H x 128 = 16,384',fontsize=18)
txt(ax,1.1,5.95,'The offset rectangles represent L separate layer caches.',13)
eq(ax,1.1,6.6,r'\mathrm{total\ bytes}=2nHd_hLb',24)
step(ax,7.35,'2','Sharing and compression change the stored width, not the number of history rows')
table=[
 [r'\mathrm{method}',r'\mathrm{KV\ width/layer}',r'\mathrm{bytes/token,\ all\ 61\ layers}'],
 [r'\mathrm{MHA}',r'2(128)(128)=32768',r'3,997,696\ \approx4.00\ MB'],
 [r'\mathrm{GQA,\ G=16}',r'2(16)(128)=4096',r'499,712\ \approx500\ KB'],
 [r'\mathrm{MQA}',r'2(128)=256',r'31,232\ \approx31.2\ KB'],
 [r'\mathrm{MLA,\ content}',r'512',r'62,464\ \approx62.5\ KB'],
 [r'\mathrm{MLA,\ with\ position}',r'512+64=576',r'70,272\ \approx70.3\ KB'],
]
grid(ax,.85,8.15,13.7,3.75,table,fontsize=16)
step(ax,12.65,'3','For MLA, cache one shared latent row plus the positional row')
rowmat(ax,1.1,14.0,5.0,2.0,'c','C',rows='n',cols='512',inds=(1,2,None,'n'),color=TEAL)
txt(ax,7.15,15.0,'and',14,GREY,ha='center')
rowmat(ax,8.05,14.0,5.0,2.0,r'k^R_{k}',r'K^R',rows='n',cols='64',inds=(1,2,None,'n'),color=ORANGE)
txt(ax,.85,16.62,'Multiply each per-token figure by n for the history total. Decimal KB/MB; weights and temporary workspace are excluded.',12)
txt(ax,.85,17.03,'Causal decoding reuses historical keys and values; only the current query is needed, so past queries are not cached.',12,TEAL)
save(fig,'detail-09b-cache-layout')

# 10. The three matrix product constructions, all using the same row/column style.
fig,ax=page(10,'Three ways to build the same matrix product',
            'A is m x r, B is r x n, P = AB is m x n. No inverse or square-matrix assumption is needed.',18.1)
step(ax,1.7,'1','Row times column: one scalar at a time')
rowmat(ax,.85,3.05,4.0,1.8,'a','A',rows='m',cols='r',inds=(1,2,None,'m'))
eq(ax,6,3.95,r'\times',25)
colmat(ax,6.75,2.8,2.5,2.55,'b','B',rows='r',cols='n',inds=(1,2,None,'n'),size=17)
eq(ax,10.5,3.45,r'P_{ij}=a_i b_j',24)
eq(ax,10.5,4.3,r'=\sum_{k=1}^{r}A_{ik}B_{kj}',20)
rule(ax,5.85)
step(ax,6.35,'2','Matrix times each column: one output vector at a time')
eq(ax,.85,7.0,r'B=[b_1\ b_2\ \cdots\ b_n]\quad\Longrightarrow\quad AB=[Ab_1\ Ab_2\ \cdots\ Ab_n]',23)
colmat(ax,.85,8.45,5.4,2.15,r'Ab_{k}',r'AB',rows='m',cols='n',inds=(1,2,None,'n'),size=19)
eq(ax,7.5,8.75,r'Ab_j=\sum_{k=1}^{r}B_{kj}A_{:k}',23)
txt(ax,7.5,9.55,'The entries of b_j weight the columns of A.',13)
eq(ax,.85,11.22,r'\mathrm{row\ analogue:}\quad (AB)_{i:}=\sum_{k=1}^{r}A_{ik}B_{k:}',23)
rule(ax,11.82)
step(ax,12.33,'3','Column times row: one outer-product matrix at a time')
colmat(ax,.85,13.65,1.4,2.0,r'A_{:k}','',rows='m',cols='1',inds=(1,),size=17)
eq(ax,3.4,14.65,r'\times',25)
rowmat(ax,4.15,14.1,3.3,1.0,r'B_{k:}','',rows='1',cols='n',inds=(1,),size=18)
eq(ax,8.65,14.65,'=',25)
weight(ax,9.35,13.65,3.6,2.0,r'A_{:k}B_{k:}','m','n',color=TEAL)
eq(ax,.85,16.3,r'AB=\sum_{k=1}^{r}A_{:k}B_{k:},\qquad \mathrm{rank}(A_{:k}B_{k:})\leq1',24)
txt(ax,.85,17.1,'At entry (i,j), all three pictures give the same sum of A_ik B_kj. Attention and MLA regroup these same products.',12)
save(fig,'detail-10-matrix-products')

# Verify the actual 10-token mask and weighted-sum examples shown above.
rng=np.random.default_rng(20261109)
Q=rng.normal(size=(10,128)); K=rng.normal(size=(10,128)); V=rng.normal(size=(10,128))
raw=Q@K.T; future=np.triu(np.ones((10,10),dtype=bool),1)
masked=raw.copy(); masked[future]=-np.inf
S=masked/np.sqrt(128); ex=np.exp(S-S.max(axis=1,keepdims=True)); A=ex/ex.sum(axis=1,keepdims=True)
assert np.isneginf(S[future]).all() and np.isfinite(S[~future]).all()
assert np.count_nonzero(A[future])==0 and A[0,0]==1.
assert np.allclose(A.sum(axis=1),1.)
assert np.allclose((A@V)[0],V[0])
assert np.allclose((A@V)[-1],sum(A[-1,s]*V[s] for s in range(10)))
assert np.allclose(Q@K.T,sum(np.outer(Q[:,k],K[:,k]) for k in range(128)))
REPORT['checks']={'masked_future_entries':int(future.sum()),'allowed_score_entries':int((~future).sum()),
                  'first_weight_row':[float(x) for x in A[0]],
                  'max_row_sum_error':float(np.max(np.abs(A.sum(axis=1)-1))),
                  'last_value_row_error':float(np.max(np.abs((A@V)[-1]-sum(A[-1,s]*V[s] for s in range(10))))),
                  'source':'raw/notes/2026-11-09-attention.pdf'}
(OUT/'detail-checks.json').write_bytes((json.dumps(REPORT,indent=2)+'\n').encode())
print(json.dumps({'figures':len(REPORT)-1,'checks':REPORT['checks']},indent=2))
