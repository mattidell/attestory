<!-- foreman-context-v1
{
  "version": 1,
  "topic": "ssa1099-benefits-line6",
  "active_plan": "docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md",
  "milestone_state": "track-2",
  "status": "CURATED CANDIDATE. Track 1, Track 2, and the findings-only verification repair are complete; final independent review and CI must bind the exact curated head.",
  "source_ref": "origin/main",
  "source_commit": "9cecf30ea7eca62aefe2462620ea063345e72cae",
  "scope": [
    "admit the bounded 2025 ordinary Form SSA-1099 class with reconciled nonnegative box-5 benefits",
    "compute the standard Social Security Benefits Worksheet and publish Form 1040 lines 6a and 6b",
    "add taxable Social Security to line 9 exactly once while preserving the preferential-income base",
    "resolve package, explanation, exact citations, and production-shaped presentation"
  ],
  "non_goals": [
    "no RRB-1099, SSA-1042S, foreign social-benefit, lump-sum-election, excess-repayment, or Publication 915 exception route",
    "no new IRA, pension, unemployment, Schedule 1, withholding, payment, credit, deduction, filing, transmission, or state support",
    "no manual line-6b conclusion and no line-9 shortcut as a worksheet input"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md",
      "docs/adr/0011-tax-fact-identity-and-source-closure.md",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0028-package-fact-surface-and-composition-obligation.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/content/tax/2025/core_calculations.bundle.v2.json",
      "packages/content/tax/2025/rule.form1040-line9.v6.json",
      "packages/content/tax/2025/rule.form1040-line11.json",
      "packages/content/tax/2025/rule.form1040-line15.json",
      "packages/content/tax/2025/rule.form1040-line16.v5.json",
      "packages/content/tax/2025/rule.form1040-line2b.v4.json",
      "packages/content/tax/2025/package.core-calculations.v26.json",
      "packages/content/tax/2025/published-packages.v21.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md#Required evidence",
      "docs/adr/0011-tax-fact-identity-and-source-closure.md",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
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
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md"
    ]
  }
}
-->
# Milestone: 2025 SSA-1099 Benefits through the Social Security Benefits Worksheet and Form 1040 Lines 6a/6b

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by owner direction on 2026-08-04.

## Objective

Make a bounded 2025 federal return class computable end to end when one or more
ordinary Form SSA-1099 statements report benefits for the taxpayer or, on a
joint return, the taxpayer's spouse. The engine will reconcile box 3, box 4,
and box 5; publish total benefits on Form 1040 line 6a; compute taxable
benefits with the official 2025 Social Security Benefits Worksheet; publish
line 6b; add taxable benefits exactly once to line 9, AGI, taxable income, and
the existing regular-tax path; and preserve the existing preferential-income
base used by line 16.

The milestone is synthetic-complete only for the explicitly closed class
below. It does not claim general Social Security, railroad-retirement,
Publication 915, or full Form 1040 support.

## Base, branch, and concurrency record

- Source ref: `origin/main` at
  `9cecf30ea7eca62aefe2462620ea063345e72cae` after the rebase. The base now
  includes the merged IRA line-4b milestone and its successor package graph;
  that upstream route is an integration prerequisite, not SSA scope.
- Milestone branch: `milestone/form1040-ssa1099-line6-local` (curated
  candidate; the original milestone branch remains the planning lineage).
- Dedicated clean worktree separate from every active milestone worktree.
- The prior Form 1099-DIV box-12 milestone is closed on the base. Draft PR
  #161, `milestone/schedule-d-form8949-covered-wash-sale`, is active in a
  separate dirty worktree and is untouched by this planning branch.
- The merged IRA line-4b route is present on this base. Its line 4b result is a
  direct worksheet dependency and must be consumed exactly once.
- The merged Form 1099-G unemployment route is present on this base. Its
  line-8 result is therefore a prescribed worksheet component for Track 2;
  absence authority remains required only for unsupported Schedule 1 income or
  adjustment families.
