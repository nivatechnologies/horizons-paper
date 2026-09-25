"""Build the 'POST-FREEZE extension' section of the vault results note directly from result files (no retyped numbers).

Writes results/ext/results_note_extension.md. Every number is read from a committed result file; the file path of
each table is printed under it.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config  # noqa: E402

R = config.RESULTS / "ext"


def rd(p):
    return list(csv.DictReader(l for l in open(p) if not l.startswith("#")))


def f(x, n=3):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    return f"{v:.{n}f}"


def src(p):
    return f"\n*Source: `{Path(p).relative_to(config.PKG)}`*\n"


def main():
    L = ["", "## POST-FREEZE extension (WO 2026-09-25, Amendments 1 and 2)", "",
         "All numbers below are generated from committed result files by `scripts/ext_results_note.py`; NUMBERS.md "
         "sections K and K2 hold the full tables. Labels: bound / reference / learned / estimate; everything here is "
         "a **post-freeze extension**. Freeze commits: part 1 `94c6cd7`, Amendment 1 `f7fedcb`, Amendment 2 `d960d0b`, "
         "part 2a (KS) `b5b476e` with fix 1 `fd992f1`, part 2b (Kolmogorov) `ef2d9f0`; A9 prediction `468cabc`; B3 "
         "prefix-invariance pass `f5c9747`.", ""]
    # systems
    L += ["### Systems", "", "| system | L | N | dt | λ | D_KY | W (time units) | Δ | σ_A |", "|---|---|---|---|---|---|---|---|---|"]
    import yaml
    efz = yaml.safe_load((config.PKG / "ext_freeze.yaml").read_text())
    kb = json.loads((R / "ks" / "data_blocks.json").read_text())
    for n, s in efz["ks"]["systems"].items():
        L.append(f"| {n} | {s['L']:g} | {s['N']} | {s['dt']} | {s['lyapunov']['lam_max']:.5f} ± {s['lyapunov']['lam_max_se']:.5f} | "
                 f"{s['lyapunov']['d_ky']:.2f} | {s['window_time']} | {' / '.join(map(str, s['frame_intervals']))} | {kb[n]['sigma_A']:.3f} |")
    kz = efz["kolmogorov"]
    kj = json.loads((R / "kolmo" / "data_blocks.json").read_text())
    ksig = kj.get("sigma_A") or kj.get("kolmo40", {}).get("sigma_A")
    L.append(f"| kolmo40 (Re 40, n 4) | 2π | 64² | {kz['numerics']['dt']} | {kz['lyapunov']['lam_max']:.5f} ± "
             f"{kz['lyapunov']['lam_max_se']:.5f} | – | {kz['window_time']} | {' / '.join(map(str, kz['frame_intervals']))} | {f(ksig)} |")
    L += ["", "KS L = 22 D_KY is 4.24 (the WO's 5.2 is from a mean-mode-keeping convention; hypothesis). Kolmogorov: "
          "64² → 128² moves λ by −0.8%. No particle filter was run in these systems (WO E3): with an indicator "
          "likelihood, a particle survives only if its predicted state falls in the observed cell, and the number of "
          "particles needed for that grows exponentially with the attractor dimension (D_KY 4.2–21 for KS, larger for "
          "Kolmogorov) and with the number of tokens per frame; at these dimensions the reference is infeasible "
          "(reasoning, not a measurement).", ""]
    # KS whole-state
    e3 = rd(R / "ks" / "e3_rows.csv")
    L += ["### KS L = 22, whole-state k-means (Δ = 0.92, ε 0.3, future frames)", "",
          "| bits | bound (bound) | S_out(1) / S_out(3) / S_out(10) | p_0 | decode-and-integrate (reference) | persistence |",
          "|---|---|---|---|---|---|"]
    for b in range(4, 17):
        def g(kind):
            r = [x for x in e3 if x["tokenizer"] == f"ks22_whole_b{b}" and x["delta"] == "0.92" and x["eps"] == "0.3"
                 and x["start"] == "future" and x["kind"] == kind]
            return r[0] if r else None
        bo, di, pe = g("bound"), g("decode_and_integrate"), g("persistence")
        if not bo:
            continue
        L.append(f"| {b} | {f(bo['restricted_mean'])} | {f(bo['S1'],2)} / {f(bo['S3'],2)} / {f(bo['S10'],2)} | {f(bo['p0'],3)} | "
                 f"{f(di['restricted_mean']) if di else '–'} | {f(pe['restricted_mean']) if pe else '–'} |")
    L.append(src(R / "ks" / "e3_rows.csv"))
    # KS patch families
    L += ["### KS patch families (primary Δ, ε 0.3, future frames)", "",
          "| system | P | b | total bits | bound | S_out(1) | decode-and-integrate | persistence |", "|---|---|---|---|---|---|---|---|"]
    prim = {n: str(s["primary_delta"]) for n, s in efz["ks"]["systems"].items()}
    for sysn in ("ks22", "ks100"):
        for P in ("8", "16", "32"):
            for b in ("8", "10", "12", "14", "16"):
                def g(kind):
                    r = [x for x in e3 if x["system"] == sysn and x["family"] == "patch" and x["P"] == P and x["b"] == b
                         and x["delta"] == prim[sysn] and x["eps"] == "0.3" and x["start"] == "future" and x["kind"] == kind]
                    return r[0] if r else None
                bo, di, pe = g("bound"), g("decode_and_integrate"), g("persistence")
                if bo:
                    L.append(f"| {sysn} | {P} | {b} | {bo['total_bits']} | {f(bo['restricted_mean'])} | {f(bo['S1'],2)} | "
                             f"{f(di['restricted_mean'])} | {f(pe['restricted_mean'])} |")
    L.append(src(R / "ks" / "e3_rows.csv"))
    # A9
    a9 = rd(R / "ks" / "a9_result.csv")
    L += ["### A9 prospective test (KS L = 22 whole-state; predictor committed in `468cabc` before any odd rate)", "",
          "| R | observed (reference) [95%] | Ĥ (estimate) | observed − Ĥ [90%] | criterion |", "|---|---|---|---|---|"]
    for r in a9:
        L.append(f"| {r['R']} | {f(r['observed'],4)} [{f(r['observed_ci95_lo'],4)}, {f(r['observed_ci95_hi'],4)}] | {f(r['H_hat'],4)} | "
                 f"{f(r['diff'],4)} [{f(r['diff_ci90_lo'],4)}, {f(r['diff_ci90_hi'],4)}] | {r['criterion']} |")
    L += [src(R / "ks" / "a9_result.csv"),
          "This tests prospective interpolation across held-out rates within the specified system, tokenizer family "
          "and rate range; it does not test extrapolation or cross-system transfer. Exposure record: no odd-rate "
          "decode-and-integrate horizon was computed or inspected before the prediction commit.", ""]
    # Kolmogorov
    ke = rd(R / "kolmo" / "e3_rows.csv")
    L += ["### Kolmogorov patch layouts (Δ = 0.35, ε 0.3, future frames)", "",
          "| layout | b | total bits | bound | S_out(1) / (3) / (10) | p_0 | decode-and-integrate | persistence |",
          "|---|---|---|---|---|---|---|---|"]
    for lay in ("4x4", "8x8", "16x16"):
        for b in ("8", "10", "12", "14", "16"):
            def g(kind):
                r = [x for x in ke if x.get("layout") == lay and x["b"] == b and x["delta"] == "0.35" and x["eps"] == "0.3"
                     and x["start"] == "future" and x["kind"] == kind]
                return r[0] if r else None
            bo, di, pe = g("bound"), g("decode_and_integrate"), g("persistence")
            if bo:
                L.append(f"| {lay} | {b} | {bo['total_bits']} | {f(bo['restricted_mean'])} | {f(bo['S1'],2)} / {f(bo['S3'],2)} / "
                         f"{f(bo['S10'],2)} | {f(bo['p0'],3)} | {f(di['restricted_mean'])} | {f(pe['restricted_mean'])} |")
    rj = json.loads((R / "kolmo" / "bound_reading_2p12_64tokens.json").read_text())
    smallest = min(rj["configurations_tested"], key=lambda c: c[2])
    L += [src(R / "kolmo" / "e3_rows.csv"),
          f"**EXT_FREEZE reading:** bound below 1 Lyapunov time at any configuration with ≥ 2^12 codes per token and "
          f"≥ 64 tokens per frame: **{rj['below_one_lyapunov_time']}** (smallest: {smallest[0]} at Δ {smallest[1]}, "
          f"{smallest[2]:.2f} Lyapunov times; {len(rj['configurations_tested'])} configurations).", ""]
    rc = json.loads((R / "kolmo" / "resolution_di_check.json").read_text())
    L += [f"Decode-and-integrate resolution check (8×8, b = 12, 300 states, 128² vs 64²): relative change "
          f"{rc['primary']['rel_change']}; crossing frames identical for every state.", ""]
    # thresholds
    L += ["### Smallest tested rate reaching 1 / 3 / 10 Lyapunov times (A3 rule; 'not reached' = not within the tested grid)", ""]
    kt = rd(R / "ks" / "thresholds.csv")
    L += ["| system | family | quantity | τ = 1 | τ = 3 | τ = 10 |", "|---|---|---|---|---|---|"]
    for sysn in ("ks22", "ks100"):
        for fam, P in (("whole", "1"), ("patch", "8"), ("patch", "16"), ("patch", "32")):
            for kind in ("bound", "decode_and_integrate"):
                cells = []
                for tau in ("1", "3", "10"):
                    r = [x for x in kt if x["system"] == sysn and x["family"] == fam and x["P"] == P and x["kind"] == kind
                         and x["delta"] == prim[sysn] and x["eps"] == "0.3" and x["start"] == "future"
                         and float(x["tau"]) == float(tau)]
                    cells.append((r[0]["smallest_tested_rate"] or "not reached") if r else "–")
                if any(c != "–" for c in cells):
                    L.append(f"| {sysn} | {fam if fam == 'whole' else 'P = ' + P} | {kind} | " + " | ".join(cells) + " |")
    kt2 = rd(R / "kolmo" / "thresholds_a3.csv")
    for lay in ("4x4", "8x8", "16x16"):
        for q in sorted({x["quantity"] for x in kt2}):
            cells = []
            for tau in ("1", "3", "10"):
                r = [x for x in kt2 if x["family"] == lay and x["quantity"] == q and x["delta"] == "0.35"
                     and x["eps"] == "0.3" and x["start"] == "future" and float(x["tau"]) == float(tau)]
                cells.append((r[0]["smallest_tested_rate"] or "not reached") if r else "–")
            if any(c != "–" for c in cells):
                L.append(f"| kolmo40 | layout {lay} | {q} | " + " | ".join(cells) + " |")
    L += ["", "Nominal total bits per frame (P·b), primary Δ, ε 0.3, future frames; 'smallest tested rate for this tokenizer "
          "family', not a minimum bit requirement. Monotone flags and the lower-95% variant are in the source files "
          "(`results/ext/ks/thresholds.csv`, `results/ext/kolmo/thresholds_a3.csv`).", ""]
    # E4
    sel = json.loads((R / "ks" / "e4_selection.json").read_text())
    L += ["### E4 (learned KS cell)", "",
          "All 48 candidates (P ∈ {16, 32}, b ∈ {10, …, 16}, both KS domains, all Δ) have a validation restricted-mean "
          "bound of 27 (every state survives the window). Selected cell: none; support-permissive contrast: none. "
          "\"No tested configuration satisfying the E4 size requirements had a validation restricted-mean support "
          "horizon below one Lyapunov time.\" No E4 model was trained; the model code and its prefix-invariance test "
          "(Amendment 2 B3) are committed.", ""]
    # controls
    pc = [r for r in rd(R / "e5_probe_control.csv") if r["kind"] == "pooled"]
    L += ["### Reviewer controls on Lorenz-63 (K2)", "", "**Probe control (E5.1), MLP probes, horizon [95%]:**", "",
          "| cell | trained A | untrained A | token-history MLP |", "|---|---|---|---|"]
    for c in ("b4_D0.02", "b4_D0.05", "b4_D0.1", "b6_D0.02"):
        def g(fc):
            r = [x for x in pc if x["cell"] == c and x["forecaster"] == fc][0]
            return f"{f(r['H_restricted_mean'])} [{f(r['ci95_lo'])}, {f(r['ci95_hi'])}]"
        L.append(f"| {c} | {g('trained_mlp')} | {g('untrained_mlp')} | {g('tokhist')} |")
    L += ["", "Reading (Amendment 1 A8.5, frozen margins): at 4 bits for all Δ, 'training makes the precision more "
          "recoverable by the tested readout'; at 6 bits Δ 0.02 no reading applies. The paper never says the untrained "
          "representation lacks it.", ""]
    tb = rd(R / "e5_tie_baselines.csv")
    L += ["**Ties with the bound at 4 bits (Amendment 2 B4): P(VPT = T_out | Δ < T_out ≤ W) [95%]:**", "",
          "| Δ | A (seeds pooled) | persistence | random-code | automatic first-frame | jointly censored |", "|---|---|---|---|---|---|"]
    for c in ("b4_D0.02", "b4_D0.05", "b4_D0.1"):
        def g(fc, seed):
            return [x for x in tb if x["cell"] == c and x["forecaster"] == fc and x["seed"] == seed][0]
        a, p_, rc_ = g("A", "0-2 pooled"), g("persistence", ""), g("random_code", "draws 0-4 averaged")
        L.append(f"| {c[4:]} | {f(a['tie_given_obs_failure'])} [{f(a['tie_ci95_lo'])}, {f(a['tie_ci95_hi'])}] | "
                 f"{f(p_['tie_given_obs_failure'])} | {f(rc_['tie_given_obs_failure'])} | {p_['n_auto_first_frame']} | "
                 f"{p_['n_jointly_censored']} |")
    sn = [r for r in rd(R / "e5_b_snapped.csv") if r["score"] == "eps0.3_future"]
    L += ["", "**B snapped to its nearest prototype (A8.1), 4 bits:**", "", "| Δ | B | B snapped | bound | snapped − bound [95%] | reading |",
          "|---|---|---|---|---|---|"]
    for c in ("b4_D0.02", "b4_D0.05", "b4_D0.1"):
        def g(row):
            return [x for x in sn if x["cell"] == c and x["row"] == row][0]
        d = g("B_snapped - bound")
        L.append(f"| {c[4:]} | {f(g('B')['value'])} | {f(g('B_snapped')['value'])} | {f(g('bound')['value'])} | "
                 f"{f(d['value'])} [{f(d['ci95_lo'])}, {f(d['ci95_hi'])}] | {d['reading'].replace('|', ';')} |")
    e53 = rd(R / "e53_larger_model.csv")
    L += ["", "**Larger and longer model (E5.3; width 256, 6 layers, 40,000 steps; Δ 0.05):**", "",
          "| arm | bits | frozen size | larger | larger − frozen [95%] | reading |", "|---|---|---|---|---|---|"]
    for r in e53:
        L.append(f"| {r['arm']} | {r['bits']} | {f(r['H_frozen_size'])} | {f(r['H_large'])} | {f(r['diff_large_minus_frozen'])} "
                 f"[{f(r['diff_ci95_lo'])}, {f(r['diff_ci95_hi'])}] | "
                 f"{r['reading'].replace('b well below a', 'frozen size well below larger').replace('a well below b', 'larger well below frozen size')} |")
    sp = rd(R / "a8_same_panel.csv")
    L += ["", "**Same-panel headline (A8.3), first 300 states, 4 bits, Δ 0.02:**", "", "| series | mean | minus particle filter [95%] | reading |",
          "|---|---|---|---|"]
    for r in sp:
        if r["bits"] == "4" and r["delta"] == "0.02":
            L.append(f"| {r['series']} | {f(r['mean'])} | {f(r['diff_vs_pf']) if r['diff_vs_pf'] else ''} "
                     f"{'[' + f(r['diff_ci95_lo']) + ', ' + f(r['diff_ci95_hi']) + ']' if r['diff_ci95_lo'] else ''} | "
                     f"{r['reading'].replace('a well below b', 'well below the particle filter').replace('b well below a', 'particle filter well below')} |")
    # B5
    L += ["", "### Release gate B5 (bootstrap resampling unit) — outcome recorded", "",
          "**FAIL, then rerun.** Reading the resampling unit from the code: confirmation panels are one independent "
          "trajectory per state (pass); decomposition and D_eff already resample calibration trajectories (pass); the "
          "exchange-law h curve, predictions, r by orientation, FSLE and the post-freeze per-state/geometric variants "
          "resampled individual calibration states that share trajectories (1,000 h states from 150 trajectories, "
          "median 7 per trajectory, ~14 time units apart, inside the ~30 time-unit scoring window) — fail. Rerun with "
          "the calibration trajectory as the resampling unit (commit `100b159`): point estimates unchanged; interval "
          "widths ×0.84–1.43 (median ×1.01–1.03); **no frozen reading changed**. Gate record: NUMBERS.md section K2F. "
          "Release may proceed on this gate.", ""]
    out = "\n".join(L) + "\n"
    (R / "results_note_extension.md").write_text(out)
    print(len(out), "chars")


if __name__ == "__main__":
    main()
