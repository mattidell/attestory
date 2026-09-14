<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-interest-deduction-translation",
  "milestone_state": "closed",
  "status": "CLOSED EXPLICITLY PARTIAL 2026-09-14. A completed bounded investigation with no production path. P0 settled, P1 selected and reviewed, P2 reviewed, P3 reviewed as a decision-ready partial design with obligations 2a and 2b undischarged. Track 0 and all production tracks were not started; no production code, content, schema, or package version was written and the coverage frontier is unchanged. The demonstrated result: no committed path can currently use every current Form 1098-E box-1 statement as the iteration subject, require exactly one usable statement association, resolve the heterogeneous related facts this case needs, fail closed on an unassociated statement, and preserve statement-isolated dependencies. The actual pairing dispatcher iterates existing pairing records, so an unpaired box-1 statement is never visited and produces neither a publication nor a blocked row. Three capability gaps are named and preserved in the deferral ledger.",
  "scope": [
    "completed: a plain-language product map and a classification of all thirteen Form 1098-E and SLI-scope answers",
    "completed: a tax-boundary record for ten decomposed section 221 constituents, and selection of eligible-student status under section 221(d)(1)(C) on a narrow production promise",
    "completed: a map of committed artifact and consumer behavior for the 2025 standard worksheet at the examined source state",
    "completed: a partial design and a reproducible executable probe establishing the bounded dispatcher and coverage failure",
    "not started: Track 0 and every production track; no implementation of the selected slice"
  ],
  "non_goals": [
    "no complete ontology or implementation of every qualified-education-loan, education-expense, repayment, employer-assistance, QTP, related-person, or dependent-status case",
    "no assumption that a Form 1098-E amount is itself the deductible amount or that the current five per-statement eligibility assertions are suitable user questions",
    "no rewrite of the existing worksheet arithmetic, Schedule 1 composition, or AGI path unless a reviewed case proves the current behavior cannot carry the selected ordinary-fact consequence honestly",
    "no Form 2555, Form 4563, Puerto Rico, American Samoa, Form 1040-NR, repayment-exceeds-benefits, filing, or production UI expansion",
    "no universal person, household, education, loan, payment, or relationship ontology unless the selected case demonstrates that a bounded representation cannot be honest",
    "no claim that one contrasting concept proves the translation method universal",
    "no production implementation was attempted or delivered; this milestone closed explicitly partial",
    "no general grouped-rule or evaluation-context contract was designed here; that is the proposed prerequisite",
    "no authoritative institutional-catalog mechanism was decided; it is a separate required blocker"
  ],
  "deep_reads": {
    "planning": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Plain-language purpose",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Planning gates",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Fixed cases",
      "docs/milestone-retrospectives/2026-09-12-nominee-interest-return-integration.md",
      "packages/content/tax/2025/f1098e.bundle.json",
      "packages/content/tax/2025/sli-scope.bundle.json",
      "packages/content/tax/2025/rule.sli-worksheet.json",
      "packages/content/tax/2025/rule.schedule1-line26.json",
      "packages/content/tax/2025/package.core-calculations.v38.json",
      "PROJECT_PLANNING.md#Lean Production Loop",
      "PROJECT_PLANNING.md#Track 0 Adversarial Closure Gate",
      "AGENTS.md#Data Safety Rules"
    ],
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Selected product boundary",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Success and stop conditions",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0038-qdcg-worksheet-and-declared-absence.md",
      "docs/adr/0064-expression-language-extension-arithmetic-and-categorical.md",
      "docs/adr/0065-schedule1-part-ii-completeness-and-line26-composition.md",
      "packages/content/tax/2025/f1098e.bundle.json",
      "packages/content/tax/2025/sli-scope.bundle.json",
      "packages/content/tax/2025/rule.sli-worksheet.json",
      "packages/content/tax/2025/rule.sli-worksheet-line1-subtotal.json",
      "packages/content/tax/2025/rule.schedule1-line26.json",
      "packages/content/tax/2025/rule.form1040-line11.v2.json",
      "packages/derivation/live.py",
      "packages/derivation/marshal.py",
      "packages/derivation/evaluator.py",
      "packages/derivation/presentation_projection.py",
      "PROJECT_PLANNING.md#Lean Production Loop",
      "PROJECT_PLANNING.md#Payload Instantiation Gate",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "OWNER_MODEL.md#The Product Model",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Plain-language purpose",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Selected product boundary",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Track 0 adversarial closure",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-09-14-student-loan-interest-deduction-translation.md"
}
-->

# Student Loan Interest Deduction Translation

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `student-loan-interest-deduction-translation`
- Primary branch: `milestone/student-loan-interest-deduction-translation`
- State: **CLOSED EXPLICITLY PARTIAL 2026-09-14**
- Retrospective:
  [`2026-09-14-student-loan-interest-deduction-translation.md`](../../../milestone-retrospectives/2026-09-14-student-loan-interest-deduction-translation.md)
- The sections below the execution record are the **original plan**, retained as
  historical context. The header, execution record, and deferral ledger describe
  the closed candidate.
- Roadmap role: first contrasting tax concept after the completed taxable-
  interest vertical

## Plain-language purpose

The current engine can take Form 1098-E interest, apply a cap and income
phaseout, and place a bounded Student Loan Interest Deduction on Schedule 1.
But the document amount is not enough to establish the deduction. The result
also depends on facts about the loan, the borrower, the education, who paid,
other education benefits, dependent status, filing status, and modified
adjusted gross income.

Today those boundaries exist in the workspace vocabulary as tax-shaped answers
such as “no related-person interest,” “no non-qualified-loan component,” or
“no QTP earnings used.” P0 established that no dedicated production producer
creates any of them: outside tests and one golden generator, nothing turns a
user's account into one of these assertions, though the kernel's generic
contribution boundary would admit one if something prepared it. So the milestone
builds the first such producer rather than swapping out a question the product
asks today. Those labels may be useful inside a rule, but they are not evidence
that the application can ask an ordinary person a comprehensible question,
preserve what actually happened, and derive the tax consequence for itself.

This milestone selects one of those current gates as a forcing case and builds
one honest translation from ordinary circumstances to the existing deduction
result. The gates do not all serve the same statutory operation: the concluding
sentence of § 221(d)(1) excludes related-person and qualified-employer-plan
indebtedness from the qualified class, its chapeau and subparagraphs (A)–(C)
state what a qualified education loan is,
§ 221(e)(1) reduces an otherwise allowable deduction by an excludable amount,
§ 221(c) dependent status decides whether this return may claim anything, the
legal-obligation requirement attaches to the indebtedness rather than to the
filer, and three of the current answers only tell the taxpayer which worksheet
the instructions direct them to. P0 separates them; P1 selects among them. It is deliberately smaller than “model student loans.” Its value is to
show whether the method proved by accrued and nominee interest transfers from
an income adjustment to a deduction whose amount also depends on another
calculated quantity.

**The selected case, in plain language.** Someone borrowed money for school and
is paying interest on it. Whether that interest is deductible depends in part on
something the lender never sees: whether the person was actually a student —
enrolled in a degree or certificate program, carrying at least half of what
their school calls a full load — during the term the borrowed money paid for.
The person can say where they went, what they were studying, which term the loan
covered, and how many classes they took. They should not be asked whether they
were an "eligible student," because that is a legal conclusion that also depends
on whether the school qualifies and on what that school counts as half-time.
The application works that out, and says so. Where it cannot establish the
school's status or the enrollment standard, it says that too, rather than
assuming the answer is favorable.

The full selection, including the narrow production promise and the loan and
academic-period identity cost it accepts, is recorded at
*P1 selection — eligible-student status*.

## Why this is next

The interest work now demonstrates a complete bounded path: preserve a report,
record an ordinary statement, derive a tax consequence, integrate the return,
and explain the lineage. Repeating the same shape on another interest
adjustment would mostly test the same assumptions.

The Student Loan Interest Deduction is a stronger contrast. Form 1098-E is
evidence of interest received by a lender, not a complete determination of the
taxpayer's deductible interest. The deduction is limited by taxpayer and loan
circumstances and then by MAGI. It therefore tests both halves of the product
model: translating ordinary life into canonical tax meaning, and composing
that meaning with other derived results.

The current implementation supplies a useful comparison target rather than a
blank slate. The milestone can preserve correct arithmetic while testing
whether the inputs and claims are honest. That makes the work smaller and more
diagnostic than opening a wholly unsupported deduction.

## Selected product boundary

The following product direction is fixed before implementation shape is
selected.

1. **The report is evidence, not the deduction.** A Form 1098-E amount records
   what the lender reported. It does not by itself establish that every dollar
   is qualified or deductible by this taxpayer.
2. **The user supplies ordinary circumstances.** The user should not be asked
   to certify a tax conclusion that the application can derive from more
   understandable facts. The planning gates must identify the exact ordinary
   proposition, speaker, scope, and correction behavior for the selected case.
3. **The rule owns tax meaning.** An adopted rule determines whether and how
   the selected circumstance changes qualified interest or eligibility. A
   user answer never masquerades as the product's legal conclusion.
4. **The existing worksheet remains a consumer.** The selected consequence
   must feed the current cap and MAGI phaseout and reach Schedule 1 line 21,
   line 26, Form 1040 AGI, and durable presentation through declared inputs.
5. **No invented negative fact.** Missing ordinary support means the selected
   route is unresolved or unavailable. It does not establish that the
   disqualifying circumstance is absent.
6. **Lifecycle stays meaningful.** Correction, retraction, and reassertion of
   the ordinary account affect later runs through current support. Historical
   assertions remain provenance, not live tax inputs.
7. **The result stays bounded.** One implemented circumstance does not prove
   every loan, expense, payment, borrower, education, coordination, or MAGI
   case supported.

## Starting committed state

This section is a baseline to verify during planning, not a claim that every
named field is an adequate product model.

- `package.core-calculations` v38 adopts the Form 1098-E family, its vocabulary,
  `tax.us.2025.rule.sli-worksheet-line1-subtotal`,
  `tax.us.2025.rule.sli-worksheet`, Schedule 1 line 21, Schedule 1 line 26, and
  the downstream AGI/form fields.
- `f1098e.bundle.json` records box 1, a box-2 companion, five per-statement
  categorical eligibility witnesses, and family closure. The five witness
  labels are tax conclusions or compressed statutory predicates; the bundle does
  not establish an ordinary-language interaction that supports them. Across both
  bundles there are thirteen fact types: ten eligibility and scope answers plus
  box 1, box 2, and the source-closure claim.
- `sli-scope.bundle.json` adds filer-level route and eligibility statements,
  including filing exceptions, dependent status, and legal obligation. All five
  are keyed by tax year alone. P0 found that filer scope is correct for
  dependent status but is a potentially lossy compression for legal obligation,
  which attaches to particular indebtedness.
- `rule.sli-worksheet.json` applies the $2,500 cap, filing-status/MAGI phaseout,
  standard-route gates, and per-statement all-equal checks. It computes a
  bounded Schedule 1 line-21 amount when every required input is available.
