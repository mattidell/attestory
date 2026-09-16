# P0 — product and evidence boundary

Gate charter for the **Student Loan Interest Bounded Method Transfer**
milestone. Owner-launchable: a cold agent can run P1 from this file plus the
committed plan.

- Milestone: `student-loan-interest-bounded-method-transfer`
- Plan: [`../student-loan-interest-bounded-method-transfer.md`](../student-loan-interest-bounded-method-transfer.md)
- Base: the ratified line as of the milestone plan commit on `milestone/student-loan-interest-bounded-method-transfer`
- Gate state: **COMPLETE** — repaired at owner direction, independently reviewed, repaired against that review's two material findings, and repaired again at owner direction. Closed before P1 began; its substantive content below is historical and unrewritten.
- Evidence levels used below: `authority` (statute, regulation, or IRS
  instructions read directly), `read` (committed artifact read at this base),
  `eval` (pure evaluator behaviour), `local` (hand-built prototype
  environment), `run` (`live_coordinate_run`), `durable` (durable output),
  `presentation` (reader-visible projection).

## 0. What this gate decides, and what it does not

P0 decides the product and evidence boundary: which ordinary fact is selected,
what each support route can honestly establish, which premises are stipulated,
whether the fixed cases need per-subject Evaluation Context, and what the
cheapest executable comparison is.

P0 draws no schema, ADR, package, contract, interface, or production code, and
does not repeat the ten-constituent survey. Every claim below carries an
evidence level; no claim is promoted above the level at which it was observed.

**P0 does not predict the production result.** § 11 records what remains
undetermined.

### Repair record — 2026-09-14

The first draft of this charter was repaired at owner direction before review.
Four of its errors are recorded here because they are the kind a later gate
could reintroduce:

1. **Documentary support was over-negated.** "Form 1098-E represents nothing
   about (C)" was too broad. Insufficiency is not unavailability (§ 3).
2. **A contradiction was invented.** The adverse ordinary fact does not
   contradict the lender's report; both can be true at once (§ 3.3).
3. **The ordinary fact was keyed to the loan.** It is a fact about a student at
   an academic period, which the loan rule *consumes* through a relation
   (§ 2.1).
4. **"Premise-free" was unqualified.** The adverse route avoids X1–X3; it still
   depends on the relationship premises (§ 2.4, § 4).

**Round 2**, against the independent P0 review. Two further material
errors, both mine, both repaired below:

5. **A lender-duty silence was claimed that does not exist.** The instructions
   *do* state, for revolving accounts resting on borrower certification, "You do
   not have to verify the borrower's actual use of the funds." The
   "absence of found text" framing is withdrawn (§ 3.2).
6. **The M6 refusal mechanism was cited from the wrong information return, and
   the actual Form 1098-E machinery does the opposite.**
   `MULTIPLE_F1098_OUT_OF_SCOPE` belongs to **Form 1098 (mortgage interest)**.
   No cardinality refusal exists for the Form 1098-E family, which by deliberate
   design *aggregates* multiple statements. The § 5 determination rested on that
   false basis and is **downgraded from a determination to an open question**
   (§ 5).

**Round 3**, at owner direction. Three further corrections:

7. **"M6 alone decides Evaluation Context" is withdrawn.** The Form 1098-E
   reporting unit is the issuer's choice — one form per loan or one for all loans —
   so M7 and X5a/X5b bear on the evaluation subject just as directly. And
   per-statement execution establishes a need for *separately attributable
   evaluation*, not for Evaluation Context: the trigger's conjunct (ii) is
   untested (§ 5.0, § 5.3).
8. **An unsafe disposition is removed.** Route-scoping to single-statement returns
   while leaving the aggregate route untouched would continue publishing the old
   deduction while holding unattributable adverse evidence. Replaced by three
   evidence states with required dispositions (§ 5.3).
9. **Route provenance was over-claimed.** A statement is not a single-basis
   object, and the form identifies no basis. "Originating on" a route is withdrawn
   (§ 3.1, § 3.2).

---

## 1. Four layers, in plain language

The milestone's whole difficulty is that four different things are easy to
confuse. They are separate objects with separate owners.

| Layer | Who says it | What it actually is | What it may never be used as |
| --- | --- | --- | --- |
| **What Form 1098-E reports** | The **Form 1098-E issuer** (the reporting filer — lender, servicer, governmental unit, or educational institution) | An amount of interest the issuer received in 2025 on a loan it treated as reportable, furnished on one identified statement | The complete § 221 deduction test; independent proof of every § 221(d)(1) predicate |
| **What an ordinary person can state** | The **tax-return filer** (the taxpayer) | A lived account of their own schooling — which school, which term, what they were enrolled in, how much they took | A legal conclusion. The person is never asked whether they were an "eligible student", nor whether a credential is legally "recognized" |
| **The intermediate tax concept** | An adopted rule | Eligible-student status under § 221(d)(1)(C) → § 221(d)(3) → § 25A(b)(3), determined *with respect to one academic period* | A field on the document, a user answer, or a property of tax year 2025 |
| **The deduction consequence** | An adopted rule | Whether this statement's box-1 interest is interest on a qualified education loan *as to (C)*, and what the worksheet, Schedule 1 line 21/26 and AGI then do | A complete Student Loan Interest Deduction authority. Every other § 221 constituent stays on its own handle or unresolved |

**Two different actors, never merged.** Throughout this charter, **tax-return
filer** means the taxpayer whose return is being prepared, and **Form 1098-E
issuer** (or *reporting filer*) means the party that furnished the statement. The
ordinary assertion belongs to the first; the document claim belongs to the second.
Bare "filer" is avoided in load-bearing passages precisely because it reads both
ways.

Two separations carry the whole milestone:

- The person supplies **facts about their life**; the rule owns the
  **classification** and the **number**. A user assertion that "I was an
  eligible student" is the wrong input, not a shortcut.
- **Absence of contradicting information is not an affirmation.** A route that
  proceeds because nothing conflicted has **not** obtained a statement from the
  person that every upstream condition held. Nor has it "relied on the document":
  the incumbent route depends on the Form 1098-E-derived subtotal, 24 direct
  determinable inputs, the derived total-income finding, family closure, and three
  parameters (§ 3.0). Proceeding on absence is a reliance posture that must be
  named accurately, never described as document-only.

---

## 2. The selected ordinary proposition

### 2.1 The proposition and its subject

Asked as an ordinary question, with no legal term in it:

> For that term, were you enrolled in — or accepted into — a program leading to
> a degree, certificate, or other credential, or were you taking individual
> classes that weren't part of any such program?

The premise-light adverse answer, in the person's own words:

> "I was taking individual classes during that term and was not enrolled or
> accepted into a degree, certificate, or other credential program."

- **Subject.** The **student** (here the tax-return filer, per X4) at an
  **identified academic period**, together with the **program relationship** between them.
  It is *not* a property of the indebtedness, of the statement, or of the
  return.
- **Time scope.** The identified academic period — a term at a named school.
  Tax year 2025 is a different object and is not a key of this fact.
