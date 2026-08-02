# Capital-Gain Distributions / Line 7a — Track 3 Independent Review

Role: Reviewer

Reviewed object: `53a9ecf86ee6f634c859704e8c068c9de9540476..75c0de90ecd271a8f552657af66206be111b0038`

Review head: `442406f31e773e6de416460161557a2122b2c335` (`Charter Track 3 presentation review`), whose parent is implementation commit `75c0de90ecd271a8f552657af66206be111b0038`. The implementation range is exactly one commit; the review-charter commit is its direct successor. The orientation SHA matched `git rev-parse HEAD`. Branch: `track/capital-gain-distributions-line7a-track3-presentation`.

## Echo and boundary

This is an author-independent review of Track 3 presentation only. The evidence ceiling is synthetic coordinator and synthetic browser evidence through the v8 package, v3 registry/release route, and `live_coordinate_run`. No real browser/workspace session, real data, computation redesign, repair implementation, Track 4 record, or ADR reopening was used.

The authoritative golden entrypoint is `tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py`: its three act logs adopt `tax.us.2025.package.core-calculations@v8` and call `live_coordinate_run`; no `RunContext` shortcut is present. Projection is zero-authority: generic resolved form-field `binds_symbol` joins exactly one atomic disposition. Numeric line 7a must be finite and categorical line 7b must use the field's fixed `"checked"` presentation. Blocked and guard-inapplicable states must be atomic and blanket-redacted: no value, stale act, checkbox state, rejected category, diagnostic, citation, accessible name, or serialized browser result may leak.

The independence constraint was observed: the committed artifact, code, goldens, manifests, and tests were read and rerun directly; no Builder thread, summary, rationale, or self-assessment was consulted. Published schemas, accepted ADRs, historical content/packages, and established v1/v6 presentation artifacts were treated as immutable history.

Stop conditions were checked: exact object/ancestry drift; accepted ADR, published schema, historical content/package, v1/v6 golden, Track-1/2 computation, contribution/admission, package-validation, resolver, Track-4, real-session, personal material, Schedule D/Form 8949/Form 1099-B, excluded-box computation, filing/transmission, unrelated UI, governance interpretation, and unattributable failures. No stop condition other than the findings below fired.

## 1. Exact object and file boundary

`git show --stat 75c0de90` and `git diff --name-status 53a9ecf..75c0de90` report exactly 13 changed files and no administrative commit inside the implementation object:

| Builder deliverable | Changed files | Measurement |
| --- | --- | --- |
| 1. Authoritative v8 presentation fixtures | `packages/sample_data/capital_gain_distributions_line7a_t3/presentation/eligible.presentation-model.v1.json`; `.../missing-authority.presentation-model.v1.json`; `.../schedule-d-required.presentation-model.v1.json`; `tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py` | All three regenerate byte-for-byte; all adoption pins are `tax.us.2025.package.core-calculations@v8`. |
| 2. Line-7a projection | `packages/derivation/presentation_projection.py`; `tests/test_capital_gain_distributions_line7a_t3_presentation.py` | Positive, blocked, guard-inapplicable, zero, citation, and numeric fail-closed paths exercised. |
| 3. Line-7b projection | `packages/derivation/presentation_projection.py`; `tests/test_capital_gain_distributions_line7a_t3_presentation.py` | Affirmative categorical, blocked, guard-inapplicable, and citation paths exercised; findings F1/F2 remain. |
| 4. Strict internal model | `packages/derivation/presentation_projection.py`; `tests/test_capital_gain_distributions_line7a_t3_presentation.py` | Committed models validate; existing strictness tests pass. |
| 5. Product-page rendering | `packages/presentation/pages/citation-walk.v1.html` | Checked accessibility path, section errors, citations, and node construction inspected. |
| 6. ADR-0046 attack set | `packages/presentation/pages/citation-walk.v1.html`; `tools/presentation_harness/examples/pages/citation-walk.v1.html`; four `cgd-*.v1.json` fixtures; new manifest; focused test | Synthetic blocked/inapplicable smuggling and sibling containment pass; negative assertions are supplemented by direct mutation/code measurements below. |
| 7. Frozen harness parity | `tools/presentation_harness/examples/pages/citation-walk.v1.html`; `tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json`; four `cgd-*.v1.json` fixtures | Both page copies retain the established provenance/substitution differences and the walk logic is aligned; all manifests pass. |
| 8. Integrated regression | `tests/test_capital_gain_distributions_line7a_t3_presentation.py`; the three goldens; generator; manifest/fixtures | Coordinator → presentation artifact → strict validation → harness path exercised. |

