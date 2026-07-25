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

- Presentation Evaluation Process Economy — **active; owner-approved planning
  unit merged in PR #65 (`1fd3d4c`) on 2026-07-24; Track 0 independent review
  returned `NOT READY` on participating-role cost completeness; the focused
  repair Builder is the current role.** This
  process milestone follows the
  Presentation Exploratory Milestone's economy analysis. Its durable capability
  is a quality-adjusted learning loop scoped specifically to UI/UX presentation
  iteration, development, and review: versioned presentation workloads,
  observations, and comparisons; a source-faithful historical baseline; and a
  bounded same-work pilot for evaluating presentation treatments without
  calling cheaper-but-worse work an improvement. Its first intervention turns
  recurring CDP/browser checks into one dependency-free offline batch harness,
  reuses one isolated browser session across a criteria × fixture × candidate ×
  tamper matrix, promotes a standing synthetic corpus and example templates,
  and tier-matches each implementation/review seat. The milestone evaluates
  presentation work and makes no economic claim about non-presentation
  workflows. It adds no product UI, ADR, or maturity-matrix lift. Plan:
  `milestones/presentation-evaluation-process-economy.md`.

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
