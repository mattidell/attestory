# Track 3 coverage contract — one statement, its current links, and their reductions

Specification only. No production code, schema file, or content citizen is added by this document. Stage B implements it after review, and stage B writes the ADR.

This is the contract for one statement subject, as the owner required on 2026-09-23. Read against branch `milestone/student-loan-circumstance-association` at `7a7d9cd5` (later than `6a97a983`). The behaviour below is not a proposal to re-decide. The open question this document answers is where that behaviour is declared.

## Plain account

A Form 1098-E statement has a box 1 amount. A recorded link says that statement is connected to a borrowing. Each such link is supposed to contribute its own numeric reduction, published earlier in the same run and pinned to that link. The statement's reported amount is box 1 minus those reductions.

Three things are different, and the probes showed the engine currently treats two of them as the same:

- Nothing was linked. The amount is box 1 minus a declared default. That default is a calculation choice. It does not claim the set of links is complete.
- Every current link has its own numeric reduction. Publish box 1 minus those reductions, and pin every one of them and every one of the links.
- A link is recorded and its reduction never became a number — the reduction is absent, blocked, or inapplicable. That statement blocks, and the block names that link. The missing reduction is not zero. Another statement in the same run is left alone.

An ordinary collection that is empty and was not declared closed still blocks. This contract does not give that collection a default.

## 1. Candidate homes

The note in [`a4-bounds.md`](a4-bounds.md) ("P3 repair") that a `rule-artifact.v10` operation is the smallest home is a hypothesis. It is not the selection. Each home below was read against the schemas and the runner that actually admit a rule today. `rule-artifact.v9` is the newest rule schema, `artifact-package.v30` is the newest package schema, and both are published history.

### 1.1 A new operation on a rule-artifact successor

**What it declares.** One expression node names the link source, the reduction source, and the parameter that supplies the reduction when no current link joined. The node's meaning is the three outcomes. The arithmetic around it stays ordinary (`subtract` of box 1 and this node).

