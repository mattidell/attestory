# First Real Return Slice — Track 5 Completion Records — Pre-Merge Review

Reviewer: owner-dispatched, author-independent pre-merge seat (no authoring-session
context). Date: 2026-07-18. Branch: `track/frrs-t5-completion` at `8c86a90`
(`8c86a90b2ffba2ce6f88677e8ffee623226430ee`). Base: `origin/main` at `527f7df`
(identical to local `main`). Delta reviewed: `origin/main..HEAD` — one commit,
`records: close First Real Return Slice (Track 5)`. Charter:
`docs/reviews/charter-2026-07-18-frrs-t5-completion-review.md`. Track charter:
`docs/reviews/charter-2026-07-18-frrs-t5-completion.md`. This review changes no
implementation, schema, package content, or merge state; it adds only this
record.

## Verdict

**`not ready`**

The scope fence holds (records only), the verification battery is green, the
deferral ledger is complete against the charter's named trail, and the delta
does not carry quarantine detail. Two of the five falsifiable checks fail:

- **Reality (F1):** the milestone plan still opens as `Status: **active**` and
  states that Track 4c "awaits the owner's merge disposition," which is false
  against `main` (PR #18 / `2a2440e`). Other body sections retain the same
  pre-close track dispositions. A bolted-on Closure section asserts completion
  while the document's live status and Current-state language contradict it.
- **Matrix fidelity (F2):** data-boundary L3 cells are marked only with footnote
  ⁸ and do not carry the Ontology §8 evidential footnote (⁷) that every other
  L3 cell carries and that check 2 requires on every L3 cell.

Findings go to foreman triage. The owner holds the merge.

## Scope fence

**Passed.** `git diff --name-status origin/main...HEAD` is nine paths, all under
`docs/`:

| Path | Change |
| --- | --- |
| `docs/foreman-handoff.md` | M |
| `docs/milestone-retrospectives/2026-07-18-first-real-return-slice.md` | A |
| `docs/phase-state.md` | M |
| `docs/phases/real-return/maturity-matrix.md` | M |
| `docs/phases/real-return/milestones/first-real-return-slice-deferral-ledger.md` | A |
| `docs/phases/real-return/milestones/first-real-return-slice.md` | M |
| `docs/phases/real-return/real-return-roadmap.md` | M |
| `docs/reviews/charter-2026-07-18-frrs-t5-completion-review.md` | A |
| `docs/reviews/charter-2026-07-18-frrs-t5-completion.md` | A |

No `packages/`, `tests/`, `tools/`, schema, content, or test path appears.
Untracked local helpers (`tools/scaffold_live_acts.py`, `workspace-seed/`) are
not in the commit range and are not part of this PR delta.

## Check 1 — Reality

**Failed (F1).** Spot-checks that *do* hold, then the contradiction.

### Claims that match git / main / review records

| Claim in the delta | Independent check |
| --- | --- |
| Owner attestation recorded PR #20 | `527f7df` is `Merge pull request #20 from mattidell/docs/frrs-owner-attestation`; tip `f72588d` records the three-fact attestation on the milestone plan Verification section. Present on `main`. |
| Three-fact attestation text | Matches the committed Verification block on `main` / this branch: ran the slice; dispositions observed in quarantine; no artifact crossed. |
| Tracks 1–4c merged per-track (ADR-0030) | Merge commits on `main`: T1 PR #8 `8d93ff1`; T2 PR #11 `aa5db67`; T3 PR #13 `530e387` + F1 repair PR #15 `8c7af6d`; T4 PR #16 `d8a2728`; T4b PR #17 `f977b4d`; T4c PR #18 `2a2440e`; phase-state advance PR #19 `2c9032f`. |
| ADR-0031 / 0032 / 0033 ratified | On `main`: PR #3 `ce86525`, PR #5 `c9dd3c4`, PR #7 `c973c72`. |
| "433+ tests at Track 4c" | Track 4c review record reports **433** full-suite tests; this review re-ran **433 OK** (see Check 5). |
| Track dispositions in phase-state / handoff *Current state* | Consistent with merges above and with "complete pending Track 5 records merge." |

The delta's **added** lines introduce only PR #20 as a new PR citation (no new
merge SHAs). Removed phase-state history carried prior SHAs that already matched
`main`; those are not re-asserted by this track.

### F1 — Milestone plan status and body still assert pre-close reality

**Classification: blocking (Reality).**

