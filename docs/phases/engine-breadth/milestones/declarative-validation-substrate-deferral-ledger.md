# Deferral Ledger: Declarative Structured Validation and Consumer Dependency Substrate

Closing 2026-08-17. See the owner-advisor product review
(`docs/prototypes/declarative-validation-substrate/reviews/owner-advisor-milestone-product-review.md`)
for the full evidence account.

## Retired for this bounded class

- Tax policy for the bounded 2025 covered-W Form 8949/Schedule D subsystem
  moved out of generic Python and into versioned content (ADR-0066): a closed
  predicate grammar for member constraints, declared cross-family identity
  exclusivity, and reachability-derived consumer prerequisites that are
  mechanically required rather than execution-order coupled. `runner.py`'s
  domain references went from 24 to 0; the four surviving domain references
  in `package_validation.py` are the ADR-0066 Decision 9 named residual.
- The superseded hard-coded Form 8949 row guards and Form 1099-B identity
  collision matrix are deleted, not bypassed.
- Both schedulers (forward saturation and backward demand-driven) are proven
  to produce byte-identical results on this substrate, including
  attachment-bearing content — closing a `reference_runner.py` gap that
  predated this milestone (Track 4 Repair 1).

## Carried forward (named future work, not addressed here)

- **P1 — hand-maintained rule-artifact/attachment-rule capability allowlists.**
  At least six distinct, hand-maintained capability predicates are
  independently re-declared as literal sets across `live.py`, `marshal.py`,
  `presentation_projection.py`, `package_validation.py`, and `runner.py`.
  Three consecutive milestones have each missed a different member of this
  set (f1098e, this milestone twice). Scoped, not built:
  `milestones/rule-artifact-capability-table-consolidation.md`.
- **P2 — `accounts_for` exact-agreement coupling cost.** ADR-0066 Decision 5's
  exact-agreement requirement between a consumer's declared `accounts_for`
  and the reachability-derived constrained-family set is deliberate and
  correct — it is what makes an incomplete authoring declaration detectable —
  but it means adding a constraint set to an existing family is a breaking
  change for every consumer that reaches it. Ten such declarations exist
  today; the coupling is superlinear in family count. Not a defect, not
  scoped as a milestone; recorded so a future family addition budgets for it.
- **Noncovered / basis-not-reported Form 8949 transactions and every
  adjustment code other than W** — unchanged from the prior Form 8949
  milestone's own deferral ledger
  (`milestones/schedule-d-form8949-covered-wash-sale-deferral-ledger.md`);
  this milestone did not touch that boundary.
- **The `test_n_mfs_live_run_currently_raises` behavior-shape change** is not
  a deferral — it was fully repaired and re-verified in the owner-advisor
  review (R2): the MFS gap is still fail-closed, only its observable shape
  improved (a citable `blocked` disposition instead of an escaping
  exception). Recorded here only so a future reader does not mistake a
  git-blame hit on that test for an open item.

## Discharged events, not deferrals

- Four round-one substrate defects (marshal.py under-registered version sets,
  `runner.py` unguarded `evaluate_member`, dead `evaluate_constraints`,
  `field_equals` bool/numeric conflation) — all fixed and independently
  re-verified against the code, not the commit message, at `77212c21`.
- A failing type gate (48 mypy errors across 4 files) — repaired in the
  owner-advisor review; `python3 -m mypy` returns clean.
- A stale root `SEAT.md` duplicating `docs/phase-state.md`'s single
  re-entry-document role — deleted; confirmed nothing in the codebase reads
  it programmatically before removal.
- Track 3's independent review (`CHANGES REQUESTED` on a
  `packages/tax/loader.py` boundary break affecting unrelated F1098/1099-DIV/
  1099-G/1099-INT/W-2 tests) — repaired at `0604f2fb` and re-confirmed
  `ACCEPTED` on re-review before close.
