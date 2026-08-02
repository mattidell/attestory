# Round 3 Expressiveness Review — Source Completeness

Date: 2026-07-12  
Seat: expressiveness, Medium tier  
Evidence rung: 3; shape A only

## Method

Read the round-3 and repair3 charters, the repair3 evaluator and tests, the
repair1 resolver, and the repair2 faithful two-layer copy. Per the seat rule, I
ran repair3 before reading `examination-repair3.md`; I did not read any
same-round peer review.

Commands run:

```
cd docs/archive/2026-08-02-milestone-artifacts/prototypes/source-completeness/repair3
python3 -m unittest -v
```

Result: 11 tests passed. I also ran an independent API-level charter matrix
against the authorized entry points; it passed.

## Measurements

| Check | Result | Evidence |
|---|---|---|
| Charter coverage | Pass | All named cases occur in `test_authority.py`: genuine zero/pin, present aggregation, six prior negatives, bare family, fabrication, provenance mismatch, duplicate orders, stale/current orders, and both bypass mutants. |
| Current literal-true closure | Pass | Empty members publish `Decimal(0)` and pin `clo-true@v5`; the independent run reproduced this. |
| Layer distinction | Pass | Present values `11 + 23` publish `34` with no closure finding and no closure-authority pin. Empty values without admitted closure block. |
| False / absent / displaced / truthy / ambiguous | Pass | Each remained publication-blocked in the suite and independent matrix. This retains false, absent, and superseded-closure distinctions rather than treating presence as closure. |
| Exact current pin | Pass | In both history orders, the successor `current@v2` pins; a carrier for `old@v1` raises `AuthorityInvalid`. |
| Fabricated and duplicate carriers | Pass on validated paths | A fake carrier over empty findings, mapping-provenance mismatch, and duplicate same-family carriers in either order all raise before `run_rule_with_carrier` publishes. |
| Correspondence invariants | Pass on validated paths | `validate_membership` checks mapping id/version, duplicate family names, then equality with fresh `resolve_A` output; resolution supplies fact type, identity, current literal-true finding, and exact mapping provenance. |
| Mutant honesty | Pass | The examination explicitly reports that the unvalidated mutant publishes both attacks; the supplied tests reproduce that divergence. |

## Finding

**Conditional decision-blocking residual: an alternate callable evaluator entry
remains.** `authorized_eval.run_rule_trusting()` accepts a fabricated or
duplicate `AuthorizedMembership` and publishes zero. This is intentional and
properly labeled as the constructor-bypass mutant, and the two corresponding
tests demonstrate the kill. Nevertheless, the round-3 failure definition says
that *any alternate accepted evaluator entry* is failure; as a public callable
in the prototype module, this path is such an entry. It yields the exact
round-2 outcome if a caller invokes it directly.

This does not falsify the repair's re-derivation mechanism: both intended entry
points are correct, and a hand-constructed carrier that exactly equals fresh
resolver output is harmless under the stated non-cryptographic contract. It
does mean the examination's unconditional sufficiency call is too broad for the
current exposed prototype surface.

## Disposition

The validated shape-A path reproduces every chartered expressiveness and
negative-result claim, including exact pins and the two-layer distinction.
However, under the round's stated alternate-entry criterion, repair3 is **not
sufficient as currently surfaced**. Treat `run_rule_trusting` strictly as a
test-only mutant (not exported or reachable by any evaluator dispatch) and
recheck no-bypass reachability; then the measured validated boundary is
sufficient for this construction question. No production, schema, persistence,
SC-P2, SC-P3, SC-D1, or shape-B conclusion follows from this review.
