# Charter — Iteration 1

Foreman, 2026-07-10. Status: under committee review (round 0); no building until owner disposition.

## What iteration 1 builds

One candidate rule-artifact encoding (the primary design), drafting every fixture below as real artifacts, with a throwaway evaluator that runs them against synthetic workspaces on branch `prototypes/rule-language/it1`. The rival encoding is iteration 2, in a clean room, against this same charter (rivals rule).

## Fixture set

Real rules from the First-Tax-Slice scope (2025 federal). Each must be drafted as artifacts, not prose. Values come from public law (see harvest notes, fixture source material).

- **F1 — Aggregation.** Sum of W-2 box 1 wages across employers → Form 1040 line 1a.
- **F2 — Cross-form bridge.** 1099-INT box 1 amounts → Schedule B Part I and line 4 → Form 1040 line 2b. The bridge must be artifact-declared (E11.3).
- **F3 — Applicability threshold.** Schedule B is required only when taxable interest exceeds $1,500; below it, interest reports directly. A conditional *path*, not just a conditional value.
- **F4 — Multi-source aggregation.** Federal withholding from W-2 box 2 and 1099-INT box 4 → Form 1040 line 25 components.
- **F5 — Parameter table keyed by an elective fact.** Standard deduction by filing status → line 12. Must block while filing status is open (Article 3 / E3.1), and the deduction amounts must live in a versioned parameter declaration, not in the rule body.
- **F6 — Subtraction with floor.** Taxable income = AGI − deductions, floored at zero → line 15.
- **F7 — Table/bracket computation.** Line 16 regular tax: IRS tax table below $100,000 (row-range lookup semantics), Tax Computation Worksheet (bracket arithmetic) at or above. The worksheet logic itself must be expressed in artifacts — "the executor implements the worksheet" is the lineage-2 failure this fixture exists to prevent.
- **F8 — Comparison and branch.** Overpayment vs amount owed (lines 33/24 → 34/37): signed comparison selecting which output facts exist.
- **F9 — Method delegation.** Whole-dollar rounding: the IRS permits rounding all entries or none — a convention the user elects. Where does the convention live, how do rules reference it, and how is it applied consistently across every computation?
- **F10 — Evolution probe (paper only).** Draft F5 and F7 for tax year 2026 with changed parameters: what changes, what versions, what stays?

## Questions iteration 1 must answer

- **Q1.** Can one artifact grammar express F1–F9 with zero engine special cases — including F7's worksheet — such that deleting any artifact removes exactly its behavior?
- **Q2.** How are policy parameters declared, versioned, and cited by rules? (Lineage 2's parameter/rule separation is the working hypothesis; test it.)
- **Q3.** How does a rule declare applicability and blocking so that a blocked run yields schema'd reasons, not narrative? (it0 lesson 2.)
- **Q4.** What expression form does F7 force — does a fixed operation enum survive worksheet-shaped rules, or does the grammar need expression trees, and at what legibility cost?
- **Q5.** Is evaluation order-stable? Same findings, artifacts shuffled: byte-identical outputs, including rounding under F9's convention.
- **Q6.** How is elective dependence declared (F5), and does an open choice block cleanly?
- **Q7.** Are F3, F5, and F7 artifacts recoverable by the starved fresh reader? (Measured in round 1; the builder should write for this test without writing *to* it.)
- **Q8.** What must pins carry for explanation walking — do it0's pin roles earn their place?
- **Q9.** Does it0's `derived-publication` act kind plus final run record hold up, or does the interruption window (published findings, no record yet) force a start/completion record pair? Draft the act and record shapes the design implies.
- **Q10.** Are derived-finding and record IDs deterministic in fixture mode (portability requirement)?

## Out of scope for iteration 1

Credits, dependents, QDCGT worksheet, state rules, migrations, generators — the charter grows only by a new charter. The rival design (it2) and any third iteration answer the same questions on the same fixtures.

## Evidence expected

Drafted artifacts for F1–F9 and the F10 paper exercise; evaluator with double-run and shuffled-order runs; examination note answering Q1–Q10 with paths, negative results included.
