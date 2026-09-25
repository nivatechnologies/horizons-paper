"""POST-FREEZE EXTENSION: E5.1 probe control and E5.2 tie baselines on Lorenz-63 rho = 28.

Protocol: ext_freeze.yaml (e5_controls, readings.probe_control) and EXT_FREEZE.md part 1.

Usage (from tokens_horizon/):
  ext_e5_controls.py check  --device cuda:2      weight checks (untrained A determinism, differs from trained)
  ext_e5_controls.py probe  --device cuda:2 [--only TAG]   E5.1 per-model runs (skip-if-done)
  ext_e5_controls.py tie                          E5.2 per-cell arrays (skip-if-done)
  ext_e5_controls.py bsnap  --device cuda:2 [--only TAG]   Amendment 1 A8.1: B re-scored snapped (skip-if-done)
  ext_e5_controls.py report                       CSVs + JSON from the saved arrays

Amendment 1 (f7fedcb) applied: ties reported as P(VPT = T_out | T_out > Delta) and share T_out = Delta (A8.2);
probe reading A8.5 ("training makes the precision more recoverable by the tested readout", read under the frozen
margin); B snapped to the nearest prototype (A8.1). The part-1 tie output is kept as
results/ext/e5_tie_baselines_SUPERSEDED_pre_amendment1.csv and e5.json key superseded_pre_amendment1.
  ext_e5_controls.py all    --device cuda:2

Labels: learned (models, probes, token-history MLP), reference (null) (persistence, random-code),
bound (output-support bound), estimate (differences, tie rates, intervals). Every output is a post-freeze extension.

Additional executor choices (not fixed by the extension freeze, stated here before results):
  * token-history MLP training windows: numpy rng seed model_seed(tag, 'tokhist-data'); validation windows are
    exactly train_probe's (model_seed(system, delta, 'probe-val'), 2,048 windows), validation every 250 steps
    as in train_probe; AdamW weight decay 0.0 as in train_probe; target = the last context frame (t = 0 at eval).
  * random-code forecaster frame 0 is also a random codeword (frame 0 is not scored in the primary score).
  * the frozen probe-control reading is applied to the MLP probe (primary) and reported for the linear probe too.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "12")
os.environ.setdefault("MKL_NUM_THREADS", "12")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "12")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
import torch.nn.functional as F  # noqa: E402
import yaml  # noqa: E402

from th import config, data, score  # noqa: E402
from th import tokenize as _tok  # noqa: E402
from th.learn import Task, model_seed, train_probe, windows  # noqa: E402
from th.models import cosine_lr  # noqa: E402

torch.set_num_threads(12)
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True


def _encode12(self, X):            # cap KD-tree query threads at 12 (library default is all cores)
    shp = X.shape[:-1]
    _, idx = self._tree.query(X.reshape(-1, X.shape[-1]), workers=12)
    return idx.reshape(shp)


def _dist12(self, X):
    shp = X.shape[:-1]
    dd, _ = self._tree.query(X.reshape(-1, X.shape[-1]), workers=12)
    return dd.reshape(shp)


_tok.Codebook.encode = _encode12
_tok.Codebook.dist = _dist12

import t3_learned as T3  # noqa: E402  (after the patch; reuses horizons() and integrate_frames())

SYSTEM = "lorenz28"
EXT = yaml.safe_load((config.PKG / "ext_freeze.yaml").read_text())
E5 = EXT["e5_controls"]
OUT = config.RUNS / "ext" / "e5"
RES = config.RESULTS / "ext"
MAIN = config.RUNS / "learned" / "main"
HEAD = config.RUNS / "headline"
LABEL_EXT = "post-freeze extension"
KINDS = ("linear", "mlp")


def a_tag(bits, delta, seed):
    return f"{SYSTEM}_A_b{bits}_D{delta}_s{seed}"


def eval_setup(task):
    pnl = data.panel(SYSTEM, "confirmation")
    hist, fut = data.frames(pnl, task.delta)
    Fn = min(data.n_future_frames(SYSTEM, task.delta), fut.shape[0] - 1)
    fut = fut[:Fn + 1]
    sub = int(round(task.delta / data.DT))
    return hist, fut, sub, Fn


def recon_rmse(rec, x0, sA):
    return float(np.sqrt(((rec - x0) ** 2).sum(1).mean()) / sA)


def recon_horizons(task, rec, fut, sub, Fn):
    tr = T3.integrate_frames(SYSTEM, rec, sub, Fn)
    return T3.horizons(tr, fut, SYSTEM, task.delta, task.sA)


# ------------------------------------------------------------------ token-history baseline
class TokHistMLP(nn.Module):
    def __init__(self, k, K, d, hidden=256):
        super().__init__()
        self.K = K
        self.net = nn.Sequential(nn.Linear(k * K, hidden), nn.GELU(), nn.Linear(hidden, hidden), nn.GELU(),
                                 nn.Linear(hidden, d))

    def forward(self, tok):                      # tok (B, k) long
        x = F.one_hot(tok, self.K).float().flatten(1)
        return self.net(x)


def train_tokhist(task, steps=3000, lr=1e-3, batch=256):
    dev = task.device
    torch.manual_seed(model_seed(task.tag, "tokhist"))
    net = TokHistMLP(task.L, task.cb.K, task.d).to(dev)
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=0.0)
    rng = np.random.default_rng(model_seed(task.tag, "tokhist-data"))
    vrng = np.random.default_rng(model_seed(task.system, task.delta, "probe-val"))
    Wv = windows(task.Tva, task.delta, task.L, 2048, vrng)

    def xy(W):
        tok = torch.as_tensor(task.cb.encode(W[:, :-1]), device=dev)       # last k frames ending at "t = 0"
        y = torch.as_tensor(task.std.fwd(W[:, -2]), dtype=torch.float32, device=dev)
        return tok, y

    vb = [xy(Wv[i:i + 256]) for i in range(0, 2048, 256)]
    best, best_state, best_step = float("inf"), None, 0
    for step in range(1, steps + 1):
        for g in opt.param_groups:
            g["lr"] = cosine_lr(step - 1, steps, lr)
        tok, y = xy(windows(task.Ttr, task.delta, task.L, batch, rng))
        loss = F.mse_loss(net(tok), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step % 250 == 0 or step == steps:
            net.eval()
            with torch.no_grad():
                vl = float(np.mean([F.mse_loss(net(t), yy).item() for t, yy in vb]))
            net.train()
            if vl < best:
                best, best_step = vl, step
                best_state = {k: v.detach().clone() for k, v in net.state_dict().items()}
    net.load_state_dict(best_state)
    net.eval()
    return net, dict(best_val=best, best_step=best_step)


# ------------------------------------------------------------------ E5.1
def weights_equal(sd1, sd2):
    return all(torch.equal(sd1[k].cpu(), sd2[k].cpu()) for k in sd1)


def weight_check(task):
    m1 = task.build()
    m2 = task.build()
    sd1, sd2 = m1.state_dict(), m2.state_dict()
    trained = torch.load(MAIN / task.tag / "model.pt", map_location="cpu")
    same_keys = set(sd1) == set(trained)
    n_diff = sum(not torch.equal(sd1[k].cpu(), trained[k].cpu()) for k in sd1 if k in trained)
    maxabs = max(float((sd1[k].cpu() - trained[k].cpu()).abs().max()) for k in sd1 if k in trained)
    return dict(deterministic=weights_equal(sd1, sd2), keys_match_trained=same_keys,
                tensors_differing_from_trained=int(n_diff), tensors_total=len(sd1),
                max_abs_diff_from_trained=maxabs), m1


def run_probe_job(bits, delta, seed, device):
    tag = a_tag(bits, delta, seed)
    p = OUT / f"probe_{tag}.npz"
    if p.exists():
        return f"skip {tag}"
    t0 = time.time()
    task = Task(SYSTEM, "A", bits, delta, seed, device)
    assert task.tag == tag
    chk, m = weight_check(task)
    assert chk["deterministic"] and chk["tensors_differing_from_trained"] > 0, chk
    m.eval()
    hist, fut, sub, Fn = eval_setup(task)
    x0 = fut[0]
    arrays, info = {}, dict(tag=tag, weight_check=chk, label=LABEL_EXT, sha=config.git_sha())
    with torch.no_grad():
        h = task.a_hidden(m, hist)
    info["untrained_probes"] = {}
    for kind in KINDS:
        pr, pinfo = train_probe(task, m, kind)
        with torch.no_grad():
            rec = task.std.inv(pr(h).double().cpu().numpy())
        pinfo["recon_rmse_rel"] = recon_rmse(rec, x0, task.sA)
        info["untrained_probes"][kind] = pinfo
        arrays[f"recon_untrained_{kind}"] = rec
        for k, v in recon_horizons(task, rec, fut, sub, Fn).items():
            arrays[f"Huntrained_{kind}_{k}"] = v
        print(f"  {tag} untrained {kind}: rmse {pinfo['recon_rmse_rel']:.4f} "
              f"H {arrays[f'Huntrained_{kind}_eps0.3_future'].mean():.3f}", flush=True)
    del m, h
    net, tinfo = train_tokhist(task)
    tok = torch.as_tensor(task.cb.encode(hist[-task.L:].transpose(1, 0, 2)), device=task.device)
    with torch.no_grad():
        rec = task.std.inv(torch.cat([net(tok[i:i + 500]) for i in range(0, len(tok), 500)]).double().cpu().numpy())
    tinfo["recon_rmse_rel"] = recon_rmse(rec, x0, task.sA)
    info["tokhist"] = tinfo
    arrays["recon_tokhist"] = rec
    for k, v in recon_horizons(task, rec, fut, sub, Fn).items():
        arrays[f"Htokhist_{k}"] = v
    print(f"  {tag} tokhist: rmse {tinfo['recon_rmse_rel']:.4f} H {arrays['Htokhist_eps0.3_future'].mean():.3f}",
          flush=True)
    info["wall"] = time.time() - t0
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"probe_{tag}.json").write_text(json.dumps(info, indent=1, default=float))
    np.savez_compressed(p, **arrays)          # written last: its existence marks the job done
    return f"{tag} {info['wall']:.0f}s"


def probe_jobs():
    return [(c["bits"], c["delta"], s) for c in E5["probe_control"]["cells"] for s in E5["probe_control"]["seeds"]]


def check_trained_pipeline(device):
    """Sanity check: re-evaluating a saved trained-A probe with this script's pipeline reproduces info.json."""
    bits, delta, seed = 4, 0.05, 0
    tag = a_tag(bits, delta, seed)
    task = Task(SYSTEM, "A", bits, delta, seed, device)
    m = task.build()
    m.load_state_dict(torch.load(MAIN / tag / "model.pt", map_location=device))
    m.eval()
    hist, fut, sub, Fn = eval_setup(task)
    from th.models import Probe
    info = json.loads((MAIN / tag / "info.json").read_text())
    ev = np.load(MAIN / tag / "eval.npz")
    with torch.no_grad():
        h = task.a_hidden(m, hist)
    out = {}
    for kind in KINDS:
        pr = Probe(kind, task.d).to(device)
        pr.load_state_dict(torch.load(MAIN / tag / f"probe_{kind}.pt", map_location=device))
        pr.eval()
        with torch.no_grad():
            rec = task.std.inv(pr(h).double().cpu().numpy())
        Hk = recon_horizons(task, rec, fut, sub, Fn)["eps0.3_future"]
        out[kind] = dict(rmse_now=recon_rmse(rec, fut[0], task.sA), rmse_saved=info["probes"][kind]["recon_rmse_rel"],
                         H_now=float(Hk.mean()), H_saved=float(ev[f"Hprobe_{kind}_eps0.3_future"].mean()),
                         max_abs_recon_diff=float(np.abs(rec - ev[f"recon_probe_{kind}"]).max()))
    return out


