"""Collect the Kolmogorov reproduction (post-freeze follow-up; released GEPS train.py at lr 1e-2, Baccus GPU 2).

Reads the offline wandb log (LevelDB-style log of wandb Record protobufs) for the released evaluation records
(train_loss, loss_test_in = RelativeL2 over the first 20 test frames, loss_test_out = the next 20; every 100 epochs), and
computes persistence (the first frame repeated) on the same 256 test trajectories with the same RelativeL2. Writes
stage2/geps/results/geps_repro_curve.json. Run on Baccus with the reproduction's dependencies on PYTHONPATH:

  PYTHONPATH=~/geps_baccus/repro_deps python stage2/geps/geps_repro_collect.py
"""
import glob
import json
import shelve
import shutil
import struct
import tempfile
from pathlib import Path

import torch
from wandb.proto import wandb_internal_pb2 as pb

REPRO = Path.home() / "geps_baccus" / "repro"
OUT = Path(__file__).resolve().parent / "results" / "geps_repro_curve.json"
PAPER_IN_D = "2.94 +/- 0.04 x 1e-1 (Table 2, in-distribution relative L2)"


def wandb_evals(f):
    b = open(f, "rb").read()
    pos, block, buf, out = 7, 32768, b"", []
    while pos + 7 <= len(b):
        left = block - (pos % block)
        if left < 7:
            pos += left
            continue
        _, ln, typ = struct.unpack("<IHB", b[pos:pos + 7])
        if ln == 0 and typ == 0:
            pos += left
            continue
        data = b[pos + 7:pos + 7 + ln]
        pos += 7 + ln
        buf = data if typ in (1, 2) else buf + data
        if typ in (1, 4):
            r = pb.Record()
            try:
                r.ParseFromString(buf)
            except Exception:
                continue
            if r.WhichOneof("record_type") == "history":
                h = {i.key or "/".join(i.nested_key): json.loads(i.value_json) for i in r.history.item}
                if "loss_test_in" in h:
                    out.append(dict(epoch=h.get("_step"), train_loss=h.get("train_loss"), loss_test_in=h["loss_test_in"],
                                    loss_test_out=h.get("loss_test_out")))
    return out


def persistence():
    with tempfile.TemporaryDirectory() as d:
        c = Path(d) / "kolmo_test"
        shutil.copy(REPRO / "data" / "kolmo" / "kolmo_test", c)
        s = shelve.open(str(c), flag="r")
        Y = torch.cat([s[k] for k in sorted(s.keys(), key=int)])
        s.close()

    def rel(p, y):
        p, y = p.reshape(p.shape[0], -1), y.reshape(y.shape[0], -1)
        return float(((p - y).norm(dim=1) / y.norm(dim=1)).mean())
    yi, yo = Y[..., :20], Y[..., 20:]
    return dict(n_test=int(Y.shape[0]), persistence_test_in=rel(Y[..., :1].expand_as(yi), yi),
                persistence_test_out=rel(Y[..., :1].expand_as(yo), yo), zero_test_in=rel(torch.zeros_like(yi), yi))


def main():
    f = sorted(glob.glob(str(REPRO / "wandb" / "wandb" / "offline-run-*" / "run-*.wandb")), key=lambda p: Path(p).stat().st_mtime)[-1]
    log = (REPRO / "run_repro.log").read_text()
    J = dict(wandb_file=f, curve=wandb_evals(f), **persistence(), paper_in_d=PAPER_IN_D,
             finished="REPRO_DONE" in log, exit_line=[x for x in log.splitlines() if x.startswith("exit ")][-1:] or None)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(J, indent=1))
    print(json.dumps({k: v for k, v in J.items() if k != "curve"}, indent=1))
    for r in J["curve"]:
        print(r)


if __name__ == "__main__":
    main()
