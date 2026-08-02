# Scoped Confirmation Review — ADR-0028 Decision 7 (Same-Quantity Force-Declare)

Date: 2026-07-15. Role: Medium-tier Adversary confirmation, owner-launched, fresh
context. Charter: `charter-confirm-decision7.md`. Paper/static only.

**Read:** the decision-7 wording quoted in the charter; `docs/adr/0028-package-fact-surface-and-composition-obligation.md` decision 7 (exact predicate text, clauses 5–8) and its Context/History/Consequences PC1/PC1b; `reviews/round-1-adversary.md` MR-A7 section only (for the original attack this retype answers).

**Not read (seal held):** any other residual ADR draft text; `review-feedback-adr0028.md`; decisions 1–6 substance beyond what's needed to state the boundary; MR-P1 / it2-rejection material; any other MR-A* finding.

---

## The rule under test, restated precisely

Decision 7: force-declare `S` when the producing rule has ≥2 distinct adopted
inputs that are alternative sources/subtotals of `S`'s **own** tax quantity —
family `authorizes_subtotal` for that quantity, or raw/ELX source amounts of
that **same** quantity — and does **not** fire for ≥2 inputs of **different**
quantities. Decision 7's own text places the weight-bearing term outside
prose: "Quantity identity is declared content ... not runner-resident symbol
tables," and must be "schema-authoritative."

That sentence is the entire test. Every one of the four required cases turns
on whether "quantity identity" is (a) actually anchored to a schema field
somewhere, and (b) mandatory wherever it needs to be compared — not on
whether the English description of the boundary is sensible, which it is.

---

## MR-C1 — Case 1: MR-A7 raw multi-ELX construction (must reject)

**Construction:** producing rule for line-2b-shaped `S` = `add(ELX(box1-amount), ELX(box3-amount), ELX(oid-amount))`. No family pins, no mapping, no composition citizen, no `composition_obligations` entry.

**Applying the predicate literally:** decision 7 says quantity identity may be declared "on source-family / **fact-type** / mapping surfaces as needed for the join" — so even absent any family/composition, the three raw ELX inputs' own `fact-type` citizens are eligible to carry the quantity tag the join needs. Under a reading where the join is *pairwise input-to-input quantity agreement* (≥2 of the rule's own inputs share one declared quantity tag), `S`'s quantity is derived from that shared tag rather than needing an independent declaration on `S` itself, and the predicate correctly fires: **reject**, matching the required outcome and matching decision 7's own claim ("still catches the adversary MR-A7 construction").

**But this reading is not the only one the text supports**, and the other one breaks the case. A literal reading of "alternative sources of **`S`'s own** tax quantity" asks for `S` to have an independently anchored quantity identity that the inputs are then checked against. In this exact construction there is no composition citizen, no family, no mapping — nothing in the package declares what quantity `S` itself is. If an implementer builds the join that way (check inputs against `S`'s declared quantity) rather than the pairwise-agreement way, the join is **inexpressible** for precisely this construction — there is nothing to check `S` against — and the natural fallback for an unanchored predicate is fail-open (no basis to force-declare → does not fire), reproducing the exact hole decision 7 was retyped to close. Decision 7's text does not disambiguate between these two joins; both are consistent with its wording.

**Deeper problem, independent of which join is chosen:** decision 7 does not make fact-type-level quantity tagging **mandatory**. It says quantity identity is "declared content ... as needed for the join" — permissive language, not a required-field commitment on `fact-type.v2` / `source-family.v2`. If an author omits the quantity tag on `box1-amount`, `box3-amount`, and `oid-amount` (exactly as easy to omit as the family pins the original MR-A7 omitted), the pairwise-agreement join also has nothing to compare and also fails open. **The evasion surface has moved, not closed:** MR-A7 v1 omitted family pins; MR-A7 v2 (implicitly re-derivable from this gap) omits quantity tags on otherwise-identical raw ELX inputs, and nothing in decision 7 forecloses it.

**Classification: AMBIGUOUS at the paper level — the case can be made to reject only under an unstated join direction, and even then only if quantity tagging is (silently) assumed mandatory, which decision 7 does not state.**

## MR-C2 — Case 2: line 9 = line 1a + line 2b (must accept, no obligation)

**Construction:** total-income rule aggregates the wages symbol and the
taxable-interest symbol — two inputs of textually and substantively different
quantities. No `composition_obligations` entry.

**Applying the predicate:** under either join reading (pairwise or
S-anchored), as long as wages and taxable-interest carry *different* declared
quantity tags (or one/both carry none), no shared quantity is found among the
two inputs, so the trigger correctly does not fire. **Classification: ACCEPTS
correctly** — this direction of the boundary holds cleanly, and is the
one case where the retype's stated purpose (stop over-firing on cross-quantity
arithmetic) is unambiguous, because "no shared tag" is a safe default in the
non-trigger direction. This asymmetry is itself notable: the predicate is
safe-by-default against over-triggering (undeclared/mismatched quantity ⇒ no
force-declare) and unsafe-by-default against under-triggering (undeclared
quantity ⇒ no force-declare, MR-C1) — the same permissive default produces a
correct result on one side of the boundary and an evasion on the other.

