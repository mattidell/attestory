<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-interest-circumstances",
  "retrospective": "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
  "status": "Closed 2026-10-15. A bounded synthetic Form 1098 account records ordinary answers about one home borrowing, calculates the supported interest treatment, names uncertainty and unsupported conditions without paying an amount, and saves an explanation that can be corrected. The next milestone is unselected.",
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
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md#Actions the team will take",
      "docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md#Actions the team will take"
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

The milestone succeeds only if four things hold together for the bounded
case:
- the person can give understandable ordinary answers;
- the application translates them into tax meaning;
- it calculates the bounded result;
- the person can inspect and correct the saved account.

Calculation evidence built from direct synthetic assertions shows the third
part only. A design that drops any part is incomplete, however well the rest
composes.

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

P0 has since run the present path on the adopted package; its account of
current behavior is in the evidence directory. Student-loan recording,
per-subject evaluation, basis explanation, correction and recovery provide
reuse candidates, not an already-proven mortgage route. The mortgage
branch also has complete-return and standard-versus-itemized dependencies.

## Actions the team will take

The sections through Track 0 are the investigation as each step closed.
The execution record and outcome at the end are the closed result. Working
charters, interim reviews, the process log, and probes that the retained
design does not cite were removed at curation. Their conclusions are kept
here, in the design account, and in the retrospective.

### Production review and repair

The independent production review required the repairs below and qualified
the earlier Foreman acceptance. Its candidate check passed 2,961 tests and
failed full typing on four errors in two test helpers. The earlier scoped
typing result was not complete-candidate typing verification. The subsequent
independent repair review accepted the repaired semantic result. It did not
accept a publication verdict.

### Production-review repair

1. Fix the four typing errors, repair the README heading, and demonstrate the
   incremental entry boundary. The nine-answer batch save remains available;
   the single-answer API may build an incomplete account or restore an account
   after withdrawals. Missing required answers block. No arbitrary minimum
   current-answer count is added.
2. Preserve choice 4 rather than narrow it: uncertainty about liability,
   certificate receipt or original-loan status must identify that condition,
   not masquerade as a known unsupported circumstance. Keep the amount blocked.
   Give the known unsupported cases named explanations as well, without adding
   calculations for them. Clarify zero reasons and the older-debt limit caveat.
3. Make saved ordinary answers recognizable through adopted content, preserving
   normalized values, exact source provenance and the distinction from defaults.
   Establish the bounded version/adoption path before changing content. Existing
   v44 and its publication artifacts remain reproducible; the successor must
   actually be exercised through recording, calculation and saved display.
