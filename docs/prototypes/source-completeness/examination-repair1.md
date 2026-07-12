# Examination: Repair Pass 1 — SC-P1 Rung-2 Enforcement

Date: 2026-07-12. Original it1 builder (deliberate continuity), rung 2
(validator/resolver mutations only), under `charter-repair1.md`. Branch
`prototypes/source-completeness/repair1`; artifacts under `repair1/`.

## What was built

An executable resolver boundary that projects source-set closed membership from
closure findings + an adopted mapping, implemented **independently for both
surviving authority shapes** and exercised by a mutation suite:

- `repair1/resolver.py` — shared admission core `admit_current_true`; two shape
  resolvers `resolve_A` (dedicated mapping citizen, exhibit it1) and `resolve_B`
  (embedded adopted-rule parameter, exhibit it2); the frozen `ResolvedMembership`
  carrier and `env_closed_sets` bridge; three named mutants.
- `repair1/test_resolver.py` — 15 cases, every admission case run against **both**
  shapes via `subTest`.

Self-contained: imports nothing from `packages/`; does not execute the
production evaluator (checks 5-6). Stands in for the real seam it will replace —
`evaluator.py` collect layer 2 (`source_set in env.closed_sets`) fed today by
caller-supplied `RunContext.closed_sets` (`runner.py`, `runners/derive.py`) —
which is grounded by reference only, never imported.

## Commands and results

```
$ cd docs/prototypes/source-completeness/repair1
$ python3 -m unittest -v test_resolver
... 15 tests ... OK   (Ran 15 tests in 0.001s)
```

All 15 pass (Python 3.14). Evidence: the verbose run lists each case; the
mutation matrix cases assert both the correct verdict AND the mutant's divergent
verdict, so a green suite is a positive kill record, not silence.

## Measured cases (charter deliverable 2 + checks 1, 4) — both shapes

| Case | Shape A | Shape B | Test |
|---|---|---|---|
| exactly one current literal-`true` → admitted, pin = that finding | admit | admit | `test_one_current_true_admitted_with_exact_pin` |
| current `false` → blocked | block | block | `test_current_false_blocked` |
| absent (no finding) → blocked | block | block | `test_absent_blocked` |
| displaced historical true (superseded by current false) → blocked | block | block | `test_displaced_true_then_false_blocked` |
| re-attested true (old true superseded by new true) → admitted, pin = **new** finding (`clo-new-true`, v2) | admit | admit | `test_displaced_true_then_true_pins_the_current_finding` |
| truthy-but-not-`True` (`1`, `"true"`, `"yes"`) → blocked | block | block | `test_truthy_but_not_literal_true_blocked` |
| two current matching findings → ambiguous → blocked | block | block | `test_two_matching_current_findings_block_both_shapes` |
| duplicate mapping entries (A) / duplicate adopted rules (B) for one family → blocked | block | block | `test_A_duplicate_mapping_entries_block`, `test_B_duplicate_adopted_rules_block` |

## Negative results disclosed (every one)

- **Presence-only mutant admits `false`.** `admit_presence_only` (the it4 defect:
  admits on presence of one current finding, never reads value) admits the family
  where `admit_current_true` blocks it, for both shapes — `killed` by the
  false-closure case (`test_presence_only_mutant_killed_by_false_closure`). This
  is the measurement round 1 lacked (governance C1 / adversary A1).
- **Currency-blind mutant resurrects a displaced true.** `admit_presence_any_history`
  scans superseded findings and admits the historical true; `admit_current_true`
  reads only the current (false) finding and blocks — killed by the
  displaced-true case (`test_currency_blind_mutant_killed_by_displaced_true`).
- **Truthy mutant admits `1`.** `admit_truthy` admits any truthy value; killed by
  the non-literal-true case (`test_truthy_mutant_killed_by_non_literal_true`).
- **A6 stale-pin, addressed for both shapes:** ambiguous authority *blocks the
  family entirely* rather than letting one pin overwrite another — A via
  duplicate-entry detection, B via `admit` returning `AMBIGUOUS` on two matching
  findings and a divergence guard on duplicate adopted rules. So the pin that
  explains a zero is always the pin admission used.

## Pre-declared checks

1. **No mutation accepts false, absence, displacement, or ambiguity.** MET —
   rows 2-4, 7-8 above; `admit_current_true` returns `None`/`AMBIGUOUS`.
2. **Presence-only mutants fail deterministically for both shapes.** MET — the
   mutation matrix; deterministic (no randomness, fixed fixtures).
3. **No caller-controlled bare set can augment resolved membership.** MET —
   `ResolvedMembership` is frozen (`test_membership_is_frozen`), `closed_families`
   is a derived property with no setter, and `env_closed_sets` has arity 1 with
   no caller-set parameter (`test_env_closed_sets_takes_no_caller_set`); there is
   no union-with-caller path (`test_bare_family_string_needs_a_finding_to_exist`).
4. **The exact admitted closure finding survives for pins.** MET — `pin_for`
   returns the exact `finding_id`/`version`; the re-attested-true case proves the
   pin is the *current* finding, never the displaced one.
5. **Prototype-only; production evaluator not executed.** MET — no `packages/`
   import; the resolver is a standalone stand-in.
6. **SC-P2, SC-P3, SC-D1, production schemas, coverage untouched.** MET — only
   two files under `repair1/` added; no edits elsewhere.

## Disposition — one call

**SC-P1 affirmative-only admission is settled at rung 2, at the resolver
boundary, for both authority shapes.** The single charter question is answered
*yes* for the boundary: each shape projects membership only from one exact,
current, literal-`true` finding, rejecting false/absent/displaced/ambiguous
authority and caller injection, and retains the exact finding for pins — and a
presence-only adapter is not merely absent by intent but is *killed by a test*.

**Rung 3 is still needed for one residual, stated precisely as a finding (not
authorization):** this measures the resolver *in isolation*. It does not prove
the resolver is the *sole* writer on the **real two-layer path** — the A2 seam.
Today `evaluator.py` L2 reads a bare `frozenset[str]` and `RunContext.closed_sets`
is caller-supplied; nothing here exercises a `collect` check consuming
`env_closed_sets(resolved)` with that caller field removed. Closing it needs
rung 3: a throwaway evaluator running a *copy* of the real two-layer check over
resolver output, with the caller seam eliminated so injection is unrepresentable
end-to-end. That, plus the production condition (remove/for­bid
`RunContext.closed_sets` — milestone Track 2 per round-1 triage), is what remains.
No shape is preferred here; both survive rung 2 equally, so shape selection stays
a committee/ADR decision, not a builder call.

## Handoff

Rung-2 evidence complete for the repair pass; stop condition reached (a need for
the real evaluator is recorded above as a rung-3 finding, not taken). Commit on
this branch only; not merged, tagged, or deleted — integration and any rung-3
authorization are the foreman/owner's. SC-P2 rekeying, SC-P3 non-convergence,
and SC-D1 remain deferred exactly as round-1 triage left them; nothing here
touches them.
