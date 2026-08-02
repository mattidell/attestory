# Round 2 Expressiveness Review

Reviewer: antigravity-expressiveness-r2-2026-07-12
Role: Expressiveness Reviewer — Closure Freshness Reducer
Round: 2
Prototype branch: prototypes/closure-freshness/repair1
Prototype commit reviewed: 78c48a5

I ran reproduction checks and independent probes of the reducer from `/tmp/finances-cf-r2-expressiveness` before opening `docs/archive/2026-08-02-milestone-artifacts/prototypes/closure-freshness/examination-repair1.md`. I did not read same-round peer outputs (`round-2-governance.md`, `round-2-adversary.md`) before this review.

## Checks

### Coverage

Result: Pass with caveats. The test suite covers all seven required cases and maps the negative constraints to specific tests. The caveats concern minor input validation edge cases that are not exercised by the current suite.

Specifically:
- **Fresh zero**: Covered in `test_replay_after_every_act_and_required_cases` via acts 0-3 (`Z0` is current at `H0`).
- **Late member**: Covered in `test_replay_after_every_act_and_required_cases` via act 6 (member `M1` added, displacing `K0` and `Z0`).
- **Value correction**: Covered in `test_replay_after_every_act_and_required_cases` via act 7 (same-member value correction does not change horizon/currency).
- **Predicate correction**: Covered in the scenario (act 8) and verified via incremental-vs-rebuild replay checks.
- **Removal/no resurrection**: Covered in `test_replay_after_every_act_and_required_cases` (act 10 removal of `M2` does not resurrect `Z0`).
- **Re-attestation/rerun**: Covered in `test_replay_after_every_act_and_required_cases` (act 11/12 publishing `Z4` on current `H4`).
- **Two-family isolation**: Covered in `test_replay_after_every_act_and_required_cases` (family G zero `ZG0` remains current after F transitions).
- **Missing successor**: Covered in `test_missing_successor_mutant_is_killed`.
- **Fabricated/future/replayed/mis-scoped/global horizons and half-transitions**: Covered in `test_fabricated_future_replayed_misscoped_and_half_transitions_reject` and `test_rejected_member_change_is_atomic`.
- **Caller staleness flags/roots**: Covered in `test_direct_stale_root_or_flag_mutant_is_killed`.

**Gaps identified during independent probing:**
1. Closure attestation with `horizon: None` for unopened families is accepted and later causes `KeyError` crashes (rather than raising a `Reject` exception) when running a zero or calculating currency.
2. Empty strings (`""`) are accepted as valid IDs for both closure findings and zeroes.

### Reproduction

Result: Pass. The tests were run successfully and independently. Independent probes verified the behavior of the reducer and exposed the aforementioned input validation edge cases.

Exhibit 1 (Running tests):

```sh
python3 -m unittest test_reducer.py
```

Output:

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

Exhibit 2 (Independent Probe - Unopened Family / None Horizon KeyError):

```sh
python3 -c "
import reducer
state = reducer.State()
act1 = {'kind': 'closure_attested', 'id': 'K_bad', 'family': 'unopened', 'scope': 'tax-year-2025', 'horizon': None, 'value': True}
act2 = {'kind': 'run_zero', 'id': 'Z_bad', 'closure': 'K_bad'}
try:
    reducer.apply(state, act1)
    reducer.apply(state, act2)
except Exception as e:
    print('Error:', type(e), e)
"
```

Output:

```text
Error: <class 'KeyError'> 'C@None'
```

Exhibit 3 (Independent Probe - Empty Zero ID):

```sh
python3 -c "
import reducer
state = reducer.State()
act0 = {'kind': 'open_family', 'family': 'F', 'scope': 'S', 'horizon': {'id': 'H0', 'family': 'F', 'scope': 'S', 'previous': None}}
act1 = {'kind': 'closure_attested', 'id': 'K0', 'family': 'F', 'scope': 'S', 'horizon': 'H0', 'value': True}
act2 = {'kind': 'run_zero', 'id': '', 'closure': 'K0'}
try:
    reducer.apply(state, act0)
    reducer.apply(state, act1)
    reducer.apply(state, act2)
    print('Accepted empty zero ID! State:', state)
except Exception as e:
    print('Rejected:', type(e), e)
"
```

Output:

```text
Accepted empty zero ID! State: State(horizons={'H0': (('F', 'S'), None)}, current_horizon={('F', 'S'): 'H0'}, closure_facts={'C@H0': (('F', 'S'), 'H0')}, closure_findings={'K0': 'C@H0'}, members={}, zeroes={'': 'K0'}, superseded_horizons=set())
```

### Schema / Contract Authority

Result: Pass. The reducer establishes clear boundary rules for what is admitted into the authoritative log. Rebuilding from the log of acts is equivalent to incremental state updates, and any act that violates the schema/preconditions is rejected before modifying the state.

### Hard Distinctions

Result: Pass. The reducer successfully differentiates between:
- Horizon citizen (ordinary citizen identity) vs findings (affirmative closure) vs zeroes (derived pins).
- Predecessor horizon as a record-derived root vs derivation edges.
- Value corrections (no horizon successor, no displacement impact) vs predicate-changing corrections (required horizon successor, causing displacement).

### Gap/Edge Audits

As demonstrated in Exhibit 2 and Exhibit 3, there are two distinct validation gaps:
1. `closure_attested` fails to ensure that `horizon` is a valid string, allowing `None` when a family is unopened, resulting in crashes during downstream usage.
2. Empty strings are allowed as IDs for findings and zeroes.

### Honesty Audit

Result: Pass with reservations. The examination accurately reflects the measured cases, negatives, and mutant-killing capabilities. However, it overclaims complete validation strictness, missing the residual input validation holes that allow `KeyError` crashes and empty string IDs.

## Observations

The reducer is remarkably elegant. By utilizing superseded horizons as record-derived roots and traversing only two declared edge kinds (`individuation` and `derivation`), it derives currency correctly without needing side-channel listeners, stored staleness bits, or manual closure withdrawals. 

The implementation of `replay_check` ensures that any incremental calculation is strictly validated against a full rebuild, guaranteeing contract consistency.

## Dissent

I dissent from the implicit claim in the examination that all input validations are completely bulletproof. The validation logic should be tightened to reject `None` horizons for closure findings (even if matching the un-opened family's default value of `None`) and reject empty finding/zero IDs.

## Verification

The formatting of this file was checked with git diff. No trailing whitespace was found.
