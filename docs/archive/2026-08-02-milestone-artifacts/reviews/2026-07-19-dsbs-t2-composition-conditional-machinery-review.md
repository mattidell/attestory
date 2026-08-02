# Review: Track 2 — Composition and Conditional Machinery — Author-Independent Pre-Merge Review

Date: 2026-07-19. Reviewer: author-independent (fresh session, no access to the
authoring session(s) or any other track's review). Object under review: the
delta `main..track/dsbs-t2-composition-conditional-machinery` at
`aa4a1cb`/`473125f` — charter `1739737`; deliverables 1-2 `6312cc4`;
deliverables 3-4 `2ed1c9c`; deliverables 5-8 `2a10f60`; doc-only handoffs
`ff7712e`, `79f7017`, `aa4a1cb` (confirmed carrying no schema/content/code:
`git diff --stat` on each shows only `docs/foreman-handoff.md` and
`docs/phase-state.md`).

## Verdict: **NOT READY**

One correctness defect (F1) in the Schedule B tie-out invariant is real,
in-scope for this track, and currently untested: it will misfire
(spurious hard-fail) on any filer who has both box-1 interest and any of
box-3/OID/non-form interest at once — a combination the product has
supported since the prior (Source Completeness and Interest) slice. This is
not a boundary or documentation gap; it is the itemization/tie-out mechanism
this track was chartered to build, comparing the wrong two things. Everything
else examined is sound: the admission-time subset invariant, same-batch
ordering, 3a/3b/line-9 composition, the existence conditional,
`collect_members` itemization identity, the dividend-side tie-out, Part III
completeness, the boundary fence, and the full verification battery all hold
up under direct re-derivation. Recommend: fix F1 (either scope Part I's
tie-out target to the box-1 subtotal symbol, or scope Part I's itemization to
the full interest composition, or add an explicit block/guard preventing the
mismatch), add a kill/passing test exercising non-zero non-box-1 interest
alongside the attachment, then re-review is not required if the fix is a
narrow, verifiable content/runner change with a new test — a diff-level
confirmation would suffice.

## F1 — Schedule B Part I tie-out compares itemized box-1 rows against the full four-subtotal line-2b value, not the box-1 subtotal (Check 5)

**Where:** `packages/derivation/runner.py:561-577` (`attempt_attachment`'s
itemization/tie-out loop); `packages/content/tax/2025/rule.attachment.schedule-b.json`
lines 15-22 (`part-i-interest`).

**What:** Line 2b (`tax.us.2025.interest.taxable-total`, published by
`packages/content/tax/2025/rule.form1040-line2b.json`) sums *four* closed
families: box-1 1099-INT, box-3 1099-INT (US Treasury interest), OID box-1,
and non-form interest (`rule.form1040-line2b.json:10-40`, all four already
production-committed by the earlier Source Completeness and Interest Slice —
`packages/content/tax/2025/rule.f1099int-b3-subtotal.json`,
`rule.non-form-interest-subtotal.json` etc. exist and are wired into that
same line). Schedule B's Part I itemization, however, only
`collect_members`s the box-1 family (`rule.attachment.schedule-b.json`'s
`part-i-interest.rows.source_family` = `tax.us.2025.f1099int.b1`), and its
`tie_out.line_symbol` names `tax.us.2025.interest.taxable-total` — the full
four-family sum, not `tax.us.2025.interest.b1-subtotal` (which exists as a
distinct symbol and would have been the scope-correct target). At
`runner.py:567-577`, `row_sum` is computed only from box-1 member findings
while `line_value` is read from the full line-2b symbol; `if row_sum !=
line_value` fires `ITEMIZATION_TIE_OUT_VIOLATION` whenever they diverge. Any
filer with non-zero box-3, OID, or non-form interest concurrent with box-1
interest triggers this: Schedule B hard-fails with a tie-out violation even
though every underlying computation is correct — the exact silent-wrongness
class ADR-0036 decision 3 says this invariant exists to prevent, now
misapplied to the honest case of "interest income from more than one
1099-INT box or source." This directly violates deliverable 7 / ADR-0036
production condition 1's own stated design: "the itemization's row-sum
equals *its line's* published value, same closed family, same horizon" — the
tie-out target here is not "its line" in the same-closed-family sense (it's
a different, wider composition), so the check compares apples pinned from
one family against oranges summed from four.

**Why it's invisible today:** `tests/test_dsbs_t2_schedule_b.py`'s own
docstring (lines 14-21) states plainly: "Every fixture keeps taxable
interest at a closure-backed zero (no 1099-INT box-1 member is ever
asserted); the $1,500 threshold is crossed through ordinary dividends
alone." All box-3/OID/non-form families are always closed-empty in every
Track 2 fixture (`_schedule_b_acts`, `tests/test_dsbs_t2_schedule_b.py:157-163`),
so line 2b's value always equals the box-1 subtotal (0 = 0, or later 0 =
some box-1 value when box-1 is populated — but box-1 member interest is
also never populated in any Track 2 fixture; Part I's row set is empty in
every executed golden). Neither `TieOutInvariant`'s two kill-tests
(`tests/test_dsbs_t2_schedule_b.py:466-493`) nor any other test constructs a
scenario with concurrent box-1 and non-box-1 interest, so the mismatch never
fires in the committed suite — full battery re-run (509 tests, mypy,
governance_lint, envelope_scan) is green, but green here is not evidence
against this defect; it is evidence the defect's triggering condition was
never exercised.