# ------------------------------------------------------------------ E5.2
def tie_cell(bits, delta):
    p = OUT / f"tie_b{bits}_D{delta}.npz"
    if p.exists():
        return f"skip tie b{bits} D{delta}"
    hz = np.load(HEAD / f"{SYSTEM}_b{bits}_D{delta}_dt0.01_M1500.npz")
    cb = _tok.kmeans_codebook(SYSTEM, bits)
    sA = data.sigma_A(SYSTEM)
    lam = config.lam(SYSTEM)
    W = config.freeze()["scoring"]["window_lyapunov_times"]
    pnl = data.panel(SYSTEM, "confirmation")
    Fn = data.n_future_frames(SYSTEM, delta)
    _, fut = data.frames(pnl, delta, n_after=Fn)
    assert pnl["sha"] == str(hz["panel_sha"]) and np.allclose(fut[0], hz["x0"])
    Hb = hz["H_bound_eps0.3_future"]
    # recompute the bound as a check on the frame grid used here
    Hb_chk, _ = score.horizon(cb.dist(fut) / sA, lam, delta, W, 0.3, 1)
    assert np.array_equal(Hb_chk, Hb)
    Hrc = []
    for draw in range(5):
        rng = np.random.default_rng(4242 + bits * 100 + int(round(100 * delta)) + draw)
        idx = rng.integers(0, cb.K, size=fut.shape[:2])
        Hd, _ = score.horizon(score.err_rel(cb.C[idx], fut, sA), lam, delta, W, 0.3, 1)
        Hrc.append(Hd)
    HA = []
    for s in (0, 1, 2):
        ev = np.load(MAIN / a_tag(bits, delta, s) / "eval.npz")
        HA.append(ev["H_eps0.3_future"])
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(p, H_bound=Hb, dC0=hz["dC0"], H_persistence=hz["H_persistence_eps0.3_future"],
                        H_random_code=np.array(Hrc), H_A=np.array(HA), lam=lam, W=W, delta=delta, bits=bits)
    return f"tie b{bits} D{delta} done"


