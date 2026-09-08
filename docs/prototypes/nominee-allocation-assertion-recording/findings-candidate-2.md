# Candidate 2 findings — adopted source family / `act-member-transition.v3`

Track 0 checkpoint T0-A, candidate 2 only. Another builder owns candidate 1.

**Probe (executed):**

```
PYTHONPATH=. python3 docs/prototypes/nominee-allocation-assertion-recording/probes/candidate-2-family.py
```

The probe folds real kernel acts through `packages.kernel.findings.apply_act` / `project` machinery (`apply_member_transition`, `apply_assertion`, `apply_horizon_genesis`) and reads currentness through `packages.kernel.currency.compute_currency` and `packages.kernel.findings._current_value_for_fact`. It validates published schemas `source-family.v2`, `act-member-transition.v3`, and `family-horizon.v1`. Synthetic `demo.*` identities only.

This file separates **RAN** (printed by that process) from **INFERRED** (judgment on that output). Case verdicts below are RAN unless marked otherwise.

## Case table

| Case | Verdict | One-line RAN observation |
| --- | --- | --- |
| A2 | **PASS** | One current Pat allocation, `$450`, fact id names report A, attributed to `demo.user.alex` via member-transition `demo.cand2.act.006`. |
| A3 | **PASS** | Two current facts: Pat `$300` and Kim `$150`, distinct `fact_id`s. |
| A4 | **PASS** | After Pat `$300 → $250`, Kim is the same finding object `demo.finding.kim.a.v1`, same supporting act `demo.cand2.act.007`; no later act names Kim. |
| A5 | **PASS** | Report B is present; Pat-on-B fact id differs; no current value on B. |
| A6 | **PASS** | Pat has no current value; stored Pat findings keep `450`/`300`/`250`; nothing zero/false written; Kim's object unchanged; remove act writes no finding. |
| A11 | **FAIL** | Same `(report, owner)` fact id cannot become current again. |

## Kernel claims the plan asserted and this probe ran

All three hold.

### `state.withdrawn_fact_ids` is monotonic

**RAN.** After A6:

```
CLAIM. monotonic withdrawn_fact_ids
before:
  []
after:
  - 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat'
grew_by_union_with_pat_a: True
nothing_subtracted: True
```

A second `remove` of the same id was refused:

```
error: 'member fact already withdrawn: demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat'
```

After a later member-transition *write* of a new finding on that same fact id (A11 path 2b), the set still contained exactly that id — it was not subtracted or reset:

```
pat_a_still_in_withdrawn_fact_ids: True
withdrawn_fact_ids:
  - 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat'
```

**INFERRED.** On this kernel there is no executed operation that removes a fact id from `withdrawn_fact_ids`. Withdrawal of a `(report, owner)` fact id is terminal for that id's currentness.

### `_current_value_for_fact` returns no current value for any withdrawn fact id

**RAN.** After A6, and still after the A11 same-id write:

```
CLAIM. _current_value_for_fact on withdrawn ids
pat_a_is_sentinel: True
kim_a_is_150: True
every_withdrawn_id:
  demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat: '<NO_CURRENT_VALUE>'
```

A11 path 2b, after storing `demo.finding.pat.a.v4-transition` with value `250` on the withdrawn fact id:

```
pat_a_current_value: '<NO_CURRENT_VALUE>'
new_finding_in_current: False
new_finding_in_displaced: True
```

**INFERRED.** Storing another finding on a withdrawn fact id does not restore currentness. Currency displaces every finding for that id.

### SC-R1 forbids a predicate-matching member fact from entering through a plain assertion

**RAN.** Registry `family_member_predicates` named `demo.allocation.amount`, matching how `packages/tax/loader.py` arms adopted families.

First entry, never a member:

```
error: 'cannot assert member fact demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat through a plain assertion; must use a member-transition instead'
```

After withdrawal (fact id has findings, but is in `withdrawn_fact_ids`, so it is not a current member):

```
error: 'cannot assert member fact demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat through a plain assertion; must use a member-transition instead'
```

Same-member *correction* of a live member is the assertion path; SC-R2 refused a member-transition correction:

```
error: 'transition asserting fact demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat already in the family is rejected: same-member correction belongs on the ordinary assertion path'
```

**INFERRED.** The live-member exception in SC-R1 is only for same-id correction of a *currently* admitted member. Withdrawal takes the fact out of that exception. Re-entry cannot use `assertion`. Re-entry via `member-transition` can write a finding and still cannot make that fact id current, because of the two claims above.

## Family contract (whole contract this route takes on)

**RAN.** `source-family.v2` required fields:

```
['schema', 'id', 'version', 'title', 'scope', 'closure_claim', 'member_predicate', 'authorizes_subtotal']
```

Omitting `closure_claim` and `authorizes_subtotal`:

```
ok: False
errors:
  - "<root>: 'closure_claim' is a required property"
  - "<root>: 'authorizes_subtotal' is a required property"
```

Empty strings:

```
ok: False
errors:
  - "authorizes_subtotal: '' should be non-empty"
  - "closure_claim: '' should be non-empty"
```

