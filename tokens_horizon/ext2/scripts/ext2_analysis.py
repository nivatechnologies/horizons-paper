"""EXT2 analysis: M1 table, horizon rows (M2-M4), M5 paired comparison and readings, M6 k-means comparison, kill table.

Reads runs/ext2/measure/<config>[tag].{json,npz} (tag "_lr1e-4" when the first run diverged) and the KKE3 rows
(results/ext/kolmo/e3_rows.csv). Writes results/ext2/:
  k3_recon.csv      M1 per configuration (confirmation states, t = 0)
  k3_rows.csv       M2 perfect next-token prediction (reference), M3 decode-and-integrate, M4 persistence
  k3_paired.csv     M5: d = M3 - M2 (paired bootstrap over the 1,000 confirmation trajectories; 2,000 reps, seed 777),
                    90/95% intervals, reading (R1 / R2 / none), strict outlast share, S(1, 3, 10) for M2 and M3
  k3_kmeans.csv     M6 descriptive: FSQ T_pt and DI beside the k-means ceiling and DI at the same layout, nearest bits
  k3_kill.csv       R1 at eps 0.1 (primary score, Delta 0.35) per configuration with both candidate eligible sets;
                    the verdict is not issued (gate: eligible set unpinned)
Readings (ext2_freeze.yaml): R1 = frozen 'well below' on d (d >= 0.25, lower 95% > 0); R2 = approximately equal
(90% within +-0.10) or T_pt above DI (upper 95% of d < 0); otherwise none.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fsq_ae import CONFIGS  # noqa: E402
from th import config, score  # noqa: E402
from th import kolmo_eval as E  # noqa: E402

M = config.RUNS / "ext2" / "measure"
TRAIN = config.RUNS / "ext2" / "train"
RES = config.RESULTS / "ext2"
KMEANS_B = {"L8-b10": ("8x8", 10), "L8-b12": ("8x8", 12), "L8-b16": ("8x8", 16), "L16-b10": ("16x16", 10),
            "L16-b12": ("16x16", 12)}
LITERAL = {n for n, (_, lv) in CONFIGS.items() if int(np.prod(lv)) >= 2 ** 10}


def tag_of(name):
    info = json.loads((TRAIN / name / "info.json").read_text())
    return "_lr1e-4" if info["diverged"] else ""


def write(name, rows, note):
    RES.mkdir(parents=True, exist_ok=True)
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    with open(RES / name, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; EXT2 learned-tokenizer kill test; {note}\n")
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def reading(pd):
    m = config.freeze()["margins"]
    hw, wb = m["approx_equal"]["half_width"], m["well_below"]["min_diff"]
    if pd["diff"] >= wb and pd["ci95"][0] > 0:
        return "R1"
    if pd["ci90"][0] >= -hw and pd["ci90"][1] <= hw:
        return "R2 (approximately equal)"
    if pd["ci95"][1] < 0:
        return "R2 (T_pt above decode-and-integrate)"
    return "none"


def main():
    names = [n for n in CONFIGS if (TRAIN / n / "info.json").exists() and (M / f"{n}{tag_of(n)}.json").exists()]
    recon, rows, paired, kill = [], [], [], []
    for n in names:
        t = tag_of(n)
        js = json.loads((M / f"{n}{t}.json").read_text())
        z = np.load(M / f"{n}{t}.npz")
        side, lv = CONFIGS[n]
        codes = int(np.prod(lv))
        bits = side * side * float(np.log2(codes))
        base = dict(config=n, latent=f"{side}x{side}", codes_per_token=codes, bits_per_frame=bits)
        recon.append(dict(base, **js["m1"], fallback_lr=bool(t), label="learned"))
        for r in js["rows"]:
            rows.append(dict(base, delta=r["delta"], eps=r["eps"], start=r["start"], kind=r["kind"], label=r["label"],
                             restricted_mean=r["restricted_mean"], ci95_lo=r["ci95_lo"], ci95_hi=r["ci95_hi"],
                             frac_no_cross=r["frac_no_cross"], median=r["median"], S1=r.get("S1"), S3=r.get("S3"),
                             S10=r.get("S10"), n=r["n"]))
        for d in (0.35, 0.14, 0.7):
            for e in E.EPS:
                for start in ("future", "from_t0"):
                    k = f"d{d:g}_eps{e}_{start}"
                    Hpt, cpt = z[f"perfect_token_{k}_H"], z[f"perfect_token_{k}_crossed"]
                    Hdi, cdi = z[f"decode_and_integrate_{k}_H"], z[f"decode_and_integrate_{k}_crossed"]
                    pd = score.paired_diff(Hdi, Hpt)
                    sp, sd = E.survival(Hpt, cpt), E.survival(Hdi, cdi)
                    rd = reading(pd)
                    paired.append(dict(base, delta=d, eps=e, start=start, primary_score=start == "future",
                                       T_pt=float(Hpt.mean()), DI=float(Hdi.mean()), diff_DI_minus_Tpt=pd["diff"],
                                       ci90_lo=pd["ci90"][0], ci90_hi=pd["ci90"][1], ci95_lo=pd["ci95"][0],
                                       ci95_hi=pd["ci95"][1], reading=rd,
                                       outlast_DI_over_Tpt=float((Hdi > Hpt).mean()), ties=float((Hdi == Hpt).mean()),
                                       **{f"Tpt_{s}": v for s, v in sp.items()}, **{f"DI_{s}": v for s, v in sd.items()},
                                       label="estimate"))
        pr = {(p["eps"], p["start"]): p for p in paired if p["config"] == n and p["delta"] == 0.35}
        kill.append(dict(base, levels=str(lv), in_literal_set=n in LITERAL, in_nominal_set=True,
                         R1_eps0_1_primary=pr[(0.1, "future")]["reading"] == "R1",
                         reading_eps0_1_primary=pr[(0.1, "future")]["reading"],
                         diff_eps0_1_primary=pr[(0.1, "future")]["diff_DI_minus_Tpt"],
                         ci95_eps0_1_primary=f"[{pr[(0.1, 'future')]['ci95_lo']:.4f}, {pr[(0.1, 'future')]['ci95_hi']:.4f}]",
                         reading_eps0_1_secondary=pr[(0.1, "from_t0")]["reading"],
                         label="estimate (reading); verdict not issued"))
    for setname, members in (("literal (>= 1,024 codes per token)", LITERAL), ("nominal (all five; b10 = FSQ ~2^10)", set(CONFIGS))):
        got = [k for k in kill if k["config"] in members]
        kill.append(dict(config=f"SET {setname}", in_literal_set="", in_nominal_set="",
                         R1_eps0_1_primary=any(k["R1_eps0_1_primary"] for k in got) if got else "",
                         reading_eps0_1_primary=f"members measured: {len(got)}/{len(members)}",
                         label="descriptive; kill verdict not issued by the executor (gate check 3), decision: Todd"))
    # M6: k-means rows
    km = [r for r in csv.DictReader(l for l in open(config.RESULTS / "ext" / "kolmo" / "e3_rows.csv") if not l.startswith("#"))
          if r["family"] == "patch"]
    comp = []
    for n in names:
        lay, b = KMEANS_B[n]
        for d in (0.35, 0.14, 0.7):
            for e in E.EPS:
                for start in ("future", "from_t0"):
                    p = [x for x in paired if x["config"] == n and x["delta"] == d and x["eps"] == e and x["start"] == start][0]
                    sel = [r for r in km if r["layout"] == lay and int(r["b"]) == b and abs(float(r["delta"]) - d) < 1e-9
                           and float(r["eps"]) == e and r["start"] == start]
                    kb = [r for r in sel if r["kind"] == "bound"][0]
                    kd = [r for r in sel if r["kind"] == "decode_and_integrate"][0]
                    comp.append(dict(config=n, fsq_bits=p["bits_per_frame"], kmeans=f"{lay} b{b}",
                                     kmeans_bits=float(kb["total_bits"]), delta=d, eps=e, start=start,
                                     fsq_T_pt=p["T_pt"], fsq_DI=p["DI"], kmeans_ceiling=float(kb["restricted_mean"]),
                                     kmeans_ceiling_ci95=f"[{float(kb['ci95_lo']):.4f}, {float(kb['ci95_hi']):.4f}]",
                                     kmeans_p0=float(kb["p0"]), kmeans_DI=float(kd["restricted_mean"]),
                                     kmeans_DI_ci95=f"[{float(kd['ci95_lo']):.4f}, {float(kd['ci95_hi']):.4f}]",
                                     label="descriptive (k-means ceiling = bound; T_pt and DI = reference); no reading"))
    write("k3_recon.csv", recon, "M1 on the 1,000 confirmation states at t = 0")
    write("k3_rows.csv", rows, "M2 perfect next-token prediction (reference, not a bound), M3, M4")
    write("k3_paired.csv", paired, "M5; d = M3 - M2; readings per ext2_freeze.yaml")
    write("k3_kmeans.csv", comp, "M6 descriptive")
    write("k3_kill.csv", kill, "R1 at eps 0.1, Delta 0.35, future frames; verdict not issued")
    for p in paired:
        if p["delta"] == 0.35 and p["start"] == "future":
            print(f"{p['config']:8s} eps {p['eps']}: T_pt {p['T_pt']:.3f} DI {p['DI']:.3f} d {p['diff_DI_minus_Tpt']:+.3f} "
                  f"[{p['ci95_lo']:+.3f}, {p['ci95_hi']:+.3f}] {p['reading']}")


if __name__ == "__main__":
    main()
