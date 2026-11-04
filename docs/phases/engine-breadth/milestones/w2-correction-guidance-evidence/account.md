# P0 evidence: when a W-2 correction has no usable result

A person who corrects W-2 wages needs to know whether the new amount was saved,
whether the calculation produced the requested figures, and whether current
calculation authorization is recorded. The route records these facts in
different places, but its top-level screen status is only “complete” or “not
complete” and it omits authorization status.

The probe at [probe.py](probe.py) exercised the actual EntryLoopServer
HTTP routes. Accepted submissions went through apply_contribution_batch,
the workspace ActLog, and live_coordinate_run. It then reopened the act log
and read the saved report and presentation. Its values and identifiers
are synthetic. For the one blocked case, it omitted one answer from a copy of
the committed v70 seed and resequenced that synthetic log; it did not alter the
fixture. The server used a temporary static placeholder, so the page copy below
is traced from the committed EntryPage.svelte, not from a browser session.
The captured results are in [probe-output.json](probe-output.json).

## What the paths show

### A successful v70 correction can be saved and computed without current authorization

The probe first posted a malformed amount. The route returned HTTP 422 with a
field-specific instruction to enter a positive dollar amount, allowing comma
grouping, an optional $ prefix, and at most two decimal places. The page shows
that response under “Check this entry.” The log revision and act count both
stayed at 293. This rejection already has a useful reason and a next step.

It then entered synthetic wages of $90,000 and corrected them to $91,000. Both
submissions returned HTTP 200. Reopening the log recovered two W-2 Box 1
contribution values, 90000 and 91000; the correction response shows 91000 as
the current answer. The latest saved report had no blocked dispositions and
the snapshot said complete: true. The page therefore says “Your entry is
complete,” “0 missing facts · fully computed,” and that the correction landed
through a contribution. The saved presentation also projects line 1a as 91000.

That saved report also says current: false and
authorization_status: AUTHORIZATION_ABSENT; the saved presentation repeats
that status and admitted: false. No grant is recorded. The displayed amount
and calculation are real outputs, but the page does not show the separate
authorization state. The useful next step is to make that missing status
visible and identify the authorization workflow for anyone who needs a current
result; this W-2 entry screen exposes no such action. The figure itself should
remain a calculated result, not be turned into a calculation error.

### A saved correction can leave other lines blocked

The normal v70 seed produces a fully computed result after Box 1 entry, so its
ordinary W-2 correction does not expose a saved-but-blocked result. To
exercise that boundary, the probe omitted the synthetic answer for whether
the taxpayer can be claimed as a dependent, then entered $90,000 and corrected
it to $91,000 through the same HTTP and recorder path.

The response accepted the correction, and reopening the log recovered both
amounts. The final report records a completed run (stop_reason: saturated)
with DEPENDENCY_ABSENT dispositions. Its line-12e rule names the missing
calculation symbol demo.form1040.standard_deduction; the line 15 and 16
blocks follow from that. The entry snapshot has no missing W-2 id, but says
complete: false; lines 15, 16, and 12e have computed: false and value: null.
The presentation has the blocked disposition and active code
DEPENDENCY_ABSENT, but no reason sentence. It does not identify the omitted
dependent-status answer in person-facing language.

The current page does not preserve that distinction. Any incomplete snapshot
gets the headline “One document closes the gap” and the status “1 missing fact
· W-2 Box 1,” even though this correction was saved and missing is empty.
Blocked expected-impact lines say “Waiting for W-2.” The untouched comparison
row for line 12e formats its null value as $0.00. Thus the screen points back
to wages that are already recorded and can display a blocked figure as zero.
The next action cannot be made specific from the screen: it should not ask for
the W-2 again, and the entry layer currently has no person-facing link to the
separate dependent-status question.

The controlled omission is an evidence probe, not a claim that the normal v70
fixture currently reaches this case. The engine report exposes a missing
derived symbol, while the source answer omitted by the probe is a different
identifier. Connecting those to an existing question remains unestablished.

### v6 keeps its existing successful correction behavior

The same real route accepted a v6 first entry and correction. It recovered the
two W-2 contributions, changed the expected-impact lines 1a, 9, 11, 15, and
16, and held comparison lines 2b, 3a, 3b, and 12 steady. Its saved result also
reported AUTHORIZATION_ABSENT separately from the computed figures. The v70
profile instead exposes lines 11a/11b and 12e. No change to either profile is
supported by this evidence.

## Where useful reasons exist—and where they do not

The rejected-input path already returns a concise, actionable message and
does not append to the log. For calculation, live_coordinate_run saves
blocked codes and missing dependency symbols in its report, and the
presentation can carry a blocked code plus optional reason sentences. In the
demonstrated missing-answer case, the presentation has only the generic
DEPENDENCY_ABSENT code; the report names a derived symbol, not a question.
The entry projection then reduces each line to its title, computed, value,
group, and change. It drops the blocked code, any reasons, and the report's
authorization fields before building the browser snapshot.

