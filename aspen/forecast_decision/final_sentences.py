"""Combined WO §7.6/7.7 sentence contract from both checked gates.

Pending two-scale evidence is explicitly open; it is never silently treated
as not run. Root supplies final not-run status at the evidence cutoff.
"""
import argparse,copy,datetime,json,time
from pathlib import Path
from protocol import ROOT,write_json,digest
import math

def reject_nonfinite(value):
    if isinstance(value,dict):
        for v in value.values():reject_nonfinite(v)
    elif isinstance(value,list):
        for v in value:reject_nonfinite(v)
    elif isinstance(value,float) and not math.isfinite(value):raise ValueError('nonfinite sentence record')

def equivalent(actual,expected):
    if actual!=expected:raise ValueError('combined sentence record mismatch')


def combined(one,two=None,two_status='pending'):
    reject_nonfinite(one)
    if two is not None:reject_nonfinite(two)
    if two_status not in ['pending','ran','not_run']:raise ValueError('unknown two-scale scope status')
    if two_status=='not_run' and two is not None:raise ValueError('not_run conflicts with supplied two-scale gate')
    g=one['primary']['gate']
    if g['sufficiency'] and g['H1a']=='KILL':return dict(status='CLOSED',campaign_kill=True,final_licensed_sentences=[],sentences=[],mandatory_companions_closed=True,reason='WO §7.6 H1a KILL stops the campaign and requires findings harvest')
    repeats=all(n in one['arms'] for n in ['CNN-20k-s2','CNN-20k-s3'])
    provisional=g.get('licensed_sentences',[])
    if two_status=='pending':return dict(status='OPEN_STAGE2B_PENDING',final_licensed_sentences=[],provisional_one_scale_ids=provisional,mandatory_companions_closed=False)
    from metrics import license_ids
    from result_note import licensed_text
    if two_status=='ran' and two is None:raise ValueError('ran two-scale scope requires checked two-scale gate')
    tg=two['primary']['gate'] if two is not None else None
    one_ids=license_ids(g,'2',selected=one.get('selected'),twoscale_gate=tg,repeats_ran=repeats)
    two_ids=license_ids(tg,'2b',selected=two.get('selected')) if two_status=='ran' else []
    all_ids=list(dict.fromkeys(one_ids+two_ids))
    if 'S1' in all_ids or 'S2' in all_ids:
        assert any(i in all_ids for i in ['S10','S10b','S10c'])
        if repeats:assert 'S1s' in all_ids
        if two_status=='ran' and 'S8' not in two_ids:assert 'S9' in all_ids
    if 'S2' in all_ids and g['H1d']!='HOLDS':assert 'S7' in all_ids
    if 'S8+' in all_ids and tg['H1d']!='HOLDS':assert 'S7₂' in all_ids
    if 'S8' in all_ids and tg.get('H1e') is not None:assert 'S11' in all_ids
    a=copy.deepcopy(one);a['primary']['gate']['licensed_sentences']=[i for i in one_ids if i!='S9'];texts=licensed_text(a)
    if two_status=='ran':
        b=copy.deepcopy(two);b['primary']['gate']['licensed_sentences']=two_ids;texts+=licensed_text(b)
    return dict(status='CLOSED',final_licensed_sentences=all_ids,sentences=texts,two_scale_status=two_status,mandatory_companions_closed=True)


