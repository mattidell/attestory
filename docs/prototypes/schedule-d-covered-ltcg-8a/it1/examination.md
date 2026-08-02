# Examination — Iteration 1: Nested-Identity, Synthesized-Conclusion Incumbent

Reports P1, P2, and P3 separately as settled at Rung 1 (static paper
instantiation) or unresolved, with exact case citations against the eleven
shared cases in `plan.md` and the mandatory negatives/lifecycle set
(cases 4, 5, 6, 7, 9, 10, 11).

---

## P1 — Transaction source family and identity

**Settled at Rung 1.**

- Identity topology (four-key member fact nested under family, mirroring
  ADR-0015/ADR-0016 and the K-1 box-5/market-discount precedents) is
  instantiated concretely and holds across cases 1, 2, 3 (positives),
  case 4 (correction — distinct member displacement demonstrated), case 8
  (all four closure lifecycle states), case 9 (reach-around foreclosed by
  construction — no sanctioned read path outside `collect_members`), and
  case 11 (non-covered/adjustment-code rejection at admission, two
  sub-variants).
- The incumbent constraint "two sales from one broker remain distinct
  members; correction displaces only the corrected transaction's
  identity" is directly demonstrated in case 4 and not violated anywhere
  else in the instance set.
- No production code, schema edit, or validator probe was needed to
  reach this conclusion — the shape is a direct, unmodified reuse of
  `source-family.v1` and `source-closure-mapping.v2`, both already
  accepted and already exercised for K-1 and market discount at one
  fewer identity level.

**Unresolved (named, not blocking):**

- Whether `transaction` identity needs further decomposition for
  lot-level partial correction is out of this milestone's supported
  source class and left for a future slice (design.md, P1 Unresolved
  §1). Not a Rung-1 gap — the supported source class explicitly excludes
  taxpayer-side basis adjustment.
- Whether the admission gate belongs in the closure-mapping's
  `admission` block or as a separate declared eligibility fact
  (design.md, P1 Unresolved §2) is unresolved because neither existing
  precedent (K-1, market discount) has a rejecting predicate to compare
  against — genuinely novel to this proposition, not answerable from
  existing paper evidence alone.

---

## P2 — Completeness-boundary declaration shape

**Settled at Rung 1, with one named schema-successor need.**

- The nine-part boundary is instantiated and shown heterogeneous by
  construction: two closure-state components (D1 new, D2 an unmodified
  citation into ADR-0050's existing box-2a closure) and seven genuine new
  declared-absence categorical facts (D3–D9), matching ADR-0038's shape
  exactly.
- Case 5 is fully worked for all nine components individually —
  every missing component produces `blocked(DEPENDENCY_ABSENT)` naming
  exactly that component, never a default and never an inferred `no`.
- Case 5b (two meaningful negatives: D3 and D7 each present-violating)
  demonstrates the `incomplete` disposition is distinct from `blocked`
  and is never conflated with it.
- Case 6 (box-2a present-and-nonzero) and case 7 (box-2a closed-empty)
  both settle: P2's D2 component only requires box-2a *closed* (either
  variant), independent of whether it is empty — the empty/nonempty
  distinction is deliberately deferred to P3's routing layer, not
  re-answered inside P2's boundary. This resolves the case 6/7 pairing
  cleanly at Rung 1.
- A lifecycle trace over D7 (undeclared → violating → corrected → clean)
  demonstrates free supersession re-evaluating the synthesized conclusion
  without any special-cased transition logic.

**Unresolved:**

- The closure-state/categorical heterogeneity requires a genuine schema
  successor (`checked-conclusion-binding.v2`, adding a `role` field) —
  this is proposed precisely (design.md, P2 topology) but whether the
  fold belongs in the binding schema itself or in an upstream derivation
  rule feeding a `.v1`-compatible binding is explicitly left open. This
  is the one question in this iteration where the paper evidence
  genuinely runs out and a rung-2 question is named: would existing
  `.v1` binding consumers need to change under either choice? (design.md,
  P2 Unresolved §1; cites case 5's D1/D2 rows as the concrete instance of
  the ambiguity.)
