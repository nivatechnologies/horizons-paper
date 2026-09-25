"""Tasks 2.7 (stall check), 3 and 4: train, select on validation loss, evaluate on confirmation panels.

Usage:
  t3_learned.py list  --grid main|stall            print the job list
  t3_learned.py run   --grid main --shard i --nshards n --device cuda:k
Each job writes runs/learned/<grid>/<tag>/{info.json, eval.npz, model.pt}; finished jobs are skipped.
Label: every number from here is `learned`.
"""
import argparse
import json
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402
import torch  # noqa: E402

from th import config, data, score  # noqa: E402
from th.learn import Task, train_probe  # noqa: E402
from th.systems import flow, get_system  # noqa: E402

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
OUT = config.RUNS / "learned"


def jobs(grid):
    fz = config.freeze()
    seeds = fz["seeds"]["model_seeds"]
    extra = fz["seeds"]["headline_extra_model_seeds"]
    D = fz["scoring"]["frame_intervals"]
    J = []
    if grid == "postfreeze_dataB":
        # POST-FREEZE (Todd, 2026-09-25): B on the 20,000 tu data axis, beside A's frozen data-axis cells
        return [dict(system="lorenz28", arm="B", bits=b, delta=0.05, seed=s, n_traj=1000, outdir="postfreeze")
                for b in (6, 10) for s in seeds]
    if grid == "postfreeze_dataC":
        # POST-FREEZE (Todd, 2026-09-25): C (sigma = 0) on the 20,000 tu data axis, paired with A 20k at 10 bits
        return [dict(system="lorenz28", arm="C", bits=0, delta=0.05, seed=s, noise=0.0, n_traj=1000,
                     outdir="postfreeze") for s in seeds]
    if grid == "ext_large":
        # POST-FREEZE EXTENSION E5.3 (ext_freeze.yaml e5_controls.larger_model)
        import yaml
        ez = yaml.safe_load((config.PKG / "ext_freeze.yaml").read_text())["e5_controls"]["larger_model"]
        bb = {k: ez["backbone"][k] for k in ("width", "layers", "heads", "ff")}
        J = []
        for s in seeds:
            for b in (4, 10):
                for arm in ("A", "B"):
                    J.append(dict(system="lorenz28", arm=arm, bits=b, delta=0.05, seed=s, steps=ez["steps"],
                                  backbone=bb, outdir="ext_large"))
            J.append(dict(system="lorenz28", arm="C", bits=0, delta=0.05, seed=s, noise=0.0, steps=ez["steps"],
                          backbone=bb, outdir="ext_large"))
        return J
    if grid == "stall":
        for b in (4, 6, 8, 10):
            for d in D:
                J.append(dict(system="lorenz28", arm="A", bits=b, delta=d, seed=0, steps=1000, panel="validation"))
        return J
    # Lorenz-63 rho = 28 core grid (never cut)
    for b in (4, 6, 8, 10):
        for d in D:
            for s in seeds + (extra if (d == 0.02 and b in (4, 6)) else []):
                for arm in ("A", "B", "D"):
                    J.append(dict(system="lorenz28", arm=arm, bits=b, delta=d, seed=s))
    for d in D:
        for nz in fz["learned"]["c_noise_levels"]:
            for s in seeds + (extra if d == 0.02 else []):
                J.append(dict(system="lorenz28", arm="C", bits=0, delta=d, seed=s, noise=nz))
    # cut order (WO 6): E last to cut, then L96 subset, rho=45 subset, data axis
    for b in (4, 6, 8, 10):
        for s in seeds:
            J.append(dict(system="lorenz28", arm="E", bits=b, delta=0.05, seed=s))
    for sysn in ("l96_5", "lorenz45"):
        for b in (6, 10):
            for s in seeds:
                for arm in ("A", "B"):
                    J.append(dict(system=sysn, arm=arm, bits=b, delta=0.05, seed=s))
        for s in seeds:
            J.append(dict(system=sysn, arm="C", bits=0, delta=0.05, seed=s, noise=0.0))
    for b in (6, 10):
        for s in seeds:
            J.append(dict(system="lorenz28", arm="A", bits=b, delta=0.05, seed=s, n_traj=1000))
    return J


def tag_of(j):
    t = f"{j['system']}_{j['arm']}_b{j['bits']}_D{j['delta']}_s{j['seed']}"
    if j["arm"] == "C":
        t += f"_n{j.get('noise', 0.0)}"
    if j.get("n_traj"):
        t += f"_traj{j['n_traj']}"
    if j.get("steps"):
        t += f"_steps{j['steps']}"
    if j.get("backbone"):
        t += f"_w{j['backbone']['width']}L{j['backbone']['layers']}"
    return t


def integrate_frames(system, x0, sub, n_frames, dt=data.DT):
    f = get_system(system).f
    out = np.empty((n_frames + 1,) + x0.shape)
    out[0] = x0
    x = x0.copy()
    for j in range(1, n_frames + 1):
        x = flow(f, x, sub, dt)
        out[j] = x
    return out


