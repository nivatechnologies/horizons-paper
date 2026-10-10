# Stage22 Freeze F — fresh forcing-shift panel

Earlier freezes are unchanged. The Stage21 R2 result remains FAIL; this panel is neither pooled with it nor substituted for it. Start only after the prior queue, including Stage18 D/C, is complete and published. Freeze G was pushed before any Stage22 outcome is scored.

R2-S22: Retained CNN-noF minus CNN-F-E0-fixed confident-error share, on the seven zero-mean patterns at 2 LT. Each seed/instance requires at least one confident answer from both pipelines. Average the defined seed differences within each instance. Retain instances with at least one defined pair. The instance is the unit. Confirm only if the two-sided 99% v2.3 interval lies wholly above zero.

R5-S22: CNN-F-E0-rolling minus CNN-F-E0-fixed confident-error share, on the seven zero-mean patterns at 2 LT. Pair rolling seed k with fixed seed k. The contributing rule, seed averaging and instance unit are the same as R2. Confirm only if the two-sided 99% v2.3 interval lies wholly above zero. The existing Stage18 rolling path already accepts E0; no rollout logic changes are needed.

R6-S22: CNN-F-E0-rolling C(delta=0) harm conditional on acting at 3 LT, for each E0 seed. Use the exact one-sided 95% Clopper-Pearson lower bound and Freeze B L2 threshold (above 0.05), with strict-positive harms and zero-effect ties recorded separately. Confirm only if every seed passes. Only a thin wrapper around existing frozen statistic functions is authorized.

Panel size, balance and code-computed precision rationale are recorded below. Fixed n: no interim scoring, no extension after failure, no pooling with Stage21. Excluded instances are withheld and never replaced. Assignment follows the Stage21 permutation rule with only count and fresh namespaces changed. Posterior priors, NUTS settings, initialization, gates, thinning, full-draw rescoring and single warm-up retry stay unchanged. First-five timing uses the same worker layout and wall-time cap as Stage21.

Pipelines are retained CNN-noF, E0 fixed and rolling for every frozen E0 seed. Retained constant-eight CNN-F and posterior are descriptive only. No other confirmatory reading is added. All compared pipelines use the Baccus 170HX path. Frozen climatology is reused by hash. No earlier queue is preempted.

A failed E0-fixed seed makes R2-S22 and R5-S22 not evaluable. A failed E0-rolling seed makes R5-S22 and R6-S22 not evaluable. Available results remain descriptive. A nonzero task return code or missing complete.json marks the phase FAILED and blocks scoring/publication. Every task log is committed beside its execution JSON.

Execution reading (R-other): case count is the sole additional execution change beyond panel path; criteria unchanged. Parameterized copies leave earlier files untouched. N=200 with Stage21 namespaces must reproduce every value in all three committed Stage21 receipts exactly, including provenance and descriptive entries. Empty diffs, logged scoring-cache access, remaining literal inventory, case-coverage assertions, adapter hashes and line-level diffs are recorded with this freeze. Any differing value or failed assertion stops execution. Stage23 uses this same parameterization on the Stage22 panel.

The panel contract must be pushed before the first observation is generated. No outcome is generated or opened outside frozen scoring. Publication reports every required reading pooled and by forcing, with the full Freeze E descriptive set and uniform-decrease choice histogram.

