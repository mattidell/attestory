# Review: a selection path collects a keyed family

Reviewed commit: the commit that chartered this review (removed at closeout) on
`milestone/selection-keyed-collect-2025`, diffed against `github/main`.
The orientation SHA matches Git. The worktree was clean at the start of
this review.

Scope understood: a selection path can collect a keyed source family
without any rule publishing a stand-in value under the member fact id; a
selection with one real path and a default needs no path on a fact type
nothing writes; core v86 retires `rule.f1099b-b4-amount-symbol` and the
inert path; every return core v85 computes stays the same, and earlier
cores stay byte-identical. Non-goals: no other change to selection
semantics or the rule language, no edit under `packages/kernel/`, and no
edit to a published schema file.

Box. Inputs are current source findings of the activity's member fact
types, marshalled before the run. Authority for an amount is that current
finding; authority for the empty case is the selection default, not a
published 0 under the amount id. The box may publish the subtotal (the sum,
or literal 0) and, through the existing line 25b rule, that line. It must
not publish under the amount id. Pre-v86 cores and packages other than
`core-calculations` keep the ADR 0077 Part 4 requires equality.

## Findings

### 1. The v86 exemption covers more operators than the collect ADR 0085 names

- File: `packages/derivation/package_validation.py:1063` and
  `packages/derivation/package_validation.py:1104`
- Claim: ADR 0085 Decision 1 omits the activity family's member collect
  from `requires`. The code omits every op in `_COLLECT_FAMILY_OPS`
  (`collect`, `count`, and `collect_categorical_all_equal`) whose
  `(name, source_set)` is an activity member paired with that family.
- Reproduction: read those two sites. On the published v86 surface, the
  only own-family op is the box 4 subtotal's `collect`. Forcing the same
  predicate over a count or `collect_categorical_all_equal` of that pair
  would drop it from `requires` too. A count of the family member predicate
  was already excluded as a closed-family count with the switch off.
- Consequence: contract text is narrower than the code. No adopted v86
  path changes today. Evidence, not a wrong line value.
- Severity: note
- Fix: in `_iter_selection_dependency_names`, set `activity_collect` only
  when `op == "collect"`. Leave `count` on the existing closed-family
  exclusion.

### 2. The Track 0 walk summary drops the member amount lines

- File: `docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence/track0.py:160`
- Claim: `recorded_values_in_walk` is the list of recorded amounts shown
  in the walk. It keeps a line only when the line contains
  `statement-box4-withholding=` or the subtotal token.
- Reproduction: published core v86, synthetic `demo.skc.review.v86.two_statements`,
  through `live_coordinate_run` (the Track 1 `execute` helper). The subtotal
  walk contains
  `f1099b.statement-box4-withholding|statement=demo.sfa.s1.statement,tax-year=2025=150.0`
  and the same shape for `demo.sfa.s2.statement` at 40.0. The summary field
  was `['190.0']` only, because the member lines use `|` before `statement=`
  and never `statement-box4-withholding=`. `walk_claims`, which the v86 test
  calls, searches the raw walk and reported no failure on this run.
- Consequence: evidence. A reader of that summary field would miss the
  member amounts. The test does not read the field.
- Severity: note
- Fix: treat a walk line as a member amount when it contains
  `statement-box4-withholding|` or `statement-box4-withholding=`, and take
  the value after the last `=`.

## Checks

1. **Engine.** The switch is `selection_collect_satisfied_by_family` in
   `packages/tax/loader.py:110`. It is true only for
   `tax.us.2025.package.core-calculations` at version rank 86 or higher.
   Measured: v86 and v87 true; v85, v84, and v1 false; an interest-slice
   package at v86 false; `86` and `latest` false. `packages/derivation/`
   has no other caller. The runner was not given a new wait. `_selection_eligible`
   (`packages/derivation/runner.py:1197`) still waits on declared `requires`
   and on `reads_subject_results`. Marshal is unchanged aside from admitting
   `rule-artifact.v16` to the ref walk.

   A package-valid v86 path does not run before its collect's members are
   current. Activity reads `current_source_fids`, filled once from the
   marshalled current findings (`packages/derivation/runner.py:611`).
   `collect` reads that same initial source snapshot
   (`packages/derivation/evaluator.py:469`). The retired stand-in publishes
   literal 0 with empty `requires`; it was never a wait for member currency.
   On the superseded case the walk input is 250, not the displaced 100. On
   the withdrawn case the subtotal walk has no amount input.

   A family the activity does not name stays a dependency. An in-memory
   foreign collect of `f1099int.box4-withholding` with empty `requires` on
   a v86 package id produced `RULE_SELECTION_DEPENDENCIES_INVALID` and
   expected that name. Listing it cleared the issue. The runner will still
   evaluate a collect whose name was left out of `requires` if validation
   is skipped. ADR 0085 assigns that check to validation. The published
   subtotal names its own family and has empty `requires`.

   Pre-v86 packages are not edited (`package.core-calculations.v86.json` is
   added; v85 and earlier are not in the diff). `packages/kernel/` is not
   in the diff. The published v85 surface has zero
   `RULE_SELECTION_DEPENDENCIES_INVALID` issues with the switch at its
   committed threshold. Setting that threshold to 85 makes the v85 subtotal
   v1 fail validation, because its `requires` still lists the amount id and
   the switch expects `[]`. Restoring the threshold returns v85 to false.
   Removing the switch (threshold above 86) makes the published v86 subtotal
   v2 fail the same code, expecting the amount id. No other v86 selection
   path collects its activity family (65 paths scanned; one own-family op).

