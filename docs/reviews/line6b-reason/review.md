# Fresh-reader review: line 6b reasons

Reviewed committed `HEAD` `e922fb1ce6b15fd899b3d642e091d464e92fef18`
on `milestone/line6b-reason-2025`, against `github/main`. The orientation
SHA matched Git. After fetch, the derived ratified line was `origin/main`
at `279e3455d8273e1ceec477c23e007dc4b4646bef`: 0 behind, 17 ahead,
not spent, with no merged PR returned for this branch. The charter commit
`e922fb1c` is administrative; the reviewed product changes are the ten
questions, core v93 / registry v91 / release v91, loader declarations and tests.

The reviewed box accepts synthetic current-year acts through the real
coordinator and the published package/release chain. It may add display
questions to explanations of currently missing facts. It may not change
answer meanings, calculation, required authority, refusal codes or source
admission. Decision 8 makes these display-only questions; there is no answer
control to certify. Decision 10 permits paired causes to be explained across
line 6b and line 6d. No governance sources were read or interpreted.

## Findings

### L6B-R1 — blocking: territorial-income question narrows its fact

**Location:**
`packages/content/tax/2025/input-question.ss-benefits-scope-no-puerto-rico-or-samoa-income.v1.json:9`.
Compare `packages/content/tax/2025/ss-benefits-scope.bundle.json:201` and
`packages/content/tax/2025/rule.ss-benefits-worksheet.v4.json:2400`.

The question adds the restriction **“income from there.”** Its fact declares
absence of income **of bona fide residents** of Puerto Rico or American
Samoa, without that source restriction. A synthetic bona fide resident with
only mainland-source income can truthfully answer no to the question while
still belonging to the fact's excluded class. Under Decision 8 that no records
`yes` for the absence fact. This is a change in represented meaning, even
though the question itself does not yet record an answer.

**Reproduction:** Start with `complete_ssa("single")` from the committed
`track0.py` evidence, loaded through `tests.test_line6b_reason_v93._evidence()`.
Use `h.say` to set
`tax.us.2025.ss-benefits-scope.no-puerto-rico-or-samoa-income`, then run
`capture(resolve_core("v93"), acts, "demo.review.territory." + value)`.
With every other scope answer held constant, the fresh real runs observed:

