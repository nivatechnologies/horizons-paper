# Step 0: blinded second mismatch term (OpenAI Codex)

Work order: WO_Adapt-The-Physics-Pivot-Kill-Test-2026-09-26, step 0. This file was committed before any other pivot
work.

## Invocation

- **Tool:** OpenAI Codex CLI `codex-cli 0.156.0`, run non-interactively.
- **Started:** Sat Sep 26 08:27:26 AM UTC 2026.
- **Command:** `codex exec --skip-git-repo-check --ephemeral --ignore-rules -s read-only -C <new empty directory> --json -o answer.md "<prompt>" < /dev/null`
- **Blinding:** the working directory was new and empty, and the session was ephemeral. The only input was the
  prompt below, with no repository, method, arm or result information.
- **What Codex did:** its tools were web search only. The event log shows no shell commands. Item and event counts:
  {"thread.started": 1, "turn.started": 1, "agent_message": 2, "web_search": 6, "turn.completed": 1}.
- **Earlier attempts:**
  - The first attempt blocked waiting on stdin and produced no output. It was killed.
  - A rerun was killed by the executor's own `pkill -f` before it produced any output.
  - The answer below is from the first run that completed.

## Prompt (exact)

A flow is simulated with the 2D incompressible Navier–Stokes equations in vorticity form on a 2π-periodic 64×64 pseudo-spectral grid. It has Kolmogorov forcing proportional to sin(4y), Reynolds number 40, and a linear drag term. Propose one additional physical effect that a real laboratory or engineering version of this flow would have, and that a standard solver of this form omits. It must not be linear drag. Give: (1) the exact term to add to the vorticity equation, with any parameters; (2) its physical justification; (3) a magnitude such that it changes the time-averaged enstrophy dissipation at Re 40 by about 10 to 15%, while the flow remains chaotic. Choose the term you consider most realistic, not the easiest to model.

## Answer (verbatim)

**Effect: topographic potential-vorticity advection** in a shallow, rotating laboratory flow. A gentle bottom slope changes the fluid-column depth, so a moving column is stretched or compressed. This effect appears in barotropic models of laboratory flows over topography, and the β effect is known to change Kolmogorov-flow stability. ([laboratory and model study](https://journals.ametsoc.org/view/journals/phoc/30/9/1520-0485_2000_030_2141_iobvwc_2.0.co_2.xml), [Kolmogorov-flow stability study](https://www.sciencedirect.com/science/article/abs/pii/S0167278901003840))

With \(\omega=\Delta\psi\), \(\mathbf u=(-\psi_y,\psi_x)\), and \(J(a,b)=a_xb_y-a_yb_x\), add

\[
\partial_t\omega+J(\psi,\omega)+\beta_T\,\partial_x\psi
=\frac{1}{40}\Delta\omega-\alpha\omega+F\sin(4y).
\]

Here \(-\alpha\omega\) is the solver’s existing drag. The added term follows from advecting \(q=\omega+\beta_Ty\), the linearized potential vorticity. For a tank with mean depth \(H(y)\), \(\beta_T\simeq-f_0\,\partial_y\ln H\), where \(f_0\) is the rotation frequency parameter.

As a **starting magnitude**, use \(\hat\beta_T=\beta_T/(U_f k_f^2)=0.1\), with \(k_f=4\) and \(U_f\) the velocity scale used to define the forcing-scale Reynolds number. This makes the topographic term about 10% of the advective vorticity term at the forcing scale. It is a plausible order-of-magnitude setting, not a guaranteed 10–15% dissipation shift: \(\beta_T\) changes the flow and therefore changes viscous enstrophy dissipation indirectly. Measure \(\bar\eta=\langle\nu|\nabla\omega|^2\rangle\) and tune around this setting until its time average differs from the baseline by 10–15%; also check that the chaotic dynamics persist. Re=40 alone cannot determine the matching value, since the forcing amplitude and drag coefficient also affect the response.
