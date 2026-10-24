# P1 independent connected-design review

**REPAIR REQUIRED — bounded paper repairs and one source-scope choice before
the proposed intermediate experiment.** This is experiment-readiness review,
not production acceptance or Track 0 closure.

Reviewed source ref `HEAD`, verified as
`65c5af37e780ac930f274a92a0367e34d748cd4e`, against the orientation block and
committed charter. After a successful fetch the assigned
`milestone/mortgage-statement-borrowing-same-loan` branch is 0 behind / 13 ahead
of derived ratified `origin/main`; its tip is not contained in that line.
The merged-PR query was unavailable because GitHub API access failed; the
reachability evidence does not indicate a spent branch. Only this report is
assigned for writing; Foreman owns disposition and commit.

## Material repairs

1. **The integration recommendation reinstates the rejected empty-family
prerequisite.** In `p1-connected-account.md:590–591`, item 5 says zero requires
no current connected account and an entered account without reports is
unresolved. This contradicts the account's debt-proposition discussion,
Changes/closure section, paper example 12, and active plan. The actual
`family.f1098.json` authorizes zero from closed-empty furnished Box 1 members;
retained ceiling, borrowing identity, or other-debt answers alone do not
defeat that authority. Remove this contradictory instruction wherever the
integration recommendation can guide the probe. Keep the distinction between
genuine closed-empty and an affirmative current link asserting membership of
an exact report that lacks a current source: the latter requires reconciliation
of report-set standing. A withdrawn link or unrelated retained loan fact is
not that affirmative orphan. For nonempty families, keep current connected
outcomes from silently restoring legacy singleton behavior.

2. **Compare source scope before selecting the shared-answer intermediate as
the experiment's premise.** The account correctly explains that report-local
and explicitly whole-loan assertions have different meanings, but its probe
selects a new borrowing-wide payment assertion and intermediate without a
concrete comparison to retaining report-local payment answers. The adopted
`rule.sli-answer-status-no-related-person-interest.json` is a closer mechanism
precedent than the sale allowlist: its real computation declares the report
as `subject`, its keyed answer as `joined`, `joined_contains_subject`, a
required answer, and a categorical status result. Missing joined answers block.

`live.py:326–349` already discovers declared subject/joined types as keyed
emission-only sources. `subject_dispatch.py:598–614, 680–728` scopes the
declared joined type even when its rows are absent, avoiding run-wide fallback.
Consequently P0's old mortgage rule does not prove a new mortgage emitter is
necessary. Compare meaningful mortgage answer/status or observation bridge
rules using this discovery against a targeted emitter. An inert declaration
added merely to expose rows would not establish the desired semantics.

The owner choice is concrete: retain report-local payment assertions, or
introduce an explicitly whole-year borrowing assertion with link-dependent
propagation. The latter can avoid repeated answers but adds a new ordinary
proposition and dependency path; the former reuses established report-local
meaning and scoped-status machinery. They may coexist later, but selecting a
shared claim must not be smuggled in as an unavoidable transport repair.
Record that choice and its cost before executing this intermediate-specific
probe. No rival prototype or production implementation is required to make
this paper comparison.

3. **Make the borrowing-level debt category and date reconciliation explicit.**
The account says the application determines a category and limit, and keeps
Box 3 report-local, but never states how two linked original-origination
observations establish one borrowing's category. The positive probe deliberately
uses equal dates, which is good isolation but cannot settle this obligation.
State that conflicting linked Box 3 dates require reconciliation; do not pick
one date, inherit A's category for B, or let a shared original-loan answer erase
contrary report evidence. State the supported limit policy: the incumbent
`parameter.mortgage-interest-debt-limit.json` supplies $750,000 / $375,000 MFS,
not a date-selected $1 million branch. Preserve that conservative boundary and
name the older-debt $1 million treatment as unmodeled, rather than promising
general applicable-limit selection. The incumbent date branch in
`rule.f1098-line8a.v2.json` separately blocks possible grandfathering at
`1987-10-13`; date comparison alone does not model that treatment. This repair
defines the connected account's scope; it need not add another probe run.

## Evidence and design properties that hold

The numerical ceiling has the correct asymmetric meaning: below-limit support,
loose above-limit uncertainty, and contrary dated observations are distinct.
The same number survives a filing-status change without inventing a new
affirmation. Other secured debt, unknown coverage, mixed payment, missing
support, and known zero remain distinct in the main account. Report facts
retain exact provenance; filing status remains return-wide.

