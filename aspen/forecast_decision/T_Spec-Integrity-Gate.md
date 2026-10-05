# Spec Integrity Gate

Standing template. Applies to every work order, scoring rule, filter, axis, threshold or classification Claude writes for an executing agent, **and to every SELECTOR Claude produces anywhere, including in conversation** (see check 9).

Written 2026-08-15 after six specification defects in the inversion-hunt workstream, all of the same class, each caught by the executing agent rather than by the author. Extended 2026-08-15 to checks 7, 8, 5a and 9 as three further instances of the same class appeared.

## The defect class, stated once

Every one produced a specification **whose outcome was determined before any data arrived.**

| # | Defect | Shape |
|---|---|---|
| 1 | Filter A redundant with the sampling frame | Could not fail |
| 2 | Ground-truth partition ambiguous between state and parameter | Referent unpinned |
| 3 | Atlas hypothesis document read as capability inventory | Source class misread |
| 4 | "Top band" never operationally defined | Could not pass |
| 5 | Worked example used as a definitional anchor | Answer fixed by fiat |
| 6 | Artifact conflated with calibration | Could not pass |
| 7 | Cavity-pressure passing example physically wrong | Unverified domain claim smuggled through check 1 |
| 8 | Lineage rubric graded candidates as solutions, so the Niva-shaped opportunity scored as a failure | Wrong construct |
| 9 | Owl query vocabulary drawn from the already-chosen candidate domain, then that domain read back out as the finding | Selector authored by the party reading the result |

Three families. **Degenerate decision geometry** (1, 4, 6): the test cannot come out both ways. **Unpinned referents** (2, 3, 5, 7): a term, source or example whose meaning is not fixed, so the executor fixes it and the author never learns which fixing happened. **Conflicted authorship** (8, 9): the same party authored both the thing being tested and the instrument that tests it.

The single diagnostic that covers the first two families: **if you can predict the specification's output without running it, it is not measuring anything.**

The diagnostic for the third: **if you can name the answer you expect before writing the selector, and the selector carries that answer's vocabulary, it is not measuring.**

## The checks

Nine checks plus 5a. Checks 1 to 6 date from the original six defects; 5a, 7 and 8 were added 2026-08-15, and 9 later the same day. Run all of them before a specification or selector is issued. Any check that cannot be answered in writing blocks it.

**1. Two-sided feasibility.** Construct one concrete input that would pass and one that would fail. Write both down. If either cannot be constructed, the condition is degenerate and must be rewritten. This check alone would have caught defects 1, 4 and 6.

**2. Independence.** Does this test consume information the selection step did not already use? A filter applied to the property the population was sampled on rejects nothing. Name the new information explicitly.

**3. Referent.** For every classifying term, name the object it classifies, not the concept. "Is the state hidden" is unpinned. "Is the *plant parameter* recoverable before the decision commits" is pinned. If two competent readers could classify the same row differently, the referent is not pinned.

**4. Source class.** For every input, state what kind of claim the source licenses. A hypothesis document is not an inventory. A patent background is a credible concession and an advocacy magnitude. A design note is not an implementation. A self-consistency result is not a validation.

**5. No example as definition.** Examples illustrate; they never define. If a worked example is carrying definitional weight, either replace it with a rule or label it contested and exclude it from scoring.

**5a. Applies to the passing and failing inputs from check 1.** Check 1 asks the author to construct a concrete passing input, which is exactly where an unverified domain claim gets smuggled in and then shapes every downstream verdict. A constructed example must be **cited, or explicitly labelled a hypothesis under test**. It is never an anchor. Worked instance: the re-spec WO asserted a cavity pressure trace as the concrete passing input for identifying a polymer-mould heat transfer coefficient. Two agents confirmed at source that cavity pressure goes to zero exactly when the air gap forms, which is the HTC-relevant regime, so the example was physically wrong and it was the exemplar the whole correction was built around.

**6. Surprise.** Name one result this spec could return that would surprise the author. If there is none, the spec is confirming, not testing.

