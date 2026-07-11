# Round 2 Adversary Review - Tax Citizen Families it2

Reviewer label: codex-adversary-r2-2026-07-11
Target: `prototypes/tax-citizen-families/it2` at commit `989d9fe`
Role: adversary reviewer

I read the required charter, examination, role, round instructions, governance
set, and permitted prior-round material. I did not read same-round peer outputs
or commit-message bodies before submitting this review.

## Dissent

I dissent from accepting it2 as contract-ready. It2 is a meaningful improvement
over it1, but its strongest claims are still partly properties of the throwaway
harness or shipped runner rather than independently declared content contracts.
The empty-closure path still depends on `closed_sets`, coverage is not rebuilt
from authoritative state, and several included Form 1040 meanings remain
unexercised. The rival design therefore does not yet establish that the two new
citizen families and closure move are safe to ratify.

## Attacks

### A1 - Missing fixture: line 1z is still skipped

**Attack.** Follow the official 2025 Form 1040 bridge from W-2 income through
lines 1a-1h to line 1z, then from line 1z into line 9. Ask whether a non-W-2
earned-income line can be added without changing the line 9 contract.

**Outcome: succeeds.** It2's line 9 rule adds only line 1a and line 2b. There is
no line 1z field, no 1b-1h closure or exclusion contract, and no negative fixture
showing that the omitted siblings are deliberately outside the slice. This is
the same unresolved attack found against it1, not a closed comparative finding.