The family and collection contract are concrete. `family.f1098.json` names
exactly `tax.us.2025.schedule-a.line8a`; `source_authority.py:183–212` audits
collects in both guard and value and rejects another publication symbol. One
successor producer with selected branches is the right paper boundary; a new
raw-subtotal symbol cannot inherit this family's authority.

The proposed intermediary is a real candidate, not an impossible two-ID
`SourceFact`. `runner.py:71` has one finding ID. Package validation checks
identity-name containment (`package_validation.py:745–763`), so the proposed
membership subject's borrowing/report/year key set contains the shared
answer's borrowing/year keys. Dispatch can bind the shared answer and
automatically pins the subject (`subject_dispatch.py:467–486`). The runner
records each actual derived publication and emits a same-run source with the
subject's structured keys (`runner.py:2448–2467, 2565–2585`). These source
observations justify testing the candidate; they do not prove its proposed
package, scheduling, categorical result typing or consumer integration works.
The experiment should use an actual declared value expression reading the
answer, not merely require an unused input or manually fabricate the result.

The positive case and four independent mutations avoid second-property and
origination-date confounders. They can discriminate wrong local pins, missing
link support, a contradictory observation and a loose upper bound. The
producer-removal control is useful: validation refusal or runtime block is
acceptable; favorable publication is not. Inspect actual derived publications,
ledger dispositions, source keys and both original input pins. The proposed
six cases are sufficient for this narrow mechanism question after the repairs;
they are not comprehensive lifecycle or release evidence.

Current versus saved state is accurately separated. The review association
checks run revision (`f1098_statement_review.py:260–275`); the account does
not claim later runs automatically admit prior derived outputs as authoritative
account assertions. Explicit exit from a started connected account remains an
unimplemented named product operation, as the Changes/closure section says;
until defined, no silent deletion-to-legacy transition is authorized. This is
a stated coverage limit, not a requirement to build the exit in this probe.

## Ceiling and handoff

I read the full connected account, active direction, P0 account and independent
review/recheck, reviewer and qualitative guidance, Owner Model, concurrent
protocol, ADR index, and targeted current code/content. P0 observations remain
background at their reviewed ceiling. No new tax proposition or legal research
was needed for these findings; the tax-source account remains P0's bounded
primary-source evidence, not fresh verification by this review.

The per-review `envelope_scan.py --range main..HEAD` exited 0. No experiment,
P0 diagnostic, pytest, production edit, staging, commit, push or spawn occurred.
Readiness can be dispositioned from these bounded repairs and source-scope
choice without repeating unchanged P0 or commissioning a full prose review
for each edit. Actual experiment results still require their explicit evidence
review; neither a repaired paper nor a passing probe authorizes production.

Approximate review cost: 15 tool calls / 15 command-or-patch operations and
roughly 16 reasoning turns, including boot and read-only freshness checks.

## P2 evidence disposition — 2026-10-22

**READY for connected production-design and Track 0 consolidation.** No
material repair is required to reuse this bounded experiment's evidence.
This is not production readiness, delivered-feature acceptance or Track 0
closure. The original paper verdict above remains the historical verdict on
its original object. The owner selected A; shared-answer propagation and its
producer-removal control are outside the selected experiment.

Reviewed `HEAD` `5b93624572d488ee7f3f6cbf56af99cdfdffc041`, verified against
Git and the updated reviewer orientation/charter. After fetching, the assigned
branch is 0 behind / 20 ahead of `origin/main`. The tree was clean at entry.
The continuation object is the committed P2 generator/results and current
Design state, plus retained synthetic evidence in
`temp/mortgage-statement-borrowing/p2-bridge-20261022T080544Z/`.

### What the actual chains establish

I compared the raw case findings, generated rule/bundle/package bytes,
scaffold metadata, completed record dispositions, five coordinator reports
and presentation files, and baseline in-memory finding. The retained registry
and release byte hashes match the scaffold's recorded hashes; the candidate
package contains exactly one `tax.us.2025.rule.f1098-line8a` member, v3.

Both baseline reason publications pin all nine of their own report's answer
bridge findings. Each of those eighteen bridges pins its own raw answer and
its own Box 1 subject. A recursive read of the recorded chains finds no peer
report's raw answer or report observation in either baseline reason. The
bridge enum maps retain the actual v2 domains, including payment's
`paid-by-others-or-partial` and certificate's `received`/`not-received`.
The fixture supplies raw assertions, not bridge/status/reason results.
This establishes more than correct final arithmetic: declared scoped rules
executed with the right source dependencies. It does not establish correction
or withdrawal displacement across live workspace revisions.

