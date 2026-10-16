# P3 — Connected design for the opening mortgage case

This draft was written on the milestone branch as a proposal. It does not
accept itself.

## Revision

**Current production-review repair.** The P7 narrative below records the
design and prototype evidence used for production v44; it does not establish
the later successor's behavior. The independent production review found that
three remaining uncertainty answers were still described as outside coverage.
The active plan selects a successor that names liability, certificate and
original-loan uncertainty, names known coverage limits, and explains the
actual basis of each zero. It preserves the amount boundary and decisive-zero
precedence. Saved answers must retain their normalized values and provenance
while displaying the selected consumer's exact-version content descriptions.
The active repair charter defines the implementation evidence required before
these successor claims count as demonstrated.

This is the P7 correction round, specified by
the P7 payment-and-fixtures charter
against the P6 re-review's payment and fixture findings.
It retains the earlier corrected completion-timing distinction. It also
retains the reviewed `date_compare` operator
(ADR 0078, accepted on review). It replaces the
earlier `v43`-successor numbering with the numbers after the
line 8a debt-limit fix, which has since
been adopted for real as core calculations v43, published-packages
registry v41, and release v41 (accepted on review) —
this round's own successor release is renumbered v42 so it no longer
collides with that real, adopted v41. Probed by
[`p5_probe.py`](p5_probe.py), which extends `p4_probe.py`'s arrangement in
a temporary registry and runs it through `live_coordinate_run` and the real
presentation model. Earlier rounds (`p3_probe.py`, `p4_probe.py`) are left
unchanged. Every mark below is either **Probe result** (`p3_probe.py`,
first round), **P4 repair** (`p4_probe.py`), **P5 repair** (`p5_probe.py`),
**P6 correction** (`p5_probe.py`), **P7 correction** (`p5_probe.py`'s
`--p7-targeted` mode), or
**Proposal** (not yet probed). Nothing here
is adopted; the probed citizens are not published and the probes commit no
generated output.

This round resolves each P6 re-review finding:

- **Payment exclusion.** `paid-the-interest` distinguishes full payment by
  the filing unit, some/all payment by others or only partial payment by the
  filing unit, genuine no-payment by or for the unit, and uncertainty. The
  partial/third-party category has its own outside-coverage reason and blocks
  line 8a; it is not a zero and cannot take the favourable arm.
- **Fixture corrections.** The named joint case records actual
  `married_filing_jointly` status; the investment example records use as
  `other` and stays outside coverage. The separate personal-expense timing
  analogues remain distinct. The pre-completion case is Publication 936
  situation 2, not Example 2.
- **Correction evidence.** Synthetic same-statement answer corrections
  demonstrate supported → outside-coverage → supported coordinator outcomes
  and current input support. Recorder save/correct/withdraw behavior remains
  specified, not built or demonstrated.

Earlier P4/P5/P6 findings remain carried forward:

- **Finding 1 (choice 8, the carrier gap).** Named precisely as a third
  reader change — see "The conclusion carrier" and section 4. Still
  **specified, not built**: no production code changes this round either,
  so `determined-zero-reader-gap` reproduces the same
  `PresentationModelError` against the real, unmodified
  `presentation_projection.py` as P4 found.
- **Finding 2 (choice 4, uncertainty folded into outside coverage).**
  P5 repaired uncertainty about ownership, residence and the sole-obligor
  statement (`no-one-else-owes-it`); P6 adds collateral and payment. Each
  gets its own reason category —
  `cannot-tell-ownership`, `cannot-tell-residence`, `cannot-tell-share`,
  `cannot-tell-collateral`, and `cannot-tell-payment` — checked after every
  earlier decisive and specific condition, so a genuine
  refinance or second property beside an uncertain identity answer still
  reaches the generic residual unchanged. **P5 repair, probed**
  (`cannot-tell-ownership-alone`, `cannot-tell-residence-alone`,
  `cannot-tell-share-alone`, and `uncertain-ownership-against-refinance`,
  reconfirmed); P6 adds standalone `cannot-tell-collateral` and
  `cannot-tell-payment` cases.
- **Finding 3 (choice 3, the personal-expense zero ships without
  grandfathering checked).** **Repaired.** See "Grandfathering" below.
- **Finding 4 (choice 1, the spouse finding).** P5 clarified liability;
  P6 puts the joint-return interpretation in all three question texts and
  probes the responding-spouse case in section 8.
- **Finding 5 (choice 11, the box 9 successor).** **Repaired.** Box 9 gets
  a genuine new fact-type version — `v2`, `optional_default` added — not a
  same-id-version substitution of the real, published v1. See "The nine
  statements" and section 7.
- **Finding 6 (constructive payment, known limitations).** **Repaired.**
  Added to the Track 0 closure's known-limitations declaration.

First round, by finding:

- **Finding 1 (debt limit).** Repaired. The line 8a value `ref`s box 2
  directly instead of collecting it from a family box 2 is not a member
  of. **Probe result:** box 2 `800000` now blocks `VALUE_INVALID`. The
  adopted v42 rule is not repaired; its defect is recorded in
  the milestone process log. Box 3's date stop is **not** repaired
  this round: `rule-artifact.v13`'s expression vocabulary has no
  date-comparison op. That successor is named in section 7 and is not
  built. Box 3 stays required and unread for the supported arm, as the
  adopted rule already treats it. **Changed this round (choice 3):** the
  personal-expense zero's own relationship to box 3 is now explicit —
  see "Condition table" and section 7's date-prerequisite recommendation.
- **Finding 2 (naming the stop) and finding 4 (unresolved sentences).**
  Repaired together. A per-statement rule,
  `tax.us.2025.rule.f1098-residence-interest-reason`, publishes exactly one
  category, modelled on the published
  `tax.us.2025.rule.sli-statement-support-reason` precedent. Each reason's
  sentence is a `description` on that category's value, read by the
  existing `_selection_blocked_reasons` declared-read mechanism. **Changed
  this round (choice 8):** that one mechanism is now too coarse — see
  "The conclusion carrier" in section 2.
- **Finding 3 (liability and payment).** Repaired, **then changed this
  round (choice 1).** The first round's repair let an owner who paid but is
  not on the note reach the supported arm. The owner's review found that
  the coverage condition (`no-one-else-owes-it` is the person's own share,
  not a statement about who holds the note) does not actually establish
  that case, and withdrew the claim. `owes-the-loan` is now a gate: that
  owner reaches `owner-not-on-note`, outside coverage with its own
  explanation (Treas. Reg. § 1.163-1(b) still may allow the deduction; this
  route does not compute it). **P4 repair, probed:** confirmed directly
  (`owner-not-on-note`).
- **Finding 5 (box 9).** Repaired. Box 9 gains an `optional_default` of `1`,
  bound once at the package's `input_bindings`. **Probe result,
  reconfirmed this round:** an omitted box 9 still publishes line 8a
  (`20000`) under the P4-repaired rules.
- **Finding 6 (double match).** Repaired by one rule, not four, for both
  the amount and (now) the reason symbol. The Schedule A attachment's own
  itemization ties out `tax.us.2025.schedule-a.line8a` through
  `presentation_projection._one_row`, which refuses any symbol with more
  than one disposition row. **Probe result, reconfirmed this round:** a
  deliberate second producer is `inapplicable` when the attachment is
  inapplicable (`double-match-zero`) and raises `PresentationModelError`
  when the attachment is required (`double-match-qualifying`). **P4
  repair, probed:** two independently decisive adverse facts true at once
  (`not-collateral` and personal-expense use; personal-expense use and a
  received certificate) each still publish exactly one conclusion, by the
  one rule's own fixed priority order, never a runner-level guard
  collision — confirmed directly.
- **Finding 7 (certificate polarity).** Repaired. The fact is renamed
  `mortgage-credit-certificate-received`, with values `received`,
  `not-received`, `cannot-tell`.
- **Track 0 adversarial closure.** Revised again this round; see below.

This round's corrections, by choice, are in the sections they change: the
condition table's uncertainty routing in "Condition table (choice 9)"; the
two ordinary timing questions and their answer mappings in section 1 and
"Which arm publishes"; the third reader change in
section 2 and section 4; liability's spouse wording in "Which arm
publishes"; the box 9 successor and the renumbered release in section 7;
the recording operation's acceptance cases in section 8.

No production code, published schema, adopted content, or fixture is
changed by any round. The sections below keep the original structure; each
changed point is marked **Proposal** (not yet probed), **Probe result**
(`p3_probe.py`), **P4 repair** (`p4_probe.py`), or **P5 repair**
(`p5_probe.py`).

## What the person experiences

A person has one Form 1098 for one loan on the home where they live. They
say, in ordinary words, whether they own that home, whether they live there
most of the time, whether the home is collateral, whether they owe the loan
and paid the interest, whether anyone else owes it, what the borrowed money
paid for, whether this is the original loan, and whether they received a
mortgage credit certificate. They can answer "can't tell" on any of those.
The application decides the tax consequence. On a clear purchase it can
deduct the reported interest. On a clear unrelated personal expense it
deducts none of that interest and the return continues, so the standard
deduction can be chosen. If they cannot tell, or the account is a refinance,
a shared loan, a second home, or another use, the application says which
condition is open and does not compute a home-mortgage deduction. They can
correct an answer or take it back. Taking back an answer the application
already used never increases the deduction. A supported result shows the
statements, the conclusion, the debt-limit assumption, and the conditions
left with them.

## 1. Ordinary statements and identity

### The tie

**Proposal.** Every new statement uses the Form 1098 vocabulary's own
identity keys, and no others:

| Key | Kind | Value |
| --- | --- | --- |
| `payer` | entity | `tax.us.mortgage-lender` |
| `statement` | entity | `tax.us.1098-statement` |
| `tax-year` | literal | `2025` |

**P0–P2 finding.** `f1098.bundle.json` keys `tax.us.2025.f1098.liable-and-paid`
and the other statement facts by those three names. The vocabulary records
no property address: boxes 7 and 8 are absent. `_statement_label` reads
`lender` and `statement`. `_sli_statement_identity` requires non-empty
`lender`, `statement`, and `tax-year`. A Form 1098 fact id therefore has no
`lender` key. P2 recorded that a blocked sentence still attaches, with the
fact id as the fallback, and that the lender label stays empty.

**Proposal.** Do not add a `lender` key, a borrower key, a home key, or a
borrowing key.

- The statement is tied to its Form 1098 by equality of `payer`,
  `statement`, and `tax-year` with that form's box facts. Box 1 and an
  ordinary answer are different fact types on the same keys, so correcting
  one does not rewrite the other.
- The statement is tied to its borrowing by being the only borrowing this
  route records for that Form 1098. The opening case is one borrowing.
- The statement is tied to its home by the ownership, residence, and
  security answers on those same keys. The home is the home those answers
  describe. There is no address to store.
- Two Form 1098 statements do not share a fact id. An answer on one cannot
  correct the other. The box 1 count still refuses to compute two of them.
  Identity does not merge the accounts, and it does not lift the count.
- A second home, or a second borrowing on one statement, is not given a
  key. Those accounts stay outside this route. A later route that needs
  them adds a key on a successor fact type. It does not reinterpret these
  three.

**P0–P2 finding, and why the smaller tie is enough.** The student-loan
inclusion adds `borrowing` and joins with ADR 0076 Part 2
`joined_contains_subject`. ADR 0075 `link_coverage` then reduces the links
of one subject. ADR 0076 Part 3, a borrowing-only join, is still open.
Choice 1's ordinary mortgage statement does not need the student-loan
recorder. Adding a borrowing key here would invent a citizen the plan does
not presume, and it would put a live relationship under ADR 0077 Part 5's
write refusal. Section 5 says Part 5 does not apply to this tie. The
`lender` name is a label read. Keying findings by it would miss every
existing Form 1098 finding, which the P3 planning review already recorded.

**Proposal.** "One home" is this reading, not a fact the person affirms
and not an assumption about an unrecorded address. One current Form 1098
whose box 9 is 1, together with one set of home answers on its keys, is
the one home. The person is not asked to affirm
`tax.us.2025.f1098.single-mortgage-single-home`. P2's gap — no home fact
on the adopted path — is closed by these answers, not by a home citizen.

### The nine statements

**Proposal, revised for finding 3.** Nine new `fact-type.v2` citizens, each
version `v1`, `nature` `determinable`, supersession `policy` `free`. Titles
say they are the person's ordinary answer and not a legal conclusion. They
are new ids. They are not renames of the eight adopted confirmations, and
they are not edits of `f1098.bundle.json`. The stored uncertain value is
`cannot-tell`, the spelling the student-loan answer facts already use.

The design review's finding 3 found that the original eighth statement,
"I owe this loan, and I paid this interest," joined liability with
payment into one value, so a `no` could mean either and the determined-zero
arm could not tell which. It is now two statements: `owes-the-loan` and
`paid-the-interest`. Its negative publishing arm now means neither filing
spouse paid any and nobody paid any for them; third-party/partial payment
and uncertainty are separate answers (section 2). Liability is a gate on the supported arm. On a joint
return, all three statements below concern the filing unit: either spouse
may owe the loan or pay the interest, and a spouse is excluded from "anyone
else" in the sole-obligor question. An owner who paid without either spouse
owing the loan is the separately named `owner-not-on-note` case, not a zero.
This keeps Treas. Reg. § 1.163-1(b) visible without implying that the bounded
route computes that case.

Correction of any of them is a later assertion of the same fact id.
**Adopted fact.** ADR 0041 `free` admits it. **P0–P2 finding.**
`_finding_corrections` then displaces the earlier finding with reason
`correction`. Withdrawal is not that assertion. **Adopted fact.** ADR 0073:
a retraction names one finding, ends its current support, supplies no
replacement, and asserts no opposite claim. What withdrawal does to the
result is section 5.

| Fact type | What the person is saying | Values | What it concerns |
| --- | --- | --- | --- |
| `tax.us.2025.f1098.owns-the-home` | "I own this home." | `yes`, `no`, `cannot-tell` | An ownership interest in the home this statement describes. Supports the ownership Publication 936 requires before home-mortgage interest is deductible. It is not `qualified-main-home`. |
| `tax.us.2025.f1098.lives-there-most-of-the-time` | "This is the home where I live most of the time." | `yes`, `no`, `cannot-tell` | Main home for this opening case. `no` may still be a second home. It is not a second-home election and not `qualified-main-home`. |
| `tax.us.2025.f1098.home-is-collateral` | "The home is collateral for this loan. The lender can take the home if I do not pay." | `yes`, `no`, `cannot-tell` | Secured debt. The form's address is not recorded, so security comes from the person. There is no adopted security confirmation. |
| `tax.us.2025.f1098.owes-the-loan` | "I (or my spouse, if we file jointly) owe this loan." | `yes`, `no`, `cannot-tell` | Liability for the filing unit. For a joint return, either spouse owing the loan is a `yes`; a spouse is not treated as an unrelated co-borrower. A `no` with payment by the filing unit is the outside-coverage `owner-not-on-note` case. |
| `tax.us.2025.f1098.paid-the-interest` | "Who paid the interest reported on this statement? If you file jointly, include payment by either spouse." | `yes`, `paid-by-others-or-partial`, `no`, `cannot-tell` | `yes`: the filer or joint-filing spouse paid all. `paid-by-others-or-partial`: someone else paid some or all for them, or the filing unit paid only part; this route leaves treatment unresolved. `no`: neither filing spouse paid any and nobody paid any for them; this is the bounded determined-zero case. `cannot-tell`: they cannot establish which description applies. No payer identity, allocation, or gift-law determination is recorded. |
| `tax.us.2025.f1098.no-one-else-owes-it` | "No one besides me (or my spouse, if we file jointly) owes this loan with us." | `yes`, `no`, `cannot-tell` | The filing unit's own share. A joint-filing spouse is not "someone else"; `no` leaves other co-obligors outside this route. It is not a share calculation. |
| `tax.us.2025.f1098.what-the-money-paid-for` | What the borrowed money paid for. | `bought-the-home`, `unrelated-personal-expense`, `other`, `cannot-tell` | The proceeds story. The application classifies acquisition indebtedness. It is not `acquisition-debt-use`. |
| `tax.us.2025.f1098.this-is-the-original-loan` | "This is the original loan." | `yes`, `no`, `cannot-tell` | Whether the borrowing is the original loan. `yes` makes `no-refinance` and `no-balance-increase` inapplicable. Silence is not a `yes`. A purchase story is not this answer: a refinanced purchase can still be acquisition debt. |
| `tax.us.2025.f1098.mortgage-credit-certificate-received` | "I received a mortgage credit certificate for this loan." | `received`, `not-received`, `cannot-tell` | **Revised for finding 7.** Presence of a §163(g) reduction, renamed from `no-mortgage-credit-certificate` so no value reads backwards: the review found that a later reader of the old id could take its `no` to mean "no certificate," the favourable case, when `no` meant the opposite. `not-received` is the publishing-favourable value. It is not `no-mortgage-interest-credit`, and it is not an assumption. |

**P4 repair, revised this round (choice 3).** Two further ordinary
statements, asked only when `what-the-money-paid-for` is
`unrelated-personal-expense` — the only use value a timing answer can
still reclassify (see "Condition table" below). Both are the same identity
keys and the same `cannot-tell` spelling as the nine above. **P5 repair
(owner finding 1):** each gains a fourth, **reserved** value, `not-asked`
— the question text below is exactly what the person sees; `not-asked` is
never an option the recording operation offers (section 8), only the
package's own structural default for a question that was never asked or
whose answer was withdrawn.

| Fact type | What the person is saying | Values | What it concerns |
| --- | --- | --- | --- |
| `tax.us.2025.f1098.loan-timing-relative-to-purchase` | "Was this loan taken out within 90 days before or after buying this home?" | `yes`, `no`, `cannot-tell`, `not-asked` (reserved) | `yes` includes either direction. Publication 936 (2025), page 12, allows the 90-day purchase relation even when the money did not buy the home. |
| `tax.us.2025.f1098.loan-timing-relative-to-building-or-improving` | "Was this loan taken out before you finished building or improving this home, or within 90 days after you finished?" | `yes`, `no`, `cannot-tell`, `not-asked` (reserved) | `yes` covers a loan made before completion or no more than 90 days afterward. The question uses the loan-money release date. |

Nearby help for both questions: "Include unfinished or paused projects and
preparation before physical work began. Use when the loan money was released.
If an earlier written application could change your timing answer, choose
'can't tell'." `not-asked` is a reserved package default, never an answer
option offered to the person.

**Checked against Publication 936 (2025), page 12 (owner finding 2,
action 4). Completion timing and the expense cap are separate tests. The
question deliberately errs toward including a possible project exception:
it asks about building or improving without asking the person to decide
whether the work was "substantial." Routine repair can therefore answer
`yes` even though the tax rule may not treat it as a substantial improvement.
That answer leaves the account open; it does not establish acquisition debt.
The completion answer is not extended by the separate 24-month expense
window.

| Circumstance and ordinary answer to the exact question | Stored answer | Observed coordinator result |
| --- | --- | --- |
| Work finished 18 months before the mortgage; "No." | Building timing `no`; purchase timing `no` | `use-unrelated-personal-expense`, line 8a `0`. Completion is outside the 90-day-after interval. |
| Work finished 26 months before the mortgage; expenses began 30 months before the mortgage (4 months before completion); "No." | Building timing `no`; purchase timing `no` | `use-unrelated-personal-expense`, line 8a `0`. The 24-month expense cap does not lengthen the completion interval. |
| Work still under way when the mortgage money is released; "Yes." | Building timing `yes`; purchase timing `no` | `timing-exception-possible`; line 8a remains unresolved. The expense cap is not computed. |
| Work finished 40 months before the mortgage; "No." | Building timing `no`; purchase timing `no` | `use-unrelated-personal-expense`, line 8a `0`. |
| Work finished exactly 90 days before the mortgage; "Yes, within 90 days after finishing." | Building timing `yes`; purchase timing `no` | `timing-exception-possible`; line 8a remains unresolved. |
| Work finished 91 days before the mortgage; "No." | Building timing `no`; purchase timing `no` | `use-unrelated-personal-expense`, line 8a `0`. |
| Project paused and unfinished when the mortgage money is released; "Yes, I had not finished." | Building timing `yes`; purchase timing `no` | `timing-exception-possible`; line 8a remains unresolved. |
| Loan money released during preparation, before physical work begins; "Yes, I had not finished." | Building timing `yes`; purchase timing `no` | `timing-exception-possible`; line 8a remains unresolved. |
| An earlier written application could change the answer; "I can't tell." | Building timing `cannot-tell`; purchase timing `no` | `cannot-tell-timing`; line 8a remains unresolved, distinct from a `no`. |
| Home bought 42 days before the mortgage; "Yes, within 90 days after buying." | Purchase timing `yes`; building timing `no` | `timing-exception-possible`; line 8a remains unresolved. |
| Mortgage taken 45 days before buying the home; "Yes, within 90 days before buying." | Purchase timing `yes`; building timing `no` | `timing-exception-possible`; line 8a remains unresolved. |