**Disposition:** Not a boundary violation (no Track 3/4 content touched to
fix it) and not a documentation gap (the title on
`rule.attachment.schedule-b.json` honestly discloses the box-1-only
itemization scope per check 4 — see below — it just doesn't disclose that
the tie-out target is wider than that scope, which is the actual defect).
Blocking: this is Track 2's own chartered mechanism (deliverable 7) failing
its own stated invariant shape on a input combination the product already
supports.

## Check-by-check findings

### Check 1 — Admission-time subset invariant and same-batch ordering: PASS

`_enforce_subset_invariants` (`packages/kernel/findings.py:160-214`) is
generic: it reads `registry.subset_invariant_pairs`
(`findings.py:180`), derives "same statement" purely from the fact id's
key suffix after the first `|` (`findings.py:186-198`), and contains no
tax-domain string literal anywhere in `packages/kernel/*.py` (confirmed by
reading the full function and its neighbors). `packages/tax/loader.py:62-64`
declares exactly one pair:
`{"tax.us.2025.f1099div.box1b-qualified": "tax.us.2025.f1099div.box1a-ordinary"}`
— grepped for any second assignment to `subset_invariant_pairs`; none
exists.

All four named rejection scenarios have a passing test each in
`tests/tax/test_dsbs_t2_dividend_admission.py`:
`test_qualified_present_ordinary_absent_rejects` (line 107),
`test_qualified_greater_than_ordinary_rejects` (112),
`test_correction_of_ordinary_rechecks_current_qualified` (125),
`test_removing_ordinary_while_qualified_remains_current_rejects` (140).
`test_violating_pair_is_never_recorded` (157) confirms the successor state
is never observed by a caller: the enforcement function raises
(`findings.py:204-214`) before `apply_assertion`/`apply_member_transition`
return the new state to any caller (`findings.py:341`, `findings.py:488`
— both call `_enforce_subset_invariants` on the fully-folded successor
state before returning it).

Both same-batch orderings are kill-tested in `SameBatchOrdering`
(`tests/tax/test_dsbs_t2_dividend_admission.py:169-300`):
subordinate-first with a violating pair fails closed
(`test_batch_admitting_qualified_before_ordinary_still_fails_closed`, 190);
dominant-first with a conforming pair completes
(`test_batch_admitting_dominant_before_subordinate_admits_a_conforming_pair`,
227); subordinate-first with a *conforming* pair also fails closed
(`test_subordinate_first_order_fails_closed_even_when_conforming`, 264) —
this is intentional, documented behavior (the check runs on cumulative
folded state after each act, so the dominant fact must already be current
when the subordinate is checked) and satisfies ADR-0032 terminal-batch
fail-closed semantics, not a defect.

Enforcement is present on every path the charter names: `apply_assertion`
(`findings.py:316-342`), `apply_member_transition`
(`findings.py:425-489`), both reached by `project()`
(`findings.py:527-531`, which the live coordinator's import at
`packages/derivation/live.py:25` uses directly), and by
`apply_contribution_batch` (`packages/kernel/contribution.py:99-...`,
which applies each successor act through `apply_act` — the same dispatcher
`project()` uses — so the same enforcement runs per-act inside a batch).

