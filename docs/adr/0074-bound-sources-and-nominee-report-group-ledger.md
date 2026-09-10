# ADR 0074 — Bound Sources and Nominee Report-Group Disposition Ledger

- Status: **accepted** (owner disposition 2026-09-09. Track 0 of
  nominee-interest-tax-consequence-supportability selected the design; it
  was independently reviewed, and this contract received its own focused
  independent review before ratification.)
- Tier: 2 — a rule-language operator and a disposition-ledger cardinality
  exception that Track 1 will implement against; not a product-thesis or
  governance-meaning decision
- Date: 2026-09-09

## Context

Track 0 of the nominee-interest tax-consequence-supportability milestone
selected two coupled mechanisms that cannot be left implicit for
implementation: a new expression operator that binds a coordinator-selected
allocation group into an adopted rule, and a disposition-ledger shape in
which that one adopted rule records one identified row per classified
report-group rather than one row per rule. Both selections live in the
milestone plan's `## Track 0 adversarial closure`
(`docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md`).

Independent review verified the load-bearing claims about committed
behavior before this text was written. Its conclusions are stated here
rather than left as a pointer to a process record: no committed
`rule-artifact.v7` mechanism satisfies the report-local-input
requirements — `collect` needs a real source family, `count` always needs
closure, `collect_categorical_all_equal` folds no decimals, pairing's 1:1
`replace`-and-`ref` is not a variable-length group, a list-valued `ref` is
tolerated evaluator behavior rather than an admission contract, and a
coordinator pre-sum would take arithmetic away from the rule; `symbol` on
a blocked disposition row is a committed capability, not an invention; and
the coordinator loop already emits per-group rows as **executable
behavior**, which is evidence rather than a ledger contract — the gap this
ADR closes.

This ADR is that ledger contract and the operator contract, written so
Track 1 implements a ratified text rather than writing one by implication.
It does not reopen the tax conclusion, remainder shape, Schedule B
boundary, legacy path, C0 product meaning, or the source-family
prohibition. Those remain as Track 0 closed them.

The two contracts are coupled: Contract A is how one nonempty
report-local allocation group becomes a typed input to the adopted rule;
Contract B is how that rule's outcomes are identified on the ADR-0008
closing-record ledger. Neither is usable as the Track 0 selection without
the other.

## Decision

1. **Operator generality versus production authorization.** State the
   boundary precisely, because this ADR does both things and they are
   different:

   `bound_sources` **is** a declared grammar operator introduced at the
   schema level (`rule-artifact.v8`), with **general** syntax,
   evaluation, dependency, and provenance semantics: any citizen of that
   schema may declare it, and Decision 2's **name discovery,
   reachability, authorization-closure, consumed-input, fail-closed
   evaluation, and pin** rules apply uniformly to every such
   declaration. Those semantics are deliberately not rule-specific — a
   per-rule operator would be the special case that rots.

   What is **not** general is **package acceptance of a live binding
   path**. Three layers must be kept apart, and "admission" alone is too
   coarse a word for them:

   1. **Schema validity.** A copied declaration may be perfectly
      **schema-valid** under `rule-artifact.v8`. Nothing about the
      operator's syntax is reserved to one rule.
   2. **Generic dependency analysis.** Its `bound_sources` names are
      still discovered, required to identify a fact type declared by an
      admitted bundle, and still contribute reachability and
      authorization-closure edges. Those checks are not rule-specific
      and must not be skipped for a rule this ADR does not authorize.
   3. **Package acceptance.** It is nonetheless **not
      package-admissible** without an authorized coordinator/binding
      registry entry. **This ADR authorizes that entry for
      `tax.us.2025.rule.interest.nominee-reduction` only.** A copied
      declaration therefore has no coordinator to populate
      `bound_sources`, and Decision 2h requires the package to be
      **refused** (`MEMBER_NO_BINDING_PATH`) rather than admitted with a
      silently inert rule.

   So another rule **may not acquire a binding path merely by copying the
   operator**. Supporting a second rule requires an explicit contract
   decision and a registry extension — a later ADR, not an
   implementation detail.

   Within that boundary there is still **no reusable grouped-rule class,
   no static grouped-dispatch marker, no generic coordinator framework,
   and no general authorization to bind any rule but the one named
   here.** This sentence is part of the contract, not commentary. The exception in
   Decision 3 applies to the exact rule named there and does not spread by
   imitation of row shape, coordinator presence, or a suffixed `symbol`.
   A later reusable class would require a **package-visible declaration**,
   and emitted suffixes would then be **required output of members, never
   the membership test**. An earlier drafting of this decision said "no broader
   grammar abstraction"; that is withdrawn as inaccurate, because the
   grammar **is** extended — by one operator with general semantics. What
   is withheld is the *class*, the *marker*, the *framework*, and any
   general authorization to bind rules other than the one named here.

