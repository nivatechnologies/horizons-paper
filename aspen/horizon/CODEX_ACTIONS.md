# Blinded action sets: exact WO prompt and verbatim Codex answers

Generated before any new experimental data. No final action-set choice has been made.

## Invocation 1

CLI: codex-cli 0.160.0. Empty isolated directory, read-only sandbox, ignored user configuration and policy rules. Completed tools: [].

### Exact prompt

```text
(1) Lorenz-96 with N = 40 and forcing F = 8. A controller may add a spatially structured forcing perturbation of small amplitude. Propose 8 candidate perturbation patterns a control engineer would compare for reducing the long-run mean energy (1/2N)Σx_i², each with an exact formula and a common amplitude parameter.

(2) 2D incompressible flow on a 2π-periodic square, vorticity form, Kolmogorov forcing sin(4y), Reynolds number 40, linear drag. A controller may modify the body forcing by a small amount. Propose 6 candidate forcing modifications a flow-control engineer would compare for reducing the mean enstrophy dissipation, each with an exact formula and a common amplitude parameter.
```

### Verbatim final answer

Use a common **RMS amplitude** \(\varepsilon\): every candidate adds \(\varepsilon p\), where \(p\) has unit spatial RMS. This makes the perturbation sizes comparable. These are candidates to test; their effect on a chaotic long-run average is not guaranteed.

### (1) Lorenz–96

Use indices \(i=0,\ldots,39\), interpreted modulo 40:
\[
\dot x_i=(x_{i+1}-x_{i-2})x_{i-1}-x_i+8+\varepsilon p_i,
\qquad \frac1{40}\sum_i p_i^2=1.
\]

Eight candidates are:

| Candidate | Exact pattern \(p_i\) | Purpose |
|---|---|---|
| Uniform forcing reduction | \(-1\) | Direct baseline for reducing energy input |
| Longest spatial wave | \(\sqrt2\cos(2\pi i/40)\) | Large-scale redistribution |
| Two-wave pattern | \(\sqrt2\cos(4\pi i/40)\) | Broad spatial structure |
| Four-wave pattern | \(\sqrt2\cos(8\pi i/40)\) | Intermediate scale |
| Eight-wave pattern | \(\sqrt2\cos(16\pi i/40)\) | Shorter spatial scale |
| Ten-wave pattern | \(\sqrt2\cos(20\pi i/40)\) | Four-site wavelength |
| Alternating forcing | \((-1)^i\) | Smallest resolved wavelength |
| Local reduction with compensation | \((1-40\delta_{i0})/\sqrt{39}\) | Concentrated actuation with zero net forcing change |

All except the uniform reduction have zero spatial mean. Compare their long-run
\[
E=\left\langle\frac1{80}\sum_i x_i^2\right\rangle_t.
\]
Testing both signs of \(\varepsilon\), and translated versions of structured patterns, helps avoid an arbitrary phase choice.

### (2) Periodic incompressible flow

Take “Kolmogorov forcing \(\sin(4y)\)” to mean the **body force**
\[
\mathbf f_0=(\sin4y,0).
\]
Its vorticity forcing is \(\operatorname{curl}\mathbf f_0=-4\cos4y\). If your convention instead specifies \(\sin4y\) directly in the vorticity equation, shift the baseline phase accordingly.

Write
\[
\mathbf f=\mathbf f_0+\varepsilon\mathbf p,\qquad
\mathbf p=(\partial_y\psi,-\partial_x\psi).
\]
Then every modification is divergence-free, its vorticity forcing is exactly
\[
\delta g=-\varepsilon\Delta\psi,
\]
and the following choices all satisfy
\[
\frac1{(2\pi)^2}\int_{[0,2\pi]^2}|\mathbf p|^2\,dx\,dy=1.
\]

| Candidate | Exact perturbation streamfunction \(\psi(x,y)\) | Added vorticity forcing \(\delta g/\varepsilon\) |
|---|---|---|
| Reduce original forcing | \(\dfrac{\sqrt2}{4}\cos4y\) | \(4\sqrt2\cos4y\) |
| Larger-scale shear | \(-\dfrac{\sqrt2}{2}\cos2y\) | \(-2\sqrt2\cos2y\) |
| Smaller-scale shear | \(-\dfrac{\sqrt2}{8}\cos8y\) | \(-8\sqrt2\cos8y\) |
| Long streamwise modulation | \(\dfrac{2}{\sqrt{17}}\cos x\cos4y\) | \(2\sqrt{17}\cos x\cos4y\) |
| Shorter streamwise modulation | \(\dfrac{1}{\sqrt5}\cos2x\cos4y\) | \(4\sqrt5\cos2x\cos4y\) |
| Large-scale cellular forcing | \(\sqrt2\cos x\cos y\) | \(2\sqrt2\cos x\cos y\) |

