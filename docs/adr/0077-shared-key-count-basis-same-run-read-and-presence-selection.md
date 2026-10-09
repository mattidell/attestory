# ADR 0077 — Shared-key count, declared basis, same-run subject results, presence selection, and scoped supersession

- Status: **accepted** (owner, 2026-10-02) as the implementation contract for Parts 1–5, with one condition: the implementation of Part 5 must guarantee that every production `ActLog` is built over a registry carrying the Part 5 declaration, so the new-write step cannot be skipped by registry choice. Implemented at acceptance: Part 5's recorder binding and read-side check in the tax modules. Everything else in this record is the contract the implementation tracks build.
- Tier: 2. Four rule-language and runner contracts later rules are written against, plus the Part 5 admission invariant. Not a product-thesis or governance-meaning decision.
- Date: 2026-10-02
- Amended: 2026-10-02, Foreman at owner direction — Part 3 states which operators read the declared entries and how a blocked entry refuses.
- Amended: 2026-10-02 — Part 5 refuses an unscoped same-identity rewrite of a declared source while a current dependent names that source. The owner chose admission refusal. This draft records that choice. Parts 1–4 and the Part 3 amendment above are unchanged.
- Amended: 2026-10-02 — Part 5's trigger is a new current finding of the declared source while a current dependent names that source, whether or not that fact id already has a finding. A retraction under ADR 0073 stays admitted. The assertion that follows is refused unless it cites reviewed-scope evidence.
- Amended: 2026-10-02 — Part 5's reviewed-scope exception is a binding, not a citation of an evidence id. One scope evidence authorizes one successor: the box 1 finding the review saw, the corrected amount, and the correction identity. Reuse is refused. The recorder and the read-side check are implemented. Replay of a log that already holds an unbound rewrite stays readable and omits that inclusion from the runners' current-subject set; that omission, and the kernel enforcer, stay proposed.
- Amended: 2026-10-02, Track 1a-5 at owner direction — Part 5 refuses a prohibited write at a new admission step in `ActLog.append`. Every durable writer calls that function, and replay never does. Part 5 is no longer bound in `apply_assertion`. Replay stays readable. It omits an unbound inclusion from the sources rules join, and it still counts that inclusion as present for Part 4. Parts 3 and 4 are replaced by the Track 1a-4 composition, with two repairs. The derived entry pin validates on `derived-finding.v3` and `derivation-record.v10`. The new path's activity also names the statement-keyed unresolved, denied and withdrawn facts Track 3 adds.
- Amended: 2026-10-02, Track 1a-6 at owner direction — An omitted inclusion now reaches its own statement's support decision. Replay supplies, in its place, a system marker of its own fact type that keeps the inclusion's statement identity and finding. The statement publishes `not-supported` whenever any inclusion on it is omitted. The marker, not the person's unresolved-inclusion fact, makes the new path present. Track 1a-5's "counts it as an unresolved inclusion" is replaced.
- Amended: 2026-10-02, Track 1e at Foreman direction — Part 5's example declaration shows the five keys the implementation added so the kernel names no tax field or evidence kind. Single use counts findings of the source fact type: the inclusion-uncertain route's own unresolved status cites the same answer evidence and does not use it up. Case 13 records the implemented way back after a retraction.
- Amended: 2026-10-08, Track 1 at owner direction — The successor worksheet (`tax.us.2025.rule.sli-worksheet` v5, in core calculations v42) replaces the both-present refusal with a per-form combination. The worksheet stays `rule-artifact.v13`: one live path reads each form's combined standing, and one inert path names `tax.us.2025.sli.inert-path-unwritten`, a fact type nothing writes. The path exists so the v13 selection still has two paths. It never activates, and it fails closed if that fact type becomes current. The decision text below is unchanged.
- Evidence: the Track 0c, 0d, 0e, 0f and 1a-3 to 1a-6 reports in the milestone evidence folder, each read on the milestone branch before this record was accepted.
- Implemented: 2026-10-03, at milestone closeout — Parts 1–5 are built and tested (Tracks 1b, 1c, 1e, 3–5, 7, 8). Labels below that read **Proposed** record the state when this record was accepted; the "Answers at implementation" section under Open questions records how each question was settled.

This record proposes one contract for four capabilities the student-loan support chain needs, and one admission invariant. A person records that a loan paid for a schooling and that an interest statement covers that loan. A rule has to count those rows, say what the favorable result assumes, let a return-level rule read each statement's result in the same run, and choose between an old input path and a new one when only one is present. Parts 1–4 are the decisions a later rule is written against. Part 5 refuses a new write before it reaches the log, at a new step in `ActLog.append`. The refused write is one that would make a new finding of a declared source current while a current dependent finding names that source, whether or not that fact id already has a finding, unless that finding is the one successor declared reviewed-scope evidence binds for that source. Replay never runs that step. A log that already holds such a write stays readable. No rule joins the unbound inclusion. A system marker takes its place, so its statement publishes `not-supported` and Part 4 still finds the new path present.

## Context

The student-loan deduction milestone's Track 0 is settled by owner disposition (path A), recorded in the plan's "Track 0 adversarial closure" section. The integration-surface row stays a build obligation. Its three missing engine capabilities, plus the shared-key count from Track 0c, are this ADR. The person-visible Schedule 1 line 21 sentence is not. The plan moves that sentence to worksheet integration.

Two accepted records bound this one. ADR 0075 accepts `link_coverage`: a reduction total over the two lists per-subject dispatch supplies, or a block. ADR 0076 Parts 1 and 2 accept per-subject scheduling and the two containment relationships. One shared key name is not a containment pass. Part 3 of ADR 0076, what several statuses for one borrowing do to the interest, is open. This record does not select it.

The Form 1040 line 2b selection is the precedent for Part 4. No accepted ADR decides that binding. The authorizing record is the nominee-interest return-integration plan, section "Contracts", "Bounded declared path contract": `rule-artifact.v9` and `artifact-package.v30` declare the shape, and package validation and the runtime bind it only to `tax.us.2025.rule.form1040-line2b` version `v8` and to the distinct nominee aggregate producer. The published v9 schema description says the same thing. `packages/derivation/runner.py` sends that one rule to `_attempt_declared_line2b_selection` and blocks every other v9 rule that carries `selection` or `aggregation` with `DEPENDENCY_INVALID` and missing `v9-declarative-binding-unauthorized`. Package validation rejects every other v9 selection with `RULE_SELECTION_UNAUTHORIZED`.

## Decision — Part 1. Shared-key count

**`shared_key_count` counts the current rows of one named fact type that share one named identity key with the subject.** It returns that count, a number, or it blocks. It reads no values. A count of current rows is not a scope mark. Scope is a separate fact.

The measured behavior is Track 0d, "Evidence 5 — what the production count must do". The operator in that probe was a stand-in. `shared_key_count` was not a schema token, and the rows are labeled "executed with the runtime stand-in operator". This part adopts that list as the production contract. Track 0c section 4 recommends this operator over the two alternatives in its section 1. Those alternatives are recorded under "Alternatives considered".

### Shape

A new expression alternative on `rule-artifact.v13`:

```json
{"op": "shared_key_count", "fact_type": "<counted fact type id>", "key": "<identity key name>"}
```

`fact_type` is the id of the fact type being counted. `key` is one identity-key name. The node carries nothing else. The subject is the subject the rule already declares under ADR 0076 Part 1. In the measured case the subject is one statement-inclusion row, the counted type is `tax.us.2025.sli.financing-relationship`, and the key is `borrowing`.

### Validation

On the package fact surface:

- The rule declares a subject. The operator is not valid on a return-level rule.
- `key` is an identity-key name of the subject fact type and of `fact_type`. The check sees declared names. It does not see values.
- The operator appears once in `value` and never in `when`. The same once-only rule is what package validation already applies to `link_count` (`link_count must appear exactly once in value and never in when`, Track 0f item 2).

This check is not a containment check. ADR 0076 Part 2 still says one shared name is not a pass for `joined_contains_subject` or `subject_contains_joined`. Naming `borrowing` here does not make financing rows a joined list, and it does not authorize the borrowing-only edge Part 2 left to Part 3.

Track 0c section 2 records that `rule-artifact.v12` rejects this node: `{"op": "shared_key_count", ...}` is "not valid under any of the given schemas". v12 stays rejected. The node becomes valid on v13.

### Runtime

Evaluated for one subject at a time, inside per-subject dispatch, over current rows of `fact_type`. A row that is not current is not a row: Track 0d evidence 5, "Financing finding not current", returns 0 and pins the inclusion only. The count compares the named key and no other key. Two rows that agree on the key and carry the same category value are two rows. The financing value, the schooling fact, and evidence text are not read. A current row whose value is `cannot-tell` still counts.

The result is one of these, and none falls through to another:

1. **A number.** Every current counted row either agrees with the subject on `key` or it does not. The number is how many agree. Zero is the number 0. Evidence 5: two financing rows, two periods, return 2 and pin both financing findings; one matching row returns 1 and pins that finding; no current match returns 0 and adds no financing pin. Two statements with two borrowings return 1 and 1, and each publication pins its own financing, not the other.
2. **Block, bad counted row.** A current counted row whose keys are null, or whose map lacks `key`, blocks `DEPENDENCY_INVALID`. `missing` is that row's finding id. The row is pinned. The number 1 is not published, and the row is not dropped. Every subject evaluating the rule blocks. Evidence 5: one row with null keys, beside one good row, blocks and pins the null-key finding id; one financing row with no `borrowing` key blocks both inclusions, missing `demo.finding.financing.no-borrowing`.
3. **Block, bad subject.** The subject's keys are null, or the subject map lacks `key`. Block `DEPENDENCY_INVALID` with missing `link-coverage-keys-unavailable`. No counted finding is named and none is pinned. Evidence 5 records both subject failures with that token and that exception text.

No new record code. `DEPENDENCY_INVALID` is already on `derivation-record.v9`. Track 0c section 4 says a distinct code for a missing key was not tried, and that need is unverified. This part does not add one.

### Pins

The operator pins each current counted finding that agreed on `key`. It pins a counted finding that blocked under item 2. A zero count adds no counted-row pin. A subject-key block adds no counted-row pin. Pins of the subject finding, of answers, or of other inputs belong to the rule that read them. Evidence 5's chain table shows those extra pins on the support publication; its direct table is the operator's own pins.

### What the count does not establish

A count of current rows is not scope. Track 0d evidence 6 recovers the real recorder. After a `cannot-tell`, a `no`, or a withdrawal, one current affirmative remains where two had been, and a chain that trusts the remaining count publishes `plain-case-supported`. The scope mark is a separate fact. This operator does not read it, write it, or treat a missing mark as `complete`.

