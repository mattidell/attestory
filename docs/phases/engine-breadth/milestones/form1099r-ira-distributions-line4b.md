<!-- foreman-context-v1
{
  "version": 1,
  "topic": "form1099r-ira-distributions-line4b",
  "milestone_state": "track-0",
  "status": "PLAN COMMITTED. Track 0 is foreman-owned; implementation seats are prepared for owner launch and no agent has been dispatched.",
  "source_ref": "origin/main",
  "source_commit": "b0480bc2178ba7d2fd8baa59b1a6823e5aa5c4a0",
  "scope": [
    "admit the bounded 2025 fully taxable IRA-family Form 1099-R class",
    "publish Form 1040 line 4b, keep line 4a blank for the fully taxable class, and carry line 4b through line 9, AGI, taxable income, and regular tax",
    "resolve package, explanation, exact citations, and production-shaped presentation"
  ],
  "non_goals": [
    "no IRA basis, Form 8606, rollover eligibility, Roth qualification, or special distribution treatment",
    "no non-IRA pension, annuity, qualified-plan, or insurance distributions",
    "no withholding, Form 5329, Form 5498, Form 1098-Q, or state treatment"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md",
      "docs/adr/0011-tax-fact-identity-and-source-closure.md",
      "docs/adr/0014-adopted-source-closure-mapping.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0028-package-fact-surface-and-composition-obligation.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/content/tax/2025/rule.form1040-line9.v4.json",
      "packages/content/tax/2025/rule.form1040-line11.json",
      "packages/content/tax/2025/rule.form1040-line15.json",
      "packages/content/tax/2025/rule.form1040-line16.v5.json",
      "packages/content/tax/2025/package.core-calculations.v17.json",
      "packages/content/tax/2025/published-packages.v12.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md#Evidence matrix",
      "docs/adr/0011-tax-fact-identity-and-source-closure.md",
      "docs/adr/0014-adopted-source-closure-mapping.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol",
      "PROJECT_PLANNING.md#Milestone Closeout"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->
# Milestone: Fully Taxable IRA Distributions from Form 1099-R to Form 1040 Line 4b

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by owner direction on 2026-08-04.

## Objective

Make a bounded 2025 return class computable end to end: one or more
IRA-family Form 1099-R statements report ordinary, fully taxable distributions,
the authoritative taxable amount is published on Form 1040 line 4b, line 4a
remains blank for the fully taxable class, and taxable line 4b flows exactly once
through the successor total-income computation on line 9, AGI, taxable income,
and the existing regular-tax path.

This milestone is independent of the concurrent Schedule D/Form 8949
milestone. It uses a separate clean worktree and branch from `origin/main`.
No agent has been dispatched; all prepared seats are owner-launched.

## Base and concurrency record

- Source ref: `origin/main` at `b0480bc2178ba7d2fd8baa59b1a6823e5aa5c4a0`.
- Milestone branch: `milestone/form1099r-ira-distributions-line4b`.
- Dedicated clean worktree, separate from the concurrent WIP checkout.
- Concurrent work at planning time: draft PR #161,
  `milestone/schedule-d-form8949-covered-wash-sale`, with a dirty WIP
  worktree and 13 commits ahead of `origin/main`. That worktree is untouched.
- The branch currently observes package core `v17` and published registry
  `v12`; these are inventory facts, not reservations. No new schema, rule,
  package, registry, release, adoption, or ADR number is allocated by this
  plan.

If concurrent work changes the base, re-fetch and re-identify the ratified
line. Before the real rebase and again during final PR preparation, run the
established ephemeral three-way semantic-ledger diagnostic: capture this
branch's intended package/member, entrypoint, admitted-schema, input-binding,
and composition-obligation delta; compare it against the common ancestor and
the new ratified tip; and use a negative control. Lost upstream members,
altered producer selections, lost schema admissions, or lost composition
obligations are blocking unless this milestone explicitly justifies them.
The diagnostic is temporary, ignored, and removed before closeout.

## Official 2025 paper boundary

The paper boundary is grounded in the 2025 IRS sources:

- [2025 Form 1040 instructions](https://www.irs.gov/instructions/i1040gi),
  lines 4a and 4b: a fully taxable IRA distribution is entered on line 4b,
  with no line-4a entry.
- [2025 Instructions for Forms 1099-R and 5498](https://www.irs.gov/pub/irs-prior/i1099r--2025.pdf),
  for box 1, box 2a, box 2b, the IRA indicator, and distribution codes.
- [Publication 590-B (2025)](https://www.irs.gov/publications/p590b),
  for the distinction between fully taxable distributions and distributions
  requiring basis or other treatment.

The supported class is exactly: tax year 2025; an IRA-family indicator for a
traditional IRA, SEP IRA, or SIMPLE IRA; normal distribution code `7` with no
additional code; nonnegative box 1; box 2a present and nonnegative; box 2b
not asserted; and box 2a equal to box 1. The family is closed affirmatively,
and every accepted statement is included exactly once. This is a statement-
reported fully taxable amount, not an engine calculation of basis or
eligibility.

## Gate-1 decision inventory and Track 0

Track 0 is foreman-owned and paper-first. It records the exact paper examples,
two positive instances, two meaningful negatives, one correction/closure
lifecycle, the producer → authority → consumer → failure map, and the
disposition of any new contract question before implementation begins.

| Proposition | Blast | Migration | Paper uncertainty | Cheap-test gap | Planned disposition |
| --- | ---: | ---: | ---: | ---: | --- |
| R1. Form 1099-R logical-statement identity and correction | 2 | 1 | 1 | 1 | Reuse the accepted statement-instance pattern if it fully expresses 1099-R; otherwise stop for a new contract decision. |
| R2. Box-1/box-2a equality as the fully-taxable admission boundary | 2 | 1 | 1 | 1 | Require exact equality and an affirmative IRA/code-7 witness; never infer full taxation from a missing box. |
| R3. Independent source closure and line-4b composition | 2 | 1 | 1 | 1 | One closed source family, one taxable subtotal, no line-4a publication; line 9 consumes only line 4b. |
| R4. Ordinary downstream tax path | 1 | 1 | 0 | 0 | Reuse existing line-9/11/15/16 rules where their contracts remain sufficient; successor only when required by the new input. |
| R5. Package, explanation, exact citation, presentation | 1 | 1 | 0 | 0 | Implementation contract with adversarial mutations and compatibility fixtures. |

Track 0 has no rival prototype authorization. If paper cannot distinguish the
selected boundary, or an accepted contract is insufficient, stop and return
the choice to the owner; do not invent a new evaluator, identity, or special
distribution doctrine in an implementation track.

## Scope

- Add the 2025 Form 1099-R IRA-family statement facts needed to establish box
  1, box 2a, box 2b state, IRA-family indicator, and code-7 normal treatment.
- Add the source family, affirmative closure, horizon, mapping, subtotal, and
  correction/displacement tests. Multiple logical statements aggregate once;
  same-statement corrections supersede rather than double count.
- Publish the Form 1040 line-4b taxable-distribution citizen, with exact
  equality enforced against source box 1 and line 4b as the only downstream
  income addend. Keep line 4a blank/absent for this fully taxable class.
- Publish a successor line-9 rule that adds the line-4b subtotal exactly once
  alongside every existing total-income member. Verify existing line 11 AGI,
  line 15 taxable income, and line 16 regular tax consume the successor path.
- Resolve the full adopted package, release, registry, and user adoption;
  produce durable explanation walks with semantic citation pins; and add one
  canonical positive production-shaped presentation model plus compact
  blocked/redacted mutations.
- Preserve all existing W-2, interest, dividend, Schedule B, Schedule D,
  and line-16/QDCG behavior with focused unmodified regressions.

## Non-goals

- No IRA basis, nondeductible contributions, Form 8606, pro-rata allocation,
  Roth ordering or qualified distributions, rollover/conversion eligibility,
  or trustee-to-trustee treatment.
- No early-distribution exceptions or additional-tax treatment, death or
  inherited distributions, QCDs, disaster distributions, excess-contribution
  distributions, recharacterizations, or any other special code.
- No non-IRA pension, annuity, qualified-plan, insurance, or other Form 1099-R
  distribution class; no Form 1040 line 5a/5b.
- No withholding, Form 5329, Form 5498, Form 1098-Q, state returns, credits,
  deductions, filing, transmission, real-data operation, or UI redesign.
- No mutation, reformatting, movement, deletion, or checksum rewrite of a
  published schema, historical content citizen, package, release, adoption,
  fixture, or accepted ADR.

## Contracts

### IRA-C1 — Authoritative fully-taxable statement boundary

A current 2025 statement member is admissible only when its IRA-family
indicator, normal code `7`, box-1 amount, box-2a amount, and explicit box-2b
negative state are all present and valid; box 2a equals box 1 exactly. Any
missing, unequal, code-combined, non-IRA, or special-treatment witness blocks
the bounded family. The engine does not calculate or infer taxable amount.

### IRA-C2 — Identity, family, and closure

Use a logical Form 1099-R statement identity, not an upload, scan, file, or
evidence id. The identity must distinguish two original statements and preserve
same-statement correction history. The source-family claim names exactly the
accepted IRA-family/code-7/box-equality universe. Closure is affirmative-only,
current-horizon pinned, and required for an empty-source zero; false, absent,
stale, duplicate, or displaced closure blocks.

### IRA-C3 — Line 4b and successor line 9

The equal fully-taxable subtotal publishes line 4b. Line 4a has no value for
this class, consistent with the 2025 Form 1040 instructions. Only line 4b is
an addend to total income. Line 9 must not read raw statement members, line 4a,
or line 4b twice. Existing line 11 AGI,
line 15 taxable income, and line 16 regular tax remain ordinary downstream
consumers of the resulting total-income/taxable-income symbols.

### IRA-C4 — Explanation, citations, and presentation

The closing record and explanation walk identify the statement facts, family,
mapping, horizon, closure, box-equality admission, line 4b rule, line 9,
AGI, taxable income, and regular tax pins. Form-field citations use exact
adopted citation citizens for Form 1099-R and Form 1040 line 4b, line 9, line 11,
15, and 16; no URL-only or legal-verification claim is sufficient. The
presentation is zero-authority and must show a real value only when its source
is published, while blocked siblings remain visible and rejected values are
redacted.

## Evidence matrix

All committed values and identities are synthetic and use `demo.*` labels.

| ID | Case or mutation | Expected result |
| --- | --- | --- |
| P1 | One IRA-family code-7 statement, box 1 = box 2a | Family, line 4b, line 9, AGI, taxable income, and line 16 publish; line 4a remains blank. |
| P2 | Two distinct statements/payers | Identity remains distinct; taxable amounts aggregate exactly once and line 4a remains blank. |
| P3 | Same logical statement correction | Prior finding is superseded; no double count; explanation pins current finding. |
| P4 | Closed-empty family with explicit closure | Line 4b may publish a closure-backed zero while line 4a remains blank; missing closure never implies zero. |
| P5 | Ordinary existing income plus IRA distribution | Line 4b is added once; line 9/11/15/16 change by the ordinary downstream amount. |
| N1 | Box 2a missing, box 2b true, or box 1 ≠ box 2a | Bounded family and downstream lines block honestly. |
| N2 | Non-IRA indicator, code other than 7, or multiple codes | Statement is outside the class and cannot enter line 4b. |
| N3 | Roth, rollover, QCD, death, early, disaster, or excess-contribution code | Special-treatment class blocks; no basis or exception logic is invented. |
| N4 | Open, false, stale, duplicate, or displaced closure | No empty-source publication; affected downstream explanations identify the block. |
| N5 | Raw member or line 4a injected into line 9 | Package/rule/runner tests prove no alternate authority or double count. |
| N6 | Existing W-2/interest/dividend/Schedule B/Schedule D fixtures | Compatibility behavior remains unchanged. |
| P6 | Positive presentation model | Line 4a is blank; line 4b and downstream lines show values, exact citations, and a walkable explanation. |
| N7 | Blocked or malformed presentation | Section-level block is visible, no rejected value is echoed, and healthy siblings survive. |

## Tracks and review structure

### Track 0 — Paper boundary and contract checkpoint

Foreman-owned. Record the Gate-1 paper evidence, exact IRS anchors, identity
decision, equality boundary, and ADR disposition. No agent launch is needed.

### Track 1 — Source family and Form 1099-R line 4b

Owner-launch one Builder against `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-track1.md`.
Implement the source facts, statement identity, family/closure/mapping,
line-4b citizen, citations, lifecycle evidence, and focused tests; line 4a
remains blank for the admitted fully taxable class.
The builder does not allocate successor versions until the rebase inventory
required by this plan is complete.

### Track 2 — Downstream, package, explanation, and presentation integration

After Track 1, owner-launch one Builder against
`docs/reviews/charter-2026-08-04-form1099r-ira-line4b-track2.md`.
Implement the line-9 successor and downstream proof, package/release/adoption
successors, exact explanation pins, production-shaped presentation, and
compatibility regressions.

### Review, repair, and re-review

Owner-launch the independent Reviewer charter only after both tracks are
complete. At most one findings-only repair cycle is prepared for the original
Builder assigned by the owner, followed by a re-review of the semantic delta.
A new product decision, lost upstream semantic ledger member, or scope
expansion stops for owner disposition.

## Version and rebase discipline

No future version number appears in this plan or its charters. Before any
implementation packaging, after any rebase, and before final PR preparation,
inventory all published tax schemas, form/rule/citation/content citizens,
package, registry, release, adoption, and presentation versions. Choose only
unused additive successors after that inventory. Existing bytes and manifest
rows remain immutable.

## Durable commit structure

1. This planning commit: plan, phase state, roadmap/frontier selection,
   charters, and owner-launch prompts; no implementation.
2. `track-0:` paper boundary and contract checkpoint.
3. `track-1:` source family and line 4b.
4. `track-2:` line 9/downstream/package/explanation/presentation integration.
5. Provisional review/repair commits folded into the completed track.
6. Curated closeout commit with retrospective and final phase state.

## Exit criteria

The bounded source class is synthetic complete; all negative boundaries block
honestly; line 4a remains blank while line 4b enters line 9 exactly once; AGI,
taxable income, and regular tax remain on the
existing path; package/release/registry/adoption and exact citation pins
resolve; explanation and presentation satisfy their contracts; all named
compatibility regressions pass; the independent review returns READY after at
most one repair cycle; the semantic-ledger rebase and final-PR diagnostics
show no lost upstream semantics; CI is green; and the owner merges the one
curated milestone PR.
