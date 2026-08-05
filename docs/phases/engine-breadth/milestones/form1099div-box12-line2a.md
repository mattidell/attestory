<!-- foreman-context-v1
{
  "version": 1,
  "topic": "form1099div-box12-line2a",
  "milestone_state": "closed",
  "status": "CLOSED. The bounded 2025 Form 1099-DIV box-12 to Form 1040 line-2a route is synthetic complete and independently reviewed READY; the route remains independent of Schedule D.",
  "retrospective": "docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md",
  "scope": [
    "promote Form 1099-DIV box 12 into an independent closed source family and aggregate it to Form 1040 line 2a",
    "replace the active 1099-DIV residual recording shape additively while preserving historical bundles and package routes byte-for-byte",
    "make line 2a complete only with explicit absence authority for every excluded tax-exempt source, premium adjustment, and excluded downstream dependency",
    "carry the bounded result through correction lifecycle, package/release/adoption resolution, explanation, and the existing presentation surface",
    "preserve existing boxes 1a, 1b, 2a, taxable interest, Schedule B, and Schedule D behavior"
  ],
  "non_goals": [
    "no Form 1099-DIV box 13 computation, Form 6251, or general AMT support",
    "no Form 1099-INT tax-exempt boxes, Form 1099-OID tax-exempt interest or OID, unreported tax-exempt interest, or premium adjustments",
    "no state or municipal return treatment, taxable Social Security, child-income elections, credits, deductions, filing, transmission, real-data operation, or UI redesign",
    "no Schedule B or Schedule D changes",
    "no claim that tax-exempt interest has no effect outside the bounded supported graph"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md#Official 2025 paper boundary",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md#Contracts",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0035-dividend-composition-and-lines-3a-3b.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/content/tax/2025/f1099div.bundle.json",
      "packages/content/tax/2025/f1099div-box2a.bundle.json",
      "packages/content/tax/2025/dividend-universe.json",
      "packages/content/tax/2025/package.core-calculations.v15.json",
      "packages/content/tax/2025/published-packages.v10.json",
      "packages/sample_data/schedule_b_interest_adjustments/adoptions/adopt-core-v15-current.json",
      "packages/sample_data/schedule_b_interest_adjustments/publication_surface/releases/demo.release.2025.v8.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md#Contracts",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md#Evidence matrix",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0035-dividend-composition-and-lines-3a-3b.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol",
      "PROJECT_PLANNING.md#Milestone Closeout"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md",
      "docs/milestone-retrospectives/2026-08-03-schedule-b-interest-adjustments.md",
      "docs/phases/engine-breadth/milestones/schedule-b-interest-adjustments.md"
    ]
  }
}
-->
# Milestone: Form 1099-DIV Box 12 to Form 1040 Line 2a

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner on 2026-08-03. This milestone is
independent of the active Schedule D inbound-carryover work.

## Objective

Make one bounded 2025 return class computable end to end: one or more Form
1099-DIV statements report nonnegative box-12 exempt-interest dividends, those
dividends are the return's only tax-exempt-interest source, and the complete
selected amount is reported on Form 1040 line 2a.

The result is a reported-but-not-directly-taxable line. It must not enter Form
1040 line 9 or taxable-income arithmetic, and the milestone must not claim
general tax-exempt-interest support.

## Current state

The accepted Form 1099-DIV graph has independent box-1a and box-1b families,
the recorded/non-composable box shape, and an additive box-2a successor that
removed box 2a from its residual member. The current residual successor still
records boxes 3, 5, 7, and 12; the historical v1 residual and its package
routes are immutable.

The adopted synthetic route on the ratified line was the Schedule B successor
graph. This milestone's additive successors are
`tax.us.2025.package.core-calculations@v17`, `published-packages.v12`,
`demo.release.2025@v10`, and `adopt-core-v17-current`; the package uses
`artifact-package.v14`. The predecessor package and published registry remain
byte-immutable. The final rebase and semantic-ledger check preserved both the
milestone delta and intervening Schedule D work.

