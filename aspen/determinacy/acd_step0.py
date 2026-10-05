"""Read-only verification, including authorized Step 0 item 7 truth reads."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import re,json,time
import numpy as np,numba
from acd_protocol import *
def run():
    numba.set_num_threads(8);begin=time.perf_counter()
    manifest={}
    for line in (INHERITED/'AFD_ARTIFACTS.md').read_text().splitlines():
        if line.startswith('- {'):
            obj=json.loads(line[2:])
            if 'sha256' in obj:manifest[obj['path']]=obj['sha256']
    records=[]
    for c in range(200):
        p=INHERITED/f'runs/test/input_{c:03d}.npz';computed=digest(p)
        with np.load(p) as data:true=data['true'];y=data['observed']
        regenerated,observed=physics.history('afd-observation-test',c,.01)
        actual=physics.costs(physics.simulate(np.repeat(true[-1,None],9,axis=0),8+.16*PATTERNS,.01))
        with np.load(INHERITED/f'runs/test/cpu_{c:03d}.npz') as data:stored=data['actual_cost']
        row=dict(case=c,sha256=computed,manifest_matches=computed==manifest.get(f'runs/test/input_{c:03d}.npz'),
                 reproduced=bool(np.array_equal(true,regenerated) and np.array_equal(y,observed)),actual_max_error=float(np.max(np.abs(actual-stored))))
        records.append(row)
        if not row['manifest_matches'] or not row['reproduced'] or row['actual_max_error']>1e-12:
            resolution('R-def',f'development {c} verification difference',row)
    numerical=json.loads((INHERITED/'runs/numerics/dtcheck.json').read_text())
    info=dict(base='1b1094a',LT=LT,SIGMA=SIGMA,LEADS=LEADS.tolist(),OUT=OUT,TICKS=TICKS.tolist(),WINDOWS=[w.tolist() for w in WINDOWS],
              pattern_rms=np.sqrt(np.mean(PATTERNS[:8]**2,axis=1)).tolist(),dt_record=numerical,
              hashes={f:digest(INHERITED/f) for f in ['protocol.py','physics.py','extras.py','campaign.py','inputs/CNN-20k.pt']},
              inputs=records,seconds=time.perf_counter()-begin,seed_leaves=assert_leaves())
    save_json(ROOT/'runs/audit/acd_step0.json',info)
    lines=['# ACD Step 0 — v2.3','',f"Read-only verification on sulaco; source base 1b1094a. Completed {len(records)} cases.",'',
           '| Item | Verification |','|---|---|',
           '| 1 Protocol | Exact LT/SIGMA/leads/OUT; ticks 0–83; unrounded inclusive epsilon window predicate confirmed in protocol.py |',
           '| 2 Observation model | history starts 8+Gaussian, rounds 50 LT/dt spin steps, then 11 frames at 0.05; observation sigma .02·SIGMA; last frame defines time zero |',
           '| 3 Actions/outcome | Eight unit-RMS patterns; persistent F+.16p; index 8 zero pattern; actual cost 9×8 |',
           '| 4 Cost | .5·mean(x²) then arithmetic window mean over inherited WINDOWS |',
           f"| 5 dt | Inherited record {numerical['status']} at {numerical['chosen_dt']} |",
           '| 6 Fits | extras.objective sums squared residuals/440; exact RK4 reverse; L-BFGS-B maxiter200, F=identify(y,dt); success/finite and all-frame RMS≤10SIGMA checks |',
           f"| 7 Data | Manifest matches {sum(v['manifest_matches'] for v in records)}/200; bitwise reproductions {sum(v['reproduced'] for v in records)}/200; maximum actual-cost discrepancy {max(v['actual_max_error'] for v in records):.3g} |",
           '| 8 CNN | Checkpoint hash below; 11 input frames and SIGMA normalization; action .16p/SIGMA. Base training draws amplitudes continuously through zero, so zero lies in its action support. No inference or model initialization performed |',
           '| 9 Two-scale | rhs2 uses h=1,c=10,b=10; state dt .001 recorded in inherited NUMBERS.md. R7 is optional and not run in this go |','',
           'No inherited module was edited. New posterior/readings follow v2.3. Any inherited discrepancy is resolved by R-def, never a pre-gate halt. Full per-case evidence: runs/audit/acd_step0.json.','',
           '| Artifact | SHA256 |','|---|---|']
    for f,v in info['hashes'].items():lines.append(f'| {f} | {v} |')
    (ROOT/'ACD_STEP0.md').write_text('\n'.join(lines)+'\n');print('Step 0 complete',flush=True)
if __name__=='__main__':run()
