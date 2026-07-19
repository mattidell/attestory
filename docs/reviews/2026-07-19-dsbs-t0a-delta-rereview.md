# Delta Re-Review: Track 0a Repair Commit `595c4e1`

Date: 2026-07-19. Author-independent delta re-review per
`docs/reviews/charter-2026-07-19-dsbs-t0a-delta-rereview.md`. The reviewer did
not author the repair; every claim below was verified against the branch and
by executed runs, not against the repair author's account.

## Object reviewed

The repair delta `18b2f9e..595c4e1` on `codex/dsbs-t0a-cmdn-production`
(one commit, "repair: discharge Track 0a review findings F1-F4"), read against
the original not-ready review (`docs/reviews/2026-07-19-dsbs-t0a-cmdn-review.md`)
and the original charter
(`docs/reviews/charter-2026-07-19-dsbs-t0a-cmdn-review.md`). This is a delta
re-check: the original review's passing checks (1a-partial, 1b, 1c, 2,
3-property, 4, 5, 6, 7) stand unless disturbed; only F1–F4 discharge and
collateral were examined afresh.

## Verdict: **ready**

All four findings are discharged on the charter's exact terms, the delta
touches nothing outside them, and the full verification battery re-run is
green. Two non-blocking observations (R1, R2) are recorded for the owner.

## Charter item 1 — F1 discharged: yes

Three new committed negative fixtures malform `conditional_dependency_set`'s
own fields, exactly the three shapes the plan and F1 named:

- `packages/sample_data/conditional_multi_dependency/negatives/rule-artifact.v3.missing-condition.json`
  — node with `members` but no `condition`;
- `.../rule-artifact.v3.non-array-members.json` — `members` present as an
  object, not an array;
- `.../rule-artifact.v3.member-missing-name.json` — a `members` entry
  `{"op": "ref"}` with no `name`.

The executed test
`ConditionalDependencySchema.test_malformed_conditional_dependency_shapes_are_rejected`
(`tests/derivation/test_conditional_multi_dependency.py:69-79`) asserts
`SchemaValidationError` for all five negatives (the two original fixtures plus
the three new ones), each as a subTest. These are schema rejections of the
declared node's shape, not an unknown-op swap: the published schema
(`packages/schemas/derivation/rule-artifact.v3.schema.json`, the
`conditional_dependency_set` branch) declares
`required: ["op", "condition", "members"]`, `members` as
`type: array, minItems: 1` of `ref_expr`, and `ref_expr` as
`required: ["op", "name"]` with `additionalProperties: false` — one clause per
fixture. The reviewer additionally isolated the cause: each new negative,
with only its single malformation repaired in memory, validates cleanly, so
the rejection is attributable to the malformed shape and nothing else.

## Charter item 2 — F2 discharged: yes

**Case 5 (lifecycle).**
`ConditionalDependencyLiveCoordinator.test_lifecycle_contribution_and_supersession_through_the_act_log`
(`tests/derivation/test_conditional_multi_dependency.py:326-378`) drives four
runs, every one entering through `live_coordinate_run` from an authoritative
act log built by `_surface_and_acts` (the same construction the case 1–4
goldens use) via the `_coordinate` helper (lines 314-324). No `RunContext` is
constructed anywhere on the repaired paths. The ladder is: two-absent blocked
(ordered missing list asserted), one-contributed blocked, published (pins
`demo.cmdn.finding.alpha` asserted present). The supersession leg appends a
successor assertion act for the same fact identity and asserts, from the
records the coordinator wrote: the re-run publishes, pins
`demo.cmdn.finding.alpha.successor` and **not** the original, and the
published finding identity is displaced (`assertNotEqual` on `finding_id`).

The displacement is demonstrated through committed machinery, as the charter
requires: `compute_currency(project(successor_acts, registry))`
(`packages/kernel/currency.py`, `packages/kernel/findings.py` — both
pre-track, last touched in commit `e4a0e4d`) is asserted to place
`demo.cmdn.finding.alpha` in `displaced_finding_ids`, and
`compute_derivation_currency` (`packages/derivation/projection.py`, also
pre-track) is asserted to place the earlier published consumer's `finding_id`
in `displaced_derived_ids` via its recorded pins (test lines 373-378). No new
currency machinery was introduced by the repair; the diff confirms it touches
only imports, fixtures, the reachability gate, and tests.

**Case 6 (no-reach-around).**
`test_no_reach_around_mutation_is_refused_at_the_live_boundary`
(`tests/derivation/test_conditional_multi_dependency.py:380-405`) builds the
full authoritative surface, then overwrites the rule member's bytes on disk
with a mutation that deletes the declared node (`when: True`) and hand-authors
the missing list in `blocked`. The run enters through `live_coordinate_run`
and asserts a refusal, no output path, and
`assertFalse((root / "workspace" / "records").exists())` — absence of the
record stream, not merely a refusal object.

The reviewer confirmed the refusal is the resolver byte boundary doing the
work, both by code path and empirically. Code path:
`packages/derivation/live.py:91-96` returns a resolver `Refusal` before
`RecordStream` is opened at line 113; the resolver's Decision 3
(`packages/derivation/production_resolver.py:249-283`,
`_resolve_member_corpus`) admits only bodies whose `citizen_checksum` matches
the verified registry, refusing `MEMBER_ABSENT_OR_MISMATCH` otherwise.
Empirically: the reviewer re-ran the exact test scenario in isolation and
observed the refusal reason `MEMBER_ABSENT_OR_MISMATCH` with the workspace
containing only its bootstrap gates and manifest — no records, no output.
The tampered member bytes versus the registry checksum are what refuse the
run; nothing downstream (schema validation, evaluation) is reached.

