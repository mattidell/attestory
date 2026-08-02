# Round 3 Expressiveness Review

Reviewer seat: `roles/reviewer-expressiveness.md`.
Exhibit reviewed: `exhibits/tax-citizen-families/it3` (`be72d63`).

## Independence and ordering

I read the expressiveness role, `charter-it3.md`, and `reviews/round-3.md`.
I did not read any same-round peer review or commit-message body.

I ran the reproduction and artifact checks before opening
`docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/examination-it3.md`, as required. I then
read the examination and compared its claims with the tagged artifacts and my
recorded results.

## Checks run

- The tagged harness, using the README command on the extracted exhibit, exited
  0 and printed 203 `[PASS]` checks. This covered both runners, all 2025 and
  2026 scenarios, the committed examples, R1-R6/R11-specific harness checks,
  and the all-open scenario.
- Independent artifact checks passed: all required exhibit files were present,
  all 41 JSON files parsed, all committed-example manifest paths resolved, the
  16 2025 and 1 2026 scenario ids were unique, and no absolute local paths
  were present.
- An independent all-open probe found zero publications, all ten 2025 rules
  accounted for as `DEPENDENCY_ABSENT` blocks, and no unaccounted rule.
- The two citation-attachment negatives were schema-valid and were rejected
  only by the harness helper. A 2025 form field mutated to bind the line-2b
  output symbol was also schema-valid and passed the existing form-field
  citation helper.

The harness result is therefore reproducible, but it is not by itself
sufficient evidence for every contract claim.

## Gate dispositions

| Gate | Disposition | Review result |
|---|---|---|
| R1 | still disputed | The fixture contains two W-2 entries and the aggregate is 42000, but `build_context` drops `employer`, `w2_instance`, and `evidence_id` when constructing `SourceFact` (`it3/tools/harness.py:204-206`). The peerage check hashes hand-written keys instead of keys derived from the fixture (`:421-449`). The correction check hashes the same key twice and does not exercise a correction or supersession act. The source-instance design is plausible, not reproduced end-to-end. |
| R2 | still disputed | The spike and bundle declare determinable closure with attested findings, identity keys, free supersession, and pins. However, the scenario runner injects `wage_closed`/`interest_closed`/`line1_other_closed` as choice inputs and directly builds `closed_sets` (`:197-202`); it does not construct or consume the committed closure finding. The semantic decision is documented but not exercised by the normal slice. |
| R3 | failed as sufficient evidence | The projection contract honestly admits that `closed_sets` is load-bearing, but the shipped scenario path bypasses the declared projection. The standalone purity check recomputes the same function over the same input (`:483-488`), and the normal contexts receive fixture-derived closure truth. The withheld-projection and stale-string probes show runner behavior, but not that authoritative findings are the actual source of projection in the scenario path. This is an unresolved machinery contract, not ordinary breadth. |
| R4 | failed | `coverage_from_record` accepts only a record (`:546-554`). The `stale_stored` dictionary is created but never passed to any coverage consumer (`:567-570`), so the probe cannot show that a contradictory stored projection is overridden. The family mapping is also hard-coded to 2025. The record itself is valid and useful evidence, but the claimed stale-projection protection is not reproduced. |
| R5 | closed for supplied content; contract evidence disputed | The supplied attachment set covers the required kinds and roles, and the helper catches wrong-line and wrong-year mutations. The attachment schema itself accepts both negatives because cross-citizen resolution is outside the schema. The examination should not describe those as schema rejection; they are validator/helper rejection. Form fields carry citation ids, but only one rule and one form-field attachment are explicitly represented in the attachment collection. |
| R6 | failed | The checks cover form-field/citation alignment and mixed rule/parameter package members. They do not cover a mixed-year fact or fact-type/bundle boundary as required. The 2026 positive has `tax_year: 2026` while its provenance names the 2025 bundle and 2025 symbol-binding file (`fixtures/scenarios.2026.json:6`). The later-year execution is meaningful, but the package provenance is not year-coherent. |
| R7 | closed for the declared narrow boundary | `line1z` is gated by the line-1-other completeness assertion and line 9 consumes line 1z, so the `line1z_unclosed` result does not pretend that line 1a is all of line 1. This is honest exclusion of omitted siblings, not coverage of those siblings. |
| R8 | closed as a guard boundary; evidence limited | The special-condition and unknown scenarios block or mark the base-table branch in the expected way. The five conditions are declared in the fact value schema. The runner nevertheless receives the projected boolean directly (`:192-193`); no check establishes that the boolean must be derived from an authoritative eligibility finding. |
| R9 | closed with an explicit breadth limitation | The ordinary path is split at the declared Tax Table/rate-schedule boundary, and the alternate-method fixture makes both ordinary rules inapplicable. The fixture-minimal Tax Table has `on_miss=block`, and the 2026 slice is rate-schedule-only. Those are acceptable declared breadth limits, not evidence of complete tax-method coverage. |
| R10 | closed | The independent probe confirmed no publications and all ten rules blocked with `DEPENDENCY_ABSENT`; no default became operative. |
| R11 | closed for the five supplied walks | Present numeric zero pins the reported source finding; closure-backed zero pins the closure input; no source/no closure and invalid source terminate in distinct record blocks; false guard terminates in an inapplicable record disposition. These walks reach findings, declared rule content, and records rather than renderer convention. The closure-backed walk still uses the fixture-injected closure input noted under R2/R3. |
| R12 | failed | `scenario.v1` requires provenance-shaped strings but does not resolve them or enforce package/bundle/year/jurisdiction agreement. The 2026 scenario demonstrates the gap by referencing 2025 bundle and symbol-binding content. A fresh reader can see labels, but cannot safely traverse verified scenario -> package -> facts -> rules -> citations -> form fields from this contract alone. |
| R13 | failed | All eight positives and all nine manifest negatives pass their declared modes. However, the attachment wrong-line, attachment wrong-year, and cross-year form-field negatives are valid under their schemas and fail only in helper code. There are no committed negatives for closure finding semantics, standard-eligibility finding semantics, tax-method finding semantics, source-instance/correction identity, or the form-field-to-output-symbol line mismatch. The manifest therefore does not satisfy the requirement for every new or materially changed family/relationship. |

## Required distinctions

- **Fact type, fact, finding:** the bundle has fact types, and committed examples
  have an entity and findings. The finding `fact_id` is opaque and is not
  checked against the declared identity keys. The scenario-to-run path does not
  preserve the W-2 instance identity. The distinction is named, but not
  demonstrated as an authoritative identity chain.
- **Form field, output symbol:** the form-field schema declares a one-way
  `binds_symbol` bridge, but a field changed from line 1a to line 2b remains
  schema-valid and passes the current citation helper. The hard distinction is
  therefore not validated.
- **Computed zero, closure-backed zero, guard/non-existence:** this is the
  strongest part of the exhibit. The two zero walks differ by their pins, and
  blocked-invalid, blocked-unclosed, and false-guard states terminate at
  distinct record entries. The closure pin is still based on the direct input
  projection rather than a scenario-derived closure finding.

## Overall assessment

The exhibit has good narrow content evidence for R7, R9, R10, and R11, and its
declared limitations are more honest than an unconditional pass would be. The
green 203-check harness result does not close R1-R4, R6, R12, or R13. R3 is a
contract-boundary issue because load-bearing machinery is still supplied outside
authoritative findings; R9 is ordinary implementation breadth because its
omitted methods are explicitly guarded and blocked. I do not find sufficient
expressiveness evidence to treat the full R1-R13 checklist as closed.
