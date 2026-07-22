# Delta Re-Review: Track 5 F1 Repair — Dividends and Schedule B Slice

Date: 2026-07-21. Author-independent delta re-review of commit `546555f` on
`track/dsbs-t5-completion` (HEAD at review time), which repairs finding F1
from `docs/reviews/2026-07-21-dsbs-t5-completion-review.md` (commit
`492cc9e`, verdict NOT READY), per that review's own charter
(`docs/reviews/charter-2026-07-21-dsbs-t5-completion-review.md`). This is a
delta review, not a full re-review: only the repair commit's scope is
independently re-examined; checks the original review already passed
(reality/PR-SHA citations, ledger completeness, boundary/data-safety) are
carried forward unverified here, since the repair commit does not touch
anything those checks depend on (confirmed under Check 0 below).

## Verdict: **READY**

The repair commit fully discharges F1 as originally scoped, and additionally
closes three cells the original review did not explicitly flag but which
had the identical defect. The non-blocking narrative slip ("two new" →
"three new") is also fixed correctly, verified by independently re-deriving
the count from the ledger's own structure. The verification battery is
green, independently re-run. No new defects found. Combined with the
original review's five passing checks (reality, ledger completeness,
boundary, and now matrix fidelity and verification battery), the branch is
ready for the owner's merge decision.

## Check 0 — Scope fence

`git show 546555f --stat`:

```
 docs/foreman-handoff.md                                      |  2 +-
 .../2026-07-21-dividends-and-schedule-b-slice.md             |  7 ++++---
 docs/phases/real-return/maturity-matrix.md                   | 12 ++++++------
 3 files changed, 11 insertions(+), 10 deletions(-)
```

Exactly three files, all records: the maturity matrix, the retrospective,
and the foreman handoff. No code, schema, content, or test file touched.
This matches the repair's claimed scope exactly and confirms the checks the
original review already passed (reality, ledger completeness, boundary) are
unaffected — none of those checks read the three touched files in a way the
repair commit's edits could invalidate (the matrix footnote citations don't
change any PR/SHA/ADR claim; the retrospective/handoff prose edit is the
already-identified count-slip fix; neither touches the ledger file itself
or any boundary-sensitive content). **Pass.**

## Check 1 — F1 resolution: matrix fidelity

Read `docs/phases/real-return/maturity-matrix.md` at
`track/dsbs-t5-completion` in full. Verified every one of the eight aspect
rows, for both the Dividends and Schedule-attachments columns (16 cells
total), now carries footnote ¹¹ somewhere in the cell:

| Aspect | Dividends | Schedule-attachments |
| --- | --- | --- |
| Admission & identity | L3 ⁹ **¹¹** | L3 **¹¹** ¹² |
| Source closure & completeness | L3 ⁹ **¹¹** | L3 **¹¹** ¹² |
| Computation | L3 **¹¹** | L3 **¹¹** ¹² |
| Adoption & authority | L3 **¹¹** | L3 **¹¹** ¹² |
| Explanation & audit record | L3 **¹¹** | L3 **¹¹** ¹² |
| Presentation | L3 ⁵ **¹¹** | L3 ⁵ **¹¹** |
| Correction & supersession lifecycle | L3 ⁶ **¹¹** | L3 ⁶ **¹¹** |
| Data boundary | L3 ⁸ ¹⁰ **¹¹** | L3 ⁸ ¹⁰ **¹¹** |

All 16 cells carry ¹¹. Confirmed against the pre-repair diff (`git show
546555f`) that this closes both defects: the three rows the original review
explicitly flagged (Presentation, Correction & supersession, Data boundary
— which previously cited only 5/6/8+10, no evidential footnote at all), and
three further Schedule-attachments cells the repair commit additionally
fixed (Admission & identity, Source closure & completeness, Computation —
which previously cited only ¹² and were missing ¹¹, even though the
Adoption/Explanation rows in the same column already had it correctly).
This second set was not named in the original review's F1 bullet list but
is the same defect under the same charter rule ("every raised cell carries
the Ontology §8 evidential footnote"), so the wider repair is in scope and
appropriate, not scope creep.

**Footnote 11 text audit.** Read the full footnote 11 text on the branch —
it describes the DSBS synthetic battery driving the full slice through the
named golden classes, cites three real review documents under
`docs/reviews/` (`2026-07-19-dsbs-t2-*`, `2026-07-20-dsbs-t3-*`,
`2026-07-20-dsbs-t4-*`), and the owner's non-descriptive attestation,
closing with the same no-quarantine-detail constraint footnote 7 carries.
This text is unchanged by the repair commit (only its citations across
cells changed) and accurately describes what it is now cited for in all 16
cells — no cell cites it for a claim outside what the footnote actually
describes. **Match.**

**No over-claiming introduced.** Every cell remains at L3 (no L4 raises);
footnote 12's Schedule-B-only scoping caveat is preserved verbatim and
still present everywhere it was before; no cell gained a footnote whose
text doesn't support its claim. The repair is additive-only (footnote
citations added, no L-level or prose claim changed). **Pass.**