The count also does not establish that the set of rows is complete, that a schooling named by a counted row is still current, or what two agreeing rows do to the interest. Two periods return 2. They do not become one loan, a portion, or a qualified amount. That last question is ADR 0076 Part 3, and it stays open. Track 0c section 3: schooling is outside this pin set, and the count does not notice a schooling row that is no longer current.

## Decision — Part 2. Declared basis on a rule

**A rule may declare `basis`, four groups of sentences, so a reader of its result can show the adopted favorable assumptions and the conditions left with the person beside the pins of what was said and what was derived.**

Track 0e section 3 names the four groups and says pins can carry the first two, because those inputs exist, and cannot carry the last two, because an assumption that was never asked and a responsibility that was never established are not findings the rule read. A favorable value with no stated basis would hide the assumptions inside the value. Section 3 left the stored field for later. This part is that field. It lives on the rule.

### Shape

An optional object on `rule-artifact.v13`:

```json
{
  "basis": {
    "said": ["<sentence>"],
    "derived": ["<sentence>"],
    "assumed": ["<sentence>"],
    "left_with_person": ["<sentence>"]
  }
}
```

Each key is required when `basis` is present. Each item is a non-empty string. An array may be empty only when that group is truly unused. The sentences are the rule's statement of its basis. They are not findings, and they are not a second copy of the pin list.

### Validation

`basis` may appear on a per-subject rule or a return-level rule. It does not replace `value` or `selection`. Package validation accepts the object when the four keys are present and the items are strings. It does not judge whether the sentences are true.

The rule that publishes `plain-case-supported` for one box 1 statement must declare `basis`, and `assumed` and `left_with_person` must be non-empty. Track 0e section 3 is the text that rule declares, grouped as follows.

**Said.** The loan-cost answer `yes` for the named borrowing. The enrollment answer `yes` for the named period, institution, and programme. The financing affirmation naming that borrowing and that schooling. The inclusion affirmation naming that statement and that borrowing.

**Derived.** The inclusion count is 1. The financing count is 1. Both are counts of current rows, not answers the person gave. Currency of the schooling and of the box 1 is not a sentence in this group. Track 0f item 1 shows a stale schooling or a stale statement blocks the chain, so a published favorable result has already survived those joins. The joins are pins of findings the rule required. They are not a fifth group.

**Assumed, in the person's favor, with no answer recorded.** The expenses fall in a reasonable period. The school costs stand in for qualified higher education expenses, and no reduction is applied for scholarships or other tax-free assistance. The schooling was for the taxpayer, a spouse, or a dependent when the loan was incurred. The named borrowing is indebtedness the taxpayer incurred. Box 1 holds no loan the person did not record, so the whole box 1 is this loan's interest.

**Left with the person.** The institution is an eligible educational institution. The enrollment meets that institution's half-time standard. The program leads to a recognized educational credential. The cost of attendance is the figure that institution determines. None of these is a finding, and none is consumed as an input.

`plain-case-supported` means those four groups hold for that statement, and the worksheet may then run its existing arithmetic on the whole box 1 once its other gates pass. It does not mean the loan is a qualified education loan. `not-supported` means the statement is outside that case. It does not mean a non-qualified loan is present. Track 0e section 3.

### How a reader reaches it

A published finding's pins include a pin of the producing rule: its role, id, and version (`runner.pins_for`). An explanation walk on `npe-walk.v3` names that same rule in the node's `rule_references`, taken from the rules that publish the symbol. The reader loads the adopted rule at that id and version and reads `basis`.

`said` and `derived` are shown beside the finding's input pins. The pins are the evidence that those inputs were read. `assumed` and `left_with_person` are shown in the same account. They have no pin and no finding. A rule with no `basis` gives the reader nothing to show for those groups. That is allowed for a rule that does not claim this favorable result. It is not allowed for the plain-case support rule.

