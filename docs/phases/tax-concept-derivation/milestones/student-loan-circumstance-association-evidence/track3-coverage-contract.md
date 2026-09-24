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

**What the runner and marshal must admit.** Marshal's walk of names declared outside `requires` currently recognizes rule schemas v3 through v9 only (`marshal._declared_symbols`). The runner's `use_v2` set stops at v9, and a rule outside that set does not record `code` and `missing` on the disposition. Both lists gain v10 and nothing else about their behaviour changes. The evaluator gains one arm. It does not gain a change to the `collect` or `count` arms.

**Blast radius.** Every admission frozenset that names `rule-artifact.v9` as the top of the ordinary rule set has to learn v10 or a v10 rule is inert (`package_validation._SUPPORTED_SEMANTIC_SCHEMAS` and the rule-schema sets, `live.py`, `authorization_closure.py`, marshal, runner). Existing v1–v9 rules are not rewritten. The operation is general grammar: any v10 rule may declare it. It is not registered to one rule id. That is deliberate, and it is the opposite of ADR-0074's package-acceptance gate for `bound_sources`. The cost of that generality is in section 2: outside a per-subject scope the operation fail-closes rather than scanning every statement.

A new disposition code is not in `derivation-record.v9`'s closed `code` enum. The subject-scoped recorder rewrites a code that is not in `RECORD_CODES` to `DEPENDENCY_INVALID` (`runner._Run.evaluate_subject_scoped_rule`). A distinct code therefore needs `derivation-record.v10`, and `records.CURRENT_RECORD_SCHEMA` is one constant for every use_v2 closing record, not a per-rule choice. New runs would write v10; v9 records stay valid history. That constant is the widest consequence of this home. It is accepted in section 5 rather than avoided by overloading an existing code.

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

**Schema.** That new citizen, and still a rule successor, because v9 has no field or expression that means this. Two schemas, where the operation needs one rule schema plus the package and record successors the operation's consequences already require.

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
- Overturn the new disposition code (and with it `derivation-record.v10`) if a consumer can reliably tell "this link's reduction is missing" from "this symbol is absent" using `missing` alone under `DEPENDENCY_ABSENT`. Section 5 says why that overload was rejected. A review that shows the global record-schema constant moving is worse than that overload may reverse the code and drop the record successor. It would not reverse the operation.

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

The node returns one decimal. It appears exactly once, inside `value`. It does not appear in `when`. `links` and `reductions` do not appear in `requires`. Package validation rejects any of those.

Package validation, beyond the schema, accepts a v10 rule declaring this node when all of the following hold, and not by an allowlist of rule ids:

- `links` and `reductions` are different strings.
- `links` is a fact type on the package fact surface. It is the kernel fact for the recorded link, not a derived symbol.
- `reductions` is the `publishes` value of another rule member, and that member is a predecessor of this rule in the package graph.
- `empty.parameter` is a package member, id and version exact.
- The node is not walked by `_iter_collect_source_sets` and not seen by `audit_collect_authority`. It adds no source-family edge.
- It is not checked by `BOUND_SOURCE_TARGET_UNDECLARED`. That check requires the name to be a fact type of an admitted bundle. The reduction is derived, so reusing the check would reject a well-formed rule.

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
  "blocked": { "code": "LINK_UNCOVERED", "missing": [] },
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
| Any joined link or reduction for the named sources has `keys is None` | `DEPENDENCY_INVALID` | `["link-coverage-keys-unavailable"]` |
| A joined reduction's key map equals no joined link | `DEPENDENCY_INVALID` | that reduction's `finding_id`, sorted if more than one |
| Two joined links have the same key map | `DEPENDENCY_INVALID` | both links' `finding_id` values, sorted |
| One link's key map equals two or more reductions | `DEPENDENCY_INVALID` | that link's `finding_id` |
| The matched reduction's value is not a number, including a boolean | `DEPENDENCY_INVALID` | that link's `finding_id` |

No row in those cases is treated as zero, dropped, or paired by `fact_id`. A missing lattice entry is already `keys=None` at marshal time. The operation does not repair it by parsing the rendered id.

