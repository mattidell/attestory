<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "personal-item-sale-circumstances",
  "status": "Closed. One Form 1099-K for one personally used item bought and sold at a loss enters its Box 1a amount at the top of 2025 Schedule 1, from an ordinary account the person records and corrects, with a saved explanation of the report, answers, assumptions, published computation and named reasons. Gain, break-even, a second statement and other outcomes are named and enter nothing.",
  "retrospective": "docs/milestone-retrospectives/2026-10-17-personal-item-sale-circumstances.md",
  "scope": [
    "connect one Form 1099-K to one identifiable sale of an item the filer bought and used personally",
    "obtain the ordinary account and amounts that establish a nondeductible personal loss, and name every other outcome",
    "enter a supported loss's Form 1099-K amount at the top of 2025 Schedule 1, with a recordable, correctable account and a saved explanation"
  ],
  "non_goals": [
    "no gain or break-even reporting on Form 8949 or Schedule D in this milestone",
    "no more than one Form 1099-K per return; no allocation of an aggregate report among multiple sales",
    "no complete Form 1099-K, business, hobby or capital-asset product, and no new general assumption framework or engine mechanism"
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
      "docs/milestone-retrospectives/2026-10-17-personal-item-sale-circumstances.md",
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
reports money received. It does not tell the application what was sold,
what it cost, or whether the person made a profit.

**Selected route (owner, 2026-10-16): a personal item sold at a loss.**
- The person has one Form 1099-K, covering one sale of an item they bought
  and used personally.
- They describe the sale in ordinary terms: how they got the item and used
  it, the agreed price, shipping, fees, refunds and what they paid.
- When that account establishes a loss, the application enters the
  statement's Box 1a amount in the 2025 Schedule 1 space for Form 1099-K
  personal items sold at a loss. Income and tax do not change.
- Every other outcome is named and enters nothing. That covers a gain,
  break-even, "I can't tell", an excluded use or acquisition, an
  unexplained Box 1a difference, a second statement, and an unanswered or
  withdrawn answer.
- The person never supplies a tax conclusion.
- A saved explanation keeps the report, their answers and the comparison
  that established the result, or the reason none was established. The
  person can inspect and correct it.

**Why the scope narrowed.** The opening plan aimed at both a gain and a
personal loss. P0 traced the 2025 rules and the adopted package:
- A gain must go to Form 8949 boxes C or F and Schedule D lines 3 or 10. None
  of these exist.
- Form 8949 needs real acquisition and sale dates and a description. The
  rule language cannot compare two recorded dates, and attachments carry
  amounts only.
- A gain route also changes existing capital-gain contracts.
- The Schedule 1 entry for a personal loss needs none of that.

The owner chose the loss-only shape as the bounded contrasting capability.
The goal of keeping reported receipts, the person's account and the tax
consequence distinct is unchanged; the gain route remains separate future
work. See "P0 result and the scope choice" below.

This is the phase's contrasting application beyond borrowing deductions. It
tests whether the application can keep reported receipts, a person's account
of a sale and its tax consequence distinct, using the established
translation, correction and explanation approach.

**Result.** The loss-only route is delivered and closed. See "Execution
record" and "Outcome" at the end of this plan.

### Original opening account (2026-10-16, before P0)

The opening plan asked the application to help the person describe the
sale, connect it to the reported payment, and determine the supported tax
treatment. It also asked the application to carry that treatment to the
appropriate return reporting and save an explanation the person could
inspect and correct. The starting case was one statement and one
identifiable sale of an ordinary purchased, personally used item, examined
both above and below its cost. Dates, ownership and use, the meaning of
cost, selling expenses and the connection between gross payments and sale
proceeds each needed a deliberate place.

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

   P0 runs in two reviewed steps, because the person's questions depend on
   which facts the rules need and which return lines can carry the result:

   - **P0a — what the rules need and where a result can go.** Establish the
     exact 2025 treatment and reporting of a gain and a personal loss on one
     purchased, personally used item, what Form 1099-K reports and how that
     relates to the sale amount, and which adopted return consumers exist for
     each outcome. A fresh reviewer checks those claims before P0b relies on
     them.
   - **P0b — what the person knows and what it would cost.** On the reviewed
     P0a basis, write the ordinary account of the sale, work the gain and
     personal-loss examples on paper, separate supplied facts from defaults
     and derived results, and estimate the integration cost and any scope
     choice. This is the account the independent P0 review in action 2 tests.

   P0a result: the report was reviewed
   and accepted with five evidence corrections. The adopted package has no
   route for this sale. A gain needs Form 8949 boxes C or F and Schedule D
   lines 3 or 10, none of which exist. A personal loss reported on Form 1099-K
   has two 2025 choices: the amount in the entry space at the top of Schedule 1,
   or Form 8949 with code L. Neither exists in the package today.
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

## P0 result and the scope choice

P0 is complete. The [P0b account](personal-item-sale-circumstances-evidence/p0b-ordinary-account.md)
was independently reviewed
and accepted with corrections. The paper arithmetic, the exclusions and the
anti-netting case hold. The corrections below are part of the choice, not
afterthoughts:

- **Box 1a reconciliation.** Box 1a is the unreduced gross charge. Refunds the
  seller gave back reduce the amount realized, not Box 1a. Fees and
  seller-paid shipping are selling expenses. A difference the person cannot
  explain stops the route with a named reason.
- **Basis is more than the purchase price.** Improvements, rebates and
  casualty recoveries are asked about, or the route stops. Buyer payment and
  sale date need "I can't tell" paths.
- **A gain on Form 8949 needs real dates and a description.** The rule
  language cannot compare two recorded dates (ADR 0078 excluded it). Attachment
  itemizations carry amounts only. Remembered months must not be turned into
  dates. Supporting a gain therefore means either new capability for dates
  and text on Form 8949, or an explicitly numeric-only Form 8949 output.
- **Any Form 8949 option changes existing capital-gain contracts.** It needs
  a successor to the `no-other-form8949-adjustments` boundary declaration,
  form fields for Schedule D lines 3 and 10, and a proceeds-based attachment
  trigger so a zero result still attaches.

**Inherited defect found during review.** The adopted preferential-rate base
(`rule.selected-preferential-base@v4`) publishes `max(Schedule D line 16, 0)`.
The 2025 Qualified Dividends and Capital Gain Tax Worksheet, line 3, says
"Enter the smaller of line 15 or line 16 of Schedule D." A return with a
covered short-term Form 1099-B gain therefore has that gain taxed at
preferential rates today. P0a's code reading misreported this rule as the
smaller of the two lines. The defect is independent of this milestone; any
gain route depends on its repair. It is reported to the owner, not repaired.

The three bounded shapes, with the review's corrections included:

1. **Loss only, through the Schedule 1 entry.** One confirmed personal item
   sold at a loss reports its Form 1099-K amount at the top of Schedule 1.
   No dates are needed. Form 8949, Schedule D, their boundary declarations and
   the preferential base are untouched. Gains and break-even sales are named
   as unsupported.
2. **Gain and loss through Form 8949 with code L.** Needs the Form 8949
   date and description capability or a numeric-only decision, the boundary
   successor, Schedule D lines 3 and 10, successor capital-gain rules, the
   preferential-base repair, and code L adjustment content.
3. **Gain through Form 8949, loss through the Schedule 1 entry.** Everything
   in option 2 except code L. The saving is real but smaller than the report
   first stated.

**Owner decision, 2026-10-16: shape 1, loss only.** One confirmed personal
item sold at a loss reports its Form 1099-K amount in the entry space at the
top of Schedule 1. Gains and break-even sales are named as unsupported and do
not produce an amount. This displaces the gain route for this milestone; it
does not change the goal of distinguishing reported receipts, the person's
account and the tax consequence. Form 8949, Schedule D, their boundary
declarations and the preferential base stay untouched. The gain route, its
date capability and the inherited preferential-base defect remain separate
decisions. The connected design (action 3) proceeds on this shape, carrying
the review's corrections that apply to it: Box 1a reconciliation, basis
adjustments, "I can't tell" paths and named stops.

The connected design runs in two reviewed steps. **D1** settles on paper
what establishes a loss, the entry amount, identities, the ordinary
questions, outcomes and their effect on the rest of the return,
corrections and the saved explanation.
An independent review tests it. **D2** then chooses the representation and
produces the Track 0 closure evidence, followed by the independent
connected-design review.

D1 result: reviewed
and accepted with corrections. Three bind D2. Use one comparison that
counts shipping the seller received. Stop on Box 4 withholding. Publish an
explicit zero when a return has no Form 1099-K, because an absent subtotal
would block Schedule 1 for existing unemployment and student-loan returns.
Two more bind the questions. The allowing answer to the use question is
personal use only. A withdrawn answer leaves the question unanswered, with
its own stop. The entry sums Box 1a over supported statements; any other
admitted statement withholds a complete return.

D2 stage 1 ([decisions](personal-item-sale-circumstances-evidence/d2-representation.md))
found the representation within existing capability: no new rule-language
operation or schema. Foreman review found one product consequence that
reverses a D1 promise. The engine treats an empty source set as zero only
when it is asserted complete (`packages/derivation/evaluator.py:361-377`). A
return therefore cannot honestly say "no Form 1099-K" without a completeness
answer. Schedule 1 and the income lines need that answer once the
application admits Form 1099-K. Stage 1 also blocked only the Schedule 1
attachment, not income and tax, contrary to D1. Both go to the owner before
stage 2.

**Owner decision, 2026-10-16: completeness only where Schedule 1 is used.**
The Form 1099-K family joins the Schedule 1 attachment decision, which
already needs a completeness answer for each family that feeds it. A return
that determines Schedule 1 must say whether it received any Form 1099-K;
one that never reaches that decision is asked nothing. Income and tax do not
depend on Form 1099-K. This supersedes D1's choice to block income and tax.
An unsupported, unresolved or excluded statement withholds the Schedule 1
result with its named reason and stays visible as an unresolved condition.
The saved explanation must say plainly that the return's income does not yet
account for that statement. Existing Schedule 1 workspaces and fixtures
need the new completeness answer; D2 lists that migration.

D2 stage 2 built the models through the real coordinator and presentation
model. Two engine limits surfaced:
- The presentation reader projects blocked reasons only for selection rules
  with categorical favorable values
  (`packages/derivation/presentation_projection.py:157-377`). The numeric
  per-statement sum therefore raises an error on every unsupported outcome.
- The marshaller leaves per-statement answers unbound when two statements
  disagree (`packages/derivation/marshal.py:395-421`).

**Foreman decision, 2026-10-16: one Form 1099-K per return.** This follows
the plan's starting case and the mortgage route's one-statement precedent. A
second statement stops with its own named reason. This supersedes the D1
review's summing across statements for this milestone. D2 is repaired to
use the mortgage route's categorical per-statement reason feeding a
selection, which the reader already projects, and to measure neighbor
returns against the current package before and after.

The connected-design review
found the design **not ready**. The representation, the neighbor
measurements, the one-statement stop and the late-statement behavior hold.
Two high findings block Track 0:
- A blank or withdrawn amount is bound to the default zero, so an omitted
  platform fee publishes a supported loss.
- The committed loss paths would pass even if the comparison ignored
  shipping, the label or refunds.

Medium findings cover several gaps:
- the completeness answer is not what the rule reads;
- the lifecycle table is missing the cost-basis gate;
- the closure claim still authorizes a multi-statement sum;
- three sentences mislead: "can't tell" is shown as a fact, the loss is
  called "allowable", and a W-2 page shows a computation failure.

A low finding adds three test modules to the migration list.

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

Track 0 adversarial closure: **settled 2026-10-16**; see the section of that name below. Before production, instantiate the
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

## Track 0 adversarial closure

Evidence is [D2](personal-item-sale-circumstances-evidence/d2-representation.md)
and its probe [`d2_probe.py`](personal-item-sale-circumstances-evidence/d2_probe.py).
The probe runs 33 disposition paths through the real `live_coordinate_run` and
presentation model. Each path asserts its reason token, its published
Schedule 1 entry, and the sentence the page shows. Candidate citizens exist
only in a temporary registry. The connected-design review
found the first build not ready. Its re-review found the repair ready, with
two documentary corrections, which are applied.

- Authority-lifecycle table: PASS. D2 artifact 1 has a row for every fact the
  reason rule reads, including the cost-basis gate and each amount, and names
  what invalidates each one. Retraction returns an answer to "not asked",
  which stops the route. Probe paths 26 and 27 show an omitted fee and a
  withdrawn price each stopping with no entry.
- Empty/nonempty authority matrix: PASS. Closed empty with the closure answer
  publishes a zero entry (path 1). Closed empty without it blocks the entry and
  the Schedule 1 attachment, while income stays unchanged (path 3). Nonempty and
  eligible publishes Box 1a (paths 5 and 30–32). Nonempty and ineligible stops
  with its own reason (paths 10–22, 28, 29 and 33). Two statements stop as out
  of scope (path 9).
- Late-member lifecycle: PASS. A statement added after a "no Form 1099-K"
  closure moves the family horizon. The earlier closure stops counting, and the
  entry stays unpublished until the person answers again (path 24,
  `SOURCE_SET_UNCLOSED`).
- Neighboring capability dependency diff: PASS. This was measured against the
  unmodified release:
  - W-2-only, unemployment and student-loan returns keep their income lines.
  - A W-2-only return's Schedule 1 result stays as it is today (blocked).
  - Unemployment and student-loan returns still attach Schedule 1 when they
    carry the new completeness answer, and block without it, as the owner
    decided.
  - Income and tax gain no Form 1099-K input.
- Reused-claim semantic/lifecycle equivalence: PASS. The Form 1040 line 8,
  line 9 and line 10 rules and `no-form8949-sources` are the same citizens.
  The Schedule 1 attachment successor is a measured behavior change, not a
  reused claim. The family closure claim authorizes one statement's Box 1a or
  a closed-empty zero, never a multi-payer sum. The zero default applies only
  to an absent Box 4.
- Integration surface: PASS. The design adds two form fields (the Schedule 1
  top entry and the Form 1099-K unresolved condition) and the Schedule 1
  attachment successor. Each disposition path is built and projected:
  published, closed-empty zero, each named stop, and out of scope. Five
  boundary cases decide the sign of the comparison (paths 29–33).
- Known limitations affecting correctness: none that change a published
  amount. Two need the owner to know about them:
  - **Existing Schedule 1 workspaces block until answered.** Existing
    unemployment and student-loan workspaces and fixtures block Schedule 1
    until they carry the completeness answer. D2 artifact 5 lists the
    migration.
  - **A W-2-only page gains a wordless blocked row.** It reads "Form 1099-K
    loss entry cannot be computed." The engine marks a row inapplicable only
    when its guard is false, and it cannot be false without closure, so the
    row blocks. That return's Schedule 1 result was already blocked.

Multiple Form 1099-K statements and per-statement circumstance binding are
outside this milestone. The inherited preferential-rate defect does not touch
this route.

### Proposed production division

1. **Adopted content and migration.** Build:
   - the D2 citizens;
   - package `v46`, registry and release `v44`;
   - the completeness answer added to the existing Schedule 1 workspaces,
     fixtures and tests D2 lists;
   - committed tests converting the 33 probe paths through
     `live_coordinate_run`.
2. **Recording, correction and review.** Build:
   - a recorder scoped to the statement, for the Form 1099-K statement, the
     person's answers and the completeness answer;
   - durable correction, and withdrawal back to unanswered;
   - the review snapshot and saved-presentation association, showing the
     person's chosen answers.
3. **Demonstration and explanation.** Run the real recorder, durable log,
   adopted package and coordinator, then reload the saved explanation. Cover a
   supported loss, a stop, and a correction across the loss/gain boundary.
   Add a README section.

Each track gets Foreman review. The curated candidate gets independent final
review and green CI.

Owner approved production 2026-10-16.

**Track 1 result.** The content is adopted as package `v46`, registry
`v44` and release `v44`. Its 12 citizens equal the reviewed probe citizens
exactly (compared by the Foreman). `tests/test_f1099k_personal_item_sale_track1.py`
runs the 33 disposition paths on the adopted release. No migration was
needed: existing workspaces and tests pin the release they adopted, so the
completeness answer arises only when a workspace adopts `v44`. CI is the
full regression gate.

**Track 2 result.** It adds `packages/tax/f1099k_statement_recording.py`
and `packages/tax/f1099k_statement_review.py`. They record a statement or
"no Form 1099-K", answer, correct with history, withdraw back to unanswered,
and review with the person's own labels beside the saved run. 26 tests run
the operations on release `v44` and cover the charter's 13 cases. "No Form
1099-K" is refused once a statement exists; a recorded statement needs no
completeness answer to publish.

**Owner review of Track 2, 2026-10-16.** The owner found two defects that
the Foreman's review missed. Both were introduced in Track 2.
- **The shipping question.** Its help excludes reimbursed shipping, but the
  rule needs the shipping expense the seller actually paid, including
  postage funded by the buyer's shipping money. Example: price $800, buyer
  shipping received $100, label $20, cost $890, Box 1a $900. Recording $20
  gives a supported loss; the $0 the wording invites gives an unsupported
  gain.
- **The saved review.** It calls a result supported only when the entry is
  positive. An admitted $0 statement that publishes `supported-loss` is shown
  as unresolved, with an unjustified income warning.

The lesson: check that each ordinary question supplies what its consumer
actually means, and that each displayed status follows the recorded outcome.
Track 3's first attempt was stopped. It had recorded the missing numerical
comparison as expected behavior instead of reporting it. Its commits are
parked on `park/track3-attempt-1-2026-10-16`.

**Track 2 repair result**.
- **The shipping question** now asks "What did you pay to ship the item,
  including postage and shipping labels?". Its help includes labels bought
  with the buyer's shipping money and excludes labels the platform supplied
  and kept.
- **The discriminating test** works through the review operations. Recording
  $20 gives a supported loss with the $900 entry; recording $0 gives the gain
  stop.
- **Saved results** fall into five distinct states: supported loss,
  supported zero, closed-empty zero, missing output and actually unresolved.
  The income sentence appears only for the last.
- **Known limit, later narrowed.** Under platform pass-through, any other
  shipping the seller paid is asked but not deducted. The closeout repair
  below turns this case into a named stop instead of a gain claim.

**The exit criterion's missing computation.** The Foreman inspected a saved
supported-loss run on release `v44`. It keeps the entry, the reason finding
and the answer findings by reference. It does not keep the amount realized,
selling expenses, net from the sale, adjusted basis or comparison; these exist
only inside the reason rule's evaluation. A gain stop keeps no figures, and
nothing states that no assumption was used. The selected remedy is that the
rules publish the computation and the reader shows it, with no recomputation
in presentation. Its feasibility is checked first.

**Track 3 result.** Stage 1 showed that a reason rule requiring computed
amounts loses its named stops. The accepted Stage 1b single-source design
publishes five per-statement figures:
- amount realized;
- selling expenses;
- net from the sale, computed from the published amount realized and selling
  expenses;
- adjusted basis;
- expected Box 1a.

Each figure is either a number or `not-computed`. The successor reason rule
keeps every named stop and compares only the published figures. It adopts as
package `v47`, registry `v45` and release `v45`.

A display-only reader in `packages/derivation/presentation_projection.py`
copies the recorded figures and states the comparison from the published
reason. The Foreman's review returned four fixes:
- assumptions are listed from the run's declared-default provenance instead
  of a constant;
- figures come only from the reason finding's own pins, and an unpinned one is
  "missing";
- explanations are per statement;
- Box 4 must be supplied explicitly.

The end-to-end demonstration (`tests/test_f1099k_personal_item_sale_demonstration.py`)
runs the real operations and the reloaded saved explanation. It shows the
report, the answers, the assumptions, the figures and the named reasons.
75 Form 1099-K tests and the mortgage reader tests pass. The full CI run on
the candidate is the regression gate.

The fast lane's 22 budget failures are pre-existing. They show the same
timings on `origin/main` and are not caused by this milestone.

**Closeout repair: additional shipping under pass-through.** The owner's
review of Track 3 found that the known limit became a false claim. Under
platform pass-through, a person who also paid $100 of their own shipping saw
selling expenses $0, net proceeds $900 against a cost of $850, and the
unsupported-gain sentence. Counting the $100 would have shown a loss.

The repair names the case rather than modelling it:
- When the arrangement is platform pass-through and the recorded seller-paid
  shipping is greater than zero, the reason is
  `additional-seller-shipping-unsupported`. It is checked after every other
  stop and before the gain, break-even and loss comparison.
- Selling expenses and net proceeds publish `not-computed` for that case.
  Amount realized, adjusted basis and expected Box 1a still show.
- The saved explanation states that the route cannot tell whether the sale
  was a gain or a loss, and that income does not yet account for the
  statement. No Schedule 1 entry is made.
- Pass-through with $0 of seller shipping still runs the comparison.

It adopts as package `v48`, registry `v46` and release `v46`. This needed
successors for the reason fact type (vocabulary bundle `v3`), the reason rule,
the selling-expenses rule, the Schedule 1 top-entry rule and the unresolved
rule. Of the 33 Track 1 paths, only path 33 (pass-through with $100 seller
shipping) changes, from `unsupported-gain` to the new stop. The regression
runs the owner's exact figures through the recorder, the coordinator and the
reloaded review, and shows that `v45` gave the gain sentence.

**Remaining known limit.** Additional seller-paid shipping under platform
pass-through is not deducted. Such a sale stops with its named reason instead
of reaching a result.

## Phase assessment after delivery

Compare this result with the student-loan and mortgage paths: what transferred,
what changed because the tax meaning differs, what assumptions were needed,
and where further breadth still needs design. If the phase's provisional
endpoint is met, recommend concluding it rather than automatically adding a
third vertical or general framework. The next phase remains unselected.

**Assessment (Foreman, 2026-10-17).** The phase should not conclude yet.
- **What transferred.** The ordinary-question and recording pattern, the
  durable correction and withdrawal operations, and the saved-explanation
  reader all transferred from student loans and mortgages.
- **What changed.** The tax meaning is the character and amount of a sale,
  not a borrowing deduction. That required published computation figures so
  the explanation could show the comparison without recomputing it.
- **Assumptions.** The route used none. The explanation states that.
- **The shared gap.** Both new routes stop at a second statement. The engine
  cannot keep two statements' different answers apart, so it treats them as
  unanswered. Ordinary households often have two Form 1099-Ks or two Forms
  1098, and the 2025 Schedule 1 instructions add several Form 1099-K amounts
  into the one entry.

The recommended next milestone is the roadmap's consolidation step. It would
investigate how the student-loan route keeps several statements' answers
apart, use one shared mechanism for the Form 1099-K route, and decide the
mortgage case separately because its debt limit applies across loans. A
bounded engineering-health milestone (test-lane timing, phase-state
validation) and the inherited preferential-rate defect are separate
candidates. The owner selects.

## Execution record

| Unit | Result |
| --- | --- |
| P0 | The 2025 authority and the return path were traced, and the ordinary account was developed and independently reviewed. Gain reporting needs Form 8949 dates and descriptions and changes existing capital-gain contracts. The owner chose the loss-only route and required completeness only when Schedule 1 is used. |
| Track 0 | The connected account (D1) and representation (D2) were reviewed. The first connected-design review was not ready: a blank amount defaulted to zero and gave a false loss. Not-asked tokens on amounts repaired it, and the re-review accepted it with 33 modeled paths. |
| Track 1 | The content adopted as package `v46`, registry `v44` and release `v44`, with a test for each of the 33 disposition paths. |
| Track 2 | Recording, correction, withdrawal and the saved review. The owner found two defects. The shipping help excluded shipping bought with the buyer's money, and saved results were classified by whether their amount was positive. Both were repaired, with a question-to-result test and five distinct saved states. |
| Track 3 | Five per-statement figures are published as numbers or `not-computed` (package `v47`, registry `v45`, release `v45`). A display-only reader shows them, the comparison stated by the published reason, and the assumptions from provenance. An end-to-end demonstration runs the real operations and the reloaded saved explanation. |
| Closeout repair | The owner found that pass-through with additional seller-paid shipping showed incomplete figures as a gain. A named coverage stop, `additional-seller-shipping-unsupported`, replaced it (package `v48`, registry `v46`, release `v46`). A focused independent review accepted it. |

## Outcome

**What a person can do.** On a synthetic account, record one Form 1099-K or
that none was received. Answer ordinary questions about one sale: how the
item was acquired and used, the agreed price, shipping, fees, platform sales
tax, refunds and the purchase cost. Save, correct and withdraw those answers,
and read a saved explanation beside the statement. README, "Personal-item
sale on Form 1099-K", is the runnable account.

**What the calculation does.** When the account establishes a loss, the
statement's Box 1a amount is entered at the top of 2025 Schedule 1, in the
space for Form 1099-K personal items sold at a loss. Income and tax do not
change. A supported $0 statement enters $0. Recording that no Form 1099-K
was received closes the family and enters $0. Every other outcome is named
and enters nothing, and the explanation says income does not yet account for
the statement. That covers a gain, break-even, "I can't tell", an excluded
acquisition or use, digital assets, Box 4 withholding, basis adjustments, an
unexplained Box 1a difference, additional seller shipping under platform
pass-through, a second statement, and an unanswered or withdrawn answer. The
explanation keeps the report, the answers, the assumptions actually used
(none), the five published figures, the comparison and the named reason.

**Evidence.** The retained P0 authority account, the ordinary and connected
accounts, the representation and the computation design hold the decisions.
Behavior is in the Form 1099-K content, recording, review, computation and
demonstration tests. CI's `verify` check on the final candidate is the
regression gate.

**Limits.** One statement and one sale. No gain or break-even reporting on
Form 8949 or Schedule D. Additional seller-paid shipping under platform
pass-through is not deducted; that sale stops with its named reason. No
browser observation of a page. Accounts are synthetic only. The inherited
preferential-rate defect is recorded and awaits owner disposition. The 22
fast-lane budget failures are inherited and unchanged by this milestone.

Working charters, interim reviews and probes that the retained design does
not cite were removed at curation.
