"""Generate AEA source tables and exact frozen readings from recorded products."""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

from common import ROOT,RESULTS,RUNS,QUERY_NAMES,rng,ratio,spearman,classify,sha,write_json

ARMS=["L_range-3","FNO-theta","law","persistence","centre-law"]


def source_hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_csv(name,rows):
    if not rows:return
    path=RESULTS/name
    with path.open("w") as f:
        f.write(f"# git_sha={sha()}\n")
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def main():
    data=json.loads((RESULTS/"points.json").read_text())
    panel_data=json.loads((RESULTS/"panel_feasibility.json").read_text()) if (RESULTS/"panel_feasibility.json").exists() else None
    evaluable=panel_data["evaluable"] if panel_data else data["evaluable_by_chaos"]
    points=data["points"];byid={p["id"]:p for p in points}
    chaos_rows=[]
    for p in points:
        path=RESULTS/"chaos"/f"{p['id']}.json"
        c=json.loads(path.read_text())
        chaos_rows.append(dict(point=p["id"],Re=p["theta"][0],A=p["theta"][1],alpha=p["theta"][2],
                              lam=c["lam"],ci_lo=c["lam_ci95"][0],ci_hi=c["lam_ci95"][1],chaotic=c["chaotic"],
                              source_sha=c.get("git_sha",sha()),source_hash=source_hash(path),label="estimate"))
    save_csv("chaos.csv",chaos_rows)
    gs=np.asarray(data["g"])
    sp=RESULTS/"sensitivity.json"
    sj=json.loads(sp.read_text())
    sensitivity_rows=[dict(query=q,g_Re=gs[i,0],g_A=gs[i,1],g_alpha=gs[i,2],norm=np.linalg.norm(gs[i]),
                           h=sj["h"],evaluable=evaluable[i],source_sha=sj["git_sha"],source_hash=source_hash(sp),label="estimate") for i,q in enumerate(QUERY_NAMES)]
    save_csv("sensitivity.csv",sensitivity_rows)
    reported=[]
    for path in sorted((RESULTS/"reported_sensitivity").glob("*.json")):
        j=json.loads(path.read_text())
        if j["g"] is None:continue
        for qi,q in enumerate(QUERY_NAMES):
            g=j["g"][qi]
            reported.append(dict(point=j["point"],query=q,g_Re=g[0],g_A=g[1],g_alpha=g[2],h=j["h"],
                                 used_for_directions=j["used_for_directions"],source_sha=j["git_sha"],
                                 source_hash=source_hash(path),label="estimate"))
    save_csv("reported_sensitivity.csv",reported)
    errors={};error_rows=[];intervals={}
    for p in points:
        for ai,a in enumerate(ARMS):
            path=RESULTS/"eval"/f"{p['id']}_{a}.json"
            if not path.exists():continue
            j=json.loads(path.read_text());errors[p["id"],a]=j["mean_errors"]
            raw=RUNS/j["raw_file"]
            samples=np.load(raw)["errors"]
            for qi in p["query_ids"]:
                e=j["mean_errors"][qi]
                lo=hi=None
                if e is not None:
                    x=samples[:,qi]
                    if not np.isclose(x.mean(),e,rtol=1e-12,atol=1e-12):raise ValueError("raw/source error mismatch")
                    b=rng("bootstrap",p["index"]*100+ai*10+qi)
                    means=x[b.integers(0,len(x),(2000,len(x)))].mean(1)
                    lo,hi=np.quantile(means,[.025,.975]).tolist()
                error_rows.append(dict(query=QUERY_NAMES[qi],point=p["id"],angle="centre" if p["id"]=="centre" else p["angle"],
                    arm=a,error=e,ci_lo=lo,ci_hi=hi,n=100,D_g=p["D_g"],D_perp=p["D_perp"],distance=p.get("distance",0.),
                    lam=p["chaos"]["lam"],h=j["h"],evaluable=evaluable[qi],seconds=j["wall_seconds"],
                    source_sha=j["git_sha"],source_hash=source_hash(path),raw_hash=source_hash(raw),
                    label="learned" if a in ARMS[:2] else "estimate" if a=="law" else "reference"))
    save_csv("errors.csv",error_rows)
    ratios={a:[] for a in ARMS};ratio_rows=[]
    for qi,q in enumerate(QUERY_NAMES):
        if not evaluable[qi]:continue
        for a in ARMS:
            e0=errors.get((f"q{qi}_0",a),[None]*4)[qi]
            e90=errors.get((f"q{qi}_90",a),[None]*4)[qi]
            r=ratio(e0,e90);ratios[a].append(r)
            ratio_rows.append(dict(query=q,arm=a,error_0=e0,error_90=e90,ratio=r,
                                  symmetric_ratio=None if r is None else max(r,1/r),available=r is not None,label="estimate"))
    save_csv("ratios.csv",ratio_rows)
    correlations={};cor_rows=[]
    training_theta=RUNS/"cache/training_theta.npy"
    covariance=None
    if training_theta.exists():
        from common import CENTRE,RANGE
        u=(np.load(training_theta)-CENTRE)/RANGE
        covariance=np.cov(u,rowvar=False);mean=u.mean(0)
    for a in ARMS:
        rows=[r for r in error_rows if r["arm"]==a and r["evaluable"] and r["error"] is not None]
        e=[r["error"] for r in rows]
        g=[r["D_g"] for r in rows];p=[r["D_perp"] for r in rows]
        rg,rp=spearman(e,g),spearman(e,p)
        correlations[a]=[rg,rp]
        re=spearman(e,[r["distance"] for r in rows]);rm=None
        if covariance is not None:
            inv=np.linalg.inv(covariance)
            distances=[]
            for r in rows:
                d=np.asarray(byid[r["point"]]["u"])-mean
                distances.append(float(np.sqrt(d@inv@d)))
            rm=spearman(e,distances)
        cor_rows.append(dict(arm=a,n_units=len(rows),rho_g=rg,rho_perp=rp,
                            gap=None if rg is None or rp is None else abs(rg-rp),
                            rho_euclidean=re,rho_mahalanobis=rm,partial_lambda_h="unavailable:constant-control",
                            ensemble="cut",identifiability="cut",label="estimate"))
    save_csv("correlations.csv",cor_rows)
    expected=[(p["id"],a) for p in points if p["chaos"]["chaotic"] and
              (RESULTS/"panels"/f"{p['id']}.json").exists() for a in ARMS]
    complete=all(key in errors for key in expected) and bool(expected)
    ne=sum(evaluable)
    if ne<3:outcome="otherwise"
    elif complete:outcome=classify(ratios,correlations,ratios["law"],ne)
    else:outcome="incomplete"
    summary=dict(outcome=outcome,n_evaluable=ne,evaluable=evaluable,complete_arm_panel=complete,
                 ratios=ratios,correlations=correlations,cuts=["45-degree","ensemble","identifiability"],
                 source_tables={f:source_hash(RESULTS/f) for f in ["chaos.csv","sensitivity.csv","errors.csv","ratios.csv","correlations.csv"] if (RESULTS/f).exists()})
    write_json(RESULTS/"summary.json",summary)
    save_csv("outcome.csv",[dict(outcome=outcome,n_evaluable=ne,complete_arm_panel=complete,label="estimate")])
    manifest=[]
    for a in ARMS[:2]:
        info=RUNS/"train"/a/"info.json"
        if info.exists():
            j=json.loads(info.read_text())
            manifest.append(dict(arm=a,steps=j["steps"],n_in=j["n_in"],param_channels=j["param_channels"],
                            params=j["params"],best_step=j["best_step"],best_val=j["best_val"],train_seconds=j["train_seconds"],
                            weights_sha256=source_hash(info.parent/"best.pt"),source_sha=j["git_sha"],label="learned"))
    save_csv("training.csv",manifest)
    print(json.dumps(summary,indent=2))


if __name__=="__main__":main()
