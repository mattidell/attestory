# P0: confirm the attachment gaps and design the guards

Milestone `attachment-closure`. Branch `milestone/attachment-closure-2025`, base `a1149bd6`
(core v62, registry v60, release v60). Synthetic `demo.*` data only. No repository content,
rule, package, schema, engine or test changed. Ceiling: live confirmation and a paper design,
plus one scratch candidate that was built and run outside the repository (below).

Evidence, all run from the repository root:

- `probe.py` -> `probe-output.json`. Every run goes through `live_coordinate_run` on the
  committed core v62 / registry v60 / release v60, using the collect-closure tests' own
  helpers. Per source set: one 1,000 member, closure unanswered ("unanswered") and the same
  member with the closure attested true ("answered", the control). Where the attachment is only
  *required* by another family, a second variant (`with_trigger`) records and closes a trigger
  family first, so the set under test is the only unconfirmed family. Wash-sale variants also
  answer the Form 8949 Part III question so Form 8949 can publish. Same-statement companions
  a refusal names are added (`f1098e.box2-checked-authority`,
  `f1099int.box9-specified-pab-authority`).
- `design_check.py` -> `design-check-output.json`, `v62-to-v63.json`. Builds a core v63
  candidate in a temporary directory with `tools/package_successor.build_successor` (13 guarded
  subtotal-rule successors), runs it through the same cases, and compares with v62. The
  candidate is not committed; the only runtime patch is that scratch v63 shares v62's companion
  declaration, as the loader would grant a published v63.

## Summary

