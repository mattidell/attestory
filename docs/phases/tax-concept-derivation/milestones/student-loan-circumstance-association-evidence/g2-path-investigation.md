# What stands between this milestone and G2

Read-only investigation. Branch `milestone/student-loan-circumstance-association`, HEAD `666edc94607077440b487c7c47a12168cfb86ec1` (`track 4: reusable link admission (ADR 0075 option B) and the unjoinable block`). Sources: ADR 0075, the milestone plan's G2 row and "A4's second pass", `a4-bounds.md` "Second pass — P4 result" and "Track 4", `a5-stage3-values-and-basis.md` "The carrier is open", `a5-stage4-scope-and-responsibility.md` Part 2, and the code cited below.

Anything not marked **Inferred** was read off those sources or off the code at that commit. This document recommends; it does not decide.

G2 is not reached. Two gaps are still open, and they are different gaps. Scheduling decides whether a production run ever evaluates the per-subject chain. The carrier decides whether a person can be shown what that chain recorded. P4 already ran the chain by hand and showed that the durable record keeps identities and the presentation keeps box 1 and an error code.

---

## Question 1 — scheduling per-subject rules

### What production does today

Nothing in rule content selects per-subject dispatch. `subject_dispatch.evaluate_subject_scoped_rule` says so, and `runner._Run.evaluate_subject_scoped_rule` repeats it: calling code passes `subject_type` and the rule. The production loop never calls it. `runner._execute` publishes associations, optionally attempts the nominee rules, then saturates: while any rule is eligible and unresolved, call `attempt` (or `attempt_attachment`). `live.live_coordinate_run` reaches that loop through `execute_and_record_marshaled` → `execute_marshaled` → `_execute`. The second scheduler, `reference_runner.run_reference`, is demand-driven and calls the same `is_eligible` and `attempt`. It does not call `try_publish_on_run` or the nominee pre-pass.

Pairing-scoped rules are scheduled, and the selection is not in the rule. It is a Python identity test.

1. **Who decides.** `runner._Run.attempt` calls `_try_pairing_scoped`, which calls `supportability.try_dispatch`. That returns `None` unless `rule["id"] == supportability.RULE_ID` (`tax.us.2025.rule.relationship.accrued-supported`). On a match it calls `run.evaluate_pairing_scoped_rule` with `pairing_type`, `left_type`, and `right_type` taken from `supportability` constants (`PAIRING_TYPE`, `ACQUISITION_FACT_TYPE`, `REPORT_FACT_TYPE`), not from the citizen. Later in `attempt`, `is_pairing_scoped_consequence_rule` matches two more hardcoded ids (`pairing_consequences.PAIRING_SCOPED_CONSEQUENCE_RULE_IDS`) and `dispatch_consequence_on_run` calls the same primitive with the same three constants. Aggregate supportability and the current-year subtotal are two further id tests in `attempt`, dispatched by `dispatch_aggregate_supportability_on_run` and `dispatch_current_year_subtotal_on_run`.
2. **What is declared.** The citizens are ordinary rules. The supportability citizen (`rule.relationship.accrued-supported.json`) is `rule-artifact.v7`, `requires: []`, `when: true`, and its `notes` string says it is pairing-scoped. `notes` is free text. `rule-artifact.v10` has `additionalProperties: false` and no dispatch or subject field. The package does not have a dispatch map either: `artifact-package.v31` requires `members`, `input_bindings`, and `entrypoints`, and nothing else that names a subject type.
3. **When in the run.** `identity_association.try_publish_on_run` runs once, before the loop, and only inside `_execute`. It derives pairing findings onto `live_sources` when acquisitions are present and pairings are not. Marshal has already put the acquisition, report, and pairing type names on `collect_names`, but only because `live._resolved_run_material` sees those rule ids and appends `supportability.COLLECT_SOURCE_NAMES`, `pairing_consequences.pairing_scoped_collect_source_names`, and `identity_association.collect_source_names`. A rule that is not one of those ids does not get that collection.
4. **Order against other rules.** `is_eligible` does not use `requires` for these ids. `consequence_eligibility` waits until the supportability rule id is in `run.resolved`, if that rule is in the package. `aggregate_supportability_eligibility` waits for the current-year pairing rule. `subtotal_eligibility` waits for both the current-year rule and the aggregate rule. The comment in `consequence_eligibility` says why: package membership sorts rules by id, so the consequence citizens precede supportability and would otherwise fire, resolve empty, and never see same-run supportability. Checked, not assumed: `package.core-calculations.v34.json` has 371 members and the id list is sorted. In that list the subtotal is at index 293, aggregate supportability at 294, the current-year pairing rule at 295, and accrued-supported at 297. No schema constraint and no check in `package_validation.validate_package` was found that rejects an unsorted `members` array. The gates exist because this package is sorted that way, and because `evaluate_pairing_scoped_rule` marks the rule resolved after one call even when it published nothing.
5. **What the symbol table does not do.** `runner._Run._record_derived_publication` stores `self.symbols[finding["symbol"]]`. Pairing symbols are suffixed (`supportability.symbol_for` → `SUPPORTABILITY_SYMBOL|pairing_fact_id`). The unsuffixed `publishes` name is not entered. Downstream pairing rules do not become eligible by seeing that name. They become eligible because a predecessor **rule id** is resolved.

