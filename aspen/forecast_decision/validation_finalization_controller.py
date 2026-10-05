"""Curate validation-only inputs; isolated workers make every scientific selection."""
import datetime,hashlib,json,shutil,subprocess,time
from pathlib import Path
import numpy as np
from training_lifecycle import terminal_record
ROOT=Path(__file__).resolve().parent
REMOTE='/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision'
ORDER=['CNN-R2','CNN-roll','CNN-80k','CNN-20k','CNN-5k']
ORDER2=['CNN2-R2','CNN2-roll','CNN2-20k']

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def write(path,payload):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n');tmp.replace(path)
def fetch(remote,local):
    local.parent.mkdir(parents=True,exist_ok=True)
    result=subprocess.run(['scp','sulaco:'+remote,str(local)],capture_output=True,text=True)
    return result.returncode==0
def model_record(name):
    if name=='CNN-20k':
        checkpoint=ROOT/'runs/training_data/CNN-20k.pt';step=20000;kind='state';training=None
    else:
        directory=ROOT/'runs/training'/name
        training,done=terminal_record(name)
        if training is None:return None
        kind=training['kind']
        checkpoint=directory/'selected.pt'
        if kind in ['r2','cost']:
            pending=[p.name for p in directory.glob('checkpoint_*.pt')
                     if not (directory/(p.stem.replace('checkpoint_','validation_')+'.json')).exists()]
            if pending:
                if training.get('status')=='EXTERNALLY_STOPPED':
                    write(directory/'finalization_blocker.json',dict(status='BLOCKED',recorded_at=now(),
                        reason='externally stopped with unevaluated scheduled checkpoints; no candidate omitted',
                        pending_checkpoints=sorted(pending),terminal_receipt=str(done.relative_to(ROOT))))
                return None
            choice=directory/'selection.json'
            if not choice.exists():return None
            step=json.loads(choice.read_text())['step']
        elif kind in ['roll','resp']:step=10000
        else:
            # Read metadata only. The checkpoint was already chosen by the frozen base worker.
            import torch
            step=int(torch.load(checkpoint,map_location='cpu',weights_only=True)['step'])
        if not checkpoint.exists():return None
    stopped=bool(training and training.get('status')=='EXTERNALLY_STOPPED')
    charged=float(training.get('charged_gpu_seconds',training.get('recorded_phase_gpu_seconds_lower_bound'))) if training else None
    extra=0.
    if training and kind not in ['r2','cost']:
        ack=ROOT/'runs/training'/name/f'validation_{step:06d}.json'
        if ack.exists():extra=float(json.loads(ack.read_text())['charged_gpu_seconds'])
    return dict(checkpoint=str(checkpoint.relative_to(ROOT)),sha256=digest(checkpoint),step=step,
                kind='cost' if kind=='cost' else 'state',completed_at=now(),
                recorded_training_selection_phase_gpu_seconds=charged+extra if charged is not None else None,
                recorded_training_selection_phase_gpu_hours=(charged+extra)/3600 if charged is not None else None,
                exact_total_gpu_seconds=None,
                phase_measurement_is_lower_bound=stopped,
                worker_terminal_status='EXTERNALLY_STOPPED' if stopped else 'COMPLETE' if training else 'HISTORICAL',
                cuda_startup_duration_seconds=None,
                cuda_startup_timing_scope='unavailable; excluded from legacy worker phase' if name in ['CNN-roll','CNN-resp','CNN-cost','CNN-R2','CNN-20k'] else 'included from before first CUDA synchronization in new worker phase',
                reservation_upper_bound_receipt='GUARD_STATUS/'+name+'.json' if name!='CNN-20k' else None,
                additional_final_validation_gpu_seconds=extra,
                base_charged_gpu_seconds_in_individual_cap=float(training.get('base_gpu_seconds_in_individual_cap',0)) if training else None,
                timing_status='last synchronized recorded phase is a lower bound; externally stopped; exact final phase unavailable' if stopped else 'synchronized recorded training/selection phase; exact total unavailable; reservation bound is separate' if training else 'historical GPU timing unavailable; no CPU-to-GPU conversion',
                training_receipt_sha256=digest(done) if training else None,
                training_receipt_path=str(done.relative_to(ROOT)) if training else None)

