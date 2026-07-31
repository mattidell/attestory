# Capital-Gain Distributions / Line 7a — Line 7b Prerequisite Review Charter

Audience: Reviewer.

Status: **chartered for author-independent review.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-line7b-prerequisite` at this
  committed review charter/pointer. Resolve and verify `HEAD` before acting.
- **Exact object:** the immediate parent commit titled
  `Add line 7b prerequisite successors`, measured against its immediate parent
  repair charter. It contains exactly seven files: the line-7b field v2,
  package v8, registry v3, synthetic release v3, synthetic adoption v8,
  deterministic FRRS generator, and focused prerequisite test module.
- **Role:** the existing independent Luna Reviewer, with no exposure to the
  Builder's implementation process.
- **Scope and evidence-rung ceiling:** independently measure every obligation in
  `docs/reviews/charter-2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite.md`.
  Resolved-graph and authoritative synthetic `live_coordinate_run` evidence is
  the ceiling. Do not review or design Track-3 projection/rendering.
- **Stop conditions:** return `NOT READY` if object custody differs; any
  historical content/package/registry/release/adoption/schema/checksum changed;
  field v2 alters tax meaning, citation identity, or dispositions beyond the
  versioned generic-symbol repair; v8 contains both field versions or any
  unchartered member change; registry/release/adoption checksum edges do not
  verify; deterministic regeneration differs; the existing rule or
  line-7a/9/16 behavior changed; proof bypasses `live_coordinate_run`; tests
  were weakened; or governance/private material is implicated.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`; the
  prerequisite repair charter; the Track-3 stop record; the exact seven-file
  implementation delta; ADR-0050 Decisions 5 and 8 plus Production Conditions;
  historical field v1/package v7/registry v2/release v2/adoption v7;
  `packages/derivation/production_resolver.py`;
  `packages/derivation/presentation_projection.py` only to measure the generic
  join boundary;
  the focused prerequisite and regression modules named below;
  `AGENTS.md#Schema Publication Protocol`; `AGENTS.md#Fixture Rules`; and
  `AGENTS.md#Data Safety Rules`.

Before measuring, echo the exact object range/file set, credited Track-2
evidence, generic-join invariant, evidence ceiling, immutable-history boundary,
and stop conditions.

## Required measurements

1. **Object custody and history.** Confirm the implementation is exactly the
   seven named files. Compare every existing v1/v6 and v2/v7
   registry/release/adoption file, field v1, package v7, published schemas, and
   their recorded checksums byte-for-byte against the repair-charter parent.
2. **Field successor.** Compare v2 with v1. The new version must preserve the
   field identity, exact line-7b citation, fixed checked render instruction,
   and atomic disposition meanings while changing only what the versioned
   generic-symbol repair requires. Its `binds_symbol` must equal the unchanged
   line-7b rule's `publishes`.
3. **Package exclusivity.** Compare v8 with v7 semantically. Aside from package
   version/checksum metadata, the only graph change must be addition of exactly
   one line-7b field member selecting v2. Neither field v1 nor any unrelated
   content may enter v8.
4. **Publication verification.** Independently recompute member, package,
   registry, release, and adoption checksum edges. Mutate each new edge in
   memory and confirm the resolver refuses it through existing verification.
5. **Generator ownership.** Render the FRRS fixture map and compare it
   byte-for-byte with the committed corpus. Prove all prior routes retain their
   prior bytes and the new v3/v8 route regenerates exactly.
6. **Production-shaped behavior.** Independently rerun the focused module and
   inspect the authoritative entrypoint. Confirm v8 resolves exactly field v2;
   the existing line-7b rule exposes published, blocked, and guard-inapplicable
   states for the three cases; and v7 remains unchanged without the line-7b
   field. Grep to ensure no hand-built `RunContext` shortcut.
7. **Regression and safety.** Run the named focused modules, diff check,
   governance lint, and envelope scan. Inspect all new identities and paths for
   synthetic-only compliance.

## Verification

Run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.derivation.test_package_validation
python3 -m unittest tests.test_schema_registry
git diff --check <repair-charter>..<implementation>
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite. CI remains the gate of record after review.

## Handoff

Commit one review record at
`docs/reviews/2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-review.md`
with a falsifiable `READY` or `NOT READY` verdict, per-measurement evidence,
exact commands/results, and residuals. Leave the tree clean. Do not repair,
edit pointers/charters, push, merge, restart Track 3, or begin Track 4.
