# Prototype Evaluation Analysis — Taxable-Interest Composition

Foreman synthesis, 2026-07-14. Advisory to the owner; the owner decides disposition and ratifies any ADR. Track 0.a of the Core Tax Conditions milestone remediation.

## Decision under evidence

How Form 1040 line 2b (Taxable Interest) composes over its source families (TIC-P1: the coextensive universe + its declaration mechanism), and how an honest zero and the late-member lifecycle behave (TIC-P2). Candidate ADR-0026, superseding the inert ADR-0021 and its spike.

## Evidence

Two independently authored, clean-room-separated designs of both propositions and six Gate-2 cases:

- Incumbent (`it1/design.md`, `examination-it1.md`) — committed exhibit `4ea0b6c`. Universe `{B1, B3, non-form}` with taxable OID deferred; package-level binding; validator V1–V8.
- Clean-room rival (`it2/design.md`, `examination-it2.md`) — committed exhibit `f3ccb43`, sealed from the incumbent, the spike, and ADR-0021. Universe `{B1, B3, taxable-OID, unreported}`; required `composition` pin + slot-bijection validator + generic `require_closed(source_set)`.

Reviewed by two independent-context committee seats: Governance (`reviews/round-1-governance.md`, TIC-G1–G5; committed by owner `15e90f3`) and Adversary (`reviews/round-1-adversary.md`, TIC-A1–A7). Neither read the other.

## Convergence under independent authorship

Both designs, authored in sealed contexts, converged on the composition **mechanism**: a versioned composition citizen declaring the universe, a validator that rejects a line-2b rule not referencing every constituent subtotal, coverage that never reports the broader universe complete from a narrow closure (ADR-0016 dec 3), and a late-member lifecycle that displaces through ADR-0017 individuation + ADR-0010 derivation edges only — no third edge, no manual withdrawal, no resurrected zero. Convergence on the mechanism under independent authorship is strong evidence the shape is right.

They **diverged** on the two questions this round existed to resolve — and both reviewers, independently, resolved both divergences the same way.

## The boundary — decided against the incumbent

