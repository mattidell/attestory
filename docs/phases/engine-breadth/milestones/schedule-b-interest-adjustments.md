<!-- foreman-context-v1
{
  "version": 1,
  "topic": "schedule-b-interest-adjustments",
  "milestone_state": "closed",
  "status": "CLOSED 2026-08-03. The bounded 2025 Schedule B interest-adjustment path is synthetic complete through line 2b, Schedule B Part I, package resolution, explanation, and presentation. Schedule D remains outside scope; the immutable v6 EOF formatting warning is deferred in the retrospective.",
  "retrospective": "docs/milestone-retrospectives/2026-08-03-schedule-b-interest-adjustments.md",
  "scope": [
    "support the bounded 2025 Schedule B Part I adjustment class for nominee distributions, accrued interest paid to a bond seller, and taxable amortizable-bond-premium adjustments",
    "preserve the existing positive-interest source-family composition and make every new adjustment source explicit, closed, and independently explainable",
    "carry the bounded adjustment result through Form 1040 line 2b, Schedule B Part I, downstream results, explanation, package/release resolution, and synthetic presentation evidence",
    "keep the product independent of Schedule D and transaction-domain capital-gain machinery"
  ],
  "non_goals": [
    "no Schedule D, Form 8949, Form 1099-B, Form 1099-DA, capital transactions, gains, losses, carryovers, basis, or securities-history completeness",
    "no OID adjustment, tax-exempt bond-premium adjustment, frozen-deposit reduction, savings-bond interest previously reported, early-withdrawal penalty, or unrelated income domain",
    "no taxpayer-side accrual or bond-premium calculation; the bounded class accepts an explicitly contributed adjustment amount and its authority, not the underlying investment computation",
    "no filing, transmission, real-data operation, UI redesign, or personal values"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/schedule-b-interest-adjustments.md#Official 2025 paper boundary",
      "docs/phases/engine-breadth/milestones/schedule-b-interest-adjustments.md#Contracts",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0026-taxable-interest-composition-and-line-2b.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/content/tax/2025/interest-composition.v3.json",
      "packages/content/tax/2025/rule.form1040-line2b.v3.json",
      "packages/content/tax/2025/rule.attachment.schedule-b.v3.json",
      "packages/content/tax/2025/package.core-calculations.v10.json",
      "packages/content/tax/2025/published-packages.v5.json",
      "packages/sample_data/market_discount_interest/adoptions/adopt-core-v10-current.json",
      "packages/sample_data/market_discount_interest/publication_surface/releases/demo.release.2025.v5.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/schedule-b-interest-adjustments.md#Contracts",
      "docs/phases/engine-breadth/milestones/schedule-b-interest-adjustments.md#Builder and reviewer verification package",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0026-taxable-interest-composition-and-line-2b.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
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
      "docs/milestone-retrospectives/2026-08-03-schedule-b-interest-adjustments.md"
    ]
  }
}
-->
# Milestone: Schedule B Interest Adjustments

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner on 2026-08-02.

## Objective

Make one additional valid-return class computable end to end: a 2025 federal
return whose taxable interest includes a Schedule B Part I subtraction for a
nominee distribution, accrued interest paid to a bond seller, or a taxable
amortizable-bond-premium adjustment.

The milestone is independent of Schedule D. It stays within the existing
interest and Schedule B domain: positive interest remains authoritative through
the current seven-family composition, while explicit nonnegative adjustment
amounts reduce the taxable-interest result only after their own authority and
closure are complete.

## Current state

The current adopted synthetic graph is
`tax.us.2025.package.core-calculations@v10` through
`published-packages.v5`, `demo.release.2025@v5`, and the current
`adopt-core-v10-current` adoption. Its positive interest composition is v3,
its line-2b rule is v3, its line-2b field is v4, and its Schedule B content is
v3. These are the selected versions to inspect mechanically at readiness.

The current positive-interest composition intentionally has no adjustment
universe. The next slice therefore needs a separate, explicit adjustment
authority and explanation boundary rather than silently accepting negative
members into an existing positive family.

After the branch was rebased onto `origin/main`, the main line's published
attachment-rule.v3/v4 and artifact-package.v7/v8 histories were preserved, as
were the branch's already-published attachment-rule.v5 and
artifact-package.v9/v10/v11. This milestone therefore uses attachment-rule.v6,
artifact-package.v12, package.core-calculations.v15, published-packages.v10,
release v8, and adoption v15 as its current successors. The older v10/v5
route remains a compatibility
baseline; Schedule D content already present in main remains outside this
milestone's scope.

