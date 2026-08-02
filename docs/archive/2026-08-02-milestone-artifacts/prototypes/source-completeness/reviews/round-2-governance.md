# Round 2 Review — Governance Fidelity

Date: 2026-07-12. Seat: governance-fidelity. Evidence rungs: 2–3
(prototype resolver and throwaway calculation path).

Authority used: governance set v0.1; ADR-0011/0012; approved plan; round-2
file; repair charters/examinations; round-1 triage and governance review; and
the named it1, it2, repair1, and repair2 exhibits. No same-round peer output or
peer commit body was read.

Independent reproduction:

- `repair1`: `python3 -m unittest -v test_resolver` — 15 tests passed.
- `repair2`: `python3 -m unittest -v test_end_to_end` — 11 tests passed.

## Measurements

### Check 1 — ADR-0011 decision 5: current true only

- **Shape A (dedicated mapping citizen) — PASS at prototype level.** Result:
  exactly one current literal-`true` finding admits; false, absent, displaced
  historical true, non-boolean truthy values, ambiguous current findings, and
  duplicate mappings block through publication. The false and displaced cases
  kill presence-only and currency-blind mutants. Exhibit:
  `repair1/resolver.py` (`admit_current_true`, `resolve_A`),
  `repair1/test_resolver.py` (`AdmissionCases`, `MutationMatrix`), and
  `repair2/test_end_to_end.py` (`Layer2Admission`, `Mutants`, `Ambiguity`).
- **Shape B (embedded adopted parameter) — PASS at prototype level.** Result:
  the same cases and assertions run through `resolve_B`; non-`True`
  `admitted_value`, duplicate adopted rules, and ambiguous findings cannot
  authorize membership. Exhibit: the same suites plus
  `repair1/resolver.py` (`resolve_B`).
- **Production condition:** these tests execute a standalone resolver and a
  faithful copy, not production. Production must install the selected resolver
  as the actual projection and retain these mutation cases.

### Check 2 — no caller-supplied closed membership

- **Both shapes — PASS by prototype construction.** Result: `ResolvedMembership`
  derives families only from exact admitted authorities; `env_closed_sets` has
  no caller-set parameter; the throwaway `Env` accepts only `sources` and
  `resolved`. Bare-family injection blocks, while a caller-union mutant
  publishes and is therefore killed for each shape. Exhibit:
  `repair1/resolver.py` (`ResolvedMembership`, `env_closed_sets`),
  `repair1/test_resolver.py` (`CallerInjectionCases`),
  `repair2/prototype_eval.py` (`Env`, `run_rule_caller_union`), and
  `repair2/test_end_to_end.py` (`CallerInjection`, `Mutants`).
- **Production condition preserved:** production still has
  `RunContext.closed_sets`. Prototype evidence proves the replacement shape is
  sole-writer-capable; only production removal plus a system-wide construction
  audit proves no caller seam remains. ADR-0011 is not cited as approving that
  seam.

### Check 5 — Article 11: declared meaning, not runner-smuggled behavior

- **Shape A — PASS for prototype sufficiency.** Result: family, closure fact
  type, required identity, and `current-true` admission are fields of the
  mapping entry; the generic resolver interprets them and the calculation path
  consumes only resolved membership. Exhibit: `repair1/resolver.py`
  (`MappingEntry`, `MappingCitizen`, `resolve_A`) and paper exhibit
  `it1/sc-p1-mapping-design.md`.
- **Shape B — PASS for prototype sufficiency.** Result: family and member fact
  type remain declared by the collecting rule, while closure fact type,
  required identity, and admitted literal are declared in
  `ClosureAuthorityParam`; the same generic admission/evaluation mechanics run.
  Exhibit: `repair1/resolver.py` (`ClosureAuthorityParam`, `CollectingRule`,
  `resolve_B`) and paper exhibit `it2/design.md`.
- No operative citation contract is introduced. **Production condition:** the
  selected content shape needs a schema-first declaration and a portability
  test; the Python prototype classes are evidence, not adopted content or a
  production schema.

### Check 6 — pins and empty-source-zero explanation

- **Both shapes — PASS at prototype level.** Result: admission retains the
  exact current finding id/version and the mapping/rule artifact id/version.
  Empty-source zero publication emits both pins; re-attestation selects the new
  finding, and ambiguity blocks instead of overwriting authority. Present-member
  aggregation correctly emits no closure pin because closure is not consulted.
  Exhibit: `repair1/resolver.py` (`ClosureAuthority`, `pin_for`),
  `repair2/prototype_eval.py` (`collect`, `build_pins`), and
  `repair2/test_end_to_end.py` (`ExplanationPins`, `Layer1`, `Ambiguity`).
- **Production conditions:** production `pins_for` must add these pins, and
  persisted withdrawal/displacement of a closure-backed zero remains rung-4
  milestone integration. The prototype proves the zero-to-authorizing-finding
  walk, not production persistence of the whole explanation chain.

### Check 7 — charter / Gate 2–3 scope

- **Substantive scope — PASS.** Result: repair1 stays at resolver mutations;
  repair2 copies rather than imports or edits production and stays at rung 3.
  Both shapes receive equal SC-P1 cases. No SC-P2, SC-P3, SC-D1, coverage,
  production schema, workspace, or persistence work is absorbed. Exhibit:
  `charter-repair1.md`, `charter-repair2.md`, the four repair code/test files,
  and both repair examinations.
- **Process cap — FAIL / explicit dissent.** Result: approved Gate 4 authorizes
  one repair pass beyond the two builders and says any further build is
  stop-and-decide with the owner. `repair2` is named and executed as Repair Pass
  2. Its charter asserts delegated progression authority, but the reviewed
  evidence contains no owner-ratified cap amendment or stop-and-decide record.
  Gate 3 allowed a conditional rung-3 climb, but that does not silently amend
  the separate repair-pass cap. Exhibit: `plan.md` Gates 3–4,
  `charter-repair1.md`, and `charter-repair2.md`.

## Observations and recommendation

The executable evidence removes the round-1 decision blocker on affirmative-
only enforcement for both mapping shapes. Governance does not prefer the
dedicated citizen over the embedded parameter on these measurements; selection
may turn on reuse/evolution tradeoffs, with the same current-true, ambiguity,
sole-writer, and pin obligations either way.

**Dissent preserved:** the round-1 Articles 9/10 failure remains a production
condition, not a demand for prototype schemas in round 2. Separately, the
unreconciled second-repair cap is a process-scope failure even though repair2's
technical content stayed inside SC-P1/rung 3. I recommend treating the
executable results as sufficient prototype evidence for SC-P1, while requiring
the foreman/owner record to reconcile that cap before citing the process as
fully plan-conformant. Gate 5 disposition and any ADR drafting remain the
foreman's responsibility.
