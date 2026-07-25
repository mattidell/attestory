# Track 0 Repair Charter — Participant-Cost Completeness

Status: **current prompt prepared 2026-07-24.** The Track 0 measurement review
returned `NOT READY` on one blocking finding. This repair is the current role
under the owner-approved milestone sequence.

## Context Capsule

- **Source ref:** `track/presentation-economy-t0-measurement-substrate`;
  resolve and record its commit when this prompt is used to launch the role.
- **Exact object:** the Track 0 implementation under
  `tools/presentation_economy/**`, `tests/test_presentation_economy.py`, and
  `docs/presentation-economy/**`, plus the blocking Measurement 4 finding in
  `docs/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`.
  Foreman/clerk continuity records and process-only commits are outside the
  implementation object.
- **Role:** one repair Builder, Medium tier / medium effort.
- **Scope:** repair only the participating-role and per-measure cost-honesty
  blocker. A comparison must derive its required participant roles from the
  frozen workload's declared `role_boundaries`; every selected observation
  must represent every declared role for each compared measure with either an
  explicit value (including an honest zero) or an explicit unknown. An absent
  declared role makes that measure `insufficient-evidence` and names the role;
  it must never yield `economically-promising`.
- **Evidence-rung ceiling:** focused production repair of the already-approved
  Track 0 contract. Do not redesign the data versions, add a published schema,
  implement the presentation harness, address non-blocking advisories, or
  begin Track 1.
- **Stop conditions:** stop before writing if the source ref cannot be
  resolved, does not contain this charter and the review record, or the
  blocking behavior cannot be reproduced. Stop if the repair would require a
  new/changed ADR, a data-version change, a file outside the allowed paths,
  personal or machine-specific data, an estimate for missing cost, or a change
  to a review measurement that already passed. Report the mismatch rather
  than expanding scope.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/INDEX.md`; the complete Track 0 review record; the milestone plan's
  Contracts, Quality-adjusted economy, Fixtures, Verification, Data safety,
  Track 0 gate, and Track 0 sections; the original Track 0 builder charter;
  `docs/presentation-economy/README.md`; the frozen workload and valid paired
  observations; the comparison/validation implementation; and
  `tests/test_presentation_economy.py`.

Before editing, echo the understood scope, evidence-rung ceiling, and stop
conditions. Reproduce the blocking omission attack before repairing it.

## Required repair

1. Determine the complete required role set from the frozen workload's
   `role_boundaries`, not from whichever participant objects remain in the
   selected observations.
2. For every compared measure and every selected baseline/treatment
   observation, require each declared role to have a measure-shaped
   participant entry:
   - an integer value, including explicit zero, participates in the total;
   - null with its required missing reason makes only that measure
     `insufficient-evidence`; and
   - an absent declared role makes only that measure
     `insufficient-evidence`, with a deterministic reason naming the missing
     role and observation.
3. Preserve raw observations and independently complete measures. Do not
   suppress valid raw evidence or turn one incomplete measure into a blanket
   comparison failure.
4. Update the paired valid example so every workload-declared role is explicit
   in both arms. A role that does no work in an arm is represented by honest
   zeros, not omission.
5. Add focused coverage reproducing the exact harness-omission attack. It must
   prove that removing a workload-declared role cannot produce
   `economically-promising`, even when quality still passes and all remaining
   participant costs are complete.
6. Add a committed invalid comparison/example for the same omission and
   document the completeness rule in
   `docs/presentation-economy/README.md`.

Do not estimate the missing role cost. Do not change the quality floor, cost
direction, evidence labels, historical baseline, orchestration/cache contract,
or any measurement the independent review passed.

## Allowed files

The repair Builder may add or edit only:

- `tools/presentation_economy/**`
- `tests/test_presentation_economy.py`
- `docs/presentation-economy/**`

The review record, charters, milestone plan, phase state, roadmap, handoff,
governance, ADRs, harness, and all other files remain foreman-owned or
out-of-scope.

## Required verification

Run:

```sh
.venv/bin/python3 -m unittest tests.test_presentation_economy
.venv/bin/python3 -m tools.presentation_economy validate \
  --dataset docs/presentation-economy/datasets/presentation-exploratory-baseline.v1.json
.venv/bin/python3 -m tools.presentation_economy compare \
  --workload docs/presentation-economy/workloads/presentation-review.v1.json \
  --observations docs/presentation-economy/examples/valid-observations.v1.json \
  --baseline manual --treatment harness-assisted
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
.venv/bin/python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

The focused suite must include the exact omitted-harness mutation and assert an
`insufficient-evidence` result with a deterministic missing-role reason. Before
handoff, inspect the fixture diff and confirm all committed data remains
manufactured and repository-relative.

## Handoff

Commit the repair as the Track 0 repair unit and report:

- the reproduced pre-fix behavior;
- the post-fix verdict and reason for the same attack;
- the exact role-completeness rule implemented;
- focused and full verification results; and
- any stop finding.

Do not review the repair, spawn a sub-agent, push, open a PR, merge, or begin
Track 1.
