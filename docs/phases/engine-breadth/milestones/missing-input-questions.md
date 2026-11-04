<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "missing-input-questions",
  "status": "Closed. On core v72 a line blocked because one of eight amounts is missing (W-2 box 2; box 4 on Forms 1099-INT, 1099-DIV, 1099-R and 1099-G; SSA-1099 box 6; lines 26 and 36) names what to enter and that $0 is an answer; a line with a missing amount and an unconfirmed family names both. Earlier cores render byte-identically.",
  "scope": [
    "a line blocked because a filer-supplied input is missing names, in plain words, what to answer, as a line held by an unconfirmed family names its closure question since core v69",
    "a line with mixed causes (missing input and unconfirmed family) names each instead of falling back to the generic text",
    "earlier cores, saved presentations and their goldens render exactly as before"
  ],
  "non_goals": [
    "no change to what any line computes or when it blocks",
    "no naming of an individual statement where the engine knows only a fact (that needs a keyed join, parked)",
    "no reasons for derived failures that a filer cannot answer (invalid values, engine faults); those keep the generic text",
    "no entry-loop change; PR #250 owns the entry loop",
    "no edit to any published schema, package or citizen; only successors, and a new schema version only with the plan's decision recorded"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-10-31-closure-questions.md",
      "docs/milestone-retrospectives/2026-11-02-statement-withholding-answer.md",
      "docs/phases/engine-breadth/milestones/missing-input-questions.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/closure-questions.md",
      "docs/phases/engine-breadth/milestones/missing-input-questions.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/missing-input-questions.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-03-missing-input-questions.md",
      "docs/phases/engine-breadth/milestones/missing-input-questions.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-11-03-missing-input-questions.md"
}
-->

# A Blocked Line Names What Is Missing (2025)

Milestone key: missing-input-questions.
Branch: milestone/missing-input-questions-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-03.
Starting point: `github/main` at `ca32e877` (PR #251 merged; core v71 is the
latest). PR #250 (W-2 correction guidance) is open in another worktree and
reads blocked-line reasons in the entry loop on core v70; this milestone does
not change v70's rendering.

## What we are trying to accomplish

Since core v69 a line held only by unconfirmed families names their closure
questions. Every other blocked line still says only "Form 1040 line 25b is
blocked because an input it needs is missing or not yet closed." The roadmap
parks it twice: generic form-field texts explain nothing, and "a blocked text
never names the missing input". PR #251 made line 25b block until each Form
1099 carries its box 4 answer, and the person is not told to enter it, or
that $0 is an answer.

The useful outcome: when a line waits on something the filer can supply, the
page says what to supply, in the filer's words, and a line with two causes
names both.

## What we know

- `_closure_question_reasons` (`packages/derivation/presentation_projection.py`)
  walks a blocked row's `missing` symbols through blocked rows to roots coded
  `SOURCE_SET_UNCLOSED` and copies each family's declared `closure_question`
  verbatim. It attaches nothing unless every root is such a closure root,
  because a reason hides the generic text.
- A missing source fact roots as `DEPENDENCY_ABSENT` with the fact id in
  `missing` and no blocked row behind it (line 25a's W-2 box 2, line 25b's
  box 4 on v71).
- **What we do not know.** Which `DEPENDENCY_ABSENT` roots on current-core
  returns are filer-answerable facts and which are derived; whether each
  answerable fact already has a declared plain question or label somewhere
  (fact-type, ordinary-question or recorder content) that can be copied
  verbatim rather than composed; how many lines and roots that is; and
  whether the declaration needs a content successor, a schema successor, or
  neither.

## Actions the team will take

1. **P0 — survey and design.** Run the current-core returns
   (`tests/helpers/current_core_returns.py` and the statement-withholding
   builders) with each answerable input withheld; catalogue every blocked
   line's root causes and what the page shows. Find any existing declared
   question for each missing fact. Design the smallest change that names it
   verbatim, including the mixed case, and say what earlier cores render.
   No production or content changes.
2. **Decide.** Where the question is declared, the class covered, and the
   wording review.
3. **Track 1 — build.** As decided; earlier cores byte-identical.
4. **Close.** Fresh-reader review (wording judged by what a filer would
   answer), full lane, exact-head CI, retrospective, roadmap.

## Cases that will shape the design

- Line 25b on v71 with one Form 1099-R missing box 4: names the box 4 answer
  and that $0 counts.
- Line 25a with a W-2 missing box 2.
- A line held by both a missing input and an unconfirmed family.
- A derived failure (an invalid value) keeps the generic text.
- A v70 and a v69 return render byte for byte as today.

## Process

Dispatch is to Sonnet 5.5 Agent sub-agents (owner direction, 2026-10-30).
Run commands in the foreground. Stop means stop.

## P0 result

P0 is in [survey and design](missing-input-questions-evidence/p0-survey-and-design.md),
with the probe and its output beside it. P0 stopped as chartered: the design
needs schema and admission changes beyond the presentation projection.

- **Catalogue.** 760 runs on core v71, each withholding one input: 230
  blocked a line; 72 distinct lines, 139 distinct roots. 44 roots are
  unconfirmed families, named since v69 when alone on a line. 88 are
  filer-answerable facts: 79 yes/no scope answers, 8 amounts (W-2 box 2;
  box 4 on Forms 1099-INT, 1099-DIV, 1099-R and 1099-G; SSA-1099 box 6; the
  line 26 and line 36 amounts) and filing status. The rest are application
  or derived causes.
