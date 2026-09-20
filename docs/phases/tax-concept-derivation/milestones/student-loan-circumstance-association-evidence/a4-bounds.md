# A4 — bounds: what the engine can hold, follow and refuse

Pass 1 of A4, the object [G1](../student-loan-circumstance-association.md#readiness-gates)
names. It classifies the demands A0, A1, A2 and A3 place on the engine and
produces the two lists A5 is held to. It chooses no shape.

**Evidence levels.** `run` = executed, naming the test. `read` = inferred from
committed source, however carefully, including by an independent reader.
`untested` = neither. G2 forbids chartering implementation on `read` claims about
mechanism.

**Discipline applied throughout:** before recording a gap, trace whether the
existing facts, evidence and rules already supply the demand. Three entries below
moved out of "missing" by doing that.

## The demands

| # | Demand | From | Level | Established by |
| --- | --- | --- | --- | --- |
| D1 | Per-item dispatch follows a recorded connection; the value depends on both sides; pins name the exact findings | A0, A3 | `run` | `tests/test_sli_circumstance_association_readiness.py` checks 1–2 |
| D2 | Losing the named target refuses **by name** | A2, A3 | `run` | Same module, check 3: `DEPENDENCY_ABSENT` naming the fact id, from the dispatcher's own resolution before the rule runs |
| D3 | A subject nobody associated produces no row at all | A3 | `run` | Same module, omission check |
| D4 | A consumer can require a fact **conditionally** — in some cases and not others | A3 | `run` | The production worksheet's own `conditional_dependency_set`, condition `count(box1) > 0`; `tests/test_sli_worksheet_line21_track3.py` drops a member and asserts the block and the name |
| D5 | A supported negative publishes a value while missing support blocks | A2, A3 | `run` | Prior milestone's disposable candidate: adverse answer publishes `0`, absent premise blocks |
| D6 | A rule can publish a **categorical conclusion** rather than an amount | A3 | `read` | `packages/content/tax/2025/rule.schedule-d-required.conclusion.json` publishes `yes`/`no` as its symbol, in the production package. Cheaply raised to `run` by finding its executing test |
| D7 | A rule expression can branch on a **per-member value** from a universal-over-members operator | A0 | `read` — and the answer is no | `collect_categorical_all_equal` returns one Boolean. **This is a limit on what an expression reads, not on what the record keeps**: witness facts are keyed `lender`+`statement`+`tax-year` and the runner pins every collected finding |
| D8 | The dispatcher follows a **corrected** target rather than a stale one | A2 | `read` | `_index_by_fact_id` indexes current sources by fact id, so the current finding at that id is what resolves |
| D9 | Tell "still resolvable" from "still supported" — A2's middle leg | A2 | `untested` | Nothing. D2 and D8 are findability; this is the further question and must not be discharged by them |
| D10 | Hold the unresolved interval as its own state | A2 | `untested` | Nothing |
| D11 | Hold A3's states as distinct | A3 | `untested` | Nothing |
| D12 | The second adverse reading — stop treating a statement's box 1 as adequate grounds until enumeration | A3 | `untested` | Nothing. The third reading is `run` via D5; the first is partly D6 |
| D13 | One statement's adverse answer does not affect another's result | A3 | `untested` | **Not** established by the omission check, which observed an *unassociated* statement rather than an isolated one |
| D14 | Two routes to the interest amount holding at once | A0 | `untested` | The enumeration route does not exist |
| D15 | A result carries A0's qualities of grounds | A0 | **no consumer named** | `finding.v2` carries a coarse `basis`; provenance already names the findings behind a result. Whether more is needed depends on a consumer nobody has named, so this is not recorded as a gap |

## Ceilings on what has already run

- **The pairing-scope observation bounds one environment.** `require_closed` and
  `count` blocked `SOURCE_SET_UNCLOSED` in an environment **rebuilt in the test
  module**, mirroring the shape of an adapter written for nominee interest, whose
  two bound symbols and empty source set are that adapter's choices. This bounds
  that environment. It is not a dispatcher limitation, and it mandates no rewrite
  of the prior calculation.
- **No parameter read has executed in pairing scope.** The rebuilt environment
  passed empty parameters and canon.
- **D4's ceiling:** the conditional set executed is the production worksheet's own,
  not one containing a schooling fact.
- **D5's ceiling:** disposable artifacts, never adopted.

## Only testable by changing production

One entry: whether the **existing worksheet** would require or tolerate a
schooling fact. Its dependency set is a committed production rule, and the owner's
build boundary excludes changing the existing worksheet's treatment here. Cost if
ever taken: an adopted-rule change with its own review, in a later milestone. Not
approximated with a disposable fixture, which would pass for the wrong reason.

## What A5 may rely on

D1, D2, D3, D4, D5 — each within the ceiling above. In ordinary terms: a design
may assume the engine can dispatch per identified item, follow a recorded
connection, refuse by name when the thing it names is gone, be required only in
the cases a consumer names, and distinguish a supported negative from missing
support.

## What A5 may not rely on without new execution

D6 through D14. In particular, a shape that depends on **an expression branching
per member** (D7), on **telling resolvable from supported** (D9), or on **one
statement's answer not affecting another** (D13) is unbounded today, and G2 will
refuse a charter that rests on any of them until they run.

D15 is not on either list: it has no consumer, so there is nothing yet to rely on
or to be refused.
