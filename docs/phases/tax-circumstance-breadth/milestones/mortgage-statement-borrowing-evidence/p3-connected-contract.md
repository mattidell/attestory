# P3 — provisional connected account contract

## Actions I will take

1. Keep each report's nine existing answers and source evidence report-local. Ask new, explicit borrowing-scoped questions only for propositions whose meaning actually applies across that borrowing.
2. Reuse the student-loan opaque entity and relationship-recorder patterns, while requiring a mortgage-specific reference and exact report link; never infer identity from labels, values or matching local answers.
3. Offer a clear-account action distinct from correction/withdrawal; preserve report sources, local answers and history, and permit legacy singleton routing only after explicit exit and only for one current report.
4. Trace shared answers only through exact current affirmed report links and declared subject/join intermediates; specify conflict, correction, withdrawal and late-report behavior before any experiment.
5. Keep one F1098-family-authorized line8a collector, true-empty dispositions, the separate line12e integrity prerequisite, and the saved group explanation tied to actual consumed findings.
6. The paper-only proposal has now had the chartered raw-count, shared-answer, explicit-exit, declaration-order, and proceeds-uncertainty disposable coordinator discriminators on adopted core v52. Treat saved models as bounded declaration/coordinator observations, not production or recorder acceptance. Five shared fact types resolve in the candidate, but only proceeds-use has runtime evidence. The shared-answer/exit product design remains provisional and needs independent review before implementation.

### Explicit-exit discriminator actions and candidate route

For this bounded experiment, assemble two supplied after-states by one
revision-checked ActLog batch each. Retract the exact current 2025 A borrowing
root and annual ceiling (`borrowing + tax-year`), all five A shared-answer
findings with those same keys, and every current A-pair relationship outcome
(`payer + statement + tax-year + borrowing`). Preserve opaque entity
introduction/history, Box 1/2/3 source findings and F1098 family closure,
report-local ordinary answers and evidence, and A's borrowing/year-keyed
answer about other debt besides A. Its coverage proposition ranges across
either home, but its excluded referent remains A. One case keeps only report A
current; the other keeps both A and B current. This models an explicit clear operation, not ordinary
withdrawal, source deletion, “no debt,” or production recorder behavior.

The candidate keeps one reason publisher and one line8a publisher. The reason
is Box 1-subject, requires the exact current link-status result, the local
answer count, and a separate report-effective-support-coverage result; it has
no `joined` or `direction` declaration. The effective-answer rule is subject
to the exact affirmative link and joins that same link; it requires the
report-local and borrowing/year shared raw-answer counts, then reads only the
optional categories matched in that link's key scope. A numeric witness rule
on that same link requires the effective category and publishes one support
count. A Box 1-subject coverage rule joins the exact affirmation carrier and
places `link_coverage(affirmed, effective-count, empty=0)` in its `value`;
this creates the completion edge and reduces only numeric witnesses with
exact full-key matches. No link is the true empty reduction, while an
affirmation without its effective result blocks as uncovered. The reason's
`requires` names the local count and coverage publication, so it cannot rely
on declaration order or pass a category to the numeric reduction. Its value
selects the effective category for `affirmed`, the original local category
only for `none`, and blocks `withdrawn`, `denied`, `cannot-tell`, or conflict.
This uses numeric `link_coverage`, not `conditional_dependency_set` on
multi-category answers.

The single readiness selector is active on a current recognized borrowing
root or any current relationship outcome. Only when both are absent does its
default wait for the current Box 1-subject reason results and then return
false; the explicit reads provide the completion edge rather than relying on
declaration order. A selected root/outcome path cannot use that no-account
default if its readiness is missing or blocked. The sole line8a value may use
the incumbent local path only when the no-account route has exactly one
current Box 1 report, its exact status is `none`, and its actual reason result
is consumed: `qualified` yields that report amount; the adopted determined-zero
reasons (`not-paid`, `not-collateral`, or `use-unrelated-personal-expense`)
yield zero; unresolved, unsupported, contradictory or absent reasons block.
Two remaining reports block rather than sum. Current end outcomes keep the
selector active and cannot masquerade as clear. These are candidate
declarations validated and measured in the bounded coordinator cases below,
not production behavior.

## Current contract (provisional)

This is a production-design proposal, not an accepted contract or implementation. Delivery remains bounded to one or two reports for one borrowing and closed-empty compatibility; it does not generalize to three or more reports or borrowing groups. Each report remains its own source with nine report-keyed ordinary answers. The owner restored a second, additive kind of claim: a person may explicitly answer certain suitable propositions once for a borrowing/period, which is distinct from and never inferred from existing local answers. Connected derivations may use that broader answer only through the exact current report link. Neither kind of answer merges sources, establishes deductibility, or infers identity from lender, account string, property, amount, date, or equal answer values.

### Recorded claims and scope

| Claim | Candidate identity and stored meaning | Authority / correction scope | Current mechanism or proposed delta |
| --- | --- | --- | --- |
| Continuing borrowing | Opaque `borrowing_ref` entity of a mortgage-specific kind; current affirmative/contrary/unknown answer about one continuing original obligation for tax year 2025 | Borrowing + year. Correction replaces this answer; withdrawal removes its current support and does not mean “no.” | Reuse `introduce_borrowing_reference_durably` / `record_borrowing_answer_durably` / `correct_borrowing_answer_durably` / `withdraw_borrowing_answer_durably` shape in `packages/tax/sli_relationship_recording.py`, with mortgage question vocabulary and recorder. The SLI recorder validates that the referenced entity is current and the expected kind; it is a mechanism precedent, not mortgage admission. |
| Exact report membership | `borrowing_ref + payer + statement + tax-year`; one current affirmed, denied, cannot-tell, or withdrawn outcome for each report/account pair | Pair-specific. Changing/removing/replacing a report link changes that pair only; it does not alter the borrowing identity or another link. | Add mortgage relationship bundle and durable operations. SLI v2 uses separate affirmed `tax.us.2025.sli.statement-inclusion-relationship`, denied, unresolved, and withdrawn fact types under the same exact pair identity; mortgage should use equivalent current outcome carriers. No outcome is absence; an affirmative carrier alone establishes a joined member. P2's `demo.f1098.borrowing.same` is not production admission. |
| Annual balance ceiling | `borrowing_ref + tax-year`; a person-confirmed numeric upper bound on the borrowing's highest balance in the year | Borrowing + year. Adding a report about the same borrowing does not itself invalidate or require reconfirmation of this proposition; a changed borrowing/period or contrary evidence may require that. The person remains free to voluntarily correct or withdraw it at any time. | New mortgage-scoped amount fact and correction/withdrawal recorder. Do not substitute either report's Box 2 snapshot: each Box 2 remains source-report evidence, checked separately against this bound. |
| Other secured home debt besides this borrowing | `borrowing_ref + tax-year`; “Besides this borrowing, did you have any other mortgage or home-equity debt secured by either home in 2025?”; yes / no / cannot-tell | Coverage authority reaches other secured debt on either home, but the explicit excluded referent is this exact borrowing and year. Preserve/correct/withdraw it independently of report links. A current A/year answer is not authority for B or another year; a replacement/new B needs its own answer. | This matches the prototype's borrowing/year-keyed `other-home-secured-debt` fact and same-key account-readiness selection. “Yes” means unsupported additional secured debt; cannot-tell, unanswered or withdrawn is unresolved coverage, never zero. No global debt-inventory citizen is implied. |
| Nine ordinary answers | Existing nine answer facts, each keyed to the exact report; same values on two reports remain two findings with separate evidence and correction histories | Exact report. Existing source corrections and answer corrections retain their current same-identity displacement behavior. | Reuse `record_f1098_statement_answers_durably`, `correct_f1098_statement_answer_durably`, `answer_f1098_statement_answer_durably` and `withdraw_f1098_statement_answer_durably` in `packages/tax/f1098_statement_recording.py`; no shared-answer reinterpretation (owner chose A). |

The student-loan model introduces an opaque entity via `entity-introduced`, then records explicit relationship facts whose identity keys include that entity. Its inclusion recorder checks both a current borrowing entity of the right kind and a current exact statement fact. Mortgage should reuse those mechanics but declare a distinct mortgage borrowing entity kind and exact F1098 link fact. A label, user-entered token, report name or P2 supplied scalar alone is not enough. Minting the opaque ID and presenting it to the person are recording-surface work; no institution verification is implied. The candidate input is two exact Box 1 family members plus one current relationship outcome for each member/account pair; do not add a separate report-set-completeness claim.

### Declared admission and common-account selection

The missing production proof in P2 is dynamic admission. The following identity declarations make the intended key available at each rule boundary (proposed content identifiers; no schema version is allocated):

