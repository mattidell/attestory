<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "question-wording",
  "status": "Open. P0 measured; Decisions 1-6; Track 0 chartered.",
  "scope": [
    "each question in scope says exactly what its consuming rule reads, for the population it is asked of, per the 2025 instructions",
    "the successors are content only: question citizens, bundles, core v87, registry v85, release v85",
    "every recorded return computes the same numbers on v87 as on v86 when answered truthfully"
  ],
  "non_goals": [
    "no engine, schema, expression-operation or recording-surface change",
    "no new question, rule or line; no change to which returns are asked a question",
    "the refusal with no question after a false Exception 1 no (an engine change; stays parked)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/question-wording.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/question-wording.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/question-wording.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/question-wording.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Questions Say What Their Rules Read (2025)

Milestone key: question-wording.
Branch: milestone/question-wording-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-11.
Starting point: `milestone/selection-keyed-collect-2025` at `7fb81080`
(PR #270, core v86, stacked; ADR 0085 awaits acceptance).

## What we are trying to accomplish

Three parked wording defects let a filer answer a question truthfully and
still give its rule the wrong input:

1. The two Form 1099-B wash-sale adjustment questions ask for an amount
   "of every covered sale", while their basis and proceeds siblings limit
   to sales with an adjustment.
2. The v2 Exception 1 questions still invite "yes" beside a zero-net sale,
   where no rule reads them since line 7b v2.
3. The age questions say "born before January 2, 1961" and handle a death
   in 2025 before age 65 loosely; the student-loan dependent answer says
   "is claimed" and asks the filer only, beside the newer "can be claimed"
   answer.

The useful outcome is a core v87 whose wording, for each question, matches
what the consuming rule reads and the 2025 instructions, with no change to
any published number for a truthful answer.

## What we know

- Each item is listed as wording in the roadmap's parked list.
- **What we do not know.** For each question: its exact current text, the
  rule that reads it and what that rule reads, the instruction it rests
  on, and whether a truthful answer under the current words can differ
  from one under the corrected words for any recorded return. Whether any
  item needs more than a question successor.

## Actions the team will take

1. **P0: measure and design.** For every question in scope, quote its
   text, its consuming rules, and the 2025 instruction; state who is asked;
   propose words. Probe a truthful filer on core v86 where the current
   words mislead. Prototype a scratch core v87 and rerun recorded returns.
   Stop and report any item that needs more than content.
2. **Decide.** The words, and which items are in.
3. **Track 0 adversarial closure.** Over the new words.
4. **Track 1: build.** Core v87, registry v85, release v85, with live and
   package tests.
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify after #270 (owner standing approval,
   2026-11-07).

## Cases that will shape the design

- A covered sale with a wash-sale adjustment beside one without: what each
  wash-sale question's answer should total.
- A zero-net sale beside the Exception 1 questions.
- A filer born on January 1, 1961, on January 2, 1961, and a filer who died
  in 2025 before turning 65.
- A student-loan filer who can be claimed as a dependent but is not.
- Every recorded return the earlier milestones replay: identical numbers on
  v87 when answered as recorded.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. Hand values come from the instructions, never from
what a prototype publishes. A sentence the filer reads is a claim: P0
records the text the presentation actually shows. Stacked on #270; if ADR
0085 is not accepted, this branch is rebuilt on main with the next free
core version.

## P0 result

Evidence: `question-wording-evidence/p0.md`, with `law.json`, `probe.py` /
`probe-output.json` (v86), `probe-v87-output.json`, `prototype.py` /
`prototype-build.json` and `rerun.py` / `rerun-output.json`.

- **All three items are content only.** None needs an engine, schema,
  expression-operation, selection or recording-surface change. Scratch core
  v87 (registry v85, release v85) replaces five members:
  - the two wash-sale adjustment closure questions (v4)
  - the Exception 1 only-box-2a question (v3)
  - the student-loan dependent question (v2)
  - the vocabulary bundle (v3), which retitles the four age and blindness
    facts without changing their versions
- **Truthful answers under the current words:**
  - A plain covered sale stays blocked on the wash-sale question.
  - A filer born January 1, 1961 gets 15,750 and no senior deduction,
    instead of 17,750 and 6,000.
  - A joint filer whose spouse is claimed deducts 500 instead of 0.
  - A zero-net sale moves no number, whatever the Exception 1 answers.
- **Under the proposed words**, all 25 probe cases reach their instruction
  hand values on v87.
- **Rerun:** the 298 recorded v83 lists that the v86 test replays are 298
  identical on v86 and v87, and every v86 pin equals its fixture pin. None
  of them shows a question in scope. In the probes, 5 cases change only
  their sentences and 20 are identical.
- **Outside the words, reported, not fixed:**
  - With a recorded wash sale and the adjustment family open, the page asks
    nothing (an admission check with no question).
  - Age and blindness are never asked (default false, no question), and
    their titles are not shown on any page measured.
- **Decisions:**
  - whether to retitle the Exception 1 and student-loan facts in their
    bundles
  - whether to keep the age and blindness title successor
  - the v87 loader entries in `packages/tax/loader.py` (code, as every core
    since v80)
  - whether to park the mixed wash-sale finding

## Decisions

Foreman, 2026-11-11, on P0. Every item is content only; the 298 recorded
returns are identical on v86 and scratch v87.

1. **Wash sale.** Both wash-sale amount questions take the P0 v4 words:
   the amount of every covered sale *with* a wash-sale loss adjustment.
2. **Exception 1.** The only-box-2a question takes the P0 v3 words, which
   exclude any 2025 sale, a zero-net sale included. The fact's title in a
   successor of `exception1.bundle.json` says the same.
3. **Student-loan dependency.** The question takes the P0 v2 words ("Is
   someone else claiming you (or your spouse, on a joint return) as a
   dependent on their 2025 return?"), and the fact's title in a successor
   of `sli-scope.bundle.json` names the spouse too.
4. **Age and blindness titles.** The vocabulary bundle successor takes the
   P0 v3 titles: born before January 2, 1961, the day-before-the-birthday
   rule, the death-in-2025 rule, and the blindness test as the instruction
   states it. Fact versions do not change. No page shows these titles
   today; they are kept so the fact means what the law says when it is
   asked.
5. Core v87, registry v85 and release v85, with their entries in
   `packages/tax/loader.py` as for every core since v80. Nothing else in
   code changes.
6. **Parked**, not built: with a recorded wash sale and the adjustment
   family open, the page asks no question; age and blindness are never
   asked and default to false.