- **How the loan rule reaches it.** The rule applies this student-period fact to
  an **identified loan** through a relation: the loan's proceeds paid for
  education, that education was furnished during that academic period. That
  relation is *separate support* the route must have (X5a, X5b), not a property
  of the ordinary fact.
- **Shape.** A closed ordinary partition over one named term:
  `{credential-program, individual-classes-only}`. It is *not* a `{yes, no}` on
  a legal predicate, and it is not the compressed
  `tax.us.2025.f1098e.no-non-qualified-loan-component` witness, which this
  milestone may not rename (P0 F5, P1).

**The user is not asked whether the credential is legally "recognized."** That
classification is not ordinary knowledge; it is X1.

### 2.2 Authority chain — verified at this base

`authority`. Verified 2026-09-14 against primary text:

| Step | Text | Source |
| --- | --- | --- |
| § 221(d)(1)(C) | interest must be "attributable to education furnished during a period during which the recipient was an eligible student" | 26 U.S.C. § 221(d)(1)(C), quoted in the retained P1 record |
| § 221(d)(3) | "The term 'eligible student' has the meaning given such term by section 25A(b)(3)." | same |
| § 25A(b)(3) | an eligible student, "with respect to any academic period", is a student who **(A)** meets HEA § 484(a)(1) "as in effect on the date of the enactment of this section", **and (B)** "is carrying at least ½ the normal full-time work load for the course of study the student is pursuing" | same |
| HEA § 484(a)(1) | "be enrolled or accepted for enrollment in a degree, certificate, or other program (including a program of study abroad approved for credit by the eligible institution at which such student is enrolled) **leading to a recognized educational credential** at an institution of higher education that is an **eligible institution** in accordance with the provisions of section 1094 of this title, except as provided in subsections (b)(3) and (b)(4), and not be enrolled in an elementary or secondary school" | 20 U.S.C. § 1091(a)(1), **current text**, fetched verbatim 2026-09-14 |
| 26 CFR § 1.221-1(e)(3)(i)(B) | paraphrases the cross-reference as "requiring that the student be a **degree candidate** carrying at least half the normal full-time workload" | regulation |

This closes a gap in the retained evidence, which characterised HEA
§ 484(a)(1) as an institutional-eligibility requirement but never quoted it.
The text is **conjunctive**: a credential-bearing *program* requirement **and**
an eligible-*institution* requirement. The selected ordinary fact is the
lay-observable part of the program half. Note that "enrolled **or accepted for
enrollment**" is the statute's own disjunction, which is why the ordinary
question offers both.

### 2.3 OV-1 — the incorporated 1997 text — **CLOSED**

§ 25A(b)(3)(A) pins § 484(a)(1) **as in effect 5 August 1997**. P0 originally
verified only the current text and flagged the gap. The independent review
closed it, and the closure was reconfirmed directly.

`authority`. The **1994 US Code Main Edition** text of 20 U.S.C. § 1091(a)(1) is
**identical to the current text**, including "leading to a recognized
educational credential at an institution of higher education that is an eligible
institution in accordance with the provisions of section 1094" and the trailing
clause "and not be enrolled in an elementary or secondary school". The amendment
history shows the last change to (a)(1) before 1997 was **Pub. L. 102-325**
(1992, inserting the study-abroad parenthetical); the elementary/secondary clause
was added by **Pub. L. 102-26** (1991). No public law touched (a)(1) between 1992
and 1998.

Therefore the text incorporated as of 5 August 1997 is the text quoted in § 2.2,
and the credential-program core is stable. **OV-1 is closed.** The earlier
caution that the elementary/secondary clause was "undated and may not be relied
on" is withdrawn — it is in the incorporated text.

**The standing constraint survives OV-1's closure:** no *other* frozen-version
predicate may be inferred from a current text without dating it. § 25A(b)(3)(A)
freezes one cross-reference; nothing else in this milestone's authority chain is
frozen, and § 25A(b)(3)(B) is read as currently in force.

### 2.4 Why the pair is comprehensible, and deliberately asymmetric

The question asks what the student was *enrolled in*, which the person lived
through and can describe. It does not ask them to classify a credential under
the Higher Education Act, to know whether their school participates in federal
aid under HEA § 1094, or to know what workload their school treats as
full-time.

Because § 25A(b)(3) conjoins (A) with (B), and § 484(a)(1) itself conjoins the
program requirement with the institution requirement, the selected fact does
not behave the same way in both directions.

**Adverse answer — free of X1, X2 and X3.** `individual-classes-only` fails the
program half of (A). A conjunction with a failed conjunct fails whatever the
other conjuncts are. So the determination needs **no credential-recognition
row, no institutional-eligibility row, and no institution-certified half-time
threshold**.

It is **not free of every premise.** It still depends on:

- **X5a** — that this statement's box-1 amount is interest on one identified
  loan; and
- **X5b** — that the loan's proceeds paid for education furnished during exactly
  the one named academic period the ordinary fact describes;

together with X4 (the student is the tax-return filer) and X6 (other constituents held
constant). Without X5a and X5b the adverse fact is about a term that has not
been connected to the interest being deducted.

**Favorable answer — additionally needs X1, X2 and X3.**
`credential-program` establishes only the lay-observable part of (A). Eligible
student status still needs credential recognition, institution eligibility under
HEA § 1094, and the (B) half-time comparison. A favorable result is therefore
honest only as *"supported favorable as to the student's enrollment in a
credential program, with X1–X3 stipulated"* — never as eligible-student status
established.

The plan permits replacing this fact if it "cannot produce an honest bounded
positive and negative pair." **It is not replaced.** The pair is honest; it is
asymmetric, and P0 states the asymmetry instead of hiding it.

### 2.5 Runner-up, and why the selection stands

