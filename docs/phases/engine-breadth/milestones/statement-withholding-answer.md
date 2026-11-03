<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "statement-withholding-answer",
  "status": "Open. P0 traces how a statement recorded without its withholding answer reaches line 25b on core v70 and designs a per-statement answer check.",
  "scope": [
    "a Form 1099-INT, 1099-DIV, 1099-R or 1099-G recorded without its box 4 answer, or a Form SSA-1099 without its box 6 answer, stops line 25b and every line behind it on a successor core package, as a Form W-2 without its box 2 answer already stops line 25a",
    "a return whose statements each carry their withholding answer, including $0, computes exactly as on core v70",
    "say plainly what an existing return must now answer, and keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no new withholding source: no Form 1099-K box 4 (SC-R1), no Form W-2G change, no line 26",
    "no pairing of each answer with its own statement beyond what the rule language already does; the W-2 box 2 check compares counts",
    "no change to income families, their closure, or what a complete withholding family computes",
    "no edit to any published schema, adopted package, parameter or rule version; only successors",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-10-30-withholding-closure.md",
      "docs/milestone-retrospectives/2026-10-22-refund-or-amount-owed.md",
      "docs/phases/engine-breadth/milestones/statement-withholding-answer.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/statement-withholding-answer.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/statement-withholding-answer.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/statement-withholding-answer.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Each Statement Answers Its Withholding (2025)

Milestone key: statement-withholding-answer.
Branch: milestone/statement-withholding-answer-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-02.
Starting point: `github/main` at `ef40e96b` (core v70 is the latest). PR #250
(W-2 correction guidance) is open in another worktree; it changes the entry
loop and publishes no core package, so this milestone's successor is core
v71.

## What we are trying to accomplish

The withholding-closure milestone (#233) left one gap parked: *a withholding
closure attested true over an amount never recorded still publishes the
smaller line 25b.* A filer records a Form 1099-R, does not enter its box 4,
confirms the family complete, and gets a smaller refund or a larger amount
owed, published as if it were the answer.

Form W-2 already closes this: line 25a blocks unless every W-2 has a box 2
answer, by comparing the count of statements with the count of answers (the
refund-or-amount-owed retrospective). The useful outcome: each Form 1099
withholding statement carries its own box 4 answer, $0 included, before line
25b publishes, and the person is told which statement is missing it.

## What we know

- **Line 25b (core v70)** adds five subtotals (Forms 1099-INT, 1099-DIV,
  1099-R, 1099-G box 4 and SSA-1099 box 6). Since v61 it waits with
  `require_closed` for each family's closure.
- **Line 25a** checks W-2 box 2 answers with the existing `count` operation.
  It catches a missing answer, not a mismatched one.
- **Cost to existing returns.** A complete return whose interest-only Form
  1099-INT has no box 4 entry would now block until $0 is answered. How many
  committed fixtures, goldens and adopted workspaces that touches is
  unknown.
- **What we do not know.** How each statement and its box 4 amount are
  recorded today (one act or two; whether a $0 answer can be recorded and is
  distinct from absence); whether the count check carries over to each
  family unchanged; whether box 4 absence and the family's closure interact;
  and how an existing v70 return reaches its answers on adoption.

## Actions the team will take

1. **P0 — trace and design.** Reproduce the gap through
   `live_coordinate_run` on v70 for each of the five families. Trace the W-2
   box 2 check and how each 1099 statement and its withholding are
   recorded. Design the smallest successor set that blocks line 25b while
   any statement lacks its answer and leaves answered returns byte-identical.
   Count what it changes for existing fixtures and goldens, and say what an
   existing return is asked on adoption. Hand-computed cases. No content
   changes. If the fix needs an engine, schema or operation change, stop.
2. **Decide.** The check's shape, its blocked-line wording, and the adoption
   path.
3. **Track 1 — check.** The successors; core v71 and its registry and
   release with `tools/package_successor.py`; the v71 companion entry in
   `packages/tax/loader.py`; cases through the real coordinator; v70 and
   earlier pinned to today's behaviour.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- A Form 1099-R with box 4 left unanswered, its family closed: blocks.
- The same statement with box 4 answered $0: identical to v70.
- Two Forms 1099-G, one answered, one not.
- One case per family, including SSA-1099 box 6.
- A joint return, one spouse's statement unanswered.
- A return with no Form 1099 at all: unchanged.
- A complete v70 return adopted onto v71: what it is asked, and nothing else
  moves.

## Process

Dispatch is to Sonnet 5.5 Agent sub-agents (owner direction, 2026-10-30).
P0 and Track 1 are builder units; the close is a fresh-reader review. Each
unit commits on this branch as it goes. Charters live under
`docs/reviews/statement-withholding-answer/` until closeout distills them
here. Stop means stop.

## P0 result

P0 is in [trace and design](statement-withholding-answer-evidence/p0-trace-and-design.md),
with the probe, the scratch v71 prototype and their outputs beside it.

- **The gap is real in all five families.** On v70 a statement recorded
  without its box 4 (SSA-1099: box 6) answer, its family closed, computes
  exactly as if $0 were answered. Two Forms 1099-G with 600 and an
  unrecorded 400 publish line 25b as 600 and a refund of 25, not 1,000 and
  425.
- **Line 25a's mechanism carries over.** It compares the count of box 2
  answers with the count of W-2 box 1 members and otherwise falls through
  to a `ref` that blocks `DEPENDENCY_ABSENT` naming the box 2 fact. A $0
  answer is an ordinary assertion and counts; absence is no finding.
- **Design.** One successor, `rule.form1040-line25b` v3 → v4 in the
  published `rule-artifact.v4` (line 25a's schema, which has `count`):
  v3's five `require_closed` guards plus, per family, `any` of a count
  comparison and a `ref` of the withholding fact. Core v71, registry v69,
  release v69; a v71 companion entry in `packages/tax/loader.py`. The
  prototype matched v70 on every answered, $0 and no-withholding case; all
  27 differences of 85 are line 25b blocks.
- **Cost.** No committed v70 fixture or golden carries a Form 1099 income
  statement; earlier packages and their tests are pinned. An existing v70
  return is asked each missing amount (or $0), then its family's closure
  question again, because recording moves the family's horizon.
- **Limits.** The check counts statements through their income box; a
  statement recorded only through another box (Form 1099-INT box 3, 8 or 10;
  Form 1099-DIV box 2a, 7 or 12) is not counted, and a surplus answer can
  offset a missing one. The block names the fact, not the statement; naming
  the statement needs a keyed join, an engine change.

## Decisions

Foreman, 2026-11-02, on P0's recommendations:

1. **`gte`.** A return with an extra withholding answer (withholding on a
   statement with no income box) computes as on v70; `eq` would block it.
2. **The other-box boundary and the surplus offset are parked**, stated in
   the outcome and the roadmap. Covering them needs a statement-level count
   or a keyed join.
3. **The block keeps line 25a's shape** (`DEPENDENCY_ABSENT` naming the
   withholding fact). Track 1 reports what the existing explanation and
   presentation say for it on v71; any wording change beyond existing
   mechanisms is parked.
4. **`rule-artifact.v4` is reused, not added**; the v71 loader entry is in
   scope (as v61's was).
5. **No v71 entry-loop profile.** The entry loop is #250's.

## Tracks

1. **Track 1 — check.** Line 25b v4; core v71, registry v69, release v69
   with `tools/package_successor.py`; the v71 companion entry; cases through
   the real coordinator for each family, joint, $0, no-withholding, the
   surplus answer, and the adopted v70 return; v70 pinned.