2. **Contract A — `bound_sources`.** A typed report-local input that
   supplies one coordinator-selected, **nonempty** group of values for
   one named fact type.

   **2a. Declared shape.** Additive `rule-artifact.v8` (v7 bytes
   untouched; ADR-0003 / Article 9) adds one `expr` `oneOf` branch:

   ```json
   {
     "type": "object",
     "properties": {
       "op": { "const": "bound_sources" },
       "name": { "type": "string", "minLength": 1 }
     },
     "required": ["op", "name"],
     "additionalProperties": false
   }
   ```

   There is **no** `source_set` property, so a sentinel family id cannot
   be smuggled onto the operator. Package admission of a v8 citizen
   requires additive `artifact-package.v28` (v26 bytes untouched; v27 is
   already proposed on `milestone-schema-ledger` by another milestone).

   **2b. Not ordinary `collect`; outside ADR-0035's source-family
   requirement for that reason.** ADR-0035's production condition rejects
   "any rule whose collect targets a non-family fact type"
   (`docs/adr/0035-dividend-composition-and-lines-3a-3b.md`, Production
   conditions). `_iter_collect_exprs` yields a node only when
   `expr.get("op") == "collect"`
   (`packages/derivation/package_validation.py`);
   `COLLECT_TARGET_NOT_FAMILY` (same module) and
   `audit_collect_authority` (`packages/derivation/source_authority.py`)
   inspect collect only. Independent review re-traced those walks and
   confirmed that a non-`collect` op is not subject to the collect-family
   rule — not because a validator currently fails to look at it, and not
   because `universe_guard_active` is inactive on production
   `artifact-package.v26` (allowlist ends at v17; Track 0 known
   limitation). This operator remains valid if that intended guard is
   later applied to current package schemas. Ordinary `collect` of
   `tax.us.nominee-allocation.amount` remains the thing the intended
   guard would refuse, because no package source-family declares that
   type.

   **2c. No source family or closure mapping for the allocation fact
   type.** None is introduced for `tax.us.nominee-allocation.amount`. An
   empty group is never collected to manufacture a zero: missing
   `env.bound_sources[name]` or `[]` raises `DEPENDENCY_ABSENT` with
   `missing=[name]`. It does not return `[]` (`add` plus `_flatten` in
   `packages/derivation/evaluator.py` would fold that to a zero) and does
   not raise `SOURCE_SET_UNCLOSED` (that would be a closure claim). The
   coordinator never schedules a report-only group into `evaluate`; that
   empty-input raise is the ordinary-evaluation / wrongly-scheduled-empty
   defense, not C0's product meaning.

   **2d. Name discovery, admission, and dependency integrity.** A walker
   `_iter_bound_source_names` yields `expr["name"]` for
   `op == "bound_sources"` only, applied to both `when` and `value`,
   matching `_iter_ref_names`. Each discovered name must identify a fact
   type declared by an admitted bundle member (`bundles_for_fact` in
   `package_validation.py`); otherwise the package is refused
   (`BOUND_SOURCE_TARGET_UNDECLARED` on the existing member-issue
   surface). The name contributes an inbound package-reachability edge
   (`adj[rule_id].update(bundles_for_fact[name])`, the same edge shape
   declared refs already use) and an authorization-closure edge
   (`edges[cid].update(bundles_for_fact.get(name, set()))` in
   `authorization_closure.py`). An omitted or unreachable declaring
   bundle therefore fails validation, and the authorization digest is
   sensitive to that dependency. Today both graphs build edges only from
   `_iter_ref_names` and `_iter_collect_source_sets`
   (`package_validation.py` reachability adjacency;
   `authorization_closure.py`); without these edges the allocation
   vocabulary would be invisible — a silent integrity hole, not a
   cosmetic gap.

   Note precisely what this edge does and does not replace. A rule's
   only committed route to a *bundle* is `binding_fact_types` — that is,
   an `input_bindings` row — so a bare `ref` reaches no bundle, and
   **`publishes` creates no bundle edge at all**. This ADR adds exactly
   one new edge kind (`bound_sources` → declaring bundle) and invents no
   repository-wide `publishes` → bundle edge. Members that this ADR's
   rule does not reach must be made reachable explicitly: the rule itself
   and the new output vocabulary are **`entrypoints` pins** (vocabulary
   bundles are already entrypoints in committed content), while the
   f1099int vocabulary is already reached by an existing path through the
   box-1 subtotal rule's `source_set` → `source-family.v1` → bundle
   chain, not by this rule's `ref`. The milestone plan's v36 topology
   states this in full; `MEMBER_UNREACHABLE` must be empty for the
   concrete package, which is what proves the topology.

   **2e. Consumed-input restrictions continue to apply.** `consumed` is
   currently `collect_names | requires | ref names`
   (`package_validation.py`). `bound_sources` names join that set, so
   existing prohibitions — in particular ADR-0035's "no rule may collect
   recorded-non-composable content" — keep applying. The operator is not
   a route around a restriction that exists for the content.

   **2f. Evaluator behavior outside the coordinator is fail-closed.**
   The operator reads **only** `env.bound_sources.get(name, [])`. It
   never reads `env.sources`. Ordinary `_Run.env()`
   (`packages/derivation/runner.py`) does not populate `bound_sources`,
   so it is `{}`. Evaluation of the same rule against that run-wide
   environment raises `EvalBlocked(DEPENDENCY_ABSENT, [name])` and cannot
   silently fold run-wide allocation values (the P2 C10/C12 leak).
   Cross-report isolation is therefore a property of the operator
   contract, not of the caller. That raise is not the honest C0-only
   disposition (Decision 3); the `_Run.attempt` intercept and
   `resolved.add` after the coordinator loop remain load-bearing for
   that honesty. Independent review re-traced this path.

   **2g. Pin isolation is part of the same contract as value isolation.**
   Cross-report isolation has two halves, and 2f closes only the value
   fold. The pin fold must close too, or a report-local *value* would
   still carry run-wide *provenance*.

   The operator records its name in a dedicated `AccessLog` field
   (`bound_source_names`) and **never** adds to `AccessLog.collects`.
   That prohibition is load-bearing:
   `dependency_pins_for_access` (`packages/derivation/runner.py`) pins
   **every** `source_fids[name]` for each name in `access.collects`,
   which is run-wide and is exactly the P2 C10/C12 pin leak. Pins for a
   `bound_sources` group are instead assembled explicitly as
   `present_pins` — this report's current finding and this group's
   current allocation findings — and unioned with the pins
   `dependency_pins_for_access` derives from the remaining access
   classes (refs, parameters, tables, operation semantics, closure
   reads), which are unaffected.

   A supported result therefore pins exactly its own report and its own
   group's allocations, and no others. An implementation that satisfied
   2f while routing the group through `access.collects` would violate
   this clause. Track 0 selected this close as part of R1, and independent
   review verified it against `dependency_pins_for_access`.

   **2h. Live source registration remains specific to this rule.**
   Deriving `collect_source_names` from the declared operator would be a
   broader change than this milestone authorizes
   (`_resolved_run_material` in `packages/derivation/live.py` builds that
   list from family predicates, companions, categoricals, and hardcoded
   pairing/supportability names). Registration of
   `tax.us.nominee-allocation.amount` stays the nominee-rule-id hook.
   Because the **operator's schema semantics and dependency analysis are
   generic** while **binding registration is rule-specific**, a
   schema-valid `bound_sources` rule with no coordinator or binding path
   would otherwise be accepted into a package and then be silently inert.
   Package acceptance is therefore **not** generic: validation refuses
   that case (`MEMBER_NO_BINDING_PATH` on the member-issue surface).
   Schema validity and dependency analysis do not imply package
   admissibility (Decision 1). The registry is the same nominee-rule-id constant the
   intercept and `_resolved_run_material` key on, so the three cannot
   drift apart without a validation failure.

