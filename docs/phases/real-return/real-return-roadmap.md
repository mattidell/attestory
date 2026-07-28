# Real Return Phase — Roadmap

Audience: Product (roadmap); Shared (status)

## Thesis

Foundation proved the substrate: declared contracts, honest blocking, auditable
derivation, and a governed decision process — all on synthetic fixtures. The
Real Return phase makes the product *real*: the system holds and computes the
owner's actual tax data, under a data boundary that is itself a ratified
contract. The phase's standing test is simple: **does the product now do
something for its user that it could not do before?**

## How milestones are selected in this phase

This phase retires the pre-written roadmap ladder. Milestones are selected from
the frontier of the **maturity matrix** (`maturity-matrix.md` in this
directory): each milestone names the cells it raises and the level it raises
them to, and the matrix is updated at milestone close alongside the phase-state
briefing. The selection decision itself remains owner-directed (Tier 3), with
the foreman presenting frontier candidates and a recommendation.

All Foundation process machinery is retained: milestone plans (owner-approved
before any charter, ADR-0013), prototype-driven Tier 2/3 decisions with rival
evidence (ADR-0005/0013), per-ADR and per-track no-ff merges to a continuous
`main` (ADR-0030), per-track review gates, retrospectives, and the data-safety
scan.

## Phase close — 2026-07-28

**Real Return is closed.** The phase set no ladder and one standing test —
*does the product now do something for its user that it could not do before?* —
and the test is met. The system holds and computes the owner's real W-2,
1099-INT and 1099-DIV facts behind a ratified data boundary, produces Form 1040
lines 1a, 2b, 3a, 3b, 9, 11, 12, 15 and 16 with Schedule B when the conditional
requires it, explains every published figure by citation, blocks honestly when it
cannot, and — since 2026-07-27 — shows that result to its owner on a human
surface that has really operated against the real residency.

**Every cell in the maturity matrix is L3 or better**, so frontier-driven
selection has no frontier left inside the phase's five columns. The matrix's
silence is the argument for closing rather than continuing.

**Read the completion accurately.** It is breadth- and hardening-limited by
construction: five income/return domains, one implemented schedule, one human
surface, and **one** real viewing session (2026-07-27) behind the entire
Presentation row. Nothing in this record asserts more sessions than that. It is
not a claim that the product is finished for its user — the user still cannot
file anything, and still enters facts by hand-editing JSON. Those gaps are
invisible to every cell in the grid because no row is named for them.

**Carried into the next phase, unclosed:**

1. The **classified-refusal path has no human confirmation** — that a browser
   which fails to start arrives as a stable reason code rather than a traceback
   rests on tests and independent review only. The oldest open item on this path,
   first named 2026-07-27.
2. The **session runbook has an unidentified unclarity**, reported by its first
   human user with the sentence unnamed.
3. The named deferral ledger
   (`milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md`)
   and the shims listed in the phase-state product briefing.

The maturity matrix in this directory is the closed instrument of *this* phase.
A later phase may adopt, extend, or replace its coordinate system; it should say
which, rather than inheriting it silently.

## Status

- Presentation — Completing the Row — **complete 2026-07-28; plan PR #97,
  milestone PR #98 (`d7628ea`).** A **records milestone**: no session, no
  browser, no real data, no code. Its one substantive act was asking the owner a
  question the repository cannot answer — *which columns did you observe during
  the session you already ran?* — and its one control was that a column the
  owner did not name would not move, with a three-cell close declared a success
  rather than a failure. All four were named (Interest 2b, Dividends 3a/3b,
  return-level conditions, Schedule attachments), so all four moved L2 → L3 on an
  **amendment** to the 2026-07-27 attestation, and the control never fired. It
  was still real: ADR-0031 Decision 7's shape includes observing dispositions in
  quarantine, so naming a column asserts observation, and no amount of rendering
  establishes that a person looked. **Observing a column is not auditing it** —
  L3 asserts the capability operated (footnotes 7/11). Most of the milestone's
  care went into foreclosing one misreading: a row filled in over two days by two
  milestones invites the inference that several sessions occurred, and there has
  been exactly one. That is stated in the matrix header, footnote 15, the
  amendment, the retrospective and the phase-state briefing, because it is free
  to prevent now and unfalsifiable later — the evidence that would settle it is
  precisely the quarantined detail nobody may cite. The plan verified directly
  that the surface covers all five columns rather than inheriting the previous
  closeout's "no build gap" (that same claim preceded three code defects), and its
  Verification block was set to the CI `verify` sequence in response to the
  previous milestone's root-cause finding; CI passed first try. Plan:
  `milestones/presentation-row-completion.md`; retrospective:
  `../../milestone-retrospectives/2026-07-28-presentation-row-completion.md`.

