# Review: Track 0a — ADR-0037 Conditional Multi-Dependency Substrate

Date: 2026-07-19. Author-independent pre-merge review per
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-19-dsbs-t0a-cmdn-review.md`. Reviewer read only
the charter, the Track 0a plan section (`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/
dividends-schedule-b-slice.md`), ADR-0037 with its cited CMDN prototype
evidence (`docs/archive/2026-08-02-milestone-artifacts/prototypes/conditional-multi-dependency-nonpublication/`),
and the branch `codex/dsbs-t0a-cmdn-production` — not the authoring session.

## Object reviewed

`main..codex/dsbs-t0a-cmdn-production`, one implementation commit `c0508cb`
("Implement ADR-0037 conditional dependency substrate"), on top of the
charter commit `40fc6d4`.

## Verdict: **not ready**

Two of the charter's seven falsifiable checks are unmet on their explicit
terms (checks 1d and 3), and one is partially unmet (check 1a). The
underlying evaluator/pin-integrity code is sound and the full verification
battery is green, but the delta does not yet carry the evidence the plan and
ADR-0037's production conditions require before merge. See F1–F4.

## Findings

### F1 — Missing "malformed condition/member shapes" negative (Check 1a) — MEDIUM

The plan (`dividends-schedule-b-slice.md` Track 0a, output 1) requires three
negative categories alongside the positive: "an empty member array, a
non-`ref` member, and malformed condition/member shapes." Only two negative
fixtures are committed:
`packages/sample_data/conditional_multi_dependency/negatives/rule-artifact.v3.empty-members.json`
and `.../rule-artifact.v3.non-ref-member.json`.

The only test that gestures at "malformed shapes" is
`tests/derivation/test_conditional_multi_dependency.py:75-83`
(`test_runner_private_conditional_requires_shape_is_rejected`), which swaps
the entire top-level `op` to a different, never-declared operator name
(`conditional_requires`) rather than malforming `conditional_dependency_set`'s
own fields (e.g., a missing `condition`, non-array `members`, or a `members`
entry missing `name`). That test proves an unknown op is rejected, not that
malformed shapes of the declared node are rejected, and it has no committed
fixture the way the other two negatives do.

**Failure scenario:** a future author could hand-author a
`conditional_dependency_set` with `members` present as a non-array, or a
`condition` field of the wrong shape, and there is no test or fixture in this
delta establishing the schema actually rejects it — only that the schema
rejects an empty array and a non-`ref` array entry.

### F2 — Only four of six CMDN paper cases enter through `live_coordinate_run` (Check 1d) — HIGH

The plan (output 4) and ADR-0037 (production condition 4) require the
coordinator-from-facts fixture family to cover all six paper cases through
`live_coordinate_run` from an authoritative act log, "not a downstream
`RunContext` shortcut." The charter repeats this as a targeted check (1d).

`ConditionalDependencyLiveCoordinator.test_authoritative_fact_goldens_cover_inactive_and_active_missing_paths`
(`tests/derivation/test_conditional_multi_dependency.py:271-298`) drives
exactly four cases through `live_coordinate_run`: inactive/no members,
active/all present, active/two absent, active/one absent. That covers paper
cases 1–4.

Case 5 (contribution and member-supersession lifecycle) is exercised only by
`test_successor_condition_or_member_changes_the_published_pin_identity`
(`tests/derivation/test_conditional_multi_dependency.py:129-147`), which
calls `run()` directly against a hand-built `RunContext` — precisely the
"downstream `RunContext` shortcut" the plan says must not stand in for the
live-coordinator fixture family.

Case 6 (no-reach-around mutation) has no `live_coordinate_run` test at all.
The nearest analog is the schema-rejection test at line 75-83 discussed under
F1, which is a schema-validation test of a differently-named op, not an
authoritative-fact-driven attempt to obtain a missing list outside the
declared node.

**Failure scenario:** the "no reach-around" property (a runner cannot supply
missing-member semantics outside the declared evaluator node) and the
supersession-through-live-facts property are both load-bearing parts of
ADR-0037's contract, but neither is demonstrated end-to-end from an
authoritative act log in this delta. A regression in either property would
not be caught by the goldens shipped here.

### F3 — No mutation test rejects an omitted active-member pin (Check 3) — HIGH

Charter check 3 is explicit: "the mutation tests must actually reject an
omitted active-member pin." ADR-0037 production condition 5 and the plan's
Verification paragraph both independently require "rejection of a mutation
that omits an active-member pin." No such test exists in
`tests/derivation/test_conditional_multi_dependency.py`, and a repo-wide
search for an established pin-mutation-rejection pattern
(`grep -rn "mutation" tests/derivation/`) found none to model against.

I read the code path this check is meant to guard
(`packages/derivation/runner.py:263-266`, the new
`source = self.symbol_pin.get(name); if source is None: continue` skip) and
traced it against `self.symbol_pin` population
(`runner.py:181, 231, 412, 532`) and `AccessLog.refs` population
(`packages/derivation/evaluator.py:108-111`, unconditional
`access.refs.add` before the presence check). `symbol_pin` is populated in
lockstep with `self.symbols` at every site that adds a symbol (input
construction, `optional_default` binding, and both derived-publication
sites), so the skip can only trigger for a symbol that was never supplied —
i.e., a genuinely absent member — never for a present one. **The static
safety property the charter is worried about holds** on inspection of every
reachable `symbol_pin` mutation site in this file. But the charter's
requirement is for an executed mutation test, not a reviewer's code-reading
argument, and that test is absent from the delta.

**Failure scenario:** without an executed test that starts from a
published/blocked record or finding, strips an active member's pin, and
confirms some verification path rejects it, a future change to the pin-skip
logic (or to how `symbol_pin`/`access.refs` are populated) could silently
reintroduce the exact "unpinned active member" defect Adversary R1 used to
reject IT2 — and nothing in this suite would catch it.

### F4 — `_iter_ref_names` reachability walk widened for v1/v2, not scoped to v3 (Check 4) — LOW / non-blocking

`packages/derivation/package_validation.py:568-570` unions
`_iter_ref_names(citizen["when"])` and `_iter_ref_names(citizen["value"])`
into the exclusive-member-graph edge set for every schema in
`_RULE_ARTIFACT_SCHEMAS` — i.e., `rule-artifact.v1` and `.v2` as well as the
new `.v3`. The motivation is specific to v3: `conditional_dependency_set`
members are `ref` expressions nested inside `when` that never appear in the
rule's top-level `requires` array (confirmed in the shipped example,
`packages/sample_data/conditional_multi_dependency/examples/rule-artifact.v3.json`:
`requires` lists only `demo.condition` and `demo.result`, not the two
members). Widening the walk was necessary to make those members reachable.

Applying the same widened walk to v1/v2 citizens is not documented as
deliberate or shown to be inert anywhere in this delta's docs. I checked it
empirically: I scanned every `rule-artifact.v1`/`.v2` fixture under
`packages/sample_data/**` for a `ref` reachable from `when`/`value` that is
absent from `requires`, and found none — so `declared_refs` is set-equal to
the old `requires`-only computation for every existing v1/v2 citizen in the
corpus, and the full test suite (445 tests, run fresh below) is green with no
v1/v2 golden touched by this commit. This is not a functional defect, but the
delta broadens shared validation code for two closed, unrelated schema
versions without a stated justification — worth a documented note (or
scoping the widened walk to v3 only) before or shortly after merge.

## Verification battery (re-run on branch, not trusted from the docs)

The reviewer's own `.venv` was a broken symlink to system Python 3.9 (this
codebase requires 3.10+ syntax, e.g. `str | None` defaults in
`tests/support.py`); the suite failed on import before any test code ran.
Per the charter's remediation instruction, the venv was rebuilt from
`requirements.txt` (using `/opt/homebrew/bin/python3.13`) and the battery was
re-run to completion:

| Command | Result |
|---|---|
| `.venv/bin/python3 -m unittest` | `Ran 445 tests in 80.030s` — **OK** |
| `.venv/bin/python3 -m mypy` | `Success: no issues found in 93 source files` |
| `.venv/bin/python3 tools/governance_lint.py` | `governance lint: conformant` |
| `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` | exit 0, no findings |

The authoritative-surface golden class
(`ConditionalDependencyLiveCoordinator`) executed as part of the full suite
and independently via
`.venv/bin/python3 -m unittest tests.derivation.test_conditional_multi_dependency -v`
(12/12 tests passed, including
`test_primary_and_reference_runners_are_byte_equal`, which is the executed
byte-equality coverage the charter requires). This confirms the branch's own
tracking-doc claims (`docs/foreman-handoff.md`, `docs/phase-state.md`:
"Focused tests, full suite, mypy, governance lint, and envelope verification
passed") are accurate as of `c0508cb` — this is a documentation-accuracy
pass, not a waiver of F2/F3, which are gaps in what the suite covers, not in
whether it passes.

## Checks not otherwise flagged

- **Check 1b (shared evaluator node):** `packages/derivation/evaluator.py`'s
  `conditional_dependency_set` handling is in the one shared `evaluate()`
  function; `runner.py`'s `use_v2` gate now includes `rule-artifact.v3`
  alongside `.v2` uniformly for both the primary and reference runner
  (`run_and_record` and `_Run.__init__`), so both runners admit v3 through
  the ordinary schema/validation path. No runner-private identifier or
  tax/form branch found anywhere in the diff.
- **Check 2 (ADR-0037 conformance):** condition-first evaluation, no member
  read/named/pinned on a false condition, every member evaluated exactly
  once via a plain `for` loop with no reordering, non-absence failures
  re-raised unchanged (`evaluator.py`, `if exc.category != BLOCK_ABSENT:
  raise`), and inactive isolation asserted by test
  (`test_inactive_members_are_neither_missing_nor_pinned` and the "inactive"
  live-coordinator case) — all confirmed. `members` uniqueness is enforced at
  the schema level (`uniqueItems` on structurally-distinct `ref` objects),
  which also forecloses double-counting via a duplicate declared ref.
- **Check 3 (pin integrity, the safety property itself):** confirmed sound —
  see F3 for the reasoning and the residual gap (no executed mutation test).
- **Check 4 (v3 admission mechanics):** `artifact-package.v3` admission is
  purely additive (new enum members, new `allOf` branch mirroring the
  existing v2 one); no semantic fork. See F4 for the one non-blocking
  observation on reachability-walk scope.
- **Check 5 (scope fence):** no QDCG worksheet, declared-absence fact type,
  dividend/Schedule B content, tax-specific missing-list path, UI
  aggregation, or currency-edge content anywhere in the diff (`git show
  c0508cb` scanned for scope-fence terms). D1/D3 are not reopened; v1/v2
  citizens are functionally unchanged (F4 aside). Docs changes
  (`docs/foreman-handoff.md`, `docs/phase-state.md`,
  `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md`,
  `docs/phases/real-return/real-return-roadmap.md`) are tracking-record
  status advances only, and their factual claims match the branch (verified
  above).
- **Check 6 (boundary and data safety):** every fixture, act, and finding
  identifier in the new sample data and tests uses the repo's established
  `demo.*` manufactured-data convention (cross-checked against
  `packages/sample_data/core_tax_conditions/examples/*.json`); no workspace
  path, real-run value, disposition, or refusal text appears anywhere in the
  delta. `envelope_scan.py --range main..HEAD` (the per-review safety scan)
  is clean. `tools/scaffold_live_acts.py` and `workspace-seed/` were left
  untouched and uncommitted, as instructed.
- **Check 7:** see the verification battery table above.

## What must change before this is ready

1. Add a committed negative fixture (or fixtures) for malformed
   `conditional_dependency_set` shapes distinct from the empty-members and
   non-ref-member cases already shipped (F1).
2. Extend `ConditionalDependencyLiveCoordinator` (or an equivalent
   `live_coordinate_run`-driven test) to cover paper case 5
   (contribution/member-supersession lifecycle observed through the
   authoritative act log) and paper case 6 (no-reach-around mutation) (F2).
3. Add an executed test that starts from a published or blocked
   record/finding, strips an active member's pin, and asserts rejection,
   per ADR-0037 production condition 5 and charter check 3 (F3).

F4 is a non-blocking, documented observation for the owner's attention.
