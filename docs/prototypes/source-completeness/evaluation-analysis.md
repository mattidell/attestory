# Prototype Evaluation Analysis — Source Completeness

Foreman, 2026-07-12. Required evidence analysis for the bounded Tier-2
decisions below. Every supported conclusion cites a followable exhibit or
review. Status: complete for owner disposition and ADR drafting.

## 1. Decisions under evidence

This analysis answers separately:

1. **SC-P1:** how an adopted closure mapping authorizes empty-source collection
   only from a current literal-true closure finding;
2. **SC-P2:** what individuates a Form 1099-INT taxable-interest fact relative
   to payer, account, statement, correction, and evidence.

**SC-P3 is not decided.** The user-facing closure claim and the member,
mapping, and coverage universes did not converge. SC-D1 remains normal milestone
implementation work.

## 2. Evidence base

| Evidence | Contribution |
|---|---|
| `exhibits/source-completeness/it1` (`d47d12c`) | Dedicated reusable mapping citizen; payer/account identity rival |
| `exhibits/source-completeness/it2` (`82ffb7f0`) | Embedded-rule mapping rival; logical statement-instance identity |
| Round 1 reviews and triage | Reject incumbent identity; expose family mismatch; route schemas and caller seam |
| `repair1` (`5eee68c`) | Resolver/mutation evidence for literal-true, currency, ambiguity, exact pins |
| `repair2` (`6144b65`) | Faithful copied two-layer calculation path; publication-level negatives |
| Round 2 reviews and triage | Reject shape B evolution behavior; expose fabricable carrier |
| `repair3` (`b09d0b5`) and round 3 | Re-derivation validation; expose duck and alternate-callable bypasses |
| `repair4` (`1c3ccb1`) and round 4 | One supported entry taking only mapping/findings; no carrier parameter or exported alternate evaluator |
| `process-log.md` and round triages | Scope, cap deviations, review defects, and proposition-specific dispositions |

The rival requirement is satisfied: it1 and it2 were built in separate contexts
against the same paper requirements. Repairs are targeted evidence, not rivals.

## 3. Supported conclusions

### C1 — Closure authority uses an independently adopted reusable mapping

The selected contract is a versioned mapping citizen, adopted independently of
collecting rules. For a named source family and scope it declares the member
fact type, closure fact type/identity, and admission condition. It is pinned by
the run and reusable across collecting rules.

Evidence:

- It1 instantiates the reusable mapping for interest and W-2; it2 supplies the
  genuine embedded-rule rival.
- Round-2 adversary shows the embedded rival blocks ordinary addition of a
  second collecting rule for the same family; shape A avoids that coupling.
- Round-2 triage rejects shape B and retains shape A.

This conclusion does not define the natural-language closure claim or the full
coverage universe (SC-P3).

### C2 — Only one current literal-true closure finding authorizes emptiness

For each mapped family/scope, generic resolution reads current findings and
admits authority only when exactly one matching current finding has value equal
to boolean `true`. False, absent, displaced, truthy-non-boolean, ambiguous, and
duplicate mapping authority block. Resolution retains the exact mapping version
and exact current finding id/version used for explanation pins.

Evidence:

- Repair1's 15 tests kill presence-only, currency-blind, and truthy mutants for
  both rivals and preserve exact pins.
- Repair2's 11 tests carry the cases through a faithful copied two-layer collect
  path and kill caller-union behavior.
- Repair3 closes ordinary fabricated/duplicate carrier validation but round 3
  correctly finds duck and alternate-callable bypasses.
- Repair4 exposes one supported `compute(rule, rows, mapping, findings)` entry,
  resolves authority internally, exports no carrier/raw evaluator parameter,
  and passes 12 tests. All round-4 reviewers reproduce the central result.

The contract is **supported dispatch**, not Python access control: production
must expose and route through the validated entry only. Private naming itself is
not authority.

### C3 — Closure-backed zero and present-source computation remain distinct

Present member findings aggregate at layer 1 without consulting or pinning
closure authority. Empty members reach layer 2 and publish zero only under C2,
with the authorizing closure pin. Otherwise the result blocks.

Evidence:

- Repair2 and repair4 test present aggregation versus closure-backed zero and
  block cases.
- Round-2 expressiveness independently measures a computed zero (`5 + -5`) with
  input pins and no closure pin.
- Repair4 omitted its chartered computed-zero regression; round-4 expressiveness
  incorrectly called coverage complete. The distinction is supported by prior
  evidence but must be a production regression test.

### C4 — 1099-INT taxable-interest identity uses a logical statement instance

The fact identity includes tax year, subject, payer, and a logical Form 1099-INT
statement-instance citizen. The statement instance is peer to evidence: files,
uploads, scans, and document ids never key the fact. Multiple furnished returns
from one payer remain distinct. A corrected copy of the same logical return
answers the same fact; a separate original return is a separate statement.

Evidence:

- It2 works two same-payer statements, same-fact correction, payer-only
  collision, and document-key rejection.
- Round-1 governance passes Article 1 and multi-instance checks for it2.
- Round-1 adversary shows it1's payer/account key collides for multiple
  same-account returns and rekeys account correction; it2 survives ordinary
  correction.

Production must define a deterministic assertion/anti-duplication rule for
logical statement sameness and classify void/reissue versus correction. That is
a production condition, not permission to derive identity from evidence.

## 4. Rejected alternatives

- **Caller-supplied `closed_sets`:** rejected because it is unpinned authority
  and false/missing closure can be smuggled into empty-source publication.
- **Embedded mapping per collecting rule:** rejected because repeated rules can
  diverge and the tested duplicate-rule guard causes a family-wide outage.
- **Presence-only closure:** rejected by false-closure mutants through
  publication.
- **Payer/account interest identity:** rejected by same-account multi-return
  collision and account-correction rekeying.
- **Evidence/document identity:** rejected by Constitution Article 1.

## 5. Unresolved and production conditions

Unresolved: SC-P3 claim wording and source-family/coverage universe; SC-D1
coverage read model; citation authority; broader interest content.

Production must:

1. publish schema-first positive and isolated negative examples for mapping and
   statement citizens;
2. remove `RunContext.closed_sets` and audit every environment construction;
3. accept only the pinned adopted mapping version at the single dispatch entry;
4. add closure-authority and mapping pins to real explanation construction;
5. test false/absent/displaced/ambiguous/duplicate/caller-injection and computed
   zero on both runners;
6. prove withdrawal displaces a closure-backed zero and explicit rerun blocks;
7. define statement sameness/anti-duplication without evidence-derived keys.

Prototype code is evidence only and never merges into production.

## 6. Dissent and process quality

Round-1 SC-P3 dissent is upheld; partial ratification is intentional. Round-3
dissent drove repair4 and is resolved for the supported surface. Round-4 review
quality defects are catalogued in `round-4-triage.md`: incorrect evidence-level
labels, privacy overstatement, unsupported evolution language, and a missed
computed-zero fixture. They limit what may be cited but do not overturn C1–C4.
