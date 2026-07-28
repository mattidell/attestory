<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-real-session-attestation",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-07-27-presentation-real-session-attestation.md",
  "status": "CLOSED 2026-07-27. Presentation moves L2 to L3 in the W-2 wages (1a) column ONLY — the first maturity lift for the Presentation row and the first time this project's human surface ran on the owner's real data. Track 1 (agent-built, five cycles) was chartered as documentation and found three real code defects the previous milestone's rehearsal missed, because that rehearsal drove the happy path and three designed refusals and none of these three sit on it: LiveViewingError was a sibling rather than a subclass of PresentationSessionError so a third of the reason-code table arrived as an uncaught traceback; teardown's except was too narrow for its own promised code to be reachable; and Ctrl-C left an orphaned headed browser displaying the real return plus a .live-view/session-* directory holding that render's profile and disk cache, outliving a preflight guarantee that binds only at session start. All three were fixed structurally — in open_presentation_session, in launch, and by making the session a context manager — NOT in the runbook template, because a guarantee living only in a copyable example silently no-ops when adapted; that is this project's fail-open drift class, now named three times. Track 2 (owner-operated) launched a real headed browser through the real path against a SYNTHETIC workspace and rendered the PRODUCT page: clean pass, no page defects, first human confirmation of the interrupt-teardown repair. Its purpose was structural rather than cautious — the owner's attestation is non-descriptive, so a defect seen during the real session arrives unactionable, and Track 2 exists so the first real render is not also the real session. Track 3 (owner-operated) performed the real session and the ADR-0031 Decision 7 attestation with all five ADR-0047 preconditions affirmed individually, conditions 3 and 4 being owner knowledge. Named gaps at close: the classified-refusal path has NO human confirmation (Track 2's browser-start-failure exercise was skipped, charter-permitted); the runbook has an unidentified unclarity reported by its first human user, carried open rather than closed by guesswork; the other four Presentation cells stay L2 because one attestation raises only what it covers, and nothing technical separates them — the record does. PLANNED 2026-07-27. Three tracks. The milestone that finally performs the act every prior Presentation milestone deliberately deferred: one real viewing session against the owner's real residency, and the ADR-0031 Decision 7 non-descriptive attestation that follows it. Track 1 is the only agent-built track — a session runbook and a bounded non-descriptive failure vocabulary, because a session that goes wrong must be reportable without breaching ADR-0047 precondition 5. Tracks 2 and 3 are owner-operated on the owner's machine: Track 2 closes the two rehearsal gaps by launching a real headed browser and rendering the product page against a synthetic workspace, and Track 3 performs the real session. Target is Presentation L2 to L3 in the W-2 wages (1a) column only; the other four Presentation cells stay L2 by design.",
  "scope": [
    "build a session runbook the owner follows in one sitting, and any scriptability repair needed so the session is one command rather than an assembled sequence",
    "define a bounded non-descriptive failure vocabulary that lets the owner report a mechanical session failure without naming a value, identifier, or disposition",
    "close both rehearsal gaps by launching a real headed browser through open_presentation_session and rendering the product page with it, against a synthetic workspace",
    "perform one real viewing session against the real residency and record the ADR-0031 Decision 7 non-descriptive attestation with each ADR-0047 precondition affirmed",
    "raise Presentation from L2 to L3 in the W-2 wages (1a) column, with a footnote in the footnote-7/11 evidential pattern"
  ],
  "non_goals": [
    "no Presentation L3 claim in the Interest, Dividends, Return-level conditions, or Schedule attachments columns — one session raises only what its attestation covers",
    "no confinement code, sandbox profile, wrapper, or probe implementation; Class C confinement and Class D precondition observation remain owner-held outside the supply chain (ADR-0047, amendment 1)",
    "no data-boundary maturity movement; that row's L3 ceiling is ratified and permanent (ADR-0044 line 164)",
    "no descriptive detail of the session anywhere — no value, identifier, disposition, screenshot, residency locator, path fragment, canonicalized form, or derived identifier in the repository, a review, a PR, chat, or the retrospective",
    "no change to the browser evaluation harness, its two manifests, or tools/presentation_harness/lib/server.mjs; they are a byte-unchanged regression floor",
    "no new presentation surfaces, forms, or schedules — breadth stays deferred until one surface is proven on real data",
    "no new tax rule, form field, citation, schedule, domain, published schema, or citizen",
    "no change to ADR-0031, ADR-0044, or ADR-0046"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/real-return/milestones/presentation-real-session-attestation.md",
      "docs/adr/0047-live-viewing-environment.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "packages/derivation/live_session.py",
      "packages/derivation/live_viewing.py",
      "packages/presentation/pages/citation-walk.v1.html",
      "docs/reviews/2026-07-27-presentation-live-session-path-track3-rehearsal.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/real-return/milestones/presentation-real-session-attestation.md",
      "docs/adr/0047-live-viewing-environment.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "packages/derivation/live_session.py",
      "docs/phases/real-return/maturity-matrix.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phases/real-return/milestones/presentation-real-session-attestation.md"
    ]
  }
}
-->

