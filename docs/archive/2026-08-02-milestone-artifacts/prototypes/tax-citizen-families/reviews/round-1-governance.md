# Round 1 Governance Review - Iteration 1

Reviewer: codex-governance-r1-2026-07-11
Scope: `prototypes/tax-citizen-families/it1` at commit `88f0139`
Role: governance fidelity only

## Measurements

Check: Article 1 / E1.1 peerage - fact identity must not be a document child -> Result: pass -> Exhibit: `it1/schemas/tax-fact-type.v1.schema.json` requires every identity key to carry `source_document_identity: false`; `it1/examples/positive/tax-fact-type.w2-box1.json` keys W-2 wage identity by taxpayer, employer, employment engagement, tax year, and declared source field; `it1/examples/negative/tax-fact-type.document-child-identity.json` is rejected for document-child identity; `it1/scenarios/synthetic-slice.json` records evidence replacement and removal mutations where finding ids and values remain stable while evidentiary standing changes.

Check: Articles 9/10 / E9.1 / E10.1 canon and declaration - schemas must exist before instances, undeclared shapes must reject, and malformed instances must not be repaired -> Result: pass -> Exhibit: `it1/schemas/` declares six new citizen families before examples instantiate them; each positive example names a declared `schema`; `it1/examples/negative/undeclared-schema-version.json` names `form-field.v2` and rejects; `it1/validators/validate_it1.py` dispatches only to declared schemas and reports undeclared schemas instead of coercing; validator run from commit `88f0139` returned `OK: positives validate, negatives fail for declared reasons, scenario checks pass`.

Check: Article 11 / E11.2 / E11.3 legibility - tax meaning, applicability, mappings, rendered absence, bridges, and citations must be declared content rather than runner convention -> Result: pass for the prototype contract shape -> Exhibit: `it1/schemas/source-field.v1.schema.json` declares source-box federal meaning and allowed/excluded bridge symbols; `it1/schemas/form-field.v1.schema.json` declares printed locator, logical symbol, citation ids, and rendered-absence states; `it1/schemas/rule-content-binding.v1.schema.json` binds a rule output to tax fact type, form field, source fields, citations, and citation parity; `it1/examples/negative/source-field.box2-misbridged-to-line2b.json` rejects hidden collapse of 1099-INT box 2 into line 2b; `it1/scenarios/synthetic-slice.json` gives explanation walks for absence, invalidity, and guard inapplicability states.

Check: Article 11 citation placement and non-operative source citations - official sources must support adoption/explanation without becoming hidden runner input or output-affecting behavior -> Result: pass -> Exhibit: `it1/schemas/official-source-citation.v1.schema.json` declares issuer, URL, revision, tax-year applicability, checked date, precise locator, and `operative_effect: false`; `it1/examples/negative/citation.missing-locator.json` rejects a citation lacking locator content; `it1/examples/negative/rule-content-binding.citation-operative.json` rejects citation text affecting evaluation; `it1/scenarios/synthetic-slice.json` records locator and tax-year citation mutations rejected while evaluation output hashes remain unchanged.

Check: Article 14 / E14.2 coverage and record boundary - coverage/gap state must not become authoritative form state or a second store -> Result: pass -> Exhibit: `it1/schemas/coverage-report.v1.schema.json` requires `authoritative_state: false`, rebuild provenance, and `accepts_unbacked_closed_projection: false`; `it1/examples/negative/coverage-report.authoritative-state.json` rejects authoritative coverage state and unbacked closure; `it1/scenarios/synthetic-slice.json` records delete/rebuild byte equality and rejection of a stale closed projection with no closure finding.

Check: Article 15 / E15.1 explanation - absence, invalidity, blocked, and guard states must terminate at declared content or records, not renderer convention or code -> Result: pass -> Exhibit: `it1/examples/positive/form-field.form1040.line2b.json` declares terminals for computed zero, closure-backed zero, block records, validation result, and artifact guard; `it1/scenarios/synthetic-slice.json` includes explanation walks for the four absence/invalidity matrix states and rendered-absence terminals including the line 16 alternate-rule guard disposition.

Check: Articles 7/12/13 supersession and derivation edges - corrected source findings must displace downstream derived findings through declared/recoverable edges rather than edits -> Result: pass for the prototype evidence -> Exhibit: `it1/scenarios/synthetic-slice.json` records `mutations.supersession_cascade` from corrected W-2 box 1 to lines 1a, 9, 11b, 15, and 16, with an explicit edge path and displaced derived-finding ids.

Check: Article 18 / E18.3 synthetic-data posture - committed prototype fixtures must be synthetic and publishable -> Result: pass -> Exhibit: `it1/scenarios/synthetic-slice.json` marks tax values synthetic and uses demo entity ids/labels; `it1/source-catalog.json` states taxpayer, employer, payer, and amount values are synthetic and contains official IRS URLs rather than local personal paths; validator checks scenario provenance and scans source catalog text for forbidden local path markers.

Check: reserved-entry safety - prototype must not build on T1 derived-finding authority construction, T2 stance/position doctrine, redaction, or multi-party authority -> Result: pass -> Exhibit: the candidate uses the already-recorded instrument/adoption framing for derived findings but does not define the reserved T1 authority construction; no artifact introduces `stance`, `position`, redaction semantics, or multi-party actor authority; `charter-it1.md` lists stance/position doctrine and redaction out of scope.

Check: ADR-0005 evidence sufficiency for a contract-foundational Tier 2 decision -> Result: pass as iteration evidence, not final ratification evidence -> Exhibit: `charter-it1.md` declares fixtures F1-F12 and questions Q1-Q10; `it1/` supplies schemas, positive and negative examples, scenario mutations, and a validator; `examination-it1.md` answers Q1-Q10 and correctly states the decision remains Tier 2 and needs committee review and rival-design comparison before ADR ratification.

## Observations

- The prototype's governance fidelity is strongest where it turns each governance risk into a rejecting example: document-child identity, undeclared schema version, missing citation locator, operative citation parity, stale coverage, and 1099-INT box misuse.
- The Article 11 pass is scoped to candidate contract shape. The prototype does not prove a production runner or full rule-artifact language; it shows that the new citizen families can carry the tax meaning required by the charter without relying on renderer or scheduler convention.
- The line 11/11b negative result is governance-relevant because it demonstrates that printed form identity is not treated as a loose string when official source content disagrees.

## Dissent

No dissent from the builder's governance claims for iteration 1. I would not treat this as sufficient for final ADR ratification until the required rival design and committee disposition exist, per ADR-0005.

## Verification

- Read required role, round, charter, examination, and full governance set.
- Inspected `it1/` artifacts at commit `88f0139` without reading same-round peer outputs or commit-message bodies.
- Ran the it1 validator from a temporary archive of commit `88f0139`: `OK: positives validate, negatives fail for declared reasons, scenario checks pass`.
- `git diff --check -- docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/reviews/round-1-governance.md` passed with no output.
