"""Greyscale figures from AEA source tables, with markers and direct labels."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import ROOT,RESULTS,QUERY_NAMES


def rows(name):
    path=RESULTS/name
    if not path.exists():return []
    with path.open() as f:return list(csv.DictReader(l for l in f if not l.startswith("#")))


def save(fig,name):
    out=ROOT/"figures";out.mkdir(exist_ok=True)
    fig.tight_layout();fig.savefig(out/(name+".png"),dpi=180);fig.savefig(out/(name+".svg"));plt.close(fig)


def main():
    error=rows("errors.csv")
    plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False})
    styles={"L_range-3":("o","-"),"FNO-theta":("s","--"),"law":("^","-."),
            "persistence":("x",":"),"centre-law":("D","--")}
    fig,axes=plt.subplots(2,2,figsize=(11,7))
    for ax,q in zip(axes.flat,QUERY_NAMES):
        for a,(marker,line) in styles.items():
            selected=[r for r in error if r["query"]==q and r["arm"]==a and r["angle"]!="centre" and r["error"]]
            selected.sort(key=lambda r:int(r["angle"]))
            if not selected:continue
            x=np.array([int(r["angle"]) for r in selected]);y=np.array([float(r["error"]) for r in selected])
            lo=np.array([float(r["ci_lo"]) for r in selected]);hi=np.array([float(r["ci_hi"]) for r in selected])
            ax.errorbar(x,y,yerr=[y-lo,hi-y],fmt=marker,color="black",linestyle=line,capsize=2,label=a)
            ax.annotate(a,(x[-1],y[-1]),xytext=(5,0),textcoords="offset points",fontsize=7)
        ax.set_title(q);ax.set_xlabel("Generating ray angle (degrees)");ax.set_ylabel("Mean query error / attractor SD")
        ax.set_xticks([0,90]);ax.margins(x=.25)
    fig.suptitle("AEA: fixed 0°/90° rays; 45° panel cut before data",fontsize=11)
    save(fig,"AEA1_error_angle")
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,term in zip(axes,["D_g","D_perp"]):
        for a,(marker,_) in styles.items():
            selected=[r for r in error if r["arm"]==a and r["error"] and r["evaluable"]=="True"]
            ax.scatter([float(r[term]) for r in selected],[float(r["error"]) for r in selected],
                       marker=marker,color="black",s=30,label=a,alpha=.75)
        ax.set_xlabel(term);ax.set_ylabel("Mean normalized query error");ax.legend(fontsize=7)
    save(fig,"AEA2_error_displacement")
    corr=rows("correlations.csv")
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,a in zip(axes,["L_range-3","FNO-theta"]):
        found=[r for r in corr if r["arm"]==a]
        if found:
            row=found[0]
            for k,(field,label) in enumerate([("rho_g","D_g"),("rho_perp","D_perp"),
                                             ("rho_euclidean","Euclidean"),("rho_mahalanobis","Mahalanobis")]):
                if row[field]:
                    value=float(row[field]);ax.bar(k,value,color="white",edgecolor="black",hatch=["/","\\","x","."][k])
                    ax.text(k,value,f"{value:.2f}",ha="center",va="bottom" if value>=0 else "top")
                else:ax.text(k,0,"unavailable",ha="center",rotation=90,fontsize=7)
        ax.set_title(a);ax.set_xticks(range(4),["D_g","D_perp","Euclidean","Mahalanobis"])
        ax.set_ylabel("Spearman(error, predictor)");ax.set_ylim(-1,1);ax.axhline(0,color="black",linewidth=.5)
    fig.suptitle("Ensemble disagreement and identifiability cut before data",fontsize=10)
    save(fig,"AEA3_index_baselines")


if __name__=="__main__":main()
