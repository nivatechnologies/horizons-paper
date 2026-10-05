# Aspen counterfactual determinacy

The v2.3 run ends at the Stage 1 development gate. Step 0b is preserved at
`eb87279`; a freeze, confirmation, training and CNN inference are outside this run.

All numerical work runs on sulaco CPU in the isolated virtual environment
`/home/todd/work/aspen-determinacy-20261005/.venv`. `requirements-cpu.lock` records
installed packages. JAX uses CPU and float64. The remote code/output root is
`/home/todd/work/aspen-determinacy-20261005/aspen/determinacy`.

Only unchanged `protocol.py` and `physics.py` are imported from the inherited
forecast-decision checkout (default `/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision`).
An alternative source location can be set with `ACD_INHERITED_ROOT`. Step0 and
artifact receipts record source/input/checkpoint hashes. `extras.py` and
`campaign.py` are inspected, never imported or edited. The Baccus close-out is
outside this worktree and is untouched.

Run from this directory, with the ACD virtual environment active. Use CPU affinity
and `OPENBLAS_NUM_THREADS=1`, `PYTHONDONTWRITEBYTECODE=1`; set
`NUMBA_NUM_THREADS` to the affinity's CPU count. The implemented sequence is:

```
python acd_stats_audit.py
python acd_step0.py
python acd_campaign.py stage0
python acd_campaign.py stage1a
python acd_campaign.py stage1b
python acd_render.py
python check_acd.py
```

The spec gate is written before Step0. The statistical audit is synthetic only.
`stage0` records settings and resolution rules. Ordinary cases can be scheduled
in independent processes with `acd_campaign.py batch --panel dev --cases 0,1,2`.
Run the first20 before Stage1a validation; finish any Stage1a reruns before the
remaining panel. Resuming keeps the designated Stage1a rerun, while a benchmark
case at the old draw count is resampled at production settings.

Optional execution parallelism for Stage1b uses `acd_measure.py --worker i
--workers N`. Arms have deterministic, nonoverlapping process assignments. Its
population uses a contiguous completed prefix, so unfinished lower indices are
never skipped. After all ordinary processes finish successfully, write the owned
marker `runs/ordinary_complete`; measurement workers finish the exact common
population. `stage1b` then verifies/reuses existing runs and generates the reading
and vault note from the saved data. This scheduling changes no seed, threshold,
fit order or population.

Raw arrays stay in ignored `runs/{audit,dtcheck,null,dev}/` on sulaco. Reports and
compact receipts are committed; `ACD_ARTIFACTS.json` inventories raw file hashes.
Sampler archives contain only observation-derived quantities. The observation
loader logs every input read. Truth scoring stays in `acd_questions.py` and
`acd_analysis.py`; `acd_measure.py` reads truth only to form the designed probe.
No confirmation input path is enabled.

`acd_analysis.py` emits `ACD_STAGE1_READING.md` and
`vault/04-Results/R_Aspen-Counterfactual-Determinacy-Stage1-2026-10.md` from the same
receipt. No publication claim is licensed by development results. Every §14
resolution appears in the Stage1 reading; only H1–H3 halt the run early.
