<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "saved-account-resumption",
  "status": "Initial plan. Trace reopening an existing synthetic workspace after the correction process ends; review that evidence before selecting the implementation.",
  "scope": [
    "reopen the same saved workspace without reseeding its account",
    "recover current answers and distinguish saved results from later changes",
    "continue the existing borrowing-answer correction interaction after reopening"
  ],
  "non_goals": [
    "no new tax coverage, question vocabulary or general assumption management",
    "no personal workspace use, cloud sync or multiple-user identity design",
    "no preservation of unconfirmed reviews as authority to save after restart"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/phases/evolving-workspace-accounts/milestones/saved-account-resumption.md",
      "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-overview.md",
      "docs/phases/evolving-workspace-accounts/milestones/account-review-correction.md#Outcome",
      "docs/milestone-retrospectives/2026-10-09-account-review-correction.md#What should change in the next plan"
    ],
    "implementation": [
      "docs/phases/evolving-workspace-accounts/milestones/saved-account-resumption.md",
      "docs/process/planning-and-development.md",
      "docs/adr/INDEX.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/evolving-workspace-accounts/milestones/saved-account-resumption.md",
      "docs/roles/qualitative-review.md",
      "docs/process/planning-and-development.md"
    ]
  }
}
-->

# Returning to a Saved Account

Milestone key: `saved-account-resumption`.
Branch: `milestone/saved-account-resumption-student-loan`.

## Purpose

A person corrects an answer, stops working, and comes back later. Their answer
and its history should still be there. The application should show which
result was calculated from that account and let them continue working without
starting from the demonstration's original answers again.

Use the existing student-loan question: whether a named borrowing paid only
for school costs. The preceding milestone made that answer correctable from
its result and explained the recalculation. This milestone makes the same
bounded interaction usable across a complete stop and restart of its process.

The difficult question is how to reconnect an existing account, its saved
calculations and a fresh interaction. A browser refresh can recover an outcome
from a running session. Returning after that session ends must rely on durable
records, rather than the old session's memory. A saved answer can survive even
when its calculation did not finish. An earlier result can remain valuable
without describing the answers that are current now.

Success is a reproducible sequence: initialize a synthetic workspace once,
correct an answer, end the process, reopen the same workspace, inspect the
saved answer and result, and make another reviewed correction. An unrelated
borrowing and the earlier outputs keep their identities and history.

## Starting evidence

Reviewing and Correcting the Account Behind a Result merged in PR #206. Its
Outcome records the capability and its limits. The adopted calculation is
core-calculations v42; no different calculation policy is selected here.

- `packages/derivation/correction_session.py` holds the correction runtime.
  Its constructor seeds an empty log, and `_seed` refuses a nonempty workspace.
  Prepared reviews, completed outcomes and retry state are held in memory.
  Inspect the current consumer paths before concluding what can be recovered
  from the log and saved run outputs.
- `packages/derivation/runners/sli_correction_evaluation.py` creates temporary
  workspaces for the opening result and correction session. Its normal stop
  disposes of them. The historical demonstration reconstructs a scenario;
  it is not a test of reopening the same workspace after process termination.
- The existing reviewed recorder saves the answer and its predecessor in the
  act log. `live_coordinate_run` writes calculation records and outputs.
  These are starting mechanisms to investigate, not proof of a complete
  resumption path or a durable record of every session outcome.
- `tests/test_sli_correction_session.py` and the README correction walkthrough
  describe runtime, transport and browser checks. Preserve their existing
  behavior while adding the process boundary to the evidence.

P0 must confirm these observations and inspect neighboring fields and readers.
Read the exact accepted recording, residency, run-authorization and surface
contracts where the proposed path depends on them. ADR 0049 and ADR 0051 route
surface delivery and entry; their index descriptions do not settle a new
storage or restart contract. No schema or ADR change is selected in this plan.

## What the application must preserve and explain

Reopening reads the existing workspace. It does not replay seed acts into it,
replace its log, or save a copy of an answer to make it available again.
Fixture creation and opening an existing workspace must be distinct operations.
Use the existing residency capability and adoption checks for every operation.
The browser never supplies a filesystem location or chooses a different account
by posting an identifier from an old page.

The current answer comes from the recovered account. An earlier result keeps
the explanation of what that calculation used. Opening it can lead to a fresh
review of the current answer, with the earlier and current answers identified.
An old review token grants no permission to save in a new process.

The application must distinguish three ordinary situations:

- The answer was saved and a matching calculation is available. Show that
  result and its history, with the basis for calling it current established.
- The answer was saved but no matching usable calculation is established.
  Show the saved answer and offer calculation without saving the answer again.
- The records do not establish what happened. Say what is known and what
  remains unresolved; do not infer success from a filename or a favorable
  number in an older output.

An outcome from the old session may be reconstructable, or it may require
additional durable information. Decide this from actual artifacts. The minimum
goal is recovery of the account and honest calculation state; it does not
require recovering every HTTP response, reopening a prepared confirmation, or
continuing a transaction interrupted at an arbitrary instruction.

