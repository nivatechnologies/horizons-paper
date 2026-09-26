"""Build the EXT2 (learned-tokenizer kill test) section of the vault results note from result files (no retyped numbers).

Writes results/ext2/results_note_ext2.md. Every number is read from a committed result file under results/ext2/ (and
results/ext/kolmo/ for the k-means rows through k3_kmeans.csv); the source path is printed under each table.
"""
import csv
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from th import config  # noqa: E402

R = config.RESULTS / "ext2"


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


def freeze_commit():
    r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%h", "--", "ext2/ext2_freeze.yaml"], cwd=config.PKG,
                       capture_output=True, text=True)
    return r.stdout.split()[-1] if r.stdout.split() else "?"


def main():
    L = ["", "## EXT2: learned-tokenizer kill test (WO 2026-09-25)", "",
         f"Generated from result files by `ext2/scripts/ext2_results_note.py`; NUMBERS.md section K3 holds the full "
         f"tables. Freeze commit `{freeze_commit()}` (ext2/EXT2_FREEZE.md, ext2_freeze.yaml), made before any training "
         f"beyond a 300-step timing pilot. Gate report: ext2/EXT2_GATE.md. Kolmogorov Re 40, 64², the 1,000 KKE3 "
         f"confirmation states; W = 27. Labels: bound / reference / learned / estimate. **T_pt is perfect next-token "
         f"prediction (reference); it is not a bound.**", ""]
    # tokenizers
    p = R / "k3_tokenizers.csv"
    t = rd(p)
    L += ["### Tokenizers (FSQ autoencoders, one seed each)", "",
          "| Config | Levels | Codes/token | Bits/frame | Params enc / dec | Train time (min) | Best step | Held-out rel. RMS | "
          "Held-out within 0.1 | Code utilization | Level usage |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in t:
        L.append(f"| {r['config']} | {r['levels']} | {r['codes_per_token']} | {f(r['bits_per_frame'], 1)} | "
                 f"{r['params_encoder']} / {r['params_decoder']} | {f(float(r['train_seconds']) / 60, 1)} | {r['best_step']} | "
                 f"{f(r['heldout_rel_rms'], 4)} | {f(r['heldout_share_within_eps0.1'])} | {f(r['code_utilization'], 4)} "
                 f"({r['codes_used']}) | {r['level_usage']} |")
    L.append(f"\nHeld-out = calibration held-out split ({t[0]['heldout_states']} states, {t[0]['heldout_traj']} "
             f"trajectories). Null reconstruction (calibration mean): relative RMS {f(t[0]['null_mean_rel_rms'])}; zero "
             f"field {f(t[0]['null_zero_rel_rms'])}. Quantizer parameters: 0 (FSQ). Label: learned.")
    L.append(src(p))
    # M1
    p = R / "k3_recon.csv"
    L += ["### M1 reconstruction at t = 0 (confirmation states)", "",
          "| Config | Rel. RMS | Median | Within 0.1 | Within 0.3 | Within 0.5 |", "|---|---|---|---|---|---|"]
    for r in rd(p):
        L.append(f"| {r['config']} | {f(r['recon_rms'], 4)} | {f(r['recon_median'], 4)} | {f(r['share_within_eps0.1'])} | "
                 f"{f(r['share_within_eps0.3'])} | {f(r['share_within_eps0.5'])} |")
    L.append(src(p))
    # M2-M5 primary
    p = R / "k3_paired.csv"
    pr = rd(p)
    rows = rd(R / "k3_rows.csv")

    def pers(c, d, e, s):
        x = [r for r in rows if r["config"] == c and r["delta"] == d and r["eps"] == e and r["start"] == s
             and r["kind"] == "persistence"]
        return f(x[0]["restricted_mean"]) if x else ""

    L += ["### M2-M5 at Δ = 0.35 (primary score: future frames; secondary: from t = 0)", "",
          "d = decode-and-integrate − T_pt, paired over trajectories. R1 = vocabulary binds (d ≥ 0.25, 95% > 0); "
          "R2 = does not bind (90% within ±0.10, or T_pt above DI).", "",
          "| Config | ε | T_pt | DI | Persistence | d [95%] | Outlast | Reading (primary) | Reading (from t = 0) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in pr:
        if r["delta"] != "0.35" or r["start"] != "future":
            continue
        sec = [x for x in pr if x["config"] == r["config"] and x["delta"] == "0.35" and x["eps"] == r["eps"]
               and x["start"] == "from_t0"][0]
        L.append(f"| {r['config']} | {r['eps']} | {f(r['T_pt'])} | {f(r['DI'])} | {pers(r['config'], '0.35', r['eps'], 'future')} | "
                 f"{f(r['diff_DI_minus_Tpt'])} [{f(r['ci95_lo'])}, {f(r['ci95_hi'])}] | {f(r['outlast_DI_over_Tpt'])} | "
                 f"{r['reading']} | {sec['reading']} |")
    L.append("\nS(τ) for T_pt and DI, and all Δ, are in K3D. Labels: T_pt, DI, persistence reference; d estimate.")
    counts = {}
    for r in pr:
        if r["delta"] != "0.35":
            counts.setdefault((r["delta"], r["start"]), {}).setdefault(r["reading"], 0)
            counts[(r["delta"], r["start"])][r["reading"]] += 1
    if counts:
        L.append("\nSecondary Δ (reading counts over configurations × ε): " + "; ".join(
            f"Δ {d} {s}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())) for (d, s), c in sorted(counts.items())) + ".")
    L.append(src(p))
    # M6
    p = R / "k3_kmeans.csv"
    L += ["### M6 beside k-means patch codebooks (Δ = 0.35, future frames; descriptive, no reading)", "",
          "| Config (bits) | k-means (bits) | ε | FSQ T_pt | FSQ DI | k-means ceiling (bound) | k-means p₀ | k-means DI |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rd(p):
        if r["delta"] == "0.35" and r["start"] == "future" and r["eps"] in ("0.1", "0.3"):
            L.append(f"| {r['config']} ({f(r['fsq_bits'], 1)}) | {r['kmeans']} ({f(r['kmeans_bits'], 0)}) | {r['eps']} | "
                     f"{f(r['fsq_T_pt'])} | {f(r['fsq_DI'])} | {f(r['kmeans_ceiling'])} {r['kmeans_ceiling_ci95']} | "
                     f"{f(r['kmeans_p0'])} | {f(r['kmeans_DI'])} |")
    L.append(src(p))
    # kill table
    p = R / "k3_kill.csv"
    L += ["### Kill criterion: R1 at ε = 0.1 (Δ = 0.35, future frames)", "",
          "| Config | Codes/token | Literal set | R1 | Reading | d [95%] | Reading from t = 0 |", "|---|---|---|---|---|---|---|"]
    sets = []
    for r in rd(p):
        if r["config"].startswith("SET"):
            sets.append(r)
            continue
        L.append(f"| {r['config']} | {r['codes_per_token']} | {r['in_literal_set']} | {r['R1_eps0_1_primary']} | "
                 f"{r['reading_eps0_1_primary']} | {f(r['diff_eps0_1_primary'])} {r['ci95_eps0_1_primary']} | "
                 f"{r['reading_eps0_1_secondary']} |")
    L.append("")
    for s in sets:
        L.append(f"- {s['config'][4:]}: R1 in any member = **{s['R1_eps0_1_primary']}** ({s['reading_eps0_1_primary']}).")
    agree = len({s["R1_eps0_1_primary"] for s in sets}) == 1
    met = agree and sets[0]["R1_eps0_1_primary"] == "False"
    L += ["", "The WO's kill criterion fires if R1 fails at ε = 0.1 for every configuration with at least 2^10 codes per "
          "token. The gate found the eligible set unpinned (the b10 FSQ level set has 1,000 < 1,024 codes), so the executor "
          "does not issue the verdict; both sets are shown. " +
          ("**Both candidate sets give the same outcome: R1 fails for every member, so the WO's kill condition is met "
           "under either referent.** " if met else
           "Both candidate sets give the same outcome. " if agree else "**The two candidate sets disagree.** ") +
          "**Decision: Todd.**", src(p)]
    out = "\n".join(L) + "\n"
    (R / "results_note_ext2.md").write_text(out)
    print(out)


if __name__ == "__main__":
    main()