Hedged recording-only wording (`"No completeness about the world is claimed..."` / `"this-recording-does-not-authorize-a-subtotal"`) and completeness/subtotal wording both schema-ok: `True`.

`act-member-transition.v3` without `successor`: `'successor' is a required property`. `family-horizon.v1` without `predecessor`: `'predecessor' is a required property`. Every executed add and remove minted a successor horizon (`h0→h1→h2→h3→h4`).

**INFERRED.** Schema acceptance of hedged wording is not an honest recording-only instance. `closure_claim` is a closure claim about the family's membership in the world; `authorizes_subtotal` names the subtotal that closure of this family may authorize. Filling those fields is taking tax-consequence authority this milestone does not have. Leaving them off is unrepresentable. This candidate is **disqualified on the family contract**, independently of A11, and is not to be renegotiated into a family that "doesn't really close."

The kernel will drive member-transitions on a bare `{id, version}` family key without ever validating a `source-family.v2` citizen. That does not discharge the contract. Adopting this route in production still takes on `source-family.v2`.

## A2 — PASS

**RAN.**

```
status: 'PASS'
add_act_id: 'demo.cand2.act.006'
current_allocations:
  finding_id: 'demo.finding.pat.a.v1'
  fact_id: 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat'
  value: 450
  supporting_act:
    act_id: 'demo.cand2.act.006'
    kind: 'member-transition'
    actor: 'demo.user.alex'
    at: '2026-09-05T14:00:06Z'
    committed_against: 6
pat_a_current_value: '450'
```

One current ordinary allocation, attributed to the caller, associated only with report A.

## A3 — PASS

**RAN.** Distinct fact ids; two current statements; Pat's `$450` finding remains stored but is displaced by correction to `$300`.

```
status: 'PASS'
distinct_fact_ids:
  - 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.kim'
  - 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat'
```

Current values: Kim `150` on `demo.finding.kim.a.v1` (member-transition `demo.cand2.act.007`); Pat `300` on `demo.finding.pat.a.v2` (assertion `demo.cand2.act.008`). No combined proposition.

## A4 — PASS

**RAN.** Record identity, not value equality.

```
status: 'PASS'
kim_finding_id_before: 'demo.finding.kim.a.v1'
kim_finding_id_after: 'demo.finding.kim.a.v1'
kim_same_object: True
kim_supporting_act_before:
  act_id: 'demo.cand2.act.007'
  kind: 'member-transition'
  actor: 'demo.user.alex'
  committed_against: 7
kim_supporting_act_after:
  act_id: 'demo.cand2.act.007'
  kind: 'member-transition'
  actor: 'demo.user.alex'
  committed_against: 7
acts_whose_payload_names_kim_finding_or_fact:
  - 'demo.cand2.act.007'
pat_new_finding_id: 'demo.finding.pat.a.v3'
pat_new_act_id: 'demo.cand2.act.009'
```

Kim's stored finding dict is the same Python object after Pat's correction. Pat's new assertion `demo.cand2.act.009` does not name Kim. Horizon stayed `demo.horizon.ordinary.h2` (value correction is the assertion path, not a membership transition).

**INFERRED.** A4 holds on this route *because* owner is a distinct component of `fact_id` and correction is per `fact_id`. That is the identity A11 would have to reuse.

## A5 — PASS

**RAN.**

```
status: 'PASS'
pat_a_fact_id: 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat'
pat_b_fact_id: 'demo.allocation.amount|report=demo.report.b,owner=demo.owner.pat'
ids_differ: True
current_fact_ids:
  - 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.kim'
  - 'demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat'
pat_b_current_value: '<NO_CURRENT_VALUE>'
report_b_entity_present: True
```

Report B shares payer `demo.payer.alpha` and is in the lattice. No current allocation attaches to it.

## A6 — PASS

**RAN.**

```
status: 'PASS'
remove_act:
  act_id: 'demo.cand2.act.010'
  kind: 'member-transition'
  actor: 'demo.user.alex'
  successor:
    id: 'demo.horizon.ordinary.h3'
    predecessor: 'demo.horizon.ordinary.h2'
pat_findings_still_stored:
  - id: 'demo.finding.pat.a.v1' / value: 450
  - id: 'demo.finding.pat.a.v2' / value: 300
  - id: 'demo.finding.pat.a.v3' / value: 250
authored_zero_or_false_or_opposite: []
history_deleted: False
pat_a_current_value: '<NO_CURRENT_VALUE>'
kim_current_finding_id: 'demo.finding.kim.a.v1'
kim_same_object_after_withdraw: True
remove_did_not_write_a_finding: True
```

Withdrawal removes current support without writing zero, `false`, or an opposite ownership claim, and without deleting history. Authorship of the withdrawal is `demo.cand2.act.010` (`actor: demo.user.alex`). Authorship of the withdrawn statements remains their original acts.

## A11 — FAIL

A11 requires that after A6 the same `(report, owner)` proposition can become current again, supported by a *new* assertion act, without reviving the withdrawn statement in place and without exhausting the pair.

### Path 1 — plain assertion of the same fact id (executed, refused)

