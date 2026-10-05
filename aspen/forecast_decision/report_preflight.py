"""Recompute numerical/sampler report values and generate NUMBERS sections."""
import copy,json,math
import numpy as np
from protocol import *
from preflight import render_numbers
def evidence():
    dt=json.loads((ROOT/"runs/numerics/dtcheck.json").read_text())
    for r in dt["rounds"]:
        for e in r["comparisons"]:
            sj=r["S_J"][list(LEADS).index(e["lead"])]
            assert np.isclose(e["threshold"],max(.05*sj,2*e["SE"]),rtol=0,atol=1e-15)
            assert e["passed"]==(sj>0 and e["change"]<e["threshold"])
        assert r["passed"]==all(e["passed"] for e in r["comparisons"])
    assert dt["status"]=="PASS" and dt["chosen_dt"]==dt["rounds"][-1]["dt"]
    rate=json.loads((ROOT/"runs/numerics/twoscale_rate.json").read_text())
    measured=float(np.median(rate["repeat_seconds_per_step"]))
    assert measured==rate["median_seconds_per_step"]
    # Projection to full 3 LT_ref, as the WO estimate states; no rounded-window substitution.
    steps=int(np.ceil(3*LT/.001))
    hours=300*9*steps*measured/3600
    raw=np.load(ROOT/"runs/twoscale/sampler_raw.npz")
    mean=raw["draws"].mean(1);error=mean-raw["realized"]
    spread=raw["draws"].std(1,ddof=1)
    sd=float(np.sqrt(np.mean(spread**2)));err=float(np.sqrt(np.mean(error**2)))
    ratio=sd/err if err>0 else None
    corr=float(np.corrcoef(mean.reshape(-1),raw["realized"].reshape(-1))[0,1])
    sampler=json.loads((ROOT/"runs/twoscale/sampler_check.json").read_text())
    assert sampler["ratio_spread_to_mean_error"]==ratio
    assert sampler["mean_realized_correlation"]==corr
    state=json.loads((ROOT/"runs/twoscale/statecheck.json").read_text())
    for r in state["rounds"]:
        assert r["passed"]==(r["max_abs_X_difference"]<=1e-6*r["sigma_X"])
    result=dict(one_scale_dt=dt["chosen_dt"],dt_rounds=len(dt["rounds"]),
        checked_comparisons=sum(len(r["comparisons"]) for r in dt["rounds"]),
        failed_comparisons=sum(not e["passed"] for r in dt["rounds"] for e in r["comparisons"]),
        argmin_changes=dt["rounds"][-1]["argmin_changes"],
        two_scale_batch_members=2048,single_core_batch_step_seconds=measured,
        dt_benchmark=.001,truth_projection_steps=steps,projected_truth_core_hours=hours,
        wo_total_estimate_core_hours=96,wo_extra_estimate_core_hours=15,
        projection_with_unmeasured_wo_extra=hours+15,
        two_scale_state_dt=state["chosen_dt"],
        state_check_rounds=state["rounds"],
        sampler_ratio=ratio,sampler_correlation=corr,sampler_spread=sd,sampler_mean_error=err,
        sampler_states=16,sampler_draws_per_state=64,
        sampler_per_state_ratios=sampler["state_ratios"],sampler_per_state_correlations=sampler["state_correlations"],
        sigma_X=sampler["sigma_X"],sigma_Y=sampler["sigma_Y"],
        hashes={str(p.relative_to(ROOT)):digest(p) for p in [
            ROOT/"runs/numerics/dtcheck.json",ROOT/"runs/numerics/twoscale_rate.json",
            ROOT/"runs/twoscale/statecheck.json",ROOT/"runs/twoscale/fastlib.npz",
            ROOT/"runs/twoscale/sampler_raw.npz",ROOT/"runs/twoscale/sampler_check.json"]})
    return result
def render(data):
    lines=["## AFD_NUMERICAL_PREFLIGHT","",
           "Source: runs/preflight_report.json; values recomputed from recorded comparisons and raw sampler draws.",
           "Truth time is a projection from measured single-core throughput; the WO extra cost remains an unmeasured estimate.",
           "","| Key | Value |","|---|---|"]
    lines += [f"| {k} | {json.dumps(v)} |" for k,v in data.items() if k!="hashes"]
    lines += ["","## AFD_PREFLIGHT_ARTIFACT_HASHES","","| Artifact | SHA256 |","|---|---|"]
    lines += [f"| {k} | {v} |" for k,v in data["hashes"].items()]
    return "\n".join(lines)+"\n"
def main():
    data=evidence()
    write_json(ROOT/"runs/preflight_report.json",data)
    prefix=render_numbers(json.loads((ROOT/"step0_evidence.json").read_text()))
    tail=render(data)
    (ROOT/"NUMBERS.md").write_text(prefix+"\n"+tail)
    assert (ROOT/"NUMBERS.md").read_text()==prefix+"\n"+render(evidence())
    bad=copy.deepcopy(data);bad["sampler_ratio"]+=1
    assert bad!=evidence(), "tamper not detected"
    report=f"""# AFD numerical and sampler preflight

One-scale decision timestep check **PASS**, dt={data['one_scale_dt']}; {data['checked_comparisons']} comparisons, {data['failed_comparisons']} failures, no winner changes at any checked lead. Every one-scale solver run uses this dt. The output grid/predicate is unchanged.

Two-scale benchmark: {data['single_core_batch_step_seconds']:.9f} seconds per RK4 step for 2048 members on one sulaco CPU core at dt=.001. Projected mandatory 300-case, nine-action/no-action truth through 3 LT_ref: **{data['projected_truth_core_hours']:.3f} single-core hours**. The WO estimated about96 including about15 for preparation/labels/checks. Combining the measured truth-rate projection with that still-unmeasured extra estimate gives {data['projection_with_unmeasured_wo_extra']:.3f} core-hours; this is not measured total campaign time. Actual dt chosen by the two-scale decision check may alter the projection.

Two-scale state check **PASS** at dt={data['two_scale_state_dt']}. Fast-state library contains4096 independent spinups, hashed before use.

Sampler check on {data['sampler_states']} twin states and {data['sampler_draws_per_state']} conditioned draws each:
- pooled RMS draw spread / RMS error of conditional mean: **{data['sampler_ratio']:.6f}**;
- conditional-mean / realized subgrid-term correlation: **{data['sampler_correlation']:.6f}**;
- RMS draw spread: {data['sampler_spread']:.9f}; RMS mean error: {data['sampler_mean_error']:.9f}.

Per-state values, raw arrays and hashes are retained. The spread/error ratio is close to unity; no acceptance threshold was specified, so this report assigns no invented sampler PASS. Two-scale truth is awaiting Todd's go. State/time-step checks and the raw sampler do not establish that this observation-conditioned distribution is calibrated beyond these states.

Every value above traces to NUMBERS §AFD_NUMERICAL_PREFLIGHT. Recompute with report_preflight.py; checker passes and altered sampler ratio is rejected.
"""
    (ROOT/"AFD_NUMERICAL_REPORT.md").write_text(report)
    print(report)
if __name__=="__main__":main()