# Milestone: Presentation — Real Session and Attestation

Audience: Product (planning instrument); Shared (status)

Phase: Real Return. Selected by the owner 2026-07-27 from frontier 1 of
`docs/phases/real-return/maturity-matrix.md`.

## Objective

Move **Presentation from L2 to L3 in the W-2 wages (1a) column** by performing
the act the matrix says is the whole remaining distance: a real viewing session
against the owner's real residency, followed by the ADR-0031 Decision 7
non-descriptive attestation.

Every prior Presentation milestone deferred this deliberately. Live Viewing
Boundary decided the environment. Live Session Path built the vehicle and
rehearsed it. Neither could raise the row, because the row is defined by real
operation and nothing a repository does to itself can substitute for it.

## Current state

The matrix (footnote 5) and the Live Session Path retrospective agree there is
**no build gap**. `open_presentation_session` runs capability → preflight →
model → loopback → confined browser → teardown as one act, refuses on every
preflight refusal, takes preflight answers as injected parameters rather than
observing the machine, and has been rehearsed end to end against a synthetic
workspace.

Two rehearsal gaps stand between that and the real session, both recorded
honestly by the milestone that created them:

1. **No real browser has ever been launched by this path.** Every existing
   exercise stopped short of a headed process.
2. **The product page has never been rendered by one.** It is a three-text-change
   copy of the evaluation fixture page; only a normalized diff and a
   `node --check` stand behind it.

Neither is a blocker. Both mean that, left alone, the first real session would
also be the first real render.

## The hazard this arrangement avoids

The owner's attestation is **non-descriptive** by ratified design: it asserts
that the capability operated, never what it showed. That constraint has a
consequence the plan must handle rather than discover.

**If the session renders something wrong, the owner cannot describe it.**
ADR-0047 precondition 5 forbids values, identifiers, dispositions, screenshots,
and the locator from chat, reviews, PRs, and the repository. A defect found
during the real session is therefore, by default, unactionable — the person who
saw it is the one person forbidden from saying what it was.

Two responses, sequenced:

- **Make the first real render not be the real session.** Track 2 launches a
  real browser and renders the real product page against a *synthetic*
  workspace, where anything found is fully describable and fully fixable. This
  is where render defects are supposed to be caught.
- **Bound what remains.** Track 1 defines a failure vocabulary that is
  **mechanical, never evaluative** — it can carry "a section failed to render",
  "a citation link resolved to nothing", "the page did not load", "teardown did
  not complete". It cannot carry "the wrong amount appeared" or anything else
  that names a value or a disposition. That distinction is the vocabulary's
  entire design problem, and getting it loose is a boundary breach, not a
  usability improvement.

This is the same shape as the Live Session Path findings: correct components,
defective join. That milestone's plan asked for a composition it had not thought
through. This section is the attempt not to repeat it.

