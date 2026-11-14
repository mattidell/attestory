# Saved-page reobservation on core v80

After PR262 merged, the branch was synchronized with main (now core v82).
This account observes v80, not v82. The original v79 evidence remains unchanged.
All inputs are synthetic demo cases; generated models/pages/traces stay ignored.

Command:

```sh
python3 tools/sale_page_observation.py --track1-regression --structured-only --core-version v80
```

The corrected ten-case capture used Chrome/156.0.8078.81 on macOS. Every model
adopted core-calculations@v80, published-packages.v78.json and
demo.release.sli-worksheet-integration.2025@v78. Summed coordinator elapsed time
was 30.933 seconds, excluding setup and Chrome. All ten browser contexts and
the browser completed cleanup. These are elapsed observations, not process CPU
or billed CI minutes.

## Input authority and provisional capture correction

V80 adds a distinct no-1099-B source-family question. The first carried v79
inputs left it unanswered: box E/W values and sales attachments blocked, so
that provisional capture did not establish completed v80 cases. The corrected
run uses the committed v80 carry helper, cfp.with_q2(acts, "no"), after each
original scenario. This records the true synthetic absence of the new families;
it does not answer or refresh the original unanswered/stale noncovered claim.

Q2 is tax.us.2025.f8949.no1099b-sold.source-closure, version v1, explicitly no.
Actual Q1 is tax.us.2025.f1099b.noncovered-sold.source-closure, version v1.
The raw corrected capture's source_question.key still named the older in-class
fact: that metadata label is not authority. The model's actual source-closure
pins establish Q1; the tool was corrected to emit its actual key in subsequent
captures. Original source acts and the retained DOM were not relabeled.

## What Chrome displayed

| Case | Principal observation | Relevant attachment state |
| --- | --- | --- |
| mortgage-1098 | Special mortgage amount 4000; line12e 15750 | Schedule A not required |
| covered-long-term-sale | Schedule D8a 4000 | Schedule D published; Form8949 not required |
| noncovered-box-e-sale | Schedule D9 4000; box E d/e/g 6000/2000/0 | Schedule D and Form8949 published |
| wash-sale-code-w | Schedule D9 -2000; box E d/e/g 4000/7000/1000 | Schedule D and Form8949 published |
| covered-basis-not-reported | Covered line blocked with the noncovered-sale instruction below | Schedule D blocked; Form8949 not required |
| wage-single-noncovered-no | Schedule D9 closure-backed zero 0 | No required sales attachments |
| wage-unanswered-question | Schedule D9 blocked; actual Q1 appears 36 times | Schedule D and Form8949 blocked |
| sale-answer-needs-reconfirmation | Schedule D9 blocked; stale Q1 appears 3 times | Schedule D and Form8949 blocked |
| mortgage-itemized-declared-boundaries | Mortgage 20000; line12e 20000; missing no-other-line16 | Schedule A blocked |
| mortgage-itemized-complete-scope | Mortgage 20000; line12e 20000; Schedule A subtotal 20000 visible | Schedule A published |

The covered-basis refusal is visible verbatim: “Record this sale as a
noncovered sale. The broker did not report its basis to the IRS.” Missing
Schedule A authority is specifically the no-other-line16 declaration; supplying
that answer distinguishes the complete case from the blocked case.

The Q1 counts come from its actual v80 wording in retained line-local blocked
reasons, not the old v79 string. Q2 occurs zero times in all ten pages after its
explicit no. No dedicated question region is present. Repetition is a finding,
not successful once-only-question behavior.

The line6c instruction and Schedule1 top-entry citation alerts remain visible.
Independent review found no new supported model/DOM discrepancy in this capture
beyond those two historical alert classes. The v80 complete mortgage has an
actual subtotal of 20000: the old v79 subtotal-absence finding does not apply
to that observed v80 page. This is not a claim about all v80 pages or v82.

## Short temporary-path repair and limits

Chrome now uses a uniquely owned private system-temp root, ignoring a long
inherited TMPDIR. An actual one-case v80 Chrome regression passed locally in
21.44 seconds, observing the environment passed to Node, a socket-path allowance
below 108 bytes, context/browser cleanup and removal of the owned root. It is
live-lane and not platform-skipped, so Linux CI exercises the same route.

The earlier immediate SIGABRT is consistent with Chromium's fatal singleton
socket-path limit, not slow startup. Discarded historic stderr prevents direct
proof of that exact abort. Local macOS success is not Linux execution evidence;
fresh exact-head CI remains required. No deadline, retry, budget, production
file, content package or schema was changed by this repair.
