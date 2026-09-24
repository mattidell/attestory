# Bounded reader contract — statement groups on the citation-walk

> **Superseded (2026-09-24)** by [`reader-contract.md`](reader-contract.md), revised on the owner's five repairs. Kept as the record of the first draft.

> **Foreman note (2026-09-24), before owner review.** Section 3's `wording` **pin role** cannot be
> added without successors of `derived-finding.v2` and `derivation-record.v9`, whose pin-role enums are
> closed as well as the rule's — contradicting "no record bump for display". Adjusted proposal: the
> condition-wording entry is declared **on the responsibility rule** (a field of ADR 0076's
> `rule-artifact.v11`), and the projector reads it from the rule it already resolves. Findings and the
> record are unchanged. Draft status: not accepted; returned to the owner with this adjustment.


Read-only design. Branch `milestone/student-loan-circumstance-association`, HEAD `b558da4e097367319816568f41091d4fbab5d0b5`. Sources: `g2-path-investigation.md` Question 2, `a4-bounds.md` "Second pass — P4 result", `a5-stage4-scope-and-responsibility.md` Part 2, `a1-approval-set.md` "The responsibility message", `packages/derivation/presentation_projection.py`, `packages/presentation/pages/citation-walk.v1.html`, and `tools/presentation_harness`. ADR 0076 is not a file at this commit. It is the scheduling item ADR 0075 leaves open.

This document is the contract for the current reader. It does not approve wording, does not schedule a run, and does not change the derivation record.

The carrier is presentation projection. `build_presentation_model` writes what the page shows into the durable `presentation.json`. `derivation-record.v9` stays `derivation-record.v9`. No `published` array, no `value` on disposition rows, no new record code.

The reader case is not complete until both of these are true:

1. The condition wording and the case-2 note have the source named in section 3, and the projector copies that source.
2. A statement-scoped responsibility rule has actually run for a bare statement and published the finding section 4 describes.

"School unknown" is never inferred from a missing pin. A row that did not pin a school has not decided that the school is unknown.

## 1. The projection

`presentation-model.v1` stays the version string. This is the `provenanceGroups` precedent: an internal validator change, not a published schema, not a version bump. Existing models that lack the new keys remain valid and render as they do today.

The form line stays one section. Section id stays `line-{line}` (`line-sch1-21` for `tax.us.2025.schedule1.line-21`). Duplicate section ids stay rejected. Keyed statement rows are groups under that one section. They are not new sections, and they are not `provenanceGroups`.

### Join

A disposition row belongs to the field when either:

- its `symbol` is exactly `field.binds_symbol`, or
- its `symbol` is `field.binds_symbol` plus `|` plus a fact id,

and in both cases the resolved rule's own `publishes` equals `field.binds_symbol`. The check reads the rule that ran. It does not rewrite `publishes` on a copy. P4's synthetic member is not the join.

`_one_row` applies only to an unsuffixed symbol. Many keyed rows for that same unsuffixed symbol are the groups, not an ambiguous join. Zero rows is still a failure. An unsuffixed row and one or more keyed rows for the same symbol is a failure. The projector does not pick one.

The field's `binds_symbol` has to be the unsuffixed symbol the per-statement amount rule publishes. Schedule 1 line 21 today binds `tax.us.2025.schedule1.line21-sli-deduction`, the return-level worksheet total. The projector must not hang statement groups on that row. Retargeting the citizen is a content change, not something the projector guesses. Until a field binds the per-statement symbol, there are no statement groups.

The owning-rule citation check keeps today's rule: `rule.publishes == field.binds_symbol`. A keyed symbol does not fail that check. Responsibility rules are not required to own the field.

### What a section gains

Optional `statementGroups`, one object per keyed row of the field's symbol. Required keys when the array is present:

| Key | What it is |
| --- | --- |
| `symbol` | The keyed symbol, `publishes\|fact_id` |
| `factId` | The suffix after `\|` |
| `findingId` | The row's finding id |
| `ruleId` | `artifact_id` of the rule that published it |
| `disposition` | The row's disposition |
| `value` | The published value, copied from the in-memory finding. Absent when the row is blocked |
| `basisOrigin` | `assertion` or `declared_default`, copied from the input pin that carried it. Absent when no such pin exists. Never computed by noticing which pins are missing |
| `nodes` | Intermediate findings the downward walk passed through and today throws away: each reduction and each status, with `findingId`, `ruleId`, `symbol`, `value`, `basisOrigin`, and its pins. Leaves stay leaves |
| `missing` | Present on a blocked group. Each entry is a `missing` id from the disposition, resolved through recorded state to `findingId` plus the recorded fact id or symbol. An unresolved id is a projector failure, the same as today's unrecorded-lineage failure |
| `responsibilities` | Rows found by the reverse walk below. Empty is legal |
| `lineNote` | The ordinary-line wording string, present only when a finding in this group pinned that wording entry. Copied, not composed |