| Fact | Identity keys | Value | Use |
| --- | --- | --- | --- |
| Existing `tax.us.2025.f1098.box1-mortgage-interest@v1` | `payer: tax.us.mortgage-lender`, `statement: tax.us.1098-statement`, `tax-year: 2025` | Numeric amount | Closed F1098 family member; report-local source identity. |
| Proposed `tax.us.2025.f1098.borrowing-inclusion@v1` | Existing three report keys plus `borrowing: tax.us.mortgage-borrowing-reference` | `affirmed` only | Exact current affirmative pair; keys, not label/value, identify the loan. |
| Proposed `tax.us.2025.f1098.borrowing-denied@v1` | Same four keys | `denied` only | Current explicit no for this pair only. |
| Proposed `tax.us.2025.f1098.borrowing-unresolved@v1` | Same four keys | `cannot-tell` only | Current uncertainty, not silence or no. |
| Proposed `tax.us.2025.f1098.borrowing-withdrawn@v1` | Same four keys | `withdrawn` only | Current end outcome with no successor answer; not silence or a clear-account exit. |
| Proposed `tax.us.2025.mortgage.continuing-borrowing@v1` | `borrowing: tax.us.mortgage-borrowing-reference`, `tax-year: 2025` | Affirmative `yes` only | The active recognized account root: person currently affirms one continuing original obligation. |
| Proposed `tax.us.2025.mortgage.continuing-borrowing-denied@v1`, `...-unresolved@v1`, `...-withdrawn@v1` | Same borrowing/year scope | `no`, `cannot-tell`, or `withdrawn`, respectively | Current nonaffirmative claim outcomes; never create an active borrowing root and never become affirmative absence/orphan evidence. |
| Proposed `tax.us.2025.f1098.borrowing-year-ceiling@v1` | `borrowing: tax.us.mortgage-borrowing-reference`, `tax-year: 2025` | Numeric upper bound on the borrowing's highest balance during the year | One borrowing/year assertion, independent of each Box 2 observation. |
| Proposed `tax.us.2025.mortgage.other-secured-home-debt@v1` | `borrowing: tax.us.mortgage-borrowing-reference + tax-year: 2025` | `yes`, `no`, or `cannot-tell` to the explicit question “Besides this borrowing, did you have any other mortgage or home-equity debt secured by either home in 2025?” | The answer's coverage proposition concerns either home, but the omitted/excluded debt is this exact borrowing. Same A/year may reuse a still-current answer; B or a new year cannot inherit it and requires its own confirmation. `yes` is unsupported coverage. This is the prototype's existing key shape, not a return-wide inventory. |
| Proposed `tax.us.2025.f1098.borrowing-member-result@v1` | Same four keys as inclusion | Derived support category (`supported`, `unsupported`, or `unresolved`) | One evaluated result per exact link; requires exact report, inclusion, and same-borrowing/year support. |
| Proposed `tax.us.2025.f1098.borrowing-member-support@v1` | Same four keys as inclusion | Numeric `1` iff that link's report is qualified and its Box 2/3 and shared support checks pass; numeric `0` only for a resolved nonqualifying result | Separate numeric reduction for `link_coverage`; missing/unknown/blocked member result emits no reduction and blocks. Never encode a category here. |
| Proposed `tax.us.2025.f1098.borrowing-member-link-count@v1` | `borrowing + tax-year` | Numeric number of exact affirmed inclusion rows joined to one active borrowing claim | Dedicated v13 `link_count` intermediate. It is the sole `link_count` occurrence in that rule; account readiness consumes this published number and does not repeat the operator. |

For a per-member rule, declare `subject` as the affirmed inclusion fact type. The subject row carries all four keys. The dispatcher's existing shared-key source scoping then admits report-local answers and Box 1/2/3 by `payer + statement + tax-year`, and the ceiling by `borrowing + tax-year`. A second opaque borrowing or another statement cannot supply that support because its shared key values differ. Do not read a global scalar account ID. Per-subject consumers read matched current source/derived rows through their own shared-key scope and `ref`; `reads_subject_results` is reserved for a return-level v14 selection that explicitly enumerates subject outputs.

The recognized active account root is the current affirmative `continuing-borrowing` claim, not its ceiling. This is deliberate: an intended A claim remains a subject when A's ceiling is missing, and blocks on its exact required A ceiling; a dormant unrelated B ceiling alone is not a subject and cannot create a second active account. A no-link active claim publishes a non-ready account result rather than disappearing. A v14 consumer path declares `reads_subject_results: [{"symbol":"...borrowing-account-readiness","subject":{"id":"...continuing-borrowing","version":"v1"}}]`; the runner enumerates those exact root subjects and refuses an uncovered or blocked result. In an ordinary expression, `count(name:"...borrowing-account-readiness", source_set:"tax.us.2025.f1098")` then counts the declared list (not source rows), and `compare(..., 1, cmp:"eq")` enforces the one-account bound. The selected path must also require current affirmative inclusion activity and the account result's ready category; a dormant ceiling does not enter this read. This is a concrete evaluator/schema pattern, but exact package admission/runtime remains subject to the bounded check.

For borrowing-wide readiness, declare `subject` as the affirmative continuing-borrowing claim and `joined` as the affirmed inclusion fact, with `direction: joined_contains_subject`; declare the exact ceiling in `requires` at this same borrowing/year scope. The package validator requires the subject key names to be contained in the joined identity. At runtime only inclusion rows equal on `borrowing + tax-year` join to that active claim. A's missing ceiling cannot be filled by B's ceiling because `requires` is shared-key scoped; A stays a subject and blocks. A dormant B ceiling beside a valid A account does not create a B subject or a second readiness. Count current F1098 Box 1 members and joined inclusion rows; both must be one or two and equal. The equality prevents an extra unlinked/different-loan report from slipping into the line8a family sum.

The member category and numeric reduction are distinct outputs. A per-link support rule publishes numeric `1` only when the exact member result is `supported`, else numeric `0` only for a resolved nonqualifying category. It blocks if the member result is absent/blocked, so unknown is not zero. Its `subject` is inclusion, preserving all four keys. Account readiness uses `link_coverage(links: inclusion, reductions: borrowing-member-support)`, whose numeric result must equal the number of current links. Because validation permits only one `link_count` node per rule value, a separate borrowing-subject count rule publishes `borrowing-member-link-count`; readiness consumes that declared keyed subject result with `ref` and compares it to `count(name=Box1, source_set=F1098)`. Both must be equal and in `[1,2]`. `link_coverage` rejects nonnumeric values, missing/multiple reductions, duplicate links and orphan reductions; its key-map match is exact equality. One supports connected-singleton and two the selected pair; more members block. The one family-authorized collector remains the sole line8a publisher.

Concrete rule-value shapes below use only existing v13/v14 operators, not proposed grammar. The per-link numeric result can be expressed as:

```json
{"op":"choose","when":{"op":"collect_categorical_all_equal","name":"tax.us.2025.f1098.borrowing-member-result","value":{"op":"category_literal","fact_type":{"id":"tax.us.2025.f1098.borrowing-member-result","version":"v1"},"value":"supported"}},"then":1,"else":{"op":"choose","when":{"op":"collect_categorical_all_equal","name":"tax.us.2025.f1098.borrowing-member-result","value":{"op":"category_literal","fact_type":{"id":"tax.us.2025.f1098.borrowing-member-result","version":"v1"},"value":"unsupported"}},"then":0,"else":{"op":"block","code":"DEPENDENCY_ABSENT"}}}
```

The borrowing readiness value has this shape (IDs abbreviated only for readability):

```json
{"op":"all","args":[
 {"op":"compare","cmp":"eq","left":{"op":"link_coverage","links":"...borrowing-inclusion","reductions":"...borrowing-member-support","empty":{"parameter":{"id":"...zero-on-empty","version":"v1"}}},"right":{"op":"ref","name":"...borrowing-member-link-count"}},
 {"op":"compare","cmp":"eq","left":{"op":"ref","name":"...borrowing-member-link-count"},"right":{"op":"count","name":"tax.us.2025.f1098.box1-mortgage-interest","source_set":"tax.us.2025.f1098"}},
 {"op":"compare","cmp":"gte","left":{"op":"ref","name":"...borrowing-member-link-count"},"right":1},
 {"op":"compare","cmp":"lte","left":{"op":"ref","name":"...borrowing-member-link-count"},"right":2}
]}
```

The count intermediate is a v13 subject rule with `subject: continuing-borrowing@v1`, `joined: borrowing-inclusion@v1`, `direction: joined_contains_subject`, and value `{"op":"link_count","links":"...borrowing-inclusion"}`. This is exactly one count node in its `value`; it counts links matched to the current borrowing/year subject. The readiness rule has the same subject/join relationship and `requires` the exact upper-bound ceiling, but contains no `link_count`. The actual `link_coverage` node requires an explicit `empty.parameter` member (unreachable after the lower bound, but required structurally); use the SLI no-inclusion parameter only if package validation and semantics accept it. Operators are evaluator/schema operators, but this exact composition is still subject to the authorized candidate package and coordinator check. `_coverage_decimal` validates the reduction's numeric value; categories are not passed to it.

Representative declaration/value fragments (proposed IDs remain unallocated):

