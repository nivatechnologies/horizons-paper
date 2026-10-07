"""Stage 19 Part 2 access gates; no hidden history or outcomes are read here."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = ROOT / 'runs/stage19'
BRANCH = 'paper/aspen-2026-10-determinacy'


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO, text=True).strip()


def part1_ready(verify_remote=True):
    """Require the complete, pushed receipt and validate its forecast hashes."""
    marker = OUT / 'final_commit.txt'
    if not marker.exists():
        raise RuntimeError('Part 1 final hash commit has not been pushed')
    commit = marker.read_text().strip()
    if verify_remote:
        subprocess.run(['git', 'fetch', 'origin', BRANCH], cwd=REPO, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(['git', 'merge-base', '--is-ancestor', commit, 'FETCH_HEAD'],
                       cwd=REPO, check=True)
    else:
        # Offline preparation may use the Part 1 finalizer's push record.
        # This never authorizes inference or scoring: freeze_ready remains strict.
        subprocess.run(['git', 'merge-base', '--is-ancestor', commit, 'HEAD'],
                       cwd=REPO, check=True)
    rel = 'aspen/determinacy/receipts/acd_stage19_part1.json'
    committed = git('show', f'{commit}:{rel}')
    receipt = json.loads(committed)
    if receipt['status'] != 'blind_sampling_complete' or len(receipt['cases']) != 200:
        raise RuntimeError('Part 1 is incomplete')
    if receipt.get('realized_outcome_accesses') or receipt.get('emulator_runs'):
        raise RuntimeError('Part 1 access contract violated')
    local = json.loads((ROOT / 'receipts/acd_stage19_part1.json').read_text())
    if local != receipt:
        raise RuntimeError('Part 1 receipt differs from its pushed commit')
    for case in receipt['cases']:
        for arm in case['arms'].values():
            for path, expected in arm['files'].items():
                if digest(ROOT / path) != expected:
                    raise RuntimeError('Part 1 hash mismatch: ' + path)
    return commit, receipt


def freeze_ready():
    """Scoring and inference both require this separately recorded push."""
    part1_ready()
    marker = OUT / 'freeze_b_pushed.json'
    if not marker.exists():
        raise RuntimeError('Freeze B has not been pushed')
    record = json.loads(marker.read_text())
    if digest(ROOT / 'ACD_STAGE19_FREEZE_B.md') != record['sha256']:
        raise RuntimeError('Freeze B hash changed')
    subprocess.run(['git', 'merge-base', '--is-ancestor', record['commit'], 'FETCH_HEAD'],
                   cwd=REPO, check=True)
    return record


def gpu_inventory():
    """A GPU with any compute process is unavailable; never stop a process."""
    cards = subprocess.check_output(
        ['nvidia-smi', '--query-gpu=index,uuid,name', '--format=csv,noheader'],
        text=True).splitlines()
    processes = subprocess.check_output(
        ['nvidia-smi', '--query-compute-apps=gpu_uuid,pid,process_name',
         '--format=csv,noheader'], text=True).splitlines()
    holders = {}
    for line in processes:
        uuid, pid, name = (x.strip() for x in line.split(',', 2))
        holders.setdefault(uuid, []).append(dict(pid=int(pid), process=name))
    inventory = []
    for line in cards:
        index, uuid, name = (x.strip() for x in line.split(',', 2))
        inventory.append(dict(index=int(index), uuid=uuid, name=name,
                              processes=holders.get(uuid, []),
                              available='170HX' in name and not holders.get(uuid)))
    return inventory


if __name__ == '__main__':
    try:
        commit, receipt = part1_ready()
        print(json.dumps(dict(part1_ready=True, commit=commit,
                              cases=len(receipt['cases'])), indent=2))
    except RuntimeError as error:
        print(json.dumps(dict(part1_ready=False, reason=str(error))))
    print(json.dumps(dict(gpus=gpu_inventory()), indent=2))