The generated rules use real `subject`/`joined` declarations and meaningful
value expressions; no new mortgage discovery allowlist was added. Existing
`live.py:326–349` discovers those source types, and subject dispatch records
the actual publications with inherited structured subject keys. This supports
the existing-first content route identified in the paper review. Borrowing
identity remains restricted to the single fixture literal
`demo.f1098.borrowing.same`; scalar account bindings are not evidence of a
general opaque-borrowing join, identity selection or ordinary recorder.

### Why the split is supported by current contracts

`package_validation.py:982–1006,1101–1114` derives selection-path dependencies
from refs and collecting names, excluding declared subject-result reads.
A family amount collect in that selection would therefore add its raw member
name to path requirements. With unequal Box 1 amounts, an ordinary scalar
binding for that name cannot supply the multi-member sum. This is a concrete
constraint on the combined selection shape, not a general content-language
failure. The retained candidate instead makes readiness a non-collecting
selection and uses one ordinary collector requiring its result.

That collector publishes exactly the family-authorized
`tax.us.2025.schedule-a.line8a`; readiness does not collect the family amount
under its own symbol. This fits `audit_collect_authority` and preserves a
single amount producer. The inert selection branch is a disclosed synthetic
scaffold, not a demonstrated production legacy/connected route selector.

### Case observations and their limits

| Isolated case | Recorded observation and causal evidence |
| --- | --- |
| Positive baseline | Line8a finding `finding:derived:28c7ef40d144fae48db3894d` has value `11000.0`, both Box 1 pins and readiness pin. The completed record names that same finding and matching ledger pins. Its extra computation pin is correctly absent from the disposition ledger. |
| B contrary payment | Only B's raw payment changes. Its bridge pins B's contrary answer; B's reason consumes that bridge and short-circuits after two relevant answer bridges. All nine bridges still execute with their own raw inputs. Readiness publishes the rejecting boolean and line8a blocks `DEPENDENCY_INVALID`; no A-only partial sum appears. |
| B membership missing | Only B's membership assertion is removed. B's link-status row blocks `DEPENDENCY_ABSENT`; readiness refuses the missing B subject result (`DEPENDENCY_INVALID`), and line8a lacks readiness (`DEPENDENCY_ABSENT`). A's link does not fill B's gap. |
| Principal contradicts ceiling | Only B Box 2 becomes $270,000. Its actual principal-status chain pins B's observation and the $250,000 ceiling. Both report reason rows still publish; readiness consumes the failed principal status and line8a blocks. Because $270,000 remains below the incumbent $750,000 limit, a legacy over-limit guard does not mask this ceiling conflict. |
| Loose upper bound | Only the ceiling becomes $900,000. Both report observations remain below it and below the tax limit; the principal-status results and report reasons remain available. Readiness reaches its ceiling/filing-status parameter comparison and line8a blocks. This withholds support; it does not establish actual excess debt. |
| Origination disagreement | Only B Box 3 changes from `2019-03-04` to `2020-03-04`. Both date bridges publish with their own raw sources. Readiness blocks `DEPENDENCY_ABSENT` on the common Box 3 scalar; line8a lacks readiness. No common-date reconciliation value or conflict-specific explanation was derived. |

For each mutation, comparison of raw finding IDs/values against baseline
shows precisely the intended changed or removed finding. The durable
coordinator dispositions equal the corresponding completed-record
dispositions in all five negative cases. These observations support the
intended narrow causes, not comprehensive negative coverage or a saved
explanation for each distinct cause.

The baseline's amount was observed in the actual exception-frame RunResult,
not reconstructed from supplied inputs. The generator extracts that object
only after `live_coordinate_run` raises. Current `live.py:660–683` records the
run before building presentation and removes reserved output files on
`PresentationModelError`; the singleton check in
`presentation_projection.py:2306–2325` rejects the two report identities in
the amount pins. This corroborates the reported boundary: completed derivation
record plus in-memory finding, **no durable baseline report/model or reloaded
group reader**. The five negative presentation files do not demonstrate that
missing group reader or conflict-specific mortgage explanations.

### Obligations carried into consolidation

