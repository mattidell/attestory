<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-statement-borrowing",
  "status": "P0 independently reviewed READY after its source-authority correction. P1 begins the ordinary shared-borrowing account and balance-treatment choices before mechanism selection. No production design selected.",
  "scope": [
    "extend the existing ordinary mortgage account to a bounded same-borrowing multiple-report case",
    "preserve report amounts, loan-level circumstances and their separate correction lifecycles",
    "establish a supported Schedule A result and saved explanation only after tax and production-path evidence"
  ],
  "non_goals": [
    "no refinancing, second-home, mixed-use, partial-payment or above-limit allocation calculator",
    "no automatic loan matching from names, account strings, amounts or property address",
    "no general assumption framework, free-text intake or broad engine redesign",
    "no changes to the separate projection-reuse performance milestone"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
      "docs/milestone-retrospectives/2026-10-19-multiple-statement-circumstances.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md"
    ]
  }
}
-->

# One Home Loan, More Than One Interest Statement

Milestone key: mortgage-statement-borrowing.
Branch: milestone/mortgage-statement-borrowing-same-loan.
Opening base: origin/main after merged PR #214. New primary managed worktree;
the separate projection-reuse milestone continues in its own worktree.

## What we are trying to accomplish

A person can receive two mortgage-interest statements even though they still
have one home loan—for example, after the company collecting payments changes.
The application should help the person describe that relationship, keep what
each form reports, and use the loan's circumstances to calculate and explain
the supported interest treatment. Two reports must not silently become two
borrowings, and saying they concern one borrowing must not erase either report.

The existing mortgage route obtains ordinary answers and saves an inspectable,
correctable result, but supports only one Form 1098. The opening case is one
continuing borrowing for one main home with two distinct reports in 2025.
Whether this case can stay within the existing calculation boundary is an
investigation question. No favorable result follows just from calling the
reports a pair.

This extends the earlier phase's completed breadth result; it does not retract
that result or imply that its original endpoint required more work. The useful
new distinction is a continuing borrowing versus the documents describing it.
Additional independent loans remain a contrast case, not promised coverage.

## What makes this uncertain

Interest reported for different periods may compose differently from a
reported outstanding balance. Naming one loan does not tell us which balance
or period the tax calculation needs. Counting the borrowing once is not a
license to choose the smaller balance, pick whichever form passes a limit,
or treat Box 2 as an annual average.

We must distinguish what the person recognizes and affirms, what a document
reports, what the application assumes, and what a tax rule establishes. A
complete set of recorded Forms 1098 is not automatically a complete account
of all home debt. The question and authority for each must be examined on its
own meaning. No new completeness claim or blanket favorable default is selected.

The current recorder, input transport, rule cardinality, debt-limit check,
closure and saved display may have different restrictions. Their names are not
evidence that two reports can reach the right loan and result. Existing sale
and student-loan mechanisms are candidates for reuse, not a selected loan model.

## Actions the team will take

1. **Review this opening account.** Independently examine whether the same-loan
   scope is useful and sufficiently bounded, what facts could defeat it, and
   whether the proposed investigation will expose those facts. Refine the plan
   before P0; do not demand a full implementation specification yet.
2. **Describe the case and verify current behavior (P0).** Explain in ordinary
   language what the person knows about the loan and reports. Verify the 2025
   reporting and deduction rules from primary sources, including balance dates,
   reporting periods, loan acquisition versus origination, and relevant limits.
   Trace the current adopted package through real recording, current support,
   marshalling, rule execution, Schedule A and saved explanation. Reproduce the
   actual second-statement stop through the offered path. Identify supplied,
   assumed, derived and unresolved information separately. Have P0 independently
   reviewed before selecting a representation.
3. **Establish the relationships and correction boundaries.** Separate the
   report, continuing borrowing, home, reported interest and balance observations.
   Identify a finite set of ordinary questions that can establish a material
   relationship without asking the person for a tax verdict. Work through
   correcting one form, correcting the shared account, withdrawing a link and
   adding a new report. Decide what remains supported and what needs renewed
   confirmation. Keep uncertainty different from a negative answer.
