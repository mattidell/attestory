<!-- foreman-context-v1
{
  "version": 1,
  "topic": "engine-breadth-phase-close",
  "status": "closed 2026-08-18; no active milestone and no successor selected or named",
  "scope": [
    "record the Engine Breadth phase close and its carried unclosed work"
  ],
  "non_goals": [
    "no active milestone",
    "no selected or named successor phase",
    "no implementation or hardening start"
  ],
  "retrospective": "docs/milestone-retrospectives/2026-08-18-engine-breadth.md",
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-18-engine-breadth.md"
    ]
  }
}
-->

# Engine Breadth Phase — Roadmap

Audience: Product (roadmap); Shared (status)

## Thesis

The engine already computes one real, auditable return slice. Engine Breadth
widens the set of valid returns it can compute by retiring one named honest
block at a time through complete vertical slices.

## How milestones are selected

Milestones are selected from `coverage-frontier.md`. A candidate must name the
unsupported return class, authoritative facts or declarations, downstream
publication or attachment, current blocker, and cheapest sufficient evidence.
Owner selection remains Tier 3.

Hardening does not become breadth because a deferral is old or important.
Security substrate, historical migration, presentation-session follow-ups, and
operational cleanup stay visible in their existing ledgers but do not enter this
roadmap unless a selected breadth slice directly depends on them.

## Phase close — 2026-08-18

**Engine Breadth is closed.** Its standing test asked whether a milestone turns
a previously honest-blocked valid-return class into an end-to-end computed
result without weakening closure, citation, contribution, or data-boundary
guarantees. The phase met that test repeatedly. Its four exit criteria are also
met: previously blocked classes operate end to end; each completed slice has
synthetic authoritative-surface evidence and keeps unsupported neighbours
explicit; the repaired frontier separates breadth from hardening and migration;
and this roadmap records the owner's decision to close with the next move left
open for owner selection.

**The coverage frontier is not exhausted.** Form 1116, other Schedule D
sources, other Schedule K-1 boxes, and a re-cut noncovered-basis/Form 8949
contract remain live candidates. Closing is a judgment, not an exhaustion:
after roughly twenty completed slices and prerequisite repairs, those rows are
more instances of a vertical shape the phase has already proved. Continuing
would buy more coverage, not a new engine capability.

**Read the completion accurately.** The phase widened what the engine
**computes**. It did not change how the user supplies facts: the user still
hand-edits JSON. It also did not make any return fileable. Real Return's close
already named both gaps; Engine Breadth did not touch them, and no row in this
phase's frontier was named for either one.

**Carried into the next phase, unclosed:**

