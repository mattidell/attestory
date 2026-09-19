# Charter — readiness gate checks

Unit for one builder. Authorises the two executed checks named in the milestone
plan's
[readiness gate](../student-loan-circumstance-association.md#readiness-gate-before-any-producer-is-chartered),
and nothing else.

Their purpose is to raise the load-bearing claims of the
[product and evidence outline](outline-product-and-evidence.md) from evidence
level `read` to `run` before any producer is chartered. They are evidence, not
a design: they select no representation and adopt nothing.

## Boundaries

- **No production change.** No edit to any file under `packages/`, no new or
  changed content citizen in the production package, no ADR, no schema.
  `packages/tax/pairing_consequences.py` in particular is **not** to be
  modified or generalised — check 1 exercises the generic primitive in
  `packages/derivation/pairing_dispatch.py` directly, which is the claim under
  test.
- Synthetic `demo.*` identities only, with source values left intact.
- Disposable artifacts only, in the test module. Nothing is adopted.
- Do not settle the structured-circumstance product choice (the plan's
  owner-visible choice). Check 1 needs *a* shape in order to run; use one and
  label it provisional.
- Do not design a completeness mechanism. Check 2 observes and reports.

## Check 1 — dereference

Establish whether the adopted per-pairing primitive can carry this
relationship at all.

Build a disposable pairing whose left side is a Form 1098-E box-1 source and
whose right side is a schooling-circumstance source, and dispatch one declared
rule expression pairing-scoped through
`pairing_dispatch.evaluate_pairing_scoped_rule` with its own `pairing_type`,
`left_type` and `right_type`.

`tests/derivation/test_pairing_dispatch.py` is the harness precedent — reuse its
shape (`_finding`, `_currency`, `_sources_for`, `_symbol_for`), do not invent a
new one, and do not import from it.

Provisional circumstance shape, for this check only: **one finding whose value
is an object with named properties**, read with ADR-0067's `field` selector.
This is the shape pairing scope favours; it is not adopted.

Assert, in this order:

1. **The value actually read.** The publication's value must depend on both
   sides — the box-1 amount from the left and a named property from the right.
   Prove the dependence by changing the right side's property and observing a
   different published value. A publication count alone proves nothing.
2. **The pins.** The publication pins the pairing finding id, the left finding
   id, and the right finding id. Assert the exact ids, not the count.
3. **Loss of the target.** With the right-side source absent, the same dispatch
   yields a blocked outcome whose code is `DEPENDENCY_ABSENT` and whose
   `missing` names the right side's fact id. This is the "surviving reference
   is not sufficient support" behaviour the plan requires; record whether it
   comes for free.
4. **The prior consumer cannot enter this scope.** Evaluate, pairing-scoped, an
   expression that uses `require_closed` (and separately `count`) and assert it
   blocks. State the code observed. This is the executed form of the claim that
   the prior milestone's rule must be restructured rather than reused.

## Check 2 — omission

Establish what happens to a statement nobody associated.

Two Form 1098-E box-1 statements in one run, at distinct identities. One has a
current pairing to a circumstance; the other has none.

**Record the expected disposition before executing, in the results document:**
one publication for the associated statement, and for the unassociated
statement **no row of any kind — neither a publication nor a blocked row.**

Then execute and assert it positively rather than by absence of failure:

- exactly one publication, whose symbol/pairing corresponds to the associated
  statement;
- no blocked row names the unassociated statement's fact id;
- the unassociated statement's box-1 source is genuinely present in the run, so
  the silence is the dispatcher's iteration and not a missing fixture.

**If the observation differs from the expectation — if a blocked row does
appear for the unassociated statement — report that as a material finding and
stop. Do not adjust the expectation to match what ran.** That outcome would
refute the outline's section 6(b) and change Track 0's gate.

## Deliverables

1. One new test module, `tests/test_sli_circumstance_association_readiness.py`.
   Docstrings state what each assertion establishes and its ceiling.
2. `readiness-gate-results.md` in this directory: the expected dispositions
   recorded before execution, what was observed, each claim it raises from
   `read` to `run`, and every claim it does **not** raise — including that
   check 1 supplies only the mechanical half of the structured-circumstance
   choice, and that neither check establishes any tax conclusion, favorable
   eligibility, or that a production route exists.
3. Both committed on this branch. Do not leave work uncommitted.

## Verification before returning

`git diff --check`; `python3 tools/governance_lint.py`;
`python3 tools/envelope_scan.py --staged`; `python3 -m mypy` (repo-wide, and it
includes `tests/` — annotate accordingly); `python3 -m pytest -n auto`. Run the
complete set, not only the new module.

## Return

Report the four check-1 observations and the three check-2 observations as
facts, the exact blocked codes seen, anything that behaved differently from the
charter's expectation, and any claim in the outline you could not raise to
`run` and why. Do not extend scope to repair what you find.