```json
{
  "N": 1000,
  "forcing_counts": {
    "7": 500,
    "9": 500
  },
  "tasks": [
    {
      "name": "CNN-noF",
      "checkpoint": "runs/stage21/checkpoints/CNN-noF.pt",
      "estimator": null,
      "checkpoint_sha256": "4bfef787a80269dada0acd7ca74ef84eb6442a580c706a57333c55dc647b1f67",
      "estimator_sha256": null
    },
    {
      "name": "CNN-F-constantF",
      "arm": "constantF",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": null,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": null
    },
    {
      "name": "CNN-F-E0-fixed-seed1",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed1.pt",
      "kind": "E0",
      "rolling": false,
      "seed": 1,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "05b0c966567209037b87478b238939eeaa23f2202ae7148c06dd34797bdee3da"
    },
    {
      "name": "CNN-F-E0-fixed-seed2",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed2.pt",
      "kind": "E0",
      "rolling": false,
      "seed": 2,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "d461bae9dfd507b07955eda2342abe717900232af40cd5ac9e0b5981fb1fcd2f"
    },
    {
      "name": "CNN-F-E0-fixed-seed3",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed3.pt",
      "kind": "E0",
      "rolling": false,
      "seed": 3,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "dc6fe8559093681cece7166443cd1a8d44bdf7f8e794e9f07bed42bf2bb876a3"
    },
    {
      "name": "CNN-F-E0-fixed-seed4",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed4.pt",
      "kind": "E0",
      "rolling": false,
      "seed": 4,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "fc538e434c04df7ffa91fa9021f9bb64c6006700b95262772b5e139e492a195b"
    },
    {
      "name": "CNN-F-E0-fixed-seed5",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed5.pt",
      "kind": "E0",
      "rolling": false,
      "seed": 5,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "6a7edd4aee91e81b7a272c6e9b2a7962e9a000ed44ab7378f478ad6657a38e2f"
    },
    {
      "name": "CNN-F-E0-rolling-seed1",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed1.pt",
      "kind": "E0",
      "rolling": true,
      "seed": 1,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "05b0c966567209037b87478b238939eeaa23f2202ae7148c06dd34797bdee3da"
    },
    {
      "name": "CNN-F-E0-rolling-seed2",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed2.pt",
      "kind": "E0",
      "rolling": true,
      "seed": 2,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "d461bae9dfd507b07955eda2342abe717900232af40cd5ac9e0b5981fb1fcd2f"
    },
    {
      "name": "CNN-F-E0-rolling-seed3",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed3.pt",
      "kind": "E0",
      "rolling": true,
      "seed": 3,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "dc6fe8559093681cece7166443cd1a8d44bdf7f8e794e9f07bed42bf2bb876a3"
    },
    {
      "name": "CNN-F-E0-rolling-seed4",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed4.pt",
      "kind": "E0",
      "rolling": true,
      "seed": 4,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "fc538e434c04df7ffa91fa9021f9bb64c6006700b95262772b5e139e492a195b"
    },
    {
      "name": "CNN-F-E0-rolling-seed5",
      "checkpoint": "runs/stage21/checkpoints/CNN-F.pt",
      "estimator": "runs/stage21/checkpoints/E0-seed5.pt",
      "kind": "E0",
      "rolling": true,
      "seed": 5,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "6a7edd4aee91e81b7a272c6e9b2a7962e9a000ed44ab7378f478ad6657a38e2f"
    }
  ],
  "rationale_R2": {
    "source": "receipts/acd_stage21_R12_recovery.json",
    "key": "$.confirmatory.R2.interval",
    "point": 0.055956160241874525,
    "original_assigned_n": 200,
    "half_width": 0.06600000000000006,
    "scaled_half_width": 0.02951609730299725,
    "half_point": 0.027978080120937263,
    "scaling": "half_width * sqrt(original_assigned_n / N)"
  },
  "rationale_R5_R6": {
    "source": "receipts/acd_stage20_C.json",
    "sha256": "904e82c54fa906deda1019c549e70845c7b1f10908f53e988b218ea94dfc9d79",
    "scope": "Original confirmation panel; post hoc E0 rolling versus E0 fixed, seven-pattern errors and gate harms."
  },
  "namespaces": {
    "acd-stage22-assign": 17397854698352781238,
    "acd-stage22-instances": 18157603091808822137,
    "acd-stage22-observation": 249933790449627459,
    "acd-stage22-sampler": 10587960102049289933
  },
  "root_disjoint": true,
  "leaves_unique": true,
  "leaf_count": 138001,
  "climatology": {
    "/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy/runs/stage21/climatology/F7.npz": "b4d7510c988ddbec91ead73f1858f83305814882137c715edebb9ccbfb15c771",
    "/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy/runs/stage21/climatology/F9.npz": "ef1ac19354975d6e1f5132f219bac9ceb0d7f0a34188a4163461f700d3ea57f6"
  },
  "freeze_e_hashes": {
    "acd_stage21_freeze_e.py": "a1bb9d0f5d693b1132945c4ad650ac703f884fd3e6ba02c93692af507d43948c",
    "acd_stage21_inference.py": "94204cd91fd47759ffb21d6837d57ba2fcc4e7eb2a6697e52c828516246f2705",
    "acd_stage21_score.py": "c5a2b073fed700672e7c2aa3cd18156ee1ec3581f3bd7e0d982305a94561f13b",
    "acd_stage21_continue.py": "6822965dcf29ebad3a0b6b2c7a7c8fb0c9bdd1162fbf440887d8e925a46607cf",
    "acd_stage9_cnn.py": "3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434",
    "acd_stage9_train.py": "9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269",
    "acd_stage18_inference.py": "a6ea2847438a23a3290fa12c91535423413f31e8f3b3bd578d93735fa4a0fcb7",
    "acd_stage18_estimators.py": "3e3d00143ecd874a3680378870683c0ccc875c3badbb098202b222de05eee4bc",
    "acd_stage19_learned.py": "9319e768f5d211472d6c52fe0b7c4cef975d878be242b14807a43178e7e85930",
    "acd_stage19_l3_statistic.py": "72da9641cfa8341a50b85514e42f0f15be1e5886e79348c9870c345cee5ce33b",
    "acd_stage19_part3b_score.py": "2d4f05bb0fe22375819af70519aef28d4f21eefcbe0eb434295a9e929ba853d6",
    "acd_stage6_analysis.py": "c9fa8c1f9e211f8e7ea47ec63947bff3693258c738c377ce7874b425bba58cd8",
    "acd_stage13_analysis.py": "ffe50e4894aa97eb6de690abc996c1a8589ec8be926af0100f077b2220be289b",
    "acd_stats.py": "1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a",
    "acd_protocol.py": "160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000"
  },
  "parameterization": {
    "adapter_sha256": "5febec5bf6abfb304bc75ea8de8543e60a867c93af67f9dfe9220df86712f98b",
    "modules": [
      {
        "path": "stage22_parameterized/acd_stage21_contract.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage21_contract.py",
        "baseline_sha256": "b483029f3b7ac4990e496c143de5dc1d5c8ca5d719722e7198873608e0b9ace3",
        "sha256": "8abc7692b321bec07796e7828cbd95b0f3b2dbdc299cc8fa1e35ddc491a8f7ff",
        "changed_lines": [
          16,
          58
        ],
        "remaining_literal_200": []
      },
      {
        "path": "stage22_parameterized/acd_stage21_inference.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage21_inference.py",
        "baseline_sha256": "94204cd91fd47759ffb21d6837d57ba2fcc4e7eb2a6697e52c828516246f2705",
        "sha256": "e31de05e4ad497eedbaea58677c1450bbbaad2eba7c7880e62fcccb21cb6bf79",
        "changed_lines": [
          15,
          25,
          36
        ],
        "remaining_literal_200": []
      },
      {
        "path": "stage22_parameterized/acd_stage21_score.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage21_score.py",
        "baseline_sha256": "c5a2b073fed700672e7c2aa3cd18156ee1ec3581f3bd7e0d982305a94561f13b",
        "sha256": "f99dc69e6bcc9a0ce986361640a531e0e9b7662840e1aa30c55a509cb7af8cba",
        "changed_lines": [
          62
        ],
        "remaining_literal_200": []
      },
      {
        "path": "stage22_parameterized/acd_stage19_part3b_score.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage19_part3b_score.py",
        "baseline_sha256": "2d4f05bb0fe22375819af70519aef28d4f21eefcbe0eb434295a9e929ba853d6",
        "sha256": "9d097f5e333a19a8d51613ab43e49df83dcb2dd74a6dc853352e9751e945c29b",
        "changed_lines": [
          41
        ],
        "remaining_literal_200": []
      },
      {
        "path": "stage22_parameterized/acd_stage21_part1.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage21_part1.py",
        "baseline_sha256": "758635e34729ef217fa3223080b9ea7193762fe0acbed61a80e3264a383c51cf",
        "sha256": "8d9b07fa86716f27c5425ec57d166335da56d59efde4b8cee21008822816d29d",
        "changed_lines": [
          141,
          149
        ],
        "remaining_literal_200": [
          {
            "line": 85,
            "text": "    theta,sreport=posterior.sample(y,fit['starts'],'r3',c,.01,sub=attempt,warmup=1000 if attempt==0 else 2000,draws=500)"
          }
        ]
      },
      {
        "path": "stage22_parameterized/acd_stage19_learned.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage19_learned.py",
        "baseline_sha256": "9319e768f5d211472d6c52fe0b7c4cef975d878be242b14807a43178e7e85930",
        "sha256": "c3485f3db7d92b6f8ed2fd055ab0b04fe945fd3e9331c9cf9ec2a77c1e6119fd",
        "changed_lines": [
          23,
          25
        ],
        "remaining_literal_200": []
      },
      {
        "path": "stage22_parameterized/acd_stage9_cnn.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage9_cnn.py",
        "baseline_sha256": "3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434",
        "sha256": "297635929df3f4f09c5d667d90cc4d8efa8f3d82ccd836f183332e8d643c097b",
        "changed_lines": [
          28
        ],
        "remaining_literal_200": []
      },
      {
        "path": "stage22_parameterized/acd_stage18_inference.py",
        "baseline_path": "/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy/acd_stage18_inference.py",
        "baseline_sha256": "a6ea2847438a23a3290fa12c91535423413f31e8f3b3bd578d93735fa4a0fcb7",
        "sha256": "d6cb0ab577f1aeba3568a64e5febd1c3d3d9fbbe420a4eefecdceb1b626b0704",
        "changed_lines": [
          35
        ],
        "remaining_literal_200": []
      }
    ],
    "criteria": "unchanged",
    "change_scope": "Assigned case count; balanced half-count derives as N//2. No statistic or rollout change."
  },
  "reproduction": [
    {
      "receipt": "/home/todd/work/aspen-stage22-prerequisites-20261010/expected/acd_stage21_R12_recovery.json",
      "sha256": "d268819d30b774450a2ba516f6320fcd78956ecfe144b72496ad63c19fa38bdf",
      "different_values": 0,
      "N": 200,
      "exact": true
    },
    {
      "receipt": "/home/todd/work/aspen-stage22-prerequisites-20261010/expected/acd_stage21_R34.json",
      "sha256": "5499288b63ed14def18c4206c9a084ccaebd635ff5ee4b353b2d95824d3f2877",
      "different_values": 0,
      "N": 200,
      "exact": true
    },
    {
      "receipt": "/home/todd/work/aspen-stage22-prerequisites-20261010/expected/acd_stage21_descriptive.json",
      "sha256": "7241c5874fa0bb60e3aee4d2742a61f84d29b2891b617a6c3b652ee0d2f536e3",
      "different_values": 0,
      "N": 200,
      "exact": true
    }
  ],
  "new_code_hashes": {
    "acd_stage22_adapter.py": "5febec5bf6abfb304bc75ea8de8543e60a867c93af67f9dfe9220df86712f98b",
    "acd_stage22_R56.py": "b133e613dde2680aa410f18b3bf55bed8260b8294879a41d552d501083d79e7e",
    "acd_stage22_freeze.py": "4fc7ce079c27440e81607bf7665e36551f2e681366bd0afeb801dcfe08b71c2d"
  },
  "criterion_changes": [],
  "hardware": "Baccus 170HX for all compared inference; sulaco CPU for sampling and scoring",
  "resolutions": [
    {
      "rule": "R-other",
      "detail": "Case count N supplied by Stage22 adapter; count-only source changes beyond panel path, criteria unchanged. Same adapter applies to Stage23 scoring on this panel."
    }
  ]
}
```

