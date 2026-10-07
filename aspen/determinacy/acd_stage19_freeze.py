"""Write Stage19 Freeze A from code, authorization constants and saved records."""
import os
os.environ.update(ACD_INHERITED_ROOT='/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision',NUMBA_NUM_THREADS='8')
import json,hashlib,re
from pathlib import Path
from acd_protocol import ROOT,INHERITED,protocol,assert_leaves
from acd_stage19_part1 import IDS,NAMES,OUT,sha,write,topology
step0=json.loads((ROOT/'receipts/acd_stage19_step0.json').read_text());assert step0['passed']
used=['acd_protocol.py','acd_fits.py','acd_posterior.py','acd_mechanism.py','acd_stage6_forward.py','acd_stage9_forward.py','acd_stage19_part1.py','acd_stage19_knownF.py','acd_stage19_step0.py','acd_stage19_freeze.py']
code={str(ROOT/n):sha(ROOT/n) for n in used};code.update({str(INHERITED/n):sha(INHERITED/n) for n in ['protocol.py','physics.py']})
null={str(p.relative_to(ROOT)):sha(p) for p in [OUT/'reused/runs/null/null.npz',OUT/'reused/runs/stage4b_null/states.npz',OUT/'reused/runs/stage6/null_block.npz']}
import numpy as np
with np.load(OUT/'reused/runs/null/null.npz') as d:jbar=float(d['jbar'])
with np.load(OUT/'reused/runs/stage6/null_block.npz') as d:blockbar=float(d['jbar_block'])
# Earlier integer-ID roots and every namespace literal in earlier ACD source.
oldroots=set(protocol.AAH_IDS)|{v for n,v in protocol.IDS.items() if n not in NAMES}
oldnames=set()
for p in ROOT.glob('acd*.py'):
 if p.name.startswith('acd_stage19'):continue
 oldnames.update(re.findall(r'[\"\'](acd[-a-zA-Z0-9_/]+)[\"\']',p.read_text()))
oldroots.update(int.from_bytes(hashlib.sha256(n.encode()).digest()[:8],'little') for n in oldnames)
assert len(set(IDS.values()))==len(IDS) and not set(IDS.values())&oldroots
leaves=[]
for c in range(200):
 for sub in [0,1]:leaves.append((IDS[NAMES[0]],0,sub,c,0,0))
 for n in NAMES[1:]:
  for m in range(128):leaves.append((IDS[n],0,0,c,m,0))
  for sub in [1,2]:
   for chain in range(4):leaves.append((IDS[n],0,sub,c,chain,0))