Part 2 adds no walk schema and no finding schema. `npe-walk.v3` and `derived-finding.v2` already point at the rule. The sentences stay on the rule. (Part 3's derived entry pin needs `derived-finding.v3`. That pin is not a basis field.)

## Decision — Part 3. Same-run reading of per-subject results

**A path on a return-level rule declares the per-subject symbols it reads. The worksheet waits for the publishers of those symbols only when that path is the selected path. Both runners then see the same entries: one result for each current subject, and a block counts as that subject's result.** The reader refuses unless each current subject has exactly one result.

Track 0f item 2 is the defect the declared read removes. A return-level rule with no `requires` let the runners disagree about a collect of the conclusion symbol. The same rule with `requires` of that unsuffixed symbol made both runners block `DEPENDENCY_ABSENT`, including when the chain had published `plain-case-supported`. The keyed publication never fills the unsuffixed name.

`packages/derivation/subject_dispatch.py` builds the keyed symbol as `publishes` plus `|` plus the subject fact id. The per-subject block rows use that same symbol.

### Shape

`reads_subject_results` is a list. It is a field of a selection path, and of the default when the default reads any per-subject result. It is not a field of the rule. One object per symbol:

```json
{
  "reads_subject_results": [
    {
      "symbol": "<the per-subject rule's publishes>",
      "subject": {"id": "<subject fact type id>", "version": "vN"}
    }
  ]
}
```

`symbol` is the unsuffixed name the per-subject rule publishes. `subject` is the fact type that rule declares as its subject. The Track 1a-4 worksheet puts five objects on the old path, one for each answer-status symbol, and one object on the new path, for `demo.tax.track0d.statement-conclusion`. The subject on every object is `tax.us.2025.f1098e.box1-student-loan-interest`. The default's list is empty.

Changed from the previous Part 3: the field was one object on the rule, and it named one symbol. One object cannot name the five old-path symbols and the new-path symbol, and a rule-level list would be waited on for every presence outcome.

### Validation

- The rule has no `subject`. A rule with both `subject` and a path or default that carries `reads_subject_results` is rejected.
- Some rule in the package publishes `symbol` and declares `subject` as its subject fact type. The subject's id and version resolve on the package fact surface.
- The declaration does not make the unsuffixed symbol a `requires` entry of the rule or of the path. Putting that symbol in `requires` keeps today's behavior: both runners block `DEPENDENCY_ABSENT`.
- A symbol in `reads_subject_results` is not a declared path pin.

Changed from the previous Part 3: the exclusion from `requires` now covers the path as well as the rule, and the same symbols are excluded from declared path pins. Part 4's equality, below, states the same exclusion.

### Runtime

`runner._execute` and `reference_runner.run_reference` share eligibility and `attempt`. This read uses that shared path.

Presence is decided first, from current sources, by the Part 4 plan. Only then does the selected declaration contribute a wait:

- Conflict: do not wait for any path's publishers.
- Default, when its `reads_subject_results` is empty: do not wait for any per-subject publisher.
- One selected path: the rule becomes eligible when every ordinary `requires` name of that path is in `symbols`, and every rule that publishes a symbol in that path's `reads_subject_results` is in `resolved`. A predecessor that blocked is in `resolved`. If the package has no publisher for a declared symbol, do not wait. The other path's publishers are not a wait.

The rule is not eligible because the unsuffixed symbol is in `symbols`. The Track 1a-4 run is the measure. Old-only published 2500 while the same run's conclusion was `not-supported`. New-only published 2500 while the same run's five status rules were blocked. Both present blocked on the presence token and did not pin those derived findings.

After the wait, both runners expose the same entries for the current rows of the declared subject fact type:

- a publication whose symbol is `symbol|<subject fact id>`, or
- a block whose symbol is that same keyed symbol, when the per-subject rule blocked and published nothing for that subject.

A block is a result. It is not the absence of a result. Publication order may differ. Values, pins, and blocked rows may not.

Inside the selected path, a collect-family operator (`collect`, `count`, or `collect_categorical_all_equal`) whose `name` is one of that path's declared symbols reads exactly these entries, one per current subject, and nothing else. If any entry is a block, that operator refuses with `DEPENDENCY_INVALID` and lists the blocked subjects' fact ids in `missing`, sorted. It never skips the blocked entry, and never reads it as an empty or favorable value. A collect-family operator over `symbol` in a rule without this declaration keeps today's behavior.

An ordinary `requires` test, and a collect that does not go through this declaration, are unchanged. The item 2 split on an undeclared collect remains the behavior of that collect.

Changed from the previous Part 3: eligibility is per selected path, after presence, and conflict and the empty default do not wait. The previous text waited, for the whole rule, until every publisher of the one symbol had resolved.

### Coverage

The reader must be able to refuse unless each current subject has exactly one result. Exactly one means one publication or one block, not both and not neither.

- A subject with no publication and no block is missing. Block `DEPENDENCY_INVALID`. `missing` is those subject fact ids, sorted.
- A subject with two results is missing, same code, same list.
- A subject whose rule blocked and published nothing has one result, the block. The reader's own value then refuses a set that contains a block, or a value other than the one favorable value, with `DEPENDENCY_INVALID` and the missing token that value expression declares.

The old path's favorable value is `yes`. The new path's favorable value is `plain-case-supported`. The Track 1a-4 run measured the favorable side: five `yes` status publications on the old path, and one `plain-case-supported` conclusion on the new path, each producing line 21 `2500` on both runners. It did not measure a selected path whose entry was a block. Inactive-path blocks were present in the new-only run and were not the worksheet's result.

No new operator is required for the refusal itself. This part does not add `SLI_STATEMENT_COVERAGE` to the record enum. The disposition code is `DEPENDENCY_INVALID`. It does not change the worksheet's phase-out or limit arithmetic. The same 2500 cap the production worksheet publishes for one box of 3000 and total income 50000 is what old-only and new-only published.

Changed from the previous Part 3: `missing` names subject fact ids in every sentence. The previous coverage sentence said subject finding ids. The nonempty-neither result in this run named the box fact id `tax.us.2025.f1098e.box1-student-loan-interest|lender=demo-lender,statement=demo-stmt,tax-year=2025`.

### Pins

Each entry carries the pins the per-subject publication or block already recorded. The return-level finding pins each published entry it read: role `input`, id the derived finding id, version `v2`, origin `derived`. It does not copy the entry's inner pins onto itself. It does not invent a pin for a subject that has no result; that subject is named in `missing`.

Origin `derived` is allowed on these pins only. The published pin enums do not admit it. Track 1a-5 probe C ran the Track 1a-4 new-only case and validated what it produced. The line 21 finding fails `derived-finding.v2`: `pins/26/origin: 'derived' is not one of ['assertion', 'declared_default']`. Its published disposition fails the disposition definition of `derivation-record.v9` the same way. In-memory copies of those two schemas with `derived` added to the pin `origin` enum accept both. A finding that carries a derived entry pin is therefore `derived-finding.v3`. A derivation record whose dispositions carry one is `derivation-record.v10`. Each successor copies its predecessor and adds `derived` to the pin `origin` enum, and nothing else. A finding or record with no derived entry pin keeps `derived-finding.v2` or `derivation-record.v9`, unchanged. See "Schemas". Old-only's line 21 finding carried five such pins. New-only's carried one.

Changed from the previous Part 3: the previous pin sentence did not say the role, version, or origin of the pin that points at the derived finding. A derived result is not an `assertion` / `v1` input.

Changed by Track 1a-5: the Track 1a-4 text let the probe skip schema validation of a finding that carries this pin. A production finding and its record must validate, so the pin needs the two successor versions above. **Proposed.**

## Decision — Part 4. Presence selection beyond line 2b

**`exclusive_presence` / `refuse` is evaluated for every `rule-artifact.v13` rule that declares it and passes the validation below. The rule id is not an authorization list. Form 1040 line 2b version `v8` keeps the binding it has today.**

Track 0f item 3 cloned the worksheet onto `rule-artifact.v9`. Every presence case blocked `DEPENDENCY_INVALID`, missing `v9-declarative-binding-unauthorized`. The v9 clone stays unauthorized. This part is the v13 behavior. The Track 1a-4 run used rule id `demo.rule.track1a4.worksheet` and did not block on that v9 token.

For that declaration the four presence outcomes, plus the closed-empty outcome the default distinguishes, were:

- Old answers present, inclusion absent: old path, line 21 published 2500. Both runners agreed. Presentation disposition `published_value`.
- Inclusion present, the five answers absent: new path, line 21 published 2500. Both runners agreed. Presentation disposition `published_value`.
- Both present: no path value. Block `DEPENDENCY_INVALID`, missing `old-and-new-sli-inputs-both-present`. Presentation disposition `blocked`, `activeCodes` `["DEPENDENCY_INVALID"]`.
- No box, no answers, no inclusion: default, line 21 published 0. Presentation disposition `computed_zero`.
- A box present, no answers, no inclusion: default, no dollar. Block `DEPENDENCY_INVALID`, missing that box's fact id. Presentation disposition `blocked`, `activeCodes` `["DEPENDENCY_INVALID"]`.

### Shape

`selection` on `rule-artifact.v13` is the v9 selection object, copied forward, with the path fields this part adds. It is an alternative to top-level `value`: a rule has one of them, not both. v13 does not carry v9's `aggregation` object.

- `mode` is `exclusive_presence`. `conflict` is `refuse`. No other mode or conflict is valid.
- `paths` has at least two paths. Each path has an `id`, an `activity`, `reads_subject_results`, `requires`, `pins`, `when`, and `value`. The id matches the v9 pattern. The default object's `id` is `neither`. The default has the same fields.
- Activity is `source_nonempty` or `derived_activity`. `source_nonempty` names a member fact type, or `member_fact_types` when the path is active if any one of several members has a current source. `source_family` is present when the member belongs to an adopted family, and omitted when it does not. The runtime predicate is current sources of the named member, which is the predicate `source_nonempty` already uses. `derived_activity` names a fact type. The Track 1a-4 old path uses `member_fact_types` for the five answer facts and the statement family. The new path uses `member_fact_types` for every statement-keyed relationship fact, and no source family: the affirmed inclusion `tax.us.2025.sli.statement-inclusion-relationship`, and the three production facts Track 3 adds for one statement and one borrowing. Those are `tax.us.2025.sli.statement-inclusion-unresolved` (the person cannot tell whether the statement includes that loan), `tax.us.2025.sli.statement-inclusion-denied` (an explicit no), and `tax.us.2025.sli.statement-inclusion-withdrawn` (an inclusion withdrawn with no successor answer). It also names the Part 5 replay marker, `tax.us.2025.sli.statement-inclusion-applicability-unestablished`, which is a system fact and not one of the person's. The new path is active when any of them has a current source.
- `refusal.code` is `DEPENDENCY_INVALID`. `refusal.missing` is a non-empty list of unique strings.

Changed from the previous Part 4: activity was one `member_fact_type` plus a required source family. One member cannot name the five answers. The inclusion in this run has no adopted family. The path and the default gain `reads_subject_results`.

Changed by Track 1a-5: the Track 1a-4 new path named only the affirmed inclusion. A return with an old answer and an unresolved inclusion then selected the old path and deducted. Track 1a-5 probe B6 ran that return on the Track 1a-4 declaration: line 21 published 2500 on both runners. With the activity above, B7 blocked `DEPENDENCY_INVALID`, missing `old-and-new-sli-inputs-both-present`. Under the repaired activity, old-only, new-only, closed-empty and nonempty-neither kept their Track 1a-4 results (B8 to B11: 2500, 2500, 0, and a block on the box fact id). These results are executed with the runtime stand-in operator. **Proposed.**

The three Track 3 ids are the names Track 3 adds. They replace the sample-bundle type `demo.tax.2025.sli.statement-inclusion-unresolved`; Track 0d records that production needs that fact admitted without the sample bundle. If Track 3 adopts other ids, this list follows them. Package validation of a worksheet that names them needs them on the package fact surface, so Track 3 lands before that worksheet is adopted. Financing-keyed recorder facts are not in the list. A financing cannot-tell, an explicit no on a financing, and a withdrawn financing name a borrowing and a schooling, not a statement. Owner decision 2 makes a link on a statement the new regime's presence. See "Open questions".

### Validation

For a v13 rule that declares `selection`:

- The rule has no `subject`. Top-level `when` is true. Top-level `requires` and `pins` are empty.
- Path ids are unique. The default id is `neither` and is not also a path id.
- Each activity's fact type resolves on the package fact surface. This checks resolution. It does not check that the ids are the nominee family or the nominee fact type.
- The names that are `requires` of a path are the `ref` names in that path's `when` and `value`, and any collect-family `name` that is not a symbol in that path's `reads_subject_results` and not the member name of a closed-family `count`. Names that appear only as members of a `conditional_dependency_set` are not `requires`. The default obeys the same rule. The Track 1a-4 default references the box-1 count and has empty `requires`.
- The path's declared pins are one pin per `requires` entry, same ids, same order. Role `choice` keeps version `v1` and has no origin. Every other declared pin is role `input`, version `v1`, origin `assertion`. Parameter ids are not `requires` and are not declared path pins. Symbols in `reads_subject_results` are not declared path pins.
- A path's `when` and `value` may use the ordinary expression operators, including `collect`, `count`, `block`, and `collect_categorical_all_equal`. Line 2b version `v8` keeps its own ban on dynamic dependency nodes inside a path. That ban is not copied here.

There is no list of authorized rule ids.

Changed from the previous Part 4: the previous equality said every name the path references is a `requires` entry, and every path pin is an `assertion` / `v1` input equal to that set. That equality cannot describe a derived per-subject collect, a choice, a parameter, a conditional member, or the closed-family count. The Track 1a-4 paths each declared 21 `requires`. The five status symbols and the conclusion symbol were not among them. `filing_status` was the choice pin. Closed-empty still published 0 with empty path `requires` on the default.

### Runtime

Both schedulers evaluate the declaration inside `attempt`, so they share one plan. The plan kinds are the ones line 2b already returns: `conflict`, `path`, or `default`. Activity is decided from current sources before any path's `requires` are consulted. An inactive path's publishers do not block the selected path. An inclusion that the Part 5 replay rule omits from the sources rules join counts toward the new path's activity through its replay marker, not as the person's unresolved inclusion. A conflict pins the marker's finding, which is the omitted inclusion's own finding, as activity evidence.

Changed by Track 1a-6: Track 1a-5 counted an omitted inclusion as the person's unresolved inclusion. That borrowed the person's fact for a reason the person did not give, and it did not reach the statement's own decision. The marker replaces it. See Part 5, "Replay".

- **One active path.** Wait as Part 3 says. Evaluate that path's `when`, then its `value`. A false `when` is inapplicable. A block raised by the value is that block. Do not evaluate the other path or the default.
- **No active path.** Evaluate the default the same way. Do not wait for a path's publishers.
- **More than one active path.** Evaluate no path value and do not wait for either path's publishers. Block `DEPENDENCY_INVALID` with the rule's `refusal.missing`. Pin the current source findings that made each active path true.

The Track 1a-4 conflict disposition pinned six findings, role `input`, version `v1`, origin `assertion`: the five answer findings and the inclusion finding, plus adoption and governance. It did not pin a path value.

The default value in that declaration is a `count` of box 1 compared with 0. The `then` branch is 0. The `else` branch blocks `DEPENDENCY_INVALID` and `missing` is the current subject fact ids, sorted. Closed-empty took `then`. Nonempty-neither took `else`.

Changed from the previous Part 4: the previous runtime waited on the selected path's `requires` and treated every named symbol the same way. It had no separate wait for per-subject publishers, and it had no way to avoid waiting on the inactive path. The closed-empty branch was not on the default.

### Pins

The selected path's publication pins what that path's expression read, plus the rule and adoption pins an ordinary publication carries. A derived entry read through `reads_subject_results` is pinned as Part 3 says: role `input`, version `v2`, origin `derived`, id the derived finding id. A ref to an ordinary derived symbol keeps the pin that symbol already has. In this run the line-1 subtotal pin was role `input`, version `v2`, origin `assertion`. Parameter reads are parameter pins. A choice input keeps role `choice`.

A conflict pins the activity evidence and does not pin a path value that was not evaluated. A contract failure before the plan runs blocks `DEPENDENCY_INVALID`. The missing token is the existing one for that failure: `declarative-top-level-contract-invalid`, `selection-path-id-duplicate`, or `selection-path-pin-contract-invalid`. This part does not add a record code for them.

Changed from the previous Part 4: publication pins are not the declared path-pin set. The declared set identifies dependencies by symbol. The publication identifies the findings that were read, and a derived per-subject entry uses origin `derived`.

### Line 2b stays as it is

`tax.us.2025.rule.form1040-line2b` version `v8`, schema `rule-artifact.v9`, keeps its id gate, its path ids `legacy` and `new`, its activity checks, its dynamic-dependency ban, and its refusal token `legacy-and-derived-nominee-both-present`. Its bytes are not edited. `rule-artifact.v9` and `artifact-package.v30` are not edited. A v9 rule that is not that citizen and that carries `selection` still fails package validation with `RULE_SELECTION_UNAUTHORIZED` and, if it is run, still blocks with missing `v9-declarative-binding-unauthorized`. v9 `aggregation` stays authorized only for `tax.us.2025.rule.interest.derived-nominee-subtotal` version `v1`.

The Track 1a-4 worksheet is a disposable v13 declaration, rule id `demo.rule.track1a4.worksheet`. It is not a rewrite of the v9 clone and not a loosening of the v8 checks.

This part does not change the person-visible line 21 sentence. Blocked cases in this run showed that generic sentence and `DEPENDENCY_INVALID`. They did not show the missing token. Published 2500 showed disposition `published_value`. Closed-empty showed `computed_zero`.

## Decision — Part 5. Scoped supersession on a new write

**A new write that would make a new finding of a declared source fact type current is refused before it reaches the log. The write is refused while a current finding of a declared dependent fact type names that source by identity, whether or not that fact id already has a current finding, unless that finding is the one successor a declared reviewed-scope evidence binds for that source. Replay of acts already in a log never runs this check.**

The binding is three things. The reviewed source state is the exact box 1 finding the review saw (`reviewed_statement_finding_id`). The intended correction is the corrected amount (`corrected_box1_total`) and a correction identity (`source_correction_id`). The resulting finding is that amount, cites corrected-statement evidence whose `source_correction_id` is that identity, and its predecessor is the finding the review saw. One scope evidence authorizes one finding. A second update that cites it is refused, including one that repeats the amount. Citing the evidence id is not the exception. Statement identity, an allowed scope label, and `refreshes_inclusion_applicability` are not enough. A missing binding field fails closed. Scope evidence recorded before `reviewed_statement_finding_id` was stored does not satisfy this exception and does not refresh the read-side tie.

The kernel does not name Form 1098-E or the statement inclusion. The registry carries the declaration. The check is generic and reads a registry map, in the same declaration style as `subset_invariant_pairs` and `companion_presence_pairs`. It does not run where `_enforce_subset_invariants`, `_enforce_companion_presence` and `_enforce_declaration_signal_contradictions` run. Those run in `apply_assertion` and on the member-transition path, and `project` runs both on replay.

The existing maps cannot carry this check. Subset and companion presence compare two fact types that share one key suffix. The statement inclusion's identity keys are the statement's keys plus `borrowing`, so the suffixes differ. Declaration/signal contradictions compare two current values. None of those maps can see "a current dependent names this source" together with "the new finding cites this evidence." Part 5 adds a map for that pair of facts. It does not widen the three maps above.

### Shape

One entry on the registry:

```json
{
  "source_fact_type": "tax.us.2025.f1098e.box1-student-loan-interest",
  "dependent_fact_type": "tax.us.2025.sli.statement-inclusion-relationship",
  "dependent_keys_not_identifying_source": ["borrowing"],
  "reviewed_scope": {
    "evidence_kind": "tax.student-loan.relationship-answer",
    "correction_path": ["recognition_context", "statement_correction"],
    "source_field": "statement_fact_id",
    "scope_field": "scope",
    "scopes": ["amount-only", "inclusion-added", "inclusion-removed", "inclusion-uncertain"],
    "refresh_field": "refreshes_inclusion_applicability",
    "binds": ["reviewed_statement_finding_id", "corrected_box1_total", "source_correction_id"],
    "successor_evidence_kind": "tax.form-1098e-corrected-statement-source"
  }
}
```

Five keys carry the names the check reads, so the kernel does not hold them. `correction_path` is the path inside the evidence `content` to the correction object. `source_field` names the field there that holds the source fact id. `scope_field` names the field that holds the scope. `refresh_field` names the flag that must be `true`. `successor_evidence_kind` is the kind of the corrected-statement evidence the new finding must cite exactly once. `binds` is read in role order: the source finding the review saw, the corrected value, and the correction identity; the successor evidence carries the correction identity under the third name. Every one of these is a Form 1098-E or student-loan name. Declaring them in the tax loader keeps `packages/kernel/findings.py` generic: it reads keys from the registry entry and names no tax field, fact type or evidence kind. The kernel refuses a malformed entry instead of guessing a default.

`source_fact_type` is the fact type whose new current finding is gated. `dependent_fact_type` is the fact type that names that source. `dependent_keys_not_identifying_source` lists identity-key names that belong to the dependent and not to the source. The tax registry installs one entry, for Form 1098-E box 1 and the statement inclusion. The recorder builds an inclusion as the statement's key bindings followed by `borrowing`. Dropping `borrowing` leaves the statement's bindings.

A dependent names the source when `fact_id_for(source_fact_type, remaining bindings)` equals the source fact id. The remaining bindings are the dependent fact's lattice key bindings, in their relative order, after the declared names are removed. The check uses `fact_id_for`. It does not split a fact-id suffix on commas. Key order is the order `fact_id_for` already renders, which is the order of the bindings, not a sort.

Reviewed-scope evidence is an `evidence.v1` object already in the log. Its `kind` is `tax.student-loan.relationship-answer`. Its `content.recognition_context.statement_correction` is an object whose `statement_fact_id` equals the source fact id of the finding being written, whose `scope` is one of the four scopes, and whose `refreshes_inclusion_applicability` is true. That object also carries the binding: `reviewed_statement_finding_id`, `corrected_box1_total`, and `source_correction_id`. `corrected_box1_total` matches the new finding's value as a number. A boolean does not match. The new finding cites that scope evidence and exactly one `tax.form-1098e-corrected-statement-source` evidence whose `content.source_correction_id` equals `source_correction_id`. The predecessor is the one current finding of that source fact id in the projection of the acts already in the log, and it equals `reviewed_statement_finding_id`. No other finding of the source fact type cites that scope evidence. A finding of another fact type that cites it, such as the unresolved status the inclusion-uncertain route records from the same answer evidence, does not use it up. Kind alone is not enough: an ordinary yes or no answer uses the same kind and does not carry that correction object. Citing only `tax.form-1098e-corrected-statement-source` is not enough either. Citing the scope evidence id, without this binding, is not enough. The reviewed route records the scope evidence first, copying `reviewed_statement_finding_id` from the review card the person saw. The corrected box 1 finding then cites that evidence together with the corrected-statement source evidence. These fields sit on `evidence.v1` content, which is an open object. They are not new citizens and they are not a published schema change.

### Where the tax registry installs it

The entry lives in `packages/tax/loader.py`, beside the other domain maps. The implementation track folds the install into `install_domain_companion_presence`. That function's own record names its two call sites, `tax_registry()` and `packages.derivation.live.live_coordinate_run`. Folding the install there reaches both sites without a third call site and without editing `packages/derivation/live.py`.

The new-write step reads the map from the registry its `ActLog` was built with. That function's record says those two sites reach "every registry a workspace fold or a production run uses". It does not say they reach every registry an `ActLog` is built with, and they do not. The relationship tests build their `ActLog` over `DerivationSchemas().registry`, which carries no domain maps. Track 1a-5 probe A3 ran a direct same-identity box 1 append over such a registry, with a current inclusion and the step installed. The append was admitted at 1800. **Proposed:** the implementation track makes every `ActLog` that can hold a statement inclusion carry the map, and tests that the recorder's `ActLog` does. A writer whose `ActLog` lacks the map is a bypassing writer, below. This paper writes neither the loader nor the kernel.

### When the check runs

The check runs on a new write of an act that would make a new finding of `source_fact_type` current. That act is an `assertion`, or a `member-transition` whose member action is `assert` or `reclassify`. The check reads the projection of the acts already in the log, which is the state before this act. It fires when a current finding of the declared dependent type in that state names the source fact id. It fires whether or not the fact id already has a current finding. The absence of a current finding is not an exception. A retraction does not make a new finding current, so the retraction act is outside this check. An act that does not make a finding of `source_fact_type` current is outside this check.

The dependent is read in the log before this act, so a retraction or answer of the inclusion already appended is visible. The reviewed amount-only route records scope evidence, and the new box 1 finding is the one successor that evidence binds, so the step admits that write while the inclusion stays current. The reviewed removal route answers the inclusion before it appends the source. At that append the answered inclusion is not current, and this check does not fire for that pair. A second inclusion on the same statement that is still current still requires the new finding to be that one bound successor. The same evidence does not authorize a second finding. Withdrawing the inclusion first leaves no current dependent, so a later source finding is admitted.

Evidence named by the new finding counts only when that evidence is already in the log. A citation of an id the log does not hold does not satisfy the declaration. A citation that fails the binding is the same refusal as a missing citation.

On a violation the step raises `FindingModelError` and writes nothing. One dependent uses the text below. When more than one current dependent names the source, the `while <dependent fact id> is current and names that source` clause repeats once per dependent, in fact-id order, each clause separated by `; `:

`scoped supersession violated: new finding <new finding id> of <source fact id> while <dependent fact id> is current and names that source; the new finding is not the one successor bound by reviewed-scope evidence for that source; rejected, not recorded`

### Where a new write is refused

**Proposed.** The new-write admission boundary is `ActLog.append` in `packages/kernel/act_log.py`, at one new step. After the act's envelope and payload validate and the expected revision matches, and before the line is written, `append` projects the acts it has just read and calls `enforce_new_write_invariants(state, act, registry)`, a new generic function in `packages/kernel/findings.py`. That function runs the Part 5 check against the projected state. If it raises, `append` re-raises and writes nothing. The act is not in the log.

It is this boundary for three reasons.

- **Every durable writer reaches it.** `ActLog.append` is the only function in `packages/` that writes an act line. Each writer calls it directly.
- **Replay never runs it.** `project` folds acts through `apply_act`. `ActLog.read` validates schemas only. Neither calls `append`. Probe A1 counted zero calls to the step while `project` replayed the recovered log; A4 and A5 counted zero again on histories that already hold a prohibited write.
- **A refusal leaves no act.** The step runs before the write. Probe A1: with a current inclusion, a direct same-identity box 1 append at 1800 and a smuggled 2900 that cites the reviewed 1775 scope evidence were both refused. Neither assertion is in the log. After an ADR 0073 retraction of box 1, a direct 1500 was refused the same way. The retraction itself was admitted.

The step returns at once, without projecting, unless the registry declares an entry and the act is one of the kinds above. A workspace with no relationship claims is admitted as today. Probe A2 ran the same no-claim direct append with and without the step installed: both logs are identical, and box 1 is 1410 in both.

The writers in `packages/`, and how each reaches the step:

| Writer | Reaches the step through |
| --- | --- |
| `_append_statement_source_correction_durably` (`packages/tax/sli_relationship_review.py`) | Its own `log.append` of evidence, contribution and assertion. It refuses an unbound write itself before its first append (**implemented**). The step is the second line. |
| `introduce_borrowing_reference_durably`, `record_submission_durably`, `withdraw_relationship_claim_durably`, `answer_relationship_claim_durably`, `_answer_unresolved_inclusion_no_durably`, `_record_unresolved_inclusion_durably`, `correct_relationship_claim_durably` (`packages/tax/sli_relationship_recording.py`) | Their `log.append` calls. None writes a box 1 finding, so the step returns at once. |
| `assert_nominee_allocation`, `retract_nominee_allocation` (`packages/tax/nominee_allocation_recording.py`) | Their `log.append` calls. Not a declared source. |
| `SyntheticW2EntryRuntime._seed` and `.contribute` (`packages/derivation/entry_loop.py`) | `self._log.append`. Not a declared source. |
| `append_publications` (`packages/derivation/runner.py`) | `act_log.append` of `derived-publication` acts. Not a source assertion. |

Probe A1 recorded the callers that reached the patched step: `introduce_borrowing_reference_durably`, `record_submission_durably`, `_append_statement_source_correction_durably`, and the test helpers `_workspace`, `_append_source` and `_append_act`.

A writer bypasses the step in two ways. It writes lines to `acts.jsonl` without `ActLog.append`, or it builds its `ActLog` over a registry without the map. Either way the prohibited assertion is in the log. Probe A5 wrote a raw line at 1900 under the step; A3 appended 1800 over a bare registry. The step cannot refuse what it does not see. The replay rule below is the defense for both, and for logs written before the step existed.

A writer that appends several acts is refused only at the prohibited act. Acts it appended before that stay. In probe A1 the direct 1800 and the smuggled 2900 each left their evidence and contribution acts in the log, with no assertion. A writer can avoid that by calling `enforce_new_write_invariants` on its staged state before its first append, as the reviewed recorder already does with its own check. Interrupted multi-act writes are plan sentence 6, not this part.

`apply_assertion` is not the boundary. It runs on replay. Binding Part 5 there would either raise on a log that already holds the write, which makes the workspace unreadable, or need a replay switch inside the fold. Part 5 adds nothing to `apply_assertion` or to the member-transition path.

### Replay of a history that already holds the rewrite

**Proposed.** A log can hold an unbound rewrite because it was written before the step existed, or because a bypassing writer put it there. Replay treats both the same way.

1. **Replay the acts unchanged.** `project` does not run the step, so it does not raise, and the history stays readable. Probe A4 wrote a reviewed 1775 and then a smuggled 2900 without the step, installed the step, and recovered the log fresh. `project` did not raise. 24 acts replayed. Box 1 is 2900. The read-side reports the inclusion `unresolved-applicability`. A version gate alone is not enough: the old acts would still replay with the inclusion and the unbound box 1 both current, and the chain would still deduct.
2. **Do not join the inclusion.** `marshal_run_context` in `packages/derivation/marshal.py` builds every input and source from `compute_currency(state).current_finding_ids`, for both runners. The rule omits from those sources every current `tax.us.2025.sli.statement-inclusion-relationship` finding that `current_claim_applicability` does not report `current`. The box 1 finding stays, so the amount stays readable. A4's sources today hold the inclusion; under the rule they hold no inclusion.
3. **Put a marker in its place.** For each omitted inclusion the marshaller supplies one source of the system fact type `tax.us.2025.sli.statement-inclusion-applicability-unestablished`. The source has the omitted inclusion's identity keys (its statement's keys plus `borrowing`), the value `sli.statement-inclusion.applicability-unestablished`, and the omitted inclusion's own finding id. No act is written. The marker exists only in the run's sources and is rebuilt from the recovered log on every run. Its reason is that the system could not establish the inclusion's applicability after an unreviewed same-identity change of its statement. It is not the person's "cannot tell". It is not `tax.us.2025.sli.statement-inclusion-unresolved`, it does not carry that fact's value or wording, and nothing the person said produced it.
4. **The statement's support decision reads the marker.** The per-statement rule that publishes `plain-case-supported` or `not-supported` requires the marker type. The marker joins to the statement by agreeing statement keys, and a statement with no marker takes a declared default, `established`. When a marker is present, the rule publishes `not-supported` before link counts or coverage are considered. It also reads every marker on that statement with `collect_categorical_all_equal`, so it pins each omitted inclusion's finding (role `input`, version `v1`, origin `assertion`) beside the current box 1 subject, which is the unreviewed change. A per-statement echo publishes the marker value beside the conclusion. The pair `not-supported` / `sli.statement-inclusion.applicability-unestablished` is distinct from the person's `not-supported` / `unresolved-scope`. The box 1 finding the inclusion was confirmed against is named by that inclusion's evidence (`confirmed_statement_finding_id`). It is reachable from the pin but is not itself a pin.
5. **Presence follows the marker.** Part 4's new path names the marker type. An omitted inclusion therefore keeps the new regime present. A return that also holds old answers blocks as both present instead of turning into old only.

