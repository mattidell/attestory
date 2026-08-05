# Retrospective — Inbound Capital-Loss Carryovers into 2025 Schedule D

## What differed from the plan

- Track 0 (paper-first) settled all seven named contract questions (D1-D7)
  against real committed source and the actual IRS Capital Loss Carryover
  Worksheet text before any implementation charter existed. Owner review
  of the drafted ADRs surfaced a real product-design gap Track 0 itself
  had not raised: requiring the five 2024 prior-return facts
  unconditionally would force every return in this class through 2024
  numeric entry, including the common case of a taxpayer with no
  prior-year loss at all. ADR-0059 was amended, before ratification, to
  keep the existing `no-inbound-capital-loss-carryovers` declaration as a
  cheap declared-absence satisfaction path (Path A) alongside the full
  five-fact authority (Path B) — reusing the same `conditional_dependency_set`
  branching pattern `selected-preferential-base` already uses, rather than
  inventing a numeric-default adapter that would have blurred the
  provenance distinction between a coarse "no carryover" attestation and
  a contributed real value of exactly zero. Both ADRs (0059, 0060) were
  ratified as amended, with no further dissent.
- Track 1's independent review verified the worksheet arithmetic and
  routing correct by direct inspection of the committed rule JSON (hand-
  tracing both worksheet rules' expression trees against the decision
  record's worked tables, including the eligibility gate's boundary
  case) and found four genuine fixture-coverage gaps: no correction/
  displacement fixture for the five prior-return facts, no Path A/B
  switch fixture, two combined-carryover tests that never asserted line
  21 (so an under-cap combined loss went untested), and no fixture or
  disclosure for the excluded joint-to-separate/canceled-debt cases. One
  findings-only repair closed all four with substantive fixtures; the
  recheck also caught and fixed one real mypy defect (an unimported type
  name masked by postponed annotations) unrelated to the findings
  themselves.
- Track 2 needed no production-code change; the existing presentation
  projection already carried the new signed/carryover values honestly.
  All 8 new goldens were hand-verified against Track 1's already-proven
  arithmetic, including the Form-1040-line-16-vs-Schedule-D-line-16
  distinction and disposition-visibility parity for the missing-
  authority state. No findings.
- **A parallel milestone collided with this one's package version, on
  already-merged history.** While this milestone was in flight, the
  independently developed Schedule B interest-adjustments milestone
  merged to `origin/main` and, within its own commits, published
  `package.core-calculations` `v15` / `published-packages` `v10` that
  silently dropped 45 of the prior milestone's 149 members — the entire
  Schedule-D covered-transaction stack — even though its own branch had
  started from a byte-identical, complete predecessor. This milestone's
  own `v15`/`v10` used the same version numbers for entirely different
  content. The owner force-pushed `origin/main` back to the pre-collision
  merge point to unmerge Schedule B, confirmed the prior milestone
  (PR #157) itself needed no repair, and had Schedule B's package
  regenerated correctly on a separate branch. This milestone rebased onto
  the repaired, re-merged result: renumbered its own package to `v16`/
  `v11` as a validated union (Schedule B's repaired member set, this
  milestone's five rule supersessions applied on top, plus its own nine
  net-new members), keeping both already-merged `v15`/`v10` files
  byte-immutable rather than deleting them.
- **A dry-run semantic-ledger check preceded the real rebase.** Before the
  Schedule B repair had actually merged, a temporary, milestone-local
  checker (never committed) captured this milestone's intended package
  delta, then rehearsed the rebase against the repaired branch's tip on a
  disposable scratch branch. The dry run passed cleanly on the surface
  comparison, but incidentally surfaced a real production defect: three
  separate places in `packages/derivation/package_validation.py` had a
  Schedule-B-specific composition-resolution special case hardcoded to
  `package.get("version") in {"v14", "v15"}` — a version-string allowlist
  that would have silently blocked any future package version, including
  this milestone's real `v16`. Generalizing it (removing the version gate
  since the underlying condition is structural, not version-scoped) was
  folded into the real rebase and verified not to regress Schedule B's
  own `v14`/`v15` validation.
- The real rebase surfaced two further integration gaps the dry run's
  surface-only comparison couldn't see: this milestone's test fixtures
  never asserted Schedule B's three adjustment-family closures, so under
  the merged `v16` package the full downstream tax chain (`taxable-total`
  through `total-tax`) blocked; and a JSON-escaped en-dash in a citation
  string tripped the data-safety digit-run scanner as a false positive.
  Both were fixed and reverified against the full test suite (926
  passed, 20 skipped, zero failures) before curation.

## What it cost

- Two ADRs (0059, 0060) drafted from one paper-first Track 0, amended once
  before ratification, both accepted with no further dissent.
- Two production tracks (Track 1 with one findings-only repair, Track 2
  clean), each independently reviewed `READY`.
- One cross-milestone incident: an already-merged parallel milestone's
  package-version collision, requiring an owner-directed unmerge/re-merge
  of the other milestone and an additive version-repair on this one.
- One generalized production defect in shared derivation code
  (`package_validation.py`), found via a milestone-local dry-run tool
  before it could block the real rebase, fixed and verified against both
  milestones' packages.

## Follow-ups for the next plan

- The dry-run-before-rebase pattern (capture the intended delta, rehearse
  on a scratch branch, verify, only then touch the real branch) is worth
  keeping as a standing discipline whenever a milestone's rebase target
  has moved underneath it during development — it caught a real defect
  before it could block publication, not after.
- `package_validation.py`'s remaining special-case branches (if any) are
  worth a dedicated audit for further hardcoded version strings, now that
  one class of this defect is known to exist.
- Form 8949 is named next in the coverage frontier; the owner has already
  indicated it should be split into a covered-adjustment slice and a
  noncovered-basis slice rather than one general milestone.
