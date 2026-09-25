"""Post-freeze extension, Kolmogorov decode-and-integrate resolution check (ext_freeze.yaml
kolmogorov.resolution_di_check): 8x8-layout b = 12 codebook, primary Delta 0.35, first 300 confirmation states.
Truth and the decoded initial state are both integrated at 128^2 from their 64^2 initial fields, spectrally zero-padded
(Nyquist dropped) and then projected by the 128^2 integrator (2/3 mask, mean removal); errors are evaluated on the 64^2
collocation points (every other 128^2 point), so the norm and sigma_A are those of the scored field. The 64^2 result
on the same states is the E3 decode-and-integrate horizon (the stored truth is the 64^2 trajectory from the same
t = 0 state). Reported: both restricted means (eps 0.1/0.3/0.5, future and from t = 0), the relative change of the
eps 0.3 future restricted mean and its paired bootstrap interval (states, seed 777, 2,000 reps).

Usage: python scripts/ext_kolmo_rescheck.py <device>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import kolmogorov as KM   # noqa: E402
from th import kolmo_eval as E   # noqa: E402
from th.score import paired_diff   # noqa: E402

TOK, NS = "kolmo_patch_L8_b12", 300


def main(device):
    t0 = time.time()
    sA = E.sigma_A()
    d = float(E.spec()["primary_delta"])
    pnl = E.Panel(n=NS)
    x0 = pnl.unit(0)
    tok = E.Tok(TOK)
    dec0, _, _ = tok.decode_nearest(x0, device)
    m = KM.Kolmogorov(N=128, device=device)
    wh = E.zero_pad_spec(np.concatenate([x0, dec0]), 128, m)
    F = E.n_future(d)
    spu = int(round(d / m.dt))
    err = np.full((F + 1, NS), np.inf)
    err[0] = np.sqrt(((dec0 - x0) ** 2).sum((-2, -1))) / sA
    done = np.zeros(NS, bool)
    for j in range(1, F + 1):
        wh = m.flow(wh, spu)
        g = m.to_phys(wh)[:, ::2, ::2].cpu().numpy()
        err[j] = np.sqrt(((g[NS:] - g[:NS]) ** 2).sum((-2, -1))) / sA
        done |= err[j] > 0.5
        if done.all():
            break
    z = np.load(E.RUNS / "e3" / f"{TOK}.npz")
    out = dict(tokenizer=TOK, delta=d, states=NS, stop_frame=j, rows=[], git_sha=config.git_sha(),
               label="post-freeze extension; reference (decode-and-integrate), resolution check",
               note="128^2 truth and reference both from spectrally zero-padded 64^2 initial fields; errors on the 64^2 points")
    H128 = {}
    for e, r in E.horizons_from_err(err, d).items():
        for start in ("future", "from_t0"):
            H, c = r[start]
            H64 = z[f"di_d{d:g}_eps{e}_{start}_H"][:NS]
            H128[(e, start)] = H
            out["rows"].append(dict(eps=e, start=start, mean_64=float(H64.mean()), mean_128=float(H.mean()),
                                    rel_change=float(H.mean() / H64.mean() - 1), frac_no_cross_128=float(1 - c.mean())))
    H = H128[(0.3, "future")]
    H64 = z[f"di_d{d:g}_eps0.3_future_H"][:NS]
    pdf = paired_diff(H, H64)
    rng = np.random.default_rng(777)
    rel = []
    for _ in range(2000):
        i = rng.integers(0, NS, NS)
        rel.append(H[i].mean() / H64[i].mean() - 1)
    out["primary"] = dict(mean_64=float(H64.mean()), mean_128=float(H.mean()), diff=pdf["diff"], diff_ci95=pdf["ci95"],
                          rel_change=float(H.mean() / H64.mean() - 1),
                          rel_change_ci95=[float(np.quantile(rel, 0.025)), float(np.quantile(rel, 0.975))],
                          per_state_equal_frac=float((H == H64).mean()))
    out["seconds"] = time.time() - t0
    np.savez(E.RUNS / "rescheck_128.npz", H128_eps0p3_future=H, H64_eps0p3_future=H64, err=err[:j + 1])
    E.RES.mkdir(parents=True, exist_ok=True)
    (E.RES / "resolution_di_check.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out["primary"], indent=1))


def detail(device):
    """Size of the 64^2 vs 128^2 difference itself (added at the coordinator's request; the frozen check is unchanged):
    per state, up to its 64^2 crossing frame j* (eps 0.3, future frames; all frames through W if it never crosses):
    max_t |e_128(t) - e_64(t)| of the normalized decode-and-integrate error, and ||x_128(t) - x_64(t)|| / sigma_A of
    the truth trajectories at t*, both on the 64^2 points. x_64 is the stored panel truth."""
    sA = E.sigma_A()
    d = float(E.spec()["primary_delta"])
    pnl = E.Panel(n=NS)
    x0 = pnl.unit(0)
    dec0, _, _ = E.Tok(TOK).decode_nearest(x0, device)
    z = np.load(E.RUNS / "e3" / f"{TOK}.npz")
    H64 = z[f"di_d{d:g}_eps0.3_future_H"][:NS]
    lam, F = E.lam(), E.n_future(d)
    jstar = np.minimum(np.round(H64 / (lam * d)).astype(int), F)
    m128 = KM.Kolmogorov(N=128, device=device)
    m64 = KM.Kolmogorov(N=64, device=device)
    w128 = E.zero_pad_spec(np.concatenate([x0, dec0]), 128, m128)
    w64 = m64.to_spec(torch.as_tensor(dec0))
    spu = int(round(d / m64.dt))
    max_de = np.zeros(NS)
    de_at = np.zeros(NS)
    truth_at = np.zeros(NS)
    truth_max = np.zeros(NS)
    for j in range(1, int(jstar.max()) + 1):
        w128 = m128.flow(w128, spu)
        w64 = m64.flow(w64, spu)
        g128 = m128.to_phys(w128)[:, ::2, ::2].cpu().numpy()
        g64 = m64.to_phys(w64).cpu().numpy()
        x64 = pnl.frame(j, d)
        e128 = np.sqrt(((g128[NS:] - g128[:NS]) ** 2).sum((-2, -1))) / sA
        e64 = np.sqrt(((g64 - x64) ** 2).sum((-2, -1))) / sA
        tdiff = np.sqrt(((g128[:NS] - x64) ** 2).sum((-2, -1))) / sA
        act = j <= jstar
        max_de = np.where(act, np.maximum(max_de, np.abs(e128 - e64)), max_de)
        truth_max = np.where(act, np.maximum(truth_max, tdiff), truth_max)
        at = j == jstar
        de_at[at] = np.abs(e128 - e64)[at]
        truth_at[at] = tdiff[at]
    q = lambda a: dict(max=float(a.max()), median=float(np.median(a)), p95=float(np.quantile(a, 0.95)))
    fn = E.RES / "resolution_di_check.json"
    out = json.loads(fn.read_text())
    out["difference_size"] = dict(
        note="added at the coordinator's request; the frozen check is unchanged. Up to each state's 64^2 crossing frame "
             "(eps 0.3, future); normalized by sigma_A on the 64^2 points; x_64 = stored panel truth, x_128 = 128^2 "
             "integration of the zero-padded t = 0 state",
        crossing_frame_median=float(np.median(jstar)), crossing_time_median=float(np.median(jstar) * d),
        max_t_abs_e128_minus_e64=q(max_de), abs_e128_minus_e64_at_crossing=q(de_at),
        truth_diff_at_crossing=q(truth_at), truth_diff_max_up_to_crossing=q(truth_max),
        git_sha=config.git_sha())
    fn.write_text(json.dumps(out, indent=1))
    print(json.dumps(out["difference_size"], indent=1))


if __name__ == "__main__":
    torch.set_num_threads(8)
    if sys.argv[1] == "detail":
        detail(sys.argv[2])
    else:
        main(sys.argv[1])
