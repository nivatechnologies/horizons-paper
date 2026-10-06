"""Stage9 report and figures generated exclusively from computed receipts."""
import os
os.environ['MPLBACKEND']='Agg'
import json,hashlib,shutil
from pathlib import Path
import numpy as np,matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent;RUN=ROOT/'runs/stage9'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def savefig(fig,name):
 fig.tight_layout()
 for ext in ['pdf','png']:fig.savefig(ROOT/f'figures/{name}.{ext}',dpi=180)
 plt.close(fig)
def figures(d):
 plt.rcParams.update({'font.size':9,'axes.prop_cycle':plt.cycler(color=['black','0.35','0.6','0.15','0.45','0.7'])})
 b=d['B']['B2'];fig,axs=plt.subplots(1,2,figsize=(10,4))
 for amp,style,marker in [(.04,'-','o'),(.64,'--','s')]:
  r=[r for r in b if r['amplitude']==amp];x=[v['lead'] for v in r]
  axs[0].plot(x,[v['per_draw_sign_agreement'] for v in r],style,marker=marker,label=f'a={amp}')
  axs[1].plot(x,[v['median_z_G'] for v in r],style,marker=marker,label=f'G; a={amp}')
  axs[1].plot(x,[v['median_z_D'] for v in r],'-.' if amp==.04 else ':',marker='x' if amp==.04 else '+',label=f'D; a={amp}')
 axs[0].set_ylabel('Per-draw sign agreement');axs[1].set_ylabel('Median posterior |mean| / SD')
 for ax in axs:ax.set_xlabel('Lead (LT)');ax.legend()
 fig.suptitle('Post hoc confirmation: tangent and finite response');savefig(fig,'F11_tangent')
 fig,axs=plt.subplots(1,2,figsize=(11,4))
 styles=[('-', 'o'),('--','s'),(':','^'),('-.','x'),((0,(5,1,1,1)),'+'),((0,(1,2,3,2)),'d'),((0,(6,2,2,2)),'v')]
 for ax,group in zip(axs,['uniform','seven_zero_mean']):
  rows=[r for r in d['B']['B1'] if r['patterns']==group]
  for band,(name,(style,marker)) in enumerate(zip(rows[0]['terms'],styles)):
   x=[r['lead'] for r in rows];y=[r['terms'][name]['median'] for r in rows]
   ax.plot(x,y,linestyle=style,marker=marker,label=name)
   ax.fill_between(x,[r['terms'][name]['q25'] for r in rows],[r['terms'][name]['q75'] for r in rows],color='0.8',alpha=.16,hatch=['/','\\','x','-','+','o'][band])
  ax.set_title(group);ax.set_xlabel('Lead (LT)');ax.set_ylabel('Share of within-pair Var(D)');ax.legend(fontsize=7)
 fig.suptitle('Post hoc confirmation: descriptive variance decomposition (median, IQR)');savefig(fig,'F12_variance')
 fig,axs=plt.subplots(1,2,figsize=(11,4))
 for (name,model),(style,marker) in zip([(n,m) for n,m in d['C'].items() if 'reliability' in m],styles):
  if not isinstance(model,dict) or 'reliability' not in model:continue
  r=[r for r in model['reliability'] if r['questions']]
  axs[0].errorbar([v['mean_probability'] for v in r],[v['accuracy'] for v in r],yerr=np.array([[v['accuracy']-v['CP95'][0] for v in r],[v['CP95'][1]-v['accuracy'] for v in r]]),linestyle=style,marker=marker,label=name)
  r=[r for r in model['error_coverage'] if r['answers']]
  axs[1].plot([v['coverage'] for v in r],[v['pooled_error'] for v in r],linestyle=style,marker=marker,label=name)
 axs[0].plot([.5,1],[.5,1],':',marker='+',color='0.6');axs[0].set_xlabel('Mean modal probability');axs[0].set_ylabel('Observed accuracy (descriptive pooled CP95)')
 axs[1].set_xlabel('Coverage');axs[1].set_ylabel('Pooled error')
 for ax in axs:ax.legend(fontsize=7)
 fig.suptitle('Post hoc confirmation: seven-pattern matched questions at 2 LT');savefig(fig,'F13_reliability')
 fig,axs=plt.subplots(1,2,figsize=(10,4))
 base=json.load(open(ROOT/'receipts/acd_stage6.json'))['A']['A1']['comparisons']
 amps=d['B']['B3']
 for lead,style,marker in [(2,'-','o'),(3,'--','s')]:
  points=[(r['amplitude'],next(v for v in r['comparisons'] if v['lead']==lead)) for r in amps]
  points.append((.16,next(v for v in base if v['lead']==lead)));points.sort()
  x=[a for a,r in points]
  axs[0].plot(x,[r['all_S_share'] for a,r in points],style,marker=marker,label=f'S {lead} LT')
  axs[0].plot(x,[r['observation_S_share'] for a,r in points],':',marker='x' if lead==2 else '+',label=f'observation S {lead} LT')
  axs[0].plot(x,[points[0][1]['Fc_share']]*len(x),linestyle=style,marker='d' if lead==2 else 'v',color='0.6',label=f'Fc {lead} LT')
  axs[1].errorbar(x,[r['seven_minus_Fc']['point'] for a,r in points],yerr=np.array([[r['seven_minus_Fc']['point']-r['seven_minus_Fc']['lower'] for a,r in points],[r['seven_minus_Fc']['upper']-r['seven_minus_Fc']['point'] for a,r in points]]),linestyle=style,marker=marker,label=f'{lead} LT')
 for ax in axs:ax.set_xscale('log',base=2);ax.set_xlabel('Amplitude');ax.legend(fontsize=7)
 axs[0].set_ylabel('Confident share');axs[1].set_ylabel('Seven-pattern S − Fc (betting99%)')
 fig.suptitle('Post hoc confirmation amplitude; 0.16 retained baseline');savefig(fig,'F14_amplitude')
