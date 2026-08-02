# Review: Track 4 — Dividend Closure Confirmation and Live-Run Harness Extension

Date: 2026-07-20. Author-independent pre-merge reviewer, dispatched per
ADR-0034 against
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-20-dsbs-t4-dividend-live-integration-review.md`.
Object under review: `56ae7af..track/dsbs-t4-dividend-live-integration`
(commit `54f581d` — review charter itself — atop `fcbf70b`, one commit,
"test+tool: Track 4 dividend live-integration goldens, scaffold extension,
gitignore net"). Every claim below was re-derived independently — read the
committed content, ran the code, reproduced the counterfactuals — not taken
from the builder's self-report or the closing note.

## Verdict: READY

No blocking findings. No scope defects. One production condition (not
blocking) and one non-blocking observation, both below. All eight charter
checks pass under independent re-derivation.

## Object-under-review confirmation

- `git log 56ae7af..track/dsbs-t4-dividend-live-integration --oneline`
  returns exactly `54f581d` (this review's own charter) and `fcbf70b` — one
  substantive commit, as the charter states.
- `git show --stat fcbf70b`: exactly three files —
  `.gitignore` (+5), `docs/archive/2026-08-02-milestone-artifacts/reviews/note-2026-07-20-dsbs-t4-closing.md`
  (+110), `tests/test_dsbs_t4_dividend_live_integration.py` (+369). The
  charter file itself was added by the prior commit (`56ae7af`), as
  expected. No DSBS content file, no `tools/scaffold_live_acts.py`, no
  `workspace-seed/` path appears.
- `git log --all -- tools/scaffold_live_acts.py workspace-seed/` returns
  nothing — these paths have never entered git history on any branch.
- `git ls-files | grep -E "scaffold_live_acts|workspace-seed"` returns
  nothing (exit 1) — confirmed untracked at HEAD.

## Findings

### F1 — Production condition (not blocking): `BUNDLE_FILES` addition is real scope, correctly justified but not literally chartered

**Check 3.** The build charter's deliverable-2 text names only
`f1099div.bundle.json` for `BUNDLE_FILES`. The builder additionally added
`scheduleb.bundle.json` and `qdcg.bundle.json`, self-reported as required
for the scaffold to be usable. I independently reproduced this claim rather
than accepting it:

- Listed `fact_types` in each bundle
  (`packages/content/tax/2025/{f1099div,scheduleb,qdcg}.bundle.json`):
  `f1099div.bundle.json` registers only
  `box1a-ordinary`/`box1b-qualified`/`1a.source-closure`/
  `1b.source-closure`/`recorded-boxes`. The Schedule B Part III facts
  (`foreign-account`, `foreign-trust`, `7b-country`) live only in
  `scheduleb.bundle.json`; the two Track-3 declared-absence citizens
  (`capital-gain-distributions`, `schedule-d-required`) live only in
  `qdcg.bundle.json`.
- Reproduced the failure directly against `packages.kernel.findings.project`:
  asserting `tax.us.2025.scheduleb.foreign-account|tax-year=2025` after
  adopting only `f1099div.bundle.json` raises
  `FindingModelError: finding references unknown fact:
  tax.us.2025.scheduleb.foreign-account|tax-year=2025`. Adopting all three
  bundles together, the same assertion projects cleanly (2 findings, no
  error).
- Confirmed both bundles predate this track: `scheduleb.bundle.json` landed
  in Track 2 (`2a10f60`), `qdcg.bundle.json` in Track 3 (`7732cc5`) — this
  is wiring an already-ratified bundle into a list, not new DSBS content,
  consistent with the scope fence ("adding an existing ratified bundle to a
  bundle list is wiring, defining new bundle content would not be").

Classification: **production condition, not blocking.** The builder's
justification is correct and independently reproduced; the scope-fence
boundary (wiring vs. content) is correctly on the wiring side. It is flagged
as a production condition rather than a clean pass only because the
literal charter text under-specified `BUNDLE_FILES` and the builder silently
corrected it rather than the charter being amended first — future charters
for this harness should name `BUNDLE_FILES` by the fact types the objective
requires, not by a single bundle name, to avoid this drift recurring. No
action required before merge.

### F2 — Non-blocking observation: `tools/scaffold_live_acts.py` content confirmed present and correct in this worktree, but is not visible to future fresh checkouts

**Check 3, boundary note.** Because this reviewer's worktree
(`.claude/worktrees/agent-aa01456026c99b5bb`) happened to already contain
the builder's local edits to the untracked
`tools/scaffold_live_acts.py` (confirmed by file inspection, not assumed),
I was able to fully verify its content directly — see "Deliverable 2"
below — rather than falling back to the charter's documented degraded path
(foreman-supplied diff / self-report with caveat). This is recorded as a
non-blocking observation, not a finding against the build: it is a
structural property of untracked files that any *future* review dispatched
into a fresh worktree without this file present would need the fallback
path. No action required.

## Check-by-check evidence

**1. Scope reconciliation (closure-mapping content, line-9 v2).**
Re-derived independently.
`packages/content/tax/2025/closure-mapping.f1099div-1a.json` and
`-1b.json` validate structurally against
`packages/schemas/derivation/source-closure-mapping.v2.schema.json`
(`source-closure-mapping.v2` schema, `family-horizon` closure key,
`current-literal-true`-only admission) and are field-for-field identical in
shape to `closure-mapping.f1099int-b1.json`/`-b3.json`, differing only in
IDs/symbols. `packages/content/tax/2025/rule.form1040-line9.v2.json` sums
`tax.us.2025.wages.total-w2-box1` + `tax.us.2025.interest.taxable-total` +
`tax.us.2025.dividends.ordinary-total` into
`tax.us.2025.income.total-income`; no v3 exists
(`find . -iname "rule.form1040-line9*"` returns only the base and `.v2`
files). `package.core-calculations.v6.json` pins
`{"id": "tax.us.2025.rule.form1040-line9", "version": "v2", ...}` —
confirmed by direct field extraction, not inspection by eye. The "no
non-form-dividend analog" claim is corroborated: `find packages/content
-iname "*non-form*"` returns only the interest-side files
(`non-form-interest.*`); ADR-0035's digest (`docs/adr/INDEX.md` line 57)
describes dividends as two per-box (1a/1b) families with no non-form
citizen. Both "already done" claims hold; no open closure-mapping or
line-9 work was silently skipped.

**2. Deliverable 1 — confirming goldens.**
`ClosureAndLineNineConfirmation` in
`tests/test_dsbs_t4_dividend_live_integration.py:245-293`, all three tests
enter via `_run()` (line 227) which calls `live_coordinate_run` — a genuine
live golden, not a shortcut.
- `test_closed_empty_both_boxes_publish_honest_zero_pinning_closure`
  (line 249): asserts the closure-family finding IDs
  (`demo.dsbs.t4.closure.div1a`/`div1b`), not source findings, are in the
  subtotal rules' pins — proves (a).
- `test_open_family_blocks_only_its_own_line_with_source_set_unclosed`
  (line 265): asserts `rows[LINE_3A_RULE]["code"] == "SOURCE_SET_UNCLOSED"`
  — I confirmed this is the real runner-emitted code, not an assumed one:
  `packages/derivation/evaluator.py:26` defines
  `BLOCK_CLOSURE = "SOURCE_SET_UNCLOSED"` — proves (b).
- `test_line9_v2_pins_ordinary_dividends_into_total_income_under_v6`
  (line 285): asserts line 3b's finding ID is present in line-9's pins
  under a live run against v6 — proves (c).

**3. Deliverable 2 — `tools/scaffold_live_acts.py`.**
Read the file directly at `tools/scaffold_live_acts.py`
(present in this reviewer's worktree with the builder's edits — see F2).
Confirmed:
`ADOPTION_FIXTURE` (lines 50-52) points at
`adopt-core-v6-current.json`; `BUNDLE_FILES` (lines 54-70) includes
`f1099div.bundle.json` plus the two additional bundles addressed in F1;
`FAMILIES` (lines 78-86) includes `tax.us.2025.f1099div.1a`/`1b` mirroring
the interest family tuples exactly (same 4-tuple shape); member-transition
templates for boxes 1a/1b exist
(`member-transition-div-box1a.json`/`-div1b.json`, structurally identical
to the interest box-1 template); the five non-composable boxes (2a, 3, 5,
7, 12) are covered by a single `dividend-recorded-boxes.json` template
against the one `tax.us.2025.f1099div.recorded-boxes` fact type (correctly
not modeled as five separate family members); declared-absence/Part-III
templates exist for both citizens
(`capital-gain-distributions.json`, `schedule-d-required.json`) and all
three Schedule B Part III answers
(`scheduleb-part3-{foreign-account,foreign-trust,7b-country}.json`).
Independently smoke-tested the tool end to end in a scratch temp directory
outside the repo: `scaffold` produced 23 prefilled acts (matching the
closing note's self-reported count exactly); `--renumber` pre-flighted
through the real kernel projector with **8 findings on record** (also
matching); a same-directory `--user`-inside-repo attempt correctly refuses
with the ADR-0031 residency message.

**4. Deliverable 3 — dividend live-integration test.**
`ScheduleBRequiredWithQdcgWorksheet` (line 296) and
`ScheduleBNotRequiredWithQdcgWorksheet` (line 329) each build a complete
synthetic act log via `_v6_dividend_acts()` (W-2 + 1099-INT + 1099-DIV +
Schedule B Part III + QDCG declared-absence declarations, v6-pinned
adoption) and each makes exactly one `_run()`/`live_coordinate_run` call,
asserting both the Schedule B disposition (`published`/`inapplicable`,
with pin-level detail) and the QDCG line-16 result together on the *same*
report object (`rows = _by_artifact(report)`) — genuine one-call
composition, not two calls bolted together.
`grep -n "RunContext(" tests/test_dsbs_t4_dividend_live_integration.py`
returns zero hits (exit 1) — vacuously satisfies "every hit is
docstring-labeled non-substitutive." Structural mirror of
`tests/test_frrs_t4_w2_live_integration.py` confirmed: `TemporaryDirectory`
for workspace, `demo.*` actor namespace (`USER = "demo.user.filer-1"`), no
real locator, same act-log construction pattern.

**5. Deliverable 4 — `.gitignore`.** `git show fcbf70b -- .gitignore`
shows exactly two added lines, `/tools/scaffold_live_acts.py` and
`/workspace-seed/`, under a scoped comment — nothing broader, no
pre-existing `.gitignore` line touched.

**6. Deliverable 5 — closing note.**
`docs/archive/2026-08-02-milestone-artifacts/reviews/note-2026-07-20-dsbs-t4-closing.md` names the F1 discrepancy
explicitly and honestly (does not silently absorb it), states plainly that
nothing remains after merge except the owner's real run and Track 5
records, and makes no claim of closing any ADR-0035/0036/0038 production
condition beyond what Tracks 1-3 already closed, and no claim of DSBS
content change. Confirmed accurate against the actual diff and code.

**7. Boundary and data safety.** `git ls-files` and
`git log --all` both confirm `tools/scaffold_live_acts.py` and
`workspace-seed/` were never tracked or staged (see "Object-under-review
confirmation" above). Read every fixture/act/finding constructor in the new
test file: all identifiers are `demo.*`/`demo-*`-namespaced synthetic data;
values are small round numbers (90000, 600, 120, 80, 2000, "no"/"yes"
strings) with no SSN-shaped value, no real dollar figure tied to a real
person, and all runs execute inside `TemporaryDirectory()` — no real
workspace path. `tools/envelope_scan.py --range main..HEAD` ran clean
(exit 0, no output).

**8. Verification battery — reproduced, not trusted.**
- `.venv/bin/python3 -m unittest`: **546 tests, OK** (matches the
  builder's reported count exactly).
- `.venv/bin/python3 -m mypy`: **Success: no issues found in 104 source
  files.**
- `.venv/bin/python3 tools/governance_lint.py`: **governance lint:
  conformant** (exit 0).
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD`: clean,
  exit 0.

