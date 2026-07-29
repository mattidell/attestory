# Entry Loop Usability Criteria

Status: **accepted by the owner, 2026-07-29** —
`docs/reviews/2026-07-29-entry-loop-synthetic-track0-owner-acceptance.md`. That
note records what the acceptance covers and what it does not: the last formal
review verdict on this document is the `NOT READY` at `319521c`, whose sole
remaining finding was closed at `1e48443` without a further review cycle.

This document defines the usability criteria a guided entry loop must meet and
the procedure for scoring a matrix cell against them. It was written before any
entry surface was built, ensuring the evaluation sets the bar rather than
conforming to an implementation.

## The Loop Criteria

The entry loop consists of five steps. An entry surface must satisfy the
following criteria for a person interacting with it. All examples are grounded
in the W-2 fact family.

For criteria 3.2, 3.3, and 4.2, the fixed **W-2 evaluation sets** are:

- **Expected-impact set:** Form 1040 lines 1a (wages), 9 (total income), 11
  (adjusted gross income), 15 (taxable income), and 16 (tax).
- **Untouched comparison set:** Form 1040 lines 2b (taxable interest), 3a
  (qualified dividends), 3b (ordinary dividends), and 12 (deduction).

These sets are scoring vocabulary, not a surface layout or explanation schema.
The evaluation fixture must make every expected-impact member change when the
fixture's W-2 Box 1 value is entered or corrected and must leave every
untouched comparison member unchanged. The surface may present the evidence in
any form, but the change status of every named member must be observable. If
the fixture cannot produce that condition, the evaluation is not runnable.

### 1. Know what is missing
What must a person be able to tell about the gap between where their return is and where it needs to be?
- **Criterion 1.1 (Mechanical):** The surface must present a finite, enumerated list of specifically missing documents or facts (e.g., "Missing W-2 from Employer X") required to complete the return.
- **Criterion 1.2 (Mechanical):** The list of missing facts must serve as the primary navigational guide through the entry session, not merely as a diagnostic report beside a separate form. To pass, every missing item must itself provide, or contain, an action that takes the evaluator directly to its corresponding input; the evaluator must not have to find that input independently in another form.
- **Criterion 1.3 (Judgement):** A person can state, without guessing, whether they currently have all the physical or digital documents needed to resolve the missing facts.

### 2. Enter a fact
What must a person be able to tell about a field *before* they type in it?
- **Criterion 2.1 (Mechanical):** Every input field must explicitly name the source document and the exact box or line it corresponds to (e.g., "W-2 Box 1: Wages, tips, other comp.").
- **Criterion 2.2 (Mechanical):** Every input field must state why the fact is being asked for and its role in the return. At minimum, field-attached text must name the immediate return destination and the completion purpose (for example, that W-2 Box 1 feeds Form 1040 line 1a and resolves the missing wages needed to compute income); a bare "required" label does not pass.
- **Criterion 2.3 (Judgement):** A person can state, without guessing, what a correctly formatted answer looks like (e.g., whole dollars vs. cents) before typing it.

### 3. See it land
What must they be able to tell *after* typing a fact?
- **Criterion 3.1 (Mechanical):** The surface must provide an immediate visual indication that the entered fact (e.g., W-2 Box 2 withholdings) was accepted by the system.
- **Criterion 3.2 (Mechanical):** After the W-2 Box 1 fact is accepted, the surface must explicitly show the changed status and resulting value of every member of the expected-impact set.
- **Criterion 3.3 (Mechanical):** After the W-2 Box 1 fact is accepted, the surface must explicitly show every member of the untouched comparison set as unchanged.

### 4. Correct an entered fact
Can they find a fact they already answered, change it, and understand the result?
- **Criterion 4.1 (Mechanical):** A previously entered fact (e.g., W-2 Box 1) must be locatable and navigable from the main loop surface without requiring a full restart of the session.
- **Criterion 4.2 (Mechanical):** Changing an answered W-2 Box 1 fact must immediately update every member of the expected-impact set to its expected post-correction value, while every member of the untouched comparison set remains unchanged.
- **Criterion 4.3 (Judgement):** A person can easily differentiate between an empty missing fact and an answered fact that needs correction.

### 5. Know the return is complete
What does "done" have to look like to count?
- **Criterion 5.1 (Mechanical):** The surface must provide a singular, unambiguous state indicating that zero facts are missing and the return is fully computed.
- **Criterion 5.2 (Mechanical):** When criterion 5.1 holds, the surface must stop presenting any fact as missing, stop prompting for further required-fact entry, and display a review/done state that is visibly distinct from the guided-entry state. Previously answered facts must remain reachable for correction.
- **Criterion 5.3 (Judgement):** A person reaching the "complete" state has no doubt that their entry task is finished and they do not need to look for additional forms.