**7. Null baseline.** Every comparator set includes a null model: predicting nothing, predicting the mean, predicting no change. Added after a comparator was found to be 2.29 times worse than predicting zero warpage everywhere. "Beats the incumbent" is not a result if the incumbent is worse than the null, and a threshold set against such an incumbent measures nothing.

**8. Comparator separability.** Where a spec names a best-in-class comparator, check that it is distinguishable from the next one. If uncertainty bands touch, or the ordering reverses between datasets, say so and threshold against the better of the pair or against the null. Quoting the single most favourable cell of a comparison table is cherry-picking even when the cell is real.

**9. Selector separation.** Added 2026-08-15 after defect 9.

A **selector** is any artifact that narrows what will be looked at before evidence arrives: a query set, a candidate list, a shortlist, a taxonomy, a vocabulary, a comparator choice, a domain framing. Selectors were previously outside this gate entirely, because they are not specifications sent to an executing agent, and that is exactly how defect 9 got through.

**The rule: the party that authored the selector may not be the party that reads the result as a finding.**

Two admissible implementations, either sufficient:

- **Different author.** A second model, or a blinded agent, generates a competing selector from a different starting point. Report the overlap alongside the result. Heavy overlap suggests the selector is measuring the space; divergence means the first selector was measuring its author's prior.
- **Three framings.** Generate the selector from at least three independent framings of the same question. Any result that appears in only one framing is labelled **vocabulary-dependent**, not a finding.

Two rules that travel with check 9:

- **Independence accounting on negatives.** N queries sharing one framing are **one** negative, not N. Report negatives as the count of independent framings, never the count of queries. Defect 9's result was reported as "five for five negative" when it was one negative in five phrasings.
- **Selector provenance line.** Whenever a negative, a ranking or a shortlist is reported, one line states which selector produced it and who authored that selector. This is the cheapest component and the one that makes the conflict visible in the same turn rather than several turns later.

**Generative rule for search selectors:** derive the terms from the *operation*, not from the *candidate*. Ask what a practitioner who performs this operation for a living calls it. Defect 9's searches were written in Earth observation vocabulary because Earth observation was already the author's candidate; deriving them from the operation itself would have surfaced redatuming, virtual staining and synthetic MRI.

## Correction discipline

When a specification fails and is revised, the revision is suspect by default, because it arrives from the same author who wrote the failure and it usually has the property of making the blocked work possible again.

**A revision must make a differential prediction: which cases stay failed.** A correction that revives everything it was blocking is a rescue, not a correction. State the prediction before the revision runs, and treat a full revival as evidence the revision is wrong.

## Where the gate sits

**The executing agent runs this gate on the specification and reports before executing it.** Not the author.

This is the structural part and it matters more than the checklist. The original six defects were found by the agent, none by the author, and that is not an accident: the author cannot see a degeneracy they built, while the executor discovers it by running into it. Moving the check upstream of execution converts a wasted run into a paragraph. Across all nine defects the count is the same: eight caught by an executing agent or a second model, zero by the author. Any fix that depends on the author noticing is not a fix.

An agent receiving a specification that fails a check should **refuse to execute and report which check failed and why**, rather than executing a defective spec faithfully. A faithful execution of a broken spec is the expensive failure mode.

**For selectors there is no executing agent**, which is why check 9 names a second author or three framings instead. The separation is the mechanism in both cases; only the second party changes.

## Boilerplate for work orders

Every WO from 2026-08-15 carries this block:

> **Spec integrity gate.** Before executing, run checks 1 to 9 including 5a in [[T_Spec-Integrity-Gate]] against this work order and report the results. For each scoring axis, filter, threshold or classification here, state a concrete passing input and a concrete failing input, and cite each or label it a hypothesis under test per check 5a. For any selector this WO contains or relies on (query set, candidate list, shortlist, taxonomy, vocabulary, comparator or domain framing), report who authored it and satisfy check 9 by a second author or three independent framings. If any check fails, do not execute that part; report the failure and stop for that part. Faithful execution of a defective specification is a worse outcome than a halt.

