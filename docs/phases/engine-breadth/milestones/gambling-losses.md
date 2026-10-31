<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "gambling-losses",
  "status": "Closed. On core v67 gambling losses up to winnings reach Schedule A line 16 and the deduction choice, and a standard-deduction filer with losses computes unchanged. The Schedule A attachment does not itemize line 16: an open owner-held question.",
  "scope": [
    "a filer with Form W-2G winnings and gambling losses computes: on the standard deduction, losses do not change the return and are no longer refused; when itemizing, losses up to winnings reach Schedule A line 16",
    "losses are recorded and confirmed complete like any other family",
    "every return without gambling losses keeps its result"
  ],
  "non_goals": [
    "no professional gambler (Schedule C) and no losses beyond winnings carried anywhere",
    "no change to how the choice between standard and itemized deduction is made, unless P0 shows the losses must enter it",
    "no engine, kernel or schema change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published citizen; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-10-31-w2g-gambling.md",
      "docs/phases/engine-breadth/milestones/w2g-gambling.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-31-gambling-losses.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-gambling-losses.md"
}
-->

# Gambling Losses (2025)

Milestone key: gambling-losses.
Branch: milestone/gambling-losses-2025, stacked on
`milestone/closure-live-confirmation` (PR #244); a successor package is core
v67, registry v65, release v65.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The Form W-2G milestone kept gambling losses refused by answer: when a W-2G
is recorded, the winnings subtotal reads the Schedule A gambling declaration,
and a filer who says they have losses is refused. Two parked consequences:

- A filer on the standard deduction with gambling losses is refused, though
  losses change nothing on that return.
- A filer who itemizes cannot deduct losses on Schedule A line 16, limited to
  winnings (100 percent for 2025).

The useful outcome: both returns compute, and the explanation shows where
the losses went or why they did not count.

## Actions the team will take

1. **P0 — trace and design.** The law, with citations (Schedule A line 16
   and the 2025 limit; whether a standard-deduction filer reports losses at
   all). How v66 refuses each case, from a run. The design: a losses family
   and closure, a Schedule A line 16 rule limited to winnings, successors
   for the declaration-reading winnings subtotal and Schedule A, and whether
   losses enter the standard-or-itemized choice. Hand-computed cases, using
   `tests/helpers/current_core_returns.py`. No content changes. Stop if the
   engine's deduction choice cannot read the new line without an engine
   change, or if the honest class needs Schedule C.
2. **Decide.**
3. **Track 1.** Successors, core v67 with `tools/package_successor.py`,
   cases on the real coordinator, v66 pinned.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Stop means stop.

## P0 result

P0 is in [trace and design](gambling-losses-evidence/p0-trace-and-design.md),
with the probe beside it.

- **Law.** The 2025 Form 1040 instructions send gambling losses to Schedule
  A line 16 (i1040gi-2025 l.6564-6571); Schedule A is the itemizer's form.
  P.L. 119-21 sec. 70114 sets 90 percent only after 2025, so 2025 is 100
  percent of losses, limited to winnings. The Schedule A instructions are not
  in the local sources; the winnings limit rests on the statute's text there.
- **Today (v66).** With losses declared, `rule.w2g-b1-subtotal` is held, so
  line 8b and everything below block, for a standard-deduction filer as for
  an itemizer. An itemizer is also refused by the Schedule A attachment's
  completeness check on the same declaration.
- **Design (13 citizens, one track).** A losses family with its closure; a
  losses subtotal; `rule.schedule-a-line16` as `choose(no winnings, 0,
  min(losses, winnings))` (a comparison inside `choose`, no new operation);
  a narrower declaration ("no other line 16 deduction") replacing the old
  one; successors for the winnings subtotal (no longer reads the
  declaration), the Schedule A total and its closed-empty form, line 12e
  (line 16 enters the itemized side, so losses can decide the choice), and
  the Schedule A attachment (line 16 as a second itemized part). Core v67.

## Decisions

Foreman, 2026-10-31, on P0's recommendations:

1. **Existing W-2G returns confirm the losses family once** (D1); the old
   declaration does not carry forward with a second meaning.
2. **A hand-entered itemized total and a nonzero line 16 together are
   refused by name** (D2), so losses cannot be counted twice.
3. **Wagering expenses stay out; losses with no winnings count as zero**
   (D3), which is the winnings limit, not a refusal.

4. **After Track 1's stop (same day).** A named block code for D2 needs a new
   runner code and a derivation-record schema successor. Accepted instead:
   the combination refuses as `DEPENDENCY_INVALID`, with the reason in the
   rule's notes; the line, taxable income and the refund do not publish.
5. **No new entrypoint.** `rule.schedule-a-boundary-no-other-line16` would ask
   every return the new declaration, so returns without gambling would gain a
   question. It is dropped; the Schedule A attachment requires the
   declaration directly, only when Schedule A is required.
6. **Earlier packages refuse recorded losses** (as for Form W-2G, ADR-0082):
   a presence pair naming an unregistered witness in the global companion
   map, removed by v67's declaration. `packages/tax/loader.py` data, not an
   engine change.

7. **Two departures from P0, accepted.** The losses subtotal applies only
   when a Form W-2G is recorded, and the Schedule A attachment does not
   itemize line 16. Either alternative would make every Schedule A itemizer
   without a W-2G confirm a losses family, changing returns without
   gambling.
8. **The attachment limit is an owner question.** Attachment parts always
   run and tie out exactly to raw row sums (`attachment-rule.v4` to `v11`,
   `attempt_attachment`), so a part cannot be conditional or limited to
   winnings. For a gambling-loss itemizer the attachment lists line 8a
   while line 12e includes line 16; a losses-only itemizer with no Form 1098
   gets correct figures and an attachment blocked on line 8a. A conditional
   or limited part needs an attachment-rule schema successor and a runner
   change.

## Tracks

1. **Track 1 — losses.** The 13 citizens in P0 section 3, core v67 / registry
   v65 / release v65 with `tools/package_successor.py`, the v67 companion
   entry, the D2 refusal, cases on the real coordinator for P0's section 4,
   v66 pinned.

## Review dispositions

Fresh-reader review: no required findings. Nine further cases on v67
matched the 2025 Tax Table (joint returns, entries above winnings, cents,
the standard-deduction boundary, withholding with an amount owed); four
returns without gambling losses publish the same values as on v66.

1. *The Schedule A attachment omits line 16* (recommended). Not fixable with
   the existing attachment schemas (decision 8); recorded as an owner
   question.
2. *A losses-only itemizer's attachment blocks on line 8a* (recommended).
   The same cause; pinned in the tests.
3. *D2's refusal names nothing in the record* (note). Accepted; the reason is
   in line 12e's notes.
4. *Wagering expenses may also be deductible for 2025* (note). Parked.
5. *An itemizer who has not answered the new declaration publishes figures
   but not the Schedule A disposition; a W-2G return confirms the losses
   family once* (note). Intended (decisions 1 and 5).

## Execution record

- Sonnet 5.5 sub-agents: one builder for P0, Track 1 and two repairs; one
  review. Track 1 stopped twice correctly (a named block code; the
  attachment shape).

## Outcome

On core v67, a Form W-2G filer with gambling losses computes. On the
standard deduction the losses change nothing (refund 1,345 with or without
$2,000 of losses). An itemizer deducts losses up to winnings on Schedule A
line 16 ($9,000 of losses against $6,000 of winnings gives 6,000), and the
losses enter the choice between itemizing and the standard deduction
($20,000 of losses alone leads to itemizing). An unconfirmed losses family
blocks line 12e; every core before v67 refuses a recorded loss. Ten new
citizens and successors; no engine or schema change. The Schedule A
attachment does not itemize line 16.
