# Capital-Gain Distributions / Line 7a — Line 7b Prerequisite Repair Charter

Audience: Builder.

Status: **chartered by owner disposition after the Track-3 clean stop.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-line7b-prerequisite` at this committed
  charter/pointer. The branch descends from Track-2 merge
  `90f12e607cd4ff61770c14859b2a720763361336` through the Track-3 binding and
  clean-stop records. Resolve `HEAD` through the orientation command and verify
  it against Git before acting.
- **Exact object:** close only the production-condition gap recorded in
  `docs/reviews/2026-07-31-capital-gain-distributions-line7a-track3-charter-stop.md`:
  the adopted graph must expose one versioned line-7b form-field citizen whose
  declared symbol joins the existing line-7b rule's atomic published, blocked,
  and guard-inapplicable dispositions through generic mechanisms.
- **Role:** the Track-3 Builder continues its own stop lineage as the
  prerequisite repair Builder.
- **Scope and evidence-rung ceiling:** add immutable content/package,
  registry/release, adoption, generator, and production-shaped synthetic test
  successors only. Do not implement presentation projection or rendering.
  Resolved-graph plus authoritative synthetic `live_coordinate_run` evidence is
  the ceiling.
- **Stop conditions:** stop and report if the repair requires editing any
  existing published content, package, registry, release, adoption, schema,
  checksum, or accepted ADR; adding a schema or generic substrate; changing the
  existing line-7b rule or conclusion computation; tax-specific projector
  behavior; changing line 7a/9/16 or Track-2 runtime behavior; weakening package
  exclusivity, resolver verification, or tests; broadening into presentation,
  Schedule D, Form 8949, Form 1099-B, or excluded-box computation; interpreting
  governance text; or touching real/private material.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/reviews/2026-07-31-capital-gain-distributions-line7a-track3-charter-stop.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md` Decisions 5 and 8
  plus Production Conditions;
  `packages/content/tax/2025/form1040.line-7b.form-field.json`;
  `packages/content/tax/2025/rule.form1040-line7b.json`;
  `packages/content/tax/2025/package.core-calculations.v7.json`;
  `packages/content/tax/2025/published-packages.v2.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v7-current.json`;
  `packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v2.json`;
  `tools/generate_frrs_t3_fixtures.py`;
  `packages/derivation/production_resolver.py`;
  `packages/derivation/presentation_projection.py` only to verify the generic
  join boundary, not to edit it;
  `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`;
  `tests/test_frrs_t3_resolver_bootstrap.py`;
  `tests/test_frrs_t4_w2_live_integration.py`;
  `tests/derivation/test_package_validation.py`;
  `tests/test_schema_registry.py`;
  `AGENTS.md#Schema Publication Protocol`; `AGENTS.md#Fixture Rules`; and
  `AGENTS.md#Data Safety Rules`.

Before editing, echo the exact production-condition gap, the versioned-successor
ceiling, the generic-join invariant, authoritative entrypoint, immutable-history
constraint, and every stop condition.

## Required repair

1. **Line-7b form-field successor.** Add a new unused version of
   `tax.us.2025.form1040.line-7b` whose `binds_symbol` exactly matches the
   existing line-7b rule's published symbol. Preserve its fixed `"checked"`
   rendering instruction, atomic blocked/guard-inapplicable descriptions, and
   exact `tax.us.2025.citation.form1040.line-7b@v1` pin. Do not edit or replace
   v1.
2. **Exclusive package successor.** Add
   `tax.us.2025.package.core-calculations@v8` as a strict successor to v7. Keep
   the reviewed v7 graph unchanged except for selecting the new line-7b field
   version as an additional form-field member. Do not include both field
   versions or admit any unreviewed neighbor.
3. **Verified publication route.** Add a new versioned package registry,
   synthetic release, and v8 adoption route. Each checksum edge must verify
   exactly. Preserve the v1/v6 and v2/v7 registry/release/adoption chains
   byte-for-byte.
4. **Deterministic generator ownership.** Extend
   `tools/generate_frrs_t3_fixtures.py` to reproduce the new route and every
   existing committed route exactly. No hand-maintained fixture may drift from
   its generator.
5. **Production-shaped proof.** Add one focused synthetic module proving:
   the resolver selects v8 and includes exactly the new field version; the
   field symbol equals the existing line-7b rule's published symbol; eligible,
   missing-authority, and conclusion-`"yes"` runs expose the existing line-7b
   rule's published, blocked, and guard-inapplicable dispositions
   respectively; and a v7 run remains unchanged. Enter runs through
   `live_coordinate_run`, never a hand-built `RunContext`.

The repair ends at the resolved member/disposition boundary. Track 3 owns
categorical projection, strict validation, product rendering, goldens, and
browser criteria after this prerequisite merges.

## Verification

Run focused modules while iterating, then once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.derivation.test_package_validation
python3 -m unittest tests.test_schema_registry
git diff --check <charter-commit>..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite. CI remains the gate of record.

## Handoff

Commit one prerequisite implementation commit after this charter/pointer
commit. Leave the worktree clean and report the SHA, exact files, immutable
byte-comparison evidence, checksum chain, resolved member/disposition proof,
focused results, and any stop finding. Do not review, push, open a PR, edit
pointers, restart Track 3, or begin Track 4.