4. **Compare existing-first mechanisms and test decisive assumptions.** Inspect
   the adopted multi-statement subtotal/subject-result pattern and explicit
   relationship recording before proposing a schema or coordinator. Determine
   what belongs in content, recording or the engine. Use paper instances first;
   charter rival prototypes only for a consequential choice paper cannot settle.
   Specify the question, cheapest discriminating cases and evidence ceiling
   before running a probe. A supplied relationship or test-only declaration is
   not evidence that production obtained it. Review one connected design rather
   than commissioning a new full review for each prose refinement.
5. **Select and build the bounded path.** Return material scope choices to the
   owner. Establish any required contract and Track 0 closure before production.
   Charter small implementation units from the settled design, keeping existing
   single-statement behavior and saved history compatible. Refine track divisions
   only after the integration cost is known; no new schema version is allocated
   by this opening plan.
6. **Demonstrate, review and close.** Use the actual recorder, durable recovery,
   coordinator and reloaded saved presentation. Show which two reports contributed,
   what borrowing account was used, why the result follows and how one correction
   changes it. Keep focused regression and typing evidence; full ready-PR CI is
   the gate. Curate the result and assess this bounded extension, rather than
   automatically adding another mortgage scenario.

Each stage changes the plan only as evidence increases specificity. Keep the
high-level goal current. If it changes, record the reason; do not rename an
unresolved prerequisite as completed breadth. Record consequential product
decisions with their grounds and implications, not a transcript of every check.

## Cases that will shape the design

- Two genuine reports for one continuing borrowing, with different interest
  amounts and balance observations. Determine the required treatment; do not
  predeclare a principal formula.
- Identical-looking reports that instead concern two different borrowings;
  a duplicate or corrected report; and a person unable to establish the link.
  Similar amounts, labels or addresses do not decide the relationship.
- A deliberately over-limit debt and balances that would cross a limit if
  incorrectly added. A fixture whose principal never reaches the comparison
  is not a useful limit test.
- Correct one reported amount without changing the borrowing; change or
  withdraw the report-to-borrowing account; remove and re-record a report;
  preserve unrelated statements and saved history.
- No reports, one report and two reports; late entry after closure; missing
  or contrary ordinary answers. Do not let an omitted report produce a
  favorable partial sum, or a withdrawn answer silently resume a default.
- Preserve the incumbent single-statement mortgage route and neighboring
  sale/student-loan behavior. Scope of each shared change determines regressions.

These are investigation classes, not an exhaustive list of human statements.
Only questions material to the relationship, tax treatment or actionable
coverage limit belong in the supported interaction.

## Decisions and readiness

The goal is unchanged. P0 is independently reviewed READY for connected design
after one source-authority account correction; see the
[working account](mortgage-statement-borrowing-evidence/p0-current-account.md)
and [Sol review and recheck](../../../reviews/mortgage-statement-borrowing/p0-independent-review.md).
This is investigation readiness, not a production design or delivered feature.

The real v49/v47 diagnostic establishes:

- One report reaches the real recorder, calculation and reloaded saved result;
  an over-limit principal reaches the comparison and saves an unresolved
  explanation, not a prorated deduction.
- Two reports meet independent review/save and calculation restrictions.
  Different principal observations cannot bind the run-wide principal input;
  agreeing values reach the explicit multiple-report stop.
- Agreeing values also expose wrong support: the second report's reason uses
  first-report ordinary-answer and document pins. Every needed report-local
  input needs the correct authority and correction dependency, not merely a
  subject label or matching value. Filing status remains return-wide.
- Publication 936 distinguishes a throughout-the-year full-deduction branch
  from Part II's limited-debt calculation. The incumbent one-report Box 2
  premise does not automatically extend to two reports. The current family
  already authorizes a Box 1 sum; no general engine rewrite or new public
  schema has been proved necessary.

P1 now develops the ordinary account and its consequential choices: what
establishes a continuing borrowing, which circumstances are report-local or
shared, and how the whole-year debt premise is supported. First return a
plain-language account and paper cases for Foreman feedback; only then refine
the connected recording, transport, calculation, lifecycle and explanation
design. Independently review that connected design and any necessary
discriminating evidence as a whole before production. Do not commission
separate full reviews for each paper refinement.

