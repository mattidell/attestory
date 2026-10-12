<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "saved-account-resumption",
  "retrospective": "docs/milestone-retrospectives/2026-10-11-saved-account-resumption.md",
  "status": "Closed 2026-10-11. A synthetic correction account can be initialized once, corrected, stopped and reopened by a new process from its files alone. The reopened page shows each loan-cost answer with its predecessor, the latest earlier result and the calculation state, calculates without saving again, and continues the correction. The foreman recommends concluding the phase; that is the owner's decision.",
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
      "docs/milestone-retrospectives/2026-10-11-saved-account-resumption.md",
      "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-overview.md",
      "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md",
      "docs/phases/evolving-workspace-accounts/milestones/saved-account-resumption.md"
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

#### P0 result and R1 disposition

P0 ran three synthetic accounts across a real process boundary. Process A was
killed with `SIGKILL`, and process B received only the workspace directory.
R1 reran the probe, confirmed the boundary and the stable identities, and
returned **READY WITH CORRECTIONS**. All four corrections and both minor notes
are adopted here.

What survives a stop, as executed:

- The act log reopens byte for byte. Opening it twice writes nothing to the
  workspace.
- Cedar's corrected loan-cost answer is current, and it names its displaced
  predecessor (`correction_of_finding_id`). Birch's findings and Cedar's
  enrollment answer are unchanged.
- A reviewed save survives a calculation that raises. A fresh process can
  calculate the saved account through `live_coordinate_run`, which appends
  run records and outputs but no act.
- Run records, outputs and presentations carry the run id, the workspace
  revision passed by the caller, the v42 package pin, empty governance pins
  and ADR 0069's authorization standing (`AUTHORIZATION_ABSENT`, `current`
  false). A fresh review reads the current account and writes nothing.

What is missing:

- **An opening path.** `CorrectionRuntime` always seeds and refuses a
  nonempty log. Nothing reads an existing account into the page.
- **A checked claim that a saved result applies to the current answers.**
  No reader joins a result's revision, package and surface to the log. The
  surface is not recorded, nor is any digest of the acts. A
  presentation's revision is the integer its caller passed. R1 found the
  fresh calculation to be the supported route (Decisions, below).
- **Durable session state.** Tokens, outcomes, the retry counter and the
  historical flag exist only in the old process's memory. Nothing needs to
  be added for them, since an unconfirmed review is never authority after a
  restart. But an old token is refused today only because a new process's
  map is empty (R1 finding 5). The selected route must refuse it by design,
  and the plan's case still submits the old token.
- **A durable record that a calculation did not finish.** The save is in
  the log; the failure is not. That is not the same as a deleted output: a
  completed calculation leaves its started and completed run records even
  if its output file is later removed (R1 finding 4).
- **The opening result lived in another workspace.** The current runner
  calculates the opening result in one temporary workspace and seeds a
  second one, so "same account" rested only on equal seed acts.

R1 also noted that the existing page shows "Saved and recalculated" together
with "Line 21: blocked (not calculated this run)" when a correction blocks
line 21 (finding 6). That pair is not a truthful account of a calculated,
blocked line, and it is not the resumption wording.

### P1 and Track 0 — select the smallest working route

Prefer reuse where P0 establishes the contract. Use a small executable probe
only for a consequential uncertainty: for example, whether existing durable
artifacts can identify a matching result after reopening. Compare alternatives
only when a case can distinguish their consequences. A new schema, durable
index or session journal needs a concrete missing property and reviewed
contract before implementation depends on it.

Track 0 adversarial closure is **CLOSED** (R2, below). Before an implementation charter,
settle the applicable authority/lifecycle table, empty and nonempty states,
late-change cases, neighboring dependencies, reused claims and integration
payloads. In plain language, answer: what makes this the same account, what
makes this result applicable to it, what survives reopening, and what must be
prepared again? Review the selected route independently.

#### Track 0 — the selected route

No P1 probe is needed. P0 executed every mechanism this route reuses. The
remaining uncertainty is in the connection, which the integrated review
tests directly.

**In plain language.**

- *What makes this the same account?* The directory the runner is handed,
  outside the repository, as the workspace capability. Opening reads that
  directory's log. No other identity is introduced. The page never names,
  chooses or receives a location.
- *What makes a result apply to it?* Only a calculation this process performs
  from the log it holds, at the revision it read, under the package adoption
  current at that revision and the session's fixed calculation surface (the
  core-calculations `PublicationSurface`, not the page artifact). Every
  result saved by an earlier process stays an **earlier result**. Its
  explanation still says what that calculation used.
