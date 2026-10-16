<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "personal-item-sale-circumstances",
  "status": "Opening plan. Investigate one personal-item sale reported on Form 1099-K before selecting its representation or production tracks. No tax treatment or implementation is yet selected.",
  "scope": [
    "connect a reported payment to one identifiable sale of a personally used item",
    "obtain ordinary circumstances and amounts needed to distinguish receipts, gain and a nondeductible personal loss",
    "select and build a bounded recording, adopted calculation, return-reporting and saved-explanation path"
  ],
  "non_goals": [
    "no complete Form 1099-K, business, hobby or capital-asset product",
    "no automatic allocation of an aggregate report among multiple sales",
    "no new general assumption framework or engine mechanism selected in advance"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
      "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md#Actions the team will take"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md#Decisions that need evidence",
      "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md#Cases that will test the account"
    ],
    "new_milestone": [
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md"
    ]
  }
}
-->

# Personal-Item Sales: What Was Sold and What the Payment Means

Milestone key: personal-item-sale-circumstances.
Branch: milestone/personal-item-sale-circumstances-translation.
Phase: Tax Circumstance Breadth. Opening plan, 2026-10-16.
Base: origin/main, mortgage milestone merge `16977f10437f8e6c2bae196a38c50f521fc943e0`
(PR #209).

## What we are trying to accomplish

A person sells something they bought and used personally, receives a Form
1099-K, and wants to know what that payment means for their taxes. The form
reports money received; it does not tell the application what was sold, what
it cost, or whether the person made a profit.

Help the person describe the sale in ordinary terms. Connect that account to
the reported payment, determine the supported tax treatment, carry it to the
appropriate return reporting, and save an explanation the person can inspect
and correct. Do not ask the person to supply a tax conclusion such as taxable
gain or deductible loss just to make the software work.

The starting case is one statement associated with one identifiable sale of
an ordinary personally used item the filer purchased. Examine both a sale
above its cost and one below its cost. Those are investigation examples, not
a claim that subtraction alone establishes every required tax fact. Dates,
ownership and use, the meaning of cost, selling expenses and the connection
between gross payments and sale proceeds need a deliberate place.

This is the phase's contrasting application beyond borrowing deductions. The
lesson sought is whether the application can preserve a distinction between
reported receipts, a person's account of a sale, and its tax consequence,
using the established translation, correction and explanation approach.

## Starting position and uncertainty

The merged mortgage capability records a finite ordinary account, distinguishes
uncertainty from unsupported circumstances, calculates a bounded result and
reloads a saved explanation. Its broader filing-unit answers have distinct
identities rather than new labels on older personal answers. These are reuse
candidates, not proof that the sale should have the same model or defaults.

An initial filename/text inventory found no Form 1099-K route in current tax
content, tax modules or tests. Existing Form 8949 and Schedule D content is
present, as is Schedule 1 composition. This establishes neither that those
paths admit a personal-item sale nor that a Form 1099-K reporting entry exists.
P0 must trace the adopted graph, not infer reuse from a filename or form title.

The IRS's [Form 1099-K guidance](https://www.irs.gov/businesses/what-to-do-with-form-1099-k)
distinguishes personal-sale gains and losses, says personal losses are not
deductible, and identifies different reporting possibilities. It also warns
that gross reported payments do not include all adjustments. This is selection
orientation, not the milestone's settled 2025 legal or reporting contract.
Establish the exact 2025 instructions and applicable authority during P0.

## Actions the team will take

1. **Describe the sale and examine the existing return path (P0).** Write a
   short plain-language account of what the person knows, what the report says,
   what the tax rules need, and what the application can establish. Verify the
   2025 gain/loss and reporting treatment from primary sources. Trace the
   adopted package through its capital-gain and other-income consumers,
   attachments and saved presentation. Use a bounded execution only where it
   answers a specific uncertainty about that path. Report supplied fixture
   facts separately from defaults and derived results.
2. **Review that account before choosing a design.** Obtain independent review
   of the first concrete P0 account and its reuse/cost conclusions. It should
   test whether the proposed ordinary answers establish the stated tax facts,
   whether gross payments were silently treated as proceeds, and whether the
   selected return route actually accepts this kind of sale. Resolve material
   findings before making the plan more concrete.
3. **Develop the connected design incrementally.** Establish the identities
   and relationships among statement, sale, item and filer; identify which need
   separate representation rather than assume they all do. Draft finite
   ordinary questions, normalized meanings, tax conclusions, assumptions and
   explanations. Work through the cases below, including correction and
   withdrawal, before selecting storage fields or rule mechanisms. Review each
   consequential section while it can still change the next section.
4. **Test the decisions that remain uncertain.** Use paper examples first.
   Where accepted contracts suffice, plan direct production. Where one
   mechanism is uncertain, use the smallest discriminating spike. Only a real,
   consequential choice between representations justifies rival prototypes;
   apply the project's prototype gates before chartering them. An integration
   experiment is evidence, not automatically the production implementation.
5. **Close Track 0 and specify the production units.** Select the bounded tax
   and reporting contract, demonstrate its load-bearing assumptions, and obtain
   independent connected-design review. Complete the Track 0 gate before any
   production charter. Use an ADR only for a new durable product contract;
   do not invent one just to restate an existing pattern.
6. **Build, review and demonstrate the selected path.** The anticipated work
   is recording/correction, adopted tax and reporting content, and saved
   explanation. Their exact track boundaries follow the design, not this list.
   Demonstrate them together through the real recorder, durable log, adopted
   package, coordinator and reloaded result. Then curate, obtain independent
   final review and green candidate CI, and assess the phase endpoint.

The immediate authorized next step is P0 planning and its scoped investigation,
not a production build. After P0, present the actual integration cost and any
necessary scope choice before expanding the milestone. If it would require a
general business/accounting system or broad capital-asset redesign, bring back
a smaller proposal; do not absorb that work silently or call a planning-only
result delivered tax breadth.

## Decisions that need evidence

- **What ordinary information establishes the treatment?** Distinguish buying
  an item, using it personally, selling it, receiving payment and connecting
  that payment to the report. Identify questions that materially change the
  result or its supported boundary. Do not build a free-text circumstance
  catalog or ask the person whether a tax-law category applies.
- **What amount belongs to the sale?** Determine when a reported gross amount
  can support a sale amount and what confirmation or records are needed.
  One selected sale is not evidence that a statement covers only that sale.
  Explore the simple no-adjustment case first; do not silently treat unknown
  fees, returns, multiple sales or missing cost as zero.
- **Where does each outcome go?** Establish the actual reporting and return
  consumers for gain, a nondeductible personal loss and unresolved treatment.
  Do not turn a personal loss into a deductible capital loss, insert an
  ordinary-income adjustment as a substitute for the required reporting, or
  drop the source report because it produces no taxable income.
- **What can the application assume?** State any chosen default, the subject
  and circumstances it concerns, and what contrary information or withdrawal
  does to it. A recorded answer, a reasonable assumption and a condition left
  with the person are different. No general default framework is preselected.
- **What survives a correction?** Establish what changing cost, use, the sale
  connection or the report amount invalidates, and what remains supported.
  Do not retarget an affirmed relationship to a different sale or reinterpret
  an earlier answer as a broader proposition without a design for doing so.

Keep a short account of consequential decisions: what was chosen, why it
matters to the product, what evidence supports it and what it displaces.
Separate product choices from implementation defects and ordinary refinements.
Maintain the opening goal as the plan develops; if it changes, say why rather
than silently describing a smaller result as the original goal.

## Cases that will test the account

These are synthetic cases to refine after the 2025 authority and consumer map
are checked, not precomputed tax verdicts or a demand to automate every case.

- One purchased, personally used item sold above its supported cost; another
  example sold below it. Keep reported receipts, sale result and tax treatment
  separately visible, including why a personal loss is not a deduction.
- Cost equal to the sale amount, contrasted with cost unknown. A genuine zero
  must not look like an unresolved calculation.
- Acquisition and sale dates that expose the relevant reporting distinction;
  identify any unsupported date treatment rather than ask for a tax label.
- A report with fees/refunds or more than one sale. These may remain outside
  production scope, but must not be accepted as the one-sale example merely
  because a gross total is present.
- A personally used item contrasted with something acquired for resale, or an
  acquisition other than purchase. Recognize the bounded route's limit without
  inventing unfavorable tax treatment for the excluded case.
- Correct the supported cost across the gain/loss boundary; withdraw a
  material answer; correct the report amount. Trace the exact current support
  and saved reason, keeping the source and history rather than overwriting it.
- Retain an unrelated existing return source while making those changes, and
  test a gain beside a personal loss as an anti-netting counterexample. The
  counterexample need not become multi-sale production support.

## Contracts, production conditions and verification

No new schema, ADR number, vocabulary, package version or generalized engine
operator is allocated by this plan. Inspect the current accepted contracts
and adopted versions before selecting reuse. Keep document evidence, ordinary
answers and canonical tax meaning distinct even if one existing representation
can serve several layers. New propositions must not be smuggled into old
answer identities by changing their labels.

Track 0 adversarial closure: **PENDING**. Before production, instantiate the
gate in PROJECT_PLANNING.md for the selected path, including actual identities,
answer/default lifecycles, producers and consumers, authority, failure behavior,
neighboring integration and remaining exclusions. A hand-built environment or
favorable finding is not proof of a live input path.

Production exit requires the supported ordinary account to be recordable and
correctable, the selected gain/loss outcomes to reach their proper return
reporting exactly once, and the saved explanation to retain the report,
material answers, actual assumptions, computation and unresolved reasons.
An explicit partial result remains possible by owner disposition, with useful
findings and reopening conditions preserved; it is not the phase's delivered
contrasting capability.

Builder charters will specify focused positive, boundary, lifecycle and
compatibility tests, exact artifact checks and applicable typing checks.
Record the fixture's actual inputs and defaults, not just its descriptive
name. Independent review is required for P0, connected-design closure and the
curated publication candidate. Ordinary production units use Foreman review
unless the refined plan names a further independent question. CI is the full
regression gate; do not repeatedly rerun unchanged deterministic results.

Only synthetic demo evidence enters the repository. Follow AGENTS.md's data,
fixture and schema-publication rules. No personal documents or private outputs
are needed. Browser observation is not required to select the initial design;
any later visual claim requires an actual observation, separate from saved
JSON evidence. No new general user-interface journey is a prerequisite.

## Phase assessment after delivery

Compare this result with the student-loan and mortgage paths: what transferred,
what changed because the tax meaning differs, what assumptions were needed,
and where further breadth still needs design. If the phase's provisional
endpoint is met, recommend concluding it rather than automatically adding a
third vertical or general framework. The next phase remains unselected.
