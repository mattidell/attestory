<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1099b-bartering",
  "status": "Closed 2026-11-19. Core v97, registry v95, release v95.",
  "retrospective": "docs/milestone-retrospectives/2026-11-19-f1099b-bartering.md",
  "scope": [
    "a filer whose Form 1099-B shows a bartering amount in box 13 is never given a return that silently leaves that income out: the engine either asks and refuses honestly (outside the supported class) or computes it, by an answer the filer can see",
    "every recorded return keeps its numbers unless P0 shows a recorded return was silently wrong"
  ],
  "non_goals": [
    "no Schedule C, business income or self-employment tax computation",
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no other Form 1099-B box"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/f1099b-bartering.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f1099b-bartering.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f1099b-bartering.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f1099b-bartering.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Form 1099-B Bartering Amount Is Not Lost (2025)

Milestone key: f1099b-bartering.
Branch: milestone/f1099b-bartering-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `54b312f8` (core v96, registry v94, release v94).
Expected target: core v97, registry v95, release v95 if a content
change is needed; tests only if P0 finds the engine already refuses.

## What we are trying to accomplish

Form 1099-B box 13 reports the fair market value of bartering. It is
not a sale on Schedule D; it is income reported elsewhere (Schedule C or
Schedule 1 under the 2025 instructions). The sale-family audit (N2)
recorded that which answer refuses a bartering amount "is not
established". If the engine accepts a statement with a box 13 amount
and computes a return without it, the filer gets a return that is
silently short. The useful outcome is that a box 13 amount is either
asked about and refused honestly by a named answer, or carried
correctly, never dropped.

## Stages

1. **P0.** Trace what happens today to a Form 1099-B with a box 13
   amount: can it be recorded, which answers or questions touch it,
   and what the return shows. Read the 2025 Form 1099-B and Form 1040 /
   Schedule 1 / Schedule C instructions in the local sources for where
   bartering goes. Check accepted ADRs and rule notes for a bound.
   Name the smallest honest design (most likely a refusing input
   question or answer, as other out-of-class sources use) and prototype
   it as a scratch successor with the full-surface replay
   (`tools/recorded_replay.py full`).
2. **Track 1.** Publish it (or pin tests if already honest).
3. **Fresh review**, repair, closeout.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/f1099b-bartering-evidence/p0.md`
(probe, scratch build, census and replay beside it).

On core v96 no fact type carries a Form 1099-B box 13 amount, and no
question names bartering. The answers that refuse it exist and every
complete return gives them: Schedule 1 line 10 v3 requires
`no-sch1-line3-business` and `no-sch1-other-income-except-w2g` to be "yes".
A box-13-only return answered as the questions are worded is identical to a
return with no Form 1099-B (Form 1040 line 9 50,000, refund 625, whatever box
13 says): the bartering income is silently left out. Answered "yes" (Pub. 525:
bartering is generally Schedule C income), line 10 is guard_inapplicable and
lines 8 through 37 block, with a generic sentence that does not name
bartering. Box 13 is ordinary income (Schedule C line 1, Schedule 1 line 3, or
line 8z); computing it needs Schedule C and SE, a non-goal. No accepted ADR
bounds bartering; the bound is line 10's Part I absence authority.

Recommended design (variant q): five input-question successors (Schedule 1
lines 2a-6, one shared sentence) that add "Also answer yes if a Form 1099-B
you received shows an amount above zero in box 13 (Bartering), even if you do
not think of it as a business." No fact, rule, field or requirement changes.
Variant qf also replaces the line 10 form field so its guard sentence names
the causes, bartering among them. Both scratch v97 builds validate.

Replay of the 775 recorded lists, v96 against scratch v97: q 775 pass, 0
unexpected (691 differ only in the package version, 84 fail identically on
both cores); qf 775 pass, 0 unexpected (plus the line 10 sentence and field
version on all 691). No recorded list carries a box 13 or bartering fact, and
all answer the Schedule 1 questions "yes", so the question change is unused
on the corpus and is exercised by the nine probe lists (9 of 9 pass on both
variants). No engine, schema, projection, page or kernel change is needed.

Decisions for the foreman: (1) q or qf; (2) five successors or only the line
3 question; (3) accept that a non-business barter is refused through the
business fact, or also name it in the lines 8a-8z question; (4) "above
zero" as the box 13 test; (5) Track 1 pins the nine probe lists live.

## Decisions

1. **Variant q (2026-11-19, foreman, on P0's recommendation).** Today a
   box 13 amount cannot be recorded, no question names bartering, and a
   filer who answers the Schedule 1 questions as worded gets a return
   identical to one with no Form 1099-B: the income is silently left
   out. Core v97 publishes five input-question successors (the Schedule
   1 lines 2a to 6 questions, which share one sentence and so must stay
   identical) adding: "Also answer yes if a Form 1099-B you received
   shows an amount above zero in box 13 (Bartering), even if you do not
   think of it as a business." A yes refuses the return through the
   existing line 10 path, honestly. No fact, rule, form field or
   required answer changes. Variant qf (also rewording the line 10
   field) is not taken: its first clause is unverified.
2. **Route and test.** Bartering is refused through the business-income
   answer, which is where Publication 525 generally sends it; the line
   8z question is not changed, so the page does not misstate where
   bartering goes. "Above zero" is the box 13 test.
3. **Track 1** publishes the five successors in core v97 (registry v95,
   release v95), pins P0's nine probe returns as live tests (including
   the unanswered case showing the new sentence, and the yes case
   refusing), and runs the full-surface replay of the 775 recorded
   lists with the changes declared. The review must check that the
   added sentence is true and sensible in each of the five questions'
   places on the page.
4. **Review notes (2026-11-19, foreman).** The fresh review
   (`docs/reviews/f1099b-bartering/review.md`) is READY with notes.
   - BART-R2 (accepted and stated): the new sentence reaches a filer
     only while the Schedule 1 lines 2a to 6 answer is open. A workspace
     that answered the old question before v97 is not asked again and
     can still compute without a bartering amount. Box 13 cannot be
     recorded, so no census can show that no return is affected; P0's
     "no recorded return was silently wrong" means only that no
     recorded list carries a bartering fact. Re-asking answered
     workspaces needs answer staleness across versions, which this
     milestone does not add. Parked.
   - BART-R3 (parked): after a yes, the page shows only the generic line
     10 sentence and does not say the return stopped because of
     bartering or business income.
   - BART-R5 (repaired): the live test now requires the page to draw the
     shared sentence exactly once, with the bartering clause.
   - BART-R6 (parked, predates this milestone): these scope facts record
     absence while the question asks "did you…?", so a filer's yes is
     stored as "no" by convention; nothing in the engine converts it,
     and a yes to any of the four sibling questions records barter
     under that question's income class. Both refuse the return.
   - BART-R4: the parked list is updated at closeout.

## Closeout

Closed 2026-11-19. A Form 1099-B box 13 bartering amount can no longer
be silently left out of a new return: the five Schedule 1 lines 2a to 6
questions (core v97) tell the filer to answer yes for a box 13 amount
above zero, and a yes refuses the return through the existing line 10
path. Box 13 itself still cannot be recorded, workspaces answered
before v97 are not asked again, and the page does not name bartering as
the reason a return stopped; all three are parked. The full-surface
replay of the 775 recorded lists changed only the package version.