Track 1a-5 probe B ran the Track 1a-4 worksheet on rows whose box 1 is A4's 2900 and whose inclusion follows A4's subject sets. These results are executed with the runtime stand-in operator, on both runners, which agreed in every case. B3 and B5 used the person's unresolved type as the presence stand-in; step 5 replaces that.

| Case | Line 21 |
| --- | --- |
| B1. Today: the inclusion is joined, Track 1a-4 activity | published 2500 |
| B2. Inclusion omitted, Track 1a-4 activity | blocked `DEPENDENCY_INVALID`, missing the box fact id (the default) |
| B3. Inclusion omitted and counted as unresolved, repaired activity | blocked `SLI_UNIVERSAL_COMPONENT_VIOLATION` (the new path; the conclusion is `not-supported`) |
| B4. Old answers too, inclusion omitted, Track 1a-4 activity | **published 2500** (old path) |
| B5. Old answers too, inclusion omitted and counted as unresolved, repaired activity | blocked `DEPENDENCY_INVALID`, missing `old-and-new-sli-inputs-both-present` |

The owner then found that omission plus presence does not reach the statement. A statement that keeps one valid inclusion beside an omitted one still published `plain-case-supported`, because its link count was 1. Track 1a-6 reproduced it and ran steps 3 to 5 (`PYTHONPATH=. python3 temp/track1a6/probe.py`). Every start state is **recorder execution**: the real recorder, a real `ActLog`, fresh recovery, and the real `current_claim_applicability`. Every chain and worksheet result is a **runtime stand-in**: the Track 0d chain with the `shared_key_count` stand-in, the Track 1a-4 scheduler, and the marker patched in. Both runners agreed in every row. The line 21 presentation showed the generic sentence in every row.

