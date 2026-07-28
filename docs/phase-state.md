<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Real Return",
  "topic": "presentation-real-session-attestation",
  "active_plan": "docs/phases/real-return/milestones/presentation-real-session-attestation.md",
  "status": "Presentation — Real Session and Attestation is PLANNED, 2026-07-27, selected by the owner from maturity-matrix frontier 1. Three tracks. Target: Presentation L2 → L3 in the W-2 wages (1a) column ONLY; the owner named that column at plan stage and the other four Presentation cells stay L2 by design. Track 1 (agent-built) produces a session runbook and a bounded non-descriptive failure vocabulary — mechanical, never evaluative — because ADR-0047 precondition 5 forbids the owner from describing a defect they see during the real session, which would otherwise make it unactionable. Tracks 2 and 3 are owner-operated on the owner's machine in one sitting, with a hard gate between them: Track 2 launches a real headed browser and renders the PRODUCT page against a synthetic workspace, closing both rehearsal gaps where defects are still describable; Track 3 performs the real session and attestation only if Track 2 cleanly passed. No agent launches a headed process. The prior milestone is CLOSED: all four tracks complete, no maturity row moved, Presentation at L2 and one owner act from L3. Track 2's two findings are the durable lesson — an unauthenticated loopback socket carrying the whole presentation model, and the evaluation fixture page telling the owner their real data was synthetic — both living in the join between correct components rather than inside either one. Two rehearsal gaps stand before the real session: no real browser has ever been launched by this path, and the product page has never been rendered by one. Presentation — Live Viewing Boundary is CLOSED at 805225e. The owner accepts a permanent L3 ceiling on the data-boundary row: ADR-0044 line 164 states that only a selected enforcement substrate plus a mechanical showing can support an L4 data-boundary claim, footnote 8 faithfully summarises that ratified Tier 3 decision, and the cell is a deliberate ceiling rather than an unfinished task. The owner holds BOTH live-run confinement (sandbox-exec, evaluated from first principles: helper-process network denial works when the top-level process is confined; sandbox escape is not possible absent a kernel zero-day; the interface is deprecated and SBPL is unstable across macOS releases, both accepted as named residuals) AND workstation-precondition observation in their own trust domain, outside the project supply chain. Neither belongs in this repository. The Presentation — Live Session Path plan (four tracks) merged as PR #92 at b777a10; all four tracks then completed on one branch and reached main as a single milestone PR. Track 1 (ADR-0047 amendment placing Class C confinement and Class D precondition observation in the owner's trust domain) returned READY on independent review. Track 2 (session entry point and model serving) returned NOT READY on the two findings above and was repaired: a 256-bit per-session route compared with hmac.compare_digest, and a fail-closed refusal to serve any page declaring synthetic provenance, with the citation-walk renderer forked to a product location at packages/presentation/pages/citation-walk.v1.html. Track 3 rehearsed the whole path against synthetic inputs; Track 4 filed the records. PR cadence is one PR at close, not one per track (owner direction, 2026-07-27), and a PR branch carries its post-merge state. Plan merged as PR #95 at ec6972b. Track 1 is CHARTERED at docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1.md: runbook plus vocabulary in one new file docs/runbooks/presentation-real-session.md, with one open question the builder must answer with a recommendation rather than silently — how the owner supplies the residency locator without putting it in shell history or the process table, which is the same hazard that killed the tmutil probe last milestone. Track 1 BUILT at 748b8e8: docs/runbooks/presentation-real-session.md, 365 lines, no code changed — open_presentation_session already runs as one act so the scriptability repair was declined. The builder recommends an interactive input() prompt for the locator over argv, env var, or file, and names it as partial closure rather than full. Track 1 review is CHARTERED at docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-review.md, independent by design: the foreman wrote the plan and build charter where the mechanical-versus-evaluative line was drawn, so a foreman review could test the builder's execution of that line but not the line itself. Independent review returned NOT READY at 50a9030 with five findings, two blocking. Finding 1 is a verified code defect, not a doc defect: LiveViewingError is a sibling of PresentationSessionError rather than a subclass, so roughly a third of the runbook's own reason-code table propagates as an uncaught traceback — the one text the vocabulary cannot describe. Finding 2: the prose promises an interactive input() locator prompt while the script derives it from the script's own position, so the open-question essay analyses a mechanism the artifact does not use, and the mechanism it does use has an unstated 'never invoke with a path argument' rule. Repair CHARTERED at docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-repair.md, directing the finding-1 fix into open_presentation_session itself rather than into the runbook's template, because a guarantee living only in an example no-ops the moment the owner retypes it — the third appearance of this project's fail-open drift class. Repair BUILT at 894ff23 across the runbook, live_session.py, and its test module. Finding 1 fixed at source: a _classified_viewing_failure helper wraps LiveViewingError into presentation-viewing-refused forwarding only the stable sub-code, and anything else into presentation-viewing-failed with detail dropped, since an arbitrary exception message is exactly the surface ADR-0047's locator confinement keeps closed. The builder agreed with the foreman on finding 2 rather than overturning, and went beyond the findings twice, flagging both: BaseException is deliberately left unclassified so Ctrl-C is not relabelled a refusal, and teardown's catch was broadened because 'teardown did not complete' is legal vocabulary only if incomplete teardown actually arrives as that code. Focused recheck CHARTERED at docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-recheck.md, reviewing those two unrequested changes as new work rather than on the builder's account of them. Recheck returned NOT READY at 0f5e5dc: all five prior findings close the failure named rather than the sentence written, and finding 1's guarantee was verified to hold by construction (every LiveViewingError site passes a ViewingReason enum member, so only fixed authored strings cross). Teardown broadening accepted. But the BaseException decision, correct in itself, left its consequence uncovered and the reviewer demonstrated it empirically: Ctrl-C leaves an orphaned headed browser still displaying the real return plus a .live-view/session-* directory holding the browser profile and the disk cache of that render. The preflight refuses on backup and indexing at session START, so residue outliving the session outlives that guarantee. Second repair CHARTERED at docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-repair2.md, fixing it structurally in launch, in open_presentation_session, and by making the session a context manager — NOT by adding try/finally to the runbook template, which is the same fail-open drift this track has now hit twice. Also closes the __context__ locator-retention residual and the _close_quietly socket-survival residual. Second repair BUILT at 36317be. Interrupt teardown fixed in three places: an _abandon_launch extraction so launch's BaseException path releases process and session directory (and so a future fourth handler inherits it), a viewing hoist closing the window between launch returning and open_presentation_session returning where the browser is live and owned by nobody, and the template switched to `with` — LivePresentationSession already had __enter__/__exit__, so the missing half was always the template, which the builder flagged honestly rather than claiming the test as evidence. __context__ residual closed non-obviously: `raise X from None` re-attaches __context__ at raise time regardless of construction, so the classified error is now raised after the handler exits with sys.exc_info() clear. _PresentationServer.close runs server_close() in a finally. Two judgment calls left open and named: best-effort teardown is invisible on failing paths, and __exit__ raising would mask an in-flight KeyboardInterrupt. Full suite 670 tests OK. Second recheck CHARTERED at docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-recheck2.md, which asks the reviewer to confirm by running rather than reading, and explicitly authorises returning READY with an honest residual rather than spending a third cycle on something that was never going to close. Second recheck returned READY at 9909cd6 with named residuals. The reviewer re-measured the interrupt path against real launch rather than a test double, checked the builder's pre-fix test claim instead of accepting it (three fail, one passes — the with-block guard, exactly as flagged), and confirmed __context__ is cleared rather than hidden. Bonus not claimed by the builder: except BaseException in launch also catches Exception subclasses the two narrow handlers missed, so an AttributeError there now tears down AND arrives classified. The __exit__/KeyboardInterrupt tension resolves: that __context__ is provably locator-free because close() swallows the path-bearing OSError and constructs a fresh exception — true by close()'s structure rather than by an explicit invariant, so recorded as reasoning. One residual, an overstated Step 3 bullet claiming library-level teardown for Ctrl-C at the prompt when that is a property of `with`, was corrected by the FOREMAN directly after review rather than in a third build cycle; recorded in the recheck record because no independent reader has seen that edit. TRACK 1 COMPLETE. Track 2 CHARTERED at docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track2.md and is OWNER-OPERATED — no agent performs it and no agent launches a headed process. Next action: the owner runs the rehearsal against a synthetic workspace; Track 3 does not begin unless it passes cleanly.",
  "current_role": "Track 2 Builder (owner-operated rehearsal; no agent performs this track)",
  "current_prompt": "docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track2.md"
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

