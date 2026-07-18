# Foreman findings: Track 4 live path cannot publish (three defects)

Date: 2026-07-18. Author: foreman, owner-directed session. Status: **recorded,
repair paused by owner decision** — no repair has merged. Evidence below is
synthetic only, from a scaffolded dry run in a scratch workspace (zero
personal data; the owner's real run was not attempted).

## Root cause (common to all three)

Track 4's synthetic goldens never drove `live_coordinate_run` with facts on
record: the coordinator golden ran an empty act log, and closure/rule goldens
hand-built `RunContext`/`ClosureFindingRecord` objects, bypassing the
marshalling path a real run uses. The missing golden class is: **a coordinator
run from an authoritative act log with contributed facts, asserting that lines
publish and the paired record commits.**

## F1 — `derivation-record.v2` pin shape lags `rule-artifact.v2` (repaired on this branch, unmerged)

Blocking. The record schema's closed pin `$def` rejects `role: "parameter"`
and the `origin` marker, both ratified in `rule-artifact.v2`'s pin `$def`
(which *requires* `origin` on input pins). Consequence: any live run with at
least one marshalled finding crashes with `SchemaValidationError` when the
completion record is appended — after the `started` record, leaving an open
run. Repair (implemented on `repair/frrs-t4-record-pin-origin`, verified
end-to-end): align the record pin `$def` with `rule-artifact.v2` (add
`parameter` role; admit `origin` with the input-pin conditional) and
regenerate the `published.json` row. Strictly widening; the release chain
attests only the package registry, so no release/adoption cascade. In-place
widening chosen over a `derivation-record.v3` successor; owner may veto at
review.

## F2 — no `rounding.convention` fact type exists; every line blocks on the live path

Blocking. `package.core-calculations@v2` declares `rounding.convention@v1` as
a **required** `input_binding` and every line rule requires the symbol, but no
adopted vocabulary bundle publishes that fact type. A contribution asserting
it is rejected (`finding references unknown fact`), so it can never enter
record state, and every rule blocks `DEPENDENCY_ABSENT: rounding.convention`
forever. Goldens masked this by hand-feeding
`InputFinding("rounding.convention", "half_up", ...)`. Repair direction:
publish the fact type as immutable v3-cycle content (vocabulary bundle,
package, registry, release, adoption pins regenerated via
`tools/generate_frrs_t4_content.py`, following the v2 precedent), or —
owner-level product decision — reclassify rounding as an adopted
default/parameter rather than a user-contributed fact.

## F3 — W-2 v2 closure fact type cannot carry its mapping's horizon key

Non-blocking for an owner holding W-2s; blocking for the empty-set case.
`tax.us.2025.w2.source-closure@v2` declares only a `tax-year` identity key,
while `closure-mapping.w2.v2` names `closure_horizon_key: "family-horizon"`.
An asserted W-2 closure therefore cannot resolve (unknown fact) and, if it
could, could not marshal. Present W-2 wages aggregate and publish without
closure authority (ADR-0014), so line 1a is unaffected when at least one W-2
exists. Repair direction: add the `family-horizon` entity key to the closure
fact type in the same v3 cycle.

## Dry-run evidence (synthetic scratch workspace)

With F1 repaired, a scaffolded act log (vocabulary adoptions, five horizons,
four interest closures, filing status `single`, core-v2 package adoption)
resolved through the verified release chain, marshalled, executed, wrote the
paired records and the declared report: `stop: saturated`, 12 dispositions —
standard deduction and line 12 published; all other lines blocked
`DEPENDENCY_ABSENT: rounding.convention` (F2), and line 2b additionally on
the four interest subtotals it feeds from.

## Interim tooling note

`tools/scaffold_live_acts.py` (deliberately uncommitted working-tree helper,
owner decision) scaffolds a live workspace act log, templates, runner, and a
renumber/pre-flight mode; its pre-flight is what surfaced F3 and its dry run
what surfaced F1/F2. Promotion to a committed tool is a later decision.

## Milestone consequence

Exit criterion 1 (the owner's real run publishes lines 1a/2b/9/11/12/15/16)
is **not currently achievable** on `main`. The Track 4c repair charter
(`charter-2026-07-18-frrs-t4c-live-path-repair.md`) defines the fix; the
owner dispatches the review seat per ADR-0034 when ready.
