# Deferral Ledger: Covered Form 1099-B Wash-Sale Adjustments through Form 8949 and Schedule D Lines 1b/8b

Closed 2026-08-05. See the retrospective
(`docs/milestone-retrospectives/2026-08-05-schedule-d-form8949-covered-wash-sale.md`)
for the full account.

## Retired for this bounded class

- Covered, basis-reported Form 1099-B transactions routed to Form 8949
  solely by broker-reported box-1g code W, the amount accepted as correct —
  short-term through Part I/box A/Schedule D line 1b, long-term through
  Part II/box D/line 8b.

## Carried forward (named future work, not addressed here)

- **Noncovered / basis-not-reported Form 8949 transactions** — its own
  candidate row on the coverage frontier; needs a distinct basis-source
  contract.
- **Every Form 8949 adjustment code other than W** (basis correction code B,
  accrued-market-discount code D, and the rest) — each needs its own
  authority and arithmetic.
- **Multiple codes on one Form 8949 row** — explicitly out of scope; this
  milestone is bounded to exactly one code per row.
- **Aggregate Form 8949 reporting under Exception 2** — not addressed.
- **Taxpayer-side wash-sale determination, replacement-security
  identification, and replacement-security future-basis adjustment** —
  permanently outside this engine's accepted authority boundary, not merely
  deferred; the engine accepts the broker-reported box-1g amount as
  contributed authority and does not compute it.
- **Incorrect Form 1099-B box-1g amounts (taxpayer correction/dispute)** —
  out of scope; only correction of the *contributed* fact at the same
  transaction identity is supported, not detection of broker error.
- **A `source-family.v2` schema with value-filtered membership predicates**
  — a real substrate gap named during this milestone's ADR-0061 amendment,
  deliberately deferred as disproportionate to one bounded slice; the
  identity-key collision kill-test achieves the same non-double-count
  guarantee without it.

## Discharged events, not deferrals

These were real problems encountered and resolved within this milestone,
not open items:

- The Track 0/ADR-0061 transaction-identity amendment (both originally-named
  mechanisms proved structurally unsafe; resolved and ratified).
- Track 1's three-round repair (arithmetic-masking defect; the transaction-
  identity mechanism; the unwired identity-key collision check) — all fixed
  and independently re-reviewed READY.
- The cross-milestone package/schema version collision with the merged Form
  1099-DIV Box 12 milestone — resolved as an additive union, caught before
  either PR merged via the proactive semantic-ledger dry-run.
- A mid-rebase worktree-registry incident (an unrelated concurrent session's
  worktree operation orphaned this session's working directory) — reported,
  confirmed unintentional, and recreated cleanly with no work lost.
