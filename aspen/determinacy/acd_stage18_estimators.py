"""Panel-disjoint E0/E1 estimator training, with resumable per-seed checkpoints."""
import argparse
import hashlib
import json
import math
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn


class Estimator(nn.Module):
    def __init__(self, action=False):
        super().__init__()
        self.action = action
        layers = []
        sizes = [12 if action else 11, 256, 256, 256, 256]
        for i in range(4):
            layers += [nn.Conv1d(sizes[i], sizes[i+1], 5, padding=2, padding_mode='circular'), nn.GELU()]
        self.trunk = nn.Sequential(*layers)
        self.head = nn.Linear(256, 1)

    def forward(self, history, action=None):
        value = torch.cat([history, action[:, None]], 1) if self.action else history
        return self.head(self.trunk(value).mean(-1))[:, 0]


def batches(data, ids, rng, rolling, device):
    if rolling:
        branches = rng.integers(2, size=len(ids))
        offsets = rng.integers(37, size=len(ids))
        entire = np.concatenate([data['H'][ids], data['T'][ids, branches]], 1)
        history = np.asarray([row[offset:offset+11] for row, offset in zip(entire, offsets)])
        action = data['A'][ids, branches]
    else:
        history = data['H'][ids]
        action = np.zeros((len(ids), 40), np.float32)
    return [torch.tensor(value, device=device, dtype=torch.float32)
            for value in [history, action, data['F'][ids]]]


