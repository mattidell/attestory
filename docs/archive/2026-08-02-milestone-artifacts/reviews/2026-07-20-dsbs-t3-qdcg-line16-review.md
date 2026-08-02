# Review: Track 3 — Line 16 under D2

Date: 2026-07-20

Branch: `track/dsbs-t3-qdcg-line16`

Base: `ebec569`

## Verdict

**not ready**

The Track 3-specific checks and targeted tests pass, but the required full
verification battery is not green. The two failing tests are branch-caused,
not pre-existing at `ebec569`; see F1.

## Scope reconciliation

The four implementation commits are present in the chartered order:
`3b3db78`, `a0574a5`, `7732cc5`, and `f12e7a1`. The literal
`ebec569..HEAD` range also contains `d858172`, which adds the author-
independent review charter. I treated that as review-input administration,
not as Track 3 implementation. No implementation file outside the chartered
delta was relied on as an authoring-session claim.

## Check results

### Check 1 — declared-absence citizens and domain-guard scope

Pass, with the scoped guard reviewed as a judgment call.

`qdcg.bundle.json:2-30` is a `bundle.v2`; both citizens are nested
`fact-type.v2` members, each has the exact categorical `{yes, no}` domain,
and neither has an optional default. This matches the bundle-adopted shape in
`scheduleb.bundle.json:1-30`; they are not package-level bare members.

`package_validation.py:804-857` checks a CMDN member only when the same v3
rule names that member through `category_literal`. The negative tests are
executed in `test_dsbs_t3_qdcg_declarations.py:171-211` for a conforming
domain, boolean, open string, non-yes/no enum, absent fact type, and the
committed QDCG bundle.

The scoping is not vacuous. The Track 0a live fixture uses numeric member
fact types at `tests/derivation/test_conditional_multi_dependency.py:222-230`
and exercises them through `live_coordinate_run` at `:285-301`. A blanket
yes/no rule would reject that generic numeric-member case. Conversely, both
ADR-0038 citizens in the line-16 rule are categorical reads at
`rule.form1040-line16.v2.json:81-114`, so the scoped guard covers every
ADR-0038 case implied by the committed rule. I found no ADR-0038 case that
requires checking a CMDN member which is not also a categorical read.

### Check 2 — v3 successor and package pin

Pass. The outer guard at `rule.form1040-line16.v2.json:43-120` starts with
`conditional_dependency_set` and places it unconditionally first. The value
branches at `:121-295` retain the ordinary bracket computation for the
qualified-zero branch and the worksheet ladder for the active branch. The
rule is a single `rule-artifact.v3` producer at `:1-4`; package v6 has exactly
one line-16 member, at
`package.core-calculations.v6.json:184-187`, and has no conflict selector.

The schema admits the node only in v3: v2 has no such definition, while
`rule-artifact.v3.schema.json:45` defines it with a condition and non-empty
ref-only members. No new evaluator or custom blocked/walk vocabulary was
added in this delta.

### Check 3 — QDCG ladder and qualified-zero reduction

Pass. The operation set in the successor is closed and pre-existing: the
new rule uses `add`, `all`, `any`, `bracket_fold`, `categorical_compare`,
`category_literal`, `choose`, `compare`, `ref`, `round`, and `subtract`;
`max` remains available but is not needed by this expression. The evaluator
implementation was not changed by this delta; the operation implementations
predate it, and the line-16 rule introduces no new operation name.

I reran the qualified-zero live case from the authoritative act log and
inspected the line-16 input pins. Neither declaration identifier appeared;
the recorded pins were the ordinary-bracket inputs and existing operation
semantics. The first-node false-condition behavior is independently visible
at `evaluator.py:204-223`, especially `:211-212`.

### Check 4 — bidirectional admission-locus interlock

Pass. `schema_registry.py:65-74` defines a generic registry collection with
no tax-domain literal in kernel behavior. `findings.py:242-287` reads only
the registry-declared fact types and field, evaluates the fully updated state,
and raises before the successor state can be observed. The tax loader adds
exactly one declaration/signal rule at `packages/tax/loader.py:65-76`, mapping
the recorded signal to the recorded-box field that raises it.

The dedicated tests passed in all three orders. Their assertions and the
raise sites are at `test_dsbs_t3_contradiction_interlock.py:105-113`
(declaration first), `:130-138` (signal first), and `:151-191`
(both same-batch orders). The never-recorded assertion is at `:141-149`.

