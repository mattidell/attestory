# Covered Long-Term Gains, Schedule D Line 8a — Track 1 Independent Review Charter

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/schedule-d-covered-ltcg-8a-track1` at
  `9cf7c738c698002d3e10f3f00ea1c8f6d7559f16`.
- **Exact object or commit range:** implementation commit
  `45b0e321a341e6b5225c38f159d2af874a58f873..9cf7c738c698002d3e10f3f00ea1c8f6d7559f16`.
  The preceding `45b0e32` commit is the charter/pointer commit and is
  context, not the implementation object.
- **Role:** one author-independent Reviewer, High tier / high effort. Do not
  consult the Builder's thread or self-assessment.
- **Scope and evidence-rung ceiling:** measure only Track 1's versioned
  schema/content citizens, publication evidence, contract tests, immutable
  history, and charter boundary. Do not design or implement a repair,
  reopen ADR-0052, or evaluate unbuilt Track-2 runtime behavior.
- **Stop conditions:** stop and report if the exact range or branch tip
  differs; if any required committed source is absent; if review would
  require interpreting governance text; if a real value, identity,
  document, disposition, reason, workspace location, or generated private
  artifact is encountered; or if a test failure cannot be attributed to
  this range without a base comparison.
- **Full reads before acting:** this charter;
  `docs/roles/reviewer.md`;
  `docs/reviews/charter-2026-08-02-schedule-d-covered-ltcg-8a-track1.md`;
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  (Supported Source Class, Completeness Boundary, Contracts sections);
  `docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md` (Decisions 1
  and 2 specifically);
  `docs/adr/0015-1099-int-statement-instance-identity.md`;
  `docs/adr/0016-source-family-claim-and-composition.md`;
  `docs/adr/0010-derived-finding-projection-and-currency.md`;
  `docs/adr/0011-tax-fact-identity-and-source-closure.md`;
  `docs/adr/0023-member-assertion-and-transition-boundaries.md`;
  every file in the exact implementation range, including
  `tests/test_schedule_d_covered_ltcg_8a_t1_citizens.py`;
  `packages/tax/loader.py`; `AGENTS.md#Schema Publication Protocol`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the resolved branch tip, exact range, review
ceiling, independence constraint, and stop conditions.

## Required measurements

1. **Exact object and boundary.** Enumerate the implementation range and
   verify it changes only Track-1 identity/family/closure/declaration
   citizens, synthetic publication examples/negatives, and focused contract
   tests. Fail the check for any Schedule D content, `selected-preferential-
   base` symbol, line 7a/7b/9/16, coordinator, admission-interlock,
   package-successor, presentation, browser, coverage, README, or
   retrospective behavior. Confirm no prototype code
   (`prototypes/schedule-d-covered-ltcg-8a/it2/design.md` etc.) was copied
   as a production artifact — the implementation must be a genuine
   reimplementation against ADR-0052 and existing accepted patterns.
2. **Statement anchor identity.** Recover the anchor identity
   `(tax-year, subject, broker-ref, logical-statement-ref)` from the
   committed citizen and compare it against ADR-0052 Decision 1 and the
   accepted Form 1099-DIV/1099-INT statement-identity pattern (ADR-0015).
   Confirm evidence, file, upload, scan, and document identifiers are
   excluded from the identity, and independently attempt at least one
   evidence-identity substitution beyond the committed negative.
3. **Eligible-transaction source family.** Verify the family is independent
   of (not nested inside) the anchor's own family, per ADR-0052 Decision 1
   — pin the current anchor finding, but do not compose the anchor's own
   closure. Recover the member predicate and confirm every named source-class
   condition is a contributed/attested field (covered security, basis
   reported to the IRS, long-term classification, no box-1f, no box-1g,
   Ordinary not indicated, QOF not indicated, no taxpayer-side adjustment,
   no collectibles/special-rate, gain-only) and that none is derived from a
   proceeds-minus-basis comparison. Independently mutate at least one
   predicate field to prove admission fails without it, beyond the
   committed negative.
