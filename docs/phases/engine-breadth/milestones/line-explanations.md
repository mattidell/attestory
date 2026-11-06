<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "line-explanations",
  "status": "Open. P0 done: 36 of 73 fields on core v77 show a generic text. Track 1 succeeds them on core v78 under the wording standard in Decisions.",
  "scope": [
    "on a successor core, every form line a filer sees says in its own words what it adds, why it is zero, or why it shows no value",
    "a blocked line's own text says what kind of input it waits for; the questions it already shows stay as they are",
    "values, dispositions and blocked reasons are unchanged; only text differs, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no change to any value, disposition, guard, rule or question",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no naming of more than a rule's first cause (a separate parked item)",
    "no recording surface or entry-loop change",
    "no edit to packages/kernel/ (another milestone owns it)",
    "no edit to any published schema, adopted package or field version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-11-05-statement-withholding-pairing.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/line-explanations.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line-explanations.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/line-explanations.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/line-explanations.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Every Line Says What It Adds (2025)

Milestone key: line-explanations.
Branch: milestone/line-explanations-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-05.
Starting point: `github/main` at `2a460670` (PR #259 merged; core v77 is the
latest).

## What we are trying to accomplish

Each form line carries a short text per outcome: a published value, a
computed zero, a closure-backed zero, a block, or a guard that does not
apply. Some lines say what they are. Others say only "blocked", "guard
false", "closure zero" or "published total income". Form 1040 line 9 is one
of them, and it appears on every return. A filer reading "guard false" learns
nothing. The useful outcome is that every line a filer sees says, in plain
words, what it adds, why it is zero, or why it shows no value.

## What we know

- **The shape.** `form-field.v2` has `dispositions` with `render` and
  `explain` per outcome. Form 1040 line 25b v3 is a worded example: its
  published text names the five forms it adds and the rounding.
- **Generic texts** (roadmap parked list): Form 1040 lines 9 and 12e-16 and
  several Schedule D lines say only "blocked". Arithmetic lines carry the
  closed-empty and worksheet-guard boilerplate.
- **Blocked lines already name their questions.** Since core v73 a blocked
  line shows every filer-answerable missing input, so a block's own text
  supplements the questions and does not replace them.
- **What we do not know.** How many current fields are generic, and on which
  forms; where a filer actually reads each text (the page, the explanation
  walk, or both); whether any golden, test or validator pins the current
  texts; whether a static text can say why a guard does not apply when the
  rule has more than one guard.

## Actions the team will take

1. **P0: inventory and draft.** List every form-field member of core v77
   with its five texts. Classify each text as specific or generic. Run a few
   synthetic returns through `live_coordinate_run` and the page, and show
   where each text appears. Draft a plain text for each generic one from the
   line's own instruction words and the rule it binds. Count the fields,
   goldens and tests a successor touches. Stop and report if the
   change needs a schema or engine change.
2. **Decide.** Which fields change, and the wording standard.
3. **Track 1: successors.** Form-field successors, then core v78 and its
   registry and release with `tools/package_successor.py`. Cases go through
   the real coordinator and the page. v77 and earlier stay pinned. Full
   suite.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- A wages-only return: lines 9, 11 and 12e-16 publish values; what each says.
- A return with an unanswered input: what a blocked line 9 says beside its
  questions.
- A return where a line's guard does not apply (for example, Schedule D on a
  return with no capital transactions): what it says.
- A closed-empty family: what a closure-backed zero says.
- A return that publishes everything on v77: every value and disposition is
  identical on v78.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction). P0 and
Track 1 are builder units; the close is a fresh-reader review. Each unit
commits on this branch as it goes. Stop means stop.

## P0 result

Recorded in
`docs/phases/engine-breadth/milestones/line-explanations-evidence/p0-inventory-and-draft.md`.
Core v77 has 73 form fields and 365 disposition texts: 239 specific and 126
generic (37 distinct sentences). 36 fields have a generic text the page can
show. A new field version plus package v78, registry v76, and release v76 is
enough to change the words. A scratch run of three successors kept every value
and disposition on the wages return and changed only those sentences. No
schema, engine, or projection change. The blocked sentence stays hidden when
questions exist, which is a page behavior.

## Decisions

