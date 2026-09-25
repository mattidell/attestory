# Track 5c build report — carrying declarations from package to execution

Builder unit. Scope: `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/charter-track5c-declaration-to-execution.md`.
Not committed; left for foreman review per the charter's hand-off. Base: Track 5b's build (HEAD
`02d82ab7` on `milestone/student-loan-circumstance-association`), unchanged by this unit except as
below.

**A stop condition was hit on final verification** (see "Stop condition met", below): one existing
test outside this unit's assigned paths now fails, as an unavoidable and charter-correct consequence
of Defect 1's fix. All three defects are reproduced, fixed, and tested as chartered; the full-suite
run surfaces this one downstream assertion that needs a foreman/owner decision before the unit is
mergeable, the same shape Track 5a's own build report flagged for its own out-of-scope enumeration
test.

## Defect 1 — declared subjects and relationships do not reach live execution

**Reproduced first.** `tests/derivation/test_subject_declaration_live_path.py` built a real
`artifact-package.v32` package (subject-only v11 rule, a standalone `fact-type.v2` member, no bundle),
ran it through `validate_package` → `_resolved_run_material` → `marshal_run_context` → `run`/
`run_reference`. Before the fix: `material.emission_only_names == ()` and both runners produced zero
publications and zero dispositions for the rule — the exact defect. Confirmed by running the whole new
file against the pre-fix code (see "Reproduction run", below): 8 of 9 tests failed, all for this reason
or Defects 2/3 (Defect 1 sits upstream of dispatch, so its absence also silences the Defect 2/3
scenarios, which declare a subject too).

**Fix**, `packages/derivation/live.py`, `_resolved_run_material` only:

