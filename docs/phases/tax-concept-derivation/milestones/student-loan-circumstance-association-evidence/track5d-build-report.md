# Track 5d build report — exact version authority

Branch `milestone/student-loan-circumstance-association`, read at `7f579294` (the charter commit). Not committed. `package-lock.json` was already untracked and was not touched. No path outside the assigned files was edited except this report.

Stage 1 is implemented. Stage 2 is characterised and not implemented. Both runners share `_Run` and the evaluator; no test needed different code for `run` and `run_reference`.

## Reproductions, before the fix

Each case below is a package that resolves both versions, through `validate_package` → `_resolved_run_material` → `marshal_run_context` → `run` and `run_reference`. The first run failed on the defect. Two fixtures were corrected before that count (an ordinary rule has no `when` argument; a `link_coverage` rule must declare `joined` equal to its links type). After that correction, and still before any product change, those cases failed as follows.

- **Default parameter, both present.** Fact type pins parameter v1 (`from-v1`); the package also resolves v2 (`from-v2`). With v2 declared last, both the ordinary rule and the declared-subject rule published `from-v2` under a parameter pin of v1. With v1 declared last, the same assertion passed by accident.
- **Pinned parameter version absent.** Only v2 is resolved. Validation accepted the package (`BINDING_DEFAULT_ABSENT` checks the parameter id, not the version). Both runners published `from-v2` with a parameter pin whose version is v1.
- **Empty `link_coverage` parameter.** No link rows. The node pins v1 (`10`); v2 is `99`. With v2 declared last the subject rule blocked `DEPENDENCY_INVALID` on the parameter id, even though v1 was in the package.
- **Categorical input.** Binding and `category_literal` pin v1, value `a`, v1 enum `["a","b"]`, v2 enum `["x","y"]`. With v2 last, the comparison blocked `DEPENDENCY_INVALID` missing `a`.
- **Two domains, one id.** Literals of v1 and v2 both valued `yes`, and `yes` is in both enums. Both orders published `true`. They were treated as one domain.
- **Literal borrows a sibling enum.** The literal pins v2, and v2 has no enum. v1's enum contains `a`. Both orders published `true`.
- **`collect_categorical_all_equal`.** Rows are `a`, legal only in the literal's v1. With v2 last, the rule did not publish.
- **`optional_default` symbol's domain.** The binding pins v1 and the default value is `a`. With v2's enum last, the comparison did not publish.
- **Field-ref, reviewer's case.** v1 scalar, v2 object with `amount`, binding pins v2. With v1 declared first, validation rejected `FIELD_REF_NOT_OBJECT`. With the binding pinning v1 and v2 declared first, validation accepted.
- **Yes/no check.** Binding pins the `{yes, no}` version. With the open-string version declared first, validation rejected `CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO`. With the binding pinning the open string and the yes/no version declared first, validation accepted.
- **Derived categorical, several versions.** Both enums contain `yes`. Both orders published `true` for the downstream comparison. The derived finding has no fact type; the ref used the symbol name and whichever domain was last.
- **Unversioned `parameter`.** v1 value `1`, v2 value `2`. v1 last published `1` and pinned v1. v2 last published `2` and pinned v2.

Zero-subject tests passed on that first run. They describe today's behaviour: no publication, no disposition, and the downstream rule blocks `DEPENDENCY_ABSENT`. They were not a defect to fix.

## Changes

