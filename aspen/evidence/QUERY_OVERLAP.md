# Query selector provenance and overlap

Final selector: one blinded Codex CLI invocation of the exact WO prompt, followed by the single permitted forcing-convention clarification. The empty-directory invocation received no work-order criteria, competing query list or experimental data. All prompts and verbatim answers are in CODEX_QUERIES.md and step0/. No second selection run was made.

| Final query | Exact scalar at t*=t_last+0.5/λ(θ) | Claude overlap |
|---|---|---|
| Forcing power | A mean(u_x sin(4y)) = -A/4 mean(ω cos(4y)) | Exact: forcing power input |
| Viscous energy dissipation | mean(ω²)/Re | Not identical; proportional to Claude's enstrophy at fixed Re |
| Drag energy dissipation | α mean(\|u\|²) | Exact: α·2E |
| Viscous enstrophy dissipation | mean(\|∇ω\|²)/Re | Distinct gradient diagnostic |

Claude's WO set is kinetic energy E=mean(|u|²)/2, enstrophy Z=mean(ω²)/2, drag dissipation 2αE and forcing power input. Exact quantity overlap is 2 of 4. Two additional state-statistic relationships exist: the viscous-energy query is 2Z/Re; the drag query is 2αE. Those relationships do not make the selectors identical across varying parameters.

The final formulas are executable for the inherited zero-mean velocity reconstruction and velocity body force. The original answer's vorticity-source power formula A/16 mean(ω sin(4y)) is not substituted into the World D solver. The single clarification retains all four quantity choices and supplies the matching formula, without changing the query family.

Authorship: blinded query author and explicitly WO-attributed Claude comparison set; angle, displacement, arm, box and outcome selectors by amended WO author, as accounted in AEA_GATE.md. Four queries in one prompt represent one independent framing for negative findings. Actual sensitivity proportions remain hypotheses to be measured; no test-point or learned-error data exist.
