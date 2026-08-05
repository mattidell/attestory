<!-- foreman-context-v1
{
  "version": 1,
  "topic": "form1099div-box7-direct-ftc",
  "milestone_state": "closed",
  "status": "CLOSED. The bounded 2025 Form 1099-DIV box-7 direct foreign tax credit without Form 1116 is synthetic complete and independently reviewed READY through Schedule 3 line 1/8 and Form 1040 line 20.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md",
  "scope": [
    "promote Form 1099-DIV box 7 into an independent closed source family of U.S.-dollar foreign tax paid",
    "replace the active 1099-DIV residual (boxes 3, 5, 7) additively with a residual successor containing boxes 3 and 5 only while preserving all historical residual shapes and package bytes",
    "establish auditable associated-income, creditability, direct-election eligibility, threshold, and regular-tax-cap authority without Form 1116 machinery",
    "publish Schedule 3 line 1 (direct FTC), bounded Schedule 3 line 8, Form 1040 line 20, and tax-after-credit succession from existing line-16 regular tax",
    "preserve Form 1099-DIV box 1a/1b and Form 1040 line 3a/3b income paths; box 7 never reduces dividend income",
    "carry the graph through correction lifecycle, package/release/adoption resolution, explanation, and the existing presentation surface"
  ],
  "non_goals": [
    "no Form 1116 calculation, attachment, separate-limitation categories, or general foreign-tax-credit framework",
    "no foreign tax above the $300/$600 direct-election threshold; no carryback or carryforward",
    "no Schedule A foreign-tax deduction election",
    "no foreign taxes from Form 1099-INT, Schedule K-1/K-3, or any source outside the selected Form 1099-DIV class",
    "no currency conversion, paid-versus-accrued elections, AMT FTC, CFC/section 962/deemed-paid, high-taxed reclassification, or Form 2555",
    "no general Schedule 3 credit support, Schedule A, Form 6251, Form 8949/Schedule D contract changes, payments/refund/balance-due, filing, transmission, real-data operation, or UI redesign"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md#Official 2025 paper boundary",
      "docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md#Contracts",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0035-dividend-composition-and-lines-3a-3b.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/content/tax/2025/f1099div.bundle.json",
      "packages/content/tax/2025/f1099div-box12.bundle.json",
      "packages/content/tax/2025/dividend-universe.v3.json",
      "packages/content/tax/2025/rule.form1040-line16.v5.json",
      "packages/content/tax/2025/package.core-calculations.v17.json",
      "packages/content/tax/2025/published-packages.v12.json",
      "packages/sample_data/form1099div_box12_line2a/adoptions/adopt-core-v17-current.json",
      "packages/sample_data/form1099div_box12_line2a/publication_surface/releases/demo.release.2025.v10.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md#Contracts",
      "docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md#Evidence matrix",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0035-dividend-composition-and-lines-3a-3b.md",
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
      "docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md",
      "docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md",
      "docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md"
    ]
  }
}
-->
# Milestone: Form 1099-DIV Box 7 Direct Foreign Tax Credit (No Form 1116)

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner on 2026-08-05. Independent of the
active Form 8949 worktree (`milestone/schedule-d-form8949-covered-wash-sale`);
that worktree must not be touched, switched, cleaned, staged, or otherwise
altered by this milestone.

## Objective

Make one bounded 2025 individual return class computable end to end: one or more
Forms 1099-DIV report foreign tax paid in box 7 (U.S. dollars); the taxpayer
qualifies for and elects the procedure to claim the foreign tax credit **without
filing Form 1116**; and the credit is carried through Schedule 3 (Form 1040)
Part I line 1, Schedule 3 line 8, Form 1040 line 20, and the tax-after-credit
graph built additively from the existing regular-tax publication.

Box 7 is a **credit source**, not a reduction of dividend income. Associated
ordinary dividends (box 1a) and, if Track 0 retains them, qualified dividends
(box 1b) remain on the existing Form 1040 line 3b/3a paths.

This milestone does **not** implement general foreign-tax-credit calculation,
Form 1116 limitation arithmetic, carryovers, or a Schedule A deduction election.

## Current state (inventory on `origin/main` @ `b0480bc`)

### Residual 1099-DIV succession (post box-12)

| Residual version | Composable elsewhere | Recorded non-composable boxes | Package note |
| --- | --- | --- | --- |
| `recorded-boxes` v1 | — | 2a, 3, 5, 7, 12 | Historical; immutable |
| residual in box-2a successor universe v2 | 1a, 1b, 2a | 3, 5, 7, 12 | Historical; immutable |
| residual v3 (`f1099div-box12.bundle` / `dividend-universe.v3`) | 1a, 1b, 2a, 12 | **3, 5, 7** | **Current active residual on ratified core package v17** |

This milestone **must extend residual v3**, not rebuild from an earlier residual.
The additive successor residual records **boxes 3 and 5 only**. Boxes 3 and 5
remain recorded-only. Mixed historical residual + independent box-7 family
graphs are rejected.

### Dividend families (current)

- Composable: box 1a → line 3b; box 1b → line 3a; box 2a → line 7a path; box 12 → line 2a path.
- Recorded non-composable (active residual v3): boxes 3, 5, 7.
- Box 7 has **no** independent family, subtotal, mapping, or credit consumer.

### Regular tax and Form 1040 lines 18–24

| Item | Current engine state |
| --- | --- |
| Filing status | `tax.us.2025.filing-status` / binding symbol `filing_status` — used by standard deduction and line 16 |
| Form 1040 line 16 | `rule.form1040-line16` **v5** publishes `tax.us.2025.tax.total-tax`; form field binds that symbol to line 16 |
| Regular-tax consumers of capital gain | Preferential base / Schedule D proceed subtotals gate line 16; **no Form 8949-specific dependency** |
| Schedule 2, Schedule 3 | **Absent** — no citizens, fields, or rules |
| Form 1040 lines 17–24 | **Absent** — no line 19 CTC, line 20 nonrefundable credits, line 21 total credits, line 22 tax-after-credits, line 24 total tax succession |
| Credits | **None**. Line 2a scope already declares `no-credit-using-tax-exempt` as an excluded downstream dependency of tax-exempt interest, not an FTC implementation |

