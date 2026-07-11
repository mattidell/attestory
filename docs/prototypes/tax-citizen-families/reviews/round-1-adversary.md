# Round 1 Adversary Review - Tax Citizen Families it1

Reviewer label: codex-adversary-r1-2026-07-11
Target: `prototypes/tax-citizen-families/it1` at commit `88f0139`
Role: adversary reviewer

## Dissent

I dissent from ratifying this candidate as-is. The design is pointed in the
right direction, but several exhibits that are claimed as rejected or
rebuildable are only asserted in scenario JSON. The schemas and throwaway
validator do not independently enforce the most important stale-projection,
mixed-year, citation-resolution, and hidden-default traps.

## Attacks

### A1 - Missing fixture: Form 1040 line 1z is the real bridge into line 9

Attack: Use the official 2025 Form 1040 income structure against the candidate's
line 9 derivation. Form 1040 line 1a is not what line 9 says to add; line 9
adds line 1z, and line 1z adds lines 1a through 1h. A slice that jumps from W-2
box 1 / line 1a directly to line 9 can hide unexercised earned-income siblings
1b through 1h.

Outcome: Succeeds. `synthetic-slice.json` derives
`derived.form1040.line9.2025` from `derived.form1040.line1a.2025` and
`derived.form1040.line2b.2025`, with no `line1z` field, no declared closure for
lines 1b-1h, and no block proving those siblings are out of scope. The candidate
therefore tests the simple arithmetic result, not the official form bridge.

Exhibit: `it1/scenarios/synthetic-slice.json` pins line 9 to line 1a and line
2b. IRS Form 1040 (2025), page 1, line 1z says to add lines 1a through 1h, and
line 9 says to add line 1z, line 2b, line 3b, line 4b, line 5b, line 6b, line
7a, and line 8.

### A2 - Smuggled default: standard deduction is published without required facts

Attack: Treat Form 1040 line 12e as a derived value and ask which facts justify
the single standard deduction amount. The value depends on filing status and
can be affected by dependency, spouse itemizing, dual-status alien, age, and
blindness checkboxes on lines 12a-12d.

Outcome: Succeeds. `derived.form1040.line12e.2025` publishes `15750` while
pinning only `irs.2025.instructions1040.standard-deduction`. It does not pin a
filing-status finding, age/blindness facts, dependent status facts,
spouse-itemizes facts, dual-status facts, or an itemized-vs-standard choice.
This is an operative default in the contract surface, not a declared
dependency.

Exhibit: `it1/scenarios/synthetic-slice.json`, `derived_findings` entry
`derived.form1040.line12e.2025`. IRS Form 1040 (2025), page 2, line 12a-12e
prints the relevant condition checkboxes and the standard deduction table.

### A3 - Smuggled default: line 16 tax table path is chosen without full guards

Attack: Force the line 16 calculation to justify why the tax table path is
eligible. A line 16 tax computation can require alternate methods depending on
facts such as qualified dividends, capital gain, foreign earned income, child
investment income, or other instruction-driven cases.

Outcome: Partially succeeds. The candidate records one false guard for an
alternate qualified-dividend rule, but the published line 16 finding pins only
line 15, filing status single, and a tax-table row. It does not carry a declared
guard set showing all alternate line 16 methods in the slice are inapplicable,
nor does it show closure or absence for the facts that would trigger those
methods. This leaves the tax table path as a runner/editor assumption.

Exhibit: `it1/scenarios/synthetic-slice.json`, `derived.form1040.line16.2025`
and `rendered_absence_states.guard_inapplicable`. IRS Form 1040 (2025), line 16
points to instructions and checkboxes for sources of tax.

### A4 - Identity trap: employment engagement can become a source-document surrogate

Attack: Replace the forbidden document key with an apparently neutral
`employment_engagement_id` and ask where that engagement is declared,
individuated, and asserted independently of the W-2 document.

Outcome: Partially succeeds. The scenario avoids putting `evidence_id` or
`source_document` inside W-2 fact identity, and the explicit document-child
negative fails. But the two same-employer W-2 facts are separated by
`entity.employment.demo-main` and `entity.employment.demo-bonus`, and the
prototype does not include a schema, act, or source-independent individuation
rule for employment engagements. Without that declaration, the engagement id
can function as a renamed source-document row key.

Exhibit: `it1/scenarios/synthetic-slice.json`, `entities`,
`source_instances`, and W-2 `source_findings.identity_keys`.
`it1/examples/negative/tax-fact-type.document-child-identity.json` covers only
the obvious `source_document_identity: true` case.

### A5 - Absence/invalidity trap: invalid source value is represented as a finding

Attack: Follow the "present schema-invalid source value" state and check whether
the invalid value is kept outside authoritative findings.

Outcome: Succeeds. The absence matrix represents the invalid case as
`source_finding: { "symbol": "tax.2025.1099-int.box1", "value": "-12" }`.
If the value is schema-invalid, it should not be a finding at all; it should be
failed source/evidence extraction, failed validation, or a blocked proposal.
The matrix does block publication, but its exhibit language has already let an
invalid value wear the finding shape.

Exhibit: `it1/scenarios/synthetic-slice.json`,
`absence_invalidity_matrix.present_schema_invalid_source`. The validator checks
that an explanation walk exists; it does not enforce that invalid source values
cannot be findings.

