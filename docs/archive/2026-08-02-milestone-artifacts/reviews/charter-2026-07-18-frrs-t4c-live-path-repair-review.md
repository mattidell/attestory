# Charter: Track 4c Live Path Repair — Pre-Merge Review Seat

Date: 2026-07-18. Status: **prepared; the owner dispatches this seat**
(ADR-0034 — explicit owner approval per dispatch). Author-independent: the
reviewer must not have implemented any part of the Track 4c repair.

## Inputs

- Findings record: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-18-frrs-t4-live-path-findings.md`
- Implementation charter: `charter-2026-07-18-frrs-t4c-live-path-repair.md`
- Contracts: ADR-0009 (record shape), ADR-0014 (closure), ADR-0024/0028
  (parameters, package fact surface), ADR-0027 (immutability/registry),
  ADR-0031/0032/0033 (boundary, contribution, resolver) — none may be
  redesigned by the repair or this review.

## Required measurements

1. **F1:** independently re-derive that the record pin widening is strictly
   additive (construct a previously valid record, assert still valid;
   construct a `parameter`-role and an input+`origin` pin, assert valid;
   assert `origin` on a non-input pin rejects). Verify the schema row matches
   on-disk bytes and that no release/registry/adoption byte outside the
   schema registry changed.
2. **F2:** through the *live path only* (act log → contribution → marshal →
   coordinator; no hand-built RunContext), assert `rounding.convention` can
   enter record state under the v3 vocabulary and that each of lines
   1a/2b/9/11/12/15/16 publishes on a fully-provisioned synthetic act log.
   Counter-probe: the pre-repair adoption (v2 package) still resolves and
   blocks exactly as the findings record describes — history preserved.
3. **F3:** an asserted W-2 closure resolves, marshals, and admits the empty
   set through the v3 fact type; the five negative closure shapes (false,
   absent, displaced, non-boolean, duplicate) still block; a displaced
   horizon closure does not admit.
4. **Immutability:** every published v1/v2 byte is unchanged; the generator
   reproduces all committed v3/registry/release/adoption bytes from a clean
   run; adoption pins in fixtures match regenerated checksums.
5. **Root-cause closure:** confirm the new golden class exercises the
   coordinator with facts on record end-to-end, such that reverting any one
   of F1/F2/F3 fails a named test.
6. Standard battery: full unittest, mypy, governance lint, data-safety scan
   over the whole delta, envelope-gate verify in the review clone.

## Output

A review record in `docs/reviews/` classifying findings (blocking / scope
defect / production condition / non-blocking), with independent evidence for
each measurement. The reviewer does not merge, push to `main`, or modify the
implementation.