Synthetic facts and selected answers remain diagnostic inputs, not proof of
an obtained same-loan relationship. Before production, settle the representation,
authority, assumptions, change handling and supported tax boundary.

### P1 working direction — provisional, not an accepted contract

P1's first plain-language account has received Foreman feedback. Continue with
explicit report links and assertions whose scope follows what the person
affirms. A genuinely loan-wide answer can cover both linked reports; report
amounts and dated observations remain separate. Distinct meanings need not
require separate screens or duplicate answers.

For the connected paper design, prefer a person-confirmed numerical ceiling
on what was owed on the identified borrowing during 2025. This is an upper
bound, not necessarily the exact highest balance. The application determines
the relevant tax category and compares the confirmed bound with its limit.
A bound within the limit can establish the balance condition. A bound above
it does not establish that the actual debt exceeded it: the bound may simply
be too loose. Preserve that distinction after a filing-status change too.
Ask separately about other borrowing secured by the main or second home;
known additional debt reaches this milestone's coverage boundary, while an
unknown answer leaves that circumstance unresolved. Do not ask the person
to classify a combined set of "qualifying acquisition debt."

This is a candidate ordinary factual source, not a claim that people were
observed answering it or that two Forms 1098 establish it. It avoids selecting
a favorable snapshot or silently treating the largest observation as an annual
ceiling. Its cost is an additional factual confirmation; some people may not
know a usable bound. Its risk is an inaccurate or contradicted answer, which
the design must make inspectable rather than describe as independently verified.
It displaces an automated balance-history/proration calculator, not the need
to represent the debt conditions accurately. A broader assumption policy is
not selected.

Develop this candidate's relationship, correction, source and consumer behavior
in P1 B, including a changed filing status and contrary principal evidence.
If a threshold-specific yes/no is considered instead, preserve the actual
number affirmed; an answer about one threshold cannot silently become an
answer about another. The existing single-report route and saved history
remain compatibility requirements. Return material costs or a demonstrated
inadequacy before selecting production. This develops the original goal;
it neither changes that goal nor authorizes implementation.

P1 B's connected paper account is drafted and under Foreman review. Before
its proposed experiment, make route selection safe when a connected account
loses a report or an assertion: a count of one must not ignore still-current
contrary or unresolved information. Identify the exact family-authorized
symbol and actual provenance carrier, and isolate positive and negative probe
cases so one failure cannot hide another. These are design-readiness repairs,
not a new product goal or authorization for production.
If the case needs a general debt-allocation calculator, a new identity system,
refinancing treatment or a broader engine contract, stop and bring back a
plain-language scope/cost choice rather than absorb it.

Track 0 adversarial closure: PENDING. No production charter is authorized yet.
Existing published schemas, ADRs and source-use contracts remain in force.
The cross-milestone schema-intent ledger applies if a successor is later chosen;
the parallel engineering work is not an assumed dependency.

Completion means the selected bounded same-borrowing case is recordable,
calculable and explainable from saved results, with exact report provenance
and demonstrated correction/withdrawal behavior. If evidence defeats this
boundary, return a specific partial result and owner decision instead of
claiming the feature is delivered. Visual observation is claimed only if
actually obtained; automated saved-model evidence is a separate observation.

Only synthetic demo accounts enter committed evidence. No personal forms,
workspaces or private outputs are used. Early plan review needs source checks,
not a fresh full suite; later shared-engine changes retain the complete gate.

## Planning sources

- The prior mortgage and multiple-statement plans and their retrospectives
  named in this plan's planning reads. Their one-Form-1098 boundary remains
  the starting point, not evidence of a multi-report calculation.
- [2025 Publication 936](https://www.irs.gov/pub/irs-prior/p936--2025.pdf):
  general deductibility, debt limits and average-balance methods. P0 must
  establish which provisions the selected class actually needs.
- [Form 1098 instructions, April 2025](https://www.irs.gov/pub/irs-prior/i1098--2025.pdf),
  Boxes 1, 2, 3 and 11: reported interest and dated principal/origination/acquisition
  observations. Opening inspection confirms those distinctions, not a complete
  same-loan deduction method. P0 must reconcile any stale tax-summary language
  against the actual 2025 rules rather than extending it to later years.