Keep the existing source-scope choice and conservative tax boundary explicit.
Settle the production borrowing identity/admission and membership lifecycle,
report-local bridge result contracts, current-account route selection and
exit limit, closed-empty/legacy compatibility, and source correction and
withdrawal behavior. Specify a group projector/reader with truthful saved
revision association and actionable distinctions among unsupported coverage,
missing support, contradictory dates/principal and a loose bound. The actual
Box 3 block proves refusal, not the proposed conflict-specific presentation.
The current candidate does not establish any of those production properties;
the plan appropriately retains them rather than claiming delivery.

No new tax research, experiment rerun, pytest, production change, schema
allocation, staging, commit, push or spawn was performed. The per-review
envelope scan exited 0. Only this report was edited. Approximate continuation
cost: nine inspection/check calls plus this append and final diff check;
roughly eleven tool calls and twelve reasoning turns. No new owner choice is
required to accept the experiment at this ceiling; production scope/contract
disposition remains the next explicit gate.

## P3 connected-contract and consumer disposition — 2026-10-22

**READY to finish Track 0 consolidation, with the concrete contract repairs
below before the first production charter.** The saved-model and consumer
experiments are credible at their stated prototype ceiling. Track 0 is not
closed and the provisional contract is not yet complete enough for builders
to implement without deciding a remaining transition policy.

Reviewed source ref `HEAD`
`a774fb18eca9649d514e054cc21c22205310f46b`, verified against Git and reviewer
orientation. After fetching, the assigned milestone branch is 0 behind / 25
ahead of `origin/main`. Entry tree was clean. This delta review reuses the P2
acceptance above; it does not repeat P0 or tax-source research.

### Concrete repairs and dispositions before production

1. **Specify connected one-report behavior.** The contract promises one-report
compatibility transitions but its route table defines only a singleton with
no membership activity and an affirmative two-report account. After removing
report B and ending B's link, A may still have an affirmative current link,
unchanged borrowing recognition and a valid annual ceiling. Neither table
row defines that state. The generic withdrawal language prevents unsafe
legacy fallback but does not decide whether this valid remaining member can
calculate under connected support or is deliberately unsupported. Add that
row, its result/explanation, and the corresponding denied/unknown/withdrawn
single-member cases. Decide which current carriers keep connected routing
selected when the final affirmative link ends. This is a missing product
contract, not a request to run every production transition now.

The smallest repair is an explicit connected-singleton rule or an explicit
bounded refusal for that transition, with no silent legacy fallback. The
owner-held clear-account exit is already identified honestly; disposition
must select a concrete exit policy or accept its absence as a delivery limit
before the first production charter. Introducing an entity or retaining an
unchanged ceiling alone must not become permanent route activity by accident.

2. **Bring the integration artifact and locators forward to the final evidence.**
Track 0 artifact 6 in `p3-connected-contract.md` still ends at the earlier
missing-`liable-and-paid` attachment block and says no tie-out publication was
established. Its final Evidence ceiling correctly records the later v53
publication and saved tie-out. Update artifact 6 to distinguish the earlier
v52 stop from the verified v53 disposition/model evidence; do not promote it
to a durable attachment body or row-list claim.

The results' locator table also points the connected ordering positive at
`p3-connected-consumers-20261022T131525Z`, a setup refusal with no coordinator
report. The successful evidence is `p3-connected-consumers-20261022T131649Z`.
Its initial closed-empty control under `p3-saved-model-20261022T125942Z` was
not closed and does not support the reported zero path; the corrected control
is `p3-saved-model-20261022T130217Z`. Name those successful locators explicitly
while retaining setup attempts as failures. These are bounded evidence-account
repairs; the actual successful evidence exists and needs no rerun.

### Independently verified scope

The saved v2 group contains two exact report identities, their distinct raw
Box 1 findings, actual reason findings and rule v3 pins, and nine own-report
answer leaves on the supported cases. The contrary-payment case appropriately
contains only the two answer leaves actually consumed before its reason
short-circuit. The model retains actual blocked membership and differing
Box 3 results rather than inventing favorable statuses or a conflict finding.

The overlay finds report identity through the pinned Box 1 fact's structured
keys, and finds producers through exact computation pins. Its metadata-only
copy of the reason expression adds each bridge's exact `joined` type/version
for the existing answer-label lineage walker; it does not execute that copy,
invent source findings or calculate a tax result in Python. Reason descriptions
come from the version selected by the actual reason rule. Shared support is
read from actual current source findings. Its unique-fixture-source lookup
remains a prototype limitation, not proof of dynamic common-account selection
or the proposed return-wide other-debt identity. The group run ID/revision
matches the completed record on the later successful v52/v53 cases.