- Current base inventory observes package core `v26` and published registry
  `v21`. These are observations, not reservations. No future schema, rule,
  package, registry, release, adoption, or presentation version is allocated
  by this plan.

If the base changes, fetch again and re-identify the ratified line. Before
rebase and before final PR preparation, run the established ephemeral
three-way semantic-ledger diagnostic over package/member, producer selection,
admitted-schema, input-binding, and composition-obligation deltas, with a
negative control. Lost upstream members, changed selections, lost schema
admissions, or lost composition obligations are blocking unless explicitly
intended and justified. The ledger is temporary and ignored; remove it before
closeout.

Rebase disposition at `9cecf30`: the latest package graph preserved all 185
prior members, all 33 prior entrypoints, all 26 prior admitted schemas, all 7
input bindings, and both composition obligations. It added upstream members
and admissions only. The ten changed producer selections are the intended
successors from the merged capital, tax-exempt-interest, and IRA milestones;
none is an SSA selection and none was silently dropped. The negative-control
removal detected a loss as required. No generated package or registry file was
changed by this planning rebase.

## Proposed supported return class

The initial class, to be refined and ratified by Track 0, is:

- tax year 2025, US federal, one or more ordinary Form SSA-1099 statements;
- each statement is authoritative for the taxpayer or spouse subject named
  by the return, uses an authoritative logical statement identity, and is
  current after correction/supersession;
- box 3 benefits paid, box 4 benefits repaid, and box 5 net benefits are
  present; box 5 equals box 3 minus box 4, all are nonnegative, and no
  statement has repayments greater than benefits;
- the aggregate box-5 amount is the only Social Security benefits amount
  entering line 6a and the worksheet;
- no RRB-1099, SSA-1042S, foreign social-benefit, or other equivalent-benefit
  statement is present;
- no prior-year lump-sum-election method is required or elected;
- no federal withholding is present on SSA-1099 box 6 unless Track 0 proves
  the existing withholding/payment path is already complete and the owner
  deliberately adopts it (the default class requires box 6 absent/zero);
- no excess-repayment deduction, credit, or claim-of-right treatment is used;
- the standard Form 1040 worksheet is eligible: no coordinated traditional-IRA
  deduction case, no Form 2555/4563/8815 case, no excluded adoption/Puerto
  Rico/American Samoa income, and no Schedule 1 line-24z write-in adjustment;
- every ordinary-income component named by worksheet line 3 and every
  Schedule 1 adjustment component named by worksheet line 6 is either
  computable and closed or explicitly declared absent at component level;
- filing status is authoritative. All five current filing-status values are
  candidates for support, with an explicit lived-apart-all-year authority for
  married filing separately. No marital living arrangement is inferred from
  filing status;
- tax-exempt interest on line 2a is included in worksheet arithmetic but never
  added to line 9; qualified dividends, capital gains, supported interest,
  wages, IRA distributions, pension/annuity amounts, and Schedule 1 income
  are each included once or explicitly absent; and
- unsupported Social Security and equivalent-benefit classes remain blocked
  with a visible, non-authoritative disposition.

## Track 0 — paper-first scope contract

Track 0 is foreman-owned. It must settle the boundary before implementation;
the owner-launch charters below are prepared but do not authorize a wider
class. A rival prototype is warranted only if a genuine architecture choice
survives the paper analysis.

### Source authority and SSA-1099 box inventory

Track 0 must classify the whole ordinary SSA-1099 statement surface:

