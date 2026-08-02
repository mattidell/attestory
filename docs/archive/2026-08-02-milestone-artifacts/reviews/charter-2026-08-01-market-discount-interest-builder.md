# Payer-Reported Current-Inclusion Market-Discount Interest — Integrated Builder Charter

Audience: Builder.

Status: prepared for owner launch after the planning unit is committed.

## Context Capsule

- **Source ref and resolved launch commit:** the committed planning tip on
  `milestone/market-discount-interest`; run
  `python3 tools/build_orientation_block.py --ref HEAD`, verify its SHA against
  Git, and echo scope, evidence ceiling, selected-version inventory, immutable
  history, and stop conditions before editing.
- **Exact object or commit range:** implement Track 1 after the planning unit;
  the Foreman will record the planning-tip-to-builder-tip range for review.
- **Role and tier:** one integrated Builder, Medium/medium. Raise the tier only
  if the paper/readiness check identifies genuine new mechanism design; that is
  a charter stop and owner checkpoint, not silent scope growth.
- **Scope and evidence ceiling:** MD-C1 through MD-C5 and the complete MD-P1–P10
  / MD-N1–N13 matrix. The ceiling is production-shaped synthetic evidence
  through `live_coordinate_run`; no real data, owner attestation,
  transaction/basis calculation, or L3 claim.
- **Stop conditions:** stop if either payer-reported boundary needs transaction,
  basis, taxpayer-accrual, election-eligibility, or new adjustment machinery;
  if a new evaluator operation, attachment schema/runtime, or presentation
  behavior is required; if historical bytes/checksums must change; if a
  positive instance cannot be written honestly; if the graph needs mixed
  producers; if the work touches Schedule D, subtractive adjustments, other
  market-discount situations, unrelated income, real/private data, governance
  interpretation, or a reserved ontology entry; or if a base failure cannot be
  isolated to this range.

## Authoritative specification

The active plan is the sole specification for MD-C1 through MD-C5 and the
MD-P/MD-N matrix. The paper sources establish the tax boundary only:

- [Instructions for Forms 1099-INT and 1099-OID](https://www.irs.gov/instructions/i1099int), Box 10 and Box 5;
- [Publication 1212 (December 2025)](https://www.irs.gov/publications/p1212);
- [Publication 550 (2025)](https://www.irs.gov/publications/p550);
- [2025 Form 1040 instructions](https://www.irs.gov/instructions/i1040gi); and
- [2025 Schedule B instructions](https://www.irs.gov/instructions/i1040sb).

The supported value is the payer-reported nonnegative current-inclusion amount.
Do not calculate accrual, election eligibility, covered-security status,
disposition inclusion, basis, or any adjustment. Form 1099-INT box 10 and Form
1099-OID box 5 are separate source families; box 5 is the OID reporting route.

## Readiness check before implementation

Before changing code, mechanically inspect and record the versions actually
selected by the current adoption and release graph:

1. `packages/sample_data/k1_interest_breadth/adoptions/adopt-core-v9-current.json`;
2. `packages/sample_data/k1_interest_breadth/publication_surface/releases/demo.release.2025.v4.json`;
3. `packages/content/tax/2025/published-packages.v4.json`;
4. `packages/content/tax/2025/package.core-calculations.v9.json`; and
5. the selected member files for composition v2, line-2b rule v2, line-2b
   field v3, and Schedule B attachment-rule.v2/content v2.

Record selected versions and checksums in the first handoff note. Do not infer
selection from a file merely being published. Also confirm the current
`artifact-package.v6` admission and composition-obligation seams before editing.

## Targeted implementation reads

Read exact contract text from the plan and ADRs 0015, 0016, 0026, 0027, 0029,
0033, 0036, and 0046. For mutable code, inspect only the relevant symbols and
callers first:

- `packages/derivation/package_validation.py`: `validate_package`,
  composition-obligation helpers, and attachment-rule v2 admission;
- `packages/derivation/source_authority.py`:
  `validate_mapping_against_family`, `resolve_closure_admissions`, and
  `audit_collect_authority`;
- `packages/derivation/runner.py`: `RunContext`, `_execute`, attachment
  evaluation dispatch, and source-family collection/tie-out path;
- `packages/derivation/marshal.py`: `marshal_closure_authority`,
  `marshal_run_context`, and live context construction;
- `packages/derivation/live.py`: `live_coordinate_run` and presentation output
  wiring;
- `packages/derivation/production_resolver.py`:
  `PublicationSurface`, `select_current_adoption`,
  `_verify_release_and_registry`, and `resolve_production_package`; and
- `packages/derivation/presentation_projection.py`:
  `_resolve_field_row`, `_resolve_attachment`, `build_presentation_model`,
  and `validate_presentation_model`.

Target test methods rather than preloading whole large files: K-1 contract and
live cases, Schedule B structural/tie-out cases, selected resolver tests,
generic presentation projection/live tests, and the existing line-2b tests used
for compatibility. Add new focused modules with MD-P/MD-N IDs.

## Implementation work packet

1. Add two versioned source bundles/families/mappings/subtotal rules/citations
   for Form 1099-INT box 10 and Form 1099-OID box 5, using existing payer +
   logical statement + tax-year identity and contribution/lifecycle paths.
2. Publish interest composition v3, line-2b rule successor, and line-2b field
   successor with exactly seven source families and current-closure pins.
3. Publish Schedule B content v3 under `attachment-rule.v2`, adding exactly two
   Part-I row sets and preserving the generic multi-family, threshold, Part-II,
   Part-III, disposition, and attachment-only failure behavior.
4. Publish package v10, registry v5, release v5, and a synthetic current
   adoption. Preserve package v9/release v4 and every historical checksum.
5. Add focused production-shaped lifecycle, package, Schedule B, explanation,
   and presentation tests. Commit one canonical positive presentation golden;
   use generic negative containment or compact mutation evidence.

No new evaluator mechanism, attachment schema/runtime, or presentation behavior
is expected. If one is required, stop and report the exact contract seam before
implementing it.

## Required evidence and economy handoff

Every MD-P/MD-N ID must appear in a test name/docstring or an explicit stronger
case equivalence. Group changed files as authored contract, runtime, tests, and
generated/expanded artifacts. Report Orientation Block bytes/words, tool calls,
wall time, authored versus generated/expanded lines and bytes, focused command
results, and every stop/residual issue. Do not review the work, write the
independent review, open/merge a PR, or expand the milestone.

## Verification before handoff

Run focused tests once after stabilization, plus touched compatibility modules,
schema registry, mypy, diff check, governance lint, and the envelope scan over
the planning-tip-to-builder-tip range. Use `live_coordinate_run` for ordinary
integration evidence. Leave the worktree clean and return custody to the
Foreman with the exact implementation range.