`citationSites` stay the non-closure leaves of the amount. The status finding's examined enrolment is a pin on that status node, not the only thing the line cites. The amount's number stays the field value.

### Blocked line

`resolved` for a blocked field gains optional `missing`, the same resolved entries as the group's `missing`. `activeCodes` stays the code list. A code alone is not the link name. The four invalid shapes (uncovered link, orphan, duplicate, non-numeric) already differ by `missing` and pins on the record. After this copy they differ in the presentation file. No new record code.

### Default basis

`basisOrigin` is the pin's `origin` and nothing else. `declared_default` is the basis. The sentence "taken as met because nothing you've described says otherwise" is not that pin and is not derived from it. It appears only as `lineNote`, and only when the finding pinned the wording entry in section 3.

On the no-link path the parameter pin is copied onto the group as a pin with its origin. It is no longer visible only inside `resolved.act`. Citation sites are not required to treat a parameter as a leaf. The basis is the pin and `basisOrigin`, not a new citation site invented for it.

### Reverse walk

After the downward nodes of a group are known, take every disposition that is not already one of those nodes. If one of its input pins names a finding id already in the group, including the amount finding, attach that disposition as a responsibility row. The downward walk does not find these rows. P4 showed nothing on the amount's pin list is the responsibility.

A responsibility row carries: `ruleId`, keyed `symbol`, `findingId`, categorical `value`, its pins, and `wording` when a pin names a condition-wording citizen. `wording` is the citizen's text after the slot rule in section 3. The row is not a citation site and is not fed through the field's citation chain.

Do not attach a disposition merely because it shares a rule family, a tax year, or an absent pin.

### Validator

`validate_presentation_model` changes as follows.

- Top-level required keys are unchanged. `provenanceGroups` and `authorization` stay the only optional top-level keys, with their current checks.
- A section may include `statementGroups`. Unknown section keys other than that one still fail.
- Each group must have the keys in the table above. `value` may be absent only when `disposition` is `blocked`. `missing` is required when `disposition` is `blocked` and forbidden when it is not. `lineNote` and `responsibilities` may be empty or absent only as specified: `responsibilities` defaults to empty; `lineNote` is omitted rather than invented.
- `basisOrigin`, when present, is `assertion` or `declared_default`.
- Every `missing` entry resolves to a finding the model already recorded. A bare id with no recorded fact id or symbol fails.
- `wording` and `lineNote` must equal the pinned condition-wording citizen's text after the slot rule. Any other string fails, including a string the projector built from a template.
- A group or responsibility whose rendered text says the school or programme is not known fails unless the pinned wording entry's `circumstance` is `not-known`.
- A slot filled from a key the finding did not pin fails.
- The unsafe-string check (`</script`, `<!--`) applies to every new string.
- Keyed-symbol owning-rule failures described above fail closed.
- `provenanceGroups` is unchanged and is not a substitute for `statementGroups`.

### What stays out of the model

- Any edit to `derivation-record.v9`, including a `value` field or a `published` array.
- A new disposition code.
- `provenanceGroups` as the carrier for this chain.
- One section per statement.
- A question, a confirmation flag, or a screen-wide warning flag.
- A school name, the word "unknown", or the case-2 sentence, unless a pinned wording entry or a pinned fact key supplied it.
- The categorical token rendered as the line's display value. `applies` is not a sentence.
- Rewriting the form field's `label`, `description`, or `explain`.

## 2. The page

The page is `packages/presentation/pages/citation-walk.v1.html`. The walk change is also applied to `tools/presentation_harness/examples/pages/citation-walk.v1.html`, because the product page says a change to the walk belongs in both. The evaluation copy keeps its synthetic declaration. It is not the page this contract's test loads. `live_session` keeps refusing that copy.

`renderLine` stays the one render path for the line's own disposition: the amount or the block, the field's own `explain`, the leaf citation buttons, the field citation. New regions are added only on a section that has `statementGroups` or a `lineNote`. Other lines are unchanged. Nothing is added to the page header, and nothing is rendered once for the whole screen.

