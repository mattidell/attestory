# Retrospective — Gambling Winnings on Form W-2G (2025)

## Result

- **Gambling winnings on Form W-2G compute on core v65.** Box 1 reaches
  Schedule 1 line 8b and total income; box 4 reaches line 25c, which had
  been a constant zero. Each family has its own closure, and an unconfirmed
  one blocks only its own lines.
- **The class is bounded by answer, not by omission.** Winnings not on a
  W-2G, other line 8 income, business gambling and gambling losses are
  refused by a new absence answer and the existing Schedule A gambling
  declaration.
- **Every earlier package refuses a recorded W-2G,** so a log is never
  computed without it.

## What the evidence changed

- **The refusal today was an answer, not a missing route.** v64 had no
  W-2G fact type at all; "no other Schedule 1 income" refused the return.
  The new answer narrows that refusal to everything except W-2G winnings.
- **New families must be guarded from both ends.** The closure guard (from
  the last three milestones) stops a partial sum; the review found a second
  shape the closure cannot see, a box 4 amount with no box 1 on the same
  statement, and a same-statement companion pair now refuses it.
- **Fail-closed by an impossible companion.** Earlier packages are made to
  refuse a W-2G by a presence pair naming a witness no log can hold, removed
  by v65's own declaration. It needed no engine change; it does mean every
  later core must carry the declaration, which is why package-scoped
  declarations in package content stays parked.

## Process

- First breadth slice in this queue: P0, one track, one review, one repair,
  all Sonnet 5.5, about an hour of agent time.
- The CI Chrome startup flake failed most full runs during this series; see
  the stacked PRs. #229 is the likely remedy.

## Follow-ups

- Cents in itemized amounts block the Schedule 1 tie-out (inherited from
  Form 1099-G; pinned).
- Add the Form W-2G and its instructions to the local sources and corroborate
  box 1 to line 8b.
- Gambling losses for itemizers, and not refusing a standard-deduction filer
  who has them.