The final adopted synthetic graph is `tax.us.2025.package.core-calculations@v15`
through `published-packages.v10`, `demo.release.2025@v8`, and
`adopt-core-v15-current`. The bounded result is synthetic-complete; the
milestone does not claim real-data coverage or support for excluded neighboring
domains.

## Official 2025 paper boundary

The paper checkpoint is grounded in the 2025 Schedule B instructions and 2025
Publication 550:

- Schedule B Part I line 1 reports all taxable interest, including interest
  shown on Forms 1099-INT and 1099-OID.
- A nominee distribution is listed below the line-1 subtotal and subtracted
  from it.
- Accrued interest paid to the seller when a bond is bought between interest
  dates is listed below the subtotal and subtracted because that amount is
  taxable to the seller.
- A taxable amortizable bond premium reduction is identified as an “ABP
  Adjustment” and subtracted when the taxpayer elects to reduce taxable
  interest; no second reduction is allowed when the payer already reported a
  net amount.

The supported boundary is an explicitly contributed, nonnegative adjustment
amount with a cited authority surface. The engine does not determine nominee
ownership, recompute accrued interest, calculate bond-premium amortization, or
decide whether a taxpayer's election was available.

The paper checkpoint must settle whether the three classes can share one
adjustment-member and closure contract while retaining class-specific labels,
citation identity, and source evidence. If they cannot, the Foreman stops and
splits the milestone before implementation.

## Track 0 record — paper boundary and contract checkpoint

Date: 2026-08-02. Result: **complete; Track 1 may begin.**

The 2025 paper distinguishes the three selected classes as separate adjustment
authorities that share a common downstream operation: each is a nonnegative
amount listed below the positive-interest subtotal and subtracted once. The
classes therefore keep separate fact types, source families, closure/declaration
surfaces, citations, and labels, while a successor line-2b rule may combine
their three subtotals with the existing `subtract` expression vocabulary.

| Class | Positive paper instances | Meaningful negatives | Lifecycle trace | Producer → authority → consumer → failure |
| --- | --- | --- | --- | --- |
| Nominee distribution | Form 1099-INT interest received in the taxpayer's name for another owner; Form 1099-OID interest received as nominee | No nominee authority supplied; negative adjustment amount | Corrected assertion for the same logical nominee instance replaces its predecessor; a late nominee member displaces the prior closure | Statement-backed contribution → nominee declaration and family closure → nominee subtotal, line 2b subtraction, Schedule B “Nominee Distribution” row → absent closure, negative value, or unsupported source family blocks |
| Accrued interest | Interest statement containing interest on a bond bought between payment dates plus an accrued-interest amount paid to the seller; a second distinct seller-paid adjustment | No evidence/authority that the taxpayer paid the seller; adjustment greater than the authorized positive-interest basis | Corrected seller-paid amount replaces the same logical adjustment; a late adjustment advances only the accrued-interest horizon | Contribution tied to the interest statement → paid-to-seller declaration and closure → accrued-interest subtotal, line 2b subtraction, Schedule B “Accrued Interest” row → absent payment authority, negative value, or overage blocks |
| Taxable ABP adjustment | A taxable-bond amortizable-premium reduction claimed against a Form 1099-INT interest amount; a second distinct payer-reported ABP amount | Payer already reported net interest; tax-exempt premium presented as taxable ABP | Corrected ABP claim replaces the same logical adjustment; a late claim displaces the prior closure | Payer-reported premium plus taxpayer claim → taxable/elected/not-netted authority and closure → ABP subtotal, line 2b subtraction, Schedule B “ABP Adjustment” row → net-payer double reduction, tax-exempt route, or negative value blocks |

The three classes use separate adjustment authorities rather than one generic
fact with a free-form kind. This preserves ADR-0016's per-family claim and
keeps a closed-empty class from authorizing a neighboring adjustment. The
downstream reducer is shared only after the three class subtotals are each
closed.

