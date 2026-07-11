# Round 1 - Legibility Review

## Review posture

This is a fresh-reader review of the six schemas, six positive examples, and
the synthetic scenario listed by the round file. I describe only meanings that
the listed files make recoverable. Where an identifier points outside that
set, its meaning is recorded as an import rather than supplied from tax
knowledge.

## Form field schema

**Concept:** A first-class tax form field with a printed locator, a logical
symbol, a role, a value domain, citations, and explicit rendered-absence
states. The schema description makes this certain.

**Identity:** The apparent identity is `id`, with `form`, `tax_year`,
`jurisdiction`, and `printed_locator` providing the printed scope and
`logical_symbol` providing the logical binding. This is probable: the schema
requires all of these, but does not declare an identity policy.

**Lifecycle/versioning:** The citizen is fixed at schema `form-field.v1` and
`version: v1`. `generated_by` can retain generator and source-citation
provenance, but is optional. No correction, supersession, or migration rule is
carried by this schema. Certain for the fixed version; guessing for any
lifecycle beyond that.

**Renderer/rule effect:** The five named absence cases select one of
`zero`, `blank`, `blocked`, or `not-applicable`; each also states whether a
finding is published, which explanation terminal applies, and a human-readable
note. This is certain as a render contract. It is probable that a renderer
chooses the state from runtime derivation/validation conditions, because the
schema does not define that state-selection algorithm.

**Legibility gap:** `included_line_family`, `role`, and
`explanation_terminal` are constrained vocabulary but not defined in the
schema. The connection between `logical_symbol` and an operative rule is also
imported. The schema does not itself verify that citation IDs, generated source
IDs, or logical symbols resolve consistently.

## Source field schema

**Concept:** Declared meaning for a source-form box or field, explicitly not a
fact child of a submitted document. Certain from the description and required
fields.

**Identity:** `id`, `source_family`, `tax_year`, `document_revision`, and
`field_key` appear to identify the declared source field; `printed_label` and
`federal_meaning` describe it. This is probable because no explicit identity
policy is present.

**Lifecycle/versioning:** The declaration is `source-field.v1` / `v1` and
contains a free-text `document_revision`. There is no explicit corrected-form,
supersession, or migration mechanism. Certain for the version; guessing for
how a later revision relates to this citizen.

**Renderer/rule effect:** `may_feed_symbols` declares permitted destinations,
`excluded_from_symbols` declares exclusions, and
`requires_declared_rule: true` says a source value cannot bridge by an
undeclared rule. It does not itself compute or render a value. Certain for the
declared bridge posture; probable that a validator or rule loader enforces it.

**Legibility gap:** The schema does not carry a rule ID, source-instance
linkage, correction relationship, aggregation/cardinality rule, or the meaning
of the `federal_meaning` vocabulary. The phrase “requires declared rule” is
therefore legible as a gate but not as a recoverable procedure.

## Tax fact type schema

**Concept:** A tax-domain companion for an external kernel fact type. It
declares tax meaning, fact role/nature, identity keys, value/basis policy,
source-set closure behavior, form-field references, and citations. Certain from
the description and field names.

**Identity:** `id`, `kernel_fact_type_id`, `tax_year`, `jurisdiction`,
`family`, and `symbol` are the visible scope and binding identifiers. The
`identity_policy.keys` list says which named parts participate and explicitly
sets `source_document_identity` to false for each key in the example. The
schema does not define how those keys establish uniqueness or peerage, so the
operational identity is only probable.

**Lifecycle/versioning:** The companion is `tax-fact-type.v1` / `v1`; tax year
and jurisdiction scope the declaration. No supersession or correction behavior
is defined. Certain for version and scope; guessing for replacement behavior.

**Renderer/rule effect:** For a source set, the declaration supplies a closure
symbol, an empty closed value, and separate unclosed/invalid block codes. It
also names form fields and limits allowed bases. This appears to tell a rule
when a value may be closed, published, or blocked. That effect is probable,
not certain, because the operative kernel fact contract and rule are imported.

**Legibility gap:** `value_domain` is only an unconstrained object here, and
`empty_closed_value` has no type constraint. The meanings of `role`,
`fact_nature`, `basis_allowed`, `peerage_note`, and the external kernel fact
type are not carried. The schema also limits the source-set vocabulary but does
not explain how multiple source findings aggregate.

## Tax fact type example: W-2 box 1 wages

**Concept:** A determinable, money-valued source fact for the symbol
`tax.2025.w2.box1`, connected to a Form 1040 line 1a field and supported by
documentary or attested basis. Certain as a reading of the literal fields;
the external tax meaning of “W-2 box 1” is not independently supplied here.

**Identity:** The example explicitly names taxpayer, employer,
employment-engagement, tax-year, and declared source-field keys, while
excluding source-document identity. Its note says a W-2 corroborates rather
than identifies the fact. Certain as declared; whether this produces the
intended peer grouping is probable because the equality/uniqueness operation is
not specified.

