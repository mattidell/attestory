<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098e-student-loan-interest-agi",
  "milestone_state": "track-4",
  "status": "Re-cut of milestone/f1098e-student-loan-interest-line21 (PR #169, owner-ruled completed design exploration). Cut from origin/main at 85b6a0f1. Track 0 settled: ten settlement questions answered, five of six adversarial closure artifacts PASS; integration surface PENDING by design (closes retroactively when Track 1-6 build the nine synthetic disposition-path models, matching the ssa-no-activity-applicability precedent). Foreman review corrected one version collision (rule-artifact v5 -> v6), a substrate bug in build_orientation_block.py (current_prompt's #anchor was ignored), and a missing SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE block test. Version claims on the local-only milestone-schema-ledger branch: attachment-rule v9, artifact-package v25, rule-artifact v6. Tracks 1-3 built and foreman-reviewed, full suite green. Known limitation carried to Track 6: multi-statement per-statement-witness disagreement is unmarshalled first-wins, untested. Track 4 dispatched.",
  "current_role": "Builder (Track 4 — Schedule 1 line-26 composition and attachment succession)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Tracks",
  "scope": [
    "settle Form 1098-E authority and identity (T0-1)",
    "settle component-level eligibility authority and the reported-interest boundary (T0-2, T0-3)",
    "settle the Student Loan Interest Deduction Worksheet as one rule citizen, including the multiply/divide expression-language addition (T0-4)",
    "settle MAGI completeness and confirm line 21 is excluded from its own base (T0-5)",
    "settle Schedule 1 Part II completeness and line 26 against the current 13-fact absence population (T0-6)",
    "settle Schedule 1 attachment disposition (T0-7)",
    "settle Form 1040 line 10 / 11a / 11b succession (T0-8)",
    "sequence the substrate repairs this design needs: multiply/divide, conditional_dependency_set adoption, path-dependency routing (T0-9)",
    "state the ADR budget and contract novelty (T0-10)",
    "produce all six Track 0 adversarial closure artifacts"
  ],
  "non_goals": [
    "no-rrb-or-foreign-social-benefit succession (the fourteenth migration candidate) -- still deferred",
    "any Schedule 1 Part I (income) change",
    "any change to rule.form1040-line15.v2 or the deduction spine",
    "implementation ahead of paper-rung Track 0 settlement of all ten questions"
  ],
  "deep_reads": {
    "paper": [
      "docs/roles/builder.md",
      "docs/governance/ontology.md#§2 — Claims, facts, findings",
      "docs/governance/ontology.md#§5 — Derivation machinery",
      "docs/governance/ontology.md#§7 — Supersession and lifecycle",
      "docs/adr/0025-expression-language-extensions.md#Decision",
      "docs/adr/0016-source-family-claim-and-composition.md#Decision",
      "docs/adr/0063-migration-artifact-direct-supersession-root.md#Decision",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Current state, re-verified at `85b6a0f1`",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Track 0 charter — settlement questions",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Version claims (schema-ledger, `milestone-schema-ledger` branch)",
      "packages/content/tax/2025/schedule1-adjustments-scope.bundle.json",
      "packages/content/tax/2025/schedule1-adjustments-scope.succession.json",
      "packages/content/tax/2025/rule.ss-benefits-worksheet.v2.json",
      "packages/derivation/evaluator.py",
      "packages/derivation/runner.py",
      "AGENTS.md#Data Safety Rules"
    ],
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Track 0 charter — settlement questions",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#T0-4 — Student Loan Interest Deduction Worksheet",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#T0-9 — Substrate repair sequencing",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Tracks",
      "packages/derivation/evaluator.py",
      "packages/schemas/derivation/rule-artifact.v4.schema.json",
      "docs/process/concurrent-work.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Objective",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Track 0 charter — settlement questions",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Track 0 adversarial closure",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Milestone: 2025 Form 1098-E Student-Loan Interest → Schedule 1 Lines 21/26 → Form 1040 Line 10 → AGI 11a/11b

Milestone key: `f1098e-student-loan-interest-agi`
Branch: `milestone/f1098e-student-loan-interest-agi`

## Provenance

This is a **re-cut**, not a continuation, of
`docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md`
(branch `milestone/f1098e-student-loan-interest-line21`, PR #169). That branch
stopped at design: the owner ruled it **completed design exploration**, not a
resumable charter, after Track 0c found `ss-benefits-scope` succession absent
from the substrate the design depended on. This plan inherits **only** that
branch's "Durable findings register" section verbatim-in-spirit — not the
Track 0/0a/0b/0c narrative, not its ten settlement items' prior answers, not
its proposed contracts. Every substrate claim below was re-verified against
`origin/main` at `85b6a0f1` (this branch's base), not trusted from the
register.

Disposition of PR #169: **argued for merge below, not decided here.**

## Objective

Compute 2025 Form 1098-E student-loan interest through Schedule 1 line 21,
Schedule 1 line 26 (total adjustments), Form 1040 line 10, and AGI on lines
11a and 11b, for the bounded class of returns the Track 0 charter below
settles. This is the first Engine Breadth route that puts a nonzero value on
Form 1040 line 10 and makes AGI differ from total income — every prior route
was income or itemized deduction.

## Current state, re-verified at `85b6a0f1`

**What changed since the register was written** (both cited facts corrected):

* **Cross-fact-type succession now exists.** ADR-0063 accepted
  `migration-artifact.v1` / `act-migration-adoption.v1` as a fourth direct
  supersession root (`schedule1-adjustments-scope.succession.json`,
  schema `migration-artifact.v1`). The thirteen shared Schedule 1 absence
  facts now carry Schedule-1-native ids under
  `tax.us.2025.schedule1-adjustments-scope.no-line{11,12,13,14,15,16,17,18,19,20,23,25}*`
  (`packages/content/tax/2025/schedule1-adjustments-scope.bundle.json`),
  succeeding their `ss-benefits-scope` predecessors. **Lines 21 and 22 were
  never in this population** — confirmed by reading the bundle and the
  succession pairs directly; there is no `no-line21` or `no-line22` fact
  anywhere in the repository. Schedule 1 Part II therefore currently has
  **twelve numbered-line absences plus one write-in absence (13 facts)**, and
  **no completeness declaration at all for lines 21, 22, 24a–24z (other than
  24z write-in), or the line-26 total**. This milestone is not slotting a
  fourteenth absence fact into an existing pattern — it is authoring the
  first *present* (non-absence) Schedule 1 Part II line and the first Part II
  total. T0-6 below must settle whether the other Part II lines' absence
  needs any restatement for line-26 completeness to be sound, or whether
  Part II completeness was never actually asserted and this milestone must
  say so explicitly rather than assume it.
* **The SSA 33-declaration burden is repaired**, but **not by migrating
  `no-rrb-or-foreign-social-benefit`.** `ssa-no-activity-applicability`
  (PR #173) collapsed the *worksheet-guard* dependency from 33 declarations
  to 1 (`docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md`
  T0-1, verdict "33 → 1"): the retained one is
  `tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit`, found
  **load-bearing** and recorded as a **fourteenth migration candidate**, not
  acted on by that milestone or by the fact-type-succession milestone.
  Current `docs/phase-state.md` still lists "no change to
  `no-rrb-or-foreign-social-benefit`" as unshipped. **This milestone does not
  touch it either** — see Non-goals. `ss-benefits-scope` remains at its base
  `v1`.

**What the register still gets right, re-verified directly:**

* No `multiply` or `divide` operator exists
  (`packages/derivation/evaluator.py`, `op ==` dispatch checked exhaustively
  — only `add`, `subtract`, `max`, `compare`, `all`, `any`, `not`, `choose`,
  `round`, `range_lookup`, `bracket_fold`, `require_closed`,
  `categorical_compare`, `category_literal`, `conditional_dependency_set`).
  The Student Loan Interest Deduction Worksheet (i1040gi p. 99) needs both
  for the phaseout ratio and its rounding.
* **`all` still short-circuits** (`evaluator.py:172-173`), so a component
  after the first `no` is never evaluated and never pinned.
  **`conditional_dependency_set` already exists as a shipped operator**
  (`evaluator.py:217-236`, the ADR-0038 shape, live in
  `rule.ss-benefits-worksheet.v2` today) — the repair for this milestone's
  eligibility gating is *using* that operator, not building a new one.
* **`requires` is still checked before evaluation**
  (`runner.py:482`, `is_eligible`), confirmed unchanged. Any route that is
  optional at the return level must be expressed as a path dependency a
  guard controls, never as a hard `requires` gated by a `when`.
* No rule, form-field, or bundle in the repository names Form 1098-E,
  Schedule 1 line 21, Schedule 1 line 26, or Form 1040 line 10. `git grep`
  for each of those identifiers returns only unrelated `schedule-d.line-21`
  matches (a Schedule D line, not Schedule 1). This is genuinely unbuilt
  territory — Track 0 is not reconciling with an existing citizen.
* `rule.form1040-line11.json` still publishes AGI as a bare `ref`
  passthrough of total income on a line number (`11`) the printed 2025 form
  does not have. `rule.form1040-line9.v7` still hard-requires
  `additional-income`, so there is still no "return with no Schedule 1" —
  line 10 has a computed authorized zero when Part II is empty, needing no
  new absence authority for that path specifically.
* The deduction spine (12e–15, `rule.form1040-line15.v2`) is unaffected;
  only the income side needs repair.

## Scope

1. Form 1098-E authority: identity, VOID handling, eligibility-component
   inventory (Track 0 T0-1/T0-2/T0-3).
2. `multiply` and `divide` evaluator operators, additively extending the
   expression language (Track 0 T0-9; a new ADR, not an ADR-0025 amendment).
3. The Student Loan Interest Deduction Worksheet as one rule citizen
   (Track 0 T0-4).
4. MAGI completeness for this route, reusing existing MAGI component
   vocabulary where a genuine claim match exists (Track 0 T0-5).
5. Schedule 1 Part II completeness including line 26 as the first Part II
   total (Track 0 T0-6).
6. Schedule 1 attachment disposition for line 21 (Track 0 T0-7).
7. Form 1040 succession: line 10 (new), 11a/11b (replacing the bare `line11`
   passthrough) (Track 0 T0-8).
8. Package, registry, release, explanation, and presentation for the new
   route.

## Non-goals

* `no-rrb-or-foreign-social-benefit` succession (the fourteenth migration
  candidate) — explicitly deferred by both prior milestones; still
  unselected.
* Any Schedule 1 Part I (income) change.
* Any change to `rule.form1040-line15.v2` or the deduction spine.
* General multi-loan MAGI phaseout edge cases beyond what i1040gi p. 99
  and Pub. 970 directly authorize.
* Retiring `ss-benefits-scope` v1 or any of its remaining (non-succeeded)
  declarations.

## Contracts expected (Track 0 confirms, refines, or replaces)

* **SLI-C1** — bounded Form 1098-E statement family, VOID-excluded, account
  number not an identity key.
* **SLI-C2** — component-level eligibility authority (no collapsed
  `qualified: yes`), gathered via `conditional_dependency_set`, not `all`.
* **SLI-C3** — reported-interest boundary: box 1 only; box 2 blocks per
  ADR-0016 §5 closure semantics (closure proves the statement set complete,
  never that the deductible-interest universe equals it).
* **SLI-C4** — the ordinary worksheet as one derived rule citizen.
* **SLI-C5** — MAGI component boundary, line 21 excluded from its own base,
  no re-pointing or re-versioning of `schedule1.line10-additional-income`.
* **SLI-C6** — Schedule 1 Part II completeness and line 26 as a real total,
  reconciled against the current 13-fact absence population (not a
  fourteenth entry in it).
* **SLI-C7** — Schedule 1 attachment content reuse, version claimed against
  the ledger, not against a number that may already be spent by a concurrent
  milestone.
* **SLI-C8** — Form 1040 line 10 / 11a / 11b succession, preserving
  `rule.form1040-line15.v2` unedited.
* **SLI-C9** — `multiply` / `divide` expression-language extension, its own
  ADR.
* **SLI-C10** — lifecycle, explanation, package, presentation for the new
  route end to end.

## Data safety

No personal document or personal data path is touched. All fixtures are
synthetic, matching existing Engine Breadth convention.

## Track 0 charter — settlement questions

Track 0 is paper-first. No implementation, schema, rule, package, registry,
attachment, or form-field version is written until Track 0 settles and passes
the adversarial closure gate below.

### T0-1 — Form 1098-E authority and identity (question)

Confirm the field inventory, VOID disposition, and identity keys against the
2025 Form 1098-E and its instructions, obtained fresh (the register notes the
source PDFs are untracked and must be re-obtained ephemerally per milestone —
confirm durable availability against ADR-0031's residency boundary or record
the same defect again). Confirm account number is recorded authority, not an
identity key, and that a lawful single-statement, multi-loan filing is
representable without a false cardinality assumption.

### T0-2 — Component-level eligibility authority (question)

Re-derive the eligibility-component inventory (the register found seventeen,
independently authorized, no collapsed conclusion) against fresh sources.
Classify each as universal (a `no` is an existential failure that blocks) or
a legal zero (an honest `not-claimed-as-dependent` reading that computes a
zero, not a block) — the register's B1/A1–A10 split is a hypothesis to
re-verify, not an inherited answer.

### T0-3 — Reported-interest boundary (question)

Settle box 1 vs. box 2 disposition and its closure argument under ADR-0016
§5, independent of the register's prior wording.

### T0-4 — Student Loan Interest Deduction Worksheet (question)

One rule citizen on the accepted worksheet pattern, i1040gi p. 99 line by
line. Settle the minimal `multiply`/`divide` expression-language addition
needed (schema shape, rounding-instruction placement — a precision floor on
the decimal, not the result) and the pin table for absence dispositions.

### T0-5 — MAGI completeness (question)

Settle the MAGI component boundary and confirm line 21 is provably excluded
from its own base (the register's DFS-over-symbol-graph argument depended on
Part II being purely additive — re-verify that premise still holds given the
succession that landed since). Settle reuse-vs-mint for the MAGI component
vocabulary against the claim-reuse proof standard in the adversarial closure
gate, not against apparent shape similarity.

### T0-6 — Schedule 1 Part II completeness and line 26 (question)

This is the item most changed by re-verification (see Current state above).
Settle: does asserting line-26 completeness require any statement about the
Part II lines that currently have no absence declaration (21, 22, 24a–24y),
or is completeness scoped only to the lines this milestone and its
predecessors jointly cover? Settle whether line 22 (reserved) needs any
disposition at all. Produce the completeness argument as one of the six
mandatory adversarial-closure artifacts, not as prose.

### T0-7 — Schedule 1 attachment disposition (question)

Settle attachment reuse. **Do not assume `attachment-rule.v4`** — two
concurrent milestones are claiming `attachment-rule.v7` and `v8` on the
ledger (see Version claims below); confirm which published version this
route's needs actually match, and claim a new version rather than colliding.

### T0-8 — Form 1040 succession: lines 10, 11a, 11b (question)

Settle the `rule.form1040-line11` → line 10/11a/11b succession: one AGI
symbol vs. two form-field citizens, whether existing consumers of the
current line-11 symbol are preserved by membership or require their own
succession, and confirm no re-pin or re-version of
`rule.form1040-line15.v2`.

### T0-9 — Substrate repair sequencing (question)

Name, in commit order, every substrate change this milestone's design
requires: the `multiply`/`divide` operators (with their own ADR — this is a
new additive contract, not an ADR-0025 amendment, so it is not a stop
condition); the specific rule sites that must use
`conditional_dependency_set` instead of `all` for eligibility gathering; and
any route in this design that must use a path dependency rather than a
`when`-guarded `requires` because it is optional at the return level.

### T0-10 — Contract novelty and ADR budget (question)

State how many new ADRs this milestone needs (expect at least two: one for
the expression-language extension, one for whichever of T0-6/T0-7/T0-8 turns
on genuinely new composition rather than reuse) and what each decides. The
next unclaimed ADR number as of this reading is **0067** — 0064–0066 are
claimed on other open, unmerged branches (`declarative-validation-substrate-f8949`
claims 0066; two others upstream of that are claimed on branches not part of
this thread's concurrency set). Re-verify the true next-free number
immediately before drafting any ADR text, not from this note.

## Version claims (schema-ledger, `milestone-schema-ledger` branch)

Re-verified against `origin/milestone-schema-ledger` at the point of filing
(see report below). This milestone's Schedule 1 composition work starts at:

* `attachment-rule` **v9** (v7 and v8 are both claimed — v7 by
  `f8949-noncovered-basis`, v8 by `declarative-validation-substrate-f8949`).
* `artifact-package` **v25** (v23 published/merged, v24 claimed by
  `declarative-validation-substrate-f8949`).
* A new schema family for `migration-artifact` is not needed — T0-6 found
  lines 21/22 were never in the predecessor absence population, so there is
  nothing to migrate.
* `rule-artifact` **v6** for the additive `multiply`/`divide` expr variants
  (T0-4/T0-9/T0-10). **Foreman correction on review:** Track 0's own
  settlement text twice named `rule-artifact.v5` for this — that version is
  already claimed (as `publish`, not merely `propose`) by
  `declarative-validation-substrate-f8949` on the local ledger
  (`schema-ledger/events/declarative-validation-substrate-f8949/20260815T183617Z-rule-artifact-d47efc.json`,
  the closed ADR-0066 `accounts_for` vocabulary — an unrelated, incompatible
  shape). v5 would have collided the moment that milestone merges. Corrected
  to v6 throughout this document and reserved on the local ledger.
* Publication counters (core package, published-packages, release) are
  **not** covered by the ledger's tracked event kinds today. Current
  published state is core **v31** / published-packages **v26** / release
  **v24** (confirmed from `docs/phase-state.md` at `85b6a0f1`). This
  milestone must claim its own event kind on the ledger branch for these
  counters before a builder writes them, per the standing instruction — no
  event filed yet because Track 0 has not started and the counters this
  milestone will need are not yet known.

Track 0 must file its schema-ledger events as soon as it knows what it
needs, not at build time, per the standing instruction.

## Track 0 settlement (performed at `b8e690295f4ca8d1ccb5fa5493807dd86e1ab8f9`)

Sources obtained ephemerally (never committed, per `AGENTS.md#Data Safety
Rules` and ADR-0031) on 2026-08-15 directly from `irs.gov/pub/irs-pdf/`:
`f1040.pdf` (2025 Form 1040), `f1098e.pdf` (2025 Form 1098-E, both copies and
borrower instructions), `i1098.pdf` (combined 2025 Instructions for Forms
1098, 1098-E, 1098-T — the separate `i1098e.pdf` URL now 404s and has been
folded into the combined instructions since 2020, confirmed by fetching that
URL and observing the IRS 404 page's `isHistorical`/`historical-date
2020-11-17` metadata), `i1040gi.pdf` (2025 Instructions for Form 1040,
pages 90–105 for the Student Loan Interest Deduction Worksheet), `p970.pdf`
(2025 Pub. 970, Chapter 4), `f1040s1.pdf` (2025 Schedule 1). All local copies
were deleted from the scratchpad at the end of this session; none were
added, staged, or referenced by path outside this document. Every claim below
cites the specific page/line of one of these.

### T0-1 — Form 1098-E authority and identity

**Durable availability confirmed, register defect not reproduced.** All
source PDFs above were reachable directly from `irs.gov/pub/irs-pdf/`
except `i1098e.pdf`, which the IRS retired in 2020 in favor of a combined
`i1098.pdf` (1098/1098-E/1098-T). This is a naming change, not an
availability defect; `ADR-0031`'s residency boundary (documents obtained
ephemerally per milestone, never committed) is unaffected — future
milestones must fetch `i1098.pdf`, not `i1098e.pdf`.

**Field inventory** (`f1098e.pdf`, Copy A/Copy B, RECIPIENT'S/LENDER'S
name block): a `VOID` checkbox and a `CORRECTED` checkbox at the top of the
statement; RECIPIENT'S/LENDER'S name, address, TIN; BORROWER'S name,
address, TIN; **Account number** ("see instructions"); **Box 1** — "Student
loan interest received by lender" (the sole reportable dollar amount); **Box
2** — a checkbox, "Check if box 1 does not include loan origination fees
and/or capitalized interest, and the loan was made before September 1,
2004." There is no box 3 or higher on this form.

**VOID disposition.** A `VOID`-checked copy is the issuer's own statement
that no report was made; per general information-return convention (already
used identically for the `f1099g` family, `packages/content/tax/2025/
f1099g-box1.bundle.json` — a corrected copy *supersedes* its prior finding,
never a second member) a VOID'd 1098-E is **not admitted to the statement
family at all** — it is not a member, not a correction, not evidence of
anything. This settles: VOID copies are excluded at admission, not filtered
post hoc, mirroring how `CORRECTED` copies are ordinary supersession of a
prior finding for the same statement identity.

**Identity keys.** Per Ontology §2 ("identity keys may reference other
workspace citizens... but never a document"), the statement's identity must
be an entity, not a file. Mirroring `tax.us.2025.f1099g.box1-unemployment`'s
precedent exactly (`payer` entity + `statement` entity + `tax-year` literal),
Form 1098-E's member fact type is keyed on a `lender` entity, a `statement`
entity, and the `tax-year` literal. **Account number is explicitly not an
identity key** — the instructions describe it only as "an account or other
unique number the lender assigned to distinguish your account," recorded
authority the lender chose to disclose, never load-bearing for statement
identity (a lender who omits it, as many will, cannot break identity). This
settles SLI-C1's "account number not an identity key" clause directly.

**Multi-loan, multi-statement cardinality.** The instructions state a lender
must furnish this statement when it "receives interest payments of $600 or
more during the year on one or more qualified student loans" (`f1098e.pdf`
p.1, borrower instructions) — one statement can already aggregate several
loans from the same lender, and a borrower with loans from different lenders
receives several statements. The family/member pattern (mirroring
`tax.us.2025.f1099g.1`) is `collect`-over-members by construction — it
imposes no cardinality assumption, lawfully representing any number of
statements from any number of lenders. SLI-C1 is fully settled.

### T0-2 — Component-level eligibility authority

Re-derived from `p970.txt` "Can You Claim the Deduction?" (p.33),
"Qualified Student Loan" / "Related person" / "Qualified employer plan"
(pp.30–32), "No Double Benefit Allowed" (p.32–33), and `i1040gi.pdf`
p.98 ("You can take this deduction only if all of the following apply"),
independent of the register's seventeen-item inventory. This settlement
finds **twelve** independently authorized components — ten universal
(a `no`/violation is an existential failure that blocks) and two legal-zero
(an honest negative answer computes a definite $0, not a block) — not
seventeen. The count differs because several of the register's presumed
separate items (qualified higher-education expenses, eligible-student
enrollment, reasonable-period-of-time timing) are not independently
assertable facts on this system's bounded route: they are constitutive of
what "qualified student loan" *means*, and Pub. 970 gives no per-return
signal distinguishing them from one another — this settlement folds them
into one contributed absence witness rather than inventing three
unfalsifiable sub-facts, the same modeling choice already used for
`no-non-qualified-loan-component`-style witnesses elsewhere in this
codebase's box-4-style "authority witness, not a composed amount" pattern
(`f1099g-box1.bundle.json`, `box4-federal-withholding-authority`).

**Universal (blocks on `no`/violation), all minted new for this route,
scoped to SLI, never reused from `ss-benefits-scope`:**

1. `filing_status` ≠ married_filing_separately (`categorical_compare`
   against the existing `tax.us.2025.filing-status` fact type, no new
   vocabulary — Pub. 970 p.33: "Your filing status is any filing status
   except married filing separately").
2. No Form 2555 (foreign earned income exclusion) filed (`i1040gi.pdf`
   p.98, "Exception. Use Pub. 970 instead...if you file Form 2555").
3. No Form 4563 (bona fide Samoa resident exclusion) filed (same
   Exception clause).
4. No income excluded as a bona fide resident of Puerto Rico (same
   Exception clause).
5. Per-statement: no related-person loan interest included in the box-1
   figure (Pub. 970 p.31, "Related person").
6. Per-statement: no qualified-employer-plan loan interest included
   (Pub. 970 p.31, "Qualified employer plan").
7. Per-statement: no non-qualified-loan component included — collapses
   student/expense/timing qualification (Pub. 970 pp.30–31, "Qualified
   Student Loan," "Qualified Education Expenses," "Reasonable period of
   time").
8. Per-statement: box 2 not checked (settled fully under T0-3 below —
   a checked box 2 is a hard route block, not a silent narrowing).
9. No employer-paid interest under an educational assistance program
   (post-3/27/2020) included in the box-1 figure (Pub. 970 p.33, "No
   Double Benefit Allowed").
10. No QTP (qualified tuition program) distribution-earnings amount used
    to pay this interest (Pub. 970 p.33, same section).

**Legal zero (a `no` computes a definite $0, not a block):**

11. Claimed as a dependent by another taxpayer — Pub. 970 p.33, Example 2:
    "neither you nor your parents may deduct the student loan interest."
    A `yes` here is not missing information; it is the law's own zero.
12. Legally obligated to pay interest on the loan — Pub. 970 p.33: only the
    person legally obligated may deduct; a `no` here is likewise a
    definite zero for this filer, not a block (someone else, not this
    return, may deduct it — irrelevant to this return's computation).
    **Scope, settled at Track 2 build time:** filer-level (tax-year-only
    key), paired with component 11 rather than per-statement. A per-loan
    reading is textually plausible too (a cosigned loan could have a
    different obligor per loan), but this route already collapses several
    Pub. 970 sub-questions the codebase has no per-return signal to
    distinguish (component 7); filer-level keeps this component at the
    same granularity as its legal-zero sibling and matches this milestone's
    bounded-class posture. Revisit if a later milestone needs per-loan
    obligation to be distinguishable.

This resolves T0-2's re-derivation demand: the register's B1/A1–A10 split
is confirmed as a real universal/legal-zero distinction in the law, but its
count and boundary are re-derived, not inherited.

### T0-3 — Reported-interest boundary

**Box 1 only; box 2 is a hard route block, not a silent exclusion.**
Box 1 is the sole reportable dollar figure. Box 2, when checked, states that
"box 1 does not include loan origination fees and/or capitalized interest"
for a pre-9/1/2004 loan — meaning box 1 is known-incomplete for that
statement, and Pub. 970 (p.32, "Loan origination fee") directs the borrower
to "use any reasonable method to allocate the loan origination fees over the
term of the loan," an out-of-scope manual computation this milestone's
worksheet-line arithmetic cannot honestly perform. Under ADR-0016 §5 ("box-1
closure ... does not authorize a broader claim"), a system that silently
dropped box-2-checked statements from the family would substitute a
narrower family (the box-1-clean subset) for the return's true, broader
"all qualified student loan interest" universe — exactly the substitution
ADR-0016 forbids. A system that silently summed the incomplete box-1 figure
as if it were the whole interest paid would overstate authority the
statement itself disclaims. Neither silent path is honest, so this
settlement treats **any admitted statement with box 2 checked as a hard
route block** (`BLOCK_INVALID`-style, per-statement, propagating to the
whole route since the worksheet's total interest-paid figure would be
provably incomplete) — mirroring `f1099g-box1.bundle.json`'s
`box4-federal-withholding-authority` companion-witness pattern, where only
the admissible value (`box 2 unchecked`) proceeds and any other value is a
hard block, never a silent net. Returns with a box-2-checked statement fall
outside this milestone's bounded class and must use Pub. 970's manual
computation, consistent with the Non-goals clause on "edge cases beyond
what i1040gi p.99 and Pub. 970 directly authorize." SLI-C3 is settled as
stated in the charter, with the box-2 mechanism now concrete.

### T0-4 — Student Loan Interest Deduction Worksheet

One rule citizen, `i1040gi.pdf` p.99 line-by-line (worksheet lines 1–9,
verified against the extracted text):

1. Total interest paid (capped at $2,500) — `collect` over the closed
   Form 1098-E box-1 family, summed, then `min`-folded against the $2,500
   cap (`max`/`compare`/`choose`, no new op needed — the existing
   vocabulary already expresses a cap).
2. Amount from Form 1040 line 9 (total income) — `ref`.
3. Total of Schedule 1 lines 11–20, 23, and 25 — `add` over the same
   symbols `rule.schedule1-line10`'s sibling Part II producers publish
   (settled fully under T0-6; **excludes line 21 itself and line 22**,
   confirming the register's premise that line 21 does not depend on its
   own base — verified directly from the worksheet text, not assumed).
4. Line 2 minus line 3 (MAGI for this route) — `subtract`.
5. Threshold by filing status: $85,000 (single/HOH/QSS) or $170,000
   (MFJ) — `bracket_fold`/`choose` over `filing_status`, MFS excluded at
   eligibility (component 1 above) so no third branch is needed.
6. Line 4 minus line 5, floored at 0 if line 4 ≤ line 5 — `max`/`subtract`.
7. Line 6 divided by $15,000 ($30,000 if MFJ), **rounded to at least
   three decimal places**, capped at 1.000 — the new `divide` op (see
   T0-9), composed with the existing `max`/`compare`/`choose` cap
   idiom exactly as line 1's $2,500 cap is expressed.
8. Line 1 times line 7 — the new `multiply` op.
9. Line 1 minus line 8 — `subtract`. Published to Schedule 1 line 21.

**`multiply`/`divide` schema shape** (settled at the design level; exact
JSON Schema text is Track 1's job): `multiply` takes `left`/`right` like
`subtract`, no new fields. `divide` takes `left`/`right` plus a
`min_decimal_places` integer and a `rounding` mode drawn from the existing
`_ROUND_MODES` vocabulary (`half_up`, `half_even`, `down`, `up`) — the
worksheet's "rounded to at least three places" is a **floor on the ratio's
own decimal precision**, evaluated once, immediately after division, and is
categorically distinct from the existing `round` op's whole-dollar
`rounding.convention` unit, which continues to govern only the final
Schedule 1 line-21 dollar amount unchanged. `divide` blocks
`DEPENDENCY_INVALID` on a zero divisor (defensive; this route's divisor is
always a fixed nonzero parameter, so the guard is never live here, but the
op must not silently produce `Infinity` or crash for any future consumer).
This is additive: no existing `rule-artifact.v4` expr variant changes shape,
satisfying stop condition 4 (settled fully under T0-9/T0-10).

**Pin table for absence dispositions:** each of the twelve T0-2 components
pins as an `input` role exactly like `rule.ss-benefits-worksheet.v2`'s
twenty-two-conjunct pattern; the six components that are per-statement
witnesses (5–10 above, corrected from a miscounted "seven" on first
settlement — Track 2 built against the exact range, not the prose count)
pin against the closed Form 1098-E family alongside the box-1 member pins,
never against an individual statement in isolation — a violation on any
admitted statement blocks the whole route, consistent with T0-3's box-2
disposition.

### T0-5 — MAGI completeness

**Reuse-vs-mint, decided against reuse for every candidate.** The only
existing vocabulary shaped like this route's exception-filer gates is
`ss-benefits-scope.no-form-2555` / `no-form-4563` /
`no-puerto-rico-or-samoa-income`. Applying the claim-reuse proof standard
(artifact 4, below) to each: same real-world proposition (did the taxpayer
file Form 2555?) — arguably yes; **same declared authority scope** — no.
Each `ss-benefits-scope` title is explicit: "...for the bounded standard
Social Security Benefits Worksheet claim." That scope clause is the
declared authority, not a decoration, and ADR-0016 decision 2 forbids an
"apparently narrow title" from broadening a source declaration — the
inverse failure mode is just as real: a declaration scoped to one worksheet
cannot be silently *reused* to authorize a different worksheet's gate,
even where the real-world question coincides, because the two worksheets'
Pub. 970/i1040gi exception clauses are legally independent (one could
change without the other). This settlement **mints new, SLI-scoped**
fact types for components 2–4 in T0-2, never reusing the `ss-benefits-scope`
ids. No other MAGI component has a shape-similar existing declaration, so
the mint-vs-reuse question does not arise elsewhere on this route.

**Line 21 excluded from its own base — premise re-verified, not assumed.**
The register's DFS-over-symbol-graph argument depended on Part II being
purely additive. Re-verified directly against `f1040s1.pdf` p.2 line 26
("Add lines 11 through 23 and 25") and `i1040gi.pdf` p.99 worksheet line 3
("the total of the amounts from Schedule 1, lines 11 through 20, and 23 and
25"): **line 21 is never a term in worksheet line 3, and line 3 explicitly
enumerates every other Part II line by number, stopping short of 21.** The
"purely additive" premise still holds for the *lines contributing to line
3's MAGI adjustment*, but line 26 (the actual Schedule 1 total) is a
different sum that **does** include line 21 — the two totals (worksheet
line 3, Schedule 1 line 26) are not the same aggregate and must not be
conflated. MAGI's own base is therefore provably acyclic: line 21 depends
on line 3, which never references line 21, so no cycle exists regardless
of what line 26 later sums. SLI-C5 is settled: no re-pointing or
re-versioning of `schedule1.line10-additional-income` (Part I; untouched
by this milestone) is needed or performed.

### T0-6 — Schedule 1 Part II completeness and line 26

**`f1040s1.pdf` p.2, line 26: "Add lines 11 through 23 and 25."** Reading
the printed lines 11–25 directly: 11 (educator expenses), 12 (reservist/
performing-artist/fee-basis expenses), 13 (HSA), 14 (Armed Forces moving),
15 (deductible SE tax), 16 (SE retirement plans), 17 (SE health insurance),
18 (early-withdrawal penalty), 19 (alimony paid), 20 (IRA deduction), **21
(student loan interest deduction — this milestone)**, **22 ("Reserved for
future use" — no entry box on the printed form at all; `i1040gi.pdf` p.99,
"Line 22 has been reserved for future use," confirmed by both the form
image and the instructions, has no line of its own worth of guidance
beyond that one sentence)**, 23 (Archer MSA), 24a–24z (itemized other
adjustments, summed to line 25), 25 (total other adjustments).

**Settlement: line-26 completeness needs no new statement about lines
22, 24a–24y, or the write-in.** Line 22 is not a taxpayer question — it is
a structurally fixed $0 by the form's own design (no box exists to enter
anything), so no absence fact, no legal-zero component, and no
`requires` entry is needed for it; a rule that sums the twelve numbered
lines plus line 21 plus line 25 already equals line 26 exactly, because
line 22 contributes nothing to add. This is not "scoping completeness
narrower than the true universe" (the ADR-0016 §5 failure mode) — it is a
provable zero from the form's own printed structure, the same status this
codebase already gives to `tax.us.2025.schedule1-adjustments-scope.
no-line24z-writein` for the 24z write-in (already migrated,
`schedule1-adjustments-scope.succession.json`) and the twelve other
already-succeeded absences, none of which this milestone touches or needs
to restate. **Line 26 completeness is therefore exactly**: the twelve
existing Schedule-1-native absence facts (11,12,13,14,15,16,17,18,19,20,
23,25 — the 25 absence already subsuming the 24a–24z detail through its
own `no-line25-other-adjustments` and `no-line24z-writein` pair) **plus**
this milestone's line 21 (a genuinely computed, present value, never an
absence) **plus** line 22's structural zero, requiring no fact at all.

**This is a new composition claim, not a fourteenth entry in the
existing 13-fact absence population** — the charter's own framing is
correct and this settlement affirms it rather than reinterpreting the
Ontology: mixing twelve *absent* lines, one *present* line, and one
*structurally fixed* line into a single total's completeness argument is
new work at the ADR-0016 layer (that ADR's decision 4 authorizes a broader
result consuming a subtotal "when the required universe is identical or an
explicit composition is established as coextensive" — it does not itself
state what coextensive means for a total that is *not* uniformly
absence-shaped). This settlement composes ADR-0016's existing doctrine
rather than reading new meaning into the Ontology, but states plainly that
the composition argument above needs its own small ADR to be citable
authority rather than unreviewed prose (settled fully under T0-10) — this
is the live risk the charter's stop condition names, and this settlement
resolves it by routing through a new, additive ADR rather than either
stopping for the owner or improvising doctrine.

### T0-7 — Schedule 1 attachment disposition

**Do not reuse `attachment-rule.v4` as a second producer of
`tax.us.2025.schedule1.disposition`.** `rule.attachment.schedule-1`
(schema `attachment-rule.v4`) already publishes that single symbol, gated
on `requirement.subtotals` under an "any subtotal over threshold" test
(`packages/derivation/runner.py:812-820`) — but its only listed subtotal is
Part I's `tax.us.2025.unemployment.box1-subtotal`, and its own title states
"Part II adjustments are out of scope." Adding a second rule that also
`publishes: tax.us.2025.schedule1.disposition` would collide under the
engine's ordinary single-producer-per-symbol conflict semantics
(`runner.py:521-528`, `"inapplicable"` on collision) — exactly the kind of
integration-surface hazard artifact 6 below exists to catch.

**Settlement: a new rule *version* of `rule.attachment.schedule-1`**,
adding the SLI worksheet's published line-21 amount as a **second entry**
in `requirement.subtotals` (the existing grammar already supports a list;
the "any … over threshold" semantics at `runner.py:815-820` already do
exactly what is needed — attach when Part I unemployment is nonzero *or*
Part II student-loan interest is nonzero, with no new op or field), and
adding one new `itemizations` part for "Line 21: Student Loan Interest
Deduction" tying out to the closed Form 1098-E box-1 family the same way
the existing Part I itemization ties out to the closed Form 1099-G box-1
family. This is the same rule identity succeeding forward (mirroring every
other line rule's version history in this codebase, e.g.
`rule.form1040-line9.v1`→`v7`), not a new attachment schema shape — the
existing `attachment-rule.v4` grammar already expresses everything this
route needs. Per the charter's pre-filed version claim, this rule version
is claimed against **`attachment-rule` v9** (not v4, and not the
concurrently-claimed v7/v8, which belong to unrelated unmerged milestones
this thread has no visibility into and must not collide with). SLI-C7 is
settled: reuse by rule succession within the existing schema shape, new
version claimed against the ledger, no collision.

### T0-8 — Form 1040 succession: lines 10, 11a, 11b

**`f1040.pdf` p.1 confirms the charter's "line 10/11a/11b" framing is the
real 2025 form, not a drafting error.** Line 10: "Adjustments to income
from Schedule 1, line 26." Line 11a: "Subtract line 10 from line 9. This is
your adjusted gross income." Line 11b (top of p.2): "Amount from line 11a
(adjusted gross income)." The 2025 form genuinely splits AGI into a
computed line (11a) and a carried-forward line (11b) that the deduction
spine (line 12e onward) reads — apparently to stage the new Schedule 1-A
senior/tips/overtime deductions cleanly behind a named AGI carry-forward.

**Settlement: one AGI symbol, `tax.us.2025.income.agi`, unchanged; two
form-field citizens.** `rule.form1040-line15.v2` requires
`tax.us.2025.income.agi` directly (`requires: ["tax.us.2025.income.agi",
"tax.us.2025.deductions.line-14"]`) — SLI-C8 and the Non-goals both forbid
touching that rule. Because line 11b's own definition on the printed form
*is* "the amount from line 11a" (an identical value, not an independent
computation), no second symbol is needed: **both** `form1040.line-11a` and
`form1040.line-11b` form-field citizens bind to the same symbol,
`tax.us.2025.income.agi`. The one substantive change is the *producer* of
that symbol: a new rule version replacing the bare passthrough of
`tax.us.2025.income.total-income` in the current `rule.form1040-line11.json`
(v1) with the corrected formula, total income minus Schedule 1 line 26
(`subtract`, requiring `tax.us.2025.income.total-income` and
`tax.us.2025.schedule1.line26-total-adjustments`). This is **ordinary rule
succession within a package version bump** — the same mechanism already
used for every other line in this codebase (`rule.form1040-line9.v1`
through `v7`, `rule.form1040-line2b.v1` through `v4`) — never the
migration-artifact machinery of ADR-0063, because `income.agi` is a
*derived* symbol with no standing findings of its own to retire: when the
producing rule changes in a new package version, the existing derivation
edge (Ontology §7) displaces and republishes automatically. Every existing
consumer of `tax.us.2025.income.agi` (today, only `rule.form1040-line15.v2`)
is preserved by symbol-name membership, requiring no succession of its own.
SLI-C8 is fully settled: `rule.form1040-line15.v2` is not touched, re-pinned,
or re-versioned.

### T0-9 — Substrate repair sequencing

In commit order:

1. **`multiply`/`divide` operators** (T0-4/T0-10): additive evaluator
   dispatch entries in `packages/derivation/evaluator.py` (new `if op ==
   "multiply"` / `"divide"` branches beside the existing `add`/`subtract`),
   and an additive `rule-artifact.v6` schema (the two new expr variants
   appended to the closed `$defs/expr` `oneOf` list in
   `packages/schemas/derivation/rule-artifact.v4.schema.json`'s successor —
   v4's published bytes are never edited, satisfying stop condition 4).
   Own ADR (T0-10).
2. **`conditional_dependency_set` for eligibility gathering**: this
   milestone's own new SLI worksheet rule must use it for the ten
   universal T0-2 components exactly as `rule.ss-benefits-worksheet.v2`
   already does for its twenty-two Schedule-1-adjacent conjuncts — never
   `all`, because `all` short-circuits (`evaluator.py:172-173`) and would
   silently fail to report every absent component at once on a short
   return. No other existing rule site in this codebase needs retrofitting
   for this milestone's scope (Non-goals excludes touching unrelated
   routes); `conditional_dependency_set` is adopted here, not built.
3. **Schedule 1 attachment rule succession** (T0-7): the new
   `rule.attachment.schedule-1` version, `attachment-rule.v9`.
4. **Form 1040 line 10/11a/11b rule citizens** (T0-8): the new
   `rule.form1040-line10` (Schedule 1 line-26 passthrough), the corrected
   `rule.form1040-line11a`/`-11b` succession, in a new
   `package.core-calculations.v32`.
5. **Path dependency vs. `requires`-under-`when`**: this route is optional
   at the return level (a taxpayer with no Form 1098-E has a genuine,
   computed $0 on Schedule 1 line 21, not a blocked return) — exactly the
   shape `rule.schedule1-line10` already handles for Part I via
   `require_closed` plus an `all`-guarded value expression, never a hard
   `requires` gated by a `when`. The new Part II line-21 rule must follow
   the same pattern: `require_closed` on the Form 1098-E family
   unconditionally (sequencing, matching the SS-worksheet precedent's
   reasoning in T0-9 of that rule's own notes), with the twelve T0-2
   eligibility components read via `conditional_dependency_set` conditioned
   on `count > 0`, never via a hard `requires` that would make a
   loan-free return ineligible rather than zero.

### T0-10 — Contract novelty and ADR budget

**Two new ADRs, not the charter's provisional "at least two" left
unconfirmed — this settlement confirms exactly two, and rules out a
third.** T0-1/T0-3 (Form 1098-E family/closure) are ordinary applications
of already-ratified ADR-0016 decisions 1–4, exactly as
`tax.us.2025.f1099g.1` already applies them — no new ADR. T0-8 (line
10/11a/11b) is ordinary rule succession within a package version bump, the
same mechanism used throughout this codebase — no new ADR, and specifically
not ADR-0063's migration-artifact root, because `income.agi` carries no
standing findings to retire. The two genuine new-composition items:

1. **Expression-language extension**: `multiply`/`divide`, `rule-artifact
   .v6`, its own additive ADR (not an ADR-0025 amendment — confirmed by
   reading ADR-0025's decision list end to end: it ratifies declared
   optional defaults and categorical comparison, and says nothing about
   arithmetic operators; adding `multiply`/`divide` amends nothing it
   decided).
2. **Schedule 1 Part II completeness and line-26 composition** (T0-6): a
   short ADR stating the coextensivity argument — the union of the twelve
   Schedule-1-native absence facts, this milestone's genuinely computed
   line 21, and line 22's form-structural zero is exactly Schedule 1 line
   26's required universe, citing ADR-0016 decision 4 as the doctrine it
   applies to a mixed absent/present/structural-zero total for the first
   time in this codebase. This keeps the settlement inside "compose an
   existing mechanism" rather than the owner-stop the charter flags for
   an Ontology-turning finding.

**ADR numbering**: the charter's provisional next-free number (0067) is
confirmed unusable as a fixed anchor — direct inspection of concurrent
unmerged branches (`milestone/declarative-validation-substrate-f8949` at
0066, `milestone/f8949-noncovered-basis-lines2-9` at its own,
conflicting, locally-numbered 0063–0065) shows numbering is a live,
branch-local moving target, exactly as the charter warned. This settlement
does not lock ADR numbers; Track 1 must re-verify the true next-free
number against `main` immediately before drafting either ADR, per the
charter's own instruction.

## Track 0 adversarial closure artifacts

### 1. Authority-lifecycle table

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `tax.us.2025.f1098e.box1-interest` (new) | Interest received by a lender on one or more qualified student loans, as reported in box 1 of one logical Form 1098-E statement | Statement (lender + statement entity + tax-year); never document-keyed | The statement's own admission (VOID-excluded, box-2-clean) | A `CORRECTED` copy of the same logical statement (ordinary supersession); statement-identity-key entity superseded (individuation edge) |
| `tax.us.2025.f1098e.1.source-closure` (new) | User attestation that every furnished 1098-E box-1 amount is recorded as of the keyed membership horizon | Return, keyed on the family-membership horizon (ADR-0017 pattern) | The horizon current at attestation | A later membership transition (a new statement admitted) displaces the closure through horizon succession; re-attestation required |
| Ten universal T0-2 components (new, e.g. `no-related-person-loan-interest`, `no-qualified-employer-plan-loan-interest`, `no-non-qualified-loan-component`, `box2-not-checked`, `no-form-2555`/`no-form-4563`/`no-puerto-rico-income` SLI-scoped, `no-employer-educational-assistance-interest`, `no-qtp-earnings-used`) | Named excluded circumstance is absent from this return's SLI claim | Return, scoped explicitly to the SLI worksheet (never the SS-worksheet's identically-shaped but differently-scoped ids) | Nothing upstream; directly asserted | A later, corrected assertion of the same fact (ordinary correction, free supersession policy) |
| Two legal-zero T0-2 components (new: `claimed-as-dependent-by-another`, `legally-obligated-to-pay-interest`) | A definite $0 SLI deduction condition, not missing information | Return | Nothing upstream; directly asserted | A later, corrected assertion of the same fact |
| `filing_status` (existing, reused) | The return's filing status | Return | Nothing upstream; directly asserted | A later corrected assertion |
| `rounding.convention` (existing, reused) | The project's whole-dollar rounding convention | Global/adoption-scoped | Adoption | A new adoption |
| Twelve Schedule-1-native Part II absence facts, lines 11–20/23/25 (existing, reused unchanged — `schedule1-adjustments-scope.bundle.json`) | Named Part II adjustment class is absent for 2025 | Return, Schedule-1-native (ADR-0063 succession, not SS-worksheet-scoped) | Migration adoption (`schedule1-adjustments-scope.succession.json`) as their supersession root | A later corrected assertion; a further migration retiring these ids (none contemplated) |
| `tax.us.2025.schedule1.line21-sli-deduction` (new, present value) | The computed Student Loan Interest Deduction for this return | Return; derived, pinning the worksheet's nine lines and all twelve T0-2 components | The SLI worksheet rule and everything it requires | Any pinned input's supersession (derivation edge) |
| `tax.us.2025.schedule1.line26-total-adjustments` (new aggregate) | Schedule 1 Part II total, the sum of lines 11–23 and 25 | Return; composed from the twelve absence facts (each contributing $0), line 21 (computed), and line 22 (structural $0, no fact) | The twelve absence facts' currency plus line 21's own derivation | Any of the twelve absence facts' supersession, or line 21's own displacement (derivation edge cascade) |
| `tax.us.2025.income.agi` (existing symbol, new producer) | Adjusted gross income | Return; unchanged meaning, unchanged symbol name | `tax.us.2025.income.total-income`, `tax.us.2025.schedule1.line26-total-adjustments` | Either input's supersession (derivation edge); the producing rule's own version change (ordinary rule succession, not a migration root) |

Storage identity is not authority scope, confirmed directly: every SLI
component above is keyed on the literal `{tax-year: 2025}` exactly like the
`ss-benefits-scope` originals were before ADR-0063 — the tax-year key alone
does not establish tax-year-only lifecycle; each component's true scope is
the SLI worksheet claim it was minted for, stated in its title, and its
true invalidating event is a corrected assertion or (for the twelve reused
absence facts) the migration root that already governs them.

### 2. Empty/nonempty authority matrix

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty (no Form 1098-E statements) | `f1098e.1.source-closure` attested true, zero current members | All ten universal components trivially satisfiable (nothing to violate); two legal-zero components still independently assertable | Line 21 computed **$0** (closed-empty box-1 subtotal is $0, worksheet line 1 is $0, line 9 is $0 regardless of MAGI) — an explicit computed zero, never a block, matching SLI-C1/C4's contract | Line 26 total unaffected in shape (still sums the same twelve lines + line-21 + line-22); Schedule 1 attachment (`rule.attachment.schedule-1`, T0-7) sees its new line-21 subtotal as $0 and its `over` trigger false for that subtotal — attachment still available on Part I's own terms alone, never newly blocked by this route's presence |
| Closed empty | Closure attestation missing (source set unclosed) | N/A | **Blocked**, `SOURCE_SET_UNCLOSED`, exactly like `rule.schedule1-line10`'s `require_closed` pattern | Line 26 blocked transitively (a `subtract`/`add` input is blocked); AGI blocked transitively; this is the same blocking shape every other Part-II-adjacent route already produces on an unclosed family, not a new blocking mode |
| Nonempty, complete and eligible | Closed with ≥1 member; all twelve T0-2 components resolve favorably (ten universal satisfied, two legal-zero answered `no`/`yes` in the deducting direction) | Positive | Line 21 **computed** per the nine-line worksheet arithmetic, capped at $2,500 and phased out by MAGI | Line 26 total reflects the nonzero line-21 contribution; Schedule 1 attachment now **required** via the new subtotal entry (T0-7), where it was previously inapplicable on a Part-I-only return |
| Nonempty, ineligible | Closed with ≥1 member; a universal component violated (e.g. box 2 checked, related-person interest present) | Blocked, per T0-2/T0-3 — **not** a computed zero, because the box-1 figure itself is not honestly usable | **Blocked**, `DEPENDENCY_ABSENT`/`DEPENDENCY_INVALID` per component, never a silent zero and never a silent full-box-1 pass-through | Line 26 blocked transitively; this is an explicit Track 0 choice (not "computed zero, blocked, or unsupported" left implicit) — a violated universal component means the box-1 figure cannot be trusted as either present or absent, so downstream must not proceed |
| Nonempty, ineligible | Closed with ≥1 member; a legal-zero component answered in the non-deducting direction (claimed as a dependent, or not legally obligated) | Negative, but honestly computable | Line 21 **computed $0** (explicit, not blocked) — the ten universal components and the box-1 amount are all known and clean; the law's own answer for this filer is zero, not "we don't know" | Line 26/AGI computed normally with a $0 contribution from line 21; attachment's line-21 subtotal is $0, same as the closed-empty row |

### 3. Late-authority counterexample

Paper trace: `attest → close → compute → add member → reclose → recompute`,
applied to the Form 1098-E box-1 family and to Schedule 1 Part II
completeness together, since this design composes both.

1. **Attest.** User asserts the twelve T0-2 universal components and the
   two legal-zero components for the return.
2. **Close.** User attests `f1098e.1.source-closure` true against the
   membership horizon current at that moment (say, one statement admitted).
3. **Compute.** The SLI worksheet rule fires: `count == 1`, all
   `conditional_dependency_set` members resolve, line 21 publishes a
   nonzero value; line 26 sums it in; AGI republishes; the new attachment
   subtotal trigger fires `true`.
4. **Add member.** A second, previously-unfurnished Form 1098-E statement
   is admitted (a late 1099-E arrives, or a corrected one supersedes the
   first). The membership horizon changes.
5. **Reclose.** `f1098e.1.source-closure`'s prior finding, keyed on the
   *old* horizon, is **not current** for the *new* horizon — this is
   horizon succession (ADR-0017 pattern), not correction; the old closure
   finding remains a true account of what it closed but is displaced. A
   fresh attestation is required for the new horizon before the worksheet
   can fire again.
6. **Recompute.** Once re-attested, the worksheet re-evaluates with two
   members, publishing a new (generally larger, subject to the $2,500 cap
   and MAGI phaseout) line-21 value; line 26 republishes through the
   derivation edge; AGI republishes; the attachment subtotal re-triggers on
   the new value.

**At every transition, what becomes unusable:** step 4 immediately
displaces the closure finding from step 2 (horizon succession, not merely
"stale but still current" — the runner's saturation model treats the old
closure as no longer satisfying `require_closed` against the new horizon,
matching `f1099g.1.source-closure`'s identical contract exactly). That
displacement cascades through the *existing, unmodified derivation edge*:
line 21's derived finding from step 3 remains a true account of what it was
computed from, but is no longer current; line 26 and AGI, both pinning line
21, are displaced with it. **This is a `PASS`, not a `FAIL`**: the design
never leaves a stale closure-backed value current after new membership
changes the horizon it was attested against — the exact discipline
`f1099g.1`/`ss-benefits-worksheet.v2` already prove out, applied here for
the first time to a Part II total.

### 4. Claim-reuse proof

Every candidate for reuse examined against the three-part standard (same
real-world proposition; same identity and lifecycle; same declared
authority scope and explanation):

| Candidate | Same proposition? | Same identity/lifecycle? | Same declared scope/explanation? | Verdict |
| --- | --- | --- | --- | --- |
| `ss-benefits-scope.no-form-2555` for SLI's Form-2555 gate | Arguably yes (did the taxpayer file Form 2555?) | Yes (literal `{tax-year}` key, free supersession, identical shape) | **No** — title states "for the bounded standard Social Security Benefits Worksheet claim," an SS-worksheet-scoped declaration | **Reject reuse; mint new**, SLI-scoped |
| `ss-benefits-scope.no-form-4563` for SLI's Form-4563 gate | Arguably yes | Yes | **No**, same scope clause | **Reject reuse; mint new** |
| `ss-benefits-scope.no-puerto-rico-or-samoa-income` for SLI's Puerto Rico gate | Arguably yes | Yes | **No**, same scope clause | **Reject reuse; mint new** |
| `filing_status` for the MFS gate | Yes — the same return-level filing status | Yes — same fact, same id, no new version | Yes — `filing_status` carries no worksheet-scoped title; it is a bare return-level fact already read unconditionally by `rule.ss-benefits-worksheet.v2` for an unrelated purpose | **Accept reuse**, unchanged |
| `rounding.convention` for the worksheet's final dollar rounding | Yes | Yes | Yes — a global project convention, not worksheet-scoped | **Accept reuse**, unchanged |
| Twelve Schedule-1-native Part II absence facts (lines 11–20/23/25) for line-26 composition | Yes — each is exactly "this Part II line's adjustment class is absent," Schedule-1-native since ADR-0063 | Yes — same ids, same succession root, no new version | Yes — each title already states its own line number and "for tax year 2025," with no worksheet-specific narrowing | **Accept reuse**, unchanged, pinned as-is |
| `tax.us.2025.income.agi` as the symbol name for the new line-11a/11b producer | Yes — the exact same real-world quantity, adjusted gross income | Yes — same symbol, same consumers, only the *producer* changes | Yes — `rule.form1040-line15.v2`'s own `requires` entry names this exact symbol with no line-11-specific narrowing in its declared meaning | **Accept reuse of the symbol name**; reject reuse of the *old rule's formula* (the bare total-income passthrough is wrong and is replaced, not reused) |

No matching-storage-shape or narrow-title substitution occurs anywhere in
this design: every rejected candidate is rejected specifically because its
declared title scopes it to a different worksheet, and every accepted
candidate is accepted because its declared scope already covers the new
use without narrowing or broadening.

### 5. Neighboring-capability dependency diff

| Neighboring capability | Prerequisites before this design | Prerequisites after this design | New feature-specific prerequisite imposed? |
| --- | --- | --- | --- |
| Form 1040 line 9 (total income) | Unchanged (`rule.form1040-line9.v7`, seven required symbols) | Unchanged — this milestone never touches line 9 or its inputs | None |
| `rule.form1040-line15.v2` (taxable income) | Requires `tax.us.2025.income.agi`, `tax.us.2025.deductions.line-14` | **Identical** — same two required symbols, same rule version, same schema | None — SLI-C8's central guarantee, verified directly against the file (`rule.form1040-line15.v2.json:11`) |
| Schedule 1 Part I / `rule.schedule1-line10` (unemployment route) | Requires its own eleven Part-I-scoped symbols; publishes `tax.us.2025.schedule1.line10-additional-income` | **Identical** — this milestone's Part II work shares no symbol, no fact type, and no rule with Part I | None |
| `rule.attachment.schedule-1` (Schedule 1 attachment) | Required only when the Part I unemployment subtotal exceeds the zero threshold; Part II out of scope by its own title | Required when Part I unemployment **or** Part II SLI subtotal exceeds the threshold (new subtotal entry, T0-7) | **Yes, but justified by the attachment's own meaning, not implementation convenience**: a Part-II-only return with a nonzero SLI deduction genuinely requires Schedule 1 to be attached under IRS instructions (Schedule 1 is attached whenever any of its lines is nonzero) — the prior rule was *incomplete* for any Schedule 1 route beyond Part I unemployment, and this milestone is the first to complete it for one more line. A return with **no Form 1098-E activity** (closed-empty family) sees the new subtotal as $0, its `over` trigger `false`, and the attachment requirement decided **exactly as before** — the empty-route neighboring result is unchanged, satisfying the return state the gate specifically calls out |
| SS Benefits Worksheet (`rule.ss-benefits-worksheet.v2`) | Requires eleven unconditional symbols plus twenty-two conditional Schedule-1-scoped symbols including the twelve Schedule-1-native absence facts this milestone reuses | **Unchanged** — this milestone reuses those twelve facts read-only (pins them into a new aggregate) and never edits, re-versions, or re-pins `rule.ss-benefits-worksheet.v2` itself | None |
| `no-rrb-or-foreign-social-benefit` (fourteenth migration candidate) | Deferred, load-bearing on the SS route only | **Unchanged** — untouched, per Non-goals | None |

### 6. Integration-surface artifact

Every symbol in this design a consumer outside the derivation graph binds
or joins on:

| Consumer | Binding artifact or join | Cardinality it expects | Satisfied by the design? |
| --- | --- | --- | --- |
| `form1040.line-10.form-field` (new) | `binds_symbol: tax.us.2025.schedule1.line26-total-adjustments` | Exactly one row per return, every disposition path (published, computed zero, closure-backed zero, blocked, guard-inapplicable) | **Yes, with evidence** — the line-26 rule is a single, unconditional producer (never guarded by a `when` that could leave it silently absent), mirroring `form1040.line-11.form-field.json`'s existing five-disposition vocabulary exactly (`published_value`, `computed_zero`, `closure_backed_zero`, `blocked`, `guard_inapplicable`) |
| `form1040.line-11a.form-field` (new) | `binds_symbol: tax.us.2025.income.agi` | Exactly one row | **Yes** — same producer, same five-disposition vocabulary as the existing `line-11.form-field.json` template |
| `form1040.line-11b.form-field` (new) | `binds_symbol: tax.us.2025.income.agi` (same symbol as 11a, by design — T0-8) | Exactly one row, value identical to line 11a's on every disposition path | **Yes, with evidence** — because both form-fields bind the *same* symbol rather than two independently-computed ones, the "always equal to 11a" invariant the real form requires (line 11b's own label is "Amount from line 11a") is enforced structurally, not by a separate reconciliation rule that could drift |
| `schedule1.line-21.form-field` (new) | `binds_symbol: tax.us.2025.schedule1.line21-sli-deduction` | Exactly one row | **Yes** — single unconditional worksheet producer, same five-disposition vocabulary |
| `rule.attachment.schedule-1` (v2, new version) | Joins on `tax.us.2025.schedule1.line21-sli-deduction` as a second `requirement.subtotals` entry | Symbol must be present (defined) for the attachment rule to be eligible at all (`_requires` reads `subtotals` directly, `runner.py:467`) | **Yes, with evidence** — the line-21 rule is unconditional (T0-9 item 5: `require_closed` unconditional, eligibility components conditional only on `count > 0`), so it always publishes something (computed value or explicit zero) before the attachment rule's eligibility is even checked, on every path including the closed-empty route |
| Package entrypoint (`package.core-calculations.v32`, new) | Registers all new rule/form-field/citation ids as package members | ADR-0028 admission and binding: every new id must be pinned into the package's dictionary | **Yes** — Track 1 deliverable, not yet built; flagged here as the concrete next step, not asserted done |

**Synthetic end-to-end models required for each materially distinct
disposition path** (Track 1 builds these; enumerated here so Track 1's
scope is unambiguous, not built during Track 0 paper settlement):
(a) closed-empty Form 1098-E family → line 21 computed $0, attachment
unaffected by this route; (b) single statement, full eligibility, MAGI
below phaseout floor → line 21 = capped interest, attachment required;
(c) single statement, MAGI inside the phaseout band → line 21 reduced by
the `divide`/`multiply` ratio; (d) single statement, MAGI at or above the
ceiling → line 21 computed $0 via the ratio reaching 1.000, not blocked;
(e) a statement with box 2 checked → hard route block; (f) a
universal-component violation (e.g. related-person interest) → hard route
block; (g) a legal-zero component answered against deduction (claimed as a
dependent) → line 21 computed $0, not blocked; (h) unclosed family →
`SOURCE_SET_UNCLOSED` block; (i) late member added after a prior close →
the late-authority counterexample trace (artifact 3) reproduced live. Each
is a materially distinct disposition path per artifact 6's requirement; a
model that only argues these rather than building them is not evidence —
Track 1 must build all nine before the implementation charter can close.

**Valid presentation-model probe**: required and not yet built (Track 1),
for `form1040.line-10`, `-11a`, `-11b`, and `schedule1.line-21` — each is a
form-field-bound symbol per the gate's own trigger clause.

**Precedent-property verification**: `rule.attachment.schedule-1`'s
existing "any subtotal over threshold" semantics were built and tested for
a *single*-subtotal case (Part I only). This design is the first to give it
a *second* subtotal entry — verified directly against `runner.py:812-820`
that the loop already iterates `subtotal_symbols` generically and computes
`any(t["over"] for t in triggers)` without assuming a list of length one,
so the precedent's properties (per-subtotal trigger recording, no silence
about which subtotal crossed) genuinely extend to two subtotals without
new runner code — confirmed by reading the implementation, not assumed
from the shape of the JSON alone.

## Track 0 adversarial closure

- Authority-lifecycle table: PASS — artifact 1 above; every contributed,
  reused, and aggregate authority this design relies on is tabled with its
  scope and invalidating event, none resting on tax-year-key-implies-scope.
- Empty/nonempty authority matrix: PASS — artifact 2 above; five states
  exercised (closed-empty complete, closed-empty-missing-closure,
  nonempty-eligible, nonempty-universal-violation, nonempty-legal-zero),
  each with an explicit feature result and neighboring (attachment) result,
  none inherited from a convenient guard.
- Late-member lifecycle: PASS — artifact 3 above; the
  attest→close→compute→add-member→reclose→recompute trace shows the closure
  finding displaced by horizon succession at step 4/5, cascading through
  the existing derivation edge to line 21, line 26, and AGI, matching the
  `f1099g.1`/`ss-benefits-worksheet.v2` precedent exactly, applied here for
  the first time to a Part II total.
- Neighboring capability dependency diff: PASS — artifact 5 above; the one
  new feature-specific prerequisite (Schedule 1 attachment now also
  triggers on the Part II SLI subtotal) is justified by the attachment's
  own IRS-instruction meaning, not implementation convenience, and the
  no-activity return state is verified unchanged.
- Reused-claim semantic/lifecycle equivalence: PASS — artifact 4 above;
  three candidates rejected for scope mismatch despite shape and
  proposition similarity (`no-form-2555`/`no-form-4563`/
  `no-puerto-rico-or-samoa-income`, all minted new instead), three accepted
  where scope genuinely matches (`filing_status`, `rounding.convention`,
  the twelve Schedule-1-native absence facts), and `tax.us.2025.income.agi`
  accepted as a symbol name while its old producing formula is explicitly
  rejected and replaced.
- Integration surface: **PENDING** — bindings, cardinalities, and every
  disposition path are enumerated and argued from the runner's actual code
  (`runner.py:467`, `:812-820`), not from JSON shape alone, in artifact 6
  above. The nine synthetic end-to-end disposition-path models and the
  presentation-model probes named there are **not built** — this Track 0
  session's dispatch was explicitly paper-only ("no schema files, no
  rule/fact-type JSON, no version numbers written to the repository"),
  which is in direct tension with `PROJECT_PLANNING.md`'s own text ("Track
  0 cannot be marked settled... while an externally bound symbol lacks a
  built end-to-end model for each of its distinct disposition paths...
  Such a result returns to paper design or to the owner for disposition;
  it is never downgraded to 'nonblocking' by the Foreman"). This
  settlement does not resolve that tension unilaterally — flagged
  explicitly for the foreman/owner rather than silently marked PASS, since
  declaring built evidence that does not exist would be exactly the kind
  of unearned PASS the gate exists to prevent. Every other artifact above
  is genuine paper evidence and is `PASS` on its own terms.
- Known limitations affecting correctness: none identified in the design
  itself. The one open item is procedural, not substantive: whether Track
  0 closes now on five `PASS` artifacts plus a named, reasoned gap in the
  sixth (owner/foreman disposition), or a short build-evidence pass
  (Track 0b) is required before the sixth can read `PASS` and the
  implementation charter can be filed — **owner/foreman disposition
  required**, named as a finding in the closing report rather than decided
  here.

### Foreman disposition on the integration-surface gap

**No Track 0b.** The `ssa-no-activity-applicability` precedent (its own
"Integration surface: PASS, retroactively") establishes that this artifact
is satisfied by whatever evidence Track 1 commits — a separate paper-only
pass would just re-argue what building the routes settles directly. Track 1
below is chartered to build the substrate and the nine synthetic
disposition-path models (plus the presentation-model probes) as committed,
runnable tests exercised through the real coordinator
(`live_coordinate_run`), matching the precedent's evidentiary bar exactly.
The integration-surface artifact remains **PENDING** — not `FAIL`, not
downgraded to nonblocking — until that evidence exists, then flips to
`PASS, retroactively` the same way the precedent's did, with no separate
closure step. Track 0's other five artifacts are accepted as `PASS` now;
nothing in Track 1 may weaken them without reopening this document.

## Tracks

Atomic, one commit each, in the T0-9 substrate order:

* **Track 1 — `multiply`/`divide` evaluator operators and `rule-artifact.v6`.**
  Additive dispatch entries in `packages/derivation/evaluator.py`; additive
  schema successor to `rule-artifact.v4` (v4's bytes untouched). Unit tests
  for both operators, including `divide`'s zero-divisor guard and its
  `min_decimal_places`/`rounding` behavior. No tax content yet — this track
  is pure substrate, reviewable and testable in isolation.
* **Track 2 — Form 1098-E family and the twelve T0-2 eligibility components.**
  New fact types (member family + twelve component facts, ten universal +
  two legal-zero), synthetic fixtures for VOID exclusion and multi-statement
  cardinality.
* **Track 3 — the Student Loan Interest Deduction Worksheet rule citizen.**
  The nine-line `i1040gi` p.99 worksheet using `conditional_dependency_set`
  for eligibility gathering and the new `multiply`/`divide` ops; publishes
  `tax.us.2025.schedule1.line21-sli-deduction`.
* **Track 4 — Schedule 1 line-26 composition and attachment succession.**
  `tax.us.2025.schedule1.line26-total-adjustments`; the new
  `rule.attachment.schedule-1` version (`attachment-rule.v9`) with the
  second `requirement.subtotals` entry.
* **Track 5 — Form 1040 line 10 / 11a / 11b succession.**
  Corrected `rule.form1040-line11` successor producing
  `tax.us.2025.income.agi` via total income minus Schedule 1 line 26; new
  `form1040.line-10`/`-11a`/`-11b` form-field citizens.
* **Track 6 — the nine synthetic end-to-end disposition-path models
  (integration-surface artifact 6) and presentation-model probes**, run
  through `live_coordinate_run`, closing Track 0's `PENDING` row. **Carries
  a known limitation from Track 3**: the five per-statement universal
  eligibility witnesses are read via a single unkeyed `ref` per fact-type-id,
  so `packages/derivation/marshal.py` binds only the first current finding
  per symbol on a multi-statement family with *disagreeing* per-statement
  answers, silently dropping the rest. Track 3's fixtures are single-
  statement only and do not exercise this. This is a pre-existing
  marshalling property, not something Track 3 introduced, but Track 6's
  nine models must include a multi-statement-disagreement case to prove
  the route's actual behavior (block, or first-wins) rather than assume it.
* **Track 7 — the two ADRs** (expression-language extension;
  Schedule 1 Part II completeness/line-26 composition), citing the evidence
  Tracks 1–6 produced.
* **Track 8 — package, registry, release, explanation, presentation.**

Each track's own charter (goal, boundary, inputs, outputs, verification,
migration risk, data safety) is filed as a Context Capsule immediately
before dispatch, per `PROJECT_PLANNING.md` ("Track Planning Checklist").

## Exit criteria

* Track 0 settled with adversarial closure PASS on all six artifacts (or an
  owner-accepted ADR disposing of any FAIL).
* Production-shaped synthetic coordinator, lifecycle, completeness, package,
  explanation, and presentation evidence for the bounded class Track 0
  defines.
* Independent review READY on the curated branch range.
* Every prior-milestone regression fixture unmodified and passing.
* Milestone Closeout performed per `PROJECT_PLANNING.md`.

## Stop conditions

The five standing conditions in this thread's owner authorization govern.
Two are live risks specific to this milestone and are called out explicitly:

* If T0-6 or T0-8 finds that Schedule 1 Part II completeness genuinely turns
  on interpreting `docs/governance/ontology.md` rather than composing an
  existing mechanism (echoing the F1 finding that stopped the predecessor
  branch), stop for the owner rather than re-deciding the individuation
  question independently.
* If the `multiply`/`divide` addition cannot be expressed additively and
  would require editing the bytes of an already-published schema version,
  stop — that is stop condition 4, not a design choice to route around.

## Disposition of PR #169 (proposed)

**Recommend: merge, with `docs/phase-state.md` excluded from the merge.**
The PR's head (`1053cd7b`) is identical to the retired branch's final tip —
it carries the complete retrospective and the full design-exploration
milestone document, including the Durable findings register this plan draws
from. That is a legitimate design record: real evidence, a real owner
ruling, and the seed of this plan's inputs, exactly the kind of curated
history `PROJECT_PLANNING.md` says belongs in a retrospective rather than
being discarded. It adds no code and allocates no version number, so merging
it costs nothing beyond review time.

The one hazard: the PR's `docs/phase-state.md` diff is stale — it predates
both the SSA-no-activity and fact-type-succession milestones that have since
merged and rewritten that file twice. Merging the PR as-is would clobber the
current phase-state pointer. Before merging, drop that hunk (keep only the
two new files: the retrospective and the milestone plan) so the merge is
retrospective-only and cannot regress the re-entry document. This is a
one-line ask for whoever merges it, not a reason to close the PR.