- `packages/derivation/live.py`, `_parameters_by_exact_version`, called from `_resolved_run_material`. Every `parameter-declaration.v1` is stored by `(id, version)`. The id key is set only when that id has one version. `marshal_run_context`'s `dict(parameters)` keeps the index, so marshalling did not need a change.
- `packages/derivation/evaluator.py`
  - `parameter_exact`, `parameter_unversioned`, `parameter_version_count`. An exact read never returns a sibling. An unversioned read returns the citizen only when there is one version.
  - `AccessLog.parameter_versions`. The version actually read, so the pin is not taken from an id-keyed slot.
  - `evaluate` for `parameter`: one version is used and recorded; several versions raise `DEPENDENCY_INVALID` and do not select; none raises `DEPENDENCY_ABSENT`.
  - `_empty_coverage_parameter`: the node's `(id, version)`. A sibling with a different version is `DEPENDENCY_INVALID`. A missing id is `DEPENDENCY_ABSENT`.
  - `_range_lookup` and `_bracket_fold`: same unversioned rule as `parameter`. One version is used and its version is recorded. Several block rather than select.
  - `categorical_domain_key`, `_resolve_categorical_domain`, `_validate_categorical_value`, `_eval_categorical_operand`. Domains are stored by `(id, version)`. One resolved version keeps the bare id as the domain identity, so existing comparisons still agree. Two versions are different identities. A named version that is absent while a sibling exists raises `CATEGORICAL_DOMAIN_MISMATCH` and does not use the sibling. A `category_literal` carries its own version. A `ref` carries `symbol_fact_versions` when the symbol has one; otherwise the symbol name is the fact-type id, and several versions of that id block.
  - `collect_categorical_all_equal` checks each row against the literal's domain, not against another version of the same id.
  - `Environment.symbol_fact_versions`.
- `packages/derivation/runner.py`, `_Run.__init__`. Categorical enums are stored with `categorical_domain_key`. The bare id is also stored only when that id has one enum version. An input symbol records its binding's version. An `optional_default` symbol records the binding's version, and the value is `parameter_exact` of the fact type's parameter pin. `dependency_pins_for_access` pins `parameter_versions` first and does not read `parameters[id]["version"]` for an id that has no single citizen. `env` passes the version map.
- `packages/derivation/subject_dispatch.py`, `_optional_default`. Same exact parameter read. `_fact_version_of` and the per-subject `Environment` carry the binding version for required symbols, the rule's `subject` version for the subject symbol, and the rule's `joined` version for the joined symbol. The publication symbol stays `publishes|fact_id`.
- `packages/derivation/package_validation.py`, `_fact_type_for_pin`, `check_field_ref_bindings`, and the conditional-dependency yes/no check. A binding's `(id, version)` is the fact type that is read. A missing exact version is not replaced by `fact_types_by_id`. Callers that still pass only an id-keyed map are unchanged.

## Tests

`tests/derivation/test_exact_version_authority.py`. Nineteen tests. Each behaviour test runs both runners. "Both orders" means the two citizens of one id are package members in either order.

| Test | Value | Pins |
| --- | --- | --- |
| `ExactDefaultParameter.test_ordinary_rule_both_orders` | Echo is `from-v1`, not `from-v2`. | The manufactured default finding's only parameter pin is `(param, v1)`. The echo's input pin is that finding, origin `declared_default`. |
| `ExactDefaultParameter.test_declared_subject_rule_both_orders` | Same value, on the suffixed subject symbol. | Same parameter pin on the default finding. |
| `UnavailableExactParameterDoesNotBorrow` (ordinary and subject) | No publication is `from-v2`. | No parameter pin of v1 or v2. The consumer's disposition is `DEPENDENCY_ABSENT`. |
| `EmptyCoverageUsesThePinnedParameter.test_both_orders_publish_v1_and_pin_v1` | Subject publication is `10`, not `99`. | That finding's parameter pins include `(param, v1)` and not v2. |
| `test_pinned_input_matches_its_own_literal_both_orders` | Publication is `true`. | The only input pin is the current finding of value `a`. |
| `test_two_versions_of_one_id_do_not_compare_equal` | No publication of `true`. | Disposition code `CATEGORICAL_DOMAIN_MISMATCH`. The literals name no input finding. |
| `test_literal_does_not_borrow_a_sibling_enum` | No publication of `true`. | The rule is blocked. v1's enum is not used for a v2 literal. |
| `test_collect_rows_use_the_literal_version` | Publication is `true` for a row `a` that only v1 allows. | No parameter pin. The row is read as a collect source, not as the sibling domain. |
| `test_optional_default_symbol_carries_the_binding_version` | Publication is `true` for default value `a` against a v1 literal. | The comparison's input is the v1 default, not v2's enum. |
| `test_binding_pinned_to_v2_is_accepted_and_reads_amount` | Publication is `10`, both orders. | The only input pin is the object finding. |
| `test_binding_pinned_to_v1_scalar_is_rejected_both_orders` | Validation rejects; there is no run. | Code `FIELD_REF_NOT_OBJECT` in both orders. |
| `test_yes_no_check_uses_the_binding_version` | Binding v2: publication is `yes`. Binding v1: validation rejects. | The accept path's value is the bound finding. Reject code `CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO`. |
| `test_no_finding_publishes_nothing_and_the_consumer_blocks` | No publications. | No disposition for the subject rule. Downstream code `DEPENDENCY_ABSENT`, missing the published symbol. |
| `test_each_current_subject_reaches_execution` | Each subject symbol's value is `executed`. | Two `published` dispositions for the subject rule. |
| `test_one_version_keeps_the_symbol_name_fallback` | Producer value `yes`. Consumer value `true`. | The producer finding has no `fact_type`. The consumer's input pin is that finding. |
| `test_several_versions_block_instead_of_taking_the_last` | Producer still `yes`. Consumer does not publish `true`, both orders. | Producer finding has no `fact_type`. Consumer code `CATEGORICAL_DOMAIN_MISMATCH`. |
| `test_one_version_is_used_and_pinned` | Publication is `1`. | Parameter pin is `(param, v1)`. |
| `test_two_versions_block_rather_than_select` | Neither `1` nor `2` is published, both orders. | Code `DEPENDENCY_INVALID`, missing the parameter id. No version is selected, so no parameter pin is written. |