Per-subject publication has the same symbol shape and none of the intercept. `subject_dispatch.evaluate_subject_scoped_rule` sets `symbol = f"{rule['publishes']}|{subject_fact_id}"`. The runner records that symbol, appends a same-run source whose **name is the unsuffixed prefix** and whose keys are the subject's keys (`_append_live_source_from_finding`), and marks the rule resolved. `attempt` never calls `evaluate_subject_scoped_rule`. A v10 coverage rule that reached ordinary `attempt` would be evaluated once, with `keyed_sources` unset, and `evaluator._link_coverage` would block `link-coverage-scope-unbound`. A status or responsibility rule, which has no such operator, would be evaluated once against the run-wide environment. `finalize_unreached` does not call `attempt` for an ordinary rule, so it does not hit the pairing intercept either. It evaluates `when` and `value` itself. A per-subject rule that the loop never finds eligible takes that ordinary fallback.

### The chain that has to be ordered

The probe's hand order, in `_t2_execute` and `_p3b_execute`, is three calls with three subject types:

| Step | Rule | `requires` (probe) | Subject passed by the caller |
| --- | --- | --- | --- |
| Status | `demo.rule.schooling-status` | financing, enrolment | financing claim |
| Link reduction | `demo.rule.link-reduction` (validated shape `_scenario_reduction`) | schooling-status only; the link is a `ref` inside `value`, not a `requires` entry | the link type `STATEMENT_BORROWING` |
| Statement amount | `demo.rule.statement-box-minus-reductions` | box 1 only | box 1; `link_coverage` names the link type and the reduction rule's `publishes` |

**Inferred from those three shapes, not from a comment:** the subject type cannot be recovered from `requires`. The status rule's subject is one of two requirements. The reduction rule's subject is not in `requires` at all. The amount rule's subject is box 1, while the type whose keys the operator joins is the link. A scheduler that guessed "the first requirement" or "the type named by `link_coverage.links`" would assign the wrong subject on at least one of the three.

Order is load-bearing because dispatch resolves the rule id once. The reduction joins schooling-status sources by shared key names (`subject_dispatch._scope`). Those sources exist only after the status call has appended them. If the reduction runs first, status is not in `run.symbols` under the unsuffixed name (the publication is keyed) and there is no source to join, so a required status with no `optional_default` blocks `DEPENDENCY_ABSENT` for that subject and the rule id is resolved. The amount rule does not `require` the reduction symbol. `link_coverage` reads the reduction **source name**. An empty reduction slot beside a present link is an uncovered link, not "the reduction has not run yet". The hand-assembled runs avoid both traps by calling status, then reduction, then amount.

The predecessor edges are already written, under names the saturation loop does not treat as edges:

- The reduction's `requires` entry `STATUS` equals the status rule's `publishes`.
- The amount rule's `link_coverage.reductions` equals the reduction rule's `publishes`. `package_validation._link_coverage_issues` already checks that exactly one other rule publishes that name.

What is not written anywhere is which fact type is the subject of each rule.

Ordinary eligibility cannot express the wait. `is_eligible` asks `req in self.symbols` for the unsuffixed name. Keyed publication never inserts that name. Collect-name facts are also absent from `self.symbols` when more than one current finding exists (`marshal.marshal_run_context`: several matches of a collect name are sources, not a scalar input). Financing, links, and box 1 are that case as soon as a return has two of them. A per-subject rule whose `requires` lists those types stays ineligible forever, then `finalize_unreached` evaluates it once as an ordinary rule.

