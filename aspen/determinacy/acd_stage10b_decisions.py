"""CPU-only CNN-noF decision extension; reuses unchanged Stage 13 scoring."""
import hashlib
import json
from pathlib import Path
import acd_stage13_analysis as scoring

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / 'receipts/acd_stage10b_decisions.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save_extension(name, result):
    previous = json.loads((ROOT / 'receipts/acd_stage13_decisions.json').read_text())
    for model, value in previous['models'].items():
        assert result['models'][model] == value, model
    old_pairs = previous['paired_comparisons']
    reproduced = [row for row in result['paired_comparisons'] if row['model'] != 'CNN-noF']
    assert reproduced == old_pairs
    result['stage13_reproduction'] = dict(exact=True, models=len(previous['models']), paired_rows=len(old_pairs))
    paths = [Path(scoring.__file__), ROOT / 'receipts/acd_stage13_decisions.json',
             ROOT / 'runs/stage9/inference/CNN-noF/complete.json',
             ROOT / 'runs/stage4b_null/null_0.16.npz', Path(__file__)]
    paths += sorted((ROOT / 'runs/stage9/inference/CNN-noF').glob('[0-9][0-9][0-9].npz'))
    result['source_hashes'] = {str(path.relative_to(ROOT)):digest(path) for path in paths}
    RECEIPT.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    render(result)

def render(result):
    lines = ['# CNN-noF decisions from saved costs', '',
             'Post hoc on the confirmation panel; licenses no frozen route. CPU-only scoring reuses the Stage 13 policies, climatological margins, exclusions and paired tests. Positive regret differences mean greater regret than the posterior. Bootstrap intervals are descriptive.', '',
             'Every prior Stage 13 model reading and paired comparison reproduced exactly.', '',
             '| Model | Lead (LT) | Policy | Improvement | Regret | Capture | Acting | Harms | Median harm | Largest harm | Zero-harm upper bound | Chosen-action histogram |',
             '|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    def fmt(value):
        return '—' if value is None else format(value, '.8g')
    for model, data in result['models'].items():
        for row in data['readings']:
            fields = [model,fmt(row['lead']),row['policy']] + [fmt(row[k]) for k in ['mean_improvement','mean_regret','capture_fraction','acting_share','harms','median_harm','max_harm','zero_harm_CP_upper']] + [str(row['chosen_actions'])]
            lines.append('| ' + ' | '.join(fields) + ' |')
    lines += ['', 'Histograms follow the frozen pattern order, ending with no action. Zero-harm bounds are one-sided Clopper–Pearson bounds using the Stage 13 confidence level.', '',
              '| Lead (LT) | Policy | Different choices | Regret difference | Descriptive bootstrap interval | Exact sign p | Posterior-only harms | CNN-noF-only harms | Exact McNemar p |',
              '|---:|---|---:|---:|---|---:|---:|---:|---:|']
    for row in result['paired_comparisons']:
        if row['model'] == 'CNN-noF':
            values = [fmt(row['lead']),row['policy'],fmt(row['chosen_option_different_share']),fmt(row['mean_regret_difference']),str(row['descriptive_paired_bootstrap_95_interval']),fmt(row['exact_two_sided_sign_p']),fmt(row['posterior_only_harm']),fmt(row['model_only_harm']),fmt(row['exact_McNemar_p'])]
            lines.append('| ' + ' | '.join(values) + ' |')
    invalid = result['models']['CNN-noF']['invalid_case_indices']
    lines += ['', 'CNN-noF invalid case indices: ' + str(invalid) + '.', '',
              'Evidence: `receipts/acd_stage10b_decisions.json`. Source costs and scoring code are SHA-256 recorded. Realized costs are opened only inside the unchanged scoring function. No new integration or inference is performed.', '', 'R-other: none.']
    (ROOT / 'ACD_STAGE10B_DECISIONS.md').write_text('\n'.join(lines) + '\n')

if __name__ == '__main__':
    scoring.MODELS = [*scoring.MODELS, 'CNN-noF']
    scoring.save = save_extension
    scoring.score_decisions()
