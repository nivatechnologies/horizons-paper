"""Durable conservative per-run charge across interruption and reboot."""
import json
from pathlib import Path
import time


class Charge:
    def __init__(self, out):
        self.path = Path(out)/'charge.json'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        old = json.loads(self.path.read_text()) if self.path.exists() else None
        self.prior = (old['charged_gpu_seconds']+max(0., time.time()-old['wall_timestamp'])) if old else 0.
        self.started = time.monotonic()
        self.snapshot()

    def snapshot(self):
        charged = self.prior+time.monotonic()-self.started
        pending = self.path.with_suffix('.tmp.json')
        pending.write_text(json.dumps(dict(charged_gpu_seconds=charged, wall_timestamp=time.time(),
                           convention='unfinished interruption interval charged conservatively against cap'))+'\n')
        pending.replace(self.path)
        return charged