| Statement surface | Initial classification | Contract question |
| --- | --- | --- |
| Box 1, name | Required authority | Bind the authoritative beneficiary to taxpayer or spouse subject without committing personal names. |
| Box 2, beneficiary SSN | Required authority in production; synthetic role mapping in fixtures | Prove recipient identity without allowing evidence/file ids to become fact identity. |
| Box 3, benefits paid in 2025 | Required authority | Reconcile with box 5 and guard prior-year lump sums, nontaxable portions, and benefits for another person when the description carries them. |
| Box 4, benefits repaid to SSA in 2025 | Required authority | Reconcile to box 5; decide whether any statement-level excess blocks before aggregation. |
| Box 5, net benefits | Required authority and line-6a source | Publish only when box 3 minus box 4 matches exactly and the accepted nonnegative boundary holds. |
| Box 6, voluntary federal income tax withheld | Guarded exclusion by default | Require absent/zero unless an already complete withholding path is deliberately adopted. |
| Box 8, claim number | Required identity authority in production; deferred (not implemented) in this synthetic-only milestone | Use it as a logical statement discriminator only through the accepted statement-instance contract; never use evidence identity. |
| Box 3/4 descriptions and adjustment rows | Required guards where they alter eligibility; otherwise irrelevant to the bounded calculation | Explicitly disposition Medicare premiums, workers' compensation, disability, paid-to-another-family-member, attorney fees, work/overpayment adjustments, offsets, pre-1983 payments, lump-sum death payments, refunds, and other nontaxable payments. Box 5 remains the authoritative net amount, but unsupported descriptions cannot be silently ignored when they change who owns or how much of the benefit is taxable. |
| Missing/reserved box numbers, layout, scan, or upload metadata | Irrelevant to this computation | Never enter fact identity or authority. |

**Deferred obligation — box 8 claim-based statement identity (owner ruling,
2026-08-09).** This milestone is synthetic-only: no furnished statement exists
to derive a claim number from, so implementing box-8-keyed identity now would
itself be synthetic. Deterministic claim-based statement-identity minting is
**not implemented**. Statement sameness is delegated to whatever mints entity
ids (test fixtures mint `f"demo.ssa.statement.{index}"` by list position; no
artifact in this milestone specifies a production minting policy). This is
carried forward, not silently dropped: it is a named, findable obligation for
the first real-entry milestone that furnishes actual SSA-1099 statements. Note
that sameness is nonetheless *enforced* today — the kernel's duplicate guard
(`packages/kernel/facts.py:109-110`, `entity already exists`) rejects a repeat
entity id unconditionally over all ids ever introduced, not only ids currently
standing. What remains open is the *derivation* of a production entity id from
a claim number, not the enforcement of its uniqueness once minted.

The minimum proposed source authority is tax year, logical statement/claim
identity, beneficiary identity, correction state, boxes 3/4/5, box-6
withholding state, and the guarded description conditions. Track 0 must prove
that this is sufficient and no broader box surface is needed.

### Standard-worksheet eligibility and exception inventory

The following exceptions must each become a supported input/rule, a precise
guarded exclusion, or a declaration whose authority closes the named state:

