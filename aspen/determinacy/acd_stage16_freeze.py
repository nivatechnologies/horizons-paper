"""Create Stage16 freeze from fixed code and saved data provenance; no GPU work."""
import hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
NAMESPACE='acd-stage16-seeds'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 # Explicit portable entropy construction; no Python randomized hash.
 entropy=np.frombuffer(hashlib.sha256(NAMESPACE.encode('utf-8')).digest(),dtype='<u4').tolist()
 streams=np.random.SeedSequence(entropy).spawn(4)
 runs=[]
 for index,stream in enumerate(streams,1):
  ts,bs=map(int,stream.generate_state(2,dtype=np.uint32))
  for model in ['CNN-F','CNN-noF']:runs.append(dict(name=f'{model}-seed{index}',model=model,seed_index=index,torch_seed=ts,batch_seed=bs,conditioned=model=='CNN-F',host='192.168.88.4' if index<=2 else '192.168.88.12'))
 baseline=json.loads((ROOT/'receipts/acd_stage9.json').read_text())['F']['CNN-F']
 paths=['acd_stage16_freeze.py','acd_stage16_train.py','acd_stage16_queue.py','acd_stage16_metrics.py','acd_stage16_render.py','acd_stage16_pipeline.py','acd_stage9_cnn.py','acd_stage9_train.py','acd_stage10b_metrics.py','acd_stage13_analysis.py','acd_stats.py','acd_protocol.py']
 contract=dict(status='deferred until Stage15A ranking definition is committed',training_dependency=False)
 d=dict(post_hoc=True,licenses_frozen_route=False,namespace=NAMESPACE,entropy_sha256=hashlib.sha256(NAMESPACE.encode()).hexdigest(),entropy_uint32=entropy,seed_derivation='SHA256 UTF-8 namespace interpreted as little-endian uint32 entropy; SeedSequence.spawn; each child generate_state(2, uint32), Torch first, batch second',runs=runs,data_sha256=baseline['data_sha256'],code_hashes={p:sha(ROOT/p) for p in paths},coverage_contract=contract,recipe=dict(training_trajectories=4096,validation_trajectories=512,updates=20000,effective_batch=128,microbatch=128,learning_rate=.001,weight_decay=.0001,gradient_clip=1,checkpoint_every=1000,validation_steps=12,cap_seconds=36000,optimizer='AdamW',schedule='cosine',dtype='FP32',TF32=False,deterministic_cudnn=True,loss='four-step autoregressive normalized-state MSE plus first-step MSE',guard='skip nonfinite microbatch loss or total preclip gradient norm; count skipped schedule steps; abort above twenty total skips or three consecutive; report every run',checkpoint_rule='lowest validation rollout MSE across all saved validation trajectories and all twelve steps; earliest on ties',parameter_counts={model:sum(sizes[i]*sizes[i+1]*(5 if i<4 else 1)+sizes[i+1] for i in range(5)) for model,sizes in [('CNN-F',[13,256,256,256,256,1]),('CNN-noF',[12,256,256,256,256,1])]}),evaluation='unchanged Stage9 F5 inference; all saved confirmation draws, own noise-free histories, own F only for CNN-F, amplitude 0.16, nine options, eight leads; sulaco-only outcome scoring; fixed posterior eligible cohort; E and C delta zero; Stage15 A matched coverage added after its committed ranking definition; training and evaluation do not wait for it; no selection among seeds')
 dest=ROOT/'receipts/acd_stage16_freeze.json';dest.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
 L=['# Stage16 training-seed replication freeze','','Post hoc on confirmation; licenses no frozen route. Every seed is reported; no selection among seeds. Starts only after Stage10b results and this freeze have been committed and pushed. Stage15 work is untouched.','','Seed derivation: '+d['seed_derivation']+'. Namespace: '+NAMESPACE+'.','','| Run | Torch initialization seed | Batch-order seed |','|---|---:|---:|']
 for r in runs:L.append(f"| {r['name']} | {r['torch_seed']} | {r['batch_seed']} |")
 L+=['','## Fixed recipe','',json.dumps(d['recipe'],indent=2),'','Same saved acd-train-F training and validation data; SHA-256s:',json.dumps(d['data_sha256'],indent=2),'','The retained Stage9 CNN-F and Stage10b CNN-noF are the baseline runs. Training-run variation is reported separately from case-level betting bounds. A failure does not stop the alternating queue. Offline pytorch:26.07 on both authorized local Spark GB10 hosts; seeds one and two on 192.168.88.4, seeds three and four on 192.168.88.12; network disabled; training container sees trainer read-only, training/validation data read-only, and its own output directory writable. No panel input or outcome is mounted for training.','','## Evaluation','',d['evaluation'], '', 'Coverage contract:',json.dumps(contract,indent=2),'','## Code hashes','','| Path | SHA-256 |','|---|---|']
 for p,h in d['code_hashes'].items():L.append(f'| {p} | {h} |')
 (ROOT/'ACD_STAGE16_TRAINING_FREEZE.md').write_text('\n'.join(L)+'\n')
 print(json.dumps({'runs':runs,'freeze_sha256':sha(dest)}))
if __name__=='__main__':main()