The only serious alternative is the (B) half-time predicate (course load
against the institution's threshold). It is **worse** for this milestone:

| | Credential-program fact (selected) | Half-time fact (rejected) |
| --- | --- | --- |
| Honest **adverse** result needs | X4, X5a, X5b, X6 | those **plus** X3, the institution-certified threshold |
| Honest **favorable** result needs | additionally X1, X2, X3 | additionally X1, X2 anyway |
| Ordinary comprehensibility | the student's own enrollment | requires knowing an institution-defined norm the user does not set |

The half-time predicate cannot avoid X3 in **either** direction. The selected
fact avoids X1–X3 in the adverse direction, which is what makes the executable
comparison of § 6 cheap enough to isolate the mechanism under test.

---

## 3. Documentary support and the three routes

### 3.0 There is no document-only baseline in production today

`read`, verified directly at this base. Three things must not be conflated.

| | What it is | Status |
| --- | --- | --- |
| **(a) Form 1098-E alone** | The reported amount and the issuer's reporting treatment | **Does not satisfy the current nonempty worksheet dependencies.** It is not a calculable baseline |
| **(b) The incumbent calculation baseline** | Form 1098-E box-1 amounts **plus** the contributed qualification witnesses **plus** every other required worksheet input | **This is the real control P1 must execute** |
| **(c) A proposed document-reliance route** | A possible product policy that would proceed on the document within a declared reliance boundary | **Not adopted by P0 and not implemented in production.** P1/P2 may evaluate it |

`read`. The committed `tax.us.2025.rule.sli-worksheet` artifact declares **29
pins**: **26** with role `input` and **3** parameter pins. Among the 26
input-role pins:

- **two are upstream derived findings** —
  `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal` (the
  closure-authorized sum of Form 1098-E box-1 members) and
  `tax.us.2025.income.total-income`;
- **twenty-four are direct determinable inputs** — the **five Form 1098-E
  qualification witnesses** (`no-related-person-interest`,
  `no-qualified-employer-plan-interest`, `no-non-qualified-loan-component`,
  `no-employer-educational-assistance-interest`, `no-qtp-earnings-used`, read via
  `collect_categorical_all_equal`); **three `sli-scope` facts**
  (`no-form-2555`, `no-form-4563`, `no-puerto-rico-or-samoa-income`); **twelve
  `schedule1-adjustments-scope` absence facts** (lines 11–20, 23, 25);
  **`not-claimed-as-dependent`**; **`legally-obligated-for-interest`**;
  **`filing_status`**; and **`rounding.convention`**.

`require_closed` additionally reads the Form 1098-E family's **closure state**,
and the three adopted parameters supply the cap and phaseout values.

**The declared pin table is not a provenance claim.** The static rule-artifact
field `origin: assertion` says how a pin is declared, **not** that the runtime
input was contributed directly. `tax.us.2025.income.total-income` is the clear
case: its pin carries `origin: assertion`, yet it is a **derived publication** of
`tax.us.2025.rule.form1040-line9` with its own upstream provenance. An earlier
round of this charter read the pin table as a provenance census and reported "one
document-derived input plus 25 contributed assertions." That count is withdrawn.

**The durable conclusion, stated simply.** The current nonempty worksheet is **not
document-only**. It depends on the Form 1098-E-derived subtotal, **24 direct
determinable inputs**, the **derived total-income finding**, **family closure**,
and **three parameters**.

The five qualification witnesses are **contributed determinable findings, not
document fields** — a `"no"` on any of them blocks
`SLI_UNIVERSAL_COMPONENT_VIOLATION`. So the incumbent route has *never* computed
from the form alone, and **the absence of the newly selected credential-program
fact does not mean a documentary baseline "automatically applies."** There is no
such baseline to fall back to. Earlier rounds called M0 the "documentary
baseline"; that name was wrong and is withdrawn.

### 3.1 What Form 1098-E's reporting test actually is

`authority`. The reporting test in the Instructions for Forms 1098-E and 1098-T
is **not** § 221(d)(1). For reporting purposes a student loan must be either

> "Subsidized, guaranteed, financed, or otherwise treated as a student loan
> under a program of the federal, state, or local government, or of a
> postsecondary educational institution; or Certified **by the borrower** as a
> student loan incurred solely to pay qualified higher education expenses."

and the form is filed by anyone who "receives student loan interest of $600 or
more from an individual during the year in the course of [their] trade or
business."

The test is a **disjunction of permitted reporting bases**:

- **Programmatic basis.** The loan was treated as a student loan under a
  governmental or postsecondary-institution program — upstream institutional or
  governmental treatment, obtained by someone other than the taxpayer.
- **Borrower-certification basis.** The loan was certified by the borrower
  (optionally on Form W-9S) as incurred solely to pay qualified higher education
  expenses — the taxpayer's own assertion.

And for **revolving accounts** resting on such a certification the instructions
say expressly:

> "You do not have to verify the borrower's actual use of the funds."

That is not a silence to be worked around. It is an affirmative statement that at
least one permitted basis may rest on borrower certification **without lender
verification of actual use** — the very thing a reader might assume the form
confirms.

**But the form identifies neither basis, and a statement is not a single-basis
object.** Two facts compound here:

1. Nothing on the statement discloses the issuer's basis. Box 1 is an amount.
2. One statement may aggregate **several loans** (§ 5.0), which may have been
   classified on **different** bases.

So it is ill-formed to describe a whole statement as "originating on" the
programmatic route or the certification route. P0 previously did exactly that,
and withdraws it.

`read` at this base is consistent: `tax.us.2025.f1098e.box1-student-loan-interest`
is an amount on one identified statement, and every qualification witness in
`packages/content/tax/2025/f1098e.bundle.json` is a *contributed categorical
assertion* by the tax-return filer, not a document field.

### 3.2 Finding D1 — the bounded conclusion

**D1**, in four bounded parts:

1. The form establishes that **its issuer (the reporting filer) treated the
   reported interest as reportable under one or more permitted reporting bases**.
2. The form **alone neither identifies those bases nor establishes
   § 221(d)(1)(C)**, and its reporting test is not the complete § 221 deduction
   test.
3. The **revolving-account instruction proves** that at least one permitted basis
   may rest on **borrower certification without lender verification of actual
   use**.
4. A product **may vary reliance by reporting basis only if additional, properly
   scoped evidence identifies that basis for the relevant loan or amount** — not
   the statement as a whole, since one statement may aggregate loans classified
   differently.

Whether documentary reliance is practically useful therefore turns on evidence
P0 does not have and on a reliance policy the product has not declared.

What D1 does **not** say, and earlier drafts wrongly did:

- It does **not** say the form represents nothing about (C). Insufficiency is
  not unavailability.
- It does **not** say documentary evidence is categorically unavailable for this
  constituent. Where **additional, properly scoped evidence** establishes that a
  relevant amount was classified on the programmatic basis, that is genuine
  upstream evidence of the loan's character; how far it reaches (C) specifically is
  open. The qualifier is essential — the classification attaches to a loan or
  amount, never to a whole statement by assumption.
- It does **not** generalise about **issuer duties** beyond the text actually
  found. The non-verification statement is scoped to **revolving accounts** on the
  certification basis (§ 3.1). P0 found no statement about what an issuer must
  determine on the **programmatic** basis, and makes no claim there. That gap is
  absence of found text, not proof of absence.
- It does **not** license inferring a basis from the form. **P1 may investigate
  practical documentary reliance, but must not manufacture route provenance from
  the form itself.**

### 3.3 The adverse ordinary fact does not contradict the document

This correction matters beyond wording. A lender can **correctly** report
interest received under the information-reporting rule while the **deduction**
fails a separate § 221 condition. Both statements are true at once: the borrower
paid the interest the lender reported, *and* the education that interest
financed was not furnished while the borrower was an eligible student.

So the route formerly called "contradiction-triggered" is renamed
**qualification-rebutting (adverse ordinary evidence)**. The distinction to
hold:

| | What it is | Where it applies here |
| --- | --- | --- |
| **Contradiction of a source claim** | Two claims about the same proposition point different ways; one must be wrong | Not what the selected adverse fact does |
| **Evidence defeating a separate tax inference** | Both claims stand; an additional fact prevents a downstream conclusion that would otherwise be drawn | Exactly what the selected adverse fact does |

**M4 is retargeted accordingly.** M4 must show that the Form 1098-E report
**remains accurate and unaltered** while the additional ordinary fact prevents
the deduction conclusion. It is not a test that one source overrode another.
A genuine same-proposition contradiction remains a distinct case and is not
what M4 exercises.

### 3.4 The routes, and what each can establish here

| Route | What it relies on | What it can establish for the selected fact | Evidence ceiling | Cases |
| --- | --- | --- | --- | --- |
| **1. Document-reliance (proposed, not adopted)** | An uncontradicted Form 1098-E, relied on operationally within a **declared** bounded reliance policy | The **amount**, the statement's identity, and that the issuer treated the interest as reportable under one or more permitted bases. Bounded positive support for (C) is **open** (D1) | **Not implemented in production and not adopted by P0** (§ 3.0c). Insufficient alone for (C); does not by itself satisfy the incumbent worksheet dependencies. **May not infer which basis applied from the form**, and may not treat a statement as a single-basis object | evaluated against M0, not equal to it |
| **2. Qualification-rebutting (adverse ordinary evidence)** | An ordinary fact that defeats a § 221 condition while leaving the document accurate | That the nominee method transfers to a rule-owned intermediate tax concept, **avoiding X1–X3** (§ 2.4) | Establishes the adverse direction only. Says nothing about the favorable direction. Depends on X5a/X5b | M2, M4; M3 with route 3 |
| **3. Constituent-derived** | Enough independently scoped facts to evaluate the legal definition directly | Eligible-student status proper, favorable or adverse | Requires X1–X3 to have real evidence routes. Not presumed necessary and not presumed available | M1 |

The three routes are not ranked, and route 1 is not written off. P1 must
determine whether documentary provenance provides any bounded positive support
(§ 11).

---

## 4. Experimental premises

Every premise the bounded case stipulates. `ok` under **Prototype** means P1 may
assert it in a disposable fixture to isolate the behaviour under test.

| # | Premise | Prototype | Production | Why |
| --- | --- | --- | --- | --- |
| **X1** | The named program leads to a **recognized educational credential** | ok — inject and label | **blocks** | No authoritative producer and no adopted categorical-parameter mechanism. `read`/`eval`: `op == "parameter"` returns `_as_decimal(...)` on both branches, so a `{recognized-credential, not-recognized}` catalog is not evaluable; encoding it as `1`/`0` would hide a determination in a number |
| **X2** | The named school is an **eligible institution** under HEA § 1094 | ok — inject and label | **blocks** | Same gap. The probe injects this as a symbol; `fact-type.v2` declares vocabulary and supplies no current finding |
| **X3** | The institution-certified **half-time threshold** for that program and period, compared directly with course load | ok — inject and label | **blocks** | A numeric adopted parameter is evaluable, but only keyed on **one** application-resolved standard id. No composite-key operator exists, so institution + program + period cannot be separate key expressions |
| **X4** | The **student is the tax-return filer** | ok | **bounds** | No person ontology. A parent-borrower would mis-key enrollment. Out-of-class cases are refused, not modeled |
| **X5a** | This statement's **box 1 is entirely interest on one identified loan** | ok | **obligation — blocker unless P1 finds a route** | No committed production path records this relationship. See § 4.1 |
| **X5b** | That loan's **proceeds paid for education furnished during exactly the one named academic period** the ordinary fact describes | ok | **obligation — blocker unless P1 finds a route** | Same. This is the link that makes a student-period fact bear on this interest at all (§ 2.1) |
| **X6** | The remaining § 221(d)(1) constituents, § 221(e)(1), and § 221(c) are held constant by the fixture | ok | **bounds** | Each stays on its own committed handle or unresolved. A published result from this route is qualified *as to (C) only* |

### 4.1 X5 is a production obligation, not a harmless bound

Earlier drafts classified X5 as a mere boundary. That was wrong, and the reason
is worth stating plainly:

- The bounded result — in **both** directions — depends on an accountable
  **statement-to-loan-and-period relationship**. Without it, the ordinary fact
  describes a term with no established connection to the interest claimed.
- **X5a stipulates away a choice the issuer is expressly permitted to make.** The
  instructions allow one Form 1098-E per loan *or* one covering all of a
  borrower's loans, and the form does not disclose which (§ 5.0). So "box 1 is
  entirely interest on one identified loan" is not a mild narrowing of an unusual
  case; it assumes away an ordinary, permitted filing pattern. This is why X5
  bears on the evaluation-subject question as directly as M6 does.
- `read` at this base: **no committed production path records that
  relationship.** The retained design proposes a statement-scoped association
  assertion; that is a starting hypothesis, not a committed contract.
- **Refusing multi-loan and multi-period cases does not create support for the
  asserted single-loan case.** Refusal disposes of the classes the route does
  not cover. It supplies no evidence for the class the route *does* cover. These
  are different obligations, and conflating them is how a stipulated premise
  becomes silent production authority.

So X5a/X5b sit with X1–X3 as things P1 and P2 must either supply an honest route
for or carry explicitly into the production decision.

### 4.2 Which premises each direction needs

| | X1 | X2 | X3 | X4 | X5a | X5b | X6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Adverse (`individual-classes-only`) | — | — | — | yes | yes | yes | yes |
| Favorable (`credential-program`) | yes | yes | yes | yes | yes | yes | yes |

No result in this milestone is free of every premise. The adverse direction is
free of **X1–X3**, and that is the precise claim.

---

## 5. Do M0–M9 require Identified Evaluation Context?

**Determination: undetermined. Evaluation Context is neither shown to be
required nor shown to be avoidable, and P0 does not name a single deciding case.**

Two successive framings have now been withdrawn:

- **Round 1** answered "no", on the basis that M6 is refused by existing tested
  cardinality machinery. That basis was false (§ 5.2).
- **Round 2** answered "open, and M6 alone decides it." That was also wrong
  (§ 5.3). M6 is an important discriminator but not the sole deciding case, and
  per-statement execution does not by itself meet the reopening trigger.

### 5.0 Why no single case decides this

`authority`. The Form 1098-E statement **is** a stable unit — of the document, of
evidence, of identity, of amount reporting, and of provenance. What it is **not**
is a reliable proxy for exactly one loan, exactly one academic period, or exactly
one reporting basis. The instructions leave the reporting unit to the issuer's
choice:

> "However, you may file a separate Form 1098-E for each student loan of the
> borrower, or you may file one Form 1098-E for the interest from all student
> loans of the borrower."

> "The $600 threshold applies to each borrower regardless of the number of
> student loans obtained by that borrower."

So two statements may be two loans or two issuers' aggregates, and one statement
may be one loan or all of a borrower's loans — **and the form does not say which.**
Statement identity remains sound and usable; **loan identity does not follow from
it.** Consequences:

- **M7 is not an exotic edge case.** One statement representing several loans is
  a permitted, ordinary filing choice. It bears on the required evaluation
  subject exactly as directly as M6 does.
- **X5a/X5b are not mild stipulations.** X5a stipulates away a choice the lender
  is expressly permitted to make either way. The statement-to-loan-and-period
  relationship (§ 4.1) is therefore a first-class part of this question, not a
  side condition.
- **Statement-level evaluation does not solve loan-level attribution.** Evaluating
  per statement leaves M7 exactly where it was.

**The reopening trigger has three conjuncts, not one.** It requires a route that
(i) needs per-subject constituent evaluation, (ii) **cannot rely honestly on a
document or a bounded specialized mechanism**, and (iii) has an observable error
if one subject is omitted. Establishing (i) and (iii) does **not** meet it.
Conjunct (ii) is untested: P1 has not tried a bounded relationship or specialized
mechanism and found it insufficient.

So per-statement execution would establish a need for **separately attributable
evaluation** — not a need for a general Evaluation Context.

### 5.0a Division of labour between the gates

| Gate | Responsibility |
| --- | --- |
| **P1** | **Observe and report.** Whether uniform/unkeyed handling produces an **observable error**; whether a **bounded relationship or specialized mechanism** can carry the identified subjects; the candidate costs of each. P1 reports observations, not a product boundary |
| **P2 / Track 0** | **Recommend the product boundary**, weighing those observations against scope, honesty, and cost |

**A run cannot choose product policy by itself.** An executed case can show that
uniform handling is wrong; it cannot decide how wide a mechanism the product
should adopt in response. P1 must not present an execution result as a boundary
decision, and P2 must not treat P1's observations as having already made one.

### 5.1 Case by case: what is settled, and what is open

The single-subject cases are settled. M6 and M7 are not, and are marked so.

| Case | Subjects | Mechanism that carries it at this base | Needs per-subject enumeration? |
| --- | --- | --- | --- |
| M0 incumbent calculation baseline | 1 statement | Existing worksheet route: `count > 0` gate, **family closure** via `require_closed`, the **Form 1098-E-derived box-1 subtotal**, **24 direct determinable inputs**, the **derived total-income finding**, and **three parameters** (§ 3.0). Not a document-only path | No |
| M1 favorable | 1 | `ref` + `categorical_compare` on one current finding. `read`/`eval`: `ref` reads one scalar from `env.symbols`, absent → `DEPENDENCY_ABSENT` | No |
| M2 adverse | 1 | Same read; `choose` selects the adverse branch | No |
| M3 missing support | 1 | `ref` on an unbound symbol → `DEPENDENCY_ABSENT`; never silently favorable | No |
| M4 document accurate, deduction defeated | 1 | A `choose` on the ordinary fact that withholds the deduction conclusion while the box-1 report is untouched. **Not** a source-contradiction block (§ 3.3) | No |
| M5 correction / retraction | 1 | `compute_currency`; correction is a new assertion at the same `fact_id`, retraction is `finding-retracted`, reassertion is a new finding | No |
| M6 several statements | 2+ statements | **Undetermined — see § 5.2, § 5.3.** No cardinality refusal exists for this family, and the current route deliberately aggregates multiple statements | Open — a discriminator, not the sole decider |
| M7 one statement, several loans | 1 statement, 2+ loans | **Undetermined, and material.** A permitted ordinary filing choice (§ 5.0), not an edge case. `count` is 1, so no cardinality test could reach it; it turns on X5a/X5b | Open — bears on the evaluation subject as directly as M6 |
| M8 worksheet compatibility | 1 | Existing cap, phaseout, Schedule 1 line 21/26, AGI cascade, unchanged | No |
| M9 provenance | 1 | Existing pins, dispositions, durable output | No |

### 5.2 What was wrong, and what the Form 1098-E machinery actually does

`read`, verified directly at this base:

- **`MULTIPLE_F1098_OUT_OF_SCOPE` is not this form's machinery.**
  `rule.schedule-a-line8a.json` governs **Form 1098 — mortgage interest** — a
  different information return, reaching Schedule A line 8a. Round 1 cited it as
  though it carried M6. It does not, and the charter failed to disclose that it
  belongs to another form. It is at most a **shape** precedent: proof that the
  corpus can express a singleton-class cardinality refusal with an adopted block
  code.
- **No cardinality refusal exists for `tax.us.2025.f1098e.1`.** The only `count`
  comparisons on that family in `rule.sli-worksheet.json` are `count == 0` (the
  closed-empty shortcut) and `count > 0` (route selection). There is no
  `count > 1` anywhere, and no `MULTIPLE_*` code for this family in the record
  vocabulary.
- **The current Form 1098-E route aggregates multiple statements by deliberate
  design.** Track 6b moved the five per-statement witnesses from unkeyed `ref`
  to `collect_categorical_all_equal` *precisely so that multi-statement returns
  keep working*: the rule's own notes state that a plain `ref` there "would
  wrongly block `DEPENDENCY_ABSENT` on every legitimate multi-statement return."
  Multi-statement support is a repaired, intended property of this route, not an
  accident.

**The consequence is not cosmetic.** Refusing M6 would **narrow currently
supported behaviour** — it would take away something a multi-statement tax-return filer can
do today — rather than reuse machinery already in place. "M6 is refused" was not a
free move, and it cannot be assumed.

**A genuinely useful datum for P1.** The corpus holds **both postures** on
adjacent information returns: Form 1098 (mortgage) *refuses* multiple statements
as out of class; Form 1098-E *aggregates* them. Neither is the house style. P1
must choose and justify, not inherit.

### 5.3 What P1 must test, and the three honest evidence states

P0 does not choose a disposition. It fixes **what must be observed** and **which
outcomes are never acceptable**.

**P1's two observations:**

1. **Does uniform/unkeyed handling produce an observable error?** Construct a case
   where two statements (or one statement covering two loans) carry different
   ordinary circumstances, evaluate it through the current uniform route, and
   record whether the published deduction is wrong — and if so, how the error
   presents.
2. **Can a bounded relationship or specialized mechanism carry the identified
   subjects?** Try one. Report whether it works, what it costs, and what it
   cannot reach. This is the untested conjunct (ii) of the reopening trigger
   (§ 5.0), and without it no claim about Evaluation Context is available.

P1 reports these observations and the candidate costs. **P2 or Track 0 recommends
the product boundary.**

#### The three evidence states, and the required disposition of each

This replaces the earlier disposition list. The first entry of that list —
*"declare the route applicable only to single-statement returns, leaving the
existing aggregate route untouched for everyone else"* — is **withdrawn as
unsafe**, for the reason given below.

| State | What is true | Required disposition |
| --- | --- | --- |
| **A. No relevant ordinary evidence in the selected route** | No current finding of the selected ordinary fact bears on any statement on the return | **Measure the incumbent result and name every support it actually uses** (§ 3.0) — it is not a document-only path. If the selected route *requires* the new ordinary fact and it is absent, **that route is unresolved or blocked**. A document-only path is available only if a later reviewed reliance policy affirmatively adopts it |
| **B. Relevant evidence exists and can be attributed honestly** | An ordinary fact bears on identified interest, and the statement-to-loan-and-period relationship is established | Attribute it and let the rule own the consequence for that interest |
| **C. Relevant evidence exists but cannot be attributed** | An ordinary fact is current and relevant, but which interest it bears on cannot be established | The dependent deduction **blocks or refuses**. It must **never** fall back silently to the old aggregate result |

**Why the withdrawn disposition was unsafe.** Routing multi-statement returns to
the untouched aggregate path is state C wearing state A's clothes. If a current
adverse ordinary fact is known but cannot be attributed, continuing to publish the
old aggregate deduction **ignores relevant evidence the product already holds**.
That is not a bounded scope limit; it is a wrong answer produced by a routing
decision. State C must block or refuse.

**Absence is not favorable.** Do not infer favorable eligibility from the absence
of the selected ordinary fact. State A is the incumbent calculation over its own
26 inputs; it is not a finding that the student was an eligible student, and it is
not a document-only reliance. This is the same rule as M3, applied at the routing
layer.

**No reader-facing reliance label is required of P1.** The prototype findings must
describe the reliance basis **accurately** — naming which supports each measured
result actually used. Whether production surfaces a reliance label to a reader is a
later question and is out of scope here (§ 11).

**Consistency note, applying § 4.1.** Refusal supplies no support for the class a
route does cover. That constrains this section too: P0 may not lean on a refusal
of M6/M7 to establish that per-subject evaluation is unnecessary — which is what
round 1 did. The corrected position leans on nothing; it records what must be
observed.

### 5.3a What P1 may and may not claim for M7

`read`: **current production has no represented loan decomposition inside an
aggregated Form 1098-E.** There is no loan entity, no per-loan amount, and no
statement-to-loan relationship in committed content.

P1 **may**:

- execute the **current aggregate behaviour** and record what it produces;
- **demonstrate that the current model cannot express loan-differentiated
  circumstances** — a negative result about the committed model, which is a real
  finding; and
- **test a disposable bounded relationship or specialized overlay** to see whether
  one could carry the identified subjects.

P1 **must not**:

- describe a result built on **synthetic loan identities or hand-authored
  relationships** as current production execution. Such a result is **`local` /
  prototype evidence** and must be labelled so;
- present a working overlay as evidence that the bounded mechanism **has a
  production route** — that is X5's open obligation (§ 4.1, V14), not something an
  overlay discharges; or
- claim that statement-level evaluation solves loan-level attribution.

This is the same ceiling discipline the retained probe carries (§ 8): a real
evaluator inside a hand-built environment proves mechanics, not availability.

### 5.4 Why the retained probe's failure is still not proof of the opposite

 The retained probe's
negative result is about `evaluate_pairing_scoped_rule`, which iterates the
*pairing* population (`pairing_sources = [s for s in sources if s.name ==
pairing_type]`, `packages/derivation/pairing_dispatch.py:129`), so an
unassociated statement is never a loop iteration. That is a true finding about
**that dispatcher on a multi-statement fixture**. The selected route neither
uses that dispatcher nor presents it with two statements to account for. The
plan's own caution applies — the probe "is not evidence that the product must
perform the decomposition."

**What P1 must do here.** Execute M6 **and** M7, make the two observations of
§ 5.3, and report them with costs — without selecting the product boundary.
`read`-level confirmation that a refusal *shape* is expressible in the corpus is
not confirmation that this route may use it, that it is honest, or that it reaches
the reader. Equally, observing that uniform handling errs is not a finding that a
general Evaluation Context is required: conjunct (ii) of the trigger must be
tested against a bounded mechanism first.

**Verified supporting mechanism.** `read`/`eval` at this base: the closed
operator set is `add, all, any, block, bound_sources, bracket_fold,
categorical_compare, category_literal, choose, collect,
collect_categorical_all_equal, compare, conditional_dependency_set, count,
divide, max, multiply, not, parameter, range_lookup, ref, require_closed,
round, subtract`. Every mechanism named above is in that set. No new operator is
implied by any fixed case.

**Multi-match honesty, for the record.** `read`: an unkeyed symbol matching two
or more current findings binds when they agree and, when they **disagree**, is
left unbound so the runner produces an ordinary blocked disposition rather than
an order-dependent pick. So even the multi-statement case fails closed rather
than silently answering from whichever finding sorted first.

---

## 6. The smallest executable comparison P1 can use

**Corrected 2026-09-15.** This section previously specified "two runs of one
fixture differing in exactly one ordinary statement" — an incumbent Run A against
a Run B carrying the selected ordinary fact. **That comparison was confounded**:
the selected ordinary fact has no production vocabulary, so Run B necessarily
carries a new package, bundle, fact type, binding path, rule, publication and
consumer. It cannot establish that the ordinary statement was the sole cause of a
changed result.

**The corrected design: three controlled cases on one identical disposable
graph**, with every artifact, binding path, publication and consumer held
constant, and X1–X3 and every other premise held constant between B1 and B2:

| Case | Selected ordinary fact |
| --- | --- |
| **B0** | absent |
| **B1** | present, adverse |
| **B2** | present, favorable |

| Comparison | Kind | Establishes |
| --- | --- | --- |
| **A vs B** | **behavioral** | Incumbent versus proposed behavior. **Not causal** |
| **B0 vs B1** | controlled | Missing support versus supported adverse treatment |
| **B1 vs B2** | **causal, single-variable** | Whether the ordinary statement changes the rule-owned consequence |

**Run A is retained only as the incumbent behavioral baseline** — the full
incumbent calculation of § 3.0b, not a document-only baseline, with every required
current input present and satisfied. No "sole cause" or "only candidate
explanation" claim attaches to it.

**And P1 must measure, not predict.** The findings must name the supports each run
actually used **as observed in the runtime and durable pins**, not as inferred from
a rule artifact's declared pin table. `origin: assertion` there is a declaration
shape, not evidence that a runtime input was contributed directly — `total-income`
is a derived publication despite carrying it (§ 3.0).

**Why the adverse direction still leads.** It is the only direction that avoids
X1–X3 (§ 2.4), so B0/B1 discriminate without stipulating the three catalog
premises. B2 adds them, labelled, to exhibit the asymmetry.

Required additions before P1 closes, in this order:

1. **M3 (missing support)** — the selected fact absent while the route requires
   it must be unresolved, never favorable.
2. **M1 (favorable)** — **kept.** X1–X3 are injected into the disposable
   fixture and **labelled in the prototype case and in the findings**. Its value
   is precisely that it exhibits the asymmetry of § 2.4 against Run B.
3. **M4** — the document remains accurate and unaltered while the ordinary fact
   prevents the deduction conclusion (§ 3.3).
4. **M5 (correction / retraction / reassertion)** — each run uses current
   support only.
5. **M6 and M7**, both executed rather than assumed. Make the two observations of
   § 5.3 — whether uniform/unkeyed handling produces an observable error, and
   whether a bounded relationship or specialized mechanism can carry the
   identified subjects — and report them with candidate costs. **Do not select the
   product boundary**; that is P2's or Track 0's (§ 5.0a). Note that no refusal
   machinery exists for this family today and that the route currently aggregates
   multiple statements, so "refuse" is a change, not a reuse. M7 is material in its
   own right: one statement may represent several loans, and statement-level
   evaluation does not solve loan-level attribution.
6. **The negative control the plan requires** — a user-supplied "I was an
   eligible student" assertion must be demonstrably the **wrong input**, not a
   shortcut that happens to work.

**Where the labels live.** X1–X3 are labelled **in the prototype fixture and
the P1 findings**, at the `local` level. P1 must **not** require the durable
product output, the presentation model, or any form-field explain to acquire a
new assumption-explanation carrier in order to run. Adding a
production-facing assumption label or explanation feature is outside P1.

**Boundary to enter.** The cheapest boundary that can observe the distinction,
and no cheaper: the distinction is a *disposition* change, so `eval` alone is
insufficient and `presentation` is more than needed. P1's report must label
every observation with its level and must not describe a `local` hand-built
environment result as a `run` result. That confusion is precisely what the
retained probe's ceilings exist to prevent.

---

## 7. Claim-to-verification matrix

| # | Claim | Level reached at P0 | Level P1 must reach | Ceiling — what it does not establish |
| --- | --- | --- | --- | --- |
| V1 | § 221(d)(1)(C) → § 221(d)(3) → § 25A(b)(3)(A) → HEA § 484(a)(1) is the authority chain, and § 484(a)(1) is conjunctive (credential program **and** eligible institution) | `authority`, verbatim, **both the current text and the text incorporated as of 5 August 1997** (1994 Main Edition; no amendment to (a)(1) between 1992 and 1998) | — | Nothing about the other five constituents. **OV-1 is closed** (§ 2.3) |
| V2 | The ordinary fact's subject is the **student at an identified academic period**, with a program relationship — **not** the indebtedness, the statement, or the tax year. The loan rule reaches it through the proceeds → education → period relation | `authority` | — | Does not supply the relation itself; that is X5a/X5b |
| V3 | The adverse answer disqualifies **without X1, X2 or X3**, while still depending on X4, X5a, X5b and X6 | `authority` (conjunction logic) | `run` | Not a claim that the adverse route is free of every premise |
| V4 | Form 1098-E establishes only that its **issuer** treated the interest as reportable under **one or more permitted bases**; it identifies no basis and establishes no § 221(d)(1) predicate. At least one permitted basis rests on borrower certification without lender verification of actual use. A statement may aggregate loans classified on different bases | `authority` (instructions, quoted) + `read` | — | Does **not** establish the form is unavailable as support. Says nothing about issuer duties on the **programmatic** basis. **Licenses no inference of basis from the form** (D1 part 4) |
| V5 | X1 and X2 are not evaluable as adopted parameters at this base | `read`/`eval` | re-`read` at P1 start | Does not prove no mechanism could exist |
| V6 | X3 is evaluable only keyed on one opaque standard id; no composite-key operator exists | `read`/`eval` | re-`read` | Does not establish that such an id has a producer |
| V7 | A `count > 1` singleton-class refusal with an adopted block code exists in the corpus for **Form 1098 (mortgage interest)** — a *different* information return. **No such refusal exists for the Form 1098-E family**, whose route deliberately aggregates multiple statements | `read`, verified | `run` if a refusal is chosen | A **shape** precedent only. Does not establish that this route may refuse, that refusing is honest, or that it reaches the reader. Refusing would narrow current behaviour |
| V8 | M4's shape is an ordinary `choose` that withholds the deduction conclusion while leaving the report intact — not a source-contradiction block | `read` | `run` | Does not establish the M4 result is the right one for this case |
| V9 | `ref` binds one current value per symbol; absence blocks; disagreement among multiple matches leaves it unbound rather than picking one | `read`/`eval` | `run` | Does not establish per-statement pairing for a multi-statement route |
| V10 | The single-subject cases M0–M5, M8, M9 need no per-subject enumeration | `read`/`eval` | `run` | Says nothing about M6/M7 |
| V10a | **Whether the selected route needs separately attributable evaluation is open, and no single case decides it.** M6 *and* M7 both bear on it, because the Form 1098-E reporting unit is the issuer's choice (§ 5.0) | open question | **`run`** — execute M6 and M7; observe whether uniform/unkeyed handling errs, and whether a bounded relationship or specialized mechanism can carry the subjects | P0 establishes no answer. **Per-statement execution would establish a need for separate attribution, not a need for Evaluation Context**: trigger conjunct (ii) is untested |
| V10b | The reopening trigger's three conjuncts are independent, and conjunct (ii) — that neither a document nor a bounded specialized mechanism can carry it — is **untested** | `read` of the trigger + absence of any test | **`run`** — P1 must try a bounded mechanism | Establishing (i) and (iii) does not meet the trigger |
| V10c | **P1 reports observations and candidate costs; P2 or Track 0 recommends the product boundary.** A run cannot choose product policy by itself | method constraint | — | Not an empirical claim. Binding on how P1's results may be read |
| V11 | The retained probe's negative result reproduces at this base | `local`, executable | rerun if the base moves | Only about `evaluate_pairing_scoped_rule` on a multi-statement fixture. Not about the selected route |
| V12 | The incumbent compressed witness collapses four predicates into one `{yes, no}`, so no single constituent can be stated, corrected, or retracted independently | `read` | — | Does not authorise renaming or reinterpreting that witness |
| V13 | The two-run comparison of § 6 discriminates method transfer | design claim, unexecuted | **`run`** | Nothing until executed. A green result establishes transfer for the adverse direction only |
| V14 | **No committed production path records the X5a/X5b statement-to-loan-and-period relationship**, and refusing multi-loan cases supplies no support for the single-loan case | `read` | **`run`** or explicit carry into P2 | Does not establish that no honest route exists — only that none is committed |
| V15 | **There is no document-only baseline in production.** The nonempty worksheet depends on the Form 1098-E-derived subtotal, 24 direct determinable inputs, the derived total-income finding, family closure, and three parameters. The five Form 1098-E qualification witnesses are contributed determinable findings, not document fields | `read` of the artifact's 29 pins (26 `input`, 3 parameter) | `run` — Run A must execute the incumbent control with every required current input present, and report the supports **measured from runtime and durable pins**, never inferred from the declared pin table | Does not establish that a document-reliance policy is unavailable — only that none is implemented, and that absence of the selected fact does not make one apply. **The pin table is not a provenance census**: `origin: assertion` is a declaration shape, and `total-income` is derived despite carrying it |
| V16 | Current production has **no represented loan decomposition** inside an aggregated Form 1098-E | `read` | `local` for any overlay tested | A working overlay is prototype evidence of mechanics, **not** evidence that the mechanism has a production route |

Claims V3, V7, V8, V10a, V10b, V13, V14 and V15 are the ones P1 must actually
execute; V16 bounds what any M7 overlay result may be called.
**No single one of them decides the milestone's deferred question**: V10a and V10b
together supply the observations, and the boundary recommendation belongs to P2 or
Track 0 (V10c). V1, V2, V4, V10 and V12 are settled at P0 and are not reopened
absent new authority. OV-1 is closed (§ 2.3).

---

## 8. Negative control, reproduced at this base

`local`, executable. `docs/prototypes/sli-eligible-student/probes/feasibility.py`
run **unmodified** at this milestone's base: exit 0, `assertions_hold=True`. Section 5
reproduces byte-identically to its recorded result:

| Observation | Value |
| --- | --- |
| `dispatcher` | `evaluate_pairing_scoped_rule` |
| `dispatcher_publication_count` | 1 |
| `dispatcher_blocked_count` | **0** |
| `box1_members_without_association` | `["demo.fact.box1.b"]` |
| `would_block_aggregate` | true |

Statement B produces **neither a result nor a failure**. Section 6 also
reproduces: `production_producer_exists: false`,
`adopted_categorical_parameter_exists: false` — the `read`-level basis for X1
and X2.

Its ceilings are restated so no later gate overreads it: hand-built
environment, authored pins, conceptual (hand-computed) box-1 completeness,
partial `VALUE_EXPR` mechanics witness, **pin isolation not-proven**,
presentation a projection over synthetic rows. Verdict of record:
`needs-owner-decision`; obligations 2a and 2b undischarged.

**What it is evidence of, here.** That the *association-driven per-statement
decomposition* silently omits an unassociated statement. It is **not** evidence
that the product must perform that decomposition, that Form 1098-E proves or
disproves any predicate, or that a general context schema is required. It is
preserved as the original negative control and is not the selected product
route.

---

## 9. Reused evidence and its ceilings

Reused within the ceilings recorded in the retained-evidence README; the
ten-constituent survey is **not** repeated.

| Source | Reused for | Revalidated at this base |
| --- | --- | --- |
| `p1-loan-qualification.md` constituent 4 | The (C) tax boundary, scope, invalidators, and the compressed-witness finding | Authority re-read; HEA § 484(a)(1) newly quoted (§ 2.2), closing a gap in that record |
| `p1-loan-qualification.md` shared consumption path | Worksheet gates, the universal "all yes" fold, the block-withholds-line-21 cascade | Yes — `count`/`collect_categorical_all_equal` nodes and the `when` guard re-read in `rule.sli-worksheet.json` |
| `p2-*` observations | Locating consumers and comparison surfaces only | Only the claims relied on: `ref` semantics, marshal multi-match behaviour, evaluator operator set |
| `p3-partial-design.md` §§ 1.1–1.3, 2a, 2c | Requirements and rejected shapes as **starting hypotheses**; the three authority determinations; the composition-claim lifecycle | Current-machinery claims re-read: parameter decimal coercion, `categorical_compare` inputs, primitive binding table, `pairing_dispatch.py:129` |
| `sli-eligible-student` probe | The negative control only | Rerun at this milestone's base (§ 8) |

Nothing above is an accepted contract. No ADR, schema, content, package
version, or production code came out of the closed milestone.

---

## 10. Charges for independent review

The reviewer should attack these five specifically, before approving P1.

1. **The repaired documentary-support boundary (§ 3).** Is D1 now correctly
   bounded — insufficiency without over-negation? Does the two-route
   provenance account hold against the instructions? Is the absence-of-found-text
   limit on lender duties respected? Is any residual language still treating
   documentary evidence as categorically unavailable for (C)?
2. **The ordinary-fact subject (§ 2.1, V2).** Is the fact now correctly attached
   to the student and academic period rather than the indebtedness? Does any
   downstream identity statement still key it to the loan? Is the ordinary
   question free of legal classification — in particular, does it avoid asking
   the user whether a credential is "recognized"?
3. **The adverse case's dependency set (§ 2.4, § 4.2, V3).** Is "free of X1–X3"
   exactly right — no more, no less? Is any premise the adverse route actually
   needs missing from X4/X5a/X5b/X6? Does the conjunction argument hold, or has
   it been read too generously?
4. **The X5 classification (§ 4.1, V14).** Is X5a/X5b correctly treated as a
   production obligation rather than a bound? Is it true that no committed path
   records the relationship? Is the "refusal creates no support" point applied
   consistently wherever M6/M7 refusals are relied on — including in the § 5
   Evaluation Context determination?
5. **The 1997 incorporated text (OV-1, § 2.3).** Verify the version of HEA
   § 484(a)(1) in effect on 5 August 1997. Confirm or refute that the
   credential-program core is stable. Confirm that no other frozen-version
   predicate is inferred anywhere from the current text.

Secondary: is any claim promoted above its evidence level — a `read` claim
asserted as `run`, or a `local` probe result treated as production behaviour?
Has P0 predicted the production result anywhere (§ 11)?

A disputed premise here must not be carried into P1's design.

### Review outcome

The independent review is committed at
the independent P0 review. Charges 2
and 3 were approved outright. Charge 5 closed OV-1 more strongly than P0 had
claimed. Charges 1 and 4 returned **material** findings, both of which are
repaired above and recorded in § 0 round 2; the charge-4 finding changed a P0
conclusion rather than only its wording.

---

## 11. Out of scope for P0, and what remains undetermined

P0 draws no schema, ADR, package, contract, interface, prototype, or production
code, and touches nothing under `packages/`. It does not repeat the
ten-constituent survey, does not design an Evaluation Context, an institutional
catalog, or a relationship or query schema, and does not migrate or supersede
the accepted nominee-interest implementation. It does **not** require any new
assumption-labelling or explanation feature in the durable product output, and it
does **not** require a reader-facing reliance label — P1's findings must describe
the reliance basis accurately, but production presentation of it is a later
question. P0 also does **not** adopt a document-reliance route (§ 3.0c).

### P0 does not select a production result

Plan result 3 — a validated translation method with production deferred — is
**likely**, because X1, X2, X3, X5a and X5b all lack an evidence route at this
base. P0 does **not** establish it, and the production shape is **not** already
known. P0 also does not presume that the bounded route will refuse anything: it
records the three evidence states of § 5.3 and leaves the boundary to P2 or
Track 0.

P1 must still determine:

1. **what the adverse route actually proves** when executed;
2. **whether documentary provenance provides any bounded positive support**, and
   under what declared reliance policy;
3. **whether X5a/X5b can be represented honestly**, given that no committed path
   records the relationship and that refusal of multi-loan cases supplies no
   support for the single-loan case;
4. **whether the favorable route teaches anything beyond its stipulated
   fixture**; and
5. **whether the selected route needs separately attributable evaluation**, from
   executing **both** M6 and M7 — observing whether uniform/unkeyed handling
   produces an observable error, and whether a bounded relationship or specialized
   mechanism can carry the identified subjects (§ 5.3). P1 reports; **P2 or Track 0
   recommends the product boundary.** Per-statement execution alone would not meet
   the Evaluation Context reopening trigger, whose conjunct (ii) is untested.

### Owner decisions

None blocking. M1 is **kept** at owner direction, with X1–X3 injected and
labelled at the prototype layer (§ 6).

Independent review of P0 is authorized and is dispatched before P1.