| Official exception or condition | Initial disposition |
| --- | --- |
| Traditional IRA contribution while taxpayer or spouse is covered by a workplace/self-employment retirement plan | Explicit absence authority; no Publication 590-A coordinated IRA deduction path in this milestone. |
| Total repayments greater than total gross benefits, including any negative box 5 | Ordinary worksheet blocked; no excess-repayment deduction, credit, or claim-of-right route. Track 0 settles per-statement and aggregate validation, starting from the stricter per-statement rule. |
| Form 2555, Form 4563, or Form 8815 | Explicit absence authority; no Publication 915 alternate worksheet or Schedule B line-2 substitution. |
| Employer-provided adoption benefits excluded from income | Explicit absence authority. |
| Foreign earned income or foreign housing exclusion | Explicit absence authority. |
| Income of bona fide residents of American Samoa or Puerto Rico | Explicit absence authority. |
| Schedule 1 line 24z write-in adjustment that must be figured before the worksheet | Explicit absence authority; no unmodeled write-in is accepted. |
| Schedule 1 lines 11–20, 23, and 25 named by worksheet line 6 | Component-level closed authority for each supported adjustment or precise declared absence; no blanket line-9 subtraction shortcut. |
| Married filing separately and lived apart all year | Supported only with authoritative lived-apart-all-year fact; base $25,000 and line 6d checked. Missing authority blocks. |
| Married filing separately and lived with spouse at any time | Supported only with authoritative lived-with fact; use the 85% branch and leave line 6d not checked through an honest categorical disposition. Missing authority blocks. |
| Lump-sum benefits for an earlier year / lump-sum election | Explicit guarded exclusion; line 6c is not an accepted election input. |
| RRB-1099 tier-1/SSEB benefits | Explicit guarded exclusion; no RRB source family. |
| SSA-1042S, nonresident/foreign social-benefit cases, or foreign social-security systems | Explicit guarded exclusion. |
| Benefits received on behalf of another taxpayer, minor child, or disabled adult | Explicit guarded exclusion unless the authoritative recipient is the taxpayer or joint-return spouse. |
| Negative-benefit repayment, excess-repayment deduction, credit, or §1341 treatment | Explicit guarded exclusion. |
| Medicare-premium deductions | Not a line-6a/6b input; no Schedule A deduction support. Any description state that requires that path is blocked or declared irrelevant only after Track 0 proves box 5 remains sufficient. |

Track 0 must record positive and negative paper examples for every row without
turning every bullet into a separate fact if a consolidated declaration remains
precise, auditable, and value-checked.

### Filing status, line indicators, and publication shape

The current filing-status citizen already has the five values `single`,
`married_filing_jointly`, `married_filing_separately`, `head_of_household`, and
`qualifying_surviving_spouse`. The proposed first slice supports all five only
if Track 0 proves the MFS living-arrangement authority and thresholds. A
missing MFS living-arrangement fact blocks; filing status alone never selects
the $25,000 or $0 base.

Line 6c is a checkbox for the excluded lump-sum election. The proposed shape
is an auditable categorical indicator: the ordinary supported class has an
explicit non-election/inapplicable disposition; a lump-sum state is blocked,
never silently rendered blank. Line 6d is an auditable categorical indicator:
checked for MFS lived apart all year, explicitly not checked for MFS lived
with the spouse, and inapplicable for other statuses. Track 0 must verify that
the accepted form-field and presentation shapes can express these states
without inventing a filed attachment or a false blank.

The Social Security Benefits Worksheet is a “keep for your records” worksheet,
not a filed Schedule. The proposed citizen shape is an auditable derived-rule
citizen plus a non-filed worksheet artifact in the explanation/presentation
walk. It must never be manufactured as a filed attachment merely for display.
If the existing content model cannot represent this without generic substrate,
stop for owner disposition.

## Component dependency and completeness graph

The worksheet graph is component-level and intentionally avoids the final line
9. Every node below must have a current value or a precise absence/closure
authority before the worksheet publishes.

```text
SSA-1099 box 3 + box 4 + box 5 + recipient/correction authority
        └─ closed SSA family subtotal ───────────────┐
                                                     ├─ W1 line 6a
                                                     ├─ W2 = 50% × W1
                                                     └─ W17 = 85% × W1

line 1z component ─┐
line 2b component ─┤
line 3b component ─┤
line 4b component ─┤── W3 ordinary-income base ─┐
line 5b component ─┤                             ├─ W5 = W2 + W3 + W4
line 7a component ─┤  line 2a component ─ W4 ───┘
line 8 component ──┘

Schedule 1 lines 11–20, 23, 25 ─ W6 adjustments
Schedule 1 line 24z absence ───── eligibility guard
W5 − W6 ─ W7; thresholds/filing status/living arrangement ─ W8–W16
W18 = min(W16, W17) ─ taxable benefits ─ line 6b

line 6b + existing line-9 members ─ successor line 9 ─ AGI ─ taxable income ─ line 16
line 2a ───────────────────────────────────────────────╯ (never an input to line 9)
```

