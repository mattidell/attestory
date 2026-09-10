<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "nominee-interest-tax-consequence-supportability",
  "milestone_state": "closed",
  "status": "CLOSED 2026-09-09. A rule-owned, report-scoped nominee-interest reduction is derived from current attributed allocation assertions and executed through the real projection, marshalling, package, and run() boundary on package.core-calculations v36, for uniquely rendered identities. Remainder is observed only. The result is a RunResult publication, not act-log standing. It does not integrate Form 1040 line 2b or Schedule B, migrate the legacy nominee adjustment, normalize information-reporting law, or build UI, and it does not repair T0-F5, which remains a hard gate on the later legacy-and-return-integration stage. Completed: three independently reviewed planning gates, Track 0 paper contract closure, ADR-0074 accepted 2026-09-09 after independent review, Track 1 implementation with two owner-directed repairs, Track 2 live evidence independently reviewed READY with no blocking finding, and this closeout. Delivered: bound_sources on rule-artifact.v8 (not a collect, therefore outside ADR-0035's collect-family requirement); artifact-package.v28 and derivation-record.v9 with a no_groups_selected inapplicable branch schema-scoped to the nominee rule; package v36 with the nominee rule, reduction vocabulary, and citation, and no source-family or closure mapping for the allocation type; a tax-layer coordinator that owns grouping, year scope, C13, and per-report pins while the declared rule owns arithmetic. ADR-0074 narrows ADR-0020 Decisions 1/1a/4 for the exact rule id only. The result is bounded to identities that pass the execution-time ambiguity guard. T0-F5 and that substrate boundary (execution-time guard, not intake; two future options unchosen) are the next-stage input contract.",
  "scope": [
    "derive a rule-owned nominee-interest reduction and taxpayer remainder for one identified Form 1099-INT report from its current nominee-allocation assertions",
    "establish report-local supportability for zero, one, and several allocations, including whole-set blocking when the current allocations exceed their own report amount",
    "preserve correction, retraction, reassertion, cross-report isolation, and provenance through the real projection, marshalling, and execution boundaries",
    "keep the ownership-supported return consequence independent of payment or credit facts and retain the prior milestone's authority-indexed, unreconciled information-reporting boundary",
    "use independently reviewed planning checkpoints before Track 0, then independently review each implementation unit before the next begins"
  ],
  "non_goals": [
    "no Form 1040 line 2b, Schedule B attachment, form-field binding, or presentation integration and no repair of T0-F5 in this milestone",
    "no migration, conversion, retirement, or double-counting resolution for the legacy user-entered nominee adjustment",
    "no normalized nominee information-reporting predicate and no Forms 1096 or 1099-INT filing implementation",
    "no user-facing intake or explanation surface and no production caller for the still non-resumable multi-act allocation-recording operation",
    "no general ownership, allocation, person-identity, or collaboration model and no reopening of the selected report-linked allocation identity",
    "no conditional assumption, provisional-return standing, action-scoped authority, or source-family closure introduced merely to make aggregation convenient"
  ],
  "deep_reads": {
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Selected product behavior",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Planning review cycle",
      "docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md#Relationship to the following stages",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#The two consequences do not share one established predicate",
      "docs/adr/0009-derived-finding-shape.md",
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0068-acquisition-report-identity-association.md",
      "docs/adr/0070-accrued-amount-supportability-rule.md",
      "docs/adr/0071-rule-owned-current-year-and-basis-consequences.md",
      "docs/adr/0072-legacy-pairing-scoped-interest-coexistence.md",
      "docs/adr/0073-assertion-standing-and-retraction-lifecycle.md",
      "packages/tax/nominee_allocation_recording.py",
      "packages/tax/nominee_allocation_recovery.py",
      "packages/tax/supportability.py",
      "packages/tax/pairing_consequences.py",
      "packages/derivation/runner.py",
      "PROJECT_PLANNING.md#Lean Production Loop",
      "PROJECT_PLANNING.md#Track 0 Adversarial Closure Gate",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "OWNER_MODEL.md#The Product Model",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Plain-language purpose",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Selected product behavior",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Success and stop conditions",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-09-09-nominee-interest-tax-consequence-supportability.md"
}
-->

# Nominee Interest Tax Consequence and Supportability

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `nominee-interest-tax-consequence-supportability`
- Primary branch: `milestone/nominee-interest-tax-consequence-supportability`
- State: **CLOSED 2026-09-09**
- Roadmap role: second production stage of nominee-interest support

## Plain-language purpose

A bank may report `$1,200` of taxable interest under the taxpayer's
name while the taxpayer has recorded that `$450` belongs to another person. The
application preserves both pieces of evidence — what the bank reported and what
a user asserted about the allocation — and, for uniquely rendered identities,
performs the tax translation. An adopted nominee rule reads the current
allocation facts, tests them against the identified report, and produces the
`$450` nominee reduction and `$750` remainder as a `RunResult` publication.

A tax rule—not the user—determines the return consequence supported by the
current report and current allocation assertions. The result retains a walkable
account of the report, every allocation it used, the rule and authority applied,
and the supportability decision. It does not put that result on Schedule B or
Form 1040.

The milestone deliberately separates three things:

1. the payer's documentary report of interest;
2. attributed ordinary statements allocating parts of that report to other
   people; and
3. the rule-produced tax consequence for the taxpayer.

The user supplies item 2. The product owns item 3. A calculated remainder is not
a finding that the taxpayer legally owns the remainder; it is the amount left in
the product's taxable-interest calculation after supported recorded reductions.

## Authority basis and its two predicates

The reduction and the duty to report have different legal bases, and this
milestone must never collapse them into one predicate.

- **The reduction.** IRC section 61(a)(4) and Treas. Reg. section 1.61-7(a)
  include the taxpayer's own interest in gross income; they do not themselves
  prescribe a nominee subtraction or a beneficial-ownership test. The reduction
  is described only by the official return mechanic: the 2025 Schedule B, Part I
  instructions have the taxpayer report the full amount (including the nominee
  portion) on line 1, subtotal line 1, enter "Nominee Distribution" below the
  subtotal for the interest received as a nominee, subtract it, and enter the
  result on line 2 — which reaches Form 1040 line 2b via line 4 after the series
  EE/I exclusion. That instruction is form guidance, not controlling law. The
  ordinary allocation the user recorded is bounded evidence that the interest
  belongs to another person for applying this mechanic; it is not independently
  proven beneficial ownership. Placement on the actual form belongs to a later
  milestone: this milestone produces the internal reduction and remainder only
  and puts nothing on Schedule B or line 2b.
- **The reporting duty.** The separate obligation to issue the actual owner a
  Form 1099-INT rests on IRC section 6049 and its nominee/middleman regulations.
  It is left unreconciled and authority-indexed here.

These are two predicates, never one. A supported reduction does not establish
that any reporting obligation was met or determined, and no reporting, payment,
or transfer fact is required to support the reduction. Gate P1 verified the
reduction's basis and mechanic against the official 2025 Schedule B and its
instructions, using the Code and Treasury regulations for any controlling claim
and IRS guidance only as explanation; Track 0 selected the exact pinned citation.

## Why this is next

The preceding milestone built the ordinary assertion and its lifecycle without
smuggling in a tax conclusion. The useful test was whether the engine can
consume that honest input and produce an honest tax consequence. Jumping
straight to Schedule B would have combined tax classification, supportability,
legacy migration, return arithmetic, attachment tie-out, and reader-facing
explanation. Keeping the consequence separate makes a failure attributable.

Paper work settled the rule boundary and the smallest executable shape. The
milestone then climbed to production code and real execution.

## Current state

The repository already provides:

- the current `tax.us.nominee-allocation.amount` ordinary fact, keyed by payer,
  statement, tax year, and recipient;
- a producer, correction and retraction lifecycle, and log-only recovery of the
  allocation and its attribution;
- the documentary Form 1099-INT box-1 fact with the same payer, statement, and
  tax-year identity components;
- immutable derived findings with rule, source, adoption, citation, and dynamic
  dependency pins;
- an accrued-interest precedent with per-item and per-report aggregate
  supportability and rule-owned current-year consequences; and
- a production runner that returns calculated publications without appending
  them as current workspace findings.

It now also provides, for uniquely rendered identities:

- an adopted `rule-artifact.v8` citizen
  `tax.us.2025.rule.interest.nominee-reduction` consuming current
  nominee-allocation facts through `bound_sources`;
- a bounded tax-layer coordinator that groups zero, one, or several current
  allocation facts by exact report identity and evaluates the group;
- a report-scoped nominee reduction (or a report-scoped block), with remainder
  observed only on a supported group;
- the internal prefix `tax.us.2025.interest.nominee-reduction` and its
  report-scoped suffixed symbol and pin topology;
- C0-as-absence: no nominee publication for a report-only group, and one
  rule-level `no_groups_selected` inapplicable row when the whole universe is
  that state.

It still does not provide:

- an information-reporting conclusion;
- a line-2b or Schedule B consumer of the new ordinary fact or of the new
  prefix;
- a kernel identity-encoding repair, or a pre-execution intake restriction for
  delimiter-shaped values; or
- a repair of T0-F5.

The accrued-interest **policy** for an excessive report group—do not choose a
winning subset, clamp, or publish a misleading remainder—was selected as the
semantic precedent by the ownership-translation milestone. Pairing-specific
dispatch did not transfer. Track 0 established the nominee mechanism from the
new fact's actual shape.

The allocation producer's interrupted multi-act write remains non-resumable.
Tests may create committed synthetic allocations through that boundary; this
milestone does not expose it through a user-facing production caller.

## Selected product behavior

These are product requirements. They do not select a schema, rule count,
dispatcher, or module.

1. **Report-local calculation.** Each current allocation applies only to the
   identified report whose payer, statement, and tax-year identity it shares.
   Another report, including one from the same payer, cannot support or absorb
   it.
2. **Current assertions only.** Corrected and retracted findings remain
   historical but do not contribute to a new execution. A later reassertion may
   contribute as a new current answer at the same proposition identity.
3. **Whole-set supportability.** For one report, the current allocations are
   evaluated together. If their sum exceeds the report amount, the product does
   not select recipients, clamp the sum, emit a negative remainder, or present
   the unreduced amount as a settled result. The dependent consequence blocks
   with a report-scoped reason.
4. **Rule-owned consequence.** When the set is supportable, an adopted rule
   produces the report-scoped nominee reduction; the remainder is the report
   amount less that reduction. The reduction is the required tax consequence.
   The remainder is an observed calculation only (`report amount − published
   reduction` on a supported group): no in-milestone consumer, lifecycle, or
   provenance need justifies a separate remainder citizen. The ordinary
   allocation finding remains what a user asserted; it is not rewritten as a
   tax result.
5. **No-activity is not a denial.** With no current allocation for a report, no
   nominee reduction applies and the report amount continues into calculation.
   The product may say no allocation is recorded. It may not say the user denied
   other ownership or that the product proved the taxpayer owns the whole
   amount.
6. **Independent factual gates.** A belonging-supported nominee reduction does
   not require an onward-payment or credit fact. Conversely, payment or transfer
   alone does not establish an allocation or a nominee reduction.
7. **Inspectable provenance.** A produced reduction identifies the exact report,
   every current allocation it used, the supportability decision, the adopted
   rule, and the cited authority. If the remainder is published in any form, it
   identifies the report and the reduction computation. Attribution remains
   recoverable through the source allocation's assertion act rather than being
   copied into the tax proposition.
8. **Execution is not durable workspace standing.** The result is an ordinary
   `RunResult` publication. This milestone does not append it to the act log,
   promote it into a permanent fact, or create provisional-result standing.
9. **Return and reporting boundaries remain separate.** This milestone may
   establish an internal tax consequence without claiming that Schedule B is
   already complete or that a normalized information-reporting obligation has
   been determined.

## Abstract decisions to settle

Track 0 closed these. The resolutions below are binding on Track 1. R1, R2,
and R3 (implementation-boundary reopenings) are recorded in full under
`## Track 0 adversarial closure`.

1. **Report-scoped allocation enumeration and the empty result — settled.**
   The coordinator enumerates from marshaled `SourceFact`s (`run.live_sources`),
   year-filters by `run.ctx.reporting_year`, and outer-joins on composed report
   identity (outline §2). A nonempty both-present group reaches declared
   arithmetic through R1's `bound_sources` op on a `rule-artifact.v8`
   successor, not through ordinary `collect`. Empty / report-only groups are
   **not collected** (C0 option 1): no nominee publication, no completeness
   proposition, no user denial. Standing workspace authorization is not
   consulted for tax arithmetic or collection completeness.
2. **Dispatch and grouping — settled.** An ordinary declared rule cannot
   express report-scoped grouping (P2 Attacks 3 and 8). A bounded tax-layer
   coordinator (`packages/tax/nominee_consequences.py`) owns identity
   filtering, year scope, outer-join scheduling, C13 diagnosis, pin assembly,
   and mixed per-report outcomes. The adopted rule owns summation and the
   over-allocation comparison through `evaluate`. Pairing-scoped dispatch is
   not reused: it iterates ADR-0068 pairings, not allocations.
