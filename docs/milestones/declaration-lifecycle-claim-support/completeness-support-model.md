# Workspace Calculation Authorization Model

## Product model

One standing authorization permits the application to use the relevant current
workspace facts as the exhaustive input universe for ordinary return
calculation. The authorization is reused across ordinary additions, removals,
reclassifications, and corrections. Each change selects a new workspace revision
and causes recalculation; it does not reopen a family-by-family questionnaire.

Four concepts remain separate:

1. **Current workspace facts** are the findings that currency and marshalling
   select at a particular revision.
2. **Standing calculation authorization** is the user's permission to treat
   those current facts as the operative calculation universe within a bounded
   scope.
3. **A run** applies adopted rules, parameters, and operation semantics to that
   revision under the authorization.
4. **A result** is the run's calculated output. It is not a filing declaration,
   a saved scenario, or a durable workspace fact merely because the runner calls
   it a publication.

The authorization does not convert unknown facts into known zeroes one at a
time. It authorizes the product to calculate across the selected workspace
universe. It also does not certify source-content accuracy, tax-law coverage,
legal effect, filing readiness, or the impossibility of later information.

## Two independent support requirements

A calculation that presents a tax total — "2025 US-federal taxable interest
is $X" — needs two things, and the standing authorization above is only one
of them:

**A. Workspace-record sufficiency.** The current workspace is treated as the
complete input record for this calculation. The standing authorization (or a
narrower family confirmation when it is inactive) supplies this.

**B. Tax-model sufficiency.** The adopted, versioned fact vocabulary,
classification rules, composition, exclusions, and adjustments cover the
exact tax concept being claimed. This is established, if at all, by the
application's own declared artifacts and their coverage account — never by
the user's authorization. A user cannot authorize the application into
having modeled every category tax law recognizes; that is a fact about the
adopted content, not about permission to read the workspace.

These are independent axes. A workspace can be authorized as exhaustive
while the adopted vocabulary covers only part of the tax concept being
calculated (the committed line-2b case below is exactly this). A vocabulary
could in principle cover the whole tax concept while the workspace itself is
incomplete. Presenting an exhaustive-total claim honestly requires both.

## Conceptual layers

Five distinct things are involved in a claim like "2025 US-federal taxable
interest is $X," and conflating any two of them is the defect this document
corrects:

1. **Evidence.** A submitted Form 1099-INT, statement, or other document is
   evidence. Its arrival does not itself establish a tax finding — someone or
   something still has to read it and assert a proposition about it.
