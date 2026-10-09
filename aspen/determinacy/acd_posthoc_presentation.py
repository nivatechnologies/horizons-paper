"""Presentation/documentation from committed receipts; no scoring or inference."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    receipt=ROOT/'receipts/acd_stage21_R12_recovery.json'
    d=json.loads(receipt.read_text());retained=len(d['models']['posterior']['pooled']['case_indices'])
    document_rows=[]
    lines=['## POST HOC — R1 and R2 definition note','','R1 and R2 concern the seven zero-mean patterns at 2 LT. Each instance/seed pair contributes only when both pipelines give at least one confident answer. Defined seed differences are averaged within each instance, then those instance means are averaged across contributing instances. This differs from pooling individual answers.']
    for reading,comparator in [('R1','CNN-F-constantF'),('R2','CNN-noF')]:
        r=d['confirmatory'][reading]
        lines += ['',f'{reading}: {r["contributing_instances"]} contributing instances out of {retained} retained. Comparator: {comparator}; comparison: comparator error minus E0-fixed error. Estimate {r["interval"]["point"]}; two-sided 99% instance betting interval [{r["interval"]["lower"]}, {r["interval"]["upper"]}]. Source: receipts/acd_stage21_R12_recovery.json $.confirmatory.{reading}.',
        '',f'| POST HOC {reading} pipeline | Population | Case-averaged seven-pattern confident error | Pooled seven-pattern confident error | Receipt key |', '|---|---|---:|---:|---|']
        for name in [comparator]+[f'CNN-F-E0-fixed-seed{i}' for i in range(1,6)]:
            for group in ['pooled','F7','F9']:
                readings=d['models'][name][group]['pattern_group_readings']
                index,row=next((i,r) for i,r in enumerate(readings) if r['lead']==2. and r['population']=='seven_zero_mean')
                a=row['accuracy'];case=1-a['case_accuracy'] if a['case_accuracy'] is not None else None
                pooled=1-a['answer_accuracy'] if a['answer_accuracy'] is not None else None
                key=f'$.models.{name}.{group}.pattern_group_readings[{index}].accuracy'
                document_rows.append(dict(reading=reading,model=name,population=group,case_error=case,pooled_error=pooled,receipt_path=key))
                lines.append(f'| {name} | {group} | {case} | {pooled} | receipts/acd_stage21_R12_recovery.json {key} |')
    lines+=['','The earlier reading table’s S columns cover all eight patterns. The tables in this definition note cover the seven zero-mean patterns only. “pooled” in the population column combines forcing levels; the pooled-error column averages individual confident answers, while case-averaged error weights contributing instances equally.','']
    note='\n'.join(lines)
    p=ROOT/'ACD_STAGE21_READING.md';old=p.read_text();heading=lines[0]
    if heading in old:old=old[:old.index(heading)]
    p.write_text(old.rstrip()+'\n\n'+note)
    # Execute only the plotting portion of the committed renderer, on committed metrics.
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    stored=json.loads((ROOT/'receipts/acd_stage16.json').read_text())
    runs=stored['runs'];posterior=json.loads((ROOT/'receipts/acd_stage9.json').read_text())['C']['posterior']
    source=(ROOT/'acd_stage16_render.py').read_text()
    body=source[source.index(' fig,axes=plt.subplots'):source.index("if __name__=='__main__'")]
    body='\n'.join(line[1:] for line in body.splitlines())
    exec(body,dict(ROOT=ROOT,runs=runs,posterior=posterior,np=np,plt=plt,json=json))
    p=ROOT/'ACD_STAGE16_READING.md';body=p.read_text();body=body.split('## Individual runs')[0].rstrip()
    p.write_text(body+'\n\nPer-run readings, bounds, calibration and action histograms: receipts/acd_stage16.json.\n')
    (ROOT/'receipts/acd_posthoc_definition_notes.json').write_text(json.dumps(dict(post_hoc=True,retained=retained,contributing={k:d['confirmatory'][k]['contributing_instances'] for k in ['R1','R2']},rows=document_rows,source_receipt='receipts/acd_stage21_R12_recovery.json'),indent=2)+'\n')
    print('Documentation and figure updated from committed receipts; no scoring.')

if __name__=='__main__':main()
