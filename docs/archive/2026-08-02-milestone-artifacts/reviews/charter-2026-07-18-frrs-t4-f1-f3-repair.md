# Charter: Track 4 Repair 1 — Envelope Capability, Atomic Refusal, Wages Quantity

Date: 2026-07-18. Owner-authorized narrow repair after the Track-4 pre-merge
review (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-18-frrs-t4-w2-live-integration-premerge-review.md`).
Base review tip: `cad81d6`. This repair addresses exactly blocking findings
F1–F3 and does not enlarge Track 4.

## Required repair

1. **F1 — real non-forgeable envelope gate.** Replace the publicly forgeable
   deterministic `InstalledEnvelopeGuards` token with installation-bound,
   non-forgeable authority. Commit and push must remain distinct guarded
   entrypoints, scan their complete declared envelopes before crossing, and
   reject a missing, fabricated, tampered, or bypass (`--no-verify` / raw
   transport) guard. Do not represent an installed hook merely as a public path
   plus reproducible hash. The implementation must remain compatible with an
   `L` that is not a Git worktree and must never require a committed locator.
2. **F2 — validate before recording.** Resolve and reserve the declared output
   location before opening a run record or executing. An escaping/invalid output
   request returns its typed residency refusal with neither started nor completed
   record and no output. Do not invent a new failure-accounting contract.
3. **F3 — wages quantity.** Correct the immutable v2 W-2 quantity identity to
   the distinct declared wages quantity. Regenerate every dependent core-v2
   package, registry, release, and adoption checksum deterministically. Add a
   semantic golden proving W-2 and taxable-interest are distinct quantities.

## Scope fence

- Do not alter published v1 bytes, ratified ADRs/schemas, real data boundaries,
  W-2 closure behavior, or unrelated review findings.
- Do not touch the unrelated untracked Track-1 review record.
- One repair implementation commit after this charter; do not push, merge, or
  dispatch agents from the builder seat.

## Verification

Run focused Track-3/4 suites, full suite, mypy, governance lint, generator
byte-regeneration, diff whitespace, and a data-safety scan. Add executed kill
tests for every F1/F2/F3 counter-probe stated above. A fresh, author-independent
delta review is required before any Track-4 PR is opened.