All four green, independently re-run in this reviewer's own worktree.

## What I could not independently verify, and why

- Per the dispatch note, a fresh checkout of this branch would not carry
  the builder's local edits to the untracked `tools/scaffold_live_acts.py`
  (untracked files never travel with git). This reviewer's assigned
  worktree happened to already contain those edits, so deliverable 2 was
  fully verified by direct content read plus independent execution — not a
  degraded self-report acceptance. This is recorded as F2 (non-blocking):
  it is a structural property of the review setup, not a defect, but it
  means a differently-provisioned reviewer session could not have closed
  check 3 to this same depth without either the same lucky worktree state
  or an out-of-band diff from the foreman.
- The builder's local smoke test in their own scratch directory (23 acts,
  8 findings, `runner.py` producing a report) is a self-report I could not
  literally replay in their exact directory — but I independently
  reproduced the same scaffold/renumber sequence in my own scratch
  directory and got the identical counts (23 acts, 8 findings), which is
  strong independent corroboration rather than acceptance on faith.
- I did not execute `runner.py` end-to-end with filled real values (that
  would require real data, which is out of scope and prohibited for this
  seat); I only confirmed the pre-flight/kernel-projection path succeeds
  with prefilled synthetic scaffold content, which is what deliverable 2
  actually claims.

## Summary

Ready to merge. Zero blocking findings, zero scope defects. One production
condition (F1: `BUNDLE_FILES` scope beyond the charter's literal text,
independently reproduced as correct and properly justified as wiring, not
content) and one non-blocking observation about untracked-file review
provenance (F2). Full verification battery green under independent re-run:
546/546 tests, mypy clean, governance lint conformant, envelope scan clean.
