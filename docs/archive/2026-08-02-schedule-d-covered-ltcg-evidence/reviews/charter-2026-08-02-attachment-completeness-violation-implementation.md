# Attachment Completeness-Violation Semantics — Implementation Charter

Audience: Builder

Status: **chartered for owner launch**

## Context capsule

- **Source ref:** orient from `HEAD` on
  `milestone/schedule-d-covered-ltcg-8a-continuation`, which contains the
  landed Track 2 commit (`37b4426`) and the ratified `docs/adr/0055-attachment-completeness-violation-semantics.md`
  (accepted 2026-08-02, Tier 2).
- **Role:** Builder, High capability. Production integration, not a
  prototype or paper unit — the design questions are already settled by
  the ratified ADR and its paper spike
  (`docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/attachment-completeness-paper-spike.md`).
- **Scope and evidence-rung ceiling:** implement ADR-0055 Decisions 1-5
  through declared schema, content, package wiring, focused tests, and
  production-shaped synthetic coordinator goldens. Ceiling is synthetic
  `live_coordinate_run` integration; no presentation/browser or real-data
  work.
- **Stop conditions:** stop if `attachment-rule.v1`/`v2`/`v3`,
  `attachment.schedule-d` v1, ADR-0036, ADR-0038, ADR-0052/0053/0054/0055,
  or any other accepted ADR or published history would need mutation; if a
  new generic evaluator/marshal operation beyond the one bounded
  `attempt_attachment` branch ADR-0055 Decision 2 describes is required; if
  the value-check needs to read anything other than the current finding
  `attempt_attachment` already fetches for the presence check; or if the
  ADR's paper claims conflict with committed source once you inspect it
  directly.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/0036-schedule-attachment-ontology.md`; `docs/adr/0055-attachment-completeness-violation-semantics.md`
  in full (Decisions 1-5, Production Conditions); the paper spike named
  above; `packages/schemas/tax/attachment-rule.v3.schema.json`;
  `packages/derivation/runner.py`'s `attempt_attachment` and
  `_attachment_family_nonempty_trigger`; `packages/content/tax/2025/attachment.schedule-d.json`
  and its citation/rule peers (line 8a/13/15/16); `packages/content/tax/2025/package.core-calculations.v11.json`
  and `published-packages.v6.json`; `packages/derivation/package_validation.py`,
  `marshal.py`, `live.py`'s attachment-schema dispatch sets (note the exact
  three call sites Track 2 found `attachment-rule.v3` missing from at merge
  time — ADR-0055's Production Conditions call this out explicitly, do not
  repeat the omission); `AGENTS.md`'s Schema Publication Protocol, Fixture
  Rules, and Data Safety Rules.

Before editing, echo the resolved `HEAD`, scope, evidence ceiling, and stop
conditions.

## Goal

Make the Schedule D attachment's own completeness disposition agree with
`selected-preferential-base`'s numeric route on every current fact set: a
present-but-disqualifying declaration (e.g. `no-current-capital-losses =
"no"`) must publish `required-and-incomplete`, naming the violated
declaration and its value, instead of a false `required-and-complete`.

## Deliverables (ADR-0055 Production Conditions)

1. **`attachment-rule.v4` schema.** Additive successor to
   `attachment-rule.v3`: widen `required_answer`'s `check` property to an
   enum of `"presence"` (unchanged existing behavior) and `"value"`
   (carries a required `equals` field naming the categorical value the
   current finding must hold). `v1`/`v2`/`v3` remain byte-for-byte
   immutable. Register the schema, add-only manifest update, hand-written
   positive instance and focused negatives (missing `equals` on a
   `"value"` check, non-categorical `equals` value, unchanged-behavior
   instance under `"presence"`).
2. **`attempt_attachment`'s value-check branch.** One bounded branch: for
   a `"value"`-checked required answer, read the current finding already
   fetched to satisfy presence (no new lookup), compare its value to
   `equals`. A mismatch is a new, distinctly-named violation reason in the
   record/walk vocabulary (versioned schema change, the
   `ITEMIZATION_TIE_OUT_VIOLATION` precedent) feeding the same
   `required-and-incomplete` disposition and non-publication walk the
   presence check already produces. Presence is still checked first,
   independently per answer; one evaluation names every currently missing
   answer and every currently violated answer in the same walk (ADR-0055
   Decision 3) — never only the first of either kind.
3. **Schedule D content successor.** A new version of
   `attachment.schedule-d` adopting `attachment-rule.v4` and
   `{"check": "value", "equals": "yes"}` for all seven
   `schedule-d-boundary.*` declarations. The v1 content remains immutable
   history.
4. **Dispatch-set wiring.** Extend `package_validation.py`, `marshal.py`,
   and `live.py`'s attachment-schema dispatch sets to admit
   `attachment-rule.v4` — the same three call sites Track 2 found
   `attachment-rule.v3` missing from at merge time.
5. **Coherent package graph.** Publish the next core-calculations and
   published-packages successor versions (v12/v7, or whatever the current
   `HEAD` heads are at launch time) folding in the Schedule D content
   successor. Preserve resolution of every prior version.
6. **Authoritative synthetic evidence.** Focused schema/content/package
   tests plus `live_coordinate_run` goldens reproducing the paper spike's
   exact cases: N1 now converges (attachment reads
   `required-and-incomplete`, naming the violated declaration and its
   current value, in the same run where `selected-preferential-base` is
   `inapplicable`); N2 unaffected (still `required-and-incomplete`, naming
   the missing symbol, no value read); P1/P2 unaffected; the T0→T1→T2
   correction lifecycle trace, showing the attachment's disposition now
   changes in step with the correction instead of staying invariant across
   it.

## Boundary

No presentation or browser work, no real session, no edit to any accepted
ADR or published history, no new evaluator/marshal operation beyond the one
named branch, no broader Schedule D class change, no Track 3 presentation
work. Do not copy paper-spike prose into production; implement against the
ratified ADR and current engine patterns.

## Verification before handoff

```text
python3 -m unittest tests.test_schedule_d_covered_ltcg_8a_t1_citizens
python3 -m unittest tests.test_schema_registry
python3 -m unittest tests.derivation.test_package_validation
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Run the full local gate at most once if useful; CI is the gate of record.

## Handoff

Commit the complete working state as one atomic implementation commit.
Leave the tree clean and report the SHA, changed surfaces, focused results,
golden entrypoint evidence, manifest inspection, and any charter-stop
finding. Do not review your own work or begin Track 3.
