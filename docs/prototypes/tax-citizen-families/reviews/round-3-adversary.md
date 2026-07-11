# Round 3 Adversary Review - Tax Citizen Families it3

Reviewer label: codex-adversary-r3-2026-07-11
Target: `exhibits/tax-citizen-families/it3` at `be72d63`
Role: adversary reviewer

I read the adversary role, the round-3 charter and round file, the governance
set, the active planning inputs, the prior adversary review, and the it3
examination/artifacts. I did not read same-round peer reviews or commit-message
bodies before submitting this review.

## Method

Baseline command:

    git archive exhibits/tax-citizen-families/it3 | tar -x -C /tmp/tcf-it3-review
    PYTHONPATH=. python3 /tmp/tcf-it3-review/docs/prototypes/tax-citizen-families/it3/tools/harness.py

Result: 203 checks passed, including both runners, with exit 0. I also ran a
no-write Python probe importing the extracted harness. It mutated deep copies
of scenarios, ran `build_context` and both derivation paths, called the local
coverage and citation helpers, and validated mutated instances. The important
outputs are recorded below. Repository searches used:

    rg -n "project_closed_sets|closed_sets" packages/derivation docs/prototypes/tax-citizen-families/it3
    find /tmp/tcf-it3-review/docs/prototypes/tax-citizen-families/it3/instances -type f