Foreman, 2026-11-05, on P0 (text only, inside the plan's scope):

1. **Which fields.** The 36 fields with a generic text the page can show.
   The three whose only generic text is a guard the rule never selects stay
   on v77's version.
2. **Which texts.** In each successor, only the generic texts the page can
   select change. Specific texts, and texts the rule never selects, keep
   their v77 bytes.
3. **The wording standard.** P0's drafts are the starting list, not the
   copy: "is zero because the calculation comes to zero" is generic too.
   Each new sentence:
   - **published:** says what the line is and what it adds or subtracts,
     naming the lines or amounts the rule actually reads (line 9: "Your
     total income: lines 1z, 2b, 3b, 4b, 5b, 6b, 7 and 8 added together",
     using the rule's real addends);
   - **computed zero:** says which amounts are zero, from the rule's
     inputs, and not "the calculation comes to zero";
   - **closure-backed zero:** names the record that is complete and empty
     ("You said you have no ..., so this line is zero");
   - **blocked:** names the kind of input the line waits for;
   - **guard:** names the condition that does not hold; with several,
     names them joined by "or";
   - is true for every return that selects it, checked against the bound
     rule;
   - has no internal ids, no nested parentheses, and none of "derived
     finding", "closure", "honest", "guard" or "route"; at most two short
     sentences; "you" where natural.
4. **Core v78**, registry v76, release v76, through
   `tools/package_successor.py`, and a loader entry sharing v77's companion
   declaration. Values and dispositions are identical to v77 on every case.
5. **Out of scope, parked:** the page hides a blocked line's own text when
   it shows questions, and refuses a numeric line with no citation (the
   Schedule 1 top entry). Both are page behaviors in
   `citation-walk.v1.html`.

## Track 1 result

Recorded in
`docs/phases/engine-breadth/milestones/line-explanations-evidence/track1.md`.
31 of the 36 fields have a new version on core v78, registry v76, and
release v76. 74 explain texts changed. Five stay on the v77 pin because
the bound rule cannot select their generic texts: Form 1098 unresolved,
Form 1099-K unresolved, Form 1040 lines 3a and 3b, and Schedule D line 8a.

The wages return, the unanswered qualified-business-income answer, and the
line 13a guard match v77 on every section value and disposition. The new
sentences show on line 9, Schedule D lines 1a and 7, and line 13a.
`tests/test_line_explanation_wording.py` rejects a selectable v77 generic
sentence, a replaced explain of more than two sentences, and the pattern
"not say that you have no". `tests/test_line_explanations.py` runs the cases.

The repair after review rewrote 14 explains on the same field versions.
Registry v76 and release v76 were regenerated with `tools/package_successor.py`.
The package pin did not change. Values and dispositions on the repair cases
match v77, and each required finding's new sentence shows in its section.

mypy on the two wording tests: Success, no issues in 2 source files.
Fast lane: 1651 passed, 8 skipped, 3975 subtests passed in 17.43s.
The case file: 10 passed in 49.09s. The earlier full suite, 4316 passed,
24 skipped, 8165 subtests passed in 1300.76s (0:21:40), was not re-run.
These are local runs. The `verify` check on the pull request is the gate
of record.

## Review dispositions

Review: `line-explanations-evidence/review.md`.

1. *A rounded zero is described as amounts that add to zero* (required).
   Fixed. Line 1a, Schedule 1 line 7, and Schedule 1 line 8b say the box 1
   amounts round to zero. A box 1 of 0.40 shows each sentence at value 0.
2. *Line 1a, blocked, names the rounding rule* (required). Fixed. The
   sentence waits for a Form W-2 box 1 amount or confirmation that the wage
   record is complete. An open wage record shows it.
3. *Line 16, blocked, omits covered sale proceeds* (required). Fixed. The
   sentence waits for taxable income, filing status, qualified dividends
   and capital gain, or covered sale proceeds. The open-proceeds return
   shows it.
4. *Schedule D line 16, blocked, names line 15 as unavailable* (required).
   Fixed. It waits for line 7 or line 15. The same return shows it, with
   line 15 already a computed zero.
5. *Line 13a guard inverts the question* (required). Fixed. The sentence
   says the line is computed only when the filer has no qualified business
   income, and that they have not answered or said they have some.
6. *Line 13b guard has the same inversion* (required). Fixed, in the same
   shape, for tips, overtime, and new-car-loan interest. The recorded no
   shows it.
7. *Line 22 guard drops Form 4972* (required). Fixed. The sentence names
   Form 4972 tax on line 16 and additional tax from Schedule 2.
8. *Schedule 3 line 8 guard uses the inverted double negative* (required).
   Fixed. The sentence says the line is computed only when the filer has
   no other nonrefundable credit on lines 2 through 6.
9. *Schedule 3 line 1 guard states reasons that are false on the return*
   (required). Fixed. Two sentences: the return is not one where the
   credit can be claimed without Form 1116, and the questions on that page
   say which condition is not met. Foreign tax of 601 with the election
   set to yes shows it.
10. *Line 16 guard is not two short sentences* (recommended). Fixed. The
    second sentence says Schedule D is required, or qualified dividends or
    capital gain is below zero, or the capital gain distributions answer
    does not match.
11. *Line 9 and Schedule D line 7 name lines that are already filled*
    (recommended). Fixed. Each waits for whichever of its lines is still
    open. The open-proceeds return shows both.
12. *The wording test would accept the required findings* (recommended).
    Fixed. A replaced explain fails when it has more than two sentences or
    contains "not say that you have no". The live cases lock the nine
    required sentences.
