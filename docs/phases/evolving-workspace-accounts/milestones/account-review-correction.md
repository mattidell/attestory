<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "account-review-correction",
  "retrospective": "docs/milestone-retrospectives/2026-10-09-account-review-correction.md",
  "status": "Closed 2026-10-09. A person can open a saved line 21 result, choose one borrowing's loan-cost answer, confirm a correction, save it through the reviewed recorder, and read the recalculated result beside the unchanged earlier one.",
  "scope": [
    "inspect the account behind line 21 and identify one existing borrowing answer",
    "confirm and persist a correction through the existing recording boundary",
    "recalculate and explain the change without altering the prior saved result"
  ],
  "non_goals": [
    "no new tax coverage or general assumption-management system",
    "no free text, expanded statement vocabulary or broad intake journey",
    "no automatic change to other answers to obtain a favorable result"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-09-account-review-correction.md",
      "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-overview.md",
      "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md",
      "docs/phases/evolving-workspace-accounts/milestones/account-review-correction.md"
    ],
    "implementation": [
      "docs/phases/evolving-workspace-accounts/milestones/account-review-correction.md",
      "docs/process/planning-and-development.md",
      "docs/adr/INDEX.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/evolving-workspace-accounts/milestones/account-review-correction.md",
      "docs/roles/qualitative-review.md",
      "docs/process/planning-and-development.md"
    ]
  }
}
-->

# Reviewing and Correcting the Account Behind a Result

Milestone key: `account-review-correction`.
Branch: `milestone/account-review-correction-student-loan`.

## Purpose

A person reads the explanation of their student-loan interest deduction and
notices an answer they gave incorrectly. They should be able to identify the
borrowing and the exact answer, review a correction, and see what changed
after saving it. They should not need to understand the application's input
methods, fact identifiers, or calculation rules to do this.

The previous milestone made the calculation tolerate different supported
input methods on different forms. This milestone makes one change to that
account accessible from the result. It is not another investigation of which
student-loan tax rules to implement.

Use one existing question: whether a named borrowing paid only for school
costs. Begin with already recorded synthetic forms, borrowings, relationships
and answers. The workflow corrects an existing answer; it does not import a
form, create a borrowing, allocate interest, or ask for new kinds of statements.
Keep the existing question's meaning and supported response choices.

Success means a bounded working interaction: inspect the result, recognize the
answer and borrowing, review and confirm the change, save it, recalculate, and
inspect the new result. Canceling changes nothing. The earlier saved result
continues to describe the earlier calculation.

## Starting evidence and what still needs checking

