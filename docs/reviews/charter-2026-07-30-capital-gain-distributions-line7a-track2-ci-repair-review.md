# Capital-Gain Distributions / Line 7a — Track 2 CI Repair Recheck Charter

Audience: Reviewer.

Status: **chartered for a fresh, author-independent focused recheck.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track2` (PR #120) at this committed
  review charter/pointer. Resolve `HEAD` through the orientation command and
  verify the printed commit against Git before acting.
- **Exact object:** the immediate parent commit titled
  `Close Track 2 CI consistency failures`, measured against its immediate
  parent, the clarified CI-repair charter. The implementation object is exactly
  three files: `packages/derivation/loader.py`,
  `tools/generate_frrs_t3_fixtures.py`, and
  `tools/presentation_harness/examples/pages/citation-walk-fixtures/production-shaped.v1.json`.
  Charter/pointer commits are context, not review targets.
- **Role:** fresh Reviewer with no exposure to the Builder's implementation
  process. This is a focused recheck of CI consistency, not a second review of
  the already-credited Track-2 runtime contract.
- **Scope and evidence-rung ceiling:** independently measure C1–C4 from
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track2-ci-repair.md`.
  Synthetic repository integration is the ceiling. Credit the prior F1/F2
  READY recheck except where this three-file delta could disturb it.
- **Stop conditions:** stop and return `NOT READY` if the object is not the
  exact three-file delta; any published schema/checksum or reviewed runtime
  behavior changed; the v1 registry, v1 release, or v6 adoption differs from
  the pre-Track-2 bytes; the generator does not reproduce both routes exactly;
  the golden did not enter through `live_coordinate_run`; the golden has any
  semantic change beyond the allowed line-16 derived-ID replacement and one
  declared line-16 citation pin; a failing test was weakened; evidence requires
  real/private material; or the review turns on governance interpretation.
- **Full reads before acting:** this charter;
  `docs/roles/reviewer.md`;
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track2-ci-repair.md`;
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track2-repair-recheck.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  the three-file implementation delta;
  `packages/schemas/artifact-package/artifact-package.v5.schema.json`;
  `packages/content/tax/2025/published-packages.json`;
  `packages/content/tax/2025/published-packages.v2.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v7-current.json`;
  `packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v1.json`;
  `packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v2.json`;
  `tests/derivation/test_language_schemas.py`;
  `tests/test_frrs_t3_resolver_bootstrap.py`;
  `tests/test_frrs_t4_w2_live_integration.py`;
  `tests/test_presentation_l2_integration.py`;
  `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`;
  `AGENTS.md#Fixture Rules`; `AGENTS.md#Schema Publication Protocol`; and
  `AGENTS.md#Data Safety Rules`.

Before measuring, echo the exact object range and file set, C1–C4, credited
evidence, evidence ceiling, and stop conditions.

## Required measurements

1. **Object custody.** Verify the reviewed implementation is the immediate
   parent of this charter and that its diff contains exactly the three named
   files. Confirm no test, schema, package registry, adoption, release, runner,
   projection, or pointer was changed by the implementation commit.
2. **One role vocabulary.** Confirm the only loader delta adds
   `checked-conclusion-binding` to `ROLE_VOCABULARY`, matching the already
   published `artifact-package.v5` role token without editing the schema or
   weakening the subset test.
3. **Two explicit publication routes.** Inspect the generator structurally and
   regenerate its in-memory file map. Confirm it exactly equals the committed
   FRRS corpus, v1 adoptions select only the v1 registry/release, v7 selects
   only v2, and the v1 registry/v1 release/v6 adoption remain byte-identical to
   the pre-Track-2 branch point.
4. **Golden provenance and semantic delta.** Confirm
   `tools/generate_presentation_l2_golden.py` still enters through
   `live_coordinate_run`; reproduce the golden byte-for-byte; compare parsed
   old/new models and establish that only presentation section 3 changed, with
   exactly the line-16 derived finding ID replacement and addition of
   `tax.us.2025.citation.form1040.line-16@v1`. Values, dispositions, all other
   citations and citation groups, redaction, package selection, and every
   other section must be unchanged.
5. **Exact regression closure.** Independently run the four previously failing
   test modules plus the adjacent coordinator, runner, and schema-registry
   modules. Do not accept the Builder's report as evidence.
6. **Safety and diff hygiene.** Run diff check, governance lint, and the
   main-to-HEAD envelope scan. Inspect fixture identities and paths for
   synthetic-only compliance.

## Verification

Run once:

```text
python3 -m unittest tests.derivation.test_language_schemas
python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
python3 -m unittest tests.test_dsbs_t2_coordinator
python3 -m unittest tests.derivation.test_runner
python3 -m unittest tests.test_schema_registry
git diff --check <clarified-charter>..<implementation>
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite. CI remains the gate of record after a READY recheck.

## Handoff

Commit one review record at
`docs/reviews/2026-07-30-capital-gain-distributions-line7a-track2-ci-repair-review.md`
with a falsifiable `READY` or `NOT READY` verdict, per-measurement evidence,
exact commands/results, and any residuals. Leave the worktree clean. Do not
repair, edit pointers or charters, push, merge, or begin Track 3.
