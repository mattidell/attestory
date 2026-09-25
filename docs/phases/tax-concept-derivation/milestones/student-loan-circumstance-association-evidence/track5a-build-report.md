# Track 5a build report — subject and relationship declarations (ADR 0076 Parts 1–2, declarative half)

Builder unit. Scope: `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/charter-track5a-subject-and-relationship-declarations.md`.
Not committed; left for foreman review per the charter's hand-off.

## Schema files (new, published)

### `packages/schemas/derivation/rule-artifact.v11.schema.json`

Byte-for-byte copy of v10's grammar (`$id: derivation/rule-artifact.v11`, `schema` const
`rule-artifact.v11`), plus:

- `subject` (required): `#/$defs/exact_pin` — the same `{id, version}` shape v10 already uses for
  `composition`/`citations` exact pins.
- `joined` (optional): `#/$defs/exact_pin`.
- `direction` (optional): `enum: [joined_contains_subject, subject_contains_joined]`.
- `dependentRequired: {"joined": ["direction"], "direction": ["joined"]}` — present-together /
  absent-together is schema-enforced (draft 2020-12 supports `dependentRequired`; verified with
  `jsonschema.Draft202012Validator.check_schema` and instance-level round-trips).
- No `wording`, `lineNote`, or `link_count` alternative — those are the second successor per the
  publication plan.

### `packages/schemas/derivation/artifact-package.v32.schema.json`

v31 plus `rule-artifact.v11` in the `$defs.member.schema` enum, the top-level
`admitted_schemas` items enum, and the matching `allOf` conditional (`members` contains a
`rule-artifact.v11` citizen ⇒ `admitted_schemas` contains `rule-artifact.v11`) — the identical
pattern v31 used to admit v10 over v30 (confirmed by diffing v30→v31 first). No package-level
subject map. `$id`, `schema` const, `title`, `description` updated; nothing else changed.

### `packages/schemas/derivation/published.json`

Two entries appended via `packages.kernel.schema_registry.write_manifest`:
`rule-artifact.v11.schema.json` and `artifact-package.v32.schema.json`. `git diff` on this file
shows exactly those two added lines; no existing entry's checksum changed.

## `packages/derivation/package_validation.py`

**Admission (v11 supported wherever v10 is), each is v10's set/branch plus `rule-artifact.v11`:**

- `_families_reached` (schema membership test, ~line 64).
- `_RULE_ARTIFACT_SCHEMAS` frozenset (~line 200) — this alone propagates to every call site that
  already reads it: role-mismatch checks, `CLOSURE_MISSING_PARAMETER`/E14.2 pin checks, force-declare
  composition, composition-obligation producer lookup, `_link_coverage_issues`'s reduction-publisher
  search, the collect-target guard loop.
- `_SUPPORTED_SEMANTIC_SCHEMAS` frozenset (~line 358) — otherwise a v11 member is rejected
  `MEMBER_SCHEMA_UNSUPPORTED` before any of the above runs.
- `compile_validation_graph` and `check_validation_graph`'s schema membership tests (~lines 897,
  968) — the ADR-0066 family-validation-prerequisite synthesis.
- The declared-refs-outside-`requires` set inside the `MEMBER_UNREACHABLE` BFS (~line 2220).
- The `link_coverage` edge block inside that same BFS (~line 2269): `citizen["schema"] in
  ("rule-artifact.v10", "rule-artifact.v11")`.
- The CDS/`category_literal` `{yes,no}`-domain check (~line 2993) and the `field`-ref load-time
  check (~line 3047).
- `_link_coverage_issues` (~line 602): `citizen.get("schema") not in ("rule-artifact.v10",
  "rule-artifact.v11")`. v10's shape checks (single `link_coverage` node in `value`, not in `when`,
  `links`/`reductions` distinct strings, `links` on the fact surface, `reductions` the sole other
  producer, `empty.parameter` an exact package parameter) now run for v11 identically.

**New checks (v11-specific), `_subject_relationship_issues`, called right after
`_link_coverage_issues`:**

For every `rule-artifact.v11` citizen in the resolved corpus:

1. `subject` must resolve, by exact `(id, version)`, to a `fact-type.v2` package member — else
   **`RULE_SUBJECT_UNRESOLVED`**.
