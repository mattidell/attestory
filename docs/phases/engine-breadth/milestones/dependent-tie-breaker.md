<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "dependent-tie-breaker",
  "status": "Track 0 built (proposed ADR-0081). Track 1 builds the tie-breaker on core v58.",
  "scope": [
    "compute who may treat a child as a qualifying child when another person also could, for the 2025 earned income credit, child tax credit and credit for other dependents, as successor content",
    "replace the yes-blocks 'another person may also claim' answers with answers about the other person whose meaning matches the rule that reads them",
    "decide which of the divorced or separated parent rules (Form 8332 release) are computed and which stay outside the class by answer",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no computation of the other person's return; the filer answers about the other person, and the engine does not record the other person's documents",
    "no head-of-household or dependent care rules beyond what the three credits read",
    "no change to the qualifying-relative tests beyond what the tie-breaker reads",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-25-other-dependents-credit.md",
      "docs/phases/engine-breadth/milestones/dependent-tie-breaker.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/dependent-tie-breaker.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/dependent-tie-breaker.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-25-other-dependents-credit.md",
      "docs/phases/engine-breadth/milestones/dependent-tie-breaker.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# A Child More Than One Person Could Claim (2025)

Milestone key: dependent-tie-breaker.
Branch: milestone/dependent-tie-breaker-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-27.
Starting point: `origin/main` at `a0bc250a` (PR #216 merged; core v57,
registry v55, release v55 are the latest).

## What we are trying to accomplish

On core v57 a child who also lives with, or is related to, someone else is
refused for all three child credits. The earned income credit and the child
tax credit each ask "another person may also claim this child … under the
tie-breaker rules", and `yes` blocks. The same follow-up is listed in the
EIC, child tax credit and credit for other dependents retrospectives.

That answer is also imprecise. It mixes two different statements: that
another person *could* treat the child as a qualifying child (meets the
relationship, age, residency and joint-return tests for them), and that the
other person *wins* under the tie-breaker. A filer who reads it the second
way answers `no` and is counted; a filer who reads it the first way is
blocked. A child living with a parent and a grandparent is the ordinary case,
not an edge.

The useful outcome: a filer whose child could also be claimed by someone else
learns, from answers about that other person they can actually give, whether
they may count the child for each credit; the explanation names the
tie-breaker step that decided it; and a situation outside the class is
refused, never given the credit or $0 silently.

## What we know

- **Engine (core v57).** The EIC child roster (`tax.us.2025.eic.child-roster`)
  and the child tax credit roster (`tax.us.2025.ctc.child-roster`, same child
  kind) each have a per-child other-claimant answer
  (`tax.us.2025.rule.eic-child.other-claimant-clear`,
  `tax.us.2025.rule.ctc-child.other-claimant-clear`); `yes` blocks. The
  credit for other dependents roster and the relatives family were added on
  core v56; how they handle another claimant is for P0 to read.
- **Law.** Publication 596 (2025) states the tie-breaker rules and examples
  (`temp/tax-on-taxable-income/sources/p596-2025.txt`, about lines 815-1070,
  and the divorced or separated parents rule near line 1005). The Form 1040
  instructions and Schedule 8812 instructions are beside it.
- **The rules in brief (to be verified by P0 with citations).** If the other
  person could claim the child but does not, there is no tie; but a
  non-parent may then claim only if their AGI is higher than the AGI of any
  parent who could claim. If both could claim and both would: a parent over a
  non-parent; between parents, the one the child lived with longer, then the
  higher AGI; between non-parents, the higher AGI. A custodial parent may
  release the child tax credit and credit for other dependents (not the EIC)
  to a noncustodial parent with Form 8332.
- **What we do not know.** Which facts about the other person a filer can
  reliably answer (the other person's AGI is the hard one; "higher than mine"
  may be answerable when the amount is not); whether one set of per-child
  answers can serve all three credits without changing meaning, given that
  the EIC and child tax credit tests differ (the EIC residency test needs the
  United States; the child tax credit adds age under 17); whether "lived with
  you longer" and "the other person will claim" are per-child answers or
  per-other-person; how the two existing other-claimant answers are succeeded
  so a v57 answer set keeps its result; and whether the Form 8332 release
  can be computed or stays outside the class.

## Actions the team will take

1. **P0 — verify and design.** The law with citations; classify each
   tie-breaker step; draft each question and say who answers it, when it is
   asked and what each answer means to the rule that reads it; trace the
   design on the real coordinator for the three credits; decide the Form 8332
   boundary; hand-compute cases. No content changes.
2. **Decide.** The model, questions, successors and versions.
3. **Track 1 — the tie-breaker.** Per-child answers, the successor rules for
   the three credits, the successor package and cases.
4. **Track 2 — presentation.**
5. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, frontier and parked list.

## Cases that will shape the design

- A child living with a parent (the filer) and a grandparent all year; the
  parent claims (parent wins); the parent does not claim and the grandparent's
  AGI is higher, and lower, than the parent's.
- Two unmarried parents living together with the child all year: higher AGI
  wins; the filer has the lower AGI (the child does not count for the filer
  for any of the three credits).
- Two parents living apart, the child with the filer for more nights; equal
  nights.
- A divorced custodial parent who released the claim with Form 8332: the
  noncustodial parent's child tax credit, and neither parent's EIC transfer.
- A return answering `no` to the old other-claimant answers keeps its result
  on the successor package; a return answering none of the new questions,
  where they are read, blocks with the facts named.
- Each credit separately: a child counted for the child tax credit but not
  the EIC (residency outside the United States), so the tie-breaker is asked
  on the path where it can change the result and nowhere else.

## P0 result

P0 and its repair are in
[verify and design](dependent-tie-breaker-evidence/p0-verify-and-design.md),
with the resolution-table generator, the probe and the case script beside it.

- **Law.** All five child benefits travel together to the tie-breaker winner;
  Form 8332 moves only the child tax credit and the credit for other
  dependents. A non-parent needs AGI strictly higher than any parent who can
  claim; the sources are silent on equal AGI between two parents with equal
  nights, or between two non-parents.
- **The engine cannot ask a child's answer only when another of that child's
  answers makes it decide.** A per-subject rule binds only `requires`, so
  every tie-breaker question would be required on every contested child.
  Family gating avoids that only with eight rosters whose membership encodes
  the whole tie-breaker, so the filer must work out the answer to place the
  child. The repair stopped there, as chartered.
- **Owner decision (2026-10-27): change the engine.** Track 0 lets a
  per-subject rule use `conditional_dependency_set` on its own subject's
  answers (proposed ADR-0081, extending ADR-0037).
- Outside the class by answer: Form 8332, more than one other person who
  could claim the child, and the equal-AGI ties the law does not settle.

## Contract

1. **One tie-breaker result per child.** A per-subject rule over the child
   kind publishes whether the filer may treat the child as a qualifying child
   (wins, loses, or blocks as outside the class). The EIC, child tax credit
   and credit for other dependents counts each read it in place of the
   other-claimant answer. All three credits follow it together (the five
   benefits are not divided); each credit's own tests still apply.
2. **Questions, yes/no, asked in this order, each only where it can decide**
   (ADR-0081). "You" includes your spouse on a joint return; "the other
   person" never means that spouse. "Parent" means a birth or adoptive
   parent, not a stepparent or foster parent who has not adopted the child.
   1. *Another person could also claim this child:* the child also meets the
      conditions to be that person's qualifying child for 2025 (lived with
      them more than half the year, related to them as the instructions list,
      younger than them, and meets the age test for them). `no` decides: the
      filer wins. Asked of every child the filer claims for any of the three
      credits.
   2. *More than one other person could also claim this child.* `yes` is
      outside the class.
   3. *You are this child's parent;* 4. *the other person is this child's
      parent.*
   5. Both parents only: *the release of the claim to this child for 2025 was
      made with Form 8332 or a decree or agreement.* `yes` is outside the
      class.
   6. Both parents only: *the child lived with you more nights in 2025 than
      with the other parent;* if `no`, *the same number of nights.*
   7. Where AGI decides (the filer is not a parent and the other person is;
      both parents with the same nights; neither is a parent): *your 2025
      AGI is higher than the other person's;* if `no` and the law does not
      settle a tie, *your AGI is the same as theirs* (`yes` is outside the
      class).
   8. Only where the filer would otherwise lose: *the other person will
      claim this child on their 2025 return* for any of the five benefits.
      `no` lets the filer win, except that a non-parent filer against a parent
      still needs the higher AGI. A filer who does not know answers `yes`.