```
accepted: False
error_type: 'FindingModelError'
error: 'cannot assert member fact demo.allocation.amount|report=demo.report.a,owner=demo.owner.pat through a plain assertion; must use a member-transition instead'
```

SC-R1. Not a re-assertion path.

### Path 2 — member-transition assert of the same fact id (executed, write accepted, currentness refused)

The write was accepted and stored `demo.finding.pat.a.v4-transition` with value `250` under act `demo.cand2.act.011`. Then:

```
status: 'FAIL'
plain_assertion_accepted: False
member_transition_write_accepted: True
same_fact_id_became_current: False

pat_a_still_in_withdrawn_fact_ids: True
pat_a_current_value: '<NO_CURRENT_VALUE>'
new_finding_in_current: False
new_finding_in_displaced: True
current_allocations:   # Kim only
  finding_id: 'demo.finding.kim.a.v1'
```

This is the exact executed path on this route with the identity A4 uses. It does not satisfy A11. The pair is exhausted at that fact id.

### Path 3 — different fact id, extra `instance` key (executed diagnostic)

A second workspace keyed identity as `(report, owner, instance)`. After withdrawing Pat instance 1, asserting Pat instance 2 became current:

```
pat_instance_1_fact_id: 'demo.allocation.amount-instanced|report=demo.report.a,owner=demo.owner.pat,instance=demo.allocation.instance.1'
pat_instance_2_fact_id: 'demo.allocation.amount-instanced|report=demo.report.a,owner=demo.owner.pat,instance=demo.allocation.instance.2'
fact_ids_differ: True
pat_1_current_value: '<NO_CURRENT_VALUE>'
pat_2_current_value: '250'
kim_current_value: '150'
kim_same_object_after_pat_correction: True
two_pat_fact_ids_exist_for_same_report_and_owner: True
```

**INFERRED.** This is not A11 on the same proposition identity. It is a new citizen. What it does to A4:

- A4's record-identity check can still pass *per instance* (Kim's instance object was unchanged by Pat's correction).
- Per-owner identity is no longer `(report, owner)`. Two Pat fact ids exist for the same report and owner; the original `(report, owner)` fact id remains permanently non-current.
- The plan's A4 proviso — "the owner is a distinct component of the fact id" — is no longer sufficient. Instance is a third component, so "Pat's statement on report A" is no longer one fact.
- That is a different product meaning, not a salvage of candidate 2.

**A11 is not satisfiable on this route with the same fact id.** A candidate that cannot express A11 is disqualified.

## History, attribution, coupling

**RAN.** After the main workspace (including the unsuccessful same-id A11 write):

- **History retained:** every finding (`demo.finding.kim.a.v1`, `demo.finding.pat.a.v1`–`v3`, `demo.finding.pat.a.v4-transition`); every act `demo.cand2.act.000`–`011`; the full horizon chain `h0`–`h4` with superseded/current status and predecessor/successor links. Nothing was deleted.
- **Attribution join:** `finding.id` → `act.payload.finding.id` (assertion) or `act.payload.member.finding.id` (member-transition assert). `actor` and `at` live on the act envelope, not the finding. Withdrawal authorship is the member-transition `remove` act joined by `payload.member.fact_id`. Executed example: Kim's current finding `demo.finding.kim.a.v1` joins `demo.cand2.act.007` / `demo.user.alex` / `2026-09-05T14:00:07Z`. Pat's withdrawal joins `demo.cand2.act.010`.
- **Owners uncoupled at finding identity:** Pat and Kim have distinct fact ids; A4 and A6 left Kim's finding object and supporting act untouched.
- **Owners coupled at family/horizon:** they share one horizon chain. Adding Kim advanced `h1→h2`; withdrawing Pat advanced `h2→h3`; the same-id re-assert write advanced `h3→h4`. A membership change for one owner mint a new current horizon for the family.

**INFERRED.** The horizon coupling is not a defect in A4's finding-identity sense, but it is coupling: any later closure keyed on the current horizon would be staled by the other owner's add or remove. That is family machinery this recording-only milestone has no other reason to carry.

## Verdict

**Candidate 2 is not viable for a recording-only milestone. No.**

Two independent executed disqualifications, either of which is enough:

1. **A11 FAIL on the identity A4 requires.** `withdrawn_fact_ids` is monotonic, `_current_value_for_fact` returns no current value for a withdrawn id unconditionally, and SC-R1 blocks plain-assertion re-entry. A member-transition write on the same fact id stores a finding that is born displaced. A different fact id (instance key) makes a current row appear and thereby abandons per-owner `(report, owner)` identity.
2. **The family contract cannot be satisfied inside recording-only limits.** `source-family.v2` requires `closure_claim` and `authorizes_subtotal`. Every transition requires a successor `{id, predecessor}` and `family-horizon.v1` requires `family`, `scope`, `predecessor`. A recording-only milestone must not assert completeness about the world or authorize a subtotal. That is disqualification, not renegotiation.

A2–A6 are real on this kernel. They do not save the candidate. Do not treat A6's honest withdrawal as evidence that A11 is feasible; that is the mistake the plan already recorded from the previous gate, and this probe ran it.