2. If `joined` is present it must resolve the same way — else **`RULE_JOINED_UNRESOLVED`**.
3. If both resolve and `direction` is one of the two named values, containment is checked by
   `identity_keys` **names only** (no value reads): `joined_contains_subject` requires subject-names
   ⊆ joined-names; `subject_contains_joined` requires joined-names ⊆ subject-names. Anything short of
   full containment — including one shared name — fails: **`RULE_RELATIONSHIP_NOT_CONTAINED`**.
4. Every `link_coverage` node in the rule's `value` must sit on a rule that declares `joined` equal
   to the node's `links` fact type and `direction: joined_contains_subject`; any other combination
   (wrong direction, wrong `joined` type, or no `joined`/`direction` at all) is
   **`LINK_COVERAGE_RELATIONSHIP_INVALID`**.

A new helper, `_exact_pin_key(pin) -> tuple[str, str] | None`, resolves a `{id, version}` pin to a
typed key or `None` for a malformed pin, so `mypy` can see the `fact_types_by_key` lookup is
`tuple[str, str]`-keyed throughout (this was the one thing `mypy` flagged on first pass; fixed
before final verification).

**New issue codes:** `RULE_SUBJECT_UNRESOLVED`, `RULE_JOINED_UNRESOLVED`,
`RULE_RELATIONSHIP_NOT_CONTAINED`, `LINK_COVERAGE_RELATIONSHIP_INVALID`.

## `packages/derivation/live.py`

`_resolved_run_material`'s `rules` schema-membership set gets `rule-artifact.v11` alongside v10
(admission only). Everything downstream of that list (`collect_names`,
`_iter_link_coverage_link_types`-driven `emission_only_names`) already walks `value`/`when`
structurally regardless of the schema string, so a v11 rule with a `link_coverage` node gets the
same `emission_only_names` treatment as a v10 one automatically once it is in `rules`.

## `packages/derivation/marshal.py`

`_rule_required_symbols`'s declared-refs-outside-`requires` schema set gets `rule-artifact.v11`
alongside v10 — `subject`/`joined`/`direction` are exact pins and an enum, not `ref` nodes, so the
existing walk is unchanged in behaviour.

## `packages/derivation/authorization_closure.py`

- `_RULE_ARTIFACT_SCHEMAS` and `_RULE_DECLARED_REFS_OUTSIDE_REQUIRES` frozensets both get
  `rule-artifact.v11`.
- The `link_coverage` edge block: `if schema in ("rule-artifact.v10", "rule-artifact.v11"):` — same
  reduction-publisher / link-fact-type / `empty.parameter` edges as v10.
