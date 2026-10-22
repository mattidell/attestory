# P1 — first account for one continuing borrowing

## Actions I will take

1. Describe the reports and the borrowing in terms a person can recognize,
   including what would make them separate loans, a correction, or a duplicate.
2. Propose a small set of ordinary confirmations and say exactly what each
   answer establishes, including when the person cannot tell, skips, or later
   withdraws an answer.
3. Keep report facts, borrowing and home circumstances, and return-wide inputs
   in their proper scopes. In particular, never let matching values or a
   subject label borrow another report's support.
4. Compare bounded ways the application might support the full-deduction
   branch's year-long debt premise, without turning two dated Box 2 values into
   an invented average or asking the person for a tax verdict.
5. Walk through paper cases, name the product choices with real tradeoffs, and
   recommend a direction for owner feedback before choosing software
   mechanisms.

This is increment A only. The current question is what account would make the
case intelligible and defensible; it is not yet a decision about recording,
transport, rules, schemas, or a production path.

## The person-facing account

Imagine two Forms 1098 for the same tax year. One came from the company that
collected payments earlier in the year; the other came from the company that
collects them now. The person recognizes one home loan that remained in place
through the change. The reports can have different Box 1 interest amounts and
different dated Box 2 principal observations. They are still two reports, and
each amount remains tied to the report that states it.

The account should let the person say, in ordinary terms: “These reports
concern the same borrowing I continued to owe; the company servicing it
changed.” It should not ask them to prove the relationship through an outside
institution, and it should not infer the relationship from a similar lender
name, account string, property address, amount, or date. Those clues can help a
person recognize a report, but they do not establish that two obligations are
one.

The relationship is different if the first borrowing was paid off and replaced
by a refinance, if the reports concern two loans on the same home, or if one
report corrects or duplicates the other. A corrected report replaces the
earlier report's information for that report identity; it is not another
interest amount to add. A duplicate is not a second contribution. If the
person cannot tell which situation applies, the reports stay separate and the
combined favorable result remains unresolved. The account does not make the
documents' labels decide for the person.

This is a statement about the person's recognition of the obligation and the
reports' relationship. It does not say that the interest is deductible, that
the debt fits a limit, or that the reports include every relevant home debt.
Those are separate questions for the application to explain.

## Ordinary confirmations and their meanings

The smallest useful meaning appears to include a claim about the continuing
borrowing, a link from each report to that borrowing, and a bounded inquiry
about other secured debt. These are distinct claims, not a prescription for
three screens, three answers in sequence, or three stored records. The person
could answer them together if the interaction remains clear. These are
proposals, not accepted policy.

| Confirmation in ordinary language | What an affirmative answer means | What it does not establish |
| --- | --- | --- |
| “Did you continue to owe the same original home borrowing through the change in the company handling payments, without paying it off and replacing it with a new loan?” | The person recognizes a continuing obligation rather than a refinance or separate borrowing. | Which report is accurate, whether the reports cover non-overlapping periods, or whether all relevant debt is represented. |
| “Do these named reports show interest paid on that same continuing borrowing?” | The person links each named report to the recognized borrowing. The link applies only to those reports. | That reported amounts agree, that either report's other answers support the other, or that the borrowing qualifies for a tax treatment. |
| “During 2025, did you have any other borrowing secured by your main home or a second home, besides the borrowing represented here?” | A “yes” identifies debt outside this main-home-only calculation boundary; “no” is the person's ordinary account that there was no such additional secured borrowing. | A complete inventory, debt classification, balance history, or a tax conclusion. It does not ask for institution-verified evidence. |

The person's answers could be represented as “same continuing borrowing,”
“not the same borrowing,” “cannot tell,” or unanswered for the relationship;
each named report may be linked, not linked, or unresolved; and the debt
coverage answer may be yes, no, cannot tell, or unanswered. “No” to the first is not
the same as “cannot tell”: a known refinance or second loan is a contrary
relationship; uncertainty supplies no relationship. No answer supplies no
support. Withdrawal removes the person's current support and returns the
affected relationship to unresolved; it does not silently assert the opposite.
Withdrawal of the other-borrowing answer also removes its current support; it
does not mean there was no other debt.

The question wording should avoid making “same loan” depend on the lender's
identity. A servicing change can leave the underlying obligation in place;
conversely, the same lender can issue a new borrowing. If the person cannot
distinguish a servicing change from a payoff and replacement, that is a useful
unresolved outcome, not a reason to guess.