- Standalone `fact-type.v2` members are now added to `fact_types`, alongside the existing
  bundle-contained ones, de-duplicated only on identical `(id, version)` — every declared version of an
  id is kept (needed by Defect 2's fix below, which resolves by exact pin).
- Every `rule-artifact.v11` member's `subject` and `joined` pin ids are added to `emission_only`
  (guarded by `not in collect_names`, matching the existing pattern), not to `collect_names` — an
  emission-only finding is not marked "used" (Track 4's option B), so an unrelated rule sharing the
  same fact-type id keeps its existing scalar binding (see the `EmissionIsNotScalarBinding` test,
  below). No source-family member and no `ref` node were added anywhere.

**What changed for existing packages.** No published schema or `published.json` entry changed. Adding
standalone `fact-type.v2` fact types to the material is additive for any package that only used
bundles (nothing to add). Adding a v11 rule's `subject`/`joined` types to `emission_only` is a genuine
behaviour change for any v11 rule already in play — this is Track 5b's own fixture surface
(`test_subject_relationship_declarations.py`'s `AdmissionSetsTreatV11LikeV10`), which is exactly what
surfaces the stop condition below: one existing test asserted the pre-fix `emission_only_names` shape
for a v11 coverage rule (only its `links` type, not its own `subject` type). That assertion is now
stale per this charter's own explicit requirement.

**Tests** (`test_subject_declaration_live_path.py`):

- `SubjectOnlyRuleStandaloneFactTypes.test_one_keyed_publication_per_statement_both_runners` — a
  subject-only v11 rule over a standalone fact type, two current findings (one per statement); asserts
  `STATEMENT in material.emission_only_names` and one keyed publication per statement from both
  runners, each pinning its own finding.
- `JoinedRowsAreEmittedAndPresenceRuns.test_joining_case_publishes_pinning_the_joined_row` — subject
  FINANCING, joined ENROLMENT, `subject_contains_joined`, both standalone; one matching row; asserts
  both `FINANCING`/`ENROLMENT` are in `emission_only_names` and the rule publishes pinning the joined
  finding.
- `...test_malformed_enrolment_row_blocks_the_subject` — same fixture plus a second, present ENROLMENT
  finding whose `fact_id` is not a lattice fact (so marshal renders `keys=None`); asserts every subject
  blocks `DEPENDENCY_INVALID` naming that finding, never publishes.
- `EmissionIsNotScalarBinding.test_ordinary_scalar_binding_unaffected_by_the_v11_rule` — an ordinary
  (non-subject) rule reading an unkeyed scalar via the legacy fallback, run once alone and once
  alongside an unrelated v11 subject-only rule; asserts the ordinary rule's publication (value and pins)
  is byte-identical either way.

## Defect 2 — runtime does not honour the pinned fact-type version

**Reproduced first.** Same package chain (not hand-populated `RunContext`). A subject fact type
declared at both `v1` (weak: identity `["tax-year"]`) and `v2` (strong: identity
`["lender","statement","tax-year"]`); the rule pins `subject: {"id": ..., "version": "v2"}`. A link row
carrying only `tax-year` is complete under the weak identity (both statements share `tax-year`, so it
cross-joins both) and malformed under the pinned strong identity. Before the fix, `_identity_names`
matched by id only, returning whichever declaration appeared first in the resolved members:
- weak declared first → both statements incorrectly published (the value the malformed link carried),
  never blocked;
- strong declared first → both statements accidentally blocked correctly (the charter's own "reversing
  the declaration order blocked both").

Confirmed against pre-fix code (both this file's live-path tests and the dispatcher-level additions to
`test_relationship_presence.py`): the weak-first case failed (published instead of blocking); the
strong-first case passed by accident, matching the narrative exactly. See "Reproduction run" below.

**Fix**, `packages/derivation/subject_dispatch.py`:

- `_identity_names(run, fact_type_id, fact_type_version)` now takes the version too and matches
  `fact_type.get("id") == fact_type_id and fact_type.get("version") == fact_type_version` — the same
  exact-pin identity `package_validation._exact_pin_key`/`_subject_relationship_issues` resolves
  statically.
- `_presence_declaration` reads both id and version off whichever pin (`subject` or `joined`) is the
  "reference" type for the declared `direction`, and passes both to `_identity_names`. A pin with no
  readable version string is treated the same as an absent fact type (empty required-names list),
  reusing the existing Defect-1 (Track 5b foreman-review) fail-closed path — no new block code.

**Tests:**

- `test_subject_declaration_live_path.py::RuntimeHonoursThePinnedFactTypeVersion` —
  `test_weak_declared_first_still_blocks_both` / `test_strong_declared_first_still_blocks_both`, through
  the full live path; both must block, in either order, naming the malformed link's finding id.
- `test_relationship_presence.py::RuntimeHonoursThePinnedFactTypeVersionDispatchLevel` — the same
  scenario at the dispatcher level (hand-built `RunContext`, this file's own existing convention),
  same two declaration orders, same assertion.

## Defect 3 — a run-wide scalar bypasses a declared relationship

**Reproduced first.** A financing subject, a declared `subject_contains_joined` relationship to
ENROLMENT, zero ENROLMENT rows anywhere in the run — but an ordinary (non-subject) rule elsewhere in
the same package publishes a scalar under the exact symbol name `ENROLMENT`. Before the fix: because
the declared joined type had no rows at all, `other_names` never contained it, `scoped` had no entry
for it, and the `required` loop's `if req in run.symbol_pin and req in run.symbols` branch bound the
subject to that unrelated ordinary rule's value — the subject published using it instead of blocking.
Confirmed failing before the fix in both the live-path test and the dispatcher-level addition to
`test_relationship_presence.py` (see "Reproduction run" below).

**Fix**, `packages/derivation/subject_dispatch.py`, `evaluate_subject_scoped_rule`:

`other_names` is now the union of every source name present in `sources` **plus** the declared
`joined_id` (when the rule declares one), computed before the per-name scoping loop runs. With zero
rows, the scoping loop still executes for `joined_id` (via `_presence_matched`/`_scope` with an empty
candidate list) and sets `scoped[joined_id] = []` — an ordinary empty join, which the existing
`required` loop already handles correctly (declared `optional_default` → take it; otherwise
`DEPENDENCY_ABSENT`). This also means `_local_maps` overwrites the local `sources[joined_id]` entry
with `[]` for every subject's evaluation, so the joined type's value is not readable from the run-wide
environment during that evaluation either — the `run.symbol_pin`/`run.symbols` branch is never reached
for a declared joined name. No evaluator arm, no `_scope` body change, no new block code.

**Tests:**

- `test_subject_declaration_live_path.py::RunWideScalarDoesNotBypassADeclaredRelationship` — three
  tests through the full live path: the bypass itself (`test_no_rows_and_a_run_wide_scalar_blocks_absent_not_the_scalar`,
  asserting `DEPENDENCY_ABSENT` and that the symbol is never published from the ambient value, while
  also confirming the ambient rule really did publish its own ordinary symbol); the ordinary valid
  joined case (`test_ordinary_valid_joined_case_publishes_pinning_the_row`); the declared-default case
  (`test_declared_default_still_takes_its_own_pinned_path`, asserting the manufactured
  `declared_default` finding, distinct from both the bypass and the ordinary case, still carries its own
  visible parameter pin).
- `test_relationship_presence.py::RunWideScalarDoesNotBypassTheDeclaredRelationship` — the same bypass
  scenario at the dispatcher level.

## Reproduction run (all defects, against pre-fix code)

Both `packages/derivation/live.py` and `packages/derivation/subject_dispatch.py` were reverted to
their `HEAD` (pre-fix) bytes (`git show HEAD:<path> > <path>`), the new/extended tests run, then the
fixed bytes restored (no commit was made at any point; `git status --short` before and after matched).

```
$ python3 -m pytest tests/derivation/test_relationship_presence.py::RuntimeHonoursThePinnedFactTypeVersionDispatchLevel tests/derivation/test_relationship_presence.py::RunWideScalarDoesNotBypassTheDeclaredRelationship tests/derivation/test_subject_declaration_live_path.py -q
...
FAILED tests/derivation/test_subject_declaration_live_path.py::SubjectOnlyRuleStandaloneFactTypes::test_one_keyed_publication_per_statement_both_runners
FAILED tests/derivation/test_subject_declaration_live_path.py::RuntimeHonoursThePinnedFactTypeVersion::test_weak_declared_first_still_blocks_both
FAILED tests/derivation/test_relationship_presence.py::RuntimeHonoursThePinnedFactTypeVersionDispatchLevel::test_weak_declared_first_still_blocks_both
FAILED tests/derivation/test_subject_declaration_live_path.py::JoinedRowsAreEmittedAndPresenceRuns::test_malformed_enrolment_row_blocks_the_subject
FAILED tests/derivation/test_subject_declaration_live_path.py::RunWideScalarDoesNotBypassADeclaredRelationship::test_ordinary_valid_joined_case_publishes_pinning_the_row
FAILED tests/derivation/test_relationship_presence.py::RunWideScalarDoesNotBypassTheDeclaredRelationship::test_no_rows_and_a_run_wide_scalar_blocks_absent
FAILED tests/derivation/test_subject_declaration_live_path.py::RuntimeHonoursThePinnedFactTypeVersion::test_strong_declared_first_still_blocks_both
FAILED tests/derivation/test_subject_declaration_live_path.py::RunWideScalarDoesNotBypassADeclaredRelationship::test_no_rows_and_a_run_wide_scalar_blocks_absent_not_the_scalar
FAILED tests/derivation/test_subject_declaration_live_path.py::JoinedRowsAreEmittedAndPresenceRuns::test_joining_case_publishes_pinning_the_joined_row
FAILED tests/derivation/test_subject_declaration_live_path.py::RunWideScalarDoesNotBypassADeclaredRelationship::test_declared_default_still_takes_its_own_pinned_path
10 failed, 2 passed in 3.08s
```

The 2 that passed pre-fix: `EmissionIsNotScalarBinding` (a parity check between two runs that are
equally silent pre-Defect-1-fix, not itself a defect reproduction) and
`RuntimeHonoursThePinnedFactTypeVersion::test_strong_declared_first_still_blocks_both` (the narratively
"accidentally correct" order, exactly as ADR reproduction described it). Every other test failed for
the reason its defect section states. After restoring the fixed files, all of the same tests pass (see
below).

## Files changed

- `packages/derivation/live.py` — `_resolved_run_material` only, as above.
- `packages/derivation/subject_dispatch.py` — `_identity_names`, `_presence_declaration`,
  `evaluate_subject_scoped_rule` (the `other_names` computation only), as above.
- `packages/derivation/marshal.py` — **not touched**. No test proved it needed a change; every
  reproduction and fix lives in `_resolved_run_material`'s admission lists and
  `subject_dispatch.py`'s own scoping/identity logic.
- `tests/derivation/test_subject_declaration_live_path.py` — new, 9 tests, all through
  `validate_package` → `_resolved_run_material` → `marshal_run_context`/`marshal_live_run_context`
  shape → `run`/`run_reference`, over a `packages.kernel.facts.KernelState` fact lattice. No hand-populated
  `RunContext.sources` or `fact_types` anywhere in this file.
- `tests/derivation/test_relationship_presence.py` — 3 tests added (dispatcher-level, this file's own
  existing hand-built-`RunContext` convention): `RuntimeHonoursThePinnedFactTypeVersionDispatchLevel`
  (2 tests) and `RunWideScalarDoesNotBypassTheDeclaredRelationship` (1 test).

## Test counts

- New file: 9 tests, all passing post-fix.
- `test_relationship_presence.py`: 11 pre-existing + 3 new = 14, all passing post-fix.
- Full suite: 2274 passed, 20 skipped, 4422 subtests passed, **1 failed** (the stop-condition finding
  below) — up from Track 5b's 2263 passed baseline by exactly the 8 new + 3 new = 11 tests this unit
  adds net of one pre-existing test's own count (`test_subject_relationship_declarations.py` test count
  unchanged; it now fails rather than passes).

## Out-of-scope finding (per charter, report only)

**A declared-subject rule with zero subject rows records no disposition at all.** Not changed. Traced
in this unit's own `SubjectOnlyRuleStandaloneFactTypes` reproduction (pre-fix): before Defect 1's fix,
a validated subject-only rule with zero sources reached both schedulers, was added to `resolved`
(`_attempt_subject_scoped`/`finalize_unreached`'s per-subject call unconditionally does this), and
produced neither a publication, an inapplicable row, nor a blocked row — total silence, not an error.
This is unrelated to whether sources exist (the loop over `subjects` in
`subject_dispatch.evaluate_subject_scoped_rule` is simply empty) and is unaffected by any of this
unit's three fixes: fixing Defect 1 makes the *rows* reach dispatch when they exist, but a package
containing a v11 rule whose subject type genuinely has zero current facts in this run (a legitimate,
non-error state — the subject type simply has nothing to say about yet) still resolves with zero
dispositions.

Whether an existing record or disposition shape could represent it without a schema change: no.
`derived-finding.v2` publishes are per-subject and keyed; the ledger's `disposition` rows
(`published`/`blocked`/`inapplicable`) are all per-attempt records keyed to a specific evaluation that
happened. There is no existing disposition shape for "this rule id resolved via zero subject
evaluations" — recording that would need either a new disposition kind (a record-shape decision, out of
this unit's stop-condition list: "if a repair needs... `derivation-record`") or overloading an existing
one with a sentinel this unit has no authority to choose. Not changed, per the charter.

## Stop condition met

**"If any existing test fails"** —
`tests/derivation/test_subject_relationship_declarations.py::AdmissionSetsTreatV11LikeV10::test_resolved_run_material_names_the_v11_rule_and_emits_the_link_type`
fails after Defect 1's fix, and only after it (confirmed: it passes against the pre-fix `live.py`, per
the "Reproduction run" section's revert-and-restore, and it is not touched by either of this unit's
other two fixes).

That test builds a v11 coverage rule declaring **both** `subject: {"id": BOX1, ...}` and
`joined: {"id": LINKS, ...}`, `direction: joined_contains_subject`, and asserts
`material.emission_only_names == (LINKS,)` — i.e., only the `joined`/`links` type, not the rule's own
`subject` type. This is exactly the shape Defect 1's required fix changes: this charter states
"Every v11 rule's subject type **and** joined type is added to the emission-only names" (not "only the
joined type when a `link_coverage` node also names it"). The pre-fix `emission_only_names` computation
only ever added a rule's `links` type (via `_iter_link_coverage_link_types`, walking `link_coverage`
nodes specifically); it never looked at a v11 rule's own `subject`/`joined` pins as such. Track 5a's own
test asserted that pre-Track-5c shape, before Defect 1 existed as a named requirement.

`tests/test_sli_g2_binding_probe.py` (both its ordinary tests and its two `..._dropped_today` tests) is
byte-unedited and passes, confirmed in the full-suite run and in every targeted run above.

This is not an implementation choice this unit could avoid while meeting the charter's own Defect 1
text: any fix that adds a v11 rule's `subject` type to `emission_only_names` (required, since the
charter's own reproduced defect is a subject-only rule with no `link_coverage` node at all) necessarily
changes this exact test's assertion for a rule that *also* happens to declare `link_coverage`. I did
not edit `tests/derivation/test_subject_relationship_declarations.py` (not an assigned path) to update
that assertion, per the charter's stop condition and its assigned-paths list.

Flagging for the foreman/owner, the same choice Track 5a's build report flagged for its own analogous
enumeration test: either (a) accept this as an expected, correctly-anticipated assertion update and let
review round update `emission_only_names == (LINKS,)` to `== (BOX1, LINKS)` (or a set comparison, since
this unit's implementation appends `subject` before `joined` when both are present — order is not a
contract either function documents), or (b) treat it as a decision about that test's own contract
requiring separate owner sign-off.

## Verification (verbatim)

```
$ python3 -m pytest tests/derivation/test_subject_declaration_live_path.py -q
.........
9 passed in 3.00s
```

```
$ python3 -m pytest tests/derivation/test_relationship_presence.py -q
..............
14 passed in 3.13s
```

```
$ python3 -m pytest tests/derivation/test_subject_declaration_live_path.py tests/derivation/test_relationship_presence.py tests/derivation/test_per_subject_scheduling.py tests/derivation/test_subject_dispatch.py tests/test_sli_g2_binding_probe.py -q
................................................uu..............
62 passed, 2 subtests passed in 3.20s
```

```
$ python3 -m pytest -n auto -q
...
FAILED tests/derivation/test_subject_relationship_declarations.py::AdmissionSetsTreatV11LikeV10::test_resolved_run_material_names_the_v11_rule_and_emits_the_link_type
1 failed, 2274 passed, 20 skipped, 4422 subtests passed in 123.87s (0:02:03)
```

```
$ python3 -m mypy
Success: no issues found in 281 source files
```

```
$ python3 tools/governance_lint.py
governance lint: conformant
```

```
$ git diff --check
(no output -- clean)
```

```
$ git status --short
 M packages/derivation/live.py
 M packages/derivation/subject_dispatch.py
 M tests/derivation/test_relationship_presence.py
?? package-lock.json
?? tests/derivation/test_subject_declaration_live_path.py
```

`package-lock.json` is pre-existing untracked state in this worktree, not touched by this unit. Not
committed; HEAD unchanged throughout.

## Everything else in the charter's stop-condition list

Not triggered: no published schema, ADR change, evaluator arm, `_scope` body, pairing, or
`derivation-record` change was needed; the two runners needed no different code (every test above
asserts `run` and `run_reference` agree); `marshal.py` needed no change (no test proved otherwise); and
no repair changes scalar binding for a rule that does not declare a subject —
`EmissionIsNotScalarBinding`'s test is the direct proof for Defect 1's emission-only change, and
Defects 2/3's fixes are confined to declared-subject dispatch (`_identity_names`,
`_presence_declaration`, and the `joined_id`-only widening of `other_names`, which is unreachable for
any rule that does not declare `joined` — `joined_id` stays `None`).