3. **Contract B — exact-rule exception to ADR-0020 for report-group
   rows.** Scope is the exact rule id
   `tax.us.2025.rule.interest.nominee-reduction` at its adopted version.
   Nothing else.

   **3a. Scope is the rule identity, not the shape of emitted rows.**
   Membership in this ADR is decided by rule id alone, and is decidable
   from the adopted package without inspecting any emitted row.

   The suffix requirement applies to **group-outcome rows**, defined as
   any `published` or `blocked` row carrying this rule's `artifact_id`.
   On such a row, a missing or malformed suffix is a **contract violation
   by a member**, never evidence of non-membership. The requirement does
   **not** reach the rule-level `inapplicable` `no_groups_selected` row,
   which Decision 3d requires to be **unsuffixed**; that row is the
   contract's own totality account, not a group outcome. Two earlier
   phrasings are withdrawn, as Track 0 withdrew them: "coordinator-grouped
   rules" is not a mechanical class; defining the governed class as
   "adopted rules whose disposition rows carry a suffixed `symbol` of the
   form `{publishes}|{subject_fact_id}`" is false and circular. False:
   `dispatch_aggregate_supportability_on_run` already publishes
   `{AGGREGATE_SUPPORTABILITY_SYMBOL_PREFIX}|{report_fact_id}`
   (`packages/tax/pairing_consequences.py` 716). Circular: it
   would define the class by the row shape the contract exists to
   require, so a member that omitted the suffix would fall *outside* the
   contract instead of *violating* it.

   **3b. ADR-0070's aggregate-supportability rows are outside this ADR
   by rule id, not by symbol shape.** Suffixed symbols are not unique to
   the nominee rule. Those aggregate rows remain under ADR-0070
   Decision 7. Whether they later need the same treatment is a separate
   question this ADR does not answer. Existing multi-row appends for one
   `artifact_id` are evidence that the runner can append more than one
   row; they are not a silent ADR-0020 answer.

   **3c. Cardinality.** This rule records one identified disposition row
   per classified disposition-group — linear in selected groups, not in
   adopted rules. That **narrows ADR-0020 Decision 1's** one-row-per-rule
   cardinality — Decision 1 records "one disposition row **per rule
   artifact in the adopted package**", and ADR-0020's *Consequences*
   restate its cost as "one row per package rule/selector artifact —
   linear, not combinatorial" — and **Decision 1a's** singular-row,
   single-status classification, **for this rule only**. Ordinary once-per-rule-id
   artifacts keep ADR-0020 unchanged. This is not a silent
   reinterpretation of ADR-0020. Mixed statuses on one `artifact_id` are
   then expected (mixed C10: one `blocked` group row and one `published`
   group row), not a fixture contradiction.

   **3d. Totality is preserved.** ADR-0020 Decision 1's totality —
   every adopted rule is accounted for, so the walker remains a pure
   projection — still holds, because a run selecting zero
   disposition-groups records exactly one rule-level `inapplicable` row
   with evidence `no_groups_selected: true` and `symbol` set to the
   unsuffixed `publishes` prefix
   `tax.us.2025.interest.nominee-reduction`. That `symbol` is
   **required**, not optional, so Decision 3f selects this row by the
   same `row.symbol == S` test it applies to group-outcome rows. That row is not a
   publication, not `guard_result: false` (the citizen's `when` is
   `true`), not `superseded_by`, and not `blocked` with
   `DEPENDENCY_ABSENT` / `SOURCE_SET_UNCLOSED` or any other existing
   code. Committed `derivation-record.v8` has no honest shape for it
   (inapplicable `oneOf` is `guard_result` xor `superseded_by`, verified
   against the committed schema).

   **3e. Group identity is the row's suffixed `symbol`
   (`{publishes}|{report_fact_id}`), not an abuse of `missing`.** Every
   group-outcome row of this rule — published or blocked — carries
   `symbol` exactly
   `tax.us.2025.interest.nominee-reduction|{report_fact_id}` for its own
   report. `missing` keeps its meaning of *absent* dependencies
   (`packages/derivation/runner.py` 978, "naming exactly the missing
   required answers"; `explanation.py` maps `missing` to
   `unmet_references`). An
   over-allocation block (`NOMINEE_ALLOCATIONS_EXCEED_REPORT`) therefore
   carries `missing: []` while pinning the present report finding and
   every current allocation in the group. C13's absent-report block
   carries `code: DEPENDENCY_ABSENT` and `missing` naming the composed
   report fact id (`pairing_dispatch.py` is the accurate precedent),
   with `symbol` still set to the suffix so Decision 3f can select it.
   Pins identify contributing findings for displacement (ADR-0010); they
   are not the consumer join key (`derivation-record.v8` pin `id` is a
   finding id, not the report fact id). Committed precedent for `symbol`
   on a blocked row: `runner.py` `absorb_association_result`. Track 1
   extends `record_named_block` with optional `symbol=` and this rule's
   coordinator always passes it. No new subject/group field.

   **3f. Selection (ADR-0020 Decision 4) for a suffixed symbol resolves
   to exactly one row; 0 or 2 is a ledger defect.** This **narrows
   Decision 4** from producer-of-`S` (`r["publishes"] == s`, then the
   first published row — the committed walker in `explanation.py`) to
   exact `row.symbol == S`, for this rule only.

   **Entry test (mechanically decidable, and not via the producer
   lookup).** The routing condition cannot be "the producing artifact is
   the nominee rule," because this ADR itself observes that the committed
   producer lookup finds **no** producer for a suffixed `S` (the citizen
   publishes the prefix). Decide entry from the adopted package instead:

   1. Resolve the exact rule `tax.us.2025.rule.interest.nominee-reduction`
      from the adopted package. If it is not a member, ADR-0074 selection
      does not apply at all.
   2. Let `P` be that rule's declared `publishes` prefix.
   3. Apply ADR-0074 selection **only when** `S == P` **or** `S` begins
      with `P + "|"`.
   4. Otherwise retain **ADR-0020 Decision 4 unchanged**.

   This is a lookup against one named member of the adopted package, so it
   is decidable without inspecting any emitted row and without a working
   producer index for suffixed symbols. It remains an exact-rule
   exception and creates **no** generic grouped-rule class: no other
   rule's prefix routes here, whatever shape its symbols take.

   Because the `no_groups_selected` row carries `symbol` equal to `P`
   (Decision 3d), both `S == P` and the suffixed forms are selected by
   the same `row.symbol == S` test.

   **The ADR-0074 path is complete and non-recursive: once entered, it
   never returns to ADR-0020's producer-based ledger-row lookup.** An
   earlier drafting ended step 4 by falling through to "Decision 4's
   remaining ordered steps," which is **unsafe and is withdrawn**. When
   `S == P` and the run contains group-outcome rows, the exact lookup
   finds no row whose `symbol` is `P`, but ADR-0020's producer lookup
   *does* find this rule (it publishes `P`), and the committed walker
   (`packages/derivation/explanation.py` 221–225,
   `producers = [r for r in rules if r["publishes"] == s]` then
   `next(...)`) would select the **first** published row of that
   producer — an arbitrary report group. That is precisely what this
   decision forbids.

   Having entered by the test above, for run `R` and symbol `S`, in this
   order:

   1. Select the **published** ledger row whose `row.symbol == S`, and
      walk the finding it names. Exactly one such row may exist; 0 or 2
      is a ledger defect.
   2. Else select a **run-scoped act-log derived publication** whose
      finding symbol `== S`, preserving ADR-0020 Decision 4's
      interrupted/recovered-run fallback. Run-scoped means bound to `R`;
      a later run's publication is never attached.
   3. Else select the **blocked or inapplicable** ledger row whose
      `row.symbol == S` (exactly one). For `S == P` this is the
      `no_groups_selected` row, which exists only on a zero-group run.
   4. Else return **`no_disposition_recorded` for `S`**, naming the run's
      closing phase (interrupted / recovered / open).

   At no step does the ADR-0074 path consult a producer index. The
   intended results follow directly:

   | Query | Result |
   | --- | --- |
   | Suffixed `S`, group published | that group's finding (1) |
   | Suffixed `S`, publication interrupted | that exact run-scoped act-log finding (2) |
   | Suffixed `S`, group blocked | that group's block row (3) |
   | `S == P` on a zero-group run | the exact unsuffixed `no_groups_selected` row (3) |
   | `S == P` while group rows exist | **`no_disposition_recorded`** (4) — there is no single disposition for `P`, and never an arbitrary group |
   | Unrelated `S` | never enters; ordinary ADR-0020 Decision 4 behavior |

   The committed walker is wrong for this rule: a suffix `S` finds no
   producer (the citizen publishes the prefix), and a prefix `S` would
   pick one report arbitrarily. This milestone does not project
   `explain()` of the new block code (the same inherited `npe-walk.v3`
   lag the accrued codes already have). Presentation
   `_dispositions_by_symbol` already prefers `row.symbol` and is the
   in-tree join this contract matches; `_one_row` already errors on
   `len(rows) != 1`.

   **3g. Checkable completeness, in two parts.** The earlier single rule
   ("count equals the number of classified disposition-groups") is not
   checkable from a closing record alone, because the group count is a
   run fact the record does not carry. Split:

   1. **Record-level XOR (checkable from the closing record alone).**
      For this `artifact_id`, either there is exactly one
      `no_groups_selected` `inapplicable` row and **no** group-outcome
      row, or there are one or more group-outcome rows with distinct
      suffixed `symbol`s and **no** `no_groups_selected` row. Never both,
      never neither.
   2. **Run-level count (checkable in a test that also holds the
      universe).** The number of group-outcome rows equals the number of
      classified disposition-groups the coordinator selected in that
      run.

   **3h. Additive `derivation-record.v9` needs this shape settled
   first.** v8 bytes stay untouched (ADR-0003 / Article 9). v9, written
   in Track 1 after this ADR is accepted (or explicitly owner-deferred
   with the dependent work withheld):

   1. Widen `code` enum with `NOMINEE_ALLOCATIONS_EXCEED_REPORT`.
   2. Widen `inapplicable` `oneOf` with a third evidence form for
      `no_groups_selected`. **The exception is scoped in the schema, not
      only in this prose.** Decision 3 confines the ledger exception to
      one rule; the schema branch must confine it the same way, or v9
      would grant every artifact an unrestricted new disposition
      property. The branch is conditioned so that it is:

      - **legal only when** `artifact_id` is exactly
        `tax.us.2025.rule.interest.nominee-reduction`;
      - **required to carry** `no_groups_selected: true`
        (`{const: true}`);
      - **required to carry** `symbol` exactly
        `tax.us.2025.interest.nominee-reduction` (the unsuffixed
        `publishes` prefix, per Decision 3d);
      - **available only for** `disposition: "inapplicable"`; and
      - **forbidding** `guard_result`, `superseded_by`, `code`,
        `finding_id`, and `act_id`.

      The schema **rejects** a purported third-form row for any other
      `artifact_id`, for any other `disposition`, with
      `no_groups_selected` present but not `true`, with `symbol` missing,
      and with a suffixed or otherwise wrong `symbol`. This is mechanical
      enforcement: a conforming validator refuses those documents without
      consulting this ADR.

      **The mere absence of `no_groups_selected` is not invalid.** The
      two existing `inapplicable` evidence forms (`guard_result` and
      `superseded_by`) remain valid exactly as in v8 and carry no such
      property. What is invalid is an `inapplicable` row carrying **none
      of the three** recognized evidence forms — the `oneOf` is widened
      from two branches to three, not replaced.
   3. No new subject field, and **every existing requirement is
      preserved exactly**. An earlier drafting said `symbol` is
      "optional at schema level"; that is wrong. In committed v8,
      `published` rows already **require** `symbol` (alongside
      `finding_id` and `act_id`). v9 keeps that, and keeps everything
      else:

      | Row form | `symbol` in v9 |
      | --- | --- |
      | `published` | **required**, unchanged from v8 |
      | `blocked` (existing rows) | **may be omitted**, unchanged from v8 |
      | `inapplicable` with `guard_result` | **may be omitted**, unchanged from v8 |
      | `inapplicable` with `superseded_by` | **may be omitted**, unchanged from v8 |
      | nominee **group-outcome** rows (published or blocked) | **required** by ADR-0074 Decision 3e |
      | nominee **`no_groups_selected`** row | **required**, exactly the unsuffixed prefix |

      No existing record that validates against v8 stops validating
      against v9.
   4. When `code == NOMINEE_ALLOCATIONS_EXCEED_REPORT`, `missing` is `[]`
      and `symbol` is required.

   **Track 1 schema-test obligations** for the branch in (2), positive and
   negative, each able to fail:

   | # | Instance | Expected |
   | --- | --- | --- |
   | P1 | `inapplicable` + `no_groups_selected: true` + prefix `symbol`, `artifact_id` = the nominee rule | **valid** |
   | N1 | same, `artifact_id` = any other rule | **rejected** |
   | N2 | same, `disposition` = `published` or `blocked` | **rejected** |
   | N3 | third-form row with `no_groups_selected` present and `false` | **rejected** |
   | N3b | `inapplicable` row carrying **none** of `guard_result`, `superseded_by`, `no_groups_selected` | **rejected** |
   | N4 | `symbol` missing | **rejected** |
   | N5 | `symbol` suffixed (`…nominee-reduction\|demo.report`) or otherwise not the exact prefix | **rejected** |
   | N6 | branch plus any of `guard_result`, `superseded_by`, `code`, `finding_id`, `act_id` | **rejected** |
   | P2 | an unrelated existing `blocked` row with **no** `symbol` | **still valid** (no regression) |
   | P3 | an existing `inapplicable` row with `guard_result` and no `symbol`, any artifact | **still valid** (no regression) |
   | P4 | an existing `inapplicable` row with `superseded_by` and no `symbol`, any artifact | **still valid** (no regression) |
   | P5 | an existing `published` row with `symbol`, `finding_id`, `act_id` | **still valid**; `symbol` remains required there |

   Nothing emits `NOMINEE_ALLOCATIONS_EXCEED_REPORT` against v8.

