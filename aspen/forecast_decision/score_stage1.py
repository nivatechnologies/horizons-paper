"""Coordinator-only Stage-1 reading; CPU bootstrap on sulaco."""
import argparse,json,datetime,time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from protocol import *
def normal_eligible(cost):
    means=cost[:,:1024].mean(1);b=int(means.argmin())
    d=cost[:,1024:]-cost[b,1024:]
    low=d.mean(1)-2.983*d.std(1,ddof=1)/np.sqrt(1024)
    good=bool(np.all(np.delete(low,b)>0))
    return b,good,low
def bootstrap_eligible(cost,b,ns,c,h):
    d=np.delete(cost[:,1024:]-cost[b,1024:],b,axis=0)
    R=rng(ns,3,c,member=h)
    values=[]
    for _ in range(40):
        ind=R.integers(1024,size=(500,1024))
        values.append(d[:,ind].mean(-1))
    draws=np.concatenate(values,axis=1)
    low=np.quantile(draws,.01/7,axis=1,method="linear")
    return bool(np.all(low>0)),low
def acc(pred,actual,climate):
    a=pred-climate[:,None,:];b=actual-climate[:,None,:]
    fa=(a*a).sum(-1);ob=(b*b).sum(-1)
    out=np.zeros_like(fa)
    out[ob<=0]=np.nan
    keep=(ob>0)&(fa>0)&(fa>=1e-24*ob)
    out[keep]=(a*b).sum(-1)[keep]/np.sqrt(fa[keep]*ob[keep])
    return out
def score_one(c,climate,fixed):
    cpu=np.load(ROOT/f"runs/test/cpu_{c:03d}.npz")
    net=np.load(ROOT/f"runs/test/CNN-20k_{c:03d}.npz")
    row=dict(case=c,leads=[])
    myopic=int(cpu["N-last_cost"][:,:,0].mean(1).argmin())
    for h,T in enumerate(LEADS):
        if h==0:continue
        truth=cpu["truth_cost"][:8,:,h]
        b,eligible,low=normal_eligible(truth)
        # Member bootstrap cross-check is truth-only and independent at each lead.
        boot,bootlow=bootstrap_eligible(truth,b,"afd-bootstrap",c,h)
        entry=dict(T=float(T),h=h,b=b,eligible=eligible,confirmation_bounds=low.tolist(),
                   bootstrap_eligible=boot,bootstrap_bounds=bootlow.tolist(),
                   full_best=int(truth.mean(1).argmin()),
                   myopic_correct=myopic==b,fixed_correct=fixed==b,arms={})
        full=truth.mean(1)
        for name in ["N-last","N-oracle","CNN-20k"]:
            if name=="CNN-20k":
                keep=net["survivors"][h];failed=int(keep.sum())<32
                chosen=int(net["cost"][h].argmin()) if not failed else -1
                mean=net["mean"][h];var=net["var"][h];cost=net["cost"][h]
                dropped=int((~keep).sum())
            else:
                mean=cpu[name+"_mean"];var=cpu[name+"_var"];cost=cpu[name+"_cost"][:,:,h].mean(1)
                chosen=int(cost.argmin());failed=False;dropped=0
            w=WINDOWS[h]
            skill=acc(mean[:8,w],cpu["actual"][:8,w],climate)
            wacc=0. if failed else float(skill.mean())
            rmse=None if failed else float(np.sqrt(np.mean((mean[:8,w]-cpu["actual"][:8,w])**2,axis=-1)).mean()/SIGMA)
            # All metrics retain per-case sufficient statistics for case bootstrap.
            other=[k for k in range(8) if k!=b]
            response=mean[other][:,w]-mean[b,w]
            truth_response=cpu["truth_mean"][other][:,w]-cpu["truth_mean"][b,w]
            vresponse=var[other][:,w]-var[b,w]
            tvresponse=cpu["truth_var"][other][:,w]-cpu["truth_var"][b,w]
            entry["arms"][name]=dict(chosen=chosen,correct=chosen==b and not failed,
                 failed=failed,dropped=dropped,wACC=wacc,wRMSE=rmse,
                 cost=cost.tolist(),J=full.tolist(),J0=float(cpu["truth_cost"][8,:,h].mean()),
                 regret_raw=float(full.max()-full.min()) if failed else float(full[chosen]-full.min()),
                 MSRE_num=None if failed else float(np.sum((response-truth_response)**2)),
                 MSRE_den=None if failed else float(np.sum(truth_response**2)),
                 VRE_num=None if failed else float(np.sum((vresponse-tvresponse)**2)),
                 VRE_den=None if failed else float(np.sum(tvresponse**2)))
        row["leads"].append(entry)
    return row