The checks run in the order of that table. An orphan reduction is reported before an uncovered link on the same subject, so a stale reduction cannot be ignored in favour of a block that names only the link, and cannot be ignored in favour of the default.

Subject dispatch installs `keyed_sources` for the subject and for every name `_scope` joined, including a name whose joined list is empty. Empty and unbound are different. Empty links with no orphan reduction is the default path. Unbound is a programming error of the caller and blocks.

The slot is a new defaulted field on `Environment`, the same pattern as `bound_sources`. Ordinary `collect` reads `env.sources` and does not read the slot. The operation reads the slot and does not read `env.sources`. Populating the slot from the rows `_scope` already selected does not change who joins to the subject.

## 4. Currency

Only current findings are marshalled (`marshal_run_context` iterates `currency.current_finding_ids`). A link finding that currency does not list is not a source and is not a recorded link.

**Correction.** A corrected link is a new finding for the same fact: same key tuple, new finding id. The displaced finding is not current. The next run marshals the successor. The reduction rule runs on that successor as its subject, so the reduction source's keys are the successor's keys and the reduction's input pin is the successor's finding id (the subject pin `_assemble_pins` already adds). The amount then matches them by those keys. The pin walk of the amount reaches the successor link, not the displaced finding. This is a re-derivation, the way P3's exhausting-portions case already re-derives after an enrolment correction. It is not an in-place edit of a live source.

**Withdrawal.** A withdrawn link is not current, so it is not a recorded link. The reduction that pinned the link is a displacement target of that pin, not a root (ADR-0010 decision 4: an `input` pin naming a finding id is a derivation edge; decision 5: the derived finding leaves currency by that edge). The next run does not marshal it. The statement sees no link and no reduction and takes the default. Taking the default here does not assert that the link set is complete. It asserts that no current link joined.

If a reduction source is still joined after the link is gone, section 3's orphan check blocks `DEPENDENCY_INVALID` and names the reduction's finding id. The default is not published. That block means the displacement edge was not there. Stage B reports it. Stage B does not delete the check to make withdrawal look like the default.

**What a blocked or inapplicable reduction is.** Subject dispatch appends a live source only for a publication. A blocked reduction is on `run.blocked` and the disposition ledger. An inapplicable reduction is on the disposition ledger. Neither is a `live_sources` row, and the statement operation does not read those ledgers. The raw link, if still current, is still a source. No matching reduction means the link is uncovered. The reduction row's own `missing` list (in the probe, `demo.tax.schooling-status`) is not copied onto the statement.

A published reduction of decimal 0 is a numeric reduction. It covers the link. It is not the uncovered case and not the default.

## 5. Semantics of each outcome

The operation runs only after the ordinary guard. A false `when` is `inapplicable` for that subject and does not publish the default and does not block uncovered. A `ref` to box 1 that is absent is `DEPENDENCY_ABSENT` for that symbol, which is a missing box, not a missing link.

Pins below are added to the ordinary rule, citation, adoption, and governance pins, and then sorted the way `pins_for` already sorts them. Link and reduction pins from this operation go through a new access-log channel, not through `access.collects`. The collect channel pins every finding id on that source name (`dependency_pins_for_access`). Using it here would pin rows that were not part of this subject's match. That is the leak `bound_sources` was given its own channel to avoid.

### No current link

The link list for this subject is empty, and the orphan check did not fire. The node returns the parameter's `values` as a decimal. It does not return `[]`. It does not record a closure read.

The published amount is box 1 minus that decimal. The disposition is `published`.

