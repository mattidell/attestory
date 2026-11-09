# Fresh-reader review: sale family audit (core v82)

Reviewer seat. Object: `milestone/sale-family-audit-2025` at `874707fb`,
diffed against `github/main` (18 commits ahead, 0 behind; draft PR #265
open, not merged). Charter: `docs/reviews/sale-family-audit/charter-review.md`.
I judged from the committed content, tests and evidence only, and made my own
coordinator runs on the published v82 (`live_coordinate_run` through the live
module's `run()` and the evidence harness's act builders, synthetic `demo.*`
findings, raw runs kept outside the repository). I did not read governance.

## Verdict

**Not ready.** Blocking: F1 and F2. Both reproduce on the published v82 with
the evidence harness's own builders, and both contradict the milestone's
scope claim that no sale family publishes a wrong return.

## Findings, by severity

### F1 (blocking): covered and code W rows with no sale of their own still reach lines 1a, 1b, 8a and 8b

- **Claim violated.** Plan, "P0 result", D6 and Decision 3: a row is refused
  when it is not tied to its sale. `audit.md` says "v82 refuses each row as
  having no sale".
- **Where.**
  - `packages/content/tax/2025/rule.f1099b.covered-st-txn.admission-check.v2.json:48-63`
    (and the three sibling admission checks v2). `require_paired` checks
    that every *sale* has a row with the same `transaction` key. Its
    evaluator (`packages/derivation/evaluator.py`, `_require_paired`) says
    "A withholding row with no income row is not a failure". A row with no
    sale is therefore never checked.
  - The `sales` path also turns on only when the sale family is nonempty.
    With rows and no sale, the `neither` default (line 107) gives 0.
  - `packages/tax/loader.py:479`: the v82 declaration carries presence pairs
    for noncovered, no-1099-B and code B rows, but none for covered or
    code W rows.
