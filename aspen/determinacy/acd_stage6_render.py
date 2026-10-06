"""Render post-hoc Stage6 report, figures and numeric receipt without changing the paper."""
import os
os.environ['MPLBACKEND']='Agg'
import json,numpy as np,time,subprocess
from pathlib import Path
from acd_stage6_analysis import ROOT,OUT,save,sha,TERMS
FIG=ROOT/'figures'
def pct(v):return 'not evaluable' if v is None else f'{100*v:.3f}%'
def bound(r):return f"{r['point']:.6f} [{r['lower']:.3f}, {r['upper']:.3f}]" if r['point'] is not None else 'not evaluable'
def figures(d):
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
 styles=[('-', 'o'),('--','s'),(':','^'),('-.','D'),('-','v'),('--','x'),(':','+'),('-.','*')]
 paths=[]
 def finish(fig,name,caption):
  fig.tight_layout()
  for ext in ['pdf','png']:
   p=FIG/(name+'.'+ext);fig.savefig(p,dpi=180);paths.append(str(p.relative_to(ROOT)))
  plt.close(fig);(FIG/(name+'_CAPTION.md')).write_text(caption+'\n')
 A=d['A'];B=d['B']
 fig,axs=plt.subplots(1,2,figsize=(12,5.3))
 fc=[r['Fc_share'] for r in A['A1']['comparisons']]
 for ax,key,title in zip(axs,['confident','observation'],['Confident intervention sign','Observation-confident intervention sign']):
  for pattern,(style,marker) in zip(A['A1']['patterns'],styles):
   ax.plot([r['lead'] for r in pattern['confidence']],[r[key] for r in pattern['confidence']],color=str(.05+.07*pattern['pattern']),linestyle=style,marker=marker,label='uniform decrease' if pattern['pattern']==0 else 'pattern '+str(pattern['pattern']))
  ax.plot([r['lead'] for r in A['A1']['comparisons']],fc,color='black',linestyle='--',marker='P',linewidth=2,label='sign of unforced window-energy anomaly')
  ax.set(xlabel='Lead (LT)',ylabel='Share',title=title,ylim=(-.02,1.02));ax.legend(fontsize=7,ncol=3,loc='upper center',bbox_to_anchor=(.5,-.18))
 finish(fig,'F7_patterns','POST HOC, confirmation. Per-pattern shares; observation confidence removes posterior-modal answers already climate-confident. Confidence in the sign of the unforced window-energy anomaly is the reference. Greyscale curves have distinct line-style/marker combinations. The uniform-decrease observation-confident share jumps when its null answer falls below 95% after 2 LT; this is a changing climate-confidence mask, not improved posterior confidence.')
 fig,axs=plt.subplots(2,2,figsize=(12,8))
 for row,(panel,label) in enumerate([('confirmation','Confirmation, amplitude 0.16'),('development_amplitude_0p64','Development exploratory, amplitude 0.64')]):
  m=B['B1'][panel];x=[r['lead'] for r in m['rows']]
  for col,indices in enumerate([[0,1,4],[2,3]]):
   for index,(style,marker) in zip(indices,styles):
    y=[r['terms'][index]['mean_posterior_mean'] for r in m['rows']]
    sd=[r['terms'][index]['mean_posterior_sd'] for r in m['rows']]
    axs[row,col].plot(x,y,color='black',ls=style,marker=marker,label={'injection':'injection contribution','mean_flow':'mean-flow contribution','rk4_residual':'RK4 residual','projection':'state projection','displacement':'squared displacement'}[TERMS[index]])
    axs[row,col].fill_between(x,np.array(y)-sd,np.array(y)+sd,facecolor='none',edgecolor='.65',hatch='//' if index%2==0 else '\\\\',linewidth=.2)
   axs[row,col].axhline(0,color='.5',ls=':');axs[row,col].set(xlabel='Lead (LT)',ylabel='Window energy contribution',title=label);axs[row,col].legend(fontsize=8)
 finish(fig,'F8_mechanism','POST HOC. Left: convolved direct injection, convolved mean-flow forcing and RK4 closure residual. Right: exact factual-state projection and squared displacement. Equal case/action weighting. Bands are ±mean within-posterior sample SD, descriptive spreads rather than confidence intervals. Development amplitude 0.64 is exploratory. Raw source-rate window means, all posterior correlations and term-z bins are in the Stage6 receipt.')
 fig,axs=plt.subplots(1,3,figsize=(13,4))
 rows=B['B2']['comparisons'];x=[r['lead'] for r in rows]
 for ax,keys in zip(axs[:2],[['all_S_share','Fc_share'],['observation_S_share','Fc_share']]):
  for key,(style,marker) in zip(keys,styles):
   ax.plot(x,[r[key] for r in rows],color='black',ls=style,marker=marker,label='block S' if key!='Fc_share' else 'sign of unforced block-energy anomaly')
  ax.set(xlabel='Lead (LT)',ylabel='Share',ylim=(-.02,1.02));ax.legend()
 axs[0].set_title('All confident');axs[1].set_title('Observation-confident')
 share=B['B2']['loss']['case_averaged_shares'];names=list(share)
 for i,name in enumerate(names):axs[2].bar(i,share[name],color='white',edgecolor='black',hatch=['//','\\\\','xx','..'][i])
 axs[2].set_xticks(range(len(names)),names,rotation=30);axs[2].set(ylabel='Eligible-case mean action share',title='Block paired first loss')
 finish(fig,'F9_block','POST HOC, confirmation. Energy of sites 0..9, normalized by10; block climatology uses saved4096 null states at true forcing. Left/middle: all/observation-confident S versus confidence in the sign of the unforced block-energy anomaly. Right: case-averaged paired first-loss categories on actions initially observation-confident with initially confident block forecast sign. No frozen route license.')
 fig,axs=plt.subplots(1,2,figsize=(11,4))
 for lead,(style,marker) in zip([2,3],styles):
  C=[r for r in A['A4']['policies'] if r['lead']==lead and r['policy']=='C']
  E=next(r for r in A['A4']['policies'] if r['lead']==lead and r['policy']=='E')
  for ax,key in zip(axs,['mean_regret','acting_share']):
   ax.plot([r['delta_fraction'] for r in C],[r[key] for r in C],color='black',ls=style,marker=marker,label=f'C, {lead} LT')
   refstyle,refmarker=('-.','^') if lead==2 else (':','D')
   ax.plot([0,.1],[E[key],E[key]],color='.5',ls=refstyle,marker=refmarker,label=f'E reference, {lead} LT')
 axs[0].set(xlabel='Margin / action-specific null SD(D)',ylabel='Mean realized regret vs best of nine')
 axs[1].set(xlabel='Margin / action-specific null SD(D)',ylabel='Acting share',ylim=(0,1.05))
 for ax in axs:ax.legend(fontsize=8)
 finish(fig,'F10_decision','POST HOC, confirmation. E chooses lowest posterior-mean cost among nine options including no action. C uses E’s chosen action only when posterior P(D<−delta·SD_null(D))≥0.95; otherwise no action. Null SD is action-specific and lead-specific, sample SD over saved matched null costs. Realized regret uses best of the same nine options. No fitted policy, new sampling or route license.')
 return paths
