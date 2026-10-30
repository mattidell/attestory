# Retrospective — Package Successor Generator

## What differed from the plan

Historical reproduction exposed an existing pin/body schema mismatch inherited
by the three successors. Strict agreement for every retained pin would make byte
reconstruction impossible. The final boundary reports a retained mismatch only
when the exact predecessor pin and registry-verified body are unchanged; every
new or replacement pin must agree with its body. This is not a tax-meaning
determination.

The first trace missed a registry reorder. Comparing complete generated files
revealed that retained entries were sorted in one transition, so the change set
needed a declared ordering control as well as insertion anchors. The measured
registry bytes and canonical citizen checksums are different kinds of evidence.

## What it cost

The implementation resumed after an earlier builder's wording-only handoff.
The corrected P0 boundary was adopted; the missing construction and tests
were built in smaller increments before the connected review.

Independent review found an unused malformed registry entry could survive
construction even when the release correctly hashed the registry bytes. The
repair validates both complete registries through existing loaders; independent
confirmation exercised predecessor and candidate refusals. Review also found
silent or unhandled invalid optional values; explicit validation now refuses
them. There is no remaining material implementation finding in the reviewed
scope.

Real package validation exceeded the fast-lane budget under contention, so the
historical and validator integrations run in the live lane while cheap
synthetic refusal checks remain fast. No budget was raised.

## Follow-ups

- When a successor is published, provide its own companion declaration and
  live release evidence; generating candidate files does not supply them.
- When the tool is needed on another operating system or filesystem, first
  establish an exclusive directory-install primitive and test collision and
  failure behavior there. Linux is exercised by CI on Ubuntu; other platforms fail closed.

## What should change in the next plan

Trace complete reader boundaries, not only the selected package's members: a
valid raw hash cannot establish that every registry entry is readable. Record
the ordering and inherited inconsistencies needed for historical comparisons
before promising exact reproduction, and distinguish structural succession
from evidence about content meaning.
