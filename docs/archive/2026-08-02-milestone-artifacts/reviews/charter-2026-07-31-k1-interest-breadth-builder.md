# Schedule K-1 Box-5 Interest Breadth — Integrated Builder Charter

Audience: Builder.

Status: **chartered for owner launch after the planning unit is committed.**

## Context Capsule

- **Source ref and resolved launch commit:** `main` at
  `7066f26e02467a58ca6cb329666782b32bd7dd12` (PR #132 merge). The planning
  and charter commits on `milestone/k1-interest-breadth` are routing context,
  not implementation evidence.
- **Exact object or commit range:** implement on
  `milestone/k1-interest-breadth` after the committed planning unit. Before
  review, the Foreman will record the planning-tip-to-builder-tip range so the
  Reviewer does not review this charter as implementation.
- **Role:** one Builder, High tier / high effort. This is an integrated
  schema/content/runtime/package/presentation build against a settled plan,
  not a prototype or review.
- **Scope and evidence-rung ceiling:** implement K1-C1 through K1-C5 and the
  complete K1-P/K1-N matrix in the active plan. The ceiling is production-
  shaped synthetic end-to-end evidence through `live_coordinate_run`; no real
  data, real workspace, owner attestation, or L3 claim.
- **Stop conditions:** stop if any accepted ADR or published historical file
  would need mutation; if a fully resolved schema example cannot be written
  honestly; if source identity needs an evidence/document key; if attachment
  v2 cannot preserve same-family row authority, atomic dispositions, or
  attachment-only failure; if package v9 needs a historical checksum rewrite
  or mixed producer graph; if the work requires governance interpretation,
  market discount, subtractive adjustments, another K-1 form/box, partnership
  basis, Schedule D, Form 8949, filing, real data, or unrelated UI changes; or
  if an unattributable base failure prevents focused verification.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/k1-interest-breadth.md`;
  `docs/adr/0015-1099-int-statement-instance-identity.md`;
  `docs/adr/0016-source-family-claim-and-composition.md`;
  `docs/adr/0026-taxable-interest-composition-and-line-2b.md`;
  `docs/adr/0027-adopted-content-manifests.md`;
  `docs/adr/0029-citation-resolution-contract.md`;
  `docs/adr/0031-real-data-residency-boundary.md`;
  `docs/adr/0032-contribution-boundary.md`;
  `docs/adr/0033-production-package-resolver.md`;
  `docs/adr/0036-schedule-attachment-ontology.md`;
  `docs/adr/0046-presentation-surface-contract.md`;
  `packages/content/tax/2025/interest-composition.json`;
  `packages/content/tax/2025/rule.form1040-line2b.json`;
  `packages/content/tax/2025/rule.attachment.schedule-b.json`;
  `packages/content/tax/2025/form1040.line-2b.form-field.v2.json`;
  `packages/content/tax/2025/package.core-calculations.v8.json`;
  `packages/content/tax/2025/published-packages.v3.json`;
  `packages/derivation/package_validation.py`;
  `packages/derivation/runner.py`; `packages/derivation/marshal.py`;
  `packages/derivation/live.py`;
  `packages/derivation/presentation_projection.py`;
  `tests/tax/test_track2_line2b.py`; `tests/test_dsbs_t2_schedule_b.py`;
  `tests/test_frrs_t3_resolver_bootstrap.py`;
  `tests/test_presentation_l2_integration.py`;
  `AGENTS.md#Schema Publication Protocol`; `AGENTS.md#Fixture Rules`; and
  `AGENTS.md#Data Safety Rules`.

Before editing, run the orientation command from `HEAD`, verify its resolved
commit against Git, and echo: the bounded Form-1065 box-5 scope; the synthetic
evidence ceiling; the immutable-history constraint; the five K1 contracts; and
every stop condition above.

## Authoritative specification

The active plan is the single source for:

- K1-C1 through K1-C5 contract text;
- the readiness inventory;
- K1-P1 through K1-P10 positive/boundary cases;
- K1-N1 through K1-N13 rejection/lifecycle cases; and
- the independent review attack checklist.

Do not silently weaken, merge, or substitute a case. If two cases share one
stronger test, name both IDs in the test and handoff. If a case is impossible
under the accepted runtime, stop and explain the precise stronger invariant or
missing capability; do not omit it.

The official tax routing sources are:

- `https://www.irs.gov/instructions/i1065sk1` — 2025 Partner's Instructions,
  Form 1065 Schedule K-1 box 5 to Form 1040 line 2b;
- `https://www.irs.gov/instructions/i1065` — 2025 Form 1065 line 5 and partner
  box-5 reporting; and
- `https://www.irs.gov/instructions/i1040sb` — 2025 Schedule B Part I all-
  taxable-interest rows and the existing threshold boundary.

The plan's paraphrases control the bounded implementation scope. A current web
page is grounding, not permission to add neighboring tax behavior.

## Readiness check before implementation

Before changing code, reconcile the plan's readiness table against `HEAD` and
record the result in the first handoff note or commit body. At minimum confirm:

1. the exact current citizens selected by core package v8;
2. every runtime/schema dispatch that recognizes only `attachment-rule.v1`;
3. every package schema enum that must add `attachment-rule.v2` without losing
   an existing admitted schema or role;
4. the v8/v3 release, registry, adoption, fixture-generator, and presentation
   consumers that must remain compatible;
5. the line-2b stable symbol's downstream consumers; and
6. the existing Schedule B tests whose box-1-only expectation is historical
   v1 behavior rather than the successor v2 contract.

If this reconciliation finds a required seam absent from the plan, stop and
report it before implementation. Do not leave it for the Reviewer to discover.

## Implementation work packet

### 1. Immutable schema successors and examples

Publish, without editing any existing schema:

- `attachment-rule.v2`, implementing K1-C3's itemization-authority,
  `row_sets`, per-family subtotal tie-out, and whole-part line tie-out shape;
- `artifact-package.v6`, preserving the v5 surface and adding
  `attachment-rule.v2` under the existing `attachment-rule` member role.

For each new schema, commit at least one hand-written, fully resolved,
obviously synthetic positive instance. Add isolated schema negatives for every
load-bearing structural constraint. Use
`packages.kernel.schema_registry.write_manifest` to append checksums. Inspect
the manifest diff: it may add the two new filenames and must not change or
remove any existing entry.

Add package-validation negatives, separate from schema negatives, for K1-N7
through K1-N9 and for wrong authority/line-symbol pairing. Schema validity by
itself is not evidence of semantic admission.

### 2. K-1 source and interest-composition successors

Implement K1-C1 and K1-C2 with additive versioned citizens:

- Form-1065 K-1 box-5 fact/closure bundle;
- dedicated source family and closure mapping;
- cited subtotal rule and citation citizen;
- interest composition v2;
- cited line-2b rule v2; and
- line-2b form-field content v3.

Use a nonnegative value schema for the box-5 source amount. Preserve logical
statement identity across corrections and distinct identity across separate
original K-1s from one partnership. Keep the non-form family predicate and all
historical interest citizens unchanged.

Extend package validation so a package-valid successor cannot omit the K-1
slot, closure read, input pin, value ref, or composition binding. Demonstrate
K1-N5 and K1-N6 against the real package-validation entrypoint.

### 3. Multi-family Schedule B successor

Implement `attachment-rule.v2` in every production path that currently special-
cases v1: loading/live selection, marshalling, evaluation, package validation,
presentation projection, and any resolver/schema admission surface found by
the readiness check. Keep v1 behavior byte- and semantics-compatible.

Publish Schedule B rule content v2:

- Part I uses composition authority over interest composition v2 and has one
  row set for each of the five declared families;
- Part II uses single-family authority over ordinary dividends;
- requirement threshold, Part III answers/branch, named obligation, and
  attachment symbol remain unchanged.

The evaluator must check each row set against its family subtotal before the
combined part against its line symbol. Both failures use the existing
`ITEMIZATION_TIE_OUT_VIOLATION`, block only Schedule B, and pin no fabricated
publication. Tests for K1-N10 and K1-N11 may use direct `RunContext` only
because an honest act log cannot produce the fabricated stale sides; all
ordinary integration cases use `live_coordinate_run`.

### 4. Package, release, coordinator, and lifecycle route

Publish core package v9 under artifact-package v6, published registry v4,
release v4, and a new synthetic adoption. Prefer a focused successor generator
that reads v8/v3 as immutable inputs and writes only v9/v4/new fixtures. If an
existing generator is extended, it must reproduce every historical output
byte-for-byte and the diff must contain only intended successors.

The package must resolve exactly one current K-1 family, composition v2,
line-2b rule v2, line-2b field v3, attachment rule v2, and every unchanged
consumer. Demonstrate mixed-graph refusal (K1-N12) and historical v8
compatibility (K1-P10).

Implement the complete source lifecycle through contribution, membership
transition, horizon closure, correction, late-member displacement, and rerun.
Do not add a direct fact-write or bypass contribution/admission.

### 5. Explanation and presentation

Generate production-shaped synthetic results through `live_coordinate_run`.
Prove that:

- line 2b and Schedule B show the K-1-derived result with exact citations;
- the line-2b successor's declared citation participates in the field -> rule
  -> resolved-citation chain;
- all five family closures and consumed row findings are represented in the
  appropriate lineage;
- blocked/rejected values never enter the presentation model; and
- one malformed K-1-derived section remains contained without blanking valid
  sibling sections (K1-N13).

Do not redesign the page or add an entry UI for K-1.

## Required evidence map

| Evidence group | Case IDs that must be named by tests |
| --- | --- |
| Identity and source admission | K1-P1, K1-P3, K1-P4, K1-N3, K1-N4 |
| Closure and line-2b composition | K1-P2, K1-P5, K1-N1, K1-N2, K1-N5, K1-N6 |
| Schedule B threshold and rows | K1-P6, K1-P7, K1-P8, K1-P9, K1-N7, K1-N8, K1-N9 |
| Tie-out failure containment | K1-N10, K1-N11 |
| Package/release compatibility | K1-P10, K1-N12 |
| Downstream explanation/presentation | K1-P1, K1-P2, K1-N1, K1-N2, K1-N13 |

Tests and docstrings must use these IDs so the Reviewer can establish matrix
completeness by direct search. A passing test without a traceable case ID does
not discharge the matrix row.

## Boundaries that must remain visible

- The supported K-1 is Form 1065 box 5 only. Do not create a generic
  `schedule-k1-interest` claim that could be read as Form 1120-S or Form 1041.
- The K-1 family is a fifth positive source, not a member of non-form interest.
- Partnership basis effects and attached-statement details are not computed.
- Schedule B v2 generalizes itemization; it does not alter the $1,500 trigger,
  Part III, FinCEN-114 naming, or attachment disposition semantics.
- Existing line-9 and downstream symbols should consume the stable line-2b
  symbol without unrelated successor content unless a concrete compatibility
  failure proves one is required.
- No market-discount or subtractive-adjustment mechanism is introduced.
- No historical file is regenerated into a different byte sequence.

## Verification before handoff

Create focused modules with these names unless a repository convention makes a
different name materially clearer:

```text
python3 -m unittest tests.test_k1_interest_breadth_contracts
python3 -m unittest tests.test_attachment_rule_v2
python3 -m unittest tests.test_k1_interest_breadth_integration
```

Run each established module once after the implementation stabilizes:

```text
python3 -m unittest tests.tax.test_track2_line2b
python3 -m unittest tests.test_dsbs_t2_schedule_b
python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m unittest tests.test_schema_registry
python3 -m mypy
git diff --check
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range 7066f26e02467a58ca6cb329666782b32bd7dd12..HEAD
```

If an established module is untouched and a new focused module strictly
subsumes it, report that fact rather than buying a duplicate broad run. Do not
rerun deterministic commands merely to confirm them. CI `verify` is the full-
suite gate of record.

## Handoff

Leave the worktree clean. Report:

- implementation commit(s) and the exact planning-tip-to-builder-tip range;
- files changed grouped by schema, content, runtime, package/release, fixtures,
  tests, and presentation;
- K1-P/K1-N case-to-test mapping, with no unaccounted row;
- schema-manifest diff inspection and historical-byte comparison;
- focused command results and the single repository-mypy result;
- any credited unchanged compatibility evidence; and
- every stop or residual issue without proposing out-of-scope implementation.

Do not review your own work, write the independent review, merge the branch,
begin a real-data exercise, or expand the milestone. The Foreman will charter
the exact-range independent review after taking custody.