1. **Delivered 2026-11-06 (milestone noncovered-sales, PR #261, core v79):**
   Form 8949 boxes B and E with code W, on ADR 0084. Boxes C and F were
   delivered 2026-11-07 (milestone f8949-boxes-cf, PR #262, core v80), and
   code B broker-basis corrections the same day (milestone f8949-code-b,
   PR #264, core v81). Other codes remain candidates. History: the
   noncovered / basis-not-reported Form 8949 milestone was to be re-cut
   against ADR-0066. Its reusable C1 evaluation-ordering analysis and
   `accounts_for` traversal-totality proof are archived, but old proposed
   ADR-0063/0064/0065 were superseded before ratification. Owner blocker C3
   (may a closure gate pass while documenting counterexamples to its own
   bar?) was answered no on 2026-11-06; see `PROJECT_PLANNING.md`, "Track 0
   Adversarial Closure Gate".
2. The **P1 rule-artifact/attachment-rule capability-table consolidation**
   (`docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md`)
   remains filed, scoped, deliberately unselected hardening. Seven-to-nine
   hand-maintained version allowlists broke four consecutive milestones,
   including one site fixed by review and then re-broken during curation of
   the same PR.
3. The entry and filing gaps remain outside engine breadth: fact entry still
   requires hand-edited JSON, and the product still cannot file a return.
4. Live breadth candidates remain recorded without being selected: general
   Form 1116, other Schedule D sources, other Schedule K-1 boxes, and the
   remaining Form 8949 codes and boxes C and F.
5. Every Engine Breadth milestone deferral ledger remains open by its own
   terms:

   - `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/declarative-validation-substrate-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/k1-interest-breadth-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers-deferral-ledger.md`

The coverage frontier is now the closed selection instrument of Engine
Breadth. It remains a historical inventory of delivered and unclosed classes;
it does not select, name, or scaffold what follows. That choice is open and
owner-held.

## Planned roadmap

1. **Capital-Gain Distributions and Form 1040 Line 7a** — promote Form
   1099-DIV box 2a from recorded/non-composable content into a closed source
   path; establish explicit authority for the Schedule-D-not-required route;
   publish line 7a and carry it through total income, taxable income, QDCG tax,
   explanation, packaging, and presentation on production-shaped synthetic
   fixtures.
   **Closed 2026-07-31** (PR #128). The bounded direct-reporting class is
   synthetic complete; Schedule-D-required returns remain honestly outside it.
2. **Schedule K-1 Box-5 Interest Breadth** — add 2025 Schedule K-1 (Form 1065)
   box-5 taxable interest as its own closed positive-interest family, carry it
   through Form 1040 line 2b, and replace Schedule B's temporary box-1-only
   Part-I simplification with a composition-complete multi-family itemization.
   **Closed 2026-07-31** (PR #133). The bounded Form-1065 box-5 class is synthetic
   complete; other K-1 forms and boxes, market discount, and subtractive
   adjustments remain outside it. Plan:
   `milestones/k1-interest-breadth.md`.
3. **Payer-Reported Current-Inclusion Market-Discount Interest** — closed
   2026-08-01. Add Form 1099-INT box 10 and Form 1099-OID box 5 as separate
   payer-reported current-inclusion source families, route both through the
   positive-interest composition, Form 1040 line 2b, and composition-complete
   Schedule B Part I, and stop at the statement boundary before disposition,
   basis, or transaction machinery. The bounded class is synthetic complete;
   disposition-time market discount, partial principal payments, taxpayer-side
   accrual, basis, and broader transaction situations remain outside it. Plan:
   `milestones/market-discount-interest.md`.
4. **Covered Long-Term Gains, Schedule D Line 8a** — selected 2026-08-01.
   **Closed 2026-08-02** (Track 2/3 independently reviewed `READY`). Added
   a transaction source family for covered, long-term, gain-only Form
   1099-B transactions, the nine-part Schedule D completeness boundary
   through component authority, Schedule D (line 8a, Part II line 15, Part
   III line 16) as content on the accepted attachment ontology (ADR-0036),
   and superseded the QDCG/line-16 path additively to use the Schedule D
   result for this class without editing ADR-0050. Two additive
   architecture repairs surfaced mid-milestone and were ratified in-scope:
   ADR-0055 (attachment completeness must check declared-answer *value*,
   not only presence) and ADR-0056 (blocked/not-required attachment
   dispositions must be visible on the presentation surface, not silently
   omitted). The bounded class is synthetic complete; short-term
   transactions, losses, carryovers, Form 8949, noncovered securities,
   digital assets, and other Schedule D sources remain honestly outside
   it. Plan: `milestones/schedule-d-covered-ltcg-8a.md`; curated contract
   evidence: `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/`;
   retrospective: `docs/milestone-retrospectives/2026-08-02-schedule-d-covered-ltcg-8a.md`;
   deferral ledger:
   `milestones/schedule-d-covered-ltcg-8a-deferral-ledger.md`.
5. **Schedule B Interest Adjustments** — selected 2026-08-02. **Closed
   2026-08-03**. Added a bounded 2025 adjustment path for nominee
   distributions, accrued interest paid to a bond seller, and taxable
   amortizable-bond-premium adjustments; subtracts only explicit, closed
   adjustment authority from the existing positive-interest universe and
   renders the named rows on Schedule B Part I. Schedule D remains separate
   and is not a dependency of this milestone. Plan:
   `milestones/schedule-b-interest-adjustments.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-03-schedule-b-interest-adjustments.md`.
6. **Current-Year Capital Losses and Schedule D Line 21** — selected
   2026-08-03. **Closed 2026-08-03** (Track 1 with one findings-only
   repair, Track 2, both independently reviewed `READY`). Added an
   additive successor long-term family (gain-or-loss) and a new
   short-term family (ADR-0057), each preserving the original ADR-0052
   gain-only family unedited and package-exclusive against it; a
   `selected-preferential-base` successor with a multi-family
   discriminator, an exact pin table, and a producer-side floor to
   nonnegative; signed Schedule D lines 1a/7/8a/15/16 and line 21's
   §1211 current-year loss cap (ADR-0058); and a completeness successor
   retiring two of the seven boundary declarations while preserving the
   rest. The bounded class is synthetic complete; inbound carryovers,
   Form 8949, noncovered securities, digital assets, and other Schedule D
   sources remain honestly outside it. Plan:
   `milestones/schedule-d-current-year-losses.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md`;
   deferral ledger:
   `milestones/schedule-d-current-year-losses-deferral-ledger.md`.
7. **Form 1099-DIV Box 12 to Form 1040 Line 2a** — selected 2026-08-03 and
   **closed 2026-08-04**. Promoted exempt-interest dividends into an
   independent closed source family and computed the complete bounded
   box-12-only tax-exempt interest amount on line 2a. The route preserves
   historical residual boxes, explicitly blocks other tax-exempt sources,
   box 13, and excluded downstream dependencies, and does not change line 9,
   taxable income, Schedule B, or Schedule D. The final package is v17 with
   published registry v12, release v10, and adoption v17; the independent
   re-review returned `READY`. Plan:
   `milestones/form1099div-box12-line2a.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md`.
8. **Form 1099-G Box 1 → Schedule 1 Line 7 / Form 1040 Line 8** — closed after
   rebase onto Form 8949 + box-8 tip. Plan:
   `milestones/form1099g-box1-schedule1-line7.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-05-form1099g-box1-schedule1-line7.md`.
9. **Form 1099-DIV Box 7 Direct Foreign Tax Credit (No Form 1116)** —
   selected 2026-08-05 and **closed 2026-08-05** after rebase onto Form 8949,
   box-8, and Form 1099-G. Final package is the additive union core **v21** /
   published **v16** / release **v14** / adopt **v21**
   (`artifact-package.v18`, `quantity-vocabulary.v10`, `dividend-universe.v4`).
   Independent review READY. Plan:
   `milestones/form1099div-box7-direct-ftc.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md`.
10. **Fully Taxable IRA Distributions from Form 1099-R to Form 1040 Line 4b**
    — selected 2026-08-05. Bound the class to ordinary, fully taxable
    IRA-family distributions reported on 2025 Form 1099-R; publish line 4b,
    keep line 4a blank/absent, and carry the result through line 9, AGI,
    taxable income, regular tax, package resolution, explanation, exact
    citation pins, and production-shaped presentation. Basis, rollover
    eligibility, and special distribution treatment remain outside the claim.
    Plan:
    `milestones/form1099r-ira-distributions-line4b.md`.
11. **2025 SSA-1099 Benefits through the Social Security Benefits Worksheet and
    Form 1040 Lines 6a/6b** — selected 2026-08-04 and retained as a separate
    planned milestone while the IRA line-4b route is the current active
    milestone. Track 0 must settle ordinary SSA-1099 identity, box
    reconciliation, worksheet eligibility, filing-status/lived-apart
    semantics, component-level closure, and the no-line-9-cycle graph before
    implementation. The planned class excludes RRB, lump-sum election,
    Publication 915 exception paths, excess repayments, foreign/nonresident
    benefits, new IRA/pension/unemployment/Schedule 1 support, and
    withholding/payment paths. Plan:
    `milestones/ssa1099-benefits-line6.md`.
12. **Form 1098 Home-Mortgage Interest through Schedule A and Form 1040 Line
    12e** — owner-chartered 2026-08-05 and **closed 2026-08-10** (PR #168).
    Bounded singleton-closed Form 1098 statement class: deductible interest
    derived through Schedule A line 8a from taxpayer-authority component
    facts, a composition-complete Schedule A for this class, deterministic
    standard-vs-itemized selection at line 12e (guarding the generic
    itemized assertion off whenever a Form 1098 statement is genuinely on
    record, including the contradictory-declaration case), and the correct
    2025 line-13a/13b/14 deduction-spine succession into taxable income.
    Final package is the additive union core **v29** / published **v24** /
    release **v22** / adopt **v29** over the merged SSA-1099 base. Multiple
    mortgages, refinancing, points, PMI, the mortgage-interest credit, and
    general Schedule A support remain outside it. Plan:
    `milestones/f1098-mortgage-interest-line12e.md`; retrospective:
    `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md`.
13. **SSA No-Activity Applicability Repair** — owner-approved as Milestone 1
    of a two-milestone prerequisite to Form 1098-E, and **closed 2026-08-14**
    (PR #173). A return with no applicable Social Security source now
    publishes the legally authorized line-6 zero and reaches total income
    without satisfying 33 Social Security worksheet-scope declarations.
    `rule.ss-benefits-worksheet` v2 is the sole producer of line 6b;
    `no-rrb-or-foreign-social-benefit` stays load-bearing on both routes and
    is recorded as a fourteenth migration candidate for Milestone 2. Final
    package is the additive union core **v30** / published **v25** / release
    **v23** / adopt **v30** over the merged Form 1098 base. Plan:
    `milestones/ssa-no-activity-applicability.md`; retrospective:
    `docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md`.
14. **Fact-type succession with neutral Schedule 1 vocabulary** —
    owner-approved as Milestone 2 of the same Form 1098-E prerequisite,
    and **closed on this branch (PR #177)**. No new tax route. The
    thirteen shared Schedule 1 absence declarations succeed onto
    Schedule-1-native ids via an adopted `migration-artifact.v1`
    (ADR-0063), a fourth named supersession root. Worksheet v3
    retargets the nonempty conditional set; the Milestone 1 empty-route
    contract is unchanged. Publication is the additive union core
    **v31** / published **v26** / release **v24**. Form 1098-E,
    Schedule 1 line 21, Form 1040 line 10, and AGI remain Part 3.
    Plan: `milestones/fact-type-succession-neutral-schedule1.md`;
    retrospective:
    `docs/milestone-retrospectives/2026-08-14-fact-type-succession-neutral-schedule1.md`.
15. **Declarative Structured Validation and Consumer Dependency Substrate**
    — owner-selected 2026-08-12 as a hardening prerequisite, not a new tax
    route: retires the hard-coded Form 8949/Form 1099-B row-guard and
    identity-collision mechanisms the closed covered-wash-sale milestone
    (item 4 below in Status) left in generic runner/package-validator code,
    replacing them with versioned-content member constraints, declared
    cross-family identity exclusivity, and reachability-derived consumer
    prerequisites (ADR-0066). **Closed 2026-08-17.** `runner.py`'s domain
    references went from 24 to 0. Both schedulers proven byte-identical on
    the migrated content, including attachment-bearing citizens (a
    pre-existing `reference_runner.py` gap, repaired in-milestone). An
    independent owner-advisor product review found and repaired a failing
    type gate and a stale cross-milestone test before close. Publication is
    the additive union core **v32** / published **v27** / release **v25** /
    adopt **v32** over the merged core v31 base. Plan:
    `milestones/declarative-validation-substrate.md`; deferral ledger:
    `milestones/declarative-validation-substrate-deferral-ledger.md`;
    retrospective:
    `docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md`.
16. **2025 Form 1098-E Student-Loan Interest through Schedule 1 Lines 21/26
    and AGI** — re-cut and **closed 2026-08-18**. Opens the first Engine
    Breadth route on the income-adjustment side of the return: a single
    2025 Form 1098-E statement's deductible interest, capped at $2,500 and
    reduced by the MAGI phaseout, computed on the Student Loan Interest
    Deduction Worksheet as rule content and carried through Schedule 1
    lines 21/26 into Form 1040 line 10 and AGI (lines 11a/11b). The
    additive `multiply`/`divide`/`collect_categorical_all_equal` expression-
    language extension (ADR-0064) and the first application of ADR-0016
    decision 4 to a mixed absent/present/structural-zero Schedule 1 Part II
    total (ADR-0065). Rebased and rebuilt onto the closed
    declarative-validation-substrate-f8949 base after that milestone merged
    mid-build; the two milestones' packages collided ADD/ADD on the same
    version number, resolved by rebuilding on top of the ratified content
    rather than renumbering schemas. Final package is the additive union
    core **v33** / published **v28** / release **v26** / adopt **v33**,
    over the merged core v32 base. An independent review of PR #178
    (curated object `64c540ce`) returned `CHANGES REQUESTED` on two
    curation-introduced defects; both fixed and the gate re-verified green.
    Plan:
    `milestones/f1098e-student-loan-interest-agi.md`; deferral ledger:
    `milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`;
    retrospective:
    `docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md`.

**Next breadth slice — owner-unselected.**
Inbound capital-loss carryovers, Form 8949/noncovered securities/adjustments,
and other Schedule D sources remain distinct candidates; other Form 1099-R
distribution treatments and unrelated income domains remain outside the
selected class.

## Bounded return — The 2025 Tax on Taxable Income — closed 2026-10-22

[Plan](milestones/tax-on-taxable-income.md).

Form 1040 line 16 and the standard deduction still run on `demo.*`
parameters: a truncated three-bracket schedule at 2024 thresholds, a flat
15 percent preferential rate, a pre-legislation standard deduction and no Tax
Table. A short-term-gain defect in the preferential base is also recorded.
Verify the 2025 law from primary sources, then replace these with successor
content so every route the phase made computable also computes correctly. No
new return class is added.

Closed on core calculations v50: verified parameters, the Tax Table and Tax
Computation Worksheet, the capital gains worksheet published line by line, the
preferential base repaired, and the 2025 standard deduction. Earlier packages
keep their results. See the plan's outcome and the
[retrospective](../../milestone-retrospectives/2026-10-22-tax-on-taxable-income.md).

## Bounded return — The 2025 Senior Deduction and a Dependent's Standard Deduction

[Plan](milestones/senior-and-dependent-deductions.md).

The tax milestone named two deductions it did not compute: the enhanced
deduction for seniors (Schedule 1-A Part V) and a dependent's limited
standard deduction. Both change real returns: a senior lost up to $6,000 per
person on line 13b, and a dependent received the full standard deduction.
Compute both as successor content on core v51, each from a question whose
meaning matches the rule that reads it.

## Bounded return — Refund or Amount Owed: Finishing the 2025 Return

[Plan](milestones/refund-or-amount-owed.md).

Every computed return stopped at tax after credits. Carry it to total tax,
withholding, payments and the refund or amount owed, recording withholding on
the documents the engine already reads, and declare absent the taxes and
credits it does not compute.

## Bounded return — The 2025 Earned Income Credit

[Plan](milestones/earned-income-credit.md).

Lines 27a-31 were $0 by one absence answer, so an eligible low-income worker
lost the credit or was outside the supported class. Compute the credit for
filers with no qualifying child first, from the printed EIC Table, asking the
eligibility questions only where income allows the credit.

## Bounded return — The 2025 Earned Income Credit with Qualifying Children

[Plan](milestones/eic-qualifying-children.md).

A filer with a qualifying child was outside the class on core v53. Count
each child from per-child answers, take the table column for that count, and
refuse when another person may also claim a child.

## Bounded return — The 2025 Child Tax Credit

[Plan](milestones/child-tax-credit.md).

Lines 19 and 28 were $0 by absence answers. Compute the child tax credit and
the additional child tax credit from Schedule 8812 for qualifying children on
a credit roster over the EIC child kind, including Part II-B for three or
more children.

## Bounded return — The 2025 Credit for Other Dependents

[Plan](milestones/other-dependents-credit.md).

A return with a dependent who was not a qualifying child under 17 was
blocked. Add the $500 credit for children marked for it and for qualifying
relatives, combined with the child tax credit, finishing Schedule 8812 for
the class.

## Bounded return — A Child More Than One Person Could Claim (2025)

[Plan](milestones/dependent-tie-breaker.md).

A child who also lived with, or was related to, someone else was refused for
all three child credits. Resolve the tie-breaker rules from answers about the
other person, for the earned income credit, child tax credit and credit for
other dependents together.

## Bounded return — Federal Tax Withheld on Forms 1099 (2025)

[Plan](milestones/form-1099-withholding.md).

Withholding on unemployment (Form 1099-G box 4) and Social Security (Form
SSA-1099 box 6) refused the return. Count it on line 25b on a successor
package, while earlier packages keep refusing it.

## Bounded return — An Unresolved Form 1099-K Stops the Bottom Line (2025)

[Plan](milestones/form-1099-k-income.md).

A Form 1099-K the engine could not resolve was left out of total income while
the refund published. Block Schedule 1 line 10 on a successor package until
every Form 1099-K is resolved and confirmed complete.

## Bounded return — Withholding Waits for Every Statement (2025)

[Plan](milestones/withholding-closure.md).

A recorded Form 1099 withholding amount counted on line 25b while its family
was not confirmed complete, so the refund published on a partial sum. Line
25b waits for every withholding family on a successor package.

## Bounded return — Every Sum Waits for Its Statements (2025)

[Plan](milestones/collect-closure-survey.md).

A survey of every rule that collects a source set found 16 that published a
partial sum while the family was unconfirmed. Five successor rules guard
seven of them on core v62, and a regression test fails on any new unguarded
path. The nine interest families behind line 2b, and the attachments, are
still open.

## Bounded return — Every Attachment Waits for Its Statements (2025)

[Plan](milestones/attachment-closure.md).

Schedule D, Form 8949, Schedule 1 and Schedule B published amounts from
unconfirmed families while the lines they support blocked, and line 2b
summed unconfirmed interest. Twenty subtotal successors on core v63 make
each wait; line 2b needed no validator change after all.

## Bounded return — Each Credit Line Explains Itself (2025)

[Plan](milestones/credit-line-explanations.md).

Seven child tax credit form fields carried line 27a's earned income credit
explanations word for word. Corrected successors on core v64, and a check
that fails on a copied explanation; no value changes.

## Bounded return — Gambling Winnings on Form W-2G (2025)

[Plan](milestones/w2g-gambling.md).

Line 25c was a constant zero and a return with gambling winnings was
refused by answer. On core v65, Form W-2G box 1 reaches Schedule 1 line 8b
and box 4 reaches line 25c, each family with its own closure; every earlier
package refuses a recorded W-2G.

## Bounded return — Statements With Cents (2025)

[Plan](milestones/itemization-cents.md).

Statements with cents blocked Schedule 1, Schedule D and Schedule B on the
tie-out, and lines that add several amounts rounded each first. On core v66
those lines include cents and round once at the total; Schedule B Part I
interest waits on a validator question.

## Bounded return — A Blocked Line Names Its Question (2025), closed on P0

[Plan](milestones/closure-question-wording.md).

No closure family declares its question, and naming it needs a schema
successor and a coordinator admission change, so the milestone closed on
its investigation; the design is an open owner-held question.

## Bounded return — A Correction Recalculates on the Current Core (2025)

[Plan](milestones/correction-current-core.md).

The correction session pinned registry v40 and refused every workspace
adopted after core v42. It now resolves the surface from the workspace's
adoption, so corrections calculate on the current core.

## Bounded return — Gambling Losses (2025)

[Plan](milestones/gambling-losses.md).

Gambling losses refused a Form W-2G return even on the standard deduction.
On core v67 a standard-deduction filer computes unchanged and an itemizer
deducts losses up to winnings on Schedule A line 16; the Schedule A
attachment does not itemize line 16 (open owner question).

## Bounded return — Interest With Cents (2025)

[Plan](milestones/interest-cents.md).

Interest with cents blocked Schedule B Part I and line 2b rounded each
subtotal first. With two owner-approved validator changes, core v68 lets
the interest subtotals keep their cents and line 2b round once.

## Bounded return — A Blocked Line Names Its Question, Built (2025)

[Plan](milestones/closure-questions.md).

Every closure on core v69 declares its question in plain words, and a line
held only by unconfirmed families names those questions instead of a
generic "blocked" text.

## Bounded return — Schedule A Shows Gambling Losses (2025)

[Plan](milestones/attachment-limited-part.md).

The Schedule A attachment now itemizes gambling losses on line 16, limited
to winnings, through a conditional and limited attachment part
(`attachment-rule.v12`); a losses-only itemizer's attachment publishes.

## Bounded return — The W-2 Entry Loop Follows Its Adopted Core (2025)

[Plan](milestones/entry-loop-rescope.md); retrospective:
`docs/milestone-retrospectives/2026-11-01-entry-loop-rescope.md`.

The entry loop now resolves the adopted surface and exact profile for package
v6 or v70. The v70 technical exercise starts with Box 1 missing, records first
entry and correction, and agrees with a fresh coordinator run; the v6 seed and
behavior remain intact. This is not usability validation or support for
unlisted future cores. Correction guidance is tracked separately below and
does not expand this runtime or tax-coverage claim.

## Delivered on milestone branch — W-2 correction guidance (2025)

The bounded v6/v70 correction surface distinguishes a saved amount from
calculation disposition and authorization currentness. It keeps blocked null
figures unavailable rather than zero, separates known validation rejection
from save uncertainty, and labels prior figures after a post-save calculation
failure. A response is installed only after it parses and matches the page's
bounded snapshot shape; an unusable successful response preserves the last
confirmed view and offers a state read without resubmitting. A usable read
recovers the saved state.

This is same-running-session recovery, not process-restart recovery or an
automatic recalculation retry. A demonstrated v70 line held only by an
unconfirmed family displays its recorded closure question verbatim, including
in the compiled page. Other outcomes without a safe attached sentence retain
general guidance; this is not universal question diagnosis. This is surface
behavior, not new tax coverage. The milestone is closed on its branch;
exact-candidate CI remains the publication gate. Plan:
`milestones/w2-correction-guidance.md`; retrospective:
`docs/milestone-retrospectives/2026-11-02-w2-correction-guidance.md`.

## Bounded return — Each Statement Answers Its Withholding (2025)

[Plan](milestones/statement-withholding-answer.md); retrospective:
`docs/milestone-retrospectives/2026-11-02-statement-withholding-answer.md`.

On core v71 line 25b waits until each Form 1099-INT, 1099-DIV, 1099-R and
1099-G carries its box 4 answer, and each SSA-1099 its box 6 answer, $0
included, as line 25a does for W-2 box 2. An answered return computes as on
v70.

## Bounded return — A Blocked Line Names What Is Missing (2025)

[Plan](milestones/missing-input-questions.md); retrospective:
`docs/milestone-retrospectives/2026-11-03-missing-input-questions.md`.

On core v72 a line blocked because W-2 box 2, a Form 1099 box 4, SSA-1099
box 6, or the line 26 or 36 amount is missing names what to enter and that
$0 is an answer, through a declared `input-question` citizen. Earlier cores
render byte-identically.

## Bounded return — A Blocked Line Asks Its Yes-or-No Question (2025)

[Plan](milestones/scope-answer-questions.md); retrospective:
`docs/milestone-retrospectives/2026-11-03-scope-answer-questions.md`.

On core v73 a line blocked on a missing yes/no scope answer or filing status
names one of 41 filer questions covering 80 facts, each asking about
presence. Earlier cores render byte-identically.

## Bounded return — The Return Answers What It Already Shows (2025)

[Plan](milestones/derived-answers.md); retrospective:
`docs/milestone-retrospectives/2026-11-03-derived-answers.md`.

On core v74 a recorded Form 1098 answers the Form 1098 question, and Form
1099-DIV box 7 over $300 ($600 joint) answers whether Form 1116 is required.
The record proves presence only, so the other direction is still asked.
Earlier cores are unchanged.

## Bounded return — Every Unconfirmed Family Asks Its Question (2025)

[Plan](milestones/closure-question-coverage.md); retrospective:
`docs/milestone-retrospectives/2026-11-04-closure-question-coverage.md`.

From core v75 an unconfirmed Form 1099-B wash-sale family names its
completeness question on the 32 lines it blocks, and Form 1099-K's two
Schedule 1 selection lines name it beside the single-sale question. All 51
families now name their question. Earlier cores are unchanged.

## Bounded return — Every Question At Once (2025)

[Plan](milestones/all-questions-at-once.md); retrospective:
`docs/milestone-retrospectives/2026-11-04-all-questions-at-once.md`.

From core v76 the completeness questions a blocked return could already ask
appear in round one, and a statement's withholding amount as soon as the
statement is recorded. Answering takes 2 rounds instead of 4 for open
amounts and the mortgage, 3 instead of 4 for Form 1099-B, and 5 instead of
6 for a dependent or foreign tax. Earlier cores are unchanged.

## Bounded return — Each Statement Is Checked For Its Own Withholding (2025)

[Plan](milestones/statement-withholding-pairing.md); retrospective:
`docs/milestone-retrospectives/2026-11-05-statement-withholding-pairing.md`.

On core v77 lines 25a and 25b block unless each statement with income has
its own withholding answer, through the new `require_paired` guard. Eleven
returns that published a wrong amount on v76 now block and ask the existing
question. Earlier cores are unchanged.

## Bounded return — Every Line Says What It Adds (2025)

[Plan](milestones/line-explanations.md); retrospective:
`docs/milestone-retrospectives/2026-11-05-line-explanations.md`.

On core v78, 31 form lines that said only "blocked", "guard false" or
"computed zero" say in plain words what they add, why they are zero, what
they wait for, or when they are computed. Values and dispositions are
unchanged from v77.

## Bounded return — Sales Whose Basis Was Not Reported (2025)

[Plan](milestones/noncovered-sales.md); retrospective:
`docs/milestone-retrospectives/2026-11-06-noncovered-sales.md`.

On core v79 a Form 1099-B sale whose basis was not reported to the IRS
reaches Form 8949 box B or E, Schedule D line 2 or 9, Form 1040 line 7a and
the tax, from a basis the filer supplies, with code W allowed. One question
closes the eight new families (ADR 0084, `source-closure-mapping.v4`). A
covered sale flagged basis-not-reported now blocks with its own reason
instead of publishing line 8a. Earlier cores are unchanged.

## Bounded return — Sales Without a Form 1099-B (2025)

[Plan](milestones/f8949-boxes-cf.md); retrospective:
`docs/milestone-retrospectives/2026-11-07-f8949-boxes-cf.md`.

On core v80 a sale of securities with no Form 1099-B or substitute statement
reaches Form 8949 box C or F, Schedule D line 3 or 10, Form 1040 line 7a and
the tax, from proceeds and basis the filer supplies, with code W allowed. A
second grouped question closes the new families and keeps every v79 answer's
meaning. Lines 2, 3, 9 and 10 now block when a sale is missing an amount,
shares a record with another sale, or disagrees with its own amounts. Ten
returns that v79 published silently or wrongly now block. Earlier cores are
unchanged.

## Bounded return — Broker Basis Corrections (2025)

[Plan](milestones/f8949-code-b.md); retrospective:
`docs/milestone-retrospectives/2026-11-07-f8949-code-b.md`.

On core v81 a Form 1099-B sale whose reported basis is wrong reaches Form 8949
box A or D with code B. Column (e) shows the broker's basis, and column (g)
carries the correction (BW rows net the wash-sale amount). The sale then
reaches Schedule D line 1b or 8b, Form 1040 line 7a and the tax, from a
correct basis the filer supplies. One new grouped question closes the new
families, and every v80 return answered "no" computes the same.

Several v80 gaps are also closed:
- a zero-proceeds sale now requires its attachments, and line 7a counts lines
  1a and 8a;
- one transaction on two families now blocks instead of counting twice;
- a covered sale flagged for a filer-side adjustment, ordinary income, market
  discount, QOF or collectibles treatment now blocks instead of publishing.

Earlier cores are unchanged.

## Bounded return — Every Sale Fact Is Read (2025)

[Plan](milestones/sale-family-audit.md); retrospective:
`docs/milestone-retrospectives/2026-11-09-sale-family-audit.md`.

An audit of every Form 1099-B and Form 8949 sale family on core v81 found
eight defects; core v82 fixes them with content and loader entries only:
- a filer who answers the Exception 1 questions truthfully now gets the
  Schedule D tax route instead of no tax, and the questions are reworded so
  each "yes" means its fact's "yes";
- line 7a and the preferential base count sales that net to zero, and line
  7b no longer says Schedule D is not required beside a recorded sale;
- boxes C and F have a count, so a 0/0 sale requires its attachments;
- box 1g on direct sales and `long_term` on covered and code W sales are read;
- every amount row must sit on its own sale, on every sale kind;
- box 4 backup withholding and box 7 are asked once per Form 1099-B
  statement and refuse on "yes".

The audit is a committed test: a sale fact field that loses its last reader
fails it. No v81 published number changes; earlier cores are unchanged.

## Bounded return — Form 1099-B Backup Withholding (2025)

[Plan](milestones/f1099b-backup-withholding.md); retrospective:
`docs/milestone-retrospectives/2026-11-10-f1099b-backup-withholding.md`.

Core v83 replaces v82's refusal on a box 4 "yes" with one box 4 amount per
Form 1099-B statement. Every current amount adds to Form 1040 line 25b,
including one whose statement has no recorded sale; a statement with a
sale and no amount blocks line 25b with its question. A return with no
sales is asked nothing new. Of the 213 v82 returns, 150 now ask the amount
and 63 are identical; none publishes a different number. Earlier cores are
unchanged.

## Bounded return — Form 1099-B Box 7 Read Only Beside a Loss (2025)

[Plan](milestones/f1099b-box7-loss.md); retrospective:
`docs/milestone-retrospectives/2026-11-10-f1099b-box7-loss.md`.

Core v84 replaces v83's refusal on any box 7 "yes" with a per-sale verdict.
A checked statement whose sales are gains or zero computes; one sale at a
loss on a checked statement blocks Schedule D line 16 and asks nothing. The
box 7 question is unchanged. All 298 recorded v83 returns are identical on
v84; earlier cores are unchanged.

## Bounded return — Form 1099-B Backup Withholding Without a Sale (2025)

[Plan](milestones/f1099b-box4-only.md); retrospective:
`docs/milestone-retrospectives/2026-11-10-f1099b-box4-only.md`.

Core v85 asks every return whether it received a Form 1099-B that shows
box 4 withholding and no closed sale (an open short at year end). A yes
asks one total, added to line 25b; a no asks nothing more. The
per-statement box 4 question is unchanged. Of the 298 recorded returns, 207
are identical and 91 newly ask the yes/no; answering no restores every
number. Earlier cores are unchanged.

## Bounded return — Form 8949 Code L for a Box 7 Loss (2025), closed on P0

[Plan](milestones/f8949-code-l.md); retrospective:
`docs/milestone-retrospectives/2026-11-10-f8949-code-l.md`.

A box 7 loss is wholly disallowed and reported on Form 8949 with code L,
column (g) the whole loss and column (h) zero (Schedule D Example 2). A
Form 8949 row is a recorded family member, and no content successor can
emit one, so the milestone closed on its investigation; the recording
change is an open owner-held question. The fast-lane schema-compile fix
landed with it.

## Bounded return — Live Evidence Harnesses Run in Isolation (tooling)

[Plan](milestones/live-harness-isolation.md); retrospective:
`docs/milestone-retrospectives/2026-11-11-live-harness-isolation.md`.

Every in-process evidence harness load in `tests/` goes through
`tests/evidence_loader.py`: private module copies per test module, and
engine attributes a harness writes restored when that module is parked or
finished. A guard test fails on any other load of an evidence file, `exec`
included. No package, schema, content or assertion changed.

## Bounded return — The v70 Entry Seed Generates Without Test Helpers (tooling)

[Plan](milestones/seed-generator-independence.md); retrospective:
`docs/milestone-retrospectives/2026-11-11-seed-generator-independence.md`.

The v70 W-2 entry seed generator reads a committed synthetic source,
`packages/sample_data/entry_loop_v70/complete-core-return.jsonl`, and
imports no test module; a static and a run-time check pin that. The seed's
bytes are unchanged. Refreshing the source is deliberate, by the recipe in
the generator's docstring.

## Bounded return — A Selection Path Collects a Keyed Family Directly (2025)

[Plan](milestones/selection-keyed-collect.md); retrospective:
`docs/milestone-retrospectives/2026-11-10-selection-keyed-collect.md`.
ADR 0085 (proposed).

From core v86 a selection path's collect of its own activity family is not
a symbol it waits for, and `rule-artifact.v16` allows one path with a
default. Core v86 retires the rule that published 0 under the Form 1099-B
box 4 amount id and the box 4 subtotal's inert path. Every recorded return
is identical; earlier cores are unchanged.

## Bounded return — Questions Say What Their Rules Read (2025)

[Plan](milestones/question-wording.md); retrospective:
`docs/milestone-retrospectives/2026-11-11-question-wording.md`.

Core v87 (registry v85, release v85) rewords four questions and three fact
titles; no rule, engine, schema or recording surface changed. The two
wash-sale adjustment amount questions ask only of covered sales with a
wash-sale loss adjustment. The Exception 1 only-box-2a question counts only
a sale that must be reported on Form 8949 or Schedule D: sales inside an IRA
or 401(k) do not count, nor does a personal-item loss unless a Form 1099-S
was received or the loss is reported on Form 8949. The student-loan
dependent question names the spouse on a joint return. The age and
blindness titles state the 2025 rules (born before January 2, 1961; the
death-in-2025 rule; blindness as of December 31, 2025). The 298 recorded
v83 runs are identical on v87.

## Bounded return — Recorded Returns Replay in Parallel (tooling)

[Plan](milestones/parallel-replay.md); retrospective:
`docs/milestone-retrospectives/2026-11-12-parallel-replay.md`.

`tools/recorded_replay.py` replays the 775 recorded act lists content
milestones compare across cores in parallel worker processes: about 43
minutes on 4 workers against about 3.8 hours single-process, with the
same rows as question-wording's committed neighbour output. Each list's
pins are stored once per core, so a P0 rerun table and a Track 0
neighbour table come from one replay; a part file is bound to its cores
and resumes. No package, schema or engine changed.

## Bounded return — Age and Blindness Are Asked (2025)

[Plan](milestones/age-blindness-asked.md); retrospective:
`docs/milestone-retrospectives/2026-11-12-age-blindness-asked.md`.

Core v88 (registry v86, release v86) asks the filer's age and blindness,
and on a joint return the spouse's, instead of defaulting them to false:
born before January 2, 1961 (the day-before-the-birthday rule; a 2025
death before 65 answers no), and blind on December 31, 2025 or by an eye
doctor's certified statement. On a separate return one question asks
whether the spouse had no income, isn't filing and can't be claimed as a
dependent; only a yes asks the spouse's age and blindness. A qualifying
surviving spouse counts only the filer's boxes, as the 2025 chart does.
Content only. The 775 recorded lists, answered as their records imply,
compute the same numbers.

## Bounded return — Blocked Lines Name Their Question (2025)

[Plan](milestones/blocked-names-question.md); retrospective:
`docs/milestone-retrospectives/2026-11-13-blocked-names-question.md`.
Contract: ADR 0086.

`rule-artifact.v17` (admitted by `artifact-package.v43`) lets an
expression `block` declare the names it waits on, and the evaluator and
runner carry them, so the page can show the question. Core v89 (registry
v87, release v87) uses it in eleven rule successors, adds the two Schedule
D boundary questions, and asks the wash-sale adjustment question before
per-sale pairing. The dead ends this closed: refused Schedule D and code B
paths, a Form 8949 "no" nothing admits, disagreeing amounts, an unanswered
Path B, an Exception 1 "no" for a personal-item loss reported on Form 8949
with no sale, and a recorded wash sale with the adjustment family open.
The 775 recorded lists compute the same numbers; no computing return is
newly asked a question.

## Bounded return — Line 12d's Boxes Are Shown (2025)

[Plan](milestones/line12d-boxes.md); retrospective:
`docs/milestone-retrospectives/2026-11-15-line12d-boxes.md`.

Core v90 (registry v88, release v88) adds Form 1040 line 12d's four boxes
as form fields: you and your spouse, born before January 2, 1961, and
blind. Each box is drawn checked or not checked from the recorded answer,
and is blocked with its question while the answer is missing. The spouse
boxes show on a joint return, or on a separate return whose spouse
condition is yes. The saved citation-walk page now draws a `not_checked`
box as "not checked"; line 6d's alert clears and line 6c's `not_elected`
alert stays. The 775 recorded lists compute the same numbers.

## Bounded return — Lines Below Line 16 Name Their Question (2025)

[Plan](milestones/preferential-base-reason.md); retrospective:
`docs/milestone-retrospectives/2026-11-15-preferential-base-reason.md`.
Contract: ADR 0086.

Core v91 (registry v89, release v89) replaces one member,
`selected-preferential-base` v11. On a return where Schedule D is
required and no sale or Schedule D amount is recorded, the preferential
base now blocks and names eight questions (the four sale and boundary
questions line 16 names, and the four Exception 1 questions) where it was
inapplicable. The 23 blocked fields that showed no question on such a
return, among them Form 1040 lines 7a, 9, 11, 15, 24, 33 and 37, now show
those questions. Changing Exception 1 to yes, or entering the sale,
reaches the instruction values. Of the 775 recorded lists, 771 are
identical and four change only that row and its sentences.

## Bounded return — The Box 4 Withholding Amount Is Asked (2025), closed on P0

[Plan](milestones/box4-amount-asked.md); retrospective:
`docs/milestone-retrospectives/2026-11-15-box4-amount-asked.md`.

Opened on a parked finding that Form 1040 lines 25b and 25d block with no
question when a Form 1099-B box 4 amount is missing. P0 showed published
core v91 already asks: both lines, and lines 33, 34, 35a and 37 behind
them, show the published amount prompt, and entering the amount reaches
the instruction values. The finding came from a probe that kept only
sentences with a question mark. Nothing was published; core v91, registry
v89 and release v89 stand.

## Bounded return — Saved Pages Without Alerts on Line 6c and Schedule 1 (2025)

[Plan](milestones/page-alerts.md); retrospective:
`docs/milestone-retrospectives/2026-11-16-page-alerts.md`.

Core v92 (registry v90, release v90) clears the two safe-render alerts
every computing return's saved page showed. Form 1040 line 6c is drawn
"not checked" where the lump-sum election was not made and, on a new
sibling field, "checked" where it was; an unanswered election blocks both
with its question. The Schedule 1 top entry has a citation, so its value
shows: 0 with "No gross payment amount in box 1a of a Form 1099-K for
personal items you sold was recorded for 2025.", or the personal-item
loss amount. All 691 computing recorded returns draw neither alert, and
the 775 recorded lists compute the same numbers. The page is unchanged.

## Bounded return — Line 6b Names Why It Is Blocked (2025)

[Plan](milestones/line6b-reason.md); retrospective:
`docs/milestone-retrospectives/2026-11-16-line6b-reason.md`.

Core v93 (registry v91, release v91) adopts ten input-question citizens,
so a blocked Form 1040 line 6b on a return with a Form SSA-1099 benefit
statement asks the question that unblocks it: eight Social Security
Benefits Worksheet scope questions, the Schedule 1 line 24z write-in
question and, for a separate filer, whether the filer lived apart from
their spouse all year. Line 6d, already blocked on that last fact, now
asks it too. No rule changed. The 775 recorded lists keep their selected
pins, and 255 current neighbour returns change no value, disposition,
required answer or refusal code. When two causes are open on a separate
return, line 6b names the one its worksheet rule refuses on first and
line 6d names living apart.

## Bounded return — A Box 4 "No" Is Not Asked For an Amount (2025)

[Plan](milestones/box4-no-prompt.md); retrospective:
`docs/milestone-retrospectives/2026-11-17-box4-no-prompt.md`.

Core v94 (registry v92, release v92) lets a Form 1099-B statement whose
box 4 the filer answered "no" stand for no withholding on that
statement: Form 1040 line 25b no longer waits for its amount, and the
box 4 amount question now asks only for statements answered "yes" or
not answered. Each statement is judged alone; an entered amount wins
over a "no"; any statement not satisfied runs the v93 pairing unchanged.
Of the 775 recorded lists, 271 now name the return-level "statement
with no sale" question on line 25b instead of the amount and 125 show
the new amount words; no value, disposition or refusal code changed.

## Bounded return — Line 16 Names the Failing Exception 1 Criteria (2025)

[Plan](milestones/line16-names.md); retrospective:
`docs/milestone-retrospectives/2026-11-17-line16-names.md`.

Core v95 (registry v93, release v93) changes what Form 1040 line 16 and
the selected preferential base name on a return where Schedule D is
required, no sale is recorded and "no Form 8949" is answered yes: each
names exactly the Exception 1 criteria whose current answer fails, so
line 16, its four dependants (line 20, Schedule 3 lines 1 and 8,
Schedule 8812 worksheet A line 5) and the 23 other blocked fields agree
and every name is an answer that can move them. A reported personal-item
loss keeps its four names; an unanswered "no Form 8949" asks that
question. Of 775 recorded lists, the four honest returns in that state
change their names; on the replay's retained surface no value,
disposition or refusal code changed.

## Bounded return — Every Line Speaks Plainly (2025)

[Plan](milestones/plain-line-texts.md); retrospective:
`docs/milestone-retrospectives/2026-11-17-plain-line-texts.md`.

Core v96 (registry v94, release v94) rewords the content texts a filer
sees on a saved page: line explanations, attachment headings, blocked
reasons and drawn mortgage notes no longer say "derived finding",
"closed-empty", "authority" or "computed zero for line X". A zero says
whether it comes from no record or from amounts that round to zero. 61
content successors, plus one validator entry admitting line 2b's
wording successor. Of 775 recorded lists, 691 change only these
sentences and 84 fail as before; no value, disposition, refusal code,
missing name or question changed.

## Bounded return — Replays Run Three Times Faster (2025)

[Plan](milestones/rust-kernel-experiment.md); retrospective:
`docs/milestone-retrospectives/2026-11-18-rust-kernel-experiment.md`.

An engineering experiment on whether to move the engine to Rust. P0
profiled the 775 recorded lists and found the kernel at about 6 % of a
replay; the time was in derivation algorithms. Four Python fixes
(package-validation index and memo, a memoized blocked-line question
walk, a marshal precompute) took the median list from 7.76 s to 2.94 s
and the slowest from 49.6 s to 3.55 s, with every recorded list
byte-identical. No package version change. The Rust port is parked.

## Bounded return — Member Files Are Read Once (2025)

[Plan](milestones/member-reads-once.md); retrospective:
`docs/milestone-retrospectives/2026-11-18-member-reads-once.md`.

Each replay read, parsed and checksummed all 1,813 member files four
times. A per-process cache keyed on the bytes read now parses and
checksums each distinct file once; an edited file is always re-parsed,
and callers get read-only views or private copies. All 775 recorded
lists replay byte-identically. Paired timing of the median list: 2.12 s
uncached, 1.67 s cold, 1.62 s warm. No package version change.

## Bounded return — Sale Reasons Speak Plainly (2025), closed on P0

[Plan](milestones/sale-reasons-plain.md); retrospective:
`docs/milestone-retrospectives/2026-11-18-sale-reasons-plain.md`.

The two parked sale reasons cannot be reworded by content: they are the
meaning text of sale source-family checks, pinned by version in every
saved sale record and copied into a published value. P0 drafted plain
sentences and parked the change behind a projection and schema route.
No package version change.

## Bounded return — Replays Compare the Whole Saved Return (2025)

[Plan](milestones/full-surface-replay.md); retrospective:
`docs/milestone-retrospectives/2026-11-18-full-surface-replay.md`.

`tools/recorded_replay.py` gains a full-surface comparison: every saved
field, explanation node and report row as typed records, a strict diff
that fails any undeclared difference, and controls that mutate the saved
output before the snapshot. It closes the line16-names L16-R1 gap.
v95 against v96 with plain-line-texts' declared changes passes all 775
lists with no unexpected difference. No package version change.

## Bounded return — Box C and F Losses Are Limited (2025)

[Plan](milestones/cf-loss-limit.md); retrospective:
`docs/milestone-retrospectives/2026-11-18-cf-loss-limit.md`.

A loss from Form 8949 boxes C and F (no Form 1099-B) is limited on
Schedule D line 21 exactly as a box A/D loss is, under every filing
status: 900 of 900 line checks match hand values. Tests pin it and that
no 2026 carryover is published. No package version change.

## Bounded return — Gains and Break-Even Sales Reach Schedule D (2025)

[Plan](milestones/gain-break-even.md); retrospective:
`docs/milestone-retrospectives/2026-11-19-gain-break-even.md`.

A gain and an exact break-even reach Form 8949, Schedule D and the line
16 tax correctly on every accepted sale path (covered, code W, code B,
noncovered, no Form 1099-B; short and long term): 1,134 of 1,134 checks
match hand values. Tests pin 27 returns on core v96. No package version
change.

## Bounded return — A Form 1099-B Bartering Amount Is Not Lost (2025)

[Plan](milestones/f1099b-bartering.md); retrospective:
`docs/milestone-retrospectives/2026-11-19-f1099b-bartering.md`.

Core v97 (registry v95, release v95) adds one sentence to the five
Schedule 1 lines 2a-6 questions: answer yes for a Form 1099-B box 13
bartering amount above zero. Before it, a filer who answered as worded
got a return with the bartering income silently left out; a yes now
refuses the return through the existing line 10 path. The full-surface
replay of 775 recorded lists changed only the package version.

## Bounded return — Chrome Cleanup Does Not Hang CI

[Plan](milestones/chrome-cleanup-hang.md); retrospective:
`docs/milestone-retrospectives/2026-11-19-chrome-cleanup-hang.md`.

The saved-page observer ends Chrome's whole process group on cleanup.
When cleanup still fails, it closes its server and exits promptly with
`browser-cleanup-failed` instead of hanging `verify` for 240 s. Harness
and test-helper change only; no package version change.

## Bounded return — Head of Household Needs a Qualifying Person (2025)

[Plan](milestones/hoh-qualifying-person.md); retrospective:
`docs/milestone-retrospectives/2026-11-19-hoh-qualifying-person.md`.

Core v98 (registry v96, release v96) asks a filer who chooses head of
household or qualifying surviving spouse whether that status's tests are
met. Before it, either status took its larger standard deduction and tax
column with nothing asked. A yes keeps every amount, and a no refuses
line 12e with the question shown. The other three statuses are unchanged.

## Bounded return — The Earned Income Credit for a Head of Household (2025)

[Plan](milestones/hoh-eic.md); retrospective:
`docs/milestone-retrospectives/2026-11-19-hoh-eic.md`.

Core v99 (registry v97, release v97) asks a head of household with no
qualifying child whether they were unmarried at the end of 2025. Yes
figures the credit as for a single filer, where v98 gave $0; no keeps $0
and asks nothing more. The separated-spouse answer now has a question.
Every other filer keeps v98's values.

## Bounded return — Every Earned Income Credit Answer Has a Question (2025)

[Plan](milestones/eic-answer-questions.md); retrospective:
`docs/milestone-retrospectives/2026-11-19-eic-answer-questions.md`.

Core v100 (registry v98, release v98) adds questions for the four
earned income credit answers that had none: age, main home, not
claimable as a dependent, and the spouse's SSN. A filer missing one was
blocked on the credit and refund lines with no sentence; now the page
asks. No rule changed, and every answered return computes as before.

## Bounded return — Validation Reuses Member Checksums

[Plan](milestones/validation-checksum-reuse.md); retrospective:
`docs/milestone-retrospectives/2026-11-23-validation-checksum-reuse.md`.

The validation memo key and `validate_package` reuse the member cache's
checksum for the same bytes instead of recomputing about 3,192 per recorded
list. Every output is byte-identical, and the median list is about 5 to 6
percent faster. No package version change.

## Bounded return — A Counted Child's Missing Credit Answer Is Asked (2025)

[Plan](milestones/eic-child-answers.md); retrospective:
`docs/milestone-retrospectives/2026-11-20-eic-child-answers.md`.

Core v101 (registry v99, release v99) and ADR 0087 make the saved page ask
a roster member's missing answer and name the member. This covers the
earned income credit, child tax credit, other-dependent child and
relative rosters. Before, 9 to 18 lines blocked with no sentence. No
number changed, and pages on earlier cores are unchanged.

## Bounded return — The Saved Page Writes Its Own Words Plainly (2025)

[Plan](milestones/page-plain-words.md); retrospective:
`docs/milestone-retrospectives/2026-11-23-page-plain-words.md`.

The saved page's own words are plain: status badges (Amount, Zero,
Confirmed none, Determined, No result, Not applicable), blocked banners
whose sentence, heading and remedy are chosen from the block code, plain
citation buttons and support-trace captions, and plain error texts. Ids,
enums, codes and pins sit in collapsed technical details and attributes.
On all 691 rendered recorded lists no engine id or enum is in the text a
filer reads first. Page and tests only; the model is unchanged on all 775
lists.

## Bounded return — A Child Without a Valid SSN Routes the Earned Income Credit (2025)

[Plan](milestones/eic-no-ssn-child.md); retrospective:
`docs/milestone-retrospectives/2026-11-23-eic-no-ssn-child.md`.

Core v102 (registry v100, release v100) counts a qualifying child without a
valid SSN as a qualifying child for the earned income credit's status,
separated-spouse and Step 4 tests, for every filing status, while the
amount column counts only children with a valid SSN (Schedule EIC: such a
filer "can claim the self-only EIC"). A separated married filer whose
children all lack an SSN gets the self-only credit instead of $0. No
recorded number changed.

## Bounded return — Content Guards Run in the Fast Lane

[Plan](milestones/fast-content-guards.md); retrospective:
`docs/milestone-retrospectives/2026-11-23-fast-content-guards.md`.

The content rule-file size guards moved from five live modules into one
fast module with one exception table, so a builder's fast-lane run catches
an oversized rule before CI does (as eic-no-ssn-child's first verify did
not). The observer manifest test no longer fails when FORCE_COLOR and
NO_COLOR are set. Tests only.

## Bounded return — The Sale Page Observer Reads Question Groups

[Plan](milestones/sale-observer-question-groups.md); retrospective:
`docs/milestone-retrospectives/2026-11-23-sale-observer-question-groups.md`.

The real-Chrome sale page observer expects each blocked reason as the
saved page renders it (question-group link, member label, statement label,
or sentence), so the opt-in ten-case fixture passes again. Tools and tests
only.

## Bounded return — The Separated-Spouse Question Is Asked Only of a Married Filer (2025)

[Plan](milestones/eic-separated-married.md); retrospective:
`docs/milestone-retrospectives/2026-11-24-eic-separated-married.md`.

Core v103 (registry v101, release v101) asks a head of household with a
qualifying child whether they were a married taxpayer at the end of 2025
(Step 3 question 3, with the year's marital rules in the question), and
asks the separated-spouse questions only after a "yes". An unmarried head
of household is no longer stopped at $0 by the separated-spouse question.
No recorded number changed.

## Bounded return — The Age Fact's Title (2025, closed on P0)

[Plan](milestones/eic-age-title.md); retrospective:
`docs/milestone-retrospectives/2026-11-24-eic-age-title.md`.

The `eic.age-25-under-65` title omits age at death, but no filer or auditor
surface shows it, and the question a filer sees already states age at
death. Kept parked with a safe route recorded. No package change.

## Bounded return — A Refused Head of Household Status Does Not Set the Worksheet Ceilings (2025)

[Plan](milestones/hoh-no-worksheet-ceilings.md); retrospective:
`docs/milestone-retrospectives/2026-11-24-hoh-no-worksheet-ceilings.md`.

Core v104 (registry v102, release v102) blocks Qualified Dividends and
Capital Gain Tax Worksheet lines 6 and 13 when a claimed head of household
or qualifying surviving spouse status is refused or unanswered, instead of
showing that status's ceiling. No amount changed.

## Saved-page observation — Mortgage and Sales (2025)

[Plan](milestones/sale-page-observation.md); retrospective:
`docs/milestone-retrospectives/2026-11-06-sale-page-observation.md`.

Ten synthetic mortgage and sale pages were observed on published core v89
through the actual coordinator, saved citation-walk renderer and Chrome.
The v79/v80 captures are historical. The v89 carry exposes repeated wrong-basis
questions (6–39 times per page), box 7 questions on the sale pages, and no
row-local reason on the stale-answer Schedule D line 9. The observation item
is retired. Specific rendering and question findings remain parked. The
ten-case fixture is opt-in because a post-launch CI stall remains unexplained.
The separate short owned temp-root regression remains in the live suite.

## Saved-page questions — Blocked Sale Pages (2025)

[Plan](milestones/blocked-sale-pages.md) and [retrospective](../../milestone-retrospectives/2026-11-22-blocked-sale-pages.md).
New saved pages group declared prompts by answer target in
presentation-model.v3. Blocked rows retain their scope, answer status, and
independent reasons. The stale Schedule D line 9 row names its basis question
alongside the amount-check explanation. Existing v1 and v2 pages remain
readable.

## Parked work and open questions

This is the single list of parked work and open owner-held questions for the
engine line (it moved here when `docs/phase-state.md` was retired). A
milestone that parks something adds it here in its closing commit; one that
delivers an item removes it.

### Open owner-held questions

- The 2025-to-2026 capital loss carryover: no box publishes it, by
  ADR-0058 and ADR-0060 Decision 7. Computing it needs a superseding ADR;
  saying on line 21 that the excess carries forward waits on the same
  question (cf-loss-limit).
- Rust kernel port (rust-kernel-experiment, parked 2026-11-18): the
  slice is the kernel replay fold (`findings.project` and the `facts.py`
  lattice) behind a PyO3 binding; the first design question is the
  per-assertion schema-validation callback into Python. Before it: a
  governance check on implementation language and the kernel boundary
  (owner or advisor) and the owner's confirmation of the
  `packages/kernel/` edit. It pays only if the kernel comes to dominate
  replays or the owner wants the language evidence regardless.
- Whether a representation-transfer adjudication act should exist, so a
  nonzero legacy claim on a superseded entity could resolve honestly
  (ADR-0072). Until then, the withdrawal policy blocks it.
- Later-year basis reuse: cross-year identity and correction for an
  acquisition reported in a later year.
- Form 8949 code L for a box 7 loss: whether to add a recording-surface
  change that records the disallowed sale in a code L family, with the
  amount computed from proceeds, basis and any recorded wash or code B
  adjustment (f8949-code-l P0). A content successor cannot emit the row.

### Parked

- Chrome cleanup, remaining gaps (chrome-cleanup-hang, 2026-11-19):
  `run.mjs` still skips its server close when `dispose()` fails and has
  no exit backstop. A Ctrl-C in its short window before launch returns
  leaves Chrome running. A SIGKILLed observer cannot kill a Chrome
  group, which Decision 2 accepts. Group cleanup was checked with real
  Chrome only on macOS; Linux is covered by CI alone.
- Replay speed, next levers (rust-kernel-experiment and member-reads-once,
  2026-11-18): recorder stories re-project the whole act log on every
  save and rebuild the fact lattice metadata per assertion (about 60 % of
  test K13; a kernel edit that needs the owner's confirmation). The
  checksum reuse is done (validation-checksum-reuse); its one note is that
  a supplied digest, or one cached for a parse later mutated through the
  view's private body, is trusted for the body it is handed with.
- Form 8949 adjustment codes other than B and W (refused by answer on
  core v81).
- Per-row Form 8949 column (f) code letters: B on a box B/E row with a
  wrong reported basis, and BW on combined rows. Today the code shows only
  in the part label.
- Making ADR-0061 Path B optional for box C/F-only returns changes when
  that answer is required, which is the owner's call. (Since core v89 the
  unanswered Path B is asked rather than blocking with no question.)
- A sale entered both on a Form 1099-B family and as a no-1099-B sale is
  refused only by the in-class answer ("entered only once"); the two are
  keyed differently, so content cannot see it.
- Per-member questions that tell the filer to answer no where the fact is
  narrower than the instructions (a sheltered workshop's gross income, a
  multiple support agreement) compute a smaller credit instead of
  blocking (eic-child-answers ECA-R3). Two members with the same recorded
  label share one reason (ECA-R7). A question's yes/no polarity is
  recorded only in evidence and tests, not in published content (ECA-R9).
- The earned income credit "not claimable as a dependent" answer could be
  derived from the line 12a "someone can claim you" answer (Publication
  596 Rule 12), but a rule cannot prefer an explicit answer and fall back
  to another; the filer is asked both.
- The `eic.age-25-under-65` fact's title states only the birth-date range;
  the question also counts age at death in 2025 (EAQ-R7). No surface shows
  the title today; if one does, a bundle successor that keeps fact type
  version v1 keeps saved answers (eic-age-title, closed on P0).
- The covered-flag refusal code sits in `missing` as
  `BASIS_NOT_REPORTED_ON_COVERED`; a derivation-record successor would put
  it on the row.
- A blocked code W gain (box 1g on a gain or break-even row) asks the
  filer no question; the page shows only the reason (gain-break-even).
- Additional seller-paid shipping under platform pass-through.
- A v1 Form 1099-K workspace re-answers its completeness question under the
  successor package; recovery for a log with two current family versions; a
  full pre-save fold for every act kind.
- Schedule A8a display/itemization: the special mortgage explanation shows
  the amount and a complete-scope itemizer's attachment publishes, but the
  observed v79 page has no ordinary line-8a row or Schedule A subtotal.
  V80 reobservation shows the complete Schedule A subtotal of 20,000; do not
  carry that subtotal absence forward as a v80 defect. Establish the intended
  ordinary-row display before choosing a production repair.
- Multiple Form 1098 support, interest allocation above the debt limit,
  second-home extension, mixed-use amounts, refinancing and the mortgage credit.
- When a Schedule 1 Part I absence answer is also missing, line 10 names the
  absence first and the Form 1099-K only once it is answered.
- Form 1099-K box 4 on line 25b (SC-R1); routing the 1098, 1099-K and nominee
  recorders through the package overlay first (ADR-0082 production
  condition 2).
- Package companion declarations in package content (the W-2G guard is a
  presence pair naming an unregistered witness, removed by v65's declaration;
  a successor that omits its declaration refuses every W-2G log); an
  in-product route for the Social Security handover.
- Gambling outside the Form W-2G class: winnings not on a W-2G and business
  gambling (refused by answer); wagering expenses for 2025. The Form W-2G
  and the Schedule A instructions are not in the local sources.
- Form 8332 and decree releases, more than one other claimant and unsettled
  equal-AGI ties (outside the class by answer); asking the tie-breaker only of
  a child some credit can count, which needs derived per-subject results as
  conditional members; Worksheet B, Form 8862, combat pay, the Medicaid waiver
  exclusion and Worksheet 1.
- `explain()` re-expands shared inputs at each use: the line 27a walk is 9,885
  tree nodes over 218 findings.
- Disabled-over-limit relatives and multiple support agreements for the
  credit for other dependents; lines 29-31 refundable credits, Schedule 2
  Part II taxes and the estimated tax penalty, each declared absent.
- No presentation line names the tie-breaker step that decided a child.
- A rule still names only its first cause when it blocks. The page hides
  a blocked line's own text when it shows questions.
- The runner stores every block code outside `RECORD_CODES` as
  `DEPENDENCY_INVALID` (line 12e's `ITEMIZED_TOTAL_WITH_GAMBLING_LOSSES`,
  `LOOKUP_MISS`, `FAMILY_VALIDATION_BLOCKED`), so the
  page can only say a rule could not use the saved information; keeping
  the specific code on the row is a derivation change (page-plain-words
  Decision 9).
- Three sale blocked reasons are not plain: "The holding period does
  not match this short-term or long-term family.", the wash-sale reason
  naming `floor_zero(basis - proceeds)` and its block code, and the
  covered-W "code W on a gain" reason. They are the `meaning` text on
  sale source-family checks, which saved sale records pin by version and
  which a run copies into a published value, so a content successor
  breaks every sale workspace (sale-reasons-plain, closed on P0). The
  route that keeps every number is a projection change with a schema
  home for the page sentence (an ADR for the owner), after
  blocked-sale-pages. Drafts: `sale-reasons-plain-evidence/wording.json`.
- Undrawn rule descriptions and notes still carry engine terms; plain
  wording covers only text a page draws (plain-line-texts).
- Two answers the record proves are still asked: line 2a Form 1099-INT
  tax-exempt interest (a closed box 8 above 0) and the other-dependent answer
  (a marked roster row). Deriving them needs the proof's family closed, so a
  return that answered with that family open would newly block; it needs an
  absent-tolerant read (an engine change), which would also restore the
  Form 1098 and other-dependent contradiction blocks v74 gives up. A
  recording surface must also not turn a "yes" to a group question into a
  value for every member.
- A derived answer is not named: the page does not say which question the
  record answered or which finding proved it (a schema).
- Worksheet lines as presentation rows; `demo.*` ids on the correct
  capital-loss and Social Security amounts.
- Blindness for someone who died in 2025: neither the Form 1040
  instructions nor Publication 501 says how it is judged, and the
  blindness questions state December 31, 2025 on every return.
- Line 12d draws each box as two sections, one always "Not applicable."
  (the line 6d pattern), and since core v92 line 6c does too. Showing one
  section per box, with its own words for a spouse box the return does
  not show, is a page-design decision for the owner.
- Every citation button on the saved page shows `id@version`; the page
  takes a readable label only from a source fact's evidence label. A
  label for a field citation is a projection or page change.
- The saved page draws a blocked field's question but has no answer
  control, and the entry loop accepts W-2 entries only; questions are
  display-only until a question-entry milestone (line6b-reason Decision
  8).
- The page-alerts alert census reads form sections only, and the
  recorded-replay pin does not hold field explain or categorical render
  text; neither can show that a sentence stayed put.
- Exact question identification from saved outcomes, process-restart recovery,
  and broader internal-error guidance remain separate questions. Do not infer
  a missing answer from a derived symbol or treat them as delivered here.
- A v70-matched usability evidence pack and scorecard, if selected. The v70
  launcher is a technical exercise, and the accepted v6 scorecard is unchanged.
- Four source sets reach an attachment without a guard of their own; each
  is held by a guarded rule downstream, confirmed live on core v66. Listed in
  `tests/test_collect_closure_regression.py`.
- A blocked line names the kind of statement short of its withholding
  answer, not the statement itself (keyed join).
- The core-v75 closure-question and core-v76 later-arm switches are keyed
  by package id and version in `packages/tax/loader.py`, which the runner
  imports; passing them into the run, or declaring them in package content,
  is a later cleanup.
- Four internal subtotals block with no filer question: Form 1099-INT box 8
  tax-exempt interest, the Schedule B nominee subtotal, and the
  other-dependent child and relative counts. None holds a line a filer sees.
- A general assumption framework, free-text intake and institutional
  verification.
- Thirty-one selection rules on core v86 still carry an inert second path
  on a fact type nothing writes. Each can move to `rule-artifact.v16` with
  one path when it is next succeeded (selection-keyed-collect survey).
- The engine cannot see the same Form 1099-B box 4 dollars entered both
  per statement and in the core v85 return-level total; the questions tell
  the filer not to, and nothing refuses it. A recording surface for a
  statement with no sale would replace the return-level total.
- Form 1099-B box 13 bartering (f1099b-bartering, core v97): the
  Schedule 1 lines 2a-6 questions now tell the filer to answer yes for a
  box 13 amount, which refuses the return. Still open: box 13 cannot be
  recorded; workspaces answered before v97 are not asked again; after a
  yes the page shows only the generic line 10 sentence; the Schedule 1
  scope facts record absence while the question asks "did you…?", and
  nothing converts a yes.
- A loss on a Form 1099-B statement whose box 7 is checked refuses
  Schedule D line 16 (core v84). The code L row is an open owner-held
  question (f8949-code-l, closed on P0).
- On a box 7 loss the filer sees the line 16 explanation, a disjunction of
  every cause that can block the line, and the generic remedy. A reason
  naming only the loss needs a value rule to carry a selection reason or a
  check to carry a subject; both are derivation changes.
- The per-statement box 4 amount and box 7 questions do not name the
  statement.
- When the failing Exception 1 answers on a required-Schedule-D return
  with no sale are right, the page names the criteria but gives no
  explicit next step (record the sale or unsupported work) and does not
  show the current answer (line16-names L16-R2; page guidance).
- Recorded lists produce only one of the six optional model blocks
  (`line21Explanation`); the mortgage, Form 1099-K and provenance
  blocks are reached only by synthetic cases, so a full-surface replay
  cannot vouch for them on recorded returns (full-surface-replay
  FSR-R1). Pin order in report rows and the explanation block is not
  compared.
- An amount entered after a per-statement Form 1099-B box 4 "no"
  leaves the earlier zero payment findings current until a run; the
  engine's currency on additions (box4-no-prompt Decision 8).
- The blocked-names-question and preferential-base-reason evidence probes
  count a sentence as a question only if it has a question mark, so an
  imperative prompt is missed. Replace the filter before reusing them.
- The unasked boundary answers (lines 18-19, QOF). Since core v89 Path B
  and "no Form 8949" are asked.
- Kernel reverse presence check: removing a sale checks only one of its
  amount rows (`packages/kernel/findings.py`), so a leftover row is
  refused by the run, not at entry. Nothing publishes.

## Why line 7a comes before Schedule D

The 2025 Form 1040 instructions permit eligible capital-gain distributions to
be reported directly on line 7a with Schedule D marked not required. A
box-2a-only milestone that nevertheless manufactures Schedule D would encode
the wrong dependency shape and would violate the project's
dependency-form-completeness discipline. Schedule D follows only when its own
source and completeness boundary is selected.

## Status

- **Capital-Gain Distributions and Form 1040 Line 7a — closed 2026-07-31.**
  The bounded direct-reporting class is synthetic complete on `main` after PR
  #128. Plan:
  `milestones/capital-gain-distributions-line7a.md`.
- **Schedule K-1 Box-5 Interest Breadth — closed 2026-07-31** (PR #133). The bounded
  Form-1065 box-5 path is synthetic complete through line 2b, Schedule B,
  downstream results, package resolution, explanation, and presentation.
  Plan: `milestones/k1-interest-breadth.md`.
- **Payer-Reported Current-Inclusion Market-Discount Interest — closed
  2026-08-01.** The bounded box-10/box-5 payer-reported class is synthetic
  complete through line 2b, Schedule B, package resolution, explanation, and
  one canonical positive presentation golden; disposition, basis,
  taxpayer-side accrual, subtractive adjustments, and broader securities
  history remain outside it. Plan:
  `milestones/market-discount-interest.md`.
- **Covered Long-Term Gains, Schedule D Line 8a — closed 2026-08-02**
  (independently reviewed `READY`). The bounded covered, long-term,
  gain-only, no-adjustment Form 1099-B class is synthetic complete through
  Schedule D (line 8a/13/15/16), Form 1040 line 7a/9, the Schedule
  D-bound QDCG line-16 path, package resolution, explanation, and
  presentation, including honest visibility for blocked/not-required
  attachment states (ADR-0056). Plan:
  `milestones/schedule-d-covered-ltcg-8a.md`.
- **Current-Year Capital Losses and Schedule D Line 21 — closed
  2026-08-03** (Track 1 with one findings-only repair, Track 2, both
  independently reviewed `READY`). The bounded covered, basis-reported,
  short-term-or-long-term, gain-or-loss Form 1099-B class is synthetic
  complete through signed Schedule D lines 1a/7/8a/15/16, the §1211
  current-year loss cap (line 21), Form 1040 line 7a/9, the Schedule
  D-bound QDCG line-16 path at any sign of Schedule D's result, package
  resolution, explanation, and presentation, including honest visibility
  for the new `SOURCE_SET_UNCLOSED` and `COMPLETENESS_VALUE_VIOLATION`
  states. Plan: `milestones/schedule-d-current-year-losses.md`.
- **Schedule B Interest Adjustments — closed 2026-08-03.** The bounded three-
  class adjustment path is synthetic complete through line 2b, Schedule B Part
  I, package resolution, explanation, and presentation. Schedule D remains
  outside scope. Plan: `milestones/schedule-b-interest-adjustments.md`.
- **Inbound Capital-Loss Carryovers into 2025 Schedule D — closed 2026-08-04**
  (Track 1 with one findings-only repair, Track 2, both independently
  reviewed `READY`). A bounded five-fact 2024 prior-return authority
  (ADR-0059) with a two-path completeness gate — a cheap declared-absence
  path preserving the existing `no-inbound-capital-loss-carryovers`
  declaration, and a full-authority path running the Capital Loss
  Carryover Worksheet as an auditable derived rule citizen (ADR-0060) —
  makes the short-term/long-term carryover synthetic complete through
  signed Schedule D lines 6/7/14/15/16/21, Form 1040 line 7a/9, package
  resolution, explanation, and presentation, including a carryover-only
  routing case and disposition-visibility parity for the missing-
  authority state. Rebased onto the merged Schedule B interest-
  adjustments milestone; the resulting package-version collision
  (`package.core-calculations` `v15` claimed independently by both) was
  resolved as an additive `v16`/`v11` union, and a latent hardcoded-
  package-version restriction in `packages/derivation/package_validation.py`
  (introduced by the Schedule B build) was generalized so it no longer
  blocks any package version past `v15`. Plan:
  `milestones/schedule-d-inbound-loss-carryovers.md`.
- **Form 1099-DIV Box 12 to Form 1040 Line 2a — closed 2026-08-04.** The
  bounded box-12-only class is synthetic complete through line 2a, explicit
  completeness and box-13 companion authority, reported-only explanation and
  presentation, package/release/adoption resolution, and focused regressions
  for existing dividend, interest, Schedule B, and Schedule D behavior. The
  independent re-review returned `READY`. Other tax-exempt sources and
  excluded downstream consumers remain honestly outside the claim. Plan:
  `milestones/form1099div-box12-line2a.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md`.
- **Covered Form 1099-B Wash-Sale Adjustments through Form 8949 and
  Schedule D Lines 1b/8b — closed 2026-08-05** (Track 1 across three
  repair/re-review rounds, Track 2, both independently reviewed `READY`).
  A covered, basis-reported Form 1099-B transaction routed to Form 8949
  solely by a broker-reported box-1g wash-sale loss (code W) is synthetic
  complete through Form 8949 columns (a)-(h), per-transaction validation
  guards, successor Schedule D lines 1b/7/8b/15/16/21, Form 1040 line 7a/9,
  package resolution, explanation, and presentation. ADR-0061 was amended
  pre-merge after review found the originally-proposed transaction-identity
  mechanism unsafe given a real `source-family.v1` schema constraint;
  resolved with a separate wash-sale fact type and an identity-key
  collision kill-test, wired into the live run path. Rebased onto the
  merged Form 1099-DIV Box 12 milestone; a second package/schema version
  collision (independently-minted `v17`/`v12` and colliding schema
  successors) was caught before either PR merged and resolved as an
  additive union (`v18`/`v13`, `quantity-vocabulary.v7`,
  `artifact-package.v15`). Every other Form 8949 adjustment code,
  noncovered securities, and taxpayer-side wash-sale determination remain
  honestly outside the claim. Plan:
  `milestones/schedule-d-form8949-covered-wash-sale.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-05-schedule-d-form8949-covered-wash-sale.md`.
- **Form 1099-INT Box 8 Tax-Exempt Interest to Form 1040 Line 2a — closed
  2026-08-05.** The bounded box-8 succession of the closed box-12 line-2a
  route is synthetic complete through Path A/B completeness, live-path box-9
  companion, reported-only explanation and presentation, and packaging
  v18/v13/v11/adopt-v18. Independent review returned `READY` with no findings.
  Plan: `milestones/form1099int-box8-line2a.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-05-form1099int-box8-line2a.md`.
- **Fact-type succession with neutral Schedule 1 vocabulary — closed
  on this branch (PR #177).** No new tax route. Thirteen Schedule 1
  absence facts succeed onto Schedule-1-native ids (ADR-0063). Empty-route
  SSA contract unchanged except the nonempty CDS retarget. Form 1098-E
  remains unselected. Plan:
  `milestones/fact-type-succession-neutral-schedule1.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-14-fact-type-succession-neutral-schedule1.md`.
- **Declarative Structured Validation and Consumer Dependency Substrate —
  closed 2026-08-17** (PR #174). No new tax route; hardening prerequisite.
  Plan: `milestones/declarative-validation-substrate.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md`.
- **2025 Form 1098-E Student-Loan Interest through Schedule 1 Lines 21/26
  and AGI — closed 2026-08-18.** First Engine Breadth route on the
  income-adjustment side of the return. The bounded single-statement,
  fully-eligible class is synthetic complete through Schedule 1 lines
  21/26, Form 1040 line 10, and AGI. Rebased and rebuilt onto the closed
  declarative-validation-substrate-f8949 base; final package core
  **v33**/published **v28**/release **v26**/adopt **v33**. Independent
  review of the curated PR (#178) returned `CHANGES REQUESTED` on two
  curation-introduced defects; both fixed, gate re-verified green. Plan:
  `milestones/f1098e-student-loan-interest-agi.md`; deferral ledger:
  `milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md`.
- Subtractive adjustments and other market-discount situations remain
  separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
- Subtractive adjustments and other market-discount situations remain
  separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
- **The W-2 Entry Loop Follows Its Adopted Core — closed 2026-11-01 on this
  milestone branch** (independent semantic review `READY`; exact-head `verify`
  remains pending for publication). The runtime resolves only the exact v6
  and v70 profiles from the workspace adoption. V70 first entry and correction
  agree with a fresh coordinator run; legacy v6 behavior remains intact.
  The v70 exercise does not establish usability or support for future cores.
  Plan: `milestones/entry-loop-rescope.md`; retrospective:
  `docs/milestone-retrospectives/2026-11-01-entry-loop-rescope.md`.
