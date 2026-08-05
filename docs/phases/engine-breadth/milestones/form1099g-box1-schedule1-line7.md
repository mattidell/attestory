<!-- foreman-context-v1
{
  "version": 1,
  "topic": "form1099g-box1-schedule1-line7",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099g-box1-schedule1-line7.md",
  "status": "CLOSED. Rebased onto origin/main after Form 8949 and Form 1099-INT box-8 merges; package v20 is the union of ratified v19 plus this milestone. Synthetic complete.",
  "scope": [
    "add an independent 2025 Form 1099-G box-1 unemployment source family with payer/agency, logical statement, and tax-year identity",
    "publish Schedule 1 line 7 from the closed box-1 family subtotal and introduce Schedule 1 as an attachment citizen for this bounded route",
    "settle an honest Schedule 1 line-10 completeness shape that does not claim general Schedule 1 income support",
    "publish Form 1040 line 8 from complete Schedule 1 line 10 and fold line 8 into Form 1040 line 9 exactly once",
    "carry the result through taxable income, tax, correction lifecycle, package/release/adoption, explanation, and presentation",
    "preserve W-2, interest, dividend, capital-gain, Schedule B, Schedule D, line 2a, and Form 8949 regressions on the final base"
  ],
  "non_goals": [
    "no Form 1099-G box-4 withholding computation or Form 1040 line 25b",
    "no state/local tax refunds (box 2), boxes 5-7 or 9, unemployment repayments, claim-of-right, fraud, or disputed benefits",
    "no other Schedule 1 income sources or Schedule 1 adjustments to income",
    "no general Schedule 1 completeness claim",
    "no payments, refund, balance-due, filing, transmission, real-data operation, or UI redesign",
    "no Schedule D, Form 8949, Schedule B, or line-2a contract changes as goals of this milestone"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/form1099g-box1-schedule1-line7.md#Official 2025 paper boundary",
      "docs/phases/engine-breadth/milestones/form1099g-box1-schedule1-line7.md#Contracts",
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
      "packages/content/tax/2025/rule.form1040-line9.v4.json",
      "packages/content/tax/2025/package.core-calculations.v17.json",
      "packages/content/tax/2025/published-packages.v12.json",
      "packages/content/tax/2025/line2a-scope.bundle.json",
      "packages/content/tax/2025/rule.attachment.schedule-b.v4.json",
      "packages/content/tax/2025/attachment.schedule-d.v4.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/form1099g-box1-schedule1-line7.md#Contracts",
      "docs/phases/engine-breadth/milestones/form1099g-box1-schedule1-line7.md#Evidence matrix",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
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
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-05-form1099g-box1-schedule1-line7.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md"
    ]
  }
}
-->
# Milestone: Form 1099-G Box 1 → Schedule 1 Line 7 → Form 1040 Line 8

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner on 2026-08-05. This is a new
income-domain milestone, independent of Schedule D's source contracts. It must
compose honestly with the existing Form 1040 line-9 and downstream tax graph.

**State:** closed — synthetic complete on the milestone branch; publication
gates are independent review of the curated candidate and green CI.

## Objective

Make a bounded 2025 individual return computable when one or more Forms 1099-G
report taxable unemployment compensation in box 1.

The supported amount must flow through:

1. Form 1099-G box 1;
2. Schedule 1 (Form 1040), line 7;
3. Schedule 1, line 10;
4. Form 1040, line 8;
5. Form 1040, line 9 and the existing downstream income and tax graph.

Support multiple payers or agencies, statement correction, family closure,
package resolution, explanation, and presentation.

## Preconditions and workspace discipline

Observed at plan time (isolated worktree on branch
`milestone/form1099g-box1-schedule1-line7`, sibling to primary checkout):

| Check | Result |
| --- | --- |
| `git fetch origin --prune` | Done |
| Preceding completed milestones on `origin/main` | Form 1099-DIV box 12 → line 2a merged as PR #158 (`b0480bc`); inbound capital-loss carryovers merged as PR #160 earlier on the same line |
| Active Form 8949 worktree | Present as `finances-engine` on `milestone/schedule-d-form8949-covered-wash-sale` — **not touched** by this plan branch |
| Parallel box-8 tax-exempt work | Present as `finances-engine-box8` on `milestone/form1099int-box8-line2a` (ahead of main; claims package successors) — not a precondition of this plan |
| Branch base | `origin/main` @ `b0480bc` |
| Dirty / spent | Clean; 0 ahead / 0 behind of `origin/main` at branch creation |

## Current inventory (planning base `origin/main` @ `b0480bc`)

### Form 1040 line 8

