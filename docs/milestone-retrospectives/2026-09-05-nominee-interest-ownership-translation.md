# Retrospective — Nominee Interest Ownership Translation

Closed 2026-09-05. Track 0 completed at the **paper** evidence rung and returned
a **decision-ready contract proposal**. No production code, schema, ADR, or test
changed: the milestone's entire diff is documentation.

The milestone asked whether the document-and-ordinary-fact translation method
transfers from a purchase circumstance (accrued interest) to an
ownership-allocation circumstance (nominee interest). It does, with two bounded
extensions and one new decision — and the answer was reached without writing a
line of product code.

## Carry-forward lessons

- **Staged planning gates before Track 0 paid for themselves.** P1 (framing),
  P2 (tax and artifact evidence), and P3 (experiments and decomposition) each
  ran as an independent review with its findings repaired into the plan before
  the next began. Every gate found real defects: P1 forced a two-step intake
  because a bare "who and how much" cannot separate nominee ownership from a
  bond buyer's accrued-interest reimbursement; P2 found three unreconciled
  information-reporting formulations where the plan had assumed one question;
  P3 dropped a rival-prototype comparison no case could discriminate and set the
  authorized rung to paper. Each of those, discovered inside Track 0 instead,
  would have invalidated work already done.

- **A kill condition inherits discriminability from its facts, not from the
  mechanism it invokes.** `N10-PIN` proposed observing whether a payment finding
  appears on the reduction's pin set — a real and observable property. But N10's
  defining fact is that *no payment finding exists*, and committed pin
  construction cannot pin an absence. The check was vacuously true for
  conforming and non-conforming implementations alike. A test written from it
  would have passed forever while appearing to cover independent gating, which
  is worse than no test.

- **In a corpus of self-documenting artifacts, string presence is near-worthless
  evidence.** Three separate conclusions in this milestone had to be corrected
  because a grep hit a `title` or `notes` field — including one where the matched
  prose explicitly *denied* the thing being matched. A fourth error ran the other
  way: a true negative about one symbol was over-scoped to a whole category.
  Walk the structure; read the hits.

- **Bounding a limitation and disposing of it are different acts.** The Track 0
  synthesis recorded "known limitations affecting correctness: none" and then
  described one, arguing its scope until it looked like someone else's problem.
  Establishing that a limitation is inherited, and narrow, is analysis.
  Deciding what to do about it is the owner's.

- **Unresolved law forces a partial result; unresolved shape does not.** The
  three reporting formulations remain unreconciled, and it would have been easy
  to call the milestone partial on that basis. It is not: the required product
  behavior is fully specifiable as separately attributed evaluation,
  qualification, or deferral. What cannot be specified without unsupported legal
  normalization forces a partial; what merely lacks a chosen representation does
  not.

- **Paper was sufficient for an entire track.** The evidence ladder authorized
  paper and pre-authorized no spike, with an explicit rule that an "optional"
  spike may not bypass the planning gate. Track 0 never needed to climb. Three
  checkpoints, six adversarial-closure artifacts, and a contract proposal came
  out of reading committed contracts against fixed cases.

## What transferred, and what did not

| Seam | Disposition |
| --- | --- |
| Supportability (ADR-0070 Decisions 8–10) | **transfer unchanged** |
| Report association | bounded extension — representation deferred |
| Rule-owned consequences | bounded extension — **independent** gates, where ADR-0071 shares one |
| Ordinary-input mapping | bounded extension — route circumstance before capture |
| Legacy coexistence | bounded extension — no silent conversion |
| Object-valued fact + owner cardinality | **new decision** |

## Follow-ups

- **T0-F5 — deferred behind a hard production gate (owner disposition,
  2026-09-05).** When the shared Schedule B attachment is required and a nonzero
  pairing-scoped current-year adjustment is present, the Part I tie-out fails:
  line 2b subtracts `current-year-adjustment-subtotal` and no Schedule B version
  itemizes it. **No production or integration unit may be accepted as complete
  for that state until it is repaired.** Preparatory work outside that
  intersection is not prevented. Inherited, not caused by nominee interest, and
  not repaired here.
- **The contract unit remains conditional and unchartered.** Track 0's proposal
  is decision-ready; instantiating schemas, ADRs, or a producer is a separate
  unit. A successor producer of an externally bound symbol makes the
  integration-surface artifact mandatory under a fresh charter.
- **R-A versus R-B stays deferred.** No case discriminated them. *Trigger:* a
  concrete consumer involving a source-independent allocation, a report-identity
  replacement, or another materially different product behavior.
- **Owner cardinality shapes.** The required behavior is specified —
  independently correctable per-owner statements — but the shapes satisfying it
  are not discriminated by the bounded cases.
- **Attribution exposure.** Attribution is recoverable from the assertion act
  and exposed by no current reader-facing consumer. The required property is
  specified; the extension is not designed.
- **Whether N12's onward transfer falls within another § 6049 route** remains a
  preserved unknown, closable only by a primary source or an explicit owner
  decision — never by reasoning.