The conditions are not `role="alert"`. They do not use the blocked banner ("No value published — cannot compute.") or the remedy box. Those stay on a real blocked disposition only. The conditions are not inputs, not checkboxes, and not questions. The explanation is a disclosure inside that line's section: collapsed in the ordinary view, opened by a control on that line, containing only what the model copied.

Renderer-owned strings (`REASON_TEXT`, the blocked banner, the remedy sentence, `ATTACHMENT_EXPLAIN`) are not a home for these sentences. The page renders model text or it renders nothing.

The sentences below are the owner's candidates from stage 4. They are quoted so the page has a target. They are not an approval act. A1's single responsibility paragraph is not the text.

### Nine-credit

The person enrolled in the BSc and the certificate programme at Riverside in autumn 2024, nine credits, and a financing claim names the period. The line shows the amount, its leaf citations, and the status node. The nine-credit telling is an examined input of that status node, not the ground of the amount and not the ground of eligible-student.

The disclosure shows three conditions, each distinguishable from an ordinary citation button by being a responsibility row (rule id and keyed symbol), not a `citationSites` entry:

> You are responsible for these conditions: that Riverside College was an eligible institution; that the programme you were pursuing led to a recognised credential; and that your course load met Riverside's half-time standard for that programme. They apply because you claimed the student loan interest deduction for [statement] and described enrolling at Riverside College in autumn 2024.

The circumstance named is the one the finding pinned (institution, programme, period). The treatment is the statement amount the reverse walk attached. `basisOrigin` on the status node is shown as the default basis. The case-2 note is not used. Nine credits are not stated as having met the half-time standard.

### Financing claim, no schooling circumstance

The person said only that this loan paid tuition for the Riverside BSc in autumn 2024. Same line structure. The disclosure uses the case-1 candidate:

> You are responsible for these conditions: that Riverside College was an eligible institution; that the BSc led to a recognised credential; and that your course load met Riverside's half-time standard. They apply because you claimed the student loan interest deduction for [statement] and said this loan paid for the Riverside BSc in autumn 2024.

The because-clause must not say the person described studying or enrolling. The financing claim remains a citation of what was said. It is not labeled as enrolment and not labeled as the ground of eligible-student. The default basis is the status node's `basisOrigin`, not the case-2 note.

### Bare statement

Nothing about schooling and nothing about what the loans paid for. The ordinary line shows the amount and this note, and no other new sentence:

> Eligibility for this deduction is taken as met because nothing you've described says otherwise.

The three conditions are not in the ordinary line's text. They are in the disclosure:

> You are responsible for these conditions on the interest reported on [statement]: that whatever education these loans paid for was at an eligible institution; that it was in a programme leading to a recognised credential; and that the course load met that institution's half-time standard. They apply because you claimed the student loan interest deduction for this statement. Which school and programme are not known here — nothing you've described names them.

The statement is named from the group's `factId`. No institution and no programme are named. "Not known" appears only because that sentence was copied from the pinned wording entry.

### Uncovered link

The line is blocked. The page shows the code it already shows, and it shows each resolved `missing` entry's recorded identity, so the link is named. Orphan, duplicate, and non-numeric do not render the same text, because their `missing` lists differ. No responsibility rows are shown: a treatment that was not taken has no responsibility on it. The blocked banner is appropriate here and is not the condition register.

### No-link default

The line is published. Box 1 remains a citation. The parameter pin and `basisOrigin: declared_default` are visible on the group. They are not left only inside `resolved.act`. This is the coverage default (nothing to reduce), not by itself the bare-statement note. When the return is also a bare statement, the note of that case is shown as well, from its own wording pin. The page does not treat "no link" as "school unknown".

## 3. The wording source

### What the projector may copy today

Every string that reaches the model is one of the following. Nothing else is a governed source.

