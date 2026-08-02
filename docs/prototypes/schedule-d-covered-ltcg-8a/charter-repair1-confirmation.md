# Repair 1 Confirmation Charter — B2 Boundary and Exact P3 Pin Contract

Audience: Reviewer

Date: 2026-08-01. Track 0 of Covered Long-Term Gains, Schedule D Line 8a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/schedule-d-covered-ltcg-8a/it2` branch and verify its commit at
  launch.
- **Exact object:** repair commit `e6747fd`, measured only against
  `charter-repair1.md`, findings CA-02/CA-04 in `round-1-triage.md`, and the
  retained P1/P2/P3 boundaries of the selected design at
  `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd`.
- **Role:** author-independent focused Confirmation Reviewer, High capability /
  high effort.
- **Scope and evidence-rung ceiling:** confirm CA-02 and CA-04 and check that
  their repair does not regress the already-settled P1/P2/P3 boundaries. Rung
  1 static paper evidence only.
- **Stop conditions:** any need to repair the design, synthesize the contract,
  draft an ADR, inspect another agent's thread, run validator/evaluator
  probes, edit schemas/content/tests/production, interpret governance, widen
  into CA-05/CA-06, use real data, or broaden beyond the named findings and
  regression boundaries.
- **Full reads before acting:** this charter; `charter-repair1.md`;
  `round-1-triage.md`; `repair1/design.md`; `repair1/examination.md`;
  `it2/design.md`; `it2/examination.md`; the topic `plan.md`;
  `reviews/contract-adversary.md` (CA-02 and CA-04 specifically); ADR-0036;
  ADR-0050 (Decisions 1, 5, 6, 7, 8); the milestone plan's Completeness
  Boundary and Contracts sections; and the linked official 2025 Schedule D
  and Form 1099-B instructions.

## Assignment

Attempt to falsify the repair. Do not improve or complete it. A claimed rule
is not sufficient paper evidence unless the repaired cases make its facts,
authority, pins, state transitions, and dispositions recoverable.

### CA-02 confirmation

Confirm whether the repair:

1. states the box-2a boundary change (`B2` must be closed, not closed-empty)
   as its own standalone numbered successor sentence (P2-S5A), not only as
   narrative inside a worked example;
2. preserves closed-empty contributing authoritative zero, unchanged from the
   selected design;
3. states that closed-nonempty `B2` contributes its current subtotal exactly
   once, through Schedule D line 13, only when the Schedule-D producer of `P`
   is current;
4. does not expand the transaction source class, edit ADR-0050, or create a
   second capital-gain path into line 9 or QDCG; and
5. demonstrates both the closed-empty (shared case 7) and closed-nonempty
   (shared case 6) states with exact synthetic facts and downstream
   dispositions, including the exact once-only line-13/line-9 arithmetic.

### CA-04 confirmation

Confirm directly against ADR-0050 Decision 7 and Decision 8 whether the
repair:

1. gives an exact, falsifiable pin contract for `TAX16` under each of the two
   `P` producer signatures (`P-direct`, `P-schedule-d`), not an "as
   applicable" or "same pins apply" assertion;
2. shows that no accepted ADR-0050 Decision 7 pin moves, and that no new
   direct line-16 pin is introduced beyond the substitution
   `selected_line7a -> P`;
3. shows that upstream authority (C1-C4, box-2a family/closure under the
   direct route; `LD16`/`ATT-D`/`B1`-`B9` under the Schedule-D route) remains
   transitive through `P` and is never duplicated as a direct `TAX16` pin;
4. correctly resolves the four-row Decision 7 table for both `P>0` and
   closure-backed `P=0` under `P-direct`, and shows the Schedule-D route adds
   none of those four rows' declaration/conclusion pins;
5. correctly handles the nonnumeric `P` states (`blocked`, `guard_inapplicable`)
   before `COMMON16` is assembled, without silently defaulting to a numeric
   read; and
6. demonstrates forward (direct-to-Schedule-D) and reverse
   (Schedule-D-to-direct) correction with exact current/displaced pins, and
   confirms no displaced finding revives.

Independently assess whether the repair's claim — that no first-class route
tag on `P` is required because the producer signature is recoverable from
direct pin lineage — actually holds for every repaired case, or whether some
case requires a tag or a Rung-2 substrate answer the repair did not name.

### Regression boundary

Confirm only that the repair leaves intact:

- P1's independent anchor-keyed transaction identity, correction, and closure
  behavior (untouched by this repair; confirm the repair did not silently
  alter it);
- the nine-part direct-multi-read completeness authorities `B1`-`B9` other
  than the `B2` wording change;
- exactly-one-producer arithmetic for `P` (no double count, no reach-around);
- honest non-publication when completeness authority is missing or violated;
  and
- the P3-S6 QDCG state partition's numeric branch condition (`Q>0 or P>0`
  selects QDCG; both closure-backed zero selects ordinary), unchanged in
  shape.

Do not reopen the owner's topology selection or reassess unrelated `it2`
material, CA-05, or CA-06.

## Verdict and output

Create exactly:

- `docs/prototypes/schedule-d-covered-ltcg-8a/reviews/repair1-confirmation.md`

Report:

1. `CA-02: CONFIRMED` or `NOT CONFIRMED`;
2. `CA-04: CONFIRMED` or `NOT CONFIRMED`;
3. `REGRESSION BOUNDARY: INTACT` or `REGRESSED`;
4. numbered, falsifiable findings with exact file/section evidence and the
   unmet charter clause;
5. one overall verdict: `READY` only if both findings are confirmed and the
   regression boundary is intact; otherwise `NOT READY`; and
6. whether any uncertainty remains that Rung 1 cannot distinguish. Do not
   climb a rung.

For every required repaired case, state whether the artifact itself contains
enough exact facts, pins, current/displaced states, and dispositions to
support the claim. Do not treat `repair1/examination.md`'s self-reported
status as evidence.

Commit only the review locally and stop. Do not push, merge, repair,
synthesize the contract, draft an ADR, begin production, or advance the
pointer. Return the commit SHA and the three status lines plus overall
verdict.

## Data safety

All evidence stays synthetic and publishable. No personal values,
identifiers, dispositions, refusal reasons, workspace locations, documents,
screenshots, or private artifacts may enter the review.
