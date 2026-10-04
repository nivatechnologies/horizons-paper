"""AAH extension of existing NUMBERS table integrity and exact source replay."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
from common import ROOT
sys.path.insert(0,str(ROOT.parents[1]/'tokens_horizon/scripts'))
sys.path.insert(0,str(ROOT.parents[1]/'tokens_horizon'))
_spec=importlib.util.spec_from_file_location('_aah_base_numbers',ROOT.parents[1]/'tokens_horizon/scripts/make_numbers.py')
MN=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MN)

def render():
    MN.PKG=ROOT;MN.SECTIONS.clear()
    out=['# NUMBERS: act beyond the horizon','',
         'AAH sections use the existing NUMBERS checker. Every measurement is replayed from its JSON source; missing inputs are pending, never zero. Labels: estimate (finite panels/bootstrap/Monte Carlo), reference (specified chance baseline). Bootstrap confidence is nominal.','']
    results=ROOT/'results'
    for system,prefix in [('l96','AAHL'),('kolmo','AAHK')]:
        path=results/f'{system}_calibration.json'
        if path.exists():
            data=json.loads(path.read_text())
            rows=[dict(system=system,delta=r['delta'],eligible=r['eligible'],n=r['total'],fraction=r['fraction'],label='estimate') for r in data['rows']]
            MN.table(out,prefix+'CAL','Amplitude calibration',path,['system','delta','eligible','n','fraction'],rows,data['git_sha'],note='Calibration cases only. First passing amplitude selected; later amplitudes not tested.')
        path=results/f'{system}_solver_statistics.json'
        if path.exists():
            data=json.loads(path.read_text());rows=[]
            for h in data['horizons']:
                for arm,a in h['arms'].items():
                    if not a:continue
                    rows.append(dict(T=h['T'],arm=arm,eligible=h['eligible'],total=h['total'],sufficient=h['sufficient'],
                                     top1=a['accuracy'][3],ACC=a['ACC'],M95=a['M95'] if a['M95'] is not None else '>256',
                                     regret=a['normalized_regret'],realized_regret=a['realized_regret'],
                                     response_correlation=a['response_correlation'],response_relative_error=a['response_relative_error'],label='estimate'))
            MN.table(out,prefix+'ARMS','Per-horizon arm readings',path,
                     ['T','arm','eligible','total','sufficient','top1','ACC','M95','regret','realized_regret','response_correlation','response_relative_error'],
                     rows,data['git_sha'])
            rows=[dict(T=h['T'],ratio=h['member_criterion']['ratio_lower_bound'],member_pass=h['member_criterion']['pass_condition'],
                       myopic=h['myopic_accuracy'],random=h['random_accuracy_expected'],committed=h['commitment']['committed'],
                       uncommitted=h['commitment']['uncommitted'],mean_members=h['commitment']['mean_members'],
                       commitment_errors=h['commitment']['error_rate'],wall_seconds=h['commitment'].get('mean_wall_seconds'),label='estimate') for h in data['horizons']]
            MN.table(out,prefix+'CONTROL','Members, commitment and null readings',path,
                     ['T','ratio','member_pass','myopic','random','committed','uncommitted','mean_members','commitment_errors','wall_seconds'],rows,data['git_sha'],
                     note='M95 restricted to budget grid. Censored unpaired conservative numerator256; paired censoring fails. Wall seconds measure nested cohorts sharing all scoring horizons plus interval analysis, on a shared host.')
    for line in out:
        if line.startswith('Source ') and ('SHA ``' in line):raise MN.NumbersError('empty source SHA')
        if line.startswith('| AAH') and line.endswith('|  |'):raise MN.NumbersError('empty AAH row label')
    return '\n'.join(out).rstrip()+'\n'

def check(path):
    expected=render();actual=Path(path).read_text()
    if actual!=expected:raise MN.NumbersError('AAH numeric/source replay mismatch')
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['build','check']);p.add_argument('--path',type=Path,default=ROOT/'NUMBERS.md')
    a=p.parse_args()
    if a.command=='build':a.path.write_text(render())
    check(a.path);print('AAH NUMBERS: zero mismatches')
