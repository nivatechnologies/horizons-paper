"""Amendment 2, B3: prefix-invariance of the E4 models (must pass before any E4 training).

For random inputs, change every token (A, B) or patch value (C) in frames t+1 onward and assert that every
prediction made from the unchanged prefix (outputs at positions of frames <= t, which predict frames <= t+1) is
bitwise identical. Checked for every t, for A, B and C, on CPU and (if available) on each GPU, in train and eval mode.
"""
import sys
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from th.e4model import PatchSeqModel  # noqa: E402

DEVICES = ["cpu"] + ([f"cuda:{i}" for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else [])


def make(arm, device, frames=6, P=4, d=3, K=32):
    torch.manual_seed(0)
    protos = torch.randn(K, d) if arm in ("A", "B") else None
    return PatchSeqModel(arm, frames, P, d, K=K, protos_std=protos, width=32, layers=2, heads=4, ff=64).to(device)


def rand_input(arm, B, T, P, d, K, g):
    if arm in ("A", "B"):
        return torch.randint(0, K, (B, T, P), generator=g)
    return torch.randn(B, T, P, d, generator=g)


@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("arm", ["A", "B", "C"])
@pytest.mark.parametrize("mode", ["train", "eval"])
def test_prefix_invariance(arm, device, mode):
    frames, P, d, K, B = 6, 4, 3, 32, 5
    m = make(arm, device, frames, P, d, K)
    m.train() if mode == "train" else m.eval()
    g = torch.Generator().manual_seed(1)
    x = rand_input(arm, B, frames, P, d, K, g).to(device)
    with torch.no_grad():
        base = m(x)
        for t in range(frames - 1):                       # frames 0..t unchanged, t+1.. replaced
            x2 = x.clone()
            x2[:, t + 1:] = rand_input(arm, B, frames - t - 1, P, d, K, g).to(device)
            out = m(x2)
            assert torch.equal(out[:, :t + 1], base[:, :t + 1]), f"{arm} {device} {mode}: prefix changed at t={t}"
            # the test must be able to fail: some later output does change
            assert not torch.equal(out[:, t + 1:], base[:, t + 1:])


def test_mask_detects_leak():
    """Control: a model whose mask is removed must fail the check (the test can come out both ways)."""
    m = make("A", "cpu")
    m.mask.zero_()
    g = torch.Generator().manual_seed(2)
    x = rand_input("A", 3, 6, 4, 3, 32, g)
    with torch.no_grad():
        base = m(x)
        x2 = x.clone()
        x2[:, 3:] = rand_input("A", 3, 3, 4, 3, 32, g)
        assert not torch.equal(m(x2)[:, :3], base[:, :3])
