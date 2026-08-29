# Clean-room review R1: Ordinary Input Mapping (Seam 6)

Reviewer read only the charter, examination.md (treated as a claim, not a
trusted account), and the artifact
(`packages/tax/obligation_acquisition_mapping.py`,
`tests/test_obligation_acquisition_translation.py`), then independently
traced `packages/kernel/contribution.py` / `packages/kernel/findings.py`
and ran the test suite. No commit messages or prior review notes were read.

## Independent test run

`python3 -m pytest tests/test_obligation_acquisition_translation.py -v`:
**14 passed** (confirmed directly, not taken from examination.md).

## Charter requirement verdicts

### 1. Subject and scope agree — MET

The module docstring states one subject ("acquired between interest dates,
paid accrued interest to the seller") and one scope (exactly the fields a
person can state without tax knowledge). `map_ordinary_acquisition_answers`
emits exactly one `finding.v2` per call; nothing about disposition,
premium, or market discount appears anywhere in the schema or output. A
fresh reader can confirm this without asking the author — the docstring's
"Subject" and "Scope of the output" sections are the load-bearing text and
match the code.

### 2. Accepts ordinary-language structured answers — MET

`ORDINARY_ANSWERS_SCHEMA` is a closed JSON Schema
(`additionalProperties: false`) over six fields: `payer_name`,
`obligation_description`, `obligation_reference` (optional),
`acquisition_date`, `accrued_interest_paid_to_seller`, `currency` (const
`"USD"`), `tax_year`. `ORDINARY_QUESTIONS` gives the plain-language prompt
for each. All six are answerable from memory of one's own transaction; none
require a tax-law judgment. Confirmed structurally (schema
`additionalProperties: false`) and by test
(`test_extra_classification_field_is_rejected`,
`test_no_question_asks_for_a_tax_classification`,
`test_schema_has_no_classification_field`) — this is not just a naming
convention, an extra field is actually rejected before a fact is built.

### 3. Contribution admission validates the output — MET, independently traced

Read `packages/kernel/contribution.py::apply_contribution_batch` directly
(not taken from examination.md's description). Confirmed:
- It requires a real `kind == "contribution"` act, applies it and each
  successor act through `apply_act` (`packages/kernel/findings.py`), and
  only then marks the process record `"completed"`.
- It checks `finding.get("contribution_id") != contribution_id` and raises
  `ContributionError` on mismatch, and rejects a `"pins"` key on the
  finding (provenance-only rule).
- `apply_act`/`findings.py` around line 517 checks
  `contribution["evidence_id"] not in finding["evidence_ids"]`, and around
  line 582 checks evidence currentness — real content checks, not a
  pass-through.
- The test fixture `tests/support.py::registry_with_demo_kinds` copies the
  **real published kernel schema files byte-for-byte** into the test
  registry; it is not a mocked-out schema. `SchemaRegistry` therefore
  performs genuine schema validation during the test run.
- `test_admission_rejects_a_contribution_whose_evidence_was_never_submitted`
  and `test_admission_rejects_a_finding_whose_evidence_is_not_the_contributions`
  both independently reproduce and confirm rejection paths (the second
  test tampers with the finding's `evidence_ids` post-mapping and calls
  `apply_contribution_batch` directly, bypassing the mapper's own helper,
  which is a genuinely convincing negative-path proof).

This requirement is met and the claim in examination.md ("the boundary
genuinely checks, it does not rubber-stamp") is independently verified
true, not merely asserted.

### 4. Emits only canonical circumstance facts — MET, with one legibility caveat

`value` names exactly five top-level fields: `obligation` (nested
`payer_name`, `description`, `reference`), `acquisition_date`,
`accrued_interest_paid_to_seller`, `currency`, `tax_year`. All are
ordinary, non-tax quantities. Field names are largely self-explanatory to
a fresh reader without needing the docstring.

Caveat: the emitted `finding.v2` envelope carries a top-level `basis` field
set to `"attested"` (line 306), meaning "the person stated this about
their own circumstance" (provenance), distinct from `"documentary"`
(what a report said). This is a `finding.v2` envelope convention, not part
of `ORDINARY_ANSWERS_SCHEMA` or the circumstance value. However, `"basis"`
is also one of the nine words in the test's `_CLASSIFICATION_WORDS`
blocklist (tests use it to scan `ORDINARY_QUESTIONS` and the schema
property names for classification leakage, e.g., cost-basis language). A
fresh reader scanning the worked example JSON in examination.md and seeing
a field literally named `"basis"` in the output could momentarily suspect
a tax-classification leak (cost basis) before realizing it is an
unrelated provenance-envelope field from `finding.v2`, not something this
module invented or a field inside the circumstance `value`. This is
resolvable by reading the code (the blocklist is checked only against
`ORDINARY_QUESTIONS` and `ORDINARY_ANSWERS_SCHEMA["properties"]`, not
against the finding envelope), but it is a naming collision a fresh reader
has to work through rather than one the artifact disambiguates for them.
Not a defect in the guarantee itself — recommend renaming or annotating in
a follow-up, not blocking.

### 5. No tax classification requested or supplied — MET

Confirmed by reading `ORDINARY_QUESTIONS` and `ORDINARY_ANSWERS_SCHEMA`
directly: none of the six questions or six schema properties name a tax
treatment, election, adjustment, deduction, exclusion, or classification.
The closed schema makes this structural, not just a convention followed by
the current tests — `test_extra_classification_field_is_rejected`
independently confirms a smuggled field (`tax_treatment`) is rejected at
`validate_ordinary_answers`, before any act or finding is built.

## Other legibility observations

- `build_obligation_acquisition_bundle`'s literal-domain fixture (an
  admission scaffold scoped to exactly the payer/reference/tax-year
  supplied) is honestly flagged in both the module docstring and
  examination.md as not a production identity/association design. A fresh
  reader who reads only the code (not examination.md) would still catch
  this from the docstring on `build_obligation_acquisition_bundle` itself
  — the disclosure is in the artifact, not only in the narrative document.
  Good: the artifact does not depend on examination.md to be honest about
  its own scope limits.
- `OBLIGATION_ACQUISITION_FACT_TYPE_ID = "demo.tax.obligation-acquisition-circumstance"`
  is prefixed `demo.` — clearly synthetic/fixture-only, consistent with the
  charter's "all fixture data synthetic" constraint, and self-evident to a
  fresh reader without needing to ask.
- The five-way split of concerns (`map_ordinary_acquisition_answers` →
  pure mapping, `build_ordinary_acquisition_contribution` → act assembly,
  `contribute_ordinary_acquisition` → real admission call) is legible from
  function names and docstrings alone; a fresh reader can recover the
  layering without needing examination.md's prose to explain it.

## Top-line verdict

All five charter requirements are met. The contribution-admission
requirement was independently traced into `packages/kernel/contribution.py`
and `packages/kernel/findings.py` (not taken on the examination's word) and
found genuine — real schema files, real evidence-matching checks, and a
negative-path test that tampers with output after mapping to prove the
boundary itself is doing the rejecting. The test suite passes independently
(14/14). One minor legibility gap noted (the `basis` field-name collision
between the finding envelope's provenance field and the classification-word
blocklist) — worth a follow-up rename or comment, not a blocker.