- Component 7's arity (one composite claim vs. seven-plus individually
  named source forms) is unresolved and named as an owner/plan-level
  question, not a Builder judgment call, since it changes the boundary's
  count, not just its encoding (design.md, P2 Unresolved §2).

---

## P3 — Schedule D content and QDCG/line-16 binding

**Partially settled at Rung 1; two named unresolved design points, one
named schema gap.**

Settled:

- Schedule D Part II line 8a/15 content instantiates directly on
  `attachment-rule.v2`'s itemization/row-set/tie-out shape, reusing the
  Schedule B precedent's structure without modification.
- The single-producer route-selection design for line 7a (a `match` over
  P2's boundary conclusion and P1's family closure variant, inside one
  successor rule) is shown to satisfy ADR-0038's Alternatives-Considered
  foreclosure of dual producers and ADR-0027 Decision 5's single-producer
  constraint. Case 9 (reach-around) and case 10b (QDCG reading raw
  content) are both foreclosed by construction, not by an added check.
- Case 10a's *mechanism* (D1-vs-box-2a is a precedence branch inside one
  match, never a summation) is settled as the incumbent's proposed
  shape; whether that precedence direction is the *correct* one is not
  (see Unresolved).
- The two negatives (boundary-incomplete blocking line 7a outright;
  case 11's rejected transaction never reaching line 8a because it was
  never admitted at P1) both settle cleanly, reusing P1/P2 results
  without new P3-specific mechanism.
- The proposed `rule.form1040-line16.v4` successor is stated precisely
  against the existing v3 rule's exact branch structure (design.md, P3
  Line-7a and line-16 successor design), satisfying the charter's
  request to extend Decision 7's structure with a Schedule-D-sourced
  case without editing ADR-0050.

Unresolved:

- **Schema gap (named, not worked around):** `attachment-rule.v2`'s
  `requirement` block is structurally threshold-only
  (`packages/schemas/tax/attachment-rule.v2.schema.json`, all of
  `subtotals`/`threshold_parameter`/`comparison: strictly_greater_than`
  required). Schedule D's "required" disposition is categorical (P2's
  boundary conclusion), not a numeric threshold. `attachment.schedule-d`
  is left with its `requirement` block unspecified pending a proposed
  `attachment-rule.v3` successor (`oneOf` threshold/categorical shape),
  named but not drafted. This is a real generality gap in accepted
  content, surfaced by the paper spike exactly as intended, not a defect
  in this design.
- **D1-vs-box-2a precedence (case 10a):** stated as a design choice
  (Schedule-D route takes precedence when both close with members) but
  explicitly flagged as needing owner/ADR ratification, not asserted as
  self-evidently correct. This is the one place in P3 where two
  reasonable shapes exist (precedence vs. an explicit-conflict block)
  and the paper evidence alone does not decide between them.
- **QDCG unconditional-eligibility assumption:** the Schedule-D-sourced
  branch of the line-16 successor reads no gating input at all (design.md,
  P3 Unresolved §3) — asserted correct given the supported source class's
  exclusions, but named for reviewer scrutiny since every other branch in
  this codebase's QDCG logic reads at least one guard.

---

## Summary

| Proposition | Status |
|---|---|
| P1 | Settled at Rung 1. Two non-blocking future-slice questions named. |
| P2 | Settled at Rung 1. One genuine schema-successor need named (`checked-conclusion-binding.v2`); one owner-level arity question named. |
| P3 | Settled at Rung 1 for content structure and single-producer routing. One schema gap named (`attachment-rule.v2` requirement block); one precedence design choice flagged for ratification; one QDCG-eligibility assumption flagged for reviewer scrutiny. |

No case in the required set (1–11, with 4/5/6/7/9/10/11 as mandatory
negatives/lifecycle) was left uninstantiated. No rung-2 escalation was
taken — every unresolved item above is unresolved because the paper
evidence itself runs out (a genuine schema/design fork), not because a
rung-1 question was left unanswered.
