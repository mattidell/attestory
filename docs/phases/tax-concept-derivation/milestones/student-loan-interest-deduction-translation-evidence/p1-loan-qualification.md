# P1 tax boundary — loan qualification

The six § 221(d)(1) constituents: the chapeau's sole-purpose requirement, subparagraphs (A), (B), and (C), and the concluding sentence's related-person and qualified-employer-plan exclusions.

**Evidence level.** Committed artifacts, statute, and regulation only. This record establishes the tax boundary; it selects nothing and authorizes no implementation.

## Citation verification

Verified against 26 U.S.C. § 221(d)(1) as currently in force (LII text of 26 U.S.C. § 221):

- The chapeau of (d)(1) reads: the term “qualified education loan” means “any indebtedness incurred by the taxpayer solely to pay qualified higher education expenses—”
- Subparagraph (A) is the person-on-whose-behalf condition, determined “as of the time the indebtedness was incurred.”
- Subparagraph (B) is the reasonable-period-of-time condition.
- Subparagraph (C) is the eligible-student condition.
- Two sentences then sit in **flush language** after (A)–(C), not in a subparagraph. The first flush sentence includes refinancing of a qualified education loan. The second is the exclusion: the term “shall not include any indebtedness owed to a person who is related (within the meaning of section 267(b) or 707(b)(1)) to the taxpayer or to any person by reason of a loan under any qualified employer plan (as defined in section 72(p)(4)) or under any contract referred to in section 72(p)(5).”

P0’s placement of related-person and qualified-employer-plan exclusion in the concluding sentence of § 221(d)(1), following (A)–(C), is also correct. Constituent 4 is § 221(d)(1)(C), not that concluding sentence.

The first flush sentence (refinancing inclusion) is not among this unit’s six assigned constituents. It is recorded here only so the flush block is not treated as a single exclusion sentence.

Implementing regulation for the definition, used below where it supplies operative tests the statute leaves open: 26 CFR § 1.221-1(e)(3) (qualified education loan after December 31, 2001). Obligation rules at § 1.221-1(b)(1) and (b)(4) are not this unit’s constituents.