- Presentation — Real Session and Attestation — **complete 2026-07-27; plan PR
  #95, milestone PR #96.** **Presentation L2 → L3 in W-2 wages (1a)** — the
  first maturity lift for the row and the first time this project's human
  surface ran on the owner's real data. Track 1 was chartered as a
  *documentation* track (a session runbook plus a failure vocabulary that is
  mechanical rather than evaluative, because ADR-0047 precondition 5 forbids the
  owner from describing a defect they see during the real session) and found
  **three real code defects** in code the previous milestone had rehearsed
  clean: `LiveViewingError` was a sibling rather than a subclass of
  `PresentationSessionError`, so about a third of the reason-code table arrived
  as an uncaught traceback — the one text the vocabulary cannot describe;
  teardown's `except` was too narrow for its own promised code to be reachable;
  and Ctrl-C left an orphaned headed browser displaying the real return plus a
  `.live-view/session-*` directory holding that render's profile and disk cache,
  outliving a preflight guarantee that binds only at session *start*. **The
  durable lesson: a rehearsal's value is bounded by the set of endings it
  drives.** All three fixes went into the session code rather than the runbook
  template, because a guarantee living only in a copyable example silently
  no-ops when adapted — fail-open drift, named for the third time in this
  project. Five cycles: `748b8e8`, `50a9030` `NOT READY`, `894ff23`, `0f5e5dc`
  `NOT READY`, `36317be`, `9909cd6` `READY`. Track 2 (owner-operated) launched a
  real headed browser through the real path against a **synthetic** workspace
  and rendered the product page: clean pass, no page defects, first human
  confirmation of the interrupt repair — structural rather than cautious, so
  that the first real render would not also be the real session. Track 3
  performed the session and the non-descriptive attestation in the same sitting.
  **Two post-close repairs CI caught and the charter's checks could not** (a
  platform-dependent socket assertion, and a mypy strict-mode error), whose root
  cause was a verification block narrower than the CI gate: **a charter's
  verification block should be the CI sequence, or a stated subset with the
  omission justified.** Plan:
  `milestones/presentation-real-session-attestation.md`; retrospective:
  `../../milestone-retrospectives/2026-07-27-presentation-real-session-attestation.md`;
  evidential basis: maturity-matrix footnote 14.

- Presentation — Live Session Path — **complete 2026-07-27; plan PR #92
  (`22c9003`), milestone PR at close.** Built and rehearsed everything the
  Presentation L3 session needs without performing one, because the owner was
  away from their desk and the run and attestation are theirs alone. Its success
  condition was explicitly that **no maturity row moves** — a shape that cannot
  be tempted to claim a lift. The plan lost a track before chartering: preflight
  probes were cut because workstation-precondition observation is owner-held for
  the same reason confinement is, which made the repository's posture uniform
  (it authors none of its own boundary enforcement) and removed the
  `tmutil isexcluded <path>` `argv` locator disclosure rather than mitigating
  it. Track 1 amended **ADR-0047** to record the owner's first-principles
  Seatbelt evaluation and the owner-held custody of Class C confinement and
  Class D observation (`e4fd30f`, review `READY`). Track 2 built
  `open_presentation_session` — capability → preflight → model → loopback →
  browser → teardown as one act (`d166d4b`) — and returned **`NOT READY`** on two
  findings that were one finding: the loopback socket carried the entire
  presentation model with no authentication (loopback is not a control; an
  ephemeral port is not a secret), and the session served the evaluation fixture
  page, which declares "synthetic `demo-*` data only" in the title of the screen
  the owner reads while attesting. Both lived in the *join* between correct
  components. The repair added a 256-bit route token, a separate product surface
  that asserts no provenance in either direction, and a fail-closed refusal to
  serve any page declaring itself synthetic; ADR-0047 gained a second amendment
  classifying the session's own socket as Class B. Track 3 rehearsed the full
  path end to end against a synthetic workspace and recorded honestly that no
  real browser was launched and the product page has never been rendered by one.
  Presentation ends at **L2**, one owner act from L3; the data-boundary row ends
  at **L3** as a permanent owner-accepted ceiling. Retrospective:
  `docs/milestone-retrospectives/2026-07-27-presentation-live-session-path.md`.