def finalize_system(two,cuts):
    system='two-scale' if two else 'one-scale'
    manifest=ROOT/'runs/training'/('final_selection_stage2b.json' if two else 'final_selection_stage2.json')
    if manifest.exists():return True
    order=ORDER2 if two else ORDER
    required=['CNN2-20k','CNN2-R2','CNN2-cost','CNN2-roll'] if two else [
        'CNN-20k','CNN-roll','CNN-resp','CNN-R2','CNN-cost','CNN-5k','CNN-80k','CNN-20k-s2','CNN-20k-s3']
    required=[n for n in required if n not in cuts]
    models={n:model_record(n) for n in required}
    if any(record is None for record in models.values()):return False
    directory=ROOT/'runs/validation_finalize_inputs'/system;directory.mkdir(parents=True,exist_ok=True)
    stem='validation2_' if two else 'validation_'
    if not fetch(REMOTE+'/runs/selection_inputs/'+stem+'inputs.npz',directory/'validation_inputs.npz'):return False
    if not fetch(REMOTE+'/runs/selection_inputs/'+stem+'skill_inputs.npz',directory/'skill_inputs.npz'):return False
    # Baseline predictions were generated with the same frozen validation windows.
    if not two and not (directory/'CNN-20k.npz').exists():
        if not fetch(REMOTE+'/runs/selection_inputs/baseline_validation_outputs.npz',directory/'CNN-20k.npz'):return False
    proofs=[];S=[n for n in order if n in models]
    for name in S:
        if name=='CNN-20k':continue
        own=ROOT/'runs/training'/name;record=models[name];step=record['step']
        result=own/f'validation_{step:06d}.npz'
        if not result.exists():
            candidate=own/f'checkpoint_{step:06d}.pt'
            if not candidate.exists():shutil.copy2(ROOT/record['checkpoint'],candidate)
            write(own/'final_validation_request.json',dict(step=step,checkpoint=candidate.name,
                 checkpoint_sha256=record['sha256'],requested_at=now(),kind=record['kind']))
            return False
        with np.load(result) as d:
            has_mean='mean_window' in d.files
        if has_mean:shutil.copy2(result,directory/(name+'.npz'))
        elif step==0 and name in ['CNN-R2','CNN2-R2']:
            baseline='CNN2-20k' if two else 'CNN-20k'
            baseline_file=directory/(baseline+'.npz')
            if not baseline_file.exists():
                baseline_step=models[baseline]['step']
                p=ROOT/'runs/training'/baseline/f'validation_{baseline_step:06d}.npz'
                if not p.exists():
                    baseown=ROOT/'runs/training'/baseline
                    basecandidate=baseown/f'checkpoint_{baseline_step:06d}.pt'
                    if not basecandidate.exists():shutil.copy2(ROOT/models[baseline]['checkpoint'],basecandidate)
                    write(baseown/'final_validation_request.json',dict(step=baseline_step,checkpoint=basecandidate.name,
                         checkpoint_sha256=models[baseline]['sha256'],requested_at=now(),kind='state'))
                    return False
                shutil.copy2(p,baseline_file)
            with np.load(result) as selected,np.load(baseline_file) as base:
                if not np.array_equal(selected['survivors'],base['survivors']):
                    raise RuntimeError('initializer baseline member masks differ')
                np.savez(directory/(name+'.npz'),cost=selected['cost'],survivors=selected['survivors'],mean_window=base['mean_window'])
            base_name=name+'_base.pt';initial_name=name+'_initial.pt'
            shutil.copy2(ROOT/models[baseline]['checkpoint'],directory/base_name)
            shutil.copy2(own/'checkpoint_000000.pt',directory/initial_name)
            proofs.append(dict(base=base_name,initial=initial_name))
        else:raise RuntimeError('validation state means unavailable for '+name)
    solver_data={}
    data_root=ROOT/'runs'/('training_data2' if two else 'training_data')
    for kind in ['pairs','cost','base_train','base_val']:
        source=data_root/(kind+'.json')
        if source.exists():solver_data[kind]=dict(source=str(source.relative_to(ROOT)),source_sha256=digest(source),receipt=json.loads(source.read_text()))
    public_compute=ROOT/'runs/training'/('compute_stage2b.json' if two else 'compute_stage2.json')
    diagnostics={}
    pilot=ROOT/'runs/training_pilot/pilot_complete.json'
    if two and pilot.exists():
        diagnostics['CNN2-roll-throughput-pilot']=dict(source=str(pilot.relative_to(ROOT)),
            source_sha256=digest(pilot),receipt=json.loads(pilot.read_text()),
            reservation_upper_bound_receipt='GUARD_STATUS/CNN2-roll-pilot.json')
    write(public_compute,dict(system=system,recorded_at=now(),models={n:{k:r[k] for k in r if k not in ['checkpoint','step','kind','completed_at']} for n,r in models.items()},
                              solver_data=solver_data,
                              diagnostics=diagnostics,
                              aggregate_recorded_phase_gpu_seconds=sum(r['recorded_training_selection_phase_gpu_seconds'] or 0 for r in models.values())+sum(d['receipt']['charged_gpu_seconds'] for d in diagnostics.values()),
                              aggregate_phase_measurement_is_lower_bound=any(r['phase_measurement_is_lower_bound'] for r in models.values()),
                              exact_total_gpu_seconds=None,
                              reservation_upper_bound_summary='GUARD_STATUS/summary.json'))
    configuration=dict(system=system,S=S,order=order,models=models,cuts=sorted(cuts),not_run=[n for n in order if n not in models],
                       compute_manifest=str(public_compute.relative_to(ROOT)),
                       initializer_proofs=proofs,input_hashes={p.name:digest(p) for p in directory.glob('*.npz')})
    write(directory/'configuration.json',configuration)
    remote_inputs=REMOTE+'/runs/validation_finalize_inputs/'+system
    remote_out=REMOTE+'/runs/validation_finalize_outputs/'+system
    subprocess.run(['ssh','sulaco','mkdir -p '+remote_inputs+' '+remote_out],check=True)
    subprocess.run(['scp']+[str(p) for p in directory.iterdir()]+['sulaco:'+remote_inputs+'/'],check=True)
    args=['aa-exec','-p','chrome','--','/home/todd/.local/bin/bwrap','--ro-bind','/','/','--proc','/proc',
          '--dev-bind','/dev','/dev','--tmpfs','/mnt','--tmpfs','/home','--tmpfs','/tmp','--dir','/tmp/worker',
          '--ro-bind',REMOTE+'/runs/selection_source','/tmp/worker/source',
          '--ro-bind',remote_inputs,'/tmp/worker/inputs','--bind',remote_out,'/tmp/worker/out',
          '--ro-bind','/home/todd/niva-datagen/.venv','/tmp/venv','--unsetenv','PYTHONPATH',
          '--chdir','/tmp/worker/source','--','/tmp/venv/bin/python','validation_finalize_worker.py',
          '--inputs','/tmp/worker/inputs','--out','/tmp/worker/out']
    import shlex
    subprocess.run(['ssh','sulaco',shlex.join(args)],check=True)
    if not fetch(remote_out+'/final_selection.json',manifest.with_suffix('.download')):raise RuntimeError('manifest transfer failed')
    manifest.with_suffix('.download').replace(manifest)
    fetch(remote_out+'/selection_evidence.json',ROOT/'runs/training'/('selection_evidence_stage2b.json' if two else 'selection_evidence_stage2.json'))
    print(now(),'finalized',system,flush=True);return True

def main():
    while True:
        control=ROOT/'runs/campaign_control.json'
        if control.exists() and json.loads(control.read_text()).get('execution')=='stop':return
        cutfile=ROOT/'runs/training/cuts.json'
        cuts=set(json.loads(cutfile.read_text()).get('cuts',[])) if cutfile.exists() else set()
        a=finalize_system(False,cuts);b=finalize_system(True,cuts)
        write(ROOT/'runs/training/finalization_status.json',dict(recorded_at=now(),stage2_final=a,stage2b_final=b,cuts=sorted(cuts)))
        if a and b:break
        time.sleep(30)

if __name__=='__main__':main()
