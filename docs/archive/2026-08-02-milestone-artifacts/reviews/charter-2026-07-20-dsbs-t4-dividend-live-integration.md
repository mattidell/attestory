# Charter: Track 4 — 1099-DIV Closure Confirmation and Live-Run Harness Extension

Date: 2026-07-20. Owner-authorized implementation track for the Dividends
and Schedule B Slice. Planning evidence: this charter's own scope
reconciliation (below) against the milestone plan's Track 4 line
(`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md`,
"1099-DIV closure content and live integration") and the FRRS precedent,
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t4-w2-closure-live-integration.md`.
This track implements no new contract — ADR-0014/0017 (closure), ADR-0031/
0032/0033 (live-run capability boundary), and ADR-0035/0036/0038 (dividend/
attachment/QDCG content, already ratified and merged) all already govern.
Branch: `track/dsbs-t4-dividend-live-integration`. The owner holds the
eventual merge.

## Scope reconciliation (read this before building)

The milestone plan's Track 4 sentence bundles four things. Three are
**already done**, landed incidentally by Tracks 1–3; only the fourth is open
work. Do not rebuild what already exists — confirm it with a golden and move
on:

1. **1099-DIV closure-mapping content (ADR-0014/0017)** — **DONE.**
   `packages/content/tax/2025/closure-mapping.f1099div-1a.json` and
   `closure-mapping.f1099div-1b.json` (landed `2a08d80`) are structurally
   identical in shape to the interest closure mappings: `source-closure-
   mapping.v2` schema, `family-horizon`-keyed, admission-locus literal-true
   only. No non-form-dividend analog is needed (dividends are 1099-DIV-only
   per ADR-0035/0016 scope — no equivalent to `non-form-interest` exists in
   the milestone plan). **Deliverable 1 below is a confirming golden, not new
   content.**
2. **Line-9 total-income extension to include 3b** — **DONE.**
   `rule.form1040-line9.v2.json` already sums wages + taxable interest +
   `tax.us.2025.dividends.ordinary-total`; v1 is kept as pinned history, no
   v3 exists or is needed. `package.core-calculations.v6.json` (the package
   built for Track 3's QDCG line-16 successor) already pins line-9 v2
   alongside 3a/3b and the dividend closure mappings. **Deliverable 1 below
   is a confirming golden, not new content.**
3. **The owner's real run and attestation** — **owner-only, not this
   track's or any builder's ground.** No code, fixture, or doc content in
   this charter substitutes for it. See "Owner handoff" below.
4. **Live-run harness extension** — **NOT DONE. This is the track's real
   scope.** `tools/scaffold_live_acts.py` (owner-held, intentionally
   untracked — see Boundary) is stale relative to the now-merged Tracks 1–3:
   its `ADOPTION_FIXTURE` still points at a v3 package (predates the
   dividend closure mappings and QDCG line-16), its `BUNDLE_FILES` list has
   no `f1099div.bundle.json`, its `FAMILIES` list has no dividend family
   entries, and it has no member-transition template for dividend boxes or
   the Track-3 declared-absence/signal citizens. There is also no
   dividend-analog of `tests/test_frrs_t4_w2_live_integration.py` — every
   other prior live-integration precedent (W-2/interest) has one; dividends
   do not yet.

## Objective

Make the owner's eventual real 1099-DIV run possible and prove it works
end-to-end on a complete synthetic analogue: extend the local live-run
scaffolding to produce a full v6-pinned adoption with 1099-DIV facts, and
add the missing dividend live-integration test proving a single
`live_coordinate_run` resolves 1a/1b, 3a/3b, Schedule B Part I/II/III, and
QDCG line 16 together from an authoritative act log — never a `RunContext`
shortcut. This track does not inspect, receive, or record any personal
data.

## Deliverables

1. **Confirming goldens for the two already-landed items.** One golden (or
   extension of an existing Track 1/2 golden — check before adding a new
   one) proving the 1099-DIV closure mappings honestly close under ADR-0014/
   0017 (literal-current-true only; present-without-closure aggregates;
   false/absent/displaced/ambiguous/duplicate blocks), and one proving
   line-9 v2 correctly absorbs 3b into total income under the pinned v6
   package. If equivalent coverage already exists in the Track 1/2/3 test
   files, cite it in the handoff instead of duplicating — this deliverable
   is about closing the ledger honestly, not padding the suite.
2. **Extend `tools/scaffold_live_acts.py` for 1099-DIV.** Bump
   `ADOPTION_FIXTURE` to the fixture that pins `package.core-calculations
   .v6.json` (confirm the exact current fixture path at build time — it may
   have moved since this charter was written; do not assume the name found
   during charter research). Add `f1099div.bundle.json` to `BUNDLE_FILES`.
   Add the `f1099div.1a` and `f1099div.1b` families to `FAMILIES`
   (horizon-genesis + closure-act generation, mirroring the existing
   interest family entries exactly). Add a member-transition template for
   recorded 1099-DIV boxes (1a, 1b, and the non-composable boxes the Track 3
   no-reach-around demonstration names — 2a, 3, 5, 7, 12 — so the scaffold
   can express a real statement's full box set even though only 1a/1b
   compose). Add scaffold support for the two Track 3 declared-absence
   citizens (`tax.us.2025.capital-gain-distributions`,
   `tax.us.2025.schedule-d-required`) so a real run can actually assert
   them. This file is a local dev/runtime convenience script, not a security
   boundary in itself — normal code-quality bar applies — but it is never
   committed (see Boundary).
3. **Dividend live-integration test.** Add the missing precedent —
   structurally mirror `tests/test_frrs_t4_w2_live_integration.py` (same
   synthetic-only discipline, same temp-workspace/capability pattern, same
   `demo.*` actor namespace) — proving a single `live_coordinate_run`
   against a complete synthetic act log (W-2 + 1099-INT + 1099-DIV +
   declarations, v6-pinned adoption) resolves through to Schedule B
   existing/not-existing correctly and line 16 publishing under the QDCG
   worksheet, entering only through the bootstrapped workspace/capability
   path — no caller package/path pin, no raw `RunContext`, no fixture
   adapter shortcut may select live authority.
4. **Untracked-path safety net.** Add `tools/scaffold_live_acts.py` and
   `workspace-seed/` to `.gitignore` (they are currently untracked by
   discipline only, not by mechanism — a future `git add -A` would catch
   them). This is a two-line additive change; do not expand it into a
   broader `.gitignore` audit.
5. **Close the ledger honestly.** A short Track-4 closing note (in the PR
   description or a committed note under `docs/reviews/`) confirming: no
   open ADR-0035/0036/0038 production condition remains unaddressed by
   Tracks 1–4 collectively, and naming explicitly what remains after this
   track merges (only the owner's real run and attestation).

## Scope fence

- Synthetic fixtures and public tax-content bytes only. No personal source,
  manual entry, workspace locator, live report, derived artifact, or
  descriptive attestation content enters Git.
- No OCR, UI, e-file, new tax lines/forms, or coverage expansion beyond what
  Tracks 1–3 already ratified and merged.
- No new schema, no new evaluator operation, no new disposition shape, no
  reopening of ADR-0014/0017/0031/0032/0033/0035/0036/0037/0038 ratified
  decisions.
- Do not touch DSBS content files (rules, schemas, families, closure
  mappings) — they are done; this track is harness and test only. If a gap
  is found that genuinely requires DSBS content changes, that is a
  charter-stop finding to escalate, not a change to make under this
  charter.
- The owner performs the real run after merge; the builder proves only the
  complete synthetic analogue and capability boundaries.

## Evidence and verification

- The confirming goldens (deliverable 1), the new dividend live-integration
  test (deliverable 3), and every existing suite green.
- Full `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m mypy`,
  `.venv/bin/python3 tools/governance_lint.py`, and
  `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — all
  green.