**Naming hazard:** `tax.us.2025.tax.total-tax` is presently **line-16 tax**, not Form 1040 line 24 total tax. This milestone must not silently repurpose that symbol as tax-after-credits. Prefer: keep line-16 publication on its current symbol (or an additive alias `regular-tax` / `line-16-tax` if Track 0 requires a clearer consumer pin), and introduce distinct symbols for Schedule 3 / line 20 / tax-after-credit.

### Package / release graph (ratified)

| Artifact | Current tip on `origin/main` |
| --- | --- |
| `package.core-calculations` | **v17** (185 members; `artifact-package.v14`) |
| `published-packages` | **v12** |
| Box-12 demo release | `demo.release.2025@v10` |
| Box-12 adoption | `adopt-core-v17-current` |
| Dividend universe | **v3** (composable 1a, 1b, 2a, 12; residual 3, 5, 7) |

Successor package/registry/release/adoption versions are **not reserved** until the final rebase collision inventory. Expect at least v18 / v13 / v11 / v18-class names if no concurrent merge lands first.

### Parallel Form 8949 discipline

Regular tax may change when Form 8949 changes capital gain/loss and line 16.
This milestone depends only on the **stable regular-tax / line-16 symbol
contract**, not on Form 8949 implementation details. Before any rebase onto
newly merged work: capture an ignored ephemeral semantic ledger; preserve this
milestone’s original delta; rebuild from the new ratified predecessor; verify
upstream additions, selections, retirements, and regular-tax consumers; **stop**
on semantic overlap or selected-version regression. Do not finalize package or
downstream credit versions against a stale base.

## Official 2025 paper boundary

Grounding sources (current official text retrieved 2026-08-05):

