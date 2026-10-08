"""Resumable Stage20 transfer/scoring/publication controller in its own worktree."""
import hashlib,json,os,shlex,subprocess,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
BASE=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy')
CACHE=BASE/'runs/stage20'
PYTHON='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python'
SCIENCE=Path('/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy')
S18=Path('/home/todd/work/aspen-determinacy-stage18-20261007/aspen/determinacy')
REMOTE=Path('/home/todd/work/aspen-stage20-20261008')
BRANCH='paper/aspen-2026-10-determinacy'

def call(cmd,**kwargs):return subprocess.run(list(map(str,cmd)),check=True,**kwargs)
def remote(host,cmd):return subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10',host,cmd],text=True,capture_output=True)
def transfer(cmd):
    while True:
        p=subprocess.run(list(map(str,cmd)))
        if p.returncode==0:return
        print('Transfer retry after sixty seconds',flush=True);time.sleep(60)
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
def add_registry(part):
    p=ROOT/'acd_numbers.py';s=p.read_text();line=f"    stage13_receipts.append(('receipts/acd_stage20_{part}.json', 'ACD_POSTHOC_20{part}'))\n"
    if line not in s:s=s.replace('    for filename,prefix in stage13_receipts:\n',line+'    for filename,prefix in stage13_receipts:\n')
    marker="omit=('source_hashes','code_hashes','reproduction_checks','invalid_cases') if filename.endswith('acd_stage20_A.json') else "
    addition="omit=('source_hashes','code_hashes','executions','records','case_records','output_hashes','invalid_cases') if filename.endswith(('acd_stage20_B.json','acd_stage20_C.json')) else ('source_hashes','code_hashes','reproduction_checks','invalid_cases') if filename.endswith('acd_stage20_A.json') else "
    s=s.replace(marker,addition);p.write_text(s)
def status(step,commit,detail):
    p=ROOT/'ACD_PIPELINE_STATUS.md';stamp=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    p.write_text(p.read_text()+f'\nStage20 | {step} | {commit} | {stamp} | {detail}\n')
def publish(part):
    before=json.loads((ROOT/'numbers_acd.json').read_text())['numbers'];add_registry(part)
    call([PYTHON,ROOT/'acd_numbers.py']);after=json.loads((ROOT/'numbers_acd.json').read_text())['numbers']
    assert all(k in after and after[k]['value']==v['value'] for k,v in before.items())
    call([PYTHON,ROOT/'check_acd.py'])
    if (ROOT/'numbers_acd.json').stat().st_size>100*1024**2:raise RuntimeError('Registry exceeds remote file cap; no prior key removed')
    files=[f'receipts/acd_stage20_{part}.json','ACD_STAGE20_READING.md','acd_numbers.py','numbers_acd.json','NUMBERS_ACD.md']
    if part=='B':files+=['figures/F22_readability_paper.pdf','figures/F22_readability_paper.png']
    git('add',*[str(ROOT/f) for f in files]);git('commit','-m',f'Report Stage20 {part} original-panel context retention')
    while True:
        git('fetch','origin',BRANCH)
        p=subprocess.run(['git','-C',str(REPO),'rebase','FETCH_HEAD'])
        if p.returncode:raise RuntimeError('Rebase needs conflict resolution; Stage20 result retained')
        call([PYTHON,ROOT/'check_acd.py'])
        pushed=subprocess.run(['git','-C',str(REPO),'push','origin','HEAD:'+BRANCH])
        if pushed.returncode==0:break
        time.sleep(60)
    commit=git('rev-parse','HEAD');status(part,commit,'Scored and pushed; other Stage20 part continues independently.')
    git('add',str(ROOT/'ACD_PIPELINE_STATUS.md'));git('commit','-m',f'Record Stage20 {part} publication');git('push','origin','HEAD:'+BRANCH)
    marker=dict(part=part,commit=commit,registry_before=len(before),registry_after=len(after),check='PASS',prior_values_unchanged=True)
    (CACHE/(part+'_published.json')).write_text(json.dumps(marker,indent=2)+'\n');print(json.dumps(marker),flush=True)