```json
{
  "schema": "rule-artifact.v13",
  "subject": {"id": "tax.us.2025.mortgage.continuing-borrowing", "version": "v1"},
  "joined": {"id": "tax.us.2025.f1098.borrowing-inclusion", "version": "v1"},
  "direction": "joined_contains_subject",
  "requires": ["tax.us.2025.f1098.borrowing-year-ceiling"],
  "value": {
    "op": "all",
    "args": [
      {"op": "compare", "cmp": "eq",
       "left": {"op": "link_coverage", "links": "tax.us.2025.f1098.borrowing-inclusion",
         "reductions": "tax.us.2025.f1098.borrowing-member-support",
         "empty": {"parameter": {"id": "tax.us.2025.parameter.sli-statement-support-no-inclusion", "version": "v1"}}},
       "right": {"op": "ref", "name": "tax.us.2025.f1098.borrowing-member-link-count"}},
      {"op": "compare", "cmp": "eq",
       "left": {"op": "ref", "name": "tax.us.2025.f1098.borrowing-member-link-count"},
       "right": {"op": "count", "name": "tax.us.2025.f1098.box1-mortgage-interest", "source_set": "tax.us.2025.f1098"}},
      {"op": "compare", "cmp": "gte",
       "left": {"op": "ref", "name": "tax.us.2025.f1098.borrowing-member-link-count"}, "right": 1},
      {"op": "compare", "cmp": "lte",
       "left": {"op": "ref", "name": "tax.us.2025.f1098.borrowing-member-link-count"}, "right": 2}
    ]
  }
}
```

The bounded candidate must carry a demo mortgage-specific zero-on-empty parameter in its disposable bundle, not reuse the SLI parameter by numeric coincidence. The member numeric result uses the preceding nested `choose`: exact `supported` yields `1`; exact `unsupported` yields `0`; absent or `unresolved` result blocks. `link_coverage` then sees only numeric values, compares the full four-key maps, and the total must equal the number of links. The ordinary consumer declares the exact result fan-in with current v14 shape:

```json
{"symbol":"tax.us.2025.f1098.borrowing-link-status",
 "subject":{"id":"tax.us.2025.f1098.box1-mortgage-interest","version":"v1"}}
```

and likewise one read of `tax.us.2025.f1098.borrowing-account-readiness` with subject `tax.us.2025.mortgage.continuing-borrowing@v1`. For report status, four distinct exact-outcome fact types each have a v13 count rule with `subject: Box1@v1`, `joined: outcome@v1`, `direction: joined_contains_subject`, `requires: []`, and the sole `link_count` in its value. With no matching carrier the exact Box1 subject still publishes numeric zero; a matching carrier produces its count. Each count preserves Box1's three inherited keys. A fifth per-Box1 rule requires all four count outputs, sums their numeric refs and classifies a total of zero as `none`, a total of one as the unique carrier category, and any other total as `conflict`. This composition was package-validated and exercised by the cited coordinator runs; it is not production lifecycle evidence.

Core-v51-derived v58 results cover the retained true-empty/orphan/withdrawn integrity observations. Core-v52-derived v70 covers explicit-clear exit and connected compatibility; v71 covers declaration-order compatibility and the shared-proceeds uncertainty discriminator. These are distinct supplied-assertion runs, not one combined package/run or production lifecycle evidence. The no-activity path preserves actual line8a inapplicability for a truly empty family; the separate line12e exact affirmed-source-match integrity dependency withholds an orphan even when the closed-empty Schedule A total is zero.

The sole ordinary line8a publisher is the T0 successor `tax.us.2025.rule.f1098-line8a@v5`, a `rule-artifact.v6` collector requiring `demo.tax.2025.mortgage.same-borrowing-ready`; it is not a v14 selection. The separate `demo.tax.2025.rule.mortgage-borrowing-readiness@v2` is the v14 `exclusive_presence` selector. Its no-account branch reads each current Box1 reason and permits incumbent singleton qualified/zero/unresolved semantics only for one report; a current connected root or relationship outcome selects connected readiness, and a missing/blocked connected result cannot fall back. Connected account readiness is a per-affirmative-borrowing v13 joined-subject result requiring the same-key ceiling and numeric full-key link coverage, with equality among the link, Box1, and active-account counts. The four v13 outcome counters use `requires: []`, so each Box1 subject publishes numeric zero when its exact joined outcome list is empty; the fifth Box1 status rule requires the four numeric results and classifies zero/one/multiple outcomes. The v14 selector enumerates exact subjects through `reads_subject_results`; there is no symbol-suffix parsing, hardcoded account ID, or global scalar authority. Package validation and the core-v52-derived v70/v71 runs exercise portions of this composition; v71 specifically shows a generic blocked uncertainty route with the raw uncertain source pinned, not a user-facing explanation or production acceptance.

Report status is rooted at Box1, not inclusion, so each current family member receives `none`, one exact outcome category or `conflict`; an affirmed orphan is separately rooted at its affirmative carrier and requires its exact current Box1 source. The measured consumer keeps line12e as the ordinary P3 rule shape: its successor declares both Schedule A total and a separate inclusion-integrity result as prerequisites, while preserving the existing guard and lazy value expression. The v14 integrity selection is a separate amount-integrity gate: current affirmed-inclusion activity reads the exact source-match result for each affirmation and publishes `true` only when those matches resolve; its no-affirmation default is `true`. Thus a closed-empty family keeps line8a `inapplicable`, the separate closed-empty Schedule A total can publish zero, and line12e can take its existing no-statement path without any loan prerequisite. If an affirmed orphan exists, the exact source-match subject blocks; integrity blocks on that subject; line12e blocks on missing integrity even though line8a is inapplicable and Schedule A total may be zero. Denied/cannot-tell/withdrawn outcomes for removed reports do not activate the gate. This is the measured candidate composition, not adopted production content; the four outcome-count rules and per-Box1 status intermediates remain separate prototype evidence.

For non-connected one-report legacy behavior, the single source-active path uses the `no-current-outcome` report status to retain incumbent reason branches. More than one Box 1 source with no complete affirmed connected group blocks; no current membership activity is inferred from matching values. Missing required per-report results cannot remove a Box 1 root: `reads_subject_results` enumerates Box 1 subjects and refuses uncovered ones. If A is current and B's ceiling is the only ceiling, A remains an active account root and blocks at its missing A ceiling; a B ceiling without a B continuing-borrowing affirmative claim remains dormant.

| Rule stage | Declared selection | What is admitted | Fail-closed discriminator |
| --- | --- | --- | --- |
| Per-report member result | `subject: borrowing-inclusion@v1`; require Box 1, nine report answers, Box 2/3, `borrowing-year-ceiling@v1` | Inclusion subject keys select same report facts by payer/statement/year and ceiling by borrowing/year | For report A linked to borrowing A, if only borrowing B's ceiling is current, the A subject's `requires` has no matching ceiling and blocks; B's value cannot fill it. If report A's affirmative link is absent and only report B has one, A is not an affirmative-link subject and receives no member result. |
| Account readiness | `subject: continuing-borrowing@v1`; `joined: borrowing-inclusion@v1`; `direction: joined_contains_subject`; require exact `borrowing-year-ceiling@v1` | A dedicated v13 joined-subject rule publishes one numeric `link_count(inclusion)` per current borrowing claim; readiness reads that keyed result once, compares it with the numeric `link_coverage` sum and closed F1098 Box 1 `count`, and admits equal member counts of one or two | A's active claim joins A links only and requires A's ceiling. B links/results do not count for A. If A's second report link/result is absent, matched count differs from family count; a third Box 1 report yields count three, outside the unit. No favorable partial subtotal. |

These are paper declarations over current mechanisms, not a P2 test result. Add precisely these A/B collision cases to production acceptance before calling dynamic selection proved.

This is the material limit of the SLI precedent. `rule.sli-answer-status-*` and `rule.sli-statement-loan-support` use a statement subject and joined statement answer/inclusion, proving exact statement admission and pair-level coverage. They do not prove a mortgage multi-report group or borrowing-wide aggregation. A Box 1 subject joined to inclusion rows admits by payer/statement/year, but does not project the inclusion's extra borrowing key into that statement subject; that shape alone cannot select the correct borrowing ceiling. The ceiling-subject join above is required. P2's literal borrowing key and agreeing scalar values did not exercise this selection.

### Current-state route and calculation

The production candidate is one successor mortgage line8a producer, not two producers whose symbols collide. It retains the externally bound symbol `tax.us.2025.schedule-a.line8a` and the existing `family.f1098.json` closure claim. The route is selected from current facts and findings, not from a remembered positive answer or the existence of a stale borrowing entity:

