<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-code-b",
  "status": "Closed. On core v81 a Form 1099-B sale with a wrong reported basis computes Form 8949 box A or D with code B (or BW), Schedule D lines 1b and 8b, Form 1040 line 7a and the tax from a filer-supplied correct basis. Zero-proceeds, cross-term duplicate and flagged covered sales no longer publish wrong returns. Core v80 and earlier are unchanged.",
  "scope": [
    "a return with a Form 1099-B sale whose reported basis is wrong computes Form 8949 with code B and the column (g) correction, Schedule D, Form 1040 line 7a and the tax, from a corrected basis the filer supplies, on boxes A, B, D and E as the instructions allow",
    "every return core v80 computes computes the same on the successor, and earlier cores render byte-identically",
    "what stays outside the class is refused by an answer, never computed partially"
  ],
  "non_goals": [
    "no adjustment codes other than B and W, and no rows carrying more than those",
    "no digital assets, no short sales, no other Schedule D sources",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-07-f8949-boxes-cf.md",
      "docs/milestone-retrospectives/2026-11-07-f8949-code-b.md",
      "docs/phases/engine-breadth/milestones/f8949-code-b.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f8949-code-b.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f8949-code-b.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f8949-code-b.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Broker Basis Corrections (2025)

Milestone key: f8949-code-b.
Branch: milestone/f8949-code-b-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-07.
Starting point: `milestone/f8949-boxes-cf-2025` at `27fc2390` (PR #262,
core v80). It was rebased onto `github/main` at `dd81de67` after #262
merged.
Closed 2026-11-07. Retrospective:
`docs/milestone-retrospectives/2026-11-07-f8949-code-b.md`.

## What we are trying to accomplish

Core v80 computes Form 1099-B sales in boxes A to F with code W. When a
broker reports a wrong basis, which often happens after a corporate action
or with employee stock, the filer reports the sale with code B and
corrects the gain or loss in column (g). Today the in-class answer
refuses that return. The useful outcome is that it computes, from a
corrected basis the filer supplies.

## What we know

- **What exists on v80.** Covered families (boxes A and D) and
  noncovered families (B and E), each with a code W path. Box C and F
  families. Two grouped closure questions (`source-closure-mapping.v4`,
  ADR 0084). The ADR-0061 Path B answer for codes other than W. Lines 2,
  3, 9 and 10, with paired-amount, count and amount-agreement checks.
- **Lessons.** The f8949-boxes-cf retrospective: check each input
  question's words against its proposition when it is written; pin each
  blocked line's reason and its row's (disposition, code, missing) from
  the first live test; load evidence harnesses under unique module names.
- **What we do not know.**
  - What the 2025 instructions require for code B. The relevant points
    include whether the broker's basis is shown in column (e) with the
    correction in (g), or the correct basis in (e). They also include how
    a basis-reported sale with code B moves from line 1a/8a direct
    reporting or box A/D to Form 8949, and how code B combines with W on
    one row.
  - Whether the v80 pattern carries over as content only.
  - What a v80 return with a wrong broker basis does today.

## Actions the team will take

1. **P0: law, state and design.**
   - Law from the 2025 instruction sources, with quotes.
   - State on core v80 through `live_coordinate_run`.
   - The smallest successor set, prototyped on scratch. Every case's
     attachment dispositions and block reasons are asserted, and the
     gain, loss and wash cases are computed by hand.
   - Stop and report if an engine, schema or recording change is needed.
2. **Decide.** The class and the question shape. The owner decides if a
   schema, ADR or recording change is needed.
3. **Track 0 adversarial closure.** The six artifacts, with built
   evidence. No row passes beside a standing counterexample.
4. **Track 1: build.** Successors, core v81 and its registry and release,
   cases through the real coordinator and the page, v80 and earlier
   pinned, full suite.
5. **Close.** Fresh-reader review with hand-computed lines, exact-head CI,
   retrospective, roadmap, frontier row and parked list. Merge on green
   verify (owner standing approval, renewed 2026-11-07).

## Cases that will shape the design

- A covered box A sale whose broker basis is too high (a smaller gain
  becomes a larger one), and a box D sale whose broker basis is too low.
- A code B correction that turns a gain into a loss (line 21 limit).
- A row with both B and W.
- A noncovered box B or E sale. Code B needs no correction there, since
  the basis is the filer's own, so the case is refused or not applicable.
- A code B sale with the corrected basis missing: it blocks and asks.
- Every return core v80 computes: identical on the successor.

## Process

Dispatch is to Opus and Sonnet sub-agents (owner, 2026-11-06, renewed
2026-11-07). Opus runs P0, Track 0 and the fresh review; Sonnet runs
content-only build units. Each unit commits on this branch as it goes.

## P0 result

Evidence: `f8949-code-b-evidence/p0-law-state-design.md`, with
`codeb_probe.py` / `codeb-probe-output.json` (core v80) and
`codeb_prototype.py` / `codeb-prototype-output.json` (scratch core v81).

- **Law.** On box A or D, column (e) is the basis the Form 1099-B shows,
  even though it is wrong. Column (g) is that basis minus the correct
  basis, from the Worksheet for Basis Adjustments. The sale stays in box A
  or D and goes on line 1b or 8b, never on line 1a or 8a. With code W the
  row's codes are "BW", and column (g) is the net: correction plus the
  wash-sale loss disallowed, measured on the corrected loss. On box B or E,
  code B applies with the correct basis in (e) and -0- in (g). On box C or
  F code B does not apply.
- **v80.** Honest answers refuse a code B return through the boundary
  answers (v80 check 3 on lines 3 and 10, and the line 1a/8a nonzero
  arms). The block has no question. If the filer follows the Form 1099-B
  and claims no Form 8949, v80 publishes the broker's wrong gain. If the
  corrected basis is recorded on line 1a/8a, on box B/E, or on code W with
  a false Path B, v80 publishes the right dollars on the wrong line or box.
  Box B/E code B already computes the right dollars, but no code is shown.
- **Design.** A content-only core v81 with 57 member edits (32 adds, 25
  replacements) and two loader entries:
  - code B sale families for box A and D, keyed like other Form 1099-B
    sales;
  - the correct basis on the sale, and a column (g) row that must equal
    the worksheet;
  - a third grouped question and a code B in-class answer, read through a
    guarded arm placed before the v80 one;
  - lines 1b and 8b add the code B column (h).

  All 30 v81 cases match their hand values and blocked states. All 143 v80
  returns are identical on v81 under the new "no". Unanswered, every one
  blocks and asks the new question. No engine, schema or recording change
  is needed.
- **Owner questions** (P0 document, "Questions for the owner"):
  1. the question shape and the one new answer on every workspace;
  2. whether the correct basis gets its own row, so that a missing one
     blocks and asks;
  3. how box B/E code B is marked;
  4. whether part labels are enough for column (f).

## Decisions

Foreman, 2026-11-07, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts afterwards.

1. **The P0 design is adopted.** It adds new box A and D code B sale
   families, each with paired proceeds, basis and column (g) rows. A
   column (g) check requires (basis shown − correct basis + wash-sale
   amount). It adds one new grouped question ("Did any Form 1099-B …
   report … a basis that is wrong?") and a new in-class answer, read only
   after that "yes" and before the v80 in-class answer. Every v80
   workspace answers the new question once. With "no", all 143 v80
   returns are identical.
2. **The correct basis stays on the sale record.** A sale entered without
   it is rejected at entry. The column (g) row blocks and asks. A separate
   correct-basis row would add two families and two questions and would
   make no return more correct.
3. **Box B/E code B: option (a).** The existing in-class answers cover it:
   the filer enters the correct basis, and column (g) is -0-, so the
   dollars are right. The part labels do not show the letter B for these
   rows.
4. **Column (f) letters: part labels are enough for this milestone.** A
   per-row code letter on Form 8949 (B on box B/E rows, BW on combined
   rows) is parked for a later milestone that models column (f) letters
   for every code.

Foreman, 2026-11-07, on Track 0:

5. **Track 0's four repairs are adopted:** cross-term exclusivity, the
   amounts check closing first, attachment counts, and the field words.
6. **The four inherited v80 gaps are taken into Track 1**, by content
   only. Each one publishes a wrong or incomplete return today, and the
   f8949-boxes-cf milestone set the precedent of blocking such returns:
   - A code W row with zero proceeds requires neither attachment.
   - A box B row with zero proceeds does not require Form 8949.
   - One transaction recorded on box B and on line 8a is counted twice.
     The same applies to every pair of covered and noncovered families
     across terms.
   - A covered sale flagged `taxpayer_side_adjustment` "yes" publishes
     the broker's gain. It must block and say why.

   The returns that change are listed in Track 1 and accepted on the same
   terms as before. If any fix needs more than content, it is parked
   instead.
7. **The presentation limit from f8949-boxes-cf extends** to the refused
   code B paths that block with a true reason but no question. One
   example is a code B sale beside a Form 8949 "yes". These stay parked
   with the rule-artifact successor.
8. **A false Path B "yes" beside a code B row is accepted.** It gives the
   same result as the honest answer, as on f8949-boxes-cf.

## Track 0 adversarial closure

Evidence: `f8949-code-b-evidence/track0-closure.md`, from
`codeb_track0.py` / `codeb-track0-output.json`. These run on the scratch
core v81 of `codeb_prototype.py` with its `REPAIRS` on. That is 99 cases
on the final and decided designs, plus the 143 v80 returns and four v80
neighbour probes, all through `live_coordinate_run`.

Track 0 found four counterexamples on the decided design, and each is
fixed by a switchable content repair:

- `cross_term_exclusive`: one transaction recorded as a code B sale and on
  the other term's v80 family was counted twice.
- `check_closes_first`: a code B answer made stale while both terms have
  members asked no question.
- `attachments_read_count`: a code B row with zero proceeds and zero shown
  basis published Form 1040 with neither attachment required.
- `field_words`: the line 1b and 8b blocked sentence named a wait that
  cannot occur.

The final build has 59 member edits (34 adds, 25 replacements). No engine,
schema or recording change is needed.

- Authority-lifecycle table: PASS. Closure document, artifact 1. The sale,
  the paired rows, the column (g) row, code W with B, Q3, IC3 and the
  checks each name their invalidating events and the cases that show them.
  These include `x_corrected_basis_changed_g_stale` and `..._g_fixed`,
  `x_remove_sale_keep_rows`, `x_bw_w_exceeds_correct_loss_within_shown`
  and `x_g_sign_flipped`.
- Empty/nonempty authority matrix: PASS. Artifact 2:
  - the code B families against the A/D direct, A/D code W, B/E and C/F
    families, under closed-empty, missing, unbacked-"yes", eligible and
    ineligible states;
  - a "yes" with nothing recorded is refused, beside each neighbour
    (`m_q3_yes_nothing_*`);
  - a code B sale beside a "no" asks Q3 (`a_q3_no_with_member`,
    `m_d_q3_no_with_member`);
  - a code B sale beside a v80-only in-class answer asks IC3
    (`m_a_v80_ic_only`, `m_a_v79_ic_only`).
- Late-member lifecycle: PASS. Artifact 3:
  - T1: "no", compute, add a code B sale, re-answer, recompute;
  - T2: a covered line 1a sale corrected into a code B sale, with
    `t2_stage4_keep_covered` refused by identity exclusivity;
  - T3: a code W row corrected into BW;
  - a stale "yes", and a stale "no" with both terms (`x_q3_*`, which ask
    Q3 after `check_closes_first`).
- Neighboring capability dependency diff: PASS. Artifact 5. With Q3 "no",
  all 143 v80 returns are identical in every line, attachment, question
  and watched row (55 publish, 84 are blocked, 4 are rejected before a
  run). Unanswered, none publishes and every one that runs asks Q3. The
  only new prerequisite is Q3, justified by lines 1b and 8b now summing
  the code B families (ADR 0084). Only the line 1b and 8b sentences change
  wording.
- Reused-claim semantic/lifecycle equivalence: PASS. Artifact 4:
  - Q1, Q2, IC79 and IC80 are never widened, and they decide nothing under
    the guarded arm (`m_a_c_ic3_yes_v80_ic_no` = `..._v80_ic_yes`);
  - Path B is never read as admitting a code B row (`x_path_b_yes` =
    `a_high`);
  - by ADR-0061 Decision 2, the code W families' proposition excludes code
    B rows, and exclusivity enforces it in both terms.
- Integration surface: PASS. Artifact 6:
  - every consumer of lines 1a, 1b, 2, 7, 8a, 8b, 9, 15, 16 and 21, line
    7a, the preferential base, both attachments, the column (h) and count
    symbols;
  - exactly one row per publisher in all 97 saturated cases and all 139
    v81 runs of v80 returns;
  - one built model per disposition path, the blocked rows' (disposition,
    code, missing) pinned, and a presentation probe of the line 1b and 8b
    v3 fields and the Form 8949 v5 code B parts.
- Known limitations affecting correctness: none in the code B class.
  Owner disposition is required for four inherited v80 neighbour
  behaviours, measured unchanged on v81 (closure document, owner question
  1):
  - zero-proceeds code W rows and zero-proceeds box B rows do not require
    Form 8949;
  - cross-term duplicates between v80 families are counted twice;
  - a covered sale flagged with a taxpayer-side adjustment publishes the
    broker's gain.

  Owner questions 2 and 3 (block-only presentation, and Path B "yes" beside
  a code B row) are presentation and posture questions, not correctness.

## Track 1 result

Built: core v81, registry v79 and release v79, made with
`tools.package_successor` from v80. 77 member edits (48 adds, 29
replacements), all generated by `codeb_prototype.py` with every
`REPAIRS` switch on and byte-identical to it. The loader adds v81's
companion declaration (v80's pairs plus the six code B scalar pairs) and
names v80's covered-flag refusal map for v81. No edit under
`packages/kernel/`, `packages/derivation/` or `packages/schemas/`, and no
recording change.

**Decision 6, by content.** Four switches were added to the prototype
(`track0-closure.md`, "Track 1 rerun"):

- `w_zero_proceeds`, `b_zero_proceeds`: per-term counts of the code W and
  box B/E sales, read by both attachments.
- `v80_cross_term_exclusive`: each Form 1099-B sale family checks per sale
  that the other term's families at or before it (covered, code W,
  noncovered) hold no sale on the same identity. Noncovered amounts-agree
  v2. The covered and code W sales get a new per-sale admission rule and a
  return-level check, which lines 1a, 8a, 1b and 8b require.
- `covered_tsa_blocks`: the same admission rule refuses a covered or code
  W sale flagged `taxpayer_side_adjustment` "yes", reading the flag
  through a yes/no parameter. Lines 1a and 8a (fields v3 and v2) and 1b
  and 8b now say such a sale, or one recorded under both terms, is outside
  what the return computes.

Family-level `identity_exclusivity` and member constraints on the v80
families would need family successors, and so a horizon handover in every
v80 workspace. That is a recording change, so the per-sale rules are used
instead.

**Cases.** Track 0 rerun: 99/99 final cases match, `decided` shows the
same seven counterexamples, and 19/19 neighbour probes match their v81
expectations. Live module `tests/test_code_b_sales_v81.py`: 98 Track 0
cases, 135 v80 returns and 19 Decision 6 probes on the published v81 (one
Track 0 case and eight v80 returns dropped as exact duplicates). The table
is `tests/fixtures/code_b_sales_v81/expected.json`, and regeneration
reproduces it byte for byte. Fast test
`tests/test_code_b_sales_v81_package.py`: byte identity, member edits,
registry add-only, release pin, loader entries, and each new question
against its proposition.

**v80 returns that change.** Of the 143, 138 are identical under Q3 "no".
Five change only in a blocked attachment row's `missing` list, which now
also names the box B/E count waiting on the same unclosed family
(pattern `b_zero_proceeds`):

- `carried_boundary_no_with_member`
- `carried_late_member_unclosed`
- `carried_late_yes_stale`
- `carried_yes_then_no_with_member`
- `v80_m_b_q1_no_with_member`

No line, value, disposition or question changes. The v80-shaped returns
that do change their result are the Decision 6 probes. Zero-proceeds code W
and box B/E rows now require their attachments. Seven cross-term
duplicates and three taxpayer-side flags now block the return, and four
controls are unchanged. On every v81 workspace, the line 1a, 8a, 1b and
8b blocked sentences change wording; no value changes.

**Checks (local).** Fast lane: 1709 passed, 8 skipped. Full `pytest`:
4844 passed, 24 skipped, 0 failed (31 min). `python3 -m mypy`: no issues
in 469 files. CI `verify` remains the gate of record.

**Deviations.**
- The cross-term check reads the other term's family closure. A covered
  or code W check never reads the noncovered (Q1) closure.
- A duplicate noncovered sale publishes "disagree" on the existing
  amounts-agree vocabulary, as box C/F review S2 did.
- A refused code W sale (duplicate or flagged) leaves Form 8949 and
  Schedule D required, which is true. A refused direct sale blocks Form
  8949 through the line 1a/8a admission checks.
- Refusals show no question (Decision 7 limit).

**Parked.** None of the four fixes needed more than content. Per-row
column (f) letters stay parked (Decision 4).

### Repair

Charter: `docs/reviews/f8949-code-b/charter-repair.md`, after the
fresh-reader review (`docs/reviews/f8949-code-b/review.md`). Core v81,
registry v79 and release v79 are rebuilt in place, with no v82, by
`codeb_prototype.py publish`, which copies the prototype's scratch build
over the published files. 80 member edits (50 adds, 30 replacements). No
edit under `packages/kernel/`, `packages/derivation/` or
`packages/schemas/`, and no recording change.

- **B1.** Two new switches cover a direct (line 1a or 8a) sale with zero
  proceeds:
  - `direct_zero_proceeds` adds per-term counts of the line 1a and 8a
    sales, which the Schedule D attachment reads (Form 8949 does not);
  - Form 1040 line 7a v8 treats a nonzero line 1a or 8a as Schedule D
    activity.

  Probes: box A and box D at 0 / 500 give line 7a -500, taxable income
  33,750, tax 3,815, and require Schedule D. Box A at 0 / 0 requires
  Schedule D.
- **B2.** Measured with `-n0 --durations=0`. Only
  `test_speculative_refusal_then_retry_and_gated_retraction_are_atomic`
  calls over 1.0 s (1.7 s), and it is now `live`. The 2.7 s setup on a
  worker's first test is the session registry warm-up in
  `tests/conftest.py`. It moves to whichever test runs first and is not
  timed, so no test was marked for it. The budget is unchanged.
- **S1 to S4.** Field wording:
  - Lines 1b and 8b say zero also when no sales are recorded.
  - Their blocked text names the checks (with the column (g) rule) and
    the refusal by an answer.
  - Line 8a v2 uses line 1a's plain words.
  - The taxpayer-side sentence on all four lines names the route to
    code B.
- **S5.** `covered_flags_block`: the admission rule refuses a covered or
  code W sale flagged `ordinary_indicated`, `box_1f_market_discount`,
  `qof_indicated` or `collectibles_or_special_rate` "yes" (new admission
  value `flagged-outside-class`). There is one probe per flag on a direct
  sale, plus a code W collectibles sale.
- **S6.** The projection pins the tie-out text of each nonzero Form 8949
  part when Form 8949 is published. A test holds columns (d), (e) and
  (g) for `a_high`, `d_low` and `a_bw`.
- **S7.** Regeneration still runs all 135 distinct v80 returns, then drops
  the 47 whose v81 projection, v80 difference and Form 1040 lines match
  another's. `SAME_PROJECTION` in `tests/test_code_b_sales_v81.py` lists
  each dropped return beside the one it matches. Regeneration fails if
  that list goes stale. 88 v80 returns stay, including every one that
  changes.
- **N3, N2.** Q3: "Did any Form 1099-B or substitute statement you
  received show a cost or other basis, reported to the IRS, that is
  wrong?" IC3 is now a two-item list followed by the question, and it
  keeps "in the one box its statement gives it".

**Track 0 rerun.** The final design matches 99/99 cases. The decided
design shows the same seven counterexamples. All 27 neighbour probes
match (19, plus three for B1 and five for S5). Unanswered, every v80
return asks Q3 and none publishes.

**v80 returns that change.** Under Q3 "no", 131 of the 143 are identical
and 12 change. In each one a row is blocked on both versions, and only
its `missing` list grows, by a symbol that waits on the same unclosed or
refused family. No line, value, disposition or question changes.

- `carried_boundary_no_with_member`, `carried_late_member_unclosed`,
  `carried_late_yes_stale`, `carried_yes_then_no_with_member` and
  `v80_m_b_q1_no_with_member`: both attachment rows add the box B/E count
  (`b_zero_proceeds`, as before).
- `carried_covered_both_boundaries_no`,
  `carried_covered_flag_corrected_to_no`,
  `carried_covered_flag_no_path_a` and `carried_covered_flag_no_st`: the
  Schedule D row adds the line 1a or 8a count, and the line 7a row adds
  line 1a or 8a (B1).
- `probe_a_high_direct_broker_honest`,
  `probe_a_high_direct_fixed_honest` and
  `probe_d_low_direct_broker_honest`: the line 7a row adds line 1a or 8a
  (B1).

The v80-shaped returns whose result changes are the probes. The two
zero-proceeds direct sales now publish line 7a -500 and require
Schedule D, where v80 published 0. The 0 / 0 sale now requires
Schedule D. The five flagged sales now block. On every v81 workspace the
line 1a, 8a, 1b and 8b sentences and the Q3 and IC3 wording change; no
value does.

**Checks (local).** Fast lane: 1714 passed, 8 skipped. Full `pytest`:
4812 passed, 24 skipped, 0 failed. That total is the fast lane plus
`-m live` run in five file shards (3098 passed, 16 skipped), because a
single run exceeds the foreground limit. `python3 -m mypy`: no issues in
469 files. CI `verify` remains the gate of record.

**Parked.** None. N1, N4 and N5 stay recorded in the review only.
