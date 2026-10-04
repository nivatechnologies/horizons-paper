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