| Case | Start state (recorder execution) | Treatment | Statement result | Line 21 |
| --- | --- | --- | --- | --- |
| Owner's mixed case | A `unresolved-applicability`, B `current`, box 1 1800 | Track 1a-5 (omit A, A counted as unresolved) | `plain-case-supported` | **published 1800** |
| Owner's mixed case | same | Track 1a-6 | `not-supported`, mark `applicability-unestablished`, pins A and the 1800 box 1 | blocked `SLI_UNIVERSAL_COMPONENT_VIOLATION` |
| Sole omitted link | A `unresolved-applicability`, box 1 1800 | Track 1a-5 | `not-supported`, pins the box 1 only (no usable link) | blocked |
| Sole omitted link | same | Track 1a-6 | `not-supported`, mark `applicability-unestablished`, pins A | blocked |
| Two omitted on one statement | A and B both `unresolved-applicability` | Track 1a-6 | `not-supported`, pins A and B | blocked |
| Mixed beside an unaffected statement | A unresolved, B current; sibling statement `current` | Track 1a-5 | both `plain-case-supported` | **published 2500** |
| Mixed beside an unaffected statement | same | Track 1a-6 | sibling `plain-case-supported`, mark `established`; first `not-supported` | blocked |
| Reviewed route, sole | after a reviewed amount-only correction to 1850, A `current` | Track 1a-6 | `plain-case-supported`, mark `established` | published 1850 |
| Reviewed route, mixed | after the same correction, A and B `current` | Track 1a-6 | `not-supported`: two current inclusions on one statement | blocked |
| Old answers + sole omitted | A unresolved, five old answers on the statement | Track 1a-6 | `not-supported` | blocked `DEPENDENCY_INVALID`, `old-and-new-sli-inputs-both-present` |
| Plain case, no change | A `current`, box 1 1250 | Track 1a-6 | `plain-case-supported`, mark `established` | published 1250 (also 1250 without the marker) |
| Track 1a-4 synthetic cases | not recorder-built | Track 1a-6 | — | old-only 2500, new-only 2500, both blocked on the presence token, closed-empty 0, nonempty-neither blocked on the box fact id |

The reviewed route re-binds A in both reviewed cases. The deduction returns where A is the statement's only loan. Where B is also current, the statement holds two loans, and owner decision 3 keeps it `not-supported` for that reason. The applicability mark is `established` again. A successful statement now carries one more pin, the declared default `established` for the marker. Its value is unchanged.

A workspace with no current dependent has nothing to omit and no marker. Its box 1 finding is replayed exactly as today. The rule does not change a workspace with no relationship claims.

A log in this state is repaired through the reviewed route. In A4, after the step was installed, a reviewed amount-only correction to 2950 was the bound successor of the current 2900 and was admitted. The inclusion became `current` again and returned to the sources rules join.

This part does not install the omission, the marker, or the presence rule, and does not edit `packages/derivation`.

### What this part leaves as it is

A source with no current finding of the declared dependent type is admitted exactly as today. A workspace with no relationship claims is that case. The ordinary first box 1 is that case as well: it is asserted before any inclusion exists, so no current dependent names it. Withdrawing the dependent is admitted, and a later same-identity append of the source is admitted once no current dependent remains. A correction of another fact type, including a schooling description or a financing row, is admitted while an inclusion is current, because that act does not make a finding of the declared source type current. `evidence.v1` content stays an open object. The correction fields are not new citizens. This part adds no published schema.

Retracting the box 1 finding is not this check. The act is `act-finding-retracted.v1`. ADR 0073 Decision 1 ends that one finding's current support, supplies no replacement, and asserts no opposite claim. Decision 3 gates the act by the ADR-0041 supersession policy alone. This part does not refuse that act, and it does not edit ADR 0073. While the box 1 finding is not current, the inclusion fails the stale-target join in Track 0f item 1: a stale statement blocks the inclusion on the missing box, and the worksheet blocks rather than deducting. A later assertion of a new finding for that same fact id is a new current finding. If a current dependent still names that source, this check refuses the assertion unless the new finding is the bound successor. The gap between the retraction and that assertion is not a first-assertion exemption. ADR 0073 Decision 8's sixth admission-invariant refusal fences declared-relation participants on committed 2025 content. That refusal is a different check. This part does not extend it and does not add those participants to this map.

### Relation to Track 6

Track 6's read-side tie is the predicate the replay rule consults. `current_claim_applicability` treats an inclusion as applicable only when the box 1 finding it was confirmed against is still current, or when the current box 1 finding is the one successor the scope evidence binds. Citing the evidence id does not refresh the tie. Scope evidence that lacks `reviewed_statement_finding_id` does not refresh it.

The deduction chain never calls `current_claim_applicability`. It joins an inclusion to its statement by identity, through the sources `marshal_run_context` supplies. The tie does not stop a new write; the step does. The tie does not stop the chain; the replay rule does, by consulting it.

In `tests/test_sli_correction_entry_enforcement.py`, three expectations change when the step lands, because the write is refused instead of recorded:

