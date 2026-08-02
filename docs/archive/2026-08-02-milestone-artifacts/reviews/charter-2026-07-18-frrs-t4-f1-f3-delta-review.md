# Charter: Track 4 Repair 1 — Author-Independent Delta Review

Date: 2026-07-18. Owner-authorized fresh review of the narrow Track-4 repair.
Branch: `track/frrs-t4-w2-closure-live-integration`. Review exactly
`cad81d6` → `a08f37b`; implementation charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t4-f1-f3-repair.md`.

## Measurements

1. **F1:** A fabricated, missing, tampered, or `--no-verify`/raw-transport
   envelope authority is rejected; separately installed commit and push entries
   scan their complete declared envelopes before crossing. The reviewer must not
   accept a deterministic public-path hash or a public constructor as proof.
2. **F2:** An escaping output path refuses before creating either run record or
   output. A valid output still produces its paired records inside `L`.
3. **F3:** W-2 uses the distinct published wages quantity; taxable-interest and
   wages are semantically distinct, and core-v2/registry/release/adoption bytes
   regenerate exactly. No v1 byte changed.
4. Re-run focused Track-3/4 suites, full suite, mypy, governance lint, generator
   regeneration, diff check, and a full repair-delta safety scan.

## Output and limits

Write exactly one record:
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-18-frrs-t4-f1-f3-delta-review.md`.

State merge-ready/not-merge-ready and classify findings. Do not modify code,
fixtures, ADRs, schemas, unrelated review records, or merge state; do not push,
open GitHub objects, handle real data, or dispatch an agent.