- Presentation — Live Viewing Boundary and Invocation Vehicle — **complete
  2026-07-26; plan PR #88, Track 1 PR #89 (`b37c536`), Track 2 PR #90
  (`bc0d8dc`).** The milestone rejected its own obvious shape before building:
  a flag-confined browser launcher would have failed on inspection, because
  Chrome's containment flags are cooperative settings inside a same-UID process
  and ADR-0044 already forecloses that as a trust boundary — the Guarded
  Transport failure again. It defined the environment first. Track 1 ratified
  **ADR-0047 (Live Viewing Environment)**, which treats a viewing session as an
  activity *within* the Live-Run Data domain rather than a fifth domain,
  classifies every headed-browser channel into four classes, and states exactly
  what the owner would attest; it took two review cycles (`b1a630a`, `a476c40`
  `NOT READY`; `63c4102` `READY`), one of them catching an overclaim in the
  negative direction — an assertion of macOS platform impossibility where
  Seatbelt was merely unevaluated. Track 2 built the confined headed invocation
  vehicle and fail-closed preflight (`d8083f9`): destinations confined to the
  live workspace and canonicalized against symlink escape, and a preflight that
  returns reason codes and cannot emit the residency locator on any surface.
  Review `974bbac` returned `NOT READY` on a missing regression guard for the
  confirmed-absent clipboard case; repair `fa47e16` was verified against the
  exact mutation it exists to catch, and recheck `1ba2634` reproduced that
  mutation independently. **No maturity lift:** no real workspace was touched,
  no viewing session performed, and no attestation made. Presentation remains
  L2 and the data boundary remains L3; the remaining distance to Presentation
  L3 is real operation plus the owner's non-descriptive attestation, which is
  an owner act rather than a build. No enforcement substrate was selected;
  Seatbelt remains an unevaluated candidate routed to ADR-0044's future gate.
  No next milestone is selected. Plan:
  `milestones/presentation-live-viewing-boundary.md`; retrospective:
  `../../milestone-retrospectives/2026-07-26-presentation-live-viewing-boundary.md`.

- Presentation — L2 Integration Grounding — **complete 2026-07-26; PR #86
  merged as `1f3bb9a` with CI `verify` green.** Boundary inspection corrected the initial PR #82 plan before
  merge: renderer integration began with a hand-shaped synthetic model, the
  coordinator discarded the inputs needed to construct it, and the browser
  harness was intentionally synthetic-only. Track 1 closed that
  coordinator-to-model gap on production-shaped synthetic data. Its first
  Builder stopped cleanly when the existing demo manifest proved impossible to
  satisfy from resolved content: line 2a is not modeled and real line 9 is not
  guard-inapplicable. The amended charter keeps that manifest unchanged as the
  renderer regression floor and adds a dedicated production-shaped manifest
  for the regenerated golden. Track 1 build `81c5504` received one independent
  `NOT READY` review (`e36086a`), one focused repair (`759c9fa`), and a `READY`
  recheck (`4a74ffd`). Track 2 records the six-row capability-state handoff in
  maturity-matrix footnote 5; fresh completion review `7f6ae79` returned
  `READY`. The handoff makes explicit that no live browser invocation vehicle
  or real operation exists; the synthetic harness is not that vehicle.
  Presentation remains L2; no next milestone is selected. Plan:
  `milestones/presentation-l2-integration-grounding.md`; retrospective:
  `../../milestone-retrospectives/2026-07-26-presentation-l2-integration-grounding.md`.