### Check 2 — Lines 3a/3b composition and line 9: PASS

Per-box closure independence confirmed by content
(`rule.form1040-line3b.json`'s `when` gates only `tax.us.2025.f1099div.1a`;
`rule.form1040-line3a.json`'s `when` gates only `...1b`) and by the golden
`test_one_family_open_blocks_only_its_own_line`
(`tests/test_dsbs_t2_coordinator.py:231-249`): box1a present/closed, box1b
open — line 3b publishes, line 3a blocks alone.

Block-code split confirmed by direct read of both content and the
precedent file: `rule.f1099div-1a-subtotal.json`'s `collect` op (evaluated
via `evaluator.py:118-131`) raises `BLOCK_CLOSURE` = `"SOURCE_SET_UNCLOSED"`
(`evaluator.py:26`) when the source set is unclosed;
`rule.form1040-line3b.json`'s `requires` gate fires `DEPENDENCY_ABSENT`
(`runner.py:344-347`) when the subtotal symbol is absent. I independently
re-read
`packages/sample_data/tax/scenarios/unclosed_interest_composition/expected/report.json`
and confirmed it says exactly this for the analogous line-2b precedent:
`form1040-line2b` blocked with `DEPENDENCY_ABSENT`, `non-form-interest-subtotal`
blocked with `SOURCE_SET_UNCLOSED` — the claimed precedent is real, not
asserted on faith.

Closed-empty publishes an honest zero pinning family closure, not a source
finding: `test_both_families_closed_empty_publish_honest_zero`
(`tests/test_dsbs_t2_coordinator.py:222-229`) asserts the closure finding
id (`demo.dsbs.t2.closure.div1a`), not a source finding, is in the
subtotal rule's pins.

Line 9 pins line 3b's finding id when dividends are present
(`test_total_income_publishes_pinning_ordinary_dividends`,
`tests/test_dsbs_t2_coordinator.py:255-260`) and still publishes when both
families are closed-empty (`test_zero_dividends_still_publishes_total_income`,
262-266). All four `Lines3a3bPublication` cases and both `Line9WithDividends`
cases enter through `live_coordinate_run` via the shared `_run` helper
(`tests/test_dsbs_t2_coordinator.py:160-171`), confirmed by grep (4
`live_coordinate_run` call sites total in the file, one per `_run` call in
these six tests). `Line3a3bAndLine9Values`
(`tests/test_dsbs_t2_coordinator.py:268-321`) is the sole `RunContext(` use
in the file, and its own docstring (269-272) explicitly disclaims
substituting for the goldens above; it cannot satisfy the charter's
mandatory golden requirement on its own and does not attempt to.

### Check 3 — Schedule B existence conditional: PASS

`attempt_attachment` (`runner.py:454-622`) computes `required = any(t["over"]
for t in triggers)` (line 501) where each trigger's `over` is `Decimal(...)
> threshold` (line 498) — strictly greater than, not greater-or-equal, not
all. Boundary-tested directly: `test_exactly_at_threshold_is_not_required`
(`tests/test_dsbs_t2_schedule_b.py:231-239`) asserts exactly $1,500 is
not-over.

Not-required publishes `inapplicable`/`guard_result: False`
(`runner.py:503-511`) — the identical disposition-row shape (`artifact_id`,
`disposition`, `guard_result`, `pins`) an ordinary rule's false-guard
inapplicable uses (`runner.py:372-380`); grepped both blocks for any
embedded state/discriminator field beyond the ratified triad's own keys —
none present, so distinguishable only by `artifact_id`, matching ADR-0012
atomicity.

Per-trigger outcome is reconstructible: `triggers` (line 496-500) names
each subtotal, its value, and its `over` boolean; asserted directly by
`test_zero_dividends_and_zero_interest_is_not_required`'s pin check
(`tests/test_dsbs_t2_schedule_b.py:217-229`).

I independently re-ran the propagation grep myself (not trusting
`AttachmentCannotPropagateToALine`'s own claim):

```
attachment symbol = tax.us.2025.scheduleb.disposition
grep -c "$symbol" rule.form1040-line2b.json rule.form1040-line3a.json \
  rule.form1040-line3b.json rule.form1040-line9.v2.json  →  0, 0, 0, 0
