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

## Status

- Presentation — L2 Integration Grounding — **Track 1 `READY`; Track 2 records
  prepared for completion review (2026-07-26).** Boundary inspection corrected the initial PR #82 plan before
  merge: the current renderer begins with a hand-shaped synthetic model, the
  coordinator does not persist the inputs needed to construct it, and the
  browser harness is intentionally synthetic-only. Track 1 closes that
  coordinator-to-model gap on production-shaped synthetic data. Its first
  Builder stopped cleanly when the existing demo manifest proved impossible to
  satisfy from resolved content: line 2a is not modeled and real line 9 is not
  guard-inapplicable. The amended charter keeps that manifest unchanged as the
  renderer regression floor and adds a dedicated production-shaped manifest
  for the regenerated golden. Track 1 build `81c5504` received one independent
  `NOT READY` review (`e36086a`), one focused repair (`759c9fa`), and a `READY`
  recheck (`4a74ffd`). Track 2 records the six-row capability-state handoff in
  maturity-matrix footnote 5. It makes explicit that no live browser invocation
  vehicle or real operation exists; the synthetic harness is not that vehicle.
  Presentation remains L2; no next milestone is selected. Plan:
  `milestones/presentation-l2-integration-grounding.md`.

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