def run():
 d=json.load(open(RUN/'receipt_analyses.json'));d['B'].update(json.load(open(RUN/'forward_readings.json')));d['E']=json.load(open(RUN/'provenance.json'));d['C']={}
 for name in ['posterior','CNN-20k','CNN-roll','CNN-resp','CNN-cost','CNN-F','CNN-F-resp']:
  p=RUN/f'metrics_{name}.json'
  if p.exists():d['C'][name]=json.load(open(p))
  elif name in ['CNN-roll','CNN-resp']:d['C'][name]=dict(status='UNAVAILABLE',resolution='R-other: no registered sulaco checkpoint located; no substitute and no comparative claim')
  else:d['C'][name]=dict(status='RUNNING')
 d['CNN_provenance']=json.load(open(RUN/'cnn_provenance.json'))
 discard=ROOT/'runs/stage9_training/discarded_training.json'
 if discard.exists():d['discarded_training']=json.load(open(discard))
 d['F']={}
 for name in ['CNN-F','CNN-F-resp']:
  p=ROOT/f'runs/stage9_training/{name}/complete.json'
  d['F'][name]=json.load(open(p)) if p.exists() else dict(status='RUNNING',training_host='spark-89d8',gpu='NVIDIA GB10')
 d['resolutions']=['R-other: initial training pair order biased the base action branch; corrected random orientation before scheduled checkpoints, fresh restart, discarded GPU duration charged to CNN-F cap.', 'R-other: all Stage9 readings are post hoc and license no frozen route; no familywise claim over the exploratory comparisons.',
 'R-other: endpoint uncertainty flips retain the original1332 eligible pairs; no selection of a new cohort.',
 'R-other: pooled Clopper–Pearson reliability intervals are descriptive with clustered questions; calibration test uses independent cases.',
 'R-other: sigma is uncentered RMS on64 endpoint states; Jbar uses a different4096-state multi-window sample.',
 'R-other: forcing-conditioned response loss preserves four-step base loss and uses the AFD paired-loss normalization principle; validation one LT is a nominal12-step grid rollout.']
 d['resolutions'].append(d['CNN_provenance']['CNNcost']['resolution'])
 d['resolutions'].append('R-other: CNN-cost is a direct window-cost head; state RMSE and anomaly correlation are not defined, so only cost and question metrics are reported.')
 for name in ['CNN-roll','CNN-resp']:
  if d['C'][name].get('status')=='UNAVAILABLE':d['resolutions'].append(d['C'][name]['resolution']+f' ({name})')
 for name,training in d['F'].items():
  if training.get('capped'):
   d['resolutions'].append(f"R-other: {name} reached its training budget and completed {training['step']} updates; selected checkpoint {training['selected_step']} by the frozen validation rule. No claim of a completed 20,000-update run.")
 if all('step' in r for r in d['F'].values()) and len({r['step'] for r in d['F'].values()})>1:
  d['resolutions'].append('R-other: the forcing-conditioned models completed different update counts under their separate time caps; their comparison does not isolate the paired-response loss effect.')
 d['environment']=json.load(open(RUN/'execution_environment.json'))
 d['verification']=json.load(open(RUN/'verification.json'))
 d['jvp_check']=json.load(open(RUN/'jvp_implementation_check.json'))
 d['source_hashes']={p.name:sha(p) for p in ROOT.glob('acd_stage9*.py')}
 p=ROOT/'receipts/acd_stage9.json';p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
 figures(d)
 lines=['# Stage 9 review-2 analyses','', 'Post hoc confirmation analyses; licenses no frozen route. Physics forward runs and truth scoring on sulaco CPU. GPU training/inference on locally authorized Spark NVIDIA GB10. Paper and abstract untouched.','', 'Machine-readable receipt: receipts/acd_stage9.json. Exact methods and code hashes: ACD_STAGE9_TRAINING_FREEZE.md and the receipt.']
 a=d['A'];lines+=['','## A — statistics','',f"A2: {a['A2']['pairs']} eligible pairs in {a['A2']['cases']} cases. Counts: "+json.dumps(a['A2']['counts'])+'.', 'Case-averaged versus pooled shares: '+json.dumps(dict(case=a['A2']['case_averaged'],pooled=a['A2']['pooled']))+'.', 'A4 global forecast-horizon rule through3LT: '+json.dumps(a['A4'])+'.','', '| Lead | Type | ESS median [IQR] | MC SE median | Within2SE of0.95 |','|---|---|---|---|---|']
 for r in a['A1']['precision']:lines.append(f"| {r['lead']} | {r['type']} | {r['ESS']['median']:.6g} [{r['ESS']['q25']:.6g}, {r['ESS']['q75']:.6g}] | {r['MC_se']['median']:.6g} | {r['threshold_uncertain_share']:.6g} |")
 lines+=['','Worst-case first-loss directions, fixed original cohort:']
 for r in a['A1']['worst_case']:lines.append('- '+r['direction']+': '+json.dumps(r['result']['interval']))
 lines+=['','Threshold sweep (.90,.95,.99): all same-lead contrasts and calibration readings in $.A.A3; first/last endpoint rows below.','', '| Threshold | First loss delta [99%] | Last confident delta [99%] |','|---|---|---|']
 for r in a['A3']:
  f=r['first_loss']['interval'];l=r['last_confident']['interval'];lines.append(f"| {r['threshold']} | {f['point']:.6g} [{f['lower']:.6g},{f['upper']:.6g}] | {l['point']:.6g} [{l['lower']:.6g},{l['upper']:.6g}] |")
 lines+=['','Threshold sweep details (threshold also applies to climatological confidence):','', '| Threshold | LT | All8 S−Fc point [99%] | Seven S−Fc point [99%] | Observation S accuracy [lower95] | Answers |','|---|---|---|---|---|---|']
 for sweep in a['A3']:
  for row,accuracy in zip(sweep['same_lead'],sweep['accuracy']):
   all8=row['all_minus_Fc'];seven=row['seven_minus_Fc'];acc=accuracy['S']
   lines.append(f"| {sweep['threshold']} | {row['lead']} | {all8['point']} [{all8['lower']},{all8['upper']}] | {seven['point']} [{seven['lower']},{seven['upper']}] | {acc['case_accuracy']} [{acc['case_lower']}] | {acc['answers']} |")
 lines+=['','## B — descriptive mechanism and amplitude','', 'B1 includes the RK4 residual and all covariance terms; the six shares sum to1 within each case–action pair. Medians/IQRs are descriptive and are reported separately for uniform decrease and seven zero-mean patterns in $.B.B1 and F12.','', '| Amplitude | Lead | Draw sign agreement | Draw correlation | Median relative difference | Three-class agreement | Kappa | median zG | median zD |','|---|---|---|---|---|---|---|---|---|']
 for r in d['B']['B2']:
  lines.append('| '+' | '.join(str(r[k]) for k in ['amplitude','lead','per_draw_sign_agreement','pooled_per_draw_correlation','pooled_median_relative_difference','three_class_agreement','three_class_cohen_kappa','median_z_G','median_z_D'])+' |')
 lines+=['','B3 matched-null confidence, accuracy and endpoint readings:']
 for r in d['B']['B3']:
  lines.append('- a='+str(r['amplitude'])+': '+json.dumps(dict(comparisons=[x for x in r['comparisons'] if x['lead'] in [2,3]],accuracy=[x for x in r['accuracy'] if x['lead'] in [2,3]],endpoint=r['first_loss']['interval'])))
 lines+=['','B1 variance-share summaries (equal case/action weighting; median [IQR]):']
 for r in d['B']['B1']:
  lines.append('- '+str(r['lead'])+' LT '+r['patterns']+': '+ '; '.join(k+' '+str(v['median'])+' ['+str(v['q25'])+', '+str(v['q75'])+']' for k,v in r['terms'].items()))
 lines+=['','## C — learned models','', 'Each inference uses the corresponding posterior draw history. Confidence-error and calibration are distinct: a lower accuracy among confident answers does not itself establish miscalibration. Calibration is checked by a case-level betting interval for predicted modal probability minus correctness; this is a necessary mean-calibration test, not a full conditional-calibration guarantee. CP reliability bars are descriptive because questions are clustered within cases.']
 for name,r in d['C'].items():
  lines.append('- '+name+': '+json.dumps({k:({kk:vv for kk,vv in r[k].items() if kk!='records'} if k.startswith('paired_endpoint') and r[k] is not None else r[k]) for k in ['status','confidence_readings','state_skill','state_skill_status','pooled_per_draw_errors','calibration_test','comparisons','paired_endpoint','paired_endpoint_fixed_posterior_cohort','execution'] if k in r}))
 lines+=['','Training/checkpoint provenance (contract expectations separated from measured receipts):',json.dumps(d['CNN_provenance'],indent=2)]
 lines+=['','## D — realized decisions','', '| Lead | Policy | Improvement | Regret | Act share | Harms | Median harm | Max harm | Zero-harm CP upper | Actions0..8 |','|---|---|---|---|---|---|---|---|---|---|']
 for r in d['D']:lines.append('| '+' | '.join(str(r[k]) for k in ['lead','policy','mean_improvement','mean_regret','acting_share','harms','median_harm','max_harm','zero_harm_CP_upper','chosen_actions'])+' |')
 lines+=['','## E — normalization provenance','',json.dumps(d['E'],indent=2),'','## F — training','',json.dumps(d['F'],indent=2),'','## Resolutions','']+['- '+r for r in d['resolutions']]
 lines+=['','Figures (PDF and PNG): F11_tangent, F12_variance, F13_reliability, F14_amplitude under figures/. All distinctions use grayscale plus markers/line styles; variance bands use hatching.','']
 (ROOT/'ACD_STAGE9_READING.md').write_text('\n'.join(lines))
 print('stage9 receipt/report/figures written',flush=True)
if __name__=='__main__':run()
