# P1 — connected account for one continuing borrowing

## Actions I will take

1. Describe the reports and borrowing in terms a person can recognize,
   including servicing change, refinance, concurrent loans, correction, and
   duplicate cases.
2. Define the ordinary claims and exact report links, including the numeric
   balance ceiling and separate other-debt coverage answer.
3. Keep report facts, explicitly scoped borrowing/home claims, and return-wide
   inputs separate; matching values never borrow another report's support.
4. Trace each input from its source and current support through keyed admission,
   per-report results, the one-loan limit comparison, the Box 1 subtotal, and a
   saved group explanation.
5. Work the correction, withdrawal, changed-filing-status, contradiction,
   late-report, no-report, and single-report cases; compare existing patterns,
   name the integration cost, and propose one discriminating probe if needed.

This connected paper design follows the Foreman's provisional P1 direction.
It is a candidate account and integration path, not an accepted contract or
production specification.

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

The account needs the person to identify a continuing borrowing, associate
each report with it, give a numeric ceiling on what was owed on that borrowing
during 2025, and answer separately whether other borrowing was secured by the
main or second home. These are distinct meanings, not a prescription for
separate screens or one record per answer. The person could answer them in one
clear interaction. This is a proposal, not accepted policy.

| Ordinary statement or answer | What it means | What it does not establish |
| --- | --- | --- |
| “Did you continue to owe the same original home borrowing through the change in the company handling payments, without paying it off and replacing it with a new loan?” | The person recognizes a continuing obligation rather than a refinance or separate borrowing. | Which report is accurate, whether the reports cover non-overlapping periods, or whether all relevant debt is represented. |
| “Do these named reports show interest paid on that same continuing borrowing?” | The person links each named report to the recognized borrowing. The link applies only to those reports. | That reported amounts agree, that either report's other answers support the other, or that the borrowing qualifies for a tax treatment. |
| “What is a dollar amount you are confident the balance on this borrowing did not go above at any point during 2025? It can be higher than the exact highest balance.” | A person-confirmed numerical ceiling for the identified borrowing over the year. It is an upper bound, not a claim that this exact amount was owed throughout or that it is the precise maximum. | The tax category, applicable limit, another borrowing's balance, or independent verification. |
| “During 2025, was any other mortgage or home-equity borrowing secured by your main home or a second home?” | “Yes” means known additional secured debt and reaches this design's coverage boundary. “No” means the person says there was no other such borrowing. | A detailed debt inventory, legal classification, or a tax conclusion. It does not ask for institution-verified evidence. |

