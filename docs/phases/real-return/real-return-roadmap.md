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
