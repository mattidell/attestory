# Review: age and blindness asked (core v88, registry v86, release v86)

Reviewer, fresh reader. Charter: `docs/reviews/age-blindness-asked/charter-review.md`.
Object: `github/main` (080d2758) `..` HEAD (`7f460a3f`) on
`milestone/age-blindness-asked-2025`. Orientation block verified at
`7f460a3f6f0e8184907d7f7eaa2ccf43e52bdcb2`. Governance not read.

The box: five yes/no facts may enter (taxpayer age, taxpayer blindness,
spouse age, spouse blindness, and the separate-return condition). Each is
usable only as the filer's answer. Core v88 may publish Form 1040 lines
12e, 13b, 15 and 16, and Schedule 1-A lines 36a and 36b, from those
answers. The dependent worksheet's earned-income path, beyond the box
count age and blindness already feed, stays outside. Recorded returns keep
the numbers their records already imply once the new facts are answered
false.

Runs below are published core v88 (registry v86, release v86) through
`age-blindness-asked-evidence/track0.py` `execute`, which calls
`live_coordinate_run` and reads the presentation model. Wages are 50,000.
Hand taxes use the 2025 Tax Table method: tax on the midpoint of the $50
band, half a dollar rounded up. Brackets used: 10 percent through 11,925
(single and married filing separately), 23,850 (joint and qualifying
surviving spouse), and 17,000 (head of household); 12 percent above that.
Schedule 1-A's $6,000 is unreduced because 50,000 is under both phaseout
floors (75,000, and 150,000 on a joint return).

## Findings

### F1 (should-fix). A separate return still asks spouse age and blindness after the condition is no

- **Where.** `packages/content/tax/2025/rule.dependents-worksheet-line-1.v2.json:108`
  (the separate-return `conditional_dependency_set`, condition true, members
  include both spouse facts) and `:229` (spouse boxes add 0 unless
  `spouse_separate_condition` is yes). The same symbol names appear in
  `rule.form1040-standard-deduction.v3.json` only inside the note; that rule
  reads the box count. `rule.schedule1a-part-v-line-36b.v2.json` reads
  spouse age only on a joint return.
- **Claim.** A question is asked where its answer can change a number. On a
  separate return the spouse's boxes count only when the condition is yes,
  and the spouse's senior deduction is published only on a joint return.
- **Consequence.** The return stays blocked on two answers that cannot move
  lines 12e, 13b, 15 or 16. Fail-closed, so no wrong number is published.
- **Reproduction.**

  ```python
  t = <load age-blindness-asked-evidence/track0.py>
  core = t.probe().harness().Core("v88", "v86", "v86")
  acts = t.build_acts(t.MFS, t.answers_for(t.MFS, False, False, None, None, condition=False))
  r = t.execute(core, acts, "demo.review.mfs-condition-no-spouse-blank")
  ```

  Result: outcome success; line 12e, 15 and 16 `blocked`; line 13b `0`;
  asked `spouse-over-65` and `spouse-blind`; missing those two symbols and
  the worksheet box count. The same spouse, age yes and blindness no, with
  the condition yes, publishes 12e 17,350, 13b 0, 15 32,650, 16 3,683. With
  the condition no it publishes 12e 15,750, 13b 0, 15 34,250, 16 3,875, box
  count 0.
- **Fix.** Keep the taxpayer's two facts and `spouse_separate_condition`
  required on every separate return. Nest `spouse_over_65` and
  `spouse_blind` in a set whose condition is the condition fact, so a no
  publishes the box count without them. Rebuild line 1 from `prototype.py`
  so the byte-identity check still holds. This narrows the always-active
  set Decision 9 recorded; the foreman can keep that set and close the
  finding.

### F2 (note). The 775-list replay is expensive as a per-PR test, and its v81 exemption does not pin v87

- **Where.** `tests/test_age_blindness_v88.py:338` (`_fixture_diffs`) and
  `:412` (`test_recorded_returns_match_their_fixtures`), pool at `:427`.
  `question-wording-evidence/track0.py` `neighbour_tasks` is the work list.
  `age-blindness-asked-evidence/track0-neighbour.json` records 775 recorded
  lists plus 3 derived, all identical, 84 refusing the same way on both
  cores.
- **What each choice loses.** Keeping the 775 in the live module re-proves,
  on every full verify, that answering the new required facts false leaves
  published numbers in place, including lines outside the 38 hand cases.
  The module pays the 38-case run and then this replay (the charter's
  figure is about 22 minutes on 4 workers). Moving the 775 to committed
  evidence, and replaying one list per source core in CI, loses per-PR
  detection of a drift the 38 cases do not touch. The 38 hand cases are the
  law battery and belong in the live module.
