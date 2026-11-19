# Track 1: the full-surface snapshot, diff and strict classifier

Tool: `tools/recorded_replay.py` (docstring has the usage). Tests:
`tests/test_recorded_replay_full_surface.py`. Scripts and summaries are in
this directory. The older pin (`pin_run`, `classify`, `neighbour`) is
unchanged and still tested.

## What the snapshot holds

`snapshot(model, report)` flattens the whole saved presentation model and the
whole saved report into typed records `[kind, identity, attribute, value]`.
Nothing is chosen by line or rule. A real list gives 22,000 to 30,000
records.

- `page`: every section (86 page fields on a real list): identity, value,
  disposition, active codes, the field's label, description, every
  disposition's explain text, blocked codes and categorical render text,
  reasons and questions, citation sites, the finding and its pins.
- `attachment`: every attachment with its title and resolved block.
- `graph`: every explanation-graph node and edge, and the roots.
- `model`: every other model key (disposition nodes, citation groups,
  authorization, section roots, pin labels, unsupported findings).
- `row`: every report row with its full identity and content (artifact,
  symbol, disposition, code, missing names, guard result, pins, finding and
  act id aliases).
- `report`: every other report key (stop reason, authorization, current).
- `error`: for a list that errors or is refused, the exception class and its
  path-masked message. Such a list is compared on class and message.

Lists of identified items (sections, rows, pins, edges, graph nodes) are keyed
by their identity, so an added or removed item is an added or removed record,
and the order of the identified items is a record (`...@order`). Lists of
strings (missing names, codes) are one record, in order. Values compare typed:
`1`, `1.0` and `true` are different.

## What it leaves out, and why (named blind spots)

- The run id: run-specific. A local path is masked only in the message of a
  list that errored or was refused (repair of FSR-R5b: it used to be masked in
  every saved string, so two labels differing only in a path compared equal;
  the identity run below shows the saved strings of all 775 lists carry no
  run-specific path).