## Chain of authority, after the change

1. **Parameter map** (`_parameters_by_exact_version`). The citizen used for a named version is that version's citizen. The id slot exists only for an id with one version, which is what every older id-keyed reader still sees. Two versions leave no id slot, so an id-keyed read cannot borrow.
2. **Ordinary `optional_default`** (`_Run.__init__`). The fact type's parameter pin is `parameter_exact`. The finding value is that citizen's `values`. The pin written beside it is the same `(id, version)`. The symbol's fact-type version is the binding's version, which is what a later categorical `ref` validates against.
3. **Per-subject `optional_default`** (`subject_dispatch._optional_default`). Same exact read and the same pin. A missing exact version returns None; the subject then blocks `DEPENDENCY_ABSENT` instead of publishing the sibling.
4. **Empty `link_coverage` parameter** (`_empty_coverage_parameter`). Reached from per-subject dispatch, which is the path that binds `keyed_sources`. An ordinary rule still blocks `link-coverage-scope-unbound` before this function, because its environment has no keyed slots. On the subject path the node's version is the value and the recorded pin. A sibling does not satisfy the node.
5. **Unversioned `parameter`, `range_lookup`, `bracket_fold`.** They name no version. One resolved version: that value, and the pin is that citizen's version. Several: `DEPENDENCY_INVALID`, nothing selected, nothing pinned. This is the stage-1 block for C2, applied to the same unversioned parameter read the table ops already were.
6. **`dependency_pins_for_access`.** Pins come from `parameter_versions` recorded at the read. It no longer does `parameters[id]["version"]` when that slot is absent or ambiguous.
7. **Categorical domains** (`_Run.__init__`, `_resolve_categorical_domain`). Each enum is stored at `(id, version)`. The bare id is an alias only for a single version. `category_literal` validates and identifies itself by its own pin. `ref` uses the symbol's recorded version when it has one. `categorical_compare` treats two versions as different domains even when the strings are equal. `collect_categorical_all_equal` checks rows against the literal's domain only.
8. **Input and default symbols.** A binding's input records `(id, version)` from the binding. An `optional_default` symbol records the binding's version, not "whatever enum was last". A subject symbol records the rule's `subject` pin; a joined symbol records the rule's `joined` pin.
9. **Plain `ref` validation** (`evaluate`). If the symbol is in `symbol_fact_types`, the value is checked against that symbol's version. A derived symbol is not in that map, so a plain `ref` still does not invent a domain. The categorical operand is the path that falls back to the symbol name.
10. **Field-ref validation** (`check_field_ref_bindings`). The binding's `(id, version)` supplies `value_schema`. v1 scalar and v2 object no longer trade acceptance with declaration order. Direct callers that pass only an id map still use that map.
11. **Yes/no validation.** The member's binding pin, not the first fact type of that id, is the domain that must be `{yes, no}`.
12. **Not this track.** `_attachment_threshold_trigger` still does `parameters.get(threshold_pin["id"])` and then pins `threshold_pin["version"]`. Executed against a two-version map from `_parameters_by_exact_version`: the id slot is None, `parameter_exact` of v1 is `10`, and the trigger returns blocked with `DEPENDENCY_ABSENT` on the id. It does not borrow v2, and it also does not use the v1 it was given. No content package resolves two versions of one parameter, and a single version still occupies the id slot, so the full suite is unchanged. Left as found.
13. **Not this track.** `BINDING_DEFAULT_ABSENT` still requires the parameter id, not `(id, version)`. A package that pins v1 and resolves only v2 still validates. Runtime then blocks, which is the test above. The check was not one of the two validation checks this charter names.
14. **`_fact_type_of`.** Still returns a fact-type id, or the symbol name when nothing has typed it. Keyed publications are still stored as `publishes|fact_id` and still carry no fact type. That is C1, below, not a stage-1 typing change.

