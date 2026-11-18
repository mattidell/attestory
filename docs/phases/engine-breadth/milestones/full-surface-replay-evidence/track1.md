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

## What it leaves out, and why

- The run id, and any local path in an error message: run-specific.
- The 24-hex hashes in finding ids and publication act ids. They are hashes of
  the pinned citizen versions, so they differ between cores for identical
  content. A derived finding is aliased by its symbol and the structure of its
  inputs (ids and roles, never versions); its value and version stay compared.
  Findings that share an alias are numbered in graph order. Graph node keys
  (which embed the id and the version) are replaced by `kind:id`.
- The relative order of list items keyed by such a hash (pins and edges that
  name a derived finding). That order is the order of the masked hashes. The
  order of every other identified item is recorded.
- Dictionary key order inside an object (not meaningful in the saved JSON).

Not a gap: the rendered HTML page is not in the snapshot; it is produced from
the saved model, so a model difference is the evidence.

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
recorded list (blocked rows, missing names, questions; 22,144 records, 86 page
fields, 323 rows) and one synthetic wage return (line 12e publishes a value;
29,987 records). Every control fails the comparison, and the expected sentence
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

Synthetic-snapshot tests also cover value type, added and removed rows,
reordered fields, categorical render text, attachment title, report keys,
bounded expectations and failure snapshots.

## Demonstration, all 775 recorded lists, 9 parallel workers

Both runs: each list is run on both cores through the real coordinate run in
one worker; strict classify.

(a) v96 against v96 (`track1-identity.json`): 775 identical (691 success,
84 error with the same class and message on both). Wall time 315 s.

(b) v95 against v96 (`track1-v95-v96.json`) with plain-line-texts' declared
changes (every replaced sentence in p0c-wording.json and repair-wording.json,
chained where the repair replaced a first-pass sentence: 71 sentence
expectations; every successor version and the package adoption pin: 62
version expectations; 133 in all): 775 pass (691 expected changes, 84
identical errors), 0 unexpected differences. Wall time 341 s. 99 of the 133
expectations were used; the 34 unused are 15 `notes` properties (not saved
in the model or report) and 19 version moves for citizens not present on any
recorded run's page, graph or rows.

The first v95 against v96 run, before `text_change` covered the citation
group, failed 366 lists on one difference: an attachment title in
`citationGroups` that plain-line-texts' `expected_model` also replaced
wherever the id appears. That was an incomplete expectation, not a core
difference; the final run above is with it corrected.
