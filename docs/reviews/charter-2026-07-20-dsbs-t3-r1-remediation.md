# Charter: Track 3 R1 Remediation (named target, not first-match-among-five)

Date: 2026-07-20. Prepared by the foreman; owner-approved dispatch
(ADR-0034). Branch: `track/dsbs-t3-qdcg-line16` (continue on this branch,
currently at `5aa47b5`). Governing finding: the F1 delta re-review
(`docs/reviews/2026-07-20-dsbs-t3-f1-delta-rereview.md`), Finding R1.

## Background

The F1 fix (`1247b89`) corrected the original defect (an unfiltered
`glob("rule.*.json")` picking up Track 3's new, unrelated
`rule.form1040-line16.v2.json`) by filtering candidates to members of
`package.interest-slice.json` before tampering. That filtered set still
contains five qualifying `role: "computation"` members
(`f1099int-b1-subtotal`, `f1099int-b3-subtotal`, `f1099oid-subtotal`,
`non-form-interest-subtotal`, `form1040-line2b`), and both tests still
iterate and break on the first sorted match among those five. The
delta re-review found this deterministic today but not principled: it is
a narrowed instance of the same implicit-first-match convention that
caused F1, just now constrained to a safe candidate set. A future change
to package membership or file layout could shift which member is selected
without the test proving the intended verified body was the one mutated.

## Scope (exactly this, nothing more)

In both `tests/test_frrs_t3_resolver_bootstrap.py::test_changed_member_bytes_under_honest_registry_refuses`
and
`tests/test_frrs_t4_w2_live_integration.py::ResolverCounterProbes::test_member_substitution_has_exact_refusal_and_layout_is_inert`,
replace the "iterate sorted candidates, break on first membership match"
logic with selection of one explicit, named target member:
`tax.us.2025.rule.form1040-line2b` (version `v1`) — the interest package's
own terminal line-output rule, a stable and semantically meaningful choice
(it is the package's published line, not an interchangeable intermediate
subtotal). Locate that specific file directly (by its declared `id`, not by
directory position) and tamper it. If the file cannot be located directly
by id without a directory scan, a scan is acceptable but must assert
after loading that the parsed body's `(id, version)` equals the named
target exactly — the test must fail loudly, not silently pick a
substitute, if the named target is ever missing or renamed.

Preserve both tests' existing assertions exactly (`Refusal` with the same
`reason` string). Do not touch any DSBS/Track 3 content, schema, or kernel
file. Do not touch any other test. Do not touch
`tools/scaffold_live_acts.py` or `workspace-seed/`.

## Verification

Before reporting done, all green:
- `.venv/bin/python3 -m unittest` — full suite, confirm 541/541 (or current
  total) pass, both named tests pass standalone too
- `.venv/bin/python3 -m mypy`
- `.venv/bin/python3 tools/governance_lint.py`
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD`

## Commit discipline

One commit on `track/dsbs-t3-qdcg-line16`, following `5aa47b5`. Do not
push, merge, or edit `docs/phase-state.md`/`docs/foreman-handoff.md`.

## Report back

State the exact selection code now used in both tests, confirmation that
`tax.us.2025.rule.form1040-line2b` v1 is genuinely a member of
`package.interest-slice.json`, and full battery pass/fail. Terse,
evidence-based.