| Current state | Expected route/result |
| --- | --- |
| F1098 family genuinely closed-empty and no current affirmative pair outcome | Preserve the observed v49/v47 path: `rule.f1098-line8a` is inapplicable (`guard_result: false`), while `rule.schedule-a-total-closed-empty` publishes the Schedule A total of zero; the Schedule A attachment is inapplicable and the existing no-mortgage-statement route publishes Form 1040 line12e. Retained entity, ceiling or other-debt claims alone do not defeat this path. Denied, cannot-tell, and withdrawn end outcomes for a now-absent report do not become affirmative orphans and do not defeat true empty. An affirmative link to a missing exact source is the sole orphan conflict. |
| One current F1098 report, no current connected-membership activity | Preserve `rule.f1098-line8a.v2.json`'s existing qualified and determined-zero reason branches and its current explanation. The nine report-local answers still determine whether the singleton is qualified, zero, or unresolved; contrary answers are not uniformly a block. |
| One current report with an affirmative link to one current borrowing and complete shared support | The affirmative four-key link selects connected handling even though the family has one report; publish connected-singleton after the one full-key member result and borrowing/year support pass, not the legacy fallback. |
| Two current F1098 reports, no current affirmative link set covering both reports | The existing singleton path is not a group contract; withhold line8a pending explicit report/account links. Do not sum independent reports or enter connected handling by matching values. |
| One current report with a current denied, cannot-tell or withdrawn relationship outcome | Keep the Box 1 report root and emit its negative/unresolved/ended status, not affirmative membership; do not count it as account coverage or route it as legacy singleton. Withhold line8a. A withdrawn outcome for a removed report is not affirmative activity and cannot by itself block true closed-empty. |
| Two current F1098 reports with affirmative membership links to the same current borrowing | Two affirmed four-key inclusion facts select connected handling. The continuing-borrowing subject joins exactly those links by borrowing + year; its required upper-bound ceiling and keyed numeric support coverage must pass. Current member/link counts of one or two are permitted and must equal. No subset sum. |
| Connected route selected; current family now has one report A after report B's source and link ended | A may compute under unchanged borrowing/year support if closure holds and A has a current affirmative link, own report result and shared support. This is connected-singleton, not legacy fallback. Missing, denied, cannot-tell or withdrawn outcome for A withholds. An affirmed link to a missing/non-current source is an orphan and blocks, not closed-empty. A's current affirmed link is the route carrier; B's withdrawn link is history, not coverage for A. |
| Connected route: one or two current report reasons qualified and shared support passes | Publish one readiness result; the single line8a producer collects each authorized current Box 1 member exactly once. |
| Current shared proceeds answer is `cannot-tell` while a linked report retains favorable local proceeds | Keep both raw claims current and distinguish uncertainty from a contrary answer or determined zero. The exact-link consumer must not issue an effective favorable result; the numeric witness/coverage chain then withholds readiness and line8a. | v71 coordinator case blocks the exact-link rules generically with `DEPENDENCY_INVALID`; reason blocks on missing coverage and line8a/line12e do not publish. The input is pinned, but the T0 model does not explain the uncertain source. Production needs a specific unresolved explanation. |
| Connected route: any member's reason is determined zero, unresolved, unsupported, or contradictory | Do not sum a favorable subset. Withhold the connected sum and report the actual disposition category. Broader mixed-result treatment is outside this delivery. |
| Current affirmed relationship points to a missing/non-current source | This is the only relationship orphan: it must be an active conflict. Line8a's closed-family guard cannot protect the consumer because it is inapplicable; closed-empty Schedule A total publishes zero and line12e may bypass line8a. The separate inclusion-integrity prerequisite reads each affirmed carrier's exact source-match result and blocks when a current affirmation has no matching Box 1 source. This dependency is conditional on current affirmative activity, not a new loan/ceiling prerequisite on every no-report return. With no affirmative link, retired denied/cannot-tell/withdrawn outcomes remain true empty. |
| No current affirmative link, no current report, and only denied/cannot-tell/withdrawn history for removed reports | These nonaffirmative end outcomes do not assert a current missing source; they are not affirmative orphan activity | Preserve actual closed-empty Schedule A total zero / attachment inapplicable / no-statement line12e. A retained entity, ceiling or borrowing/year-keyed other-debt answer alone also does not change this route. |
| One current report with no current report/account outcome | This is the incumbent legacy singleton route. A retained opaque entity, ceiling, borrowing/year-keyed other-debt answer or displaced relationship history does not count as current route activity. |
| Affirmed relationship corrected to denied, unresolved or withdrawn; including the final affirmative link | Atomically end the affirmed outcome and record its successor outcome for the same exact pair. If the source report remains current, the nonaffirmative result prevents legacy fallback and dependent amounts are withheld. If the report was also removed, the end outcome is not an affirmative orphan and cannot defeat true closed-empty. The separate clear-account action ends the whole borrowing connection, not just this pair. |

P2 found a workable prototype shape, but its account key was manually supplied. The declared subject/join plus exact-key numeric support coverage above is the production candidate; the experiment did not exercise dynamic selection. Current relationship carriers are affirmed, denied, cannot-tell/unresolved, or withdrawn. Affirmed selects connected handling; other current outcomes are read as those outcomes, never as missing-as-no. Retained borrowing identity or ceiling alone does not select the route. Closed F1098 family membership plus exact per-report outcomes and a nonempty one-or-two-member count establish coverage for this bounded case; no separate report-set assertion is proposed.

For the supported candidate boundary, each report keeps its own Box 1 and nine answers; each report's Box 2 is checked against the common numeric ceiling; raw Box 3 dates remain report-local and must agree before one borrowing-wide debt category is used. The conservative existing $750,000 / $375,000 MFS limit and exclusion for origination on or before 1987-10-13 remain; no higher pre-2017 limit or refinance treatment is introduced. The actual line8a amount is the sum of authorized current family Box 1 members once readiness succeeds. No allocation or interest-apportionment formula is proposed.

### Restored design: explicit exit and suitable shared answers

The user-facing choice is either “keep these reports connected to this
borrowing,” “answer this suitable question once for this borrowing,” or the
separate action “stop connecting these reports through this borrowing.” Existing
statement questions stay attached to their exact reports. The shared prompt is
asked as a new ordinary claim about a named opaque borrowing and its stated
period; matching old answers never auto-create it.

The nine v2 questions are those admitted by
`f1098_statement_recording._questions_for_version("v2")` and consumed by
`rule.f1098-residence-interest-reason.v2`. The currently recorded facts remain
keyed to `payer + statement + tax-year`; these scope recommendations do not
rewrite them:

| Adopted v2 proposition | Natural scope | Provisional connected treatment |
| --- | --- | --- |
| `filing-unit-owns-home` | Filing unit + home + tax year | Keep report-specific for now. No exact home/property key joins two reports; same borrowing alone does not prove one collateral home. |
| `shared-main-home` | Filing unit + home + tax year | Keep report-specific for the same missing property identity; do not infer same home from a shared loan. |
| `home-is-collateral` | This home–this loan relationship | Keep report-specific until the home side has an exact shared identity; the F1098 can describe more than one property. |
| `owes-the-loan` | Filing unit + borrowing + tax year | Suitable for a new explicit borrowing-wide answer, scoped here to borrowing + tax year 2025. |
| `paid-the-interest` | Who paid the interest reported on this statement | Retain report-local scope for this delivery: each statement's amount/payment evidence is separate. This does not rule out a future, separately asked annual-payment proposition. |
| `no-one-else-owes-it` | Other co-obligors on this borrowing for the filing unit/year | Suitable as a new explicit borrowing-wide answer, scoped here to borrowing + tax year 2025. |
| `what-the-money-paid-for` | The identified borrowing's proceeds/use | Suitable as a new borrowing + tax-year-2025 assertion for this route. Preserve categories; `other` does not authorize mixed-use allocation. Proceeds do not become different in another year. |
| `this-is-the-original-loan` | Borrowing lineage | Suitable as a new borrowing + tax-year-2025 assertion for this route, not a statement answer. Lineage does not change merely because the route period changes; refinance treatment remains excluded. |
| `mortgage-credit-certificate-received` | Filing unit + borrowing + tax year | Suitable as a new borrowing + tax-year-2025 answer; do not generalize it to another loan or year. |

For one consistent exit boundary, give all five new assertions the exact
`borrowing + tax-year=2025` identity in this bounded delivery. The annual key
scopes their use in this return route; it does not assert that proceeds or
lineage change each year. Clear-account therefore ends only this year's
borrowing claim, links, ceiling and shared-answer assertions, never other-year
claims. Record them through ordinary evidence/contribution, correction and
retraction; do not promote local findings. Keep v1/v2 meanings and the
report-local recorder unchanged. No property identity or schema is proposed.
The new facts keep each adopted v2 answer vocabulary but remain distinct fact
types: e.g. `owes-the-loan` and `no-one-else-owes-it` map `yes`/`no`/
`cannot-tell`; use-of-proceeds keeps `bought-the-home`,
`unrelated-personal-expense`, `other`, `cannot-tell`; the original-loan answer
keeps `yes`/`no`/`cannot-tell`; and the certificate answer keeps
`received`/`not-received`/`cannot-tell`. The linked-answer rule names the new
fact type in each category literal. A successor reason rule explicitly maps
that result to the existing reason branch; matching value spelling alone does
not make fact types interchangeable.

The current T0 content candidate admits all five new types, each with exact
`borrowing + tax-year=2025` identity and the listed adopted-v2 value vocabulary.
Only the proceeds mapping is measured at runtime; the other rows below are
declaration and acceptance requirements, not executed behavior.

