# Capability — Compare a recorded date with a fixed date in a rule

## Purpose

The owner approved building this now. The mortgage route must tell whether a
loan is grandfathered debt, meaning debt secured by the home on October 13,
1987. Grandfathered debt is deductible whatever the money paid for. The
recorded origination date is box 3, `tax.us.2025.f1098.box3-origination-date`,
a JSON string in `date` format. The rule language has no date comparison:
`compare` is numeric only, and the `rule-artifact.v13` operators include
none for dates. See [P3 revision](p3-connected-design.md) and the
[design account](design-account.md), choice 3.

Build the narrowest capability that lets a rule compare one date-valued
fact with one fixed ISO date. Its first consumer is the grandfathering
condition. It is not a general date framework.

## Actions

1. **ADR.** Draft the next-numbered ADR, status `proposed`. It covers the
   operator's name, shape and semantics, and the schema versions it needs.
   It also covers how a missing value, a malformed value or a non-date value
   behaves (fail closed, with a named block code; choose existing codes if
   they fit). Name the first consumer, and record what is excluded: date
   arithmetic, intervals, durations, date-to-date comparison between two
   facts, time zones and parameters for the threshold. The literal date sits
   in the rule.
2. **Schema successor.** Add `rule-artifact.v14`, which is v13 plus the one
   operator. Add whatever package-schema successor is needed to admit v14.
   Follow AGENTS.md "Schema Publication Protocol" exactly:
   - new files only;
   - manifest entries appended through `write_manifest`;
   - no edits to published schema bytes or existing checksums.
3. **Engine support.** Wire the operator through every place a rule schema
   version is admitted and evaluated, including:
   - the evaluator;
   - package validation;
   - both runners;
   - `marshal.py` and `live.py`;
   - the authorization closure.

   The 2026-08-09 retrospective recorded a previous schema addition that was
   never wired into the live path. Pins and derivation records must show the
   date fact read as an input, like any other ref.
4. **Tests.** Add unit tests for the operator, covering each comparison,
   equality at the threshold, and missing, malformed and non-date input. Add a
   live test through `live_coordinate_run` with a test-only v14 rule reading a
   synthetic box 3, on a temporary or test publication surface, showing
   publication and pins. Show that the existing v13 content is unchanged in
   behaviour.

## Boundary and completion

Do not adopt the operator into any published tax package, and do not write
mortgage rules; the connected design does that later. Do not add date
arithmetic or any second operator. This is substrate work under
`packages/derivation/`, so run the full suite, plus `pytest
tests/test_schema_registry.py` and the schema consumer tests. Synthetic data
only.

Completion: the ADR draft, the schema successors, the engine wiring and the
tests are committed, and the full suite passes. Report the operator's final
shape, so the mortgage design can use it exactly, together with the commit.
The ADR stays `proposed` until the foreman has had it reviewed and the owner
accepts it.

## Context Capsule

- Source ref: `HEAD`. Resolve and report the full launch commit, then
  corroborate it against Git.
- Role: Builder. Milestone key: `mortgage-interest-circumstances`.
- Primary branch: `milestone/mortgage-interest-circumstances-translation`.
- Assigned paths:
  - the new ADR file and its `docs/adr/INDEX.md` row;
  - new schema files and their manifest entries under `packages/schemas/`;
  - `packages/derivation/` modules needed for the wiring;
  - new test modules.

  Do not edit `packages/content/` or the milestone documents.
- Deep reads: this charter; ADR 0077 (as the model for a schema-successor
  ADR); the commit `8ff08835` as the template for adding a rule-artifact
  schema version and its wiring;
  `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md`;
  AGENTS.md "Schema Publication Protocol" and "Test lanes".

## Resumption after interruption — owner findings

The first builder was stopped by a usage limit. Its work is checkpointed,
unpushed, in the commit titled `Checkpoint the interrupted date-comparison
capability (not yet passing)`. Resume from that commit. The owner
independently reproduced these defects in it, and they are part of this unit:

1. **Inherited package validation.** `artifact-package.v36` must keep every
   check v35 makes. In the checkpoint, `_reader_role_issues` returns early
   for v36, and exact-entrypoint validation's package-schema set omits v36.
   Through `validate_package`, v35 rejects an entrypoint naming `v999` when
   only `v1` is a member, and rejects `lineNote` on a rule lacking the
   required reader role. v36 accepts both. Extend every inherited check to
   v36, auditing every package-schema gate in validation, not only these two
   and not only rule-schema gates. Add negative package-validation tests
   showing v36 rejects what v35 rejects. A passing date rule does not show
   that v35's contract is preserved.
2. **Date domain.** The parser accepts `0000-01-01` and `0000-02-29`, and
   compares them as earlier than the threshold. The repository's JSON
   date-format checker rejects them. Make the operator's accepted calendar
   domain match that checker, for both the operand and the literal. Test
   invalid operands and literals accordingly, including year 0000, impossible
   days and leap-year edges.
3. **ADR wording.** Keep ADR 0078's tax example precise. Comparing an
   origination date identifies a *possible* grandfathering case; it does not
   establish every grandfathering condition. The ADR must not choose the
   cutoff's comparison or its equality behaviour for the consumer. P5 selects
   both against the authority.

All three findings must be resolved, not only attempted, before the unit is
complete. The ADR wording has no test, so say in the report where it was
changed. Leave the older universe-guard admission gap, which stops at
`artifact-package.v17`, untouched: it predates this unit and does not admit
v35. When this unit completes, it is independently reviewed before the
mortgage design relies on its contract.
