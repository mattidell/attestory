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