### Check 5 — structural no-reach-around

Pass. A direct repository grep of
`packages/content/tax/2025/rule.form1040-line16.v2.json` found neither the
capital-gain signal nor the recorded-box fact type. The committed structural
test at `test_dsbs_t3_line16_coordinator.py:452-475` derives the forbidden
symbols from the dividend-universe citizen and checks the same file.

### Check 6 — `marshal.py` collateral change

Pass and load-bearing. The exact additive hunk is
`packages/derivation/marshal.py:53-100`; only v3 rules add refs found in
`when` and `value`, while v1/v2 rules still return their `requires` surface.
An independent live-run experiment using the pre-change requires-only helper
removed the two declaration inputs from the v3 run; restoring the helper
allowed the declaration-aware line-16 path to execute. A comparison over all
committed v1/v2 rule citizens showed identical required-symbol results.

This is necessary for deliverable 2’s live successor path. The admission
interlock in Check 4 is independently exercised at kernel admission and does
not rely on marshal behavior; the collateral change therefore does not claim
to replace that mechanism.

### Check 7 — package versioning and derived registries

Pass. v6 is distinct from v5 and the adoption fixture uses the next synthetic
scope year in `adopt-core-v6-current.json:11-25`. The v6 entrypoints include
the successor rule and QDCG bundle at
`package.core-calculations.v6.json:23-55`; the preferential parameter is
reached through the existing table-reference adjacency. No adjacency-walker
change appears in the branch delta.

The generator outputs match all committed generated files byte-for-byte.
The package checksum recomputes, the package registry contains the v6 entry,
and the release registry hash matches the committed release fixture.

### Check 8 — six authoritative golden classes

Pass. `rg 'RunContext\\('` finds exactly one hit at
`test_dsbs_t3_line16_coordinator.py:414`, inside the explicitly
non-substitutive supplementary class documented at `:390-396`. The six
authoritative classes use `_run_tmp` → `_run` → `live_coordinate_run` through
`:209-214`, with bodies at `:230-387` covering the qualified-positive,
qualified-zero, both-absent, each single-absent case, both present-yes cases,
and declaration supersession. The supplementary evaluator tests at
`:432-449` cover the arithmetic comparison that the live report deliberately
does not carry.

The three Track 3 test modules—declaration admission, coordinator goldens,
and contradiction interlock—were rerun independently: 31 tests, all passed.

### Check 9 — boundary and data safety

Pass. The content diff adds only the declared Schedule D citizen, not
Schedule D computation. The line-16 rule contains no closure mapping, live
workspace integration, or recorded non-composable input. No evaluator
operation, result shape, or new blocked/walk vocabulary was added. New
fixtures use synthetic `demo.*` / `demo-*` identifiers. The branch diff and
working-tree status contain no `tools/scaffold_live_acts.py` or
`workspace-seed/` change.

### Check 10 — verification battery and base comparison

Not pass; F1 is blocking.

Independent battery results:

- `.venv/bin/python3 -m unittest`: 541 tests, 2 failures.
- `.venv/bin/python3 -m mypy`: pass.
- `.venv/bin/python3 tools/governance_lint.py`: pass.
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD`: pass with
  no findings.

The two failing assertions are in
`tests/test_frrs_t3_resolver_bootstrap.py:216-230` and
`tests/test_frrs_t4_w2_live_integration.py:367-379`. Both targeted tests pass
when run at base `ebec569`; therefore the failures are not pre-existing.

## Findings

### F1 — Check 10: adding the new rule file breaks two existing substitution probes

Severity: blocking.

At base, both affected tests pass. On this branch, both fail because the
tests copy the content directory and mutate the first result of
`glob("rule.*.json")` (`test_frrs_t3_resolver_bootstrap.py:219-225` and
`test_frrs_t4_w2_live_integration.py:369-376`). The new
`rule.form1040-line16.v2.json` introduced by `7732cc5` is first in the branch
enumeration, but it is not a member of the interest package selected by
those probes. The mutation therefore targets an unrelated file and the
expected resolver rejection is not observed.

This is a real regression in the required battery, not a base failure. The
implementation branch is not ready until the affected probes select their
intended package member deterministically or the equivalent existing test
contract is otherwise restored. This review does not change those tests.
