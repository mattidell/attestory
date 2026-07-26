# Retrospective — Presentation: Citation Walk on Real Derivation Output

Status: **docs finalized; pending owner merge of PR #77, which closes the
milestone.** Track 1 (renderer, review gate, repair, focused recheck) is
`READY` with CI `verify` green; nothing further is chartered. The
maturity-matrix disposition below is owner-confirmed: Presentation moves to
L2, not L3 (`docs/phases/real-return/maturity-matrix.md`, footnote 5).

## Milestone

- Planning unit: `docs/phases/real-return/milestones/presentation-citation-walk.md`,
  owner-selected 2026-07-25 on ADR-0046 (Presentation Surface Contract,
  ratified same day).
- Implementation: `track/presentation-citation-walk-track1`, one track
  (renderer + fixtures + manifest), one review gate, one repair, one focused
  recheck — all as commits inside the single PR #77, per
  `PROJECT_PLANNING.md`'s merge-unit-equals-review-unit rule.
- Accepted implementation: PR #77, CI `verify` green at `05443d8`,
  mergeable, **not yet merged** (owner-held merge).

## Shipped

A renderer (`tools/presentation_harness/examples/pages/citation-walk.v1.html`)
that consumes `form-field.v3` + `act-derived-publication.v1` records and
produces the citation walk — line → subtotal → per-source disposition →
citation pin → source fact — satisfying every ADR-0046 requirement and
foreclosure:

1. Every numeric disposition kind (`published_value`, `computed_zero`,
   `closure_backed_zero`) renders with a bound citation; a missing
   `field.citation` fails loud rather than rendering uncited (F1, closed in
   repair).
2. Diagnostic eligibility requires the resolved value to be an actual finite
   number, not merely a numeric-kind disposition, so a diagnostic tied to a
   failed-validation input is correctly suppressed (F2, closed in repair).
3. Rejected/tampered values (T1–T3 fault suite) are blanket-redacted, never
   echoed, anywhere in visible text.
4. Blocked-state salience stays section-level; no page-level banner.
5. Citation identity survives reuse across two sites without collision.
6. No `innerHTML`, no new dependency, no framework, no build step.

A committed manifest
(`tools/presentation_harness/examples/manifests/citation-walk.v1.json`)
drives 26 criteria through the completed browser evaluation runner: the
original 23 (five dispositions kinds, T1–T3 fault cases, the settled
exploratory-milestone criteria) plus 3 added during repair proving F1/F2
closed.

## Verification

- Track 1 build: `docs/reviews/charter-2026-07-25-presentation-citation-walk-track1.md`;
  landed `6ce90e7`.
- Track 1 review gate: `docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md`
  — `NOT READY`; measurements 1–8 passed, F1 and F2 blocked.
- Track 1 repair: `docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair.md`;
  landed `8109048`; self-verified 26/26 criteria, exit 0, `git diff --check`
  clean.
- Track 1 repair recheck: `docs/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md`
  — `READY`; F1 and F2 independently confirmed closed, no new ADR-0046
  violation, directly touched invariants (citation reuse, keyboard tab order,
  no new `innerHTML`/dependency) intact; original measurements 2–8
  spot-checked, not re-derived.
- CI `verify` green on PR #77's head (`05443d8`), confirmed directly against
  GitHub, not asserted from a prior report.

## Decisions

- **Owner scope decision, 2026-07-25:** select the Presentation frontier,
  citation-walk spine, prototype-first, now that the browser evaluation
  runner is trustworthy tooling (per the prior milestone).
- **Cap discipline:** the milestone plan's fixed cap (one build, one review
  gate, one repair, one focused recheck) held without exception — unlike the
  prior milestone's R1/R2 residual, no further finding survived the recheck,
  so no owner exception was needed.

## Maturity-matrix disposition (owner-confirmed: L2)

ADR-0046 explicitly declined to make the matrix claim itself, deferring it to
"a later real-data implementation milestone that builds and verifies a
surface against this contract" — this milestone. The matrix's own ladder
defines the levels precisely:

- **L2 — Synthetic:** implemented and verified end-to-end on synthetic
  fixtures.
- **L3 — Real:** operates on the owner's actual data under the ratified data
  boundary.

Track 1's fixtures are, by explicit charter scope, **synthetic only** — "no
real workspace, owner browser, credential, remote URL, or personal output"
(milestone plan, Data Safety). The renderer has never been pointed at a real
resolved run's actual `form-field.v3`/`act-derived-publication.v1` output.

**Decision: the Presentation cell moves to L2, not L3.** By the matrix's own
definition, this milestone earns L2 for the human-surface capability
specifically — down from the prior L3 mark, which predated a working
renderer and was itself a footnote-qualified overstatement ("not a human
surface"). The exact remaining gap to L3 is narrow and named: **exercise the
renderer against one real resolved run's actual output**, under the existing
data boundary (out-of-repo residency, synthetic-by-default review). No
further schema or renderer change is implied — the fixtures already cover
the full dispositions-state matrix; what is missing is real-data exercise,
not more building.

Applied to `docs/phases/real-return/maturity-matrix.md`: the Presentation row
now reads L2 across all domains; footnote 5 rewritten to record the renderer,
its synthetic-only verification, and the named L3 gap; the "as of" date and
the Tier 3 frontier candidate list both updated to match.

## Deviations

None from the ratified plan's exit criteria. Exit criterion 7 ("the
retrospective records the maturity-matrix Presentation cell claim ... or
explicitly declines the claim with the smallest exact gap") is satisfied by
the decline and named gap above, since review returned `READY` but the
milestone's own scope never exercised real data.

## Disposition

- Track 1 is complete and `READY`; PR #77 awaits owner merge.
- The Presentation frontier now has a real, ADR-0046-conformant renderer;
  the remaining gap to a full L3 human-surface claim is real-data exercise,
  named above, not further construction.
- `track/presentation-citation-walk-track1` may be deleted once PR #77
  merges, since its content becomes fully contained in `main`.

## Next

Docs are finalized on this branch, riding inside PR #77 alongside the
reviewed implementation. Merging PR #77 is owner-held and is what closes the
milestone: once merged, this retrospective's status line updates to
**complete** with the merge commit SHA, and the milestone plan's phase-state
pointers advance past this milestone. No further review cycle is open on
Track 1.
