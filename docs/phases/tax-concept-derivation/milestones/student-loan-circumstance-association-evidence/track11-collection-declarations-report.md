# Track 11 — collection declaration evidence

## Question and evidence boundary

This unit tested whether an already admitted declaration can consume several
current financing observations for one borrowing while retaining the complete
expected source set and producer readiness. The values are neutral synthetic
schooling categories. They do not select tax treatment.

The Track 10 control is its required-source statement-borrowing consumer. The
candidate removes that `requires` entry and leaves the existing
`collect_categorical_all_equal` expression. Its category literal names
`demo.sli.track10.schooling@v1`, the source result category; it does not use
the destination financing-observation type as authority. The candidate was
admitted through normal package validation after test-local resealing.

## Inspection

- `requires` makes the scheduler wait for the financing producer. The
  per-subject dispatch path also checks the required source values. Two current
  financing values for one subject fail this control check before its
  collection predicate can read them.
- `link_coverage` is constrained to a rule whose `joined` fact type is the
  `links` type under `joined_contains_subject`. The Track 10 membership and
  financing identity key names do not satisfy that relationship. The operator
  also expects numeric reductions for linked rows. `link_count` has the same
  declared joined-type relationship constraints. Those operators therefore
  did not supply a valid candidate for this graph.
- A bounded second candidate adds numeric EXPECTED and AVAILABLE witnesses
  with two synthetic `source-family.v1` declarations. EXPECTED emits one value
  for each current FINANCE source claim. AVAILABLE is keyed to the same
  subject, requires FINANCE_RESULT, and reads that result before emitting one
  value. The consumer compares `add(collect EXPECTED)` with
  `add(collect AVAILABLE)`, selects the existing categorical collector on
  equality, and otherwise selects `block(DEPENDENCY_INVALID)`. The family
  declarations describe the emitted witness rows; they do not assert that the
  families are closed or complete. Ordinary package admission accepted these
  test-local declarations.
- The current collector does not establish an exact type guarantee for the
  values it reads. This report makes no such claim.

## Executed cases

All inputs are synthetic and entered through the Track 10 test helper's
contribution admission. The source identity and expected financing membership
were projected from freshly reopened authoritative ActLog acts. Producer
findings, structured fact IDs, consumer pins and blocked references remain
separate namespaces.

