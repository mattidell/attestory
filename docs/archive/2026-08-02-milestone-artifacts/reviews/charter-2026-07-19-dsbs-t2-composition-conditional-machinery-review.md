# Charter: Track 2 — Composition and Conditional Machinery — Author-Independent Pre-Merge Review

Date: 2026-07-19. Prepared by the foreman; the owner dispatches this seat
(ADR-0034). The reviewer is author-independent: it reads this charter, the
Track 2 build charter (`docs/reviews/charter-2026-07-19-dsbs-t2-composition-
conditional-machinery.md`), ADR-0035 and ADR-0036 with their cited prototype
evidence, and the branch `track/dsbs-t2-composition-conditional-machinery`
— not the authoring session(s). Two different builder sessions and one
foreman reconciliation touched this branch; treat the branch as the sole
source of truth, not any session's self-report.

## Object under review

The delta `main..track/dsbs-t2-composition-conditional-machinery`: charter
commit `1739737`; deliverables 1–2 `6312cc4` (ADR-0035 1b≤1a admission-time
subset invariant, same-batch ordering); deliverables 3–4 `2ed1c9c` (lines
3a/3b, line-9 fold-in); deliverables 5–8 `2a10f60` (the complete Schedule B
attachment); plus handoff-only doc commits (`ff7712e`, `79f7017`, `aa4a1cb`)
that carry no schema/content/code — verify that claim rather than assume it.

## Falsifiable checks

### 1. Admission-time subset invariant and same-batch ordering (deliverables 1–2, `6312cc4`)

Read `packages/kernel/findings.py`'s `_enforce_subset_invariants` and
`_current_value_for_fact`. Confirm: the mechanism is generic (reads
`registry.subset_invariant_pairs`, no tax-domain string literal in
`packages/kernel/*.py`); the tax registry
(`packages/tax/loader.py`) declares exactly the one pair (box1b-qualified
subordinate to box1a-ordinary); rejection fires on all four named rejection
scenarios (qualified present/ordinary absent; qualified > ordinary;
correction of ordinary re-checking current qualified; removal of ordinary
while qualified remains current) with a passing test each in
`tests/tax/test_dsbs_t2_dividend_admission.py`; a violating pair is never
recorded (the successor state is never observed by the caller — read the
raise site, not just the test assertion); both same-batch orderings
(dominant-first, subordinate-first within one contribution batch) are
kill-tested and both fail closed per ADR-0032 terminal-batch semantics.
Confirm this enforcement point is genuinely on every admission path named
in the charter (`project()`, `apply_contribution_batch`, the live
coordinator's `project()` call) — read the call sites, not the docstring's
claim.

### 2. Lines 3a/3b composition and line 9 (deliverables 3–4, `2ed1c9c`)

Confirm per-box closure independence: an open/undeclared family blocks only
its own line, never the other. Confirm the documented block-code split
(composing line reports `DEPENDENCY_ABSENT` via its `requires` gate,
`runner.py:310`; the subtotal rule itself reports `SOURCE_SET_UNCLOSED`)
against the cited precedent
(`packages/sample_data/tax/scenarios/unclosed_interest_composition/expected/report.json`)
— confirm the precedent file actually says what the commit claims, don't
take it on faith. Confirm closed-empty publishes an honest zero pinning the
family closure (not a source finding). Confirm line 9 pins line 3b's
finding id when dividends are present, and still publishes when both
dividend families are closed-empty. Confirm all four coordinator cases in
`tests/test_dsbs_t2_coordinator.py::Lines3a3bPublication` and the two in
`Line9WithDividends` enter through `live_coordinate_run`, and that
`Line3a3bAndLine9Values` is genuinely supplementary (its docstring says so —
confirm the class cannot be mistaken for satisfying the charter's mandatory
golden-class requirement on its own).

### 3. Schedule B existence conditional (deliverable 5)

Read `_Run.attempt_attachment` in `packages/derivation/runner.py`
(committed at `2a10f60`). Confirm: the requirement is "any subtotal
strictly greater than the threshold parameter" (not all, not
greater-or-equal — boundary-test exactly $1,500 as not-over); not-required
publishes the ordinary `inapplicable`/`guard_result: false` disposition
(confirm this is schema-admitted and distinguishable from a line's
ordinary inapplicable disposition only by `artifact_id`, per ADR-0012
atomicity — no embedded state field anywhere); per-trigger outcome is
reconstructible from the published `triggers` array (each subtotal's value
and over/under boolean), not silent. Confirm
`AttachmentCannotPropagateToALine` genuinely proves no sibling content file
(`rule.form1040-line2b.json`, `-line3a.json`, `-line3b.json`,
`-line9.v2.json`) names the attachment's `publishes` symbol anywhere —
re-run the grep yourself, don't trust the test's own claim.

### 4. `collect_members` itemization (deliverable 6)

Confirm the mechanism pins the member findings of the *same closed family,
same horizon* that the tied line's subtotal already collected — read how
`self.sources`/`self.source_fids` are populated and confirm they are the
same tables the ordinary `collect` op reads (`evaluator.py`), so a
member-finding pin for a row is identical in identity to the one the
subtotal rule itself pinned (no parallel, potentially-divergent resolution
path). Confirm row shape (`finding_id` + `value`) is attachment-runner-
internal and never generalized into `packages/schemas/tax/attachment-
rule.v1.schema.json` (that schema is closed — Track 1 territory; a change
there would be a scope violation). Confirm the Part I "box-1/1099-INT
family only" simplification is honestly documented in the citizen's own
`title` field (not buried), and that no test or golden claims Part I covers
box-3/OID/non-form interest.

