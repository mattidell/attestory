# Review: Track 1 — Schema Citizens — Author-Independent Pre-Merge Review

Date: 2026-07-19. Seat: author-independent reviewer (did not author this
work; read only the charters, ADR-0035/0036 and their cited prototype
evidence, and the branch — no authoring session, no other track's review
consulted). Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-19-dsbs-t1-schema-citizens-review.md`. Build
charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-19-dsbs-t1-schema-citizens.md`.
Object under review: `main..track/dsbs-t1-schema-citizens`
(`1d2a58b`, `2a08d80`, `60bbbc0`, `272b7a9`, `95e36ab`, `a6f11f3`, plus the
charter/handoff-only commits `c6d62f6` and `a698dca` that carry no
schema/content/code — noted at F1).

## Verdict: ready

No decision-blocking finding. All eight falsifiable checks hold. Findings
below are observational (non-blocking), each tied to a charter check.

## Findings

**F1 (process, non-blocking).** The branch carries two commits beyond the
charter's named six: `c6d62f6` ("plan: charter Track 1 pre-merge review",
adds this review's charter and the build charter to the repo) and `a698dca`
("docs: hand off with Track 1 review dispatched", touches only
`docs/foreman-handoff.md` and `docs/phase-state.md`). Verified via
`git show --stat` on both: no schema, content, code, or test file is
touched by either. Boundary-safe, no data-safety exposure. Recorded for
completeness against the charter's commit list.