4. The 2025 Publication 936 "Married taxpayers" passage (printed page 5)
   confirms that ownership by either spouse can satisfy the joint-return home's
   ownership aspect. Clarify that question. Residence remains this route's
   common main-home account for the filing unit, not an inference that either
   spouse's separate home is necessarily the supported case. The "Main home"
   passage (printed page 4) provides the ordinary residence definition.
   [Year-specific source](https://www.irs.gov/pub/irs-prior/p936--2025.pdf#page=5).
   Implementation inspection found a further distinction: the earlier
   ownership and residence inputs describe the respondent personally. The
   broader filing-unit propositions therefore receive distinct input fact
   IDs, not merely new labels on those old assertions. The successor requires
   the new answers; a v1-only account does not establish them. Preserve v44
   and the v1 questions. Explicit v2 recording supplies the new bounded account;
   automatic migration of older answers is not part of this repair.
5. Have the repaired semantic surface independently reviewed, then curate the
   final publication candidate and obtain its final review and green CI. Browser
   inspection remains deferred; no visual observation is claimed.

The repairs preserve the four-part product goal and the calculation boundary;
they correct inconsistencies in its explanation and evidence. A small entry
clarification is recorded explicitly rather than presented as a new tax rule.

The verification unit is complete: repository mypy checks all 349 files,
the three affected focused modules pass 26 tests, and the final targeted
incomplete-entry test reads the saved amount-rule disposition as blocked.
The README headings are corrected. These are local results, not a new green
CI claim. The explanation unit began with a reviewed version/adoption outline.

The production repair built the new content and package versions, the
explicitly selected broader input questions, the exact answer descriptions,
and the saved-page adaptation, then committed the regression evidence. The
new module passed seven tests and nineteen subtests; after strengthening
two methods, those changed methods passed two tests and eight subtests. The
unchanged methods were not rerun. Complete repository typing passes all 350
files. Independent source, integrity, and committed-evidence review accepts
the repair with no material defect remaining. A nonblocking ownership-reason
wording note does not change the distinct input, offered question, or saved
answer meaning. The pre-push fixture and envelope checks pass fourteen tests
and five subtests; the scoped envelope scan is clean. No green full-suite
result is claimed for this candidate.

### Production delivery before independent review

The connected design is independently accepted and ADR 0078 is accepted.
Track 1 provides the production vocabulary and defaults. Its reviewed tests
separate durable answer admission/correction/retraction from a synthetic
consumer package exercising real validation, material resolution, marshalling
and both runners. No adopted mortgage calculation or recorder is claimed by
that evidence alone. Track 2 now connects those citizens to core package v44's calculation and unresolved
indicator. Foreman review found no outstanding material defect in the bounded
calculation: focused live cases cover qualified amounts, three justified
zeros, unresolved treatment, current-only correction and unrelated student-loan
behavior. These tests supply ordinary answers directly, not through a recorder.

Track 3 now provides the saved explanation. Foreman review repaired a material label
error that confused reported interest with the calculated deduction. The reader
keeps those amounts distinct, labels document values and ordinary answers,
and shows a default only when the account's actual dependency pins reach it.
Qualified reported zero and the three justified-zero reasons retain different
accounts. The exact producing rule supplies the declared basis; no tax is
recomputed by presentation.

Focused and local full regression checks passed on the repaired reader.
The earlier restricted-run retries are not claimed as a green full run;
the later complete run supplies the local regression evidence. The browser
harness could not start its local server, so no visual mortgage-page observation
is claimed. Final CI remains the release gate. Track 4 now supplies the recording/correction operation and is Foreman-reviewed.
Its finite question and review model is a bounded callable
interaction, not a new general browser UI. Review tightened every public
mutation to the one current statement and selected answer set. It also
separated an absent answer and its declared default policy from evidence that
a saved calculation actually used that default. The saved review validates
the presentation and joins its run to the durable run-revision record;
unresolved results reuse the existing statement-specific explanation rather
than pretending to be completed accounts.

The acceptance evidence must use the actual recorder, durable log, coordinator
and reloaded presentation. Direct-assertion calculation tests remain separate
evidence. In particular, the unrelated account retained in the recording
fixture is the native closed-empty Form 1098-E closure account; Track 2's
populated student-loan compatibility test does not become recorder evidence.
The focused recording/review modules pass 13 tests and 3 subtests. They cover
real contribution admission, interrupted atomic saves, singleton/direct API
refusals, timing relevance and current support, an actual joint-return case,
qualified/partial/qualified results, justified zeros, withdrawal and re-answer,
malformed or stale reviews, and saved-run association. Typing and the scoped
synthetic-fixture/envelope tests pass. The earlier broad fast-lane run had
remaining budget overruns in unchanged test paths; no baseline comparison
established their cause, so it is not a green regression result. Final CI must
settle the complete candidate's gate.

That repair closed the tax-design work. It did not claim a publication
verdict or a green full-suite result. The supported boundaries and the
absence of browser observation stay explicit in the outcome. The four-part
goal above is unchanged. The completed investigation below explains the
choices; its earlier open-state statements are historical, not instructions
to restart that work.

**Production ordering clarification.** The selected unresolved indicator
recognizes four completed outcomes, while the present reader accepts only one
expected categorical value and throws on the genuinely unresolved path.
Track 2 therefore includes the already-selected nonempty expected-set reader
compatibility change and its regression tests. This moved one dependency from
unit C forward; it changed no product decision. Track 3 subsequently built the
general basis loader, completed-zero account and lender label. Track 4 remains
the recording/correction operation. The milestone is not complete after
calculation or after an explanation built on direct synthetic assertions.

### Completed iterations

**P0, the baseline.** On adopted v42 a single Form 1098 reaches line 8a, line
12e and line 15 only if the person answers yes to eight confirmations. A
missing or "no" acquisition-use answer blocks line 12e and line 15, while the
standard deduction is computed but not selected. Fixture defaults supply the
demographic answers and the legacy itemized amount. The configured $15,000
standard deduction is not the verified 2025 amount. See the P0 baseline and its re-review.

**P1, what the person knows against what the rule needs.** The circumstance account sets each 2025 condition of the opening case beside its possible sources. The
purchase and personal-expense arms each have a determined 2025 answer. Four
confirmations are legal conclusions the person is asked to affirm; four are
software coverage limits. Security has no confirmation at all. Uncertainty
cannot be recorded, and the vocabulary declares box 11 wrongly and drops the
property address. After review,
the account was corrected to cite the 2025 text of §163 rather than the
later compilation, and to source the ownership requirement.

**P2, mechanism fit.** The mechanism-fit account and its live probe show that the existing rule machinery can carry choices
1–6 with new content: ordinary-statement fact types with a "can't tell"
value, a successor line 8a, and a determined adverse result that publishes
zero so line 12e selects the standard deduction. Missing and withdrawn
answers still block. After review,
the explanation cost was split. Blocked results can already carry their own
wording as content. Two engine gaps remain: showing a rule's basis, whose
reader is implemented only for student-loan rules although ADR 0077 Part 2
describes it generally, and a sentence attached to a published line 12e
value. Choice 8 takes on the reader and leaves the line 12e sentence to the
connected design. In the explanation, a disallowed statement currently
looks the same as a zero-interest one.

**P3, the connected design.** The [first draft](mortgage-interest-circumstances-evidence/p3-connected-design.md) was reviewed and sent back. The review also found that the adopted v42 line 8a rule never
reads box 2, so a principal over the limit deducts the whole interest today.
That defect is recorded and awaits the owner's disposition; it is not repaired
here. The revision read box 2 directly, consolidated four line 8a rules into
one, split liability from payment, and drafted the Track 0 closure artifacts.
Its probe ran the consolidated rule.

The owner's review of the revision found that it does not yet support the
stated boundary. A personal-expense answer published zero even for a 1986
loan, a refinance and a two-property statement. Uncertain ownership was
treated as unsupported coverage. Determined zeros were explained through the
blocked-result field. "I owe the loan" was required but given no purpose. The
box 9 probe ran a different arrangement from the one proposed. And no unit
obtained the person's answers. The [design account](mortgage-interest-circumstances-evidence/design-account.md)
records each change and what kind of change it is.

### Design refinement before production

Track 0 remained open for P4, which repaired the connected design against
the revised choices after a review of the proposed next action. The following
iterations developed that design through P7's independent acceptance.

Two revisions make existing intentions more specific:
- The four-part goal above.
- Choice 9's rule that each conclusion lists the conditions it needs, and that
  the amount and the explanation follow one table.

Four revisions change earlier choices, each for a stated reason:
- **Choice 3.** The determined zero now needs timing and grandfathering
  established, because P1's exceptions apply to the same use.
- **Choice 7.** The date stop on the debt limit is withdrawn, because the
  strictest limit can only under-claim.
- **Choice 8.** Completed conclusions are shown with their own basis, not
  through the blocked field, because that is a product distinction an engine
  constraint should not erase.
- **The supported boundary.** It no longer claims the owner who paid without
  being on the note, because the coverage condition excludes that case.

P4 establishes:
1. **The condition table.** For the supported conclusion and each determined
   zero, list the conditions each needs. Say which adverse facts are
   decisive, and which coverage or uncertainty conditions prevent them.
   Establish against authority whether "I did not pay" and "not collateral"
   are decisive. Apply one table to the amount rule and the conclusion rules.
2. **Ordinary timing questions.** Write the questions, asked only when the
   money did not buy the home, that place an account outside the 90-day and
   building windows without asking the person to recognise either.
3. **The date prerequisite.** Specify the narrow date comparison that
   grandfathering needs, with its ADR and schema cost. Compare it with
   withholding the determined zero for this milestone, and recommend one.
4. **The conclusion carrier.** Specify one conclusion publication per kind of
   conclusion, each with its own basis, beside one amount rule. Specify the
   presentation section that shows the answers, the conclusion and the
   basis. Keep the blocked field for unresolved and unsupported results only.
5. **Liability.** State the supported boundary, and the explanation for an
   owner who paid without being on the note.
6. **The successor arrangement.** Specify the package-level box 9 default on
   the unchanged vocabulary, and show that existing recorded box values still
   resolve. Run the probe on exactly that arrangement, and list any remaining
   stand-ins.
7. **The recording operation.** Specify the bounded operation through which
   the person identifies the statement, answers, saves, corrects, withdraws
   and reviews. Model it on the student-loan recording and review operations,
   and assign it to a production unit.
8. **Probe and closure.** Run the riskiest combinations through the real
   coordinator, and revise the six Track 0 closure artifacts to match.

**What P4 does not establish:** acceptance, or a production charter. The
repaired design goes to an independent re-review. Track 0 closes only when
the design and its evidence support the stated boundary.

The owner's decision on the date prerequisite, and on the v42 debt-limit
defect, may redirect P4's output. Neither blocks drafting it.

This plan revision, the revised design account, and the P4 charter were reviewed together before assignment. Both of its corrections are applied. The conclusion
carrier must not let two rules publish the same conclusion, and the probe
pairs two decisive adverse facts. Choice 6's added dependence on the timing
questions is now recorded.

**P4 outcome.** The [repaired design](mortgage-interest-circumstances-evidence/p3-connected-design.md)
carries the condition table, the ordinary timing questions, liability as a
condition, the recording operation as a specified unit, and closure artifacts
that pass five of the gate's six tests. The re-review accepts it only with corrections, and the foreman confirmed its two
code-level findings:
- Uncertain ownership, residence or share still reads as outside coverage,
  against choice 4.
- The named reader fixes would leave a determined zero with no account at
  all; a third reader change is needed.
- The personal-expense zero still publishes for a grandfathered loan, which
  is neither option choice 3 allows.
- A spouse on a joint return is not addressed.
- The box 9 default cannot be added without changing the vocabulary.
- The constructive-payment case is missing from the known limitations.

**Owner decisions.** The owner approved fixing both now. Two units run in
parallel on disjoint files:
- A fix to the adopted line 8a rule, so that it reads box 2. It ships as core calculations v43 and release v41.
- The [date comparison capability](mortgage-interest-circumstances-evidence/charter-date-threshold-capability.md):
  one operator, `rule-artifact.v14`, and a proposed ADR. It is not adopted
  into any package.

Each gets an independent review of its result. Both follow the owner's
explicit direction to start now, so neither has a pre-execution planning
review.

**Progress.** Two owner-approved units are complete and independently
reviewed:
- The line 8a fix is accepted. Core calculations v43 and release v41 now apply the debt
  limit.
- The date comparison is accepted. It adds the `date_compare` operator in `rule-artifact.v14`
  and `artifact-package.v36`, under ADR 0078. The ADR is proposed and
  awaits the owner's acceptance. The review asks the owner to note that the
  operator's left side admits any expression, which the ADR discloses.

The owner's two timing findings are carried by P5.

**P5 outcome.** The [corrected design](mortgage-interest-circumstances-evidence/p3-connected-design.md)
carries grandfathering through the reviewed date comparison, with equality
counting as grandfathered. Absent and withdrawn timing answers reach "not
established", never the zero. Box 9 becomes a v2 successor whose existing
values still resolve. The re-review confirmed these on a 35-case probe and accepted the design with three
corrections:
- the building question's "shortly" can falsely clear the exception;
- the spouse clarification is not in the question text;
- "can't tell" on collateral and on payment still reads as outside coverage.

**Next action.** P6 applies the three corrections, following the design account's provisional
wording and scope, and probes a building boundary case and a joint filer.
It is a content-only correction, under the same pre-execution review. Track
0 closes if the design re-review then finds the boundary supported, and the
owner accepts ADR 0078.

The P6 planning review corrected the three-year premise: completion timing and the expense cap are
different tests. P6 now applies the completion question with project-stage
and mortgage-date help, the spouse interpretation in all three actual
questions, and the two uncertainty reasons. The design account records the
timing rationale as corrected by evidence; it is not a change in milestone
purpose. The P6 builder's 49 named prototype results include 17 ordinary-answer
and stored-answer observations. The corrected completion cases, purchase
directions, joint-spouse account and two uncertainty reasons match the expected
outcomes. These are synthetic coordinator observations, not recording or human
intake evidence. Independent re-review found the timing correction sound but returned three bounded findings.
The named joint-filer fixture still stored `single`, and the stock example
was stored as personal expenditure. Correcting these changes the evidence,
not the product aim. The payment counterexample is more consequential:
listing third-party payment as outside coverage did not stop a literal
"I didn't pay" from producing zero.

**Current action.** P7 applies the review's small exclusion and corrects those fixtures. The person
can say somebody else paid some/all, or that they paid only part; the route
then leaves treatment unresolved without recording another payer or calculating
gift treatment/allocation. The genuinely negative answer is narrower, and
uncertainty remains distinct. This develops the existing requirement that a
zero be justified; it does not expand the milestone to multi-person accounting.
The design account records the value, cost and conservative boundary. Review
the changed outcomes and correction reach before closing Track 0. ADR 0078's
owner acceptance remains separate from these routine corrections.

**P7 build observation.** The targeted coordinator cases now leave third-party
and partial payment outside coverage without an amount. The narrowed negative
still yields zero and uncertainty remains open. The direct-assertion correction
trace moves support from the original answer to each current successor, with
old support absent. Actual MFJ now selects the configured `30000` deduction
while line 8a is `20000`; the actual investment example records `other` and
blocks. These are synthetic prototype observations, not production recorder
or reader delivery. Focused independent review accepted the repair in its report.
No material finding remains on the bounded connected design. The record now
distinguishes tested prototype behavior from the recorder and reader still to
be implemented.

**Track 0 handoff (historical).** ADR 0078 is accepted and Track 0 is closed on the
P7 independent review. Track 1 builds unit A (statement vocabulary/parameters) from the connected design's
production divisions. Continue with unit B's adopted
calculation package, unit C's basis/explanation and unit D's saving/correction
operation. Keep their test obligations separate from the design probe: the
milestone is not delivered until its four-part product goal works through the
real recording path and saved result. No new tax area or broader payer model
is part of this continuation.

The earlier repair action was reviewed before execution. P6 and P7 supplied the subsequent corrections and independent
acceptance; those, rather than the earlier readiness claim, close the design.

### Provisional sequence

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

Maintain a short, evolving [design account](mortgage-interest-circumstances-evidence/design-account.md)
of consequential product choices. It explains how ordinary answers, canonical
tax concepts, assumptions and conditions left with the person fit together,
why we chose that arrangement, and what materially different alternatives we
set aside. Keep open questions distinct from selected designs. When a choice
changes, preserve the reason rather than a narration of every repair.

This is not a catalog of review findings or an additional approval ceremony.
Execution discrepancies and unexpected unresolved cases belong in evidence
and review records unless they change the product model or a consequential
design choice. Link to any eventual contract rather than restating it. Review
this account alongside each planning iteration as its understanding develops.

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

Track 0 is complete: the [connected design](mortgage-interest-circumstances-evidence/p3-connected-design.md)
settles the tax proposition, ordinary input, relationships, change semantics,
assumption behavior and return integration, as corrected and independently
accepted in P7. ADR 0078 is accepted. This is design readiness, not a claim
that the production mortgage route exists.

Production follows its four divisions: Track 1 vocabulary/defaults (A),
Track 2 calculation package (B), Track 3 explanation (C), and Track 4 saved
recording/review (D). Each unit uses the lean Builder/Foreman review loop;
independent final-publication review remains required. A genuinely new design
question returns to review rather than being hidden in implementation.

The first production bundle uses `tax.us.2025.f1098-successor.vocabulary`
version `v1`: the prototype's `v3` was an experimental round label, never a
published production citizen. Fact identifiers and their declared semantics
stay unchanged. Box 9 really has an existing production `v1`, so its new
default remains a genuine `v2` fact-type successor. This is publication
normalization, not another tax or input-model decision.

The connected design's divisions include the interaction through which the
person supplies and corrects the account; the initial design had omitted it.
Their scoped work orders are committed before each build. Prototype
rivalry is conditional on an unresolved, testable design choice. Final publication
receives independent review under the existing process.

## Track 0 adversarial closure

The evidence lives in the connected design's section 9 tables and declaration;
the P7 review independently
accepted the final delta. ADR 0078 acceptance closes the remaining prerequisite.

- Authority-lifecycle table: PASS — connected design section 9.1, including
  corrected payment meaning, statement keys and reserved timing defaults.
- Empty/nonempty authority matrix: PASS — section 9.2 and its measured
  nonempty, excluded and closed-empty cases; P7 adds the payment exclusion.
- Late-member lifecycle: PASS — section 9.3; the current singleton bound and
  family authority remain explicit rather than inferred from the count.
- Neighboring capability dependency diff: PASS — section 9.5; no new mortgage
  answers on a no-mortgage or unrelated student-loan route.
- Reused-claim semantic/lifecycle equivalence: PASS — section 9.4; box 9 is a
  real successor, not mutation of its prior declaration.
- Integration surface: PASS — section 9.6; one amount producer satisfies the
  attachment cardinality, with prototype observations for distinct dispositions.
- Known limitations affecting correctness: no unresolved design finding within
  the selected bound. At Track 0 close, production still had to implement the
  calculation, all three reader changes, and the recording operation;
  prototype stand-ins did not satisfy those gates. The execution record is
  that later work. Third-party and partial payment, allocation, grandfathering
  beyond the fixed-date check, and the other excluded cases keep their
  reviewed conservative disposition rather than silently receiving an amount.

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

## Execution record

| Unit | Result |
| --- | --- |
| Track 0 | The connected design, corrected through P7, is independently accepted. ADR 0078 is accepted. |
| Debt-limit repair | The adopted line 8a rule reads box 2. Core calculations v43, registry v41, and release v41. Independent review accepted the repair. |
| Date comparison | `date_compare` on `rule-artifact.v14` and `artifact-package.v36`, under ADR 0078. Independent review accepted it. The operator's left side admits any expression; the ADR discloses that. |
| Track 1 | Production vocabulary and defaults. The reviewed tests separate durable answer admission from a synthetic consumer of validation, resolution, marshalling, and both runners. That evidence alone does not adopt a calculation. |
| Track 2 | Core calculations v44 calculates the bounded treatment and the unresolved indicator. Focused cases cover a qualified amount, three justified zeros, unresolved treatment, current-only correction, and unrelated student-loan behavior. Those tests supply ordinary answers directly. |
| Track 3 | The saved explanation keeps reported interest distinct from the deduction, labels document values and ordinary answers, and shows a default only when the account's pins reach it. No browser observation is claimed. |
| Track 4 | Recording and correction use the real admission path, the durable log, and the saved reader. The finite question model is a bounded callable interaction. |
| Production review | Revise. Typing failed on four errors in two new test helpers. Three "can't tell" answers were reported as outside coverage. Zero descriptions omitted part of their basis. Saved tokens hid the offered answer. The debt-limit sentence omitted the older-debt caveat. Joint-return ownership needed distinct filing-unit inputs. |
| Repair | Core calculations v45, registry v43, and release v43 name those conditions and keep the amount blocked. The independent repair review accepted the semantic result. It did not accept a publication verdict. Local typing passes all 350 files. No green full-suite result is claimed. |

## Outcome

**What a person can do.** On a synthetic account, prepare a review of one
current Form 1098 statement, record the ordinary answers, save, correct, and
withdraw them, and read a saved explanation beside that statement. The v2
question set asks filing-unit ownership and a shared main home as distinct
inputs. The v1 questions and the v44 route remain for historical records. A
v1-only account does not establish the v2 inputs. For a personal-expense
answer, the two timing questions may be answered or left absent. Absence is
not an answer offered to the person.

**What the calculation does.** Qualified interest can reach Schedule A line
8a. A justified zero publishes zero. Uncertainty about liability, certificate
receipt, or original-loan status is named, and the amount stays blocked.
Refinance, a property count other than one, other use, a non-owner, a
non-main-home, an outside co-obligor, and third-party or partial payment are
named and blocked. An over-limit principal blocks, and the explanation says
that older debt may have a higher limit while this route uses its stricter
bound. The v43 repair makes the earlier confirmation route read box 2. The
circumstance route reads box 2 directly. ADR 0078's fixed-date comparison
places the grandfathering check; it does not decide continuous security or
a later refinancing.

**Evidence.** The retained design account and connected design hold the
Track 0 choices and the probe results those documents cite. Production
behavior is in the vocabulary, calculation, explanation, and recording tests,
and in the regression evidence for the v45 repair. README, "Mortgage
statement answers", is the runnable account of the review operations.

**Limits.** One current statement. No allocation, no mixed-use amount, no
multiple mortgages or homes, and no mortgage-credit computation. No browser
observation of the page. The configured standard deduction, $15,000, or
$30,000 when married filing jointly, is inherited and is not the verified
2025 amount. The correction session does not carry this route. No green
full-suite result is claimed for this candidate. The phase's contrasting tax
area is unselected.

Working charters, interim reviews, the process log, and probes the retained
design does not cite were removed at curation.
