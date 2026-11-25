<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "rule-artifact-capability-table-consolidation",
  "status": "Closed 2026-11-25. Hardening only; schema_capabilities.py + guards landed, 775/775 replay identical.",
  "retrospective": "docs/milestone-retrospectives/2026-11-25-rule-artifact-capability-table-consolidation.md",
  "scope": [
    "replace hand-maintained literal rule-artifact, attachment-rule, and artifact-package version sets across packages/derivation/ with one declared capability table (packages/derivation/schema_capabilities.py)",
    "enforce structural completeness via a registry test that fails whenever any published rule-artifact, attachment-rule, or artifact-package schema version lacks a capability-table row, and preserve every real capability distinction with zero behavioral or numeric change across all 775 recorded lists"
  ],
  "non_goals": [
    "no new tax coverage, no published schema edits, no core/registry/release version bump, and no ADR",
    "no flattening of genuinely distinct capability predicates into a single set",
    "no packages/kernel/ edits"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-25-rule-artifact-capability-table-consolidation.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Milestone Plan: Rule-Artifact/Attachment-Rule Capability Table Consolidation

Milestone key: rule-artifact-capability-table-consolidation.
Branch: milestone/rule-artifact-capability-table-consolidation-hardening.
Phase: Engine Breadth (hardening). Selected & refreshed: 2026-11-25.
Starting point: main at `2b761638f` (core v106, registry v104, release v104;
`rule-artifact` v1–v17, `attachment-rule` v1–v12, `artifact-package` v1–v44).

Audience: Foreman, Owner, Builder, Reviewer. Hardening milestone spanning core
derivation machinery (`packages/derivation/`). No tax-coverage change, no
published schema change, no core version bump, and no ADR.

## Origin

Filed 2026-08-17 from the `declarative-validation-substrate-f8949` milestone's
owner-advisor product review (P1,
`docs/prototypes/declarative-validation-substrate/reviews/owner-advisor-milestone-product-review.md`),
after the foreman independently re-verified the review's claim by direct
inspection of all four named files. Not attempted inside that milestone per
explicit owner instruction: scope it, do not build it, unless scoping
revealed it was small enough to land safely inline — it is not; see
"Why this is not a same-milestone repair" below.

## Problem

Every schema version a `rule-artifact.*`/`attachment-rule.*` citizen may
declare is checked against a hand-written, literal Python set or tuple,
independently re-declared at each call site that needs to know "can this
citizen do X." There is no single source of truth. ADR-0066 Decision 7
closed the *unregistered* case — a schema entirely absent from every list now
fails loudly at the package-validation boundary. It did not close the
*partially registered* case: a schema present in most but not all of the
sets that should include it. That is the failure mode that keeps recurring,
and it is silent — content validates cleanly, then misbehaves only at
runtime, only on the specific citizen that exercises the missing capability.

**Confirmed recurrence, four consecutive milestones, plus one same-milestone
re-break:**

1. f1098e milestone: `runner.py:1331` missing a registered version (documented
   in that milestone's own record).
2. declarative-validation-substrate-f8949: `marshal.py:101` missing
   `rule-artifact.v5`, and `marshal.py:89` missing `attachment-rule.v8` — the
   same omission, in the same function, found independently twice (once by
   the owner-advisor review, once more precisely by the foreman during
   repair).
3. A third, earlier instance already lives only as a code comment:
   `artifact-package.v22` (referenced in the owner-advisor review; not
   independently re-verified by this plan — confirm its exact site before
   chartering).
4. f1098e milestone's own rebase onto the ratified
   declarative-validation-substrate-f8949 base (2026-08-18): 8 sites across
   `live.py`/`marshal.py`/`package_validation.py`/`runner.py` needed
   independent fixes to admit `rule-artifact.v6`. One of the eight,
   `runner.py`'s disposition `record_codes` closed set, is not even a
   pre-existing gap this milestone could have caught earlier — it is a
   mechanism declarative-validation-substrate-f8949 itself introduced,
   discovered only because f1098e's own new SLI block codes were silently
   downgraded to generic `DEPENDENCY_INVALID` at runtime. See
   `docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md`.
5. The same f1098e milestone's own subsequent bisectable-rebase curation
   (still 2026-08-18) **re-broke one of the sites item 4 had just fixed**:
   `runner.py`'s `run_and_record` function has its own separate `use_v2`
   computation from `_Run.__init__`'s, and the curation dropped
   `rule-artifact.v6` from one but not the other, reopening the exact
   divergence item 4 closed. Latent and test-invisible — f1098e's real
   package also trips `_uses_attachment_machinery`, forcing both paths to
   `True` regardless of which schema set is checked. Caught only by an
   independent review of PR #178, not by the 1488-test suite. This is the
   first confirmed instance of the mechanism being re-broken after a fix,
   not merely missed on first build — direct evidence that fixing each
   recurrence by hand does not make the next one less likely.

## Evidence: the sets are not one set

A shallow read might suggest "just union everything into one registered-schema
set." Direct inspection of `packages/derivation/package_validation.py` alone
(sampled at lines 64, 244, 280, 591, 662, 1380, 1439, 1715, 1760, 1805, 1819,
1921, 1955) shows the sets are **not duplicates of one list** — they encode
at least six genuinely distinct capability predicates:

| Capability | Example membership | Sample sites |
| --- | --- | --- |
| Full known-schema membership (rule-artifact + attachment-rule, every version) | `rule-artifact.v1`-`v5`, `attachment-rule.v1`-`v6`,`v8` | `package_validation.py:591,662,1715`; `live.py:71` |
| Declared-absence `when`/`value` refs outside `requires` | `rule-artifact.v3`-`v5` only | `marshal.py:101`; `package_validation.py:1380,1955` |
| "v6-shape" attachment (adjustment rows, positive/adjustment tie-out subtotals) | `attachment-rule.v6`,`v8` only | `runner.py`'s `_V6_SHAPE_ATTACHMENT_SCHEMAS`; `package_validation.py:1439,1805,1819`; `presentation_projection.py:369,401` |
| Itemization-capable attachment (excludes v1, which predates itemizations) | `attachment-rule.v2`-`v6`,`v8` | `package_validation.py:1760` |
| Full attachment-only membership | `attachment-rule.v1`-`v6`,`v8` | `marshal.py:89`; `presentation_projection.py:39`; `runner.py`'s `ATTACHMENT_SCHEMAS` |

A consolidation that flattens these into one set would silently widen or
narrow at least one call site's actual eligibility — that is exactly the
defect class this plan exists to close, reintroduced by the fix. **The real
design task is a capability table with one row per schema version and one
boolean/enum column per distinct predicate above**, not a single set.

## Why this is not a same-milestone repair

- At least six distinct capability predicates (likely more once `live.py`
  and `presentation_projection.py` are read as closely as
  `package_validation.py` was for this plan — this plan's site count is a
  lower bound, not a final inventory).
- Spans five files: `live.py`, `marshal.py`, `presentation_projection.py`,
  `package_validation.py`, `runner.py` — all core generic engine machinery,
  blast radius across every tax form, not just this milestone's Form 8949
  content.
- Every call site's migration must be individually verified to read the
  *correct* capability column, not just "the new shared thing" — a
  mechanical find-replace risks exactly the silent-widening/narrowing defect
  this plan exists to prevent.
- `package_validation.py` is this milestone's read-only reference precedent
  throughout Track 3/4; touching it was explicitly out of every repair
  charter's assigned paths.

## Proposed shape (design sketch, not a spec — Track 0 owns the real design)

A single declared table, one row per `(schema, version)`, one column per
capability predicate named above, likely as a small module
(`packages/derivation/schema_capabilities.py` or similar) that
`live.py`/`marshal.py`/`presentation_projection.py`/`package_validation.py`/`runner.py`
import from rather than re-declaring literal sets. Candidate shape:

```python
# sketch only
SCHEMA_CAPABILITIES = {
    "rule-artifact.v5": {"declared_absence_refs", "known"},
    "attachment-rule.v8": {"known", "attachment", "v6_shape", "itemizations"},
    # ...
}
```

Open questions a real Track 0 must settle, not this plan:

- Whether the table lives beside the schemas themselves (generated from
  schema metadata) or as hand-maintained content with its own registry test
  proving every published schema version has a row (closing the
  under-registration failure mode structurally, the same way ADR-0066
  Decision 7 closed the unregistered-schema failure mode).
- Migration order and whether it can be additive (new table + old sets
  temporarily coexisting, verified equal, then old sets deleted) to keep
  each step's blast radius reviewable.
- Whether `package_validation.py`'s role as reference precedent changes —
  it currently has the most complete/correct sets; the table's initial
  content should likely be derived from it, not re-authored from scratch.

## Evidence a Track 0 for this milestone should require

- A registry-level test that fails if any published `rule-artifact.*` or
  `attachment-rule.*` schema version lacks a capability-table row (structural
  closure of the recurring defect, not just a fixed snapshot).
- A migration proof per consumer file showing byte-identical behavior before
  and after switching that file's literal set to a table lookup.
- Full-suite green, per this repo's `AGENTS.md` "Test lanes" (any change
  under `packages/derivation/` runs the full suite, not the fast lane).

## Non-goals

- Does not add tax coverage; not an engine-breadth slice.
- Does not change any published schema.
- Does not attempt to unify capabilities that are genuinely distinct into
  one flag "for simplicity" — the table must preserve every real
  distinction found above.
- Does not edit `packages/kernel/` or any published schema/content file.

## 2026-11-25 Refresh and Stages

Since this plan was filed on 2026-08-17 (`rule-artifact.v6`, `attachment-rule.v8`,
`artifact-package.v22`), schema families have grown to `rule-artifact.v1`–`v17`,
`attachment-rule.v1`–`v12`, and `artifact-package.v1`–`v44`. In PR #309
(`sale-block-explanations`), `packages/derivation/package_validation.py` still
carried per-version `artifact-package.v*` allowlists skipping `v41`–`v43` until
`v44` was manually appended. Accordingly, this milestone consolidates all three
derivation schema families (`rule-artifact.*`, `attachment-rule.*`, and
`artifact-package.*`) across `packages/derivation/` into one typed capability
table (`packages/derivation/schema_capabilities.py`).

1. **P0 (census & capability-table design, no committed code).** Exhaustively
   inventory every literal `rule-artifact.v*`, `attachment-rule.v*`, and
   `artifact-package.v*` version set/tuple/comparison across
   `packages/derivation/`. Group every call site by its exact semantic
   capability predicate, identify any pre-existing partial-registration drift
   (intentional vs. accidental omission), design
   `packages/derivation/schema_capabilities.py` plus its registry-completeness
   and drift-prevention tests, and prove exact set-equivalence (or classify
   every intentional drift fix) before writing production code.
2. **Decisions** by the foreman (logged in `## Decisions`).
3. **Track 1** implements `packages/derivation/schema_capabilities.py`, migrates
   every audited call site in `packages/derivation/`, adds registry-completeness
   and consumer-equality/anti-literal-set tests, and verifies full `pytest`,
   `mypy`, `governance_lint.py`, `envelope_scan.py`, and 775-list full-surface
   replay (`775 / 775` identical, zero diffs).
4. **Fresh independent review**, repair if needed, curation, closeout, final
   review, green CI `verify`, merge.

## P0 result

Completed 2026-11-25 against `main` `2b761638f` (evidence in
`docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation-evidence/p0.md`):

- **Published schema inventory (70 total):** `rule-artifact.v1`–`v17` (17, in
  `packages/schemas/derivation/published.json`), `artifact-package.v1`–`v26` and
  `v28`–`v44` (43, `v27` absent, in `packages/schemas/derivation/published.json`),
  and `attachment-rule.v1`–`v6`, `v8`, `v10`–`v12` (10, `v7` and `v9` absent, in
  `packages/schemas/tax/published.json` — Track 1 completeness guard must read
  both manifests).
- **Exhaustive AST census:** 107 AST sites across `packages/derivation/**/*.py`
  (58 multi-version capability checks, 29 single-version capability checks, 5
  family-prefix checks, 12 `_successor_graphs` historical pin tuples, 3
  historical/synthesized single-schema literals).
- **Capability table design:** Three frozen dataclasses
  (`RuleArtifactCapabilities`, `AttachmentRuleCapabilities`,
  `ArtifactPackageCapabilities`) in `packages/derivation/schema_capabilities.py`
  preserving every distinct predicate (`84 / 87` capability checks match with
  exact set equality).
- **Drift audit:** 3 accidental omissions (`package_validation.py:1262` skipping
  `artifact-package.v41`–`v43`; `package_validation.py:3047` skipping
  `artifact-package.v28,v32`–`v34,v41`–`v43`; `package_validation.py:4017`
  skipping `attachment-rule.v8`) verified safe to fix against all 106
  committed 2025 packages; 3 preserved historical/schema-constrained boundaries
  (`rule-artifact.v12`–`v17` outside `compile_validation_graph` /
  `check_validation_graph`, `artifact-package.v18`–`v44` outside
  `universe_guard_active`, and `attachment-rule.v10` / `v5` / `v1`–`v5` BFS
  distinctions); plus 1 test source-grep dependency at
  `tests/test_later_year_basis_reuse_track0.py:1849` flagged for Foreman
  decision.

## Decisions

1. **Fix the 3 accidental omissions in Track 1 while preserving all 3 schema-constrained/historical boundaries (foreman decision under owner direction, 2026-11-25).**
   - Fix `package_validation.py:1262` (`_reader_role_issues`) to include `artifact-package.v41`–`v43` (`PACKAGE_READER_ROLE_SCHEMAS`: `v34`–`v44`).
   - Fix `package_validation.py:3047` (exact entrypoint pins) to include `artifact-package.v28`, `v32`–`v34`, `v41`–`v43` (`PACKAGE_EXACT_ENTRYPOINT_SCHEMAS`: `v20`–`v44`).
   - Fix `package_validation.py:4017` (check 10c `subtractive_positive_basis`) to include `attachment-rule.v8` (`ATTACHMENT_ADJUSTMENT_ROWS_EXECUTABLE_SCHEMAS`: `v6`, `v8`, `v11`), matching check 10b at line 3862.
   - Preserve `validation_graph_participant` (`rule-artifact.v1`–`v11` only), `universe_guard_active` (`artifact-package.v3`–`v17` only), and `bfs_reachability_edges` (`attachment-rule.v6,v8,v11,v12` only) so committed cores `v1`–`v106` and historical digests stay byte-identical.
2. **Keep `attachment-rule.v10` at `executable_and_validated=False`, `projection_supported=True` (foreman decision, 2026-11-25).**
   Preserves exact current runtime and validation behavior with zero unintended widening while maintaining projection compatibility (`tests/derivation/test_attachment_rule_v11.py`).
3. **Update `tests/test_later_year_basis_reuse_track0.py:1844-1858` to inspect `PACKAGE_UNIVERSE_GUARD_SCHEMAS` directly (foreman decision, 2026-11-25).**
   Replaces the fragile source-text partition of `package_validation.py` with direct inspection of `PACKAGE_UNIVERSE_GUARD_SCHEMAS`, preserving the exact `highest == 17` and `artifact-package.v26 not in allowed` assertions.
4. **Migrate all 58 multi-version sites, all 29 single-version capability checks, and the 4 `rule-artifact.` prefix checks to `packages/derivation/schema_capabilities.py` (foreman decision, 2026-11-25).**
   Retain only the explicit non-capability pins (`loader.py:45,47`, `package_validation.py:1683`, `package_validation.py:2926-2958`, and `presentation_projection.py:93`'s intentional fail-closed `startswith("attachment-rule.")` detector). Enforce both the dual-manifest registry completeness guard (`derivation/published.json` + `tax/published.json`) and the zero-exemption AST anti-scattered-allowlist guard in `tests/derivation/test_schema_capabilities.py`.

## Closeout

Closed 2026-11-25. Added pure-stdlib `packages/derivation/schema_capabilities.py`
covering all 70 published `rule-artifact`, `attachment-rule`, and
`artifact-package` schemas, migrated all 7 derivation consumer modules, closed
the 3 accidental omissions in `package_validation.py` (`_reader_role_issues` on
`v41`–`v43`, exact entrypoint pins on `v28`/`v32`–`v34`/`v41`–`v43`, check 10c
on `attachment-rule.v8`), preserved the 3 historical/schema-constrained
boundaries (`validation_graph_participant`, `universe_guard_active`,
`attachment-rule.v10`), and added dual-manifest completeness and zero-exemption
AST anti-scattered-allowlist guards in `tests/derivation/test_schema_capabilities.py`.
No published schema, content, kernel, or HTML file changed. Full `pytest`
(7,729 passed), `mypy` (551 files clean), and 775-list `v106` replay (`775 / 775`
identical, `0` differences) passed; independent review returned `READY` with no
findings.