2. **Workspace facts.** A workspace finding records a proposition about the
   taxpayer's circumstances, or about what an information return reports. A
   form-oriented fact is legitimate when its proposition is genuinely
   form-oriented — "this logical Form 1099-INT statement reports $X in box
   1" — and its identity must remain independent of the uploaded file or
   evidence id (see "Form-oriented facts are peer to evidence, not evidence
   themselves" below). Other facts may be economic or tax-domain facts
   without any form behind them — interest received without a Form 1099-INT
   is already committed content, not a hypothetical. Whether all
   form-oriented facts should eventually be replaced or supplemented by
   economic-event facts is successor investigation, not decided here.
3. **Tax classification and composition.** Adopted rules determine which
   workspace facts are relevant to a tax concept, how they are characterized
   under the declared jurisdiction and tax year, which positive amounts,
   exclusions, and adjustments participate, and whether the declared
   categories are coextensive with the output claim. This is system/
   adopted-machinery responsibility. The user does not establish it by
   authorizing use of the workspace.
4. **Derived tax concept.** "2025 US-federal taxable interest for this
   taxpayer is $X" is a tax concept independent of any Form 1040 field or
   Schedule B location that presents it. It need not be directly asserted by
   the user; adopted rules may produce it from current findings. The
   repository's current representation is the output symbol
   `tax.us.2025.interest.taxable-total`. Whether that symbol-plus-rule shape
   is a sufficient long-term declaration of a derived tax concept, or
   whether a stronger, fact-type-like citizen is needed, is successor
   investigation.
5. **Presentation.** Form 1040 line 2b and Schedule B present or support the
   derived concept. They do not own its identity. Schedule B in particular is
   generated return material, not a family of source documents — and it
   covers several distinct subjects (interest, dividends, payer itemization,
   foreign accounts, foreign trusts), so "all Schedule B facts" is never a
   precise closure proposition for any one of them.

## Tax context

Federal reporting is about the return's tax totals, not the application's
internal source-family inventory. IRS Publication 550 requires taxable interest
to be reported even when no Form 1099-INT was received and identifies interest
and adjustments beyond a simple list of Forms 1099-INT
([IRS Publication 550 (2025)](https://www.irs.gov/publications/p550)).
The 2025 Form 1040 asks for total taxable interest on line 2b and has one
return-level knowledge-and-belief declaration at filing
([2025 Form 1040](https://www.irs.gov/pub/irs-pdf/f1040.pdf)).

Accordingly:

- source-document completeness is not tax-law completeness;
- source-family closure is an application-created support mechanism;
- lack of internal closure is not itself a federal bar to draft calculation;
- calculation authorization and the later filing declaration are different
  acts with different scope and consequence.

## Current committed machinery

### Form-oriented facts are peer to evidence, not evidence themselves

`packages/content/tax/2025/f1099int.bundle.json` declares
`tax.us.2025.f1099int.box1-interest`: a determinable fact whose `identity_keys`
are `payer`, `statement`, and `tax-year` — no file, upload, scan, document, or
evidence identity key. Its own title states the statement instance "is peer
to evidence and its identity carries no file, upload, scan, document, or
evidence key," and that a corrected copy of the same logical statement
answers the same fact and supersedes the prior finding. This is the
committed shape of a legitimate form-oriented fact: its proposition is about
what one logical statement reports, not about a piece of evidence.

`packages/content/tax/2025/interest_composition.bundle.json` shows this is
not the only shape available. Alongside 1099-INT box-3 and 1099-OID box-1
facts (both form-oriented, same pattern), it declares
`tax.us.2025.non-form-interest.amount`: "Interest income received without a
Form 1099-INT/OID statement instance for 2025" — a genuinely non-form,
economic fact, already present in committed content. Whether all
form-oriented facts should eventually be replaced or supplemented by
economic-event facts more broadly is successor investigation this document
does not resolve.

### Record and currency

The append-only record projects current findings before a run. The marshaller
reads `currency.current_finding_ids`, each finding's `fact_id` and `value`, the
mapping's `closure_fact_type` and `closure_horizon_key`, and projected
`horizon_state.current_by_chain`. It does not rely on a finding's `basis`,
`evidence_ids`, `capture`, `pins`, or `contribution_id` when constructing
`ClosureFindingRecord`; those sibling fields remain available elsewhere in the
record (`packages/derivation/marshal.py:158-205`). The downstream consumer is
`resolve_closure_admissions`, called once by `_Run.__init__`
(`packages/derivation/runner.py:166-183`).

ADR-0017's horizon lifecycle makes membership transitions an individuation
root. Addition, removal, and predicate-changing reclassification create a
successor horizon and displace closure keyed to the predecessor; a same-member
value correction does not (`docs/adr/0017-recorded-family-horizons-for-closure-freshness.md`,
Decisions 3-7).

### Closure admission

Each adopted `source-closure-mapping.v2` names a family, member fact type,
closure fact type, horizon key, admitted subtotal symbol, and
`current-literal-true` condition. For 1099-INT box 1 those fields appear in
`packages/content/tax/2025/closure-mapping.f1099int-b1.json:2-10`; sibling
family wording and the closure fact's Boolean value schema appear in
`packages/content/tax/2025/family.f1099int-b1.json:2-9` and
`packages/content/tax/2025/f1099int.bundle.json:23-35`.

`resolve_closure_admissions` reads the mapping and declaration identity/version,
current horizon, closure finding identity, fact type, horizon, and value. It
admits exactly one literal-true current finding and rejects absence, false,
displacement, non-Boolean truthiness, and duplicates. It does not read the
finding's basis or author information because those fields are absent from
`ClosureFindingRecord` (`packages/derivation/source_authority.py:65-97,100-166`).
The resulting family map is consumed by `runner.env()` as
`Environment.closed_sets` (`packages/derivation/runner.py:286-295`).

### Evaluation

The evaluator's operators use closure differently:

- `collect` reads closure only when no source rows exist. Nonempty rows aggregate
  without reading or pinning closure.
- `count` reads closure whether rows are empty or nonempty.
- `require_closed` always reads closure.

Those branches read `Environment.sources` and/or `closed_sets`; they do not read
closure findings, mappings, or horizons directly
(`packages/derivation/evaluator.py:118-141,206-211`). `runner.pins_for` converts
each successful closure read into exact mapping, declaration, and closure-finding
pins and also records sources, parameters, rule identity/version, and operation
semantics actually read (`packages/derivation/runner.py:297-395`).

This means closure has never been only a zero mechanism. A nonempty box-1
subtotal does not read closure, but Form 1040 line 2b still calls
`require_closed` for all ten interest families before consuming their subtotals
(`packages/content/tax/2025/rule.form1040-line2b.v4.json:91-102,165-206`).
Closure therefore supports workspace-record sufficiency for both empty-family
zero and a broader nonzero total. **It does not, on its own, supply
tax-model sufficiency for either** — closure only says the ten families the
rule already reads are complete on their own declared terms; whether those
ten families and their composition are themselves the right, coextensive
account of "total taxable interest" is a separate question the next section
addresses directly.

### What the current composition does and does not establish

`packages/content/tax/2025/interest-composition.v4.json` declares seven
positive families (box-1, box-3, 1099-OID box-1, non-form interest, Form
1065 K-1 box 5, box-10 market discount, 1099-OID box-5 market discount) as
`"required_universe": {"claim": "Seven declared positive taxable-interest
families forming the gross Schedule B Part I line-1 basis, without
subtractive adjustments."}` — the declaration's own text scopes the claim to
exactly these seven, not to "total taxable interest" at large.
`packages/content/tax/2025/rule.form1040-line2b.v4.json` then subtracts
three separately declared adjustment families (nominee, accrued interest,
ABP adjustment) and publishes `tax.us.2025.interest.taxable-total`, and
`packages/content/tax/2025/form1040.line-2b.form-field.v5.json` describes
exactly this seven-family/three-adjustment result.

ADR-0026 decision 7's honesty gate states plainly that the composition's own
claim "must not assert 'total taxable interest complete'" and that
additional positive families (e.g. Schedule K-1 interest, market discount
beyond what is already declared) and the general subtractive-adjustment
mechanism are explicitly out of that decision's scope, deferred to named
follow-on decisions. **This document does not infer that later additions to
the composition would prove complete current-law coverage, and does not
perform a new total-tax-coverage audit.** What the committed artifacts
establish is only what is stated above: ten families are consulted, their
own declared scope is honest about what it does and does not cover, and
whether that scope is coextensive with "total taxable interest" as a legal
concept is unproved by anything committed — not proved false, simply
unproved, and it is not this document's place to prove or disprove it.

### Execution and durable state

`execute_marshaled` accepts only a marshaller-minted context and returns
`RunResult` (`packages/derivation/production_executor.py:11-20`).
`execute_and_record_marshaled` writes start and completion process records around
the run. The records carry the workspace revision, governance and adoption pins,
and per-rule dispositions. Published dispositions carry finding, act, and symbol
ids; blocked dispositions carry codes and missing dependencies. The
`adopted_packages` set gates the adoption pin before the start record is written
but is not itself stored in the record (`packages/derivation/production_executor.py:23-69`;
`packages/derivation/records.py:188-248`;
`packages/schemas/derivation/derivation-record.v7.schema.json:3-178,286-341`).

The runner constructs derived findings and returns them in
`RunResult.publications` (`packages/derivation/runner.py:104-115,1289-1340`).
The separate `append_publications` function would write those values into the
workspace act log, but production execution does not call it; repository callers
are tests (`packages/derivation/runner.py:1372-1393`). `live_coordinate_run`
uses the returned publications to build presentation and output files without
appending them (`packages/derivation/live.py:213-247`). Therefore a current
run's calculated outputs are not automatically current workspace findings.

ADR-0007 Decision 1 requires each derived finding's entry into the record to
use a derived-publication act. ADR-0010 Decisions 1-2 require the workspace act
log to admit those envelopes and the projection to admit their derived
findings (`docs/adr/0007-derived-publication-act-kind.md:9-18`;
`docs/adr/0010-derived-finding-projection-and-currency.md:14-40`). Ordinary
derived-result publication remains governed by those decisions exactly as
ratified. That current production does not call `append_publications` is an
observed implementation fact, not a product decision this milestone selects
for preservation; whether and how to close that gap is a separate
implementation question, not something this completeness decision resolves.

Process records describe the run. They do not become derivation ingredients.
A later run must marshal its current workspace facts and adopted artifacts; it
must not use an earlier run record as an invented tax input.

### Presentation and explanation

There are two committed reader-entry paths for the box-1 subtotal:

1. `_resolve_field_row` resolves a published symbol selected by a form field.
   A repository-wide scan of `binds_symbol` under
   `packages/content/tax/2025/` finds no form field binding
   `tax.us.2025.interest.b1-subtotal`. Form 1040 line 2b instead binds the broader
   `tax.us.2025.interest.taxable-total`
   (`packages/content/tax/2025/form1040.line-2b.form-field.v5.json:1-5,31-46`).
2. `_resolve_attachment` resolves adopted attachment itemizations. Schedule B
   v4 Part I declares box 1 as a `row_sets[].subtotal_symbol`, so its source rows
   can appear as citation sites when Schedule B is required and published
   (`packages/content/tax/2025/rule.attachment.schedule-b.v4.json:115-131,217-234`;
   `packages/derivation/presentation_projection.py:349-400`).

For numeric form fields, `_classify_numeric` distinguishes source-backed values,
computed zero, and closure-backed zero. `_resolve_field_row` recursively walks
finding pins and keeps source leaves as citations while omitting closure leaves.
The attachment path uses direct row finding ids for its v6-shaped itemizations
and also filters any direct closure leaf
(`packages/derivation/presentation_projection.py:122-124,177-188,248-264,349-400`).
Readers can therefore see source rows on committed surfaces but not the exact
closure authority behind a closure-dependent total. The selected direction
requires the standing calculation authorization to survive into explanation
provenance; source citations alone are insufficient.

## Current capture behavior

The committed W-2 entry loop automatically creates closure when the first wage
fact is entered. It writes a `member-transition` and an `assertion` whose finding
has the W-2 closure `fact_id`, literal `true`, `basis: "documentary"`, an
`evidence_ids` entry, and `contribution_id`. The enclosing act supplies
`kind: "assertion"` and inherits the envelope's `actor`. Authoritative
ordering comes from the act's position in the append-only log;
`committed_against` participates in that revision sequencing, while `at` is
timestamp metadata only. Neither field turns the wage entry into a user
affirmation (`packages/derivation/entry_loop.py:65-78,770-807`).

Kernel finding validation checks the finding's value against its fact type,
rejects elective/determinable basis mismatches, and requires evidence for a
documentary basis. It does not impose the closure-specific attested-basis
requirement in ADR-0011/0017 (`packages/kernel/findings.py:524-558,582-590`).
Marshalling then omits basis and admission consumes the literal true. The system
therefore manufactures reusable closure from wage entry without asking. This is
committed behavior, not selected product meaning.

No equivalent committed 1099-INT closure-capture interface exists. The content
declares the fact, family, and mapping; no 1099-INT producer writes it. The gap
is not just a missing action-scoped control. It is that one live producer grants
workspace closure without authorization while the concrete 1099-INT family has
no capture path at all.

## Selected lifecycle

| State or event | Authorization state | Calculation consequence | What must be preserved |
| --- | --- | --- | --- |
| No standing authorization, no exhaustive-total request yet | Not established | Ordinary source entry and background calculation proceed unprompted; the authorization decision is not surfaced. | Nothing to preserve; no decision has been sought. |
| First exhaustive-total request with no standing authorization | Not established | The product surfaces the authorization decision now, not earlier. If declined, the product requests a narrower per-family confirmation only for the specific dependent result. | The absence of authority; no inference that the workspace is known incomplete. |
| No standing authorization, request declined or unmet | Not established | The dependent exhaustive-total result blocks. Unrelated facts and calculations, and a directly sourced value or recorded-items sum, remain available. | The absence of authority; no inference that the workspace is known incomplete. |
| Authorization adopted | Current within its declared scope | Ordinary return rules may treat current workspace facts as the complete input record (workspace-record sufficiency); tax-model sufficiency is a separate question the adopted rules' own coverage must independently answer. | Authorization identity and scope. |
| Relevant fact added | Still current | Recalculate from the new workspace revision; no repeated confirmation. | New current finding, superseded result history, unchanged authorization. |
| Relevant fact removed | Still current | Recalculate without the removed finding; the last removal may make zero applicable. | Removal/succession history and new revision. |
| Fact reclassified | Still current if within scope | Recalculate under current adopted rules. | Old and new membership/accounting provenance. |
| Same-fact value corrected | Still current | Recalculate from the corrected current finding. | Correction displacement and exact current input. |
| Authorization suspended or withdrawn | Not current for future ordinary calculation | Closure-dependent ordinary totals block for future runs until authority is restored, superseded, or a narrower per-family confirmation supplies it. Mechanically independent source-backed aggregates and unrelated calculations remain available but are not presented as the exhaustive ordinary return total. | Historical runs retain the authority they actually used; withdrawal asserts no incompleteness. |
| Authorization superseded | New scope controls | Future runs use only the successor authorization. | Both authorizations and the supersession relationship. |
| Calculation vocabulary materially expands beyond scope | Applicability unsettled until the scope rule is decided | Do not silently reuse the old authorization for the new universe. | Adopted package/version and the scope comparison. |

Unlike current per-family horizons, ordinary member changes do not expire the
selected authorization. Its invalidators are suspension, withdrawal,
supersession, or departure from its declared scope.

## Required run provenance

Every authorized run must retain enough information to answer:

- which standing authorization was in effect and its scope;
- which exact workspace revision was used;
- which current findings were consumed and which earlier findings were
  displaced;
- which adopted package, rules, mappings or successor artifacts, parameters,
  citations, and operation semantics were used;
- which results were calculated and which rules blocked or were inapplicable.

The existing run start/completion records and derived-finding pins supply much
of this topology, but the reader path currently suppresses closure authority and
there is no standing workspace-exhaustiveness authorization citizen. Those are
requirements for later contract work, not permission to invent a schema here.

## Narrow source-family confirmation (fallback, not deferred)

Per-family confirmation is not a deferred alternative. It is the adopted
fallback the product uses when the standing authorization is inactive and a
particular exhaustive claim still needs a basis. Because it concerns the
completeness of one family's current membership, adding, removing, or
reclassifying a member invalidates it; correcting an already-represented
member's value does not. Its technical representation — citizen shape,
keying, marshalling — is successor-contract work; its semantics are decided
and are not reopened here.

## Deferred alternatives and reopening triggers

The following analysis is retained only as a catalog:

- An **action-scoped affirmation** would separate truth content from one-run
  reuse. Reopen it only for a concrete case that requires one execution to rely
  on a true affirmation while forbidding later reuse.
- A **conditional assumption** would request a calculation that does not claim
  the assumed proposition as true. Reopen it only when users need intentional
  departure from current workspace state.
- A **provisional result status** would create two result standings. Reopen it
  only when those standings have materially different permitted uses.
- A **saved scenario or premise citizen** would preserve an editable alternative
  universe. Reopen it only for durable, comparable alternative workspaces.
- A **distinct negative-completeness value** would let the product record an
  affirmative "known incomplete" claim. Reopen it only for a concrete need
  beyond mere absence of authorization or confirmation.
- A **new persistence model for calculated results** would change how or
  whether a result is stored, projected, or reused. Reopen it only for a
  concrete need current production behavior does not already meet.

None is an implementation obligation. No schema, act kind, storage design,
identity, evaluator input, interface, or publication mechanism is selected for
them.

## Open scope question

A standing authorization must not silently grow to cover a materially different
calculation universe. The principal unresolved boundary is whether its identity
must include workspace, taxpayer or return subject, tax year, adopted package or
calculation vocabulary, and any other dimension that changes what “relevant
workspace information” means.

Ordinary additions, removals, reclassifications, and corrections do not cross
that boundary. A future package that introduces a new source category might.
The successor contract must define that distinction before implementation.

## Evidence map

| Layer | Artifact and fields read | Relevant sibling fields not relied upon | Downstream consumer and conclusion |
| --- | --- | --- | --- |
| W-2 capture | `entry_loop.py:65-78,770-807`: closure `fact_id`, `value`, `basis`, `evidence_ids`, `contribution_id`; act `kind`, `actor`, `at`, `committed_against`, `payload` | Wage formatting and comparison-line constants do not establish affirmation | Kernel admission, currency, closure marshalling: a wage-entry action currently creates reusable documentary closure without asking. |
| Closure content | `closure-mapping.f1099int-b1.json:2-10`: schema, family, member/closure fact types, horizon key, admitted symbol, condition; `family.f1099int-b1.json:2-9`: claim, member predicate, subtotal; bundle closure fact `f1099int.bundle.json:23-35` | Titles do not determine runtime admission; the member amount fact's value schema does not define closure | Package validation, marshalling, `resolve_closure_admissions`, evaluator: committed authority is narrow per-family literal true. |
| Currency/marshalling | `marshal.py:158-205`: current finding ids, `fact_id`, `value`, mapping closure type/horizon key, current horizon chains | Finding `basis`, `evidence_ids`, `capture`, `pins`, `contribution_id` are not copied into `ClosureFindingRecord` | `resolve_closure_admissions`: current record truth survives, but basis/authorship detail is lost at this projection. |
| Admission | `source_authority.py:65-97,100-166`: mapping/declaration ids and versions, current horizon, closure finding id/type/horizon/value | No actor, basis, evidence, contribution, or capture fields exist in the admission record | `_Run.__init__` and `env.closed_sets`: only one current literal true admits a family. |
| Evaluation | `evaluator.py:118-141,206-211`: `sources`, `closed_sets`, expression `name`/`source_set` | Findings, acts, mappings, and horizons are not direct evaluator inputs | `runner.pins_for`: empty collect, count, and require_closed have distinct closure dependencies. |
| Line 2b content | `rule.form1040-line2b.v4.json:91-102,111-206`: ten subtotal refs, ten `require_closed` source sets, rule identity/version, composition | Notes do not create the dependency; blocked display text does not alter evaluation | Evaluator and runner: even a nonzero line 2b requires all ten current family admissions — workspace-record sufficiency for those ten, not a coverage claim about the ten themselves. |
| Composition scope | `interest-composition.v4.json`: seven `constituents`, `required_universe.claim` text scoping the claim to those seven; `quantity.taxable-interest.json`: quantity vocabulary listing `taxable-interest`; ADR-0026 decision 7 honesty-gate text | The composition schema's `coextensiveness: "slot-bijection"` governs the rule's constituent set against the composition's own declared slots, not against "total taxable interest" at large | Package validation, rule authoring: the declared composition proves its own seven-family coverage is honestly scoped; it does not prove, and its own text disclaims, that this is complete taxable-interest coverage. |
| Run boundary | `production_executor.py:23-69`, `records.py:188-248`, and `derivation-record.v7.schema.json:3-178,286-341`: workspace revision, governance/adoption pins, run id, and per-rule published/blocked/inapplicable dispositions; `adopted_packages` is checked but not stored | Start/completion record ids identify records but are not tax inputs; versioned records do not duplicate legacy top-level `published`/`blocked` lists | Record stream and caller: production records execution and returns calculated publications without calling `append_publications`, an observed implementation fact governed by ADR-0007 Decision 1 and ADR-0010 Decisions 1-2, not a preservation this milestone selects. |
| Internal provenance | `runner.py:297-395,1289-1340`: rule, source, ref, parameter/table, closure, operation, citation pins; result publications/dispositions | Symbol cache and evaluation order do not enlarge claim scope | Derived finding and run result: exact dependencies can be retained internally. |
| Reader projection | `presentation_projection.py:122-124,177-188,248-264,349-400`: finding value/pins, source and closure classification, form binding, attachment rows | Finding basis is used only for optional evidence labeling; closure ids are not reader citations | Presentation model and renderer: sources can be visible while the authority licensing the total is hidden. |
