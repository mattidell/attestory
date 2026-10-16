<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-interest-circumstances",
  "status": "Initial plan. Investigate the Form 1098 circumstance path and its assumptions before selecting implementation. No production design or build charter is approved by this plan.",
  "scope": [
    "connect a bounded ordinary account of a home borrowing and its use to the Form 1098 interest treatment",
    "decide how recorded circumstances and any adopted assumptions support or change that treatment",
    "build and demonstrate the selected bounded recording, calculation and saved-explanation path"
  ],
  "non_goals": [
    "no complete mortgage-interest or Schedule A coverage",
    "no automatic copying of student-loan whole-loan treatment or defaults",
    "no general assumption engine, free-text intake or allocation calculator selected in advance"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md"
    ],
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md",
      "docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md",
      "docs/milestone-retrospectives/2026-10-03-student-loan-deduction-completion.md",
      "docs/milestone-retrospectives/2026-10-08-account-refinement.md"
    ]
  }
}
-->

# Mortgage Interest and What the Loan Paid For

Milestone key: mortgage-interest-circumstances.
Branch: milestone/mortgage-interest-circumstances-translation.

## What we are trying to accomplish

A person brings a Form 1098 and knows what they borrowed for. Help them
describe that circumstance in ordinary terms, connect it to the reported
interest, and let the application determine the supported tax treatment.
They should be able to inspect and correct that account from its result.

Start by examining a single borrowing secured by a single main home and a
single statement: money used to buy that home, contrasted with money used
entirely for a personal expense unrelated to the home. These are investigation
cases, not a selected rule or an assertion that those facts alone establish
deductibility. The home, security, dates, debt limits, payment and other
conditions still need a deliberate place in the bounded route.

## What exists and what needs checking

The Form 1098 vocabulary records document amounts and confirmations including
`qualified-main-home`, `acquisition-debt-use` and `liable-and-paid`. The
Schedule A line-8a rule admits a bounded singleton class and requires those
confirmations. Core calculations v42 includes this vocabulary. The original
milestone excluded refinancing, home-equity and mixed-use debt, multiple
statements and several other situations. Those are coverage limits, not tax
conclusions about the excluded cases.

These are content and historical-design observations. Resolve the adopted
package and run the present path before claiming behavior. Student-loan
recording, per-subject evaluation, basis explanation, correction and recovery
provide reuse candidates, not an already-proven mortgage route. The mortgage
branch also has complete-return and standard-versus-itemized dependencies.

## Actions the team will take

1. **Describe and inspect the present case.** Explain what the person can know
   and say, what the form reports, what the application must decide, and why
   it changes treatment. Trace and run the current route. Review this account
   before refining the design around it.
2. **Establish the tax and product boundaries.** Consult 2025 authorities;
   identify the ordinary answers, canonical concepts and relationships needed.
   Settle the opening cases and catalog only materially relevant circumstances.
   Locate mixed use, refinancing and other neighbors without committing to
   automate them all.
3. **Decide how incomplete information is handled.** Describe any adopted
   assumptions, their grounds and scope, what contrary or uncertain information
   does, and what correction or withdrawal changes. Separate missing information
   from missing product capability. Show the effect on calculation and explanation.
4. **Test and select a bounded design.** Follow an ordinary answer through
   recording, relationship identity, tax conclusion and the Schedule A consumer.
   Prototype competing mechanisms only where a consequential difference remains
   unsettled. Review the connected design before implementation.
5. **Build in small units.** Implement the selected content and recording path,
   connect the real package and return consumers, and expose the account and
   its correction through a bounded interaction and saved explanation.
6. **Demonstrate and assess.** Run the supported route, a material adverse or
   unresolved case, and correction/recovery. Explain what transferred from
   student loans, what changed and what the next tax area would still need.

Refine these actions as evidence arrives. Keep consequential decisions and why
they permit the next action visible to review. Follow changed premises into
affected cases and proposed work. No separate communication experiment is required.

## Decisions before building

- Which ordinary circumstances support the tax proposition, and what remains
  assumed or the person's responsibility? Decide before naming a favorable
  result. Do not rename a legal yes/no as an ordinary question.
- What identifies the home, borrowing and statement, and what confirms their
  relationship? Preserve correction and distinct accounts; no new citizen is
  presumed necessary.
- Which legacy confirmations can coexist with the new account, which become
  inapplicable, and how can disagreement be resolved while preserving history?
- What happens to the mortgage result, Schedule A and the return when a
  condition is adverse, uncertain or outside coverage? A zero, a blocked path
  and an unchanged standard deduction mean different things.
- Can existing basis, lifecycle and rule mechanisms express the selected
  assumptions? Demonstrate a gap before chartering an extension.

Use [2025 Publication 936](https://www.irs.gov/pub/irs-prior/p936--2025.pdf)
to orient the inquiry into acquisition debt, secured debt, limits and reporting.
Verify the exact provisions and 2025 reporting instructions before adopting
rule content. Current guidance is not a substitute for the selected year's law.

## Candidate demonstrations

Use synthetic accounts to compare a supported purchase case, a known different
use of proceeds, and an uncertain or mixed use requiring an explicit boundary.
Correct an answer while preserving the original document amount; withdraw it
and examine the selected default policy. Check an additional statement or
borrowing as a boundary case without presuming the singleton limit is lifted.
Preserve an unrelated student-loan account.

Include a case where mortgage interest changes the chosen return deduction and
one where the standard deduction remains larger. The explanation must not claim
a tax saving merely because interest qualifies for Schedule A. Specific expected
outcomes follow the selected tax and product contract.

## Contracts, tracks and verification

Track 0 is PENDING. It settles the tax proposition, ordinary input, relationships,
change semantics, assumption behavior and return integration. Independent review
examines that connected result before the first production charter. ADRs and
schema successors follow actual contract changes.

Provisional production divisions are recording and translation, calculation
integration, and the interaction with saved explanation. The foreman may combine
or split them after tracing the path; they are not build charters. Prototype
rivalry is conditional on an unresolved, testable design choice. Final publication
receives independent review under the existing process.

Verify synthetic inputs through production recording and live calculation,
package validation and saved reader output. Characterize existing Form 1098
behavior and preserve unaffected routes. Follow the repository's applicable
test lanes and publication checks. Manually supplied relationships or conclusions
must remain visible limits on evidence. Follow existing synthetic-data rules.

## Completion and stopping points

Complete means the ordinary circumstance is obtained and recorded, the tax rule
uses it in the adopted route, its result reaches Schedule A and the bounded
return calculation, and a saved explanation shows the answer and basis used.
Correction and recovery preserve the account's meaning. State supported cases,
adopted assumptions and adjacent limits plainly.

If investigation exposes a larger prerequisite or substantial allocation work,
bring back its product consequence and the smallest useful alternative. A partial
result preserves learning but does not satisfy the phase's delivered-breadth
endpoint. Neither a general household model nor a universal assumption framework
is silently added to this milestone.