- **Reproduction** (published v82, honest answers, box 4 and box 7 "no").
  Build each case with `h.opened()` and `probe.S(...)`, then add rows with
  `h._member(acts, kind, term, "proceeds"|"basis", amount, tag)` under a new
  tag (a new broker, statement and transaction):

  | Case | Correct (by hand) | v82 publishes |
  | --- | --- | --- |
  | covered st sale 10,000/7,000 with its own rows, plus a proceeds row of 5,000 and a basis row of 1,000 on another transaction | refuse, or line 1a 3,000, tax 4,235, refund 265 | line 1a **7,000**, TI 41,250, tax **4,715**, owes **215** |
  | the same rows only, no sale recorded | refuse, or 0, tax 3,875, refund 625 | line 1a **4,000**, tax **4,355**, refund 145, line 7b checked |
  | the same rows on the covered lt family, no sale | refuse, or 0 | line 8a **4,000**, line 7a 4,000 |
  | code W st sale 4,000/5,000 (W 300) with its own rows, plus 5,000/1,000 rows on another transaction | refuse, or line 1b −700 | line 1b **3,300**, tax **4,271** |
  | covered st sale 10,000/7,000, then only the sale removed (its rows stay) | 0, tax 3,875, refund 625 | line 1a **3,000**, tax **4,235**, refund 265 |

  - The same shape on box E, box C and code B is rejected at entry ("companion
    presence violated", "companion provenance missing").
  - Charter cases "rows on a different transaction" and "a removed sale" both
    publish wrong numbers.
  - The first case gives the same wrong 7,000 on v81, so the defect is
    inherited. The milestone claimed to close it, though.
  - No Track 0 or live case records a row with no sale beside it. The 57 v81
    returns with misplaced rows block only because each sale lost all its
    rows.
- **Fix.** Either of two:
  - Add covered and code W row-to-sale presence pairs to the v82 entry at
    `packages/tax/loader.py:479`, as v79 to v81 did for the other three
    kinds. This is the smallest change, and it matches the siblings.
  - Or give each covered and code W admission check v2 a reverse
    `require_paired` (`income` = the row fact types, `withholding` = the
    sale), with a path that is active when a row family is nonempty.

  Then add the five cases above to the live module.

### F2 (blocking): Form 1040 line 7b says "Schedule D not required" next to a required Schedule D

- **Claim violated.** Decision 1 says that once a sale is recorded, the
  Exception 1 answers are not read. Decision 2 says an entry screen that
  records the reworded replies literally gives the right return.
- **Where.**
  - `packages/content/tax/2025/rule.form1040-line7b.json:37`. This v1 member
    is unchanged in v82. It reads only `schedule-d-required.conclusion`, so
    it ignores the ten sale counts that line 16 v7, line 7a v9, the base v10
    and both attachments now read.
  - `tables.py:39` (`CONSUMERS`) and `tables.py:219` (`ROUTE_READERS`) leave
    line 7b out of the audit.
  - `audit_harness.py:416` (`WATCH`) leaves it out of every projection.
- **Reproduction.** Wage return. A box C sale for 0 with basis 0, given the
  honest in-class answers. The four Exception 1 facts are left at the harness
  base, which is "yes" to each.
  - Under the v2 wording those are the truthful replies. The filer had no
    capital gain other than box 2a and no capital loss, and the sale is
    neither. The same holds for a 5,000/5,000 covered sale beside a 1,000
    box 2a distribution.
  - v82 publishes line 7b `published_categorical` ("checked") while Form
    8949 and Schedule D are both `published` (required).
  - On v81 the same answers gave line 7b checked and no attachment, which is
    consistent but wrong (D3). The v82 attachment fix makes the return
    contradict itself.
  - The same contradiction is in every base-answer run beside a sale (the
    124 Track 0 `base_exception1` runs, and `p_covered_st_only2a_yes_nolosses_yes`).
  - The tax itself is right. The return still says "Schedule D not required"
    with Schedule D attached, while Exception 1 does not apply to a filer who
    must report a sale on Form 8949 or Schedule D.
- **Fix.**
  - Add a line 7b successor that is `guard_inapplicable` when any of the ten
    sale counts is above zero, like `tax_activity` on line 16. Add line 7b
    to `ROUTE_READERS` and to the live projection.
  - Separately, the v2 question "Is it true that you had no capital gains in
    2025 other than …" invites "yes" from a filer with a zero-net sale. If
    the questions are meant to be read with no sale recorded only, say so in
    their words, for example "… and you did not sell or exchange any capital
    asset".

### F3 (should-fix): two field sentences are not true of their rules

- `packages/content/tax/2025/form1040.line-16.form-field.v3.json:42`
  (`guard_inapplicable`) says "Line 16 is computed here only when you sold
  covered securities, or when Schedule D is not required …". This was carried
  unchanged from v2. Line 16 v7 takes the Schedule D route for any recorded
  sale on any of the ten families.
  - Reproduction: `t4_s1_removed/honest` (no sale, a leftover "only box 2a"
    "no") shows this sentence.
  - Fix: "… only when you recorded a sale, or when …".
- `packages/content/tax/2025/form1040.line-7a.form-field.v2.json:34`
  (`blocked`) begins "Line 7a is blocked because Exception-1 authority is
  incomplete or the box-2a family is unclosed". With a sale recorded, line 7a
  v9 does not read Exception 1.
  - Reproduction: `n_covered_lt_box1g/honest` blocks line 7a on the
    admission refusal, and neither cause in that first sentence is present.
  - Fix: lead with the sale reasons, or drop "because".
- Every blocked line I saw has a non-empty field `explain`. The per-line
  `reasons` array is empty in 1,464 of the 1,734 blocked lines in the
  fixture. The page shows the field sentence, so these two sentences are what
  the filer reads.

### F4 (should-fix): the evidence does not reach line 7b or row-without-sale shapes

- `tests/test_sale_family_audit_v82.py:145` (`projection`) pins lines from
  `WATCH`, which has no line 7b. `tables.py` checks only the sale objects.
  - The `tables.py` docstring (line 9) says "and each scalar row", but
    `SALE_OBJECTS` holds no row fact type, so a row with no sale is outside
    the audit.
  - This is why F1 and F2 pass every committed check.
- `tests/test_sale_family_audit_v82.py:243` (`honest_exception1`) answers
  "only box 2a" "no" for any sale. That is the v1 sense of honest. Under the
  v2 wording, a zero-net sale's honest answer is "yes", which is the F2 path.
- Fix: add line 7b to the projection and the audit's route readers. Add the
  row fact types to the field table, with each row required to have a
  sale-pairing reader. Add a literal-v2 honest mode for zero-net sales.

### F5 (should-fix): CI cost, 694 runs and a 1.8 MB fixture

Measured from the committed fixture:

- **v81 honest runs: 198, redundant.** All 198 are asserted equal to their
  recorded-answer run by
  `test_each_honest_v81_return_computes_or_blocks_as_on_the_recorded_answers`.
  They witness only Decision 1, which the 20 `p_*` polarity cases already
  witness through the coordinator.
- **Track 0 `base_exception1` runs: 123 of 124, redundant.** Each has a
  projection identical to its honest run. The exception is `t4_s1_removed`,
  which is the one case where the answer matters. These runs witness the
  same Decision 1 property.
- **What can go.** Dropping both sets removes 321 runs: 694 to 373, about
  46 percent, or roughly 6 of the 11 minutes on 10 workers. The fixture loses
  about 0.84 MB and falls to about 0.92 MB.
- **What stays.** Every Track 0 row keeps a witness: the polarity matrix,
  `t4_s1_removed` in both modes, and every honest case.
- **Possible further cuts.**
  - The 10 `p0_d1_*` negative-proceeds runs are rejected at entry. They
    could be one entry-validation test per family, without a coordinator
    run.
  - The 28 `p0_e_*` duplicate pairs are kept as honest runs only (their base
    runs are in the 123). They could share one witness per family pair kind
    rather than all 28, though that is a judgement call, since they are the
    double-count witness.
- **Keep.** The 213 recorded v81 runs are the witness that every v81 return
  computes the same, and should stay.

### Notes

- **N1.** `tables.py:170` `NO_EFFECT` is keyed by field name only. Any future
  sale object with a `covered_security` field is exempt from the audit
  automatically. Key it by (object, field).
- **N2.** `REFUSED_BY` (`tables.py:177`) names boxes 2, 1f, 3, 4, 6 and 7. It
  does not name Form 1099-B boxes 8 to 11 (section 1256 contracts, which go to
  Form 6781) or box 13. Those fall under the unasked
  `no-other-schedule-d-sources` boundary, an accepted limit under
  Decision 5. The table would be a truer record if it named them with that
  answer.
- **N3.** The committed consumer table (`tables-v82.json`) uses transitive
  reach, which is coarse. For example, `f1099b.code-b-lt` "reaches"
  `schedule-d.line-1b` and `line-7`, and `f1099b.noncovered-lt` reaches
  `line-3`. It is pinned as a golden, so a reader may take it for the true
  flow.
- **N4.** The schedule-d line 1b v4 and 8b v4 blocked sentences now list "a
  line 1a or 8a sale with … box 1g". That cannot block lines 1b or 8b. The
  sentence is harmless but misplaced.
- **N5.** The per-statement box 4 and box 7 questions show once on the page,
  in generic "For each … statement" words, and do not say which statement
  is unanswered (`b4_two_statements_one_unanswered`). The owner accepted this
  in Decision 6.

## Per question

1. **Tax correctness.** I computed each case by hand: 2025 Tax Table midpoint
   rows, the single brackets 11,925 / 48,475 / 103,350, the 0 percent
   capital-gain ceiling of 48,350, and the standard deduction of 15,750 on
   wages of 50,000. Then I ran each through the coordinator on v82:
   - D1 `t1_s2/honest`: TI 38,250, tax 3,875, refund 625. Matches.
   - D2, a 5,000/5,000 covered sale or box E sale beside a 1,000 box 2a
     distribution (my own case): line 15 1,000, line 16 1,000, base 1,000,
     line 7a 1,000, TI 35,250, tax 3,875. Matches.
   - D3 `t5_s2`: all zero, both attachments required. Matches.
   - D4 `n_covered_lt_box1g`: blocks on the line 8a admission. Correct.
   - D5 `p0_f_covered_lt`: line 8a 3,000, TI 37,250, tax 3,875. Matches.
   - Box 4 `t2_s2`: blocks line 25b and asks. `t2_s3_no`: line 9 6,000,
     TI 40,250, tax 3,875. `t2_s3_yes`: blocks. Correct.
   - Box 7 `t3_s2`, `t3_s3_yes`, `p0_b2`: Schedule D line 16 and Form 1040
     block. Correct.

   I also rechecked all 119 published Track 0 entries in `expected.json`
   with my own implementation of the Qualified Dividends and Capital Gain Tax
   Worksheet. That covers TI, line 7a from Schedule D lines 16 and 21, tax,
   line 34 and 37, and the line 7 and 16 sums. There are no
   inconsistencies. **No expected value I checked is wrong.** The fixture
   does not pin line 7b (F2).
2. **Admission.**
   - Rows on a different transaction, beside an admitted sale or with no
     sale, and a removed sale whose rows stay: **wrong numbers publish**
     (F1).
   - A box 4 or box 7 answer left after a new statement: blocks and asks
     (`t2_s2`, `t3_s2`).
   - An Exception 1 answer beside a recorded sale: the numbers are
     unaffected (the polarity cases and my runs), but line 7b reads it (F2).
   - No v81 answer changes meaning. The Exception 1 fact types keep v1, and
     only the question words change. The return-level box answers were never
     published.
3. **The audit test.**
   - I mutated `rule.f1099b.covered-st-txn.admission.v2.json` so that it no
     longer reads `long_term` on line 1a. Five package tests failed,
     including `test_every_sale_field_on_v82_is_read_or_has_a_recorded_reason`
     with "f1099b.covered-st-txn.long_term is read by no rule".
   - I mutated `family.f1099b-code-b-st.json` so that its holding-period
     constraint no longer reads `long_term`. The audit failed the same way.
   - Both files were restored, and the tree is clean.
   - The `covered_security` reason is true: Form 8949 box A versus B follows
     box 12, whether basis was reported, not box 5.
   - The `REFUSED_BY` answers are each declared and read. The gaps are N1,
     N2 and F4.
4. **Immutability.**
   - `git diff github/main --stat` over `packages/content` and
     `packages/schemas`: 35 files, all added (`--diff-filter=MDRT` is
     empty), and no schema change.
   - Registry v80 keeps all 1,410 citizens and 85 packages of v79
     byte-equal, and adds 33 citizens and one package (core v82).
   - The loader change is the two v82 entries and a docstring line, nothing
     else.
5. **What the filer sees.** Every blocked line I saw has a non-empty field
   `explain`. Two are untrue of their rule (F3), and line 7b publishes wrong
   (F2).
   - The four v2 Exception 1 questions each assert their fact's proposition,
     so "yes" means yes. The words are plain, but they invite "yes" from a
     filer with a zero-net sale (F2).
   - The box 4 and box 7 questions' "yes" is the box shown or checked, which
     is the fact's "yes".
   - The new line 25b, Schedule D line 16 and lines 1a and 8a sentences are
     true of their rules.
6. **CI cost.** See F5: 694 runs can become 373, and the fixture can fall
   from 1.8 MB to about 0.9 MB, without losing a Track 0 witness.
7. **Test isolation.**
   - Neither new module assigns another module's globals. Evidence modules
     load under their own `sys.modules` names (`sale_family_audit_*`).
   - The only assignment anywhere is `audit_harness.loader_entries`, which
     swaps two `packages.tax.loader` functions for one run and restores them
     in `finally`. It is reached only for a scratch core, and the live module
     asserts that `loader_from is None` for v82.
   - The v81 returns are built in a subprocess.
8. **Data safety.**
   - `python3 tools/envelope_scan.py --range github/main..HEAD` exits 0 with
     no findings.
   - Grepping the added lines of the diff for home, private, temp and
     var-folders path prefixes finds nothing.
   - This review names no local path.