- *What survives reopening?* The answers and their predecessors, run records,
  outputs and presentations.
- *What must be prepared again?* Every review and confirmation. Tokens,
  outcomes and retry counts belong to one process.

**Wording boundary.** ADR 0069 uses "current" for authorization standing, and
these synthetic runs record `AUTHORIZATION_ABSENT`. The page does not call any
result "current". It says that a result was calculated from the answers shown
in this session, or that it is an earlier result. The exact words wait for the
owner walkthrough.

**Selected route.**

1. **Initialize and open are separate operations.** Initializing refuses a
   directory that already holds a log and seeds the named synthetic state
   once. It then reads the log back (`ActLog.read`) and calculates the opening
   result from that read's acts and revision, in the same workspace, with the
   session's fixed run scope, scope user and calculation surface. A
   caller-supplied revision or act list never stands in for the read (R2
   finding 1). Opening refuses a
   directory without a log and never seeds. Both use the existing residency
   bootstrap and adoption checks. The runner's existing temporary-workspace
   states keep working unchanged.
2. **The opened page, before any calculation**, shows three things, all read
   from the files:
   - Each borrowing's current loan-cost answer and its predecessor. The
     predecessor is named by the edge the correction recorded: the displaced
     finding on that fact whose correction reason's `by` is the current
     finding (`currency.py`), cross-checked against the successor's
     `correction_of_finding_id`. Listing every displaced finding is not
     history (R2 finding 5).
   - The latest earlier result, located by identity. That is the last
     record in the record stream's own order (`RecordStream.read().records`)
     whose `phase` is `completed`, not the last key of `standings()`. Its
     presentation is found by reading the presentation files under this
     workspace's `outputs/` and matching the `runId` field to the record's
     `run_id`. The filename chooses nothing, so the opening result's
     `initial.presentation.json` is found. When no file matches, the result
     is reported as an earlier result whose file is unavailable. When two
     files match, the page says which file is not established (R2 finding 4).
     No completed run is reported as "no result has been calculated for this
     account". A started run with no closing record (`open_runs`) is
     reported as a calculation that did not finish, whether or not an
     earlier completed run exists.
   - If the record stream does not read (`RecordStreamCorruption`) or has an
     incomplete tail, the answers are still shown. The page says that the
     result records are not established. Nothing is seeded or reset (R2
     finding 2).
   - One action: calculate from the saved answers.
3. **Calculating** runs `live_coordinate_run` once over the log read under
   the session lock. It appends run records and outputs, never an act. The
   output name comes from this process's own serial, never from a token or an
   earlier output. If the calculation refuses or raises, the page says it did
   not calculate and the account is unchanged. Calculating again saves
   nothing.
4. **After a calculation**, the existing interaction runs on that result
   unchanged: choices from its displayed answers, then `choose`, `confirm`,
   `cancel`, `outcome` and `retry`. The predecessor milestone's safeguards and
   outcome distinctions apply as they are.
5. **Tokens are bound to the process that issued them.** Each runtime holds a
   random session identity in memory, and every token names it. A token from
   another session, including an unprefixed token from today's format, is
   refused because it names a different session, before any map is read. On
   such a token, `confirm` stays a refusal and saves nothing. `outcome`
   returns `unknown`, so the page shows its existing undetermined sentence.
   `retry` stays an error with the existing "Calculating again did not
   complete." The page never sends `unknown` through the not-saved display,
   and it then drops the stored token. The account shows as read from the
   log, so any correction the old session saved is visible as the current
   answer with its predecessor. Nothing is saved again (R2 finding 3).
6. **The page artifact** is built for each opening into a target new to that
   opening, because the existing build refuses an existing target. The server's
   static root is that target. Earlier builds are left in place and not served. This is the only write that
   opening performs, and it is outside the log.
7. **Line 21 wording.** The page states line 21's disposition from the model's
   `resolved.disposition`, so a blocked line is not described as "not
   calculated" (R1 finding 6).
8. **No "not current" banner from a caller flag.** An earlier result is shown
   with the earlier-result sentence. The `historical` flag stays false on the
   opening path. The page does not render ADR 0069's `current` or
   `authorization` fields as account currency (R2 finding 6).

**Authority and lifecycle.**

