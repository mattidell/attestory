# Examination: Repair Pass 2 — SC-P1 End-to-End Sole-Writer Check

Date: 2026-07-12. Original it1 builder (deliberate continuity). Evidence level:
throwaway evaluator (rung 3). Branch `prototypes/source-completeness/repair2`;
artifacts under `repair2/`.

## What was built

A faithful COPY of the production two-layer `collect` path — collect → sum →
publish with pins — wired **only** to repair1's resolved-authority carrier, and
exercised end-to-end (through publication) for **both** authority shapes.

- `repair2/prototype_eval.py` — `Env` (no `closed_sets` field; layer-2
  membership derived from a repair1 `ResolvedMembership`), `collect` (faithful
  copy of `evaluator.py:107-119`), `build_pins` (copy of `pins_for` rule+input
  pins plus the repair1 closure-authority pin), `run_rule`, and one end-to-end
  `run_rule_caller_union` mutant.
- `repair2/test_end_to_end.py` — 11 cases, every case asserted across both
  shapes via `subTest`; imports repair1's `resolver` as the sole authority
  source (not re-implemented).

Self-contained: no `packages/` import; the production runner/evaluator is never
executed (check 6).

## Commands and results

```
$ cd docs/prototypes/source-completeness/repair2
$ python3 -m unittest -v test_end_to_end
... 11 tests ... OK   (Ran 11 tests in 0.004s)
```

## Correspondence to the real two-layer check (check 1)

`collect` copies `evaluator.py:107-119` line-for-line in structure: **layer 1**
`rows = sources.get(name, [])`; nonempty → `[Decimal(v) ...]` (closure never
consulted). **layer 2** empty → `source_set is None or source_set not in
members` → block `SOURCE_SET_NOT_CLOSED`, else return `[]`. `add` fold copies
`evaluator.py:134`. `build_pins` copies `pins_for` rule + per-collect input
pins (`runner.py:143-154`).

**Declared deviations** (only these): (1) the `round` wrapper is omitted —
rounding never gates layer 2; (2) adoption/governance pins omitted — outside the
closure question; (3) the one substantive change under test — membership is not
a settable `frozenset[str]` (`env.closed_sets`) but is **derived** from
`ResolvedMembership` via `env_closed_sets`. Deviations 1-2 are immaterial to the
measured property; deviation 3 *is* the property.

## Measured cases (both shapes, through publication)

| Case | Result | Test |
|---|---|---|
| present members → aggregate 34, **no** closure pin, 2 input pins | publish | `test_present_members_publish_without_consulting_closure` |
| empty + one current literal-`true` → zero | publish | `test_empty_publishes_zero_only_for_current_true` |
| false / absent / displaced / truthy-`1` / truthy-`"true"` / ambiguous | **block** | `test_negatives_block_through_publication` |
| zero pins the exact current-true finding (id+version) | publish+pin | `test_zero_pins_exact_current_true_finding` |
| re-attested true pins the **new** finding, not the displaced one | publish+pin | `test_reattested_true_pins_new_not_displaced_finding` |
| duplicate mapping entries (A) / duplicate adopted rules (B) | **block** | `Ambiguity.*` |
| `Env` has no caller `closed_sets` field; passing one is a `TypeError` | n/a | `test_env_has_no_caller_closed_set_field` |
| no construction path admits a bare wanted family | **block** | `test_no_construction_path_admits_a_bare_family` |

## Negative results disclosed (every one)

- **Six negatives block through publication, not merely at resolver output**
  (check 3): false, absent, displaced-true, truthy-int, truthy-str, ambiguous —
  each reaches `run_rule` and raises `SOURCE_SET_NOT_CLOSED`, so nothing
  publishes. Verified for A and B.
- **Caller-union mutant killed by injection** (deliverable 4): with no resolved
  authority for the family, the faithful path blocks; `run_rule_caller_union`
  unions a caller `{FAM}` into layer-2 membership and publishes a zero — the
  divergence is the kill. That injected zero also carries no closure pin, i.e.
  it cannot explain itself, a second reason it is illegitimate. Both shapes.
- **Presence-only resolver mutant killed by false closure** (end-to-end): a
  membership resolved with `admit_presence_only` admits a *false* closure and
  the faithful evaluator then publishes a zero, where the correctly-resolved run
  blocks. Both shapes. This carries the repair1 unit-level kill through to
  publication.

## Pre-declared checks

1. Copied L1/L2 semantics preserved; deviations listed above. **MET.**
2. Resolved authority is the sole source of membership **by construction** —
   `Env` exposes no settable membership; `closed_families` is a derived
   property. **MET.**
3. Every repair1 negative blocks through publication. **MET.**
4. Successful empty-source publication pins the exact current-true finding.
   **MET.**
5. Both shapes receive the same cases and assertions (`subTest` over `SHAPES`).
   **MET.**
6. No production import, mutation, schema, workspace, persistence, or coverage.
   **MET.**

## Final call

**SC-P1 affirmative-only enforcement is settled at the executable-path level for
both surviving mapping shapes.** The question repair1 left open — is the
resolver the *sole possible writer* when the real two-layer check consumes its
output — is answered *yes* against a faithful copy: membership is unrepresentable
except through resolved authority, injection is a `TypeError` or a demonstrably
illegitimate mutant, and the empty-source zero carries the exact closure finding
for explanation. Both shapes pass identically, so **shape selection remains a
committee/ADR decision, not a builder call**; the SC-P1 evidence chain (paper
it1/it2 → repair1 resolver → repair2 path) is sufficient to draft the ADR.

**Residual uncertainty — production-only behaviors the faithful copy cannot
represent** (not prototype gaps; milestone implementation conditions):

1. Production must actually **replace `RunContext.closed_sets`** with this
   resolver-built environment and prove no *other* `Environment` caller retains
   a bare-set seam (round-1 triage → milestone **Track 2**). The copy proves the
   design is sole-writer-*capable*; only production removal proves no seam
   survives system-wide.
2. Production **`pins_for` must add the closure-authority pin**; today it pins
   present collected findings only. The copy models the addition; production
   must implement it (Track 2/3).
3. The **persisted displacement cascade** of a published closure-backed zero when
   the closure finding is withdrawn (ADR-0010 currency across a real run) is
   rung-4 / **Track 3** integration, deliberately not represented here.

## Handoff

Rung-3 evidence complete; stop condition reached (residuals name production-only
behaviors, none absorbed). SC-P2 (rekeying), SC-P3 (non-convergence), SC-D1
remain deferred as round-1 triage left them. Committed on `repair2` only; not
merged, tagged, or deleted — integration, exhibit tagging, and the SC-P1 ADR
draft/shape selection are the foreman/owner's.