The consumer-ordering diagnosis is supported by both code and actual order.
Ordinary scheduling waits for declared requirements (`runner.py:757`), and
value evaluation can terminally record a missing branch input. The initial
$11,000 run records line12e's block before line8a and Schedule A total publish.
The successor adds the existing Schedule A total to requirements, declared
pins and blocked metadata; its guard and value expression are unchanged.
The successful v52/v53 records then show line8a, nonempty Schedule A total,
and line12e publishing in that order. This is a content dependency repair;
package resolution alone would not have established it.

The changed-content controls preserve measured empty and singleton behavior:
closed-empty line8a is **inapplicable**, a separate Schedule A total publishes
zero, and line12e retains the raw legacy itemized $18,000 route. The singleton
control publishes $20,000. These are ordering controls, not proof of the
unbuilt connected/no-activity production selector or full compatibility.

The attachment successor changes only version and completeness: it removes
the one presence-only legacy answer and retains all seven exact boundary
`check: value, equals: yes` entries. Requirement, threshold, single-family
authority, collector, subtotal and tie-out are byte-equivalent as parsed
content. The selected connected amount's transitive reason chains retain
both reports' own obligation and payment answers, so the prototype does not
replace the removed presence check with an unsubstantiated favorable default.
Production adoption must preserve that support for every selected route,
including its legacy singleton route.

In the v53 positive, the completed attachment disposition publishes finding
`finding:derived:e04b89f56303f5257208b3ae`, with both Box 1 sources, seven
boundary findings and line8a among its input pins. The saved citation group
contains `Reported subtotal: 21000` and both source pins; saved line12e is
$21,000. The no-medical control retains line8a/line12e but blocks the
attachment for exactly that missing boundary and saves no attachment citation
group. Both saved associations are current at their respective revisions,
244 and 243. The retained overlay, attachment, registry and release SHA-256
values match the results. This is genuine saved-model/disposition evidence,
not a retained attachment finding body or inspectable row-list artifact.

### Remaining closure boundary

Finish the six Track 0 artifacts around the repaired transition contract and
required owner dispositions. Keep independent raw claims separate from their
dependent derivations: adding a report does not invalidate an unchanged
borrowing/year ceiling; withdrawing recognition does not rewrite independent
raw membership assertions. Specify dynamic mortgage reference admission,
same-account selection, source/link correction and withdrawal carriers,
late-member reclosure and the production route/exit boundary concretely.
The visible saved group reader, strict production projection/validation,
actionable unresolved/conflict categories, production adoption and integration
evidence remain chartered implementation work after closure. None is claimed
proved by HTML serialization, fixture literals or a passing package resolve.

No additional broad experiment is indicated by this review. Only this report
was changed; no production edits, schema allocation, passing-case reruns,
suite, browser, staging, commit or spawn occurred. Envelope scan exited 0.
Approximate delta cost: ten inspection/check calls, this append and final
diff check, roughly twelve tool calls and thirteen reasoning turns.

## Interim foundation/proceeds checkpoint — 2026-10-23

**One bounded mechanism repair before reusing the derived-marker counting
pattern; the five retained case observations stand.** This is not a final
Track 0 or production disposition. Explicit exit and the other restored-work
checks remain pending as declared, not newly discovered defects.

Reviewed pinned `HEAD` `05a8344221c7598c7dbad8ed7e700d5d78f204b1` and its
product-evidence change `806b751d`. Orientation matched Git and the entry
tree was clean. Fetch advanced `origin/main`; this branch is 6 behind / 43
ahead. Foreman explicitly directed continuing this historical-evidence review
at the pinned ref, with synchronization before the next builder. No claim
here validates an implementation against the newer ratified base.

### Material mechanism finding

All eight proceeds count rules, including
`demo.tax.2025.rule.local-proceeds-bought-count`, have `requires: []` and
`value: link_count` over a **derived** marker. Their `joined` declaration
supplies identity containment but does not wait for its producer.
`runner.py::_subject_scheduling_predecessor_names` waits on `requires` and
coverage reductions; it does not include `link_count.links` or `joined`.
Package reachability likewise reaches the marker's fact declaration, not its
producer through this operation. Making marker computations entrypoints
ensures inclusion, not runtime completion before counting.

In every retained proceeds case, all marker dispositions actually occur
before the first count (last marker index 112, first count index 113 in the
coordinator ledger). Thus no wrong zero is observed in these five runs.
However, an eligible count before an unresolved marker sees no published row
and can resolve zero; a later marker does not retry that resolved count.
The complete candidate currently relies on its rule enumeration order for
this distinction. Assertion-order invariance does not establish producer-order
invariance. This is an unsupported general mechanism guarantee, not a claim
that the retained successful numbers are false.

