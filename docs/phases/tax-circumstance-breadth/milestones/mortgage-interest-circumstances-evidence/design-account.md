# Mortgage circumstances — consequential design account

## What this account is for

Explain the product we are choosing to build and why. This is a working,
plain-language account for the owner and future agents, not another contract
or a running list of defects. Exact evidence and adopted contracts keep their
own homes; link to them when they support a choice.

## Where the design stands

The goal has four parts, and each must hold for the opening case. The person
gives understandable ordinary answers about one Form 1098. The application
translates them into tax meaning. It calculates the bounded result. And the
person can inspect and correct the saved account.

We want a person to describe what happened with a home borrowing without
having to decide its tax classification themselves. The document, their
ordinary account, the canonical tax meaning and the application's treatment
are related but not interchangeable. The P7 independent review
supports a bounded design that connects them. The questions, tax conditions
and assumption policy were selected and tested through a temporary
publication surface. ADR 0078 is accepted. Production vocabulary, the
calculation package, the saved explanation, and recording are built. The
independent production review found that three uncertainty answers were
explained as coverage limits, zero descriptions omitted part of their basis,
and saved answer tokens did not convey the offered meaning. Those repairs
keep choice 4 and do not broaden the tax calculation. The v45 successor
names the conditions and blocks the amount. The repair review accepted that
semantic result. It did not accept a publication verdict, browser observation,
or a verified 2025 standard-deduction amount. The joint-return wording repair
also exposed a meaning boundary. An older personal answer about ownership or
residence is not automatically an answer about the filing unit. The successor
asks the two broader questions under distinct input fact names; it does not
rewrite the older answers. Its valid recording demonstration uses that
explicitly selected question set. The recording tests save evidence-backed
answers through the real log before calculation and saved review; the earlier
calculation and reader tests that supply answers directly remain separate
evidence.

The starting point is now established. The present path asks the person to
answer yes to eight confirmations about the home and the debt. P1 settled
which are which. Four are legal conclusions the person is asked to affirm:
liability and payment, main home, acquisition-debt use, and no mortgage
credit. Four are software coverage bounds: single mortgage and single home,
no refinance, no balance increase, and not shared except with a spouse.
Security has no confirmation at all. Without a yes to acquisition use, the return
reaches neither the deduction line nor taxable income: the standard deduction
is still computed but not selected. That is the arrangement an ordinary
account would replace or extend, not a behaviour we have chosen to keep.

The opening investigation characterized software to extend; subsequent design
and review selected the choices below. Identifying a default in the existing
package did not itself adopt it as the new circumstance path's policy.

## Provisional choices for the opening case

Choices 1–6 follow from the P1 circumstance account
and its review. Choices 7 and 8 follow from the
P2 mechanism fit. Choices 9–11, and the revisions to
1, 3, 4, 7 and 8, follow from the connected-design review; the section after
the choices says how each changed. P2 found that existing mechanisms
can carry choices 1–6 with new content, apart from the explanation. All
choices are now reviewed design selections for this bounded implementation;
the owner may redirect any of them. Production contract acceptance and delivery
are separate from the prototype evidence.

**1. The person describes what happened; the application draws the tax
category.** The new route asks ordinary questions about ownership and the main
home, whether the home is collateral, who owes the loan and paid the interest,
whether anyone outside the filing unit owes it, and what the borrowed money
paid for. The application concludes whether the interest is qualified residence
interest. *Alternative set aside:* keep the four legal confirmations with
friendlier wording. That only renames a legal yes/no, and P1 showed that one
confirmation, acquisition-debt use, stands for several conditions at once.
*Consequence:* those four confirmations do not belong to the new route. "No one
else owes it" is the person's statement about their own loan; it supports
liability and makes the co-borrower bound inapplicable. Liability and payment
are separate answers. The supported case is an owner who owes the loan alone
and paid the interest, so "I owe this loan" is a material condition of that
case, not an informational one. On a joint return the spouses answer
together: the question text itself says that a loan owed by either spouse
counts, so a spouse who is not on the note is not pushed into the
not-on-the-note case. An owner who paid without being on the note
may still deduct (Treas. Reg. §1.163-1(b)), but someone else then owes the
loan. That case is outside coverage: the application explains it and leaves
the treatment with the person.

For the production-review successor, ownership can be by either spouse on a
joint return, while the residence answer describes this route's shared main
home. These are separate propositions from the earlier "I own this home" and
"where I live" questions. New input names preserve that distinction. A saved
personal "no" is not translated into "neither spouse owns it", and a v1-only
account does not establish the successor's broader required answers. The old
v44 route and its questions remain reproducible; automatic migration is not
selected.

