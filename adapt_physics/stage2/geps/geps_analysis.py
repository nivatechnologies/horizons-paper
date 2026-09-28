"""GEPS as a learned adaptive opponent: scoring, frozen reading, tables and the results-note section (geps_freeze.yaml).

Inputs: runs/geps_eval/geps_range_s0/<panel>_<tag>.npz|json, copied from the Sparks (runs/geps_range_s0/eval/), timing
JSONs (timing_adapt<steps>.json) and the training logs/info; Part A arms from runs/s2_eval and runs/obj_eval.
Scope (Todd 2026-09-28): the first N = 50 states of s2_test_Re50_D and s2_test_Re56_D; GEPS-range at 500 and 5,000
adaptation steps; no-adaptation at Re 50. Horizons at w = 11 on future frames, eps 0.1 (primary) and 0.3.

Reading (frozen): at Re 50 AND Re 56, H - GEPS-range at the better of its two budgets (chosen per Re: the higher GEPS
restricted mean) >= 0.25 with the 95% interval excluding 0 -> "A learned adapter built for parametric PDEs does not
close the gap": STATED; otherwise GEPS is reported prominently and Todd decides the headline. A cell still missing ->
reading PENDING. Interval: paired bootstrap over trajectories (same resampled states for both arms); H has 3 seeds, so the
crossed scheme (seed columns resampled too; the primary scheme since the post-freeze change) is primary and the
interval conditional on the trained models is beside; GEPS has one seed.

Writes stage2/geps/results/geps_rows.csv, geps_reading.csv, geps_timing.csv, geps_training.csv, results_note_geps.md.
Usage: python stage2/geps/geps_analysis.py
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
PKG = HERE.parents[2]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(PKG / "stage2" / "scripts"))
from ap import config  # noqa: E402
from s2_analysis import boot_all, boot_idx, q  # noqa: E402
from th import score  # noqa: E402

N = 50
RUN = "geps_range_s0_lr0.001"     # published lr 1e-2 collapsed to persistence (archived, never evaluated); deviation
GEV = config.RUNS / "geps_eval" / RUN
S2EV = config.RUNS / "s2_eval"
OEV = config.RUNS / "obj_eval"
RES = HERE.parent / "results"
DELTA = 0.35
MARGIN = 0.25
STEP_MATCHED_EPOCHS = 2500      # 640,000 published steps (20,000 epochs x 32 steps) / 256 steps per epoch on our data
CLIP_CAVEAT = ("Every GEPS run trained unclipped: the released train.py:158 calls clip_grad_norm_ after optimizer.zero_grad() "
               "(train.py:157), so clipping never applies, and the wrapper copies that order. The published lr 1e-2 was not "
               "tested with working clipping, so this result cannot tell whether GEPS needs the lower lr (1e-3, used here) "
               "or only working clipping.")
TP = json.loads((PKG / "stage2" / "results" / "test_panels.json").read_text())
rng = np.random.default_rng(2809)
IDX = boot_idx(N, seed=2809)

GEPS_CELLS = [("GEPS_range_adapt500", "adapt500"), ("GEPS_range_adapt5000", "adapt5000"), ("GEPS_range_noadapt", "noadapt")]
PARTA = [("H", S2EV, "H_s{s}_std_11.npz", (0, 1, 2)), ("O", S2EV, "O_s0_std_11.npz", (0,)),
         ("persistence", S2EV, "persistence_s0_std_11.npz", (0,)), ("L0", S2EV, "L0_s{s}_std_11.npz", (0, 1, 2)),
         ("L_range", S2EV, "L_range_s{s}_std_11.npz", (0, 1, 2)), ("L_range_wide", S2EV, "L_range_wide_s0_std_11.npz", (0,)),
         ("FNO_Re_true", OEV, "FNO_Re_true_s{s}_11.npz", (0, 1, 2)), ("FNO_Re_id", OEV, "FNO_Re_id_s{s}_11.npz", (0, 1, 2)),
         ("L_ft", OEV, "L_ft_s0_11.npz", (0,))]


def horizons(files, lam, eps):
    Z = [np.load(f)["err"].astype(float)[:, :N] for f in files]
    out = [score.horizon(e, lam, DELTA, 10.0, eps, 1) for e in Z]
    return np.stack([o[0] for o in out]), np.stack([o[1] for o in out])


def arm_files(Re, arm):
    panel = f"s2_test_Re{Re}_D"
    for name, tag in GEPS_CELLS:
        if arm == name:
            f = GEV / f"{panel}_{tag}_states0-{N}.npz"
            return [f] if f.exists() else []
    for name, root, pat, seeds in PARTA:
        if arm == name:
            fs = [root / panel / pat.format(s=s) for s in seeds]
            return fs if all(f.exists() for f in fs) else []
    return []


def write(name, rows, note):
    if not rows:
        return
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    RES.mkdir(parents=True, exist_ok=True)
    with open(RES / name, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics GEPS WO; {note}\n")
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main():
    rows, reading, H = [], [], {}
    for Re in (50, 56):
        panel = f"s2_test_Re{Re}_D"
        lam = TP[panel]["lam"]
        fo = arm_files(Re, "O")
        Ho01 = horizons(fo, lam, 0.1)[0]
        for arm in [a for a, _ in GEPS_CELLS] + [a for a, *_ in PARTA]:
            fs = arm_files(Re, arm)
            if not fs:
                continue
            for eps in (0.1, 0.3):
                Hs, Cs = horizons(fs, lam, eps)
                H[(Re, arm, eps)] = Hs
                b = boot_all(Hs, IDX, rng)
                Ho = Ho01 if eps == 0.1 else horizons(fo, lam, 0.3)[0]
                geps = arm.startswith("GEPS")
                rows.append(dict(world="D", Re=Re, arm=arm, source="GEPS (this WO)" if geps else "Part A (same states)",
                                 w=11, eps=eps, n=Hs.shape[1], seeds=Hs.shape[0], restricted_mean=float(Hs.mean()),
                                 ci95_lo=q(b["crossed"])[0], ci95_hi=q(b["crossed"])[1],
                                 cond_ci95_lo=q(b["cond"])[0], cond_ci95_hi=q(b["cond"])[1],
                                 S1=float(np.mean(~Cs | (Hs > 1))), S3=float(np.mean(~Cs | (Hs > 3))),
                                 retention=float(Hs.mean() / Ho.mean()),
                                 label="learned opponent (reported)" if geps else "comparator (reported)"))
    TR = next((t for t in training() if t["run"] == RUN), {})
    for Re in (50, 56):
        cells = [a for a in ("GEPS_range_adapt500", "GEPS_range_adapt5000") if (Re, a, 0.1) in H]
        if len(cells) < 2 or (Re, "H", 0.1) not in H:
            reading.append(dict(Re=Re, better_budget="", GEPS=None, GEPS_epochs=TR.get("epochs_trained"),
                                GEPS_undertrained=TR.get("undertrained"), GEPS_val_change_last2=TR.get("val_change_last2"),
                                GEPS_val_change_last2_pct=TR.get("val_change_last2_pct"), H=None, H_minus_GEPS=None, ci95_lo=None, ci95_hi=None,
                                cond_ci95_lo=None, cond_ci95_hi=None, holds_at_this_Re="PENDING",
                                label="reading component (cell not yet evaluated)"))
            continue
        best = max(cells, key=lambda a: H[(Re, a, 0.1)].mean())
        Hh, Hg = H[(Re, "H", 0.1)], H[(Re, best, 0.1)]
        bh, bg = boot_all(Hh, IDX, rng), boot_all(Hg, IDX, rng)
        d = bh["crossed"] - bg["crossed"]
        dc = bh["cond"] - bg["cond"]
        lo, hi = q(d)
        val = float(Hh.mean() - Hg.mean())
        reading.append(dict(Re=Re, better_budget=best.replace("GEPS_range_adapt", ""), GEPS=float(Hg.mean()),
                            GEPS_epochs=TR.get("epochs_trained"), GEPS_undertrained=TR.get("undertrained"),
                            GEPS_val_change_last2=TR.get("val_change_last2"), GEPS_val_change_last2_pct=TR.get("val_change_last2_pct"),
                            H=float(Hh.mean()),
                            H_minus_GEPS=val, ci95_lo=lo, ci95_hi=hi, cond_ci95_lo=q(dc)[0], cond_ci95_hi=q(dc)[1],
                            other_budget_H_minus_GEPS=float(Hh.mean() - H[(Re, [c for c in cells if c != best][0], 0.1)].mean()),
                            holds_at_this_Re=bool(val >= MARGIN and lo > 0), label="reading component"))
    comp = [r["holds_at_this_Re"] for r in reading]
    # Todd 2026-09-28: the claim is not stated whatever the components show. The evaluated GEPS-range trained 35 of about
    # 2,500 step-matched epochs (the WO's 8 h cap: a spec error), so the reading cannot answer its question.
    budget = (f"GEPS-range trained {TR.get('epochs_trained')} of about {STEP_MATCHED_EPOCHS:,} step-matched epochs "
              "(the WO's 8 h cap; a spec error), so the reading cannot answer its question")
    if "PENDING" in comp:
        claim = f"NOT STATED (a reading cell is still pending; in any case {budget})"
    elif all(comp):
        claim = f"NOT STATED: both reading components hold, but {budget}"
    else:
        claim = f"NOT STATED: a reading component fails (GEPS reported prominently), and {budget}"
    reading.append(dict(Re="50 and 56", holds_at_this_Re="PENDING" if "PENDING" in comp else all(comp), claim=claim, caveat=CLIP_CAVEAT,
                        label="frozen reading (decides the claim)"))
    write("geps_rows.csv", rows, f"first N = {N} states, w = 11; Part A arms on the same states")
    write("geps_reading.csv", reading, "frozen reading (H - GEPS-range, better budget per Re)")
    write("geps_timing.csv", timing(), "batch-1 timing on a DGX Spark GB10 (states 3-22 / 3-5 of s2_test_Re50_D)")
    write("geps_training.csv", training(), "GEPS training runs")
    write("geps_followup.csv", followup(reading), "post-freeze follow-up: GEPS-range trained longer (seed 1, Baccus), frozen cells")
    write("geps_repro.csv", repro(), "post-freeze follow-up: released GEPS on its own Kolmogorov data (lr 1e-2)")
    note(rows, reading)
    for r in reading:
        print(r)


def timing():
    out = []
    for steps in (500, 5000):
        f = GEV / f"timing_adapt{steps}.json"
        if f.exists():
            J = json.loads(f.read_text())
            out.append(dict(arm=f"GEPS_range_adapt{steps}", steps=steps, n_timed=J["n_timed"], frames=J["frames"],
                            wall_median=J["wall_median"], wall_p90=J["wall_p90"], adapt_median=J["adapt_median"],
                            forecast_median=J["forecast_median"], forecast_fps=J["forecast_fps"], device=J["device"],
                            torch=J["torch"], label="cost (reported only)"))
    return out


def persistence_val(data):
    """No-change forecast RelativeL2 on the training script's 64 fixed validation windows (collapse reference)."""
    D = config.RUNS / "cache" / "geps_stage"
    sc = 64.0 / json.loads((D / "meta.json").read_text())["sigma40"]
    V = np.load(D / f"val_{data}.npy", mmap_mode="r")
    vr = np.random.default_rng(1)
    vi, vk = vr.integers(0, V.shape[0], 64), vr.integers(0, V.shape[1] - 20 + 1, 64)
    x = np.stack([V[i, k:k + 20] for i, k in zip(vi, vk)]).astype(np.float64).reshape(64, 20, -1) * sc
    p = np.repeat(x[:, :1], 20, 1)
    return float((np.sqrt(((p - x) ** 2).sum((1, 2))) / np.sqrt((x ** 2).sum((1, 2)))).mean())