## Relationship to ADR-0046 (Presentation Surface Contract)

ADR-0046 was written for a surface that only displays data, while the entry
loop creates data. Every carried-over rule below is an additional Mechanical
criterion: each evaluator scores it Pass or Fail under the same aggregation
rule as the numbered Mechanical criteria.

- **Carries over: Sub-section blast containment.** An invalid entry in one field must not hide or invalidate correct sibling fields, and the surface must not show a value whose evidence includes that invalid or not-yet-accepted entry.
- **Carries over: Accessibility baseline.** Normal text must have at least a 4.5:1 contrast ratio; large text (at least 18 point, or 14 point bold), visible control boundaries, and focus indicators must have at least a 3:1 ratio. The entry loop must expose a `main` landmark and a named form landmark; every action must be reachable with Tab and Shift+Tab and operable with the control's standard Enter or Space key; and keyboard focus must remain visible through `:focus-visible`.
- **Carries over: No derived value from invalid or blocked input.** No derived or diagnostic value fed by an invalid, blocked, or not-yet-accepted entry may reach the DOM.
- **Carries over: Fail-loud.** Any validation failure (e.g., malformed input) must produce a visible on-page signal, never console-only.
- **Carries over: Blanket redaction.** We do not echo rejected values into visible error text, to prevent leak channels.
- **Does not carry over: Zero-authority projection.** Entry surfaces inherently hold the authority to emit `act-contribution.v1` events. They are not zero-authority read-only views.
- **Does not carry over: Honest blocking (Absence-of-key).** While read-only surfaces block on missing keys and show no value, an entry surface *must* render a field specifically because the key is missing, in order to collect it.

## Weakest Criteria & Omissions

- **Weakest Point:** Criterion 3.3 deliberately proves blast containment only across the fixed untouched comparison set. It does not claim to predict or display every value a person might expect to change; that broader requirement remains omitted so the retained criterion is mechanically scoreable.
- **Omitted Criterion:** I wanted to write a criterion enforcing that a user understands *how* a derived value was calculated from their entry (e.g., how W-2 Box 2 affects the final refund). However, this could not be made sharp enough; explaining the US tax code's derivation logic inside an entry loop is an unbounded requirement that cannot be mechanically checked without knowing the specific explanation UI shape.

## Scoring Procedure

- **Dependencies for running the evaluation (not confirmed by Track 0):** Track 1 must establish four dependencies: (1) a synthetic workspace can be seeded with every required non-W-2 fact so W-2 is the only missing family; (2) the entry surface can be served at a URL and can send contributions through the admission path; (3) the surface makes the fixed W-2 evaluation sets and the zero-missing, fully computed state observable; and (4) the evaluation fixture makes every expected-impact member change when the fixture's W-2 Box 1 value is entered or corrected and leaves every untouched comparison member unchanged. The evaluation does not run until all four dependencies are demonstrated. Naming them here does not confirm them.
- **Who evaluates:** Exactly two agents evaluate independently and do not confer before filing their scores. Evaluator A uses the Builder brief: exercise every criterion as an explicit system outcome and preserve the action/result transcript. Evaluator B uses the Reviewer brief: approach the same evidence pack without implementation context, attempt the five steps from the surface's own guidance, and record every point at which the surface requires inference. Both score every criterion; the distinct briefs, rather than an interchangeable role example, are the required difference.
- **What they are given:** Once the run dependencies are met, both evaluators receive the same seeded synthetic workspace, entry surface URL, synthetic W-2 source data, fixed W-2 evaluation sets, criterion score sheet, and instructions to preserve their raw transcripts.

**Aggregation and cell-pass rule:**

1. Each evaluator scores every criterion Pass or Fail. No third value at the
   evaluator level.
2. A split becomes **Disputed** at aggregation.
3. A cell passes if and only if every mechanical criterion is Pass/Pass, and no
   judgement criterion is Fail/Fail.
4. A **Disputed mechanical** criterion fails the cell.
5. A **Disputed judgement** criterion does not fail the cell. It escalates to
   the owner with both rationales.

- **Who decides:** The aggregation rule produces the cell verdict. The owner receives that verdict, both raw transcripts, the aggregated Pass/Fail/Disputed matrix, and the rationales for every Disputed or Failed criterion; the owner decides whether to accept the evidence and resolves each escalated judgement dispute.
