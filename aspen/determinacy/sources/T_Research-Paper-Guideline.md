# Research Paper Guideline

Standing template for every Niva research paper, website paper or preprint. It governs how a paper is chosen, tested, narrowed or stopped, and written. Work orders for paper experiments carry the [[T_Spec-Integrity-Gate]] block as before. This guideline sits above that gate: the gate checks that a specification can measure something, and this guideline checks that the thing measured is worth publishing.

Written 2026-09-25, after two papers in a row began with a bold thesis and ended with a narrow result: the lagging-thermocouple paper and "You Can't Train Past Your Vocabulary". Their pattern is described in the last section.

## 1. The publication rule

**A Niva paper shows that Niva's approach, or the paradigm it embodies, beats the strongest current practice by a margin a practitioner would act on, at the practitioner's own operating point.** Limitations belong in the paper when they are the price of that advantage and are smaller than it.

The rule has two corollaries.

- **Limitation-of-the-incumbent papers need the other half.** Showing that the current paradigm fails somewhere is half a paper. The other half shows that the alternative Niva stands for does not fail there, at a cost the reader would accept. Without it the reader's response is "so what".
- **Choosing what to publish is strategy. Choosing what to report inside a paper is not.** We may decline to publish a result, and we may choose which true result to headline. Inside a published paper we never omit a result within its stated scope that contradicts its headline. We never tune on confirmation data, and we label every post-hoc analysis. Unpublished results go into the vault as a findings harvest (section 10), where they inform strategy and seed the next hypothesis.

**The so-what test.** After reading only the abstract, a reader at a target lab would do at least one of three things: change a design decision, try Niva's approach, or cite the paper as evidence for it. If none applies, the paper does not ship.

**The reconsider test.** Rigor and honesty are the floor, not the goal. A Niva paper makes the reader reconsider how they see their problem. Before writing, state the revelation in two sentences: what the target reader believes now, and what the result shows instead. A result that only adds a data point to what the reader already believes fails this test, even when it passes the so-what test.

## 2. Start with the headline contract

Before any experiment is specified, write the headline contract (template below) and get Todd's go. It fixes five things.

1. **Headline sentence**, as it would appear in the abstract, with the number that would make it matter. Example form: "At [reader's operating point], [Niva approach] achieves [metric] of X against Y for [strongest incumbent], a Z-fold improvement."
2. **Reader and operating point.** Who the reader is, and what they actually use: their model class, tokenizer or solver, scale, data regime and accuracy requirement. The operating point is theirs, not ours. A toy setting is allowed only to explain a mechanism, never to carry the headline.
3. **Strongest incumbent.** The best configuration the reader would realistically deploy, with its standard tuning. Also a null model, per gate check 7.
4. **Publish threshold and kill threshold.** The publish threshold is the smallest effect, in the reader's units, that passes the so-what test. The kill threshold is the result that ends the paper, and it is written before any data arrives.
5. **Pre-mortem.** The three most likely reasons a skeptical reader at the target lab would ignore the published paper. Each must map to an experiment in stage 1 or 2. The reader's most likely objection is tested first.

## 3. The fidelity ladder

Every stage has a budget, a gate and three possible outcomes: go, pivot or stop. Todd makes each gate decision. Claude brings a one-paragraph gate summary: the headline value now, what changed, and whether Claude would go, pivot or stop, and why.

| Stage | Budget | What it does | Gate |
|---|---|---|---|
| **0. Desk** | hours | Literature and prior-result check, a back-of-envelope effect estimate at the reader's operating point, and a check that a Niva arm exists or can be built cheaply. | The estimated effect is at least the publish threshold, and the thesis has not already been shown or refuted. |
| **1. Kill test** | at most 1 day and about 10 GPU-hours | The cheapest experiment that could falsify the headline at the reader's operating point: the realistic incumbent, the Niva arm, a small panel. Manual runs are fine. | The effect is at least 1.5 to 2 times the publish threshold. Effects shrink as fidelity rises, so a stage-1 effect that only just clears the threshold is a stop. |
| **2. Robustness pilot** | at most 3 days | The pre-mortem objections, each tested, plus robustness of the headline to analysis conventions (scoring rule, tolerance, metric, panel). | The effect survives, and the narrowing ledger (section 4) stays above the publish threshold. |
| **3. Freeze and confirm** | as planned | Pre-registered protocol, margins and readings, then the full campaign. | Frozen readings, with number provenance through a NUMBERS file and its checker. |
| **4. Write, review, release** | 1 to 2 days | The writing rules (section 6), one draft review and a factual audit. | The release checklist (section 8). |