**F2 (Check 4 — vocabulary reconciliation, informational).** The chosen
direction and its evidence are stated in one canonical place: the `1d2a58b`
commit message ("Direction: SOURCE_SET_UNCLOSED wins. The evaluator has
always emitted it (BLOCK_CLOSURE), every executed scenario golden records it
verbatim, and committed tests assert it; SOURCE_SET_OPEN existed only as an
unexercised enum entry..."). Cross-checked against
`packages/derivation/evaluator.py` (`BLOCK_CLOSURE = "SOURCE_SET_UNCLOSED"`,
unchanged in this delta) and against
`tests/test_dsbs_t1_schema_citizens.py::test_the_runner_emission_is_the_reconciled_code`,
which asserts this directly. The reconciled schemas
(`derivation-record.v3.schema.json`, `npe-walk.v2.schema.json`,
`form-field.v3.schema.json`) name only `SOURCE_SET_UNCLOSED`; a repo-wide
grep for `SOURCE_SET_OPEN` confirms it survives only in schema-history files
(`derivation-record.v2.schema.json`, `npe-walk.v1.schema.json`,
`form-field.v2.schema.json`) and in the superseded content instance
`packages/content/tax/2025/form1040.line-2b.form-field.json` (schema
`form-field.v2`, version `v1`), which `packages/tax/loader.py`'s
`load_form_fields()` no longer surfaces as current: the loader now indexes
by id and keeps the highest published version (`_version_rank`), and the
new `form1040.line-2b.form-field.v2.json` (schema `form-field.v3`, version
`v2`) is the id's only current citizen — confirmed by
`test_form_field_v3_carries_the_emitted_code_and_line_2b_v2_rides_it`. The
old v1 instance remains published (checksummed in
`packages/content/tax/2025/published-packages.json`) as history, not as a
current-loadable value — exactly the charter's "historical, not current"
carve-out. `ITEMIZATION_TIE_OUT_VIOLATION` was confirmed name-only: a
repo-wide grep for it under `packages/derivation/*.py` and
`packages/tax/*.py` returns no hits; it appears only in the three schema
files and one example fixture.

**F3 (Check 5a — runtime universe guard scoping, informational).** The
`universe_guard_active` gate in `packages/derivation/package_validation.py`
(`package.get("schema") in {"artifact-package.v3", "artifact-package.v4"}`)
scopes only the `COLLECT_TARGET_NOT_FAMILY` half of the guard; the
`RECORDED_NON_COMPOSABLE_INPUT` half runs unconditionally for every package
generation (it is not inside the `if not universe_guard_active: continue`
branch — verified by reading the loop body directly). This matches the
in-code comment precisely ("The collect-target half binds the
package-language generations that postdate ADR-0035... the already-published
v1/v2 instances are recorded history") — the comment names only the
collect-target half as exempted, and the code does exactly that, no more.
The exemption is asserted by an executed test, not merely documented:
`test_published_pre_adr_0035_package_generations_stay_exempt` constructs an
`artifact-package.v2` whose sole rule collects against
`demo.family.alpha` with no `source-family.v1` member in the package (a
violation that free-standing under v3/v4 triggers `COLLECT_TARGET_NOT_FAMILY`,
confirmed by the adjacent `test_collect_against_an_undeclared_source_set_is_rejected`
on the same fixture shape under `artifact-package.v4`) and asserts the code
is *not* raised under `artifact-package.v2`. The scoping choice is a
reasonable builder judgment, not literal charter text, but it is consistent
with this codebase's established pattern of admitting old package/schema
generations alongside new ones (e.g. `form-field.v1`/`v2`/`v3`,
`quantity-vocabulary.v1`/`v2` co-admitted in `artifact-package.v4.schema.json`)
rather than retroactively invalidating already-published, already-checksummed
package instances (`tax.us.2025.package.interest-slice` v1,
`tax.us.2025.package.core-calculations` v1–v3) that predate the family/universe
vocabulary and could not have declared it.

**F4 (Check 6 — boundary fence, confirmed clean).** `git diff main..HEAD --
packages/derivation/evaluator.py packages/derivation/runner.py` is empty:
neither file is touched anywhere in this delta. The only `packages/derivation/`
runtime-adjacent files touched are `loader.py` (two new entries in the
existing `ROLE_VOCABULARY` frozenset — `dividend-universe`, `attachment-rule`),
`records.py` (a `CURRENT_RECORD_SCHEMA` string constant bumped from
`derivation-record.v2` to `.v3`, and `_VERSIONED_RECORD_SCHEMAS` widened to
recognize both on recovery), `explanation.py` (docstring/schema-string bump
from `npe-walk.v1` to `.v2`), and `package_validation.py` (the two new
admission-time guards, new role/schema-enum entries). None of these change
evaluator or runner *semantics*; they are the mechanical string/vocabulary
carry the reconciliation requires. No 3a/3b, line-9, or line-16 rule
content; no Schedule B form content (`grep -rn "SCHB\|schedule-b" packages/content
packages/schemas` returns nothing outside the generic `attachment-rule.v1`
schema description, which names Schedule B only as prose context, not as a
schema key); no tie-out check implementation (confirmed at F2); no D2
declared-absence facts were added.

**F5 (Check 7 — data safety, confirmed clean).** Every new fixture id in
`packages/sample_data/dsbs_t1/{examples,negatives}/` is `demo.*`/`demo-*`
scoped (`family: "demo"`); the committed tax-layer content
(`packages/content/tax/2025/`) uses only the established `tax.us.2025.*`
production-content convention, consistent with every other committed 2025
citizen in the repo (not a fixture, not flagged). A scan of `git diff
main..HEAD` for a real local filesystem path prefix and for the two
owner-held tool names finds only the charter/handoff prose *naming* the two
owner-held tools as
intentionally-untracked references — no file content from either is
present. `git status --short` confirms `tools/scaffold_live_acts.py` and
`workspace-seed/` remain untracked (`??`) in this worktree and were not
touched or committed by this review. No dollar values, dispositions, or
refusal text appear anywhere in the delta; the `$1,500` reference from
ADR-0036 does not recur in this delta at all (Track 1 is schema-only, no
threshold parameter values are instantiated). `tools/envelope_scan.py
--range main..HEAD` (re-run fresh, see below) exits 0 with no findings.

**F6 (Check 8 — verification battery, re-run fresh, not trusted).** All four
green, run directly in this worktree on `.venv/bin/python3` (Python 3.13.12,
no rebuild needed):
- `.venv/bin/python3 -m unittest` — `Ran 477 tests in 102.198s`, `OK`.
- `.venv/bin/python3 -m mypy` — `Success: no issues found in 94 source files`.
- `.venv/bin/python3 tools/governance_lint.py` — `governance lint: conformant`.
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — exit 0, no
  output (clean).

## Check-by-check disposition

1. **1099-DIV statement/family citizens** — holds. Direct comparison of
   `packages/content/tax/2025/family.f1099div-1a.json` /
   `-1b.json` and their closure mappings against
   `family.f1099int-b1.json` / `closure-mapping.f1099int-b1.json` shows
   identical structural shape (schema, scope, `closure_claim` prose pattern,
   `member_predicate`, `authorizes_subtotal`, `closure_horizon_key:
   "family-horizon"`, `admission.condition: "current-literal-true"`). The
   bundle (`f1099div.bundle.json`) declares five `fact-type.v2` citizens
   with `value_schema`s (box1a, box1b, two source-closures, recorded-boxes);
   `published-packages.json` carries checksummed rows for the family and
   bundle citizens.
2. **`dividend-universe.v1`** — holds. Schema and content name
   `{1a→family, 1b→family}` composable boxes and `{2a,3,5,7,12}`
   recorded-non-composable; `recorded-boxes` value schema structurally
   enforces explicit `null` as declared absence (required keys, `null`
   admitted, `additionalProperties: false`), verified both by direct
   `jsonschema.Draft202012Validator` probe in
   `test_recorded_boxes_value_schema_admits_declared_absence_only` and by
   inspection. Three named negatives present and rejected
   (`composable-without-family`, `box-in-both-sets`, `undeclared-box`), plus
   a fourth exercised structural negative (duplicated composable box).
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` is named on the schema/content
   surface only; `grep -rn "CAPITAL_GAIN_DISTRIBUTION_RECORDED"
   packages/derivation packages/tax --include=*.py` returns no hits — it is
   not raised anywhere in this delta.
3. **Attachment citizens** — holds. `attachment-rule.v1.schema.json` is
   schedule-agnostic (`additionalProperties: false` on every level, no key
   containing "schedule" or "b1099" etc.); `collect_members` is a `$def` at
   schema level. Part III answer pattern pins `{"enum": ["yes","no"]}`,
   never boolean, cross-checked against ADR-0036 decision 4 and
   confirmation round 2 (`reviews/confirmation-r1.md` lines 162–189, which
   settled on exactly this presence-over-categorical-truthy-domain shape
   after round 1 found the boolean-encoding masking hole). The Schedule D
   stub (`attachment-rule.v1.schedule-d-stub.json`) shares the identical key
   set with the generic example (asserted by
   `test_generalization_stub_shares_the_identical_schema_surface`). Three
   named negatives present and rejected: boolean-valued answer fact type
   (`fact-type.v2.boolean-answer.json`, rejected at admission not at the
   fact-type schema — correctly, since `fact-type.v2` legitimately admits
   booleans elsewhere), a completeness expression reading value before
   presence (`attachment-rule.v1.value-before-presence.json`, rejected
   because `required_answer.check` is pinned to the const `"presence"`), and
   a member row outside the declared family
   (`attachment-rule.v1.row-outside-declared-family.json`, rejected because
   `collect_members` is `additionalProperties: false` and admits no sibling
   literal-row key). No disagreement found between the shipped shape and
   `evaluation-analysis.md`/`confirmation-r1.md` beyond what ADR-0036 already
   resolved in the owner-ratified text; where the round-1 confirmation
   found gaps (boolean short-circuit, unpinned answers), the ratified ADR
   and this delta both carry the round-2 fix.
4. **Vocabulary reconciliation** — holds; see F2.
5. **Admission-time validation guards** — holds; see F3 for the scoping
   assessment. Both guards (`COLLECT_TARGET_NOT_FAMILY` /
   `RECORDED_NON_COMPOSABLE_INPUT` for 5a;
   `ATTACHMENT_ANSWER_NOT_CATEGORICAL` / `ATTACHMENT_ANSWER_FACT_TYPE_ABSENT`
   for 5b) have both rejecting and admitting tests in
   `tests/test_dsbs_t1_schema_citizens.py::AdmissionGuards`. The categorical
   check (`packages/derivation/package_validation.py` guard 10) is tested
   against the boundary case directly: `test_otherwise_falsy_categorical_answer_domain_is_rejected`
   uses `{"enum": ["yes", ""]}` (a non-boolean, technically-string domain
   with a degenerate falsy member) and confirms rejection — not just the
   boolean case.
6. **Boundary fence** — holds; see F4.
7. **Boundary and data safety** — holds; see F5.
8. **Verification battery** — holds; see F6.

## Data safety
No real-run values, dispositions, refusal text, or workspace locations
appear in this review or in the delta it examines.