3. **Tax-consequence identity — settled.** One report-level
   `derived-finding.v2` at `tax.us.2025.interest.nominee-reduction|{report_fact_id}`.
   Remainder is an observed calculation only: no in-milestone consumer,
   lifecycle, or provenance need justifies a second publication (outline §6).
4. **Supportability result — settled.** Rule-local `choose`/`compare`/`block`
   gate. No separately published supportability verdict. A failing group never
   had a reduction finding to retract.
5. **Relationship to existing symbols — settled.** No established
   current-year-adjustment or legacy nominee symbol states this proposition
   (outline §8; claim-reuse proof below). New internal prefix; not bound to
   line 2b or Schedule B.
6. **Authority-indexed reporting boundary — settled.** IRC §6049(a)(1)–(2)
   and Treas. Reg. §1.6049-4 remain unreconciled and unimplemented. The 2025
   Schedule B Nominees paragraph is the return-reduction mechanic cited by the
   new citation `tax.us.2025.citation.interest.nominee-reduction`, not a
   reporting authority. A future reporting evaluation still needs nominee
   receipt *and* payments aggregating $10 or more, plus the §1.6049-4(d)(6)(i)
   deemed-payment reading; C9 found no in-scope payment/credit/transfer event
   citizen. A supported reduction does not determine that any information-
   reporting obligation was met.

Any Tier 2 or Tier 3 decision genuinely forced by these cases is recorded in an
ADR. Do not create an ADR for a reversible helper or file-layout choice, and do
not stretch an accepted ADR past its demonstrated proposition to avoid writing
a successor. **R3 requires ADR-0074** (grouped-rule disposition cardinality);
Track 0 names it and does not write it.

## Scope

The milestone:

- independently revalidated the tax proposition and current artifact boundary;
- selected and instantiated the smallest rule-owned consequence shape;
- implemented report-local coordination for current allocations;
- implemented supportability and supported reduction production (remainder
  observed only);
- exercised the behavior through the real projection, marshalling, package, and
  runner boundaries with synthetic data;
- preserved exact provenance and currentness across correction, retraction, and
  reassertion;
- demonstrated same-payer, different-report non-leakage;
- retained an explicit authority-indexed information-reporting matrix without
  implementing a normalized reporting obligation; and
- left a precise input contract for the later legacy-and-return-integration
  milestone.

## Non-goals

- No Form 1040 line 2b, Schedule B attachment, form-field binding, or
  presentation-projection change.
- No repair of the Schedule B T0-F5 tie-out defect. It becomes mandatory before
  a later milestone integrates a nonzero new adjustment onto an affected
  Schedule B surface.
- No legacy nominee-adjustment coexistence, conversion, migration, or
  deprecation.
- No Forms 1096 or 1099-INT filing, and no single normalized
  information-reporting predicate.
- No user-facing question, recipient editor, result explanation, or permission
  model.
- No durable negative allocation, beneficial-ownership determination, or claim
  that the remainder is independently proven ownership.
- No source-independent allocation identity, report-identity replacement, spouse
  exception, trust/custodian case, or contested-ownership workflow.
- No durable publication act, provisional finding, or cross-run reuse of a
  calculated result.

## Planning review cycle

The plan is developed through three small, independently reviewed checkpoints.
Each checkpoint edits this plan directly. Findings are absorbed before the next
checkpoint; a later section may not assume an earlier answer that is still
open. No Track 0 charter may be filed until all three checkpoints pass.

### Gate P1 — product and tax boundary — **PASS (findings absorbed)**

Independently reviewed against the official 2025 Schedule B, IRC section 61(a)(4)
and 6049, and Treasury regulations 1.61-7 and 1.6049-4. Six blocking findings
were absorbed: the reduction's controlling basis was overclaimed (now §61(a)(4)
and §1.61-7(a) include the interest; the nominee subtraction is form-instruction
mechanic, not controlling law); Decision 6 no longer lists the Schedule B
instructions as a reporting authority; C0 no longer pre-settles the empty state
as a `$0` reduction (Track 0 and Decision 1 own its representation); C9 no longer
requires an out-of-scope transfer fact; C7 was split into supportable isolation
and C12 was added for same-payer over-allocation with no absorption; and C11 was
added for several recipients summing exactly to the report ceiling. Stop
conditions 1–2 now name the forbidden empty-collection-as-completeness and
family-closure-via-coordinator moves.

Start with the plain-language purpose, selected behavior, fixed cases, and tax
propositions. Verify the nominee reduction against the official 2025 Schedule B
and instructions. Use IRC and Treasury regulations for controlling legal claims;
use IRS publications only as explanation. Review must attack:

- whether the product is deriving a tax conclusion rather than asking the user
  to supply it;
- whether absence, recorded allocation, supportability, and ownership are kept
  distinct;
- whether reduction and information reporting have been silently given one
  predicate;
- whether any case requires a fact excluded by scope; and
- whether the milestone produces a useful tax capability before return
  integration.

Output: a corrected product boundary and scenario set, with each authority claim
bounded to what its source establishes.

### Gate P2 — committed artifact and consumer map — **PASS (findings absorbed)**

