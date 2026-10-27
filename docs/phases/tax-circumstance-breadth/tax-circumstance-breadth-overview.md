# Tax Circumstance Breadth

## Bounded mortgage extension

[One Home Loan, More Than One Interest Statement](milestones/mortgage-statement-borrowing.md)
extends the earlier mortgage route to one or two Forms 1098 about one
continuing original borrowing for one main home. Each report keeps its own
amounts and local answers; explicitly shared borrowing answers reach it only
through the person's exact link. The supported calculation and saved
explanation preserve those scopes through correction, withdrawal and clear.

This extension does not invalidate the earlier phase endpoint or select
general mortgage allocation, refinancing, another home/borrowing or a general
assumption system. Publication review and CI remain in progress. Further
milestones remain unselected.

## Purpose

Help a person describe circumstances that change the tax meaning of a document,
and have the application use that account in its calculation and explanation.
Extend the work demonstrated for student-loan deductions to other tax areas.

A form reports an amount. A person knows what happened in their life. The
application connects those accounts, applies the relevant rules, and explains
the resulting treatment. The person should not need to translate their own
answer into terms such as acquisition debt before the application can use it.

The aim is useful, bounded product capabilities in additional domains. Existing
representations and engine mechanisms are starting points. New circumstances
may need different concepts or relationships; resemblance to student loans is
not sufficient reason to copy their model.

## What we will do

1. Choose an ordinary situation where document data alone does not determine
   the treatment and where the person can supply a material circumstance.
2. Describe the situation, rule, available information and intended interaction
   in plain language; examine what the current application actually does.
3. Establish which relationships and distinctions must survive translation,
   calculation, correction and explanation.
4. Test consequential uncertainties, select a bounded approach and build it
   through the adopted package and saved result.
5. Apply the approach in a contrasting tax area, then assess the phase's result
   and the remaining cost of further breadth.

Develop each milestone incrementally under the existing
[planning guidelines](../../process/planning-and-development.md). Review the
first concrete account and the proposed implementation boundary while they can
still change cheaply. Short accounts of decisions, their grounds and their
consequences support ordinary review; the shelved communication experiments do
not become an additional process gate.

## Defaults and assumptions

The product may deliberately proceed on reasonable assumptions. A default is
the application's action under specified circumstances; the assumption is what
it is treating as true when it takes that action. Neither establishes that the
person said it or that an institution verified it.

For each selected tax case, decide what can be assumed, what supports that
choice, which subject and period it concerns, and what information changes its
use. Silence, an explicit answer, contrary information, uncertainty and a
withdrawal may call for different behavior. Removing an answer must not
accidentally make a result more favorable. Whether a default resumes is a
product decision whose effect is tested.

Keep conditions left with the person inspectable even where the application
does not obtain a finding for them. Such a condition can still affect the tax
result; displaying it does not resolve it. A missing software capability is
also different from an unfavorable tax conclusion.

Begin with the actual cases and the existing basis and lifecycle mechanisms.
If they reveal an essential missing assumption capability, define the smallest
required change with its consumer. If several cases need the same behavior,
consider a shared contract. This phase does not preselect a universal default
engine, blanket favorable policy or new schema.

## Product boundary

Start with 2025 federal individual-return content to reuse the established
calculation path. Each milestone selects a finite set of ordinary questions
whose answers affect treatment, relationships, applicability or an actionable
limit. Free-text interpretation and an exhaustive catalog of life events are
not prerequisites.

Preserve separate meanings for document evidence, normalized ordinary answers,
canonical tax concepts, derived results and explanations. The tax concept is
not defined by the wording or polarity of a particular question.

Specialized allocation and accounting calculations are not automatically the
application's responsibility. Where automation ends, evaluate whether a scoped
person-supplied amount would be useful; admitting and using such an amount
requires a concrete design, not an implicit override. General intake, external
institutional verification, a complete filing product and annual content
updates remain separately selectable work.

## Provisional phase endpoint

Two additional, distinct tax contexts have a bounded production path from
recorded ordinary circumstances and documentary amounts to a tax result and
saved explanation. At least one reaches beyond borrowing-related deductions.
For each, the supported interaction obtains an ordinary answer, preserves its
scope, and demonstrates how correcting it changes the result without erasing
the source report or unrelated answers.

The phase leaves a short account of what transferred, what required new work,
where assumptions remain, and which adjacent cases are still unsupported.
Assess this endpoint after the first delivery. A prerequisite or partial result
may change the phase plan, but does not count as delivered tax breadth.

## Starting position

Tax Concept Derivation established a bounded derivation and explanation chain.
Evolving Workspace Accounts added correction and recovery for the student-loan
account, through merged PR #207. Its owner visual review, independent reader
assessment and personal-workspace use remain open; this phase inherits no new
claim about those activities.

Shared Understanding in Development is shelved by owner direction. Its
experiment record remains on `milestone/working-model-experiment-statement-scope`.
No experimental participant plan or new development convention is adopted.
