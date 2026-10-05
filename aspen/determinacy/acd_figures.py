"""Stage4 tables and greyscale figures from existing receipts only."""
import json,hashlib,os
from pathlib import Path
os.environ['MPLBACKEND']='Agg'
os.environ['CUDA_VISIBLE_DEVICES']=''
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
RAW=Path(os.environ.get('ACD_RECEIPTS_ROOT','/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs'))
OUT=ROOT/'figures'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read():return json.loads((ROOT/'receipts/acd_stage2.json').read_text())
def mechanism(d):
 m=d['R1m'];lines=['# Aspen mechanism — confirmation, descriptive','',
 'Source: receipts/acd_stage2.json, $.R1m. No fits, forecasts or new statistics. R1m intervals stored under descriptive are approximate bootstrap intervals and descriptive; they license no directional comparison. Quartiles and plotted IQR bands describe dispersion, not uncertainty in a median. z_F and divergence have saved quartiles but no saved bootstrap interval.',
 '',
 'R-other: z_D/z_F below is the ratio of the two saved medians, not the median of individual ratios. Per-lead divergence is the saved window average; its quartiles are unavailable. Tick-level divergence medians and quartiles remain in NUMBERS and F3.',
 '',
 '| Lead (LT) | Median rho | Median c | Median z_D | Median z_F | Ratio of medians z_D/z_F | Confident S | Observation-confident S | Confident Fc | Window divergence |',
 '|---|---|---|---|---|---|---|---|---|---|']
 for i,r in enumerate(m['lead_relationship']):
  values=[r['lead'],m['rho']['median'][i],m['cancellation']['median'][i],m['z_D']['median'][i],m['z_F']['median'][i],m['z_D']['median'][i]/m['z_F']['median'][i],r['confident_S_share'],r['observation_S_share'],r['confident_Fc_share'],r['window_divergence_ratio']]
  lines.append('| '+' | '.join(repr(x) for x in values)+' |')
 lines+=['','Fc means the sign of the unforced window-energy anomaly. Confidence is posterior modal probability at least 0.95 under the declared model class, prior, noise and actions. Observation-confident removes modal answers already confident under the frozen true-forcing climatological null.','']
 for key in ['rho','cancellation','z_D','z_F']:
  lines+=['| '+key+' lead (LT) | Q25 | Median | Q75 |','|---|---|---|---|']
  for i,r in enumerate(m['lead_relationship']):lines.append('| '+' | '.join(repr(v) for v in [r['lead'],m[key]['quartiles'][0][i],m[key]['median'][i],m[key]['quartiles'][1][i]])+' |')
  lines.append('')
 for key in ['cancellation','z_D']:
  lines+=['| '+key+' lower | Upper (exclusive) | Count | Confident S share | Mean Phi(z_D) |','|---|---|---|---|---|']
  for r in m['bins'][key]:lines.append('| '+' | '.join('unbounded' if r[k] is None else repr(r[k]) for k in ['lower','upper','count','confident_share','mean_Phi_zD'])+' |')
  lines+=['','Bins pool the saved case–action–lead values; they are descriptive relationships, not tests of mechanism or independent samples.','']
 (ROOT/'ACD_MECHANISM.md').write_text('\n'.join(lines).rstrip()+'\n')
def select_f1(d):
 null=np.asarray(d['null']['question_probabilities']);jbar=d['null']['jbar'];selection=[];hashes={}
 for r in sorted(d['R5']['arms']['Q']['site_records'],key=lambda r:r['case']):
  c=r['case'];p=RAW/f'conf/case_{c:03d}.npz'
  with np.load(p,allow_pickle=False) as a:j=a['J'].copy()
  li=3;k,l=r['k'],r['l'];s=j[:,:8,li]<j[:,8,None,li]
  prob=s.mean(0);modal=prob>=.5;conf=np.maximum(prob,1-prob)>=.95
  climate=np.array([null[a,li,int(modal[a])]>=.95 for a in range(8)])
  pair=j[:,k,li]<j[:,l,li];p0=float(pair.mean())
  eligible=bool(np.any(conf&~climate) and max(p0,1-p0)<.95 and r['confident'] and not r['excluded'])
  if eligible:
   # Authorized scoring only: realized cost is never passed to samplers or targeting.
   sp=RAW/f'conf/score_{c:03d}.npz'
   with np.load(sp,allow_pickle=False) as a:actual=a['actual_cost'].copy()
   eligible=bool(bool(actual[k,li]<actual[l,li])==r['modal'])
  selection.append(dict(case=c,qualifies=eligible))
  if not eligible:continue
  rp=RAW/f'conf/measure/refit_{c:03d}_3_0.npz'
  with np.load(rp,allow_pickle=False) as a:z=a['z'].copy();sites=a['sites'].copy()
  ids=[int(np.flatnonzero(pair)[0]),int(np.flatnonzero(~pair)[0])]
  for pth in [p,sp,rp]:hashes[str(pth)]=sha(pth)
  return dict(status='ILLUSTRATIVE',case=c,k=k,l=l,lead=2,draw_indices=ids,draw_costs=j[ids][:,[k,l]].tolist(),probe_sites=sites.tolist(),probe_values=z[sites].tolist(),pre_probability=p0,post_probability=r['p'],post_modal=r['modal'],observation_confident_actions=np.flatnonzero(conf&~climate).tolist(),candidates=selection,source_hashes=hashes,resolution='R-other: only window-energy trajectories of individual draws are saved; no individual state trajectory is reconstructed. Illustrative energy curves carry no population claim.')
 return dict(status='OMITTED',candidates=selection,resolution='R-other: no case satisfies the frozen F1 rule; F1 omitted.')
