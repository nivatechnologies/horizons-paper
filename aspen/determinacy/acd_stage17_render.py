"""Render Stage 17 entirely from its computed receipt."""
from acd_stage17 import *
def render():
 d=json.loads(RECEIPT.read_text());lines=['# Stage 17 review-5 readings','','Post hoc on confirmation; licenses no frozen route. CPU-only saved-output calculations on sulaco. No integration, inference, sampling, Spark access or protected-stage mutation.','','## A. Tangent response','','Existing endpoint-amplitude B2 rows reproduced bit-for-bit. The main amplitude uses the saved confirmation costs. Relative difference below is the equal case/action median of per-draw relative differences; pooled median and within-pair distributions are also in the receipt.','','| a | Lead | Sign agreement | Pooled correlation | Median relative difference | Three-class agreement | Three-class kappa | Binary agreement | Binary kappa | Median zG | Median zD |','|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
 def fmt(x):return '—' if x is None else format(x,'.8g') if isinstance(x,(float,int)) else str(x)
 for r in sorted(d['A']['B2'],key=lambda x:(x['lead'],x['amplitude'])):
  keys=['amplitude','lead','per_draw_sign_agreement','pooled_per_draw_correlation','median_relative_difference','three_class_agreement','three_class_cohen_kappa','confidence_classification_agreement','cohen_kappa','median_z_G','median_z_D']
  lines.append('| '+' | '.join(fmt(r[k]) for k in keys)+' |')
 lines+=['','Posterior near-zero mass uses the saved Stage 11 climatological tangent SD for each pattern and lead.','','| a | gamma | Lead | Patterns | Q25 | Median | Q75 |','|---:|---:|---:|---|---:|---:|---:|']
 for r in d['A']['near_zero_mass']:lines.append('| '+' | '.join(map(fmt,[r['amplitude'],r['gamma'],r['lead'],r['patterns'],r['mass']['q25'],r['mass']['median'],r['mass']['q75']]))+' |')
 lines+=['','## C. Selected-action risk','','All existing decision readings reproduced exactly before extending them. New harm counts use realized D >= 0 among acted cases; the source reproduction retains strict D > 0. Conditional CP lower and upper limits each use a one-sided confidence level. Selected-action reliability is a post hoc diagnostic.','','| Model | Lead | Policy | Actions | Harms | Conditional harm | Lower95 | Upper95 | Unconditional upper95 | Expected harms |','|---|---:|---|---:|---:|---:|---:|---:|---:|---:|']
 for model,records in d['C']['models'].items():
  for r in records['selected']:
   cp=r['harm_conditional_CP_one_sided95'] or [None,None]
   lines.append('| '+' | '.join(map(fmt,[model,r['lead'],r['policy'],r['actions'],r['harms'],r['harm_conditional'],*cp,r['unconditional_harm_CP_upper95'],r['expected_harms']]))+' |')
 lines+=['','Selected-action reliability; E includes probabilities below one-half so no acted case is silently omitted.','','| Model | Lead | Policy | Lower edge | Upper edge | Cases | Mean predicted benefit | Observed benefit | CP lower95 | CP upper95 |','|---|---:|---|---:|---:|---:|---:|---:|---:|---:|']
 for model,records in d['C']['models'].items():
  for r in records['selected']:
   for b in r['reliability']:
    cp=b['CP_one_sided95'] or [None,None]
    lines.append('| '+' | '.join(map(fmt,[model,r['lead'],r['policy'],b['lower_edge'],b['upper_edge'],b['acted_cases'],b['mean_probability'],b['observed_benefit'],*cp]))+' |')
 lines+=['','Benefit margin: '+d['C']['margin_definition']+'.','','| Model | Lead | Delta | Actions | Harms | Insufficient benefit | Mean regret |','|---|---:|---:|---:|---:|---:|---:|']
 for model,records in d['C']['models'].items():
  for r in records['margins']:lines.append('| '+' | '.join(map(fmt,[model,r['lead'],r['delta'],r['actions'],r['harms'],r['insufficient_benefit'],r['mean_regret']]))+' |')
 lines+=['','Harm magnitudes, regret distributions and gate-threshold risk/coverage/regret curves are fully retained in the receipt.','','## E. Methods','','See ACD_METHODS_WINDOWS_BETTING.md for every output tick, time and LT value, variance convention, running-maximum inversion and code hashes. No new interval uses fallback.']
 if 'B' in d:
  lines+=['','## B. Event scores','',''+d['B']['frontier_scope'],'','| Model | Lead | Forecast Brier | Seven-pattern benefit Brier | All-eight benefit Brier |','|---|---:|---:|---:|---:|']
  for m,rows in d['B']['models'].items():
   if m=='CNN-F-resp':continue
   for r in rows:lines.append('| '+' | '.join(map(fmt,[m,r['lead'],r['forecast']['case_Brier'],r['benefit']['seven_zero_mean']['case_Brier'],r['benefit']['all_eight']['case_Brier']]))+' |')
  lines+=['','Signed probabilities are used for Brier scores and event reliability. Reliability CP intervals are pooled and descriptive. Risk gates depend only on predicted modal probability; cases without answers are omitted from case-error bounds.','','| Model | Lead | Event | Brier difference | Lower99 | Upper99 |','|---|---:|---|---:|---:|---:|']
  for r in d['B']['Brier_differences']:
   if r['model']=='CNN-F-resp':continue
   q=r['interval'];lines.append('| '+' | '.join(map(fmt,[r['model'],r['lead'],r['event'],q['point'],q['lower'],q['upper']]))+' |')
  lines+=['','| Model | Lead | Draw J8 RMSE | Draw J8 bias | Ensemble J8 RMSE | Forecast Brier | Confident S pooled error | Seven-pattern benefit Brier |','|---|---:|---:|---:|---:|---:|---:|---:|']
  for m,rows in d['B']['models'].items():
   if m=='CNN-F-resp':continue
   for r in rows:
    f=r['frontier'];lines.append('| '+' | '.join(map(fmt,[m,r['lead'],*[f[k] for k in ['per_draw_J8_RMSE','per_draw_J8_bias','ensemble_mean_J8_RMSE_against_realized','forecast_Brier','pooled_confident_S_error','benefit_Brier_seven']]]))+' |')
  lines+=['','## D. Transfer diagnostic','',''+d['D']['bound_definition'], '', '| Model | Lead | Median gap | P90 gap | Median bound | Share below 0.05 | Share at least one |','|---|---:|---:|---:|---:|---:|---:|']
  for r in d['D']['rows']:lines.append('| '+' | '.join(map(fmt,[r[k] for k in ['model','lead','median_probability_difference','p90_probability_difference','median_minimized_bound','share_bound_below_0_05','share_bound_at_least_one']]))+' |')
 else:lines+=['','B and D pending: the required Stage 15A committed receipt and ranking definitions are absent from the fetched branch. No outcomes were used to set a substitute equivalence margin.']
 lines+=['','## R-other and sequencing','']+d['resolutions']
 (ROOT/'ACD_STAGE17_READING.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':render()