def B():
    target=CACHE/'B';target.mkdir(exist_ok=True)
    transfer(['rsync','-a','192.168.88.4:'+str(REMOTE/'B')+'/',str(target)+'/'])
    call([PYTHON,ROOT/'acd_stage20_readability.py','--outputs',target,'--inputs',BASE/'runs/stage18/confirmation_inputs','--receipt',ROOT/'receipts/acd_stage20_B.json','--reading',ROOT/'ACD_STAGE20_READING.md','--figures',ROOT/'figures'])
    publish('B')

def C():
    target=CACHE/'C';target.mkdir(exist_ok=True)
    transfer(['rsync','-a','192.168.88.12:'+str(REMOTE/'C')+'/',str(target)+'/'])
    call(['ssh','sulaco','mkdir','-p',str(REMOTE/'C')])
    transfer(['rsync','-a',str(target)+'/', 'sulaco:'+str(REMOTE/'C')+'/'])
    transfer(['scp',str(ROOT/'acd_stage20_C.py'),'sulaco:'+str(REMOTE/'C/score.py')])
    transfer(['scp',str(ROOT/'ACD_STAGE20_READING.md'),'sulaco:'+str(REMOTE/'C/READING.md')])
    args=['/home/todd/work/aspen-determinacy-20261005/.venv/bin/python',str(REMOTE/'C/score.py'),
        '--science-root',str(SCIENCE),'--stage18',str(S18),'--outputs',str(REMOTE/'C'),'--inputs',str(S18/'runs/stage18/confirmation_inputs'),
        '--receipt',str(REMOTE/'C/acd_stage20_C.json'),'--reading',str(REMOTE/'C/READING.md')]
    call(['ssh','sulaco',shlex.join(args)])
    transfer(['scp','sulaco:'+str(REMOTE/'C/acd_stage20_C.json'),str(ROOT/'receipts/acd_stage20_C.json')])
    transfer(['scp','sulaco:'+str(REMOTE/'C/READING.md'),str(target/'READING.md')])
    p=ROOT/'ACD_STAGE20_READING.md';p.write_text(p.read_text()+'\n## C'+(target/'READING.md').read_text().split('\n## C',1)[1])
    publish('C')

def main():
    CACHE.mkdir(parents=True,exist_ok=True)
    while not all((CACHE/(p+'_published.json')).exists() for p in ['B','C']):
        if not (CACHE/'C_started.json').exists():
            ping=remote('192.168.88.12','hostname')
            if ping.returncode==0:
                try:
                    call([PYTHON,BASE/'acd_stage20_prepare.py','--part','C'])
                    launch=remote('192.168.88.12',f'nohup python3 -u {REMOTE}/code/acd_stage20_queue.py C > {REMOTE}/C/queue.log 2>&1 < /dev/null & echo $!')
                    if launch.returncode:raise RuntimeError(launch.stderr)
                    (CACHE/'C_started.json').write_text(json.dumps(dict(pid=launch.stdout.strip(),host='192.168.88.12'))+'\n')
                except Exception:traceback.print_exc()
            else:print('Spark2 unavailable; retry after sixty seconds',flush=True)
        for part,host in [('B','192.168.88.4'),('C','192.168.88.12')]:
            if (CACHE/(part+'_published.json')).exists() or (CACHE/(part+'_failed.json')).exists():continue
            probe=remote(host,f'test -f {REMOTE}/{part}/queue_complete.json')
            if probe.returncode==0:
                try:B() if part=='B' else C()
                except Exception:
                    failure=traceback.format_exc();(CACHE/(part+'_failed.json')).write_text(json.dumps(dict(part=part,failure=failure))+'\n');print(failure,flush=True)
                    status(part+' failure','pending',failure.splitlines()[-1]);git('add',str(ROOT/'ACD_PIPELINE_STATUS.md'));git('commit','-m',f'Record Stage20 {part} completion failure');git('push','origin','HEAD:'+BRANCH)
        time.sleep(60)
if __name__=='__main__':main()
