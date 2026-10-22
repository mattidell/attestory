# Bounded Track 0 dynamic-account candidate

Status: the v50-derived disposable candidate package validates; the supported
pair and both A/B ceiling-collision inputs reached the actual coordinator.
This is bounded synthetic evidence, not a Track 0 closure finding, production
recorder proof, or proof for the four remaining lifecycle cases.

## What was validated

### Historical v49-base structural and runtime observations

The earlier structural four-count candidate resolved at
`temp/mortgage-statement-borrowing/t0-dynamic-binding-20261022T145900Z`.
It was not combined with the later dynamic-account runtime candidate; its
four-count/status composition therefore remains unproved in the runtime.

The first dynamic supported-pair coordinator case ran on the now-historical
v49-derived candidate at
`temp/mortgage-statement-borrowing/t0-dynamic-binding-20261022T151819Z`.
That disposable package was v55 with 469 resolved members. It must not be
treated as current-base proof. Its one run produced two ledger records
(started and completed), not two runs.

### Current-base v50 result

The current candidate explicitly started from adopted core package v50,
registry `published-packages.v48.json`, and source release v48, preserving the
current tax-rule and parameter members. The T0 disposable successor uses core
package v56, candidate registry `published-packages.t0-p56.json`, and bridge
release v6. The normal production resolver succeeded with 494 resolved
members at
`temp/mortgage-statement-borrowing/t0-dynamic-binding-20261022T172122Z`.
The full disposable members/releases surface, source package/registry/release,
final package/registry/release, synthetic supplied acts, and durable consumer
artifacts are retained there. `declaration-check.json` contains hashes for
the core v50 source package/registry/release and the v56 candidate chain.
The saved `coordinator-report.json`, `presentation-model.json`, and
`synthetic-records.json` SHA-256 values are respectively
`d7cad665eed52457cc9575c16a4917e114cbf653a329927721457c87e7131709`,
`fa006278d3de4e612a872c82faee3225d0f705d6a96f338e3029807e650039b9`, and
`36546064a3e7a6bf8886c658a339ce2ba2409a07cc032b7f6e6ac89929fb01ac`.

The supported-pair case ran once (two ledger rows: started and completed) and
completed without refusal. It published mortgage line8a at **$11,000** and
Schedule A total; line12e published **$15,750**, matching the standard
deduction and exceeding the $11,000 itemized total. The saved model and record
show the v56 adoption, line12e rule v2, standard-deduction rule v2, and
`tax.us.2025.parameter.standard-deduction-base` v1. In the run output, the
standard-deduction disposition pins that parameter; the selected line12e
finding pins line12e v2 and the v56 package. The v56 package retains the
rebased line16 rule v6 and selected preferential-base rule v5. The line16
consumer was blocked by unrelated missing inputs in this fixture, so no line16
execution is claimed. The saved mortgage explanation retains the incumbent
$750,000 conservative limit pin and exact report provenance. The inherited
P2 fixture run identifier includes its old `v51` label, but the current saved
finding and publications pin the v56 package adoption.

The P2 materializer now accepts explicit base package, registry, candidate
registry, and source-release selectors while preserving its old v49/v47/v47
defaults for historical P2 runs. This current T0 invocation selected v50/v48/v48.

An earlier structural-only candidate added four distinct exact-outcome facts: affirmed, denied,
unresolved, and withdrawn. For each, a v13 rule declares Box1 as subject,
that outcome as joined, `joined_contains_subject`, and one numeric
`link_count` in `value`. Each publishes a numeric count with the Box1
`payer + statement + tax-year` keys. A fifth per-Box1 rule requires the four
numeric outputs and classifies zero total as `none`, one total as that unique
outcome, and any other total as `conflict`. The existing v14 readiness
selection declared a `reads_subject_results` read of that fifth result.
That composition resolved at
`temp/mortgage-statement-borrowing/t0-dynamic-binding-20261022T145900Z`.
The later v55 supported-pair increment does not yet include or consume that
four-count/status composition; it still reads P2's affirmative membership
status. Combining these two increments remains unproved.

The supplied synthetic acts include two Box1 reports with full payer,
statement, and year keys; both affirmatively link to opaque borrowing A, and
only A has the continuing-borrowing root, annual-ceiling fact, and other-home
secured-debt fact. That prototype other-debt fact is still borrowing-keyed;
the production contract requires return/year scope, which this run does not
demonstrate. The fixture also includes the mortgage-specific zero pin
for empty support. This is the supported pair only; it does not prove all
seven transitions, unprovided source facts, authorized final-recording behavior,
or broad consumer compatibility.

