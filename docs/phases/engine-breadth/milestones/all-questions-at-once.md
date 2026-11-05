<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "all-questions-at-once",
  "status": "Open. P0: measure how often answering a blocked line's questions only reveals another question, and why.",
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
    ]
  }
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