`docs/phases/real-return/milestones/first-real-return-slice.md` still opens:

> Status: **active** (2026-07-18) — Tracks 0–4b are merged; the Track 4c
> live-path repair passed independent review and awaits the owner's merge
> disposition.

Independent facts on `main`:

- Track 4c merged as PR #18 (`2a2440e`, 2026-07-18).
- Phase-state advance PR #19 (`2c9032f`) already treated 4c as merged.
- Owner attestation PR #20 (`527f7df`) already closed the real-run gate.

The same file's **Current state**, **Track 0** heading ("complete pending D3
merge"), and Track 4 acceptance-evidence sentence ("disposition report") remain
pre-close wording. Track 5 only appended `## Closure (2026-07-18, Track 5)`
asserting "Milestone complete" and per-criterion dispositions. The document
therefore carries mutually exclusive live claims: active / awaiting T4c merge
vs. complete.

Roadmap, phase-state, and handoff Current-state correctly describe completion
pending this records merge. The milestone plan — the deliverable named as
"milestone plan closure" in the track charter — does not.

**What would clear F1:** bring the plan's Status line, Current state, and
obviously-stale track disposition sentences into agreement with the Closure
section and with `main` (T4c merged; real run attested; Track 5 is the
remaining records unit), without inventing new quarantine detail.

## Check 2 — Matrix fidelity

**Failed (F2).** Raises are otherwise within the pre-committed claim.

### Pre-committed claim (exit criterion 5; frontier reading 2026-07-15)

On `main` the matrix was post-Foundation 2026-07-15: covered capability cells
L2 (one exception: W-2 **Source closure & completeness** at **L1** ¹ — no
closure mapping content), data-boundary row **L0**, Dividends / Schedule
attachments **L0**. Frontier reading: raise data-boundary L0→L3 across covered
domains, which also lifts every covered L2 cell to L3.

Track 5 matrix (2026-07-18):

- Covered domains (W-2, Interest, Return-level): capability aspects → **L3**;
  data-boundary → **L3**.
- Dividends and Schedule-attachments columns remain **L0** (not raised).
- No cell is **L4**.
- Footnote 1 corrected to horizon-keyed W-2 closure as immutable v3 content
  (Tracks 4/4c) — matches what merged.
- Footnote 4 corrected to production resolver outside the fixture boundary
  (ADR-0033, Track 3) with ADR-0028 historical-v1 still deferred — matches
  what merged.
- Footnote 7 states the Ontology §8 evidential basis (synthetic battery +
  non-descriptive attestation; no quarantined run detail).

The L1→L3 raise on W-2 source-closure is within milestone scope (Track 4/4c
shipped the missing mapping, then the real-run attestation supports L3). It is
not a raise *beyond* L3 or into an L0 column.

### F2 — Data-boundary L3 cells lack the Ontology §8 evidential footnote

**Classification: blocking (Matrix fidelity).**

Check 2 requires: every L3 cell carries the Ontology §8 evidential footnote.

| Aspect | W-2 / Interest / Return-level L3 markers |
| --- | --- |
| Admission … Correction aspects | include **⁷** |
| **Data boundary** | **L3 ⁸** only — no **⁷** |

Footnote ⁷ is the Ontology §8 evidential note. Footnote ⁸ states ADR
implementation status and the guarded-transport deferral that holds the row
short of L4; it does **not** restate the evidential basis (synthetic path +
attestation; never quarantine detail). Footnote ⁷'s own prose claims to be the
basis "for every L3 claim," yet the data-boundary cells do not cite it.

The Closure criterion 5 text says covered L2→L3 cells each carry the Ontology
§8 footnote (those cells do cite ⁷). The review charter's rule is stricter:
**every** L3 cell, including data-boundary.

**What would clear F2:** mark data-boundary L3 cells with ⁷ (e.g. `L3 ⁷ ⁸`) or
otherwise make the Ontology §8 evidential footnote attach to those cells as
explicitly as it does to every other L3 cell.

### Non-blocking observation (matrix wording)

**N1 — Exit-criterion phrasing vs. the L1 cell.** Closure criterion 5 and the
track charter say "covered cells L2→L3." One covered cell was L1, not L2, and
is now L3. End-state L3 is correct and within the milestone's W-2-closure work;
the phrasing is slightly imprecise. Not blocking if F1/F2 are fixed without
claiming that cell was already L2.

## Check 3 — Ledger completeness

**Passed.**

