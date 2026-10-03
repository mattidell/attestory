# Track 1a-5 — ADR 0077 integration repairs

Labels: **implemented** means code changed and tested on this branch. **Proposed** means ADR text, or a disposable probe. The probe is `temp/track1a5/probe.py` (ignored). It was run as `PYTHONPATH=. python3 temp/track1a5/probe.py` after item 1 and exited 0. Its output is quoted below.

## 1. Three tests that encoded the old gap — implemented

These three tests now expect `unresolved-applicability` after a direct unscoped box 1 append, with a comment naming the Track 6 tie:

- `OrdinaryRelationshipRecording.test_statement_inclusion_correction_and_withdrawal_are_independent`
- `VersionedSourceConsumer.test_actlog_recovery_both_runners_and_independent_claim_lifecycles`
- `Track17RelationshipApplicability.test_same_key_statement_record_has_no_composition_answer`

Nothing else in those tests changed. Before the change, all three failed with `'unresolved-applicability' != 'current'`. After it, they pass.

## 2. Part 5: new-write boundary separated from replay — proposed

Boundary: a new admission step inside `ActLog.append`. It runs after envelope, payload and revision checks and before the line is written. It calls a new generic `enforce_new_write_invariants(state, act, registry)` on the projection of the acts already in the log. `project` and `apply_assertion` do not run it. Each writer in `packages/` reaches it through its own `log.append` (ADR 0077 Part 5 lists them). A raw-line writer and an `ActLog` built over a registry without the map bypass the step. Replay is their defense.

The probe patched a stand-in step into `ActLog.append` at runtime. It used the real recorder, `ActLog` and `project`.

| Case | Output |
| --- | --- |
| A1 direct 1800 with a current inclusion | refused; new acts `evidence-submitted`, `contribution`; assertion in log `false` |
| A1 smuggled 2900 citing the reviewed 1775 scope | refused; assertion in log `false` |
| A1 ADR 0073 retraction, then direct 1500 | retraction admitted; 1500 refused, not in log |
| A1 step calls while `project` replays | `0` |
| A2 no-claim direct append, with and without the step | box 1 `[1410.0]` both; logs identical `true` |
| A3 registry without the map | direct 1800 admitted |
| A4 pre-step history holding 2900 | `project_raises=false`, step calls `0`, 24 acts, box 1 `[2900.0]`, read-side `unresolved-applicability`; join today holds the inclusion, proposed join holds none, proposed presence holds it |
| A4 reviewed 2950 after that | admitted; read-side `current`; inclusion back in the join |
| A5 raw-line writer under the step | 1900 in log; step calls during replay `0`; same omission |

Worksheet on A4's rows, using the Track 1a-4 declaration and stand-in. Runners agreed in every case.

| Case | Line 21 |
| --- | --- |
| B1 today, inclusion joined | published 2500 |
| B2 omitted, Track 1a-4 activity | blocked `DEPENDENCY_INVALID`, box fact id |
| B3 omitted and counted unresolved, repaired activity | blocked `SLI_UNIVERSAL_COMPONENT_VIOLATION` |
| B4 old answers, omitted, Track 1a-4 activity | **published 2500** |
| B5 old answers, omitted and counted unresolved, repaired activity | blocked `DEPENDENCY_INVALID`, `old-and-new-sli-inputs-both-present` |

B4 is a counterexample to omission alone. Part 5's replay rule now also keeps the omitted inclusion present for Part 4.

## 3. Parts 3 and 4 from Track 1a-4, with two repairs — proposed

Parts 3 and 4 are the Track 1a-4 item 5 text, plus "Changed by Track 1a-5" notes.

**Derived pins validate.** Probe C, on the Track 1a-4 new-only output:

```
C.derived-finding.v2="invalid: ... pins/26/origin: 'derived' is not one of ['assertion', 'declar..."
C.derivation-record.v9.disposition="invalid: 'derived' is not one of ['assertion', 'declared_default']"
C.successor_copy_derived_finding_with_derived_origin="valid"
C.successor_copy_record_disposition_with_derived_origin="valid"
```

The disposition fails too, so the pin needs two successors: `derived-finding.v3` and `derivation-record.v10`. Each adds `derived` to the pin origin enum and is used only when that pin is present. The names are absent from this branch, `origin/main`, `origin/main-ui` and the ledger. `derived-finding.v3` has no file on any ref. `derivation-record.v10` has an unrelated unmerged draft at `96e98da8` and on tag `backup/pre-publication-curation-2026-08-31`. No schema file was written.

**New-path presence includes unresolved links.** The new path's activity is now the affirmed inclusion plus Track 3's `tax.us.2025.sli.statement-inclusion-unresolved`, `-denied` and `-withdrawn`.

| Case | Line 21 |
| --- | --- |
| B6 old answers + unresolved inclusion, Track 1a-4 activity | published 2500 |
| B7 same, repaired activity | blocked `DEPENDENCY_INVALID`, `old-and-new-sli-inputs-both-present` |
| B8–B11 old-only, new-only, closed-empty, nonempty-neither, repaired | 2500, 2500, 0, blocked on the box fact id |

Financing-keyed recorder facts are left out, following owner decision 2's "link on any statement". This is an open question in the ADR.

## 4. Consistency pass — proposed

The header, summary, "What stays unchanged", "Schemas", "Evidence and gates", "Alternatives", "Open questions", "Consequences" and the INDEX row now match Parts 1–5. Each evidence row carries implemented or proposed. Removed as false: Part 5 bound in `apply_assertion`; "no derivation-record version follows"; `CURRENT_RECORD_SCHEMA` always v9; the three older tests "still expect `current`"; "Open questions: none".

## Verification

- The three tests and `tests/test_sli_correction_entry_enforcement.py`: `python3 -m pytest <the three node ids> tests/test_sli_correction_entry_enforcement.py -q` gave 14 passed. The three test files plus the Track 6 file gave 30 passed. `tests/test_f1098e_student_loan_interest_agi_track6.py` gave 11 passed.
- `python3 -m mypy`: `Success: no issues found in 307 source files`.
- `python3 tools/governance_lint.py`: conformant.
- The full suite was not run. No code under `packages/` changed. CI `verify` is the gate of record.