`reference_runner.run_reference` has a second copy of the same mistake. It indexes producers by unsuffixed `publishes` and stops when that string is in `state.symbols`. After a keyed dispatch the unsuffixed name is still absent, so demand does not observe the chain. Any fix that lives only in `self.symbols` fixes neither scheduler. The pairing gates work in both because both call `is_eligible` and `attempt`.

### Candidate (a) — a subject declaration on the rule

**Declares the subject type:** a new field on the rule citizen, an exact fact-type pin (`id`, `version`). It has to be on the rule. The three rules in the chain do not share a subject type, so one package-level subject would be false for two of them.

**Schema.** `rule-artifact.v10` is published (`packages/schemas/derivation/published.json`) and `additionalProperties` is false. The field cannot be added to v10. It is a new file, `rule-artifact.v11`, copying the v10 grammar (including `link_coverage`) and adding the subject pin as a required field, so a v11 rule is per-subject and an older rule is not. `artifact-package.v31`'s member `schema` enum lists `rule-artifact.v10` and does not have a free string. Admitting v11 is `artifact-package.v32`. Both checksums are appended. Existing v1–v10 rules and v31 packages stay as they are.

**ADR.** This is the open item in ADR 0075 "Not decided". It is the same tier as that record: a scheduling contract later rules are written against. It can be an amendment of 0075 before acceptance, or a successor. Not a process note.

**Where the runner calls dispatch.** `is_eligible` and `attempt`, which both schedulers share. A v11 rule is not eligible by unsuffixed symbols. It is eligible when every predecessor rule is resolved: a rule in the same run whose `publishes` equals one of this rule's `requires` entries, or equals this rule's `link_coverage.reductions`. If that predecessor is not in the package, do not wait — the same posture as `consequence_eligibility` when supportability was omitted. Subject facts and other collect sources are not symbol gates. `attempt` calls `evaluate_subject_scoped_rule` with the declared subject type and does not also evaluate `value` once. `finalize_unreached` must use that same intercept. Today it bypasses `attempt` for ordinary rules, which is how a rule that never became eligible would publish or block once, unsuffixed.

That eligibility orders the chain without a new order field. Status has no predecessor that publishes `FINANCING` or `ENROLMENT`, so it fires on the first pass, appends keyed status sources, and resolves. Reduction then sees the status rule resolved and fires. Amount then sees the reduction rule resolved and fires. Within one pass, package member order still decides which already-eligible rule runs first. The predecessor gate makes that order irrelevant, which is what the pairing gates already do. Ordinary rules keep today's `requires` test. An ordinary rule that `requires` the unsuffixed statement-amount symbol still never sees it. A return-level total has to be an aggregator in the sense of `dispatch_current_year_subtotal_on_run`: it reads the keyed publications after the per-subject rule has resolved. That aggregator is not one of the three chain rules. **Inferred:** the form line, if it is one number for many statements, is that aggregator, and it should stay an ordinary unkeyed rule. The investigation did not trace the current Schedule 1 student-loan line's `requires`.

**Static binding.** Once `subject` names a fact type, `package_validation.validate_package` can prove the ADR 0075 join before a run. It already builds `fact_types_by_key` from both bundle-nested fact types and bare `fact-type.v2` members. `fact-type.v2` requires `identity_keys`, each with a `name`. For a v11 rule whose `value` contains `link_coverage`, reject the package unless the link type's key names and the subject type's key names share at least one name. That is the property `_scope` uses: shared names, then agreeing values. The static check can see the names. It cannot see the values. ADR 0075 leaves open whether one shared name is a strong enough join. This check should not invent a stronger one.

Zero rows are exactly why the check is static. `_scope` returns `[]` when there are no candidates, before it reads a key. `evaluate_subject_scoped_rule` then treats an empty link slot as a real empty join, and the operator may return the parameter. Present unjoinable rows already block `link-coverage-unjoinable`. Absent rows do not. The package check covers the absent case the runtime cannot see.

Bare fact types do not need to be copied onto the run for that proof. `live._resolved_run_material` sets `fact_types` from `bundle.v1` / `bundle.v2` only. A top-level `fact-type.v2` member is on the resolved graph and on the validation fact surface, and it is not on `RunContext.fact_types`. `subject_dispatch._optional_default` looks up defaults in `run.ctx.fact_types`, so a bare fact type's `optional_default` is invisible at runtime today. ADR 0075 also says the run context must carry bare fact-type declarations for any runtime use of them. **Recommendation on that sentence:** do the joinability proof in package validation, where the bare members already are, and do not widen `RunContext.fact_types` unless some runtime reader of `identity_keys` is actually added. Nothing in `subject_dispatch` reads `identity_keys`. The keys it joins are `SourceFact.keys`, copied from the kernel lattice at marshal time.