| Operation | Authority | Writes | After a restart |
| --- | --- | --- | --- |
| Initialize | Capability; adoption checks; refuses an existing log | Seed acts once; opening run records and outputs | Never repeated on the same directory |
| Open | Capability; refuses a missing log | Surface build target only | Repeatable; appends nothing to the log |
| Read the opened account | None beyond open | None | Recomputed from files |
| Calculate | Capability; adopted package at the revision read | Run records and outputs; no act | Earlier results stay earlier |
| `choose` / `cancel` | This session's calculated result | None | Gone |
| `confirm` | This session's token; the reviewed recorder's revalidation | One reviewed correction; then a calculation | The saved correction survives; the token does not |
| `outcome` / `retry` | This session's token only | `retry`: run records and outputs | Old tokens report "unknown to this session" |

**New contracts:** none. No schema, ADR or durable store is selected. The
session identity is held in memory only.

**Alternatives not selected.**

- *Reuse a saved result as current when its revision matches the log.* The
  files do not establish it (R1 finding 2). It would need a new checked
  relationship and an owner decision.
- *Persist sessions, tokens or outcomes.* This is a non-goal. The log already
  holds whatever was saved, and an unconfirmed review grants nothing after a
  restart.
- *Calculate automatically on opening.* Every opening would write run records.
  It would also hide the saved-but-not-calculated state that the person needs
  to understand. Opening stays a read.

**How the cases decide this route.**

| Plan case | Decided by |
| --- | --- |
| Correct, calculate, stop, reopen | Answer and predecessor ids from the log, byte-identical neighbors, the earlier result located by run id, and a new calculation writing no act |
| Saved, calculation refused, stop, reopen | The saved answer shown as current with its predecessor, the earlier result shown as earlier, and one calculation leaving the act count unchanged |
| Old token after a restart | Refused by session identity on `confirm`, `outcome` and `retry`; no act appended; the page never shows "Not saved" for it; a new review reads the current account |
| Later change, then an older result | The older result is labeled earlier; choices come only from this session's calculation |
| No completed calculation | No earlier result is invented; a started run without a close is stated as did not finish; calculating is offered |
| Missing or unreadable result file | The account and answers are shown; the earlier result is reported as unavailable, not lost |
| Reopen twice | Log bytes unchanged; only a new surface build target |

#### Track 0 adversarial closure

R2 reviewed the draft adversarially against code and returned **READY WITH
CORRECTIONS**: four corrections and two minor notes, each adopted above.

- **Opening result.** It is calculated from a log read, not a
  caller-supplied revision.
- **Unreadable record stream.** It leaves the account visible.
- **Last completed run.** It is the last `completed` record, not the last
  standing.
- **Old tokens.** They are refused before any map on all three routes, and
  never shown as "Not saved".
- **Presentation join.** It matches the `runId` field within this workspace
  and reports duplicates.
- **Predecessor.** It is the recorded correction edge.
- **Surfaces.** The calculation surface and the page artifact are kept
  distinct, and no caller-set "not current" banner is shown.

R2 confirmed that the predecessor's distinguishability check no longer
depends on `choose` (`_require_card_distinguishable_in_workspace` reads every
current borrowing). It also listed each safeguard with the inputs its caller
must supply. The integrated review checks those inputs at the production
caller.

### Implementation and integrated review

The units are:

1. **Track 1, the first working stop and return.** Build the selected
   route, items 1 to 8, through the existing page and recorder. Prove it
   across a real process kill and restart for three cases:
   - a completed correction;
   - a saved correction whose calculation did not finish;
   - an old token.

   **Complete.** Constructing today's `CorrectionRuntime` is not the opening path. It
   always seeds and refuses a nonempty log (R1 finding 3).
2. **Track 2, the remaining cases and the owner walkthrough.** The cases
   are:
   - a missing, duplicated or unreadable result file;
   - a record stream that does not read;
   - a calculation that started and did not finish;
   - a later change before an older result is reopened;
   - reopening twice;
   - the README walkthrough and its browser paths.

   Track 2 also lands R3's corrections first. **Complete**, with R4's
   repair (below).

Combine these units if splitting them would hide the recovery connection.
Review the first integrated stop-and-return interaction independently before
adding the rest of the cases. The final curated candidate also receives
independent review. Keep the plan, charter and displayed claims consistent
with what the executed path establishes.

## Track 1 integrated review

Track 1 built the selected route through the existing page and recorder. R3
reviewed it as an interaction across real `SIGKILL` restarts. It ran the
owner walkthrough over HTTP and in the headless-Chrome client, and returned
**READY WITH CORRECTIONS**.

What the integrated session establishes:

