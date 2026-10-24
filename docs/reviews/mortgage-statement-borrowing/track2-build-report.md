# Track 2 build report

## Historical implementation checkpoints

The first checkpoint, `c31fb9ce`, adds the canonical mortgage-borrowing
calculation vocabulary, five local/shared effective-answer mappings, the v54
core successor, and the additive v52 registry/release successor. It preserves
the complete v51 registry entries and the v53 core's 580 members and 26 input
bindings. The new mortgage-borrowing bundle was absent from v53; the existing
F1098 vocabulary v1 and successor vocabulary v2 were already present.

The projection increment adds a narrowly gated saved projection for
current Box 1 reports, current relationship outcomes (including separate
orphans), recorded account claims, actual effective-answer values and pins,
consumed input/choice finding IDs, and the exact line8a disposition. It does not
calculate tax or reread the workspace. Tests use the real Track 1 borrowing
and F1098 answer recorders and the normal coordinator, then inspect the saved
report/model. The third unlinked current-report case is represented once and
does not crash projection. A report's actual reason-chain finding is included
when a current reason publication pins that exact Box 1 finding; in the
two-report probe, this is present only for B, whose report-local answers are
complete, while A's missing local answers remain visibly absent.

The saved-model implementation and recorder-backed integration tests are in
`a82eec30` and `f27e82f8`. Consumer successors and the exact v55/v53 release
chain are in `20c9e9b4`.

The connected calculation increment is committed in `59c557ee`; its projector
compatibility/basis repair is `11d012a6`. The real recorder and coordinator
publish and save a supported two-report line8a finding of $25,500 (22,000 +
3,500), with both Box 1 findings pinned and qualified report-local reason
findings. A separate no-current-borrowing singleton publishes $22,000 and keeps
the legacy mortgage explanation, including its actual basis and answer record.
The v55 amount rule uses an exact v14 citizen with a route-aware declared basis:
the Box 2-as-annual-balance shortcut is explicitly singleton-only; the
connected route uses a separately recorded annual ceiling and retains the
conservative $750,000/$375,000 cap while disclosing the unmodeled higher
grandfathered limit. Categorical reader labels are resolved from exact
producing-rule joined/category references; the old missing-basis error remains
fail-loud, while numeric/date Box titles keep their established source path.

## Current connected shared-mapping increment

The current unmerged v55 candidate now uses the five canonical effective
answer mappings as the connected route. Each reason retains its existing
report-local answer path when no current borrowing link exists; those branches
read exact report-local v2 answers. For an affirmed link, the reason consumes
the canonical effective v1 findings. The five producer dependencies sit on the
exact-link completeness witness, reached through report-effective-support
coverage, so an unresolved producer cannot disappear while an unconnected
singleton remains eligible.

Real recorder/coordinator runs now demonstrate: shared-only local facts on
both reports plus the five agreeing shared claims publish and save one $25,500
line8a finding, with both report reasons qualified and pinning all five of
their effective findings; all five one-at-a-time shared `cannot-tell` cases
withhold line8a despite favorable local answers; disagreeing local/shared
`owes-the-loan` answers withhold line8a in both save orders; and shared
`no-one-else-owes-it=no` maps to an actual `no` finding and
`outside-co-obligor` reason; certificate `received` maps to an actual
`received` finding and `certificate-received` reason. Both shared-only cases
withhold line8a. The unconnected singleton remains $22,000 with its legacy
explanation and basis.
The package-order assertions place the reason, coverage consumer, all-five
completion witness and effective producers in that sequence in both authored
members and `PackageValidation.resolved_members`. Shared-only positive and
uncertainty coordinator runs demonstrate dependency resolution despite this
consumer-first order.

## Evidence and limits

The next consumer increment is now exercised through the same real recorder
and coordinator path. With explicit synthetic current-return answers for the
unrelated line12e prerequisites, the connected $25,500 line8a finding feeds a
published Schedule A attachment and line12e result of $25,500; the saved
attachment citation tie-out reports the same subtotal and retains both
report-specific rows. Removing one Schedule A boundary answer keeps line8a
published but blocks the attachment. A fully supported A/B pair plus an
unlinked current C report blocks both the line8a group amount and line12e.
When A's `owes-the-loan` local answer and the corresponding shared claim are
missing, B's separately recorded local answer publishes only B's effective
finding; A's finding and reason remain absent and no group amount is saved.
These cases show tested consumer and report-key boundaries, not correction or
withdrawal behavior.

One corrected shared cannot-tell proceeds claim is now replaced through the
durable recorder by bought-the-home; both effective findings pin the new
current shared finding, exclude its predecessor, and are pinned by their
qualified report reasons. Withdrawing that shared proceeds answer leaves the
two independently recorded local proceeds answers eligible: the amount remains
$25,500, and a transitive walk through actual published disposition pins
connects each local finding to its report reason. The saved projection currently
omits local-only fallback publications from effectiveAnswers; this does not
change the calculated result, but Track 3's reader should associate exact
published symbols from declared rule outputs and structured subject keys rather
than relying only on inclusion-pin joins.

