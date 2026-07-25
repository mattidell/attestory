# Track 0 Review Charter — Presentation Economy Measurement Integrity

Status: **current prompt prepared 2026-07-24.** This is the current role under
the owner-approved milestone sequence.

## Context Capsule

- **Source ref:** `track/presentation-economy-t0-measurement-substrate`;
  resolve and record its commit when this prompt is used to launch the role.
- **Exact object:** the Track 0 implementation at the resolved source commit:
  `tools/presentation_economy/**`, `tests/test_presentation_economy.py`, and
  `docs/presentation-economy/**`, evaluated against the Track 0 plan and builder
  charter. Foreman/clerk continuity records and their process-only commits are
  outside the artifact-quality object.
- **Role:** one fresh independent Reviewer, High tier / high effort, using the
  measurement-integrity lens.
- **Scope:** source fidelity, strict contracts, append/supersession,
  comparability, quality-before-cost behavior, participating-role cost
  completeness, orchestration/cache telemetry honesty, deterministic output,
  and synthetic-data safety for Track 0 only.
- **Evidence-rung ceiling:** independent implementation review of the approved
  Track 0 contract. Do not redesign the contract, implement repairs, begin the
  harness, or generalize findings beyond UI/UX presentation work.
- **Stop conditions:** stop if the source ref cannot be resolved, the exact
  object is missing, the reviewer has seen builder working context, a check
  would require personal/machine-specific data or a remote, or the requested
  conclusion would exceed the Track 0 review gate. Report the mismatch rather
  than reconstructing context.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/INDEX.md`; the milestone plan's Contracts, Fixtures, Verification,
  Data safety, Presentation execution economy and review allocation, Track 0
  gate, and Track 0 sections; the Track 0 builder charter;
  `docs/prototypes/human-presentation-citation-walk/analysis/04-economy.md`;
  `analysis/06-timeline.md` in that same prototype; `AGENTS.md` Fixture Rules
  and Data Safety Rules; and the complete Track 0 implementation object.

Before reviewing, echo the resolved object, scope, evidence ceiling, and stop
conditions. Review the committed artifacts and rerun their evidence; do not use
the builder's report as proof.

## Review measurements

### 1. Historical source fidelity

Independently reconstruct the C1–C5 builder/reviewer table from
`analysis/04-economy.md`. Reconcile every tokens, tool-calls, and wall-seconds
cell against the committed baseline. Confirm C3 R2 tokens remain approximate,
its two em-dash measures remain explicitly missing, and foreman costs remain
unmeasured rather than reconstructed.

Blocking: any invented precision/value, silently dropped null, false zero,
missing provenance, or causal label attached to the historical observations.

### 2. Strict contract and correction behavior

Attack all three versions with unknown keys, wrong versions/types, negative
values, duplicate ids, dangling workload/comparison/supersession references,
invalid approximation/missing states, self-supersession, cross-workload
supersession, and silent in-place correction.

Blocking: an invalid instance passes, an old observation can be overwritten,
or a committed invalid case fails for a reason different from the one it
claims to exercise.

### 3. Workload comparability and quality floor

Mutate candidate/range, fixtures, criteria, seeded defects, required outputs,
role boundaries, quality floor, and treatment apparatus. Confirm materially
different work cannot yield a quality-adjusted economy verdict. Force missed
T1/T2/T3 defects, incomplete coverage, a failing verdict, and an unmet quality
floor.

Blocking: cost is interpreted before equivalent work and outcome quality, or a
cheaper-but-worse result is called promising.

### 4. Participating-role and per-measure cost honesty

Add and remove participant costs independently for tokens, tool calls, wall
seconds, resources, rework/recheck, task duration, batch size, and foreman idle
gap. Confirm every participating role is aggregated and an unavailable value
blocks only the affected measure while complete measures remain visible.

Blocking: hidden cost shift, partial-role total presented as complete, blended
cost/quality score, or one incomplete measure suppressing valid raw evidence.

### 5. Dispatch, idle-gap, and cache telemetry

Exercise task-budget, observed-duration, dispatch-batch identity/size/mode,
foreman idle-gap, and cache-status validation. Attempt to infer cache status
from elapsed time or tokens and to assert a hit/miss without direct-observation
provenance.

Blocking: inferred cache state passes, missing telemetry is silently filled, or
the five-minute hypothesis is represented as an observed cache result.

### 6. Evidence strength and deterministic output

Run representative historical, paired-pilot, and repeated comparisons.
Confirm historical and single-pair evidence remains non-causal, raw
observations/reasons remain present when no verdict is available, stable
ordering holds, and identical inputs produce byte-identical output.

Blocking: unsupported causal/economy claim, mutable output ordering, omitted
raw evidence, or nondeterministic serialization.

### 7. Documentation and data safety

Reconcile the README commands and interpretation guidance against executable
behavior. Inspect every committed fixture for obvious synthetic identity and
manufacturing provenance. Run the envelope scan.

Blocking: documentation overclaims behavior, the scope expands beyond
presentation work, or any personal data, agent/model/account identity, prompt,
response, reasoning trace, absolute path, credential, remote configuration, or
private output appears.

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

Use additional temporary synthetic mutations needed by the measurements, but
commit no generated scratch output and access no network or private surface.

## Output and verdict

Write the review to
`docs/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`.
Return `READY` only if every measurement is explicitly supported and no
blocking finding remains. Otherwise return `NOT READY`, name the failed
measurement, exact path/behavior, and smallest evidence-backed remediation.
Do not repair the implementation, spawn a sub-agent, push, open a PR, merge, or
begin Track 1.
