# Retrospective — Every Attachment Waits for Its Statements (2025)

## Result

- **On core v63, no attachment shows an unconfirmed amount.** Schedule D,
  Form 8949, Schedule 1 and Schedule B wait until every family they read is
  confirmed complete. Before, one recorded Form 1099-B proceeds amount put
  1,000 on Schedule D while line 8a blocked.
- **Line 2b waits too.** An unconfirmed Form 1099-INT, 1099-OID, Schedule
  K-1 box 5, non-form interest or Schedule B adjustment no longer moves line
  2b, total income or AGI. That closes the largest gap the collect-closure
  survey left open.
- **Twenty subtotal successors,** each guarding its own collect. No
  attachment, line, validator, engine or schema change, and no new question.
  A complete return computes exactly as on v62.

## What the evidence changed

- **The line 2b question was mis-framed.** The survey's Track 1 found the
  validator forbids a guarded line 2b, and the foreman concluded that the
  subtotals were pinned by version, so guarding them needed a new line 2b
  too. Line 2b v8 has no pins; it reads the subtotals by symbol. Guarding the
  subtotals was content all along, and the owner question raised in #234 is
  withdrawn.
- **Guard the producer, not the consumer.** An attachment's completeness
  takes only categorical answers and its tie-out must equal the raw
  subtotals, so the attachment cannot carry the guard. A guarded subtotal
  makes every reader wait at once: the line, the attachment and the
  explanation.
- **A plan guess was wrong.** The plan expected the wash-sale families to be
  forced closed; P0 showed they are not, and Form 8949 published the
  unconfirmed amount.

## Process

- At the usage-limit resume, the foreman took P0's uncommitted files for an
  interrupted unit and launched a second builder while the first was still
  running. The first finished; the second was stopped before it changed
  anything. Lesson recorded: confirm an agent has ended before relaunching
  its unit.
- The eight-citizen stop was waived for one change set of one guard shape,
  reviewed as one unit; the review found nothing required.
- Stacked on #234 (core v62) by owner direction; this package is core v63.

## Follow-ups

- Confirm Form 1099-INT box 8 live with a return that box 8 does not block
  outright.
- The guard is now in the subtotal for every family the survey found; a new
  subtotal should copy it. The regression test enforces that.
