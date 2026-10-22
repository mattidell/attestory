<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "refund-or-amount-owed",
  "status": "P0 complete; contract settled. Track 1 makes line 20 free of foreign-tax questions when there is no foreign tax and records withholding on lines 25a-25d.",
  "scope": [
    "carry every return the engine computes from tax after credits to total tax, payments, and the refund or amount owed (Form 1040 lines 22-37)",
    "record federal income tax withheld from the source documents the engine already reads, starting with Form W-2 box 2",
    "ask for estimated tax payments and other payments the documents do not show, each with a question whose meaning matches its rule",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no new income source, form or attachment beyond the withholding amount on documents already read",
    "no Schedule 2 additional taxes (alternative minimum tax, self-employment tax, additional Medicare tax, net investment income tax); they stay declared absent",
    "no refundable credit (earned income credit, additional child tax credit, American opportunity credit, net premium tax credit); they stay declared absent, never assumed zero",
    "no estimated-tax penalty computation (Form 2210); declared absent",
    "no direct deposit, payment method or electronic filing detail",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-22-senior-and-dependent-deductions.md",
      "docs/phases/engine-breadth/milestones/refund-or-amount-owed.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/refund-or-amount-owed.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/refund-or-amount-owed.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-22-senior-and-dependent-deductions.md",
      "docs/phases/engine-breadth/milestones/refund-or-amount-owed.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# Refund or Amount Owed: Finishing the 2025 Return

Milestone key: refund-or-amount-owed.
Branch: milestone/refund-or-amount-owed-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-22.
Starting point: `origin/main` at `25a11498` (PR #218 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216); whichever merges second
takes the next free package, registry and release versions.

## What we are trying to accomplish

The last two milestones made Form 1040 lines 12e through 16 follow 2025 law.
The return still stops at tax after nonrefundable credits
(`rule.form1040-tax-after-credits`, line 22). Nothing computes total tax
(line 24), federal income tax withheld (lines 25a-25d), payments (line 33),
or the line a person actually acts on: the refund (lines 34-35a) or the
amount owed (line 37). The W-2 records only box 1; no source records
withholding except a few facts that exist to block (for example Form 1099-G
box 4).

The useful outcome is that every return the engine computes ends where a
filed return ends: a refund or an amount owed, explained back to the
documents and answers it came from. Lines that need taxes or credits the
engine does not compute are declared absent by questions, so a return that
needs them is outside the supported class instead of silently low.

## What we know

- Core v51 computes lines 1-16, line 20 (Schedule 3 direct foreign tax
  credit) and tax after credits; line 22's rule already requires answers that
  Schedule 2 line 17 and the child tax credit line 19 are absent.
- Fact types for withholding exist for SSA-1099 box 6, Form 1099-K box 4 and
  a Form 1099-G box-4 authority; none for W-2 box 2 or Forms 1099-INT,
  1099-DIV and 1099-R box 4.
- W-2 wages reach the engine through `tax.us.2025.w2.box1-wages`, used by
  `packages/derivation/entry_loop.py` and fixture generators.
- Sources downloaded (ignored) under `temp/tax-on-taxable-income/sources/`:
  the 2025 Form 1040 instructions (lines 22-38 near text line 2551 onward and
  4200-4520). P0 downloads the 2025 Form 1040 and Form W-2 instructions it
  needs into the same ignored directory.
- What we do not know: how each source document the engine reads is
  recorded, and therefore what adding its withholding amount takes; whether
  any route records withholding today that is silently dropped; whether
  line 23 (other taxes) and the refundable credits can share one absence
  answer or need one each; how lines 34-37 round and which line a zero
  balance lands on; and whether a person must choose between refund and
  applying an overpayment to 2026 estimated tax (line 36).

## Actions the team will take

1. **P0 — verify and trace.** Record lines 22-38 of the 2025 Form 1040 with
   citations. For each source document the engine reads (W-2, 1099-INT,
   1099-DIV, 1099-R, 1099-G, SSA-1099, 1099-K, K-1), name its withholding
   box, how the document is recorded today, and what recording that box would
   take. Trace W-2 box 1 from document to rule on the real path. Probe one
   W-2-only return to line 22 on core v51. Hand-compute the case table. No
   content changes.
2. **Decide.** Settle the contract here: which documents' withholding is in
   scope (W-2 at least), the absence questions for line 23 and lines 27-32,
   the estimated-payment question, line 36, rounding, rule ids, and
   compatibility for saved history. A new expression operation, schema
   successor or owner-visible choice returns to the owner first.
3. **Track 1 — withholding.** Fact types and recording for the in-scope
   withholding boxes, lines 25a-25d, and cases through the real path.
4. **Track 2 — total tax to the bottom line.** Lines 23-24, 26, 33, 34, 35a,
   36 and 37 as one rule per line, the successor package chain, and saved
   presentations whose explanation walks reach each withholding document.
5. **Close.** Fresh-reader review of the curated candidate, the full lane
   before ready, exact-head CI, retrospective, coverage frontier and parked
   list.

## Cases that will shape the design

- W-2 only, single: withholding above the tax (refund), below it (amount
  owed), and exactly equal (neither).
- Two W-2s, and a W-2 plus a 1099-INT with backup withholding: line 25a and
  25b totals.
- Estimated tax payments with a refund; a refund the person applies to 2026
  estimated tax.
- A senior on core v51's line 13b, and a dependent on its line 12e, carried
  to the bottom line.
- A return answering none of the new questions on the successor package is
  blocked with the missing facts named, never a silent zero.
- Every existing golden keeps its package and its result.

P0 computes the figures for these cases from the sources.

## P0 result

P0 is complete ([law and path](refund-or-amount-owed-evidence/p0-law-and-path.md)).
Lines 22-38 are verified against the 2025 Form 1040 and instructions. No
schema successor, expression operation or engine change is needed.

- **Withholding is new content.** W-2 box 2 and Forms 1099-INT, 1099-DIV and
  1099-R box 4 have no fact type. Each follows the W-2 box 1 shape: a fact
  type, a source family and closure scoped to it, and a `collect`-and-add
  rule. Form 1099-R's is a companion on the existing IRA statement.
- **Form 1099-K box 4 is recorded and summed nowhere.** It only names a block
  reason. The Foreman corrected P0 here: the line 25b instructions cover any
  Form 1099 showing tax withheld on "other income you received" in box 4, so
  it belongs on line 25b.
- **Forms 1099-G box 4 and SSA-1099 box 6 admit only zero.** Recording a real
  amount would change an admission rule those routes ship today.
- **Line 22 is reachable only through the direct foreign tax credit.** The
  Foreman found this in P0's probe: line 20 comes from
  `rule.schedule3-line1-direct-ftc`, which requires the direct-credit
  election ("no" blocks) and about twenty foreign-tax eligibility answers,
  even when no Form 1099-DIV box 7 shows foreign tax. A W-2-only return must
  answer all of them to reach line 22. P0's probe supplied them.
- **Lines 23 and 27-31 need their own absence answers.** The existing
  Schedule 2 and Schedule 3 answers cover Schedule 2 Part I and Schedule 3
  Part I, not Schedule 2 Part II (line 23) or Schedule 3 Part II (line 31).
- **Lines 34 and 37 are each conditional on "more than".** Equal payments and
  tax give neither a refund nor an amount owed. Line 36's election to apply an
  overpayment to 2026 cannot be changed later.
- P0's W-2-plus-1099-INT case held tax constant despite the interest income.
  The tracks recompute it with the interest taxed.

## Contract

1. **No foreign tax, no foreign-tax questions.** A successor to
   `rule.schedule3-line1-direct-ftc` publishes $0 when the Form 1099-DIV
   box 7 source set is closed with no foreign tax, requiring only that
   closure. The election and eligibility answers are required only when box 7
   shows foreign tax (`conditional_dependency_set`). Every other result of
   the v1 rule is unchanged.
2. **Withholding in scope:** W-2 box 2 (line 25a); Forms 1099-INT, 1099-DIV
   and 1099-R box 4, and the already-recorded Form 1099-K box 4 (line 25b).
   Line 25c is $0 because no W-2G route exists. Forms 1099-G and SSA-1099
   withholding stay zero-only and are parked. Each withholding amount is
   per statement, summed across statements, and rounded once, like box 1.
3. **New questions** (`yes`/`no` unless stated, no default):
   - the return has none of the other taxes on Schedule 2 Part II
     (line 23);
   - the return claims none of the refundable credits and other payments on
     lines 27-31 (earned income credit, additional child tax credit, American
     opportunity credit, refundable adoption credit, Schedule 3 Part II);
   - the return reports no estimated tax penalty (line 38);
   - 2025 estimated tax payments and any 2024 overpayment applied (line 26),
     an amount, $0 allowed;
   - the amount of an overpayment applied to 2026 estimated tax (line 36), an
     amount, required only when line 34 is more than $0. An amount above
     line 34 blocks rather than being reduced.

   All but line 36's are required on every return that adopts the successor
   package. A missing answer blocks with the fact named.
4. **One rule per line:** 23, 24, 25a, 25b, 25c, 25d, 26, 32, 33, 34, 35a,
   36, 37 and 38, with lines 27-31 as one absence-gated $0 that line 32
   reads. Line 34 is line 33 minus line 24 when larger, else $0; line 37 is
   line 24 minus line 33 when larger, else $0; line 35a is line 34 minus
   line 36. Line 38 is $0 by its answer, and line 37's rule follows the
   instructions for it.
5. **Successor content only:** core v52, registry v50 and release v50 (unless
   PR #216 merges first), an adoption fixture and new goldens. Earlier
   packages, saved presentations and goldens stay byte-identical.
6. **Data safety and lanes:** synthetic amounts only; the full lane runs
   before the PR is marked ready.

## Parked by this milestone

- Forms 1099-G box 4 and SSA-1099 box 6 withholding: both admit only zero
  today; recording a real amount changes a shipped admission rule.
- Form W-2G and line 25c.
- Refundable credits (lines 27-31), Schedule 2 Part II taxes and the
  estimated tax penalty, each declared absent.
