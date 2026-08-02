# Round 1 Triage and Owner Disposition

Date: 2026-08-01

This is the foreman's Gate-5 record after the two clean-room designs and two
independent committee reviews. It records where the reviews agree, one
substantive dissent between them, and the disposition the topic needs from
the owner before contract synthesis.

## Owner disposition

The owner confirmed on 2026-08-01: (1) the rival topology (independent-family
P1, direct-multi-read P2, selected-preferential-base P3) is selected; the
incumbent is not carried forward. (2) CA-02/P2-S5 is adopted as the
completeness-boundary successor: `B2` (box-2a) must be closed, not
closed-empty, for the boundary to be satisfied, with a closed-nonempty
amount contributing once via Schedule D line 13. (3) The CA-04 repair is
authorized, spending the plan's single fixed repair pass. Repair charter:
`charter-repair1.md`, assigned to the rival Builder for design continuity.

## Review agreement

Both reviews independently converge on:

- **P1 (transaction identity):** both designs are recoverable and correction-
  safe at Rung 1. The rival's anchor-keyed independent family is the cleaner
  shape (decouples transaction closure from statement closure); the
  incumbent's nested member identity also works structurally.
- **Incumbent P1's admitted source class is too broad.** The contract/
  adversary review names this explicitly (CA-01: the incumbent's committed
  `member_predicate` omits covered-security, box-1f/1g, Ordinary, QOF,
  taxpayer-adjustment, collectibles, and special-rate exclusions, and derives
  gain-only from an amount comparison rather than a contributed assertion).
  The expressiveness review's own case-1/case-11 recovery table reproduces
  the same narrower predicate without flagging the gap — see "Dissent" below
  for why this is not full agreement.
- **Incumbent P3 drops the box-2a gain in the both-gain case (shared case
  6).** Both reviews independently reconstruct the same defect: the
  incumbent's line-7a match chooses Schedule-D precedence and never adds the
  box-2a amount anywhere, silently under-reporting real taxable gain. This is
  corroborating evidence from two independent reviewers using different
  charters, which strengthens the finding.
- **Rival P2-S5 (the box-2a-nonzero boundary successor) is the only sound
  resolution of the both-gain case.** Both reviews reconstruct the rival's
  Schedule D line 13 inclusion and confirm it preserves both gains exactly
  once. Neither review treats this as a free interpretation of the plan —
  the contract/adversary review is explicit that it is a real successor to
  the milestone's stated "box-2a closed empty" completeness wording and
  needs owner adoption, not silent acceptance.
- **Rival P2 (direct multi-read completeness)** is sufficient and is the
  stronger topology: exact per-component failure naming, no synthesizing
  conclusion hop, no ADR-0050 edit.

## Dissent: rival P3's pin-selection question (CA-04)

The contract/adversary review classifies **CA-04 as decision-blocking**: the
rival's shared `selected-preferential-base` symbol `P` is described as
route-neutral, but ADR-0050's route-specific direct pins (the checked
Schedule-D-required conclusion, read whenever the direct producer is
current) have no stated home once `P` — not the direct publication — is what
line 16 consumes. The review's own worked example (rival case 6, where C1 is
`"no"` and the checked conclusion is `"yes"`) shows the pin set must differ
by which producer is current, and the design does not say how a single
numeric/route-neutral `P` carries that.

The expressiveness review reaches **READY** for rival P3 and does not
identify this gap. Its case-by-case recovery table for P3 stops at "exactly
one route publishes `P`; no double-counting" — a true statement about
arithmetic exclusivity, but not an answer to CA-04's narrower question of
where the *route-specific pin set* attaches once `P` is the consumed symbol.
The expressiveness charter measures recoverability and case-by-case
reconstruction, not exhaustive pin-contract sufficiency, so this is not a
process-conformance failure by that reviewer — it is a question the two
charters were not both aimed at, and the gap between "arithmetic is right"
and "every downstream pin is accounted for" is exactly the kind of thing a
single READY verdict can miss. Per `PROJECT_PLANNING.md`, dissent is
recorded, not resolved by wordsmithing.