Ledger: `docs/phases/real-return/milestones/first-real-return-slice-deferral-ledger.md`
— eleven open entries; preamble states the ledger *records* and that retirement
is future milestone work. No entry claims retirement.

| Required trail item | Ledger treatment |
| --- | --- |
| ADR-0026 further positive interest sources | Entry 7 |
| ADR-0026 subtractive-adjustment mechanism | Entry 8 |
| ADR-0028 historical-v1 migration | Entry 9 |
| ADR-0031 / Track 4b guarded transport / credential confinement | Entry 1 (highest priority) |
| Track 4b operator-level bypass (`--no-verify` / hook deletion) | Entry 2 |
| GitHub remote private (Track 3 recorded default) | Entry 3 |
| Track 1 D3 re-review F3 (split-registry / bad-checksum corpus) | Entry 4 |
| Track 2 F3 (failed-batch record shape) | Entry 5 |
| Track 2 F4 (marshaller binding-route simplification) | Entry 6 |
| Track 2 F2 (name-based reflection helper) | Expressly recorded in entry 6 parenthetical |
| Track 2 F1 | Expressly recorded as **discharged** by Track 3 evaluator fence (entry 6) |
| Standing shims: free supersession; E8.1 / citation display | Entries 10–11 |
| RG-1 eight core-package issues | "Explicitly not deferrals" — discharged in Track 4 per ADR-0033 MUST |
| Disposition report as review evidence | "Explicitly not deferrals" — corrected away (Ontology §8), not deferred |

Nothing in the ledger claims a deferral is retired. Reactivation triggers are
present on the substantive entries.

## Check 4 — Boundary

**Passed.**

Scanned the full `origin/main...HEAD` diff and the new retrospective / ledger
bodies for:

- personal values, amounts, identifiers
- line-level published/blocked dispositions of the real run
- refusal text naming live content
- workspace locators / filesystem paths to the live workspace
- any real-run fact beyond the three-fact attestation, except pre-flight at
  error-class level

Findings:

- The only real-run fact carried is the three-fact attestation (and pointers to
  its Verification / PR #20 record already on `main`).
- Pre-flight support is described at error-class level in the retrospective
  ("pre-flight failure"; kernel refusal class: a closure naming a horizon no
  transition had introduced; diagnosis via synthetic seed / structure-only
  greps; fix owner-side). No values, dispositions, workspace paths, or live
  refusal payloads appear.
- Form-line numbers (1a/2b/9/11/12/15/16) appear only as product-capability
  coverage claims, not as real-run outcomes.
- `$1,500` appears only as the designated Schedule B hard-trace case on the
  frontier (synthetic/planning, pre-existing matrix vocabulary).

No boundary violation found.

## Check 5 — Verification battery

**Passed.** Re-run by this reviewer on `track/frrs-t5-completion` at `8c86a90`.
(Review environment recreated `.venv` against Linux `python3.11` because the
checked-in venv symlink targeted a macOS Homebrew interpreter absent here;
package set is `requirements.txt` only.)

| Command | Result |
| --- | --- |
| `.venv/bin/python3 -m unittest` | **433 tests, OK** (~68s) |
| `.venv/bin/python3 -m mypy packages tools tests` | **Success: no issues found in 92 source files** |
| `.venv/bin/python3 tools/governance_lint.py` | **governance lint: conformant** |
| `.venv/bin/python3 tools/envelope_scan.py --range origin/main..HEAD` | **exit 0** (clean) |

Also confirmed `tools/envelope_scan.py --verify` → installed and verified (suite
prerequisite; not a substitute for the range scan).

## Findings summary

| ID | Check | Class | One-line |
| --- | --- | --- | --- |
| **F1** | Reality | **blocking** | Milestone plan Status/body still claim active + Track 4c awaiting merge; contradicts Closure and `main`. |
| **F2** | Matrix fidelity | **blocking** | Data-boundary L3 cells omit Ontology §8 evidential footnote ⁷. |
| N1 | Matrix wording | non-blocking | "L2→L3" phrasing ignores the one covered cell that was L1. |

No ledger, boundary, scope-fence, or battery finding.

## Recommendation

**Not ready to merge** until F1 and F2 are repaired on this track (or a narrow
follow-on records delta) and a fresh author-independent pass re-checks those two
items. F1 and F2 are records-only fixes; they do not reopen code, schema, or the
real-run attestation. The owner decides disposition under ADR-0030/0034.
