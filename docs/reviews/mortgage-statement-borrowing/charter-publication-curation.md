# Publication curation — mortgage borrowing

Audience: Builder assisting the Foreman with a mechanical publication rebuild.

## Purpose

Prepare a reproducible version of the reviewed mortgage work: the current
plan, the accepted source-family restoration decision, the finished product,
and useful lessons. Preserve the actual behavior and tests of the reviewed
candidate, including payment-comparison repairs. The Foreman will inspect and
integrate the result; this assignment does not push or merge the PR.

## Source and boundaries

- Primary branch: `milestone/mortgage-statement-borrowing-same-loan`.
- Ratified base: fetched `origin/main` at `31ff9c78e47aa5ccea3e320a9bf3f903433c9863`.
- Exact reviewed product source and safety ref:
  `snapshot/2026-10-26-mortgage-reviewed-pre-curation`, commit
  `2c219230440bacb2c43781eef26b4080ec05817a`, tree
  `8cdd8897b87aa8a0b80a6e53fb071691333fda19`.
- Independently reviewed fixes are in that source tree. Distill relevant
  product meaning into the plan and tests rather than shipping review narration.
- Do not alter product code, content, schemas, tests, fixtures or generator
  bytes relative to the reviewed source. Preserve ratified base artifacts,
  package v57 / registry v55 / release v55 and their checksum chain.
- Preserve the owner-approved ADR 0080 without changing accepted ADR bytes.
  Keep milestone status in progress until the Foreman completes closeout.
  Final independent review and CI remain pending on the rebuilt candidate.

## Actions

1. In a temporary, agent-owned worktree and `temp/milestone/` branch based on
   the stated ratified commit, reconstruct a small logical commit sequence:
   plan; ADR 0080 and its index entry; scoped recording; restoration kernel;
   declared calculation and package; saved reader; and current closeout-ready
   documentation. Split or combine implementation files only as necessary to
   keep coherent work and preserve their final bytes.
2. Distill the plan to the current product contract, supported behavior,
   meaningful scope limits, publication status and source citations. Remove
   temporary paths, interim commit IDs, historical review narration and
   pointers that would dangle after curation. Keep the owner's exact-pair
   meaning, distinction between source applicability and recorded statements,
   result dependencies and correction/withdrawal behavior.
3. Update README, phase documents and retrospective to match the finished
   behavior and pending gates. The retrospective carries only material lessons
   that can guide future work, not a timeline of repairs. Keep Box 11's separate
   known limitation appropriately bounded; do not repair it here.
4. Remove working review files only after their useful design content has a
   durable home. Until a final closeout/review charter is committed, preserve
   enough valid active routing for a successor Foreman; do not claim the PR is
   reviewed or CI-green on the rebuilt candidate.
5. Verify every product/test/generator file against the safety-ref tree, the
   ratified base against its original bytes, generator `--check`, diff check,
   governance lint and envelope scan. Report all differences with reasons;
   any product-byte mismatch is a stop, not an invitation to repair it.

Do not touch the primary branch, force-push, alter GitHub, run a full suite or
perform a browser walkthrough. Report the temporary candidate ref, commit list,
tree and validation results. Keep the worktree and branch available for Foreman
inspection and integration; do not clean them until confirmed safe.

## Fold the publication-review repairs

Fresh publication review found two wording defects, now repaired and
independently rechecked. The owner's full local lane also exposed a synthetic
v1 compatibility-test fixture defect, now repaired; the complete lane then
passed with 3,524 tests and 20 skips, and mypy passed. Preserve this exact
product/test/tool tree from
`snapshot/2026-10-26-mortgage-verified-pre-final-curation` at `8d953302`, tree
`33ec548096455fba0ef3e1f2010d5e5abbecf82e`.

Reconstruct or refold the already curated commits on the same ratified base,
integrating the branch-only bundle title and generated-checksum changes into
their owning content commit, the local help change into recording/review, and
the tests into their relevant units. Do not alter the verified product bytes.
Use the current primary plan, README and carry-forward lessons as the durable
document source. Keep only the active curation and final-review charters needed
for routing while this work remains open; remove other working review records
after preserving their meaning in tests and plan. Keep status honest: the
publication review and full local lane have passed on the source, but final CI
on the rebuilt PR head remains outstanding. No closure, CI or merge claim.

Verify byte identity against the new safety ref for every `packages/`, `tests/`
and `tools/` path; verify ratified schema/content bytes, generator `--check`,
diff/lint/envelope and valid Foreman orientation. The full test lane already
passed with the exact product bytes and must not be rerun merely for curation.
Do not modify the primary branch or the earlier temporary worktree. Return the
new temporary candidate ref, commits, tree and exact evidence; final review and
CI are separate.
