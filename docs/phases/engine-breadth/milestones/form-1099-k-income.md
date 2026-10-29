<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form-1099-k-income",
  "status": "Track 1: block Schedule 1 line 10 on core v60 while any Form 1099-K is unresolved.",
  "scope": [
    "an unresolved or unsupported Form 1099-K stops every line that would otherwise publish without its income, on a successor core package",
    "a resolved Form 1099-K, and a return with none, keeps every result it has today",
    "missing-box-4 cases for Forms 1099-DIV and 1099-R beside the existing 1099-INT case",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no new Form 1099-K income route: what a resolved 1099-K computes is unchanged",
    "no Form 1099-K box 4 on line 25b (SC-R1 still holds), and no family declared on the published box-4 fact",
    "no package companion declaration for the 1099-K family (ADR-0082 production condition 2 stays parked)",
    "no change to the withholding-while-unclosed behaviour of any withholding family",
    "no edit to any published schema, adopted package, parameter or rule version; only successors",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-10-28-form-1099-withholding.md",
      "docs/phases/engine-breadth/milestones/form-1099-k-income.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/form-1099-k-income.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/form-1099-k-income.md"
    ]
  }
}
-->

# An Unresolved Form 1099-K Stops the Bottom Line (2025)

Milestone key: form-1099-k-income.
Branch: milestone/form-1099-k-income-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-28.
Starting point: `origin/main` at `3fc6160a` (PR #228 merged; core v59,
registry v57, release v57 are the latest).

## What we are trying to accomplish

The form-1099-withholding final review recorded a return with one Form
1099-K whose box 4 was $150. The 1099-K unresolved rule, the Schedule 1 top
entry and the Schedule 1 attachment blocked, but lines 24, 25b, 33, 35a and
37 published the same figures as without the 1099-K: a $505 refund. The
repair traced it further: any Form 1099-K the engine cannot resolve (a
nonzero box 4, or circumstance questions left unanswered) is left out of
line 8 and total income while lines 24 through 37 publish, on v58 as on v59.

A filer who received a Form 1099-K is shown a refund computed as if the form
did not exist. The only signal is a blocked Schedule 1 attachment, which no
bottom-line figure waits on.

The useful outcome: while any Form 1099-K is unresolved, no line whose value
depends on total income publishes; the explanation names the 1099-K as the
reason; once the filer resolves it, the return computes as it does today.

## What we know

- **Engine (core v59).** `rule.f1099k-unresolved` v3 blocks when any
  statement's loss reason is not `supported-loss`, and is otherwise
  inapplicable (P0 corrected "otherwise `false`"). The Schedule 1 top entry
  read the same loss reason (neither reads the unresolved symbol). Its
  form-field text says "the return's income does not yet account for this
  Form 1099-K statement".
- **What we do not know.** Which rule chain carries Schedule 1 Part I into
  Form 1040 line 8, and why it publishes while the attachment blocks; whether
  line 8 should block or the whole chain from line 9 down should wait on the
  1099-K condition; which successors that needs (rules, package v60, registry
  v58, release v58) and what an existing workspace is asked on adoption
  (ideally nothing); whether any saved presentation or golden reaches a
  1099-K.

## Actions the team will take

1. **P0 — trace and design.** Reproduce the gap through `live_coordinate_run`
   on v58 and v59 for both causes (nonzero box 4; unanswered circumstance).
   Trace the line 8 chain from content. Design the smallest successor set
   that blocks every line depending on total income while any 1099-K is
   unresolved, and leaves resolved returns byte-identical. Hand-computed
   cases. No content changes.
2. **Decide.** The block point and successors.
3. **Track 1 — block.** The successor rules, core v60 / registry v58 /
   release v58, cases through the real coordinator, the missing-box-4 tests
   for 1099-DIV and 1099-R.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, frontier and parked list.

## Cases that will shape the design

- The reviewer's return on v60: unemployment with $600 withheld plus one
  Form 1099-K with $150 in box 4. Line 8 onward does not publish; the reason
  names the 1099-K.
- The same with box 4 zero and supported-loss answers: every line as today.
- A Form 1099-K with a circumstance question unanswered: blocked, same reason.
- A return with no Form 1099-K: every line as on v59.
- A v59 answer set adopted onto v60 with a resolved 1099-K: no new question,
  same result.

## P0 result

P0 is in [trace and design](form-1099-k-income-evidence/p0-trace-and-design.md),
with the probe and its output beside it.

- **The gap.** Schedule 1 line 10 reads line 7 (unemployment) and the ten
  Part I absence facts, nothing from the 1099-K. Line 8 reads line 10 only.
  No rule pinned by v59 names `tax.us.2025.f1099k.unresolved`. A Form 1099-K
  whose loss reason is anything but `supported-loss` blocks the top entry and
  the attachment and nothing else; lines 8 through 37 publish. The same split
  holds on v58.
- **A resolved 1099-K adds nothing to line 10, correctly.** The only
  supported class is a personal item sold at a loss, which the 2025 Schedule 1
  reports in its top entry, not as income.
- **Decision (foreman, 2026-10-28): block at Schedule 1 line 10.** A
  successor `rule.schedule1-line10` v2 refs line 7 when every loss reason is
  `supported-loss` (or there is no 1099-K), and otherwise a
  `conditional_dependency_set` on `tax.us.2025.f1099k.unresolved`, so line 10
  blocks naming it and lines 8 through 24 and 34 through 37 wait behind it.
  Lines 25b and 33 do not read income and still publish. Line 10 rather than
  line 8, because line 10 is the figure that publishes the additional income.
  No engine, schema or expression-operation change; no new question on
  adoption; no golden reaches a 1099-K statement.
- **Core v60 must repeat v59's ADR-0082 companion declaration**, or it
  refuses 1099-G and SSA-1099 withholding again.

## Tracks

- P0: trace and design.
- Track 1: the block on core v60.
