<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "multiple-statement-circumstances",
  "status": "Closed. A person with more than one Form 1099-K records, corrects, withdraws and removes each statement's own sale account; when every current statement is a supported personal loss, their Box 1a amounts are combined at the top of 2025 Schedule 1, and each statement keeps its own reason, figures and saved explanation. ADR 0079 adds a recorded family-version handover. One Form 1098 remains the mortgage limit.",
  "retrospective": "docs/milestone-retrospectives/2026-10-19-multiple-statement-circumstances.md",
  "scope": [
    "let a person with more than one Form 1099-K record and correct each statement's own sale account, and reach the combined Schedule 1 entry when every statement is a supported personal loss",
    "keep each statement's ordinary answers, result and named reason with that statement through calculation, correction and saved explanation",
    "retain and explain the one-statement Form 1098 limit; use its P0 comparison to inform shared input-ownership design without extending mortgage treatment"
  ],
  "non_goals": [
    "no allocation of one statement among several sales, and no gain or break-even reporting on Form 8949 or Schedule D",
    "no multiple-statement mortgage support, interest allocation, second-home extension, mixed use or refinancing in this milestone",
    "no general multi-document intake, free-text circumstance matching or new general assumption framework"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/milestone-retrospectives/2026-10-17-personal-item-sale-circumstances.md",
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#Actions the team will take"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#Decisions that need evidence",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#Cases that will test the account"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-19-multiple-statement-circumstances.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md"
    ]
  }
}
-->

# More Than One Statement: Keeping Each Account With Its Form

