# Fresh review: replays compare the whole saved return

Reviewed source: `HEAD` `5f224126ff2873c961cd33dc2cf9d96158fabd49` on
`milestone/full-surface-replay-2025`, range `github/main..HEAD`
(`d9010776..5f224126`, 4 commits; the last adds this review's charter and
is administration). The Orientation Block resolved to the same SHA. After
fetch: 0 behind and 4 ahead of `origin/main`; PR #288 is an open draft, so
the branch is not spent. Worktree was clean before and after the review.

The box: the tool may read two cores' saved presentation models and
reports for every recorded list. It may produce snapshots, diffs and a
strict classification. It may not change `packages/`, existing evidence or
the narrower pin. The claim under review is that a passing comparison
means nothing changed in the saved output except the declared
expectations.

## Verdict

**READY with notes** for the semantic content of Track 1. The snapshot,
diff and strict classifier work as described on the surfaces the corpus
reaches. The controls mutate saved output before the snapshot. Both
demonstrations reproduce. The widened `text_change` was a tool fix. Old
callers are unchanged. The findings narrow the claims the milestone can
make and add evidence for parts that are not tested. They do not show a
defect in the comparison.

The mechanical gate has not been met: see FSR-R6. Publication still needs
a green `verify` on the exact head.

## Findings

### FSR-R1 — should-fix: unused expectations come from surfaces the corpus never reaches, and track1.md misstates why

Location: `docs/phases/engine-breadth/milestones/full-surface-replay-evidence/track1.md:117-119`;
`packages/derivation/presentation_projection.py:3372-3389`;
`packages/presentation/pages/citation-walk.v1.html:799`.

track1.md says the 15 unused `notes` expectations are "not saved in the
model or report". That is wrong. Resolved members, including `notes`, are
saved in `mortgageBorrowingExplanation.calculationChain.resolvedContent`,
and the page renders `member.notes`. I ran all 775 lists on v96 and
counted the optional model blocks. 773 lists produce none of
`provenanceGroups`, `calculationView`, `line21Explanation`,
`mortgageInterestExplanation`, `mortgageBorrowingExplanation` or
`f1099kStatementExplanation`. The other 2 produce only
`line21Explanation`. The 19 "version moves for citizens not present"
describe a different case. Some of those citizens are present by id. For
example, `tax.us.2025.rule.attachment.f8949` is an attachment and has a
citation group on every success. Their own version is not saved, because
the attachment's act is null when it is blocked.

Failure scenario: a successor that wrongly changes a mortgage note, a
mortgage borrowing explanation value, or a 1099-K or provenance block
passes all 775 lists as `expected_changes` or `identical`.

Consequence: evidence scope. "Nothing else changed" holds only for the
saved surfaces the recorded corpus reaches. A content milestone touching
mortgage or 1099-K text cannot use this replay alone.

Smallest fix: correct the track1.md sentence. Have `run_full` report which
optional model blocks the corpus reached, and list unused expectations
(FSR-R2). Milestones then state the reached surface next to their claim.

### FSR-R2 — note: an unused expectation is silent

Location: `tools/recorded_replay.py:962-985` (`classify_full`) and `:1088`
(`run_full`).

An unused expectation cannot hide a difference. Matching requires the
kind, an exact attribute, a bounded identity and exact before/after
values (see below). It can hide the absence of a declared change: a
milestone can declare a sentence or version move that no list exercised,
and the run still reads 775 pass. The summary has only `expected_by_note`.
The demo script computes the unused count; the tool does not.

Fix: add `unused_expectations` (notes) to the `run_full` summary so a
caller cannot overlook a declared change that was never observed.

### FSR-R3 — should-fix: no control or test fails if the graph or model kinds, or typed equality, are removed

Location: `tools/recorded_replay.py:1128-1232` (`standard_controls`);
`tests/test_recorded_replay_full_surface.py:127`.

I patched the tool in memory in a separate process. Each of these tool
mutations left all 11 standard controls passing on a real v96 output:
dropping `graph` records (8,970 of 22,144), dropping `model` records
(3,704), dropping `attachment`, `report`, every `.explain` text, or every
`@order` record; diff ignoring added/removed records (sections and
fields are still caught through `@order`); and expectations ignoring
identity/before/after. The synthetic tests catch the attachment, report,
explain, order, render and loose-expectation mutations. Nothing catches
dropping `graph` or `model`, or replacing typed equality with `==`. The
"value type" test changes 100 to `True`, which `==` already rejects.

Failure scenario: a later refactor stops flattening `explanationGraph` or
`dispositionNodes`. An intermediate finding's value then changes with no
section change (worksheet lines live only there), and every control and
test stays green.

Smallest fix: add one real-output control that changes a derived graph
node's value and one that changes a `dispositionNodes` record. Add
synthetic `1` vs `1.0` and `1` vs `true` cases.

Each existing control does fail when its own part is removed. Dropping
row kind fails the code, disposition and missing-name controls. Dropping
`resolved.value`, `resolved.disposition`, `missing`, `code`, `sentence`
or `label` fails exactly the matching control. The question control
mutates the real question text (`reasons[].sentence`).

### FSR-R4 — note: the order of hash-keyed edges and pins is not checked even as an invariant

Location: `tools/recorded_replay.py:804`;
`packages/presentation/pages/citation-walk.v1.html:912-913`.