- `test_case_3_direct_same_identity_append_does_not_keep_inclusion_applicable`. Today the append is recorded at 1800 and applicability is `unresolved-applicability`. Under this part the assertion is refused and not recorded. The original box 1 stays current. The inclusion stays current against it.
- `test_case_5_unrelated_statement_inclusion_stays_applicable`. Today the touched inclusion is unresolved and the other inclusion stays current. Under this part the touched assertion is refused. Both inclusions stay current. The other statement's box 1 is untouched.
- `test_case_7_reviewed_correction_restores_applicability_after_direct_append`. Today a direct append leaves applicability unresolved, and a later reviewed correction restores it, with history 1250, 1800, and 1900. Under this part the direct assertion is refused. The reviewed correction is the write that admits the new amount. The inclusion stays current through that write. The refused 1800 is not in history.

Four Track 6 expectations stay:

- `test_case_1_reviewed_amount_only_keeps_inclusion_and_both_amounts`. The reviewed finding is the one successor the scope evidence binds, so the step admits it. The inclusion stays current. Both amounts stay in history. **Implemented** at the recorder and the read-side. **Proposed** at the step.
- `test_case_2_reviewed_removal_drops_applicability_and_keeps_affirmation`. The inclusion is answered before the source append, so that pair has no current dependent at append time. The inclusion is not current. The affirmation stays in history. **Implemented** on the reviewed route. **Proposed** at the step, which does not fire for that pair.
- `test_case_4_direct_append_without_claims_is_admitted`. There is no relationship claim. The append is admitted exactly as today.
- `tests/test_f1098e_student_loan_interest_agi_track6.py`. An old-path workspace has no statement-inclusion claim. That file stays as it is.

Three older tests perform the same direct append: `OrdinaryRelationshipRecording.test_statement_inclusion_correction_and_withdrawal_are_independent` in `tests/test_sli_relationship_recording.py`; `VersionedSourceConsumer.test_actlog_recovery_both_runners_and_independent_claim_lifecycles` in `tests/test_sli_track15_versioned_source_consumer.py`; `Track17RelationshipApplicability.test_same_key_statement_record_has_no_composition_answer` in `tests/test_sli_track17_relationship_applicability.py`. **Implemented** in Track 1a-5: each now expects `unresolved-applicability` after that append, which is what the read-side tie returns. When the step lands, their direct assertion is refused, and the implementation track changes them again.

### Evidence, and what has not run

Track 6 case 3, on the base before the read-side tie, failed in `test_case_3_direct_same_identity_append_does_not_keep_inclusion_applicable` with `AssertionError: 'current' != 'unresolved-applicability'`. That failure is the evidence the gap exists. After Track 6 the same append is recorded and applicability is `unresolved-applicability`. The deduction chain still does not call `current_claim_applicability`, so the runners can still join an inclusion to the new box 1 by identity. Probe B1 shows that join deducting 2500 on a smuggled 2900. The owner chose admission refusal for that reason.

The owner then reproduced a reviewed correction to 1775 followed by an unreviewed update to 2900 that cited the same scope evidence. Before the Track 1a-3 fix that test failed `AssertionError: 'current' != 'unresolved-applicability'`. **Implemented** after the Track 1a-3 fix: the recorder refuses that second write, and the read-side does not refresh a smuggled citation that fails the binding.

**Proposed, run as a disposable probe:** Track 1a-5 patched a stand-in of the step into `ActLog.append` at runtime and drove the real recorder, the real `ActLog`, and the real `project` (`PYTHONPATH=. python3 temp/track1a5/probe.py`). The step is not in `packages/kernel`. A green suite on the current tree is not evidence that the step fires.

The implementation track executes these cases:

1. Reviewed amount-only while an inclusion is current: admitted. The inclusion still applies. Both amounts are kept. Probe A1 ran it at 1775 through the step.
2. Reviewed inclusion-removed: the inclusion is answered first, the source is admitted, the inclusion no longer applies, and the affirmation is kept.
3. A direct same-identity box 1 append, with a current inclusion and no reviewed-scope evidence: refused, not recorded. The original finding stays current. The inclusion still applies to it. Probe A1 refused it at 1800.
4. The same append with no relationship claims: admitted, the same as today. Probe A2.
5. Case 3 beside an unrelated statement that has its own inclusion: the touched append is refused. The unrelated inclusion still applies. Its statement is unchanged.
6. `tests/test_f1098e_student_loan_interest_agi_track6.py` stays unchanged.
7. After a refused case 3, a reviewed correction: admitted. The inclusion applies through the reviewed route. The refused amount is not in history.
8. The first box 1 of a fact id, asserted before any inclusion exists: admitted, because no current dependent names that source. The lack of a prior finding is not the reason it is admitted.
9. Retraction of the box 1 finding under ADR 0073: admitted as a retraction. Probe A1.
10. A correction of an unrelated fact type, schooling description or financing, while an inclusion is current: admitted.
11. Withdrawal of the inclusion, then a same-identity box 1 append: admitted, because no current dependent remains.
12. Reviewed-scope evidence cited for a different statement fact id: refused.
13. Retract the current box 1 finding, then assert a new same-identity box 1 finding while the inclusion is still current. The assertion is refused and not recorded. Probe A1 refused 1500. After a retraction there is no current box 1 finding, so no predecessor can equal `reviewed_statement_finding_id`, and no write can be a bound successor; a finding that cites scope evidence for the retracted finding is refused too. The way back is to withdraw or re-answer the inclusion, enter box 1, then confirm the inclusion again. With no current dependent, the box 1 entry is admitted, and the new confirmation is tied to it.
14. A reviewed correction to 1775, then an unreviewed update to 2900 that cites the same scope evidence. **Implemented:** the recorder refuses before any append. A smuggle that skips the recorder is refused by the step and leaves no assertion (probe A1).
15. A second update that repeats 1775 and cites the same scope evidence. **Implemented:** the recorder refuses.
16. A review prepared against one box 1 finding, after that finding has changed to 1640. **Implemented:** `apply_statement_correction_review` refuses. The step refuses the same write because the predecessor is not the finding the review saw.
17. One citation whose `reviewed_statement_finding_id` is not the predecessor. **Implemented:** the read-side reports `unresolved-applicability`.
18. The same binding stored on evidence whose kind is not `tax.student-loan.relationship-answer`. **Implemented:** the recorder refuses.
19. A pre-step history holding the 2900 smuggle: `project` does not raise and runs the step zero times. The inclusion is omitted from the sources rules join, and its marker makes its statement `not-supported` and keeps the new path present. The worksheet blocks, including with old answers present. Probes A4 and B; Track 1a-6 for the marker.
21. One valid inclusion beside an omitted one on the same statement: the statement is `not-supported` for the applicability reason. An unaffected second statement stays `plain-case-supported`, and the return still blocks. A reviewed correction re-binds the omitted inclusion. Track 1a-6.
20. A raw-line writer and a bare-registry writer: both persist the write (probes A5, A3). Replay treats the result as case 19.

Cases 2, 5, 7, 8, 10, 11 and 12 did not run in the probe. Case 13's admitted half did not run. Cases 14 through 18 are the Track 1a-3 counterexamples (`docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track1a3-correction-binding.md`). The Track 1a-5 report is `track1a5-adr-integration.md` beside it. The Track 1a-6 report is `track1a6-omitted-inclusion-support.md`.

This part does not make the deduction chain call `current_claim_applicability` directly. It does not set a person-visible sentence. It does not publish a schema.

## What stays unchanged

ADR 0075 stays as accepted. `link_coverage` still returns a reduction total or blocks. Its empty-list parameter, its sum, its blocks, and its option B admission are untouched. A result of that operator is a statement-specific claim only where ADR 0076 Parts 1 and 2 say so. This record does not say so for a new case.

ADR 0076 Parts 1 and 2 stay as accepted. A per-subject rule still declares `subject`. Both schedulers still wait on predecessor rule resolution rather than on an unsuffixed symbol. The two containment directions are unchanged, and one shared name is still not a pass. A joined row that lacks a required name still blocks every subject. No-link stays subject-local. Undeclared rules keep today's behavior, including the item 2 split on an undeclared collect.

ADR 0076 Part 3 stays open. Nothing here publishes an amount from several financing rows, selects whole-loan disqualification, a portion, or unresolved-blocks, or treats two periods as one qualified loan.

ADR 0073 stays as accepted. Retraction is admitted as today.

Published schema bytes stay put: `rule-artifact.v1` through `rule-artifact.v12`, `artifact-package.v1` through `artifact-package.v34` (there is no v27), `derivation-record.v1` through `derivation-record.v9`, `npe-walk.v1` through `npe-walk.v3`, and `derived-finding.v1` and `derived-finding.v2`. A run with no derived entry pin still writes `derivation-record.v9`, and its findings stay `derived-finding.v2`. No existing rule, package, or line 2b citizen is migrated onto v13 by this decision.

Ordinary `collect`, `count`, `link_count`, and `link_coverage` are unchanged. A closed-empty source family still publishes 0, now on the default path, which holds the worksheet's existing closed-empty branch. The worksheet's limit, phase-out, and MAGI arithmetic are unchanged.

## Schemas

Checked at this HEAD by listing `packages/schemas/derivation`, at `origin/main` and `origin/main-ui`, across every ref with `git log --all`, and in the schema-intent ledger on `origin/milestone-schema-ledger`. The highest versions here are `rule-artifact.v12`, `artifact-package.v34`, `derived-finding.v2`, and `derivation-record.v9`. These names are absent from this branch, from both ratified lines, and from the ledger: `rule-artifact.v13`, `artifact-package.v35`, `derived-finding.v3`, `derivation-record.v10`, `npe-walk.v4`. Track 0c section 4 found the same next rule and package names at the start of Track 0c.

Two notes on the names. `derived-finding.v3` has no file on any ref. It is named once, in a docstring in `packages/derivation/authorization.py`, as an optional later home for an authorization pin role. Nothing reserves it. `derivation-record.v10` has a different, unmerged draft on other refs: commit `96e98da8` on `repair/act-log-scope-declaration-schema-selector` and related branches, and tag `backup/pre-publication-curation-2026-08-31` at `3488e42a`. That draft widens the block-code vocabulary for ADR-0072. It is not on a ratified line or in the ledger. See "Open questions".

| Version | What it adds | When it is published |
| --- | --- | --- |
| `rule-artifact.v13` | Copies v12. Adds the `shared_key_count` expression, optional `basis`, and `selection` as an alternative to `value`. Each selection path and the default carry a `reads_subject_results` list. Activity may name `member_fact_types`. Does not add `aggregation`. Declared path pins stay `assertion` / `v1` or `choice`, so its pin `origin` enum is v12's. | Only after the owner accepts the parts whose fields it carries. A partial acceptance publishes only the accepted parts. |
| `artifact-package.v35` | Copies v34's admissions and also admits `rule-artifact.v13`. | With v13. |
| `derived-finding.v3` | Copies v2. Adds `derived` to the pin `origin` enum. A finding uses it only when it carries a Part 3 derived entry pin. | With v13, because only a v13 declared read produces that pin. |
| `derivation-record.v10` | Copies v9. Adds `derived` to the pin `origin` enum that disposition pins use. A run writes it only when one of its dispositions carries a derived entry pin. | With v13. |