Smallest property-level repair: give the declared composition a real
completion/dependency barrier so counts run only after marker producers have
resolved, while preserving legitimate zero for resolved absent/inapplicable
markers. Simply requiring a possibly absent marker without preserving that
zero behavior would not suffice. Use existing content machinery if possible;
no new engine or global record code is demanded by this finding. Verify one
discriminating producer-order/delayed-marker case after repair, rather than
rerunning all passing cases. Do not base the next exit check on an assumption
that these counts already distinguish unresolved production from absence.

### Verified observations and ceiling

I inspected the retained v59 declarations, complete package surface, raw
case acts, dispositions, saved models and hashes at
`temp/mortgage-statement-borrowing/t0-dynamic-binding-20261022T194245Z/`,
plus the foundation's declared count/status and inclusion-integrity shape.
The current candidate starts from core v51 / registry v49 / release v49;
the package comparison preserves existing members except the four intended
mortgage/consumer successors. Standard deduction v3, line13b v2, line16 v6
and selected preferential base v5 remain pinned. Retained package/registry
hashes and all five report/model/record hashes match the results account.

The local proceeds marker explicitly joins the existing local type at v2
with `subject_contains_joined`; the shared source is a separate v1 type on
borrowing/year keys. The effective result is keyed to the affirmed report
link and uses eight real numeric count results with a distinct effective
category type. A's missing-local fixture leaves B's local answer present:
A's markers block on its absent local source, its local counts have no marker
rows, and its saved consumed proceeds leaf is the shared assertion only.
B's leaf set retains its own local assertion and the shared assertion.
No B-local answer is presented as A's support. This closes the observed
peer-value fallback defect for this specific candidate and case.

Agreeing answers preserve both consumed sources. Both conflicting assertion
orders block the effective result and dependent amounts. The shared-ended
case supplies an actual retraction act, retains the independent local answer,
and saves only that local proceeds leaf in each reason chain; its amounts
publish. Those are supplied-state coordinator observations, not demonstrated
ordinary-recorder lifecycle or a guarantee for uncertain/contrary fallback.
Only proceeds-use is exercised at runtime; admission of five shared types
does not establish the other four computations.

Generic `DEPENDENCY_INVALID` is adequate evidence of fail-closed disagreement
at this rung. Before production, the saved explanation must still identify
the conflicting applicable propositions and their actual sources so the
person can reconcile them; this property does not require a new global code.
Applicable displayed raw claims and actual consumed pins remain distinct.

Safe next step: close the marker/count scheduling property, then continue
the planned explicit-exit and remaining scoped-support checks against the
synchronized base. Reuse the measured foundation and five proceeds outputs
at their recorded ceiling. No full Track 0 verdict is warranted yet.

Only this review record was edited. No passing-case execution, suite,
production/schema/engine/test edit, staging, commit or spawn occurred.
Envelope scan exited 0. Approximate checkpoint cost: ten inspection/check
calls plus append/final diff check, with brief Foreman coordination; roughly
twelve tool calls and thirteen reasoning turns, excluding wait/coordination.

Scheduling basis checked on follow-up: accepted ADR-0076 Part 1 defines a
predecessor exactly as a producer named by `requires` or
`link_coverage.reductions`, and waits for its **resolution**, not publication.
It does not grant an implicit producer edge to `link_count.links`. The same
omission reaches the reference runner: `reference_runner.run_reference`
demands `_Run.demand_names`, whose non-selection branch returns `_requires`,
and shares `is_eligible`/`attempt` with the forward runner. In package
validation, the `link_count` adjacency at `package_validation.py:2971–2979`
reaches fact declarations/bundles only, whereas ordinary required symbols
reach their publishers. The candidate's explicit marker entrypoints repair
reachability by inclusion, but do not create a completion edge in either
scheduler. This is a candidate dependency-design gap under the existing
contract, not evidence that the engine violated an accepted implicit edge.

No declaration-order permutation was executed: doing it through normal live
resolution requires a newly checksum-published disposable surface plus the
matching presentation process. The exact code/declaration trace establishes
the missing guarantee without calling a hand-built context production
evidence. Whether a permuted validated live candidate actually publishes a
wrong zero or favorable amount is **not measured** by this checkpoint; the
five retained runs themselves do not exhibit that defect. The proposed
targeted follow-up should discriminate it and the repaired completion/zero
contract without replaying the full passing set. Three additional read-only
calls established this accepted-contract/reference-runner basis.

