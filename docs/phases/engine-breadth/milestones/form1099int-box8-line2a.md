<!-- foreman-context-v1
{
  "version": 1,
  "topic": "form1099int-box8-line2a",
  "milestone_state": "closed",
  "status": "CLOSED. The bounded 2025 Form 1099-INT box-8 succession of the closed box-12 line-2a route is synthetic complete and independently reviewed READY.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099int-box8-line2a.md",
  "scope": [
    "add an independent 2025 Form 1099-INT box-8 source family reusing accepted 1099-INT statement identity",
    "add per-statement box-9 absence/zero companion authority on the live production path",
    "succeed the closed box-12-only line-2a rule so line 2a aggregates closed box-12 and closed box-8 subtotals",
    "replace unconditional no-f1099int-tax-exempt yes with a two-path completeness gate (Path A declaration vs Path B closed box-8 family)",
    "preserve remaining line-2a scope absences, reported-only downstream semantics, package/release/adoption exclusivity, explanation, and presentation",
    "preserve historical box-12 package exclusivity and all focused dividend/interest/Schedule B/Schedule D/box-12 regressions"
  ],
  "non_goals": [
    "no nonzero Form 1099-INT box 9, Form 6251, or general AMT computation",
    "no Form 1099-OID boxes 2 or 11, unreported tax-exempt interest, or tax-exempt premium/acquisition-premium adjustments",
    "no state or municipal returns, taxable Social Security, child-income elections, credits, deductions, Schedule B changes, Schedule D or Form 8949 changes",
    "no Form 1099-INT box-4 withholding / line 25b, filing, transmission, real-data operation, or UI redesign",
    "no claim that line 2a is universally informational or that tax-exempt interest has no effect outside the supported graph"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/form1099int-box8-line2a.md#Official 2025 paper boundary",
      "docs/phases/engine-breadth/milestones/form1099int-box8-line2a.md#Contracts",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md",
      "docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0019-selector-citizen-and-conditional-structures.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0024-conditional-structures-in-the-rule-language.md",
      "docs/adr/0037-conditional-multi-dependency-nonpublication.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0059-prior-return-capital-loss-authority.md",
      "packages/content/tax/2025/rule.form1040-line2a.json",
      "packages/content/tax/2025/line2a-scope.bundle.json",
      "packages/content/tax/2025/f1099div-box12.bundle.json",
      "packages/content/tax/2025/family.f1099div-12.json",
      "packages/content/tax/2025/interest-composition.v4.json",
      "packages/content/tax/2025/package.core-calculations.v17.json",
      "packages/content/tax/2025/published-packages.v12.json",
      "packages/sample_data/form1099div_box12_line2a/adoptions/adopt-core-v17-current.json",
      "packages/sample_data/form1099div_box12_line2a/publication_surface/releases/demo.release.2025.v10.json",
      "packages/tax/loader.py",
      "packages/derivation/live.py",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/form1099int-box8-line2a.md#Contracts",
      "docs/phases/engine-breadth/milestones/form1099int-box8-line2a.md#Evidence matrix",
      "docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md#Contracts",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0037-conditional-multi-dependency-nonpublication.md",
      "docs/adr/0059-prior-return-capital-loss-authority.md",
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
      "docs/milestone-retrospectives/2026-08-05-form1099int-box8-line2a.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/phases/engine-breadth/milestones/form1099int-box8-line2a.md",
      "docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md"
    ]
  }
}
-->
# Milestone: Form 1099-INT Box 8 Tax-Exempt Interest to Form 1040 Line 2a

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner on 2026-08-05. This milestone
**extends** the closed Form 1099-DIV box-12 → line-2a route; it is not a new
independent line-2a implementation.

## Objective

Make a bounded 2025 return computable when one or more Form 1099-INT statements
report nonnegative tax-exempt interest in box 8.

The complete Form 1040 line-2a amount must aggregate:

1. the existing closed Form 1099-DIV box-12 family; and
2. a new independently closed Form 1099-INT box-8 family.

The result remains **reported-but-not-directly-taxable**. It must not be added
directly to Form 1040 line 9, taxable income, or Schedule B Part I.

## Current merged state (prerequisite)

`origin/main` at planning base `b0480bc` (Merge PR #158,
`milestone/form1099div-box12-line2a`) includes the closed box-12 milestone:

| Surface | Ratified tip |
| --- | --- |
| Core package | `package.core-calculations.v17` (185 members, `artifact-package.v14`) |
| Published registry | `published-packages.v12` |
| Release | `demo.release.2025.v10` under `packages/sample_data/form1099div_box12_line2a/` |
| Adoption | `adopt-core-v17-current` |
| Quantity vocabulary | through `quantity-vocabulary.v6` |
| Artifact-package schema | through `artifact-package.v14` |
| Line-2a rule | `tax.us.2025.rule.form1040-line2a@v1` = closed box-12 subtotal only |
| Scope authority | `line2a-scope.bundle` including unconditional `no-f1099int-tax-exempt` = yes |
| Companion enforcement | box-12 → box-13 pair in `domain_companion_presence_pairs()` and live install |
| Retrospective | `docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md` |
| Plan (closed) | `docs/phases/engine-breadth/milestones/form1099div-box12-line2a.md` |