def training():
    out = []
    for run, data, lr, host, ev in (
            ("ARCHIVED_geps_range_s0_lr0.01_collapsed", "range", 1e-2, "Spark A", "no (collapsed to persistence; archived, never evaluated)"),
            (RUN, "range", 1e-3, "Spark A", "yes"),
            ("geps_range_wide_s0", "range_wide", 1e-2, "Spark B", "no (diverged)"),
            ("geps_range_wide_s0_lr0.001", "range_wide", 1e-3, "Spark B", "no (cut)")):
        d = config.RUNS / "geps_eval" / run
        log = d / "train.log"
        if not log.exists():
            continue
        L = [json.loads(x) for x in log.read_text().splitlines() if x.startswith("{")]
        E = [x for x in L if "epoch" in x]
        vals = [x["val_loss"] for x in E]
        fin = [v for v in vals if v == v]
        info = json.loads((d / "info.json").read_text()) if (d / "info.json").exists() else {}
        pers = persistence_val(data)
        falling = len(fin) >= 3 and fin[-1] < fin[-2] < fin[-3]
        best_ep = E[int(np.nanargmin(np.where(np.isnan(vals), np.inf, vals)))]["epoch"] if fin else None
        out.append(dict(run=run, data=data, lr=lr, host=host, epochs_trained=(info.get("epochs_done") if info else (E[-1]["epoch"] + 1 if E else None)),
                        steps=info.get("steps", E[-1]["steps"] if E else None), best_val=min(fin) if fin else None, best_epoch=best_ep,
                        persistence_val=pers, best_minus_persistence=(min(fin) - pers) if fin else None,
                        val_curve=" ".join(f"{x['epoch']}:{x['val_loss']:.7f}" for x in E),
                        undertrained=falling,
                        val_change_last2=(fin[-1] - fin[-2]) if len(fin) >= 2 else None,
                        val_change_last2_pct=(100 * (fin[-1] - fin[-2]) / fin[-2]) if len(fin) >= 2 else None, diverged=bool(vals and not fin), collapsed=(d / "COLLAPSED").exists() or run.startswith("ARCHIVED"),
                        cap_hours=info.get("cap_hours"), evaluated=ev, label="training (reported)"))
    return out