# ------------------------------------------------------------------ report
def boot_ci(H):
    m, lo, hi = score.bootstrap_mean(H)
    return m, lo, hi


def _pd(a, b):
    pd = score.paired_diff(a, b)
    return dict(diff=pd["diff"], ci90=list(pd["ci90"]), ci95=list(pd["ci95"]), reading=score.reading(pd))


def report():
    sha = config.git_sha()
    RES.mkdir(parents=True, exist_ok=True)
    out = dict(label=LABEL_EXT, git_sha=sha,
               protocol="ext_freeze.yaml e5_controls + amendment_1; EXT_FREEZE.md part 1 + Amendment 1 (f7fedcb)",
               probe_control={})
    rows = []
    rule_mlp_all, rule_lin_all, complete = True, True, True
    for c in E5["probe_control"]["cells"]:
        bits, delta = c["bits"], c["delta"]
        cell = f"b{bits}_D{delta}"
        seeds = E5["probe_control"]["seeds"]
        H, R = {}, {}
        missing = [s for s in seeds if not (OUT / f"probe_{a_tag(bits, delta, s)}.npz").exists()]
        if missing:
            complete = False
            out["probe_control"][cell] = dict(status=f"missing seeds {missing}")
            continue
        for s in seeds:
            tag = a_tag(bits, delta, s)
            ev = np.load(MAIN / tag / "eval.npz")
            info = json.loads((MAIN / tag / "info.json").read_text())
            z = np.load(OUT / f"probe_{tag}.npz")
            zi = json.loads((OUT / f"probe_{tag}.json").read_text())
            for kind in KINDS:
                H.setdefault(f"trained_{kind}", []).append(ev[f"Hprobe_{kind}_eps0.3_future"])
                R.setdefault(f"trained_{kind}", []).append(info["probes"][kind]["recon_rmse_rel"])
                H.setdefault(f"untrained_{kind}", []).append(z[f"Huntrained_{kind}_eps0.3_future"])
                R.setdefault(f"untrained_{kind}", []).append(zi["untrained_probes"][kind]["recon_rmse_rel"])
            H.setdefault("tokhist", []).append(z["Htokhist_eps0.3_future"])
            R.setdefault("tokhist", []).append(zi["tokhist"]["recon_rmse_rel"])
        H = {k: np.array(v) for k, v in H.items()}
        cj = dict(forecasters={}, paired={}, weight_checks={})
        for k in H:
            m, lo, hi = boot_ci(H[k])
            cj["forecasters"][k] = dict(label="learned", recon_rmse_rel_per_seed=R[k], H_restricted_mean=m,
                                        ci95=[lo, hi], H_per_seed=[float(x) for x in H[k].mean(1)])
            for s, r, hs in zip(seeds, R[k], H[k].mean(1)):
                rows.append(dict(kind="per_seed", cell=cell, bits=bits, delta=delta, forecaster=k, seed=s,
                                 label="learned", recon_rmse_rel=r, H_restricted_mean=float(hs), ci95_lo="",
                                 ci95_hi="", reading=""))
            rows.append(dict(kind="pooled", cell=cell, bits=bits, delta=delta, forecaster=k, seed="0-2",
                             label="learned", recon_rmse_rel=float(np.mean(R[k])), H_restricted_mean=m,
                             ci95_lo=lo, ci95_hi=hi, reading=""))
        for kind in KINDS:
            worse_every = bool(all(u > t for u, t in zip(R[f"untrained_{kind}"], R[f"trained_{kind}"])))
            pdu = _pd(H[f"untrained_{kind}"], H[f"trained_{kind}"])
            well_below = "a well below b" in pdu["reading"]
            # Amendment 1 A8.5: "trained probe beats untrained probe" read under the frozen margin
            # (untrained well below trained); the 95% interval excluding zero is reported beside it.
            beats = well_below
            cj["paired"][f"untrained_{kind}_minus_trained_{kind}"] = dict(
                pdu, label="estimate", untrained_worse_recon_every_seed=worse_every,
                trained_beats_untrained_frozen_margin=beats,
                trained_higher_ci95_excludes_zero=bool(pdu["ci95"][1] < 0),
                part1_rule_holds_superseded=bool(well_below and worse_every))
            if kind == "mlp":
                rule_mlp_all &= beats
            else:
                rule_lin_all &= beats
            rows.append(dict(kind="paired_diff", cell=cell, bits=bits, delta=delta,
                             forecaster=f"untrained_{kind} - trained_{kind}", seed="0-2", label="estimate",
                             recon_rmse_rel=f"untrained worse every seed: {worse_every}",
                             H_restricted_mean=pdu["diff"], ci95_lo=pdu["ci95"][0], ci95_hi=pdu["ci95"][1],
                             reading="; ".join(pdu["reading"]) + f" | ci90 [{pdu['ci90'][0]:.3f}, {pdu['ci90'][1]:.3f}]"))
        pdt = _pd(H["tokhist"], H["trained_mlp"])
        cj["paired"]["tokhist_minus_trained_mlp"] = dict(pdt, label="estimate")
        rows.append(dict(kind="paired_diff", cell=cell, bits=bits, delta=delta, forecaster="tokhist - trained_mlp",
                         seed="0-2", label="estimate", recon_rmse_rel="", H_restricted_mean=pdt["diff"],
                         ci95_lo=pdt["ci95"][0], ci95_hi=pdt["ci95"][1],
                         reading="; ".join(pdt["reading"]) + f" | ci90 [{pdt['ci90'][0]:.3f}, {pdt['ci90'][1]:.3f}]"))
        for s in seeds:
            zi = json.loads((OUT / f"probe_{a_tag(bits, delta, s)}.json").read_text())
            cj["weight_checks"][str(s)] = zi["weight_check"]
        out["probe_control"][cell] = cj
    rule_text = EXT["amendment_1"]["probe_reading"]
    A85 = "training makes the precision more recoverable by the tested readout"
    per_cell = {k: {kind: v["paired"][f"untrained_{kind}_minus_trained_{kind}"]["trained_beats_untrained_frozen_margin"]
                    for kind in KINDS} for k, v in out["probe_control"].items() if "paired" in v}
    out["probe_control_reading"] = dict(
        frozen_rule=rule_text, amendment="Amendment 1 A8.5 (f7fedcb); replaces the part-1 reading",
        beats_definition="untrained-A probe well below trained-A probe on horizon under the frozen margin",
        applied_to="MLP probe (primary); linear probe reported beside",
        all_cells_mlp=rule_mlp_all if complete else None, all_cells_linear=rule_lin_all if complete else None,
        per_cell=per_cell,
        permitted_sentence_per_cell={k: {kind: (A85 if b else "no A8.5 sentence for this readout")
                                         for kind, b in d.items()} for k, d in per_cell.items()},
        never_say="the untrained representation lacks it", label="estimate")
    _write_csv(RES / "e5_probe_control.csv", rows, sha)
    sup = OUT / "superseded_pre_amendment1.json"
    if sup.exists():
        out["superseded_pre_amendment1"] = json.loads(sup.read_text())
    tie_report(out, sha)
    bsnap_report(out, sha)
    (RES / "e5.json").write_text(json.dumps(out, indent=1, default=float))
    return out