The P6 re-review found one remaining payment distinction.
"I did not pay it myself" cannot alone justify a zero: somebody else may
have paid for the filer. The provisional P7 question distinguishes all interest
paid by the filing spouses, third-party or partial payment, genuinely no
payment by/for them, and uncertainty. Third-party/partial payment is explicitly
outside coverage, not a tax verdict. The product records no other payer's
identity and does not compute allocation or gift treatment. This costs one
unpublished answer/reason and small existing-rule branches; it prevents the
admitted counterexample from silently becoming a settled zero. The cost to
the person is an unresolved result for that wider payment account.

**2. Only the single-statement bound is the application's to state.** The
application establishes "single mortgage, single home" from the one recorded
statement and the one home in the account; the person is not asked to affirm
it. The refinance and balance-increase bounds become inapplicable when the
person describes an original borrowing. The purchase statement is not that
description: a refinanced purchase loan can still be acquisition debt, and
silence about an earlier loan is not evidence that there was none. The
co-borrower bound becomes inapplicable through the person's own statement in
choice 1. When the account falls outside these bounds, for example a
refinance or another person on the loan, the application says so and leaves
the treatment with the person. *Alternative set aside:* keep asking the
person to affirm the single-statement bound, which makes them vouch for the
software's scope. *Consequence:* an account outside coverage is a third
outcome, distinct from a supported and an adverse one. The new route needs an
ordinary way for the person to say whether this is the original loan.

**3. A determined adverse account is a result, not a gap, but only once it
is established.** When the person's account establishes that the interest is
not qualified residence interest, the statement carries that determined
result and the return proceeds, so line 12e can select the standard
deduction. The explanation says the interest was reported, why it does not
count, and what that conclusion rests on. *Alternatives set aside:* keep
today's block, which withholds a return the rule can compute; or treat the
answer as missing, which discards what the person said. This differs from the
student-loan route, where a "no" means the statement is outside the plain
case and line 21 blocks.

"The money paid for a personal expense" is not enough on its own. A mortgage
taken out within 90 days of buying the home, or around building or improving
it, can be acquisition debt even when the borrowed dollars went elsewhere.
Debt secured by the home on October 13, 1987 is grandfathered and deductible
whatever it paid for. A refinance carries over the old balance's status. So
the zero is justified only when the account also establishes the following:
- it is the original loan;
- one statement and one property;
- the loan was not taken out around a purchase or a building project;
- the debt is not grandfathered.

The person establishes the timing by answering ordinary questions about when
things happened. They are never asked to recognize the exception. These
questions are asked only when the money did not buy the home. One asks when
the home was bought relative to this loan, before or after. The other asks
whether building or major improvement work fell within the periods
Publication 936 describes. The wording must not let an ordinary answer
falsely clear an exception. Where precise wording is hard to make
understandable, a wider, conservative window is acceptable: it can only
leave more cases with the person.

The P6 planning review corrected the P5 re-review's
reason for widening this question. The 24-month period limits the expenses
that count; it does not extend the interval between completion and the loan.
A project completed 18 months before the loan does not establish this
exception. The three-year screen would unnecessarily leave completed projects
from 91 days to three years earlier with the person.

The provisional question instead asks: "Was this loan taken out before you
finished building or improving this home, or within 90 days after you
finished?" Nearby help includes unfinished or paused projects and preparation
before physical work began. It uses the release of the loan money as the date;
if an earlier written application could change either timing answer, the
person chooses "can't tell". The purchase question explicitly says "within
90 days before or after buying the home" and shares that date help. A building
"yes" leaves the expense cap and substantial-improvement determination with
the person. Saying "improving" is deliberately conservative: routine repairs
can leave the case unresolved rather than being silently classified by the
question. The timing screen does not itself establish acquisition debt.

An unasked question is not an answer. When the money bought the home, the
timing questions are never asked, and their absence must not block that
account. When the money went elsewhere, the timing conditions must be
established by the person's answers. A missing or withdrawn timing answer
cannot clear them, so the zero is not reached and the condition is shown as
unanswered. That is not the same as the person saying "can't tell", and the
explanation must not say they did.

Grandfathering is different: it turns on the origination date in box 3, and
the rule language cannot compare a date. The recommended prerequisite is one
narrow capability: comparing a recorded date with a fixed date, with no date
arithmetic and no general date framework. It costs a rule-schema successor,
evaluator and runner support, and an ADR. It is one engine unit, run against
the full suite. *Alternatives set aside, pending review:*
- Asking the person whether the loan dates from before October 1987 restates
  a document field and invites contradiction with it.
