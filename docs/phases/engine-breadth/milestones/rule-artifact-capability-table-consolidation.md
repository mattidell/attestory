# Milestone Plan: Rule-Artifact/Attachment-Rule Capability Table Consolidation

Audience: Foreman (future), Owner. Status: **scoped, not selected, not
chartered.** This is hardening, not an engine-breadth tax-coverage slice
(`docs/phases/engine-breadth/engine-breadth-overview.md`'s non-goals
explicitly exclude hardening from the breadth roadmap); it is filed here as
a standalone plan because it is core generic-machinery work spanning the
same files a breadth milestone will keep touching.

## Origin

Filed 2026-08-17 from the `declarative-validation-substrate-f8949` milestone's
owner-advisor product review (P1,
`docs/prototypes/declarative-validation-substrate/reviews/owner-advisor-milestone-product-review.md`),
after the foreman independently re-verified the review's claim by direct
inspection of all four named files. Not attempted inside that milestone per
explicit owner instruction: scope it, do not build it, unless scoping
revealed it was small enough to land safely inline — it is not; see
"Why this is not a same-milestone repair" below.

## Problem

Every schema version a `rule-artifact.*`/`attachment-rule.*` citizen may
declare is checked against a hand-written, literal Python set or tuple,
independently re-declared at each call site that needs to know "can this
citizen do X." There is no single source of truth. ADR-0066 Decision 7
closed the *unregistered* case — a schema entirely absent from every list now
fails loudly at the package-validation boundary. It did not close the
*partially registered* case: a schema present in most but not all of the
sets that should include it. That is the failure mode that keeps recurring,
and it is silent — content validates cleanly, then misbehaves only at
runtime, only on the specific citizen that exercises the missing capability.

**Confirmed recurrence, three consecutive milestones:**

1. f1098e milestone: `runner.py:1331` missing a registered version (documented
   in that milestone's own record).
2. This milestone (declarative-validation-substrate-f8949): `marshal.py:101`
   missing `rule-artifact.v5`, and `marshal.py:89` missing `attachment-rule.v8`
   — the same omission, in the same function, found independently twice (once
   by the owner-advisor review, once more precisely by the foreman during
   repair).
3. A third, earlier instance already lives only as a code comment:
   `artifact-package.v22` (referenced in the owner-advisor review; not
   independently re-verified by this plan — confirm its exact site before
   chartering).

## Evidence: the sets are not one set

A shallow read might suggest "just union everything into one registered-schema
set." Direct inspection of `packages/derivation/package_validation.py` alone
(sampled at lines 64, 244, 280, 591, 662, 1380, 1439, 1715, 1760, 1805, 1819,
1921, 1955) shows the sets are **not duplicates of one list** — they encode
at least six genuinely distinct capability predicates:

| Capability | Example membership | Sample sites |
| --- | --- | --- |
| Full known-schema membership (rule-artifact + attachment-rule, every version) | `rule-artifact.v1`-`v5`, `attachment-rule.v1`-`v6`,`v8` | `package_validation.py:591,662,1715`; `live.py:71` |
| Declared-absence `when`/`value` refs outside `requires` | `rule-artifact.v3`-`v5` only | `marshal.py:101`; `package_validation.py:1380,1955` |
| "v6-shape" attachment (adjustment rows, positive/adjustment tie-out subtotals) | `attachment-rule.v6`,`v8` only | `runner.py`'s `_V6_SHAPE_ATTACHMENT_SCHEMAS`; `package_validation.py:1439,1805,1819`; `presentation_projection.py:369,401` |
| Itemization-capable attachment (excludes v1, which predates itemizations) | `attachment-rule.v2`-`v6`,`v8` | `package_validation.py:1760` |
| Full attachment-only membership | `attachment-rule.v1`-`v6`,`v8` | `marshal.py:89`; `presentation_projection.py:39`; `runner.py`'s `ATTACHMENT_SCHEMAS` |

A consolidation that flattens these into one set would silently widen or
narrow at least one call site's actual eligibility — that is exactly the
defect class this plan exists to close, reintroduced by the fix. **The real
design task is a capability table with one row per schema version and one
boolean/enum column per distinct predicate above**, not a single set.

## Why this is not a same-milestone repair

- At least six distinct capability predicates (likely more once `live.py`
  and `presentation_projection.py` are read as closely as
  `package_validation.py` was for this plan — this plan's site count is a
  lower bound, not a final inventory).
- Spans five files: `live.py`, `marshal.py`, `presentation_projection.py`,
  `package_validation.py`, `runner.py` — all core generic engine machinery,
  blast radius across every tax form, not just this milestone's Form 8949
  content.
- Every call site's migration must be individually verified to read the
  *correct* capability column, not just "the new shared thing" — a
  mechanical find-replace risks exactly the silent-widening/narrowing defect
  this plan exists to prevent.
- `package_validation.py` is this milestone's read-only reference precedent
  throughout Track 3/4; touching it was explicitly out of every repair
  charter's assigned paths.

## Proposed shape (design sketch, not a spec — Track 0 owns the real design)

A single declared table, one row per `(schema, version)`, one column per
capability predicate named above, likely as a small module
(`packages/derivation/schema_capabilities.py` or similar) that
`live.py`/`marshal.py`/`presentation_projection.py`/`package_validation.py`/`runner.py`
import from rather than re-declaring literal sets. Candidate shape:

```python
# sketch only
SCHEMA_CAPABILITIES = {
    "rule-artifact.v5": {"declared_absence_refs", "known"},
    "attachment-rule.v8": {"known", "attachment", "v6_shape", "itemizations"},
    # ...
}
```

Open questions a real Track 0 must settle, not this plan:

- Whether the table lives beside the schemas themselves (generated from
  schema metadata) or as hand-maintained content with its own registry test
  proving every published schema version has a row (closing the
  under-registration failure mode structurally, the same way ADR-0066
  Decision 7 closed the unregistered-schema failure mode).
- Migration order and whether it can be additive (new table + old sets
  temporarily coexisting, verified equal, then old sets deleted) to keep
  each step's blast radius reviewable.
- Whether `package_validation.py`'s role as reference precedent changes —
  it currently has the most complete/correct sets; the table's initial
  content should likely be derived from it, not re-authored from scratch.

## Evidence a Track 0 for this milestone should require

- A registry-level test that fails if any published `rule-artifact.*` or
  `attachment-rule.*` schema version lacks a capability-table row (structural
  closure of the recurring defect, not just a fixed snapshot).
- A migration proof per consumer file showing byte-identical behavior before
  and after switching that file's literal set to a table lookup.
- Full-suite green, per this repo's `AGENTS.md` "Test lanes" (any change
  under `packages/derivation/` runs the full suite, not the fast lane).

## Non-goals

- Does not add tax coverage; not an engine-breadth slice.
- Does not change any published schema.
- Does not attempt to unify capabilities that are genuinely distinct into
  one flag "for simplicity" — the table must preserve every real
  distinction found above.