def _tie_stats(Hf, Hb, lam, delta, per_draw_avg=False):
    """Amendment 1 A8.2. Hf (S, n) forecaster, Hb (n,) bound; future frames, eps 0.3.

    Returns unconditional tie rate, P(VPT = T_out | T_out > Delta), share with T_out = Delta (all with
    bootstrap intervals; states, and seeds when S > 1 and not per_draw_avg) and the restricted mean."""
    Hf = np.atleast_2d(Hf)
    jb = np.rint(Hb / (lam * delta)).astype(int)          # bound's first crossing frame (W-capped states large)
    first = jb == 1
    ties = (Hf == Hb[None]).astype(float)
    red = (lambda A: A.mean(0)) if per_draw_avg else (lambda A: A)
    t_all = boot_ci(red(ties))
    t_cond = boot_ci(red(ties[:, ~first]))
    share = boot_ci(first.astype(float))
    Hm = boot_ci(red(Hf))
    return dict(tie_rate_all=t_all, tie_rate_given_Tout_gt_Delta=t_cond, share_Tout_eq_Delta=share,
                n=int(len(Hb)), n_Tout_gt_Delta=int((~first).sum()), H_restricted_mean=Hm)


def _tie_rows(rows, cell, bits, delta, name, seed, label, st):
    rows.append(dict(cell=cell, bits=bits, delta=delta, forecaster=name, seed=seed, label=label,
                     n=st["n"], n_Tout_gt_Delta=st["n_Tout_gt_Delta"],
                     share_Tout_eq_Delta=st["share_Tout_eq_Delta"][0],
                     share_ci95_lo=st["share_Tout_eq_Delta"][1], share_ci95_hi=st["share_Tout_eq_Delta"][2],
                     tie_given_Tout_gt_Delta=st["tie_rate_given_Tout_gt_Delta"][0],
                     tie_cond_ci95_lo=st["tie_rate_given_Tout_gt_Delta"][1],
                     tie_cond_ci95_hi=st["tie_rate_given_Tout_gt_Delta"][2],
                     tie_all=st["tie_rate_all"][0], tie_all_ci95_lo=st["tie_rate_all"][1],
                     tie_all_ci95_hi=st["tie_rate_all"][2], H_restricted_mean=st["H_restricted_mean"][0],
                     H_ci95_lo=st["H_restricted_mean"][1], H_ci95_hi=st["H_restricted_mean"][2],
                     stat_label="estimate"))


