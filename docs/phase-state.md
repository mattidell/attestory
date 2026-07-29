<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "packaging-the-surface",
  "active_plan": "docs/phases/legible-entry/milestones/packaging-the-surface.md",
  "status": "Legible Entry accepted (PR #100). AT THE MILESTONE-SELECTION FRONTIER — nothing is chartered. Milestones 1 and 2 are both CLOSED 2026-07-28 and NO MATURITY CELL HAS MOVED; both built decisions and delivery, not the entry loop. MILESTONE 1, THE ENTRY BOUNDARY (PR #102, c451a40, ADR-0048 ACCEPTED): a browser form is acceptable for typing real tax facts on stated conditions, and an entry surface emits act-contribution.v1 through the existing admission path rather than writing facts directly. It also established that CONFINEMENT IS NOT TOTAL — the vehicle writes a single-instance lock outside the confined tree, surviving a crash, holding no typed content. Open from it: NOTHING HAS SEARCHED FOR THE RESIDENCY LOCATOR OUTSIDE CONFINEMENT (every run looked for typed tokens only); the singleton lock as a second orphan surface; crash-reporter and GPU-cache paths narrowed but not closed; the spellcheck flag's mechanism undesigned. MILESTONE 2, PACKAGING THE SURFACE (PR #108, closed at 2fb6761): UI code now crosses Developer/Supply to Live-Run Data in a SECOND, SEPARATE ARTIFACT (surface-artifact.v1) under its own surface-adoption, carrying opaque program bytes verified by digest and never validated for meaning. artifact-package.v4 is byte-for-byte UNTOUCHED and is to stay that way. packages/derivation/surface_resolver.py reuses ADR-0033's release/registry chain and diverges only at member-graph validation. One trivial Svelte page builds at the workspace offline (svelte/compiler plus browser import maps, no bundler) and opens in the live-viewing vehicle on a synthetic workspace; five refusal paths tested. ADR-0049 is PROPOSED, NOT RATIFIED — ratification is the owner's. OWNER DECISION, same day, AFTER the close: THE REPOSITORY DOES NOT STORE THE VENDORED DEPENDENCY TREE. node_modules is gitignored; it ships in the artifact and is reconstructed with `npm ci` in packages/sample_data/surface_t1/content/app followed by tools/generate_surface_t1_fixtures.py. Six surface tests SKIP without it, so the digest and refusal evidence is reproducible on demand rather than continuously checked; the data-safety test was deliberately left unguarded and runs everywhere. Measured tree: 941 entries / 5,065,001 bytes from one direct dependency. CARRIED OPEN: the build's output is never digest-verified (trust is verified inputs plus one fixed command; determinism CHECKED byte-identical on one machine under Node v25.8.0, UNVERIFIED across machines or versions, which is the same gap as the Node precondition seen from the other side); offline enforcement is macOS sandbox-exec only with NO CI COVERAGE; surface_resolver imports three underscore-private names from production_resolver (real reuse, fragile coupling); the sample page uses no TypeScript so that toolchain cost is untested; tools/build_orientation_block.py defaults to --ref main, which is a stale Real-Return-era branch in this repo — the live trunk is main-ui. Retrospectives: docs/milestone-retrospectives/2026-07-28-entry-boundary.md and 2026-07-28-packaging-the-surface.md; the latter's subject is that the milestone plan shipped a FALSE PREMISE — the foreman called the package-member route 'close to forced' without opening the schema, and it survived a plan PR and an owner decision built on top of it. NEXT: milestone 3, The Entry Loop synthetic, UNPLANNED. It builds the guided loop end to end on synthetic data to L2, and works out the usability evaluation criteria that score its own L2 claim. Filing is out of scope for the phase. Process: a milestone gets one PR to open and one to close; tracks keep their review gate but not their own PR; PRs target main-ui. Phase documentation uses plain, product-facing language — the habit being corrected is writing every planning document as though defending it to a hostile auditor. Prior phase Real Return closed 2026-07-28 with every matrix cell L3 or better; read narrowly, it was breadth- and hardening-limited by construction. THE PHASE-BOUNDARY LEGIBILITY AUDIT IS STILL DUE and is owner-spawned — the foreman must not launch it.",
  "current_role": "Foreman — Packaging the Surface closed; at the milestone-selection frontier for Legible Entry, nothing chartered",
  "current_prompt": "docs/phases/legible-entry/legible-entry-roadmap.md"
}
-->
# Phase State

