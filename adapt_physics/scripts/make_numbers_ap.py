"""Build adapt_physics/NUMBERS.md: every number the Adapt the Physics paper may use, sections AP*, with stable ids,
labels, source files and producing SHAs. Uses the tokens-horizon NUMBERS checker (tokens_horizon/scripts/make_numbers.py
`table`): a duplicate section, an empty table or an unresolved column raises NumbersError. An AP-specific check
also fails if any row lacks a label or a section lacks its source SHA.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parents[2] / "tokens_horizon" / "scripts"))
sys.path.insert(0, str(HERE.parents[2] / "tokens_horizon"))
import make_numbers as MN  # noqa: E402

from ap import config  # noqa: E402

MN.PKG = config.PKG
R = config.RESULTS
ci = MN.ci


def check(lines):
    """AP checker extension: every table row carries a non-empty label; every section has a SHA."""
    sec = None
    for l in lines:
        if l.startswith("## "):
            sec = l
        if l.startswith("Source ") and ("SHA ``" in l):
            raise MN.NumbersError(f"{sec}: empty SHA")
        if l.startswith("| AP") and l.rstrip().endswith("|  |"):  # covers AP* and APV*
            raise MN.NumbersError(f"{sec}: unlabelled row {l[:40]}")


def main():
    out = ["# NUMBERS (Adapt the Physics, stage 1)", "",
           "Every number the paper may use. Labels: **reference** (solver arms and persistence), **learned** (FNO arms), "
           "**estimate** (differences, ratios, costs, identified parameters). Horizons are restricted means in Lyapunov "
           "times of the test system (W = 10), 95% intervals unless stated. Stage 1 is a screening panel "
           "(300 trajectories per Re; L_ft on the first 100).", ""]
    for fname, sec, title, cols, note in (
            ("drag_calibration.json", None, None, None, None),
            ("ap_kill_verdict.csv", "APK", "Kill rule on the frozen cell (Re 44, eps 0.1, w 11, first 100 states)",
             ["cell", "I_star", "I_arm", "A_star", "A_arm", "ratio_44", "ratio_50", "ratio_40", "pass_condition",
              "kill_condition", "outcome", "flag_no_drift_ratio_ge_drift", "opponents_present"],
             "Pass: I* >= 2 A* at Re 44 and Re 50. Kill: A* >= 0.75 I* at Re 44. Flag: ratio at Re 40 >= ratio at Re 44."),
            ("ap_kill.csv", "APKT", "I*, A* and ratios for every Re, w, eps (first 100 states; 300-state ratio without L_ft)",
             ["Re", "w", "eps", "O", "P1", "L_param_P1", "L_range", "L_ft", "L0big", "I_star", "I_arm", "A_star", "A_arm",
              "ratio", "ratio_300_without_Lft"], ""),
            ("ap_rows.csv", "APH", "Horizons per arm, test Re, window and tolerance",
             ["Re", "arm", "role", "w", "eps", "panel", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")),
              "phys_time", ("95% (time)", ci("phys_ci95_lo", "phys_ci95_hi")), "S1", "S3", "frac_no_cross", "lam_test"],
             "panel all = every state the arm ran on (300; L_ft 100); first100 = the kill-rule subset."),
            ("ap_paired.csv", "APD", "Paired differences a - b (same states) and frozen readings",
             ["Re", "w", "eps", "a", "b", "n", "mean_a", "mean_b", "diff", ("90%", ci("ci90_lo", "ci90_hi")),
              ("95%", ci("ci95_lo", "ci95_hi")), "reading"],
             "Readings: well below = difference >= 0.25 with the 95% interval excluding 0; approximately equal = 90% "
             "interval within +-0.10; otherwise no reading."),
            ("ap_recovery.csv", "APR", "Time to 90% of the oracle (smallest tested w)",
             ["Re", "eps", "arm", "w_tested", "w_to_90pct_oracle"], ""),
            ("ap_identify.csv", "API", "Identified Re (P1: no-drag family; P1x: drag known)",
             ["Re", "arm", "w", "n", "re_hat_mean", "re_hat_sd", "re_hat_median", "median_abs_error", "frac_at_bounds"], ""),
            ("ap_cost.csv", "APC", "Online adaptation cost per arm",
             ["Re", "arm", "w", "n", "wall_seconds_per_state", "identify_seconds_per_state", "solver_steps_identify",
              "objective_evals", "gradient_steps", "forecast_steps"],
             "Wall-clock on one CMP 170HX (shared); solver steps are dt = 0.01 IFRK4 steps of one 64^2 state."),
            ("ap_training.csv", "APT", "Training cost of the learned models",
             ["model", "params", "steps", "batch", "train_seconds", "best_step", "best_val"], "")):
        if sec is None:
            continue
        p = R / fname
        if p.exists():
            rows, sha = MN.read_csv(p)
            MN.table(out, sec, title, p, cols, rows, sha, note=note)
    # system table from json
    import json
    cg = json.loads((R / "chaos_gate.json").read_text())
    dc = json.loads((R / "drag_calibration.json").read_text())
    srows = [dict(Re=v["Re"], alpha=v["alpha"], lam=v["lam"], lam_ci95=f"[{v['lam_ci95'][0]:.4f}, {v['lam_ci95'][1]:.4f}]",
                  lam_min_start=v["lam_min_start"], sigma_A=v["sigma_A"], chaotic=v["chaotic"],
                  drag_share_at_Re40=dc["share"], label="estimate (system property)")
             for k, v in sorted(cg.items(), key=lambda kv: kv[1]["Re"] if isinstance(kv[1], dict) else 0)
             if isinstance(v, dict)]
    MN.table(out, "APS", "Systems: drag calibration and chaos gate (with drag)", R / "chaos_gate.json",
             ["Re", "alpha", "lam", "lam_ci95", "lam_min_start", "sigma_A", "chaotic", "drag_share_at_Re40"], srows,
             cg.get("git_sha", ""))
    # ---- pivot sections APV* (pivot/PV_FREEZE.md)
    PR = config.PKG / "pivot" / "results"
    for fname, sec, title, cols, note in (
            ("pv_outcome.csv", "APVO", "Pivot: pre-committed outcome (w 11, eps 0.1, 300 states)",
             ["outcome", "kill_any", "pass_all", "middle_all", "complete", "precedence"],
             "Precedence KILL -> PASS -> MIDDLE -> otherwise (gate pin)."),
            ("pv_conditions.csv", "APVK", "Pivot: every pre-committed criterion",
             ["criterion", "world", "Re", "value", "threshold", "holds"], ""),
            ("pv_rows.csv", "APVH", "Pivot: horizons per world, arm, test Re, window, tolerance",
             ["world", "Re", "arm", "w", "eps", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")), "phys_time",
              "S1", "S3", "retention", "ratio_to_L_range", "lam_test"],
             "World D Re 36/40/44/50 stage-1 arms are the stage-1 evaluations (identical panels and code)."),
            ("pv_paired.csv", "APVD", "Pivot: paired differences a - b and frozen readings",
             ["world", "Re", "w", "eps", "a", "b", "n", "mean_a", "mean_b", "ratio", "diff", ("90%", ci("ci90_lo", "ci90_hi")),
              ("95%", ci("ci95_lo", "ci95_hi")), "reading"], ""),
            ("pv_recovery.csv", "APVR", "Pivot: time to 90% of the oracle", ["world", "Re", "eps", "arm", "w_tested",
                                                                          "w_to_90pct_oracle"], ""),
            ("pv_detector.csv", "APVW", "Pivot: window-drift detector (identified Re against w; reported only)",
             ["world", "Re", "arm", "re_hat_w3", "re_hat_w6", "re_hat_w11", "re_hat_w23", "slope_per_frame",
              ("95%", ci("slope_ci95_lo", "slope_ci95_hi")), "slope_per_lyapunov_time"], ""),
            ("pv_cost.csv", "APVC", "Pivot: online cost", ["world", "Re", "arm", "w", "n", "wall_seconds_per_state",
                                                            "solver_steps_identify", "objective_evals", "forecast_steps",
                                                            "gradient_steps"], ""),
            ("pv_training.csv", "APVT", "Pivot: training cost (conditions = distinct Re in the training data)",
             ["model", "params", "steps", "batch", "train_seconds", "best_step", "training_conditions", "training_states"], "")):
        p = PR / fname
        if p.exists():
            rows, sha = MN.read_csv(p)
            MN.table(out, sec, title, p, cols, rows, sha, note=note)
    # ---- stage 2 sections APS* (stage2/S2_FREEZE.md)
    SR = config.PKG / "stage2" / "results"
    for fname, sec, title, cols, note in (
            ("s2_outcome.csv", "APSO", "Stage 2 part A: outcome of the pivot criteria on fresh panels (3 seeds)",
             ["outcome", "kill_any", "pass_all", "middle_all", "complete", "all_three_seeds", "precedence"], ""),
            ("s2_conditions.csv", "APSK", "Stage 2 part A: every pivot criterion on fresh panels, with 95% intervals",
             ["criterion", "world", "Re", "value", ("95%", ci("ci95_lo", "ci95_hi")), "threshold", "holds", "screening_value"],
             "Point ratio decides; interval = bootstrap over trajectories with seeds resampled within trajectories."),
            ("s2_rows.csv", "APSH", "Stage 2 part A: seed-pooled horizons on fresh panels",
             ["world", "Re", "arm", "w", "eps", "score", "seeds", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")),
              "phys_time", "per_seed", "S1", "S3", "retention", "ratio_to_L_range"],
             "score future = frames 1.. (primary); from_t0 = frame 0 included (item 6)."),
            ("s2_paired.csv", "APSD", "Stage 2: paired differences H - b (seed-pooled) and frozen readings",
             ["world", "Re", "w", "eps", "a", "b", "mean_a", "mean_b", "ratio", "diff", ("90%", ci("ci90_lo", "ci90_hi")),
              ("95%", ci("ci95_lo", "ci95_hi")), "reading"], ""),
            ("s2_recovery.csv", "APSR", "Stage 2: time to 90% of the oracle (w in 3, 6, 11)",
             ["world", "Re", "eps", "arm", "w_tested", "w_to_90pct_oracle"], ""),
            ("s2_detector.csv", "APSW", "Stage 2: window-drift detector and the World C slope-shortfall correlation",
             ["world", "Re", "arm", "re_hat_w3", "re_hat_w6", "re_hat_w11", "slope_per_frame",
              ("95%", ci("slope_ci95_lo", "slope_ci95_hi")), "spearman_slope_vs_shortfall",
              ("95%", ci("spearman_ci95_lo", "spearman_ci95_hi"))], "Reported only."),
            ("s2_partB.csv", "APSB", "Stage 2 part B: robustness items 1-4 (reported, not criteria)",
             ["item", "panel", "arm", "variant", "window", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")),
              "ratio_to_O", "ratio_to_L_range", "ratio_to_O_std", "ratio_to_O_noise5", "H_seed_pooled", "H_over_L_range_wide",
              "re_hat_median", "amp_hat_median", "window_starts_before_tc"], "Single seed (seed 0) where stated in the freeze."),
            ("s2_cost.csv", "APSC", "Stage 2: online cost", ["panel", "key", "arm", "seed", "variant", "window", "n",
                                                             "wall_seconds_per_state", "solver_steps", "objective_evals"], ""),
            ("s2_training.csv", "APST", "Stage 2: training cost", ["model", "seed", "params", "steps", "train_seconds", "best_step",
                                                                    "training_conditions", "training_re_range", "training_states"], "")):
        p = SR / fname
        if p.exists():
            rows, sha = MN.read_csv(p)
            MN.table(out, sec, title, p, cols, rows, sha, note=note)
    check(out)
    (config.PKG / "NUMBERS.md").write_text("\n".join(out) + "\n")
    print("wrote NUMBERS.md", sum(1 for l in out if l.startswith("| AP")), "rows")


if __name__ == "__main__":
    main()
