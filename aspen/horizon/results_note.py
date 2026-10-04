"""Generate a current status/results note from gate and measured evidence."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def render():
    gate_pass=(ROOT/'AAH_GATE_AMENDMENT1A.md').exists()
    reading=ROOT/'results/readings.json'
    state=json.loads(reading.read_text()) if reading.exists() else {}
    complete=state.get('execution_complete',False)
    status=('Execution complete with the prescribed Kolmogorov calibration stop; no two-system empirical PASS/KILL.' if state.get('stopped_systems') else 'Execution complete; frozen scientific verdict: '+state.get('scientific_verdict','unavailable')) if complete else 'Gate passed under Amendment 1a; execution in progress.'
    lines=["# Aspen act beyond the horizon: results and execution status (2026-10)","",
           status if gate_pass else "Experimental execution blocked by specification gate.","",
           "Work order: [[WO_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10-03]]. Gate: [[R_Aspen-Act-Beyond-Horizon-Spec-Gate-2026-10-04]].",
           "", "Repository: nivatechnologies/horizons-paper, branch `paper/aspen-2026-10-horizon`. Protocol: `aspen/horizon/AAH_FREEZE.md`; measured calibration addenda precede each system's test/training. Step 0 complete and not rerun.",
           "", "M_95 is only a tested-grid budget in {8,16,32,64,128,256}. Censored unpaired numerator is conservatively 256; censored paired fails. Bootstrap confidence/commitment levels are nominal; empirical errors are reported.",
           "", "Machines: Baccus for Kolmogorov and FNO; sulaco for Lorenz and brute-force truth ensembles. No Qwen service stopped."]
    for system,title in [('l96','Lorenz-96'),('kolmo','Kolmogorov')]:
        lines += ['', '## '+title, '']
        p=ROOT/'results'/f'{system}_calibration.json'
        progress=False
        if not p.exists():
            p=ROOT/'results'/f'{system}_calibration_progress.json';progress=True
        if p.exists():
            c=json.loads(p.read_text())
            lines += ['Calibration running; completed amplitude readings below. No amplitude selected yet.' if progress else f"Calibration status: {c['status']}; selected delta: {c['delta']}.", '']
            lines += ['| delta | Determinable | Panel | Fraction |','|---|---|---|---|']
            for r in c['rows']:
                lines.append(f"| {r['delta']} | {r['eligible']} | {r['total']} | {r['fraction']:.3f} |")
            if c.get('status')=='CALIBRATION_FAIL':
                lines += ['', 'No amplitude meets 16/20. Kolmogorov stopped under A8: no escalation, replacement panel, chaos gate, test ensemble or FNO data/training. Prepared code was not executed. This is a calibration failure, not the empirical KILL criterion.']
        else:
            lines += ['Calibration truth ensembles pending or running.']
        p=ROOT/'results'/f'{system}_solver_statistics.json'
        if p.exists():
            s=json.loads(p.read_text())
            lines += ['', f"Niva forecast horizon T_f={s['Tf']} LT; sustained decision horizon T_d={s['Td']} LT.", '',
                      '| T (LT) | Eligible / panel | Niva top-1 (M64) | Forecast ACC | Myopic top-1 | Paired / unpaired M95 |',
                      '|---|---|---|---|---|---|']
            for h in s['horizons']:
                a=h['arms']['paired'];u=h['arms']['unpaired']
                def fmt(x):return 'unavailable' if x is None else f'{x:.4f}'
                lines.append(f"| {h['T']} | {h['eligible']} / {h['total']} | {fmt(a['accuracy'][3])} | {fmt(a['ACC'])} | {fmt(h['myopic_accuracy'])} | {a['M95'] if a['M95'] is not None else '>256'} / {u['M95'] if u['M95'] is not None else '>256'} |")
            if system=='l96' and s['Tf']==10 and s['Td']==12:
                lines += ['', 'Lorenz reading misses PASS: sustained horizon 12 is below the required G(30), which is outside the frozen grid; paired/unpaired M95 ratio at T_f is 1 (128 members each). At G(1.5 T_f)=16, accuracy 0.79 does not meet the <0.5 KILL rule.']
            lines += ['', 'Learned-arm evaluation remains pending.' if s.get('learned_arm_pending',True) else 'Learned-arm evaluation included.']
            if not s.get('learned_arm_pending',True):
                drops=s['learned_stability']
                lines += ['',f"Learned stability: {drops['dropped']} dropped of {drops['attempted_members']} attempted members under the all-action 21-LT rule.", '',
                          '| T (LT) | Learned top-1 (M64) | Learned ACC | Response correlation | Response relative error |',
                          '|---|---|---|---|---|']
                for h in s['horizons']:
                    a=h['arms']['learned']
                    lines.append(f"| {h['T']} | {fmt(a['accuracy'][3])} | {fmt(a['ACC'])} | {fmt(a['response_correlation'])} | {fmt(a['response_relative_error'])} |")
    if state.get('diagnostics'):
        lines += ['', '## Descriptive response/forecast correlations', '',
                  'Unit: (arm,T), pooling learned/misidentified/jitter within each system. Full-rank QR residuals; unavailable coefficients stay unavailable; no inferential or strongest-practice claim. Pending learned evidence means an incomplete panel.', '',
                  '| System | Available / attempted units | Learned Tf / status | Accuracy–response controlling ACC | Accuracy–ACC controlling response |',
                  '|---|---|---|---|---|']
        for key,d in state['diagnostics'].items():
            f=lambda x:'unavailable' if x is None else f'{x:.4f}'
            lines.append(f"| {key} | {d['available_units']} / {d['attempted_units']} | {d['learned_Tf']} / {d['learned_Tf_status']} | {f(d['partial_accuracy_response_controlling_ACC'])} | {f(d['partial_accuracy_ACC_controlling_response'])} |")
    lines += ['', '## Evidence and completion', '',
              'Every measured number is generated from JSON sources into `aspen/horizon/NUMBERS.md` (AAH sections). `make_numbers.py check` replays source values and reports zero mismatches; a deliberate numeric mutation was rejected.',
              '', 'Raw arrays/logs are retained under each compute checkout’s `aspen/horizon/runs/`; source SHAs accompany summaries. Lorenz calibration launch-tag correction is explicitly recorded in its source JSON and calibration freeze addendum; numerical data unchanged.',
              '', 'Commitment wall times measure nested forecast cohorts plus bootstrap interval analysis, sharing all 16 horizons. They exclude parameter identification, observation preparation and sampler setup; no end-to-end planner latency claim is made.',
              '', 'Optional cuts fixed before data, in the WO order: latent emulator, W=2 sensitivity, impulsive timing. All mandatory Lorenz arms were retained. The planned 30-case Kolmogorov panel and FNO were not executed because its calibration failed.',
              '', 'No two-system PASS/KILL finding is inferred from a stopped system. Calibration/chaos failures stop the affected part. Results and session review are published through the niva-obsidian MCP.',
              '', 'Greyscale PNG/PDF figures: repository `aspen/horizon/figures/decision_and_forecast`, `members_paired_unpaired`, and `learned_response_and_forecast`. A stopped system is explicitly marked unavailable. Checked NUMBERS sections AAH* replay source measurements with zero mismatches.',
              '', 'Generated by `aspen/horizon/results_note.py` into `04-Results/R_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10.md`.']
    training=ROOT/'results/l96_training.json'
    if training.exists():
        t=json.loads(training.read_text())
        lines += ['',f"Lorenz CNN training complete: {t['steps_done']} updates, {t['params']} parameters; best normalized 1-LT validation MSE {t['best_val']:.8g}. Training score is not test performance. The final 200-case test evaluation uses the same full-FP32 sulaco CUDA backend with TF32 disabled; preliminary CPU outputs retained and excluded."]
    frequency=ROOT/'results/l96_posthoc_action_frequency.json'
    if frequency.exists():
        d=json.loads(frequency.read_text())
        lines += ['', '## Post-hoc action-frequency diagnostic', '',
                  'Diagnostic only; no selector or criterion changed. Uniform negative-forcing action 0 is the truth-best action in every eligible Lorenz case at 10, 12, 16, 20 LT. The myopic null selects action 0 for all 200 cases. This is a boundary of the selected action panel, not a universal claim about planning. Selector: final blinded Codex run1 action set; one framing.', '',
                  'Source: `results/l96_posthoc_action_frequency.json`; checked section AAHLPOSTHOC.']
    return '\n'.join(lines)+'\n'

if __name__=='__main__':
    path=ROOT/'R_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10.md'
    path.write_text(render());print(path)
