"""Drive the authorized Spark campaign, freeze numeric geometry, and recover all review artifacts."""
import datetime
import hashlib
import json
import shlex
import subprocess
import sys
import time

from common import ROOT,REPO,RUNS,RESULTS,write_json

HOST="192.168.88.4"
REMOTE="/home/todd/work/aspen-evidence-20261004"
PYTHON="/home/todd/geps_work/venv/bin/python"


def local(argv,**kwargs):
    return subprocess.run(argv,cwd=REPO,check=True,text=True,**kwargs)


def ssh(command,check=True):
    return subprocess.run(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=10",HOST,command],
                          capture_output=True,text=True,check=check)


def state(phase,**extra):
    write_json(RUNS/"campaign_status.json",dict(phase=phase,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**extra))


def sync_results():
    RESULTS.mkdir(parents=True,exist_ok=True)
    local(["rsync","-a",HOST+":"+REMOTE+"/aspen/evidence/results/",str(RESULTS)+"/"])


def wait_prepare():
    print("Waiting for complete sensitivity and every-point chaos gates",flush=True)
    while True:
        result=ssh(f"test -f {REMOTE}/aspen/evidence/results/points.json && test -f {REMOTE}/aspen/evidence/results/feasibility.json",check=False)
        if result.returncode==0:return
        alive=ssh("kill -0 1822817",check=False)
        if alive.returncode:
            raise RuntimeError("Preparation exited without a complete point/feasibility product")
        tail=ssh(f"tail -n 2 {REMOTE}/aspen/evidence/runs/logs/prepare.log").stdout.strip()
        print(tail,flush=True)
        time.sleep(30)


def deploy():
    # Prepare has exited; updating the source tag now cannot relabel a running calibration.
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=REPO,text=True).strip()
    archive=RUNS/"source.tar"
    archive.parent.mkdir(parents=True,exist_ok=True)
    with archive.open("wb") as f:local(["git","archive","HEAD","aspen/evidence"],stdout=f)
    local(["scp",str(archive),HOST+":"+REMOTE+"/source.tar"])
    ssh(f"cd {REMOTE} && tar -xf source.tar && printf '%s\\n' {shlex.quote(head)} > SOURCE_COMMIT")
    # Actual branch on Spark advances via a bundle; raw caches and results remain untracked.
    bundle=RUNS/"source.bundle"
    local(["git","bundle","create",str(bundle),"paper/aspen-2026-10-evidence"])
    local(["scp",str(bundle),HOST+":"+REMOTE+"/source.bundle"])
    ssh(f"cd {REMOTE} && git fetch -q source.bundle paper/aspen-2026-10-evidence && git reset -q --hard FETCH_HEAD")
    archive.unlink();bundle.unlink()
    print("Spark source frozen at",head,flush=True)


def run_phase(phase):
    state(phase)
    done=f"{REMOTE}/aspen/evidence/runs/phase_status/{phase}.json"
    previous=ssh("cat "+done,check=False)
    if previous.returncode==0 and json.loads(previous.stdout)["returncode"]==0:
        print("Already complete",phase,flush=True);return
    command=(f"cd {REMOTE}; mkdir -p aspen/evidence/runs/logs; "
             f"nohup {PYTHON} -u aspen/evidence/run_phase.py {phase} "
             f"> aspen/evidence/runs/logs/{phase}.log 2>&1 < /dev/null & echo $!")
    pid=int(ssh(command).stdout.strip())
    print("Started",phase,"PID",pid,flush=True)
    while True:
        result=ssh("cat "+done,check=False)
        if result.returncode==0:
            status=json.loads(result.stdout)
            if status["returncode"]!=0:
                tail=ssh(f"tail -n 25 {REMOTE}/aspen/evidence/runs/logs/{phase}.log").stdout
                raise RuntimeError(f"{phase} failed: {status}\n{tail}")
            print("Completed",phase,"seconds",status["seconds"],flush=True)
            sync_results();return
        if ssh(f"kill -0 {pid}",check=False).returncode:
            raise RuntimeError(f"{phase} PID {pid} exited without completion record")
        tail=ssh(f"tail -n 2 {REMOTE}/aspen/evidence/runs/logs/{phase}.log").stdout.strip()
        if tail:print(phase,tail,flush=True)
        time.sleep(30)


def main():
    branch=subprocess.check_output(["git","branch","--show-current"],cwd=REPO,text=True).strip()
    if branch!="paper/aspen-2026-10-evidence":raise RuntimeError("wrong branch")
    state("preparation");wait_prepare();sync_results()
    local([sys.executable,str(ROOT/"freeze_addendum.py")])
    # The numeric addendum must be a commit before panel data/training.
    local(["git","add","aspen/evidence/AEA_FREEZE_CALIBRATION.md","aspen/evidence/results"])
    staged=subprocess.run(["git","diff","--cached","--quiet"],cwd=REPO)
    if staged.returncode:local(["git","commit","-m","Aspen evidence: freeze measured sensitivity geometry and every-point chaos gates"])
    deploy()
    for phase in ["reported","data","nulls","law","train_L","train_F","learned"]:run_phase(phase)
    # Recover raw per-state evidence and final training metadata, excluding bulky weights/data.
    for sub in ["eval","train","phase_status"]:
        dest=RUNS/sub;dest.mkdir(parents=True,exist_ok=True)
        argv=["rsync","-a"]
        if sub=="train":argv += ["--exclude=*.pt","--exclude=resume.tmp"]
        local(argv+[HOST+":"+REMOTE+"/aspen/evidence/runs/"+sub+"/",str(dest)+"/"])
    cache=RUNS/"cache";cache.mkdir(parents=True,exist_ok=True)
    local(["scp",HOST+":"+REMOTE+"/aspen/evidence/runs/cache/training_theta.npy",str(cache)+"/"])
    local([sys.executable,str(ROOT/"analyze.py")])
    local([sys.executable,str(ROOT/"make_numbers.py")])
    local([sys.executable,str(ROOT/"make_numbers.py"),"--check"])
    # Negative check: mutate a rendered table token, prove rejection, restore exact artifact.
    path=ROOT/"NUMBERS.md";original=path.read_text()
    path.write_text(original.replace("AEA-C-1","AEA-C-TAMPER",1))
    negative=subprocess.run([sys.executable,str(ROOT/"make_numbers.py"),"--check"],cwd=REPO,capture_output=True,text=True)
    path.write_text(original)
    if negative.returncode==0:raise RuntimeError("NUMBERS tamper check failed to reject")
    local([sys.executable,str(ROOT/"figures.py")])
    local([sys.executable,str(ROOT/"results_note.py")])
    state("complete",numbers_check="zero mismatches",negative_tamper_check="rejected")
    print("CAMPAIGN COMPLETE; generated RUN_RESULTS.md ready for vault append",flush=True)


if __name__=="__main__":
    try:main()
    except Exception as error:
        state("failed",error=str(error))
        raise
