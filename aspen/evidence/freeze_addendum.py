"""Record numeric calibration and geometry before any held-out panels or training."""
import hashlib
import json

from common import ROOT,RESULTS,QUERY_NAMES


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    points=json.loads((RESULTS/"points.json").read_text())
    sensitivity=json.loads((RESULTS/"sensitivity.json").read_text())
    rows=["# AEA numeric freeze addendum — pre-panel / pre-training","",
          "Directions and parameters are fixed by Amendment1/1b and the committed centre sensitivity. "
          "Every generated endpoint was tested with the inherited64-start800-tu chaos gate. "
          "Failed points remain excluded with no substitution. Step0 was not rerun.","",
          f"Centre fixed lead: {sensitivity['h']:.17g} time units.","",
          "| Query | g_Re | g_A | g_alpha | Evaluable by sensitivity and chaos |",
          "|---|---|---|---|---|"]
    for qi,name in enumerate(QUERY_NAMES):
        g=points["g"][qi]
        rows.append(f"| {name} | {g[0]:.17g} | {g[1]:.17g} | {g[2]:.17g} | {points['evaluable_by_chaos'][qi]} |")
    rows += ["","| Point | Re | A | alpha | D_g | D_perp | lambda | CI low | CI high | Chaos pass |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for p in points["points"]:
        c=p["chaos"];t=p["theta"]
        values=[p["id"],*[f"{v:.17g}" for v in t],f"{p['D_g']:.17g}",f"{p['D_perp']:.17g}",
                str(c["lam"]),str(c["lam_ci95"][0]),str(c["lam_ci95"][1]),str(c["chaotic"])]
        rows.append("| "+" | ".join(values)+" |")
    rows += ["",f"Evaluable queries before attractor normalization: {points['n_evaluable']} of4.","",
             "| Source product | SHA256 |","|---|---|"]
    for p in [RESULTS/"points.json",RESULTS/"sensitivity.json",*sorted((RESULTS/"chaos").glob("*.json"))]:
        rows.append(f"| {p.relative_to(ROOT)} | {digest(p)} |")
    rows += ["","Report-only local sensitivities use independent point streams and cannot change these directions. "
             "Query normalization can only exclude an endpoint under Amendment1b; it cannot relocate it. "
             "All mandatory arms run at available points. Frozen otherwise applies if fewer3 queries remain."]
    target=ROOT/"AEA_FREEZE_CALIBRATION.md"
    content="\n".join(rows)+"\n"
    if target.exists() and target.read_text()!=content:raise RuntimeError("Numeric freeze is immutable")
    target.write_text(content)
    print(target)


if __name__=="__main__":main()