- Opening never seeds, and its log bytes are unchanged.
- The opening result is calculated from the log read.
- The earlier result is the last `completed` record, joined by `runId`
  within the workspace. Renamed files still resolve.
- Calculation holds the lock from the read through the run and appends no
  act.
- Old tokens are refused before any map on `confirm`, `outcome` and `retry`,
  and the page shows the undetermined sentence.
- The next correction names the previous successor as its predecessor.

R3's corrections, all for Track 2 before page text is frozen:

- **Damaged file.** An unreadable presentation file is reported with the
  "more than one file matches" sentence.
- **Calculated result.** The result calculated in this session is headed as
  an earlier result.
- **Superseded answer.** Inside an earlier result, a superseded answer is
  rendered under "Current." That happens when the earlier result predates the
  saved correction, as in the case where the calculation did not finish.

Two minor findings: the runner's restart line tells a persistent workspace to
run `--init` again, and the page drops its token on a retry response lost in
transit.

## Track 2 review and repair

R4 reviewed Track 2 and returned **READY WITH CORRECTIONS**. It also recorded
the visible text of every walkthrough screen from the rendered page in
headless Chrome. It confirmed three things:

- R3's five corrections hold.
- All eight cases are produced honestly. The open run comes from a process
  killed between its started and closing records, and the empty account from
  a refused opening calculation. Product code has no failure switch.
- The README matches the served page.

R4 found one defect. The second process ever to press "Calculate from the
saved answers" on a workspace failed silently. Its output name came from a
serial that restarts with each process, so it collided with the earlier
process's reserved file. The exception was swallowed and reported as "did not
calculate". The repair:

- Each runtime adds its own random nonce to the run id and output name.
- A regression test calculates in two successive runtimes on one workspace.
  It fails before the repair and passes after.

R4 also noted that an interrupted run's empty output reservation made every
later earlier-result lookup in that workspace read as "a file beside it
could not be read". An empty file is a reservation that was never written and
carries no `runId`, so the lookup now skips it. A non-empty unreadable file
still has its own status.

## Owner review repairs

The owner reviewed the curated candidate and found two more places where a
failure to receive or read something was presented as a different failure.

- **A lost calculate response.** A real reproduction calculated, saved its
  presentation, and dropped the HTTP response. The page said "This session
  did not calculate", although the session held the result. The page now
  separates an explicit answer that the session did not calculate from an
  answer it never received. In the second case it reads the session's state
  once and shows what it holds.
- **An uninterpretable earlier explanation.** A valid JSON presentation whose
  row named a missing reason raised during the opened state. The account it
  sat beside was hidden with it. Rows that were not objects were silently
  skipped, so an incomplete explanation rendered as if it were whole. The
  reader now checks that the explanation can be read whole. A failure there
  is unavailable explanation evidence: the answers, predecessors and
  calculate action remain, and no part of the explanation is shown.

Three tests failed before these repairs and pass after them:
- the served-page lost-response test;
- the two structural damages to the actual saved file, read by a new
  process.

The explicit-refusal test passes on both, as it should.

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
No personal files are needed. A persistent synthetic workspace is a directory
outside the repository, supplied at run time as the workspace capability
(ADR 0031 Decisions 1 and 4; `_assert_topology` refuses any location inside
the repository, ignored paths included). Stable committed fixtures use `demo.*`
identities. Do not expose
local paths in page responses or commit generated private output.

Show the owner the stop-and-return walkthrough before freezing wording.
Browser-tool failure should lead to a reproducible owner walkthrough with the
unverified visual checks named. The predecessor's independent-reader assessment
remains open; automated checks do not establish that assessment.

## Decisions and completion boundary

P0 must establish the durable sources for recovery and the existing authority
to open and calculate. Track 0 must choose whether to reuse a matching saved
result or calculate afresh when its currency cannot be established, and name
any required new contract. P0 and R1 settled the first part: no existing
reader establishes that a saved result describes the current account, so
reuse as current is unsupported and a fresh calculation is the supported
route (R1 finding 2). Showing a saved result as current without a new
calculation would need a new checked relationship and is the owner's
decision. Each consequential decision should explain the
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

## Outcome

**What a person can now do.** A person can initialize a synthetic Cedar and
Birch account once, in a directory outside the repository, and correct a
borrowing's loan-cost answer through the existing correction page. They can
then stop the process. A new process opens the same directory without seeding
it. The opened page shows:

- each borrowing's current loan-cost answer and, where one exists, its
  earlier answer, named by the recorded correction;
- the latest earlier result, labelled as an earlier result. Inside it, each
  answer is labelled as what that calculation used, not as current;