A saved result is usable as current only under an explicit checked relationship
to the recovered workspace, adopted calculation and scope. P0 must determine
what the existing artifacts establish. Modification times and filename order
are not that relationship. If determining currency requires more than the
bounded consumer can establish, offer a fresh authorized calculation and keep
the old output historical. Do not force a general run-history design to avoid
that honest fallback.

## Develop the plan through evidence

### P0 — trace one stop and return

Charter one small investigation. On synthetic data, save a correction through
the existing reviewed recorder and calculate through `live_coordinate_run`.
Stop the process that owns the runtime. Start a fresh process against those
same files and trace what it can establish without copied Python objects or
reconstructed seed data.

Produce a short walkthrough of what the person sees and a map from each claim
to its durable source. Trace workspace opening, bundle and package adoption,
finding identity, predecessor history, result identity and calculation scope.
Include a saved correction whose calculation did not finish. Identify the
missing connection rather than assuming a new store is necessary.

Independently review this evidence and the initial plan before expanding the
design. Check that reopening truly crosses process lifetime, and that a
reconstructed fixture or in-memory outcome is not standing in for recovery.
Revise the plan when the evidence changes the chosen boundary.

### P1 and Track 0 — select the smallest working route

Prefer reuse where P0 establishes the contract. Use a small executable probe
only for a consequential uncertainty: for example, whether existing durable
artifacts can identify a matching result after reopening. Compare alternatives
only when a case can distinguish their consequences. A new schema, durable
index or session journal needs a concrete missing property and reviewed
contract before implementation depends on it.

Track 0 adversarial closure is **PENDING**. Before an implementation charter,
settle the applicable authority/lifecycle table, empty and nonempty states,
late-change cases, neighboring dependencies, reused claims and integration
payloads. In plain language, answer: what makes this the same account, what
makes this result applicable to it, what survives reopening, and what must be
prepared again? Review the selected route independently.

### Implementation and integrated review

Provisional units are:

1. Open an existing synthetic workspace and recover its answer/history and
   honest result state. Keep one-time initialization separate. Integrate the
   current correction page and recorder as early as possible.
2. Complete the stop/reopen/calculate/correct workflow, its bounded failure
   cases, and a reproducible owner walkthrough.

Combine these units if splitting them would hide the recovery connection.
Review the first integrated stop-and-return interaction independently before
adding the rest of the cases. The final curated candidate also receives
independent review. Keep the plan, charter and displayed claims consistent
with what the executed path establishes.

## Cases and verification

Use Cedar and Birch with the existing question and response vocabulary.

| Situation | Observation that decides the case |
| --- | --- |
| Correct Cedar, calculate, stop and reopen | The successor and predecessor survive; Birch's findings and earlier outputs are unchanged; the recovered display uses the actual saved account |
| Save Cedar's correction, calculation refuses, then stop and reopen | The saved correction remains; calculating again writes no second correction |
| Prepare a confirmation, stop, reopen and submit its old token | No correction is saved from the expired review; a new review reads current context |
| Make a later supported change before reopening an older result | The old result stays historical and correction starts from the current answer |
| Open a workspace with no completed calculation | The account can be inspected or calculated where authorized; no invented zero or completed result |
| Encounter a missing or unreadable result artifact | The account is not reset; the display distinguishes missing calculation evidence from a lost answer |
| Reopen twice without editing | No seed acts or replacement findings are appended |

Exercise at least one real process termination and restart, with the same
workspace files retained between them. Read the log and outputs to check exact
finding identity, predecessor, revision and pins. Verify that a displayed
currentness claim follows the selected checks and that a stale result cannot
silently become current. Keep fixture setup, new implementation and executed
observations explicit.

Run appropriate repository checks and use final CI as the publication gate.
No personal files are needed. Persistent synthetic workspaces belong beneath
ignored paths; stable committed fixtures use `demo.*` identities. Do not expose
local paths in page responses or commit generated private output.

Show the owner the stop-and-return walkthrough before freezing wording.
Browser-tool failure should lead to a reproducible owner walkthrough with the
unverified visual checks named. The predecessor's independent-reader assessment
remains open; automated checks do not establish that assessment.

## Decisions and completion boundary

P0 must establish the durable sources for recovery and the existing authority
to open and calculate. Track 0 must choose whether to reuse a matching saved
result or calculate afresh when its currency cannot be established, and name
any required new contract. Each consequential decision should explain the
user consequence, cost and evidence that supports it before dependent work.

Completion is one supported answer usable across stopping and returning, with
history preserved and calculation state explained truthfully. Personal workspace
entry, crash recovery for partially committed writes, cloud sync, multiple
users, form importing, additional questions, free text, allocation and new tax
coverage are outside this milestone. Surface and engine neighbors must remain
usable under their existing contracts.

The previous two milestones already support a bounded phase exit. This is an
owner-requested additional milestone, not a revision of those achievements.
At closeout recommend whether to conclude Evolving Workspace Accounts with
this practical returning-user path. No further milestone is automatic.