This is the **single re-entry document.** It carries the machine-readable
`foreman-context-v1` block above, a **product briefing** in ordinary language,
the current operational state, and durable pointers. It describes *now*: durable
history lives in milestone retrospectives, review records, ADRs, and Git, and
this file links there rather than retelling it.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
.venv/bin/python3 tools/foreman_context.py --ref HEAD --format markdown
```

Reconcile its source commit and worktree report with Git, then read the
action-specific sources it names. If it refuses, inspect those committed sources
directly and resolve the disagreement before acting. The capsule reports state;
it does not change the data boundary or replace accepted authority.

## Product briefing (as of 2026-07-26, after Presentation L2 grounding)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2, 1099-INT, and 1099-DIV facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16** with full explanations, plus Schedule B (Parts I/II payer itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion facts) when the $1,500 conditional requires it — publishing, or blocking honestly with a walkable account of what is missing. Line 16 is the QDCG worksheet over contributed declared-absence facts, with a bidirectional interlock against the capital-gain-distribution signal. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; the 1099-DIV declared universe is boxes 1a/1b only (2a/3/5/7/12 are named honest-block exclusions); standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family — including both dividend box families — closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8). A correction to an already-answered fact is no longer necessarily unrestricted: a fact type may declare `locked` (never correctable again) or `closed-on-attestation` (correctable until a named closure fact attests true), enforced at the existing supersession-policy dispatch (ADR-0041); every fact type shipped today still declares `free`, unaffected, by choice.

**Shims in place.** E8.1 UI coverage partially met — a citation-walk renderer exists, satisfies ADR-0046 end to end, and as of 2026-07-27 has been exercised in a real viewing session against the owner's real residency, carrying Presentation to **L3 across all five columns** — the W-2 wages (1a) cell on that session's attestation (matrix footnote 14), the other four on a 2026-07-28 amendment naming the columns the owner observed in that same single session (footnote 15). No other form or schedule has a human surface. Mechanical separation between Developer/Supply and Live-Run Data **not implemented**, which holds the data-boundary row at L3; guarded publication transport / credential confinement also not implemented, as a separate publication-integrity deferral; a synthetic push-envelope posture audit makes the hook/`--no-verify` bypass visible but does not protect an owner push; ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment; `closed-on-attestation` reaches only fact types keyed identically to their gate fact type, not yet differently-keyed per-item facts. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md` (which also dispositions the Dividends and Schedule B Slice ledger's entries this milestone touched — two, both retired).

**What the completed milestones establish.** Live-Run System Definition and Trust Domains accepts ADR-0044 as the project's bounded security position: Developer/Supply, Publication, Live-Run Data, and Owner Authorization are separate logical authority domains; the intended live supply crossing is the current owner-adopted, byte-verified package; and guarded transport belongs to publication integrity rather than the live-data privacy wall. It implements no isolation mechanism, schedules none, and leaves the data-boundary row at L3. The Presentation Exploratory Milestone then demonstrated an agent-authored, agent-reviewed UI-development loop on a synthetic citation walk: roughly 65–80% of the exercised quality surface was mechanically checkable, while information-design judgment remained distinct and under-served. Presentation Evaluation Process Economy added the Track 0 declare → observe → compare → retain foundation: strict presentation workload/observation/comparison contracts, a source-faithful historical baseline, participating-role completeness, and quality-before-cost enforcement; its proposed general browser harness failed independent review and was not merged. Browser Evaluation Runner Completion then finished that same runner as trustworthy tooling: it adopted the preserved implementation commit rather than rebuilding it, repaired the review's six blocking correctness classes plus two owner-accepted post-verdict residuals (R1/R2), and completed the transferred lifecycle/output measurements, under one focused delta review and one focused recheck. It added no product UI, ADR, or maturity lift; it removes the "runner not trustworthy" blocker on starting presentation work. Presentation — Citation Walk on Real Derivation Output then spent that unblocked capacity: it ratified ADR-0046 (Presentation Surface Contract) straight from the exploratory milestone's existing five-cycle evidence rather than re-deriving it, and shipped the first conforming human surface. Its lasting result is the contract, not the page — zero-authority foreclosure (nothing renders without a source citation), blanket redaction of rejected values, section-level blocked-state salience — and the demonstration that an independent review gate catches contract violations the builder's own 23-criterion manifest passed clean (F1, F2). It lifts Presentation to L2. A later boundary inspection corrected its proposed next bar before that proposal merged as a new plan.

**What just completed.** Presentation — L2 Integration Grounding corrected the
prior closeout's unsupported conclusion that a real exercise
required no further building. Before this milestone, renderer integration
started from a hand-shaped model, the coordinator discarded the publications
and resolved graph needed to construct it, and the browser harness was
intentionally synthetic-only. Track 1 closed the coordinator-to-model gap on a
production-shaped synthetic run. Its first Builder correctly stopped before
writing code because the existing demo manifest requires line 2a and
guard-inapplicable line 9 states absent from the resolved production package.
The amended charter preserves that manifest as the full renderer regression
floor and adds a dedicated manifest for the coordinator-generated golden.
That build landed as `81c5504` on the milestone branch. Independent review
`e36086a` returned `NOT READY` on one coordinator-level projector-failure path.
The plan's single repair landed as `759c9fa`; focused recheck `4a74ffd` returned
`READY`. Track 2 records the resulting six-row capability state in the maturity
matrix, and completion review `7f6ae79` returned `READY`. PR #86 merged as
`1f3bb9a` with CI `verify` green. Presentation remains L2: no live browser
invocation vehicle exists and no real operation occurred. The next milestone
is unselected.

**Nature of the pending schema/contract change.** None pending. `fact-type.v3` and `bundle.v3` are published; any further correction-authority extension is separately chartered. ADR-0044 is accepted positioning, not a mechanism decision: any authority-separation implementation requires a later owner-selected milestone, mechanical proof, and real-run verification before an L4 claim.

## Current state (2026-07-28)

**Phase: Legible Entry.** Accepted 2026-07-28 in PR #100. The phase is about
getting the owner from a pile of tax documents to a computed return without
opening a text editor. Roadmap:
`docs/phases/legible-entry/legible-entry-roadmap.md`.

- **Milestone 1, The Entry Boundary — closed 2026-07-28.** PR #102 merged at
  `c451a40`; **ADR-0048 accepted**. A browser form is acceptable for typing real
  tax facts on stated conditions, and an entry surface emits
  `act-contribution.v1` through the existing admission path rather than writing
  facts directly. No product code changed and no maturity cell moved — it was a
  decision, and the instrument measures capability.

  What it means for building the entry surface: the form runs inside the
  confined vehicle rather than a browser someone opens themselves; entry hands a
  contribution to the existing boundary; the spellcheck network path must be
  closed by an explicit flag. It says nothing about what the form asks or how a
  field explains itself — that design is entirely still ahead.

  It also established that **confinement is not total**: the vehicle writes a
  single-instance lock outside the confined tree, surviving a crash, holding no
  typed content. That was believed total before this milestone.

  Retrospective: `docs/milestone-retrospectives/2026-07-28-entry-boundary.md`.

- **Open, and carried in ADR-0048 rather than fixed.** Most consequential:
  **nothing has searched for the residency locator outside confinement** — every
  run looked for typed tokens only, and the locator is protected in its own
  right. Also: the singleton lock is a second orphan surface sitting outside the
  residency with nothing sweeping it; crash-reporter and GPU-cache paths are
  narrowed but not closed; the spellcheck flag's mechanism is undesigned.

- **Milestone 2, Packaging the Surface — closed 2026-07-28.** PR #108 merged at
  `2fb6761`. UI code now has a sanctioned route into the live workspace: a
  **second, separate artifact** (`surface-artifact.v1`) with its own adoption,
  carrying program bytes verified by digest and never read for meaning. It hangs
  off the same release and registry verification the rule package already uses,
  and **`artifact-package.v4` is untouched** — the package's promise that
  everything in it validates stays true without a footnote. One trivial Svelte
  page ships through it, builds at the workspace with the network off, and opens
  in the live-viewing vehicle on a synthetic workspace. No maturity cell moved:
  this is the delivery route, not the loop.

  **ADR-0049 is proposed, not ratified.** Ratification is the owner's.

  The plan for this milestone shipped a false premise — it said the UI would
  ship as members of the adopted package, which is impossible, and that survived
  a plan PR and an owner decision built on it. Caught only because chartering
  forced someone to open the schema. Retrospective:
  `docs/milestone-retrospectives/2026-07-28-packaging-the-surface.md`.

- **The repository does not store the vendored dependency tree** (owner
  decision 2026-07-28, landed after the close as `370f8a6`). `node_modules/` is
  gitignored. It ships inside the artifact; it is checked into nothing. Rebuild
  it before running the surface tests:

  ```sh
  (cd packages/sample_data/surface_t1/content/app && npm ci)
  python3 tools/generate_surface_t1_fixtures.py
  ```

  Six tests skip without it, so the digest and refusal evidence is reproducible
  on demand rather than continuously checked. The data-safety test is
  deliberately unguarded and runs everywhere.

- **Open from milestone 2, carried not fixed.** The build's **output is the one
  thing in the chain no digest covers** — trust is verified inputs plus one fixed
  command. Determinism was checked byte-identical on one machine under Node
  v25.8.0 and is unverified across machines or Node versions; that is the same
  gap as the Node precondition seen from the other side. Offline enforcement is
  proved only under macOS `sandbox-exec`, with no CI coverage, because the tests
  need Node and Chrome present. `surface_resolver.py` reuses three
  underscore-private names from `production_resolver.py` — real reuse, fragile
  coupling. The sample page uses no TypeScript, so that toolchain cost is
  untested and will appear later.

- **Milestone 3, The Entry Loop (synthetic) — unplanned.** Nothing chartered. It
  builds the guided loop end to end on synthetic data to L2, and works out the
  usability evaluation criteria that score its own L2 claim.

- **`tools/build_orientation_block.py` defaults to `--ref main`,** which is a
  stale Real-Return-era branch in this repository. The live trunk is `main-ui`;
  pass it explicitly.

- **Filing is out of scope** for this phase (settled 2026-07-28). The phase ends
  at a complete, computed return.

- **Process changes, now in force.** A milestone gets one PR to open
  it and one to close it; tracks keep their review gate but no longer get their
  own PR. Phase documentation uses plain, product-facing language.

- **The phase-boundary legibility audit is still due.** It is owner-spawned by
  design; the foreman must not launch it.

- **The Real Return phase is closed** (owner decision, 2026-07-28). Its standing
  test is met and every cell of its maturity matrix is L3 or better. Read that
  narrowly: it was breadth- and hardening-limited by construction, and the owner
  still enters facts by hand-editing JSON. Legible Entry replaces the Real
  Return maturity matrix rather than extending it. Phase-close record:
  `docs/phases/real-return/real-return-roadmap.md`, "Phase close — 2026-07-28".

### Prior phase detail (Real Return)

- **Presentation — Completing the Row:** **complete 2026-07-28.** **The
  Presentation row is L3 across all five columns, and every cell in the maturity
  matrix is now L3 or better.**

  **There has been exactly one real viewing session in this project's history:
  2026-07-27.** It rendered all nine published lines and Schedule B Parts I and
  II in a single render. The W-2 wages (1a) column was recorded from it by the
  previous milestone; the other four were recorded a day later by an **amendment**
  in which the owner named the columns they observed. Nothing in the record
  asserts that five sessions occurred, or two. This is stated here, in the matrix
  header, in footnote 15, in the amendment, and in the retrospective, because a
  row filled in over two days by two milestones invites exactly that misreading
  and it is free to prevent now and impossible to correct later.

  A **records milestone** by design: no session, no browser, no real data, no
  code. Its one substantive act was asking the owner a question the repository
  cannot answer — which columns did you observe — and its one control was that a
  column not named would not move. All four were named, so the control did not
  fire, but it was real: ADR-0031 Decision 7's shape includes observing
  dispositions in quarantine, and no amount of rendering establishes that a
  person looked. **Observing a column is not auditing it**; L3 asserts the
  capability operated, per footnotes 7/11.

  Verified rather than inherited: the surface covers all five columns — the
  production-shaped fixture's sections and its Schedule B Parts I/II citation
  group, and `_resolve_attachment` projecting attachments into the model. The
  previous closeout also said "no build gap" and Track 1 then found three code
  defects, so this was checked directly.

  **Two gaps carry forward unclosed**, both needing a session this milestone did
  not perform: the **classified-refusal path has no human confirmation** — now
  the oldest open item on this path — and the **session runbook has an
  unidentified unclarity** reported by its first human user. Named in footnote 15
  so they are not lost with the row that carried them.

  Plan: `docs/phases/real-return/milestones/presentation-row-completion.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-07-28-presentation-row-completion.md`.

- **Presentation — Real Session and Attestation:** **complete 2026-07-27.**
  **Presentation moves L2 → L3 in the W-2 wages (1a) column** — the first
  maturity lift for the Presentation row, and the first time this project's
  human surface has run on the owner's real data. Three tracks on one branch,
  one PR at close.

  Track 1 was chartered as a *documentation* track — a session runbook plus a
  failure vocabulary that is mechanical rather than evaluative, because
  ADR-0047 precondition 5 forbids the owner from describing a defect they see
  during the real session. It found **three real code defects**, all in code the
  previous milestone had rehearsed clean: `LiveViewingError` was a sibling
  rather than a subclass of `PresentationSessionError`, so roughly a third of
  the reason-code table arrived as an uncaught traceback — the one text the
  vocabulary cannot describe; teardown's `except` was too narrow for its own
  promised code to be reachable; and Ctrl-C left an orphaned headed browser
  displaying the real return plus a `.live-view/session-*` directory holding
  that render's profile and disk cache, outliving a preflight guarantee that
  binds only at session *start*. **The durable lesson: a rehearsal's value is
  bounded by the set of endings it drives**, and the previous rehearsal drove
  the happy path and three designed refusals. All three fixes went into
  `open_presentation_session`, `launch`, and a context manager — **not** into
  the runbook template, because a guarantee living only in a copyable example
  silently no-ops when adapted. Five cycles: `748b8e8`, `50a9030` `NOT READY`,
  `894ff23`, `0f5e5dc` `NOT READY`, `36317be`, `9909cd6` `READY`.

  Track 2 (owner-operated) launched a real headed browser through the real path
  against a **synthetic** workspace and rendered the **product** page: clean
  pass, no page defects, and the first human confirmation of the interrupt
  repair. Its purpose was structural rather than cautious — the attestation is
  non-descriptive, so a defect seen during the real session arrives
  unactionable, and this track exists so the first real render is not also the
  real session. Track 3 performed the real session and the attestation in the
  same sitting.

  **Named gaps at close.** The classified-refusal path has **no human
  confirmation** — Track 2's browser-start-failure exercise was skipped, which
  its charter permitted. The runbook has an **unidentified unclarity** reported
  by its first human user, carried open rather than closed by guesswork. The
  other four Presentation cells stay **L2**: nothing technical separates them,
  the *record* does, and one attestation raises only what it covers.

  Plan:
  `docs/phases/real-return/milestones/presentation-real-session-attestation.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-07-27-presentation-real-session-attestation.md`;
  evidential basis: maturity-matrix footnote 14.

- **Presentation — Live Viewing Boundary and Invocation Vehicle:** **complete
  2026-07-26; plan PR #88, Track 1 PR #89 (`b37c536`), Track 2 PR #90
  (`bc0d8dc`).** The owner selected the Presentation frontier and the headed
  viewing shape, then directed a first-principles boundary check before any
  charter, explicitly to avoid repeating the Guarded Transport milestone. The
  check rejected the obvious vehicle-first shape: a headed browser confined by
  Chrome command-line flags is the same same-UID defect as the mode-600
  credential store, and ADR-0044 already forecloses it — naming directories and
  wrapping commands does not create a trust boundary. That is a claim about
  *flag-configured browsers*, not about the platform: no per-process network
  confinement has been selected, prototyped, or verified here, and the
  base-system Seatbelt facility remains an **unevaluated candidate rather than a
  foreclosed one**. The narrowing that made the milestone tractable: mechanical
  authority separation is the **L4** gate, while Presentation **L3** rests, like
  every existing L3 (footnote 7), on the synthetic battery plus a
  non-descriptive owner attestation under an accidental-leakage posture. The
  real question was therefore what the owner would be attesting to for a *human*
  surface — a case ADR-0044's process-oriented domains never contemplated.

  Track 1 ratified that as **ADR-0047 (Live Viewing Environment)**: a viewing
  session is an activity *within* the Live-Run Data domain, not a fifth domain,
  and every headed-browser channel falls into one of four classes. Two review
  cycles (`b1a630a`, `a476c40` `NOT READY`; `63c4102` `READY`) closed an
  unclassified clipboard-history precondition and the platform-impossibility
  overclaim noted above. Track 2 built the confined vehicle and fail-closed
  preflight (`d8083f9`); review `974bbac` returned `NOT READY` on a missing
  regression guard for the confirmed-absent clipboard case, repair `fa47e16`
  was verified against the exact mutation it exists to catch, and recheck
  `1ba2634` reproduced that mutation independently.

  **No maturity lift.** No real workspace was touched, no viewing session
  performed, no attestation made, and no enforcement substrate selected.
  Presentation remains L2 and the data boundary remains L3. Plan:
  `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-07-26-presentation-live-viewing-boundary.md`.

- **Presentation — L2 Integration Grounding:** **complete 2026-07-26; PR #86
  merged as `1f3bb9a` with CI `verify` green.** Boundary inspection corrected the prior “no
  further building” handoff before PR #82 merged. The first Builder then found
  that the demo manifest's fabricated line 2a and guard-inapplicable line 9
  cannot come from the resolved package and stopped with no code written. Track
  1 build `81c5504` now constructs and validates the renderer model inside a
  production-shaped synthetic `live_coordinate_run`, writes it below
  `LiveWorkspace`, and proves the golden through a dedicated
  production-shaped manifest. The unchanged demo manifest remains the full
  renderer-state regression floor. Review `e36086a` passed eight of nine
  measurements and found one gap: a projector rejection through
  `live_coordinate_run` can strand reserved result/presentation artifacts.
  The plan's one findings-only repair landed as `759c9fa`: projection now
  precedes durable output writes, both reserved artifacts are removed on
  `PresentationModelError`, and a coordinator-level regression exercises the
  failure. Focused recheck `4a74ffd` returned `READY` with all six measurements
  passing. Maturity-matrix footnote 5 now records the durable handoff: the
  surface contract, renderer, coordinator projection, and strict internal input
  are synthetic-end-to-end; the browser path remains synthetic-only, and no
  real operation occurred. A later Presentation L2→L3 milestone must select and
  verify a data-boundary-safe live invocation vehicle before a real exercise;
  this milestone selects neither. Fresh completion review `7f6ae79` returned
  `READY`.
  Plan:
  `docs/phases/real-return/milestones/presentation-l2-integration-grounding.md`.
  Current prompt:
  `docs/phases/real-return/milestones/presentation-l2-integration-grounding.md`.

- **Live-Run System Definition and Trust Domains:** complete; ADR-0044 accepted
  as a positioning contract; closure PR #61 **merged**. It selects and schedules
  no enforcement mechanism, makes no L4 claim.
- **Presentation Exploratory Milestone:** complete 2026-07-24. An **exploratory
  milestone (no ADR, no matrix cell raised)** — studied developing/evaluating UI
  under agent-authored, agent-reviewed, owner-light constraints, using a synthetic
  citation-walk surface. Five 2-builder/2-reviewer cycles. Finding: developable
  via a demonstrated loop; ~65–80% of UI quality is agent-mechanizable. Main
  artifact = seven evaluation-analysis documents at
  `docs/prototypes/human-presentation-citation-walk/analysis/` (cycle log +
  process in the sibling `plan.md`; reference prototypes/fixtures/harness-seed
  under `reference/`; retrospective pointer
  `docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md`).
  Raising the Presentation matrix aspect for real remains a well-formed but
  **unselected** decision prototype.
- **Presentation Evaluation Process Economy:** closed early by owner direction
  2026-07-25. Track 0 merged in PR #66 (`870c8ed`) and is the accepted
  foundation: strict presentation workload/observation/comparison contracts,
  the source-faithful historical baseline, participating-role completeness,
  and quality-before-cost comparison. Track 1's independent review returned
  `NOT READY` on tuple storage leakage, false-pass malformed injection,
  launch-time cleanup leakage, path/provenance traversal, incomplete strict
  validation, and rejected-input echo. Its implementation was not merged; the
  prepared repair/re-review and Tracks 2–3 were retired. The review trace
  reported 42 turns, 41 tool calls, 12 harness invocations, 11 Chrome launches,
  batched browser execution, several very large context reads, and unknown
  total token use. The retrospective records the owner disposition and the
  promoted foreman discipline: give known adversarial classes to both Builder
  and Reviewer as executable coverage, and spend independent review on an
  explicit novel boundary.
- **Browser Evaluation Runner Completion:** complete. PR #71 merged as
  `c329afd` on 2026-07-25T23:12:23Z with CI `verify` green on the merge
  commit. It adopted the existing, independently reviewed implementation
  rather than rebuilding it and repaired the six known blockers: storage
  isolation, injection acknowledgement, cancellation-safe cleanup, canonical
  path/provenance confinement, strict non-vacuous validation, and redacted
  external failures. The focused delta Reviewer returned `READY` for F1–F6
  and the transferred measurements. Voluntary post-verdict exploration then
  found residual R1: the repair's injection-acknowledgement wait could
  bypass the manifest timeout and still return a pass; R2 recorded the fixed
  acknowledgement marker's collision fragility. The owner accepted both
  findings and authorized one narrow R1/R2 repair charter plus its focused
  recheck as an explicit exception to the original cap. The residual repair
  landed, and the focused R1/R2 recheck returned `READY` with no new in-scope
  finding. No broader second review cycle was authorized. Retrospective:
  `docs/milestone-retrospectives/2026-07-25-browser-evaluation-runner-completion.md`.
- **Presentation — Citation Walk on Real Derivation Output:** **complete
  2026-07-26.** PR #77 merged as `2d4c195` with CI `verify` green on the merge
  commit; that merge is the milestone's end boundary. ADR-0046 (Presentation
  Surface Contract) ratifies the Presentation Exploratory Milestone's
  five-cycle convergence directly from existing evidence, resolving its three
  open rule-points: derived/diagnostic values are zero-authority; rejected
  values are blanket-redacted, never echoed; blocked-state salience is
  section-level. Track 1 shipped the renderer over `form-field.v3` /
  `act-derived-publication.v1` fixtures across all five disposition kinds plus
  the standardized T1–T3 fault cases, driven by a browser evaluation runner
  manifest. Its review gate returned **`NOT READY`** on two independent
  zero-authority failures — F1 (`computed_zero`/`closure_backed_zero` rendered
  a numeric value with no citation, because the renderer read only
  `citationSites` and never `field.citation`) and F2 (diagnostic eligibility
  checked disposition kind but not that the resolved value was a finite
  number). The repair closed exactly those two, and the focused recheck
  returned **`READY`** with no new ADR-0046 violation and directly touched
  invariants intact; the manifest now carries 26 criteria (23 original + 3
  proving F1/F2 closed). Track 2 filed the retrospective and moved the
  maturity-matrix Presentation cell **L3 → L2** (owner-confirmed): L2 is
  synthetic end-to-end, and Track 1's charter scoped it to synthetic fixtures,
  so the prior L3 mark was a footnote-qualified overstatement. Its retrospective
  then characterized the remaining work as one real exercise with no further
  building; the current L2 Integration Grounding plan corrects that conclusion
  after inspecting the renderer, harness, and coordinator boundaries.
  Retrospective:
  `docs/milestone-retrospectives/2026-07-26-presentation-citation-walk.md`.
  The accepted economy contracts remain available but were not this
  milestone's subject.
- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Pointers

Active phase: **Legible Entry** — `docs/phases/legible-entry/`. Roadmap and
current prompt: `docs/phases/legible-entry/legible-entry-roadmap.md`. Milestone
selection in this phase follows the proposed sequence in that roadmap; the
instrument is the entry-loop matrix described there, which replaces Real
Return's rather than extending it.

Prior phase: **Real Return** — closed 2026-07-28,
`docs/phases/real-return/real-return-roadmap.md` ("Phase close — 2026-07-28").
Foundation before it: `docs/phases/foundation/foundation-roadmap.md`. Their
milestone-by-milestone history lives in those roadmaps, the milestone plans, the
retrospectives under `docs/milestone-retrospectives/`, and Git — the detail
below is kept only where it bears on work still ahead.

Completed in this phase:

- **The Entry Boundary** — closed 2026-07-28, PR #102 at `c451a40`. ADR-0048
  accepted. Plan:
  `docs/phases/legible-entry/milestones/entry-boundary.md`; retrospective:
  `docs/milestone-retrospectives/2026-07-28-entry-boundary.md`.
- **Packaging the Surface** — closed 2026-07-28, PR #108 at `2fb6761`. ADR-0049
  proposed. Plan:
  `docs/phases/legible-entry/milestones/packaging-the-surface.md`; retrospective:
  `docs/milestone-retrospectives/2026-07-28-packaging-the-surface.md`; charters
  `docs/reviews/charter-2026-07-28-packaging-the-surface-track{1,2}.md` and
  reviews `docs/reviews/2026-07-28-packaging-the-surface-track{1,2}-review.md`,
  both READY.

