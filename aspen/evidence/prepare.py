"""Numerical QA, centre calibration, fixed-lead sensitivities and every-point chaos gate."""
import argparse
import gc
import json
import math
import time

import numpy as np
import torch

from common import CENTRE, RANGE, QUERY_NAMES, RESULTS, RUNS, World, queries, rng, geometry, write_json
from ap.solver import KolmoDrag


def starts(theta, stream, index, n):
    theta = np.broadcast_to(theta, (n, 3)).copy()
    model = World(theta)
    return model, model.random_ic(rng(stream, index), n)


def qa():
    theta = np.array([[40., 1., .07733], [46., 1.1, .092796]])
    model = World(theta)
    x = model.random_ic(rng("qa"), 2)
    fast = model.flow(x, 25)
    slow_model = World(theta, graphs=False)
    slow = slow_model.flow(x, 25)
    torch.testing.assert_close(fast, slow, rtol=1e-12, atol=1e-12)
    errors = []
    for i in range(2):
        base = KolmoDrag([theta[i, 0]], alpha=theta[i, 2], amp=[theta[i, 1]], device="cuda")
        reference = base.flow(x[i:i+1], 25)
        torch.testing.assert_close(fast[i:i+1], reference, rtol=1e-12, atol=1e-12)
        errors.append(float((fast[i:i+1]-reference).abs().max()))
    # Query identities and scalar-vs-batched derivative operators.
    q = queries(model, x)
    omega = model.to_phys(x)
    cos4y = torch.cos(4*torch.arange(64, device="cuda", dtype=torch.float64)*2*math.pi/64)[:,None]
    theta_t = torch.as_tensor(theta, device="cuda")
    torch.testing.assert_close(q[:, 0], -theta_t[:, 1]/4 * (omega*cos4y).mean((-2,-1)), rtol=1e-12, atol=1e-12)
    torch.testing.assert_close(q[:, 1], (omega**2).mean((-2,-1))/theta_t[:, 0], rtol=1e-12, atol=1e-12)
    del model, fast, slow, x, base, slow_model, q
    gc.collect(); torch.cuda.empty_cache()
    timing = []
    for n in [64, 128]:
        m, x = starts(CENTRE, "qa", n, n)
        x = m.flow(x, 10)
        torch.cuda.synchronize()
        t = time.monotonic()
        y = m.flow(x, 1000)
        torch.cuda.synchronize()
        timing.append(dict(batch=n, steps=1000, seconds=time.monotonic()-t, finite=bool(torch.isfinite(y).all())))
        del m, x, y
        gc.collect(); torch.cuda.empty_cache()
    write_json(RESULTS/"numerical_qa.json", dict(max_reference_errors=errors, graph_eager_verified=True,
               query_identities_verified=True, timing=timing, torch_version=torch.__version__,
               gpu=torch.cuda.get_device_name(0)))
    print(json.dumps(timing), flush=True)


def chaos(theta, index, name):
    path = RESULTS/"chaos"/f"{name}.json"
    if path.exists():
        result = json.loads(path.read_text())
        if not np.array_equal(result["theta"], theta):
            raise RuntimeError("existing chaos parameters changed")
        return result
    t = time.monotonic()
    model, x = starts(theta, "chaos", index*2, 64)
    print("chaos burn", name, theta, flush=True)
    x = model.flow(x, 50000)
    theta_all = np.broadcast_to(theta, (128, 3)).copy()
    twins = World(theta_all)
    perturb = model.to_spec(torch.as_tensor(rng("chaos", index*2+1).standard_normal((64,64,64)), device="cuda"))
    def norm(wh):
        return model._mean_sq(wh).sqrt()
    perturb *= (1e-6*norm(x)/norm(perturb))[:, None, None]
    both = torch.cat([x, x+perturb])
    logs = []
    for k in range(800):
        both = twins.flow(both, 100)
        base, twin = both[:64], both[64:]
        d = twin-base
        nd, target = norm(d), 1e-6*norm(base)
        logs.append(torch.log(nd/target).cpu().numpy())
        both = torch.cat([base, base+d*(target/nd)[:,None,None]])
        if (k+1)%100 == 0:
            print("chaos", name, k+1, round(time.monotonic()-t,1), flush=True)
    lam = np.asarray(logs)[20:].mean(0)
    finite = bool(np.isfinite(lam).all() and torch.isfinite(both).all())
    mean = float(lam.mean()) if finite else None
    se = float(lam.std(ddof=1)/8) if finite else None
    ci = [mean-1.96*se, mean+1.96*se] if finite else [None,None]
    result = dict(name=name, theta=np.asarray(theta).tolist(), lam=mean, lam_se=se, lam_ci95=ci,
                  per_start=lam.tolist() if finite else [], finite=finite,
                  chaotic=finite and ci[0]>0, seconds=time.monotonic()-t,
                  n_starts=64, burn=500, lyapunov_duration=800, transient=20, seed_index=index)
    write_json(path, result)
    print("chaos finished", name, mean, ci, result["chaotic"], flush=True)
    del model, twins, both, x
    gc.collect(); torch.cuda.empty_cache()
    return result


