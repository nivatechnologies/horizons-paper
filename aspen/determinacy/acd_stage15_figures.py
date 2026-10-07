"""Stage 15B: presentation only from saved receipts."""
import os
os.environ['MPLBACKEND']='Agg'
import json,hashlib,re,subprocess
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
NAMES=['posterior','CNN-20k','CNN-F','CNN-noF']
STYLE={'posterior':('-','o'),'CNN-20k':('--','s'),'CNN-F':('-.','^'),'CNN-noF':((0,(8,3,1,3)),'D')}
def read(n):return json.loads((ROOT/'receipts'/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
def main():
 before={}
 for name in ['F13_main_paper','F17_decisions_paper','F18_matching_paper']:
  for ext in ['pdf','png']:
   key=f'figures/{name}.{ext}';old=subprocess.run(['git','show',f'HEAD:aspen/determinacy/{key}'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL);before[key]=hashlib.sha256(old.stdout).hexdigest() if old.returncode==0 else None
 plt.rcParams.update({'font.size':9,'axes.prop_cycle':plt.cycler(color=['black','0.35','0.60','0.15'])})
 sizes={}
 def save(fig,name):
  fig.tight_layout()
  for ext in ['pdf','png']:fig.savefig(ROOT/f'figures/{name}.{ext}',dpi=180)
  plt.close(fig)
  raw=(ROOT/f'figures/{name}.pdf').read_bytes();box=re.search(rb'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]',raw);a=list(map(float,box.groups()));sizes[name]=[a[2]-a[0],a[3]-a[1]]
 stage9=read('acd_stage9.json')['C'];ten=read('acd_stage10b.json')['models'];models={n:stage9[n] if n!='CNN-noF' else ten[n] for n in NAMES}
 fig,axes=plt.subplots(1,2,figsize=(10,4))
 for n,m in models.items():
  style,marker=STYLE[n];r=[r for r in m['reliability'] if r['questions']]
  axes[0].errorbar([v['mean_probability'] for v in r],[v['accuracy'] for v in r],yerr=np.array([[v['accuracy']-v['CP95'][0] for v in r],[v['CP95'][1]-v['accuracy'] for v in r]]),linestyle=style,marker=marker,label=n)
  r=[v for v in m['error_coverage'] if v['answers']];axes[1].plot([v['coverage'] for v in r],[v['pooled_error'] for v in r],linestyle=style,marker=marker,label=n)
 axes[0].plot([.5,1],[.5,1],linestyle=':',linewidth=.7,color='0.6');axes[0].set(xlabel='Mean modal probability',ylabel='Observed accuracy');axes[1].set(xlabel='Coverage',ylabel='Pooled error')
 for a in axes:a.legend(fontsize=8)
 save(fig,'F13_main_paper')
 decisions=read('acd_stage10b_decisions.json')['models'];fig,axes=plt.subplots(1,2,figsize=(10,4));x=np.arange(len(NAMES));width=.35
 for a,lead in zip(axes,[2,3]):
  for i,(policy,label,hatch) in enumerate([('E','E','/'),('C_delta_0','C (δ = 0)','x')]):
   rows=[next(r for r in decisions[n]['readings'] if r['lead']==lead and r['policy']==policy) for n in NAMES];bars=a.bar(x+(i-.5)*width,[r['mean_regret'] for r in rows],width,label=label,color='0.85' if i else '0.6',edgecolor='black',hatch=hatch)
   for b,r in zip(bars,rows):a.annotate(str(r['harms']),xy=(b.get_x()+b.get_width()/2,b.get_height()),xytext=(0,3),textcoords='offset points',ha='center',fontsize=8)
  a.set_xticks(x,NAMES,rotation=15);a.set(ylabel='Mean realized regret',title=f'{lead} LT');a.legend(fontsize=8)
 save(fig,'F17_decisions_paper')
 matching=read('acd_stage15_matching.json')['A'];fig,axes=plt.subplots(1,2,figsize=(10,4));x=np.arange(len(NAMES));width=.18
 for i,(lead,cov,hatch) in enumerate([(2,.5,'/'),(2,.7,'x'),(3,.5,'..'),(3,.7,'\\')]):
  values=[]
  for n in NAMES:
   r=next(r for r in matching[n]['rows'] if r['lead']==lead);values.append(next(m['pooled_error'] for m in r['matched_coverage'] if m['patterns']=='all_eight' and m['target_coverage']==cov))
  axes[0].bar(x+(i-1.5)*width,values,width,color=str(.5+i*.13),edgecolor='black',hatch=hatch,label=f'{lead} LT, coverage {cov}')
 for i,(lead,hatch) in enumerate([(2,'/'),(3,'x')]):
  values=[next(r['forecast']['accuracy']['answer_accuracy'] for r in matching[n]['rows'] if r['lead']==lead) for n in NAMES];axes[1].bar(x+(i-.5)*.35,values,.35,color='0.65' if i==0 else '0.9',edgecolor='black',hatch=hatch,label=f'{lead} LT')
 for a in axes:a.set_xticks(x,NAMES,rotation=15);a.legend(fontsize=7)
 axes[0].set_ylabel('Pooled S error at matched coverage');axes[1].set_ylabel('Confident forecast-sign accuracy');save(fig,'F18_matching_paper')
 after={k:sha(ROOT/k) for k in before};receipt=dict(post_hoc=True,presentation_only=True,before_sha256=before,after_sha256=after,page_sizes_points=sizes,styles={k:dict(line_style=str(v[0]),marker=v[1]) for k,v in STYLE.items()},source_hashes={n:sha(ROOT/'receipts'/n) for n in ['acd_stage9.json','acd_stage10b.json','acd_stage10b_decisions.json','acd_stage15_matching.json']})
 (ROOT/'receipts/acd_stage15_figures.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
