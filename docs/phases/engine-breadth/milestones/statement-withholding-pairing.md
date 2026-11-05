<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "statement-withholding-pairing",
  "status": "Open. P0: show, through the real coordinator, the returns where line 25b publishes a wrong amount because a withholding answer on one statement covers a missing one on another, and whether the rule language can pair them per statement.",
  "scope": [
    "on a successor core, line 25b blocks unless every recorded Form 1099-INT, 1099-DIV, 1099-R, 1099-G and SSA-1099 has its own withholding answer, $0 included",
    "a statement recorded only through another box is checked too, where the record can show it is a statement",
    "a return whose every statement is answered computes exactly as on the current core, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no change to line 25a or the W-2 check unless P0 shows the same defect there",
    "no new question wording beyond naming the short statement",
    "no recording surface or entry-loop change",
    "no edit to packages/kernel/ (another milestone owns it)",
    "no edit to any published schema, adopted package or rule version; only successors",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-11-02-statement-withholding-answer.md",
      "docs/milestone-retrospectives/2026-11-04-all-questions-at-once.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/statement-withholding-pairing.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/statement-withholding-pairing.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/statement-withholding-pairing.md"
    ]
  }
}
-->

# Each Statement Is Checked For Its Own Withholding (2025)

Milestone key: statement-withholding-pairing.
Branch: milestone/statement-withholding-pairing-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-04.
Starting point: `github/main` at `0cf68edd` (PR #257 merged; core v76 is the
latest).

## What we are trying to accomplish

Since core v71 line 25b blocks when a Form 1099 or SSA-1099 is recorded
without its withholding answer. The check compares counts: at least as many
withholding answers as income amounts, per form. A count is not a pairing.
Two Forms 1099-G, one with an answer of 600 and a second answer recorded
twice by mistake, or one statement answering withholding on its own while
another does not, pass the count and publish a refund that leaves out the
missing statement. The retrospective of that milestone named the case. The
useful outcome is that line 25b never publishes while any one statement is
missing its answer.

## What we know

- **The check today** (line 25b v4): per form, `count(withholding) >=
  count(income)` over two families, or the withholding `ref` is absent.
- **Two known gaps** (roadmap parked list):
  - a statement recorded only through another box (Form 1099-INT box 3, 8
    or 10; Form 1099-DIV box 2a, 7 or 12) is not counted at all;
  - a surplus answer on one statement offsets a missing one on another.
- **Operations that may already pair.** The evaluator has `shared_key_count`
  and `link_coverage`. Whether either pairs a withholding member with its
  statement's income member, and on what key, is not known.
- **What we do not know.** Whether a wrong amount is reachable through
  `live_coordinate_run` today (or whether admission, identity or the
  statement key already refuses the surplus case); which forms are
  affected; whether W-2 line 25a has the same gap; what the blocked line
  should say.

## Actions the team will take

1. **P0 — reproduce and design.** On core v76 through `live_coordinate_run`:
   build each surplus and other-box case per form, and record what line 25b
   publishes against the hand-computed right answer. Establish what key
   ties a withholding member to its statement, and whether
   `shared_key_count`, `link_coverage` or another existing operation can
   express "every statement has its own answer". Prototype the smallest
   successor in scratch. Check line 25a for the same gap. No content
   changes. If the fix needs an engine, schema or operation change, stop
   and report.
2. **Decide.** Which forms and cases are fixed, and what the blocked line
   names.
3. **Track 1 — fix.** The successors; core v77 and its registry and release
   with `tools/package_successor.py`; any loader companion entry; cases
   through the real coordinator; v76 and earlier pinned; full suite.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- Two statements of one form, one answered and one not, where the answered
  one has a second withholding member: what is published today, and after.
- The same across two forms (a Form 1099-INT answered twice, a Form 1099-DIV
  not answered).
- A statement recorded only through another box, with and without an
  answer.
