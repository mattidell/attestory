# Track 8 (build part) — demonstration, rendered check, cleanups

Plan sentence 8 as one person's story, a check of the page a person would
read, and two cleanups carried in the plan.

## The story

`tests/test_sli_deduction_end_to_end.py` uses one synthetic workspace. The
filer has 50,000 in wages and 3,000 of interest on Cedar's Form 1098-E. Each
step saves through the real recorder and its reviews and recovers the log
fresh. It then resolves core calculations v41 through its release, runs
`live_coordinate_run`, and runs the coordinator's marshalled context on the
reference runner as well (Track 5's `run_live`). Both runners agree at every
step.

| Step | What the person does | Line 21 | What line 21 says |
| --- | --- | --- | --- |
| 1 | Nothing entered yet | 0 (closed, empty family) | — |
| 2 | Enters Cedar's Form 1098-E | blocked | No student loan is linked to this statement. Say which student loan this statement covers. |
| 3 | Links loan, schooling and statement; answers the two loan questions and the four yes/no questions | **2500** | — |
| 4 | Corrects the statement link to no | blocked | No student loan is linked to this statement. Say which student loan this statement covers. |
| 5 | Restores it | **2500** | — |
| 6 | Changes the enrollment answer to no | blocked | You said the student was not enrolled at least half-time in a degree or certificate program during the schooling this loan paid for. The deduction is worked out here only when they were. If that answer is wrong, change it. |
| 7 | Changes it back to yes | **2500** | — |
| 8 | Withdraws the loan-to-schooling link | blocked | A link between the loan on this statement and a schooling was withdrawn and not answered again. Say which schooling the loan paid for. |
| 9 | Restores it; the save is interrupted | blocked, identical to step 8 | same as step 8 |
| 10 | Saves the schooling link again | blocked | The loan on this statement has no answer yet to: was the student enrolled at least half-time in a degree or certificate program during the schooling it paid for? Answer that question. A missing answer is not treated as no. |
| 11 | Answers the enrollment question again | **2500** | — |

Every blocked sentence is prefixed with "2025 Form 1098-E from Cedar / Cedar
Servicing".

At each 2500 the line 21 finding pins package v41. Its pins trace through the
run's derived findings to each of the following: the box 1 finding, the
financing and inclusion relationship findings, both loan answers, and the four
retained yes/no answers. The trace also reaches the worksheet, standing and
`sli-statement-loan-support` rules. That last rule declares the four basis
groups. The enrollment-no standing traces to the saved "no" answer. The
financing-withdrawn standing traces to the withdrawal finding.

Step 9 restores the financing link with one `append_batch` of four acts:
evidence, contribution, assertion and retraction. The test crashes while the
third act is written and leaves that line torn. The recovered log equals the
log before the save, and line 21 is unchanged.

Ending a schooling link also ends the enrollment answer whose question referred
to that schooling. Restoring the link does not restore the old answer. Steps
10–11 demonstrate the separate re-answer needed to restore the deduction.

## Rendered check

Each state was rendered with the repository's citation-walk page
(`packages/presentation/pages/citation-walk.v1.html`, filled by
`live_session._render_page` from the `live_coordinate_run` presentation
model). The states were published (step 3), statement link no (step 4) and
enrollment no (step 6). Each page was opened in headless Chromium
(Playwright's `chrome-headless-shell`, driven over the DevTools protocol). The
HTML, DOM dumps and line 21 screenshots are in ignored `temp/track8/`.

- **Published.** The line shows `2500` and its published badge. The citations
  list the synthetic answers.
- **Blocked.** The line shows "No value published — cannot compute." Under
  "Why:" it lists "2025 Form 1098-E from Cedar, Cedar Servicing:" in bold,
  followed by the step's sentence. The page joins the statement and lender with
  a comma; the tests join them with " / ".

Seen during the check:

- Before the renderer repair, a blocked line 21 with a "Why:" list also showed
  the generic blocked sentence and "Remedy: contribute the missing dependency
  to unblock this line", which contradicted the specific sentence when the
  person had answered. The repair in this track removes both for a line that
  carries reasons. The line "Missing dependency code(s): DEPENDENCY_INVALID"
  remains and is carried in the retrospective.
- An unrelated "Lump-sum election" section on the same page shows "This line
  is missing its rendering instruction for the declared disposition." It also
  appears on `main` and is carried in the retrospective.

## Cleanups

- The applicability marker's value,
  `INCLUSION_APPLICABILITY_UNESTABLISHED_VALUE`, moved from
  `packages/derivation/marshal.py` to `packages/tax/sli_relationship_recording.py`
  beside its type constant. `marshal.py` imports it at its one use.
- Worksheet v2 was superseded before publication and is not part of the
  published history: no registry, package or release names
  `(tax.us.2025.rule.sli-worksheet, v2)`. Track 5's docstring names v3.

## Removed-statement boundary

The live integration tests also remove a statement while its saved inclusion
remains current. Package v40 loses that unresolved inclusion when a supported
second statement remains: it can calculate from the second statement alone.
The successor package v41 uses worksheet v4 and an explicit per-marker refusal
rule, so unresolved inclusions are checked even without a current statement
subject. The remaining statement keeps its supported result; the aggregate
deduction blocks. The saved presentation names the removed statement and
copies the adopted applicability wording rather than inventing a tax reason.

## Open questions

1. When a statement link is corrected to no, the standing (`no-loan-link`)
   traces to the statement only, not to the saved "no". The sentence is
   accurate. Pinning the person's no is carried in the retrospective.
2. Resolved in this track: the generic blocked explanation and remedy give way
   to the specific reasons when reasons are present.
