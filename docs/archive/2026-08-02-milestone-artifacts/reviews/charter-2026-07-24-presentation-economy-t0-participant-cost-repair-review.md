# Track 0 Delta Review Charter — Participant-Cost Completeness

Status: **completed 2026-07-24; `READY`.** The focused repair Builder completed
the accepted Track 0 blocker and the independent delta review cleared it. Track
1 Builder is the current role.

## Context Capsule

- **Source ref:** `track/presentation-economy-t0-measurement-substrate`;
  resolve and record its commit when this prompt is used to launch the role.
- **Exact object:** the participant-cost repair at the resolved source commit,
  principally `tools/presentation_economy/comparison.py`, its focused tests,
  paired examples, and README contract text. Reconcile the repair against the
  pre-repair implementation commit `2f5fcc1`'s Track 0 artifact object and the
  blocking review at
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`.
  Foreman/clerk continuity records and process-only commits are outside the
  artifact-quality object.
- **Role:** one fresh independent delta Reviewer, High tier / high effort,
  using the measurement-integrity lens.
- **Scope:** verify that the repair closes the omitted-participant cost-shift
  finding, derives required roles from the frozen workload's `role_boundaries`,
  preserves explicit zeros and explicit unknowns, blocks only the affected
  measure, retains complete measures and raw observations, and does not regress
  the other Track 0 measurement results.
- **Evidence-rung ceiling:** independent delta review of the approved Track 0
  repair. Do not redesign the contract, implement another repair, begin the
  presentation harness, address non-blocking advisories, or generalize beyond
  UI/UX presentation work.
- **Stop conditions:** stop if the source ref cannot be resolved, the exact
  repair object or prior review is missing, the pre-fix attack cannot be
  reproduced from committed artifacts, a check requires personal or
  machine-specific data or a remote, or the conclusion would exceed the Track
  0 review gate. Report the mismatch rather than reconstructing context.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/INDEX.md`; the complete Track 0 review record and repair charter;
  the milestone plan's Contracts, Quality-adjusted economy, Fixtures,
  Verification, Data safety, Track 0 gate, and Track 0 sections; the repair
  commit and changed tests/examples/README; the frozen workload; the comparison
  implementation; and the valid/invalid comparison fixtures.

Before reviewing, echo the resolved object, scope, evidence ceiling, and stop
conditions. Review committed artifacts and rerun the evidence independently.

## Required measurements

1. Reproduce the pre-repair harness-omission mutation against the pre-repair
   implementation and confirm it could produce `economically-promising`.
2. Run the same mutation against the repair and confirm every affected
   participant-cost measure becomes `insufficient-evidence` with a deterministic
   reason naming the observation and missing declared role.
3. Confirm the required role set comes from the frozen workload's
   `role_boundaries`, so omission is detected even when the role is absent from
   both visible participant lists. Confirm an explicit zero is accepted and a
   null plus missing reason blocks only that measure.
4. Confirm complete measures and raw observations remain visible when one
   measure is incomplete, quality checks still precede cost interpretation, and
   no blended or causal conclusion appears.
5. Rerun the focused Track 0 suite, committed valid/invalid examples, and the
   full verification floor. Check the README and fixture changes against the
   executable behavior and run the envelope scan.

Blocking: the omission attack still yields an economy verdict, a declared role
can disappear without a deterministic refusal, explicit zeros are rejected,
one incomplete measure suppresses complete measures, or any previously passing
Track 0 measurement regresses.

## Output and verdict

Write the review to
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-24-presentation-economy-t0-participant-cost-repair-review.md`.
Return `READY` only if the blocker is cleared and no regression remains.
Otherwise return `NOT READY`, name the exact failed measurement and smallest
evidence-backed remediation. Do not repair the implementation, spawn a
sub-agent, push, open a PR, merge, or begin Track 1.