**Regulation examples verified 2026-09-13.** An independent reviewer fetched the
verbatim text of 26 CFR § 1.221-1(e)(4) and confirmed this file's
characterizations of Examples 3-6 are accurate: Example 3 (half-time graduate
student at an eligible institution; half-time is enough), Example 4 (90-day
disbursement timing), Example 5 (later loss of institutional eligibility does not
undo a loan already qualified for earlier terms), Example 6 (mixed-use
home-improvement plus spouse's education; disqualified for want of sole purpose).
The standing open verification item is closed.

## Discrepancies

These do not reopen P0; it is the factual baseline for this record.


2. **Committed title of `tax.us.2025.f1098e.no-non-qualified-loan-component` versus P0 F5.** The fact-type title in `packages/content/tax/2025/f1098e.bundle.json` (the object with `"id": "tax.us.2025.f1098e.no-non-qualified-loan-component"`) says the witness “collapses the student-status, qualified-education-expense, and reasonable-period-of-time sub-questions Pub. 970 (pp.30-31, …) gives no per-return signal to distinguish.” That list names three Pub. 970 headings and does not name the (A) person-and-timing predicate. P0 F5 classifies the same fact as compressing four statutory predicates: the chapeau plus (A), (B), and (C). The classification is taken from the statute, as P0 says (“Classified from those predicates, not from the field title”). The title’s omission of (A), and its citation of Pub. 970 rather than § 221(d)(1), are recorded.

3. **Regulation reorders (B) and (C).** 26 CFR § 1.221-1(e)(3)(i) places eligible-student status in (B) and the reasonable-period requirement in (C). The statute places reasonable period in (B) and eligible student in (C). P0 follows the statute. This unit follows the statute and cites the regulation’s tests without adopting its lettering.

4. **Related-person and employer-plan fact titles cite Pub. 970, not the concluding sentence.** `tax.us.2025.f1098e.no-related-person-interest` and `tax.us.2025.f1098e.no-qualified-employer-plan-interest` titles in the same bundle cite “Pub. 970 p.31.” P0 rows 3 and 4 correctly place both on the concluding sentence of § 221(d)(1). Pub. 970 is explanatory only.

5. **§ 1.221-1 effective-date recitation.** 26 CFR § 1.221-1(a)(1) and (h) still describe the 2001 amendment as applying through December 31, 2010. The statute as currently in force is the post-2001 text (no 60-month limitation). This unit uses § 1.221-1(e)(3) as the matching regulatory definition of a qualified education loan, not § 1.221-2 (pre-2002 / 60-month regime).

## Shared current consumption path (constituents 1–6)

Verified from the artifacts and evaluator path, not from titles.

- **No package `input_bindings`.** `packages/content/tax/2025/package.core-calculations.v38.json` `"input_bindings"` lists filing-status, rounding, and the four age/blindness/itemized symbols. None of the ten eligibility/scope facts appear there. The vocabulary bundle is a package member (`tax.us.2025.f1098e.vocabulary`); that is membership, not a binding.
- **Per-statement witnesses reach the run as collect sources.** `packages/derivation/live.py` `_iter_collect_categorical_names` walks `tax.us.2025.rule.sli-worksheet` `when`/`value` and registers each `collect_categorical_all_equal` `name` as a collect source. `packages/derivation/marshal.py` then, for each collect name, appends a `SourceFact` for every current finding whose fact type matches, rendering the value as `str(raw_value)` (`"yes"` / `"no"`). Identity keys on the finding are not used as the collect key; `env.sources[name]` is `list[str]` of values.
- **The worksheet reads a universal “all yes.”** On the nonempty Form 1098-E route, `tax.us.2025.rule.sli-worksheet` `value` has a `choose` whose `when` is `not` of an `all` of ten conjuncts. Three of those conjuncts are `collect_categorical_all_equal` nodes named `tax.us.2025.f1098e.no-related-person-interest`, `tax.us.2025.f1098e.no-qualified-employer-plan-interest`, and `tax.us.2025.f1098e.no-non-qualified-loan-component`, each with `value` a `category_literal` `"yes"` for that fact type. `packages/derivation/evaluator.py` `collect_categorical_all_equal`: empty `env.sources[name]` raises `EvalBlocked(BLOCK_ABSENT, [name])`; otherwise it returns `all(row == expected_val for row in rows)`. If any of those three (or the other universal conjuncts) is not all-`"yes"`, the `choose` takes `then: { "code": "SLI_UNIVERSAL_COMPONENT_VIOLATION", "op": "block" }`.
- **That block withholds line 21.** The rule publishes `tax.us.2025.schedule1.line21-sli-deduction`. A block is a product refusal, not a tax-law zero (P0 F4). `tax.us.2025.rule.schedule1-line26` reads line 21 by ref; Form 1040 line 10 / AGI then cannot compute from a missing dependency.
- **Closed-empty never reads these witnesses.** The same rule’s outer `choose` returns literal `0` when `count` of `tax.us.2025.f1098e.box1-student-loan-interest` over family `tax.us.2025.f1098e.1` equals 0. P0 F7: that zero is not a supported tax result.
- **Line-1 subtotal does not read qualification.** `tax.us.2025.rule.sli-worksheet-line1-subtotal` collects only box-1 amounts.
- **Form-field explanation does not name the circumstance.** `packages/content/tax/2025/schedule1.line-21.form-field.json` blocked `explain` is a four-way disjunction; its `codes` list is `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_UNCLOSED` and does not include `SLI_UNIVERSAL_COMPONENT_VIOLATION` (P0 F3).
- **No dedicated producer.** Outside tests and `tools/generate_f1098e_track8_presentation_goldens.py`, nothing prepares these assertions (P0 F1). Generic admission would accept a prepared `{yes, no}` for the declared fact type.
- **Correspondence.** Presence of at least one current value per fact type is required on the nonempty route (`BLOCK_ABSENT` if `rows == []`). Nothing requires one answer per statement, still less per loan (P0 F2, F6). Two box-1 statements with one witness finding between them yield `rows == ["yes"]` and the universal test can pass.

Identity of each of the three qualification facts: `lender` (entity `tax.us.student-loan-lender`), `statement` (entity `tax.us.1098e-statement`), `tax-year` literal `"2025"`. Domain `{yes, no}`. Supersession policy `free`.

---

## Constituent 1 — indebtedness incurred solely to pay qualified higher education expenses (chapeau)

### 1. Proposition

This loan was taken out only to pay the student’s higher-education costs of attendance (tuition and fees, and the institution’s allowances for room and board, books, supplies, transportation, and miscellaneous expenses), and not also to pay for something else.

### 2. Authority

26 U.S.C. § 221(d)(1) chapeau (flush language of paragraph (1) before the em-dash that introduces (A)–(C)):

> The term “qualified education loan” means any indebtedness incurred by the taxpayer solely to pay qualified higher education expenses—

“Qualified higher education expenses” is defined in § 221(d)(2) as the cost of attendance (HEA § 472 / 20 U.S.C. 1087ll, as in effect the day before August 5, 1997) at an eligible educational institution, reduced by amounts excluded under §§ 127, 135, 529, or 530 and by scholarships, allowances, or payments described in § 25A(g)(2). Eligible educational institution takes the § 25A(f)(2) meaning, plus internship/residency programs as provided in the last sentence of (d)(2).

26 CFR § 1.221-1(e)(3)(i) restates the sole-purpose requirement: “A qualified education loan means indebtedness incurred by a taxpayer solely to pay qualified higher education expenses that are—” 26 CFR § 1.221-1(e)(4) Example 6 (mixed-use loans): a note used in part to improve a residence and in part to pay a spouse’s qualified higher education expenses “is not a qualified education loan” because it was “not solely to pay qualified higher education expenses.”

The refinancing inclusion is the first flush sentence after (A)–(C), not this chapeau: “Such term includes indebtedness used to refinance indebtedness which qualifies as a qualified education loan.” 26 CFR § 1.221-1(e)(3)(v)(A) matches.

### 3. Scope

**Identified indebtedness.** The chapeau defines a term that applies to “any indebtedness.” The mixed-use example treats one promissory note as in or out of the class as a whole. The object is the loan (or a refinancing of such a loan), not a Form 1098-E statement and not the return. A statement may aggregate several loans (fact-type title of `tax.us.2025.f1098e.box1-student-loan-interest`; P0 F2 C7). That aggregation is how the report is keyed, not how the statutory object is scoped.

### 4. Ordinary facts and evidence

A person could state, without using the word “qualified”:

- what the borrowed money was used to pay (school bill, housing, books, versus a car, home improvement, or general living costs unrelated to the institution’s cost of attendance);
- whether one note mixed those uses;
- which school received the proceeds, and that it was a college, university, vocational school, or postgraduate internship/residency;
- for a refinancing, that the new note only paid off an earlier education loan.

Supporting records: promissory note and disbursement instructions; school account statements showing proceeds credited to tuition/housing; a mixed-use closing statement showing non-education proceeds.

The ordinary account is what the borrowed money paid for — school costs of attendance versus mixed non-education uses — and which school received the proceeds. That account is not itself the legal classification. Section 221(d)(2) defines the “qualified higher education expenses” the chapeau uses: cost of attendance reduced by the amounts in (d)(2)(A)–(B) (exclusions under §§ 127, 135, 529, or 530, and scholarships, allowances, or payments described in § 25A(g)(2)). A person can state those covering amounts as ordinary facts (a scholarship, employer educational assistance, a 529 or Coverdell exclusion applied to the same expenses) without applying the statute. They are a different ordinary showing from mixed-use. They are still part of what a favorable chapeau conclusion depends on.

### 5. Dependencies and invalidators

Must also be true for the indebtedness to be a qualified education loan: (A), (B), (C), and that the concluding-sentence exclusions do not apply. This constituent does not establish those.

A favorable chapeau conclusion also depends on the § 221(d)(2) determination of qualified higher education expenses, including those reductions. The chapeau’s object is indebtedness incurred solely to pay that *net* amount, not the institution’s gross cost of attendance. A covering amount — a scholarship, employer assistance, 529 or Coverdell exclusion, or other (d)(2)(A)–(B) amount — is a dependency that may reduce the supported ceiling. It does not, by its mere existence, disqualify the loan. The relevant question is quantitative and allocative: after the statutory reductions, did the indebtedness finance no more than, and was it incurred solely for, the remaining qualified expenses? That (d)(2) determination is a dependency of this constituent’s positive classification. It is not a the P1 obligation-and-amounts record § 221(e)(1) amount-reduction of an otherwise allowable deduction: (e)(1) operates later, on interest, after the loan is in the class.

Invalidators of a previously supported “solely” answer: evidence that some proceeds paid non-education costs; that the note was a home-equity or other mixed-purpose borrowing; that a purported refinancing also paid off non-qualified debt. A covering amount lowers the § 221(d)(2) ceiling and invalidates only when the borrowing exceeded that reduced net or financed something outside it. Existence of such a covering amount is not, by itself, an invalidator. A later change in how the student used leftover funds after a solely-education disbursement is a different question from the purpose for which the indebtedness was incurred.

### 6. Tax consequence

**Disqualify identified indebtedness.** If the indebtedness was not incurred solely to pay qualified higher education expenses as § 221(d)(2) defines them, it is not a qualified education loan. Interest on it is not interest “on any qualified education loan” under § 221(a). The operation is exclusion from the defined class, not a reduction of an otherwise allowable amount under § 221(e)(1), not a return-level zero under § 221(c), and not worksheet selection. A mixed-use showing is enough to disqualify. The absence of mixed use is not, by itself, a favorable chapeau conclusion.

The current product disposition is not that operation: a `"no"` on the compressed witness blocks `SLI_UNIVERSAL_COMPONENT_VIOLATION` and withholds Schedule 1 line 21 rather than computing a tax-law zero for that loan (P0 F4).

### 7. Correction and retraction behavior

Changing the ordinary account of what a particular loan paid for must displace the prior current support at that loan’s proposition identity. A later run must use only the corrected current support; the prior assertion remains history (ADR-0010; Selected product boundary 6). Withdrawing the account must leave this predicate unsupported. Absence is not a favorable “solely” answer (Selected product boundary 5).

Today the compressed fact cannot be corrected or retracted for this predicate alone: a new `{yes, no}` at `lender`/`statement`/`tax-year` restates chapeau+(A)+(B)+(C) together. Retracting the compressed fact, on the nonempty route, leaves `collect_categorical_all_equal` with `rows == []` and raises `BLOCK_ABSENT` only if no other current finding of that type remains; one remaining `"yes"` from another statement can still satisfy the universal test (P0 F2).

### 8. Reader-facing explanation

A durable output would have to say that this loan is not a qualified education loan because it was not taken out only to pay qualified higher education expenses — naming mixed use if that is the reason, or, if the borrowing exceeded the § 221(d)(2) net after covering amounts, that the loan financed more than the remaining qualified expenses. A covering amount is not itself the reason the loan is unqualified. If the product merely cannot support the purpose, or cannot support the (d)(2) ceiling, the explanation must say so, not that the law allows zero.

Today the blocked line-21 `explain` does not distinguish this circumstance from related-person debt, employer-plan debt, employer assistance, QTP earnings, worksheet-selection answers, MFS, or missing authority.

### 9. Unsupported nearby inference

The ordinary account that proceeds went to tuition, housing, or other cost-of-attendance categories does not establish that the indebtedness was incurred solely to pay the net “qualified higher education expenses” § 221(d)(2) defines. This proposition also does not establish that the expenses were for the taxpayer, spouse, or a then-dependent; that they were paid in time; that the student was an eligible student; that the lender is unrelated; that the loan was not an employer-plan loan; that the interest is deductible by this filer; or that the Form 1098-E box-1 figure is the deductible amount. A federal student loan is not automatically a qualified education loan merely because a lender reported it.

### 10. Current representation

Compressed into `tax.us.2025.f1098e.no-non-qualified-loan-component` `{yes, no}`, per statement. Consumption: shared path above. The single committed witness asks the answerer to certify that “no non-qualified-loan component is included in this statement’s box-1 figure.” A person would have to be asked today, for this constituent, what the loan proceeds paid for and whether any non-education use shared the same note — not whether a “non-qualified-loan component” is absent from box 1. That ordinary proceeds question is not the whole chapeau.

If a bounded candidate captures only whether proceeds went to nominal cost-of-attendance categories or to mixed non-education purposes, that showing establishes three things and not a fourth:

- it can support a **mixed-use negative** that disqualifies the indebtedness (reg. Example 6);
- it can supply **one premise** toward a favorable classification (the proceeds were not mixed with non-education uses);
- it **cannot alone** establish that the indebtedness was incurred solely to pay the net “qualified higher education expenses” defined by § 221(d)(2).

The § 221(d)(2) determination, including its reductions, is a dependency of a favorable chapeau conclusion: it sets the ceiling against which the borrowing is compared. It is amount-bearing because (d)(2) is an amount definition. That does not make a covering amount an automatic disqualifier, a different constituent, or a reason to treat this chapeau as cheaper than (A)–(C) or the concluding-sentence exclusions. On boundedness, without ranking: mixed-use is a closed negative; the (d)(2) net is the ceiling required for the positive and is not decided by the mixed-use question.

---

## Constituent 2 — person on whose behalf the expenses were incurred, as of origination (subparagraph (A))

### 1. Proposition

The school costs this loan was taken out to pay were for the borrower, the borrower’s spouse, or a person who was the borrower’s dependent at the time the loan was taken out — not for someone who stood in some other relation then.

### 2. Authority

26 U.S.C. § 221(d)(1)(A):

> which are incurred on behalf of the taxpayer, the taxpayer’s spouse, or any dependent of the taxpayer as of the time the indebtedness was incurred,

The relative “which” refers to the qualified higher education expenses in the chapeau.

§ 221(d)(4): “The term ‘dependent’ has the meaning given such term by section 152 (determined without regard to subsections (b)(1), (b)(2), and (d)(1)(B) thereof).”

26 CFR § 1.221-1(e)(3)(i)(A): expenses that are “Incurred on behalf of a student who is the taxpayer, the taxpayer’s spouse, or a dependent (as defined in section 152) of the taxpayer at the time the taxpayer incurs the indebtedness.” The regulation inserts “a student who is” and cites § 152 without restating (d)(4)’s disregarded subsections. The statutory timing words “as of the time the indebtedness was incurred” are controlling.

### 3. Scope

**Identified indebtedness.** Subparagraph (A) is a condition on the expenses that define whether *that indebtedness* is a qualified education loan. The determination date is origination of that indebtedness, not the current taxable year and not the Form 1098-E statement year. A statement that aggregates loans originated for different students, or at times when dependent status differed, is not the statutory object.

### 4. Ordinary facts and evidence

A person could state:

- who was in school when this loan was taken out;
- that person’s relation to the borrower at that time (self, spouse, child, other);
- whether the borrower could claim that person as a dependent on a return for the period that includes origination (who lived where, support, age, student status as ordinary household facts — not the § 152 conclusion as a user-supplied tax label).

Supporting records: the note naming the student; school bills in that person’s name dated around origination; household and support facts as of origination, not as of 2025 filing.

### 5. Dependencies and invalidators

Depends on there being identified indebtedness and identified expenses (constituent 1’s object). Independent of whether, in 2025, another taxpayer claims the filer (§ 221(c) — return-scoped, the P1 obligation-and-amounts record) and independent of who is legally obligated to pay the 2025 interest (§ 1.221-1(b)(1) — the P1 obligation-and-amounts record).

Invalidators: the student was a sibling, friend, or other person who was not the taxpayer, spouse, or a § 221(d)(4) dependent at origination; origination-time household facts were wrong; the loan was taken out after the person ceased to be a dependent. That the student later marries, or later is no longer a dependent, does not by itself undo an origination-time (A) that was true.

### 6. Tax consequence

**Disqualify identified indebtedness.** If the expenses were not incurred on behalf of the taxpayer, spouse, or a then-dependent, the indebtedness is not a qualified education loan. Same statutory operation as constituent 1; different predicate. Current product disposition on the compressed `"no"` is the same `SLI_UNIVERSAL_COMPONENT_VIOLATION` refusal.

### 7. Correction and retraction behavior

A correction must be at the origination-time person/relationship identity of that loan. Changing “this was for my child, who I could claim then” to “this was for my sibling, who I could not claim then” must displace the prior current support. Retraction must leave (A) unsupported, not “yes.”

Today the compressed statement-scoped `{yes, no}` cannot correct (A) without restating the chapeau, (B), and (C). Origination-time dependent status has no identity of its own in the committed vocabulary.

### 8. Reader-facing explanation

The output would have to say this loan is not a qualified education loan because the school costs it paid were not for the borrower, the borrower’s spouse, or someone the borrower could claim as a dependent when the loan was taken out — naming who the student was. A missing origination-time account must be explained as unsupported, not as a zero deduction.

### 9. Unsupported nearby inference

Does not establish that the student was an eligible student, that costs were paid in time, that the loan was solely for those costs, that the 2025 filer may deduct the interest, or that a parent who signed a 2025 Form 1098-E as borrower is the person (A) is about. Does not decide § 221(c) for the current year.

### 10. Current representation

Same compressed fact as constituent 1. The committed witness does not ask who the student was or whether that person was a dependent at origination. A person would have to be asked those ordinary questions today; the single `{yes, no}` asks only whether a “non-qualified-loan component” is absent from the statement’s box 1. The fact-type title does not even list this predicate among the collapsed sub-questions (discrepancy 2).

On boundedness, without ranking: “self / spouse / then-dependent / someone else” is a small ordinary partition. Applying the modified § 152 test at origination is a legal determination over those household facts. No loan-level identity exists today (P0 F2 C7).

---

## Constituent 3 — reasonable period of time (subparagraph (B))

### 1. Proposition

The school costs this loan was taken out to pay were paid, or billed, around the time the loan was taken out — not years earlier or years later as unrelated spending.

### 2. Authority

26 U.S.C. § 221(d)(1)(B):

> which are paid or incurred within a reasonable period of time before or after the indebtedness is incurred,

The statute does not define “reasonable period of time.” 26 CFR § 1.221-1(e)(3)(ii) supplies the test (lettered (C) in the regulation; (B) in the statute — discrepancy 3):

> Except as otherwise provided in this paragraph (e)(3)(ii), what constitutes a reasonable period of time for purposes of paragraph (e)(3)(i)(C) of this section generally is determined based on all the relevant facts and circumstances. However, qualified higher education expenses are treated as paid or incurred within a reasonable period of time before or after the taxpayer incurs the indebtedness if—
>
> (A) The expenses are paid with the proceeds of education loans that are part of a Federal postsecondary education loan program; or
>
> (B) The expenses relate to a particular academic period and the loan proceeds used to pay the expenses are disbursed within a period that begins 90 days prior to the start of that academic period and ends 90 days after the end of that academic period.

26 CFR § 1.221-1(e)(4) Examples 4 and 5 illustrate the 90-day disbursement window and that a later loss of the school’s Title IV eligibility does not undo a loan that already met the test for those semesters.

### 3. Scope

**Identified indebtedness**, paired with the expenses and academic period that indebtedness paid. The 90-day safe harbor is stated in terms of “the loan proceeds used to pay the expenses” and “a particular academic period.” The federal-program safe harbor is stated in terms of “education loans that are part of a Federal postsecondary education loan program.” Neither is a fact about a Form 1098-E statement as a whole, nor about the 2025 return.

### 4. Ordinary facts and evidence

A person could state:

- when the loan was signed and when proceeds were disbursed;
- which academic term those proceeds paid for, and that term’s start and end dates;
- whether this was a federal student loan (Direct, FFEL, Perkins, or another federal postsecondary program) whose proceeds paid the school costs;
- if not, the dates of the school charges relative to disbursement.

Supporting records: promissory note and disbursement dates; school calendar; school account credits; for a federal loan, the loan program identified on the note or Master Promissory Note. The person need not apply the words “reasonable period.”

### 5. Dependencies and invalidators

Depends on identified expenses for identified indebtedness (the chapeau’s object). Independent of who the student was (A) and of eligible-student status (C), though the 90-day window is measured against an academic period that (C) also cares about.

Invalidators of a previously supported timing answer: disbursement actually fell outside the academic period by more than 90 days on each end, and the loan was not a federal postsecondary education loan; the proceeds paid a different term than claimed; facts-and-circumstances timing that once looked contemporaneous is shown to be a reimbursement of much earlier costs or an advance for a remote future period. Example 5: the school’s later loss of eligibility does not invalidate a loan that already satisfied timing for those terms.

### 6. Tax consequence

**Disqualify identified indebtedness.** Expenses not paid or incurred within a reasonable period before or after origination keep that indebtedness out of the qualified-education-loan class. Current product disposition on the compressed `"no"` is again `SLI_UNIVERSAL_COMPONENT_VIOLATION`, a refusal.

### 7. Correction and retraction behavior

A correction must change the origination/disbursement/academic-period account for that loan. A later run must use only the corrected dates and program identity. Retracting “this was a federal loan disbursed for fall 2018” must leave timing unsupported.

Today the compressed `{yes, no}` cannot correct timing without restating the chapeau, (A), and (C). There is no committed place to record disbursement dates or federal-program membership.

### 8. Reader-facing explanation

The output would have to say this loan is not a qualified education loan because the school costs were not paid around the time the loan was taken out — or that the product cannot support the timing. If a safe harbor is the reason the timing holds, a reader-facing account could name it (federal program, or disbursed within 90 days of the term). Today the blocked explain names none of that.

### 9. Unsupported nearby inference

Does not establish that a federal student loan is qualified in every other respect; that box 1 is the right amount; that origination fees or capitalized interest are interest (those are § 1.221-1(f), not (e)(3)(ii)); or that a disbursement inside 90 days proves eligible-student status or sole purpose.

### 10. Current representation

Same compressed fact. The committed witness does not ask when proceeds were disbursed, which term they paid, or whether the loan was part of a federal postsecondary program. A person would have to be asked those timing and program facts today; the single `{yes, no}` asks whether a “non-qualified-loan component” is absent from box 1. The fact-type title does name “reasonable-period-of-time” as one of three collapsed Pub. 970 sub-questions, still as a tax-labelled absence, not as dates.

On boundedness, without ranking: the two regulatory safe harbors are closed tests (federal program; 90-day window). Outside them, “all the relevant facts and circumstances” is open-ended. No loan-level identity exists today.

---

## Constituent 4 — eligible-student status (subparagraph (C))

### 1. Proposition

The person whose schooling this loan paid for was, during the academic period of that schooling, a student in a degree or certificate program who was taking at least half of a full-time load.

### 2. Authority

26 U.S.C. § 221(d)(1)(C):

> which are attributable to education furnished during a period during which the recipient was an eligible student.

§ 221(d)(3): “The term ‘eligible student’ has the meaning given such term by section 25A(b)(3).”

26 U.S.C. § 25A(b)(3):

> For purposes of this subsection, the term “eligible student” means, with respect to any academic period, a student who—
>
> (A) meets the requirements of section 484(a)(1) of the Higher Education Act of 1965 (20 U.S.C. 1091(a)(1)), as in effect on the date of the enactment of this section, and
>
> (B) is carrying at least ½ the normal full-time work load for the course of study the student is pursuing.

26 CFR § 1.221-1(e)(3)(i)(B) (lettered (B) in the regulation; (C) in the statute — discrepancy 3):

> Attributable to education provided during an academic period, as described in section 25A and the regulations thereunder, when the student is an eligible student as defined in section 25A(b)(3) (requiring that the student be a degree candidate carrying at least half the normal full-time workload);

The parenthetical is the regulation’s paraphrase of § 25A(b)(3). The statutory cross-reference remains (b)(3)(A) and (B).

This is **not** the concluding sentence of § 221(d)(1). Related-person and employer-plan exclusion sit after (C), in flush language.

### 3. Scope

**Identified indebtedness**, through the education the expenses paid for and the academic period of that education. “Eligible student” is defined “with respect to any academic period.” A loan can fail (C) for one period and, if it paid more than one period, present mixed academic-period facts on the same indebtedness. The object is still that indebtedness, not the 2025 statement and not the return. Enrollment in 2025 is irrelevant unless that is the period the loan paid for.

### 4. Ordinary facts and evidence

A person could state:

- which school and which term the loan paid for;
- that the student was enrolled in a degree, certificate, or other recognized-credential program (not a casual non-degree course);
- roughly how many credits or clock hours, and whether that was at least half of a full-time load for that program.

Supporting records: enrollment or registrar certification for that term; course load; program of study. The person need not say “eligible student.”

### 5. Dependencies and invalidators

Depends on identified expenses attributable to identified education (chapeau + the “attributable to” clause of (C)). Independent of origination-time dependent status (A), except that both name a student. Independent of 2025 half-time status.

Invalidators: the student was less than half-time that term; was not enrolled in a degree/certificate program; was not enrolled or accepted for enrollment in an eligible program at an eligible institution (HEA § 484(a)(1) as pinned by § 25A(b)(3)(A)); the loan actually paid a different period than claimed. Example 3 of § 1.221-1(e)(4) is a half-time graduate student whose commercial-bank loan is a qualified education loan when the other tests are met — half-time is enough; full-time is not required.

### 6. Tax consequence

**Disqualify identified indebtedness.** If the education was not furnished while the recipient was an eligible student, the indebtedness is not a qualified education loan. Current product disposition on the compressed `"no"` is `SLI_UNIVERSAL_COMPONENT_VIOLATION`.

### 7. Correction and retraction behavior

A correction must change the enrollment/load account for the academic period this loan paid for. Retracting “I was half-time in a bachelor’s program that term” must leave (C) unsupported.

Today the compressed `{yes, no}` cannot correct (C) without restating the chapeau, (A), and (B). There is no committed enrollment or workload fact.

### 8. Reader-facing explanation

The output would have to say this loan is not a qualified education loan because, during the term it paid for, the student was not in a degree or certificate program at least half-time — or that the product cannot support that enrollment. Today the blocked explain does not name enrollment or workload.

### 9. Unsupported nearby inference

Does not establish the American Opportunity or Lifetime Learning credit, which share § 25A(b)(3) for a different statutory operation. Does not establish that the school is an eligible educational institution for § 221(d)(2) (a chapeau/QHEE question). Does not establish that a graduate student is ineligible (Example 3 is the opposite). Does not establish current-year student status.

### 10. Current representation

Same compressed fact. The committed witness does not ask whether the student was in a degree/certificate program or at least half-time during the term the loan paid for. A person would have to be asked those enrollment facts today; the single `{yes, no}` asks whether a “non-qualified-loan component” is absent from box 1. The fact-type title names “student-status” as one collapsed Pub. 970 sub-question.

What a person would have to be asked today versus the single committed witness, for constituents 1–4 together:

| Constituent | Ordinary question a person would face | What `no-non-qualified-loan-component` actually asks |
| --- | --- | --- |
| 1 chapeau | What did this loan pay for, and did the same note pay for anything else? (ordinary proceeds use; not the § 221(d)(2) net) | One `{yes, no}` that no “non-qualified-loan component” is in this statement’s box 1 |
| 2 (A) | Who was the student, and at origination were they you, your spouse, or someone you could claim? | Same single `{yes, no}` |
| 3 (B) | When were proceeds disbursed relative to the term, and was this a federal student loan? | Same single `{yes, no}` |
| 4 (C) | During that term, was the student in a degree/certificate program at least half-time? | Same single `{yes, no}` |

A `"yes"` on that witness asserts all four predicates at once. A `"no"` does not say which failed. There is no way to state, correct, or retract any one of them independently (P0 F5).

On boundedness, without ranking: half-time-or-more in a degree/certificate program is a closed ordinary partition for a named term. HEA § 484(a)(1) as of August 5, 1997, is a legal cross-reference on top of that enrollment. No loan- or period-level identity exists today.

---

## Constituent 5 — related-person indebtedness (concluding sentence)

### 1. Proposition

The person this loan is owed to is not someone related to the borrower in the family or ownership sense the tax law uses for related-party deals — not a parent, grandparent, sibling, spouse, or other person in that relatedness list.

### 2. Authority

Flush concluding sentence of 26 U.S.C. § 221(d)(1), following subparagraphs (A)–(C), not itself a subparagraph:

> The term “qualified education loan” shall not include any indebtedness owed to a person who is related (within the meaning of section 267(b) or 707(b)(1)) to the taxpayer or to any person by reason of a loan under any qualified employer plan (as defined in section 72(p)(4)) or under any contract referred to in section 72(p)(5).

The related-person clause is the first exclusion in that sentence: “indebtedness owed to a person who is related (within the meaning of section 267(b) or 707(b)(1)) to the taxpayer.” The employer-plan clause is a separate exclusion in the same sentence (constituent 6).

26 CFR § 1.221-1(e)(3)(iii) splits the sentence the same way:

> A qualified education loan does not include any indebtedness owed to a person who is related to the taxpayer, within the meaning of section 267(b) or 707(b)(1). For example, a parent or grandparent of the taxpayer is a related person.

26 U.S.C. § 267(b) lists the related persons. Family, for this purpose, is § 267(c)(4): “brothers and sisters (whether by the whole or half blood), spouse, ancestors, and lineal descendants.” § 267(c) constructive-ownership rules apply “for purposes of determining, in applying subsection (b), the ownership of stock” — they reach this question only where a (b) paragraph turns on stock ownership, not for the family paragraph itself. 26 U.S.C. § 707(b)(1) adds partnership/partner and two-partnership relationships at more than 50 percent of capital or profits interests, with constructive ownership via § 267(c) other than (c)(3).

### 3. Scope

**Identified indebtedness.** The statute removes “any indebtedness owed to” a related person from the qualified-education-loan class. Relatedness is between the taxpayer and the creditor on that indebtedness. It is not a fact about the 2025 return as a whole, and it is not a fact about a Form 1098-E statement except insofar as a statement happens to name a lender. A servicer on the form may not be the person to whom the indebtedness is owed. A statement that aggregates a related-person loan with an unrelated-person loan has mixed objects under this proposition.

### 4. Ordinary facts and evidence

A person could state:

- who lent the money (the person or entity the note is owed to, not merely who sent the 1098-E);
- that person’s relation to the borrower (parent, grandparent, sibling, spouse, child, unrelated bank or federal program, family partnership, closely held corporation).

Supporting records: the promissory note naming the lender; for a family loan, the family relationship as an ordinary household fact. The person need not apply § 267(b) or constructive-ownership arithmetic. Those are the rule’s classification, not the ordinary account.

### 5. Dependencies and invalidators

Independent of chapeau+(A)+(B)+(C): a loan that otherwise meets the definition is still not a qualified education loan if owed to a related person. Independent of who paid the 2025 interest (§ 1.221-1(b)(4)) and of who is legally obligated (§ 1.221-1(b)(1)). A parent who *pays* interest on a loan owed to an unrelated lender is not this constituent.

Invalidators: the creditor is (or is discovered to be) a § 267(b) or § 707(b)(1) related person; a note nominally from an unrelated entity is owed in substance to a related person; relatedness that depends on stock or partnership ownership changes so that the >50 percent tests are met. A later sale of the note to an unrelated holder is a different indebtedness question (who it is “owed to” now) and is not decided here.

### 6. Tax consequence

**Disqualify identified indebtedness.** Related-person debt “shall not include” in the qualified-education-loan class at all. The operation is exclusion from the definition, not an amount reduction under § 221(e)(1), not a § 221(c) return-level zero, and not worksheet selection.

Current product disposition: `"no"` on `tax.us.2025.f1098e.no-related-person-interest` makes `collect_categorical_all_equal` false and the worksheet blocks `SLI_UNIVERSAL_COMPONENT_VIOLATION`, withholding line 21 rather than computing a tax-law zero for that loan (P0 F4).

### 7. Correction and retraction behavior

Changing “I borrowed this from my grandmother” to “I borrowed this from a bank” (or the reverse) must displace the prior current support at this proposition’s identity. A later run must use only the corrected creditor/relationship account. Retracting the account must leave relatedness unsupported, not a favorable “not related.”

Today the committed fact is statement-scoped `{yes, no}` at `lender`/`statement`/`tax-year`. A correction at that identity restates the whole related-person conclusion for the statement, not a named creditor. Two statements with one related-person finding between them still have the F2 correspondence gap. Mixed loans on one statement have no per-loan answer.

### 8. Reader-facing explanation

A durable output would have to say this loan is not a qualified education loan because it is owed to a related person — naming the relation (for example, a parent or grandparent) — and that interest on it therefore does not enter the deduction. If the product cannot support who the creditor is, it must say that, not that the law allows zero. Today the blocked line-21 `explain` does not distinguish related-person debt from the compressed 1–4 predicates, employer-plan debt, or the other universal gates.

### 9. Unsupported nearby inference

Does not establish that the loan otherwise meets the chapeau and (A)–(C). Does not establish § 267(a) loss or expense matching. Does not establish that a related person who *paid* the interest is the creditor. Does not establish qualified-employer-plan exclusion (same sentence, different clause). Does not establish that the Form 1098-E lender identity is the person to whom the indebtedness is owed.

### 10. Current representation

`tax.us.2025.f1098e.no-related-person-interest` in `packages/content/tax/2025/f1098e.bundle.json`. Per-statement `{yes, no}`; `"yes"` asserts the excluded class is absent from this statement’s box 1; `"no"` asserts it is present. Title cites “Pub. 970 p.31, ‘Related person’” (discrepancy 4), not the concluding sentence of § 221(d)(1). Identity keys: `lender`, `statement`, `tax-year` `"2025"`. Supersession `free`.

Consumption: shared path. This fact is one of the five `collect_categorical_all_equal` conjuncts in `tax.us.2025.rule.sli-worksheet`, not the compressed `no-non-qualified-loan-component` fact. It is not in `package.core-calculations.v38.json` `input_bindings`. No dedicated producer (P0 F1). Presence of at least one current value is required on the nonempty route; per-statement and per-loan correspondence are not (P0 F2, F6).

What a person would have to be asked today versus the committed witness: who the loan is owed to, and that person’s ordinary relation to the borrower — not whether “no related-person loan interest is included in this statement’s box-1 figure,” which asks the answerer to apply the § 267(b)/§ 707(b)(1) test and report the tax conclusion (P0 row 3).

On boundedness, without ranking: parent/grandparent/sibling/spouse as ordinary family facts match the regulation’s example and § 267(c)(4). The rest of the (b) list and constructive ownership are a legal test over ownership facts. Statement-level `{yes, no}` cannot represent mixed creditors on one Form 1098-E.

---

## Constituent 6 — qualified-employer-plan indebtedness (concluding sentence)

### 1. Proposition

This loan was not a borrowing from the borrower’s workplace retirement plan — not a 401(k), 403(a), 403(b), or government-plan loan, and not a loan under a contract bought under one of those plans.

### 2. Authority

Same flush concluding sentence of 26 U.S.C. § 221(d)(1), second exclusion (not a subparagraph):

> … or to any person by reason of a loan under any qualified employer plan (as defined in section 72(p)(4)) or under any contract referred to in section 72(p)(5).

26 CFR § 1.221-1(e)(3)(iii), second sentence:

> In addition, a qualified education loan does not include a loan made under any qualified employer plan as defined in section 72(p)(4) or under any contract referred to in section 72(p)(5).

26 U.S.C. § 72(p)(4)(A)(i): “qualified employer plan” means a plan described in § 401(a) with a § 501(a) trust, an annuity plan described in § 403(a), or a plan under which the employer contributes for a § 403(b) annuity contract. § 72(p)(4)(A)(ii) includes any plan that was (or was determined to be) a qualified employer plan or a government plan. § 72(p)(4)(B): “government plan” means any plan, whether or not qualified, established and maintained for its employees by the United States, a State or political subdivision, or an agency or instrumentality of any of those.

26 U.S.C. § 72(p)(5): for purposes of subsection (p), an amount received as a loan under a contract purchased under a qualified employer plan (and any assignment or pledge with respect to such a contract) is treated as a loan under that employer plan.

The related-person clause (constituent 5) is about *who is owed*. This clause is about *under what arrangement the loan was made*. They share a sentence and do not share a proposition.

### 3. Scope

**Identified indebtedness.** The statute removes indebtedness that exists “by reason of a loan under” a § 72(p)(4) plan or a § 72(p)(5) contract. The object is that plan loan, not the Form 1098-E statement and not the return. A statement that aggregates a plan loan with a commercial or federal student loan has mixed objects. Plan loans often never produce a Form 1098-E; that is a reporting fact, not a change in the statutory object.

### 4. Ordinary facts and evidence

A person could state:

- that the money came from a workplace retirement account or pension (401(k), 403(b), 457, TSP, state or federal employee plan, or similar);
- that the “lender” is the plan or the annuity contract, not a bank or the Department of Education;
- that repayment is by payroll withholding against the plan balance.

Supporting records: plan-loan promissory note; summary plan description; Form 1099-R if a deemed distribution occurred (a different tax event, usable only as a clue that a plan loan existed). The person need not classify the arrangement as “§ 72(p)(4)” or “§ 72(p)(5).”

### 5. Dependencies and invalidators

Independent of chapeau+(A)+(B)+(C) and of related-person status: a plan loan is out of the class even if it paid school costs for an eligible then-dependent student and is owed to an unrelated trustee. Independent of § 221(e)(1) employer educational assistance (that provision reduces an otherwise allowable deduction by an amount; this provision says the indebtedness is not a qualified education loan). Independent of who paid the 2025 interest.

Invalidators: the arrangement is (or is discovered to be) a § 72(p)(4) plan or a § 72(p)(5) contract loan; a commercial-looking note is in substance a plan loan. That the plan later offsets the balance, or issues a deemed distribution under § 72(p)(1), does not convert a plan loan into a qualified education loan.

### 6. Tax consequence

**Disqualify identified indebtedness.** A loan under a qualified employer plan or a § 72(p)(5) contract is not a qualified education loan. Same statutory operation as constituent 5 (exclusion from the defined class), different clause.

Current product disposition: `"no"` on `tax.us.2025.f1098e.no-qualified-employer-plan-interest` makes `collect_categorical_all_equal` false and the worksheet blocks `SLI_UNIVERSAL_COMPONENT_VIOLATION`, withholding line 21 rather than computing a tax-law zero (P0 F4).

### 7. Correction and retraction behavior

Changing “this was a 401(k) loan” to “this was a Direct Loan” (or the reverse) must displace the prior current support. Retracting the account must leave the plan-loan predicate unsupported, not a favorable “not a plan loan.”

Today the committed fact is statement-scoped `{yes, no}` at `lender`/`statement`/`tax-year`. A correction restates the whole employer-plan conclusion for the statement. Mixed plan and non-plan loans on one statement have no per-loan answer. The F2 correspondence gap applies the same way as for constituent 5.

### 8. Reader-facing explanation

A durable output would have to say this loan is not a qualified education loan because it was a workplace-retirement-plan loan (naming the kind of plan if known) — or that the product cannot support whether it was. Today the blocked line-21 `explain` does not distinguish this from related-person debt or from the compressed 1–4 predicates.

### 9. Unsupported nearby inference

Does not establish related-person exclusion. Does not establish § 72(p)(1) deemed-distribution income. Does not establish § 221(e)(1) employer educational-assistance reduction (different operation, different object). Does not establish that absence of a Form 1098-E means there was no plan loan, or that presence of a 1098-E means there was none. Does not establish the chapeau or (A)–(C).

### 10. Current representation

`tax.us.2025.f1098e.no-qualified-employer-plan-interest` in `packages/content/tax/2025/f1098e.bundle.json`. Per-statement `{yes, no}`; `"yes"` asserts the excluded class is absent from this statement’s box 1; `"no"` asserts it is present. Title cites “Pub. 970 p.31, ‘Qualified employer plan’” (discrepancy 4). Identity keys: `lender`, `statement`, `tax-year` `"2025"`. Supersession `free`.

Consumption: shared path; a separate `collect_categorical_all_equal` conjunct from related-person and from `no-non-qualified-loan-component`. Not in package `input_bindings`. No dedicated producer (P0 F1). Same presence-without-correspondence behavior as the other per-statement witnesses (P0 F2, F6).

What a person would have to be asked today versus the committed witness: whether this borrowing came from a workplace retirement plan or a contract bought under one — not whether “no qualified-employer-plan loan interest is included in this statement’s box-1 figure,” which asks the answerer to classify the arrangement under § 72(p)(4) or § 72(p)(5) and report the tax conclusion (P0 row 4).

On boundedness, without ranking: “borrowed from my 401(k) / 403(b) / government plan / not a workplace plan” is an ordinary partition a person can state. Mapping that account onto § 72(p)(4) and (p)(5) is a legal classification. Statement-level `{yes, no}` cannot represent mixed plan and non-plan loans on one Form 1098-E.

---

## Grouping analysis

Tested against the plan’s six equivalence requirements: precise tax proposition; ordinary facts and evidence; dependencies and invalidators; correction and retraction behavior; tax consequence; reader-facing explanation. Sharing a debt identity is not sufficient. This section does not select, rank, or recommend a forcing case.

**None of the six constituents can honestly be grouped with any other.**

All six share one statutory operation class — they disqualify identified indebtedness from the qualified-education-loan definition — and constituents 1–4 range over the same loan. That is the plan’s stated non-reason. They fail the other five requirements, as follows.

**Constituents 1–4 (chapeau and (A)–(C)) cannot be grouped with each other.**

| Requirement | Why they are not equivalent |
| --- | --- |
| Proposition | Four different ordinary assertions: what the note paid for; who the student was at origination; whether costs were paid around origination; whether that student was at least half-time in a degree/certificate program during the term paid for. Constituent 1’s ordinary proceeds-use assertion is not the legal chapeau: a favorable solely-to-pay conclusion still depends on the § 221(d)(2) net. |
| Ordinary facts and evidence | Proceeds-use and mixed-purpose records, plus covering amounts as inputs to the § 221(d)(2) ceiling, not as a demonstrated failure; origination-time household/relationship facts; disbursement dates, academic calendar, and federal-program identity; enrollment and workload for a named term. |
| Dependencies and invalidators | Each fails on a different showing (mixed-use note, or borrowing that exceeded the § 221(d)(2) net after covering amounts — not the mere existence of a covering amount; student was not then a dependent; disbursement outside the safe harbors and not contemporaneous; less-than-half-time or non-program enrollment). A later change that undoes one leaves the others untouched. |
| Correction and retraction | Each needs its own current support. The incumbent `no-non-qualified-loan-component` `{yes, no}` forces them to be stated, corrected, and retracted together; that compression is the defect P0 F5 named, not evidence they are the same proposition. |
| Tax consequence | Same *class* of operation (the indebtedness is not a qualified education loan), produced by different predicates. Implementing one must not silently establish the others. |
| Reader-facing explanation | A reader who is told only that a “non-qualified-loan component” is present cannot tell which of the four circumstances obtained. Each warrants its own named reason. |

Reassembling 1–4 under a new label would reconstruct `no-non-qualified-loan-component`. The plan forbids that.

**Constituents 5 and 6 cannot be grouped with each other**, even though they share the concluding sentence and the same exclusion-from-the-class operation.

| Requirement | Why they are not equivalent |
| --- | --- |
| Proposition | 5 is about *who is owed* (related creditor). 6 is about *under what arrangement the loan was made* (workplace plan or § 72(p)(5) contract). |
| Ordinary facts and evidence | Family or ownership relation to the creditor versus “this came from my 401(k) / 403(b) / government plan.” |
| Dependencies and invalidators | A parent note fails 5 and need not be a plan loan. A 401(k) loan fails 6 even when the trustee is unrelated. |
| Correction and retraction | Separate committed facts today, which is the right split of identities even though both are statement-scoped `{yes, no}`. Correcting relatedness must not restated plan-loan status, or the reverse. |
| Tax consequence | Same class (not a qualified education loan), different clause. |
| Reader-facing explanation | “Owed to your grandmother” is not “borrowed from your 401(k).” |

**Constituents 5 and 6 cannot be grouped with 1–4.** The concluding sentence removes indebtedness from a class that the chapeau and (A)–(C) would otherwise include. Relatedness and plan-loan status do not answer what the money paid for, whether the borrowing stayed within the § 221(d)(2) ceiling after covering amounts, for whom, when, or during what enrollment. The incumbent already keeps 5 and 6 as separate facts from the compressed 1–4 witness; that split tracks the statute and is not a reason to merge either with 1–4.

**The shared current product disposition is not a grouping ground.** All six, on a `"no"`, currently raise `SLI_UNIVERSAL_COMPONENT_VIOLATION` and withhold line 21. That is P0 F4’s flattening of distinct operations into one refusal, not equivalence of proposition, evidence, invalidators, correction, or explanation.

On boundedness, without ordering: each constituent has an ordinary showing that can fail it, and a legal classification that ordinary showing does not finish. Constituent 1’s mixed-use negative can disqualify and is only one premise toward a favorable chapeau; the positive still depends on the § 221(d)(2) ceiling after covering amounts, which are inputs to that ceiling, not existence-invalidators. Constituent 2 has a small ordinary person-partition plus a modified § 152 test at origination. Constituent 3 has two closed regulatory safe harbors and an open facts-and-circumstances residue. Constituent 4 has a closed ordinary enrollment/load partition for a named term plus a legal HEA cross-reference. Constituent 5 has an ordinary family core (the regulation’s parent/grandparent example) and a wider legal relatedness list. Constituent 6 has an ordinary workplace-plan partition plus a legal § 72(p) classification. Neither mixed-use nor the (d)(2) ceiling is a reason to treat constituent 1 as cheaper or costlier than 2–6. None of that is a ranking.
