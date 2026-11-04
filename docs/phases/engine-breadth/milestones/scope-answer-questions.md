<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "scope-answer-questions",
  "status": "Open. P0 drafts a filer question for each yes/no scope answer and filing status that can block a line on core v72.",
  "scope": [
    "a line blocked because a yes/no scope answer or filing status is missing names the question to answer, through declared input-question citizens, on a successor core",
    "each question is judged by what a filer would answer, and its yes and no mean exactly what the engine records",
    "earlier cores render byte-identically"
  ],
  "non_goals": [
    "no change to what any line computes or when it blocks",
    "no new schema; input-question.v1 and artifact-package.v39 exist",
    "no change to fact-type titles or the recorded answer values",
    "no entry-loop change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-11-03-missing-input-questions.md",
      "docs/phases/engine-breadth/milestones/missing-input-questions.md",
      "docs/phases/engine-breadth/milestones/scope-answer-questions.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/scope-answer-questions.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/scope-answer-questions.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/scope-answer-questions.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Blocked Line Asks Its Yes-or-No Question (2025)

Milestone key: scope-answer-questions.
Branch: milestone/scope-answer-questions-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-03.
Starting point: `github/main` at `9cfae1bb` (PR #252 merged; core v72 is the
latest). PR #250 is open in another worktree and reads v70 reasons only.

## What we are trying to accomplish

Since core v72 a line blocked on one of eight missing amounts names what to
enter. The missing-input survey found 79 more filer-answerable roots that
still show "Missing dependency code(s): DEPENDENCY_ABSENT": 78 categorical
scope answers and one boolean (Form 1098 scope), plus filing status. A
missing line 2a scope answer alone holds 28 lines. Their fact-type titles
are engineering prose ("... is not present for tax year 2025", with a
"yes asserts absent" gloss), so none can be copied.

The useful outcome: the filer sees a plain yes-or-no question for each, and
answering it the obvious way records what the engine means.

## What we know

- `input-question.v1` citizens are keyed by fact type; the projection
  attaches a question for an absent leaf whose `missing` id is that fact
  type. Filing status is missing as the binding symbol `filing_status`, not
  a fact type id, so it may need the projection to resolve the binding.
- By bundle: direct-FTC scope 23 (plus the election), Schedule 1
  adjustments 12, Schedule 1 Part I 9, line 2a 8, SLI 5, EIC 4, Exception 1
  4, CTC 2, Social Security 2, and one each for Form 1098, line 38, lines
  29-31, QBI, Schedule D boundary, Schedule 1-A, Schedule 2 Part II, the
  standard deduction and Form W-2G.
- **The risk is meaning, not code.** Many answers assert an absence ("yes"
  means the item is not present). A question whose natural "yes" records
  the opposite of the filer's intent is worse than the generic text.

## Actions the team will take

1. **P0 — draft and verify.** For each of the 80 facts: its title, the
   values it records and what each value does to the computation (traced in
   content), when it is asked, and a drafted question whose natural answer
   maps to the right value. Group facts that share a pattern. Say how
   filing status reaches a question. No production changes.
2. **Wording review.** The foreman reads every question before the build;
   the owner sees the table.
3. **Track 1 — build.** The citizens; core v73 and its registry and release;
   any projection change for filing status; tests through the real
   coordinator; earlier cores byte-identical.
4. **Close.** Fresh-reader wording review, full lane, exact-head CI,
   retrospective, roadmap.

## Decisions

Owner, 2026-11-03: avoid misleading questions, and avoid questions where
"yes" means something is missing. Each question asks whether the thing is
present ("Did you ...?", "Do you have ...?"), so "yes" always means present.
Where the recorded fact asserts an absence, the evidence table states the
inversion explicitly (a "no" to the question records the absence), so any
surface that records the answer knows to flip it. A fact that cannot be
asked that way is flagged and left without a question.

Owner, 2026-11-03: a person using the application should not face the
low-level questions one by one; questions reduce to computed meaning. For
this milestone:

1. **Group by meaning.** Facts a filer would settle with one answer share
   one filer-level question ("Did you pay foreign tax on any investment
   income in 2025?" for the direct-FTC scope answers). Each fact still gets
   its `input-question` citizen, carrying the group's sentence; the
   projection already shows each distinct sentence once.
2. **Find what is already known.** P0 lists the facts whose answer follows
   from what the return already records (for example, no statement of a
   kind recorded), so no question should be needed. Deriving those answers
   changes recording or computation; it is the candidate next milestone,
   not built here.
3. The per-fact table stays as the audit mapping from each filer question
   to the facts and values it records.

## Process

Dispatch is to Sonnet 5.5 Agent sub-agents. Charters live under
`docs/reviews/scope-answer-questions/` until closeout. Foreground commands
only. Stop means stop.
