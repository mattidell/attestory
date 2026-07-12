# Examination: Repair Pass 4 — Single Evaluation Entry

Date: 2026-07-12. Original it1 builder (deliberate continuity). Evidence level:
focused throwaway refinement; no production import, edit, or execution. Branch
`prototypes/source-completeness/repair4`; artifacts under `repair4/`. **Shape A
only**; shape B stays rejected and is not restored.

## Correspondence to the round-3 finding

`reviews/round-3-adversary.md` found repair3 *validated* carriers but still
offered bypasses: alternate public callables (`run_rule_with_carrier`,
`run_rule_trusting`, the raw repair2 `Env`/evaluator) and duck typing — `Env`
accepted any object with `closed_families`/`pin_for`. Validation was reachable
around, not just through. This pass removes every entry but one.

## The supported-surface contract

`repair4/surface.py` exposes exactly **one** public callable, `compute(rule,
source_rows, mapping, findings)`. It resolves shape-A authority internally
(`_resolve_authority` → repair1 `resolve_A`) and consumes it immediately before a
faithful copy of the two-layer `collect`, as one operation. It accepts **no**
external authority carrier, closed-family set, raw environment, validator
callback, or alternate evaluator, and re-exports none: `__all__ == ["compute"]`,
and the only public `FunctionType` on the module is `compute`. The resolver is a
private import (`_resolver`); `_collect`/`_pins`/`_resolve_authority` are
underscore-private internal steps, not public paths.

**Stated limit (not overclaimed).** Python privacy is a convention, not a
security boundary. The contract modeled is that the production surface *exposes
and dispatches only* this validated entry. The prototype measures that the
selected surface offers no alternate reachable entry; it does not (and cannot)
prove language-level inaccessibility.

## What was built

- `repair4/surface.py` — the single-entry runtime module (self-contained; the
  faithful two-layer `collect` + pins inlined as privates; resolution delegated
  to the private repair1 resolver).
- `repair4/test_surface.py` — 12 cases. The duck-carrier, direct-raw, and
  presence-only mutants exist **only** in the test file, never in the runtime
  module (charter deliverable 2/4).

## Commands and results

```
$ cd docs/prototypes/source-completeness/repair4
$ python3 -m unittest -v test_surface
... 12 tests ... OK   (Ran 12 tests in 0.001s)
```

(The surface-inspection test earlier caught `dataclass` leaking as a public
callable via the import; fixed by aliasing it private — the check is real.)

## Measured cases (all through `compute`)

| Case | Result | Test |
|---|---|---|
| true closure → zero + exact pin (`clo-true`@v5) | publish | `test_true_publishes_zero_with_exact_pin` |
| present members → 34, **no** closure pin, 2 input pins | publish | `test_present_members_omit_closure_pins` |
| false / absent / displaced / truthy-int / truthy-str / ambiguous | **block** | `test_negatives_block_through_publication` |
| duplicate mapping entries | **block** | `test_duplicate_mapping_entries_block` |
| stale-first/current-second (both orders) → pin is successor | publish | `test_stale_first_current_second_pins_successor` |
| pin/mapping values equal the exact inputs passed | publish | `test_inputs_are_the_exact_values_used_for_resolution_and_pins` |
| only public function is `compute`; `__all__ == ["compute"]` | n/a | `test_only_public_function_is_compute` |
| no raw evaluator/resolver/carrier re-exported | n/a | `test_no_raw_evaluator_or_resolver_re_exported` |
| `compute` signature accepts no authority/carrier/env/closed-set param | n/a | `test_compute_signature_accepts_no_authority_object` |

## Negatives and rejected-path mutants disclosed

- Six value/currency/ambiguity negatives block through publication, plus
  duplicate-entry block — same guarantees as prior passes, now behind one entry.
- **Duck carrier has no way in**: a `DuckAuthority` with `closed_families`/
  `pin_for` cannot be supplied — `compute` takes no such parameter; passing it
  positionally or by keyword raises `TypeError`
  (`test_duck_carrier_has_no_public_parameter_to_enter`).
- **Direct-raw path is private, not public**: a test-local mutant reaches
  `surface._collect` with a fabricated admitted-map and it would zero — proving
  exactly why `_collect` stays private. No public entry supplies that map;
  `compute({}, [])` blocks. The mutant lives in the test, not the module.
- **Presence-only mutant is test-local**: the presence-only resolution variant
  admits a false closure in the test, while `compute` blocks it — the mutant is
  never exported from `surface.py`.

## Final call

**The selected shape-A prototype surface now exposes one supported calculation
entry with no reachable bypass measured.** Authority is derived and consumed
internally from declared inputs; there is no carrier to fabricate, no duck object
that fits a parameter, no alternate evaluator or validator hook, and no re-export
of the private resolver. Combined with repair1 (admission), repair2 (sole use on
the real two-layer path), and repair3 (validated construction), the SC-P1 shape-A
enforcement chain is executable end to end and, at the prototype level, offers a
single entry — sufficient to draft the SC-P1 ADR against a *dispatch-only-the-
validated-entry* contract.

**Residual — production-only routing facts this prototype cannot model** (named,
not absorbed):

1. **Production dispatch.** The prototype shows *this module* has one entry; it
   cannot prove the production runner exposes and routes **every** derivation
   through the validated entry and retains no legacy `RunContext.closed_sets`
   constructor or second evaluator. That is milestone **Track 2** (remove the
   caller seam; single dispatch), verifiable only in production code.
2. **Adopted-mapping identity.** `compute` trusts the passed `mapping`; in
   production the mapping must be the pinned, adopted artifact (Article 4) and
   the run re-derives against the adopted version — **Track 2/3**.
3. **Persisted displacement.** Withdrawal-driven displacement of a published zero
   across a real run (ADR-0010 end-to-end) is rung-4 / **Track 3**, not modeled.

## Handoff

No-bypass reachability measured for the selected surface; stop condition reached
(residuals are production-only routing facts, none absorbed). SC-P2, SC-P3,
SC-D1 remain deferred; shape B stays rejected. Committed on `repair4` only — not
merged, tagged, or deleted. Integration, exhibit tagging, and the SC-P1 shape-A
ADR draft are the foreman/owner's.