- **Absent.** No `tax.us.2025.form1040.line-8` form-field, rule, citation, or
  symbol exists under `packages/content/tax/2025/`.
- Line 9 does **not** currently reference additional income or Schedule 1.
- Historical archive prototypes noted Schedule 1 as out of scope; no production
  Schedule 1 citizen exists on the ratified line.

### Form 1040 line 9 (total income)

| Artifact | Version | Role |
| --- | --- | --- |
| `rule.form1040-line9.v4.json` | **v4** (current) | Adds wages + taxable interest + ordinary dividends + selected line-7a total |
| `rule.form1040-line9.v3.json` | v3 historical | Line 7a introduction |
| `rule.form1040-line9.v2.json` | v2 historical | Ordinary dividends |
| `rule.form1040-line9.json` | v1 historical | Wages + interest |
| `form1040.line-9.form-field.json` | v1 | Binds `tax.us.2025.income.total-income` |
| `citation.form1040.line-9.json` | v1 | Citation citizen |

**v4 requires / pins (all origin assertion):**

- `tax.us.2025.wages.total-w2-box1`
- `tax.us.2025.interest.taxable-total`
- `tax.us.2025.dividends.ordinary-total`
- `tax.us.2025.capital-gains.line7a-total`

**How line 8 is represented today:** it is **not** declared-absent and not
temporary-zero. It is simply missing from the additive total. The milestone must
introduce line 8 as a first-class publication and fold it into a **line-9 v5**
successor that adds the published line-8 amount exactly once — without changing
unrelated consumer semantics for wages, interest, dividends, or capital gains.

### Schedule 1

- No production Schedule 1 attachment, form-fields, rules, or completeness
  vocabulary on the ratified line.
- Attachment substrate in production: Schedule B (`rule.attachment.schedule-b`
  through v4) and Schedule D (`attachment.schedule-d` through v4 /
  `rule.attachment.schedule-d` through v4), both on the accepted attachment
  ontology (ADR-0036).
- Attachment-rule schemas through `attachment-rule.v6` exist (Form 8949 branch
  already uses v6 in package v18); planning base admits through the versions
  selected in `package.core-calculations@v17` / `artifact-package.v14`.

### Package, registry, release, adoption (ratified tip)

| Layer | Current tip on `origin/main` |
| --- | --- |
| Core package | `tax.us.2025.package.core-calculations@v17` (185 members, `artifact-package.v14`) |
| Published registry | `published-packages.v12` (includes v17 checksum `4091c5109afb…`) |
| Demo release | `demo.release.2025@v10` (box-12 sample surface) |
| Demo adoption | `adopt-core-v17-current` |
| Line-9 package entrypoint | `tax.us.2025.rule.form1040-line9@v4` |
| Line 2a (independent) | present; **not** an input to line 9 |
| Taxable income / tax | line 11 / 12 / 15 / 16 chain present (line 16 @ v5) |

### Parallel package graph (do not touch; integration risk)

| Branch / worktree | Package tip | Line-9 rule | Notes |
| --- | --- | --- | --- |
| `milestone/schedule-d-form8949-covered-wash-sale` (`finances-engine`) | **v18** + `published-packages.v13`; `artifact-package.v15` | still **v4** | Changes Schedule D / Form 8949 path feeding line 7a; expands package membership. Active Track 1. |
| `milestone/form1099int-box8-line2a` (`finances-engine-box8`) | owner-recorded intent for **v18/v13** | n/a for line 8 | Parallel line-2a succession; package-number collision risk with Form 8949. |

**Planning numbers are not reservations.** Final package, registry, release,
adoption, and schema successor numbers are chosen only after the last rebase
onto the ratified line immediately before packaging.

## Official 2025 paper boundary

Grounded in current official sources (fetched / consulted 2026-08-05):

| Source | URL | Confirmed routing for this milestone |
| --- | --- | --- |
| IRS unemployment compensation guidance | https://www.irs.gov/individuals/employees/unemployment-compensation | Unemployment is taxable; report Form 1099-G box 1 on **Schedule 1 line 7**; box 4 withholding on **Form 1040 line 25b**; attach Schedule 1. Page reviewed 13-Aug-2025. |
| 2025 Form 1040 instructions | https://www.irs.gov/instructions/i1040gi | Additional income (including unemployment) is reported via Schedule 1; Schedule 1 total additional income feeds Form 1040 line 8. |
| Schedule 1 (Form 1040) 2025 | https://www.irs.gov/pub/irs-pdf/f1040s1.pdf | Line 7 = Unemployment compensation (with optional repaid-overpayment checkbox/amount). Line 10 = combine lines 1–7 and 9; enter on Form 1040 line 8. |
| Form 1099-G instructions | https://www.irs.gov/instructions/i1099g | Box 1 unemployment compensation meaning and recipient reporting; other boxes have distinct treatment. |
| Publication 525 (2025) | https://www.irs.gov/publications/p525 | Taxable unemployment, repayments, and related income boundaries. |

