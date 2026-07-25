# Track 0 Delta Review — Participant-Cost Completeness Repair

Status: **READY**
Date: 2026-07-24
Role: independent High / high delta Reviewer (measurement-integrity lens)
Charter: `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair-review.md`

## Capsule echo (pre-review)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-economy-t0-measurement-substrate` → `5c979e50cbfb6ae6ca5d7cd69a9d7a77ca78e859` (working tree clean at this tip) |
| **Exact object** | The participant-cost repair at the resolved source commit, principally `tools/presentation_economy/comparison.py`, its focused tests, paired examples, and README contract text — repair landed as `4f8a07c` (*repair Track 0: enforce participating-role completeness in comparisons*). Reconciled against the pre-repair implementation commit `2f5fcc1` (identical to its parent `4f8a07c^` for `comparison.py`) and the blocking review at `docs/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`. Foreman/clerk continuity records and process-only commits (charters, phase-state, handoff, roadmap) are outside the artifact-quality object. |
| **Role** | One fresh independent delta Reviewer, High tier / high effort, measurement-integrity lens. |
| **Scope** | Verify the repair closes the omitted-participant cost-shift finding; derives required roles from the frozen workload's `role_boundaries`; preserves explicit zeros and explicit unknowns; blocks only the affected measure; retains complete measures and raw observations; does not regress the other Track 0 measurement results. |
| **Evidence-rung ceiling** | Independent delta review of the approved Track 0 repair. No contract redesign, no second repair, no harness start, no non-blocking advisories, no generalization beyond UI/UX presentation work. |
| **Stop conditions** | Stop if source ref unresolvable, exact repair object or prior review missing, pre-fix attack cannot be reproduced from committed artifacts, a check needs personal/machine-specific data or a remote, or the conclusion would exceed the Track 0 review gate. |

Source ref resolved cleanly against a clean working tree; the exact repair
object and the prior blocking review are both present and readable. No stop
condition tripped. Builder self-report (the repair commit message and repair
charter) was treated as input, not proof — every claim below was independently
reproduced from committed artifacts and ephemeral, uncommitted synthetic
mutations.

## Verdict

**READY**

The omitted-participant cost-shift finding (Track 0 review Measurement 4) is
closed. No other Track 0 measurement result regresses. Required verification
floor is green.

---

## Independent verification

### 1. Reproduced the pre-repair attack against the pre-repair implementation

Extracted `tools/presentation_economy/comparison.py` and its sibling modules
at `2f5fcc1` (byte-identical to `4f8a07c^`) into an isolated package and ran
the exact review-described sequence against the pre-repair fixtures:

| Step | Action | Result |
| --- | --- | --- |
| 1 | Set treatment `harness` participant `tokens.value = 50000` | `tokens` verdict `regression` (baseline `15200`, treatment `61200`) |
| 2 | Remove the `harness` participant object entirely (same quality outcomes) | `tokens` verdict **`economically-promising`** (baseline `15200`, treatment `11200`, delta `-4000`) |

Confirms the pre-repair implementation could and did produce
`economically-promising` from an undeclared harness-cost shift — matching the
blocking finding exactly.

### 2. Ran the identical mutation against the repaired implementation

Same two-step mutation (set harness cost to `50000`, then delete the harness
participant from the treatment observation) replayed against the current
`tools/presentation_economy/comparison.py` and the current committed frozen
workload/fixture (which now declares harness at explicit zero in the manual
arm):

```
tokens        insufficient-evidence | demo-paired-harness: missing required participant role 'harness' for tokens
tool_calls    insufficient-evidence | demo-paired-harness: missing required participant role 'harness' for tool_calls
wall_seconds  insufficient-evidence | demo-paired-harness: missing required participant role 'harness' for wall_seconds
```

Every affected measure becomes `insufficient-evidence` with a deterministic
reason naming both the offending observation id and the missing declared
role. `economically-promising` is no longer reachable through this attack.
Non-participant measures (`agent_count`, `browser_count`, …) are unaffected
and remain `no-interpretable-difference`, confirming the block is scoped to
the three participant-cost measures only.

### 3. Required role set comes from the frozen workload, not from visible participants

