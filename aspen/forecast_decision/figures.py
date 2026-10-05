"""Publication greyscale plots from checked metrics; no data access on import."""
from pathlib import Path
import numpy as np


def render(metrics_by_lead,outdir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
    names=list(metrics_by_lead[0]['metrics']);markers=['o','s','^','D','v','P','X','*'];styles=['-','--',':','-.']
    outputs=[]
    for field,label in [('P','Best-action accuracy'),('wACC','Window ACC'),('wRMSE','Window normalized RMSE'),('MSRE','Mean-state response error'),('VRE','Variance response error')]:
        fig,ax=plt.subplots(figsize=(7,4))
        for i,name in enumerate(names):
            x=[];y=[]
            for r in metrics_by_lead:
                val=r['metrics'][name]['eligible'].get(field)
                if val is not None and np.isfinite(val):x.append(r['T']);y.append(val)
            if not x:continue
            ax.plot(x,y,color=str(.15+.55*(i%3)/2),marker=markers[i%len(markers)],linestyle=styles[i%len(styles)],label=name)
            ax.annotate(name,(x[-1],y[-1]),xytext=(5,(i%3-1)*7),textcoords='offset points',fontsize=8)
        ax.set_xlabel('Lead (LT)');ax.set_ylabel(label);ax.margins(x=.22);fig.tight_layout()
        for ext in ['pdf','png']:
            target=outdir/(field+'.'+ext);fig.savefig(target,bbox_inches='tight');outputs.append(str(target))
        plt.close(fig)
    return outputs