def sensitivity(theta, h, index):
    model, x = starts(theta, "sensitivity", index, 64)
    x = model.flow(x, 50000)
    g = np.zeros((4,3))
    for j in range(3):
        qpm = []
        for sign in [-1,1]:
            perturbed = np.asarray(theta).copy()
            perturbed[j] += sign*.1*RANGE[j]
            m = World(np.broadcast_to(perturbed,(64,3)).copy())
            y = m.advance(x.clone(), h)
            qpm.append(queries(m,y).mean(0).cpu().numpy())
            del m,y
            gc.collect(); torch.cuda.empty_cache()
        g[:,j] = (qpm[1]-qpm[0])/.2
    del model,x
    gc.collect(); torch.cuda.empty_cache()
    return g


def prepare():
    RESULTS.mkdir(parents=True, exist_ok=True)
    cg = chaos(CENTRE,0,"centre")
    if not cg["chaotic"]:
        write_json(RESULTS/"feasibility.json", dict(outcome="otherwise", reason="centre chaos failed", n_evaluable=0))
        return
    sp = RESULTS/"sensitivity.json"
    if sp.exists():
        sj = json.loads(sp.read_text())
        g = np.asarray(sj["g"])
    else:
        h = .5/cg["lam"]
        print("centre sensitivity", h, flush=True)
        g = sensitivity(CENTRE,h,0)
        write_json(sp, dict(g=g.tolist(), query_names=QUERY_NAMES, h=h, lead="fixed-centre", fd_step=.1, n_states=64))
    points = [{"id":"centre", "index":0, "theta":CENTRE.tolist(), "u":[0.,0.,0.], "chaos":cg,
               "query_ids":list(range(4)), "D_g":0., "D_perp":0.}]
    usable = []
    for qi,name in enumerate(QUERY_NAMES):
        panel = geometry(g[qi])
        if panel is None:
            usable.append(False)
            continue
        good = True
        for angle in ["0","90"]:
            idx = 1+2*qi+(angle=="90")
            point_id = f"q{qi}_{angle}"
            p = dict(panel[angle], id=point_id, index=idx, query_ids=[qi], angle=int(angle))
            p["chaos"] = chaos(p["theta"],idx,point_id)
            good &= p["chaos"]["chaotic"]
            points.append(p)
        usable.append(bool(good))
    write_json(RESULTS/"points.json", dict(points=points, g=g.tolist(), query_names=QUERY_NAMES,
               evaluable_by_chaos=usable, n_evaluable=sum(usable), cuts=["45-degree", "ensemble", "identifiability"]))
    write_json(RESULTS/"feasibility.json", dict(n_evaluable=sum(usable), evaluable_by_chaos=usable,
               outcome="ready" if sum(usable)>=3 else "otherwise",
               reason="chaos-and-sensitivity panel sufficiency"))
    print("PREPARE COMPLETE", sum(usable), "evaluable queries", flush=True)


def reported_sensitivity():
    points=json.loads((RESULTS/"points.json").read_text())["points"]
    for p in points:
        path=RESULTS/"reported_sensitivity"/f"{p['id']}.json"
        if path.exists():continue
        if p["id"]=="centre":
            result=json.loads((RESULTS/"sensitivity.json").read_text())
            write_json(path,dict(point=p["id"],g=result["g"],h=result["h"],lead="fixed-local",used_for_directions=True))
        elif p["chaos"]["chaotic"]:
            h=.5/p["chaos"]["lam"]
            g=sensitivity(p["theta"],h,p["index"])
            write_json(path,dict(point=p["id"],g=g.tolist(),h=h,lead="fixed-local",used_for_directions=False))
            print("reported sensitivity",p["id"],flush=True)
        else:
            write_json(path,dict(point=p["id"],g=None,h=None,reason="chaos-failed",used_for_directions=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["qa","prepare","reported-sensitivity"])
    args = parser.parse_args()
    torch.set_num_threads(4)
    {"qa":qa,"prepare":prepare,"reported-sensitivity":reported_sensitivity}[args.phase]()
