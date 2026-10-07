"""Temporarily stop an authorized Baccus vLLM unit and restore it after Stage18 work."""
import argparse
import contextlib
import datetime
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from acd_stage18_inference import OUT, guarded as freeze_ready
from acd_stage19_part2_gate import gpu_inventory

UNITS = {0: 'qwen3.8-vllm-mtp@card-a.service',
         1: 'qwen3.8-vllm-mtp@card-b.service',
         2: 'qwen3.8-vllm-mtp@card-c.service'}
AUTHORIZATION = ('Todd authorizes stopping vLLM on Baccus GPUs and bringing '
                 'the services back up after the authorized GPU work finishes.')


def service(*args):
    return subprocess.run(['systemctl', '--user', *args], check=True,
                          text=True, capture_output=True)


def log(event, **fields):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'gpu_service_access.jsonl').open('a') as f:
        f.write(json.dumps(dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                               event=event, **fields)) + '\n')


def active(unit):
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', unit]).returncode == 0


@contextlib.contextmanager
def lease(index):
    """Stop only this GPU's known service; record any other holders and refuse them."""
    freeze_ready()
    if os.uname().nodename != 'baccus':
        raise RuntimeError('This authorization is for Baccus only')
    unit = UNITS[index]
    inventory = gpu_inventory()
    card = next(c for c in inventory if c['index'] == index)
    # A non-serving process may belong to another stage and must not be disturbed.
    if any('VLLM' not in p['process'].upper() for p in card['processes']):
        raise RuntimeError('GPU has a non-vLLM compute process')
    was_active = active(unit)
    record = dict(unit=unit, gpu=card, was_active=was_active,
                  authorization=AUTHORIZATION)
    recovery = OUT / f'gpu_service_recovery_{index}.json'
    recovery.write_text(json.dumps(record, indent=2) + '\n')
    log('before_gpu_service_stop', **record)
    try:
        if was_active:
            service('stop', unit)
        for _ in range(60):
            current = next(c for c in gpu_inventory() if c['index'] == index)
            if current['available']:
                break
            time.sleep(1)
        else:
            raise RuntimeError('GPU did not become free; no process was killed manually')
        log('gpu_available', gpu=current)
        yield current
    finally:
        if was_active:
            service('start', unit)
            if not active(unit):
                raise RuntimeError('vLLM unit restoration failed; recovery record retained')
            log('gpu_service_restarted', unit=unit)
        recovery.unlink(missing_ok=True)


def interrupted(signum, frame):
    raise KeyboardInterrupt(f'Signal {signum}; restore the leased service')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gpu', type=int, choices=tuple(UNITS), default=0)
    parser.add_argument('--restore', action='store_true')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.restore:
        recovery = OUT / f'gpu_service_recovery_{args.gpu}.json'
        record = json.loads(recovery.read_text())
        if record['was_active']:
            service('start', record['unit'])
            log('gpu_service_restarted_after_interruption', unit=record['unit'])
        recovery.unlink()
        return
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('An inference command is required; no service will be stopped')
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    with lease(args.gpu) as card:
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=card['uuid'])
        child = subprocess.Popen(command, env=env)
        try:
            result = child.wait()
        except BaseException:
            child.terminate()
            try:
                child.wait(timeout=60)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
            raise
        if result:
            raise RuntimeError(f'Inference exited with status {result}')


if __name__ == '__main__':
    main()
