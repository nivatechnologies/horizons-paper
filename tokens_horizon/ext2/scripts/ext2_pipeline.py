"""EXT2 per-configuration runner: wait for the frozen training run to finish (info.json present and no `running`
marker; ext2_train.py refuses to reuse a directory that already holds a run; timeout 6 h); if it diverged, run the
single frozen fallback (lr 1e-4, tag _lr1e-4); then run the M1-M4 measurements on the selected checkpoint.

Usage: python ext2/scripts/ext2_pipeline.py <config> <device>
"""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from th import config  # noqa: E402

HERE = Path(__file__).resolve().parent
TRAIN = config.RUNS / "ext2" / "train"


def main(name, device):
    info = TRAIN / name / "info.json"
    t0 = time.time()
    while not info.exists() or (TRAIN / name / "running").exists():
        if time.time() - t0 > 6 * 3600:
            raise TimeoutError(name)
        time.sleep(30)
    tag = ""
    if json.loads(info.read_text())["diverged"]:
        tag = "_lr1e-4"
        subprocess.run([sys.executable, str(HERE / "ext2_train.py"), name, device, "30000", "1e-4", tag], check=True)
        if json.loads((TRAIN / f"{name}{tag}" / "info.json").read_text())["diverged"]:
            print(name, "fallback also diverged; not measured", flush=True)
            return
    subprocess.run([sys.executable, str(HERE / "ext2_measure.py"), name, device, tag], check=True)
    print(name, "pipeline done", round(time.time() - t0), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