### Paper confirmations required by owner selection

| Claim | Paper result |
| --- | --- |
| Form 1099-G box 1 → Schedule 1 line 7 | **Confirmed** (IRS unemployment page + Schedule 1 form) |
| Schedule 1 line 10 → Form 1040 line 8 | **Confirmed** (Schedule 1 line 10 instruction text) |
| Box 4 is federal withholding, not a reduction of box-1 income | **Confirmed** (IRS unemployment page: box 4 → line 25b) |
| Repayments, fraud corrections, other 1099-G boxes have distinct treatment | **Confirmed** (Schedule 1 line 7 repayment checkbox; Pub 525; box-specific 1099-G instructions) — **cannot be silently absorbed** by the unemployment family |

## Supported class

- Tax year **2025**.
- One or more **nonnegative** Form 1099-G box-1 amounts.
- Payer/agency and logical-statement identity.
- Reported box-1 amount accepted as the taxable unemployment amount.
- Box 4 **absent/null or numeric zero** only (explicit companion authority).
- No current- or prior-year unemployment repayment adjustment.
- No disputed, fraudulent, or incorrect Form 1099-G not yet reflected on an
  authoritative corrected statement.
- No other Schedule 1 income source.
- No other Form 1099-G box that would affect the federal return.
- Otherwise supported W-2, interest, dividend, and capital-gain sources may
  coexist on the same synthetic return.

## Non-goals

- Form 1099-G box-4 withholding and Form 1040 line 25b payment computation.
- State or local tax refunds in box 2.
- Boxes 5–7 or 9 and their distinct downstream treatment.
- Unemployment repayments, claim-of-right calculations, deductions, or credits.
- Unemployment fraud, identity theft, disputed benefits, or corrected amounts
  not yet reflected on an authoritative statement.
- Supplemental unemployment benefits reported as wages.
- Railroad Retirement forms or benefits not reported through the selected
  Form 1099-G shape.
- Every other Schedule 1 income source (business, rental, farm, Form 4797,
  gambling, prizes, awards, royalties, other income, etc.).
- Schedule 1 adjustments to income (Part II).
- General Schedule 1 support as a product claim.
- Payments, refund, balance-due, filing, or transmission computation.
- Schedule D, Form 8949, Schedule B, or line-2a contract changes as goals.
- Real-data operation or UI redesign.
- Mutation of any published schema, historical citizen, package, release,
  adoption, fixture, or accepted ADR.

## Track 0 — Gate-1 decision inventory and paper evidence

Track 0 is paper-first. Scores use the four Gate-1 axes (future blast radius,
migration cost, residual uncertainty after paper examples, inability to test
cheaply during implementation), each 0–2. Gate 2 requires two positive
instances, two meaningful negatives, one lifecycle trace, and a
producer → authority → consumer → failure map per proposition. If paper
distinguishes the shape, stop at paper; no rival prototype is authorized unless
Schedule 1 completeness leaves two genuinely viable shapes after paper.

| Proposition | Blast | Migration | Paper uncertainty | Cheap-test gap | Total | Planned disposition |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **P1. Form 1099-G statement identity, box-1 family, closure, correction** | 2 | 1 | 1 | 0 | **4** | Paper spike + reuse ADR-0015/0016/0017; content-level family analogous to box-12 |
| **P2. Box-4 companion authority (null/zero only; nonzero blocks)** | 1 | 1 | 0 | 0 | **2** | Implementation contract; mirror box-13 companion pattern from box-12 milestone |
| **P3. Schedule 1 line-7 attachment citizen and dispositions** | 2 | 2 | 1 | 1 | **6** | Paper first; reuse ADR-0036 attachment ontology as content; no general Schedule 1 claim |
| **P4. Schedule 1 line-10 completeness universe** | 2 | 2 | 2 | 1 | **7** | **Primary contract risk.** Paper compares alternatives below; prefer explicit absence slots + unemployment amount; escalate to rival prototype only if paper fails |
| **P5. Form 1040 line-8 publication and line-9 succession** | 2 | 2 | 1 | 0 | **5** | Paper + additive line-9 v5; exact-once line-8; preserve all existing line-9 components |
| **P6. Form 1099-G residual / other-box boundary** | 2 | 1 | 1 | 1 | **5** | Paper; smallest shape that blocks unsupported payment classes without treating box-1 closure as proof of other-box absence |
| **P7. Repayment vs correction boundary** | 1 | 1 | 0 | 0 | **2** | Implementation contract; nonnegative box-1; repayment blocks via scope authority |
| **P8. Lifecycle, explanation, pins, presentation** | 1 | 1 | 0 | 0 | **2** | Implementation contract + adversarial tests; reuse ADR-0020/0029/0046 |