| Source | Where it lands | The page reads it |
| --- | --- | --- |
| Form-field citizen, copied whole onto `section.field` (`form-field.v2` / `v3`) | `label`, `description`, `line`, `form.*`, `citation` id and version, each disposition's `render`, `explain`, and blocked `codes` | `label`, `line`, `render`, `explain`, `codes`, field `citation`. Not `description` |
| Evidence `label` (`evidence.v1`) | `pinLabels`, via `_evidence_label` | Citation button text. Absent label falls back to `pinId@pinVersion` |
| Attachment title (`attachment-rule` `title`) | Attachment status and citation-group `title` | Yes |
| Itemization `label`, adjustment `label` | Part `heading`, citation `context` | Yes, as heading |
| Published numeric `value` | `resolved.value` | Yes, through `{value}` |
| Published categorical `value` | Compared to the field's `render`, then stored only inside `resolved.act`. The page is required not to read it | No. The instruction `render` is shown instead |
| Adjustment row `label`, `kind`, `row_sum`, and the derived finding `value` | Citation-group tie-out text and `provenanceGroups` | Tie-out text on a citation group only. The page does not read `provenanceGroups` |
| Fact-type `title`, and the unsupported finding's `value` | `unsupportedSourceFindings` | No |
| Authorization provenance | Optional top-level `authorization` | No |

Two further strings are composed by the projector, not copied from a citizen: `_reader_label_for_finding` (`{adjustment label} — {payer}` or `{adjustment label} report group`) and the tie-out templates (`Reported subtotal: {value}`, `Adjustment: -{row_sum}`, `Recorded contributing reduction {value}`). Both serve the attachment path. They are not a wording mechanism to extend.

`citation.v1` is resolved and then dropped. Its `authority.title` and `section` never reach the model. `rule-artifact` `notes` is not read. A parameter id is not a sentence.

### Human text that exists and is not a source

| Citizen | Human text | Why it is not the condition message |
| --- | --- | --- |
| `form-field.v3` `description` and disposition `explain` | One string per line. Line 21's `explain` talks about worksheet eligibility, MAGI, and an unclosed box-1 family | One text for every return. Cannot name Riverside on one statement and "not known" on another. Putting the conditions here would put them on the ordinary line, which case 2 forbids |
| `rule-artifact.v10` `notes` | Free developer text. The schema does not govern it as wording | The projector does not copy it. Stage 4 already rejected it |
| `citation.v1` | A locator. `authority.title` is a code title, not a sentence | No message. One locator can stand for two conditions. Same role as an ordinary citation |
| `fact-type.v2` / `v3` `title` | Developer description. The 1098-E eligibility components in `f1098e.bundle.json` are yes/no absence witnesses; their titles are those descriptions | A fact type types an assertion. A responsibility is not one. The projector copies `title` only onto `unsupportedSourceFindings`, which the page does not render. Repurposing `title` is the alternative stage 4 rejected |
| `evidence.v1` `label` and `content` | The person's evidence | Not a condition. Only `label` is copied, and only onto `pinLabels` |
| `finding.v2` `capture` | `presented` and `asserted` of an assertion | Rides along only if the finding is embedded in `resolved.act`. The page does not render it. A responsibility has no capture |
| `source-family.v2` `title`, `closure_claim`, constraint `meaning` | The family's natural-language closure claim | Not read by the projector. A family claim is not a per-condition responsibility |
| `parameter-declaration.v1` | `values` only. No message field | A parameter id is not the approved sentence |
| `entry-field.v1` | `purpose`, source `label`, `hintLabel`, `errorLabel` | Entry loop. This projector does not read it. Those strings are prompts and refusals, which this page must not become |
| `attachment-rule` `title` and `label` | Schedule attachment headings | The attachment path. Not this line |
| `checked-conclusion-binding.v1` `title` | Schedule D conclusion binding | Not read. Not these conditions |
| `quantity-vocabulary` | Closed tokens, no prose field | Not a sentence |

Page constants are not content. Adding the candidates to `REASON_TEXT` or to a new frozen object in the HTML would put owner-approved tax wording in two page copies, outside content governance, and would make the page an author. ADR-0046's zero-authority rule is that the page renders the model. `ATTACHMENT_EXPLAIN` is not a precedent for tax wording: that text has no content surface because the attachment ontology has none. These sentences do need a surface.

### Recommendation

A new citizen, `condition-wording.v1`, schema file `packages/schemas/tax/condition-wording.v1.schema.json`. New published schema. Not an edit of any existing `*.vN.schema.json`. Checksum appended with `packages.kernel.schema_registry.write_manifest` for that directory. If the manifest changes an existing entry, stop.

This is the content declaration stage 4 left open. It is preferred to holding the sentences in the page or in Python, which is the other open option, because that option fails the projector's copy rule and the page's zero-authority rule.

One citizen, entries keyed by condition and case. Each entry:

- `condition`: `eligible-institution`, `recognised-credential`, or `half-time`, or `ordinary-line-note` for the case-2 note.
- `case`: `described-enrolment`, `financing-claim`, or `bare-statement`. The note's case is `bare-statement`.
- `circumstance`: `named` or `not-known`. `not-known` is legal only on `bare-statement` condition entries.
- `text`: the owner's candidate for that case, with slots only where that sentence has them: `{statement}`, `{institution}`, `{programme}`, `{period}`. The bare-statement condition text and the note have no institution, programme, or period slot.

The rule pins the entry. Pin role `wording`. `rule-artifact.v10`'s role enum is closed and does not include `wording`, and v10 cannot gain it. ADR 0076's rule successor is the schema that has to admit this role, in the same publication as `subject`, so the wording pin does not force a further rule version. Role `citation` is the wrong role: stage 4 showed a citation pin cannot say "this is a responsibility" or carry the sentence.

Slot rule. The projector replaces a slot only with a key on a fact the finding pinned. A missing key does not become "unknown", an empty string, or a placeholder. A bare-statement entry has no such slots, so there is nothing to fill. The case-2 note is pinned by the statement-keyed favourable conclusion (the default basis), once. It is not repeated on each condition rule.

Until the pin exists, the model may carry the responsibility's identity and must not carry the sentence. The page then shows the rule id and symbol and no message. That state is not a completed reader case.

## 4. The statement-scoped responsibility rule

Three rules, one per condition. The probe rule `demo.rule.responsibility-eligible-institution` is not this rule. That rule publishes when status is `not-adverse`, its subject in P4 was the financing claim, and with subject box 1 it blocked `DEPENDENCY_ABSENT` because it requires status. Status sources are keyed to financing claims. Requiring status is what makes the bare statement unable to publish.

### Subject

The subject is the statement fact type `tax.us.2025.f1098e.box1-student-loan-interest` (identity keys lender, statement, tax-year). Not a financing claim, not an enrolment, not a run-wide box-1 scalar.

### What it reads

- The current box-1 finding for that statement. That is the asserted input that establishes the subject. Origin `assertion`.
- The published per-statement amount finding for that same statement. That is the treatment. The amount rule does not read the responsibility. The responsibility is not an input of the amount.
- The condition-wording entry for this condition and `case: bare-statement`.
- Its own citations, this condition's authorities only.

It does not read enrolment, a financing claim, a school, a programme, a period, or a status finding. It does not read the absence of any of those.

### What it publishes

One categorical finding per statement. Symbol is the unsuffixed condition symbol plus `|` plus the statement fact id. The value is a declared applicability token, not the prose. The finding pins the wording entry whose `circumstance` is `not-known` and whose text is the bare-statement sentence. That pin is how the finding says the school and programme are not known. A value of `applies` with no wording pin does not say it, and the projector must not complete the sentence.

Nothing consumes the finding. It lapses when the favourable treatment it rests on is not published.

### What it pins

- The statement's box-1 finding, role `input`, origin `assertion`.
- The per-statement amount finding, role `input`, so the reverse walk attaches it to that statement's group.
- Citation pins for this condition only.
- The wording pin for the bare-statement entry of this condition.

It does not pin an institution, a programme, a period, a financing claim, or an enrolment. It does not pin a default finding it does not publish. It does not pin a sentinel that means "unknown" by being absent.

The ordinary-line note is not this rule's pin. The statement-keyed favourable conclusion pins that entry. The conclusion's input is the statement's box-1 finding, as stage 4 designed, so the conclusion has an asserted input. Its `basisOrigin` is `declared_default` only when an input pin actually has that origin.

### Which scheduling it needs

