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

Active milestone: **Dividends and Schedule B Slice** — plan approved by the
owner 2026-07-18 (plan: `milestones/dividends-schedule-b-slice.md`). Raises
the Dividends and Schedule-attachments matrix columns L0→L3; decision topics
D1 (attachment ontology, Tier 3), D2 (line 16 under qualified dividends,
Tier 3, owner-narrowed to the declared-absence worksheet), D3 (1099-DIV
composition, Tier 2). Track 0 (prototype topics) is next; each prototype
plan requires owner approval before its first charter (ADR-0013).

- Dividends and Schedule B Slice — **active** (approved 2026-07-18).

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
