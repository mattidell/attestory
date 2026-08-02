# Triage: Conditional Selectors Round 1R

Date: 2026-07-13
Foreman: Claude, principal foreman

Round 1R independently re-performed the round-1 review of iteration 1 under the remediation exclusions (original round-1/repair/round-2/evaluation/ADR-0019 material denied to both seats; within-round independence held; the governance seat was owner-launched 2026-07-12, the adversary seat foreman-spawned 2026-07-13 with owner go). Reviews: `reviews/round-1r-governance.md` (CS-G1R–G7R), `reviews/round-1r-adversary.md` (CS-A1R–A9R).

## Headline result

Both seats, independently, reach the **opposite verdict from the tainted original round's eventual outcome**: Shape A (rule-driven derivation in the existing rule language) is conditionally accepted by both; Shape B (first-class selector citizen — the shape draft ADR-0019 adopted) is **rejected as specified** by both. The original process crowned Shape B after a repair pass; round 1R shows that outcome does not survive independent measurement against the committed contracts.

## Decision-blocking findings

**Common to both shapes — CS-P1 is not settled by iteration 1:**
- **CS-G1R:** categorical filing-status guards (`compare(ref(filing_status), eq, "single")`) do not execute under the committed evaluator's comparison contract, which coerces operands to decimals — the traced positive cases cannot resolve as written.
- **CS-A1R:** neither design authors the `operation-semantics.v1` citizens that `evaluate()` hard-requires for `round`/`bracket_fold`; Case 5 raises an uncaught `KeyError`, not a contained block.
- **CS-A2R:** the bracket-table row shape `{limit, rate}` is illegal under the committed `_bracket_fold` and the canon `row_shape` enum (`lower/upper/rate`).

**Shape B:**
- **CS-G2R:** policy values (15000/30000/2000/1550) hardcoded in selector logic — CS-P2 violation.
- **CS-G3R:** the design's `optional` contract does not match any committed schema, and its silent null/false policy is an implicit runner rule (Articles 9/11). Triage note: the `selector-artifact.v1` schema the review measured against was itself Track 1 implementation of the unratified ADR-0019 and has since been removed by the owner-directed reset — there is now **no committed selector contract at all**, which strengthens this finding.
- **CS-G4R:** native selector execution is an unlicensed runner pathway with undefined package-member, adoption, lineage, disposition, and edge contracts (Articles 4, 7, 11–14; ADRs 0006–0010).
- **CS-A3R:** the selector's cases cover 2 of 5 filing statuses with no defined fallback; restoring exhaustiveness also collapses its file-count advantage (CS-A6R).

**Shape A:**
- **CS-A4R:** default-injector rules overwrite an already-asserted spouse input with no presence check — a silent-collision hazard invisible to the package validator's rule-to-rule ownership check.

## Production conditions

CS-G5R (declare input fact nature and why absence is determinable, not elective — E3.1/Article 3), CS-G6R (demonstrate full derived-finding/pin/displacement lineage before production admission), CS-A5R (Shape B's "native optional resolution" claim unverified against the real evaluator), CS-A9R (state the bracket-boundary convention).

## Non-blocking

CS-G7R (examination overstates settlement — it must be reclassified: CS-P1 unresolved for Shape B, conditional for Shape A), CS-A7R, CS-A8R.

## Foreman recommendation

1. **Direction:** the remediated evidence supports the Shape A family — conditional selection modeled in the existing rule language with parameter citizens — under the repairs above. This matches CS-P1 as the plan originally stated it.
2. **ADR-0019** (selector citizen) is not supported by independent evidence. Recommend marking it **rejected** (retained, per the ADR-0013 amendment) rather than leaving it proposed; a selector citizen may return only via a fresh charter that declares the runner/contract boundaries CS-G4R names.
3. **Next step per plan:** the clean-room rival builder seat is still unfilled. Recommend chartering the rival to design the strongest categorical-condition representation in the Shape A family (resolving CS-G1R/A1R/A2R: supported categorical semantics, canon operation citizens, legal bracket rows), clean-room from it1. Owner decides.
4. The reopened `evaluation-analysis.md` must be rewritten from round-1R evidence; its prior Shape B recommendation is withdrawn.