**Gate-0 discipline:** P4 is the primary contract proposition. P1, P3, and P5
are tightly dependent secondaries. P2, P6, P7, P8 are implementation-boundary
obligations unless paper reveals a new product shape. If paper cannot settle P4
(and secondarily P3/P5), stop and return to the owner before any Builder
charter — do not let the Builder invent the Schedule 1 source universe ad hoc.

### Paper evidence plan (Gate 2)

**P1 identity/closure.** Positives: one agency/one statement; two agencies;
two logical statements from the same payer. Negatives: open closure; stale
closure after late member. Lifecycle: correction at same logical identity;
late member advances horizon; successor closure restores. Map: statement fact →
family horizon/closure → box-1 subtotal → Schedule 1 line 7.

**P2 box 4.** Positives: explicit null; explicit zero. Negatives: missing
companion; nonzero box 4. Map: statement + box-4 witness → route guard →
publish or hard block (never line 25b).

**P3 attachment.** Positives: required Schedule 1 when unemployment publishes;
closed-empty unemployment with complete line-10 scope still produces honest
attachment disposition (required with zero line 7, or inapplicable only if the
settled paper rule says so — prefer **required when any Schedule 1 line-10
slot is in the completeness universe for the bounded full-return claim**).
Negatives: missing attachment when line 7 would publish; blocked disposition
when box-1 family open. Map: line-7 finding → attachment rule → presentation
disposition.

**P4 line-10 completeness (compare on paper).**

| Alternative | Shape | Pros | Cons |
| --- | --- | --- | --- |
| **A (preferred)** | Line 10 = closed unemployment subtotal (line 7) **plus** explicit absence authority for every unsupported Schedule 1 Part I income class (lines 1, 2a, 3, 4, 5, 6, 8a–8z/9 aggregate, and any paper-required repayment flag absent) | Names the complete additional-income universe; closed-empty unemployment works; unemployment closure alone cannot claim all Schedule 1 income is known; mirrors successful line-2a-scope pattern | Larger declaration surface; must name categories carefully without manufacturing zero amounts for absent authority |
| **B** | Single opaque `schedule1-part1-scope-complete` boolean | Smaller payload | Poor diagnostics; blurs which class failed; weaker future reuse |
| **C** | Multi-family composition implementing zero families for every Schedule 1 line | "Real" composition | Implements unsupported sources as fake zeros; violates non-goals and "no manufactured zero for absent authority" |

**Selected planning recommendation: Alternative A.** Track 0 paper instances
must list each named absence slot against Schedule 1 Part I labels. If paper
shows a tighter grouping that preserves per-class honest block reasons, prefer
the tighter grouping; do not collapse to Alternative B solely for payload size.

**P5 line 8 / line 9.** Positives: unemployment-only return (line 7 = line 10 =
line 8; line 9 increases exactly once by that amount); unemployment + W-2;
unemployment + interest/dividends; unemployment + supported capital gain/loss.
Negatives: double-count if both raw subtotal and line 8 added; missing line 8
with "assumed zero." Map: complete line 10 → line 8 field → line-9 v5 sum →
taxable income / tax.

**P6 residual.** Positives: residual companions absent/null for unsupported
boxes on each statement, or tax-year absence declarations where paper prefers
that grain. Negatives: box-2 (state refund) present; other income box present;
treating box-1 closure as residual proof. Prefer **per-statement residual
companion authority** for boxes that can appear on the same Form 1099-G as box
1 (at minimum: box 2, and a residual bucket or explicit slots for 5–7 and 9 as
paper requires), rather than inventing full source families.

**P7 repayment.** Positive: ordinary correction superseding box 1. Negative:
repayment flag/amount present; negative box-1 attempt rejected at admission.
Map: repayment scope authority → hard block of complete-return claim.

**P8 pins.** Positive presentation golden walks payer statement → closure →
composition → Schedule 1 line 7/10 → Form 1040 line 8 → line 9. Negatives:
presentation value treated as authority; missing pins; raw reach-around.

### Track 0 proposed settlement (planning recommendation)

These are the Foreman's paper-grounded recommendations for owner review. They
become binding for implementation only after owner approval of this plan (and
any owner amendments). No rival prototype is planned unless the owner rejects
Alternative A without accepting an equally complete paper shape.

