"""Public compute receipts; no training data, validation outcomes or test reads."""
import json,datetime
from protocol import ROOT,RECIPE,digest,write_json


def collect(root=ROOT):
    training={'CNN-20k':dict(actual_gpu_hours=None,reason='AAH recorded CPU wall time only; GPU time unavailable')};sources={}
    for name in RECIPE:
        path=root/f'runs/training/{name}/training_complete.json'
        if not path.exists():continue
        row=json.loads(path.read_text());charge=row['charged_gpu_seconds']
        training[name]=dict(actual_charged_gpu_seconds=charge,actual_charged_gpu_hours=charge/3600,
            selection_gpu_seconds=row.get('selection_gpu_seconds'),gpu_name=row.get('gpu_name'),last_step=row.get('last_step'),receipt_sha256=digest(path))
        sources[str(path.relative_to(root))]=digest(path)
    solver={}
    for system,directory in [('one-scale','training_data'),('two-scale','training_data2')]:
        for label in ['pairs','cost']:
            path=root/f'runs/{directory}/{label}.json'
            if not path.exists():continue
            row=json.loads(path.read_text());solver[system+'_'+label]=dict(measured_cpu_wall_seconds=row.get('seconds'),starts=row.get('starts'),dt=row.get('dt'),data_sha256=row.get('sha256'),receipt_sha256=digest(path))
            sources[str(path.relative_to(root))]=digest(path)
    return dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),training=training,solver_data=solver,receipt_source_hashes=sources,
        rule='CPU wall seconds are never relabeled as GPU-hours; GPU time comes only from charged worker receipts')
if __name__=='__main__':write_json(ROOT/'runs/statistics_compute_metadata.json',collect())