**Lifecycle/versioning:** It is `v1`, scoped to tax year 2025, and its
`source_document_identity: false` policy suggests replacement evidence should
not create a new fact identity. The latter is probable, not certain, because
correction behavior is not represented in this example.

**Renderer/rule effect:** The example names `irs.form1040.2025.line1a` as a
form binding and permits documentary/attested bases. It does not state the
aggregation or derivation that a renderer/rule must perform. Any such behavior
is imported through `kernel_fact_type_id` and the referenced rule/content.

**Legibility gap:** `tax.fact-type.w2.box1-wages`, the W-2 citation, and the
form-field citation are references; only the line 1a citation example is in
the allowed reading set. The kernel fact type itself is unavailable, so the
question contract is not recoverable from this example alone.

## Official source citation schema

**Concept:** A non-operative citation to official tax source material used for
adoption, review, and explanation. `operative_effect: false` makes the
non-operative boundary certain.

**Identity:** `id` and `version` are the explicit identifiers. Issuer, source
type, title, URL, document revision, tax-year applicability, and locator
describe the cited material. No identity policy says whether a changed locator
or revision is a new citation, so that lifecycle interpretation is probable at
most.

**Lifecycle/versioning:** The citation has `v1`; `document_revision` and
`tax_year_applicability.status` distinguish final, draft, and evolution-probe
material. The schema does not define supersession or whether a citation can be
reused across packages. Certain for the available status vocabulary; guessing
for transitions.

**Renderer/rule effect:** Citation text, URL, and locator are expressly not
operative and therefore should not change evaluation output. They can support
review or explanation if a consumer chooses to display them. Certain for
evaluation non-effect; display behavior is probable because the schema does
not prescribe a citation renderer.

**Legibility gap:** The citation carries a title and text anchor, not the
underlying source text or the proposition being supported. Meaning still has to
be recovered from the locator and external official document. URI/date format
checking also depends on the schema validator rather than this file's prose.

## Citation example: 2025 Form 1040 line 1a

**Concept:** A final IRS Form 1040 citation for 2025, page 1, Income, line 1a,
anchored by the text “Total amount from Form(s) W-2, box 1.” Certain from the
example.

**Identity/lifecycle:** It is `irs.2025.form1040.line1a`, `v1`, with a stated
2025 final applicability and a concrete PDF revision. `checked_at` records a
check date. It is probable that changing the PDF revision or locator would
create a changed citation declaration; no supersession rule is present.

**Renderer/rule effect:** `operative_effect: false` means this citation must
not alter rule evaluation. It may provide an explanation anchor. Certain for
non-operation; the rule that consumes it is not in the allowed files.

**Legibility gap:** The URL and locator identify material but do not carry the
full legal or tax proposition. The citation IDs used by the other listed
artifacts for Form 1040 line 2b and 1099-INT box 1 are not defined by this
listed example, so their content cannot be inferred from this one.

## Rule content binding schema

**Concept:** Companion content that associates an existing rule artifact with
tax meaning: a published symbol, tax fact type, form field, source fields, and
citations. The schema description makes this certain.

**Identity:** The binding has its own `id` / `version`; the operative-looking
reference is `rule_artifact_id` plus `rule_artifact_version`, scoped by tax
year, jurisdiction, and family. The referenced symbols and IDs identify the
members of the binding. Certain for the visible references; how identity is
deduplicated is not stated.

**Lifecycle/versioning:** The binding is `v1` and points to a separately
versioned rule artifact. This makes rule-artifact versioning recoverable, but
does not say how a binding is superseded when the source/form/citation changes.
Certain for the two version fields; guessing for cascade behavior.

**Renderer/rule effect:** The binding appears to make tax content available to
an existing rule while leaving computation to that rule artifact. The citation
parity object asserts that mutating citation text leaves the output hash
unchanged. That non-effect is probable as an assertion to be checked, but the
schema does not define the hash inputs, verification process, or enforcement of
cross-reference consistency.

**Legibility gap:** The rule artifact itself is not listed, so no formula,
closure gate, source aggregation, or output semantics are recoverable. The
schema does not say whether the binding is independently operative, even though
it contains tax meaning.

## Rule content binding example: 1099-INT box 1 to Form 1040 line 2b

**Concept:** A 2025 US-federal individual-income-tax binding that publishes
`tax.2025.form1040.line2b` from the named tax fact, form field, and 1099-INT
source field. Certain as the declared graph of references.

**Identity/lifecycle:** The binding ID is descriptive and versioned `v1`; the
rule artifact is separately identified as `tax.2025.rule.1099int-box1-to-form1040-line2b`
`v1`, within an explicit 2025 package scope. Certain for those declarations.

**Renderer/rule effect:** The equal before/after output hashes and
`citation_text_affects_evaluation: false` declare that citation text mutation
does not change the rule output. The actual line 2b computation or the
conditions under which it publishes are not present. Any claim about closure,
zero, or blocking comes from the scenario rather than this binding itself.

