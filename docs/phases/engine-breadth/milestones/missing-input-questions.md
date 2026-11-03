<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "missing-input-questions",
  "status": "Open. P0 surveys which lines block on a missing input on core v71, what the person is shown, and whether a plain question for each already exists.",
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
      "docs/phases/engine-breadth/milestones/missing-input-questions.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
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
Charters live under `docs/reviews/missing-input-questions/` until closeout
distills them here. Run commands in the foreground. Stop means stop.