Milestone key: multiple-statement-circumstances.
Branch: milestone/multiple-statement-circumstances-consolidation.
Phase: Tax Circumstance Breadth. Opening plan, 2026-10-17.
Base: origin/main, personal-item sale milestone merge
`4c5305abae10ff462f79cd26b074c6d203dac69d` (PR #210).

## What we are trying to accomplish

A tax form arrives as a statement: one Form 1099-K from a payment platform,
one Form 1098 from a mortgage lender. The person then answers ordinary
questions about it: what was sold and what it cost, or whose home it is and
what the loan paid for. Those answers belong to that statement.

Both circumstance routes this phase built work only when there is exactly one
statement. A second statement stops the route with a named reason ("more than
one Form 1099-K" or "more than one Form 1098"). Ordinary households commonly
have two. Someone may sell on two platforms, or receive a Form 1099-K from a
platform and another from a payment app. Someone may have a second home or a
second loan with another lender. The 2025 Schedule 1 instructions expect
several Forms 1099-K: for personal items sold at a loss, "enter the total
amount from Form(s) 1099-K, box 1(a)" in the entry space at the top of
Schedule 1.

The delivery goal is that each Form 1099-K keeps its own account. A person with
two sale statements answers each one separately. The application evaluates
each on its own answers and combines results only where the tax rules combine them.
Correcting one statement changes only that statement's result. The saved
explanation shows each statement with its answers, figures and reason, and
the combined entry where one is made.

This is the roadmap's consolidation step. P0 compared both delivered routes;
the owner selected the sale extension first and retained the mortgage route's
named one-statement limit. Mortgage support needs additional debt, home and
balance decisions, not just the shared transport improvement. The milestone
consolidates the sale route before the phase is assessed; it does not promise
two completed multi-statement routes.

## Starting position and uncertainty

**What the earlier milestones found.** When the personal-item sale route was
designed, two Form 1099-K statements with different answers could not be
evaluated. The engine matched each answer to a calculation by the kind of
answer, not by the statement it described. Given two statements whose answers
to the same question differ, it refuses to guess and leaves the answer
unbound. Both statements then stop as if unanswered. The guard is in
`packages/derivation/marshal.py`, in the binding loop that leaves a
disagreeing, unkeyed match unbound. That refusal is correct; guessing would
be worse. The route therefore stops on a second statement by design. The
mortgage route had already done the same (`MULTIPLE_F1098_OUT_OF_SCOPE`).

**What may already exist.** The engine joins collected source rows to a
subject by agreeing values on shared identity keys
(`packages/derivation/subject_dispatch.py`). The student-loan route records
explicit relationships between a borrowing, a school and a statement, and its
tests cover more than one statement. Whether either mechanism can carry a
statement's ordinary answers to that statement's calculation is the first
question. A content or declaration change might suffice where an engine change
was assumed. These are reuse candidates, not evidence of compatibility.

**What differs between the two routes.**
- **Form 1099-K.** Each statement's personal-loss result is independent, and
  the 2025 instruction adds the Box 1a amounts. The open questions are the
  return-level rule when statements disagree, and how each statement's
  explanation and stop survive.
- **Form 1098.** Two loans are not independent. The debt limit applies to the
  combined qualifying debt, so interest on loans whose combined principal
  exceeds the limit must be allocated. Even below the limit, the second
  statement's home, use and ownership answers must stay with it. The bounded
  case, if any, is a P0 finding to bring back, not an assumption.

**Inherited constraints.** Published schemas and content are immutable;
changes are successors. A change under `packages/kernel/` or
`packages/derivation/` needs the full suite in CI and an independent review.
The 22 fast-lane budget failures are inherited and are not this milestone's
work. The preferential-rate defect stays separate.

## Actions the team will take

The milestone executed through six stages:
1. **Trace the gap (P0):** Traced why multiple Form 1099-K statements were previously out of scope and compared the existing student-loan pattern (`multiple-statement-circumstances-evidence/p0-account-and-trace.md`).
2. **Review the account:** Independent review confirmed that statement answers were durable and keyed, but input dispatch lacked per-statement routing.
3. **Design the connected account:** Decoupled strata from recording through calculation to saved explanation (`multiple-statement-circumstances-evidence/connected-sale-design.md`), selecting Policy 1 combination and Candidate C aggregation (`multiple-statement-circumstances-evidence/p7-existing-pattern-candidate-c.md`).
4. **Establish the lifecycle contract (ADR 0079):** Independent review identified authority overlap when multiple family versions coexist. A formal proposal (`multiple-statement-circumstances-evidence/family-handover-contract-proposal.md`) established explicit family-version handover and containment, accepted as ADR 0079.
5. **Close Track 0:** Settled adversarial closure across all disposition, lifecycle, and integration paths (`multiple-statement-circumstances-evidence/track0-closure-evidence.md`, `multiple-statement-circumstances-evidence/test_track0_closure_probe.py`).
6. **Build, verify, and close:** Implemented handover in the kernel, delivered Track 1 content and derivation updates, verified through targeted test lanes, and closed the milestone.

## Design state

### Settled direction and evidence

- **Delivery goal:** Each Form 1099-K statement keeps its own answers, figures, reason, and saved explanation. Form 1098 retains its named one-statement limit because mortgage breadth requires cross-loan debt, home, and balance identity.
- **Combination policy (Policy 1):** The raw Box 1a total is entered once at the top of 2025 Schedule 1 only when every current statement is a supported personal loss. Any other reason, blocked statement, or unclosed family prevents the entry; nothing is netted or silently omitted. A closed-empty family derives $0.00.
- **Combined-entry representation:** Follows Candidate C (`p7-existing-pattern-candidate-c.md`), adopting the existing student-loan pattern (raw Box 1a subtotal rule and two-path selection reading per-statement reasons) without extending the rule schema or aggregation engine.
- **Authority handover and containment:** Form 1099-K family v2 takes over authority from v1 via a recorded handover act (`act-family-handover.v1`) under ADR 0079. Multiple active version chains for the same family refuse closure authority and fail closed.

## Decisions that need evidence

### Decisions made and reasons

- **Form 1098 out-of-scope retention:** Retaining the one-statement Form 1098 limit was selected because multi-mortgage calculations require debt-limit allocation and multi-property tracking, not merely shared transport.
- **Policy 1 over Policy 2:** Selected Policy 1 (enter total only when all statements are supported losses) over qualifying-subset netting because gain or break-even reporting on Form 8949 / Schedule D is outside current milestone scope.
- **Bounded input discovery over helper rules:** Chose bounded emission discovery in `packages/derivation/live.py` (Option B) with fail-closed named refusal (`TransportContractError`) over adding sixteen synthetic helper rules, keeping the calculation graph and citation chains direct.
- **Single-save statement removal:** Statement removal advances the family horizon and retracts that statement's findings in a single commit, preserving atomic horizon integrity.
- **Kernel family-version handover (ADR 0079):** Implemented explicit handover and pre-save lifecycle folding rather than allowing concurrent active version chains or mutating published schemas, ensuring deterministic completeness authority across package upgrades.

## Cases that will test the account

The synthetic account the acceptance tests execute
(`tests/test_multiple_statement_sale_acceptance.py`).

- Two Forms 1099-K, each a supported personal loss with different answers.
  The entry is the sum of both Box 1a amounts, and each statement's
  explanation keeps its own figures.
- Two Forms 1099-K where one is a supported loss and the other is a gain, an
  excluded item, a "can't tell" or an unanswered question. Each statement
  keeps its own reason. The combined result follows the selected rule, and
  nothing is netted.
- The same two statements with identical answers. This guards against a fix
  that only works when answers differ.
- Correct the purchase cost on one statement across the gain/loss boundary;
  withdraw an answer on the other. Only the touched statement's result
  changes.
- Record "no Form 1099-K", then two statements, then withdraw one. Closure
  and the zero entry behave as the single-statement route does.
- Retain P0's two-Form-1098 stop observations and unchanged single-statement
  behavior as compatibility evidence. No multi-mortgage computation is built.
- A single statement of each kind, unchanged from the merged behavior, as the
  regression guard.

## Contracts, production conditions and verification

The lifecycle repair allocated ADR 0079 and the kernel payload schema
`act-family-handover.v1`, both owner-accepted. Track 1 allocates the content
and package successors the connected design names; nothing else is allocated. Inspect accepted contracts and adopted versions
before selecting reuse. Keep document evidence, ordinary answers, tax meaning
and results distinct.

Production exit requires all of the following:
- a person with two Forms 1099-K can record and correct each statement's
  account;
- the combined Schedule 1 entry follows 2025 authority exactly once;
- each statement's reason and figures survive in the saved explanation;
- a correction to one statement leaves the other unchanged;
- the selected Form 1098 outcome is either delivered or kept as a named,
  explained limit;
- single-statement behavior and saved history are unchanged.

An explicit partial result remains possible by owner disposition.

Builder charters specify focused positive, boundary, lifecycle and
compatibility tests. At least one test must answer through the offered
questions for two statements, not through hand-built numbers. Every displayed
status follows the recorded outcome. Independent review is required for P0,
connected-design closure, any engine change and the curated candidate. CI is
the full regression gate.

Only synthetic `demo.*` evidence enters the repository. Follow AGENTS.md's
data, fixture and schema-publication rules. Browser observation is not
required.

### Targeted verification during implementation

By owner direction (2026-10-19), implementation units do not wait on PR CI
or run the full suite. They use the two lanes below. The full suite, CI
`verify` and any repairs they expose are taken together at milestone
closeout.

**Core lane** (seconds; after each increment):

```sh
pytest tests/test_family_handover_fold.py tests/test_family_handover_actlog.py \
  tests/test_family_handover_recording.py tests/test_act_log.py \
  tests/test_act_log_batch.py tests/test_schema_registry.py \
  tests/source_completeness/test_track2_horizon_projection.py \
  tests/source_completeness/test_track5_lifecycle.py \
  tests/source_completeness/test_exact_family_version.py \
  tests/test_f1099k_content_successors_increment_a.py \
  tests/test_multiple_statement_sale_input_transport_increment_b.py \
  tests/test_f1099k_statement_removal_increment_c.py
```

**Unit lane** (about 4.5 minutes; at the end of each unit, after the core
lane):

```sh
pytest tests/test_f1099k_computation_rules.py \
  tests/test_f1099k_statement_recording.py tests/test_f1099k_statement_review.py \
  tests/test_f1099k_personal_item_sale_track1.py \
  tests/test_f1099k_personal_item_sale_demonstration.py \
  tests/test_f1098_circumstances_calculation.py \
  tests/test_f1098_circumstances_explanation.py \
  tests/test_f1098_circumstances_vocabulary.py \
  tests/test_ssa1099_benefits_line6_track2.py \
  tests/test_frrs_t4_w2_live_integration.py \
  tests/test_dsbs_t4_dividend_live_integration.py \
  tests/test_schedule_d_form8949_covered_wash_sale_t1.py \
  tests/test_sli_deduction_end_to_end.py \
  tests/test_f1099k_saved_presentation_increment_d.py \
  tests/test_multiple_statement_sale_acceptance.py \
  tests/test_multiple_statement_candidate_repairs.py
```

Together they cover the kernel handover and save fences, closure marshalling
and containment, the Form 1099-K route from recording to saved review, the
one-statement Form 1098 neighbor, closure-marshalling neighbors on v1 and v2
wash-sale bases, and one return-level student-loan story that consumes
per-statement results. Both lanes passed together before Track 1: 326 passed,
66 subtests, 4m22s. Run `python -m mypy` with the unit lane; the lanes as first written omitted
it. A unit adds its own new test modules to the lane it
belongs in. A unit that changes `packages/derivation/live.py` transport or
`presentation_projection.py` also runs the existing modules that exercise
the touched function, named in its report.

## Track 0 adversarial closure

Evidence: `track0-closure-evidence.md` and its executed probe
`test_track0_closure_probe.py` (12 passed), in the milestone
evidence directory. The probe records through the real Form 1099-K writers
(`family_version="v2"`), the accepted handover (ADR 0079), `ActLog`,
`live_coordinate_run` and the presentation projection, against disposable
successor content in a temporary directory. **Input transport is
instrumented**: it wraps `_resolved_run_material` with the design's
emission predicate, skipping mismatches silently. Production transport and
its named refusal remain Unit 1's proof, through the real recorder.

Facts the closure relies on beyond the probe:
- **Top-entry consumers.** Only the Schedule 1 attachment rule consumes
  `tax.us.2025.schedule1.top-entry` (content search of
  `packages/content/tax/2025/rule.*.json`). No Schedule 1 line or Form 1040
  rule reads it, so income and tax do not depend on the entry, as the previous
  milestone established.
- **v1 claim.** The v1 claim reads "Closed with members authorizes one
  statement's Box 1a; closed-empty authorizes subtotal 0. Does not authorize
  a multi-payer sum." (`family.f1099k.json`).

- **Authority-lifecycle table: PASS.** Evidence section 1, with the per-statement
  reason finding added: it is derived per subject from that statement's Box
  1a and answers, and is invalidated by that statement's answer correction or
  withdrawal, or by a statement correction. A v1 closure is invalidated by a
  v1 member transition or by handover (ADR 0079). It is never copied.
- **Empty/nonempty authority matrix: PASS.** Closed-empty v2 publishes $0.00
  (`test_case4`); a missing absence authority blocks `SOURCE_SET_UNCLOSED`
  (`test_case5b`); nonempty eligible publishes $1,340.00 with a two-row
  attachment tie-out (`test_case1`); a published non-loss or an excluded
  statement blocks `DEPENDENCY_ABSENT`, and the sibling keeps its own status
  (`test_case2`, `test_case6`); a blocked subject blocks `DEPENDENCY_INVALID`
  naming that statement's Box 1a (`test_case3`). Neighbor: only the
  attachment follows the entry; Form 1040 totals are independent of it.
- **Late-member lifecycle: PASS.** `test_case7` observes the closure on
  `demo.f1099k.h36` displaced when statement B advances the chain to `h37`;
  an intermediate run blocks `SOURCE_SET_UNCLOSED`; the fresh closure on `h37`
  and run 2 publish $1,340.00 pinning it and both reasons. Upgrades:
  `test_case8` and `test_case9` show the v1 closure displaced at handover and
  fresh closure required on the post-transition horizon.
- **Neighboring capability dependency diff: PASS.** No new prerequisite falls on
  a return without Form 1099-K activity beyond the existing Schedule 1
  question. Single-statement workspaces on core calculations v46–v48 keep
  writing v1 (`FAMILY_VERSION` stays v1); the unit test lane's Form 1099-K
  modules on v47/v48 pass in the unit lane. The one-statement Form 1098 route is
  untouched; its circumstance modules pass in the same lane. Product cost,
  stated rather than hidden: a workspace whose Form 1099-K answer is on v1
  (including "no Form 1099-K") does not calculate the Schedule 1 entry under
  the successor package until the person answers again. That follows the
  accepted no-copied-closure rule; it fails closed and affects no other
  calculation.
- **Reused-claim semantic/lifecycle equivalence: PASS.** The closure claim is
  not reused across versions. The member fact
  `tax.us.2025.f1099k.box1a-gross-amount` is reused with the same proposition,
  keys (`payer`, `statement`, `tax-year`) and lifecycle; a retained statement
  stays current across handover and joins the v2 subtotal (`test_case9`).
- **Integration surface: PASS.** Bindings of the top entry and attachment:
  the form-field binding `schedule1.top-entry.form-field.json` (exactly one
  value or a blocked disposition; `test_case10` validates the presentation
  model with 1340); the attachment part `sch1-top-entry-f1099k` (sum ties to
  the entry, one row per member; `test_case1`); the per-statement explanation
  (one entry per statement, each with its own Box 1a and reason;
  `test_case10`); the statement review reader in
  `packages/tax/f1099k_statement_review.py` (own Box 1a per statement;
  `test_case10`); the unresolved rule (one disposition; `test_case1`,
  `test_case2`); and the family `authorizes_subtotal` and closure mapping,
  which the successor family points at the raw Box 1a subtotal.
- **Known limitations affecting correctness: none.** Remaining limits are
  explicit exclusions or fail-closed costs: no gain or break-even reporting;
  one Form 1098; a v1 workspace re-answers its Form 1099-K question under the
  successor package; transport and statement removal are proven only in their
  production units.

Track 0 is settled. Track 1 built the design's units, each verified through
the recorder and coordinator with the targeted test lanes above.

## Phase assessment after delivery

Assess whether the phase's provisional endpoint is met with multi-statement
support in place. Compare what the shared mechanism made reusable with what
each route still needed. Recommend concluding the phase or naming one
further bounded step. The next phase remains unselected.

**Assessment (Foreman, 2026-10-19).** The provisional endpoint is met.
- **Delivered breadth.** Two distinct contexts beyond the inherited student
  loan route have bounded production paths from ordinary answers to a tax
  result and a saved explanation: mortgage interest (one Form 1098) and
  personal-item sales (now any number of Forms 1099-K). The sale route goes
  beyond borrowing deductions. Correction keeps the source report and
  unrelated answers in both.
- **What transferred.** The adopted student-loan pattern carried the
  combination with no new rule schema: a plain subtotal rule and a selection
  that reads each statement's result. Recording, correction and the saved
  reader transferred again.
- **What needed new work.** Per-statement input transport for the sale
  answers, and a kernel lifecycle contract (ADR 0079) so a successor family
  version takes over completeness authority instead of coexisting with it.
- **What remains unsupported.** More than one Form 1098, which needs debt and
  home identity across loans; gain and break-even reporting on Form 8949 and
  Schedule D; assumptions beyond the stated ones.

The Foreman recommends concluding the phase. A bounded engineering-health
milestone is the strongest next candidate: `verify` takes about 2.5 hours and
the full suite about 29 minutes, and both slowed every unit here. Gain
reporting, multiple Forms 1098 and the inherited preferential-rate defect are
the product candidates. The owner selects.

## Execution record

| Unit | Result |
| --- | --- |
| P0–P7 | Recording keeps statement identity, but calculation inputs lose it. Independent review set aside a schema successor for the adopted student-loan pattern (Candidate C). The owner selected Policy 1 and kept the one-statement Form 1098 limit. |
| Shared authority | The exact-version candidate selected closure authority by exact family version. Independent review found Finding 1: a change through the other current version left the selected closure and its saved zero current. The owner approved a lifecycle repair. |
| Lifecycle contract | An outline, carrier comparison and four-increment proposal were reviewed. The owner selected handover on the first successor-version write, a lifecycle-kind pre-save fold, refusal of two current versions, and fresh v2 wash-sale fixtures. |
| Handover implementation | `act-family-handover.v1`, the fold, save fences, containment and writer changes, reviewed READY. The owner accepted ADR 0079. The fixture policy repaired the 174 failures the candidate had left in CI. |
| Track 0 | The connected design was aligned with ADR 0079 and reviewed READY. An executed probe of every disposition path settled the adversarial closure. |
| Track 1 | Core calculations `v49`, registry `v47`, release `v47`; writers take the family version from the adopted package; bounded per-statement transport with a named refusal; single-save removal; per-statement saved projection and review; 13 acceptance cases. Reviewed READY. |
| Closeout repairs | Three review scrutiny items repaired. Full suite on the pre-curation candidate: 3131 passed, 20 skipped. |
| Candidate repair | The owner reproduced four defects in the curated candidate: re-recording a removed statement saved a displaced fact; colliding statement ids merged two explanations; a populated v1 workspace on v49 could not re-attest without a new statement; and a local supported loss was described as entered while the entry was blocked. Each was repaired with a regression through the real writers: the removal refusal checks the withdrawn fact and an unchanged log; the identity, re-attestation and wording repairs also run the coordinator and reload the saved presentation. Both closure routes now refuse an older requested family version, as the other writers do. |

## Outcome

**What a person can do.** On a synthetic account, record any number of Forms
1099-K, or that none was received. Answer the ordinary sale questions for each
statement, and save, correct, withdraw or remove each statement's account
without changing another's. Read a saved explanation for each statement beside
the combined entry. README, "Personal-item sale on Form 1099-K", is the
runnable account.

**What the calculation does.** When the family is closed and every current
statement's reason is a supported personal loss, the Box 1a amounts are added
and entered once at the top of 2025 Schedule 1. Income and tax do not change.
A closed family with no statements enters $0. Any other reason, a blocked
statement, or an unclosed family blocks the entry, and each statement keeps
its own reason. A workspace first recorded on the v1 family hands over to the
successor in the same save as its next write. Completeness is then asked
again. A workspace that has not written since stays as it was until the
person answers again; answering the completeness question records the
handover and the fresh closure in one save, with no statement added. A
removed statement cannot be recorded again under the same identity. Saved
explanations and reviews match each statement by its full identity keys, and
a statement's own supported loss is not described as entered when the
combined entry is blocked.

**Evidence.** ADR 0079, `connected-sale-design.md`, the Track 0 closure above
and its probe hold the decisions. Behavior is in the handover, transport,
removal, projection and acceptance tests. CI's `verify` check on the final
candidate is the regression gate.

**Limits.** No gain or break-even reporting; one Form 1098; no recovery for a
log with two current family versions; no browser observation; synthetic
accounts only. The inherited preferential-rate defect and the 22 fast-lane
budget failures are unchanged.
