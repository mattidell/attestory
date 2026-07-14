# ADR 0026 — Taxable-Interest Composition and Form 1040 Line 2b

- Status: **accepted** (owner ratification 2026-07-14, principal foreman custody)
- Tier: 2
- Date: 2026-07-14

## Context

ADR-0016 established that a family subtotal carries its declaration/predicate, that a broader result may consume it **only** where the universe is identical or an explicit composition is *established as coextensive* (decision 4), that box-1 closure authorizes only the box-1 subtotal and never a line-2b zero (decision 5), and that coverage cannot silently report a broader universe complete (decision 3). It left the full taxable-interest taxonomy *Not Decided*. The inert ADR-0021 and its single-author spike asserted `sum(b1, b3, non-form)` without establishing coextensiveness — the exact gap this decision closes.

The `taxable-interest-composition` prototype (Track 0.a remediation) produced two clean-room-separated designs (incumbent `4ea0b6c`, rival `f3ccb43`) and two independent committee reviews (`round-1-governance.md`, `round-1-adversary.md`). Both reviewers **rejected** the incumbent's `{B1, B3, non-form}` universe (it omits taxable OID, an in-scope line-2b source, while publishing the line-2b symbol — narrow promotion in composition form) and **carried the rival's** mechanism and OID-inclusive boundary. The committee also proved that neither design owns honest *total* taxable interest: subtractive adjustments (nominee, accrued-interest-at-purchase, bond-premium amortization) cannot be expressed as a summed positive slot, and further positive sources (K-1, market discount) need real predicates. Evidence: `docs/prototypes/taxable-interest-composition/evaluation-analysis.md` and the reviews and exhibits it cites. Owner scope decision (2026-07-14): ratify the **mechanism + the OID-inclusive positive-source boundary + a strict honesty gate**, deferring subtractive adjustments and further positive sources to named follow-on decisions.

## Decision

1. **Line 2b is a coextensive composition over positive taxable-interest source families.** A versioned `taxable-interest-composition.v1` citizen declares the line-2b universe as a closed set of constituent slots, each pinning one source-family declaration (its ADR-0016 `closure_claim` + `member_predicate`) and that family's `authorizes_subtotal`. The line-2b rule consumes the constituent subtotals; consuming them is licensed **only** through this declaration, never a bare sum.

2. **Coextensiveness is a slot-bijection, validated.** Package validation rejects unless the line-2b rule's constituent set is an exact bijection with the universe's slots — no omission, duplication, substitution, or extra — and each constituent's predicate/scope/claim equals its pinned slot and each subtotal is that family's declared `authorizes_subtotal`. This is ADR-0016 decision 4's *explicit composition established as coextensive*, not decision 5's implicit narrow promotion. (Supersedes the incumbent's V5 "refs every constituent," which is necessary but not one-to-one, and the rival's equivalent bijection is adopted.)

3. **Mandatory member boundary (v1): the positive taxable-interest sources.** The line-2b universe v1 comprises exactly: `int_box1` (1099-INT box 1), `int_box3` (1099-INT box 3 US-savings-bond/Treasury interest, federally taxable), `taxable_oid` (taxable OID / periodic interest on 1099-OID or substitute — **mandatory**; the Form 1040 line-2b instructions name Form 1099-OID), and `unreported_taxable_interest` (residual **positive** taxable interest with an enumerated predicate for the residual it actually covers — informal/non-form cash interest). Tax-exempt interest (Form 1040 line 2a / 1099-INT box 8, tax-exempt OID) is excluded. The incumbent's OID-deferred `{B1,B3,non-form}` universe is rejected.

4. **The composition binding is mandatory and licensed.** A new pin role `composition` is added to the shared closed vocabulary (ADR-0006 decision 9) as **provenance only** — it is not an `input`/`choice` pin and creates **no** derivation edge (ADR-0010). The line-2b symbol may be published **only** by a rule carrying a required `composition:{id,version}` pin resolving to an adopted composition whose `publishes` is that symbol; a package shipping a line-2b rule with no bound composition is rejected (defeating the vacuous-binding hole where composition audit no-ops and the rule reduces to a bare sum).

5. **Closure is read per constituent, including non-empty ones.** The line-2b rule `require_closed`s every constituent source set — a generic operation whose tax meaning comes only from the declared source set and which reuses the committed ADR-0014 current-horizon / current-literal-true admission dispatch. The line-2b finding pins every closure read. Line 2b is therefore eligible only when **every** constituent family is closed on its current horizon, **even when a constituent subtotal is a present-source non-empty value** — closing the incumbent's holes where a present-source value published without a closure read (TIC-A3) and was not displaced by a later member (TIC-A5). Box-1 closure alone can never authorize a line-2b value or zero (ADR-0016 decision 5).

