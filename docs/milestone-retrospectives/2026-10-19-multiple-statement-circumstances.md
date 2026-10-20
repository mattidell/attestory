# Retrospective — More Than One Statement: Keeping Each Account With Its Form

## What differed from the plan

The plan expected to find an existing way to keep each Form 1099-K's answers
with its own calculation. P0 found that recording already keeps statement
identity, but calculation inputs lose it. The P1–P6 papers then drifted toward
a new rule-schema version and an ADR-0077 amendment. Independent review found
that the adopted student-loan worksheet already sums several statements with
no schema change: a plain subtotal rule plus a selection that reads each
statement's result. That pattern ("Candidate C") became the design. The owner
chose Policy 1: combine Box 1a amounts only when every current statement is a
supported personal loss.

Settling which closure authority applies to a successor family version
expanded the milestone. The exact-version candidate selected authority by exact
family version. Independent review showed that a member added through the
other current version left the selected version's old closure and its saved
zero current. The owner approved a lifecycle repair. It became ADR 0079: a
recorded family-version handover, remembered retirement, save-time fences,
and a refusal when two versions are current. The sale route then followed
in Track 1.

## What it cost

- **Paper rounds.** P0 through P7, a lifecycle outline, a carrier comparison
  and a four-increment contract proposal each had their own reviews before
  any production code.
- **An unrun full suite.** The exact-version candidate was accepted on focused tests
  and left CI red for a day: 174 failures from synthetic bases that record v1
  wash-sale chains under packages that map v2. The approved fixture policy
  (fresh v2 bases) repaired them during the handover implementation.
- **CI.** `verify` takes about 2.5 hours on this branch; the last green run
  before the milestone took 1h50m. The owner moved implementation to two
  targeted test lanes, with the full suite and CI at closeout.
- **Builder lineages.** A resumed builder lineage replays its whole context.
  Calls grew from about 0.3M to 6.2M input tokens. The Track 0 evidence unit
  took 4.6 hours, and the closeout run 3.9 hours, mostly polling a running
  suite. Fresh lineages per unit were far cheaper.

## Material dissent

- P6 recommended a schema successor and an ADR-0077 amendment; independent
  review found the omitted adopted precedent, and the design used it.
- The connected sale design was first INCOMPLETE; the exact-version candidate
  was REPAIR REQUIRED (Finding 1); the handover proposal had five wrong
  requirements; the Track 0 design review corrected the version source
  (keep the v1 default, take v2 from the adopted package).
- The Track 0 evidence claimed Form 1040 totals depend on the Schedule 1
  entry. Only the attachment reads it; the Foreman corrected the closure.
- After the final review returned READY and CI was green, the owner
  reproduced four defects that agent reviews missed: a removed statement
  could be recorded again into a displaced fact; two statements whose ids
  compose identically shared one explanation; a populated v1 workspace on v49
  could not re-attest without adding a statement; and a supported loss was
  described as entered while the combined entry was blocked.

## Follow-ups

- A workspace whose Form 1099-K answer is on v1, including "no Form 1099-K",
  must answer again before the successor package calculates the entry.
  Reactivate if real use shows the re-answer is a burden.
- Recovery for logs where two family versions are already current, and a
  full pre-save fold for every act kind. Reactivate if a writer outside the
  recorders appears.
- The sixteen per-statement transport inputs are listed in `live.py`. Move
  them to content if the answer set grows.
- Gain and break-even reporting on Form 8949 and Schedule D; more than one
  Form 1098; the preferential-rate defect; the 22 fast-lane budget failures;
  suite and CI duration. Engineering-health candidates.

## What should change in the next plan

Run the full suite, or a measured targeted lane that covers every sibling
consumer, before calling a change to shared machinery a passing candidate. A
targeted lane must include `python -m mypy`: the lanes here ran tests only,
and ten type errors first appeared in CI on the final head.
Before proposing a schema or ADR change, look for an adopted precedent that
already does the job. Before claiming a neighbor depends on a symbol, list the
content that actually reads it. Test identity with adversarial keys whose
composed ids collide, test the lifecycle after removal and after adoption,
not only the first write, and take displayed wording from the published
result rather than the local reason. Start a fresh builder lineage for each unit,
and have the builder report when a long test run finishes instead of polling.
