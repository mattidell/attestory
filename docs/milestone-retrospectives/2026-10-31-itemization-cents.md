# Retrospective — Statements With Cents (2025)

## Result

- **Statements with cents compute on core v66.** Two Form 1099-G box 1
  amounts of $100.40 blocked the Schedule 1 attachment on v65 (rows 200.80,
  subtotal 201). On v66 the subtotal keeps its cents, line 7 rounds once to
  201, and the attachment ties out. The same for Form W-2G, Schedule D line
  13 and Schedule B Part II.
- **Lines that add several amounts round once, at the total,** as the 2025
  instructions say: line 25b over two families of $100.40 is 201, not 200,
  and the refund moves by a dollar.
- **Whole-dollar returns compute as before.**
- **Not delivered: Schedule B Part I interest,** which waits on an owner
  question about the package validator.

## What the evidence changed

- **The bug was a rounding order, not a tie-out bug.** The tie-out was right
  to compare raw rows with the subtotal; the subtotal was wrong to round. The
  fix moved one `round` per family from the subtotal to the line that reads
  it.
- **Line 2b is pinned three times over.** The validator's successor-graph
  table fixes line 2b's rule, its form field and the Schedule B attachment
  from core v38 on. That blocked a content fix here, as it did a closure fix
  in the collect-closure survey. It is now one owner question.
- **The citizen stop worked as a design tool.** P0 met it at 39 and
  proposed five tracks; building them one at a time surfaced the validator
  table before most of the work was spent.

## Process

- Sonnet 5.5 throughout. One builder carried four tracks and a repair,
  stopping twice correctly (a representation change in saved explanations,
  then the validator table). The foreman accepted the first and deferred
  the second.
- The stack this milestone sat on (#233-#237) was rebased onto #229 and
  merged during it.

## Follow-ups

- The line 2b validator question (owner).
- Current-core harnesses for line 2a, Schedule 8812 line 21 and Form 1098-E.