### A6 - Citation trap: citation ids are opaque strings, and IRS PDF URLs drift

Attack: Mutate a source-field citation to cite the wrong official source while
keeping the schema valid. Separately, check whether document identity is stable
when an IRS "latest" PDF URL changes.

Outcome: Succeeds. A no-write probe changed the positive
`source-field.1099int.box1.json` citation to `irs.2025.formw2.box1`; the
`source-field.v1` schema returned no validation errors. The schema requires
strings, not resolvable citations whose tax year, document family, and locator
match the content being cited. In addition, the candidate catalog labels
`https://www.irs.gov/pub/irs-pdf/fw2.pdf` as `2025 Form W-2`, but that URL
currently opens as `2026 Form W-2`. The candidate's free-text
`document_revision` is not enough to pin document identity against IRS latest
PDF drift.

Exhibit: `it1/schemas/source-field.v1.schema.json` has `citation_ids` as an
array of strings only. `it1/source-catalog.json` uses `fw2.pdf` for the alleged
2025 W-2. Official IRS source checked: `https://www.irs.gov/pub/irs-pdf/fw2.pdf`.

### A7 - Ordering/evolution trap: mixed-year package membership is not enforced

Attack: Build a `rule-content-binding.v1` instance with a 2025 package scope
but 2026 fact, form-field, source-field, and citation ids.

Outcome: Succeeds. A no-write schema probe returned no validation errors for
that mixed-year binding. The scenario says a mixed-year package member rejects,
but the rejection is not in the schema and is not independently checked by the
validator except as a literal `result: "reject"` field in scenario JSON.

Exhibit: `it1/schemas/rule-content-binding.v1.schema.json` has no cross-field
tax-year consistency rule. `it1/scenarios/synthetic-slice.json`,
`mutations.mixed_year_negative`, is assertion evidence rather than a rejected
instance.

### A8 - Coverage trap: stale closed projection passes the report schema

Attack: Keep `coverage-report.v1.authoritative_state` false and the stale policy
strict, but set a source set to `closure_state: "closed"` with
`closure_finding_id: null`.

Outcome: Succeeds. A no-write schema probe returned no validation errors. The
negative example fails because it also sets `authoritative_state: true` and
`accepts_unbacked_closed_projection: true`; it does not isolate the stale
closed projection shape. The scenario says stale projection is rejected, but
the report schema permits it.

Exhibit: `it1/schemas/coverage-report.v1.schema.json` lacks an `if/then`
constraint requiring a non-null closure finding when `closure_state` is
`closed`. `it1/examples/negative/coverage-report.authoritative-state.json`
mixes the stale-projection issue with other invalid fields.

### A9 - Misleading artifact: hash and parity evidence is not recomputed

Attack: Treat the stored hashes in citation parity and coverage rebuild as
evidence and ask whether the validator recomputes them from inputs.

Outcome: Succeeds. The validator compares literal hash strings inside the
scenario and examples; it does not rebuild coverage from an act log, rerun
evaluation with a citation mutation, or verify bytes. A stale or fabricated
hash with the expected string shape would still pass unless it violated another
hand-coded condition.

Exhibit: `it1/validators/validate_it1.py`, `check_scenario()`, checks equality
between fields already present in `synthetic-slice.json`.

### A10 - Failed attack: explicit document-child identity is rejected

Attack: Use the obvious forbidden identity key:
`source_document_identity: true`.

Outcome: Failed. The `tax-fact-type.v1` schema rejects this shape with the
expected `False was expected` reason, and the scenario source findings I
inspected do not put `source_document` or `evidence_id` in their identity key
objects.

Exhibit: `it1/examples/negative/tax-fact-type.document-child-identity.json`;
`it1/schemas/tax-fact-type.v1.schema.json`.

### A11 - Failed/limited attack: 1099-INT box 2 direct bridge is caught

Attack: Feed 1099-INT box 2 early-withdrawal penalty directly to Form 1040 line
2b.

Outcome: Failed for the exact fixture. The throwaway validator has a semantic
check for `source-field.box2-misbridged-to-line2b.json` and rejects it. The
failure is limited: the schema itself does not encode the bridge rule, so the
protection depends on special-case validator code for this one filename rather
than declared portable content.

Exhibit: `it1/validators/validate_it1.py`, `semantic_errors()`;
`it1/examples/negative/source-field.box2-misbridged-to-line2b.json`.

## Observations

- The candidate is strongest where it creates named citizen families for form
  fields, source fields, official citations, tax fact companions, rule bindings,
  and coverage reports. That direction matches the governance pressure for
  canon, declaration, and legibility.
- The weakest evidence pattern is "scenario as proof." Several central claims
  are represented as result strings inside `synthetic-slice.json`, not as
  independently rejected instances or rebuildable outputs.
- Citation placement needs a resolver-level contract: citation ids must resolve
  to existing citation citizens, and cited tax year/document family/locator must
  be compatible with the citing artifact. String arrays are insufficient.
- The prototype uses synthetic demo entities and values. I saw no personal data
  or absolute local path in the inspected artifacts.

## Verification

- Ran no-write schema probes against pinned commit `88f0139` for stale coverage,
  mixed-year binding, and wrong citation id; each returned no schema errors.
- Ran `git diff --check -- docs/prototypes/tax-citizen-families/reviews/round-1-adversary.md`: pass.