## Keep the scopes separate

Report, borrowing, and return are scopes of assertions and evidence, not
permanent properties of a question topic. The answer to “who paid this
report's interest?” is report-local. A different assertion—“our filing unit
paid all interest on this borrowing during 2025”—could legitimately cover both
reports once each report has an explicit link to that borrowing. The first
does not become shared because the answer values happen to match; the second
is intentionally shared because its meaning and named subject cover both.

The paper account distinguishes:

| Scope | Examples | How support attaches |
| --- | --- | --- |
| **Report-local** | Each report's Box 1 amount; each dated Box 2 balance and Box 3 origination date; who paid that report's interest; report correction or duplicate status. | The exact report and its own source and answer history. Raw amounts and dates remain tied to the report. A value or answer from A cannot support B merely because it matches. |
| **Borrowing/home-wide or otherwise explicitly shared** | Whether named reports concern one continuing obligation; use of that borrowing; an assertion that the filing unit paid all interest on the borrowing in the year; whether the borrowing is secured by the identified main home. | A claim explicitly about the named borrowing or group of linked reports, with that scope made clear. It may cover both reports without duplicate answers. It cannot supply report-specific values or an answer whose meaning differs by report. |
| **Return-wide** | Filing status and other facts whose meaning applies to the return as a whole. | The current return's support, not either report's answer. Filing status was correctly return-wide in P0; it must not be misread as report-local merely because a report result consumes it. |

The same-loan link does not by itself authorize every circumstance to be
shared. The question's actual meaning sets the scope. “Who paid this report's
interest?” is local; “our filing unit paid all interest on this borrowing in
2025” can cover both linked reports if that is what the person means. No
duplicate answer is needed just because a current storage shape might key
answers by statement. In either case, the support needs to name its scope and
the linked reports it covers. P0's equal-value pin reuse was accidental
transport of A's evidence into B's result, not such a scoped shared assertion:
it did not establish that the assertion was meant to cover both reports or
that B depended on the right evidence. If a report has a missing or contrary
answer whose meaning is report-specific, a shared assertion cannot fill it.
Likewise, report B's published result is not independently supported if its
actual pins still point to report A's Box 2, Box 9, or ordinary answers. P0's
agreeing-value control proved exactly that failure: the B-labeled reason used
A's report-local observations and all nine A answers. Equal values do not
repair wrong authority or correction dependencies.

