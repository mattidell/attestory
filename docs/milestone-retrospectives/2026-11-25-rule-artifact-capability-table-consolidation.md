# Retrospective: Rule-Artifact, Attachment-Rule, and Artifact-Package Capability Table Consolidation

Milestone key: rule-artifact-capability-table-consolidation. Plan:
`docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md`.
Closed 2026-11-25. Hardening under `packages/derivation/` and `tests/`; no
published schema, core, registry, release, or kernel change.

## What happened

Hand-maintained schema version sets across `packages/derivation/` had caused
silent partial-registration drift across four earlier milestones and again in
PR #309 (`artifact-package.v41`–`v43` omitted from `package_validation.py`). P0
inventoried all 70 published schemas across `packages/schemas/derivation/published.json`
(17 `rule-artifact`, 43 `artifact-package`) and `packages/schemas/tax/published.json`
(10 `attachment-rule`), audited all 107 AST sites across `packages/derivation/**/*.py`,
identified 3 accidental omissions safe to close and 3 historical/schema-constrained
boundaries that must remain explicit, and designed a pure-stdlib capability table.

Track 1 added `packages/derivation/schema_capabilities.py` (`RuleArtifactCapabilities`,
`AttachmentRuleCapabilities`, `ArtifactPackageCapabilities`, lookup helpers, and
derived `frozenset[str]` views), migrated all 7 derivation consumer modules,
closed the 3 accidental omissions (`_reader_role_issues` on `v41`–`v43`, exact
entrypoint pins on `v28`/`v32`–`v34`/`v41`–`v43`, check 10c on `attachment-rule.v8`),
updated `tests/test_later_year_basis_reuse_track0.py` and `tests/test_track1_validation_index.py`
(where `v96`'s `artifact-package.v43` mutations now properly catch `ENTRYPOINT_DANGLING`
and `ENTRYPOINT_VERSION_MISMATCH`), and added `tests/derivation/test_schema_capabilities.py`
enforcing dual-manifest completeness and zero scattered multi-version allowlists.
Full `pytest` (7,729 passed), `mypy` (551 files clean), and the 775-list `v106`
replay (`775 / 775` identical, `0` diffs) passed; independent review returned
`READY` with no findings.

## What worked

- Checking both `packages/schemas/derivation/published.json` and
  `packages/schemas/tax/published.json` in P0 caught that `attachment-rule.v*`
  lives in the tax manifest, ensuring the completeness guard covers all 70
  schemas rather than silently skipping attachments.
- Running a drift-vs-boundary audit before editing separated the 3 accidental
  omissions from the 3 schema-constrained/historical boundaries (`validation_graph_participant`,
  `universe_guard_active`, `attachment-rule.v10`), keeping every committed
  core (`v1`–`v106`) valid and every recorded return byte-identical.

## What to change

- Any future `rule-artifact`, `attachment-rule`, or `artifact-package` schema
  version now adds one typed row in `packages/derivation/schema_capabilities.py`
  and is automatically rejected by `tests/derivation/test_schema_capabilities.py`
  if omitted or if a consumer introduces a raw literal version set.