- Withholding the determined zero for this milestone avoids the engine work,
  but every personal-expense account would then leave the return blocked.
  That would include the common home-equity loan spent on something else.

Choice 9 sets out which conditions each conclusion needs.

*Consequence:* the closed-empty family and a zero-interest statement already
select the standard deduction, so a disallowed statement must still differ
from both in its conclusion and explanation. Withdrawing the answer leaves a
statement with no answer, which blocks. It never selects the standard
deduction, so withdrawal is never more favourable than the adverse answer.

**4. Uncertainty is an answer, not a blank and not a "no".** "I can't say
what the money paid for" is recorded as the person's answer. It names the
open condition, produces no deduction from that statement and leaves the
return unresolved, with that condition shown. It is not reported as outside
coverage: what the money paid for is a question the application handles, and
the answer is simply not yet known. *Alternatives set aside:*
treating uncertainty as yes claims what the person did not say, and treating
it as no concedes what they did not say. *Consequence:* each statement the
new route asks for needs a way to say "can't tell". The student-loan route
already has one. Each "can't tell" names its own condition. Not knowing
whether one owns the home is not the same as a circumstance the application
does not support, even though neither lets the calculation finish. This
applies to every statement, including collateral and payment. P5 had
carried it for ownership, residence and share only. The re-review noted that
the same mechanism covers the other two, so the narrower scope is not
adopted.

**5. No assumption about the person's own circumstances.** The application
does not assume what the money paid for, ownership, residence or security.
P1 found no grounds for those assumptions, and the 90-day rule shows that an
apparent purchase story can still be misclassified. P1 offered two
candidate assumptions, each with stated grounds and stopping conditions:
that the debt limit is met, and that no mortgage-credit reduction applies.
Choice 7 takes the first and declines the second.

**6. Mixed use, the 90-day rule and refinancing stay outside the computed
path.** The application explains why and leaves the treatment with the
person. Staying outside means neither the supported amount nor the
determined zero is computed for them, and the ordinary timing answers in
choice 3 are how the application recognises them. This milestone does not take a person-supplied allocated amount or
build allocation. Whether a scoped supplied amount is useful remains a later
question.

**7. The debt limit is a declared assumption; the mortgage credit stays a
question.** The present rule is written to publish the whole box 1 when box
2 is at or under the post-2017 limit for the filing status, and to block
when it is over. That publication is the assumption: one date's principal
stands for the whole year's balance, with no proration. The comparison was
meant to be its guard, but the design review found
that it never sees box 2: it collects box 2 from a family whose members are
box 1 amounts, so it compares zero with the limit. A principal over the
limit therefore deducts the whole interest today. Box 3, the origination
date, is required but never read, so the post-2017 limit is applied even to
older debt. The new route must read box 2 itself, and only then does the
over-limit block act as the stop. The supported conclusion does not need
the origination date. The post-2017 limit of $750,000 is the strictest that
applies to any debt, so applying it to older debt can block a loan a higher
limit would allow, but can never overstate the deduction. A loan over the
limit is therefore left with the person, with an explanation that older debt
may have a higher limit. The date matters to the determined zero instead,
through the grandfathering in choice 3. P1's other stops (a higher
balance during the year, another mortgage, a credit line, an added draw, a
second home's debt) are stated in the basis but not enforced; nothing the
person records triggers them. What is left with the person is the prorated
amount when a stop applies. Because the route records no stop-reports,
there is no report whose withdrawal could restore the assumption. Correcting
box 2 or box 3 is a correction of the statement, and the guard re-evaluates.

The mortgage credit stays an ordinary statement: "I did not receive a
mortgage credit certificate." Silence blocks, as today's required yes does.
*Alternatives set aside:* assuming no reduction would ask less than today,
and silence or a withdrawn certificate report would then take the favourable
path. Asking every person about average balances would bring in Table 1
work that P1 declined. *Consequence:* the debt-limit assumption is
favourable, so it is acceptable only if the person can see it. That makes
showing the basis a requirement, not an option.

