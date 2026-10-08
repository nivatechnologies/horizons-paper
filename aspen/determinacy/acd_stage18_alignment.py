"""Read-only alignment record from generating, training and inference code."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,'/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision')
import protocol

def run():
    freeze=json.loads((ROOT/'receipts/acd_stage18_freeze.json').read_text())
    data=ROOT/'runs/stage18/data/train.npz'
    if hashlib.sha256(data.read_bytes()).hexdigest()!=freeze['training_data_sha256']['train.npz']:raise RuntimeError('Training data hash differs')
    with np.load(data) as d:
        frames=d['H'].shape[1];future=d['T'].shape[2]
    offsets=np.arange(frames)-frames+1
    files=['acd_stage9_training_data.py','acd_stage9_train.py','acd_stage9_cnn.py','acd_stage18_estimators.py']
    evidence={}
    for name in files:
        path=ROOT/name;lines=path.read_text().splitlines()
        tokens={'acd_stage9_training_data.py':['H=physics.simulate','A=amp','T[b:e]='],
                'acd_stage9_train.py':['def base','pred=model(ctx,A[:,0],F)','ctx=H.repeat_interleave'],
                'acd_stage9_cnn.py':['ctx=torch.tensor(H[draw]/sigma','pred=model(ctx,a,f)'],
                'acd_stage18_estimators.py':['offsets = rng.integers','entire = np.concatenate','action = data[']}[name]
        evidence[name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'lines':[i for i,line in enumerate(lines,start=1) if any(t in line for t in tokens)]}
    record={'post_hoc':True,'licenses_frozen_route':False,'training_data_sha256':freeze['training_data_sha256'],
            'context_frames':frames,'future_frames_per_branch':future,'context_tick_offsets_from_onset':offsets.tolist(),
            'context_times_from_onset':(offsets*protocol.OUT).tolist(),'output_spacing':protocol.OUT,
            'LT':protocol.LT,'all_original_context_replaced_after_ticks':frames,
            'all_original_context_replaced_after_time':frames*protocol.OUT,'all_original_context_replaced_after_LT':frames*protocol.OUT/protocol.LT,
            'training_context':f'{frames-1} factual frames before onset and the cutoff state at onset; intervention begins for the next predicted step. The action field accompanies the full factual context, including frames generated before onset.',
            'training_rollout':'The same action field and trajectory forcing accompany every autoregressive call as predicted frames replace factual frames.',
            'evaluation':'Each draw supplies its own noise-free factual history at the cutoff; the selected action field accompanies the initial context and every subsequent rolling context. This matches the onset alignment of training.',
            'E1':'Random offsets range from the pre-action context through the last complete context in each action branch. The branch action field is supplied even to a window entirely before onset.',
            'evidence':evidence,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'receipts/acd_stage18_alignment.json').write_text(json.dumps(record,indent=2)+'\n')

if __name__=='__main__':run()
