# Current-Year Capital Losses and Schedule D Line 21 — Deferral Ledger

Audience: Shared (status); Product (planning input)

Prepared 2026-08-03 with milestone closeout. This ledger names what the
reviewed slice retired and preserves the neighboring work that remains
separately selectable.

## Retired for the selected class

1. **Short-term transactions and current-year capital losses.** Prior to
   this milestone, no short-term source family existed at all, and the
   only accepted long-term family (ADR-0052) was ratified gain-only by
   decision — it structurally excluded losses. This milestone adds an
   additive successor long-term family (gain-or-loss) and a new
   short-term family (ADR-0057), each independently closed, and computes
   signed Schedule D lines 1a/7/8a/15/16 plus the §1211 current-year
   $3,000/$1,500 capital-loss limitation (line 21, ADR-0058).
2. **Route selection for non-long-term-gain returns.** The prior
   `selected-preferential-base` discriminator could not select Schedule D
   for a short-term-only or loss-only return. The successor discriminates
   on either family's closed-nonempty state, with an exact per-branch pin
   table proving no untaken family's inputs leak into the taken branch.
3. **Negative values reaching the preferential-rate computation.** The
   successor floors the Schedule D branch to nonnegative at the producer
   (`max(line16, 0)`), not by asking the QDCG consumer to re-floor;
   verified both at the coordinator layer (Track 1) and independently at
   the presentation layer (Track 2) that the floored/signed values are
   projected honestly, never coerced or dropped.
4. **Two of the seven completeness boundary declarations.**
   `no-short-term-transactions` and `no-current-capital-losses` are
   retired as declared-absence claims, replaced by the two families' own
   closure authority. The remaining five
   (`no-inbound-capital-loss-carryovers`, `no-form8949-sources`,
   `no-other-schedule-d-sources`, `no-lines-18-19-sources`,
   `no-1099da-or-qof`) are unchanged in meaning.

## Capital-gain breadth carried

5. **Inbound capital-loss carryovers.** No prior-year-amount source, its
   own completeness authority, or 2026 carryforward derivation and
   publication exists. This milestone's completeness boundary only
   detects and blocks on the declaration's presence and value; it computes
   no carryover, inbound or outbound, in either direction. This is a
   deliberate, owner-confirmed bound (ADR-0058 Decision 7), not an
   oversight.
6. **Form 8949 transactions and adjustments.** Noncovered securities,
   basis corrections, wash sales, and adjustment codes remain outside the
   engine. The completeness boundary blocks honestly when any is present;
   none is computed.
7. **Noncovered securities and digital assets (Form 1099-DA).** No source
   family or authority exists for either.
8. **Other Schedule D sources.** K-1 capital gains (box 9/10), Forms 2439,
   4684, 4797, 6252, 6781, 8824, and lines 18/19 special-rate sources (28%
   collectibles rate gain, unrecaptured section 1250 gain) remain outside
   this milestone. Each requires its own selected source and consumer
   boundary.
9. **QOF (Qualified Opportunity Fund) flow.** No deferral or basis-step-up
   authority exists.

## Other breadth and infrastructure carried by reference

10. **Subtractive interest adjustments.** Nominee interest, accrued
    interest at purchase, and bond-premium adjustments still lack an
    authority, arithmetic, and explanation contract. Carried from the
    K1-interest-breadth and market-discount-interest ledgers; unaffected
    by this milestone.
11. **Other K-1 content, partnership computations, and historical
    migration/live-run/infrastructure items.** Unaffected by this
    milestone; see the K1-interest-breadth deferral ledger's entries 5-7
    for their standing triggers.

## Discharged events, not deferrals

- Track 0's paper-first decision record settled all six named contract
  questions (D1-D6) against real committed source, not assumption, before
  any implementation charter was written; no rival shape was found that
  required Gate 1 escalation to a full prototype round.
- Track 1's independent review found the arithmetic and routing correct by
  direct inspection, but named four fixture-coverage and disclosure
  findings (an untested Q>0/net-loss QDCG interaction, an undisclosed
  MFS-fixture workaround for a pre-existing bracket-table gap, several
  missing named fixtures, one dead helper). One findings-only repair round
  closed all four with substantive fixtures — pin-membership double-count
  checks, distinct violated-vs-missing completeness codes, unclosed-family
  blocking — rather than disposition rubber-stamping. The recheck was
  `READY`.
- Track 2's independent review found no findings; its goldens assert
  actual projected numeric values (not just dispositions), proving the
  presentation layer shows the true signed/floored amount rather than
  coercing or dropping it.