The exact pin table must name each prescribed component once. The line-9
successor may consume the derived line-6b publication once, but the worksheet
must never consume line 9, AGI, taxable income, or any successor that already
contains line 6b. The preferential-income base remains the existing qualified
dividend/capital-gain base; taxable Social Security is ordinary income only.

Current-base component inventory:

| Worksheet component | Base state at `origin/main` | Integration rule |
| --- | --- | --- |
| line 1z | No Form 1040 line-1z citizen; W-2 line 1a exists | Track 0 must define a bounded line-1z component from current wages plus explicit absence for unsupported line-1 entries, or stop if that is generic substrate. |
| line 2b | Closed multi-family taxable-interest composition and selected line-2b rule | Consume the final selected line-2b publication exactly once; no Form 8815 alternate path. |
| line 3b | Closed Form 1099-DIV box-1a ordinary-dividend family | Consume ordinary dividends exactly once; qualified dividends remain on the preferential path only. |
| line 4b | Merged fully taxable IRA-family route; selected line-4b successor is present | Consume the final selected line-4b publication exactly once; do not add a second IRA producer. |
| line 5b | Absent on the base | Explicitly declare pension/annuity component absent; no new pension support. |
| line 7a | Closed selected direct/Schedule-D capital-gain path on the base; draft Form 8949 work may add a successor | Rebase after any Schedule D/Form 8949 merge and verify the final selected line-7a producer is consumed once. |
| line 8 | Merged Form 1099-G box-1 unemployment route; selected line-8 successor is present | Consume the selected line-8 publication exactly once; separately close unsupported Schedule 1 income/adjustment families. |
| line 2a | Merged tax-exempt-interest successors, including the selected Form 1099-INT box-8 route | Include in W4 and keep excluded from line 9; consume the final selected line-2a result once. |
| Schedule 1 adjustments | Schedule 1 income routes exist, but no worksheet-named adjustment families are supported | Use precise absence authorities for lines 11–20, 23, 25 and line 24z eligibility; do not treat Schedule 1 income or line 9 as an adjustment shortcut. |

## Ratified decision — statement identity (owner, 2026-08-09)

The SSA-1099 fact-identity key is **logical statement + tax year**. Payer is
not part of the key, and the alternative payer-bearing shape considered on a
comparative branch is rejected.

Rationale, in the owner's terms: the `statement` entity represents one
logical furnished SSA-1099 and is peer to evidence; it must be
deterministically claim/statement-based and never upload- or file-based. SSA
is the single issuer for this admitted ordinary SSA-1099 class, so payer
would be degenerate and would not distinguish any two admissible facts.
Return/workspace scope supplies taxpayer context. Recipient is a correctable
companion fact and eligibility authority, not a statement individuator:
correcting the recipient does not turn the same furnished statement into a
different statement.

This is milestone-specific. It does **not** generalize ADR-0015 (which keys
Form 1099-INT statement identity on payer, tax year, and payer's own
statement reference, because 1099-INT has many issuers and multiple returns
per payer/account must not collide) beyond Form 1099-INT, and this milestone
does not edit ADR-0015.