- Appended a synthetic `role_boundaries` entry for the already-valid `builder`
  role (not present in either arm's committed participant list) to a copy of
  the frozen workload and reran comparison: all three participant measures
  correctly became `insufficient-evidence`, each reason naming `'builder'` as
  the missing role — proving the requirement is driven by
  `workload["role_boundaries"]` (`_required_roles`) and is detected even when
  the role is absent from **both** arms, not merely diffed between them.
- Confirmed an explicit zero is accepted: the committed fixture's harness
  `tokens.value = 0` contributes to (and does not block) the treatment total
  (`11200` including harness's `0`).
- Confirmed a null value with its required `missing_reason` on one role/measure
  blocks only that measure: nulling the harness `tokens` measure (with a valid
  `missing_reason`) left `tokens` at `insufficient-evidence` while
  `tool_calls` and `wall_seconds` remained independently interpretable
  (`economically-promising` in this synthetic case) — the null does not
  cascade to other measures.

### 4. Complete measures and raw observations remain visible; quality precedes cost

- Read `build_comparison`: the per-measure loop checks `quality_comparable`
  first, then the role-completeness `missing_reason`, then per-value nulls —
  quality still gates before cost interpretation, and the new role-omission
  check sits alongside (not ahead of or replacing) the existing quality gate.
- The existing `test_incomplete_role_cost_blocks_only_that_measure` and the
  new `test_omitted_declared_role_cannot_yield_economically_promising` both
  assert the unaffected measures/verdicts remain interpretable and that raw
  baseline/treatment values are preserved on affected measures where present.
- No blended cost/quality score is introduced; the repair only added
  role-derivation and a completeness gate ahead of the existing per-measure
  aggregation, unchanged for `agent_count`, `browser_count`, and the other
  non-participant extractors.

### 5. Full and focused verification floor (independently rerun)

| Command | Result |
| --- | --- |
| `.venv/bin/python3 -m unittest tests.test_presentation_economy` | **27 tests OK** (was 26 pre-repair; adds `test_omitted_declared_role_cannot_yield_economically_promising`) |
| `validate --dataset …/presentation-exploratory-baseline.v1.json` | `{"valid":true}` |
| `compare … --baseline manual --treatment harness-assisted` (×2) | exit 0; byte-identical |
| `.venv/bin/python3 -m unittest` (full) | **590 tests OK** (was 589 pre-repair) |
| `.venv/bin/python3 -m mypy` | Success: no issues found in 114 source files |
| `.venv/bin/python3 tools/governance_lint.py` | conformant |
| `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` | clean (exit 0) |
| `git diff --check main..HEAD` | clean |

The committed `test_committed_invalid_comparison_fixtures` case now includes
`demo-invalid-comparison-omitted-harness-role` (removes
`observations.1.participants.1`, expects `tokens` →
`insufficient-evidence`) and passes. README's new "Participating-role
completeness" section (explicit zero participates; null+missing-reason blocks
only that measure; absent declared role blocks only that measure and names it;
never `economically-promising`) matches the executable behavior exhibited
above line for line. The paired valid-observations fixture's manual arm now
declares `demo-harness` at explicit `tokens/tool_calls/wall_seconds` zero
instead of omitting it, consistent with the repair's stated intent.

---

## Regression check against the other six Track 0 measurements

Re-examined each PASS measurement from the prior review against the repaired
code and reran its supporting evidence:

| # | Measurement | Status | Note |
| ---: | --- | --- | --- |
| 1 | Historical source fidelity | **PASS (unchanged)** | Repair touches only `comparison.py`/fixtures/README/tests; baseline dataset and its reconciliation are untouched. |
| 2 | Strict contract and correction behavior | **PASS (unchanged)** | `validation.py` was not modified by the repair; full unittest confirms no change in accept/reject behavior. |
| 3 | Workload comparability and quality floor | **PASS (confirmed)** | Quality gating (`quality_comparable`) still precedes the new role-completeness check in the per-measure loop; unaffected by the repair. |
| 4 | Participating-role and per-measure cost honesty | **PASS — blocker cleared** | See sections 1–4 above. |
| 5 | Dispatch, idle-gap, and cache telemetry | **PASS (unchanged)** | Extractor list for these measures is untouched; full unittest and mypy confirm no regression. |
| 6 | Evidence strength and deterministic output | **PASS (confirmed)** | Two independent `compare` runs of the same committed inputs remain byte-identical after the repair; causal/evidence labeling logic untouched. |
| 7 | Documentation and data safety | **PASS (confirmed)** | Envelope scan clean; README addition matches executable behavior; all identifiers remain `demo-*`; no absolute paths, credentials, or account identity found by local pattern scan of the changed files. |

No previously passing Track 0 measurement regressed.

---

## Out of scope (honored)

No implementation repair, no sub-agent spawn, no push/PR/merge, no Track 1
work, and no contract redesign beyond confirming the minimal enforcement
already specified by the repair charter and the approved milestone plan's
economy definition.
