# Track 0 adversarial closure: the sale family audit

Evidence for `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate". The
design under test is the seven fixes that Decisions 1-5 in
`docs/phases/engine-breadth/milestones/sale-family-audit.md` take
(`tax_activity`, `no1099b_count`, `base_activity`, `admission_reads`,
`paired_rows`, `box4_question`, `box7_question`). Charter:
`docs/reviews/sale-family-audit/charter-track0.md`. This is a scratch
prototype only. It makes no production, test or content edits and uses only
synthetic `demo.*` findings.

Source ref: `milestone/sale-family-audit-2025` at `0ba2a011` (core v81,
registry v79, release v79).

## How the evidence was built

- `prototype.py` builds the scratch core v82, registry v80 and release v80
  from v81 with `tools.package_successor`, in a temporary copy of the
  content tree outside the repository.
  - `FIXES` holds the seven decided fixes. `REPAIRS` holds the three Track 0
    repairs below. `SWITCHES` is both lists, and is what `main` builds by
    default (`prototype-build.json`).
  - The decided design has 27 member edits (5 adds, 22 replacements). The
    final design has 29 (5 adds, 24 replacements). Neither reports an
    inherited inconsistency, and the build asserts that every file it writes
    is new, so no existing content file changes.
- `track0.py` runs every case through `live_coordinate_run` and writes
  `track0-output.json` (the cases, the field sentences and the static
  surface) and `track0-rerun-output.json` (the 213 v81 returns).
  - It loads `prototype.py`, `audit_harness.py`, `probe.py` and
    `rerun_v81.py` under unique names (`sale_family_audit_*`) and sets no
    attribute on any of them. The only in-process change is the harness's
    own per-run `loader_entries`, the two loader entries a scratch core needs.
  - Designs: `decided` (FIXES), `final` (FIXES and REPAIRS), and the
    published v81 for the traces that compare with it.
  - Every case runs in both answer modes. In `honest` mode the filer
    answers the Exception 1 question as a filer with these sales must. In
    `base_exception1` mode the harness's base answers ("only box 2a gains",
    "no capital losses") stand, as in every earlier sale milestone. The
    20 polarity cases (`p_*`) give their own Exception 1 answers.
- The box 4 and box 7 answers follow the design. On `decided` there is one
  answer per return. On `final` there is one answer per recorded Form 1099-B
  statement (`box_answers`). Unless a case says otherwise, every answer is
  "no".
- Every check below is in `track0.py` `verdict`. A case passes only if:
  - the run stopped `saturated`;
  - the presentation model passed `validate_presentation_model`, with no
    duplicate form-field id;
  - every watched publisher recorded exactly one disposition row (45 on
    v82, 43 on v81: every Schedule D line rule, Form 1040 lines 7a, 16, 24,
    25b, 33, 34 and 37, the preferential base, every attachment the package
    declares, the ten sale counts (eight on v81), and the four admission
    checks and six amounts checks);
  - the hand values publish (`expect: values`), or Form 1040 lines 16, 34
    and 37 do not all publish (`expect: block`);
  - every pinned row is (disposition, code, missing) as pinned;
  - every expected question is asked.
- Hand values are `probe.hand`: the harness wage return (single, wages
  50,000, W-2 withholding 4,500, standard deduction 15,750, taxable income
  34,250 before capital gains), the 2025 Tax Table at the row midpoint, and
  the Qualified Dividends and Capital Gain Tax Worksheet (0% up to 48,350).

**Run totals** (`track0-output.json` `verdicts`):

| Design | Right | Correctly blocked | Observed | Rejected at entry | Wrong or blocked wrongly |
| --- | --- | --- | --- | --- | --- |
| final | 122 | 156 | 8 | 10 (the five negative-proceeds cases, as on v81) | **0** |
| decided | 52 | 64 | 8 | — | **6** (the counterexamples below) |
| v81 | 5 | 4 | 8 | — | 3 (D1 and D3, which the fixes repair) |

P0's 81 cases were rerun on `final` in both modes (`p0_*`). All 162 runs are
as expected. Each has the same Schedule D and Form 1040 lines, the same
attachments and the same preferential base as P0's decided v82 run
(`probe-output-v82.json`). The repairs change nothing outside box 4, box 7
and two sentences.

Abbreviations: `cbz` is `closure_backed_zero`, `cz` is `computed_zero`, `gi`
is `guard_inapplicable` and B is blocked. TI is Form 1040 line 15, tax is
line 16, and "pub / gi" is the Form 8949 / Schedule D attachment. Q1, Q2 and
Q3 are the grouped noncovered, no-1099-B and code B questions.

**Result: all six artifacts PASS on the changed prototype.** Track 0 found
one counterexample on the decided design, shown in three traces (six
runs), and one gap in what two changed lines say. Three content repairs fix
them. No engine, schema, expression or recording change is needed. No v81
return publishes a different number.

## Design changes made to the prototype

Each repair is a switch in `prototype.REPAIRS`, and all are on in `final`.

| Repair | Counterexample on the decided design | After the repair |
| --- | --- | --- |
| `statement_box4` | The box 4 answer is one answer per return. It stays current when a sale from a Form 1099-B statement it never covered is recorded later. `t2_s2`: a box E sale on statement A, box 4 answered no, then a second box E sale on a new statement B that shows 1,440 of backup withholding, and Q1 answered yes again. Decided publishes line 25b 0 and a 625 refund (TI 40,250, tax 3,875). The true return has line 25b 1,440 and a refund of 2,065, which this return does not compute. `t2c_s1` is the same on line 1a: no grouped question goes stale, and decided publishes TI 41,250, tax 4,715 and 215 owed, without the 1,440. Both modes | The answer is one per recorded statement (`f1099b.statement-box4-withholding-reported`, keyed by the statement entity and tax year). Line 25b v6 requires an answer for the statement of every recorded Form 1099-B sale (`require_paired` on `statement`), and blocks on a "yes" for any statement (`collect_categorical_all_equal`, read only when a Form 1099-B sale count is above zero). `t2_s2` and `t2c_s1` now block line 25b with `(blocked, DEPENDENCY_ABSENT, [f1099b.statement-box4-withholding-reported])`, and the page asks "For each Form 1099-B or substitute statement you recorded a sale from, does it show federal income tax withheld in box 4?" A second sale on a statement already answered computes without asking (`t2_same_statement`: line 9 6,000, TI 40,250, tax 3,875) |
| `statement_box7` | The same for box 7. `t3_s2`: a box E gain on statement A with box 7 answered no, then a loss of 3,000 / 5,000 on a new statement B whose box 7 is checked. Decided publishes Schedule D line 16 2,000, line 7a 2,000 and TI 36,250. The loss based on the box 1d gross proceeds is not allowed, so no line from 16 on can publish | Per statement as well (`f1099b.statement-box7-loss-not-allowed`). Schedule D line 16 v3 requires every recorded statement's answer and blocks on any "yes". `t3_s2` blocks Schedule D line 16 with `(blocked, DEPENDENCY_ABSENT, [f1099b.statement-box7-loss-not-allowed])` and asks the box 7 question. On a "yes" it is refused (`t3_s3_yes`) |
| `field_words` | Not a wrong number. Form 1040 line 16 v7 and line 7a v9 now also wait for the ten sale counts. Their unchanged fields (line 16 v2, line 7a v1) said the line waits only for "your taxable income, your filing status, your qualified dividends and capital gain, or your covered sale proceeds" (line 16), and "Exception-1 authority ... or the box-2a family" (line 7a). The page shows the field sentence whenever no question attaches | Line 16 field v3 adds "It also waits for your answers about each kind of sale, because whether you recorded any sale decides whether your tax is figured with Schedule D." Line 7a field v2 adds "It also waits for your answers about each kind of sale and for Schedule D, because any recorded sale puts line 7a on the Schedule D route." No value or disposition changes |

Decisions 1-5 are otherwise unchanged. Decision 4 ("box 4 and box 7 are
refused by answer") still holds. The answers are per statement, and a "yes"
still refuses.

The gate requires each counterexample to be fixed or refused by an answer.
Here:

- **Fixed:** the three above.
- **Refused by an answer** (the answer is false, or puts the sale outside
  the class, and the return publishes no Form 1040 tax or refund):
  - a box 4 "yes" (`b4_yes_*`, `t2_s3_yes`);
  - a box 7 "yes" (`b7_yes_*`, `t3_s3_yes`), including one on a statement
    whose only sale is a gain (`b7_yes_gain`; owner question 3);
  - an Exception 1 "only box 2a gains" or "no capital losses" answered no
    while nothing is recorded (`m_empty_exc1_*`, `m_2a_only_exc1_only2a_no`,
    and `t4_s1_removed` after the only sale is removed). Line 16 is
    `guard_inapplicable` and lines 34 and 37 block. This is identical on v81
    in all three (owner question 2).
- **Not a counterexample:** an Exception 1 answer that a later sale makes
  false is never read once a sale is recorded. All 20 polarity cases
  compute the same return in all four polarities.

No other counterexample stands.

## 1. Authority-lifecycle table

**PASS.** Each row names the cases that would fail if the row were wrong.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| The eight Form 1099-B sale counts `f1099b.{covered,covered-w,noncovered,code-b}-{st,lt}-count` (v81 rules, unchanged) and the box C / F counts `f8949.no1099b-{st,lt}-count` (new) | The number of current sales on one family | The family at its current horizon | The family's closure: the literal per-family closure for covered and code W, and Q1, Q2 or Q3 for the grouped families. A count blocks `SOURCE_SET_UNCLOSED` naming its family | Any member transition moves the horizon. The closure is then stale until it is re-closed or re-answered, and every consumer blocks and asks that family's question: `t1_s1` (Q1), `t5_s1` (Q2), `t2_s1`, `m_empty_q{1,2,3}_unanswered`, `m_empty_covered_unclosed` (the covered question), `m_empty_w_unclosed`. The counts are derived and recomputed on every run |
| `long_term` on a covered or code W sale (read by admission v2) | Box 2: the sale is long-term | One sale | The filer's assertion of the sale | Correction by supersession. A value naming the other term refuses the sale (`term-mismatch`): P0 `a2`, `a3`, `n_covered_lt_says_short`, `n_w_lt_says_short`. Each blocks the family's admission check `(blocked, DEPENDENCY_INVALID, [])` |
| `box_1g_wash_sale_adjustment` on a line 1a or 8a sale (admission v2) | Box 1g shows a nondeductible wash-sale loss, so the sale is reported on Form 8949 with code W, not directly | One sale | The assertion | Correction. "yes" refuses the sale (`needs-form-8949`): P0 `a1`, `n_covered_lt_box1g` |
| Row-to-sale pairing (admission v2 and the admission check v2 `require_paired`) | Each proceeds, basis and (code W) column (g) row is this sale's own amount | One sale; the join uses all of the sale's identity keys | The rows and the sale. `require_paired` on `transaction` in the admission check's sales path | Recomputed every run. A row that differs from its sale refuses it: P0 `d6` and `d7`, `n_w_proceeds_row_disagrees`, `n_covered_two_sales_one_disagrees`. A missing row blocks `(blocked, DEPENDENCY_ABSENT, [the row's fact type])`: P0 `d8`, `n_covered_basis_row_missing`, `n_w_adjustment_row_missing`, and `n_covered_two_sales_one_rowless`, where another sale's rows are present. Two sales with their own rows compute (`n_covered_two_sales`: 3,000 + 4,000, TI 41,250, tax 4,715; `n_w_two_sales`: −700 + 1,000) |
| `f1099b.statement-box4-withholding-reported` (`statement_box4`) | "This Form 1099-B statement shows federal income tax withheld in box 4" | One Form 1099-B statement (the statement entity and tax year) | The filer's answer for that statement. Line 25b requires one for the statement of every current Form 1099-B sale | Correction by free supersession. A sale on a statement with no answer blocks line 25b and asks (`t2_s2`, `t2c_s1`, `b4_two_statements_one_unanswered`, `b47_unanswered`). A later sale on an answered statement does not change the proposition, which is about the statement, and computes (`t2_same_statement`, `b4_same_statement_two_sales`). An answer for a statement with no sale is not read (`m_empty_box4_yes_no_sale`: 34,250 / 3,875, refund 625) |
| `f1099b.statement-box7-loss-not-allowed` (`statement_box7`) | "Box 7 is checked for a sale on this statement" | One statement | As above; read by Schedule D line 16 | As above: `t3_s2`, `b7_two_statements_one_unanswered`, `b47_unanswered` ask; `b7_yes_*` and `t3_s3_yes` refuse |
| The decided return-level `f1099b.box4-withholding-reported` and `box7-loss-not-allowed` | "Any Form 1099-B shows ..." | The return (tax year) | The answer | **Not invalidated by a later sale from a new statement**: the counterexample (`t2_s2`, `t2c_s1`, `t3_s2` on `decided`). In the final design no rule reads these two facts (artifact 6 surface: no consumer) |
| Exception 1: `exception1.only-box2a-capital-gains`, `exception1.no-capital-losses` and the derived `schedule-d-required.conclusion` (all v81) | Exception 1 holds: the only capital gains are box 2a distributions, and there are no capital losses | The return | The filer's answers | Correction. Line 16 v7, line 7a v9 and the preferential base v10 read the conclusion only when every sale count is zero. A sale recorded after a "yes" makes it false but leaves it unread (`t1_s2` in base mode: TI 38,250, tax 3,875). All four polarities beside one sale on each of five families compute the same return (`p_*`, 20 cases). A "no" with nothing recorded refuses the return. That includes a "no" left standing after the only sale is removed (`t4_s1_removed`), identically on v81 |
| `schedule-d-boundary.*` answers, Q1-Q3 and the in-class answers | Unchanged v81 facts | — | — | Unchanged: lifecycle as recorded in f8949-code-b Track 0. Their staleness is exercised again here (`t1_s1`, `t2_s1`, `t5_s1`, `n_box_e_q1_no`, `n_box_c_q2_no`, `n_code_b_q3_no`) |

## 2. Empty/nonempty authority matrix

**PASS.** The families are the covered direct (lines 1a and 8a), code W (1b
and 8b), box B/E (2 and 9), box C/F (3 and 10) and code B (1b and 8b)
families, together with the new per-statement answers and Exception 1. Rows
are `final`, and are identical in both modes unless noted. On every
"Blocked" or "Refused" row, Form 1040 lines 16, 34 and 37 do not all
publish. A box 4 refusal blocks lines 25b, 34 and 37 and leaves TI and the
tax published.

| Case | Family state | Answers | Expected | Lines 7a / TI / tax / 25b / 34; attachments |
| --- | --- | --- | --- | --- |
| `m_empty`, `t1_s0` | Every family closed empty | Q1-Q3 no, base Exception 1 | Explicit zero; tax on the Exception 1 route | 0 / 34,250 / 3,875 / 0 / 625; gi / gi. v81 identical |
| `m_empty_q1_unanswered`, `_q2_`, `_q3_` | One grouped family's authority missing | That question unanswered | Blocked, asks that question | B; the counts block `SOURCE_SET_UNCLOSED`. Line 16, 24, 25b (Q1, Q3; line 25b reads only the Form 1099-B counts), 33, 34, 37 and 7a ask "Did you sell any securities whose basis was not reported to the IRS?" (Q1), and the Q2 and Q3 forms |
| `m_empty_covered_unclosed`, `m_empty_w_unclosed` | A per-family literal closure missing | — | Blocked, asks the family's closure | B; asks "Have you recorded every covered short-term sale ...?" |
| `m_empty_box4_yes_no_sale` | No Form 1099-B sale; a box 4 "yes" stands for a statement with no sale | — | Not read | 0 / 34,250 / 3,875 / 0 / 625 |
| `m_empty_exc1_only2a_no`, `m_empty_exc1_nolosses_no` | Closed empty; Exception 1 answered not to hold | A false Exception 1 answer | Refused | 7a B, TI B, tax gi, 25b 0, 34 B; the base `inapplicable`. **Identical on v81 and decided** |
| `m_2a_only` | Closed empty, 1,000 box 2a | Exception 1 holds | Computed on the Exception 1 route | 1,000 / 35,250 / 3,875 / 0 / 625; base 1,000 (line 13); gi / gi |
| `m_2a_only_exc1_only2a_no` | Same | "Only box 2a" no (false) | Refused | 7a B, tax gi. Identical on v81 |
| `m_2a_box_f_loss` | Box F 0 / 500 beside 1,000 box 2a | Q2 yes, IC80 yes, Exception 1 honest | Computed on the Schedule D route | 500 / 34,750 / 3,875 / 0 / 625; base 500 = min(line 15 500, line 16 500); pub / pub |
| P0 `f_*` (10 controls), `f_two_unrelated_covered`, `n_covered_two_sales`, `n_w_two_sales`, P0 `c1`-`c4`, `d2`-`d5` | Nonempty, eligible, on every family and term, including zero, 0/0, equal and fully disallowed sales | Honest | Computed | The hand value in every case. For example `f_noncovered_lt` 4,000 / 38,250 / 3,875 / 0 / 625, and P0 `c4` box C 0/0: 0 / 34,250 / 3,875 with pub / pub |
| `p_{covered_st,noncovered_lt,no1099b_st,w_lt,codeb_st}_only2a_{yes,no}_nolosses_{yes,no}` | Nonempty, one sale | **Exception 1 in all four polarities** | Computed, identically in every polarity | covered 3,000 / 37,250 / 4,235 / 0 / 265; box E 4,000 / 38,250 / 3,875 / 0 / 625; box C −500 / 33,750 / 3,815 / 0 / 685; code W LT −700 / 33,550 / 3,791 / 0 / 709; code B 6,000 / 40,250 / 4,595, owes 95. Decided identical |
| `n_box_e_q1_no`, `n_box_c_q2_no`, `n_code_b_q3_no` | Nonempty; the grouped answer "no" | Q1, Q2 or Q3 no | Blocked, asks it | B |
| P0 `a1`-`a3`, `d6`-`d8`; `n_covered_lt_says_short`, `n_w_lt_says_short`, `n_covered_lt_box1g`, `n_w_proceeds_row_disagrees`, `n_w_adjustment_row_missing`, `n_covered_basis_row_missing`, `n_covered_two_sales_one_*` | Nonempty, ineligible (term, box 1g, rows) | Honest | Refused: **blocked** is the choice | B; the family's admission check pinned (artifact 1) |
| `b4_yes_{covered,w,noncovered,codeb}`, `b4_two_statements_one_yes` | Nonempty; a statement shows box 4 | Box 4 yes | Refused at line 25b only | TI and tax publish (covered 37,250 / 4,235; box E 38,250 / 3,875; code W LT 33,550 / 3,791; code B 40,250 / 4,595). 25b, 34, 37 B; `form1040-line25b (blocked, DEPENDENCY_ABSENT, [])` |
| `b7_yes_{covered,w,noncovered,codeb}`, `b7_yes_gain` | Nonempty; a statement's box 7 checked | Box 7 yes | Refused from Schedule D line 16 on | Schedule D line 16, 7a, TI, tax, 34, 37 B; `schedule-d-line16 (blocked, DEPENDENCY_ABSENT, [])` |
| `b4_two_statements_one_unanswered`, `b7_two_statements_one_unanswered`, `b47_unanswered` | Nonempty; a statement's answer missing | — | Blocked, asks per statement | B; asks the box 4 or box 7 question |
| `b4_box_c_only` | Box C only (no Form 1099-B) | — | Neither box question read | 1,500 / 35,750 / 4,055 / 0 / 445; pub / pub |

The neighbouring result: on every closed-empty, fully answered row it is the
v81 result (artifact 5). A family that does not read the sale families
still computes beside a refused return, as before. For example, beside a
box 4 refusal the tax and TI publish.

## 3. Late-member trace

**PASS** on `final`. Each stage is a fresh `live_coordinate_run` over the
act log at that point. Answers are added by supersession, never edited in
place. A member recorded "after" an answer follows it in the act log.

**T1 (the charter's D1 trace): a wage return computes; add a box E sale;
recompute through the Schedule D route** (`t1_s0` to `t1_s2`, on `final`,
`decided` and v81)

| Stage | Change | Result | What became unusable, and why |
| --- | --- | --- | --- |
| 0 | Wage return; Q1-Q3 no | 0 / 34,250 / 3,875 / 0 / 625; gi / gi. The same on all three cores | — |
| 1 | A box E sale, 6,000 / 2,000, recorded after the Q1 no | Form 1040 blocks and asks Q1. The `noncovered-lt` count blocks `SOURCE_SET_UNCLOSED`. Line 16 v7, line 7a v9, the base v10 and line 25b v6 name the count | The Q1 no is stale: a member followed it. Stage 0's zero lines 2 and 9, the count, and every line built on them are not reproduced |
| 2 | Q1 yes, IC79 yes, Form 8949 no, Path B no; in honest mode Exception 1 "only box 2a" no | 4,000 / 38,250 / 3,875 / 0 / 625; line 9 4,000; base 4,000; pub / pub. Through the Schedule D route, in both modes. **On v81 in honest mode line 16 is `gi`**, and lines 34 and 37 block (D1). In base mode v81 is right | The stage 0 Exception 1 conclusion is no longer read: a sale count is above zero |

**T2 (the charter's box 4 trace): a box 4 "no", then a sale whose statement
has box 4 withholding** (`t2_s0` to `t2_s3_no`, `t2_same_statement`,
`t2c_s1`)

| Stage | Change | Result on `final` | On `decided` | What became unusable, and why |
| --- | --- | --- | --- | --- |
| 0 | Box E sale on statement A, 6,000 / 2,000; box 4 and box 7 no | 4,000 / 38,250 / 3,875 / 0 / 625 | the same | — |
| 1 | A box E sale on new statement B, 3,000 / 1,000, after the answers; B shows 1,440 in box 4 | Blocked; asks Q1 | the same | Q1 yes is stale (a later member) |
| 2 | Q1 yes again | **Blocked.** Line 25b `(blocked, DEPENDENCY_ABSENT, [f1099b.statement-box4-withholding-reported])`, asks the box 4 question. Schedule D line 16 asks the box 7 question for B | **Publishes line 25b 0, refund 625: the counterexample.** The true line 25b is 1,440 | On `final`, the statement set grew: B has no answer, so the line cannot rest on A's. On `decided`, the single "no" stays current although the statements it summarizes changed |
| 3 | B box 4 yes | Line 25b refused, and box 7 is still asked for B | Line 25b refused | — |
| 3' | B box 4 no, box 7 no (the variant where B has no withholding) | 6,000 / 40,250 / 3,875 / 0 / 625 | the same | — |
| 2'' | `t2_same_statement`: the second sale is on statement A | Computes, 6,000 / 40,250 / 3,875, with no new question | the same | Nothing: A's answer is about statement A, which did not change |
| 1c | `t2c_s1`: the same on line 1a (a second covered sale on new statement B; the literal closure is re-closed, so no grouped question goes stale) | Blocked; asks box 4 and box 7 for B | **Publishes TI 41,250, tax 4,715, owes 215, without the 1,440** | As stage 2 |

**T3: the box 7 analogue** (`t3_s0`, `t3_s2`, `t3_s3_yes`). Stage 0 is a box
E gain on statement A with box 7 no: 4,000 / 38,250 / 3,875. Stage 2 adds a
loss of 3,000 / 5,000 on new statement B, with box 7 checked, and re-answers
Q1. On `final` Schedule D line 16 blocks with
`(blocked, DEPENDENCY_ABSENT, [f1099b.statement-box7-loss-not-allowed])` and
asks. On `decided` it publishes line 16 2,000 and TI 36,250, which is the
counterexample. Stage 3 answers B yes and the return is refused.

**T4: Exception 1 and a removed sale** (`t4_s0`, `t4_s1_removed`, on all
three cores). Stage 0 is a line 1a sale, 10,000 / 7,000, answered honestly:
3,000 / 37,250 / 4,235, owes 0, refund 265. Stage 1 removes the sale and its
rows, which closes line 1a again at a new horizon.

- In base mode the return is the wage return again on every core.
- In honest mode the "only box 2a" no is still current with nothing
  recorded, and line 16 is `gi` on all three cores.

A removal says the sale was recorded in error. The real-world proposition
was then "only box 2a gains" all along, and the standing "no" is a false
answer. It refuses, and no number publishes. Nothing on the page asks for
the answer to change (owner question 2).

**T5: a box C sale for 0 with basis 0, after Q2 no** (`t5_s1`, `t5_s2`, on
all three cores). Stage 1 blocks and asks Q2. Stage 2 (Q2 yes and the
in-class answers) gives 0 / 34,250 / 3,875, with both attachments published
(`no1099b_count`). On v81 the honest mode blocks line 16 (D1), and base
mode publishes with neither attachment required (D3).

**The other aggregate declarations.**

- The sale counts and the admission and amounts checks are derived. They
  are recomputed from current rows on every run and hold no state a later
  member could leave stale.
- The Exception 1 conclusion is an aggregate over all capital activity.
  Once a sale is recorded it is not read (T1 stage 2 in base mode, the `p_*`
  cases).

## 4. Claim reuse

**PASS.** Five claims are reused. Three are not.

| Claim | Same real-world proposition | Same identity and lifecycle | Same scope and explanation |
| --- | --- | --- | --- |
| Line 16's Exception 1 path: `schedule-d-required.conclusion` "no" (v81 rule, unchanged) | Yes: Exception 1 holds and the tax is figured without Schedule D | Yes: the same derived fact from the same two answers, keyed by tax year, free supersession | **Narrowed, not broadened.** v6 read it on every return without covered proceeds. v7 reads it only when all ten sale counts are zero, which is the only state in which Exception 1 can be true of the recorded sales. Evidence: `m_empty` and `m_2a_only` use the path (tax 3,875); the 20 `p_*` cases show it is not read beside a sale; and the refusal on a false "no" is identical to v81 (`m_empty_exc1_*`) |
| The preferential base's Exception 1 arm (line 13 alone), v10 | Yes: with no Schedule D, the base is the box 2a distributions | Yes, unchanged | Narrowed in the same way: read only when every count is zero. `m_2a_only` base 1,000. Beside a sale the base is min(line 15, line 16): `m_2a_box_f_loss` 500, P0 `c3` 500 (v81 base mode: 1,000, D2) |
| Line 25b's five document withholding subtotals (1099-INT, 1099-DIV, 1099-R, 1099-G, SSA-1099), v5 → v6 | Yes: the value arm is v5's sum, unchanged | Yes: the same subtotal rules and pins | Yes. v6 adds a block arm and a `require_paired` before it. It never changes the sum. On every return that records no Form 1099-B sale, line 25b is v5's value (the 134 identical returns, `b4_box_c_only`) |
| The eight Form 1099-B sale counts (v81 rules) | Yes: the number of current sales on a family | Yes: the same rules, family closure and horizon | Read by line 16, line 7a, the base, line 25b and Schedule D line 16 only through "count > 0", never as an amount. The attachments read them as before |
| The code W, box B/E, box C/F and code B families, and their closures and questions | Yes, unchanged | Yes, unchanged | Yes. Only the covered and code W admission rules change, and they read fields of the same sale (P0 `f_*` unchanged) |
| The box C and box F counts | **Not reused.** New rules on the v80 families, copied in shape from the v81 code B counts | — | — |
| The per-statement box 4 and box 7 answers | **Not reused.** New facts | — | — |
| The admission vocabulary v2 values `term-mismatch`, `needs-form-8949`, `amounts-disagree` | **Not reused.** New values in a successor bundle. The rule shows none of them (Decision 7 limit); each blocks its admission check `DEPENDENCY_INVALID` | — | — |

## 5. Neighbouring-capability dependency diff

**PASS.**

**Prerequisites before and after** (the final v82 rules, read from
`requires` and the expressions):

| Neighbour | v81 | Final v82 adds | Justified by the neighbour's own meaning |
| --- | --- | --- | --- |
| Form 1040 line 16 (v6 → v7) | TI, filing status, qualified dividends, the base, covered proceeds, the worksheet; `schedule-d-required.conclusion` on the Exception 1 path | The ten sale counts | Whether any sale is recorded decides whether the tax is figured with Schedule D (Exception 1, `i1040gi` line 7a). It costs nothing new: TI already waits on line 7a, which waits on every Schedule D line and so on every closure (`t1_s1` on v81 blocks line 16 the same way) |
| Line 7a (v8 → v9), preferential base (v9 → v10) | Schedule D lines, line 13, Exception 1 | The ten sale counts | The same: a recorded sale makes the return a Schedule D return. Every count reads only closures these lines already needed through Schedule D lines 1a-10 |
| Line 25b (v5 → v6) | The five withholding subtotals and their closures | The eight Form 1099-B counts. With a Form 1099-B sale recorded, a box 4 answer for each of its statements | Box 4 withholding belongs on line 25b, so line 25b must know whether any Form 1099-B exists. With no Form 1099-B sale nothing new is read (`m_empty_box4_yes_no_sale`). It blocks while a sale family is unclosed (Decision 5, accepted) |
| Schedule D line 16 (v2 → v3) | Lines 7 and 15 | The eight counts, and a box 7 answer per statement when a Form 1099-B sale is recorded | Box 7 disallows a loss that would reach line 16. The counts are already needed through lines 7 and 15 |
| Form 8949 and Schedule D attachments (v5 → v6, v9 → v10) | Each family's subtotals and counts | The box C and box F counts | Form 8949 reports every sale (`i8949`), including one for 0 with basis 0 |
| Lines 1a, 8a, 1b, 8b (producers unchanged; fields v4, v3, v4, v4) | The admission checks v1 | The checks v2 read `long_term`, box 1g (direct only) and each sale's own rows, and require them (`paired_rows`) | Each line sums that family's sales, which must be of its term and its reporting method, with rows that are the sale's own (Decision 3) |
| Line 9 (EIC investment income), the Social Security worksheet (they read line 7a) | Line 7a | Through line 7a, the counts | As line 7a. They are unchanged on all 134 identical returns |

**The return state with no sale** (the wage return, `m_empty`, `t1_s0`, and
the no-sale returns among the 213): the same answers as v81. No box question
is read, and no new answer is asked. With all ten counts at zero, line 16
takes the v81 Exception 1 path.

**All 213 pinned v81 returns, before and after** (`track0-rerun-output.json`):

- The harness's v81 run matches the committed table
  (`tests/fixtures/code_b_sales_v81/expected.json`) on every line and
  attachment: 0 mismatches.
- Each return runs on v81; on `final` with every recorded statement's box 4
  and box 7 answered no; on `final` with them unanswered; and on `final`
  without `paired_rows`.
- `classify` compares every watched line, attachment disposition, page
  question, and the untruncated (disposition, code, missing) of every
  watched publisher. It labels each change by the decided fix that explains
  it, or `UNCLASSIFIED`.

| Class | Returns | What changes |
| --- | --- | --- |
| Identical | 134 | Nothing |
| D3 `paired_rows` (Decision 3, accepted) | 51 | The earlier harnesses record a direct or code W sale's rows under other transaction entities. The admission check refuses each sale as having no rows of its own. Lines change only from a number to blocked; rebuilt without `paired_rows` all 51 are identical |
| D3 and D5 | 6 | As above, plus the class below |
| D5: line 25b waits on an unclosed family (Decision 5, accepted) | 17 | Form 1040 was already blocked on v81. Line 25b changes from 0 to blocked, waiting on a Form 1099-B count; line 33's `missing` grows by line 25d. No other line changes |
| D1 `no1099b_count`: a count row on an unclosed family | 5 | A blocked box C or F count row, and attachment `missing` lists that name it. No line, attachment disposition or question changes |
| **UNCLASSIFIED** | **0** | — |

Further results:

- **No return publishes a different number** (`numbers_changed` is empty
  for every return, and between the builds with and without `paired_rows`).
- All 79 changed returns change exactly as P0 recorded for the decided v82
  (`same_as_p0_decided` 79). The repairs change no v81 return.
- With the box questions unanswered, 7 returns still publish Form 1040. None
  of them records a Form 1099-B sale (`unanswered_publishing_1040_with_a_1099b_sale`
  is empty): they are the no-sale and box C / F returns, for which nothing
  is asked. Of the 174 that record a Form 1099-B sale, 150 ask the box
  questions; the other 24 block first on an unclosed sale family, whose
  question the page asks instead.
- Every publisher records exactly one row in every run, and every model is
  valid (`rows_not_one` 0, `invalid_models` 0).

**Earlier cores are untouched.** v82 replaces members only in its own
package, and the build writes only new files.

**Inherited behaviour, unchanged.** v81's refusal of a false Exception 1
"no" with nothing recorded (`m_empty_exc1_*`, `t4_s1_removed`) is identical
on v81, `decided` and `final`. This design does not touch it, so it is not
a counterexample to this row. Owner question 2 asks whether Track 1's
rewording (Decision 2) should also make the page ask.

## 6. Integration surface

**PASS.** The bindings come from the final v82 package (`surface`, 974 of
974 members resolved). The cardinality is measured in every saturated run:
286 on `final`, 130 on `decided`, 20 on v81, and every run of the rerun. In
each run, each of the 45 watched publishers (43 on v81) records exactly one
disposition row, on the published, zero, blocked, refused, inapplicable and
guard-false paths.

| Consumer | Binding | Cardinality expected | Satisfied |
| --- | --- | --- | --- |
| Form 1040 line 16 | `rule.form1040-line16` v7 publishes `tax.total-tax`; field `form1040.line-16` v3. Read by `form1040-tax-after-credits` v2, `ctc-worksheet-a.line-1` and `schedule3-line1-direct-ftc` v5 | Exactly one | Yes |
| Line 24 | `rule.form1040-line24` v1 (`tax.line24-total-tax`), field v1; read by lines 34 and 37 | Exactly one | Yes |
| Line 25b | `rule.form1040-line25b` v6 (`payments.line25b`), field v4; read by line 25d | Exactly one | Yes |
| Lines 33, 34, 37 | `rule.form1040-line33`, `-line34`, `-line37` v1; fields v1. Line 33 is read by 34 and 37; line 34 by 35a and 36 | Exactly one each | Yes |
| Line 7a | `rule.form1040-line7a` v9 (`capital-gains.line7a-total`), field v2. Read by `form1040-line9` v8, `eic-investment-income` v2, `ss-benefits-worksheet` v4 | Exactly one | Yes |
| Preferential base | `rule.selected-preferential-base` v10. Read by line 16 v7, line 7a v9 and `qdcg-worksheet.line-4` and `line-5` | Exactly one | Yes |
| Schedule D line 16 | `rule.schedule-d-line16` v3, field v3. Read by line 21, line 7a and the base | Exactly one | Yes |
| Form 8949 attachment | `rule.attachment.f8949` v6 (`form8949.disposition`), presentation `attachments` | Exactly one per return | Yes: on `final` published 142, blocked 92, inapplicable 52 |
| Schedule D attachment | `rule.attachment.schedule-d` v10 (`schedule-d.disposition`) | Exactly one per return | Yes: on `final` published 174, blocked 96, inapplicable 16 |
| Box C / F counts | `rule.f8949-no1099b-{st,lt}-count` v1. Read by both attachments, line 16, line 7a and the base | Exactly one | Yes |
| Covered and code W admission checks | `rule.f1099b.{covered,covered-w}-{st,lt}-txn.admission-check` v2. Read by lines 1a, 8a (and Form 8949), 1b and 8b | Exactly one | Yes |
| Per-statement box 4 / box 7 answers | `f1099b.statement-boxes.vocabulary` v1; `input-question.f1099b-statement-box{4,7}-*` v1. Read only by line 25b v6 and Schedule D line 16 v3. The return-level box 4 and box 7 facts have no consumer | Any number (one per statement) | Yes: `require_paired` needs at least one per recorded statement, and `collect_categorical_all_equal` reads all of them |

**One built model per disposition path** (all on `final`):

| Consumer | Path | Model | Pinned (disposition, code, missing) |
| --- | --- | --- | --- |
| Line 16 | Published, Exception 1 route | `m_empty`, `m_2a_only` | published 3,875 |
| | Published, Schedule D route (D1) | `t1_s2`, every `p_*` and `f_*` case | published |
| | Blocked, asks a family question | `m_empty_q1_unanswered`, `t1_s1` | `(blocked, DEPENDENCY_ABSENT, [..., f1099b.noncovered-lt-count])`; asks Q1 |
| | Blocked by a refused sale | P0 `a1`, `n_*` refusals, `b7_yes_*` | blocked behind TI |
| | Refused by a false Exception 1 answer | `m_empty_exc1_*` | `(inapplicable, -, [])`, as on v81 |
| Line 25b | Computed (the v5 value, 0 on the harness) | `m_empty`, `f_*`, `t2_s3_no` | `computed_zero`. Published and computed zero are the same unchanged value arm |
| | Blocked, an unanswered statement | `t2_s2`, `t2c_s1`, `b4_two_statements_one_unanswered` | `(blocked, DEPENDENCY_ABSENT, [f1099b.statement-box4-withholding-reported])`; asks the box 4 question |
| | Refused, box 4 yes | `b4_yes_*`, `t2_s3_yes` | `(blocked, DEPENDENCY_ABSENT, [])`; the field v4 sentence names box 4 |
| | Blocked, an unclosed Form 1099-B family | `m_empty_q1_unanswered`, the 23 D5 returns | `(blocked, DEPENDENCY_ABSENT, [the count])` |
| Lines 24, 33, 34, 37 | Published / blocked behind line 16 or 25b | as above | lines 34 and 37 block whenever line 16 or 25b does |
| Line 7a | Published positive, negative, zero, Exception 1 | `t1_s2` 4,000; `p_no1099b_*` −500; P0 `c2` 0; `m_2a_only` 1,000 | published |
| | Blocked | `m_empty_q1_unanswered`; `m_empty_exc1_*` | `(blocked, DEPENDENCY_ABSENT, [..., counts])` |
| Preferential base | min(line 15, line 16); line 13; zero; inapplicable | `m_2a_box_f_loss` 500; `m_2a_only` 1,000; `p_w_lt_*` 0; `m_empty_exc1_*` inapplicable | — |
| Schedule D line 16 | Published | every computing case | published |
| | Blocked, an unanswered statement | `t3_s2`, `b7_two_statements_one_unanswered` | `(blocked, DEPENDENCY_ABSENT, [f1099b.statement-box7-loss-not-allowed])`; asks the box 7 question |
| | Refused, box 7 yes | `b7_yes_*`, `t3_s3_yes` | `(blocked, DEPENDENCY_ABSENT, [])` |
| Form 8949 attachment | Published / inapplicable (direct only) / blocked | P0 `f_*` / `f_covered_*`, `m_empty` / every refusal | — |
| Schedule D attachment | Published, including box C 0/0 / inapplicable / blocked | P0 `c4`, `d3_no1099b_zero_zero`, `t5_s2` / `m_empty` / refusals | — |

**Precedent check.** The read copies `rule.sli-worksheet`. It reads plain
Form 1098-E answers keyed by a statement entity
(`f1098e.no-related-person-interest`: lender, statement, tax year) with
`collect_categorical_all_equal`, the operation added to read a per-statement
witness. The pairing copies line 25b v5's own `require_paired`, which pairs
each 1099 income row with a withholding row on its statement key. The
precedents had to satisfy one row per publisher per run, whatever the
number of answers, and that property is measured above.

Two properties neither precedent had to satisfy are measured here instead:

- **Pairing across eight fact types on one key.** The Form 1099-B answer
  pairs with the sale rows of eight fact types, not one family. Every Form
  1099-B sale object carries `statement` (broker, statement, transaction,
  tax year). `t2_same_statement` shows two sales on one statement joining
  one answer, and `t2c_s1` shows a covered sale on a new statement asking.
- **An answer with no row to pair.** A statement answered with no sale is
  never a failure (`m_empty_box4_yes_no_sale`).

**Presentation-model probe** (`field_sentences`; each case's reasons in
`field_reasons`):

| Field or question | Path (case) | What the page shows |
| --- | --- | --- |
| Line 25b v4 (changed) | blocked, unanswered statement (`t2_s2`) | The question "For each Form 1099-B or substitute statement you recorded a sale from, does it show federal income tax withheld in box 4?" |
| | refused, box 4 yes (`b4_yes_noncovered`) | No question (`block` carries no missing list). The sentence "... It is also blocked while a recorded Form 1099-B statement has no answer about box 4, and when a Form 1099-B shows federal income tax withheld in box 4: this return does not add Form 1099-B withholding yet." |
| | computed zero (`m_empty`) | "Form 1040 line 25b publishes a computed zero." |
| Schedule D line 16 v3 (changed) | blocked, unanswered (`t3_s2`); refused (`b7_yes_noncovered`) | The box 7 question: "For each Form 1099-B or substitute statement you recorded a sale from, is box 7 ("If checked, loss is not allowed based on amount in 1d") checked for any sale on it?" / the sentence "... and when box 7 (loss not allowed) is checked on a Form 1099-B: this return does not compute that sale." |
| Form 1040 line 16 v3 (changed, `field_words`) | blocked with no question attached | "Your tax has no value yet. It is waiting for your taxable income, your filing status, your qualified dividends and capital gain, or your covered sale proceeds. It also waits for your answers about each kind of sale, because whether you recorded any sale decides whether your tax is figured with Schedule D." With a single cause, the cause's question is shown instead (`m_empty_q1_unanswered`: Q1) |
| Line 7a v2 (changed, `field_words`) | blocked | "... It also waits for your answers about each kind of sale and for Schedule D, because any recorded sale puts line 7a on the Schedule D route." |
| Lines 1a v4, 8a v3, 1b v4, 8b v4 (changed) | blocked by an admission refusal (P0 `a1`, `n_covered_lt_says_short`, `n_w_proceeds_row_disagrees`) | The blocked sentence, which now names the new reasons: "A sale whose own proceeds, basis or wash-sale row is missing or differs from the sale, a sale that says it is of the other term, and a line 1a or 8a sale with a wash-sale loss disallowed in box 1g (record it as a code W sale) are also outside what this return computes." No question: which admission value fired is not shown (Decision 7 limit) |
| | blocked, a missing row (`n_covered_basis_row_missing`) | The same sentence. The covered rows have no input question in v81 |
| | `cbz` (`m_empty`), published (`f_covered_st`) | Unchanged v81 sentences |
| Both attachments (titles v6, v10) | published for box C 0/0 (P0 `c4`, `t5_s2`) | "Form 8949 attachment v6: the previous requirement, plus the box C and box F sale counts, so a box C or F sale for 0 with basis 0 requires it." The Schedule D form is the same |

## Presentation limits (not correctness)

Each of these returns is refused or blocked, and no Form 1040 tax or refund
publishes:

- a box 4 or box 7 "yes", or an admission refusal, shows the line's blocked
  sentence and no question, because `block` carries no missing list (the
  f8949-boxes-cf Decision 4 mechanism, extended by f8949-code-b Decision 7);
- a false Exception 1 "no" with nothing recorded leaves line 16
  inapplicable with no question (owner question 2).

Refused returns still publish the Schedule D lines that do not wait on the
refusing answer. A box 7 refusal (`b7_yes_noncovered`) blocks Schedule D
line 16 and everything after it, while lines 2 to 15 keep their recorded
column (h). That is the posture of the existing refusals (P0 `b4` and `b6`,
whose Schedule D lines 9 and 15 publish beside a blocked Form 1040). Owner
question 1 asks whether that posture is right for box 7.

## Owner questions

1. **Box 7 and the Schedule D part lines.** A box 7 "yes" blocks Schedule D
   line 16 on, but the sale's own line (for example line 9 at −2,000 in a
   loss case) still publishes its recorded column (h). The Form 1040 is
   refused, as for the existing collectibles and QOF refusals. Accept that
   posture? The alternative is to read the box 7 answer in each sale's own
   admission or amounts rule, so that the sale's family line blocks. That is
   about four more rule successors, all content.
2. **Exception 1 with nothing recorded.** A "no" to Exception 1 with no sale
   recorded refuses the return (line 16 inapplicable), and the page asks
   nothing. This includes a "no" left standing after the only sale is
   removed. It is unchanged from v81. Should the Track 1 rewording (Decision
   2) also give line 16 a question in this state, or is the refusal enough?
3. **Box 7 on a gain.** A statement whose box 7 is checked is refused even
   when its sales are gains, which box 7 does not affect (`b7_yes_gain`).
   This is an over-refusal, never a wrong number. Accept it, or read box 7
   only beside a loss?
4. **Per-statement questions.** The repairs ask box 4 and box 7 once for each
   recorded Form 1099-B statement, not once per return. Unanswered, 150 of
   the 174 pinned v81 returns that record a Form 1099-B sale ask them; the
   other 24 block first on an unclosed sale family, and none publishes Form
   1040. Accept this shape for Track 1?

## Track 1 addendum: the Exception 1 questions (Decision 2)

Track 1 adds a fourth switch to `prototype.REPAIRS`, `exception1_words`. On
v81 the four Exception 1 input questions share one sentence, "Besides
capital gain distributions in box 2a of Form 1099-DIV, did you have any
other capital gain or loss in 2025 ...?". Its "yes" means each fact's "no".
The repair replaces the four `input-question.exception1-*` citizens with v2
successors. Each asks its own fact, and its "yes" is the fact's "yes":

| Fact | v2 question |
| --- | --- |
| `exception1.only-box2a-capital-gains` | "Is it true that you had no capital gains in 2025 other than capital gain distributions in box 2a of Form 1099-DIV (for example, no gain from selling stock, funds or other property)?" |
| `exception1.no-capital-losses` | "Is it true that you had no capital losses in 2025 (for example, no loss from selling stock, funds or other property)?" |
| `exception1.no-qof-deferral` | "Is it true that you did not defer any capital gain in 2025 by investing in a qualified opportunity fund?" |
| `exception1.no-boxes-2b-2c-2d` | "Is it true that none of your 2025 Forms 1099-DIV or substitute statements shows an amount in box 2b, 2c or 2d?" |

The facts, rules and values are unchanged. The final scratch v82 now has 33
member edits (5 adds, 28 replacements), with no inherited inconsistency.

Rerun on the final design with the repair:

- **Cases.** The stored result of each of the 296 earlier runs is
  unchanged. One case is new,
  `m_empty_exc1_unanswered`: every family is closed empty and no Exception 1
  answer is recorded. In both modes it blocks, and Form 1040 lines 16, 24,
  33, 34 and 37 each list the four v2 questions. Final totals: 122 right,
  158 correctly blocked, 8 observed, 10 rejected at entry, and none wrong.
- **The 213 v81 returns.** `track0-rerun-output.json` is byte-identical:
  134 identical, 51 D3, 6 D3 + D5, 17 D5 and 5 D1, with 0 unclassified and
  no published number changed. No pinned v81 return shows an Exception 1
  question, so the rewording changes none of them. The v81 runs were taken
  from the earlier Track 0 raw runs of the same act lists, because v81 did
  not change. The three v82 variants were rerun.
- `track0.py rerun` now resumes from its raw file (`[max]` runs at a time).
  `cases` now merges the design summaries and field sentences of a partial
  run instead of overwriting them.

## Review repair addendum

The fresh-reader review (`docs/reviews/sale-family-audit/review.md`) found
two blocking defects in the published v82. Each repair is a switch in
`prototype.REPAIRS`, rerun here on the final design before it reached
`packages/`. `track0.py` builds a third design, `track1`: the v82 Track 1
published, which is final without the review repairs. It shows each defect
on the cases that witness it.

### F1: `row_needs_sale`

`paired_rows` requires every covered and code W sale to have its own rows.
A row with no sale of its own was never checked. It was summed on its line
beside an admitted sale, or alone, or after its sale was removed. The
repair adds a presence pair from each covered and code W proceeds, basis
and column (g) row to its sale on the same identity. The noncovered,
no-1099-B and code B rows have had these pairs since v79 to v81. The pairs
are a loader entry (`presence_pairs` in `prototype.py`, which
`audit_harness.loader_entries` applies per run). No content changes, and
the final scratch v82 still has 33 member edits.

Eight new cases (group R, honest mode, final and `track1`):

| Case | `track1` (by hand) | final |
| --- | --- | --- |
| `r_f1_covered_extra_rows`: a line 1a sale 10,000 / 7,000, plus 5,000 / 1,000 rows on another transaction | line 1a 7,000, tax 4,715, owes 215 (right: 3,000, 4,235, refund 265): wrong | refused at entry |
| `r_f1_covered_rows_alone`: the rows, no sale | line 1a 4,000, tax 4,355 (right: 0, 3,875): wrong | refused at entry |
| `r_f1_covered_lt_rows_alone`: the rows on line 8a, no sale | line 8a 4,000, line 7a 4,000: wrong | refused at entry |
| `r_f1_w_extra_rows`: a code W sale 4,000 / 5,000 (W 300), plus 5,000 / 1,000 rows | line 1b 3,300, tax 4,271 (right: -700): wrong | refused at entry |
| `r_f1_covered_sale_removed`: the sale removed, its rows left | line 1a 3,000, tax 4,235 (right: 0, 3,875): wrong | refused at entry |
| `r_f1_w_adjustment_row_alone`: a code W column (g) row, no sale | - | refused at entry |
| `r_f1_covered_sale_removed_after_basis_row`: the basis row removed, then the sale | - | the run refuses (see below) |
| `r_f1_covered_sale_and_rows_removed`: the rows removed, then the sale | - | right (tax 3,875) |

Every refusal names the row and its missing sale: "companion presence
violated: ...covered-st-txn.proceeds|broker=...,transaction=... is current
(5000) but ...covered-st-txn|... has no current value". The case checks the
words (`rejects`).

One shape is refused later than the others. In
`r_f1_covered_sale_removed_after_basis_row` the basis row is removed, then
the sale. When a sale is touched, the kernel's reverse presence check reads
only one row per sale: the last pair the loader declares, which is the basis
row. That row is gone, so the sale's removal is admitted, and the proceeds
row is left. The run then refuses with "companion provenance missing for
...covered-st-txn.proceeds|...". Nothing publishes. The noncovered,
no-1099-B and code B pairs behave the same way. The scratch core must
declare the pairs in the loader's order to show this (the first rerun
sorted them, which made proceeds the last pair, so it refused at entry).
Fixing the kernel's reverse check is outside this milestone.

- **Cases.** The 298 earlier final runs are unchanged. Final totals: 123
  right, 158 correctly blocked, 8 observed, 17 rejected at entry, none
  wrong.
- **The 213 v81 returns, as their harnesses record them**
  (`track0-rerun-output.json`, rerun in full): 129 identical, 63 refused at
  entry by `row_needs_sale`, 15 D5, 5 D1 and 1 D3 (`a_duplicate_on_direct`,
  a direct sale with no rows). No published number changed and none is
  unclassified. The 63 are 56 of the 57 returns whose builder puts a sale's
  rows on other transactions, and 7 (`t2_stage1` to `t2_stage4`, `t3_stage1`
  to `t3_stage3`) whose builder corrects a sale by removing the sale before
  its rows. On v82 that removal leaves rows with no sale for one act, so it
  is refused.
- **The 213 v81 returns as the live test corrects them.** Decision 3
  already moves each row onto its own sale's transaction (`own_rows`). The
  live test now also removes a direct or code W sale after its rows
  (`rows_removed_first`). Each corrected return was run on v81 and on the
  published v82 with the new loader entry. Every v81 run equals the
  committed v81 table, and every v82 run equals the committed v82 table.
  F1 changes no corrected v81 return.

### F2: `line7b_activity`

Form 1040 line 7b v1 checks "Schedule D not required" whenever the
Schedule-D-required conclusion is no, and the Exception 1 answers decide
that conclusion. Since `tax_activity` the tax does not read those answers
once a sale is recorded. So a filer whose only sale nets zero, and who
answers the v2 questions truthfully ("yes": no capital gain other than box
2a, no capital loss), got line 7b checked beside a required Schedule D. A
recorded sale is reported on Form 8949 or Schedule D, so Exception 1 does
not apply.

The repair is line 7b v2 (rule) and its field v3. The rule reads the same
ten sale counts and two covered proceeds subtotals as line 16 v7, and is
`guard_inapplicable` when any is above zero. The conclusion decides line 7b
only when no sale is recorded. Like line 16, it waits while a sale family is
unclosed. The field's three sentences say so. The final scratch v82 has 35
member edits (5 adds, 30 replacements).

The harness now watches line 7b (`audit_harness.WATCH`, `probe.KEPT_LINES`,
`PROBED_FIELDS`). The hand values say that line 7b is `published_categorical`
(checked) exactly when Schedule D is not required, and `guard_inapplicable`
otherwise. `tables.py` adds line 7b to the consumers and to the route
readers, so a sale count that line 7b does not read fails the audit. On v81
the audit now fails 46 times: the 38 failures before, plus the 8 Form
1099-B counts that line 7b does not read.

Four new cases (group R, honest mode, final and `track1`). Each leaves the
Exception 1 facts at the harness base ("yes"):

| Case | `track1` | final |
| --- | --- | --- |
| `r_f2_box_c_zero`: a box C sale 0 / 0 | line 7b checked beside both attachments: wrong | line 7b not checked; tax 3,875 |
| `r_f2_covered_zero_net_beside_2a`: a line 1a sale 5,000 / 5,000 and a 1,000 box 2a distribution | line 7b checked beside Schedule D: wrong | right: line 16 1,000, base 1,000, TI 35,250, tax 3,875, line 7b not checked |
| `r_f2_box_e_zero_net_beside_2a`: the same on box E | wrong, as above | right, with Form 8949 |
| `r_f2_box_e_gain_base_answers`: a box E gain, Exception 1 facts yes (false) | line 7b checked: wrong | right: tax unchanged, line 7b not checked |

- **Cases.** Every final run was rerun. Apart from the line 7b line and its
  field sentence, every earlier final run is unchanged. Line 7b on the final
  runs: not checked in 259, checked in 10 (no sale and Exception 1 holding),
  blocked in 20 (every one beside a blocked line 16), and absent in 17
  (refused at entry). Final totals: 127 right, 158 correctly blocked, 8
  observed, 17 rejected at entry, none wrong. `track1`: the 9 review cases
  publish wrong (F1 and F2), as the review found.
- The decided and v81 runs are Track 0's, made before line 7b was watched.
  On those cores line 7b v1 is checked beside a sale under the base answers.
- **The v81 returns.** Line 7b changes are classified in the live test's
  regeneration (item 5): "F2 line 7b is not checked beside a required
  Schedule D" and "F2 line 7b waits on an unclosed family".
  `track0-rerun-output.json` is the F1 rerun above and does not watch line 7b.

### F3: `field_truth`

Two field sentences were not true of their rules' `when`. The repair
replaces each sentence in the unpublished v82 citizen. No version changes,
because neither field was published before v82.

- Form 1040 line 16 field v3, `guard_inapplicable`: "Line 16 is computed
  here only when you recorded a sale, or when Schedule D is not required and
  your qualified dividends and capital gain fit your capital gain
  distributions answer. Neither is true on this return." It used to say
  "when you sold covered securities", but line 16 v7 takes the Schedule D
  route for any recorded sale.
- Form 1040 line 7a field v2, `blocked`: "Line 7a has no value yet. Whether
  you recorded any sale decides its route, so it waits for your answers
  about each kind of sale. With a sale recorded, line 7a is the Schedule D
  amount and waits for Schedule D. With none, it waits for your Exception 1
  answers and for your box 2a capital gain distributions to be complete."
  It used to begin "because Exception-1 authority is incomplete or the
  box-2a family is unclosed", and line 7a v9 reads neither when a sale is
  recorded.

The cases that show these sentences (`t4_s1_removed`,
`m_empty_exc1_only2a_no` and `n_covered_lt_box1g`) were rerun on final.
Their verdicts and results are unchanged, and `field_sentences` holds the
new words.

### F4: the audit reaches amount rows and line 7b, and honest means the v2 words

- **Rows.** `tables.py` has a row table. Each amount row is a proceeds,
  basis or column (g) fact that is a sale family's member. The table names
  the sale the row's loader presence pair ties it to, or "unpaired". An
  unpaired row fails the audit (`row_audit`), because it is summed on its
  line whether or not its sale is recorded. On v82 all 28 rows are paired.
  On v81 the 10 covered and code W rows are unpaired, so the audit now fails
  56 times on v81. The docstring now says what the field table covers (the
  sale objects' fields) and what the row table covers.
- **Line 7b** is in the projection and the route readers (F2 above).
- **Honest answers.** Track 0's honest mode, and with it the live test,
  answered "only box 2a gains" with "no" whenever a sale was recorded. That
  was the v1 sense of the question. Honest answers now follow the v2
  questions read literally, from the recorded sales
  (`audit_harness.honest_exception1`). "No capital gains other than box 2a"
  is "no" only if some sale is a gain. "No capital losses" is "no" only if
  some sale is a loss. A sale that nets zero is neither. This changes the
  honest act lists of 56 cases: loss-only sales, zero-net sales and the
  duplicate pairs. Every final run was rerun, and not one result changed.
  That is Decision 1 again: beside a recorded sale, the Exception 1 answers
  are not read, and line 7b no longer reads them either.

### F5: the live test's cost

`tests/test_sale_family_audit_v82.py` made 694 coordinator runs per full
suite, and its table was 1.8 MB. Two sets of runs repeated runs the table
already pins:

- **The v81 honest reruns (198).** Each was asserted equal to the same
  return's recorded-answer run. They witnessed only Decision 1, which the 20
  `p_*` polarity cases witness through the coordinator. Each v81 return now
  runs once, with its recorded answers.
- **Base-answer Track 0 runs that repeat their honest run.** The live test
  now runs a case's base-answer mode only when Track 0 recorded a different
  final result for it (`repeats_honest`). That covers 5 of the 139 base runs:
  `t4_s1_removed`, the one case where the answer matters, plus `t2_s1`,
  `n_box_e_q1_no`, `n_box_c_q2_no` and `n_code_b_q3_no`, where a stale
  closure under the base answers leaves line 7b waiting, while under the
  honest answers line 7b is not checked. The other 134 are dropped.
  `test_every_track0_case_keeps_a_run_and_every_dropped_run_repeats_one`
  checks that every final-design case keeps a run and that every dropped run
  equals its honest run in `track0-output.json`.

The live test now runs 176 Track 0 runs (every final case, with the 12
review cases) and 213 v81 returns: 389 coordinator runs, down from 694. Its
table is 989,693 bytes, down from 1,761,186.

**The v81 returns on the published v82**, as the live test corrects them
(rows on their own sale's transaction, and a sale removed after its rows),
compared with their v81 runs:

| Class | Returns |
| --- | --- |
| identical | 16 |
| F2 line 7b is not checked beside a recorded sale | 168 |
| D5 line 25b waits on an unclosed family + F2 line 7b waits on an unclosed family | 18 |
| D5 + F2 line 7b is not checked beside a recorded sale | 5 |
| D1 a count row waits on an unclosed family + F2 line 7b waits on an unclosed family | 4 |
| D1 + F2 line 7b is not checked beside a recorded sale | 1 |
| D3 a direct or code W sale with no rows of its own + F2 line 7b is not checked beside a recorded sale | 1 |

None is unclassified, and no published number changes (2,035 numbers
compared with the v81 table). Before the review repairs, 184 were identical.
Of those, 168 now differ only because line 7b is no longer checked beside a
recorded sale. The earlier v81 harnesses kept the base Exception 1 answers
beside their sales, so v81 checks "Schedule D not required" on each of
them. In the F2 classes "waits on an unclosed family", the Form 1040 was
already blocked on v81. In one of them (`v80_q2_late_yes_stale`), the page
now also asks that family's question.

### Notes N1 to N5

- **N1, fixed.** `tables.NO_EFFECT` is keyed by (sale object, field). The box
  5 reason covers only `covered_security` on the four covered and code W
  objects. The same field on any other object fails the audit, and a test
  checks this.
- **N2, fixed for boxes 8 to 11.** `REFUSED_BY` names Form 1099-B boxes 8 to
  11 (section 1256 contracts, which go to Schedule D lines 4 and 11 through
  Form 6781) with the unasked `no-other-schedule-d-sources` answer that
  refuses them. Decision 5 accepted that answer as unasked. Box 13
  (bartering) is parked: it is not a sale reported on Schedule D, and this
  milestone has not established which answer refuses it.
- **N3, fixed in words.** The consumer table is transitive reach through
  `requires`. The `tables.py` docstring and a `consumers_are` field in
  `tables-v8x.json` now say that it shows what can block or change a
  consumer, not the line a sale is reported on.
- **N4, fixed** (`field_truth`). Only Schedule D lines 1a and 8a name the box
  1g refusal, and only lines 1b and 8b name a wash-sale row. The four
  fields are unpublished v82 citizens, rewritten in place. The cases that
  block these lines were rerun on final, with unchanged results, and
  `field_sentences` holds the new words.
- **N5, parked.** Decision 6 accepted the per-statement box 4 and box 7
  questions as asked once on the page, in "for each statement" words, with
  no statement named.
