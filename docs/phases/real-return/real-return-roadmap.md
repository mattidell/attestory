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

Active milestone: **First Real Return Slice** — **active; Tracks 0–3 and the
Track-3 F1 repair are merged, and Track 4 is reviewed merge-ready awaiting
owner merge**
(plan: `milestones/first-real-return-slice.md`).

- First Real Return Slice — **active** (2026-07-18). D1 residency (ADR-0031),
  D2 contribution (ADR-0032), and D3 production resolver (ADR-0033) are
  ratified; Tracks 1–3 plus the reviewed Track-3 F1 repair are merged. Track 4
  now has repaired the immutable core package, added W-2 closure mapping, and
  connected the capability-gated synthetic live path. Its reviewed PR awaits the
  owner merge; the owner alone then contributes real W-2 / 1099-INT facts and
  runs the slice in quarantine. The repository continues to carry no personal
  data.
