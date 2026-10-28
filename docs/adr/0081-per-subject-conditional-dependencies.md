# ADR 0081 — Per-Subject Conditional Dependencies

- Status: **accepted** (2026-10-27; owner-accepted after the dependent-tie-breaker final review)
- Tier: 2
- Date: 2026-10-27

## Context

ADR-0037 adopted `conditional_dependency_set` for return-level rules: the
evaluator reads the condition and reads declared members only when the condition
evaluates to true. If any member is absent, evaluation halts with
`DEPENDENCY_ABSENT` naming all missing active members in a single non-publication
walk; inactive members are neither read nor pinned.

In per-subject rules (rules declaring a `subject` pin, evaluated per subject row
via `packages/derivation/subject_dispatch.py`), this mechanism was unavailable
for facts keyed to the subject:

1. `packages/derivation/live.py` discovered per-subject rule inputs solely from
   the top-level `requires` list. Any fact type named only inside
   `conditional_dependency_set` members in `when` or `value` was never registered
   in `emission_only`, so candidate findings were never marshalled as
   `SourceFact` rows in `live_sources`.
2. `packages/derivation/subject_dispatch.py` bound only symbols listed in
   `requires` and checked presence upfront before evaluating `when`. Any absent
   symbol in `requires` immediately blocked execution with `DEPENDENCY_ABSENT`
   for that subject.

Consequently, every per-subject question had to be listed in `requires` and was
demanded unconditionally on every subject in the roster. In the dependent
tie-breaker (IRC § 152(c)(4)), this limitation would require asking all 8
subordinate tie-breaker questions on every contested child, even when
categorical rules (e.g. parent over non-parent) decide immediately. P0
investigated family gating with 8 distinct child rosters as a workaround without
engine changes (P0 repair section 9, Option 1), but showed that this forced the
filer to pre-evaluate the entire statutory decision tree simply to place the child
in the correct roster. On 2026-10-27, the owner authorized an engine change to
extend conditional dependencies to per-subject rules.

## Decision

1. **Declared expression.** Per-subject rules (`rule-artifact.v11` through
   `rule-artifact.v14`) may declare `conditional_dependency_set` nodes within
   their `when` or `value` expressions whose `members` include fact types keyed to
   the rule's `subject` that do not appear in `requires`. Existing schemas
   already admit `conditional_dependency_set` in expression trees; no new schema
   version is introduced.

2. **Per-subject input discovery.** When resolving run material in `live.py`, any
   fact type named as a `conditional_dependency_set` member in a per-subject rule
   that shares distinguishing identity keys with the rule's `subject` is added to
   `emission_only` if not already collected. This ensures candidate findings are
   emitted into `RunContext.sources` for scoping without being bound as run-wide
   scalars.

3. **Per-subject binding and isolation.** In `subject_dispatch.py`, for each
   subject:
   - Conditional dependency member names sharing the subject's identity keys are
     included in candidate scoping (`other_names`), ensuring unasserted types
     produce an empty scoped set and overwrite local sources maps.
   - When present for the subject, a conditional member is scoped by identity
     keys and bound into `local_symbols`, `symbol_pin`, and `fact_types` for that
     subject only.
   - When absent for the subject, the member is left unbound. It is not added to
     the upfront `absent` list. Crucially, per-subject types are never bound from
     run-wide symbols or another subject's findings (preserving the per-subject
     binding rule).
   - If an active condition subsequently causes the evaluator to read an unbound
     member via `ref`, the evaluator raises `EvalBlocked(BLOCK_ABSENT, ...)`,
     and the rule blocks with `DEPENDENCY_ABSENT` naming the missing member(s)
     for that subject.
   - If the condition is false, members are never evaluated, never named in
     missing lists, and never pinned.
   - When a member is present and the condition is true, the member is read and
     its specific finding is pinned.

4. **Invariance of `requires`.** The meaning of `requires` is preserved: every
   symbol listed in `requires` remains unconditionally required on every subject
   prior to evaluating `when`. If a member of a `conditional_dependency_set` is
   also listed in `requires`, it behaves as required on every subject.

5. **Domain guard.** ADR-0038's `{yes, no}` domain guard for categorical member
   fact types continues to apply unchanged.

## Production conditions

1. Amend `packages/derivation/live.py` to discover per-subject member references
   inside `conditional_dependency_set` nodes in `when` and `value` expressions and
   include them in `emission_only`.
2. Amend `packages/derivation/subject_dispatch.py` to scope and bind per-subject
   conditional dependency members when present and leave them unbound when
   absent, strictly preventing cross-subject or run-wide scalar leakage.
3. Verify that `rule-artifact.v14` and existing validation tools accept the shape
   without new schema versions.
4. Provide comprehensive unit and coordinator tests through `live_coordinate_run`
   on a synthetic two-subject surface proving inactive non-pinning, active
   absence blocking, active presence pinning, cross-subject isolation, sibling
   non-satisfaction, supersession re-derivation, and `requires` mutation
   invariance.
5. Prove that the full derivation and tax test suites continue to pass with zero
   regressions.

## Consequences

- The dependent tie-breaker for 2025 (Track 1) can evaluate all statutory
  branches sequentially on a unified child roster, asking subordinate questions
  only when reached on that child's path.
- Future per-subject rules gain honest conditional completeness without roster
  fragmentation or UI-side legal pre-classification.
- The per-subject binding rule is maintained: no per-subject answer ever leaks
  between subjects or to/from return-level symbols.

## Alternatives considered

- **Family gating (P0 repair section 9, Option 1).** Partitioning into 8
  separate rosters by branch. Rejected because it shifts the entire tie-breaker
  classification into the filer's roster-placement decision, creating fragile
  user-facing pre-adjudication.
- **Unconditional `requires`.** Requiring all tie-breaker questions on every
  child. Rejected because off-path questions (e.g. AGI comparisons when parent
  status decides) must not block or be demanded from taxpayers.
- **Top-level conditional requires in schema.** Adding a top-level conditional
  requires syntax. Rejected under ADR-0037 because expression-level
  `conditional_dependency_set` already cleanly encapsulates conditional
  dependencies within declared boolean logic.

## Links

- Extends: ADR-0037, ADR-0038
- Builds on: ADR-0076, ADR-0077, ADR-0078
- Evidence and Design: `docs/phases/engine-breadth/milestones/dependent-tie-breaker-evidence/p0-verify-and-design.md`
