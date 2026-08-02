# Capital-Gain Distributions / Line 7a — Track 1 Builder Charter

Audience: Builder.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** `main` at
  `1cb12d78553479902a91c654510e7f9c88cc1934` (PR #110 merge; ADR-0050 and
  its complete evidence chain are on `main`).
- **Exact object or commit range:** build on
  `track/capital-gain-distributions-line7a-track1`, starting from the source
  commit above. The Track-1 review range will be `main..HEAD`.
- **Role:** one Builder, Medium tier / medium effort. This is production
  reimplementation from an accepted contract, not a new design round and not a
  review.
- **Scope and evidence-rung ceiling:** implement only Track 1's versioned
  schema/content citizens and their contract evidence. The ceiling is
  schema/content publication plus validation: no evaluator, coordinator,
  contribution-admission, tax-computation, package-successor, presentation, or
  real-data behavior.
- **Stop conditions:** stop and report if an accepted historical schema,
  manifest entry, content version, checksum, or ADR would need mutation; if a
  fully resolved positive instance cannot be written honestly; if the work
  requires interpreting governance text, a new generic substrate, runtime
  evaluator/coordinator behavior, or any citizen not assigned below; if exact
  line-7b citation identity cannot be represented without changing an accepted
  contract; or if any real value, identity, document, disposition, reason,
  workspace location, or generated private artifact would be needed.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md`;
  `docs/adr/0031-real-data-residency-boundary.md`;
  `docs/adr/0035-dividend-composition-and-lines-3a-3b.md`;
  `docs/adr/0036-schedule-attachment-ontology.md`;
  `docs/adr/0038-qdcg-worksheet-and-declared-absence.md`;
  `packages/content/tax/2025/dividend-universe.json`;
  `packages/content/tax/2025/f1099div.bundle.json`;
  `packages/content/tax/2025/qdcg.bundle.json`;
  `packages/content/tax/2025/form1040.line-9.form-field.json`;
  `packages/content/tax/2025/form1040.line-16.form-field.json`;
  `packages/tax/loader.py`; `AGENTS.md#Schema Publication Protocol`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved source commit, the Track-1 scope and evidence
ceiling, the immutable-history constraint, and every stop condition.

## Goal

Publish the versioned source, authority, universe, form-field, citation, and
supporting schema/content citizens that ADR-0050 requires before any direct
line-7a computation can be built.

## Deliverables

1. **Four Exception-1 component fact types.** Add content citizens for the four
   accepted current contributed categorical assertions C1–C4. Each has the
   exact `{yes, no}` domain, no default, presence-before-value semantics,
   `free` supersession, synthetic positive examples, and meaningful named
   negatives. Preserve the accepted distinction between each component and the
   derived checked conclusion.
2. **Checked-conclusion binding.** Add the versioned schema/content citizen
   that binds `schedule-d-required.conclusion` to C1–C4 with the accepted truth
   table and direct-pin boundary. This track publishes the declarative citizen;
   it does not execute the derivation.
3. **Box-2a source path.** Add a new Form 1099-DIV box-2a member fact type,
   independent source family, horizon-keyed closure fact type, and closure
   mapping. Identity must follow the accepted Form 1099-DIV statement pattern;
   closure must authorize the box-2a subtotal, including the closed-empty case,
   without changing the historical 1a/1b families.
4. **Successor universe and residual recorded content.** Publish a successor
   dividend-universe schema/content version whose composable set is exactly
   `{1a, 1b, 2a}` and whose residual recorded-non-composable set omits `2a`.
   Publish the matching successor recorded-boxes fact type/content version.
   Historical `dividend-universe.v1` and recorded-boxes v1 remain byte-for-byte
   immutable. This track represents only the successor graph; mixed-graph
   package rejection and the re-homed runtime signal feed belong to Track 2.
5. **Line 7a / 7b form and citation citizens.** Add distinct versioned
   form-field citizens and exact citation citizens for Form 1040 lines 7a and
   7b. Line 7b must carry exactly one ADR-0029 citation pin to
   `tax.us.2025.citation.form1040.line-7b@v1`, at the exact locus fixed by
   ADR-0050. Do not add line-7a or line-7b producer rules.
6. **Publication evidence.** Add every new schema version to its registry using
   `packages.kernel.schema_registry.write_manifest`; the manifest diff may
   only add unused filenames. For every new schema that carries or references
   a payload, commit one hand-written, fully resolved, obviously synthetic
   positive instance. Add named negatives for the load-bearing constraints,
   including non-`{yes,no}` component values, incomplete/incorrect conclusion
   binding, invalid box-2a family or closure references, malformed successor
   universe/residual-box partitions, and incorrect line-7b citation identity
   or cardinality.
7. **Contract tests.** Add a focused Track-1 test module covering every positive
   instance and named negative, exact identity/family/closure/universe pins,
   historical-byte immutability through the registry, manifest additions, and
   the line-7b citation identity/cardinality. Tests must validate content
   through the same loader/registry surface production uses where that surface
   already exists.

## Boundary

No line-7a/7b producer rule; no line-9 or line-16 successor; no QDCG worksheet
change; no admission interlock or signal raising; no mixed-graph or forbidden
raw-collect package-validation behavior; no coordinator, evaluator, marshaller,
resolver, presentation, browser, README, coverage-frontier, or retrospective
change. Do not copy prototype code into production. Reimplement each citizen
against ADR-0050 and established accepted patterns. Do not edit any accepted
ADR or published historical file.

## Verification before handoff

Run the focused modules while iterating:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
python3 -m unittest tests.test_schema_registry
git diff --check main..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

If a touched established loader/content test module exists, run that module
once and report it. Do not repeatedly run the full suite; CI `verify` is the
gate of record.

## Handoff

Commit the complete Track-1 implementation as one implementation commit after
this charter commit. Leave the worktree clean and report the commit SHA, exact
files changed, focused command results, manifest-diff inspection, and any
charter-stop finding. Do not review the work, open or merge a PR, begin Track
2, or modify the charter/pointers. The foreman will take custody and charter an
author-independent Track-1 review.