1. **Statement authority.** Reuse the ADR-0015 pattern with
   `payer/agency + logical statement + tax-year=2025` identity keys (entity
   kinds for Form 1099-G payer and statement). Nonnegative box-1 source amount;
   family, horizon, closure mapping, subtotal, citation. Two statements from
   the same payer remain distinct originals; a corrected copy of the same
   logical statement supersedes the prior answer.

2. **Box-4 companion.** Every box-1 member requires an explicit box-4
   companion: null/absent-or-zero admissible shapes only as settled by content
   (explicit null **or** numeric zero). Missing companion is not absence.
   Nonzero blocks the complete-return claim; no line-25b computation.

3. **Schedule 1 line 7.** Add Schedule 1 as an attachment citizen for this
   bounded route. Publish line 7 from the closed box-1 family subtotal.
   Dispositions: required when the bounded complete-return path needs Schedule
   1 additional income; blocked when dependencies are open/invalid;
   inapplicable only when the settled completeness path honestly says Schedule
   1 is not part of the claim (prefer not using inapplicable merely because
   unemployment is zero if other line-10 absence authority is in play). Do not
   claim general Schedule 1 completeness from the unemployment family alone.

4. **Schedule 1 line 10.** Alternative A: unemployment slot + explicit absence
   authority for every unsupported Schedule 1 Part I income class. Closed-empty
   unemployment is allowed when absences are current. Missing absence authority
   blocks. Absence is not a published zero amount for an unimplemented line.

5. **Line 8 / line 9.** Publish Form 1040 line 8 from complete Schedule 1 line
   10. Line-9 **v5** adds published line 8 exactly once to the existing four
   components. No temporary-zero and no silent omission. Downstream taxable
   income and tax recompute without changing unrelated consumer semantics.

6. **Residual boundary.** Box-1 family closure never proves other 1099-G boxes
   absent. Require explicit residual/companion or tax-year absence authority
   for other payment classes that can co-occur on Form 1099-G; smallest shape
   that honestly blocks returns containing unsupported classes.

7. **Repayment vs correction.** Correction = ordinary supersession at the same
   logical-statement identity. Repayment = unsupported; block via explicit
   scope authority (and/or Schedule 1 line-7 repayment controls present).
   Box-1 amounts remain nonnegative; negative box-1 is admission-invalid.

8. **Lifecycle / explanation / pins.** Multi-statement aggregation without
   identity collapse; late discovery advances horizon and displaces stale
   closure; successor closure restores; correction displaces Schedule 1 line
   7/10, Form 1040 line 8/9, and downstream results. Explanation walks the
   chain without treating presentation values as authority.

### ADR disposition

Prefer existing identity, closure, composition, attachment, package,
explanation, and presentation contracts:

| ADR | Reuse |
| --- | --- |
| ADR-0015 | Payer/statement/year identity |
| ADR-0016 | Per-family claim and composition |
| ADR-0017 | Family horizon / closure freshness |
| ADR-0020 / ADR-0029 | Explanation walking and citation pins |
| ADR-0027 / ADR-0033 | Package/adoption exclusivity and verified resolution |
| ADR-0036 | Schedule attachment ontology (Schedule 1 as content) |
| ADR-0046 | Presentation surface |

**New ADR recommendation:** draft a new Tier-2 product ADR **only if** Schedule
1 line-10 completeness or the line-8/line-9 succession establishes a reusable
contract not already settled by the ADRs above (most likely: a reusable
"additional-income completeness via named absence slots + one supported family"
pattern, or a cross-form bridge pattern for Schedule 1 line 10 → Form 1040 line
8). Do **not** create an ADR merely to record process or milestone organization.
ADR number/filename are **unreserved** until final rebase (parallel milestones
may publish successors). If accepted ADRs plus this plan fully express the
shape, record the decision in this plan and the retrospective instead. No
accepted ADR is edited.

## Contracts

### UG-C1 — Independent Form 1099-G box-1 family

- Identity: payer/agency + logical statement + tax-year 2025; no file/upload/
  scan/document/evidence key on identity (ADR-0015).
- Amount: nonnegative source amount with named quantity and Form 1099-G box-1
  citation.
- Family closure covers box 1 only; closed-empty is explicit zero; absent
  closure is not zero.
- Subtotal sums current members across payers/agencies without identity
  collapse.
- Correction supersedes the same logical statement; two originals from one
  payer remain distinct.

### UG-C2 — Box-4 companion authority

- Per box-1 statement: explicit box-4 companion required.
- Admissible: explicit null/absent encoding **or** numeric zero (both must be
  tested).
- Nonzero: hard block of the bounded complete-return claim.
- Never reduces box-1 income; never implements line 25b.

### UG-C3 — Schedule 1 line 7 attachment citizen

