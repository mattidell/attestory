<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "all-questions-at-once",
  "status": "Closed. On core v76 the completeness questions a return could already show appear in round one: answering a blocked return takes 2 rounds instead of 4 for open amounts and the mortgage, 3 instead of 4 for Form 1099-B, and 5 instead of 6 for a dependent or foreign tax. Conditional questions still wait for their answer. Earlier cores are unchanged.",
  "scope": [
    "a filer who answers every question a blocked return shows is not then shown a new question that was already knowable, on a successor core where the engine or content must change",
    "measure first: how many answer rounds a return takes today, and which rules hide a later cause behind their first",
    "earlier cores render byte-identically, and a return whose inputs are complete computes exactly as before"
  ],
  "non_goals": [
    "no change to what any line computes once its inputs are present",
    "no new question wording",
    "no recording surface or entry-loop change",
    "no edit to any published schema, adopted package or rule version; only successors",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-11-04-closure-question-coverage.md",
      "docs/milestone-retrospectives/2026-11-03-scope-answer-questions.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/all-questions-at-once.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/all-questions-at-once.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/all-questions-at-once.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-04-all-questions-at-once.md",
      "docs/phases/engine-breadth/milestones/all-questions-at-once.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-11-04-all-questions-at-once.md"
}
-->

# Every Question At Once (2025)

Milestone key: all-questions-at-once.
Branch: milestone/all-questions-at-once-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-04.
Starting point: `github/main` at `86179db1` (PR #256 merged; core v75 is the
latest).

## What we are trying to accomplish

Since core v75 every blocked line names the questions it waits on: missing
amounts, scope answers, filing status and unconfirmed families. But a rule
that blocks records only its first cause. A filer who answers everything
shown can run again and meet a question that was knowable the first time.
Each extra round is an extra trip through the return. The useful outcome is
that one pass of answers is enough wherever the engine could already know
the full set.

## What we know

- The runner records a missing `requires` before it evaluates `when`, and
  an expression that raises on one `ref` does not evaluate the rest.
- `_closure_question_reasons` walks blocked rows to their roots. It sees
  only the causes the rules recorded.
- **What we do not know.** How many rounds a return takes from empty to
  computed; which rules hide a later cause; whether a hidden cause is
  knowable without the earlier answer (a `requires` list is static; a
  `choose` branch may depend on the answer); and whether the fix is
  content (reorder or declare `requires`), the runner (record every missing
  `requires`, not only the first), or the evaluator.

## Actions the team will take

1. **P0 — measure and trace.** On core v75 through `live_coordinate_run`,
   start from representative returns with every filer answer withheld,
   answer exactly the questions shown each round, and count rounds until the
   return computes. Record every question that appears after round one, the
   rule that hid it, and whether it was knowable in round one (it does not
   depend on an earlier answer). Design the smallest change that shows the
   knowable ones in round one; count rounds before and after on a scratch
   prototype. No production changes. If the change needs an engine,
   schema or operation change, stop and report.
2. **Decide.** Owner direction on any engine change.
3. **Track 1 — fix.** Behind a core-version switch if engine behaviour
   changes; cases through the real coordinator; v75 and earlier pinned.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- A return with every scope answer withheld.
- A return with every amount answer withheld and its families open.
- A mortgage, a Form 1099-B, a dependent and a foreign-tax return, each
  from empty.
- A question that truly depends on an earlier answer (asked only when the
  answer is "yes"): still asked only then.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction,
2026-11-04). P0 and Track 1 are builder units; the close is a fresh-reader
review. Each unit commits on this branch as it goes. Stop means stop.

## P0 result

P0 is in [rounds and design](all-questions-at-once-evidence/p0-rounds-and-design.md),
with the probe, the scratch prototype and their outputs beside it. P0
stopped on the evaluator condition.

- **Rounds on v75, from empty.**

  | Return | Rounds |
  | --- | --- |
  | Every scope answer withheld | 2 |
  | Every amount withheld, families open | 4 |
  | Mortgage | 4 |
  | Form 1099-B | 4 |
  | Dependent | 6 |
  | Foreign tax | 6 |

