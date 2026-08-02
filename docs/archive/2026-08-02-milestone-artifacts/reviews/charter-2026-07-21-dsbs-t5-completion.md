# Charter: Track 5 — Dividends and Schedule B Slice Completion Records

Date: 2026-07-21. Owner-directed unit ("charter and build"), implemented by
the foreman in-session (no sub-agent dispatch; ADR-0034 satisfied by direct
owner instruction). Branch: `track/dsbs-t5-completion`. The owner holds the
merge; the pre-merge review seat is owner-dispatched per ADR-0034 from the
prepared review charter.

## Origin

The milestone plan names Track 5 as the completion track: "Matrix,
phase-state, retrospective, deferral ledger; itself reviewed and merged as a
records track." Its trigger — the owner's quarantined real 1099-DIV run — is
recorded in the milestone plan's Verification section (`dividends-schedule-b-slice.md`,
"Owner attestation (recorded 2026-07-21)", merged PR #40, `4f0645c`/`c971e30`):
non-descriptive attestation ("I ran in quarantined workspace, dispositions
were observed there, no artifact crossed the boundary"), package pinned at
`core-calculations` v6, one intervening stale-pin repair reproduced
structurally from committed fixtures with no live detail crossing.

## Deliverables

1. **Maturity matrix update** (`docs/phases/real-return/maturity-matrix.md`):
   Dividends (3a/3b) and Schedule-attachments columns raised per the
   milestone plan's exit criterion 6 — L0→L3 across the aspects the slice
   exercises (3a/3b publication, line 9 dividend absorption, Schedule B
   existence/Part I/II/III, line 16 under D2), with honest footnotes for any
   aspect the slice did not exercise; an explicit note that L3 claims rest on
   the non-descriptive attestation plus the synthetic battery — never on
   quarantine detail (Ontology §8). Fresh frontier reading for the owner's
   next milestone selection.
2. **Roadmap status** (`docs/phases/real-return/real-return-roadmap.md`):
   milestone completion recorded.
3. **Milestone plan closure** (`milestones/dividends-schedule-b-slice.md`):
   per-exit-criterion disposition (the six criteria in that file's "Exit
   criteria" section), each stated in the strongest form the data boundary
   admits, citing the merged track PRs (#30/#31/#32/#36/#39/#40) and ratified
   ADRs (0035–0038).
4. **Deferral ledger**
   (new file, `milestones/dividends-schedule-b-slice-deferral-ledger.md`,
   sibling to the First Real Return Slice ledger): every named deferral this
   milestone created or re-affirmed — declared universe exclusions (2a/3/5/7/12
   dividend boxes named in the milestone plan), any shim carried forward from
   the First Real Return Slice ledger this milestone touches, and anything
   named as future work in the track reviews — with origin, reason, and
   reactivation trigger. Nothing silently closed.
5. **Retrospective**
   (`docs/milestone-retrospectives/2026-07-21-dividends-and-schedule-b-slice.md`):
   what shipped, the D1/D2/D3 prototype-and-ratification arc, promoted
   lessons (candidates: charter authoritative-surface golden class as a
   standing requirement already promoted from FRRS and reconfirmed here;
   D2's mid-milestone missing-ratification catch and repair; the shared-refs
   git race from Track 4's handoff note), any lesson worth promoting to
   standing process.
6. **Phase-state briefing rewrite** (`docs/phase-state.md`) at the milestone
   boundary per that file's contract (what it does now / shims / next
   milestone / pending contract change), and a handoff update recording the
   milestone as closed and next-milestone selection as owner-directed
   (Tier 3), open.

## Scope fence

Records only: no code, no schema, no content, no test, no tool changes. No
quarantine detail of any kind — the attestation sentence already recorded in
the milestone plan is the only fact about the real run any record may carry;
no further description crosses. No new deferral may be *retired* here
(retirement is future milestone work); the ledger only records. Next-milestone
selection is owner-directed (Tier 3) and expressly out of scope — the matrix
presents frontiers, not a decision.

## Verification

Full `.venv/bin/python3 -m unittest`; `-m mypy packages tools tests`;
`tools/governance_lint.py`; `tools/envelope_scan.py --range main..HEAD` over
the track branch. All must be green before the review seat is requested
(records-only changes should not move these, but the floor still applies).

## Review

A prepared companion charter
(`charter-2026-07-21-dsbs-t5-completion-review.md`) assigns an
author-independent reviewer to verify: records match git/`main` reality
(track PRs, ADR ratifications, the attestation record); the matrix claims
match the milestone plan's exit criteria and carry the Ontology §8
qualification; the ledger is complete against the named-deferral trail in the
track reviews, ADRs, and the milestone plan's declared-exclusion list; no
record carries quarantine detail beyond the already-recorded attestation
sentence; and the verification battery is green. The owner dispatches it
(ADR-0034) and holds the merge.