The relationship can be affirmed, denied, unresolved because the person
cannot tell, or absent because no answer was given. Each report link can have
the same states. A known refinance or concurrent second loan is contrary; it
is not the same as cannot-tell. The numeric ceiling has a value, cannot-tell,
unanswered, or withdrawn state. The other-debt inquiry has yes, no,
cannot-tell, unanswered, and withdrawn states. Known additional debt makes
this bounded calculation unsupported; unknown, unanswered, or withdrawn
means coverage remains unresolved. Withdrawal ends current support and does
not assert the opposite. None of these answers requires institutional
verification.

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
main and second homes. This design excludes a second-home calculation. A
“yes” to other secured borrowing means known debt outside the supported
coverage; the application cannot silently treat it as zero or calculate the
combined limit from these main-home reports alone. “Cannot tell,” no answer,
or withdrawal leaves the circumstance unresolved. A “no” is an ordinary
person affirmation, not a proved inventory. The question asks for a simple
circumstance, not detailed institutional verification. ([2025 IRS Publication
936, “Fully deductible interest”](https://www.irs.gov/pub/irs-prior/p936--2025.pdf))

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

The candidate is one ordinary factual source: the person gives a numerical
upper bound for the balance on the identified borrowing during 2025. The
question is about one debt the person recognizes, not whether a combined set
is qualifying acquisition debt. They can give an amount they are confident
the balance did not exceed, even if they cannot state its exact maximum. The
application separately determines the borrowing's tax category, the filing-
status limit, and how to compare the asserted bound. The person is not asked
to decide a deduction or legal classification.

The application must not silently populate this annual ceiling with either
Box 2 observation, the larger observation, or any other selected date. Box 2
remains a dated report observation. If the person cannot provide a usable
ceiling, the full-deduction branch stays unresolved. The numeric assertion is
an ordinary source accepted by this proposed account; P0 did not observe a
person answer it, and the fact asserted is not independently verified.

The comparison is asymmetric. A ceiling at or below the applicable limit
supports the bounded full-interest branch: if the actual balance never
exceeded that ceiling, it also never exceeded the limit. A ceiling above the
limit proves no excess; it may simply be loose. In that case ask for a tighter
ceiling if the person can give one, otherwise leave this support unresolved.
Do not call it over-limit debt. A dated report principal observation above
the applicable limit is different evidence of an actual balance at that date;
when the report is explicitly linked to this borrowing, it contradicts a
below-limit ceiling and needs reconciliation. Neither a loose ceiling nor an
observation can be converted into an annual maximum by choosing a report date.
After filing status changes, retain the same numeric assertion and compare it
with the new limit: a ceiling now above that limit becomes unresolved unless
tightened; it does not become proof of actual excess. Any threshold-specific
yes/no would have to retain the exact threshold affirmed and cannot transfer.

The separate other-debt answer has its own consequence. “Yes” means the case
has known other main- or second-home debt, which this bounded calculation
does not cover; do not publish a favorable partial deduction or a determined
zero. “Cannot tell,” unanswered, or withdrawn leaves that debt set unknown
and likewise prevents the full-deduction result. Only “no” supplies the
person's ordinary assertion that no other such debt needs consideration. This
is not a general debt-allocation or proration calculator.

This bounded account supports the whole-loan ordinary outcome that the
filing unit paid all reported interest for the identified borrowing, or an
unresolved/unsupported contrary outcome. A known mixed or partial-payment
case is outside scope: do not sum only reports answered “yes,” allocate a
fraction, or treat uncovered interest as zero. Family closure has a separate
scope: a genuinely closed-empty F1098 family means there are no current
furnished Form 1098 Box 1 members and authorizes line8a = 0 even if the person
still has borrowing-account facts. Incomplete or unresolved closure blocks.
An affirmed current membership link to an exact report for which no current
F1098 source is present is a concrete conflict with that empty closure; a
ceiling, other-debt answer, or merely retained borrowing identity is not.

If a threshold-specific yes/no were used instead, the number and context
actually affirmed must be retained. A response to a threshold selected under
one filing status cannot be reinterpreted under another threshold. This
candidate avoids that problem by retaining a numeric ceiling: if filing
status changes, the same amount remains the same factual assertion and the
application compares it with the newly applicable limit. The new comparison
may change the result; the person's past answer does not.

## Connected design: one borrowing account, two report links

This is the smallest paper design that appears to preserve the meaning. It
uses a specific borrowing reference and explicit report membership, without
creating a general mortgage identity system.

| Durable assertion or source | Identity and scope | Current meaning |
| --- | --- | --- |
| Existing Form 1098 facts | Current exact report identity `(payer, statement, tax-year)`; unchanged. | Each source report keeps its own Box 1 amount, dated Box 2 observation, Box 3 origination date, Box 9 count, source evidence and correction lineage. Amounts and observations never move to the borrowing account. |
| Borrowing reference | One opaque reference for the continuing obligation, created explicitly in the person's workspace and retained while that obligation is current. No value is inferred from lender, address, amount, dates, or report order. | Gives the relationship and genuinely borrowing-wide assertions one subject. This is local to this feature and year, not an identity service or a universal mortgage model. |
| Continuing-borrowing assertion | `borrowing reference + tax year`, with the person's response and provenance. | The person says the original obligation continued through the servicing change without being paid off and replaced. Affirmed, denied, cannot-tell, unanswered, and withdrawn remain distinguishable. |
| Report membership link | `borrowing reference + exact report identity`, one current relationship outcome per pair. | Explicitly identifies which report is about this borrowing. Each named report is independently affirmed, denied, unresolved, unanswered, or withdrawn. No report joins because its values match. |
| Annual balance ceiling | `borrowing reference + tax year`, numeric amount, response evidence, actor/time, and correction/withdrawal lineage. | The person confirms this number was not exceeded by the balance on this borrowing during the year. The value is not treated as an exact maximum, a report balance, or a legal classification. |
| Other secured borrowing answer | `return + tax year`, with yes/no/cannot-tell/unanswered/withdrawn and provenance. | Answers whether other mortgage or home-equity borrowing was secured by the main or second home. Yes is known debt outside this calculation; unknown is unresolved. Neither is treated as zero. |

The proposed input shapes are concrete: `continuing-borrowing` is a
borrowing/year answer; `report-membership` is a borrowing/exact-report answer;
`annual-balance-ceiling` is a borrowing/year numeric answer; and
`other-home-debt` is a return/year yes/no/cannot-tell answer. Each answer
finding carries its wording/version, value, identity keys, and correction or
withdrawal lineage. `SourceFact` currently has only one `finding_id`; it
cannot itself pin both a shared answer and a membership link. The proposed
transport therefore needs a declared per-report intermediate finding: its
inputs are the original whole-loan answer finding and that report's current
membership-link finding, and it publishes the answer for that exact report
subject. The report result pins that intermediate finding, whose declared
inputs retain both originals. This is a proposed content path, not a claim
that today's mortgage path already does it. A separate report-local answer
continues to pin its own answer finding directly. No copied value or
equal-valued report answer stands in for either relationship. No external
institutional verification is required; the product must state this is the
person's affirmation.

One submission can collect these related claims together. Conceptual scope
does not require a separate screen or duplicate answer. The person confirms
the same continuing borrowing once, and links each report by identity. A
report-specific question such as “Who paid the interest reported on this
statement?” remains report-specific. A separate assertion, “Our filing unit
paid all interest on this borrowing during 2025,” can support both linked
reports because that exact proposition covers the whole borrowing and year.
The source must retain that shared scope; it cannot be created by copying a
statement-keyed answer or by two equal answer values.

### Scope of every input the current reason consumes

The existing reason rule consumes more than principal. The paper account must
decide the source of each input before any subject result can be trusted.

| Existing input | Candidate scope and source rule |
| --- | --- |
| Box 1 interest and source document | Exact report. These are the amounts and evidence to preserve and later include once in the family subtotal. |
| Box 2 principal, Box 3 date, and Box 9 property count | Exact report observation. A report's values can be compared with the borrowing account for contradiction, but are not loan-wide answers and cannot replace the annual ceiling. |
| `paid-the-interest` | The current wording is explicitly “Who paid the interest reported on this statement?” and stays report-local. A distinct borrowing-wide payment claim may cover both linked reports only if the person affirms that whole-year proposition. Do not treat the old report answer as that claim by matching its fact type. |
| Owns the home; main home shared by the filing unit | About the identified home and return, not automatically about the report. It may support both reports if the person is affirming the same identified home and both report links refer to the same borrowing/home account. The assertion's wording and evidence must say so. |
| Home is collateral; who owes the loan; whether another person owes it | About the identified borrowing. One explicit borrowing-scoped assertion can apply to both linked reports where the claim is truly unchanged; a contrary report-specific fact still requires clarification. |
| What the money paid for; whether this is the original loan; mortgage timing relative to purchase/build/improvement; mortgage credit certificate | Potentially borrowing-wide, but only when the ordinary proposition names this borrowing (and the relevant home/year where needed). Do not infer shared support from a field name or from the continuing-loan link alone. A report-specific or ambiguous answer remains local/unresolved. |
| Filing status | Return-wide. It comes from the current return and is not borrowed from either report. |
| Annual balance ceiling | Borrowing- and tax-year-scoped numeric person assertion. It is compared to the limit selected by the application's tax category and current filing status. |
| Other secured borrowing answer | Return-/home-set-wide for the tax year. Yes reaches the unsupported coverage boundary; cannot-tell, unanswered, and withdrawn leave coverage unresolved. |
| Timing defaults | Only explicit, separately declared “not asked/not relevant” outcomes when the exact timing predicate establishes irrelevance. A missing answer, withdrawal, or stale support is not a default. A former default cannot become current merely because a shared account was withdrawn. |

For a shared assertion to support report B, the link from B to the identified
borrowing must be current, the assertion's own subject and period must include
B, and the consuming rule must receive the assertion's actual finding and
provenance. P0's B-labelled result failed this standard: it pinned A's Box 2,
Box 9, and all nine A ordinary answers even though B-keyed answers with equal
values existed. The proposed design would make shared support explicit and
loan-scoped, while exact report facts remain exact-keyed. The assertion ID,
its evidence and its correction predecessor remain visible in B's support
chain; no A assertion is relabeled as B evidence.

### From answers to the saved Schedule A result

1. **Recognize and record.** The person identifies the continued borrowing,
   provides a numeric ceiling for 2025, answers the separate other-debt
   question, and explicitly links report A and report B. Reports retain their
   existing `(payer, statement, tax-year)` identities. The borrowing reference
   is opaque and never inferred from report contents.
2. **Establish current support.** The current account contains a continuing-
   borrowing claim, two current membership links, the ceiling assertion, the
   other-debt answer, and each report's own current answers. A denial,
   cannot-tell, no answer, withdrawal, or stale report source remains distinct
   and blocks only the affected path. The link does not convert any other
   answer to shared scope by itself.
3. **Admit facts to the run.** A proposed targeted admission exposes
   report-local Box 2, Box 3, Box 9 and report-local answers as keyed
   `SourceFact` rows on the exact report identity. It separately exposes
   current report-to-borrowing link findings and loan-wide assertion
   findings. Since a `SourceFact` has only one `finding_id`, transport must
   use a declared per-report intermediate finding whose input pins are the
   original shared answer and the current link; the resulting report-scoped
   row then has one actual finding to pin downstream. This join/transport is
   proposed, not demonstrated by the existing sale admission. Filing status
   remains a separate return-wide symbol. The ceiling is never emitted under
   the Box 2 symbol.
4. **Evaluate each report's standing and reason.** A subject result remains
   attached to each Box 1 report. Its report-local requirements bind to that
   report's own source keys; genuinely shared requirements bind to the
   explicitly linked borrowing assertion. Any missing B input cannot fall
   through to A's run-wide scalar. Contrary source values block with the
   source and conflict named. The annual ceiling and other-debt boundary
   support the account-level treatment, not a separate debt per report.
5. **Aggregate once.** The existing `family.f1098` v1 closure still means all
   furnished 2025 Box 1 reports were recorded; its already-authorized raw
   authorized multi-member sum includes current Box 1 members once. Closure does not establish that
   every member belongs to this one borrowing. The bounded connected path is
   selected by current connected-account evidence, not report count alone.
   For an active account with one current linked report, it may evaluate that
   one member under the same borrowing-level support; it does not silently
   route to the legacy single-report rule. The bounded aggregate is favorable
   only when the closed report set is exactly covered by explicit links to
   this one borrowing and the other-debt answer is “no.”
   The single successor Schedule A line8a producer must preserve the legacy
   one-report behavior when no connected account exists, and admit the F1098
   collect only in the selected calculation branch. It publishes the family-
   authorized line8a symbol directly; there is no second generic subtotal
   publication. The application compares the one borrowing's numeric ceiling
   once against its determined limit; it does not add Box 2 observations. It
   gates that family sum as the line 8a amount. If another report is unlinked, a
   second borrowing is present, other home debt is known, or coverage is
   unknown, it does not publish a favorable partial sum or a determined zero.
6. **Present and reload.** The saved explanation identifies each report and
   Box 1 amount, its own Box 2/Box 3/Box 9 observations, its current link to
   the named borrowing, and exactly which report-local and shared answers
   supported its result. It shows the numeric annual ceiling as a person
   assertion, the tax category and filing-status limit used, the separate
   other-debt answer, the Box 1 subtotal, and the reason for any unresolved
   result. It states that the ceiling is user-confirmed, not independently
   verified; it does not describe Box 2 as an annual average or silently use a
   selected Box 2 date. A fresh reader associates the explanation with the
   saved ActLog revision and exact report and assertion identities. It must
   explain the group result and both underlying reports, not display only a
   B subject label or one singular report account.

### Changes, closure, and compatibility

- **Correct Box 1 only.** If the corrected amount is reconciled as the current
  successor for the same report identity, it replaces that report's amount
  source. The report link, loan ceiling and loan-wide answers remain current
  because the person did not change those claims. Recompute the subtotal and
  saved result. Do not treat a corrected-report flag alone as contradiction.
- **Correction changes the report relationship or currentness is uncertain.**
  Keep both source records and correction lineage. If it is unclear whether
  the corrected form replaces or adds to the current report, the family
  member set and affected link are unresolved. If the correction indicates a
  different borrowing, end the affected link and require clarification. The
  report's other answers do not transfer to the new report by amount match.
- **Correct or withdraw a borrowing assertion.** A correction names its
  current predecessor and replaces that current claim. Withdrawal ends the
  affirmed loan claim, ceiling, or membership link it targets in the same
  logical save; it does not assert the opposite. Results depending on that
  support become unresolved. Keep a current explicit withdrawn/cannot-tell/
  denied outcome in the account rather than erasing the evidence of this
  path; otherwise a single surviving report could accidentally re-enter the
  legacy favorable route. Do not reactivate a previous favorable finding or
  default. Unrelated report-local answers remain current when their source
  report is unchanged.
- **Remove and re-record a report.** Removing a report from the active family
  ends its current membership link, but does not deny that it once belonged
  to the borrowing. Re-recording a report requires a current report source
  and a new explicit link before the shared account can use it. A matching
  identity or Box 1 amount does not resume a withdrawn link.
- **Add a report after closure.** The new statement changes the current family
  horizon; the closed-empty/closed-members set cannot silently stand for it.
  Record the report-local sources, explicitly link it if it belongs to the
  borrowing, and close the new full report set. A loan-wide claim can remain
  current if its whole-year meaning is unchanged, but it cannot silently add
  the new report to its support set; the link is explicit. If the new report
  concerns another borrowing or cannot be identified, this one-borrowing
  aggregate is unsupported/unresolved, not a favorable partial sum.
- **No reports, one report, excluded debt.** Route selection first checks
  current recorded account assertions and outcomes, not just family member
  count. If no connected-account assertion/outcome has been recorded for this
  current scope, preserve legacy behavior: closed-empty authorizes the
  existing zero, and one report keeps the incumbent single-report path. If
  the person has entered this account, any current affirmative, denied,
  cannot-tell, unanswered, or withdrawn outcome keeps the connected path
  selected for nonempty reports, so a removed/withdrawn member cannot cause
  unsafe singleton fallback. Closed-empty still authorizes line8a = 0 when
  there are genuinely no current furnished Form 1098 Box 1 members; account
  answers alone do not negate family closure. If a current affirmative
  membership link names a report but that report has no current F1098 source,
  treat the closure as contradicted/incomplete and block rather than call it
  empty. With one current linked report, evaluate it under that account's
  support; with one report but a denied, withdrawn, or unresolved link, do not
  fall back to legacy. More
  than the bounded report set, an unlinked member, another borrowing, known
  other secured debt, or unknown coverage is unsupported/unresolved.
  Returning to legacy after starting the connected path requires an explicit
  product operation that clears the current account scope; silently deleting
  its last finding is not such an operation and is not specified here.
- **Current recorded state versus old runs.** Account answers, links, report
  corrections and withdrawals are current recorded assertions at a workspace
  revision. Derived subject results and scoped intermediate findings are
  run-local publications, not new authoritative account assertions. A change
  makes a presentation from the prior revision stale; current review
  association already returns `recalculation-needed` on revision mismatch. A
  new live run recomputes from then-current recorded findings and emits a new
  presentation; it does not rewrite an older saved output. The observed live
  coordinator records the run to its record stream, persists output and
  presentation files, and returns the full publications in-memory. Those are
  run-scoped derived records, not account assertions; this design does not
  assume a later run admits them as current source state or that they survive
  as reusable account state across runs.
- **Filing status changes.** The numeric ceiling remains the same ordinary
  fact. The application recomputes the limit from the current return-wide
  filing status and tax category. If instead a future interaction records a
  threshold-specific yes/no, that assertion must preserve the exact threshold
  and context the person affirmed and cannot be carried to a different
  threshold.
- **Box 2 contradicts the ceiling.** Each Box 2 amount is a dated observation,
  not an annual maximum. If either linked report states a principal greater
  than the person's ceiling, preserve both and flag a material conflict; do
  not discard the form, raise or lower the ceiling automatically, or choose a
  report. Ask the person to reconcile the observation or correct the annual
  ceiling. Until then, the full-deduction branch is unresolved. A Box 2
  observation below the ceiling does not prove the ceiling for the unobserved
  periods.

The single-report path and saved history remain compatible by preserving
their existing meanings. No old one-report finding is silently reinterpreted
as a borrowing-scoped assertion. A legacy single-report workspace retains its
current reader and output; the connected result needs a group-shaped saved
explanation and reader behavior. The published mortgage family v1 authorizes
only `tax.us.2025.schedule-a.line8a`, not a generic raw Box 1 subtotal. A
singleton review, current line 8a
rule, or singular saved reader does not alone require a family successor or
public schema version. Whether existing content can declare the bounded group
path, or a new unpublished/adopted content shape is needed, remains an
implementation decision after this meaning is reviewed.

## Paper examples

1. **Servicer changes; same obligation recognized.** Report A says $8,000 Box
   1 and $240,000 Box 2 on its date. Report B says $3,000 Box 1 and $220,000
   Box 2 on its date. The person identifies one continuing original borrowing
   and links both reports, confirms that the borrowing never exceeded
   $250,000 during 2025, and says there was no other mortgage or home-equity
   borrowing on either home. The account preserves $8,000 and $3,000
   separately, plus both dated principal observations. The application
   compares the confirmed $250,000 ceiling—not $240,000 + $220,000 and not a
   selected report date—with the limit it determines from debt category and
   filing status. The amount remains a person assertion; the forms do not
   verify the ceiling.
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
   borrowing-wide circumstance supported for the identified borrowing, an
   explicit shared answer may cover it. For example, “our filing unit paid
   all interest on this borrowing in 2025” can cover both explicitly linked
   reports. If the missing item is “who paid the interest reported on this
   statement,” the other report's answer cannot fill the gap. The result names
   which information is missing and what calculation it prevents.
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
   asserting the reports are separate. Only results depending on the changed
   link are blocked; unrelated current answers remain available.
9. **Late report after a set was closed.** A newly added report means the
   current report set must be considered again. A previously affirmed
   borrowing account might still describe the same loan, but its membership
   cannot silently expand to a newly added report. The person must link that
   report explicitly, and closure must protect against both omission and
   double counting. The loan-wide ceiling can remain current for its
   whole-year subject, but the new report is not a member until linked.
10. **Reported principal contradicts the ceiling.** The person gives a
    $250,000 annual ceiling, but linked report B states $270,000 on its date.
    Preserve both values and identify the conflict. Do not raise the ceiling
    from the form or dismiss the form based on the person's answer. The person
    must reconcile the report or correct the ceiling; until then the branch
    is unresolved. If both dated observations are below the ceiling, that
    still does not verify the unseen days. A separate case is a $900,000
    ceiling when the applicable limit is $750,000 but both source observations
    are below $750,000: the loose bound does not establish excess; ask for a
    tighter bound if available or leave the support unresolved.
11. **Other debt or unknown coverage.** A “yes” to other borrowing secured by
    either home is known debt outside this one-borrowing calculation; the app
    does not calculate a partial result or call it zero. “Cannot tell,” no
    answer, or withdrawal is unresolved coverage, also not zero. A “no” is
    the person's affirmative ordinary account and permits this bounded
    calculation to continue.
12. **No reports, one report, and changed filing status.** A genuinely
    closed-empty family keeps the existing determined zero even if a borrowing
    account and ceiling remain recorded; if that account still has a current
    affirmative link to a missing report, closure is instead incomplete. A
    legacy-only single report keeps incumbent behavior; one linked report
    stays on the connected path. If filing status changes, the numeric
    $250,000 ceiling stays unchanged;
    only the limit the application compares it against changes. A previous
    threshold-specific yes/no could not be reused unless it retained the
    exact threshold asked.

## Integration choices and cost

### Existing-first comparison

The student-loan path supplies a precedent for explicit relationships, not
mortgage tax semantics. `packages/tax/sli_relationship_recording.py` records a
person's answers as source evidence, then records affirmed financing and
statement-inclusion links using an opaque borrowing reference and an exact
statement subject. It also distinguishes cannot-tell, denied, withdrawn and
corrected outcomes, and requires the correction to identify its current
predecessor. That explicit identity and lifecycle pattern transfers. Its
student-loan qualifying rules, school relationships, worksheet, and allocation
logic do not.

The adopted student-loan content separates a family-authorized subtotal
(`rule.sli-worksheet-line1-subtotal.json`) from a downstream cap and reads subject results in the combined worksheet
(`rule.sli-worksheet.v5.json`). Its closed-empty default is distinct from a
nonempty source set with a blocked result. Those are useful composition
patterns: preserve each statement's result, aggregate only the family's
authorized Box 1 amounts, and keep “no reports” distinct from “missing or
unsupported.” The student-loan calculation and eligibility rules do not
transfer.

The sale path demonstrates exact report-key emission. `live.py` admits a
bounded list of 1099-K per-statement inputs only when the selected subject,
fact type, package binding and `(payer, statement, tax-year)` identity match;
it emits them as `SourceFact` rows. Generic `subject_dispatch.py` scopes those
rows to each report subject by their shared keys. That discovery is
Form-1099-K-specific, not universal transport. In particular, it does not
join mortgage facts to a borrowing account. Current subject dispatch can
still fall back to a run-wide symbol when no scoped source row exists, which
is how matching B values failed to prevent use of A's pins in P0.

For this account, the smallest content/transport candidate is therefore:

1. Keep the existing F1098 v1 family, statement keys and Box 1 subtotal. Do
   not add a second Box 1 path or a family successor merely because the
   recorder, rule and saved reader are currently singleton.
2. Keep report facts and report-local answers keyed by exact report identity.
   A targeted mortgage admission declaration would emit every report-local
   input the consumers actually require—not just Box 2—including Box 3,
   Box 9 and any genuinely report-specific ordinary answers. Missing keyed
   rows must remain absent/blocked; they must never fall back to a matching
   run-wide symbol.
3. Preserve borrowing-wide answers as their own person assertions keyed to
   the opaque borrowing reference and year. A proposed declared per-report
   intermediate finding must consume the original answer finding and that
   report's current membership-link finding, so its own pins—not a fabricated
   `SourceFact` carrying two IDs—retain both supports. It is not a copy or
   relabeling of report A's answer as report B's answer.
4. Keep filing status as a return-wide input. Keep the numeric ceiling as a
   separate borrowing/year input, not under the Box 2 symbol. The combined
   debt-limit calculation consumes that one ceiling once; per-report subject
   results keep their own interest source and explanatory support.
5. Select the connected mortgage path when current account assertions or
   explicit account outcomes exist, regardless of current report count. A
   closed family with one currently linked report can use that account's
   support; a legacy-only single report keeps the incumbent route. A
   closed-empty family gets the existing zero only when no connected account
   is current; an entered account with no reports is unresolved. The favorable
   aggregate requires every current report explicitly linked to this one
   borrowing, a closed family, and supported no-other-debt answer. More reports,
   unlinked members, another loan, or unknown coverage block the connected
   favorable route. No selection rule may fall through from an unresolved
   two-report case to the singleton path or a partial sum.

This is an existing-first design recommendation, not proof that today's
content language can express the scoped links and one-time ceiling exactly as
needed. A new mortgage vocabulary or content version may be needed; it is not
automatically a new published schema. No schema family or version is allocated
here. The design does not assume a general engine rewrite: the remaining
mechanism question is whether targeted source admission plus existing generic
subject dispatch can carry report-keyed and link-scoped findings with exact
pins. If it cannot, return the narrow missing join/binding requirement rather
than broadening the engine by default.

### Integration cost and evidence ceiling

| Area | Candidate change | What existing evidence establishes | What remains unproven |
| --- | --- | --- | --- |
| Ordinary account | Explicit opaque borrowing reference, two exact statement links, numeric annual ceiling, and separate other-home debt answer. Reuse answer evidence and correction patterns; no automatic matching. | Student-loan recorder demonstrates explicit opaque borrowing links and correction/withdrawal lineage. Mortgage recorder has exact statement answer keys and correction operations. | Mortgage has no borrowing entity/link, no numeric ceiling question, no multi-report review/save path, and no account-level lifecycle. |
| Report-local answer support | Keep all source facts and questions whose meaning names a report keyed to `(payer, statement, tax-year)`. Let the assertion's actual scope decide whether an answer is shared. | P0 agreeing-value pins prove today's subject label can consume A's answers and Box 2/Box 9 for B. | No mortgage transport currently guarantees each report-specific answer and correction predecessor reaches its own result. |
| Source admission/dispatch | Add bounded mortgage report-local emission and a declared per-report intermediate result whose actual input pins are the whole-loan answer and current report link. | Sale route demonstrates targeted keyed source emission; generic subject dispatch scopes matching rows. `SourceFact` has a single `finding_id`. | No live mortgage link-join/emission path exists; exact handling of the declared intermediate and report-local sources needs the discriminating check. |
| Content and aggregate | Make one successor producer of Schedule A line8a, with F1098 family collect inside the selected path; no separate raw-subtotal producer. Gate it on current account/link/coverage and compare one ceiling once. | F1098 v1 authorizes exactly `tax.us.2025.schedule-a.line8a`; `audit_collect_authority()` rejects a collecting rule that publishes another symbol. There is no separate incumbent raw-subtotal rule. | No connected line8a rule exists. The proposed successor must preserve the authorized symbol while guarding which family collection/result is admitted; current singleton rule consumes Box 2 and statement-local inputs and cannot implement it unchanged. |
| Saved explanation and reader | Add a group account containing both report explanations, one borrowing summary and exact shared/report pins, tied to the saved revision. Keep the old singular reader for one report. | Current projection validates a singular mortgage account with exact `statementKeys`; current review reloads and checks the one statement and revision. | No group-shaped mortgage model or reader exists. The connected design needs behavior that identifies all contributing reports and the exact source of the ceiling and each answer. |

The cheapest discriminating mechanism probe is one synthetic positive
two-report baseline plus four isolated mutations and one producer-removal
kill control (six coordinator runs total) through the actual
`live_coordinate_run` and targeted-admission/dispatch path.
The baseline uses different Box 1 values, but the same Box 3 and Box 9 values
on A and B, linked explicitly to one borrowing, a $250,000 ceiling, a “no”
other-debt answer, and uncontroversial report-local answers. This avoids
unrelated scope failures: Box 9 is 1 on both, and dates do not imply a
refinance. It must produce the authorized Schedule A line8a once and show
report-local versus shared support accurately.

Then change exactly one thing per run: (1) make B's report-local answer
contrary while A remains favorable, expecting B to use B's own answer and not
A's pin; (2) omit B's membership link, expecting the line8a branch to block,
not include B or silently drop to legacy; (3) set linked B's dated Box 2
observation above the ceiling, expecting conflict/unresolved; (4) set the
ceiling above the applicable limit while both observed Box 2 values remain
below the limit, expecting unresolved need for a tighter bound, not a finding
of actual excess. Each mutation leaves all other facts exactly at baseline.
The observable failures are wrong-source pins, missing answer/link pins,
unauthorized/generic subtotal publication, Box 2 substituted for ceiling, or
any partial/favorable/zero result on a blocked case.

The fixture supplies only raw loan-scoped answers, raw exact-report
membership-link findings, and the Box 1/other report sources. The intermediate
must be calculated by an actual package rule in the run, with the real
resolver, marshal, subject dispatch and evaluator; inspect its derived
finding's ledger disposition and input pins. A concrete paper candidate uses
an ordinary `rule-artifact.v13` computation with `subject` set to
`tax.us.2025.mortgage.report-membership`, `joined` set to
`tax.us.2025.mortgage.borrowing-paid-all-interest`, and `direction` set to
`subject_contains_joined`. For example, the subject's exact identity keys are
`borrowing=demo.loan-1,payer=demo.servicer-b,statement=demo.1098-b,tax-year=2025`,
while the joined answer is keyed by `borrowing=demo.loan-1,tax-year=2025`.
The proposed rule requires the shared answer and publishes a declared
report-scoped finding (for example,
`tax.us.2025.mortgage.report-paid-all-interest`) keyed to the report subject.
Its derived-finding disposition must actually pin both the membership finding
and shared-answer finding. The downstream report result consumes that
intermediate; it must not be manually fabricated in the fixture. These are
candidate fact/rule identifiers and an instance, not an allocated content
version. Existing `subject`/`joined`/`direction` fields support analogous
stale-target and relationship joins; the probe is specifically to verify
they can express this cross-identity loan-to-report propagation with actual
pins. If package/schema validation refuses these two different identity key
sets, or dispatch cannot emit a report-scoped derived finding with both
inputs, record that exact missing identity-join or derived-source operation
instead of supplying a hand-built intermediate.

The kill control removes only this intermediate producer from the proposed
package while retaining the raw membership and answer findings. Under the
actual contract, package validation may reject the dangling declared
consumer, or runtime dependency resolution must block it; in either case
line8a must not publish favorably. The six-run set is one tiny synthetic
fixture, no suite run and no new framework; proposed, not executed. It tests
transport, pinning, routing and line8a gating, not the ordinary recorder, a
person's actual affirmation, saved group reader, or cross-run persistence.

The Foreman's provisional direction selects the meaning below for this paper
design. It is not an accepted contract or production authorization.

| Product meaning | Proposed direction | Value | Cost or risk |
| --- | --- | --- | --- |
| Same borrowing and report membership | One explicit continuing-borrowing claim plus a link for each exact report. Opaque identity is created in the person's workspace, never inferred from report details. | Makes the relationship visible without institutional verification or automatic matching. | Requires a small account and link lifecycle; the current statement recorder is singleton. |
| Annual balance support | Ask for a numerical ceiling the person is confident was not exceeded during the year; keep it separate from dated Box 2 facts. | Gives the application a number it can compare after it determines the tax category and limit; remains usable if filing status changes. | An additional user assertion may be unavailable or contradicted; it is not independently verified and is not proven by the reports. |
| Other borrowing | Ask separately whether other mortgage or home-equity borrowing was secured by either home. Yes is unsupported here; unknown is unresolved; no is an ordinary assertion, not an objective completeness proof. | Avoids silently assuming second-home debt is absent while keeping the interaction bounded. | Excludes a real case when other debt exists; calculating combined debt would be broader work. |
| Input scope | Make scope follow the exact proposition. Keep raw report facts local; allow a genuinely whole-loan answer to cover linked reports only through explicit links and retained evidence. | Supports shared circumstances without accidental pin reuse or duplicate answers caused by storage keys. | Requires explicit source admission and correction dependencies for each scope. |
| Aggregation and compatibility | One Schedule A line8a producer retains the legacy route only when no connected account is current, and selects connected handling from current account state; use F1098 family v1's authorized collect only within that selected branch. | Reuses established family authority without conflating closure with loan identity. | New subject calculation, connected recorder/admission, and group saved-reader behavior remain unproven. |

The numeric ceiling is a provisional product-source choice, visible for
independent review: it is a person-confirmed ordinary fact, not an external
verification claim or a new trust domain. It remains an advisory choice for
owner disposition after review, not permission required to investigate its
transport or meaning. The explicit boundary for known other main-/second-home
debt follows this charter's excluded combined-debt scope; the product must
not silently assume zero or compute an unchartered allocation.

## Evidence ceiling and handoff

This account uses the committed P0 tax-source review, current path inspection,
synthetic diagnostic observations, and independent review/recheck. P0 showed
that two-report save/review and saved-reader paths are currently singleton;
that differing Box 2 values leave the unkeyed scalar absent; and that agreeing
values still do not make B's reason consume B's report-local observations and
answers. This design corrects the account of that limitation but does not
demonstrate a new path.

The account and integration path remain proposals, not accepted policy. The
numeric ceiling, links, and other-debt answer have not been recorded from a
person; no production feasibility, group reader, or new path has been proven.
The proposed single discriminating probe is described above and was not run.
No public schema version or production change is selected. The next gate is
one independent review of this connected design and the proposed probe, then
a production charter only if the owner accepts the remaining source and scope
choices.