**Blast radius.** New v11 and v32 schemas and their manifest entries. Every closed schema-name set that lists `rule-artifact.v10` has to admit v11 or a v11 rule never runs: `live._resolved_run_material`, `package_validation` (the supported-schema set, the compile walk, the reachability walks), `authorization_closure`, `runner` rule-schema tuples, `marshal._rule_required_symbols`. Existing packages and v1–v10 rules do not change behavior. Hand-called `evaluate_subject_scoped_rule` in the probe tests stays valid. The presentation join is not fixed by this candidate.

**Cost.** Two published schemas, one ADR decision, an eligibility rule that understands predecessor publications, and the intercept in both the loop and `finalize_unreached`. No new record code. No change to pairing.

### Candidate (b) — a package-level map

**Declares the subject type:** a new array on the package, each entry a rule member-ref plus a fact-type pin. One entry per per-subject rule. Not one subject for the package.

**Schema.** `artifact-package.v32` only, if the rules stay on v6/v10. `rule-artifact.v10` stays immutable. Smaller schema surface than (a). The map is not on the citizen, so the same rule bytes can be per-subject in one package and ordinary in another.

**Where the runner calls dispatch.** `live.live_coordinate_run` can see the package. `reference_runner.run_reference` and `runner.run` cannot; they see `RunContext`. The production path has to stamp the subject type onto the rule dict, or onto the context, before either scheduler runs. A missing stamp means `attempt` treats the rule as ordinary. For a coverage rule that fails closed (`link-coverage-scope-unbound`). For the status rule and the responsibility rule it does not: they have no operator that refuses an unbound scope. They publish once, or block once, under the unsuffixed symbol. Forgetting a map entry is a silent wrong grain, not a package error, unless validation requires every `link_coverage` rule to appear in the map **and** every rule that publishes a name another per-subject rule requires to appear too. The second half is the status rule. It is easy to miss, because nothing in its bytes says it is per-subject.

**Ordering.** Same predecessor gate as (a), if the stamp is visible to `is_eligible`. Without the stamp, the reference runner and the fixture runner do not share the production behavior. Pairing does not have this split: the id test is inside `attempt`, which both runners call.

**Static binding.** The map is on the package, and `_link_coverage_issues` already runs there with the full fact surface, including bare fact types. The key-name check fits beside it. Same limit as (a): shared names, not shared values. Same recommendation against widening the run context.

**ADR.** Same open item as (a). The contract is "which rules of this package are per-subject", not "this rule is per-subject".

**Blast radius.** One new package schema. `live.py` must thread the map into the context. Every package that adopts v32 must list the map, including packages that have no per-subject rules (empty array), or v32 is not a drop-in successor. Runner intercept is smaller than (a) only if the stamp is the signal. Validation must grow the "you forgot the status rule" check or the failure mode above stands. Presentation is unchanged.

**Cost.** Less schema than (a), more ways to schedule a non-coverage rule once and miss it. The chain's first rule is a non-coverage rule.

### Candidate (c) — a tax-layer hook, like pairing

**Declares the subject type:** constants in a `packages/tax` module, next to the rule ids, the way `supportability.PAIRING_TYPE` sits next to `RULE_ID`.

**Schema / ADR.** None, for the mechanism. ADR 0075's open scheduling item would be answered "the way 0070 and 0071 were answered: code names the citizens". The static key check has no content declaration to read. It would import the same Python map, or it would not exist. Package validation does not import the pairing id lists today. `live._resolved_run_material` does, for collect names only.

**Where the runner calls dispatch.** A new lazy import in `is_eligible` and `attempt`, plus `finalize_unreached`, plus the collect-name block in `_resolved_run_material`. Both schedulers pick up the `attempt` half. The collect-name half runs only on the live path. The predecessor waits are more constants, as `consequence_eligibility` is.

**Ordering.** Works, for the ids the module lists. Status, reduction, amount, and each responsibility rule are listed with their subject types, and eligibility waits on the predecessor id. A producer chartered later is not scheduled until someone edits the module. That is the pairing blast radius, and it is accepted there because those citizens are a closed vertical. It is a poor fit for a grammar that ADR 0075 says any later rule may use. A content author can add a v10 coverage rule, pass package validation, and still have production evaluate it once and block `link-coverage-scope-unbound`. The package is valid. The run is not statement coverage. ADR 0075 already says a schema-valid, accepted package has not established coverage.