| Adopted v2 question → new shared type | Explicit value mapping for the linked rule | Evidence status |
| --- | --- | --- |
| `owes-the-loan` → `demo.tax.2025.mortgage.shared-owes-the-loan@v1` | `yes` may satisfy the same borrowing-specific obligation proposition; `no` is a contrary/unsupported claim; `cannot-tell` remains unresolved. The link rule must use the new fact type's category literals. | Type admitted; no runtime mapping. Accept A shared yes/no/unknown, local disagreement, correction and withdrawal without borrowing another account's answer. |
| `no-one-else-owes-it` → `demo.tax.2025.mortgage.shared-no-one-else-owes-it@v1` | The adopted v2 question means “no one besides joint spouses owes this debt”: `yes` supports that proposition; `no` means an additional obligor and is unsupported for this bounded route; `cannot-tell` is unresolved, never zero. | Type admitted; no runtime mapping. Accept yes supported, no unsupported, unknown unresolved, plus local/shared disagreement. |
| `what-the-money-paid-for` → `demo.tax.2025.mortgage.shared-proceeds-use@v1` | Preserve `bought-the-home`, `unrelated-personal-expense`, `other`, and `cannot-tell`; map only equal determinate local/shared categories to the effective per-link type. `other` does not enable allocation; `cannot-tell` blocks favorable effective support. | Type admitted and consumed. Retained proceeds cases cover shared-only, agreement, disagreement in both assertion orders, shared retraction with local support, and unrelated borrowing; v71 additionally measured `cannot-tell` beside favorable local support. The uncertainty run is a generic block and did not render an explanatory answer. |
| `this-is-the-original-loan` → `demo.tax.2025.mortgage.shared-original-loan@v1` | `yes` affirms original-loan lineage; `no` does not qualify this bounded original-loan route (refinance remains excluded); `cannot-tell` is unresolved. | Type admitted; no runtime mapping. Accept affirmative original, contrary/refinance, unknown, disagreement, and changed claim with independent provenance. |
| `mortgage-credit-certificate-received` → `demo.tax.2025.mortgage.shared-credit-certificate@v1` | Preserve `received`, `not-received`, `cannot-tell`; map using the shared type's literals to the existing certificate branch, negative branch, or unresolved branch, respectively. | Type admitted; no runtime mapping. Accept each value, local disagreement, withdrawal, and exact-account isolation. |

For every row, the report-local v2 finding remains unchanged and is not copied
or rewritten. On an exact affirmed four-key report link, a successor derived
per-link fact must map the shared category by question and compare it with an
applicable local category only where the propositions have the same meaning.
An absent local answer may use the explicit shared claim only for its selected
question; a current local/shared contradiction or uncertainty cannot be
silently hidden by a favorable peer, another account, or save order. Shared
withdrawal may leave independently valid local authority usable only when no
current contrary or uncertain applicable claim remains. These coexistence
rules are product contract proposals; only the proceeds rule's selected
composition is currently measured.

The following is the measured proceeds-category composition in the disposable
core-v52-derived candidate (not a generic claim that any optional-input design
is executable):

1. The effective consumer `demo.tax.2025.rule.effective-proceeds-use` is
   declared before its two raw-source counters. Its subject is the exact
   four-key affirmed report link; the derived `effective-proceeds-use` has
   those same report-plus-borrowing keys and uses the existing proceeds
   category values. It requires the numeric local-count and shared-count
   outputs, then evaluates matched optional categories under this link's
   identity. Local raw answer remains `tax.us.2025.f1098.what-the-money-paid-for@v2`
   keyed by payer/statement/year; shared raw answer is
   `demo.tax.2025.mortgage.shared-proceeds-use@v1` keyed by borrowing/year.
   They are separate types, and only the explicit category mapping makes
   their values comparable. Absence of either raw answer is not itself an
   unconditional dependency failure.
2. `demo.tax.2025.rule.local-proceeds-answer-count` has Box1@v1 as subject,
   joins the exact local v2 answer, and publishes numeric `link_count` at the
   three report keys. `demo.tax.2025.rule.shared-proceeds-answer-count` has
   the recognized continuing-borrowing@v1 root as subject, joins the shared
   proceeds fact, and publishes numeric `link_count` at borrowing/year keys.
   Both count only recorded source fact types, not derived answer markers.
   Their published outputs are explicit prerequisites of the effective
   per-link rule; this removes the earlier unsupported assumption that
   counting a derived marker also establishes its producer dependency.
3. The current coordinator observation demonstrates exact scope: with A local
   retracted, A's local count published without an A local-answer input pin;
   A's shared-only effective result pinned the A shared finding and numeric
   counts, while B's local answer remained independently pinned to B. In the
   unrelated-B case, A's exact four-key link did not select B's borrowing/year
   answer. In the disagreement case, the effective result failed closed. These
   observations validate only proceeds-use's existing category vocabulary,
   not the other four shared propositions.
4. This experiment did not rerun a reference runner. Preserve any prior
   reference-runner agreement only as the exact earlier trace and base it on
   that trace's actual control flow; the three new coordinator cases are not
   additional reference-runner evidence. Likewise, the existing connected
   reason/support and account-readiness chain is inherited from earlier
   bounded observations, not newly proven across all propositions here.

When local and shared values are both current, compare them in the same
proposition domain. Conflicting affirmations require clarification; a
`cannot-tell` value is unresolved, not contrary. Do not choose by save order.
If a shared claim is corrected or withdrawn, its linked bridge ceases to be
current. Independently recorded, still-current local answers remain eligible
if they alone provide sufficient support and no current contradiction or
uncertainty is hidden. The discriminating case is A/B with independently valid,
agreeing local answers followed by shared-answer withdrawal: the locals remain
available. If their local values conflict, or either is uncertain, do not
produce favorable support. Property-scoped and paid-interest answers are not
compared to borrowing-wide answers because their scopes differ. Withdrawing
one report link removes only that link's bridge; all current family members
still need exact coverage.

**Explicit clear-account action.** “Stop connecting these reports through this
borrowing” names the current borrowing and previews the exact current links and
shared claims to be ended. It is not a negative answer, link withdrawal, debt-
absence answer, report deletion, or history erasure. In one revision-checked
batch, the proposed recorder retracts the current 2025 continuing-borrowing
claim, all current relationship-outcome findings for that account/year's
report pairs, its 2025 borrowing-wide answer findings and annual ceiling. It retains
the opaque entity introduction and all past findings/evidence/retractions;
retains Form 1098 source findings, Box 1/2/3, all nine local answers and their
evidence; and retains A's other-debt answer/history under its exact A/year
referent. That answer may still support A if the same account/year is later
made current again, but clear does not transfer it to B or assert “no debt.”
The clear does not touch any other account/year claim. This uses the existing `finding-retracted` and
`append_batch(expected_revision=...)`/`_stage_retractions` pattern: read the
current log, reject incomplete tails or stale revisions, select only findings
whose structured keys exactly match the confirmed account/year, then commit
all retractions or none. Ordinary relationship withdrawal instead leaves a
current `withdrawn` outcome; it does not perform this group exit or authorize a
legacy route.

Because exit does not change report membership, a still-current F1098 closure
is retained; if a source changed independently, its normal closure/reclose
obligation still applies. Retraction displaces connected derived support under
the ordinary currency rules; earlier saved models remain historical and tied
to their consumed findings. After the explicit exit, exactly one current
report may use the existing report-local singleton route. If two reports
remain current, neither the singleton route nor a connected group route may
sum them: with no active account links, the sole line8a producer blocks and
line12e has no favorable subtotal. No report answers are copied or erased.

The cheapest distinguishing payloads are: (1) local answers only, with no
inferred shared authority; (2) shared answer present where one suitable local
answer is missing; (3) one shared A answer while B has matching values but a
different borrowing; (4) disagreement in both save orders plus
cannot-tell-versus-affirmation; (5) shared-answer withdrawal followed by valid
local A/B answers, and a later exact link/reclose; and (6) clear-account with
one versus two current reports (legacy singleton only in the first). These
cases separate existing prototype evidence from new propositions. Content work adds
the five scope-correct facts, per-link bridge/conflict and route dependencies;
recorder work adds explicit shared-answer operations and one atomic clear
batch; reader work adds a shared-answer panel with period, exact linked reports,
conflict/withdrawal disposition and source pins, while preserving each report
row. None is production-built or executed yet. The six closure artifacts
remain provisional pending this design, its bounded review, and independent
connected review.

### Lifecycle and correction consequences

Raw assertions and derived support have separate lifecycles. Box amounts/dates and the nine local answers remain report-keyed; the five newly explicit suitable shared answers, continuing-borrowing claim, exact pair outcome, numeric ceiling, and other-debt answer are separately scoped raw claims with independent evidence/history. Per-report reason, shared-to-link bridge, membership/status, borrowing readiness, line8a, Schedule A total, line12e, and explanation are derived; recompute them from current raw claims. A prior saved result remains a record of the inputs it consumed.

