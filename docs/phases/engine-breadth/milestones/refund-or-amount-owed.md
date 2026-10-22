<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "refund-or-amount-owed",
  "status": "Planned. P0 verifies the 2025 law for Form 1040 lines 22-38 and traces how withholding on the documents the engine already reads would reach the return.",
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