| Recorded absence fact | Line 6b disposition | Value |
| --- | --- | --- |
| `yes` (the new question's truthful no in this scenario) | `published_value` | 10,200 |
| `no` (the existing fact's meaning in this scenario) | `guard_inapplicable` | none |

The existing fact has no separate residence or income-source input that
repairs this mismatch. The 2025 instruction, printed page 31, refers to
excluded Puerto Rico-source income; that does not authorize silently narrowing
the existing, broader product scope fact. The SLI sibling explicitly describes
excluded income in its own fact title, so its wording cannot redefine this
SSA fact either.

**Fix:** Make the question ask about the complete existing fact boundary,
without the added source restriction. Keep the fact and rule semantics intact;
use the applicable publication succession procedure for corrected question
content. Include the resident-with-mainland-income counterexample in the
meaning evidence. A narrower fact/rule contract would be a separate decision,
not a words-only repair.

### L6B-R2 — should-fix: source excerpts point to unrelated passages

**Location:**
`docs/phases/engine-breadth/milestones/line6b-reason-evidence/track0.py:57`
and `:75`; generated example:
`docs/phases/engine-breadth/milestones/line6b-reason-evidence/track1-neighbours-questions.json:534`.

The recorded physical line offsets are applied to `str.splitlines()`, which
also splits the PDF extract's form-feed page separators. This shifts the
excerpts. All ten entries in both `track0-questions.json` and
`track1-neighbours-questions.json` carry excerpts from the wrong physical
lines, despite recording the correct source-file hash and a PASS verdict.
For example, the Form 2555 excerpt discusses pension amounts instead of the
exception; the line 24z excerpt begins the Social Security exception rather
than the worksheet prerequisite. The source file itself is intact.

**Reproduction:** On the source text whose SHA-256 is
`6024dc94dd1f545ed6e2068a42ea11859be546e8fe18ec3082021259f9b45ff1`, compare
`text.splitlines()[1980:1985]` with `text.split("\n")[1980:1985]`.
The former reproduces the committed Form 2555 excerpt; the latter contains
the actual Form 2555/4563/8815 exception at physical lines 1981–1985.
There are 29 form feeds before physical line 1981. The same comparison fails
for every catalog entry's recorded physical span.

**Fix:** Apply physical offsets using newline-only splitting, or use checked
page/paragraph anchors, then regenerate and inspect the two source catalogs.
Check that each excerpt contains its claimed passage. This repair does not
require repeating the unchanged live grid or recorded replay. The independent
source read below supplies the correct passages for this review.

### L6B-R3 — note: replay “identical” is equality of selected pins

**Location:**
`docs/phases/engine-breadth/milestones/line6b-reason-evidence/track1_replay.py:50`;
underlying pin: `tests/test_f1099b_backup_withholding_v83.py:163`.

**Reproduction:** Feed that `pin()` two otherwise equal successful result
dictionaries with a line 6b value of zero, changing its field disposition from
`computed_zero` to `published_value`, or changing its field description.
The pins remain equal and `recorded_replay.classify()` returns `identical`.
Those properties are omitted from the pin. Changing a blocked reason to a
sentence without a question mark is detected, however:
`numbers_identical_sentences_changed`.

Thus “775 identical” cannot alone establish equality of every sentence or
field disposition. The helper also inherits question extraction using
`sentence.endswith("?")` in the older harness. These are limitations of the
reused instrument, not observed v93 calculation regressions. The new v93
tests do not classify questions by punctuation. The richer neighbour ledger
and field comparisons, together with the content-only diff, supply the
missing preservation evidence for this change.

**Fix:** Describe the replay result as selected-pin parity and retain its
limits beside the richer neighbour evidence. If complete page parity is
claimed later, compare an explicit complete semantic projection rather than
expanding the present repair into a replay-tooling project.

## Independent checks

### Words, facts and sources

I read the adopted fact declarations, all adopted rules reading these ten
facts, and the actual local 2025 instruction text. The local PDF SHA-256
matches `law.json`:
`c196586433aaa1899719158ecc9df56b60b525090bf122d2b8d8120d7f3b118b`.
The text hash also matches, independently of the incorrect excerpt slicing.

| Question/fact suffix | Source and meaning check |
| --- | --- |
| `no-unsupported-line1-entries` | Worksheet p.32, line 3 includes line 1z. The question names the bounded W-2-box-1-only boundary. |
| `no-pension-annuity-line5b` | Worksheet p.32, line 3 explicitly includes taxable line 5b. |
| `no-traditional-ira-deduction` | p.31 exception directs contribution/workplace-plan coordination to Pub. 590-A. The question names the existing deduction-coordination fact, not a new deduction input. |
| `no-form-2555` | p.31 exception names filing Form 2555. |
| `no-form-4563` | Same exception names Form 4563. |
| `no-form-8815` | Same exception names Form 8815. |
| `no-excluded-adoption-benefits` | Same exception names excluded employer-provided adoption benefits. |
| `no-puerto-rico-or-samoa-income` | Fails the existing fact boundary: L6B-R1. |
| `schedule1-adjustments-scope.no-line24z-writein` | p.32 prerequisite applies to every write-in directed onto line 24z. Its “before completing” qualifier does not exclude a subclass under that passage. |
| `mfs-lived-apart-all-year` | p.31 line 6d and p.32 worksheet line 8 distinguish apart all year from together at any time. Yes maps to the affirmative fact. |

The nine absence facts are required on the nonempty SSA worksheet route and
must equal `yes` for its guard to pass. Their reader is the adopted worksheet
v4. The living-arrangement fact additionally has checked/not-checked line 6d
readers and selects the separate-filer worksheet branch. I compared the
published SSA lump-sum/foreign-benefit questions and SLI and Schedule 1
siblings: the yes/no direction conforms to Decision 8; only L6B-R1 changes
the class the question describes.

### Live placement and Decision 10

Fresh runs used published cores v92 and v93 without scratch-loader inheritance,
real `live_coordinate_run`, projection and saved HTML models: 17 synthetic
lists, 34 coordinator calls, five parallel workers. Cases covered each of the
ten isolated omissions, the MFS scope/living pair, answering scope alone,
answering both, MFS without benefits, fully answered benefits, and present
territorial-income/line24z scope facts. Omissions were verified absent before
and after handover.

Every compared field's disposition, value, active codes, missing names and
terminal roots stayed equal; all compared ledger rows stayed equal. All 29
fields gaining questions were blocked and had the corresponding fact among
their terminal missing roots. No gaining field had duplicate questions. No
published value gained a question. Answers admitting an unsupported scope
remain guard-inapplicable as before; adding words does not promise support
for those circumstances.

With both MFS answers absent, line 6b asks the scope question and line 6d asks
living apart. Supplying scope alone makes line 6b ask living apart too.
Supplying both publishes 10,200 on line 6b and checked on line 6d, with no
questions there. Without benefits, line 6b is computed zero without a question;
line 6d still properly asks living apart and the refund remains 625.

Two saved pages were drawn in headless Chrome using the page-alerts `_dump`
route: the single-filer Form 2555 omission and the MFS paired omission. Their
union covers all 29 gaining fields. Drawn question text matches the saved
models; no generic blocked explanation or remedy supplants it; zero
section-error alerts appear anywhere.

### Preservation, replay and tests

Independent structural comparison found exactly ten added core members and
entrypoints. All other core fields except version/checksum are equal.
Registry v91 retains every prior entry and adds ten citizens plus core v93;
release v91 changes only its version and registry hash. Loader changes add
v93 declarations equivalent to v92 and do not alter earlier declarations.
The changed core-enumeration test includes v93. The diff over
`packages/kernel`, `packages/derivation`, `packages/schemas` and
`packages/presentation` is empty, and no pre-existing published content file
changed.

I sampled the first and last deduplicated list from each recorded set using
`tools.recorded_replay.recorded_lists()` and `replay(...,
neighbour_classify_per_list, workers=5)`. All ten v92/v93 comparisons were
identical pins:

- `v83/track0/s0/b4_amount_no_answer`
- `v83/zero/v80/v80_t2_stage3/recorded`
- `v84/authority/alc_closed_empty`
- `v84/late/late_new_statement_unanswered/1`
- `v85/authority/alc_double_count`
- `v85/late/late_yes_to_no/1`
- `v82/m_empty_exc1_only2a_no/honest`
- `v82/p0_f_two_unrelated_covered/honest`
- `v81/case/a_8949_yes`
- `v81/neighbour/n_w_zero_proceeds`

The committed 253-neighbour result has 160 identical, 90 questions-only and
three same admission refusals; inspection found zero state changes, ledger
differences or placement failures. Its 20 meaning cases and 55 isolated/pair
checks pass their stated predicates. These results support questions-only
placement and fixed-answer parity; they do not answer L6B-R1's meaning
counterexample. The recorded 775-list result separately includes 84 equal
errors (82 FindingModelError, one HorizonModelError, one SourceAuthorityError),
not 775 successful completed returns.

`test_required_v93_cases_once` and the Chrome test take their expected words
from the same prototype dictionary used to generate the citizens;
`test_ten_question_files_are_byte_identical_to_p0` also checks against that
prototype. They would pass with semantically wrong prototype words carried
unchanged into the published content, including L6B-R1. This is why the
independent fact/source read matters. The other package tests establish
adoption and integrity, not natural-language truth.

The named omissions in the new tests really are removed locally and checked
before and after handover; no “unanswered” case is silently answered by the
helper. The fourteen required lists exercise different roots, pairs or value
states; the extra joint-filing list supplies the Chrome boundary check.
I found no redundant live run without a distinct observation. Both the new
module and page-alerts use `pytestmark = pytest.mark.live`. Evidence enters
through `tests/evidence_loader.py`, with the relevant sibling dependency names
bound by path before their parents load. Grep found no `RunContext` shortcut
in the new tests or milestone harness.

The 10,200 hand value follows worksheet lines 1–18 for benefits 12,000,
wages 50,000, and zero other inputs: combined income 56,000; the 85% benefits
cap is 10,200 and is smaller than the other worksheet result. This review did
not rerun pytest: there was no specific failing-test claim to confirm.

### Safety and CI

`python3 tools/envelope_scan.py --range github/main..HEAD` exited zero.
Only synthetic `demo.*` lists were used. The review contains no local-machine
or temporary-directory paths. No other repository file was edited.

At the reviewed SHA, PR [#281](https://github.com/mattidell/attestory/pull/281)
is draft. Its [quick check](https://github.com/mattidell/attestory/actions/runs/43958439778/job/133619086733)
is green; [verify](https://github.com/mattidell/attestory/actions/runs/43958439778/job/133619087503)
is failed at the draft gate, with full-suite jobs skipped. This is the expected
draft state, not a measured product failure; there is no green required verify
record establishing publication readiness yet.

## Verdict

**Not ready. Blocking: L6B-R1.** L6B-R2 should be repaired in the source
evidence; L6B-R3 is an instrument limitation to retain. A bounded repair can
reuse the unchanged structural, placement, replay and Chrome evidence above,
with the changed wording and its meaning checked again. Publication also
requires the ordinary green `verify` gate on its final candidate.