grep -rl "$symbol" packages/content/  →  only rule.attachment.schedule-b.json itself
```

No sibling content file names the attachment's `publishes` symbol anywhere.

### Check 4 — `collect_members` itemization: PASS, with the F1 caveat noted separately

`self.sources`/`self.source_fids` (`runner.py:244-248`) are populated once
from `ctx.sources` at `_Run.__init__` and are the exact same dicts both the
ordinary `collect` op reads (`env.sources` passed at `runner.py:257`,
consumed at `evaluator.py:121`) and the attachment's itemization rows read
(`runner.py:564-565`) — one table, one resolution path, no parallel or
divergent lookup. A member-finding pin for a row is therefore identical in
identity to the pin the subtotal rule itself produced for the same finding
(both read from `self.source_fids[name]`).

Row shape (`finding_id` + `value`, `runner.py:566`) is confirmed
attachment-runner-internal: `git diff main..HEAD --
packages/schemas/tax/attachment-rule.v1.schema.json` is empty — the schema
is untouched, closed per Track 1 as the charter requires.

Part I's box-1-only simplification is honestly documented in the citizen's
own `title` field (`rule.attachment.schedule-b.json` line 4, quoted in F1
above) — not buried in a comment or test docstring only. I confirmed no
test or golden claims Part I covers box-3/OID/non-form interest: the only
place those families are mentioned in the Track 2 test suite is the
docstring at `tests/test_dsbs_t2_schedule_b.py:14-21`, which explicitly
states they are held at zero. This same honest-scoping is precisely what
makes F1 non-obvious: the itemization's *row* scope is honestly
box-1-only, but the tie-out's *comparison target* silently is not.

### Check 5 — Tie-out invariant: FAIL (F1) for the interest side; PASS for the dividend side

The dividend-side tie-out (`part-ii-ordinary-dividends`) does compare the
itemization's row-sum to the pinned line value for the *same* closed
family (`tax.us.2025.f1099div.1a`) at the same horizon — `line_value` for
that part reads `tax.us.2025.dividends.ordinary-total`, which is exactly
and only the box-1a subtotal (`rule.form1040-line3b.json`'s `value` is a
direct `ref` to the box-1a subtotal, no composition). That part of the
mechanism is correct and is what both kill-tests exercise. The interest
side (`part-i-interest`) is the defect described in F1: its tie-out target
is a four-family composition, not "the same closed family."

Fires only after completeness holds: confirmed by code order in
`attempt_attachment` — completeness/`missing_answers` is checked and can
return `blocked` (line 543-549) strictly before the itemization loop (line
561) runs; a missing-answer block can never be masked behind a tie-out
block because the tie-out code is unreachable until completeness has
already passed.

On violation, hard-fails the attachment only: `_attachment_block` (line
443-452) only appends to `self.blocked`/`self.dispositions` keyed by the
attachment's own `rule_id`; it never touches another artifact's row. No
new error code was invented — grepped the full diff's schema changes
(`git diff main..HEAD -- packages/schemas/` is empty) and the runner
(`ITEMIZATION_TIE_OUT_VIOLATION` is imported/used as the pre-existing
constant from `runner.py:127`, already added to the v3/v2 record/walk
schemas by Track 1's `1d2a58b`, not re-declared here).

Both named kill-tests exist and are genuinely falsifying (read, not
trusted): `test_stale_row_set_a_row_superseded_after_subtotal_but_before_tie_out`
(`tests/test_dsbs_t2_schedule_b.py:466-479`) constructs a line value (2000)
that disagrees with a row set summing to 1600 — a real, non-vacuous
divergence, and asserts the attachment blocks with
`ITEMIZATION_TIE_OUT_VIOLATION` and never publishes.
`test_stale_line_the_published_line_value_superseded_independent_of_the_itemization`
(481-493) constructs the opposite direction (rows sum to 2500, line value
carries 3000) and asserts the same. `test_tying_rows_publish_clean` (495-502)
is the necessary control showing a genuinely-tying case publishes. All
three operate only on the dividend part, which is exactly why F1 on the
interest part went unexercised.

The charter's own allowance (`RunContext`-level rather than
`live_coordinate_run` for these two) is sound: the divergence these tests
construct — a subtotal's published value disagreeing with its own
itemization rows within one run — cannot arise from an honest,
single-threaded fold over one authoritative act log, because both the
subtotal and the itemization read the identical `self.sources`/`self.symbols`
snapshot inside the same run (verified above, Check 4). Fabricating the
divergence therefore requires constructing inconsistent `RunContext` inputs
directly; there is no way to reach it through `live_coordinate_run` without
first reproducing a defect in the fold itself, which is a different (and
already covered) surface. This reasoning holds; it is not a rationalization
for skipping the harder path.

### Check 6 — Part III completeness: PASS

Presence checked independently per required answer before any value is
read: `missing_answers = [s for s in required_answers if s not in
self.symbols]` (`runner.py:520`) is a flat scan with no value read;
branch requirements only look up `self.symbols[trigger_symbol]` (line 532)
after confirming `trigger_symbol in self.symbols` (line 526) — presence
strictly precedes any value read, structurally, not just by test
construction. `test_foreign_trust_absent_alone_names_only_that_answer`
(`tests/test_dsbs_t2_schedule_b.py:311-321`) and
`test_foreign_account_absent_alone_names_only_that_answer` (301-309) each
set the *other* answer to a present value ("no") and confirm only the
truly-absent one is named — this is the masking-risk case the charter asks
for, and it is genuinely covered (not vacuous: the other answer's presence
is real, not also absent).

`FINCEN_114_NAMED` is confirmed text-only by an independent re-run of the
serialized-content scan: `test_yes_branch_names_fincen_obligation_never_produces_it`
(`tests/test_dsbs_t2_schedule_b.py:410-425`) greps the serialized published
value for `form_id`, `"form":`, `"fields":` — I additionally grepped the
full committed value shape assembled at `runner.py:589-595` by hand and
confirmed `named_obligations` carries only `{code, label}` string fields,
no nested form/field/filing structure of any kind.

ADR-0036 text does not itself name any foreign-trust obligation (re-read
decision 4 directly: "a 'yes' on foreign-trust likewise" — parallel
presence-then-value-read structure only, no named obligation content for
foreign-trust anywhere in the ADR). The citizen's title
(`rule.attachment.schedule-b.json` line 4) states "ADR-0036 ratifies no
distinct obligation for foreign-trust (8), so no branch_requirements entry
names one for it" — this is accurate against the ADR text, not a
self-serving claim taken on faith; the ADR genuinely contains no ratified
foreign-trust obligation to invent or omit.

Every answer finding is pinned unconditionally: `used_answer_symbols =
sorted(set(required_answers) | set(triggered_extra_symbols))` (line 551)
includes both `foreign-account` and `foreign-trust` regardless of their
value, and `test_both_answers_no_publishes_whole_form`
(`tests/test_dsbs_t2_schedule_b.py:254-282`) asserts both "no"-valued
answer findings appear in the published pins, exactly as a "yes" would.

**Named finding investigated, disposition: non-blocking observation, not a
real finding.** `missing_answers = sorted(set(missing_answers))`
(`runner.py:542`) is alphabetical. I read ADR-0036 decision 4 in full (it
speaks only to *presence evaluation order*, "no evaluation order can mask
an answer" — nothing about the *output list's* order) and the milestone
plan's Track 0a section
(`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md:202-278`),
which is the source of the declared-member-order guarantee the charter's
Check 6 asks me to distinguish from. That guarantee is scoped explicitly
and exclusively to ADR-0037's `conditional_dependency_set` node (a
different, later mechanism serving D2/line-16/Track 3, not yet built on
this branch — Track 0a is "reviewed ready, pending owner merge," a
prerequisite for Track 3, wholly outside this track's `attempt_attachment`
completeness path). Nothing in ADR-0036, the attachment-ontology synthesis,
or the milestone's Track 2 section extends that ordering guarantee to Part
III's `missing_answers`. This is genuinely unconstrained by ratified text,
as the charter anticipated it might be; sorted-alphabetical is a reasonable
deterministic choice and not a regression against any promised contract.

### Check 7 — Boundary fence: PASS

No QDCG worksheet, D2 declared-absence facts, line-16 content, or
live-run-harness/real-data changes anywhere in the diff (confirmed by the
full `git diff --stat main..HEAD` file list: only dividend/attachment
content, kernel/runner/marshal/live code, tests, and two generator
scripts).

`live.py`'s and `marshal.py`'s diffs are both additive and
schema-gated: `live.py`'s rule filter only widens the accepted-schema set
literal to add `"attachment-rule.v1"` (`live.py:53-59`), otherwise
identical; `marshal.py`'s new `_rule_required_symbols` helper
(`marshal.py:53-68`) branches exclusively on `rule.get("schema") ==
"attachment-rule.v1"`, and its `else` arm (`return list(rule.get("requires",
[]))`) is byte-identical to the prior inline expression it replaced
(`rule.get("requires", [])`) — confirmed by reading both the old and new
hunks side by side in the diff; no existing `rule-artifact.v1/v2/v3` path
changes behavior.

Package validation's reachability walker is untouched: `git diff main..HEAD
-- packages/derivation/package_validation.py` is empty. v5's `entrypoints`
array (`package.core-calculations.v5.json`) lists the new attachment
citizen, its citation, its threshold parameter, and its Part III vocabulary
bundle directly (7 entries total, confirmed by reading the array), the same
pattern v4 used for `dividend-universe.v1` — no `_iter_ref_names`/adjacency
change shipped beyond what Track 1 already committed.

### Check 8 — Boundary and data safety: PASS

`git status --porcelain` on the worktree is clean (no untracked
`tools/scaffold_live_acts.py` or `workspace-seed/` present to accidentally
commit — nothing was touched). Scanned the full diff's added string
literals for real-looking identifiers, PII patterns (SSN-shaped strings),
and non-`demo.`/non-`tax.us.2025.` prefixed ids in new test/tool/content
additions: none found. Tax-layer content consistently uses the
`tax.us.2025.*` convention; fixtures consistently use `demo.*`/`demo-*`.

### Check 9 — Verification battery: PASS (re-run myself, not trusted)

`.venv` in this worktree was absent; rebuilt with `/opt/homebrew/bin/python3.13`
per the charter's fallback instructions, then ran the full battery fresh:

- `.venv/bin/python3 -m unittest` — **509 tests, OK** (111s).
- `.venv/bin/python3 -m mypy` — **Success: no issues found in 98 source files**.
- `.venv/bin/python3 tools/governance_lint.py` — **governance lint: conformant**.
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — **exit 0, clean**.

Grepped each test file myself for `live_coordinate_run` vs `RunContext(`
occurrence counts rather than accepting any commit message's claim:
`test_dsbs_t2_coordinator.py` — 4 `live_coordinate_run`, 1 `RunContext(`;
`test_dsbs_t2_schedule_b.py` — 4 `live_coordinate_run`, 2 `RunContext(`;
`test_dsbs_t2_dividend_admission.py` — 0 of either (kernel/admission-level,
as its own docstring states and the charter's Verification item 6 permits).
All six named golden classes are present and enter through
`live_coordinate_run`: 3a/3b publication (`Lines3a3bPublication`, 4 cases),
line 9 with dividends (`Line9WithDividends`, 2 cases), not-required
(`NotRequired`, 3 cases), required-and-complete (`RequiredAndComplete`, 2
cases), required-and-incomplete (`RequiredAndIncomplete`, 5 cases,
including both single-answer-absent cases and the both-absent case), plus
the runner/admission-level same-batch-ordering and tie-out kill-tests
(charter-permitted exception, both present and executed as enumerated
above).

## Summary

Eight of nine checks pass on direct re-derivation from committed source,
not from any report or test's self-description. Check 5 surfaces a real,
currently-untested correctness defect (F1) in the interest-side tie-out
target, which is this track's own chartered deliverable, not a
Track 3/4 boundary matter and not adequately covered by existing tests
because every Track 2 fixture happens to hold non-box-1 interest at zero.
Recommend the owner route this back for a narrow fix plus a new test
exercising concurrent box-1 and non-box-1 interest before merge.