**Do not reserve** package, registry, release, adoption, or schema versions on
this planning base. The active Form 8949 milestone may merge while this work
is in flight; final packaging rebuilds from the latest ratified predecessor.

### Parallel-track package inventory (other worktrees / branches)

Read-only inventory after `git fetch --prune` (Form 8949 worktree not
modified):

| Branch / surface | Core package tip | Published tip | Artifact-package tip | Notes |
| --- | --- | --- | --- | --- |
| `origin/main` (planning base) | **v17** (185 members, box-12 present) | **v12** | **v14** | Ratified line |
| `origin/milestone/schedule-d-form8949-covered-wash-sale` @ `58ea64e` | **v17** (215 members, **no** box-12 members) | **v12** | **v13** | Rival claim on the same version number with different semantics; 41 Form-8949-only members; missing main's 11 box-12 line-2a members; schema lag vs main (`v13` vs `v14`) |
| UI worktree (`document-oriented-entry`) | n/a (UI line) | n/a | n/a | Not an engine package predecessor |

**Implication:** if Form 8949 merges before this milestone packages, both
milestones must rebase and regenerate as additive unions from the new
predecessor. Never rebuild from a hardcoded historical filename. Capture a
temporary ignored semantic ledger before the real rebase; stop on unexplained
member loss, version regression, reversed retirement, or semantic overlap.


### Owner-confirmed packaging successors (2026-08-05)

Use **higher versions wherever the surface must change**. Do not edit ratified
predecessor files. After Form 8949 merged to `main` (`package.core-calculations.v18` /
`published-packages.v13` / `artifact-package.v15` / `quantity-vocabulary.v7`),
this milestone's additive successors are:

| Surface | Predecessor (byte-immutable) | Successor (this milestone) | Why higher |
| --- | --- | --- | --- |
| Quantity vocabulary schema | `quantity-vocabulary.v7` (Form 8949) | **`quantity-vocabulary.v8`** | New enum token `tax-exempt-interest` |
| Artifact-package schema | `artifact-package.v15` (Form 8949) | **`artifact-package.v16`** | Admits `quantity-vocabulary.v7` and `v8` |
| Core package | `package.core-calculations.v18` (Form 8949 on `main`) | **`package.core-calculations.v19`** (`schema: artifact-package.v16`) | Union of Form 8949 v18 + box-8 / line-2a succession |
| Published registry | `published-packages.v13` (Form 8949 on `main`) | **`published-packages.v14`** | Registers core `v19` |
| Release | `demo.release.2025.v10` | **`demo.release.2025.v12`** | Pins core `v19` graph |
| Adoption | `adopt-core-v18-current` (Form 8949) | **`adopt-core-v19-current`** | Adopts core `v19` + release `v12` |

Schema publication manifests (`packages/schemas/kernel/published.json`,
`packages/schemas/derivation/published.json`) are **append-only**.

If a concurrent milestone (e.g. Form 8949) lands first and consumes any of
these filenames, rebuild from the new predecessor and choose the **next
unused higher** pair — never overwrite ratified files, never reuse a version
number with different semantics.

## Supported return class

Bound the milestone to:

- tax year **2025**;
- one or more Form **1099-INT box-8** amounts, including multiple statements or
  payers;
- existing Form **1099-DIV box-12** amounts **or** an explicitly **closed-empty**
  box-12 family;
- Form 1099-INT **box 9 absent or numeric zero** on every statement carrying
  box 8;
- **no** Form 1099-OID tax-exempt stated interest or tax-exempt OID;
- **no** unreported/non-form tax-exempt interest;
- **no** tax-exempt bond-premium or acquisition-premium adjustment;
- **no** excluded downstream consumer of tax-exempt interest;
- otherwise supported unrelated income.

## Official 2025 paper boundary

Ground the plan in current official sources:

