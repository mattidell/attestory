# A0 — the tax concept facts the engine operates with

The work of action A0, per its
[refinement](../student-loan-circumstance-association.md#a0-in-detail--modelling-the-tax-concept-facts).
Consulted the [owner-stated facts](owner-stated-facts.md) first.

Evidence levels: **`read`** for anything read off committed content or statute;
**`run`** only where the readiness-gate checks executed it. No claim here is
`run` unless marked.

## The two relations, and a third thing

- **On the path to** — a fact is a step in working out another fact.
- **Sits behind** — a fact bears on another fact's correctness without being a
  step in working it out. Removing it changes whether the answer is right; it
  never appears in the arithmetic.
- **Support** — what the product accepts as adequate grounds for taking a route.
  Not the same as the fact being proven. A supported determination is a
  determination; it is not a finding that the underlying fact is true.

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
silently zeroes. *Standing of the result:* supported only. What stays unproven is
twofold — that the composition is as the person says, and, because the operator
is a universal over members, *which* statement any particular answer was about.
A "yes" from every member is not five attributed facts.
**Engine represents them today:** yes, five `f1098e.no-*` fact types.

### F5 — Every loan the interest was paid on is a qualified education loan

**Stage:** behind F2. **Sits behind, not on the path**, established `read` from
the worksheet itself: no step from box 1 through the cap, the threshold, the
phase-out ratio and the reduction computes or reads loan qualification. Its only
appearance anywhere in the route is as one per-statement negative witness in the
conditional set. The owner's statement that *loan eligibility status does not
directly impact total student loan interest deduction* corroborates this; it is
not the evidence for it.

**Routes.** *R5a:* the person states it, in the form the application poses —
"all of your student loans must be eligible", per the owner's item 7. *R5b:*
derived from an enumeration plus facts about the institution and the borrowing.
*Concurrency:* both could hold at once and could disagree; nothing here says which
governs.

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

**Routes.** *R6a:* the person's ordinary account of their schooling for a named
period — which the previous milestone showed works in the adverse direction and
not the favourable one. *R6b:* institutional and public-authority
determinations, for which no producer exists. *Concurrency:* not a real case
today, since R6b has no producer.

*Grounds the product accepts:* undecided. The previous milestone established, at
`run`, that an adverse ordinary answer defeats the test on its own, while a
favourable answer needs credential recognition, institution eligibility and a
half-time threshold, none of which has a producer. *Standing of the result:*
asymmetric, and this is the milestone's central fact. An adverse answer is
**adequate grounds for a supported determination that the test fails** — one
required conjunct fails and the test fails with it, on the person's ordinary
knowledge alone. It is not proof that the person was ineligible, and a later action
must not promote it to one. A favourable answer is weaker, and could not rise above
supported without producers that do not exist.
**Engine represents it today:** no. Nothing.

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
separately answerable and separately behind F2, grouped here only because their
grounds are alike. **On no path:** none appears in the arithmetic.
*Grounds:* the person's answers, and for filing status the return's own.
*Standing:* supported, and least troubling of the set — these are facts a person
ordinarily knows about themselves.
**Engine represents them today:** yes, all of them.

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

**1. The pattern this milestone needs is already implemented once.** F4 is a set
of behind-facts collected from the person, per statement, precisely because the
box-1 route cannot say what the amount consists of. A5 does not need to invent the
shape of a behind-fact; one exists, with a producer and a consumer.

**2. But the existing shape is a universal negative, and the new fact may not be
one.** `collect_categorical_all_equal` asks whether every member answers the same
way. It carries "no statement's interest is on a non-qualified loan". It cannot
carry "this statement's interest concerns that period". A5 still has to choose a
shape, and reusing the universal negative is **one candidate among others**,
attractive because the adverse direction is what the previous milestone validated
at `run`. This does not shrink A5's question: the statement-to-borrowing-and-period
relationship is still listed above as unrepresented, and nothing here shows it can
be avoided.

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

So the engine's established convention is **model a behind-fact, then require it**.
What happens today is not that unanswered behind-facts are ignored; it is that F5
and F6 are *not modelled at all*, so they are never asked and never block. The
deduction computes without them because they are absent from the model, not because
absence is tolerated.

That matters to A3 and A5. A3 cannot treat "never posed" as owing no response on
the general ground that unanswered behind-facts are the norm — they are not. It is
owed no response only while the fact sits outside the model, and the moment this
milestone models a schooling fact, the existing convention would require it.
Whether to follow that convention is a real choice with a real consequence, and it
is not settled here.

**5. The engine never separates support from proof in one place.** Every
behind-fact is accepted on the person's own categorical answer, with no record
distinguishing "the person said so" from "this is established". A6 will need that
distinction to be visible, because F5 and F6 are where a person's answer is least
like proof.

**6. Standing is not uniform, and it varies in a way that matters.** Reading the
per-route standing across the list: F3's is arithmetic; F7 and F8 rest on things a
person ordinarily knows about themselves; F4's rests on the person's answer and,
because its operator is a universal over members, does not even attribute an
answer to a statement; F5 asks the person for what is effectively the conclusion
of a statutory test; F6's is asymmetric, strong adverse and weak favourable. So
"the person told us" covers at least four different qualities of grounds, and the
engine records them identically. A1 should ask different things of a person in
each case, and A6 should be able to show which kind of grounds a result rests
on.
