"""Greyscale figures from checked summaries, with direct labels and patterns."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import ROOT

def main():
    sources=[]
    for system,title in [('l96','Lorenz-96'),('kolmo','Kolmogorov')]:
        path=ROOT/f'results/{system}_solver_statistics.json'
        if path.exists():sources.append((system,title,json.loads(path.read_text())))
        else:
            status=ROOT/f'results/{system}_execution_status.json'
            if status.exists() and json.loads(status.read_text()).get('status','').startswith('STOP_'):
                sources.append((system,title,None))
    if not sources:raise RuntimeError('no measured sources')
    out=ROOT/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':220})
    def save(fig,name):
        fig.tight_layout();fig.savefig(out/(name+'.pdf'));fig.savefig(out/(name+'.png'));plt.close(fig)
    def stopped(ax,system,title):
        c=json.loads((ROOT/f'results/{system}_calibration.json').read_text())
        counts='\n'.join(f"δ={r['delta']:g}: {r['eligible']}/{r['total']} determinable" for r in c['rows'])
        ax.set_title(title+' — calibration stopped')
        ax.text(.5,.5,counts+'\n\nRequired: ≥16/20\nTest and learned arms not run',transform=ax.transAxes,
                ha='center',va='center',fontsize=11)
        ax.set_xticks([]);ax.set_yticks([])
        for spine in ax.spines.values():spine.set_visible(False)
    fig,axes=plt.subplots(1,len(sources),figsize=(7.2*len(sources),4),squeeze=False)
    for ax,(system,title,data) in zip(axes[0],sources):
        if data is None:stopped(ax,system,title);continue
        rows=data['horizons'];T=[r['T'] for r in rows];end_labels=[]
        specs=[('paired','Niva decision','-','o','0'),('unpaired','Unpaired decision','--','s','.35'),
               ('learned','Learned decision',':','^','.15')]
        for arm,label,style,marker,color in specs:
            if arm in rows[0]['arms']:
                y=[r['arms'][arm]['accuracy'][3] for r in rows]
                ax.plot(T,y,linestyle=style,marker=marker,markersize=3,color=color,label=label)
                if y[-1] is not None:end_labels.append((y[-1],label,color))
        ax.plot(T,[r['arms']['paired']['ACC'] for r in rows],color='0',linestyle=(0,(6,2,1,2)),marker='x',markersize=4,label='Niva forecast ACC')
        ax.plot(T,[r['myopic_accuracy'] for r in rows],color='.5',linestyle=(0,(3,1,1,1)),marker='d',markersize=3,label='Myopic decision')
        if rows[-1]['arms']['paired']['ACC'] is not None:end_labels.append((rows[-1]['arms']['paired']['ACC'],'Niva forecast ACC','0'))
        if rows[-1]['myopic_accuracy'] is not None:end_labels.append((rows[-1]['myopic_accuracy'],'Myopic decision','.5'))
        previous=-.06
        for value,label,color in sorted(end_labels):
            location=max(value,previous+.075);previous=location
            ax.annotate(label,xy=(T[-1],value),xytext=(21.2,location),fontsize=8,color=color,va='center',
                        arrowprops=dict(arrowstyle='-',color=color,linewidth=.6))
        chance=rows[0]['random_accuracy_expected'];ax.axhline(chance,color='.65',linestyle=':',linewidth=.8)
        ax.text(20.5,chance,'Random',va='center',fontsize=8,color='.4')
        ax.axhline(.8,color='.7',linewidth=.6);ax.text(.5,.78,'0.8 decision',fontsize=8,va='top')
        ax.axhline(.2,color='.7',linewidth=.6);ax.text(.5,.18,'0.2 ACC',fontsize=8,va='top')
        if data['Tf'] is not None:ax.axvline(data['Tf'],color='.4',linestyle=':',linewidth=.8);ax.text(data['Tf'],1.02,'T_f',ha='center')
        ax.set(title=title+(' (learned arm pending)' if data.get('learned_arm_pending',True) else ''),xlabel='Lead time (unperturbed LT)',ylabel='Top-1 accuracy / forecast ACC',ylim=(-.12,max(1.1,previous+.08)),xlim=(0,29))
    save(fig,'decision_and_forecast')
    fig,axes=plt.subplots(1,len(sources),figsize=(6*len(sources),3.8),squeeze=False)
    for ax,(system,title,data) in zip(axes[0],sources):
        if data is None:stopped(ax,system,title);continue
        rows=data['horizons'];T=np.array([r['T'] for r in rows])
        for arm,color,marker,style,label in [('paired','0','o','-','Paired'),('unpaired','.4','s','--','Unpaired')]:
            value=np.array([r['arms'][arm]['M95'] if r['arms'][arm]['M95'] is not None else 320 for r in rows])
            ax.plot(T,value,color=color,marker=marker,linestyle=style,markersize=4,label=label)
            cens=np.array([r['arms'][arm]['M95'] is None for r in rows])
            ax.scatter(T[cens],value[cens],marker='^',color=color,s=30)
            ax.annotate(label,(T[-1],value[-1]),xytext=(7,7 if arm=='paired' else -12),textcoords='offset points',fontsize=8,color=color)
        ax.set_yscale('log',base=2);ax.set_yticks([8,16,32,64,128,256,320],labels=['8','16','32','64','128','256','>256'])
        ax.set(title=title,xlabel='Lead time (LT)',ylabel='Smallest tested budget with top-1 ≥0.95',xlim=(0,24))
        ax.legend(frameon=False);ax.text(.24,.03,'Triangles: censored; no 320-member test',transform=ax.transAxes,fontsize=8)
    save(fig,'members_paired_unpaired')
    complete=[s for s in sources if s[2] is not None and not s[2].get('learned_arm_pending',True)]
    if complete:
        fig,axes=plt.subplots(len(complete),2,figsize=(10,3.8*len(complete)),squeeze=False)
        for row,(_,title,data) in enumerate(complete):
            for arm,marker,color,label in [('learned','^','0','Learned'),('misidentified','s','.4','Misidentified'),('jitter','o','.7','Jitter')]:
                if arm not in data['horizons'][0]['arms']:continue
                for col,key,xlabel in [(0,'response_correlation','Cost-response correlation'),(1,'ACC','Forecast ACC')]:
                    ax=axes[row,col];x=[];y=[]
                    for h in data['horizons']:
                        a=h['arms'][arm]
                        if a[key] is None or a['accuracy'][3] is None:continue
                        x.append(a[key]);y.append(a['accuracy'][3])
                        if arm=='learned' and h['T'] in (2,4,8,10,20):ax.annotate(f"{h['T']:g}",(a[key],a['accuracy'][3]),fontsize=7,xytext=(4,4),textcoords='offset points')
                    ax.scatter(x,y,marker=marker,c=color,label=label,s=27)
                    ax.set(title=title,xlabel=xlabel,ylabel='Top-1 accuracy (M64)',ylim=(-.03,1.05));ax.legend(frameon=False,fontsize=8)
        save(fig,'learned_response_and_forecast')
    metadata=dict(sources=[dict(system=s[0],git_sha=s[2]['git_sha'] if s[2] else None,
                  diagnostics_source_sha=s[2].get('diagnostics_source_sha') if s[2] else None,
                  calibration_source_sha=json.loads((ROOT/f'results/{s[0]}_calibration.json').read_text())['git_sha'],
                  learned_pending=s[2].get('learned_arm_pending',True) if s[2] else False,
                  stopped=s[2] is None) for s in sources],
                  labels='Censored M95 plotted at a display-only320; no inferred member count. Learned point labels show selected LT: 2,4,8,10,20.')
    (out/'sources.json').write_text(json.dumps(metadata,indent=2)+'\n')

if __name__=='__main__':main()