def render(d):
 A=d['A'];B=d['B'];C=d['C']
 lines=['# Aspen Stage6 — POST HOC confirmation analyses','',
 'Every confirmation analysis below was chosen after the frozen confirmation reading. It licenses **no frozen route**, paper or abstract sentence. Development amplitude 0.64 is additionally exploratory. Paper and abstract remain unchanged.',
 '', 'All 200 saved confirmation cases use every draw that was used to score that case (512 or 2000), retaining existing diagnostic exclusions. Case order is 0–199. Statistics reuse v2.3 case-level predictable betting bounds: 99% for differences; one-sided 95% for case-averaged calibration. Intervals are individually labelled, with no new family-wide or selection-adjusted guarantee.',
 '', '## A1: seven-pattern and all-pattern comparisons','',
 'Differences use each case’s mean confident S share minus its binary confident forecast-sign indicator. Seven-pattern means exclude pattern 0, the uniform decrease; patterns 1–7 are equally weighted. Fc always denotes the sign of the unforced window-energy anomaly.',
 '', '| Lead LT | Seven S | All S | Fc | Seven minus Fc, 99% interval | All minus Fc, 99% interval |','|---|---|---|---|---|---|']
 for r in A['A1']['comparisons']:lines.append(f"| {r['lead']} | {pct(r['seven_S_share'])} | {pct(r['all_S_share'])} | {pct(r['Fc_share'])} | {bound(r['seven_minus_Fc'])} | {bound(r['all_minus_Fc'])} |")
 lines+=['','| Pattern | Lead LT | Confident S | Observation-confident S |','|---|---|---|---|']
 for pattern in A['A1']['patterns']:
  for r in pattern['confidence']:lines.append(f"| {pattern['pattern']} | {r['lead']} | {pct(r['confident'])} | {pct(r['observation'])} |")
 lines+=['','Per-pattern confident/observation-confident shares at every lead and per-pattern first-loss earlier/later/same/beyond shares are in receipts/acd_stage6.json → A.A1.patterns. Eligibility is observation-confident S and confident Fc at lead 0, as frozen; uniform-decrease pattern 0 has no eligible actions if climatology supplies all its initial answers.','', '| Pattern | Earlier | Later | Same | Both beyond | Eligible cases/actions |','|---|---|---|---|---|---|']
 for r in A['A1']['patterns']:
  x=r['loss'];v=x['case_averaged_shares']
  lines.append('| '+' | '.join([str(r['pattern'])]+[pct(v[k]) for k in ['earlier','later','same','both_beyond']]+[str(x['cases'])+'/'+str(x['actions'])])+' |')
 lines+=['','## A2: confidence re-entry and last-confident endpoints','',
 '| Type | Eligible pairs | Observed first losses | Re-entry count | Of eligible pairs | Of observed losses | Unique re-entering cases |','|---|---|---|---|---|---|---|']
 for k,r in A['A2']['reentry'].items():lines.append('| '+' | '.join(map(str,[k,r['eligible_pairs'],r['observed_losses'],r['reentered'],pct(r['fraction_of_eligible']),pct(r['fraction_of_observed_losses']),r['unique_reentered_cases']]))+' |')
 lines+=['','First-loss later-minus-earlier: '+bound(A['A2']['first_loss']['interval'])+'. Last-confident-lead later-minus-earlier: '+bound(A['A2']['last_confident']['interval'])+'.',
 'Re-entry means a confident tested lead strictly after the first tested nonconfident lead. Fc is paired with each eligible action, so its pair-weighted share differs from a unique-case rate. Last-confident endpoints compare the last observed confident lead; a shared final-grid endpoint is a tie, not evidence of loss beyond 6 LT. No unobserved endpoint is inferred.',
 '', '## A3: Monte Carlo threshold sensitivity','',
 'Threshold-uncertain means |p−0.95|<2se with the saved draw set’s bulk indicator ESS, using the frozen half-count correction. Modal answers and climatological probabilities stay fixed; uncertainty changes confidence and therefore eligibility. Threshold-uncertain shares by question type and lead are in A.A3.uncertainty (original B over eight intervention actions).',
 '', '| Threshold-uncertain treated as | Lead LT | Observation S minus Fc | Seven S minus Fc | R2b-style later-minus-earlier |','|---|---|---|---|---|']
 for variant in A['A3']['sensitivity']:
  for t in [3,5]:
   r=variant['comparisons'][t];lines.append(f"| {variant['uncertain_counted']} | {r['lead']} | {bound(r['observation_minus_Fc'])} | {bound(r['seven_minus_Fc'])} | {bound(variant['loss']['interval'])} |")
 lines+=['','| Type | Lead LT | Threshold-uncertain share | Count / questions |','|---|---|---|---|']
 for r in A['A3']['uncertainty']:lines.append(f"| {r['type']} | {r['lead']} | {pct(r['share'])} | {r['count']} / {r['questions']} |")
 lines+=['','## A4: realized decision analysis','',
 'E minimizes posterior-mean J across all nine options. C takes E’s selected action only when P(D_k<−delta·SD_null(D_k))≥0.95. Null SD is action/lead-specific with ddof 1; delta is the displayed fraction. No action is index 8. Strict realized-cost increase counts as worse than no action. Regret is relative to realized best of nine; zero errors in this finite panel is not a zero-risk guarantee.',
 '', '| Lead LT | Policy | delta/SD | Mean realized regret | Worse than no action | Acting share |','|---|---|---|---|---|---|']
 for r in A['A4']['policies']:lines.append(f"| {r['lead']} | {r['policy']} | {r['delta_fraction']} | {r['mean_regret']:.9f} | {pct(r['worse_than_no_action_share'])} | {pct(r['acting_share'])} |")
 lines+=['','| Lead LT | Per-instance Fc-rule answered-not-confident / all S | / answered S | Conditional accuracy | B-nine confident | B-nine accuracy |','|---|---|---|---|---|---|']
 for r,b in zip(A['A4']['instance_Fc_rule'],A['A4']['best_of_nine']):lines.append(f"| {r['lead']} | {pct(r['answered_not_confident_share'])} | {pct(r['answered_not_confident_fraction_of_answered'])} | {pct(r['answered_not_confident_accuracy'])} | {pct(b['confident_share'])} | {pct(b['accuracy'])} |")
 lines+=['','## B1: energy-budget and projection mechanisms','',
 'The initial action and factual states are identical, so D starts at zero. Raw sources are a<p_k,x_k>/N and F_s(mean(x_k)−mean(x_8)). Each is propagated through dc/dt=−2c+source, with the same RK4 stage states and dt 0.01 as the trajectories. Their convolved contributions are window-averaged. The discretized energy difference also has a measured RK4 closure residual; it is reported as a third budget term. Injection + mean-flow + residual sum to D. The projection and squared-displacement terms sum algebraically to D at every draw/window. Sources/contributions are distinct; raw rate window means are retained in the per-draw archives.',
 'No causal term is identified by descriptive correlations alone. Equal case/action weighting is used for posterior means, sample SDs and posterior correlations. Minority-sign share is min(P(term>0), P(term≤0)) within each posterior. Binned confidence versus absolute mean/SD(z) is descriptive, not a new significance test.',
 '']
 for key,label in [('confirmation','Confirmation, amplitude 0.16'),('development_amplitude_0p64','Development exploratory, amplitude 0.64')]:
  m=B['B1'][key];lines +=['### '+label,'',
   f"Maximum energy-budget closure residual: {m['budget_closure_max_abs']:.12g}. Maximum exact projection-split discrepancy: {m['projection_closure_max_abs']:.12g}.",
   '', '| Lead LT | Term | Mean posterior mean | Mean posterior SD | Median z | Mean minority-sign share | Correlation minority-sign share, confident | Correlation log(1+z), confident |','|---|---|---|---|---|---|---|---|']
  for r in m['rows']:
   for term in r['terms']:
    lines.append(f"| {r['lead']} | {term['name']} | {term['mean_posterior_mean']:.9g} | {term['mean_posterior_sd']:.9g} | {term['median_z']:.6g} | {term['mean_sign_disagreement']:.6g} | {term['confidence_sign_disagreement_correlation']} | {term['confidence_log_z_correlation']} |")
 lines+=['','| Panel | Lead LT | Largest descriptive confidence association among convolved injection/mean-flow z | Correlation |','|---|---|---|---|']
 for key,m in B['B1'].items():
  for row in m['rows']:
   candidates=[x for x in row['terms'][:2] if x['confidence_log_z_correlation'] is not None]
   if candidates:
    term=max(candidates,key=lambda x:x['confidence_log_z_correlation'])
    lines.append(f"| {m['panel']} amplitude{m['amplitude']} | {row['lead']} | {term['name']} | {term['confidence_log_z_correlation']:.6f} |")
 lines+=['','All within-posterior contribution correlation matrices and term-z bins are in B.B1.*.rows. These show association with confidence loss; neither source attribution nor a learned causal mechanism is inferred.','',
 '## B2: block-energy observable','',
 'Chosen before Stage6 readings: sites 0..9, E_block=(1/20)sum x_i². The unforced block climate origin is the mean unforced window cost across all 4096 saved null states and all inherited windows. Climate confidence compares the posterior-modal answer to this block null at true F=8. The same stored draws and inherited lead/window predicates are used; realized block answers are computed only inside scoring.',
 '', f"Block climatological mean: {B['B2']['jbar']:.12g}. Full-energy saved-null reproduction error: {B['B2']['null_full_energy_reproduction_max_abs']:.12g}.",
 '', '| Lead LT | Confident block S | Observation-confident block S | Confident block Fc | Seven block S minus Fc, 99% | S case accuracy | One-sided95% lower |','|---|---|---|---|---|---|---|']
 for r,cal in zip(B['B2']['comparisons'],B['B2']['calibration']):
  lines.append(f"| {r['lead']} | {pct(r['all_S_share'])} | {pct(r['observation_S_share'])} | {pct(r['Fc_share'])} | {bound(r['seven_minus_Fc'])} | {pct(cal['S']['case_accuracy'])} | {pct(cal['S']['case_lower'])} |")
 lines+=['', 'Block paired first-loss later-minus-earlier: '+bound(B['B2']['loss']['interval'])+'. Case-averaged earlier/later/same/beyond shares: '+json.dumps(B['B2']['loss']['case_averaged_shares'])+'. All block calibration values and Fc betting bounds are retained in the receipt; diagnostic statuses do not license a frozen route.',
 '', '## B3: conventional factual forecast skill','', B['B3']['anomaly_origin']+'. '+B['B3']['time_definition']+'.',
 '', '| Lead LT | First saved time | Mean state RMSE/sigma | Mean spatial anomaly correlation | Window-mean RMSE/sigma | Window-mean anomaly correlation |','|---|---|---|---|---|---|']
 for r in B['B3']['rows']:lines.append(f"| {r['lead']} | {r['time']} | {r['RMSE_over_sigma']:.6f} | {r['spatial_anomaly_correlation']:.6f} | {r['window_mean_RMSE_over_sigma']:.6f} | {r['window_mean_spatial_anomaly_correlation']:.6f} |")
 lines+=['','## C: frozen CNN with posterior-draw histories','', 'Status: '+C['status']+'.']
 if C['status']=='COMPLETE':
  lines+=['The unchanged CNN-20k is fed each saved draw’s own noise-free H0..10 history and the action. All scoring draws are retained; any divergent surrogate draw would make that entire case contribute no confident answers rather than select surviving draws. Inferred forcing is encoded indirectly by the history, without a separate F channel.',
   'At 2 LT: confident S '+pct(C['comparisons_2LT']['all_S_share'])+', observation-confident S '+pct(C['comparisons_2LT']['observation_S_share'])+', confident unforced-anomaly sign '+pct(C['comparisons_2LT']['Fc_share'])+'.',
   'Seven-pattern difference: '+bound(C['comparisons_2LT']['seven_minus_Fc'])+'. Observation-confident S case accuracy '+pct(C['calibration_2LT']['S']['case_accuracy'])+', one-sided 95% lower '+pct(C['calibration_2LT']['S']['case_lower'])+'.',
   'GPU inference only; no training. Per-case draw counts, valid counts, micro-batches and checkpoint hash are in C.']
 else:lines +=[C.get('reason','No additional details')]
 lines+=['','## Resolution rules, validation and artifacts','']
 for r in d['resolutions']:lines.append('- '+r['rule']+': '+r.get('resolution',''))
 lines +=['','Verification, execution settings and source/output hashes: receipts/acd_stage6.json and receipts/acd_stage6_verification.json. NUMBERS regeneration is checked by check_acd.py. Figures: '+', '.join(d['figure_paths'])+'.',
 '', 'Vault: 04-Results/R_Aspen-Counterfactual-Determinacy-Stage6-2026-10.md. All reports are generated by script. No posterior/MAP/RML sampling, training or cloud compute. Qwen services and Baccus close-out remain untouched.','']
 return '\n'.join(lines)
