<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "derived-answers",
  "status": "Open. P0: trace each scope answer the return already implies and say, per fact, which direction the recorded statements actually prove.",
  "scope": [
    "a scope answer that the recorded statements already prove is not asked of the filer on a successor core, and the line it holds computes as if the filer had answered it",
    "the basis for each derived answer is named: what recorded fact proves it, and in which direction; an answer the record cannot prove is still asked",
    "a return that already answers the question computes exactly as on core v73, and earlier cores are unchanged"
  ],
  "non_goals": [
    "never derive an absence from the lack of a record: no recorded Form 1098 does not prove the filer received none",
    "no recording surface for group questions, and no per-member value written from a group yes",
    "no change to what a line computes once its answers are present",
    "no edit to any published schema, adopted package, parameter or rule version; only successors",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-11-03-scope-answer-questions.md",
      "docs/phases/engine-breadth/milestones/scope-answer-questions.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/derived-answers.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/derived-answers.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/derived-answers.md"
    ]
  }
}
-->

# The Return Answers What It Already Shows (2025)

Milestone key: derived-answers.
Branch: milestone/derived-answers-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-03.
Starting point: `github/main` at `7a5c9e8f` (PR #253 merged; core v73 is the
latest).

## What we are trying to accomplish

Since core v73 a line blocked on a missing yes/no scope answer names one of
41 questions covering 80 facts. Some of those questions ask what the return
already shows. A filer who recorded a Form 1098 is still asked whether they
have one; a filer whose Form 1099-INT box 8 family is closed is still asked
about tax-exempt interest; a filer who listed dependents is still asked
about other dependents. The useful outcome is fewer questions, each one
asking only what the record cannot settle.

The danger is the other direction. The record proves presence; it never
proves absence. Not having recorded a Form 1098 does not mean the filer
received none. Every derived answer must name its basis, and an answer the
record cannot prove stays a question.

## What we know

- **Candidates** (roadmap parked list): Form 1098 scope; line 2a Form
  1099-INT tax-exempt interest (the closed box 8 family); the
  other-dependent answer (the rosters); and in part Form 1116 required and
  the Form 1099-OID and Exception 1 capital-gain facts.
- **How answers are read today.** Each scope fact is an input binding; a
  rule reads it with `ref`, and its absence blocks `DEPENDENCY_ABSENT`,
  which `_closure_question_reasons` turns into the input question.
- **Polarity.** Some facts assert presence and some assert absence; since
  v73 every question's "yes" means present. A derived "present" can satisfy
  a presence fact directly, but it can only satisfy an absence fact by
  making the absence false.
- **What we do not know.** For each candidate, which direction the record
  proves; whether the rule language can already express "answered, or
  proved by the record" (an `any` over a `ref` and a count, as line 25b v4
  does), or whether this needs an engine change; how many lines each
  derived answer releases; and what an existing v73 return that already
  answered sees.

## Actions the team will take

1. **P0 — trace and design.** For each candidate, through
   `live_coordinate_run` on v73: what the filer is asked, what the record
   proves and in which direction, and what each consuming rule would need
   to accept the proof instead of the answer. Classify each candidate as
   *derivable* (the record proves the answer the rule reads), *partly
   derivable* (it proves one value only; the other still asks), or *not
   derivable*. Design the smallest successor set; count the lines each
   releases and what changes for existing fixtures and goldens. Hand-computed
   cases. No content changes. If any candidate needs an engine, schema or
   operation change, stop and report.
2. **Decide.** Which candidates are delivered, and how a derived answer is
   shown to the filer (so the line's explanation says what proved it).
3. **Track 1 — derive.** The successors; core v74 and its registry and
   release with `tools/package_successor.py`; any loader companion entry;
   cases through the real coordinator; v73 and earlier pinned.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- A Form 1098 recorded and the Form 1098 scope unanswered: no question; the
  mortgage lines compute.
- No Form 1098 recorded and the scope unanswered: still asked.
- Each candidate with the record proving it, and with the record silent.
- A filer who answered the question and whose record agrees: identical to
  v73.
- A filer whose answer contradicts the record (answered "no Form 1098" with
  one recorded): what happens today on v73, and what should.
- A joint return where one spouse's record proves the answer.
- A return with none of the candidate records: unchanged from v73.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction, 2026-11-03).
P0 and Track 1 are builder units; the close is a fresh-reader review. Each
unit commits on this branch as it goes. Stop means stop.

## P0 result

P0 is in [trace and design](derived-answers-evidence/p0-trace-and-design.md),
with the probe, the scratch v74 prototype and its outputs beside it.

- **Four candidates are partly derivable; none fully.** Each record proves
  presence only:
  - a recorded Form 1098 proves a statement was received (releases 19
    lines);
  - a closed box 8 subtotal above 0 proves tax-exempt interest (28 lines;
    a recorded zero still asks);
  - a marked other-dependent row proves an other dependent (13 lines);
  - box 7 over $300 ($600 joint) proves Form 1116 is required (one line;
    the credit stays unpublished, as on v73 after the same answer).
- **Not derivable.** The Form 1099-OID fact, the four Exception 1 facts and
  the other 74 facts. The answer that releases their lines is an absence,
  and Exception 1 would also need a new operation.
- **Shape.** Seven successor rules read the record first and read the
  answer only when the proof fails, with no new schema or operation. Line
  12e v4, line 2a v5, Schedule 3 line 1 direct-credit v4, and four
  other-dependent rules.
- **Costs found.**
  - A filer whose answer contradicts the record no longer blocks; the record
    wins. `ref` raises when absent, so no rule can both skip a missing
    answer and check a present one.
  - Every answered return publishes v73's amounts. The presentations differ
    because of the added closure reads, and on the proved path the
    scope-answer pin disappears.
  - The proof needs its family closed, so an answered return with that
    family open would block on closure where v73 published.
  - Nothing names the question that was skipped or the finding that proved
    it.

## Decisions

Foreman, 2026-11-03, on P0:

1. **Deliver the four partly derivable candidates**, each held to one
   condition: no return v73 publishes may newly block on v74. Track 1 runs
   each answered return with the proof's family left open; a candidate that
   newly blocks there is held back and parked, not delivered.
2. **The record wins over a contradicting answer.** A recorded Form 1098 or
   a marked other-dependent row is stronger evidence than the answer
   against it, and the published amounts equal the agreed return's. The
   lost contradiction blocks are stated in the outcome. Keeping them needs
   an absent-tolerant read, an engine change, parked.
3. **"Computes exactly as on v73" means the published amounts.** Answered
   returns' presentation bytes differ by the proof's closure reads and the
   dropped scope pin; that is stated, not hidden.
4. **No per-run "derived from" sentence.** The computed line cites the
   statement figures it read; naming the skipped question needs a schema,
   parked.
5. **Not delivered:** the Form 1099-OID fact, Exception 1 and the other 74.
   The direct-credit rule's member/file schema mismatch on v73 (member
   `rule-artifact.v14`, file `rule-artifact.v3`) is left; the successor
   member uses the file's schema.

## Tracks

1. **Track 1 — derive.** The successors from P0; core v74, registry v72,
   release v72 with `tools/package_successor.py`; any loader companion
   entry; cases through the real coordinator; v73 and earlier pinned.
