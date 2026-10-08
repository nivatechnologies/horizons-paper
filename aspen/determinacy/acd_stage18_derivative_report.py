"""Render frozen derivative-comparison receipts without recomputation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def fmt(x):return '—' if x is None else format(x,'.6g')

def run():
    models={p.stem.removeprefix('acd_stage18_derivatives_'):json.loads(p.read_text()) for p in sorted((ROOT/'receipts').glob('acd_stage18_derivatives_*.json'))}
    result=dict(post_hoc=True,licenses_frozen_route=False,models=models)
    (ROOT/'receipts/acd_stage18_D.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    text='\n## Part D\n\nForward-mode derivatives pass through the actual FP32 learned rollout; window energies accumulate in float64. Sulaco compares saved derivatives against each draw’s saved physics tangent response. No realized outcome is required.\n\n| Model | LT | Sign agreement | Normalized RMS error | Three-class agreement | Kappa | Median z | Pooled squared error |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
    for name,m in models.items():
        for r in m['rows']:
            text+=f"| {name} | {fmt(r['lead'])} | {fmt(r['per_draw_sign_agreement'])} | {fmt(r['normalized_RMS_error'])} | {fmt(r['three_class_agreement'])} | {fmt(r['three_class_kappa'])} | {fmt(r['median_z'])} | {fmt(r['pooled_MSE'])} |\n"
    text+='\nRMS errors divide by the pooled physics tangent RMS at the same lead. Near-zero posterior masses, per-pair squared-error quartiles and probability-transfer errors are retained in the receipt. The selected response-control derivative is added after its frozen validation selection. All readings are post hoc and license no frozen route.\n'
    path=ROOT/'ACD_STAGE18_READING.md';existing=path.read_text();marker='\n## Part D\n'
    if marker in existing:
        start=existing.index(marker);end=existing.find('\n## Part ',start+len(marker));existing=existing[:start]+(existing[end:] if end!=-1 else '')
    path.write_text(existing.rstrip()+'\n'+text)

if __name__=='__main__':run()
