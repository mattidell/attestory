# Round 3 Governance Review - Iteration 3

Reviewer: codex-governance-r3-2026-07-11
Scope: `exhibits/tax-citizen-families/it3` at `be72d639`
Role: governance fidelity only

This review measures the R1-R13 closure claims against the ratified
governance set. A passing harness check is reported separately from whether
the exhibit is sufficient evidence for a contract-foundational Tier 2
decision.

## Measurements

### R1 - Two-source W-2 identity

**Prototype check: pass for peer identity.** The W-2 fact type keys on
employer, tax year, and a `us.w2-slip` entity, not on document or evidence.
`two_w2_same_employer` produces two facts and line 1a equals `42000`. The
evidence swap/removal probe preserves the finding id, fact id, and value.
Exhibits: `it3/content/bundle.tax-2025.json`,
`it3/fixtures/scenarios.json`, `it3/tools/harness.py` section 6.

**Tier 2 evidence: disputed for correction semantics.** The corrected-W-2
check calls the same `fact_id` function twice with the same keys; it does not
materialize a correction finding, superseding act, or displacement of a
dependent finding. The identity choice is coherent, but the correction
lifecycle required by Articles 7 and 12 is asserted in prose rather than
reproduced through the workspace record.

### R2 - Closure semantics

**Prototype check: pass.** The mini-spike rejects elective closure, adopts
`fact-type.v1`, declares `nature: determinable`, gives the closure finding
`basis: attested`, states `{tax-year}` identity, free supersession, and pins
from a closure-backed result. The committed closure finding validates.
Exhibits: `it3/spikes/closure-semantics.md`,
`it3/content/bundle.tax-2025.json`,
`it3/instances/positive/finding.closure-attested.json`.

**Tier 2 evidence: sufficient for the semantic choice, conditional on R3.**
The fact-type decision is materially stronger than it2 and does not invoke
reserved T1 or T2 doctrine. Its lifecycle evidence is still only declarative;
the correction and displacement evidence remains the R1 limitation.

### R3 - Closure load-bearing check

**Prototype checks: partial pass.** The three perturbations pass: a closure
finding plus projection yields a pinned zero, a stale projection without the
closure symbol does not yield a zero, and withholding the projection blocks
with `SOURCE_SET_UNCLOSED`. The exhibit honestly admits that `closed_sets` is
load-bearing in `it3/content/closure-projection.md`.

**Tier 2 evidence: disputed.** The declared projection is not actually wired
into scenario construction. In `it3/tools/harness.py`, `build_context`
creates both the closure input and `closed_sets` directly from the scenario
booleans; `project_closed_sets` is used only in the isolated R3 assertions.
The harness therefore does not establish that the runner receives a
projection rebuilt from authoritative current closure findings. The markdown
contract is also not a versioned package member or an adoption/pin dependency.
This leaves a load-bearing machinery boundary outside the declared adopted
artifact set, contrary to Articles 4, 11, and 12. The examination's escalation
to an owner/machinery decision is correct, but the gate cannot be called fully
closed on this evidence.

### R4 - Coverage from records

**Prototype checks: narrow pass.** A schema-valid `derivation-record.v1` is
constructed, coverage is recomputed from its blocked entries, and a stale
stored projection cannot override the result. The unclosed-interest and fully
closed cases produce the expected states.
Exhibit: `it3/tools/harness.py` section 8.

**Tier 2 evidence: insufficient.** `coverage_from_record` is a harness-local
hard-coded map from rule ids to closure symbols, not declared content or a
record-derived read-model contract. The record is synthesized after the run
from `RunResult`; no authoritative workspace record is rebuilt after deleting
or changing a coverage representation, and no competing current records are
tested. This proves the stale-override property for one record shape, not the
Article 14 boundary that observed coverage belongs to records and available
coverage is computed fresh.

### R5 - Citation attachment model

**Prototype checks: partial pass.** Form-line, tax-year, and cross-citizen
attachment examples validate; the wrong-line and wrong-year negatives reject;
attachments cover fact types, parameters, a rule, and a form field. The
resolved-citation invariant is now in the schema rather than only in a helper.
Exhibits: `it3/schemas/citation-attachment.v1.schema.json`,
`it3/content/citation-attachments.2025.json`, harness section 4.

