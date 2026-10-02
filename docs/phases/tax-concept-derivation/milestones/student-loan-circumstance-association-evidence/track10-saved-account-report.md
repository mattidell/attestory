# Track 10 saved-account evidence report

## Implemented

Source inspection found that `packages/derivation/runner.py` provides
`append_publications`, which appends each actual derived publication as an
ActLog `derived-publication` act. Inspection of `packages/derivation/live.py`
found that the live coordinator returns actual publications in its outcome,
while its durable run output stores summarized dispositions. This unit
inspected, but did not execute, the `append_publications` route. The experiment
therefore assembles the actual coordinator publications, actual dispositions,
and support/lineage from freshly reopened authoritative acts into a separate
file that can be reopened after the live workspace is gone.

The experimental carrier writes and reopens `sli-saved-account-evidence.v1`
files containing actual live coordinator publications, dispositions, package
and run provenance, full recorded pins, current source findings, structured
fact-key bindings, evidence records, context-only records, and unresolved
support. It records producer selection by actual computation pin IDs and labels
the complement `other_run_publication_ids`; it does not claim those rows are
independent. It does not infer identity or type from a rendered symbol.

Reopen checks publication/run equality, package adoption pins, structured
source identity, evidence references, exact unresolved pin owner/target pairs,
and exact selection/dependency scope. Original blocked disposition rows are
kept intact in `recorded_blocked_dependencies`; their actual missing fact IDs
remain separate from `unresolved_support` and are never rewritten as pins.
`complete` means the recorded whole-run publication/disposition
input-pin/source/evidence closure is present, regardless of whether a consumer
blocked on a known-but-invalid required source. It does not mean that the full
workspace, package citizens, or governance sources have been embedded or
revalidated.

## Demonstrated

- Synthetic schooling, financing, statement membership, and statement-count
  declarations were admitted through real package resolution, contribution
  admission, ActLog persistence, a fresh ActLog reopen, live coordination, and
  both runners.
- Equal-valued distinct schooling situations for borrowing A produced two
  distinct financing publications. The S1 collection retained both finance
  publications, both source findings, both school values, structured
  situation/period/institution/programme/borrowing bindings, and exact input
  pins. The fixture carries 2024 and 2025 as observed source keys.
- With one schooling situation per borrowing, correcting a shared schooling
  source changed S1 and S2 neutral outputs and their exact transitive support.
  The separate S3 output and support rows were byte-equivalent across the
  correction. These neutral values do not select tax treatment.
- A corrected shared schooling source with two different current financing
  values for borrowings A and B caused two subjects of the same real
  required-source consumer to block with `DEPENDENCY_INVALID`. Their original
  disposition rows retain different actual symbols, subject identity, missing
  finance fact IDs, adoption/input pins, and code; the carrier preserves both
  rows without conflating them by artifact ID. Their membership subject inputs
  remain in evaluated support. The two successful finance results per account
  remain publications with their actual inputs.
- A final-producer-only selection still records the exact upstream membership
  and finance publications as required support. They appear in
  `required_support_publication_ids`, not `other_run_publication_ids`.
- An empty selected account result and a supplied unresolved Track 9 account
  are distinct saved states. The empty state retains actual run/package
  provenance and selects zero account publications; it implies no tax default.
  The supplied answer passed contribution admission and produced the real
  neutral `unknown` result, with both unknown borrowing identity and unknown
  statement scope retained in the source value.
- The account's borrowing identity was later resolved by a second ordinary
  contribution against an actual synthetic borrowing entity, while schooling
  and statement scope remained unresolved. A real finding retraction then
  removed the account publication from current support. The saved snapshot keeps
  the actual displaced findings, correction/retraction reasons, and retraction
  act separately from current evaluated support.
- The mixed-period experiment metadata is saved outside findings and
  dispositions with status `unadopted`; it does not create a tax result.
- Negative reopen tests reject removed support, cross-run publication data,
  and a tampered unresolved-pin owner. A broader Track 8 horizon probe remains
  incomplete and records the actual publication/disposition owners of its
  unsupported horizon targets.

For these tests the selected account results are identified by declared
computation IDs. The saved envelope keeps whole-run publication/disposition
closure; other outputs are listed with the neutral
`other_run_publication_ids` label. Actual horizon pins remain unresolved and
make the corresponding whole-run files incomplete. The `DEPENDENCY_INVALID`
refusals are recorded separately and do not themselves make source evidence
incomplete.

## Limits and not demonstrated

- The broader horizon records remain unresolved by this focused carrier.
- Blocked disposition records in the engine do not include producer versions;
  no version is inferred from the artifact ID. The saved refusal preserves the
  actual artifact ID, code, symbol, missing fact IDs, and recorded pins.
- The coordinator output does not expose evaluation type metadata. The file
  records actual publication values and pins without claiming such metadata.
- The saved lineage current/displaced statuses are captured from the freshly
  reopened authoritative projection. The saver validates their structure but
  does not recompute workspace standing from the file.
- The resolution experiment demonstrates account field/reference and
  knownness consumption only. It does not claim that account references alone
  materialize into the staged schooling/financing/membership graph.
- The schooling period/institution/programme keys are synthetic prototype
  grain, not a selected product identity contract.
- G2, worksheet integration, production recording, general application
  adoption, and mixed-period tax treatment remain outside this evidence.

## Verification so far

- `pytest tests/test_sli_track10_saved_account_evidence.py -q`: 7 passed.
- `mypy tools/sli_saved_account_evidence.py tests/test_sli_track10_saved_account_evidence.py`:
  passed.
- `python3 tools/governance_lint.py`: conformant.
- `pytest tests/test_kernel_fixtures.py -q`: 2 passed, 5 subtests passed, 5
  skipped.
- Captured local full-suite command:
  `set -o pipefail; { /usr/bin/time -p pytest -q; } 2>&1 | tee temp/track10/pytest-full.log`
  exited 0 (session handle `51574`): 2,376 passed, 20 skipped, 4,499
  subtests passed; pytest elapsed 146.38s, shell `real` 147.19s. Durable log:
  `temp/track10/pytest-full.log`.
- This is local verification, not the CI gate of record; the CI verify check
  remains authoritative.
- A durable pre-repair failure log is unavailable; the original working source
  was not retained for replay. Current regressions directly exercise exact
  per-subject missing sets, duplicate-rule owner symbols, owner-tampering
  refusal, and selected-publication dependency closure.
- Builder turn/tool-call totals are unavailable.

Disposable JSON files and logs are under ignored `temp/track10/`.