Existing dividend, taxable-interest, Schedule B, and Schedule D behavior is a
compatibility boundary. The new line-2a graph is a new consumer path; it does
not alter Schedule B or Schedule D.

## Official 2025 paper boundary

The tax routing is grounded in current official sources:

- [2025 Form 1040 instructions, line 2a](https://www.irs.gov/instructions/i1040gi)
  direct exempt-interest dividends from Form 1099-DIV box 12 to line 2a,
  while also identifying tax-exempt stated interest, OID, and premium routes
  that this milestone excludes.
- [Instructions for Form 1099-DIV](https://www.irs.gov/instructions/i1099div)
  define box 12 as exempt-interest dividends from a mutual fund or other RIC,
  and state that specified private-activity-bond interest dividends in box 13
  are included in box 12.
- [Publication 550 (2025)](https://www.irs.gov/publications/p550),
  “Reporting tax-exempt interest” and “Exempt-interest dividends,” direct the
  total of box 12 and other tax-exempt-interest sources to line 2a, state that
  exempt-interest dividends are not taxable income, and route box 13 to AMT
  treatment without adding it to box 12 a second time.

The supported source class is exactly: tax year 2025; one or more nonnegative
Form 1099-DIV box-12 amounts; box 13 absent or zero with explicit authority
for every statement; no Form 1099-INT or Form 1099-OID tax-exempt source; no
unreported tax-exempt interest; no tax-exempt bond or acquisition premium
adjustment; no excluded downstream consumer of tax-exempt interest; and
otherwise supported unrelated income only.

## Track 0 — Gate-1 decision inventory and paper evidence

Track 0 is paper-first. The scores below use the four Gate-1 axes (future
blast radius, migration cost, residual uncertainty after paper examples, and
inability to test cheaply during implementation), each from 0 to 2. Gate 2
requires two positive instances, two meaningful negatives, one lifecycle
trace, and a producer → authority → consumer → failure map for each
proposition. If paper distinguishes the shape, the track stops at paper and
no rival prototype is created.

| Proposition | Blast | Migration | Paper uncertainty | Cheap-test gap | Total | Planned disposition |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P1. Historical residual succession and package exclusivity | 2 | 2 | 1 | 1 | 6 | Paper first; likely one additive residual successor plus mixed-graph rejection; draft one new contract ADR only if ADR-0035 is insufficient |
| P2. Box-12 family identity, independent closure, and correction lifecycle | 2 | 1 | 1 | 1 | 5 | Paper spike plus ADR disposition; reuse ADR-0015/0016/0017 if no new semantics are needed |
| P3. Smallest complete line-2a composition boundary | 2 | 2 | 2 | 1 | 7 | Paper compares one-family-plus-explicit-scope-authority with additive slots; prefer the former if it names every excluded source and downstream dependency |
| P4. Box-13 included-in-box-12 and AMT boundary | 1 | 1 | 1 | 0 | 3 | Implementation contract; nonzero box 13 blocks and never invokes Form 6251 |
| P5. Reported-only downstream graph semantics | 2 | 1 | 1 | 1 | 5 | Paper plus existing explanation/presentation contracts; line 2a is excluded from line 9 and taxable income |
| P6. Exact pins, stale closure, restoration, and reach-around rejection | 1 | 1 | 1 | 0 | 3 | Implementation contract and adversarial tests |

Gate-0 discipline: P1 is the primary contract proposition; P2 and P3 are its
tightly dependent secondaries. P4–P6 are implementation-boundary obligations,
not additional rival-design topics. If paper cannot distinguish P1–P3,
implementation stops and the owner receives a choice between a bounded
prototype plan, a split milestone, or deferral.

### Paper evidence plan

For P1, use a historical residual-only statement, a successor-family-only
statement, a mixed package, and a same-statement double-adoption mutation. The
map is: residual/family fact → package exclusivity and family closure → box-12
subtotal → mixed graph or double-count rejection.

For P2, use one payer, two payers, a corrected statement with the same logical
identity, and a late member after closure. The map is: payer/statement fact →
box-12 family horizon closure → subtotal → open, stale, or superseded
consumer.

For P3, use a positive box-12-only return and meaningful negatives containing
each excluded tax-exempt source class. Compare the candidate compositions on
paper. The expected smallest shape is one box-12 subtotal gated by a single
explicit `line-2a-scope-completeness` authority whose payload names: Form
1099-INT tax-exempt source absent; Form 1099-OID tax-exempt stated/OID source
absent; unreported tax-exempt interest absent; bond/acquisition premium
adjustment absent; and excluded downstream dependency absent. The authority
does not claim those sources are computed.

Track 0 records the exact paper instances, negatives, lifecycle trace, maps,
Gate-1 disposition, citation URLs, and proposed ADR outcome before any
implementation charter.

### Track 0 record — paper settled 2026-08-04

The paper examples distinguish the selected shape, so no rival prototype is
created. The values below are synthetic paper values only.

| Proposition | Positive instances | Meaningful negatives | Lifecycle trace | Producer → authority → consumer → failure |
| --- | --- | --- | --- | --- |
| P1 residual succession | `demo.payer.alpha` historical residual box-12 `100`; successor box-12 member `100` with residual `{3:null,5:null,7:null}` | historical residual plus successor family in one package; same statement reachable through both shapes | old package remains resolvable; successor package adopts only residual-v3 plus box-12 family | statement member → package exclusivity/residual-v3 → box-12 subtotal → mixed graph or double-count rejection |
| P2 family identity/closure | one payer/one statement `100`; two payers/statements `100` + `40` | open closure; stale closure after a late statement | corrected `100` to `125` keeps payer/statement/year identity; late second statement advances the family horizon; restoration closes the successor horizon | logical statement fact → box-12 family horizon → subtotal/line 2a → open, stale, or superseded consumer |
| P3 line-2a boundary | box-12-only return with explicit all-slots-absent scope authority; closed-empty box-12 family with the same authority | Form 1099-INT tax-exempt source, Form 1099-OID tax-exempt source, unreported source, premium adjustment, or excluded downstream dependency present; missing scope authority | scope authority is corrected/superseded as a tax-year declaration; line 2a leaves current state until the successor authority is current | box-12 subtotal + scope authority → line-2a composition → complete value or honest block |
| P4 box 13 | box 13 explicit null; box 13 explicit `0` | box 13 explicit positive value; missing companion authority | corrected box-13 witness follows the same logical statement identity | box-12 statement + box-13 witness → line-2a guard → publish or block; never Form 6251 |
| P5 downstream semantics | line 2a `140` with line 9/taxable income unchanged; explanation marks reported-but-not-directly-taxable | child-income/Social Security/credit/deduction consumer present | excluded consumer stays blocked/nonpublished while the bounded full-return claim is unavailable | line-2a field → zero-authority presentation and explanation; excluded consumer → honest nonpublication |
| P6 pins/lifecycle | subtotal and line 2a carry family, mapping, horizon, closure, completeness, and citation pins | missing pin; raw historical reach-around; restored old closure consumed after successor horizon | correction displaces prior finding; stale closure displaces consumers; restoration recomputes | exact attribution chain → resolver/explanation/presentation → resolved value or pin/closure rejection |

The paper comparison for P3 is settled in favor of one-family composition plus
one explicit `line-2a-scope-completeness` authority. The alternative additive
multi-slot composition would require implementing or independently closing
every unimplemented Form 1099-INT, Form 1099-OID, non-form, and premium slot;
it costs more while adding no supported source. The selected authority names
each excluded slot and downstream dependency without pretending to compute it.

P1 and P2 reuse the accepted logical statement, per-family claim, and horizon
contracts. P4 uses a companion witness tied to the same statement and does not
create an AMT source. P5 preserves the existing zero-authority presentation
projection and makes excluded consumers block explicitly. P6 is an exact-pin
and lifecycle implementation obligation.

**Track 0 disposition:** the plan's B12-C1 through B12-C7 contracts, together
with accepted ADR-0015, ADR-0016, ADR-0017, ADR-0020, ADR-0027, ADR-0029,
ADR-0033, ADR-0035, and ADR-0046, are sufficient for this bounded route. No
new ADR is required by the paper decision. Any implementation discovery that
requires a new product contract stops and returns to the owner; no accepted
ADR is edited.

## Proposed contract and ADR disposition

Existing accepted ADRs remain unchanged. ADR-0015 supplies payer/statement/year
identity; ADR-0016 supplies per-family claims and independent composition;
ADR-0017 supplies horizon succession; ADR-0020 and ADR-0029 supply explanation
and semantic citation pins; ADR-0027 and ADR-0033 supply package/adoption
exclusivity and verified resolution; ADR-0035 supplies the dividend-family
pattern; ADR-0046 supplies presentation behavior.

Track 0 should produce one new Tier-2/Tier-3 ADR only if paper shows that the
box-12 residual succession and bounded line-2a completeness authority are
future-facing contracts not fully stated by those ADRs. The ADR number and
filename are deliberately unreserved until the final rebase because the
concurrent Schedule D milestone may publish a successor. If the accepted ADRs
plus this plan fully express the shape, record the decision in this plan and
the retrospective instead. No accepted ADR is edited.

## Scope

- Add an independent 2025 Form 1099-DIV box-12 amount fact keyed by payer,
  logical statement, and tax year, with nonnegative admission and correction
  semantics.
- Add its source family, horizon, closed-empty behavior, subtotal, mapping,
  and citation surface; aggregate multiple payers without collapsing identity.
- Add an additive residual recorded-box successor containing boxes 3, 5, and 7
  only. Preserve historical residual v1 and the current successor shape
  byte-for-byte and reject package graphs that adopt box 12 through both a
  historical residual and the successor family.
- Add explicit per-statement box-13 absence/zero authority. A present nonzero
  box 13 blocks the bounded route; Form 6251 is not implemented.
- Add one explicit line-2a scope/completeness authority naming every excluded
  tax-exempt source, premium adjustment, and excluded downstream dependency.
  The line-2a rule composes only the closed box-12 subtotal and requires this
  authority.
- Publish versioned line-2a composition, rule, citation, and form-field
  citizens; carry the graph through explanation and the existing presentation.
- Publish additive package, published-registry, release, and adoption
  successors after the final collision inventory.
- Prove line 2a is not collected by line 9 or taxable-income arithmetic.
- Preserve accepted boxes 1a, 1b, 2a, taxable interest, Schedule B, and
  Schedule D behavior with unmodified regression fixtures.

## Non-goals

- Form 1099-DIV box 13 computation, Form 6251, AMT, or specified
  private-activity-bond calculation.
- Form 1099-INT box 8 or other tax-exempt-interest boxes; Form 1099-OID
  tax-exempt stated interest or OID; unreported/non-form tax-exempt interest;
  or tax-exempt bond/acquisition-premium adjustments.
- State or municipal returns; taxable Social Security; child-income elections;
  credits or deductions using modified AGI that includes tax-exempt interest;
  or any downstream consumer not named in the bounded graph.
- Schedule B changes, Schedule D changes, Form 8949, filing, transmission,
  real-data operation, and UI redesign.
- A claim that line 2a is universally informational or tax-exempt interest
  has no effect outside the current supported graph.
- Mutation, reformatting, movement, deletion, or checksum rewriting of any
  published schema, historical content citizen, package, release, adoption,
  fixture, or accepted ADR.

## Contracts

### B12-C1 — Independent box-12 family

Use `payer + statement + tax-year=2025`; the statement identity carries no
file, upload, scan, document, or evidence key. The proposed amount fact is a
nonnegative scalar source amount with a named quantity and exact box-12
citation. Corrections supersede the same logical statement; two originals from
the same payer remain distinct.

The family closure is keyed to its current family horizon and covers box 12
only. It closes independently of boxes 1a, 1b, 2a, and residual boxes. A
closed-empty family is an explicit zero; absent closure is not zero. The
subtotal sums all current members across multiple payers and cannot read
historical residual content.

### B12-C2 — Residual succession and exclusive adoption

Historical `tax.us.2025.f1099div.recorded-boxes` v1 and the current successor
that still contains box 12 remain immutable. Add a new residual version whose
properties are exactly boxes 3, 5, and 7. The selected package adopts that
residual and the independent box-12 family, never an old residual that
contains box 12.

Package validation rejects old residual plus box-12 family in one graph, a
same-statement contribution that reaches the subtotal through both shapes, a
raw/historical reach-around, and any mixed historical/successor residual
graph. The historical package route remains resolvable and byte-unchanged.

### B12-C3 — Box-13 authority without AMT computation

Each box-12 statement item carries an explicit companion authority for box 13:
absent or numeric zero is admissible; a present nonzero value is a hard block.
No missing companion is treated as absent. The companion is an authority
witness, not a composed amount or a Form 6251 input. Correction/restoration
supersedes/restores the same logical statement authority with the box-12 member.

### B12-C4 — Smallest complete line-2a boundary

The preferred shape is one explicit 2025 `line-2a-scope-completeness`
authority with separately named absence assertions for every unimplemented
tax-exempt source and premium adjustment, plus absence of child-income,
Social Security, AMT, credit, deduction, or other downstream consumer that the
current graph does not implement.

The line-2a composition is:

```text
line-2a = closed box-12 subtotal
```

only when the box-12 family closure, every box-13 absence/zero witness, and
the scope-completeness authority are current. The authority does not claim
any excluded source was computed. Missing, stale, contradictory, or
false/present excluded slots block the bounded line-2a claim. If Track 0 proves
that one authority cannot preserve per-slot diagnostics or closure semantics,
stop and return to the owner before adding multiple source-family slots.

### B12-C5 — Reported-only downstream semantics

The line-2a form field and finding publish with exact source, mapping, closure,
completeness, horizon, and citation pins. The line-2a symbol is not an input
to line 9, taxable income, or currently supported taxable-income arithmetic.
A positive fixture must show line 2a changing while line 9 and taxable income
remain unchanged.

When an excluded downstream dependency is present, the affected downstream
finding is blocked/nonpublished with its authority reason. The graph never
describes line 2a as universally informational merely because the positive
fixture leaves taxable income unchanged.

### B12-C6 — Exact pins and lifecycle

The box-12 subtotal pins the box-12 family identity, member-to-subtotal
mapping, current family horizon and closure, box-13 authority, and Form
1099-DIV box-12 citation. The line-2a producer and field pin the box-12
subtotal, family closure, scope-completeness authority, tax-year horizon,
mapping identity, and Form 1040 line-2a citation. Corrections displace prior
findings; stale closure displaces consumers; restoration re-establishes the
current graph; raw/historical reach-arounds are rejected.

### B12-C7 — Package, release, adoption, and presentation

The final graph resolves through one verified package, published registry,
release, and adoption successor. It is exclusive: one current source family,
closure, subtotal, line-2a producer, field, explanation citation, and
presentation route. Old packages remain resolvable.

Use `live_coordinate_run` for one canonical positive presentation golden. The
golden shows the actual line-2a value, the reported-but-not-directly-taxable
explanation, and the authority/citation walk. Negative presentation cases use
compact in-memory mutations and existing block/redact behavior.

## Exact citation and authority pins

Create repository citation citizens with stable semantic anchors:

| Pin purpose | Official source and anchor |
| --- | --- |
| Line-2a routing and excluded premium/OID routes | IRS, 2025 Form 1040 instructions, “Line 2a—Tax-Exempt Interest,” `https://www.irs.gov/instructions/i1040gi` |
| Box-12 meaning and box-13 inclusion | IRS, Form 1099-DIV instructions, “Box 12. Exempt-Interest Dividends” and “Box 13. Specified Private Activity Bond Interest Dividends,” `https://www.irs.gov/instructions/i1099div` |
| Aggregation, non-taxable treatment, and AMT distinction | IRS, Publication 550 (2025), “Reporting tax-exempt interest” and “Exempt-interest dividends,” `https://www.irs.gov/publications/p550` |

Every subtotal and line-2a field also pins family, mapping, horizon, closure,
completeness authority, and the relevant citation citizen. URL-only payload
strings are insufficient; citation resolution follows ADR-0029.

## Readiness and version-collision checkpoints

Before implementation, the Builder mechanically verifies the selected graph
and real entrypoint. Immediately before final implementation packaging, and
again before PR curation:

1. Fetch/prune origin and identify the latest ratified line with the repository
   resolver; do not compare against a guessed line.
2. Inventory every published tax schema, artifact-package schema, package,
   published registry, release, adoption, and relevant presentation artifact
   version on that line and this branch.
3. Rebase onto the latest ratified line and repeat the inventory.
4. Choose unused successor filenames and discriminators only after rebasing;
   preserve every ratified file and manifest row byte-for-byte.
5. Verify package exclusivity, registry checksums, release hashes, adoption
   pins, and historical-route compatibility before handoff.

The current v15/v10/v8/v15 values are not reservations. If the concurrent
Schedule D milestone lands first, its phase state, roadmap, frontier,
retrospective pointers, package history, and schema versions survive the
rebase; this milestone adds successors and never restores an older state.

## Evidence matrix

All cases use synthetic identities and values. Existing regressions remain
unmodified.

| ID | Case or mutation | Expected result |
| --- | --- | --- |
| P1 | One payer with box 12 | Closed family subtotal and line 2a publish the exact amount |
| P2 | Multiple payers | Statements remain distinct; subtotal aggregates exactly once |
| P3 | One statement with boxes 1a, 1b, and 12 | Existing line 3a/3b behavior remains; line 2a adds only box 12 |
| P4 | Box 12 alongside the accepted direct box-2a route | Line 7a/Schedule D behavior is unchanged; line 2a is independent |
| P5 | Box-12 family closed empty | Explicit zero publishes; missing closure does not |
| P6 | Missing, open, stale, corrected, and restored closure | Consumers leave current state until successor closure; correction preserves identity; restoration recomputes |
| P7 | Box 13 absent and box 13 zero | Both admissible with explicit authority |
| N1 | Box 13 nonzero | Honest block; no Form 6251 is created |
| N2 | Form 1099-INT tax-exempt source present | Scope authority fails; bounded line-2a result blocks |
| N3 | Form 1099-OID tax-exempt source present | Scope authority fails; bounded line-2a result blocks |
| N4 | Unreported/non-form tax-exempt interest present | Scope authority fails; no inference or omission |
| N5 | Tax-exempt bond/acquisition premium adjustment present | Scope authority fails; no premium computation |
| N6 | Missing excluded-source declaration | Line 2a blocks; absence is never assumed |
| N7 | Excluded downstream dependency present | Affected downstream result is blocked/nonpublished; no universal informational claim |
| N8 | Historical residual plus successor family adoption | Package/adoption validation rejects double adoption |
| N9 | Raw/historical reach-around or mixed residual graph | Resolver/package validation rejects the graph |
| N10 | Correction with same logical identity | Prior statement finding is superseded, not double-counted |
| N11 | Existing boxes 1a, 1b, 2a, taxable interest, Schedule B, Schedule D | Focused regressions pass with behavior unchanged |
| P8 | Positive line-2a presentation | Actual value, citation, authority, and reported-only explanation render |
| N12 | Malformed/blocked presentation model | Existing fail-loud/block/redact behavior holds without copied full golden |

## Tracks and review structure

### Track 0 — Paper boundary and contract checkpoint

Foreman-owned. Record Gate-1 scores, paper instances, negatives, lifecycle
traces, maps, exact citations, and ADR disposition. Stop at paper if it
distinguishes the shape. No rival prototype is authorized.

### Track 1 — Integrated production build

After owner approval and Track 0, one integrated Builder implements the source
family, residual successor, box-13 authority, completeness boundary, line-2a
composition/field, package/release/adoption graph, explanation, presentation
golden, and tests. If existing evaluator, marshal, package, or presentation
substrate cannot express the settled paper shape, the Builder stops and
returns the issue to the owner rather than expanding scope.

## Review gate — Integrated independent review

One author-independent Reviewer measures contract fidelity, double-adoption
risk, completeness honesty, box-13/AMT boundary, downstream nonpublication,
package collisions, exact pins, and all evidence-matrix regressions. The
Reviewer reports a falsifiable `READY` or numbered findings.

### Repair and closeout

At most one bounded findings-only repair cycle is available to the same
Builder. A second substantive defect, new product decision, or scope expansion
returns to the owner. One findings-only repair addressed production-path
box-13 companion enforcement; the independent re-review returned READY.
Working charters and interim records are removed at final curation; this plan
and the retrospective preserve durable decisions.

## Durable commit structure

1. `plan: select Form 1099-DIV box 12 to line 2a` — this plan, planned phase
   state, roadmap selection, and frontier split; no implementation.
2. `track-0: record box-12 and line-2a paper boundary` — paper evidence and
   ADR disposition after owner approval.
3. `track-1: implement bounded box-12 line-2a route` — integrated production
   implementation and focused tests/fixtures.
4. Provisional review/repair commits, folded into Track 1 before curation.
5. A closeout commit with retrospective, curated records, final state, and no
   temporary briefing capsule. The closed plan remains the re-entry pointer
   until the owner selects the next milestone.

No schema, package, release, registry, adoption, or ADR number is reserved
before the rebase checkpoints.

## Fixtures, verification, economy, and data safety

Committed fixtures use synthetic `demo.*` identities, nonnegative sample
values, and no absolute paths, personal documents, real facts, dispositions,
or private outputs. Use one canonical positive presentation golden and compact
in-memory negative mutations. While iterating run only touched modules. The
final focused set includes source-family/admission, lifecycle, composition,
package/resolver, explanation, presentation, and dividend/interest/Schedule
B/Schedule D regression modules, plus `tests.test_schema_registry` when
schemas or manifests change. Typed changes run `python3 -m mypy`; final checks
include `git diff --check`, governance lint, envelope scan, and CI `verify`.
Named positives enter through `live_coordinate_run`.

Builder and Reviewer handoffs report Orientation Block words/bytes, wall time,
turns, tool calls, authored versus generated lines/bytes, first verdict, and
repair count. Personal source documents, current-year facts, prior returns,
real values, identifiers, credentials, workspaces, screenshots, and generated
personal artifacts remain outside the repository, branch, review, chat, and
output.

## Exit criteria

Track 0 paper evidence settles the contract shape; the one-family line-2a
composition is implemented; positive and negative cases are evidenced; box 13,
other tax-exempt sources, excluded dependencies, missing declarations, stale
closures, corrections, restoration, and double adoption fail honestly; line 9
and taxable income remain unchanged; existing dividend, interest, Schedule B,
and Schedule D regressions pass; explanation, presentation, package, release,
registry, and adoption resolve; historical files remain byte-identical; the
independent review returns READY with at most one repair cycle; CI is green;
and the owner merges the single curated milestone PR.