assert len(leaves)==len(set(leaves));prior=assert_leaves();groups,reserved=topology()
d=dict(panel_instances=200,seeds=dict(ids=IDS,id_rule='first eight bytes of SHA-256(namespace), little endian; SeedSequence [ID,0,sub,case,member,action]',new_leaf_count=len(leaves),prior_acd_leaf_count=prior['count'],earlier_namespace_literals=sorted(oldnames),earlier_root_count=len(oldroots),root_disjoint=True,leaves_unique=True),code_hashes=code,null_hashes=null,jbar=jbar,jbar_block=blockbar,environment=step0['environment'],cpu_groups=groups,reserved_cpus=reserved,step0_receipt_sha256=sha(ROOT/'receipts/acd_stage19_step0.json'),knownF_stage15C_comparison='pending its commit; this contract will not change')
write(ROOT/'receipts/acd_stage19_freeze_a.json',d)
text='''# Stage 19 Freeze A — fresh reference confirmation panel

Part 1 is blind reference sampling. The fresh reference family is confirmatory; mechanism and learned-model readings will be frozen separately in Part 2. This stage licenses no frozen route. No emulator may read these draws, and no realized outcome may be computed or opened in Part 1.

## Generation and access

Generate 200 instances using `acd-r3-observation`. Use the inherited generation exactly: independent 8 + N(0,1) at every site, spin up 50 LT at F=8, eleven noise-free frames spaced 0.05 apart, and independent Gaussian observation noise of standard deviation 0.02 sigma. The hidden history is written only by generation into runs/stage19/hidden; neither posterior nor forecasting code opens it. Observations are atomically saved and hashed before inference. Every sampler, initializer, diagnostic and forecast file is saved and hashed before dependent consumers read it. Large arrays remain untracked. Per-case outputs and sampler attempts permit restart after a reboot; completed cases are verified and skipped.

## Main posterior

Use the frozen prior and likelihood from acd_posterior.py: x_first has independent Normal(0,(10 sigma)^2) components, F is Uniform(6,10), and the Gaussian likelihood uses the identical float64 RK4 observation map. Four vectorized dense-mass NUTS chains use target acceptance 0.9, 1000 warm-up iterations and 500 retained draws per chain. Initialization uses the frozen acd_fits.case_fits implementation: 128 independent noise-perturbed fits, original-observation misfit and path checks, and the first four valid members. New RNG leaves are supplied by the Stage19 adapter, without changing the inherited module's source. Fewer than four valid members stops the case for R-other instead of relaxing its initialization requirement.

Retain 128 evenly spaced draws per chain (512 total). Split rank R-hat <=1.01 and bulk ESS >=400 are required for every parameter and the log likelihood, with divergent fraction <=0.01. Test all eight D_k and J_8 at both 2 and 3 LT. A failed functional gate triggers forecasts and diagnostics on all 2000 draws, with an integer confidence threshold of 1900 votes. If gates still fail, including any parameter failure, rerun once with 2000 warm-up iterations and 500 draws per chain. Exclude only after that retry fails. Preserve both attempts and every gate vector. The frozen forward forecast map is used for the diagnostics.

## Known-forcing contract (Todd's instruction)

Target p(x_first | Y,F=8), with 40 sampled dimensions. The prior, likelihood, RK4 map, NUTS settings, thinning, diagnostic thresholds, full-draw rescoring and retry rule are identical to the main posterior, except that F is fixed at 8 and is absent from the sampled coordinates and parameter diagnostics. Each chain starts from a maximum-likelihood fit at F=8 to an independently noise-perturbed observation copy. The original misfit and path checks remain unchanged; select the first four valid members among 128 fits. `acd_stage19_knownF.py` implements this contract; its hash is recorded below. Namespace acd-r3-knownF-sampler is disjoint from all other streams. When Stage15C commits, compare its implementation and record any difference as R-other. Keep this Stage19 contract unchanged.

## Forecasts and frozen null

Forecast every retained draw of both posteriors under all nine options at amplitude 0.16, using each main draw's F or fixed F=8 for knownF. Use all eight inherited leads and inclusive output windows, global energy and the energy of sites 0 through 9. Main-posterior draws additionally use the unchanged Stage9 forward-mode RK4 tangent recursion and Stage9 B1 energy-budget code path (the Stage6 forward kernel), saving all per-draw G_k and budget terms. Record closure against the inherited cost calculation. No truth is needed for any of these computations. Reuse the saved 4096-state null, global J-bar and block J-bar unchanged; their source-file hashes are recorded below. MCMC output is not expected to be bitwise identical across hosts.

## Confirmatory reference family

All following readings belong to one declared family, each tested at the original 1% level, and all will be reported without selection:

- C1: original R0 accuracy at every lead, using the original criterion; PASS required at 2 LT.
- C2: original eligible paired first-loss endpoint and censoring. PRECEDES requires estimate at most -0.20 and the two-sided 99% interval's upper bound below zero. Report the direction criterion (upper bound below zero) separately.
- C3: at both 2 and 3 LT, observation-confident S share over all eight patterns minus confident F_c share, magnitude at least 0.15 and two-sided 99% interval excluding zero.
- C4: at both 2 and 3 LT, confident S share over seven zero-mean patterns minus confident F_c share, with the two-sided 99% interval wholly below zero.

All other Part1 quantities are descriptive. Realized-answer scoring waits for the pushed Part2 freeze; no mechanism or learned-model confirmatory reading is set here.

## Timing and continuation

First run five complete instances, including both posterior gate workflows and all prescribed forecasts, tangents, budget terms and block energies. Project the full panel on the recorded available CPU groups, adding conservative allowances for the original confirmation rescore and retry rates. Continue only if projected wall time is at most 24 hours. Otherwise save the timing receipt and stop. Each worker is pinned to four distinct physical cores; four physical cores remain outside all worker affinity groups for Stage18. Every step uses CPU-only JAX and float64, with exact NumPyro 0.22.0 and JAX 0.11.2. No GPU, Qwen service or AFD close-out file is touched.

## Machine-readable freeze

The following values are generated from existing source files, saved receipts and the namespace algorithm.

'''
text+='```json\n'+json.dumps(d,indent=2)+'\n```\n'
(ROOT/'ACD_STAGE19_FREEZE_A.md').write_text(text)
print(json.dumps(d,indent=2))