The probe records each ordinary answer beside the asserted stored value and
the coordinator output. The completion cases show that no qualifying
completion exception is cleared by a `no`; the `yes` cases stay open rather
than claiming that the exception's expense cap or substantial-improvement
test is met. Purchase wording covers both directions. These are prototype
coordinator results from direct synthetic findings, not evidence of a
production question/recorder/reader.

**P5 repair (owner finding 1).** Both timing facts are deliberately **not**
in either rule's `requires` as a *conditional* dependency; see "Condition
table" and section 7 for why a subject-scoped rule's `requires` cannot be
conditional at all (ADR-0037's `conditional_dependency_set` was assessed
and set aside: it only governs evaluation inside `value`, not which types
`subject_dispatch` joins into a subject's row in the first place), and the
`optional_default` each one gets instead. That default is now the
**reserved sentinel `not-asked`**, not a favourable real-world value: the
first round's "more than 90 days" / "no building work" defaults were
withdrawn by the owner's review (design account, "earlier choice changed by
new evidence") because they let an unanswered account quietly clear the
exception, the same shape as an assumption choice 5 rules out. `not-asked`
is never that — it is routed, inside "Which arm publishes," to its own
open-condition reason (`timing-not-established`), never to the zero and
never to `cannot-tell-timing`'s sentence, so the explanation never claims
the person said "can't tell" when they were simply never asked, or
withdrew what they said. **P5 repair, probed:** a purchase account never
asks either question and is unaffected (`supported-purchase`,
`purchase-account-timing-questions-unasked`); a personal-expense account
with neither timing question answered reaches `timing-not-established`
(`personal-expense-no-timing-answers`); one answered and one absent reaches
the same category (`personal-expense-one-timing-answer-missing`); a
favourable answer given and then withdrawn returns to `not-asked`, not to
the missing row other statements fall to, and reaches
`timing-not-established` again, not the zero it would otherwise have
reached (`personal-expense-timing-withdrawn`).

Original statement, before this revision: `tax.us.2025.f1098.owes-the-loan-and-paid-the-interest` ("I owe this loan, and I paid this interest.") and `tax.us.2025.f1098.no-mortgage-credit-certificate` ("I did not receive a mortgage credit certificate."). Neither id is used by this revision; both are superseded in this draft, not published, so nothing is retracted.

`other` on the use fact is one value for a known story that is neither arm:
building, a substantial improvement, mixed use, business or investment use,
or a purchase-and-borrowing the person knows is not "I borrowed this money
to buy that home." **Proposal.** The route stores no amount and computes no
allocation. Choice 6 stays outside the computed path. This value is how the
person says so without being pushed into either arm or into `cannot-tell`.

**P0–P2 finding.** The eight adopted confirmations accept only `yes` and
`no`. A `cannot-tell` on `acquisition-debt-use` is refused before a run.
Each new fact admits `cannot-tell` so uncertainty is a stored answer. A
missing answer remains the absence of the fact, not a stored blank.

**P0–P2 finding.** Box 9 is `tax.us.2025.f1098.box9-number-of-properties`.
The adopted line 8a rule requires it and does not read it, so a count above
one can sit beside `single-mortgage-single-home` without changing the
result. **Proposal.** The new route reads box 9. A value of 1 is one
property reported on the statement. Any other number is outside coverage.
The person is not asked to affirm it. Correcting box 9 is a correction of
the statement and is re-read.

**Repaired for finding 5.** The design review ran this unrepaired and found
that `requires` alone still blocks `DEPENDENCY_ABSENT` on an absent box 9,
regardless of whether the rule's `value` ever reads it — a blank box 9 never
reached the supported or the disallowed account. The repair declares box 9's
`optional_default` as the literal `1`, bound once in the package's
`input_bindings` (`{"fact_type": {"id": "tax.us.2025.f1098.box9-number-of-properties", "version": "v1"}, "mode": "optional_default", "symbol": "tax.us.2025.f1098.box9-number-of-properties"}`),
pinned to a new parameter citizen,
`tax.us.2025.parameter.f1098-box9-default-single-property`, value `1`. This
is the same declared shape as the existing `taxpayer_over_65` /
`tax.us.2025.parameter.default-false` pair — not the retrospective's
rejected "optional, safely-defaulting" shape, because a blank box 9 is
not a completeness gap the person must answer: the Form 1098 instructions
themselves say the filer may leave it blank when only one property secures
the mortgage, so "absent" and "1" are the same real-world fact, not a
missing answer standing in for a default. The bound is scoped to this
route's own singleton-statement cardinality; a future multi-statement
capability needs its own binding, not a wider reading of this one.
**Probe result:** with box 9 omitted, `tax.us.2025.rule.f1098-residence-interest-reason`
publishes `qualified` and line 8a publishes `20000`, where the adopted
route (and this draft's first version) blocked `DEPENDENCY_ABSENT`. A
recorded box 9 other than `1` still falls through to the account's
outside-coverage reason, never to `qualified`.

**P0–P2 finding.** The payer key is the lender. It does not record the
borrower. Who owed the loan and paid the interest is now two statements,
`owes-the-loan` and `paid-the-interest` (finding 3).

### Condition table (choice 9, P4 repair, P5 repair)

For the supported conclusion and for each candidate determined zero, every
condition it needs, stated as established, adverse, uncertain, or outside
coverage. This is the one table the amount rule and the reason rule both
follow, as the priority order in "Which arm publishes." A row earlier in
the table is checked first and, where marked **decisive**, is not
reclassified by any row below it.

| Order | Condition | Established | Adverse (decisive?) | Uncertain | Outside coverage |
| --- | --- | --- | --- | --- | --- |
| 1 | Security | `home-is-collateral` `yes` | `no` — **decisive.** §163(h)(3)(B)(i)(II) requires the debt be secured by the qualified residence; no use, refinance, or grandfathering fact restores an unsecured debt to acquisition debt. A Form 1098 is the lender's report of a mortgage secured by real property, so a person's `no` beside one is conflicting information this route still takes at face value, as the person's own account of their own collateral — it does not re-derive security from the form. | `cannot-tell` — `cannot-tell-collateral`, left with the person, not a zero. This is an open answer, not outside coverage. | — |
| 2 | Payment | `paid-the-interest` `yes` | `no` — **decisive** only when neither filing spouse paid any and nobody paid any for them. This is the bounded zero. `paid-by-others-or-partial` — **not a zero and never favourable:** some/all paid by another person for the filing unit, or only part paid by the filing unit; `payment-outside-coverage`, line 8a blocked and dependent line 12e unresolved. This probe does not decide whether a particular third-party payment is legally treated as the taxpayer's. | `cannot-tell` — `cannot-tell-payment`, left with the person, not a zero. | — |
| 3 | Liability (choice 1; spouse wording, P6 correction) | `owes-the-loan` `yes` | `no` beside `paid-the-interest` `yes` — **not a zero.** Treas. Reg. § 1.163-1(b) may still allow this equitable owner's deduction; this route does not compute it. `owner-not-on-note`, outside coverage. **P6 correction:** liability, payment, and sole-obligor questions say that the joint-filing spouses answer as a unit; either spouse may owe or pay, and a spouse is excluded from "anyone else." A joint-return case where the responding spouse is not on the note but the other spouse owes and paid reaches `qualified` (section 8). | `cannot-tell` — left with the person | `owes-the-loan` `no` and `paid-the-interest` `yes`, as above |
| 4 | Use (choice 3) | `what-the-money-paid-for` `bought-the-home` | `unrelated-personal-expense` — decisive **only once** the two timing questions, original-loan/box 9, and grandfathering below also clear; see rows 5–7. Not decisive against refinancing, more than one statement or property, the two timing windows, or grandfathering — each can reclassify the same use. | `cannot-tell` — `cannot-tell-use`, left with the person | `other` (a known non-purchase story the route does not classify, e.g. a substantial improvement or mixed use) |
| 5 | Timing, when use is personal-expense (choice 3, P6 correction) | Both timing answers favourable (`no` and `no`) | Either timing answer `yes` — `timing-exception-possible`, outside coverage: the purchase relation or building/completion interval may make this acquisition debt after all. Completion timing is separate from Pub. 936's 24-month expense cap; this route does not compute that cap or decide whether improvement work is substantial. `yes` is conservative and can include non-substantial work. | Either timing answer `cannot-tell` — `cannot-tell-timing`, left with the person. Either timing answer is reserved `not-asked` (never asked, or withdrawn) and neither is `yes` or `cannot-tell` — `timing-not-established`, left with the person. | — |
| 6 | Original loan and box 9, when use is personal-expense and timing clears | `this-is-the-original-loan` `yes` and box 9 is `1` or absent | — (not an adverse fact; a `no`/other count is a coverage bound) | `this-is-the-original-loan` `cannot-tell` — its own original-loan uncertainty reason, not a known refinance | `this-is-the-original-loan` `no`, or box 9 other than `1` — named refinance/property-count coverage reasons: a refinance can carry over the old balance's acquisition status (§163(h)(3)(F)(iii)), which this route does not trace |
| 7 | Grandfathering, when use is personal-expense, timing clears, and row 6 establishes an original single-property loan (choice 3, P5 repair) | Box 3 strictly after October 13, 1987 (the `date_compare` check, `cmp: "lte"`, against the cutoff is false) | — (not itself an adverse fact; it only withholds the zero) | — | Box 3 on or before October 13, 1987 (`date_compare`, `cmp: "lte"`, true) — `possible-grandfathered-debt`, outside coverage. §163(h)(3)(D)(i)(II) and Pub. 936 (2025) p.13 ("before October 14, 1987") make the cutoff date itself grandfathered, so equality is the outside-coverage side, not the zero. Box 3 is required (unchanged) but was previously unread for this branch; it is now read only here. This check establishes a *possible* case, not every grandfathering condition — it does not verify continuous security or a later refinancing's effect. |
| 8 | Certificate | `mortgage-credit-certificate-received` `not-received` | — (reduces, does not zero, the deduction; §163(g)) | `cannot-tell` — its own certificate uncertainty reason, left with the person | `received` — `certificate-received`, outside coverage (Form 8396 not computed) |
| 9 | Debt limit | Box 2 at or under `tax.us.2025.f1098.mortgage-interest-limit` | Box 2 over the limit — `VALUE_INVALID`, `debt-limit-over`, outside coverage (the prorated amount is left with the person) | — | — |
| 10 | Ownership, residence, sole-obligor, collateral uncertainty (P5/P6, choice 4) | all `yes` | — | `cannot-tell` alone on ownership, residence, sole-obligor, or collateral gets its matching reason. Payment uncertainty is handled in row 2 before liability/use. | `no` on any, without an earlier zero already matching — folds into row 11 |
| 11 | Remaining known coverage limits | — | — | — | A `no` on ownership, residence or no-one-else gets a named coverage explanation. The residual remains only for a condition no earlier row classifies; it must not absorb a selected `cannot-tell` answer. |

**Production-review correction.** Row 3's liability uncertainty likewise
gets its own named reason. Rows 6, 8 and 11 above repair the design's earlier
conflation, not just its implementation: the v44 probe/production observations
remain historical evidence. The successor keeps all amount dispositions and
the decisive-zero precedence. Its named messages must not claim that a known
coverage limit is uncertainty, or that an unresolved condition is an adverse
tax conclusion. The production-review repair unit also gives the zero's
description its full condition-table basis; the earlier short description
did not in fact preserve all of that meaning.

Rows 1–3 are checked before use (row 4), because each is independently
decisive regardless of what the money paid for: a personal-expense answer
beside `home-is-collateral` `no` is `not-collateral`, not
`use-unrelated-personal-expense` — confirmed directly
(`not-collateral-and-personal-expense`). Rows 5–7 only matter once row 4
is `unrelated-personal-expense`; a `bought-the-home` or `cannot-tell`
answer never reaches them.

### The reason, and the inert path

**Probe result (first round), extended by P4 and again by P5 for the
condition table.** One further per-statement `fact-type.v2`,
`tax.us.2025.f1098.residence-interest-reason`, `nature` `determinable`,
same identity keys as the nine statements above. Its value is categorical:
`qualified`, or one of eighteen reasons the interest is not (yet) qualified
residence interest. The first round had seven; P4 added
`owner-not-on-note` (choice 1), `timing-exception-possible`, and
`cannot-tell-timing` (choice 3), for ten. P5 added five more;
**P6 correction** adds `cannot-tell-collateral` and
`cannot-tell-payment`; P7 adds `payment-outside-coverage`:
`timing-not-established` and `possible-grandfathered-debt` (choice 3),
and `cannot-tell-ownership`, `cannot-tell-residence`, and
`cannot-tell-share` (choice 4) — `use-unrelated-personal-expense`,
`not-collateral`, `not-paid`, `owner-not-on-note`,
`timing-exception-possible`, `cannot-tell-timing`,
`timing-not-established`, `possible-grandfathered-debt`,
`cannot-tell-use`, `cannot-tell-ownership`, `cannot-tell-residence`,
`cannot-tell-share`, `payment-outside-coverage`, `certificate-received`, `debt-limit-over`, or
`outside-coverage` (a refinance, a second property, or any other
condition this route does not compute). Each value's
`value_schema.oneOf[].description` is the sentence the person sees for
that reason — content, admitted by the existing `fact-type.v2` schema
(the published `tax.us.2025.sli.statement-support-reason` already carries
per-value descriptions this same way). No new schema. Section 2 describes
the rule that publishes it, and section 4 describes the reader that shows
its sentence, and the third reader change choice 8 still needs to show a
determined zero's sentence this way.

One further fact type, `tax.us.2025.f1098.inert-path-unwritten`, is not a
statement at all: a one-value marker nothing ever writes, the same
technique the published `tax.us.2025.sli.inert-path-unwritten` already uses
to give a two-path `rule-artifact.v13` selection its required second path
when only one real activity exists. It carries no claim and is not reused
from the student-loan pair; it is new content on the same pattern. Section
2's unresolved-field rule names it.

The return each value produces is section 2. The sentences in a supported
or disallowed result are section 3.

## 2. Conclusion and return

### The chain

**Revised for finding 6.** The first draft proposed four rules on one
symbol. The review's finding 6 asked for either an explicit
first-publisher-wins statement or fewer rules "if that removes the hazard
more simply." This revision proposes fewer: **one** rule carries every
arm, replacing the adopted line 8a body in a successor package. The
adopted citizen stays `tax.us.2025.schedule-a.line8a.rule` version `v1`,
schema `rule-artifact.v4`. The successor package does not include it.
Nothing in this draft edits that file.

**P7 delta to the P6 rule inventory:** the same reason-rule shape now has
nineteen values total (`qualified` plus eighteen non-qualified reasons),
including `payment-outside-coverage`. The next inventory row's statement
of seventeen open categories describes the P6 baseline only. P7 classifies
`paid-by-others-or-partial` before other payment/use arms and never publishes
line 8a for it.

| Rule | Schema | Publishes | When it publishes |
| --- | --- | --- | --- |
| `tax.us.2025.rule.f1098-line8a` `v3` (P5 repair, retained in P7) | `rule-artifact.v14` (P5 repair, up from `v13` — the grandfathering check's `date_compare` node needs ADR 0078's successor schema) | `tax.us.2025.schedule-a.line8a` | One nested `value`, now the condition table's priority order: literal `0` when the home is not collateral; block with `payment-outside-coverage` when someone else paid some/all or the filing unit paid only part; block on uncertain payment; literal `0` only when neither filing spouse paid and nobody paid for them; block when neither joint filer owes the loan (choice 1); continue through personal-expense timing, original-loan, box 9, grandfathering, use/certificate, qualified and box 2 checks. |
| `tax.us.2025.rule.f1098-residence-interest-reason` `v3` (P5 repair, retained in P6) | `rule-artifact.v14` (P5 repair, up from `v13`), `subject` | `tax.us.2025.f1098.residence-interest-reason` | Always, once every statement answer, box 2, box 3, and the two timing facts (by their `optional_default` when absent) are current: the same priority order as above, ending in the category `qualified` or one of seventeen open-reason categories, never a block. Box 3 joins `requires` for the first time in P5 (finding 1's repair left it required-but-unread; P5 reads it, only inside the personal-expense/original-loan/box-9-clear branch). P6 adds the two standalone collateral/payment uncertainty categories to that existing content rule. Dispatched per subject (ADR 0077's subject-scoped primitive), so its publication is `symbol|subject_fact_id`-keyed and does not itself feed the line 8a rule above — the two rules read the same input facts independently and agree by construction, not by one reading the other's output. |

**P4 repair, found by probing a split rule and rejecting it.** A first
attempt split the reason rule into two disjoint-guarded rules (use ==/!=
unrelated-personal-expense), on this corpus's own
`schedule-a-total`/`schedule-a-total-closed-empty` precedent, so that only
the personal-expense-guarded rule would need the two timing facts in its
own `requires`. **Probe result:** this fails a second, unrelated
constraint — the unresolved field's declared read
(`reads_subject_results`) requires exactly one rule publishing the read
symbol for the subject type; two REASON producers make
`build_presentation_model` raise `PresentationModelError: declared read
... has no single publisher` for every case, including ones with no
double-match question at all. The repair instead keeps REASON as one
rule and gives both timing facts a structural `optional_default` (see
"Condition table" and section 7): a subject-scoped rule's `requires` is
the *exhaustive* join set for every subject it dispatches over
(`packages/derivation/subject_dispatch.py`'s shared-key join) — a fact
outside it is never available to any subject, not merely "available but
possibly absent" the way an ordinary (non-subject) rule's `value` can
safely `ref` a fact outside `requires` and let the runner's own
`EvalBlocked` catch it. **Probe result:** confirmed this difference
directly — the line 8a rule (not subject-scoped) read both timing facts
outside its `requires` without issue in an earlier probe attempt; the
reason rule (subject-scoped) did not, until the facts' own defaults were
added.

**Probe result.** A single rule removes the double-match hazard by
construction: there is exactly one producer, so no guard collision is
possible, and `p3_probe.py`'s `double-match-zero`/`double-match-qualifying`
cases exist only to probe what a *second* producer would do if someone
proposed one anyway (see "Which arm publishes" and finding 6's note
below). The probe found a second, independent reason to prefer one rule
over four, beyond the double-match question the charter asked about: the
Schedule A attachment's own itemization (`attachment.schedule-a.json`)
ties out this exact symbol through `presentation_projection._one_row`,
which raises `PresentationModelError` for any symbol with more than one
disposition row — regardless of whether the extra row is a true conflict
loser or simply a second rule that was merely *attempted*. `double-match-zero`
(the attachment inapplicable; the extra producer's row never reaches
`_one_row`) completes normally, first-publisher-wins, exactly as the
charter's finding 6 describes. `double-match-qualifying` (the attachment
required, because line 8a publishes a nonzero amount) raises
`PresentationModelError: missing or ambiguous disposition join for symbol
'tax.us.2025.schedule-a.line8a': 2 row(s)` the moment a second producer
exists, independent of which guard wins. Four independent producers are
therefore not merely a double-match risk on this symbol; they are
incompatible with the existing attachment the moment Schedule A is
actually required. One rule is the only shape this probe found that
composes with the attachment as it stands.

**P0–P2 finding, read again.** `tax.us.2025.schedule-a.line8a` is not
form-field-bound, so `_one_row`'s cardinality bound was not visible from
the form-field path the first draft checked. It reaches this symbol
through the Schedule A attachment's itemization instead, which the first
draft did not trace. The basis section in section 4 reads the publication
directly. It does not bind a form field to this symbol.

**Adopted fact, carried unchanged.** `tax.us.2025.rule.form1040-line12e`
version `v1`, schema `rule-artifact.v4`, still publishes
`tax.us.2025.deductions.line-12e`. When the no-statement flag is false and
box 1 count is not 0, its value refs `tax.us.2025.schedule-a.line8a`. When
the flag is true and the count is 0, it takes the itemized input, which
the closed-empty producer has set to 0, and `max` selects the standard
deduction. When the flag is true and the count is not 0, it blocks
`F1098_SCOPE_CONTRADICTION`. **P0–P2 finding.** `tax.us.2025.rule.schedule-a-total`
version `v1` requires line 8a and is the count-greater-than-0 producer.
`tax.us.2025.rule.schedule-a-total-closed-empty` version `v1` is the count-0
producer. Line 12e and both total rules keep those ids and versions.

**Proposal.** The one line 8a rule, and the reason rule separately, each
put every fact their own `when`/`value` read into `requires`, including a
dependency that is only sometimes the source of the number. An empty
`requires` list is not used. The closed-empty shape is the adopted one:
`require_closed` on `tax.us.2025.f1098`, then a count greater than 1
blocks `MULTIPLE_F1098_OUT_OF_SCOPE` on the line 8a rule's own `when`
(its only guard branch now; the three zero arms sit in `value`, not in
`when`, so they no longer need their own copy of the count-equals-1
compare). **P0–P2 finding.** Closed-empty is inapplicable on line 8a even
though v1 lists the eight confirmations in `requires` and the fixture does
not assert them. The successor keeps that shape: on a closed-empty family
the count compare's guard preflight is false before any of the nine new
`requires` entries are even checked, so closed-empty stays inapplicable,
not a block. Demonstration 6 re-measures the row. The reason rule is not
attempted on a closed-empty return either, because `require_closed` plus
`count == 1` on this corpus's existing subject-scoped `_scope` join means
there is no box 1 subject to dispatch it over at all.

**Revised for findings 2 and 4.** The second rule, carrying every
sentence for a row that publishes no line 8a, is unchanged in role from
the first draft but changed in mechanism:

| Rule | Schema | Publishes |
| --- | --- | --- |
| `tax.us.2025.rule.f1098-residence-interest-unresolved` `v1` | `rule-artifact.v13` with `selection` | `tax.us.2025.f1098.residence-interest-unresolved` |

**Proposal.** One `form-field.v3`,
`tax.us.2025.form.f1098.residence-interest-unresolved`, binds that symbol.
One producer, so the form-field join stays singular. Top-level `requires`
and `pins` are empty, and top-level `when` is true, as ADR 0077 Part 4
requires of a v13 selection rule. The **first** path, `statement`, is
`source_nonempty` on box 1 and declares one `reads_subject_results` entry
on the reason rule's symbol, subject box 1. Its own `requires` is `[]`
(the design review's finding 4 found that a declared read is not an
ordinary `requires` name, and `p3_probe.py`'s first attempt at a nonempty
`requires` here failed `RULE_SELECTION_DEPENDENCIES_INVALID`); its `when`
is `not(collect_categorical_all_equal(reason, "qualified"))`, true exactly
when the statement's reason is not `qualified`; its `value` is a bare
`block DEPENDENCY_ABSENT`. The **second** path, `inert`, is
`source_nonempty` on `tax.us.2025.f1098.inert-path-unwritten`, is never
active (nothing writes that fact), and exists only because
`rule-artifact.v13`'s selection schema requires at least two paths — the
same `minItems: 2` the published `tax.us.2025.rule.sli-worksheet` already
satisfies with its own inert second path. The default, when box 1 is not
current, has a false `when`: the field is inapplicable on a closed-empty
return and does not block line 12e. When line 8a publishes (reason
`qualified`), the active path's own `when` is false for the same reason:
the field is inapplicable, and the reason rule's own publication — read
through the basis in section 4 — is the account the person sees.

**Probe result.** `_selection_blocked_reasons` fills `resolved.reasons`
from the active path's declared read without any reader change: the
reason rule publishes a category (never a bare block), so the "declared
read" branch applies — for each current subject, a published value other
than the declaration's favourable literal (recovered from the
`collect_categorical_all_equal` node `_favorable_values` scans for) gives
that value's own `fact-type.v2` `description` as the sentence. The
over-limit, can't-tell, and refinance cases below show three different
descriptions reaching the person this way. A fact truly missing — none of
the nine statements ever answered — makes the reason rule itself block
`DEPENDENCY_ABSENT` before it can classify anything; that falls to the
"no single result" branch of the same reader, which supplies the reason
rule's own declared `wording` as a generic fallback sentence. The v42
package already admits `rule-artifact.v13`, `form-field.v3`, and
`fact-type.v2`'s `oneOf` descriptions (the published SLI content already
uses all three). Today's line 12e producer is `rule-artifact.v4`, and its
blocked explain text is the word "blocked", so the sentence still does not
go on line 12e — unchanged from the first draft's decision in section 4.