## Consequences

- Track 1 implements these two contracts after owner ratification. It
  does not invent a marker, a reusable grouped-rule class, a source
  family for allocations, or a silent reinterpretation of ADR-0020.
- ADR-0020 remains the disposition-ledger contract for every adopted
  rule other than the one named in Decision 3. Decision 1 totality and
  the ledger as the single authoritative surface are preserved. Decision
  1 cardinality and Decision 1a singular-row classification are narrowed
  only for that named rule; Decision 4 selection is narrowed to
  `row.symbol == S` for that named rule's group-outcome and no-groups
  rows.
- `bound_sources` is the smallest honest mechanism that lets the adopted
  rule own the summation (ADR-0006; ADR-0071 Decision 3) without
  introducing an allocation source family (milestone stop conditions 1
  and 2). Cross-report isolation does not depend on the caller omitting a
  run-wide fold.
- Schema publication stays additive. This ADR writes no schema file.
  Track 1 writes `rule-artifact.v8`, `artifact-package.v28`, and
  `derivation-record.v9` against the shapes above, runs
  `write_manifest`, and inspects that existing checksums do not change.

## Alternatives considered

- **Ordinary `collect` of the allocation fact type, with or without
  `source_set`.** Rejected: a real family violates the source-family
  prohibition; a non-family `source_set` is schema-valid on v7 but fails
  ADR-0035's collect-family rule the moment the intended guard is applied;
  optional-`source_set` collect is not enough (`collect.get("source_set")`
  of a missing key is `None`, and that is `COLLECT_TARGET_NOT_FAMILY`).
  Track 0's committed-mechanism survey, independently re-verified twice
  before ratification.