## Shared-answer completion repair recheck — 2026-10-24

**Prior completion finding closed for the repaired proceeds composition.
The explicit-exit experiment can build on it.** This is a bounded recheck,
not Track 0 or production readiness. Exit, the other four shared propositions
and remaining lifecycle cases are still open.

Reviewed repair `bdce4731` at oriented `HEAD`
`2391c43af03ffb883f59eb7f9297d3a1956a12fb`. Git matched orientation; entry tree
was clean. After fetch the mortgage branch is 0 behind / 47 ahead of
`origin/main`. Current evidence is core-v52-derived disposable v61, not the
historical v59 composition.

The retained local counter counts recorded `what-the-money-paid-for@v2`
rows per exact Box 1 report; the shared counter counts recorded
`shared-proceeds-use@v1` rows per borrowing/year recognition root. Their
count-result types inherit those natural subject keys. No derived marker is
counted, so a zero now concerns the already-marshalled current raw sources,
not a producer that has not run. Optional categories remain optional: the
effective link consumer requires the two numeric count symbols rather than
unconditionally requiring either raw answer.

That explicit dependency is honored by both scheduler paths. Forward subject
eligibility waits until the counter producers resolve; reference demand
traverses these required symbols and uses the same eligibility/attempt code.
Package required-symbol adjacency also reaches the producers. Unlike the
old marker scheme, this supplies a real completion edge while permitting a
published count of zero. Reference behavior is code-traced here; no reference
execution is claimed.

The consumer is deliberately declared first (member index 571, counters 572
and 573) in both retained surfaces. Actual coordinator dispositions record
the counters at 98–100 before effective results at 122–123. The effective
consumer's optional `collect_categorical_all_equal` reads use scoped source
maps: local rows have exact payer/statement/year keys, shared rows have exact
borrowing/year keys, and the affirmed-link subject carries all four. Exact
local v2/shared v1 category literals map into the distinct effective v1 type;
no run-wide scalar or report-label substitution establishes the value.

I inspected the three actual reports/models/records at
`t0-dynamic-binding-20261024T001519Z` and `...001616Z` under the milestone's
ignored evidence directory. All nine file hashes match the results account.
The shared-only A result pins its own link, numeric prerequisites and shared A
answer, with no A-local or B-local answer pin; its saved reason leaf is that
shared answer. B independently retains B's local source. The contrary case
pins the applicable local/shared disagreement and blocks both effective
results and dependent amounts. With A-local retracted and only unrelated B
shared support present, A blocks `DEPENDENCY_ABSENT` without pinning B's
shared answer; report B publishes from its own local answer, but no favorable
combined amount follows. These are retained supplied-state coordinator
observations, not recorder transitions or a general sharing/exit acceptance.

No new material defect in the completion repair. The prior generic-conflict
explanation limit remains at its declared ceiling. No passing case, reference
run or suite was rerun, and no production files were edited. Only this report
was changed; envelope scan exited 0. Approximate recheck cost: four inspection
calls, append and final diff check (six calls), roughly seven reasoning turns.

## Final connected-design disposition — 2026-10-24

**REPAIR REQUIRED — settle the other-debt referent/reuse contract and correct
one remaining evidence upgrade.** The measured exit/completion results hold;
these repairs do not require replaying their passing cases. No production
charter or Track 0 closure is recommended until the bounded repairs are
dispositioned and reflected in the connected contract.

Reviewed oriented `HEAD`
`288563ff636b2189ff54aec6246e6f04fff6cdac`, including the consolidated contract,
six artifacts and new v70/v71 evidence. Git matched orientation and was clean;
after fetch the branch is 0 behind / 55 ahead of `origin/main`. Core v52 is
the adopted base for this review. Earlier findings remain historical at their
recorded versions; previous measured reviews above are reused.

### Material remaining repairs

1. **“Other” debt needs a stable excluded-borrowing referent and a reuse rule.**
The recording table and admission declaration make this a return/year fact
about “other mortgage or home-equity debt,” while the clear operation retains
it as independent authority. None names the borrowing excluded from “other”
or states what authorizes reusing the retained answer with a replacement
borrowing. The same omission is carried into the authority/lifecycle table
and proposed recorder unit. This is consequential because connected readiness
consumes `no` as coverage support.