- ADR-0064 supplies the existing multiply, divide, and categorical collection
  operations. ADR-0065 supplies the current mixed Schedule 1 Part II
  composition. Neither ADR decides how an ordinary-life account becomes one
  of the current Student Loan Interest Deduction eligibility claims.
- P0 correction: the family closure attests that the recorded box-1 amount
  family is complete relative to the box-1 amounts on furnished Forms 1098-E.
  Its members are box-1 amount findings; it inventories no documents and does
  not establish which forms were furnished. It says nothing about how much
  student loan interest the taxpayer paid. A lender is generally
  required to file at $600 or more of interest for 2025 — the threshold does not
  prohibit a form below that — and § 221 has no deduction threshold, so interest
  below it may be deductible if the other requirements are met rather than being
  resolved either way by the absence of a form. The current closed-empty literal
  zero therefore asserts more than the closure supports, and puts a numeric
  deduction on the return path where the result is unavailable (F7).
- The current package proves bounded arithmetic and return wiring. It does not
  prove that the five per-statement tax-labelled answers are appropriate facts
  to solicit from a user or that one answer can honestly summarize every loan
  potentially aggregated on a statement. Where the current route blocks, the
  product withholds an otherwise potentially supportable result; that is an
  application refusal, not a tax-law zero.
- P0 correction: the adopted package establishes a consumer, not an entry path.
  Package v38 declares no `input_bindings` for the ten eligibility and scope
  answers — marshalling and consumer evidence about how an answer reaches a run,
  not about whether one can be created — and separately, the producer search
  found no dedicated production producer for any of them. The kernel's generic
  contribution boundary would admit a prepared assertion for any of these
  declared fact types; nothing prepares one.

Primary tax sources for the planning gate are 26 U.S.C. § 221, its regulation
26 CFR § 1.221-1, and the official 2025 Instructions for Form 1040/Schedule 1.
§ 1.221-1(b)(1) supplies the explicit legal-obligation rule, and § 1.221-1(b)(4)
governs interest paid by a third party on behalf of the legally obligated
taxpayer — both are controlling for the "obligation for the interest"
proposition and for the ordinary-fact questions about who was obligated and who
paid. IRS Publication 970 may explain the rules and supply examples, but it is
not treated as controlling law. The plan
does not yet select one current gate as the production slice.

## Planning gates

Planning is intentionally incremental. Each gate is independently reviewed
before the next one is treated as settled. Findings are repaired in the plan
section that owns the claim rather than accumulated into a final broad repair.

### P0 — product outline and claim inventory — **SETTLED 2026-09-12**

Drafted and repaired six times on owner direction. The owner waived further
independent review on 2026-09-12 and directed P1 to proceed; P0 is the factual
baseline for the later gates.

Throughout P0, two vocabularies are kept apart.

- **Tax consequence** is what the law does: indebtedness is a qualified
  education loan or it is not; the otherwise allowable deduction is reduced by
  an excludable amount or it is not; the taxpayer is eligible or the deduction
  for this return is zero.
- **Product disposition** is what the application does: publish a value,
  publish a computed or closure-backed zero, block, or leave the route
  unresolved.

A block is an application refusal — a statement that the product cannot support
a result on the evidence it holds. It is not a finding that the law allows zero,
and it does not take away a deduction the taxpayer is entitled to. A missing
ordinary fact is likewise a refusal, never a favorable answer.

A third distinction runs alongside these, about what a fact is evidence *of*.
**Source status** is what the workspace holds or does not hold — here, which
box-1 amounts are recorded under a completeness claim. A **tax result** is a
figure on the return path. Source status never establishes a tax result:
converting "this amount family is complete and empty" into a numeric zero on the
return asserts something the source evidence does not support. F7 is where this
goes wrong today. Note that the recorded amount family is not a document
inventory: a statement about which forms were *furnished* would need its own
evidence basis. Whether any source status is separately *rendered* to a reader
is a further question, unsettled here — see F7.

#### P0.1 Plain-language map

**What the form reports, and what it omits.** Box 1 reports the interest the
lender received during 2025 on one or more loans made to the borrower. It does
not identify who paid that interest. Box 2 reports one qualification about box 1
itself: whether the figure excludes loan origination fees and capitalized
interest on a pre-9/1/2004 loan. The form applies the reporting classification
*qualified student loan* to decide what to report; that classification governs
the lender's reporting obligation and is not the application's own deduction
determination. The form omits which loans the figure aggregates and in what
proportion, the borrower's relationship to the lender, what the borrowed money
paid for and for whom, who was enrolled and when, who made the payments, and
whether an employer or a tax-favored education program supplied any of them.

**What happened in the user's life.** The circumstances the deduction turns on
are ordinary events: who signed for the loan, what the money paid for, who was
in school, who made the payments, whether an employer or a 529 plan paid any of
it, and whether a parent still claims the user. A person can describe all of
that without knowing the word "qualified."

**What an adopted rule must determine.** The rule, not the user, decides which
ordinary circumstances bear on the deduction and through which statutory
operation. 26 U.S.C. § 221 uses several distinct operations, and one boolean
cannot stand for all of them:

- **Loan qualification.** § 221(d)(1) defines a qualified education loan
  through its chapeau — indebtedness incurred *solely to pay* qualified higher
  education expenses — and three subparagraphs: (A) the expenses were incurred
  on behalf of the taxpayer, spouse, or a dependent as of the time the
  indebtedness was incurred; (B) they were paid or incurred within a reasonable
  period of time; (C) they are attributable to education furnished during a
  period in which the recipient was an eligible student. A separate exclusion,
  in the concluding sentence following those subparagraphs, removes indebtedness
  owed to a related person, or owed by reason of a loan under a qualified
  employer plan or a contract referred to in § 72(p)(5), from the definition
  entirely. Such indebtedness is not a qualified education loan at all.
- **Denial for a doubly-benefited amount.** § 221(e)(1)'s **first** sentence
  allows no deduction for any amount for which a § 127 exclusion is allowable by
  reason of the employer's payment of indebtedness on the taxpayer's qualified
  education loan. This is a denial as to that amount, not a reduction formula,
  and § 127 covers the employer's payment of *principal or interest*.
- **Reduction for QTP earnings.** § 221(e)(1)'s **second** sentence reduces the
  deduction otherwise allowable under § 221(a) — expressly *prior to the
  application of subsection (b)*, so before the cap and the MAGI phaseout — but
  not below zero, by the § 529(c)(9) distribution earnings that QHEE treatment
  kept out of income. It too reaches principal or interest, not interest alone.

  These two sentences are different operations and P0 earlier treated them as
  one. The loan stays qualified under both; what differs is whether an amount is
  denied or the allowable amount is reduced, and where in the worksheet order
  that happens.
- **Return-scoped eligibility.** Dependent status under § 221(c) is a fact
  about this return and this taxpayer. When another taxpayer claims the filer,
  no deduction is available on this return at all, whatever the loans look
  like.
- **Obligation for the interest.** Under 26 CFR § 1.221-1(b)(1), only the
  person legally obligated to pay the interest may deduct it. This condition
  attaches to indebtedness, not to the filer as a whole: a taxpayer may be
  obligated on some relevant loans and not others, and Form 1098-E may aggregate
  interest across exactly that mix. It is listed separately from return-scoped
  eligibility for that reason. § 1.221-1(b)(4) separates obligation from payment:
  where a third party who is not legally obligated pays the interest on the
  taxpayer's behalf, the payment is treated as made to the taxpayer and then by
  the taxpayer. So "who paid" and "who was obligated" are distinct ordinary
  questions, and the form answers neither.
- **Worksheet selection.** The instructions direct a filer with Form 2555,
  Form 4563, or income excluded as a bona fide resident of Puerto Rico or
  American Samoa to Publication 970's worksheet rather than the standard one,
  because § 221(b)(2)(C) MAGI requires add-backs the standard worksheet does not
  compute. That is a direction about which instrument applies, not about whether
  the deduction exists. The application implements no Publication 970 route: an
  adverse answer on any of the three blocks the standard worksheet instead.

**How MAGI limits the amount.** Qualified interest is capped at $2,500, then
reduced on a straight-line ratio across a filing-status-keyed income band. The
engine's MAGI is `tax.us.2025.income.total-income` minus other Schedule 1
Part II adjustments — currently a literal 0, because no other Part II line has
a producer. The § 221(b)(2)(C) add-backs are not computed, and the alternate
Publication 970 worksheet is not implemented; an adverse answer on any of the
three worksheet-selection questions blocks the standard worksheet rather than
selecting another one.

**What the return shows.** The result publishes
`tax.us.2025.schedule1.line21-sli-deduction`, which Schedule 1 line 26 reads by
reference, which Form 1040 line 10 reads, which reduces AGI on line 11a.

**What must be refused.** If the product cannot establish qualification, line 21
must block or stay unresolved — never publish a silent zero and never pass box 1
through whole. That refusal is a statement about the product's evidence, and the
reader-facing account must say so rather than implying a tax outcome.

#### P0.2 Claim inventory

Every fact type in `f1098e.bundle.json` and `sli-scope.bundle.json`. The bundles
contain thirteen fact types: ten eligibility and scope answers (rows 3–7 and
9–13) plus box 1, box 2, and the source-closure claim. Each row is classified by
what the answer *is* and placed on the statutory axis it serves.