**Tier 2 evidence: failed for the claimed role boundary.** The attachment
schema permits every role for every subject kind, and `attachment_ok` checks
only subject existence and the expected citation fingerprint. A W-2
fact-type attachment relabeled with the `tax-method` role and retaining the
matching W-2 citation is accepted. The required wrong-content-role negative
is absent. Also, the ordinary form-field check accepts a 2025 line 1a field
with the 2026 line 1a citation; only the separate 2026 cross-year probe catches
its particular direction. Citation linkage is improved, but the claimed
governance constraint is not closed.

### R6 - Cross-citizen package and year checks

**Prototype checks: partial pass.** The later-year positive runs, and package
validation rejects the tested 2025/2026 rule and parameter substitutions. A
2026 form field bound to a 2025 symbol/citation is rejected.

**Tier 2 evidence: insufficient for the gate as written.** The mixed-year
checks do not cover fact or fact-type membership, citation membership, or a
package that closes over those citizens. The package manifests contain rules
and parameters only; bundle, form fields, citations, and symbol bindings are
outside the package closure. The 2026 scenario points to the 2025 bundle and
2025 symbol-bindings file, and scenario validation does not cross-check those
references against tax year. R6 therefore demonstrates selected year guards,
not the required cross-citizen package boundary.

### R7 - Form 1040 line 1z boundary

**Prototype check: pass for the declared narrow slice.** Line 1z is a
completeness-gated rule, line 9 consumes line 1z rather than line 1a, and
`line1z_unclosed` blocks instead of silently omitting lines 1b-1h.
Exhibits: `it3/content/rules.2025.json`,
`it3/content/form-fields.2025.json`, the `line1z_unclosed` scenario.

**Tier 2 evidence: sufficient for this boundary claim, not for full line-1
coverage.** The omission is declared and cannot make line 9 appear complete.
The absent sibling citizens remain out of scope as the examination states.

### R8 - Standard deduction eligibility boundary

**Prototype checks: partial pass.** The eligibility fact declares five inputs;
special-condition and unknown fixtures prevent silent publication, and the
all-open fixture does not default the branch.

**Tier 2 evidence: disputed at the projection boundary.** The declared fact
is object-valued, but scenario inputs and `build_context` accept the already
projected boolean `std_ordinary_eligible`. No authoritative finding and
declared executable projection from the five conditions to that boolean is
run. `symbol-binding.v1` documents the projection in prose, while the
scenario harness supplies its result directly. The guard boundary is honest
for the tested slice, but Article 11 evidence is not sufficient to show that
the five declared inputs, rather than runner knowledge, control eligibility.

### R9 - Line 16 method boundary

**Prototype checks: partial pass.** The high-income fixture selects the rate
schedule, the low-income branch is fixture-tested through the minimal Tax
Table, and alternate-method input makes both ordinary branches inapplicable.
The `on_miss: block` limitation is honest breadth management.

**Tier 2 evidence: disputed at the same projection boundary as R8.** The
object-valued `tax-computation-method` fact is reduced to the direct boolean
`ordinary_tax_method` scenario input; no declared projection is executed. The
ordinary-versus-alternate boundary is therefore described and sampled, but
not shown as an artifact-controlled dependency. The fixture-minimal Tax Table
alone is a breadth limitation; the unexecuted method projection is a contract
limitation.

### R10 - All-elective-open saturation

**Prototype check: pass.** The reproduced `all_open` run publishes nothing,
and a direct inspection shows all ten rules blocked, with no inapplicable
disposition. No default becomes operative. This is sufficient narrow evidence
for E3.1, subject to the R8/R9 projection limitations for their non-elective
eligibility/method facts.

### R11 - Complete absence and rendered-absence explanations

**Prototype checks: partial pass.** The two positive-zero walks pin the source
or closure finding, and the three negative-state checks find the expected
blocked or inapplicable record entries with declared codes and guard results.

**Tier 2 evidence: insufficient as five explanation walks.** Only the two
positive cases go through `explain()`. The no-source, invalid-source, and
false-guard cases extract entries from a newly synthesized record; they do not
walk an explanation graph grounded in the persisted process record. The
positive explanation input index is also a harness-local hand-built map rather
than the scenario's authoritative findings. This passes the intended
disposition checks but does not establish Article 15's record-grounded
explanation contract.