### 5. Tie-out invariant (deliverable 7)

Confirm the check compares itemization row-sum to the *pinned* line value
(same closed family, same horizon — not a re-derivation), fires only after
completeness already holds (never masks a missing-answer block behind a
tie-out block), and on violation hard-fails the attachment only — never
touches the line's own disposition, never publishes divergent form content.
Confirm it reuses `ITEMIZATION_TIE_OUT_VIOLATION` (Track 1's vocabulary,
`derivation-record.v3.schema.json` / `npe-walk.v2.schema.json`) rather than
inventing a new code — grep for any new error-code string this delta might
have added. Confirm both named kill-tests exist and are genuinely
falsifying (stale row set: a row's source finding superseded after subtotal
but before tie-out; stale line: the line's own published value superseded
independent of the itemization) — read `TieOutInvariant` in
`tests/test_dsbs_t2_schedule_b.py` and confirm each test actually
constructs the claimed divergence rather than a vacuous case. Assess the
charter's own allowance that these may be `RunContext`-level rather than
`live_coordinate_run` goldens (the stated reason: a correctly-computed live
run can never disagree with itself) — confirm this reasoning is actually
sound and not a rationalization for skipping the harder authoritative-
surface path.

### 6. Part III completeness (deliverable 8)

Confirm presence is checked independently per required answer *before* any
value is read — construct or find a test where one answer is absent and
the other's value would, if read first, mask the first's absence; confirm
it doesn't. Confirm a `yes` on foreign-account adds the 7b-country
requirement and names `FINCEN_114_NAMED` as text only — re-run the
existing serialized-content scan (`form_id`, `"form":`, `"fields"` absent)
yourself and extend it if you find a gap the committed test missed. Confirm
ADR-0036's text actually supports "no branch requirement for foreign-trust"
(the citizen's own docstring makes this claim — verify against the ADR,
don't take the content's self-description as authoritative). Every answer
finding must be pinned unconditionally in the published/blocked disposition
regardless of its value — confirm a `no` answer is pinned exactly like a
`yes` answer. **Named finding to investigate, not pre-judged:** the missing-
answers list is built via `sorted(set(missing_answers))`
(`runner.py`, in `attempt_attachment`) — alphabetical, not declared order.
ADR-0036 does not state an ordering requirement for this list the way
ADR-0037 did for `conditional_dependency_set`'s member order; confirm
whether this is actually silent in the ADR (then note it as a
non-blocking observation) or whether the milestone plan/synthesis implies
an ordering guarantee this delta breaks (then it is a real finding).

### 7. Boundary fence

No QDCG worksheet, no D2 declared-absence facts, no line-16 content (Track
3), no live-run harness or real data (Track 4). The two live-path wiring
fixes (`live.py`'s rule filter, `marshal.py`'s legacy-input fallback) are
additive extensions recognizing `attachment-rule.v1`'s own symbol surface —
confirm they do not change behavior for any existing `rule-artifact.v1/v2/v3`
citizen (read the diffs at the exact hunks, confirm the added branches are
strictly `attachment-rule.v1`-gated or genuinely inclusive without altering
prior matches). Confirm package validation's reachability walker was not
modified to add attachment-specific adjacency logic (the commit message
claims v5's entrypoints list every new citizen directly instead, the same
pattern v4 used for `dividend-universe.v1` — confirm this by reading v5's
`entrypoints` array and confirming no `_iter_ref_names`/adjacency-walker
change shipped in this delta beyond what Track 1 already committed).

### 8. Boundary and data safety

Every fixture, identifier, and golden is manufactured `demo.*`/`demo-*`
data; committed tax-layer content uses the established `tax.us.2025.*`
convention. No workspace path, real-run detail, value, disposition, or
refusal text anywhere in the delta. Run the per-review safety scan. Never
commit `tools/scaffold_live_acts.py` or `workspace-seed/`.

### 9. Verification battery (re-run, not trusted)

On the branch: `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m
mypy`, `.venv/bin/python3 tools/governance_lint.py`, and `.venv/bin/python3
tools/envelope_scan.py --range main..HEAD` — all green. Confirm all six of
the charter's named authoritative-surface golden classes are executed and
enter through `live_coordinate_run`: 3a/3b publication, line 9 with
dividends, Schedule B not-required, Schedule B required-and-complete (whole
form), Schedule B required-and-incomplete (honest block, both the
single-answer-absent and both-absent cases), plus the same-batch ordering
and tie-out kill-tests (runner-level, per the charter's stated allowance).
Grep the test files yourself for `live_coordinate_run` vs `RunContext(` and
confirm which class each golden lives in — do not accept a commit
message's count.

## Verdict

Write `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-19-dsbs-t2-composition-conditional-machinery-review.md`
on the branch with an explicit `ready` / `not ready` verdict and findings
numbered F1…, each tied to a check above with file/line evidence. The
foreman triages findings; the owner holds the merge (ADR-0030). Merge of
this track closes Track 2; Track 3 (line 16 under D2) opens next.