def tie_report(out, sha):
    trows = []
    out["tie_baselines_a8_2"] = dict(amendment="Amendment 1 A8.2 (f7fedcb)", definition=EXT["amendment_1"]["e5_ties"])
    for c in E5["tie_baselines"]["cells"]:
        bits, delta = c["bits"], c["delta"]
        p = OUT / f"tie_b{bits}_D{delta}.npz"
        if not p.exists():
            continue
        z = np.load(p)
        Hb, lam = z["H_bound"], float(z["lam"])
        cell = f"b{bits}_D{delta}"
        cj = dict(p0=float((z["dC0"] > 0.3).mean()), bound=dict(label="bound", H_restricted_mean=boot_ci(Hb)))
        trows.append(dict(cell=cell, bits=bits, delta=delta, forecaster="bound", seed="", label="bound",
                          n=len(Hb), H_restricted_mean=cj["bound"]["H_restricted_mean"][0],
                          H_ci95_lo=cj["bound"]["H_restricted_mean"][1], H_ci95_hi=cj["bound"]["H_restricted_mean"][2]))
        st = _tie_stats(z["H_persistence"], Hb, lam, delta)
        cj["persistence"] = dict(label="reference (null)", **st)
        _tie_rows(trows, cell, bits, delta, "persistence", "", "reference (null)", st)
        st = _tie_stats(z["H_random_code"], Hb, lam, delta, per_draw_avg=True)
        cj["random_code"] = dict(label="reference (null)", draws="0-4 averaged per state", **st)
        _tie_rows(trows, cell, bits, delta, "random_code", "draws 0-4 averaged", "reference (null)", st)
        cj["A"] = dict(label="learned")
        for s in range(3):
            st = _tie_stats(z["H_A"][s], Hb, lam, delta)
            cj["A"][f"seed{s}"] = st
            _tie_rows(trows, cell, bits, delta, "A", str(s), "learned", st)
        st = _tie_stats(z["H_A"], Hb, lam, delta)
        cj["A"]["pooled"] = st
        _tie_rows(trows, cell, bits, delta, "A", "0-2 pooled", "learned", st)
        cj["note"] = "tie rates and shares are estimates; horizons carry the forecaster's label; (point, lo95, hi95)"
        out["tie_baselines_a8_2"][cell] = cj
    _write_csv(RES / "e5_tie_baselines.csv", trows, sha,
               extra="# Amendment 1 A8.2: P(VPT = T_out | T_out > Delta), share T_out = Delta, unconditional tie")