| # | Fact type | Scope | Classification | Axis | Basis |
| --- | --- | --- | --- | --- | --- |
| 1 | `f1098e.box1-student-loan-interest` | per statement | **reported fact** | source amount | The lender's reported figure for one or more loans; family member predicate; authorizes the line-1 subtotal. Does not identify the payer. |
| 2 | `f1098e.box2-checked-authority` | per statement | **reported fact** | amount composition | A reported amount-composition qualifier: it says whether specified loan origination fees and capitalized interest on a pre-9/1/2004 loan are omitted from the box-1 figure. Read off the form. Its domain is `{null, false}`, so a checked box never enters a run: the application refuses because it cannot reconstruct the omitted amount. Companion presence at kernel admission is the mechanism that enforces the fact, not the axis the fact sits on. |
| 3 | `f1098e.no-related-person-interest` | per statement | **tax determination** | loan qualification — concluding sentence of § 221(d)(1) | Asks the answerer to apply the related-person test — relatedness within the meaning of § 267(b) or § 707(b)(1), with constructive-ownership rules reaching the question only where those sections incorporate them — and report the conclusion. The exclusion sits in the flush language after subparagraph (C), not in a subparagraph. |
| 4 | `f1098e.no-qualified-employer-plan-interest` | per statement | **tax determination** | loan qualification — concluding sentence of § 221(d)(1) | Asks the answerer to classify the arrangement as a qualified employer plan under § 72(p)(4) or a contract referred to in § 72(p)(5). Same flush-language exclusion as row 3. |
| 5 | `f1098e.no-non-qualified-loan-component` | per statement | **compression of distinct predicates** | loan qualification — § 221(d)(1) chapeau and subparagraphs (A)–(C) | One `{yes, no}` stands for the whole definition: the chapeau's requirement that the indebtedness was incurred *solely to pay* qualified higher education expenses, plus (A) that those expenses were incurred on behalf of the taxpayer, spouse, or a dependent as of the time the indebtedness was incurred, (B) that they were paid or incurred within a reasonable period of time, and (C) that they are attributable to education furnished while the recipient was an eligible student. Classified from those predicates, not from the field title. |
| 6 | `f1098e.no-employer-educational-assistance-interest` | per statement | **tax determination** | double-benefit denial, § 221(e)(1) first sentence | The statute allows no deduction for any *amount* for which a § 127 exclusion is allowable by reason of the employer's payment — principal or interest, capped at § 127(a)(2)'s $5,250. The witness is a per-statement `{yes, no}` about box-1 interest and carries no amount. The "reduced (but not below zero)" language belongs to the *second* sentence, not this one. |
| 7 | `f1098e.no-qtp-earnings-used` | per statement | **tax determination** | amount reduction, § 221(e)(1) second sentence | The statute reduces the § 221(a) amount, prior to § 221(b) and not below zero, by the § 529(c)(9) earnings that QHEE treatment kept out of income, with respect to loans of the taxpayer. It reaches principal or interest; the witness asks a per-statement `{yes, no}` about interest only. |
| 8 | `f1098e.1.source-closure` | family horizon | **absence/completeness claim** | box-1 amount-family completeness (closure attestation) | Its members are box-1 amount findings. The claim is that the recorded family is complete relative to the box-1 amounts on furnished Forms 1098-E, as of the keyed horizon. Bounded to box 1 and its box-2 companion, and explicitly disclaims the eligibility components. It is not a document inventory: it neither identifies which forms were furnished nor establishes that none was — see F7. |
| 9 | `sli-scope.no-form-2555` | filer | **statement about the filer's own return composition** | worksheet selection | "Did you file this form" is close to ordinary once the form is named. Directs to the Publication 970 worksheet, not to ineligibility. |
| 10 | `sli-scope.no-form-4563` | filer | **statement about the filer's own return composition** | worksheet selection | Same. |
| 11 | `sli-scope.no-puerto-rico-or-samoa-income` | filer | **tax determination** | worksheet selection | Bona fide residence is a statutory test, presented as an absence claim. Like rows 9 and 10, an adverse answer blocks the standard worksheet; no alternate route is implemented. |
| 12 | `sli-scope.not-claimed-as-dependent` | filer | **tax determination over an ordinary substrate** | return-scoped eligibility, § 221(c) | The statutory test is legal; the underlying fact ("my parents claim me") is ordinary and statable. Filer scope is correct here: the condition is genuinely about this return and this taxpayer. |
| 13 | `sli-scope.legally-obligated-for-interest` | filer | **tax determination over an ordinary substrate, and a potentially lossy compression** | obligation for the interest | The committed fact is keyed by tax year alone, and the worksheet reads one adverse value to produce zero for the whole deduction. That is the current implementation's scope, not proof that the condition is filer-wide: obligation attaches to particular indebtedness, and a filer may be obligated on some relevant loans and not others while one Form 1098-E aggregates interest across the mix. Ordinary evidence such as whose name is on the loan may be useful support, but it is not itself the legal determination; 26 CFR § 1.221-1(b)(1) supplies the rule, and § 1.221-1(b)(4) makes clear that a third party's payment on the obligated taxpayer's behalf does not move the obligation. |

The twelve `schedule1-adjustments-scope.no-line*` witnesses are outside this
milestone's vocabulary but are read by the worksheet and by
`rule.schedule1-line26`. They are Schedule 1 Part II completeness claims, not
Student Loan Interest Deduction answers.

#### P0.3 Verified findings

Each was checked against the adopted package, the committed rule content, the
evaluator, and the marshalling path — not against labels.

**F1 — No dedicated production producer exists for the ten eligibility and
scope answers.** Three separable observations, deliberately not merged:

1. *Producer search.* Outside `tests/` and
   `tools/generate_f1098e_track8_presentation_goldens.py`, no module prepares or
   contributes any of the ten. The contrast is
   `packages/tax/nominee_allocation_recording.py`, a dedicated producer that
   turns an ordinary answer set into acts through the real contribution
   boundary. Nothing of that kind exists for this deduction.
2. *Marshalling and consumer evidence.* `package.core-calculations.v38`
   declares no `input_bindings` for any of the ten. This is evidence about how
   an answer reaches a run — the filer-level five through `marshal.py`'s
   unbound-symbol fallback, the per-statement five through `env.sources` — not
   evidence about whether one can be created.
3. *Generic admission is available.* The kernel's contribution boundary
   (`apply_contribution_batch`) admits a prepared assertion for any declared
   fact type. Nothing about these ten prevents admission. What is absent is the
   producer that would turn a user's account into such an assertion.

Consequence: this milestone builds the first such producer for this deduction
rather than displacing a question the product asks today.

**F2 — The per-statement witnesses carry no per-statement correspondence.**
`collect_categorical_all_equal` reads `env.sources[name]`, whose type is
`dict[str, list[str]]` — values only, with identity keys dropped. `marshal.py`
selects rows by fact-type match alone. The reproduced consequences are bounded:

- **C6 is defeated.** Two box-1 statements with one witness finding between them
  yield `rows == ["yes"]`; the universal test passes and the line-1 subtotal
  sums both statements. One statement's answer accidentally covers the other.
  The Track 6b repair removed assertion-order dependence; it did not establish
  coverage.
- **C3 still holds.** When the selected fact type is wholly absent, `rows == []`
  and the evaluator raises `BLOCK_ABSENT`. Total absence of the answer is still
  a refusal, not a favorable reading.
- **C7 remains unresolved, for a different reason.** Neither the witness
  identity keys (`lender`, `statement`, `tax-year`) nor Form 1098-E itself
  supplies per-loan correspondence. A statement aggregating several loans has no
  representable per-loan answer at all. The same gap reaches the filer-level
  answers: `legally-obligated-for-interest` is keyed by tax year alone, so a
  taxpayer obligated on some of a statement's loans and not others has no way to
  say so, and the single value the worksheet reads decides the whole deduction.
  P0 records the gap; it does not propose a loan identity design.

**F3 — Eight distinct gates collapse into one block code.** The five
per-statement witnesses and three worksheet-selection witnesses all raise
`SLI_UNIVERSAL_COMPONENT_VIOLATION`. The line-21 form field's blocked `explain`
is a four-way disjunction, and its declared `codes` list (`DEPENDENCY_ABSENT`,
`DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_UNCLOSED`) does
not contain any of the three `SLI_*` codes the rule emits — nothing in
`presentation_projection.py` enforces that list against `activeCodes`. This is a
limit on how a refusal is explained, not a tax error. It bears on C10: a reader
cannot learn which circumstance caused the product to withhold a result.

**F4 — Distinct statutory operations are represented by one product
disposition.** Loan qualification under § 221(d)(1), denial of a doubly-
benefited amount under § 221(e)(1)'s first sentence, and reduction for QTP
earnings under its second sentence are three different operations on different
objects. (the P1 obligation-and-amounts record established the split inside § 221(e)(1); P0 had treated
both sentences as one "reduce by an amount" rule.) The incumbent represents all
three, plus worksheet selection, as a per-statement or filer-level `{yes, no}`
whose "no" raises `SLI_UNIVERSAL_COMPONENT_VIOLATION`.

The resulting product disposition is a refusal: line 21 does not publish, so
Schedule 1 line 26 and Form 1040 line 10 block on the missing dependency. Stated
exactly: the current behavior **withholds an otherwise potentially supportable
result**. It does not compute a tax-law zero, and it does not cost the taxpayer a
deduction — the taxpayer's entitlement under § 221 is unaffected by the
application's inability to support a figure.

What P0 does not establish: whether either operation can be represented
honestly on the identities available today. The § 221(d)(1) determination —
whether through the chapeau and subparagraphs (A)–(C) or the concluding
sentence's related-person and employer-plan exclusion — applies to identified
indebtedness. Both § 221(e)(1) consequences must resolve an amount, and the
second sentence additionally fixes *where* in the worksheet order it applies:
prior to § 221(b), so before the $2,500 cap and the MAGI phaseout the incumbent
already computes. Neither statement fixes the shape of the ordinary evidence that would
support it — that is P1 and P2 work.

**F5 — `no-non-qualified-loan-component` compresses the whole § 221(d)(1)
definition into one answer.** The chapeau's sole-purpose requirement, (A) the
person on whose behalf the expenses were incurred and the timing of that
determination, (B) the reasonable-period-of-time requirement, and (C) the
eligible-student requirement are separate predicates with separate evidence. One
`{yes, no}` admits no way to state, correct, or retract any one of them
independently. The P1 candidate surface therefore lists them as four separate
constituents; the compressed phrase is not itself a candidate.

**F6 — Dependency presence is enforced on one branch; per-object correspondence
is not enforced at all.** The gap is narrower than "no coverage mechanism," and
it is branch-dependent. Everything below describes the **nonempty Form 1098-E
route** only. On the closed-empty branch the rule returns literal 0 from its
top-level `count == 0` test and the `conditional_dependency_set`'s own condition
is false, so rows 3–13 are never read and none of this enforcement runs (see F7
for what that branch then publishes). With that qualification, what the
committed rule enforces on the nonempty route, and where it stops, differs by
row:

- **Rows 9–12** (`no-form-2555`, `no-form-4563`,
  `no-puerto-rico-or-samoa-income`, `not-claimed-as-dependent`). The worksheet's
  `conditional_dependency_set` requires one current fact for each, at the
  filer/tax-year scope those facts declare. Presence is enforced and the scope
  is the right one, because each proposition is genuinely about this return.
- **Row 13** (`legally-obligated-for-interest`). Presence is enforced the same
  way, at the same declared filer scope. The enforcement is not the problem; the
  scope is, because mixed debt-level obligation is unrepresentable in a fact
  keyed by tax year alone.
- **Rows 3–7** (the per-statement witnesses). `collect_categorical_all_equal`
  requires at least one current value for the fact type — an empty row set
  raises `BLOCK_ABSENT` — but nothing requires one answer per statement, still
  less per loan. This is the correspondence failure F2 reproduces at C6.

So the open design problem is **per-object correspondence and cardinality where
the proposition requires it**, not an absence of dependency enforcement — and
even the presence enforcement that does exist is conditional on the nonempty
route.

Four distinct notions are in play and P0 keeps them apart:

1. **Closure attestation** — a horizon-keyed user claim that a family's
   membership is complete (row 8, for the box-1 amount family only).
