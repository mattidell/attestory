# Charter — Track 2 Builder: keyed same-run sources, a bounded test of statement reach

One builder unit. Authorised by the owner's choice of option A on 2026-09-23, **as a bounded test,
not a settled general solution**, after probe P2 found a corrected circumstance reaches every
borrowing but no Form 1098-E statement ([`a4-bounds.md`](a4-bounds.md), "Second pass — P2
result").

**The question this track answers:** do structured keys, carried from a subject into a same-run
intermediate result, let a corrected schooling circumstance change the **correct** statement
outcomes — without parsing rendered ids, and without affecting unrelated statements?

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at `4e79c5af` or later on that
  branch; verify with `git rev-parse HEAD` and `git branch --show-current`.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 2 Builder.
- **Assigned paths:** `packages/derivation/subject_dispatch.py`; the `_Run` methods
  `evaluate_subject_scoped_rule` and `_append_live_source` (and only as needed
  `_append_live_source_from_finding`) in `packages/derivation/runner.py`;
  `tests/derivation/test_subject_dispatch.py`; and new test classes appended to
  `tests/test_sli_circumstance_association_a4_pass2.py` (do not edit its existing tests).
- **Evidence ceiling:** synthetic `demo.*` identities; no content citizen adopted.
- **Deep reads, complete:** `packages/derivation/subject_dispatch.py` (its docstring states the
  join contract); `runner._append_live_source` and the comment above it; `SourceFact`;
  `tests/test_sli_circumstance_association_a4_pass2.py`, the P2 classes; `temp/a4-pass2/p2-report.md`
  if present.
- **Stop conditions:** stop and report, without working around it, if meeting an acceptance
  criterion needs: a published-schema change; storing keys in a derived finding; parsing any
  rendered id or symbol; a change to `marshal.py`, `pairing_dispatch.py` or `evaluator.py`;
  a change to how **any other caller** of `_append_live_source` behaves; or aggregation of
  several joined values into one (see "Not this track").

## What to build

When the per-subject dispatch publishes a finding, the **temporary same-run source** it appends
carries the **subject's structured keys**, taken from the subject `SourceFact` at dispatch time.
Nothing is parsed. The derived finding itself is unchanged — it gains no keys, and the durable
record gains nothing. Every other caller of `_append_live_source` still appends with no keys.

## The chain the acceptance tests drive

Four records, each hop one per-subject rule, all in one run:

1. **Status**, subject = financing claim (borrowing + period + institution + programme): publishes
   a categorical status for **both** outcomes — `adverse` pinning the adverse enrolment
   circumstance it joined, `not-adverse` pinning the declared default. It must **publish** in
   the adverse case; an `inapplicable` intermediate is not acceptable here.
2. **Link consequence**, subject = statement-to-borrowing claim (lender + statement + tax-year +
   borrowing): joins the status on `borrowing`, publishes the link's consequence.
3. **Statement consequence**, subject = the statement's box-1 finding (lender + statement +
   tax-year): joins the link consequence on the statement's keys, publishes a **statement-facing
   amount** — the reported amount when not adverse, zero when adverse — for a statement covering
   one borrowing.

## Acceptance

In `tests/test_sli_circumstance_association_a4_pass2.py` (P2's re-run) unless noted; exact ids,
not counts.

1. **Favourable path.** Each statement publishes its reported amount, and walking its pins
   reaches the link consequence, the status, and the default — never an enrolment finding.
2. **Corrected-adverse path.** Correct the enrolment to adverse through kernel currency (as P2
   Part A did) and re-derive. The affected statement **publishes a changed statement-facing
   amount**, and walking its pins reaches the **corrected** enrolment finding and not the
   displaced one. A statement that merely blocks because an intermediate disappeared does **not**
   pass this criterion.
3. **Two statements on one borrowing** (a servicer transfer): both follow the correction.
4. **Mismatched link:** a statement linked to a different, unaffected borrowing is byte-identical
   before and after the correction; and a link naming a statement that does not exist affects no
   statement.
5. **Keys are carried, not stored or parsed** (in `tests/derivation/test_subject_dispatch.py`):
   the appended same-run source's keys equal the subject's structured keys; the published derived
   finding has no keys; a source appended by any other caller still has none.
6. **Observed, not solved: one statement covering two borrowings** with different status values.
   Record what the current scalar join does — it selects one equal-valued match or blocks on
   differing values — as a test of the observed behaviour. That case belongs to P3.

## Not this track

Aggregating several joined values into one result (a statement covering several borrowings).
If any acceptance criterion above turns out to need it, stop and report with the evidence.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m mypy`, `python3 tools/governance_lint.py`,
`git diff --check` — all clean.

## Hand-off

Do not commit; the foreman reviews and commits. Report to `temp/a4-pass2/track2-report.md`: each
criterion, its test, what it asserts, the verification tails verbatim, and any stop condition met.