**Static binding.** Only if the hook's subject type is visible to the checker. A constant in `packages/tax` is visible to a test and invisible to `validate_package` unless validation starts importing tax modules. Doing that for a general operator inverts the dependency pairing already lives with: derivation importing tax inside `attempt`, behind a lazy import, to break a cycle. Extending that into package validation couples every package check to this milestone's rule ids.

**Blast radius.** `runner.py` and `live.py` gain another tax import. No published schema. Every new per-subject rule is a code change in the same files that know the accrued-interest rule ids. The probe's `demo.*` rules are not those ids, so the hook does not make the existing probes into a production run. It makes a future content module into one, after the ids are copied into Python.

**Cost.** Smallest diff that schedules one named chain. Largest ongoing cost, and it does not put the subject type where the static check already has the fact surface.

### Recommendation

Candidate (a). The subject type is a fact about the rule — which grain it publishes per — and the three rules in the chain have three grains. A package map can omit the status rule and get one unsuffixed publication. A Python id list will not track a later content rule, and the joinability proof then lives apart from the fact types it has to read. v11 plus v32 is the expensive part, and it is the part the publication protocol already expects: v10 and v31 are immutable, so the declaration was never going to land on them.

The runner change that must accompany (a), and would equally accompany (b) or (c): eligibility waits on predecessor **rule resolution**, not on the unsuffixed symbol appearing in `self.symbols`. The intercept has to be on `attempt` and on `finalize_unreached`. The static check is one new condition in `validate_package`, next to `_link_coverage_issues`: the link type and the declared subject type share a key name. Do not widen the run context for that. Do not treat one shared name as a stronger join than ADR 0075 left open.

(a) does not show anyone the result. That is Question 2.

---

## Question 2 — the reader carrier

### What is durable, and what the page reads

`records.closing_record` with `use_v2=True` writes a `derivation-record.v9` closing record whose body is pins and dispositions. It does not write `published` or `blocked`. `production_executor.execute_and_record_marshaled` calls that path and does not call `runner.append_publications`. `live.live_coordinate_run` then writes `out.json` with `dispositions` and no findings, and writes `presentation.json` from `build_presentation_model`. Derived values exist on the in-memory `RunResult.publications` at projection time. They are not in the record and not in `out.json`. P4 measured that: every disposition row lacks `value`, and `subject_fact_id` is not a field on the record. The subject fact id survives only as the suffix of the keyed `symbol`. Rows join on pin `id` and on that suffix.

`act-derived-publication.v1` is not a place to put them either. Its `finding.schema` const is `derived-finding.v1`. The runner's findings are `derived-finding.v2`. Production does not emit the act. Emitting it would not validate against the published act schema.

P4's presentation results, from the `DurableReader…` tests, still hold:

| Case | Record / `out.json` | Presentation, and only if a synthetic field is aimed at the keyed symbol |
| --- | --- | --- |
| Uncovered link | `DEPENDENCY_INVALID`, `missing` is the link finding id, link pinned | `activeCodes: [DEPENDENCY_INVALID]`. No `missing`, no link id. The four invalid shapes render the same bytes |
| No-link default | Parameter pin on the row; box 1 is the only input pin; value not on the row | Citation sites are box 1 only. The parameter id is inside the embedded act, not a citation site |
| Covered chain | Amount pins box 1, both links, both reduction finding ids. Each reduction pins its link and its status. Status pins the financing finding and the corrected enrolment, or a `declared_default` pin | Citation sites are the **leaves**. Status ids and reduction ids are not in the model. The number is the amount. `provenanceGroups` is absent |
| Named conclusion and one responsibility rule | Own rows, keyed symbols, input pins, no values. The responsibility is not an input of the amount. The same rule with subject box 1 blocks `DEPENDENCY_ABSENT` / `missing: [STATUS]` | Not in the model at all |