# ------------------------------------------------------------------ A8.1: B snapped to nearest prototype
def b_tag(bits, delta, seed):
    return f"{SYSTEM}_B_b{bits}_D{delta}_s{seed}"


def b_jobs():
    fz = config.freeze()
    J = []
    for b in (4, 6, 8, 10):
        for d in fz["scoring"]["frame_intervals"]:
            for s in fz["seeds"]["model_seeds"] + (fz["seeds"]["headline_extra_model_seeds"]
                                                   if (d == 0.02 and b in (4, 6)) else []):
                J.append((b, d, s))
    return J


@torch.no_grad()
def b_rollout_snap(task, m, hist, n_future, fut, eps_stop, chunk=500):
    """Replica of Task._rollout_chunk for arm B (same greedy loop, same fed-back nearest codes), also recording
    the nearest-prototype snap of each output. Stops only once BOTH outputs have exceeded eps_stop for every
    state, so neither output's first crossings are truncated."""
    L = task.L
    ctx = hist[-L:]
    n = ctx.shape[1]
    d = ctx.shape[2]
    P = np.full((n_future + 1, n, d), np.nan)
    S = P.copy()
    run = 0
    for c0 in range(0, n, chunk):
        c1 = min(n, c0 + chunk)
        seq = torch.as_tensor(task.cb.encode(ctx[:, c0:c1].transpose(1, 0, 2)), device=task.device)
        P[0, c0:c1] = task.cb.C[seq[:, -1].cpu().numpy()]
        S[0, c0:c1] = P[0, c0:c1]
        dead = np.zeros(c1 - c0, bool)
        dead_s = np.zeros(c1 - c0, bool)
        for j in range(1, n_future + 1):
            out = m(seq)[:, -1]
            x = task.std.inv(out.double().cpu().numpy())
            P[j, c0:c1] = x
            tok = task.cb.encode(x)
            S[j, c0:c1] = task.cb.C[tok]
            seq = torch.cat([seq[:, 1:], torch.as_tensor(tok, device=task.device)[:, None]], 1)
            f = fut[j, c0:c1]
            dead |= np.linalg.norm(P[j, c0:c1] - f, axis=-1) / task.sA > eps_stop
            dead_s |= np.linalg.norm(S[j, c0:c1] - f, axis=-1) / task.sA > eps_stop
            if dead.all() and dead_s.all():
                break
        run = max(run, j)
    return P, S, run


