# P0 increment A — one loan, two reports

Status: **P0 investigation complete; pending independent review and Foreman
disposition.** Increments A and B are source research and bounded synthetic
diagnostic evidence, not a product design or tax verdict. Initial source ref was `HEAD` at
`6332119a30f3420698bde5dcbce1fc81e93190ac`, on
`milestone/mortgage-statement-borrowing-same-loan`; at that ref the branch was
0 behind / 4 ahead of `origin/main`. This continuation's actual probe ran from
`HEAD` `75209121` and made no production or test edits.

## Plain-language account

Two Forms 1098 are two reports from a filer / reporting interest recipient.
They do not, by themselves, tell us whether a single loan stayed with the same
holder but moved to a new payment collector, the mortgage itself was acquired
by another holder, a borrower replaced an old loan by refinancing, two separate
loans are secured by the same home, or a report was corrected or duplicated.
The reporting filer, recipient named for collected interest, legal debt holder
and payment servicer may be different roles; the current application's
“lender” labels do not establish which role an entity has. Payer name, property
address, account string, amount, or matching dates alone cannot settle the
borrowing relationship. A person may be able to affirm “this is the same
continuing obligation” from their loan history or transfer notices; that is an
ordinary affirmation, not independent verification by the application.
Someone unable to tell should remain unresolved. No relationship field, loan
identifier, or default is selected here.

Keep distinct: each report and its reported amounts; a reporting recipient's
acquisition of a mortgage; the underlying borrowing and whether it continued
or was replaced; who holds or services it; the home securing it; and the
tax-year debt category and balance proposition. A report's annual interest is
report-local. Debt category, refinancing history, loan-wide balance and
all-debt limits are not established
by summing report-local amounts. In particular, one continuing borrowing with
two 1098s does not mean two debts, and two Box 2 observations do not imply that
their principal should be added or that either is the right limit balance.

## What the documents and tax sources establish