FOLLOW = config.RUNS / "geps_eval" / "followup_s1_ep130"


def followup(reading):
    """Post-freeze follow-up (not a substitute): seed 1's best-on-validation checkpoint (Baccus) on the frozen reading
    cells, scored exactly as the frozen reading; the frozen value beside."""
    snap = json.loads((FOLLOW / "snapshot.json").read_text()) if (FOLLOW / "snapshot.json").exists() else {}
    froz = {r["Re"]: r for r in reading if r["Re"] in (50, 56)}
    out = []
    for Re in (50, 56):
        panel = f"s2_test_Re{Re}_D"
        lam = TP[panel]["lam"]
        fs = {b: FOLLOW / "eval" / f"{panel}_adapt{b}_states0-{N}.npz" for b in (500, 5000)}
        have = {b: f for b, f in fs.items() if f.exists()}
        if not have:
            continue
        Hh, _ = horizons(arm_files(Re, "H"), lam, 0.1)
        Hs = {b: horizons([f], lam, 0.1)[0] for b, f in have.items()}
        best = max(Hs, key=lambda b: Hs[b].mean())
        bh, bg = boot_all(Hh, IDX, rng), boot_all(Hs[best], IDX, rng)
        lo, hi = q(bh["crossed"] - bg["crossed"])
        fr = froz.get(Re, {})
        out.append(dict(Re=Re, checkpoint=f"seed 1, epoch {snap.get('epoch')}", val_loss=snap.get("val_loss"),
                        budgets_done=",".join(map(str, sorted(have))), better_budget=best,
                        GEPS_500=float(Hs[500].mean()) if 500 in Hs else None,
                        GEPS_5000=float(Hs[5000].mean()) if 5000 in Hs else None,
                        H=float(Hh.mean()), H_minus_GEPS=float(Hh.mean() - Hs[best].mean()), ci95_lo=lo, ci95_hi=hi,
                        frozen_H_minus_GEPS=fr.get("H_minus_GEPS"), frozen_epochs=fr.get("GEPS_epochs"),
                        label="post-freeze follow-up: GEPS-range trained longer (reported, not a substitute)"))
    return out


