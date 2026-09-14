# P3 R7 feasibility probe — findings

Probe: `probes/feasibility.py`. Ran through
`packages.derivation.evaluator.evaluate` and
`packages.derivation.pairing_dispatch.evaluate_pairing_scoped_rule`.
Presentation uses `build_presentation_model` over synthetic publications
and dispositions. It does **not** call `live_coordinate_run`, write a
durable presentation file, or execute `citation-walk.v1.html`. Synthetic
`demo.*` only. Exit 0; assertions held.

## Outcome: `needs-owner-decision`

Not softened. 2a and 2b are not discharged. P3 is a **decision-ready
partial design**: the selected eligible-student direction survives; no
production path exists.

`VALUE_EXPR` is a **partial mechanics witness**. It reads institution
eligibility and the keyed numeric half-time threshold. It does **not**
read program classification. A successful `evaluate()` is not proof that
the whole selected (C) predicate ran.

Owner decisions, smallest first:

1. **Box-1-driven heterogeneous group-binding.**
   `evaluate_pairing_scoped_rule` was called with two current box-1
   `SourceFact`s and one pairing (A only). It returned one publication
   with value `2000`, pins on A's box 1 / enrollment / pairing, **zero
   blocked rows**, and no pin on B. The dispatcher cannot account for
   unassociated B. Box-1-driven completeness (every current box-1 has
   exactly one usable association) is **conceptual**: no committed
   coordinator performs it; the probe computes it by hand.
2. **Authoritative catalog input.** `op == "parameter"` on `eligible`
   raises `DEPENDENCY_INVALID`. Keyed numeric half-time with one
   application-resolved id **works**. `categorical_compare` of a `ref`
   **works** when the probe injects the category. Injected probe facts
   are not a production catalog. Remaining choice: determinations become
   current findings through a defined evidence/producer path, **or** the
   rule grammar gains an adopted categorical catalog/parameter mechanism.
3. **Explanation carrier (optional if the narrowed promise is accepted).**
   Static explain names no statement or predicate. Mixed A-favorable /
   B-negative **projection** shows `published_value` 2000 citing only A
   because the probe authored those pins. All-negative `computed_zero` 0
   with attachment `guard_inapplicable` is projected from a **manually
   supplied inapplicable row**. The committed attachment requirement
   (not-required when line 21 is 0) was established in P2, not re-run
   here.

Pin isolation is a required property **not yet proven**. AccessLog
symbol names and manually authored aggregate pins do not establish
finding-level pin selection.

A general grouped-rule contract is not designed here.

## What the probe actually showed

| Requirement | Result |
| --- | --- |
| Two statements, different supported circumstances | Partial `VALUE_EXPR` in a hand-built env: A load 12 ≥ 6 → `2000`. B load 3 < 6 → `0`. Program classification not in the tree. |
| Two statements, one association missing | **Dispatcher:** two box-1 `SourceFact`s, one pairing; `evaluate_pairing_scoped_rule` emits one publication `2000` (A), blocked count 0, B unpinned. **Conceptual:** box-1 completeness fails on B; no committed coordinator performs that check. |
| One categorical institutional determination | `categorical_compare` of injected `ref`. Parameter of `eligible` fails. **Not a production catalog.** Program classification not evaluated. |
| Keyed numeric half-time | `parameter` keyed by one opaque standard id. Unknown id → `LOOKUP_MISS`. |
| Supported negative vs missing support | B publishes `0`. Absent eligibility `ref` → `DEPENDENCY_ABSENT`. |
| Correction | A's load 12 → 3; result becomes `0`. |
| Pin isolation | **Not proven.** |
| Mixed positive/negative projection | Synthetic publications: `published_value` 2000; citations A only because pins were authored; B's supported negative is not identifiable. |
| All-negative numeric zero, attachment absent | Synthetic: `computed_zero` 0; attachment `guard_inapplicable` from a manually supplied inapplicable row; `citationGroups` empty. P2 established the requirement behavior separately. |

## What a projected reader-facing model can and cannot identify

This is presentation projection over synthetic rows, not durable
presentation.

**Can (in the projected model):** a published number vs a block vs a
computed zero vs attachment not-required; citation sites the projector
walks from the pins the probe supplied; `DEPENDENCY_ABSENT` when that
code is allowlisted.

**Cannot:** which statement failed; which (C) predicate failed; that B
was a supported negative on a mixed return; B's reported amount when
line 21 is 0 (attachment projected inapplicable); unknown composition as
a named code after the renderer filters `SLI_*`; a production
institution-eligibility catalog; finding-level pin isolation.
