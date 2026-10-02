# Track 13 — explicit relationship recording experiment report

## Implemented boundary

The test-only recorder takes a stable claim address, kind, affirmative attestation, evidence address, and explicit references. Financing requires a current `demo.sli-borrowing` entity and the exact current SCHOOL fact. Statement membership independently requires that borrowing and the exact current 1098-E box-1 source fact plus literal `named-statement` scope; it does not require schooling. Both source findings use the existing `FINANCE@v1` and `MEMBERSHIP@v1` declarations and categorical values. Membership says only that the borrowing is associated with that named statement; it has no interest portion or treatment meaning.

The recorder validates source identity from the fresh projection's structured keys, never rendered IDs or symbols. It records the supplied claim ID, kind, attestation, exact input references, and scope in synthetic evidence, then admits each source finding through `apply_contribution_batch`. It stages evidence, contribution and assertion acts and changes the caller's act list only after admission succeeds. Nonaffirmative claims produce no act; missing, stale and wrong-kind targets, wrong scope and duplicate current identities are refused before source assertion. An active claim address and active evidence address cannot be reused. After explicit predecessor retraction, a correction may retain the claim address and must supply new evidence; full claim/evidence addresses give its successor distinct finding/contribution addresses.

## Executed source, consumer and saved path

The positive cases begin with Track 12's account and current borrowing, schooling and statement targets, with no FINANCE or MEMBERSHIP source finding. The account-context FINANCE diagnostic is explicitly omitted from the candidate package. The recorder's supplied claims cause their own separately contributed findings. The existing Track 10 source/consumer rules and Track 11 EXPECTED/AVAILABLE declaration pass package admission, ActLog recovery, forward and reference runners, live coordination, and saved-evidence reopening after the live objects and temporary workspace are discarded.

The test's concrete addresses are:

| Supplied claim | Evidence | Admitted finding |
| --- | --- | --- |
| `demo.sli.track13.claim.finance-a` | `demo.evidence.sli.track13.finance-a` | `demo.finding.sli.track13.8fcf2a20a29f8730f665` |
| `demo.sli.track13.claim.member-a-s1` | `demo.evidence.sli.track13.member-a-s1` | `demo.finding.sli.track13.8a05407d2eea7de06fea` |
| `demo.sli.track13.claim.finance-b` | `demo.evidence.sli.track13.finance-b` | `demo.finding.sli.track13.71a047758050094ffb32` |
| `demo.sli.track13.claim.member-b-s2` | `demo.evidence.sli.track13.member-b-s2` | `demo.finding.sli.track13.f7d1dc158847128825c6` |

The two statement claims omit schooling from their supplied references and saved evidence. Their saved consumer support nevertheless reaches the exact financing and SCHOOL source findings actually used by each statement: S1/A closes over its membership, A's financing claim, and the shared SCHOOL finding; S2/B closes over its membership, B's financing claim, and that SCHOOL finding. The account finding is context and is absent from both exact leaf sets. An equal-valued but separately keyed current schooling fact remains distinct; changing A's supplied target retires A's predecessor and admits a successor under the same stable claim ID. S1's exact new leaf set is its original membership, the successor financing finding, and the alternate SCHOOL finding; it excludes both predecessor financing and shared SCHOOL findings. The alternate source value equals the shared source value. S2's publication value and exact pins remain unchanged.

After the financing correction, the predecessor is `displaced`, its successor is `current`, and the other financing and membership findings remain `current`. Withdrawing A's corrected financing finding publishes no opposite relationship; the successor becomes `displaced`, while B and both membership findings remain `current`. S1's saved disposition is blocked with `DEPENDENCY_ABSENT`, missing exactly `demo.sli.track11.financing-expected` and `demo.sli.track11.financing-available`; no S1 publication is saved. S2's saved disposition remains published with its baseline pins, and its publication keeps the same symbol, value, and exact pins. An account-only correction displaces only the prior account finding; retracting the account successor displaces that account finding too, while all four relationship findings remain current and both relationship consumers preserve their symbols, values, and exact input pins.

