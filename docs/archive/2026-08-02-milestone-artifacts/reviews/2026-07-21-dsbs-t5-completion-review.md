# Review: Track 5 Completion Records — Dividends and Schedule B Slice

Date: 2026-07-21. Author-independent pre-merge review of
`track/dsbs-t5-completion` against `main`, per
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-21-dsbs-t5-completion-review.md`. This review
reads only the charters, the branch diff (`git diff main..track/dsbs-t5-completion`),
and committed repository history — not the authoring session.

## Verdict: **NOT READY**

One blocking finding (F1) — a real, mechanical violation of the charter's
own check 2 requirement. All other checks pass. F1 is narrow and cheap to
fix (footnote additions to three matrix rows); it does not implicate the
underlying claims, the ledger, the boundary, or the verification battery.

## Scope fence (check 0)

`git diff main..track/dsbs-t5-completion --stat` touches only: `docs/foreman-handoff.md`,
`docs/phase-state.md`, `docs/phases/real-return/maturity-matrix.md`,
`docs/phases/real-return/real-return-roadmap.md`,
`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md` (Closure
section appended), the new
`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md`,
the new `docs/milestone-retrospectives/2026-07-21-dividends-and-schedule-b-slice.md`,
and the two Track 5 charters. `git diff --stat -- '*.py' '*.json' packages
tools tests` against the same range is empty. **Pass** — records only, no
code/schema/content/test change.

## Check 1 — Reality

Spot-checked every PR/SHA/ADR citation the delta introduces against `git
log --oneline --all` and `docs/adr/`:

- PR #30 → `6f303fe` (Track 0a), #31 → `a870a2f` (Track 1), #32 → `c39c6c7`
  (Track 2), #36 → `e25cc11` (Track 3), #39 → `e15bd39` (Track 4), #40 →
  `c971e30`/`4f0645c` (owner attestation). All six merge commits exist with
  matching branch names and PR numbers. **Match.**
- ADR-0035: `Status: accepted (owner ratification 2026-07-18...)`. ADR-0036:
  `accepted (owner ratification 2026-07-19, Tier 3)`. ADR-0037: `accepted
  (owner ratification 2026-07-18)`. ADR-0038: `accepted (owner ratification
  2026-07-19, Tier 3)`. All four dates and statuses in the branch's records
  match the ADR files on `main`. **Match.**
- The D1/D2/D3 → ADR mapping the closure section and retrospective use
  (D3=ADR-0035, D1=ADR-0036, D2 prerequisite=ADR-0037, D2=ADR-0038) is
  consistent with the milestone plan's Track 0 topic descriptions on `main`.
  **Match.**
- The four named golden-test files (`test_dsbs_t2_coordinator.py`,
  `test_dsbs_t2_schedule_b.py`, `test_dsbs_t3_line16_coordinator.py`,
  `test_dsbs_t4_dividend_live_integration.py`) all exist under `tests/`.
  **Match.**
- Minor, non-blocking: the retrospective and `foreman-handoff.md` both state
  the new ledger has "14 entries... two new to this milestone." Counting the
  ledger's own section structure, three entries are *not* labeled "carried"
  from the prior ledger: entry 4 (dividend-universe exclusion), entry 5
  (Schedule B Part I single-family scope), and entry 9 (Track 4 F2 scaffold
  visibility) — all three sit outside the "carried" bookkeeping the other
  eleven entries use. The "two new" count appears to undercount entry 5 by
  one. This is a narrative arithmetic slip, not a completeness gap — entry 5
  is present, correctly sourced (Track 2 review's F1 discussion, `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-19-dsbs-t2-composition-conditional-machinery-review.md`
  lines ~86, 235–255), and correctly disposed. Noting for the record; does
  not affect the verdict.

## Check 2 — Matrix fidelity

**F1 (blocking).** Three of the eight aspect rows for the newly-raised
Dividends and Schedule-attachments columns are marked L3 without citing
either Ontology §8 evidential footnote (⁷ for the original three domains,
¹¹ — the new equivalent the branch itself defines — for Dividends/Schedule-
attachments):

- **Presentation** row: `L3 ⁵ | L3 ⁵` (Dividends, Schedule-attachments) —
  cites only footnote 5 (E8.1 deferral note). Compare the same row's W-2/
  Interest/Return-level cells, which all carry `⁷` alongside their other
  footnotes.
- **Correction & supersession lifecycle** row: `L3 ⁶ | L3 ⁶` — cites only
  footnote 6 (free-supersession shim note). Same pattern: the other three
  columns on this row all carry `⁷`.
- **Data boundary** row: `L3 ⁸ ¹⁰ | L3 ⁸ ¹⁰` — cites footnotes 8 and 10 but
  neither 7 nor 11. Footnote 10 only asserts shared infrastructure with the
  existing columns; it does not itself carry the evidential-basis text that
  7 and 11 carry.

The charter's check 2 is explicit and unconditional: "every raised cell
carries the Ontology §8 evidential footnote." The branch's own footnote 12
claims the Schedule-attachments L3 is scoped to "the aspects Schedule B
exercises (all eight rows)" — i.e., the branch's own position is that all
eight rows are in scope for the L3 claim, which makes the missing citation
on three of them a straightforward omission rather than an intentional
narrower claim. The other five rows (Admission & identity, Source closure,
Computation, Adoption & authority, Explanation & audit) correctly carry
footnote 11. This is a mechanical, cheap-to-fix omission — most plausibly
a copy-paste gap when footnotes 5/6/8 were reused verbatim from the existing
columns without also appending 11 (10 was added to the Data boundary row
but 11 was not; 5 and 6 got no addition at all).

Everything else in check 2 passes:

- The matrix raise matches exit criterion 6 exactly: Dividends column L0→L3,
  Schedule-attachments L0→L3, both scoped to what Schedule B exercises per
  footnote 12's honest caveat (Schedule B is the only implemented
  attachment; the D1 ontology's generality is evidenced by an
  already-existing Schedule D stub, not new production content).
- No cell is raised beyond L3 (no L4 claims); the frontier reading correctly
  reflects a breadth- and hardening-limited, not depth-limited, posture.
- Footnote 9 (declared dividend universe = boxes 1a/1b only) and footnote 11
  (evidential basis) are new, correctly scoped, and cite real review
  documents (`2026-07-19-dsbs-t2-*`, `2026-07-20-dsbs-t3-*`,
  `2026-07-20-dsbs-t4-*`) that exist under `docs/reviews/`.

## Check 3 — Ledger completeness

Cross-checked the new ledger's 14 entries against `main`'s
`first-real-return-slice-deferral-ledger.md` (11 entries) and the DSBS
review/ADR trail:

- All 11 prior-ledger entries are accounted for, each explicitly marked
  "carried" with a disposition (untouched, or — for the marshaller
  binding-route entry — "re-affirmed, not retired"). `git log --oneline --
  packages/derivation/marshal.py` confirms exactly one DSBS-track commit
  touched that file (`2a10f60`, Track 2, adding the `attachment-rule.v1`
  binding route) — the ledger's claim that this is the only prior-ledger
  entry this milestone touched, and that it is additive (not replacing any
  existing route), is accurate. The "ten remaining prior entries untouched"
  arithmetic (11 total − 1 touched = 10) in the milestone plan's Closure
  section is correct.
- The milestone plan's declared-universe exclusions (dividend boxes
  2a/3/5/7/12) appear as ledger entry 4, correctly sourced to ADR-0035/D3
  and the milestone plan.
- Track 2's review F1 (Schedule B tie-out defect) is correctly recorded
  under "Explicitly not deferrals" as repaired, not deferred, distinct from
  entry 5's box-1-only scope simplification (which is a genuine, separate,
  still-open scope limitation, verified against the review text).
- Track 3's F1 and R1 findings, Track 1's F2/F3 informational findings, and
  Track 4's F1 scope-reconciliation finding are all correctly characterized
  as repaired/informational/justified rather than open deferrals, matching
  the corresponding review files under `docs/reviews/2026-07-20-dsbs-t3-*`,
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-19-dsbs-t1-schema-citizens-review.md`, and
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-20-dsbs-t4-dividend-live-integration-review.md`.
- Nothing in the ledger claims retirement; every entry's disposition is
  "carried"/"untouched," "re-affirmed, not retired," or "new."

**Pass**, modulo the F1 footnote-citation defect (matrix, not ledger) and
the non-blocking count slip noted under check 1.

## Check 4 — Boundary

Grepped the full diff for real values, workspace locators, disposition
detail, and refusal text beyond the sentence already on `main`. The only
quarantine-adjacent references in the diff are structural/mechanical
restatements already present on `main` before this branch (the
`RELEASE_ABSENT_OR_MISMATCH` stale-pin repair narrative, `git status`/
`envelope_scan.py --verify` confirmation, and pointers to
`tools/scaffold_live_acts.py` / `workspace-seed/`) — none of these add any
new fact beyond what `main`'s milestone-plan Verification section already
recorded before Track 5 branched. No dollar values, no payer/taxpayer
detail, no dispositions, no workspace paths outside the two named
(gitignored) tool files, no expansion of the attestation sentence itself.
**Pass.**

## Check 5 — Verification battery

Run directly on `track/dsbs-t5-completion` (HEAD `8f525bb`), which was
already the primary checkout's state at review start:

- `.venv/bin/python3 -m unittest` — **546 tests, OK.**
- `.venv/bin/python3 -m mypy packages tools tests` — **Success: no issues
  found in 104 source files.**
- `.venv/bin/python3 tools/governance_lint.py` — **governance lint:
  conformant.**
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — **exit 0,
  no findings.**

All four green, independently re-run, not taken from any commit message.
**Pass.**

## Summary of findings

- **F1 (blocking).** Maturity matrix: the Presentation, Correction &
  supersession lifecycle, and Data boundary rows for the Dividends and
  Schedule-attachments columns are marked L3 without citing the Ontology §8
  evidential footnote (7 or the new 11), violating the charter's check 2 in
  its own explicit terms. Fix: add footnote 11 (or 7, per the pattern
  already used on the other five rows) to those six cells
  (`docs/phases/real-return/maturity-matrix.md`).
- Non-blocking note: the "two new" ledger-entry count in the retrospective
  and `foreman-handoff.md` undercounts by one relative to the ledger's own
  three non-"carried" entries (4, 5, 9). No completeness impact — worth a
  one-word correction ("three") if the branch is amended for F1.

## Disposition

Not ready to merge as-is. F1 is a small, mechanical, high-confidence defect
against the charter's own falsifiable text — not a substantive gap in the
underlying evidence, the ledger, or the boundary. Recommend: append the
missing footnote citations to the six affected cells, optionally correct the
ledger-count prose, re-run `governance_lint.py` (docs-only, should be a
no-op), and re-request review only if the footnote fix touches anything
beyond the matrix table. The owner holds the merge per ADR-0034; this
finding is triaged, not adjudicated, by the foreman.
