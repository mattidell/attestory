# Capital-Gain Distributions / Line 7a — Track 2 F1/F2 Repair Charter

Audience: Builder.

Status: **chartered for Luna dispatch after a charter-bound owner grant.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track2` at review commit
  `9c531c6d075c09dde23ea193d03f83ff0baf79f3`.
- **Exact object:** repair only F1 and F2 from
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track2-review.md`.
  The current implementation baseline is
  `679b5532768f5fa4cd051fa3853752690cbbad94`; its stable patch ID
  `4cfecac372e13691241fd12e33335942008eabc8` exactly matches the review
  record's pre-rebase implementation object. The review-charter and
  administrative phase-state commits are context, not repair targets.
- **Role:** Luna as the Track-2 repair Builder, High tier / high effort. This
  is the one findings-only repair allowed for the track.
- **Scope and evidence-rung ceiling:** restore ADR-0050's typed-state partition
  for line 16 and isolate the Track-2 release/adoption fixture successor from
  the existing v6/v1 fixture pair. Production-shaped synthetic integration is
  the ceiling. Every passing review measurement is credited and must remain
  unchanged.
- **Stop conditions:** stop and report if either finding requires changing
  accepted ADR-0050; mutating a published schema or existing checksum;
  changing an accepted historical content/package version; adding a new
  evaluator operation, runner-resident tax arithmetic, or generic substrate;
  weakening the exact failing tests or replacing production evidence with a
  test-only helper; broadening into Schedule D, Form 8949, Form 1099-B,
  excluded-box computation, presentation, browser, or Track 3; interpreting
  governance text; or touching any real/private material. If the typed state
  partition cannot be represented by existing declared machinery, return that
  charter-stop finding instead of inventing substrate.
- **Full reads before acting:** this charter;
  `docs/roles/builder.md`;
  `docs/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track2.md`;
  `docs/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track2-review.md`;
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track2-review.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  ADR-0050 Decisions 5–8 and Production Conditions;
  ADR-0012's atomic-disposition contract;
  ADR-0038's line-16 and declared-absence contract;
  `packages/content/tax/2025/rule.form1040-line16.v3.json`;
  `packages/content/tax/2025/package.core-calculations.v7.json`;
  `packages/content/tax/2025/published-packages.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v7-current.json`;
  `packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v1.json`;
  `packages/derivation/live.py`;
  `packages/derivation/runner.py`;
  `packages/derivation/production_resolver.py`;
  `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`;
  `tests/test_dsbs_t2_coordinator.py`;
  `tests/test_dsbs_t3_line16_coordinator.py`;
  `tests/test_dsbs_t3_qdcg_declarations.py`;
  `tests/derivation/test_package_validation.py`;
  `AGENTS.md#Schema Publication Protocol`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before editing, echo F1 and F2, the credited passing measurements, the exact
repair ceiling, the authoritative `live_coordinate_run` entrypoint, the
immutable-history constraint, and every stop condition.

## Credited passing evidence

Preserve without re-buying the first review:

- published-schema history and manifest integrity;
- box-2a closure and admission interlock behavior;
- package validation, raw-read guards, and mixed-graph rejection;
- checked-conclusion truth table and every non-guard-inapplicable line-7a,
  line-9, line-16, QDCG, pin, explanation, and lifecycle branch;
- authoritative goldens entering through `live_coordinate_run`; and
- clean patch, governance lint, and data envelope.

The repair must add no unrelated cleanup. Run focused regression checks to
prove these credited surfaces remain intact; do not redesign them.

## Required repair

### F1 — Preserve the typed disposition partition before numeric line-16 work

1. Make selected line 7a's atomic disposition control line 16 before missing
   numeric dependencies or comparisons can collapse the outcome:
   `guard_inapplicable` must produce line-16 `inapplicable`, while a genuinely
   blocked selected line 7a remains blocked.
2. Preserve all numeric branches exactly: QDCG when `Q>0` or `L>0`, ordinary
   tax only when both are closure-backed zero, with the already-reviewed direct
   pins and citations.
3. Keep the behavior declared through existing production machinery. Do not
   special-case the two failing fixture IDs, weaken required inputs globally,
   or add runner-resident tax doctrine.
4. Make both existing F1 reproductions pass: the component-`"no"` case and the
   forward correction to component `"no"`. Add a focused assertion only if an
   adjacent blocked-versus-inapplicable invariant is not already explicit.

### F2 — Version the new fixture route; restore the existing route byte-for-byte

1. Restore
   `adopt-core-v6-current.json` and
   `demo.release.2025.v1.json` to their exact pre-Track-2 bytes. Track 2 may
   not rewrite the established v6 adoption or v1 release to absorb the new
   package-registry checksum.
2. Give the new v7 adoption its own explicitly versioned synthetic release
   route and checksum chain. Follow the established resolver/release schema;
   do not alter production resolution semantics merely to accommodate the
   fixture.
3. Prove both routes coexist: the existing
   `tests.test_dsbs_t2_coordinator` v6/v1 surface remains green, and the
   Track-2 v7 coordinator resolves and executes through its successor release.
4. Inspect the resulting diff for accidental changes to established
   adoptions, releases, packages, registry entries, or generated goldens.

## Verification

Run the two finding modules while iterating, then run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
python3 -m unittest tests.test_dsbs_t2_coordinator
python3 -m unittest tests.tax.test_capital_gain_distributions_line7a_t2_package
python3 -m unittest tests.tax.test_dsbs_t3_contradiction_interlock
python3 -m unittest tests.test_dsbs_t3_line16_coordinator
python3 -m unittest tests.test_dsbs_t3_qdcg_declarations
python3 -m unittest tests.derivation.test_package_validation
python3 -m unittest tests.test_schema_registry
git diff --check 9c531c6d075c09dde23ea193d03f83ff0baf79f3..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite. CI remains the gate of record.

## Handoff

Commit one repair commit after this charter/pointer commit. Leave the worktree
clean and report the SHA, exact files changed, focused results, exact
pre-Track-2 byte-restoration evidence for the v6/v1 fixtures, the new successor
release route, and whether every credited passing measurement remains
structurally unchanged. Do not review the repair, edit the review record or
pointers, push, open a PR, or begin Track 3. The foreman will charter the
original Reviewer for a focused F1/F2 recheck.
