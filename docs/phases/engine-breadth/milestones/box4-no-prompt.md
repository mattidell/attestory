<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "box4-no-prompt",
  "status": "Closed 2026-11-17. Core v94, registry v92, release v92.",
  "retrospective": "docs/milestone-retrospectives/2026-11-17-box4-no-prompt.md",
  "scope": [
    "a filer who answers that a Form 1099-B statement reported no federal income tax withheld in box 4 is not asked for the box 4 amount, and lines 25b and 25d follow from that answer",
    "every recorded return that does not answer that question computes the same numbers"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to how a box 4 'yes' is asked or recorded",
    "repeated shared questions on the page belong to the blocked-sale-pages milestone",
    "the return-level box 4 total and the per-statement/return-level double entry stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/box4-no-prompt.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/box4-no-prompt.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/box4-no-prompt.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/box4-no-prompt.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Box 4 "No" Is Not Asked For an Amount (2025)

Milestone key: box4-no-prompt.
Branch: milestone/box4-no-prompt-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-16.
Starting point: main at `258afd0e` (core v93, registry v91, release v91).
Expected target: core v94, registry v92, release v92.

## What we are trying to accomplish

A filer with a Form 1099-B sale answers, per statement, whether box 4
reported federal income tax withheld. Answering "no" today does not
finish the job: Form 1040 line 25b still blocks on the box 4 amount and
the page keeps showing the amount prompt ("If box 4 is blank, enter
$0") until the filer also enters $0. The filer has already told us the
answer. The useful outcome is that a "no" lets lines 25b and 25d
compute with nothing withheld from that statement, and the amount
prompt is shown only where an amount is actually needed.

## What we know

- box4-amount-asked P0 (`box4-amount-asked-evidence/p0.md`) observed it
  on core v91: lists that answer
  `statement-box4-withholding-reported` "no" with no amount block line
  25b `DEPENDENCY_ABSENT` on `f1099b.statement-box4-withholding`; line
  25b v8 does not read the yes/no. Entering $0 publishes line 25b as 0.
- Three recorded lists (`codeb_amounts_disagree`,
  `codeb_sale_beside_8949_yes`, `wash_adjustment_open`) answer "no" with
  no amount; they also block elsewhere.

**What we do not know.** Whether the defect still reproduces on core
v93; exactly what the yes/no question asks and whether a "no" truthfully
means $0 for that statement; which rule should read it (line 25b, the
per-statement amount pairing, or a derived zero); how a "no" with an
amount also entered, or a "yes" with no amount, should behave; and
whether content alone can do it without changing any other answer's
requirements.

## Actions the team will take

1. **P0: reproduce, trace and design** on published v93 and a scratch
   successor.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1 build.**
5. **Fresh review, repair, close.**

## Cases that will shape the design

Synthetic `demo.*` act lists on a wage return with one or two Form
1099-B statements carrying a sale: box 4 answered yes with an amount,
yes without, no without an amount, no with $0, no with a nonzero amount
(a contradiction), and unanswered; two statements with mixed answers;
the return-level "no sale box 4 present" answered yes and no; a return
with no Form 1099-B as the neighbour; single, joint and separate filing.

## P0 result

P0 completed on published core v93 and a scratch v94 successor. Evidence:
`box4-no-prompt-evidence/p0.md`, scripts and JSON outputs. No production,
test, engine, new schema, projection, page or kernel edits.

All 48 focused live cases complete. A statement-level no without an amount
now computes lines 25b/25d and removes the per-statement amount prompt;
yes and unanswered retain the amount requirement. Explicit amounts take
precedence over a contradictory no. The final content design adds 17
helper rules and a vocabulary bundle and retains the original pairing as
the fallback in a line-25b successor, preserving unresolved-family behavior.

The final 775-list replay has 420 identical successes, 84 identical errors
on both cores and 271 no-without-amount changes, with no unexpected change.
All numerical line values, refusal codes, attachments and tax bases remain
identical. The 271 changes expose the already-required return-level question;
they do not compute 25b/25d because that older corpus leaves it unanswered.
The three named recorded examples in the focused matrix already answer
it and do compute 25b/25d. That qualifies the original expected numerical
unblocking without changing the parked return-level question.

The initial two-core replay took 1390.389 seconds; the final successor pass
reused its unchanged v93 pins and took 744.465 seconds, using 9 workers.
The retained part supports Track 0 reuse. Recommendation: Track 0 on the
final content design. Foreman decisions are explicit-amount precedence,
content cost, the partial-return replay distinction and independent closure
of statement isolation and correction/withdrawal before a production build.

## Decisions

Foreman, 2026-11-16, on P0 (`box4-no-prompt-evidence/p0.md`).

1. **Design.** Build P0's content-only shape: per-subject helper rules
   that count, for each Form 1099-B sale statement, whether its box 4
   amount is still needed (0 when an amount is recorded or the statement
   answered "no"; 1 for "yes" or unanswered), a return-level selection
   that sums them, and a line 25b successor that skips the sale pairing
   only when that sum is zero and otherwise runs the original
   `require_paired` expression unchanged. No schema, engine, projection,
   page or kernel change.
2. **Contradiction.** A recorded amount wins over a "no" on the same
   statement: the amount is what the statement reports, and dropping it
   would silently lose a tax payment. A "no" counts only when its
   statement has no amount.
3. **The 271 next-question changes are expected.** On those recorded
   lists line 25b stops waiting on the per-statement amount and waits on
   the return-level "statement with no sale" question, which was always
   required and stays unanswered there. No value, disposition or refusal
   code changes. The return-level question and total stay as they are
   (parked); nothing defaults them.
4. **Content cost.** Seventeen helper rules are accepted. Track 0 may
   propose a smaller admitted shape, but only if it keeps statement
   locality and the original fallback; it does not block on finding one.
5. **Statement naming and repeated page questions** stay with
   blocked-sale-pages; this milestone edits neither.
6. **Track 0** closes mixed statements, repeated sales on one statement,
   correction and withdrawal, all eight sale subject types, and the page
   sentence a filer sees next, reusing P0's replay.


## Track 0 adversarial closure

Builder examination completed on P0's unchanged final scratch successor.
Evidence: `box4-no-prompt-evidence/track0-closure.md`, track0.py and
track0-*.json. Gate result: **FAIL**, item 6 only; no charter stop condition.

The 41 mechanical cases pass, including mixed two/three statements,
reversed order, repeated sales on one statement, no+200 precedence,
yes+zero and each of the eight sale types. Three lifecycle traces pass:
correction/retraction restore the amount prompt and displace prior payment
findings through their pins; a new amount after no recomputes and pins it.
Nine computing neighbour pairs have all 86 page fields equal v93 (774
field comparisons, no differences or added questions). Optional smaller
shape was not pursued. The 775-list P0 replay is reused with matching
fingerprints and content bytes, with no corpus rerun.

**F1, content wording:** on a mixed return the published amount prompt says
to enter box 4 for each statement, including a no already sufficient and
an amount already entered. Its v93 witness matches, but it fails item 6's
criterion. The closure report proposes input-question successor wording
that excludes recorded amounts and satisfied no answers; no content was
edited here. The return-level no-closed-sale question and amount wording
are truthful in the tested context and remain parked and unchanged.
Recommendation: foreman disposition of F1 and a narrow content repair
before Track 1. New adopted wording would require a new parallel replay.

A separate measured limit is recorded: adding an amount does not displace
old zero payment findings on either v93 or v94, although fresh pages
compute correctly. This is not a prototype-only regression; the v93 base
control is in track0-addition-control.json. The item-4 PASS claims actual
correction/retraction displacement and fresh-run amount precedence, not
addition-triggered invalidation. The foreman may route that common
freshness boundary separately without confusing it with the wording fix.

## Track 0 disposition

Foreman, 2026-11-16, on `box4-no-prompt-evidence/track0-closure.md`.
Items 1-5, 7 and 9 pass; item 8 (smaller shape) was not pursued, so the
17-helper shape stands (Decision 4).

7. **F1 (item 6) is repaired in Track 1 with new words.** The box 4
   amount prompt is one return-level sentence that asks for "each"
   statement with a sale, so on a mixed return it also asks for a
   statement answered "no" and one whose amount is already entered. Track 1
   publishes an `input-question.f1099b-box4` successor, same fact and
   answer meaning, with these words:

   > Enter the federal income tax withheld in box 4 of each Form 1099-B
   > or substitute statement you recorded a sale from, except a statement
   > you said shows no federal income tax withheld in box 4 or whose
   > amount you already entered. If box 4 is blank, enter $0.

   They are shorter than Track 0's proposal and keep the published
   "If box 4 is blank, enter $0" instruction. No rule changes. Because
   the question's bytes change, Track 1 replays the recorded lists
   again; the expected classes are P0's, with the amount sentence
   changed wherever it is shown.
8. **Adding an amount after a "no" is parked.** A fresh run computes the
   new amount on both v93 and the successor, but the earlier zero payment
   findings stay current until a run; that is the engine's currency
   behaviour on additions, unchanged by this milestone and outside its
   scope.


## Track 1 result

Builder complete on published core v94, registry v92 and release v92.
Evidence: `box4-no-prompt-evidence/track1-result.md`, track1-*.json, and
new live/package tests. The 19 prototype artifacts are byte-identical;
the v2 box 4 amount question has Decision 7's exact words. Published
citizens and schemas are unchanged; no recording, kernel, derivation,
schema or presentation edit was needed. V94 loader declarations carry
v93 unchanged, with the enumerated-core test extended through v94.

The full 775-list v93/v94 replay took 1408.692 seconds with 9
workers: 295 identical successes, 84 same errors, 125 sentence-only
changes and the accepted 271 next-question changes. No numerical value,
row disposition or refusal code changes; no unexpected changes. The nine
computing neighbour pairs have 774 page-field comparisons with zero
differences, in 34.651 seconds.

Eight distinct live cases and seven fast package tests cover the charter.
Both new modules passed with unrelated evidence first on PYTHONPATH.
Targeted runs passed 34 initially, then 14 for the static-gate repair and
7 for final package import isolation. Final fast lane: 1823 passed,
8 skipped in 15.48 seconds. Mypy: no issues in 507 source files. The
required github/main..HEAD envelope scan passed. CI verify remains the
full-suite gate; this is not a merge/publication decision.

Deviation: the first fast lane required 16 exact new helper rule/version/
symbol entries in tools/required_versus_read_allowlist.json. Their
subject dependency supplies dispatch identity rather than a sale value
read by the expression. Explicit reasons and a package test were added;
no checker code, accepted content bytes or recording changed. The final
fast lane is green. Decision 8's addition-only currency behavior and the
parked return-level question remain unchanged.

## Review disposition

Foreman, 2026-11-17, on `docs/reviews/box4-no-prompt/review.md`. No
product-behaviour finding; the reviewer's own live runs, Chrome pages and
ten-list replay agree with the build.

9. **F1 (blocking) is the draft gate, not a defect.** `verify` refuses a
   draft PR by design; the curated head is marked ready and merges only on
   a green exact-head `verify`.
10. **F2 (should-fix) is repaired.** `classify.py` rejects any changed
    value, outcome, disposition, refusal code, or added or removed row
    before it assigns an expected label, and permits only line 25b's
    missing name moving from the statement amount to the return-level
    question and the exact amount-question substitution. Mutation tests
    exercise it, and the 775-list classification is rerun from the saved
    replay (live only if the saved pins do not hold the rows).


## Review repair

Builder completed the Decision 10 classifier repair. Every row is compared
before an expected label is assigned; added/removed rows and changed values,
outcomes, dispositions or codes are rejected. Only the specified missing-name
transition and whole amount-question substitution are permitted, including
the presentation's alphabetical sentence ordering. All five mutation checks
return `unexpected`, and all 775 saved Track 1 pairs retain their labels:
295 identical successes, 84 same errors, 125 sentence-only and 271 accepted
next-question changes. Strict counters report zero value, nonpayment,
disposition/code, added-row or removed-row changes. The replay was reused;
classification took 55.963 seconds (original live replay: 1408.692 seconds).
Evidence: `box4-no-prompt-evidence/repair-*.json` and `check-classifier.py`.
The fast lane passed 1823 tests with 8 skips in 16.08 seconds. No tests Python
changed, so mypy was not required by this charter. The required
`github/main..HEAD` envelope scan passed. No content, package, loader or
production files changed; no push or spawn. CI verify remains the publication
gate under Decision 9.

## Closeout

Closed 2026-11-17. Retrospective:
`docs/milestone-retrospectives/2026-11-17-box4-no-prompt.md`. The repair
was not re-reviewed: it touched only evidence (`classify.py` and its
mutation check), and the foreman read the strict comparison and the
unchanged reclassification. The review's F1 clears with a green
exact-head `verify` on the ready PR.

Parked: an amount added after a "no" leaves earlier zero payment
findings current until a run (Decision 8). Unchanged: the return-level
box 4 question and total, and the box 4 questions not naming their
statement.