Rules that travel with the ladder:

- **Steelman first.** A provocative claim is most likely to fail where the incumbent is strongest, and that is usually the reader's operating point. Test there first. Toy-first sequencing makes bold claims easy early and lets realism erode them later. That is the pattern this guideline exists to stop.
- **Realism enters at stage 1, not after the draft.** If a realistic setting is added after a result exists, it is a new kill test for the headline. It is not an extension.
- **A convention cannot carry the headline.** If the headline changes sign or magnitude under a reasonable alternative convention (scoring from t = 0 rather than from the first forecast frame, a different tolerance, a different panel), the headline is the convention, not the finding. Find this at stage 2.
- **Pre-registration belongs at stage 3, not stage 1.** Freezing a protocol before the kill test spends rigor on a thesis that has not yet earned it. Freezing after it protects the result that has.

## 4. Close the loop: the narrowing ledger

Every paper keeps a one-page claim ledger in the vault, updated at every gate and after every review round.

- **Headline v0** is the contract as first written. Each revision records the new headline, the reason for it (data, review or scope decision), and the **headline value**: the effect at the reader's operating point times the breadth of settings it covers.
- **Two kinds of narrowing.** *Precision narrowing* states the same claim more exactly and costs nothing: "at 0.3 of the attractor spread" in place of "at a loose tolerance". *Scope narrowing* shrinks where the claim holds, and it counts against the paper.
- **Drift triggers.** Any one of these forces a ledger review with Todd before more work is spent:
  - the headline number moves by more than 30%, or its setting changes;
  - a new qualifier enters the abstract;
  - the reader's operating point falls outside the region where Niva wins;
  - an experiment is proposed to find a setting where the claim still holds after it failed at the operating point. That is a rescue. A rescue is allowed only as a pivot: a new contract and a new stage-1 kill test.
- **Stop rule.** Stop or pivot when any one of these holds. Time already spent is not a reason to continue.
  - The headline value falls below the publish threshold.
  - The limitations, measured in the reader's units, reach half the size of the gain.
  - The winning region no longer contains the reader's operating point.
- **Pivot while the deadline leaves time for a kill test** (Todd, 2026-10-04; replaces a one-pivot limit Claude had drafted). Each pivot gets its own headline contract and stage-1 kill test, and every stopped line gets a findings harvest (section 10).

## 5. What makes a hypothesis worth testing

Prefer hypotheses that have all of these properties.

1. **Comparative, with a Niva arm.** The claim is "our approach beats theirs by X", not only "theirs has a limit".
2. **Monotone in the stakes.** The advantage grows with something the reader cares about: required accuracy, state dimension, forecast horizon, data scarcity, distribution shift, safety margin. Then the realistic regime is where we win, and realism strengthens the paper instead of eroding it.
3. **Mechanism-backed.** We can say why the advantage exists, and the mechanism predicts where it holds and where it does not. That turns limitations into stated boundaries rather than surprises.
4. **Cheap to kill.** A stage-1 test exists within a day.
5. **Robust to convention.** The headline survives the obvious alternative metric, tolerance and scoring rule.
6. **Incumbent at its best.** The incumbent arm is what the reader uses (their tokenizer, their solver, their tuning), not the easiest version for us to analyze. Where exact analysis needs a simplified incumbent, the realistic incumbent is still run at stage 1, even if only approximate measurements are possible for it.

## 6. Rigor without hedging

Hedging and rigor are different things. Rigor is exact conditions, correct numbers and valid inference. Hedging is doubt added to a claim that the evidence already supports. Reviewers, including Claude and GPT, systematically over-supply hedges: a qualifier is never wrong, and the cost of a paper nobody reads is invisible to them. The author owns that cost.

**Writing rules**

- **Lead with the revelation, and never dilute it.**
  - The first two sentences of the abstract and the first paragraph of the introduction say what the reader believes and what the result shows instead, with the number.
  - The evidence that makes the revelation hard to dismiss belongs in the abstract and the main results, not in a paragraph of a later section. That evidence is usually the incumbent's most natural fix, measured and failing.
  - A draft that buries the revelation is not ready for review.
