# Review Charter — Expressiveness and Recoverability

Audience: Reviewer

Date: 2026-08-01. Track 0 of Covered Long-Term Gains, Schedule D Line 8a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/schedule-d-covered-ltcg-8a/it2` branch and verify its commit at
  launch.
- **Exact objects:** incumbent Builder output at
  `d4e220376cfa29785447fe8cc183355532eb168f` and clean-room rival Builder
  output at `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd` — the same two exact
  objects the contract/adversary review used. The working tree at the launch
  branch tip is one commit ahead of the rival object (a non-substantive
  grounding-citation addition); read the rival exactly as pinned, the same
  way the first review did, and note the discrepancy rather than silently
  using the newer tree.
- **Role:** Expressiveness Reviewer, Medium-High capability / medium effort.
- **Scope and evidence-rung ceiling:** recover P1-P3 case-by-case from both
  Rung-1 paper designs and judge whether paper distinguishes the topologies.
  Do not run a Rung-2 probe.
- **Stop conditions:** missing or mismatched objects; exposure to another
  review or foreman finding; need for governance interpretation, artifact
  mutation, a validator/evaluator probe, real data, or scope beyond P1-P3.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`; the
  topic `plan.md`; both Builder charters (`charter-it1.md`, `charter-it2.md`);
  both exact Builder artifact sets; the milestone plan's Supported Source
  Class, Completeness Boundary, Prototype Decision Inventory, Contracts,
  Review Gates, and Data Safety sections; ADR-0036; ADR-0050; and the
  committed expression semantics in `packages/derivation/evaluator.py`.

## Independence boundary

Do not read:

- `docs/prototypes/schedule-d-covered-ltcg-8a/reviews/contract-adversary.md`;
- the foreman's custody notes or process log;
- either Builder's thread, summary, or uncommitted work; or
- any future triage, repair, or disposition.

If another review or finding reaches the context, stop and report the
independence breach.

Read the incumbent artifacts without switching the working branch:

```sh
git show d4e220376cfa29785447fe8cc183355532eb168f:docs/prototypes/schedule-d-covered-ltcg-8a/it1/design.md
git show d4e220376cfa29785447fe8cc183355532eb168f:docs/prototypes/schedule-d-covered-ltcg-8a/it1/examination.md
```

Read the rival artifacts pinned to the exact reviewed object, not the working
tree:

```sh
git show bbecd3f3aae6777cf06e4bdbe58d91545f4faedd:docs/prototypes/schedule-d-covered-ltcg-8a/it2/design.md
git show bbecd3f3aae6777cf06e4bdbe58d91545f4faedd:docs/prototypes/schedule-d-covered-ltcg-8a/it2/examination.md
```

## Measurement

For each of the eleven shared cases, and separately for each design, recover
from the committed artifact alone:

1. the authoritative producer;
2. why Schedule D line 8a applies, blocks, or is inapplicable;
3. the exact current source set, horizon, family closure, and
   completeness-boundary state;
4. every downstream consumer through Schedule D line 8a/15/16, Form 1040
   line 7a, line 9, taxable income, and line 16;
5. what displaces the result; and
6. the exact failure or non-publication state.

Failure means a required answer is missing, inferred only from prose, differs
between equivalent cases without a contract reason, or requires a more
expensive evidence rung merely because the design is underspecified.

Additionally score, for each design and each of P1/P2/P3:

- whether a fresh reader can reconstruct the proposed successor contract
  sentences precisely enough to accept or reject them without asking the
  Builder;
- whether the mandatory negatives (cases 4, 5, 6, 7, 9, 10, 11) are concrete
  reproducible states or unresolved prose; and
- whether the design's own named "unresolved questions" are honestly scoped
  (a real paper-evidence limit) versus a case the charter required settled.

Do not credit a design for asserting a conclusion without a citable instance.
"The topology handles this" is not a measurement; a specific pinned state is.

## Output

Create exactly:

`docs/prototypes/schedule-d-covered-ltcg-8a/reviews/expressiveness.md`

The review must contain:

- review-object verification (confirm both objects match the pinned SHAs
  above, and note the working-tree/rival-object discrepancy if it applies);
- a per-case, per-design recoverability table (the eleven shared cases ×
  the six recovery questions, summarized);
- P1, P2, and P3 sufficiency judgments for each design, independent of the
  contract/adversary review's conclusions;
- whether paper distinguishes the identity, completeness, and P3
  route-binding topologies from each other;
- which unresolved questions in each design are genuine paper-evidence
  limits versus underspecification; and
- a final `READY` or `NOT READY` recommendation without enlarging scope.

Before writing, echo the exact objects, scope, Rung-1 ceiling, independence
boundary, measurements, and stop conditions.

## Completion

Run:

```sh
python3 tools/envelope_scan.py --range origin/main..bbecd3f3aae6777cf06e4bdbe58d91545f4faedd
python3 tools/envelope_scan.py --range origin/main..d4e220376cfa29785447fe8cc183355532eb168f
```

Commit only the review output and stop. Do not edit either design, phase
state, SEAT file, charter, plan, process log, ADR, schema, test, or
production file. Do not prepare a repair, reconcile dissent, review the other
reviewer, open a PR, push, merge, or advance the pointer. Return the review
commit SHA and verdict.

## Data safety

Use only the committed synthetic paper evidence. No personal values,
identifiers, dispositions, refusal reasons, workspace locations, documents,
screenshots, or private artifacts may enter the review.
