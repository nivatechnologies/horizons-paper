"""Publication greyscale plots from checked metrics; no data access on import."""
from pathlib import Path
import numpy as np


def render(metrics_by_lead,outdir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
    names=list(dict.fromkeys(name for r in metrics_by_lead for name in r['metrics']));markers=['o','s','^','D','v','P','X','*'];styles=['-','--',':','-.']
    outputs=[]
    for field,label in [('P','Best-action accuracy'),('wACC','Window ACC'),('wRMSE','Window normalized RMSE'),('MSRE','Mean-state response error'),('VRE','Variance response error')]:
        fig,ax=plt.subplots(figsize=(7,4))
        for i,name in enumerate(names):
            x=[];y=[]
            for r in metrics_by_lead:
                val=r['metrics'].get(name,{}).get('eligible',{}).get(field)
                if val is not None and np.isfinite(val):x.append(r['T']);y.append(val)
            if not x:continue
            ax.plot(x,y,color=str(.15+.55*(i%3)/2),marker=markers[i%len(markers)],linestyle=styles[i%len(styles)],label=name)
            ax.annotate(name,(x[-1],y[-1]),xytext=(5,(i%3-1)*7),textcoords='offset points',fontsize=8)
        ax.set_xlabel('Lead (LT)');ax.set_ylabel(label);ax.margins(x=.22);fig.tight_layout()
        for ext in ['pdf','png']:
            target=outdir/(field+'.'+ext);fig.savefig(target,bbox_inches='tight');outputs.append(str(target))
        plt.close(fig)
    return outputs


def render_required(metrics_by_lead,outdir,selected=None,two_scale=False):
    """WO §11 headline scatters and incumbent/physics lead comparisons."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    primary=next(r for r in metrics_by_lead if r['T']==2);markers=['o','s','^','D','v','P','X','*'];paths=[]
    fields=['wACC'] if two_scale else ['wACC','MSRE','VRE']
    labels={'wACC':'Decision-window ACC','MSRE':'Mean-state response error','VRE':'Variance response error'}
    def save(fig,name):
        fig.tight_layout()
        for ext in ['pdf','png']:
            p=outdir/(name+'.'+ext);fig.savefig(p,bbox_inches='tight',dpi=180);paths.append(str(p))
        plt.close(fig)
    for field in fields:
        fig,ax=plt.subplots(figsize=(7,4.5));point_labels=[]
        for i,(name,m) in enumerate(primary['metrics'].items()):
            x=m['eligible'].get(field);y=m['eligible'].get('P')
            if y is None:continue
            if x is None:
                if field=='wACC' and name.endswith('-cost'):
                    ax.axhline(y,color='.25',linestyle='--');ax.text(.02,y,name+' (no state forecast)',transform=ax.get_yaxis_transform(),va='bottom',fontsize=9)
                continue
            ax.scatter([x],[y],color=str(.15+.5*(i%3)/2),marker=markers[i%len(markers)],s=60)
            point_labels.append((y,x,name))
        ordered=sorted(point_labels);positions=[]
        for y,x,name in ordered:positions.append(max(y,positions[-1]+.04 if positions else y))
        if positions and positions[-1]>1.01:positions=[y-(positions[-1]-1.01) for y in positions]
        for (y,x,name),target in zip(ordered,positions):ax.annotate(name,(x,y),xytext=(1.04,target),textcoords=ax.get_yaxis_transform(),arrowprops={'arrowstyle':'-','color':'.5','linewidth':.6},fontsize=9,va='center')
        if field=='wACC':
            null_labels={}
            for i,(name,m) in enumerate(primary.get('null_metrics',{}).items()):
                y=m['eligible']['P']
                if y is None:continue
                ax.axhline(y,color='.65',linestyle=[':', '-.', '--'][i%3]);null_labels.setdefault(y,[]).append(name)
            for y,names in null_labels.items():ax.text(.02,y,' / '.join(names)+' null',transform=ax.get_yaxis_transform(),ha='left',va='bottom',fontsize=8)
        ax.set_xlabel(labels[field]);ax.set_ylabel('Eligible best-action accuracy');ax.set_ylim(0,1.04);ax.margins(x=.25)
        save(fig,('two_scale_' if two_scale else '')+'primary_P_vs_'+field)
    if not two_scale:
        names=list(dict.fromkeys(['N-last','CNN-20k']+([selected] if selected else [])))
        fig,axes=plt.subplots(1,2,figsize=(9,4))
        for i,name in enumerate(names):
            for ax,field in zip(axes,['P','wACC']):
                xy=[(r['T'],r['metrics'][name]['eligible'][field]) for r in metrics_by_lead if name in r['metrics'] and r['metrics'][name]['eligible'][field] is not None]
                if not xy:continue
                x,y=zip(*xy);ax.plot(x,y,color=str(.15+.25*i),marker=markers[i],linestyle=['-','--',':'][i]);ax.annotate(name,(x[-1],y[-1]),xytext=(4,7*(i-1)),textcoords='offset points',fontsize=8)
                ax.set_xlabel('Lead (LT)');ax.set_ylabel('Eligible best-action accuracy' if field=='P' else 'Decision-window ACC');ax.margins(x=.23)
        save(fig,'physics_base_selected_lead_curves')
    return paths
