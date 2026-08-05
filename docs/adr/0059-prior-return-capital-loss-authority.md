# ADR 0059 — Prior-Return Capital-Loss Authority and Completeness Successor

- Status: **accepted** (ratified by the owner 2026-08-04)
- Tier: 2 — additive prior-return fact contract and completeness successor for
  one breadth slice; reuses existing fact-type, supersession, and displacement
  substrate without a new schema kind.
- Date: 2026-08-04

## Context

The Current-Year Capital Losses milestone (ADR-0057 / ADR-0058) made the
bounded covered, basis-reported, short-term-or-long-term, gain-or-loss 2025
Form 1099-B class synthetic complete, with Schedule D lines signed through
line 16, a current-year §1211 line-21 limitation, and a retained completeness
declaration that the return has **no inbound capital-loss carryovers**
(`tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers` in
`packages/content/tax/2025/schedule-d-boundary.bundle.json`, still
value-checked on `attachment.schedule-d.v3.json`).

The Inbound Capital-Loss Carryovers milestone must admit a **bounded 2024
prior-return authority** so the IRS Capital Loss Carryover Worksheet can
derive 2025 Schedule D lines 6 and 14 — without importing an entire 2024
return, without a 2024 package tree (none exists under
`packages/content/tax/`), and without editing accepted ADRs or historical
citizens.

Requiring the five prior-return facts unconditionally would force every
return in this class through 2024 numeric entry, including the common case
of a taxpayer with no prior-year loss at all. This ADR keeps the existing
declared-absence declaration as a cheap, honest satisfaction path instead of
retiring it, adding the full prior-return authority only as the path taken
when the declaration says carryover history exists to report.

Track 0's paper-first decision record settled this ADR's fact-identity,
completeness, and correction contracts against real committed source and the
actual IRS worksheet instructions before this ADR was drafted; it is
distilled here and in the milestone retrospective, not retained separately.

Companion worksheet arithmetic, Schedule D line 6/14 sign, carryover-only
routing, and the 2026 bound are **ADR-0060**.

## Decision

1. **Bounded prior-return authority (fixed line tuple, not a 2024 package).**
   For tax year **2025** returns in this class, admit exactly these
   **contributed scalar** fact types (exact ids fixed at Track 1 publication;
   names here are normative intent):

   | Role | Meaning (2024 return) |
   | --- | --- |
   | Form 1040 / 1040-SR / 1040-NR **line 15** | Taxable income; may be negative when the IRS worksheet requires parentheses |
   | Schedule D **line 21** | Allowed capital-loss deduction (signed loss on the 2024 return) |
   | Schedule D **line 7** | Net short-term capital gain or loss (signed) |
   | Schedule D **line 15** | Net long-term capital gain or loss (signed) |
   | Schedule D **line 16** | Combined net (signed); required for the worksheet **eligibility** precondition, not as a numbered worksheet body line |

   No other 2024 line, form, or attachment is admitted. Joint-to-separate
   reallocation and canceled-debt special handling remain out of scope and
   block honestly when those situations are the reason a carryover cannot be
   represented in this authority.

2. **Identity-key shape.** Each prior-return fact type uses:

   ```text
   identity_keys:
     - { name: "tax-year",        kind: "literal", values: ["2025"] }
     - { name: "source-tax-year", kind: "literal", values: ["2024"] }
   ```

   - `tax-year: "2025"` is the **return being prepared** (package / workspace
     year), matching every existing `packages/content/tax/2025` fact type.
   - `source-tax-year: "2024"` is mandatory so the fact cannot be confused
     with a 2025 Schedule D or Form 1040 line and cannot be silently reused
     for another source year without an additive successor type.
   - Fact type ids live under the 2025 content namespace (e.g.
     `tax.us.2025.prior-return.schedule-d.line-7`), **disjoint** from
     `tax.us.2025.schedule-d.line-7` and other 2025 line symbols.

3. **Not a multi-member source family.** The authority is a **fixed named
   line tuple**. Completeness is presence of all five current facts (Decision
   5), not `collect_members` over a family horizon. This matches the
   structural class of Schedule D boundary declarations and QDCG
   declared-absence facts (ADR-0038), not the 1099-B family class
   (ADR-0052 / ADR-0057). Supersession policy is `free`.

4. **Value shapes.** Schedule D prior lines are signed numbers (gain
   positive, loss negative), consistent with ADR-0058's signed Schedule D
   convention for the year they came from. Form 1040 line 15 may be
   negative. These are **line-result assertions**, not
   `source_amount: true` quantity-pinned 1099 members; they do not require a
   quantity-vocabulary extension unless Track 1 chooses additive quantities
   for presentation — not required by this contract.

5. **Completeness successor — two satisfaction paths, one declaration.** The
   existing `no-inbound-capital-loss-carryovers` fact type is **not
   retired**; its meaning is unchanged. Successor Schedule D attachment
   completeness item 4 is satisfied by exactly one of:

   - **Path A (declared absence).** `no-inbound-capital-loss-carryovers` =
     `"yes"`. Completeness item 4 is satisfied on this fact alone; the five
     prior-return facts are not required; Capital Loss Carryover Worksheet
     results **W8** and **W13** publish as `0` directly, citing this
     declaration as their pin (no worksheet body arithmetic runs).
   - **Path B (full authority).** `no-inbound-capital-loss-carryovers` =
     `"no"` — previously an honest permanent block outside this milestone's
     predecessor scope, now unlocked. Requires the five prior-return facts
     (Decision 1) present and current; the Capital Loss Carryover Worksheet
     (ADR-0060) runs over them and publishes **W8** / **W13**, including a
     legitimate zero result.

   The discriminator is read the same way `selected-preferential-base`
   already discriminates between its direct and Schedule D producer
   branches (`conditional_dependency_set` gating which facts are required) —
   an existing pattern, not new machinery. Downstream consumers (the
   attachment threshold, `selected-preferential-base`) read only the
   published **W8** / **W13** pair and never need to know which path
   produced them.

   The following remain value-checked `"yes"` and are **untouched in
   meaning**:

   - `no-form8949-sources`
   - `no-other-schedule-d-sources`
   - `no-lines-18-19-sources`
   - `no-1099da-or-qof`

   ST family closed, LT family closed, and box-2a family closed remain
   required authorities as under ADR-0057 / ADR-0058.