**➡️ Next action: the owner selects the next milestone.** Nothing is chartered.
The roadmap's sequence puts **The Entry Loop, synthetic** next — build the
guided loop end to end on synthetic data, and work out the usability evaluation
criteria that score its own L2 claim. That is a proposal, not a commitment.

Two things are outstanding and are the owner's, not the foreman's: **ADR-0049 is
proposed and awaits ratification**, and the **phase-boundary legibility audit is
due** and is owner-spawned by design.

The Real Return milestone-by-milestone chain that used to be listed here is
retained in "Prior phase detail (Real Return)" above, in each milestone's plan
and retrospective, and in Git. Two of its items are still open and follow into
this phase: the **classified-refusal path has never been confirmed by a human**
(the oldest open item on this path; it needs a session to close), and the
**session runbook has an unidentified unclarity** — whoever uses it next should
note where it reads badly at the moment it reads badly.

The four owner constraints from that milestone remain in force as a standing
posture, and all four are the same constraint from different sides: **this
repository does not author its own boundary enforcement.** No confinement code —
the `sandbox-exec` profile is owner-held outside the supply chain. No probes —
`PreflightProbes` stays an injected input defaulting to `UNKNOWN`; nothing here
reads backup state, indexing state, or the process table. No locator in any
surface: server logs, request paths, subprocess arguments, diagnostics, test
names. And `sandbox-exec`'s deprecation is a named, owner-accepted residual, not
a blocker.

