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

**Stage:** 1 → 2, before the worksheet's own arithmetic.

**Routes.**

*R1a — the lender statements.* Sum box 1 across the person's Form 1098-E
statements. *Establishes:* the amount lenders reported as student loan interest
received from this person. *Does not establish:* which loans it was on, whether
each is a qualified education loan, which institution or academic period any of
it financed, or whether the whole amount is even interest of the deductible kind.
*Rests on:* a payer's information return, admitted as evidence.
*Support the product accepts:* the admitted statement itself, plus five separate
per-statement statements from the person (see F4). Nothing about the loans is
proven.

*R1b — an enumeration of loans.* The person's qualified education loans and the
interest paid on each. *Establishes:* per-loan amounts and what each loan was
for. *Does not establish:* that the person's account of each loan is correct, or
that the enumeration is complete. *Rests on:* the person's own records.
*Support the product accepts:* not yet decided — there is no such route in the
engine. The owner names a "fill out student loan data into this spreadsheet"
action as where it would live.

**Neither is a lesser version of the other.** R1a is complete as to amounts and
silent as to composition. R1b is the reverse: it can be wrong or partial about
amounts while saying exactly what each loan was for.

**Sits behind it:** F4 (what the reported amount consists of).
**Engine represents it today:** yes, via R1a only — `f1098e.box1-student-loan-interest`
keyed on lender + statement + tax-year, summed into
`sli-worksheet.line1-total-interest-paid-subtotal` over the closed family
`f1098e.1`, whose closure claim authorises exactly that subtotal.

### F2 — The amount of that interest that is deductible

**Stage:** 5. The fact the owner named.

**Routes.** One, today: through the worksheet from F1, F3 and F5, with the cap
and the phase-out. *Establishes:* the deduction as the worksheet computes it.
*Does not establish:* any of the facts behind it — it consumes their answers.
*Rests on:* the arithmetic plus every behind-fact having been answered.
*Support the product accepts:* a computed result whose provenance names the
statement findings, the scope findings, the parameters, the rule and its
authority.

**On the path to it:** F1, F3 (modified AGI), and the parameters.
**Sits behind it:** F4, F5, F6, F7, F8.
**Engine represents it today:** yes — `schedule1.line21-sli-deduction`.

### F3 — Modified adjusted gross income, and where it falls in the phase-out

**Stage:** 3. **On the path to F2**, not behind it — it is an input to the
arithmetic.

**Route.** From total income and the filing-status-keyed threshold and phase
range. *Rests on:* `income.total-income` and two parameters.
**Engine represents it today:** yes.

### F4 — What the reported amount consists of

**Stage:** behind stage 1–2. **Sits behind F1**, and through it behind F2.

This is five separate facts the engine already keeps, each a statement by the
person about one Form 1098-E: that none of the interest is related-person
interest, none is on a qualified employer plan, none is a non-qualified loan
component, none is employer educational assistance, and no qualified tuition
programme earnings were used.

**Why they exist is the point.** Route R1a reaches F1 and cannot say what the
amount consists of, so the engine collects the composition facts *separately*,
from the person, per statement. That is this milestone's pattern already
implemented: a route reaching a fact, and the facts behind it gathered on their
own.

*Support the product accepts:* the person's own answer, as a categorical
yes/no per statement. Read with `collect_categorical_all_equal`, which asks
whether **every** member answers the same way — a universal negative, not a
per-statement lookup. A single "no" blocks with
`SLI_UNIVERSAL_COMPONENT_VIOLATION`; it never silently zeroes.
**Engine represents them today:** yes, five `f1098e.no-*` fact types.

### F5 — Every loan the interest was paid on is a qualified education loan

**Stage:** behind F2. **Sits behind**, emphatically not on the path — no step of
the worksheet computes it, and the owner states the matching product fact
directly: *loan eligibility status does not directly impact total student loan
interest deduction.*

**Routes.** *R5a:* the person states it, in the form the application poses —
"all of your student loans must be eligible", per the owner's item 7. *R5b:*
derived from an enumeration plus facts about the institution and the borrowing.

*Support the product accepts:* today, partially and obliquely — the
`no-non-qualified-loan-component` witness in F4 is a per-statement negative that
covers part of this ground. There is **no** fact type for qualified-education-loan
status as such. *Does not establish:* the constituents below.
**Engine represents it today:** no, not as a fact. Only the negative witness.

### F6 — The student was an eligible student for the academic period the loan financed

**Stage:** behind F5, which is behind F2. **Two levels behind**, and on no path.

This is the previous milestone's subject: `§ 221(d)(1)(C) → § 221(d)(3) →
§ 25A(b)(3)(A) → HEA § 484(a)(1)`, with `26 CFR 1.221-1(e)(3)(i)(B)`.

**Routes.** *R6a:* the person's ordinary account of their schooling for a named
period — which the previous milestone showed works in the adverse direction and
not the favourable one. *R6b:* institutional and public-authority
determinations, for which no producer exists.

*Support the product accepts:* undecided. The previous milestone established, at
`run`, that an adverse ordinary answer defeats the test on its own, while a
favourable answer needs credential recognition, institution eligibility and a
half-time threshold, none of which has a producer.
**Engine represents it today:** no. Nothing.

### F7 — The person is legally obligated to pay the interest

**Stage:** behind F2. **Engine represents it today:** yes,
`sli-scope.legally-obligated-for-interest`, a filer-level statement by the
person. *Support:* their own answer.

### F8 — The person is not claimed as a dependent, and other filer-level exclusions

**Stage:** behind F2. Covers `not-claimed-as-dependent`, `no-form-2555`,
`no-form-4563`, `no-puerto-rico-or-samoa-income`, and — outside the conditional
set, because its domain is five statuses rather than yes/no — filing status,
where married-filing-separately blocks with `SLI_MFS_INELIGIBLE`.
**Engine represents them today:** yes, all of them.

## What has no representation

| Fact | Status |
| --- | --- |
| F5 — qualified education loan | No fact type. Partially and obliquely covered by one per-statement negative witness |
| F6 — eligible student for the period | Nothing at all |
| R1b — an enumeration route to F1 | No route exists |
| The relationship between a statement and a borrowing and a period | Nothing. This is the deferred item E1 |

## Findings that bear on later actions

**1. The pattern this milestone needs is already implemented once.** F4 is a set
of behind-facts collected from the person, per statement, precisely because the
box-1 route cannot say what the amount consists of. A5 does not need to invent the
shape of a behind-fact; one exists, with a producer and a consumer.

**2. But the existing shape is a universal negative, and the new fact may not be
one.** `collect_categorical_all_equal` asks whether every member answers the same
way. It carries "no statement's interest is on a non-qualified loan". It cannot
carry "this statement's interest concerns that period". So whether the schooling
fact can use the existing shape depends on whether it can be honestly put as a
universal negative — which is the adverse direction the previous milestone
validated at `run`. That is a question for A5, and it is now a much narrower one
than "design a relationship".

**3. F6 is two levels behind F2, not one.** It sits behind F5, which sits behind
F2. The plan has been treating the schooling circumstance as though it bore
directly on the deduction. It does not.

**4. Nothing on any path to F2 is missing.** Every route and every step is
represented. What is missing is entirely behind-facts — which is why no
prerequisite was blocking a number, and why A3's earlier account of an
"unresolved statement" described a state that does not arise.

**5. The engine never separates support from proof in one place.** Every
behind-fact is accepted on the person's own categorical answer, with no record
distinguishing "the person said so" from "this is established". A6 will need that
distinction to be visible, because F5 and F6 are where a person's answer is least
like proof.