The existing attachment contract cannot express the selected presentation.
`packages/schemas/tax/attachment-rule.v2.schema.json` admits only
`row_sets` whose operation is `collect_members`, whose values are summed as
positive rows, and whose whole-part tie-out is that positive sum. The runner
implements that same positive-only behavior. A new immutable
`attachment-rule.v6` schema is therefore required for explicit adjustment rows
and a signed/typed whole-part tie-out; the existing v2 schema and content stay
unchanged. This is a schema successor, not a mutation of published history.

No rival prototype is required at this checkpoint. The paper settles the
authority split, the existing rule language already contains `subtract`, and
the v2 schema inspection provides direct falsifiable evidence that reuse is
insufficient. The Builder must stop if v5 requires semantics beyond the
bounded adjustment-row and tie-out shape stated in SIA-C4.

## Streamlined milestone process

- **Paper scope check:** required as Track 0. It must produce two positive
  instances, two meaningful negatives, one lifecycle trace, and a
  producer → authority → consumer → failure map for each adjustment class.
- **Rival prototypes:** skipped only if the paper check and existing
  `subtract` expression vocabulary settle the shape. If the paper leaves a
  consequential alternative between a shared adjustment contract and separate
  class contracts, stop for an owner checkpoint and a prototype plan.
- **Build:** split into a sequential schema gate and integrated build. Track 1A
  settles and verifies the bounded immutable `attachment-rule.v6` successor,
  its manifest append, package admission, and focused runtime/validation seam.
  Only after Track 1A is complete may Track 1B implement source/admission,
  adjustment composition, line 2b, Schedule B, package adoption, lifecycle,
  explanation, and presentation. Track 1B may parallelize only disjoint
  adjustment-family content and isolated fixtures after the Track 1A contract
  is fixed.
- **Review:** one independent integrated Reviewer after a clean exact-range
  handoff.
- **Repair:** at most one bounded findings-only repair cycle assigned to the
  same Builder. A second substantive defect or any scope-expanding finding
  returns to the owner.
- **Scope contract:** Contracts below become binding only after Track 0 records
  that the paper boundary and expression/attachment shape are honest. A need
  to interpret governance or a reserved ontology entry is a stop.

## Scope

- Add distinct 2025 adjustment facts and authority for nominee distributions,
  accrued interest paid to a seller, and taxable amortizable-bond-premium
  adjustments.
- Give each adjustment class an explicit source/authority boundary and a
  closure or contributable declaration so an absent adjustment is never
  inferred merely from a missing member.
- Publish the successor line-2b computation that subtracts the closed total of
  authorized adjustments from the current positive taxable-interest total,
  with a fail-closed result when an adjustment universe is incomplete or an
  adjustment exceeds its authorized positive-interest basis.
- Publish the Schedule B Part I successor that preserves positive line-1
  itemization and renders the named adjustment rows below the subtotal with
  exact labels and tie-out to line 2b.
- Publish the coherent package/release/adoption successor and prove that the
  v10/v5 route remains resolvable and unchanged.
- Add synthetic identity/admission, closure, correction or replacement,
  positive/negative adjustment, line-2b, Schedule B, package, explanation, and
  one production-shaped positive presentation golden through
  `live_coordinate_run`.

## Non-goals

- Schedule D, Form 8949, Form 1099-B, Form 1099-DA, capital transactions,
  gains/losses, carryovers, basis, disposition income, or securities-history
  completeness.
- OID adjustment, tax-exempt bond-premium adjustment, frozen-deposit
  reduction, savings-bond-interest-previously-reported reduction,
  early-withdrawal penalty, seller-financed mortgage interest, or other
  Schedule B Part I adjustments not named in Scope.
- Calculation of nominee ownership, accrued interest, bond-premium
  amortization, election eligibility, or any underlying transaction amount.
- New evaluator operations, filing/transmission behavior, UI redesign, a
  real-data operation, or an unrelated income domain unless Track 0 proves the
  existing contracts cannot express the selected class; that discovery is a
  stop and owner checkpoint, not automatic scope expansion.
- Mutation, reformatting, movement, deletion, or checksum rewriting of any
  published schema, historical content citizen, package, release, adoption,
  or existing synthetic golden.

## Contracts

### SIA-C1 — Three explicit adjustment classes

Create independent nonnegative adjustment member types for:

1. nominee distribution amounts belonging to another person;
2. accrued interest paid to the seller of a bond bought between interest dates;
3. taxable amortizable bond premium reductions, admitted only where the
   taxpayer's authority says the reduction is being claimed and the payer did
   not already net the amount.