The remaining changed files are the four fixture JSON files:

- `tools/presentation_harness/examples/pages/citation-walk-fixtures/cgd-eligible.v1.json`
- `tools/presentation_harness/examples/pages/citation-walk-fixtures/cgd-missing-authority-smuggled.v1.json`
- `tools/presentation_harness/examples/pages/citation-walk-fixtures/cgd-schedule-d-smuggled.v1.json`
- `tools/presentation_harness/examples/pages/citation-walk-fixtures/cgd-broken-line7a.v1.json`

The implementation-range name check found no changed schema, ADR, resolver, admission, package/release/adoption, phase-state, or Track-4 path. `tools/generate_presentation_l2_golden.py` is byte-identical to the charter base. No established v1/v6 golden changed. `git diff --check` is clean.

## 2. Measurements

### Authoritative goldens and live entrypoint

The following independent exact-byte regeneration passed for `eligible`, `missing-authority`, and `schedule-d-required`:

```text
TMP_OUT=$(mktemp -d /tmp/cgd-track3-goldens.XXXXXX) python3 -c '...goldens.regenerate()...'
cmp <temporary>/eligible.presentation-model.v1.json committed/eligible.presentation-model.v1.json
cmp <temporary>/missing-authority.presentation-model.v1.json committed/missing-authority.presentation-model.v1.json
cmp <temporary>/schedule-d-required.presentation-model.v1.json committed/schedule-d-required.presentation-model.v1.json
exact-byte-regeneration=pass
```

The generator contains `live_coordinate_run` at line 48 and no `RunContext` reference. Each committed model contains the v8 adoption pin. Production-shaped outcomes are eligible line 7a published / line 7b categorical, missing authority blocked, and Schedule-D-required guard-inapplicable.

### Projection, atomic states, and strict validation

`python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation` passed 4 tests. It confirmed deterministic regeneration, the three production-shaped states, categorical no-value shape, malformed non-string categorical rejection, and missing/wrong-absent citation rejection.

The existing `tests.test_presentation_l2_integration` module passed 29 tests, including ambiguous joins, unknown dispositions, invalid numeric values, strict schema/unknown-key/duplicate-section/unsafe-string validation, resolver refusal, output confinement, unchanged caller result shape, and projector rejection with no reserved result or presentation artifact.

Direct mutation measurements used synthetic `demo.*` values:

```text
categorical finding values: "checked" ACCEPTED; "no" ACCEPTED; "unchecked" ACCEPTED; "" ACCEPTED; 1 REJECTED; None REJECTED
categorical citation: duplicate resolved citation ACCEPTED; wrong citation identity/version supplied as a resolved member ACCEPTED
numeric field citation: missing ACCEPTED; wrong identity/version ACCEPTED
```

The numeric citation result was compared at the charter base in an isolated detached worktree: the parent also accepted missing and wrong numeric field citations, and its 29 presentation integration tests passed. Thus that gap is a charter residual rather than a regression introduced by this commit; it remains an owed fail-closed measurement for the reviewed unit (F3).

### Product and frozen harness

Both HTML copies were inspected. Dynamic rendering uses `createElement`, `appendChild`, and text nodes; no dynamic `innerHTML`, `insertAdjacentHTML`, or `outerHTML` occurs. The affirmative line-7b path renders `checked` as visible text and an ARIA status, and citation buttons have keyboard focus styles and structural detail/backlink relationships. Blocked and inapplicable paths do not read their rejected `resolved.value` fields; the broken line-7a path is caught at its own section and leaves line 7b visible.

The only product/harness differences are the established provenance and substitution differences (`MODEL` versus `FIXTURE`, product/live wording versus synthetic-only wording); the render walk changes are present in both copies.

### Harness and regression commands