Independently reviewed (record:
Gate P2's independent review). Four blocking
gaps were absorbed into Gate P3: live reachability, nonempty report-scoped
grouping, empty enumeration without source-family closure, and execution
cardinality for allocation report groups.

Map the real path from current allocation and box-1 findings to every candidate
collection, grouping, supportability, publication, package, and later consumer.
For every load-bearing repository claim, record the artifact, fields read,
relevant sibling fields not relied upon, and downstream consumers. Review must
independently verify:

- all readers and producers of `tax.us.nominee-allocation.amount`;
- allocation-to-report identity and its correction/retraction behavior;
- every place pairing-specific supportability or consequence dispatch is
  hard-coded;
- the report-scoped enumeration route: whether ordinary `collect` can return
  every current allocation for one report including the empty result, given that
  it currently requires source-family closure when its rows are empty, and
  whether another existing route, a bounded extension, or a grammar decision is
  needed — recording the exact authority evaluated (Decision 1 and stop
  conditions 1–2);
- the live runner's kernel-projected input path, compared against
  `packages/tax/nominee_allocation_recovery.py`. Establish which one an adopted
  calculation actually consumes; do not assume a tax-specific recovery or read
  view is an authoritative derivation input merely because it already groups
  convenient fields;
- how the real production path encounters and diagnoses a current allocation
  whose box-1 report has no current finding (deterministic `report_fact_id`
  present, `current_report_finding_id` absent), so C13's fail-closed result is
  traceable rather than assumed;
- whether any committed fact honestly represents a payment, credit, or transfer
  event usable within scope, to decide whether C9 is an executed negative control
  or a structural dependency prohibition;
- the existing current-year adjustment, legacy nominee subtotal, line-2b, and
  Schedule B bindings without treating package membership as adoption; and
- whether the planned consequence is externally bound, which would make the
  Track 0 integration-surface artifact mandatory.

Output: a bounded producer → authority → consumer → failure map and a list of
mechanical questions that paper inspection did or did not settle.

### Gate P3 — executable design and track decomposition — **PASS (findings absorbed; R1/R2/R3 reopened for Track 0)**

Independently reviewed (record:
Gate P3's independent review). Two blocking
admission/kill-7 defects were repaired in the outline; a later owner directive
withdrew the sentinel-`source_set` repair and reopened R1, R2, and R3, which
Track 0 closes below. The design outline's conclusions are absorbed into
`## Track 0 adversarial closure` and ADR-0074; the working outline itself is
not retained.

Turn the corrected cases and artifact map into a small implementation outline.
Name the proposed findings, rule or coordinator boundaries, call graph,
dispositions, pins, fixtures, and exact kill conditions without writing
production code. Review the outline section by section, then recheck all
cross-section dependencies. Review must attack:

- whether a cited precedent shares the properties this consumer needs;
- whether the zero-allocation path has real authority rather than a convenient
  default;
- whether a negative test can fail;
- whether a proposed rule artifact actually controls execution;
- whether the selected package can execute without entering the deferred
  Schedule B intersection; and
- whether the implementation tracks can be completed and reviewed one at a
  time.

Output: an implementation-ready Track 0 charter boundary. If one architectural
alternative remains materially distinguishable only by execution, stop and add
an owner-approved prototype plan with one proposition and the cheapest rung that
can decide it; do not hide a prototype inside Track 0.

## Fixed cases

All identifiers and values are synthetic. Each case must state the current
committed behavior, selected behavior, implementation work, and what it does not
establish.

| Case | Current facts | Required consequence |
| --- | --- | --- |
| C0 — no allocation | Report A is `$1,200`; no current allocation fact concerns it | No nominee reduction applies; `$1,200` continues into the taxable-interest calculation. **C0 option 1:** no nominee-rule invocation or publication for a report-only group (not a published `$0`, not a per-report inapplicable). The product may report that no allocation is recorded. It must not claim the user denied another owner or that ownership was independently proven. When the whole universe is report-only or empty, R2(a)/R3 record one rule-level `inapplicable` / `no_groups_selected` ledger row so the adopted rule does not disappear |
| C1 — one partial allocation | Report A `$1,200`; demo.pat `$450` | Supported reduction `$450`; remainder `$750`; both trace to report A, demo.pat's current allocation, rule, and authority |
| C2 — full allocation | Report A `$1,200`; demo.pat `$1,200` | Supported reduction `$1,200`; remainder `$0`; the report and explanation remain present |
| C3 — several recipients | Report A `$1,200`; demo.pat `$300`; demo.kim `$150` | One report-group supportability result; reduction `$450`; remainder `$750`; both allocations remain separately visible in provenance |
| C4 — over-allocation | Report A `$1,200`; demo.pat `$800`; demo.kim `$450` | The allocation set is preserved as assertions, but because the set sum `$1,250` exceeds the report the dependent reduction and remainder block for report A. No subset, clamp, negative remainder, or settled `$1,200` result |
| C5 — same-identity report correction | C1, then report A becomes `$1,000`; separately, C1 then report A becomes `$400` | Re-execution yields `$450` / `$550` in the first branch and the C4 block in the second; no stale `$750` or `-$50` |
| C6 — allocation lifecycle | C1, then demo.pat becomes `$400`, is retracted, and is later reasserted at `$250` | Successive executions use only the current answer: reduction `$400` with `$800` continuing; then the retracted step is C0-shaped — no nominee reduction applies and `$1,200` continues, represented as Track 0 selected for C0 rather than as a published `$0`; then `$250` with `$950` continuing. History remains recoverable but does not contribute |
| C7 — same payer, supportable isolation | Reports A and B share a payer; A `$1,200` with demo.pat `$450`; B `$1,500` with no current allocation | A reduces by `$450` to a `$750` remainder; B is unreduced at `$1,500`. Neither report's allocations or amounts reach the other |
| C8 — ownership without payment | C1, with no payment, credit, or transfer fact | The `$450` reduction remains available. No normalized information-reporting conclusion is inferred |
| C9 — payment/credit/transfer is not a reduction input | Report A `$1,200`; no current allocation. Gate P2 searches for a committed fact that honestly represents a payment, credit, or transfer event | If such a fact exists and is usable within scope, instantiate it as a negative control: its presence yields no reduction. If none exists, this is a structural dependency prohibition — the nominee-reduction rule may consume the report and current allocations but declares no payment/credit/transfer dependency, and no reduction arises without a current allocation. Do not claim execution proved the behavior of a nonexistent payment citizen |
| C10 — unrelated report group | Report A `$1,200` over-allocated (demo.pat `$800`; demo.kim `$450`); unrelated report C `$1,200` with demo.sam `$400` | A blocks without suppressing C's supported `$400` reduction / `$800` remainder |
| C11 — several recipients at the report ceiling | Report A `$1,200`; demo.pat `$700`; demo.kim `$500` | One report-group result; supported reduction `$1,200`; remainder `$0`; both allocations remain separately visible. A design that reaches remainder `$0` only for a single ceiling allocation must fail here |
| C12 — same-payer over-allocation, no absorption | Reports A and B share a payer; A `$1,200` over-allocated (demo.pat `$800`; demo.kim `$450`); B `$2,000` with no current allocation | A blocks; B does not absorb A's excess to make A supportable, and A's excess does not reduce B. Same-payer proximity never pools capacity across reports |
| C13 — allocation with no current report finding | The report's deterministic box-1 `report_fact_id` exists but no current box-1 finding stands (`current_report_finding_id` absent); a current allocation demo.pat `$450` names it | Report-scoped fail-closed: no reduction is produced, no historical or invented report amount is substituted, no zero is fabricated, and no crash. The state is diagnosed with a report-scoped reason. Gate P2 traces how the real production input path encounters and reports it |

## Evidence ladder and economy

Planning Gates P1–P3 and Track 0 begin at paper and committed-artifact
inspection. That is sufficient only for conclusions about meaning and existing
mechanics. Production claims require execution through the actual runner.

No rival prototype is pre-authorized. Gate P3 may propose one only if a named
decision remains both materially product-distinguishable and unresolved by the
committed artifacts. A prototype topic then requires its own approved plan and
one authorized evidence rung. Otherwise implement normally and test the real
consumer.

Capability guidance:

- Foreman and tax/contract reviewers: High / high.
- Novel synthesis builder for Track 0 or a new runner boundary: High / high.
- Production builder once the boundary is settled: Medium–High / high.
- Focused repair builder: Medium / medium.
- Independent adversarial reviewer: High / high.

## Tracks

### Track 0 — consequence contract and execution boundary

Resolve the six abstract decisions from the fixed cases and committed artifact
map. Produce the required adversarial-closure artifacts in this plan. Close
R1, R2, and R3. If a new published payload or schema is required, record
schema intent here; Track 1 discharges the Payload Instantiation Gate by
writing the schema files and the committed positive instance.

Track 0 is complete only when:

- the zero-, single-, multi-, over-allocated, lifecycle, cross-report, and
  no-current-report paths each have an explicit authority and expected
  disposition;
- the exact executable producer → authority → consumer path is named,
  including R1's selected collection/admission mechanism;
- the result identity and pin topology are selected;
- every reuse of an accepted claim passes the proposition, identity/lifecycle,
  and authority/explanation test;
- **R1, R2, and R3 are closed**, with the selected mechanism, disposition
  shape, and dispositions stated and justified — including R1's full
  specification (expression/schema shape, coordinator binding, evaluator
  behavior outside the coordinator, empty-input behavior, validation rule,
  `AccessLog` entries, pin conversion), R3's ledger-totality answer, and R2's
  answers stated as consequences of R3; and
- no unresolved product or contract choice remains for the Track 1 charter.

Track 0 received an independent adversarial review before Track 1 was chartered
(Track 0's independent review).

### Track 1 — report-local supportability and tax consequences

Implement the smallest selected production shape. It must consume current
nominee allocations and the exact current report, evaluate the whole report
group, publish or block the report-scoped nominee reduction (remainder is
observed-only), and emit truthful pins and dispositions under R1–R3: the
`bound_sources` op on `rule-artifact.v8`, per-group ledger rows identified
by suffixed `symbol`, empty `missing` on over-allocation, and the
`no_groups_selected` inapplicable row when no group is selected. Use
declared rule content wherever the contract says a rule owns behavior; do not
bury a tax decision in a coordinator. Write the three schema successors and
the committed v9 instances before emitting the new block code.

Run focused tests during development and the full suite before handoff because
changes under `packages/derivation/` or the runner require it. Track 1 received
independent review READY with no blocking finding (record:
Track 1's independent review) and two
owner-directed repairs before Track 2 began.

### Track 2 — lifecycle, isolation, and package execution

Exercise C0–C8 and C10–C13 through the real projection, marshalling, package resolution,
and `run()` boundary. Prove corrections, retraction, reassertion, same-payer
report isolation, unrelated-group behavior, and exact provenance. Confirm the
selected package does not claim line-2b or Schedule B completeness and does not
consume or reinterpret the legacy nominee fact.

Track 2 received independent review READY with no blocking finding (record:
Track 2's independent review) before
closeout.

### Closing unit — durable boundary and next-stage handoff

The plan, accepted ADR-0074, tests, implementation, and a short lesson-oriented
retrospective are curated. The later legacy-and-return-integration milestone's
input contract is stated below. T0-F5 is carried forward as a hard gate on that
stage. Final publication review is independent.

## Track 0 adversarial closure

Paper closure of the absorbed Gate P3 design outline plus the three
owner-reopened decisions. The outline's conclusions are recorded here and in
ADR-0074; it is not retained as a separate working record, and nothing below
depends on an object identifier that branch curation would orphan. No artifact below is `PENDING`. Identifiers are synthetic
`demo.*` / `demo-*`.

R3 is settled first; R2 is stated as a consequence of it; R1 is independent
of the ledger shape.

### R3 — authoritative disposition shape for a grouped rule

**Compared shapes (none preselected).**

| Shape | What “complete ledger” would mean | Honest mixed C10? | C0-only row? | ADR-0020 |
| --- | --- | --- | --- | --- |
| **1. Totality redefined at report-group scope** with an explicit group subject | One identified row per classified disposition-group (both-present evaluations + C13); when that set is empty, exactly one rule-level no-selection row | Yes: two group rows, different subjects | Yes, the empty-selection row | **Supersedes** Decision 1 cardinality (“one row per package rule/selector artifact — linear, not combinatorial”, ADR-0020 Consequences) and Decision 1a’s singular-row one-status. Preserves Decision 1 *totality* (every adopted rule is accounted for) via the empty-selection row |
| **2. One rule-level summary plus separately identified group outcomes** | Always exactly one summary row per adopted rule, plus group rows | Only if the summary is **not** a tax outcome: a single `published`/`blocked`/`inapplicable` summary cannot honestly describe mixed C10. Off-ledger group outcomes would leave blocked groups unwalkable, contradicting Decision 1’s “single authoritative disposition surface” | The summary | Preserves totality-as-one-summary. Cardinality still combinatorial if group rows are first-class ledger entries. Decision 1a still needs a non-tax summary kind |
| **3. Nested group outcomes on exactly one rule row** | One row per adopted rule; group outcomes live in a nested array | Yes, if the row-level status is a new host kind | Empty nested array | **Preserves** cardinality. Extends Decision 1a (a fourth host status) and Decision 4 (selection must enter the nested structure). Fights the committed primitives (`record_named_block` / `publish_symbol_finding` append flat rows; `presentation_projection._dispositions_by_symbol` joins flat `symbol`) |

**Selected: shape 1**, with group identity carried by the disposition row’s
`symbol` (the same suffixed string the publication uses), not by abusing
`missing` and not by a new subject field.

**Why this one.** The outline’s executable behavior (one coordinator loop,
per-group `record_named_block` / `publish_symbol_finding`, no cross-group
suppression) already emits per-group rows; Gate P3 review Attack 8 verified
that as executable behavior, not as a ledger contract. Shape 1 is that
behavior plus an honest contract for what the rows mean. Shape 3 would
preserve ADR-0020 cardinality at the cost of a nested recording shape the
primitives and the presentation join do not have, which is not the smallest
Track 1 delta. Shape 2’s summary cannot be a v8 tax status under mixed C10
without lying; making the summary a non-tax host kind plus first-class group
rows is shape 1 plus a redundant summary.

Existing aggregate-supportability appends (`pairing_consequences.py`
`dispatch_aggregate_supportability_on_run` 706–721; `runner.py`
`record_named_block` 1289–1313) are **evidence** that the runner can append
multiple rows for one `artifact_id`. They are not a silent ADR-0020 answer
(charter R3; outline §5 REOPENED). ADR-0070 Decision 7 ratifies report-scoped
supportability outcomes for accrued-interest publications; it does not
reconcile mixed per-report rows with ADR-0020 Decision 1 totality.

**ADR required.** This selection **supersedes** ADR-0020 Decision 1’s
cardinality contract and Decision 1a’s “each artifact’s ledger row”
(singular) one-status classification **for the exact rule
`tax.us.2025.rule.interest.nominee-reduction` only** — the
"coordinator-grouped rules" class is withdrawn (ADR-0074 Decision 3a).
It does **not** silently reinterpret ADR-0020. **ADR-0074** (not written in
this track) must record: grouped-rule cardinality is one identified
disposition row per classified disposition-group, linear in selected groups
not in adopted rules; totality (every adopted rule accounted for) is
preserved by the empty-selection row; Decision 4 selection is by exact
`row.symbol == S` (below). Ordinary once-per-rule-id artifacts keep
ADR-0020 unchanged.

**Scope predicate — withdrawn and replaced.** Two earlier phrasings are
withdrawn.

*"Coordinator-grouped rules"* is not a mechanical class.

*"Adopted rules whose disposition rows carry a suffixed `symbol` of the form
`{publishes}|{subject_fact_id}` — today exactly the nominee reduction rule"* is
**false and circular**. False: `dispatch_aggregate_supportability_on_run`
already publishes `{AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX}|{report_fact_id}`
(`packages/tax/pairing_consequences.py` 716), so that shape is not unique to the
nominee rule today. Circular: it defines the governed class **by the very row
shape the contract exists to require**, so a rule that omitted the suffix would
fall *outside* the contract instead of *violating* it — the opposite of what an
enforceable contract must do.

**Selected scope: the exact rule identity.** ADR-0074 governs
`tax.us.2025.rule.interest.nominee-reduction` at the adopted version, named
explicitly. No static grouped-dispatch marker is introduced: R1's contract does
not supply one (the coordinator dispatch registry is Python, not package-visible
declaration), and inventing a package-visible marker for a single rule would be
a broader grammar change than this milestone authorizes. If a later milestone
needs a reusable class, a declared marker is the right shape then — and the
suffix must remain a *requirement* on members of the class, never the test for
membership.

Under this scope a missing or malformed suffix on a nominee row is a **contract
violation**, which is what the kills below assert. ADR-0070's
aggregate-supportability rows are outside ADR-0074 because they are a different
rule id, not because of their symbol shape; they are not retroactively
reinterpreted, and whether they need the same treatment is a separate question
this milestone does not answer.

**Implementation kills for the grouped-ledger contract.** Each must be able to
fail:

1. **Exact suffix on every group outcome.** Every nominee group-outcome row
   (published or blocked) carries `symbol` exactly
   `tax.us.2025.interest.nominee-reduction|{report_fact_id}` for its own report.
   Fails on a missing suffix, the bare prefix, or another report's id — a
   missing suffix is a violation, not an exemption.
2. **No duplicate group outcome.** For one run and one `artifact_id`, no two
   rows share a suffix. Fails if a group is recorded twice.
3. **Mixed C10 independently selectable.** Looking up A's suffix yields exactly
   A's `blocked` row and C's suffix exactly C's `published` row — each a single
   row, neither shadowing the other. Fails if a lookup returns 0 or 2 rows.
4. **C0 keeps exactly the unsuffixed row.** A C0-only run records exactly one
   `inapplicable` / `no_groups_selected` row at the **unsuffixed** prefix and
   **no** suffixed group row. Fails on a suffixed C0 row, an extra group row, or
   a missing no-groups row (the record-level XOR above).

**Track 1 boundary — the governing contracts come first.** ADR-0074's
grouped-ledger contract and the `bound_sources` declaration/dependency semantics
must be **fixed before code relies on them**, not deferred to milestone
closeout. A Track 1 charter is not implementation-ready unless ADR-0074 is
accepted (or explicitly owner-deferred with the dependent work withheld) and the
dependency-integrity contract is settled. Writing the coordinator, the v8
citizen, and the v36 package against an unratified ledger cardinality would mean
the ratifying document gets written to match whatever the code did — the
inversion these planning gates exist to prevent.

#### How each case is recorded

Disposition-group keys are universe keys that emit a nominee outcome: both-
present (consequence evaluation) and C13 (allocations, no current report).
Report-only keys (C0, C7/C12 B) are **not** disposition-groups (C0 option 1).

| Case | Ledger rows for the nominee rule | Identification | `missing` |
| --- | --- | --- | --- |
| **C0-only** (every universe key report-only, or empty universe) | Exactly one `inapplicable` row, evidence `no_groups_selected: true` | `symbol` = unsuffixed prefix `tax.us.2025.interest.nominee-reduction` — **required** (ADR-0074 Decision 3d). No finding, no `guard_result`, no `superseded_by`, no `code` | absent (inapplicable forbids a false dependency list) |
| **One successful group** (C1, C2, C3, C8, C11) | Exactly one `published` row | `symbol` = `tax.us.2025.interest.nominee-reduction\|{report_fact_id}`; `finding_id` / `act_id` as today (`_record_derived_publication`) | n/a |
| **One blocked over-allocation** (C4, C5b, C12 A) | Exactly one `blocked` row | `symbol` = same suffix; `code` = `NOMINEE_ALLOCATIONS_EXCEED_REPORT`; pins name the present report finding and every current allocation in the group | **`[]`** (nothing is absent; the report is present and pinned) |
| **Mixed C10** | Two group rows, same `artifact_id`: A `blocked` as C4; C `published` as C1 | Distinct suffixed `symbol`s. A’s pins exclude `demo.sam`; C’s pins exclude `demo.pat` / `demo.kim` | A: `[]`; C: n/a |
| **C13** | Exactly one `blocked` row | `symbol` = same suffix; `code` = `DEPENDENCY_ABSENT`; pins name the current allocation finding(s) only | **`[composed report_fact_id]`** (the named report finding is absent; pairing_dispatch 170–180 is the accurate precedent) |
| **C7** | One published row for A; **no** row for report-only B | A identified by suffix. B is C0 option 1 (no per-report nominee row). The adopted rule is on the ledger via A | n/a |

#### Cardinality and “complete ledger”

- **One row per selected disposition-group**, identified by suffixed
  `symbol`.
- **When zero disposition-groups were selected:** exactly one rule-level
  `inapplicable` / `no_groups_selected` row.
- **Checkable completeness, in two parts.** The earlier single rule ("count
  equals the number of classified disposition-groups") is **not checkable from
  a closing record alone**, because the group count is a run fact the record
  does not carry. Split it:

  1. **Record-level XOR (checkable from the closing record alone).** For this
     `artifact_id`, either there is exactly one `no_groups_selected`
     `inapplicable` row and **no** group-outcome row, or there are one or more
     group-outcome rows with distinct suffixed `symbol`s and **no**
     `no_groups_selected` row. Never both, never neither.
  2. **Run-level count (checkable in a test that also holds the universe).**
     The number of group-outcome rows equals the number of classified
     disposition-groups the coordinator selected in that run.

  Mixed statuses on one artifact are then expected, not a fixture
  contradiction.

#### Group identity without abusing `missing`

Pins do **not** suffice as the consumer join key. Pin `id` is a finding id
(`derivation-record.v8` pin `$defs`), not the report fact id string.
`presentation_projection._dispositions_by_symbol` (109–121) joins on
`row["symbol"]`, falling back to `rule["publishes"]` (the unsuffixed prefix)
when `symbol` is absent; `_one_row` (124–128) errors on `len(rows) != 1`.
A blocked C10 row without `symbol` would collide on the prefix. Aggregate
supportability’s `missing=[report_fact_id]` while also pinning that report
(`pairing_consequences.py` 706–710) is a tolerated same-run side-channel
for the line-2b subtotal; this milestone has **no** later same-run consumer
of the nominee block, and `explanation.py` 283–321 maps `missing` to
`unmet_references` (a present report in `missing` would be explained as an
unmet dependency).

**Selected identity:** the optional v8 `symbol` property on the blocked row,
set to the same suffixed string a successful publication would have used.
Committed precedent: `runner.py` `absorb_association_result` 1486–1497 sets
`symbol` on association refusal rows so presentation can join. Track 1
extends `record_named_block` with optional `symbol=` and the nominee
coordinator always passes it. No v9 subject/group field.

#### Explanation / presentation selection for a suffixed symbol
(ADR-0020 Decision 4)

This milestone does not project `explain()` of the new code (same inherited
`npe-walk.v3` lag the accrued codes already have). The **selection contract**
a later walker must implement, and that presentation already almost
implements via `row.symbol`:

**The selection algorithm is specified normatively by ADR-0074 Decision 3f and
is not restated here.** Two properties matter for this plan's scenarios: entry
is decided by resolving the exact nominee rule from the adopted package and
testing `S == P` or `S` beginning with `P + "|"` (where `P` is that rule's
declared `publishes` prefix) — not by a producer lookup, which finds nothing for
a suffixed symbol. A walk that **does not enter** uses ADR-0020 Decision 4
unchanged. A walk that **does enter** stays on the ADR-0074 path and **never
returns to ADR-0020's producer-based ledger-row lookup**: it selects the
published row at `row.symbol == S`, else a run-scoped act-log derived
publication with that finding symbol (preserving Decision 4's
interrupted/recovered-run fallback), else the blocked or inapplicable row at
`row.symbol == S`, else `no_disposition_recorded` for `S`. Falling back to
Decision 4's producer lookup after an entered-but-unmatched walk would be
**unsafe**: for `S == P` with group rows present, that lookup finds this rule
and would select an arbitrary group's row. Querying `P` while group rows exist
therefore yields `no_disposition_recorded`, never an arbitrary group.

The committed walker (`explanation.py` 221–277) currently matches
`r["publishes"] == s` and then takes the first published row for that
producer. That is **wrong for this rule**: a suffix `S` finds no producer
(the citizen publishes the prefix), and a prefix `S` would pick one report
arbitrarily — which is exactly why ADR-0074 Decision 3f decides entry from the
adopted package rather than from that lookup. The narrowing is recorded in
ADR-0074, not applied by silently reinterpreting the committed walker, and it
reaches no rule other than the named one. Presentation `_dispositions_by_symbol` already prefers
`row.symbol` and is the in-tree join this contract matches.

#### Attempt outcome (subsumes R2(c))

`_execute` ignores `attempt`’s return (`runner.py` 1697–1714; Gate P3 review
Attack 2). The string is a saturation-facing summary, **not** the
authoritative ledger.

| Coordinator situation | Attempt return | Authoritative ledger |
| --- | --- | --- |
| No disposition-group selected (C0-only / empty universe) | `"inapplicable"` | the `no_groups_selected` row |
| At least one group published (including mixed C10) | `"published"` | the per-group rows; mixed C10 is not a single published rule |
| At least one group blocked and none published | `"blocked"` | the per-group blocked row(s) |

`resolved.add(rule_id)` after the loop is unchanged and still required so
`finalize_unreached` skips the rule (outline §5). The pairing empty-loop
`"published"` (`supportability.py` 131–133) is a **resolution** precedent
only; it is not used as the C0-only outcome string.

#### `derivation-record` successor fields

`derivation-record.v9` is additive (v8 bytes untouched). **Its exact shape is
specified normatively by ADR-0074 Decision 3h and is not restated here** —
including the artifact- and symbol-scoping of the `no_groups_selected` branch,
the preservation of every existing v8 requirement (`published` still requires
`symbol`; existing `blocked` rows and both existing `inapplicable` forms may
omit it), and the positive/negative schema-test obligations.

Track 1 verification items from that decision: widen the `code` enum with
`NOMINEE_ALLOCATIONS_EXCEED_REPORT`; add the third `inapplicable` evidence
branch under ADR-0074's scoping conditions; add no new subject field; enforce
that a `NOMINEE_ALLOCATIONS_EXCEED_REPORT` row carries `missing: []` and a
`symbol`. No record valid under v8 may stop validating under v9.

#### ADR-0020

**Supersedes** Decision 1 cardinality and Decision 1a singular-row
classification for the exact nominee-reduction rule only. **Narrows** Decision 4
selection to exact `row.symbol`. **Preserves** Decision 1 totality
(every adopted rule accounted for) and the ledger as the single
authoritative surface. **ADR-0074** is required; do not write it in
Track 0; do not treat this plan as that ADR.

### R1 — collection/admission mechanism

**Committed `rule-artifact.v7` survey (verified against the files named).**
No committed mechanism satisfies R1’s five requirements. That measurement
was first taken by the Track 0 charter review (Attack 1) and is re-verified
here:

| Candidate | Artifact actually read | Which requirement it fails |
| --- | --- | --- |
| Ordinary `collect` | `rule-artifact.v7.schema.json` 239–258 `required: ["op","name","source_set"]`; `evaluator.py` 136–149 nonempty ignores `source_set`, empty requires `source_set in closed_sets`; `package_validation.py` `COLLECT_TARGET_NOT_FAMILY` when `universe_guard_active` (guard and allowlist 1692–1708; collect enforcement 1826–1840) | A real family violates (3) and stop conditions 1–2. A non-family `source_set` is schema-valid but fails (5) the moment the intended guard is applied: measured against **then-production `package.core-calculations` v35 / `artifact-package.v26`**, the allowlist already ended at `artifact-package.v17`. Piggybacking an existing family’s id fails `name != declared_member`. Optional-`source_set` collect is **not** enough: `collect.get("source_set")` of a missing key is `None`, `str(None) == "None"`, and that is `COLLECT_TARGET_NOT_FAMILY` |
| `count` | `evaluator.py` 151–158 | Always requires `source_set in closed_sets` — a completeness proposition even on a nonempty group |
| `collect_categorical_all_equal` | schema 650–669 (no `source_set`); evaluator 241–262 | Reads `env.sources` as strings and tests categorical equality; does not fold decimals. Empty raises `DEPENDENCY_ABSENT`. `_iter_collect_exprs` (455–459) does not see it. Wrong op |
| Pairing 1:1 `replace`+`ref` | `supportability.evaluate_one` 94–103; accrued citizen `rule.relationship.accrued-supported.json` 14–33 | Two scalars, not a variable-length allocation group. The adopted rule would not own summation |
| List-valued `ref` | `marshal.py` 267–304 binds **one** current finding per symbol; `Environment.symbols` is the single-value table; `_flatten` docstring names collect lists | Tolerated evaluator behavior if a coordinator stuffed a list into `symbols`, not an admission contract |
| Coordinator pre-sum, then `ref` of the total | — | Fails (2): the adopted rule would not own summation (ADR-0006 / ADR-0071 Decision 3) |

`COLLECT_TARGET_NOT_FAMILY` inactivity is confirmed: `universe_guard_active`
allowlist is `artifact-package.v3`–`v17` (`package_validation.py` 1692–1708),
while then-production `package.core-calculations` v35 used
`artifact-package.v26` — the generation at which `rule-artifact.v7` is first
admitted. The delivered v36 uses `artifact-package.v28`; both are beyond the
allowlist, so the guard binds neither. ADR-0035 production condition:
reject “any rule whose collect targets a non-family fact type.” An inactive
guard is not an admissible meaning for `collect.source_set`. Adding a
nominee-allocation source family is forbidden (stop conditions 1–2).

**Selected: `rule-artifact.v8` additive successor with a new op
`bound_sources`.** Smallest honest mechanism: a typed report-local input that
is **not** ordinary `collect`, so `_iter_collect_exprs` does not treat it as
a collect-family target, the intended validator does not apply, and no
family is introduced. Not a general package-validator repair.

#### Expression / schema shape

New `rule-artifact.v8` (v7 bytes untouched). Copy v7, add one `expr` `oneOf`
branch:

```json
{
  "type": "object",
  "properties": {
    "op": { "const": "bound_sources" },
    "name": { "type": "string", "minLength": 1 }
  },
  "required": ["op", "name"],
  "additionalProperties": false
}
```

No `source_set` property exists, so it cannot be filled with a sentinel.
Citizen fields otherwise match the outline §10 table: `id`
`tax.us.2025.rule.interest.nominee-reduction`, `schema` `rule-artifact.v8`,
`requires: []`, `when: true`, `pins: []`, `publishes`
`tax.us.2025.interest.nominee-reduction`, `blocked.code`
`NOMINEE_ALLOCATIONS_EXCEED_REPORT`, `blocked.missing: []`,
`citations` the new citation, `scope.tax_year` 2025.

Declared `value` (paper; Track 1 writes the citizen):

```text
choose
  when: compare gt
          left:  add( bound_sources name=tax.us.nominee-allocation.amount )
          right: ref  tax.us.2025.f1099int.box1-interest
  then: block code=NOMINEE_ALLOCATIONS_EXCEED_REPORT
  else: add( bound_sources name=tax.us.nominee-allocation.amount )
```

`add` + `_flatten` (`evaluator.py` 177–178, 292–300) already folds a list of
decimals; `gt` (not `gte`) keeps C11 publishing the full reduction.

**Package admission of the citizen** requires `artifact-package.v28`, which `package.core-calculations` **v36** now uses (v26
bytes untouched; **v27 is already proposed** on `milestone-schema-ledger`
by `document-ordinary-fact-translation` for `source-family.v4`, event
`20260829T180001Z-artifact-package-b7d1f4`). v26’s member `schema` enum
ends at `rule-artifact.v7` (`artifact-package.v26.schema.json` 89, 934;
description: “admitting rule-artifact.v7”). A v36 package that pins a v8
rule is not a valid v26 document. `_RULE_ARTIFACT_SCHEMAS`
(`package_validation.py` 192–194) must gain `rule-artifact.v8` in Track 1.
If the other milestone publishes v27 first, Track 1 writes v28 as an
additive admit-v8 successor of that published file; it does not edit v27.

#### Coordinator binding

For one selected both-present group, after year-filter and outer-join
(outline §2, unchanged):

1. Read marshaled `SourceFact`s from `run.live_sources` (starts as
   `list(ctx.sources)`, `runner.py` 267) filtered by name; do not read
   `Environment.sources` (decimal strings only, no `fact_id`).
2. Build `local_env = dataclasses.replace(run.env(), symbols={
   "tax.us.2025.f1099int.box1-interest": this report’s amount },
   sources={}, bound_sources={ "tax.us.nominee-allocation.amount":
   [this group’s allocation values, sorted by allocation `fact_id`] })`.
   Precedent: `supportability.evaluate_one` 94–101 (`replace` on
   `base_env`). **Do not name `closed_sets` in
   `packages/tax/nominee_consequences.py`:**
   `tests/source_completeness/test_track3_authority_dispatch.py`
   `test_no_module_reintroduces_a_closed_sets_carrier` allows that
   identifier only in `evaluator.py`, `runner.py`, and
   `runners/derive.py`. The selected op does not consult the field, so
   leaving the run’s admissions in place is harmless.
3. `evaluate(rule["value"], local_env, access)`.
4. On `EvalBlocked(NOMINEE_ALLOCATIONS_EXCEED_REPORT)` →
   `record_named_block(..., code=that, missing=[], symbol=suffix, pins=present_pins)`.
   On a decimal → `publish_symbol_finding` with coordinator
   `format(amount, "f")` (the primitive does not stringify; pairing
   formats first).

`Environment.bound_sources` is a new field with `default_factory=dict`,
placed after existing defaults so positional `Environment(symbols, {},
frozenset(), parameters, canon)` in `_pairing_local_environment` 232 keeps
working.

#### Evaluator behavior outside the coordinator

`bound_sources` reads **only** `env.bound_sources.get(name, [])`. It does
**not** read `env.sources`. Ordinary `_Run.env()` (`runner.py` 337–347)
does not populate `bound_sources`, so it is `{}`.

If the same rule is evaluated by ordinary `attempt` or `finalize_unreached`
against the run-wide environment, the op raises `EvalBlocked(DEPENDENCY_ABSENT, [name])`.
That is fail-closed: it cannot silently fold run-wide allocation values
(the P2 C10/C12 leak). It is **not** the honest C0-only disposition (R2(a)
forbids a false dependency block); the `_Run.attempt` intercept remains
load-bearing for honesty and for `resolved.add`. The op is defense in
depth against leakage if the intercept is omitted.

#### Empty-input behavior

Empty `env.bound_sources[name]` (missing key or `[]`) raises
`DEPENDENCY_ABSENT` with `missing=[name]`. It does **not** return `[]`
(that would manufacture a zero) and does **not** raise `SOURCE_SET_UNCLOSED`
(that would be a closure claim). The coordinator never schedules a
report-only group into `evaluate` (C0 option 1), so this path is the
ordinary-evaluation / wrongly-scheduled-empty defense, not C0’s product
meaning.

#### Validation rule

- Schema: `additionalProperties: false` on the op refuses a `source_set`
  field.
- `schemas.validate_declared` remains the admission gate
  (`package_validation.py` 852–856).
- `_iter_collect_exprs` continues to yield only `op == "collect"`; the
  intended `COLLECT_TARGET_NOT_FAMILY` guard does not see `bound_sources`.
  **No general validator repair.** If someone writes ordinary `collect` of
  `tax.us.nominee-allocation.amount`, the intended guard (when applied to
  current package schemas) still issues `COLLECT_TARGET_NOT_FAMILY`
  because no package source-family declares that type — that is the
  correct refusal, not a new rule.
- Kill 7’s static package-member half (outline §9) still fails v36 if any
  `source-family` or `source-closure-mapping` names
  `tax.us.nominee-allocation.amount`.

#### Declaration and dependency integrity for `bound_sources`

Adding `rule-artifact.v8` to the version allowlists makes the citizen
*admissible*. It does **not** make `bound_sources.name` **visible** to package
or authorization dependency analysis. Both graphs today build edges only from
`_iter_ref_names` and `_iter_collect_source_sets`
(`package_validation.py` reachability adjacency ~1511–1551;
`authorization_closure.py` 130–145). A `bound_sources` name is invisible to
both, so without the work below the nominee rule would have **no edge** to the
bundle declaring `tax.us.nominee-allocation.amount`: the bundle would be
unreachable, and the authorization digest would not change when that dependency
changed. That is a silent integrity hole, not a cosmetic gap.

**Name discovery.** Track 1 adds one walker,
`_iter_bound_source_names(expr)` in `package_validation.py`, mirroring
`_iter_collect_exprs`’ recursive shape but yielding `expr["name"]` for
`op == "bound_sources"` only. It is applied to **both** `when` and `value`,
exactly as `_iter_ref_names` already is. `authorization_closure.py` imports it
(it already imports `_iter_collect_source_sets` from that module).

**Name identifies an admitted fact type.** Package validation must prove each
discovered name is a fact type declared by an admitted bundle member — not an
arbitrary string. Reuse the committed `bundles_for_fact` map
(`package_validation.py` 1477–1482, built from bundle `fact_types`): a
`bound_sources.name` absent from `bundles_for_fact` is a member issue
(`BOUND_SOURCE_TARGET_UNDECLARED`, new code on the existing member-issue
surface — no schema change). A misspelling therefore fails admission rather
than silently binding nothing at run time.

**Inbound package reachability.** In the reachability adjacency, for each
`bound_sources` name add `adj[rule_id].update(bundles_for_fact[name])`, the same
edge shape already used for declared refs (1517, 1551). This connects the
nominee rule to the allocation vocabulary bundle, so omitting that bundle from
v36 yields a validation failure rather than a quietly inert rule.

**Authorization closure.** In `authorization_closure.py`, alongside the existing
declared-refs and collect-source-set edges, add for each `bound_sources` name
`edges[cid].update(bundles_for_fact.get(name, set()))`. The allocation
vocabulary then enters the closure and the authorization digest, so changing
that dependency changes the digest.

**Consumed-input restrictions.** `consumed` (1797) is currently
`collect_names | requires | ref names`. `bound_sources` names must join that set
so existing prohibitions keep applying — in particular the
recorded-non-composable check (ADR-0035’s "no rule may collect
recorded-non-composable content"). A non-family input mechanism must not become
a way around a restriction that exists for the content, not for the operator.

**v36 member and dependency topology (corrected against the committed
reachability builder).**

An earlier version of this table asserted two edges that **do not exist**. The
committed graph (`package_validation.py`, adjacency ~1500–1560; roots ~1618) is:
roots are declared `entrypoints` plus every form-field member; a rule's edges are
producers of its declared refs, bundles reached **only** through
`binding_fact_types` (that is, `input_bindings`), `source-family.v1` targets of
its `collect` `source_set`s, parameter/table refs, `composition`, and
`citations`. **There is no `publishes` → bundle edge**, and a bare `ref` reaches
no bundle without an `input_bindings` row — and Track 0 deliberately declines to
add one, because box-1 and allocations are multi-member sources an unkeyed
binding would leave unbound.

Reproducing reachability with the proposed members therefore gives:

| Member | Role | How it is actually reached |
| --- | --- | --- |
| `tax.us.2025.rule.interest.nominee-reduction` @ v1 (`rule-artifact.v8`) | the consequence rule | **Explicit `entrypoints` pin** (exact id@version). It is a root; nothing needs to point at it |
| `tax.us.nominee-allocation.vocabulary` (`bundle.v2`, existing bytes) | declares `tax.us.nominee-allocation.amount` | From the rule via the **new `bound_sources` → `bundles_for_fact` edge** this section specifies. This is the one new edge, and it is what makes omitting the bundle a validation failure |
| `tax.us.2025.f1099int.vocabulary` (existing member) | declares the box-1 report type | **Already reachable, by an existing path that does not involve the nominee rule**: an entrypoint reaches `rule.f1099int-b1-subtotal`, whose `collect` `source_set` edges to `source-family.v1` `tax.us.2025.f1099int.b1`, which edges to the bundle declaring its `member_predicate.fact_type` (adjacency ~1558–1562). The nominee rule's `ref` contributes **no** edge here |
| `tax.us.2025.interest.nominee-reduction.vocabulary` (new `bundle.v2`) | declares the published prefix as a fact surface | **Explicit `entrypoints` pin.** `publishes` creates no edge, so without this the member is `MEMBER_UNREACHABLE`. This is the committed idiom, not an invention: v35 already lists vocabulary bundles among its entrypoints (for example `tax.us.2025.f1098e.vocabulary`, `tax.us.2025.prior-return.vocabulary`) |
| `tax.us.2025.citation.interest.nominee-reduction` v1 | citation | From the rule via the existing `citations` edge |

Smallest explicit topology: **two entrypoint pins** (the rule and the new output
vocabulary) plus **one new edge kind** (`bound_sources` → declaring bundle). No
repository-wide `publishes` → bundle edge is invented to make a table true, and
no `input_bindings` row is added. `MEMBER_UNREACHABLE` must be empty for the
concrete v36 (kill 3), which is what proves this topology rather than asserting
it.

No `source-family` and no `source-closure-mapping` member is added.

**Live source registration stays rule-specific, and validation must say so.**
Deriving `collect_source_names` from the declared operator would be the more
general design, but `_resolved_run_material` builds that list from family
predicates, companions, categoricals, and hardcoded pairing/supportability
names; generalizing it is a broader change than this milestone authorizes.
Registration therefore remains the nominee-rule-specific hook (outline §1).
Because the operator's schema semantics and dependency analysis are generic
while binding registration is rule-specific, a `bound_sources` citizen could
otherwise be **schema-valid and dependency-analyzed** yet have **no coordinator
or binding path at all**, and would then silently never evaluate. Package
acceptance is therefore **not** generic (ADR-0074 Decision 1): such a citizen is
**not package-admissible**. Track 1 must enforce that — package validation
refuses a `bound_sources` rule whose id is not in the coordinator's dispatch
registry (`MEMBER_NO_BINDING_PATH`, member-issue surface). The registry is the same nominee-rule-id constant the intercept and
`_resolved_run_material` already key on, so the three cannot drift apart
without a validation failure.

#### Implementation kills for declaration and dependency integrity

Each must be able to fail:

1. **Unknown name.** A v36 variant whose `bound_sources.name` is misspelled
   (`tax.us.nominee-allocation.amont`) fails `validate_package` with
   `BOUND_SOURCE_TARGET_UNDECLARED`. Fails if validation passes.
2. **Omitted vocabulary.** A v36 variant without the allocation vocabulary
   member is not a valid reachable package. Fails if it validates clean.
3. **No unreachable members.** The concrete v36 produces **no**
   `MEMBER_UNREACHABLE` result. Fails if the allocation or reduction
   vocabulary is unreachable.
4. **Closure contains the dependency.** The computed authorization closure for
   v36 contains `tax.us.nominee-allocation.vocabulary`. Fails if absent.
5. **Digest sensitivity.** Changing that dependency changes the authorization
   digest. Fails if the digest is unchanged.
6. **Live path, not a hand-built context.** C1’s positive `$450` result is
   produced through the real package/adoption path
   (`live_coordinate_run`), not only a hand-assembled `RunContext`. Fails if
   the rule never enters `ctx.rules` — the silent `live.py` allowlist failure.
7. **No binding path.** A schema-valid `bound_sources` rule whose id is absent
   from the coordinator registry is **refused**: validation fails with
   `MEMBER_NO_BINDING_PATH`, so it is never package-admitted. Fails
   if such a package validates clean.
**Track 1 must-edit inventory.** Two kinds of edit are required, and the second
was missing when this section previously called the first a "complete
inventory": the **version allowlists** below make the v8 citizen *admissible*,
and the **declaration and dependency integrity** work above makes
`bound_sources.name` *visible* to dependency analysis. Admissibility without
visibility is the silent hole. Introducing a new `rule-artifact` version means
every allowlist that *enumerates* versions is a place the new citizen silently
does not exist. Two of these fail **silently**,
which is why the inventory is exhaustive rather than illustrative. Track 1 must
edit each, and a Track 1 charter is not implementation-ready until it names them:

| Site | Artifact | If missed |
| --- | --- | --- |
| `_RULE_ARTIFACT_SCHEMAS` | `packages/derivation/package_validation.py` | v8 citizen not recognized as a rule artifact |
| v3+ declared-refs-outside-requires set (~1510) | `packages/derivation/package_validation.py` | declared `ref` names not validated |
| `_SUPPORTED_SEMANTIC_SCHEMAS` (262) | `packages/derivation/package_validation.py` | **loud** `MEMBER_SCHEMA_UNSUPPORTED`: the v8 citizen is schema-valid but not package-admissible |
| `rules` membership set (102–105) | `packages/derivation/live.py` | **silent**: v8 never enters `ctx.rules`, so the rule never saturates and every C0-shaped assertion passes for the wrong reason |
| `RECORD_CODES` | `packages/derivation/runner.py` | **silent**: `NOMINEE_ALLOCATIONS_EXCEED_REPORT` collapses to `DEPENDENCY_INVALID` (`record_named_block`), so C4 records the wrong reason |
| `rule-artifact` allowlist (36+) | `packages/derivation/authorization_closure.py` | parallel authorization gate does not admit v8 |
| `_iter_bound_source_names` walker + reachability edge | `packages/derivation/package_validation.py` | **silent**: no edge to the allocation vocabulary, so an unreachable or omitted bundle validates clean |
| `bound_sources` edge in the closure builder | `packages/derivation/authorization_closure.py` | **silent**: the allocation dependency is outside the closure, so the authorization digest does not change when it changes |
| `consumed` set (1797) | `packages/derivation/package_validation.py` | recorded-non-composable and related consumed-input restrictions stop applying to `bound_sources` inputs |
| coordinator dispatch registry check | `packages/derivation/package_validation.py` | **silent**: without it, a schema-valid `bound_sources` rule with no binding path would be package-admitted and then never evaluate |

The two silent failures are the reason Track 2's kill conditions must assert a
**positive** nominee outcome (C1 publishes `$450`; C4's closing-record row
carries the exact code), not only the absence of a wrong one.

**This table under-counted (Track 1 review, non-blocking 4).** Track 1 found and
edited further version-enumerating sites beyond the six listed — in `marshal.py`
and additional sets in `runner.py`, `records.py`, and `package_validation.py`.
The list above is therefore a **floor, not a census**: any future
`rule-artifact` or record successor must re-enumerate rather than trust it.

**Not done, and must not be assumed done (Track 1 review, non-blocking 5).**
ADR-0074 Decision 3f's selection order is a **contract**; `explanation.py` still
carries the committed producer lookup unchanged. The ADR already records that
walker as wrong for this rule and defers `explain()` of
`NOMINEE_ALLOCATIONS_EXCEED_REPORT` (the inherited `npe-walk.v3` lag). No track
of this milestone changes it.

#### `AccessLog` entries

New field `bound_source_names: set[str]` on `AccessLog`
(`evaluator.py` 50–61). The op adds `expr["name"]` there. It does **not**
add to `access.collects` (that is the P2 leak vector:
`dependency_pins_for_access` 378–385 pins every `self.source_fids[name]`).
`refs` of the box-1 type still go to `access.refs`. `closure_reads` stays
empty: this op never reads closure.

#### Pin conversion

The outline’s “discard `access.collects` then `dependency_pins_for_access`”
assumed a `collect`. That discard is **moot** here (`collects` is empty)
and must not be replaced by a walk of `bound_source_names` against
`source_fids`.

After `evaluate(rule["value"], local_env, access)`:

1. Build `present_pins` = rule pin + citation pin + adoption + governance
   + input pin of this report finding + input pin of **each of this
   group’s** allocation findings (sorted by allocation `fact_id`).
2. Call `run.dependency_pins_for_access(access)` **without** adding a
   `bound_source_names` walker. Live fields that convert are `refs`
   (box-1 will not resolve on `symbol_pin` because the type is in
   `collect_names` and marshal skips InputFinding fallback — Gate P3
   review Attack 1; `present_pins` is the only report-finding cover),
   plus `parameters` / `tables` / `operations` if the expression actually
   reads them (none in the paper sketch). `collects` and `closure_reads`
   are empty.
3. Union, then `_sorted_pins` (`runner.py` 207–209; dedupes by
   `(role, id, version)`). Finding-level pins may include the rule pin
   with `role` equal to `rule["role"]` (`pins_for` 456–458). Disposition
   rows strip `_LEDGER_EXCLUDED_PIN_ROLES` (`computation`,
   `applicability`, `field-mapping`, `cross-form-bridge` — `runner.py`
   148–150), which is why the paper v9 instances do not carry a
   `computation` pin (`derivation-record.v8` pin `role` enum does not
   include it).

Invariant: a supported result pins exactly its own report and its own
group’s allocations, and no others. C10/C12 leak into pins is a kill-1
failure.

Reachability (unchanged from outline §1 half 1): register
`tax.us.nominee-allocation.amount` in `collect_source_names` gated on the
nominee rule id (`live.py` 147–163 pattern) so marshal emits `SourceFact`s
for the coordinator’s universe. That registration is not a family and is
not this op.

### R2 — disposition semantics (consequences of R3)

**(a) No-selected-group rule disposition.** Consequence of R3’s empty-
selection row: `inapplicable` with `no_groups_selected: true`. Not a
publication, not `guard_result: false` (the citizen’s `when` is `true`;
`finalize_unreached` 1574–1580 records false-guard only when the preflight
is actually false), not `superseded_by`, not `blocked` with
`DEPENDENCY_ABSENT` / `SOURCE_SET_UNCLOSED` / any other existing code.
No committed v8 shape is honest (`derivation-record.v8.schema.json`
144–149 enum; inapplicable `oneOf` 87–110; charter-review Attack 3
re-verified). v9’s third inapplicable form is the additive field.

**(b) `missing` on an over-allocation block.** Consequence of R3’s group
identity: **empty `missing`**. The report is present and pinned; `missing`
names absent dependencies (`runner.py` attachment comment at 978;
evaluator `block` emits `EvalBlocked(code, [])` at 161–162; accrued
citizen `blocked.missing: []`). Group identity is the suffixed `symbol`,
not `missing=[report_fact_id]`. Pins identify the contributing findings
for displacement (ADR-0010) but are not the consumer join key.

**(c) C0-only attempt outcome.** Consequence of R3’s attempt table:
return `"inapplicable"`, not `"published"`. `_execute` still ignores it;
`resolved.add` after the loop still runs.

**C13 unchanged:** `DEPENDENCY_ABSENT` with `missing=[composed report_fact_id]`
and, per R3, `symbol` set to the suffix so Decision 4 can select it.

### 1. Authority-lifecycle table

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| Current box-1 finding `tax.us.2025.f1099int.box1-interest` | The payer reported this amount of taxable interest on this Form 1099-INT for this tax year | Payer + statement + tax-year (report fact id from `REPORT_FACT_TYPE` / `fact_id_for`; `packages/tax/report_statement_identity.py`) | Kernel `compute_currency` current standing of that `fact_id` | Same-identity correction; retraction; taxpayer-entity or other displacement root that drops the finding from `current_finding_ids` (C5, C13) |
| Current nominee-allocation finding `tax.us.nominee-allocation.amount` (per recipient) | A workspace actor attested that this amount of the identified report belongs to this named other person. Ordinary proposition only; not a tax result | Payer + statement + tax-year + recipient (`nominee-allocation.bundle.json` identity_keys 13–18) | Kernel current standing of that `fact_id`; assertion act for attribution (recovery, not a tax pin) | Correction of the same `fact_id`; `act-finding-retracted.v1`; entity supersession of payer, statement, or recipient (C6) |
| Adopted rule `tax.us.2025.rule.interest.nominee-reduction` @ v1 (`rule-artifact.v8`) | Declared arithmetic: sum the coordinator-bound allocation values; if the sum is `gt` this report’s amount, block; else publish the sum as the report-scoped nominee reduction | The adopted package graph (exclusive execution projection, ADR-0027) | Package adoption pin; citation pin; `bound_sources` binding supplied by the coordinator for one nonempty group | Package supersession / different exclusive adoption; rule-citizen version change |
| Citation `tax.us.2025.citation.interest.nominee-reduction` v1 | Schedule B Part I nominee-distribution *mechanic* (form guidance, not controlling law). Gate P1: IRC §61(a)(4) / Treas. Reg. §1.61-7(a) include the interest; the subtraction is the 2025 Schedule B instruction | `authority.family = irs-instructions`, `form_id = 1040-SCH-B`, `tax_year = 2025` (`citation.v1` schema) | Package membership of this citation | Citation version change; package no longer pinning it. **Not reused:** `tax.us.2025.citation.scheduleb-adjustment.nominee` (see claim-reuse) |
| Package adoption of `package.core-calculations` v36 | Exclusive adopted graph that contains the nominee rule, allocation vocabulary, reduction vocabulary, and citation. v35 workspaces do not silently gain the rule | The adoption act / pin (`act-package-adoption`) | Verified release (ADR-0033) | Different package version adopted; adoption withdrawn |
| `reporting_year` | **Execution scope, not a fact.** Which relevant `SourceFact`s the coordinator inserts into the universe. Every *relevant* source is validated **first**, from structured `SourceFact.keys` — never by re-parsing a rendered `fact_id` — and missing or inconsistent required identity raises `NomineeIdentityError` rather than being filtered away. When relevant sources exist and the run declares **no** reporting year, execution likewise **raises `NomineeIdentityError`**; it does not quietly produce an empty universe. Only a **different, successfully established** tax year is excluded by the year filter. Same field `RunContext.reporting_year`, produced by `live_coordinate_run` from `run_scope["year"]` (`packages/tax/nominee_consequences.py` `_build_universe` / `_validated_keys`; `live.py`; `runner.py`) | The run, not a taxpayer proposition | The run request’s year | A different run with a different year. A 2024 allocation is not a C13 in a 2025 execution |

Not listed, by prohibition: a source-family or closure finding for
`tax.us.nominee-allocation.amount`; any payment/credit/transfer fact.

Storage identity and tax-year-alone are not authority scope. An allocation
whose recipient changes is a different proposition; a box-1 correction at
the same payer+statement+tax-year is the same proposition with a new current
finding.

### 2. Empty/nonempty authority matrix

“Closed empty family” is **N-A** for allocations. R1’s `bound_sources` has
**no named set** and is not a closure claim: it reads a coordinator-injected
`Environment.bound_sources` list and never consults `closed_sets`. Substituting
a closed-empty allocation family here is a Track 0 `FAIL` against stop
conditions 1–2.

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Report-only (C0; allocation-free reports in C7/C12). Allocation emptiness is **not** a closed family | No current allocation finding for that report in this execution. Not a completeness proposition, not a user denial | Nominee rule not invoked for that group (C0 option 1) | No nominee publication or per-report nominee block. Box-1 still calculated. If the whole universe is this state, R2(a) records the rule-level `no_groups_selected` row and `resolved.add` skips `finalize_unreached` | Box-1 family collect / b1-subtotal available without nominee facts (`rule.f1099int-b1-subtotal.json` collects `tax.us.2025.f1099int.b1`). Line 2b v6 unchanged |
| N-A — required allocation-family universe missing | **N-A.** There is no allocation family to be missing | N-A | N-A | N-A |
| Both-present, supportable (C1, C2, C3, C8, C11, C of C10) | Current box-1 finding and current allocation finding(s) for that report; sum `<=` report (`gt` is false) | Consequence evaluation once | Publish suffixed reduction; observed remainder = report − reduction; pins = this report + this group’s allocations | Box-1 still independently calculated. No new `requires` on line 2b. Legacy nominee subtotal unconsumed |
| Both-present, over-allocated (C4, C5b, A of C10/C12) | Same current facts; sum `>` report | Consequence evaluation once; declared `block` | `blocked` `NOMINEE_ALLOCATIONS_EXCEED_REPORT`, `missing=[]`, suffixed `symbol`, no reduction finding. **No settled unreduced nominee remainder** (the dependent consequence blocks; box-1 is not a nominee remainder) | Box-1 still independently calculated. Unrelated reports unaffected (C10 C publishes). Line 2b / Schedule B / legacy path unchanged |
| Allocations without a current report (C13) | Current allocation finding(s); composed report fact id has no current box-1 finding | No rule arithmetic | `blocked` `DEPENDENCY_ABSENT`, `missing=[composed report_fact_id]`, suffixed `symbol`, pins = allocation finding(s) only. No invented `$0`, no historical report amount | Box-1 collect has nothing for that report (independent). Not a box-1 halt |

### 3. Late-authority counterexample (C5/C6)

Trace uses synthetic `demo.payer.a` / `demo.stmt.a` / 2025 / `demo.pat`.
Displacement is ADR-0010 (a superseded pinned input displaces its consumers
to non-current), **not** family membership.

```text
attest → compute → correct/retract → recompute → reassert → recompute
```

| Step | Current facts | Nominee result | What becomes unusable, and why |
| --- | --- | --- | --- |
| Attest | Box-1 A `$1,200` (finding `demo.f.box1.a1`); allocation `demo.pat` `$450` (finding `demo.f.pat.1`) | — | — |
| Compute (C1) | Same | Published reduction `$450` at suffix A; observed remainder `$750`; input pins `demo.f.box1.a1` and `demo.f.pat.1` | — |
| Correct report A to `$1,000` (C5a) | `demo.f.box1.a1` displaced by `demo.f.box1.a2` `$1,000`; `demo.f.pat.1` still current | Recompute publishes `$450` / observed `$550`; pins `demo.f.box1.a2` + `demo.f.pat.1` | The `$450`/`$750` finding is unusable because its report **input pin** `demo.f.box1.a1` was displaced (ADR-0010). Marshal does not emit displaced findings (`marshal.py` current-finding loop) |
| Separately: correct report A to `$400` (C5b) | `demo.f.box1.a3` `$400`; `demo.f.pat.1` current | C4-shaped block; no `-$50`; no reduction finding | Same pin displacement of `demo.f.box1.a1`. A design that reused the prior published `$450` would present a stale remainder |
| Correct allocation `demo.pat` to `$400` (C6 first) | `demo.f.pat.1` displaced by `demo.f.pat.2` `$400`; box-1 A `$1,200` current | Reduction `$400` / `$800`; pins current box-1 + `demo.f.pat.2` | Prior `$450` finding unusable because allocation input pin `demo.f.pat.1` was displaced |
| Retract `demo.f.pat.2` (C6 middle) | No current allocation for A; box-1 A current | C0-shaped: no nominee publication for A; `$1,200` continues; if this is the only former group, the `no_groups_selected` row is the rule-level account | Prior `$400` finding unusable because its allocation input pin was retracted (`act-finding-retracted.v1`, ADR-0073). Retracted finding id must not appear as an input pin (kill 3) |
| Reassert `demo.pat` `$250` (C6 last) | New current finding `demo.f.pat.3` `$250` at the same allocation `fact_id` | Reduction `$250` / `$950`; pins current box-1 + `demo.f.pat.3` | History remains in `state.findings` / recovery’s retracted records and does not contribute. Reassertion is a new current answer (ADR-0010 / ADR-0073), not a revival of `demo.f.pat.1` or `.2` |

No family membership changes in this trace. `reporting_year` is unchanged.

### 4. Reused-claim semantic/lifecycle equivalence

**Policy transferred from ADR-0070/0071, not pairing-specific machinery.**

| Policy | Source | Nominee use |
| --- | --- | --- |
| Whole-set block; no winning subset, clamp, or published misleading remainder | Plan Behavior 3; ADR-0070 Decision 8 (no allocation policy) | Declared `choose`/`compare gt`/`block`; remainder observed only on a supported group |
| Mixed report outcomes; one group’s block does not suppress another | ADR-0070 Decision 7 (named, scoped blocking) | Coordinator loop; no `dispatch_current_year_subtotal_on_run`; no `_retract_pairing_scoped_publications_for_blocked_groups` |
| Declared arithmetic owns the number and the block | ADR-0006; ADR-0071 Decision 3 | `evaluate(rule["value"], local_env)` with `bound_sources` + `add` + `compare` + `block` |

**Not transferred:** pairing-typed dispatch (`evaluate_pairing_scoped_rule`
iterates `PAIRING_TYPE`); aggregate publication grouping by pairing
`right_fact_id`; line-2b-bound subtractands; separately published `True`
verdict; dummy `{"op":"add","args":["0"]}` aggregate citizen.

**Negative proof, four outline-§8 symbols** (each fails at least one of
proposition / identity-lifecycle / authority-explanation):

| Existing symbol | Same proposition? | Same identity / lifecycle? | Same authority / explanation? |
| --- | --- | --- | --- |
| `tax.us.2025.interest.current-year-adjustment.pairing-scoped\|{pairing_fact_id}` | **No.** Accrued-interest pairing proposition (ADR-0071): return of capital at acquisition, not “this report’s interest is allocated to another person” | **No.** Identity is the pairing fact id, not payer+statement+tax-year+recipient allocations. Lifecycle is pairing + acquisition + report, not allocation retraction | **No.** Citation is the accrued-interest Schedule B mechanic; pins are pairing/left/right, never `tax.us.nominee-allocation.amount` |
| `tax.us.2025.interest.current-year-adjustment-subtotal` | **No.** Run-wide sum of those pairing publications | **No.** Run-wide, not report-scoped. Externally bound to `rule.form1040-line2b` v6 (`requires` and subtract, `rule.form1040-line2b.v6.json` 42–52, 77–79) | **No.** Line-2b subtractand. Reuse would force the integration-surface artifact and fire T0-F5 |
| `tax.us.2025.interest.current-year-adjustment.aggregate-supported\|{report_fact_id}` | **No.** Aggregate accrued-interest supportability *verdict* (`True`), not a nominee reduction amount | **No.** Grouped from pairing-scoped publications by `right_fact_id`, not from allocation findings. ADR-0070 Decision 9 retracts pairing publications on aggregate block; nominee never publishes per-allocation | **No.** Code `AGGREGATE_ACCRUED_EXCEEDS_REPORT` names a different proposition (kill 2 forbids reusing it) |
| `tax.us.2025.interest.scheduleb-nominee-subtotal` | **No.** Collects legacy `tax.us.2025.scheduleb.adjustment.nominee.amount` (user-entered Schedule B adjustment-instance) | **No.** Identity is tax-year + adjustment-instance, not payer+statement+recipient. Externally bound to line 2b v6. Coexistence tests already show the new allocation is not a pin of this rule (P2 Attack 1) | **No.** Citation `tax.us.2025.citation.scheduleb-adjustment.nominee` is bound to the legacy adjustment-instance rule |

**Citation decision.** Default **new**
`tax.us.2025.citation.interest.nominee-reduction` v1,
`authority: {family: irs-instructions, form_id: 1040-SCH-B, tax_year: 2025}`.
Reusing `tax.us.2025.citation.scheduleb-adjustment.nominee` **fails** the
three-part test: same instruction family, but that citizen is the citation
of the legacy adjustment-instance rule whose identity, lifecycle, and
line-2b binding this milestone must not inherit. Similar form-guidance
source is insufficient (plan Decision 5).

### 5. Neighboring capability dependency diff

| Neighbor | Prerequisites before | Prerequisites after | When the nominee rule has no activity (C0) |
| --- | --- | --- | --- |
| Box-1 family collect (`rule.f1099int-b1-subtotal.json`, family `tax.us.2025.f1099int.b1`) | Current box-1 findings + family closure for empty collect | **Unchanged.** A blocked nominee reduction must not halt box-1. Return integration is a later milestone | Unchanged; C0 box-1 `$1,200` still calculated (kill 7 executable half) |
| Legacy nominee path (`rule.scheduleb-adjustment.nominee-subtotal.json` / family `tax.us.2025.scheduleb.adjustment.nominee`) | Legacy adjustment-instance facts + that family’s closure | **Unconsumed.** v36 keeps those members. Kill 8 fails if a nominee-reduction pin is a current legacy finding | Unchanged |
| Line 2b v6 (`rule.form1040-line2b.v6.json`) | The ten `requires` listed at 42–52, including `scheduleb-nominee-subtotal` and `current-year-adjustment-subtotal`; not the new prefix | **No new `requires`.** The new prefix is unnamed in that citizen (P3 review Attack 10 grep) | Unchanged |
| Schedule B attachment (`rule.attachment.schedule-b.v5.json` 57–71) | Itemizes `nominee_distribution` against the **legacy** family / `scheduleb-nominee-subtotal` | **No itemization of the new prefix.** T0-F5 untouched | Unchanged |
| Information reporting | Unimplemented; authority-indexed only | Still unimplemented. No normalized §6049 predicate | Unchanged |

`explain()` of `NOMINEE_ALLOCATIONS_EXCEED_REPORT` is out of scope, the same
inherited lag the accrued codes already have versus `npe-walk.v3`.

No new feature-specific prerequisite is imposed on any neighbor. Blast
radius: none that this design introduces.

### 6. Integration surface: **N-A**

The selected symbol `tax.us.2025.interest.nominee-reduction` is not
externally bound. No form field, attachment, package entrypoint, or
presentation join names it (P2 Attack 9; P3 review Attack 10).

| Consumer | Binding artifact or join | Cardinality it expects | Satisfied by the design? |
| --- | --- | --- | --- |
| *(none)* | — | — | — |

**Stop, not a Track 1 surprise:** binding this prefix to line 2b would make
this artifact mandatory (exactly-one producer per symbol on every path,
presentation-model probe) and would fire T0-F5 (Schedule B Part I tie-out
when a nonzero subtractand is not itemized). That binding is out of scope.

### Substrate boundary — non-injective fact-id rendering

**What is supported.** Ordinary punctuation is supported, including ordinary
commas in payer names and statement references. `"Demo Bank, N.A."` and a
statement reference like `"acct 12,345 / copy B"` associate correctly and publish
the expected reduction; regressions on the real `live_coordinate_run` path cover
both. Track 1 does not reject or rewrite ordinary punctuation.

**The substrate defect.** `packages/kernel/facts._fact_id` joins `name=value`
pairs on `,` **without escaping**, so the rendering is **non-injective**. Two
genuinely distinct Form 1099-INT box-1 identities render byte-identically today:

| Inputs | Rendered box-1 fact id |
| --- | --- |
| payer `a,statement=a::statement::b`, statement reference `c` | identical |
| payer `a`, statement reference `b,statement=a,statement=a::statement::b::statement::c` | identical |

`SourceFact.keys` does **not** repair this. Structured keys avoid *re-parsing* a
rendered id; the kernel lattice (`facts.facts_of`) is itself a dict keyed on the
rendering, so a collision collapses two facts before any consumer sees either.

**What the coordinator actually does.** The nominee coordinator conservatively
rejects a relevant source whose component value contains a delimiter-shaped
`,<identity-key-name>=` sequence, raising `NomineeIdentityError`. This is a
superset of the genuinely colliding cases. Its purpose is narrow and should be
described narrowly:

- it **protects nominee calculation** from silently computing on an ambiguous
  rendered identity; and
- it **does not repair** the kernel's non-injective fact-id representation.

**It is an execution-time guard, not an intake or admission gate.** The existing
recording contracts can admit such values long before the coordinator sees them:
`assert_nominee_allocation` and the 1099-INT report path accept these strings and
commit findings for them. Nothing refuses them at intake.

**Measured failure boundary (not yet a clean product refusal).** Through
`live_coordinate_run`, `NomineeIdentityError` is raised *after* output paths are
reserved and the derivation start record is appended. The observed state after
the raise is:

- `records/derivation_records.jsonl` containing exactly one `started` record and
  **no** `completed` record — the run is left **open**;
- `outputs/out.json` and `outputs/out.presentation.json` present and **empty
  (0 bytes)**.

So this is an in-flight exception, **not** a pre-run refusal and not a
`Refusal`-shaped product outcome. `tests/test_nominee_consequences_live.py`
carries a regression that observes exactly this boundary, so later work cannot
accidentally describe it as a pre-run refusal.

**Bounded Track 1 conclusion.** Correct nominee consequences are established for
identities that pass this guard — that is the scope of Track 1's result, and it
is not weakened by the boundary above.

**Genuine future requirement, not chosen here.** Closing this properly needs
**either**:

1. a **general identity repair** — escaping or a structured identity
   representation in the kernel, which changes the general fact-identity contract
   and touches every fact id in the corpus; **or**
2. a **real pre-execution intake/admission restriction** with explicit failure
   semantics — refusing or normalizing such values where findings are recorded,
   with a defined product-visible outcome.

This milestone selects neither, and Track 1's coordinator exception is **not**
coverage for either. Track 2 proceeded while preserving this explicit substrate
dependency.

### Known limitations affecting correctness

| Limitation | Why it can affect correctness | Owner disposition line |
| --- | --- | --- |
| `COLLECT_TARGET_NOT_FAMILY` is inactive for the current package generation: the `universe_guard_active` allowlist ends at `artifact-package.v17` (`package_validation.py` 1692–1708; ADR-0035 production condition), while the Track 0 measurement was taken against **then-production v35 / `artifact-package.v26`** and the delivered **v36 uses `artifact-package.v28`**. Both generations are beyond the allowlist, so the guard has never bound a `rule-artifact.v7` collect | A future repair of the allowlist would start rejecting ordinary `collect` of non-family types. **This rule does not `collect`.** R1’s `bound_sources` remains valid if the intended guard is applied to current package schemas. A builder who later switched this rule to ordinary `collect` would then fail admission — that is desired | **Recommended standing (this milestone follows it):** do not repair the allowlist here; do not depend on it remaining inactive; never admit a nominee-allocation source family if the guard is repaired. Owner may later charter a validator-allowlist repair as a separate bounded unit |
| Allocation `tax-year` literal domain `{2024, 2025}` (`nominee-allocation.bundle.json` 16) versus box-1 `{2025}` (P2 Attack 2 Foreman note) | A current 2024 allocation is schema-admitted. Without the coordinator year filter it would either leak into a 2025 sum or insert a false 2024-keyed C13. The coordinator's year filter on **both** validated source sets drops it before classification. This milestone does not shrink the allocation schema | **Recommended standing:** accept as a domain-width asymmetry, not a live 2025 identity mismatch. Fixtures stay on 2025; the cross-year case is the discriminating extra row. Do not treat a 2024 allocation as a 2025 C13 |

### Schema-intent (record only; no schema file)

Settled after R1/R2/R3. Three additive successors, each with a ledger event
under `schema-ledger/events/nominee-interest-tax-consequence-supportability/`
on `milestone-schema-ledger` (`change_kind: additive`). Track 1 writes the
immutable schema files, runs `write_manifest` (inspect that existing
checksums do not change), and commits the positive instances **before** any
coordinator emits `NOMINEE_ALLOCATIONS_EXCEED_REPORT`.

| Family | Version | Path | Why this track needs it |
| --- | --- | --- | --- |
| `rule-artifact` | v8 | `packages/schemas/derivation/rule-artifact.v8.schema.json` | R1: `bound_sources` op |
| `artifact-package` | v28 | `packages/schemas/derivation/artifact-package.v28.schema.json` | Admit `rule-artifact.v8` as a member schema (v26 enum ends at v7; v27 is already proposed by another milestone) |
| `derivation-record` | v9 | `packages/schemas/derivation/derivation-record.v9.schema.json` | R2/R3: new code + `no_groups_selected` inapplicable form |

Event ids (appended on the ledger branch; `replaces_event: null`):

- `20260909T044800Z-rule-artifact-3f4c88`
- `20260909T050200Z-artifact-package-190f6f`
- `20260909T044802Z-derivation-record-6168c8`

**ADR-0074** is required for the grouped-rule cardinality contract (R3).
Track 0 does not write it. No `npe-walk` successor is required to record
the consequence.

### Paper positive v9 instances (Payload Instantiation Gate target)

Track 1 commits these (or byte-equivalent honest instances) alongside
`derivation-record.v9.schema.json`. They are paper here.

**Instance A — over-allocation closing record (the new code).** Every
required v9 field honest. `missing` is empty; `symbol` identifies the
group; pins name the present report and the group’s allocations.

```json
{
  "schema": "derivation-record.v9",
  "record_id": "demo.record.nominee-over-allocation",
  "run_id": "demo.run.nominee-c4",
  "phase": "completed",
  "workspace_revision": 1,
  "governance_pins": [
    {"role": "governance", "id": "governance.constitution", "version": "v1"}
  ],
  "adoption_pin": {
    "role": "adoption",
    "id": "demo.package.core-calculations",
    "version": "v36"
  },
  "stop_reason": "saturated",
  "dispositions": [
    {
      "artifact_id": "tax.us.2025.rule.interest.nominee-reduction",
      "disposition": "blocked",
      "code": "NOMINEE_ALLOCATIONS_EXCEED_REPORT",
      "missing": [],
      "symbol": "tax.us.2025.interest.nominee-reduction|tax.us.2025.f1099int.box1-interest|payer=demo.payer.a,statement=demo.payer.a::statement::demo.stmt.a,tax-year=2025",
      "pins": [
        {"role": "citation", "id": "tax.us.2025.citation.interest.nominee-reduction", "version": "v1"},
        {"role": "adoption", "id": "demo.package.core-calculations", "version": "v36"},
        {"role": "governance", "id": "governance.constitution", "version": "v1"},
        {"role": "input", "id": "demo.f.box1.a1", "version": "v1", "origin": "assertion"},
        {"role": "input", "id": "demo.f.pat.1", "version": "v1", "origin": "assertion"},
        {"role": "input", "id": "demo.f.kim.1", "version": "v1", "origin": "assertion"}
      ]
    }
  ]
}
```

**Instance B — C0-only no-selected-group row** (the additive inapplicable
form). Not a publication, not a false guard, not a false block.

```json
{
  "schema": "derivation-record.v9",
  "record_id": "demo.record.nominee-c0",
  "run_id": "demo.run.nominee-c0",
  "phase": "completed",
  "workspace_revision": 1,
  "governance_pins": [
    {"role": "governance", "id": "governance.constitution", "version": "v1"}
  ],
  "adoption_pin": {
    "role": "adoption",
    "id": "demo.package.core-calculations",
    "version": "v36"
  },
  "stop_reason": "saturated",
  "dispositions": [
    {
      "artifact_id": "tax.us.2025.rule.interest.nominee-reduction",
      "disposition": "inapplicable",
      "no_groups_selected": true,
      "symbol": "tax.us.2025.interest.nominee-reduction",
      "pins": [
        {"role": "citation", "id": "tax.us.2025.citation.interest.nominee-reduction", "version": "v1"},
        {"role": "adoption", "id": "demo.package.core-calculations", "version": "v36"},
        {"role": "governance", "id": "governance.constitution", "version": "v1"}
      ]
    }
  ]
}
```

The `symbol` string in instance A is illustrative of the suffix shape
(`prefix|{report_fact_id}`). Track 1’s committed instance must use a
`report_fact_id` produced by `derive_1099int_box1_fact_id` (kill 4’s
independent composer), not a hand-waved concatenation that disagrees with
`_fact_id`.

Nothing ever emits `NOMINEE_ALLOCATIONS_EXCEED_REPORT` against v8.

## Verification

Implementation tracks ran focused schema, package-validation, supportability,
consequence, and nominee allocation tests; executable C0–C8 and C10–C13 cases through the
real runner; and kill tests for the negative properties, including cross-report
masking, over-allocation, stale currentness, the report-with-no-current-finding
fail-closed result, payment/reduction decoupling (a structural
no-payment-dependency check — no usable committed payment/credit/transfer fact
exists), and legacy consumption. Substrate changes ran the full suite. The PR's
green `verify` check is the merge gate and the record of the full suite. Do not
repeat it merely to manufacture another result.

## Data safety

Only obviously synthetic identifiers and amounts may enter fixtures and
documents. Use `demo.*` or `demo-*` identities. No personal forms, personal
allocations, personal recipient names, workspace paths, credentials, generated
private artifacts, or real refusal reasons enter the repository or review.

## Success and stop conditions

The milestone succeeded: a real execution takes a current report and its
current attributed allocation assertions and produces an independently supported,
report-scoped nominee reduction — remainder observed only, as Track 0
justified — with correct blocking, isolation, currentness, and provenance, without
pretending that return presentation, legacy migration, or information reporting
has been solved. The result is bounded to identities that pass the ambiguity
guard.

None of the stop conditions fired. They remain the conditions that would have
returned a decision rather than forcing implementation:

1. enumerating every current recorded allocation for one report — including the
   empty result — cannot be expressed without asserting a separate completeness
   proposition, turning absence into a user denial, or claiming that no
   real-world allocation exists;
2. the only available enumeration route imports source-family closure or another
   proposition the product did not select — for example, using source-family
   membership, a family horizon, or family-completeness collect (with or without
   a coordinator wrapping it) to obtain the report's current allocation set;
3. a proposed reuse fails proposition, identity/lifecycle, or
   authority/explanation equivalence;
4. accurate tax consequences require one normalized information-reporting
   predicate;
5. the selected symbol is already externally bound and cannot be introduced
   without entering the deferred Schedule B defect;
6. supportability cannot block one report without suppressing unrelated correct
   report groups; or
7. implementation requires relaxing retraction, provenance, schema-publication,
   or data-safety contracts.

## Exit criteria

All ten are met.

1. P1, P2, and P3 were independently reviewed and their findings absorbed
   before the Track 0 charter.
2. Track 0's adversarial closure contains no unresolved `FAIL` and every reused
   claim has a property-level proof.
3. C0–C8 and C10–C13 execute through the real runner with exact expected values,
   dispositions, source isolation, and currentness, for identities that pass
   the ambiguity guard.
4. Supported results pin the exact current report, every contributing current
   allocation, the supportability authority, adopted rule and version, and tax
   citation; blocked results preserve an explainable report-scoped reason.
5. No ordinary allocation is interpreted as a user-supplied tax conclusion, and
   no remainder is described as independently proven beneficial ownership.
   Concretely, no published finding label, disposition, or pin explanation
   describes the remainder as proven beneficial ownership or the C0 no-allocation
   result as a user denial.
6. Payment is not required for the nominee reduction, proved by C8. That it is
   not sufficient is enforced structurally — the reduction rule declares no
   payment/credit/transfer dependency and no reduction arises without a current
   allocation. No usable committed payment/credit/transfer fact exists; no claim
   rests on a nonexistent payment citizen.
7. The authority-indexed reporting boundary remains explicit and no normalized
   reporting obligation is implemented.
8. No changed package or surface claims line-2b or Schedule B completeness; the
   T0-F5 gate and the later legacy/return integration boundary remain explicit.
9. No legacy nominee fact is consumed, converted, retired, or double-counted by
   the new consequence path.
10. Focused verification, required full-suite lanes, governance lint, envelope
    scan, diff check, and the independent Track 2 review are complete, with CI as
    the merge gate of record.

## Next-stage input contract

The later **legacy-and-return-integration** milestone may consume exactly this
internal capability, and nothing that was withheld:

- **Prefix.** `tax.us.2025.interest.nominee-reduction`. Not bound to line 2b or
  Schedule B. Binding it would make the Track 0 integration-surface artifact
  mandatory and would fire T0-F5.
- **Symbol and pin topology.** A published or blocked group outcome is
  identified by the suffixed symbol
  `tax.us.2025.interest.nominee-reduction|{report_fact_id}`. Pins name the
  current report finding and every current allocation in that group (C13 pins
  the allocations only). Attribution remains on the source allocation's
  assertion act; it is not copied into the tax proposition.
- **Grouped-ledger shape.** One identified disposition row per classified
  report-group, same `artifact_id`, mixed statuses expected. Over-allocation
  carries `NOMINEE_ALLOCATIONS_EXCEED_REPORT` and empty `missing`. C13 carries
  `DEPENDENCY_ABSENT` with `missing=[composed report_fact_id]`. ADR-0074
  governs the exact rule id only.
- **C0-as-absence.** A report with no current allocation produces no nominee
  publication and no per-report nominee row. When the whole universe is
  report-only or empty, the adopted rule is accounted for by one unsuffixed
  `inapplicable` / `no_groups_selected` row. Absence is not a user denial and
  not independently proven ownership.
- **T0-F5 is a hard gate on that stage.** No production or integration unit
  may be accepted as complete for a state combining required Schedule B
  presentation with a nonzero pairing-scoped current-year adjustment until
  T0-F5 is repaired. This milestone did not repair it and did not itemize the
  new prefix.
- **Substrate boundary, carried forward unchanged.** `facts._fact_id` joins
  `name=value` on `,` without escaping, so the rendering is non-injective.
  The coordinator conservatively rejects delimiter-shaped
  `,<identity-key-name>=` values. Ordinary punctuation, including ordinary
  commas in payer names and statement references, is supported. This is an
  **execution-time guard, not an intake or admission gate**: the recording
  contracts admit such values first, and through `live_coordinate_run` the
  guard raises after output reservation and the start record, leaving an open
  run and empty reserved outputs. It is not yet a clean product refusal. The
  result is bounded to uniquely rendered identities. Closing the boundary
  needs **either** a general identity repair **or** a real pre-execution
  intake restriction with explicit failure semantics; this milestone selects
  neither, and the coordinator exception is not coverage for either.

The later stage also inherits, unchanged: no source-family or closure mapping
for `tax.us.nominee-allocation.amount`; remainder observed-only; the
authority-indexed, unreconciled information-reporting boundary; the
non-resumable allocation-recording hard gate.

## Execution record

Closed 2026-09-09. Retrospective:
[`2026-09-09-nominee-interest-tax-consequence-supportability.md`](../../../milestone-retrospectives/2026-09-09-nominee-interest-tax-consequence-supportability.md).

| Unit | Result |
| --- | --- |
| Gate P1 — product and tax boundary | Independently reviewed (Gate P1's independent review). Six blocking findings absorbed: controlling basis bounded to §61(a)(4) / §1.61-7(a) plus the Schedule B mechanic; Decision 6 no longer lists Schedule B instructions as reporting authority; C0 no longer pre-settles empty as a `$0` reduction; C9 no longer requires an out-of-scope transfer fact; C7 split and C12/C11 added |
| Gate P2 — committed artifact map | Independently reviewed (Gate P2's independent review). Four blocking gaps absorbed into Gate P3: live reachability, nonempty report-scoped grouping, empty enumeration without source-family closure, and execution cardinality for mixed report groups. C9 is a structural dependency prohibition |
| Gate P3 — executable design | Independently reviewed (Gate P3's independent review). Two blocking admission/kill-7 defects repaired in the outline. A later owner directive withdrew the sentinel-`source_set` repair and reopened R1, R2, and R3 |
| Track 0 — consequence contract | Independently reviewed (Track 0's independent review); findings absorbed. R1 `bound_sources` on `rule-artifact.v8`; R2 as consequences of R3; R3 grouped-ledger shape requiring ADR-0074. Six adversarial-closure artifacts complete; integration-surface **N-A** |
| ADR-0074 | Independently reviewed (ADR-0074's independent review); owner-directed repair rounds; **accepted** 2026-09-09. Exact-rule narrowing of ADR-0020 Decisions 1/1a/4; `bound_sources` operator contract; no reusable grouped-rule class |
| Track 1 — implementation | Independently reviewed READY with no blocking finding (Track 1's independent review). Five non-blocking findings absorbed: C10 `len==2` before symbol collapse; authorization-closure kill on the real v36; v7-admission probe names v26 and v28; allowlist table recorded as a floor; Decision 3f walker recorded as not done |
| Track 1 owner-directed repair — stop parsing | Coordinator had reconstructed a report fact id by parsing an allocation fact id, so an ordinary comma in a payer name produced `DEPENDENCY_ABSENT` instead of the reduction. Repaired by carrying structured `SourceFact.keys` from the kernel lattice and never re-parsing. Citation pin no longer manufactured |
| Track 1 owner-directed repair — fail loudly | Missing or inconsistent identity was a silent filter that turned a real allocation into C0 or a smaller total. Repaired by validating before filtering and raising `NomineeIdentityError`. The live isolation test, which had executed only one of its two reports, was rewritten as one two-report live run. The identity-boundary account was then corrected to the measured execution-time guard |
| Track 2 — live evidence | Independently reviewed READY with no blocking finding (Track 2's independent review). C0–C8 and C10–C13, the cross-year case, provenance, and the legacy/line-2b boundary execute through `live_coordinate_run` on v36. **C9 is closed structurally, not live**: no committed payment, credit, or transfer citizen exists to instantiate, so a static test proves the adopted rule declares no payment, credit, transfer, accrued-interest, or legacy-nominee dependency, and that no reduction arises without a current allocation. Test-only. Three non-blocking findings absorbed: two previously untested refusal sites now discriminate; C0's box-1 `$1,200` does not prove the nominee rule ran; Track 2 was not independently verified before that review record |
| Closeout | This unit. Retrospective, plan closure, next-stage input contract, roadmap item 8, and phase-state selection posture |