- Schedule 1 becomes an attachment citizen for this route (ADR-0036 content).
- Line 7 publishes the closed box-1 subtotal when dependencies are current.
- Attachment dispositions: required / blocked / inapplicable as settled in
  Track 0 paper for this bounded path.
- Explanation and presentation show published or blocked line 7 with authority
  reasons.
- Unemployment family closure alone never asserts general Schedule 1
  completeness.

### UG-C4 — Schedule 1 line-10 completeness (Alternative A)

```text
line-10 = closed unemployment (line 7)
          when every unsupported Schedule 1 Part I income class
          is explicitly declared absent (and repayment controls are absent)
```

- Missing, stale, contradictory, or "present" excluded slots block.
- Closed-empty unemployment + complete absences → line 10 = 0 (explicit).
- Do not manufacture zero amounts for unsupported classes without absence
  authority.
- Name categories at least as finely as Schedule 1 Part I lines 1, 2a, 3, 4,
  5, 6, other-income (8/9), plus repayment-not-present for the bounded claim.

### UG-C5 — Form 1040 line 8 and line-9 succession

- Line 8 form-field + rule + citation publish from complete Schedule 1 line 10.
- Line-9 **v5** = wages + taxable interest + ordinary dividends + line-7a total
  + **line 8**, each exactly once.
- Historical line-9 v1–v4 remain immutable; packages select versions
  exclusively.
- Preserve W-2, interest, dividends, capital gains/losses, and every existing
  line-9 component semantics.
- Carry through taxable income and tax without changing unrelated consumer
  semantics (including line 2a remaining non-input to line 9).

### UG-C6 — Form 1099-G residual boundary

- Box-1 closure ≠ other-box absence.
- Explicit residual/companion or tax-year absence authority for unsupported
  Form 1099-G payment classes that can appear with box 1.
- Smallest honest block shape; no silent absorption into the unemployment
  family.

### UG-C7 — Repayment and correction boundary

- Correction: free supersession at the same logical-statement identity.
- Repayment: unsupported; explicit scope block; not a negative box-1 amount.
- Admission rejects negative box-1 source amounts.

### UG-C8 — Lifecycle, explanation, package, presentation

- Late member advances family horizon; stale closure displaces consumers;
  successor closure restores publication.
- Correction displaces Schedule 1 line 7/10, Form 1040 line 8/9, and
  downstream findings.
- Exact pins: family, mapping, horizon, closure, companions, completeness
  authority, citations (ADR-0029).
- One verified package + published-registry + release + adoption successor;
  exclusive current graph; historical routes remain resolvable.
- One canonical positive presentation golden via `live_coordinate_run`; compact
  negative mutations for block/redact behavior.

## Line-8 / line-9 succession and integration order

### Intended succession (this milestone)

```text
[existing v4]
line9 = wages + interest + ordinary dividends + line7a

[successor v5]
line9 = wages + interest + ordinary dividends + line7a + line8
where line8 = complete Schedule1.line10
      Schedule1.line10 = f(unemployment_subtotal, schedule1_part1_absences…)
      unemployment_subtotal = closed Form 1099-G box-1 family
```

### Integration recommendation relative to Form 8949

| Topic | Observation | Recommendation |
| --- | --- | --- |
| Semantic overlap | Form 8949 changes Schedule D / Form 8949 path that feeds **line 7a**, which is an input to line 9; this milestone adds **line 8** and a **line-9 v5** rule. Both expand `package.core-calculations`. | Treat as **known semantic overlap**, not a mere version-number collision. |
| Current 8949 line-9 | Still selects line-9 **v4** on its branch tip. | This milestone owns the first line-9 **v5** that introduces line 8, unless Form 8949 lands a different line-9 successor first — re-inventory before packaging. |
| Package numbers | 8949 branch already carries **v18** / registry **v13** / `artifact-package.v15`. Box-8 branch also records v18/v13 intent. Planning base is **v17/v12**. | **Do not hardcode** successor numbers in implementation until final rebase. Prefer **merge-order discipline**: whoever merges second rebuilds as additive union of the then-ratified tip. |
| Recommended order | Form 8949 is active Track 1 on a dedicated worktree. | **Prefer letting Form 8949 (or any earlier-merging package successor) land first** if it is near merge; this milestone rebases, captures the ephemeral three-way semantic ledger, preserves its delta, rebuilds package/registry/release/adoption successors as a validated **union**, and verifies line-9 v5 still adds line 8 exactly once on top of the post-8949 line-7a path. If Form 8949 is delayed, this milestone may land on v17 first; Form 8949 then must re-union without dropping unemployment members. |
| Hard stop | Unexplained overlap, selected-version regression, or dropped members | Stop and return to owner (lesson of the Schedule B v15 collision). |