**8. The explanation shows the answer, the conclusion and its basis.** The
milestone is complete only when a saved explanation shows the answer and
the basis used. P2 and its review found two routes. A blocked
result can already carry its own wording as new content: "you could not say
what the loan paid for", or "a refinance is outside what this application
computes". Showing the basis is different: ADR 0077 Part 2 already says a
reader loads `basis` from the rule a result pins, but today that is done
only for the student-loan rules. The new route finishes that reader for any
rule rather than adding a mortgage-only one. Blocked-result wording alone
cannot do this, because it does not load `basis`. *Alternative set aside:* new
content only, with no basis shown. That cannot meet the completion
criterion, and it would hide the assumptions in choice 7. *Consequence:* this
milestone takes on one engine change, finishing the general basis reader. No
sentence is attached to the published line 12e value.

Three kinds of result must stay distinct to the person:
- **A determined conclusion.** Either the interest qualifies, or it does not.
  The return completes. The person sees their answers, the conclusion, and
  the basis of the rule that reached it, including any assumption used.
- **An unresolved condition.** Something the person could not say. The
  return does not complete, and the person is told which answer is open.
- **Unsupported coverage.** A circumstance the application does not compute.
  The return does not complete, and the person is told which circumstance,
  and that the treatment is theirs.

A completed conclusion is never shown through the blocked-result field,
which is only for results that cannot finish. Which basis is shown follows
from the conclusion reached, not from incidental differences in the
derivation record. The selected carrier is one categorical reason rule per
statement, alongside one amount producer. Its value distinguishes qualification,
the three justified-zero conclusions and the unresolved reasons. The earlier
recommendation of separate conclusion rules was replaced when the declared
reader proved to require one publisher; the connected design's section 2
records that experiment. No two amount rules compete for the same account.
The P4 re-review
found that the reader changes named so far would leave a determined zero with
no account at all. Blocked-field reasons attach only to a blocked result, and
the proposed basis section is gated on a pin a zero never carries. So
showing a completed conclusion with its basis is a third reader change. It
is still Python only, with no published schema change. A qualified result
uses the amount rule's declared basis. A justified zero uses the matching
reason's content and the inputs that support that conclusion, without copying
the qualified result's assumptions. Both receive a completed-result account;
neither is explained as an unresolved question. The cost is the presentation
account and a generic exact-rule basis loader, not separate competing reason
or amount producers.

**9. Each conclusion lists the conditions it needs.** The supported
conclusion needs every favourable condition established. A determined zero
needs its decisive adverse fact, plus every condition that could otherwise
reclassify that fact. An adverse fact is independently decisive only when
nothing else the account could hold would make the interest deductible.

- **Use.** Within the selected payment boundary, a personal-expense use may
  justify the zero. It is not decisive over refinancing, more than one
  statement or property, the purchase and building timing windows, or
  grandfathering, because each of those can change how the same use is
  classified. P7 deliberately routes known third-party/partial payment and
  payment uncertainty out before this use arm; it does not claim tax law
  makes a zero impossible in every such case. This is the conservative
  product boundary selected without allocation or another payer model.
- **Payment and collateral.** The payment negative must exclude payment for
  the filing spouses by someone else. That narrowed answer supports the zero;
  third-party/partial payment does not. "The home is not collateral" remains
  the independently decisive home-mortgage exclusion in the reviewed condition
  table. Neither zero says no deduction could exist under another provision.

The line 8a amount and the explanation follow one condition table. They are
tested over combinations of conditions, not one case at a time.
*Alternatives set aside:* blocking every account that is not fully favourable
throws away determined answers, and letting any adverse fact win throws away
the conditions that justify it.

**10. The person records, corrects and withdraws the account through one
bounded operation.** For an already recorded Form 1098, the person:
- identifies the statement;
- answers the questions, including the timing questions when the use was
  not buying the home;
- saves, corrects or withdraws an answer;
- reviews the saved account and its explanation.

The student-loan recording and review operations are the model. Direct
synthetic assertions only show that the calculation is feasible. They do not
show that a person can supply the account, which is half of the goal.

**11. The production arrangement is the one that is tested.** The new
statements form a separate bundle. Evidence for feasibility must run the
arrangement proposed for production, or name what it stands in for. The P4
re-review found that a default for a blank box 9 is declared on the fact type
itself, not on the package binding alone. Leaving the published vocabulary
unchanged and adding the default are therefore incompatible. Either box 9
gets a successor fact-type version, with an account of how existing recorded
box 9 values still resolve, or the route stops requiring box 9 and finds
another way to notice a statement that reports more than one property. The
choice belongs to the next repair, and its probe must run the arrangement
chosen.

## How the choices changed after the connected-design review

The design review, the [revision](p3-connected-design.md)
and the owner's review of the revision changed several choices. Each entry
says what kind of change it was.

