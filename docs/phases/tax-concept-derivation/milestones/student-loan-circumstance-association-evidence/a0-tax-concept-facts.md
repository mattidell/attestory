# A0 — the tax concept facts the engine operates with

The work of action A0, per its
[refinement](../student-loan-circumstance-association.md#a0-in-detail--modelling-the-tax-concept-facts).
Consulted the [owner-stated facts](owner-stated-facts.md) first.

Evidence levels: **`read`** for anything read off committed content or statute;
**`run`** only where the readiness-gate checks executed it. No claim here is
`run` unless marked.

## What belongs in this model, and what does not

Owner direction, 2026-09-22. Two pursuits run alongside each other and must not be
conflated.

**Tax concept derivation — this document.** The tax concept represents the *nature of
the tax consequence rules*, so the facts here are held **along the same lines as the
rule**. `legally obligated to pay the interest` is a positive fact because
26 CFR § 1.221-1(b)(1) states it positively; `eligible student` is a positive fact
because § 221(d)(1)(C) does. The model does not reshape a condition to suit how it will
be obtained.

**The translation layer — A1's territory, not this document's.** How a positive
condition is *arrived at* from ordinary statements is a different question, and its
formula is **default user expectation plus any disqualifiers**. An earlier version of
this section held that material here; it has moved to A1, where it belongs.

Two consequences worth stating, because they are what the separation buys:

- **A translation-layer limitation is not a tax-concept change.** That we cannot yet
  enumerate the circumstances defeating a legal obligation is a fact about the
  translation layer. The concept stays positive either way, and the question's polarity
  can change without the fact changing.
- **It is also why the responsibility category is coherent.** Institutional eligibility
  remains a condition of the rule and stays in the model. What the translation layer
  declines to do is *establish* it. Keeping the condition while declining to produce it
  is only expressible because the two layers are separate.

**Deferred, not blocking:** what it takes to *be* legally obligated. The regulation
supplies the test and not its application, and a co-signer being obligated is as far as
this milestone needs to go.

## The two relations, and a third thing

Both relations are **relative to a route**, and they are **not mutually
exclusive**. The same fact can be on the path by one route and behind by another,
and it can be both at once for a single route when it enters the working in one
place and constrains the result in another. Asking "is this fact behind or on the
path" without naming a route is malformed.

- **On the path, by a route** — the fact is a step in working out another fact by
  that route.
- **Sits behind, for a route** — the fact bears on whether the result that route
  produces is correct, without being a step in producing it.
- **Support** — what the product accepts as adequate grounds for taking a route.
  Not the same as the fact being proven. A supported determination is a
  determination; it is not a finding that the underlying fact is true.

**Worked example of the relativity, so it is not mistaken for pedantry.** Filing
status is behind the deduction for the married-filing-separately exclusion, and
simultaneously on the path, because the MAGI threshold and the phase range are
both filing-status-keyed parameters. Qualified-education-loan status is behind the
deduction by the box-1 route, and plausibly on the path by an enumeration route,
where one would sum the interest on qualifying loans. Neither fact has a single
intrinsic answer.

## Stages of the calculation

Established `read` from `rule.sli-worksheet.json` and
`rule.sli-worksheet-line1-subtotal.json`.

1. Interest reported per statement (Form 1098-E box 1)
2. Total interest paid — worksheet line 1, capped
3. Modified AGI, the threshold, and the phase-out ratio — lines 2–7
4. The reduction — line 8
5. The deduction — line 9, published as Schedule 1 line 21
6. Adjusted gross income

## The facts

### F1 — The amount of student loan interest this person paid in the tax year

**Stage:** 1, aggregated to the *uncapped* line 1. The cap is a limit on the
deduction and belongs to F2's path, not to how much interest was paid.

**Routes.**

*R1a — the lender statements.* Sum box 1 across the person's Form 1098-E
statements. *Establishes:* the amount lenders reported as student loan interest
received from this person. *Does not establish:* which loans it was on, whether
each is a qualified education loan, which institution or academic period any of
it financed, or whether the whole amount is even interest of the deductible kind.
*Rests on:* a payer's information return, admitted as evidence.
*Grounds the product accepts:* the admitted statement itself. *Standing of the
result:* a supported figure, not a proven one — what stays unproven is that the
amount is interest of the deductible kind, since the five composition statements
in F4 are the person's own answers and the statement itself distinguishes
nothing.

*R1b — an enumeration of loans.* The person's student loans and the interest paid
on each. Not "qualified" loans — that is F5, and a route to an amount must not
arrive pre-filtered by a fact that sits behind it. *Establishes:* the amount, via
per-loan figures. It also *exposes* what each loan was for, which R1a cannot — but
exposing composition is not establishing this fact, which is an amount.
*Does not establish:* that the person's account of each loan is correct, or
that the enumeration is complete. *Rests on:* the person's own records.
*Grounds the product accepts:* not yet decided — there is no such route in the
engine. The owner names a "fill out student loan data into this spreadsheet"
action as where it would live. *Standing of the result:* whatever is decided, it
would rest entirely on the person's own account, so it could not be stronger than
supported.

**Neither is a lesser version of the other.** R1a is complete as to amounts and
silent as to composition. R1b is the reverse: it can be wrong or partial about
amounts while saying exactly what each loan was for.

**Both at once is a real case.** A person can hold statements *and* enumerate,
and the two need not agree. Nothing in this model says which governs when they
disagree, and nothing should: that is a product decision for a later action, and
it is the strongest argument against treating either route as the canonical
one.

**Sits behind it:** F4 (what the reported amount consists of).
**Engine represents it today:** yes, via R1a only — `f1098e.box1-student-loan-interest`
keyed on lender + statement + tax-year, summed into
`sli-worksheet.line1-total-interest-paid-subtotal` over the closed family
`f1098e.1`, whose closure claim authorises exactly that subtotal.

### F2 — The amount of that interest that is deductible

**Stage:** 5. The fact the owner named.

**Routes.** Through the worksheet from F1 and F3, with the cap and the phase-out.
It inherits F1's two routes to the amount rather than having a single conceptual
path of its own. **F5 is not an input to this arithmetic** — see the behind-list
below. *Establishes:* the deduction as the worksheet computes it. *Does not
establish:* any of the facts behind it. *Rests on:* the arithmetic over F1, F3,
the cap and the phase range.
*Grounds the product accepts:* a computed result whose provenance names the
statement findings, the scope findings, the parameters, the rule and its
authority. *Standing of the result:* a supported determination, never a proven
one. Its standing is **mixed rather than uniformly testimonial**: F1 by R1a rests
on a payer's information return, F3 is arithmetic, and the behind-facts rest on
the person's own categorical answers. The deduction is no stronger than the
weakest of those. This is the same distinction the
nominee-interest milestone drew about its own reduction.

**On the path to it:** F1, F3 (modified AGI), and the parameters.
**Sits behind it:** F4, F5, F6, F7, F8.
**Engine represents it today:** yes — `schedule1.line21-sli-deduction`.

### F3 — Modified adjusted gross income, and where it falls in the phase-out

**Stage:** 3. **On the path to F2**, not behind it — it is an input to the
arithmetic.

**Route.** From total income and the filing-status-keyed threshold and phase
range. *Rests on:* `tax.us.2025.income.total-income`,
`tax.us.2025.parameter.sli-magi-threshold` and
`tax.us.2025.parameter.sli-magi-phase-range`. *Grounds:* the computation itself.
*Standing:* as good as total income is; what stays unproven is whatever total
income rests on, which is outside this model. One route only; no concurrency.

**It is on the path because it appears in the arithmetic of lines 2–7**, not
because its standing is arithmetic rather than testimonial. Path-versus-behind asks
whether a fact is a step in the working, never how good its grounds are — F1 rests
on a payer's return and is squarely on the path. Using standing as the test would
mis-sort later facts.

Strictly this entry holds two things: modified AGI, a fact; and where it falls in
the phase range, which is arithmetic over it. Treat the ratio as path-arithmetic
from MAGI rather than as a second fact.
**Engine represents it today:** yes — the three symbols named above, consumed by
the worksheet's lines 2–7.

### F4 — What the reported amount consists of

**Stage:** behind stage 1–2. **Sits behind F1**, and through it behind F2.

This is five separate facts the engine already keeps, each a statement by the
person about one Form 1098-E:
`tax.us.2025.f1098e.no-related-person-interest`,
`no-qualified-employer-plan-interest`, `no-non-qualified-loan-component`,
`no-employer-educational-assistance-interest`, `no-qtp-earnings-used`.

**Why they exist is the point.** Route R1a reaches F1 and cannot say what the
amount consists of, so the engine collects the composition facts *separately*,
from the person, per statement. That is this milestone's pattern already
implemented: a route reaching a fact, and the facts behind it gathered on their
own.

*Grounds the product accepts:* the person's own answer, as a categorical yes/no
per statement. Read with `collect_categorical_all_equal`, which asks whether
**every** member answers the same way — a universal negative, not a per-statement
lookup. A single "no" blocks with `SLI_UNIVERSAL_COMPONENT_VIOLATION`; it never
silently zeroes. *Standing of the result:* supported only. What stays unproven is that the
composition is as the person says.

**Attribution is not lost, and an earlier version of this entry said it was.**
Each witness fact type is keyed `lender` + `statement` + `tax-year`, exactly like
box 1, so every witness finding carries the identity of the statement it concerns.
Marshalling preserves those identities, and the runner pins **every collected
finding individually** by finding id (`packages/derivation/runner.py`, the
`access.collects` loop). So the records supporting the answer remain identifiable
in provenance.

What the operator yields is one aggregate Boolean: the expression sees no
per-member value and cannot branch on one. That is a limit on what a *rule
expression* can read, not a loss of identity in the record. The two must not be
conflated — a consumer that returns one Boolean has not erased its inputs.
**Engine represents them today:** yes, five `f1098e.no-*` fact types.

### F5 — Every loan the interest was paid on is a qualified education loan

**Stage:** behind F2 **by the box-1 route**. Plausibly on the path by an
enumeration route, where the interest summed would be that on qualifying loans;
that route does not exist, so nothing here settles it. For R1a, established `read`
from the worksheet itself: no step from box 1 through the cap, the threshold, the
phase-out ratio and the reduction computes or reads loan qualification. Its only
appearance anywhere in the route is as one per-statement negative witness in the
conditional set. The owner's statement that *loan eligibility status does not
directly impact total student loan interest deduction* corroborates this; it is
not the evidence for it.

**Routes.** **There is no route that establishes this favourably.** *R5a:* a rule reads
the F9 circumstances and can conclude that the classification **fails**, one defeated
constituent being sufficient; it concludes nothing in the other direction, and the
bounded calculation does not need it to. *R5b:* additionally from facts about the
institution; **not a route this milestone builds**, because those are conditions the
person is responsible for rather than things determined. *Concurrency:* not a live
question while R5b is not a route. See F9's three outcomes — proceeding is not
establishing.

**Sits behind it:** F6.

*Grounds the product accepts:* today, partially and obliquely — the
`no-non-qualified-loan-component` witness in F4 is a per-statement negative that
covers part of this ground. There is **no** fact type for qualified-education-loan
status as such. *Standing of the result:* supported at best, and weakest of any
fact here — the person is being asked, in effect, for the conclusion of a
statutory test, which is exactly what the milestone's boundaries forbid asking
for directly. That tension is real and belongs to A1. *Does not establish:* the
constituents below.
**Engine represents it today:** no, not as a fact. Only the negative witness.

### F6 — The student was an eligible student for the academic period the loan financed

**Stage:** behind F5, which is behind F2. **Two levels behind**, and on no path.

This is the previous milestone's subject: `§ 221(d)(1)(C) → § 221(d)(3) →
§ 25A(b)(3)(A) → HEA § 484(a)(1)`, with `26 CFR 1.221-1(e)(3)(i)(B)`.

**Routes.** *R6a:* the person's ordinary account of their schooling for a named period
— the F9 circumstances. It supports an **adverse** determination and nothing favourable,
which is F9's first and third outcomes and not a deficiency in the first. *R6b:* institutional and public-authority
determinations. **R6b is not an unbuilt route; it is not a route.** Institutional
eligibility, credential recognition and the half-time standard are represented as
conditions the person is responsible for, which the application does not establish and
no calculation consumes. *Concurrency:* not applicable.

*Grounds the product accepts:* an adverse ordinary account, and nothing on the other
side. *Standing of the result:* asymmetric, and this is the milestone's central fact.

An adverse answer is **adequate grounds for a supported determination that the test
fails** — one required conjunct fails and the test fails with it, on the person's
ordinary knowledge alone, established at `run` by the previous milestone. It is not
proof that the person was ineligible, and a later action must not promote it to one.

**A favourable ordinary answer establishes nothing.** Not a weak positive, not a
determination of lesser standing — nothing. The institutional conditions it would need
are not unbuilt producers waiting to be supplied; they are conditions the person is
responsible for, and no route reaches them. Where no adverse answer is supported the
calculation proceeds, and that is F9's second outcome, never its third.

### F9 — The ordinary circumstances that contribute to F5 and F6

**Added after A1 and the responsibility direction.** F5 and F6 were placed as
composites, and A1 then posed the circumstances beneath them. Those circumstances are
facts in their own right and belong on this list; without them A1 poses what this model
never placed.

Each is an ordinary description a person supplies, normalised by the translation layer.
None is a classification, and none establishes the composite it contributes to.

**Two of them are not about the loan at all.** Employer-paid interest and
qualified-tuition-programme earnings concern what paid the *interest* reported on a
statement — the double-benefit rule — not whether the borrowing qualifies. Grouping
them with the employer-plan circumstance, as an earlier version of this table did,
would let an adverse answer disqualify a loan when what it actually bears on is an
amount. **What the incumbent worksheet does with either is block the whole route**; a
different consumer treating them as amount facts is A5's to select, not something this
model asserts.

| Circumstance | Contributes to | Stage |
| --- | --- | --- |
| What the borrowed money paid for, and whether it paid for **only** that | F5, constituent 1 (the chapeau) | Behind F2 by the box-1 route |
| Whose education it paid for — the person, a spouse, a dependent | F5, constituent 2 | Same |
| Who lent the money | F5, constituent 5 (related-person indebtedness) | Same |
| Borrowing against an employer's plan | F5, constituent 6 — takes the indebtedness out of the class | Same |
| An employer paid interest on these loans under an educational assistance programme | **Not a constituent.** A § 221(e)(1) double-benefit witness about what paid the *interest*, not about the loan's classification | Behind F1's amount |
| Qualified-tuition-programme earnings were used to pay this interest | **Not a constituent**, same double-benefit ground | Behind F1's amount |
| Attendance at an identified institution for an identified period | F6 | Behind F5, which is behind F2 |
| Enrolment in an identified programme | F6 | Same |
| Course load for that period | F6, with the threshold itself a responsibility | Same |

*Routes:* the person's own account, normalised. *Grounds:* their own answer.
*Standing:* supported only, and the qualities differ — what money paid for is ordinary
recall; who lent it is ordinary; a course load is ordinary but its sufficiency is not.
*Engine represents them today:* four of them are, each by its own committed fact type —
`f1098e.no-related-person-interest`, `no-qualified-employer-plan-interest`,
`no-employer-educational-assistance-interest` and `no-qtp-earnings-used`, one per row
rather than part of a bundled one. The use-of-proceeds, whose-education, attendance,
enrolment and course-load rows have no representation.

**Three outcomes, kept apart.** An earlier version said the composite is "assembled by
rule", which implied the classification gets derived. It does not. What a rule can
conclude from these circumstances is one of:

1. **An adverse determination is supported.** A relevant circumstance defeats a
   constituent, and one failed constituent defeats the classification. This is a real
   conclusion and it stands on its own — it is not weakened by the fact that
   establishing the favourable classification would need more. *Conceptual relationship
   from the statute's conjunction; executed at `run` for the enrolment case by the
   previous milestone, on disposable artifacts.*
2. **No adverse determination is supported**, so the bounded calculation proceeds.
   *Selected behaviour* — the owner's non-gating posture. Not yet executed in the new
   consumer.
3. **A complete favourable classification is established.** *Nothing produces this.* No
   route reaches it, and the bounded calculation does not require it.

**The second does not establish the third.** Proceeding because nothing adverse was
said is not a finding that the loan qualifies, and no part of this model may be read as
though it were. The institutional constituents are not established at all — they are
conditions the person is responsible for.

### F7 — The person is legally obligated to pay the interest

**Stage:** behind F2. **Engine represents it today:** yes,
`sli-scope.legally-obligated-for-interest`, a filer-level statement by the person.
*Routes:* the person's answer; or the loan documents, which would be a second route
and has no producer. *Concurrency:* not a real case today. *Grounds:* their own
answer. *Standing:* supported only — what stays unproven is whether the obligation
exists, a question about the documents. **On no path:** it appears nowhere in the
worksheet arithmetic.

### F8 — The person is not claimed as a dependent, and other filer-level exclusions

**Stage:** behind F2. **A family of distinct facts, not one proposition** —
`sli-scope.not-claimed-as-dependent`, `sli-scope.no-form-2555`,
`sli-scope.no-form-4563`, `sli-scope.no-puerto-rico-or-samoa-income`, and, outside
the conditional set because its domain is five statuses rather than yes/no, filing
status, where married-filing-separately blocks with `SLI_MFS_INELIGIBLE`. Each is
separately answerable, grouped here only because their grounds are alike.

**Filing status is both behind and on the path**, and is the clearest instance of
the relativity above: behind, for the MFS exclusion; on the path, because
`parameter.sli-magi-threshold` and `parameter.sli-magi-phase-range` are each keyed
by the five filing statuses, so it selects the arithmetic. The four
`sli-scope.*` absences are behind only — none appears in the arithmetic.
*Grounds:* the person's answers, and for filing status the return's own.
*Standing:* supported, and least troubling of the set — these are facts a person
ordinarily knows about themselves. What stays unproven is what another return or
the underlying documents would say, not the person's knowledge of their own
status.
**Engine represents them today:** yes, all of them.

## What has no representation, and how that was checked

**The search.** Every `fact_types` entry in every JSON file under
`packages/content/` was enumerated and filtered for `loan`, `eligible` or
`student` in its **id**. The complete result is two ids:
`tax.us.2025.f1098e.box1-student-loan-interest` and
`tax.us.2025.f1098e.no-non-qualified-loan-component`. Nothing matching
`qualified-education-loan` or `eligible-student` exists anywhere in committed
content. The absences below are therefore `read` findings from that search, not
inferences from the worksheet failing to read something. (Filtering the whole
fact-type body rather than the id matches more entries, mostly "student loan" in
SLI titles; the id filter is the right search for "is there a fact type for
this".)

## What has no representation

| Fact | Status |
| --- | --- |
| F5 — qualified education loan | No fact type. Partially and obliquely covered by one per-statement negative witness |
| F6 — eligible student for the period | Nothing at all |
| R1b — an enumeration route to F1 | No route exists |
| The relationship between a statement and a borrowing and a period | Nothing. This is the deferred item E1 |

## Verified: what the 1098-E route does not carry

Owner item 12 — the 1098-E may not enumerate the loans, the issuers, and what
institution the user attended — is confirmed `read` against
`packages/content/tax/2025/f1098e.bundle.json`. Box 1's identity keys are lender,
statement and tax-year; its value is a single number; the fact type's own title
records that a lender may aggregate several qualified student loans on one
statement. There is no loan identifier, no per-loan amount, no institution and no
academic period anywhere in the bundle. So the absence is a property of the form
as modelled, not an omission in our content.

## Findings that bear on later actions

**1. The abstract pattern exists already; whether its shape transfers is a separate
question.** F4 is a set of behind-facts collected from the person, per statement,
precisely because the box-1 route cannot say what the amount consists of. So the
*idea* of a route reaching a fact while the facts behind it are gathered on their
own is implemented, with a producer and a consumer. Whether its concrete shape can
carry what this milestone needs is finding 2, and the answer there is no.

**2. But the existing shape is a universal negative, and the new fact may not be
one.** `collect_categorical_all_equal` asks whether every member answers the same
way, so a rule expression using it sees one Boolean and cannot branch per member.
It carries "no statement's interest is on a non-qualified loan". It does not carry
"this statement's interest concerns that period" as a value the expression can read.

A5 still has to choose a shape, and reusing the universal negative is **one
candidate among others**. Nothing here narrows the question: the
statement-to-borrowing-and-period relationship is still listed above as
unrepresented, and nothing shows it can be avoided.

**What this is not.** It is not a finding that the engine cannot dispatch per
identified item, and it is not a requirement to restructure the prior
calculation. The pairing-scope observation was made in an environment **rebuilt in
a test module**, mirroring the shape of a **specialized adapter written for
nominee interest**, whose two bound symbols and empty source set are that adapter's
choices rather than the dispatcher's limits. What is bounded is that environment.
The mechanism choice is open, and includes adapting or writing an adapter with a
different environment.

**3. F6 is two levels behind F2, not one.** It sits behind F5, which sits behind
F2. The plan has been treating the schooling circumstance as though it bore
directly on the deduction. It does not.

**4. What is missing is behind the answer, not on the path — but "missing" and
"tolerated" are different, and this is where an earlier version of this finding was
wrong.**

First, **not every route is represented**: R1b is a route to F1, which is on the
path to F2, and it does not exist in the engine. The accurate statement is that
every *fact* currently on the path has a representation.

Second, and more consequentially: **an unanswered behind-fact is not tolerated
today — it blocks.** Established `read` from `rule.sli-worksheet.json`: the
seventeen scope and absence facts sit in a `conditional_dependency_set` whose
condition is `count(box1) > 0`, so the moment a Form 1098-E exists every one of
them is required, and an absent member raises `DEPENDENCY_ABSENT` naming it. The
five per-statement witnesses are likewise required, and a single "no" blocks with
`SLI_UNIVERSAL_COMPONENT_VIOLATION`.

**What follows is a fact about that rule, not a law about representation.** The
worksheet rule requires *those particular named answers* because its own
declaration names them in its dependency set. Representing a fact does not make it
mandatory: an obligation exists only where some consumer's declaration creates one.
Nothing about adding a schooling fact to the model would, by itself, make any
existing rule require it.

So the question is not "will modelling it make it required" but **which named
consumer would need this information, and what does that consumer do when it is
absent**. That is a question about a specific rule and a specific case, and it is
answerable only once there is a consumer to name — which is A3's and A5's work,
not something settled by observing the worksheet's current dependency list.

What happens today is simply that F5 and F6 are not modelled, so no consumer names
them, so nothing asks and nothing blocks.

**5. A6 will need the difference between "the person said so" and "this is
established" to be visible — and the kernel already draws a coarse version of it.**
Every behind-fact in this model is accepted on the person's own categorical answer,
and nothing in the entries above records that standing alongside the result.

The search this finding previously declined to make has since been made, and it
found something: `packages/schemas/kernel/finding.v2.schema.json` carries a `basis`
of `documentary` / `attested` / `elective`. That maps onto the coarsest cut here —
R1a's payer return is documentary, the person's answers are attested.

**No storage conclusion follows, and an earlier version of this finding drew one.**
It concluded that what was missing is finer resolution *within* `attested`. That is
a proposal about representation derived from a distinction in the domain model, with
no consumer asked. The distinctions belong here, in the model, because they are true
of the facts. Whether anything needs to *store* them differently depends on what a
concrete consumer must distinguish, and on whether the existing facts, evidence and
rules already let it — a rule can read the facts themselves, and provenance already
names the findings a result rests on. That question is for whoever names the
consumer; it is not answered by this model and must not be pre-empted by it.

**6. Standing is not uniform, and it varies in a way that matters.** Reading the
per-route standing across the list:

- **F1 by R1a is documentary** — a third party's information return. Neither the
  person's word nor a computation, and not to be folded under "the person told us".
- F3's is arithmetic.
- F7 and F8 rest on things a person ordinarily knows about themselves.
- F4's rests on the person's answer. Its operator yields one Boolean, so a rule
  expression cannot branch on a member's answer — but the answers themselves are
  keyed by statement and each supporting finding is pinned, so attribution is
  preserved in the record. What is coarse is the *expression's* view, not the
  evidence.
- F5's grounds *would be* the conclusion of a statutory test, which is precisely why
  A1 does not ask for it.
- F6's is asymmetric: adequate to support failure when adverse, and **nothing at all**
  when favourable.

So grounds come in at least five qualities, of which four are testimonial.

**These are distinctions in the domain, and this model is where they belong.**
`finding.v2`'s `basis` separates `documentary` from `attested` from `elective`,
which cleanly divides R1a from the person's answers; the four testimonial qualities
sit inside `attested` together. Whether that matters is not a question this model
can answer, because it depends on what a consumer must distinguish and on whether
the facts, their evidence and the rules already supply it — provenance, for
instance, already names the findings behind a result, and a rule can read the facts
themselves rather than a label about them.

What follows for later actions is narrower than a storage need: A1 should put
different things to a person across the four testimonial qualities — F3 is not among
them, being nobody's answer, and R1a is not either — and whoever names a consumer
that must show what a result rests on should first establish what it needs to
distinguish and trace whether that already survives. In F4's case it does: the
statement-keyed findings and their pins are there, so a consumer needing
per-statement attribution would be reading the record rather than asking for a new
one.