Pinned: the box-1 finding (`role` `input`, `origin` `assertion`) and the parameter (`role` `parameter`, the pin's id and version). Not pinned: any link, any reduction, any source-family, any closure mapping, any closure finding.

The finding does not carry `resolved_input`. That field is the closed shape for a manufactured input (`origin` `declared_default` on a fact that was not asserted). This amount is a computation. What records that the reduction came from the default is the parameter pin, which the covered publication does not carry.

### Every current link covered

Each joined link has exactly one numeric reduction with the same key map. The node returns the sum of those reduction decimals, and only those. The published amount is box 1 minus that sum. The disposition is `published`.

Pinned, each once: every covered reduction's `finding_id` and every covered link's `finding_id`, each as `role` `input`, `version` `v1`, `origin` `assertion`. The parameter is not pinned. Closure pins are not present.

The reduction finding already pins its link, because the link was the reduction rule's subject. The amount pins the links as well, on its own pin list. A reader of the amount does not have to walk through the reduction to find the link. P3's defect was the unresolved link missing from both the amount's pins and the walk.

### Any uncovered link

One or more joined links have no matching reduction. The subject blocks. The code is `LINK_UNCOVERED`. `missing` is exactly the uncovered links' `finding_id` values, sorted lexicographically, and nothing else. Not the reduction symbol. Not the rendered fact id. Not the reduction rule's missing list. Not the links that were covered.

Pinned: those same uncovered finding ids, as input pins. No synthetic zero. No parameter pin.

`LINK_UNCOVERED` is added to the runner's closed record-code set so the disposition keeps the code instead of being rewritten to `DEPENDENCY_INVALID`. It is added to the `code` enum of a new `derivation-record.v10` (v9 bytes untouched). The `missing` items stay strings, which v9 already allows; the new schema's job is to admit the code.

Other subjects are separate iterations of the same dispatch. A block for one statement does not drop, rewrite, or pin another statement's finding.

### Undeclared empty collection

A `collect` or `count` that does not go through this operation is unchanged. An empty `collect` whose `source_set` is missing or not in `env.closed_sets` still raises `SOURCE_SET_UNCLOSED` with `missing` of `[source_set or name]`. A `count` whose `source_set` is not closed still blocks even when rows are present. This operation is not a default for that path. A v10 rule may still contain `collect`; if it does, `collect`'s rules apply, including the required `source_set` on the v10 schema.

## 6. The default's declaration

The number comes from the parameter named in `empty.parameter`. In the worked example that parameter is `demo.param.no-link-reduction` at `v1`, and `values` is `"0"`. The operation reads `parameters[id].values` and checks that the citizen's version equals the pin's version. A missing parameter is `DEPENDENCY_ABSENT` with `missing` of `[parameter id]`. A version mismatch is `DEPENDENCY_INVALID` with `missing` of `[parameter id]`. Neither is the no-link success path.

The published amount records the default by carrying that parameter pin and by not carrying a closure pin and not carrying `resolved_input`. Two published amounts that both equal box 1 are distinguishable: the no-link amount pins the parameter; the covered amount whose reductions sum to zero pins each reduction and each link instead.

This is not a closure admission. `resolve_closure_admissions` admits a family only when a mapping honours the declaration and exactly one closure finding on the family's current horizon is literal `True`. That admission means the member set is complete. An absent link means nothing was described, not that the statement covers no borrowing. The operation has no `source_set`, writes no `closure_reads`, and never calls that function. `audit_collect_authority` would also reject a rule that collected a family whose `authorizes_subtotal` was the reduction symbol while publishing `demo.tax.statement-facing-amount`. The statement rule does not collect that family, so it does not take on that restriction, and it does not need an exception from it.

The default does not declare the link set complete. A later current link, on a later run, is a recorded link and is covered or uncovered under sections 4 and 5. The earlier default publication is then stale because its inputs changed, which is ordinary re-derivation, not a revision of the default's meaning.

## 7. What does not change

- The `collect` and `count` arms in `evaluator.evaluate`, including empty-collect `SOURCE_SET_UNCLOSED` and count's requirement that `source_set` be in `closed_sets`.
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

Per-subject isolation is the same loop that already evaluates one subject at a time. This contract does not add a cross-subject pass.

## 8. Test obligations for stage B

Stage B's tests are synthetic `demo.*` identities. Minimum set:

1. **Flip `ObservedUnresolvedLinkDefect.test_one_of_two_links_unresolved`.** Both links stay. The institutional reduction blocks and is not a live source. The statement blocks `LINK_UNCOVERED`. `missing` is exactly `["demo.finding.link.p3-inst"]` (or that id sorted with any other uncovered link). The published amount 1500 does not appear. The institutional link's finding id is on the statement disposition's input pins. The private reduction is not treated as the whole reduction.
2. **Flip `ObservedUnresolvedLinkDefect.test_only_recorded_link_unresolved`.** The only recorded link is uncovered. The statement blocks `LINK_UNCOVERED` naming that link's finding id. It does not block `SOURCE_SET_UNCLOSED`, and `missing` is not `[demo.tax.link-reduction]`.
3. **No link.** A statement with no joined `demo.tax.statement-to-borrowing` source publishes box 1 minus the parameter (1500 when box 1 is 1500 and the parameter is 0). The publication pins the parameter and the box. It does not pin a closure mapping, a closure finding, or a link. `resolved_input` is absent.
4. **All links resolved.** Both reductions numeric. The amount is box 1 minus their sum. The amount's own input pins include each reduction finding id and each link finding id.
5. **Inapplicable reduction.** The link guard is false, so no reduction source is appended. The statement blocks `LINK_UNCOVERED` naming that link. It does not publish, and it does not copy a reduction row (there is none).
6. **Blocked reduction** is the flipped tests above (the reduction blocks `DEPENDENCY_ABSENT` on the schooling status). The statement's `missing` is the link finding id, not `demo.tax.schooling-status`.
7. **A published zero covers.** A not-adverse link whose reduction published `0` is covered. The statement does not block `LINK_UNCOVERED` for that link.
8. **Correction of a link.** Re-derive after the link's current finding is a successor with the same keys. The amount pins the successor link finding and not the displaced one.
9. **Withdrawal of a link.** After the link is not current, it is not a source. The reduction that pinned it is not a source. The statement takes the no-link default. If the reduction is still joined, the statement blocks `DEPENDENCY_INVALID` naming the reduction finding id, and stage B reports that the displacement edge did not fire rather than changing the check.
10. **Another statement is isolated.** South's statement finding and its disposition row stay byte-identical to the run that did not uncover North's link. West, with no link, publishes its own default in the same run North blocks.
11. **Successful pins.** Asserted on item 4: every covered link and every covered reduction is an input pin of the amount itself.
12. **The block names the link.** Asserted on items 1, 2, and 5: `missing` is the uncovered `finding_id` values, sorted, and not the rendered fact id.
13. **An undeclared empty collection still blocks.** A `collect` with no closed `source_set`, including an empty reduction collect on a rule that does not use `link_coverage`, still blocks `SOURCE_SET_UNCLOSED`. `count` of rows whose `source_set` is not closed still blocks. Existing `ObservedMechanismLimits` cases that assert those two facts stay true.
14. **The rule validates as a published production rule under the new schema.** The worked example validates against `rule-artifact.v10`. A package on `artifact-package.v31` whose members are the worked example, the parameter, the link fact type, the reduction rule, and the citation, accepts the rule. The same rule is rejected as a member of a v30 package. A v10 rule that puts `link_coverage` in `when`, puts `links` or `reductions` in `requires`, or points `reductions` at a name no member publishes, is rejected. A copied `link_coverage` on a second rule id is not rejected for the copy: there is no id gate. Evaluated through ordinary `attempt()` with no keyed slot, that copy blocks `link-coverage-scope-unbound` and does not publish a figure from run-wide sources.
15. **Keys missing.** A joined link or reduction with `keys is None` blocks `link-coverage-keys-unavailable` and does not publish the default.
16. **Non-numeric reduction.** A published reduction whose value is not a number blocks `DEPENDENCY_INVALID` naming the link and does not coerce the value to zero.

Items 15 and 16 are the fail-closed identity cases in section 3. They are obligations because a stage B that only flips the happy tests can ship a `fact_id` comparison without failing items 1–14.

## 9. Governance

Gate 1, scored 0–2 on the four axes in `PROJECT_PLANNING.md` ("Prototype Economic Gates"). The proposition is: the coverage-checked reduction total is the `link_coverage` operation on `rule-artifact.v10`, with the outcomes in this document.

| Axis | Score | Reason |
| --- | --- | --- |
| Future blast radius | 2 | The operation is general grammar, not one rule id. Admitting it touches every rule-schema admission set. `CURRENT_RECORD_SCHEMA` is one constant, so a new disposition code moves every new use_v2 closing record to `derivation-record.v10`. Collect, closure, currency, and existing rule bytes do not move. |
| Migration cost | 1 | New schema versions beside immutable history. No existing rule, package, or record is rewritten. Tests that pin the current record schema at v9 have to move with the constant. |
| Residual uncertainty after paper | 1 | The homes are separated by the P3 measurements. What paper does not execute is a link withdrawal's displacement of its reduction, and the fact that no scheduler selects per-subject dispatch from the rule. Neither is a fork between the four homes. |
| Inability to test cheaply during implementation | 0 | Section 8 is the existing probe module plus schema validation. No prototype rung. |

**Total: 4.** That is paper plus an ADR draft, not a prototype. This document is the paper. Tier 2 status does not raise the evidence rung.

**A Tier 2 ADR is required.** The decision is a rule-language schema and a runner behaviour that later rules will be written against. That is the Tier 2 definition in `PROJECT_PLANNING.md` ("Decision Records"): schema shape, artifact identity, runner behaviour. It is the same class as the accepted expression-language ADRs (ADR-0064 for `multiply` / `divide`, ADR-0074 for `bound_sources`). A retrospective cannot publish a schema. Gate 1's score of 4 means the ADR does not need a prototype first.

The ADR is stage B's, after this contract is reviewed. Its decision, in one paragraph:

A statement amount subtracts, from box 1, the reduction total declared by the `link_coverage` operation on `rule-artifact.v10`; earlier rule schemas stay as published. The operation matches each current link to its reduction by equality of the structured key tuples those sources already carry, never by a rendered fact id. No current link produces box 1 minus the value of a named parameter, and that publication pins the parameter and not a source-family closure. Every current link with exactly one numeric reduction produces box 1 minus the sum of those reductions, and the publication pins each of those reductions and each of those links. Any current link without that reduction blocks `LINK_UNCOVERED`, and the disposition's missing list is those links' finding ids. Ordinary `collect` and `count`, source families, and closure admission are unchanged, and an empty collection that was not declared closed still blocks.

Stage B also appends the schema-intent ledger event for `rule-artifact` v10, `artifact-package` v31, and `derivation-record` v10 before editing those schemas. That ledger is not this assignment.

## 10. Evidence boundary

P3 and the P3 repair ran hand-assembled `_Run` values. The test calls `evaluate_subject_scoped_rule` itself. The rules are built by `_t2_rule`, which sets `schema` to `rule-artifact.v6` and omits `scope`, `pins`, and `blocked`, and the `collect` nodes omit `source_set`. They are not validated as published production rules. v6 and v9 both require `source_set` on `collect`. The evaluator still runs a non-empty `collect` that omits it. Those runs show what the current operators do with joined sources. They do not show that a schema-valid rule behaves.

Nothing in those runs, and nothing in this contract, establishes what a durable reader sees. The disposition row and the in-run pins are specified here. How a later reader projects them is P4.

Currency in the probes is `compute_currency` over a `FindingState`, and marshal then drops findings that are not current. That is the currency this contract relies on. It is not an act-log fold, and this document does not claim one.

Per-subject dispatch is not selected by the rule. A production saturation that never calls `evaluate_subject_scoped_rule` for this rule will hit `link-coverage-scope-unbound` and will not perform the three outcomes. Wiring that call is outside this contract. Stage B's item 14 requires the fail-closed behaviour and does not require a new dispatch marker.

## Not in this contract

- No edit to `collect`, `count`, source families, or closure admission.
- No comparison of rendered `fact_id` strings or symbol suffixes.
- No hard-coded check for one rule id inside subject dispatch.
- No claim that the link set is complete when the default is used.
- No durable-reader behaviour (P4).
- No schema file, package member, or ADR file in this assignment.
