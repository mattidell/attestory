# A4 — bounds: what the engine can hold, follow and refuse

Pass 1 of A4, the object [G1](../student-loan-circumstance-association.md#readiness-gates)
names. It classifies the demands A0, A1, A2 and A3 place on the engine and
produces the two lists A5 is held to. It chooses no shape.

**Evidence levels.** `run` = executed, naming the test. `read` = inferred from
committed source, however carefully, including by an independent reader.
`untested` = neither. G2 forbids chartering implementation on `read` claims about
mechanism.

**Discipline applied throughout:** before recording a gap, trace whether the
existing facts, evidence and rules already supply the demand.

It took two passes. The first pass moved three entries out of "missing" and still
under-claimed four more — D6, D8 and D13a already execute, and a demand this
document's own working set named (D16) had no row at all. The failure direction
was consistently the same: reasoning from one consumer's behaviour, or from a
document's absence of a test reference, to a conclusion about the engine. Every
`run` row below now names the test that establishes it, and every `read` and
`untested` row is a claim that no such test was found rather than that none was
looked for.

## The demands

| # | Demand | From | Level | Established by |
| --- | --- | --- | --- | --- |
| D1 | Per-item dispatch follows a recorded connection; the value depends on both sides; pins name the exact findings | A0, A3 | `run` | `tests/test_sli_circumstance_association_readiness.py` checks 1–2 |
| D2 | Losing the named target refuses **by name** | A2, A3 | `run` | Same module, check 3: `DEPENDENCY_ABSENT` naming the fact id, from the dispatcher's own resolution before the rule runs |
| D3 | A subject nobody associated produces no row at all | A3 | `run` | Same module, omission check |
| D4 | A consumer can require a fact **conditionally** — in some cases and not others | A3 | `run` | The production worksheet's own `conditional_dependency_set`, condition `count(box1) > 0`; `tests/test_sli_worksheet_line21_track3.py` drops a member and asserts the block and the name |
| D5 | A supported negative publishes a value while missing support blocks | A2, A3 | `run` | Prior milestone's disposable candidate: adverse answer publishes `0`, absent premise blocks |
| D6 | A rule can publish a **categorical conclusion** rather than an amount | A3 | `run` | `tests/test_capital_gain_distributions_line7a_t2_coordinator.py` runs `rule.schedule-d-required.conclusion` through `live_coordinate_run`: `EligibleSinglePayer` exercises the `no` branch, `ComponentNo` the `yes` branch, `ComponentAbsence` the `DEPENDENCY_ABSENT` path. Ceiling: the tests assert dispositions and downstream routing, not the literal string |
| D7 | A rule expression can obtain a **member value** from `collect_categorical_all_equal` | A0 | `read` — and the answer is no, **for that operator only**. Nothing here bears on per-member branching by other mechanisms; per-item dispatch is D1 and D13a | `collect_categorical_all_equal` returns one Boolean. **This is a limit on what an expression reads, not on what the record keeps**: witness facts are keyed `lender`+`statement`+`tax-year` and the runner pins every collected finding |
| D8 | The dispatcher follows a **corrected** target rather than a stale one | A2 | `run` | `tests/test_nominee_consequences_live.py::test_c5a_report_correction_yields_corrected_remainder` — a live per-item consumer (nominee reduction, grouping bound sources by report `fact_id`, not `evaluate_pairing_scoped_rule`): both findings in the act log, the current one pinned and the stale one excluded. Ceiling: follows the current finding at the same `fact_id`; settles nothing about D9 |
| D9 | Tell "still resolvable" from "still supported" — A2's middle leg | A2 | `untested` | Nothing. D2 and D8 are findability; this is the further question and must not be discharged by them |
| D10 | Hold the unresolved interval as its own state | A2 | `untested` | Nothing |
| D11 | Hold A3's states as distinct | A3 | `untested` | Nothing |
| D12 | The second adverse reading — stop treating a statement's box 1 as adequate grounds until the affected scope or amount is determined, by whichever route does it. **Not** "until enumeration": A3 withdrew that requirement and A5 stage 1's route (a) supersedes it | A3 | `untested` | Nothing. The third reading is `run` via D5; the first is partly D6 |
| D13a | Per-item outcomes are **isolated** under pairing dispatch — one item blocking does not take another down | A3 | `run` | `tests/derivation/test_pairing_dispatch.py::test_evaluate_one_block_is_per_pairing` and `::test_two_pairings_dispatch_independently`; pins do not cross. Ceiling: pairing dispatch, not any other consumer |
| D13b | The production worksheet's universal fold is **not** isolated — one statement's "no" blocks the whole route | A3 | `run` | `tests/test_f1098e_student_loan_interest_agi_track6.py::TestPathJMultiStatementDisagreement` — two statements disagreeing on one witness, both assertion orders, whole route blocked. Track 3's single-statement case is not multi-statement evidence and is not cited. This is the incumbent behaviour, and it is the opposite of D13a |
| D16a | A categorical telling can be **published in the same run** as amounts | A3 | `run` | `tests/test_capital_gain_distributions_line7a_t2_coordinator.py::test_line7a_publishes_and_line9_includes_once` — the conclusion publishes alongside line 7a, line 7b and line 9. Ceiling: this consumer **gates** line 7a on the conclusion (`requires` it, and its `when` is a `categorical_compare` against it), and line 7b publishes the literal `"checked"` and is a checkbox rather than an amount. The test never varies a rule that omits the declaration |
| D16b | A telling can be published **without changing** an amount | A3 | `read` | Nothing executes this. A rule reads what it declares, so a telling changes an amount only where some rule is wired to it — but the wiring can be **transitive**: line 9 does not name the conclusion, yet the conclusion gates line 7a and line 9 requires line 7a's total. So "does the amount rule declare a dependency on the telling" is not the whole coupling question |
| D14 | Two routes to the interest amount holding at once | A0 | `untested` | The enumeration route does not exist |
| D15 | A result carries A0's qualities of grounds | A0 | **no consumer named** | `finding.v2` carries a coarse `basis`; provenance already names the findings behind a result. Whether more is needed depends on a consumer nobody has named, so this is not recorded as a gap. **A5 stage 3 names it** — A6's revealing consumer and A0 F6's record requirement — and finds `basis` the wrong place. A favourable value resting on a named conclusion is honest in `RunResult.publications`, and recoverable by identity but not value from the completed record and `out.json`. **It does not reach the reader:** `presentation.json` walks through derived findings to raw leaves, so the conclusion is not emitted and the circumstances it examined become citations of the amount. `origin: "assertion"` means only "not via a declared default" and says nothing about whether the conclusion's subject was described. The carrier to the reader is open and owed to G2 and A6 |

## Ceilings on what has already run

- **The pairing-scope observation bounds one environment.** `require_closed` and
  `count` blocked `SOURCE_SET_UNCLOSED` in an environment **rebuilt in the test
  module**, mirroring the shape of an adapter written for nominee interest, whose
  two bound symbols and empty source set are that adapter's choices. This bounds
  that environment. It is not a dispatcher limitation, and it mandates no rewrite
  of the prior calculation.
- **Parameter reads and dependency pins do execute in pairing scope.**
  `tests/test_pairing_consequences.py::TestDependencyPinFidelity` publishes and pins
  a declared `parameter` reference from a pairing-scoped expression. The
  empty-parameter limitation belongs to **this milestone's own probe**, which passed
  empty parameters and canon into a rebuilt environment; it is not a property of
  pairing scope.
- **D4's ceiling:** the conditional set executed is the production worksheet's own,
  not one containing a schooling fact.
- **D5's ceiling:** disposable artifacts, never adopted.

## Only testable by changing production

One entry: whether the **existing worksheet** would require or tolerate a schooling
fact. Its dependency set is a committed production rule, and the owner's build
boundary excludes changing the existing worksheet's treatment here. Cost if ever
taken: an adopted-rule change with its own review, in a later milestone.

**This is not a bar on testing a candidate dependency declaration.** A disposable
candidate rule may declare a schooling fact in its own dependency set and be run, and
that needs no production change — the previous milestone did exactly this. What such
a test establishes is candidate-scoped: that *a* rule can require the fact and block
by name when it is absent. It says nothing about what the adopted worksheet would
do, and must not be reported as though it did.

## What A5 may rely on

D1, D2, D3, D4, D5, D6, D8, D13a and D16a — each within its ceiling. In ordinary
terms: a design may assume the engine can dispatch per identified item, follow a
recorded connection, follow a corrected target, refuse by name when the thing it
names is gone, keep one item's outcome from taking another down *under pairing
dispatch*, be required only in the cases a consumer names, distinguish a supported
negative from missing support, publish a conclusion rather than an amount, and
publish that conclusion in the same run as amounts.

**Not** that a telling can be published without changing an amount. That is D16b,
and it is `read` — the only consumer executed here gates an amount on its telling.

D13b is on this list in the opposite sense: a design may **rely on knowing** that
the incumbent worksheet fold is not isolated, and must not treat it as though it
were.

## Owed to A4's second pass, from A5's selections (stages 1 and 3)

Behaviours a selection needs that nothing demonstrates today, though a component or an
analogue has run. **A component having run is not the behaviour having run**, and these are
G2's to see rather than A4 pass 1's to have covered:

| Behaviour | Nearest thing that has run | Why that is not it |
| --- | --- | --- |
| One corrected circumstance reaching every statement its reference bears on | D8 — a consumer follows the current finding at a `fact_id` after a correction there | D8's test corrects one nominee report and checks the current finding is used. It exercises no shared subject across several statements |
| A partial reduction of a statement — a reduced figure once a portion is determined | D5 — an adverse answer produces a determined zero on disposable artifacts | A whole-statement zero is not a partial reduction. The arithmetic and the disposition both differ |
| A revealing consumer recovering an intermediate conclusion's identity **and meaning** at the reader, and stating a default-supported basis (A5 stage 3). Test cases: the nine-credit case; a financing claim identifying the period with no schooling circumstance, where the cited financing claim must not read as grounds for eligible student; and no financing claim at all, where A5 stage 4 attaches the default to the statement and the reader today sees the 1098-E and nothing about eligibility. In the first two, the conditions left to the filer (A5 stage 4, carried as the conclusion's rule citations) must reach the reader too; in the third no schooling condition applies and none may be shown | `explain()` over `LiveCoordinatorOutcome.publications` — in memory — returns the intermediate node with symbol, value and rule | Nothing durable holds values; `presentation.json` walks through intermediates and emits raw leaves as citations. An in-memory walk is not a reader, and the carrier is not chosen |
| One categorical conclusion published **per key of a single subject** — one per student-and-period, one per borrowing (A5 stage 3). The period key is supplied by a financing claim or a statement-grain scope claim; where neither exists, A5 stage 4 keys the conclusion on the **statement**, a third key kind this row now covers. The per-key publication must also **carry the rule's declared citations**, which the existing per-item paths do not do by default — they assemble their own pins without `pins_for` | D6 and D16a — a categorical conclusion published in the same run as amounts; D1 and D13a — per-item publication under pairing dispatch | D6 publishes one conclusion per return. Pairing dispatch publishes one finding per **pairing**, a pair of pinned sides; a conclusion keyed on one subject is not a pairing |

## What A5 may not rely on without new execution

D7, D9, D10, D11, D12, D14 and D16b. In particular, a shape that depends on **an
expression branching per member** (D7), on **telling resolvable from supported**
(D9), on **holding the unresolved interval as a state** (D10), or on **the second
adverse reading being expressible** (D12) is unbounded today, and G2 will refuse a
charter that rests on any of them until they run.

Note what is no longer on this list. Three capabilities were on it in the first
version of this document and are not gaps: publishing a categorical conclusion,
following a corrected target, and per-item isolation under pairing dispatch. Each
already executes. Declaring them missing would have forbidden A5 the one isolation
mechanism the engine actually has.

D15 is not on either list: it has no consumer, so there is nothing yet to rely on
or to be refused.
