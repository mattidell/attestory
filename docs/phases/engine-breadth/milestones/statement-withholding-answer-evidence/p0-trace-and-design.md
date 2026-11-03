# P0: a statement recorded without its withholding answer

Milestone: `statement-withholding-answer`. Branch
`milestone/statement-withholding-answer-2025`, base `f5efe368` (core v70,
registry v68, release v68). Charter: the P0
unit of the plan (removed at closeout; in history at `f5efe368`).

Evidence in this directory:

- `probe.py` / `probe-output.json`: 85 cases on the committed core v70, each
  through `live_coordinate_run`. Builders are the withholding-closure
  milestone's (`tests/test_withholding_closure.py`) on the v64 base plus the W-2G
  answers core v65 asks, the same base `tests/helpers/current_core_returns.py`
  (`base_return`) uses; core v70 accepts it. That helper itself runs only v66/v67,
  so the probe carries a v70 runner of its own (the shape of
  `tests/test_attachment_limited_part.py::run`).
- `prototype.py`, `prototype-output-eq.json`, `prototype-output-gte.json`,
  `prototype-line25b-v4-{eq,gte}.json`: the proposed core v71 built in a
  temporary copy outside the repository with `tools/package_successor.py`, and
  the same 85 cases run on it. Nothing under `packages/` or `tests/` changed.
- Data is synthetic `demo.*`. Every figure below is read from those outputs
  unless marked "hand". Hand figures are reconciled to the run in section 7.

Ceiling: a reproduced trace, a paper design, and a scratch prototype that
validates and behaves on the 85 cases. Track 1 must rebuild the prototype as
committed content and own its tests.

## Summary

- **The gap is real in all five families.** On v70 a Form 1099-INT, -DIV, -R or
  -G recorded without box 4, or a Form SSA-1099 without box 6, with the family's
  closure attested true, publishes line 25b without it, and the bottom line
  with it. The number is the same as if $0 had been answered (the cases are in
  section 1). A refund or amount owed is wrong by exactly the omitted amount.
- **Form W-2 is closed by a count.** Line 25a compares the number of box 2
  answers with the number of W-2s, and blocks when they differ. It blocks
  `DEPENDENCY_ABSENT` naming the box 2 fact; a $0 answer is a recorded finding
  with value 0, so it counts and is not absence.
