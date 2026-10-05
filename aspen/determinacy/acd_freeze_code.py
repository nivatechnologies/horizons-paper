"""Commit-ready code addendum, generated before confirmation data access."""
import json,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    p=ROOT/'ACD_FREEZE_CODE.md'
    if p.exists():raise SystemExit('Preserve the original code freeze.')
    original=json.loads((ROOT/'receipts/acd_freeze.json').read_text())
    assert digest(ROOT/'acd_stats.py')==original['hashes']['acd_stats.py']
    assert digest(ROOT/'acd_posterior.py')==original['hashes']['acd_posterior.py']
    assert digest(ROOT/'acd_fits.py')==original['hashes']['acd_fits.py']
    assert digest(ROOT/'acd_mechanism.py')==original['hashes']['acd_mechanism.py']
    assert digest(ROOT/'ACD_STAGE1_READING.md')==original['hashes']['ACD_STAGE1_READING.md']
    files=sorted(v.name for v in ROOT.glob('*.py'))+['ACD_FREEZE.md','receipts/acd_freeze.json','requirements-cpu.lock','requirements-stage2.lock','sources/Ledger_pre_stage2.md']
    record=dict(version='2.3',scientific_freeze_commit='1f38be370718825196ecf4ff1e5e82138faf44c7',
                settings=original['settings'],seeds=original['seeds'],inherited=original['inherited'],
                checkpoint=original['checkpoint'],null_raw_manifest=original['null_raw_manifest'],
                hashes={name:digest(ROOT/name) for name in files},
                resolutions=[dict(rule='R-other',trigger='RML-conf cut removes prescribed fourth MAP and chain initializers',
                    detail='No RML fits on confirmation. Four MAP starts at (y0,Fhat),(y0,6.5),(y0,9.5),(y0,8.0); 8.0 is the prior midpoint. The four fitted states initialize the four chains. Lowest MAP likelihood cost is provisional; final minimum includes every full posterior draw. Same prior, likelihood, optimizer, diagnostics, seeds and thresholds.'),
                    dict(rule='R-other',trigger='Frozen R5-A cut removes all-site licensed-sentence clause',
                    detail='Report Q/F/V/R only; omit the all40 ceiling clause and RML sentence. No value is imputed for a cut arm.')])
    receipt=ROOT/'receipts/acd_freeze_code.json';receipt.write_text(json.dumps(record,indent=2)+'\n')
    table='\n'.join(f'| `{name}` | `{sha}` |' for name,sha in record['hashes'].items())
    p.write_text(f'''# ACD execution-code freeze addendum — v2.3 confirmation

Connectivity is restored. The original scientific freeze at `1f38be3` has been
pushed. This addendum records the confirmation adapters before any confirmation
data is generated or accessed. Commit and push this addendum before execution.
The scientific thresholds, seeds, null, priors, likelihood, forecasting kernels
and Stage 1 reading are unchanged. `acd_stats.py`, `acd_posterior.py`,
`acd_fits.py` and `acd_mechanism.py` match their original frozen hashes exactly.

The sole changes to baseline scientific interfaces are observation-only
confirmation input paths, a separate truth path in permitted scoring/measurement
code, and the confirmation adapters/readings. The CPU JAX environment and the
original CPU package lock are retained; the GPU inference package additions are
recorded separately in `requirements-stage2.lock`.

## Pre-data resolutions

'''+ '\n\n'.join(f"**{r['rule']}** — {r['trigger']}: {r['detail']}" for r in record['resolutions'])+f'''

## Execution and blind-order checks

`acd_confirmation.py` verifies every execution hash, inherited source hash,
checkpoint hash, raw-null hash and exact compute setting before generating any
case. A pushed-freeze receipt binds this addendum's committed receipt. Execution
requires sulaco. All inference uses the logged `load_observed` interface.
Truth-bearing histories are saved separately, without exposing them to inference.
Observed windows are generated from the inherited history stream, not from any
outcome. The posterior archive contains no truth/scoring arrays.

For each case, observations, posterior, crude and CNN are written and hashed,
in that order, before realized outcomes. A GPU omission has a hashed R-gpu
receipt before outcomes. CNN predictions use all nine actions, share the RML
perturbation seed, and pair-drop invalid members across all actions through the
2 LT scoring horizon (the last tick in its inherited window). The network and
normalization match the inherited code. CPU JAX cannot preallocate GPU memory.
No service is stopped; CNN tries smaller batches if memory is short.

R5 population is chosen only after the ordinary panel is complete, by case
index from pre-probe posteriors. Failed refits remain in the common denominator.
The refit and measurement kernels are unchanged except for the scoring truth
path. `acd_stage2_check.py` independently checks every blind-order event,
sampler archive/hash, settings, checkpoint, population and refit artifact.

The confirmation analysis preserves the Stage1 R0/R0-F/R1/R1m/R2a/R2b/R2c/R3/R5
calculations, replaces the development STRONG rule with §11 publish/kill/decide,
omits RML and cut P/B leads, and adds R6 at2LT. KILL takes precedence if coverage
is below .85. Every statistical route retains its frozen prerequisites and
count floors. Reports/ledger/vault outputs are generated from the final receipt.

Pre-data checks: Python syntax and whitespace checks; synthetic rendering of
publish/kill/decide and cut-arm suppression; four-MAP initializer smoke check
on development case0 only. No confirmation data was used for these checks.

## Code hashes (SHA-256)

| File | SHA-256 |
|---|---|
{table}

Addendum receipt SHA-256: `{digest(receipt)}`.
''')
    print('Wrote execution-code freeze; confirmation remains unopened.')
if __name__=='__main__':run()