## Check 2 — Narrative slip: "two new" → "three new"

Independently re-derived the correct count from
`docs/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md`'s
own structure (not from the repair commit's claim). The ledger has 14
numbered entries organized under headed sections. Entries explicitly marked
**carried** (with a "carried, untouched" / "carried, re-affirmed" /
"carried, **untouched** this milestone" disposition): 1, 2, 3, 6, 7, 8, 10,
11, 12, 13, 14 — eleven entries. The three entries NOT marked carried:

- **Entry 4** ("Dividend boxes 2a, 3, 5, 7, 12 are named honest-block
  exclusions") — under the section header "New this milestone:
  declared-universe scope," no carried label.
- **Entry 5** ("Schedule B Part I ties to the box-1/1099-INT family only")
  — same section, no carried label.
- **Entry 9** ("Scaffold visibility for fresh checkouts") — explicitly
  labeled "**new**, Track 4 review F2 (non-blocking)."

That is three new entries, matching the repair's claim exactly (and
matching the original review's own count/citation of these same three
entry numbers under its non-blocking note). Confirmed both edited files
now read "three new"/"3 new" and name all three entries correctly:

- `docs/milestone-retrospectives/2026-07-21-dividends-and-schedule-b-slice.md`:
  "fourteen entries, none silently closed; three new to this milestone (the
  declared dividend-universe exclusion, Schedule B Part I's single-family
  scope, and Track 4's scaffold-visibility observation)."
- `docs/foreman-handoff.md`: "(14 entries: 3 new, 1 prior-ledger entry
  re-affirmed touched-not-retired, 10 carried untouched; nothing silently
  closed)." Arithmetic checks: 3 + 1 + 10 = 14. **Match.**

**Pass.**

## Check 3 — Verification battery (re-run independently, current tip)

Run on a fresh `git worktree` checked out to `track/dsbs-t5-completion`
HEAD `546555f`, using the primary checkout's `.venv` interpreter (the venv
itself is gitignored and not branch-specific):

- `.venv/bin/python3 -m unittest` — **546 tests, OK** (122.98s). Same count
  as the original review's re-run on `8f525bb`, as expected — the repair is
  docs-only.
- `.venv/bin/python3 -m mypy packages tools tests` — **Success: no issues
  found in 103 source files.** (Original review reported 104 on the primary
  checkout; the one-file difference is `tools/scaffold_live_acts.py`, an
  intentionally untracked/gitignored file — ADR-0031 — present on disk in
  the primary checkout but absent from a fresh worktree. Confirmed by
  listing the file in both locations. Not a defect; mypy is clean either
  way.)
- `.venv/bin/python3 tools/governance_lint.py` — **governance lint:
  conformant.**
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — **exit 0,
  no output (no findings).**

All four green, independently re-run on the current tip, not taken from the
repair commit's message. **Pass.**

## Findings

None. F1 is fully repaired, with a slightly wider (correctly wider) scope
than the original review's explicit bullet list, and the non-blocking
narrative slip is fixed and independently re-verified as arithmetically
correct.

## Disposition

Combined with the original review's checks 0, 1, 3, and 4 (scope fence,
reality, ledger completeness, boundary — all Pass, unaffected by this
docs-only repair), and this delta's re-verification of check 2 (matrix
fidelity, now Pass) and check 5 (verification battery, Pass), the branch as
a whole is **ready** for the owner's merge decision. The owner holds the
merge per ADR-0034; this finding-free delta is triaged, not adjudicated, by
the foreman.