### Package-rebase and semantic-ledger checkpoints

Before implementation packaging, and again before PR curation:

1. Fetch/prune origin; identify latest ratified line with the repository
   resolver (not a guessed version).
2. Inventory every published tax schema, artifact-package schema, package,
   published registry, release, adoption, line-8, line-9, Schedule 1, and
   relevant presentation artifact version on that line and this branch.
3. If rebasing onto newly merged work (especially Form 8949 or box-8):
   - capture the **ignored ephemeral three-way semantic ledger** (temporary;
     never commit the ledger artifact);
   - preserve the pre-rebase milestone delta;
   - rebuild from the new predecessor;
   - verify upstream additions, selections, and retirements;
   - stop on unexplained overlap or selected-version regression.
4. Choose unused successor filenames/discriminators only after rebase;
   preserve every ratified file and manifest row byte-for-byte.
5. Require a focused test proving the final core package is the **union** of
   the current ratified graph and this milestone's intended changes.
6. Verify package exclusivity, registry checksums, release hashes, adoption
   pins, and historical-route compatibility before handoff.

## Tracks and independent review structure

Economy preference: **one paper-first Track 0**, **one integrated production
Builder**, **one independent Reviewer**. No rival prototype unless paper leaves
two viable Schedule 1 completeness shapes. No separate schema-gate, attachment,
or packaging tracks unless a real contract dependency requires independent
settlement (if Schedule 1 attachment cannot be expressed on existing
attachment-rule schemas without a schema succession, split a minimal schema
gate only after that dependency is proven).

### Track 0 — Paper boundary and contract checkpoint (Foreman)

Record Gate-1 scores (this plan), paper instances, negatives, lifecycle
traces, maps, exact citations, Alternative A slot list, and ADR disposition.
Owner approval of this plan is the Track 0 authorization to treat the proposed
settlement as binding for chartering. No rival prototype authorized by default.

### Track 1 — Integrated production build (Builder)

After owner approval and any owner-amended Track 0 settlement, one integrated
Builder implements:

- Form 1099-G box-1 family, companions, residual/absence boundary, subtotal;
- Schedule 1 line 7 / line 10 completeness / attachment citizen;
- Form 1040 line 8; line-9 v5 succession; downstream recompute;
- package / registry / release / adoption successors from the then-ratified tip;
- explanation, presentation golden, fixtures, and tests.

If existing evaluator, marshal, package, or presentation substrate cannot
express the settled paper shape, the Builder **stops** and returns the issue to
the owner rather than expanding scope or inventing the Schedule 1 universe.

### Review gate — Independent Reviewer

One author-independent Reviewer measures: contract fidelity; Schedule 1
completeness honesty; box-4/residual/repayment boundaries; exact-once line-8
in line 9; double-count risk; package union integrity; pin completeness;
lifecycle displacement; regression preservation (line 2a, Schedule B, Schedule
D, carryovers, Form 8949 as present on the final base). Report falsifiable
`READY` or numbered findings.

### Repair and closeout

At most one bounded findings-only repair cycle for the same Builder. A second
substantive defect, new product decision, or scope expansion returns to the
owner. Working charters and interim records are removed at final curation; this
plan and the retrospective preserve durable decisions.

## Evidence matrix (fixture and lifecycle matrix)

All cases use synthetic identities and values. Existing regressions remain
unmodified on the final base.