- Of the 24, **13 publish a partial amount** on v62, **10 are already blocked** (an upstream
  guarded rule that the attachment's own requirement reads is absent), and **1 reaches no
  attachment amount** (`f1099int.b8`).
- An attachment cannot be made to wait through its own content: `completeness` carries only
  fact-type answers (presence or categorical value), and the validator rejects any answer type
  that is not a categorical string domain, which a boolean closure fact is not. It waits only
  when a symbol it reads is absent. So the guard goes on the **subtotal rule** the attachment
  reads (the pattern v62 already used for box 2a and line 4b, and the reason those two left
  the known-gap list).
- **13 successor citizens are needed**, all `...-subtotal` rules, 7 of them entrypoints. That
  exceeds the eight-citizen stop condition: **stop met, split proposed** (section 3).
- No engine, schema, kernel or operation change is needed. A complete return is unchanged
  (scratch v63: 240 published values identical to v62, no blocks).
- The two Schedule B adjustment sets cannot be guarded without also stopping line 2b from
  publishing a partial total, because line 2b reads the same subtotal symbols. Line 2b's
  citizen is untouched; its behaviour changes. This is an owner decision (section 5).

## 1. Confirmation (question 1)

Results are v62, one 1,000 member, closure unanswered. "Row set" is the amount the attachment
itemizes. In every "partial" row the line behind the same set is blocked
`SOURCE_SET_UNCLOSED` while the attachment publishes.

| Source set | Attachment | v62 result | Class |
| --- | --- | --- | --- |
| `f1099b.covered-lt-proceeds` | Schedule D | `line-8a-proceeds` row set 1,000 published; line 8a blocked | partial amount published |
| `f1099b.covered-st-proceeds` | Schedule D | `line-1a-proceeds` 1,000 published; line 1a blocked | partial amount published |
| `f1099b.covered-lt-basis` | Schedule D | alone: not required (requirement reads proceeds only). With lt proceeds closed: `line-8a-basis` 1,000 published | partial amount published (once required) |
| `f1099b.covered-st-basis` | Schedule D | same, `line-1a-basis` 1,000 | partial amount published (once required) |
| `f1099b.covered-w-lt-proceeds` | Form 8949 | `box-d-proceeds` 1,000 published; Schedule D line 8b blocked | partial amount published |
| `f1099b.covered-w-st-proceeds` | Form 8949 | `box-a-proceeds` 1,000 published; line 1b blocked | partial amount published |
| `f1099b.covered-w-lt-basis` | Form 8949 | alone: not required. With w-lt proceeds closed: `box-d-basis` 1,000 published | partial amount published (once required) |
| `f1099b.covered-w-lt-adjustment` | Form 8949 | with w-lt proceeds closed: `box-d-adjustment` 1,000 published | partial amount published (once required) |
| `f1099b.covered-w-st-basis` | Form 8949 | with w-st proceeds closed: `box-a-basis` 1,000 published | partial amount published (once required) |
| `f1099b.covered-w-st-adjustment` | Form 8949 | with w-st proceeds closed: `box-a-adjustment` 1,000 published | partial amount published (once required) |
| `f1099g.1` | Schedule 1 | `line-7-unemployment` 1,000 published; `schedule1-line7` blocked | partial amount published |
| `scheduleb.adjustment.nominee` | Schedule B | alone: not required. With 1099-INT box 1 at 2,000 closed: Part I `nominee_distribution` row 1,000 published; line 2b also publishes | partial amount published (once required) |
| `scheduleb.adjustment.abp-adjustment` | Schedule B | same, `abp_adjustment` row 1,000 | partial amount published (once required) |
| `f1099div.1a` | Schedule B | blocked `DEPENDENCY_ABSENT` on `dividends.ordinary-total` (line 3b guarded) | blocked |
| `f1099int.b1`, `.b3`, `.b10`; `f1099oid.b1`, `.b5`; `form1065-k1.box5`; `non-form-interest` (7) | Schedule B | blocked `DEPENDENCY_ABSENT` on `interest.positive-total` (`interest-positive-total` guarded) even at 1,000, below the Schedule B threshold; line 2b and AGI still publish the partial (the owner-held gap) | blocked |
| `f1099k` | Schedule 1 | blocked on `schedule1.top-entry` (guarded) | blocked |
| `f1098e.1` | Schedule 1 | blocked on `schedule1.line21-sli-deduction` (`sli-worksheet` guarded) | blocked |
| `f1099int.b8` | Schedule 1 (static path only) | nothing published by any attachment; Schedule 1 itemizes only `f1099g.1`, `f1098e.1`, `f1099k`, and box 8 reaches it only through the SLI deduction chain that line 2a and the worksheet already hold | not reachable in practice |

Counts: **13 partial amount published, 10 blocked, 1 not reachable in practice** (24).

Caveats, stated plainly.

- The plan's guess that the wash-sale sets "may already block" is disproved. Member validation
  forces related members, not an answered closure: with the closure unanswered the Schedule D
  line (8b / 1b) blocks and Form 8949 publishes the unconfirmed amount.
- The "blocked" class rests on an existing guarded rule that happens to sit in the attachment's
  requirement. It is a live fact today, not a property of the attachment, so each needs a pinned
  case. `f1099k` and `f1098e.1` cannot be shown publishing in the answered control with this
  harness (their answered return is itself incomplete: `schedule1.top-entry` and
  `line21-sli-deduction` need answers the harness does not supply), so their verdict is the
  unanswered block naming the guarded symbol, as in the collect-closure survey.
- The standalone basis and adjustment variants leave the attachment `inapplicable`; the partial
  amount appears only once another closed family makes the attachment required. That is a real
  return (proceeds recorded, basis not yet confirmed), so they stay in scope.
- The Schedule D row sets carry no wash-sale sets (Form 8949 does), so Schedule D is
  unaffected by the wash adjustment and basis sets beyond being required by wash proceeds.

## 2. Mechanism (question 2)

`packages/derivation/runner.py`, `attempt_attachment` (and `_attachment_threshold_trigger`,
`_attachment_block`, `_collect_row_source`):

1. **Requirement.** Every symbol in `requirement.subtotals` (or each `any_trigger` trigger)
   must be present: a missing one blocks `DEPENDENCY_ABSENT` before the threshold is compared
   (`_attachment_threshold_trigger`). Not required -> `inapplicable`.
2. **Itemization symbols.** For schema v2/v3/v4/v5/v6/v8/v11, every part's `tie_out.line_symbol`,
   every row-set `subtotal_symbol` and every adjustment `subtotal_symbol` must be present, else
   `DEPENDENCY_ABSENT` (`missing_itemization`).
3. **Completeness.** `required_answers` and `branch_requirements` are fact-type answers: presence,
   and for `check: value` an equality to a categorical string. Nothing in them can name a
   source set or a closure.
4. **Rows.** The rows are read straight from the family's members (`self.sources`,
   `_collect_row_source`) with no closure check, and tied out to the subtotal symbol. A tie-out
   mismatch blocks `ITEMIZATION_TIE_OUT_VIOLATION`.

So `completeness` cannot require a source set closed, and no other content field can: it is
presence and categorical value only. `packages/derivation/package_validation.py` (the
"Attachment answer encoding guard") rejects any answer fact type that is not a categorical
all-truthy string domain (`ATTACHMENT_ANSWER_NOT_CATEGORICAL`), and the closure fact is a
boolean. Making an attachment require closure directly would be a schema and validator change.
Not needed.

**An attachment can be made to wait by a guarded rule, but only the subtotal rule.** It reads the
raw subtotal as both requirement trigger and tie-out line (`attachment-rule.v8`/`v11` also
check that `tie_out.positive_subtotals` equal the row-set subtotals), so it cannot be pointed at
a guarded gain line instead: line 8a is proceeds minus basis and would not tie out. Guarding the
rule that publishes the subtotal makes the symbol absent, and every reader waits, including the
attachment. This is exactly what happened to box 2a and line 4b on v62: their attachment paths
are not in `KNOWN_GAP_ATTACHMENTS`, and `test_the_check_finds_new_attachment_paths_on_core_v61`
finds them on v61 only. The design check shows it live (section 4).