- Every statement answered, $0 included: identical to v76.
- A joint return with one statement per spouse.
- A return with no Form 1099: unchanged.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction). P0 and
Track 1 are builder units; the close is a fresh-reader review. Each unit
commits on this branch as it goes. Stop means stop.

The opening commit also marks `test_three_dispositions_are_honest` in
`tests/test_capital_gain_distributions_line7a_t3_presentation.py` live, as
its sibling already is. It regenerates the goldens through the derivation,
takes about 1 s locally, and tripped the 3.0 s fast-lane budget on a CI
runner during #257.

## P0 result

The count gap is reachable on v76 through `live_coordinate_run`. A missing
withholding answer plus a withholding-only 7 publishes first-plus-7 on
INT, DIV, IRA, 1099-G and SSA-1099 (57, 47, 1207, 607, 807). The right
answer is a block. INT boxes 3, 8 and 10, and DIV boxes 2a and 12, publish
0 when unanswered. DIV box 7 is already covered by its box 1a companion.
A second member on the same statement keys is rejected; an ordinary later
assertion replaces the current amount. Line 25a has the same gap: a
box-2-only slip makes the counts equal and publishes 4600.

Existing operations are enough. Ten subject rules use `shared_key_count`
on the key `statement` and publish the category `answered`. Line 25b v5
is a selection that reads those results and otherwise keeps the v4 sum.
A scratch v77 ran all 44 probe rows: 44 met, and every answered return
matched v76, including a 0 answer and a withholding-only extra. The ten
defect rows now block and name the unanswered statement. No engine,
schema, or new operation is required. A real successor also copies v76's
gambling companion declaration onto the new package version. Line 25a was
measured and left unchanged.

The record, the probe, and the prototype are in
`docs/phases/engine-breadth/milestones/statement-withholding-pairing-evidence/`.

## Decisions

Owner, 2026-11-04, on P0:

1. **A guard operation, from core v77.** A per-statement pairing check a
   rule's `when` can use: every current statement with an income amount
   of the named fact types has its own withholding answer on the same
   statement key, $0 included. When one does not, it blocks
   `DEPENDENCY_ABSENT` naming the missing withholding fact, so the existing
   box 4, box 6 and box 2 input questions still show. A withholding-only
   statement still counts in the total. Not P0's content-only selection:
   it would have named the income statement instead of the missing answer,
   and it needed two facts that nothing records.
2. **Line 25a too.** W-2 box 2 is paired on `w2-slip` on the same core.

Foreman:

3. The operation is a rule-language addition, so it lands as
   `rule-artifact.v15` under the schema publication protocol, and as ADR
   0083 in `proposed` status, which the owner accepts or sends back at
   close. The evaluator change sits in `packages/derivation/`; no edit to
   `packages/kernel/`.
4. An ordinary later assertion on the same statement replaces the current
   amount; that is correction, not this milestone.
5. Core v77, registry v75, release v75, and a loader companion entry
   sharing v76's declaration.

## Tracks

1. **Track 1 — pair.** The operation, `rule-artifact.v15`, ADR 0083
   (proposed), line 25b and 25a successors, core v77, its registry and
   release; P0's 44 cases and the W-2 rows through the real coordinator;
   v76 and earlier pinned; full suite and mypy.

## Track 1 result

Landed. `require_paired` on `rule-artifact.v15`, admitted by
`artifact-package.v40`. ADR 0083 is proposed. Line 25b v5 and line 25a v3
keep the prior value and closures and replace the count comparison with the
pairing check. Core v77, registry v75, and release v75. The loader shares
v76's companion declaration.

The ten line 25b defect rows and the W-2 4600 row now block and show the
existing withholding question. Answered rows, the $0 answer, the
withholding-only extra, a return with no Form 1099, and a joint return with
one statement per spouse publish the v76 amount. v76 spot checks matched the
recorded probe. The full suite passed: 4308 passed, 24 skipped, 8066
subtests passed. No earlier golden moved.

The case table, the suite lines, and the limitations are in
`docs/phases/engine-breadth/milestones/statement-withholding-pairing-evidence/track1.md`.
