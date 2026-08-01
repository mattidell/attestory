<!-- foreman-context-v1
{
  "version": 1,
  "topic": "market-discount-interest",
  "milestone_state": "closed",
  "status": "CLOSED. The bounded 2025 payer-reported current-inclusion market-discount interest implementation is synthetic complete after one bounded findings-only repair; the owner-authorized re-review returned READY and the closing PR verify check is green.",
  "retrospective": "docs/milestone-retrospectives/2026-08-01-market-discount-interest.md",
  "scope": [
    "support nonnegative market-discount amounts reported by a payer in 2025 Form 1099-INT box 10 or Form 1099-OID box 5 when the amount is already currently includible as taxable interest under a section 1278(b) election",
    "preserve separate source-family authority for the Form 1099-INT and Form 1099-OID reporting routes and require closure of both families in the adopted positive-interest composition",
    "carry both source families through Form 1040 line 2b, composition-complete Schedule B Part I, downstream results, exact citations, package/release resolution, and production-shaped synthetic presentation evidence",
    "reuse the K-1 milestone's positive-interest composition and multi-family Schedule B machinery without adding an evaluator mechanism, attachment schema/runtime, or presentation behavior",
    "preserve every historical schema, content citizen, package, registry, release, adoption fixture, and accepted ADR byte-for-byte"
  ],
  "non_goals": [
    "no disposition-time market discount, Form 1099-B or Form 1099-DA transaction reporting, partial principal payments, taxpayer-side accrual calculations, basis adjustments, or general securities history",
    "no market discount that is not already payer-reported in Form 1099-INT box 10 or Form 1099-OID box 5 as current inclusion",
    "no nominee interest, accrued-interest-at-purchase adjustment, bond-premium or acquisition-premium adjustment, other subtractive interest mechanism, or broader transaction domain",
    "no Schedule D, Form 8949, Form 1099-B, unrelated income domain, filing, transmission, real-data run, or UI redesign",
    "no new evaluator mechanism, attachment schema/runtime, or presentation behavior; discovery of a need for one stops the charter and returns the scope to an owner checkpoint",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema or historical versioned citizen",
    "no personal values, identifiers, dispositions, workspace locations, documents, screenshots, or generated private artifacts"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/reviews/charter-2026-07-31-k1-interest-breadth-builder.md",
      "docs/phases/engine-breadth/milestones/market-discount-interest.md#Official 2025 paper boundary",
      "docs/phases/engine-breadth/milestones/market-discount-interest.md#Contracts",
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
      "packages/content/tax/2025/interest-composition.v2.json",
      "packages/content/tax/2025/rule.form1040-line2b.v2.json",
      "packages/content/tax/2025/rule.attachment.schedule-b.v2.json",
      "packages/content/tax/2025/form1040.line-2b.form-field.v3.json",
      "packages/content/tax/2025/package.core-calculations.v9.json",
      "packages/content/tax/2025/published-packages.v4.json",
      "packages/sample_data/k1_interest_breadth/adoptions/adopt-core-v9-current.json",
      "packages/sample_data/k1_interest_breadth/publication_surface/releases/demo.release.2025.v4.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/reviews/charter-2026-07-31-k1-interest-breadth-review.md",
      "docs/reviews/charter-2026-08-01-market-discount-interest-builder.md",
      "docs/phases/engine-breadth/milestones/market-discount-interest.md#Contracts",
      "docs/phases/engine-breadth/milestones/market-discount-interest.md#Builder and reviewer verification package",
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
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
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
      "docs/milestone-retrospectives/2026-08-01-market-discount-interest.md",
      "docs/phases/engine-breadth/engine-breadth-overview.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/phases/engine-breadth/milestones/market-discount-interest.md"
    ]
  }
}
-->
# Milestone: Payer-Reported Current-Inclusion Market-Discount Interest

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner 2026-08-01.

## Objective

Make one additional valid-return class computable end to end: an individual
2025 federal return containing payer-reported market-discount amounts that are
already currently includible as taxable interest.