## Stage 2

### C1 — derived categorical results

Today a derived finding has no fact type. `symbol_fact_types` is not set when the finding is published. A later categorical `ref` uses `symbol_fact_types.get(name, name)`, so the symbol name is the fact-type id. `_fact_type_of` does the same for a symbol with no binding: keyed same-run symbols are not given a type.

Stage 1 keeps that fallback when exactly one version of that id is resolved, and blocks `CATEGORICAL_DOMAIN_MISMATCH` when several are. It does not type the value from the `category_literal` that produced it, and it does not require a declared output type.

Content that relies on the fallback, scanned across package files under `packages/content` (40 packages; none of them resolve two versions of one fact type or one parameter): in `package.core-calculations.v38`, three rules categorically ref a symbol that is published and not input-bound, and that symbol is also a fact type in the package, at one version:

- `tax.us.2025.rule.form1040-line16`
- `tax.us.2025.rule.form1040-line7b`
- `tax.us.2025.rule.selected-preferential-base`

The symbol is `tax.us.2025.schedule-d-required.conclusion`. One version means stage 1 still checks the derived `yes`/`no` against that fact type's enum. No other latest package had such a pair.

Options, not implemented:

- Type the derived value, in the run only, from the `category_literal` actually evaluated. A downstream `ref` would then carry that evaluation's domain. A value not produced by a literal would still have no domain. This does not change a published schema.
- Require a declared output type on the rule. That is a schema successor. Existing derived findings would stay untyped until migrated. The three rules above would name `tax.us.2025.schedule-d-required.conclusion` explicitly instead of matching it by symbol.

### C2 — unversioned `parameter`

