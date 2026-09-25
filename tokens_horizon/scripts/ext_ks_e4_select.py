"""Post-freeze extension, KS E4 candidate evaluation and selection (ext_freeze.yaml ks.e4; Amendment 2 B2).

VALIDATION panel only (300 states of the validation block; no confirmation data). Candidates: patch-product
configurations with >= 2^10 codes per token and >= 16 tokens per frame: P in {16, 32}, b in {10, 12, 14, 16}, both
KS systems, all three Delta. Per candidate: certified exact bound (th/ks_eval.bound on the validation panel), eps 0.3,
future frames: restricted mean, S_out(1), no-cross fraction, p_0.
Selection: smallest total bits P*b among candidates with validation restricted-mean bound < 1 Lyapunov time; equal-rate
order (B2.2): L = 22 first, primary Delta first, lower validation mean, configuration ID lexical. None -> no learned
cell, with the B2.1 wording. Contrast (B2.3): smallest-bits configuration with the same system, family, P and Delta,
more total bits, validation mean >= 3 and validation S_out(1) >= 0.9; none -> no contrast (B2.4). No training here.

Usage: python scripts/ext_ks_e4_select.py <device>
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402
from th import ks_eval as E   # noqa: E402

OUTR = config.RUNS / "ext" / "ks" / "e4_validation"
OUTD = config.RESULTS / "ext" / "ks"


def cid(s, P, b, d):
    return f"{s}_P{P}_b{b}_d{d:g}"


def main(device):
    OUTR.mkdir(parents=True, exist_ok=True)
    cands = []
    for s in ("ks22", "ks100"):
        spec = K.ks_spec(s)
        sA = E.sigma_A(s)
        for P in (16, 32):
            for b in (10, 12, 14, 16):
                if not (E.CB / f"{s}_patch_P{P}_b{b}.npz").exists():
                    print("codebook not yet available:", s, P, b, flush=True)
                    continue
                tok = E.Tok(f"{s}_patch_P{P}_b{b}")
                for d in [float(x) for x in spec["frame_intervals"]]:
                    c = cid(s, P, b, d)
                    f = OUTR / f"{c}.json"
                    if f.exists():
                        cands.append(json.loads(f.read_text()))
                        continue
                    out, dC0, cnt = E.bound(tok, s, "validation", d, sA, device)
                    H, cr = out[0.3]["future"]
                    np.savez(OUTR / f"{c}.npz", H=H, crossed=cr, dC0=dC0)
                    rec = dict(config_id=c, system=s, P=P, b=b, total_bits=P * b, delta=d,
                               primary_delta=d == float(spec["primary_delta"]), n_states=int(len(H)),
                               val_restricted_mean=float(H.mean()), val_frac_no_cross=float(1 - cr.mean()),
                               val_p0=float(out[0.3]["p0"].mean()), **{f"val_{k}": v for k, v in E.survival(H, cr).items()},
                               counters=cnt)
                    f.write_text(json.dumps(rec, indent=1))
                    cands.append(rec)
                    print(c, round(rec["val_restricted_mean"], 3), round(rec["val_S1"], 3), flush=True)
    if len(cands) < 48:
        print(f"only {len(cands)} of 48 candidates evaluated; selection not run", flush=True)
        return
    # selection
    qual = [c for c in cands if c["val_restricted_mean"] < 1.0]

    def order(c):
        return (c["total_bits"], 0 if c["system"] == "ks22" else 1, 0 if c["primary_delta"] else 1,
                c["val_restricted_mean"], c["config_id"])
    selected = sorted(qual, key=order)[0] if qual else None
    contrast = None
    if selected:
        pool = [c for c in cands if c["system"] == selected["system"] and c["P"] == selected["P"]
                and c["delta"] == selected["delta"] and c["total_bits"] > selected["total_bits"]
                and c["val_restricted_mean"] >= 3.0 and c["val_S1"] >= 0.9]
        contrast = sorted(pool, key=lambda c: (c["total_bits"], c["config_id"]))[0] if pool else None
    res = dict(
        label="post-freeze extension; E4 selection on the validation panel (bound, validation block only)",
        git_sha=config.git_sha(),
        exposure_record=("no validation bound was computed or inspected before the equal-rate selection order was "
                         "frozen in d960d0b (Amendment 2 B2.2); validation bounds were first computed by this script"),
        rule=K.ext_freeze()["ks"]["e4"]["selection"], contrast_rule=K.ext_freeze()["ks"]["e4"]["contrast"],
        candidates=sorted(cands, key=order),
        n_qualifying=len(qual),
        selected=selected["config_id"] if selected else "none",
        selected_record=selected,
        selection_statement=(None if selected else
                             "No tested configuration satisfying the E4 size requirements had a validation restricted-mean support horizon below one Lyapunov time."),
        contrast=contrast["config_id"] if contrast else "none",
        contrast_record=contrast,
        contrast_statement=(None if contrast or not selected else
                            "No support-permissive contrast exists in the tested grid; no contrast is trained and the grid is not extended."),
    )
    (OUTD / "e4_selection.json").write_text(json.dumps(res, indent=1, default=float))
    keys = ["config_id", "system", "P", "b", "total_bits", "delta", "primary_delta", "n_states", "val_restricted_mean",
            "val_S1", "val_S3", "val_S10", "val_frac_no_cross", "val_p0"]
    with open(OUTD / "e4_candidates_validation.csv", "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n")
        w = csv.DictWriter(fh, keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(cands, key=order))
    print("selected", res["selected"], "contrast", res["contrast"])


if __name__ == "__main__":
    main(sys.argv[1])