def run():
 A=json.load(open(OUT/'A.json'));B=json.load(open(OUT/'B.json'));C=json.load(open(OUT/'C.json'))
 d=dict(stage=6,base='92d83355bb4b9c8f0a7205bfff341b3d55bd6b0d',post_hoc=True,licenses_frozen_route=False,
  A=A,B=B,C=C,settings=dict(dt=.01,dtype='float64',CPU_threads=32,analysis_threads=2,CNN_dtype='float32',CNN_energy_accumulation='float64',CNN_GPU_only=True,block_sites=list(range(10)),amplitude=.16,
  no_sampling=True,no_training=True,no_cloud=True),resolutions=[
  dict(rule='R-other',resolution='Stage6 is post hoc on confirmation; all comparisons, bounds and diagnostic statuses license no frozen route. No multiplicity/selection-adjusted inference is claimed.'),
  dict(rule='R-other',resolution='Retain measured RK4 energy-budget residual as a third closure term; do not describe two discretized continuous-budget contributions as exactly summing to trajectory energy.'),
  dict(rule='R-other',resolution='Last-confident tested lead is an observed-grid endpoint; both at the final grid point are tied, with no extrapolated loss time.')
  ]+C.get('rules',[]))
 if C['status']=='COMPLETE':
  C['cases']=len(C['members']);C['total_draws']=sum(r['draws'] for r in C['members']);C['total_valid_draws']=sum(r['valid_draws'] for r in C['members']);C['cases_with_any_invalid']=sum(r['valid_draws']<r['draws'] for r in C['members'])
  C['microbatch_min']=min(r['microbatch'] for r in C['members']);C['microbatch_max']=max(r['microbatch'] for r in C['members'])
 C['seconds_scope']='Elapsed in final resumed inference invocation, including loading earlier-case results; not total GPU-hours.'
 d['figure_paths']=figures(d)
 d['source_hashes']={p:sha(ROOT/p) for p in ['acd_stage6_forward.py','acd_stage6_analysis.py','acd_stage6_cnn.py','acd_stage6_render.py','acd_stage6_verify.py','acd_numbers.py','check_acd.py','acd_stats.py','acd_protocol.py','runs/stage4b_null/states.npz','runs/stage4b_null/null_0.16.npz','receipts/acd_stage2.json','receipts/acd_stage4b_null.json']}
 d['output_hashes']={str(p.relative_to(ROOT)):sha(p) for p in sorted(OUT.glob('*.npz'))}
 save(ROOT/'receipts/acd_stage6.json',d)
 text=render(d);(ROOT/'ACD_STAGE6_READING.md').write_text(text)
 url='https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/'
 vault='# Aspen Stage6 — POST HOC review-driven analyses\n\n[Full reading]('+url+'ACD_STAGE6_READING.md) · [Receipt]('+url+'receipts/acd_stage6.json) · [NUMBERS]('+url+'NUMBERS_ACD.md)\n\n'+text
 vault+='\n\nFigures: '+ ' · '.join('['+Path(p).name+']('+url+p+')' for p in d['figure_paths'])+'\n'
 (ROOT/'R_Aspen-Counterfactual-Determinacy-Stage6-2026-10.md').write_text(vault)
 print('Stage6 receipt, report, figures and vault copy generated',flush=True)
if __name__=='__main__':run()
