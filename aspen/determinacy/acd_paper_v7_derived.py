"""Paper v7 derivations from retained receipts; post hoc, no frozen-route license."""
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def build():
    stage9=json.loads((ROOT/'receipts/acd_stage9.json').read_text())
    tangent=json.loads((ROOT/'receipts/acd_stage11_clim_tangent.json').read_text())
    rows={}
    def add(key,value,source,path,derivation):
        rows[key]=dict(value=value,source=source,source_path=path,derivation=derivation)
    for model in ['posterior','CNN-20k','CNN-F']:
        readings=stage9['C'][model]['confidence_readings']
        i=next(i for i,r in enumerate(readings) if r['lead']==2.0)
        a=readings[i]['all_confident_accuracy'];error=1-a['answer_accuracy']
        path=f'$.C.{model}.confidence_readings[{i}].all_confident_accuracy'
        wrong=round(error*a['answers'])
        assert math.isclose(error*a['answers'],wrong,abs_tol=1e-9)
        add(model+'_POOLED_S_ERROR_2LT',error,'receipts/acd_stage9.json',path+'.answer_accuracy','one minus pooled answer accuracy; all confident intervention-sign answers, main amplitude')
        add(model+'_S_WRONG_2LT',wrong,'receipts/acd_stage9.json',path,'rounded integer reconstructed from (1 - answer_accuracy) * answers; integer identity checked within float round-off')
        add(model+'_S_ANSWERS_2LT',a['answers'],'receipts/acd_stage9.json',path+'.answers','retained pooled all-confident intervention-sign answer count')
    indexed=[(i,r) for i,r in enumerate(tangent['rows']) if 1<=r['pattern']<=7]
    for key,field,operation in [('ZERO_MEAN_MAX_ABS_MEAN_OVER_SD','mean_over_sd','maxabs'),('ZERO_MEAN_MIN_NEGATIVE_SHARE','negative_share','min'),('ZERO_MEAN_MAX_NEGATIVE_SHARE','negative_share','max')]:
        fn=(lambda r:abs(r[field])) if operation=='maxabs' else (lambda r:r[field])
        i,r=(min if operation=='min' else max)(indexed,key=lambda p:fn(p[1]))
        add(key,fn(r),'receipts/acd_stage11_clim_tangent.json',f'$.rows[{i}].{field}',operation+' over patterns one through seven and all retained leads; extremizing source row recorded')
    return dict(scope='Post hoc receipt-only v7 derivations; no frozen-route license',source_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['receipts/acd_stage9.json','receipts/acd_stage11_clim_tangent.json']},quantities=rows)
if __name__=='__main__':
    (ROOT/'receipts/acd_paper_v7_derived.json').write_text(json.dumps(build(),indent=2,allow_nan=False)+'\n')
