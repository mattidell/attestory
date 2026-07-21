# Track 4 closing note — 1099-DIV closure confirmation and live-run harness extension

Date: 2026-07-20. Builder closing note per charter
`docs/reviews/charter-2026-07-20-dsbs-t4-dividend-live-integration.md`,
deliverable 5 ("close the ledger honestly").

## What this track built

1. **Confirming goldens (deliverable 1).** `tests/test_dsbs_t4_dividend_live_
   integration.py::ClosureAndLineNineConfirmation` proves, specifically
   under the v6-pinned package (not v4, where line-9 v2's dividend
   absorption was first proven), that: a closed-empty 1099-DIV family
   publishes an honest zero pinning the closure finding, not a source
   finding that was never asserted; an open (undeclared-closure) family
   never silently aggregates into a publication (its composing line blocks
   `SOURCE_SET_UNCLOSED`); and line-9 v2 pins line 3b's finding into total
   income. The closure-admission mechanism's general shape — literal-
   current-true is the only empty-set authority, false/absent/displaced/
   truthy-non-boolean/duplicate all fail closed — is proven directly
   against `resolve_closure_admissions` by
   `tests/test_frrs_t4_w2_live_integration.py::W2Closure` over the w2
   mapping; per the charter's own "Scope reconciliation" item 1, the
   dividend closure mappings are structurally identical in shape
   (`source-closure-mapping.v2` schema, `family-horizon`-keyed,
   literal-true-only admission locus), so that proof already covers the
   dividend mappings generically. This track's goldens supply the two
   things that generic proof alone doesn't: live-path confirmation
   specific to the dividend families, and confirmation that v6 still pins
   the same behavior.

2. **Extended `tools/scaffold_live_acts.py`** (owner-held, untracked —
   never part of this branch's diff). Bumped `ADOPTION_FIXTURE` to
   `adopt-core-v6-current.json`; added `f1099div.bundle.json` to
   `BUNDLE_FILES` per the charter, plus `scheduleb.bundle.json` and
   `qdcg.bundle.json` (not named in the charter's literal `BUNDLE_FILES`
   line, but required for the scaffold to actually be usable — see
   "Scope reconciliation discrepancies" below); added the two 1099-DIV
   families to `FAMILIES`; added member-transition templates for the two
   composable boxes (1a, 1b) and a plain-assertion template for the five
   non-composable boxes (2a, 3, 5, 7, 12, via the single
   `tax.us.2025.f1099div.recorded-boxes` fact type — confirmed against the
   live schema, not assumed to be family/member-shaped); and added
   assertion templates for both Track 3 declared-absence citizens
   (`capital-gain-distributions`, `schedule-d-required`) and the three
   Schedule B Part III answers. Smoke-tested end to end: scaffold →
   renumber (kernel projection OK, 23 acts, 8 findings) → `runner.py 1`
   (produces a report, no crash) in a scratch directory outside the repo.

3. **Dividend live-integration test (deliverable 3).**
   `tests/test_dsbs_t4_dividend_live_integration.py::
   ScheduleBRequiredWithQdcgWorksheet` and `::
   ScheduleBNotRequiredWithQdcgWorksheet` prove a single
   `live_coordinate_run` against a complete synthetic act log (W-2 +
   1099-INT + 1099-DIV + every consumable declaration, v6-pinned
   adoption) resolves Schedule B existing (required, published) and
   not-existing (inapplicable) correctly, together with line 16
   publishing under the QDCG worksheet in both branches — the
   composition neither `tests/test_dsbs_t2_schedule_b.py` (v5, no QDCG
   content) nor `tests/test_dsbs_t3_line16_coordinator.py` (v6, no
   Schedule B attachment exercised) proves. Every golden class enters
   exclusively through `live_coordinate_run`; `RunContext(` does not
   appear anywhere in the file (grep-confirmed).

4. **Untracked-path safety net.** `.gitignore` gained `/tools/scaffold_
   live_acts.py` and `/workspace-seed/`.

## Scope reconciliation discrepancies found and how they were handled

- The charter's own named worktree path did not exist on disk; the branch
  `track/dsbs-t4-dividend-live-integration` at the charter commit
  (`56ae7af`) existed only as a ref, not checked out anywhere. Resolved
  per the charter's own fallback instruction: checked it out in the
  isolation-tooling-provided worktree instead.
- Neither `tools/scaffold_live_acts.py` nor `workspace-seed/` existed in
  that worktree (expected — they are untracked, so a fresh worktree never
  carries them). They existed in the separate main checkout; copied from
  there read-only (the main checkout itself was never modified) rather
  than authored from scratch, preserving whatever the owner had already
  begun there.
- `BUNDLE_FILES`: the charter's deliverable 2 text names only
  `f1099div.bundle.json`. Verified against the live v6 package and
  content directory that the Schedule B and QDCG worksheet fact types
  (`foreign-account`/`foreign-trust`/`7b-country`;
  `capital-gain-distributions`/`schedule-d-required`) are registered by
  `scheduleb.bundle.json` and `qdcg.bundle.json` respectively, not by
  `f1099div.bundle.json`. Without adopting those two bundles, a real run
  attempting to assert any Part III answer or either declared-absence
  citizen would fail kernel admission with "unknown fact" — the scaffold
  would silently fail to support exactly the content the charter's own
  objective and deliverable-2 sentence ask it to support ("member-
  transition template for ... the Track 3 declared-absence/signal
  citizens"). This is not new DSBS content, a new schema, or a new
  evaluator operation — both bundles are already-ratified, already-merged
  citizens; adding their adoption to the harness is squarely "harness ...
  only" per the scope fence. Treated as a charter filename staleness the
  charter itself anticipated ("confirm the exact current fixture path at
  build time ... do not assume the name found during charter research"),
  not a charter-stop finding.
- No other discrepancy: the closure-mapping and line-9 v2 "already done"
  claims in the charter's Scope reconciliation items 1–2 were independently
  re-derived (not taken on the charter's word) and confirmed correct
  against the live v6 package and content directory.

## What remains after this track merges

Per the charter's "Exit and owner handoff": nothing in DSBS content,
harness, or test coverage. The only remaining live-data action is the
owner's own quarantined real 1099-DIV run (via the now-extended
`tools/scaffold_live_acts.py`) and its permitted three-fact attestation
(ADR-0031 Decision 7). Track 5 then closes the milestone records.