2. **Structural companion enforcement** — an admission-time requirement that
   each member of one fact type carry a paired fact (row 2's box-2 companion).
3. **Ordinary dependency presence** — a rule requiring that some current value
   exist before it computes (`conditional_dependency_set` for rows 9–13;
   `collect_categorical_all_equal`'s non-empty requirement for rows 3–7).
4. **Per-object coverage** — a guarantee that a supporting answer exists for
   every object the proposition ranges over. Only notion 2 delivers this today,
   and only for box 2.

P0 selects no remedy. Which notion a candidate needs depends on the scope of the
proposition P1 selects, and a return-scoped proposition may need nothing beyond
notion 3.

**F7 — The closed-empty zero rests on an inference the closure does not
support.** An earlier draft of P0 concluded this route was already honest. That
conclusion is withdrawn. Stated separately:

- *Committed behavior.* `count == 0` returns literal 0 without reading filing
  status, any eligibility component, the line-1 subtotal, or the worksheet
  arithmetic. The presentation projector classifies that zero as
  `closure_backed_zero` (`_classify_numeric` in
  `packages/derivation/presentation_projection.py`), and it populates Schedule 1
  line 21, from which line 26 and Form 1040 line 10 compute an AGI. That
  classification is an implementation label for how the projector reached a
  numeric disposition — it is not evidence that the zero is a supported tax
  result, and P0 rejects the tax-support inference the name invites.
- *Evidence meaning.* The closure's members are box-1 amount findings. It
  attests that the **recorded box-1 amount family is complete** relative to the
  box-1 amounts on furnished Forms 1098-E, as of the keyed horizon; closed-empty
  therefore means that family has no current amount members under that
  completeness claim. It is not a document inventory: it does not independently
  establish which forms were furnished, or that none was. And it does not attest
  that the taxpayer paid no deductible student loan interest — the point that
  carries the rest of this finding. A lender is generally required to
  file Form 1098-E at $600 or more of interest for 2025; the threshold does not
  prohibit a form below that amount, and no form is guaranteed below it. Section
  221 has no corresponding deduction threshold, so interest below the reporting
  threshold may be deductible if the other § 221 requirements are met. It is not
  automatically deductible — it is simply not resolved by the absence of a form.
- *Product consequence.* A closed-empty family cannot produce a numeric Student
  Loan Interest Deduction on Schedule 1 line 21, and line 26 and AGI cannot
  compute from that unsupported zero. The required reader outcome is a truthful
  unavailable or blocked deduction, explained as the source evidence not
  establishing whether interest was paid. Whether the product *also* renders a
  separate source-status statement — about the empty amount family, or a
  stronger claim about which forms were furnished — is optional and presently
  unverified. The stronger claim would need its own source or evidence basis,
  since the closure does not supply one. P0 requires no source-status citizen,
  field, or publication surface, and does not decide that any such statement is
  warranted. One current constraint is on record —
  `presentation_projection.py` suppresses closure findings from citation sites
  (`_is_closure_finding` at the citation-site loop, and `closure_backed_zero`
  carrying an empty evidence set) — but that fact alone does not determine what
  the eventual explanation mechanism must be. P2 determines whether the current
  output and presentation contracts can expose such a status at all; Track 0 may
  decide whether it is needed.
- *Milestone boundary.* Two things are deferred differently. The
  **documentless-interest input route** — how a taxpayer states that interest
  was paid without a Form 1098-E — is not designed in P0 and need not be built
  by this milestone. The **disposition** is not deferred: if production
  proceeds, the closed-empty path must stop publishing a numeric deduction on
  the return path, whichever eligibility gate P1 selects. Track 0 closes that
  disposition before production begins.

This is a production condition, not a candidate-dependent one. P0 records the
defect and does not design the remedy.

**F8 — Box 2 establishes a bounded enforcement precedent, not an ordinary-fact
model.** Two things about box 2 are separate and both matter.

*Its semantics.* Box 2 is a reported amount-composition qualifier: it states
whether specified origination fees and capitalized interest are omitted from the
box-1 figure. It is a fact about how an amount was composed, not a completeness
claim about a family and not an eligibility condition.

*Its enforcement.* `domain_companion_presence_pairs` requires a same-statement
box-2 companion on every box-1 member, at kernel admission. That is a structural
per-object mechanism and it demonstrably works — it is the one place in this
route where an answer is guaranteed to exist for each statement.

The value of the precedent is the enforcement mechanism, not the fact's shape.
Because the domain is `{null, false}`, only an allowed state is ever admitted:
a checked box causes refusal, since the application cannot reconstruct the
omitted amount. P0 does not design that reconstruction. So the precedent says
nothing about recording an ordinary-language circumstance, and nothing about
representing an adverse answer durably.

**F9 — "MAGI" here is exact only inside a narrow class.** Worksheet line 2 is
`tax.us.2025.income.total-income`; line 3 is a literal 0 justified by the twelve
Schedule 1 Part II absence witnesses. The § 221(b)(2)(C) add-backs are not
computed. The instructions direct the filers who would need them to
Publication 970's worksheet; the application implements no such route, so an
adverse answer on any of the three worksheet-selection questions blocks the
standard worksheet. The phaseout is correct for the bounded class, and the
product refuses rather than computing for the rest.

#### P0.4 What P0 hands to P1

P0 ranks nothing and selects nothing. It hands P1 a neutral comparison surface:
six requirement dimensions, and where each current answer sits on them. P1
records each candidate's exact proposition, authority, scope, dependencies,
invalidators, and unsupported nearby inference, and selects exactly one.

| Dimension | What a candidate on it would require | Current answers on it |
| --- | --- | --- |
| **Loan qualification** | The tax determination applies to identified indebtedness — § 221(d)(1)'s chapeau and subparagraphs (A)–(C) state what qualifies, and its concluding sentence removes related-person and qualified-employer-plan debt from the class. The ordinary inputs that support it (relationship to the lender, whether the arrangement is an employer plan, what the borrowed money paid for, for whom, and when) need not share that identity, and may each have an independently useful one. | rows 3, 4, 5 |
| **Double-benefit denial** | § 221(e)(1)'s first sentence denies a deduction for any amount a § 127 exclusion already covers — the employer's payment of principal or interest on the loan, capped at § 127(a)(2)'s $5,250. A candidate here must resolve that amount, not merely flag that an employer paid something. | row 6 |
| **Amount reduction, with worksheet ordering** | § 221(e)(1)'s second sentence reduces the § 221(a) amount by the § 529(c)(9) earnings QHEE treatment kept out of income, not below zero, expressly prior to § 221(b). A candidate here must resolve an amount **and** land before the $2,500 cap and the MAGI phaseout. | row 7 |
| **Return-scoped eligibility** | An account of whether another return claims this filer. Genuinely filer-scoped: the answer is about this return and this taxpayer, with no per-statement or per-loan unit. | row 12 |
| **Obligation for the interest** | An account of who is obligated on the indebtedness the interest was paid on. The condition attaches to debt, so a filer-scoped answer is a compression whose loss is invisible when one statement aggregates loans with different obligors. The committed fact is filer-scoped today. | row 13 |
| **Worksheet selection** | An account of the filer's return composition and residence sufficient to decide whether the standard worksheet applies. Filer-scoped. Note that adverse answers currently block rather than select an alternate route. | rows 9, 10, 11 |
| **Identity** | A stable proposition identity supporting correction, retraction, and reassertion, at the scope the proposition actually needs. Available today at statement scope (rows 1–7) and filer scope (rows 9–13); **not** available at loan or debt scope for any answer, per F2's C7 result. A return-scoped candidate is already served; a debt-scoped one is not. | all |
| **Coverage enforcement** | Whether a supporting answer is guaranteed to exist for every object the selected proposition ranges over. Dependency *presence* is enforced for rows 3–13 on the nonempty Form 1098-E route (F6): rows 9–13 through `conditional_dependency_set` at filer scope, rows 3–7 through `collect_categorical_all_equal`'s non-empty requirement. The closed-empty branch reads none of them. What is missing is *per-object correspondence* where the proposition needs it — one answer per statement, or per debt. A return-scoped candidate may need nothing more than what exists; a statement- or debt-scoped candidate needs a mechanism this route does not yet have for it. Box 2 (row 2) is the only place per-object coverage is delivered today, structurally at kernel admission rather than by a rule. | presence: rows 3–13, **nonempty route only** (the closed-empty branch skips them); per-object correspondence: row 2 only |

Open requirements that apply to any selection: F1 means no candidate may be
credited for having an entry path; F3 means the reader-facing account of a
refusal must be able to name the circumstance; F4 means the selected
representation must match the statutory operation rather than flatten it; F6
means the coverage mechanism is chosen with the case, not assumed in advance.

For both § 221(e)(1) rows the ordinary evidence supporting the amount may be
categorical facts, amounts, payment events, source records, or a combination —
P1 compares candidates without assuming the user supplies the final tax
adjustment directly.

Assumptions P1 must not carry in from the current implementation: that legal
obligation is filer-wide; that a user supplies a numeric tax adjustment; that
coverage must be enforced by a closure-style attestation; that per-object
correspondence is required regardless of the selected proposition's scope; and
that a closed-empty Form 1098-E family establishes a zero deduction (F7).

P0 review fails if the map starts from storage fields, treats a label as the
underlying proposition, conflates a tax consequence with a product disposition,
or implies that the entire deduction must be remodeled to improve one seam.

### P1 — tax boundary and candidate forcing cases — **SELECTED 2026-09-13**

Read 26 U.S.C. § 221, 26 CFR § 1.221-1 (especially paragraphs (b)(1) and
(b)(4)), and the official 2025 reporting instructions for the standard
worksheet. Use Publication 970 for explanation and examples only.
For every candidate and every current gate — at its actual statement, debt, or
return scope — record the exact proposition, authority, scope, dependencies,
invalidators, and nearby inference it does not support.

Compare at least these constituents for the first production slice. The list is
decomposed deliberately: "interest associated with a loan or expense that is not
qualified" is **not** a candidate, because F5 established that the phrase
compresses several separate predicates.

Loan qualification, § 221(d)(1) chapeau and subparagraphs:

- the indebtedness was incurred solely to pay qualified higher education
  expenses;
- the person on whose behalf those expenses were incurred, determined as of the
  time the indebtedness was incurred;
- the reasonable-period-of-time requirement;
- eligible-student status.

Loan qualification, concluding sentence of § 221(d)(1):

- related-person indebtedness;
- qualified-employer-plan indebtedness.

Obligation for the interest (26 CFR § 1.221-1(b)(1), with (b)(4) on third-party
payment):

- legal obligation to pay the interest.

Double-benefit denial, § 221(e)(1) first sentence:

- employer educational-assistance amounts (§ 127 exclusion, principal or
  interest, $5,250 cap).

Amount reduction, § 221(e)(1) second sentence:

- QTP earnings used for the interest (§ 529(c)(9), reduction not below zero,
  applied prior to § 221(b)).

Return-scoped eligibility, § 221(c):

- dependent status.

P1 may group two constituents for comparison only if they share **all** of the
material semantics the product depends on — not merely their statutory operation
and their identity. Grouping requires equivalence of:

- the precise tax proposition;
- the ordinary facts and evidence that support it;
- its dependencies and invalidators;
- its correction and retraction behavior;
- the tax consequence it produces; and
- the reader-facing explanation it warrants.

Sharing a debt identity is not sufficient. The § 221(d)(1) chapeau and its
subparagraphs (A)–(C) all operate on the same indebtedness and still require
separate treatment, because they rest on different ordinary evidence and fail
in different ways. P1 must not reconstruct `no-non-qualified-loan-component`
merely because those predicates range over one loan, and may **not** reassemble
any set of constituents into the old compressed tax conclusion under a new
label.

If P1 selects one constituent previously hidden inside
`no-non-qualified-loan-component`, it must state how the remaining constituents
stay unresolved or fail closed: implementing one must not silently establish the
others.

Select exactly one by product value and discriminating power: the user can
state the underlying circumstance in ordinary terms; it materially changes a
named result; its identity and lifecycle can be bounded; and its tax
classification can be supported without pretending the rest of the deduction
is complete. Candidates that qualify or disqualify identified indebtedness (§ 221(d)(1)),
candidates whose consequence is a denial as to a doubly-benefited amount
(§ 221(e)(1) first sentence), and candidates whose consequence is a reduction of
the allowable amount before § 221(b) (§ 221(e)(1) second sentence) are three
different operations, none interchangeable with another or with a return-scoped
eligibility condition. Compare them on the consequence the rule
must reach, not on the shape of the evidence a user might supply for it.

P1 review fails if a publication is treated as controlling law, a Form 1098-E
label is treated as the definition of qualified interest, the selected case
requires the user to supply the tax conclusion under a friendlier label, or the
two § 221(e)(1) sentences are treated as one operation.

#### P1 selection — eligible-student status, § 221(d)(1)(C)

**Selected 2026-09-13.** One constituent: whether the education the indebtedness
paid for was furnished during a period in which the recipient was an eligible
student, § 221(d)(1)(C) through § 25A(b)(3) — a degree, certificate, or other
recognized credential candidate carrying at least half the normal full-time
workload, at an eligible educational institution.

##### The production promise

This is the narrow claim the milestone undertakes, and it is narrower than
"disqualify a statement":

> For an identified loan, an identified academic period, and an amount of
> interest attributable to that loan, the application can derive whether the
> eligible-student condition is supported, from enrollment and institutional
> evidence. Unknown or mixed loan composition remains unresolved.

Everything below bounds that promise.

##### Identity and allocation cost, acknowledged before selection

Eligible-student status attaches to a particular loan **and** a particular
academic period. Composition can be mixed at two levels:

1. one Form 1098-E may combine interest from several loans, which may have
   financed different terms with different enrollment status; and
2. one loan may itself have paid for more than one academic period, and can
   satisfy (C) for one period and fail it for another.

So "a disqualified statement's interest leaves worksheet line 1" is **too
broad** and is withdrawn. The rule may remove only interest attributable to a
disqualified loan. Per *Fixed cases* C7, the milestone must deliver exactly one
of:

- a case where the statement is supportably associated with one loan and one
  academic period;
- an honest per-loan allocation of the statement's interest; or
- a refusal when the statement's composition is unknown.

A statement-level answer may not pretend the loans — or the periods — are
uniform. Which of the three the milestone delivers is a Track 0 decision, not a
P1 one.

Note also that enrollment during 2025 is irrelevant except where 2025 is the
period the loan financed. The tax year and the academic period are different
objects.

##### Institutional and public-authority dependencies

The application must support, and cannot push onto the user:

- the **program** requirement — candidacy for a degree, certificate, or other
  recognized credential;
- the **institution** requirement, as (C) actually embeds it — § 25A(b)(3)(A)
  incorporates HEA § 484(a)(1) (20 U.S.C. § 1091(a)(1)), which requires
  enrollment at an institution eligible under HEA § 1094. This is **not** the
  chapeau's own § 25A(f)(2) test; see *What this selection does not establish*;
  and
- the **institution-defined half-time threshold** for the relevant academic
  period, which is the institution's own standard, not a fixed number.

These are legitimate unresolved inputs. Where they cannot be established the
route stays unresolved and never favorable — that is healthy bounded coverage,
not a weakness of the case. The statute expressly attaches the determination to
an academic period and incorporates the half-time and program requirements.

This is also why the case is instructive beyond its own facts: it is the first
selected circumstance whose supporting facts come from an **institution or
public authority** rather than from the user's own assertion. The product has so
far treated every non-document fact as a user assertion; this case does not fit
that shape.

##### What the user supplies, and what the rule owns

The user reports their school, program, the academic period the borrowed money
paid for, and their course load. The application determines the tax
significance: whether that constitutes eligible-student status for that period,
and therefore whether the indebtedness is a qualified education loan.

The user is never asked whether they were an "eligible student."

##### Effect on the result

Where the condition fails for an identified loan, interest attributable to that
loan is not interest on a qualified education loan and does not enter worksheet
line 1; Schedule 1 line 21, line 26, and AGI follow from the reduced figure with
a stated reason.

The incumbent behavior this improves on is precise: an adverse answer on the
compressed witness today blocks the Student Loan Interest Deduction and the
calculations that depend on it — line 21, line 26, and AGI — not the entire
return. Other return positions are unaffected.

##### What this selection does not establish

Implementing (C) also establishes nothing about the chapeau's *separate*
institution test. § 221(d)(2) defines qualified higher education expenses by
reference to an eligible educational institution under § 25A(f)(2), which reaches
HEA § 481 (20 U.S.C. § 1088). The eligible-student test reaches institutional
eligibility by a different route — § 25A(b)(3)(A) → HEA § 484(a)(1) → HEA
§ 1094. The two tests will usually agree for a school actually participating in
federal aid, but they are distinct cross-references and satisfying one does not
dispose of the other. The P1 loan-qualification record says so directly at
`student-loan-interest-deduction-translation-evidence/p1-loan-qualification.md` constituent 4, "unsupported nearby
inference."

Implementing (C) establishes nothing about the chapeau's sole-purpose test,
subparagraph (A)'s person-and-timing test, subparagraph (B)'s reasonable period,
the concluding sentence's related-person and employer-plan exclusions, legal
obligation, either § 221(e)(1) operation, or § 221(c) dependent status. Each
remains unresolved or fails closed on its own terms.

##### Runner-up, and why it lost

Reasonable period, § 221(d)(1)(B). It does **not** escape the loan-and-period
identity problem — it too attaches to a particular loan and academic period. Its
only real advantage is that its additional evidence is simpler: dates rather
than institutional status. That is a smaller lesson, and the institutional
dependency is the more valuable thing to learn on a bounded case.

### P2 — committed artifact and consumer map — **REVIEWED 2026-09-13**

Trace the selected candidate through the current package and production path.
For every load-bearing artifact claim, record the artifact, fields read,
relevant sibling fields not relied upon, and all downstream consumers.

At minimum, verify:

- Form 1098-E contribution and closure behavior;
- the five per-statement witness identities, their multi-statement fold, and
  whether any answer is guaranteed to exist per statement (P0 F6);
- worksheet eligibility, arithmetic, pins, and blocked/inapplicable outcomes;
- Schedule 1 line 21 and line 26 composition;
- AGI and any feedback or same-run ordering risk;
- durable run and presentation visibility; and
- whether a production entry or mapping path exists for the current answer.

P2 also determines whether the current output and presentation contracts can
expose source status at all, and on what surface — distinguishing a statement
about the recorded box-1 amount family, which the closure does support, from a
statement about which forms were furnished, which would need its own source or
evidence basis. One constraint is already on record:
`presentation_projection.py` suppresses closure findings from citation sites.
P2 establishes what follows from that; P0 does not.

P2 must distinguish “the rule can consume a prepared fact” from “the product
can obtain and preserve the fact honestly.” Where the selected proposition is
statement- or debt-scoped, it must also test whether a single Form 1098-E can
cover several loans whose selected circumstances differ; where the proposition
is return-scoped, it must instead show that no per-statement or debt identity is
fabricated to serve it. P2 also records what the closed-empty path currently
publishes and what the closure actually establishes (P0 F7).

#### P2 findings — **REVIEWED 2026-09-13**

Independently reviewed and returned READY with no findings requiring rework. The
reviewer verified G1 and G3 from the executing code and content rather than from
the evidence files, reconstructed the C6 two-statement coverage scenario from
scratch through `live_coordinate_run`, and ran
`AttachmentTriggerCases.test_over_cap_filer_itemization_no_longer_false_blocks`.
All seven reported stale-text items were confirmed real. One additional detail
the review established, load-bearing for P3's shape choice:
`audit_collect_authority`'s `_collect_source_sets`
(`packages/derivation/source_authority.py`) matches only `op == "collect"` and
never `count` or `require_closed`, which is why the worksheet itself passes the
collect-authority audit today.

Traced by two concurrent units against the executing code, not against titles or
notes. Full records in
`student-loan-interest-deduction-translation-evidence/p2-source-and-entry.md` and
`student-loan-interest-deduction-translation-evidence/p2-computation-and-consumers.md`.

**G1 — None of the production promise's three preconditions is representable
today.** Every Form 1098-E fact type except the closure is keyed
`lender` + `statement` + `tax-year`. There is no loan identity distinct from
lender and statement; no academic period, school, term, program, enrollment, or
workload anywhere in `packages/content/tax/2025/`; and no per-loan amount — box 1
is one number per statement and the family collect can only sum statement
totals. The nearest shapes exist in other domains: `tax.us.interest-obligation`
and `tax.us.acquisition-report-pairing` (ADR-0068, bonds) for a debt-like object
below a payer, and `tax.us.nominee-allocation.amount` for splitting a statement
amount — by recipient, on a Form 1099-INT, not by loan on a 1098-E.

**G2 — Only one of C7's three resolutions needs no new identity.** Refusal on
unknown composition can use existing block machinery, though no committed block
code names composition and the current fold treats unknown composition as
covered. A single-loan single-period association needs a period representation
and an association claim. Honest per-loan allocation needs both plus per-loan
amounts and their lifecycle.

**G3 — The family's authorized subtotal must stay the raw sum.** The Schedule 1
attachment itemizes every current box-1 member and requires
`row_sum == symbols[subtotal_symbol]` exactly, with `subtotal_symbol` and
`tie_out.line_symbol` both being
`tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`. Publishing a
qualified, smaller figure under that symbol raises
`ITEMIZATION_TIE_OUT_VIOLATION` — the Track 4b failure, recurring. That failure
hard-fails the attachment only; line 21, line 26, and AGI are not that check.
Changing only which symbol the worksheet consumes as line 1 does not break the
tie-out. Six shapes are available; two avoid the collision entirely (qualify in
the consumer and leave the family subtotal raw; or refuse mixed composition so
no qualified subset is published), and three introduce a different symbol for
the qualified or subtractive amount.

**Limit on what Track 4b establishes.** Track 4b's cap is applied to an
aggregate, as a single scalar over the whole subtotal. It shows that a consumer
can compute a smaller figure while the family's authorized symbol stays raw. It
does **not** show that a consumer can qualify *particular* statements, because
the collection environment the fold reads carries values without statement
identity (G1). Report-specific qualification is an open P3 design question, not
a proved pattern.

**G4 — Block propagation is already honest.** A line-21 block reaches line 26
through a bare `ref` that raises `DEPENDENCY_ABSENT` rather than substituting a
zero, and line 10 and AGI follow. No silent zero anywhere on that path.

**G5 — The reader cannot currently see which circumstance caused a refusal.**
Confirmed at two layers. The projector copies the rule's code into
`resolved.activeCodes` but never compares it to the form field's declared
`dispositions.blocked.codes`, which omits all three `SLI_*` codes the rule
emits. The citation-walk renderer then drops the code from what a reader sees.
C10 therefore needs work regardless of which constituent is built.

**G6 — Closed-empty, as committed.** Line 21 is a `closure_backed_zero` with a
value of 0 and zero citation sites; line 10 renders that as `computed_zero` with
the twelve Part II absences cited, so the closure-backed classification does not
carry forward. The family's `closure_claim` still says "closed-empty authorizes
subtotal 0," which is true of the subtotal symbol and is not authority for line
21. P0 F7's production condition stands.

**Stale text found, not reopened.** The worksheet's notes claim ten universal
components where the executing `all` has eight, and a 22-member
`conditional_dependency_set` where the executing array has 17 (Track 6b removed
five). The engine-breadth plan cites `runner.py:964-975` for the tie-out; it
executes at 1592-1611 and 1694-1713. A Track 8 test class is named
`ClosedEmptyComputedZero` while its body and golden assert
`closure_backed_zero`. VOID exclusion is prose and omission rather than an
executing kernel filter, and no test constructs a VOID finding.

#### Scope decision — continue on a bounded path — **ACCEPTED 2026-09-13**

G1 shows the selected constituent's promise names three objects and none is
representable today. That engages the stop condition about requiring a
materially broader loan, education, or payment identity model. The owner
accepted the foreman's recommendation to continue rather than close partial, on
the following reasoning and bound.

**All three preconditions still require semantic support. What the bounded
approach avoids is narrower than "representing fewer objects."** It avoids
exactly two things: a separately reified loan entity, and per-loan allocation of
a statement's box-1 amount. Each precondition is still discharged:

- *the loan* is identified **relationally**, as the sole loan represented by
  that statement — not reified as its own entity, and not equated with the
  statement;
- *the academic period* is **explicitly represented**, as new vocabulary. This
  is the one precondition that gains a first-class representation, and it is the
  part of the case the owner identified as instructive;
- *the interest attributable to that loan* is discharged by treating the **whole
  statement amount** as attributable to the sole loan the statement represents —
  which is a consequence of the association claim, not an allocation.

So the claim being asserted is that this statement's aggregation is trivial:
*this statement's box 1 is entirely interest on a single loan that financed this
academic period.* That is assertable at the existing `lender` + `statement` +
`tax-year` identity. Where the taxpayer cannot say it, composition is unknown
and the route refuses, which is C7's third resolution and needs no new identity
(G2).

So the bounded path is:

1. new vocabulary for the education facts the condition actually needs — school,
   program, academic period, workload — which is the part of this case the owner
   identified as instructive, because these facts come from an institution or
   public authority rather than from the user's own assertion;
2. a statement-scoped association claim. Its premise, stated exactly: the
   association identifies the relevant loan **relationally**, as the sole loan
   represented by that statement. The statement is not the loan and must not be
   described as one. The claim is assertable and correctable at the existing
   `lender` + `statement` + `tax-year` identity;
3. refusal when composition is unknown or mixed, with a reader-facing reason
   that names composition rather than reusing
   `SLI_UNIVERSAL_COMPONENT_VIOLATION`; and
4. qualification applied in the consumer, leaving `f1098e.1`'s authorized
   subtotal as the raw sum.

**What this deliberately does not build:** a loan entity distinct from lender
and statement, per-loan amounts, an allocation of box 1 across loans, or any
change to the family's authorized subtotal symbol. The general case — a
statement that genuinely aggregates loans with different enrollment histories —
is refused, not modeled.

**What this path does not yet have.** Three obligations are open and belong to
P3. They are recorded here so the bounded direction is not mistaken for a
settled design.

- *Per-statement qualification is not proved by Track 4b.* Track 4b proves that
  an **aggregate-wide** cap can be applied while the raw family subtotal is
  preserved. It does not prove **report-specific** qualification. G1 and the P2 source-and-entry record
  show the ordinary collection environment drops statement identity —
  `env.sources` is values only — so the fold cannot pair each box-1 amount with
  that statement's own education support. P3 must demonstrate a **declared**
  path that handles two statements with different circumstances, without a
  values-only fold, without Python tax special-casing, and without one
  statement's support covering another. Until then, shape 1 is a candidate, not
  a proved mechanism.
- *The reader-facing attachment surface is not solved by passing the tie-out.*
  The committed below-floor golden already renders the heading "Line 21: Student
  Loan Interest Deduction" with `tieOutText` "Reported subtotal: 3000" while
  line 21 publishes 2500. If qualification excludes a disqualified statement's
  amount, that same surface would still list the excluded amount under the
  deduction heading. Passing the runner tie-out is mechanical feasibility only.
  P3 must either distinguish raw reported interest from the supported deduction
  on the attachment and explanation surface, or establish another honest
  presentation shape.
- *The statement-scoped association must earn its scope.* P3 must prove that a
  statement-scoped association can carry the academic period and the
  institutional evidence, stay correct through correction and retraction, and
  refuse any unknown, multi-loan, or multi-period composition. The P2 source-and-entry record's finding
  stands: a single-loan single-period association in the **general** case needs a
  distinct loan entity. The bounded path avoids that entity only by relational
  identification plus refusal, and P3 must show the avoidance holds.

Neither the per-statement computation mechanism nor the attachment mechanism is
selected here.

**Handoff correction reviewed 2026-09-14 by the owner; further independent
review waived.** The correction was made in two owner-directed rounds. The first
withdrew the Track 4b overclaim, added the reader-facing attachment problem as a
P3 condition, reconciled the C7 contradiction, and fixed an overbroad
entity-kind sentence in the P2 source-and-entry record. The second withdrew the claim that fewer than
three preconditions need semantic support, corrected the P2 computation-and-consumers record's shape 1 locally,
and rewrote the phase-state capsule to carry only the current account. No
sub-agent review of the correction was run; the record is owner review, not an
agent verdict.

**Contingency discharged 2026-09-13.** This decision rested on G1 and G3. The
independent P2 review confirmed both from the executing code — no loan identity,
no academic period or enrollment vocabulary, no per-loan amount; and the
attachment tie-out's exact `Decimal` equality against the family's authorized
subtotal symbol, with shapes 1 and 6 writing nothing new into it. The decision
stands and P3 proceeds on this path.

**Deferred, and named for a successor milestone.** A student-loan identity
carrying per-loan amounts, and the per-loan allocation of an aggregating
statement's box 1, are the smallest prerequisites for the general case. They are
not in this milestone's scope and this milestone's partial coverage must say so
on the refusal path.

### P3 — executable design and reviewable case table — **REVIEWED 2026-09-14; decision-ready partial result**

Turn the P1 selection into the smallest complete vertical. **Outcome 2026-09-14: P3 is a decision-ready partial design, not a complete vertical** — see *P3 outcome*. Write two positive
cases, two meaningful negatives, one correction/retraction/reassertion trace,
and a producer → authority → consumer → failure map before proposing a schema
or implementation.

If two materially different representations remain plausible and a named
consumer behaves differently, run one bounded rival comparison at the cheapest
evidence rung capable of deciding it. If no consumer differs, defer that
representation choice and use the simpler bounded shape. Do not run rivals for
the worksheet arithmetic already established by committed tests.

**P3 status 2026-09-14: drafted, and the 2a/2b discharges are withdrawn.** A
first P3 design (`student-loan-interest-deduction-translation-evidence/p3-partial-design.md`) reported all three obligations discharged. Owner
review found the proposed path not executable against current machinery, and the
foreman verified each point in the code:

- the evaluator's `parameter` operator returns `_as_decimal` on both its keyed
  and unkeyed branches, so it cannot return the categorical catalog values the
  design proposed; and no operator in the grammar constructs a composite
  institution + program + period lookup key (the committed `key` usage is a
  single `ref`);
- `evaluate_pairing_scoped_rule` resolves exactly `left_fact_id` and
  `right_fact_id` from the pairing payload — two facts — not the statement
  amount, association, period, enrollment, and catalog determinations the design
  needs;
- pairing dispatch is selected by Python rule-id registration
  (`is_pairing_scoped_consequence_rule`), **not** refused at package admission.
  The mechanical admission refusal covers unauthorized `bound_sources`
  (`MEMBER_NO_BINDING_PATH`) and v9 `aggregation`
  (`NOMINEE_AGGREGATE_ID_INVALID`) only. The design's claim otherwise is
  withdrawn;
- a form field carries one static `explain` string per disposition, so the
  surface cannot dynamically say which statement failed on which predicate.

Obligation 2c stands. 2a and 2b return to open, and P3 is not complete until a
bounded executable feasibility probe demonstrates the path through the real
evaluator and the presentation projection.

P3 must additionally discharge the three obligations recorded under *Scope
decision*:

1. **A declared per-statement path.** Demonstrate handling of two statements
   with different circumstances without a values-only fold, without Python tax
   special-casing, and without one statement's support covering another. The
   collection environment drops statement identity, so this cannot be assumed
   from Track 4b's aggregate cap.
2. **An honest attachment and explanation surface.** The committed below-floor
   golden renders "Reported subtotal: 3000" under the heading "Line 21: Student
   Loan Interest Deduction" while line 21 is 2500. Either distinguish raw
   reported interest from the supported deduction on that surface, or establish
   another honest shape. Passing the runner tie-out is not sufficient.
3. **A statement-scoped association that earns its scope.** Show it can carry
   the academic period and institutional evidence, survive correction and
   retraction, and refuse unknown, multi-loan, or multi-period composition —
   identifying the loan relationally as the sole loan that statement represents,
   never by treating the statement as the loan.

P3 review fails if the proposed fact merely renames the old tax-labelled
witness, if a post-hoc process record is treated as a derivation input, if the
selected consequence reaches the result only through Python special-casing, or
if the case table cannot distinguish missing support from a supported negative.

#### P3 outcome — **REVIEWED 2026-09-14; OWNER DECISION TAKEN**

Independently reviewed and returned READY with no findings. The reviewer ran the
probe, then verified the deciding claim from `pairing_dispatch.py`'s own control
flow rather than from the probe's assertion: iteration is
`for pairing in pairing_sources`, so an unpaired left fact id is never visited
and can produce neither a publication nor a blocked row. It confirmed every
load-bearing claim is either traced to executed code or labeled at its true
evidentiary level — conceptual completeness, partial mechanics witness,
unproven pin isolation, projection over synthetic rows — and recorded that the
two-round overstatement failure mode is not present in the repair.

**Owner decision 2026-09-14: close this milestone explicitly partial.** The
eligible-student direction and its cases are preserved as the forcing consumer
for a prerequisite engine milestone. No further one-off exact-rule coordinator
is authorized. The authoritative institutional-catalog problem stays a separate
required decision. The narrowed presentation is accepted as a description of
current limitations, not as the final product promise.


Obligation 2c stands. **2a and 2b are not discharged.** The selected
eligible-student product direction is unchanged and is not reopened.

The bounded executable feasibility probe
(`docs/prototypes/sli-eligible-student/`) ran through the real evaluator and the
real pairing dispatcher, with presentation checked by **projection over
synthetic publications and disposition rows** — `build_presentation_model` in
memory. It does **not** call `live_coordinate_run`, write a durable presentation
file, or execute `citation-walk.v1.html`. The attachment-inapplicable
observation is projected from a manually supplied inapplicable row; the
committed attachment requirement behavior was established separately in P2. The
probe runs clean and its assertions hold; the foreman executed it
independently. What it establishes:

**The coverage defect is real and decides the mechanism.** Dispatch driven by
current *association* findings cannot see a current box-1 statement that has no
association. With statements A and B and an association for A only, the
association-driven path publishes A's `2000` and silently omits B. This was
exercised against the **real** `evaluate_pairing_scoped_rule`: with two current
box-1 sources and one pairing it returned one publication of `2000`, pinned A's
findings, left B absent from the pins, and produced no blocked row. Completeness
would require iteration driven by the **current box-1 family**, with the check
that every current box-1 fact id has exactly one usable association — **that
result is conceptual**: the probe computes it by hand and no committed
coordinator performs it. That is P0 F2's
coverage failure reappearing in the proposed mechanism, and `pairing_dispatch`
cannot express it: it iterates the pairings it is given.

**Three capability gaps, in order of decisiveness.**

1. **Box-1-driven heterogeneous group-binding.** `evaluate_pairing_scoped_rule`
   binds exactly `left_fact_id` and `right_fact_id`. This vertical needs the
   statement amount, association, academic period, enrollment, and catalog
   determinations, and needs the driver to be the box-1 family so unassociated
   statements are caught. No committed primitive does this.
2. **An authoritative catalog-input contract.** A `fact-type.v2` citizen
   declares vocabulary; it does not supply a current institution-eligibility or
   program-classification finding. The probe injected synthetic categoricals to
   test evaluation mechanics only. Production has neither a producer or evidence
   path for those determinations nor an adopted categorical catalog grammar —
   and the `parameter` operator returns `_as_decimal`, so it cannot carry them.
   Only the half-time threshold is presently representable as a numeric
   parameter, keyed by an opaque standard id.
3. **An explanation carrier.** Deferred, not dismissed. A narrowed promise is
   acceptable as a description of current limitations, but the resumed milestone
   must eventually identify which statement was excluded and the supported
   reason. Carrier design waits until the computation and catalog inputs exist;
   it is retained as a **production condition**.

**Two further evidence limits, recorded.** The probe's `VALUE_EXPR` reads
institution eligibility and the keyed half-time threshold but never program
classification, so it is a **partial mechanics witness**, not the declared
eligible-student (C) tree. And pin isolation is **not proven**: the probe
authors aggregate and result pins by hand, and `AccessLog` symbol names do not
establish finding-level pin selection.

**What a reader can and cannot see, measured on the projection over synthetic rows.** Can:
`published_value` versus `computed_zero` versus `blocked` versus an
`guard_inapplicable` attachment; the citation sites actually projected;
`DEPENDENCY_ABSENT` when allowlisted. Cannot: which statement failed; which
(C) predicate failed; that B was a supported negative on a mixed return; B's
reported amount when line 21 is 0 and the attachment is therefore absent;
unknown composition as a named code after the renderer's allowlist filter.

**No bespoke exact-rule ADR is proposed.** The earlier recommendation of one
additive ADR with no new operator is withdrawn: it would bless a prototype
coordinator the committed machinery does not support.

**If a general contract is later wanted**, the abstraction is not "evaluate once
per thing." It is an identified evaluation context that declares the subject
driving iteration, all required related facts, cardinality and completeness,
local bindings, failure behavior, and pin isolation. P3 does **not** design it;
the probe only shows the bounded path cannot be described without something of
that kind.

## Fixed cases

The exact selected circumstance is filled in after P1. These case classes are
fixed now so selection cannot avoid the difficult behavior.

**Every case respects the selected proposition's actual scope.** C6 and C7 test
whether the implementation is honest about the scope it claims — not whether it
manufactures a per-statement or per-debt answer. A genuinely return-scoped
condition such as dependent status passes them by governing the return once,
correctly, without inventing per-statement copies or debt identity. A statement-
or debt-scoped condition passes them by representing mixed circumstances
honestly or refusing the mixed class outright. Neither shape is disqualified for
failing a test that does not apply to it; a candidate fails only by claiming a
scope it cannot support.

| Case | State | Required observation |
| --- | --- | --- |
| C0a — closed-empty source family, no other interest evidence | The box-1 amount family is attested complete with no current members; nothing else in the workspace evidences student loan interest | The Student Loan Interest Deduction is unavailable or blocked, and the reader-facing explanation says the source evidence does not establish whether interest was paid. Schedule 1 line 21 carries no numeric deduction, and neither line 26 nor Form 1040 AGI computes from one. The selected circumstance is not demanded and no negative ordinary fact is invented. A separately rendered source-status statement is optional, not required by this case. |
| C0b — closed-empty source family, ordinary interest evidence | The box-1 amount family is attested complete with no current members; ordinary evidence that student loan interest was nevertheless paid — including interest below the amount at which a lender is generally required to file | Same disposition as C0a, and the explanation does not contradict the ordinary evidence. The closure is not read as establishing zero. This milestone need not implement the documentless-interest input route; if it does not, the deduction and the dependent return results remain unavailable and the limitation is stated (P0 F7). |
| C1 — supported ordinary case | One synthetic Form 1098-E and ordinary facts establishing the selected condition does not apply | The rule, not the user, establishes the favorable tax consequence; the bounded worksheet reaches the expected Schedule 1 result. |
| C2 — consequence changes | Same report with ordinary facts establishing that the selected condition applies | The selected tax consequence reaches the named amount exactly as P1 requires, and the resulting product disposition is distinguishable from a refusal; no unrelated gate supplies the outcome. |
| C3 — missing ordinary support | Report present; selected ordinary fact absent | The route fails closed or remains unresolved. Absence is not read as a favorable answer. |
| C4 — correction | C2 ordinary fact corrected at the same proposition identity | A later run uses only the corrected current support and preserves the prior assertion as history. |
| C5 — retraction and reassertion | Retract the current ordinary assertion, run, then assert again | The retracted answer no longer supports the deduction; reassertion restores support without reviving the old finding. |
| C6 — several statements | Two Form 1098-E statements. If the selected condition is statement- or debt-scoped, their selected circumstances differ | **Statement- or debt-scoped selection:** one statement's favorable answer cannot hide the other's adverse or unresolved state, and ordering does not change the result. **Return-scoped selection:** the one return-scoped fact governs both statements without per-statement copies being invented, and the result is identical however the statements are ordered or divided. |
| C7 — one statement, several loans | One statement aggregates more than one loan | **Statement- or debt-scoped selection:** where the selected circumstance differs by loan — including a filer obligated on some loans and not others — the plan either carries honest identity for the indebtedness or explicitly refuses the class. Neither a statement-level nor a filer-level answer may pretend the loans are uniform; the current filer-scoped legal-obligation answer is one such compression (P0 F2, F6). **Return-scoped selection:** the case instead proves the condition legitimately governs regardless of how many loans a statement aggregates, and that no debt identity was fabricated to satisfy it. |
| C8 — MAGI phaseout | C1 and C2 repeated below and inside the phaseout range | The selected qualification and the existing MAGI limitation compose once, with distinguishable provenance. |
| C9 — bounded exception | A Form 2555/4563/territorial-income or other excluded worksheet class | The milestone refuses or remains outside scope; it does not silently apply the standard worksheet. |
| C10 — reader account | Successful, computed-zero, blocked, unavailable, and inapplicable paths used above | Durable output identifies the report, ordinary support, adopted tax rule, worksheet inputs, and result without attributing the tax conclusion to the user. |

## Scope

### Included

- A fluid, plain-language domain map for the bounded Student Loan Interest
  Deduction translation.
- A verified current-artifact and consumer map for the 2025 standard worksheet.
- Selection of one constituent condition as the forcing production slice, from
  the decomposed P1 candidate surface.
- The minimum ordinary facts, mapping, rule-owned consequence, package wiring,
  lifecycle, provenance, and presentation needed for C0a-C10.
- Preservation of the current cap, phaseout, Schedule 1, AGI, and other existing
  bounded behavior unless the selected case proves a correction necessary.

### Excluded

- Complete support for every qualified education loan or every route in
  Publication 970.
- A general person/household/loan/education/payment ontology not required by the
  selected case.
- Form 1040-NR and alternate worksheets for Form 2555, Form 4563, or territorial
  income.
- Production UI, filing, document ingestion, OCR, or lender data exchange.
- Reworking unrelated Schedule 1 adjustments or treating current absence facts
  as canonical ordinary facts by default.

## Contracts

The milestone starts with no selected new schema or ADR. P0-P3 must determine
whether the selected vertical fits accepted fact, evidence, assertion,
retraction, rule, package, run, and presentation contracts or needs one bounded
successor.

Accepted contracts that remain load-bearing include source-family claim
boundaries (ADR-0016), declared-absence semantics where genuinely applicable
(ADR-0038), arithmetic and categorical collection (ADR-0064), Schedule 1 Part
II composition (ADR-0065), and current assertion/retraction standing. The fact
that the current worksheet consumes a witness does not ratify that witness as
the selected ordinary-fact model.

If a new payload-bearing schema is required, the payload instantiation gate is
discharged before code depends on it. Published schemas are never edited.

## Fixtures

- Only obviously synthetic `demo.*` and `demo-*` people, lenders, loans,
  statements, evidence, and amounts.
- One committed case per materially different C0a-C10 path that survives P1
  selection.
- Compatibility cases for the incumbent standard worksheet below, within, and
  above the MAGI phaseout.
- Where the selected proposition is statement- or debt-scoped: multi-statement
  and, where representable, multi-loan cases that prevent a single categorical
  answer from hiding a mixed population — including a mixed obligation
  population if the selected case reaches legal obligation. Where it is
  return-scoped: cases proving one fact governs several statements without
  per-statement copies or fabricated debt identity.
- Closed-empty amount-family cases (C0a, C0b) whose durable output carries an
  unavailable or blocked Student Loan Interest Deduction with a truthful
  explanation — never a numeric zero on Schedule 1 line 21 — and dependent
  line 26 and AGI results consistent with that unavailability. No fixture
  asserts that no Form 1098-E was furnished. Whether the output renders any
  separate source-status statement is not fixed here.
- Durable output/presentation fixtures for successful, computed-zero, blocked,
  unavailable, and inapplicable results.

## Verification

Planning reviews measure each gate against its stated failure conditions before
the next gate is treated as settled. Track 0 receives the final P0-P3 case table
and evidence; it does not reconstruct them from broad prose.

Production verification must enter through the real contribution and
`live_coordinate_run` path and inspect durable output and presentation. It must
prove:

- the ordinary fact can be contributed, corrected, retracted, asserted again,
  and recovered with truthful attribution;
- the adopted tax rule owns the selected tax classification and arithmetic;
- C0a-C10 outcomes and multi-member order independence, each measured at the
  selected proposition's own scope;
- that a closed-empty box-1 amount family produces an unavailable or blocked
  deduction, explained as the source evidence not establishing whether interest
  was paid, with no numeric zero on Schedule 1 line 21 and no downstream line 26
  or AGI figure computed from one, and with no claim that no Form 1098-E was
  furnished;
- the worksheet cap and MAGI phaseout remain correct and execute once;
- Schedule 1 line 21/26 and Form 1040 AGI remain coherent;
- reader-visible provenance distinguishes reported amount, ordinary support,
  rule-owned conclusion, and derived result; and
- predecessor package behavior and unrelated current routes remain compatible —
  except the closed-empty deduction disposition, whose current behavior is a
  defect (F7) and is corrected rather than preserved.

Use focused tests while iterating. Any implementation change under
`packages/kernel/` or `packages/derivation/` requires the full suite before
handoff; CI remains the gate of record. Run repository mypy for typed Python,
governance lint, envelope scan, and `git diff --check` as applicable.

## Data safety

No personal source document, borrower fact, education history, dependent
status, employer benefit, workspace path, generated return, credential, or
private output may enter the repository or a review. All committed examples are
synthetic and use `demo.*` / `demo-*` identifiers.

## Tracks

P0-P3 are reviewed planning gates, not implementation tracks. The Foreman
updates this plan after each gate so later work receives the current model, not
a pile of superseded reviews.

### Track 0 — adversarial contract closure — **NOT STARTED**

Close the selected proposition, authority, identity, lifecycle, empty/nonempty,
multi-statement, multi-loan (each at the selected proposition's own scope),
consumer, and explanation boundaries. Decide
whether the existing contracts carry the vertical or one bounded successor is
needed. No production implementation begins while any required adversarial
artifact is unresolved.

### Contract unit — **NOT STARTED**

Only if Track 0 identifies a contract gap: publish the smallest additive ADR or
schema successor, with a concrete positive payload and independent review,
before production code consumes it.

### Track 1 — ordinary-fact recording and mapping — **NOT STARTED**

Record the selected ordinary circumstance through the real contribution path,
including stable proposition identity, correction, retraction, reassertion,
attribution, and recovery. Do not compute the tax result in the entry mapper.

### Track 2 — rule-owned consequence and worksheet integration — **NOT STARTED**

Derive the selected tax consequence from current ordinary support and connect
it through the existing standard worksheet, Schedule 1 line 21/26, AGI, durable
run output, and presentation. Preserve the current arithmetic and scope
refusals unless P1-P3 specifically displace them.

This track also carries the closed-empty disposition correction settled by
Track 0 (P0 F7), independent of which gate P1 selected: the closed-empty path
yields a truthful unavailable or blocked deduction and no longer places a
numeric zero on Schedule 1 line 21 or computes line 26 and AGI from one. Whether
a separate source-status statement is rendered follows Track 0's decision, on
what P2 found the current contracts can actually expose. The
documentless-interest input route is out of scope unless P1 selected it.

### Closing unit — **NOT STARTED** (closeout performed by the foreman at the explicit-partial close)

Curate the plan, accepted contracts, production tracks, durable domain model,
phase state, roadmap, and retrospective into the reproducible final result.
Remove working gate reviews and repair narration after distilling material
decisions and evidence.

## Track 0 adversarial closure

- Authority-lifecycle table: **PENDING**
- Empty/nonempty authority matrix: **PENDING**
- Closed-empty disposition (no numeric deduction on the return path; the
  truthful unavailable/blocked outcome and its explanation; and whether a
  separate source-status rendering is needed at all) — **PENDING**, required
  before production
- Late-member lifecycle: **PENDING**
- Neighboring capability dependency diff: **PENDING**
- Reused-claim semantic/lifecycle equivalence: **PENDING**
- Integration surface: **PENDING**
- Known limitations affecting correctness: **PENDING**

## Execution record — CLOSED EXPLICITLY PARTIAL 2026-09-14

A completed bounded investigation with no production path.

| Gate / track | Result |
| --- | --- |
| P0 product outline and claim inventory | Settled. Product map plus all thirteen Form 1098-E and SLI-scope answers classified. Owner waived further independent review. |
| P1 tax boundary and selection | Complete and independently reviewed. Ten constituents recorded; eligible-student status under § 221(d)(1)(C) selected on a narrow production promise. |
| P2 artifact and consumer map | Complete and independently reviewed READY. Six findings, G1-G6. |
| P3 executable design | Complete and independently reviewed READY as a **decision-ready partial design**. Obligation 2c discharged; **2a and 2b not discharged**. |
| Track 0 adversarial closure | **Not started.** |
| Contract unit, Track 1, Track 2 | **Not started.** No production code, content, schema, or package version was written. |

**Why it closes partial.** P3's executable probe established a bounded result: No committed path can currently use every current Form 1098-E box-1 statement as the iteration subject, require exactly one usable statement association, resolve the heterogeneous related facts this case needs, fail closed on an unassociated statement, and preserve statement-isolated dependencies. The actual pairing dispatcher iterates existing pairing records, so an unpaired box-1 statement is never visited and produces neither a publication nor a blocked row. The owner declined a fourth one-off
exact-rule coordinator and directed the capability out to a prerequisite
milestone.

**Deferral ledger — preserved for the resumed milestone.**

- The selected eligible-student direction under § 221(d)(1)(C) via
  § 25A(b)(3)(A), unchanged and not narrowed.
- The narrow production promise, and the bounded path's premise: the loan is
  identified relationally as the sole loan a statement represents, the academic
  period is explicitly represented, and the whole statement amount is
  attributable to that sole loan.
- Fixed cases C0a-C10, including C7's three admissible resolutions.
- **Gap 1 — box-1-driven heterogeneous group-binding.** Addressed by the
  proposed prerequisite milestone
  (`PROPOSED-identified-evaluation-context.md`), for which this case is the
  forcing consumer.
- **Gap 2 — an authoritative catalog-input contract.** A separate required
  blocker, deferred for sequencing only and not conceptually dependent on
  gap 1. It is the next explicit decision after the prerequisite lands, before
  production resumes.
- **Gap 3 — an explanation carrier.** Deferred, retained as a **production
  condition**: the resumed milestone must eventually identify which statement
  was excluded and the supported reason. The narrowed presentation is a
  description of current limitations, not the final product promise.
- P0 F7's closed-empty production condition, unaddressed and still standing.
- The stale text recorded at P2: the worksheet's notes overstate its universal
  conjuncts and conditional dependency members; the engine-breadth plan cites a
  stale runner line range; a Track 8 test name contradicts its own golden; VOID
  exclusion is prose rather than an executing filter.

**Retained evidence and future use.** None of this is a binding contract. Each
artifact is classified by what it may be used for.

| Artifact | What it is | Future use |
| --- | --- | --- |
| `student-loan-interest-deduction-translation-evidence/` | Tax-boundary evidence for ten section 221 constituents | For the **resumed student-loan vertical**. Not an input to the engine contract, except that it defines the forcing consumer's bounded meaning. The prerequisite's builders should not absorb the full tax analysis. |
| `student-loan-interest-deduction-translation-evidence/` | A map of committed behavior **at the examined source state** | Useful for locating consumers and comparison surfaces. Later work **must revalidate it against current code** before relying on any specific claim. |
| `student-loan-interest-deduction-translation-evidence/p3-partial-design.md` | A partial design and requirements record | **Not an accepted contract**, and not evidence that the mechanisms it proposes work. Obligations 2a and 2b are undischarged. |
| `docs/prototypes/sli-eligible-student/probes/feasibility.py` and its findings | Reproducible evidence for the bounded dispatcher and coverage failure | Directly reusable, **with its stated limitations**: hand-built environment, authored pins, projection over synthetic rows, conceptual box-1 completeness, partial mechanics witness, unproven pin isolation. |
| This plan's **deferral ledger** | The routing surface for what the resumed milestone must preserve | **Authoritative** for that question. |

## Success and stop conditions

The milestone succeeds when one selected constituent condition is replaced by a
complete ordinary-fact-to-rule-owned-consequence production path, the
closed-empty disposition is corrected, and the bounded deduction remains
coherent through durable presentation. It also
succeeds as an explicit partial result if reviewed evidence shows that none of
the candidates can be bounded without first deciding a larger identity or
domain contract; that result must name the smallest forcing decision and must
not fabricate a production track.

Stop and return to the owner if:

- P1 cannot select one case without making an unresolved legal determination;
- the selected ordinary proposition requires a materially broader person,
  household, loan, education, or payment identity model than this milestone can
  test with one consumer;
- a current accepted contract would need semantic supersession rather than an
  additive bounded successor;
- fixing the selected path requires redesigning the worksheet, Schedule 1, or
  AGI generally rather than connecting one tax consequence; or
- two representations remain materially different but no named consumer can
  discriminate them.

## Exit criteria

1. P0-P3 each have independently reviewed evidence, and their surviving
   conclusions are integrated into this plan before Track 0 closes.
2. The publication explains in plain language how the source report, ordinary
   circumstance, rule-owned tax meaning, MAGI limitation, and return result
   differ and connect.
3. One forcing case is selected with an exact proposition, authority, identity,
   lifecycle, consumer, invalidators, and unsupported nearby inference.
4. Every artifact in *Track 0 adversarial closure* passes — including the
   closed-empty disposition — or the milestone closes explicitly partial
   without implementation.
5. If production proceeds, C0a-C10 are exercised through the real contribution,
   package, derivation, durable run, and presentation path.
6. If production proceeds, the closed-empty path yields an unavailable or
   blocked Student Loan Interest Deduction, explained as the source evidence not
   establishing whether interest was paid: no numeric zero reaches Schedule 1
   line 21, and neither line 26 nor AGI is computed from one. This holds
   whichever gate P1 selected. Rendering a separate source-status statement is
   not required. The documentless-interest input route may remain
   unimplemented; the limitation is then stated on that path rather than
   inferred away.
7. The user is not asked to supply the selected tax conclusion, and missing
   ordinary support is not treated as a favorable answer.
8. Existing cap, phaseout, Schedule 1 line 21/26, AGI, and unrelated package
   behavior remain compatible or any deliberate correction is separately
   evidenced and reviewed.
9. Reader-facing provenance distinguishes the lender report, user-attributed
   ordinary facts, adopted tax rule, derived inputs, and deduction result.
10. The roadmap states which parts of the translation cadence transferred,
   extended, failed, or remain domain-specific; it does not claim universality.
11. The final curated candidate passes governance lint, envelope scan,
    `git diff --check`, author-independent review, and CI on the exact head.