def horizons(pred, fut, system, delta, sA):
    lam = config.lam(system)
    W = config.freeze()["scoring"]["window_lyapunov_times"]
    err = score.err_rel(pred, fut, sA)
    return {k: v["H"] for k, v in score.horizon_all(err, lam, delta, W).items()}


def evaluate(task: Task, m, panel_block):
    sysn, delta = task.system, task.delta
    pnl = data.panel(sysn, panel_block)
    hist, fut = data.frames(pnl, delta)
    F = min(data.n_future_frames(sysn, delta), fut.shape[0] - 1)
    fut = fut[:F + 1]
    sA = task.sA
    sub = int(round(delta / data.DT))
    res, arrays = {}, {}
    if task.arm in ("A", "B", "C", "E"):
        r = task.rollout(m, hist, F, eps_stop=max([0.3] + config.freeze()["scoring"]["eps_secondary"]), fut=fut)
        for k, v in horizons(r["pred"], fut, sysn, delta, sA).items():
            arrays[f"H_{k}"] = v
        res["rollout_frames_run"] = int(r["steps_run"])
        if task.arm == "A":
            for k, v in horizons(r["diag"], fut, sysn, delta, sA).items():
                arrays[f"Hdiag_{k}"] = v
            res["repeat_fraction"] = r["repeat"]
            toks = task.cb.encode(fut.transpose(1, 0, 2))
            res["true_repeat_fraction"] = float((toks[:, 1:] == toks[:, :-1]).mean())
    if task.arm == "D":
        rec = task.reconstruct(m, hist)
        arrays.update(_recon_eval(task, rec, fut, sub, F, "D"))
        res["recon_rmse_rel"] = float(np.sqrt(((rec - fut[0]) ** 2).sum(1).mean()) / sA)
    if task.cb is not None and task.arm in ("A", "D"):
        base = task.cb.C[task.cb.encode(fut[0])]
        res["current_token_rmse_rel"] = float(np.sqrt(((base - fut[0]) ** 2).sum(1).mean()) / sA)
    return res, arrays


def _recon_eval(task, rec, fut, sub, F, prefix):
    tr = integrate_frames(task.system, rec, sub, F)
    arrays = {f"H{prefix}_{k}" if prefix != "D" else f"H_{k}": v
              for k, v in horizons(tr, fut, task.system, task.delta, task.sA).items()}
    arrays[f"recon_{prefix}"] = rec
    return arrays


def run_job(j, device):
    tag = tag_of(j)
    grid_dir = OUT / (j.get("outdir") or ("stall" if j.get("panel") == "validation" else "main")) / tag
    if (grid_dir / "done").exists():
        return "skip"
    grid_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    task = Task(j["system"], j["arm"], j["bits"], j["delta"], j["seed"], device, noise=j.get("noise", 0.0),
                n_traj=j.get("n_traj"), steps=j.get("steps"), backbone=j.get("backbone"))
    m, info = task.train()
    torch.save(m.state_dict(), grid_dir / "model.pt")
    info["job"] = j
    info["sha"] = config.git_sha()
    panel_block = j.get("panel", "confirmation")
    res, arrays = evaluate(task, m, panel_block)
    info["eval"] = res
    info["panel"] = panel_block
    if j["arm"] == "A" and j["bits"] in (4, 6) and j["system"] == "lorenz28" and not j.get("n_traj") \
            and panel_block == "confirmation":
        pnl = data.panel(task.system, "confirmation")
        hist, fut = data.frames(pnl, task.delta)
        F = min(data.n_future_frames(task.system, task.delta), fut.shape[0] - 1)
        fut = fut[:F + 1]
        sub = int(round(task.delta / data.DT))
        h = task.a_hidden(m, hist)
        info["probes"] = {}
        for kind in ("linear", "mlp"):
            pr, pinfo = train_probe(task, m, kind)
            with torch.no_grad():
                rec = task.std.inv(pr(h).double().cpu().numpy())
            pinfo["recon_rmse_rel"] = float(np.sqrt(((rec - fut[0]) ** 2).sum(1).mean()) / task.sA)
            arrays.update(_recon_eval(task, rec, fut, sub, F, f"probe_{kind}"))
            torch.save(pr.state_dict(), grid_dir / f"probe_{kind}.pt")
            info["probes"][kind] = pinfo
    info["wall"] = time.time() - t0
    np.savez_compressed(grid_dir / "eval.npz", **arrays)
    (grid_dir / "info.json").write_text(json.dumps(info, indent=1, default=float))
    (grid_dir / "done").write_text("ok\n")
    return f"{tag} {info['wall']:.0f}s"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "run"])
    ap.add_argument("--grid", default="main")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    J = jobs(a.grid)
    if a.only:
        J = [j for j in J if a.only in tag_of(j)]
    if a.cmd == "list":
        for i, j in enumerate(J):
            print(i, tag_of(j))
        print(len(J), "jobs")
        sys.exit(0)
    for i, j in enumerate(J):
        if i % a.nshards != a.shard:
            continue
        try:
            print(run_job(j, a.device), flush=True)
        except Exception:
            print("FAILED", tag_of(j), flush=True)
            traceback.print_exc()