## Charter item 3 — F3 discharged: yes

`ConditionalDependencyPinMutation.test_stripping_an_active_member_pin_is_rejected_by_identity_verification`
(`tests/derivation/test_conditional_multi_dependency.py:408-430`) is executed
(runs in the focused module, 15/15) and does exactly what the charter asks:

- starts from a **published** finding (active condition, both members
  present, `run(...)` publication);
- includes the **positive control**: the intact finding's `id` equals the
  reconstruction `_content_id("finding:derived:", {"symbol", "value",
  "pins"})` — the committed content-identity derivation the runner itself
  uses at publication (`packages/derivation/runner.py:127-128, 380-383,
  499-503`), so the control proves the reconstruction is the real one;
- strips, in turn, **each** active member pin (`demo.finding.alpha`,
  `demo.finding.beta`) **and the condition pin**
  (`demo.finding.condition`), asserts the pin was genuinely removed
  (`len(mutated) == len(pins) - 1`), and asserts the mutated pin set no
  longer reproduces the finding's content identity.

A finding whose active-member or condition pin is omitted therefore fails
content-identity verification — the executed mutation rejection ADR-0037
production condition 5 and original charter check 3 required.

## Charter item 4 — F4 discharged: yes

`packages/derivation/package_validation.py:567-574`: the widened
`_iter_ref_names` walk over `when`/`value` is now gated on
`citizen["schema"] == "rule-artifact.v3"`, with a comment stating the
rationale. For v1/v2, `declared_refs` is exactly `set(citizen.get("requires",
[]))` — the same edge set as the pre-track computation on `main`
(`main:packages/derivation/package_validation.py`, the
`for req in citizen.get("requires", [])` loop): iterating a de-duplicated set
instead of the list is behaviorally identical because every accumulation
target (`adj[m_id]`, the `bundles_for_fact` union) is a set. All other v1/v2
edge sources (source sets, parameter/table refs, composition, citations) are
untouched by the diff. `git show 595c4e1 --stat` lists five files — the
validator, three new negative fixtures, and the test module — and **no
golden**. The full suite passes with no golden regeneration.

## Charter item 5 — no collateral damage: yes

The delta's entire content is within the four findings: the v3 scope gate
(F4), three `demo.*` negative fixtures (F1), and test-module additions (F1
test extension, `_surface_and_acts` optional `successors` parameter plus
`_coordinate` helper and the two live tests for F2, the pin-mutation class
for F3, and the imports they need). The one pre-existing test renamed
(`test_empty_and_non_ref_members_are_rejected` →
`test_malformed_conditional_dependency_shapes_are_rejected`) retains both
original negatives. Every new identifier is manufactured `demo-*` data; no
workspace path, real-run value, disposition, or refusal text appears in the
delta. `tools/scaffold_live_acts.py` and `workspace-seed/` remain untracked
and untouched. The original review's passing checks are not disturbed: the
evaluator, runner, record, and NPE paths have no code change in this delta.

## Charter item 6 — battery re-run (not trusted)

All commands re-run by this reviewer on the branch at `b522e47`
(tree identical to `595c4e1` plus the re-review charter doc):

| Command | Result |
|---|---|
| `.venv/bin/python3 -m unittest tests.derivation.test_conditional_multi_dependency -v` | 15/15 **OK** (all five new/extended tests executed and named in the verbose log) |
| `.venv/bin/python3 -m unittest` | `Ran 448 tests` — **OK** (445 pre-repair + 3 new) |
| `.venv/bin/python3 -m mypy` | `Success: no issues found in 93 source files` |
| `.venv/bin/python3 tools/governance_lint.py` | `governance lint: conformant` |
| `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` | exit 0, no findings |

## Findings

### R1 — Lifecycle displacement check composes two act histories — OBSERVATION / non-blocking

In the case-5 test, the published consumer row comes from the stage-3 run
(its own temporary workspace and act log, without the successor), while the
kernel currency asserted against it is computed from the stage-4 act log
(which contains both the original and successor alpha assertions). The
composition is sound because `_surface_and_acts` is deterministic — the
original `demo.cmdn.finding.alpha` assertion in the stage-4 log is
identity-identical to the one the stage-3 publication pinned — so the
demonstrated property (a successor assertion displaces the earlier published
consumer through the existing two-edge currency model) genuinely holds. But
the test models one continuing history as two regenerated ones; a future
change that makes act construction non-deterministic (e.g., unique act or
finding identifiers per invocation) would silently decouple the two legs.
A one-line comment in the test acknowledging the deterministic-regeneration
dependency would protect it. Not a defect in the repair.

### R2 — Pin-mutation test imports a private symbol — OBSERVATION / non-blocking

`tests/derivation/test_conditional_multi_dependency.py:22` imports
`_content_id` from `packages.derivation.runner` to reconstruct the content
identity. This is precisely the committed derivation (which is why the
positive control is meaningful), but it couples the test to a private symbol
rather than a public verification entry point. If a public
verify-finding-identity surface is introduced later, this test should move to
it. Not a defect in the repair; the charter's requirement ("rejection by the
committed content-identity derivation") is met.

## Conclusion

F1–F4 are discharged on the charter's exact terms; the original review's
passing checks stand undisturbed; the battery is green under this reviewer's
own run. Track 0a — the original delta `c0508cb` plus the repair `595c4e1` —
is **ready**. The owner holds the merge (ADR-0030).