The lifecycle edge is also executed: correcting the recognized borrowing to
withdrawn while its sole report link remains affirmed blocks line8a rather
than restoring the singleton path. Explicit clear is distinct: one remaining
locally qualified report saves $22,000, while two remaining current reports
block rather than publishing a partial amount.

For limits, an exact B Box 2 value of $250,001 produces a published
principal-within-ceiling finding pinned to B's Box 2 and the selected
$250,000 ceiling, while the connected line8a amount remains blocked. The
report-local residence reason can still be qualified; the account link-support
barrier withholds the group. A shared $800,000 ceiling also withholds the group
without describing the $200,000 Box 2 observation as over-ceiling. A differing
B Box 3 date blocks the connected sum.

Verified so far:

- v54 validates against the current content corpus and retains the v53 input
  bindings and member set as a subset.
- v52 retains all v51 package and citizen entries and the release pins the exact
  v52 registry bytes.
- v55 preserves the v54 base except for the intended mortgage reason/amount,
  line12e, and attachment successors. Line12e v2 explicitly requires/pins Schedule A total;
  attachment v2 retains exactly the seven value-checked boundary declarations
  and removes only the obsolete liability/payment presence check. Registry v53
  retains all v52 entries, which in turn retains v51, and the release pins the
  exact v53 registry bytes.
- The real coordinator's shared-only positive consumes all five effective
  findings transitively in both reasons and saves the $25,500 amount. Five
  separate uncertainty cases show each shared `cannot-tell` blocks its exact
  per-report effective output and the line8a amount; the saved model retains
  the exact uncertain source finding.
- Contradictory local/shared `owes-the-loan` answers block in both save orders.
  The explicit negative “another obligor” and “certificate received” shared
  values also withhold the amount. These checks establish no save-order choice
  for the tested proposition; the remaining disagreement/negative matrix is
  still open.
- The durable projection records actual Box 1 values, current relationship
  claims, effective values/pins, annual ceiling (separate from Box 2), and an
  exact line8a producer disposition. The fixture has
  `AUTHORIZATION_ABSENT`; it is not evidence of return authorization or a
  complete return.
- The extra unlinked third current report appears once and has no relationship;
  only the two explicitly linked reports are in the borrowing's report keys.
- The no-borrowing-activity singleton path in the v55 candidate publishes its
  actual $22,000 amount and legacy explanation with basis/answers. This is
  candidate-path evidence, not a claim that v55 is ratified or a substitute for
  the full compatibility/refusal matrix.

Track 2 remains open. The shared-only amount, all five `cannot-tell` refusals,
singleton compatibility, bounded contrary/disagreement cases, the supported
Schedule A/line12e consumer, one missing-boundary attachment refusal, and
unlinked-report/cross-fill boundaries, one current shared correction, one
shared-answer withdrawal with independently supported local fallback, root
withdrawal, and explicit clear with one versus two reports above are
demonstrated. The withdrawn final report-link case remains blocked without
singleton fallback. After clear, one report with `paid-the-interest=no`
publishes a known numeric zero with a `not-paid` reason; omitting that required
answer leaves the amount blocked. Two fully supported current reports linked
to separately recorded active borrowing references produce no line8a and one
blocked disposition. A true closed-empty F1098 family under the candidate
emits no mortgage explanation or line8a disposition; omitting closure produces
a blocked return disposition, but the generic blocker is not attributed to an
exact closure mapping, so this is not accepted as the inapplicable-line8a
contract. Unrelated dormant-B cross-fill, affirmative orphan, and remaining
independent refusal cases remain unverified.
This checkpoint does not claim complete Track 2 acceptance, return
authorization, or a complete return.

## Focused commands

- `python3 -m pytest -q -o cache_dir=<temporary-cache-dir> tests/test_mortgage_borrowing_calculation.py` — 19 passed before the added correction/withdrawal cases.
- The saved Schedule A citation lineage case passed after asserting both Form 1098 Box 1 finding IDs in attachment citation sites.
- The shared correction and withdrawal-with-local-fallback cases passed through the real recorder and coordinator.
- The root-withdrawal and explicit-clear one/two-report cases passed through the real recorder and coordinator.
- The Box 2-over-ceiling, loose-ceiling-over-cap, and disagreeing Box 3 date cases passed through the real coordinator.
- The explicit-clear known-zero/unresolved cases and withdrawn-final-link case
  passed through the real coordinator.
- The two-active-borrowing-root case passed through the real coordinator.
- Closed-empty/missing-closure probes passed with candidate adoption, with the
  bounded limitation noted above.
- `python3 -m mypy --cache-dir=<temporary-cache-dir> packages tests` — no issues in 332 source files.
- `python3 tools/envelope_scan.py --verify` and `git diff --check` — passed.

Full CI remains the gate of record, particularly because the projector is
under `packages/derivation/`.
