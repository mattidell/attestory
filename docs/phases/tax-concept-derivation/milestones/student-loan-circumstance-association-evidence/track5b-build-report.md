# Track 5b build report — per-subject scheduling and runtime presence (ADR 0076 Parts 1–2, runtime half)

Builder unit. Scope: `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/charter-track5b-per-subject-scheduling-and-presence.md`.
Not committed; left for foreman review per the charter's hand-off. Base: Track 5a
(`rule-artifact.v11` / `artifact-package.v32`, commit `1cfae2b8`), unchanged by this unit.

## `packages/derivation/runner.py` — Part 1, scheduling

**`_Run.use_v2`** (~line 254) and the matching set in `run_and_record` (~line 2477): both admit
`rule-artifact.v11` alongside v10 — a v11 rule always produces `derived-finding.v2` (subject
dispatch's own publication helpers are unconditionally v2), so the ledger-pin/`origin` machinery
must be live whenever a v11 rule is present. This is the charter's "admit v11 as v10" instruction
for the rule-schema sets in this file.

**`is_eligible`** — one new branch, immediately before the final `all(req in self.symbols ...)`
fallback, after every pairing/nominee special case (undisturbed):

```python
if isinstance(rule.get("subject"), dict):
    return self._subject_scheduling_eligible(rule)
```

Two new helper methods:

- `_subject_scheduling_predecessor_names(rule)` — `rule["requires"]` plus, for every
  `link_coverage` node in `rule["value"]` (found via `package_validation._iter_link_coverage_nodes`,
  imported lazily), that node's `reductions` name if not already present. This is the ADR's "a
  predecessor is a rule ... whose `publishes` equals one of this rule's `requires` entries, or
  equals this rule's `link_coverage.reductions`."
- `_subject_scheduling_eligible(rule)` — for each such name, finds every rule in `ctx.rules` whose
  `publishes` equals it; if none exists, does not wait (continues); otherwise the declared-subject
  rule is eligible only once every such producer rule id is in `self.resolved`. Never consults
  `self.symbols` for these names, since a subject rule's predecessor publishes only a keyed symbol
  (`publishes|fact_id`), which never populates the unsuffixed name.

**`attempt`** — one new branch, beside the pairing intercept (`_try_pairing_scoped`) and before
every other special case:

```python
if isinstance(rule.get("subject"), dict):
    return self._attempt_subject_scoped(rule)
```

New method `_attempt_subject_scoped(rule)`: calls `self.evaluate_subject_scoped_rule(subject_type=
rule["subject"]["id"], rule=rule)` (the existing `_Run` method Track 5a's predecessor left
untouched — it already records every publication/inapplicable/blocked row and adds the rule id to
`resolved`) and reports "published"/"blocked"/"inapplicable" back to the caller in the same shape
ordinary `attempt` uses. `value` is evaluated exactly once per subject, inside that call, and never
a second time at the rule level.

**`finalize_unreached`** — one new branch, first inside the per-rule loop, before the
`ATTACHMENT_SCHEMAS` check and the ordinary guard/value fallback:

```python
if isinstance(rule.get("subject"), dict):
    self.evaluate_subject_scoped_rule(subject_type=rule["subject"]["id"], rule=rule)
    continue
```

Mirrors the ordinary fallback's own posture (no eligibility re-check, a real evaluation, does not
call `attempt`).

**`packages/derivation/reference_runner.py`** — not touched. `run_reference` already shares
`is_eligible`/`attempt`/`finalize_unreached`; its own `resolve()` demands every declared `publishes`
name across the whole rule set at the top level (`for target in sorted(producers): resolve(target)`
inside the `while changed` fixpoint), so a subject rule's predecessor gets its own chance to resolve
independently of whether the successor's own `_requires` walk reaches it — the ADR's "`run_reference`
needs no fourth copy" held; no test forced a change.

## `packages/derivation/subject_dispatch.py` — Part 2, runtime presence

New module-level helpers, none touching `_scope` itself:

- `_identity_names(run, fact_type_id)` — a fact type's declared `identity_keys` names, by id, read
  from `run.ctx.fact_types` (never from a row).
- `_presence_declaration(run, rule)` — `None` when the rule declares neither `joined` nor
  `direction`; otherwise `(joined_id, required_names, reference_id)`, where `required_names` is the
  subject type's own identity names under `joined_contains_subject`, or the joined type's own
  identity names under `subject_contains_joined` (per the ADR's exact wording), and `reference_id`
  is the fact-type id those names were (or should have been) read from.
- `_malformed_joined_rows(sources, joined_id, required)` — every present row of `joined_id` lacking
  a required name (or carrying no keys at all), by **finding id**, sorted.
- `_presence_matched(subject, candidates, required)` — `None` when the subject's own keys are
  unavailable, **or when the subject's own keys omit one of the required names** (foreman-review
  fix, below) — both the same fail-closed contract `_scope` returns; otherwise the candidates that
  are complete (carry every required name) and agree with the subject on every required value. A
  complete-but-disagreeing row ("another subject's") is silently excluded here, not blocked.