4. **Identity correction and multiplicity.** Independently verify: two
   transactions from one anchor remain distinct members; two anchors with a
   colliding transaction-ref suffix remain distinct; correcting one
   transaction's value supersedes only that transaction's prior finding and
   leaves a sibling transaction, the anchor, and the family declaration
   current; and a plain assertion of a not-yet-member transaction is
   rejected (member transitions must go through the accepted membership
   path, ADR-0023). Reproduce at least one of these independently rather
   than only reading the committed test's assertion.
5. **Seven completeness declarations.** Recover all seven absence
   declarations (short-term, current losses, inbound carryovers, Form 8949,
   other Schedule D sources, lines-18/19, 1099-DA/QOF) and compare each
   against ADR-0052 Decision 2: exact `{yes, no}` domain, no default,
   presence-before-value, free supersession, keyed by tax year and subject.
   Confirm no synthesizing conclusion citizen exists anywhere in the range —
   Decision 2 requires nine authorities read directly, never through a
   conclusion hop. Independently mutate one declaration to a non-`{yes,no}`
   value and confirm rejection, beyond the committed negative.
6. **Boundary discipline on P2-S5A / box-2a.** Confirm this track does not
   publish, edit, or reference the box-2a family or its closure mapping as
   anything other than accepted, byte-unchanged history (ADR-0050). If the
   Builder's report states no citation citizen was needed at this track,
   confirm that determination is correct — the box-2a-closed successor
   consumption belongs to Track 2, not this track.
7. **Payload-instantiation and negatives.** Inventory every new content
   citizen against the existing (reused, not new) schemas. Each citizen
   that carries or references a payload must have a hand-written, fully
   resolved, obviously synthetic positive instance. Independently run every
   named negative and confirm each fails for its intended load-bearing
   reason — not an unrelated earlier error. Identify any required contract
   edge that lacks a meaningful negative.
8. **Loader and test honesty.** Read the focused test rather than accepting
   its assertions at face value. Confirm positives and negatives traverse
   the published registry and established production loader wherever that
   surface exists; tests must not validate a private reconstruction that
   production never loads. Grep for bypasses, hard-coded allowlists, and
   assertions that merely restate fixture bytes.
9. **Historical immutability.** Confirm every accepted ADR (including
   ADR-0036 and ADR-0050), every existing schema, and every existing
   content citizen remains byte-unchanged. Confirm no new schema file was
   introduced (the Builder's report claims reuse of existing generic
   schemas only) — verify this claim directly rather than trusting it.
10. **Data safety.** Inspect the exact range for real or private material
    and run the required envelope scan. All identities and values must be
    obviously synthetic; no absolute local path or generated private
    artifact may appear.

## Verification

Run once, independently:

```text
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t1_citizens
python3 -m unittest tests.test_schema_registry
git diff --check 45b0e321a341e6b5225c38f159d2af874a58f873..9cf7c738c698002d3e10f3f00ea1c8f6d7559f16
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Run an established loader/content test module only if the implementation
touches or claims that surface. Do not run the full suite merely to
duplicate CI; use a base comparison only for a specific failure
attribution.

## Review record and verdict

Write
`docs/reviews/2026-08-02-schedule-d-covered-ltcg-8a-track1-review.md` and
commit it on the same branch. Report one explicit verdict:

- `READY` — every required measurement passes with cited evidence; or
- `NOT READY` — one or more numbered findings F1... identify the violated
  charter/ADR/publication/safety clause, precise file/line evidence, and a
  reproducible measurement.

Record all commands and results. Findings recommend no scope expansion and
no repair design. Do not edit implementation, manifests, charters, phase
state, or the milestone plan; do not open/merge a PR or begin Track 2. Stop
after the review-record commit and return custody to the foreman.
