# Fresh-reader review: box 4 no prompt

Reviewed committed `HEAD` `8cac2c5e6daf0c6516e3f318c83689c20ef001db` on
`milestone/box4-no-prompt-2025`, against `github/main`
`258afd0e0d0a844afd850eef4d1f81591b844cba`. The orientation SHA matched
Git. After fetching, the derived ratified line was `origin/main`, at the
same baseline: 0 behind, 16 ahead, no merged PR for this branch. The
charter/plan commits are administrative context, not implementation evidence.

The reviewed box accepts current, statement-identified 2025 sale facts,
box 4 amounts, and the person's yes/no answers through the adopted package.
It determines whether each sale's statement needs an amount and guards
line 25b; the existing withholding subtotal supplies the money. A derived
requirement count is not a recorded zero amount or a closure declaration.
Other years, statements outside the supplied workspace, other withholding
families, the parked return-level question, and addition-only currency
behavior remain outside this change's claim.

## Findings

### F1 — blocking: the required publication gate has not run

Location: `.github/workflows/ci.yml:162`; measured candidate check on
[PR #282](https://github.com/mattidell/attestory/pull/282).

Reproduction: `gh pr view 282 --json isDraft,headRefOid,statusCheckRollup`
and `gh run view 44021740188 --log-failed`. On the reviewed SHA, `quick`
passed, `precheck` and `suite-shard` were skipped, and `verify` failed at
the explicit draft gate. Its log says the full suite has not run on this
head. This is an administrative gate failure, not a measured test failure.
The semantic checks below do not replace the required green check.

Fix: the foreman should mark the existing PR ready and obtain a successful
`verify` on the candidate to be published. Reference that check before
publication. No content repair is indicated by this finding. The reviewer
did not change PR state, push, or run the suite.

### F2 — should-fix: expected replay labels admit forbidden changes

Location:
`docs/phases/engine-breadth/milestones/box4-no-prompt-evidence/classify.py:65`
and `:69` (the summary counter at `:90` also omits added/removed rows).

Reproduction: evaluate the committed classification branch with two pins
that differ only in line 25b's disposition or refusal code. Removing that
row before comparison labels either difference
`line25b_dependency_route_only`. With a statement in
`facts['no_without_amount']`, changing a line value from 0 to 999 instead
receives `no_without_amount_changed`. I executed those three mutations
against the branch extracted from the committed Python AST. These labels
therefore do not establish the promised absence of value, disposition, or
code changes. The separate counters catch the common-row examples, but
their list-only condition skips row appearance/disappearance.

The current committed detailed classification reports zero value and
disposition/code changes; the independent ten-list replay below also found
none. This finding is about the strength of the evidence classifier, not
an observed tax computation defect.

Fix: reject changed values, outcomes, dispositions, codes, and unexpected
row additions/removals before assigning an expected label. Permit only the
enumerated missing-name transition and exact question substitution. Keep
the separate measurements and exercise the classifier with those mutations.

## Verified behavior and limits

**Meaning and content.** Read the published yes/no question, amount
questions v1/v2, all sixteen helpers, the selection, vocabulary, and line
25b v9. The eight count rules and eight needed rules respectively have
identical structures after substituting their sale subject names. The
question asks whether the identified statement shows withholding. A
truthful no supplies no withholding from that statement; it says nothing
about another statement or an incorrect document. The local source hashes
match the evidence: `i1040gi-2025.pdf`, page 39, line 25b;
`i1099b-2025.pdf`, page 12, box 4; and `f1099b-2025.pdf`, page 7,
recipient instructions. Those passages concern carrying reported federal
withholding, including backup withholding, to the return.

The v2 amount question is exactly Decision 7 and retains the blank-box
instruction. Its exception describes the subset of statements already
satisfied; it does not assert that every return contains a no answer.
It remains truthful on yes-only, unanswered, and mixed returns. An entered
positive amount wins over a contradictory no, as decided. Line 25b's value
expression is unchanged. Its original sale `require_paired` expression is
structurally identical in the new fallback; the other guard arms are
unchanged. The bypass applies only when every dispatched sale is satisfied.

**Independent live checks.** Ran twelve valid synthetic lists on the real
coordinator and published v94, plus one deliberately invalid year input.
Read the saved presentation models and disposition ledgers. The twelve
covered one no; yes without amount; mixed no/unanswered; that mixed return
after entering 200 on the unresolved statement; two sales on one statement
with one 200 amount; no with 200; a noncovered long-term no; unanswered
return-level question; no 1099-B; correction to yes; retraction; and a
mixed-family return with an additional unresolved statement.

- One no publishes 25b = 0, 25d = 4500, 33 = 4500 and 37 = 0, with no
  amount sentence on any of those four lines.
- Yes/unanswered statements block 25b on the amount fact type with
  `DEPENDENCY_ABSENT`. One statement's no does not satisfy another,
  including a different sale family. Entering only the unresolved
  statement's 200 completes the mixed return: 25b = 200 and 25d = 4700.
- Two sales sharing one statement and one amount publish 200, not 400.
  No plus 200 also publishes 200. The wage fixture actually contains 4500
  withholding, so these hand totals follow from the recorded facts.
- With the return-level question unanswered, all four payment-related
  lines show that existing question, rather than the statement amount
  sentence. Nothing defaults the parked answer.
- A 2024 key on the 2025 answer is rejected with `FindingModelError` at
  admission. Declared joins include statement and year; the schemas admit
  only 2025 here. Helpers read the provided workspace's current sources,
  not other workspaces. They add no independent real-world filer identity
  inference; statement ownership remains an input responsibility.

Chrome drew three saved pages using the headless draw helper from
`tests/test_page_alerts_v92.py`: one no, yes without amount, and mixed
no/unanswered. The drawn sections confirm the saved-model observations on
25b, 25d, 33 and 37. The blocked pages retain both the exception clause
and the blank-box instruction. Repetition across lines remains parked.

On production v94, a separate publication-history check established that
both earlier payment findings transitively pin the no finding. Correcting
it to yes and retracting it each displace the source and both old payment
findings. Fresh pages restore the amount sentence. I do not claim that
adding a new amount invalidates old results; Decision 8 explicitly parks
that existing limitation.

**Compatibility and publication bytes.** Independently compared ten lists
through `tools.recorded_replay.replay` with five worker processes, two from
each recorded set. Selected keys:

```text
v81/case/a_8949_yes
v81/case/a_q3_no_with_member
v82/p_covered_st_only2a_yes_nolosses_yes/honest
v82/b4_yes_covered/honest
v83/track0/s1/d2_mixed_statements
v83/track0/s0/b4_amount_no_answer
v84/late/late_new_statement_unanswered/1
v84/authority/alc_closed_empty
v85/surface/surface_blocked_sale_box4
v85/authority/alc_double_count
```

Results: three identical, five sentence-only, two expected next-question
changes. No line value, attachment, tax-base, disposition, or refusal-code
change in these comparisons. The two changed rows remain blocked with
`DEPENDENCY_ABSENT`; only their missing name changes from statement amount
to the existing return-level question. The computing no-1099B page also
matches all 86 prior v93 field states. The full 775-list figures are
committed evidence, not a newly rerun corpus: 295 identical successes,
125 sentence-only, 271 next-question changes and 84 same errors. F2 limits
what its classification names alone prove.

Verified the core retains every other member row and property; only the
old question and line 25b versions are replaced, with the eighteen new
helper/vocabulary members added. Entrypoints replace the question and add
the vocabulary. The core checksum and all twenty new citizen checksums
match. Registry v92 retains every v91 entry and adds twenty citizens and
one package. Release v92 is the exact registry-hash/version successor.
No pre-existing content file was edited. V94 companion declarations and
covered-flag maps equal v93. The loader diff adds only v94 support. The
kernel, derivation, schemas and presentation diffs are empty. All sixteen
allowlist additions name the exact rule version and its required subject;
their expressions use dispatch identity rather than the sale's value.

**Test review.** The eight live cases are distinct and correctly named;
`second-subject-no` really uses noncovered long-term sales, and
`mixed-no-unanswered` really has only the first statement's box 4 answer.
No new live case merely duplicates another's state. The new modules do not
classify sentences by punctuation: they compare complete sentences. The
inherited replay harness does use a question-mark bucket, but additionally
retains blocked reason sentences, including this non-question amount
instruction. Direct grep found the real `live_coordinate_run` entry and
no `RunContext` shortcut in the new tests. Evidence imports go through
`tests/evidence_loader.py`; bare prototype/probe siblings are bound by path
before the parent harness loads.

The package hash/manifest tests would pass a semantically wrong prototype
copied faithfully into production: they establish identity and publication
integrity, not tax semantics. The live cases provide that separate check.
The permanent live assertions cover 25b/25d rather than 33/37 or browser
drawing; this review independently checked those additional surfaces.
No specific failing pytest claim arose, so no pytest command was run.

**Safety.** Both `python3 tools/envelope_scan.py --range github/main..HEAD`
and the standing `--range main..HEAD` scan exited successfully. A direct
scan of every changed committed file found no local absolute-path patterns.
Only synthetic demo facts were used. No governance files were read.

Verdict: **not ready**. Blocking list: **F1**. No product-behavior blocker
was found; F2 is a should-fix evidence-strength finding.
