# Review Round 1 — Governance Fidelity

Reviewer: Codex resume session, 2026-07-10.

Seat: governance fidelity.

Artifacts reviewed:
- `docs/governance/` v0.1, including `records/2026-07-09-closure-check-v0.1.md`
- `docs/prototypes/rule-language/charter-it1.md` v2
- `docs/prototypes/rule-language/reviews/round-1.md`
- `docs/prototypes/rule-language/examination-it1.md`
- branch `prototypes/rule-language/it1` at the round-stated tip `362f8a3`, especially `prototype-rule-language-it1/artifacts/federal-1040-core-2025.package.json`, `schemas/`, and `machinery/evaluator.py`

I did not read any other Round 1 review output before writing this review.

## Check 1 — Article 11 Legibility

Check: for each artifact kind, is the complete rule meaning recoverable from the artifact without reading evaluator code? Name any meaning that lives only in the evaluator.

Result: partial pass with governance findings. The artifact instances carry the visible tax rule content for every represented artifact kind, but the complete semantics are not recoverable from artifact plus schema alone because several decisive meanings live in evaluator conventions.

Exhibits:
- Rule artifacts: `prototypes/rule-language/it1:prototype-rule-language-it1/artifacts/federal-1040-core-2025.package.json`.
- Rule schema: `prototypes/rule-language/it1:prototype-rule-language-it1/schemas/rule-artifact.v1.prototype-it1.schema.json`.
- Evaluator: `prototypes/rule-language/it1:prototype-rule-language-it1/machinery/evaluator.py`.

Measurements:
- `field_mapping`, `cross_form_bridge`, `derivation_rule`, and `applicability_rule` artifacts all expose inputs, labels, source citations, expressions, outputs, scope, and dependencies in the corpus. Examples include W-2 wages to Form 1040 line 1a, Schedule B line 4 to Form 1040 line 2b, Form 1040 line 16 regular tax, and Schedule B applicability.
- The expression grammar is not declared as a grammar in the schema. The schema permits `expression` as object/string/number/boolean/null/array without enumerating operation forms or their required members. The meaning of `sum`, `lookup`, `table_row`, `let_row`, `round_money`, `publish_when`, and applicability suppression is recoverable only by reading evaluator branches.
- The false-applicability rule is evaluator meaning: `if rule["artifact_kind"] == "applicability_rule" and value is not True: return [], []`. The artifact declares an applicability expression and output, but not the record semantics for a false condition.
- `publish_when` is artifact-visible but its publish-suppression semantics live in evaluator code.
- Optional many-input missing facts become an empty list, and ordinary missing single optional facts become `Decimal("0")` in evaluator binding. That zero/empty behavior is not schema-declared as a rule-language semantic.
- Whole-dollar rounding declares stage and mode in artifacts, but the tie-breaking rule comes from evaluator code (`ROUND_HALF_UP`), not from a parameter, rule artifact, or schema-declared rounding convention.

Finding: Article 11's "obtuse is permitted; hidden is not" is not fully satisfied by it1. The prototype demonstrates an expressive artifact surface, but the operation vocabulary and several publication/blocking semantics are still sealed in evaluator code.

## Check 2 — Article 11 Purity

Check: do artifacts declare all inputs? Name any implicit input: clock, environment, ordering assumption, ambient constant.

Result: pass for forbidden external impurity; partial fail for ambient constants and implicit operation semantics.

Exhibits:
- `machinery/evaluator.py`
- `artifacts/federal-1040-core-2025.package.json`
- `schemas/derived-publication-act.v1.prototype-it1.schema.json`
- `schemas/derivation-record.v1.prototype-it1.schema.json`

Measurements:
- I found no rule-evaluation dependency on clock, network, environment variables, filesystem state beyond loading the fixed prototype corpus/fixtures, or randomness. The shuffled-order verification uses `random.Random(17)` outside rule meaning.
- Artifact order is not operative tax meaning: the evaluator saturates until no progress, and the examination reports shuffled-artifact equality.
- The package id used inside `run_start_record_id` is hardcoded in evaluator code as `pkg.2025.us-federal.1040-core.v1`, rather than taken from the loaded package instance. This is not tax law meaning, but it is process-record content that should be declared from inputs.
- Governance versions are hardcoded in the evaluator's derivation record construction. The record shape requires `governance_versions`, but the values are ambient code constants rather than explicit run inputs.
- The rounding mode value `whole_dollars_post_total` and the tie-breaking behavior behind it are not declared by a parameter or choice schema. The choice fact supplies the string; code gives the string its operational meaning.

Finding: The prototype is pure in the ordinary execution-sandbox sense, but a ratifiable language needs the operation vocabulary, rounding semantics, package identity, and governance-version inputs declared rather than carried by evaluator constants.

## Check 3 — Ontology §5 Conformance

Check: inputs, conditions, operation, results, applicability, thresholds, mappings, dependencies declared? Name each missing or smuggled item.

Result: partial pass. The corpus declares most required categories, but some categories are underspecified or smuggled through schema laxity/evaluator behavior.

Exhibits:
- `artifacts/federal-1040-core-2025.package.json`
- `schemas/rule-artifact.v1.prototype-it1.schema.json`
- `schemas/parameter-declaration.v1.prototype-it1.schema.json`
- `schemas/derivation-record.v1.prototype-it1.schema.json`
- `machinery/evaluator.py`

