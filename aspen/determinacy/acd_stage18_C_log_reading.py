"""Descriptive extraction of existing C training logs; no model or outcome access."""
import hashlib
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/stage18'
HEADING='\n## Part C saved training logs\n'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fmt(v):return format(v,'.8g') if isinstance(v,(int,float)) else str(v)
def run():
    selection=json.loads((OUT/'C_selection.json').read_text())
    models={}
    for selected in selection['rows']:
        name=selected['model'];directory=OUT/'training'/name
        meta=json.loads((directory/'complete.json').read_text())
        progress=json.loads((directory/'progress.json').read_text())
        skipfile=directory/'skips.json'
        skips=json.loads(skipfile.read_text()) if skipfile.exists() else []
        assert len(skips)==meta['skipped_updates']
        rows=[]
        for row in progress:
            assert row['step']%100==0
            components=row['microbatches']
            sizes=[(components[i+1]['microbatch_start'] if i+1<len(components) else 128)-m['microbatch_start'] for i,m in enumerate(components)]
            assert sum(sizes)==128
            def mean(key):
                values=[m[key] for m in components]
                if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in values):return 'nonfinite in saved log'
                return sum(v*n for v,n in zip(values,sizes))/sum(sizes)
            rows.append(dict(step=row['step'],base_loss=mean('base_loss'),paired_loss=mean('paired_loss'),preclip_gradient_norm=row['gradient_norm'],microbatches=components))
        allnorms={r['step']:r['preclip_gradient_norm'] for r in rows}
        allnorms.update({r['step']:r['gradient_norm'] for r in skips})
        windows=[]
        for skip in skips:
            start=max(1,skip['step']-500)
            norms=[dict(step=s,preclip_gradient_norm=n) for s,n in sorted(allnorms.items()) if start<=s<skip['step']]
            windows.append(dict(skip_step=skip['step'],window_start_inclusive=start,window_end_exclusive=skip['step'],recorded_preclip_norms=norms,recorded_updates=len(norms),unrecorded_updates=skip['step']-start-len(norms)))
        sources=[directory/'complete.json',directory/'progress.json']+([skipfile] if skipfile.exists() else [])
        models[name]=dict(weight=selected['weight'],initial_normal_base=meta['normal_base'],initial_normal_paired=meta['normal_difference'],initial_base_over_paired=meta['normal_base']/meta['normal_difference'],
            normalization_scope='Measured initial mean base loss / initial mean paired loss from frozen initial normalization batches; raw paired losses below are before normalization and weight.',
            progress_every_100_updates=rows,skips=skips,skip_steps=[s['step'] for s in skips],pre_skip_gradient_windows=windows,
            gradient_logging='Every scheduled hundredth update and every skip only. Unrecorded updates are unavailable; no interpolation or reconstruction.',
            source_hashes={str(p.relative_to(ROOT)):sha(p) for p in sources})
    receipt=dict(post_hoc=True,descriptive_only=True,criteria_unchanged=True,licenses_frozen_route=False,source_code_sha256=sha(Path(__file__)),models=models)
    (ROOT/'receipts/acd_stage18_C_training_logs.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(10,8),sharex=True)
    for ax,(name,m) in zip(axes.flat,models.items()):
        for key,label,style,marker in [('base_loss','base','-','o'),('paired_loss','paired (raw)','--','s')]:
            points=[(r['step'],r[key]) for r in m['progress_every_100_updates'] if isinstance(r[key],(int,float)) and r[key]>0 and math.isfinite(r[key])]
            ax.plot([p[0] for p in points],[p[1] for p in points],color='black',linestyle=style,marker=marker,markevery=max(1,len(points)//12),markersize=3,linewidth=.8,label=label)
        for s in m['skip_steps']:ax.axvline(s,color='.55',linestyle=':',linewidth=.5)
        ax.set_yscale('log');ax.set_title('weight '+format(m['weight'],'g'));ax.set_xlabel('scheduled update');ax.set_ylabel('logged loss');ax.legend(fontsize=7)
    fig.tight_layout()
    for ext in ['pdf','png']:fig.savefig(ROOT/'figures'/('F_stage18_C_training_losses.'+ext),dpi=150)
    plt.close(fig)
    body=HEADING+'\nPOST HOC, descriptive only; criteria unchanged. These readings extract existing logs, without training, inference, outcome access or loss recomputation. Base and raw paired losses are logged microbatch component means, weighted by saved microbatch size. Plot: figures/F_stage18_C_training_losses.pdf (both losses on a logarithmic scale; solid circles for base, dashed squares for paired; dotted vertical lines mark skips). Nonfinite logged loss points cannot be placed on a log axis and remain explicit in the receipt.\n\n'
    body+='| Weight | Measured initial base | Measured initial paired | Base / paired | Every skipped update |\n|---:|---:|---:|---:|---|\n'
    for m in models.values():body+=f"| {fmt(m['weight'])} | {fmt(m['initial_normal_base'])} | {fmt(m['initial_normal_paired'])} | {fmt(m['initial_base_over_paired'])} | {', '.join(map(str,m['skip_steps'])) or 'none'} |\n"
    body+='\nThe normalizer ratio is measured before response weighting. The loss plot uses raw paired components rather than the normalized weighted contribution.\n\nPreclip gradient norms were saved every hundredth update and at skips, not at every update. The table lists every available sample in the preceding half-open 500-update window, and the skip’s own norm separately. Missing norms are not reconstructed.\n\n| Weight | Skip update | Reason | Norm at skip | Recorded preceding update:norm samples | Unrecorded updates in window |\n|---:|---:|---|---|---|---:|\n'
    for m in models.values():
        for s,w in zip(m['skips'],m['pre_skip_gradient_windows']):
            samples=', '.join(str(x['step'])+':'+fmt(x['preclip_gradient_norm']) for x in w['recorded_preclip_norms'])
            body+=f"| {fmt(m['weight'])} | {s['step']} | {s['reason']} | {fmt(s['gradient_norm'])} | {samples or 'none'} | {w['unrecorded_updates']} |\n"
    body+='\nAll hundred-update base and paired loss values, microbatch records, skip records and source hashes are retained in receipts/acd_stage18_C_training_logs.json.\n'
    p=ROOT/'ACD_STAGE18_READING.md';text=p.read_text()
    if HEADING in text:
        start=text.index(HEADING);end=text.find('\n## ',start+len(HEADING));text=text[:start]+(text[end:] if end!=-1 else '')
    p.write_text(text.rstrip()+'\n'+body)
    return receipt
if __name__=='__main__':
    r=run()
    print(json.dumps({n:dict(ratio=m['initial_base_over_paired'],skip_steps=m['skip_steps'],loss_samples=len(m['progress_every_100_updates'])) for n,m in r['models'].items()},indent=2))
