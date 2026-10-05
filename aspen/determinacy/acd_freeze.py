"""Record the pre-confirmation contract using Stage 1 receipts only.

Uses the standard library; does not import scientific modules or access runs.
Confirmation adapters must be recorded before any confirmation data is generated.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    target = ROOT / 'ACD_FREEZE.md'
    if target.exists():
        raise SystemExit('Freeze already exists; preserve the original record.')
    stage1 = json.loads((ROOT / 'receipts/acd_stage1.json').read_text())
    numerical = json.loads((ROOT / 'receipts/acd_numerical.json').read_text())
    artifacts = json.loads((ROOT / 'ACD_ARTIFACTS.json').read_text())
    step0 = json.loads((ROOT / 'receipts/acd_step0.json').read_text())
    expected = dict(dt=.01, warmup=1000, draws=500, r5_population=60,
                    cuts=['R7', 'R5-A', 'R6-3LT', 'RML-conf',
                          'P/B-other-leads', 'R5-3LT'])
    assert stage1['settings'] == numerical['settings'] == expected
    for name, sha in stage1['source_hashes'].items():
        assert digest(ROOT / name) == sha, f'Stage 1 source changed: {name}'
    assert numerical['seeds'] == artifacts['seed_leaves'] == step0['seed_leaves']
    null_files = [row for row in artifacts['manifest']
                  if row['path'].startswith('runs/null/')]
    null_receipt = json.loads((ROOT / 'receipts/null.json').read_text())
    assert next(row['sha256'] for row in null_files
                if row['path'].endswith('.npz')) == null_receipt['sha256']
    assert stage1['null']['jbar'] == null_receipt['jbar']
    wo = (ROOT / 'sources/WO_v2.3.md').read_text()
    references = wo[wo.index('## 10. Readings and statistics'):
                    wo.index('## 12. Two-sided feasibility')]
    base = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    names = [*sorted(p.name for p in ROOT.glob('*.py')),
             'requirements-cpu.lock', 'CODEX_SELECTOR.md',
             'ACD_STAGE1_READING.md', 'ACD_SPEC_GATE.md', 'ACD_STATS_AUDIT.md',
             'ACD_STATS_AUDIT_v2.3.json', 'ACD_ARTIFACTS.json',
             'receipts/acd_stage1.json', 'receipts/acd_numerical.json',
             'receipts/acd_step0.json', 'receipts/null.json', 'sources/WO_v2.3.md']
    record = dict(version='2.3', stage1_commit=base,
                  settings=expected, seeds=numerical['seeds'],
                  hashes={name: digest(ROOT / name) for name in names},
                  inherited=artifacts['inherited'],
                  checkpoint=step0['hashes']['inputs/CNN-20k.pt'],
                  null_raw_manifest=null_files, null_outputs=stage1['null'],
                  stage1_resolutions=stage1['resolutions'],
                  confirmation_cases=list(range(200)),
                  confirmation_namespace='acd-observation-conf',
                  stage2_adapters_recorded=False)
    snapshot = ROOT / 'receipts/acd_freeze.json'
    snapshot.write_text(json.dumps(record, indent=2) + '\n')
    table = '\n'.join(f'| `{name}` | `{sha}` |'
                      for name, sha in record['hashes'].items())
    inherited = '\n'.join(f'| `{name}` | `{sha}` |'
                          for name, sha in record['inherited'].items())
    target.write_text(f'''# Aspen counterfactual determinacy — pre-confirmation freeze (v2.3)

Todd authorized freeze and Stage 2 confirmation on 2026-10-05. This record uses
only the committed development reports and receipts at `{base}`. Step 0b remains
at `eb87279` and is not rerun. No confirmation data was generated or accessed in
preparing this record.

## Execution status

The scientific contract below is recorded before confirmation. Execution is
blocked in the current session: sulaco SSH sockets and the Obsidian connector are
unavailable. The freeze must be pushed before confirmation, as Todd requested.
The existing Stage 1 modules still disable confirmation and do not implement the
CNN runner. Before generating any confirmation observations, implement and check
the confirmation adapters without confirmation data, and commit and push a code
hash addendum. It must retain this scientific contract and record any §14
resolution, including the fit-order resolution needed by the RML-conf cut.
No confirmation execution is licensed by an unrecorded adapter.

## Stage 1 compute settings retained for confirmation

```json
{json.dumps(expected, indent=2)}
```

Posterior, fitting and integration run on sulaco CPU only, with float64,
`JAX_PLATFORMS=cpu` and `jax_enable_x64=True`. NumPyro 0.22.0, JAX 0.11.2;
the complete environment is hashed in `requirements-cpu.lock`. NUTS has dense
mass adaptation, target acceptance 0.9 and four vectorized chains. Production
warmup is 1000 and post-warmup draws are 500 per chain. Keep indices
floor(i*500/128), i=0..127, per chain: 512 forecast draws. The prescribed
functional-diagnostic fallback uses all 2000 post-warmup draws, then one retry
with warmup 2000 and 500 draws per chain. These are diagnostic rules, not
discretionary compute changes. Split R-hat <=1.01, bulk ESS >=400, divergence
share <=0.01 apply to parameters/log likelihood and required gate functionals.
Threshold-uncertain probabilities retain their point classification.

The fixed cuts, in original order, are R7, R5-A, R6-3LT, RML-conf,
P/B-other-leads and R5-3LT. There is no confirmation RML smoother or R3b reading,
no all-site ceiling, and no 3 LT R5/CNN comparison. RML perturbation seeds remain
available for the CNN input ensemble. R5 uses the first 60 qualifying cases by
case index at 2 LT, one common denominator for Q/F/V/R, including unresolved
refits; fewer than 40 is NOT EVALUABLE. Existing failed-refit retry and coverage
rules remain in force. Production warmup/draws apply to refits too.

Initial serial projection was 104977.9093867197 seconds; after cuts and the
population reduction it was 56050.68403900741 seconds before draw reduction.
R-time permits continuation with these final settings. Case parallelism may
change scheduling, never seed assignment, population order or inference rules.

CNN-20k runs on sulaco GPU for inference only, 128 perturbed windows with the
same perturbation stream as the omitted RML arm, all eight actions and no action.
R6 is reported at 2 LT. Drop a member for every action if it is invalid under
any action. Encode 11 normalized frames and the action channel as in the
inherited inference implementation. Checkpoint SHA-256:
`{record['checkpoint']}`. Use smaller micro-batches on GPU memory shortage;
if it still cannot fit, record R-gpu and omit R6. Never stop Qwen services.

No training, cloud execution or changes to the Baccus close-out are authorized.

## Panel and blind order

Confirmation is 200 cases, indices 0–199, generated by
`physics.history("acd-observation-conf", case, 0.01)` with the inherited
observation/action/cost/window definitions. Observed arrays alone reach samplers
and targeting through the logged observation loader. Store truth separately.
For each case: write and hash observations; write and hash posterior outputs,
crude outputs and CNN outputs (or a recorded R-gpu omission); only then compute
and save realized outcomes. RML is absent under the frozen cut. Scoring and
coverage are the permitted truth readers; measurement code may form the designed
probe z, while selection uses posterior draws alone. Maintain hash/order receipts.
R5 chooses sites using the pre-probe posterior, shares the same 40-site probe
noise across arms and retains the designated action pair through all refits.

## ACD_IDS and sub roles

```json
{json.dumps(numerical['seeds'], indent=2)}
```

Inherited history sub 0 initializes the state, sub 1 adds noise. Sampler/crude
member is the ensemble index; posterior member is the chain index. Measurement
and refit action is the index of the lead in LEADS (2 LT is index 3). Refit arm
indices Q/F/V/R/A are 0/1/2/3/4, hence primary sub 10+arm and retry sub 20+arm.
Bootstrap subs have the roles above. Preserve the 147564-leaf disjointness check
and inherited-ID non-overlap; update only the in-memory protocol ID registry.

## Frozen null outputs

The 4096 independently seeded climatological states use the true F=8 and the
existing dt=0.01 forecasts. Jbar is `{stage1['null']['jbar']}`.
Fc-above shares in lead order [0,1,1.5,2,2.5,3,4,6] are
`{stage1['null']['Fc_above_shares']}`.
Every per-question/action/pair/lead modal probability is copied unchanged into
`receipts/acd_freeze.json` under `null_outputs`; retain the existing raw null,
with no recomputation using confirmation information.

```json
{json.dumps(null_files, indent=2)}
```

## Code, input-contract and report hashes

Stage 1 reading SHA-256: `{record['hashes']['ACD_STAGE1_READING.md']}`.
The code below is the verified Stage 1 baseline; the execution-status addendum
requirement applies to confirmation adapters. SHA-256 throughout.

| File | SHA-256 |
|---|---|
{table}

Inherited source hashes (recorded on sulaco during Step 0):

| File | SHA-256 |
|---|---|
{inherited}

Snapshot SHA-256: `{digest(snapshot)}`. It includes all null probabilities,
settings, seeds and carried-forward resolution details.

## Resolution rules and decision contract

Carried forward: **R-time**, with the fixed cuts/settings above; **R-rml**, with
development disagreements recorded as approximate cross-check diagnostics;
**R-other**, with literal climate classification rather than a proven confidence
ordering, L6 restricted to tested Q/F/V/R arms, and measured Wilks coverage
reported as approximate. These findings do not authorize stronger claims.
No new numerical fallback or GPU-memory resolution has fired in this session.
Infrastructure blocking is not a scientific H1–H3 result.

H1 prohibits truth leakage into inference/selection/null; H2 prohibits
confirmation before the committed freeze; H3 prohibits unauthorized actions.
The additional user requirement is to push the freeze before confirmation.
All §14 resolution rules remain in force and must be reported if triggered.

The following §10/§11 text is copied verbatim from the hashed v2.3 source.
Its thresholds, statistics, prerequisites and licensed language are frozen.
RML-conf, R5-A, R6-3LT and R5-3LT references are governed by the cuts above:
omitted readings are explicitly marked not run, and supply no licensed sentence.
The Stage 2 report and vault note must be generated from confirmation numbers
only; the claim ledger must show which L1–L10 conditions are met.

{references}
''')
    print('Wrote ACD_FREEZE.md and receipts/acd_freeze.json from Stage 1 only.')


if __name__ == '__main__':
    main()
