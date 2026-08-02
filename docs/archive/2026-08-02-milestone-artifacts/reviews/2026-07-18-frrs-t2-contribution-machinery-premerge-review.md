# First Real Return Slice — Track 2 (Contribution Machinery) — Pre-Merge Review

Reviewer: owner-launched, author-independent pre-merge reviewer (did not implement
Track 2). Date: 2026-07-18. Branch: `track/frrs-t2-contribution-machinery`.
Delta reviewed: **`c48973c` → `b449b20`** (the single implementer commit;
1,588 insertions across 10 files). Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-17-frrs-t2-contribution-machinery.md`;
contract: ADR-0032 (D2). Advisory — the owner decides disposition. This review
does not redesign ratified contracts.

## Verdict

**Merge-ready. No blocking finding and no scope defect.** All six charter
deliverables are present and, where the charter demanded *executed* goldens
rather than asserted stubs, they execute. The runs-consume-facts **MUST**
condition is genuinely discharged at the live entrypoint: `live_run` has no
raw-input parameter and no `**kwargs`, so the adversary's `inputs=`/ghost-id
injection is a Python argument-binding `TypeError` — a structural barrier, not a
policy check — and `marshal_run_context` reads evaluator input **only** from
current record state, so a ghost id absent from the record cannot appear.
Full suite, mypy, governance lint, and the data-safety scan are green. Findings
below are one production condition for Track 3 and non-blocking observations.

## Evidence (re-run by this reviewer on this branch)

- `python3 -m unittest` (full suite) → **373 tests OK**. Track-2 suite
  `tests/test_frrs_t2_contribution_machinery` → **15 OK**, including the
  kill-test, both E14.2 paths, any-order, supersession, and SC-R2 as executed
  tests.
- `python3 -m mypy packages tools tests` → **no issues in 81 source files**.
- `tools/governance_lint.py` → **conformant**.
- Data-safety: a marker scan of the whole `c48973c..b449b20` diff finds no
  personal path or value (the only hit is the data-safety test's *own* forbidden-
  token tuple); the Track-2 fixture `frrs_t2/examples/contribution-batch.synthetic.json`
  and all identifiers are `demo.*` synthetic.
- **Independent structural probe (not relying on the test's assertions):**
  `inspect.signature(live_run)` has no `inputs`/`sources`/`raw_inputs`/`scenario`
  parameter and no `VAR_KEYWORD`, confirming the `TypeError` barrier is real;
  `marshal_run_context(state=FindingState(), …)` over empty record state returns
  empty `inputs`/`sources`, confirming a ghost id cannot be marshalled.

## Deliverable-by-deliverable

1. **Contribution applicator — faithful.** `apply_contribution` admits a
   `contribution.v1` citizen as an immutable provenance anchor (no supersession,
   no withdrawal; references must be *current* evidence). `_validate_finding`
   enforces ADR-0032 Decision 2 exactly: a finding's `contribution_id` must
   resolve to a known contribution whose `evidence_id` is a **member of the
   finding's `evidence_ids`**, and the kernel still rejects any `pins` on a human
   finding — so the contribution pin cannot become a derivation edge. Verified by
   the applicator's positive golden and the evidence-mismatch rejection.
2. **Contribution record — faithful.** `contribution-record.v1` started → terminal
   accounts validate against the published schema; the started record rejects
   terminal-only fields. Schema registered in kernel `published.json`.
3. **Runs consume facts (MUST) — discharged.** `run-request.v1` stays a closed
   request citizen distinct from `RunContext` (a value-bearing request is
   schema-rejected). `marshal_run_context` is the sole production constructor and
   projects inputs/sources from `currency.current_finding_ids` only. `live_run`
   is the live entrypoint with no raw-value channel. See F1 for the residual.
4. **E14.2 static check — faithful, both halves.** `validate_package` emits
   `E14_2_FORBIDDEN_DEPENDENCY` for a contribution/record citizen appearing as a
   package member **and** for a rule `pin` naming one. Both are executed goldens.
5. **Schema wiring — present.** The seven Track-1 contribution citizens are
   registered; `act_log._payload_schema_id` now resolves `act-assertion.v2` /
   `act-member-transition.v2` from the nested finding's declared `schema`, so v2
   carrier acts admit without inventing a second envelope channel.
6. **Negative goldens — executed, not asserted.** Any-order equivalence
   (independent batches commute to equal current state); correction-by-
   supersession (both findings on record, `horizon_state.current_by_chain`
   asserted unchanged — no horizon advance); SC-R2 (a same-member correction
   routed through `member-transition` rejects with "already in the family").

## Findings

### F1 — The raw evaluator `run()` and the fixture `_context` remain reachable by import; the entrypoint barrier is structural, the runner fence is policy
**Classification: production condition (Track 3), non-blocking now.** The charter's
target — the `7770000` ghost-id bypass **through the live entrypoint** — is closed
structurally: `live_run` cannot accept a raw input, and the marshaller cannot
surface an off-record value. But the guarantee "a live run has *no* structural
path to a raw input" is entrypoint-scoped, not evaluator-scoped: `packages.derivation.runner.run`
is still public and accepts any hand-assembled `RunContext`, and
`runners/derive.py._context` (which builds `InputFinding`/`SourceFact` from
scenario JSON, ghost ids included) is still importable. Their only fence is the
`FIXTURE_ADAPTER_ONLY = True` flag plus docstrings — policy, not a type barrier.
This is acceptable for Track 2, which has **no wired production caller at all**
(synthetic-fixture-only): there is not yet a "live run" that could call the wrong
function. When Track 3 wires the real workspace to `live_run`, it must also close
the raw runner as a live path — e.g. make `run`/`_context` unreachable from
production (private module, marshalling-token parameter, or import fence), so the
structural guarantee covers the evaluator and not only the entrypoint. Recorded so
it is carried, not lost. (Consistent with the closing note's "carried to Track 3"
row for structural-against-a-production-resolver.)

### F2 — `live_entrypoint_accepts_raw_inputs()` is a name-based reflection proxy
**Classification: non-blocking.** The helper checks the signature for a fixed set
of forbidden *parameter names*. It would not catch a raw channel introduced under
a different name or via `**kwargs`. It is harmless as a belt-and-suspenders assert
because the kill-test *also* attempts the real call and requires the `TypeError`
(the genuine structural fact), and `live_run` today has no `**kwargs`. If the helper
is kept, prefer asserting the positive invariant (the parameter set is exactly the
marshalling inputs) over enumerating forbidden names.

### F3 — Failed-batch terminal record swallows its own schema-validation error
**Classification: non-blocking.** In `apply_contribution_batch`, the `failed`
terminal record is best-effort validated inside `except SchemaValidationError: pass`.
That is defensible (the batch is already failing and the caller gets the record on
the raised exception), but it means a malformed *failed* record would pass silently.
Optional hardening: assert the failed-record shape in a test, since the failure
path is otherwise unexercised by a golden.

### F4 — `marshal_run_context` carries heuristic binding paths
**Classification: non-blocking.** The marshaller has several binding routes
(explicit `input_bindings`, `collect_source_names`, and a "legacy demo path" where
`symbol == fact type id` gated by a `required_by_rules` scan). This is more surface
than the invariant strictly needs, but every route reads exclusively from
`current_findings`, so none of it can introduce an off-record value — the property
that matters holds. Flagged only as future simplification surface for Track 3/4
when the real binding contract is wired.

## Scope fence — clean

The delta touches only: `kernel/contribution.py` (new), `kernel/findings.py`,
`kernel/act_log.py`, `derivation/live.py` (new), `derivation/marshal.py`,
`derivation/package_validation.py`, `derivation/runners/derive.py` (fence flag +
docstring), one synthetic fixture, and the Track-2 test. No production resolver,
release/adoption resolution, live-workspace bootstrap, RG-1 repair, W-2 closure,
live-run harness, OCR, or UI. No ratified ADR or Track-1 schema citizen is edited.

## Recommendation

Merge PR for Track 2. Carry **F1** into the Track-3 charter as a named production
condition (close the raw evaluator/`_context` as a live path when the production
entrypoint is wired). F2–F4 are non-blocking; none requires a change to this
branch. The ADR-0032 named production conditions are discharged here or explicitly
carried to Track 3 per the closing note, which this review confirms as accurate.