Both `track/presentation-citation-walk-track1` and
`track/browser-evaluation-runner-completion` may be deleted; their content is
fully contained in `main` at `2d4c195` and `c329afd` respectively.

Standing operational notes: `PROJECT_PLANNING.md` ("Branch, PR, and Merge Protocol") governs per-track PRs, owner merges, and `main` as the continuous ratified record; `AGENTS.md` ("Dispatch authorization") governs dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history lives in its milestone plan, retrospective, and git history. The Dividends and Schedule B Slice's track-by-track history (D1/D2/D3 ratification, Tracks 0/0a/1–4, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.

## Durable pointers

- Track 0 independent review:
  `docs/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`.
- Track 0 participant-cost repair charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair.md`.
- Track 0 participant-cost repair delta-review charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair-review.md`.
- Track 1 instrumented harness core charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core.md`.
- Track 1 harness-core review charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core-review.md`.
- Completed Track 1 harness-core review (`NOT READY`):
  `docs/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`.
- Interrupted Track 1 review progress:
  `docs/reviews/2026-07-25-presentation-economy-t1-harness-core-review-progress.md`.
- Reactivated existing-runner repair Builder charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`.
- Prepared focused post-repair delta-review charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair-review.md`.
- Citation-walk Track 1 build charter:
  `docs/reviews/charter-2026-07-25-presentation-citation-walk-track1.md`.
- Citation-walk Track 1 review-gate charter:
  `docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-review.md`.
- Completed citation-walk Track 1 review (`NOT READY`, F1/F2):
  `docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md`.
- Citation-walk Track 1 repair charter (executed, F1/F2):
  `docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair.md`.
- Citation-walk Track 1 repair recheck charter:
  `docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair-review.md`.
- Completed citation-walk Track 1 repair recheck (`READY`):
  `docs/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md`.
- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Operating rules: `AGENTS.md` and `PROJECT_PLANNING.md`. Process is not in the
  ADR corpus (ADR-0045); `docs/adr/INDEX.md` routes product contracts only.
- Grounding economy analysis:
  `docs/prototypes/human-presentation-citation-walk/analysis/04-economy.md`.
- Accepted decision: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`.
- Live-run system-definition plan:
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`, with
  review `docs/reviews/2026-07-23-live-run-system-trust-domains-adr-review.md`
  and retrospective
  `docs/milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md`.
- Completed-milestone lessons: `docs/milestone-retrospectives/`.
- Presentation UI/UX process experiment (preserved findings + reusable
  agent-driven-UI method recipe): `docs/prototypes/human-presentation-citation-walk/plan.md`.