- **`count`, `collect_categorical_all_equal`, pairing 1:1 `replace`+`ref`,
  list-valued `ref`, or coordinator pre-sum then `ref` of the total.**
  Rejected in that same survey: closure claims, wrong value domain, two
  scalars rather than a variable-length group, no admission contract, or
  the adopted rule would not own summation.
- **R3 shape 2 — one rule-level summary plus separately identified group
  outcomes.** Rejected: a single `published`/`blocked`/`inapplicable`
  summary cannot honestly describe mixed C10; a non-tax summary kind plus
  first-class group rows is shape 1 plus a redundant summary.
- **R3 shape 3 — nested group outcomes on exactly one rule row.**
  Rejected: preserves ADR-0020 cardinality at the cost of a nested
  recording shape the primitives (`record_named_block` /
  `publish_symbol_finding`) and the presentation join (`row.symbol`) do
  not have.
- **Defining the ADR-0020 exception by suffixed-`symbol` shape, or by a
  "coordinator-grouped rules" class.** Rejected: false (aggregate
  supportability already emits a suffix) and circular (a missing suffix
  would exempt the member). Decision 1 and Decision 3a are the replacement.
- **A package-visible grouped-dispatch marker for this one rule.**
  Rejected: R1's contract does not supply one (the coordinator dispatch
  registry is Python, not package-visible declaration), and inventing a
  marker for a single rule would be a broader grammar change than this
  milestone authorizes. Decision 1 states what a later reusable class
  would require.

