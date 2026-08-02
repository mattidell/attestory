# Charter: Track 4 — W-2 Closure, Core Package Repair, and Live-Run Integration

Date: 2026-07-18. Owner-authorized implementation track for the First Real
Return Slice. Planning evidence: the two-seat prebuild charter at
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t4-prebuild-analysis.md`. This track
implements accepted ADR-0014, ADR-0027/0028, ADR-0031/0032/0033; it does not
propose a new contract. Branch: `track/frrs-t4-w2-closure-live-integration`.
The owner holds the eventual merge.

## Objective

Make a synthetic, production-shaped run resolve the current user adoption to a
verified repaired core package, project its record-state facts in a bootstrapped
out-of-repo workspace, and produce only its declared outputs and paired run
records. The W-2 family must close honestly under ADR-0014. This track makes the
owner's later first real run possible; it does **not** inspect, receive, or
record any personal data.

## Deliverables

1. **Repair RG-1 as immutable v2 content.** Preserve every published v1 byte.
   Add the accepted versioned W-2 fact/bundle/family/mapping/rule content and a
   new immutable core package version that fixes all eight known contained
   issues—four reachability defects, `SCHEMA_NOT_ADMITTED`, `ROLE_MISMATCH`,
   and two `MAPPING_FACT_TYPE_NOT_ADMITTED`—with no issue allowlist. Regenerate
   the published package registry, Track-3 synthetic release, and adoption pins
   deterministically. Keep the former core-v1 hard-gate refusal as history.
2. **Close W-2 under ADR-0014.** The v2 W-2 source-family and
   `source-closure-mapping.v2` must use exact versioned fact-type pins, a
   family-horizon identity, and the wages quantity vocabulary. Literal-current
   true closure alone authorizes an empty W-2 zero; present wages aggregate
   without closure pins; false, absent, displaced, ambiguous, or duplicate
   closure blocks. The mapping and its closure authority are adopted package
   members, never caller input.
3. **Discharge the Track-4 ADR-0027/0028 ledger.** The repaired core package
   must demonstrate role-canon and form-field producer integrity, versioned
   fact-type/bundle members, dual fact-surface pins and wholesale nested-set
   equality, exact mapping edges, declared composition obligations with full
   binding, closed quantity vocabulary, same-quantity force-declare, successor
   schemas/admitted schemas, and the required reject-direction / accept
   non-trigger goldens. Historical-v1 migration remains an explicit deferral;
   issue-code strings remain non-normative.
4. **Install one production live coordinator.** Starting only from a
   `WorkspaceCapability`, a fixed workspace revision, a declared run scope, and
   the authoritative act log in `L`, it must bootstrap `L`, project record state,
   resolve the current user adoption through the verified release/registry/package
   chain, derive run inputs only from the resolved graph, marshal, execute, and
   write paired run records and outputs only below `LiveWorkspace.live_output_path`.
   No caller package/path/catalog/adoption pin, raw `RunContext`, fixture adapter,
   or direct `runner.run` route may select live authority. A resolver refusal
   creates no run record.
5. **Complete the remaining safety installation checks.** The coordinator must
   structurally require `WorkspaceCapability`/`LiveWorkspace`; install and test
   the ADR-0031 whole-envelope commit and independent push gates with
   integrity-checked hook/guarded-transport entrypoints so `--no-verify` or raw
   push cannot bypass them. Harden the forgeable `MarshalledRunContext` channel
   (review F2), strengthen the physical filesystem-order golden (F4), and make
   the member-byte substitution kill require its exact refusal (F6).
6. **Owner-held first real run protocol.** Provide a documented command/API
   boundary that receives the live locator only through runtime capability. Do
   not create a real-run report, locator, value, identifier, disposition, log,
   or screenshot in the repository. After merged code is available, only the
   owner performs the quarantined run and may add the exact non-descriptive
   attestation allowed by ADR-0031 Decision 7: the run occurred in quarantine,
   dispositions were observed there, and no artifact crossed the boundary.
7. **Close the ledger honestly.** Add a Track-4 closing note that explicitly
   disposes of every ADR-0033 §4 PC(T4) row and records what remains deferred.

## Scope fence

- Synthetic fixtures and public tax-content bytes only. No personal source,
  manual entry, workspace locator, live report, derived artifact, or
  descriptive attestation content enters Git.
- No OCR, UI, e-file, new tax lines/forms, or coverage expansion. Do not alter
  ratified ADRs or rewrite existing published v1 citizens.
- No new schema or contract meaning beyond accepted ADR-0014/0027/0028/0031/
  0032/0033. Surface any unexpressible requirement as a blocking decision.
- The owner performs the real run after merge; the builder proves only the
  complete synthetic analogue and capability boundaries.

## Evidence and verification

- New focused Track-4 suite proving closure truth/pins and every failure mode;
  clean core-v2 resolver success; preserved core-v1 RG-1 refusal; registry and
  release/adoption byte regeneration; whole-envelope commit/push bypass kills;
  coordinator success/refusal record behavior; forged-token, order, and exact
  member-byte kills.
- Existing focused Track-3 resolver/bootstrap and relevant tax/package suites.
- Full `python3 -m unittest`, `python3 -m mypy packages tools tests`, and
  `python3 tools/governance_lint.py` all pass.
- Data-safety scan covers the full Track-4 delta and generated artifacts.
- The implementation group is intentionally one **grouped Track-4 commit**:
  the new immutable package bytes, registry/release/adoption pins, and live
  coordinator must agree atomically. This charter records the grouping before
  implementation, as required by the track-commit protocol.

## Review gate

One fresh author-independent reviewer, separately chartered after the builder
lands, measures every deliverable above and runs the required counter-probes.
It classifies findings as blocking, scope defect, production condition, or
non-blocking. The owner authorized this builder and reviewer dispatch in this
session; neither may merge, handle personal data, or enlarge scope.

## Exit and owner handoff

The Track-4 PR is merge-ready only after synthetic evidence proves the repaired
core graph and capability-gated live coordinator. After the owner merges it, the
only remaining live-data action is the owner's quarantined run and its permitted
three-fact attestation; Track 5 then closes the milestone records.
