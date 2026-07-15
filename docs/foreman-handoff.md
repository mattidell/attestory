# Foreman Handoff Note

A lightweight, living continuity note — **not a protocol and not a gate.** The
foreman keeps this current *enough* during multi-step work that, if a session
ends mid-task, a fresh foreman can resume without re-deriving everything. Update
it opportunistically; there is no required cadence and no ceremony. It describes
*now*, not history — overwrite stale content freely (durable history lives in
commits, retrospectives, and process logs).

## How the owner relaunches a foreman

Start a fresh session and say, roughly: *"Resume as foreman. Read
`docs/phase-state.md`, `docs/foreman-handoff.md`, and the active plan they point
to, then continue."* The new foreman reads those, reconciles the in-flight state
below against `git status` / `git log`, and proceeds. If the note looks stale
against git, trust git and say so.

## Current state (updated 2026-07-14; branch `milestone/core-tax-conditions`)

- **Seat:** Claude is principal foreman (owner-appointed 2026-07-13). Standing
  owner directives (ADR-0013 amendment + AGENTS.md): rival evidence every round;
  non-accepted ADRs are inert; rejected ADRs retained, never deleted; **no
  foreman-spawned agents without a fresh owner go** — the owner launches every
  builder/reviewer seat from foreman-issued prompts; the foreman integrates
  their dropped files from the working tree, commits with custody, and **splits
  each owner-launched delivery into its own commit, separate from foreman doc
  changes**.

- **The working rhythm (every remediation topic follows it):** foreman drafts
  `plan.md` → owner approves → foreman writes `charter-it1.md`, owner launches
  the incumbent → foreman conformance-checks + commits the exhibit → foreman
  writes `charter-it2.md` (clean-room rival, sealed from it1 **and** any prior
  spike/ADR), owner launches it → conformance + commit → foreman charters two
  committee reviewers (Governance + Adversary, independent contexts, both read
  both designs), owner launches them → foreman triages into
  `evaluation-analysis.md` → foreman drafts the ADR → owner ratifies. Conformance
  is scope-only (two files, exam ≤120 lines, all required cases incl. the
  mandatory ones, Rung boundary held); merits go to the committee.

- **Milestone:** Core Tax Conditions And Presentation Integration — plan
  **revised 2026-07-14** (`docs/phases/foundation/milestones/core-tax-conditions-and-presentation-integration.md`,
  see its revision note). Track 0 (contract decisions) must fully ratify before
  any implementation track opens; implementation tracks 1–7 rebuild on the
  ratified ADRs and inherit their production conditions (threaded per track).

- **Track 0 status — 3 of 5 topics settled:**
  - ✅ Conditional structures → **ADR-0024** accepted; expression extensions → **ADR-0025** accepted.
  - ✅ Non-publication explanations → **ADR-0020** accepted (5 rounds; NPE-G10 fold+fixture-repair lands concurrently in implementation).
  - ✅ **Taxable-interest composition → ADR-0026 accepted (Track 0.a, just closed).** Mechanism + honest-partial OID-inclusive boundary; new provenance-only `composition` pin role; per-constituent `require_closed`; K-1/market-discount and subtractive adjustments (nominee/accrued/premium) deferred to named follow-ons.
  - ✅ **Track 0.b floor — ADR-0027 accepted (2026-07-15).** Hybrid: extend package.v2; it2 typed graph / role canon / package-instance immutability / exclusive projection / form-field producer integrity; it1 `admitted_schemas`; reject path-manifest (0022 superseded); reject it1-alone. **Not Decided N1/N2** (fact-surface versioning ⋂ wholesale adoption; declared composition-obligation trigger) → residual micro-round plan **proposed**: `docs/prototypes/adopted-content-manifests/micro-round/plan.md`. Complete membership surface / full Track 4 closure waits on residual ADR (~0028).
  - 🔧 **Track 0.b residual micro-round — committee complete; ADR-0028 proposed but has an open review finding.** Both exhibits + both reviews under custody. Synthesis: reject it2; carry it1 dual fact surface + non-circular `composition_obligations` with committee tightenings (A4 inclusion covers all of F(P); A7 broaden force-declare beyond family-subtotal-only). Evidence: `micro-round/evaluation-analysis.md`. Draft: `docs/adr/0028-package-fact-surface-and-composition-obligation.md` (**proposed**). **Owner-requested review (2026-07-15) found decision 7 not ratification-ready** — the A7 broadening over-fires on ordinary downstream arithmetic (line 9 = 1a+2b, lines 11/15/16), which the round never tested. Feedback + fix: `micro-round/review-feedback-adr0028.md`. Rest of the round is sound.
  - 🔧 **Track 0.c — Citation resolution (ADR-0018):** after 0028 accepts (default). **No prototype artifact exists at all**.

- **➡️ NEXT ACTION: resolve the ADR-0028 decision-7 review finding, then send to owner.**
  Do **not** send ADR-0028 to ratification as drafted. Per the owner-requested
  review (`micro-round/review-feedback-adr0028.md`): (1) retype decision 7's
  trigger to *same-quantity source aggregation* (fire on ≥2 adopted inputs that
  are alternative sources/subtotals of the published symbol's own quantity — not
  any ≥2 inputs) so it still catches MR-A7's raw-amount line 2b but exempts
  line 9 = 1a+2b; (2) add the negative golden (line 9 validates with no
  `composition_obligations`); (3) run one scoped adversary confirmation pass on
  the trigger boundary both directions before ratification. Then owner ratify.
  On accept: close Track 0.b residual (0027 N1/N2 done); full Track 4 membership
  surface unblocked; sequence Track 0.c plan.

- **ADR ledger:** 0019 rejected; 0023, 0024, 0025, 0020, 0026, **0027 accepted**;
  0022 superseded by 0027; **0028 proposed** (residual N1/N2); 0018 inert.
  Closed-topic detail in each topic's process-log / evaluation-analysis.

- **Git/env hygiene:** use the project `.venv` (system python lacks jsonschema);
  check `git status` before any `git add -A` (owner threads drop uncommitted
  files); the owner sometimes commits a delivery directly (e.g. the TIC
  governance review `15e90f3`) — reconcile against git, don't assume custody.
  Milestone roadmap/handoff will conflict with `main`'s at merge; resolve toward
  the milestone versions.

- **Pending / deferred (owner-timed, not blocking Track 0.b):**
  - Milestone-level **process retrospective** on the delegation experiment —
    rich evidence now in hand across four topics: the two-builder rivalry caught
    an unsound mechanism (ELX-A1 `default_superseded`) and a substantive omission
    (TIC-A1 OID); NPE showed an authored-vs-transcribed defect pattern across
    four drafts; and the skipped-rival defect propagated to 3 inert Track-0 ADRs.
    **Proposed ADR-0013 amendment awaiting ratification here:** foreman-authored
    fixes to adversary/governance findings default to a scoped confirmation pass
    (foreman recommends it proactively; owner is never asked to adjudicate
    "is this in-evidence?"). See ADR-0013 "Amendment (2026-07-15, proposed)".
    Origin: the ADR-0028 decision-7 over-trigger handback.
  - The ADR-0026 deferred follow-ons (further positive interest sources; the
    subtractive-adjustment mechanism) are future decision topics, not this
    milestone's blockers.
  - **Side thread (not foreman scope):** product naming — front-runner
    "Attestory"; `attestory.com` is a 2026-01-30 GoDaddy "Launching Soon"
    registration; owner's USPTO check decides.