Constructed: I swapped two same-role derived edges of
`tax.us.2025.f1099b.box4-amounts-ready` in the saved v96 graph, and
separately two derived pins on `line-eic-a-2`'s finding. Both snapshots
are `identical`. The exclusion's premise holds for current cores, because
the page requires edges in (role, id) order, so their order is hash order.
A core that stopped sorting would make the page refuse the section as
`malformed-shared-explanation`, and the replay would not see it.

Matters: low. Fix: record one boolean per list, taken before aliasing:
"every derived node's edges are in (role, raw id) order".

### FSR-R5 — note: two other exclusions are wider than track1.md says

Location: `track1.md:48`; `tools/recorded_replay.py:777`;
`citation-walk.v1.html:775`.

(a) Dictionary key order is rendered in one place:
`Object.entries(group.recordedApplicableClaims)` sets the list order of
claims. That block is in `mortgageBorrowingExplanation`, which the corpus
never reaches (FSR-R1).

(b) `LOCAL_PATH` masking applies to every saved string, not only to
error messages. Constructed: label "… see /var/demo-a" against
"… see /var/demo-b" classifies `identical`. No current content carries
such strings, so this matters little. Fix: mask paths only in failure
messages, or state the rule.

Checked and not a gap: graph node keys drop a middle number, but that
number is `len(identifier)` (`packages/derivation/explanation_graph.py:32`),
so it carries no information. No real v96 output had same-alias derived
findings (zero `#n` aliases), so alias numbering in graph order hides
nothing here. The rendered HTML is a fixed template outside the core, so
leaving it out is sound.

### FSR-R6 — gate: no green verify on the exact head

PR #288 at `5f224126`: `verify` fails because it is a draft and the full
gate did not run. `quick` fails on
`tests/test_k1_interest_breadth_contracts.py::...test_k1_n6_missing_closure_read_ref_or_pin_rejects`
(fast-lane budget 3.1 s > 3.0 s). This branch does not touch that module;
it appears to be timing. Under the qualitative standard the candidate is
not publication-ready until `verify` is green on the exact head.

## Answers to the charter's questions

1. **Completeness.** Every page field (all text, reasons, questions,
   codes), attachment, graph node and edge, model key and report row is
   held, with typed values. The blind spots are FSR-R1 (corpus reach,
   which is the material one), FSR-R4 and FSR-R5. Aliased hashes and the
   dropped node-key number lose no information.
2. **Strictness.** On the real v95 to v96 diff for one recorded list
   (602 differences), every match landed on the named citizen's own leaf
   identity, and no difference matched more than one expectation.
   `text_change` needs an exact attribute and exact old and new sentences,
   so an unrelated sentence change, or the same sentence on another field,
   fails (synthetic tests and my in-memory loosening both show this).
   Identity is searched across ancestors, so in principle the same exact
   sentence change on a descendant citizen would match. The saved shapes
   are shallow; no real sentence record nests under a second citizen id.
   For unused expectations, see FSR-R2.
3. **Controls.** They mutate deep copies of the saved model and report,
   then take the snapshot, as L16-R1 asked. Line 12e and the unwatched
   nominee-reduction row code are both rejected. Coverage gaps are in
   FSR-R3.
4. **Demonstrations.** I reran v95 to v96 with the declared 133
   expectations: 775 lists, 691 `expected_changes`, 84 identical
   error/error, 0 unexpected, 99 of 133 used, 392 s. The 84 errors are
   domain `FindingModelError`s (companion presence and member
   conformance), not harness faults. I reran with `text_change` limited
   to page and attachment kinds. That reproduced exactly 366 failing
   lists and 617 differences, all `model|changed|title` on
   `citationGroups[<attachment rule>]`, with before and after equal to
   the declared title sentences. Widening the kinds was a tool fix. It
   did not loosen the check: the model kind is still bound by the exact
   attribute and sentence. I did not rerun the v96 to v96 identity run.
5. **Compatibility.** The only removed line from the old code is
   `if args.subcommand == "neighbour":`, which became `elif`. `pin_run`,
   `classify`, `neighbour` and the rerun path are untouched.
   `tests/test_recorded_replay.py` passes.

## What I ran

- `python3 tools/build_orientation_block.py --ref HEAD --charter docs/reviews/full-surface-replay/charter-review.md --role reviewer`;
  `git fetch`; `git rev-list --left-right --count origin/main...HEAD` (0 4); `gh pr list`, `gh pr checks 288`, `gh run view --log-failed`.
- Saved v95 and v96 outputs for `v83/returns/case/a_duplicate_on_direct/recorded`
  via `rr.saved_output`, held outside the repository. On them I made
  in-memory constructions (node-key number, edge and pin swaps, dict key
  order, path mask, claims order), checked leaf precision of expectation
  matches, and applied tool mutations against `run_controls` and the
  synthetic test functions (separate process, nothing written to the
  worktree).
- `rr.run_full("v95", "v96", declared)` and the narrowed variant, all 775
  lists, parallel, with part files outside the repository. A v96 pass over
  all 775 lists counting optional model blocks and error classes.
- `pytest tests/test_recorded_replay.py tests/test_recorded_replay_full_surface.py`
  (28 passed, including the live control test);
  `python3 -m mypy tools/recorded_replay.py tests/test_recorded_replay_full_surface.py`
  (clean); `python3 tools/envelope_scan.py --range github/main..HEAD` and
  `--range main..HEAD` (exit 0).