The exact citizen shape is settled by Track 0. The expected identity is a
logical tax-year plus adjustment-instance identity; evidence, file, upload,
scan, and document identifiers never become the fact key. A corrected
assertion supersedes the same logical adjustment instance; two original
adjustments remain distinct. Negative adjustment inputs are rejected
atomically.

### SIA-C2 — Closed adjustment universe

Each class must authorize only its named adjustment surface and expose a
current closure or explicit contributable declaration. A closed-empty class is
an honest zero. A late member advances only the affected horizon and displaces
the adjustment total, line 2b, Schedule B, and downstream consumers until a
successor declaration closes the class again.

No class closure claims that all interest is adjusted, that the underlying
investment calculation is complete, or that any Schedule D or transaction
condition has been satisfied.

### SIA-C3 — Positive interest less explicit adjustments

The successor line-2b producer must read the current seven-family positive
interest total and the exact adjustment-class totals, require every relevant
closure, and publish the stable taxable-interest symbol. Its expression must
use the already accepted `subtract` vocabulary or a separately reviewed
successor contract; no direct runtime computation is authorized.

The contract must define the fail-closed behavior when the authorized
adjustments exceed the positive-interest basis they reduce. No negative taxable
interest value may be silently published as a convenience.

### SIA-C4 — Schedule B Part I adjustment presentation

Schedule B Part I continues to itemize the positive source families on line 1,
then renders explicit adjustment rows below the line-1 subtotal. The adjustment
rows use the exact paper labels “Nominee Distribution,” “Accrued Interest,”
and “ABP Adjustment,” and the final Part I result ties exactly to the stable
taxable-interest symbol.

Track 0 must determine whether the existing `attachment-rule.v2` contract can
represent signed presentation semantics without ambiguity. If not, the plan
requires a new versioned attachment schema and its registry manifest append;
the existing published schema remains immutable.

Part II, the $1,500 strict-greater-than requirement, Part III presence
semantics, citation identity, and attachment-only tie-out containment remain
unchanged unless a named contract test proves otherwise.

### SIA-C5 — Package, explanation, and presentation route

Publish one coherent successor package/release/adoption route. Expected
successor surfaces are package v15, published registry v10, release v8, a
successor line-2b producer, and the Schedule B/content or schema successor
settled by Track 0. The v12 graph selects one current version of every
adjustment family, closure, subtotal, line-2b producer, Schedule B producer,
and unchanged consumer.

`live_coordinate_run` is the authoritative production-shaped integration
surface. Explanations expose each adjustment through its authority, label, and
subtractive path; presentation redacts rejected or blocked derived values
using the existing generic behavior. One canonical positive golden is
authoritative; any malformed variant is a compact in-test mutation.

### SIA-C6 — Stop conditions and historical compatibility

Stop before implementation or adoption if paper or readiness reveals a need
for Schedule D, transaction/basis machinery, an unsupported source claim, a
new evaluator operation not accepted by the current rule language, a
governance interpretation, a reserved ontology entry, a mixed package graph,
or mutation of published history. Route the discovery to an owner checkpoint.

## Readiness inventory

Before editing, the Builder must mechanically inspect the selected current
versions rather than relying on published files:

| Surface | Selected base | Expected successor |
| --- | --- | --- |
| Adoption | rebased main package v14 / registry v9 route | `adopt-core-v15-current`: package v15, release v8 |
| Release | main's current release → registry SHA for `published-packages.v9` | `demo.release.2025.v8` → registry SHA for `published-packages.v10` |
| Positive interest | composition v3; line-2b rule v3; line-2b field v4 | same positive composition plus explicit adjustment route |
| Schedule B | attachment-rule.v2 / content v3 | content successor, or a new attachment schema version if Track 0 requires it |
| Source families | seven positive families and their closures/subtotals | three bounded adjustment classes with independent authority and closure |
| Runtime seam | existing `subtract` evaluator and `live_coordinate_run` graph | unchanged unless a stop condition is met |

## Builder and reviewer verification package

### Positive and boundary cases