| Source | Anchor and confirmation for this milestone |
| --- | --- |
| [2025 Form 1040 instructions, line 2a](https://www.irs.gov/instructions/i1040gi) | Tax-exempt stated interest is shown in **box 8 of Form 1099-INT** (and tax-exempt OID routes on Form 1099-OID that this milestone excludes). Enter the total on **line 2a**. Also include exempt-interest dividends from **Form 1099-DIV box 12**. If a tax-exempt bond was acquired at a **premium**, only the **net** tax-exempt interest is reported on line 2a — this milestone **blocks** premium adjustment rather than computing it. Tax-exempt interest is **not** taxable interest on **line 2b**. |
| [Instructions for Forms 1099-INT and 1099-OID](https://www.irs.gov/instructions/i1099int) | **Box 8** is tax-exempt interest. **Include specified private activity bond interest in box 9 and in the total for box 8** — box 9 is already in box 8 and must **not** be added a second time to line 2a. Exempt-interest dividends are on Form 1099-DIV, not 1099-INT. |
| [Publication 550](https://www.irs.gov/publications/p550) | Reporting tax-exempt interest: aggregate reported tax-exempt interest on line 2a; distinguish taxable interest; note AMT treatment for specified private activity bond interest without converting box 9 into a second line-2a addend. |
| [Schedule B instructions](https://www.irs.gov/pub/irs-pdf/i1040sb.pdf) | Tax-exempt interest is **not** reported on Schedule B Part I as taxable interest; box 8 totals go to Form 1040 line 2a. An amount in box 9 is generally reported on Form 6251 (out of scope; nonzero box 9 **blocks** this route). |

Confirmed paper facts for Track 0 and implementation contracts:

1. **Box 8 is included in Form 1040 line 2a.**
2. **Box 9 identifies specified private-activity-bond interest already included
   in box 8** and must not be added a second time; nonzero box 9 routes toward
   Form 6251 / AMT, which this milestone does **not** implement.
3. **Bond-premium adjustments can change the amount reported on line 2a**; this
   milestone does not compute them and requires explicit absence authority.
4. **Tax-exempt interest is not taxable-interest income on line 2b** and is not
   a Schedule B Part I itemization of taxable interest.

## Non-goals

Explicitly exclude:

- nonzero Form 1099-INT box 9;
- Form 6251 or general AMT computation;
- Form 1099-OID boxes 2 or 11 and all tax-exempt OID;
- tax-exempt bond-premium and acquisition-premium adjustments;
- unreported or non-form tax-exempt interest;
- state or municipal return treatment;
- Schedule B changes;
- Schedule D or Form 8949 changes;
- Form 1099-INT box-4 withholding and Form 1040 line 25b;
- taxable Social Security, child-income elections, credits, or deductions that
  consume tax-exempt interest;
- a claim that line 2a is universally informational or that tax-exempt interest
  has no effect outside the supported graph;
- filing, transmission, real-data operation, or UI redesign;
- mutation of any ratified schema, citizen, package, registry, release,
  adoption, fixture, or accepted ADR.

## Track 0 — Gate-1 decision inventory (paper-first)

Track 0 starts at paper under the project's prototype gate. Scores use four
Gate-1 axes (future blast radius, migration cost, residual uncertainty after
paper examples, inability to test cheaply during implementation), each 0–2.
Escalate to a rival prototype **only** if paper and accepted contracts leave a
genuine competing shape. No separate schema-gate track is authorized unless a
real new schema or runtime contract must settle independently.

| Proposition | Blast | Migration | Paper uncertainty | Cheap-test gap | Total | Planned disposition |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P1. Box-8 family authority (identity, nonnegative amount, independent closure) | 1 | 1 | 0 | 0 | 2 | Paper; reuse ADR-0015/0016/0017 and the box-1/box-3/box-10 family pattern |
| P2. Box-9 companion authority (null/zero only; live-path install; no Form 6251) | 1 | 1 | 0 | 0 | 2 | Implementation contract patterned on box-13; **mandatory live-path pair** (box-12 review lesson) |
| P3. Line-2a composition succession (box-12 + box-8 coextensive universe) | 2 | 2 | 1 | 1 | 6 | Paper compares declared composition citizen vs additive rule successor; **prefer declared tax-exempt-interest composition citizen** if schema fit is cheap; else additive `rule.form1040-line2a` successor with exact family claims |
| P4. Two-path `no-f1099int-tax-exempt` completeness (Path A declaration / Path B closed box-8) | 2 | 2 | 1 | 1 | 6 | Paper; reuse ADR-0059 / ADR-0037 two-path / conditional-dependency pattern; Path B exhausts the **bounded** Form 1099-INT tax-exempt surface (box 8 only) |
| P5. Remaining completeness boundary (OID, unreported, premium, excluded consumers) | 1 | 1 | 0 | 0 | 2 | Implementation: preserve existing scope facts as unconditional yes; do not imply them from box-8 closure |
| P6. Reported-only downstream semantics | 1 | 1 | 0 | 0 | 2 | Preserve box-12 behavior; line 2a never inputs line 9 / taxable income / Schedule B Part I |
| P7. Lifecycle, exact pins, historical box-12 package exclusivity | 1 | 1 | 0 | 0 | 2 | Implementation and adversarial tests; historical package bytes immutable |

**Gate-0 discipline:** P3 and P4 are the primary contract propositions. P1–P2
and P5–P7 are tightly dependent or implementation-boundary obligations. If
paper cannot distinguish P3–P4, stop and return a bounded prototype plan or
owner choice rather than inventing during build.

### Preferred paper shapes (to settle in Track 0 record)

#### P1 — Box-8 family authority

- Reuse accepted Form 1099-INT statement identity: **payer + logical statement +
  tax year 2025** (ADR-0015). No file/upload/scan/document/evidence key.
- Nonnegative box-8 source amount with named quantity (new quantity citizen if
  needed) and Form 1099-INT box-8 citation.
- Independent source family, horizon, closure mapping, subtotal, and correction
  lifecycle. Closed-empty is explicit zero; absent closure is not zero.
- Closing box 1, box 3, or box 10 says **nothing** about box 8. Box-8 closure
  says nothing about taxable-interest composition.

#### P2 — Box-9 companion authority

- Per-statement companion fact tied to the **same** logical statement as the
  box-8 member.
- Admit only explicit **null/absent** or numeric **zero**.
- Nonzero value is a hard block and **never** creates Form 6251 input.
- Missing companion is not treated as absent.
- Register the pair in `domain_companion_presence_pairs()` **and** ensure
  `live_coordinate_run` / production projection installs it (do not repeat the
  box-12 production-path omission).

#### P3 — Line-2a composition succession

Current rule (`@v1`):

```text
line-2a = closed box-12 subtotal
  when box-12 closed
   and no-f1099int-tax-exempt = yes
   and all other scope components = yes
```

**Paper candidate A (composition citizen) — not selected:**

Introduce a small **tax-exempt-interest composition** citizen (ADR-0016) whose
declared coextensive universe for this bounded route is exactly:

| Slot | Family | Authorizes subtotal |
| --- | --- | --- |
| Form 1099-DIV box 12 | `tax.us.2025.f1099div.12` | box-12 subtotal (existing) |
| Form 1099-INT box 8 | `tax.us.2025.f1099int.b8` (proposed) | box-8 subtotal (new) |

```text
line-2a = box-12 subtotal + box-8 subtotal
```

only when both families are closed (closed-empty allowed) and completeness
gates (P4–P5) hold. Neither family's closure promotes a claim about the other.
Box-12-only, box-8-only, closed-empty, and mixed-source returns are all
explicit.

**Selected shape (Alternative B — additive rule successor):**

`rule.form1040-line2a@v2` publishes `add(box-12-subtotal, box-8-subtotal)` with
`require_closed` on both families and exact pins, without a separate
composition citizen. Acceptable if Track 0 shows a new composition schema
would be pure cost. Reject any shape that leaves only one family required when
the other is open.

**Historical rule `@v1` remains immutable** and package-exclusive against the
successor; historical box-12 routes continue to resolve.

#### P4 — Two-path `no-f1099int-tax-exempt` completeness

Do **not** leave `tax.us.2025.line2a-scope.no-f1099int-tax-exempt` as an
unconditional required `yes` when box-8 interest is present.

| Path | Gate | Box-8 family | Meaning |
| --- | --- | --- | --- |
| **A** | declaration `no-f1099int-tax-exempt` = **yes** | not required for completeness (box-8 may be closed-empty or unused; Path A asserts no INT tax-exempt source exists) | preserves existing box-12-only returns |
| **B** | box-8 family **closed** on its current horizon **and** every box-8 member has admissible box-9 companion | required | box-8 is the supported Form 1099-INT tax-exempt source |

**Path B exhausts the bounded Form 1099-INT tax-exempt source surface** for
this milestone (box 8 only; box 9 is a non-additive companion). No narrower
residual INT absence declaration is required unless Track 0 discovers another
INT box that paper routes to line 2a independently of box 8 (none expected).

Exact branch pins: unused-path authority must not leak into the selected
disposition (ADR-0037 / ADR-0059 pattern). Path switch A→B or B→A displaces
line 2a. Prefer a `conditional_dependency_set` (or accepted rule-language
conditional) rather than inventing a third completeness mechanism.

Historical box-12 fixtures that assert `no-f1099int-tax-exempt = yes` remain
valid Path A returns under the successor package.

#### P5 — Remaining completeness boundary

Preserve as **unconditional** explicit authorities (yes required):

- no Form 1099-OID tax-exempt source;
- no unreported tax-exempt interest;
- no premium adjustment;
- no child-income election;
- no taxable-Social-Security consumer;
- no Form 6251/AMT consumer;
- no credit using tax-exempt interest;
- no deduction using tax-exempt interest.

Box-8 closure does **not** imply any of these.

#### P6 — Reported-only downstream semantics

- Line 2a equals the supported tax-exempt-interest composition.
- Absent from direct line-9 and taxable-income arithmetic.
- Not itemized as taxable interest on Schedule B Part I.
- Explanation and presentation describe **bounded** reported-only behavior
  without a universal downstream claim.

#### P7 — Lifecycle and exact pins

- Multiple statements and payers aggregate without identity collapse.
- Corrected statement supersedes the same logical statement.
- Late membership invalidates stale closure; re-closing restores publication.
- Box-9 correction displaces the line-2a result.
- Historical box-12 package-exclusivity protections remain intact.


### Track 0 record — paper settled 2026-08-05

Owner approved the milestone plan on 2026-08-05, including the preferred
Track 0 shapes. Paper distinguishes the selected succession; **no rival
prototype** and **no new schema-gate track** are authorized. Synthetic paper
values only.

| Proposition | Positive instances | Meaningful negatives | Lifecycle trace | Producer → authority → consumer → failure |
| --- | --- | --- | --- | --- |
| P1 box-8 family | one payer/statement box 8 = `80`; two payers `80` + `20` | open closure; negative box 8 rejected; box-1/box-3 closure does not close box 8 | corrected `80`→`95` same payer/statement/year; late second statement advances horizon; re-close restores subtotal | logical 1099-INT statement → box-8 family horizon/closure → box-8 subtotal → open/stale/superseded consumer |
| P2 box-9 companion | box 9 null; box 9 `0` on same statement as box 8 | missing companion; nonzero box 9 | box-9 correction on same statement displaces line 2a | box-8 member + box-9 witness → admission/live companion pair → publish or block; never Form 6251 |
| P3 line-2a composition succession | box-12-only (Path A); box-8-only with box-12 closed-empty (Path B); mixed `100` box-12 + `80` box-8 → line 2a `180` | open box-12; open box-8 under Path B; historical `@v1` line-2a rule mixed with successor family graph | correction of either subtotal displaces line 2a; historical package still resolves box-12-only `@v1` | closed family subtotals → successor line-2a rule → form field / explanation; mixed historical/successor exclusivity rejection |
| P4 two-path INT completeness | Path A: `no-f1099int-tax-exempt=yes` with closed box-12, no box-8 members; Path B: box-8 closed + companions with declaration not required as unconditional `yes` | Path B missing/open box-8; Path A with contradictory non-empty box-8 under a `yes` declaration; path-switch without re-pin | A→B and B→A path switches displace line 2a with exact selected-path pins | scope/conditional gate → line-2a when → publish or DEPENDENCY/guard block; unused-path authority does not leak |
| P5 residual scope | all remaining scope components `yes` with Path A or Path B | OID tax-exempt present; unreported present; premium present; each excluded downstream consumer present | scope component supersession leaves line 2a non-current until successor authority is current | residual scope facts → line-2a when → block without claiming those sources computed |
| P6 reported-only | line 2a changes (`180`); line 9 and taxable income unchanged vs baseline without tax-exempt | claim that line 2a feeds line 9; Schedule B Part I itemizing box 8 as taxable interest | N/A | line-2a field → zero-authority presentation/explanation; not an input to line 9 / taxable income / Schedule B Part I |
| P7 lifecycle/pins/exclusivity | multi-payer aggregate once; closed-empty zeros; box-12 package exclusivity probes remain | raw/historical reach-around; stale closure after late member; double-count same statement | late member invalidates; restoration recomputes; box-9 correction displaces | exact pins (family, mapping, horizon, closure, path gate, citations) → resolver/explanation/presentation |

#### Settled decisions

**P1 — Box-8 family.** Reuse ADR-0015 Form 1099-INT statement identity
(payer + logical statement + tax year 2025). Independent nonnegative box-8
source amount, family, horizon, closure mapping, subtotal, citation, and
correction lifecycle. Closing boxes 1, 3, or 10 says nothing about box 8;
box-8 closure says nothing about taxable-interest composition or box 12.

**P2 — Box-9 companion.** Per-statement companion fact on the same logical
statement as the box-8 member. Admit only explicit null/absent or numeric
zero. Nonzero is a hard block and never creates Form 6251 input. Missing
companion is not treated as absent. Register in
`domain_companion_presence_pairs()` **and** install on the live production
path (`install_domain_companion_presence` / `live_coordinate_run`) — do not
repeat the box-12 production-path omission.

**P3 — Line-2a composition succession → Alternative B (rule successor with
exact dual-family claims).**

Paper and accepted contracts: Form 1040 line 2a is the aggregate of supported
tax-exempt sources (box 12 and box 8 in this bounded class). ADR-0016 requires
a coextensive supported universe and independent family claims.

Alternative A (dedicated tax-exempt-interest composition citizen + new schema)
would mirror `taxable-interest-composition.v1`, but **no existing tax-exempt
composition schema exists**. A new schema is not justified for a two-family
sum the rule language already expresses; that cost is pure migration without
paper distinction. **Alternative B is selected:**

```text
line-2a = box-12-subtotal + (Path A ? 0 : box-8-subtotal)
```

implemented as an additive **`rule.form1040-line2a` successor** that:

- requires **box-12 family closed** (closed-empty allowed);
- under Path B, requires **box-8 family closed** (closed-empty allowed) and
  sums both subtotals;
- under Path A, does **not** require box-8 family presence and contributes
  **zero** from the INT slot;
- pins both family identities, subtotals, mapping, horizon/closure, selected
  path gate, residual scope, and citations;
- leaves historical `@v1` (box-12-only + unconditional `no-f1099int=yes`)
  immutable and package-exclusive against the successor.

This establishes a coextensive **bounded** universe of exactly the two
supported families without promoting either family's closure into a claim
about the other. Future Form 1099-OID tax-exempt support may revisit a
composition citizen when a third supported slot arrives.

**P4 — Two-path `no-f1099int-tax-exempt` completeness.**

| Path | Gate | Box-8 family | Line-2a INT contribution |
| --- | --- | --- | --- |
| **A** | `no-f1099int-tax-exempt` = **yes** | not required | `0` |
| **B** | box-8 family **closed** on its current horizon **and** every current box-8 member has an admissible box-9 companion | required | closed box-8 subtotal |

**Path B exhausts the bounded Form 1099-INT tax-exempt source surface** for
this milestone (box 8 only; box 9 is a non-additive companion already included
in box 8 per IRS instructions). No narrower residual INT absence declaration
is required.

Exact branch pins: unused-path authority must not leak (ADR-0037). Prefer a
`choose` / conditional structure in the successor rule `when`/`value` (and
requires list consistent with the selected path), patterned on ADR-0059
two-path completeness and existing rule-language conditionals (ADR-0024).
Path switch A→B or B→A displaces line 2a. Historical box-12 fixtures that
assert `no-f1099int-tax-exempt=yes` remain valid Path A returns under the
successor package when box-12 is closed and residual scope holds.

If Path A is selected, a current non-empty box-8 membership is a contradictory
state and must fail honestly (not silently ignore box-8 amounts).

**P5 — Residual scope.** Preserve unconditional `yes` for:
no-f1099oid-tax-exempt; no-unreported-tax-exempt; no-premium-adjustment;
no-child-income-election; no-taxable-social-security; no-amt-form-6251;
no-credit-using-tax-exempt; no-deduction-using-tax-exempt.
Box-8 closure does not imply any of these.

**P6 — Reported-only.** Line 2a remains absent from line 9, taxable-income
arithmetic, and Schedule B Part I taxable-interest itemization. Explanation
and presentation describe bounded reported-only behavior without a universal
downstream claim.

**P7 — Lifecycle and exclusivity.** Multi-statement aggregation without
identity collapse; correction supersession; late membership invalidates stale
closure; re-close restores; box-9 correction displaces line 2a; historical
box-12 package-exclusivity protections remain intact.

**Track 0 disposition:** B8-C1 through B8-C6, together with accepted
ADR-0015, ADR-0016, ADR-0017, ADR-0020, ADR-0024, ADR-0027, ADR-0029,
ADR-0033, ADR-0037, ADR-0046, and the ADR-0059 two-path **pattern** (not an
edit of ADR-0059), are sufficient for this bounded route. **No new ADR** is
required by the paper decision. **No new composition schema.** Any
implementation discovery that needs a new product contract, new evaluator op,
or new schema stops and returns to the owner; no accepted ADR is edited.

## Contracts

### Proposed contracts

### B8-C1 — Independent box-8 family

Nonnegative Form 1099-INT box-8 amount fact keyed by payer, logical statement,
and tax year 2025. Independent source family, horizon, closed-empty behavior,
subtotal, mapping, and citation. Aggregate multiple payers without collapsing
identity. Independent of boxes 1, 3, 10 and of Form 1099-DIV box 12.

### B8-C2 — Box-9 companion without AMT computation

Explicit per-statement box-9 absence/zero authority. Nonzero blocks. No missing
companion treated as absent. Live coordinator installs and validates the pair.
Never creates Form 6251 input.

### B8-C3 — Line-2a multi-family composition succession

Successor line-2a producer consumes **both** closed family subtotals under the
selected P3 shape. Historical `@v1` rule and package remain resolvable and
byte-unchanged. Package exclusivity rejects graphs that adopt both historical
line-2a producer and successor for the same current claim, or that mix
historical and successor residual shapes already protected by box-12.

### B8-C4 — Two-path Form 1099-INT completeness

Successor completeness gate implements Path A / Path B for the former
unconditional `no-f1099int-tax-exempt` slot. Exact pins for the selected path.
Path B does not require a contradictory `yes` declaration.

### B8-C5 — Residual scope and reported-only semantics

Unconditional remaining scope components. Line 2a published with exact pins;
not an input to line 9, taxable income, or Schedule B Part I taxable interest.
Excluded downstream consumers remain honest blocks.

### B8-C6 — Package, release, adoption, presentation

One verified additive package, published registry, release, and adoption
successor after final collision inventory. One canonical positive presentation
golden via `live_coordinate_run`; compact in-memory negative mutations.

## ADR disposition

Existing accepted ADRs remain unchanged. Likely reuse:

- ADR-0015 statement identity
- ADR-0016 family claim / composition
- ADR-0017 horizons
- ADR-0019 / ADR-0024 / ADR-0037 conditional structures and multi-dependency
- ADR-0020 / ADR-0029 explanation and citation pins
- ADR-0027 / ADR-0033 package/adoption
- ADR-0046 presentation
- ADR-0059 as the **pattern** for two-path completeness (not an edit)

Track 0 should produce **at most one** new Tier-2/Tier-3 ADR if paper shows
that multi-family line-2a composition plus two-path INT completeness are
future-facing contracts not fully stated by those ADRs. **Do not reserve an
ADR number** until after the final rebase (Form 8949 may publish successors).
If accepted ADRs plus this plan fully express the shape, record the decision
in this plan and the retrospective instead. No accepted ADR is edited.

## Scope (implementation after owner approval)

- Add independent 2025 Form 1099-INT box-8 amount, family, horizon, closure,
  subtotal, mapping, and citation.
- Add box-9 companion authority and **live-path** companion-presence pair.
- Succeed line-2a composition to aggregate closed box-12 and box-8 subtotals.
- Succeed completeness so Path A preserves box-12-only returns and Path B
  admits closed box-8 without an unconditional `no-f1099int-tax-exempt = yes`.
- Preserve remaining scope absences and reported-only downstream semantics.
- Publish additive package / registry / release / adoption successors after
  rebase checkpoints.
- Prove line 2a can change while line 9 and taxable income remain unchanged.
- Preserve box-12, dividend, taxable-interest, Schedule B, Schedule D,
  carryover, and (when present on final base) Form 8949 regressions.

## Evidence matrix

### Required fixtures (minimum)

| ID | Case | Expected |
| --- | --- | --- |
| P1 | One box-8 payer | Closed box-8 subtotal; line 2a includes amount under Path B |
| P2 | Multiple box-8 payers/statements | Distinct identities; exact aggregate once |
| P3 | Box-8-only line 2a; box-12 family closed empty | Line 2a = box-8 total |
| P4 | Box-12-only line 2a; Path A `no-f1099int-tax-exempt = yes` | Line 2a = box-12 total; no box-8 members required |
| P5 | Mixed box-8 + box-12 aggregation | Line 2a = sum of both closed subtotals |
| P6 | Box 9 explicit null | Admissible |
| P7 | Box 9 explicit zero | Admissible |
| N1 | Missing box-9 companion authority | Hard block / admission rejection |
| N2 | Nonzero box 9 | Block without Form 6251 |
| N3 | Missing or open box-8 family under Path B | Line 2a blocks |
| P8 | Late member after closure; restored successor closure | Stale then restored publication |
| P9 | Correction of box-8 amount at same statement identity | Supersession; no double count |
| P10 | Switch Path A ↔ Path B | Displaces line 2a; exact pins for selected path |
| N4 | Form 1099-OID tax-exempt source present | Remaining scope fails |
| N5 | Premium adjustment present | Remaining scope fails |
| N6 | Excluded downstream consumer present | Downstream blocked; no universal informational claim |
| P11 | Line 2a changes; line 9 and taxable income unchanged | Reported-only semantics |
| R1 | Existing box-12, dividend, taxable-interest, Schedule B, Schedule D, carryover regressions | Unmodified fixtures pass |
| R2 | Form 8949 graph regressions if present on final base | Pass without behavior change |
| P12 | One canonical positive presentation golden | Value, citation, authority, reported-only explanation |
| N7 | Compact negative presentation mutations | Existing fail-loud / block / redact |

Share builders; avoid duplicating complete act logs or many large goldens.

## Tracks and review structure

### Track 0 — Paper boundary and contract checkpoint (Foreman-owned)

Record Gate-1 scores, paper instances, negatives, lifecycle traces, maps,
exact citations, composition alternative choice (A vs B), two-path pin table,
and ADR disposition. Stop at paper if it distinguishes the shape. **No rival
prototype** unless P3/P4 remain genuinely contested after paper.

### Track 1 — Integrated production build (one Builder)

After owner approval and Track 0, one integrated Builder implements family,
companion (including live install), composition succession, two-path
completeness, package/release/adoption graph, explanation, presentation
golden, and tests. Prefer reusing the recent box-12 Builder context if the
owner launches that role. If substrate cannot express the settled paper shape,
stop and return to the owner.

### Review gate — Integrated independent review (one Reviewer)

Author-independent Reviewer measures: family independence; box-9 live-path
companion; composition coextensiveness; Path A/B exact pins and non-leakage;
remaining scope honesty; reported-only semantics; package collisions; box-12
historical exclusivity; full evidence matrix. Prefer reusing the recent box-12
Reviewer context if practical. Report falsifiable `READY` or numbered findings.

### Repair and closeout

At most one bounded findings-only repair cycle. Second substantive defect or
scope expansion returns to the owner. Working charters and interim records
removed at final curation; this plan and the retrospective remain durable.

## Readiness and version-collision checkpoints

Before implementation, and immediately before final packaging / PR curation:

1. Fetch/prune origin; identify latest ratified line with the repository
   resolver (never a guessed filename).
2. Inventory published tax schemas, artifact-package schemas, packages,
   published registries, releases, adoptions, and presentation artifacts on
   that line and this branch.
3. Capture ignored ephemeral semantic ledger vs predecessor.
4. Rebase onto latest ratified line; rebuild from new predecessor; re-inventory.
5. Verify both upstream and milestone deltas; stop on unexplained member loss,
   version regression, reversed retirement, or semantic overlap.
6. Choose unused successor filenames only after rebasing; preserve every
   ratified file and manifest row byte-for-byte.
7. Focused package-surface regressions for box 12, Schedule B, Schedule D
   carryovers, and Form 8949 if present on the final base.

**Planning-base inventory is not a reservation.** Likely next unused tips
*today* are core **v18**, published **v13**, release **v11**, adoption
**v18**, but Form 8949 may consume those numbers first.

## Durable versus temporary artifacts

| Durable | Temporary (remove at closeout) |
| --- | --- |
| This plan | Working Builder/Reviewer charters |
| Track 0 paper record in plan/retrospective | Interim review drafts |
| Implementation content, tests, generator | Semantic ledger / dry-run notes |
| Additive package/registry/release/adoption | Branch-local briefing capsules |
| Phase-state, frontier, roadmap, retrospective | |

## Coverage-frontier updates (this plan)

Split Form **1099-INT box 8** into its own **selected** row. Leave as separate
future work (named block or candidate):

- Form 1099-OID tax-exempt stated interest / OID (boxes 2 / 11);
- unreported / non-form tax-exempt interest;
- tax-exempt bond-premium and acquisition-premium adjustments;
- nonzero box 9 / Form 6251 / AMT;
- excluded downstream consumers (taxable Social Security, etc.).

## Durable commit structure

1. `plan: select Form 1099-INT box 8 to line 2a` — this plan, planned phase
   state, roadmap selection, frontier split; **no implementation**.
2. `track-0: record box-8 and line-2a succession paper boundary` — after owner
   plan approval.
3. `track-1: implement bounded box-8 line-2a succession` — integrated build.
4. Provisional review/repair commits, folded before curation.
5. Closeout commit with retrospective, curated records, final state.

No schema, package, release, registry, adoption, or ADR number is reserved
before the rebase checkpoints.

## Fixtures, verification, economy, and data safety

Synthetic `demo.*` identities only. One canonical positive presentation golden;
compact negative mutations. Final focused set includes family/admission,
lifecycle, Path A/B completeness, composition, package/resolver, explanation,
presentation, box-12 regressions, interest/Schedule B/Schedule D regressions,
and `tests.test_schema_registry` when schemas or manifests change. Typed
changes run `python3 -m mypy`. Final checks: `git diff --check`, governance
lint, envelope scan, CI `verify`. Named positives enter through
`live_coordinate_run`.

No personal or real tax data in the branch, fixtures, review, chat, or output.

## Exit criteria

Track 0 paper settles P3/P4; integrated build implements the succession;
positive/negative matrix evidenced; box 9, OID, premium, excluded consumers,
missing declarations, stale closures, corrections, restoration, and path
switches fail honestly; line 9 and taxable income remain unchanged when line
2a changes; historical box-12 and related regressions pass; package/release/
registry/adoption resolve; historical files byte-identical; independent review
`READY` with at most one repair; CI green; owner merges the single curated
milestone PR.

## Owner decisions (recorded at Track 0)

Owner approved 2026-08-05; Track 0 recorded preferred shapes as settled:

1. Track 0 paper-first approach and Gate-1 scores above.
2. Preferred P3 Alternative A (composition citizen) vs B (rule-only successor).
3. Path A / Path B completeness shape and Path B exhaustion claim.
4. Single integrated Builder + single independent Reviewer economy.
5. Explicit non-reservation of package/schema versions pending rebase.
