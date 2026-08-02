# Paper Spike — Multi-Scalar Member Collection Substrate

Audience: Owner, Foreman.

Date: 2026-08-02. Foreman-run, Rung 1 paper only. No Builder charter, no
committee review, per owner disposition on 2026-08-02.

## Why this exists

Track 2's Builder filed a charter-stop: Track 1's eligible-transaction
member fact type, `tax.us.2025.f1099b.covered-ltcg-txn`, is object-valued —
one finding carries `proceeds`, `basis`, `gain_only`, and eight other
predicate fields together. This is exactly what ADR-0052 Decision 1
requires (a contributed/attested predicate on one member fact) and is
correct, immutable Track-1 content. But Schedule D line 8a needs two
independent numeric sums across the eligible-member set — column (d)
proceeds, column (e) basis (column (h) is `(d)-(e)`, per ADR-0052 Decision
3, not a third summed field) — and every existing collection path in the
engine assumes a scalar member value:

- `packages/derivation/evaluator.py`'s `collect` op passes each collected
  row through `_as_decimal`, which requires a single numeric literal.
- `packages/derivation/marshal.py`'s `marshal_run_context` stringifies the
  *entire* finding value into one `SourceFact.value: str` — for an
  object-valued finding this produces a Python dict repr, not a number.
- `SourceFact.value`'s declared type is `str`; every existing collectible
  precedent (1099-INT, K-1, 1099-DIV, market discount) is a single scalar
  member — none is object-valued.

Both fixes the Builder identified are explicitly named Track-2 charter-stop
conditions: editing Track 1's citizen shape, or adding new evaluator/marshal
field-projection substrate. Per `PROJECT_PLANNING.md` Gate 2, a missing
substrate discovered mid-implementation routes to its own decision.

**Gate 1 score:** blast radius 2 (whichever mechanism is chosen becomes the
template for every future multi-scalar-member source — short-term
transactions, other capital-gain forms); migration cost 1-2 depending on
shape; residual uncertainty 2 (two genuinely different shapes, not yet
compared); inability to test cheaply 1. Total ~6 — technically in the
prototype-eligible band. The owner directed the lightweight foreman-paper-
spike treatment anyway (matching the CA-05/CA-06 precedent), accepting a
single compared-but-not-adversarially-reviewed pass rather than a full
incumbent/rival committee round.

## Option A — Generic field-projection substrate

Extend `collect` with an optional field projector (e.g. `{"op": "collect",
"name": "...", "field": "proceeds"}`), change `SourceFact.value` from `str`
to `Any` (or a typed union), and change `marshal_run_context` to preserve
object-valued findings' structure instead of stringifying them, so
`collect`'s projector can pull `proceeds` or `basis` out of the shared
object member at evaluation time.

**Cost.** Touches core derivation machinery used by *every* existing rule
in the system (`evaluator.py`, `marshal.py`, `runner.py`'s `SourceFact`
type) — the blast radius is the whole engine, not just this milestone.
Every existing scalar `collect` call site would need to keep working
unchanged (backward-compatible), which is achievable but adds a real
regression surface to a component nothing in this milestone actually
requires touching if Option B works. It is more reusable: a future source
needing to project fields out of a shared object member gets it for free.

## Option B — Twin scalar collectible companions (recommended)

Leave Track 1's object-valued member fact type exactly as committed — no
edit, no version bump, no touch at all. It continues to gate admission and
serve as the audit/explanation record of the full contributed predicate.

Add two **new**, purely additive sibling fact types at the same identity
`(tax-year, subject, statement-anchor-ref, logical-transaction-ref)`, each
scalar-valued and each unconditionally admitted into its own new source
family, exactly matching every existing `collect_members` precedent's
shape:

- `tax.us.2025.f1099b.covered-ltcg-txn.proceeds` — scalar `proceeds`
  amount, its own family and closure mapping;
- `tax.us.2025.f1099b.covered-ltcg-txn.basis` — scalar `basis` amount, its
  own family and closure mapping.

The contribution act that admits an eligible transaction writes all three
findings (the object, the proceeds scalar, the basis scalar) together at
one identity, so they stay in lockstep; a correction to the transaction's
amounts is a correction to all three findings at the same identity, closed
under the same horizon-advance discipline Track 1 already established.
Schedule D line 8a's columns (d) and (e) become ordinary
`collect_members` sums over the two new scalar families, unchanged from
every existing precedent's arithmetic. Column (h) is `(d)-(e)`, per
ADR-0052 Decision 3 — no third scalar family needed. Completeness authority
#1 (ADR-0052 Decision 2, "the eligible long-term family closed") continues
to read the *original* object-valued family's closure, unchanged; the two
new scalar families' closures are additional required authorities for
Schedule D's own line-8a/13/15/16 computation, not a new completeness
category.

**Cost.** Two new fact-type/family/closure-mapping citizen sets, entirely
additive, using schemas and evaluator operations already in production
unchanged. Zero new generic substrate; zero change to `evaluator.py`,
`marshal.py`, or `SourceFact`. Zero touch to any Track-1 citizen — Track
2's existing charter boundary ("do not edit any Track-1 citizen") is
satisfied by construction, not by exception. The cost is one more
same-identity, same-horizon atomicity discipline for the contribution act
to hold (an implementation detail, not a new mechanism) and one more
citizen pair for a fresh reader to track alongside the object member.

## Disposition

Option B is recommended: it resolves the charter-stop with zero new
generic substrate, reuses 100% of existing, already-proven `collect_members`
machinery, and keeps the blast radius scoped to this milestone's own new
citizens rather than the whole engine's evaluation core. Option A is not
rejected as wrong — it is more general and would pay off if a future
source needs three or more scalar quantities per member, or needs to
project fields conditionally — but that generality is not needed by this
milestone's two-scalar case, and paying for it now is exactly the kind of
premature substrate expansion `PROJECT_PLANNING.md`'s economy discipline
warns against ("climb one rung at a time; never demand rung 4 ... in one
charter").

Recorded as ADR-0054, an additive addendum to ADR-0052 (which named
Schedule D content, including the column-(d)/(e) sums, as owed to Track 2
without specifying the collection mechanism) — not an edit to ADR-0052,
ADR-0036, or any Track-1 citizen.
