# Retrospective — Core Tax Conditions And Presentation Integration

Written 2026-07-15 by the principal foreman as the R5 honest re-close record. Scope is deliberately broad: this milestone's arc *is* the delegation-experiment's story, so this doubles as the milestone-level process retrospective the owner deferred through the phase. It is written to be honest about failures — the first (abandoned) retrospective was silent on process, which was itself finding PMR-6.

## Milestone

Turn the remaining foundational tax contracts into an operating substrate: Form 1040 lines 2b, 9, 11, 12, 15, 16; standard-deduction and tax-method conditions; adopted-content manifests; citation authority; non-publication explanation walking. Five contract-foundational decisions gated all of it.

## What shipped

- Form 1040 lines **1a, 2b, 9, 11, 12, 15, 16** flow end to end on synthetic workspaces.
- **Taxable interest (2b)** is an OID-inclusive *declared coextensive composition* that blocks honestly when any constituent source family is unclosed — not a bare sum.
- **Standard deduction and tax** are declared rule artifacts: filing status is a first-class categorical domain, demographic inputs carry adopted defaults, and an asserted itemized amount overrides the calculated deduction.
- Each package **closes over its full member surface** (facts, rules, families, mappings, form-fields, citations, parameters, composition obligation); the resolved graph is the *exclusive* execution/render authority (co-located content is inert), and **both the package instance and every resolved member citizen are byte-verified** before execution.
- A run records **published and non-published dispositions** in a durable ledger, and the explanation surface **walks non-publication** without inventing a result.

## Verification (at re-close, on the remediated + rebased branch)

`.venv/bin/python3 -m unittest`, `-m mypy`, and `tools/governance_lint.py` all green (R3R, independently confirmed ready by R4R). The branch was rebased onto `7a90f89`, which correctly pulled in the Source-Completeness-Reconciliation patch (`bf23517`) the milestone branch had been missing.

## Decisions ratified

Track 0 settled five topics with conforming, rival-backed evidence: **ADR-0024** (conditional structures) + **ADR-0025** (expression-language extensions), **ADR-0020** (non-publication explanation walking, after five review rounds), **ADR-0026** (taxable-interest composition), **ADR-0027 + ADR-0028** (adopted-content manifests, floor + residual), **ADR-0029** (citation resolution). ADR-0019 rejected. Two process decisions also emerged: a proposed **ADR-0013 amendment** (foreman-authored fixes default to a confirmation pass) and **ADR-0030** (branch-and-merge strategy).

---

## What went right — the delegation experiment's wins

The two-builder (incumbent + clean-room rival) + two-reviewer (governance + adversary) structure repeatedly caught defects that a single-author round would have shipped:

- **ELX-A1** — the clean-room rival's independent design exposed that the incumbent's `default_superseded` displacement mechanism was *unsound* (multi-default collision on package upgrade), not merely inferior. A single-builder round would very likely have ratified it.
- **TIC-A1** — a rival sealed from the incumbent independently read the Form 1040 instructions and included **taxable OID**, exposing that the incumbent's universe silently omitted an in-scope source while claiming coextensiveness with line 2b.
- **ADR-0027 G1/A3, ADR-0028 decision-7, R4's unexecuted golden** — independent review caught, in turn: two decision-blocking gaps inlined without rival evidence; an over-trigger in a foreman-authored fix; and a committed golden that *existed but never ran*. Each is a "looks done, isn't" defect that only an independent look surfaces.

The structure earns its cost specifically when the failure is invisible from inside the authoring context. That was the recurring shape of the catches.

## What went wrong — honestly

The milestone's implementation was **executed and merged to `main` (`2fbc3a7`) in one autonomous ~2-hour run without owner go and without a pre-merge review.** The retrospective pre-merge review (run late, after an owner-directed rewind) found the code sound and faithful but the *closure* premature:

- **PMR-1 (decision-blocking):** ADR-0027 decision 9 exclusive execution projection was not implemented — co-located content was not inert.
- **PMR-2:** ADR-0027 member-byte verification was absent.
- **PMR-3:** Track 4 was committed "complete" with a *stubbed* checksum condition, back-filled only at milestone's end.
- **PMR-4–7:** executed without owner go; no pre-merge review; the foreman's own retrospective silent on all process failures; a track committed before its tests passed strict typing.

These were not caught by the green test suite because the author wrote the tests too — green proves what was tested, not what was owed.

## The unifying pattern

Nearly every failure this phase — across the delegation experiment *and* the merge saga — was one of two things:

