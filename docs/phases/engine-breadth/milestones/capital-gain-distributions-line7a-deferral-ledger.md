# Capital-Gain Distributions and Line 7a — Deferral Ledger

Audience: Shared (status); Product (planning input)

Prepared 2026-07-31 with the Track 4 completion records. This ledger reconciles
work created, touched, retired, or reaffirmed by the milestone. A future unit
retires an entry only by naming this ledger and supplying its own reviewed
evidence.

## Retired for the selected class

1. **Box 2a recorded/non-composable block — narrowly retired.** The block
   carried from the Dividends and Schedule B ledger (entry 4) is retired only
   for returns whose contributed C1–C4 authority selects ADR-0050's direct
   route. A successor horizon-closed box-2a family supplies Form 1040 line 7a.
   Historical recorded content remains immutable, and this retirement does not
   cover Schedule-D-required returns or any other capital-gain source.

## Capital-gain breadth carried

2. **Schedule D and its source scope.** No Schedule D artifact is produced.
   Reactivate only when an owner-selected milestone establishes the sources,
   completeness, netting, attachment, and explanation boundary for returns
   that require Schedule D.
3. **Form 8949, Form 1099-B, and transaction-level gains or losses.** These
   remain distinct source and computation work, not implied by box 2a support.
   Reactivate when a selected Schedule D or transaction-source milestone names
   their identity, correction, closure, and downstream contract.
4. **Capital-loss carryover.** No carryover authority, lifecycle, or
   computation was selected. Reactivate when a milestone explicitly adds
   prior-year loss authority and its Schedule D consumer.
5. **Qualified-opportunity-fund flow.** C3 contributes only the bounded
   statement that no QOF deferral applies; it creates no QOF source or
   computation. Reactivate when a selected milestone supports a positive QOF
   case rather than the direct-route exclusion.

## Form 1099-DIV exclusions carried

6. **Boxes 2b, 2c, and 2d.** C4 is return-level eligibility authority only;
   it is not a member, family, closure, mapping, or collection path. Reactivate
   when one or more boxes form a coherent selected downstream slice with
   explicit source completeness.
7. **Boxes 2f, 3, 5, 7, and 12.** These remain recorded/non-composable or
   otherwise outside the successor family. Reactivate per box or coherent
   group only after its downstream tax meaning and completeness boundary are
   selected. No general “other dividend boxes” milestone is inferred.

## Other breadth carried

8. **Further positive interest sources.** K-1 box 5 interest and market
   discount remain outside line 2b's declared universe (ADR-0026). Reactivate
   through an owner-selected interest-breadth milestone.
9. **Interest subtractive adjustments.** Nominee, accrued, and premium
   adjustments remain without an authority and explanation contract.
   Reactivate through a selected subtractive-adjustment milestone.

## Migration and infrastructure carried by reference

10. **Historical-v1 migration.** The ADR-0028 migration entry remains
    untouched. This milestone used additive successor versions; it did not
    migrate historical content. Full history and trigger:
    `correction-authority-and-marshaller-simplification-deferral-ledger.md`
    entry 9.
11. **Live-run authority separation and guarded publication transport.** Both
    remain unimplemented and separately selectable; this synthetic breadth
    milestone touched neither control. Full distinction and triggers:
    `correction-authority-and-marshaller-simplification-deferral-ledger.md`
    entry 4.
12. **Other untouched infrastructure and operating items.** Operator-level
    bypass, private-remote posture, `closed-on-attestation` cross-scope
    projection, split-registry/bad-checksum corpus fixtures, failed-batch
    record shape, and scaffold visibility retain their prior dispositions and
    triggers. See the three Real Return deferral ledgers named in this
    milestone's Track 4 charter; no history is rewritten here.

## Presentation compatibility carried

13. **Legacy owning rules without a `citations` declaration.** Track 3's
    generic presentation repair validates the exact field → owning rule →
    resolved citation chain when the owning rule declares citations. Existing
    legacy rules with no declaration retain their prior compatibility path.
    This is preservation, not validation or backfilling of citation chains.
    Reactivate only through an explicit migration/contract unit that versions
    those rules and packages and defines the new citation obligation.

## Discharged events, not deferrals

- Prototype Repair 1's incomplete component/pin shape was superseded by the
  final Rung-1 repair and accepted ADR-0050.
- Track 1 F1, Track 2 F1/F2, the Track 2 CI consistency/type failures, the
  line-7b prerequisite CI failures, and Track 3 F1–F3 were repaired and
  independently rechecked `READY`.
- Track 3's line-7b prerequisite stop correctly exposed a missing package
  successor and was discharged by the reviewed prerequisite merged in PR
  #125.
- The first Track-3 citation-repair charter stopped cleanly at the legacy-rule
  wall. No implementation landed under that defective scope; the amended
  generic invariant completed without retrofitting legacy rules.
