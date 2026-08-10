<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098-mortgage-interest-line12e",
  "milestone_state": "closed",
  "status": "Closed 2026-08-10 (PR #168). Track 0, Track 1, and Track 2 built, curated to atomic Plan/Track-1/Track-2 commits, independently reviewed READY, and CI-green on the exact pushed head. Base: core-calculations v29 / published v24 / release v22, built additively on origin/main's SSA-1099 merge (48d46f9). Interim review and repair-round records are distilled into the retrospective, not carried in this doc.",
  "retrospective": "docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/engine-breadth/coverage-frontier.md",
  "scope": [
    "admit a bounded, singleton-closed Form 1098 mortgage-interest statement family with correction/duplicate/late-member lifecycle",
    "derive deductible home-mortgage interest for Schedule A line 8a from accepted component authority, never from a contributed conclusion",
    "implement a composition-complete Schedule A for the bounded class, with every unimplemented category published as explicit closed-absent authority",
    "add successor Form 1040 line-12e, line-13a (QBI, closed-absent), line-13b (Schedule 1-A, closed-absent), and line-14 citizens, and repoint line-15 to consume line-14",
    "guard the existing generic tax.us.2025.deductions.itemized raw-assertion path off whenever a Form 1098 statement is on record, without altering its behavior for out-of-class returns",
    "implement conditional Schedule A attachment disposition (not-required / required-and-complete / required-and-incomplete) reusing the ADR-0036 ontology",
    "add production-shaped synthetic identity, correction, closure, completeness, attachment, package, explanation, and presentation evidence",
    "update the Engine Breadth coverage frontier row for Form 1098 mortgage interest from candidate to synthetic complete"
  ],
  "non_goals": [
    "no second mortgage, second home, or multiple Form 1098 statements (blocks as out-of-class)",
    "no refinancing, cash-out refinancing, home-equity or mixed-use debt, or Publication 936 average-balance calculation",
    "no pre-December-16-2017 grandfathered debt",
    "no points, mortgage-insurance premiums, refunded interest, or mortgage-interest credit",
    "no shared-borrower allocation or seller-financed interest",
    "no interest paid but not reported on a Form 1098",
    "no rental or business use allocation",
    "no Schedule A deduction category other than the selected Form 1098 interest (medical, SALT, other-interest, investment interest, charitable, casualty/theft, gambling/other all explicitly closed-absent)",
    "no QBI deduction (line 13a) or Schedule 1-A deductions (line 13b) — both published as closed-absent, not silently zero",
    "no disaster-loss standard-deduction addition, dependent-taxpayer standard-deduction reduction, MFS-spouse-itemizes forced itemization, or dual-status-alien standard-deduction exclusion — all excluded from the supported class (blocking, not inferred)",
    "no voluntary itemization when it does not exceed the standard deduction",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema, historical content citizen, or accepted ADR"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md#Track 0: paper-first scope contract",
      "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md#Track 1 charter",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "docs/adr/0056-attachment-disposition-visibility.md",
      "packages/content/tax/2025/form1040.line-12.form-field.json",
      "packages/content/tax/2025/rule.form1040-line12.json",
      "packages/content/tax/2025/rule.form1040-line15.json",
      "packages/content/tax/2025/rule.form1040-standard-deduction.json",
      "packages/content/tax/2025/package.core-calculations.v29.json",
      "packages/content/tax/2025/published-packages.v24.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md#Contracts",
      "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md#Evidence matrix",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Milestone: Form 1098 Home-Mortgage Interest through Schedule A and Form 1040 Line 12e

- Phase: Engine Breadth
- Status: **closed 2026-08-10** (PR #168) — Track 0 (paper-first scope
  contract), Track 1 (Form 1098 family, Schedule A line 8a), and Track 2
  (line-12e succession, Schedule A attachment, package build) are all built,
  independently reviewed READY, and CI-green. Interim review/repair-round
  detail is distilled into the retrospective, not carried here.
- Base: `tax.us.2025.package.core-calculations` v29 / published v24 /
  release v22 / adoption v29 (built additively on `origin/main` at `48d46f9`,
  the merged SSA-1099 milestone).
- Branch: `milestone/f1098-mortgage-interest-line12e`.

## Track 0: paper-first scope contract

### 1. Current-engine finding that motivates this milestone

`packages/content/tax/2025/rule.form1040-line12.json` computes
`max(demo.form1040.standard_deduction, tax.us.2025.deductions.itemized)`
where `tax.us.2025.deductions.itemized` is pinned `origin: assertion` — a
raw taxpayer-contributed total with no Schedule A behind it. This is exactly
the bypass the owner flagged: nothing in the current graph *derives* an
itemized figure from component authority. Confirmed no Schedule A, no Form
1098, no QBI, and no Schedule 1-A content exists anywhere in the repo today
(`find` over `packages/` and `docs/adr/` returns nothing for any of the
four). This is greenfield, not a rename.

`rule.form1040-line15.json` computes `max(0, agi - deductions.total)`
directly — there is no line-13a, line-13b, or line-14 citizen. The single
`form1040.line-12` form-field is labeled "Standard deduction or itemized
deductions" and bound straight to `deductions.total`, i.e. it is functioning
as line 12e without being named as such and without the intervening
combine step.

### 2. Supported mortgage class (refined from the owner's proposal)

Adopted materially as proposed, unchanged in substance:

- exactly one 2025 Form 1098 statement, closed singleton family (a second
  statement blocks as out-of-class; a corrected statement replaces the
  original at the same statement identity, reusing the ADR-0015/0016/0017
  correction/closure pattern already proven for Form 1099-INT);
- box 1 interest present and nonnegative; box 2 outstanding principal
  present; box 3 origination date present and after 2017-12-15; boxes 4
  (refund), 5 (PMI), 6 (points) zero/absent — each a guarded exclusion, not
  a silent default;
- taxpayer liability and actual payment, qualified-main-home status,
  acquisition-debt purpose, no balance increase/additional advance, no
  refinance, single mortgage, no shared borrower outside a joint-filing
  spouse, no mortgage-interest credit, and no deductible interest outside
  the selected Form 1098 are each a **taxpayer-asserted authority fact**
  (Form 1098 does not and cannot establish any of these — see §3);
- all other Schedule A categories explicitly closed absent;
- taxpayer eligible for the engine's already-supported standard-deduction
  computation (filing status, age, blindness); no forced itemization; no
  voluntary itemization when it does not dominate;
- QBI (line 13a) and Schedule 1-A (line 13b) explicitly absent.

### 3. Form 1098 box inventory and taxpayer-authority ceiling

| Box | Classification | Reason |
| --- | --- | --- |
| 1 (interest received) | required authority | the deductible-interest candidate amount |
| 2 (outstanding principal) | required authority | debt-limit mechanical proof, §4 |
| 3 (origination date) | required authority | grandfather-date test |
| 4 (refund of overpaid interest) | guarded exclusion | nonzero indicates a prior-year adjustment out of bounded scope |
| 5 (mortgage insurance premiums) | guarded exclusion | separate, currently-unsupported deduction category |
| 6 (points) | guarded exclusion | separate deductibility test (may not be currently-year-deductible) |
| 7/8 (property address/securing-property description) | required authority | property identity, needed for duplicate/correction matching and to corroborate single-property |
| 9 (number of properties securing the mortgage) | required authority | must equal 1 for the bounded class |
| 11 (mortgage acquisition date, if servicer-acquired mid-year) | guarded exclusion | presence signals a transfer that this milestone does not model; must be absent |
| payer/borrower TIN, account number | required authority | statement and mortgage identity, correction/duplicate matching |

Form 1098 establishes **payment received by the lender**, not the taxpayer's
legal liability, actual payment, or the home's qualified/acquisition-debt
status — those are not information-return facts and are not asserted by any
third party in this engine's data model. The smallest fact set that
establishes deductible qualified-residence interest without accepting a
contributed conclusion is therefore: the Form 1098 box authority above,
**plus** seven taxpayer-asserted boolean/categorical facts (liable-and-paid,
qualified-main-home, acquisition-debt-use, no-balance-increase,
no-refinance, single-mortgage-single-home, not-shared-except-spouse,
no-mortgage-interest-credit). Each is a distinct fact type with its own
citation pin; none is inferred from box presence alone.

### 4. Debt-limit calculation — mechanical, no Pub. 936

Given post-2017-12-15 origination and the taxpayer-asserted
no-balance-increase/no-additional-advance fact, an amortizing loan's
principal is non-increasing, so box 2's reported outstanding balance is the
maximum balance for the year. The limit test is therefore a single
comparison: `box2_outstanding_principal <= acquisition_debt_limit(filing_status)`
(the $750,000 / $375,000 MFS parameter). No average-balance worksheet is
needed for this scope; if the no-balance-increase assertion is absent or
false, the fact set blocks rather than falling through to an unsupported
average-balance path.

### 5. Schedule A completeness boundary

Per-part closed-absent declarations (consolidated only within an IRS
Schedule A part, not across parts, so each remains independently
auditable): Part I medical/dental (lines 1–4) absent; Part I taxes (SALT,
lines 5–7) absent; Part I interest lines 8b–8e (non-1098 mortgage interest,
points not on 1098) absent, line 8a supported; line 9 investment interest
absent; Part III charitable (lines 11–14) absent; Part IV casualty/theft
(line 15) absent; Part V gambling/other (line 16) absent. Every category
publishes an explicit closed-absent finding with citation — none defaults
silently to zero.

### 6. Disposition of the generic itemized assertion

The historical `tax.us.2025.deductions.itemized` fact type and every
existing package version are immutable and untouched. The successor
`rule.form1040-line12e` (replacing `rule.form1040-line12`, new symbol name
matching the corrected line) guards the raw-assertion input: **if the
Form-1098 closed family has an admitted member on the return, the itemized
side of the selection must come from the Schedule A composition total**
(a new derived symbol), and the raw assertion is not consulted. Returns with
no Form 1098 statement on record are unaffected — the legacy assertion path
remains exactly as it is today. This is the bounded guard the owner asked
for: it closes the bypass for the supported class without touching
out-of-class behavior or any historical citizen.

### 7. 2025 deduction-spine assessment — bounded additive successor, not a prerequisite repair

For this bounded class, QBI and Schedule 1-A are guaranteed absent (§2), so
line 14 is arithmetically `line-12e + 0 + 0` and the current line-15
subtraction is *numerically* correct today. But the graph has no line-13a,
line-13b, or line-14 citizen, and the "line-12" form-field is mislabeled —
it is functioning as 12e without the name, citation, or presentation to
match. This is a **small, mechanical, strictly-downstream-of-AGI** fix, and
the milestone title itself commits to landing on line 12e correctly, so
Track 0 concludes a bounded additive successor is sufficient: add
`form1040.line-12e` (correct label/citation), `line-13a` and `line-13b` as
blocking-absent citizens (published "not applicable" with citation, never
silent zero), a real `line-14` combine citizen, and repoint `line-15` (new
version) to consume `line-14` instead of the legacy `line-12` symbol. This
does not touch AGI, any income line, or any unrelated deduction — it is not
the broader deduction-spine repair the owner asked me to flag if found, and
is not being smuggled in as one.

### 8. Schedule A attachment-selection contract

Reusing ADR-0036 verbatim: the Schedule A composition total (line 8a only,
in this class) is always computed once a Form 1098 statement is on record,
independent of whether it wins. Disposition: computed total strictly
greater than the standard deduction → *required-and-complete* (or
*required-and-incomplete* if any completeness-authority fact is missing —
blocked, not "not required"); computed total less than or equal to the
standard deduction → *not-required*, deterministic tie rule favors the
standard deduction (matches the existing `max` semantics and the excluded
voluntary-itemization non-goal). The attachment disposition rule consumes
the same selection contract as line 12e, not mere presence of a Form 1098.

### 9. Worksheet vs. filed attachment

Schedule A's composition total is computed unconditionally whenever a Form
1098 statement exists (needed for the max() comparison itself). Publication
as a **filed** attachment citizen is gated by the disposition in §8, exactly
mirroring Schedule B's already-proven computed-vs-filed split.

### 10. Contract novelty

No new governance-level ontology is required. Statement/mortgage/property
identity and closure reuse ADR-0015/0016/0017 (bounded to a singleton
family); attachment existence/completeness/disposition reuses ADR-0036 and
its completeness/visibility amendments (ADR-0055/0056); explanation-walking,
presentation, package resolution, and citation resolution reuse
ADR-0020/0027/0029/0033/0046 unchanged. All reuse is content-level.

### 11. Standard-deduction eligibility carve-out

Already correctly supported: filing status, taxpayer/spouse age-65,
taxpayer/spouse blindness (`rule.form1040-standard-deduction.json`
confirmed). Not supported and not inferable from missing facts — each is a
named exclusion from the supported class, blocking rather than assumed
absent: dependent-taxpayer status, MFS-spouse-itemizes, dual-status alien,
disaster-loss addition.

## Contracts

Successor citizens this milestone adds (all additive; every predecessor
version, schema, and package remains reachable and untouched):

- `tax.us.2025.f1098` bundle/schema family (statement, mortgage, property,
  lender/taxpayer identity) + 7 taxpayer-authority fact types (§3)
- `tax.us.2025.rule.schedule-a-line8a` (derives deductible interest from the
  component authority above, blocks on any missing/failing condition)
- `tax.us.2025.attachment.schedule-a` (ADR-0036 shape; not-required /
  required-and-complete / required-and-incomplete)
- 7 closed-absent Schedule A category citizens (§5)
- `tax.us.2025.form1040.line-12e` (replaces `line-12`'s role), `line-13a`,
  `line-13b`, `line-14` citizens
- `tax.us.2025.rule.form1040-line12e` (guards the itemized bypass, §6),
  `tax.us.2025.rule.form1040-line15` v2 (consumes line-14, §7)

## Evidence matrix

Positive/negative/boundary/lifecycle cases as enumerated in the owner
charter's "Required evidence" section — carried into Track 1/2 fixture
plans verbatim; not restated here to avoid drift between this doc and the
track charters.

## Track 1 charter

**Scope:** Form 1098 family, component authority, lifecycle (identity,
correction, duplicate, late-member, singleton closure), and Schedule A line
8a derivation plus the full Schedule A completeness boundary (§5, §3 above).
Does **not** touch the standard/itemized selection, attachment disposition,
Form 1040 succession, package graph, explanations, or presentation — that is
Track 2.

**Non-goals:** identical to the milestone non-goals above; additionally,
Track 1 does not modify `rule.form1040-line12`, `line-15`, or any published
package/registry file — those land in Track 2 alongside the guard.

**Stop conditions:** stop and return to the foreman if (a) the singleton
closed-family pattern cannot bound cardinality to 1 without new ontology
(expected reuse: ADR-0016/0017 as used for Form 1099-INT, only with a
membership-count guard); (b) any Schedule A completeness category cannot be
expressed as closed-absent without inventing new absence semantics beyond
ADR-0036/0055; (c) the seven taxpayer-authority facts cannot be expressed as
plain assertion fact types under existing schemas.

**Deep reads:** see `deep_reads.implementation` in this doc's header block.

## Track 2 charter (2026-08-08, post-rebase)

**Scope:** finish the milestone. Standard-versus-itemized selection guard
(§6), Schedule A attachment disposition (§8), Form 1040 line-12e/13a/13b/14
succession (§7), package build, explanations, presentation, and goldens.
Base: core-calculations **v29** (next free after the rebased v28 tip),
published **v24**, release **v22**, admitting `rule-artifact.v4` and
`artifact-package.v22` (already built in Track 1/its repair) plus this
track's own new citizens.

**Concrete deliverables:**

1. **`tax.us.2025.rule.form1040-line12e`** (new citizen, `rule-artifact.v4`
   or later as needed): `max(standard_deduction, itemized_side)` where
   `itemized_side` is `tax.us.2025.schedule-a.line8a` **when** the
   `tax.us.2025.f1098` closed family has an admitted member, and the legacy
   `tax.us.2025.deductions.itemized` raw assertion **only** when it does not
   (§6's guard). Replaces `rule.form1040-line12`'s role; do not edit
   `rule.form1040-line12.json` itself (historical, immutable) — this is a
   new, differently-named successor citizen consumed by the new
   `form1040.line-12e` form-field, not a version bump of the old one (the
   old symbol name is wrong for 2025's actual form structure, per Track 0
   §1/§7).
2. **`tax.us.2025.form1040.line-12e`** form-field citizen (correct label,
   correct line "12e", citation), replacing `form1040.line-12.form-field.json`'s
   role for the supported class.
3. **`tax.us.2025.rule.form1040-line13a`** and **`...line13b`**: each
   publishes a closed-absent/"not applicable" disposition with citation
   (QBI and Schedule 1-A are guaranteed absent for this bounded class, per
   the milestone non-goals) — never silent zero.
4. **`tax.us.2025.rule.form1040-line14`**: combines line-12e + line-13a +
   line-13b (mechanically `line-12e + 0 + 0` for the supported class, but
   expressed as a real combine rule per §7, not hardcoded).
5. **`tax.us.2025.rule.form1040-line15`** successor (new version): consumes
   `line-14` instead of the legacy `tax.us.2025.deductions.total` symbol.
   Do not edit `rule.form1040-line15.json` (historical); add a versioned
   successor per this corpus's convention (see `rule.form1040-line16.v2`
   through `.v5` for the pattern of successive line-rule versions).
6. **`tax.us.2025.attachment.schedule-a`**: ADR-0036-shaped attachment
   citizen (not-required / required-and-complete / required-and-incomplete),
   disposition per §8 — computed Schedule A total (line 8a, the only
   populated category) strictly greater than the standard deduction →
   required; less-than-or-equal → not-required (deterministic tie favors
   standard, matching the `max` semantics already in the line-12e rule and
   the milestone's exclusion of voluntary itemization). Reuse
   `attachment.schedule-d.v4.json` or `attachment.f8949.json` as the
   closest existing shape precedent — read both before drafting.
7. **Package build**: assemble `package.core-calculations.v29.json` as the
   additive union of the base tip (v28) plus every citizen this milestone
   added across Track 1 and Track 2 (family, closure-mapping, bundle,
   boundary rules, line8a rule, and this track's new citizens). Publish
   `published-packages.v24.json` and a new release
   (`demo.release.2025.v22.json`) and adoption act, following the exact
   structure of the SSA-1099/IRA milestones' own v22-v28 package
   progression (read 2-3 of those files as the immediate precedent, since
   they're the freshest examples of this exact mechanical step).
8. **Explanations and citations**: every new rule/attachment needs a
   citation pin and walkable explanation per ADR-0020/0029, matching the
   existing corpus's citation-file convention (see
   `citation.form1040.line-4b.json`, `citation.form1040.ss-benefits-worksheet.json`
   from the base tip as the freshest precedent for form-field citation
   shape).
9. **Presentation and goldens**: production-shaped synthetic fixtures under
   `packages/sample_data/f1098_mortgage_interest_line12e/` (adoption,
   publication surface, presentation golden), following the shape of
   `packages/sample_data/form1099r_ira_line4b/` or
   `packages/sample_data/ssa1099_benefits_line6/` (both freshest, both on
   this same rebased base).
10. **Coverage frontier**: flip the Form 1098 row from `selected` to
    `synthetic complete` once Track 2 is READY.

**Required evidence** (per the original owner charter, carried forward):
deductible interest greater/less/equal to standard deduction; zero
interest; Schedule A required only when itemized wins; Schedule A not
required when standard wins; exact line 8a / Schedule A total / line 12e /
line 14 / taxable income / line 16 recomputation; the generic itemized
assertion unable to bypass the derived path when a Form 1098 statement is
on record (and still usable when one is not); exact citation/explanation
pins; package and schema-registry integrity; every existing regression
fixture (including SSA-1099's and IRA's) unmodified and passing.

**Non-goals:** identical to the milestone non-goals above. Additionally:
do not touch `rule.form1040-line16` or anything downstream of taxable
income (tax computation, credits) — this track ends at taxable income.

**Stop conditions:** stop and return to the foreman if (a) the Schedule A
attachment shape needs anything beyond content-level reuse of
ADR-0036/0055/0056; (b) the package-build step surfaces another
same-version collision or any destructive change to an existing package
version; (c) any required evidence case cannot be expressed without
touching a file outside this milestone's own citizens.
