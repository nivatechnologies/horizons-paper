"""CPU-only response-weight decision extension from saved costs; Stage 13 scoring unchanged."""
import hashlib
import json
from pathlib import Path
import acd_stage13_analysis as scoring

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / 'receipts/acd_stage10b_resp001_decisions.json'
NEW_MODEL = 'CNN-F-resp-0.01'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save_extension(name, result):
    previous = json.loads((ROOT / 'receipts/acd_stage10b_decisions.json').read_text())
    for model, value in previous['models'].items():
        assert result['models'][model] == value, model
    old_pairs = previous['paired_comparisons']
    reproduced = [row for row in result['paired_comparisons'] if row['model'] != NEW_MODEL]
    assert reproduced == old_pairs
    result['stage10b_reproduction'] = dict(exact=True, models=len(previous['models']), paired_rows=len(old_pairs))
    paths = [Path(scoring.__file__), ROOT / 'receipts/acd_stage10b_decisions.json',
             ROOT / 'runs/stage9/inference/CNN-F-resp-0.01/complete.json',
             ROOT / 'runs/stage4b_null/null_0.16.npz', Path(__file__)]
    paths += sorted((ROOT / 'runs/stage9/inference/CNN-F-resp-0.01').glob('[0-9][0-9][0-9].npz'))
    result['source_hashes'] = {str(path.relative_to(ROOT)):digest(path) for path in paths}
    RECEIPT.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    render(result)

def render(result):
    lines = ['# Response-weight decisions from saved costs', '',
             'Post hoc on the confirmation panel; licenses no frozen route. CPU-only scoring reuses the Stage 13 policies, climatological margins, exclusions and paired tests. Positive regret differences mean greater regret than the posterior. Bootstrap intervals are descriptive.', '',
             'Every prior Stage 10b model reading and paired comparison reproduced exactly.', '',
             '| Model | Lead (LT) | Policy | Improvement | Regret | Capture | Acting | Harms | Median harm | Largest harm | Zero-harm upper bound | Chosen-action histogram |',
             '|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    def fmt(value):
        return '—' if value is None else format(value, '.8g')
    for model, data in result['models'].items():
        for row in data['readings']:
            fields = [model,fmt(row['lead']),row['policy']] + [fmt(row[k]) for k in ['mean_improvement','mean_regret','capture_fraction','acting_share','harms','median_harm','max_harm','zero_harm_CP_upper']] + [str(row['chosen_actions'])]
            lines.append('| ' + ' | '.join(fields) + ' |')
    lines += ['', 'Histograms follow the frozen pattern order, ending with no action. Zero-harm bounds are one-sided Clopper–Pearson bounds using the Stage 13 confidence level.', '',
              '| Lead (LT) | Policy | Different choices | Regret difference | Descriptive bootstrap interval | Exact sign p | Posterior-only harms | CNN-F-resp-0.01-only harms | Exact McNemar p |',
              '|---:|---|---:|---:|---|---:|---:|---:|---:|']
    for row in result['paired_comparisons']:
        if row['model'] == NEW_MODEL:
            values = [fmt(row['lead']),row['policy'],fmt(row['chosen_option_different_share']),fmt(row['mean_regret_difference']),str(row['descriptive_paired_bootstrap_95_interval']),fmt(row['exact_two_sided_sign_p']),fmt(row['posterior_only_harm']),fmt(row['model_only_harm']),fmt(row['exact_McNemar_p'])]
            lines.append('| ' + ' | '.join(values) + ' |')
    invalid = result['models'][NEW_MODEL]['invalid_case_indices']
    lines += ['', 'CNN-F-resp-0.01 invalid case indices: ' + str(invalid) + '.', '',
              'Evidence: `receipts/acd_stage10b_resp001_decisions.json`. Source costs and scoring code are SHA-256 recorded. Realized costs are opened only inside the unchanged scoring function. No new integration or inference is performed.', '', 'R-other: none.']
    (ROOT / 'ACD_STAGE10B_RESP001_DECISIONS.md').write_text('\n'.join(lines) + '\n')

if __name__ == '__main__':
    scoring.MODELS = [*scoring.MODELS, 'CNN-noF', NEW_MODEL]
    scoring.save = save_extension
    scoring.score_decisions()