def figures(d):
 OUT.mkdir(exist_ok=True);plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
 captions={};manifest={}
 def save(fig,name,caption):
  fig.tight_layout()
  for ext in ['pdf','png']:
   p=OUT/(name+'.'+ext);fig.savefig(p,dpi=220,metadata={'Creator':'Aspen analysis','CreationDate':None,'ModDate':None} if ext=='pdf' else None);manifest[str(p.relative_to(ROOT))]=sha(p)
  plt.close(fig);captions[name]=caption
 f1=select_f1(d);(ROOT/'receipts/acd_stage4_f1.json').write_text(json.dumps(f1,indent=2)+'\n')
 leads=np.array([r['lead'] for r in d['R1m']['lead_relationship']])
 if f1['status']!='OMITTED':
  fig,axs=plt.subplots(1,2,figsize=(8,3.5));a=axs[0]
  for draw,style,marker in [(0,'-','o'),(1,'--','s')]:
   for action,color in [(0,'black'),(1,'0.55')]:
    # Separate panels would make action identity clearer than color alone: filled/open markers add cue.
    a.plot(leads,np.array(f1['draw_costs'])[draw,action],color=color,ls=style,marker=marker,mfc=color if action==0 else 'white',label=f"draw {f1['draw_indices'][draw]}, action {[f1['k'],f1['l']][action]}")
  a.axvline(2,color='0.6',ls=':');a.set(xlabel='Lead (LT)',ylabel='Window energy',title=f"F1 illustrative: confirmation case {f1['case']}");a.legend(fontsize=7)
  axs[1].scatter(f1['probe_sites'],f1['probe_values'],c='black',marker='x',s=60)
  axs[1].set(xlabel='Site',ylabel='Saved probe observation',title='Question-targeted probe')
  save(fig,'F1_illustrative',f"Illustrative, first qualifying confirmation case {f1['case']}, actions {f1['k']}/{f1['l']}, 2 LT. First saved draw of each opposing P answer; before p={f1['pre_probability']!r}, after Q p={f1['post_probability']!r}, correct. R-other: curves show saved window-energy forecasts, not individual physical-state trajectories (not saved); no reintegration. Draw identity uses line style and marker; action identity uses grey shade and filled/open markers. Saved four-site probe. No generalization from this selected case.")
 else:captions['F1_omitted']=f1['resolution']
 fig,axs=plt.subplots(2,2,figsize=(8,6))
 for ax,t in zip(axs.flat,['S','P','B','Fc']):
  rows=[r for r in d['R1'] if r['type']==t];x=[r['lead'] for r in rows]
  for key,style,marker in [('observation','-','o'),('confident','--','s')]:ax.plot(x,[r[key]['point'] for r in rows],color='black',ls=style,marker=marker,label=key)
  ax.set(xlabel='Lead (LT)',ylabel='Share',ylim=(0,1),title=t if t!='Fc' else 'Fc: sign of unforced energy anomaly');ax.legend(fontsize=8)
 save(fig,'F2_confidence','Confirmation R1, frozen threshold and null. Observation-confident solid circles; all-confident dashed squares. P/B only at 2 and 3 LT under frozen cuts; lines connect tested leads without imputing other readings. Fc is the sign of the unforced window-energy anomaly.')
 fig,axs=plt.subplots(2,2,figsize=(8,6));m=d['R1m']
 for ax,key,title in [(axs[0,0],'rho','Posterior energy correlation'),(axs[0,1],'cancellation','Cancellation ratio'),(axs[1,0],'divergence_ratio','Divergence / factual spread')]:
  v=m[key];x=np.arange(len(v['median']))*.05/float(json.loads((ROOT/'receipts/acd_step0.json').read_text())['LT']) if key=='divergence_ratio' else leads
  ax.plot(x,v['median'],'k-o',markevery=8 if key=='divergence_ratio' else 1,ms=3,label='median')
  ax.fill_between(x,*v['quartiles'],facecolor='0.9',edgecolor='0.6',hatch='///',linewidth=.3,label='IQR')
  ax.set(xlabel='Time after action (LT)' if key=='divergence_ratio' else 'Lead (LT)',title=title);ax.legend(fontsize=7)
 ax=axs[1,1]
 for key,style,marker,hatch,grey in [('z_D','-','o','///','0.85'),('z_F','--','s','xxx','0.95')]:
  v=m[key];ax.plot(leads,v['median'],color='black',ls=style,marker=marker,label=key+' median');ax.fill_between(leads,*v['quartiles'],facecolor=grey,edgecolor='0.6',hatch=hatch,linewidth=.3,label=key+' IQR')
 ax.set(xlabel='Lead (LT)',ylabel='Standardized magnitude (log scale)',yscale='log',title='Effect and unforced anomaly');ax.legend(fontsize=7)
 save(fig,'F3_mechanism','Confirmation R1m saved medians and IQR dispersion bands; no new statistics. Divergence uses saved output ticks on a Lyapunov-time axis, not per-window quartiles. z_D solid circles/slash hatching; z_F dashed squares/cross hatching. Stored R1m bootstrap intervals are approximate and descriptive; these plotted bands are quartiles, not bootstrap confidence intervals.')
 dev=json.loads((ROOT/'receipts/acd_stage1.json').read_text())
 fig,ax=plt.subplots(figsize=(6,4))
 for label,rows,style,marker in [('posterior — confirmation',d['reliability'],'-','o'),('crude — confirmation',d['R3']['reliability'],'--','s'),('CNN — confirmation',d['R6']['reliability'],'-.','^'),('RML — development',dev['R3b']['reliability'],':','D')]:
  rr=[r for r in rows if r['answers'] and r['accuracy'] is not None]
  ax.plot([(r['lower']+r['upper'])/2 for r in rr],[r['accuracy'] for r in rr],color='black',ls=style,marker=marker,label=label)
 ax.plot([.5,1],[.5,1],color='0.7',ls='--',label='identity');ax.set(xlabel='Saved confidence-bin midpoint',ylabel='Empirical answer accuracy',xlim=(.5,1),ylim=(.45,1.02));ax.legend(fontsize=8)
 save(fig,'F4_reliability','Saved aggregate reliability bins. Posterior/crude/CNN are confirmation; RML is development and is labelled development. CNN is the deterministic CNN emulator at its frozen lead. Posterior/crude/RML aggregate their saved tested leads; CNN is 2 LT only. Curves have distinct line styles and markers. These mixed panels and bin aggregates do not establish a comparator ordering or RML confirmation performance.')
 fig,ax=plt.subplots(figsize=(6,4));arms=['Q','F','V','R']
 bars=ax.bar(arms,[d['R5']['arms'][a]['C'] for a in arms],color=['0.8']*4,edgecolor='black')
 for b,h,a in zip(bars,['///','xxx','...','\\\\'],arms):
  b.set_hatch(h);r=d['R5']['arms'][a];ax.text(b.get_x()+b.get_width()/2,b.get_height()+.008,f"{r['correct']}/{r['population']}",ha='center')
 ax.set(ylabel='Confident and correct share',xlabel='Q: question; F: forecast; V: spread; R: random',ylim=(0,.32),title='Confirmation R5 at 2 LT')
 save(fig,'F5_measurements','Confirmation R5 arms Q/F/V/R, frozen first 60 qualifying cases at 2 LT. Arm A was cut; no all-site value is imputed. One persistent F-arm diagnostic failure remains unresolved in the denominator. Q did not reliably beat the best alternative (saved route DOES NOT BEAT). Counts shown are correct/population; all settled answers were correct.')
 (OUT/'CAPTIONS.md').write_text('# Aspen figures — receipt sources and scope\n\n'+'\n\n'.join('**'+k+'**. '+v for k,v in captions.items())+'\n')
 manifest['figures/CAPTIONS.md']=sha(OUT/'CAPTIONS.md')
 (ROOT/'receipts/acd_stage4_figures.json').write_text(json.dumps(dict(source_hashes={p:sha(ROOT/p) for p in ['receipts/acd_stage2.json','receipts/acd_stage1.json','receipts/acd_step0.json','receipts/acd_stage4_f1.json']},outputs=manifest,captions=captions),indent=2)+'\n')
 print('F1',f1['status'],f1.get('case'));print('Figures',list(manifest))
if __name__=='__main__':
 d=read();mechanism(d);figures(d)
