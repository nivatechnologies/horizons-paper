"""Generate measured results separately, preserving the audit history and vault append path."""
import csv
import json

from common import ROOT,RESULTS


def rows(name):
    path=RESULTS/name
    if not path.exists():return []
    with path.open() as f:return list(csv.DictReader(l for l in f if not l.startswith("#")))


def table(source,columns):
    data=rows(source)
    if not data:return "Unavailable: no produced source table.\n"
    text="| "+" | ".join(columns)+" |\n|"+"---|"*len(columns)+"\n"
    for row in data:
        values=[]
        for key in columns:
            value=row[key]
            if value:
                try:value=f"{float(value):.4g}"
                except ValueError:pass
            values.append(value or "unavailable")
        text+="| "+" | ".join(values)+" |\n"
    return text+f"\nSource: aspen/evidence/results/{source}; checked in NUMBERS.md.\n"


def main():
    summary=json.loads((RESULTS/"summary.json").read_text())
    outcome=summary["outcome"]
    text=(
        "## GB10 execution results — Amendment 1b\n\n"
        f"Frozen outcome: **{outcome}**. Evaluable queries: **{summary['n_evaluable']} of 4**. "
        f"Complete arm panel: **{summary['complete_arm_panel']}**. "
        "Step 0 was retained without rerunning.\n\n"
        "The experiment uses the amended fixed-lead sensitivity and inherited 8-frame L_range / "
        "4-frame FNO-θ inputs, with three parameter channels only for FNO-θ. All arms use the "
        "same physical query functional at each test θ; its explicit parameter factors are "
        "evaluation constants, not additional inputs to L_range or the identifier. "
        "Point errors use each point's 0.5-Lyapunov-time lead and 100 independent states. "
        "The law uses all 11 observations and exactly 270 misfit evaluations per state.\n\n"
        "45° points, ensemble disagreement and context identifiability were cut in the specified "
        "order before data. This is one selector framing with four queries; a negative is not "
        "four independent negative findings. Selector provenance and exact query overlap remain "
        "in CODEX_QUERIES.md, QUERY_OVERLAP.md and the gate appendix.\n\n"
        "### Every-point chaos gate\n\n"
        +table("chaos.csv",["point","Re","A","alpha","lam","ci_lo","ci_hi","chaotic"])
        +"\n### Endpoint ratios\n\n"
        +table("ratios.csv",["query","arm","error_0","error_90","ratio","symmetric_ratio","available"])
        +"\n### Index and baselines\n\n"
        +table("correlations.csv",["arm","n_units","rho_g","rho_perp","gap","rho_euclidean","rho_mahalanobis"])
        +"\nThe partial correlation controlling λ(θ)·h is unavailable because that control equals "
        "0.5 at every point. Unavailable statistics satisfy no outcome clause. "
        "No epsilon denominator or excluded-point substitution is used.\n\n"
        +"### Learned recipe and cost\n\n"
        +table("training.csv",["arm","steps","n_in","param_channels","params","best_step","best_val","train_seconds"])
        +"\n### Figures and provenance\n\n"
        "Greyscale figures: aspen/evidence/figures/AEA1_error_angle.png, AEA2_error_displacement.png, "
        "AEA3_index_baselines.png, with SVG equivalents. Mean normalized query errors and state-bootstrap "
        "95% intervals are in AEA-E. Centre and reported local gradients are in AEA-G and AEA-GP. "
        "Tables use inherited NUMBERS column/section validation, producing commit SHAs and source SHA256 hashes.\n"
    )
    if outcome=="otherwise":
        text+="\nThe frozen PASS/KILL rules return otherwise; Todd decides the next stage.\n"
    if not summary["complete_arm_panel"]:
        text+="\nArm comparisons are incomplete and cannot be presented as measured PASS or KILL.\n"
    (ROOT/"RUN_RESULTS.md").write_text(text)
    historical=(ROOT/"QUERY_OVERLAP.md").read_text()+"\n\n"+(ROOT/"AEA_GATE.md").read_text()
    gate=(ROOT/"AEA_GATE_AMENDMENT1B.md").read_text()
    (ROOT/"R_Aspen-Evidence-Alignment-Kill-Test-2026-10.md").write_text(
        "# Aspen evidence-alignment kill test — October 2026\n\n"+text+
        "\n\n## Protocol and gate record\n\n"+gate+"\n\n## Historical pre-correction audit\n\n"+historical)
    print(ROOT/"RUN_RESULTS.md")


if __name__=="__main__":main()
