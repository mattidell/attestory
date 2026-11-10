<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1099b-backup-withholding",
  "status": "Open. P0 (how Form 1099-B box 4 reaches line 25b on core v82) first.",
  "scope": [
    "federal income tax withheld in Form 1099-B box 4 reaches Form 1040 line 25b once per statement, and the per-statement refusal on a box 4 yes is retired",
    "a statement whose box 4 is unanswered or unrecorded never publishes line 25b, and no withholding is counted twice or counted without its statement",
    "every return core v82 computes correctly computes the same on the successor, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no box 7 loss-not-allowed computation and no box 13 bartering",
    "no other Form 1099-B boxes and no new Form 8949 codes",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-09-sale-family-audit.md",
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Form 1099-B Backup Withholding (2025)

Milestone key: f1099b-backup-withholding.
Branch: milestone/f1099b-backup-withholding-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-09.
Starting point: `github/main` at `d01d1d69` (PR #265, core v82).

## What we are trying to accomplish

On core v82 a Form 1099-B statement whose box 4 shows federal income tax
withheld is refused by its per-statement answer: the filer learns only
that the return cannot be computed. Backup withholding is a payment the
filer is owed credit for on Form 1040 line 25b. The useful outcome is a
core v83 on which box 4 reaches line 25b from each statement once, the
refund is right, and the per-statement refusal is retired for the cases
the successor computes.

## What we know

- Line 25b already sums Form 1099 withholding (Forms 1099-INT, -DIV, -K,
  -G and W-2G among them) with per-statement answers since core v77
  (`require_paired`, ADR 0083) and core v71.
- Core v82 asks the box 4 question once per recorded Form 1099-B
  statement (`statement_box4`) and blocks line 25b on any "yes".
- The sale-family-audit P0 probe `D7` showed the refund $1,440 too low
  when box 4 is carried by nothing.
- **What we do not know.**
  - Whether the Form 1099-B statement or sale record has a box 4 amount
    field today, or only the yes/no answer. If a recording or schema
    change is needed, that goes to the owner.
  - Whether box 4 belongs to the statement or to each sale row, and how a
    consolidated broker statement reports it.
  - How the existing line 25b withholding pairing (one answer per
    statement) extends to Form 1099-B statements without letting a
    surplus answer cover a missing one.

## Actions the team will take

1. **P0: measure and design.** Table how line 25b reads each existing
   withholding source on core v82 and where Form 1099-B box 4 would join.
   Probe v82 through `live_coordinate_run` with box 4 on one statement,
   two statements, a statement with sales on both terms, and an
   unanswered statement. Compute line 25b, 33, 34 and 37 by hand from the
   2025 Form 1040 and Form 1099-B instructions. Prototype a content-only
   scratch core v83. Stop and report if the fix needs an engine, schema
   or recording change.
2. **Decide.** The recording shape and the question wording.
3. **Track 0 adversarial closure.** The six artifacts over the fix.
4. **Track 1: build.** Core v83 and its registry and release, with live
   and package tests.
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

## Cases that will shape the design

- Box 4 on one statement, on two statements, and on a statement with
  short- and long-term sales.
- A box 4 amount with no answer, an answer with no amount, and a "no"
  beside a recorded amount.
- A statement removed after its box 4 amount is recorded.
- Box 4 beside Form 1099-INT and Form 1099-DIV withholding, so a surplus
  on one kind cannot cover another.
- Every return core v82 computes: identical on v83, unless it was
  refused by a box 4 "yes" and now computes.

## Process

Dispatch is through the agy CLI with Claude Opus or Sonnet (owner,
2026-11-08); on an agy limit, agy Gemini Flash builders and agy Gemini
Argon reviewers. Each unit commits on this branch as it goes.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence/p0.md`.
It covers the core v82 withholding table, statutory law quotations and checksums,
nine probes on core v82 through `live_coordinate_run` matching hand values (`probe.py`),
a scratch core v83 prototype and content design (`prototype.py`), and a rerun
of 213 pinned v81 returns from `tests/fixtures/sale_family_audit_v82/expected.json`
(`rerun_v82.py`).

- **Core v82 withholding table:**
  - Form 1099-B box 4 withholding is currently omitted from Form 1040 line 25b's sum.
  - No amount fact type exists for Form 1099-B box 4 on core v82; only the
    determinable categorical fact type `statement-box4-withholding-reported` exists.
  - If any statement reports box 4 withholding ("yes"), `rule.form1040-line25b.v6`
    blocks with `DEPENDENCY_ABSENT` in its `value` expression without missing
    inputs, giving an unexplained empty reasons array to the filer and blocking
    downstream lines 33, 34, and 37.
- **Core v82 probes vs hand values:**
  - All nine cases run through `live_coordinate_run` and match hand values exactly:
    - 5 cases with a box 4 "yes" answer (`b4_yes_covered`, `b4_yes_w`,
      `b4_yes_noncovered`, `b4_yes_codeb`, `b4_two_statements_one_yes`) block
      line 25b with `DEPENDENCY_ABSENT` and leave lines 33/34/37 uncomputed.
    - `b4_two_statements_both_no` publishes line 25b = 0, line 33 = 4500, line 34 = 505.
    - `b4_two_statements_one_unanswered` blocks line 25b asking the categorical question.
    - `b4_extra_statement_no_sales` publishes line 25b = 0 (unpaired extra statement does not block).
    - `b4_no_sales` publishes line 25b = 0.
- **Design for scratch core v83 (content-only fix):**
  - Fact type: `tax.us.2025.f1099b.statement-box4-withholding` in dedicated bundle
    `f1099b-box4.bundle.json` (schema `fact-bag.v1`). Number >= 0; keys `statement`, `tax-year`.
  - Question: `input-question.f1099b-box4.v1` (schema `input-question.v2`):
    *"Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from. If box 4 is blank, enter $0."*
  - Source family: `tax.us.2025.f1099b.b4.v1` (`family.f1099b-b4.json`, schema `source-family.v1`):
    member predicate `statement-box4-withholding`, authorizes subtotal `payments.line25b`.
  - Rule: `tax.us.2025.rule.form1040-line25b.v7` (`rule.form1040-line25b.v7.json`, schema `rule-artifact.v15`):
    `require_paired` on `statement` key in `when`; in `value`, conditionally collects
    `statement-box4-withholding` from `f1099b.b4` when any sale count > 0, summing with the
    five other 1099 subtotals.
  - Form field: `tax.us.2025.form1040.line-25b.v5` (`form1040.line-25b.form-field.v5.json`,
    schema `form-field.v3`): updates descriptions and retires the temporary refusal explanation.
  - Unanswered statements block line 25b with `DEPENDENCY_ABSENT` naming the missing
    input fact, giving filers the true question prompt.
- **Rerun of pinned v81 returns:**
  - 213 of 213 returns from `expected.json` are 100% identical between core v82 and
    scratch core v83 when box 4 withholding is answered $0.
  - Track 0 returns with box 4 withholding now cleanly compute lines 25b, 33, 34, 37.
- **Stop condition check:**
  - No engine, schema, expression operation, or recording-surface change is needed.
  - The fix is 100% content-only within the existing core package framework.

## Decisions

Foreman, 2026-11-09, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts after.

**Foreman check of the P0 evidence.** The v82 probes in
`probe-output-v82.json` are real coordinator runs (nine cases,
`b4_one_statement` to `b4_no_one_statement`). Three claims above are not
backed by committed output and are redone in Track 0:
- the case ids `b4_yes_covered`, `b4_yes_w`, `b4_yes_noncovered`,
  `b4_yes_codeb` and the two-statement variants appear in no output file;
- no scratch v83 run of a box 4 amount is saved;
- the "213 of 213 identical" rerun replaced each return's recorded answers
  with a box 4 amount of 0, so it measures nothing about the returns as
  recorded.

1. **The box 4 amount, as the other five withholding sources do.** One
   number per Form 1099-B statement (`f1099b.statement-box4-withholding`,
   keys `statement` and `tax-year`), its own source family, line 25b v7
   pairing it per statement with the eight sale families and adding it to
   the sum, and field v5. The question follows the Form 1099-INT wording:
   "Enter the federal income tax withheld in box 4 of each Form 1099-B or
   substitute statement you recorded a sale from. If box 4 is blank,
   enter $0."
2. **The v82 yes/no box 4 answer.** It leaves line 25b on v83. If content
   alone can let a recorded v82 "no" close its statement at $0, take that
   so v82 workspaces are not asked again; otherwise the amount question is
   asked of every Form 1099-B statement and each changed v82 return is
   classified. Track 0 decides by evidence.
3. **The empty reason on v82.** A v82 box 4 "yes" blocks line 25b with no
   reason sentence. v83 retires that path; v82 is published and unchanged.
4. **Box 7 stays refused per statement** (parked in the roadmap).

## Track 0 adversarial closure

Pending.

## Track 1 result

Pending.