**Legibility gap:** The referenced tax fact type is for Form 1040 line 2b but
the only listed tax-fact example is W-2 box 1; its definition is absent. Both
citation IDs in this binding are also absent from the listed citation examples.
The reader therefore cannot independently recover the tax meaning or verify
the reference graph from the permitted artifacts.

## Coverage report schema

**Concept:** A recomputable, non-authoritative read model reporting source-set
closure gaps. Certain from the description, `authoritative_state: false`, and
the required rebuild hashes.

**Identity/lifecycle:** `id` plus `workspace_revision` identify a projection
instance, while `act_log_hash` and `derivation_record_hash` identify the inputs
from which it was rebuilt. This is probable as projection identity because no
explicit identity policy or timestamp is present.

**Renderer/rule effect:** A consumer can display each source set as closed or
open, show a closure finding when present, and show a gap code when present.
The stale policy says an unbacked closed projection is rejected with
`STALE_PROJECTION_REJECTED`. Certain for report/rejection semantics; whether
the report itself blocks a tax rule is not declared.

**Legibility gap:** The report says which source sets are open but does not
carry the rule that consumes that state. `closure_finding_id` and `gap_code`
are nullable independently, so their valid combinations are not fully
constrained by this schema.

## Coverage report example: open interest

**Concept:** At workspace revision 18, the W-2 source set is closed and the
1099-INT source set is open with gap `SOURCE_SET_UNCLOSED`; the projection is
not authoritative and must reject an unbacked closed state. Certain from the
example.

**Identity/lifecycle:** `coverage.demo.revision-18` and the two input hashes
identify this report instance and its rebuild inputs. Rebuilding from the same
inputs is implied by the hashes, but immutability or retention behavior is not
specified.

**Renderer/rule effect:** A report renderer should show W-2 closed, 1099-INT
open, and the open gap. It should reject a stale injected closed projection.
It is probable, not certain, that a separate interest rule uses the open state
to block publication; that relationship is shown elsewhere only in the listed
scenario.

## Synthetic scenario

**Concept:** A synthetic end-to-end slice showing entities, source instances,
source findings, closure findings, derived findings, rendered-absence states,
mutation probes, coverage rebuild behavior, and an evolution probe. The
synthetic provenance declaration is certain; the scenario's outputs are
declarations of expected behavior, not executable rule definitions.

**Identity:** Entity, evidence, finding, fact, derived-result, act, rule, and
citation IDs are all explicit. The W-2 fact identity visibly includes taxpayer,
employer, engagement, and year; the evidence IDs distinguish original and
reissued evidence. Certain as the scenario's identifiers. The identity and
peerage behavior is probable only where the scenario records a mutation result,
because the underlying identity algorithm is not listed.

**Lifecycle/versioning:** Evidence replacement and removal are modeled as
mutations; corrected W-2 input displaces downstream derived findings. Coverage
is deleted and rebuilt, and later-year content uses a new citizen while the old
ID persists. These are clear scenario claims. The scenario itself has no
`version` property beyond its schema-like `schema` string, so its own
evolution lifecycle is guessing.

**Renderer/rule effect:** The scenario declares 42,000 wages on line 1a, 320
interest on line 2b, subsequent derived line values, and four interest
absence/invalidity outcomes. It also declares that line 11b is the valid 2025
AGI destination in this slice and that a guarded qualified-dividend-tax display
is not applicable. The values and state transitions are certain as scenario
claims; their causal rule semantics are probable because the rules and kernel
contracts are not listed.

**Legibility gaps and imported knowledge:**

- The scenario references `../source-catalog.json`, rule artifacts, act
  records, derivation records, citations, and findings that are not in the
  permitted reading set. Their content cannot be independently checked.
- The only listed source-field example is 1099-INT box 1, while the scenario
  also uses 1099-INT boxes 2 and 8. Their declared meanings are therefore
  imported.
- The only listed tax-fact example is W-2 box 1, while the interest binding
  names a different tax fact type. The closure behavior for that interest fact
  is asserted by the scenario but not recoverable from a listed tax-fact
  example.
- Several citation IDs used in the scenario and binding have no listed
  citation artifact. The reader can see that citations are intended as pins,
  but cannot recover their source propositions.
- The line 11b choice is stated in `candidate_contract` and the derivation
  list, but no listed form-field or citation artifact defines line 11b. The
  choice is therefore a probable scenario assertion, not a self-contained
  declaration.

## Fresh-reader conclusion

The artifact family is legible at the boundary level: each document states
whether it is a form field, source-field meaning, tax-fact companion, citation,
rule binding, or non-authoritative coverage projection; IDs, tax-year scope,
and most version markers are visible. The rendered-absence states and the
non-operative citation boundary are especially recoverable.

The candidate is not fully recoverable from the listed artifacts alone. The
largest issue is that the examples do not form a closed explanatory slice:
the interest rule binding lacks its tax-fact and citation definitions, while
the only tax-fact example is for W-2 wages. A fresh reader can follow the
intended references and the scenario's claimed results, but must import the
kernel contract, rule behavior, source catalog, and several official citation
meanings to know what a renderer or rule actually does.