None of these is published by this record. ADR 0076's publication rule applies: a published schema version carries only fields whose authorizing decision is accepted before that version is published. No field is added to a published version. The two pin successors follow from Part 3's derived entry pin. Part 5 adds no schema version. Its declaration is in-memory registry state, the same way `companion_presence_pairs` is.

Track 1a-5 probe C also checked `act-derived-publication.v1`. Its `finding.schema` is the constant `derived-finding.v1`, so it rejects a carried `derived-finding.v2` today, and it rejects v3 the same way. The pin successors add no new gap there.

The implementation track that adds the files appends the schema-intent ledger event before editing them, and appends checksums with `packages.kernel.schema_registry.write_manifest` for the new filenames only. If that manifest changes an existing entry or removes one, that track stops. This paper assignment does not append the ledger event and does not write a schema file.

Every closed schema-name set that currently stops at `rule-artifact.v12` has to admit v13, or a v13 rule never runs. Track 0c names the sets in `packages/derivation/live.py`, `runner.py`, `marshal.py`, `authorization_closure.py`, and `package_validation.py`. That list was traced in Track 0c. It was not re-derived for this draft. The places that choose `derived-finding.v2` and `records.CURRENT_RECORD_SCHEMA` need the conditional choice in the table. They were not traced for this draft either. The implementation track re-checks both. `packages/kernel` has no `rule-artifact` string. Track 0c checked that. No kernel change follows from Parts 1–4. Part 5 is outside that sentence. It adds one step to `ActLog.append`, one generic function in `packages/kernel/findings.py`, and the domain map the tax registry installs. This paper writes no kernel file.

## Evidence and gates

Gate 1, scored 0–2 on the four axes in `PROJECT_PLANNING.md` ("Prototype Economic Gates"). The proposition is: the four capabilities in this record are the grammar and runner behavior on `rule-artifact.v13`, admitted by `artifact-package.v35`, with derived entry pins on `derived-finding.v3` and `derivation-record.v10`, with the outcomes above. Part 5 is outside this score. It is an admission invariant, not a grammar or runner capability.

| Axis | Score | Reason |
| --- | --- | --- |
| Future blast radius | 2 | The operator, the basis field, the same-run read, and the selection binding are general grammar, not one rule id. Admitting v13 touches every rule-schema admission set that stops at v12. The derived entry pin adds a finding and a record successor, written only when that pin is present. The line 2b v8 gate does not move. v1–v12 rules are not rewritten. |
| Migration cost | 1 | Four new schema versions beside immutable history. No existing rule, package, record, finding, or walk is rewritten. A run with no derived entry pin writes what it writes today. Line 2b stays on v9. |
| Residual uncertainty after paper | 1 | The behaviors this record adopts were executed: the count list (Track 0d evidence 5, stand-in), the scope gap (evidence 6), the runner split and the coverage refusals (Track 0f item 2), the unauthorized v9 selection clone (item 3), the composed worksheet (Track 1a-4 item 4, stand-in), the repaired activity and the pin schema check (Track 1a-5 probes B and C). What has not run is a schema-valid v13 rule, because v13 does not exist yet. That is implementation of this contract. It is not a fork between rival shapes. Part 5 adds a further residual: its step ran only as a runtime patch. That does not rescore this cell. |
| Inability to test cheaply during implementation | 0 | The tests are the probe cases already written down, plus schema validation of v13, `derived-finding.v3`, and `derivation-record.v10`. No prototype rung. |

**Total: 4.** That is paper plus this ADR for the four capabilities, not a prototype, and not a score of Part 5. Tier 2 does not raise the rung.

Each row carries its status here. **Implemented** means code changed and tested on this branch. **Proposed** means paper or a disposable probe.

| Part | Evidence | Label in the report | Status here |
| --- | --- | --- | --- |
| 1 | Track 0d, evidence 5 | "executed with the runtime stand-in operator". Direct table and chain table. The production list at the end of that section. | Proposed |
| 1 | Track 0d, evidence 6 | "executed existing engine" for recovery; conclusions "executed with the runtime stand-in operator". The naive count publishes `plain-case-supported` after one affirmative remains. | Proposed |
| 1 | Track 0c, sections 1, 2, and 4 | Options A and B, the schema rejection of `shared_key_count`, the recommendation of option C. Command exit 0. Both runners agreed on values, pins, and blocked rows. | Proposed |
| 2 | Track 0e, sections 2 and 3 | The basis table and "What the result says", including the four groups. Paper. No probe was run in that track. | Proposed |
| 3 | Track 0f, item 2 | "executed existing engine" for the return-level rule and for the worksheet gate. The runner disagreement, the `requires` block, and `SLI_STATEMENT_COVERAGE` on a missing or blocked statement. This is the defect, not the repair. | Proposed |
| 3, 4 | Track 1a-4, items 1–4 | The composed declaration. "executed with the runtime stand-in operator" for worksheet dollars and the chain; "presentation only" for presentation. Old-only 2500, new-only 2500, both blocked on the presence token, closed-empty 0, nonempty-neither blocked on the box fact id. Both runners agreed. | Proposed |
| 3 | Track 1a-5, probe C | Existing schema validation: the Track 1a-4 new-only line 21 finding fails `derived-finding.v2` and its disposition fails `derivation-record.v9` on origin `derived`. In-memory successor copies accept both. | Proposed |
| 4 | Track 0f, item 3 | "executed existing engine". Schema rejection on v6, schema acceptance on v9, and `v9-declarative-binding-unauthorized` on all four presence cases. | Proposed |
| 4 | Track 0d, evidence 4 | The line 2b declaration, "not a run". The both-present worksheet clone is a different mechanism and is not this part. | Proposed |
| 4 | Nominee return-integration plan, "Contracts" | "Bounded declared path contract". The id gate this part leaves in place. | Proposed |
| 4 | Track 1a-5, probe B6–B11 | Executed with the runtime stand-in operator. An old answer with an unresolved inclusion deducts 2500 on the Track 1a-4 activity and blocks on the presence token with the repaired activity. The four Track 1a-4 cases keep their results. | Proposed |
| 5 | Track 6 case 3, on the base before the read-side tie; Track 1a-3 binding | Case 3 failed `AssertionError: 'current' != 'unresolved-applicability'`. The gap exists. The 1775-then-2900 reuse failed the same way before the Track 1a-3 fix. The recorder refusal and the read-side binding are in `packages/tax` and tested (Track 1a-3). | Implemented |
| 5 | Track 1a-5, item 1 | The three older tests expect `unresolved-applicability` after a direct append (Track 1a-5). | Implemented |
| 5 | Track 1a-5, probes A1–A5 | A runtime patch of `ActLog.append` over the real recorder, real `ActLog`, and real `project`. Prohibited writes leave no assertion; replay runs the step zero times and stays readable; no-claim logs are identical with and without the step; bare-registry and raw-line writers bypass it. | Proposed |
| 5 | Track 1a-5, probes B1–B5 | Executed with the runtime stand-in operator. Today's join deducts 2500 on a smuggled 2900. Omission blocks. Omission without presence deducts 2500 when old answers are present; with presence it blocks on the presence token. | Proposed |
| 5 | Track 1a-6 probe | Start states: recorder execution. Chain and worksheet: runtime stand-in. Omission plus presence publishes `plain-case-supported` and 1800 for one valid inclusion beside an omitted one; with the marker the statement is `not-supported` and line 21 blocks. Sole, two-omitted, unaffected-sibling, reviewed-route, both-present and the successful cases as in Part 5, "Replay". | Proposed |

Evidence boundary. The count rows are a stand-in, not production code. The v13 scheduler in Tracks 1a-4 and 1a-5 is a stand-in. The selection clone is schema-valid v9 and is not evaluated. The same-run table in Track 0f is the current engine, and it shows the defect rather than the repair. Part 5's step, its replay omission, and its applicability marker ran only as runtime patches. A green suite on the current tree is evidence for none of them. The recorder binding and the read-side check have run, and they are not that step. Hand-built findings in the probes use synthetic `demo-*` ids. No personal values are in the reports this record cites.

## Alternatives considered

**Track 0c option A, a closed-family `count` joined by today's `_scope`.** Executed. It returns 2 for two periods and 1 for one. It is not adopted. The join is the single-name join ADR 0076 Part 2 does not authorize. A financing row that lacks `borrowing` shrinks the count and is not named. The number exists only while a closure claim the product does not have is admitted. Removing the family, the mapping, and the closure leaves the package valid and blocks `count` with `SOURCE_SET_UNCLOSED`.

**Track 0c option B, a second hop on one statement rule.** Not executed. v12 rejects the extra field. It would need the same kind of new schema and new ADR, and it would carry several financing values into one statement result. That is the open Part 3 question. The count does not answer it.

**Lifting the v9 selection id gate.** Considered, because the item 3 clone is already a v9 rule. Not chosen. The gate is the shipped authorization: copied v9 syntax stays inspectable and inert. Lifting it would change who may execute a v9 selection, with no new schema version, and it would reopen the nominee line 2b checks. The general binding is a v13 declaration. Line 2b v8 is not migrated.

**Storing the basis on the finding or on the explanation walk.** Not chosen. Track 0e section 3: pins cannot carry the last two groups. The walk and the finding already name the rule. A new `npe-walk` or `derived-finding` version is not required to show text that lives on that rule.

**Teaching unsuffixed `requires` to see keyed rows.** Not chosen. Item 2 shows that declaring the unsuffixed symbol blocks both runners. ADR 0076 records why: the keyed publication does not fill the unsuffixed name. A separate declaration waits on the publisher's rule id.

**Relabelling the derived entry pin `assertion` / `v1`, or `assertion` / `v2`, to fit the published enum.** Not chosen. A per-subject result is not something the person asserted. The pin would validate and misstate its origin. Two additive successors keep the published versions as they are.

**Relying only on Track 6's read-side tie.** Not chosen. The tie is correct inside `current_claim_applicability`. The deduction chain never calls that function. It joins an inclusion to its statement by identity, so a direct same-identity box 1 append still lets an old inclusion apply. Probe B1 deducts 2500 that way. The owner chose to refuse that write at admission.

**Binding Part 5 in `apply_assertion`.** The previous draft. Not chosen. `project` runs `apply_assertion` on replay. A raise there makes a log that already holds the write unreadable. Skipping it on replay needs a switch inside the fold that every reader would have to set correctly.

**A new admission function each writer calls before `ActLog.append`.** Not chosen as the boundary. `append_publications` and `SyntheticW2EntryRuntime._seed` do not pre-apply their acts at all, and a writer that forgets the call bypasses it. `ActLog.append` is already the one call every writer makes. A writer may still call `enforce_new_write_invariants` early, to refuse a multi-act batch before its first append.

