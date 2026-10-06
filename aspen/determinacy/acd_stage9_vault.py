"""Publish Stage9 vault note from the receipt; no manual number transcription."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def run():
 d=json.load(open(ROOT/'receipts/acd_stage9.json'))
 url='https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/'
 complete=all(d['F'][n].get('selected_step') is not None and d['C'][n].get('model')==n for n in ['CNN-F','CNN-F-resp'])
 status='complete' if complete else 'gpu-work-running'
 lines=['---','title: Aspen counterfactual determinacy Stage 9','type: research-result','status: '+status,'created: 2026-10-06','tags: [aspen, determinacy, post-hoc]','---','# Stage 9 — review-2 analyses','', 'Post hoc confirmation; licenses no frozen route. Physics and scoring: sulaco CPU. GPU inference and new forcing-conditioned training: authorized local Spark NVIDIA GB10. Paper and abstract untouched.','', 'Status: '+status+'. Existing checkpoint results and F completion are published as each finishes. Missing CNN-roll/CNN-resp copies are reported as unavailable pending supplied paths.','']
 for title,path in [('Reading','ACD_STAGE9_READING.md'),('Receipt','receipts/acd_stage9.json'),('Training freeze','ACD_STAGE9_TRAINING_FREEZE.md'),('Numbers','NUMBERS_ACD.md')]:lines.append('- ['+title+']('+url+path+')')
 for name in ['F11_tangent','F12_variance','F13_reliability','F14_amplitude']:
  lines.append('- '+name+': [PDF]('+url+'figures/'+name+'.pdf), [PNG]('+url+'figures/'+name+'.png)')
 lines+=['','Headlines (exact values; see receipt for intervals and denominators):','']
 for label,key in [('A2','A2'),('A4','A4')]:lines.append('- '+label+': '+json.dumps(d['A'][key] if label=='A4' else {k:d['A'][key][k] for k in ['pairs','counts','case_averaged','pooled','interval']}))
 for amp in d['B']['B3']:
  lines.append('- B3 amplitude '+str(amp['amplitude'])+': '+json.dumps(dict(comparisons=[r for r in amp['comparisons'] if r['lead'] in [2,3]],endpoint=amp['first_loss']['interval'])))
 for name,r in d['C'].items():lines.append('- C '+name+': '+json.dumps({k:r[k] for k in ['status','confidence_readings','state_skill','calibration_test'] if k in r}))
 lines+=['- F: '+json.dumps(d['F']),'','Resolution rules fired:','']+['- '+r for r in d['resolutions']]
 text='\n'.join(lines)+'\n'
 target=Path('/home/todd/obsidian-vault/04-Results/R_Aspen-Counterfactual-Determinacy-Stage9-2026-10.md')
 target.write_text(text)
 (ROOT/'receipts/acd_stage9_vault.md').write_text(text)
 print(target)
if __name__=='__main__':run()
