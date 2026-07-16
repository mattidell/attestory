# Scoped Confirmation Review — ADR-0028 Decisions 7–8 (Same-Quantity Force-Declare, Round 2)

Date: 2026-07-15. Role: Medium-tier Adversary confirmation, owner-launched, fresh context. Charter: `charter-confirm-decision7-round2.md`. Paper/static only.

**Read:** the decision-7 and decision-8 wording in `docs/adr/0028-package-fact-surface-and-composition-obligation.md`; `reviews/confirm-decision7-adversary.md` (Round 1 confirmation review for the gap being closed).

**Not read (seal held):** any other residual ADR draft text; decisions 1–6 substance beyond what's needed to state the boundary; MR-P1 / it2-rejection material; any other MR-A* finding.

---

## Redesigned Quantity-Vocabulary and Force-Declare Rules

We evaluate the redesigned mechanisms under Decisions 7 and 8:
1. **Redesigned Quantity-Vocabulary:** Under Decision 7, quantity identity is now mandatory, closed, and versioned. Every aggregation-eligible `fact-type.v2` source amount must carry a required `quantity: {id, version}` field resolving to a closed, versioned quantity vocabulary. Non-vocabulary, missing, or unknown quantity tokens reject at load (no fail-open).
2. **Pairwise Same-Quantity Force-Declare:** Under Decision 8, force-declare join is evaluated pairwise among the rule's inputs, checking for same resolved quantity `Q`. If ≥2 inputs share `Q`, obligation is triggered. If any input lacks a mandatory quantity, it rejects as a schema/quantity issue before force-declare check (no fail-open). Cross-quantity combinations (distinct quantity IDs) do not trigger force-declare.

---

## Scoped Findings

### MR-C6-1 — Case 1: Tagged same-quantity raw multi-ELX with obligations omitted (must reject)

**Construction:** Producing rule for line-2b-shaped `S` = `add(ELX(box1-amount), ELX(box3-amount), ELX(oid-amount))`. All three source fact types carry the mandatory quantity tag `quantity: {id: "taxable-interest", version: "v1"}`. No `composition_obligations` entry is present in the package.

**Evaluation:** Under Decision 8, the join direction is explicitly pairwise among the rule's inputs. The inputs share the same resolved quantity ID `Q` ("taxable-interest"). Because there are ≥2 distinct inputs sharing the same resolved quantity, the force-declare rule fires, requiring `S` to appear in `composition_obligations`. Since the obligation list is empty/omitted, this package is correctly **rejected**. The pairwise join direction is expressible here without requiring `S` itself to carry a quantity tag.
**Classification: REJECTS correctly.**

### MR-C6-2 — Case 2: Omitted quantity tags on source fact types (must reject)

**Construction:** The same raw multi-ELX construction as Case 1, but the author omits the `quantity` tag field entirely on the source `fact-type.v2` definitions to evade the pairwise match.

**Evaluation:** Under Decision 7, the `quantity` field is a required field on all aggregation-eligible `fact-type.v2` source amounts. Furthermore, Decision 8 specifies that if a rule has ≥2 inputs and any input lacks a resolvable mandatory quantity, it must reject with a quantity/schema issue *before* evaluating force-declare. This prevents the system from failing open into a "no shared quantity ⇒ no obligation" state.
**Classification: REJECTS correctly (on schema/mandatory-tag boundary, not failing open).**

### MR-C6-3 — Case 3: Line 9 wages/interest cross-quantity sum (must accept)

**Construction:** Form 1040 line 9 = line 1a (wages) + line 2b (taxable interest). The wages fact type is tagged with quantity `wages`, and the taxable interest subtotal inherits quantity `taxable-interest`. No `composition_obligations` entry is authored for line 9.

**Evaluation:** The rule has distinct inputs with different quantity IDs. No two inputs share the same resolved quantity ID. Under Decision 8, the cross-quantity non-trigger rule applies: "if no two inputs share a quantity id ... force-declare does not fire." The package is accepted without requiring a `composition_obligations` entry for line 9.
**Classification: ACCEPTS correctly.**

### MR-C6-4 — Case 4: Line 15-style multi-quantity fold (must accept)

**Construction:** Form 1040 line 15 = line 11 (AGI) − line 12 (standard/itemized deduction) − line 13 (QBI deduction), folding three distinct quantities. No `composition_obligations` entry is authored for line 15.

**Evaluation:** Similar to Case 3, all three inputs resolve to distinct, non-matching quantity IDs (AGI, deduction, QBI deduction). Under Decision 8, the cross-quantity non-trigger applies. Force-declare does not fire, and the package is accepted.
**Classification: ACCEPTS correctly.**

### MR-C6-5 — Case 5: Family-subtotal line-2b, obligations omitted (must reject)

**Construction:** Producing rule for `S` aggregates `B1.authorizes_subtotal`, `B3.authorizes_subtotal`, and OID's `authorizes_subtotal` subtotals, each of which resolves to the same quantity ID `Q` ("taxable-interest"). The `composition_obligations` entry is omitted.

**Evaluation:** The rule aggregates multiple source-family subtotal inputs that share the same resolved quantity ID `Q`. Under Decision 8, this matches the first condition ("a source-family authorizes_subtotal whose family's quantity is Q"). Since ≥2 inputs share `Q`, force-declare fires for `S`. Lacking the obligation, the package is rejected.
**Classification: REJECTS correctly.**

### MR-C6-6 — Case 6: Spelling drift / non-vocabulary quantity tags (must reject)

**Construction:** An author attempts to evade force-declare or bypass validation by using divergent free strings for the quantity tags, e.g., using `quantity: {id: "taxable_interest", version: "v1"}` and `quantity: {id: "taxable-interest", version: "v1"}`, or using a non-vocabulary token.

**Evaluation:** Decision 7 restricts quantity tags to a closed, versioned quantity vocabulary. Any missing, unknown, or non-vocabulary quantity tokens reject at load time and do not fail open. Spelling drift and arbitrary annotation are structurally foreclosed.
**Classification: REJECTS correctly.**

---

## Cross-cutting Analysis

Decisions 7 and 8 successfully close the gap identified in Round 1 (MR-C1 and MR-C5):
1. **Hole Closure:** In Round 1, an author could evade force-declare by omitting quantity tags or using divergent strings because quantity identity was underspecified and not mandatory. Under Round 2, making quantity mandatory on source fact types and validating them against a closed versioned vocabulary prevents the undeclared-tag evasion.
2. **Pairwise Join Soundness:** Specifying that the force-declare join is pairwise input-to-input resolves the ambiguity around "S's own quantity" and ensures the rule is expressible even in the absence of a pre-declared composition or subtotal symbol.
3. **No Fail-Open:** Explicitly requiring rejection of missing quantity tags on inputs prior to force-declare evaluation prevents any potential fail-open path.

---

## Disposition

**confirm**
