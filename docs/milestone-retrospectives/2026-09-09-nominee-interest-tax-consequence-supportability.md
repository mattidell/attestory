# Retrospective — Nominee Interest Tax Consequence and Supportability

Closed 2026-09-09. The second production stage of nominee-interest support: a
rule-owned, report-scoped nominee reduction is derived from current attributed
allocation assertions and executed through the real projection, marshalling,
package, and `run()` boundary on `package.core-calculations` v36 — **for
identities that pass the ambiguity guard**. Remainder is observed only
(`report amount − published reduction` on a supported group). The result is a
`RunResult` publication, not act-log standing.

No Form 1040 line 2b, Schedule B attachment, form-field binding, or
presentation integration; no repair of T0-F5; no legacy nominee-adjustment
migration; no information-return filing; no UI.

## What was established

- **Operator.** `bound_sources` on `rule-artifact.v8`: a typed report-local
  input that is not ordinary `collect`, and therefore outside ADR-0035's
  collect-family requirement. Fail-closed outside the coordinator; does not
  write `access.collects`.
- **Ledger.** ADR-0074 narrows ADR-0020 Decisions 1/1a/4 for the exact rule
  `tax.us.2025.rule.interest.nominee-reduction` only. One identified
  disposition row per classified report-group, identified by suffixed
  `symbol`; C0-as-absence is one rule-level `inapplicable` /
  `no_groups_selected` row at the **unsuffixed** prefix. ADR-0070
  aggregate-supportability rows are outside by rule id, not by symbol shape.
  No reusable grouped-rule class.
- **Package.** `artifact-package.v28` and `derivation-record.v9` (additive);
  v36 carries the nominee rule, reduction vocabulary, and citation, and **no**
  source-family or closure mapping for the allocation type. Line 2b v6 and
  the legacy nominee subtotal remain unconsumed.
- **Division of labour.** The coordinator owns the outer-join universe, year
  scope, grouping, C13 diagnosis, per-report pins, and the `_Run.attempt`
  intercept. The declared rule owns summation and the over-allocation
  comparison.