- **The same count carries over to every 1099 family, with one boundary.** Each
  1099 box 4 (SSA box 6) is its own family whose members share the statement's
  identity with the statement's income box. Counting the box 4 members against
  the members of the statement's income family (INT box 1, DIV box 1a, 1099-R
  IRA box 1, 1099-G box 1, SSA box 5) catches a missing answer. It cannot see a
  statement that never reaches that income family (section 4, "What it does not
  catch").
- **The fix is content-only: one new citizen.** Line 25b v4, in the already
  published `rule-artifact.v4` (the version that has `count`), keeps v3's five
  `require_closed` guards and adds five count checks. No kernel, schema,
  expression-operation or engine change. No stop condition met.
- **The block names the fact, not the statement.** It is
  `DEPENDENCY_ABSENT` on `f1099int.box4-withholding` (and the like), the same way
  line 25a names `w2.box2-withholding`. Naming which statement lacks its answer
  would need a per-key join the rule language does not have. That is an engine
  change; not designed.
- **Cost.** Every committed return on an earlier core is untouched (earlier
  packages, goldens and saved presentations stay byte-identical). A v70
  workspace with a statement lacking its answer is, on v71, blocked at line 25b
  until it records that answer (the amount, or $0) and re-answers the family's
  existing closure question. Nothing else moves (section 5).
- **Recommendation:** `count(answers) >= count(statements)` (`gte`) rather than
  equality, so a return whose statements all carry answers never newly blocks
  (section 4). One decision for the foreman, below.

## 1. The gap on v70, per family

Base return: single, wages 50,000, one W-2 with box 2 of 4,500, standard
deduction, every closure answered (line 24 = 3,875, refund 625 with nothing
else). "Closed" below means the family's box 4 (box 6) closure is attested true
at its current horizon, which is what the recorder does. Source:
`probe-output.json`, family `int`, `div`, `ira`, `g`, `ssa`.

One statement, income box recorded, **no box 4 answer, family closed**, against
the same statement with **$0 answered**:

| Family | Income | Line 24 | 25b (no answer) | 33 | Bottom line | 25b ($0 answered) | Bottom line ($0) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1099-INT | box 1 500 | 3,935 | 0 | 4,500 | refund 565 | 0 | refund 565 |
| 1099-DIV | box 1a 500 | 3,935 | 0 | 4,500 | refund 565 | 0 | refund 565 |
| 1099-R | box 1 10,000 | 5,075 | 0 | 4,500 | owed 575 | 0 | owed 575 |
| 1099-G | box 1 6,000 | 4,595 | 0 | 4,500 | owed 95 | 0 | owed 95 |
| SSA-1099 | box 5 12,000 | 5,099 | 0 | 4,500 | owed 599 | 0 | owed 599 |

The two columns are identical: absence and $0 publish the same number, and
nothing blocks (no blocked row, `root_blocks` empty). That is the gap. It
matters when the unrecorded amount is not 0:

| Family | Two statements, answers recorded | Line 25b | Line 33 | Bottom line | If the second answer were also recorded |
| --- | --- | --- | --- | --- | --- |
| 1099-INT | 50, none | 50 | 4,550 | refund 579 | 25b 80, refund 609 |
| 1099-DIV | 40, none | 40 | 4,540 | refund 569 | 25b 60, refund 589 |
| 1099-R | 1,200, none | 1,200 | 5,700 | owed 55 | 25b 2,000, refund 745 |
| 1099-G | 600, none | 600 | 5,100 | refund 25 | 25b 1,000, refund 425 |
| SSA-1099 | 800, none | 800 | 5,300 | owed 895 | 25b 1,300, owed 395 |

Joint returns behave the same (wages 80,000, W-2 7,000; `joint-*` cases): INT
50 recorded of 80 gives refund 1,608 instead of 1,638, and the other four
families likewise. A return with every family populated and one second
statement unanswered shifts the bottom line by exactly that statement's amount
(`all/single-only-*-second-not-answered`: 25b 4,310 / 4,320 / 3,540 / 3,940 /
3,840 against the complete 4,340, line 33 8,810 / 8,820 / 8,040 / 8,440 / 8,340
against 8,840).

## 2. How Form W-2 box 2 is checked on line 25a

`rule.form1040-line25a` v1 (`rule-artifact.v4`):

```
when:  any[ compare eq ( count(w2.box2-withholding, set w2-box2),
                         count(w2.box1-wages,       set w2) ),
            ref(w2.box2-withholding) ]
value: round( add( collect(w2.box2-withholding, set w2-box2) ) )
```

- **Citizens:** the rule; `family.w2-box2` (member predicate
  `w2.box2-withholding`) and `family.w2` v2 (member predicate `w2.box1-wages`);
  their two closure mappings. `count` (`evaluator.py` about 390) raises
  `SOURCE_SET_UNCLOSED` unless its source set is in `closed_sets`, so both the
  box 1 and box 2 families must be closed before the comparison happens.
- **Equal counts:** the first `any` argument is true; the rule publishes.
- **Unequal counts:** the first argument is false, so `any` evaluates
  `ref(w2.box2-withholding)`. The `ref` of that plural fact type raises `DEPENDENCY_ABSENT` naming it
  (observed; I did not trace why the evaluator has no bound scalar for it). The rule blocks naming the box 2
  fact, never a particular W-2. Reproduced on v70: one W-2 with no box 2 answer, or
  two W-2s with one answer, closure attested true: line 25a
  `DEPENDENCY_ABSENT [w2.box2-withholding]`; 33, 35a, 37 blocked
  (`w2/one-w2-no-box2-closed`, `w2/two-w2-one-box2-closed`).
- **How $0 is recorded:** box 2 is a plain `assertion` act with
  `fact_id = w2.box2-withholding|employer=…,w2-slip=…,tax-year=2025` and
  `value 0.0` (the fact type's `value_schema` is `minimum 0`). It is a recorded
  finding, so it counts as an answer; absence is no finding at all. Reproduced:
  one W-2 with box 2 of 0: 25a 0, owed 3,875; two W-2s, the second answered 0:
  25a 4,500 (`w2/one-w2-box2-zero`, `w2/two-w2-second-box2-zero-closed`).
- **Limit (already in the retrospective):** a count catches a missing answer,
  not a mismatched one.

## 3. How each 1099 statement and its withholding are recorded

There is no interactive recorder for these forms in the repository. The
entry loop runs bounded W-2 entry only; a 1099 is recorded as acts, as the test
builders (`tests/test_form_1099_withholding.py`) do. The sequence is the same
for four of the five forms:

| Form | Statement entities | Income box | Withholding box | Same-statement companions |
| --- | --- | --- | --- | --- |
| 1099-INT | payer + statement (`1099int-statement`), 2 intro acts | member-transition into `f1099int.b1` (box 1) | **separate** member-transition into `f1099int.b4` | none for box 1 |
| 1099-DIV | payer + statement, 2 acts | `f1099div.1a` | `f1099div.b4` | none for box 1a |
| 1099-R (IRA) | payer + statement, 2 acts | `f1099r.ira-fully-taxable` v2, after 4 companion assertions (box 2a, checkbox, code 7, 2b false) | `f1099r.box4` | the 4 above |
| 1099-G | payer + statement, 2 acts | `f1099g.1` (box 1) | `f1099g.b4` | none since v59 |
| SSA-1099 | statement only, 1 act | `ssa1099.benefits` (box 5), after box 3, box 4, recipient, kind, lump-sum assertions | `ssa1099.b6` | the 5 above; box 6 witness dropped in v59 |

- **One act or several:** several. The withholding amount is its own act. It
  is a member-transition into its own family, on the same identity keys
  (`payer`, `statement`, `tax-year`; SSA: `statement`, `tax-year`), not a field of
  the income member. Each transition advances that family's horizon, and the
  family's closure (`<family>.source-closure`, key `family-horizon`) is a
  separate assertion at the final horizon.
- **Which fact carries the statement:** the income-box member. Nothing carries
  "this statement exists" for the rule language except its income-family member
  (no rule reads an entity introduction).
- **$0 vs absence:** each box 4 / box 6 fact type has `value_schema minimum 0`;
  a recorded 0 is a member (probe `*/one-statement-zero-answered`, count 1),
  absence is no member. Today they compute alike.
- **Companion declarations (v70, `packages/tax/loader.py`):** no pair requires a
  box 4 or box 6 answer. v59 removed the 1099-G box-1 -> box-4 authority pair
  and the SSA box-5 -> box-6 witness pair when the families were added; the
  1099-R vocabulary note records that a box 4 presence pair was refused as a
  global, unscoped invariant. The package-scoped dictionary
  `domain_package_companion_declarations()` has an entry per core; core v71
  needs its own (a copy of v70's), as v61 did, or recording a nonzero 1099-G
  box 4 is refused under it. The prototype adds it in process only.

## 4. Design

### Recommended: line 25b v4 (one citizen)

| Citizen | From | To | Schema | Change |
| --- | --- | --- | --- | --- |
| `tax.us.2025.rule.form1040-line25b` | v3 | **v4** | `rule-artifact.v3` -> `rule-artifact.v4` | `when` keeps v3's five `require_closed` and adds, per family, `any[ compare gte (count(box 4 fact, box 4 set), count(income fact, income set)), ref(box 4 fact) ]`. `value`, `pins`, `requires`, `blocked` as v3; notes updated. |

The five checks (box 4 / box 6 set vs the statement's income set):

| Family | Answers (fact, set) | Statements (fact, set) |
| --- | --- | --- |
| 1099-INT | `f1099int.box4-withholding`, `f1099int.b4` | `f1099int.box1-interest`, `f1099int.b1` |
| 1099-DIV | `f1099div.box4-withholding`, `f1099div.b4` | `f1099div.box1a-ordinary`, `f1099div.1a` |
| 1099-R | `f1099r.ira-box4-withholding`, `f1099r.box4` | `f1099r.ira-box1-taxable-distribution`, `f1099r.ira-fully-taxable` |
| 1099-G | `f1099g.box4-withholding`, `f1099g.b4` | `f1099g.box1-unemployment`, `f1099g.1` |
| SSA-1099 | `ssa1099.box6-voluntary-withholding`, `ssa1099.b6` | `ssa1099.box5-net-benefits`, `ssa1099.benefits` |

Totals for Track 1: **1 new citizen** (the rule, in `rule-artifact.v4`, which
the v70 package already admits and line 25a already uses), the v71 package,
registry v69 and release v69 built by `tools/package_successor.py` (a one-member
change set; the manifest diff only adds the rule's checksum and the package
entry; one inherited inconsistency, `schedule3-line1-direct-ftc` v3, as on
v70), and one entry in `packages/tax/loader.py` for v71. `rule-artifact.v4`
is `v3` plus the `count` and `block` operations (diffed), so nothing in the
rule's other expressions changes.

**Behaviour.** The rule publishes only when all five families are closed
(existing guard, evaluated first, so the order of existing blocks is
unchanged) and each family has at least as many answers as statements. Else it
blocks. Line 25d, 33, 34, 35a, 36 and 37 wait behind it through the existing
`DEPENDENCY_ABSENT` chain; lines 24 and 25a still publish.

**What it names.** `DEPENDENCY_ABSENT` with `missing = [<box 4 / box 6 fact>]`
for the first failing family in the order INT, DIV, 1099-R, G, SSA (an
INT-and-G return names INT; the G block appears after INT is answered; the
second half is by construction, not run). It does not name the statement.

**On the `ref` fallback:** it is reached only when the counts disagree. In every
mismatch case run (including exactly one answer recorded) the rule blocked, rather
than being held as not applicable. Observed, not traced in the evaluator.

### `eq` vs `gte`

Both prototypes are in the evidence. They differ in one case:

| Case | v70 | v71 `eq` | v71 `gte` |
| --- | --- | --- | --- |
| Two INT statements, both answered, plus a third box 4 answer on a statement with no box 1 recorded | 25b 87 | **blocked** | 25b 87 |

`eq` mirrors line 25a. It blocks a return whose statements all carry answers
(contradicting "such a return computes exactly as v70"), whenever an answer
exists for a statement the income family does not hold. `gte` never blocks that
return and blocks exactly the case the milestone names (fewer answers than
statements). Neither can pair an answer to its own statement. **Recommendation:
`gte`.**

### What it does not catch (limits to state, not fix)

1. **A statement that never reaches the counted income family.** A 1099-INT
   recorded only through box 8, or a 1099-DIV only through box 12, has no member
   in `f1099int.b1` / `f1099div.1a`, so the count does not see it: 25b publishes
   as on v70 (`census/int-box8-only-statement-no-box4`,
   `census/div-box12-only-statement-no-box4`). There is no single family that
   holds "a Form 1099-INT exists".
2. **A surplus answer hides a missing one.** An answer on a statement not in the
   income family offsets another statement's missing answer: counts 2 and 2,
   25b publishes 57 (`census/int-box4-on-a-statement-without-box1`). W-2's
   check has the same blindness.
3. **Scope of the income families.** 1099-R means IRA-family statements only
   (code 7); 1099-G means a recorded box 1; SSA means a recorded box 5. Whatever
   those forms do outside them is outside this check.
4. **Closure of the income family** is read too. A statement count of an
   unclosed income family blocks 25b `SOURCE_SET_UNCLOSED` naming it. Where that
   matters (DIV box 1a closure unanswered) the return is already blocked at line 3b
   and the bottom line (`income-closure/div-1a-closure-unanswered-box4-answered`:
   v70 line 24 and 33 already blocked; v71 adds the 25b block). I could not
   exercise the SSA case: the Social Security hand-over re-attests that closure.

### Alternatives considered

| Alternative | Citizens | Verdict |
| --- | --- | --- |
| **Per-subtotal successors**: five `rule.f1099*-subtotal` v3 each with its own count guard, plus line 25b v5 pinning them | 6 | Names every incomplete family at once and lets the explanation walk end at the subtotal. Same counts, same blind spots, same filer ask. Five more checksums, pins, explanation edges. Not smallest; the withholding-closure P0 chose the single rule for the same reason. |
| **Package-scoped presence pairs** (`domain_package_companion_declarations`: income-box member requires the box 4 member, as v58 required the G/SSA authority) | 0 content, loader entry | Refuses at recording instead of blocking at the line, so an existing v70 workspace is refused whole on adoption (ADR-0082 decision 4) rather than asked a question; the box 4 transition currently follows the income transition, so it also reorders every recorder. A box 4 member is a family member, not a plain companion; I did not test that the kernel accepts the pair across a member-transition. Not the milestone's stated shape ("stops line 25b"). Not designed further. |
| **Per-statement join** (match each answer to its own statement; name the statement) | 1 + an operation | Needs a keyed join the rule language lacks: an expression-operation or engine change. Stop condition; not designed. Would remove limits 1, 2 and the fact-not-statement naming. |
| **Edit `collect`** to read closure with members | n/a | Engine change, changes every family; excluded by the milestone. |

## 5. Cost

**Earlier packages, goldens, presentations:** byte-identical. v71 adds a rule
file and appends two registry entries; no published file, checksum or version
changes (manifest diff reviewed in the prototype: additions only). v70 and
earlier are pinned.

**Committed fixtures and sample workspaces on v70:** none carries a 1099
income statement.

- `packages/sample_data/entry_loop_v70/workspace/acts.jsonl` (the only committed
  v70 workspace): adopts the five box 4 / box 6 vocabularies and records no
  statement of any 1099 family. Unaffected.
- `packages/sample_data/entry_loop_t1`: core v6, records 1099-INT box 1 and
  1099-DIV box 1a with no box 4; pinned to v6, unaffected.
- Sample presentations/goldens that mention these families
  (`form_1099_withholding/…`, `refund_or_amount_owed/…`, the per-form
  scenarios) are pinned to the earlier cores they were produced on and stay as they are.

**Tests on v70 and on the helpers (static survey, not run on v71):** `tests/test_attachment_limited_part.py`
(v69/v70) uses a W-2G return with no 1099 statement: unaffected.
`tests/helpers/current_core_returns.py` (v66/v67) adders record box 8, box 12,
box 7 (with box 1a only as a plain assertion) and Form 1098-E; none holds an
income-box member in the five counted families, so none changes on v71
(`census/*` cases, and `current_core_returns` adders were not run on v71; this is
static). Tests that record an income-box statement with no box 4 on cores v61 to
v69 and are pinned there, so they do not move: `test_collect_closure.py`,
`test_collect_closure_regression.py`, `test_attachment_closure.py`,
`test_closure_questions.py` (v68, v69), `test_interest_cents.py` (v67, v68),
`test_itemization_cents.py` (v65, v66), `test_correction_current_core.py` (v66),
`test_withholding_closure.py` (v60, v61). Any of them re-pointed at v71 would
block line 25b until it adds an answer. Track 1's own new cases are the only
tests that run on v71. The entry loop has a v70 profile
(`packages/derivation/entry_loop.py`); giving v71 one is a separate decision,
and the entry-loop PR in flight touches that file.

**What a v70 return is asked on v71.** Each statement lacking its answer: its
box 4 (SSA: box 6), the amount or $0. Recording it is a member-transition, which
advances that family's horizon, so the family's existing closure question
("Have you recorded every federal income tax withheld amount in box 4 of every
Form 1099-INT …") is behind and must be answered again. No new question is
created. Measured: answer recorded, closure not re-attested -> 25b
`SOURCE_SET_UNCLOSED [<family>]`; closure re-attested -> publishes what v70
published (`adopt/*`, 10 cases, five families). A v70 return whose statements
all carry answers, including $0, computes identically (every `*-answered`,
`*-zero*`, `all/*-every-statement-answered` case: lines 24 to 37 equal on v70
and v71; finding ids differ, as on any successor).

## 6. Prototype result

85 cases. Under `gte`, 58 have identical lines 24, 25a, 25b, 25d, 33, 35a and 37
on v70 and v71 and 27 differ; under `eq`, 57 and 28. Every difference is a
line 25b block: all 26 cases where a counted statement has no answer
(`DEPENDENCY_ABSENT` naming that family's box 4 / box 6 fact), plus the DIV 1a
closure case above (`SOURCE_SET_UNCLOSED [f1099div.1a]`), plus, under `eq` only,
the surplus-answer case. No case errored. Every `answered` / `zero` /
`no-withholding` / W-2 case is identical.

## 7. Hand-computed expectations (single unless marked)

Base: taxable income 50,000 - 15,750 = 34,250; the tax table's midpoint row
34,275 gives 1,192.50 + 12% x 22,350 = 3,874.50 -> 3,875. Refund = 25a + 25b +
25c - line 24.

| # | Case | v70 | Expected v71 |
| --- | --- | --- | --- |
| 1 | 1099-R 10,000, box 4 unanswered, closed. Taxable 60,000 - 15,750 = 44,250, row 44,275: 1,192.50 + 12% x 32,350 = 5,074.50 -> 5,075 | 25b 0, 33 4,500, owed 575 | 25b, 25d, 33, 35a, 37 blocked, `DEPENDENCY_ABSENT [f1099r.ira-box4-withholding]`; 24 = 5,075, 25a = 4,500 publish |
| 1b | the same, box 4 answered $0 | owed 575 | identical to v70 |
| 2 | Two 1099-G 6,000 and 4,000, box 4 600 on the first only, closed. Income 10,000, so line 24 is 5,075 as in case 1 | 25b 600, 33 5,100, refund 25 | blocked as case 1 (`[f1099g.box4-withholding]`) |
| 2b | second answered $0 | refund 25 | identical |
| 2c | second answered 400 | 25b 1,000, 33 5,500, refund 425 | identical |
| 3 | One per family, one statement, no answer, closed: INT 500 (24 = 3,935), DIV 500 (3,935), 1099-R (case 1), 1099-G 6,000 (taxable 40,250, row 40,275: 1,192.50 + 12% x 28,350 = 4,594.50 -> 4,595; owed 95), SSA-1099 12,000 (85% tier: taxable 44,450, row 44,475, 5,098.50 -> 5,099; owed 599) | 25b 0; refund 565 / 565 / owed 575 / 95 / 599 | each blocked naming its own box 4 / box 6 fact; $0 answered identical to v70 |
| 4 | Joint, wages 80,000, W-2 7,000, two 1099-INT 500 and 300, first answer 50, second none. Taxable 80,800 - 31,500 = 49,300, row 49,325: 2,385 + 12% x 25,475 = 5,442 | 25b 50, 33 7,050, refund 1,608 | blocked `[f1099int.box4-withholding]`; second $0: identical (refund 1,608); second 30: 25b 80, refund 1,638 |
| 5 | No 1099 at all: refund = 4,500 - 3,875 | 625 | 625, unchanged |
| 6 | Every family complete, two statements each: 25b = 80 + 60 + 2,000 + 900 + 1,300 = 4,340; 33 = 8,840 | owed 2,943 (line 24 11,783) | identical |
| 7 | Every family complete, INT's second statement unanswered | 25b 4,310 | blocked `[f1099int.box4-withholding]`; $0: 4,310 identical |
| 8 | INT and G both lacking | 25b 3,910 | blocked naming INT first |
| 9 | A v70 return adopted onto v71, one statement lacking: asked its answer, then the closure | published | blocked until answered; after: identical to v70 |
| 10 | W-2 two slips, second box 2 absent | 25a blocked | unchanged (25a untouched) |

## Open decisions for the foreman (Decide step)

1. **`gte` or `eq`** (section 4). Recommendation: `gte`.
2. **Accept the boundary.** The check protects every statement that reaches its
   income family and none that does not (limits 1 to 3). If the owner wants INT
   box 3 / box 8 / box 10-only statements or DIV box 2a / 7 / 12-only
   statements covered, the check needs one family per statement; that is a
   different, larger design.
3. **Block naming.** The block names the fact (`f1099g.box4-withholding`), not
   the statement. Wording the filer reads ("a Form 1099-G has no box 4 answer;
   enter 0 if none was withheld") is a presentation matter for the Decide
   step; the retrospective already lists "name the closure question, not the
   family id".
4. **Reuse `rule-artifact.v4`** for a v3 rule (admitted already; line 25a uses
   it). Confirm that is not a "new schema".
5. **`packages/tax/loader.py` v71 entry**: needed; not kernel, evaluator, schema
   or operation (as v61).
6. **Entry-loop profile for v71** and the current-core test helpers (still v67):
   out of this milestone; the entry-loop PR is in flight.

## Stop conditions

None met. No kernel, schema, expression-operation or engine change is needed;
no published file changes; a return whose statements each carry an answer
computes as on v70.