## 3. Design (question 3)

Smallest successor: for each confirmed gap, a successor of the `...-subtotal` rule whose `when`
is `require_closed` over the source set its `collect` reads (the v2 shape of
`rule.f1099div-2a-subtotal`). No other citizen changes: the attachment citizens, the form-field
citizens (they bind symbols), the interest composition and the line rules all keep their
versions. Core v62 -> v63, registry v60 -> v61, release v60 -> v61 with
`tools/package_successor.py`; the change set is `v62-to-v63.json`, which the builder accepted
(ad hoc, `build_successor` validated the full package and registry for all 13, and for all 24
subtotal rules in a throwaway run that is not committed).

| # | Citizen (id, from -> to) | Schema | Entrypoint | Closes |
| --- | --- | --- | --- | --- |
| 1 | `tax.us.2025.rule.f1099b-covered-lt-proceeds-subtotal` v1 -> v2 | rule-artifact.v2 | no | Schedule D 8a proceeds |
| 2 | `...f1099b-covered-lt-basis-subtotal` v1 -> v2 | rule-artifact.v2 | no | Schedule D 8a basis |
| 3 | `...f1099b-covered-st-proceeds-subtotal` v1 -> v2 | rule-artifact.v2 | no | Schedule D 1a proceeds |
| 4 | `...f1099b-covered-st-basis-subtotal` v1 -> v2 | rule-artifact.v2 | no | Schedule D 1a basis |
| 5 | `...f1099g-1-subtotal` v1 -> v2 | rule-artifact.v3 | yes | Schedule 1 line 7 |
| 6 | `...scheduleb-adjustment.nominee-subtotal` v1 -> v2 | rule-artifact.v3 | no | Schedule B nominee row (and line 2b) |
| 7 | `...scheduleb-adjustment.abp-adjustment-subtotal` v1 -> v2 | rule-artifact.v3 | no | Schedule B ABP row (and line 2b) |
| 8 | `...f1099b-covered-w-lt-proceeds-subtotal` v2 -> v3 | rule-artifact.v5 | yes | Form 8949 box D proceeds |
| 9 | `...f1099b-covered-w-lt-basis-subtotal` v2 -> v3 | rule-artifact.v5 | yes | Form 8949 box D basis |
| 10 | `...f1099b-covered-w-lt-adjustment-subtotal` v2 -> v3 | rule-artifact.v5 | yes | Form 8949 box D adjustment |
| 11 | `...f1099b-covered-w-st-proceeds-subtotal` v2 -> v3 | rule-artifact.v5 | yes | Form 8949 box A proceeds |
| 12 | `...f1099b-covered-w-st-basis-subtotal` v2 -> v3 | rule-artifact.v5 | yes | Form 8949 box A basis |
| 13 | `...f1099b-covered-w-st-adjustment-subtotal` v2 -> v3 | rule-artifact.v5 | yes | Form 8949 box A adjustment |

Change set v62 -> v63: 13 member replacements, 7 entrypoint replacements (rows 5, 8-13), no
binding or admitted-schema edit, 13 new registry entries, `package_version` v63,
`release_version` v61. Rows 1-4 are reached through dependencies rather than listed as
entrypoints, as on v62.

**Stop condition met: 13 > 8.** Proposed split, each at or under eight:

- **Track 1a (7): Schedule D, Schedule 1, Schedule B.** Rows 1-7. One entrypoint edit (row 5).
  Core v63, registry v61, release v61.
- **Track 1b (6): Form 8949.** Rows 8-13. Six entrypoint edits. Core v64, registry v62,
  release v62 (stacked on 1a), or a single v63 if the owner waives the limit; the rows are
  independent, so they may be reordered.

**What the 10 blocked and 1 not-reachable sets need.** Nothing in content: they are held by a
guarded rule the attachment's requirement reads. The regression test's static survey cannot see
that (it over-approximates), so they stay flagged statically. Track 1 should leave exactly these
11 in `KNOWN_GAP_ATTACHMENTS`, renamed for what they are (held by the attachment's own
requirement), each with a pinned live case (the unanswered block named in section 1), and the
other 13 removed from the list. An alternative is to teach the survey to credit requirement
symbols (a change to `tools/collect_closure_survey.py`, outside this unit).

**The nine interest sets without touching line 2b.**

- The seven positive sets (`f1099int.b1`, `.b3`, `.b10`, `f1099oid.b1`, `.b5`,
  `form1065-k1.box5`, `non-form-interest`): their attachment path is already held, by the
  guarded `interest.positive-total` that Schedule B's requirement reads. No successor needed.