## Milestone stages

1. **Track 1 — session runbook and failure vocabulary.** Agent-built.
2. **Track 2 — real-browser rehearsal on a synthetic workspace.** Owner-operated.
3. **Track 3 — real session, attestation, and records.** Owner-operated, then
   foreman.

Tracks 2 and 3 are expected to run in **one owner sitting**, with a hard gate
between them: Track 2's outcome is recorded, and the real session does not begin
if the rehearsal did not cleanly pass. Both browser launches happen on the
owner's machine; no agent launches a headed process.

## Scope

As the capsule's `scope`. Two restatements:

**Track 1's scriptability repair is bounded.** If the session already runs as one
call, Track 1 writes a runbook and nothing else. Any code change must be
justified by the owner sitting being materially harder without it — not by
general tidiness. `server.mjs` and both evaluation manifests are byte-unchanged;
if a clean implementation appears to require touching them, stop and report.

**The vocabulary is a contract, not a convenience.** It is the only channel from
a failed real session back to a repair, so it is reviewed against ADR-0047
precondition 5 as a data-safety artifact, not as documentation.

## Non-goals

As the capsule's `non_goals`. Three worth restating in prose:

- **Only the W-2 column moves.** The owner named W-2 wages (1a) at plan stage.
  The other four Presentation cells stay L2. If the session's attestation
  covers additional columns, the owner may name those columns at attestation
  time — naming a column is not describing content — but the plan does not
  assume it and the exit criteria do not require it.
- **No confinement code and no probes.** Unchanged from the previous milestone
  and for the same reason: boundary enforcement is not authored by the supply
  chain it constrains. `PreflightProbes` stays an injected input. The owner
  applies their own confinement if they choose to.
- **No repository claim about what was seen.** L3 asserts the capability
  operated. It does not assert any disposition was correct, and the footnote
  must not drift into implying it did.

## Verification