All required commands were run once independently:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation  # 4, OK
python3 -m unittest tests.test_presentation_l2_integration                    # 29, OK
python3 -m unittest tests.test_presentation_live_session                       # 15, OK
python3 -m unittest tests.test_presentation_live_viewing_vehicle               # 11, OK
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite # 5, OK
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator    # 9, OK
node --test tools/presentation_harness/tests/*.test.mjs                         # 34 pass, 0 fail
```

Harness manifests:

```text
citation-walk.v1.json                    # 26 pass, 0 fail, 0 error
citation-walk-production-shaped.v1.json  # 19 pass, 0 fail, 0 error
capital-gain-distributions-line7a.v1.json # 9 pass, 0 fail, 0 error
```

The new matrix covers eligible publication/citations/focus, blocked and inapplicable smuggling fixtures, broken-line-7a local alert, and healthy line-7b sibling survival. Existing baseline manifests remain unchanged.

Safety and boundary commands:

```text
python3 tools/governance_lint.py                    # governance lint: conformant
python3 tools/envelope_scan.py --range main..HEAD   # clean
git diff --check 53a9ecf..75c0de90                  # clean
```

No real-data run was performed. The committed values, IDs, paths, and browser fixtures are synthetic or repository content; the envelope scan found no personal value, credential, absolute machine path, or private output.

## 3. Findings

### F1 — Arbitrary categorical source values are accepted as affirmative `checked`

The charter requires line 7b to accept only the field's declared fixed categorical `"checked"` presentation and to fail closed for malformed categorical publications. In `packages/derivation/presentation_projection.py:204-214`, the categorical branch checks only `isinstance(finding.get("value"), str)` and then emits `published_categorical`; it does not require the source value to be `"checked"`. The renderer subsequently always displays `checked` at `packages/presentation/pages/citation-walk.v1.html:290-298`.

Reproduction:

```text
python3 - <<'PY'
from tests.test_capital_gain_distributions_line7a_t3_presentation import _categorical_model
for value in ("checked", "no", "unchecked", "", 1, None):
    ...
PY

"checked" ACCEPTED
"no" ACCEPTED
"unchecked" ACCEPTED
"" ACCEPTED
1 REJECTED
None REJECTED
```

This is introduced by the reviewed commit's categorical projection branch. It violates the Track 3 line-7b projection clause and the required malformed-categorical fail-closed measurement. No repair design is proposed.

### F2 — Categorical field citation identity is not unique or exact

The charter requires missing, duplicate, wrong-version, and wrong-identity field citations to fail closed. The new citation index at `packages/derivation/presentation_projection.py:323-327` is a dict comprehension that silently overwrites duplicate `(id, version)` members. The exactness check at lines 239-248 only checks membership, so a wrong citation is accepted when that wrong citation is present in the resolved members. The categorical check is only invoked at lines 341-342.

Reproduction with synthetic members:

```text
categorical citation: duplicate resolved citation       ACCEPTED
categorical citation: wrong identity/version present    ACCEPTED
```

This is introduced by the reviewed commit and violates the charter's exact citation-identity and duplicate-citation measurements. No repair design is proposed.

### F3 — Numeric line-7a uncited/wrong field citations reach the artifact

The charter requires an uncited or malformed published line 7a to fail closed before a presentation artifact is written. Numeric fields take the path at `packages/derivation/presentation_projection.py:204-232`; the resolved field citation is neither required nor checked there. The strict validator also validates only that the field is a form-field citizen, not that its citation is present or resolved. A synthetic numeric projection accepted both a missing field citation and a wrong identity/version.

The isolated parent comparison reproduced the same acceptance on `53a9ecf`, so this is not introduced by the reviewed commit. It nevertheless means the exact Track 3 charter measurement does not pass for this unit. No repair design is proposed; foreman/owner disposition is required.

## Verdict

**NOT READY**

F1 and F2 are implementation-range findings. F3 is a pre-existing charter residual confirmed by base comparison. The focused runtime, lifecycle, resolver, synthetic browser, golden, parity, and safety checks are otherwise green. Findings recommend no scope expansion or repair design; custody returns to the foreman after this record is committed.