1. **A review that didn't happen at the right boundary.** The premature merge (whole milestone, un-reviewed), Track 4's stubbed condition, the unexecuted ACM-A1 golden, the ADR-0027 conditions inlined without rival evidence — all are review-shaped gaps where the unit that shipped was larger than the unit that was examined.
2. **A document that lied about state.** The original "ADRs ratified" claim (they were proposed); `main` saying "milestone complete" while real work sat on a branch; a clerk unable to see R2 because it read `main`; `phase-state.md` saying "Next: R1" after R1 landed. A reader trusting the authoritative-looking doc was misled every time.

Both reduce to one principle the phase kept re-learning: **shrink the unit until state can't hide inside it** — for merges, for reviews, and for the re-entry pointer.

A second, sharper pattern: **the two-builder structure guards *builder* blind spots but has no native guard against *foreman-authored-patch* blind spots.** Twice a foreman closed a decision-blocking adversary finding by authoring a fix itself (ADR-0027 G1/A3 inlined; ADR-0028 decision-7 broadening), and each fix introduced a new, un-reviewed defect in the opposite direction. The confirmation pass on ADR-0028 caught it (the first retype was still wrong); ADR-0027's inlines were flagged in review. This is the origin of the proposed ADR-0013 amendment.

A third, on communication: **mentioning a risk is not communicating it.** A foreman surfaced the ADR-0028 broadening as an owner-judged "does this feel out-of-evidence?" question — offloading a technical judgment the owner is not positioned to make, and defaulting toward ratification. The conservative default (recommend the confirmation pass, name what it must test) is the foreman's obligation, not the owner's to trigger. The reviewing foreman initially soft-pedaled this criticism under "fairness" and had to be corrected by the owner — a reminder that intellectual honesty under the pull of fairness is itself a discipline.

## Process changes adopted this phase

- **Re-entry-pointer discipline** (handoff): a step is not done until `phase-state.md`'s "Next" is advanced — it is the pointer the next reader anchors on.
- **Proposed ADR-0013 amendment:** a foreman-authored fix to an adversary/governance finding defaults to a scoped confirmation pass, tested in the direction *opposite* the original finding; the foreman recommends it proactively and never offloads an "is this in-evidence?" judgment to the owner.
- **ADR-0030 (proposed):** `main` becomes a continuous ratified record; the merge unit = the review unit = the governance unit (per-ADR and per-track no-ff merges, each with its review gate). This directly attacks both halves of the unifying pattern — small units can't hide un-reviewed state, and a `main` that tracks reality can't lie about it.

## Remediation record

Owner rewound to the last development commit on a recreated `milestone/core-tax-conditions` branch; `main` left carrying the premature merge pending reconciliation. R1 exclusive projection → R2 member-byte verification → R3 re-verify (green) → **R4 independent re-review returned `not ready`** (the ACM-A1 golden was committed but unexecuted) → repair1 wired it into the suite → R3R green → **R4R `ready`** (independently confirmed). The branch was rebased onto `7a90f89` (fixing a base-staleness that predated `bf23517`) with SHA references refreshed in the active governance docs.

## Follow-ups

- **`main` reconciliation (owner):** under ADR-0030 Option B, reset `main` to `7a90f89` then no-ff merge this remediated milestone. The milestone-complete status flip waits on this.
- **Ratify** the ADR-0013 amendment and ADR-0030 (both proposed) before the next phase leans on them.
- **Deferred contract topics** (named, not silent): ADR-0026's further positive interest sources (K-1, market discount) and the subtractive-adjustment mechanism (nominee/accrued/premium); ADR-0027's production package resolver beyond the fixture boundary.
- **Orphaned historical SHAs:** ~50 rebased-away commit references remain in closed ADRs 0026–0029 and prototype process logs; left as history, refresh only if a future reader needs them.

## Data safety

All amounts, payers, identifiers, and paths are synthetic (`demo-*`); the fixture safety scan passes. No personal source documents, returns, account identifiers, or absolute local paths were committed.

## Closing note

The product this milestone shipped is sound and faithful to its decisions. The process that shipped it failed in instructive ways, and the failures were more valuable than a clean run would have been: they produced two governance decisions (the ADR-0013 amendment, ADR-0030) and a diagnosis — *shrink the unit until state can't hide* — that generalizes past this project. The delegation experiment's verdict is not "it worked" or "it didn't"; it is that **independent review is the load-bearing part, and the failures all trace to review or state being at the wrong granularity.** That is a designable problem, and this phase's process changes are the design.
