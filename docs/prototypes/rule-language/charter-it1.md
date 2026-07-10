# Charter — Iteration 1

Version 2 (2026-07-10). Status: approved for iteration 1 — round-0 reviews complete, adversary dissent withdrawn (`reviews/round-0-adversary-delta.md`), builder seat open.

Revision history: v1 reviewed in round 0 (`reviews/round-0-governance.md`, `reviews/round-0-adversary.md`); v2 incorporates all ten findings (owner disposition 2026-07-10). Every amendment traces to a review exhibit.

## What iteration 1 builds

One candidate rule-artifact encoding (the primary design), drafting every fixture below as real artifacts, with a throwaway evaluator that runs them against synthetic workspaces on branch `prototypes/rule-language/it1`. The rival encoding is iteration 2, in a clean room, against this same charter (rivals rule).

## Fixture set

Real rules from the First-Tax-Slice scope (2025 federal). Each must be drafted as artifacts, not prose. Values come from public law (see harvest notes). Narrow synthetic cases are acceptable where noted; blocking with schema'd reasons is an acceptable answer where facts are open.

- **F1 — Aggregation.** Sum of W-2 box 1 wages across employers → Form 1040 line 1a.
- **F2 — Cross-form bridge.** 1099-INT box 1 amounts → Schedule B Part I and line 4 → Form 1040 line 2b. The bridge must be artifact-declared (E11.3).
- **F3a — Amount-triggered applicability.** Schedule B required when taxable interest exceeds $1,500; below it, interest reports directly. A conditional *path*, not just a conditional value.
- **F3b — Non-amount applicability.** *(v2, adversary attack 1.)* Schedule B Part III required by a foreign-account fact regardless of interest amount: taxable interest of $10, no dividends, asserted foreign-account fact → Part III applicability with its questions surfaced.
- **F4 — Multi-source aggregation.** Federal withholding from W-2 box 2 and 1099-INT box 4 → Form 1040 line 25 components.
- **F5 — Parameter table keyed by an elective fact.** Standard deduction by filing status → line 12. Must block while filing status is open (Article 3 / E3.1); deduction amounts live in a versioned parameter declaration, not the rule body.
- **F6 — Subtraction with floor.** Taxable income = AGI − deductions, floored at zero → line 15.
- **F7 — Table/bracket computation.** Line 16 regular tax: IRS tax table below $100,000 (row-range lookup semantics), Tax Computation Worksheet (bracket arithmetic) at or above. The worksheet logic itself must be in artifacts — "the executor implements the worksheet" is the lineage-2 failure this fixture exists to prevent.
- **F8 — Comparison and branch.** Overpayment vs amount owed (lines 33/24 → 34/37): signed comparison selecting which output facts exist.
- **F9 — Method delegation.** Whole-dollar rounding: an elected convention (round all entries or none). Where the convention lives, how rules reference it, how it applies consistently.
- **F10 — Evolution probe (paper only).** *(v2 expanded, adversary attack 7.)* (a) Parameter change: F5 and F7 for tax year 2026 with changed values. (b) Structural change: one field mapping changes, one applicability question changes, or one source-box semantic changes — name which artifact ids persist, which new ids appear, which versions change, and whether a migration artifact is implicated.
- **F11 — Exclusion and source-box classification.** *(v2, adversary attack 2.)* Schedule B line 3 (excludable savings-bond interest) and 1099-INT box 3 classification: a narrow synthetic case with zero excludable amount is acceptable, plus a blocked reason when the exclusion facts are open.
- **F12 — AGI chain with an adjustment.** *(v2, adversary attack 3.)* Form 1040 line 9 → Schedule 1 line 26 → line 10 → line 11, with 1099-INT box 2 (early-withdrawal penalty) as the first concrete adjustment.
- **F13 — Rounding boundary.** *(v2, adversary attack 4.)* Two sub-dollar additive inputs (e.g., two W-2 wages of $1.49) where per-input rounding and post-total rounding diverge ($2 vs $3). Artifacts must declare the rounding stage; the IRS convention (include cents when adding, round the total) must be expressible and checkable.
- **F14 — No-convention blocking.** *(v2, adversary attack 5.)* With the rounding convention unasserted, every rule needing it blocks with schema'd reasons — or the design argues from artifacts why "no rounding" is not an elective default.

## Questions iteration 1 must answer

- **Q1.** Can one artifact grammar express F1–F14 with zero engine special cases — including F7's worksheet — such that deleting any artifact removes exactly its behavior?
- **Q2.** How are policy parameters declared, versioned, and cited by rules — and *(v2, governance check 2)* how do artifacts or artifact packages declare their effective scope (tax year, jurisdiction, family) as content, such that the evaluator supplies no tax meaning through ambient run configuration, directory layout, or branch context?
- **Q3.** How does a rule declare applicability and blocking so that a blocked run yields schema'd reasons, not narrative? (it0 lesson 2.)
- **Q4.** What expression form does F7 force — does a fixed operation enum survive worksheet-shaped rules, or does the grammar need expression trees, and at what legibility cost?
- **Q5.** Is evaluation order-stable *and stage-correct*: same findings, artifacts shuffled, byte-identical outputs — and F13 distinguishes stable-but-wrong rounding placement from correct declared staging?
- **Q6.** How is elective dependence declared (F5, F14), and does an open choice block cleanly?
- **Q7.** *(v2 broadened, governance check 1 + adversary attack 6.)* Fresh-reader recovery across **every artifact kind represented by F1–F14** — explicitly including output identity, field mappings, and cross-form bridge declarations, not just computation bodies.
- **Q8.** What must pins carry for explanation walking — do it0's pin roles earn their place?
- **Q9.** Does it0's `derived-publication` act kind plus final run record hold up, or does the interruption window force a start/completion record pair? Draft the act and record shapes the design implies. *(v2 guardrail, governance check 6.)* This evaluates publication vocabulary and record timing only; it must not resolve the reserved T1 authority construction beyond the existing instrument framing.
- **Q10.** Are derived-finding and record IDs deterministic in fixture mode (portability requirement)?
- **Q11.** *(v2, governance checks 3/5.)* Are the design's kinds **citizens**? Draft schema-level shapes for every citizen, act, and record kind the design proposes (rule artifact, parameter declaration, package/adoption envelope, publication act, derivation record); every drafted instance names its schema version; include at least one negative validation example — a label/id or prose/id mismatch — if the schema can express the distinction.

## Out of scope for iteration 1

Credits, dependents, QDCGT worksheet, 1099-DIV/dividend content beyond F3a's threshold framing, state rules, migrations beyond F10(b)'s naming exercise, generators. The charter grows only by a new charter. The rival design (it2) answers the same questions on the same fixtures.

## Evidence expected

Drafted artifacts for F1–F9 and F11–F14; the F10 paper exercise; schema shapes per Q11 with instances naming versions and one negative validation example; evaluator with double-run, shuffled-order, and F13 stage-divergence runs; examination note answering Q1–Q11 with paths, negative results included.
