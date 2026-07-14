# Examination — Taxable-Interest Composition it1 (Incumbent)

Date: 2026-07-14. Design: `it1/design.md`. Rung 2 paper only; no runner/schema/horizon edits; no git writes.

## Scope echo

Designed TIC-P1 (coextensive line-2b universe + checkable declaration) and TIC-P2 (honest coextensive zero + late-member lifecycle). Prior art (spike, inert ADR-0021) read to supersede, not inherit boundary or bare sum. Stopped at two static files.

## TIC-P1 — Coextensive universe + declaration

**Status: settled at static level** (mechanism + justified U_2b^v1), with open taxonomy questions not closed by fiat.

**Universe (justified against line 2b, not inherited):** Form 1040 line 2b is *taxable* interest; line 2a is tax-exempt. **In:** 1099-INT box 1; box 3 US savings-bond/Treasury interest; residual non-form taxable interest. **Out:** box 8 / line 2a tax-exempt; non-interest boxes. Separate families follow ADR-0016 (box-specific predicates; non-form and box 3 defeat B1-as-all). Same three-way set as the spike only because the line-2b definition and ratified counterexamples independently require it.

**Declaration mechanism:** versioned `coextensive-composition.v1` pins each constituent family’s ADR-0016 declaration + `authorizes_subtotal`, states exact `required_universe.claim`, names `publishes` = line-2b symbol. Validator `audit_composition_authority` (V1–V8) rejects missing/extra constituents, collect→line-2b, mapping that admits line-2b for a narrow family, and coverage that reports composition complete from a subset. Line-2b rule only `ref`s all constituent subtotals (never `collect`s). Defeats spike gap: bare sum without coextensiveness check.

**Open (explicit):** OID / K-1 / foreign / seller-financed as further constituents vs versioned surface growth; EE/I exclusion placement; composition pin role vs package binding; exact production schema bytes (Gate 5).

## TIC-P2 — Honest zero + late-member lifecycle

**Status: settled at static level.**

Honest zero: line 2b publishes 0 only when every constituent subtotal has published, and every empty constituent used current literal-true closure on its current horizon (ADR-0014/0017). B1-alone never authorizes line-2b zero (ADR-0016 dec. 5).

Late member: `member-transition` → horizon succession (individuation) displaces horizon-keyed closure → derivation displaces subtotal zero → derivation displaces line-2b zero. Re-attest on successor + explicit rerun republishes. No new edge, no manual withdrawal, no resurrection of old zero (ADR-0010/0017). Named trace: §3.3 of design (`H_*`, `CF_*`, `DF_*`, edges).

## Cases (all cited)

| Case | Disposition | Design anchor |
|---|---|---|
| 1 Empty coextensive zero | Pass (P1a/b; N1a/b) | §4 Case 1; Phase A pins |
| 2 Box-1 only, others closed empty | Pass (P2a/b; N2a/b) | §4 Case 2 |
| 3 Multi-source | Pass (P3a/b; N3a/b) | §4 Case 3 |
| 4 One constituent unclosed | Pass (N4a/b); coverage open (V8) | §4 Case 4; ADR-0016 dec. 3 |
| 5 Narrow substitution (mandatory) | Pass — V5 + existing collect audit + mapping check | §4 Case 5; defeats spike |
| 6 Late-member lifecycle (mandatory) | Pass — full named edge/finding/pin trace | §3.3 Phases A–C |

## Conformance checklist

- ADR-0016 dec. 3/4/5: exact composition claim; explicit coextensiveness; no B1→line-2b promotion.
- Article 7 / ADR-0010 / ADR-0017: only individuation + derivation; horizon machinery unchanged.
- No third edge; no stored currency; no runner tax meaning beyond declared artifacts.

## Stop

Two files only. Implementation of schema/content/audit is Track 2 after conforming ADR (candidate 0026 superseding inert 0021).