The existing family closure says whether all furnished Forms 1098 Box 1
amounts have been recorded. It does not say all relevant home debt has been
identified, or that listed reports share a loan. Publication 936 states that
the relevant acquisition-debt limits apply to the combined mortgages on the
main and second homes. This increment excludes a second-home calculation, so
a “yes” to the other-secured-debt question reaches a boundary: the application
cannot silently assume the other home is irrelevant or calculate the combined
limit from the main-home reports alone. It should leave the full-deduction
branch unresolved and explain that this account does not cover the additional
home debt. A “cannot tell” or no answer also leaves coverage unknown. The
question asks for an ordinary circumstance, not detailed institutional proof.
([2025 IRS Publication 936, “Fully deductible interest”](https://www.irs.gov/pub/irs-prior/p936--2025.pdf))

## The debt proposition and ways to support it

For the bounded full-deduction branch, the P0 source review identifies a
whole-year proposition: the acquisition-debt balance relevant to this
borrowing must be represented as within the applicable limit throughout the
year, and the applicable debt cannot be evaluated as if other relevant debt
does not exist. The current one-report rule states its own premise that Box 2
stands for the acquisition-debt balance throughout the year. That is a
disclosed single-report premise, not authority to extend it to two dated
observations.

Two Box 2 values are snapshots taken on report dates. Adding them treats one
continuing balance as two debts. Choosing the smaller, larger, later, or
earlier one does not establish the balance for the rest of the year. Their
average is not the year's average balance method. The reports also do not
automatically establish that no other relevant home debt existed. A general
average-balance, debt-allocation, or proration calculator is outside this
bounded case.

Two concrete candidates remain open:

| Possible basis | Value | Cost and risk | Work it displaces |
| --- | --- | --- | --- |
| **Factual-basis candidate:** For the bounded post-December 15, 2017 debt class, ask: “During 2025, was the amount owed on the home-purchase or improvement mortgages on your main home and second home ever above the $750,000 limit ($375,000 if married filing separately)?” A “yes” routes out of this full-deduction branch; a “no” is the person's direct year-long balance assertion the application uses for that limit comparison. Ask separately whether any other mortgage or home-equity borrowing was secured by either home; a “yes” is outside this main-home-only calculation. | Names the period, combined homes, threshold, and consequence for this bounded debt class. It asks about an amount owed, not “are you eligible?” | It is demanding recall. The person may not know which borrowing falls in this debt class or whether the amount ever crossed the threshold. A “no” still relies on the person's debt inventory and classification; no separate year-long balance history is supplied. Debt in another acquisition-date class needs its applicable limit and is outside this proposed question. | Avoids a general average-balance or allocation calculator, but places the whole-year fact burden on the person. |
| **Disclosed-assumption candidate:** Tell the person: “For this limited estimate, we assume the largest Box 2 balance on the reports you linked was the highest balance of the relevant borrowing at every point in 2025, and that no other qualifying mortgage debt on your main or second home needs to be added. We compare that assumed ceiling with the filing-status limit.” The application would use the larger observation as an assumed ceiling, not as a legal rule. | Makes a precise, visible application assumption and avoids implying either dated observation is itself the annual balance. | The reports do not establish that the larger snapshot bounded unobserved periods, nor that no other home debt existed. No evidence currently justifies that assumption; disclosure makes it visible but does not make it sound. The second-home possibility remains a boundary even if the person affirms the loan link. | Avoids collecting a balance timeline and avoids selecting a favorable date, but accepts a potentially false application premise. |

Neither candidate is established by P0. The first would be a person's direct
assertion about a year-long, combined-home circumstance, but P0 provides no
evidence that people can reliably answer that tax-shaped question. The second
is explicit, but the current evidence does not justify its “largest observed
balance was the ceiling” assumption or its coverage of other homes. The exact
missing evidence is a basis for the balance over the unobserved portions of
2025 and whether other relevant main- or second-home debt existed. Until the
owner chooses a bounded basis, or evidence supports one, this case cannot
claim the full-deduction branch from two Box 2 values alone. No larger/smaller
or dated observation is a tax rule.

Neither should be phrased as “Are you eligible to deduct all the interest?”
That asks the person to supply the tax conclusion the application is meant to
explain. The application must state the branch and premise it applies and why;
absent support, it should leave the result unresolved.

## Paper examples

1. **Servicer changes; same obligation recognized.** Report A says $8,000 Box
   1 and $240,000 Box 2 on its date. Report B says $3,000 Box 1 and $220,000
   Box 2 on its date. The person identifies one continuing original borrowing
   and links both reports. The account preserves $8,000 and $3,000 separately,
   and preserves each balance with its report date. It does not add the
   balances or decide that $220,000 or $240,000 held all year. The full-
   deduction branch remains dependent on the selected whole-year basis and
   whether other relevant debt existed.
2. **Concurrent loans on one home.** Two reports have similar lender names
   and addresses, but the person says they concern two obligations that
   existed at the same time. They are independent loans secured by the same
   home, not one continuing borrowing. No shared circumstance or combined
   favorable result follows from matching details. This account does not
   calculate their combined treatment.
3. **Refinance.** The person says the first borrowing was paid off when a new
   borrowing replaced it. That is a refinance/replacement, not the servicing
   transition in this bounded case. The reports do not join as one continuing
   obligation under this account; refinance treatment is excluded here.
4. **Possible correction or duplicate.** The person recognizes one report as
   corrected, or as a duplicate, rather than a second report for interest
   paid. It replaces or is excluded as appropriate to the report identity;
   the account does not sum both copies. If they cannot tell, the duplicate
   relationship is unresolved and no favorable extra amount is counted.
5. **Same link, conflicting report information.** The person says both reports
   concern the same borrowing, but one report's source or answer indicates a
   different use or a separate loan. The application must expose the concrete
   conflict and ask which circumstance is true or leave it unresolved. The
   link does not erase report evidence, and the report's label does not erase
   the person's link.
6. **One report missing an answer.** If the missing item is genuinely a
   borrowing-wide circumstance supported for the identified borrowing, the
   explicit shared answer may cover it. If it is who paid that report's
   interest, or another report-local matter, the other report's answer cannot
   fill the gap. The result then says which report-local information is
   missing and what calculation it prevents.
7. **Amount-only correction reconciled.** A corrected Box 1 amount is
   reconciled as the successor for report B, with report identity and the
   same-borrowing relationship unchanged. The new amount replaces the old
   amount support; it does not by itself contradict the continuing-loan
   account. If the correction's effect on currentness or which report is
   controlling is uncertain, do not treat it as an amount-only change yet.
8. **Correction changes the relationship.** If the corrected report shows a
   different loan or otherwise changes the material relationship, the
   cross-report account needs renewed clarification and affected support is
   unresolved. A correction flag alone does not mean the relationship changed.
   Withdrawing the person's link also ends its current support without
   asserting the reports are separate. Increment B must identify which
   current assertions and results depend on the changed relationship.
9. **Late report after a set was closed.** A newly added report means the
   current report set must be considered again. A previously affirmed
   borrowing account might still describe the same loan, but its membership
   cannot silently expand to a newly added report. The person must link that
   report explicitly, and any closure behavior must protect against both
   omission and double counting. This is a lifecycle choice for the connected
   design.

## Choices for owner feedback

These are the material choices left by increment A; they are proposals, not
accepted decisions.

| Choice | Recommendation | Value | Cost/risk and displaced work |
| --- | --- | --- | --- |
| What the person confirms about one borrowing | Require a clear claim that this is one continuing obligation and explicit links from the named reports. These are distinct meanings, not necessarily separate questions or records. Treat cannot-tell and no answer as unresolved; a known non-match as contrary. | Makes the relationship visible without using names, amounts, or institutional verification as identity. | Requires an account and explicit report scope. Avoids automatic matching and a broader loan identity system. |
| Which facts may be shared | Let the assertion's meaning determine scope: raw amount/date facts stay report-local; a report-specific payer answer stays local; an assertion that the filing unit paid all interest on the borrowing may cover both linked reports. Keep filing status return-wide. | Preserves legitimate shared facts without allowing accidental pin reuse or redundant questions. | Requires clear scope and correction dependencies. Avoids making scope a permanent property of an answer topic or requiring duplicate answers because of storage keys. |
| How the full-year balance premise is supported | Decide between the concrete factual question and the explicit largest-observed-balance assumption above; neither is currently justified as sufficient. A “yes” to other main/second-home debt places the case outside this bounded calculation. | Names the missing year-long and combined-home coverage instead of treating two dates as a year. | The factual question may be too tax-shaped; the assumption lacks evidence about unobserved periods and other debt. Avoids a general debt-history and proration calculator. |
| What defeats or changes the account | A known second concurrent loan or refinance is outside this account. An amount-only correction reconciled as successor does not by itself change the relationship; uncertain currentness pauses support; a correction that changes the material relationship or withdrawal requires clarification. | Changes only the affected support and avoids treating every corrected form as a contrary loan relationship. | Requires B to distinguish correction states and their dependencies. Avoids invalidating all answers for an amount-only change or preserving them after a material relationship change. |

My recommendation is to proceed with explicit report links and assertions
whose scope follows their meaning, while preserving report-local source
amounts and dates. The remaining owner choice is whether this narrow case
should accept the person's direct year-long combined-home balance assertion,
or adopt a disclosed largest-observed-balance ceiling assumption despite the
missing support described above. My recommendation is to accept neither as
established today: the person-facing factual question may be too tax-shaped,
and the disclosed assumption is not substantiated by the reports. Keep the
full-deduction result unresolved unless the owner chooses that explicit
assumption or further evidence supplies year-long balance and other-home
coverage. This leaves a precise choice rather than asking for generic proof
or opening a general debt calculator.

## Evidence ceiling and handoff

This account uses the committed P0 tax-source review, current path inspection,
synthetic diagnostic observations, and independent review/recheck. P0 showed
that two-report save/review and saved-reader paths are currently singleton;
that differing Box 2 values leave the unkeyed scalar absent; and that agreeing
values still do not make B's reason consume B's report-local observations and
answers. This design corrects the account of that limitation but does not
demonstrate a new path.

The answer meanings and paper behavior here are proposed design. No
same-borrowing affirmation has been obtained, no whole-year debt premise has
been established for a real or synthetic account, and no production feasibility,
tax verdict, recording mechanism, schema need, correction contract, or saved
explanation behavior is proven. Return to the Foreman for feedback on these
actual choices before developing increment B or selecting a mechanism.