The join failure is specific. `presentation_projection._dispositions_by_symbol` indexes a row by its `symbol` when the row has one. Per-subject rows have `publishes|fact_id`. `build_presentation_model` loads a field with `symbol = field["binds_symbol"]` and `_one_row` requires exactly one row. The unsuffixed symbol matches nothing (`0 row(s)`). The keyed symbol matches the blocked row without an owning-rule check, because `_require_declared_field_citation_chain` runs only for numeric and categorical dispositions. For a **published** row the same keyed field fails `lacks a joined owning rule`, because that function requires `rule["publishes"] == field["binds_symbol"]` and the rule that ran publishes the unsuffixed name. P4's `join=True` rewrites `publishes` on a copy of the rule to the keyed symbol. That copy is not the rule that ran.

`_one_row` also cannot attach many statements to one field. Two keyed rows for one `binds_symbol` are an ambiguous join. Section ids are `line-{line}`, and duplicate section ids are rejected. One form line and many statement amounts do not fit the current section shape.

The citation-walk page (`packages/presentation/pages/citation-walk.v1.html`) reads `sections`, `citationGroups`, and `attachments`. It renders `citationSites`, the field's own citation, `activeCodes` filtered through the field's declared code list, and attachment tie-out text. It does not read `provenanceGroups`. A blocked line shows the code and the words "No value published". It does not show `missing`.

### The provenanceGroups precedent

For an `attachment-rule.v11` adjustment row that itemizes a derived finding, `_resolve_attachment` appends one object per finding: finding id, attachment id, adjustment kind and label, a reader label parsed from the symbol suffix when it contains `payer=`, citation sites walked from that finding's pins (not only the field's leaves), and `tieOutText` that includes the finding's value (`Recorded contributing reduction …`). `validate_presentation_model` allows `provenanceGroups` as an optional top-level key and checks that the groups line up with citation-group parts. The version string is still `presentation-model.v1`. Adding the key did not publish a schema and did not bump the version.

That is a precedent for the shape: an intermediate derived finding, its value, and its own pins, written beside the flattened field. It is not a carrier for this milestone. It is built only inside the attachment resolver, only for derived adjustment rows, and the page does not read it. P4's student-loan models have no attachment and no `provenanceGroups`.

### How the projector has to change to join a keyed symbol

Independent of which carrier is chosen, a field whose `binds_symbol` is the rule's unsuffixed `publishes` does not meet a per-subject row. The join has to become: a row belongs to the field when its `symbol` is exactly `binds_symbol`, or its `symbol` is `binds_symbol` plus `|` plus a fact id, and its `artifact_id` is a rule whose `publishes` equals `binds_symbol`. The owning-rule check has to accept that pair. It currently rejects it.

That change alone still leaves `_one_row` and the single `resolved` object per section. **Inferred:** the useful join for this return is not "one section per statement". The ordinary view is one line. The per-statement rows are groups under that line, which is the provenanceGroups shape moved from attachment adjustments to form-field sections. A literal one-section-per-keyed-row presentation would also need new section ids, because `line-{line}` collides. Either choice is a `presentation-model` validator change. Neither is a published schema. The page has to be taught to render the groups, or they sit beside the line the way `provenanceGroups` sits beside Schedule B today: present in the file, not on the page.

### Candidate 1 — project the intermediates into the presentation model

**What changes.** `build_presentation_model` and `validate_presentation_model`. A new optional collection, or a widening of `provenanceGroups`, holding one group per per-subject finding the field should expose: symbol, fact-id suffix, value, artifact id, disposition, `missing`, and the pins that are not the leaves. `citation-walk.v1.html` has to render it, including a blocked line's `missing` and a published line's intermediate groups. No change to `derivation-record.v9`. The projector already holds publications, dispositions, the resolved rules, and `FindingState` when it runs. Values and source-finding labels are available there without a new record.

**Uncovered link.** The disposition already has `missing` and the link pin. The projector drops both when it builds a blocked section (`_resolve_field_row` returns the code and no sites). Copying `missing` onto the section, and resolving those ids through `state` when they are recorded findings, names the link. The four invalid shapes stop rendering as the same bytes, because their `missing` lists differ. A code is not required. P4 already settled that. The page's blocked branch has to show the list. Today it shows the code only.

**No-link default.** The parameter pin is on the row and on the embedded finding. Citation sites skip it because `_DEPENDENCY_ROLES` is `input` and `choice`. Emitting parameter pins, or a basis flag taken from an input pin's `origin`, lets the model say the amount pinned a parameter and no link. The approved sentence ("taken as met because nothing you've described says otherwise") is not that pin. No citizen the projector is allowed to copy a string from holds that sentence. Stage 4 traced the allowed string sources: a published value, or a label, description, citation, attachment title, itemization label, or evidence label. A parameter id is not the sentence.