For example, “no other debt” when discussing A means no relevant debt besides
A; preserving that answer on clear does not make it “no debt” or automatically
mean no relevant debt besides a newly selected B. Return-wide storage alone
cannot establish that substitution. The prototype still uses a borrowing-keyed
other-debt assertion and does not settle the proposed return/year semantics.
The saved empty `sharedSupport` after clear is likewise not proof of safe
reuse when a different borrowing later becomes current.

Smallest repair: state the exact ordinary proposition and how its excluded
borrowing/account context is retained and checked. Preserve its original
answer/history on exit, but require a matching referent or explicit renewed
support before it can authorize a different connected borrowing. Alternatively
choose a stable, unambiguous return-wide proposition and explain how it
establishes this bounded coverage. No debt inventory system is required by
this finding. Add one replacement-borrowing acceptance case; genuine
closed-empty and legacy singleton must not gain an irrelevant debt-answer
prerequisite. This is a missing design decision, not an unperformed production
test being treated as a design failure.

2. **The contract's final Evidence ceiling still upgrades historical integrity
observations.** It says core-v52 T0 content additionally measured
“empty/orphan integrity.” The six-artifact integration rows correctly locate
the retained true-empty/orphan/withdrawn integrity cases on core-v51-derived
v58; the new core-v52 v70/v71 cases are explicit exit, changed connected
compatibility, declaration order and proceeds uncertainty. Correct that final
summary to preserve the exact bases. No new empty/orphan run is demanded to
repair this account; future current-base production acceptance remains open.

### Findings closed and evidence that holds

The new declarations address the reason completion edge concretely: the
effective category requires both natural raw-source counters; a separate
exact-link numeric witness requires that effective result and publishes 1;
Box1 coverage uses `link_coverage` with that witness as `reductions`, hence
the existing predecessor-resolution edge. The reason requires coverage and
the local counter. This avoids requiring publication of an absent optional
raw answer and avoids feeding a category into numeric coverage. The retained
v71 consumer-first case records effective result → witness → coverage/reason
→ readiness → line8a → line12e, despite the reason's earlier declaration.
The amount producer is an ordinary `rule-artifact.v6` collector, separate
from the v14 readiness selection. Only that collector publishes the exact
family-authorized line8a symbol.

The v70 exit cases consume actual current reason results: qualified cleared
singleton publishes $8,000; the same route with `not-paid` publishes zero;
two cleared reports block instead of summing. The no-account readiness
default explicitly reads current Box1 reasons; current root/outcome activity
cannot use that default merely because connected readiness is absent. The
changed connected-singleton compatibility case retains its link, actual
principal result and $8,000 amount. These are supplied retraction/after-state
coordinator observations, not the proposed recorder's atomic interaction.

The v71 uncertain shared source remains current beside favorable local
support and is pinned by both blocked effective results. Missing numeric
witnesses then block coverage, reason, readiness and dependent amounts. It
does not publish favorable support or tax zero. The generic block and absent
shared-support display are honestly identified as prototype limits; production
acceptance requires an actionable uncertainty explanation, not a new global
record code. `AUTHORIZATION_ABSENT` limits these runs to calculation/pin/model
evidence. The inaccurate retained convenience flag is explicitly corrected
by the raw-source/pin account without rewriting the historical run.

The other four shared propositions are declaration/acceptance requirements,
not falsely claimed runtime evidence. Their stated mappings match the adopted
v2 vocabulary: particularly `no-one-else-owes-it=yes` supports no additional
obligor, `no` identifies another obligor; original-loan `no` is refinance;
certificate `received` reaches the unmodeled-certificate branch rather than
qualifying interest. Existing local meanings are not rewritten as shared
assertions. Production must implement/test each explicit mapping and preserve
unknown versus contrary versus determined-zero distinctions.

The late-member artifact names real `append_batch` / member-transition /
`horizons.apply_transition` / currency/closure boundaries and distinguishes
one-to-two from an excluded third report. Its fresh-horizon requirement and
unchanged borrowing/year raw claims are coherent paper obligations, accurately
separated from future recorder/lifecycle acceptance. Visible group rendering,
durable recorder operations and inspectable attachment rows remain production
deliverables after the selected design is closed; they do not invalidate the
bounded declaration experiments already reviewed.

Only this review record was changed. No production/code/schema edits, Git
mutation, suite, browser, new experiment or subagent was used. Envelope scan
exited 0. Approximate final-delta cost: six inspection/check calls plus append
and final diff check, roughly eight calls and nine reasoning turns.