- Browser Evaluation Runner Completion — **complete 2026-07-25; PR #71 merged
  `c329afd` with CI `verify` green on the merge commit.** This tooling
  milestone resumed the preserved implementation from
  `track/presentation-economy-t1-harness-core` rather than rebuilding it. It
  repaired the independent review's six blockers, completed the transferred
  lifecycle/output measurements, received one focused delta review (`READY`),
  and closed two owner-authorized post-verdict residuals (R1/R2) under a
  narrow one-time exception to the plan's fixed cap. It is not a presentation
  prototype, an economy experiment, or an adversarial-novelty practice run; it
  added no product UI, ADR, or matrix lift. Plan:
  `milestones/browser-evaluation-runner-completion.md`; retrospective:
  `../../milestone-retrospectives/2026-07-25-browser-evaluation-runner-completion.md`.

- Presentation — Citation Walk on Real Derivation Output — **complete
  2026-07-26; PR #77 merged as `2d4c195` with CI `verify` green.** Shipped the
  ADR-0046 citation-walk renderer across the complete synthetic disposition
  matrix and T1–T3 fault suite. Its first independent review returned
  `NOT READY` on uncited numeric-zero paths and an invalid-input diagnostic;
  one repair closed both and the focused recheck returned `READY`. The
  milestone moved Presentation to L2. Its original “exercise one real run”
  handoff was later corrected by the L2 Integration Grounding plan after the
  renderer, harness, and coordinator seams were inspected. Plan:
  `milestones/presentation-citation-walk.md`;
  retrospective:
  `../../milestone-retrospectives/2026-07-26-presentation-citation-walk.md`.

- Presentation Evaluation Process Economy — **closed early by owner direction
  2026-07-25; Track 0 merged in PR #66 (`870c8ed`) as the accepted foundation;
  Track 1 was rejected and not merged; Tracks 2–3 were canceled.** This process
  milestone follows the
  Presentation Exploratory Milestone's economy analysis. Its durable capability
  is a quality-adjusted learning loop scoped specifically to UI/UX presentation
  iteration, development, and review: versioned presentation workloads,
  observations, and comparisons; a source-faithful historical baseline; and
  quality-before-cost/participating-role enforcement that prevents
  cheaper-but-worse or cost-shifted work from appearing economically promising.
  The proposed general browser runner failed independent review on six
  lifecycle/failure-integrity blockers. Its implementation remains preserved
  outside `main`; the separately planned Browser Evaluation Runner Completion
  milestone resumes that work without reopening this closed economy milestone.
  The milestone adds no product UI, ADR, or maturity-matrix lift. Plan:
  `milestones/presentation-evaluation-process-economy.md`; retrospective:
  `../../milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md`.

- Presentation Exploratory Milestone — **complete** (2026-07-24). Five
  two-builder/two-reviewer cycles over a synthetic citation-walk surface
  demonstrated the surface-a-criterion → specify → verify loop and found
  roughly 65–80% of the exercised UI-quality surface mechanically checkable.
  Its seven-vector evaluation analysis, reusable final prototypes, synthetic
  fixtures, and harness seed live under
  `../../prototypes/human-presentation-citation-walk/`. It was deliberately
  exploratory: no ADR and no matrix-cell lift. Retrospective:
  `../../milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md`.

- Foreman Context Loading — **complete** (merged PR #56, `962c1ac`,
  2026-07-23). The process milestone
  adds a deterministic, provenance-bearing advisory foreman capsule, compact
  metadata for volatile re-entry records, charter capsules for builders and
  reviewers, mechanical task capsules for clerks, action-specific deep-read
  routing, and an honest handoff boundary. Trusted-advisor context is out of
  scope. Its initial independent review found M3; the authorized M3 delta
  review returned READY. It changes neither the live-run topic's scope nor its
  planning-only status; no seat was authorized by this entry. Plan and
  retrospective: `milestones/foreman-context-loading.md` and
  `../../milestone-retrospectives/2026-07-23-foreman-context-loading.md`.

- Live-Run System Definition and Trust Domains — **complete; publication PR
  #61 merged** (owner accepted ADR-0044 on 2026-07-23). ADR-0044 and
  its plain-language companion define the four authority domains and crossings,
  the unprivileged-developer threat posture, guarded transport as publication
  integrity, and the later enforcement/L4 gate. The owner-directed bounded
  review returned READY with no blocking finding. No real run, owner
  attestation, implementation, mechanism selection, schedule commitment, or
  maturity lift is part of the decision; the data-boundary row remains L3.
  Schema-publication and agent-scope controls remain tabled. Plan:
  `milestones/live-run-trust-domain-definition.md`; retrospective:
  `../../milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md`.

