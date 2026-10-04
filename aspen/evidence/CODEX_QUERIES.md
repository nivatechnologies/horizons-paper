# Blinded query selector

## Exact prompt

A 2D incompressible flow on a 2π-periodic square is computed with the vorticity equation, Kolmogorov forcing A·sin(4y), Reynolds number Re and linear drag α. An engineer forecasts it from a short window of full-field observations. Propose four scalar forecast quantities, each evaluated a fixed short time ahead, that a practitioner would care about, chosen so that they depend on (Re, A, α) in clearly different proportions. Give the exact formula for each.

## Verbatim answer

A useful set is **forcing power, viscous energy loss, drag energy loss, and viscous enstrophy loss**. They measure energy supply, two competing energy sinks, and the dissipation of fine vorticity structure.

Take the forcing to be in the **vorticity equation**:
\[
\partial_t\omega+\mathbf u\cdot\nabla\omega
=Re^{-1}\Delta\omega-\alpha\omega+A\sin(4y).
\]
Define \(t_*=t+\tau\), with the same fixed short lead \(\tau>0\) for every forecast, and
\[
\langle g\rangle=\frac1{(2\pi)^2}\int_{[0,2\pi]^2}g\,dx\,dy.
\]
Recover the zero-mean velocity through
\(\Delta\psi=\omega,\ \mathbf u=(-\psi_y,\psi_x)\). All fields below are evaluated at \(t_*\).

| Forecast quantity | Exact formula | Parameter emphasis and practical meaning |
|---|---|---|
| Forcing power | \(\displaystyle I_*=\frac{A}{16}\langle\omega\sin(4y)\rangle\) | Explicitly proportional to \(A\); measures how much power the forcing supplies at the forecast time. |
| Viscous energy dissipation | \(\displaystyle D_{\nu,*}=\frac1{Re}\langle\omega^2\rangle\) | Explicitly proportional to \(Re^{-1}\); measures energy lost through viscosity. |
| Drag energy dissipation | \(\displaystyle D_{\alpha,*}=\alpha\langle|\mathbf u|^2\rangle\) | Explicitly proportional to \(\alpha\); emphasizes energetic large-scale motion. |
| Viscous enstrophy dissipation | \(\displaystyle H_{\nu,*}=\frac1{Re}\langle|\nabla\omega|^2\rangle\) | Emphasizes much finer spatial structure than \(D_{\nu,*}\); useful for forecasting sharp vorticity gradients and dissipation bursts. |

These enter the exact balances
\[
\frac{d}{dt}\frac{\langle|\mathbf u|^2\rangle}{2}
=I-D_\nu-D_\alpha,
\qquad
\frac{d}{dt}\frac{\langle\omega^2\rangle}{2}
=16I-H_\nu-\alpha\langle\omega^2\rangle.
\]
Energy and enstrophy balances are standard diagnostics for forced two-dimensional flow with drag. [Tsang & Young](https://arxiv.org/abs/0803.0558)

The different spatial weights also matter: in Fourier space, the three loss quantities weight \(|\widehat\omega_{\mathbf k}|^2\) by \(Re^{-1}\), \(\alpha/|\mathbf k|^2\), and \(|\mathbf k|^2/Re\), respectively.

**These are distinct parameter emphases, not guaranteed sensitivity ratios.** The forecast field itself depends on all three parameters; actual sensitivities require perturbation experiments over the intended operating range.

If \(A\sin(4y)\mathbf e_x\) instead denotes a **velocity body force**, replace the forcing-power formula by \(I_*=A\langle u_x\sin(4y)\rangle\); the other three formulas are unchanged.

## Single clarifying question

The mandated reused truth solver applies velocity body force A sin(4y) e_x, so its vorticity forcing is -4A cos(4y); the query lead is h=0.5/lambda(theta) after the last observation at each test point. For this convention, what are your final four exact scalar query formulas, retaining your four chosen quantities?

## Verbatim clarification answer

Let \(\theta=(Re,A,\alpha)\) and evaluate all fields at
\[
t_*=t_{\mathrm{last}}+\frac{0.5}{\lambda(\theta)}.
\]
With \(\langle g\rangle=(2\pi)^{-2}\int_{[0,2\pi]^2}g\,dx\,dy\), the four queries are
\[
\boxed{
\begin{aligned}
I_*&=A\langle u_x(t_*)\sin(4y)\rangle
=-\frac{A}{4}\langle\omega(t_*)\cos(4y)\rangle,\\
D_{\nu,*}&=\frac{1}{Re}\langle\omega(t_*)^2\rangle,\\
D_{\alpha,*}&=\alpha\langle|\mathbf u(t_*)|^2\rangle,\\
H_{\nu,*}&=\frac{1}{Re}\langle|\nabla\omega(t_*)|^2\rangle.
\end{aligned}}
\]
Here \(\omega=\partial_xu_y-\partial_yu_x\), consistent with the vorticity forcing \(-4A\cos(4y)\).