- The 24-hex hashes in finding ids and publication act ids. They are hashes of
  the pinned citizen versions, so they differ between cores for identical
  content. A derived finding is aliased by its symbol and the structure of its
  inputs (ids and roles, never versions); its value and version stay compared.
  Findings that share an alias are numbered in graph order. Graph node keys
  (which embed the id and the version) are replaced by `kind:id`. A generated
  id that names no graph node and no report row (found by the mortgage case
  below: a pin in the explanation block's disposition records) is aliased by
  its enclosing record and pin role; two such ids under one record and role are
  numbered in hash order.
- **Blind spot (FSR-R4): the order of hash-keyed list items.** Pins and edges
  that name a derived finding sit in the order of the masked hashes, so their
  relative order is not recorded as a sequence. The order of every other
  identified item is recorded. Partly closed: the page requires every derived
  node's edges, and every page finding's pins, to be in (role, raw id) order
  (it refuses the section otherwise), so the snapshot holds one boolean for
  each (`graph|edges-in-role-id-order`, `page|pins-in-role-id-order`), taken
  before aliasing. A core that stopped sorting changes the boolean and the
  list fails. Pin order in report rows and in the explanation block is not
  covered by such a boolean.
- **Blind spot (FSR-R5a): dictionary key order.** Key order inside an object is
  not recorded. The page renders it in one place,
  `Object.entries(group.recordedApplicableClaims)`, which sets the list order of
  claims in `mortgageBorrowingExplanation`; the snapshot records those keys
  (`recordedApplicableClaims@keys`). No other dictionary's key order is shown
  by the page.
- **Blind spot (FSR-R1): the corpus.** See the next section.

Not a gap: the rendered HTML page is not in the snapshot; it is produced from
the saved model, so a model difference is the evidence.

## What "nothing else changed" covers

It covers the parts of the saved output the recorded corpus reaches. The
snapshot holds every key a model or report has, but the optional model blocks
are only produced when a list has the matching records. Running all 775 lists
on v96 (`optional_blocks_reached` in the summary) reached only
`line21Explanation` (2 lists). No recorded list produces
`provenanceGroups`, `calculationView`, `mortgageInterestExplanation`,
`mortgageBorrowingExplanation` or `f1099kStatementExplanation`. A successor
that changes a mortgage note, a mortgage borrowing explanation value, or a
1099-K or provenance block therefore passes the 775 lists unchanged. A
milestone touching those texts must add a list that reaches the block (the
synthetic mortgage list below is one) and state the reached blocks beside its
claim. `run_full` now reports `optional_blocks_reached` and every unused
expectation by identity (`unused_expectations`), so a declared change that no
list exercised cannot pass unnoticed.

The `notes` texts are saved: resolved members, including `notes`, are in
`mortgageBorrowingExplanation.calculationChain.resolvedContent`, and the page
renders `member.notes`. (An earlier draft of this file said they were not
saved; that was wrong.)

### Synthetic mortgage list (repair of FSR-R1)

`mortgage_explanation_acts()` in `tests/test_recorded_replay_full_surface.py`
builds a synthetic demo.* list (two Form 1098 statements connected to one
borrowing, from the connected-borrowing case of
`tests/test_mortgage_borrowing_calculation.py`, with its package adoption
dropped so a core's adoption applies). Both v95 and v96 produce the
`mortgageBorrowingExplanation` block on it (24 resolved members, 22 with
`notes`; about 20,500 records). It is held by the snapshot, and the controls
`changed_explanation_block_note` (rejected) and `expected_explanation_block_note`
(accepted when declared, with `text_change`) judge it
(`track1-controls.json`, judged on that output only). A note change declared for
another citizen id is not accepted (live test).

`repair_mortgage_run.py` runs v95 against v96 on that list with the same 133
plain-line-texts expectations (`repair-mortgage-v95-v96.json`): 1 list,
expected changes, 0 unexpected, 129 of 133 expectations used. It uses all 15
`notes` and 15 of the 19 version moves that were unused on the 775 lists; the
4 still unused are the attachment rules (the attachment's own version is not
saved when the attachment is blocked or absent). The first attempt on this list
failed with 34 unexpected differences: two generated ids in the block's
disposition pins were not aliased. That was a tool defect (not a core
difference); it is fixed (see the aliasing note above) and tested.

## Diff, classification and the expectation interface

`diff_snapshots(a, b)` returns every difference as
`{change: changed|added|removed, kind, identity, attribute, before, after}`.
`classify_full(a, b, expectations)` returns class `identical`,
`expected_changes` or `unexpected` (any difference not matched), the count,
the per-expectation counts and the full unexpected list.

An `Expectation` must name a kind and an attribute (a regular expression, full
match); `identity` is searched, `change`, `before` and `after` narrow it.
Examples:

    text_change("tax.us.2025.form1040.line-6a",
                "dispositions.computed_zero.explain", "<old>", "<new>")
    version_change("tax.us.2025.rule.attachment.f8949", "v6", "v7")

`text_change` matches the named citizen, the named property and exactly the
old and new sentence (kinds page, attachment and model, because an attachment
title is saved on the attachment and in its citation group).
`version_change` matches the version attribute of that citizen's pins and
nodes moving from the old to the new version. A change to the value of the
same field, a different sentence, or the same sentence on another citizen is
not matched and fails. Expectations are plain data (JSON-able, picklable), so
the same list drives the parallel replay (`run_full`, CLI `full`).

## Controls (before projection)

`standard_controls` mutates deep copies of the saved model or report, then the
snapshot is taken (`track1_controls.py`, `track1-controls.json`). It uses one
recorded list (blocked rows, missing names, questions; 22,146 records, 86 page
fields, 323 rows), one synthetic wage return (line 12e publishes a value;
29,989 records) and the synthetic mortgage list (20,534 records). Every control fails the comparison, and the expected sentence
passes:

| Control | Result |
| --- | --- |
| changed field value (any field) | rejected |
| changed line 12e value | rejected |
| unwatched report row's code | rejected |
| removed field, added field | rejected |
| changed page disposition, changed row disposition | rejected |
| changed missing name | rejected |
| changed question | rejected |
| unexpected changed sentence | rejected |
| expected changed sentence (declared) | accepted |
| changed value of a derived graph node (worksheet finding no page field shows) | rejected |
| changed `dispositionNodes` record | rejected |
| changed `sectionRoots` entry; changed `authorization` status | rejected |
| changed `notes` text in the mortgage explanation block (mortgage list only) | rejected |
| the same, declared with `text_change` (mortgage list only) | accepted |

Synthetic-snapshot tests also cover value type, added and removed rows,
reordered fields, categorical render text, attachment title, report keys,
bounded expectations and failure snapshots.

### Controls against a tool that stops comparing (repair of FSR-R3)

The review showed that dropping graph or model records, or comparing with
plain `==`, left every control green. `repair_mutations.py` replaces one tool
function in memory (nothing is written to the tool or committed as a change to
it), runs the standard controls on the wage and mortgage outputs and the fast
strict-classifier tests, and lists what stops passing
(`repair-mutations.json`). The unmutated run lists nothing.

| Mutation (in memory) | Controls that stop rejecting | Tests that fail |
| --- | --- | --- |
| drop every `graph` record | `changed_graph_node_value` (both outputs) | graph/model comparison (4), order and key-order substitutes, typed values (7) |
| drop every `model` record (other model keys, explanation blocks) | `changed_authorization`, `changed_disposition_node`, `changed_section_root`; on the mortgage output also both explanation-note controls | graph/model comparison (4), order and key-order substitutes, unseen-id aliasing |
| drop the mortgage explanation block only | both explanation-note controls (mortgage output) | key-order substitutes, unseen-id aliasing |
| compare values with plain `==` | none (controls change values to unequal ones) | typed values: `100`/`100.0`, `1`/`True`, `0`/`False`, `1.0`/`True`, and the typed expectation test (5) |

Typed equality is covered by the synthetic tests, not a real-output control:
a control that makes `1` into `1.0` would need a real output whose value is
exactly such a number.

## Demonstration, all 775 recorded lists, 9 parallel workers

Both runs: each list is run on both cores through the real coordinate run in
one worker; strict classify.

(a) v96 against v96 (`track1-identity.json`): 775 identical (691 success,
84 error with the same class and message on both). Wall time 316 s. Rerun
after the repair (path masking removed from saved strings, order booleans and
unseen-id aliasing added): still 775 identical.

(b) v95 against v96 (`track1-v95-v96.json`) with plain-line-texts' declared
changes (every replaced sentence in p0c-wording.json and repair-wording.json,
chained where the repair replaced a first-pass sentence: 71 sentence
expectations; every successor version and the package adoption pin: 62
version expectations; 133 in all): 775 pass (691 expected changes, 84
identical errors), 0 unexpected differences. Wall time 342 s (rerun after the
repair: still 775 pass, 0 unexpected). 99 of the 133 expectations were used.
The summary now lists the 34 unused by identity (`unused_expectations`): 15
`notes` properties, which are saved only inside the
`mortgageBorrowingExplanation` block that no recorded list reaches
(`optional_blocks_reached`: `line21Explanation` on 2 lists, nothing else); and
19 version moves for citizens that are not on any recorded run's saved page,
graph or rows (15 mortgage rules, used on the synthetic mortgage list above;
4 attachment rules, whose version is not saved when the attachment is blocked
or absent).

The first v95 against v96 run, before `text_change` covered the citation
group, failed 366 lists on one difference: an attachment title in
`citationGroups` that plain-line-texts' `expected_model` also replaced
wherever the id appears. That was an incomplete expectation, not a core
difference; the final run above is with it corrected.
