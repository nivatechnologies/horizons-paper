"""Public compute receipts; no training data, validation outcomes or test reads."""
import json,datetime
from protocol import ROOT,RECIPE,digest,write_json


def collect(root=ROOT):
    training={'CNN-20k':dict(actual_gpu_hours=None,reason='AAH recorded CPU wall time only; GPU time unavailable')};sources={}
    for name in RECIPE:
        path=root/f'runs/training/{name}/training_complete.json'
        if not path.exists():continue
        row=json.loads(path.read_text());charge=row['charged_gpu_seconds']
        training[name]=dict(recorded_charged_phase_gpu_seconds=charge,recorded_charged_phase_gpu_hours=charge/3600,
            timer_scope=row.get('charged_timer_scope','Legacy worker phase timer; excludes CUDA setup'),cuda_setup_gpu_seconds=row.get('cuda_setup_gpu_seconds'),total_gpu_hours=None,
            total_gpu_hours_status='unavailable: CUDA setup GPU duration is not recorded; conservative process reservation is a separate upper bound',
            selection_gpu_seconds=row.get('selection_gpu_seconds'),gpu_name=row.get('gpu_name'),last_step=row.get('last_step'),receipt_sha256=digest(path))
        sources[str(path.relative_to(root))]=digest(path)
    solver={}
    for system,directory in [('one-scale','training_data'),('two-scale','training_data2')]:
        for label in ['pairs','cost']:
            path=root/f'runs/{directory}/{label}.json'
            if not path.exists():continue
            row=json.loads(path.read_text());solver[system+'_'+label]=dict(measured_cpu_wall_seconds=row.get('seconds'),starts=row.get('starts'),dt=row.get('dt'),data_sha256=row.get('sha256'),receipt_sha256=digest(path))
            sources[str(path.relative_to(root))]=digest(path)
    published={}
    for stage in ['2','2b']:
        path=root/f'runs/training/compute_stage{stage}.json'
        if path.exists():
            published[stage]=json.loads(path.read_text());sources[str(path.relative_to(root))]=digest(path)
            for name,receipt in published[stage]['models'].items():
                # FINAL public receipt supersedes a partial legacy worker receipt.
                # Externally stopped workers have no fabricated training_complete.
                charge=receipt['recorded_training_selection_phase_gpu_seconds']
                training[name]=dict(recorded_charged_phase_gpu_seconds=charge,
                    recorded_charged_phase_gpu_hours=receipt['recorded_training_selection_phase_gpu_hours'],
                    phase_measurement_is_lower_bound=receipt.get('phase_measurement_is_lower_bound',False),
                    timer_scope=receipt['cuda_startup_timing_scope'],
                    timing_status=receipt['timing_status'],
                    cuda_setup_gpu_seconds=receipt.get('cuda_startup_duration_seconds'),
                    total_gpu_hours=None,total_gpu_hours_status='exact total unavailable; reservation upper bound is separate',
                    worker_terminal_status=receipt['worker_terminal_status'],
                    additional_final_validation_gpu_seconds=receipt.get('additional_final_validation_gpu_seconds'),
                    reservation_upper_bound_receipt=receipt.get('reservation_upper_bound_receipt'),
                    receipt_sha256=receipt.get('training_receipt_sha256'),public_compute_sha256=digest(path))
    stage_hours={stage:sum(v['recorded_charged_phase_gpu_hours'] or 0 for name,v in training.items() if name!='CNN-20k' and (name.startswith('CNN2-') if stage=='2b' else not name.startswith('CNN2-'))) for stage in ['2','2b']}
    return dict(published_stage_recorded_phase_gpu_hours={stage:receipt['aggregate_recorded_phase_gpu_seconds']/3600 for stage,receipt in published.items()},aggregate_phase_measurement_is_lower_bound=any(v.get('phase_measurement_is_lower_bound',False) for v in training.values()),published_stage_compute=published,terminal_model_recorded_phase_gpu_hours=stage_hours,at=datetime.datetime.now(datetime.timezone.utc).isoformat(),training=training,solver_data=solver,receipt_source_hashes=sources,
        rule='CPU wall seconds are never relabeled as GPU-hours; Recorded GPU phase time comes only from worker receipts; legacy CUDA setup duration and exact total GPU time remain unavailable; process elapsed reservation bounds are not measured GPU time')
if __name__=='__main__':write_json(ROOT/'runs/statistics_compute_metadata.json',collect())
