# EXT2 spec integrity gate: learned-tokenizer kill test

Work order: "WO: Learned-tokenizer kill test (tokens-horizon paper)", issued 2026-09-25. Gate run by the executing
agent on 2026-09-26, before the freeze and before any training beyond a timing pilot. Template:
T_Spec-Integrity-Gate, checks 1 to 9 including 5a.

All numbers cited as "KKE3" come from `results/ext/kolmo/e3_rows.csv`: k-means patch rows at Δ = 0.35, future frames,
1,000 confirmation states. Horizons are in Lyapunov times. The floor of the future-frame score is one frame,
λΔ = 0.0444.

## Summary

| Part | Gate outcome | Action |
|---|---|---|
| Tokenizer, training, data | passes once pinned (checks 3, 4) | pinned in `ext2_freeze.yaml` |
| M1 to M6 measurements | passes | executed |
| R1 reading | passes (check 1 two-sided on cited analogues) | executed |
| R2 reading | referent "or above it" unpinned (check 3) | pinned: upper 95% limit of (M3 − M2) < 0 |
| **Paper-level kill criterion** | **fails check 3** (eligible set unpinned). Under the literal referent it also fails check 6 (outcome predictable from the paper's own rows) | **not applied.** R1 is reported per configuration together with both candidate eligible sets. The kill decision goes to Todd. |
| Figure "F8" | ID collision with the existing `figures/F8_controls.*` | issued as **F9** |
| Premise ("Why") | partly contradicted by KKE3 (check 4) | reported below; the measurements are unaffected |

## Spec errors found

1. **The kill-criterion referent is unpinned (check 3).** "Every configuration with at least 2^10 codes per token"
   excludes L8-b10 and L16-b10, because [8,5,5,5] gives 1,000 codes and 1,000 < 1,024. Two sets are possible:
   - the literal set {L8-b12, L8-b16, L16-b12};
   - the nominal set of all five configurations, if "b10" is read as 2^10 in the FSQ paper's sense. Mentzer et al.
     2023, Table 1, give [8,5,5,5] only as a set that approximately matches 2^10.

   The two sets can disagree. L16-b10 is the configuration the WO says must never be cut, and it is the only one
   whose k-means analogue passes R1 (item 2).
2. **Under the literal set, the kill outcome is predictable from rows already in the paper (checks 1 and 6).**
   The k-means analogues at ε = 0.1 fail R1 in every literal-set configuration:

   | Analogue | Ceiling | DI | Difference | Result |
   |---|---|---|---|---|
   | 8x8 b12 | 0.0443 | 0.251 | 0.207 | below the 0.25 margin, so no reading |
   | 8x8 b16 | 1.133 | 0.782 | ceiling above DI | R2 |
   | 16x16 b12 | 2.555 | 1.433 | ceiling above DI | R2 |

   The only analogue that passes R1 is 16x16 b10: ceiling 0.0445, DI 1.056 [1.010, 1.102]. It is excluded by the
   literal referent.

   This does not make the FSQ measurement degenerate. FSQ's reconstruction, and so its T_pt and its DI, can differ
   from k-means. The prior, however, points strongly toward the kill firing under the literal set.
3. **The premise in "Why" is partly false (check 4: a claim licensed only as a summary).**
   - "At 0.1σ, no decodable frame is within tolerance": KKE3 gives p_0 = 1.0 only for 8x8 b8 to b12 and 16x16 b8 to
     b10. It gives p_0 = 0.851 at 8x8 b14, 0.37 at 8x8 b16, 0.217 at 16x16 b12, 0.078 at 16x16 b14 and 0.048 at
     16x16 b16.
   - In those rows the ceiling lies **above** DI at ε = 0.1, for example 14.17 against 2.06 at 16x16 b16.

   So the tight-tolerance k-means result holds only at the low-bit end of each layout. "Its ceiling sits far above
   decode-and-integrate at 0.3σ" is correct: 8x8 b12 gives 13.97 against 1.46.
4. **There are no Kolmogorov training or validation blocks.** The extension generated only the calibration (fit and
   held-out) and confirmation blocks. I pinned and generated them under the freeze.yaml seed scheme:
   - training: stream 0, seed 20800;
   - validation: stream 0, seed 30800.

   Sizes are in the freeze.
5. **The R2 clause "or above it" is unpinned (check 3).** The frozen margins define "well below", "approximately
   equal" and "near", but not "above". Pinned as: the upper 95% limit of the paired difference (M3 − M2) is below 0.
   R1 is the frozen "well below" reading applied to (M3 − M2).
6. **Architecture, loss scale and divergence were not defined (check 3).** They are pinned in the freeze:
   - VQGAN-style residual blocks, channel widths and circular 3×3 convolutions;
   - the MSE scale, chosen so the loss equals the scored ‖x − x̂‖²/σ_A²;
   - the optimizer constants;
   - divergence: a non-finite loss, or a best validation loss ≥ 1, which is the zero-prediction null.
7. **The figure ID "F8" collides** with the existing `figures/F8_controls.*`. The new figure is **F9**.
8. **The figure's ε is unpinned.** F7 is drawn at ε = 0.3, but the WO's question is about ε = 0.1. Pinned: F9 has
   two panels, ε = 0.1 and ε = 0.3, both at Δ = 0.35 with future frames and F7's axes.
9. **"Bootstrap over confirmation trajectories."** Each of the 1,000 confirmation states lies on its own trajectory
   (one burned-in trajectory per state), so resampling states is resampling trajectories. `th/score.paired_diff`
   (2,000 reps, seed 777) is used unchanged. This is a clarification, not an error.
10. **The FSQ listing typo (check 4).** The paper's appendix listing computes the bound shift as `tan(offset/half_l)`.
    The intended function is arctanh, which is what the reference implementation uses and what is used here. With
    arctanh, even level counts get half-integer-centred bins.

## Checks

**1. Two-sided feasibility.** The passing and failing inputs are k-means analogues at Δ = 0.35 with future frames,
cited from KKE3. For FSQ they are hypotheses under test (check 5a).

| Condition | Passing input | Failing input |
|---|---|---|
| R1: difference ≥ 0.25 and 95% CI > 0 | 16x16 b10 at ε 0.1: T_pt 0.0445 against DI 1.056 (cited) | 8x8 b12 at ε 0.1: difference 0.207 < 0.25 (cited) |
| R2 approximately equal: 90% CI within ±0.10 | 8x8 b10 at ε 0.1: 0.0443 against 0.0486, difference 0.004 (cited; CIs [0.0443, 0.0443] and [0.046, 0.052]) | 16x16 b10 at ε 0.1 (cited) |
| R2 "above": upper 95% of (M3 − M2) < 0 | 16x16 b12 at ε 0.1: 2.555 [2.37, 2.75] against 1.433 [1.38, 1.49] (cited) | 16x16 b10 at ε 0.1 (cited) |
| Kill criterion | fires if no eligible configuration shows R1. With the k-means analogues, it fires under the literal set and does not fire under the nominal set, because 16x16 b10 passes (cited) | see check 3: the eligible set is unpinned |
| Divergence | a non-finite loss (hypothesis) | the timing-pilot loss decreasing from its initial value (observed in the pilot) |

**2. Independence.** The test consumes the learned decoder's reconstructions of future true frames and a trajectory
integrated from its decoded state. Neither was used to choose the configurations: the layouts and bit levels were
frozen in `ext_freeze.yaml` before any Kolmogorov tokenizer result, and the level sets are external. The analysis
passes.

**3. Referent.** It fails for the kill criterion (error 1) and for R2 "above" (error 5), and is pinned for R2. The
other referents are pinned:
- T_pt uses the first frame at which the learned encode-decode of the **true** state exceeds εσ_A.
- DI integrates the learned decode of x_0.
- Both use the E3 frame grid.

**4. Source class.**
- The level sets are the FSQ paper's Table 1 recommendations. That is an external design recommendation for image
  tokenizers, not a result about fluid fields.
- The premise sentences are an author summary of KKE3 and are partly contradicted (error 3).
- M2 is a reference, not a bound. Another token sequence from the same tokenizer could do better, because the
  learned encoder does not select the output-nearest code.

**5. No example as definition.** The claim "for k-means the ceiling equals the perfect-token horizon" is a
definitional identity: the k-means encoder is the exact nearest-code map, so d_C(x) equals the reconstruction error.
`scripts/ext_kolmo_e3.py` asserts that equality. It is not a worked example.

**5a.** Every passing and failing input above is either cited to KKE3 or labelled a hypothesis for FSQ.

**6. Surprise.**
- It would surprise the author if FSQ at L16-b12 or L8-b16 (4,375 or 64,000 codes per token) showed R1 at ε = 0.1.
  The k-means analogues' ceilings lie above DI there.
- It would also surprise the author if L16-b10 showed R2. That would mean a learned decoder removes the
  tight-tolerance k-means result at the paper's headline layout.

**7. Null baseline.**
- Persistence of the decoded state (M4) is the null forecaster.
- For reconstruction, the zero field gives ‖x‖/σ_A and the calibration mean gives about 1.0. Both are reported.
- The divergence rule is benchmarked against the zero-prediction null.

**8. Comparator separability.** The k-means rows in M6 are descriptive, with no reading, at nearest bits:
- 637.8 against 640 bits;
- 774.1 against 768;
- 1,021.8 against 1,024;
- 2,551 against 2,560;
- 3,096 against 3,072.

The rate differences are at most 0.8%. No threshold is set against the k-means rows.

**9. Selector separation.**

| Selector | Author | Read by |
|---|---|---|
| Configuration list (layouts 8x8 and 16x16, targets b10, b12, b16) | WO author: Todd with Claude (chat, 2026-09-25), inheriting the frozen extension layouts and bit levels | the same party |
| FSQ level sets | Mentzer et al. 2023, Table 1 (external) | — |
| Architecture and training pins | the executing agent (Claude), frozen before training | — |

Check 9 is not satisfied by a second author or by three framings. Every result is labelled as specific to one
learned tokenizer family, one architecture, one seed and one training budget. An R1 failure for this FSQ
autoencoder is one negative for "learned tokenizers", not a general one.

## Stops

- **The paper-level kill verdict is not issued** (check 3 failure). The results give R1 per configuration and which
  configurations would be eligible under each referent. The decision is Todd's.
- Everything else executes.