def train(kind, seed, torch_seed, batch_seed, data, out, micro):
    from acd_stage18_inference import guarded, digest
    freeze = guarded()
    for name, expected in freeze['training_data_sha256'].items():
        if digest(data/name) != expected:
            raise RuntimeError('Training data differs from freeze: '+name)
    if (out/'complete.json').exists():
        return
    from acd_stage18_charge import Charge
    budget = Charge(out)
    torch.set_num_threads(4)
    torch.manual_seed(torch_seed)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    out.mkdir(parents=True, exist_ok=True)
    if (out/'complete.json').exists():
        return
    rolling = kind == 'E1'
    model = Estimator(rolling).cuda()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    training = np.load(data/'train.npz')
    validation = np.load(data/'val.npz')
    generator = np.random.default_rng(batch_seed)
    # Fixed trajectory-disjoint validation windows, independent of training order.
    vg = np.random.default_rng(np.random.SeedSequence([batch_seed, 1]))
    val = batches(validation, np.arange(len(validation['H'])), vg, rolling, 'cpu')
    best, selected, step, charged = math.inf, None, 0, budget.prior
    history = []
    resume = out/'resume.pt'
    if resume.exists():
        ck = torch.load(resume, weights_only=False)
        model.load_state_dict(ck['state_dict'])
        optimizer.load_state_dict(ck['optimizer'])
        generator.bit_generator.state = ck['batch_rng']
        torch.set_rng_state(ck['torch_rng'])
        torch.cuda.set_rng_state_all(ck['cuda_rng'])
        best, selected, step, history = [ck[k] for k in ['best', 'selected', 'step', 'history']]
        if selected is not None:
            selected_ck = torch.load(out/'selected.pt', map_location='cpu', weights_only=True)
            if selected_ck['step'] != selected or selected_ck['validation_MSE'] != best:
                eligible_path = out/f'checkpoint_{selected:06d}.pt'
                recovered = torch.load(eligible_path, map_location='cpu', weights_only=True)
                if recovered['step'] != selected or recovered['validation_MSE'] != best:
                    raise RuntimeError('Scheduled checkpoint does not match recovery identity')
                pending = out/'selected.tmp.pt'
                pending.write_bytes(eligible_path.read_bytes())
                pending.replace(out/'selected.pt')
    begin = budget.started
    for iteration in range(step+1, 5001):
        if charged+time.monotonic()-begin >= 36000:
            break
        ids = generator.integers(len(training['H']), size=128)
        h, a, f = batches(training, ids, generator, rolling, 'cuda')
        optimizer.zero_grad()
        total = 0.
        for b in range(0, len(ids), micro):
            predicted = model(h[b:b+micro], a[b:b+micro])
            loss = (predicted-f[b:b+micro]).square().mean()
            if not torch.isfinite(loss):
                raise RuntimeError('Nonfinite estimator loss; checkpoint remains resumable')
            (loss*len(predicted)/len(ids)).backward()
            total += float(loss.detach())*len(predicted)/len(ids)
        norm = torch.linalg.vector_norm(torch.stack([torch.linalg.vector_norm(p.grad) for p in model.parameters() if p.grad is not None]))
        if not torch.isfinite(norm):
            raise RuntimeError('Nonfinite estimator gradient; no optimizer step')
        nn.utils.clip_grad_norm_(model.parameters(), 1.)
        optimizer.param_groups[0]['lr'] = 1e-3*.5*(1+math.cos(math.pi*(iteration-1)/5000))
        optimizer.step()
        budget.snapshot()
        step = iteration
        if iteration % 100 == 0:
            print(kind, seed, iteration, total, flush=True)
        if iteration % 500 == 0:
            with torch.no_grad():
                mse = 0.
                for b in range(0, len(val[0]), micro):
                    hh, aa, ff = [x[b:b+micro].cuda() for x in val]
                    mse += float((model(hh, aa)-ff).square().mean())*len(hh)/len(val[0])
            ck = dict(state_dict=model.state_dict(), optimizer=optimizer.state_dict(), batch_rng=generator.bit_generator.state,
                      torch_rng=torch.get_rng_state(), cuda_rng=torch.cuda.get_rng_state_all(), step=step,
                      best=min(best, mse), selected=step if mse < best else selected,
                      charged_gpu_seconds=charged+time.monotonic()-begin,
                      history=history+[dict(step=step, validation_MSE=mse)])
            pending_checkpoint = out/f'checkpoint_{step:06d}.tmp.pt'
            checkpoint = out/f'checkpoint_{step:06d}.pt'
            torch.save(dict(state_dict=model.state_dict(), step=step, validation_MSE=mse), pending_checkpoint)
            pending_checkpoint.replace(checkpoint)
            if mse < best:
                pending_selected = out/'selected.tmp.pt'
                torch.save(dict(state_dict=model.state_dict(), step=step, validation_MSE=mse), pending_selected)
                pending_selected.replace(out/'selected.pt')
                best, selected = mse, step
            pending = out/'resume.tmp.pt'
            torch.save(ck, pending)
            pending.replace(resume)
            history = ck['history']
    if selected is None:
        raise RuntimeError('No frozen validation checkpoint exists')
    result = dict(estimator=kind, seed_index=seed, torch_seed=torch_seed, batch_seed=batch_seed,
                  completed_updates=step, selected_step=selected, validation_MSE=best,
                  charged_gpu_seconds=charged+time.monotonic()-begin,
                  gpu=torch.cuda.get_device_name(), torch=torch.__version__,
                  parameter_count=sum(p.numel() for p in model.parameters()),
                  selected_sha256=hashlib.sha256((out/'selected.pt').read_bytes()).hexdigest(),
                  data_sha256={name: hashlib.sha256((data/name).read_bytes()).hexdigest() for name in ['train.npz', 'val.npz']},
                  validation_windows='one fixed seeded offset and branch per trajectory for E1; pre-action for E0', history=history)
    budget.snapshot()
    (out/'complete.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--kind', choices=['E0', 'E1'], required=True)
    p.add_argument('--seed-index', type=int, required=True)
    p.add_argument('--torch-seed', type=int, required=True)
    p.add_argument('--batch-seed', type=int, required=True)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--micro', type=int, default=128)
    a = p.parse_args()
    train(a.kind, a.seed_index, a.torch_seed, a.batch_seed, a.data, a.out, a.micro)
