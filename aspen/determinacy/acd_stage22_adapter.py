"""Stage22 execution adapter: panel path and assigned case count only.

The generated modules differ from the frozen sources only at case-count
literals. N is injected before execution, leaving statistic/rollout code intact.
"""
import argparse
import ast
import difflib
import hashlib
import importlib.abc
import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = Path(os.environ.get('ACD_STAGE22_BASE', '/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy'))
OVERLAY = HERE/'stage22_parameterized'
N = None
MODULES = ['acd_stage21_contract', 'acd_stage21_inference', 'acd_stage21_score',
           'acd_stage19_part3b_score', 'acd_stage21_part1', 'acd_stage19_learned',
           'acd_stage9_cnn', 'acd_stage18_inference']

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def generate():
    OVERLAY.mkdir(exist_ok=True)
    records = []
    patches = []
    for name in MODULES:
        source = BASE/(name+'.py')
        old = source.read_text()
        lines = old.splitlines(keepends=True)
        replacements = []
        for node in ast.walk(ast.parse(old)):
            if isinstance(node, ast.Constant) and type(node.value) is int and node.value == 200:
                replacements.append((node.lineno, node.col_offset, node.end_col_offset, 'N'))
        if name == 'acd_stage21_contract':
            for node in ast.walk(ast.parse(old)):
                if isinstance(node, ast.Constant) and node.value == 100 and 'np.repeat([7.,9.],100)' in lines[node.lineno-1]:
                    replacements.append((node.lineno, node.col_offset, node.end_col_offset, 'N//2'))
        for line, start, end, value in sorted(replacements, reverse=True):
            lines[line-1] = lines[line-1][:start] + value + lines[line-1][end:]
        new = ''.join(lines)
        target = OVERLAY/source.name
        target.write_text(new)
        patches.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                       fromfile='FreezeE/'+source.name, tofile='Stage22/'+source.name))
        records.append(dict(path=str(target.relative_to(HERE)), baseline_path=str(source),
                            baseline_sha256=digest(source), sha256=digest(target),
                            changed_lines=sorted(set(x[0] for x in replacements)),
                            remaining_literal_200=[dict(line=i, text=l.rstrip()) for i,l in enumerate(new.splitlines(),1) if '200' in l]))
    (HERE/'ACD_STAGE22_PARAMETERIZATION.diff').write_text(''.join(patches))
    (HERE/'receipts').mkdir(exist_ok=True)
    record=dict(adapter_sha256=digest(__file__), modules=records, criteria='unchanged',
                change_scope='Assigned case count; balanced half-count derives as N//2. No statistic or rollout change.')
    (HERE/'receipts/acd_stage22_parameterization.json').write_text(json.dumps(record,indent=2)+'\n')
    return record


class ParameterizedLoader(importlib.abc.Loader):
    def __init__(self, path): self.path = path
    def create_module(self, spec): return None
    def exec_module(self, module):
        assert type(N) is int and N > 0 and N % 2 == 0
        module.__dict__['N'] = N
        exec(compile(self.path.read_text(), str(self.path), 'exec'), module.__dict__)


class ParameterizedFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in MODULES:
            file = OVERLAY/(fullname+'.py')
            spec = importlib.util.spec_from_file_location(fullname,file,loader=ParameterizedLoader(file))
            return spec


def install(count):
    global N
    N = count
    assert type(N) is int and N > 0 and N % 2 == 0
    sys.path.insert(0,str(BASE))
    sys.meta_path.insert(0,ParameterizedFinder())


def differences(expected, actual, path='$'):
    if type(expected) is not type(actual): return [dict(path=path, expected=expected, actual=actual)]
    if isinstance(expected,dict):
        if expected.keys()!=actual.keys(): return [dict(path=path,expected_keys=sorted(expected),actual_keys=sorted(actual))]
        return [d for k in expected for d in differences(expected[k],actual[k],path+'.'+k)]
    if isinstance(expected,list):
        if len(expected)!=len(actual):return [dict(path=path,expected_length=len(expected),actual_length=len(actual))]
        return [d for i,(a,b) in enumerate(zip(expected,actual)) for d in differences(a,b,f'{path}[{i}]')]
    return [] if expected == actual else [dict(path=path,expected=expected,actual=actual)]