| Event | Required current-state effect |
| --- | --- |
| Correct Box 1 amount only; report identity and membership unchanged | Use the source recorder's same-report correction lineage. Recompute that report's reason, borrowing readiness, line8a, totals, line12e and current explanation. Keep same-borrowing claim, pair links and borrowing/year ceiling current because their subject and period did not change and no evidence contradicts them. Keep other report claims current. |
| Correct a report-local ordinary answer only | Replace only that answer on that exact report; recompute that report's result and downstream readiness. Equal answers on peers do not change. |
| Correct/withdraw continuing-borrowing claim | End or replace borrowing-year support and dependent derived readiness/amount results. Preserve independent raw membership claims as recorded; without current borrowing recognition they cannot support calculation. A withdrawal is neither a contrary answer nor permission to restore singleton. |
| Correct/withdraw one report membership | Change only that pair's current outcome and dependent connected results. A current withdrawn/denied/unknown outcome remains a route carrier and does not restore legacy behavior; only the separate clear-account batch ends the whole connection. |
| Correct annual ceiling amount, without changing account scope | Replace that borrowing/year amount; re-evaluate all report Box 2 comparisons and limit readiness. The reported Box 2 observations stay untouched. |
| Change or withdraw the borrowing identity assertion | End dependent derived membership/readiness/amount results. Preserve independent raw membership findings as recorded; they remain unusable without a current recognized borrowing. An explicit relationship correction/withdrawal changes only the named pair's current outcome. |
| A family member is added after closure (including a late report) | Trace: `close(A,B) → derive(A,B) → add(C) → prior closure-dependent findings/publications cease to be current → record C source + nine answers + exact pair outcome → reclose(A,B,C) → recompute all per-report results and readiness`. The same borrowing/year ceiling remains current absent subject/period change or contrary evidence. A new report alone does not invalidate it. |
| Remove/re-record a report | End only that report's source and dependent current derived outputs; preserve independent account/ceiling claims and other report claims. Re-recording needs a current source and its own nine answers; old membership does not attach by similar labels or values. Re-record the exact link. If the affirmative link remains while source is removed, it is an affirmed orphan and blocks. |
| Withdraw or correct the final affirmative link | In one save, retract the affirmation and record its current withdrawn/denied/unresolved successor for the same four-key pair. If the source report remains current, the nonaffirmative result prevents legacy fallback and dependent amounts are withheld. If the report was also removed, that end outcome is not an affirmative orphan and cannot defeat true closed-empty. Only the separate explicit clear-account batch removes the account's current route claims; it does not say debt is absent. |
| Any account save races with another workspace save | Read and validate current log/revision, stage entity/fact/evidence/contribution/retraction acts, then append in one `append_batch(expected_revision=...)`. A stale revision or incomplete tail refuses the save; no partial transition is visible. This mirrors the SLI recorder transaction pattern, not existing mortgage behavior. |

These are required effects, not demonstrated mortgage-recorder behavior. The current mortgage answer recorder handles exact-report answer correction and withdrawal only; it does not record opaque mortgage borrowing identities, report membership, numeric ceilings, account-level lifecycle or route choice.

### Published and saved consumers

The direct graph consumers and external bindings are different. The adopted package has no Schedule A line 8a `form-field` citizen; line8a is externally bound by the Schedule A attachment, while Form 1040 line 12e is the form-field consumer downstream.

| Consumer class | Exact binding | Expected cardinality / consequence |
| --- | --- | --- |
| Derivation: subtotal | `rule.schedule-a-total.json` requires/refs line8a when the F1098 family is nonempty; `rule.schedule-a-total-closed-empty.json` publishes Schedule A total zero when the closed family is empty | Exactly one current producer for `tax.us.2025.schedule-a.total` across disjoint empty/nonempty routes; the nonempty path consumes one line8a result. |
| Derivation: excess and return line | `rule.schedule-a-excess-over-standard.json` consumes Schedule A total; `rule.form1040-line12e.json` uses line8a for the F1098 path and publishes line 12e | One value for each consumed symbol; line12e must not route around a blocked connected line8a to raw itemized deductions. The bounded candidate successor adds existing `tax.us.2025.schedule-a.total` to line12e `requires`, adds its v1 input pin with the corpus's declared `origin: assertion` convention, and adds it to `blocked.missing`; guard and value expression remain unchanged. Its candidate package passed the real resolver and the coordinator published connected line12e after the nonempty Schedule A total. Changed-content v50 controls also published line12e through closed-empty and singleton routes. This is temporary evidence, not production adoption. |
| External attachment | `attachment.schedule-a.json` has a `single_family` authority over `tax.us.2025.f1098`, one `row_sets` collector whose `subtotal_symbol` is line8a, and `tie_out.line_symbol` line8a | One family row set and one subtotal/tie-out; no helper subtotal may claim this authority. The attachment's requirement uses `tax.us.2025.schedule-a.excess-over-standard` to determine whether Schedule A is required. |
| External Form 1040 field | `form1040.line-12e.form-field.json` binds `tax.us.2025.deductions.line-12e` (not line8a); `packages/derivation/presentation_projection.py` joins one disposition row per bound form-field symbol | Exactly one line12e disposition row; line8a remains an indirect input through `rule.form1040-line12e.json`. |
| Saved internal mortgage explanation | `presentation_projection.py` `_mortgage_interest_explanation` joins `tax.us.2025.rule.f1098-residence-interest-reason` and `tax.us.2025.rule.f1098-line8a` by exact statement pins; v1 validator requires one account | The current product reader remains singleton. The original P3 adapter's global-current-fact scan is not valid evidence of account-scoped display: it displayed B's ceiling beside A when A's ceiling was absent, and rejected the two-current-ceiling case before saving a model. The T0-only adapter repair associates raw displayed claims to the actual current continuing-borrowing root's structured borrowing/year keys. These displayed applicable claims are not automatically consumed inputs; only recorded derivation pins prove consumption. Production visible group reader remains unbuilt. |
| Family authority / coordinator | `family.f1098.json`, `closure-mapping.f1098.json`, the adopted core package, and `live_coordinate_run` supply source closure, admitted line8a, resolution/dispatch, records, and presentation construction | One line8a producer/result for the selected two-report route; genuine closed-empty remains a distinct current result. |

The bounded P3 prototype does this only in a process-local presentation adapter: it retains run/revision, exact report identities, each report's raw amount and own reason lineage, shared support, and actual line8a result. The original adapter's unkeyed shared-support enumeration was disproved by the two ceiling-collision cases. A T0-local adapter repair selects displayed raw support only by exact structured keys from the run's current continuing-borrowing root; when that root's ceiling is absent, it omits the ceiling rather than substituting another current borrowing. Its retained model remains prototype evidence, not production projection acceptance. It does not change `packages/derivation/` production code. A correction's saved explanation must continue to point at the finding that run consumed; it cannot imply a later correction changed saved history.

Keep result categories distinct in saved output: (1) unsupported coverage, such as affirmative other-home debt; (2) missing or unknown/withdrawn support, such as absent membership or cannot-tell; and (3) contradictions, such as Box 2 above the ceiling or conflicting linked Box 3 dates. P2's Box 3 case only blocked because the common scalar was absent; it did not derive a conflict-specific explanation. P3 tested a temporary adapter using real coordinator outputs. Any production projection addition belongs in `packages/derivation/presentation_projection.py` and its strict validator; the coordinator remains the authority, and the saved reader should continue to use the existing validate/reload path.

### Track 0 closure artifacts on paper (not closed)

1. **Authority-lifecycle table — paper contract; recording is not proved.**

   | Fact/claim | Meaning and authority scope | Exact dependencies | What invalidates it |
   | --- | --- | --- | --- |
   | Box 1 amount | Reported interest, `payer + statement + tax-year` | Current exact source finding; F1098 family membership | Same-report correction/removal; a new family closure displaces old aggregate outputs. |
   | Box 2 / Box 3 | Report-local balance/date, same three report keys | Current exact source finding | Same-report correction/removal; disagreement among current linked Box 3 dates is a conflict, not date selection. |
   | Adopted v2's nine existing answers | Continue recording each against its exact report; see the scope table above for which connected calculations need an additional explicit claim rather than reinterpretation | Current v2 finding and that report's evidence/source | Correction/withdrawal or report identity change; never propagate the local finding. |
   | Five suitable borrowing-wide answers | New explicit claims for the propositions classified below; never inferred or copied from local answers | Current scoped shared finding, exact affirmed report links, and derived per-link support; runtime evidence currently covers proceeds-use only | Correction/withdrawal or changed borrowing/year; recompute every bridge that consumed the changed finding. |
   | Continuing-borrowing claim | One continuing obligation, `borrowing + tax-year` | Current person claim plus current opaque mortgage-borrowing entity | Correction/withdrawal, entity ending, year/subject change, or contrary evidence. |
   | Pair outcome | This exact report concerns / does not concern / is unresolved / was withdrawn for that borrowing; four report keys plus borrowing | Current outcome fact and exact source for affirmation | Pair correction/replacement/withdrawal; removed source with current affirmation is an orphan. |
   | Annual ceiling | Upper bound on the borrowing's highest balance in one tax year | Current numeric claim; each report's Box 2 checked independently | Subject/year change, correction/withdrawal, contrary evidence. New report or Box 1 amount-only correction alone does not invalidate it. |
   | Other secured home debt besides this borrowing | Other secured debt on either home, excluding this exact borrowing; keyed by borrowing/year | Current yes/no/cannot-tell answer for that referent | Correction/withdrawal or changed referent/year; yes is unsupported, unknown/withdrawn unresolved, never zero. Do not transfer A's answer to replacement B. |
   | F1098 closure | Complete 2025 horizon of report Box 1 members | Existing family, closure mapping, current closure fact | Attestation/member change/reclose. Proves source universe, not loan identity. |
   | Seven Schedule A boundary declarations | Seven separate current affirmative `yes` claims | Exact attachment completeness requirements | Any individual correction/withdrawal remains a missing boundary. |
   | Derived report result/readiness/line8a/total/line12e/explanation | Current calculation/projection over raw support | Exact current source, answer, link, ceiling and closure pins relevant to rule | Any dependency change/new closure; saved historical result remains tied to inputs it consumed. |