**`evaluate_subject_scoped_rule`** — three integration points:

1. Once per rule call (not per subject): computes `presence = _presence_declaration(...)` and, when
   declared, `malformed_finding_ids = _malformed_joined_rows(...)` over the *entire* `sources` list.
2. Inside the per-subject loop, immediately after `symbol_pin`/`local_symbols`/`fact_types` are
   seeded and before the ordinary `invalid`/`absent`/`scoped` machinery: if any malformed row exists
   anywhere, **every** subject blocks `DEPENDENCY_INVALID` with `missing` the sorted malformed
   finding ids, and `continue`s — matching "its owner cannot be determined, so it cannot be excluded
   from any subject."
3. In both existing scoping loops (`other_names`, for an ordinary `requires` source such as
   enrolment; `coverage_names`, for the `link_coverage` operator's keyed sources), the one name
   equal to the declared `joined_id` now calls `_presence_matched` instead of `_scope`; every other
   name — including `reductions`, which Part 2 does not touch — keeps `_scope` unchanged. An
   undeclared rule (`presence is None`) has `joined_id = None`, so every `name == joined_id` guard
   is unreachable and `_scope` applies to every source type exactly as before.

The pre-existing type-level `_present_rows_share_no_key_name`/`unjoinable` check (ADR 0075's
mechanism) is untouched and is reached only when `malformed_finding_ids` is empty; a row that used
to trigger it (sharing zero key names with the subject) now always also lacks at least one required
identity name, so it is caught earlier as malformed and the old check becomes dead code on that path
for a declared rule — left as-is per the charter ("Every other source type the rule reads keeps
`_scope`").

## Foreman review round 1 — two fail-open defects fixed

The independent review found two fail-open gaps in the presence check above. Both are fixed in
`packages/derivation/subject_dispatch.py` only; no other assigned path changed.

**Defect 1 — an unreadable reference identity made presence join everything.**
`_identity_names` legitimately returns `[]` when the reference fact type (the subject type under
`joined_contains_subject`, the joined type under `subject_contains_joined`) is absent from
`run.ctx.fact_types`. `_malformed_joined_rows` then has nothing to check for (`required=[]` makes
`any(name not in row_keys for name in required)` false for every row), and `_presence_matched`'s own
`all(...)` over an empty `required` is vacuously `True` — every row would silently join every
subject, the opposite of fail-closed.

Fix: `_presence_declaration` now also returns `reference_id` (the fact-type id the names were read
from). `evaluate_subject_scoped_rule` computes `identity_unreadable_type = presence[2]` whenever
`presence is not None and not required_names` — an empty name list is never treated as "nothing
required"; `fact-type.v2` always requires at least one named identity key, so empty means unread,
not read-as-empty. When set, **every** subject evaluating the rule blocks `DEPENDENCY_INVALID` with
`missing = (identity_unreadable_type,)` — the reference fact-type's **id string**, not a finding id.
Per the reader contract (`reader-contract.md` §4), that string is recognized as **class 3, "symbol or
source-set name"** ("it is a fact-type id in the resolved graph, and it is not a finding id in
state"), never the finding-id lookup (class 4) — the projector shows the type id as text, not as a
resolved finding. This check runs before the malformed-row check (which needs `required_names` to
mean anything) and short-circuits it: `malformed_finding_ids` is computed only when
`identity_unreadable_type is None`.

**Defect 2 — a subject missing its own required name took the no-link result.**
`_presence_matched` only checked `subject_keys is None`; a subject whose keys were a real dict but
missing one of the *required* names (e.g. a statement fact keyed on `statement`/`tax-year` but not
`lender`) fell through to the comparison loop, where every candidate row's required-name check
against `subject_keys.get(missing_name)` (`None`) simply never agreed — producing an empty match
list indistinguishable from "no links at all," so the subject silently took the no-link parameter.
ADR 0076 Part 2 requires the no-link result only "when its own keys are present" — present in full,
not partially.

Fix: `_presence_matched`'s guard is now `if subject_keys is None or any(name not in subject_keys for
name in required): return None`. This reuses the **existing** "subject keys unavailable" fail-closed
path unchanged in both call sites — inside a `link_coverage` rule the caller's `coverage_names` loop
already turns a `None` match into the `KEYS_UNAVAILABLE` sentinel, which the evaluator already blocks
`DEPENDENCY_INVALID` / `link-coverage-keys-unavailable` on (ADR 0075's existing diagnostic marker,
already in the reader contract's class-1 table); for an ordinary `requires` source (the
`subject_contains_joined` enrolment case) the `other_names` loop's existing `invalid.append(name)`
path fires, blocking `DEPENDENCY_INVALID` naming the required symbol. Neither path is new code; only
the condition that reaches them is broadened. A subject with `keys is None` entirely is unaffected —
same behaviour as before this fix.

## Tests

### `tests/derivation/test_per_subject_scheduling.py` (Part 1, 7 tests, all new)

Every test builds `rule-artifact.v11` rules (declaring `subject` only) and drives them through
`packages.derivation.runner.run` and `packages.derivation.reference_runner.run_reference` directly
(never hand-called `evaluate_subject_scoped_rule`), except where noted.

- `DeclaredSubjectDispatchesPerSubject.test_dispatches_per_subject_and_does_not_evaluate_once` — two
  statement subjects, one rule; both runners publish exactly the two keyed symbols and never the
  unsuffixed name; publication ids agree between runners.
- `PredecessorChainThroughRealSchedulers.test_blocked_predecessor_releases_successor_and_fails_closed`
  — status/reduction/coverage chain (financing → link → statement), one financing missing its
  enrolment: status blocks `DEPENDENCY_ABSENT` for that financing, its reduction blocks
  `DEPENDENCY_ABSENT` missing `[STATUS]`, and the statement blocks `DEPENDENCY_INVALID` missing the
  uncovered link's finding id, never taking the no-link parameter. Both runners agree (same
  publication id set).
- `...test_inapplicable_predecessor_releases_successor` — same chain with a guarded status rule
  false for one financing (inapplicable, not blocked); the successor still sees no source and
  blocks the same way.
- `...test_reversed_declaration_order_still_waits_for_the_reduction_publisher` — the coverage rule
  is listed **first** in `ctx.rules` (reduction and status after it); asserts the final published
  value is the correct `900`, not a permanently-stuck "uncovered" block — the only way that value
  can be reached is if eligibility genuinely waited for the reduction rule to resolve rather than
  firing prematurely on the first saturation pass (a one-time-resolved rule can never retry).
- `DontWaitWhenPublisherIsAbsent.test_missing_predecessor_rule_does_not_block_eligibility` — a
  coverage rule alone in the package (no reduction rule at all); asserts `is_eligible` is
  immediately `True` on a freshly constructed `_Run`, and both real schedulers publish the no-link
  default.
- `FinalizeUnreachedSubjectPath.test_finalize_unreached_dispatches_the_declared_subject_rule` — calls
  `_Run.finalize_unreached()` directly (no prior saturation loop), the same shape the pre-existing
  v10 finalize probe uses; asserts the rule id is resolved and the expected finding published.
- `V10Unaffected.test_v10_rules_still_evaluate_once_unsuffixed_and_agree` — reproduces
  `tests.test_sli_g2_binding_probe.Schedulers.test_both_runners_record_ordinary_absence_and_agree`
  verbatim in assertion shape after this unit's edits: v6/v10 rules still evaluate once, unsuffixed,
  and both runners still miss the chain identically.

### `tests/derivation/test_relationship_presence.py` (Part 2, 8 tests, all new)

Every test builds a `rule-artifact.v11` rule declaring `subject`, `joined`, and `direction` (reusing
Track 5b's own Part 1 rule builders from `test_per_subject_scheduling.py`, extended with the
relationship fields) and drives it through `run`/`run_reference`, except the one v10 comparison
noted below.

- `FullStatementIdentityJoinsOnlyItsStatement...` — `joined_contains_subject`; full statement
  identity plus borrowing; each statement gets its own reduction only (`900`/`360`).
- `MalformedLinksBlockEverySubject.test_link_missing_statement_blocks_every_subject` and
  `...test_link_keyed_on_borrowing_only_blocks_every_subject` — a link lacking the statement's
  identity blocks **both** subjects' amount rules `DEPENDENCY_INVALID`, naming the malformed link's
  finding id, never the no-link parameter.
- `...test_v10_rule_still_drops_the_same_malformed_rows` — the **same** malformed/unjoinable
  fixtures against the undeclared v10 `_coverage()` rule, hand-dispatched (the only test in either
  new file that does this, and only because a v10 rule is never scheduled per-subject in production
  — the same posture `tests.test_sli_g2_binding_probe.SubjectLocalNoLink` records): both rows are
  still silently dropped and S2 still takes the parameter, proving the old path is untouched.
- `AnotherSubjectsCompleteLinkDoesNotBlockThisSubjectsNoLink...` — the two-statement case: S1's own
  complete link does not block S2, and does not prevent S2's no-link result.
- `IdenticalKeyValuesStillJoinBothFacts...` — residual 2, asserted as a residual: two statement
  facts with identical identity values both join the one fully-keyed link (`900`/`300`).
- `SubjectContainsJoinedAppliesTheSameClassification.test_full_enrolment_reaches_both_borrowings_of_one_situation`
  — `subject_contains_joined`; a full-identity enrolment reaches both borrowings of its situation
  and not the third.
- `...test_malformed_enrolment_row_blocks_every_subject` — an enrolment row missing `programme`
  blocks every financing subject `DEPENDENCY_INVALID`, naming the malformed row — the symmetric case
  for the other direction.

### Foreman review round 1 fixes — 3 new tests, `tests/derivation/test_relationship_presence.py`

All three build v11 rules on the declared fields and run through `run` and `run_reference`, both
runners asserted to agree, matching the review's own executed scenarios.

- `UnreadableReferenceIdentityFailsClosed.test_missing_fact_type_blocks_every_subject_naming_the_type_id`
  — the reviewer's exact Defect 1 fixture (S1 lender-a/statement-1/1000 with its own link+reduction;
  S2 lender-b/statement-2/400; `fact_types=[]`): **both** subjects now block `DEPENDENCY_INVALID`
  with `missing == [BOX1]` (the fact-type id, confirmed not equal to either box-1 finding id or the
  link finding id), and no publication happens for either.
- `SubjectMissingOwnRequiredNameFailsClosed.test_joined_contains_subject_variant` — the reviewer's
  exact Defect 2 fixture (S2 keyed on `statement`/`tax-year` only, no `lender`, with the statement
  fact type properly declared this time): S1 still publishes `900` unaffected; S2 now blocks
  `DEPENDENCY_INVALID` with `missing == [link-coverage-keys-unavailable]` and no parameter pin —
  never the no-link `400`.
- `...test_subject_contains_joined_variant` — the symmetric case: a financing subject missing
  `programme` from its own keys (the joined enrolment type's own declared identity requires it)
  blocks `DEPENDENCY_INVALID` naming `ENROLMENT`; a sibling, fully-keyed financing subject in the
  same run is unaffected and still publishes its status.

## Verification tails (verbatim)

```
$ python3 -m pytest tests/derivation/test_relationship_presence.py -q
...........
11 passed in 2.98s
```

```
$ python3 -m pytest tests/derivation/test_per_subject_scheduling.py tests/derivation/test_relationship_presence.py tests/test_sli_g2_binding_probe.py -q
......................................
38 passed in 3.08s
```

```
$ python3 -m pytest -n auto -q
2263 passed, 20 skipped, 4422 subtests passed in 123.60s (0:02:03)
```

(2263 = the pre-fix 2260 + this round's 3 new tests; 20 skipped unchanged; no regressions.)

```
$ python3 -m mypy
Success: no issues found in 280 source files
```

```
$ python3 tools/governance_lint.py
governance lint: conformant
```

```
$ git diff --check
(no output — clean)
```

```
$ git status --short
 M packages/derivation/runner.py
 M packages/derivation/subject_dispatch.py
?? docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track5b-build-report.md
?? package-lock.json
?? tests/derivation/test_per_subject_scheduling.py
?? tests/derivation/test_relationship_presence.py
```

`package-lock.json` is pre-existing untracked state in this worktree, not touched by this unit.
`packages/derivation/reference_runner.py` has no diff — the ADR's prediction that it needs no
fourth copy held. Not committed; HEAD unchanged at `1cfae2b8` throughout, including this round.

## Stop conditions

None met. In particular:

- No evaluator arm, `_scope`, a published schema, `derivation-record`, or pairing needed a change —
  `_scope` itself is byte-identical; Part 2 only changes which function a caller passes a joined
  type's candidates through.
- The two runners needed no different code — `reference_runner.py` is untouched, and every new test
  asserts `run` and `run_reference` agree.
- No existing test failed at any point, including every `tests/test_sli_g2_binding_probe.py` test —
  all 23 (including the two `..._dropped_today` tests) pass unchanged; they were never edited.
- The ADR was not ambiguous on a point this unit had to decide. The one implementation choice not
  spelled out verbatim — treating a joined row with `keys is None` (no keys at all) as malformed,
  and using each malformed row's `finding_id` (not `fact_id`) in `missing` — follows directly from
  the ADR's own text ("its owner cannot be determined" and "the malformed rows' finding ids
  (recorded findings, so a reader can name them)").

Review round 1's fixes stayed inside the same file (`subject_dispatch.py`) and did not touch
`_scope`, an evaluator arm, or a schema either; both new fail-closed paths reuse existing block
machinery rather than adding a new one.
