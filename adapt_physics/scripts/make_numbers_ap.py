"""Build adapt_physics/NUMBERS.md: every number the Adapt the Physics paper may use, sections AP*, with stable ids,
labels, source files and producing SHAs. Uses the tokens-horizon NUMBERS checker (tokens_horizon/scripts/make_numbers.py
`table`): a duplicate section, an empty table or an unresolved column raises NumbersError. An AP-specific check
also fails if any row lacks a label or a section lacks its source SHA.
"""
import json
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
    # ---- all worlds: chaos gates (APVS) and the drag / beta calibrations (APVB)
    srows = []
    for world, f in (("D", config.RESULTS / "chaos_gate.json"), ("D", PR / "chaos_gate_D.json"), ("C", PR / "chaos_gate_C.json"),
                     ("V", config.PKG / "stage2" / "objections" / "results" / "chaos_V.json"),
                     ("D two-parameter", config.PKG / "stage2" / "results" / "chaos_2p.json")):
        if not f.exists():
            continue
        for k, v in sorted(((k, v) for k, v in json.loads(f.read_text()).items() if isinstance(v, dict)),
                           key=lambda kv: (kv[1]["Re"], kv[1].get("amp", 1.0))):
            srows.append(dict(world=world, system=k, Re=v["Re"], amp=v.get("amp", 1.0), alpha=v.get("alpha"),
                              beta=v.get("beta", 0.0), lam=v["lam"], lam_ci95_lo=v["lam_ci95"][0], lam_ci95_hi=v["lam_ci95"][1],
                              sigma_A=v["sigma_A"], chaotic=v["chaotic"], source=str(f.relative_to(config.PKG)),
                              label="estimate (system property)"))
    MN.table(out, "APVS", "All worlds: chaos gate (lambda with 95% interval over 64 starts) and sigma_A per test system",
             PR / "chaos_gate_C.json", ["world", "system", "Re", "amp", "alpha", "beta", "lam", ("95%", ci("lam_ci95_lo", "lam_ci95_hi")),
                                         "sigma_A", "chaotic", "source"], srows, config.git_sha(),
             note="World D Re 36-50: stage-1 gate; Re 56: pivot; World C: pivot; World V (alpha = alpha0 * 40 / Re) Re 50: "
                  "objections WO; two-parameter systems: stage 2 item 3.")
    dcj = json.loads((R / "drag_calibration.json").read_text())
    bcj = json.loads((PR / "beta_calibration.json").read_text())
    crows = [dict(calibration="drag (World D truth)", parameter="alpha", value=it["alpha"], quantity="drag share of enstrophy dissipation at Re 40",
                  result=it["share"], target=dcj["target"], selected=it["alpha"] == dcj["alpha"], label="estimate (calibration)")
             for it in dcj["iterations"]]
    crows += [dict(calibration="Codex topographic beta (World C truth)", parameter="beta_T", value=it["beta"],
                   quantity="relative change of <nu \\|grad omega\\|^2> at Re 40 vs beta = 0", result=it.get("rel_change", 0.0),
                   target=f"\\|change\\| = {bcj['target']} +- {bcj['tol']}", selected=it["beta"] == bcj["beta"], label="estimate (calibration)")
              for it in bcj["iterations"]]
    MN.table(out, "APVB", "Calibrations: drag share (World D) and the Codex beta term (World C), every iteration",
             PR / "beta_calibration.json", ["calibration", "parameter", "value", "quantity", "result", "target", "selected"], crows,
             bcj.get("git_sha", ""), note=f"Drag: alpha = {dcj['alpha']:.7f} gives share {dcj['share']:.5f}. Beta: Codex start 3.35; "
                                        f"selected beta_T = {bcj['beta']:.7f} ({bcj['rel_change']:+.4f}).")
    # ---- stage 2 sections APS* (stage2/S2_FREEZE.md)
    SR = config.PKG / "stage2" / "results"
    for fname, sec, title, cols, note in (
            ("s2_outcome.csv", "APSO", "Stage 2 part A: outcome of the pivot criteria on fresh panels (3 seeds)",
             ["outcome", "kill_any", "pass_all", "middle_all", "complete", "all_three_seeds", "precedence"], ""),
            ("s2_conditions.csv", "APSK", "Stage 2 part A: every pivot criterion on fresh panels, with 95% intervals",
             ["criterion", "world", "Re", "value", ("95%", ci("ci95_lo", "ci95_hi")), ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")),
              ("95% nested", ci("nested_ci95_lo", "nested_ci95_hi")), "per_seed", "threshold", "holds", "screening_value"],
             "Point ratio decides. Primary 95% intervals: CROSSED bootstrap (trajectory rows and seed columns resampled independently; post-freeze change, Todd 2026-09-27). Also: 95% cond = conditional on the trained models (seeds fixed); 95% nested = the frozen method (seeds resampled within trajectories). per_seed = the ratio for each seed."),
            ("s2_rows.csv", "APSH", "Stage 2 part A: seed-pooled horizons on fresh panels",
             ["world", "Re", "arm", "w", "eps", "score", "seeds", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")),
              ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")), ("95% nested", ci("nested_ci95_lo", "nested_ci95_hi")),
              "phys_time", "per_seed", "seed_sd", "S1", "S3", "retention", "ratio_to_L_range"],
             "score future = frames 1.. (primary); from_t0 = frame 0 included (item 6)."),
            ("s2_paired.csv", "APSD", "Stage 2: paired differences H - b (seed-pooled) and frozen readings",
             ["world", "Re", "w", "eps", "a", "b", "mean_a", "mean_b", "ratio", "diff", ("90%", ci("ci90_lo", "ci90_hi")),
              ("95%", ci("ci95_lo", "ci95_hi")), "reading", ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")), "reading_cond",
              ("95% nested", ci("nested_ci95_lo", "nested_ci95_hi")), "reading_nested", "per_seed_diff"],
             "Reading = frozen margins on the crossed interval (primary). Primary 95% intervals: CROSSED bootstrap (trajectory rows and seed columns resampled independently; post-freeze change, Todd 2026-09-27). Also: 95% cond = conditional on the trained models (seeds fixed); 95% nested = the frozen method (seeds resampled within trajectories)."),
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
                                                                    "training_data", "training_conditions", "training_re_range",
                                                                    "training_states"],
             "Conditions = distinct Re values in the training data (range sets: one Re per trajectory).")):
        p = SR / fname
        if p.exists():
            rows, sha = MN.read_csv(p)
            MN.table(out, sec, title, p, cols, rows, sha, note=note)
    # ---- objections WO sections APDD* (Part 1), APFR* (Part 2), APEDGE* (Part 3) (stage2/objections/OBJ_FREEZE.md)
    OR = config.PKG / "stage2" / "objections" / "results"
    for fname, sec, title, cols, note in (
            ("obj_part1_readings.csv", "APDD-R", "Objections Part 1 (World V, Re 50): readings (reported, not criteria)",
             ["eps", "primary", "H_over_O", ("95%", ci("H_over_O_ci95_lo", "H_over_O_ci95_hi")), "H_over_O_cond_ci95",
              "H_over_O_nested_ci95", "H_over_O_per_seed", "H_over_L_range_V",
              ("95%", ci("H_over_L_range_V_ci95_lo", "H_over_L_range_V_ci95_hi")), "H_over_L_range_V_cond_ci95",
              "H_over_L_range_V_nested_ci95", "H_over_L_range_V_per_seed", "outcome_reading", "L_range_V_seeds",
              "H_true_minus_H", ("95%", ci("H_true_minus_H_ci95_lo", "H_true_minus_H_ci95_hi")), "H_true_minus_H_cond_ci95",
              "H_true_minus_H_nested_ci95", "H_true_minus_H_per_seed", "partA_D_Re50_H_over_O", "partA_D_Re50_H_over_L_range"],
             "Primary 95% intervals: CROSSED bootstrap (trajectory rows and seed columns resampled independently; post-freeze change, Todd 2026-09-27). Also: 95% cond = conditional on the trained models (seeds fixed); 95% nested = the frozen method (seeds resampled within trajectories)."),
            ("obj_part1.csv", "APDD-H", "Objections Part 1 (World V, Re 50): horizons (seed-pooled)",
             ["arm", "w", "eps", "seeds", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")),
              ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")), ("95% nested", ci("nested_ci95_lo", "nested_ci95_hi")), "per_seed",
              "seed_sd", "S1", "S3", "phys_time", "partA_worldD_Re50"], "Primary 95% intervals: CROSSED bootstrap (trajectory rows and seed columns resampled independently; post-freeze change, Todd 2026-09-27). Also: 95% cond = conditional on the trained models (seeds fixed); 95% nested = the frozen method (seeds resampled within trajectories)."),
            ("obj_detector.csv", "APDD-W", "Objections: identified-Re detectors (H and P1x_V in World V; FNO-Re identified in World D)",
             ["world", "Re", "arm", "w_tested", "re_hat_w3", "re_hat_w6", "re_hat_w11", "re_hat_w23", "mean_re_hat", "bias_from_true",
              "slope_per_frame", ("95%", ci("slope_ci95_lo", "slope_ci95_hi")),
              ("95% cond", ci("slope_cond_ci95_lo", "slope_cond_ci95_hi")), "slope_per_seed", "detector_reading"],
             "Detector reading (H, World V): flags iff the (crossed) 95% interval excludes 0; no effect-size floor (gate). "
             "Slopes are per seed and state; crossed interval resamples states and seeds independently."),
            ("obj_part2_reading.csv", "APFR-R", "Objections Part 2: frozen claim reading (World D, Re 50 and 56)",
             ["Re", "H_minus_FNO_Re_true", ("95%", ci("ci95_lo", "ci95_hi")), ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")),
              ("95% nested", ci("nested_ci95_lo", "nested_ci95_hi")), "per_seed", "seeds", "holds_at_this_Re", "holds_cond",
              "holds_nested", "claim"], "holds_at_this_Re uses the crossed interval (primary). Primary 95% intervals: CROSSED bootstrap (trajectory rows and seed columns resampled independently; post-freeze change, Todd 2026-09-27). Also: 95% cond = conditional on the trained models (seeds fixed); 95% nested = the frozen method (seeds resampled within trajectories)."),
            ("obj_part2.csv", "APFR-H", "Objections Part 2: FNO-Re (true and identified Re) against H, fresh panels",
             ["world", "Re", "arm", "w", "eps", "seeds", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")),
              ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")), "per_seed", "S1", "S3", "retention", "H", "H_retention", "H_minus_arm",
              ("95%", ci("diff_ci95_lo", "diff_ci95_hi")), ("95% cond", ci("diff_cond_ci95_lo", "diff_cond_ci95_hi")),
              ("95% nested", ci("diff_nested_ci95_lo", "diff_nested_ci95_hi")), "diff_per_seed"],
             "FNOw_* = the L_param recipe trained on Re 30-60 (post-freeze request; one seed; reported, no reading). Primary 95% intervals: CROSSED bootstrap (trajectory rows and seed columns resampled independently; post-freeze change, Todd 2026-09-27). Also: 95% cond = conditional on the trained models (seeds fixed); 95% nested = the frozen method (seeds resampled within trajectories)."),
            ("obj_lft.csv", "APFR-FT", "Objections Part 2: fine-tuned FNO (L_ft) on fresh panels (reported, not a reading)",
             ["world", "Re", "w", "eps", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")), "retention", "H",
              "H_minus_L_ft", ("95%", ci("diff_ci95_lo", "diff_ci95_hi")), ("95% cond", ci("diff_cond_ci95_lo", "diff_cond_ci95_hi")),
              ("95% nested", ci("diff_nested_ci95_lo", "diff_nested_ci95_hi")), "diff_per_seed", "online_seconds_per_state"],
             "Primary 95% intervals: CROSSED bootstrap (trajectory rows and seed columns resampled independently; post-freeze change, Todd 2026-09-27). Also: 95% cond = conditional on the trained models (seeds fixed); 95% nested = the frozen method (seeds resampled within trajectories)."),
            ("obj_id_error.csv", "APFR-ID", "Per-state |identified Re - true Re| at w = 11 (pooled over states and seeds)",
             ["world", "Re", "arm", "w", "seeds", "n_values", "abs_err_median", "abs_err_p90", "abs_err_max"],
             "H: the hybrid's golden-section identification; FNO_Re_id: identification through the Re-conditioned network."),
            ("obj_ftb.csv", "APFR-FTB", "L_ft at matched budgets, World D Re 50 fresh panel, first 100 states, w = 11 (reported only, not a reading)",
             ["steps", "lr", "n", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")), "S1", "S3", "retention", "O_same_states",
              "H_same_states", "wall_median", "wall_p90", "finetune_median", "forecast_median"],
             "Every configuration (steps x lr), no post-hoc selection. Stage-1 pair rule; base L0 seed 0; one seed, so the 95% "
             "interval is over trajectories. Retention = restricted mean / O's on the same 100 states. Wall = batch-1 seconds per "
             "state (fine-tuning + forecast, CUDA-synchronised, Baccus CMP 170HX)."),
            ("obj_edge.csv", "APEDGE", "Objections Part 3: edge timing, Orin NX against datacenter (batch 1, reported only)",
             ["arm", "orin_result", "orin_wall_median", "orin_wall_p90", "dc_batch1_wall_median", "orin_identify_or_adapt_median",
              "orin_forecast_fps", "dc_batch1_forecast_fps", "orin_peak_torch_mem_MB", "orin_tegrastats_ram_peak_MB",
              "orin_vdd_in_mean_mW", "orin_energy_per_state_J", "horizon_max_abs_diff", "horizon_states_identical", "horizon_n",
              "orin_fixed_frames", "orin_fixed_wall_median", "orin_fixed_wall_p90", "orin_fixed_identify_or_adapt_median",
              "orin_fixed_forecast_median", "orin_fixed_forecast_fps", "orin_fixed_vdd_in_mean_mW", "orin_fixed_energy_per_state_J",
              "dc_fixed_wall_median", "dc_fixed_forecast_median", "dc_fixed_forecast_fps"],
             "Early-stop columns: each arm forecasts until every state exceeds 0.3 sigma_A (frame counts differ by arm). "
             "*_fixed_* columns: every arm forecasts the same F = 111 frames (10 Lyapunov times at Re 50), no early stop.")):
        p = OR / fname
        if p.exists():
            rows, sha = MN.read_csv(p)
            MN.table(out, sec, title, p, cols, rows, sha, note=note)
    # ---- GEPS WO sections APGEPS* (stage2/geps/geps_freeze.yaml; first N = 50 states, Todd's scope ruling 2026-09-28)
    GR = config.PKG / "stage2" / "geps" / "results"
    for fname, sec, title, cols, note in (
            ("geps_reading.csv", "APGEPS-R", "GEPS: frozen reading (H - GEPS-range at the better budget per Re; World D, first 50 states, w = 11)",
             ["Re", "better_budget", "GEPS", "GEPS_epochs", "GEPS_undertrained", "H", "H_minus_GEPS", ("95%", ci("ci95_lo", "ci95_hi")),
              ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")), "holds_at_this_Re", "claim", "caveat"],
             "Holds at a Re: H - GEPS >= 0.25 with the 95% interval > 0; stated if it holds at Re 50 AND 56. Paired bootstrap "
             "over trajectories (crossed over H's 3 seeds; GEPS one seed); 95% cond = conditional on the trained models."),
            ("geps_rows.csv", "APGEPS", "GEPS and Part A arms on the same first 50 states (World D, w = 11)",
             ["Re", "arm", "source", "eps", "n", "seeds", "restricted_mean", ("95%", ci("ci95_lo", "ci95_hi")),
              ("95% cond", ci("cond_ci95_lo", "cond_ci95_hi")), "S1", "S3", "retention"],
             "Retention = restricted mean / O's on the same states and eps. GEPS_range_noadapt: one context fitted on Re-40 "
             "nominal data, the same for every state."),
            ("geps_timing.csv", "APGEPS-T", "GEPS: batch-1 cost per state on a DGX Spark GB10 (s2_test_Re50_D; reported only)",
             ["arm", "steps", "n_timed", "frames", "wall_median", "wall_p90", "adapt_median", "forecast_median", "forecast_fps",
              "device"],
             "One state at a time, CUDA-synchronised; the 5,000-step budget timed on states 3-5 only (time-bound)."),
            ("geps_training.csv", "APGEPS-TR", "GEPS training runs",
             ["run", "data", "lr", "host", "epochs_trained", "steps", "best_val", "best_epoch", "persistence_val",
              "best_minus_persistence", "undertrained", "diverged", "collapsed", "evaluated", "val_curve"],
             "Validation RelativeL2 on the 64 fixed windows; persistence_val = the no-change forecast on the same windows. At the "
             "published lr 1e-2 GEPS-range collapsed to persistence (archived, never evaluated) and GEPS-wide diverged; both were "
             "retrained at 1e-3 (deviations; GEPS-range for ~1 h, validated every 2 epochs). GEPS-wide's evaluation is cut.")):
        p = GR / fname
        if p.exists():
            rows, sha = MN.read_csv(p)
            MN.table(out, sec, title, p, cols, rows, sha, note=note)
    check(out)
    (config.PKG / "NUMBERS.md").write_text("\n".join(out) + "\n")
    print("wrote NUMBERS.md", sum(1 for l in out if l.startswith("| AP")), "rows")


if __name__ == "__main__":
    main()