The class covers both reporting routes: Form 1099-INT box 10 for a covered
security acquired with market discount and no OID reporting route, and Form
1099-OID box 5 for a covered security acquired with OID. Each amount enters a
separate source family with its own closure, both families participate in the
successor positive-interest composition, and the resulting total reaches Form
1040 line 2b, Schedule B Part I, downstream calculations, explanation, package
resolution, and presentation.

## Current state

The current adopted synthetic graph is `tax.us.2025.package.core-calculations@v9`
through `published-packages.v4`, `demo.release.2025@v4`, and the current
`adopt-core-v9-current` adoption. Its selected interest composition is v2,
its line-2b rule is v2, its line-2b field is v3, and its Schedule B attachment
rule is v2. These are the selected versions to verify mechanically at build
readiness; separately published versions are not evidence of selection.

ADR-0026 defines the current positive-interest composition and explicitly
defers market discount. The K-1 milestone established the reusable successor
composition and generic multi-family Schedule B contract. This milestone adds
two source families and two row sets to that settled machinery; it does not
redesign the evaluator, attachment schema/runtime, or presentation projection.

## Official 2025 paper boundary

The paper check supports both boxes, with mutually exclusive payer routing for
covered securities with OID:

- [Instructions for Forms 1099-INT and 1099-OID](https://www.irs.gov/instructions/i1099int), Box 10, direct the payer to report market discount accrued during the tax year for a covered security when the recipient notified the payer of a section 1278(b) election, and direct the payer to use Form 1099-OID instead when the covered security has OID.
- The same instructions, Form 1099-OID Box 5, direct the payer to report the accrued market discount for a covered security acquired with OID under the same election/reporting condition.
- [Publication 1212 (December 2025)](https://www.irs.gov/publications/p1212) identifies Form 1099-OID box 5 as the market discount includible in income when the holder elects current inclusion and notifies the broker, and explains the covered-security reporting route.
- [Publication 550 (2025)](https://www.irs.gov/publications/p550) identifies Form 1099-INT box 10 and Form 1099-OID box 5 as the payer-reported market-discount amounts to report on the income tax return.
- [2025 Form 1040 instructions](https://www.irs.gov/instructions/i1040gi) route total taxable interest, including market discount, to line 2b, and [2025 Schedule B instructions](https://www.irs.gov/instructions/i1040sb) require all taxable interest, including includible accrued market discount, in Part I line 1.

The exact supported authority is therefore: every nonnegative amount in a 2025
Form 1099-INT box 10 or Form 1099-OID box 5 statement item, where the payer's
form represents market discount accrued during the year under the recipient's
section 1278(b) current-inclusion election and the amount is intended to be
reported as taxable interest. The engine accepts the payer-reported amount; it
does not calculate whether the election was available, recompute accrual,
determine covered-security status, or reconcile the amount to a transaction or
basis.

Completeness is statement-family closure, not securities-history closure:

- the Form 1099-INT box-10 family claims every furnished 2025 box-10 statement
  item in scope;
- the Form 1099-OID box-5 family claims every furnished 2025 box-5 statement
  item in scope; and
- each family has its own logical statement identity, member subtotal, and
  current family horizon. A closed empty family is an honest zero; a late
  statement advances that family horizon and displaces its consumers.

This boundary excludes disposition-time Form 1099-B/1099-DA amounts, partial
principal payments, taxpayer-side accrual calculations, basis or acquisition
premium adjustments, unreported market discount, general securities history,
and any transaction-domain completeness claim. If implementation discovers
that this payer-reported boundary cannot be honored without one of those
mechanisms, the Builder stops and the owner receives a new scope checkpoint.

## Streamlined milestone process

- **Paper scope check:** complete. Both Form 1099-INT box 10 and Form 1099-OID
  box 5 are admitted as separate source families under the boundary above.
- **Rival prototypes:** skipped. This is an imitation-successor build against
  accepted source-family, positive-composition, attachment, package, and
  presentation contracts; no competing product shape is selected.
- **Build:** one integrated Medium/medium Builder, unless the readiness or
  paper check reveals genuine new mechanism design. One integrated source,
  content, runtime seam, package, fixture, test, explanation, and presentation
  packet is expected.
- **Review:** one independent integrated Reviewer after the Builder hands off a
  clean exact range. The Reviewer returns one verdict and may report findings.
- **Repair:** at most one bounded findings-only repair cycle, assigned back to
  the same Builder. A second substantive defect or any scope-expanding finding
  returns to the owner rather than being absorbed.
- **Scope contract:** the Contracts section is binding for this milestone. No
  new ADR is planned. An accepted-contract conflict or governance question is a
  stop, not an implementation invitation.

## Scope

- Add dedicated 2025 Form 1099-INT box-10 and Form 1099-OID box-5 source facts,
  source families, closure mappings, subtotals, and citation content using the
  existing statement identity and contribution/lifecycle patterns.
- Publish the successor interest composition, line-2b rule, line-2b field,
  and Schedule B content with exactly seven positive-interest row sets: the
  five current K-1 composition families plus the two market-discount families.
- Publish the next coherent package/release/adoption route and prove historical
  v9/v4 compatibility.
- Add synthetic identity, correction, late-member, closure, composition,
  package, Schedule B, explanation, and presentation evidence.
- Commit one canonical production-shaped positive presentation golden. Reuse
  generic negative presentation evidence or express a new malformed case as a
  compact in-test mutation; do not copy a whole presentation model merely to
  change one field.

## Non-goals

- Schedule D, Form 8949, Form 1099-B, Form 1099-DA, transaction gains/losses,
  partial principal payments, disposition-time market discount, basis,
  acquisition premium, general securities history, and taxpayer-side accrual.
- Nominee interest, accrued interest paid to a seller, bond premium,
  acquisition premium, negative/subtractive adjustments, or any new adjustment
  arithmetic/explanation mechanism.
- Other market-discount situations not already represented by payer-reported
  2025 box 10 or box 5 current-inclusion amounts.
- Any new evaluator mechanism, attachment schema/runtime, presentation
  behavior, UI, filing, transmission, real-data operation, or unrelated income
  domain. Discovery of a need for one is a charter stop and owner checkpoint.
- Mutation of any published schema, historical content citizen, manifest entry,
  package v9 or earlier, registry v4 or earlier, release v4 or earlier, or
  existing synthetic adoption/golden.

## Contracts

### MD-C1 — Two payer-reported source families

Create two separate, horizon-closed source families:

1. `tax.us.2025.f1099int.b10` for the market-discount amount reported in Form
   1099-INT box 10; and
2. `tax.us.2025.f1099oid.b5` for the market-discount amount reported in Form
   1099-OID box 5.

Each family has a dedicated nonnegative taxable-interest fact type, subtotal,
closure mapping, family declaration, and IRS citation. Its fact identity uses
the existing statement-instance pattern: tax year + payer + logical statement
entity. Evidence, file, upload, scan, and document identifiers never enter the
fact key. Two original statements from one payer remain distinct; a corrected
copy of one logical statement supersedes its prior finding.

The two families claim only their named 2025 form box. Their closure claims do
not cover market discount on Form 1099-B/1099-DA, unreported amounts, other
1099 boxes, taxpayer calculations, disposition history, basis, or total taxable
interest. A negative amount fails atomically. A late member advances only the
affected family horizon and displaces the old closure and every consumer that
depends on it.

### MD-C2 — Seven-family positive-interest composition

Publish `tax.us.2025.interest-composition@v3` under the existing
`taxable-interest-composition.v1` schema. Its exact slot bijection is the five
current v2 constituents, unchanged, followed by:

6. Form 1099-INT box-10 market-discount subtotal; and
7. Form 1099-OID box-5 market-discount subtotal.

Publish the cited line-2b successor with exact references, pins, value refs,
and `require_closed` reads for all seven families. Package validation must
reject an omitted, duplicated, substituted, extra, or wrong-family slot and a
mixed v2/v3 producer graph. The stable taxable-interest symbol remains the
downstream input; no new evaluator operation is authorized.

### MD-C3 — Schedule B content successor using existing machinery

Publish `tax.us.2025.rule.attachment.schedule-b@v3` under the existing
`attachment-rule.v2` schema. Part I uses composition authority over composition
v3 and contains one row set for each of the seven declared positive-interest
families. Each row set uses the existing `collect_members` operation, the
family's canonical member fact type, and its family-authorized subtotal. The
combined Part I ties to the stable taxable-interest symbol.

Part II, the $1,500 strict-greater-than requirement, Part III presence
semantics, attachment dispositions, citation identity, and
`ITEMIZATION_TIE_OUT_VIOLATION` attachment-only failure containment remain
unchanged. No attachment schema or evaluator/runtime feature is expected.

### MD-C4 — Package, release, explanation, and presentation route

Publish one coherent successor route:

- `tax.us.2025.package.core-calculations@v10` under the existing
  `artifact-package.v6` schema;
- `published-packages.v5` with appended checksums only;
- `demo.release.2025@v5`; and
- a new obviously synthetic current adoption for package v10/release v5.

The v10 graph selects exactly one current version of the two source families,
their closures/subtotals/citations, interest composition v3, line-2b successor,
line-2b field successor, Schedule B content v3, and every unchanged consumer.
The existing v9/v4 graph remains resolvable and semantically compatible.

`live_coordinate_run` is the authoritative production-shaped integration
surface. Explanation and presentation expose the market-discount amounts only
through the derived line-2b and Schedule B results, with exact citation
identity. One positive golden is authoritative. Generic malformed-value
redaction and section containment are credited unchanged; any new malformed
case is a compact mutation in a test, not a copied model.

### MD-C5 — No-new-mechanism and compatibility stop

The implementation is additive. Stop before writing implementation if any of
the following occurs:

- paper authority requires a transaction, basis, election-eligibility, or
  taxpayer-side accrual evaluator;
- the two-box boundary cannot be represented as separate source families with
  existing statement identity and closure machinery;
- composition v3 or Schedule B v3 requires a new evaluator operation, a new
  attachment schema/runtime, or presentation behavior;
- a fully resolved positive schema/content instance cannot be written honestly;
- package v10 requires changing a historical checksum or selecting mixed
  producer versions; or
- implementation turns on governance interpretation, a reserved ontology
  entry, Schedule D, subtractive adjustments, another market-discount source,
  or an unrelated income domain.

Such a discovery is a charter stop and owner scope checkpoint. It is not an
automatic expansion of this milestone.

## Readiness inventory

Before editing, the Builder must mechanically inspect the current adoption,
release registry, package registry, and package member graph. The handoff must
record actual selected versions, not merely published versions, for:

| Surface | Selected base to verify | Expected successor |
| --- | --- | --- |
| Adoption | `adopt-core-v9-current`: package v9, release v4 | synthetic adoption for package v10/release v5 |
| Release | `demo.release.2025.v4` → registry SHA for `published-packages.v4` | release v5 → registry SHA for v5 |
| Interest composition | `tax.us.2025.interest-composition@v2` | `@v3`, seven exact slots |
| Line 2b producer | rule v2, stable `tax.us.2025.interest.taxable-total` | cited rule v3, same stable symbol |
| Line 2b field | form-field v3 | form-field v4, same line/symbol/citation chain |
| Schedule B | attachment-rule.v2 / content v2 | attachment-rule.v2 / content v3 with seven Part-I row sets |
| Package schema | artifact-package.v6 | unchanged artifact-package.v6 |
| Source families | four historical families plus Form-1065 K-1 box-5 family | two additional families, mappings, bundles, subtotals |

The inventory must also locate the current package-validation composition and
attachment admission seams, the current `live_coordinate_run` graph path, the
stable line-2b consumers, the K-1 Schedule B row-set tests, and the current
presentation golden generator. An omitted required seam is a charter stop.

## Builder and reviewer verification package

### Positive and boundary cases

| ID | Scenario | Required observation |
| --- | --- | --- |
| MD-P1 | One Form 1099-INT box-10 member with all seven families closed | Market-discount subtotal and line 2b publish the payer amount; downstream results and citations are current |
| MD-P2 | One Form 1099-OID box-5 member with all seven families closed | OID-route subtotal and line 2b publish the payer amount; it is not classified as ordinary OID box 1 or non-form interest |
| MD-P3 | One box-10 and one box-5 statement item | Both distinct families contribute once; the paper's OID routing remains represented as separate authority |
| MD-P4 | Existing interest plus market-discount amount | Line 2b sums distinct family subtotals and Schedule B Part I contains both payer rows |
| MD-P5 | Same payer, two original statements | Distinct logical statement identities both contribute exactly once |
| MD-P6 | Corrected box-10 or box-5 statement | Same logical identity supersedes the prior amount and downstream results rerun to the corrected value |
| MD-P7 | Both market-discount families closed empty | Composition publishes an honest unchanged zero/unchanged total; no inferred market-discount amount appears |
| MD-P8 | Market-discount amount crosses Schedule B threshold, and dividend-only trigger | Schedule B requirement and Part I itemization preserve existing threshold and multi-family behavior |
| MD-P9 | Historical package v9/release v4 adoption | Historical graph resolves and retains prior behavior and bytes |
| MD-P10 | One canonical production-shaped positive presentation run | `live_coordinate_run` produces one committed positive golden with exact line-2b/Schedule-B citations and no rejected value |

### Honest-block, lifecycle, and rejection cases

| ID | Mutation or condition | Required observation |
| --- | --- | --- |
| MD-N1 | Box-10 or box-5 family unclosed | Line 2b and dependent results block; no market-discount value publishes from an incomplete universe |
| MD-N2 | Late member after a current closure | Affected family horizon advances; old closure and consumers leave current state until successor closure and rerun |
| MD-N3 | Negative payer-reported amount | Contribution/admission fails atomically with no partial member or closure state |
| MD-N4 | Evidence/file/document identifier used as statement identity | Schema/admission rejects the identity substitution |
| MD-N5 | Composition v3 omits, duplicates, substitutes, or adds a slot | Package validation refuses the graph |
| MD-N6 | Line-2b successor omits a market-discount closure/value/pin or composition binding | Package validation refuses the producer graph |
| MD-N7 | Schedule B Part I omits, duplicates, or mispairs a market-discount row set | Package validation refuses before execution |
| MD-N8 | Stale market-discount row set disagrees with its subtotal | Schedule B alone blocks with `ITEMIZATION_TIE_OUT_VIOLATION`; line 2b remains published |
| MD-N9 | Combined Part-I total disagrees with line 2b | Schedule B alone blocks with the same attachment-only code; no divergent attachment publishes |
| MD-N10 | Mixed v2/v3 composition, line rule, field, or Schedule B producer | Resolver/package validation refuses the mixed graph |
| MD-N11 | Disposition-time/partial-principal/basis-shaped input is presented as box 10/box 5 current inclusion | The source contract rejects or leaves the neighboring transaction/basis case outside the supported class; no new mechanism is invented |
| MD-N12 | Rejected or malformed market-discount-derived value reaches presentation | Existing generic redaction and section containment hold; use a compact mutation rather than a copied golden |
| MD-N13 | Package manifest or historical citizen mutation | Registry/schema/history checks refuse the change or the Builder stops before adoption |

### Reviewer attack checklist

The independent Reviewer must answer:

1. Does the paper-grounded contract cover both boxes exactly, while preserving
   the IRS distinction that OID-reporting securities use Form 1099-OID box 5?
2. Is the engine trusting a payer-reported current-inclusion amount rather than
   silently calculating accrual, election eligibility, basis, or disposition?
3. Are source identity, correction, separate originals, family closure, and
   late-member displacement independently proved for both families?
4. Does composition v3 contain exactly seven families, and does line 2b require
   all seven current closures and pins?
5. Does Schedule B Part I contain exactly one row set per composition family,
   including both market-discount families, while all existing multi-family,
   tie-out, threshold, attachment-only, and Part III invariants remain valid?
6. Does the mechanical readiness inventory report selected package/release
   versions rather than relying on published files?
7. Are v10/v5 and the single positive golden authoritative through
   `live_coordinate_run` and the actual resolver?
8. Is generic negative presentation evidence credited without a copied model,
   and are authored contract/runtime/test changes reported separately from
   generated or expanded artifacts?
9. Did any code, content, fixture, or test broaden the milestone into
   disposition, basis, transaction history, subtractive adjustments, Schedule
   D, unrelated income, or presentation behavior?

## Fixtures

Use only synthetic committed fixtures with `demo.*` or `demo-*` identities and
no absolute local paths. Add a focused fixture family containing one box-10
return, one box-5 return, one mixed return, original/correction lifecycle
traces, closed-empty and late-member traces for both families, threshold and
tie-out mutations, v10/v5 resolution, and one production-shaped positive
presentation golden generated through `live_coordinate_run`.

Reuse generic presentation negative tests. If a market-discount-specific
malformed value is useful, mutate the canonical model in memory or commit only
the compact mutation needed by the named consumer. Generated/expanded artifact
volume must be reported separately from authored contract, runtime, and test
changes in the Builder handoff, Reviewer record, and retrospective.

## Verification

The integrated Builder must create focused tests named by MD-P/MD-N case IDs.
Likely commands are:

```text
python3 -m unittest tests.test_market_discount_interest_contracts
python3 -m unittest tests.test_market_discount_interest_integration
python3 -m unittest tests.test_market_discount_interest_schedule_b
python3 -m unittest tests.test_schema_registry
python3 -m mypy
git diff --check
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range <planning-tip>..HEAD
```

Run touched existing modules once, including the K-1 composition/Schedule B,
resolver, presentation, and line-2b compatibility modules that participate in
the successor graph. Do not rerun the full suite to confirm a deterministic
result; CI `verify` remains the gate of record. Ordinary integration evidence
must use `live_coordinate_run`; direct `RunContext` is reserved for impossible
tie-out kill cases.

## Economy measurements

The Builder handoff and Reviewer record must report Orientation Block bytes and
words, tool-call count, wall time, authored contract/runtime/test lines and
bytes, generated or expanded artifact lines and bytes separately, first-review
verdict, and repair count. These are process observations, not a weaker
product acceptance standard.

## Data safety

No personal or real tax data is needed. All values, identities, acts,
workspaces, reports, presentations, and goldens are synthetic and publishable.
No personal source document, real return, absolute local path, private output,
or derived personal artifact may enter the repository, branch, review, chat, or
handoff.

## Exit criteria

The milestone is complete when MD-P1 through MD-P10 and MD-N1 through MD-N13
have committed evidence or reviewer-accepted stronger-case equivalence; v10/v5
computes the bounded class end to end; Schedule B Part I is complete against
composition v3; historical content and package routes remain immutable and
compatible; the Reviewer returns `READY` or one repair pass is independently
rechecked; the closing PR's `verify` is green and owner-merged; and frontier,
roadmap, phase state, and retrospective record only the bounded synthetic
result.

## Execution record

| Unit | Result | Evidence |
| --- | --- | --- |
| Scope and contracts | Complete | Plan committed in the milestone branch; the paper boundary and MD-C1 through MD-C5 contracts remain binding. |
| Integrated build | Complete | One Medium/medium Builder on `milestone/market-discount-interest`; implementation and focused evidence landed in the branch. |
| Independent review | Initial `NOT READY`; re-review `READY` | `docs/reviews/review-2026-08-01-market-discount-interest.md`; the owner-authorized bounded re-review accepted both repairs and the unchanged product scope. |
| Repair | Complete | `docs/reviews/charter-2026-08-01-market-discount-interest-repair.md`; one findings-only repair removed the stale expectation and copied malformed model. |
| Closeout | Complete for closing PR | PR #134's replacement `verify` check is green; owner merge remains the ratification boundary. |

## Execution sequence

### Track 1 — Integrated source-to-presentation build

One Medium/medium Builder implements MD-C1 through MD-C5 in dependency order:
mechanical readiness inventory; source facts/families/closures; content
successors; package validation; lifecycle integration; one positive golden; and
focused tests. Keep separable commits when helpful, but do not create extra
role or PR gates.

### Integrated independent review

After a clean handoff, the Foreman files the exact-range Reviewer charter. The
Reviewer measures the contract, case matrix, compatibility, safety, selected
versions, and economy report, then returns one verdict.

### One bounded findings-only repair and closeout

Concrete findings may return to the same Builder for one bounded findings-only
repair cycle. The Reviewer rechecks changed behavior and adjacent invariants.
Any second substantive defect, new mechanism, or scope expansion returns to
the owner. The Foreman then performs milestone closeout records.
