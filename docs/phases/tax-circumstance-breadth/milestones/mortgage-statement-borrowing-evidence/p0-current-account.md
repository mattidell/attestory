# P0 increment A — one loan, two reports

Status: **incomplete; returned for Foreman feedback before any probe**. Source
ref: `HEAD` at `6332119a30f3420698bde5dcbce1fc81e93190ac`, on
`milestone/mortgage-statement-borrowing-same-loan`; verified with Git. At this
ref the branch was 0 behind / 4 ahead of `origin/main`. This account establishes
investigation questions and a proposed check, not a product design or tax
verdict.

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
| Marshalling | `packages/derivation/live.py` gathers declared family and rule source types; `packages/derivation/marshal.py:marshal_run_context` binds one unkeyed input per symbol (refusing a disagreeing multi-match) while family members feed declared collections. Same-key/agreeing Box 2 is not proof of common loan identity. |
| Rule and limit | `rule.f1098-line8a.v2.json` requires a closed family, explicitly blocks count >1 as `MULTIPLE_F1098_OUT_OF_SCOPE`, and admits count ==1. Its Box 2 ref is compared directly with the v1 filing-status parameter (`parameter.mortgage-interest-debt-limit.json`: $750,000 except $375,000 MFS); qualifying outcome collects Box 1. The rule basis expressly assumes Box 2 stands for acquisition-debt balance throughout the year. That is a disclosed premise of this bounded one-report branch; the fact it does not implement Part II's average-balance method is not by itself a defect. Whether two reports for one borrowing can support that premise or a different tax branch is open. `rule.f1098-residence-interest-reason.v2.json` is a per-Box-1 subject rule with its own Box 2, Box 3, status and ordinary-answer inputs. |
| Consumer and saved explanation | `rule.schedule-a-total.json`, the Schedule A attachment, `form.f1098.residence-interest-unresolved.form-field.json`, and `packages/derivation/presentation_projection.py` produce the line and statement-level saved model. It retains statement keys, reported interest source, answer/default basis and rule references. `review_f1098_statement_with_saved_presentation` reloads and checks revision plus exact statement provenance; the model account is currently singular. |
| Existing correction paths | `f1098_statement_recording.py` has exact-answer correction and withdrawal operations; `tests/test_f1098_statement_review.py` covers correcting/withdrawing an ordinary answer. `tests/test_f1098_mortgage_interest_lifecycle.py` covers correction of Box 1 at the same statement identity and distinct-statement cardinality blocking. Form 1098 instructions direct corrected information returns to the general information-return instructions; those distinguish a correction to a previously furnished report from a new original report. This increment did not execute lifecycle behavior or establish a two-report same-loan correction contract. |

## Proposed bounded check for increment B

Use the instructed existing, read-only Python runtime from this worktree with
`PYTHONPATH=.`; keep its machine path out of repository evidence. After Foreman
continuation, prepare a fresh synthetic `ActLog` workspace from the existing
fixture builders in
`tests/test_f1098_statement_review.py` and
`tests/test_f1098_circumstances_calculation.py`; adapt only the diagnostic
script under this evidence directory if necessary. Resolve the actual
`PublicationSurface` from the v49 package, registry v47, and release v47;
record its resolved package/release/checksums and pins before running
`live_coordinate_run`. Put generated output only under ignored
`temp/mortgage-statement-borrowing/`. Proposed invocation, where
`MORTGAGE_PYTHON` names that existing runtime:

```sh
PYTHONPATH=. "$MORTGAGE_PYTHON" docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing-evidence/p0-current-path-probe.py
```

Cap this command at 300 seconds. No pytest or production change is proposed.

Cases and observations:

1. **One report:** request the real review and capture the questions it offers.
   The synthetic fixture supplies normalized report facts and evidence
   identities; the diagnostic script selects synthetic ordinary answer
   values. No person is interviewed, and the setup does not claim to contain
   source documents unless a fixture actually does. Save the selected answers
   through the real durable recorder, read them back; run the real
   coordinator; inspect the durable report, Schedule A line 8a and the
   reloaded saved presentation/revision association. A synthetic answer does
   not show that a person affirmed a loan relationship.
2. **Two distinct report keys:** with both synthetic Box 1 reports current,
   call the real review and record its refusal; separately attempt ordinary
   durable answer save on each exact statement key and record refusal plus
   unchanged ActLog revision. Close the family and run the coordinator to
   observe its separate cardinality disposition. The fixture supplies two
   distinct report identities, not a same-loan claim; no output may be called
   a shared-loan calculation.
3. **Over-limit principal:** use the real Box 2 fact at a value greater than
   the selected filing-status limit, with all other baseline inputs
   deliberate and non-missing; run the actual coordinator and capture the
   Box 2 finding, comparison inputs, reason/disposition, Schedule A result and
   saved model. This can establish whether the current one-report comparison
   is actually reached and what it reports. It cannot establish the
   publication's average-balance or all-debt computation, or any multi-report
   treatment.

The fixture supplies report values, evidence identifiers and closure as
synthetic setup; the diagnostic script chooses ordinary answers and the real
recorder writes them as separate durable acts. Any application default must
be read from the selected package's validated explanation and not relabeled
as an answer. The probe cannot tell whether the reporting interest
recipient/collector reported correctly, independently verify an institution,
prove the supplied relationship, or support a production same-loan design. It can
show exact current route restrictions and preserve the actual blocker if the
latest package cannot reach the nominal baseline. No fact, closure, adoption,
or finished output will be rewritten to manufacture a passing result.

## Current stop and next gate

No probe, pytest or production edit has been performed in this increment. The
next work depends on Foreman feedback and continuation. P0 remains incomplete:
the current code explicitly stops at two reports, its one-report Box 2
comparison states a whole-year acquisition-debt premise rather than a general
average-balance calculation, and the current recorder has not obtained a
same-borrowing relationship. The execution can measure those existing route
boundaries; it cannot choose a loan identity, default, balance method, or
broad debt-allocation contract.
