# Charter: Track 4 — Dividend Closure Confirmation and Live-Run Harness Extension — Author-Independent Pre-Merge Review

Date: 2026-07-20. Prepared by the foreman; the owner dispatches this seat
(ADR-0034). The reviewer is author-independent: it reads this charter, the
Track 4 build charter
(`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-20-dsbs-t4-dividend-live-integration.md`),
ADR-0014, ADR-0017, ADR-0031, ADR-0032, ADR-0033, ADR-0035, ADR-0036,
ADR-0038, and the branch `track/dsbs-t4-dividend-live-integration` — not the
builder's self-report. Treat the branch as the sole source of truth.

## Object under review

The delta `56ae7af..track/dsbs-t4-dividend-live-integration` (charter
itself is `56ae7af`): one commit, `fcbf70b` ("test+tool: Track 4 dividend
live-integration goldens, scaffold extension, gitignore net"). Confirm this
is exhaustive — `git log 56ae7af..track/dsbs-t4-dividend-live-integration
--oneline` yourself, don't take it on faith. The tracked diff touches
exactly four files: `.gitignore`, `docs/reviews/note-2026-07-20-dsbs-t4-
closing.md`, `tests/test_dsbs_t4_dividend_live_integration.py`, and the
charter file itself (added by the prior commit). Confirm no other file is
in the diff — in particular confirm `tools/scaffold_live_acts.py` and
`workspace-seed/` never appear in `git show --stat fcbf70b` or anywhere in
`git log --all -- tools/scaffold_live_acts.py workspace-seed/`.

## Falsifiable checks

### 1. Scope reconciliation — the two "already done" claims (charter's own scope-reconciliation section)

The build charter claims the milestone plan's Track 4 line names two items
that were already complete before this track: the 1099-DIV closure-mapping
content (`closure-mapping.f1099div-1a.json`, `-1b.json`) and line-9's
absorption of 3b (`rule.form1040-line9.v2.json`). **Re-derive this
independently — do not take the builder's or the foreman's word.** Read
both closure-mapping files against `packages/schemas/derivation/source-
closure-mapping.v2.schema.json` and compare their shape to
`closure-mapping.f1099int-b1.json`. Read `rule.form1040-line9.v2.json` and
confirm it sums `tax.us.2025.dividends.ordinary-total` (3b) into total
income, and that `package.core-calculations.v6.json` pins this v2 (not v1).
If either claim is wrong — if there is in fact open closure-mapping or
line-9 content work the builder silently treated as done and skipped — that
is a blocking finding.

### 2. Deliverable 1 — confirming goldens

Read `ClosureAndLineNineConfirmation` in
`tests/test_dsbs_t4_dividend_live_integration.py`. Confirm it actually
proves, under the v6 pin: (a) a closed-empty dividend closure family
publishes an honest zero pinning the closure finding — not an assumed
zero; (b) an open/unclosed family blocks with `SOURCE_SET_UNCLOSED` (or the
correct current code — check the committed goldens for the real code,
don't assume) rather than silently aggregating; (c) line-9 v2 genuinely
pins 3b's finding into total income in a live run, not just by static
inspection of the rule file. Confirm this is a genuine golden entering
through `live_coordinate_run`, not a shortcut.

### 3. Deliverable 2 — `tools/scaffold_live_acts.py` extension

This file is untracked and will not appear in the branch diff — read it
directly on disk in the reviewer's checkout of the branch (it is a local
file in the builder's worktree; if your own checkout doesn't carry the
builder's local edits, ask the foreman for the exact diff rather than
re-deriving it from scratch, since re-deriving a from-scratch version would
not actually confirm what the builder did). Confirm: `ADOPTION_FIXTURE`
points at the v6-pinning fixture; `BUNDLE_FILES` includes
`f1099div.bundle.json`; the builder's final report claims it *also* added
`scheduleb.bundle.json` and `qdcg.bundle.json` beyond what the charter's
literal text named, justified as "needed for the Schedule B/QDCG fact types
the charter's own objective requires." **Named finding to investigate, not
pre-judged:** verify this justification independently — do the two
declared-absence citizens and the Schedule B Part III facts genuinely fail
to resolve/register without those two bundles present in `BUNDLE_FILES`
(reproduce, don't accept the claim), and confirm adding them does not
constitute new scope beyond "harness wiring for already-ratified citizens"
(re-read the charter's scope fence — no DSBS content changes; adding an
existing ratified bundle to a bundle *list* is wiring, defining new bundle
content would not be — confirm which this is). Also confirm the family
entries (`f1099div.1a`, `f1099div.1b`), the member-transition templates
(boxes 1a/1b, the five non-composable boxes per a `f1099div.recorded-boxes`
template, and the declared-absence/Schedule-B-Part-III assertion
templates) exist and mirror the existing interest templates' shape.

### 4. Deliverable 3 — dividend live-integration test

Read `ScheduleBRequiredWithQdcgWorksheet` and
`ScheduleBNotRequiredWithQdcgWorksheet` in the same test file. Confirm each
constructs a complete synthetic act log (W-2 + 1099-INT + 1099-DIV +
declarations, v6-pinned adoption) and asserts, in one `live_coordinate_run`
call, both the Schedule B disposition (existing or not, correctly) and the
QDCG line-16 result together — this composition is the thing no prior
track's tests exercise, so confirm it's not merely two separate assertions
bolted together with the interaction unverified. Grep the whole file for
`RunContext(` and confirm every hit is docstring-labeled non-substitutive
supplementary use, per the Track 0a/2/3 discipline — cite the exact lines.
Confirm the test mirrors `tests/test_frrs_t4_w2_live_integration.py`'s
synthetic-only discipline (temp workspace, `demo.*` actor namespace, no
real locator).

### 5. Deliverable 4 — `.gitignore` safety net

Confirm `.gitignore` gained exactly `/tools/scaffold_live_acts.py` and
`/workspace-seed/` (or equivalent patterns) and nothing broader — the
charter explicitly said not to expand this into a wider gitignore audit.

### 6. Deliverable 5 — closing note

Read `docs/archive/2026-08-02-milestone-artifacts/reviews/note-2026-07-20-dsbs-t4-closing.md`. Confirm it honestly
names what remains after this track merges (only the owner's real run and
attestation) and does not overclaim — in particular confirm it does not
claim to have closed any ADR-0035/0036/0038 production condition that
Tracks 1-3 didn't already close, and does not claim DSBS content changed.

### 7. Boundary and data safety

Confirm `tools/scaffold_live_acts.py` and `workspace-seed/` are untracked
on this branch (`git ls-files | grep -E "scaffold_live_acts|workspace-seed"`
returns nothing) and were never staged in commit `fcbf70b` (`git show
--stat fcbf70b` confirms). Confirm every fixture/act/finding in the new
test file is `demo.*`/`demo-*` synthetic data — no real SSN-shaped value,
no real dollar amount tied to a real person, no real workspace path. Run
the per-review safety scan (`tools/envelope_scan.py --range main..HEAD`).

### 8. Verification battery (re-run, not trusted)

On the branch: `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m
mypy`, `.venv/bin/python3 tools/governance_lint.py`, and
`.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — all green.
The builder reports 546 tests passing (up from the pre-branch count) and a
clean mypy/lint/scan run — reproduce, don't accept the count on faith.

## Verdict

Write `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-20-dsbs-t4-dividend-live-integration-review.md`
on the branch with an explicit `ready` / `not ready` verdict and findings
numbered F1…, each tied to a check above with file/line evidence. The
foreman triages findings; the owner holds the merge (ADR-0030). Merge of
this track closes Track 4 — the only remaining milestone item is Track 5
(records/completion) and the owner's real run.