**Covered chain.** Stop collapsing at the leaves. The walk already passes through the reduction findings and the status findings; `_leaf_pins` throws those nodes away. Emitting them, as provenanceGroups emits a nominee reduction, puts each reduction and each status on the model with its value and its pins. The corrected enrolment stays a leaf, distinguishable by being the status row's input pin rather than the only thing the line cites. The amount's number stays the field value.

**Named conclusion.** On this chain the status finding **is** on the downward walk, so emitting intermediates shows it: rule id, keyed symbol, categorical value, and whether the enrolment pin's `origin` is `assertion` or `declared_default`. That is the identity and the basis stage 3 asked the reader to recover. It is not the approved wording.

**Three responsibilities.** Not reached by the downward walk. P4 showed the responsibility row pins the status finding, and nothing on the amount's pin list is the responsibility. Emitting "nodes the field walk passes through" does not emit it. The projector has to walk the other way: dispositions whose input pins name a finding already in the group, or every publication of a rule the field's chain reached. The record can already do that join. The projector does not. Identity is the rule id and the symbol. Circumstance, for the financing-keyed rule P4 ran, is the financing finding on the input pins; the school and period are that fact's keys in `state`, which the projector can read and the derivation record does not store. Treatment is the reverse join from that status to the reduction to the amount, which P4 showed as pin ids across rows. Wording is still absent. The categorical value in the probe is the literal `applies`.

**Case 2, school unknown.** Not what P4 ran. The responsibility rule with subject box 1 blocked `DEPENDENCY_ABSENT` because it `requires` status, and status sources are keyed to financing claims, not to the statement. Stage 4's case-2 grain — the condition tied to the statement, school and programme unknown — needs a rule whose subject is the statement and whose pins do not pretend a school. **Inferred:** once that rule is scheduled and publishes, this carrier can show the statement-scoped symbol, the absence of a school pin, the amount it qualifies, and a short note on the ordinary line. It cannot show the sentences until a wording home exists. The page has no "note on the line, conditions in a contextual explanation" structure. `renderLine` is one disposition. That layout is page work on top of the model, and it is what the owner's choice A asked for. It must not become a question, a confirmation, or a banner on every line. The current blocked banner ("No value published — cannot compute") is the wrong register for a condition that applies and blocks nothing.

**Cost.** Internal model and validator, and the citation-walk page. No published schema. Does not by itself create the case-2 finding or the wording. Does not survive if a later reader ignores `presentation.json` and reads only the derivation record: the values were never written there. The presentation file is already the durable copy of what this path knows how to show.

### Candidate 2 — persist publications, or the conclusions, durably

**What changes.** Either `derivation-record.v10`, so a closing record can carry finding values (and, for a conclusion, the symbol, the pins, and the value), or a new act schema that admits `derived-finding.v2`, plus a call `execute_and_record_marshaled` does not make today. v9 cannot gain a `value` field or a `published` array. The pin vocabulary also has no slot for a reader sentence. `origin` is `assertion` or `declared_default` only.

The projector would then read those stored findings instead of, or as well as, the in-memory publications. The join problem is unchanged: stored keyed symbols still do not equal `binds_symbol`. The page still does not render intermediates. Persistence without the candidate-1 projection puts values in a file the citation-walk does not open.

**What the reader could show.** Everything candidate 1 could show, **after** the same projection and page changes, plus a reader that is not the live coordinator can reconstruct the values later. Identity, circumstance, and treatment are already on v9, as joins. Persistence adds the derived values (`500`, `adverse`, `applies`) and any string someone stores as a value. It does not add a wording home. It does not name an uncovered link in the page until `missing` is projected. It does not display "school unknown" until a finding or a string says that. Case 2's statement-scoped responsibility is still a rule that has to run first.

**Cost.** A published schema (record v10, or an act successor) and every consumer of the closing record, for values the projector already holds in memory at the only moment the page is built. Justified if a reader must work from the record stream alone, without re-running and without `presentation.json`. Nothing in the G2 row says the citation-walk is that reader. The page's input is the presentation model. P4's objection to a new record code still applies to a new record version: the identities are already there, and a version that only adds values does not put them on the page.

### Candidate 3 — reconstruct at read time from the durable record

