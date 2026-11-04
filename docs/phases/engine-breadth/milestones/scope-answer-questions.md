<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "scope-answer-questions",
  "status": "Open. P0 drafted 39 filer questions for 80 facts; Track 1 builds them on core v73.",
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

## P0 result

P0 is in [questions](scope-answer-questions-evidence/p0-questions.md), with
its probes, a scratch v73 build and the filing-status prototype beside it.

- **All 80 facts still block on v72**, across 1,674 blocked lines in the
  one-fact-withheld returns.
- **39 filer questions settle the 80 facts**: 38 yes/no and the
  filing-status choice. Every question asks about presence. Most facts
  assert an absence, so the table records the inversion: "yes" to the
  question records the fact's `no`, "no" records its `yes`.
- **On a scratch v73** every held line carried exactly its expected
  sentences, and v72 rendered byte-identically.
- **Filing status** is missing as the binding symbol `filing_status`. The
  package's `input_bindings` map it to the fact type; reaching the question
  needs that map passed from `live.py` into the projection (about five
  lines, presentation only).
- **Answers the return already implies**: Form 1098 scope (true exactly
  when no Form 1098 is recorded), line 2a Form 1099-INT tax-exempt (the
  closed box 8 family), the other-dependent answer (the rosters), and in
  part Form 1116 required (the $300/$600 threshold) and the Form 1099-OID
  and Exception 1 capital-gain facts. Candidate next milestone.

## Decisions (after P0)

Foreman, 2026-11-03:

1. **The 39 questions are accepted as drafted**, with one change: EIC1 adds
   "or marked 'Valid for Work Only With DHS Authorization' and you have that
   authorization", so a filer with authorization does not answer "no".
2. **FTC10's third fact** (`direct-ftc-scope.no-schedule2-regular-tax-add`)
   is traced in Track 1 before its citizen is written; if FTC10 does not
   describe it, it gets its own question in the same style, or none.
3. **A "yes" to a group question is displayed, not recorded.** These
   citizens only name what to answer on a blocked line. A "yes" to an
   absence group (for example S1A) means the return has something the
   engine does not compute; a recording surface must not turn it into a
   value for every member. Per-member follow-ups belong to whichever
   milestone records answers.
4. **The filing-status projection change is in scope.** It is presentation
   plumbing (the package's own binding map) with no schema or computation
   change, and earlier cores carry no citizen, so they render as before.
   Taken under the owner's approval of the input-question design; the owner
   may revert it.
5. **Derived answers are the next milestone**, not built here.

## Tracks

1. **Track 1 — build.** 80 `input-question` citizens (79 facts plus
   filing status) with the P0 table's sentences and decision 1; the
   filing-status projection change; core v73, registry v71, release v71
   with `tools/package_successor.py`; tests through the real coordinator;
   v68 to v72 byte-identical.

## Decisions (after review)

Foreman, 2026-11-03, on the fresh-reader wording review (the citizens are
new on this branch, so they are corrected in place and v73 is regenerated):

1. **FTC10 split.** Track 1 found that FTC10's third fact is the Schedule 2
   Part I addition to regular tax, not line 17, and gave it its own
   question (FTC12): 40 filer questions. Accepted.
2. **S1A (required):** student loan interest is computed and is not one of
   the twelve facts; the sentence ends with "any other adjustment listed on
   Schedule 1 lines 24a through 24z" and says student loan interest is not
   counted.
3. **Ask what a filer can check, not a conclusion.** FTC11 asks about the
   $300/$600 foreign tax threshold and other reasons to file Form 1116; M2
   asks the Form 2210 safe-harbor facts (owing $1,000 or more and paying
   less than 90% of 2025 tax and 100% of 2024 tax, 110% above $150,000 of
   2024 AGI); M3 and M4 ask whether the filer had the income or payments
   (qualified business income, REIT dividends in Form 1099-DIV box 5,
   publicly traded partnership income; qualified tips, overtime, new
   personal vehicle loan interest), not whether they are claiming.
4. **Trace, then say it** (L2A2, L2A3, FTC12, DEP1): the repair confirms
   what each rule reads and words the sentence to it. If the student loan
   fact means "is claimed" rather than "can be claimed", DEP1 splits into
   two questions (the difference is already parked).
5. **M6** lists the common Schedule 1 line 8 items (prizes and awards, jury
   duty pay, an Alaska Permanent Fund dividend, canceled debt) besides
   gambling. **EIC1** is rewritten so the DHS clause attaches clearly and
   the due date includes extensions.
6. **A test reads each fact's polarity** (the `GROUPS` flags) against the
   value the rule treats as supported.

## Process

Dispatch is to Sonnet 5.5 Agent sub-agents. Foreground commands
only. Stop means stop.
