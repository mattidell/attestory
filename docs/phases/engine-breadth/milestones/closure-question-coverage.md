<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "closure-question-coverage",
  "status": "Open. P0: survey every source family left unconfirmed and record whether the line it blocks names its completeness question.",
  "scope": [
    "a line blocked because a statement family's completeness is unconfirmed names that family's completeness question, on a successor core where content must change",
    "the two f1099b.covered-w-* families, which block DEPENDENCY_ABSENT on an unconfirmed closure, are the known cases; P0 finds the rest",
    "earlier cores render byte-identically, and a confirmed family computes exactly as before"
  ],
  "non_goals": [
    "no change to what any line computes once its families are confirmed",
    "no new question wording beyond the family's existing closure question unless one is missing",
    "no keyed join or naming of a single statement",
    "no edit to any published schema, adopted package or rule version; only successors",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-11-03-missing-input-questions.md",
      "docs/milestone-retrospectives/2026-11-03-derived-answers.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/closure-question-coverage.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/closure-question-coverage.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/closure-question-coverage.md"
    ]
  }
}
-->

# Every Unconfirmed Family Asks Its Question (2025)

Milestone key: closure-question-coverage.
Branch: milestone/closure-question-coverage-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-04.
Starting point: `github/main` at `9baed50d` (PR #255 merged; core v74 is the
latest).

## What we are trying to accomplish

Since core v72 a blocked line walks to its root causes. When a root is
`SOURCE_SET_UNCLOSED`, the line names that family's completeness question
("Have you recorded every … ?"). The missing-input survey found two Form
1099-B families (`f1099b.covered-w-st-txn` and `f1099b.covered-w-lt-txn`)
whose unconfirmed closure reaches the line as `DEPENDENCY_ABSENT` instead.
Their question is never shown, and the filer sees only that the line is
blocked. Nobody has checked whether other families have the same defect.
The useful outcome is that every family whose completeness the filer must
confirm says so on the line it holds.

## What we know

- `_closure_question_reasons` in `packages/derivation/presentation_projection.py`
  names a closure question only from a `SOURCE_SET_UNCLOSED` root, and an
  input question only from a `DEPENDENCY_ABSENT` leaf with a declared
  `input-question`.
- The covered wash-sale families came from a separate fact type (the
  2026-08-05 covered wash-sale retrospective); how their closure is read is
  not traced.
- **What we do not know.** Why those two families report the wrong code;
  whether others do; whether the fix is a content successor (a rule or
  closure mapping), a declared question, or a projection change; and how
  many lines each releases a question on.

## Actions the team will take

1. **P0 — survey and design.** On core v74, through `live_coordinate_run`,
   leave each adopted source family unconfirmed in turn on a return that
   otherwise publishes. Record the lines it blocks, their root codes, and
   whether each names the family's question. Trace each failure to its
   cause. Design the smallest successor set; count what changes. No content
   changes. If the fix needs an engine, schema or operation change, stop.
2. **Decide.** The fix and its scope.
3. **Track 1 — fix.** The successors; core v75 and its registry and release
   with `tools/package_successor.py` if content changes; cases through the
   real coordinator; v74 and earlier pinned.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- Each `f1099b.covered-w-*` family unconfirmed, with and without members.
- Every other adopted family unconfirmed in turn.
- A family both unconfirmed and holding a missing scope answer: both
  questions, sorted, as today.
- Every family confirmed: unchanged from v74.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction,
2026-11-04). P0 and Track 1 are builder units; the close is a fresh-reader
review. Each unit commits on this branch as it goes. Stop means stop.

## P0 result

P0 is in [survey and design](closure-question-coverage-evidence/p0-survey-and-design.md),
with the probe and its output beside it. P0 stopped on the engine
condition.

- **51 families surveyed on v74. Three fail.**
  - Both `f1099b.covered-w-*` transaction families fail with and without
    members: 32 blocked lines each, none naming the question.
  - Form 1099-K fails with one member: two Schedule 1 selection lines
    explain the unanswered single-sale question and not the completeness
    question. The other 28 lines name it.
- **Cause, wash sales.** The transaction families carry member
  constraints, so `compile_validation_graph` gives each consumer a
  synthesized `.member-validation` require. That require is checked before
  `require_closed`, and while the family is unadmitted it records
  `DEPENDENCY_ABSENT` naming the family id. The projection names a closure
  question only for `SOURCE_SET_UNCLOSED`.
- **Fix.** No successor rule, mapping or declared question reaches it. The
  smallest fix is an engine change: record `SOURCE_SET_UNCLOSED` for an
  unadmitted family, which the projection already turns into the existing
  question. Form 1099-K's two lines would need a projection change.
- **Wording.** All 51 questions exist. The two wash-sale adjustment
  questions ask about "every covered sale" where their siblings limit to
  sales with an adjustment; listed, not reworded.

## Decisions

Owner, 2026-11-04:

1. **Engine fix, from core v75 only.** While a constrained family is
   unadmitted, its synthesized member validation records
   `SOURCE_SET_UNCLOSED` naming the family, so the existing closure question
   is named. Core v74 and earlier render byte-identically. The per-version
   switch must need no schema change; if it does, stop.
2. **Form 1099-K's two selection lines are included**, through the
   presentation projection, from core v75 only as well: a blocked
   selection line whose root is an unconfirmed family names the
   completeness question beside its selection reason.

Foreman: the two adjustment questions' wording is parked, not changed.

## Tracks

1. **Track 1 — fix.** The version switch, the engine and projection
   changes, core v75 (registry and release) with
   `tools/package_successor.py`, cases through the real coordinator, v74
   and earlier pinned; full suite (substrate).
