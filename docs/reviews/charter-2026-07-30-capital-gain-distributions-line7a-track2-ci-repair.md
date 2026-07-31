# Capital-Gain Distributions / Line 7a — Track 2 CI Repair Charter

Audience: Builder.

Status: **chartered as a continuation of the Track-2 F1/F2 repair lineage after
the full CI gate rejected readiness.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track2` (PR #120) at this committed
  charter/pointer. Resolve `HEAD` through the orientation command and verify
  the printed commit against Git before acting.
- **Exact object:** repair only the four deterministic failures from PR #120
  `verify` run `30591151422`. The reviewed F1/F2 repair is
  the branch commit titled `Repair Track 2 line 16 and release routing`; the
  focused recheck is
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track2-repair-recheck.md`.
  CI, not that focused recheck, is the final gate of record and rejected the
  track.
- **Role:** the original Track-2 repair Builder, continuing its own lineage.
- **Scope and evidence-rung ceiling:** restore full-suite consistency among the
  already-reviewed v7 package/release route, the repository-wide role
  vocabulary, deterministic FRRS fixture generation, and the existing
  production-shaped presentation golden. Synthetic repository integration is
  the ceiling. This is completion of the existing repair, not a second
  findings-driven redesign.
- **Stop conditions:** stop and report if closing a failure requires changing
  accepted ADR text; changing a published schema or checksum; changing the
  reviewed F1/F2 runtime behavior; rewriting the established v6 adoption, v1
  release, or canonical v1 registry; changing production resolution semantics;
  adding a rule-language operation or runner-resident tax doctrine; changing
  presentation projection semantics; weakening or deleting a failing test;
  broadening into Track 3 product presentation work; interpreting governance
  text; or touching real/private material.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track2-repair.md`;
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track2-repair-recheck.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `packages/derivation/loader.py`;
  `packages/schemas/artifact-package/artifact-package.v5.schema.json`;
  `tools/generate_frrs_t3_fixtures.py`;
  `tools/generate_presentation_l2_golden.py`;
  `packages/content/tax/2025/published-packages.json`;
  `packages/content/tax/2025/published-packages.v2.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v7-current.json`;
  `packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v1.json`;
  `packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v2.json`;
  `tests/derivation/test_language_schemas.py`;
  `tests/test_frrs_t3_resolver_bootstrap.py`;
  `tests/test_frrs_t4_w2_live_integration.py`;
  `tests/test_presentation_l2_integration.py`;
  `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`;
  `AGENTS.md#Fixture Rules`; `AGENTS.md#Schema Publication Protocol`; and
  `AGENTS.md#Data Safety Rules`.

Before editing, echo the four CI failures, the exact consistency invariant for
each, the immutable v1/v6 boundary, the synthetic-only ceiling, and every stop
condition.

## Required repair

### C1 — Keep the published role token inside the one master vocabulary

The published `artifact-package.v5` role
`checked-conclusion-binding` must be recognized by the repository's single
`ROLE_VOCABULARY`. Do not edit the published schema, weaken the subset test, or
create a second vocabulary.

### C2 — Make the deterministic FRRS generator own both release routes

Extend `tools/generate_frrs_t3_fixtures.py` so its rendered file map exactly
matches the committed synthetic corpus, including the reviewed v2 registry
release and v7 adoption. Preserve the canonical v1 registry, v1 release, and v6
adoption byte-for-byte. The generator must select each adoption's matching
registry/release/checksum chain explicitly; do not make the old route inherit
the new registry.

### C3 — Refresh only the deterministic presentation golden affected by F1

Regenerate the existing production-shaped v6 presentation golden through
`tools/generate_presentation_l2_golden.py` and its authoritative
`live_coordinate_run` path. Inspect the semantic diff. It may reflect only the
reviewed generic false-guard finalization's deterministic derivation identity
and corresponding explanation structure, plus the already-reviewed Track-2
runner behavior that adds the rule's declared
`tax.us.2025.citation.form1040.line-16@v1` pin to the resolved line-16 finding.
The latter is required by the original Track-2 charter's exact-citation
contract and entered the branch in the reviewed Track-2 build; this
clarification does not authorize a new runner or projection change. If values,
dispositions, any other citation, redaction behavior, package selection, or
unrelated sections change, stop and report instead of accepting the golden.

### C4 — Prove the repair closes the exact full-suite failures

Run each of the four previously failing tests directly, then the adjacent
Track-2 and legacy coordinator modules. Do not edit tests merely to accept the
new output. Preserve the focused recheck's F1/F2 conclusions.

## Verification

While iterating, run only the directly affected modules. Before handoff, run
once:

```text
python3 -m unittest tests.derivation.test_language_schemas
python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
python3 -m unittest tests.test_dsbs_t2_coordinator
python3 -m unittest tests.derivation.test_runner
python3 -m unittest tests.test_schema_registry
git diff --check <charter-commit>..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite. CI remains the gate of record.

## Handoff

Commit one CI-repair commit directly after this charter/pointer commit. Leave
the worktree clean and report the SHA, exact files changed, focused results,
byte-identity evidence for the v1 registry/v1 release/v6 adoption, the exact
semantic categories changed in the presentation golden, and whether all four
CI failures are closed. Do not review, edit review records or pointers, push,
merge, or begin Track 3.