1. **[Instructions for Form 1116 (2025)](https://www.irs.gov/instructions/i1116)** —
   “Election To Claim the Foreign Tax Credit Without Filing Form 1116”:
   - All foreign-source gross income is passive-category income (includes most
     interest and dividends; for the election, also high-taxed income and
     certain export financing interest).
   - All the income and any foreign taxes paid on it were reported on a
     **qualified payee statement** (Form 1099-DIV, 1099-INT, Schedule K-1
     (1041), Schedule K-3 (1065/1120-S), or similar substitute).
   - Total **creditable** foreign taxes are not more than **$300** (**$600** if
     married filing a joint return).
   - Election not available to estates or trusts.
   - If electing: **no carryover to or from** the election year of foreign taxes
     paid or accrued in that year; general creditability rules still apply;
     still reduce taxes by amounts that would have been on Form 1116 line 12.
   - To elect: enter on the FTC line (Schedule 3 Part I line 1) the **smaller
     of (a) total foreign tax or (b) regular tax**. Regular tax for individuals
     (Form 1116 line 20 instructions): Form 1040 line 16 + Schedule 2 Part I
     line 1z, less any Form 4972 tax included on line 16. Regular tax liability
     is §26(b)(1); does not include NIIT.
   - The election removes the **Form 1116 limitation calculation**, not
     underlying creditability requirements.

2. **[Foreign Tax Credit — How to figure the credit](https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit-how-to-figure-the-credit)** —
   restates the four election conditions (passive, ≤$300/$600, qualified payee
   statements, elect) and the caution that the election does **not** exempt the
   taxpayer from other Pub. 514 requirements (e.g. nonrefundable income tax).

3. **[Publication 514 (2025)](https://www.irs.gov/publications/p514)** —
   credit vs deduction choice; qualified foreign taxes; **dividend holding-period
   denial**: taxes on dividends of stock held less than **16 days** during the
   31-day period beginning 15 days before the ex-dividend date (preferred stock
   special rule: less than 46 days in a 91-day period for dividends covering
   more than 366 days); short-sale / obligation-to-pay related denial;
   refund/subsidy/noncreditable categories.

4. **[Instructions for Form 1099-DIV](https://www.irs.gov/instructions/i1099div)** —
   Box 7: foreign tax paid on dividends/distributions, U.S. dollars; RIC
   pass-through only of elected amount. Box 8: foreign country or U.S.
   possession for the tax in box 7; **RICs do not complete box 8**.

5. **[2025 Form 1040 / Schedule 3 instructions](https://www.irs.gov/instructions/i1040gi)** —
   Schedule 3 Part I line 1 Foreign Tax Credit **Exception** (no Form 1116 if
   all five apply):
   1. All foreign-source gross income was from interest and dividends, and all
      of that income and the foreign tax paid on it were reported on Form
      1099-INT, Form 1099-DIV, or Schedule K-3 (or substitute).
   2. Total foreign taxes not more than $300 ($600 MFJ).
   3. Held the stock or bonds at least **16 days** and were not obligated to pay
      those amounts to someone else.
   4. Not filing Form 4563 or excluding Puerto Rico-source income.
   5. Taxes legally owed / not refund-or-treaty-rate eligible, and paid to
      countries recognized by the United States that do not support terrorism.
   - If yes: enter on line 1 the **smaller of (a) total foreign taxes or (b)
     Form 1040 line 16 + Schedule 2 line 1a**.
   - Form 1040: nonrefundable credits other than CTC/ODC use Schedule 3 Part I;
     line 20 is the Schedule 3 line 8 amount; line 21 adds line 19 and line 20;
     line 22 subtracts line 21 from line 18 with a floor at zero (form arithmetic).

6. **[Schedule 3 (Form 1040)](https://www.irs.gov/pub/irs-pdf/f1040s3.pdf)** —
   Part I line 1 Foreign tax credit; lines 2–6 other nonrefundable credits;
   line 8 total of Part I → Form 1040 line 20.

### Paper-derived arithmetic for the bounded class

```text
threshold(filing_status) =
  600 if married filing jointly else 300

eligible_threshold =
  closed box-7 subtotal ≤ threshold(filing_status)

regular_tax (bounded class) =
  Form 1040 line 16
  # Schedule 2 line 1a / 1z and Form 4972 absent by explicit scope authority

schedule_3_line_1 =
  min(closed box-7 subtotal, regular_tax)
  only when election + eligibility + creditability + associated-income
  + threshold + scope authorities are current

schedule_3_line_8 =
  schedule_3_line_1
  only when every other Schedule 3 Part I credit is explicitly absent

form_1040_line_20 = schedule_3_line_8

# Bounded tax-after-credit (when line 17/19/23 absent by authority):
line_18 = line_16                    # no Schedule 2 additional tax in class
line_21 = line_20                    # no CTC/ODC in class
line_22 = max(line_18 - line_21, 0)
line_24 = line_22                    # no other taxes in class
```

Threshold eligibility is distinct from the final allowable-credit cap
(`min(tax, regular_tax)`). Exceeding the threshold **blocks the direct
election**, it does not silently clip to $300/$600.

## Supported class

- Tax year **2025**; individual Form 1040 filing status already supported by the
  engine (single, MFJ, MFS, HOH, QSS as presently modeled).
- One or more Form **1099-DIV box-7** amounts in **U.S. dollars**, nonnegative.
- Associated dividend income on the **same logical statements** through
  supported box **1a** (required positive association) and, if Track 0 retains
  it, box **1b** coexistence on the existing income path.
- All foreign-source gross income is **passive** and reported only on
  **qualified payee statements** in this class (Form 1099-DIV only for the
  selected slice).
- All foreign taxes for the claim are reported on those Form 1099-DIV
  statements; total **creditable** foreign tax ≤ **$300**, or **$600** if MFJ.
- Explicit taxpayer **election** to use the direct-credit procedure for the
  tax year.
- **No** foreign-tax carryback or carryforward for the election year; **no**
  Schedule A deduction election; **no** Form 1116 required or produced.
- **No** other Schedule 3 Part I credit; **no** CTC/ODC on line 19; **no**
  Schedule 2 Part I additional tax affecting regular tax; otherwise supported
  income and tax computation only.

### Recommended first-slice narrowing (owner decision)

**Qualified dividends (box 1b):** prefer **retain coexistence** for the income
path (line 3a) and require **explicit creditability component authorities**
including the Pub. 514 / Schedule 3 **16-day holding-period** and
no-obligation-to-pay declarations — **not** securities-history machinery. If
owner rejects declaration-based holding-period authority, narrow the selected
class to statements with box 1b absent or zero and leave qualified-dividend
foreign taxes for a successor. Track 0 records the owner disposition before
implementation.

**Multi-country supplemental allocation of one box-7 amount:** exclude unless
paper shows a bounded model that does not invent countries or collapse
allocations. RIC missing box 8 is a first-class companion state, not silence.

## Non-goals

- Form 1116 calculation, attachment, Part I–IV limitation, or multi-category
  Forms 1116.
- Foreign tax above the direct-election threshold (including “clip to threshold”).
- Foreign-tax carrybacks or carryforwards; Schedule A deduction of foreign tax.
- Foreign taxes from Form 1099-INT, Schedule K-1, Schedule K-3, or any source
  outside the selected Form 1099-DIV class.
- General foreign-source income allocation; separate limitation categories
  (general, passive multi-form, foreign branch, §901(j), treaty, lump-sum,
  resourced-by-treaty); high-taxed-income reclassification.
- Foreign earned income / Form 2555; CFC; §962; deemed-paid taxes; AMT FTC.
- Currency conversion; paid-versus-accrued elections; refunded, rebated,
  subsidized, or otherwise noncreditable taxes; taxes on excluded income.
- Unsupported holding-period **computation** from trade history.
- General Schedule 3, Schedule A, Form 6251 support.
- Payments, refund, balance due, filing, transmission.
- Schedule D or Form 8949 contract changes; real-data operation; UI redesign.
- Mutation of any published schema, historical content citizen, package,
  release, adoption, fixture, or accepted ADR byte.

## Track 0 — Gate-1 decision inventory

Track 0 is paper-first. Scores use the four Gate-1 axes (future blast radius,
migration cost, residual uncertainty after paper examples, cheap-test gap),
each 0–2. Gate 2 requires two positives, two meaningful negatives, one
lifecycle trace, and a producer → authority → consumer → failure map per
primary proposition. If paper distinguishes the shape, stop at paper; no rival
prototype is authorized by this plan.

| Proposition | Blast | Migration | Paper uncertainty | Cheap-test gap | Total | Planned disposition |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P1. Box-7 family identity, closure, multi-statement aggregation, correction | 2 | 1 | 1 | 1 | 5 | Paper; reuse ADR-0015/0016/0017 pattern from box-12 |
| P2. Residual succession (v3 → boxes 3+5 only) and package exclusivity | 2 | 2 | 1 | 1 | 6 | Paper; mixed residual/family rejection; no double admission of box 7 |
| P3. Box-8 country companion (required vs RIC-null; multi-country exclusion) | 1 | 1 | 2 | 1 | 5 | Paper; no invented country; missing companion fails closed |
| P4. Associated foreign-income authority (not inferred from tax amount) | 2 | 2 | 2 | 1 | 7 | Paper compares per-statement 1a/1b association vs distinct foreign-income fact vs tax-year completeness; select smallest honest shape |
| P5. Creditability component authorities (not a single unexplained `qualified`) | 2 | 2 | 2 | 1 | 7 | Paper names minimum components; synthesized conclusion only if derived from named parts |
| P6. Direct-election eligibility (passive, payee statements, threshold, election, no carry, no deduction, no Form 1116 condition) | 2 | 2 | 1 | 1 | 6 | Paper; mix of contributions, closed-family derivations, and filing-status computation |
| P7. Threshold vs regular-tax cap arithmetic and zero/under-tax cases | 2 | 1 | 1 | 0 | 4 | Paper instances; keep threshold gate ≠ min(tax, regular_tax) |
| P8. Schedule 3 completeness (line 1 + absent other Part I credits → line 8) | 2 | 2 | 1 | 1 | 6 | Paper; closed-empty box-7 and no-foreign-tax representable; no silent zero other credits |
| P9. Form 1040 credit/tax succession (line 20; line 19 interaction; total credits; floor at zero; line-16 symbol hygiene) | 2 | 2 | 1 | 1 | 6 | Paper; additive symbols; count FTC once; preserve line-16 computation |
| P10. Lifecycle, exact pins, explanation (no Form 1116 claim), presentation | 1 | 1 | 1 | 0 | 3 | Implementation contract and adversarial tests |

Gate-0 discipline: **P2, P4, P5, P6, P8, P9** are primary contract propositions.
P1/P3/P7/P10 are tightly dependent secondaries or implementation-boundary
obligations. If paper cannot express an honest bounded authority without
material Form 1116 machinery, **stop and return to the owner**.

### Competing shapes (paper must compare)

**Associated foreign income (P4):**

| Shape | Idea | Risk |
| --- | --- | --- |
| A. Per-statement association with existing box 1a/1b | Box-7 member requires same-statement box-1a presence; optional 1b | Does not alone prove all foreign income is passive or only on payee statements |
| B. Distinct foreign-source passive-income fact keyed to the statement | Explicit gross foreign passive income amount | May over-claim precision the 1099 does not provide for the foreign portion of 1a |
| C. Tax-year completeness authority | Declares no foreign-source income outside qualified 1099-DIV (and no 1099-INT/K-3 foreign income in class) | Needed for election honesty; must not invent amounts |

**Recommended paper outcome to validate:** A + C (per-statement 1a association and
tax-year completeness), without inferring foreign-source income **amount** from
box 7. Shape B only if paper shows the form/instructions require a separate
amount the engine can honestly take.

**Creditability (P5):**

| Shape | Idea | Risk |
| --- | --- | --- |
| A. Component declarations | tax type income/war/excess-profits or in-lieu; legal liability; paid (cash method); no refund/rebate/subsidy; no excluded-income association; holding period met; no short-sale obligation; country recognized / not terrorism-supporting (Schedule 3 exception) | Verbose but auditable |
| B. Single `qualified=yes` | One boolean | **Rejected** unless derived and pinned to named components |
| C. Hybrid | Named components + derived eligibility conclusion fact | Acceptable if derivation is explicit and explanation walks components |

**Recommended:** C derived from A; never B alone.

### Track 0 paper evidence plan

For each primary proposition, record synthetic paper instances (no code):

- Threshold: below / at / above $300 (non-joint); at / above $600 (MFJ); MFS uses $300.
- Election: missing; declined; accepted.
- Regular tax: foreign tax <, =, > regular tax; regular tax zero.
- Completeness negatives: non-passive foreign income; foreign income not on
  payee statements; foreign tax source outside 1099-DIV; other Schedule 3
  credit present; carryover/carryback present; deduction election present;
  missing associated-income authority; unqualified/refundable tax; failed
  holding period; missing box-8 companion when required.
- Lifecycle: correction same logical identity; multiple originals same payer;
  late member after closure; successor closure restoration.
- Residual: historical residual containing box 7 + independent family mixed
  package rejection.
- Income preservation: box 1a fully included; box 7 never reduces line 3a/3b;
  box 7 appears once in credit path.
- Tie-outs: Schedule 3 line 1 and line 8; Form 1040 line 20 and tax-after-credit.

Track 0 records exact paper instances, negatives, lifecycle traces, maps,
Gate-1 disposition, citation URLs, ADR recommendation, and any owner
narrowing (especially box 1b / holding period) **before any implementation
charter**.

### Track 0 record — paper settled 2026-08-05

The paper examples distinguish the selected shapes, so no rival prototype is
created. Values below are synthetic paper values only. Owner dispatch for the
thread was granted; Track 0 remains foreman-owned paper and does not implement.

| Proposition | Positive instances | Meaningful negatives | Lifecycle trace | Producer → authority → consumer → failure |
| --- | --- | --- | --- | --- |
| P1 box-7 family | `demo.payer.alpha` statement A box-7 `100`; two payers `100`+`40` | open closure; negative box-7 rejected | correction `100`→`125` same identity; late second statement advances horizon; restoration recloses | statement fact → box-7 family horizon → subtotal → open/stale/superseded consumer |
| P2 residual succession | successor residual `{3:null,5:null}` + box-7 member `100` | historical residual still containing box 7 + box-7 family in one package; same statement via both shapes | old packages remain resolvable; selected package adopts residual successor (3+5 only) + box-7 family | residual/family fact → package exclusivity → subtotal → mixed-graph rejection |
| P3 box-8 companion | country `"CA"`; RIC `not_applicable` with explicit authority | missing companion; invented/blank country; multi-country supplemental allocation present | companion corrects with same statement identity as box-7 member | box-7 member + box-8 companion → admission/credit gate → publish or block |
| P4 associated income | same-statement box-1a `500` with box-7 `100`; tax-year completeness all foreign income on 1099-DIV only | missing 1a association; non-passive foreign income declared present; 1099-INT foreign income present; foreign income amount inferred only from tax | completeness/election authorities supersede as tax-year declarations | 1a association + completeness → credit eligibility → block without inventing foreign-income amount from box 7 |
| P5 creditability | all components true → derived eligible; holding-period yes + no short-sale obligation | refundable tax; holding-period failed; subsidy; excluded-income association; bare `qualified=yes` without components | component correction displaces derived eligibility and credit | components → derived creditability → schedule-3 line 1 → block if any component fails |
| P6 direct election | election=yes; passive-all; payee-statements-all; no carry; no deduction; threshold ok | missing election; declined; carry present; deduction election present; Form-1116-required condition present | election correction displaces credit | eligibility set → election gate → line 1 or block |
| P7 threshold & cap | box-7 `250` single (under); `300` single (at); MFJ `600` (at); regular tax `1000` | single `300.01` (or 1 cent above per rounding); MFJ `600.01`; MFS `301`; foreign tax `200` with regular tax `50`; regular tax `0` | N/A arithmetic | subtotal + filing_status threshold gate (distinct) → min(subtotal, regular_tax) → line 1; never negative tax |
| P8 Schedule 3 completeness | line 1 credit only; all other Part I credits explicitly absent → line 8 = line 1; closed-empty box-7 with election path yields zero | another Sch3 credit present; missing absence authority; silent default zero other credits | absence authorities supersede | line 1 + Part I absences → line 8 → incomplete block |
| P9 Form 1040 succession | line 20 = line 8; line 19 absent → line 21 = line 20; line 17 absent → line 18 = line 16; line 22 = max(line 18 − line 21, 0) | line-16 symbol repurposed as after-credit tax; double-counting credit; CTC present without authority | line-16 remains regular-tax pin; new symbols for Sch3/L20/after-credit | regular_tax (line 16) + line 20 → tax-after-credit → floor at zero; credit once |
| P10 pins/lifecycle | pins for source, income, creditability, election, threshold, regular tax, Sch3, Form 1040; explanation shows direct election not Form 1116 | missing pin; explanation claims Form 1116 completed; presentation treated as authority | correction/stale/restore as P1 | attribution chain → explanation/presentation → resolved or reject |

**Associated income (P4) selected shape:** per-statement association with
existing box-1a (required present on the same logical statement as each box-7
member) **plus** tax-year completeness authority that all foreign-source gross
income and foreign taxes in the class are on qualified Form 1099-DIV payee
statements and are passive. Do **not** infer foreign-source income amount from
box 7. Distinct foreign-income amount facts (shape B) are not required for the
first slice.

**Creditability (P5) selected shape:** hybrid — named component declarations
plus a derived eligibility conclusion pinned to those components. A single
unexplained `qualified` boolean is rejected.

**Box 8 (P3) selected shape:** each box-7 member requires an explicit companion
that is either (1) a non-empty country/U.S.-possession name, or (2) an explicit
RIC `not_applicable` authority (Form 1099-DIV instructions: RICs do not
complete box 8). Missing companion fails closed. Multi-country supplemental
allocation of one box-7 amount is **excluded** from the first slice.

**Qualified dividends:** retain box-1b coexistence on the existing line-3a
income path. Creditability still requires the explicit 16-day holding-period
and no-obligation components; do not compute holding period from trade history.

**Regular-tax symbol hygiene (P9):** keep `tax.us.2025.tax.total-tax` (or its
line-16 binding) as **Form 1040 line 16 regular tax**. Introduce distinct
symbols for Schedule 3 line 1, line 8, Form 1040 line 20, and tax-after-credit.
Bounded regular tax equals line 16 when Schedule 2 line 1a/1z and Form 4972 tax
are explicitly absent.

**Threshold vs cap:** `$300` for every non-MFJ status including MFS; `$600` for
MFJ only. Over-threshold **blocks** the direct election (no clip). Allowable
credit is `min(creditable_box7_subtotal, regular_tax)` only after the threshold
gate passes.

**Track 0 disposition:** contracts B7-C1 through B7-C10, together with accepted
ADR-0015, ADR-0016, ADR-0017, ADR-0020, ADR-0027, ADR-0029, ADR-0033, ADR-0035,
and ADR-0046, are sufficient for this bounded route on paper. **No new ADR is
required by the paper decision.** If implementation discovers a reusable product
contract that these cannot express (especially nonrefundable-credit composition
or regular-tax cap semantics), stop and return to the owner rather than editing
accepted ADRs or inventing silent defaults. Honest bounded authority does **not**
require Form 1116 machinery for this class.

## Proposed contract and ADR disposition

Reuse without edit: ADR-0015 (statement identity), ADR-0016 (per-family claim),
ADR-0017 (horizons), ADR-0020 / ADR-0029 (explanation and citations),
ADR-0027 / ADR-0033 (package/adoption exclusivity), ADR-0035 (dividend pattern),
ADR-0046 (presentation).

**Recommend a new Tier-2/Tier-3 ADR if and only if** paper shows that any of
the following is a reusable product contract not already settled by those ADRs
plus this plan:

- direct foreign-tax-credit **eligibility authority** composition (election +
  passive + payee-statement completeness + threshold + no carry + no deduction);
- **regular-tax cap** consumer contract against the line-16 symbol with Schedule 2
  absence boundary;
- **nonrefundable-credit composition** (Schedule 3 Part I completeness → line 8
  → Form 1040 line 20 → tax-after-credit with floor).

Do **not** force these into implementation prose merely to avoid an ADR. ADR
number and filename remain unreserved until final rebase. No accepted ADR is
edited.

## Scope

- Independent 2025 Form 1099-DIV box-7 amount fact: payer + logical statement +
  tax year; nonnegative U.S.-dollar source amount; correction supersession;
  multi-payer aggregation without identity collapse.
- Source family, horizon, closed-empty behavior, subtotal, mapping, citation.
- Additive residual successor: properties **3** and **5** only; preserve v1/v2/v3
  residual history; reject mixed residual/family package graphs that admit box 7
  twice.
- Box-8 companion authority per Track 0 (country string or explicit RIC
  not-applicable; never invent; multi-country supplemental allocation excluded
  or modeled only if paper settles a bounded shape).
- Associated-income and tax-year foreign-income completeness authorities per
  Track 0.
- Creditability component authorities and derived eligibility conclusion.
- Direct-election authority set: passive-all; payee-statements-all; filing-status
  threshold; total ≤ threshold; election=yes; no carryback/carryforward; no
  Schedule A deduction election; no Form-1116-required condition.
- Threshold gate and `min(box-7 subtotal, regular_tax)` cap as distinct steps.
- Schedule 3 line 1; explicit absence of every other Part I credit; line 8;
  Form 1040 line 20; bounded tax-after-credit succession with floor at zero;
  line-16 symbol preserved and not double-counted as the credit.
- Explanation and presentation: direct-election basis and block reasons
  visible; never claim Form 1116 was completed; presentation values are not
  authority.
- Additive package, published-registry, release, adoption successors after
  collision inventory; focused final-package test of the union of all ratified
  members plus this milestone’s successors.
- Unmodified regression fixtures for box 12, taxable interest, Schedule B,
  Schedule D, carryover, and Form 8949-adjacent line-16 consumers as present on
  the ratified line.

## Contracts

### B7-C1 — Independent box-7 family

Use `payer + statement + tax-year=2025`; statement identity carries no
file/upload/scan/document/evidence key (ADR-0015). Amount is a nonnegative
U.S.-dollar scalar source amount with named quantity and box-7 citation.
Corrections supersede the same logical statement; two originals from the same
payer remain distinct. Family closure is horizon-keyed and covers **box 7
only**. Closed-empty is explicit zero; absent closure is not zero. Subtotal
sums current members across payers and **never** reads residual recorded-boxes
content.

### B7-C2 — Residual succession and exclusive adoption

Historical residual versions that still contain box 7 remain immutable. Add a
new residual version whose properties are exactly boxes **3** and **5**. The
selected package adopts that residual and the independent box-7 family, never
an old residual that still records box 7. Package validation rejects:
old residual + box-7 family in one graph; same-statement contribution reaching
the subtotal through both shapes; raw/historical reach-around; mixed
historical/successor residual graphs. Historical package routes remain
resolvable and byte-unchanged. Boxes 3 and 5 remain recorded-only.

### B7-C3 — Box-8 country companion

Each box-7 statement item carries an explicit companion for box 8. Track 0
settles the admissible states (country/possession name vs RIC not-applicable).
Missing companion is never treated as absent-by-default. Do not invent a
country, collapse multiple countries, or silently accept multi-country
supplemental allocation unless that shape is explicitly modeled. Companion is
authority, not a composed credit amount.

### B7-C4 — Associated foreign-income authority

Box 7 names **tax**, not gross foreign income. The engine must establish that
related income is included in the U.S. return, all foreign-source gross income
in the class is passive and on qualified payee statements, and no unsupported
foreign-source income exists elsewhere — **without** inferring foreign-source
income solely from the box-7 amount. Preferred paper shape: per-statement
association with existing box-1a (and optional 1b) facts **plus** tax-year
completeness authority. Failure of association or completeness blocks the
credit claim; it does not invent amounts.

### B7-C5 — Creditability authority

Minimum explicit authority for each selected tax (or a derived conclusion pinned
to these components):

- tax type (income / war profits / excess profits, or tax in lieu);
- legal liability and payment status (cash-method paid for the class);
- no refund, rebate, subsidy, or reimbursement;
- no excluded-income association;
- dividend holding-period requirement met (Pub. 514 / Schedule 3 exception);
- no disqualifying short-sale or related obligation to pay the dividend;
- country recognition / non-terrorism support as required by the Schedule 3
  exception path.

Prefer concrete component declarations or source facts. A synthesized
`eligible` conclusion is allowed only if derived from named authority.

### B7-C6 — Direct-election eligibility

Explicit, auditable authority for:

| Fact | Source class |
| --- | --- |
| All foreign gross income passive | Contributed tax-year declaration (bounded class) |
| All foreign income and taxes on qualified payee statements | Contributed + closed box-7 family + excluded-source absences |
| Applicable filing-status threshold | Derived from `filing_status` ($300 / $600) |
| Total foreign tax within threshold | Derived from closed box-7 subtotal vs threshold |
| Taxpayer election | Contributed election fact (yes required; missing/declined block) |
| No carryback/carryforward | Contributed absence |
| No foreign-tax deduction election | Contributed absence |
| No Form-1116-required condition | Contributed / derived from the above |

### B7-C7 — Threshold and credit arithmetic

- Threshold: **$600** only for married filing jointly; **$300** for every other
  supported status including MFS.
- Above-threshold: **block** direct election (do not clip).
- Allowable credit: `min(creditable_box7_subtotal, regular_tax)`.
- Regular tax for the bounded class: Form 1040 **line 16** symbol, with
  explicit absence of Schedule 2 amounts that the Schedule 3 / Form 1116
  instructions would add, and absence of Form 4972 tax on line 16.
- If regular tax is zero, credit is zero (nonrefundable); never create negative
  tax unless an existing downstream contract already permits it (none does).
- Keep threshold eligibility distinct from the final cap.

### B7-C8 — Schedule 3 completeness

- Line 1 = direct foreign tax credit under B7-C6/C7.
- Every unsupported Schedule 3 Part I credit (lines 2–6 and other nonrefundable
  slots) is **explicitly absent**.
- Line 8 is complete only under that authority and equals line 1 in the
  bounded class.
- Closed-empty box-7 and no-foreign-tax cases remain representable (line 1/8
  zero only through honest closure + election path, or blocked when election
  claimed without tax).
- No unsupported credit is silently defaulted to zero.

### B7-C9 — Form 1040 credit and tax succession

- Form 1040 line 20 binds to Schedule 3 line 8.
- Line 19 (CTC/ODC) is explicitly absent in the bounded class so total
  nonrefundable credits for the succession equal line 20.
- Line 17 / other Schedule 2 additions that would change line 18 are explicitly
  absent so line 18 equals line 16 for the class.
- Tax after credits: `max(line_18 - line_21, 0)` with line_21 = line_20 under
  line-19 absence.
- Downstream total-tax publication for the class uses the new tax-after-credit
  symbol where the product claims “tax after nonrefundable credits”; **do not**
  overwrite `tax.us.2025.tax.total-tax`’s line-16 meaning without an additive
  succession that keeps both pins exact.
- Count the foreign tax credit **exactly once**.

### B7-C10 — Lifecycle, pins, explanation, presentation

- Box-7 correction displaces the credit and downstream tax result.
- Late family membership invalidates stale closure; successor closure restores
  publication.
- Election or eligibility correction displaces the result.
- Exact pins distinguish: source tax, associated income, creditability,
  election/eligibility, threshold, regular tax, Schedule 3, Form 1040 consumers.
- Explanation must not claim Form 1116 was completed; it must show
  direct-election basis and block reasons.
- Presentation uses existing ADR-0046 surface; presentation values are not
  authority. One canonical positive golden; compact negative mutations.

## Exact citation and authority pins

| Pin purpose | Official source and anchor |
| --- | --- |
| Direct election conditions and regular-tax entry | IRS, Instructions for Form 1116 (2025), “Election To Claim the Foreign Tax Credit Without Filing Form 1116”; line 20 regular tax, `https://www.irs.gov/instructions/i1116` |
| Election overview and non-exemption of creditability | IRS, Foreign Tax Credit — How to figure the credit, `https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit-how-to-figure-the-credit` |
| Creditability, holding period, credit vs deduction | IRS, Publication 514 (2025), `https://www.irs.gov/publications/p514` |
| Box 7 / box 8 meaning | IRS, Form 1099-DIV instructions, boxes 7–8, `https://www.irs.gov/instructions/i1099div` |
| Schedule 3 line 1 exception and Form 1040 credit lines | IRS, 2025 Form 1040 instructions, Schedule 3 line 1; Form 1040 lines 16–24, `https://www.irs.gov/instructions/i1040gi` |
| Schedule 3 structure | IRS, Schedule 3 (Form 1040), `https://www.irs.gov/pub/irs-pdf/f1040s3.pdf` |

URL-only payload strings are insufficient; citation resolution follows ADR-0029.

## Readiness and version-collision checkpoints

Before implementation, and again before final packaging / PR curation:

1. Fetch/prune origin; identify the latest ratified line with the repository
   resolver (do not guess).
2. Inventory every published tax schema, artifact-package schema, package,
   published registry, release, adoption, and relevant presentation artifact
   version on that line and this branch.
3. Capture an ignored ephemeral semantic ledger before rebase; preserve this
   milestone’s original delta; rebuild from the new ratified predecessor.
4. Choose unused successor filenames only after rebasing; preserve every
   ratified file and manifest row byte-for-byte.
5. Verify package exclusivity, registry checksums, release hashes, adoption
   pins, historical-route compatibility, and **union** of all ratified package
   members plus this milestone’s successors.
6. Verify regular-tax consumers still resolve; stop on semantic overlap or
   selected-version regression involving line 16 or credit symbols.

Current v17/v12/v10/v17 values are **not** reservations. Concurrent Form 8949
or other merges may advance the ratified tip; this milestone adds successors
and never restores an older state.

## Evidence matrix

All cases use synthetic identities and values. Existing regressions remain
unmodified.

| ID | Case or mutation | Expected result |
| --- | --- | --- |
| P1 | One box-7 statement below single-filer threshold | Credit publishes; Sch3 L1/L8 and Form 1040 L20 tie out |
| P2 | Multiple box-7 statements aggregating below threshold | Distinct identities; subtotal once; credit once |
| P3 | Exactly $300 non-joint | Eligible; credit = min(300, regular_tax) |
| P4 | One cent/dollar above $300 non-joint (per rounding contract) | Direct election blocked |
| P5 | Exactly $600 MFJ | Eligible |
| P6 | Above $600 MFJ | Blocked |
| P7 | MFS uses $300 threshold | $300+ blocks; $300 at boundary eligible |
| N1 | Missing election | Blocked |
| N2 | Election declined | Blocked |
| P8 | Foreign tax > regular tax | Credit = regular_tax; tax-after-credit floors at 0 |
| P9 | Zero regular tax | Credit 0; no negative tax |
| N3 | Missing associated foreign-income authority | Blocked |
| N4 | Non-passive foreign income present | Blocked |
| N5 | Foreign income not entirely on qualified payee statements | Blocked |
| N6 | Unqualified or refundable foreign tax | Blocked |
| N7 | Failed dividend holding-period authority | Blocked |
| N8 | Carryover or carryback present | Blocked |
| N9 | Deduction election present | Blocked |
| N10 | Foreign tax source outside Form 1099-DIV | Blocked |
| N11 | Another Schedule 3 credit present | Line 8 / completeness blocked |
| N12 | Box-8 companion missing when required | Blocked |
| P10 | Statement correction same logical identity | Supersedes; no double count |
| P11 | Multiple originals same payer | Distinct; aggregate once |
| P12 | Late member after closure; successor closure | Stale consumers leave; restoration recomputes |
| P13 | Box 1a fully included; box 7 does not reduce dividends | Lines 3a/3b unchanged by credit path |
| P14 | Supported box 1b coexistence if retained | Income path intact; credit still gated by creditability |
| P15 | Box 7 appears exactly once in credit path | No double credit; no income reduction |
| P16 | Sch3 L1 and L8 tie-out; Form 1040 L20 and tax-after-credit tie-out | Exact equality under bounded absences |
| N13 | Residual historical/successor mixed package | Validation rejects |
| N14 | Box-12, interest, Schedule B, Schedule D, carryover, line-16 regressions | Unchanged pass |
| P17 | Canonical positive presentation golden | Direct-election basis, amounts, citations visible |
| N15 | Compact negative presentation mutations | Fail-loud / block / redact without full goldens |

## Tracks and review structure

### Track 0 — Paper boundary and contract checkpoint

Foreman-owned after owner plan approval. Record Gate-1 scores, paper instances,
negatives, lifecycle traces, maps, exact citations, ADR disposition, and any
owner narrowing. Stop at paper if it distinguishes the shape. **No rival
prototype and no implementation charter** until Track 0 is recorded and the
owner approves moving on.

### Track 1 — Integrated production build (preferred)

After Track 0 settles authority and credit-composition contracts, **one**
integrated Builder implements source/residual/eligibility citizens and Schedule
3 / Form 1040 integration, package/release/adoption graph, explanation,
presentation golden, and tests.

**Split only if Track 0 proves source authority and downstream credit
composition are independently substantial**, still inside the **one** milestone
PR:

1. Source / residual / eligibility citizens.
2. Schedule 3 / Form 1040 integration.

Reuse box-12 Builder/Reviewer context for residual-family and package cold-start
cost; do **not** let that familiarity substitute for foreign-tax authority
review. Do **not** create a general FTC framework or Form 1116 engine.

If existing evaluator, marshal, package, or presentation substrate cannot
express the settled paper shape, the Builder stops and returns the issue to the
owner rather than expanding scope.

## Review gate — Integrated independent review

One author-independent Reviewer measures: residual exclusivity, associated-
income honesty, creditability component fidelity, election/threshold arithmetic,
Schedule 3 completeness, line-16 symbol hygiene, single credit count, tax floor,
package collisions, exact pins, explanation (no Form 1116 claim), presentation,
and all evidence-matrix regressions. Report falsifiable `READY` or numbered
findings.

### Repair and closeout

At most one bounded findings-only repair cycle for the same Builder. A second
substantive defect, new product decision, or scope expansion returns to the
owner. Working charters and interim records are removed at final curation; this
plan and the retrospective preserve durable decisions.

## Durable commit structure

1. `plan: select Form 1099-DIV box 7 direct FTC` — this plan, planned phase
   state, roadmap selection, and frontier split; **no implementation**.
2. `track-0: record box-7 direct FTC paper boundary` — after owner plan
   approval.
3. `track-1: implement bounded box-7 direct FTC route` — production
   implementation and focused tests/fixtures (optionally two sub-commits if
   split, still one PR).
4. Provisional review/repair commits, folded into Track 1 before curation.
5. Closeout commit with retrospective, curated records, final state, and no
   temporary briefing capsule.

No schema, package, release, registry, adoption, or ADR number is reserved
before the rebase checkpoints.

## Fixtures, verification, economy, and data safety

Committed fixtures use synthetic `demo.*` identities, nonnegative sample
values, and no absolute paths, personal documents, real facts, dispositions, or
private outputs. Prefer shared builders and negative mutations over sprawling
fixture trees. While iterating run only touched modules. Final focused set:
source-family/admission, residual exclusivity, eligibility/threshold,
Schedule 3 / Form 1040 succession, lifecycle, package/resolver, explanation,
presentation, and regressions for box 12, interest, Schedule B, Schedule D,
carryover, and line-16 consumers; plus `tests.test_schema_registry` when
schemas or manifests change. Typed changes run `python3 -m mypy`; final checks
include `git diff --check`, governance lint, envelope scan, and CI `verify`.
Named positives enter through `live_coordinate_run`.

Personal source documents, current-year facts, prior returns, real values,
identifiers, credentials, workspaces, screenshots, and generated personal
artifacts remain outside the repository, branch, review, chat, and output.

## Durable versus temporary artifacts

| Durable | Temporary (never merge / remove at closeout) |
| --- | --- |
| This plan; Track 0 paper record in-plan or linked retrospective exhibit | Ephemeral semantic ledgers (ignored, uncommitted) |
| New content citizens, additive package/registry/release/adoption | Working charters, interim review prompts |
| Synthetic fixtures and one presentation golden | Rival prototype branches (none authorized unless owner expands) |
| Optional new ADR if Track 0 requires it | `initial_briefing_follow_up` capsule if added |

## Frontier updates (required)

Split the prior single “box 7” named block into:

1. **Direct foreign tax credit without Form 1116** — **selected** (this plan).
2. **General Form 1116 foreign tax credit** — future candidate.
3. **Foreign-tax deduction election (Schedule A)** — future candidate.

## Exit criteria

- Owner has approved this plan.
- Track 0 paper evidence settles the contract shape (and ADR disposition).
- Integrated implementation (or authorized two-track split) is complete.
- Evidence matrix positives and negatives pass; residual exclusivity holds;
  dividend income paths preserved; credit counted once; tax never negative from
  the credit alone.
- Package union test green; historical files byte-identical; independent review
  READY with at most one repair cycle; CI green; owner merges the single curated
  milestone PR.

## Recommendation for owner approval

**Do not charter a Builder until the owner approves this plan** and any
recommended narrowing (especially declaration-based holding-period authority
vs box-1b exclusion). Track 0 remains the primary cost-control mechanism and
must finish on paper before implementation.