- `git status` at handoff shows `tools/scaffold_live_acts.py` and
  `workspace-seed/` still untracked (now also gitignored) — never staged,
  never committed.
- Named golden classes enter through `live_coordinate_run` from an
  authoritative act log, confirmed by grep at handoff (`RunContext(` may
  appear only in explicitly docstring-labeled non-substitutive supplementary
  classes), per the Track 0a/2/3 discipline.

## Boundary

`tools/scaffold_live_acts.py` and `workspace-seed/` are owner-held run
tooling and stay untracked by absolute rule (ADR-0031) — edit them locally,
never `git add` or commit them, even after deliverable 4 adds them to
`.gitignore`. Values, dispositions, refusal reasons, and workspace locations
never enter the repository, a review, or a chat session. All fixtures and
goldens are manufactured `demo.*`/`demo-*` data per the milestone's
Data-safety section.

## Review gate

One fresh author-independent reviewer, separately chartered after the
builder lands, measures every deliverable above, in particular verifying
deliverable 1's claim that the two already-landed items need no rework
(re-derive it independently, do not take the builder's word) and running the
required live-integration counter-probes (order-independence,
`RunContext(` grep). The owner authorized this builder and reviewer dispatch
in this session; neither may merge, handle personal data, or enlarge scope.

## Exit and owner handoff

The Track-4 PR is merge-ready only after the confirming goldens, the
extended harness, and the dividend live-integration test all pass under the
full battery. After the owner merges it, the only remaining live-data action
is the owner's quarantined real 1099-DIV run and its permitted three-fact
attestation (ADR-0031 Decision 7); Track 5 then closes the milestone
records.