3. **Resolution.** Parent over non-parent; between parents, more nights,
   then higher AGI; between non-parents, higher AGI; a parent who could
   claim but does not leaves the child to a non-parent only with AGI higher
   than the parent's. Every combination of answers resolves through exactly
   one step, shown by a generated table over these questions.
4. **A child the filer loses** counts for none of the three credits. The EIC
   then follows Pub. 596's rule that the filer may take the credit without a
   qualifying child; the return-level "no qualifying child" answer must not
   block that filer, and its successor wording must be true for them.
5. **Succession.** The old other-claimant answer's published title says
   `yes` blocks, so it cannot become the root of the new questions without
   changing its meaning, and the engine has no operator to fall back from an
   absent new answer to the old one (Track 1 stop, 2026-10-27). A v57 answer
   set on v58 is therefore asked the one root question, *another person
   could also claim this child*, for each child, and blocks naming it until
   answered; with `no` on every child it then keeps every v57 result. The
   regression test runs the v57 answer set on v58, asserts the block names
   only that question, adds `no` per child and asserts the published lines
   equal v57's. Earlier packages keep their results unchanged.
6. **Successor content only:** core v58, registry v56, release v56; earlier
   packages and goldens byte-identical.
7. **Required exactly where read,** with an omitted-answer test on each
   branch, asserting on the published lines; the full lane and `mypy`
   before ready.

## Tracks

- **Track 0:** per-subject conditional dependencies (engine, ADR-0081).
- **Track 1:** the tie-breaker questions and successor rules for the three
  credits, core v58.
- **Track 2:** saved presentations.
