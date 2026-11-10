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
    return ax.text(x,y,s.replace(r'\mathsf T',r'\mathsf{T}'),fontsize=size,color=color,ha=ha,va='center',**kw)

def eq(ax,x,y,s,size=21,color=INK,ha='left'):
    return txt(ax,x,y,'$'+s.replace(r'\mathsf T',r'\mathsf{T}')+'$',size,color,ha)

def page(number,title,subtitle,h,w=16):
    fig,ax=plt.subplots(figsize=(w,h),dpi=140)
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    ax.set(xlim=(0,w),ylim=(h,0)); ax.axis('off')
    fig.patch.set_facecolor('white')
    code=f'{number:02d}' if isinstance(number,int) else str(number)
    txt(ax,.55,.48,f'{code}  {title}',23,BLUE,weight='bold')
    txt(ax,.55,1.03,subtitle,12)
    txt(ax,.55,h-.34,'Original Codex illustration. Braces give dimensions; matrix proportions are schematic.',10,GREY)
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
    if '{k,' in sym: return sym.replace('{k,','{'+str(k)+',')
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