6. **Correction and displacement.** Superseding any of the five prior-return
   facts, **or the `no-inbound-capital-loss-carryovers` declaration itself**
   (including a path switch — e.g. correcting "yes" to "no" once carryover
   history is discovered, or the reverse), displaces, via existing ADR-0010
   derivation edges, at least:

   - Capital Loss Carryover Worksheet results (ST and LT carryover amounts)
   - Schedule D lines **6, 7, 14, 15, 16, 21**
   - Form 1040 lines **7a** and **9**
   - `selected-preferential-base` and Form 1040 line 16 / QDCG consumers that
     pin that base on the Schedule D branch
   - Schedule D attachment disposition pins that included the prior-return
     authority, the declaration, or carryover subtotals

   Absence of the authority (neither path satisfied) is a completeness /
   dependency failure, distinct from a present-then-corrected value or a
   corrected path selection. No new edge kind.

7. **Non-confusion invariant.** Only Capital Loss Carryover Worksheet rules
   (ADR-0060) may read `prior-return.*` symbols. 2025 Schedule D line rules
   continue to read only 2025 Schedule D symbols and current-year family
   subtotals. Package validation kill-tests any 2025 line rule that pins a
   prior-return symbol.

## Production conditions (owed to Track 1; never allowlisted)

1. Additive prior-return fact-type citizens with the identity-key shape above;
   Payload Instantiation positives and named negatives (wrong source year,
   dual identity, contribution into a non-2025 package scope).
2. Successor Schedule D attachment completeness content adding the Path A /
   Path B `conditional_dependency_set` gate on `no-inbound-capital-loss-
   carryovers`, without changing that fact type's meaning or required-answer
   status.
3. Goldens: Path A (declared no carryover, W8/W13 published as 0 without the
   five facts); Path B missing authority (blocked); Path B present authority
   with zero worksheet result; Path B correction of each of P1–P5 displacing
   the Decision 6 list; a corrected path switch (A → B and B → A) displacing
   the same list; every prior-milestone regression fixture unmodified on
   historical packages.
4. Structural proof that 2025 Schedule D line producers do not pin
   prior-return symbols.

## Consequences

- Inbound carryovers become an honest, correctable authority instead of a
  permanent absence attestation.
- Cross-year confusion is prevented by disjoint ids plus a mandatory
  `source-tax-year` literal, without inventing a 2024 package.
- Worksheet body, sign into lines 6/14, and carryover-only routing remain
  ADR-0060 so this ADR stays reviewable as a fact/completeness unit.

## Alternatives considered

- **`tax-year: "2024"` only on facts inside the 2025 package.** Rejected:
  conflicts with the universal 2025 fact-type pattern and package scope
  convention inspected in `packages/content/tax/2025`.
- **Full 2024 package / return import.** Rejected: plan non-goal; no 2024
  content tree exists; out of milestone scope.
- **Multi-member family + horizon for the five lines.** Rejected: fixed
  tuple does not need variable membership machinery; adds horizon genesis
  without a member set.
- **Reuse ADR-0052 transaction identity for prior lines.** Rejected: these
  are return-line results, not statement-instance members.
- **Retire `no-inbound-capital-loss-carryovers` and require the five
  prior-return facts unconditionally.** Rejected: forces 2024 numeric entry
  on every return in this class, including the common case of a taxpayer
  with no prior-year loss at all — an unnecessary usability regression
  against today's single-declaration checkbox for no material benefit,
  once the two-path shape carries no branching cost downstream.
- **A numeric fact-adapter: map a confirmed "no" declaration to five
  literal-zero prior-return facts instead of a completeness branch.**
  Considered. Would let downstream consumers (worksheet, attachment) read
  only the five canonical facts with no branch at all. Rejected in favor of
  the explicit two-path completeness shape: the declaration and the
  contributed facts are provenance-distinct assertions (a coarse "I had no
  carryover" attestation is not the same claim as "I am contributing a real
  2024 Schedule D line 21 of exactly zero"), and this project's existing
  `conditional_dependency_set` pattern already expresses branch-gated
  completeness without inventing an adapter/mapping mechanism.

## Links

- Track 0's decision record settled this ADR's contracts before drafting;
  distilled into this ADR and the milestone retrospective
  (`docs/milestone-retrospectives/2026-08-04-schedule-d-inbound-loss-carryovers.md`),
  not retained separately.
- Plan:
  `docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md`
- Builds on: ADR-0003, ADR-0010, ADR-0011, ADR-0032, ADR-0036, ADR-0038,
  **ADR-0052**, **ADR-0057**, **ADR-0058**
- Companion: **ADR-0060** (worksheet arithmetic, sign, routing, 2026 bound)