- **Questions after round one: 29.** Twelve were knowable in round one:
  - eight Form 1099-B closures behind a guard: the two parent families and
    the six wash-sale companions;
  - the W-2 wage closure;
  - the W-2 box 2 amount and the Form 1099-DIV box 4 amount, each in a
    later `any` arm;
  - the Form 1099-DIV box 7 closure, behind a static `requires`.

  Seventeen are truly conditional: Form 1098 scope, the overpayment
  applied, the credit gates, the W-2 box 4 and box 6 closures, and the
  foreign-tax answers asked once box 7 is known. They stay.
- **Design, two layers.**
  - *Content:* one closure-check rule per unconditional family, listed in
    its consumer's `requires`. Measured on the amounts return only: 4 → 3
    rounds.
  - *Evaluator:* record a `ref` in a later `any` arm while an earlier
    `count` is blocked, only when a compared set already has a member.
    Both layers together: amounts 4 → 2, mortgage 4 → 2, Form 1099-B 4 → 3,
    dependent 6 → 5. Scope and foreign tax are unchanged.
  - Complete returns published identical values with the patch on.
- **Found on the way.** Four subtotal rules (`f1099int-b8-subtotal`,
  `scheduleb-adjustment.nominee-subtotal`, `odc-child-count`,
  `odc-relative-count`) block with no filer question on any presentation
  line.

## Decisions

Owner, 2026-11-04:

1. **Content and evaluator, from core v76.**
   - Content: closure-check successors for the unconditional families.
   - Evaluator: record a later `any`-arm `ref` while an earlier `count` is
     blocked, only when a compared set already has a member.
   - The evaluator change is behind a core-version switch keyed like
     v75's. Core v75 and earlier render byte-identically.

Foreman:

2. Truly conditional questions stay where they are.
3. The four subtotals that block with no question on a line are parked;
   they hold no line a filer sees.

## Tracks

1. **Track 1 — fix.**
   - The successors, the evaluator change and its switch.
   - Core v76, its registry and release, with
     `tools/package_successor.py`.
   - Round counts through the real coordinator; v75 pinned; full suite.

## Track 1 result

[Track 1](all-questions-at-once-evidence/track1.md). Ten closure-check
witnesses (the two Form 1099-B parents, the six wash-sale families, W-2
wages and Form 1099-DIV box 7) and ten consumer successors; the evaluator
and runner change behind `later_any_arm_refs_while_count_blocked` in
`packages/tax/loader.py`; core v76, registry v74, release v74.

| Start | v75 rounds | v76 rounds |
| --- | --- | --- |
| scope withheld | 2 | 2 |
| amounts open | 4 | 2 |
| mortgage | 4 | 2 |
| Form 1099-B | 4 | 3 |
| dependent | 6 | 5 |
| foreign tax | 6 | 5 |

Foreign tax beats the prototype's 6: the successor names the box 7 closure
on the credit rule, so round one asks it. Complete returns publish v75's
amounts, headline and face. No golden moved.

## Review dispositions

Fresh-reader review ([review](all-questions-at-once-evidence/review.md)):
no required findings.

1. *The Form 1099-DIV box 4 amount is checked only in round one*
   (recommended). Fixed: the test now asserts it is never asked on the five
   starts with no Form 1099-DIV, and asked from round 2 until the loop stops
   on the foreign-tax start.
2. Notes: the switch is on for any core rank of 76 or more (`v100`
   included) and off for every other package and pin; registry v74 is
   add-only; a return with no W-2 is never asked box 2.

## Execution record

- Grok CLI agents in this worktree (owner direction): P0 builder, Track 1
  builder (220 turns, $7.04, full suite 4,252 passed with one Chrome-harness
  failure that passed alone), fresh reviewer (55 turns, $5.05). The foreman
  added the review's box 4 assertions.

## Outcome

On core v76 a filer who answers a blocked return's questions is no longer
then shown a completeness question the return could already have asked. The
W-2 wage, Form 1099-B and wash-sale, and Form 1099-DIV box 7 questions
appear in round one, and the W-2 box 2 and Form 1099-DIV box 4 amounts
appear as soon as a statement is recorded, never before. Conditional
questions (the Form 1098 answer, the dependent tests, the Form 1116 choice)
still wait for the answer they depend on. Values do not change; core v75
and earlier render byte-identically.

Parked: four internal subtotals still block with no filer question (box 8
tax-exempt interest, the Schedule B nominee subtotal and the two
other-dependent counts); none holds a line a filer sees.