**Omitting an unbound inclusion from presence as well as from the join.** Not chosen. Probe B4: with old answers present, the return turns from both present into old only and deducts 2500. Owner decision 2 blocks a return that has both.

**Omitting an unbound inclusion and counting it only toward presence (the Track 1a-5 rule).** Not chosen. Its own statement never sees it. One valid inclusion beside it publishes `plain-case-supported` and line 21 1800 on both runners (Track 1a-6, owner's mixed case). The all-omitted case blocked only because no usable link remained.

**Counting the omitted inclusion as the person's unresolved inclusion.** Not chosen. The person did not say they cannot tell. The system could not establish applicability. Borrowing the person's fact would give the wrong reason in the wrong words.

**Keeping the omitted inclusion joined, with its support forced to 0.** Considered, not executed. The statement would refuse, through the link count or the coverage. But the rule would read an unusable inclusion as a current link of the new amount, and the statement's reason would be a count rather than the applicability.

**Editing ADR 0073 so that retraction is this check.** Not chosen. Retraction ends one finding and supplies no replacement. The assertion that follows is a different act: a new current finding. Refusing that assertion while a current dependent names the source leaves ADR 0073 Decision 1 as it stands. Part 5 cites ADR 0073 and does not amend it.

## Open questions

No repair needed an accepted ADR's decision to change. ADR 0076 Part 1 left the return-level reader open; Part 3 of this record decides that opening. ADR 0076 Part 3 is not decided here. ADR 0073's retraction stays as accepted. A workspace with no current dependent finding is admitted and replayed exactly as today (probe A2). Stating these parts does not require interpreting `docs/governance/`. The line 2b binding is not an accepted ADR; it is the nominee milestone contract and the v9 id gate, and Part 4 leaves both in place.

Six questions remain for the owner or Foreman.

1. **Which registry an `ActLog` carries.** The step reads the map from the `ActLog`'s registry. The relationship tests build that registry with `DerivationSchemas()`, which has no domain maps, and a direct append over it is admitted (probe A3). The implementation track has to choose where the map reaches those `ActLog`s. Replay protects a workspace either way.
2. **`derivation-record.v10`.** It is free on both ratified lines and in the ledger. A different draft with that name sits on unmerged repair branches and a backup tag. If that repair can still land, one of the two takes v11. The ledger event should be appended before either edits a file.
3. **Financing-keyed recorder facts and presence.** Part 4's new path names the statement-keyed facts only, following owner decision 2's "any loan link on any statement". Whether a financing cannot-tell, no, or withdrawal with no inclusion should also make the new regime present is not decided here.
4. **Presence of an omitted inclusion.** The replay marker keeps an unbound inclusion present for Part 4, so that owner decision 2 still blocks (Track 1a-6, old answers with a sole omitted link). That follows the existing decision. It changes no workspace without relationship claims. The owner may still want to confirm it.
5. **Pinning the box 1 finding an omitted inclusion was confirmed against.** Today it is reachable through the inclusion's evidence, not pinned directly. A source carries one finding id. A direct pin needs a second channel. Whether the walk is enough is open.
6. **Marker names.** The marker fact type, its value and the default `established` are names this record proposes. The package track may rename them. The meaning stays: a system fact, distinct from every fact the person records.

### Answers at implementation

1. **Registry.** `ActLog` refuses to open for writing unless its registry
   carries a valid Part 5 declaration, and checks again on every append.
   Read-only logs and explicitly named test-only logs are the only exceptions;
   a source scan fails if production code uses the test-only opt-out
   (Track 1e). This is the owner's acceptance condition.
2. **`derivation-record.v10`** is published by this milestone, with its ledger
   event recorded first.
3. **Financing-keyed facts and presence.** Not counted; presence follows owner
   decision 2 (any loan link on any statement). The worksheet's new-path
   activity also counts the person's statement-level doubt about which loan a
   statement covers (Track 5).
4. **Presence of an omitted inclusion.** Kept, through the applicability
   marker, which also makes its statement `not-supported` (Track 1a-6, built in
   Track 1e and Track 4).
5. **Pinning the confirmed box 1 finding.** The implementation retains the
   walk through the omitted inclusion's evidence; it adds no direct second
   source pin. Whether a future consumer needs that direct pin remains open.
6. **Marker names.** Kept as proposed, except the `established` default:
   Track 4 detects the marker by a per-statement count instead.

The final worksheet integration also reads a blocked result for each marker
directly. A marker can outlive its statement's current box 1, so the statement
count alone cannot keep that unresolved inclusion consequential. Worksheet v4
uses the existing Part 3 declared-result count: zero marker subjects is empty,
and any blocked marker result refuses the read. Package v41 adopts this check;
no new operator or schema is added.

The person-visible line 21 reasons, the recorder's scope facts, and mixed-period treatment are outside this record by the milestone plan. They are not open questions inside it.

## Consequences

- Tracks that implement this record publish `rule-artifact.v13`, `artifact-package.v35`, `derived-finding.v3`, and `derivation-record.v10` only after acceptance. Then they add the evaluator arm, the dispatch slot and pin loop, the package shape checks, the per-path same-run read in both schedulers, the v13 selection plan, and the derived entry pin. Existing v9 line 2b tests keep their current outcomes.
- A later rule can count current rows that share one key, state the four basis groups, read each current subject's result in the same run, and select one presence path or refuse when more than one is present.
- This record forecloses treating a current-row count as a scope conclusion, treating an undeclared collect as a same-run read of per-subject results, copying a v9 selection onto a rule other than line 2b v8 in the hope that it will run, and labelling a derived per-subject result as an asserted input.
- A run whose dispositions carry a derived entry pin writes `derivation-record.v10`. Other runs write `derivation-record.v9`. The blocks this record uses are `DEPENDENCY_INVALID` and, where a dependency is genuinely absent, `DEPENDENCY_ABSENT`. The `missing` list is what distinguishes a bad counted row, a bad subject key, a coverage gap, and a both-present refusal.
- Track 3 adds `tax.us.2025.sli.statement-inclusion-unresolved`, `tax.us.2025.sli.statement-inclusion-denied`, and `tax.us.2025.sli.statement-inclusion-withdrawn` before a worksheet that names them in its activity is adopted.
- After acceptance, the implementation track adds the step to `ActLog.append`, the generic `enforce_new_write_invariants`, and the tax declaration in Part 5. It publishes no schema for that part. A source with no current dependent, a first box 1 asserted before any inclusion exists, a withdrawal of the dependent, a correction of another fact type, and an ADR 0073 retraction stay admitted as they are today. A new finding of that source after the retraction is refused while a current dependent still names the source, unless that finding is the one successor the reviewed-scope evidence binds.
- **Implemented.** The tax correction writer refuses a new write that is not that bound successor, before any act is appended. The read-side check refreshes an inclusion only for that same successor. One scope evidence authorizes one finding. Reuse, a repeated amount, a changed box 1, a different predecessor, and the wrong evidence kind do not refresh it. The three older tests expect `unresolved-applicability` after a direct append.
- **Proposed.** `ActLog.append` refuses the same write for every writer that calls it. `project` never runs that step. Replay of a log that already holds an unbound rewrite does not raise. `marshal_run_context` omits the inclusion from the sources both runners join and supplies its replay marker in its place, so its statement is `not-supported`, the new path stays present, and the worksheet blocks instead of deducting. A workspace with no relationship claims is unchanged.
- Build obligations from the replay marker (Track 1a-6):
  - `marshal_run_context` supplies one `tax.us.2025.sli.statement-inclusion-applicability-unestablished` source per omitted inclusion, with that inclusion's identity keys and finding id and the value `sli.statement-inclusion.applicability-unestablished`. Both runners read the same sources. Nothing is written to the log.
  - The package declares the marker fact type, its default `established`, and its input binding. The per-statement conclusion rule requires it, publishes `not-supported` whenever a marker is present, and reads every marker on the statement, so each omitted inclusion is pinned. A per-statement echo publishes the marker value beside the conclusion.
  - Part 4's new path names the marker type.
  - The person-visible line 21 reason for this case says the statement changed without review and the link must be confirmed again. It does not reuse the person's "cannot tell" wording. That sentence belongs to worksheet integration.
  - Tests start from a saved log, recover it fresh, and run both runners. They cover the owner's mixed case, the sole omitted link, two omitted links, an unaffected second statement, the reviewed route (sole and mixed), both present, and the successful cases. A workspace with no relationship claims is unchanged.
- When the step lands, `test_case_3_direct_same_identity_append_does_not_keep_inclusion_applicable`, `test_case_5_unrelated_statement_inclusion_stays_applicable`, and `test_case_7_reviewed_correction_restores_applicability_after_direct_append` change: the direct assertion is refused and not recorded. The three older tests change again for the same reason. Cases 1, 2, 4, and 6 keep their current expectations.

## Links

- Plan: `docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion.md`, sections "Track 0 adversarial closure" and "Tracks".
- Evidence: `docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0c-link-count.md`, `track0d-closure-repair.md`, `track0e-conclusion-basis.md`, `track0f-mechanism-rows.md`, `track1a3-correction-binding.md`, `track1a4-worksheet-composition.md`, `track1a5-adr-integration.md`.
- Predecessor contracts: `docs/adr/0075-link-coverage-operation.md`, `docs/adr/0076-per-subject-scheduling-and-binding-relationships.md`.
- Line 2b authorization: `docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md`, section "Contracts"; `packages/schemas/derivation/rule-artifact.v9.schema.json`; `packages/derivation/runner.py` (`_attempt_declared_line2b_selection`); `packages/derivation/package_validation.py` (`RULE_SELECTION_UNAUTHORIZED`).
- Keyed symbol: `packages/derivation/subject_dispatch.py`.
- Schemas named and not created by this record: `packages/schemas/derivation/rule-artifact.v13.schema.json`, `packages/schemas/derivation/artifact-package.v35.schema.json`, `packages/schemas/derivation/derived-finding.v3.schema.json`, `packages/schemas/derivation/derivation-record.v10.schema.json`.
- Part 5 boundary: `packages/kernel/act_log.py` (`ActLog.append`); `packages/kernel/findings.py` (`project`, `apply_act`, `apply_assertion`); `packages/kernel/contribution.py` (`apply_contribution_batch`); `packages/derivation/marshal.py` (`marshal_run_context`). Pattern: `packages/kernel/findings.py` (`_enforce_subset_invariants`, `_enforce_companion_presence`, `_enforce_declaration_signal_contradictions`); `packages/tax/loader.py` (`install_domain_companion_presence`); `packages/kernel/facts.py` (`fact_id_for`). Retraction: `docs/adr/0073-assertion-standing-and-retraction-lifecycle.md`. Stale target: `track0f-mechanism-rows.md`, item 1. Track 6 evidence: `tests/test_sli_correction_entry_enforcement.py`.