- **What the page shows.** A blocked line without a reason shows the
  field's generic sentence, "Missing dependency code(s): DEPENDENCY_ABSENT"
  and "Remedy: contribute the missing dependency". The missing fact is never
  named.
- **No usable wording exists.** The only declared question is a family's
  closure question ("Have you recorded every ...?"), which never says $0 is
  an answer; fact-type titles are engineering prose.
- **One cause per rule.** A rule reports its first cause; a mixed line is
  downstream of two rules (W-2 box 2 missing and the Form 1099-INT box 4
  family unconfirmed hold lines 25d and 33 through 37 for both).
- **Design.** A new leaf citizen `input-question.v1` (`fact_type`,
  `question`, blank refused), one per fact, listed by `artifact-package.v39`;
  core v72, registry v70, release v70. `_closure_question_reasons`
  generalises: a closure root gives its closure question, an absent leaf the
  input question for its fact type; if every leaf has a sentence the
  distinct sentences attach, sorted, otherwise the generic text stays.
  Earlier packages carry no input question, so v71 and earlier render
  byte-identically.

## Decisions

Owner, 2026-11-03: approve the design for the eight amounts (two new
schemas and the same admission points the closure-question schema needed).

Foreman, 2026-11-03:

1. **The class is the eight amounts.** The 79 scope answers and filing
   status are parked; their sentences would all be new wording.
2. **The wording.** Each says what to enter and that $0 is an answer. The
   check knows the fact, not the statement, so each names every statement of
   its kind:
   - W-2 box 2: "Enter the federal income tax withheld in box 2 of each
     Form W-2 you or your spouse received for 2025. If box 2 is blank, enter
     $0."
   - Form 1099-INT, 1099-DIV, 1099-R, 1099-G box 4 (one each, form named):
     "Enter the federal income tax withheld in box 4 of each Form 1099-INT
     you or your spouse received for 2025. If box 4 is blank, enter $0."
   - SSA-1099 box 6: "Enter the voluntary federal income tax withheld in
     box 6 of each Form SSA-1099 you or your spouse received for 2025. If
     box 6 is blank, enter $0."
   - Line 26: "Enter the estimated tax payments you made for 2025, plus
     any 2024 overpayment you applied to 2025. If there were none, enter $0."
   - Line 36: "Enter how much of your 2025 overpayment you want applied to
     your 2026 estimated tax. If none, enter $0."
3. **Mixed reasons sort as strings**, as closure questions do today.
4. **Parked:** the two `f1099b.covered-w-*` families report an unconfirmed
   closure as `DEPENDENCY_ABSENT` and are never named; per-statement and
   per-child causes (`DEPENDENCY_INVALID`) keep the generic text downstream.
5. **Schema intent** for `input-question.v1` and `artifact-package.v39` is
   appended to the schema ledger before the schema edit.

## Tracks

1. **Track 1 — build.** Schema-ledger events; `input-question.v1` and
   `artifact-package.v39`; admission; eight citizens; the generalised
   projection; core v72, registry v70, release v70 with
   `tools/package_successor.py`; cases E1 to E11 of the P0 design; v68 to v71
   presentations byte-identical.

## Review dispositions

Fresh-reader review of P0 and Track 1: READY, no required findings. Earlier
cores v68 to v71 render byte-identically (including the v70 closure reasons
PR #250 reads); each exact-version list was extended, not loosened; a v38
package with an input question and an input question for a fact type outside
the package are refused; the schema manifest only adds.

1. *Line 36's sentence assumes an overpayment* (recommended). Kept: line 36
   asks for the amount only when line 34 is more than 0 (a conditional
   dependency in `rule.form1040-line36`), so a filer who owes never sees it.
2. *A named reason can hide a second cause* (recommended). With W-2 box 2
   and the line 36 amount both missing, lines 35a and 37 name only box 2,
   because a rule reports its first cause. The same holds for closure
   questions since v69. Kept; noted in the retrospective. The second
   question appears once the first is answered.
3. *"You or your spouse" shows to a single filer* (note). Kept, as in the
   closure questions.
4. *No sentence names where to enter the answer* (note). The entry surface
   owns placement.

## Execution record

- One Sonnet 5.5 builder for P0 (about 28 minutes, 64 tool calls; stopped
  as chartered on the schema change) and Track 1 (about 31 minutes, 51 tool
  calls, full suite included); one fresh Sonnet reviewer (about 11 minutes,
  24 tool calls).
- The owner approved the two schemas and the class of eight on P0's
  evidence.
- The foreman's first Track 1 charter commit was refused by the envelope
  gate (an absolute path); fixed before the build began.

## Outcome

On core v72 a line blocked because one of eight amounts is missing names
what to enter: W-2 box 2; box 4 on Forms 1099-INT, 1099-DIV, 1099-R and
1099-G; SSA-1099 box 6; the line 26 estimated payments; and the line 36
amount applied to 2026. Each sentence says that a blank box is $0. A line
held by both a missing amount and an unconfirmed family names both, sorted.
A line with any cause that has no declared sentence keeps the generic text,
because a reason hides it. Declared as content: `input-question.v1`, eight
citizens, `artifact-package.v39`, core v72, registry v70, release v70; the
presentation projection generalises the closure-question walk. v71 and
earlier render exactly as before. The 79 yes/no scope answers and filing
status still show the generic text.