def repro():
    f = HERE.parent / "results" / "geps_repro_curve.json"
    if not f.exists():
        return []
    J = json.loads(f.read_text())
    return [dict(epoch=r["epoch"], train_loss=r["train_loss"], loss_test_in=r["loss_test_in"], loss_test_out=r["loss_test_out"],
                 persistence_test_in=J["persistence_test_in"], persistence_test_out=J["persistence_test_out"],
                 test_in_minus_persistence=r["loss_test_in"] - J["persistence_test_in"], paper_in_d=J["paper_in_d"],
                 label="reproduction (released code, lr 1e-2; reported)") for r in J["curve"]]


def fmt(x, p=2):
    return "" if x is None else f"{x:.{p}f}"


def note(rows, reading):
    L = [f"## GEPS as a learned adaptive opponent (script-generated: stage2/geps/geps_analysis.py @ {config.git_sha()[:7]})", ""]
    fin = reading[-1]
    L += [f"**Frozen reading:** {fin['claim']}.", "", f"**Caveat:** {CLIP_CAVEAT}", "",
          "| Re | better budget | GEPS-range (epochs trained) | H | H - GEPS (95%) | holds |", "|---|---|---|---|---|---|"]
    for r in reading[:-1]:
        dv = "" if r.get("GEPS_val_change_last2") is None else \
            f"; val change over last two checks {r['GEPS_val_change_last2']:+.4f} ({r['GEPS_val_change_last2_pct']:+.2f}%)"
        ep = "" if r.get("GEPS_epochs") is None else \
            f" ({r['GEPS_epochs']} epochs{', UNDERTRAINED' if r.get('GEPS_undertrained') else ''}{dv})"
        L.append(f"| {r['Re']} | {r['better_budget'] or 'pending'} | {fmt(r['GEPS'])}{ep} | {fmt(r['H'])} | "
                 f"{fmt(r['H_minus_GEPS'])} [{fmt(r['ci95_lo'])}, {fmt(r['ci95_hi'])}] | {r['holds_at_this_Re']} |")
    L += ["", f"First N = {N} states of the fresh World D panels, w = 11, eps 0.1, future frames; margin {MARGIN} with the "
          "95% paired interval excluding 0 (crossed bootstrap over trajectories and H's seeds; GEPS one seed). Scope reduced "
          "by Todd's ruling (feasibility); see GEPS_GATE.md and geps_freeze.yaml.", "",
          "| Re | arm | source | restricted mean (95%) | S(1) | S(3) | retention |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["eps"] == 0.1:
            L.append(f"| {r['Re']} | {r['arm']} | {r['source']} | {fmt(r['restricted_mean'])} [{fmt(r['ci95_lo'])}, "
                     f"{fmt(r['ci95_hi'])}] | {fmt(r['S1'])} | {fmt(r['S3'])} | {fmt(r['retention'])} |")
    L += ["", "GEPS training (validation RelativeL2 on the 64 fixed windows; persistence = the no-change forecast on the same windows):", "",
          "| run | lr | epochs | best val (epoch) | persistence | val curve (epoch:loss) | status |", "|---|---|---|---|---|---|---|"]
    for r in training():
        st = "collapsed to persistence" if r["collapsed"] else ("diverged" if r["diverged"] else ("undertrained (val still falling)" if r["undertrained"] else "trained"))
        if r["val_change_last2"] is not None:
            st += f"; val change over last two checks {r['val_change_last2']:+.4f} ({r['val_change_last2_pct']:+.2f}%)"
        L.append(f"| {r['run']} | {r['lr']:g} | {r['epochs_trained']} | {fmt(r['best_val'], 7)} ({r['best_epoch']}) | "
                 f"{r['persistence_val']:.7f} | {r['val_curve']} | {st}; evaluated: {r['evaluated']} |")
    t = timing()
    if t:
        L += ["", "| cost (batch 1, Spark GB10) | steps | n timed | wall median s | adapt median s | forecast median s |",
              "|---|---|---|---|---|---|"]
        L += [f"| {r['arm']} | {r['steps']} | {r['n_timed']} | {fmt(r['wall_median'], 1)} | {fmt(r['adapt_median'], 1)} | "
              f"{fmt(r['forecast_median'], 1)} |" for r in t]
    fu = followup(reading)
    if fu:
        L += ["", "Post-freeze follow-up, GEPS-range trained longer (seed 1 on Baccus; not a substitute for the frozen reading):", "",
              "| Re | checkpoint (val) | budgets | GEPS 500 / 5,000 | H - GEPS (95%) | frozen H - GEPS (epochs) |", "|---|---|---|---|---|---|"]
        L += [f"| {r['Re']} | {r['checkpoint']} ({fmt(r['val_loss'], 4)}) | {r['budgets_done']} | {fmt(r['GEPS_500'])} / {fmt(r['GEPS_5000'])} | "
              f"{fmt(r['H_minus_GEPS'])} [{fmt(r['ci95_lo'])}, {fmt(r['ci95_hi'])}] | {fmt(r['frozen_H_minus_GEPS'])} ({r['frozen_epochs']}) |" for r in fu]
    rp = repro()
    if rp:
        L += ["", "Post-freeze follow-up, reproduction: released GEPS code on its own Kolmogorov data at the published lr 1e-2 "
              f"(in-distribution test RelativeL2 vs persistence {rp[0]['persistence_test_in']:.4f}; the paper reports {rp[0]['paper_in_d']}):", "",
              "| epoch | train loss | test in-d | test in-d - persistence | test extrapolation |", "|---|---|---|---|---|"]
        L += [f"| {r['epoch']} | {r['train_loss']:.4g} | {r['loss_test_in']:.4f} | {r['test_in_minus_persistence']:+.4f} | {r['loss_test_out']:.4f} |" for r in rp]
    (RES / "results_note_geps.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