- whether a calculation started and did not finish;
- one action: calculate from the saved answers.

Calculating saves no answer. Its result is headed as calculated from the saved
answers in this session. The existing correction interaction then continues
unchanged, and the next correction names the previous one as its
predecessor. Reopening again works the same way.

**What the session refuses or reports honestly:**

- **Initializing and opening.** Initializing refuses a directory that already
  holds an account. Opening refuses a directory without one and never writes
  to the log. The only file opening adds is a new build of the page.
- **Earlier results.** No result saved by an earlier process is presented
  as describing the current answers. The files do not establish that
  relationship, so the person calculates afresh. The earlier result is found
  by the last completed run record and the `runId` inside the presentation,
  never by filename or time. A missing file, two matching files, an
  unreadable neighbor and an unreadable record stream each have their own
  sentence, and the answers stay visible in every case. A presentation that
  parses but cannot be interpreted is reported as an earlier result whose
  explanation could not be read. That covers a reason it names that is
  missing, and rows that are not readable. None of that explanation is shown.
  The answers, their predecessors and the calculate action remain.
- **A lost calculate response.** If the session answers that it did not
  calculate, the page says so. If the answer never arrives or cannot be
  read, the page reads the session's state once. A calculated result the
  session holds is shown as this session's result, with no failure claim.
  Otherwise the page says it could not confirm the calculation and that the
  saved answers are unchanged. The page never sends another calculation on
  its own.
- **Old reviews.** A token from a stopped process is refused because it
  names another session. The page says it cannot determine whether that
  correction was saved, never "Not saved", and drops the token. Any
  correction the old process saved is already visible as the current answer.
- **Line 21.** A blocked line 21 is stated as blocked, not as "not
  calculated".
- **"Current".** The page never uses "current" for a result in ADR 0069's
  sense. These synthetic runs record `AUTHORIZATION_ABSENT`, and the page
  does not render it.

**What it is built from.**

- `packages/derivation/correction_session.py`: `CorrectionRuntime.initialize`
  and `open`, the opened state, the `calculate` route, session-bound tokens,
  and the earlier-result lookup over `RecordStream`.
- The existing page in `packages/sample_data/sli_correction_t1/`,
  regenerated as the same ADR 0049 surface artifact.
- The runner's persistent mode,
  `sli_correction_evaluation --workspace DIR [--init]`.

There is no new schema, fact type, ADR, durable store or calculation change.
The existing temporary-workspace states behave as before.

**Evidence.**

- `tests/test_sli_correction_resumption.py` has seventeen tests. They cover
  runtime, HTTP and real `SIGKILL` restarts. Four headless-Chrome paths go
  through the served page:
  - the reopened account;
  - a calculate response lost after the calculation finished;
  - an explicit refusal to calculate;
  - an earlier explanation that cannot be interpreted. Their deciding assertions read the log, records
  and outputs.
- R4 recorded the text of every screen of the walkthrough from the rendered
  page.
- The README part "Returning to a saved account" reproduces it.

The working charters, the P0 probe and the R1–R4 reviews were removed at
curation, and their conclusions are recorded above.

**Limits.**

- **Wording.** The wording is provisional, and the owner has the
  screen-by-screen walkthrough. The static note "This reviews one saved
  result" still shows on every screen. The predecessor's first-run heading,
  "Earlier result (line 21) — unchanged", is unchanged. No independent reader
  has assessed the interaction.
- **Synthetic only.** Accounts are synthetic only. A real workspace still
  needs the residency path and an owner decision.
- **No "same account" check.** Nothing checks that a directory is "the same
  account" beyond reading its log. The page never receives or chooses a
  location.
- **Unfinished calculations.** A calculation that did not finish is
  recognized only from a started record without a close. A failure before
  the run starts leaves no trace, and the page then simply offers
  calculation.
- **One process.** The session lock binds one process. Two processes serving
  the same directory at once are outside this milestone.

**Phase assessment (recommendation; the decision is the owner's).** The
previous two milestones met the phase's bounded exit. This milestone adds a
practical returning-user path for the same supported answer: the account, its
history and an honest calculation state survive a complete stop and restart,
and the correction continues. It needed no new mechanism beyond an opener, a
calculate action and session-bound tokens.

The foreman recommends **concluding Evolving Workspace Accounts** here. Three
items stay open:

- the owner's visual check and wording;
- an independent reader assessment;
- the real-workspace residency decision.

None of them needs another milestone in this phase. No further tax case is
proposed.