At the production admission boundary, this decision is already how the
vocabulary is shaped: every SSA-1099 fact type in
`packages/content/tax/2025/ssa1099.bundle.v2.json` declares identity keys
`{entity_kind: tax.us.ssa1099-statement}` plus the `tax-year` literal — no
payer key. The admitted `tax.us.ssa1099-statement` entity is itself the
logical-statement individuator (`packages/kernel/facts.py` renders one fact
id per current entity of that kind, per the fact type's declared identity
keys), so a distinct entity is a distinct statement, a repeat assertion
against the same entity's fact id is a correction (the fact types' `free`
supersession policy makes the last-inserted finding for a fact id current),
and re-introducing an entity id is rejected by the kernel's `entity already
exists` check (`packages/kernel/facts.py:109-110`) — a duplicate-identity
guard grounded in entity individuation rather than a payer/reference
comparison. This guard is stronger than "already-current": it rejects a
repeat id unconditionally over every entity id ever introduced in the
workspace, current or superseded, not only ids presently standing.

### Citation coverage record

`rule.ssa1099-benefits-subtotal.json` cites the four SSA-1099 amount boxes it
consumes (box 3, box 4, box 5, box 6). Under ADR-0029 decision 3, a rule
artifact's citation pins are an **optional**, explanatory array that must not
alter `when`, `value`, `publishes`, blocking, or form-field dispositions —
never a mandatory per-fact requirement. Statement-kind and lump-sum-election
are eligibility/guard witnesses, not consumed amounts, and — consistent with
every other guard fact in this milestone (recipient, the MFS living-arrangement
fact, and all twenty-three `SCOPE_TOKENS` absence declarations) — carry no
citation pin of their own. Adding citations for only these two guard facts
while leaving the others uncited would be an inconsistent, speculative
addition, which this milestone's evidence bar forbids. No new citation
artifact is added; existing box 3/4/5/6 coverage is unchanged and sufficient
under the accepted contract.

## Source-family closure and lifecycle contract

The source family must claim exactly the admitted ordinary SSA-1099 universe,
not “all Social Security” or “all equivalent benefits.” Its mapping, subtotal,
closure, horizon, explanation, and worksheet consumer must pin the same family
declaration. A closed-empty family may publish line 6a zero only with current
closure on the current family horizon and the complete exception/absence
authority. A late member advances the horizon and invalidates a prior
closure-backed empty result and its downstream findings. Present-source
aggregation of current members remains valid without reclosure; a new closure
is required only to publish a new closed-empty zero (and any closure-dependent
downstream result). A same-statement correction preserves logical identity and
supersedes the old value; a distinct statement remains a distinct member.

Joint-return aggregation is over the authoritative taxpayer and spouse
subjects, including a negative/positive interaction only if Track 0 elects to
support it; the starting proposed class rejects negative box 5. A statement
for another person, a duplicate identity, or a stale correction blocks rather
than disappearing. A late present member is aggregated on the current source
path without a new closure; the closed-empty path remains blocked until
reclosure.

## Scope and non-goals

### Scope

- Add the bounded SSA-1099 source facts, identity, correction, duplicate,
  recipient, box reconciliation, family horizon, closure, and exact mapping.
- Add the auditable standard worksheet, line 6a, taxable line 6b, and only the
  accepted line-6c/6d categorical indicators.
- Add an additive line-9 successor and prove AGI, taxable income, regular tax,
  package resolution, exact explanation pins, and production-shaped
  presentation.
- Add focused positive, negative, boundary, lifecycle, closure, cycle, and
  compatibility evidence while preserving all existing fixtures.

### Non-goals

- RRB-1099, railroad retirement, SSA-1042S, foreign systems, nonresident cases,
  lump-sum election, Publication 915 exception worksheets, excess-repayment
  deductions/credits, and claim-of-right treatment.
- Traditional IRA deduction coordination, new IRA support, pension/annuity,
  unemployment, Schedule 1 income or adjustment, Medicare-premium deductions,
  withholding/payment/refund paths not already complete, or any new credit.
- Benefits belonging to another taxpayer, state taxation, filing/transmission,
  real-data operation, or accepting a contributed line-6b conclusion.
- Editing any published schema, historical content, package, release,
  adoption, checksum, accepted ADR, or unrelated regression fixture.

## Proposed contracts and ADR disposition

Track 0 should prefer content-level reuse of ADR-0011, ADR-0015, ADR-0016,
ADR-0017, ADR-0020, ADR-0027, ADR-0028, ADR-0029, ADR-0033, and ADR-0046.
No new ADR is planned. If paper analysis finds that SSA-1099 identity,
component-level absence authority, or non-filed worksheet representation is a
genuine new product contract, stop before implementation and return the exact
choice to the owner. Do not interpret governance text or introduce generic
substrate from a builder track.

## Required evidence

All committed values use synthetic labels and ids only.

- below-threshold zero taxable benefits;
- 50% inclusion region, 50-to-85% transition, 85% inclusion region, and the
  85% statutory cap;
- tax-exempt interest changing line 6b while remaining outside line 9;
- qualified dividends through line 3b exactly once, capital gains through line
  7a exactly once, supported interest and wage income exactly once, and line
  4b exactly once after IRA integration;
- every supported filing status, including joint taxpayer/spouse aggregation
  and authoritative MFS lived-apart/lived-with branches;
- multiple statements, corrected replacement, duplicate rejection, late member,
  closed-empty family, zero benefits, and repayment equal to benefits;
- repayment exceeding benefits, lump-sum election, RRB-1099, another-taxpayer
  benefit, missing living-arrangement authority, missing component completeness,
  excluded foreign/adoption/Puerto Rico/Samoa/IRA/8815 states, and write-in
  adjustment cases all block honestly;
- exact absence of a line-9/line-6b cycle and exact worksheet pin table;
- exact line 6a, line 6b, line 9, AGI, taxable-income, and line 16
  recomputation, with Social Security excluded from preferential income;
- exact citations, walkable explanation, honest categorical line indicators,
  production-shaped positive and blocked presentation;
- package, release, adoption, and schema-registry integrity, including
  additive-only manifest changes; and
- every existing regression fixture preserved.

## Tracks, owner-launch charters, and commit sequence

1. `Track 0: paper-first scope contract` — foreman-owned paper evidence,
   decision inventory, dependency graph, exact pin table, exception
   disposition, filing-status boundary, worksheet citizen/publication shape,
   integration order, and ADR disposition. No prototype unless a genuine
   architecture choice remains.
2. `Track 1: SSA-1099 source family and closure` — one atomic implementation
   commit after Track 0 ratification.
3. `Track 2: worksheet, line 6a/6b, downstream and presentation` — one atomic
   implementation commit after Track 1 and upstream income integration.
4. Independent final review, one findings-only repair cycle if needed, and
   curated closeout are folded into the owning track and milestone PR; no
   track, review, repair, or cleanup gets its own PR.

The planning commit contained this plan, the phase/roadmap/frontier selection,
and the owner-launch charters. Those working charters and interim review
records are removed during final curation. The milestone has one branch and
one draft-to-final PR.

## Stop conditions

Stop and return to the owner when any of these occurs:

- Track 0 cannot close an exception, statement-box, recipient, filing-status,
  or component-completeness boundary precisely;
- a new identity, closure, rule-language, worksheet, package, explanation, or
  presentation contract is genuinely required rather than content reuse;
- any implementation would need to read line 9, AGI, taxable income, or a
  derived result containing line 6b as a worksheet input;
- a concurrent IRA, Schedule D/Form 8949, unemployment, or other income merge
  changes the base and the semantic-ledger diagnostic finds lost members,
  altered selections, lost schema admissions, or lost composition obligations;
- a published schema or manifest would be edited, a package/registry version
  collides, a non-additive successor is proposed, or a production resolver
  graph cannot close;
- the worksheet cannot represent MFS living arrangement or line 6c/6d states
  honestly without false blanks or invented filed content; or
- any requested scope expands to RRB, Publication 915 exceptions, pensions,
  unemployment, Schedule 1 support, withholding/payment, or real data.

## Verification and closeout

While iterating, run only touched unittest modules. Before final PR curation,
rebase onto the latest ratified line, rebuild generated packages and registries,
run the ephemeral semantic-ledger comparison, confirm additive-only schema
manifest changes, inspect the exact once-only worksheet pins, remove transient
charters/ledgers/spikes, and leave no ignored diagnostic residue. The final
suite gate is the green CI `verify` check on the exact PR head.