| ID | Case or mutation | Expected result |
| --- | --- | --- |
| P1 | One Form 1099-G box-1 statement | Closed family subtotal; Schedule 1 line 7; line 10; Form 1040 line 8 publish the amount |
| P2 | Multiple agencies/statements | Distinct identities; subtotal aggregates exactly once |
| P3 | Two logical statements from the same payer | Both count; no identity collapse |
| P4 | Correction at the same logical-statement identity | Prior finding superseded; downstream displaced and recomputed |
| P5 | Closed-empty unemployment family + complete absences | Explicit zeros on line 7/10/8; not "missing" |
| P6 | Missing / open family closure | Consumers block; absence ≠ zero |
| P7 | Late member after closure + restored successor closure | Stale closure displaces; successor restores |
| P8 | Box 4 explicit null | Admissible |
| P9 | Box 4 explicit zero | Admissible |
| N1 | Box 4 missing companion | Hard block; not assumed absent |
| N2 | Box 4 nonzero | Hard block; no line-25b computation |
| N3 | Another Form 1099-G income box present / residual incomplete | Honest block |
| N4 | Unemployment-repayment case | Honest block via scope authority |
| N5 | Another Schedule 1 income source present | Line-10 completeness fails |
| N6 | Missing Schedule 1 scope/absence authority | Line 10 / line 8 block; no manufactured zero |
| P10 | Unemployment-only return | line 7 = line 10 = Form 1040 line 8; line 9 increases exactly once by that amount |
| P11 | Unemployment + W-2 | Line 9 = wages + unemployment (+ zeros for other supported components as closed) |
| P12 | Unemployment + taxable interest and dividends | Line 9 includes interest and ordinary dividends plus line 8 once |
| P13 | Unemployment + supported capital gain or loss | Line 7a path unchanged in semantics; line 8 added once |
| P14 | Downstream taxable-income and tax recomputation | Lines 15/16 (and related) recompute from new total income |
| P15 | Correction/displacement reaches all downstream consumers | Stale findings leave current state until successor graph is current |
| P16 | Canonical positive presentation golden | Walks statement → closure → composition → Schedule 1 → line 8 → line 9 |
| N7 | Compact negative presentation mutations | Existing fail-loud / block / redact behavior |
| R1 | Line 2a regressions | Unchanged |
| R2 | Schedule B regressions | Unchanged |
| R3 | Schedule D / carryover regressions | Unchanged |
| R4 | Form 8949 regressions as present on final base | Unchanged (if Form 8949 content is on the final base after merge order) |

## Fixtures, verification, economy, and data safety

- Prefer compact shared fixture builders and **one** canonical positive
  presentation golden rather than duplicating full act logs and presentation
  outputs.
- Use synthetic demo identities only; honor `AGENTS.md` Data Safety Rules.
- Focused package-union test required (see checkpoints).
- No real-data operation.

## Durable versus temporary artifact boundaries

| Durable (commit and keep) | Temporary (do not commit, or remove at curation) |
| --- | --- |
| This milestone plan | Builder/reviewer working charters after closeout |
| Accepted ADRs (if any new) | Ephemeral three-way semantic ledger |
| Production content, packages, registries, releases, adoptions | Local rebase scratch, unrebased package number guesses |
| Synthetic fixtures and tests | Duplicate full presentation goldens for every negative |
| Coverage-frontier and roadmap updates | Interim process notes superseded by retrospective |
| Phase-state updates | Spent branch debris |

## Coverage-frontier and roadmap updates

This plan creates a **distinct unemployment compensation row** on the Engine
Breadth coverage frontier and roadmap item. Other Form 1099-G boxes and other
Schedule 1 income sources remain **separately selectable** rows / named blocks
— not absorbed into this claim.

## Exit criteria

- Owner-approved plan (this document, as amended).
- Track 0 settlement binding for implementation (this document after approval,
  or an additive Track 0 amendment commit).
- Track 1 production path synthetic-complete for the supported class.
- Independent Reviewer `READY` (with at most one findings-only repair).
- Package union integrity proven; historical packages resolvable.
- Frontier row marked synthetic complete only after closeout; other 1099-G and
  Schedule 1 classes remain separately named.

## Durable commit structure (planned)

1. `plan: select Form 1099-G box 1 to Schedule 1 line 7 / Form 1040 line 8` —
   this plan, phase-state, frontier, and roadmap selection.
2. Later (after owner approval): Track 0 amendment only if needed; then
   implementation; review; closeout commits per project protocol.

## Unresolved Track 0 questions (for owner review)

These do **not** block plan approval if the owner accepts the preferred
defaults; they are the residual paper choices to ratify or amend:

1. **Exact Schedule 1 Part I absence slot list** — confirm Alternative A slot
   granularity (line-by-line vs grouped "other income 8a–8z") and whether the
   repaid-2025-overpayment control is a separate scope fact or part of line-7
   authority.
2. **Schedule 1 attachment required vs inapplicable** when unemployment is
   closed-empty but absences are complete (recommend: still required for the
   bounded complete additional-income claim that publishes line 8 = 0, so line
   8 is never a silent omission on line 9).
3. **Residual grain** — per-statement companions for boxes 2/5–7/9 vs a single
   residual payload vs tax-year declarations for classes that cannot share a
   statement with box 1.
4. **New ADR** — approve "no new ADR" if Alternative A + line-9 v5 are judged
   content applications of existing ADRs; otherwise authorize one completeness
   / bridge ADR after Track 0 final wording.
5. **Integration order** — confirm preference: wait for Form 8949 merge when
   practical; otherwise allow this milestone to land first with mandatory
   union discipline for the later merge.

---

**Stop condition:** no Builder charter and no agent spawn from this plan until
the owner explicitly approves the plan (and any amendments) and later provides
dispatch authorization if a Builder is to be launched by the foreman.
