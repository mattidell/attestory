# Payer-Reported Current-Inclusion Market-Discount Interest — Independent Review Charter

Audience: Reviewer.

Status: prepared for owner launch after the Builder hands off a clean exact range.

## Context Capsule

- **Source ref and resolved launch commit:** the market-discount milestone
  branch at the Builder handoff commit; verify the resolved SHA against Git.
- **Exact implementation object:** the Foreman will record the planning-tip to
  Builder-tip range. Review only that exact range; the planning commit is
  context, not implementation.
- **Role and tier:** one author-independent integrated Reviewer, Medium/medium.
  Do not consult the Builder thread, uncommitted ledger, or self-assessment.
- **Scope and evidence ceiling:** measure MD-C1 through MD-C5 and MD-P1–P10 /
  MD-N1–N13. The ceiling is production-shaped synthetic evidence through
  `live_coordinate_run`; no real data, transaction/basis calculation, new
  evaluator design, or implementation repair.
- **Stop conditions:** stop if the exact range or branch tip differs, the
  worktree is dirty, historical bytes/checksums changed, review requires
  governance interpretation or a neighboring tax decision, private material is
  encountered, or a failure cannot be attributed to the exact range.

## Review measurements

The Reviewer must report falsifiable results, not a general quality impression:

1. **Paper and boundary:** verify that both boxes are covered exactly, that box
   5 is the OID route, and that the implementation trusts payer-reported
   current inclusion rather than calculating accrual/election/basis/disposition.
2. **Selected-version inventory:** independently reproduce the Builder's
   mechanical inventory from the current adoption, release registry, package,
   and selected member checksums. Published-but-unselected citizens do not
   count.
3. **Source identity and closure:** exercise separate originals, correction,
   negative rejection, closed-empty, late-member displacement, and both family
   closures at the production contribution/lifecycle boundary.
4. **Composition and line 2b:** mutate composition v3 and the line-2b successor
   to omit, duplicate, substitute, or unpin a family; prove package validation
   refuses and all seven closures are required.
5. **Schedule B:** verify exactly seven Part-I row sets, correct member type and
   subtotal pairing, preserved threshold/Part-II/Part-III behavior, per-family
   and combined tie-outs, and attachment-only containment.
6. **Compatibility:** resolve v10/v5 through the real resolver and prove v9/v4
   remains valid and unchanged. Inspect registry diff for additions only.
7. **Explanation/presentation:** trace one canonical positive golden from
   `live_coordinate_run` through exact citations. Reuse generic negative
   presentation evidence or inspect a compact mutation; reject copied one-field
   presentation models as evidence of a new behavior.
8. **Economy accounting:** report Orientation Block bytes/words, tool calls,
   wall time, authored versus generated/expanded lines/bytes, first-review
   verdict, and repair count, keeping artifact volume separate from authored
   contract/runtime/test changes.
9. **Boundary attack:** search for disposition, partial-principal, basis,
   taxpayer-accrual, subtractive-adjustment, Schedule D, unrelated-income, new
   evaluator, attachment-runtime, or presentation behavior that escaped the
   charter.

## Targeted review reads

Read the plan, Builder charter, reviewer role, exact ADR text, selected current
and successor content, and the complete case-bearing tests. For large mutable
code, inspect these symbols and entrypoints first:

- `packages/derivation/package_validation.py`: `validate_package` and
  composition/attachment admission helpers;
- `packages/derivation/source_authority.py`:
  `resolve_closure_admissions` and `audit_collect_authority`;
- `packages/derivation/runner.py`: `_execute` and attachment/tie-out dispatch;
- `packages/derivation/live.py`: `live_coordinate_run`;
- `packages/derivation/production_resolver.py`:
  `select_current_adoption`, `_verify_release_and_registry`, and
  `resolve_production_package`; and
- `packages/derivation/presentation_projection.py`:
  `_resolve_field_row`, `_resolve_attachment`, `build_presentation_model`,
  and `validate_presentation_model`.

Prescribed test surfaces are the new market-discount contract/integration/
Schedule-B modules, K-1 contract and integration methods used as unchanged
evidence, `tests/test_attachment_rule_v2.py`, selected resolver methods in
`tests/test_frrs_t3_resolver_bootstrap.py`, and generic projection/live tests
in `tests/test_presentation_l2_integration.py`.

## Verdict and handoff

Return exactly one verdict:

- `READY` when the full matrix, boundary, compatibility, safety, selected
  version, and economy measurements pass; or
- `NOT READY` with numbered findings that name the violated contract/case,
  precise file/line evidence, and a reproducible measurement.

Findings may recommend one bounded correction but must not implement it or
expand the milestone. The Reviewer writes and commits its review record, then
returns custody to the Foreman. A second substantive finding after one repair
cycle returns to the owner.