### The conclusion carrier (choice 8, P4 repair)

The first round's own repair above has a defect the owner's review
caught: the active path's `when`, `not(collect_categorical_all_equal(reason,
"qualified"))`, is favourable to exactly one value, `qualified`. Every
other reason — including the three now-determined zero reasons
(`use-unrelated-personal-expense`, `not-collateral`, `not-paid`), which
are completed conclusions, not open questions — is still shown through
this same blocked field. That is exactly what choice 8 forbids: "a
completed conclusion is never shown through the blocked-result field,
which is only for results that cannot finish."

**Probe result, this round.** The fix this round tried first is content
only: widen the path's `when` to `not(any(four collect_categorical_all_equal
checks))`, one per determined value. This changes which rows the field
is *active* for (confirmed: a personal-expense row's path becomes
`guard_inapplicable`, not `blocked`, exactly as choice 8 wants). But the
same declaration's `reads_subject_results` entry is read a second time,
inside `_selection_blocked_reasons`, by `_favorable_values` — which scans
the declaration for every `collect_categorical_all_equal` node naming the
read symbol and requires **exactly one** result (`presentation_projection.py`,
the `len(favorable) != 1` check). Four nodes fail that check. **Probed
live, against the real, unmodified module:** a case where the path is
genuinely active (`cannot-tell-use`, not one of the four favourables)
raises `PresentationModelError: declared read
'tax.us.2025.f1098.residence-interest-reason' has no single expected
value` — reproduced by `p4_probe.py`'s `determined-zero-reader-gap` case.
A personal-expense case was tried first and did *not* reproduce the
error, because that path's own `when` is already false for it (the
reason is one of the four favourables), so `_selection_blocked_reasons`
is never reached at all for that row; the gap is specifically in the
sentence-building code, not in path activation.

**Consequence.** This round's repair can correctly make the unresolved
field *inapplicable* for the three determined zero reasons (content only,
no code change), but it cannot yet show those three reasons' sentences
through any carrier other than the blocked field, because the one
general carrier the first round found (`_selection_blocked_reasons`)
assumes a single favourable value and a determined zero is not an
unfavourable one. Section 7 names and costs the smallest additive fix
(generalise the check from "exactly one" to "one or more") as a second,
small reader change alongside the general basis loader section 4
already proposes. Until it lands, this design keeps the three
determined zero reasons' sentences on the blocked field — a known,
named limitation, not a silent one — and recommends against building a
production charter around a mechanism that still conflates a completed
zero with a genuinely open question.

**The third reader change (P5 repair, P4 re-review finding 1).** The two
fixes above are not sufficient together, and the design must say so rather
than imply a determined zero is already shown correctly once they land.
Tracing the combination against the real code: once the unresolved field's
`when` is widened (fix one) and `_favorable_values`' "exactly one" check is
loosened (fix two), a `not-collateral`, `not-paid`, or
`use-unrelated-personal-expense` row's unresolved-field path becomes
`guard_inapplicable` — and a `guard_inapplicable` row never populates
`resolved.reasons` at all (`presentation_projection.py`'s field-resolution
code only calls `_selection_blocked_reasons` when the row's own disposition
is `blocked`, section 4's "Show the basis of whatever rule a result pins").
Section 4's own general basis-section gate, meanwhile, only builds a line
8a section "when the publication's pins include
`tax.us.2025.f1098.mortgage-interest-limit`" — which the three
decisive-zero reasons never pin, by construction (they publish a literal
`0`, not a collected, limit-compared amount). So once both named fixes
land exactly as specified, a determined zero gets **neither** the
blocked-field sentence **nor** a basis section — a silent account, worse
than today's mislabeled-but-visible one, and squarely against choice 8's
completion test. The smallest third change: widen the basis-section gate
in section 4 to also build a section for a literal-zero publication whose
reason is one of the three decisive-zero categories, assembling its
`said`/`derived`/`left_with_person` content from that reason's own
`description` — the exact narratives section 3's "The three disallowed
reasons" already drafted — rather than from the line 8a rule's own
`basis` object (which stays reserved for the supported narrative, section
3). This is still pure Python in `presentation_projection.py`, no schema
successor, and still **specified, not built**: no production code changes
this round. `determined-zero-reader-gap` (`p5_probe.py`) reproduces the
same `PresentationModelError` against the real, unmodified module as P4
found, confirming the underlying gap is unchanged by this round's content
work.

### Which arm publishes

**Revised for findings 1, 3, and 5; re-ordered this round for the
condition table (choice 9, P4 repair).** Counts and closure are the
adopted gates. Box 9 equal to 1 (or absent, by its `optional_default`,
finding 5) is required on every publishing arm except arms 1–3 below,
which read box 9 nowhere (see the condition table: security, payment, and
liability are decisive before box 9 is even relevant). Filing status is
required because the limit parameter is keyed by it. A missing filing
status is the missing row. The one rule's `value` tries each arm in this
order, first match wins (an ordinary nested `choose`, not a selection
among competing rules) — this is the condition table above, read as a
priority list:

1. **Disallowed, security.** Collateral is `no`: literal `0`. **P0–P2
   finding.** P1 pairs "the home is not collateral" with the same
   return-level choice as a determined disallowance, and the opening case
   has no other deduction category to publish. Checked first because it
   is decisive over every other condition, including use — confirmed
   directly (`not-collateral-and-personal-expense` still publishes
   `not-collateral`, not the personal-expense zero).
2. **Payment.** Not matched above, `paid-the-interest=paid-by-others-or-partial`
   gives `payment-outside-coverage` and blocks (no line 8a amount);
   `cannot-tell` gets its own blocked reason; only `no`—neither filing
   spouse paid any and nobody paid any for them—publishes literal `0`.
3. **Outside coverage, owner not on note (choice 1, P4 repair).** Not
   matched above, and `owes-the-loan` is `no` while `paid-the-interest`
   is `yes`: block. The first round's repair let this case reach the
   supported arm; the owner's review found no condition in this account
   that actually establishes the equitable-ownership fact Treas. Reg.
   § 1.163-1(b) needs, so the claim is withdrawn. This person may still
   deduct the interest they paid, but this route does not compute it —
   confirmed directly (`owner-not-on-note`).
4. **Disallowed or outside coverage, personal-expense use, timing, and
   grandfathering (choice 3, P4–P6).** Not matched above, and use is
   `unrelated-personal-expense`: if either timing answer is `yes`, block
   (`timing-exception-possible` — confirmed directly,
   `pub936-example1-investment-other` (outside coverage; the separate
   personal-expense purchase-window analogues follow),
   `pub936-situation2-building-before-completion`, and
   `pub936-situation3-mortgage-after-completion`); if either timing fact is
   `cannot-tell`, block (`cannot-tell-timing`); if either timing answer is
   the reserved `not-asked` (never asked, or withdrawn) and
   neither is unfavourable or `cannot-tell`, block
   (`timing-not-established` — confirmed directly,
   `personal-expense-no-timing-answers`,
   `personal-expense-one-timing-answer-missing`, and
   `personal-expense-timing-withdrawn`); otherwise, once
   `this-is-the-original-loan` is `yes` and box 9 is `1` or absent — **P5
   repair:** block if box 3 is on or before October 13, 1987 (the
   grandfathering check, `date_compare`, `cmp: "lte"` — confirmed directly,
   `personal-expense-grandfathered-on-cutoff` and
   `personal-expense-grandfathered-before-cutoff`), else literal `0`
   (confirmed directly, `personal-expense-clean` and
   `personal-expense-not-grandfathered-after-cutoff`); otherwise block (a
   refinance or a second property — confirmed directly,
   `personal-expense-refinance` and `personal-expense-two-properties`,
   both `outside-coverage`).
5. **Unresolved, use.** Not matched above, and use is `cannot-tell`:
   block (`cannot-tell-use`).
6. **Outside coverage, certificate.** Not matched above, and the
   certificate is `received`: block.
7. **Supported.** Not matched above, and every other answer is favourable
   — owns `yes`, lives `yes`, collateral `yes` (redundant with arm 1's
   guard but kept explicit), `owes-the-loan` `yes` (**new gate, choice
   1**), `paid-the-interest` `yes`, no-one-else `yes`, use
   `bought-the-home`, original-loan `yes`, certificate `not-received`,
   box 9 equal to 1 (or absent). **Repaired for finding 1.** The value
   then `ref`s box 2 directly — not `collect`s it from the
   `tax.us.2025.f1098` family, whose declared member predicate is box 1
   only, which is why the adopted rule's compare always saw an empty
   collected list. Box 2 over the limit for the filing status: block
   `VALUE_INVALID`, publishing none of box 1. Box 2 at or under the limit:
   publish collected box 1. That publication is the debt-limit assumption
   in choice 7: one date's principal stands for the year's balance, and
   the whole reported interest is deducted, with no proration. **Probe
   result:** box 2 `800000` now blocks `VALUE_INVALID`, where the adopted
   rule (and this draft's first version) published the whole box 1
   regardless.
8. **Everything else blocks `DEPENDENCY_ABSENT`.** A refinance
   (original-loan `no` or `cannot-tell`), a second property, or any other
   open condition among the nine statements that no earlier arm already
   classified — none of these reaches an earlier arm or the supported
   arm's conjunction, so the rule falls to this last branch rather than to
   a `missing` list the `block` op cannot carry (finding 2). The reason
   rule (this section's companion) independently classifies the same
   input into a specific category, and its sentence is what the person
   sees (section 4) — the dollar rule's own block carries no
   distinguishing payload, by design, because the reason rule already
   carries it. **P5 repair:** the reason rule's own priority order now
   checks `owns-the-home`/`lives-there-most-of-the-time`/
   `no-one-else-owes-it` `cannot-tell`, each alone, only once everything
   else (use, original-loan, certificate, box 9) already favours the
   account — a refinance or second property beside an uncertain identity
   answer still reaches this generic residual, confirmed directly
   (`uncertain-ownership-against-refinance`, reconfirmed this round); a
   standalone identity uncertainty now reaches its own category instead
   (`cannot-tell-ownership-alone`, `cannot-tell-residence-alone`,
   `cannot-tell-share-alone`). **P6 correction:** collateral and payment
   `cannot-tell` now each have a specific reason when the remaining account
   is otherwise within the supported boundary; the personal-expense branch
   and other earlier conditions retain priority. Confirmed directly by
   `cannot-tell-collateral-alone` and `cannot-tell-payment-alone`.

**Grandfathering, built this round (choice 3's date prerequisite).** Box
3's date stop is now in this value tree, inside the personal-expense arm
only, after timing clears and the original-loan/box-9 condition holds —
not for the supported arm, which choice 7 still does not need a date stop
for (the post-2017 limit can only under-claim). The reviewed `date_compare`
operator (ADR 0078, `rule-artifact.v14`) compares box 3 against the fixed
literal `1987-10-13` with `cmp: "lte"`: true (on or before the cutoff,
inclusive of the cutoff date itself) blocks as `possible-grandfathered-debt`
instead of publishing the zero; false (strictly after) proceeds to the zero
as before. The cutoff and its inclusive-equality reading follow
§163(h)(3)(D)(i)(II) ("incurred on or before such date") and Publication
936 (2025) p.13 ("before October 14, 1987, ... qualify as grandfathered
debt"). This establishes a *possible* grandfathering case, not every
condition grandfathering needs (continuous security, a later refinancing's
effect) — named in the reason's own sentence and in the Track 0 closure's
known limitations.

**P0–P2 finding.** The adopted value already blocks `VALUE_INVALID` when
collected box 2 is over `tax.us.2025.f1098.mortgage-interest-limit`
version `v1` ($750,000, or $375,000 for married filing separately) — it
simply never saw a real box 2 value to compare, which finding 1 repairs.
`VALUE_INVALID` is already in `RECORD_CODES`, so the line 8a row keeps
that code. No new record code is proposed.

**Proposal.** Ownership `no` and lives `no` do not publish zero, except
that a personal-expense answer still takes arm 1, which does not read
them. P1 left the ownership return-level choice unmade, and a home the
person does not live in may be a second home. Those rows are outside
coverage. Publishing zero there would decide a choice P1 withheld, and
it would select the standard deduction on a return that may still have a
deduction this route does not compute.

Arms 1–3 do not read the limit parameter. **P0–P2 finding.** Their pins
therefore omit `tax.us.2025.f1098.mortgage-interest-limit`. A supported
publication of collected box 1, including a collected zero, pins the
limit because the value compared box 2 with it. That pin difference is in
the derivation record. It is not the sentence the person sees. Section 4
says what the person sees. **Probe result:** the personal-expense value
(`0`, not pinning the limit) and the zero-interest value (`0.0`, pinning
the limit) are distinguishable in the derivation record exactly this way,
confirmed by running both through `live_coordinate_run`.

### Outcomes

Figures are the synthetic package behaviour P0 and P2 measured. Wages are
`90000`. The configured standard deduction is `15000`, pinned to
`demo.parameter.standard-deduction-base.2025` version `v1`. **P0–P2
finding.** The 2025 Form 1040 instructions state $15,750 for single
filers. Line 15 of `70000` or `75000` is that configuration. It is not a
2025-law result. Schedule A publishes when the derived total exceeds the
standard deduction.

| Outcome | Reason | Line 8a | Line 12e | Line 15 | What the person is shown |
| --- | --- | --- | --- | --- | --- |
| Supported, box 1 `20000` | `qualified` | Publishes `20000.0` | `20000`. Attachment published. Tie-out `Reported subtotal: 20000` | `70000` | Supported basis (section 3). Unresolved field inapplicable. **Probe result.** |
| Supported, box 1 `5000` or `8000` | `qualified` | Publishes that amount | `15000`. Attachment guard inapplicable | `75000` | The same supported basis. The interest qualifies and does not change the deduction. The account does not claim a tax saving. |
| Zero interest | `qualified` | Publishes collected `0.0`, limit parameter pinned | `15000`. Same displayed leaves as the disallowed row, including box 1 | `75000` | Supported basis. The interest qualifies and the statement reported none. **Probe result.** |
| Determined disallowed, personal expense | `use-unrelated-personal-expense` | Literal `0`, limit parameter not pinned | `15000`. Attachment inapplicable. No tie-out text | `75000` | The reason's description: the money paid for a personal expense; the interest was reported and does not count. **Probe result.** |
| Determined disallowed, security | `not-collateral` | Literal `0` | `15000`. Attachment inapplicable | `75000` | The reason's description: the home is not collateral for this loan. |
| Determined disallowed, payment | `not-paid` | Literal `0` | `15000`. Attachment inapplicable | `75000` | The reason's description: neither filing spouse paid any and nobody paid any for them. A third-party/partial payment is not a zero. |
| Payment outside coverage (P7) | `payment-outside-coverage` | No line 8a publication; dependent return blocks | Blocked | Blocked | Another person paid some/all for the filing unit, or they paid only part. This probe neither allocates payment nor decides its legal treatment. |
| Outside coverage, owner not on note (choice 1, P4 repair) | `owner-not-on-note` | Blocked `DEPENDENCY_ABSENT` (no zero arm matches) | Blocked | Blocked | The reason's description: paid but not on the note; Treas. Reg. § 1.163-1(b) may still allow the deduction; this route does not compute it. **P4 repair, probed.** |
| Personal expense, timing exception possible (choice 3, P4 repair) | `timing-exception-possible` | Blocked `DEPENDENCY_ABSENT` | Blocked | Blocked | The reason's description: a 90-day or building exception may still apply; this route does not compute the home-cost cap it needs. **P4 repair, probed** (both the 90-day and the building case). |
| Personal expense, timing uncertain (choice 3, P4 repair) | `cannot-tell-timing` | Blocked `DEPENDENCY_ABSENT` | Blocked | Blocked | The reason's description: you said you cannot tell whether a timing exception applies. **P4 repair, probed.** |
| Personal expense, timing not yet established (choice 3, P5 repair) | `timing-not-established` | Blocked `DEPENDENCY_ABSENT` | Blocked | Blocked | The reason's description: you haven't yet said whether this loan was taken out around buying, building, or improving the home. Never claims the person said "can't tell." **P5 repair, probed** (no timing answers, one missing, and one withdrawn after being given). |
| Personal expense, possible grandfathered debt (choice 3, P5 repair) | `possible-grandfathered-debt` | Blocked `DEPENDENCY_ABSENT` (no zero arm matches) | Blocked | Blocked | The reason's description: this loan was originated on or before October 13, 1987, which may make it grandfathered debt, fully deductible regardless of use; this route only compares the origination date, not continuous security or a later refinancing's effect. **P5 repair, probed** (box 3 exactly on the cutoff, and before it). |
| Closed-empty, no-statement flag true | No reason row (no box 1 subject) | No publication. Inapplicable | `15000`. Cites the filing-status leaf and the no-statement flag. Does not cite box 1 | `75000` | No mortgage basis. Unresolved field inapplicable. **Probe result.** |
| Missing answer, or a retraction of one | Reason rule itself blocked `DEPENDENCY_ABSENT` (one of the nine statements has no current finding) | Blocked `DEPENDENCY_ABSENT` | Blocked | Blocked | Unresolved field carries the reason rule's own `wording` as a generic fallback sentence (finding 4's "no single result" branch). Standard deduction stays computed and is not selected. |
| `cannot-tell` on use | `cannot-tell-use` | Blocked `DEPENDENCY_ABSENT` | Blocked | Blocked | The reason's description: you said you cannot tell what the money paid for. **Probe result.** |
| `cannot-tell` on ownership, residence, or the sole-obligor statement, alone (choice 4, P5 repair) | `cannot-tell-ownership` / `cannot-tell-residence` / `cannot-tell-share` | Blocked `DEPENDENCY_ABSENT` | Blocked | Blocked | The reason's own description, naming the specific open question — not the generic outside-coverage sentence. **P5 repair, probed** (each standalone). |
| Outside coverage (refinance, a second property, uncertain ownership beside a refinance, etc.) | `outside-coverage` | Blocked `DEPENDENCY_ABSENT` | Blocked | Blocked | The reason's description: this statement's circumstances are outside what this route computes. **Probe result** (refinance); **P4 repair, probed** (second property, and uncertain ownership beside a refinance — one result, not an ambiguous one). |
| Certificate received | `certificate-received` | Blocked `DEPENDENCY_ABSENT` (no zero arm matches) | Blocked | Blocked | The reason's description: a certificate was reported; the reduced amount is left with the person; this route does not compute Form 8396. |
| Box 2 over the limit | `debt-limit-over` | Blocked `VALUE_INVALID`. None of box 1 published | Blocked `DEPENDENCY_ABSENT` | Blocked | The reason's description: the principal on the statement is over the limit this route uses; the prorated amount is left with the person. **Probe result.** |

**Built this round (choice 3's date prerequisite).** The box 3 date-stop
row (grandfathered on-or-before-October-13-1987 debt spent on a personal
expense) is in this table above (`possible-grandfathered-debt`). See
"Which arm publishes" and section 7 for the reviewed operator and the
schema successor it needs.

**P4 repair.** Every "determined disallowed" row above is a completed
conclusion (the dollar rule published a real value, literal `0`, never a
block), but is still shown to the person through the same blocked
"unresolved" field as the unsupported and unresolved rows below it — the
named, unrepaired carrier gap in "The conclusion carrier" above. This
table's "What the person is shown" column is therefore the *current*,
not the *intended*, account for those three rows.

Outside coverage, for this draft, is any of: original-loan `no` or
`cannot-tell`; use `other`; lives `no`, no-one-else `no`, or ownership
`no` while no zero arm matches; box 9 other than 1; box 1 count greater
than 1. Count greater than 1 is also the adopted
`MULTIPLE_F1098_OUT_OF_SCOPE` block on the line 8a rule's own `when`.
**P0–P2 finding.** That code is not reused for a refinance. The line 12e
field shows `DEPENDENCY_ABSENT` either way. The reason's sentence is what
distinguishes them, not a new record code.

`cannot-tell` is not outside coverage and not the disallowed zero. The
zero arms compare for a specific `no` value, so `cannot-tell` fails them.
The supported arm's conjunction requires `yes` or `bought-the-home`, so it
fails too, and falls to the reason rule's own `cannot-tell-use` or
`outside-coverage` classification.

**P0–P2 finding.** Missing and retracted match each other, including
under a literal-0 rule. A recorded adverse value is a different line 8a
disposition from a missing fact. Withdrawal of a determined answer is the
missing row, so line 12e does not select `15000`. The determined zero
does. Withdrawal is the less favourable return. Section 5 is the
lifecycle.

### How a disallowed statement differs from zero interest

Both can show line 12e `15000` and line 15 `75000`, with box 1 among the
citation leaves and the Schedule A attachment inapplicable. **Proposal.**
The person-facing difference is which rule published, and therefore which
basis section 3 shows.

- Disallowed: literal `0`, limit parameter not pinned, basis says the
  interest was reported and why it does not count.
- Zero interest: collected `0.0`, limit parameter pinned, supported basis
  says the interest qualifies and the reported amount is zero.

A sentence on the published line 12e value is not how they are
distinguished. Section 4 says why.

### Composition hazards the demonstrations have to catch

**Revised for finding 6.** With one rule, "two guards match" cannot happen
inside the production design — there is one `value` tree, tried in a fixed
priority order, never two competing rule citizens. The hazards below are
restated for what remains, plus the one the probe added:

1. A `cannot-tell` or a missing fact publishes `0`. It must not: the
   priority order's zero arms each name one adverse (`no`) value, not
   "anything other than `yes`," and a missing required fact blocks
   `DEPENDENCY_ABSENT` before any arm is reached.
2. The unresolved field and the dollar rule's own disposition must agree
   with the table below: whenever the reason is not `qualified`, the
   unresolved field is active (blocked, carrying that reason's sentence),
   whether or not the dollar rule separately publishes a zero for the same
   case. A row where the two disagree about which reason applies fails the
   demonstration.
3. **Probe-added.** If a later charter or repair reintroduces a second
   producer for `tax.us.2025.schedule-a.line8a` — to restore per-arm basis
   text, for example — the demonstration set must include a case where
   Schedule A is genuinely required (not merely a zero-dollar return), not
   only a double-match case where the attachment is inapplicable. This
   probe's own `double-match-zero` would have passed silently; only
   `double-match-qualifying` caught the defect.
4. **P4 repair.** Two independently decisive adverse facts true at once
   must still publish exactly one conclusion. With one rule and a fixed
   priority order this is true by construction — there is no guard
   collision to detect, only an ordering question, already answered by
   the condition table. The demonstration set still has to exercise it,
   because the ordering could be miswritten: confirmed directly for
   `home-is-collateral` `no` beside a personal-expense answer
   (`not-collateral` wins, per the table's row 1) and for a personal-expense
   answer beside a received certificate (`use-unrelated-personal-expense`
   wins, per the table's row 4 preceding row 6).
5. **P4 repair.** A subject-scoped rule's `requires` is checked as an
   exhaustive join set, not a conditional one; a fact a person was never
   asked (because an earlier answer made the question moot) still has to
   resolve to something, or every subject that never reaches that
   question blocks. The demonstration set has to include a case on the
   side of the gate that never reads the conditional fact (any
   `bought-the-home`/`cannot-tell`/`other` row) to show the structural
   default is never actually consulted there, not merely that it exists.

## 3. Basis

**Adopted fact.** ADR 0077 Part 2 puts an optional `basis` on a
`rule-artifact.v13` rule: `said`, `derived`, `assumed`, and
`left_with_person`. Each item is a sentence. The sentences are not
findings and not a second copy of the pins. `said` and `derived` are
shown beside the pins of what the taken path read. `assumed` and
`left_with_person` have no pin. Package validation checks the four keys
and the string items. It requires non-empty `assumed` and
`left_with_person` only for a rule whose expressions can publish
`plain-case-supported`. It does not judge the sentences. These mortgage
rules publish a number, not that category, so the non-empty check does
not apply. The supported rule still fills `assumed`, because choice 7
makes the assumption visible. The zero rules leave `assumed` empty
because they use no favorable assumption. An empty group is allowed
when the group is unused.

**P0–P2 finding.** A blocked "no" on the student-loan route does not
carry basis in the saved explanation. The same limit is kept here. Basis
is shown for a line 8a publication, including a published zero. A block
has no publication and no basis. The unresolved field's wording is the
account on those rows.

**Proposal, revised for finding 6.** The first draft had each of four
rules declare its own `basis`, so the group never had to say both that the
debt limit was treated as met and that the interest was disallowed in one
object. Collapsing to one line 8a rule (finding 6) means one declared
`basis` object serves every arm that rule can take — it cannot vary by
which branch of `value` actually published. This draft resolves that by
scope, not by inventing a conditional-basis mechanism the schema does not
have: the line 8a rule's own `basis` states only the supported narrative
below. For every other arm (the three zero arms, and every non-publishing
reason), the person-facing account is the reason rule's own category
description, shown through the unresolved field's `resolved.reasons`
(section 2, section 4) — which is active whenever the reason is not
`qualified`, whether or not the dollar rule also published a zero for the
same statement (confirmed by the probe's `personal-expense` and
`double-match-zero` cases: the unresolved field is `blocked`, carrying the
personal-expense sentence, at the same time line 8a publishes literal
`0`). The three disallowed narratives the first draft wrote as full
`said`/`derived`/`assumed`/`left_with_person` groups are retained below as
the source for each reason's one-sentence `description` in section 1's
reason fact type, not as a second basis object a reader has to load from
two different rules.

### Supported result

Used for a collected box 1, including a collected zero. The amount the
person sees is the published value. The sentences do not say the amount
is zero, and they do not say it is above the standard deduction.

**Said.**

- The person owns the home this statement describes.
- They live there most of the time.
- The home is collateral for this loan.
- The person or, on a joint return, their spouse owes this loan.
- The person or, on a joint return, their spouse paid the interest.
- No one besides the person or their joint-filing spouse owes the loan.
- The borrowed money bought the home.
- This is the original loan.
- They did not receive a mortgage credit certificate (**revised for
  finding 7**: the statement is now phrased as receipt, so "did not
  receive" is its favourable `not-received` value, not a double negative).

**Derived.**

- One Form 1098 is on record, and box 9 reports one property, directly
  recorded or supplied by its `optional_default` (**finding 5**). The
  application holds the single-statement bound. The person did not
  affirm it.
- The application concluded that this interest is qualified residence
  interest for the opening case.
- Box 2 was compared with `tax.us.2025.f1098.mortgage-interest-limit`
  version `v1` for the filing status, read directly (**finding 1**; the
  adopted rule's collect never saw this value). That check passed. It is
  a check, not an assumption. Box 3 is required and is not part of this
  check this round — see "Which arm publishes" and section 7.
- The published amount is the reported box 1.

**Assumed.**

- For this one original borrowing, for this tax year, box 2 stands for
  the acquisition-debt balance at every moment of the year. The route
  publishes the whole of box 1 and does not prorate. Grounds are
  Publication 936's fully deductible shortcut, and the ordinary course
  of an amortizing loan whose highest balance is at the start of the
  year or at origination. The subject is this borrowing's
  acquisition-debt balance.

**Left with the person.** Stated on this result. Not enforced. Nothing
the person records triggers them, and the route records no stop-report
whose withdrawal would restore the assumption.

- A higher balance during the year, another mortgage, a line of credit,
  an added draw, or a second home's debt. If one of those is true, the
  prorated or combined amount is the person's. This route does not
  compute Publication 936 Table 1.
- Interest box 1 includes that accrues after the year. Publication 936
  tells the payer to deduct only the year's qualified interest. The
  route publishes box 1 whole.
- Points, mortgage-insurance premiums, and a box 4 refund of prior-year
  interest. They stay out of this amount. The route does not report the
  refund as income and does not add the premium.

The bound stop is not repeated here as an open condition. A box 2 over
the limit means this rule did not publish, so this basis is not shown.
Box 3 is not a bound stop on the supported arm (choice 7; unchanged this
round — the post-2017 limit can only under-claim, so no date stop is
needed here). Box 3 is now read for the personal-expense zero's
grandfathering check instead — see "Which arm publishes." Section 5 says
how the person sees the assumption return after a correction.

Choice 5 is kept. **Derived** carries one more sentence: ownership,
residence, security, and use are the person's answers. The route did
not supply them. That sentence is not an `assumed` item. An assumption
is a premise with no answer recorded, taken in the person's favor.

### The three disallowed reasons

**Revised for finding 6.** These are no longer separate rule `basis`
objects (there is one line 8a rule). Each is instead the
`description` text [section 1](#1-ordinary-statements-and-identity)
declares for the matching `tax.us.2025.f1098.residence-interest-reason`
value, written from the same material the first draft's three full
`said`/`derived`/`assumed`/`left_with_person` groups established, so no
content is lost — only its carrier changes.

- **`use-unrelated-personal-expense`** ("the money paid for a personal
  expense"). Said: the borrowed money paid for a personal expense that
  was not buying, building, or improving the home; this is the original
  loan; **P4 repair:** the loan was not taken out within 90 days of
  buying the home, and the person was not building or improving the home
  shortly before or after taking it out (the two ordinary timing
  questions, choice 3). Derived: the debt is not acquisition
  indebtedness; the published zero is that conclusion, not a report that
  the lender received no interest; the debt-limit assumption is not used;
  **P5 repair:** box 3 is strictly after October 13, 1987 — this is not
  possibly grandfathered debt (the `date_compare` check, section 7).
  Left with the person: a deduction under another provision (none
  published here); a mortgage credit certificate, if they also have one
  (the credit does not restore this interest; Form 8396 is not computed);
  **named limitation, carried forward:** the grandfathering check compares
  only the origination date — it does not verify continuous security or
  how a later refinancing of pre-cutoff debt would affect this result
  (this route already treats a refinance as outside coverage, condition
  table row 6, before this check is ever reached).
- **`not-collateral`** ("the home is not collateral"). Said: the home is
  not collateral for this loan. This conclusion does not establish that it
  is the original loan. Derived: the
  debt is not acquisition indebtedness because it is not secured by the
  home; the published zero is that conclusion; the debt-limit assumption
  is not used. Left with the person: any deduction under another
  provision (none published here).
- **`not-paid`** ("neither you nor your joint-filing spouse paid any, and
  nobody paid any for you"). Said: `paid-the-interest` is `no`. Derived:
  no home-mortgage deduction is published for this statement; the debt-limit
  assumption is not used. Left with the person: a share
  reported on someone else's Form 1098 (Schedule A line 8b, which this
  route does not compute).
- **`payment-outside-coverage`** ("someone else paid some or all of this
  interest, or you paid only part"). Said: `paid-the-interest` is
  `paid-by-others-or-partial`. Derived: no line 8a amount and line 12e
  remains blocked. Left with the person: the applicable tax treatment. The
  route does not identify the payer, allocate amounts, or decide gift or
  constructive-payment treatment.

None of the three carries an `assumed` group. None reads the limit
parameter, matching the pin finding above.

### Twelve further outside-coverage and unresolved reasons (choice 1, choice 3, choice 4; P4–P6 repairs)

None of these twelve carries a `basis` group at all: each is a block, not
a publication (condition table rows 3, 5, 7, and 10). The person's account
is entirely the reason's `description`, shown through the blocked
unresolved field like every other non-`qualified`, non-decisive-zero
reason — these were never part of "The conclusion carrier"'s gap, because
none of them is a completed conclusion.

- **`owner-not-on-note`** ("paid but does not owe the loan"). Said:
  `owes-the-loan` is `no`; `paid-the-interest` is `yes`. Left with the
  person: Treas. Reg. § 1.163-1(b) may let an equitable owner who is not
  on the note deduct the interest they paid; this route does not compute
  that owner's deduction, because nothing in this account establishes the
  equitable-ownership fact that regulation needs.
- **`timing-exception-possible`** ("a purchase or completion timing
  exception may apply"). Said: the borrowed money paid for a personal
  expense; the loan was within 90 days before or after buying the home, or
  before completion of building or improving the home or within 90 days
  after completion. Left with the person: Publication 936 (2025), page 12,
  may make this acquisition debt, subject to the separate expense cap;
  this route does not compute that cap or decide whether the work was a
  substantial improvement. Its `yes` answer is conservative and can
  include non-substantial work.
- **`cannot-tell-timing`** ("timing is not yet known"). Said: the
  borrowed money paid for a personal expense; the person could not say
  whether the 90-day or building timing applies. Left with the person:
  the same exception as above, once the timing is known.
- **`timing-not-established`** ("timing has not been answered yet", P5
  repair). Said: the borrowed money paid for a personal expense; one or
  both timing questions have no current answer — never asked, or an
  answer given and then withdrawn. Left with the person: the same
  exception as `timing-exception-possible`, once they answer. This is a
  different open question from `cannot-tell-timing`: the person never said
  "I don't know," so the sentence never implies they did.
- **`possible-grandfathered-debt`** ("this loan may be grandfathered",
  P5 repair). Said: the borrowed money paid for a personal expense; the
  timing and original-loan/box-9 conditions above are already established;
  box 3 reports an origination date on or before October 13, 1987. Left
  with the person: §163(h)(3)(D) may make this debt fully deductible
  regardless of use; this route only compares the origination date, not
  whether the debt stayed continuously secured by the home or how a later
  refinancing of pre-cutoff debt would affect this result.
- **`cannot-tell-ownership`** ("ownership is not yet known", P5 repair).
  Said: the person could not say whether they own this home; every other
  answer is favourable. Left with the person: nothing further — once
  ownership is answered, the account resolves on its own terms.
- **`cannot-tell-residence`** ("residence is not yet known", P5 repair).
  Said: the person could not say whether this is the home where they live
  most of the time; every other answer is favourable. Left with the
  person: the same, once residence is answered.
- **`cannot-tell-share`** ("the sole-obligor statement is not yet known",
  P5 repair). Said: the person could not say whether anyone else owes this
  loan with them; every other answer is favourable. Left with the person:
  the same, once that is answered. On a joint return, a co-obligor spouse
  does not make this answer `cannot-tell` or `no` — see "Liability" above.
- **`cannot-tell-collateral`** ("collateral is not yet known", P6). Said:
  the person could not say whether the home is collateral for this loan;
  every other answer is favourable. Left with the person: the same, once
  that answer is known.
- **`cannot-tell-payment`** ("payment is not yet known", P6). Said: the
  person could not say whether they or their spouse on a joint return paid
  the interest; every other answer is favourable. Left with the person:
  the same, once that answer is known.

The first draft's three separate disallowed `basis` write-ups, superseded
by "The three disallowed reasons" above since the first repair round,
are deleted here; the earlier drafts remain in Git.

## 4. Explanation reader

### Show the basis of whatever rule a result pins

**P0–P2 finding.** `_sli_support_basis` and `_sli_cover_basis` in
`packages/derivation/presentation_projection.py` load `basis` only when
the publication's computation pin id is
`tax.us.2025.rule.sli-statement-loan-support` or
`tax.us.2025.rule.sli-statement-combined-standing`. They return
`assumed` and `leftWithPerson`. The support reader also rebuilds an
`answers` list. Neither returns the object's `said` or `derived`. A
missing basis on those two rules raises `PresentationModelError`.
`packages/derivation/explanation.py` records `rule_references` and does
not read `basis`. The probe's presentations had no mortgage basis.
`line21Explanation` was absent on every mortgage row.

**Adopted fact.** ADR 0077 Part 2, "How a reader reaches it": the reader
loads the adopted rule at the publication's computation pin and reads
`basis`. `said` and `derived` are shown beside the input pins.
`assumed` and `left_with_person` are shown in the same account and have
no pin. A rule with no `basis` gives the reader nothing for those
groups. That is allowed except for the plain-case support rule. Part 2
adds no walk schema and no finding schema.

**Proposal.** One loader, used for any publication the presentation is
already showing. It takes the computation pin's id and version, finds
that member, and returns the four groups when `basis` is present. It
returns nothing when `basis` is absent. It does not raise because the
rule id is unfamiliar, and it does not raise because a rule has no
basis. The two student-loan callers keep the checks they have now:
the support rule must have basis, the cover basis is refused unless
the older answer is `yes`, and the cover basis is refused when it
reuses the support rule's box 1 assumption. Those checks run after the
load. They are not an id allowlist on the loader.

The mortgage publication has to be in the model or the loader is never
called. **P0–P2 finding.** No presentation section is bound to
`tax.us.2025.schedule-a.line8a`. **Proposal.** `build_presentation_model`
gains a section for a publication of that symbol. The section is built
from the finding, not from `_one_row` over every disposition of the
symbol — **revised for finding 6:** now there is exactly one producer, so
there is no sibling producer to exclude; the earlier "not a second
account" caveat described the first draft's four-rule shape and is moot
with one rule.

**Revised for findings 3 and 6; widened by the third reader change (P5
repair).** With the line 8a rule's own `basis` written for the supported
narrative only (section 3), the section this reader builds must not show
that basis unmodified for a literal-`0` disallowed publication of the same
symbol — but it must show *some* account of that publication, per choice
8, not none at all (P4 re-review finding 1). The current statement-scoped
reason selects the account: `qualified` uses the supported basis, while a
zero publication whose reason is one of the three decisive-zero categories
(`not-collateral`, `not-paid`, `use-unrelated-personal-expense`) builds a
completed line 8a account from
that reason's own `description` content (section 3's "The three disallowed
reasons"), never from the line 8a rule's own `basis` object. Neither
account duplicates the unresolved field once the first reader
change (widening the field's `when`) makes that field inapplicable for
these three rows — the basis section is the account for them instead. For
every other non-`qualified` reason (outside coverage, uncertain, or
unresolved — none a completed conclusion), no line 8a section is built;
the person's account is entirely the unresolved field's `resolved.reasons`
sentence, as before. When line 8a did not publish at all, the section is
absent for that reason instead. Blocked rows never receive an empty basis,
in any case.

This is the engine change in choice 8. It is one loader for any pinned
rule. It is not a mortgage-only function with the line 8a rule id
written into it.

**Adopted fact, and why this is not a new ADR.** The loader is the
reader Part 2 already describes. The line 8a section is the call site
that was missing because the implemented reader named two rule ids.
No schema version changes. `npe-walk.v3` and `derived-finding.v2` stay
as they are.

**P4 repair, named gap — the second reader change choice 8's remaining
defect needs.** The loader above shows the supported narrative correctly
once the limit parameter is pinned. It does not, on its own, fix the
three determined zero reasons' carrier: "The conclusion carrier" in
section 2 traces that gap to `presentation_projection._favorable_values`
and the `len(favorable) != 1` check inside `_selection_blocked_reasons`,
which assumes a declared read's favourable set is exactly one value.
**Probe result:** a four-favourable declaration (the three zero reasons
plus `qualified`) raises `PresentationModelError: declared read ... has no
single expected value`, reproduced live and reconfirmed unchanged this
round (`determined-zero-reader-gap`, `p5_probe.py`).

**Proposal, not built.** Loosen that one check from "exactly one" to
"one or more": `_favorable_values` already returns a `set`, built by
scanning every `collect_categorical_all_equal` node in the declaration,
so a path's `when` written as `not(any(...))` over several such nodes
already produces the right set; only the consuming check needs to admit
more than one member. Every existing caller (the two student-loan
selection rules) still declares exactly one favourable value, so this is
additive, not a behaviour change for adopted content. It is a pure
Python change in `presentation_projection.py`, not a schema successor —
`rule-artifact.v13`'s selection shape does not change. Costed alongside
the date-comparison capability in section 7. Until it lands, the three
determined zero reasons stay on the blocked field — named, not silent.

**P5 repair, named gap — the third reader change.** Even with the check
above loosened, the unresolved field becoming `guard_inapplicable` for the
three determined-zero reasons means it stops carrying *any* sentence for
them (a `guard_inapplicable` row never populates `resolved.reasons`), and
the basis-section gate immediately above this paragraph was, until this
round's correction, gated on the limit pin alone — which these three
reasons never carry. Traced precisely in "The conclusion carrier" (section
2): the two fixes above are each individually sound but insufficient
together, and this paragraph's widened gate (the "second branch," above)
is the third change that closes the gap, specified the same way: pure
Python in `presentation_projection.py`, no schema successor, not built
this round.

### A sentence on the published line 12e value

**P0–P2 finding.** Line 12e is `form-field.v3` bound to a
`rule-artifact.v4` producer. A published numeric field resolves to
disposition, value, and citation sites. The field's blocked explain
text is the word "blocked" for every code. A sentence on that published
number does not come from `resolved.reasons`. Reasons attach when the
producer is a blocked v13 selection rule.

**Selected design.** Do not attach a sentence to the published line 12e
value. Line 12e remains the chosen deduction: the standard deduction or
the itemized total. Qualified interest, including reported zero interest,
gets the supported line 8a basis account. Each justified-zero reason gets
its own completed account, without the supported arm's assumptions.
Only an unresolved or outside-coverage result uses the unresolved field's
`resolved.reasons`. The current reason and amount select these accounts;
limit-pin presence does not define the tax conclusion.

**Historical probe limitation:** the early `personal-expense` probe showed
its sentence through a blocked field, whereas `zero-interest` had an
inapplicable unresolved field. That was the defect the selected reader work
repairs, not the intended production distinction. Both may leave line 12e
at the same configured standard deduction, but the mortgage accounts must
explain their different conclusions. This does not establish that the
fixture's `15000` is the legally correct 2025 standard deduction.

**Proposal.** That further reader change is not made, so it needs no
ADR. Making it would need a new ADR. Part 2 does not describe copying
wording onto a published numeric field, and line 12e's own rule is the
wrong place for the debt-limit assumption. No accepted ADR requires
the sentence. Choice 8's completion test is a saved explanation of the
answer and the basis. The basis section and the unresolved field meet
it.

### The lender label

**P0–P2 finding.** `_statement_label` reads `lender` and `statement`.
Form 1098 keys use `payer`. The label stays empty, and a blocked
sentence still attaches on the fact id.

**Proposal.** In the same reader unit, when `lender` is absent and
`payer` is present, the label uses the `payer` entity. Fact ids do not
change, and no `lender` key is added. This is a label fix. It is not an
ADR. The unresolved sentence can then name the statement's lender
instead of only the fact id.

## 5. Correction, withdrawal, and legacy records

### What each change does to the result

**Adopted fact.** ADR 0041 `free` admits a later assertion of the same
fact. **P0–P2 finding.** `_finding_corrections` displaces the earlier
finding with reason `correction`. The fact id does not change. Box 1,
box 2, and box 3 are different fact types from the ordinary answers, so
an answer correction does not rewrite the form, and a form correction
does not rewrite the answer.

**Adopted fact.** ADR 0073. Withdrawal is `finding-retracted` with
payload `{"finding_id": <that finding>}`. It ends current support for
that one finding. It writes no replacement and no opposite claim. It
does not establish that the original author withdrew the statement.
Product text says the answer is no longer in the account. It does not
say the author recanted.

| Change | Current value afterward | Result |
| --- | --- | --- |
| Correct an answer to a different stored value | The new value | The arms in section 2 are evaluated again on the new value. |
| Answer `cannot-tell`, including as a correction of a previous `yes` or `no` | `cannot-tell` | The unresolved row. Not zero. Not outside coverage. |
| Withdraw an answer | No current value | The missing row. Same measured disposition as an answer that was never given. |

**Proposal.** Withdrawing an answer a publishing arm used never makes
the result more favourable.

- Withdrawing a supported answer drops a published deduction and blocks
  line 12e and line 15. The standard deduction stays computed and is
  not selected.
- Withdrawing the personal-expense value, the collateral `no`, or the
  `paid-the-interest` `no` (**revised for finding 3**) leaves the missing
  row. Line 12e blocks. The determined zero had selected `15000` and
  completed line 15. The block does not.
- Withdrawing certificate `not-received` (**revised for finding 7**; was
  `yes`) drops the supported arm and blocks.
- Withdrawing certificate `received` leaves the fact absent. The reported
  certificate had blocked, and the absence blocks. Neither publishes
  box 1. The absence is not the favorable `not-received`.
- **P4 repair.** Withdrawing `owes-the-loan` `yes` (choice 1's new gate)
  drops the supported arm and blocks, the same direction as withdrawing
  any other favourable gate above.
- **P5 repair (owner finding 1).** Withdrawing one of the two timing
  facts, while use stays `unrelated-personal-expense`, returns that fact
  to its package-level `optional_default` — the reserved sentinel
  `not-asked` — not to the missing row every other ordinary statement
  falls to, because the fact's absence is bound at the package level (the
  exhaustive-join constraint "Condition table" and section 7 explain).
  Unlike P4's withdrawn structural defaults, `not-asked` is never
  favourable: the reason rule routes it to `timing-not-established`, the
  same open-condition category an unanswered or never-asked question
  reaches, never the zero. This is still a direction worth naming
  precisely: a timing withdrawal is *less* favourable than keeping the
  answer whenever that answer was favourable (the zero was reached and is
  now withdrawn to an open question), and it is *not more* favourable than
  an unfavourable answer (both reach a blocked, non-zero row) — withdrawal
  never increases the deduction, matching every other fact in this table.
  **P5 repair, probed** (`personal-expense-timing-withdrawn`: a favourable
  answer given, then retracted within the same run, reaches
  `timing-not-established`, not the zero it would otherwise have reached).

A correction that replaces `unrelated-personal-expense` with
`bought-the-home`, while the rest of the supported arm holds, does
increase the deduction. That is a new answer, not a withdrawal. A
correction from `bought-the-home` to `cannot-tell` blocks. It does not
keep the deduction and it does not publish zero. **P4 repair.** A
correction from `unrelated-personal-expense` to `owes-the-loan` `no`
while `paid-the-interest` stays `yes` moves the account to
`owner-not-on-note`; that correction is less favourable only in the
sense that it was never the supported arm to begin with — choice 1's
boundary, not a new direction of this table.

### The debt-limit assumption

**Starts** when the supported rule publishes box 1. The person sees the
assumption in that result's `assumed` group, and the unenforced stops
in `left_with_person`. They do not see it on a blocked row, because
that row has no basis.

**Stops, and the rule binds the stop.**

- Box 2 over the limit: `VALUE_INVALID`, none of box 1, no basis. The
  reason rule publishes `debt-limit-over`; the unresolved field's sentence
  says the principal is over the limit this route uses, and the prorated
  amount is left with the person. **Revised for finding 2:** this
  sentence comes from the reason category's `description`, not from a
  `missing` list the `block` op cannot carry.
- Box 3's date stop is **deferred** this round (see "Which arm
  publishes" and section 7); there is no "both stops" row until it
  exists.

A missing, withdrawn, or `cannot-tell` answer is not a debt-limit stop.
The line 8a rule does not publish, so the assumption is not in force,
and the return is the missing or unresolved row.

**Stops, stated and not enforced.** A higher balance during the year,
another mortgage, a line of credit, an added draw, or a second home's
debt. They are sentences on a supported result. They do not change the
published amount. The route stores no stop-report. Silence is the case
in which the assumption applies, because the person was not asked for
a report. There is no report to withdraw, so withdrawal cannot restore
a deduction a report had removed. **P0–P2 finding.** The P3 planning
review showed that a stored stop-report would make withdrawal more
favourable than the report. This draft does not store one. A later
route that adds the report has to state that direction itself.

**Resumes** when a correction makes the supported arm true again. The
guard re-evaluates. The person sees the basis, including the
assumption, come back.

- Box 2 corrected from over the limit to at or under: the publication and
  the assumption return.
- Box 2 corrected the other way: the assumption stops, and the person
  sees the reason rule's `debt-limit-over` sentence instead of the basis.

Those box corrections are more favourable when they restore a
publication, and less favourable when they remove one. They are
corrections of the reported statement, not withdrawals of an answer the
rule determined. Choice 7 is this re-evaluation. The unenforced stops
remain visible in `left_with_person` whenever the assumption is showing.
**Probe result:** box 2 corrected from `800000` to `200000` is not run by
this probe directly, but the over-limit and supported-purchase cases
already show both ends of this correction independently (same statement
keys, different box 2), which is the same evaluation the runner would do
on a correction.

### ADR 0077 Part 5

**Proposal.** Part 5 does not apply to this tie. It refuses a new
current finding of a declared source fact while a current dependent
fact names that source, unless one reviewed-scope successor is bound.
The student-loan map pairs box 1 with the statement-inclusion fact,
whose keys add `borrowing`. This route has no inclusion and no extra
key. No registry entry is added. A new box 1 finding is admitted while
the ordinary answers are current. The answers stay current. The line 8a
arm re-evaluates on the new amount. Copying the refusal here would
block a correction of the reported interest until evidence this route
does not collect had been reviewed. Part 5's replay rule is unchanged
because there is no new map: a history that already holds a rewrite
stays readable.

### Legacy confirmations

**P0–P2 finding.** Section 4 of the mechanism-fit account states three
options and chooses none. Keep requiring the eight. Stop reading them.
Retire the types. An old `yes` is not copied onto a new statement by
any of the three. **P0–P2 finding.** `_present_successor_claims`
presents a predecessor value and does not write the successor.
`_is_zero_value` is false for `yes` and `no`, so a current confirmation
blocks a `resolved-required` migration. The probe did not run a
migration.

**Proposal.** Stop reading the eight. The successor package omits
`tax.us.2025.schedule-a.line8a.rule` version `v1` and does not name the
eight fact types in any new rule. The fact types stay published
citizens. Their findings stay in the log.

A workspace that already holds them keeps eight current findings, keyed
by `payer`, `statement`, and `tax-year`, still correctable on those
ids. The new rules do not read them, so the return blocks on the
missing ordinary statements until the person answers. An old
`acquisition-debt-use` `yes` beside a new
`unrelated-personal-expense` follows the new answer and publishes zero.
An old `no` beside a new `bought-the-home` follows the new answer and
can publish box 1. The old finding is history. It is not a second gate,
and it is not a sentence in the new basis. No migration is required for
the successor package to resolve.

Retiring the types is the option set aside. A `resolved-required`
migration cannot proceed while those `yes` and `no` findings are
current, and a migration that does displace them takes them off current
standing. Stopping the read gets the same computation — the old facts
do not feed the new deduction — and leaves the history correctable.

Keeping the eight in the new gate is the option set aside. It would
put the legal confirmations and the software bounds back on the route
choices 1 and 2 removed. The count, box 9, `this-is-the-original-loan`,
and `no-one-else-owes-it` carry the bounds the application states. The
person is not asked to affirm them.

## 6. Demonstrations

Every case is synthetic. Payer `demo.f1098.lender.a`, statement
`demo.f1098.stmt.a`, tax year `2025`, filing status single, wages
`90000`, unless a case says otherwise. Box 2 is `200000`, box 3 is
`2020-06-01`, box 9 is `1`, and boxes 4, 5, 6, and 11 are `0`, unless
a case varies them. The scope flag is false when a statement is
present. The Form 1098 family is closed. A closed-empty Form 1098-E
family and the Schedule 1 absence declarations are the same synthetic
setup P0 used. They are not a student-loan account. That account is
its own case below.

**P0–P2 finding.** The configured standard deduction is `15000`, pinned
to `demo.parameter.standard-deduction-base.2025` version `v1`. The
`70000` and `75000` line 15 figures are that package behaviour. They
are not the $15,750 single-filer amount in the 2025 instructions.

Runs go through `live_coordinate_run` on a publication surface. A
`RunContext` shortcut is not the demonstration.

**P7 targeted capture:** `python3 .../p5_probe.py --p7-targeted` runs nine
changed cases (four payment answers, three same-fact correction states, the
actual MFJ case, and stock Example 1). The three correction states can be
captured alone with `--p7-correction-only`. These summaries compare named
expected and observed coordinator values and current assertion support. P7
does not rerun the unchanged full battery.

| Case | What is recorded | Expected result | Probed |
| --- | --- | --- | --- |
| Supported purchase | All nine answers favorable (finding 3's split). Box 1 `20000`. | Line 8a `20000.0` from the line 8a rule. Reason `qualified`. Line 12e `20000`. Attachment published, tie-out `Reported subtotal: 20000`. Line 15 `70000`. Basis is section 3's supported text, including the debt-limit assumption. Unresolved field inapplicable. | **Yes** (`supported-purchase`), except the attachment tie-out text, line 15, and the basis section itself, which this probe did not build a presentation check for. |
| Personal expense | Use `unrelated-personal-expense`. Original-loan `yes`. Both timing answers favorable (`more-than-90-days`, `no`). Box 3 after the grandfathering cutoff (default `2020-06-01`). The other answers favorable. Box 1 `20000`. | Literal line 8a `0`. Reason `use-unrelated-personal-expense`. Limit parameter not pinned. Line 12e `15000`. Attachment inapplicable. Line 15 `75000`. Unresolved field blocked, carrying that reason's sentence (not a basis section — the carrier gap, section 2/4; still unrepaired this round, "The conclusion carrier"). | **Yes** (`personal-expense-clean`), except line 15 and the attachment disposition directly. |
| Standard deduction stays larger | Supported answers. Box 1 `5000`, and the same case again at `8000`. | Line 8a is that amount. Reason `qualified`. Line 12e `15000`. Line 15 `75000`. Attachment guard inapplicable. Supported basis is shown. The text does not claim a tax saving. | No. |
| Uncertain use | Use `cannot-tell`. Every other answer favorable. Box 1 `20000`. | No line 8a publication (blocked `DEPENDENCY_ABSENT`). Reason `cannot-tell-use`. Line 12e and line 15 blocked. Unresolved field carries the `cannot-tell-use` sentence. The row is not labeled outside coverage. No basis section. | **Yes** (`cannot-tell-use`). |
| Outside coverage | Original-loan `no`. Use `bought-the-home`. Other answers favorable. Box 1 `20000`. | No line 8a publication. Reason `outside-coverage`. Not `MULTIPLE_F1098_OUT_OF_SCOPE`. Line 12e and line 15 blocked. Unresolved field says a refinance is outside what this route computes and leaves the treatment with the person. | **Yes** (`refinance`). |
| Correction and withdrawal | Start from the supported purchase. Correct the use answer to `unrelated-personal-expense`. Then retract that use finding. Separately, from the supported purchase, correct box 2 to `800000` and then back to `200000`. | After the use correction: the personal-expense row. After the retraction: the missing row, line 12e blocked, not `15000`. After box 2 `800000`: line 8a `VALUE_INVALID`, reason `debt-limit-over`, no basis section. After the correction back: the supported purchase, assumption visible again. | Not directly as a correction sequence; the probe's `box2-over-limit` and `supported-purchase` cases independently cover both ends on the same statement keys. |
| Interest changes the deduction | The supported purchase, box 1 `20000`. | Line 12e moves from the `15000` standard deduction to `20000`. This is the same run as the supported purchase. It is listed so the deduction change is an expected outcome of its own. | Same run as `supported-purchase`. |
| Box 2 over the limit | Supported answers. Box 2 `800000`. | One `VALUE_INVALID` block. Reason `debt-limit-over`. No basis. | **Yes** (`box2-over-limit`). |
| Box 9 absent | Supported answers. Box 9 omitted. | Line 8a publishes `20000`, as if box 9 were `1` (finding 5). Reason `qualified`. | **Yes** (`box9-absent`). |
| Zero interest | Supported answers. Box 1 `0`. | Collected line 8a `0.0`. Limit parameter pinned. Reason `qualified`. Line 12e `15000`. Supported basis section shown, not the personal-expense reason. | **Yes** (`zero-interest`). |
| Certificate | Certificate `received`. Other answers favorable. Box 1 `20000`. | No line 8a publication. Not literal `0`. Reason `certificate-received`. Unresolved field says a certificate was reported and Form 8396 is not computed. | Not directly; the `_bundle()`'s `certificate-received` reason and description are built and probed only indirectly through the other cases' guards. |
| Closed-empty | No statement. No-statement flag true. None of the nine new answers. | Line 8a inapplicable. No reason row (no box 1 subject to dispatch over). Line 12e `15000`, citing the flag and not box 1. Unresolved field inapplicable. | **Yes** (`closed-empty`). |
| Deliberate double match, attachment inapplicable | A second producer rule, guard-for-guard identical to the first, added to the package. Personal-expense answers (Schedule A not required). | Run completes. First-attempted producer publishes; the second is `inapplicable`, no `guard_result` (a true conflict loser, not a false guard). | **Yes** (`double-match-zero`). |
| Deliberate double match, attachment required | Same second producer. Supported answers (Schedule A required). | `build_presentation_model` raises `PresentationModelError` on the attachment's `_one_row` join for `tax.us.2025.schedule-a.line8a` — a genuine composition defect this design's one-rule repair avoids by construction. | **Yes** (`double-match-qualifying`) — this is the result that changed finding 6's repair from "state first-publisher-wins" to "propose fewer rules." |
| Old confirmation left in place | A current `acquisition-debt-use` `yes` on the same keys, and the new use answer `unrelated-personal-expense`. | The personal-expense row. The old `yes` is not a pin of the zero and is not a basis sentence. | No. |
| Unrelated student-loan account | A synthetic student-loan return that already publishes line 21, run once with no Form 1098 and once with the supported purchase added. | Line 21's value, combined standing, and student-loan basis match the run that has no Form 1098. The mortgage section shows the supported purchase. The mortgage rules do not read the student-loan facts. | No. |
| Personal expense, refinance (choice 3) | Personal expense, favorable timing, but original-loan `no`. | Reason `outside-coverage`, not the zero. Line 8a blocked, not literal `0`. | **Yes** (`personal-expense-refinance`). |
| Personal expense, two properties (choice 3) | Personal expense, favorable timing, box 9 `2`. | Reason `outside-coverage`, not the zero. | **Yes** (`personal-expense-two-properties`). |
| Personal expense, timing uncertain (choice 3) | Personal expense, either timing answer `cannot-tell`. | Reason `cannot-tell-timing`. | **Yes** (`personal-expense-cannot-tell-timing`). |
| Personal expense, uncertain ownership (choice 9) | Personal expense, favorable timing, ownership `cannot-tell`. | Reason `use-unrelated-personal-expense`. Ownership uncertainty does not reclassify a decisive personal-expense use. | **Yes** (`personal-expense-uncertain-ownership`). |
| Uncertain ownership against a refinance (choice 9) | Ownership `cannot-tell`, original-loan `no`, use `bought-the-home`. | Reason `outside-coverage` — one result, not an ambiguous one between the ownership and the refinance conditions. | **Yes** (`uncertain-ownership-against-refinance`). |
| Owner not on the note (choice 1) | `owes-the-loan` `no`, `paid-the-interest` `yes`, other answers favorable. | Reason `owner-not-on-note`. Not the supported arm. Line 8a and line 12e blocked. | **Yes** (`owner-not-on-note`). |
| Two decisive adverse facts, security and use (choice 9) | `home-is-collateral` `no` and use `unrelated-personal-expense` at once. | Reason `not-collateral` — row 1 of the condition table wins over row 4, by the rule's fixed priority order, not a runner-level guard choice. | **Yes** (`not-collateral-and-personal-expense`). |
| Two decisive adverse facts, use and certificate (choice 9) | Use `unrelated-personal-expense` and certificate `received` at once. | Reason `use-unrelated-personal-expense` — row 4 precedes row 6. | **Yes** (`personal-expense-and-certificate-received`). |
| Payment: another person paid all or partial payment | Ordinary answer “someone else paid all” / “someone else paid part, and I paid only part”; stored `paid-by-others-or-partial`. | `payment-outside-coverage`; no line 8a publication; line 12e blocked, never zero or qualified. | **Yes, P7 targeted coordinator** (`payment-other-person-paid-all`, `payment-partial`). |
| Payment: no one paid by or for filing unit | Neither filer nor joint spouse paid any and nobody paid any for them; stored `no`. | `not-paid`; line 8a literal `0`; line 12e selects configured `15000`. | **Yes, P7 targeted coordinator** (`payment-none-by-or-for-filing-unit`). |
| Payment: cannot establish which description | Ordinary answer cannot tell; stored `cannot-tell`. | `cannot-tell-payment`; line 8a and line 12e blocked, not zero. | **Yes, P7 targeted coordinator** (`payment-cannot-tell`). |
| Payment correction and current support | Supported `yes`, correct to partial/other payment, then correct back to `yes` on the same statement-keyed fact. | Start: qualified, line 8a `20000.0`, line 12e `20000`, current pin `demo.f1098.p5.paid-the-interest`. Outside-coverage correction: no line 8a amount, line 12e blocked, current pin `demo.f1098.p7.payment-corrected-to-partial`; the initial pin is absent. Correction back: qualified and both amounts `20000`, current pin `demo.f1098.p7.payment-corrected-back-to-supported`; both prior pins absent. | **Yes, P7 correction-only coordinator capture** (`payment-correction-supported-start`, `payment-correction-to-outside-coverage`, `payment-correction-back-to-supported`). Recorder lifecycle is not exercised. |
| Supported real joint filing status | Ordinary spouse account: other spouse owes and paid; stored filing status `married_filing_jointly`, liability/payment/sole-obligor `yes`. | `qualified`; line 8a `20000.0`; actual configured line 12e `30000`. | **Yes, P7 targeted coordinator** (`joint-filer-other-spouse-obligor-and-payer`). |
| Publication 936 Example 1, stock purchase | Home bought 42 days before loan; loan money bought stocks. Stored use is `other` (purchase timing also recorded `yes`). | `outside-coverage`; no line 8a amount and line 12e blocked. The personal-expense timing analogues remain separate. | **Yes, P7 targeted coordinator** (`pub936-example1-investment-other`). |
| Publication 936 situation 2, building before completion (choice 3, action 4, P5 repair) | Personal expense, building or improving shortly before or after taking out the loan — mortgage taken out before the work is completed, within 24 months. | Reason `timing-exception-possible`. | **Yes** (`pub936-situation2-building-before-completion`). |
| Publication 936 situation 3, mortgage after completion | Same building question (the application does not distinguish situation 2 from 3) — Logan's case: building started Jan 31, home completed Oct 31, mortgage taken out Nov 21 (within 90 days after, within 24 months of starting). | Reason `timing-exception-possible`, the same way, leaving the precise 24-month expense window with the person. | **Yes** (`pub936-situation3-mortgage-after-completion`). |
| Personal expense, grandfathered on the cutoff (choice 3, P5 repair) | Personal expense, favorable timing, original loan, one property, box 3 exactly `1987-10-13`. | Reason `possible-grandfathered-debt` — equality is the grandfathered side (§163(h)(3)(D)(i)(II), Pub. 936 p.13). Not the zero. | **Yes** (`personal-expense-grandfathered-on-cutoff`). |
| Personal expense, grandfathered before the cutoff (choice 3, P5 repair) | Same, box 3 `1985-01-01`. | Reason `possible-grandfathered-debt`. Not the zero. | **Yes** (`personal-expense-grandfathered-before-cutoff`). |
| Personal expense, not grandfathered, one day after the cutoff (choice 3, P5 repair) | Same, box 3 `1987-10-14`. | Reason `use-unrelated-personal-expense` — the zero publishes; the grandfathering check does not falsely clear a loan one day past the cutoff. | **Yes** (`personal-expense-not-grandfathered-after-cutoff`). |
| Personal expense, no timing answers (owner finding 1, P5 repair) | Personal expense, neither timing question asked. | Reason `timing-not-established`, not `cannot-tell-timing` and not the zero. Line 8a blocked `DEPENDENCY_ABSENT`. | **Yes** (`personal-expense-no-timing-answers`). |
| Personal expense, one timing answer missing (owner finding 1, P5 repair) | Personal expense, purchase timing answered favourably, building timing never asked. | Reason `timing-not-established` — the favourable answered question does not establish the zero while the other is open. | **Yes** (`personal-expense-one-timing-answer-missing`). |
| Personal expense, timing answer withdrawn (owner finding 1, P5 repair) | Personal expense, both timing answers favourable, then the purchase-timing finding retracted within the same run. | Reason `timing-not-established` — the withdrawal returns the fact to the reserved `not-asked` default, not to the zero it would otherwise have reached, and not to a missing row. | **Yes** (`personal-expense-timing-withdrawn`). |
| Purchase account, timing questions unasked (owner finding 1, P5 repair) | The supported purchase — identical to `supported-purchase`, named separately to record this coverage line explicitly. | `qualified`, unaffected: an unasked timing question never blocks a purchase account. | **Yes** (`purchase-account-timing-questions-unasked`). |
| Uncertain ownership, alone (choice 4, P5 repair) | `owns-the-home` `cannot-tell`, every other answer favourable. | Reason `cannot-tell-ownership`, not the generic `outside-coverage`. | **Yes** (`cannot-tell-ownership-alone`). |
| Uncertain residence, alone (choice 4, P5 repair) | `lives-there-most-of-the-time` `cannot-tell`, every other answer favourable. | Reason `cannot-tell-residence`. | **Yes** (`cannot-tell-residence-alone`). |
| Uncertain sole-obligor statement, alone (choice 4, P5 repair) | `no-one-else-owes-it` `cannot-tell`, every other answer favourable. | Reason `cannot-tell-share`. | **Yes** (`cannot-tell-share-alone`). |

The personal-expense, zero-interest, and "standard deduction stays
larger" rows share line 12e's `15000`. The unresolved field versus the
basis section is the expected difference between the first and the
second (**probe result**: confirmed directly). The third shows a
qualifying amount that does not change the deduction.

**Not run as a demonstration but probed directly as
`determined-zero-reader-gap`, reconfirmed unchanged this round:** a
four-favourable-value declaration (the first named fix in "The conclusion
carrier") raises `PresentationModelError: declared read ... has no single
expected value` against the real, unmodified `presentation_projection.py`.
This is evidence that the gap is real and exactly located, not evidence
that a production charter can close it without all three named reader
changes.

## 7. Contracts and divisions

### Production execution clarification

ADR 0078 is now owner-accepted. The production bundle and previously
unpublished rule ids use first production version v1; the prototype's v3
labels remain experimental evidence. Unit B starts from actual core package
v43, replacing its legacy line 8a **v2** producer, not merely the old v1 file.

The original division below put all reader changes in unit C. Its nonempty
expected-value-set compatibility fix is now included with unit B, because the
selected unresolved indicator cannot render genuinely unresolved cases without
it. Unit B ships that fix with the four-value completed-outcome gate. Unit C
still owns the generic basis loader, the completed-zero explanation section
and the payer label. This is an execution-order adjustment, not a change to
the condition table or the four-part product goal. The Track 2 charter is the
current work packet for that division; historical probe limitations below do
not become production acceptance criteria.

### Contract changes

| Change | What | Why |
| --- | --- | --- |
| New ADR | **ADR 0078, accepted on review.** `date_compare` on `rule-artifact.v14`/`artifact-package.v36` (reviewed in the date-unit review). The ADR itself awaits only the owner's formal acceptance; its result is used exactly as reviewed. The basis loader is still ADR 0077 Part 2's reader, which was implemented for two rule ids. Finishing it for any pinned rule, and the third reader change above, add no new contract. A sentence on the published line 12e value is not proposed. ADR 0073 is applied as written. ADR 0077 Part 5 is not extended: no registry pair is added. ADR 0075 and ADR 0076 are not used. |
| Schema successor | **`rule-artifact.v14` and `artifact-package.v36` (P5 repair), used exactly as ADR 0078 reviewed them.** `fact-type.v2` (including a second version of the same id, box 9's successor — see "New content bundle" below), `form-field.v3`, and `rule-artifact.v13`'s unchanged shapes (`subject`-scoped dispatch, `collect_categorical_all_equal`, `selection`) already admit every other citizen this draft names, confirmed by `p3_probe.py`/`p4_probe.py`/`p5_probe.py` actually building and running them. No published schema file is edited, and `published.json` is not rewritten; ADR 0078's own checksums are already appended, independently reviewed and reconfirmed. |
| **Reader generalization (choice 8's remaining carrier gap) — recommendation, three changes now named precisely** | **Deferred, not built.** (1) Widen the unresolved field's `when` to exclude all four determined values (content only, probed). (2) `presentation_projection._favorable_values` and the `len(favorable) != 1` check in `_selection_blocked_reasons` assume a declared read's favourable set is exactly one value (code change, confirmed by live reproduction, section 2 "The conclusion carrier" and section 4). (3) **Named this round.** The basis-section gate (section 4) must widen beyond "pins the limit parameter" to also admit a literal-zero publication from one of the three decisive-zero reasons, building its content from that reason's own `description` — without this third change, fixes (1) and (2) alone leave a determined zero with *no* account at all (P4 re-review finding 1). | **Recommendation: build all three together**, in a later, separately chartered unit (each is pure Python in `presentation_projection.py`, no schema successor). Every existing caller (the two student-loan selection rules) is unaffected by (2); (1) and (3) are new, mortgage-specific call sites. Without them, a determined zero stays shown through the blocked field — a product defect choice 8 names, not a cosmetic one. `determined-zero-reader-gap` (`p5_probe.py`) reproduces the unmodified failure live, unchanged from P4. |
| New content bundle | `tax.us.2025.f1098-successor.vocabulary` production version `v1` (the temporary probe uses `v3`, an unpublished experiment label), for the nine statements (finding 3's split), the two timing facts (choice 3, now with the fourth reserved value `not-asked`), the expanded reason category (fifteen non-qualified values in P5, seventeen in this P6 prototype), the inert placeholder fact, and (P5 repair, finding 5) **box 9's genuine successor version, `tax.us.2025.f1098.box9-number-of-properties` `v2`** | `f1098.bundle.json` stays as published bytes, byte-identical and untouched this round (unlike P4, which had to mutate a copy of it to work around the same-version substitution finding 5 flagged). Box 9 `v2` is a new fact-type *version* of the same id, carrying `optional_default` the real, published `v1` lacks — not an edit of `v1` and not a second `v1`. Existing recorded box 9 values resolve under a `v2`-admitting package because this corpus's finding-to-symbol binding (`packages/derivation/marshal.py`'s `_fact_id_has_type`) matches a current finding to its symbol by fact-type *id* alone, and `finding.v2` findings (this probe's own, and every adopted Form 1098 finding) carry no fact-type version pin to begin with — read directly from the code, not argued; `p5_probe.py` builds this exact shape (both the real, untouched `v1` bundle and the new `v2` bundle member coexisting in one package) and every case runs against it. This is probe-only evidence; no schema or adopted content changed. |
| New parameters | `tax.us.2025.parameter.f1098-box9-default-single-property`, value `1` (finding 5, unchanged); **P5 repair, value changed:** `tax.us.2025.parameter.f1098-timing-purchase-structural-default` and `tax.us.2025.parameter.f1098-timing-building-structural-default`, both now value `not-asked` (was `more-than-90-days`/`no` in P4, withdrawn by the owner's review as a disguised assumption) | Finding 5's repair, and the reserved-sentinel default the two timing facts need so a subject-scoped rule's exhaustive `requires` join resolves for every subject, not only personal-expense ones (see "Condition table" and "The chain"; ADR-0037's `conditional_dependency_set` was assessed and set aside — it governs evaluation inside `value`, not which types the join admits). Same declared shape as the existing `taxpayer_over_65` / `tax.us.2025.parameter.default-false` pair, but — unlike box 9's blank-means-one, which is a real-world Form 1098 instruction — the sentinel value is purely structural: it is never confused with a real answer, because the value tree checks for it explicitly and routes it to its own open-condition reason. |
| Package successor | `tax.us.2025.package.core-calculations` version `v44` (unchanged number — already the number after the real, adopted `v43` line 8a fix), schema **`artifact-package.v36`** (P5 repair, up from `v35` — admits the `rule-artifact.v14` rules below) | v42 pins line 8a `v1`; the real, adopted `v43` is the unrelated debt-limit fix and is not superseded or touched by this design. The package includes the new bundle and the three parameters, **one** line 8a rule and **one** reason rule, now `rule-artifact.v14` (each with internal branches, not four or two — finding 6's repair, and the rejected split-rule attempt above), the unresolved rule (`rule-artifact.v13`, unchanged — it does not use `date_compare`), and the unresolved field; gains three `input_bindings` entries (box 9's `v2` and the two timing facts' `optional_default`s). Because there is exactly one producer of each symbol, **no `conflict_semantics` entry is needed for either.** v42's bytes and checksum stay. **Probe result (P5 repair):** `p5_probe.py` builds this exact shape (as `v44`, in a temporary registry) and runs it through `live_coordinate_run` for every case in section 6 marked "Probed: Yes." |
| Release successor | `demo.release.sli-worksheet-integration.2025` version **`v42`** (P5 repair, renumbered from P4's `v41` — the probe pins its own synthetic checksum, not a new release file) | **P5 repair.** P4's recommended `v41` is now taken: the real, adopted line 8a fix ships as release `v41` for real (accepted on review). This design's own successor release, which was never the same release as that fix, is renumbered to the next free number, `v42`, so it no longer collides with the adopted release. v42 would pin the `v44` package checksum. The v40 and v41 release files stay. A workspace adopted to v41 or earlier keeps its current path until it adopts v42. |

### Production divisions

Four units. Each is one charter. Calculation and the unresolved field
land together, as before: a package that has the dollar rule without the
field, or the field without the dollar rule, fails the "one account"
demonstration. **New this round (choice 10):** unit D, the recording
operation, so the person can actually supply the account — the part of
the four-part goal no earlier unit reaches.

| Unit | Delivers | Depends on |
| --- | --- | --- |
| A. Statements | The new bundle (nine statements, the two timing facts with their fourth reserved value, the reason category, the inert marker, box 9's `v2` successor) and the three parameters. Tests admit every value in section 1 and section 1a, including `cannot-tell` and (reserved, package-default-only) `not-asked`, keep two statements on different fact ids, correct by a later assertion, and retract without writing an opposite value; confirm box 9's and each timing fact's `optional_default` resolves when absent and is overridden by a real assertion; confirm a box 9 value recorded before `v2` is admitted still resolves after. No rule and no package. | Nothing in this milestone. |
| B. Calculation | Package v44 (schema `artifact-package.v36`) and release v42: the one line 8a rule, the one reason rule (both `rule-artifact.v14`), the unresolved rule, and the field. The section 6 rows, checked as publications and dispositions through `live_coordinate_run`. The reason's descriptions are the content for section 3's narratives. The person-facing section is unit C. | A. |
| C. Reader | The general basis loader and the `payer` label; the gate that shows the line 8a basis section for a pinned-limit publication, and (P5 repair, the third reader change) for a literal-zero publication from one of the three decisive-zero reasons; **named but not yet specified as code:** the `_favorable_values` generalization. Tests: the supported and zero-interest publications show section 3; the determined-zero rows show the widened basis section; every other non-`qualified` row shows the unresolved field's reason sentence; a rule with no `basis` shows nothing; the student-loan support and cover guards still refuse what they refuse now; the line 12e number gains no sentence. The file is under `packages/derivation/`, so the full suite is the check for this unit. | B's outcome table matches section 6. |
| D. Recording (choice 10) | The bounded save/correct/withdraw/review operation section 8 specifies: identify the statement, answer (including `cannot-tell` and the two conditional timing questions — never `not-asked`, which is reserved), save, correct, withdraw, and review the saved account and explanation. Modelled on `packages/tax/sli_relationship_recording.py` and `sli_relationship_review.py`. Tests: section 8's "Acceptance cases" (P5 repair, including the absence and withdrawal cases choice 10's recording operation now names explicitly). | A, B, C (the saved account's explanation is unit C's output). |

No unit computes an allocation, adds a home or borrowing citizen, installs
an ADR 0077 Part 5 map, adds a `RECORD_CODES` entry, or edits line 12e.
The `date_compare` operator itself is not built by any of these units — it
is already built and reviewed, ADR 0078, as its own prerequisite unit; this
design only uses it.

### What review is checking

A reviewer can start from one ordinary answer, follow its fact id to the
arm in section 2, read that arm's basis (or its reason's description) in
section 3, see where the reader shows it in section 4, and apply a
correction or a withdrawal from section 5, or save it through the
operation in section 8. The section 6 row is the expected end of that
path. This draft does not accept itself. `p3_probe.py`, `p4_probe.py`, and
`p5_probe.py` built the respecified successor citizens in a temporary
registry and ran most of section 6's rows through them via
`live_coordinate_run`; the rows not probed are marked so in section 6's
table, and remain readings. The box 3 date-stop row for the
personal-expense zero is now built and probed (`possible-grandfathered-
debt`), not deferred. The third reader change (choice 8's remaining
carrier gap) is still a named, specified-but-unbuilt capability — its
negative evidence (`determined-zero-reader-gap`) is probed, not its fix.
The recording operation in section 8 is specified, not built; every
section 6 case still uses a direct synthetic assertion, which is that
round's own stand-in, named here rather than left implicit.

## 8. Recording operation (choice 10)

**New this round.** The first round, and `p3_probe.py`'s direct synthetic
assertions, showed only that the calculation is feasible — the third of
the four-part goal. Nothing in either round obtained and saved the
person's own account. This section specifies the bounded operation
through which a person identifies a recorded Form 1098 statement,
answers the nine ordinary statements and (when relevant) the two timing
questions, saves, corrects, withdraws, and reviews the saved account and
its explanation. It follows the shape `packages/tax/sli_relationship_recording.py`
and `sli_relationship_review.py` already prove for student-loan
relationships, carrying what transfers and naming what does not.

### What transfers from the student-loan recording module

- **One save, one batch.** `record_submission_durably` reads the log
  once, stages every act a submission needs (evidence, contribution,
  assertion, any retraction a changed answer displaces), and writes them
  with one `append_batch`: an interrupted save leaves the state before it,
  or the whole save, never a part. The mortgage operation's
  `record_f1098_statement_answers_durably` does the same for one
  statement's nine-or-eleven-answer submission.
- **Evidence-backed findings, not bare assertions.** Each answer is an
  `evidence-submitted` act (kind `tax.mortgage.f1098-statement-answer`,
  by analogy to `tax.student-loan.relationship-answer`) followed by a
  `contribution` and an `assertion`, admitted through
  `apply_contribution_batch` exactly as the student-loan recorder does.
  The saved explanation can then show which evidence backs which answer,
  the same account section 4's reader already reaches for a `basis`
  group's `said` items.
- **Correction is a later assertion of the same fact id; withdrawal is a
  named retraction.** ADR 0041 and ADR 0073 are applied exactly as
  `correct_relationship_claim_durably` / `withdraw_relationship_claim_durably`
  already apply them: a correction's evidence names the predecessor
  finding it replaces (where the student-loan module's reviewed-correction
  scope checks apply); a withdrawal's evidence names the one finding it
  ends and asserts no opposite claim. Section 5's table is the exact
  lifecycle this operation has to produce.
- **Review as a snapshot, revalidated before every save.** `prepare_review`
  and `_revalidate_review` snapshot the current, recognisable choices (here:
  the one current Form 1098 statement, by its `payer`/`statement`/
  `tax-year` identity, and its nine-or-eleven current answers) and refuse
  a save whose snapshot has gone stale — the mortgage review has only one
  statement to show, so it has no `_require_distinguishable_selection`
  work to do, but it keeps the same staleness check.
- **Correct→answer coupling.** A correction to one of the nine statements
  that changes whether the timing questions are even relevant (for
  example, `what-the-money-paid-for` corrected away from
  `unrelated-personal-expense`) ends the timing answers' *relevance*, not
  their standing — they stay current findings, simply unread by the
  rule's `value` tree once the use answer no longer reaches that branch
  (see "Which arm publishes"). This is unlike the student-loan recorder's
  `_stage_enrollment_follows_schooling`, which actively retracts an answer
  whose *subject* changed; here no subject changes, so no retraction is
  staged. Named so a later builder does not assume parity where none is
  needed.

### What does not transfer, and why

- **No relationship/link identity.** The student-loan recorder admits or
  denies a *link* between two already-identified subjects (a borrowing
  and a schooling, or a borrowing and a statement) — ADR 0076 Part 2's
  `joined_contains_subject` join. The mortgage route has one statement and
  no second subject to link; each of the nine-or-eleven answers is a
  plain ordinary statement on the Form 1098's own identity keys (section
  1, "The tie"). No `borrowing_ref`, no entity introduction, and no
  `link_outcomes_adopted` bundle-v2 branching are needed.
  `introduce_borrowing_reference_durably` has no mortgage counterpart.
- **No recognition-clue distinguishing.** The student-loan review has to
  tell two borrowings, two schooling situations, or two statements apart
  for the person (`_borrowing_cards`, `recognition_clue_labels`,
  `_require_card_distinguishable_in_workspace`). The opening case is one
  statement; there is nothing to distinguish it from. A later route that
  admits more than one Form 1098 statement would need this machinery; this
  one does not, and does not import it speculatively.
- **No statement-inclusion-scope or financing-outcome bundle.** The
  student-loan `STATEMENT_INCLUSION_SCOPE_UNRESOLVED`,
  `FINANCING_DENIED`/`UNRESOLVED`/`WITHDRAWN` triple, and
  `link_outcomes_adopted` version gate have no mortgage equivalent: this
  route's "no"/"cannot-tell" outcomes are already carried as ordinary
  fact values (`no`, `cannot-tell`) on the statement fact itself, not as
  a separate outcome-pair bundle keyed by a link.

### The bounded operation's four acts

| Act | Student-loan model | Mortgage shape |
| --- | --- | --- |
| Identify | The statement and borrowing cards `prepare_review` shows | The one current Form 1098 statement, by `payer`/`statement`/`tax-year` |
| Answer | `_submission`'s `financing_response`/`inclusion_response` pair | The nine ordinary statements, each `yes`/`no`/`cannot-tell` or its own enum, plus the two timing facts (**reserved value `not-asked` never offered — P5 repair**), included in the submission only when `what-the-money-paid-for` is `unrelated-personal-expense` in the *submitted* answers — the recorder decides relevance from the submission itself, not from the prior saved state, so a first-time personal-expense answer can include its own timing pair in the same save |
| Save / correct / withdraw | `record_submission_durably` / `correct_relationship_claim_durably` / `withdraw_relationship_claim_durably` | `record_f1098_statement_answers_durably` / `correct_f1098_statement_answer_durably` / `withdraw_f1098_statement_answer_durably`, one per statement-keyed fact, following ADR 0041/0073 exactly |
| Review | `prepare_review`, revalidated by `_revalidate_review` before `save_review` | `prepare_f1098_statement_review`, showing the one statement's current nine-or-eleven answers, the reason category once computed, and the basis or unresolved sentence section 4 reads for the current disposition |

### Acceptance cases (P5–P7 corrections)

The recording operation's own test surface, named explicitly rather than
left to unit D's charter to invent. Each case below is a save, correction,
withdrawal, or review the operation must accept or refuse, stated as a
behavior the unit's tests check — not run against real code this round
(choice 10 is specified, not built; section 6's cases all use a direct
synthetic assertion instead).

- A first save admits all nine statements and, only when
  `what-the-money-paid-for` is submitted as `unrelated-personal-expense`,
  the two timing facts in the same batch.
- **Production entry clarification:** that first-save case describes the
  batch API, not a ban on incremental entry. The single-answer API may begin
  an incomplete account and may restore answers after withdrawal. Required
  answers that are still absent leave the amount blocked; admitting one answer
  is not evidence of a complete account. This is the selected disposition of
  independent production finding 8.
- A first save with `what-the-money-paid-for` submitted as anything other
  than `unrelated-personal-expense` admits the nine statements and refuses
  (or silently ignores — the production charter decides which, and must
  say so) a submitted timing answer, since the recorded account never asks
  for one.
- A save admits `cannot-tell` on any of the eleven submittable answers.
- The payment answer uses the four P7 meanings: full payment by the filing
  unit (`yes`), somebody else paying some/all or only partial payment by the
  unit (`paid-by-others-or-partial`), no payment by or for either filing
  spouse (`no`), or uncertainty (`cannot-tell`). It does not collect payer
  identities, amounts, or gift-law conclusions.
- A correction from supported payment `yes` to
  `paid-by-others-or-partial` on the same statement key re-derives
  `payment-outside-coverage`, publishes no line 8a amount, and blocks line
  12e. The current explanation and publication support the replacement
  finding, not the displaced `yes` finding.
- A further correction from `paid-by-others-or-partial` back to `yes` on
  that same key re-derives the supported result and pins only that current
  answer. A correction is not a withdrawal and must not revive either
  displaced answer.
- `no` is accepted only for neither filing spouse paying any and nobody
  paying any for them; it is the bounded `not-paid` zero. A payment by
  someone else or only partial payment must never be translated to this
  answer.
- A joint-filer save where the responding spouse is not on the note but
  the other spouse owes the loan and paid the interest records `yes` for
  liability and payment, and `yes` for the sole-obligor answer when no one
  besides the filing spouses owes the loan; the saved explanation reaches
  the qualified case.
- **P5 repair.** A save that omits both timing facts, where use is
  `unrelated-personal-expense`, is accepted: the statement is saved with
  those two facts absent, exactly the "timing questions unasked or not yet
  answered" case — it is not refused for incompleteness, because an
  in-progress submission is a real, inspectable state (section 4's
  `timing-not-established` reason is what the person then sees).
- **P5 repair.** A save that supplies one timing fact and omits the other
  is accepted the same way.
- **P5 repair.** Correcting `what-the-money-paid-for` away from
  `unrelated-personal-expense` (to `bought-the-home`, `other`, or
  `cannot-tell`) does not retract the two timing facts, if any were
  already saved — section 5's "Correct→answer coupling" note: they stay
  current findings, simply unread by the rule once the use answer no
  longer reaches that branch.
- **P5 repair.** Withdrawing one timing fact, while use stays
  `unrelated-personal-expense`, is accepted and ends that finding's
  support; the saved review (below) must show the resulting current state
  as the package's own `not-asked` default, not as a blank the review
  cannot explain and not as `cannot-tell`.
- **P5 repair.** Withdrawing both timing facts in the same correction
  batch is accepted, following `record_submission_durably`'s one-batch
  guarantee (section 8, "What transfers") — an interrupted save leaves the
  state before it or the whole withdrawal, never one fact withdrawn and
  not the other.
- A review snapshot taken before a correction or withdrawal lands, then
  used for a save after a concurrent change landed first, is refused as
  stale — the same `_revalidate_review` check the student-loan review
  performs, unchanged by any P5 fact.
- A review of a statement whose timing facts are at their `not-asked`
  default shows that condition distinctly from a statement whose timing
  facts were genuinely answered `cannot-tell` — the review must not
  collapse the two into the same displayed state, matching section 4's
  reader distinction.

### What this section does not do

It does not build the module above; it specifies it, for a later,
separately chartered production unit (unit D, section 7). It does not
change `packages/tax/sli_relationship_recording.py` or
`sli_relationship_review.py`; those stay the model, not a dependency —
the mortgage module is new content on the same pattern, not an import of
student-loan identity. It does not record a home, a borrowing, or a
property address as its own citizen; the tie stays exactly what section
1 already established. No case in section 6 is run through this
operation; every case still uses a direct synthetic assertion, named
here as this round's own stand-in.

## Track 0 adversarial closure

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate." Evidence
below is this design's text (sections 1–8) and
`p3_probe.py`/`p4_probe.py`/`p5_probe.py`'s measured results, not argument.
Where a probe did not run a row, this closure says so rather than treating
the design account as the evidence. This revises the P4 round's six
artifacts for the P5 repair; it does not restart the gate from nothing.

### 1. Authority-lifecycle table

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `tax.us.2025.f1098.box1-mortgage-interest` | Reported mortgage interest, box 1 | One statement (`payer`, `statement`, `tax-year`) | The Form 1098 the lender furnished | A later assertion on the same keys (correction); the `tax.us.2025.f1098` family's closure changing the member set |
| `tax.us.2025.f1098.box2-outstanding-principal` | Reported outstanding principal, box 2 | Same statement | Same form | A later assertion; now actually read (finding 1) by the line 8a rule's guard |
| `tax.us.2025.f1098.box3-origination-date` | Reported origination date, box 3 | Same statement | Same form | Required; **P5 repair:** now read for the personal-expense zero's grandfathering check (not for the supported arm, choice 7, unchanged); a later assertion re-evaluates that check |
| `tax.us.2025.f1098.box9-number-of-properties` **v2** (P5 repair, finding 5) | Reported property count, box 9 | Same statement | Same form, or its `optional_default` of `1` when absent (finding 5) | A later assertion of a real value supersedes the default (the default is never a current finding; it is a declared-default pin, so there is nothing to invalidate by correction — only a real assertion can displace it). **P5 repair:** `v2` adds `optional_default` to the fact type's own declaration (finding 5's repair — the real `v1` has none); a value recorded under either version resolves the same way, since this corpus matches a current finding to its symbol by fact-type id, not by the type's own schema version. |
| The nine new ordinary statements (section 1) | The person's own account of ownership, residence, security, liability, payment, share, use, originality, certificate receipt | Same statement keys | The person's own answer | A later assertion (correction, ADR 0041); a retraction (withdrawal, ADR 0073) |
| The two timing statements (choice 3, P4 repair, P5 repair) | The person's own account of when this loan was taken out relative to the purchase, and relative to building or improving | Same statement keys | The person's own answer, or the reserved sentinel `optional_default` of `not-asked` when absent | A later assertion; a retraction returns the fact to its sentinel default rather than to a missing row — named in section 5 as a difference from every other ordinary statement's withdrawal direction. **P5 repair:** the default is no longer a favourable real-world value (P4's withdrawn "more than 90 days"/"no building work"); it is a reserved marker the value tree never confuses with a real answer. |
| `tax.us.2025.f1098.residence-interest-reason` | The one classification of why this statement's interest is or is not qualified, now nineteen values total: `qualified` and eighteen non-qualified reasons. P7 adds `payment-outside-coverage` to P6's eighteen total values. | Same statement keys, per-subject dispatch | Every one of the nine statements, box 2, box 3 (P5 repair), box 9, the two timing facts (by value or sentinel default), filing status — all current | Any one input's correction or retraction re-dispatches this rule for that subject; it is derived, never itself corrected or retracted |
| `tax.us.2025.f1098.residence-interest-unresolved` | Whether an open condition remains for this statement | The run (one subject, this route's bound) | The reason rule's publication for the same subject; the `inert-path-unwritten` marker (never current) | The reason rule's own invalidation, transitively |
| `tax.us.2025.f1098.mortgage-interest-limit` v1 | The post-2017 acquisition-debt limit by filing status | Parameter, not per-statement | 2025 law (§163(h)(3)(F); Publication 936) | A later version of the parameter; not asserted or retracted like a finding |
| `tax.us.2025.parameter.f1098-box9-default-single-property` v1 | The declared default for an absent box 9 | Parameter | The Form 1098 instructions' own "may leave blank" rule | A later version of the parameter |
| `tax.us.2025.parameter.f1098-timing-purchase-structural-default` / `-timing-building-structural-default` v1 (P4 repair; **value changed, P5 repair**) | The declared sentinel default (`not-asked`) for an unasked or withdrawn timing question | Parameter | A subject-scoped rule's `requires` join, not a real-world "blank means X" fact — named distinctly from box 9's default for this reason | A later version of the parameter |
| `tax.us.2025.f1098.source-closure` | The Form 1098 family is closed (with or without members) | The horizon the closure finding names | The person's closing assertion | A later closure assertion naming a different, later horizon (ADR-0014) |
| `tax.us.2025.f1098-scope.no-mortgage-statement` | Whether the person declares no Form 1098 at all | The return, `tax-year` | The person's own declaration | A later assertion; checked together with the family's observed count, never trusted alone (adopted `F1098_SCOPE_CONTRADICTION` guard, carried unchanged) |

Storage identity is not authority scope: box 1/2/3/9 share identity keys
with the nine statements but are not the same authority — a box
correction never rewrites an answer, and an answer correction never
rewrites the form (section 5). Finding 1 was exactly an authority that
did not invalidate when its own input (box 2) changed; this revision's
repair makes the box 2 value load-bearing on the authority it already
claimed to depend on.

### 2. Empty/nonempty authority matrix

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighbouring result |
| --- | --- | --- | --- | --- |
| Closed empty | Scope flag asserted `true`, family genuinely closed with 0 members (adopted `F1098_SCOPE_CONTRADICTION` guard holds) | Inapplicable | Line 8a inapplicable; reason rule not dispatched (no box 1 subject); unresolved field inapplicable | Line 12e selects the standard deduction, citing the flag, not box 1 (**probe result**, `closed-empty`); the Schedule A total's closed-empty producer (unchanged) supplies the zero subtotal; an unrelated student-loan return's own line 21 is untouched (design-level reading, not re-run this round — P0 already established no shared symbol) |
| Closed empty | Flag absent, or flag `false` with a genuinely empty family | Blocked | Line 12e blocks `DEPENDENCY_ABSENT` or `F1098_SCOPE_CONTRADICTION` (adopted guard, unchanged) | Unaffected — the adopted guard, not this revision's content |
| Nonempty | One current statement, every one of the nine answers favourable, box 2 at or under the limit | Eligible, positive | Line 8a publishes box 1; reason `qualified`; unresolved field inapplicable; attachment published when the total exceeds the standard deduction | Schedule A total (nonempty producer) requires and reads line 8a; line 12e refs it (**probe result**, `supported-purchase`) |
| Nonempty | One current statement, ineligible (a zero arm, cannot-tell, a refinance, a received certificate, a timing exception, timing never established, a possible grandfathered loan, uncertain ownership/residence/share/collateral/payment, an owner not on the note, a payment outside coverage, or box 2 over the limit) | Negative or blocked, explicitly, per arm | Line 8a publishes literal `0` only for the three determined-zero arms and blocks for every other open or excluded condition. (**P7 targeted prototype:** third-party/partial payment and cannot-tell payment block; genuine no-payment produces zero. P7 also observes correction/current support, actual MFJ status and 30,000 line 12e, and the stock example stored as `other`.) | A published zero is available to Schedule A total and allows line 12e to select the configured standard deduction. A blocked line 8a instead leaves dependent totals and line 12e unresolved. These are distinct paths; section 6 and the production tests check them. |
| Nonempty, two statements | `count` greater than 1 | Blocked `MULTIPLE_F1098_OUT_OF_SCOPE` | Line 8a blocks on its own `when`, before any of the nine answers are read | Unchanged from the adopted route; not separately probed this round (P0/P2 already measured this shape on the adopted rule, and this revision's guard is the same count compare) |

### 3. Late-authority counterexample

```text
attest → close → compute → add member → reclose → recompute
```

Run against the Form 1098 family's closure, the aggregate declaration
this design depends on (box 1's family-level closed/closed-empty
authority, not the per-statement box facts, which are not aggregates):

1. **Attest.** The person's lender furnishes a Form 1098; its box 1
   finding is asserted on `demo.f1098.lender.a`/`demo.f1098.stmt.a`.
2. **Close.** The person asserts the family closed, naming a horizon
   with that one member. `require_closed` now passes.
3. **Compute.** With every other answer favourable, the line 8a rule
   publishes box 1; the Schedule A total, attachment, and line 12e
   consume it. This is the `supported-purchase` probe result.
4. **Add member.** A second Form 1098 statement's box 1 is asserted
   (`demo.f1098.lender.b`/`demo.f1098.stmt.b` in this corpus's existing
   convention). The closure finding from step 2 still names a horizon
   whose member set the new assertion has outgrown — ADR-0014's closure
   authority is keyed to a specific horizon, so the OLD closure finding
   does not retroactively claim the new member exists, and the new
   member is not yet part of any *closed* horizon until a new closure
   act names a successor horizon that includes it.
5. **Reclose.** The person (or the application, on the same worked
   pattern this corpus already proves for a second F1098 statement —
   `MULTIPLE_F1098_OUT_OF_SCOPE`) asserts a new closure naming the
   successor horizon with both members.
6. **Recompute.** `count` is now `2`. The line 8a rule's own `when`
   blocks `MULTIPLE_F1098_OUT_OF_SCOPE` before any of the nine answers
   are read. The step-3 publication is superseded: `self.symbols` for
   `tax.us.2025.schedule-a.line8a` no longer holds the old value once the
   rule is re-attempted against the new state; the Schedule A total and
   line 12e re-derive from the new (blocking) disposition, not from the
   stale publication.

What becomes unusable at step 6: the step-3 line 8a publication, and
everything pinned to it (the Schedule A total's nonempty producer, the
attachment's tie-out, line 12e's refs). Nothing about the nine ordinary
statements, or the two new timing statements, becomes unusable — they
are per-statement, not per-family, and the second statement's own
answers (if any) are a second, independent account this route still
does not compute (outside coverage by `count`). This trace was not run
live this round (P0/P2 already measured the equivalent shape —
`MULTIPLE_F1098_OUT_OF_SCOPE` on a second statement — on the adopted
rule; this design's guard reproduces the identical compare on `count`,
unchanged by the P4 repair); it is a design-level trace corroborated by
that prior measurement, not a fresh probe run.

### 4. Claim-reuse proof

| Reused claim | Same proposition? | Same identity and lifecycle? | Same authority scope and explanation? | Verdict |
| --- | --- | --- | --- | --- |
| `tax.us.2025.rule.form1040-line12e` v1 | Yes — "the chosen deduction is the larger of the standard or itemized amount," unchanged | Yes — same id, version, `requires`, guard structure; this revision edits nothing in that file | Yes — its own explanation (the word "blocked" on any block) is unchanged; this revision deliberately does not attach a sentence to it (section 4) | **PASS** |
| `tax.us.2025.rule.schedule-a-total` / `-closed-empty` v1 | Yes — "Schedule A's total is the sum (or zero) its members produce" | Yes — same ids, versions; `requires: ["tax.us.2025.schedule-a.line8a"]` unchanged | Yes — reused exactly, reading whatever the (now single) line 8a producer publishes | **PASS** |
| `tax.us.2025.f1098.mortgage-interest-limit` v1 | Yes — "$750,000 ($375,000 MFS) is the post-2017 acquisition-debt limit" | Yes — same parameter id/version | **Changed, not merely reused: finding 1's repair.** The adopted rule cited this parameter as its stop but never compared a real box 2 value against it. This revision makes the comparison load-bearing. The proposition and the parameter are unchanged; what changed is which expression reads it. Named here so the repair is visible as a claim-reuse question and not mistaken for a new parameter. | **PASS, with the named repair** |
| `tax.us.2025.f1098.box1-mortgage-interest` / `box2-outstanding-principal` / `box3-origination-date` (fact types) | Yes — each is the Form 1098's own reported box, unchanged | Yes — same ids and versions | Yes, unchanged — box 3's meaning does not change by being newly read (P5 repair) | **PASS** |
| `demo.parameter.standard-deduction-base.2025` v1 | Yes | Yes | Yes — unchanged, same known non-2025-exact configuration P0 already recorded | **PASS** |
| The eight adopted confirmations (`tax.us.2025.f1098.liable-and-paid`, etc.) | **Not reused.** Section 1 and section 5 ("Legacy confirmations") are explicit: new ids, no copied value, the old findings stay unread. | N/A | N/A | **N/A — deliberately not a reused claim** |
| `tax.us.2025.rule.f1098-residence-interest-reason` / `-unresolved` v1 → v2 (P4 repair) → v3 (P5 repair) | **Changed proposition at each step, named rather than silently reversioned.** v1 claimed "qualified or one of seven reasons," gated the supported arm on eight statements without `owes-the-loan`. v2 claims "qualified or one of ten reasons" and adds `owes-the-loan` as a gate — a real change to which accounts the supported arm covers (choice 1). **v3 (P5)** claims "qualified or one of fifteen reasons": it adds the grandfathering check (a real account that was previously the deferred, unchecked zero now resolves to `possible-grandfathered-debt` instead), and it reclassifies three uncertainty cases from the generic `outside-coverage` to their own categories — each a real change to the account the rule returns, not an additive content successor. | Same ids; version bumped at each step. | Changed, named at each step: a grandfathered personal-expense account moves from "zero" (v2) to "possible-grandfathered-debt, outside coverage" (v3); a standalone identity uncertainty moves from `outside-coverage` (v2) to its own category (v3). | **Versioned as a changed claim, not reused, at each step** |
| `tax.us.2025.f1098.mortgage-interest-limit` v1 (P4 repair, reconfirmed, unaffected by P5) | Unchanged from the first round's PASS-with-a-named-repair. | Unchanged. | Unchanged — still read directly by the box 2 compare, now inside a longer priority chain; the comparison itself is untouched. | **PASS, carried forward** |
| `tax.us.2025.f1098.box9-number-of-properties` v1 → v2 (P5 repair, finding 5) | **Additive declaration, not a changed proposition.** v1 and v2 both claim "the statement's reported property count, blank meaning one." v2 only adds the `optional_default` declaration v1 lacks — the same real-world meaning, now machine-checkable when blank. | Same id; version bumped; identity keys unchanged. | Unchanged meaning; a value recorded under either version resolves to the same current finding, confirmed by reading `marshal.py`'s id-only finding-to-symbol match (section 7). | **PASS, versioned as additive, not a changed claim** |

### 5. Neighbouring-capability dependency diff

| Neighbour | Prerequisites before this design | Prerequisites after this design | Justified by |
| --- | --- | --- | --- |
| `tax.us.2025.rule.form1040-line12e` | `demo.form1040.standard_deduction`; `tax.us.2025.f1098-scope.no-mortgage-statement` | **Unchanged.** Still refs `tax.us.2025.schedule-a.line8a` by symbol, not by which rule produces it. | The symbol's meaning, not this revision — line 12e does not know or care how many rules used to produce it |
| `tax.us.2025.rule.schedule-a-total` / `-closed-empty` | `tax.us.2025.schedule-a.line8a` (nonempty producer); count-0 guard (closed-empty producer) | **Unchanged.** | Same |
| Schedule A attachment (`attachment.schedule-a.json`) | Ties out `tax.us.2025.schedule-a.line8a` through `_one_row`, which the adopted single rule already satisfied | **Unchanged in requirement, newly load-bearing in this design's own choice.** The attachment's existing `_one_row` cardinality is exactly why this revision collapsed four rules to one (finding 6) — the design had to be checked against this neighbour, not merely against the dollar figures section 6 already measured. | The attachment's own tie-out meaning, confirmed live by the probe's `double-match-qualifying` failure against the four-rule shape |
| A return with no Form 1098 statement at all | None of this route's facts | **Unchanged.** `closed-empty`'s probe result shows no new required fact: the flag and the family count are the only inputs, both already adopted. | The closed-empty row's own measured result |
| An unrelated student-loan (Form 1098-E) return | Its own closed family, its own twelve eligibility components | **Unchanged** — this design reads none of the SLI symbols, and the reason rule is dispatched on the Form 1098 (not 1098-E) subject type. Not re-run live this round; P0/P2 already established no shared symbol between the two routes, and this revision adds no new symbol either route reads. | Design-level reading, corroborated by P0/P2, not a fresh probe run |
| The student-loan recording and review modules (choice 10, P4 repair) | Their own ActLog, their own relationship fact types, their own link-outcome bundle | **Unchanged.** Section 8 models the mortgage recording operation on these modules' shape but imports no identity from them — no `borrowing_ref`, no link, no recognition-clue machinery. Neither module gains a mortgage-specific branch or dependency. | Section 8's own "What does not transfer, and why" |

### 6. Integration-surface artifact

`tax.us.2025.schedule-a.line8a` is **not** form-field-bound (finding 6's
own repair starting point — this was already true of the adopted rule).
It is bound by three consumers inside the derivation graph, and this
design is checked against all three, not only the dollar figure:

| Consumer | Binding artifact or join | Cardinality it expects | Satisfied by the design? |
| --- | --- | --- | --- |
| `tax.us.2025.rule.schedule-a-total` | `requires: ["tax.us.2025.schedule-a.line8a"]`, a plain `ref` | Any number of producers; reads whichever value is current | Yes, trivially, with one producer |
| `tax.us.2025.rule.form1040-line12e` | `ref` inside a `choose` | Any number of producers; reads whichever value is current | Yes, trivially, with one producer |
| Schedule A attachment itemization (`attachment.schedule-a.json`) | Tie-out row, resolved through `presentation_projection._one_row` | **Exactly one** disposition row for the symbol, on every path, including a losing or merely-attempted producer | **Only with one producer.** The probe's `double-match-qualifying` result is the negative case: a second producer, even a guard-disjoint one, raises `PresentationModelError` the moment the attachment is required. This design's one-rule repair is what makes "yes" correct here. |

`tax.us.2025.f1098.residence-interest-unresolved` **is** form-field-bound
(`tax.us.2025.form.f1098.residence-interest-unresolved`), one producer
(now a `rule-artifact.v13` selection rule unchanged by the P5 repair),
satisfying `_one_row`'s ordinary expectation — confirmed live for every
disposition path the probe ran. **Named limitation distinct from
cardinality, carried forward:** this field's single producer still
satisfies `_one_row`, but the three determined-zero reasons are still
routed through it pending the third reader change ("The conclusion
carrier," section 2, now three named changes) — a reader completeness
gap, not a binding-cardinality one; this gate does not treat it as
closing the integration surface, because it is a different property than
the one this gate checks.

`tax.us.2025.f1098.residence-interest-reason` binds nothing outside the
derivation graph. Its only consumer is the unresolved rule's
`reads_subject_results` declaration, which is not an external binding
and carries no cardinality obligation of its own kind — `_subject_results`
already fails closed on more than one result per subject (section 2,
"The chain").

**Synthetic end-to-end models, one per materially distinct disposition
path, built through the real consumers (`live_coordinate_run` plus
`build_presentation_model`), not argued. P5 repair closes the grandfathering
and identity-uncertainty rows the P4 re-review's own findings named, and
adds the three Publication 936 worked examples and the absent/withdrawn
timing cases:**

| Disposition path | Built? |
| --- | --- |
| Qualified, nonzero (supported) | **Yes** — `supported-purchase` |
| Qualified, zero reported (zero interest) | **Yes** — `zero-interest` |
| Disallowed, personal expense | **Yes** — `personal-expense-clean` |
| Disallowed, not collateral | **Yes** — `not-collateral` (standalone) and `not-collateral-and-personal-expense` (priority-ordering case) |
| Disallowed, not paid | **Yes** — `not-paid` (standalone) |
| Payment outside coverage | **Yes, P7 targeted** — `payment-other-person-paid-all`, `payment-partial`; correction reach `payment-correction-to-outside-coverage` |
| Corrected current payment support | **Yes, P7 correction-only** — `payment-correction-supported-start`, `payment-correction-to-outside-coverage`, `payment-correction-back-to-supported`; replaced support is absent after each correction |
| Publication 936 Example 1, investment `other` | **Yes, P7 targeted** — `pub936-example1-investment-other` (outside coverage; not a personal-expense timing result) |
| Outside coverage, owner not on note (choice 1) | **Yes** — `owner-not-on-note` |
| Outside coverage, timing exception possible (choice 3) | **Yes** — personal-expense analogues `pub936-situation2-building-before-completion`, `pub936-situation3-mortgage-after-completion`, `completion-exactly-90-days-before`, `paused-unfinished-project`, `preparation-before-physical-work`; purchase window both directions `purchase-within-90-days-before-home-buying` and `purchase-within-90-days-after-home-buying` |
| Determined disallowed, completion outside the window | **Yes** — `completion-18-months-before`, `completion-26-months-before-expenses-start-30-months-before`, `completion-40-months-before`, `completion-91-days-before` |
| Supported joint return where responding spouse is not on note | **Yes** — `joint-filer-other-spouse-obligor-and-payer`: stored filing status `married_filing_jointly`; the ordinary answer says the other spouse owes and paid; stored filing-unit values are `owes-the-loan=yes`, `paid-the-interest=yes`, `no-one-else-owes-it=yes`; observed reason `qualified`, line 8a `20000.0`, configured line 12e `30000`. |
| Unresolved, timing uncertain (choice 3) | **Yes** — `personal-expense-cannot-tell-timing` |
| Unresolved, timing not yet established (choice 3, P5 repair) | **Yes, P5 repair** — `personal-expense-no-timing-answers`, `personal-expense-one-timing-answer-missing`, `personal-expense-timing-withdrawn` |
| Outside coverage, possible grandfathered debt (choice 3, P5 repair) | **Yes, P5 repair** — `personal-expense-grandfathered-on-cutoff` (equality), `personal-expense-grandfathered-before-cutoff`; the negative case (not grandfathered) is `personal-expense-not-grandfathered-after-cutoff` and `personal-expense-clean` |
| Cannot-tell on use | **Yes** — `cannot-tell-use` |
| Unresolved, uncertain ownership/residence/share/collateral/payment alone (choice 4, P5–P6) | **Yes** — P6 ordinary answers “I can't tell whether the home is collateral for this loan” / “I can't tell which payment description applies”; stored value is `cannot-tell` on the respective question; observed reasons `cannot-tell-collateral` / `cannot-tell-payment`, with line 8a and unresolved field blocked. Cases: `cannot-tell-ownership-alone`, `cannot-tell-residence-alone`, `cannot-tell-share-alone`, `cannot-tell-collateral-alone`, `cannot-tell-payment-alone`. |
| Outside coverage (refinance) | **Yes** — `refinance`, `personal-expense-refinance`, `personal-expense-two-properties`, `uncertain-ownership-against-refinance` (an uncertain identity answer beside a refinance still reaches the generic residual, confirmed unchanged by the P5 repair) |
| Certificate received | **Yes** — `certificate-received` (standalone) and `personal-expense-and-certificate-received` (priority-ordering case) |
| Over the debt limit | **Yes** — `box2-over-limit` |
| Box 9 absent | **Yes** — `box9-absent` |
| Closed-empty | **Yes** — `closed-empty` |
| Deliberate double match, attachment inapplicable | **Yes** — `double-match-zero` |
| Deliberate double match, attachment required | **Yes** — `double-match-qualifying` (the negative case) |
| Reader completeness gap (choice 8) | **Yes, negative case, reconfirmed unchanged by P5** — `determined-zero-reader-gap`: the four-favourable declaration the first two named fixes would need raises `PresentationModelError` against the real, unmodified reader — the same failure that motivates the third named change. |

Every row the P4 re-review named as a repair the design had not yet
closed is now built live. No disposition path in section 2's condition
table is unprobed as of this round.

### Declaration

- Authority-lifecycle table: **PASS** — section above; storage identity
  versus authority scope distinguished for every row, including the two
  timing facts and their sentinel-default parameters, and box 9's new
  `v2` successor (P5 repair).
- Empty/nonempty authority matrix: **PASS** — four states given; the
  ineligible-nonempty P6 coverage spans all seventeen non-`qualified`
  categories; P7 adds targeted `payment-outside-coverage` and
  correction/current-support evidence, the other states
  unchanged from P4.
- Late-member lifecycle: **PASS** — trace given; corroborated by P0/P2's
  prior live measurement of the identical `count` guard, not a fresh
  probe run this round; unaffected by the P5 repair.
- Neighboring capability dependency diff: **PASS** — six neighbours
  listed, unchanged this round; the Schedule A attachment's own
  cardinality is still the row that changed this design (finding 6);
  unit D (choice 10) adds no new prerequisite to any neighbour; box 9's
  `v2` successor adds no new neighbour either (section 7).
- Reused-claim semantic/lifecycle equivalence: **PASS** — nine reused or
  versioned claims checked; the debt-limit parameter's reuse is
  PASS-with-a-named-repair; the reason/unresolved rules' v1→v2→v3 bumps
  are each versioned as a changed claim, not silently reused; box 9's
  v1→v2 bump is versioned as additive, not a changed claim.
- Integration surface: **PASS** — every binding enumerated and
  cardinality-checked; every materially distinct disposition path,
  including the grandfathering, timing-not-established, and
  identity-uncertainty rows the P4 re-review's findings named, is now
  built live through the real consumers. The reader carrier gap for the
  three decisive-zero reasons (choice 8) is a named, separate
  limitation, not an integration-surface defect — see below.
- Known limitations affecting correctness, each requiring an owner
  disposition before a production charter, not none:
  - **Choice 7's debt-limit defect** (carried forward, unchanged since
    P3): the adopted v42 rule never reads box 2; recorded in
    the milestone process log. (The unrelated, real, adopted v43 fix repairs this
    for the eight-confirmation path, not for this design's own successor
    content.)
  - **Choice 8's reader carrier gap** (carried forward; now three named
    changes, P5 repair). The three decisive-zero reasons are shown
    through the same blocked field as genuinely unresolved and
    unsupported reasons, pending all three reader changes named in
    section 4 and section 7. This is a correctness-of-explanation
    defect, not a correctness-of-amount one: the published dollar figure
    is right; the person-facing account of why is not yet separated the
    way choice 8 requires.
  - **Choice 10, carried forward.** The recording operation is
    specified, not built. Every probe case still uses a direct
    synthetic assertion. The fourth part of the milestone's four-part
    goal — the person can supply the account — has no implementation
    evidence yet, only a specification checked against the
    student-loan precedent's shape, now with named acceptance cases
    (section 8).
  - **Third-party and partial payment (P7).** These answers now have the
    separate `payment-outside-coverage` result, no line 8a amount, and a
    blocked dependent return; they no longer fall through to a determined
    zero. This route does not decide whether a specific payment made for
    the taxpayer is legally treated as the taxpayer's payment, or compute
    gift treatment or allocation. That treatment remains with the person
    (condition table row 2, section 3); this is a declared coverage bound,
    not an observed human-intake or recorder behavior.
  - **Grandfathering's narrow scope (P5 repair, newly declared, not a
    regression).** The `date_compare` check establishes only a *possible*
    grandfathered-debt case (box 3 on or before October 13, 1987,
    §163(h)(3)(D)); it does not verify continuous security or how a
    later refinancing of pre-cutoff debt would affect the result. A
    refinance already reaches `outside-coverage` through condition table
    row 6 before this check is ever reached, so the narrower scope does
    not misclassify a refinance as grandfathered — but it also does not
    attempt the fuller statutory test for the narrow case it does reach.