## Line-level count diff

```diff
--- FreezeE/acd_stage21_contract.py
+++ Stage22/acd_stage21_contract.py
@@ -13,7 +13,7 @@
 def rng(name,sub=0,case=0,member=0,action=0):
  return np.random.default_rng(np.random.SeedSequence([IDS[name],0,sub,case,member,action]))
 def assignments():
- return rng(NAMES[0]).permutation(np.repeat([7.,9.],100))
+ return rng(NAMES[0]).permutation(np.repeat([7.,9.],N//2))
 def configure():
  # Adapter globals implement Todd's explicit Stage21 sigma without editing inherited files.
  import acd_fits,acd_posterior
@@ -55,7 +55,7 @@
  oldroots=set(protocol.AAH_IDS)|set(protocol.IDS.values())|{int.from_bytes(hashlib.sha256(n.encode()).digest()[:8],'little') for n in oldnames}
  assert not set(IDS.values())&oldroots and len(set(IDS.values()))==len(IDS)
  leaves=[(IDS[NAMES[0]],0,0,0,0,0)]
- for c in range(200):
+ for c in range(N):
   leaves.extend([(IDS[NAMES[1]],0,0,c,0,0),(IDS[NAMES[2]],0,1,c,0,0)])
   leaves.extend((IDS[NAMES[3]],0,0,c,m,0) for m in range(128))
   leaves.extend((IDS[NAMES[3]],0,s,c,m,0) for s in [1,2] for m in range(4))
--- FreezeE/acd_stage21_inference.py
+++ Stage22/acd_stage21_inference.py
@@ -12,7 +12,7 @@
  d=ready();target=OUT/'inference_inputs';target.mkdir(exist_ok=True)
  settings=dict(sigma=float(SIGMA),patterns=PATTERNS.tolist(),windows=[w.tolist() for w in WINDOWS])
  (target/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
- for c in range(200):
+ for c in range(N):
   output=target/f'{c:03d}.npz';source=OUT/f'main_forecast_{c:03d}.npz'
   if not output.exists():
    with np.load(source) as z:theta=z['theta'].copy()
@@ -22,7 +22,7 @@
  for arm in ['meanF','constantF']:
   folder=OUT/'A_inputs'/arm;folder.mkdir(parents=True,exist_ok=True)
   (folder/'settings.json').write_bytes((target/'settings.json').read_bytes())
-  for c in range(200):
+  for c in range(N):
    output=folder/f'{c:03d}.npz'
    if output.exists():continue
    with np.load(target/f'{c:03d}.npz') as z:h,f=z['H'].copy(),z['F'].copy()
@@ -33,7 +33,7 @@
  folder=OUT/'inference'/name
  if not (folder/'complete.json').exists():return False
  d=json.loads((folder/'complete.json').read_text());hashes=json.loads((folder/'hashes.json').read_text())
- return d['cases']==200 and len(hashes)==200 and all(digest(folder/p)==h for p,h in hashes.items())
+ return d['cases']==N and len(hashes)==N and all(digest(folder/p)==h for p,h in hashes.items())
 
 def worker(name):
  d=ready();r=next(x for x in d['tasks'] if x['name']==name)
--- FreezeE/acd_stage21_score.py
+++ Stage22/acd_stage21_score.py
@@ -59,7 +59,7 @@
  for f in [7,9]:
   with np.load(OUT/'climatology'/f'F{f}.npz') as z:
    j=z['J'].copy();climates[f]=dict(jbar=float(z['jbar']),null=z['prob'].copy(),sd=(j[:,:8]-j[:,8,None]).std(0,ddof=1),mean=z['states'].mean(0))
- for c in range(200):
+ for c in range(N):
   with np.load(OUT/f'main_forecast_{c:03d}.npz') as z:
    physical.append(z['J'].copy());posterior_means.append(z['factual_mean'].copy());keep.append(not bool(z['excluded']));post_f.append(z['theta'][:,40].copy());fstdev.append(float(post_f[-1].std(ddof=1)))
  keep=np.array(keep);summaries={};results={};missing=[]
--- FreezeE/acd_stage19_part3b_score.py
+++ Stage22/acd_stage19_part3b_score.py
@@ -38,7 +38,7 @@
 
 def forcing_error(name):
     values = []
-    for case in range(200):
+    for case in range(N):
         with np.load(OUT/'inference'/name/f'{case:03d}.npz') as data:
             if 'estimated_F_at_cutoff' not in data:
                 return None
--- FreezeE/acd_stage21_part1.py
+++ Stage22/acd_stage21_part1.py
@@ -138,7 +138,7 @@
  prior=[json.loads(p.read_text()) for p in (Path(os.environ['ACD_STAGE21_PRIOR_CONF'])).glob('case_*.json')]
  retry=sum(r['diagnostics'].get('attempt',0)>0 for r in prior)/len(prior)
  full=sum(r['diagnostics'].get('full_forecast',False) for r in prior)/len(prior)
- mean=float(np.mean([r['seconds'] for r in rows]));projected=200*mean/len(groups)*(1+retry+full)
+ mean=float(np.mean([r['seconds'] for r in rows]));projected=N*mean/len(groups)*(1+retry+full)
  projection=dict(seconds=projected,hours=projected/3600,limit_hours=24,workers=len(groups),cores_per_worker=len(groups[0]),reserved_cpus=reserved,pilot_wall_seconds=time.monotonic()-started,pilot_mean_seconds=mean,prior_retry_rate=retry,prior_rescore_rate=full,component_seconds={a:{k:float(np.mean([r['arms'][a][k] for r in rows])) for k in ['fit_seconds','forecast_seconds']} for a in ['main']},passed=bool(projected<=24*3600))
  summarize('timing_passed' if projection['passed'] else 'timing_gate_stopped',projection)
  from acd_stage21_publish import publish
@@ -146,7 +146,7 @@
  if not projection['passed']:return
  # One persistent worker per affinity group avoids overlap as case durations vary.
  def queue(index):
-  for c in range(5+index,200,len(groups)):job(c,groups[index]);summarize('blind_sampling_running',projection)
+  for c in range(5+index,N,len(groups)):job(c,groups[index]);summarize('blind_sampling_running',projection)
  with concurrent.futures.ThreadPoolExecutor(max_workers=len(groups)) as pool:list(pool.map(queue,range(len(groups))))
  result=summarize('blind_sampling_complete',projection);result['wall_seconds']=time.monotonic()-started;write(RECEIPT,result)
  publish('panel')
--- FreezeE/acd_stage19_learned.py
+++ Stage22/acd_stage19_learned.py
@@ -20,9 +20,9 @@
     directory = OUT / 'inference' / name
     if name != 'posterior':
         execution = json.loads((directory / 'complete.json').read_text())
-        if execution['cases'] != 200:
+        if execution['cases'] != N:
             raise RuntimeError('Model inference incomplete')
-    for case in range(200):
+    for case in range(N):
         with np.load(OUT / f'main_forecast_{case:03d}.npz') as data:
             physical = data['J'].copy()
             mean = data['factual_mean'].copy()
--- FreezeE/acd_stage9_cnn.py
+++ Stage22/acd_stage9_cnn.py
@@ -25,7 +25,7 @@
  ck=torch.load(checkpoint,map_location='cpu',weights_only=True);conditioned=name.startswith('CNN-F');cost=name=='CNN-cost'
  model=ForcingModel() if conditioned else CostModel() if cost else Emulator()
  model.load_state_dict(ck['state_dict']);model.cuda().eval();out.mkdir(parents=True,exist_ok=True)
- for c in range(200):
+ for c in range(N):
   target=out/f'{c:03d}.npz'
   if target.exists():continue
   start=time.monotonic()
--- FreezeE/acd_stage18_inference.py
+++ Stage22/acd_stage18_inference.py
@@ -32,7 +32,7 @@
         target = OUT/'A_inputs'/arm
         target.mkdir(parents=True, exist_ok=True)
         (target/'settings.json').write_bytes((source/'settings.json').read_bytes())
-        for case in range(200):
+        for case in range(N):
             path = target/f'{case:03d}.npz'
             if path.exists():
                 continue
```