Both reviewers **reject** the incumbent's `{B1, B3, non-form}` universe as coextensive with Form 1040 line 2b (TIC-G1, TIC-A1). The Form 1040 and Schedule B instructions name Form **1099-OID** as a source of taxable interest for line 2b; taxable OID is neither B1, B3, nor the incumbent's non-form residual. The incumbent's "scoped/versioned" claim — *complete under the constituents I chose* — is precisely the ADR-0016 decision-5 narrow promotion it was meant to avoid, in composition form: it publishes the line-2b symbol and binds the line-2b form field while omitting an in-scope source, understating the filer's line 2b by construction (adversary's synthetic filer F-OID: $200 published, $550 correct). Versioning tracks a changing tax surface; it cannot narrow the fixed meaning of a form line. The rival's mandatory taxable-OID slot is the honest boundary.

## The binding and closure mechanics — decided for the rival

The rival's bundle is materially stronger, and the adversary isolated three holes in the incumbent the governance fidelity pass alone would not have:

- **Present-source open-family publication (TIC-A3, decision-blocking).** The incumbent gates *coverage* on all-constituent closure (V8) but not *publication*: a present-source B1 subtotal publishes without a closure read, so line 2b ships a value while B1 is open (a second unrecorded 1099-INT would silently leave the number wrong). The rival's `require_closed` per slot — including non-empty slots — blocks until every constituent is closed. This is the round's cleanest single-mechanism differentiator.
- **Present-source late-member non-displacement (TIC-A5, decision-blocking).** Because the incumbent's present-source line finding pins no closure, a late member advances the horizon but does not displace the already-published line value (it only displaces closure-backed zeros). The rival's line finding pins the direct closure findings, so horizon succession displaces the line value through the existing two edges — showing why direct closure pins on the line are load-bearing, not cosmetic.
- **Vacuous binding (TIC-A7, decision-blocking for it1).** The incumbent's V4 is a pairing rule; a package shipping the line-2b rule with **no** composition citizen leaves the quantifier vacuous and reduces to a bare spike sum. The rival's required `composition:{id,version}` pin makes the binding non-optional.

## Supported conclusions

- **C1 — the composition mechanism is settled at the static level, on the rival's bundle:** a versioned universe citizen; a slot-bijection validator (rejecting omission/duplication/substitution/extra); a **mandatory, licensed** composition binding on the line rule; the line rule referencing every constituent subtotal **and** `require_closed`-ing every constituent via the committed ADR-0014 dispatch; the line finding pinning every closure read.
- **C2 — the member boundary must include taxable OID** and exclude tax-exempt interest (2a / box 8). The incumbent's OID-deferred universe is rejected.
- **C3 — TIC-P2 (honest zero + lifecycle) is settled on the rival's mechanics** and conforms to Articles 7 / ADR-0010 / ADR-0017; the incumbent's is sound only for closure-backed zeros, not present-source values.
- **C4 — neither design yet owns honest *total* taxable interest.** Two structural gaps, from the adversary:
  - **Positive residual sources** (Schedule K-1 interest, market discount) are absorbed by a residual slot only if production authors real predicates for them — the label `unreported` is a relabel, not a proof (TIC-A2).
  - **Subtractive adjustments** (nominee interest, accrued interest paid at purchase, bond-premium amortization) are **not** positive source families and **cannot** be expressed as another summed slot; a sum-of-positive-subtotals composition structurally cannot represent them.

## Rejected alternatives

- **Incumbent scoped/versioned coextensiveness `{B1,B3,NF}` (it1 TIC-P1).** Rejected: omits taxable OID while publishing line 2b — ADR-0016 dec 4/5 narrow promotion (TIC-G1, TIC-A1).
- **Publication gated on coverage but not on closure reads (it1).** Rejected: present-source open-family publication and late-member non-displacement (TIC-A3, TIC-A5).
- **Optional/package-only composition binding (it1).** Rejected: vacuous with no composition citizen (TIC-A7).
- **A residual `unreported` slot as proof of completeness (both).** Rejected: relabels the gap; forces nothing (TIC-A2).

## Production conditions (for ADR-0026 and Track 2)

1. **License the composition binding.** The composition pin/role must be added to the shared closed vocabulary (ADR-0006 dec 9) as **provenance only**, non-edge (ADR-0010) — or the binding enforced by a non-vacuous package rule (the line-2b symbol may be published only by a composition-bound rule). Both reviewers require it mandatory and licensed, not optional.
2. **`require_closed` via the single ADR-0014 dispatch only** (no second closed-set writer); reject alternate runners that evaluate the refs without executing the closure ops; pin-set goldens include all closures on multi-source non-zero lines.
3. **V5 one-to-one:** reject duplicate references to one constituent, not merely absence.
4. **Lifecycle:** atomic member-transition (ADR-0017), dual-family reclassification admission, and `conflict_semantics` resolution that cannot elect a non-composition producer for the line-2b symbol.
5. **Residual predicates and adjustment arithmetic** are declared as adopted content before any "total taxable interest complete" claim.

## The scope question the owner must settle (see recommendation)

C4 forces a genuine scope-and-honesty decision for ADR-0026: does the decision require the **full** taxable-interest universe (OID + K-1 + market discount as positive families **and** nominee/accrued/premium as a separate adjustment mechanism) before line 2b may publish at all — or does it ratify the **mechanism + the OID-inclusive positive-source boundary + a strict honesty gate**, explicitly scoping additional positive sources and all subtractive adjustments to named follow-on decisions, so line 2b may publish honestly over its declared positive-source universe while blocking/over-claiming nothing? This changes how much ships in this milestone and is the owner's call.

## Recommendation

Ratify **ADR-0026** on the rival (it2) mechanism and the OID-inclusive boundary (C1–C3), with production conditions 1–5. On the scope question, the foreman recommends the **mechanism + honest-partial** framing: decide the composition contract and the coextensiveness *principle* now (every in-scope **positive** source family must be a constituent; adjustments are a separate arithmetic decision), require the taxable-OID slot, and make the universe's claim text state exactly which positive families it covers — so line 2b is honest about its scope rather than blocked indefinitely behind the entire interest taxonomy. Whether that honest-partial line 2b is acceptable for the milestone, or the full universe is required first, is the owner's decision.