- Module docstring updated (v1–v10 → v1–v11; notes that `subject`/`joined`/`direction` add no edge
  here, matching Track 5b's scheduling being out of scope).

## Tests — `tests/derivation/test_subject_relationship_declarations.py` (22 tests, all new)

Every behaviour test builds a `rule-artifact.v11` rule on an `artifact-package.v32` package (the
ADR's acceptance condition). `tests/test_sli_g2_binding_probe.py` and
`tests/derivation/test_link_coverage_contract.py` are read for fixtures/identity-key values but not
edited.

**`RuleArtifactV11Schema`** (schema shape):
- `test_worked_shape_validates` — a minimal valid v11 rule (subject only) validates.
- `test_missing_subject_is_rejected` — no `subject` → `SchemaValidationError`.
- `test_joined_without_direction_is_rejected` / `test_direction_without_joined_is_rejected` — each
  half alone → `SchemaValidationError` (`dependentRequired`).
- `test_unknown_direction_is_rejected` — `direction: "sideways"` → `SchemaValidationError`.
- `test_v11_rejected_as_member_of_v31_accepted_on_v32` — the same rule+fact-type pair: package-level
  `PACKAGE_SCHEMA_INVALID` on `artifact-package.v31`, `result.ok` on `artifact-package.v32`.

**`PinResolution`** (unresolvable pins):
- `test_unresolvable_subject_is_rejected` — subject id not a package member → `RULE_SUBJECT_UNRESOLVED`.
- `test_unresolvable_joined_is_rejected` — joined id not a package member → `RULE_JOINED_UNRESOLVED`.
- `test_stale_version_does_not_resolve` — subject id present but at a different published version →
  `RULE_SUBJECT_UNRESOLVED` (id-only match is not resolution).

**`RelationshipKeyNameTable`** (ADR Part 2's key-name table, both directions, as declared
`fact-type.v2` `identity_keys`):
- `test_tax_year_and_borrowing_vs_statement_identity_both_reject`.
- `test_shared_statement_id_only_both_reject` (statement + borrowing on the link, no lender/tax-year).
- `test_lender_tax_year_and_borrowing_both_reject`.
- `test_full_statement_identity_plus_borrowing_only_joined_contains_subject` — accepts
  `joined_contains_subject` only.
- `test_full_enrolment_vs_financing_only_subject_contains_joined` — accepts `subject_contains_joined`
  only.
- `test_period_only_enrolment_subject_contains_joined_accepts_this_is_adr_residual_1` — asserts the
  weak-declaration pass explicitly, named and docstring'd as ADR residual 1, not a defect in this
  check.

**`LinkCoverageRelationshipRequirement`**:
- `test_wrong_direction_is_rejected`, `test_wrong_joined_type_is_rejected`,
  `test_no_joined_is_rejected` — each → `LINK_COVERAGE_RELATIONSHIP_INVALID`.
- `test_right_pair_is_accepted` — `joined` = the node's `links` type, `direction:
  joined_contains_subject` → `result.ok`, no `LINK_COVERAGE_RELATIONSHIP_INVALID`.

**`V10Unaffected`**:
- `test_existing_v10_worked_example_still_validates` — re-runs
  `test_link_coverage_contract._base_parts()`/`_validate` unchanged; still `result.ok`.

**`AdmissionSetsTreatV11LikeV10`**:
- `test_resolved_run_material_names_the_v11_rule_and_emits_the_link_type` — a v11 coverage rule with
  a `link_coverage` node appears in `_resolved_run_material(...)[0]` (`rules`) and produces
  `emission_only_names == (LINKS,)`, `LINKS`/`REDUCTIONS` excluded from `collect_names`, exactly as
  the v10 fixture does.
- `test_authorization_closure_gives_v11_the_same_edges_as_v10` — same rule body, run once as
  `rule-artifact.v10` and once as `rule-artifact.v11` (subject/joined/direction stripped for the v10
  run); `build_dependency_edges` returns the identical edge set (reduction-publisher id, links
  fact-type id, parameter id) both times.

## Verification tails (verbatim)

```
$ python3 -m pytest -n auto -q
...
FAILED tests/test_later_year_basis_reuse_track0.py::C8bCandidateAgainstCurrentPackageValidation::test_rule_artifact_v7_exists_only_in_the_unguarded_generation
1 failed, 2244 passed, 20 skipped, 4422 subtests passed in 123.07s (0:02:03)
```

```
$ python3 -m pytest tests/test_schema_registry.py -q
..............                                                           [100%]
14 passed in 1.34s
```

```
$ python3 -m pytest tests/derivation/test_subject_relationship_declarations.py tests/derivation/test_link_coverage_contract.py tests/derivation/test_link_coverage_admission.py tests/derivation/test_link_coverage_runtime.py tests/test_sli_g2_binding_probe.py tests/derivation/test_attachment_rule_v11.py -q
..uu.....uu...........u.u.uu......u.u.u..uuu.uu...u.uu.u.uu.uu.u...u..u.
uu.....uu....u.uuuu..u..uu..u.u.....u.........u...........u.....uuuuuu..
u..uuuuuuuu..u..uuuuuuu..........
110 passed, 67 subtests passed in 3.16s
```

```
$ python3 -m mypy
Success: no issues found in 278 source files
```

```
$ python3 tools/governance_lint.py
governance lint: conformant
```

```
$ git diff --check
(no output — clean)
```

```
$ git diff packages/schemas/derivation/published.json
@@ -27,6 +27,7 @@
   "artifact-package.v3.schema.json": "74ba8b11fe05278ce352ede39899202b27c9759f06546549383126a2cae12b41",
   "artifact-package.v30.schema.json": "04562ef7a2ae234d7076cf431c2927c794b1808cac769799df8e3bd1b6a2a83c",
   "artifact-package.v31.schema.json": "da1ddefe27a2f8b05fde5039491c8268e6334a35c4404228cc47564d26e59f1c",
+  "artifact-package.v32.schema.json": "aa9f885ea40d55913a5271bc207b861c7e62e80fa60d481f72da857e7bd3fc23",
   "artifact-package.v4.schema.json": "7b820d4d1d3bd19e8f37f2c69a9d74f809304c07c126b1ad572f95f1549aad54",
   "artifact-package.v5.schema.json": "1e857d177f73d0b9614c4bee2c1856e1a7069d54efa2fc8666e4b0f4e9756698",
   "artifact-package.v6.schema.json": "1012e48f9800d224b05d6f7dbef81a95beb79bc64f68695b20cd3bee097e7d4a",
@@ -59,6 +60,7 @@
   "release-registry.v1.schema.json": "c81e432be13e81d038598236df2670c788cec7b9506fbfd3a0142993f44e6be0",
   "rule-artifact.v1.schema.json": "9a98d3f4f7e1d1d842291db2f28291c3b61812a64a4ed7069ab23950ca458118",
   "rule-artifact.v10.schema.json": "dace417ff64f5447c93d633f9b3314d930bd2c1156ba344cb477e4e930b8a03f",
+  "rule-artifact.v11.schema.json": "f8cab29c790466072064ccae625f740b61360360ace3b87d2f61e267206b8cd3",
   "rule-artifact.v2.schema.json": "aa6af201ffc2e52a50d2347b508f94643ffc61e37027b36152a50d0d8fc69230",
   "rule-artifact.v3.schema.json": "affb1fe3780988d438fe84ce36e49c397986d9ade64356a675d554e49d49d1b9",
   "rule-artifact.v4.schema.json": "5170efb918884acd2deca68986262eba301fbf232a5ea6c0633708e41cc27660",
```

Only two lines added; no existing checksum changed.

## Stop condition met

**"An existing test fails for any reason"** — `tests/test_later_year_basis_reuse_track0.py::
C8bCandidateAgainstCurrentPackageValidation::test_rule_artifact_v7_exists_only_in_the_unguarded_generation`
fails after `artifact-package.v32.schema.json` is added, and only after that. That test is an
out-of-scope, exhaustive-enumeration regression test recording which published
`artifact-package.vN` schema files' *bytes* happen to contain the literal substring
`"rule-artifact.v7"` (a proxy for "which package generations are outside the collect-target guard's
v3–v17 allowlist and therefore never bound a `rule-artifact.v7` collect check"). It currently asserts
that list is exactly `[v26, v28, v31]`.

`artifact-package.v32` is v31's full byte content plus one addition (per the charter: "v32 — v31
plus `rule-artifact.v11` in the member schema enum"), so it necessarily still contains
`rule-artifact.v7` in its `admitted_schemas`/`member.schema` enums, extending the true list to
`[v26, v28, v31, v32]`. This is not a defect introduced by an implementation choice — any
byte-for-byte-additive v32 built from v31, as the charter specifies, reproduces it. I did not edit
`tests/test_later_year_basis_reuse_track0.py` (not an assigned path) to fix the assertion, per the
charter's explicit stop condition and the "leave `docs/` and other in-flight foreman files alone"
posture. Confirmed by isolating the failure: it is the sole failure in the full suite both before and
after the `mypy` fix, and it does not fail on `main` before this change (the only file it globs is
`packages/schemas/derivation/artifact-package.v*.schema.json`, and `artifact-package.v32.schema.json`
did not exist before this unit).

Flagging for the foreman/owner: either (a) accept this as an expected, correctly-anticipated
enumeration update and let the review round add `"artifact-package.v32.schema.json"` to that list, or
(b) decide the recorded-gap test should generalize to "the highest N with rule-artifact.v7 present at
or above the last named version" rather than an exact list, which is a decision about that test's own
contract, not this unit's schema content.

## Everything else in the charter's stop-condition list

Not triggered: no published schema file or existing `published.json` entry changed (see diff above);
no check needed runtime information; the ADR was not ambiguous on any point this unit had to decide
(the containment direction, the `link_coverage` requirement, and the pin-resolution requirement are
all stated in ADR 0076 Part 2 and the charter without a gap this unit had to fill).