- Correction Authority and Marshaller Simplification — **complete**
  (2026-07-22; plan approved PR #49). ADR-0041 (Track 0, PR #50) closes the
  supersession-policy vocabulary to `free`/`locked`/`closed-on-attestation`,
  ratified (PR #52); enforcement (Track 1, PR #53) lives at the existing
  dispatch site in `findings.py`, shipped as new `fact-type.v3`/`bundle.v3`
  schema versions (`v1`/`v2` of each untouched); marshaller dedup (Track 2,
  PR #51) collapsed four routes' duplicated fact-id parsing into shared
  helpers without merging the routes themselves (distinct multiplicity
  semantics, correctly left alone). Retires deferral-ledger entries 8 and
  13; raises the Correction & supersession lifecycle matrix row L3→L4 across
  every domain — the phase's first aspect-wide L4. Named deferrals live in
  `milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md`;
  retrospective at
  `docs/milestone-retrospectives/2026-07-22-correction-authority-and-marshaller-simplification.md`
  records a schema-immutability defect caught and corrected in-branch before
  merge. Next milestone selection is owner-directed from the maturity-matrix
  frontier.

- Push-Envelope Preflight and Bypass Visibility — **complete** (Track 1
  merged PR #45; Track 2 records merged PR #46, `9cc6e89`, 2026-07-22). This
  is an honest L3
  operator-safety aid, not the
  original L3→L4 credential-confinement claim. The stopped H1 prototype
  demonstrated that two clean-room local-Git topologies and one repair did not
  yield reproducible scan-before-credential-release evidence. The rescope
  added a synthetic audit that reports hook protection when it runs and reports
  raw `--no-verify` as still bypass-reachable; it retires neither deferral nor
  raises the matrix. A later OS/identity/hosted-boundary topic is the only path
  back to credential-confinement scope. Track 2 review found no blocking
  finding in its re-affirmation of ledger entries 1/2 and explicit L3 matrix
  qualification; it made no real-run or server-control claim.

- Dividends and Schedule B Slice — **content complete, completion records in
  progress** (plan approved 2026-07-18; Track 5 records on
  `track/dsbs-t5-completion`, pending independent review and owner merge).
  Raised the
  Dividends and Schedule-attachments matrix columns L0→L3 across all eight
  aspects. D1 (attachment ontology, ADR-0036), D2 (line 16 under qualified
  dividends, ADR-0038), D3 (1099-DIV composition, ADR-0035) all ratified;
  ADR-0037 (`conditional_dependency_set` prerequisite substrate) ratified and
  merged as Track 0a. Tracks 0a/1/2/3/4 merged per-track (ADR-0030; PRs
  #30/#31/#32/#36/#39). The owner contributed real 1099-DIV facts to the
  same quarantined out-of-repo workspace and ran the widened slice; the
  non-descriptive attestation is recorded in the milestone plan (2026-07-21,
  PR #40). Named deferrals live in
  `milestones/dividends-schedule-b-slice-deferral-ledger.md`. Next milestone
  selection is owner-directed from the maturity-matrix frontier.

- First Real Return Slice — **complete** (2026-07-18; Track 5 records merged
  PR #21). D1 residency (ADR-0031), D2 contribution (ADR-0032), and D3
  production resolver (ADR-0033) ratified; Tracks 1–4c merged per-track
  (ADR-0030). The owner contributed real W-2 / 1099-INT facts to a
  quarantined out-of-repo workspace and ran the slice; the non-descriptive
  attestation — ran the slice, dispositions observed in quarantine, no
  artifact crossed the boundary — is recorded in the milestone plan
  (2026-07-18, PR #20). The repository carries no personal data,
  mechanically gated (Track 4b envelope hooks). Named deferrals live in
  `milestones/first-real-return-slice-deferral-ledger.md`. The phase's
  standing test is met: the product computes its user's actual return
  slice, which it could not do before. Next milestone selection is
  owner-directed from the maturity-matrix frontier.