The starting line is the merged account-refinement milestone (PR #205):
`core-calculations` v42 and worksheet v5. Its plan's Outcome and Limits are
the capability account, not a promise of complete tax coverage.

- `packages/derivation/presentation_projection.py` builds the saved line 21
  account; `packages/presentation/pages/citation-walk.v1.html` renders it.
- `packages/tax/sli_relationship_review.py` provides
  `prepare_borrowing_answer_review` and `correct_borrowing_answer_review`.
  The correction takes an identified finding, borrowing, question, response
  and reviewed context. These functions are not evidence that a visible
  result-to-correction route already exists.
- `packages/tax/sli_relationship_recording.py` is the durable recording
  boundary. Inspect its consumer and revalidation paths before reusing it.
- `tests/test_sli_track1_combined_standing.py`,
  `tests/test_sli_track2_explanation.py`, and
  `tests/test_sli_track2_repair.py` preserve calculation and attribution
  expectations. Existing recording/review tests cover neighboring behavior.

No new schema, ADR, browser transport, or independent surface product is
selected by this plan. P0 must locate the actual entry surface and its
write/adoption boundary. Consult accepted ADRs 0051 and 0049 where that surface
relies on them, and the recording contracts the called APIs implement. Read
exact decision text before selecting a contract change. If the viable build
belongs on `main-ui`, report a bounded integration plan rather than merging
the two lines or quietly changing this milestone's base. This branch starts
on `origin/main`.

## Meaning that the interaction must preserve

The person corrects their answer, not the calculated deduction or an assumption.
Show the borrowing, question, current answer and proposed answer together.
Identification must survive repeated display labels. A form is an entry point
to the account; it is not necessarily the scope of the correction. If two
forms include the same borrowing, the shared answer can affect both. Explain
that relationship without promising a tax amount before recalculation.

An assumption or a read-only responsibility is not an editable answer merely
because it appears beside one. A saved result is historical evidence, not a
write authorization. Any edit launched from it must prepare against the current
workspace and check that the target answer and relevant recognition context
have not changed before saving. A stale interaction must not silently retarget,
overwrite a newer answer, or claim that the old result has become current.

Do not change another broad answer, inclusion, financing relationship, or
assumption to make the correction produce a favorable result. Preserve the
selected v42 policy, including its existing conservative blocks. If the new
answer makes the result blocked, explain that honestly; this milestone does
not resolve the underlying tax or product deferral.

## How the plan develops

### P0 — trace one concrete journey before choosing its implementation

Charter a small investigation. Start with the saved result of a supported
two-form case. Trace exactly how a person could reach and correct the loan-cost
answer for one borrowing, and identify the missing connection, if any.

Produce one short walkthrough and a source-to-save-to-result map. Separate
what the existing software executes from proposed controls and manually
supplied fixture setup. Trace subject identity, the finding being corrected,
currentness checks, save authority, persistence, recalculation and saved output.
Identify what a person would see at each step; do not substitute a function
inventory for the interaction.

Independently review that walkthrough and the plan's implementation boundary
before drafting a large design. Review concrete sections as they develop; a
finding about identity or currentness must update dependent sections. If the
complete interaction already exists, exercise and improve it rather than
building another one.

#### P0 result and R1 disposition

P0 traced the path on this line, and R1 reproduced its citations and runs. Its verdict
was READY WITH CORRECTIONS, and both corrections are adopted below.

What already works, by direct call:

- `correct_borrowing_answer_review` → `correct_borrowing_answer_durably`
  saves one borrowing's answer as a reviewed correction. The save is keyed by
  the borrowing's identity, never its label. It writes one batch or nothing,
  and it names its predecessor.
- One correction reaches every form that includes the borrowing. There is no
  form-local edit to build.
- Preparing a review writes nothing, so cancelling needs no write path.
- A superseded finding id, such as one read from an older saved result, is
  refused as a correction target.
- An unrelated new borrowing does not invalidate a prepared review.
- Each run writes its own result and presentation, and later runs leave
  earlier ones byte-identical.

What is missing is a set of connections, not a capability:

- from a displayed answer to the current borrowing and question that a review
  needs;
- from a person's confirmation to the review and save calls;
- from a successful save to a recalculation;
- from one saved result to another.

The saved citation-walk page and `live_session.py` are read-only. They serve
GET only and answer POST with 405. The only write-capable surface on `main` is
the W-2 entry loop, which is fixed to its one W-2 field.

`origin/main-ui` (283 behind, 23 ahead) extends the same W-2 pattern and has
nothing for this question. **No main-ui integration is needed.** The build
stays on `main`, and `main-ui` holds nothing this milestone would adopt.

R1 found two obligations the plan had not named. They are connected:

1. **Borrowing recognition.** Borrowing cards carry no recognition clues, so
   two borrowings with the same label refuse every selection. Neither one can
   be corrected through the review. Whether that refusal is right or needless
   depends on whether existing relationships (inclusion on a form, financing
   of a schooling) can be shown as clues. They are not new statements.
2. **Relationship context.** Neither currentness layer reads inclusion or
   financing. Withdrawing the borrowing's inclusion on Cedar after the review
   was prepared still lets the save succeed.

The answer is about the borrowing, so the save may still be right. But if the
person recognized the borrowing by the forms it belongs to, or confirmed an
effect on named forms, that context is now stale. The choice of recognition
clues therefore determines which context changes must invalidate a confirmation.

P1 and Track 0 decide these two obligations together.

### P1 — demonstrate the consequential seam, then select the build

Prefer direct reuse where the contract and consumer are settled. If connecting
the displayed answer to the recorder is uncertain, run one bounded executable
spike through the real save boundary and recalculation, together with the
displayed confirmation and resulting explanation. A hand-built model proves
layout only; it cannot prove correct recording or recovery.

The P1 spike ran the four missing connections through the real save boundary and
`live_coordinate_run`, measures the recognition and context obligations
above, and stated the contract cost of each candidate home for the
confirmation.

Use rival prototypes only if the P0 review identifies materially different
options whose consequences a concrete case can distinguish. Do not launch
rivals merely to compare wording. Review any needed contract before code
depends on it. The foreman may revise the track split from this evidence.

### Track 0 — readiness for implementation

SETTLED; see "Track 0 adversarial closure" below. P1
ran all four missing connections through the real
save boundary and `live_coordinate_run`. R2
reviewed the selection. T0b ran the six claims
R2 found asserted rather than run. No schema, fact type, statement kind or
v42 change is needed.

**Selected interaction.**

1. **Where it opens.** The person opens a correction session on one saved
   result.
   - The session reads that run's saved presentation. It does not modify the
     run, and does not use the run as write authority.
   - It shows the line 21 rows, and for each borrowing's loan-cost answer, a
     "review this answer" choice. Answers appear in both row shapes the saved
     model uses: `account.said.current` on blocked rows, and `basis.answers`
     on supported rows (P1 part 1).
   - The same finding shown on two forms is one choice, not two.
   - The read-only citation-walk page and its viewing session do not change.
2. **Choosing an answer resolves it against the current workspace.** The
   saved file contributes only the finding id. A resolver reads the current
   log and returns one of four outcomes:
   - **current:** the review proceeds;
   - **superseded:** the page says the answer has since changed, shows the
     current answer, and offers a review of that answer instead;
   - **no target:** the answer was withdrawn, so there is nothing to correct;
   - **not a target:** box witnesses, assumptions and other questions.

   The supported question stays fixed to loan cost.
3. **The confirmation.** It shows:
   - the borrowing's label;
   - recognition clues taken from relationships already recorded: each form
     whose inclusion of the borrowing is current, with whether it was affirmed
     or denied, and the schooling the borrowing financed;
   - the question;
   - the current answer and the proposed answer;
   - the forms whose current account uses this answer;
   - a statement that the effect is known only after recalculation.

   The clues go into the borrowing card of the borrowing-answer review only.
   They come from a new card builder used by `prepare_borrowing_answer_review`.
   `_borrowing_cards` is shared with `prepare_review`, so it is not edited,
   and `prepare_review`'s cards are unchanged (R2 finding 5). Two borrowings with
   identical labels and identical relationships still refuse; that refusal
   is correct.
4. **Currentness: the as-shown rule.** Because the clues are part of the
   prepared card, the existing revalidation, which compares the prepared
   cards with a fresh read, refuses the save when something shown has
   changed:
   - an inclusion was withdrawn or newly affirmed;
   - the financing changed;
   - the borrowing's identity ended.

   The recorder still refuses a superseded predecessor. Unrelated borrowings
   and other answers do not refuse (P1 part 3, cases 6 and 7). A refused save
   writes nothing, and the session offers a fresh review.
5. **Save, then recalculate.** Confirming calls
   `correct_borrowing_answer_review` with the session's own prepared review.
   That is the reviewed path, `correct_borrowing_answer_durably`, which
   already writes through `apply_contribution_batch`. The session then calls
   `live_coordinate_run` under an output name derived from the new
   successor finding, so the earlier run's name cannot collide (R2 finding 3). The person sees one of
   three outcomes, and each names what is true:
   - **saved and calculated:** the new line 21 rows for each affected form,
     the corrected answer as current with its predecessor in history, and
     the earlier result still available, unchanged;
   - **saved, not calculated:** "your correction was saved; the result could
     not be calculated", with a retry that only runs and never saves again
     (P1 part 5);
   - **not saved:** what changed, and nothing written.
6. **Cancel** discards the prepared review. Nothing is written.

**Home: H4, settled by R2.** Three
candidates were considered:

- **H1**, a write route on the viewing session, is ruled out. ADR 0047's
  amendment admits GET only. ADR 0048 Decision 2 leaves extending that
  session type out of scope.
- **H3**, a page served directly from the repository, is not consistent with
  the precedent it cites. The only write-capable precedent, the entry loop,
  obtains its page through the ADR 0049 surface-artifact route. Serving
  directly from the repository is the read-only citation walk's precedent
  only.
- **H4** is selected.

H4 is a separate local correction session on the entry-loop pattern. Its one
static page is delivered as an ADR 0049 surface artifact:

- a manifest with one entry;
- `entrypoint_html` naming that entry;
- a no-op `build_command`;
- one `surface-adoption` act and its registry entry.

`resolve_surface_artifact` never runs the command. `build_entry_surface`
copies the verified entries before running it. The page therefore needs no
Node and no new ADR or schema. Its write authority is the reviewed recorder
call through `apply_contribution_batch`, as ADR 0048 Decision 2 and ADR 0051
require. ADR 0046's redaction rules and ADR 0051's validated admission and
redacted failure apply to the session.

**T0b: closing the asserted rows.** T0b demonstrated all six claims:

- **The empty return.** No choices appear, and v42's result is unchanged.
- **Deduplication.** One finding shown on two forms is one choice, with both
  forms listed. Two borrowings with the same label stay two choices.
- **The as-shown rule with clue-bearing cards.** P1 cases 1 to 5 now refuse
  without writing, and cases 6 and 7 save. Duplicate labels with different
  relationships become distinguishable. Identical relationships still refuse.
  The saved `choices_shown` carries the clues and validates against
  `evidence.v1`.
- **D1 with an inclusion denial.** The result goes from 2500 to blocked and
  back to 2500. Spring's findings keep their identities.
- **A recalculation refusal after a valid save** (`ADOPTION_NONE_CURRENT`
  under a stale workspace revision). The correction is durable, no output is
  written, and a run with no second save recovers it.
- **The H4 rehearsal.** Resolution and the no-op build succeed, the served
  bytes equal the entry, and no Node, schema or ADR is needed.

Three implementation consequences follow from T0b:

- **Where the clues go.** They must be added in
  `_prepare_borrowing_answer_review_from_contents`, because the revalidation
  calls that function directly. They cannot go in the public wrapper alone,
  and they cannot go in the shared `_borrowing_cards`.
- **Entry-loop reuse.** `resolve_surface_artifact` and the loopback server
  classes are reusable. The entry loop's resolve, build and seed functions are
  hard-wired to the W-2 fixture, so they need parallel functions for this
  fixture rather than edits.
- **Neighbor display.** When a row's standing changes, a neighbor's
  "recorded, not used" entries can leave that row's display while the
  neighbor's own findings are untouched. The explanation must not imply that
  the neighbor's record changed.

The failure trigger is a caller-supplied stale revision. That is a real
refusal path, but a careful session would not reach it. The reporting
behavior is independent of the trigger, so Track 2 tests it through this
path or an equivalent refusal.

**Six artifacts (rows marked *target* describe Track 1 behavior, demonstrated by T0b's in-memory patch).**

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| Loan-cost answer finding | The person says this borrowing paid only for school costs (yes / no / cannot tell) | One borrowing, every form that includes it | The person's reviewed act; the borrowing entity | A later correction or withdrawal of the same borrowing and question; the end of the borrowing entity |
| Prepared correction review (*target*) | What the person was shown: card, clues, current answer | One session, one borrowing | A fresh read of the label, inclusion and financing; the current answer | Any change to a shown clue; supersession of the target; the end of the session |
| Displayed finding id in a saved result | What this run used | That run only; **never** write authority | The run's saved presentation | Nothing; it is history. The resolver maps it to current state |
| Recalculated result | Line 21 under v42 for the current answers | The return | Every current answer; the adopted release | Any later answer; never edited in place |
| Inclusion and financing facts | Which forms include, and what was financed | Read-only here | Their own acts | Their own corrections, which make the prepared review stale |

- **Empty or nonempty:**
  - With no borrowing, or no loan-cost answer, there are no choices; the
    session shows the result and offers nothing to correct.
  - A withdrawn answer gives no target.
  - A current answer is correctable.
  - A superseded answer resolves to the current one.
  - Neighbors: line 21's computation and the v42 standings are unchanged in
    every state, and only the person's answer moves them.
- **Late change:** prepare → change → save, for each of P1's seven changes,
  plus save → later correction → open the older result. P1 part 3 ran the
  first set and part 6 the last. Under the as-shown rule, the expected refusals
  are cases 1 to 5, and cases 6 and 7 save.
- **Claim reuse:** the displayed `findingId` and the recorder's predecessor
  are the same finding: the same proposition, the same identity
  (`fact.keys.borrowing`) and the same borrowing-wide scope (P1 parts 1 and
  4). The explanation must say that the correction reaches every form that
  includes the borrowing (the shared-borrowing case).
- **Neighbor diff:** the following are untouched:
  - `prepare_review` and its statement and schooling flows;
  - the W-2 entry loop;
  - the viewing session;
  - v42 content.

  New prerequisites on neighbors: none.
- **Integration surface:** a new consumer binds the saved model's
  `findingId` in `said.current` and in `basis.answers`. Cardinality: one
  finding per item, possibly repeated across rows, deduplicated by id. The
  built evidence is P1's runs. A model for each outcome path (current,
  superseded, no target, not a target; saved and calculated, saved and not
  calculated, refused) is required before closure.

### Implementation units

1. **Track 1 — the correction session, integrated early.** Build:
   - the resolver;
   - the clue-bearing borrowing-answer card;
   - the session's prepare, confirm, cancel, save and recalculate handlers;
   - one page, delivered as one surface-artifact manifest and adoption.

   All through the existing recorder call and `live_coordinate_run`, with no
   parallel write path. Stop at the first working example: two forms, one
   correction, one recalculation, rendered. Get an integrated review of it,
   and show the owner the interaction before the wording is frozen.

   **Status: complete.** After the first build:
   - the owner's integrated review found four defects;
   - the repair (R3) found four more corrections;
   - the Foreman found the explanation incomplete and brought it to parity
     with the citation walk;
   - R4 found three more corrections.

   All were folded into Track 1. The interaction shown to the owner
   is the runner's base state:
   - Cedar and Birch;
   - a yes → no correction on Cedar;
   - Cedar blocked, with its reason named;
   - the predecessor answer in history;
   - Birch and the earlier result unchanged.

   Three kinds of evidence back it:
   - **backend:** `CorrectionRuntime` tests;
   - **transport:** HTTP tests;
   - **visible interaction:** four headless-Chrome paths.

   The owner's visual check and any independent reader's check are still
   open.
2. **Track 2 — complete the cases and the wording.** Add:
   - stale and refused saves;
   - saved but not calculated, with its retry;
   - historical results;
   - duplicate labels and the shared borrowing.

   Add the owner's wording changes and the regression tests. Combine Track 2
   with Track 1 if splitting them would hide the seam.

   **Status: complete.** The runner offers six named synthetic states:
   base, D1, shared, duplicate labels, blocked and historical. They are
   generated as committed fixtures. Track 2 also built:
   - a retry that only recalculates and never saves;
   - historical review that targets the current answer;
   - duplicate-label clues on the choices;
   - the no → yes direction.

   Each case has backend, transport and page evidence. R5 found three low
   corrections, which were applied:
   - drive the retry through a real refusal;
   - make the D1 walkthrough match the page;
   - make the generator independent of the tests.

   The owner has not yet given wording changes, so the wording is still
   provisional.

Independently review the first integrated workflow and the final curated
candidate. Use the normal lean loop within each unit. No additional unit is
automatic; return a concrete scope/cost decision if a general surface platform
or new engine semantics becomes necessary.

## Track 0 adversarial closure

Applied by the Foreman under `docs/roles/qualitative-review.md`, from R2 and
T0b. It covers only the correction interaction. The calculation's own
closure is the predecessor's.

- **Authority-lifecycle table: PASS.** See the five rows under Track 0. The
  rows that decide the result:
  - A saved run's displayed finding is history, never write authority.
    P1's resolver showed it, and T0b reused that resolver. A superseded id is
    refused as a target, and an older result resolves to the current answer.
  - The prepared review is invalidated by every displayed clue change. T0b
    cases 2 to 4 now refuse, with the log revision unchanged.
- **Empty/nonempty authority matrix: PASS.** The no-borrowing and no-answer
  returns give no choices, and v42's result is unchanged (T0b claim 1). A
  withdrawn answer is "no target", and a current answer is correctable
  (P1 part 1). Calculation states are v42's own, untouched.
- **Late-member lifecycle: PASS.** The trace is prepare → change → save, over
  seven changes (T0b claim 3), then save → later correction → open the older
  result (P1 part 6). There is no aggregate declaration: the correction
  summarizes no family. A newly affirmed inclusion makes a prepared review
  stale (case 3) instead of silently widening its effect.
- **Neighboring capability dependency diff: PASS.** `prepare_review` and its
  cards, the W-2 entry loop, the viewing session, the citation-walk page and
  v42 content gain no prerequisite. The clue builder sits on the
  borrowing-answer path only (T0b claim 3). One neighbor effect is
  documented: the display of another borrowing's entries in "recorded, not
  used" (T0b claim 4).
- **Reused-claim semantic/lifecycle equivalence: PASS.** The displayed
  `findingId` and the recorder's predecessor are one finding. They share the
  proposition, the identity (`fact.keys.borrowing`) and the borrowing-wide
  scope (P1 parts 1 and 4, and T0b claims 2 and 4). The confirmation names
  every form the answer reaches.
- **Integration surface: PASS.** The consumer is the correction session,
  binding `findingId` in `account.said.current` and in `basis.answers`. It
  expects one finding per item, possibly repeated across rows, and
  deduplicates by id (T0b claim 2). Models were built for every path:
  - current, superseded, no target and not a target (P1 part 1);
  - saved and calculated, and refused (T0b claims 3 and 4);
  - saved but not calculated (T0b claim 5).

  No form field or new published symbol is produced.
- **Known limitations affecting correctness: none.** Two limitations are
  recorded instead:
  - The failure trigger used is a stale revision, which affects only the
    test's realism, not the behavior.
  - The surface's real browser behavior is unverified until the owner's
    walkthrough.
  - This closure rests on prototype evidence; see "Track 1 integrated review
    and repairs" for the claims the integrated session must re-establish.

## Track 1 integrated review and repairs

The owner's independent review of the first integrated session found that
four Track 0 claims held in prototype evidence but not in the session.

**What the prototype showed, and what the session lost:**

1. **Distinguishability.** T0b's duplicate-label cases prepared a review that
   showed both borrowings, so the existing check compared them.
   `CorrectionRuntime.choose` prepares a review of the selected borrowing
   only. Two borrowings with identical labels and relationships then produce
   identical confirmations, and the save succeeds. The safeguard depended on
   the caller's inputs, and the caller narrowed them. An opaque id is an
   address for the action. It is not a clue a person can recognize.
2. **Financing outcome.** P1 and T0b recorded each relationship's outcome.
   The production formatter renders every financing outcome (affirmed,
   denied, withdrawn, unresolved) as "financed …". The page loses that
   meaning, and so does the retained review context. Because the prepared and
   refreshed labels are equal, a financing withdrawal after prepare saves.
   T0b case 4 therefore holds only in the prototype.
3. **Failure reporting.** P1 and T0b distinguished a recorded correction from
   a calculated result at the runtime. The page treats a failed or missing
   response as "nothing changed", which the session cannot know.
4. **The explanation.** The first example's page shows a form label and an
   internal standing code. It does not show the saved answer, the correction,
   the support or block explanation already in the model, or which result is
   historical and which is new.

**Status of the readiness claims.** The as-shown rule, distinguishability
and the honest save outcomes are demonstrated as **prototype evidence**
(P1 and T0b). They are **not yet established for the integrated session**.
The repair must demonstrate them through `CorrectionRuntime`, the HTTP API
and the page. The three kinds of evidence stay separate:

- backend;
- transport;
- the visible interaction.

R3 reproduced all four repairs through the
runtime, including in cases the suite does not run, and returned READY WITH
CORRECTIONS. Its corrections were:

- labels compared as displayed, not as stored;
- the full committed test matrix for relationship meaning;
- the three browser paths not yet driven;
- shared initial live runs.

The Foreman added one more: borrowing attribution resolved by identity
through the runtime, replacing the page's rule of attributing answers only
when a form has exactly one loan.

The corrections landed, and all four browser paths
ran. In the Foreman's check of the running session, defect 4 was only partly
repaired:

- headings showed standing codes;
- relationship answers showed raw codes;
- a blocked form said its reason was "named above" without naming it;
- the assumed, left-with-you and recorded-not-used groups were absent.

The saved citation walk already renders all of these from the same model.
A parity unit brought the correction page into line with it, using the
citation walk's existing wording. R4 then found three corrections:
unredacted refusal text (ADR 0051), relationship answers left unattributed,
and the missing box 1 amount line. They were applied.

**The rule the repair applies.** For a safeguard demonstrated by a helper,
trace the connection to the caller: check that the caller still supplies the
inputs that make the safeguard work. For information the backend retains,
trace the connection to the page: check that the page still shows it.

## Bounded cases and verification

Use only existing normalized inputs and synthetic `demo.*` identities.

| Case | What must be learned or preserved |
| --- | --- |
| Correct one borrowing's loan-cost answer on Cedar; Birch uses an unrelated borrowing or older answer | The intended answer changes, other answers remain current, and the adopted calculation is rerun |
| Correct yes to no and no to yes in suitable existing fixtures | Neither favorable nor blocked output is the interaction's goal; the result follows the recorded answer and existing rules |
| Two borrowings share a display label; one is denied for the form | Recognition and save target use identity, not labels or a form-wide flag |
| Two forms affirm the same borrowing | One correction reaches both real dependents and does not masquerade as a form-local edit |
| The target answer or relevant schooling/relationship context changes after review preparation | Save does not overwrite or silently reinterpret a stale confirmation |
| Cancel; then reopen an older saved result after a later successful correction | Cancel writes nothing; historical output stays historical; a new edit starts from current state |
| An assumption or responsibility appears beside the answer | The surface does not offer it as an editable user assertion |
| The correction saves, then recalculation fails or refuses | The confirmation reports a recorded correction without a calculated result; the earlier saved result is not presented as current |

Observe the saved acts, exact target and predecessor, current findings, run
results and reloaded presentation. A UI success message alone proves none of
these. Do not require a return-wide numeric change when caps or another
blocking condition legitimately mask one; inspect the affected publications.
Failure tests should demonstrate a wrong target, stale overwrite or misleading
attribution being caught. Preserve the existing supported and conservative
outcomes rather than duplicating the predecessor's entire case matrix.

Show the owner the bounded interaction before freezing wording. Invite an
independent reader who has not authored it to identify the borrowing, answer,
proposed change and result from the visible material. Their comprehension is
qualitative evidence, not a numerical score or proof of layperson usability.
Do not claim this happened if only automated assertions ran. If browser tools
fail, stop troubleshooting and provide a reproducible synthetic walkthrough
for owner inspection, naming which visual/interaction checks remain unverified.

Use the repository's test lanes, data scan, diff checks and final CI. Keep
scratch outputs ignored; no personal records or private workspaces are needed.

## Open decisions and stopping boundary

- **Where the edit lives:** decide after P0 traces the existing surface and
  its authority boundary, before implementation. Do not assume the saved
  citation-walk page should itself gain write authority.
- **How a historical result opens a current review:** establish the identity
  and refresh behavior at Track 0. Avoid both silent retargeting and needless
  refusal caused only by an unrelated workspace change; inspect the existing
  contract rather than weakening it by convenience.
- **What happens after a successful save if the run cannot complete:** the
  confirmation must distinguish a recorded correction from a calculated
  result. Decide the bounded recovery/reporting behavior before integration.

Completion is one integrated, durable correction workflow and an honest
account of its evidence and limits. Do not add more questions, new tax rules,
interest allocation, institutional checking, automatic assumption replacement,
free text, or a complete intake/navigation system.

The previous milestone already demonstrated the phase's core calculation
transition. This milestone is a deliberate additional interaction boundary,
not a claim that phase exit requires every future capability. At closeout
recommend whether to conclude Evolving Workspace Accounts; do not automatically
propose another vertical. Preserve unresolved questions with a concrete future
consumer, not a backlog of every combination imaginable.

## Outcome

**What a person can now do.** A person can:

- open a correction session on a saved line 21 result;
- choose one borrowing's loan-cost answer;
- read a confirmation that shows:
  - the borrowing, with clues from relationships already recorded;
  - the question;
  - the current answer and the proposed one;
  - the forms whose account uses that answer;
- confirm.

The correction is saved through the existing reviewed recorder call, and the
return is recalculated under v42. The page shows the new explanation for
each affected form beside the earlier result, which does not change. The
explanation uses the citation walk's model and wording: the reason a form is
blocked, what was said (current and history), what was used, what was
assumed, what is left with the person, and what was recorded but not used.
Cancelling writes nothing.

**What the session refuses or reports honestly:**

- **Look-alike borrowings.** A borrowing that would look identical to another
  current borrowing is refused. The comparison uses labels as displayed, so
  whitespace differences do not make borrowings distinguishable.
- **A changed display.** If anything the confirmation displayed has changed
  by the time of saving, nothing is saved: an inclusion, a financing outcome,
  a label, or the borrowing itself.
- **Failure after the save.** A failure after the durable save is reported as
  saved but not calculated, and a retry only recalculates.
- **A lost confirmation response.** The page asks the session for the outcome
  of that same correction, identified by its own review token. That token
  survives a refresh of the tab. The page then shows one of four things:
  - the new result, if the correction was saved and calculated;
  - "saved, not calculated", with "Calculate again", if the calculation did
    not finish;
  - "not saved", if nothing was saved. This includes a review whose
    confirmation never arrived; that review is closed so a late confirmation
    cannot save.
  - that the outcome is unknown, if the session cannot tell.

  The page never substitutes another correction's outcome and never
  resubmits. "Calculate again" recalculates only for its own correction, and
  is refused once a later correction has replaced that one. The earlier
  result stays unchanged throughout.
- **Refusal wording.** Refusals use fixed sentences and never echo exception
  text.
- **Earlier results.** A saved result is never write authority. An earlier
  result is labelled as not current. A superseded answer leads to a review of
  the current answer, and a withdrawn one has nothing to correct.

**What it is built from.**

- `packages/derivation/correction_session.py`: the runtime and the loopback
  session.
- `packages/sample_data/sli_correction_t1/`: one page delivered as an
  ADR 0049 surface artifact with a no-op build. It needs no Node.
- `tools/generate_sli_correction_t1_fixtures.py` and the runner
  `packages/derivation/runners/sli_correction_evaluation.py --state …`.
- In `packages/tax/sli_relationship_review.py`: clue-bearing
  borrowing-answer cards, and distinguishability across the whole workspace.

There is no new schema, fact type, statement kind, ADR or calculation
change.

**Evidence.** Three kinds back the result:

- runtime tests;
- HTTP tests;
- headless-Chrome tests of the served page, covering fourteen paths across the
  six states.

The README walkthrough lets the owner reproduce each state. The working
charters, probes and interim reviews were removed at curation. They were P0,
P1, T0b, R1–R5 and the Track 1 and Track 2 correction charters, and their
conclusions are recorded above.

**Limits.**

- **Wording.** The wording is provisional. The owner has the walkthrough but
  has not yet reviewed the interaction visually, and no independent reader
  has assessed it.
- **Copied wording.** The explanation's wording is copied from the citation
  walk, because each page is a self-contained artifact. A wording change
  must be made in both pages.
- **Synthetic only.** The session works on synthetic workspaces only, like
  the W-2 entry loop. Using a real workspace needs the residency path and an
  owner decision.
- **Identical pairs.** The refusal does not say which clue two identical
  borrowings share.
- **One question.** Only the loan-cost question is offered. The others are
  outside the selected scope.

**Phase assessment (recommendation; the decision is the owner's).** The
phase's provisional exit goals asked for three things:

- one production transition that preserves the person's account while
  changing its use;
- tests that distinguish detail, correction, adverse and unresolved
  information;
- a saved explanation that separates what was said, used and assumed before
  and after the change.

The previous milestone delivered the calculation transition and the
explanation. This milestone adds the interaction that makes a correction
reachable from the result. The interaction lets a person correct one
answer, keeps that answer's history, and shows what changed, without exposing
input methods. Whether a reader who has not seen the engine understands it
has not yet been assessed.

The foreman recommends **concluding Evolving Workspace Accounts** at this
bounded result. Two items stay open: the owner's visual check, with any
wording changes, and an independent reader assessment. Neither requires
another milestone in this phase. No further tax vertical is proposed.