def score():
    if not all((ROOT/f"runs/test/CNN-20k_{c:03d}.npz").exists() for c in range(200)):
        raise RuntimeError("CNN test inference incomplete")
    climate=np.load(ROOT/"inputs/climatology.npy")
    fixed_choices=[]
    for c in range(100):
        with np.load(ROOT/f"runs/val/cpu_{c:03d}.npz") as d:
            fixed_choices.append(int(d["truth_cost"][:8,:1024,PRIMARY].mean(1).argmin()))
    fixed=int(np.bincount(fixed_choices,minlength=8).argmax())
    rows=[]
    # Coordinator compute threads; case streams are fixed and independent.
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures=[pool.submit(score_one,c,climate,fixed) for c in range(200)]
        for c,future in enumerate(futures):
            rows.append(future.result())
            write_json(ROOT/"runs/stage1_cases_partial.json",dict(cases=rows))
            print("scored",c+1,flush=True)
    readings=[]
    for j,T in enumerate(LEADS[1:]):
        entries=[r["leads"][j] for r in rows]
        mask=np.array([e["eligible"] for e in entries]);n=int(mask.sum())
        correct={name:np.array([e["arms"][name]["correct"] for e in entries],dtype=float) for name in ["N-last","N-oracle","CNN-20k"]}
        P={name:float(a[mask].mean()) if n else None for name,a in correct.items()}
        myopic=float(np.array([e["myopic_correct"] for e in entries])[mask].mean()) if n else None
        pfixed=float(np.array([e["fixed_correct"] for e in entries])[mask].mean()) if n else None
        arm={}
        for name in correct:
            failures=sum(e["arms"][name]["failed"] for e in entries)
            dropped=sum(e["arms"][name]["dropped"] for e in entries)
            a=[e["arms"][name] for e in entries]
            skill=float(np.mean([v["wACC"] for v,m in zip(a,mask) if m])) if n else None
            rmses=[v["wRMSE"] for v,m in zip(a,mask) if m and v["wRMSE"] is not None]
            arm[name]=dict(P=P[name],wACC=skill,wRMSE=float(np.mean(rmses)) if rmses else None,
                 failed_cases=failures,dropped_members=dropped,attempted_members=200*64,
                 reliable=failures<=2 and dropped<=128,
                 excluded_wRMSE_cases=sum(m and v["failed"] for v,m in zip(a,mask)),
                 all_case_wACC=float(np.mean([v["wACC"] for v in a])))
        R=rng("afd-bootstrap",3,member=j+100)
        samples=R.integers(200,size=(2000,200))
        denom=mask[samples].sum(1)
        gap=(correct["N-last"]-correct["CNN-20k"])
        if n and np.all(denom>0):
            dist=(gap[samples]*mask[samples]).sum(1)/denom
            assert np.isfinite(dist).all()
            lower=float(np.quantile(dist,.05,method="linear"));upper=float(np.quantile(dist,.95,method="linear"))
        else:
            lower=upper=None
        g=P["N-last"]-P["CNN-20k"] if n else None
        sufficient=n>=160
        trivial=n>0 and P["N-last"]-max(myopic,pfixed)<.05
        comparable=n>0 and arm["CNN-20k"]["wACC"]>=arm["N-last"]["wACC"]-.01
        kill=comparable and upper is not None and upper<=.05
        witness=comparable and lower is not None and arm["CNN-20k"]["wRMSE"] is not None and arm["N-last"]["wRMSE"] is not None and arm["CNN-20k"]["reliable"] and arm["CNN-20k"]["wACC"]>=arm["N-last"]["wACC"] and arm["CNN-20k"]["wRMSE"]<=arm["N-last"]["wRMSE"] and g>=.15 and lower>=.10
        verdict="otherwise" if not sufficient or trivial else "KILL" if kill else "PASS" if witness else "otherwise"
        readings.append(dict(T=float(T),eligible=n,total=200,eligible_fraction=n/200,sufficiency=bool(sufficient and not trivial),
                   sufficiency_status="INSUFFICIENT" if not sufficient else "TRIVIAL" if trivial else "SUFFICIENT",
                   null_gap=P["N-last"]-max(myopic,pfixed) if n else None,myopic_P=myopic,fixed_P=pfixed,fixed_action=fixed,
                   random_P=1/8,arms=arm,comparable=comparable,gap=g,lower95=lower,upper95=upper,H1a=verdict,
                   eligibility_bootstrap_agreement=sum(e["eligible"]==e["bootstrap_eligible"] for e in entries),
                   eligible_full_argmin_disagreements=sum(e["eligible"] and e["b"]!=e["full_best"] for e in entries)))
    output=dict(stage="1",S=["CNN-20k"],read_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                actor="coordinator",licensed_sentences=[],leads=readings,
                primary=next(r for r in readings if r["T"]==2))
    write_json(ROOT/"runs/stage1_cases.json",dict(cases=rows))
    write_json(ROOT/"runs/stage1_reading.json",output)
    print("Stage1",output["primary"]["H1a"],flush=True)
if __name__=="__main__":score()