- **v81.** The explanation is true of the code. `implied` answers age,
  blindness, and, on a separate return, the condition, false when the
  record omits them. `_fixture_diffs` then exempts a v81 list only when the
  run errors, or when a watched line the fixture published as a number is
  no longer a number. A number both sides publish still has to match, so an
  age-driven change of 12e would fail. Those fixtures were recorded before
  questions added after v81. Comparing that class with published v87 is
  sound. The live test does not do that comparison: it drops the list. A
  later v88-only error on a v81 list would be exempted. The neighbour
  artifact is the comparison that exists today. This review did not replay
  the 775.
- **Process pool.** Safe. The pool uses the spawn context, so each child is
  a new interpreter and the xdist worker is not forked. xdist's own package
  has no daemon flag; its workers are subprocesses, and a spawn child of
  one is allowed. This test holds one xdist slot and at most four children
  (`min(4, cpu_count - 1)`). The extra processes can oversubscribe the
  machine while the rest of `-n auto` is busy. That is cost, and it does
  not deadlock the pool.
- **Fix.** Leave the 775 as committed evidence. In CI, replay one list from
  each source core. For a v81 list that blocks, assert the published v87
  outcome beside it.

### F3 (note). Two line 16 amounts the charter names are correct and unpinned

- **Where.** `tests/test_age_blindness_v88.py:58` (`TAX`) and
  `age-blindness-asked-evidence/track0.py:81` (the same map).
  `hand_amounts` adds line 16 only when `(status, line 15)` is in that map
  (`track0.py:189`). The judge compares keys the hand dict contains.
- **Measurement.** Qualifying surviving spouse, spouse age recorded yes,
  taxpayer not 65: lines 12e 31,500, 13b 0, 15 18,500, 16 1,853. Separate,
  spouse age yes, condition no: 12e 15,750, 13b 0, 15 34,250, 16 3,875.
  Both line 16 amounts match the tax table above (joint rates for the
  surviving spouse). Neither pair is in `TAX`, so the live judge never
  sees them. The pins that do exist match the runs in the table below,
  including separate-with-condition-yes line 16 at 3,683. The two-box
  dependent pin (12e 19,750, line 16 2,675) is the one-box worksheet result
  plus one more $2,000 box, and the tax on taxable income 24,250.
- **Fix.** Add `("qualifying_surviving_spouse", 18500): 1853` and
  `("married_filing_separately", 34250): 3875` to both `TAX` maps.

### F4 (note). The blindness sentences omit the instructions' alternative statement

- **Where.** `packages/content/tax/2025/input-question.taxpayer-blind.v1.json:7`,
  `input-question.spouse-blind.v1.json:7`, and the matching titles in
  `core_calculations.bundle.v4.json` (taxpayer-blind and spouse-blind).
  The instructions' sentence is `age-blindness-asked-evidence/law.json`
  quote `blindness`: a statement that the eye condition is not likely to
  improve beyond 20/200 or a 20-degree field can be used instead.
- **Measurement.** Both questions, and both titles, state total blindness
  on December 31, 2025, or a certified statement of the 20/200 or
  20-degree test. A filer whose only certificate is the "not likely to
  improve" statement has to decide whether the question names it. The rule
  treats a yes as the checkbox and does not read blindness for the senior
  deduction. The sentences do not promise the $6,000. Decision 7 stands
  beside this: neither the instructions nor Publication 501 says how
  blindness is judged for a person who died in 2025, and these questions
  still state December 31 on every return, including a decedent's.
- **Fix.** Add the alternative statement to both questions and both titles
  on the successor path. Leave the 2025-death case parked, with no hand
  value.

## Answers

1. **Truth of the sentences, by the runs.** Each age sentence matches what
   its rule reads. A yes is the line 12d age box and, except on a separate
   return, Schedule 1-A's $6,000 for that person. The taxpayer sentence
   states the day-before-the-birthday rule, that January 1, 1961 counts and
   January 2, 1961 does not, and that a 2025 death before age 65 is a no.
   That is Publication 501's death-of-taxpayer paragraph and the
   instructions' February 14, 1960 example, applied to a January 1, 1961
   birthday: age 65 is reached on December 31, 2025. The engine stores the
   filer's boolean; it does not see a date. Answered as the sentence says:

   | Case | 12e | 13b | 15 | 16 |
   | --- | ---: | ---: | ---: | ---: |
   | Single, born January 1, 1961 | 17,750 | 6,000 | 26,250 | 2,915 |
   | Single, born January 2, 1961 | 15,750 | 0 | 34,250 | 3,875 |
   | Single, died December 30, 2025, answer no | 15,750 | 0 | 34,250 | 3,875 |
   | Single, died December 31, 2025, answer yes | 17,750 | 6,000 | 26,250 | 2,915 |
   | Joint, spouse 65 only | 33,100 | 6,000 | 10,900 | 1,093 |
   | Separate, spouse 65, condition yes | 17,350 | 0 | 32,650 | 3,683 |
   | Separate, spouse 65, condition no | 15,750 | 0 | 34,250 | 3,875 |
   | Head of household, spouse age and blindness recorded yes | 23,625 | 0 | 26,375 | 2,825 |
   | Qualifying surviving spouse, spouse age recorded yes | 31,500 | 0 | 18,500 | 1,853 |
   | Dependent filer, age yes, wages 50,000 | 17,750 | 6,000 | 26,250 | 2,915 |

   Joint spouse-65 puts the $6,000 on line 36b and 0 on line 36a. The
   dependent row is the worksheet at this wage (line 2 is 50,450, line 4a
   is the 15,750 base, line 4b is one $2,000 box), which equals the chart.
   Schedule 1-A does not exclude a dependent. A separate return publishes
   senior deduction 0, matching the form's "if married, you must file
   jointly" line under Part V. No pinned hand value in
   `tests/test_age_blindness_v88.py` is wrong. F3 covers the two line 16
   amounts the pins skip.

   The four age and blindness fact bodies in vocabulary v4 are identical to
   v3, titles included. The new condition fact's title is the chart
   footnote in statement form. The condition question is that footnote:
   "no income, isn't filing a return, and can't be claimed as a dependent."
   Line 1 reads that boolean only as the separate-return spouse-box gate.
   Publication 501's separate-return test is "no gross income" and "can't
   be claimed as a dependent," and it does not state "isn't filing a
   return." A spouse with no gross income who is filing answers this
   question no, and the boxes stay off. That matches the form instructions
   the rule cites. F4 is the blindness gap.

