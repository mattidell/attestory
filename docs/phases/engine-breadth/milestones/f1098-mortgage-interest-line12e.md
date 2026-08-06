<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098-mortgage-interest-line12e",
  "milestone_state": "planned",
  "status": "Track 0 (paper-first scope contract) authored and committed by foreman 2026-08-05, base core-calculations v21 / published v16 / release v14 / adoption v21. Track 1 chartered; not yet built. No dispatch this session per owner instruction — owner-launch only.",
  "current_role": "Builder (Track 1)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md#Track 1 charter",
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
      "packages/content/tax/2025/package.core-calculations.v21.json",
      "packages/content/tax/2025/published-packages.v16.json",
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
- Status: **planned** — Track 0 settled by foreman paper analysis; Track 1
  chartered below; not yet built.
- Base: `tax.us.2025.package.core-calculations` v21 / published v16 /
  release v14 / adoption v21 (tip of `origin/main` at `20a67ce`, immediately
  after Form 1099-DIV box-7 direct FTC).
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

## Stop condition (a) resolution — 2026-08-05

A Track 1 builder correctly stopped rather than inventing a mechanism: the
existing closed-family/closure machinery (ADR-0016/0017) proves "every
statement is recorded," not "no more than one statement exists." Statement
identity must distinguish a *correction* to the same mortgage (same identity
key → supersession, collapses to one member) from a *second, genuinely
different* mortgage (different identity key → a second concurrent member) —
that is the entire purpose of identity keys, so cardinality cannot be
enforced by identity alone. Checked `packages/schemas/derivation/rule-artifact.v3.schema.json`:
its `op` vocabulary is explicitly enumerated (`add`, `max`, `collect`,
`require_closed`, `compare`, …) and has no count/cardinality primitive, and
`packages/derivation/evaluator.py` has no such op either. This is a genuine,
narrow interpreter gap, not a paper-only ambiguity — resolved on paper here
rather than invented mid-build:

- Add one new evaluator op, `"op": "count"`, evaluating to the integer
  length of a `collect`'s admitted-member list for a given `source_set`
  (same shape as `collect`: `{"op": "count", "name": ..., "source_set": ...}`),
  gated by the same `require_closed` semantics `collect` already uses.
- This is an additive, narrow primitive — not new governance or generic
  substrate — but it is a schema change: bump `rule-artifact.v3` to
  `rule-artifact.v4` (additive-only, per the existing v1→v2→v3 precedent in
  `packages/schemas/derivation/`), admit `rule-artifact.v4` into the
  successor package alongside `.v3` (both remain valid; existing `.v3`
  citizens are untouched).
- `tax.us.2025.rule.schedule-a-line8a` (and any other rule reading the
  family) guards on `compare(count(...), 1, "eq")` after `require_closed`;
  a count of 0 means "no Form 1098 statement — out of this milestone,"
  count of 1 proceeds, count > 1 blocks with a new named code
  `MULTIPLE_F1098_OUT_OF_SCOPE` (out-of-class, not incompleteness).
- **Single family, not a per-box split.** `family.f1098.json` (member
  predicate = box-1 interest, since that is the amount that ultimately
  flows to line 8a) is the correct shape and should be kept. Box 2
  (outstanding principal), box 3 (origination date), boxes 4/5/6 (guarded
  exclusions), boxes 7–9 (property), and box 11 are **companion facts
  pinned to the same statement identity** — matching this codebase's
  existing "box-9 companion" / "box-13 companion" pattern used for other
  multi-box statements (Form 1099-INT box 8/9, Form 1099-DIV box 12/13) —
  not separate closed families each needing their own closure proof.
  `family.f1098-b1.json`, `family.f1098-b2.json`,
  `closure-mapping.f1098-b1.json`, and `closure-mapping.f1098-b2.json`
  should be discarded; `closure-mapping.f1098.json` (already keyed to the
  single family) is correct as committed.
- `rule.schedule-a-line8a.json`'s `when` should read
  `{"op": "count", ...} == 1` over the single `tax.us.2025.f1098` family
  (not `require_closed` on a `b1`-only source set), with box 2 consumed as
  a plain `ref` to the companion fact once closure/count both pass.

Resume Track 1 with this resolution; no other stop condition was reported.

## Owner-launch prompt (Track 1 resume)

```
Resume as builder on branch milestone/f1098-mortgage-interest-line12e,
continuing Track 1 of
docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md
after the foreman's stop-condition-(a) resolution (see that section, dated
2026-08-05). Concretely: discard family.f1098-b1.json, family.f1098-b2.json,
closure-mapping.f1098-b1.json, closure-mapping.f1098-b2.json. Keep
family.f1098.json, closure-mapping.f1098.json, f1098.bundle.json,
schedule-a-boundary.bundle.json. Add a new evaluator op "count" to
packages/derivation/evaluator.py (integer length of a collect's admitted
members for a source_set, gated by require_closed like collect already is),
and bump rule-artifact.v3 to a new additive rule-artifact.v4 schema
(packages/schemas/derivation/) admitting the new op — schema-manifest
change must be additive only, v3 stays valid and unedited. Rewrite
rule.schedule-a-line8a.json's `when` to require count(tax.us.2025.f1098) ==
1 after require_closed, blocking with a new code MULTIPLE_F1098_OUT_OF_SCOPE
on count > 1, treating count == 0 as out-of-milestone (not this rule's
concern). Then continue the rest of Track 1 scope unchanged: the seven
taxpayer-authority fact types, the remaining Schedule A completeness
boundary, and lifecycle/correction/duplicate evidence. Stop and report again
if stop condition (b) or (c) is hit.
```

## Owner-launch prompt (Track 1, cold start)

```
Resume as builder on branch milestone/f1098-mortgage-interest-line12e,
charter Track 1 of
docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md.
Run: python3 tools/build_orientation_block.py --ref HEAD
Follow docs/roles/builder.md. Build exactly the Track 1 scope in that
milestone doc's "Track 1 charter" section: the bounded Form 1098 family
with singleton-closed identity/correction/duplicate/late-member lifecycle,
the seven taxpayer-authority fact types, the Schedule A line-8a derivation
rule, and the full Schedule A completeness boundary (every unimplemented
category published closed-absent with citation, never silent zero). Do not
touch rule.form1040-line12, rule.form1040-line15, any published package or
registry file, or the standard/itemized selection — that is Track 2. Add
production-shaped synthetic fixtures and lifecycle evidence per the
milestone's Track 0 §3/§5. Commit atomically. Stop and report if any of the
three stop conditions in the milestone's "Track 1 charter" section are hit.
```