For the first candidate, \(\mathbf p=(-\sqrt2\sin4y,0)\), so positive \(\varepsilon\) reduces the baseline forcing.

Hold Reynolds number and drag fixed and compare
\[
D_\nu=\nu\left\langle|\nabla\omega|^2\right\rangle_{x,y,t}.
\]
If “enstrophy dissipation” includes linear drag \(-\alpha\omega\), compare instead
\[
D_{\rm total}=D_\nu+\alpha\langle\omega^2\rangle_{x,y,t}.
\]

If the engineering constraint requires preserving the original forcing amplitude, exclude the direct-reduction candidates from the comparison.

## Invocation 2

CLI: codex-cli 0.160.0. Empty isolated directory, read-only sandbox, ignored user configuration and policy rules. Completed tools: ['web_search'].

### Exact prompt

```text
(1) Lorenz-96 with N = 40 and forcing F = 8. A controller may add a spatially structured forcing perturbation of small amplitude. Propose 8 candidate perturbation patterns a control engineer would compare for reducing the long-run mean energy (1/2N)Σx_i², each with an exact formula and a common amplitude parameter.

(2) 2D incompressible flow on a 2π-periodic square, vorticity form, Kolmogorov forcing sin(4y), Reynolds number 40, linear drag. A controller may modify the body forcing by a small amount. Propose 6 candidate forcing modifications a flow-control engineer would compare for reducing the mean enstrophy dissipation, each with an exact formula and a common amplitude parameter.
```

### Verbatim preliminary assistant message

I’ll give explicit families with a shared amplitude normalization, and distinguish body-force modifications from their vorticity forcing so the flow candidates are unambiguous.

### Verbatim final answer

These are candidate families to test, not guaranteed improvements. Use a common **RMS forcing amplitude** \(\varepsilon\): every pattern below has RMS one, so equal \(|\varepsilon|\) means equal forcing perturbation strength.

**(1) Lorenz–96**

