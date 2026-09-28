"""Computationally equivalent reformulation of the GEPS low-rank layers (geps_freeze.yaml `efficiency`).

GEPS conditions every layer on a context c (codes passed as diag_embed(c)): the effective weight of sample b is
W + sum_r c[b, r] * (A_r outer B_r). The released code materialises that per-sample weight (and applies the 7x7
convolution through an explicit strided-window einsum), which costs O(batch) memory and time per layer. Because the
context enters linearly, the same output is

    f(x; W) + sum_r c[b, r] * f(x; A_r outer B_r)      (+ bias + c @ bias_context)

where f is the layer's own linear map (cross-correlation on the circularly padded input, dense map, or Fourier-mode
multiplication). The functions below compute exactly that with standard kernels: same parameters, same parameter names,
same function of the inputs; only the order of the linear operations changes (floating-point rounding differs at the
1e-6 relative level; verified by verify()). Swish is unchanged.

Usage: import geps_fast; geps_fast.patch()   (after the GEPS package is importable)
"""
import torch
import torch.nn.functional as F


def _diag(codes):
    return torch.diagonal(codes, dim1=-2, dim2=-1)               # (b, r)


def conv2d_forward(self, input, codes):
    c = _diag(codes)
    x = F.pad(input, (self.padding,) * 4, mode=self.padding_mode)
    # rank-r weights W_r[o, i, k, l] = A[i, r, k, l] * B[o, r, k, l]
    Wr = torch.einsum("irkl,orkl->roikl", self.A, self.B)            # (r, O, I, k, l)
    R, O = Wr.shape[0], Wr.shape[1]
    Wall = torch.cat([self.weight[None], self.factor * Wr], 0).reshape((R + 1) * O, *self.weight.shape[1:])
    y = F.conv2d(x, Wall, stride=self.stride)                       # (b, (R+1) O, H, W): one cuDNN convolution
    y = y.view(x.shape[0], R + 1, O, y.shape[-2], y.shape[-1])
    out = y[:, 0] + torch.einsum("br,brohw->bohw", c, y[:, 1:])
    bias = self.bias + self.factor * (c @ self.bias_context)
    return out + bias[..., None, None]


def linear1d_forward(self, input, codes):
    c = _diag(codes)                                              # (b, r)
    base = input @ self.weight                                    # (b, n, out)
    xa = input @ self.A                                           # (b, n, r)
    ctx = (xa * c[:, None, :]) @ self.B                           # (b, n, out)
    bias = self.bias + self.factor * (c @ self.bias_context)
    return base + self.factor * ctx + bias.unsqueeze(1)


def spectral2d_forward(self, x, codes):
    c = _diag(codes).to(torch.cfloat)
    b = x.shape[0]
    x_ft = torch.fft.rfft2(x)
    out_ft = torch.zeros(b, self.out_channels, x.size(-2), x.size(-1) // 2 + 1, dtype=torch.cfloat, device=x.device)
    m1, m2 = self.modes1, self.modes2

    def mul(xs, W, A, B):
        base = torch.einsum("bixy,ioxy->boxy", xs, W)
        xa = torch.einsum("bixy,irxy->brxy", xs, A.to(torch.cfloat))
        ctx = torch.einsum("brxy,roxy->boxy", xa * c[:, :, None, None], B.to(torch.cfloat))
        return base + self.factor * ctx

    out_ft[:, :, :m1, :m2] = mul(x_ft[:, :, :m1, :m2], self.weights1, self.A_1, self.B_1)
    out_ft[:, :, -m1:, :m2] = mul(x_ft[:, :, -m1:, :m2], self.weights2, self.A_2, self.B_2)
    return torch.fft.irfft2(out_ft, s=(x.size(-2), x.size(-1)))


ORIG = {}


def patch():
    from geps.model import layers as L
    for cls, fn in ((L.GEPSConv2D, conv2d_forward), (L.GEPSLinear1D, linear1d_forward),
                    (L.GEPSSpectralConv2d_fast, spectral2d_forward)):
        ORIG.setdefault(cls, cls.forward)
        cls.forward = fn


def unpatch():
    for cls, fn in ORIG.items():
        cls.forward = fn


def verify(device="cuda", seed=0):
    """Original vs reformulated forward on random parameters, inputs and codes; returns max relative differences."""
    from geps.model import layers as L
    torch.manual_seed(seed)
    r = 4
    res = {}
    for name, mk, xin in (
            ("conv2d", lambda: L.GEPSConv2D(16, 16, 7, 3, padding_mode="circular", bias=True, code=r),
             lambda b: torch.randn(b, 16, 64, 64)),
            ("linear1d", lambda: L.GEPSLinear1D(16, 32, True, r), lambda b: torch.randn(b, 100, 16)),
            ("spectral2d", lambda: L.GEPSSpectralConv2d_fast(16, 16, 10, 10, r), lambda b: torch.randn(b, 16, 64, 64))):
        m = mk().to(device)
        for p in m.parameters():
            if p.dtype.is_complex:
                p.data = torch.randn_like(p.data) * 0.1
            else:
                p.data.normal_(0, 0.1)
        b = 5
        x = xin(b).to(device)
        cd = torch.diag_embed(torch.randn(b, r, device=device))
        unpatch()
        y0 = m(x, cd)
        patch()
        y1 = m(x, cd)
        res[name] = float((y1 - y0).abs().max() / y0.abs().max())
    return res
