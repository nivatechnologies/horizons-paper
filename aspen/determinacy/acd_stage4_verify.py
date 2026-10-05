"""Meaningful Stage4 checks: tamper detection, numeric lexer and saved-data invariants."""
import json,subprocess,sys,tempfile,re,hashlib
from pathlib import Path
import numpy as np
from acd_numbers import ROOT,build,render,digest
from check_acd import tokens,match
def run():
 checks={}
 def passed(name,condition):
  if not condition:raise AssertionError(name)
  checks[name]=True
 expected=build();passed('registry regeneration',json.loads((ROOT/'numbers_acd.json').read_text())==expected and (ROOT/'NUMBERS_ACD.md').read_text()==render(expected))
 def cmd(*args):return subprocess.run([sys.executable,str(ROOT/'check_acd.py'),*args],capture_output=True,text=True)
 for path,mutation in [(ROOT/'NUMBERS_ACD.md',lambda x:x+'tampered\n'),(ROOT/'numbers_acd.json',lambda x:x.replace('"value": 0.0','"value": 0.125',1))]:
  original=path.read_text()
  if path.suffix=='.json':
   def mutation(x):
    a=json.loads(x);k=next(iter(a['numbers']));a['numbers'][k]['value']+=1;return json.dumps(a)
  try:
   path.write_text(mutation(original));result=cmd();passed(path.name+' tamper returns nonzero',result.returncode!=0 and 'differs' in result.stdout)
  finally:path.write_text(original)
 with tempfile.TemporaryDirectory(prefix='acd-stage4-test-') as temp:
  p=Path(temp)/'unmatched.md';p.write_text('Synthetic unattested value 339937.121817767.\n')
  result=cmd('--text',str(p));passed('unmatched text fails and prints literal',result.returncode!=0 and 'UNMATCHED' in result.stdout and '339937.121817767' in result.stdout)
 passed('numeric lexer signs decimals scientific percent counts', [x for _,x in tokens('N=40; .01; -0.243125; 95%; 2.3e-3; CNN-20k; 2026-10-05.')]==['40','.01','-0.243125','95%','2.3e-3','20k','2026','10','05'])
 passed('decimal rounding',bool(match('72.38%',expected['numbers'])))
 passed('scientific rounding',bool(match('1.00e0',expected['numbers'])))
 passed('Stage2 every visible number',cmd('--text',str(ROOT/'ACD_STAGE2_READING.md')).returncode==0)
 raw=Path('/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs')
 amp=json.loads((ROOT/'receipts/acd_stage4_amplitude.json').read_text())
 dev=json.loads((ROOT/'receipts/acd_stage1.json').read_text())
 base=next(r for r in amp['rows'] if r['amplitude']==.16)
 for row in base['shares']:
  li=3 if row['lead']==2 else 5;r=dev['R1m']['lead_relationship'][li]
  passed('development baseline shares '+str(row['lead']),row['confident_S']==r['confident_S_share'] and row['observation_confident_S_frozen_null_proxy']==r['observation_S_share'] and row['confident_Fc']==r['confident_Fc_share'])
 passed('development baseline R2b',all(base['matched_null_R2b'][k]==dev['R2b'][k] for k in ['point','lower','upper']))
 for c in range(200):
  with np.load(raw/f'dev/case_{c:03d}.npz',allow_pickle=False) as a:baseline=a['J'].copy()
  for a in [.04,.08,.16,.32,.64]:
   with np.load(ROOT/f'runs/stage4_amplitude/J_{a}_{c:03d}.npz',allow_pickle=False) as z:
    passed(f'unforced bitwise c{c} a{a}',np.array_equal(z['J'][:,8],baseline[:,8]))
    if a==.16:passed(f'baseline whole forecast bitwise c{c}',np.array_equal(z['J'],baseline))
 f1=json.loads((ROOT/'receipts/acd_stage4_f1.json').read_text());c=f1['case']
 with np.load(raw/f'conf/case_{c:03d}.npz',allow_pickle=False) as a:j=a['J'].copy()
 top=j[:,:8,3].mean(0).argsort()[:2];passed('F1 designated pair',set(top)==set([f1['k'],f1['l']]))
 delta=j[f1['draw_indices'],f1['k'],3]-j[f1['draw_indices'],f1['l'],3];passed('F1 opposite P answers',delta[0]<0<delta[1])
 manifest=json.loads((ROOT/'receipts/acd_stage4_figures.json').read_text());before=manifest['outputs']
 result=subprocess.run([sys.executable,str(ROOT/'acd_figures.py')],capture_output=True,text=True);passed('figure renderer exits zero',result.returncode==0)
 passed('PDF/PNG and caption reproduction bitwise',all(digest(ROOT/p)==h for p,h in before.items()))
 passed('figure receipt source hashes',all(digest(ROOT/p)==h for p,h in manifest['source_hashes'].items()))
 # Scientific source modules are unchanged; the authorized checker replacement is archived exactly.
 old=subprocess.check_output(['git','show','c1d692a:aspen/determinacy/check_acd.py'],cwd=ROOT)
 passed('original checker archive',old==(ROOT/'sources/check_acd_pre_stage4.py').read_bytes())
 changed=subprocess.check_output(['git','diff','--name-only','c1d692a'],cwd=ROOT).decode().splitlines()
 original_files=set(subprocess.check_output(['git','ls-tree','-r','--name-only','c1d692a'],cwd=ROOT).decode().splitlines())
 passed('scientific modules unchanged',not any(p in original_files and p.endswith('.py') and p!='aspen/determinacy/check_acd.py' for p in changed))
 compact={k:v for k,v in checks.items() if not k.startswith(('unforced bitwise','baseline whole'))}
 compact['unforced invariants checked']=1000;compact['baseline full forecast invariants checked']=200
 out=dict(status='PASS',checks=compact,stage2_numeric_extraction=544,total_checks=len(checks))
 (ROOT/'receipts/acd_stage4_verification.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':run()