- The two adjustments (`scheduleb.adjustment.nominee`, `.abp-adjustment`): rows 6 and 7 guard
  them with no edit to the line 2b citizen. But line 2b reads the same two subtotal symbols, so
  on the candidate **line 2b and everything behind it also stop publishing** while either
  adjustment family is unclosed (live: `interest.taxable-total` and AGI absent). That closes
  the line 2b gap for those two sets, and the plan's non-goal ("no line 2b change") is met in
  the citizen but not in behaviour.
- The same subtotal-rule guard on the seven positive sets would, by the same mechanism, close
  line 2b for them with no validator change. This contradicts the stated reason the line 2b
  successor was parked (a guard on line 2b itself is refused by the validator); the subtotal
  route sidesteps that. Not run live, not in the 13, and a new scope question for the owner.

## 4. Cases (question 4)

All on the real coordinator. Control for every guarded set: closure answered, one 1,000
member -> **v63 values identical to v62** (`design-check-output.json`,
`v62_answered_values_equal: true` for all 15 sets run). Unanswered column is v62 -> v63.

| Set (variant) | v62, closure unanswered | Expected and observed on v63, unanswered | v63, answered |
| --- | --- | --- | --- |
| lt-proceeds | Schedule D publishes row set 1,000; line 8a blocked | Schedule D `DEPENDENCY_ABSENT` on `f1099b.covered-lt-proceeds-subtotal`; line 8a, AGI absent | Schedule D 1,000; AGI 51,000 (= v62) |
| st-proceeds | same, line 1a | Schedule D blocked on `...st-proceeds-subtotal` | = v62 |
| lt-basis (with lt proceeds closed) | Schedule D publishes `line-8a-basis` 1,000 | Schedule D blocked on `...lt-basis-subtotal` | = v62 |
| st-basis (with st proceeds closed) | same | Schedule D blocked on `...st-basis-subtotal` | = v62 |
| w-lt / w-st proceeds | Form 8949 publishes proceeds 1,000 (Schedule D also required) | Form 8949 and Schedule D blocked on the proceeds subtotal | Form 8949 1,000 (= v62) |
| w-lt / w-st basis, adjustment (with w proceeds closed) | Form 8949 publishes the basis or adjustment 1,000 | Form 8949 blocked on the set's subtotal | = v62 |
| f1099g.1 | Schedule 1 publishes 1,000 | Schedule 1 blocked on `unemployment.box1-subtotal` | = v62 |
| nominee, abp (with box 1 at 2,000 closed) | Schedule B publishes the adjustment row 1,000; line 2b 1,000 | Schedule B blocked on the adjustment subtotal and `interest.taxable-total`; line 2b and AGI absent | = v62 |
| controls: `f1099div.1a`, `f1099int.b1` (not guarded in the candidate) | Schedule B blocked on `dividends.ordinary-total` / `interest.positive-total` | unchanged; line 2b still publishes the partial for b1 (the owner-held gap) | = v62 |

**Complete-return controls.**

- The collect-closure test's complete return (interest, dividends, a 1099-R, an SSA-1099 and
  1099-B sales, every family closed): v62 and scratch v63 both 0 blocked, 240 published
  values, identical, Schedule D published.
- Each guarded set answered (above): identical values to v62, including Form 8949, Schedule 1
  and Schedule B attachments where required.
- Track 1 should pin each of the 13 flipped sets with a v62 case (the existing
  `test_known_gap_schedule_d_attachment_still_publishes_the_partial_amount_on_v62` covers lt
  proceeds) and add a v63 case for each, plus a pinned live block for each of the 11 held sets.

## 5. Decisions to carry to the owner

1. **Eight-citizen limit.** 13 are needed. Split 7 + 6 (recommended), or waive for one v63.
2. **Line 2b side effect.** Rows 6 and 7 are the only way to guard the Schedule B adjustment
   rows and they also stop line 2b publishing a partial total for those two sets. Accept, or
   defer rows 6 and 7 with the Schedule B adjustment gap named as held with line 2b.
3. **Seven positive interest subtotals.** Guarding them would close the parked line 2b gap with
   no validator change. New scope; not planned.
4. **The 11 held sets.** Rename the known-gap list for what it is and pin the live blocks, or
   improve the survey to read requirements. The first needs no tool change.

## 6. Stop conditions

- Engine, schema, kernel or expression-operation change needed: **no**.
- More than eight successor citizens: **met (13)**; split proposed above.
- A guard would change a complete return: **no** (scratch v63 identical on every control).

## 7. What was not shown

- The seven positive-interest subtotal guards, and their effect on line 2b, were not run live;
  the two adjustment guards, which share line 2b's reading, were.
- The candidate is scratch: no published-package companion declaration, release evidence or
  checksum review exists for v63.
- One 1,000 member per set; two members, stale closures and corrections follow the same
  `collect` path as the five withholding families the earlier probes exercised.