- **Earlier choice deliberately changed.**
  - *Choice 7.* It had promised to bind a date stop on the debt limit. The
    revision deferred it because the rule language has no date comparison.
    On reflection the supported conclusion does not need it, since the
    strictest limit can only under-claim, so the promise is withdrawn. The
    consequence: pre-2018 loans between $750,000 and $1,000,000 are left with
    the person rather than computed.
  - *Choice 8.* An engine constraint drove the revision to show determined
    zeros through the blocked field. That change is reversed as a product
    judgment, because a completed conclusion and an unresolved question must
    look different.
- **Requirement lost while repairing another problem.**
  - When the four line 8a rules were consolidated into one, the conditions
    behind the personal-expense zero were dropped: original loan, one
    property, and not grandfathered. Consolidation was sound; dropping the
    conditions was not a decision. Choice 9 restores them.
  - The split of liability from payment left "I owe the loan" required but
    described as informational. Choice 1 now gives it a material purpose.
- **Assumption never established.**
  - That a person would recognise the 90-day exception and answer "other".
    Choice 3 replaces it with ordinary timing questions.
  - That an owner who paid without being on the note reaches the supported
    case. The "no one else owes it" condition excluded that case, so it is
    now stated as outside coverage.
  - That uncertain ownership is outside coverage. Choice 4 separates the two.
- **Consequence of another change.** Choice 6 now says that the timing
  questions in choice 3 are how the application recognises the 90-day and
  building cases it does not compute. That follows from the choice 3
  revision and is not a separate decision.
- **Earlier choice changed by new evidence (P4 re-review).** Choice 11's
  "unchanged vocabulary plus a package default" is not achievable, because
  the default lives on the fact type. Choice 8's reader cost grows by a third
  change.
- **Assumption introduced as a mechanism (owner review of P4).** To keep
  unasked timing questions from blocking a purchase account, P4 gave both
  timing facts a "structural" default: "more than 90 days" and "no building
  work". Those defaults also applied when the money went elsewhere and the
  person had not answered. So an unanswered account reached the zero, and
  withdrawing an answer restored it. A default about a person's
  circumstances is an assumption, which choice 5 rules out. Choice 3 now
  separates "not asked" from "not answered".
- **Earlier reading corrected by new evidence (P6 planning review).** The
  proposed three-year building screen confused the completion timing with
  the expense cap. Choice 3 now asks about completion, including unfinished
  projects and mortgage-date uncertainty. This corrects the rationale, not
  merely the precision of the wording. The P5 report remains historical
  evidence, not the source of the current timing premise.
- **Made more specific (P5/P6 reviews).** The spouse clarification moves into
  the liability, payment and sole-obligor questions. Choice 4 covers collateral
  and payment uncertainty too. These carry existing requirements through to
  the actual questions and results rather than changing the earlier choices.
- **Work missing from the plan.** No production unit obtained and saved the
  ordinary account. Choice 10 assigns it. The box 9 default was probed on an
  arrangement different from the one proposed. Choice 11 requires the
  proposed arrangement to be the one tested.

## Questions whose answers will shape the product

- **What is the person answering?** Choose understandable, materially useful
  statements and their scope. Establish how those answers support a tax concept
  without asking the person to provide the legal conclusion under a friendlier
  label. Similar wording or polarity does not make the two the same fact.
- **What does the application supply?** Identify actual assumptions separately
  from the person's answers, rule-derived conclusions and conditions merely
  explained to the person. Decide when an assumption is used, what it concerns,
  and which new information changes its use. Do not treat every missing input
  as a default, or every displayed condition as an established fact.
- **How do these accounts meet and change?** Decide what connects the answer,
  borrowing, home and statement, and how correction, uncertainty or withdrawal
  affects the tax treatment and its basis. The result should follow that model,
  rather than an accumulation of unrelated special-case rules.
- **Where does the application stop?** Decide which distinctions it resolves,
  which it explains but cannot resolve, and whether a person-supplied amount
  has a useful place when allocation is outside the selected capability.

## How to retain the decisions

As a choice becomes concrete, replace or expand the relevant open question
with a short account of the chosen model, the reason for it, the meaningful
alternative, and what it changes for the person and later development. Include
one example when it clarifies the distinction. Keep provisional choices visibly
provisional; retain the reason if subsequent evidence changes them.

A discovered engine behavior belongs here only if it changes that account—for
example, revealing that our representation cannot distinguish a person's answer
from an application assumption. A corrected trace or a test that exposes an
omitted dependency is not itself a consequential product decision.
