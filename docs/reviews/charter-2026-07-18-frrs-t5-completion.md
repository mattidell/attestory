# Charter: Track 5 — First Real Return Slice Completion Records

Date: 2026-07-18. Owner-directed unit ("charter and build"), implemented by
the foreman in-session (no sub-agent dispatch; ADR-0034 satisfied by direct
owner instruction). Branch: `track/frrs-t5-completion`. The owner holds the
merge; the pre-merge review seat is owner-dispatched per ADR-0034 from the
prepared review charter.

## Origin

The milestone plan names Track 5 as the completion track: "maturity-matrix and
phase-state updates, retrospective, deferral ledger. No single milestone merge
— completion is a records track, itself reviewed and merged." Its trigger — the
owner's quarantined real run — occurred 2026-07-18; the non-descriptive
attestation is recorded in the milestone plan's Verification section (PR #20).

## Deliverables

1. **Maturity matrix update** (`docs/phases/real-return/maturity-matrix.md`):
   data-boundary row L0→L3 across covered domains; covered L2 cells raised to
   L3 per the milestone plan's pre-committed claim; footnotes corrected where
   the milestone discharged them (W-2 closure mapping, production resolver);
   an explicit note that L3 claims rest on the non-descriptive attestation
   plus the synthetic battery — never on quarantine detail (Ontology §8).
   Fresh frontier reading for the owner's next milestone selection.
2. **Roadmap status** (`docs/phases/real-return/real-return-roadmap.md`):
   milestone completion recorded.
3. **Milestone plan closure** (`milestones/first-real-return-slice.md`):
   per-criterion exit disposition, each stated in the strongest form the data
   boundary admits.
4. **Deferral ledger**
   (`milestones/first-real-return-slice-deferral-ledger.md`): every named
   deferral this milestone created or re-affirmed, with origin, reason, and
   reactivation trigger — nothing silently closed.
5. **Retrospective**
   (`docs/milestone-retrospectives/2026-07-18-first-real-return-slice.md`).
6. **Phase-state briefing rewrite** (`docs/phase-state.md`) at the milestone
   boundary per that file's contract, and handoff update.

## Scope fence

Records only: no code, no schema, no content, no test, no tool changes. No
quarantine detail of any kind — the attestation sentence is the only fact
about the real run any record may carry; the pre-flight support interaction is
described only at the error-class level already recorded on `main`. No new
deferral may be *retired* here (retirement is future milestone work); the
ledger only records. Next-milestone selection is owner-directed (Tier 3) and
expressly out of scope — the matrix presents frontiers, not a decision.

## Verification

Full `.venv/bin/python3 -m unittest`; `-m mypy packages tools tests`;
`tools/governance_lint.py`; `tools/envelope_scan.py --range origin/main..HEAD`
over the track branch. All must be green before the review seat is requested.

## Review

A prepared companion charter
(`charter-2026-07-18-frrs-t5-completion-review.md`) assigns an
author-independent reviewer to verify: records match git/`main` reality; the
matrix claims match the milestone plan's pre-committed raises and carry the
Ontology §8 qualification; the ledger is complete against the named-deferral
trail in the track reviews and ADRs; no record carries quarantine detail; and
the verification battery is green. The owner dispatches it (ADR-0034) and
holds the merge.