- **Name the direction the reader should move.** A result that supports Niva's paradigm can be read as licence for a small tweak to the incumbent. Name that tweak, measure it, and say where it lands. Then say in plain words which way the architecture should change.
- **Conditions are part of the claim, not qualifiers.** "At 0.1 of the attractor spread on Kolmogorov flow, X lasts 24 frames and Y one" is precise. "X may, under some conditions, last longer than Y" is hedged. Write the first kind.
- **Scope lives in one place.** The Setup section states the conditions once. Each claim carries at most one qualifier, where it is made. The Limitations section holds only limits that would change a reader's decision.
- **The abstract and introduction carry claims, numbers and conditions.** Process narrative (freezes, amendments, review history) gets at most one sentence there. There is no "what we do not claim" section in the introduction.
- **Banned in abstract, introduction and conclusion** unless a number follows: "may", "might", "suggests", "it is worth noting", "to be clear", "that said", "empirical summary rather than".
- **Negative results that bound the claim are stated as boundaries**, in the positive voice: "the ceiling binds below 0.1σ and not above 0.3σ", not "we could not show that the ceiling binds in general".

**Review discipline**

- **Two external reviews per paper, at fixed points:** one on the design, before the stage-3 freeze, and one on the draft, before release. Further rounds happen only for correctness defects.
- Ask reviewers targeted questions: "What would make a practitioner at [lab] ignore this?", "What is the strongest incumbent we left out?" and "Which claim is false as worded?" Do not ask only "What is wrong with this?".
- **Classify every comment and record the disposition in a table.**
  - **A. Correctness** (a wrong statement, a wrong number, an invalid inference): always fix.
  - **B. Execution safety** (leakage, pre-registration order, interval validity): fix.
  - **C. Scope or wording** (add a qualifier, narrow a claim): accept only if the claim as written is false or would mislead a typical reader. Otherwise decline, with one line of reason.
  - **D. More experiments:** accept only if the result could change the headline. Otherwise it becomes future work.
- **The factual audit before release is a separate pass.** An independent agent checks claims against the numbers and flags anything false as worded. It does not propose new qualifiers.

## 7. Roles

| Who | Does |
|---|---|
| **Todd** | Approves the headline contract. Decides every gate (go, pivot or stop), the publication decision and the venue. |
| **Claude** | Drafts the contract, the kill-test specification and the work orders. Keeps the ledger. Writes gate summaries and says plainly whether it would go, pivot or stop. Drafts the paper and dispositions reviews. |
| **Claude Code** | Executes the work orders, runs the Spec Integrity Gate before executing, maintains the NUMBERS file and the checker, and reports ledger-relevant results the day they appear. |
| **External models** | Review at the two fixed points only, answering the targeted questions. |

## 8. Release checklist

- [ ] The headline contract is met at the reader's operating point, with a Niva arm and the strongest incumbent.
- [ ] The so-what test passes on the abstract alone.
- [ ] The reconsider test passes. The revelation leads the abstract and the introduction, and the incumbent's most natural fix is measured in the main results.
- [ ] The ledger is final, and the headline value is above the publish threshold.
- [ ] Every number traces to the NUMBERS file, and the checker reports zero mismatches.
- [ ] The independent factual audit is closed.
- [ ] The headline is robust to the obvious alternative conventions.
- [ ] Limitations are only those that change a reader's decision.
- [ ] There is no AI attribution anywhere: paper, repository, commits.
- [ ] Figures are greyscale-safe, with every distinction carried by a second cue.
- [ ] The venue matches the result's strength: website note, preprint or conference.

## 9. The pattern this guideline is written against

**Lagging-thermocouple paper (September 2026).**
- The work order's load set was found during implementation to show little recoverable capacity.
- The ruling that followed was that a Niva paper must tackle a large business problem and show breakthrough gains, not a few percent of capacity.
- A stage-1 kill test measuring recoverable capacity on common load sets would have surfaced this before the work order was written.