def replay(count):
    """Read committed Stage21 costs, access outcomes only inside frozen scorer."""
    assert count == 200, 'This reproduction gate uses the complete Stage21 panel'
    record=generate()
    install(count)
    import numpy as np
    import acd_stage21_freeze_e as freeze
    # Hash checks use the original Freeze E files, including its amendment.
    import acd_stage21_contract as contract
    contract.digest=digest
    frozen=freeze.ready()
    import acd_stage21_score as scorer
    import acd_stage21_inference as inference
    import acd_stage19_part3b_score as seed_module
    assert len(contract.assignments()) == N
    root=HERE/'runs/stage22/reproduction'
    root.mkdir(parents=True,exist_ok=True)
    (root/'receipts').mkdir(exist_ok=True)
    (root/'ACD_STAGE21_FREEZE_E.md').write_bytes((BASE/'ACD_STAGE21_FREEZE_E.md').read_bytes())
    scorer.ROOT=root
    log=root/'outcome_access.jsonl'
    load=np.load
    def logged_load(path,*args,**kwargs):
        result=load(path,*args,**kwargs)
        if Path(path).resolve() == (contract.OUT/'scoring/actual.npz').resolve():
            caller=inspect.stack()[1]
            assert caller.function=='score_actual' and Path(caller.filename).name=='acd_stage21_score.py'
            assert result['actual'].shape[0] == N and result['factual'].shape[0] == N
            with log.open('a') as stream:
                stream.write(json.dumps(dict(path=str(path), sha256=digest(path), caller=caller.filename,
                                 function=caller.function, N=N, utc=time.time()))+'\n')
        return result
    np.load=logged_load
    names=['CNN-F-constantF']+[f'CNN-F-E0-fixed-seed{j}' for j in range(1,6)]+['CNN-noF']
    phases=[('R12_recovery','R12',[r for r in frozen['tasks'] if r['name'] in names]),
            ('R34','R34',[r for r in frozen['tasks'] if r.get('kind')=='E1']),
            ('descriptive','descriptive',[r for r in frozen['tasks'] if r['name'] not in names and r.get('kind')!='E1'])]
    results=[]
    try:
        for receipt_name, part, tasks in phases:
            print('Reproducing',receipt_name,'pipelines',len(tasks),flush=True)
            for row in tasks:
                folder=contract.OUT/'inference'/row['name']
                hashes=json.loads((folder/'hashes.json').read_text())
                assert set(hashes)=={f'{c:03d}.npz' for c in range(N)}, row['name']
                assert inference.complete(row['name']),row['name']
            scorer.ready=lambda:dict(frozen,tasks=tasks)
            # Also score_actual's ready is the same module global: freeze verified above.
            scorer.score()
            actual=json.loads((root/'receipts/acd_stage21.json').read_text())
            keys=['R1','R2'] if part=='R12' else ['R3','R4','R4_F7_descriptive','R4_F9_descriptive'] if part=='R34' else []
            actual['confirmatory']={k:v for k,v in actual['confirmatory'].items() if k in keys}
            actual['part']=part
            actual.setdefault('source_hashes',{})['execution_reorder']=digest(BASE/'receipts/acd_stage21_reorder.json')
            tasknames={r['name'] for r in tasks}
            actual['missing_models']=[n for n in actual['missing_models'] if n in tasknames]
            ids=actual['models']['posterior']['pooled']['case_indices']
            assert len(ids)+len(actual['excluded_cases']) == N
            assert set(ids)|set(actual['excluded_cases']) == set(range(N))
            for key in keys[:2]:
                row=actual['confirmatory'].get(key,{})
                if row.get('evaluable'):
                    assert len(row['defined_seeds_per_instance'])==N
                    assert len(row['case_mean_differences'])==N
                    assert all(len(p['case_differences'])==N for p in row['per_seed'])
            expected_path=Path(os.environ.get('ACD_STAGE22_EXPECTED', str(BASE/'receipts')))/f'acd_stage21_{receipt_name}.json'
            expected=json.loads(expected_path.read_text())
            diff=differences(expected,actual)
            (root/f'{receipt_name}.diff.json').write_text(json.dumps(diff,indent=2)+'\n')
            (root/f'acd_stage21_{receipt_name}.json').write_text(json.dumps(actual,indent=2,allow_nan=False)+'\n')
            assert not diff, f'{receipt_name}: {len(diff)} differing values; see {root}/{receipt_name}.diff.json'
            results.append(dict(receipt=str(expected_path),sha256=digest(expected_path),different_values=len(diff),N=N,exact=True))
            print('Exact reproduction:',receipt_name,flush=True)
    finally:
        np.load=load
    report=dict(N=N,namespaces=contract.NAMES,results=results,all_exact=True,
                outcome_access_log=str(log.relative_to(HERE)),code=record)
    (HERE/'receipts/acd_stage22_reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Gate PASS',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['generate','replay'])
    parser.add_argument('--N',type=int,default=200)
    args=parser.parse_args()
    generate() if args.mode=='generate' else replay(args.N)
