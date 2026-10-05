"""One-scale timestep check and measured single-core two-scale rate."""
import argparse,json,time,platform
from pathlib import Path
import numba,numpy as np
from physics import history,simulate,costs,flow2
from protocol import ROOT,LEADS,WINDOWS,PRIMARY,TICKS,LT,SIGMA,rng,patterns,write_json,digest,assert_leaves
def dtcheck(workers):
    numba.set_num_threads(workers)
    dt=.01;rounds=[]
    while True:
        begin=time.monotonic();rows=[];means=[]
        for c in range(16):
            true,y=history("afd-dtcheck",c,dt)
            member=y+.02*SIGMA*rng("afd-dtcheck",2,c).standard_normal((512,11,40))
            ini=np.tile(member[:,-1],(8,1))
            f=np.repeat(8+.16*patterns(),512,axis=0)
            coarse=costs(simulate(ini,f,dt)).reshape(8,512,len(LEADS))
            fine=costs(simulate(ini,f,dt/2)).reshape(8,512,len(LEADS))
            assert np.isfinite(coarse).all() and np.isfinite(fine).all()
            means.append(coarse.mean(1))
            rows.append((coarse,fine))
            print("dtcheck",dt,c+1,flush=True)
        SJ=np.median(np.array([np.ptp(a,axis=0) for a in means]),axis=0)
        entries=[];argmin_changes=np.zeros(len(LEADS),dtype=int)
        for c,(coarse,fine) in enumerate(rows):
            for h in range(len(LEADS)):
                b=int(coarse[:,:,h].mean(1).argmin())
                argmin_changes[h]+=int(b!=int(fine[:,:,h].mean(1).argmin()))
                for k in range(8):
                    if k==b:continue
                    changes=(fine[k,:,h]-fine[b,:,h])-(coarse[k,:,h]-coarse[b,:,h])
                    difference=abs(float(changes.mean()))
                    se=float(changes.std(ddof=1)/np.sqrt(512))
                    bound=max(.05*float(SJ[h]),2*se)
                    entries.append(dict(case=c,lead=float(LEADS[h]),action=k,winner=b,
                                        change=difference,SE=se,threshold=bound,
                                        passed=bool(SJ[h]>0 and difference<bound)))
        passed=all(e["passed"] for e in entries)
        record=dict(dt=dt,dt_fine=dt/2,passed=passed,S_J=SJ.tolist(),
                    argmin_changes=argmin_changes.tolist(),comparisons=entries,
                    seconds=time.monotonic()-begin)
        rounds.append(record)
        write_json(ROOT/"runs/numerics/dtcheck.json",dict(status="PASS" if passed else "REFINE",
                   chosen_dt=dt if passed else None,rounds=rounds,leaf_roots=assert_leaves()))
        if passed:break
        dt/=2
        if dt<1e-6:raise RuntimeError("refinement failed to settle; halt")
def rate():
    numba.set_num_threads(1)
    z=rng("afd2-dtcheck",0,299).standard_normal((2048,440))*.01
    z[:,:40]+=10
    f=np.full((2048,40),10.)
    flow2(z[:1],f[:1],1,.001)
    measurements=[]
    for _ in range(5):
        start=time.perf_counter();out=flow2(z,f,20,.001)
        elapsed=time.perf_counter()-start
        assert np.isfinite(out).all()
        measurements.append(elapsed/20)
    rate=float(np.median(measurements))
    truth_steps=int(np.ceil(3*LT/.05)) * 50 # output-grid run through primary last tick plus tick cover
    primary_steps=int(WINDOWS[PRIMARY][-1])*50
    total=300*9*primary_steps*rate/3600
    write_json(ROOT/"runs/numerics/twoscale_rate.json",
        dict(host=platform.node(),threads=1,batch_members=2048,dt=.001,steps_per_repeat=20,
             repeat_seconds_per_step=measurements,median_seconds_per_step=rate,
             LT_ref=LT,primary_truth_steps=primary_steps,
             projected_primary_truth_single_core_hours=total,
             wo_reference_total_hours=96,extra_cost_wo_estimate_hours=15,
             projection_plus_wo_extra_hours=total+15,
             note="Truth projection derived from measured batch step rate. Extra 15h is WO estimate, not measured.",
             source_hash=digest(ROOT/"physics.py")))
    print("rate",rate,"projected primary truth core-hours",total,flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("task",choices=["dtcheck","rate"]);p.add_argument("--workers",type=int,default=96);a=p.parse_args()
    assert (ROOT/"AFD_FREEZE.md").exists()
    if a.task=="dtcheck":dtcheck(a.workers)
    else:rate()
if __name__=="__main__":main()