2. **Schema.** `rule-artifact.v16` differs from v15 only in `paths.minItems`
   (2 to 1), `$id`, `schema.const`, and `title`. `artifact-package.v42`
   differs from v41 by admitting `rule-artifact.v16` in the member enum,
   the `admitted_schemas` enum, and one `allOf` guard, plus `$id`,
   `schema.const`, `title`, and `description`. `published.json` adds those
   two filenames and changes no existing checksum. Both new checksums match
   the file bytes. v15 and `artifact-package.v41` are byte-identical to
   `github/main`. A one-path body with `schema` set to `rule-artifact.v15`
   is rejected by `DerivationSchemas.validate_declared`; the errors name
   `minItems` / too short. The same body validates as `rule-artifact.v16`.
   Enumerations under `packages/` that mentioned v15 and not v16 are only
   the untouched v15, v40, and v41 schema files.

3. **Tax result.** Six `live_coordinate_run` calls on published core v86
   (registry v84, release v84), `loader_from` none, synthetic `demo.skc.review.v86.*`
   acts from this milestone's case builders. All six returned success and a
   valid presentation. No publication under the amount id. No
   `rule.f1099b-b4-amount-symbol` row. The subtotal walk does not name the
   stand-in.

   | Case | Line 25b | Subtotal | Walk inputs |
   | --- | --- | --- | --- |
   | no amount | 0 | 0 | none (default 0) |
   | one amount 150 | 150 | 150 | 150 on `demo.sfa.one.statement` |
   | zero | 0 | 0 | 0.0 on `demo.sfa.one.statement` |
   | two statements 150 and 40 | 190 | 190 | 150 and 40 on `demo.sfa.s1` and `demo.sfa.s2` |
   | superseded 100 then 250 | 250 | 250 | 250 only |
   | withdrawn 150 | blocked | 0 | none |

   Withdrawn line 25b is `DEPENDENCY_ABSENT`, missing
   `tax.us.2025.f1099b.statement-box4-withholding`, sentence asking for box 4
   on each recorded sale (blank box 4 entered as 0). That is the hand result
   of a sale with no current box 4 amount. The subtotal default is 0 and is
   not published under the amount id. The 298 recorded-catalog runs were not
   re-executed here. Their test compares `pin()` to the committed v83 fixture
   and does not itself assert these walks.

4. **ADR 0085.** Decision 1 matches the loader gate, the validation
   omission, the unchanged marshal, and the runner's existing requires wait.
   Decision 2 matches the v16 diff. Decision 3 correctly supplements ADR 0077
   Part 4: Part 4 still requires at least two paths and still counts a
   collect-family name as `requires` except for a per-subject read and a
   closed-family count; v16 is the one-path successor; the requires omission
   is the package switch, not a silent edit of Part 4. Line 2b v8 stays on
   `rule-artifact.v9` and is outside `is_v13_selection_rule`. No expression
   operator was added. The extra ops in finding 1 are the only behavior the
   decision text does not name. The record is still **proposed**. This review
   does not accept it. The plan withholds a ready PR until the owner does.

5. **Design weight.** The package id and version are the smallest gate that
   leaves every earlier core on the old equality. Binding keyed members as
   one symbol would change marshal for every core. A schema-only edit would
   not stop the runner waiting on a `requires` entry. The other inert paths
   should stay parked. v16 is the only v86 selection with one path (64 paths
   still have two). Those v15 rules do not collect their activity family, so
   the switch does not change their `requires`, and the whole v86 surface
   has zero selection-dependency issues. A switch test of one inert path
   would not fail if this switch were removed. The v15 one-path rejection
   already pins `minItems`.

6. **Tests.** In memory, raising the switch threshold above 86 makes
   `rule.f1099b-b4-withholding-subtotal` v2 fail validation on a v86 package
   id (expected `requires` is the amount id). Lowering it to 85 makes v1 fail
   on the published v85 surface (expected `requires` is `[]`). Both are the
   assertions in `tests/test_selection_collect_by_family.py`. The package
   test's byte comparison is honest about the body. `prototype._subtotal_v2`
   emits `rule-artifact.v15`. The test assigns `rule-artifact.v16` and then
   compares bytes. The only field that differed before that assignment was
   `schema`. Any other drift fails the comparison. The test says it stamps
   the schema.

7. **CI and isolation.** The new live module's 298 catalogue ids are
   partitioned once: the identical set and the present=no set are disjoint
   and cover the fixture (the split test asserts that). No id is scheduled
   twice. The six design cases are separate act lists; they are the runs
   that assert the walk and the absent amount publication. The catalogue
   repetition against the older v83 live module is the identity claim, not
   a second execution of the same v86 acts. `test_recorded_split_is_207_identical_and_91_asks`
   only reads JSON. It is still on the live lane because the module source
   contains `live_coordinate_run`. That is one cheap test in the slow lane,
   not a redundant coordinator run. Neither new test module assigns an
   attribute of another module. The package loader does not register the
   prototype. The live loader registers only its own private module names.

8. **Data safety.** `python3 tools/envelope_scan.py --range github/main..HEAD`
   exited 0. This review records no absolute path and no temp-directory path.

## Verdict

**ready.** Blocking list: none.

The two notes above do not change the published v86 result. ADR 0085
remains proposed.