ADR 0076, the subject declaration on the rule (Question 1's candidate (a), which the owner favours). Not a package-level map, and not a Python id list. A map can omit this rule and it then publishes once, unsuffixed, or blocks once. An id list will not track three content rules.

What that scheduling has to provide for this rule:

- A required `subject` on the rule successor, an exact fact-type pin to `tax.us.2025.f1098e.box1-student-loan-interest`. `rule-artifact.v10` has `additionalProperties: false` and no subject field. The same successor admits pin role `wording`.
- The package successor that admits that rule schema.
- Eligibility waits on predecessor **rule resolution**, not on the unsuffixed symbol appearing in `self.symbols`. The predecessor is the per-statement amount rule. It is not the schooling-status rule. Keyed publication never inserts the unsuffixed name, so a `requires` entry of that name stays ineligible and `finalize_unreached` would then evaluate the rule once, unsuffixed.
- The intercept is on `attempt` and on `finalize_unreached`, so `runner._execute` and `reference_runner.run_reference` share it.
- One dispatch publishes per statement. The rule id resolving once must not collapse the three statements into one unsuffixed finding, and must not block every statement because one amount was blocked. A statement whose amount is blocked gets no responsibility finding. The other statements still publish.
- These rules are not `link_coverage` rules. They do not join links. ADR 0076's link-binding half still gates the amount they qualify: until a joined link is this statement's, a coverage result is not a statement-specific claim, and this rule must not be shown as qualifying one. The rule's own grain does not depend on a shared key name with a link type.

Situation-scoped responsibility rules, for the nine-credit case and the financing-claim case, stay per schooling situation. Their subject is that situation, and their pins name the institution, programme, and period. They are not this bare-statement rule. They use the same wording citizen, the `named` entries, and the same reverse walk.

## 5. The demonstration standard

P4 inspected `build_presentation_model`'s return value while the run object was still in hand, and it did not load the page. That does not satisfy this contract.

The test does all of the following.

1. Run the bare-statement case, the nine-credit case, the financing-claim case, an uncovered link, and a no-link default through the real writers. The live path already writes `outputs/<stem>.presentation.json` from `build_presentation_model` before it returns.
2. Discard the run result, the publications, the dispositions, and any in-memory model. The rest of the test may hold the path of the presentation file and nothing else from the run.
3. Read that file back from disk. `validate_presentation_model` on the reloaded JSON is allowed. It is not the page proof.
4. Load the product page. Read `packages/presentation/pages/citation-walk.v1.html`. Replace `__MODEL_JSON__` with the file bytes, which is the splice `live_session` performs (`const MODEL = Object.freeze(__MODEL_JSON__);`). Serve that one document on the harness loopback and open it in a fresh Chrome target, the way `tools/presentation_harness/lib/executor.mjs` loads a candidate.
5. The harness server today splices only `__FIXTURE_JSON__`, and only into the evaluation page. The test must splice the product page's token. The fixture bytes are the re-read presentation file, not a hand-written golden and not the evaluation copy.
6. Assert with the harness check `dom-text-present`: `textContent` of the loaded document includes the sentence the case requires and excludes the sentences section 2 forbids. Assert the disclosure control is inside the line section and that no other line contains the note or the conditions. Assert the conditions have no `role="alert"` and no input control. Assert an uncovered link's text names that link and differs from the other three invalid shapes. Assert a model with no wording pin does not contain the sentence. Assert a model whose finding pinned no school, and whose wording entry is not `not-known`, does not contain "not known" or "unknown".

A passing structural check on the Python object, or a passing check on the evaluation page, is not this demonstration.

Out of scope for the demonstration: the full `pytest` suite as a substitute for the page load; a second derivation from the closing record; `explain()`; personal or live workspace data; approving the candidate sentences.

## 6. Limitations and completion

`derivation-record.v9` does not retain intermediate values. A closing record written with `use_v2=True` stores pins and dispositions. It does not store `published`, `blocked`, or `value`. `out.json` stores dispositions and no findings. The values this page shows — the amount, a reduction, a status, the applicability token — are in `presentation.json` only because the projector copied them from memory while it built that file. A reader that ignores `presentation.json` and reads the record cannot show them. Identity joins (which link, which status, which responsibility, whether an input pin is `declared_default`) remain on the record. This contract does not add a record version to move the values. The demonstration is void if the page was explained by re-reading the run object.

The presentation file is not a reconstruction. If it is deleted, the page is not rebuilt from the record under this contract.

Completion. All of these are required. Any one missing means the reader case is not complete.

1. `condition-wording.v1` is published as a new schema, the projector copies it, and the page renders the copied text for each case in section 2.
2. The three statement-scoped rules have run for a bare statement under ADR 0076's subject declaration, published keyed findings, pinned the `not-known` wording entries, and not pinned a school.
3. The reloaded `presentation.json` contains the statement groups, the kept intermediate nodes, `missing` resolved to the named link, `basisOrigin`, and the responsibility rows from the reverse walk.
4. The product citation-walk page, loaded from that file after the run object was discarded, shows the five cases in section 2 in the owner's register.
5. A projection that sees a missing school pin and no `not-known` wording pin does not render the school as unknown.

Not this contract: ADR 0076's full link-binding decision, the legal-obligation consumer, the partial-reduction remainder, entry-loop questions, a change to the incumbent eligibility witnesses, and any edit to an existing published schema file.