6. **Honest zero and late-member lifecycle through existing edges only.** A line-2b zero publishes only when every constituent has a current literal-true closure — a coextensive zero, never box-1's zero. A late member is one atomic `member-transition` advancing the affected family's horizon (individuation root, ADR-0017); the predecessor-horizon closure finding leaves current state through individuation, and the line finding's closure/subtotal `input` pins displace the line result through derivation (ADR-0010) — no new standing-affecting edge, no manual withdrawal, no resurrected zero. Re-attestation on the successor horizon plus an explicit rerun publishes the successor.

7. **Honesty gate and deferred scope.** The universe's `required_universe.claim` states exactly which positive source families it covers and must **not** assert "total taxable interest complete." Explicitly **out of this decision**, deferred to named follow-on decisions: (a) additional *positive* taxable-interest source families (Schedule K-1 interest, market discount) — the `unreported_taxable_interest` predicate must be authored to cover only what it genuinely absorbs and must not silently claim these; (b) the *subtractive adjustment* mechanism (nominee interest, accrued interest paid at purchase, bond-premium amortization), which a sum-of-positive-subtotals composition structurally cannot express and which requires its own contract decision. Until (a)/(b) are adopted, the composition claim must be honest that line 2b is the sum of its declared positive families **without adjustments**, and content/coverage must not over-claim.

## Consequences

- Form 1040 line 2b can publish this milestone over an honest, OID-inclusive positive-source universe, blocking (never silently under- or over-reporting) rather than waiting on the entire interest taxonomy.
- New schema/content lands in Track 2: `taxable-interest-composition.v1`, the B3 / taxable-OID / residual-positive source families, mappings and subtotal rules parallel to the committed B1, the line-2b rule and form field, and the `composition` pin-role addition to the shared vocabulary.
- **PC1.** `require_closed` is implemented solely through the single ADR-0014 dispatch (no second closed-set writer); alternate runners that evaluate the refs without executing the closure ops are rejected; pin-set goldens include all closures on multi-source non-zero lines.
- **PC2.** Package validation enforces the slot bijection one-to-one (rejecting duplicate constituent references) and the mandatory composition binding non-vacuously.
- **PC3.** Lifecycle: atomic member-transition (ADR-0017 decision 3), dual-family reclassification admission, and `conflict_semantics` resolution that cannot elect a non-composition producer for the line-2b symbol.
- **PC4.** The deferred follow-on decisions (further positive sources; subtractive-adjustment mechanism) are tracked; line 2b's adopted claim text is kept honest to the current universe.

## Alternatives Considered

- **Incumbent scoped/versioned coextensiveness `{B1,B3,non-form}` (it1 TIC-P1).** Rejected: omits taxable OID while publishing line 2b — ADR-0016 decision 4/5 narrow promotion (TIC-G1, TIC-A1).
- **Publication gated on coverage but not on per-constituent closure reads (it1).** Rejected: present-source open-family publication and present-source late-member non-displacement (TIC-A3, TIC-A5).
- **Optional / package-only composition binding (it1).** Rejected: vacuous when no composition citizen is present (TIC-A7); the binding must be mandatory and licensed.
- **A residual `unreported` slot as proof of completeness (both designs).** Rejected: a residual label absorbs nothing it does not enumerate; further positive sources need real predicates (TIC-A2).
- **Requiring the full taxable-interest universe (all positive sources + subtractive adjustments) before any line-2b publication.** Considered and not chosen (owner scope decision 2026-07-14): it blocks line 2b behind a separate adjustment-mechanism decision; the honesty gate lets line 2b ship correctly over its declared universe instead.

## Links

- Evidence: `docs/prototypes/taxable-interest-composition/evaluation-analysis.md`; `reviews/round-1-governance.md`, `reviews/round-1-adversary.md`; exhibits `it1/design.md` (`4ea0b6c`), `it2/design.md` (`f3ccb43`).
- Supersedes: ADR-0021 (inert, retained) and its spike.
- Contracts: ADR-0016 (source-family claim/composition), ADR-0014 (closure/admission), ADR-0017 (horizons), ADR-0010 (edges), ADR-0006 (shared vocabulary, conflict semantics), ADR-0012 (dispositions).
- Deferred follow-ons: additional positive taxable-interest sources (K-1, market discount); subtractive-adjustment mechanism (nominee / accrued-at-purchase / premium).