| ID | Scenario | Required observation |
| --- | --- | --- |
| SIA-P1 | One nominee distribution with all positive families and adjustment classes closed | Schedule B shows the positive amount on line 1, the nominee row below the subtotal, and line 2b publishes the reduced total |
| SIA-P2 | One accrued-interest adjustment | The seller-paid amount is subtracted once with its own citation and is not treated as a negative source member |
| SIA-P3 | One taxable ABP adjustment | The payer-reported/elected reduction is subtracted once and the net-payer case is outside the accepted adjustment path |
| SIA-P4 | Multiple adjustment classes on one return | Each class remains separately explained and the combined reduction ties exactly to line 2b |
| SIA-P5 | No adjustments, all adjustment declarations closed empty | Existing positive-interest result remains unchanged; no adjustment row is inferred |
| SIA-P6 | Same logical adjustment corrected | The correction displaces the prior adjustment and recomputes line 2b and Schedule B |
| SIA-P7 | Adjustment triggers Schedule B despite positive interest below $1,500 | Existing requirement logic and the new Part I rows remain honest |
| SIA-P8 | Historical v10/v5 adoption | The prior package route resolves with prior behavior and bytes |
| SIA-P9 | One production-shaped positive presentation run | `live_coordinate_run` produces one committed golden with exact adjustment labels/citations and no rejected value |

### Honest-block and rejection cases

| ID | Mutation or condition | Required observation |
| --- | --- | --- |
| SIA-N1 | Adjustment class is unclosed | Line 2b and dependent results block; no adjustment is inferred as zero |
| SIA-N2 | Late adjustment after closure | The old adjustment total and consumers leave current state until the successor closure is present |
| SIA-N3 | Negative adjustment or evidence-key identity | Admission rejects atomically with no partial state |
| SIA-N4 | Adjustment exceeds the authorized positive-interest basis | The result blocks or reports the named contract failure; it never publishes silent negative taxable interest |
| SIA-N5 | ABP payer already reported net interest | A second reduction is rejected or honestly outside the supported class |
| SIA-N6 | Schedule B adjustment row omitted, duplicated, mislabeled, or mismatched | Attachment/package validation rejects or contains only the attachment with the named tie-out code |
| SIA-N7 | Line-2b producer omits an adjustment closure, value reference, or citation pin | Package validation refuses the graph |
| SIA-N8 | Mixed v10/v11 or old/new Schedule B producer graph | Resolver/package validation refuses the mixed graph |
| SIA-N9 | OID adjustment, tax-exempt premium, frozen deposit, or transaction-shaped input | The input remains outside the class; no neighboring mechanism is invented |
| SIA-N10 | Rejected or malformed derived adjustment reaches presentation | Existing generic redaction and section containment hold; no copied full-size malformed model |
| SIA-N11 | Published schema, manifest, or historical package mutation | Registry/history checks refuse the change or the Builder stops before adoption |

### Reviewer attack checklist

The independent Reviewer must answer:

1. Does the paper boundary distinguish nominee, accrued-interest, and ABP
   adjustments rather than collapsing unlike authority surfaces?
2. Is every adjustment explicitly contributed and closed, with no inference from
   absence and no direct-read bypass around source authority?
3. Does the line-2b producer subtract only the exact adjustment classes and
   preserve the stable positive-interest composition?
4. Does Schedule B show line-1 positive sources and line-2 adjustment rows with
   exact labels, citations, and a single tie-out to line 2b?
5. Are corrections, late members, closed-empty declarations, and adjustment
   overages handled fail-closed?
6. Does the package/release/adoption route use mechanically selected versions,
   preserve v10/v5 compatibility, and avoid mutating published history?
7. Is the positive golden authoritative through `live_coordinate_run`, with
   generic negative presentation evidence credited without copied models?
8. Did any implementation broaden into Schedule D, transactions, OID
   adjustments, tax-exempt premium, unrelated income, or new UI behavior?

## Fixtures

Use only synthetic committed fixtures with `demo.*` or `demo-*` identities and
no absolute local paths. Add focused scenarios for each adjustment class,
combined adjustments, closed-empty and late-member lifecycle, corrections,
overage/negative rejection, Schedule B threshold, historical v10/v5 resolution,
and one production-shaped positive presentation golden.

Reuse generic presentation negatives. If an adjustment-specific malformed
value is useful, mutate the canonical model in memory or commit only the
compact mutation needed by the named consumer. Report authored contract,
runtime, and test volume separately from generated or expanded artifacts.

## Verification

Track 0 must record the paper evidence and the exact decision about the
adjustment and attachment shapes before implementation. Expected focused
commands after implementation are:

```text
python3 -m unittest tests.test_schedule_b_interest_adjustments_contracts
python3 -m unittest tests.test_schedule_b_interest_adjustments_integration
python3 -m unittest tests.test_schedule_b_interest_adjustments_schedule_b
python3 -m unittest tests.test_schema_registry
python3 -m mypy
git diff --check
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range <planning-tip>..HEAD
```

Run only touched existing modules while iterating. Ordinary integration
evidence uses `live_coordinate_run`; direct `RunContext` is reserved for
attachment-only kill cases that cannot be exercised through the normal path.
CI `verify` remains the gate of record.

## Economy measurements

The Builder handoff and Reviewer record must report Orientation Block words and
bytes, tool calls, wall time, authored contract/runtime/test lines and bytes,
generated or expanded artifact lines and bytes separately, first-review
verdict, and repair count.

## Data safety

No personal or real tax data is needed. All values, identities, acts,
workspaces, reports, presentations, and goldens are synthetic and publishable.
No personal source document, real return, absolute local path, private output,
or derived personal artifact may enter the repository, branch, review, chat, or
handoff.

## Exit criteria

The milestone is complete when Track 0's paper boundary is recorded; SIA-P1
through SIA-P9 and SIA-N1 through SIA-N11 have committed evidence or reviewer-
accepted stronger-case equivalence; the bounded adjustment class computes end
to end through line 2b and Schedule B; historical package/release routes remain
immutable and compatible; the Reviewer returns `READY` or one repair pass is
independently rechecked; the closing PR's `verify` is green and owner-merged;
and the frontier, roadmap, phase state, and retrospective record only the
bounded synthetic result.

## Tracks

### Track 0 — Paper boundary and contract checkpoint

The Foreman records the paper instances, negatives, lifecycle traces, and
producer → authority → consumer → failure maps for all three adjustment
classes. The track decides whether a shared adjustment contract and the
existing expression vocabulary are sufficient. If not, it stops and routes a
split milestone or prototype plan to the owner.

### Track 1A — Shared attachment schema contract gate

The Builder first adds the immutable `attachment-rule.v6` successor required
for typed adjustment rows and whole-part tie-out, appends its checksum using
the schema registry writer, and extends only the package-admission and runtime
dispatch seams needed to prove the bounded shape. The Builder must preserve
`attachment-rule.v2`, prove the manifest diff is append-only, run the schema
registry and focused attachment consumer tests, and stop if the shape needs
new evaluator semantics or any unplanned contract. No adjustment fact family,
downstream composition, package successor, release/adoption successor, or
canonical golden is in scope for this gate.

Track 1B may begin only after Track 1A is committed and independently accepted.
The Track 1A review is a separate gate from the later integrated Track 1B
review; it may not be inferred from the Builder's focused test results.

### Track 1A repair — owner-authorized package-schema successor

The same Builder may make one repair pass limited to the review's F1/F2
findings: bind each v5 kind to its exact paper label and class authority, add
compact mutation coverage for all three classes, add immutable
`artifact-package.v11` as the successor to the rebased package-schema history,
append its derivation-schema manifest checksum, and demonstrate v5 package
admission at the package boundary. All existing published package-schema
versions remain unchanged. The package/release/adoption content
successors for the full Schedule B implementation remain Track 1B work. No
new adjustment family, evaluator operation, unrelated schema, or golden is
authorized. Track 1B remains blocked until the repair is independently
re-reviewed and returns `READY`.

The package-schema repair was completed and independently re-reviewed before
the integrated Track 1B build began.

### Track 1B — Integrated adjustment source-to-content build

After Track 1A settles the shared schema contract, one Medium/medium Builder implements the
adjustment facts, authority/closure, successor line-2b computation, Schedule B
content/schema seam, package graph, lifecycle tests, and focused contract
evidence. The Builder verifies the selected-version inventory before editing.

## Review gate

The Builder adds the production-shaped positive presentation golden and
`live_coordinate_run` evidence. An independent Reviewer measures the complete
case matrix and compatibility boundary. At most one findings-only repair pass
returns to the same Builder; any second substantive defect or scope expansion
returns to the owner.

### Track 2 — Closeout

After the final track merges, the Foreman performs the required closeout:
retrospective, frontier and roadmap status, phase-state closed pointer, data
safety scans, and successor selection state.
