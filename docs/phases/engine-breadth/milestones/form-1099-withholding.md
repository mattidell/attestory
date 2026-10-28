<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form-1099-withholding",
  "status": "Closed. On core v59 withholding on Forms 1099-G box 4 and SSA-1099 box 6 reaches line 25b; earlier packages still refuse it (ADR-0082). Form 1099-K stays outside the class.",
  "scope": [
    "count federal income tax withheld on Form 1099-G box 4, Form SSA-1099 box 6 and Form 1099-K box 4 on Form 1040 line 25b, as successor content",
    "retire the hard blocks that refuse a return whose 1099-G box 4 or SSA-1099 box 6 is nonzero",
    "decide what happens to a Form 1099-INT, 1099-DIV or 1099-R recorded without its box 4 answer",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no Form W-2G: its withholding belongs on line 25c and needs gambling income on Schedule 1, which the engine does not read",
    "no Form RRB-1099, Schedule K-1 or other line 25c source, and no line 26 estimated payments",
    "no Form 1099-G box 2, 5-7 or 9 income, and no change to what the unemployment or Social Security routes compute",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-28-form-1099-withholding.md",
      "docs/phases/engine-breadth/milestones/form-1099-withholding.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/form-1099-withholding.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/form-1099-withholding.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-28-form-1099-withholding.md",
      "docs/phases/engine-breadth/milestones/form-1099-withholding.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-28-form-1099-withholding.md"
}
-->

# Federal Tax Withheld on Forms 1099 (2025)

Milestone key: form-1099-withholding.
Branch: milestone/form-1099-withholding-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-27.
Starting point: `origin/main` at `bb9e05e9` (PR #227 merged; core v58,
registry v56, release v56 are the latest).

## What we are trying to accomplish

Line 25b adds the federal tax withheld on Forms 1099-INT, 1099-DIV and
1099-R box 4. Three sources the engine already reads also carry withholding,
and none of it reaches the return:

- **Form 1099-G box 4.** A nonzero amount is a hard block on the
  unemployment route (`tax.us.2025.f1099g.box4-federal-withholding-authority`).
  A filer who had tax withheld from unemployment, the ordinary case, is
  refused.
- **Form SSA-1099 box 6.** The Social Security family's closure claim covers
  only statements with box 6 absent or zero; voluntary withholding puts a
  filer outside the class.
- **Form 1099-K box 4.** Recorded and summed nowhere. The line 25b rule's
  notes record why: a new family declaring the already-published box 4 fact
  as a member predicate would retroactively change every existing use of it
  (SC-R1), and one family may authorize only one subtotal (ADR-0016). The
  line 25b form-field text nevertheless says it includes 1099-K box 4.

The useful outcome: a filer with withholding on any of these documents sees
it on line 25b, and through the refund or amount owed; the explanation walks
from line 25b to each document; and a source the engine still cannot read is
refused, never left out silently.

## What we know

- **Law.** Form 1040 instructions (2025), line 25b
  (`temp/tax-on-taxable-income/sources/i1040gi-2025.txt`, about lines
  2559-2576): Form 1099-R box 4, and any Form 1099 showing withholding on
  dividends, interest, unemployment, Social Security, railroad retirement or
  other income, "shown in box 4 of Form 1099, box 6 of Form SSA-1099, or box
  10 of Form RRB-1099". W-2G withholding is line 25c.
- **Engine (core v58).** `tax.us.2025.rule.form1040-line25b` adds three
  family-closed subtotals (INT, DIV and 1099-R box 4). Each is its own
  family, separate from the document's income family, with its own closure.
- **What we do not know.** Whether 1099-G box 4 and SSA-1099 box 6 need new
  families with their own closure, or can ride on the existing statement
  identity; how the 1099-G authority witness and the Social Security closure
  claim are succeeded so that a v58 answer set with no withholding keeps its
  result; whether the SC-R1 obstacle for 1099-K box 4 still holds after the
  family work since, and what a successor fact would cost a v58 workspace; and
  whether a 1099-INT, 1099-DIV or 1099-R recorded without its box 4 answer
  should be asked for it.

## Actions the team will take

1. **P0 — verify and design.** The law with citations; how each of the six
   sources treats withholding today, read from content; the design for each
   of the three new sources, including succession; the SC-R1 question for
   1099-K box 4 tested, not taken from the note; the missing-box-4 decision;
   a probe on the real coordinator; hand-computed cases. No content changes.
2. **Decide.** The model, successors and versions.
3. **Track 1 — withholding.** The successor families, rules and line 25b,
   the successor package (core v59, registry v57, release v57) and cases.
4. **Track 2 — presentation.** Line 25b and the bottom line in a saved
   presentation, and line 25b's form-field text corrected by successor.
5. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, frontier and parked list.

## Cases that will shape the design

- Unemployment with 10% withheld: line 25b includes it, and the refund or
  amount owed moves by exactly that amount.
- Social Security with voluntary withholding in box 6, alone and with a
  1099-R box 4 amount on the same return.
- A Form 1099-K with backup withholding in box 4.
- A joint return with withholding on two 1099-Gs, one for each spouse.
- A v58 answer set with no withholding on any of these documents keeps its
  result on the successor package; one with nonzero 1099-G box 4 goes from
  refused to computed.
- A 1099-INT recorded without its box 4 answer, under whatever P0 decides.

## P0 result

P0 and its repair are in
[verify and design](form-1099-withholding-evidence/p0-verify-and-design.md),
with the probe and the case script beside it.