Measurements:
- Declared: inputs and roles (`input`, `condition`, `choice`, `parameter`, `bridge`); outputs; source citations; scope; field mappings; cross-form bridges; artifact dependencies; thresholds inside parameters; F7 table and worksheet rows; F8 conditional publication; F13 rounding stage.
- Missing or smuggled: the expression operation vocabulary and its type rules; false-applicability semantics; `publish_when` publication semantics; empty-list/zero behavior for optional inputs; rounding tie-breaking; parameter value shapes; and item shapes for `published`, `blocked`, `artifact_versions`, and `parameter_versions` in the derivation-record schema.
- The prototype references fact types and form fields by string id, not by drafted fact-type or form-field citizens. The examination discloses this as negative evidence. For it1 design evidence this is acceptable, but as a governance measurement it means the rule artifacts do not yet stand on a fully declared vocabulary for their consumed and produced facts.

Finding: Ontology §5 is directionally satisfied by the artifact corpus, but not by the schema family. The proposed language still depends on runner knowledge for what expressions mean and on conventional string IDs for several citizens that later surfaces will need as declared schemas.

## Check 4 — E11.3 No Orchestrated Traversal

Check: does form order, traversal, or cross-form bridging live anywhere but artifacts?

Result: pass with one prototype-only caveat.

Exhibits:
- `artifacts/federal-1040-core-2025.package.json`
- `machinery/evaluator.py`
- grep result: evaluator form-specific hits are limited to fixed prototype file/package ids, the F13 diagnostic target, and the negative validation example references in schema files.

Measurements:
- Cross-form bridges are represented as artifacts: Schedule B line 4 to Form 1040 line 2b and Schedule 1 line 26 to Form 1040 line 10 both use `artifact_kind: "cross_form_bridge"` with bridge/input dependencies in the artifact corpus.
- The evaluator does not encode a form order. It iterates rules to saturation and relies on known/published fact ids and declared inputs.
- The evaluator contains no scheduler branches for Form 1040, Schedule B, Schedule 1, line 16, or line 2b. The form-specific strings found in evaluator code are the fixed prototype package id and F13 diagnostic target used for the wrong-stage comparison.
- Caveat: the F13 wrong-stage comparison deliberately targets `rule.2025.w2.box1.to.f1040.line1a.v1` in code. That is verification machinery rather than derivation behavior, but a production conformance test should move this kind of targeted mutation into a declared test fixture or harness metadata.

Finding: it1 succeeds on the E11.3 traversal question for derivation behavior. Cross-form behavior lives in artifacts, not scheduler code.

## Check 5 — Article 9/10 Canon and Declaration

Check: are artifacts schema-versioned citizens with declared shape? Is any meaning carried by convention?

Result: partial pass. Every proposed citizen, act, and record shape names a schema version, but important meaning is carried by convention because schemas are loose.

Exhibits:
- `schemas/rule-artifact.v1.prototype-it1.schema.json`
- `schemas/parameter-declaration.v1.prototype-it1.schema.json`
- `schemas/artifact-package.v1.prototype-it1.schema.json`
- `schemas/derived-publication-act.v1.prototype-it1.schema.json`
- `schemas/derivation-record.v1.prototype-it1.schema.json`
- `schemas/negative-label-id-mismatch.example.json`

Measurements:
- Pass: package, parameters, rules, derived-publication act, and derivation record all have `schema_version` constants and `citizen_kind` declarations.
- Pass: the negative validation example proves the schema can reject one bespoke label/id mismatch for "Form 1040 line 2b".
- Fail: label/id coherence is not generally declared. The one negative example is encoded as a special-case `if label pattern then output fact id contains ...` rule, not as a general form-field or fact-type declaration system.
- Fail: `expression` is effectively untyped at the schema layer. A malformed or misleading operation object can pass schema validation and fail or behave unexpectedly only at evaluator time.
- Fail: parameter `values` is unconstrained, so table schemas, bracket rows, standard deduction keys, threshold types, and null upper bounds are private conventions between artifacts and evaluator.
- Fail: derivation record arrays have no item schemas, and the derived-publication act schema does not require `run_start_record_id` even though the examination presents the start/completion split as a design result.

Finding: the it1 artifacts are schema-versioned, but the schemas do not yet declare enough shape to be Article 9/10-grade contracts. The next design step needs either stricter schemas or declared subordinate artifact kinds for expressions, parameters, fields, facts, and records.

## Check 6 — Reserved-Entry Safety

Check: does the design improvise T1 (derived-finding authority) or T2 (stance) doctrine?

Result: pass.

Exhibits:
- `artifacts/federal-1040-core-2025.package.json`
- `schemas/derived-publication-act.v1.prototype-it1.schema.json`
- `schemas/derivation-record.v1.prototype-it1.schema.json`
- `docs/prototypes/rule-language/examination-it1.md`, Q9

Measurements:
- The prototype uses `derived_publication` as an act kind distinct from `assertion`, pins input findings/artifacts/parameters/workspace revision/adoption act, and records `actor_id`. This stays within the existing instrument framing for derived findings.
- The examination explicitly limits Q9 to publication vocabulary and record timing and says it does not resolve reserved T1 authority beyond the existing instrument framing.
- I found no stance/position artifact or filed-return position modeling in it1.

Finding: no reserved T1 or T2 doctrine is improvised in this iteration. The publication-act vocabulary is a design proposal that still needs ADR treatment, but the prototype does not claim legal or ontological closure beyond the allowed guardrail.

## Observations

The primary design's strongest governance result is E11.3: it shows that cross-form bridges and worksheet logic can be moved into artifacts without a form-order scheduler. The weakest result is schema declaration: the artifacts are legible examples, while the schemas are closer to permissive envelopes than contracts.

For a rival design, I would measure whether it can make expression semantics, parameter shapes, record items, and form-field identity recoverable from declared artifacts without making the artifacts unreadable. That is the real tradeoff exposed by it1.

## Dissent

No dissent from continuing the process to a rival design. I dissent from treating it1, as-is, as ratifiable Article 11 machinery language: too much operation and record meaning still lives in evaluator convention rather than declared artifacts.