2. **Who is asked.** Unanswered single and unanswered head of household ask
   the taxpayer's two sentences and no spouse sentence. Unanswered joint
   asks the four and does not ask the condition. Unanswered separate asks
   the four plus the condition; line 36b is already 0. Head of household
   with both spouse facts recorded yes keeps box count 0 and the head of
   household base. Qualifying surviving spouse with spouse age recorded yes
   keeps 31,500, not the joint one-box 33,100. A joint return with spouse
   age yes, changed to separate, blocks on the condition and does not
   publish 17,350; after the condition is no it publishes 15,750 with the
   spouse-age yes still recorded. The same joint return changed to head of
   household publishes 23,625. The stale spouse-age yes does not move the
   number. F1 is the case that is asked where it cannot matter: spouse age
   and blindness after the condition is already no.

3. **What the filer sees.** Each of the five sentences can be answered once.
   The taxpayer age sentence states the January 1 and January 2 examples;
   the spouse age sentence states the day-before rule and the 2025 death
   sentence, and "born before January 2, 1961" already counts January 1.
   The condition sentence is one "is it true that" over the three chart
   conditions. None of the five promises the $6,000, a spouse box on head
   of household or qualifying surviving spouse, or a spouse box on a
   separate return when the condition is no. F4 is the blindness sentence
   being narrower than the instructions.

4. **Immutability.** Measured against `prototype.py`: the five question
   files, line 1 v2, line 36b v2, and vocabulary bundle v4 are byte
   identical, and the prototype's spouse titles match the published v3
   titles. Registry v86 adds eight citizens (the five questions, line 1 v2,
   line 36b v2, vocabulary v4) and core v88. Every v85 citizen and package
   entry is unchanged; nothing is removed. Release v86 differs from v85
   only in `version` and `package_registry_sha256`, and that sha is the
   sha256 of `published-packages.v86.json`. `packages/tax/loader.py` adds
   the v88 companion declaration and the v88 covered-flag refusal entry,
   each the same map v87 carries, and the switch test's version tuple gains
   v88. `git diff --stat github/main...HEAD -- packages/schemas
   packages/kernel packages/derivation` is empty. Two evidence harnesses
   outside this milestone's directory (`f1099b-backup-withholding-evidence/track0.py`
   and `sale-family-audit-evidence/audit_harness.py`) pass the act list
   through `state_taxpayer_facts` with the core version. On v88 that states
   the taxpayer's two facts false when the list omits them. Any other core
   is returned unchanged. That is Decision 6's helper, used so a v88 replay
   can run. It is not an engine, schema, or kernel change.

5. **CI cost.** Answered under F2. The 38 cases belong in CI. The 775
   belong as committed evidence. The process pool inside the xdist worker
   is safe.

6. **The v81 lists.** Answered under F2. The "questions added after v81"
   explanation matches the exemption, and comparing that class with v87 is
   sound. The live test exempts them instead of pinning v87. Numeric
   disagreements are not exempted.

7. **Test isolation.** `tests/test_age_blindness_v88.py` and
   `tests/test_age_blindness_v88_package.py` load evidence only through
   `tests/evidence_loader.py`. Neither assigns another module's attributes.
   The loader keeps evidence copies under the owning test and arms
   `packages.*` so an assignment would be recorded. Nested loads inside the
   evidence files go through `sys.modules`, which that overlay sees while
   the owner is active.

8. **Data safety.** `python3 tools/envelope_scan.py --range github/main..HEAD`
   exits 0. The added lines that mention path prefixes are the evidence
   scrubber's own needles.

The suite was not run. No failing claim needed it. The cases above were
single coordinator runs on published core v88.

## Verdict

**Ready.** No blocking finding. Should-fix: F1. Notes: F2, F3, F4.
