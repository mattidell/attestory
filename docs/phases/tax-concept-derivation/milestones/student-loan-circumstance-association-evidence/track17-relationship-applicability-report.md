# Track 17 — relationship applicability report

## Result

Track 15's v34 neutral consumer reproduces the gap: after the exact schooling
finding is retracted, its financing relationship finding remains current and
the v34 rule still publishes `sli.financing.observed`. The separate
`current_claim_applicability` projection marks that relationship
`unresolved-applicability`, but v34 does not use that projection in its rule.

The v35 diagnostic package adds subject-scoped rules that require and read both
the exact relationship and its current schooling or Form 1098-E box-1 source.
The rules join by the relationship's structured keys. A usable neutral
observation therefore pins the relationship finding and target source finding.
If the target finding is retracted, that subject receives a runner-authored
`DEPENDENCY_ABSENT` blocked disposition and no observation publication. The
relationship finding and its history remain intact. This is an admitted
diagnostic consumer explicitly selected in the test; no existing production
route selects it, and registration does not integrate it into a product flow.

The v35 registry preserves every v34 citizen and package entry unchanged. The
new package is `demo.tax.2025.package.sli-relationship-source-diagnostic@v3`
(package checksum `772802e823d58305b6e49a0ca23ce844d2b013768d191ff3db65b546c37316db`).
The release `demo.release.sli-relationship-source.2025@v35` pins registry
SHA-256 `369918dfa7f9415d61c9dc0ee16b060815805528f3e02e7c289889c579484144`;
the release file SHA-256 is
`39a218c5b74652db5c2e2659b5d6d101b03c6fdf996a2e226101810cc2eb359c`.
No published schema or schema checksum manifest changed.

## Executed source and consumer path

`tests/test_sli_track17_relationship_applicability.py` creates synthetic
borrowing, schooling and statement sources, records affirmative claims through
the Track 14 durable recorder, adds the v35 package adoption, then creates a
fresh ActLog before each consumer run. The package is resolved from the exact
v35 release and registry, admitted by `validate_package`, and executed by both
the forward and reference runners.

With two subjects and two statements, every usable v35 result has the exact
relationship finding pin and the current target finding pin, plus its package
adoption and computation pins. Both runners agree on publications,
dispositions and blocked rows. Correcting the first statement's box-1 amount at
the same statement identity keeps its inclusion observation usable and changes
that observation's target pin to the new current statement finding. Correcting
the first schooling description at the same situation identity likewise
refreshes only that financing observation's target pin. The second subject's
observations retain their finding IDs, values and complete pins through both
corrections and later target retractions.

The saved relationship lifecycle is also exercised through v35. Correcting
the first financing claim to an explicitly selected schooling situation
removes only its predecessor observation and publishes the successor with
pins for the successor relationship and its exact current schooling finding.
Withdrawing the first statement-inclusion claim then removes only that
observation. The corrected financing observation and both second-subject
observations keep their finding IDs, values and pins.
Both runners agree after each action.

Retracting the first subject's corrected schooling and statement findings
removes its two usable observations and yields blocked dispositions for the
corresponding relationship subjects. Each blocked row carries the exact
relationship input pin, the v3 adoption pin, the blocked rule identity,
`DEPENDENCY_ABSENT`, and the missing source fact-type ID. The runner's blocked
record exposes the relationship `subject_fact_id` and missing source type; it
does not serialize a standalone expected target fact ID. The test verifies
that the exact target fact ID is recoverable from that relationship's
structured keys and agrees with `current_claim_applicability`'s
`source_fact_id`. The returned state is blocked and unresolved; it does not
become a positive or negative relationship result.

## Same-key composition limit

The saved Track 16 review shows a statement's year, issuer, box-1 total and
source support, then records an explicit statement-inclusion answer for a
selected borrowing. It has no answer about whether that identified
statement–borrowing inclusion still holds after a same-key correction. The
test places two borrowing relationships on one statement, then changes the
statement's amount at the same statement identity. Both relationship claims
and both guarded observations remain current, with their support refreshed to
the new statement finding. The ordinary statement fact and saved review do
not distinguish an amount-only correction from a correction whose borrowing
composition changed.

This experiment establishes the absence of information about the correction's
effect on inclusion. It does not establish that every amount correction needs
reconfirmation or that per-pair questioning is the uniquely smallest remedy.
One proposed product response is to distinguish a known amount-only correction,
an explicit inclusion change, and genuine uncertainty; ask about an identified
pair only when its continued inclusion needs clarification. A coarse signal
that composition changed could help locate affected pairs but cannot answer
for them. Preserve uncertainty; choose no borrowing by label, amount, order or
identity alone. The later
[capability handoff](relationship-capability-handoff.md) records the bounded
correction workflow and its remaining production entry-path limit.

## Limits and verification

The observed values remain neutral relationship observations. This work does
not establish eligibility, amount treatment, allocation, deduction, or any
other tax treatment. A later tax producer may not rely on this diagnostic
package without a separately selected production route and additional
decisions. G2 and ADR 0076 Part 3 remain open.

Verification:

- `python3 -m pytest tests/test_sli_track17_relationship_applicability.py
  tests/test_sli_track15_versioned_source_consumer.py
  tests/test_sli_track16_one_review_input.py
  tests/test_sli_relationship_recording.py -q` — 29 passed, including the
  Track 17 relationship correction and withdrawal case.
- Kernel fixture and envelope tests — 14 passed, 5 subtests passed.
- `python3 -m mypy tests/test_sli_track17_relationship_applicability.py` — clean.
- `python3 tools/governance_lint.py` — conformant.
- `git diff --check` — clean after final edits.
- Historical full suite before the relationship lifecycle test — **2,416
  passed, 20 skipped, 0 failed; exit 0; 325.820 seconds**. Session `14148`;
  pytest reported 324.94 seconds. Retained at `temp/track17/full-suite.log`
  and `temp/track17/full-suite-metadata.json`.
- Final captured full suite after the relationship lifecycle test, with local
  socket access from process start, `pipefail`, and 10 workers — **2,417
  passed, 20 skipped, 0 failed; exit 0; 252.293 seconds**. Session `36988`;
  pytest reported 251.42 seconds. Log and metadata:
  `temp/track17/full-suite-after-lifecycle.log` and
  `temp/track17/full-suite-after-lifecycle-metadata.json`.
- Executable hashes for the final captured run: Python 3.14.3
  `83177d8351dbd470c6072025c5d4a56162437b12110e56f2a798564e64e012e5`;
  pytest CLI
  `ff99a092615ea26925d2cab494fa7504439b7a46fe2b8e8cfb599d43bb73de1a`;
  pytest module
  `ee37885c9583f843390684dfb496907f87a0905128e7a3cf4ad227f49ff34c2d`.
