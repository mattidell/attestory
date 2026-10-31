<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "credit-line-explanations",
  "status": "Closed. On core v64 Form 1040 lines 19 and 28, Schedule 8812 lines 4, 14, 17 and 20 and Credit Limit Worksheet A line 5 explain their own lines; a check fails on a copied explanation. No value changes.",
  "scope": [
    "every form field in the latest core package explains its own line: Form 1040 lines 19 and 28, Schedule 8812 lines 4, 14, 17 and 20, and Credit Limit Worksheet A line 5 stop reading as the earned income credit",
    "a check that fails if a form field's disposition text names another line or credit",
    "keep every computed value, earlier package and saved presentation unchanged"
  ],
  "non_goals": [
    "no change to any rule, value or disposition code",
    "no presentation of the tie-breaker step (parked separately)",
    "no edit to any published schema, adopted package or form-field version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/credit-line-explanations.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/credit-line-explanations.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/credit-line-explanations.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-31-credit-line-explanations.md",
      "docs/phases/engine-breadth/milestones/credit-line-explanations.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-credit-line-explanations.md"
}
-->

# Each Credit Line Explains Itself (2025)

Milestone key: credit-line-explanations.
Branch: milestone/credit-line-explanations-2025, stacked on
`milestone/attachment-closure-2025` (`55431cb6`, PR #235), so the successor
package is core v64, registry v62, release v62.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The parked list records that lines 19 and 28's form-field explanations "read
as the earned income credit (copied from line 27a on core v55)". A reader of
a saved return who opens line 19, the child tax credit, is told "Form 1040
line 27a: the earned income credit from Worksheet A line 6", and a blocked
line 28 says "Earned income credit is blocked". The explanation is the
product; a wrong one on a correct number misleads exactly where the engine
claims to be auditable.

A foreman read of core v63 finds seven form fields that carry line 27a's five
disposition texts unchanged: Form 1040 lines 19 and 28; Schedule 8812 lines
4, 14, 17 and 20; and Credit Limit Worksheet A line 5.

The useful outcome: each of them explains its own line, and a check keeps a
copied explanation from coming back.

## Actions the team will take

1. **Track 1 — correct.** (a) A script lists every form field in core v63
   whose disposition text names a different line, form or credit than its
   own label and description; confirm the seven and report any others. Stop
   if more than eight need correcting. (b) Write a successor for each with
   its own disposition texts, in the style of correct neighbours (line 27a
   for the credit lines; other Schedule 8812 fields). (c) Core v64 / registry
   v62 / release v62 with `tools/package_successor.py`, the v64 companion
   entry. (d) Tests: each successor's texts name its own line; v63 keeps the
   old texts (pinned); a saved presentation on v64 shows the new text for
   lines 19 and 28; every computed value identical on v63 and v64; the
   copy-check as a regression test.
2. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

There is no P0: the defect and its fix are read directly from content.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Stop means stop.

## Review dispositions

Fresh-reader review of Track 1: no required findings.

1. *Lines 19 and 14 described only the child tax credit* (recommended). Both
   include the credit for other dependents (line 8 is lines 5 and 7), and
   line 14's text omitted its gates and zero floor. Fixed in the unmerged v2
   successors, and line 14's label now names both credits; registry v62 and
   release v62 regenerated (core v64 pins only ids and versions, so its
   bytes did not change).
2. *The copy-check missed a whole-text copy that names no line*
   (recommended). Fixed: identical texts across fields with different lines
   are flagged, outside a commented list of generic phrases; a planted copy
   proves it.
3. *Line 28's Part II-B condition was incomplete* (note). Fixed: it also
   needs line 20 below line 17.
4. *Generic texts elsewhere explain nothing* (note). Parked.

## Execution record

- One Sonnet 5.5 builder (Track 1 and its repair) and one Sonnet 5.5
  reviewer. The builder's first survey rule flagged 52 fields and was
  narrowed to the seven; the review showed the narrowed rule could miss a
  copy, which the repair closed.

## Outcome

On core v64, Form 1040 lines 19 and 28, Schedule 8812 lines 4, 14, 17 and 20
and Credit Limit Worksheet A line 5 explain their own lines in every
disposition. Every computed value is unchanged. Seven form-field successors;
no rule, value, code or schema change. A regression check fails if a form
field's text names another line or repeats another line's text.