2. **Empty/nonempty authority matrix — paper contract, with distinct prototype routes cited below.**

   | Family and current links | Authority read | Feature result | Neighbor result |
   | --- | --- | --- | --- |
   | Closed-empty, no current affirmative pair outcome | F1098 closure proves no Box 1 members; denied/cannot-tell/withdrawn outcomes are not affirmative links | Line8a inapplicable, not numeric zero | Existing empty Schedule A total zero, attachment inapplicable, no-statement line12e |
   | Closure absent | No complete source universe | No line8a; do not infer empty | Only dependents of F1098 closure block |
   | One report, no current connected outcome | Current family member and its nine report-local answers | Existing singleton qualified, determined-zero, or unresolved branch | Preserve incumbent singleton explanation/path |
   | A current denied/cannot-tell/withdrawn outcome while its source report remains current | Exact pair outcome is negative/uncertain/ended, not affirmative coverage | Does not count as A's affirmative link or support; non-affirmative outcome does not itself create an orphan | No legacy fallback for a current report lacking required connected affirmative coverage |
   | A removed B source with withdrawn B link and one current, fully supported A | B's withdrawn outcome is not affirmative orphan or A coverage | A remains connected-singleton if its own affirmed link and account/year support pass; otherwise withhold | No legacy fallback for A |
   | One or two current reports; every report affirmed to exactly the same current borrowing; all report results qualified and shared support current | Family closure enumerates reports; borrowing/year joined subject selects exact links; numeric keyed coverage equals link_count and link_count equals Box 1 count | One authorized line8a sum | Existing Schedule A total/excess/line12e and attachment paths |
   | Two reports have different current borrowing keys, or current links span multiple borrowings | Opaque keys differ; no match by lender, amount, label, address or answer | This milestone does not combine accounts; block connected calculation and retain each raw relationship assertion | No cross-borrowing subtotal and no other borrowing's ceiling/link can fill a missing intended key |
   | Missing/denied/unknown/withdrawn link; unresolved/zero/conflicting member; missing/loose ceiling; or current member count outside one or two | Read the specific carrier and source pins; distinguish absence, negative, unknown, withdrawal, contradiction and unsupported | Withhold connected sum; never sum a favorable subset | Downstream stays blocked/inapplicable, no fallback amount |
   | Current `cannot-tell` shared proceeds answer beside favorable local answer | Both exact scoped claims remain current; uncertainty is neither a contrary answer nor zero | The v71 coordinator consumer blocks generically with `DEPENDENCY_INVALID`; the raw uncertain source is pinned but not explained in the saved model | No favorable link coverage, readiness, line8a or line12e amount. Production must retain and explain uncertainty, not call it conflict or zero. |
   | Current affirmed pair but exact source absent/non-current | Affirmation cannot match current exact family member | Exact-source-match result blocks; the separate inclusion-integrity prerequisite blocks line12e. Schedule A zero alone does not resolve the orphan. | No subset; line8a may remain inapplicable, and no loan prerequisite is added to true empty |

3. **Late-authority counterexample — paper transition only; not a recorded lifecycle test.**

   | Transition | Current state and expected effect |
   | --- | --- |
   | One report A | Record Box1 A as a source-family member and close at current horizon H-A. Record A's nine v2 answers, exact affirmed link, borrowing/year root and ceiling; derive A result/readiness and one line8a. This is a paper start state, not a mortgage recorder test. |
   | Add report B | Use the kernel's atomic `member-transition` shape to assert B Box1 and advance the F1098 family/scope horizon H-A→H-AB. It validates the current predecessor and applies member plus successor together. The old closure is keyed to H-A, so it does not attest H-AB; closure-dependent results must not be treated as current through the open interval. |
   | Record B while open | After B is current, the existing `record_f1098_statement_answers_durably` shape checks one exact Box1 source and revision before recording its nine report-local answers. A mortgage-specific exact four-key link operation must be built from the SLI relationship-recorder pattern; no matching-by-values shortcut. Existing F1098 recording has no mortgage account/link operation. |
   | Reclose reports A/B | Obtain fresh closure evidence on H-AB; do not copy the H-A closure. Kernel horizon mechanics and a current closure fact supply the shape; `close_f1099k_family_durably` is a different-family precedent, not an F1098 recorder. Recompute per-report counts/results, shared-to-link support, four-outcome status, readiness, line8a, Schedule A total/excess, line12e and attachment. Both reports still concern the same borrowing: its raw shared answers, other-debt answer and annual ceiling remain current absent subject/period change or contrary evidence. Adding report B does not change that excluded-borrowing referent; selecting a different borrowing would require that borrowing's own answer. |
   | Third report C | The current declaration bound is one or two: count three makes readiness fail and prevents an A/B subset. Any later three-report feature must replace this bound and acceptance; an assembled two-report after-state does not prove this lifecycle. |

4. **Claim-reuse proof — exact reuse versus mechanism-only reuse.**

   | Candidate | Proposition | Identity/lifecycle | Scope/explanation | Disposition |
   | --- | --- | --- | --- | --- |
   | Nine ordinary answers and report amounts | Same existing report-local claim/source | Same payer/statement/year recorder and correction history | Exact report only | Reuse unchanged; equal values stay separate. |
   | SLI opaque entity introduction | Both use person-distinguished opaque borrowing address | Mortgage has a distinct entity kind; no cross-domain ID reuse | SLI current-kind check is a mechanism precedent | Reuse operation shape only. |
   | SLI inclusion relationship | 1098-E includes student-loan interest vs mortgage 1098 concerns a continuing home borrowing | Different entity kind, report identity, outcomes and correction lifecycle | SLI proves statement link coverage, not mortgage group aggregation | New mortgage facts and recorder required. |
   | F1098 family and closure | `family.f1098@v1` already authorizes every current 2025 Box1 member at its family horizon, a multipayer sum, and the existing line8a symbol; `closure-mapping.f1098@v1` maps that Box1 fact to the closure fact on the same horizon | Reuse current source-family authority and exact closure scope; a new horizon requires fresh closure | It establishes the complete Box1 report universe, not borrowing identity, account membership, or debt coverage. Empty-family authority produces an inapplicable line8a guard plus the separate empty Schedule A total zero, not a numeric line8a zero. | Preserve the family/mapping; add mortgage-specific links/readiness only. Late-member acceptance must use the new horizon and fresh closure. |
   | Seven Schedule A boundary declarations | Seven existing answer facts, each independent of mortgage account identity | Retain exact affirmative value requirements; no presence-only shortcut | The ephemeral v53 attachment candidate removed only `liable-and-paid` presence while retaining seven value checks; its attachment result did not retain an independently inspectable row body. | Production attachment must keep all seven checks, saved result/row inspection and a missing-boundary negative. |
   | P2 literal ID / agreeing scalar | Test names one supplied account | No dynamic key selection or recorder lifecycle | Scalar agreement is not identity authority | Not production admission evidence. |

5. **Neighbor dependency diff — paper contract; production regressions remain open.**

   | Existing path | Before | After when no connected activity | Connected-only dependency / acceptance |
   | --- | --- | --- | --- |
   | One-report F1098 | Closure, report source, nine local answers and existing reason branches | Same prerequisites and meanings; no borrowing/link/ceiling/other-debt dependency | Keep qualified, determined-zero, unresolved controls; a retained A-keyed other-debt answer alone adds no prerequisite. |
| Closed-empty Schedule A / no-statement line12e | Genuine closed-empty authority and current empty path | Unchanged with retained entity, ceiling or borrowing/year-keyed other-debt answer | No connected-only prerequisite; no numeric line8a zero. |
   | Student-loan and home-sale neighbors | Existing adopted facts/rules/consumers | Unchanged; no shared IDs or collector authority | Regression scope follows any shared implementation touched. |
   | Two-report connected mortgage | Unsupported before this feature | No added requirements on paths without current connected carriers | Requires exact outcomes, two report results, same-borrowing/year support including that borrowing's own other-debt answer, family closure and readiness before sole collector. A's answer cannot cover B. |

6. **Integration-surface artifact — bindings enumerated; production acceptance open.**

   | Consumer | Binding | Cardinality | Prototype evidence and limit | Production acceptance |
   | --- | --- | --- | --- | --- |
