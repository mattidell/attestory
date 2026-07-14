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
  - 🔧 **Track 0.b — Adopted-content manifests (ADR-0022): plan drafted, awaiting owner approval.** Inert single-author spike only; needs full remediation. Must reckon with ADR-0006's existing package-as-closed-manifest substrate, ADR-0025's new schema versions (`fact-type.v2`, `artifact-package.v2`, `derived-finding.v2`, `rule-artifact.v2`, `operation-semantics.v2`), and ADR-0026's new `composition` citizen + pin role. Plan: `docs/prototypes/adopted-content-manifests/plan.md`.
  - 🔧 **Track 0.c — Citation resolution (ADR-0018):** last. **No prototype artifact exists at all** — starts from the plan.

- **➡️ NEXT ACTION: owner approve/amend the Track 0.b plan**, then authorize
  chartering. Plan drafted at `docs/prototypes/adopted-content-manifests/plan.md`
  (process log open). Propositions ACM-P1 (membership surface — extend vs
  succeed ADR-0006 over form-fields / source-authority / composition / ELX
  bindings) + ACM-P2 (cross-kind binding + schema-generation coexistence).
  Candidate ADR-0027 superseding inert ADR-0022. Spike is prior art to
  supersede — it ignored the committed package-as-closed-manifest substrate.
  On approval: issue `charter-it1.md` for the High-tier incumbent.

- **ADR ledger:** 0019 rejected (retained); 0023, 0024, 0025, 0020, 0026 **accepted**;
  0018 & 0022 **inert non-conforming drafts** (to be superseded by conforming
  successors, retained). Closed-topic detail lives in each
  `docs/prototypes/<topic>/process-log.md` and `evaluation-analysis.md`.

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
  - The ADR-0026 deferred follow-ons (further positive interest sources; the
    subtractive-adjustment mechanism) are future decision topics, not this
    milestone's blockers.
  - **Side thread (not foreman scope):** product naming — front-runner
    "Attestory"; `attestory.com` is a 2026-01-30 GoDaddy "Launching Soon"
    registration; owner's USPTO check decides.
