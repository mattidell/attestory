# Capital-Gain Distributions / Line 7a — Track 1 Independent Review Charter

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track1` at
  `b8a44e37462c464e5f9989dff24477d17f51930f`.
- **Exact object or commit range:** implementation commit
  `b80b5c8b87d4125c55c788e20af2171206bdb5ea..b8a44e37462c464e5f9989dff24477d17f51930f`.
  The preceding `b80b5c8` commit is the charter/pointer commit and is context,
  not the implementation object.
- **Role:** one author-independent Reviewer, High tier / high effort. Do not
  consult the Builder's thread or self-assessment.
- **Scope and evidence-rung ceiling:** measure only Track 1's versioned
  schema/content citizens, publication evidence, contract tests, immutable
  history, and charter boundary. Do not design or implement a repair, reopen
  ADR-0050, or evaluate unbuilt Track-2 runtime behavior.
- **Stop conditions:** stop and report if the exact range or branch tip differs;
  if any required committed source is absent; if review would require
  interpreting governance text; if a real value, identity, document,
  disposition, reason, workspace location, or generated private artifact is
  encountered; or if a test failure cannot be attributed to this range without
  a base comparison.
- **Full reads before acting:** this charter;
  `docs/roles/reviewer.md`;
  `docs/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track1.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md`;
  `docs/adr/0031-real-data-residency-boundary.md`;
  `docs/adr/0035-dividend-composition-and-lines-3a-3b.md`;
  `docs/adr/0036-schedule-attachment-ontology.md`;
  `docs/adr/0038-qdcg-worksheet-and-declared-absence.md`;
  every file in the exact implementation range, including
  `tests/test_capital_gain_distributions_line7a_t1_citizens.py`;
  `packages/tax/loader.py`; `AGENTS.md#Schema Publication Protocol`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the resolved branch tip, exact range, review ceiling,
independence constraint, and stop conditions.

## Required measurements

1. **Exact object and boundary.** Enumerate the implementation range and verify
   that it changes only Track-1 schema/content citizens, synthetic publication
   examples/negatives, manifest additions, and focused contract tests. Fail the
   check for any evaluator, coordinator, admission, package-successor, line-9,
   line-16, QDCG, presentation, browser, coverage, README, or retrospective
   behavior. Confirm no prototype code was copied as a production artifact.
2. **Exception-1 authority.** Recover C1–C4 from the committed citizens and
   compare them directly with ADR-0050: exact identities and `{yes,no}` domains,
   no defaults, presence-before-value, `free` supersession, and the accepted
   distinction between contributed components and derived checked conclusion.
   Exercise at least one non-`{yes,no}` mutation independently rather than
   relying only on the committed negative.
3. **Checked conclusion.** Verify the binding is declarative only, depends on
   exactly C1–C4, pins those four direct inputs, and implements the complete
   accepted truth table: `"no"` only when all four components are `"yes"`;
   otherwise `"yes"` once all are present; absent components do not silently
   become values. Independently mutate one truth-table row and one component
   omission and prove both reject.
4. **Box-2a source topology.** Compare member identity to the accepted 1a/1b
   statement pattern. Verify an independent box-2a family, horizon-keyed closure
   fact, closure mapping, selected subtotal symbol, multi-statement eligibility,
   and closed-empty authority are representable without changing either
   historical family. Confirm the member signal semantics and residual
   recorded-boxes successor do not create a second box-2a source inside the
   successor graph.
5. **Universe transition and history.** Verify the successor universe composes
   exactly `{1a,1b,2a}`, maps each once to the correct family, and leaves the
   residual recorded-non-composable set without `2a`. Confirm every historical
   schema and content citizen remains byte-unchanged. Inspect both manifest
   diffs: they may only add unused filenames/checksums, and the recorded
   checksums must match exact schema bytes. Mixed-graph runtime rejection is
   Track 2; flag runtime implementation here rather than demanding it.
6. **Form fields and citations.** Verify distinct line-7a and line-7b form-field
   identities and atomic disposition surfaces. Line 7b must contain exactly one
   ADR-0029 citation pin, with identity
   `tax.us.2025.citation.form1040.line-7b@v1`, whose source locus is exactly the
   2025 Form 1040 instruction paragraph fixed by ADR-0050. Confirm wrong
   identity and multiple citation mutations reject. Verify line 7a's citation
   citizen and printed locator against its declared source. No producer rule
   may exist in the range.
7. **Payload-instantiation and negatives.** Inventory every new schema version.
   Each schema that carries or references a payload must have a hand-written,
   fully resolved, obviously synthetic positive instance. Independently run
   every named negative and confirm each fails for its intended load-bearing
   reason—not an unrelated earlier error. Identify any required contract edge
   that lacks a meaningful negative.
8. **Loader and test honesty.** Read the focused test rather than accepting its
   assertions at face value. Confirm positives and negatives traverse the
   published registry and established production loader wherever that surface
   exists; tests must not validate a private reconstruction that production
   never loads. Grep for bypasses, hard-coded allowlists, and assertions that
   merely restate fixture bytes.
9. **Data safety.** Inspect the exact range for real or private material and run
   the required envelope scan. All identities and values must be obviously
   synthetic; no absolute local path or generated private artifact may appear.

## Verification

Run once, independently:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
python3 -m unittest tests.test_schema_registry
git diff --check b80b5c8b87d4125c55c788e20af2171206bdb5ea..b8a44e37462c464e5f9989dff24477d17f51930f
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Run an established loader/content test module only if the implementation
touches or claims that surface. Do not run the full suite merely to duplicate
CI; use a base comparison only for a specific failure attribution.

## Review record and verdict

Write
`docs/reviews/2026-07-29-capital-gain-distributions-line7a-track1-review.md`
and commit it on the same branch. Report one explicit verdict:

- `READY` — every required measurement passes with cited evidence; or
- `NOT READY` — one or more numbered findings F1… identify the violated
  charter/ADR/publication/safety clause, precise file/line evidence, and a
  reproducible measurement.

Record all commands and results. Findings recommend no scope expansion and no
repair design. Do not edit implementation, manifests, charters, phase state, or
the milestone plan; do not open/merge a PR or begin Track 2. Stop after the
review-record commit and return custody to the foreman.