**What changes.** A reader — `explanation.explain` / `walk_npe`, or a new consumer — run when the page is built, from the closing record plus whatever else is still durable. `explain` walks pins and can return a value only when the caller passes the derived finding, including `value`. The record has the pins and not the value. `walk_npe` finds a published row by `artifact_id` and then looks up an unsuffixed symbol (`r["publishes"] == s`). A keyed row does not match that index. So the existing explainers do not reconstruct this chain. A new reader would join keyed symbols by suffix and by pin id, which P4 showed is enough to recover the **identity** graph: which link, which status, which responsibility, which parameter, whether an input pin is `declared_default`.

Re-deriving the values means running the rules again from kernel findings (those are durable in the workspace) and the rule citizens (durable as content). That is a second run. It is possible only after Question 1's scheduler exists; otherwise the second run is the same hand assembly P4 used. Stage 3's rejected alternative — "leave it to presentation to infer from the value and the rule" — was rejected because the basis would not be on the record. The basis origin **is** on the record. The categorical value is not. Recomputing the value from the rule and the pinned inputs is not the same as inventing the basis, and it is also not what `explain` does today.

**Uncovered link.** `missing` is on the record. A reader of the record can name the finding id. The page still will not, unless projection copies it. The four shapes are distinguishable in the record and identical on the page.

**No-link default.** The parameter pin is on the record. The sentence is not. Re-derivation reproduces the amount, not the sentence.

**Covered chain.** The pin join across rows is the chain. A reader can list it. The page flattens it. Re-derivation reproduces the numbers and then needs candidate 1 to show the nodes.

**Named conclusion.** Identity, rule id, and the enrolment pin's origin are on the row. The value `adverse` / `not-adverse` is not. The enrolment **source** finding is in workspace state, not in the derivation record, so a reader given `state` can show what was asserted. A reader given only the record cannot.

**Responsibilities.** Same as the record join P4 already has, plus the wording gap, plus the case-2 grain the probe's rule did not publish. Re-derivation does not create a wording home.

**Case 2.** Reconstructing "school unknown" from the absence of a financing pin over-reads the record. Absence of a pin means this row did not pin a school. It does not mean the product has decided to say the school is unknown, and it does not produce the short note or the contextual explanation. Those are display choices stage 4 recorded and no artifact stores. **Inferred:** a reconstructor that printed "unknown" whenever a school pin was missing would also print it for any not-yet-joined chain, which is the uncovered-link bug in words.

**Cost.** No schema, if the reader only exposes joins the record already stores. That reader still cannot show values, wording, or the case-2 sentences, and the page still has to change to show the joins. Re-derivation duplicates the run, depends on Question 1, and still needs candidate 1's projection to reach the page. Stage 3 already said the citation-walk does not read the one intermediate structure the projector emits.

### Recommendation

Candidate 1, aimed at the form-field section rather than reused blindly as `provenanceGroups`. The projector is the only component that already has the publications, the dispositions, the rules, and the source findings at the moment the page's input is built. The record should stay v9: P4 showed it already distinguishes the failure shapes and already joins the chain, and a new published version would store values the page does not read. Reconstruction from the record recovers identities a projection can copy more directly, and it cannot recover wording or a case-2 sentence that was never stored.

The projection has to do four things the leaf walk does not:

1. Join keyed rows to the unsuffixed field, and hold many of them as groups under one line rather than as one `resolved` object.
2. Keep the intermediate nodes (reduction, status) instead of collapsing them to leaves, and copy `missing` onto a blocked line so the uncovered link is named.
3. Walk back from those nodes to responsibility rows that pin them, so a condition nothing consumes is still shown. The downward walk will not find it.
4. Leave a place for a wording string and for the case-2 note, and do not invent either from a missing pin.

Wording stays open, as stage 4 left it. The carrier can show identity, circumstance, treatment, the default basis, and the uncovered link without a new published schema. It cannot show the approved sentences until some governed string exists — a content declaration or the consumer — and the citation-walk page has to grow the ordinary-line note and the contextual explanation or the model will carry them unread. Scheduling (Question 1) is what makes the case-2 statement-scoped findings exist to project. The carrier does not schedule them.

---

## What this does not close

G2's bar is still the four behaviours on the nine-credit case, the financing claim with no schooling circumstance, and the bare statement, including the three conditions at the reader. This investigation traces how a production run would have to schedule the chain, and how a reader would have to be shown it. It does not run either. ADR 0075 remains proposed. The wording home remains open. The case-2 responsibility rule, keyed on the statement rather than on a financing claim, was not a rule P4 published; the one P4 ran blocked when the subject was the statement.