The neighboring CorrectionRuntime shows a narrow vocabulary for a different
workflow: not-saved, saved-not-calculated, and saved-and-calculated, with
redacted refusal sentences. That is useful evidence that the save boundary can
be stated explicitly. Its token outcomes live in an in-memory map, however, so
it is not a durable W-2 recovery design to copy.

The main code paths are [entry_loop.py](../../../../../packages/derivation/entry_loop.py#L809)
for calculation, projection, contribution admission, and append;
[live.py](../../../../../packages/derivation/live.py#L766) for the durable report
and presentation; [EntryPage.svelte](../../../../../packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte#L102)
for the current messages; and
[presentation_projection.py](../../../../../packages/derivation/presentation_projection.py#L576)
for blocked rows and optional reason sentences. The comparison is
[correction_session.py](../../../../../packages/derivation/correction_session.py#L1154).
The focused tests in [test_entry_loop_t1.py](../../../../../tests/test_entry_loop_t1.py#L746)
were inspected but not run; the executed evidence is the standalone probe.

## Design alternatives for the next decision

1. **Project existing outcomes into the entry response.** Preserve the
   accepted/saved state, calculation disposition, and authorization status as
   separate entry fields. For blocked lines, show an existing reason sentence
   when one is present; otherwise use a bounded “another required answer is
   missing” message without inventing a tax explanation. This is the smallest
   path: entry snapshot shaping and page copy, using the existing report and
   presentation, with targeted tests. Its unresolved cost is mapping the
   missing calculation symbol to the exact next question; the probe does not
   establish that connection.

2. **Add an entry-level correction outcome record.** Record and recover a
   bounded result such as saved/not saved, calculated/not calculated, and
   current/not current, with a retry action only where supported. This makes a
   lost response and later recovery explicit, but adds a second outcome
   record beside the authoritative act log and saved live outputs. This is the
   larger path: it requires decisions about identity, replay, recovery, and
   retries, plus tests for each boundary. The P0 evidence does not show that
   this extra record is needed for the current loop.

Do not map every engine code to a question. The demonstrated code does not
name the omitted answer, and an internal fault must not become a prompt for the
person to answer. If the selected design needs a tax-content or published
schema change to identify a missing answer, this charter's stop condition
applies.

## Track 1 refinement: the blocked result has no question link

I checked the saved v70 report and presentation path before choosing the
entry-layer projection. For the controlled line-12e block, the report records
`DEPENDENCY_ABSENT` and the missing derived symbol
`demo.form1040.standard_deduction`; it does not carry a source-fact or question
identifier. The dependent-status fact omitted by the probe is a different
identifier, known to the probe because it removed that seed assertion. The
presentation row has the line label, blocked disposition, and active code, but
no reason sentence or question link. The presentation projector adds a
person-facing sentence only for its existing, narrowly declared selection or
source-closure cases; neither connects this dependency block to the omitted
answer. The entry layer must not treat the probe's controlled omission as a
general mapping.

The source fact exists in the current tax vocabulary, but that alone is not a
question connection: neither the blocked report nor its presentation names
that fact, and the W-2 page does not contain that separate question. The
smallest connected design is therefore to pass through an already-projected
reason sentence when one exists, and otherwise use a bounded plain-language
fallback. For `DEPENDENCY_ABSENT`, say that more return information is needed
and that this screen cannot identify which answer; direct the person to review
the rest of the return, then reload the result. For a blocked result without an
established missing-answer cause, say the figure is unavailable and offer a
reload rather than inventing a question. Do not expose calculation symbols,
rule identifiers, or refusal codes as instructions.

Adding a question-to-dependency mapping would be a materially larger design:
it needs an authoritative connection, likely in tax content or a published
contract, and it risks asking for the wrong answer if inferred from a derived
symbol. That is not justified by these artifacts and remains outside Track 1.

The v6 closure probe confirms the same boundary from the other direction: its
content includes a 1099-INT closure question, but the saved line-2b
presentation carries only `SOURCE_SET_UNCLOSED`, with no attached sentence.
The presence of a mapping in content is not a person-facing question link for
this outcome. The reader should pass through only a sentence already attached
to the saved line; this case uses the general unavailable-result fallback.

## Claims for a later implementation charter

- A rejected value leaves the act-log revision unchanged and shows the
  field-specific correction instruction.
- A successful correction preserves both prior and corrected contributions,
  and the saved presentation matches the recovered current W-2 amount.
- A saved correction with a blocked dependent line says the W-2 change was
  saved, identifies a separate missing answer only when the evidence connects
  it to an existing question, and never renders a null result as zero.
- A computed amount with AUTHORIZATION_ABSENT remains computed while its
  lack of current authorization is clearly shown.
- v6's impact and comparison line roles remain unchanged while v70 retains its
  own line profile.

No production, test, content, schema, or protocol files were changed. The
probe was run directly; no test suite was run. A browser was not launched, and
the controlled omitted-answer case is not a stock fixture workflow.
