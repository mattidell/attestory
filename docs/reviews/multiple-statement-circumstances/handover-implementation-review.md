# Review — family-version handover implementation

Audience: Foreman.

- Reviewer, same lineage. HEAD `3fbf0139c6ea73910f1cba1c97706b76e7d61d97` on `milestone/multiple-statement-circumstances-consolidation`. Orientation role: reviewer. Envelope scan `origin/main..HEAD` exited 0. No pytest: no specific failing claim. Candidate `34ca5860` stays the ancestor this work contains; sale Track 0 is not accepted here.

## Verdict

**READY.** The five commits implement the approved contract. Finding 1's both-current admission is refused, and the sale route can rely on that authority boundary. The owner may accept ADR 0079 subject to CI.

## Fold and fences

`horizons.apply_handover` (`packages/kernel/horizons.py:177-247`) enforces the six preconditions and returns a new state only after they pass: same family and scope, distinct versions, predecessor horizon current, exactly one active chain for that family and scope, successor chain absent and not in `retired_chains`, fresh successor horizon id. The predecessor chain key is removed from `current_by_chain` and added to `retired_chains`. The successor citizen is `family-horizon.v1` with `predecessor` set to the old horizon id (`horizons.py:228-229`). `apply_genesis` and `apply_transition` refuse a retired chain key (`horizons.py:104-105`, `137-138`). `apply_family_handover` (`findings.py:816-841`) supersedes the predecessor entity and introduces the successor entity; a failed entity check raises before the caller receives a new `FindingState`.

`ActLog.append` and `append_batch` (`act_log.py:223-228`, `285-290`) project the log, run the ADR-0077 step when it applies, then for `horizon-genesis`, `member-transition`, and `family-handover` run the second-genesis rule on genesis only and `apply_act` before any write. `read` parses and schema-validates (`act_log.py:146-184`). `project` folds acts (`findings.py:1440-1444`) and does not call `_enforce_second_genesis_rule`. A historical two-genesis log written on disk stays readable and projects both chains (`tests/test_family_handover_actlog.py:315-342`). A direct closure assertion on a retired horizon is saved and fails later at `project` (`tests/test_family_handover_actlog.py:440-462`).

## Containment

`marshal_closure_authority` (`packages/derivation/marshal.py:307-333`) raises `SourceAuthorityError` when one family id and scope has more than one current version, keeps `c_ver == version` selection when exactly one chain is current, and still raises when the selected version has chains in more than one scope. The message includes the family id (`marshal.py:316-318`). The helper-log test and `test_marshal_containment_refuses_both_current_log` assert that refusal. A raw second genesis beside a live chain is refused at append with `active chain already exists in scope` and leaves the log unmutated (`tests/test_family_handover_recording.py:94-133`).

## Writers

`record_f1099k_statement_durably` and `record_f1099k_no_statements_durably` take `family_version`, defaulting to `FAMILY_VERSION` `"v1"` (`f1099k_statement_recording.py:51`, `378`, `749`). On a v1 chain and a v1 call they genesis or continue that chain as before. When the current chain's version differs and is older, they stage `family-handover` in the same `append_batch`, then the statement path member-transitions from that successor (`f1099k_statement_recording.py:474-505`, `555-562`; no-statements `790-821`). A numerically newer current chain raises `F1099KRecordingRefused` (`477-480`, `793-796`). The answers writer does not take `family_version` and opens no horizon. Same-member corrections stay assertions. There is still no v2 Form 1099-K declaration; a caller must pass the newer version.

## Fixtures

Wash-sale v2 mappings begin at `package.core-calculations.v32.json`. Schedule D Track 1 adopts v32 and now records those eight families at v2 (`tests/test_schedule_d_form8949_covered_wash_sale_t1.py:274-287`, adoption at 706). Packages through v31 keep v1 bases: 1099-G v20, IRA v26, SSA v28, and Form 1098 Track 2 v29 default `wash_sale_version="v1"`. Form 1098-E v33, the v43 debt-limit cases, and the v44 circumstance cases pass v2. `append_wash_sale_v2_empty_authority` drops v1 wash-sale genesis and closure acts and appends fresh v2 genesis plus a true closure (`tests/source_completeness/fixture_authority.py:75-127`). The `20ee105a` sample-data diff is forty line pairs whose only token change is the family version on the eight wash-sale genesis acts. Expectation edits in that commit are version pins, not amount or disposition changes.

## ADR 0079

The proposed ADR states the dedicated act, the Decision 1 supplement, remembered retirement, containment, owner choices A and targeted fold, the four consequences and not-decided items, and the reliance on ADR-0017 Decisions 3, 5, 6, and 7 and ADR-0077 Part 5. The published manifest only adds `act-family-handover.v1.schema.json`, and its checksum matches the file. The ADR's error phrase omits the family id the code includes; the named error and the failure are the same. That is accurate enough for the owner to accept, subject to CI.