- **Law.** Line 25b is Form 1099-R box 4, any Form 1099 box 4 (interest,
  dividends, unemployment, other income), SSA-1099 box 6 and RRB-1099 box
  10. W-2G, Schedule K-1 and the foreign withholding forms are line 25c.
- **Recording refuses the withholding, for every package at once.** A
  1099-G box 1 or SSA-1099 box 5 must carry a same-statement companion whose
  value is absent or zero (`packages/tax/loader.py`,
  `domain_companion_presence_pairs` and `domain_companion_value_domains`).
  The kernel enforces these on every registry, not per package. Relaxing
  them lets a v58 run admit $600 of unemployment withholding that its line
  25b never reads: a $508 refund becomes $92 owed, with no refusal. Recording
  a false zero to get past the check changes what the answer means.
- **Form 1099-K box 4 stays outside the class.** Declaring a family on the
  published box-4 fact still breaks nine tests (SC-R1: statements are
  recorded by plain assertion). Line 25b's form-field text, which names
  1099-K, is corrected. (The final review found that a nonzero box 4 is not
  refused at the bottom line; see "Review dispositions".)
- **A statement recorded without its box-4 answer** stays excluded from its
  subtotal, as today; requiring the answer would change every existing
  answer set.
- **New closure answers.** Each new family is closed by the filer, so a
  v58 answer set is asked "all 1099-G box 4 recorded" and "all SSA-1099 box
  6 recorded" on the successor package.
- **Owner decision (2026-10-27): change the engine.** Track 0 makes the
  companion admission rules belong to the package being run (proposed
  ADR-0082), so v58 and earlier keep refusing nonzero withholding and the
  successor package admits and counts it.

- **Owner decision (2026-10-28): replace the Social Security claim.**
  Track 1 first kept `family.ssa1099-benefits` v1 to hold a v58 answer set
  to two questions, leaving a claim that says box 6 withholding is absent or
  zero on a package that admits it. On v59 the family is v2 without that
  limit; an existing workspace hands its Social Security chain over to v2
  (ADR-0079, `packages/tax/ssa_family_handover.py`) and the filer
  re-confirms that every SSA-1099 is recorded. A v58 answer set is asked
  three things on v59.

## Review dispositions

Tracks 0 and 1 review: sound.

1. *A recorded box-4 amount counts while its family is unclosed* (medium).
   Kept: the 1099-INT, 1099-DIV, 1099-R and W-2 withholding families
   already behave this way, and changing it is a cross-family engine
   question, not this milestone's. Parked.
2. *Line 25b's form-field text* (low): Track 2, as planned; v59 is not
   released without it.
3. *Two published fact titles still describe the absent-or-zero rule*
   (low): both stay true on v59 (those facts still refuse nonzero); kept.
4. *ADR-0082 said the direct `apply_act` recorders already use the overlay*
   (low): corrected.
5. *The v59-log-on-v58 test never adopts v59* (low): Track 2 adds the
   adoption; the reviewer showed such a log refuses on v58.
6. Notes: a 1099-G box-4 amount is not tied to a box-1 statement (correct
   in law); the adoption-before-statements ordering is as ADR-0082 states.

Final review: sound, one gap from this plan's own goal.

1. *A nonzero Form 1099-K box 4 reaches no line while the refund publishes*
   (medium). The repair traced it and stopped as chartered: a Form 1099-K
   the engine cannot resolve, for any reason (nonzero box 4, or unanswered
   circumstance questions), is left out of line 8 and total income, and
   lines 24 through 37 still publish, on v58 as on v59. Only the Schedule 1
   attachment and the 1099-K unresolved entry block. Blocking line 25b on
   box 4 alone would leave the dropped income. Not fixed here; it is the
   next milestone. This plan's goal ("never left out silently") is not met
   for Form 1099-K.
2. *The plan and phase state were stale; missing box 4 tested for 1099-INT
   only* (low): the plan and phase state are corrected at closeout; the
   1099-DIV and 1099-R cases are parked with the 1099-K work.
3. *ADR-0082 said the declaration map ships empty* (low): corrected; it
   names v59's entry and the withholding tests.
4. *Saved explanations name pins by id, and lines 33-37 do not say the
   refund moved because of line 25b* (low): the presentation layer's
   existing style; parked.
5. *The Social Security handover has no in-product route* (low): like the
   other recorders, wiring belongs to the surface line; parked.

## Tracks

- Track 0: package-scoped companion admission (ADR-0082).
- Track 1: 1099-G box 4 and SSA-1099 box 6 families, line 25b, core v59 /
  registry v57 / release v57.
- Track 2: presentation, and line 25b's form-field text by successor.

## Execution record

- P0 and its repair ran on agy Gemini Flash. The first pass designed on top
  of the global admission rule without stopping and its case table was
  corrupted; the repair stopped at the engine-change question.
- The owner stopped the Flash Track 0 build before it committed anything and
  moved dispatch to Sonnet 5.5 sub-agents for Track 0, Track 1, its repair,
  Track 2, both reviews and the final repair.
- Track 1 worked around its two-closure stop condition instead of stopping;
  the repair replaced the Social Security claim (owner decision above).
- The final repair stopped at its hard stop (the 1099-K income gap).

## Outcome

On core v59 federal income tax withheld on Forms 1099-G box 4 and SSA-1099
box 6 reaches line 25b, total payments and the refund or amount owed; core
v58 and earlier still refuse it, and a log recorded with it under v59 is
refused under v58. One engine change, ADR-0082. Form 1099-K is not
in the class, and an unresolved Form 1099-K still leaves the bottom line
publishing without it; that is the next milestone.