```text
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_presentation_l2_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

Both evaluation manifests are an unchanged regression floor throughout.

Tracks 2 and 3 are not verified by the suite. Their verification is the owner's
record: Track 2 a rehearsal record describing a synthetic run in full detail,
Track 3 an attestation describing nothing.

## Data safety

**This is the first milestone in which the presentation path touches real data.**
The standing rules apply with no relaxation:

- No absolute local path, residency locator, path fragment, canonicalized form,
  or derived identifier in Git, a review, a PR body, a commit message, or chat.
- Track 1 and Track 2 use synthetic inputs and temporary workspaces only.
- Track 3's real session produces exactly one repository-eligible statement: the
  non-descriptive attestation. Nothing else from it is recordable.
- No screenshot of the real session is taken, retained, or referenced.
- ADR-0047 precondition 3 binds the owner during the session: no paste outside
  the residency, no print to a networked or external destination, no retained
  screenshot, and **no copy at all while clipboard-history retention is in
  force**, since a retained copy leaves the residency with no subsequent paste.

## Exit criteria

1. A session runbook exists that the owner can follow start to finish in one
   sitting, and a non-descriptive failure vocabulary exists that is mechanical
   rather than evaluative, reviewed as a data-safety artifact against ADR-0047
   precondition 5.
2. A real headed browser has been launched by `open_presentation_session`
   against a synthetic workspace, has rendered the **product** page, and the
   result is recorded — closing both rehearsal gaps named in matrix footnote 5
   and in the Live Session Path retrospective.
3. The owner has performed one real viewing session against the real residency
   and recorded the ADR-0031 Decision 7 non-descriptive attestation, with each
   of ADR-0047's five preconditions affirmed, conditions 3 and 4 being owner
   knowledge.
4. The maturity matrix shows **Presentation / W-2 wages (1a) at L3**, with a new
   footnote in the footnote-7/11 evidential pattern: the synthetic battery
   exercised the identical path in-repo, and the owner's non-descriptive
   attestation establishes that it operated on real data with the boundary
   intact. The footnote states that no L3 claim rests on, or may cite,
   quarantined run detail. The other four Presentation cells remain L2 and the
   footnote says why.
5. No descriptive detail of the real session appears anywhere in the repository,
   a review, the PR, chat, or the retrospective. `tools/envelope_scan.py` is
   clean over the full range.
6. The evaluation harness is byte-unchanged and both manifests still pass.

## Review gates

**Track 1.** The vocabulary cannot express a value, identifier, or disposition —
a reviewer should attempt to smuggle one through it and fail. The runbook's
preflight step makes clear that the three answers come from the owner's own
trust domain and that the project observes nothing. The clipboard-copy
prohibition is stated where the owner will read it before the session, not
buried. Any code change is minimal and justified by the sitting, and
`server.mjs` and both manifests are byte-unchanged.

**Track 2.** A real headed browser process was actually launched by the real code
path, not a test double of it. The page rendered was the **product** page, not
the evaluation fixture. The synthetic workspace is structurally identical to a
real one, so the rehearsal proves something. The record states honestly what was
and was not covered. Any defect found is described fully — this track is
synthetic and description is safe here.

**Track 3.** The attestation is non-descriptive and matches ADR-0031 Decision 7's
ratified shape. All five ADR-0047 preconditions are affirmed. The matrix moves
exactly one cell. The footnote claims capability operation and not disposition
correctness. Every cited SHA resolves. No other cell moved. The envelope scan is
clean.

## Tracks

### Track 1 — Session runbook and non-descriptive failure vocabulary

Build the two artifacts the owner sitting needs. The runbook is the exact
sequence for one sitting: what to supply for each of the three preflight
answers and where those answers come from, how to point the capability at the
real residency without that locator entering any recorded surface, how to run
the session, what the ADR-0047 preconditions oblige during it, and how to tear
down. The vocabulary is the bounded set of statements the owner may make about a
session that failed.

Any scriptability repair is in scope but bounded as above.

### Track 2 — Real-browser rehearsal against a synthetic workspace

Owner-operated on the owner's machine. Launch a real headed browser through
`open_presentation_session` against a synthetic workspace and render the product
page. Follow the Track 1 runbook, so the runbook is rehearsed too. Record what
happened in full detail — this is synthetic and description is safe.

If a defect appears, it is repaired and the rehearsal is repeated before Track 3
begins. This gate is the point of the track.

### Track 3 — Real session, attestation, and records

Owner-operated, then foreman. The owner supplies the preflight answers, applies
their own confinement if they choose to, points the capability at the real
residency, runs the session, and looks. The foreman then files the attestation,
moves the single matrix cell with its footnote, writes the retrospective, and
updates `docs/phase-state.md`.

## Execution economy

Track 1 is one builder unit and one independent review. Tracks 2 and 3 are owner
acts and cost the project almost nothing in tokens; their cost is the owner's
sitting, which the runbook exists to keep short. All tracks land on one branch
and reach `main` as a single milestone PR, per the cadence recorded in
`docs/roles/foreman.md`.

## Execution record

**Complete 2026-07-27. Presentation moves L2 → L3 in the W-2 wages (1a) column.**
All six exit criteria met, criterion 2 with one named gap.

### Track 1 — session runbook and failure vocabulary (agent-built)

Five cycles: build, review, repair, recheck, repair, recheck.

- **Build `748b8e8`.** `docs/runbooks/presentation-real-session.md`, 365 lines,
  no code changed — `open_presentation_session` already ran as one act, so the
  scriptability repair was declined as out of the plan's bound. The builder
  recommended an interactive `input()` locator prompt over argv, env, or file,
  and named it partial closure rather than full.
- **Review `50a9030` — NOT READY, five findings, two blocking.** Finding 1 was a
  **code** defect found by a documentation track: `LiveViewingError` is a sibling
  of `PresentationSessionError`, so roughly a third of the runbook's own
  reason-code table propagated as an uncaught traceback — the one text the
  vocabulary cannot describe. Finding 2: the prose promised the `input()` prompt
  while the script derived the locator from its own position.
- **Repair `894ff23`.** Finding 1 fixed **at source**, not in the runbook
  template: `_classified_viewing_failure` forwards only the stable sub-code. The
  builder went beyond findings twice and flagged both.
- **Recheck `0f5e5dc` — NOT READY.** All five prior findings closed the failure
  rather than the sentence. But the deliberate `BaseException` passthrough left
  its consequence uncovered, and the reviewer **demonstrated it by running it**:
  Ctrl-C left an orphaned headed browser displaying the real return plus a
  `.live-view/session-*` directory holding the profile and disk cache of that
  render — residue outliving a preflight guarantee that binds only at session
  start.
- **Repair `36317be`.** Fixed structurally in three places — `_abandon_launch`
  extraction in `launch`, a `viewing` hoist closing the window where the browser
  is live and owned by nobody, and the template switched to `with`. Also closed
  the `__context__` locator-retention residual (`raise X from None` re-attaches
  `__context__` at raise time) and the socket-survival residual. 670 tests OK.
- **Recheck `9909cd6` — READY**, four named residuals. The reviewer re-measured
  against real `launch` rather than a double, and checked the builder's pre-fix
  test claim instead of accepting it. One residual — an overstated Step 3 bullet
  — was corrected by the **foreman** directly rather than in a third cycle, and
  recorded in the review record because no independent reader had seen that edit.

### Track 2 — real-browser rehearsal, synthetic workspace (owner-operated)

**CLEAN PASS.** Record:
`docs/reviews/2026-07-27-presentation-real-session-attestation-track2-rehearsal.md`.

Both rehearsal gaps from matrix footnote 5 are closed: a real headed browser was
launched by `open_presentation_session` — the real path, not a double — and it
rendered the **product** page rather than the evaluation fixture. Happy-path and
Ctrl-C teardown both confirmed by human observation: no surviving browser, no
surviving session directory. No page defects.

Two things recorded honestly rather than passed over: the browser-start-failure
exercise was **skipped** (charter-permitted, so a named gap — the
classified-refusal path has no human confirmation), and the runbook's first human
user reported it "not very clear, but fine" **without identifying the sentence**,
carried open rather than closed by guesswork.

### Track 3 — real session, attestation, records (owner-operated, then foreman)

Performed in the same sitting, after Track 2's gate passed. Attestation:
`docs/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md`.

Non-descriptive per ADR-0031 Decision 7 — session performed, dispositions
observed in quarantine, no artifact crossed — with each of ADR-0047's five
honesty preconditions affirmed **individually** rather than summarized,
conditions 3 and 4 being owner knowledge rather than mechanism.

Foreman records: matrix footnote 14 and the single cell move; the retrospective
at `docs/milestone-retrospectives/2026-07-27-presentation-real-session-attestation.md`;
`docs/phase-state.md`.

### Post-close repairs: two defects CI caught and the charter's checks could not

PR #96 failed `verify` twice, on two independent defects both introduced by
Track 1's second repair (`36317be`) and both invisible to everything this
milestone actually ran.

**The root cause is the charter's verification block, not either defect.** Every
Track 1 charter listed the same floor: three `unittest` modules, two harness
manifests, `envelope_scan.py`, and `git diff --check`. CI's `verify` runs
**`pytest`, `mypy`, `governance_lint.py`, and `envelope_scan.py`**. The charter
omitted `mypy` entirely, so a `strict = True` type error sat in merged-quality
code through a build, two repairs, and three independent review passes — one of
which verified the surrounding logic by running it — without anything looking
for it. The second defect below could only ever have been caught by CI, but the
first one was a `mypy` invocation away the whole time.

**Correction for future charters: the verification block must be the CI
sequence, or a stated subset with the omission justified.** A floor that is
quietly narrower than the gate is a floor that reports green on work that is
not.

#### Defect 1 — a platform-dependent test assertion

CI `verify` failed with **1 failed, 669 passed** —
`test_the_socket_is_released_even_when_shutdown_raises`, added by Track 1's
second repair (`36317be`) to close the socket-survival residual. It passed on
macOS every time it was run, locally and by the reviewer, and failed on Linux.

The assertion was `URLError`; Linux raised `ConnectionResetError`. The cause is
specific to this test rather than to the four sibling assertions that pass:
`shutdown()` is deliberately made to explode, so the serving thread is still
running when `server_close()` closes the listening socket underneath it. What a
client then sees is platform-dependent — ECONNREFUSED wrapped as `URLError` on
macOS, ECONNRESET raised bare on Linux, because `urlopen` wraps failures from
the request phase and not from reading the response.

Repaired by the **foreman** by widening that one assertion to `OSError`, which
`URLError` subclasses. The property under test is unchanged and still has teeth:
if the socket were still serving, `urlopen` would return a page and no exception
would be raised at all. The four orderly-teardown sites keep the stricter
`URLError`, because their serving thread is stopped before the socket closes and
their behaviour is not platform-dependent.

Recorded here rather than silently, on the same discipline as Track 1's
post-review runbook correction: it is a change to a reviewed artifact that no
independent reader has seen. It changes no product code and no vocabulary rule.

**The generalizable point:** the test encoded a platform's errno as if it were
the contract. Every prior exercise of this path — including the reviewer's, who
verified this repair by running it — ran on macOS, so the assumption was
invisible until CI ran it somewhere else. Same shape as this milestone's main
lesson at a smaller scale: the exercise covered what it drove.

#### Defect 2 — a strict-mode type error, never once looked for

With the test fixed, `verify` reached the `mypy` step for the first time and
failed there: `live_session.py`, incompatible assignment of `None` to a
variable inferred as `PresentationSessionError`. Fixing that surfaced a second,
deeper one behind it — `_browser` receiving `LiveViewingSession | None` where a
session is required, because the `viewing = None` hoist (itself a correct fix,
closing the window where a browser is live and owned by nobody) left the value
un-narrowed at the constructor.

Repaired by the **foreman** by moving the success path into the `try`'s `else`
clause, so `viewing` is narrowed on the one path that uses it, and letting
`raise classified` fall to the end. This **preserves the property the second
repair existed to establish** — the classified error is still raised after the
handler has exited, with `sys.exc_info()` clear, so `__context__` cannot be
re-attached and no `OSError.filename` can carry the locator out. That is the
locator-confinement claim the reviewer verified independently, and it is
unchanged; only the control flow around it moved.

Full local reproduction of the CI sequence now passes: `pytest` 670 passed /
2451 subtests, `mypy` clean over 127 files, `governance_lint.py` conformant,
`envelope_scan.py` clean over `main..HEAD`.

### Exit criteria

| # | Criterion | Met |
| --- | --- | --- |
| 1 | Runbook and mechanical-not-evaluative vocabulary, reviewed as a data-safety artifact | yes |
| 2 | Real headed browser rendered the product page on a synthetic workspace; both rehearsal gaps closed | yes, with the skipped browser-start-failure exercise named as a gap |
| 3 | Real session performed; non-descriptive attestation with all five preconditions affirmed | yes |
| 4 | Matrix shows Presentation / W-2 wages (1a) at L3 with a footnote in the 7/11 pattern; other four cells L2 with the reason stated | yes (footnote 14) |
| 5 | No descriptive detail anywhere; envelope scan clean over the full range | yes |
| 6 | Evaluation harness byte-unchanged, both manifests pass | yes |

### Carried forward

The classified-refusal path's missing human confirmation; the runbook's
unidentified unclarity; Track 1's four residuals; and the owner-held pair —
invocation discipline and the `cd` history entry — that nothing this repository
writes can close.
