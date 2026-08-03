# Covered Long-Term Gains, Schedule D Line 8a — Deferral Ledger

Audience: Shared (status); Product (planning input)

Prepared 2026-08-02 with milestone closeout. This ledger names what the
reviewed slice retired and preserves the neighboring work that remains
separately selectable.

## Retired for the selected class

1. **Schedule D as a producible form.** Prior to this milestone, no
   transaction source family, Schedule D production content, or
   completeness boundary existed anywhere in the engine; box 2a alone
   could never manufacture Schedule D. The bounded covered, long-term,
   gain-only, no-adjustment Form 1099-B class now publishes Schedule D
   line 8a columns (d)/(e)/(h), Part II line 15, Part III line 16, Form
   1040 line 7a/9, and the Schedule D-bound QDCG line-16 path end to end.
2. **Attachment completeness by presence alone.** ADR-0036's generic
   completeness check validated only that a required answer exists, never
   its value — correct for Schedule B, wrong for Schedule D's
   eligibility-gating declarations. ADR-0055 adds an additive
   `check: "value"` shape; the gap is retired for any future schedule with
   the same eligibility-gating declared-absence pattern.
3. **Silent blocked/not-required attachments.** A blocked or not-required
   attachment (Schedule B's included) previously rendered no signal at all
   on the presentation surface. ADR-0056 adds a disposition-tagged
   `attachments` model key; every attachment-bearing schedule inherits
   honest visibility once it adopts the widened model.

## Capital-gain breadth carried

4. **Short-term transactions.** No source family, holding-period
   authority, or Schedule D Part I content exists. Reactivate through a
   selected short-term milestone.
5. **Capital losses, loss limitation, and inbound carryovers.** No loss
   arithmetic, the $3,000 limitation, or a carryover source/authority
   exists. This milestone's completeness boundary only detects and blocks
   on their presence; it computes none of them.
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
   boundary — the completeness boundary's ninth component only detects and
   blocks on their presence.
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

- Track 2's builder self-identified a fidelity gap mid-charter (the
  `selected-preferential-base` guard's discriminator check risked leaking
  a spurious proceeds-family pin into the direct-producer branch) and
  resolved it before commit, per ADR-0052 Decision 4's exact pin table —
  confirmed by the Track 2/3 independent review.
- Two production conditions were flagged by their own builders exactly
  where their charters anticipated stopping (attachment
  completeness-value semantics after Track 2; attachment
  blocked/not-required presentation visibility after Track 3), each
  resolved through a paper-spike-plus-ADR-draft decision unit and a
  separate implementation charter (ADR-0055, ADR-0056) rather than
  improvised in place.
- The Track 2/3 independent review returned `READY` on the first pass; no
  repair cycle was needed.