| Schedule A total | `rule.schedule-a-total.json` and closed-empty sibling | One current total producer across disjoint paths | P3 empty/singleton controls; core-v51-derived v58 supplies the retained true-empty total-zero observation distinct from inapplicable line8a. Core-v52-derived v70 covers explicit-clear exit and connected compatibility; v71 covers declaration order and current uncertainty. See results for exact cases. | Production tests must preserve distinct closed-empty zero and nonempty/missing-support behavior, with exactly one total producer. |
| Form 1040 line12e | `form1040.line-12e.form-field.json` binds line12e; the measured ordinary successor requires Schedule A total and the separate inclusion-integrity result | One disposition per field symbol; integrity is a separate publisher | Historical P3 v52/v53 remain as recorded. Core-v51-derived v58 supplies retained true-empty/orphan/withdrawn integrity observations; core-v52-derived v70 covers explicit-clear and connected compatibility; v71 covers declaration order and uncertainty. See results for exact cases; these are distinct runs. | Production successor must retain the Schedule A ordering edge and integrity prerequisite; save/reload positive, blocked, empty, singleton and uncertainty models. |
   | Schedule A attachment | `attachment.schedule-a.json`, `single_family`, one row-set collector, line8a subtotal/tie-out | One row set, subtotal, tie-out | v53 ephemeral successor published `$21,000`, retained both Box 1 pins/tie-out; missing-no-medical blocked; no durable row-list/body | Adopt removal of only presence-only `liable-and-paid`, retain all seven value checks, inspect actual durable attachment result and negative control. |
   | Saved mortgage explanation | `presentation_projection.py::_mortgage_interest_explanation`, strict validator, reload/page reader | Existing reader one account; proposed one group with each report once and one shared account section | T0 adapter associates connected singleton/group claims by structured root keys and follows real pins. For blocked uncertainty, the saved model omits `sharedSupport`, although coordinator pins retain the current `cannot-tell` finding; generic `DEPENDENCY_INVALID` is not acceptable production explanation. HTML serialization is not visible group delivery. | Production projection/validation and visible reader; retain run/revision, source pins, nine separate answers, shared support, and an explicit unresolved/uncertain source explanation without converting it to contradiction or zero. |
   | Family admission/coordinator | `family.f1098.json`, closure mapping, package entrypoints, `live_coordinate_run` | One authorized line8a disposition/result on every path, including false guard/blocked/never eligible | Coordinator executed supplied relationships and shared proceeds cases on adopted core v52-derived content; no recording lifecycle proof | Mortgage recorder plus dynamic cases: intended ceiling vs another borrowing's ceiling; intended link missing vs other link present; deny/unknown/withdraw/orphan; no cross-account selection; add one late member, observe open horizon, reclose, and separately reject a third member. |

   Reviewed prototype pointers are [P3 saved-model results](p3-saved-model-results.md) and the ignored run directories listed there. They establish only the coordinator dispositions described above, not mortgage recording, adopted content, production display, or all distinct production paths. Paper requirements, prototype proof and production acceptance are separate evidence rungs.

### Proposed implementation boundaries and open choices

The likely production changes are: mortgage borrowing entity/relationship/ceiling/other-debt facts in the ordinary vocabulary and package; a focused `packages/tax/` recorder that mirrors the existing evidence/contribution/correction/retraction and revision-check pattern; a successor rule set for report-local statuses, account readiness, route selection and one authorized line8a producer; and an additive group mortgage explanation in the existing internal presentation model plus strict validator and saved reader compatibility. The inspected `subject`/`joined`, shared-key source selection, `link_count`/`link_coverage`, and family collector mechanisms appear sufficient to express the proposed keys; P2 did not test them dynamically, so this is not implementation proof. The demonstrated presentation limit is narrower: the current mortgage projection/validator expects one account and needs an additive group shape and visible reader. No published schema change is indicated because this internal presentation model is not a published citizen schema; no new engine capability is presently demonstrated as necessary. If implementation shows the declared joins cannot express the A/B exclusion case, stop and return that concrete gap rather than broadening the engine speculatively.

Small production units, with exact surfaces and evidence cases:

| Unit | Content / recording / presentation surface | Positive and negative acceptance cases |
| --- | --- | --- |
| Account facts and recorder | Add a mortgage borrowing source bundle beside `packages/content/tax/2025/f1098.bundle.json` and `f1098-circumstances.bundle.v2.json`; load/adopt through `packages/tax/loader.py`. Add focused durable operations under `packages/tax/` for opaque entity introduction, continuing-borrowing claim, exact report outcome, annual ceiling, other-debt answer keyed to its excluded borrowing/year referent, five explicitly borrowing/year-scoped shared answers, and atomic clear-account exit. Mirror SLI's evidence/contribution/retraction/batch revision-check pattern; leave `packages/tax/f1098_statement_recording.py`'s report-local history intact. Exit ends only the selected borrowing/year root, all its exact relationship-outcome claims, five shared answers, and ceiling in one revision-checked batch; it preserves report sources, Box1/2/3, local answers, A's current borrowing/year other-debt answer/history, opaque entity/history, and F1098 family closure. It asserts no debt absence. The retained A answer may be reused only for the same current A/year referent; replacement B or another year needs its own confirmation. | Record two exact reports to one opaque borrowing; correct amount without ending link/ceiling; correct or withdraw one link atomically; clear one account/year then confirm two remaining reports do not gain a subtotal; stale revision/incomplete tail refuses; labels or equal amounts never merge IDs. Explicitly test retaining A's answer through clear, then replacing A with B: without B's own answer, connected coverage is unresolved; A's answer is not inherited. Legacy singleton and true-empty paths gain no debt-answer prerequisite. Shared correction/withdrawal must preserve independent local authority absent current contradictory/uncertain applicable information. |
| Connected status and one line8a producer | Successor citizens in `packages/content/tax/2025/` and successor to adopted `package.core-calculations.v52.json` (registry v50; SLI release v50): report-member status/result, borrowing-year readiness, route outcome and one family-authorized line8a collector. Preserve `family.f1098.json` and its closure mapping, and all adopted non-mortgage members including IRA vocabulary v3, direct FTC v2, and current withholding/refund members. Consumer successors retain the measured line12e Schedule A-total and separate integrity prerequisites, plus the attachment's seven value checks. | Positive two reports/one borrowing; connected singleton; other-borrowing ceiling only; other-borrowing link only; two accounts; unlinked third family member; missing/denied/unknown/withdrawn/orphan; loose or contradictory ceiling; changed Box 3. Empty and incumbent singleton controls stay on their real paths. |
| Saved group explanation | Add group projection and strict validation in `packages/derivation/presentation_projection.py`, then update the saved mortgage reader/page to render it after the existing validate/reload path. Keep one report row per current family source and one shared account-support section. | Save/reload and visibly render two report amounts, separate answers/reasons/source pins and shared borrowing/ceiling; correction changes current model only; old saved run remains tied to consumed findings. Include missing support, unsupported debt, contradictory support, and a current shared `cannot-tell` answer beside favorable local support. The v71 synthetic coordinator run retained/pinned that uncertain source but produced only generic `DEPENDENCY_INVALID` and a saved model without `sharedSupport`; this is a demonstrated presentation gap, not authorization to relabel it contradiction or zero. |
| Integrated lifecycle and neighbors | Use the real coordinator/save/reload surfaces and focused regressions for changed code; do not alter unrelated loan/sale contracts. | Late report is a separate `ActMemberTransition.v3` transition (family, scope, member, successor): report A at horizon H-A, then add B and transition to H-AB. The concrete existing path is `ActLog.append_batch` → `findings.apply_member_transition` / `_apply_member_transition` → `horizons.apply_transition`; the old H-A closure cannot prove completeness at H-AB, so keep closure-dependent outputs withheld until a fresh H-AB close. `compute_currency` (including superseded-entity roots) and `marshal_closure_authority` establish the current source/closure boundary. `close_f1099k_family_durably` is a different-family recorder precedent, not an F1098 operation. Then independently refuse a third current report rather than summing an A/B subset. Also test report removal/re-record; final affirmative link ending with no legacy fallback; explicit clear; F1098 closed-empty; incumbent singleton qualified/zero/unresolved; and Schedule A missing-boundary control. Coordinator after-states supplied to the prototype are not recorder lifecycle proof. |

These are proposed implementation units, not charters or a Track 0 PASS. Do not start them until the Foreman reviews this draft and Track 0 is closed. Clear-account exit and suitable borrowing-wide answers are in scope; their recording, reader behavior and independent review remain open.

Required production evidence still ahead: durable introduction/re-use of an opaque mortgage reference; actual recorder transitions for affirmative, denied, cannot-tell, missing and withdrawn membership; independent source-amount and pair-link corrections; adding a late report with an observed open horizon and reclose; connected withdrawal without singleton fallback; incumbent one-report qualified, determined-zero and unresolved behavior through the production route; production saved-reader rendering of shared, missing, contrary, unsupported-coverage, conflicting-support and uncertain dispositions; and inspectable Schedule A attachment row output with its missing-boundary control. Disposable coordinator runs cover supplied after-states for empty, singleton, connected, missing, contrary, explicit clear and shared uncertainty; they are not durable lifecycle or production-reader proof. The charter's retained cases additionally exercise Box 2/ceiling conflict, loose ceiling and differing Box 3. Production evidence remains open.

## Evidence ceiling

P2's synthetic content experiment and independent acceptance establish a bounded derivation shape, not production recording, identity establishment or lifecycle correctness. The P3 disposable presentation adapter and content-only line12e ordering probe establish a durable synthetic two-report model and connected line12e publication. An ephemeral v53 attachment successor removed only the legacy presence-only `tax.us.2025.f1098.liable-and-paid` completeness answer, retained all seven boundary-value checks, and reached a published attachment disposition on the connected $21,000 case; the missing-no-medical control remained blocked. Saved evidence is the coordinator's disposition and model tie-out/pins; it does not retain an independently inspectable attachment body or row list. Core-v51-derived v58 contains the retained true-empty, affirmed-orphan, and withdrawn-integrity observations; core-v52-derived v70 contains explicit-clear and connected-path compatibility observations; core-v52-derived v71 contains declaration-order compatibility and the shared-proceeds `cannot-tell` discriminator. Earlier core-v52-derived candidates cover the raw/shared-answer composition and borrowing/year key selection. These are distinct disposable supplied-assertion/content observations, not a combined run, mortgage recorder, production reader, or lifecycle acceptance. The v71 saved coordinator run pins the uncertain source but blocks generically and does not render a shared-support explanation. This document remains an implementable provisional contract, not filing conclusion, Track 0 PASS or authorization to allocate a schema version. Recorder, production route, visible group reader, and production adoption remain open.