**This dissent is not settled here.** CA-04 remains an open decision-blocking
finding on the currently-favored (rival) topology until either the owner
finds the expressiveness review's implicit answer sufficient, or a bounded
repair supplies the exact pin sentence CA-04 asks for.

## Finding classification

| Id | Finding | Gate-5 class | Disposition |
| --- | --- | --- | --- |
| CA-01 | Incumbent P1 admits a broader source class than the charter's Supported Source Class permits. | `decision-blocking`, incumbent P1 | Moot if the rival topology is selected; incumbent is not carried forward. |
| CA-02 | Box-2a closed-nonempty interaction is an unresolved scope contract in both designs; rival's P2-S5 is the sound resolution but changes the plan's stated completeness wording. | `decision-blocking` until explicitly adopted | **Owner disposition needed:** adopt P2-S5 (box-2a family must be closed, not closed-empty; closed-nonempty contributes once via Schedule D line 13) as the milestone's completeness-boundary successor. |
| CA-03 | Incumbent P3 omits a required QDCG `Q` input and a full correction chain. | `decision-blocking`, incumbent P3 | Moot if the rival topology is selected. |
| CA-04 | Rival P3's route-neutral `P` symbol has no stated home for ADR-0050's route-specific direct pins. | `decision-blocking`, rival P3, **unresolved by the second review** | **Owner disposition needed:** authorize a bounded repair requiring the rival Builder to supply the exact pin sentence, or accept the expressiveness review's implicit sufficiency and record the dissent as accepted risk. |
| CA-05 | `attachment-rule.v2`'s requirement block is threshold-only; Schedule D's disposition is categorical. Both designs need it; only the incumbent names it precisely. | `separate-decision` prerequisite | Not blocking topology selection. A `attachment-rule.v3` successor is a production condition regardless of which topology is selected. |
| CA-06 | Rival's exactly-one-producer enforcement for `P` needs a generic representation decision (two mutually exclusive rules vs. a selected-binding citizen). | `separate-decision` prerequisite | Not blocking topology selection. Appropriate Rung-2 question only after CA-04 is repaired. |
| CA-07 | Incumbent's synthesized-conclusion binding locus is unselected. | `separate-decision` prerequisite | Moot if the rival topology is selected. |
| EXP (case 1/11 predicate) | Expressiveness review's per-case recovery reproduces the incumbent's narrow predicate without flagging it as a source-class gap. | process-observation, non-blocking | No action; CA-01 already covers this defect on the record. Noted so a fresh reader does not mistake the expressiveness review's silence for disagreement with CA-01. |

## Recommendation

Both reviews converge on the rival topology (independent-family P1,
direct-multi-read P2, selected-preferential-base P3) as the stronger and
more nearly sufficient basis. The incumbent is not recommended to carry
forward — its P1, P2, and P3 defects are each independently corroborated by
at least one review, and the box-2a data-loss defect (case 6) is
corroborated by both.

The rival is not yet adoptable as committed. Two items need owner
disposition before contract synthesis:

1. **CA-02 / P2-S5 adoption** — explicit acceptance that the milestone's
   completeness boundary requires box-2a *closed* (not closed-empty), with
   a nonzero closed box-2a amount contributing once via Schedule D line 13.
2. **CA-04 repair** — the rival Builder supplies an exact successor pin
   sentence for how ADR-0050's route-specific direct pins attach when `P` is
   consumed at line 16, resolving the dissent above.

Recommended path: one bounded, owner-directed repair pass (the plan's single
authorized pass) assigned to the rival Builder for design continuity,
scoped to CA-04 only — plus a repair-scope requirement that the repaired
design state P2-S5 as an explicit, adopted successor sentence rather than an
implicit resolution. No new proposition, no Rung-2 probe, no production
code. CA-05/CA-06/CA-07 stay out of scope as separate-decision prerequisites
routed to production conditions.

This spends the plan's single fixed repair pass (`PROJECT_PLANNING.md` Gate
4). A second substantive defect after this repair returns to the owner
rather than being absorbed.