- **Live evidence.** C0–C8 and C10–C13, the cross-year case, ordinary-comma
  payer and statement references, two-report isolation, pin-chain, and the
  legacy/line-2b boundary execute through `live_coordinate_run` on v36.
  **C9 is closed structurally, not live.** No committed payment, credit, or
  transfer citizen exists, so there is nothing to instantiate; a static test
  (`test_c9_rule_declares_no_payment_or_legacy_nominee_dependency`) proves the
  adopted rule declares no payment, credit, transfer, accrued-interest, or
  legacy-nominee dependency, and that no reduction arises without a current
  allocation. Inventing a fixture for a nonexistent citizen would have been a
  claim about behavior nothing in the corpus can exhibit. Track 2 was
  independently reviewed READY with no blocking finding
  (Track 2's independent review). The load-bearing C0 assertion is the unsuffixed
  `no_groups_selected` row, **not** box-1 `$1,200` — box-1 is a different
  rule and would publish either way.

## Carry-forward lessons

- **Working code is not a ratified contract.** Three decisions were nearly
  settled by observing what the runner tolerated rather than what an accepted
  document required: treating a non-family `collect.source_set` as admissible
  because the intended guard is inactive; treating one-row-per-rule
  cardinality as already answered because the primitives can append more than
  one row; treating a resolved rule with no ledger row as totality. Gate P3
  sketched a v7 `collect` the schema refuses; a sentinel `source_set` then
  tried to occupy the hole the inactive guard left; ADR-0020 was almost
  reread from `record_named_block`. The contract has to be written, then
  implemented. Tolerance is not permission.

- **A test that cannot fail is not evidence.** Several kills passed review
  while being unable to catch the defect they named: a symbol-keyed dict that
  merged the duplicate grouped-ledger rows it was meant to detect; an
  isolation test that executed only one of its two reports, so the other
  report's absence proved nothing; an absence paired with a positive that
  belongs to a **different rule** (C0's box-1 `$1,200`, produced by the box-1
  family collect whether or not the nominee rule ran). Pair an absence with a
  neighbouring positive only when that positive shares the execution path
  under test. Prove a kill is load-bearing by breaking it.

- **A rendering is not a structure.** Splitting a rendered `fact_id` assumed
  an encoding that is not injective: `facts._fact_id` joins `name=value` on
  `,` without escaping, so an ordinary comma in a payer name made a current
  report and a current allocation look like different identities
  (`DEPENDENCY_ABSENT` instead of the reduction). No parser recovers the
  values. The honest fix was to stop parsing — carry structured
  `SourceFact.keys` from the kernel lattice — and to **bound the claim**, not
  to write a cleverer parser. Structured keys avoid re-parsing; they do not
  repair the collision in the lattice itself.

- **An edit that can silently no-op is not an edit.** Successive
  anchor-based text replacements froze both the phase-state status and the
  plan's identity narrative without error, once the anchor text stopped
  matching. Capsule `milestone_state` and `current_role` stayed current; the
  prose still described Track 0 as the work in flight. A string-replace edit
  to a canonical document needs an assertion that its anchor matched, or it
  is a write that can quietly fail. Rewrite wholesale when the narrative has
  drifted; do not patch a frozen paragraph.

## Material dissent

There was no standing dissent on the tax conclusion, the remainder shape, the
Schedule B boundary, the legacy path, or the source-family prohibition.

Three substantive defects were found by **owner direction rather than by
review**, after Track 1's independent review had returned READY with no
blocking finding: reconstructing a report fact id by parsing a rendered
allocation id; treating missing or inconsistent identity as a silent filter
that turned a real allocation into C0 or a smaller total; and a live
isolation test that ran only one of its two reports. Independent review later
caught wording and two untested refusal sites; it did not catch those three.
That is a fact about the review pattern, not a claim that review is
optional. A later milestone that treats a clean READY as the last look at
identity, isolation, or kill vacuity will repeat it.

## Deferred, with triggers

- **T0-F5** remains a hard gate on the later legacy-and-return-integration
  stage: no production or integration unit may be accepted as complete for a
  state combining required Schedule B presentation with a nonzero pairing-scoped
  current-year adjustment until it is repaired. Binding the new prefix to
  line 2b would fire it. *Trigger:* that stage is selected.
- **The substrate boundary.** The identity guard is an execution-time stop,
  not an intake or admission gate, and not yet a clean product refusal
  (open run, empty reserved outputs). Closing it needs **either** a general
  identity repair **or** a real pre-execution intake restriction with explicit
  failure semantics. This milestone selects neither. *Trigger:* a product
  case that must accept or refuse delimiter-shaped identity values at
  recording time, or a kernel change to fact-id encoding.
- **`explain()` of `NOMINEE_ALLOCATIONS_EXCEED_REPORT`.** ADR-0074 Decision 3f
  records the committed producer lookup as wrong for this rule and defers
  the walk, the same inherited `npe-walk.v3` lag the accrued codes already
  have. *Trigger:* a consumer that must explain the new block code.
- **A reusable grouped-rule class.** ADR-0074 is exact-rule scope. A later
  rule that needs the same ledger shape needs its own contract and a
  declared marker — never membership-by-suffix. *Trigger:* a second
  coordinator-grouped rule.

## Known limitations

- The result is bounded to uniquely rendered identities. Ordinary punctuation,
  including ordinary commas in payer names and statement references, is
  supported. Delimiter-shaped `,<identity-key-name>=` values are refused at
  execution, after output reservation and the start record.
- `COLLECT_TARGET_NOT_FAMILY` remains inactive (`universe_guard_active` ends
  at `artifact-package.v17`; production is v28). This rule does not `collect`.
  Do not depend on the guard remaining inactive, and never admit a
  nominee-allocation source family if it is repaired.
- Allocation `tax-year` admits `{2024, 2025}` while box-1 admits `{2025}`. The
  coordinator year-filters both marshaled sets before classification; a 2024
  allocation is not a 2025 C13.