**Shims in place.** E8.1 UI coverage partially met — a citation-walk renderer now exists and satisfies ADR-0046 end to end, but only over **synthetic** fixtures (maturity L2); it has never been exercised against a real resolved run, and no other form or schedule has a human surface. Mechanical separation between Developer/Supply and Live-Run Data **not implemented**, which holds the data-boundary row at L3; guarded publication transport / credential confinement also not implemented, as a separate publication-integrity deferral; a synthetic push-envelope posture audit makes the hook/`--no-verify` bypass visible but does not protect an owner push; ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment; `closed-on-attestation` reaches only fact types keyed identically to their gate fact type, not yet differently-keyed per-item facts. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md` (which also dispositions the Dividends and Schedule B Slice ledger's entries this milestone touched — two, both retired).

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

## Current state (2026-07-26)

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

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Most recent completed milestone: **Presentation — L2 Integration Grounding** —
complete 2026-07-26. PR #86 merged as `1f3bb9a` with CI `verify` green.
The durable Presentation handoff is maturity-matrix footnote 5 in records
commit `8e29b52`; completion review `7f6ae79` is `READY`. Presentation remains
L2, and no next milestone is selected.
Plan:
`docs/phases/real-return/milestones/presentation-l2-integration-grounding.md`.
Current prompt:
`docs/phases/real-return/milestones/presentation-l2-integration-grounding.md`.
Retrospective:
`docs/milestone-retrospectives/2026-07-26-presentation-l2-integration-grounding.md`.

Prior completed milestone: **Presentation — Citation Walk on Real
Derivation Output** — complete 2026-07-26. PR #77 merged `2d4c195` with CI `verify` green
on the merge commit. Ratified ADR-0046 (Presentation Surface Contract), shipped
the citation-walk renderer over synthetic `form-field.v3` /
`act-derived-publication.v1` fixtures through one review gate (`NOT READY` on
F1/F2), one repair, and one focused recheck (`READY`), and moved the
maturity-matrix Presentation cell L3 → L2. Its original closeout framed the
next step as one real exercise; the current milestone corrects that handoff
without rewriting the completed implementation record. Plan:
`docs/phases/real-return/milestones/presentation-citation-walk.md`. Decision
record: `docs/adr/0046-presentation-surface-contract.md`. Retrospective:
`docs/milestone-retrospectives/2026-07-26-presentation-citation-walk.md`.

Prior milestone: **Browser Evaluation Runner Completion** — complete
2026-07-25. PR #71 merged `c329afd` with CI `verify` green on the merge
commit. Adopted and repaired the existing browser-evaluation runner
implementation (six blockers plus two owner-accepted residuals, R1/R2); no
product UI, ADR, or matrix lift. Plan:
`docs/phases/real-return/milestones/browser-evaluation-runner-completion.md`.
Retrospective:
`docs/milestone-retrospectives/2026-07-25-browser-evaluation-runner-completion.md`.

Earlier milestone: **Presentation Evaluation Process Economy** — closed early by
owner direction 2026-07-25. Track 0 merged in PR #66 (`870c8ed`) as the
accepted economy foundation. Track 1 failed independent review and was not
merged; its repair/re-review and Tracks 2–3 were retired. Plan:
`docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`.
Retrospective:
`docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md`.

Earliest of this run: **Presentation Exploratory Milestone** — complete
2026-07-24; no ADR or matrix lift. Its evaluation analysis and reference
material live under `docs/prototypes/human-presentation-citation-walk/`.

**➡️ Next action:** the **owner milestone-selection frontier**. Presentation —
Live Session Path is closed; nothing is chartered. The foreman's job is to read
`docs/phases/real-return/maturity-matrix.md` and present candidates. Selection is
owner-held.

**What stands between Presentation L2 and L3 is one owner act, not a build.** A
real viewing session plus the non-descriptive attestation under ADR-0047's five
honesty preconditions. The path now exists end to end and has been rehearsed
against synthetic inputs, so the act is short. Two gaps remain, and both are of
the same kind — nothing has been exercised by a real browser:

1. **No real browser has ever been launched by this path.** The rehearsal used a
   stub; only the loopback-URL validation and the launch-failure path were
   covered for real.
2. **The product page has never been rendered by one.**
   `packages/presentation/pages/citation-walk.v1.html` is backed only by a
   normalized diff against the evaluation fixture page and a `node --check`.

Both close on the first real session, which is therefore also the first real
render. Do not record Presentation as L3 on the strength of the vehicle
existing.

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
