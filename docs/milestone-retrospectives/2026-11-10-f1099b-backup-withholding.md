# Retrospective: Form 1099-B Backup Withholding (2025)

Milestone key: f1099b-backup-withholding. Plan:
`docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md`.
Closed 2026-11-10.

## What happened

Core v82 refused any Form 1099-B statement whose box 4 answer was "yes".
Core v83 asks one box 4 amount per statement and adds every current amount
to Form 1040 line 25b, beside the five existing withholding subtotals.

P0 settled the amount design, but its summary cited case ids that no
output held, and its rerun of the 213 v82 returns replaced each return's
answers with a box 4 of $0. The foreman recorded what was unbacked and
Track 0 redid it. The first Track 0 classified the 213 returns by
construction; the rerun measured them: 150 now ask the box 4 amount, 63 are
identical, none publishes a different number. Decision 2's hoped-for
bridge (a v82 "no" closing its statement at $0) is impossible in content,
because `require_paired` blocks before a fallback can read the old answer.

The fresh review computed every case by hand and found one wrong number:
Track 0 had decided that a box 4 amount whose statement has no recorded
sale is ignored, so line 25b published $0 and the refund was low. Box 4 is
tax withheld whether or not a sale is recorded (a broker files a
box-4-only Form 1099-B for a short still open at year end). Decision 6
reversed it; the repair rebuilt v83 in place, and the re-review measured
every case correct.

## What worked

- A hand-computing fresh reader. Track 0 and the build both pinned the
  wrong orphan value, because each followed the engine; only a reader
  working from the IRS instructions caught it.
- Re-reviewing the repair, not just accepting it. The re-review measured
  the fix and named the content workaround it needed.

## What to change

- A Track 0 row that rules an amount "ignored" is a tax claim. Write its
  hand value from the instructions, not from what the prototype publishes.
- The repair needed a selection default to publish zero with no closure
  question, and the language makes a selection path name its collect as a
  symbol. A rule therefore publishes 0 under the box 4 amount's own id (no
  consumer reads it; its explanation walk says 0). That is a language gap,
  parked below, not a pattern to copy.
- The P0 builder's summary was not its evidence. Check every cited case id
  against a committed output before deciding on P0.
- Builder cost rose: Track 1 and its repair cost about $28 on grok, the
  two reviews about $12. The 2.1 MB fixture and 298 runs follow the
  sibling's shape; shrinking both is parked with harness isolation.

## Follow-ups

Parked in the roadmap: a way for a selection path to name a keyed collect
without a symbol publication (then retire
`rule.f1099b-b4-amount-symbol` and the unwritten `inert` path in a
successor), and box-4-only Form 1099-B statements, which are counted when
recorded but never asked.