def check_combined(one,two,status,reading):
    reject_nonfinite(reading);equivalent(reading,combined(one,two,status))
    return dict(status='PASS',mandatory_one_scale_and_two_scale_companions_checked=True,final_sentence_set_closed=reading['status']=='CLOSED')


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--watch',action='store_true');a=p.parse_args()
    root=a.root
    while True:
        one_path=root/'runs/2_metrics.json';one_check=root/'runs/2_metrics_checker.json';two_path=root/'runs/2b_metrics.json';two_check=root/'runs/2b_metrics_checker.json';scope_path=root/'runs/final_scope_status.json'
        authorization=root/'runs/final_scope_authorization.json'
        complete_two=two_path.exists() and two_check.exists() and json.loads(two_check.read_text()).get('status')=='PASS'
        if authorization.exists() and not scope_path.exists() and not complete_two:
            auth=json.loads(authorization.read_text());reject_nonfinite(auth)
            if auth.get('authorize_not_run_if_incomplete') is True:
                deadline=datetime.datetime.fromisoformat(auth['two_scale_deadline_utc'].replace('Z','+00:00'))
                if deadline.tzinfo is None:raise ValueError('cutoff authorization deadline must include timezone')
                current=datetime.datetime.now(datetime.timezone.utc)
                if current>deadline:
                    write_json(scope_path,dict(two_scale='not_run',final=True,at=current.isoformat(),deadline_utc=deadline.isoformat(),reason='No checked complete Stage2b gate at the explicitly authorized evidence cutoff',authority=auth['authority'],authorization_sha256=digest(authorization),sampler_go_implied=False))
        if not one_path.exists() or not one_check.exists():
            write_json(root/'runs/final_sentences_status.json',dict(status='WAITING_STAGE2',at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
        else:
            one=json.loads(one_path.read_text());assert json.loads(one_check.read_text())['status']=='PASS';two=None;scope='pending'
            if scope_path.exists():
                stated=json.loads(scope_path.read_text());reject_nonfinite(stated)
                if stated.get('two_scale')=='not_run' and stated.get('final') is True:
                    if stated.get('authorization_sha256') is not None:
                        if not authorization.exists() or digest(authorization)!=stated['authorization_sha256']:raise ValueError('not-run authorization receipt changed')
                        recorded=datetime.datetime.fromisoformat(stated['at'].replace('Z','+00:00'))
                        cutoff=datetime.datetime.fromisoformat(stated['deadline_utc'].replace('Z','+00:00'))
                        if recorded.tzinfo is None or cutoff.tzinfo is None or recorded<=cutoff:raise ValueError('not-run receipt precedes authorized cutoff')
                    scope='not_run'
            if scope=='pending' and two_path.exists() and two_check.exists() and json.loads(two_check.read_text())['status']=='PASS':two=json.loads(two_path.read_text());scope='ran'
            reading=combined(one,two,scope);checker=check_combined(one,two,scope,reading)
            # Missing mandatory S9 must be rejected when a ran panel lacks S8.
            if scope=='ran' and 'S9' in reading['final_licensed_sentences']:
                tamper=copy.deepcopy(reading);tamper['final_licensed_sentences'].remove('S9')
                try:check_combined(one,two,scope,tamper)
                except (ValueError,AssertionError):checker['missing_S9_tamper_rejected']=True
                else:raise AssertionError('missing mandatory S9 accepted')
            sources={str(one_path.relative_to(root)):digest(one_path),str(one_check.relative_to(root)):digest(one_check)}
            if scope=='ran':sources.update({str(two_path.relative_to(root)):digest(two_path),str(two_check.relative_to(root)):digest(two_check)})
            if scope=='not_run':sources[str(scope_path.relative_to(root))]=digest(scope_path)
            output=dict(reading=reading,checker=checker,source_hashes=sources)
            write_json(root/'runs/final_sentences.json',output)
            write_json(root/'runs/final_sentences_status.json',dict(status=reading['status'],at=datetime.datetime.now(datetime.timezone.utc).isoformat(),factual_audit='OPEN; independent prose audit remains required'))
            if reading['status']=='CLOSED':
                (root/'NUMBERS_FINAL_SENTENCES.md').write_text('# NUMBERS final sentence contract\n\n```json\n'+json.dumps(output,indent=2,allow_nan=False)+'\n```\n')
                (root/'AFD_FINAL_LICENSED_SENTENCES.md').write_text('\n'.join(x['id']+': '+x['text'] for x in reading['sentences'])+'\n')
                return
        if not a.watch:return
        time.sleep(30)
if __name__=='__main__':main()
