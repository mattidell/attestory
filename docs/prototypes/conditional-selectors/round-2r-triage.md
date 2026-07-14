# Triage: Conditional Selectors Round 2R

Date: 2026-07-13
Foreman: Claude, principal foreman

Round 2R reviewed the clean-room rival's iteration 2 in independent owner-launched contexts. Reviews: `reviews/round-2r-governance.md` (CS-G8R–G11R), `reviews/round-2r-adversary.md` (CS-A10R–A14R). Both verdict **conditionally accept**; both rule CS-P2's settlement sound and CS-P1's deliberate non-settlement contractually correct.

## The load-bearing result

The adversary **confirmed the optional-input impossibility claim** after refuting the three plausible counterexample constructions (staged multi-publisher rules → ownership conflict or deadlock; source-collection closure aggregation → not a true default and ontologically wrong; evaluation-order short-circuiting → cannot cover the always-applicable taxpayer's own flags). Under committed contracts, referencing an absent scalar input blocks, and a default-injecting rule overwrites. Combined with governance's independent concurrence (CS-G9R: genuine contract gap; governance-body resolution), CS-P1's residue is now firmly a **separate decision topic**, not a defect in it2.

## Decision-blocking (repairable in-place)

- **CS-A10R / CS-A11R:** the spouse-adjustment `all(...)` expressions reference the possibly-absent spouse flag *before* the `spouse_allowed` guard; the committed evaluator's `all` short-circuits left-to-right, so Single/HoH/QSS and ineligible-MFS filers block. Repair is the adversary's argument reordering (`spouse_allowed` first) plus the explicit documentation that taxpayer demographic flags must be asserted (adversary condition 2). Per the NPE precedent, these fold into the eventual ADR's decision text and design errata — no new build pass warranted.

## Production conditions

- **CS-G8R:** numeric status-code strings ("1"–"5") are an executable but illegible workaround for the evaluator's decimal-coercing `compare`; production needs categorical/string comparison support in the expression language (Article 11).
- **CS-G9R / authority question 1:** the optional-input absence/default mechanism — a genuine contract gap touching Article 7 edge semantics and Article 11. Route as its own prototype-eligible Tier-2/3 decision topic (candidate scope: expression-language extensions — categorical comparison + declared absence/defaults — one plan, since CS-G8R lands in the same contract surface).
- Authority question 2 (itemized-deduction package) is resolvable within existing contracts; it stays with roadmap content planning.

## Verified

CS-G10R (bracket-fold canon + row shape — resolves CS-A1R/A2R), CS-G11R (exhaustive five-status scoping — resolves CS-A3R), CS-A12R (spouse-scope exclusivity), CS-A13R (thresholds, zero/negative income), CS-A14R (itemization override blocks downstream honestly).

## Foreman recommendation

1. **Accept it2 as the settled Shape A design** under the CS-A10R/A11R reordering repairs, recorded as errata in the eventual ADR rather than a rebuild.
2. **Rewrite `evaluation-analysis.md`** from rounds 1R and 2R: CS-P2 settled; CS-P1 settled for the guarded-derivation subset, with the absence gap split out.
3. **Draft a fresh conditional-structures ADR** (next free number — not 0019, which stays rejected) for the accepted subset, gated on the owner's disposition.
4. **Owner-approved plan for the expression-language-extensions topic** (absence/defaults + categorical comparison) before any further CS implementation; Track 3 rebuild waits on both ADRs.