## Not decided

- The tax conclusion, remainder shape, Schedule B / line 2b boundary,
  legacy nominee path, C0 product meaning, and the source-family
  prohibition. Track 0 closed those; this ADR does not reopen them.
- Whether ADR-0070's aggregate-supportability rows later need the same
  grouped-ledger treatment. Outside by rule id (Decision 3b).
- `explain()` of `NOMINEE_ALLOCATIONS_EXCEED_REPORT` and any
  `npe-walk` successor. Out of scope, the same inherited lag the accrued
  codes already have.
- The Track 1 version-allowlist inventory that makes a v8 citizen
  *exist* in live rules, authorization, and `RECORD_CODES`. That is
  implementation against Decision 2; this ADR does not enumerate those
  sites as if they were a third contract.
- Binding `tax.us.2025.interest.nominee-reduction` to line 2b or
  Schedule B. The prefix is not externally bound (Track 0 integration
  surface: N-A). Binding it would fire T0-F5 and is out of scope.

## Links

- Milestone plan, sections `## Track 0 adversarial closure` (the selections
  and their evidence) and `## Fixed cases` (C0–C13 and the cross-year case):
  `docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md`.
  The plan is cited by path and section, not by object id: a blob pin does
  not survive branch curation, and this ADR must remain resolvable from any
  clone of the ratified line.
- Independent review of this contract, and of the Track 0 selections it
  records, preceded acceptance. Their verified conclusions are absorbed into
  the Context and Decision text above rather than retained as process rounds.
- Contracts narrowed, for the named rule only: ADR-0020 Decisions 1
  (cardinality), 1a (singular-row classification), and 4 (selection).
  Totality and the single authoritative ledger are preserved.
- Contracts cited unchanged: ADR-0035 (collect targets a source family);
  ADR-0006 / ADR-0071 Decision 3 (declared arithmetic ownership);
  ADR-0070 Decision 7 (aggregate supportability — outside by rule id);
  ADR-0010 (displacement via pins); ADR-0003 / Article 9 (schema
  publication: additive successors, published bytes immutable).
- Schema-intent (record only; Track 1 writes the files):
  `rule-artifact.v8`, `artifact-package.v28`, `derivation-record.v9`;
  ledger events `20260909T044800Z-rule-artifact-3f4c88`,
  `20260909T050200Z-artifact-package-190f6f`,
  `20260909T044802Z-derivation-record-6168c8`.