The April 2025 Form 1098 instructions say Box 1 is interest (not points)
received by the reporting interest recipient / filer from borrowers during
the calendar year (p. 5). Box 2 is principal outstanding January 1, except a mortgage originated
in the year reports principal on its origination date and a mortgage acquired
in the year reports principal on its acquisition date. Box 3 is the mortgage's
original origination date, not the date another filer acquired it; Box 11 gives
the date the mortgage was acquired when that occurred in the calendar year
(p. 6). The instructions also allow a collection agent to identify the person
for whom interest was collected in Box 10. So a Box 11 date is a report about
mortgage acquisition, not proof that a change in collection alone changed the
debt holder. The instructions' reporting distinction does not say
that a Box 2 observation is an annual average or determine how multiple reports
for one borrowing should be reconciled. ([2025 Form 1098 instructions, Boxes
1–3 and 11](https://www.irs.gov/pub/irs-prior/i1098--2025.pdf))

For tax year 2025, Publication 936 first distinguishes a full-deduction route
from its limited-debt calculation. Part I says a taxpayer who itemizes may
deduct all mortgage interest when the mortgages fit a listed category
throughout the year and combined debt is within the applicable limit; Figure
A on pp. 2–3 walks through those conditions. That branch does not require
Table 1's average-balance calculation. Part II's Table 1 addresses the
limited-debt calculation. For it, Publication 936 says to figure an average
balance for each mortgage; it offers methods with their own conditions,
including first/last balances, interest divided by rate, monthly closing or
average balances, or an annual average provided by the lender (pp. 13–14).
When the Table 1 limit is less than total qualifying average balances, the
publication prorates interest (p. 13). ([2025 Publication 936, Part I / Figure
A, pp. 2–3; Part II / Table 1, pp. 13–14](https://www.irs.gov/pub/irs-prior/p936--2025.pdf))

For the 2025 rule, the retrievable 2024 U.S. Code text of 26 U.S.C.
§163(h)(3)(A) and (B)(i) defines qualified residence interest and acquisition
debt, including its acquisition/construction/substantial-improvement purpose
and qualified-residence security. Pub. L. 115-97 §11043 added the temporary
2018–2025 limitation: $750,000 ($375,000 married filing separately), rather
than $1 million ($500,000 MFS). Pub. L. 119-21 §70108's effective-date clause
applies its later amendments only to tax years beginning after Dec. 31, 2025;
those later changes are not the rule stated here. ([2024 U.S. Code §163(h)(3)(A), (B)(i), GovInfo](https://www.govinfo.gov/content/pkg/USCODE-2024-title26/html/USCODE-2024-title26-subtitleA-chap1-subchapB-partVI-sec163.htm); [Pub. L. 115-97 §11043, GovInfo](https://www.govinfo.gov/content/pkg/PLAW-115publ97/html/PLAW-115publ97.htm); [Pub. L. 119-21 §70108 and effective date, GovInfo](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm))

For this case, the tax question is first which Publication 936 branch is
supported for the borrowing(s) across the year. The full-deduction route and
the Part II limited-debt calculation have different premises; the latter's
average-balance method is not mandatory for every below-limit case. The
application's one-report rule deliberately states a bounded premise
that Box 2 represents acquisition debt throughout the year and compares that
amount directly with its filing-status limit. Not being a general average
balance calculator does not alone make that bounded premise defective. What
remains open is whether two reports for a continuing borrowing can support the
same bounded premise or a different applicable branch without confusing
report-local amounts with loan-wide circumstances. ([26 U.S.C. §163, as
amended for tax year 2025 by Pub. L. 115-97 §11043](https://www.govinfo.gov/content/pkg/PLAW-115publ97/html/PLAW-115publ97.htm))

Still unanswered: whether the two reports concern one continuing obligation;
whether their reported interest periods overlap or leave a gap; whether either
is corrected or replaced; which 2025 branch applies; what evidence supports
the relevant balance through the year if the full-deduction branch is used;
and, if Part II applies, the appropriate average-balance method and all debt
entering the limit. The ordinary account does not establish that all relevant
home debt is represented. Do not extend the April 2025 instructions' summary
language to later tax years.

## Information status for the proposed case

| Class | What is known now | What remains unknown |
| --- | --- | --- |
| Supplied scenario | The plan's investigation case is one continuing home borrowing and two distinct 2025 reports. | Whether source documents really describe that case; report values and dates. |
| Reported | The 2025 reporting instructions assign meanings to Boxes 1, 2, 3 and 11 as above. | What actual synthetic fixture reports, and whether amounts overlap. Form labels do not prove the collector, holder and original creditor are the same party. |
| Person's ordinary affirmation | The person may recognize a continuing obligation and a lender/collector transition. | What they can affirm; whether the loan was refinanced, shared, or replaced. |
| Application defaults | The current review can display declared timing defaults separately from unanswered questions. | Whether current adoption selects those defaults and whether they are relevant. |
| Derived | Current content has a Box 2 / limit comparison and a Schedule A line 8a consumer. | Whether the adopted run receives the intended principal and filing status, and whether this case fits that rule's stated whole-year premise. |
| Unresolved | Same-loan identity and balance treatment are not established by documents' similar labels. | Which 2025 Publication 936 branch applies; relevant throughout-year facts for the full-deduction branch, or method/all-debt inputs for Part II; report completeness and any new supported relationship. |

## Exact current path and version map

The version boundary matters. README's mortgage example identifies core
calculations **v45**, published package registry **v43**, release
`demo.release.sli-worksheet-integration.2025` **v43**. The consolidation
baseline is core calculations **v49**, package registry **v47**, release of
that same id **v47**. Their exact files are:

| Artifact | Version/path | SHA-256 |
| --- | --- | --- |
| README package | `packages/content/tax/2025/package.core-calculations.v45.json` | `4e64cb5e5482f3c1060229429f497352b0d99f6e2f2289c68fad2c46419bcb7d` |
| README registry | `packages/content/tax/2025/published-packages.v43.json` | `b26bbd9ba2ce138cef0202c443dc1e0d5345e9bd69c7e27094fe0966015c6e9c` |
| README release | `packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/demo.release.sli-worksheet-integration.2025.v43.json` | `6755cd884faad0f11efef1b43e716dfef48eec4e3f53b200ec31ddb68426f862` |
| Consolidated package | `packages/content/tax/2025/package.core-calculations.v49.json` | `e18ec4032df22bf2ecc5b91794ae8f04c576ac2dce894ed1c9505a5c58615b03` |
| Consolidated registry | `packages/content/tax/2025/published-packages.v47.json` | `24057c68608179295df7b6668c92e196298ffb0dd37618fc58b4dadbb8b7f783` |
| Consolidated release | `packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/demo.release.sli-worksheet-integration.2025.v47.json` | `09d888121f726e8ae7728a7c2a1189ac83ec1a423b23f16ed09b7c7c92ad5fca` |

The v45/v43 and v49/v47 package selections both include mortgage family
`tax.us.2025.f1098` v1, closure mapping v1, mortgage vocabulary v1,
successor-answer vocabulary v2, limit parameter
`tax.us.2025.f1098.mortgage-interest-limit` v1, line8a rule v2, reason rule
v2, unresolved rule v2, and unresolved field v1. The release v43 points at
registry v43; release v47 points at registry v47. They are not the same
resolved run. The latest route should be resolved and pinned by the real
coordinator with v49/v47. Existing recorder tests instead seed v44/v42; the
old Track 2 mortgage goldens use v44/v42, and the earlier lifecycle tests use
a patched/historical route. Those remain useful route-specific evidence, not
proof of latest-package execution. For later synthetic setup, inspect the
latest-route helpers `_finish_acts_v49` and `_seed_workspace_v49` in
`tests/test_multiple_statement_candidate_repairs.py`; they are sale-specific
and cannot be reused as-is. Historical `_base_acts` setup comes from v44/v42
and strips circumstance answers, so any adaptation must be explicit. Prefer
the latest helpers where suitable, while preserving validated adoption,
closure, review and durable-save paths. The f1098 family v1 already authorizes
summing Box 1 across furnished reports; current single-report review,
recording and line8a restrictions alone do not imply a family successor or a
loan identity.

The source-to-consumer map is:

| Stage | Source and current independent constraint |
| --- | --- |
| Offered questions | `packages/tax/f1098_statement_review.py:prepare_f1098_statement_review` requires exactly one current Box 1 finding before it can show the finite per-statement review; the recorded statement determines the question keys. |
| Durable answers | `packages/tax/f1098_statement_recording.py:_require_current_statement` requires one exact current Box 1 source and exactly one current Box 1 source overall. Answer facts are keyed by payer, statement and year; they contain no same-loan relationship. Save also checks answer vocabulary, evidence identities and expected revision. |
| Support/closure | `packages/content/tax/2025/family.f1098.json` says closure means every furnished 2025 Form 1098 Box 1 amount is recorded. It is report completeness, not proof that all home debt is represented or that reports share a loan. `closure-mapping.f1098.json` maps that exact family/version to closure. |
| Principal and origination facts | `packages/content/tax/2025/f1098.bundle.json` gives Box 1, Box 2 and Box 3 the same report keys (payer, statement, year). They remain report-local; no borrower/loan link joins two reports. Current entity key/label is not evidence of legal holder versus collector role. |
| Marshalling | `packages/derivation/live.py` gathers declared family and rule source types; `packages/derivation/marshal.py:marshal_run_context` binds one unkeyed input per symbol (leaving unequal multi-matches unbound) while family members feed declared collections. Numerically agreeing Box 2 values do not prove common loan identity. |
| Rule and limit | `rule.f1098-line8a.v2.json` requires a closed family, explicitly blocks count >1 as `MULTIPLE_F1098_OUT_OF_SCOPE`, and admits count ==1. Its Box 2 ref is compared directly with the v1 filing-status parameter (`parameter.mortgage-interest-debt-limit.json`: $750,000 except $375,000 MFS); qualifying outcome collects Box 1. The rule basis expressly assumes Box 2 stands for acquisition-debt balance throughout the year. That is a disclosed premise of this bounded one-report branch; the fact it does not implement Part II's average-balance method is not by itself a defect. Whether two reports for one borrowing can support that premise or a different tax branch is open. `rule.f1098-residence-interest-reason.v2.json` declares a Box 1 subject and requires Box 2, Box 3, Box 9, circumstance answers, timing answers and filing status. The subject declaration does not establish that every requirement is bound to that subject's exact report facts: in the agreeing-Box-2 control, the B-labelled reason pins B Box 1, but pins A Box 2, A Box 9 and A's nine ordinary answers. Filing status is legitimately return-wide. |
| Consumer and saved explanation | `rule.schedule-a-total.json`, the Schedule A attachment, `form.f1098.residence-interest-unresolved.form-field.json`, and `packages/derivation/presentation_projection.py` produce the line and statement-level saved model. It retains statement keys, reported interest source, answer/default basis and rule references. `review_f1098_statement_with_saved_presentation` reloads and checks revision plus exact statement provenance; the model account is currently singular. |
| Existing correction paths | `f1098_statement_recording.py` has exact-answer correction and withdrawal operations; `tests/test_f1098_statement_review.py` covers correcting/withdrawing an ordinary answer. `tests/test_f1098_mortgage_interest_lifecycle.py` covers correction of Box 1 at the same statement identity and distinct-statement cardinality blocking. Form 1098 instructions direct corrected information returns to the general information-return instructions; those distinguish a correction to a previously furnished report from a new original report. This increment did not execute lifecycle behavior or establish a two-report same-loan correction contract. |

## Increment B — bounded synthetic observations

The diagnostic-only script is
`docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing-evidence/p0-current-path-probe.py`.
It built each live workspace in an ephemeral OS temporary directory because
the workspace residency guard rejects an ActLog inside the repository. It
copied only synthetic acts, derivation records, coordinator report, presentation
model and summaries to ignored
`temp/mortgage-statement-borrowing/20261022T004914Z/`; there is no machine
temporary locator in the evidence. These copies are diagnostic data, not a
second live workspace. The final bounded invocation completed in 21.452
seconds with exit 0, under the 300-second cap. It used the assigned read-only
read-only runtime, `PYTHONPATH=.`, and the following command shape (the local
runtime path was held in `$MORTGAGE_PYTHON` and is intentionally not persisted):

```sh
PYTHONPATH=. "$MORTGAGE_PYTHON" -c 'import subprocess,sys; sys.exit(subprocess.run([sys.executable,"docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing-evidence/p0-current-path-probe.py"],timeout=300).returncode)'
```

The real route was package `tax.us.2025.package.core-calculations@v49`
(`package_checksum` `d59bbf4f3205d213d4845f19b5010b7de3c8ed0c393e786c456a8ffe2d901040`),
registry `published-packages.v47.json`, release
`demo.release.sli-worksheet-integration.2025@v47` (checksum
`09d888121f726e8ae7728a7c2a1189ac83ec1a423b23f16ed09b7c7c92ad5fca`), package
adoption at ActLog index 201. Report disposition pins—not a guessed report-root
summary—show the v49 adoption and actual inputs. The unchanged mortgage family
is v1 with its v1 closure map and the selected answer vocabulary is v2.

The latest-route seed is an explicit adaptation, not a historical golden.
It starts with the sale-specific latest closed-empty base and its v49/v47
adoption (`tests/test_f1099k_personal_item_sale_track1.py:_make_base_acts`,
`tests/test_multiple_statement_candidate_repairs.py:_finish_acts_v49`). It
retains that base's unrelated closed-empty family versions, including the
Form 1099-K v2 family/closure mapping and v3 vocabulary needed by v49. From the
historical v44/v42 mortgage helper it keeps only report facts, scope and the
true mortgage-family closure; it strips ordinary/timing answers and the old
successor-vocabulary adoption, then explicitly adopts mortgage-answer v2
before review. It preserves the helper's one-report mortgage closure in the
one-report cases; the two-report case uses the helper's two-member closure.
The latest package adoption is validated and remains last; no post-run output,
closure or adoption was substituted to make a case pass. The v49/v47 helper is
sale-specific, so this is diagnostic composition, not a reusable general seed.

### Cases

| Synthetic case | Actual observation | What it does not establish |
| --- | --- | --- |
| One report, Box 1 $20,000 / Box 2 $200,000 | Before save, all nine ordinary v2 questions were absent; two timing questions were absent with separately declared `not-asked` defaults. The real recorder saved nine answers, advancing revision 202→229. A fresh read-only ActLog and the durable record stream reloaded the calculation at matching revision 229. Coordinator published line8a $20,000, the per-statement reason `qualified`, and Schedule A total; unresolved was inapplicable. Saved explanation associated the exact statement keys and stated the Box 2 whole-year acquisition-debt premise. No answer asked whether another report was for this same borrowing. | Synthetic normalized report/evidence IDs and synthetic answers are not source documents, a human affirmation, or independent institutional verification. The fixture has no recorded loan relationship. |
| Two reports: A Box 1 $20,000 / Box 2 $200,000; B Box 1 $5,000 / Box 2 $180,000 | Real review refused: “the bounded review requires exactly one current Form 1098 box 1 statement.” Two separate exact-key real recorder saves (one for each statement) each refused “answer requires one exact current Form 1098 box 1 source”; revision stayed 230→230. Coordinator was run separately with normalized synthetic v2 answer facts for both reports (clearly fixture-supplied, not recorder answers, not a same-loan affirmation). Both per-report reason derivations blocked with `DEPENDENCY_ABSENT` on the unkeyed Box 2 symbol because the two report-local observations had different values and the scalar input had no single bindable value; line8a also blocked `DEPENDENCY_ABSENT` on Box 2, unresolved had `DEPENDENCY_INVALID`, and Schedule A total lacked line8a. The report did not reach the line8a rule's explicit multiple-Form-1098 stop. Reopening the saved presentation through the singleton review helper separately refused with the same exactly-one-source restriction; raw presentation and records remain retained for inspection. | The two report identities deliberately differ and their Box 2 observations have different values at their respective reporting dates. This does not imply two debts, establish that they share one loan, or select whether either balance is right. The actual earliest blocker is unkeyed scalar ambiguity, not proof that the explicit cardinality branch is defective. |
| Two reports, same Box 2 control: A Box 1 $20,000 / Box 2 $200,000; B Box 1 $5,000 / Box 2 $200,000 | Under the same synthetic answer and latest-route setup, two subject-labelled reason findings published, unresolved was inapplicable, and line8a reached `MULTIPLE_F1098_OUT_OF_SCOPE`; Schedule A total lacked line8a. Review and saved-presentation reader still refused at their one-report boundary. Retained B reason pins show B Box 1 but A Box 2, Box 9 and nine ordinary-answer findings—even though the seed contains distinct B-keyed answer assertions with matching values. Filing status is the return-wide input. Thus this control establishes the count guard is reachable when the unkeyed scalar values agree; it does not establish independent B input transport or a B-supported reason. | Agreement between two report-local observations does not establish one continuing loan, make their evidence interchangeable, or establish which balance/debt proposition the law requires. The output's B subject label alone does not prove the B report's circumstances were consumed. |
| One report, Box 1 $20,000 / Box 2 $800,000 | Real recorder again saved nine ordinary answers, revision 202→229. The coordinator's actual v49 line8a disposition was `blocked / VALUE_INVALID`; its pins include the supplied Box 2 $800,000 finding, so the current comparison was reached. The per-statement reason published. Schedule A total was blocked by absent line8a. Fresh saved-presentation recovery matched run revision 229 to ActLog revision 229 and returned the unresolved reason that the bounded route's principal exceeded its limit; it did not invent a prorated amount. | This does not implement Publication 936 Part II's average-balance, eligible-debt, or proration calculations, and says nothing about multi-report balances. |

Case reports, question snapshots, exact disposition pins, actual acts and paired
records are in each case subdirectory under the ignored diagnostic path named
above. The coordinator report has only actual dispositions; summary extraction
filters actual `dispositions[].artifact_id` rows and extracts their `pins`.

Foreman then authorized one same-question control, without repeating the
completed cases: keep the two report identities and Box 1 amounts but make both
Box 2 observations $200,000. The selector
`--case two-reports-agreeing-box2` ran only that case; its output is retained in
`temp/mortgage-statement-borrowing/20261022T005020Z/`. The command completed in
15.4 seconds wall time (12.775 seconds for the case) with exit 0:

```sh
PYTHONPATH=. "$MORTGAGE_PYTHON" -c 'import subprocess,sys; sys.exit(subprocess.run([sys.executable,"docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing-evidence/p0-current-path-probe.py","--case","two-reports-agreeing-box2"],timeout=300).returncode)'
```

Here v49 adoption was at index 229 because the two synthetic fixture-answer
sets were appended before package adoption; seed revision was 230. The line8a
rule then reached its actual `MULTIPLE_F1098_OUT_OF_SCOPE` disposition. Both
subject-labelled residence-interest reason findings published; unresolved
was inapplicable; Schedule A total blocked because line8a was absent. This
confirms the earlier differing-Box-2 run's `DEPENDENCY_ABSENT` was a
marshalling blocker before the explicit count guard. However, the retained B
reason pins identify B Box 1 but A's Box 2, Box 9 and all nine ordinary
answers. The seed contains separate B-keyed synthetic answer findings, but
their equal values do not establish their authority as inputs to B's result.
Filing status is legitimately return-wide. Equal Box 2 values still do not
mean one loan, identify the right balance, or establish any person affirmation.
The review and saved presentation still refused under the same one-report
review limit.

## Existing-first comparison and integration cost

The current student-loan route is a precedent for explicit relationship
recording and report/subject aggregation, not an answer to mortgage semantics. In
`packages/tax/sli_relationship_recording.py`, an ordinary answer can affirm
`FINANCING` between an opaque borrowing reference and a schooling fact, and
`STATEMENT_INCLUSION` between that borrowing reference and an exact Form
1098-E statement finding; the recorder refuses to infer borrowing identity
from lender, amount, label or order. Both links have unresolved/denied/
withdrawn lifecycle outcomes. This is distinct from subject results: current
per-statement calculations and support rules keep a result attached to the
statement while recording links to named borrowing subjects.

The v49 package adopts `rule.sli-worksheet-line1-subtotal.json` v1 and
`rule.sli-worksheet.v5.json`. The former publishes the family-authorized raw
Box 1 sum (`tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`);
it does not impose the worksheet cap. The latter uses
`selection.mode=exclusive_presence`: the combined path is active for a
nonempty Form 1098-E source family, while `default.neither` yields zero only
after that source family is closed empty. The combined path uses
`reads_subject_results` for per-statement standing and answer results, then
uses the ordinary subtotal as aggregate worksheet input. This is an adopted
pattern combining subject-level adjudication with an authorized family
subtotal and explicit closed-empty behavior. It does not prove mortgage
reports ought to share the student-loan relationship or tax calculation.
Student debt has distinct eligibility, allocation and worksheet semantics;
copying its shape would still require decisions about what a continuing
mortgage borrowing means and which loan-wide proposition tax needs.

The sale route provides a second, different precedent: current Form 1099-K
source families can retain several report members. Generic
`packages/derivation/subject_dispatch.py` evaluates a declared subject rule
against keyed subject sources and joins declared sources by shared keys. But
source discovery is not universal: `packages/derivation/live.py` has bounded
Form 1099-K Box 1a discovery that validates subject version, permitted
per-statement inputs, package input bindings and exact
`payer`/`statement`/`tax-year` keys before exposing inputs as emission-only
`SourceFact`s. That is separate from generic dispatch. Thus sale support does
not show mortgage Box 2 is already transported as a keyed subject input; this
probe exposed Box 1 as the family member, while different Box 2 report-local
values left the legacy scalar unbound. Nor does that isolate the only missing
transport: in the equal-value control, the B subject-labelled reason used A's
Box 2, Box 9 and nine ordinary-answer findings. A keyed Box 2 path alone would
not establish the provenance of those other inputs. The v49 setup also needs
unrelated closed-empty latest family/closure/vocabulary versions. Neither sale
transport nor mortgage family v1's Box 1 sum authorizes combining mortgages or
making a loan-level claim.

For mortgage, report keys localize Box 1/Box 2/Box 3 and ordinary answers in
source facts, but current consumers do not necessarily consume each fact by
the matching report key. Unequal Box 2 values left its run-wide scalar
unbound; with equal Box 2 values, the B-labelled reason used A's Box 2, Box 9
and ordinary-answer facts despite B-keyed findings being present. The labels
and values therefore do not show exact source authority. Filing status is a
legitimate return-wide input and should remain distinguished from report-local
or loan-wide facts.

Further integration must decide, in product language, what the person can
affirm about a continuing obligation, what stays report-local versus becomes
loan-wide, and what balance/debt proposition the selected tax branch needs.
For every input the selected rule needs, the design must establish whether it
is report-local, loan-wide or return-wide; source authority and correction
dependency must match that scope. Matching values or repairing Box 2 alone
would not satisfy that obligation for other inputs. “Support” must distinguish
ordinary person affirmation from an intentional application assumption;
neither should be described as independent institutional verification. Do not
select a loan id, relationship shape, default policy, tax calculation, or new
schema in P0.

### Short integration-cost map

| Area | Current evidence | Cost if product scope expands | Proven vs open |
| --- | --- | --- | --- |
| Content/rule | F1098 v1 family already sums Box 1; line8a stops at count > 1 and reads Box 2 as a scalar. Subject-labelled reason rules require report-keyed facts but their outputs need not consume values from the matching report. | Specify which reports contribute and which debt/balance proposition applies; for every used input, bind it to report, loan or return scope and preserve that authority through the result. | Current route behavior and the control's cross-report pins are proven; new content shape is open. |
| Ordinary recording | Real review and durable answer save each require exactly one current report overall; their fact keys are exact per statement. But matching synthetic answers did not make B's rule result use B's answers. | Keep answer authority and correction dependency exact for each report-local input, or deliberately record a loan-wide affirmation if product/tax meaning calls for it. | Singleton boundary and current A-to-B pin reuse are proven; question and claim binding are open. |
| Source transport/marshalling | Report facts carry keys; the current Box 2 and Box 9 symbols and nine ordinary-answer inputs can be taken run-wide. Unequal scalar observations remain unbound; equal values can bind one report's finding for multiple subject results. | Choose report-local, loan-wide and return-wide inputs; ensure each needed local value is transported with its exact source authority and correction dependency, without treating equality as identity. | Safe scalar refusal and agreeing-value cross-report pinning are proven. Exact source-binding path depends on tax/product contract. |
| Saved reader | Reader calls singleton review and carries one statement explanation. | If multi-report support is chosen, present per-report basis and any cross-report result while retaining exact revision association. | Current reader ceiling is proven; saved-model contract is open. |
| Engine | Generic subject dispatch scopes emitted `SourceFact`s by shared keys, but requirements without matching scoped source rows can fall back to run-wide symbols. Form 1099-K source discovery is a bounded domain-specific addition in `live.py`. | If the selected rule needs report-local values, supply exact keyed sources (and maintain the correction dependency) or another explicitly justified mechanism. | This is an evidenced source-transport design obligation, not proof that a general/core engine rewrite is inevitable. Whether existing dispatch plus targeted source admission suffices remains open. |

### Lifecycle sources and bounded limits

Mortgage source answers have real correction and withdrawal operations in
`packages/tax/f1098_statement_recording.py` and review wrappers in
`packages/tax/f1098_statement_review.py`; `tests/test_f1098_statement_review.py`
covers correcting and withdrawing answers, including reloading after an
answer withdrawal. `tests/test_f1098_mortgage_interest_lifecycle.py` proves a
Box 1 correction at the same report identity and the one-vs-many cardinality
behavior on its historical route. These do not describe two reports as one
borrowing or provide an account-level report-transfer operation. Form 1098
instructions distinguish an acquired mortgage from collection-agent
reporting; labels alone do not identify which relationship changed.

For comparison, sale statement recording in
`packages/tax/f1099k_statement_recording.py` explicitly admits multiple source
reports, retains family closure and answer corrections/withdrawals. Current
report membership is a source-family fact, not a cross-report loan relation.
For student debt, `sli_relationship_recording.py` instead keeps both link
affirmations and their end/denial/correction history, with outcomes admitted
atomically; those lifecycle costs cannot be assumed free in any mortgage
design. The mortgage answer correction and withdrawal APIs preserve a
statement-keyed assertion, but the agreeing control proves the current reason
consumer can pin another statement's matching assertion. Any expanded path
must define which exact source or loan-level claim an output depends on and
how correction, withdrawal, or a replacement report invalidates or retains
that result. Existing same-report correction tests do not prove cross-report
dependency safety. `marshal.py`'s unkeyed fallback deliberately leaves unequal
multi-match values unbound instead of silently choosing last-in-order; when
values agree, however, its scalar binding can still pick A for a B subject.

## Current stop and next gate

No pytest or production edit was performed. The chartered P0 investigation is
complete and awaits independent review and Foreman disposition. It establishes
the present latest-route single-report behavior, real review/recorder refusals
for multiple current reports, differing-Box-2 marshalling behavior, the
equal-Box-2 cardinality stop, and the reachable over-limit stop with a saved
unresolved explanation. It cannot determine what the person can truthfully
affirm, which report changes represent servicing versus holder/loan changes,
which debt or balance proposition applies, or the appropriate tax branch.
Those are open product/tax choices, not an incomplete investigation.
Foreman/product decisions remain required before selecting any schema,
relationship, default, or calculation. The 2025 full-deduction branch must not
be conflated with Part II limited-debt average-balance calculations.