def bsnap_job(bits, delta, seed, device):
    tag = b_tag(bits, delta, seed)
    p = OUT / f"b_snapped_{tag}.npz"
    if p.exists():
        return f"skip {tag}"
    t0 = time.time()
    task = Task(SYSTEM, "B", bits, delta, seed, device)
    assert task.tag == tag
    m = task.build()
    m.load_state_dict(torch.load(MAIN / tag / "model.pt", map_location=device))
    m.eval()
    hist, fut, sub, Fn = eval_setup(task)
    eps_stop = max([0.3] + config.freeze()["scoring"]["eps_secondary"])
    P, S, run = b_rollout_snap(task, m, hist, Fn, fut, eps_stop)
    HB = T3.horizons(P, fut, SYSTEM, delta, task.sA)
    HS = T3.horizons(S, fut, SYSTEM, delta, task.sA)
    ev = np.load(MAIN / tag / "eval.npz")
    repro = {k: bool(np.array_equal(HB[k], ev[f"H_{k}"])) for k in HB}
    maxdiff = {k: float(np.abs(HB[k] - ev[f"H_{k}"]).max()) for k in HB}
    arrays = {f"HB_{k}": v for k, v in HB.items()}
    arrays.update({f"HBsnap_{k}": v for k, v in HS.items()})
    OUT.mkdir(parents=True, exist_ok=True)
    info = dict(tag=tag, label=LABEL_EXT, sha=config.git_sha(), frames_run=run, reproduces_stored_H=repro,
                max_abs_diff_stored_H=maxdiff, wall=time.time() - t0)
    (OUT / f"b_snapped_{tag}.json").write_text(json.dumps(info, indent=1, default=float))
    np.savez_compressed(p, **arrays)
    return f"{tag} {info['wall']:.0f}s repro={all(repro.values())} H_B={HB['eps0.3_future'].mean():.3f} " \
           f"H_snap={HS['eps0.3_future'].mean():.3f}"