### R12 - Scenario and package provenance

**Prototype check: partial pass.** `scenario.v1` requires package, bundle, tax
year, jurisdiction, form-field, citation, and symbol-binding references, and
the committed scenarios carry them. A fresh reader can identify the intended
files from the strings.

**Tier 2 evidence: insufficient.** Schema validation does not resolve or
cross-check the referenced files, and `build_context` uses the provenance only
for year and adoption pins. The package itself is not a closed manifest over
the bundle, form fields, citations, or symbol bindings. The later-year scenario
uses a 2025 bundle and 2025 symbol-binding file without an explicit
cross-year compatibility assertion. The path from scenario to package is
declared, but the full scenario -> package -> facts -> rules -> citations ->
form-fields chain is not contract-validated.

### R13 - Committed positive and negative examples

**Prototype check: pass for the manifest.** Eight positive and nine negative
examples are committed and the harness validates each according to its
declared rejection mode. The examples are synthetic and publishable.
Exhibits: `it3/instances/expected.json`, `it3/instances/positive/`,
`it3/instances/negative/`.

**Tier 2 evidence: insufficient for every changed relationship.** The
manifest has no correction/supersession example for the R1 lifecycle, no
executed closure-projection example as a workspace contract, no
tax-computation-method finding example, and no wrong-content-role citation
negative. It proves the listed examples, not the charter's broader
"every materially changed citizen family or relationship" claim.

## Observations

1. The exhibit is materially stronger than it2 on peer identity, closure
   nature/basis, source-set boundary, line 1z honesty, citation resolution,
   scenario provenance shape, and explicit absence dispositions.
2. The green harness result is real but narrow: the tagged harness reproduced
   `203` passing checks with exit `0`, including forward/reference parity and
   deterministic reruns. Several checks validate helper functions or
   post-hoc records rather than the authoritative workspace boundaries named
   by the Constitution.
3. `GOVERNANCE_PINS` contains Constitution, Ontology, Principles, and
   Engineering Constraints, but omits `governance.commentary`. The generated
   derivation records therefore do not pin the complete governance set required
   by Article 14 and the Constitution governance note.
4. The closure projection contract is useful evidence because it names the
   load-bearing dependency instead of hiding it. Its current form is still a
   machinery contract in a markdown file, not a versioned adopted artifact
   with a pin.
5. No artifact introduces reserved T1 derived-finding authority construction,
   T2 stance/position doctrine, redaction, or multi-party authority. The
   closure and method choices remain workspace facts/inputs and do not claim
   legal effect.

## Dissent

I dissent from the examination's blanket disposition that every R1-R13 gate
is closed. I agree that the listed harness checks pass and that R2, R7, and
R10 have strong narrow evidence. I do not agree that R1 correction, R3
projection wiring, R4 record-derived coverage, R5 role validation, R6
cross-citizen year closure, R8/R9 condition projections, R11 record-grounded
walks, R12 full provenance, or R13 relationship coverage are sufficient for a
contract-foundational Tier 2 decision.

The exhibit should remain evidence for a further disposition, not be treated
as ratification-ready contract evidence under ADR-0005. The primary blocking
questions are whether load-bearing machinery is itself adopted and pinned, and
whether projected eligibility/method/coverage state is derived from declared
authoritative citizens rather than supplied by the harness.

## Verification

- Read the governance set, `roles/reviewer-governance.md`,
  `charter-it3.md`, `round-3.md`, ADR-0005, and prior-round governance
  material.
- Inspected the it3 artifacts from tag `exhibits/tax-citizen-families/it3`.
- Did not read same-round peer reviews or commit-message bodies before
  submitting this review.
- Reproduced the tagged harness from a temporary archive:
  `PYTHONPATH=. python3 docs/prototypes/tax-citizen-families/it3/tools/harness.py`;
  `203` checks passed, exit `0`.
- Probed the tagged harness: `project_closed_sets` is not called by
  `build_context`; a wrong citation content role is accepted; a 2025 field
  with a 2026 citation passes the ordinary form-field check; `all_open` has
  zero publications and ten blocked rules.
- `artifact-checks.txt` reported `RESULT PASS`, with zero missing required
  files, zero JSON parse failures, and zero absolute-path matches.