## MR-C3 — Further cross-quantity control: line 15 (must accept)

**Construction:** Form 1040 line 15 = line 11 (AGI) − line 12 (standard/itemized deduction) − line 13 (QBI deduction), a three-input fold over three distinct quantities (adjusted gross income, deduction, QBI deduction). No `composition_obligations` entry.

**Applying the predicate:** three inputs, no two of which represent alternative sources/subtotals of one shared tax quantity — AGI is not an "alternative source" of the deduction amount, nor is QBI. Under either join reading, no pairwise match exists, so the trigger correctly does not fire. **Classification: ACCEPTS correctly.** (Line 16 was considered as an alternative control but rejected as a control case here: it is typically a single-input bracket/table lookup off line 15, so it wouldn't even reach the "≥2 inputs" precondition — a weaker test of the cross-quantity direction than line 15's genuine three-way distinct-quantity fold.)

## MR-C4 — Family-subtotal line-2b, obligations omitted (must reject)

**Construction:** producing rule for `S` aggregates `B1.authorizes_subtotal`, `B3.authorizes_subtotal`, and OID's `authorizes_subtotal` — each a source-family subtotal under ADR-0016 — with no `composition_obligations` entry and no composition citizen.

**Applying the predicate:** decision 7's text names "source-family `authorizes_subtotal` values for that quantity" as one of the two explicitly qualifying input shapes — this is the shape decision 7 was written closest to, and it is also the one case where an anchor for "S's own quantity" is least ambiguous: a source-family declaration (ADR-0016) already carries `authorizes_subtotal` naming exactly the symbol it feeds, which structurally ties each family to the same downstream `S` even without a separate "quantity" field per family — the join can key on "these ≥2 families all declare `authorizes_subtotal` feeding the same producing rule/`S`" rather than needing a free-floating quantity tag at all. **Classification: REJECTS correctly**, and with less ambiguity than MR-C1 — the family-subtotal shape has a natural, already-committed anchor (`authorizes_subtotal`) that the bare-ELX shape (MR-C1) lacks entirely.

---

## Cross-cutting finding

## MR-C5 — The predicate's correctness is asymmetric, and the vulnerable side is the one decision 7 exists to fix

Collecting MR-C1–C4: the boundary holds cleanly in the accept direction (MR-C2, MR-C3) and in the family-subtotal reject direction (MR-C4), because in every one of those three cases there is a structural anchor already available in committed or ADR-0016-declared content (`authorizes_subtotal`, or simply the absence of any shared tag). The boundary is genuinely uncertain in exactly one direction: the bare-raw-ELX reject case (MR-C1) that motivated the retype in the first place. That case's correctness depends on two unresolved choices decision 7's text does not make:

1. **Join direction** — pairwise input-to-input quantity agreement (workable) vs. an independently-anchored "S's own quantity" (inexpressible when no family/composition exists, i.e. inexpressible in exactly the adversarial case).
2. **Tag mandatoriness** — decision 7 nowhere requires that a raw source-amount fact type declare its quantity; "declared content ... as needed for the join" reads as discretionary. A discretionary tag on exactly the citizen kind an evader controls (their own new fact-type content) is not a closing move against an adversarial author — it is an invitation to omit the tag the same way MR-A7 v1 omitted the family pin.

Decision 7's own §7 closing paragraph claims quantity identity "must" be schema-authoritative, but "must be schema-authoritative" is a requirement on the *implementation*, not a specification decision 7 itself makes — it names no field, no schema version, no closed vocabulary discipline (contrast with how ADR-0006 treats the operation vocabulary or role vocabulary: closed, enumerated, versioned). Two independently-authored fact types for the same real-world quantity could tag it `"taxable-interest"` and `"taxable_interest"` (a false negative — same quantity, no match, under-trigger survives) or two different quantities could coincidentally share a casually-chosen string (a false positive — over-trigger on line 9-style arithmetic, undoing MR-C2's clean pass). Neither failure mode is foreclosed by anything in decision 7's text.

---

## Disposition

**needs redesign** — the same-quantity vs. cross-quantity semantic cut itself is correct and passes three of four required cases cleanly (MR-C2, MR-C3, MR-C4). But the fourth — the exact MR-A7 construction decision 7 was retyped to close — remains ambiguous at the paper level: the predicate depends on a "quantity identity" concept that decision 7 requires to be schema-authoritative but does not itself specify (no named field, no schema-version diff, no closed/versioned vocabulary, no mandatoriness commitment on the fact-type/family surfaces an adversarial author controls). Until quantity identity is pinned down as a **mandatory, closed, versioned** declared field on the relevant citizen kinds (paralleling how ADR-0006 closes the operation and role vocabularies), MR-C1 shows the predicate can be read — and, absent a mandatory-tagging rule, can be *implemented* — in a way that reproduces the original under-trigger hole through an undeclared-tag evasion rather than an undeclared-family evasion. This is a redesign of the quantity-identity mechanism specifically, not a rejection of the same-quantity boundary concept, which MR-C2–MR-C4 confirm is the right cut.

Advisory only — disposition of ADR-0028 itself is the owner's.
