# Source Completeness And Interest Slice — Post-Merge Reconciliation Review

- Reviewer seat: reconciliation reviewer, High tier
- Subject: Source Completeness And Interest Slice as merged at `382a7af`.
- Reviewed at: committed `HEAD` on 2026-07-13. This review did not read
  successor-prototype material, switch branches, or inspect `wip/` or
  `archive/` refs.

## Findings

### SC-R1 — A direct member assertion preserves stale closure authority

- Severity: **patch-candidate**
- Defect: The kernel accepts an ordinary `assertion` for a current fact whose
  type is the adopted B1 family's member predicate, but it neither requires a
  `member-transition` nor advances the family's horizon. The existing closure
  finding therefore remains current, as does a zero that pins it. The known
  boundary is explicit in `packages/kernel/horizons.py` and is not enforced by
  any consuming workspace-service layer at `HEAD`.
- Contract: ADR-0017 decisions 3, 5, 6, and 7 require every membership change
  to atomically advance the horizon so old closure findings and their derived
  results fall through the existing individuation and derivation edges.
  ADR-0016 decision 5 limits a B1 closure-backed zero to the actually closed
  B1 universe. This violates Constitution Articles 7 (record-derived
  supersession through the declared edges), 12 (the derived finding remains
  current despite a now-relevant unpinned input), and 13 (the old zero remains
  published as eligible state).
- Reproduction: Starting from the committed lifecycle's B1 bundle, genesis
  horizon `b1.h0`, and current true closure finding `b1.closure.h0`, publish
  the empty-family zero. Introduce the payer and statement entities, then
  append a normal `assertion` for
  `tax.us.2025.f1099int.box1-interest|payer=demo-payer-bank-alpha,statement=stmt.demo-payer-bank-alpha.2025.a,tax-year=2025`
  with value `120`, rather than a `member-transition`. Projecting the accepted
  acts observed: horizon `b1.h0`; late-member finding current; `b1.closure.h0`
  current; prior derived zero current; coverage `closed`.
- Expected: The membership-changing assertion must be rejected at the
  authoritative admission boundary or routed atomically through a successor
  horizon. In either case, no current B1 closure-backed zero or `closed`
  coverage may survive a recorded late B1 member. No-resurrection is not a
  meaningful protection on this path: the predecessor was never superseded.

### SC-R2 — A same-member correction is accepted as a horizon transition

- Severity: **patch-candidate**
- Defect: `act-member-transition.v1` calls its `assert` member arm an addition,
  but `findings.apply_member_transition` does not verify that the asserted fact
  is new to the family. A second transition asserting the same fact is accepted
  as an ordinary correction and advances the horizon.
- Contract: ADR-0017 decision 4 states that a same-member value correction
  which does not change predicate membership does not advance the horizon;
  decision 3 limits accepted transitions to membership changes. This also
  violates Constitution Articles 7 and 13 by creating an unnecessary
  supersession root and forcing unrelated closure-backed outputs out of current
  state.
- Reproduction: From the same B1 genesis, introduce the payer and statement,
  then accept a `member-transition` asserting the B1 fact at `120` with
  successor `probe.h1`. Submit a second `member-transition` asserting that
  identical fact at `125` with successor `probe.h2`. Both acts are schema-valid
  and accepted; observed current horizon is `probe.h2` and the corrected member
  finding is current.
- Expected: The second act must be rejected as a non-membership transition (the
  value correction belongs on the ordinary assertion path), leaving `probe.h1`
  current. The admission boundary needs a way to distinguish add/remove/
  reclassification from same-member correction.

## Verified surfaces and limits

- The committed lifecycle and horizon tests reproduce incremental/full-rebuild
  equality, malformed-transition atomic rejection, family isolation, old-zero
  displacement after a valid transition, re-attestation plus explicit rerun,
  and no resurrection after valid removal. These guarantees do not cover the
  two accepted misrouted paths above.
- `RunContext` has no caller-supplied `closed_sets`; the only evaluator
  `closed_sets` value is internally derived from
  `resolve_closure_admissions`. Coverage structurally calls that same resolver
  after marshalling the same projected state, so calculation and coverage share
  admission resolution rather than duplicating it.
- The two-runner byte-parity result covers scheduling-independent publications
  for contexts supplied to both runners. It does not independently validate
  record admission, currency projection, coverage, or blocked/disposition
  assembly: both runners construct the same `_Run` and use `_Run.attempt`.
- Published schema manifests reject missing, unlisted, and checksum-mutated
  schema files; their Track 1 immutability tests pass.
- `.venv/bin/python -m unittest` passed: 314 tests. `.venv/bin/python
  tools/governance_lint.py` reported `governance lint: conformant`.
- The committed interest-content data-safety scan passes. A review scan of the
  merge's changed content found no private-path markers or account-identifier-
  shaped digit runs; fixture payers, statement identifiers, and amounts are
  explicitly synthetic.

## Verdict

A reconciliation patch branch is warranted. Its minimal finding set is
**SC-R1 and SC-R2**: establish an authoritative adopted-family membership
routing/admission boundary that (1) cannot accept a predicate-matching member
through plain assertion without the corresponding atomic horizon successor,
and (2) cannot accept a same-member correction as a membership transition.
The branch should add end-to-end regression probes for both accepted-act paths
and preserve the existing valid-transition lifecycle guarantees.