Use cyclic indices \(i=0,\ldots,39\) and
\[
\dot x_i=(x_{i+1}-x_{i-2})x_{i-1}-x_i+8+\varepsilon p_i,
\qquad
\frac1{40}\sum_i p_i^2=1.
\]
This is the standard Lorenz–96 convention. [DART documentation](https://docs.dart.ucar.edu/en/v11.22.0/models/lorenz_96/readme.html)

Let \(\theta_i=2\pi i/40\). Compare these eight fixed patterns:

| Candidate | Exact \(p_i\) | Purpose |
|---|---|---|
| 1. Uniform forcing reduction | \(-1\) | Benchmark for reducing input directly |
| 2. Domain-scale wave | \(\sqrt2\cos\theta_i\) | Broad spatial redistribution |
| 3. Two-wave pattern | \(\sqrt2\cos(2\theta_i)\) | Intermediate broad structure |
| 4. Four-wave pattern | \(\sqrt2\cos(4\theta_i)\) | Intermediate spatial scale |
| 5. Eight-wave pattern | \(\sqrt2\cos(8\theta_i)\) | Finer spatial scale |
| 6. Alternating sites | \((-1)^i\) | Finest resolved spatial structure |
| 7. Localized reduction with compensation | \(\displaystyle \frac{1-40\delta_{i0}}{\sqrt{39}}\) | Reduce forcing at one site, redistribute elsewhere |
| 8. Two opposing sectors | \(\displaystyle \begin{cases}-1,&0\le i<20,\\+1,&20\le i<40\end{cases}\) | Broad, discontinuous redistribution |

Candidates 2–8 have zero spatial mean and therefore preserve the mean forcing \(8\). Candidate 1 changes it to \(8-\varepsilon\).

Compare the long-run objective
\[
J_E(\varepsilon,p)=
\lim_{T\to\infty}\frac1T\int_0^T
\frac1{80}\sum_i x_i(t)^2\,dt.
\]
For the zero-mean patterns, test both signs of \(\varepsilon\). Under a translation-invariant, differentiable statistical response, their first-order effect on this spatially averaged objective vanishes; finite-amplitude and second-order effects matter.

**(2) Kolmogorov flow**

Interpret the stated forcing as the **body force**
\[
\mathbf f_0=(\sin4y,0).
\]
With \(\omega=\partial_xv-\partial_yu\), adopt
\[
\partial_t\omega+\mathbf u\cdot\nabla\omega
=\frac1{40}\Delta\omega-\alpha\omega-4\cos4y
+\varepsilon q,
\qquad \alpha>0.
\]
Here \(\alpha\) is the fixed drag coefficient, and \(q=\partial_xg_y-\partial_yg_x\) for the body-force modification
\[
\delta\mathbf f=\varepsilon\mathbf g,
\qquad
\langle|\mathbf g|^2\rangle=1.
\]
Angle brackets denote area averages. Kolmogorov flow with drag is a standard setting for energy–enstrophy analysis. [Research paper](https://arxiv.org/abs/0803.0558)

All six modifications below are periodic, divergence-free, and have zero spatial mean:

| Candidate | Exact body-force pattern \(\mathbf g(x,y)\) | Vorticity-forcing pattern \(q(x,y)\) |
|---|---|---|
| 1. Reduce original forcing | \((-\sqrt2\sin4y,0)\) | \(4\sqrt2\cos4y\) |
| 2. Add a broader shear | \((\sqrt2\sin2y,0)\) | \(-2\sqrt2\cos2y\) |
| 3. Add a finer shear | \((\sqrt2\sin8y,0)\) | \(-8\sqrt2\cos8y\) |
| 4. Add a perpendicular shear | \((0,\sqrt2\sin4x)\) | \(4\sqrt2\cos4x\) |
| 5. Add an oblique shear | \((1,-1)\sin(4x+4y)\) | \(-8\cos(4x+4y)\) |
| 6. Modulate the forcing across \(x\) | \(\displaystyle\frac2{\sqrt{17}}(-4\cos x\sin4y,\;\sin x\cos4y)\) | \(2\sqrt{17}\cos x\cos4y\) |

Use the viscous enstrophy-dissipation objective
\[
J_\Omega=\overline{\frac1{40}\langle|\nabla\omega|^2\rangle}.
\]
If “enstrophy dissipation” includes drag, use instead
\[
J_{\Omega,\mathrm{total}}
=\overline{\frac1{40}\langle|\nabla\omega|^2\rangle
+\alpha\langle\omega^2\rangle}.
\]

Keep \(\alpha\) fixed across comparisons. Equal body-force RMS does **not** imply equal vorticity-forcing RMS: finer-scale forcing has a larger curl. If \(\sin4y\) was intended as the scalar vorticity forcing, that requires a different baseline body force.


## Selector overlap and unresolved choice

This is a formula/family comparison, not a performance result. Claude's sets are descriptions from the WO, not exact formulas; exact overlap counts against Claude cannot be asserted.

| Comparison | Overlap | Differences / ambiguity |
|---|---|---|
| CLI run 1 vs run 2, Lorenz-96 | 7 of 8 exact patterns shared: uniform reduction, cosine modes 1/2/4/8, alternating sites, compensated single-site reduction | Run 1 adds mode 10; run 2 adds opposing half-domain sectors |
| CLI run 1 vs run 2, Kolmogorov | 4 of 6 exact body-force patterns shared: baseline reduction, mode-2 shear, mode-8 shear, mode-(1,4) modulation | Run 1 adds mode-(2,4) modulation and a cellular mode-(1,1); run 2 adds perpendicular mode-4 and oblique mode-(4,4) shear |
| Each CLI run vs Claude, Lorenz-96 | Shared families: uniform offset, modes 1/2/4, localized intervention | Claude's sectors are not exact formulas; compensated single-site actuation is not an uncompensated sector. Run 2 additionally has opposing sectors |
| Each CLI run vs Claude, Kolmogorov | Both share baseline-amplitude reduction | Neither has Claude's explicit phase shift, mode-3 shear or damping patch. Run 2 has a cos(4x) vorticity-forcing component, but Claude's forcing convention is unspecified |

Claude sets, verbatim from WO:
- Lorenz-96: sector-localized increases and decreases, wavenumber 1, 2 and 4 patterns, a uniform offset.
- Kolmogorov: amplitude ±, a phase shift, a sin(3y) component, a cos(4x) component, a localized damping patch.

Both CLI responses choose a common RMS **body-force** amplitude for Kolmogorov and distinguish viscous dissipation from dissipation including drag. Neither choice is silently adopted as the WO's missing objective rule. Final action-set selection/comparison remains blocked pending a pre-data rule. Both answers are retained unchanged; no experimental performance was used to prefer one.

Run 1 completed without tools; run 2 performed a web search using the operation/system vocabulary. Neither invoked a shell command or read repository files. The exact user prompt is duplicated above, and preliminary assistant text is retained. CLI method follows the [official noninteractive documentation](https://learn.chatgpt.com/docs/non-interactive-mode); installed CLI version is recorded per invocation.

Selector provenance: blinded Codex CLI authors for these two sets; Claude explicitly credited by the WO for comparison families. Both CLI calls share one prompt framing, so no “two independent negatives” interpretation is admissible.