**"You Can't Train Past Your Vocabulary" (September 2026).**
- It began as "how much horizon does a bit buy". The pre-registered exchange-law test failed, so the headline moved to an exact ceiling on token forecasters.
- Realistic vocabulary sizes and physical systems were added after the draft existed. At the reader's operating point and the paper's primary tolerance, the ceiling does not bind.
- At a tighter tolerance it does bind, but that result rests on independent-patch codebooks that readers do not use, and on excluding the first frame from scoring.
- The paper has no Niva arm.
- A one-day kill test at the start (a learned tokenizer at a physics-grade tolerance, against a continuous forecaster from the same tokens) would have shown which of these papers existed.

The common failure: **the thesis was tested last at the point where it mattered first.** The ladder in section 3 reverses that order.

**"Adapt the Physics, Not the Weights" (September 2026): a writing failure, not a testing one.**
- Draft v0 led with numbers and buried its sharpest result in one paragraph, on the screening panel only. That result: a network handed the true physical parameter still failed to extrapolate, reaching 69% of the oracle against the hybrid's 98%.
- A network given the physical parameter is exactly the tweak a world-model researcher would reach for. With that result buried, the paper read as licence to add a little physics to a learned model, not as a case for physics as the backbone.
- Todd caught it on first read. The fix: promote the arm to a confirmed main result, and name the direction of the architecture change.
- The general failure: **the revelation was hidden, diluted or hedged.** The writing rules in section 6 and the reconsider test in section 1 exist to stop it.

## 10. When a paper stops: harvest the findings

Stopping a paper stops publication, not learning. A study that fails the publication rule can still show where Niva can improve, characterize a limitation nobody had measured, or show where a thesis holds and where it does not. Within a day of any stop, Claude writes a findings harvest in the vault (template below). Each result goes into one of four classes.

1. **Opportunity for Niva.** Either a limitation of the incumbent that Niva can exploit, or a limitation of Niva's own approach that Niva can remove while keeping its architecture invariants. Each becomes an engineering item or a candidate headline contract.
2. **Newly characterized limitation.** A limit of Niva's approach or the incumbent's that had not been measured, or whose size is now known. Record the size and the conditions. These sharpen positioning and keep future claims inside what is true.
3. **Boundary knowledge.** Where a thesis holds and where it fails. This stops a failed line from being re-run, and tells sales and fundraising which claims are safe to make.
4. **Reusable instrument.** A method, check or piece of code that applies beyond the stopped paper.

Each entry states:
- the finding, with numbers and conditions;
- where the data live;
- what it changes: a decision, a claim, a design or a next hypothesis.

A finding that suggests a new paper enters stage 0 with its own headline contract; it does not revive the stopped paper. The harvest is internal. Publishing any part of it goes through the full rule in section 1.

## Templates

**Headline contract**
```
Paper:
Headline sentence (abstract form, with the number):
Revelation (what the reader believes now / what the result shows instead):
The incumbent's most natural fix, and the arm that measures it:
Reader (lab or community) and what they will do differently:
Reader's operating point (model, tokenizer or solver, scale, data, accuracy need):
Strongest incumbent, and how it is tuned:
Null model:
Niva arm:
Publish threshold (reader's units):
Kill threshold (the result that ends the paper):
Pre-mortem, top 3 objections, and the stage-1 or stage-2 experiment for each:
Venue and date:
Todd go / no-go:
```

**Kill test (stage 1)**
```
Question it answers:
Operating point:
Arms: incumbent / Niva / null
Panel and budget (at most 1 day, about 10 GPU-hours):
Result that kills the paper:
Result that passes (at least 1.5 to 2 times the publish threshold):
Convention checks included:
```

**Claim ledger**
```
| Date | Headline (as it would read) | Effect at operating point | Breadth | Headline value | Change type (precision / scope) | Reason (data / review / decision) | Trigger hit? |
```

**Gate summary (Claude to Todd)**
```
Stage and gate:
Headline value now, against the threshold:
What changed since the last gate:
Largest remaining risk to the so-what test:
Claude would: go / pivot / stop, because ...
```

**Review disposition**
```
| # | Comment | Class (A/B/C/D) | Disposition (fix / decline / future work) | One-line reason |
```

**Findings harvest**
```
Stopped paper, date and gate:
Why it stopped (one line, with the number):
| # | Finding (numbers and conditions) | Class (opportunity / limitation / boundary / instrument) | Where the data live | What it changes |
Candidate headline contracts seeded (to stage 0):
```

