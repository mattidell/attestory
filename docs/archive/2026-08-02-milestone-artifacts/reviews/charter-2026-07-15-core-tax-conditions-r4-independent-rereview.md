# Charter — R4 Independent Re-review

Date: 2026-07-15. Chartered by the principal foreman under the Core Tax
Conditions remediation. Parent charter:
`charter-2026-07-15-core-tax-conditions-remediation.md`. Preconditions: R1
(`85ce351`) and R2 (`351c880`) are landed; R3 verification is recorded in
`2026-07-15-core-tax-conditions-r3-verification.md`.

## Seat and independence

The owner launches one reviewer in an independent context. The reviewer is not
the foreman, R1/R2 builder, or an agent supplied their in-progress work. The
reviewer writes only the review note
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-15-core-tax-conditions-r4-independent-rereview.md`; the
foreman retains commit custody and does not review the finding's merits.

## Read order

1. `docs/archive/2026-08-02-milestone-artifacts/reviews/SEAT.md`
2. This charter and its parent remediation charter
3. `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-15-core-tax-conditions-premerge-review.md`
4. `docs/adr/0027-adopted-content-manifests.md` (decisions 6–7, PC3)
5. R1 (`85ce351`) and R2 (`351c880`) diffs and their focused evidence
6. `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-15-core-tax-conditions-r3-verification.md`

## Measurements

Report evidence and a pass/fail result for each check:

1. **Exclusive projection (PMR-1 / ADR-0027 decision 7).** Trace the runner
   boundary from adoption through derivation and rendering. Demonstrate whether
   only resolved member citizens enter those surfaces, and whether the ACM-A1
   co-located unpinned-content golden proves an unpinned rule/form-field cannot
   affect either surface.
2. **Member-byte verification (PMR-2 / ADR-0027 decision 6 and PC3).** Trace
   every resolved member path to a publication-registry byte check. Demonstrate
   whether an unchanged `(id, version)` with altered bytes is rejected before
   adoption, and look for a call-site or projection bypass that admits unverified
   member content.
3. **No remediation-created contract hole.** Check that R1/R2 did not add a
   second membership authority, filesystem-path membership authority, or a
   package-embedded duplicate checksum authority.
4. **Verification evidence.** Confirm the R3 record names all three required
   green commands and that the focused R1/R2 tests named in the handoff exist.

## Verdict and stop

Conclude exactly `ready` or `not ready`, with every failed measurement tied to
a path, command, fixture, or contract clause. A `not ready` verdict stops R5;
the foreman triages and charters any follow-up. A `ready` verdict permits the
foreman to prepare R5's honest closure record, but never authorizes rewriting
`main` without owner direction.