The `parameter` op names an id and no version. No content package resolves two versions of one parameter (same scan; the foreman's count of content fact types is unchanged by this pass).

Stage 1 blocks at runtime with `DEPENDENCY_INVALID` when a package resolves several versions, and does not pick one. One version is still that version's value and pin.

Options, not implemented:

- Validation rejects the package as ambiguous when an unversioned `parameter` (or table id) is read and the package resolves more than one version. The package never runs. A package that does not read the id can still carry both versions for versioned pins such as `optional_default` and `link_coverage.empty`.
- Something selects a version: highest version, first declaration, or an explicit package default. Any of those makes declaration order or an unstated rule part of the answer, which is what this track is removing for pins that already name a version. It would also have to say which version the pin records.

## Stop conditions

- No published schema and no ADR was edited.
- No existing test failed. The full run is 2300 passed, 20 skipped. The previous full run recorded on this branch was 2281 passed and the same 20 skipped; the difference is these 19 tests. `tests/test_sli_g2_binding_probe.py` was not edited.
- `run` and `run_reference` did not need different code.
- The attachment-threshold consumer above is outside the named consumers. Its consequence was executed and it was not changed.
- Zero-subject rules got tests only. No new disposition.

## Verification

```
$ python3 -m pytest -n auto -q
2300 passed, 20 skipped, 4450 subtests passed in 123.62s (0:02:03)
```

```
$ python3 -m mypy
Success: no issues found in 282 source files
```

```
$ python3 tools/governance_lint.py
governance lint: conformant
```

```
$ git diff --check
(no output)
```

```
$ git status --short
 M packages/derivation/evaluator.py
 M packages/derivation/live.py
 M packages/derivation/package_validation.py
 M packages/derivation/runner.py
 M packages/derivation/subject_dispatch.py
?? package-lock.json
?? tests/derivation/test_exact_version_authority.py
```

`package-lock.json` is the pre-existing untracked file. This report is the remaining untracked path written for hand-off; it is not in the status above because that status was taken before the report was written.

## Round 2

The attachment threshold is on the same parameter chain. The `\x00` sentinel is gone. The exact index is a field on the run and on the environment, carried through marshalling. Not committed.

### Reproductions, before this round's change

`AttachmentThresholdUsesThePinnedParameter`, live path, both runners. v1's value is `10`, v2's is `1000`, the subtotal is `50`. Over v1 the attachment is required and then blocks on the absent answer. Over v2 it would be inapplicable. The pin is whatever version was actually used.

- Both declaration orders, two versions resolved: the disposition blocked `DEPENDENCY_ABSENT` missing the parameter id, not the answer. The named v1 was in the package. The id-keyed map held only the `\x00` sentinel, so `parameters.get(id)` was empty.
- Only v2 resolved, pin names v1: the disposition was `inapplicable` (50 is not over 1000) and the parameter pin still said v1. v2's value was used under a v1 pin.
- The same package's parameter map contained the `\x00` key. Its value was the version index, not a parameter citizen.

### Changes

- `packages/derivation/runner.py`, `_attachment_threshold_trigger`. The threshold is `parameter_exact` of `threshold_parameter`'s `(id, version)`. Absent exact version blocks `DEPENDENCY_ABSENT` on that id. The value compared is that citizen's `values`. The pin remains the named version, which is now the version that was read. A hand-built `ctx` with no `parameter_index` attribute still resolves.
- `packages/derivation/live.py`, `_parameters_by_exact_version` and `_ResolvedRunMaterial`. The id-keyed dict contains a parameter citizen only when that id has one version, and nothing else. Every version is on `material.parameter_index` (`id -> version -> citizen`). `live_coordinate_run` and `live_run` pass that index into marshalling.
- `packages/derivation/marshal.py`, `marshal_run_context` and `marshal_live_run_context`. New optional `parameter_index`, default empty, copied onto `RunContext`. Existing callers that do not pass it are unchanged. The live-path tests need this: `_resolved_run_material` no longer hides the index inside the parameters dict, and `dict(parameters)` would drop anything that was not a key.
- `packages/derivation/runner.py`, `RunContext.parameter_index`, default empty. `env` copies it onto the environment. `optional_default` and `dependency_pins_for_access` pass it into the lookups.
- `packages/derivation/evaluator.py`. `EXACT_PARAMETER_INDEX` is removed. `Environment.parameter_index` defaults empty, so existing `Environment(...)` constructions keep working. `parameter_exact`, `parameter_unversioned`, and `parameter_version_count` take that index. An id the index lists is never answered by a sibling or by the id slot. An id the index does not list still uses the single id-keyed citizen. A hand-built citizen that has `values` and no `version` still satisfies a pin; a citizen that names a different version does not. `parameter`, `link_coverage`'s empty parameter, `range_lookup`, and `bracket_fold` pass `env.parameter_index`.
- `packages/derivation/subject_dispatch.py`. `_optional_default` and the per-subject `Environment` use `run.ctx.parameter_index`.

Nothing iterates, serializes, or hashes a sentinel. The id-keyed dict's values are parameter citizens.

### Tests

Both new tests go through `validate_package` → `_resolved_run_material` → `marshal_run_context(..., parameter_index=material.parameter_index)` → `run` and `run_reference`. The rest of this file uses that same marshalling call, so the round-1 cases still see the index.

| Test | Value | Pins |
| --- | --- | --- |
| `test_both_orders_use_v1_and_pin_v1` | Both orders: disposition `blocked`, `DEPENDENCY_ABSENT`, missing the answer symbol. That is 50 over v1's 10. It is not inapplicable, which is what v2's 1000 would do. The id-keyed map has no `\x00` and no entry for this id. The exact index holds v1=`10` and v2=`1000`. | The disposition's only parameter pin is `(param, v1)`. |
| `test_unavailable_exact_version_blocks_and_does_not_borrow` | Only v2 is resolved. Disposition is not `inapplicable`. Code `DEPENDENCY_ABSENT`, missing the parameter id. | No parameter pin of v2. The sibling's value is not used under a v1 pin. |

### Outside this path

`packages/tax/pairing_consequences.py` builds its own `Environment` from `ctx.parameters` and does not copy `parameter_index`. That file is not an assigned path. With one version the id-keyed citizen is still there, so the fallback answers. With two versions the id is absent from that copy and the local environment's index is empty, so an unversioned `parameter` there blocks instead of borrowing. No content package resolves two versions of one parameter. Not changed.

### Verification

```
$ python3 -m pytest -n auto -q
2302 passed, 20 skipped, 4452 subtests passed in 124.61s (0:02:04)
```

```
$ python3 -m mypy
Success: no issues found in 282 source files
```

```
$ python3 tools/governance_lint.py
governance lint: conformant
```

```
$ git diff --check
(no output)
```

```
$ git status --short
 M packages/derivation/evaluator.py
 M packages/derivation/live.py
 M packages/derivation/marshal.py
 M packages/derivation/package_validation.py
 M packages/derivation/runner.py
 M packages/derivation/subject_dispatch.py
?? docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track5d-build-report.md
?? package-lock.json
?? tests/derivation/test_exact_version_authority.py
```

`package-lock.json` is still the pre-existing untracked file. `marshal.py` is edited because the live path drops the exact index unless marshalling copies it onto `RunContext`.

## Round 3

Validation of the default-parameter chain now reads the same `(id, version)` runtime reads. Not committed. `packages/tax/pairing_consequences.py` and `packages/derivation/runners/derive.py` were not changed. `docs/phase-state.md` is dirty in this worktree and was not touched.

### Reproductions, before this round's change

Each case is a package whose pin names parameter v1 and whose members resolve only v2. `validate_package` returned `ok` with no issues, in both declaration orders. The tests that require rejection failed first:

```
AssertionError: True is not false : validate_package accepted a package whose optional_default pins parameter v1 while only a sibling version is resolved: ()
AssertionError: True is not false : validate_package accepted an attachment whose threshold_parameter pins v1 while only v2 is resolved: ()
```

Six subtests, all the same acceptance: ordinary rule and declared-subject rule, fact type before the v2 parameter and after it; attachment threshold, parameter member before the attachment and after it. That run's summary was `6 failed, 3 passed in 2.63s`. Every listed failure was this acceptance.

### Changes

Both are in `packages/derivation/package_validation.py`, `validate_package`.

- `BINDING_DEFAULT_ABSENT`. The fact type's `optional_default` parameter pin was accepted when `param_pin["id"]` was in `member_ids`. It now requires `_corpus_key(id, version)` to be in `parameter_keys`. A resolved sibling of the same id is not that parameter. A missing id is still absent.
- Top-level `requirement["threshold_parameter"]`. The exact-key check covered `any_trigger` triggers only. The same `ATTACHMENT_TRIGGER_PARAMETER_ABSENT` check now applies to the requirement's own pin, which is the attachment-rule.v1 shape (and the same top-level shape on later versions). The trigger loop is unchanged.

### Tests

Sibling-only cases assert admission rejection. They do not run. Acceptance cases go through `validate_package` → `_resolved_run_material` → `marshal_run_context` → `run` and `run_reference`.

| Test | Rejection or value | Pins |
| --- | --- | --- |
| `test_sibling_only_rejected_ordinary_both_orders` | Both orders of fact type and v2 parameter: not `ok`. Issue `BINDING_DEFAULT_ABSENT` names the parameter id and `v1`. | No run. |
| `test_sibling_only_rejected_declared_subject_both_orders` | Same rejection, declared-subject rule, both orders. | No run. |
| `test_pinned_version_only_accepted_both_orders` | Only v1 resolved. Both orders, ordinary and declared-subject. Published value is `from-v1`, not `from-v2`. No `BINDING_DEFAULT_ABSENT`. | The manufactured default's only parameter pin is `(param, v1)`. |
| `test_pinned_version_beside_sibling_accepted_both_orders` | v1 and v2 both resolved, v1 declared first and v2 first, both rule shapes. Published value is `from-v1`. | Same pin: `(param, v1)`, not v2. |
| `test_sibling_only_is_rejected_in_both_declaration_orders` | Attachment pins v1, only v2 is a member, parameter before the attachment and after it. Not `ok`. Issue `ATTACHMENT_TRIGGER_PARAMETER_ABSENT` names the parameter id and `v1`. | No run. |
| `test_pinned_version_only_is_used_in_both_declaration_orders` | Only v1 (`10`) resolved, both orders. Subtotal `50`. Disposition `blocked`, `DEPENDENCY_ABSENT`, missing the answer. Not inapplicable. | The disposition's only parameter pin is `(param, v1)`. |
| `test_both_orders_use_v1_and_pin_v1` | v1 `10` and v2 `1000` both resolved, both orders. Same disposition as the only-v1 case: required, then blocked on the answer. v2 would have been inapplicable. | Same pin: `(param, v1)`. |

`test_unavailable_exact_version_blocks_and_does_not_borrow` was removed. It required the sibling-only attachment package to validate and then block at runtime. Admission now rejects that package, which is the check above.

### Stop

Two existing packages name a top-level threshold parameter and do not resolve any parameter member. They now fail `ATTACHMENT_TRIGGER_PARAMETER_ABSENT`. They are outside the assigned paths, so they were not given the missing parameter member:

- `tests/derivation/test_declarative_validation_package_closure.py`, `test_baseline_validates`. Attachments `declarativevalidation.demo-attachment` and `declarativevalidation.demo-scalar-attachment` pin `demo.param` v1. The loaded citizens have no parameter declaration.
- `tests/test_dsbs_t1_schema_citizens.py`, `test_conforming_package_is_admitted_by_both_guards`. The example attachment pins `demo.parameter.attachment-threshold` v1. The guard package's members do not include that parameter.

The full suite is red on those two tests. The exact-version file is green (`24 passed, 46 subtests passed`).

### Verification

```
$ python3 -m pytest -n auto -q
FAILED tests/derivation/test_declarative_validation_package_closure.py::DeclarativeValidationPackageClosureTest::test_baseline_validates
FAILED tests/test_dsbs_t1_schema_citizens.py::AdmissionGuards::test_conforming_package_is_admitted_by_both_guards
2 failed, 2303 passed, 20 skipped, 4468 subtests passed in 123.68s (0:02:03)
```

```
$ python3 -m mypy
Success: no issues found in 282 source files
```

```
$ python3 tools/governance_lint.py
governance lint: conformant
```

```
$ git diff --check
(no output)
```

```
$ git status --short
 M docs/phase-state.md
 M packages/derivation/evaluator.py
 M packages/derivation/live.py
 M packages/derivation/marshal.py
 M packages/derivation/package_validation.py
 M packages/derivation/runner.py
 M packages/derivation/subject_dispatch.py
?? docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track5d-build-report.md
?? package-lock.json
?? tests/derivation/test_exact_version_authority.py
```

`docs/phase-state.md` was already modified in this worktree and is not part of this round. `package-lock.json` is still the pre-existing untracked file.

## Foreman note after round 3

The two shared-fixture failures above describe the tree before the foreman narrowed the new top-level
threshold check. It now rejects only when another version of the parameter id is resolved and the pinned
version is not — the version-authority case. A threshold parameter absent altogether was never checked at
validation and still passes, with runtime blocking `DEPENDENCY_ABSENT`; that wider gap is reported to the
owner rather than closed here, because closing it changes two other milestones' sample fixtures. With the
narrowing the full suite passes (2305 passed, 20 skipped). A confirming independent review verified it.
