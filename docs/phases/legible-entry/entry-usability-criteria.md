# Entry Loop Usability Criteria

This document defines the usability criteria a guided entry loop must meet and the procedure for scoring a matrix cell against them. It was written before any entry surface was built, ensuring the evaluation sets the bar rather than conforming to an implementation.

## The Loop Criteria

The entry loop consists of five steps. An entry surface must satisfy the following criteria for a person interacting with it. All examples are grounded in the W-2 fact family.

### 1. Know what is missing
What must a person be able to tell about the gap between where their return is and where it needs to be?
- **Criterion 1.1 (Mechanical):** The surface must present a finite, enumerated list of specifically missing documents or facts (e.g., "Missing W-2 from Employer X") required to complete the return.
- **Criterion 1.2 (Mechanical):** The list of missing facts must serve as the primary navigational guide through the entry session, not merely as a diagnostic report beside a separate form.
- **Criterion 1.3 (Judgement):** A person can state, without guessing, whether they currently have all the physical or digital documents needed to resolve the missing facts.

### 2. Enter a fact
What must a person be able to tell about a field *before* they type in it?
- **Criterion 2.1 (Mechanical):** Every input field must explicitly name the source document and the exact box or line it corresponds to (e.g., "W-2 Box 1: Wages, tips, other comp.").
- **Criterion 2.2 (Mechanical):** Every input field must state why the fact is being asked for and its role in the return.
- **Criterion 2.3 (Judgement):** A person can state, without guessing, what a correctly formatted answer looks like (e.g., whole dollars vs. cents) before typing it.

### 3. See it land
What must they be able to tell *after* typing a fact?
- **Criterion 3.1 (Mechanical):** The surface must provide an immediate visual indication that the entered fact (e.g., W-2 Box 2 withholdings) was accepted by the system.
- **Criterion 3.2 (Mechanical):** The surface must explicitly show which derived values or subtotals changed as a result of the entered fact (e.g., total tax liability).
- **Criterion 3.3 (Mechanical):** The surface must explicitly show which derived values or subtotals did *not* change, if the user might reasonably expect them to (blast containment).

### 4. Correct an entered fact
Can they find a fact they already answered, change it, and understand the result?
- **Criterion 4.1 (Mechanical):** A previously entered fact (e.g., W-2 Box 1) must be locatable and navigable from the main loop surface without requiring a full restart of the session.
- **Criterion 4.2 (Mechanical):** Changing an answered fact must immediately update all dependent derived values and subtotals.
- **Criterion 4.3 (Judgement):** A person can easily differentiate between an empty missing fact and an answered fact that needs correction.

### 5. Know the return is complete
What does "done" have to look like to count?
- **Criterion 5.1 (Mechanical):** The surface must provide a singular, unambiguous state indicating that zero facts are missing and the return is fully computed.
- **Criterion 5.2 (Mechanical):** The transition to the "complete" state must visually shift the surface from a guided-entry posture to a review or submission posture, blocking further prompted entry of required facts.
- **Criterion 5.3 (Judgement):** A person reaching the "complete" state has no doubt that their entry task is finished and they do not need to look for additional forms.

## Relationship to ADR-0046 (Presentation Surface Contract)

ADR-0046 was written for a surface that only displays data, while the entry loop creates data. The following principles apply or do not apply:

- **Carries over: Sub-section blast containment.** An invalid entry in one field must not hide or invalidate correct sibling fields.
- **Carries over: Fail-loud.** Any validation failure (e.g., malformed input) must produce a visible on-page signal, never console-only.
- **Carries over: Blanket redaction.** We do not echo rejected values into visible error text, to prevent leak channels.
- **Does not carry over: Zero-authority projection.** Entry surfaces inherently hold the authority to emit `act-contribution.v1` events. They are not zero-authority read-only views.
- **Does not carry over: Honest blocking (Absence-of-key).** While read-only surfaces block on missing keys and show no value, an entry surface *must* render a field specifically because the key is missing, in order to collect it.

## Weakest Criteria & Omissions

- **Weakest Point:** Criterion 3.3 ("Show what did *not* change") is the weakest criterion. It is difficult to mechanically enforce because a system cannot easily predict every derived value a user *expects* to change. It relies heavily on surface-level heuristics.
- **Omitted Criterion:** I wanted to write a criterion enforcing that a user understands *how* a derived value was calculated from their entry (e.g., how W-2 Box 2 affects the final refund). However, this could not be made sharp enough; explaining the US tax code's derivation logic inside an entry loop is an unbounded requirement that cannot be mechanically checked without knowing the specific explanation UI shape.

## Scoring Procedure

- **Who evaluates:** Two distinct agent evaluators (e.g., a standard Builder agent and a specialized Advisor/Reviewer agent). Their different system prompts and operational constraints ensure varied interaction approaches that mimic different user mental models.
- **What they are given:** A synthetic workspace seeded with all facts except the target family (e.g., seeded with everything except W-2). They are provided the entry surface URL and the synthetic source document data (e.g., a synthetic W-2 JSON) to enter.
- **What happens to disagreement:** Disagreement is preserved as signal. If Evaluator A passes a criterion and Evaluator B fails it, the criterion is marked as "Disputed" along with the rationales from both evaluators. It is not averaged into a numerical score.
- **What a pass is:** A cell passes only if *all* mechanical criteria receive a "Pass" from both evaluators (no fatal failures). Judgement criteria must not receive any "Fail" verdicts (Disputed is acceptable for escalation, but a Fail is fatal).
- **Who decides:** The owner makes the final decision. They are presented with the evaluators' raw transcripts, the scoring matrix (Pass/Fail/Disputed for each criterion), and the specific rationales for any Disputed or Failed criteria.