The tax checks were compared with the primary [2025 Form 1040](https://www.irs.gov/pub/irs-prior/f1040--2025.pdf),
[2025 Form 1040 instructions](https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf),
[2025 Publication 1040 tables](https://www.irs.gov/publications/p1040),
[2025 W-2 instructions](https://www.irs.gov/pub/irs-prior/iw2w3--2025.pdf),
[1099-INT instructions](https://www.irs.gov/instructions/i1099int),
[Rev. Proc. 2024-40](https://www.irs.gov/pub/irs-drop/rp-24-40.pdf), and
[Rev. Proc. 2025-32](https://www.irs.gov/pub/irs-drop/rp-25-32.pdf).

## R1-R13 Attacks

### R1 - Two-source W-2 identity: disputed

Attack 1, two-source identity: **failed against the declared key, but the
runner reproduction is weak**. `content/bundle.tax-2025.json:8-21` declares
employer, tax year, and `w2-instance`, and the positive W-2 entity is present.
The `two_w2_same_employer` scenario produces line 1a = 42000. This is useful
evidence that two fixture rows can aggregate.

Attack 2, correction identity: **succeeds**. `it3/tools/harness.py:435-449`
computes `fact_id(..., k1)` twice with the same hard-coded key. It never creates
an old finding, a corrected value, a W-2c/correction act, or a supersession
record. The no-write probe changed the value from 42000 to 43000 and still
reported the same identity because `fact_id` does not receive a value. The
probe also changed both W-2 rows to the same `w2-instance` and finding ID; the
runner still published line 1a = 42000 because `build_context` passes only
symbol, value, and finding ID to `SourceFact` (`harness.py:197-204`). The
declared identity therefore is not what the runner exercised.

The [2025 W-2 instructions](https://www.irs.gov/pub/irs-prior/iw2w3--2025.pdf)
and [Form W-2c guidance](https://www.irs.gov/forms-pubs/about-form-w-2-c)
make correction a materially different event from merely repeating a key.
The examination itself discloses that no workspace supersession act is
materialized (`examination-it3.md:171-174`). R1 is not ready to close as a
correction contract.

### R2 - Closure semantics: decision closed, implementation still exposed

Attack: **failed against the written semantic decision**. The spike adopts
`fact-type.v1` reuse, `nature=determinable`, tax-year identity, free
supersession, and an attested finding basis (`spikes/closure-semantics.md`;
`content/bundle.tax-2025.json:78-121`; `instances/positive/finding.closure-attested.json`).
That directly repairs the it2 elective/determinable error.

Observation: the executable scenario does not carry that finding. It carries
`True` as a `choice` input for each closure (`harness.py:190-204`), while the
projection helper accepts only `fact_type` and `value.complete`
(`harness.py:464-470`). Thus R2 is a sound content decision, but its adoption
into the workspace-to-run boundary is not demonstrated by the harness.

### R3 - Load-bearing `closed_sets`: successful attack, honest disclosure

Attack 1: **succeeds as a machinery dependency**. `content/closure-projection.md:5-20`
admits that `closed_sets` is load-bearing. `rg` finds the field in the shipped
evaluator/runner, but `project_closed_sets` only in the it3 harness and review
content, not in the production derivation path. `RunContext` still accepts a
caller-supplied `frozenset` (`packages/derivation/evaluator.py:63-116`). The
standard scenario path derives that set directly from fixture booleans
(`harness.py:194-220`), not from current closure findings.

Attack 2, stale set without a finding: **failed**. The harness correctly blocks
the stale-set probe; R3(b) is real. Attack 3, finding without the projection:
**failed in the sense claimed by the artifact, but confirms the unresolved
dependency**. It returns `SOURCE_SET_UNCLOSED`, exactly as R3(c) says
(`harness.py:501-520`). This is honest disclosure, not closure of the
machinery boundary. I mark R3 still disputed pending the separately named
machinery decision.

### R4 - Coverage from records: partial closure

Attack, stale stored coverage: **failed**. `coverage_from_record` rebuilds the
interest family as open from the `unclosed_interest` record and overrides the
stale all-closed dictionary (`harness.py:546-573`). The record is schema
validated.

Attack, authoritative implementation/generalization: **succeeds**. The
coverage function is a throwaway harness helper, not a shipped read model or
coverage contract; the `rg` command above finds no production equivalent. It
also defines a family as open only when one selected mapping rule lists the
closure symbol in `missing` (`harness.py:546-554`). In the probe, removing
filing status caused five rules to block, yet coverage reported all three
source families closed. That may be correct as source-set coverage, but it is
not a general derivation-gap report. R4 demonstrates one record rebuild, not a
ratifiable coverage boundary.

### R5 - Citation attachment: wrong-line/year checks pass; role generality fails

Attack 1, wrong line: **failed**. The line 1a to line 2b mutation is rejected
by `form_field_citation_ok` (`harness.py:305-333`) and the committed negative.
Attack 2, wrong year: **failed** for the supplied 2026 form-field case;
`cross_year_ok` rejects a 2026 field bound to a 2025 symbol/citation
(`harness.py:312-351`). The schema-level resolved-citation negative also
works.

Attack 3, wrong content role: **succeeds**. I changed the valid rate-schedule
attachment's subject to the known line-12 standard rule while retaining the
valid rate-schedule citation fingerprint and `tax-method` role. The attachment
schema had no errors and `attachment_ok` returned `True`. The schema declares
independent enums but no relationship between subject identity/role and the
citation role (`schemas/citation-attachment.v1.schema.json:10-29`); the helper
checks known subject, tax year, locator kind, and substring only
(`harness.py:288-302`). This disproves the examination's general claim that a
valid citation attached to the wrong content role is rejected.

### R6 - Cross-citizen and year checks: failed at the claimed package surface

Attack, package boundary across facts, citations, and form fields: **succeeds**.
The three package mutations cover only a 2025/2026 parameter or rule. A
fact-type inserted into a package corpus returns `MEMBER_ABSENT`, not a
cross-year scope check; citations and form fields are not package members at
all. The package validator only resolves the rule/parameter corpus
(`packages/derivation/package_validation.py:98-145`). The direct form-field
check is useful but is not a package-boundary check. `content/package.tax-2025.json`
contains only rules and parameters.

The later-year positive is valid evidence that the 2026 high-income schedule
can be selected, and [Rev. Proc. 2025-32](https://www.irs.gov/pub/irs-drop/rp-25-32.pdf)
supports that year-specific parameter. It does not close the charter's
cross-citizen package claim. R6 is failed as stated.

### R7 - Line 1z boundary: narrow safety claim passes, semantic join remains weak

Attack, omitted siblings smuggled into line 9: **failed**. With
`line1-other.closed` false, the fixture publishes line 1a but blocks line 1z
and line 9. The rule requires line 1z, not line 1a
(`content/rules.2025.json:20-39`, `:62-73`), and the official 2025 form
explicitly says line 1z adds lines 1a through 1h and line 9 adds line 1z.

Attack, untyped sibling content: **succeeds as a limitation**. Adding an
arbitrary `line1_other_sources` row of 1000.00 while closed produced line 1z
43000 and line 9 43800. The fixture source type is the generic `intSource`
shape and there are no individual 1b-1h field citizens. A closure attestation
can therefore authorize an aggregate without a per-sibling join. The guard is
honest enough for a narrowly attested aggregate boundary, so I mark R7 closed
for the stated anti-omission property, with the aggregate limitation recorded
rather than treating it as full Form 1040 coverage.

### R8 - Standard deduction eligibility: failed

Attack, unknown individual conditions: **succeeds**. The declared fact value
schema is an object with five required booleans (`content/bundle.tax-2025.json:123-146`),
but the scenario schema accepts one nullable boolean and `build_context` emits
that boolean directly. With no object-valued eligibility finding, the ordinary
scenario still publishes line 12 = 15750. The probe output was:
`fact schema type object; runner value True; line12 15750`.

The explicit false and null fixtures do prove guard behavior, so the negative
behavior is not absent. They do not prove that the five facts are actually
asserted or projected. The [2025 Form 1040](https://www.irs.gov/pub/irs-prior/f1040--2025.pdf)
line 12a-d boxes are precisely the conditions that make the base table
insufficient. R8 remains failed at the workspace/run boundary.

### R9 - Line 16 method boundary: limitation is disclosed, input contract fails

Attack 1, ordinary method with unknown triggers: **succeeds**. The method fact
also declares an object with three required booleans, but the runner consumes a
plain `True` and publishes line 16 = 3011. This is the same bypass as R8
(`content/bundle.tax-2025.json`, method fact; `harness.py:174-220`). The
`alternate_method_blocked` fixture only proves the explicit false branch.

Attack 2, uncovered ordinary Tax Table band: **failed**. Changing wages to
50000 produced taxable income 35050, no line 16, and `LOOKUP_MISS`; the
fixture-minimal `on_miss=block` behavior is honest. This is consistent with the
[IRS 2025 Tax Table](https://www.irs.gov/publications/p1040), whose instructions
route taxable income below 100000 to the table, and with the line-16
instructions in the [2025 Form 1040 instructions](https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf).

The disclosed R9 limitation is therefore real and properly conservative, but
it does not cure the unasserted method object. R9 remains disputed rather than
closed for ratification.

### R10 - All-elective-open saturation: failed attack

The all-open attack **fails**. The scenario leaves filing status, rounding,
itemizing, eligibility, method, and all closures absent/open. The runner
published zero findings. No default became operative. This is a successful
E3.1 saturation check (`fixtures/scenarios.json` `all_open`; examination
`examination-it3.md:138-140`).

### R11 - Explanation termination: successful attack

Attack, actual five walks: **succeeds**. The present-zero and closure-zero
cases call `explain`, but the three alleged blocked/inapplicable walks only
extract fields from a newly constructed record (`harness.py:601-643`). They do
not call `explain` or render a terminal explanation for those states. The
no-write probe replaced the hard-coded `input_index_2025` with `{}`; the
rendered tree lost the source value but the check still passed because it only
inspected the finding's pin. The output still showed `[input]
f.int.firstbank.box1.zero.2025` without a resolved input value.

The five states are distinguished in records, which is useful, and the form
field content has five rendered-absence instructions. But the evidence does
not show that each explanation terminates at declared content and authoritative
records rather than a helper's hard-coded index or renderer convention. R11
is failed as an explanation-walk claim.

### R12 - Scenario/package provenance joins: failed

Attack, corrupt provenance without changing execution: **succeeds**. I changed
`package_id`, `bundle_id`, all three content filenames, and jurisdiction to
arbitrary non-empty strings. `scenario.v1` still validated, and the runner
still published line 1a = 42000. The schema only constrains these fields as
strings (`schemas/scenario.v1.schema.json:11-24`); the runner uses tax year and
the package id for an adoption pin but never resolves the named files or
checks bundle/package/jurisdiction compatibility (`harness.py:174-222`).

`symbol-bindings.2025.json` is a useful declared correspondence, but the
scenario -> package -> bundle -> content/citations join is not enforced.
R12 is failed.

### R13 - Committed examples: partial, not every changed relationship

Attack, example completeness: **succeeds**. The harness validates the listed
manifest entries, but `instances/expected.json:3-22` contains positives for
the five it3 schemas plus two finding types and a W-2 entity, and negatives for
schema/fact-value/attachment/cross-year cases. There are no committed positive
and negative examples for the changed package membership, rule guards,
parameter tables, bundle-to-symbol bindings as relationships, or the
correction/supersession behavior. The `find` command confirms the instance
tree contains only the listed hand-written files.

The existing examples are valuable and harness-local mutations are correctly
supplemental. They do not meet the charter's every-new-or-materially-changed
family/relationship wording. R13 is partial.

## Observations

- The synthetic-data boundary held. The exhibit contains synthetic identifiers,
  and the baseline, JSON, governance-lint, and whitespace checks reported by
  the examination were reproducible.
- The strongest it3 repairs are real: W-2 slip keys are declared without
  document keys; wrong-line and wrong-year supplied citation probes fail; the
  line-1z unclosed guard prevents a false line-9 total; alternate line-16
  methods publish nothing; all-open saturation publishes nothing; and Tax Table
  misses block rather than invent values.
- The 2025 Form 1040 primary source makes the remaining boundaries material:
  lines 1a-1h, 1z, and 9 are separate bridges; line 12a-d changes the standard
  deduction path; and line 16 is conditional on the instructions. The prototype
  must not turn those boundaries into a claim that the booleans are themselves
  asserted fact findings.
- R3 and R9 are not hidden limitations. Their disclosure is good process, but
  disclosure of a load-bearing machinery dependency or fixture-minimal tax
  table is not the same evidence as a ratified contract boundary.

## Dissent

I dissent from the examination's statement that every R1-R13 gate is closed.
The prototype is useful evidence and several attacks fail, but correction
identity, closure projection ownership, coverage as a production boundary,
citation-role validation, cross-citizen year joins, object-valued R8/R9
inputs, explanation termination, scenario joins, and example completeness
remain unresolved or only partially exercised. I do not recommend using this
round as sufficient evidence for the contract-foundational Tier 2 decision.