The v56 run establishes that the current-base candidate rule declarations,
rebased non-mortgage content, and retained P3 consumer successors are
structurally admitted together by the existing resolver. Package/release
version numbers here are disposable candidate lineage, not reservations or
published-content claims.

### Ceiling-collision cases on the current v56 candidate

Both cases used the same validated v56 candidate and supplied explicit
structured borrowing/year keys. Each case had one coordinator run (two record
rows: started and completed); the positive case above was not replayed. Raw
acts, candidate content/hashes, and case artifacts are retained at
`temp/mortgage-statement-borrowing/t0-dynamic-binding-20261022T172816Z/`.

1. **A ceiling absent; B ceiling $300,000.** The input retained A's
   continuing-borrowing affirmation, both current report-to-A links, A's
   other-debt answer, and all report-local facts; it removed only A's annual
   ceiling and supplied B's ceiling under the explicit key
   `borrowing=demo.f1098.borrowing.B, tax-year=2025`. B's $300,000 ceiling is
   within the $750,000 limit and above both Box 2 observations ($240,000 and
   $220,000), so the blocker is not that B's value is unsuitable. Package
   validation resolved. The coordinator completed with line8a blocked on the
   missing `demo.tax.2025.mortgage.same-borrowing-ready`; Schedule A total was
   blocked on line8a and line12e on Schedule A total. The account-ceiling
   selection for A was blocked on its missing A-keyed ceiling, while B did not
   supply that join. This confirms no favorable dependent mortgage amount is
   selected from B. However, the saved P3 temporary model's `sharedSupport`
   incorrectly displays B's $300,000 ceiling alongside A's recognition and
   other-debt facts. Thus the derivation gate is keyed correctly, but this
   overlay is not safe evidence of shared-support display in a collision.

2. **A ceiling $250,000; dormant B ceiling $900,000.** B has no recognition
   claim or report link. Package validation resolved, and the coordinator
   published line8a at $11,000, Schedule A total, and line12e. The exact
   account-ceiling-selected result is keyed to continuing-borrowing A and pins
   A's raw ceiling act (`demo.mortgage.p2.annual-ceiling`) plus A's recognition;
   no B ceiling appears in that derivation lineage. The line8a publication is
   $11,000 and pins both report Box 1 inputs plus the current readiness
   finding. The completion record also says line12e was published under v56
   and line12e rule v2; its finding ID matches the saved positive result, whose
   value was $15,750. The current collision run's numeric line12e value is not
   directly retained: P3's overlay failed before saving its report/model,
   raising `P3 expected one current shared support finding for
   demo.tax.2025.mortgage.annual-ceiling` because two raw annual-ceiling claims
   were current. The durable completion records and in-memory line8a
   publication are retained, but this case has no durable coordinator report
   or presentation model.

For audit, case 1's raw-acts, report, model, and records hashes are
`8e99b6e7be1308a4454d05fd549db38737f4bfbf1978bf70f329e4160fb12730`,
`beff0018a1860233776df2fddd837722f40c90aa1e4806d4bc9ddfb26ea9c83d`,
`4500eb5989a30a49f95f17da308b367df9e157bab21c534a55e51bcdf9586dcb`, and
`f5e3287094610f956eca61e9fceeb7e0a1aee19300434d6e6a745312b1088f3f`.
Case 2's raw-acts, completion-records, and in-memory line8a publication hashes
are `f3cd9f76251a6ad1949fb2c4eafe64d9886aa82285b3b638c28ee10a9b5684d6`,
`31ed9d4f5b02293be1d2c548019f69dbf257d25239dd94cf1418207a83665ee8`, and
`8582fe1979f001f5f4d184970613fba258e79440c83af3b5d34fe22b33a38770`.

## What remains unproved

The next authorized work remains the four lifecycle/empty/orphan cases and
four-outcome status integration. Although the two A/B derivation boundaries
are now observed, the P3 shared-support overlay visibly misassociates B's
ceiling when A's is absent and rejects two current ceilings instead of
selecting A. This presentation-path limitation is separate from the successful
keyed derivation lineage. The remaining runtime evidence does not yet establish
withdrawn-current status being load-bearing, affirmed orphan handling,
closed-empty behavior with only retired outcomes, or the other connected
singleton and correction transitions.

## Validation attempts

Earlier candidate attempts were rejected for composition issues, including
unreachable intermediate rules, invalid selection dependencies, and an
unupdated package-adoption release binding. These were repaired in the
candidate; none demonstrates an engine limitation. The successful current
run is the first complete dynamic-account supported-pair result.
