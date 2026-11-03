# Retrospective — Each Statement Answers Its Withholding (2025)

## Result

- **On core v71 a Form 1099 recorded without its withholding answer stops
  line 25b.** Forms 1099-INT, 1099-DIV, 1099-R and 1099-G need a box 4
  answer and SSA-1099 a box 6 answer, $0 included, as W-2 box 2 already did
  on line 25a. Before, two Forms 1099-G with 600 recorded and 400 not
  published a refund of 25 instead of 425.
- **An answered return computes exactly as on v70.** One successor rule
  (line 25b v4) in an already-published schema, one loader entry; no engine
  or schema change.
- **Two limits remain:** a statement recorded only through another box is
  not counted, and a surplus answer can offset a missing one.

## What the evidence changed

- **The W-2 mechanism carried over unchanged.** Line 25a's count comparison
  needed only `gte` instead of equality, so a withholding-only statement
  keeps v70's result.
- **Adoption costs two answers, not one.** Recording a missing box 4 moves
  the family's horizon, so its closure question is asked again.
- **A count is not a pairing.** The review's surplus case publishes the
  wrong number on v71 as on v70; only a keyed join closes it.

## Process

- First milestone run in its own new worktree beside another foreman's open
  milestone (#250); no shared files.
- P0 lost about 20 minutes to `pgrep` waiters that matched themselves.
  Later dispatch prompts said to run commands in the foreground.

## Follow-ups

- A statement-level count or keyed join for line 25b's check.
- Name the short statement, and say $0 is an answer, when line 25b blocks.