Correcting the shared SCHOOL source to `demo.finding.sli.track13.school.shared.corrected` displaces the original SCHOOL finding and leaves the corrected finding current. Both relationship assertions remain current. S1's exact leaves are its membership, A's financing finding and the corrected SCHOOL finding; S2's are its membership, B's financing finding and the corrected SCHOOL finding. Neither closure contains the displaced SCHOOL finding. Retracting that SCHOOL successor displaces it, leaves both explicit relationship findings current, and blocks both financing producers with `DEPENDENCY_ABSENT`, missing exactly `demo.sli.track10.schooling`; the S1 and S2 statement dispositions then block with `DEPENDENCY_ABSENT`, missing exactly `demo.sli.track11.financing-available`, and neither result is published. The source assertion is not silently retargeted or withdrawn.

The reopened saved files preserve actual coordinator publications and dispositions, structured fact keys, exact pins, evidence, current/displaced lineage and retraction acts. The carrier's whole-run `complete` is false because it retains unrelated Track 8 horizon pins; the selected relationship dependency sets close completely. This is a carrier horizon limitation, not an unclosed relationship path.

## Refusals and product limits

Unknown attestation creates no act. Wrong named-statement scope, stale schooling reference, wrong-kind borrowing, and duplicate current relationship identity are recorder refusals before contribution. Failed admission leaves the original act list unchanged. The saved evidence preserves the exact synthetic assertion rather than deriving its meaning from the fact ID or consumer symbol.

This fixture convention resolves borrowing entity IDs and exact source finding IDs; it does not select future product namespaces or production recording. Membership records only association to a named statement and says nothing about interest share, whole-loan treatment, legal indebtedness, or deduction. The neutral consumer and its successful status do not select tax treatment. G2 remains open, ADR 0076 Part 3 remains unselected, and worksheet integration remains outside this unit.

## Verification

- `pytest tests/test_sli_track13_explicit_relationship_recording.py -q` after Foreman exact-leaf/disposition review: **5 passed** in 73.95s.
- Earlier combined focused command over Track 13/12/11 passed **12 tests** in 115.55s; Track 12 and Track 11 source/tests were unchanged during the later bounded assertion repair.
- `mypy tools/sli_explicit_relationship_recording_experiment.py tests/test_sli_track13_explicit_relationship_recording.py tests/test_sli_track12_account_reference_boundary.py tests/test_sli_track11_collection_declarations.py`: success, no issues across 4 files.
- `pytest tests/test_kernel_fixtures.py tests/test_envelope_hooks.py -q`: **14 passed, 5 subtests passed** in 3.33s.
- `python3 tools/governance_lint.py`: conformant. `git diff --check`: success.
- Foreman-approved full suite, with local socket permission from process start, ran exactly once in exec session `1565` and exited `0`: **2,388 passed, 20 skipped, 4,499 subtests passed** in 314.84s.
- Captured command:

  ```sh
  set -o pipefail
  mkdir -p temp/track13
  sha256sum tools/sli_explicit_relationship_recording_experiment.py tests/test_sli_track13_explicit_relationship_recording.py tests/test_sli_track12_account_reference_boundary.py > temp/track13/executable.sha256.start
  pytest -q 2>&1 | tee temp/track13/track13-full-suite.log
  suite_status=${PIPESTATUS[0]}
  sha256sum tools/sli_explicit_relationship_recording_experiment.py tests/test_sli_track13_explicit_relationship_recording.py tests/test_sli_track12_account_reference_boundary.py > temp/track13/executable.sha256.end
  printf 'FULL_SUITE_EXIT_CODE=%s\n' "$suite_status"
  cat temp/track13/executable.sha256.start
  cat temp/track13/executable.sha256.end
  exit "$suite_status"
  ```

- Start and end executable hashes matched:
  - `tools/sli_explicit_relationship_recording_experiment.py`: `11251f0c9b7ac3a0aa90a24420a385676e7f5b2d9148b37838fedaba2f0f0bea`
  - `tests/test_sli_track13_explicit_relationship_recording.py`: `a189556dbcb011a8328903310c06810334c5872719b07834c4dc5094b7fc7c80`
  - `tests/test_sli_track12_account_reference_boundary.py`: `e6b4bec43f837b9a7df9289999b6f0d3e90d45007bb6c6e901f204db1c0c99a1`
- Durable ignored full-suite log: `temp/track13/track13-full-suite.log`.