**Exhibit.** `it2/content/rules.2025.json:43-52` and
`it2/content/form-fields.2025.json:37-51`. The official 2025 Form 1040 has the
line 1z and line 9 bridges: [Form 1040 (2025)](https://www.irs.gov/pub/irs-prior/f1040--2025.pdf).

### A2 - Smuggled default: standard deduction eligibility is incomplete

**Attack.** Assert only filing status and the non-itemize choice, then vary the
line 12a-12d conditions that affect the standard deduction: dependency, age,
blindness, spouse itemizing, dual-status, and other instruction conditions.

**Outcome: succeeds.** The standard branch requires only `filing_status` and
`itemize-election` and then publishes the filing-status table amount. It has no
declared inputs or guards for the other conditions. The absence of an engine
default is not enough when the rule itself chooses a base amount for an
under-specified taxpayer. The official instructions describe the additional
standard-deduction conditions: [Instructions for Form 1040 (2025)](https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf).

**Exhibit.** `it2/content/rules.2025.json:68-78` and
`it2/content/parameters/standard-deduction.2025.json:1-12`. The fixture set has
only the ordinary single-filer path.

### A3 - Smuggled default: line 16 selects the rate schedule for all incomes

**Attack.** Run line 16 with taxable income below $100,000 and with a condition
that requires a qualified-dividend, capital-gain, foreign-earned-income, or
other alternate worksheet. Ask whether the rule declares why the rate schedule
is eligible.

**Outcome: succeeds, although the limitation is disclosed.** The rule has an
unconditional `when: true` and applies the rate schedule across all incomes.
The note admits that the real 2025 instructions require the Tax Table below
$100,000 and that alternate worksheets exist, but disclosure does not make the
published line 16 result an honest covered result. No fixture crosses the
$100,000 boundary or proves alternate methods are inapplicable. See the
[2025 Form 1040 instructions](https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf)
and [2025 tax tables](https://www.irs.gov/publications/p1040).

**Exhibit.** `it2/content/rules.2025.json:107-122`; every line 16 positive in
`it2/fixtures/scenarios.json` is below the omitted method boundary.

### A4 - Identity trap: same-employer W-2 questions can collide

**Attack.** Supply two distinct W-2 source instances for the same employee,
employer, and tax year, with different reported wages, then replace one with a
corrected or reissued source. Ask whether the model distinguishes separate
questions without making a document id the fact key.

**Outcome: succeeds as an evidence and contract attack.** It2 keys the W-2
wage fact only by employer and tax year. Its F1 check hashes the same key twice
and changes only `evidence_ids`; it never executes two same-employer source
instances. A second legitimate W-2 therefore has no declared individuation
path, while a correction and a second contemporaneous form are forced toward
the same fact without a declared distinction. The obvious document-child trap
is rejected, but the harder collision remains open.

**Exhibit.** `it2/content/bundle.tax-2025.json:7-18` and
`it2/tools/harness.py:323-340`. This also remains in tension with the Ontology's
statement that a second W-2 brings its own wage questions into existence.

### A5 - Citation trap: valid ids do not establish citation meaning

**Attack.** Change the 2025 line 1a field to cite the valid line 2b citation.
Separately ask where rules and parameters declare their source citation ids.

**Outcome: succeeds.** The form-field schema requires only a nonempty citation
id, and the harness checks only that the id exists. A no-write probe changed
`us.f1040-2025.line1a.citation_id` to
`us.cite.f1040-2025.line2b` and produced no validation failure. Rules and
parameters have no citation-id field, and the package manifest does not include
the citation or form-field citizens. The resolved flag mutation is caught, but
document identity, tax-year compatibility, and locator-to-field compatibility
are not.

**Exhibit.** `it2/schemas/form-field.v1.schema.json:22-25`,
`it2/content/package.tax-2025.json:6-16`, and
`it2/tools/harness.py:162-178`. The citation records themselves are
`it2/content/citations.2025.json:1-99`.

### A6 - Evolution trap: the package check is narrower than the content set

**Attack.** Build a 2026 form field that binds to the 2025 line 1a symbol and
the 2025 citation, or instantiate a 2026 tax-year key from the 2025 fact bundle.
Ask whether a 2025 package or field registry rejects the mixed-year shape.

**Outcome: succeeds.** A no-write schema probe accepted the mixed 2026 form
field because the schema does not relate `form.tax_year` to `binds_symbol` or
`citation_id`. The 2025 fact bundle explicitly permits both 2025 and 2026 in
its identity-key value lists. The passing mixed-package probe checks one 2025
parameter as a member of a 2026 package; it does not close the bundle,
form-field, or citation relationships.

**Exhibit.** `it2/content/bundle.tax-2025.json:11-14`, `:27-30`, and `:44-46`;
`it2/content/evolution/form-fields.2026.json:3-10`; the narrower check is
`it2/tools/harness.py:518-533`.

### A7 - Coverage trap: the rebuild result is a fixture projection

**Attack.** Run an unclosed workspace, then ask the coverage builder for current
coverage while supplying a stale or contradictory closure projection. Delete
the projection and rebuild from current findings and run blocks.

**Outcome: succeeds.** `coverage_report()` ignores the run result and returns
`closed` or `open` directly from fixture booleans. A no-write probe paired an
unclosed run, which blocked line 2b, with a fixture carrying `interest_closed:
true`; the report still said `interest-sources: closed`. The stale-projection
check proves only that the derivation rule does not publish a zero from a bare
`closed_sets` string. It does not validate a coverage citizen, an act log, or a
rebuild against authoritative current state.

**Exhibit.** `it2/tools/harness.py:417-451`. This is a direct failure of the
Article 14 / E7.1 detection, despite the examination's F11 claim.

### A8 - Runner dependency: closure facts do not replace `closed_sets`

**Attack.** Keep the closure finding present and valid, remove only the
`closed_sets` projection, and run an empty interest source set. If the closure
fact is authoritative and load-bearing, the closure-backed zero should still
publish.

**Outcome: succeeds.** With the interest closure finding present and
`closed_sets=frozenset()`, the empty interest scenario blocks line 2b with
`SOURCE_SET_UNCLOSED`. With the projection restored, it publishes zero. Thus
`closed_sets` remains an operative runner input for the exact F3/F4 empty-set
case, contrary to the claim that it has degraded to a projection. The stale
probe tests the opposite direction only: a bare projection without the finding
does not publish.

**Exhibit.** `it2/content/rules.2025.json:26-38`,
`it2/tools/harness.py:192-218`, and the examination's load-bearing claim at
`examination-it2.md:60-69`.

### A9 - Closure-as-elective-fact attack

**Attack.** Assert `{complete: true}` with no documentary evidence and ask
whether the system has declared the epistemic basis and lifecycle of the
completeness assertion, rather than treating it as an ordinary tax election.

**Outcome: succeeds as a semantic dissent.** It2 declares source-set closure
with `nature: elective` and injects it as a `choice` input. The Ontology defines
elective nature for questions the law leaves open, such as filing status and
methods; closure is instead an assertion about whether the source search is
complete. No basis, source-set inventory, attestation act, or distinction from
an elective tax choice is represented in the closure citizen. The move may be
defensible, but it is not established by the unchanged `fact-type.v1` schema
and should not be treated as a settled Tier 1 reuse.

**Exhibit.** `it2/content/bundle.tax-2025.json:83-115`,
`it2/tools/harness.py:192-198`, and Ontology sections 2 and 4.

### A10 - Invalidity and explanation-walk attack

**Attack.** Follow the invalid source value through the assertion boundary and
then request explanation walks for all four F5 states and the F7 false guard.

**Outcome: mixed.** The runner correctly blocks the supplied invalid string
with `DEPENDENCY_INVALID`, and the unclosed state has a distinct block. But the
harness passes the invalid string directly as a `SourceFact`; it does not prove
that an invalid value cannot enter authoritative findings. More importantly,
the only actual explanation walk executed is the closure-backed zero. The
examination's claim that each F5/F7 state has a walk is therefore scenario
assertion, not evidence.

**Exhibit.** `it2/fixtures/scenarios.json:67-92`,
`it2/tools/harness.py:268-311` and `:458-488`. This is narrower than it1's
scenario-as-proof problem, but it remains a real evidence gap.

## Failed attacks

- **F1 obvious document-child identity:** failed. The W-2 identity keys contain
  no source document or evidence id, and the evidence swap/removal probe keeps
  the fact id and value stable. Exhibit: `it2/content/bundle.tax-2025.json:7-18`
  and `it2/tools/harness.py:323-340`.
- **F2 box 8 leakage into line 2b:** failed for the exercised case. The box 8
  source is present and line 2b remains 800; the rule explicitly collects only
  box 1 and box 3. Exhibit: `it2/content/rules.2025.json:21-39` and
  `it2/fixtures/scenarios.json:54-65`.
- **E3.1 all-elective-open saturation:** failed. A no-input run published no
  findings and blocked every rule with missing dependencies. This closes the
  narrow machinery-default attack, not the under-specified tax inputs in A2.
- **F8 citation operability:** failed. Citations are absent from `RunContext`,
  so changing citation text cannot affect derived output. This establishes
  non-operability, not correct citation attachment.
- **F9 parameter-member mixed package:** failed. The ratified package validator
  rejects a 2025 parameter in the one-member 2026 package probe with
  `SCOPE_MISMATCH`. The broader A6 field/bundle attack still succeeds.
- **F10 wage correction cascade:** failed. The harness observes displacement of
  line 1a and downstream wage-dependent findings while leaving line 2b
  independent. Exhibit: `it2/tools/harness.py:384-410`.

## Observations

- It2 closes or sharpens several it1 findings: box 1/box 3 membership is
  declared, closure findings can appear in pins, strict schema negatives are
  exercised against the published registry, and the limited parameter package
  cross-year check is real. These are convergent improvements, not evidence
  that the full content contract is closed.
- The new `form-field.v1` and `source-citation.v1` families are directionally
  appropriate. Their cross-citizen relations, package membership, and tax-year
  compatibility are not yet declared strongly enough for independent consumers.
- The harness is useful reproduction evidence, but several checks compare
  strings or fixture fields rather than rebuilding state. `EVIDENCE.txt` proves
  the harness run, not the stronger claims made in the examination.
- The committed prototype artifacts inspected are synthetic and contain no
  personal data or absolute local machine paths.

## Comparative disposition

Evidence converges that it2 is stronger than it1 on the exercised 1099-INT box
mapping, closure pin visibility, strict negative examples, and the narrow
parameter-package evolution check. Evidence also converges that the line 1z
bridge, standard-deduction eligibility, same-employer W-2 collision, and full
line 16 method surface remain unresolved. It2 introduces or exposes additional
contract risks around runner-dependent closure, fixture-derived coverage,
cross-citizen citation resolution, and closure's elective classification.

I recommend a third iteration before any Tier 2 ratification. It should make
coverage rebuild from authoritative records, remove the empty-closure runner
dependency or declare it as a machinery contract, enforce citation and year
relationships across package members, exercise line 1z and the omitted line 12
and line 16 guards, and provide a source-instance identity decision with
explanation evidence for every absence and invalidity state.

## Verification

- Extracted the pinned it2 tree to a temporary directory and ran
  `PYTHONPATH=. python3 docs/prototypes/tax-citizen-families/it2/tools/harness.py`:
  77 checks passed, exit 0.
- Ran no-write probes for wrong citation attachment, fixture-derived coverage,
  missing `closed_sets`, mixed-year form-field binding, and all-elective-open
  saturation. The first four exposed the outcomes reported above; the last
  published nothing.
- `git diff --no-index --check /dev/null
  docs/prototypes/tax-citizen-families/reviews/round-2-adversary.md`: no
  whitespace errors (the expected exit status was 1 because the file is new).