def bsnap_report(out, sha):
    rows = []
    res = dict(amendment="Amendment 1 A8.1 (f7fedcb)", definition=EXT["amendment_1"]["e5_b_snapped"], cells={})
    lam = config.lam(SYSTEM)
    by_cell = {}
    for b, d, s in b_jobs():
        by_cell.setdefault((b, d), []).append(s)
    for (bits, delta), seeds in by_cell.items():
        files = [OUT / f"b_snapped_{b_tag(bits, delta, s)}.npz" for s in seeds]
        if not all(f.exists() for f in files):
            res["cells"][f"b{bits}_D{delta}"] = dict(status="incomplete")
            continue
        Z = [np.load(f) for f in files]
        infos = [json.loads(f.with_suffix(".json").read_text()) for f in files]
        hz = np.load(HEAD / f"{SYSTEM}_b{bits}_D{delta}_dt0.01_M1500.npz")
        cell = f"b{bits}_D{delta}"
        cj = dict(seeds=seeds, reproduces_stored_H_all=all(all(i["reproduces_stored_H"].values()) for i in infos))
        # outlast check at every eps and start (must be 0)
        outl = {}
        for k in [x[3:] for x in Z[0].files if x.startswith("HB_")]:
            Hs = np.array([z[f"HBsnap_{k}"] for z in Z])
            outl[k] = float((Hs > hz[f"H_bound_{k}"][None]).mean())
        cj["outlast_snapped_over_bound"] = outl
        if any(v > 0 for v in outl.values()):
            raise RuntimeError(f"A8.1 STOP: snapped-B outlasts the bound in {cell}: {outl}")
        for tagk in ("eps0.3_future", "eps0.3_from_t0"):
            HB = np.array([z[f"HB_{tagk}"] for z in Z])
            HS = np.array([z[f"HBsnap_{tagk}"] for z in Z])
            Hb = hz[f"H_bound_{tagk}"]
            e = dict(B=boot_ci(HB), B_snapped=boot_ci(HS), bound=boot_ci(Hb),
                     B_per_seed=HB.mean(1).tolist(), B_snapped_per_seed=HS.mean(1).tolist(),
                     snapped_minus_B=_pd(HS, HB), snapped_minus_bound=_pd(HS, Hb))
            if tagk == "eps0.3_future":
                e["ties_snapped"] = _tie_stats(HS, Hb, lam, delta)
                e["ties_B"] = _tie_stats(HB, Hb, lam, delta)
            cj[tagk] = e
            for name, lab, v in (("B", "learned", e["B"]), ("B_snapped", "learned", e["B_snapped"]),
                                 ("bound", "bound", e["bound"])):
                r = dict(cell=cell, bits=bits, delta=delta, score=tagk, row=name, seeds=len(seeds), label=lab,
                         value=v[0], ci95_lo=v[1], ci95_hi=v[2], reading="")
                if name != "bound" and tagk == "eps0.3_future":
                    t = e["ties_snapped" if name == "B_snapped" else "ties_B"]
                    r.update(tie_given_Tout_gt_Delta=t["tie_rate_given_Tout_gt_Delta"][0],
                             tie_cond_ci95_lo=t["tie_rate_given_Tout_gt_Delta"][1],
                             tie_cond_ci95_hi=t["tie_rate_given_Tout_gt_Delta"][2],
                             share_Tout_eq_Delta=t["share_Tout_eq_Delta"][0], tie_all=t["tie_rate_all"][0])
                if name == "B_snapped":
                    r["outlast_over_bound"] = outl[tagk]
                rows.append(r)
            for name, pdx in (("B_snapped - B", e["snapped_minus_B"]), ("B_snapped - bound", e["snapped_minus_bound"])):
                rows.append(dict(cell=cell, bits=bits, delta=delta, score=tagk, row=name, seeds=len(seeds),
                                 label="estimate", value=pdx["diff"], ci95_lo=pdx["ci95"][0], ci95_hi=pdx["ci95"][1],
                                 reading="; ".join(pdx["reading"]) +
                                         f" | ci90 [{pdx['ci90'][0]:.3f}, {pdx['ci90'][1]:.3f}]"))
        res["cells"][cell] = cj
    out["b_snapped_a8_1"] = res
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    rows = [{k: r.get(k, "") for k in keys} for r in rows]
    _write_csv(RES / "e5_b_snapped.csv", rows, sha, extra="# Amendment 1 A8.1: B outputs snapped to nearest prototype")


def _write_csv(path, rows, sha, extra=None):
    import csv
    import io
    buf = io.StringIO()
    if rows:
        keys = list(dict.fromkeys(k for r in rows for k in r))
        w = csv.DictWriter(buf, fieldnames=keys, restval="")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})
    head = f"# git_sha={sha}; POST-FREEZE EXTENSION\n" + (extra + "\n" if extra else "")
    path.write_text(head + buf.getvalue())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "probe", "tie", "bsnap", "report", "all"])
    ap.add_argument("--device", default="cuda:2")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    if a.cmd == "check":
        t = Task(SYSTEM, "A", 4, 0.05, 0, a.device)
        print(json.dumps(weight_check(t)[0], indent=1))
        print(json.dumps(check_trained_pipeline(a.device), indent=1))
    if a.cmd in ("probe", "all"):
        for bits, delta, s in probe_jobs():
            if a.only and a.only not in a_tag(bits, delta, s):
                continue
            print(run_probe_job(bits, delta, s, a.device), flush=True)
    if a.cmd in ("tie", "all"):
        for c in E5["tie_baselines"]["cells"]:
            print(tie_cell(c["bits"], c["delta"]), flush=True)
    if a.cmd in ("bsnap", "all"):
        for bits, delta, s in b_jobs():
            if a.only and a.only not in b_tag(bits, delta, s):
                continue
            print(bsnap_job(bits, delta, s, a.device), flush=True)
    if a.cmd in ("report", "all"):
        report()
        print("report written", flush=True)
