# Retrospective: Workspace Kernel

## Milestone

- Phase: Foundation
- Branch: `milestone-workspace-kernel-track4` continuation branch, merged to `main`
- Merge commit: `c8799ce` (`Merge milestone: Workspace Kernel`)
- Track commits: `1ccc6c5` (schema framework and registry), `67d9c89` (act log and revisions), `7a86235` (fact types, facts, bundle adoption), `37c3d57` (evidence and asserted findings), `659c643` (supersession and derived currency), `d45b49c` (read models and containment drills), `906bd21` (inspection runner and kernel fixtures)

## Shipped

The workspace kernel now exists as code. It has immutable published JSON Schema citizens, a strict schema registry, an append-only JSONL act log, fact-type bundle adoption, entity-driven fact individuation, evidence submission and replacement, asserted findings, derived currency and displacement closure, rebuildable read models, a read-only inspection runner, and a synthetic fixture workspace with golden projections.

The conformance suite covers E1.1, E5.1, E5.2, E6.1, E7.1, and E7.2 with mutation or negative cases. E8.1 is recorded as not applicable because no UI flows exist yet.

## Verification

- `python3 -m unittest` - 88 tests, OK (pre-merge and post-merge).
- `python3 tools/governance_lint.py` - conformant (pre-merge and post-merge).
- `python3 -m mypy` - strict, no issues in 30 source files (pre-merge and post-merge).
- `python3 -m packages.kernel.runners.inspect_workspace --workspace packages/sample_data/kernel/demo_workspace` - printed the expected synthetic workspace summary.

## Decisions

- Tier 2: ADR-0002 and ADR-0003 remained sufficient for the durable act-log, schema, and identity contracts. No ADR-0004 was needed because the act envelope and kernel API did not materially diverge from the ratified sketches.
- Tier 1: the fact lattice is projected from adopted fact types plus current entities rather than stored; findings are projected separately over that lattice. This keeps facts open and queryable without creating a second store.
- Tier 1: evidence replacement changes a derived evidentiary-standing view, not finding identity or content. This is enforced by E1.1 tests.
- Tier 1: derivation-edge behavior is represented in the currency closure through optional finding pins, but assertion acts do not admit pinned derived findings yet. Derivation Machinery remains responsible for publishing derived findings.

## Deviations

- Work resumed from an interrupted state with Track 4 schema files uncommitted in a detached secondary worktree. The original `milestone-workspace-kernel` branch was checked out in another worktree at Track 3, so the remaining work was continued on `milestone-workspace-kernel-track4` and merged to `main` with the required milestone merge commit. The branch history still preserves one implementation commit per track.
- The schema manifest was initially regenerated before final wording cleanup on new Track 4 schema descriptions. The registry correctly refused republishing mutated entries; final hashes for only the not-yet-committed Track 4 schemas were recomputed and patched before commit.
- The milestone plan named `.venv/bin/python -m mypy`; this worktree had no `.venv`, so verification used `python3 -m mypy`.

## Data Safety

All committed fixtures are synthetic and use demo labels and IDs. No real tax documents, personal fact instances, generated artifacts from personal data, or absolute local paths were committed. `tests/test_kernel_fixtures.py` asserts the committed kernel fixture tree does not contain absolute local path markers.

## Follow-Ups

- Derivation Machinery can now consume stable kernel contracts: act envelopes, findings, fact lattice, currency closure, and read models.
- The next UI or flow milestone must add live E8.1 step-off tests; the current N/A rationale should not be treated as permanent coverage.
- Consider cleaning up the stale `milestone-workspace-kernel` branch or aligning it to the completed merge after confirming no separate work remains in the primary worktree.

## Planning Lessons

- When a milestone branch is checked out elsewhere, create an explicit continuation branch immediately instead of working detached.
- Manifest immutability checks are useful even before commit; final wording for new schemas should settle before adding their hashes.
- Keeping read models small and JSON-stable made containment and golden tests straightforward.