| Case | Observation |
| --- | --- |
| Existing required-source control, two subjects | The live coordinator recorded two `DEPENDENCY_INVALID` membership findings for A and B. Each had its own subject symbol and two missing financing fact IDs. The findings retained the statement-membership subject pin. |
| Candidate 1, producer first | Both runners and the coordinator agreed. The consumer published `false` for A and B with differing current categories, and `true` for the one-observation C control. Each A/B output pinned its membership claim plus both actual financing publications. Each financing publication pinned its own current financing source finding and schooling source finding. The complete transitive support contained both financing claims and both school sources for each subject. |
| Candidate 1, consumer first | The resolved rule sequence placed the consumer before the finance producer. The coordinator recorded `DEPENDENCY_ABSENT` for A, B and C, with `missing: ["demo.sli.track10.financing-observation"]`; these are recorded symbol/type references, not suffixed fact IDs. The forward and reference runner snapshots differed. This is a real declaration-order failure, not an order-independent result. |
| Numeric witness candidate, equal observations | The admitted family-backed declaration produced EXPECTED and AVAILABLE witnesses for all five current financing claims. The live coordinator, forward runner and reference runner agreed; A, B and C each published `true`. Each EXPECTED witness pinned exactly one current raw financing finding. Each AVAILABLE witness pinned that same raw finding and its actual financing-result publication. Consumer direct pins and saved transitive source closure exactly matched membership, financing, witness and schooling inputs. |
| Numeric witness candidate, corrected observations in both orders | The same corrected source input was separately admitted with the membership consumer before and after its witness producers; the resolved rule sequences differed. Both runner snapshots and coordinator results agreed in both runs. A and B published `false`, and C remained `true`; complete finding identities and input pins matched across declaration orders. |
| Numeric witness candidate, shared-school retraction | Retracting the corrected shared schooling finding blocked A and B with `DEPENDENCY_INVALID` and `missing: []`, because each retained current financing claims whose results no longer all existed. C's complete membership finding and inputs remained unchanged. A/B blocked pins included exactly their membership claim and expected/available witness rows; they contained no direct financing-result branch publications. Saved transitive closure retained both current financing claims and only schooling support actually present. |
| Numeric witness candidate, independent-school retraction | A and B blocked with `DEPENDENCY_INVALID` and `missing: []` after each retained two current financing claims but only one available result. C blocked with `DEPENDENCY_ABSENT`, `missing: ["demo.sli.track11.financing-available"]`. A/B blocked inputs were exactly their membership source and expected/available witness rows. |
| Numeric witness candidate, empty C collection | Retracting C's sole current financing claim left its statement-membership claim active. Its consumer blocked with `DEPENDENCY_ABSENT`, `missing: ["demo.sli.track11.financing-expected", "demo.sli.track11.financing-available"]`; the saved direct input set contained only the membership claim. |
| Candidate 1, partial producer loss | Retracting the independent schooling finding blocked two financing producers while their financing source claims remained current. Candidate 1 still published `true` for A and B using the one remaining financing publication per subject, although each subject had two current expected financing claims. Its result pins expose only that successful subset. C's sole financing source claim was retracted; its membership consumer blocked with `DEPENDENCY_ABSENT` on the financing-observation symbol. |
| Correction and retraction effects | Candidate 1's differing case corrected the shared schooling finding before both runner passes; derived financing pins cite the correction and exclude its displaced predecessor. Candidate 2's correction and retraction paths use ordinary contribution and finding-retraction acts. Other current financing members remain visible; no result was assembled by hand. |
| Saved recovery | Each decisive run used `live_coordinate_run`; the unchanged Track 10 carrier captured the coordinator's publications, dispositions, support and pins. The temporary workspace and live objects were discarded before `loads()` reopened the Track 11 file. For both candidates the test compares coordinator publications and projected dispositions to the actual forward-runner snapshot; the readiness candidate also agrees with the reference runner. `complete` remains false because the existing carrier does not serialize four unrelated Track 8 horizon targets (`demo.ug.wlt.h0` and `demo.ug.wst.h0`, each referenced by a publication and disposition); this known carrier boundary is distinct from the consumer result. |

## Finding

Removing `requires` permits the collector to combine differing values when its
producer rules happen to resolve first, but the consumer-first candidate
records absence, the runner snapshots diverge, and a blocked expected producer
is silently excluded from a successful partial collection. The admitted
numeric-witness candidate separated readiness from equality in the tested
declaration grammar: it derived expected membership from each current raw
FINANCE claim, derived availability from each actual FINANCE_RESULT, and
blocked A/B when the per-subject counts differed. In the bounded Track 10
source graph, exact raw IDs, witness pins, consumer pins and saved support
matched the complete expected set, and both declared orders produced the same
corrected results. The empty case recorded both missing witness symbols.

This is test-local declaration evidence for the current source graph and one
producer rule per current financing claim. It does not establish general
collector type guarantees, family closure, arbitrary producer multiplicity,
or tax treatment. No engine, reader, schema, operator, type conversion or
tax-policy repair is within this unit.

## Verification and handoff

The Track 11 focused module asserts the control refusal, both Candidate 1
resolved rule orders and runner disagreement, Candidate 1's partial set,
Candidate 2's actual producer/consumer orders, exact witness membership and
pins, corrected values, shared and independent source loss, empty collection
refusal, and saved recovery. The saved envelopes and execution snapshots are
under ignored `temp/track11/`.

Local checks: `pytest tests/test_sli_track11_collection_declarations.py -q`
passed (3 tests, 104.34 seconds); targeted `mypy tests/test_sli_track11_collection_declarations.py`
passed; `pytest tests/test_kernel_fixtures.py -q` passed (2 tests and 5 subtests);
`python3 tools/governance_lint.py` was conformant; `git diff --check` passed.

After Foreman review, one captured full suite ran with loopback access:
`set -o pipefail; pytest 2>&1 | tee temp/track11/track11-full-suite.log`.
It exited 0 with 2,379 passed and 20 skipped in 262.46 seconds. The session
handle was 29593; the complete output is preserved at the ignored log path
above. Builder turn and tool-call totals are unavailable in this session.

This report is local evidence, not CI. G2 remains unpassed, ADR 0076 Part 3
remains open, and worksheet integration, reader acceptance and production
recording remain outside scope.