**Schema.** A new `rule-artifact.v10`. v9's bytes stay as they are (ADR-0003; the schema publication protocol). v10 does not carry v9's `selection` or `aggregation` fields. Those fields are schema-valid on any v9 rule and are executed only for two exact rule ids; every other v9 carrier blocks `DEPENDENCY_INVALID` with `missing == ["v9-declarative-binding-unauthorized"]` (`runner._Run.attempt`, the v9 declarative branch). Copying them forward would either repeat that id gate or give them a second runtime. v10 is the ordinary guarded clause (the same required fields as v9's `value` branch) plus one expression alternative.

**What validates it.** The v10 JSON Schema, then package validation on a package schema that lists `rule-artifact.v10` in `admitted_schemas`. v30's enum includes `rule-artifact.v9` and does not include a v10, and its title is the package that admits v9. Admitting the rule into a package therefore needs `artifact-package.v31`, not an edit to v30. The checks that are not schema are in section 2.

**What the runner and marshal must admit.** Three admissions, and they are not the same list.

Marshal's walk of `ref` names declared outside `requires` (`marshal._rule_required_symbols`) recognizes rule schemas v3 through v9 only. That frozenset gains `rule-artifact.v10`, so a v10 rule's `ref` names are still seen by the legacy input fallback. `links` and `reductions` are not `ref` names. That walk does not admit them.

*(Amended 2026-09-24, ADR 0075.)* The production admission of the link type is `live._resolved_run_material`. That function builds `collect_names` and, separately, an emission-only name set. The live coordinator passes `collect_names` to marshal as `collect_source_names` and the emission-only set as `emission_only_source_names` (optional, default empty, including through `live_run` and `marshal_live_run_context`). `collect_names` is source-family member predicates, their companions, names from `_iter_collect_categorical_names`, and four rule-id special cases. A `link_coverage` node does not add to it. The rule-schema set includes `rule-artifact.v10`, or a v10 rule is not in `rules` and the walk never sees it. For every rule in that list it walks `value`, by the same recursion `_iter_collect_categorical_names` uses, and for every `link_coverage` node it appends that node's `links` string to the emission-only set when the string is not already a collect name. It does not append `reductions` to either list. The walk adds no source-family member, no companion, and no closure read. It is not `_iter_collect_source_sets`, and `audit_collect_authority` does not see the node. `marshal_run_context` emits sources for the union of the two sets. The input-binding loop and the legacy fallback consult only `collect_names`. Findings emitted only because of the emission-only set are not added to the used ids: the legacy fallback skips a used id before the collect-name test, and marking those ids would drop the run-wide scalar that fallback still binds when the current values agree. A name that is already a collect name keeps that exclusion. Marshal emits a `SourceFact` for a current kernel finding whose fact type matches a name in either set (`currency.current_finding_ids`, then the fact-type test). A current link is admitted by that emission once its name is on the emission-only set. A reduction is a derived finding. Marshal never loads derived findings, and `reductions` is not registered, so nothing on either list emits one. The reduction becomes a source only when its rule appends a same-run live source (`runner._Run._append_live_source`, from `_append_live_source_from_finding`). Dropping that registration does not by itself drop confinement; confinement is dropped because the link type is outside the set those two branches consult and its finding ids are not marked used (section 2). When the link type has no current finding, per-subject dispatch installs an empty slot (section 3). That empty slot is the default in section 5. It is not a missing admission, and it is not `link-coverage-scope-unbound`.

`use_v2` is a flag on the run, not on one rule. `_Run.__init__` and `run_and_record` set it true when any rule in `ctx.rules` has schema `rule-artifact.v2` through `rule-artifact.v9`, or the run uses attachment machinery (`_uses_attachment_machinery`). The set stops at v9. A v10 rule that shares a run with any v2–v9 rule already records `code` and `missing`. A run whose rules are all outside the set does not. Adding `rule-artifact.v10` to both of those sets is what a v10-only run needs. The flag stays per run. When it is true, the subject-scoped recorder (`runner._Run.evaluate_subject_scoped_rule`) still keeps a code that is in `RECORD_CODES` and copies `missing`. Nothing else about that recording changes.

The evaluator gains one arm. It does not gain a change to the `collect` or `count` arms.

**Blast radius.** Every admission frozenset that names `rule-artifact.v9` as the top of the ordinary rule set has to learn v10 or a v10 rule is inert (`package_validation._SUPPORTED_SEMANTIC_SCHEMAS` and the rule-schema sets, `live.py`, `authorization_closure.py`, marshal, runner). Existing v1–v9 rules are not rewritten. The operation is general grammar: any v10 rule may declare it. It is not registered to one rule id. That is deliberate, and it is the opposite of ADR-0074's package-acceptance gate for `bound_sources`. The cost of that generality is in section 2: outside a per-subject scope the operation fail-closes rather than scanning every statement. *(Amended 2026-09-24, ADR 0075.)* Another member may name the link type. A sibling `collect` returns decimals, not key maps, and a plain `ref` outside dispatch binds a run-wide scalar only through the legacy fallback, when the current values agree. `derivation-record.v9` is not a schema that moves. The `collect` and `count` arms do not move.

No new disposition code, and no `derivation-record.v10`. An uncovered link blocks `DEPENDENCY_INVALID`. That code is already in `derivation-record.v9`'s closed `code` enum and in `RECORD_CODES`. `missing` is exactly the uncovered links' `finding_id` values, sorted. `records.CURRENT_RECORD_SCHEMA` stays `"derivation-record.v9"` for every use_v2 start and close; it is one constant, and this home does not change it. What the shared code does not distinguish is in section 5. P4 decides, from what a durable reader sees, whether a distinct code is needed. If it is, the record bump is chartered then. It is not a consequence of this home.

### 1.2 A field on the rule, on a successor

**What it declares.** A rule-level object naming the same two sources and the same parameter. `value` would still be a separate expression.

**Schema.** Also a new rule-artifact version. A field does not avoid v10. v9 cannot grow a property.

**What validates it.** Schema plus a package check that `value` does not also `collect` or `count` those names. Without that check the field and the expression can disagree.

**What the runner and marshal must admit.** The same v10 admission lists. In addition, both `subject_dispatch.evaluate_subject_scoped_rule` and `_Run.attempt` must honour the field. Dispatch is not selected by rule content (`subject_dispatch` says so, and `runner.evaluate_subject_scoped_rule` repeats it). A field honoured only inside subject dispatch would be ignored on the ordinary saturation path, and that path would evaluate `value`. If `value` still contains the probe's `collect` of reductions, the measured defect returns: one published reduction keeps the collection non-empty, and the uncovered link is dropped.

**Blast radius.** Same schema and admission cost as the operation, plus a second interpreter beside the expression evaluator, plus a prohibition that exists only to stop the field and the expression from diverging. v9 already showed what a generic-looking rule field becomes: `selection` and `aggregation` have no generic runtime.

**Why it loses.** The three outcomes are three different evaluations of one number (the reduction total). That number is an expression input to `subtract`. Putting the decision in a field and the number in `value` splits one fact across two places. P3 measured the split that looks smaller and is wrong: a default on the empty reduction collection does not run in the one-of-two case, and in the only-unresolved case it publishes the no-link figure.

### 1.3 A new binding mode on an artifact-package successor

**What it declares.** `artifact-package.v30` `input_bindings[].mode` is `required` or `optional_default`. A new mode would be a property of a package binding: one symbol, one fact-type pin.

**Schema.** `artifact-package.v31` would be required even for this home, and the mode's object would have to grow link and reduction names that are not a binding. At that point it is no longer a binding mode.

**What validates it.** `package_validation` accepts `optional_default` only when the fact type declares `optional_default.parameter` and that parameter is a package member. The runner manufactures one symbol value in `_Run.__init__` when the symbol is unbound, and subject dispatch does the same per subject in `_optional_default`.

**What it cannot say.** The reduction is a derived symbol, not a fact type. A default that fills "the reduction symbol" when zero reductions joined is both the no-link statement and the only-unresolved statement, and it does not run when one of two reductions published. That is measured (`temp/a4-pass2/p3c-report.md`, part 4). A binding also has no per-link identity and no place to put one link's finding id into `missing`.

**Blast radius.** Every package's binding validator and both manufacture sites. The calculation would sit on the package, which is membership and adoption, not the rule. ADR-0006 puts the computation in the rule.

**Why it loses.** It does not have a shape that can state the required behaviour. Stretching it until it can is a rule-level declaration that happens to be stored on the package.

### 1.4 A separate content citizen the rule references

**What it declares.** A new citizen (its own schema, its own published checksum) holding the two names and the parameter pin. The rule would carry a pin to it.

**Schema.** That new citizen, and still a rule successor, because v9 has no field or expression that means this. Two schemas, where the operation needs one rule schema plus the package successor section 1.1 already requires. It does not need a record successor.

**What validates it.** Package membership, an exact pin, and a semantic check that the citizen's names resolve. The runner would have to load the citizen onto the run context the way it loads parameters.

**Blast radius.** A new adopted-content kind. The nearest existing shapes are `source-family` and `source-closure-mapping`: adopted, versioned, pinned, and meaningful only when a closure finding admits them. A reviewer would be right to ask whether this citizen is a completeness claim. It must not be one. Nothing in the measured behaviour needs a declaration that outlives the one rule expression and is adopted on its own.

**Why it loses.** No second rule is shown that must share this declaration apart from its own expression. The extra citizen adds the appearance of family authority without adding any fact the operation cannot state.

### 1.5 Selection

**Selected home: the operation, named `link_coverage`, on `rule-artifact.v10`.**

Reasons, tied to what was measured rather than to which diff looks shorter:

1. The defect is that `collect` returns numbers and drops identity (`evaluator.evaluate`, the `collect` arm; P3). The fix has to see two scoped source lists and their key tuples, and then return one number or block. That is an expression node. `bound_sources` is the precedent for a node that is not `collect`: it has no `source_set`, it records a different access-log channel, and it never reads `env.sources`.
2. The field home needs the same new rule schema and the same admission lists, and it also needs a ban on `collect` of the same names so the field and `value` cannot diverge. The operation is that ban by construction: the reduction total is the node.
3. The binding mode and the separate citizen cannot state a per-link match without becoming a worse copy of the operation, and the binding mode has already been measured not to distinguish no-link from only-unresolved.
4. None of the four homes requires editing the `collect` or `count` arms, manufacturing a source family, or comparing rendered ids. The stop condition is not met. The homes that would do those things (an empty-collect default, a closed `source_set` on the reduction name) were the ones P3 already ruled out, and they are not selected.

**What would overturn the choice.**

- Overturn toward the field if extending `Environment` cannot be done with a defaulted slot. It can: `bound_sources` is already a defaulted field so the positional constructor in `pairing_consequences.py` keeps working. A review that shows a defaulted slot still changes `collect` or `count` would overturn the operation. This contract forbids that change.
- Overturn toward the field if the operation, evaluated from ordinary `attempt()`, can see another statement's rows. The contract forbids that: the operation reads only `keyed_sources`, and an ordinary environment leaves that map empty and fail-closes. It does not read `env.sources`.
- Overturn toward a separate citizen if more than one rule must share one coverage declaration as adopted content, independently of the expression that uses it. Not shown.
- Overturn toward a binding mode if the default is filling one missing fact-type symbol rather than choosing the reduction total for an empty link list. The reduction is derived. P3c part 4 stands until a measurement contradicts it.
- A distinct disposition code is not part of this selection. Section 5 records what reusing `DEPENDENCY_INVALID` does not distinguish, and leaves a record bump to P4. Evidence from the durable reader that a consumer cannot do its job without that distinction charters `derivation-record.v10` then. It would not reverse the operation, and it is not a reason to adopt the record successor in this contract.

## 2. Exact shape

`link_coverage` is one alternative in v10's expression `oneOf`. No `source_set`. No match-mode field: a declaration cannot opt into comparing `fact_id`.

```json
{
  "type": "object",
  "properties": {
    "op": { "const": "link_coverage" },
    "links": { "type": "string", "minLength": 1 },
    "reductions": { "type": "string", "minLength": 1 },
    "empty": {
      "type": "object",
      "properties": {
        "parameter": { "$ref": "#/$defs/exact_pin" }
      },
      "required": ["parameter"],
      "additionalProperties": false
    }
  },
  "required": ["op", "links", "reductions", "empty"],
  "additionalProperties": false
}
```

`exact_pin` is the object v9 already uses: `id` (string, min length 1) and `version` (`^v[0-9]+$`), both required, no extra properties.

`empty` is a parameter pin, not a nested expression. An expression there could hide a `collect`. The parameter citizen is the only source of the default number (ADR-0006 decision 5: policy values are not inlined).

The rest of the v10 rule object is the ordinary guarded clause. Required: `schema` (`const` `rule-artifact.v10`), `id`, `version`, `scope` (tax year, jurisdiction, family), `role`, `requires`, `pins`, `when`, `value`, `publishes`, `blocked`. `citations` stays optional and is how the worked example names its authority. `selection` and `aggregation` are not properties. `additionalProperties` is false.

The node returns one decimal. It appears exactly once, inside `value`. It does not appear in `when`. *(Amended 2026-09-24, ADR 0075.)* `links` and `reductions` may appear in `requires`. Package validation rejects the `when` placement and a second node in `value`. It does not reject those strings in `requires`.

Package validation, beyond the schema, accepts a v10 rule declaring this node when all of the following hold, and not by an allowlist of rule ids:

- `links` and `reductions` are different strings.
- `links` is a fact type on the package fact surface. It is the kernel fact for the recorded link, not a derived symbol.
- `reductions` is the `publishes` value of another rule member, and that member is a predecessor of this rule in the package graph.
- `empty.parameter` is a package member, id and version exact.
- The node is not walked by `_iter_collect_source_sets` and not seen by `audit_collect_authority`. It adds no source-family edge and no closure read. That refusal is not the admission. *(Amended 2026-09-24, ADR 0075.)* `live._resolved_run_material` returns `links` on the emission-only set and puts neither `links` nor `reductions` on `collect_names`, as section 1.1 specifies. `marshal_run_context` emits the emission-only set and does not consult it when binding a scalar.
- It is not checked by `BOUND_SOURCE_TARGET_UNDECLARED`. That check requires the name to be a fact type of an admitted bundle. The reduction is derived, so reusing the check would reject a well-formed rule.

**Name confinement — dropped.** *(Amended 2026-09-24, ADR 0075.)* `validate_package` does not reject another member for naming `links` or `reductions`. `LINK_COVERAGE_NAME_REUSED` is not raised. Shape checks stay, and they use `LINK_COVERAGE_INVALID`: the node is not in `when`, it appears exactly once in `value`, the two strings differ, `links` is on the fact surface, `reductions` is one other rule's `publishes`, and `empty.parameter` is an exact package parameter. The node placed in `when` still fails that shape check. `marshal._rule_required_symbols` does not change. `evaluator.evaluate` does not change. A second `link_coverage` node that repeats either string is not a name-reuse rejection.

What a sibling sees, because the link type is emitted and is not a collect name, and because findings emitted only for that set are not marked used:

- **Scalar binding.** The binding loop in `marshal_run_context` binds `matches[0]` when `len(matches) == 1 or symbol not in collect_names`. `symbol` is `binding["symbol"]`. `matches` are the current findings of `binding["fact_type"]["id"]`. Disagreeing multi-matches stay unbound. The link type is not in `collect_names`, so an input binding whose `symbol` is the link type binds as it would if the type were not collected: one finding binds, several agreeing findings bind `matches[0]`, and disagreement stays unbound. A binding whose symbol is some other string is unchanged, including when its fact type is the link type, because the test never sees the fact-type id. A sibling fact type still binds as before, including one finding and including several agreeing findings. `reductions` is not a kernel fact type and is not on the list.
- **Legacy fallback.** The fallback skips a fact type id that is in `collect_names`, and it skips a finding id already in the used ids before that test. The link type is not in `collect_names`, and coverage emission does not add its finding ids to the used ids, so a `ref` of the link type outside dispatch binds a run-wide scalar through the fallback when the current link values agree, including one finding, and does not bind when they disagree. That is the behaviour before registration. It is not a per-statement read. The `ref` arm reads `env.symbols`, not the row list. `reductions` is not a kernel fact type. Omitting it from both lists does not create a scalar.
- **Sibling `collect`.** `evaluator.evaluate`'s `collect` arm is unchanged. It reads `env.sources`, which `_Run.__init__` copies from the sources marshal emitted. A sibling may `collect` the link type. The arm returns each value as a decimal. It does not return key maps. A non-numeric value, including a JSON object, blocks `DEPENDENCY_INVALID` from `_as_decimal` (`not a number`), not a separate `VALUE_INVALID` code. The rows are every current link of that type, run-wide, not the per-subject join. A consumer that needs the canonical links reads them per subject, by per-subject dispatch, which joins on shared key names. A `collect` of `reductions` sees same-run appended rows, which do not depend on registration. An empty `collect` whose `source_set` is not closed still blocks `SOURCE_SET_UNCLOSED`.
- **Closed `count`.** `count` is unchanged. It still blocks when `source_set` is not in `env.closed_sets`, and when the set is already closed it returns `len(rows)`. A sibling may `count` the link type, and a closed count counts the emitted rows. `collect_categorical_all_equal` reads the same `env.sources` rows (and blocks `DEPENDENCY_ABSENT` when there are none). A sibling that collects the link type pins every row it read, across statements. That pin is the sibling's own read, not the operator's.

**Not solved here.** Nothing in rule content selects per-subject dispatch. Calling code does. A production run that attempts the reduction rule or the coverage rule through ordinary `attempt` does not perform the per-subject outcomes. The operation fail-closes `link-coverage-scope-unbound` on that path, because an ordinary `Environment` leaves the keyed slot empty. How per-subject rules are scheduled in a production run is shared by Tracks 1–3. Track 3 does not settle it. It is open for G2.

`_SUPPORTED_SEMANTIC_SCHEMAS` must include `rule-artifact.v10`. A schema the validator does not handle fails as `MEMBER_SCHEMA_UNSUPPORTED`. v10 does not inherit the v9 id gate (`RULE_SELECTION_UNAUTHORIZED` and the aggregate checks key off `schema == rule-artifact.v9`).

### Worked example

Synthetic ids, the same names the P3 probes use. This citizen is not adopted content. The parameter value `"0"` is a decimal string.

```json
{
  "schema": "parameter-declaration.v1",
  "id": "demo.param.no-link-reduction",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "us",
    "family": "demo-student-loan"
  },
  "values": "0"
}
```

```json
{
  "schema": "rule-artifact.v10",
  "id": "demo.rule.statement-box-minus-reductions",
  "version": "v2",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "us",
    "family": "demo-student-loan"
  },
  "role": "computation",
  "requires": ["demo.tax.f1098e.box1-student-loan-interest"],
  "pins": [],
  "when": {
    "op": "compare",
    "cmp": "gt",
    "left": { "op": "ref", "name": "demo.tax.f1098e.box1-student-loan-interest" },
    "right": 0
  },
  "value": {
    "op": "subtract",
    "left": { "op": "ref", "name": "demo.tax.f1098e.box1-student-loan-interest" },
    "right": {
      "op": "link_coverage",
      "links": "demo.tax.statement-to-borrowing",
      "reductions": "demo.tax.link-reduction",
      "empty": {
        "parameter": {
          "id": "demo.param.no-link-reduction",
          "version": "v1"
        }
      }
    }
  },
  "publishes": "demo.tax.statement-facing-amount",
  "blocked": { "code": "DEPENDENCY_INVALID", "missing": [] },
  "citations": [
    { "id": "demo.citation.statement-box-minus-reductions", "version": "v1" }
  ]
}
```

The rule's `blocked` object is the schema-required declaration. The runner does not read it today. The disposition's `code` and `missing` are the runtime values in section 5, not this empty `missing` array.

The finding symbol is unchanged from subject dispatch: `demo.tax.statement-facing-amount` plus `|` plus the statement subject's fact id. The same-run source appended for a published amount still carries that statement subject's key tuple. This contract does not put keys on the derived finding.

For a statement whose box 1 is 1500 and which has no current link, the node returns the parameter's decimal 0, and the published amount is 1500. That equality is box 1 minus the declared reduction. It is not an empty sum.

## 3. Identity

A link matches a reduction when both have `SourceFact.keys` and the name-to-value maps are equal. `keys` is the tuple of `(name, value)` pairs the kernel `Fact` holds and that marshal copies onto the source (`lattice_fact.keys`). Track 2 copies that same tuple from the link subject onto the reduction's same-run source. Order of the tuple is not the comparison; the map is. Two tuples that carry the same names and values match. A reduction whose map is only the statement's keys, without the borrowing key the link carries, does not match.

The match does not use `fact_id`, the symbol, or the suffix of a symbol. `SourceFact` records why: `fact_id` is a lossy rendering, two different key tuples can render as the same string, and a value containing a comma cannot be recovered by splitting. `_append_live_source_from_finding` partitions the symbol on `|` to choose a `fact_id`. That partition is not a match key. `dependency_pins_for_access` compares rendered fact-id suffixes for companion pins. This operation does not use that comparison.

Fail closed, for that subject only, before any of the three outcomes:

| Situation | Code | `missing` |
| --- | --- | --- |
| The name is not in `keyed_sources` at all (ordinary `Environment`, slot left empty) | `DEPENDENCY_INVALID` | `["link-coverage-scope-unbound"]` |
| Either declared name's slot is the sentinel `keys_unavailable` (`_scope` returned `None` for that name) | `DEPENDENCY_INVALID` | `["link-coverage-keys-unavailable"]` |
| A joined reduction's key map equals no joined link | `DEPENDENCY_INVALID` | that reduction's `finding_id`, sorted if more than one |
| Two joined links have the same key map | `DEPENDENCY_INVALID` | both links' `finding_id` values, sorted |
| One link's key map equals two or more reductions | `DEPENDENCY_INVALID` | that link's `finding_id` |
| The matched reduction's value is not a number, including a boolean | `DEPENDENCY_INVALID` | that link's `finding_id` |
| Present link rows share no key name with the subject, and every coverage slot is an empty list *(amended 2026-09-24, ADR 0075)* | `DEPENDENCY_INVALID` | `["link-coverage-unjoinable"]` |

No row in those cases is treated as zero, dropped, or paired by `fact_id`. The sentinel is not a row. A missing lattice entry is already `keys=None` at marshal time. The operation does not repair it by parsing the rendered id.

The checks run in the order of that table. A keys-unavailable sentinel is reported before an orphan, and it is not reported as an empty link list. An orphan reduction is reported before an uncovered link on the same subject, so a stale reduction cannot be ignored in favour of a block that names only the link, and cannot be ignored in favour of the default. *(Amended 2026-09-24, ADR 0075.)* The unjoinable row is last, immediately before the no-link default. It fires only when every coverage slot is an empty list, so a joined reduction is still reported as an orphan first. Zero link rows are not this row. A shared key name whose values disagree is a join of nothing, not this row. The check reads the present candidates at the coverage-slot fill in `subject_dispatch.evaluate_subject_scoped_rule`, after the ordinary guard and before `value`. The operation sees only the joined list, and `_scope` returns `[]` both for unjoinable rows and for a real empty join, so the check cannot move into the evaluator. `_scope` is unchanged. With no link row in the run, joinability is not observable; that case takes the default and is G2's, including when the subject's keys are absent.

`subject_dispatch.evaluate_subject_scoped_rule` installs the operation's slot for both names the `link_coverage` node declares, on every subject. It learns those names by walking `value`. It does not learn them by listing names that happen to occur in `sources`. For each declared name it takes the live sources of that name, which may be none, and calls `_scope`. `_scope` of an empty candidate list returns `[]` without reading keys. The slot receives that list. *(Amended 2026-09-24, ADR 0075 repair.)* **Except:** when the subject's own keys are absent, dispatch installs the keys-unavailable sentinel for both declared names without calling `_scope`, so a subject of unknown identity never takes the no-link default. Empty and unbound are different. *(Amended 2026-09-24, ADR 0075.)* Empty links with no orphan reduction, and no present unjoinable link row, is the default path. That is the path when no link row exists anywhere in the run, and the path when rows exist but a shared key name's values do not agree. It is not `link-coverage-scope-unbound`. Present rows that share no key name are the unjoinable row in the table above, not this default.

`link-coverage-scope-unbound` is only the slot left at its default. That is ordinary `attempt()`, whose `Environment` never installs the field. The per-subject function does not leave either declared name out. *(Amended 2026-09-24, ADR 0075.)* A validated package emits the link type through the emission-only set (section 1.1), so a current link finding of that type is a source. `reductions` is not registered; the reduction row is a same-run live source. `_scope` itself does not change.

When `_scope` returns `None` for either declared name, the same function installs the sentinel `keys_unavailable` as that name's slot value. It does not install `[]`. The operation, seeing the sentinel on either declared name, blocks `DEPENDENCY_INVALID` with `missing` `["link-coverage-keys-unavailable"]` and does not take the default. A `None` for a name the node does not declare keeps today's caller behaviour: an empty list in the scoped sources, and `DEPENDENCY_INVALID` naming the symbol only when that name is required. The sentinel is written only on the operation's slot, not into the `sources` map `_local_maps` builds.

The slot is a new defaulted field on `Environment`, the same pattern as `bound_sources`. Ordinary `collect` reads `env.sources` and does not read the slot. The operation reads the slot and does not read `env.sources`. Populating the slot from what `_scope` returned — the list of rows it selected, or the sentinel when it returned `None` — does not change who joins to the subject. `_scope`'s join is unchanged.

## 4. Currency

Marshal emits a `SourceFact` for a kernel finding that `currency.current_finding_ids` lists and whose fact type is a collected name or an emission-only name (`marshal_run_context`). *(Amended 2026-09-24, ADR 0075.)* A link finding that currency does not list is not a source and is not a recorded link. A current link whose type was on neither list is also not a source; section 1.1 puts that type on the emission-only set for a validated package, not on `collect_names`, so that omission is not a production path. Derived findings are not in that loop. A reduction becomes a source only as a same-run live source, as section 1.1 says. `reductions` is not registered.

**Correction.** A corrected link is a new finding for the same fact: same key tuple, new finding id. The displaced finding is not current. The next run marshals the successor. The reduction rule runs on that successor as its subject, so the reduction source's keys are the successor's keys and the reduction's input pin is the successor's finding id (the subject pin `_assemble_pins` already adds). The amount then matches them by those keys. The pin walk of the amount reaches the successor link, not the displaced finding. This is a re-derivation, the way P3's exhausting-portions case already re-derives after an enrolment correction. It is not an in-place edit of a live source.

**Withdrawal.** A withdrawn link is not current, so it is not a recorded link and it is not a subject. Derived findings are never marshalled. `marshal_run_context` reads kernel findings in `state.findings` that `currency.current_finding_ids` lists, and emits a `SourceFact` only for a collected name. It does not load a derived finding, current or displaced. `live.live_coordinate_run` calls kernel `compute_currency(state)` and passes that view to marshal. It does not call `compute_derivation_currency`. Kernel `_declared_edges` reads `finding["pins"]["finding_ids"]` on kernel findings, not the role pins on a derived finding.

The reduction is absent on the next run because the reduction rule has no current link subject left to re-derive it, so nothing republishes it. The statement sees no link and no reduction and takes the default. That absence does not depend on a derivation edge, and it is not marshal dropping a displaced derived finding. Taking the default here does not assert that the link set is complete. It asserts that no current link joined.

ADR-0010 decision 4 still describes the pin: an `input` pin that names a finding id is an edge from that finding to the derived finding. Decision 5 still says a derived finding is a displacement target, never a root. `_assemble_pins` appends the subject pin (`role` `input`, the subject's finding id). This contract does not use that edge as the account of why the next run omits the reduction.

If a reduction source is still joined in the same run after the link is not among the joined sources, section 3's orphan check blocks `DEPENDENCY_INVALID` and names the reduction's finding id. The default is not published. That check is defensive and in-run. It detects a joined reduction whose key map equals no joined link. It does not diagnose a missing displacement edge. A cross-run withdrawal does not produce the row: the reduction is not re-derived, so it is not joined. Stage B keeps the check. Stage B does not delete it to make an in-run orphan look like the default, and does not report the block as a displacement failure.

**What a blocked or inapplicable reduction is.** Subject dispatch appends a live source only for a publication. A blocked reduction is on `run.blocked` and the disposition ledger. An inapplicable reduction is on the disposition ledger. Neither is a `live_sources` row, and the statement operation does not read those ledgers. The raw link, if still current, is still a source. No matching reduction means the link is uncovered. The reduction row's own `missing` list (in the probe, `demo.tax.schooling-status`) is not copied onto the statement.

A published reduction of decimal 0 is a numeric reduction. It covers the link. It is not the uncovered case and not the default.

## 5. Semantics of each outcome

The operation runs only after the ordinary guard. A false `when` is `inapplicable` for that subject and does not publish the default and does not block uncovered. A `ref` to box 1 that is absent is `DEPENDENCY_ABSENT` for that symbol, which is a missing box, not a missing link.

Pins below are added to the ordinary rule, citation, adoption, and governance pins, and then sorted the way `pins_for` already sorts them. Link and reduction pins from this operation go through a new access-log channel, not through `access.collects`. The collect channel pins every finding id on that source name (`dependency_pins_for_access`). Using it here would pin rows that were not part of this subject's match. That is the leak `bound_sources` was given its own channel to avoid.

### No current link

*(Amended 2026-09-24, ADR 0075.)* The link list for this subject is empty, the orphan check did not fire, and no present link row was unjoinable. The empty list is the slot per-subject dispatch installed for `links` when that name has no source in the run, and when rows shared a key name but none agreed. It is not the unbound slot, and it is not the unjoinable row in section 3. Zero rows still take this default; joinability of a type with no rows is G2's. The node returns the parameter's `values` as a decimal. It does not return `[]`. It does not record a closure read.

The published amount is box 1 minus that decimal. The disposition is `published`.

Pinned: the box-1 finding (`role` `input`, `origin` `assertion`) and the parameter (`role` `parameter`, the pin's id and version). Not pinned: any link, any reduction, any source-family, any closure mapping, any closure finding.

The finding does not carry `resolved_input`. That field is the closed shape for a manufactured input (`origin` `declared_default` on a fact that was not asserted). This amount is a computation. What records that the reduction came from the default is the parameter pin, which the covered publication does not carry.

### Every current link covered

Each joined link has exactly one numeric reduction with the same key map. The node returns the sum of those reduction decimals, and only those. The published amount is box 1 minus that sum. The disposition is `published`.

Pinned, each once: every covered reduction's `finding_id` and every covered link's `finding_id`, each as `role` `input`, `version` `v1`, `origin` `assertion`. The parameter is not pinned. Closure pins are not present.

The reduction finding already pins its link, because the link was the reduction rule's subject. The amount pins the links as well, on its own pin list. A reader of the amount does not have to walk through the reduction to find the link. P3's defect was the unresolved link missing from both the amount's pins and the walk.

### Any uncovered link

One or more joined links have no matching reduction. The subject blocks. The code is `DEPENDENCY_INVALID`. `missing` is exactly the uncovered links' `finding_id` values, sorted lexicographically, and nothing else. Not the reduction symbol. Not the rendered fact id. Not the reduction rule's missing list. Not the links that were covered.

Pinned: those same uncovered finding ids, as input pins. No synthetic zero. No parameter pin.

There is no `LINK_UNCOVERED` code. It is not added to `RECORD_CODES`, and it is not added to any derivation-record schema. `DEPENDENCY_INVALID` is already in that set and in `derivation-record.v9`'s `code` enum. v9 `missing` is already an array of strings, so the link finding ids validate. When the run's `use_v2` flag is true, the subject-scoped recorder keeps the code and copies `missing`. `records.CURRENT_RECORD_SCHEMA` stays `"derivation-record.v9"`.

What is lost. The code does not say "uncovered" rather than "invalid". Section 3 uses the same code, with finding ids in `missing`, for an orphan reduction, two links with the same key map, and a non-numeric reduction on the same subject. A consumer that reads only `code`, or only the shape of `missing`, cannot tell an uncovered link from those. One uncovered link and one non-numeric reduction are the same shape: a single link `finding_id` under `DEPENDENCY_INVALID`. P4 decides, with evidence from the durable reader, whether a distinct code is needed. If it is, the record bump is chartered then. This contract does not bump the record.

Other subjects are separate iterations of the same dispatch. A block for one statement does not drop, rewrite, or pin another statement's finding.

### Undeclared empty collection

A `collect` or `count` that does not go through this operation is unchanged. An empty `collect` whose `source_set` is missing or not in `env.closed_sets` still raises `SOURCE_SET_UNCLOSED` with `missing` of `[source_set or name]`. A `count` whose `source_set` is not closed still blocks even when rows are present. This operation is not a default for that path. A v10 rule may still contain `collect`; if it does, `collect`'s rules apply, including the required `source_set` on the v10 schema. *(Amended 2026-09-24, ADR 0075.)* A sibling may `collect`, `count`, or `collect_categorical_all_equal` the link type. Those arms are unedited. A `collect` of `links` sees the emitted rows and returns decimals, or blocks `DEPENDENCY_INVALID` when a value is not a number. It does not return key maps. A closed `count` of `links` counts those rows. A `collect` of `reductions` sees same-run appended rows even though that name is not registered.

## 6. The default's declaration

The number comes from the parameter named in `empty.parameter`. In the worked example that parameter is `demo.param.no-link-reduction` at `v1`, and `values` is `"0"`. The operation reads `parameters[id].values` and checks that the citizen's version equals the pin's version. A missing parameter is `DEPENDENCY_ABSENT` with `missing` of `[parameter id]`. A version mismatch is `DEPENDENCY_INVALID` with `missing` of `[parameter id]`. Neither is the no-link success path.

The published amount records the default by carrying that parameter pin and by not carrying a closure pin and not carrying `resolved_input`. Two published amounts that both equal box 1 are distinguishable: the no-link amount pins the parameter; the covered amount whose reductions sum to zero pins each reduction and each link instead.

This is not a closure admission. `resolve_closure_admissions` admits a family only when a mapping honours the declaration and exactly one closure finding on the family's current horizon is literal `True`. That admission means the member set is complete. An absent link means nothing was described, not that the statement covers no borrowing. The operation has no `source_set`, writes no `closure_reads`, and never calls that function. `audit_collect_authority` would also reject a rule that collected a family whose `authorizes_subtotal` was the reduction symbol while publishing `demo.tax.statement-facing-amount`. The statement rule does not collect that family, so it does not take on that restriction, and it does not need an exception from it.

The default does not declare the link set complete. A later current link, on a later run, is a recorded link and is covered or uncovered under sections 4 and 5. The earlier default publication is then stale because its inputs changed, which is ordinary re-derivation, not a revision of the default's meaning.

## 7. What does not change

- The `collect` and `count` arms in `evaluator.evaluate`, including empty-collect `SOURCE_SET_UNCLOSED` and count's requirement that `source_set` be in `closed_sets`. `collect_categorical_all_equal` is likewise unedited. *(Amended 2026-09-24, ADR 0075.)* Section 2 does not reject a package in which another member applies those ops, or a scalar binding, to `links` or `reductions`. A `collect` of the link type returns decimals, or blocks on a non-number, and does not return key maps.
- *(Amended 2026-09-24, ADR 0075.)* `marshal_run_context` gains an emission-only name set. The input-binding loop and the legacy fallback still consult only `collect_names`, and `marshal._rule_required_symbols` does not change. A sibling fact type's scalar binding is unchanged, because its symbol is not the link type: one current finding still binds, and several agreeing current findings still bind `matches[0]`. An input binding whose symbol is the link type binds as it would if the type were not collected.
- `rule-artifact.v1` through `rule-artifact.v9`, byte for byte. v9's `selection` and `aggregation` stay id-gated.
- `artifact-package.v1` through `artifact-package.v30`, byte for byte. v30 does not admit a v10 rule.
- `fact-type.v2` `optional_default`, and both places that manufacture it (`_Run.__init__`, `subject_dispatch._optional_default`).
- `source-family.v1`, `source-family.v2`, `source-closure-mapping.v1`, `source-closure-mapping.v2`.
- `resolve_closure_admissions` and `audit_collect_authority`.
- Subject dispatch for a rule whose `value` does not contain `link_coverage`: same join, same optional default, same one-source binding, same block and inapplicable rows.
- Every other caller of `_append_live_source`: still no keys unless that caller passes them. This contract does not start passing keys from any other caller.
- `bound_sources`, including its refusal to read `env.sources`.
- Other per-subject callers. Pairing dispatch is not this path.
- Existing adopted rule versions. Nothing is migrated onto v10 by this contract. A rule moves to v10 only by a new citizen, when its content is this behaviour.
- `derivation-record.v9`, byte for byte, including its `code` enum. `records.CURRENT_RECORD_SCHEMA` stays `"derivation-record.v9"`. `RECORD_CODES` does not gain a member.

Per-subject isolation is the same loop that already evaluates one subject at a time. This contract does not add a cross-subject pass.

## 8. Test obligations for stage B

Stage B's tests are synthetic `demo.*` identities. Minimum set:

1. **Flip `ObservedUnresolvedLinkDefect.test_one_of_two_links_unresolved`.** Both links stay. The institutional reduction blocks and is not a live source. The statement blocks `DEPENDENCY_INVALID`. `missing` is exactly `["demo.finding.link.p3-inst"]` (or that id sorted with any other uncovered link). The published amount 1500 does not appear. The institutional link's finding id is on the statement disposition's input pins. The private reduction is not treated as the whole reduction.
2. **Flip `ObservedUnresolvedLinkDefect.test_only_recorded_link_unresolved`.** The only recorded link is uncovered. The statement blocks `DEPENDENCY_INVALID` naming that link's finding id. It does not block `SOURCE_SET_UNCLOSED`, and `missing` is not `[demo.tax.link-reduction]`.
3. **No link.** A statement with no joined `demo.tax.statement-to-borrowing` source publishes box 1 minus the parameter (1500 when box 1 is 1500 and the parameter is 0). The publication pins the parameter and the box. It does not pin a closure mapping, a closure finding, or a link. `resolved_input` is absent. This includes a run in which that name has no source at all: per-subject dispatch still installs an empty slot, and the outcome is this default, not `link-coverage-scope-unbound`. *(Amended 2026-09-24, ADR 0075.)* Zero rows still take this default, including when the subject's keys are absent. Present link rows that share no key name with the subject do not: that subject blocks `DEPENDENCY_INVALID` with `missing` `["link-coverage-unjoinable"]`, and it does not publish the parameter. A shared key name whose values disagree stays this default. A joined reduction on an otherwise unjoinable link list is still the orphan, not this block.
4. **All links resolved.** Both reductions numeric. The amount is box 1 minus their sum. The amount's own input pins include each reduction finding id and each link finding id.
5. **Inapplicable reduction.** The link guard is false, so no reduction source is appended. The statement blocks `DEPENDENCY_INVALID` naming that link. It does not publish, and it does not copy a reduction row (there is none).
6. **Blocked reduction** is the flipped tests above (the reduction blocks `DEPENDENCY_ABSENT` on the schooling status). The statement's `missing` is the link finding id, not `demo.tax.schooling-status`.
7. **A published zero covers.** A not-adverse link whose reduction published `0` is covered. The statement publishes. It does not block on that link.
8. **Correction of a link.** Re-derive after the link's current finding is a successor with the same keys. The amount pins the successor link finding and not the displaced one.
9. **Withdrawal of a link.** After the link is not current, it is not a source. The reduction is not a source on the next run, because no current link subject re-derives it, and marshal does not load the prior derived finding. The statement takes the no-link default. If a reduction source is still joined in the same run, the statement blocks `DEPENDENCY_INVALID` naming the reduction finding id. That is the in-run orphan check. Stage B keeps it and does not report it as a missing displacement edge.
10. **Another statement is isolated.** South's statement finding and its disposition row stay byte-identical to the run that did not uncover North's link. West, with no link, publishes its own default in the same run North blocks.
11. **Successful pins.** Asserted on item 4: every covered link and every covered reduction is an input pin of the amount itself.
12. **The block names the link.** Asserted on items 1, 2, and 5: `missing` is the uncovered `finding_id` values, sorted, and not the rendered fact id.
13. **An undeclared empty collection still blocks.** A `collect` with no closed `source_set`, including an empty reduction collect on a rule that does not use `link_coverage`, still blocks `SOURCE_SET_UNCLOSED`. `count` of rows whose `source_set` is not closed still blocks. Existing `ObservedMechanismLimits` cases that assert those two facts stay true.
14. **The rule validates as a published production rule under the new schema.** The worked example validates against `rule-artifact.v10`. A package on `artifact-package.v31` whose members are the worked example, the parameter, the link fact type, the reduction rule, and the citation, accepts the rule. The reduction rule publishes `reductions` and `ref`s `links`, and it does not otherwise name either string. The same rule is rejected as a member of a v30 package. A v10 rule that puts `link_coverage` in `when`, or points `reductions` at a name no member publishes, is rejected with `LINK_COVERAGE_INVALID`. *(Amended 2026-09-24, ADR 0075.)* Putting `links` or `reductions` in `requires` is accepted. `LINK_COVERAGE_NAME_REUSED` is not raised. A copied `link_coverage` on a second rule id is not rejected for the copy when the two nodes name different strings: there is no id gate. A second node that repeats `links` or `reductions` is not rejected for the repeated string. The collect list `_resolved_run_material` builds for a package that contains this rule includes neither `links` nor `reductions`. `links` is on the emission-only set. `reductions` is on neither list. That admission is not a source-family edge. Evaluated through ordinary `attempt()` with no keyed slot, that copy blocks `link-coverage-scope-unbound` and does not publish a figure from run-wide sources. That fail-closed result is not a scheduler.
15. **Keys missing.** A candidate of either declared name with `keys is None` makes `_scope` return `None` for that name. Per-subject dispatch installs the `keys_unavailable` sentinel, not an empty list. The statement blocks `link-coverage-keys-unavailable` and does not publish the default.
16. **Non-numeric reduction.** A published reduction whose value is not a number blocks `DEPENDENCY_INVALID` naming the link and does not coerce the value to zero.
17. **Reusable names.** *(Amended 2026-09-24, ADR 0075.)* Validation accepts a sibling that names the link type in `requires`, an input binding's `symbol`, an input binding's `fact_type.id`, a `ref`, a `collect`, or a `count`. `LINK_COVERAGE_NAME_REUSED` is not raised for those uses, nor for the same uses of `reductions`, nor for an attachment rule that names either string. The reduction rule's `ref` of `links`, and its `publishes` equal to `reductions`, stay accepted. A package marshals every other rule's scalar inputs as it did without these two names on `collect_names`. The witness is a sibling fact type: one current finding still binds, and several agreeing current findings still bind `matches[0]`. The link rows are present as sources because the link type is on the emission-only set, not because it is a collect name. An input binding whose symbol is the link type binds as it would if the type were not collected: one finding binds, several agreeing findings bind `matches[0]`, and disagreement stays unbound. A `ref` of the link type outside dispatch binds a run-wide scalar through the legacy fallback when the current values agree, and does not bind when they disagree. A sibling `collect` of the link type returns decimals, or blocks `DEPENDENCY_INVALID` from `_as_decimal` on a non-number. It does not return key maps. A closed `count` of the link type counts the emitted rows. `_resolved_run_material` returns the link type on the emission-only set and returns neither name on `collect_names`.

Items 15 and 16 are the fail-closed identity cases in section 3. They are obligations because a stage B that only flips the happy tests can ship a `fact_id` comparison without failing items 1–14.

## 9. Governance

Gate 1, scored 0–2 on the four axes in `PROJECT_PLANNING.md` ("Prototype Economic Gates"). The proposition is: the coverage-checked reduction total is the `link_coverage` operation on `rule-artifact.v10`, with the outcomes in this document.

| Axis | Score | Reason |
| --- | --- | --- |
| Future blast radius | 2 | The operation is general grammar, not one rule id. Admitting it touches every rule-schema admission set. *(Amended 2026-09-24, ADR 0075.)* `live._resolved_run_material` returns the link type on an emission-only set and does not register `reductions`. `CURRENT_RECORD_SCHEMA` does not move: an uncovered link reuses `DEPENDENCY_INVALID` on `derivation-record.v9`. The `collect` and `count` arms, closure, currency, existing rule bytes, and the record schema do not move. `marshal_run_context` gains that emission-only set; its input-binding loop and legacy fallback still consult only `collect_names`, and findings emitted only for the new set are not marked used. Another member's scalar binding does not move. A sibling may `collect` or `count` the link type; those arms are unchanged and a `collect` returns decimals, not key maps. |
| Migration cost | 1 | New schema versions beside immutable history (`rule-artifact.v10`, `artifact-package.v31`). No existing rule, package, or record is rewritten. Tests that pin the current record schema at v9 stay on v9. |
| Residual uncertainty after paper | 1 | The homes are separated by the P3 measurements. What paper does not execute is the next run after a link withdrawal (the reduction is absent because it is not re-derived, not because marshal drops a displaced derived finding), and the fact that no scheduler selects per-subject dispatch from the rule. Neither is a fork between the four homes. Scheduling the reduction rule and the coverage rule onto per-subject dispatch is shared with Tracks 1 and 2 and is open for G2. Name confinement does not settle it. Whether a distinct disposition code is needed is deferred to P4 and is not a fork between the homes. |
| Inability to test cheaply during implementation | 0 | Section 8 is the existing probe module plus schema validation. No prototype rung. |

**Total: 4.** That is paper plus an ADR draft, not a prototype. This document is the paper. Tier 2 status does not raise the evidence rung.

**A Tier 2 ADR is required.** The decision is a rule-language schema and a runner behaviour that later rules will be written against. That is the Tier 2 definition in `PROJECT_PLANNING.md` ("Decision Records"): schema shape, artifact identity, runner behaviour. It is the same class as the accepted expression-language ADRs (ADR-0064 for `multiply` / `divide`, ADR-0074 for `bound_sources`). A retrospective cannot publish a schema. Gate 1's score of 4 means the ADR does not need a prototype first.

The ADR is stage B's, after this contract is reviewed. Its decision, in one paragraph:

*(Amended 2026-09-24, ADR 0075.)* A statement amount subtracts, from box 1, the reduction total declared by the `link_coverage` operation on `rule-artifact.v10`; earlier rule schemas stay as published. The operation matches each current link to its reduction by equality of the structured key tuples those sources already carry, never by a rendered fact id. No current link produces box 1 minus the value of a named parameter, and that publication pins the parameter and not a source-family closure. Present link rows that share no key name with the subject are not that empty case: they block `DEPENDENCY_INVALID` with `missing` `["link-coverage-unjoinable"]`, before the default, and only when no earlier block (an orphan reduction, missing keys) already fired. Zero rows still take the parameter; joinability with no rows is open for G2. Every current link with exactly one numeric reduction produces box 1 minus the sum of those reductions, and the publication pins each of those reductions and each of those links. Any current link without that reduction blocks `DEPENDENCY_INVALID`, and the disposition's missing list is those links' finding ids. That code does not distinguish an uncovered link from an orphan reduction, a duplicate link map, a non-numeric reduction, or an unjoinable link row on the same subject; a distinct code, if the durable reader needs one, is a later charter and not this decision. Ordinary `collect` and `count` arms, source families, and closure admission are unchanged, and an empty collection that was not declared closed still blocks. The link type is emitted through a channel the input-binding loop and the legacy fallback do not consult, and those findings are not marked used. The reduction name is not registered. Package validation does not confine either string. Another member may name the link type. A sibling `collect` returns decimals, not key maps. A `ref` outside dispatch binds a run-wide scalar through the legacy fallback only when the current values agree. No other symbol's scalar binding changes. How a production run schedules either rule onto per-subject dispatch is not this decision. It is open for G2.

Stage B also appends the schema-intent ledger event for `rule-artifact` v10 and `artifact-package` v31 before editing those schemas. It does not open a `derivation-record` version. That ledger is not this assignment.

## 10. Evidence boundary

P3 and the P3 repair ran hand-assembled `_Run` values. The test calls `evaluate_subject_scoped_rule` itself. The rules are built by `_t2_rule`, which sets `schema` to `rule-artifact.v6` and omits `scope`, `pins`, and `blocked`, and the `collect` nodes omit `source_set`. They are not validated as published production rules. v6 and v9 both require `source_set` on `collect`. The evaluator still runs a non-empty `collect` that omits it. Those runs show what the current operators do with joined sources. They do not show that a schema-valid rule behaves.

Nothing in those runs, and nothing in this contract, establishes what a durable reader sees. The disposition row and the in-run pins are specified here. How a later reader projects them is P4.

Currency in the probes is `compute_currency` over a `FindingState`, and marshal then drops findings that are not current. That is the currency this contract relies on. It is not an act-log fold, and this document does not claim one.

Per-subject dispatch is not selected by the rule. Calling code does, for the reduction rule and for the coverage rule. A production run that attempts either through ordinary `attempt` does not perform the per-subject outcomes. The coverage operation fail-closes `link-coverage-scope-unbound` there. Stage B's item 14 requires that fail-closed behaviour and does not require a dispatch marker. How per-subject rules are scheduled in a production run is shared by Tracks 1–3. This contract does not settle it. It is open for G2.

## Not in this contract

- No edit to `collect`, `count`, source families, or closure admission.
- No comparison of rendered `fact_id` strings or symbol suffixes.
- No hard-coded check for one rule id inside subject dispatch.
- No claim that the link set is complete when the default is used.
- No durable-reader behaviour (P4). Whether a distinct disposition code is required is decided there, from that reader, and is not decided here.
- No `derivation-record.v10`, and no `LINK_UNCOVERED` code.
- No schema file, package member, or ADR file in this assignment.
- No scheduler that selects per-subject dispatch from rule content. Tracks 1–3 share that gap. It is open for G2, not settled here.

## Review disposition

Independent review: `temp/a4-pass2/track3a-review.md`, against this document as committed at `df1abb02`.

1. **Link type never admitted as a source (defect).** Specified the production admission. `live._resolved_run_material` appends every `link_coverage` node's `links` and `reductions` to `collect_names`, with no source-family edge and no closure read. `marshal_run_context` is unchanged and still emits a `SourceFact` only for a collected name that matches a current kernel finding. `subject_dispatch.evaluate_subject_scoped_rule` installs the slot for both declared names on every subject, empty when no rows join, so no link anywhere in the run is the default, not `link-coverage-scope-unbound`. A validated package cannot leave the link type uncollected. The match rule, the three outcomes when the slot holds rows, and the unchanged `collect` / `count` / closure behaviour are kept.
2. **Missing keys fall through to the default (defect).** For the two names the node declares, `subject_dispatch.evaluate_subject_scoped_rule` installs the sentinel `keys_unavailable` when `_scope` returns `None`, and the operation blocks `DEPENDENCY_INVALID` / `link-coverage-keys-unavailable` instead of storing `[]`. `_scope` is unchanged. The passing identity claims are kept: the match is the key map, not `fact_id`; an orphan, a duplicate link map, two reductions, and a non-numeric value still block and do not publish.
3. **Nothing ordinary changes (pass).** Kept. No edit.
4. **Withdrawal and `use_v2` (defect on the mechanism; the record-code facts passed).** Replaced the displacement-edge account. Derived findings are never marshalled. A withdrawn link's reduction is absent on the next run because no current link subject re-derives it. The orphan check stays as a defensive in-run check and does not diagnose a missing displacement edge. ADR-0010 decisions 4 and 5 stay as a description of the subject pin, not as the marshal account. The correction paragraph is kept. Corrected `use_v2`: it is per run (`_Run.__init__` and `run_and_record`). A v10-only run needs `rule-artifact.v10` added to that set. A v10 rule that shares a run with any v2–v9 rule already records `code` and `missing`.
5. **The home (pass).** Kept, including the overturn conditions that are about the operation. The overturn condition that adopted a new disposition code is replaced by the record decision below.
6. **The record bump (not decided).** Adopted no `derivation-record.v10`. An uncovered link blocks `DEPENDENCY_INVALID`, and `missing` is exactly those links' `finding_id` values, sorted. Removed `LINK_UNCOVERED` from the outcomes, the test obligations, the worked example, and the consequence list. Stated what is lost: the code does not distinguish an uncovered link from an orphan reduction, a duplicate link map, or a non-numeric reduction on the same subject. P4 decides, from the durable reader, whether a distinct code is needed; if it is, the record bump is chartered then. Gate 1 scores stay 2, 1, 1, 0, total 4. The blast-radius reason no longer says the record schema moves, and the migration reason no longer says v9 record tests must move.
7. **Test obligations and governance (pass).** Kept, apart from the code names and the withdrawal report, which now match the decision and the withdrawal account. The Gate 1 band is unchanged: paper plus an ADR draft. Tier 2 status does not raise the evidence rung.
8. **Evidence boundary (pass).** Kept. P4 remains the durable reader, and the distinct-code question is named as belonging there.

Second round: `temp/a4-pass2/track3a-confirm.md` §2 and §4, against the contract after the first repair. Both defects are the same registration. Round 1 item 3 kept the `collect` and `count` arms. It did not confine another member's use of the two names once they are on `collect_names`.

9. **Collect-name cross-effect (defect).** Confined by package validation, not by a change to marshal. `package_validation.validate_package` accepts a package containing a `link_coverage` node only when `links` is named by that node and by the reduction rule's `ref`, and `reductions` is named by that node and is the predecessor's `publishes`. No other member may name either string in `requires`, an input binding's `symbol` or `fact_type.id`, a `ref`, a `collect`, a `count`, or a `collect_categorical_all_equal`. The finding code is `LINK_COVERAGE_NAME_REUSED`. `marshal_run_context` stays unchanged, and so do `marshal._rule_required_symbols` and the evaluator arms. That confines the four effects: no binding has either string as `symbol`, so an agreeing multi-match is not dropped; the legacy fallback's loss of a `links` scalar hits no other member, because none may `requires` or `ref` it; no sibling `collect` of `links` can leave the empty path or block `DEPENDENCY_INVALID` from `_as_decimal`; no closed `count` of either name can count the new rows. Stage B obligation 17 rejects each sibling use and requires a sibling fact type's scalar binding, one finding and several agreeing findings, to stay as it is. Gate 1 scores stay 2, 1, 1, 0, total 4. The blast-radius reason now says `marshal_run_context` and those sibling uses do not move, because validation rejects the uses. The residual reason now names the scheduler as open for G2. The limit this does not solve is stated in section 2 and section 10: nothing in rule content selects per-subject dispatch, ordinary `attempt` of either rule does not perform the per-subject outcomes, and scheduling those rules is open for G2.

10. **Attachment-rule symbols (foreman fix after the second confirmation).** `marshal._rule_required_symbols` returns attachment rules' requirement and completeness symbols before any `requires` or `ref` walk, and the legacy fallback drops the scalar for a type id in `collect_names` before consulting them — so an attachment member naming `links` would have lost its scalar while passing the ban. The ban now covers every attachment symbol field that function reads, stated generally as any string it returns for a member other than the reduction rule; obligation 17 adds the attachment rejections.
